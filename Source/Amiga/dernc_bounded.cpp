/* Bounded RNC-1 decoder for OpenFodder - GPL-3.0-or-later.
 * Preserves the original decoding grammar using byte offsets, not unchecked
 * pointers. Speculative lookahead at the end is virtually zero-extended;
 * literal bytes always require physical input.
 */
#include "dernc.hpp"
#include <cstdint>
#include <cstddef>
#include <cstring>
#include <limits>

namespace {
uint16_t be16(const uint8_t* p) { return uint16_t((uint16_t(p[0]) << 8) | p[1]); }
uint32_t be32(const uint8_t* p) {
    return (uint32_t(p[0]) << 24) | (uint32_t(p[1]) << 16) |
           (uint32_t(p[2]) << 8) | uint32_t(p[3]);
}
uint32_t mirrorBits(uint32_t x, int n) {
    uint32_t output = 0;
    while (n--) { output = (output << 1) | (x & 1u); x >>= 1; }
    return output;
}
struct BitInput {
    const uint8_t* data;
    size_t size;
    size_t pos = 0;
    uint32_t bits = 0;
    int count = 16;
    bool ok = true;
    explicit BitInput(const uint8_t* p, size_t n) : data(p), size(n) { bits = lookahead(0); }
    uint32_t lookahead(size_t at) const {
        // A final speculative two-byte refill may have fewer than two bytes.
        // The virtual missing bits never become literal bytes.
        uint32_t low = at < size ? data[at] : 0;
        uint32_t high = at < size && size-at > 1 ? data[at+1] : 0;
        return low | (high << 8);
    }
    uint32_t peek(unsigned mask) const { return bits & mask; }
    void advance(int n) {
        if (n < 0 || n > 16 || count < n) { ok = false; return; }
        bits >>= n; count -= n;
        if (count < 16) {
            if (pos > size || size-pos < 2) pos = size;
            else pos += 2;
            bits |= lookahead(pos) << count;
            count += 16;
        }
    }
    uint32_t read(unsigned mask, int n) { auto x = peek(mask); advance(n); return x; }
    void fixLiterals() {
        if (count < 16 || count > 31) { ok = false; return; }
        count -= 16;
        bits &= (uint32_t(1) << count) - 1;
        bits |= lookahead(pos) << count;
        count += 16;
    }
    bool literals(uint8_t* output, size_t countBytes) {
        if (pos > size || countBytes > size-pos) return false;
        std::memcpy(output, data+pos, countBytes);
        pos += countBytes;
        fixLiterals();
        return ok;
    }
};
struct Huffman {
    unsigned code[32] = {};
    uint8_t width[32] = {};
    uint8_t value[32] = {};
    int count = 0;
    bool readTable(BitInput& stream) {
        count = 0;
        int n = int(stream.read(0x1f, 5));
        if (!stream.ok || n > 31) return false;
        if (!n) return true;
        int widthValue[32] = {};
        int maxWidth = 1;
        for (int i=0; i<n; ++i) {
            widthValue[i] = int(stream.read(0x0f, 4));
            if (widthValue[i] > maxWidth) maxWidth = widthValue[i];
        }
        if (!stream.ok) return false;
        unsigned codeValue = 0;
        for (int bitWidth=1; bitWidth<=maxWidth; ++bitWidth) {
            for (int symbol=0; symbol<n; ++symbol) {
                if (widthValue[symbol] != bitWidth) continue;
                if (count >= 32 || codeValue >= (1u << bitWidth)) return false;
                code[count] = mirrorBits(codeValue++, bitWidth);
                width[count] = uint8_t(bitWidth);
                value[count] = uint8_t(symbol);
                ++count;
            }
            codeValue <<= 1;
        }
        return true;
    }
    bool read(BitInput& stream, uint32_t& result) const {
        for (int i=0; i<count; ++i) {
            const uint32_t mask = (1u << width[i]) - 1u;
            if (stream.peek(mask) != code[i]) continue;
            stream.advance(width[i]);
            if (!stream.ok) return false;
            result = value[i];
            if (result >= 2) {
                uint32_t high = 1u << (result - 1);
                result = high | stream.read(high - 1, value[i] - 1);
            }
            return stream.ok;
        }
        return false;
    }
};
}

long rnc_unpack_bounded(const void* packed, size_t packedCapacity,
                        void* unpacked, size_t unpackedCapacity) {
    if (!packed || packedCapacity < 18) return RNC_FILE_SIZE_MISMATCH;
    const uint8_t* p = static_cast<const uint8_t*>(packed);
    if (be32(p) != RNC_SIGNATURE) return RNC_FILE_IS_NOT_RNC;
    const size_t outLen = be32(p+4), inputLen = be32(p+8);
    if (!outLen || !unpacked || outLen > unpackedCapacity ||
        inputLen > packedCapacity-18 || outLen > size_t(std::numeric_limits<long>::max()))
        return RNC_FILE_SIZE_MISMATCH;
    const uint8_t* data = p+18;
    if (rnc_crc(const_cast<uint8_t*>(data), static_cast<long>(inputLen)) != be16(p+14))
        return RNC_PACKED_CRC_ERROR;
    const uint16_t outputCrc = be16(p+12);
    uint8_t* out = static_cast<uint8_t*>(unpacked);
    BitInput bs(data, inputLen);
    bs.advance(2);
    size_t made = 0;
    while (made < outLen) {
        const size_t before = made;
        Huffman raw, distance, length;
        if (!raw.readTable(bs) || !distance.readTable(bs) || !length.readTable(bs))
            return RNC_HUF_DECODE_ERROR;
        unsigned pairs = bs.read(0xffff, 16);
        if (!bs.ok || !pairs) return RNC_HUF_DECODE_ERROR;
        for (unsigned i=0; i<pairs; ++i) {
            uint32_t literalLen = 0;
            if (!raw.read(bs, literalLen)) return RNC_HUF_DECODE_ERROR;
            if (literalLen > outLen-made || !bs.literals(out+made, literalLen))
                return RNC_FILE_SIZE_MISMATCH;
            made += literalLen;
            if (i+1 == pairs) break;
            uint32_t back = 0, run = 0;
            if (!distance.read(bs, back) || !length.read(bs, run))
                return RNC_HUF_DECODE_ERROR;
            if (back >= made || uint64_t(run) + 2 > outLen-made)
                return RNC_FILE_SIZE_MISMATCH;
            for (size_t k=0; k<size_t(run)+2; ++k) {
                out[made] = out[made-size_t(back)-1];
                ++made;
            }
        }
        if (made == before) return RNC_HUF_DECODE_ERROR;
    }
    if (rnc_crc(out, static_cast<long>(made)) != outputCrc)
        return RNC_UNPACKED_CRC_ERROR;
    return static_cast<long>(made);
}
