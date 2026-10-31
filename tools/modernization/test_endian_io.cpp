/* GPL-3.0-or-later: reference endian and unaligned access regression. */
#include "../../Source/Utils/EndianIO.hpp"
#include <cstdlib>
#include <iostream>
static void check(bool value) { if (!value) std::abort(); }
int main() {
    unsigned checked = 0;
    for (unsigned offset = 0; offset < 4; ++offset)
        for (unsigned value = 0; value < 65536; ++value) {
            unsigned char bytes[16] = {};
            writeUnalignedLE16(bytes + offset, static_cast<std::uint16_t>(value));
            check(readUnalignedLE<std::uint16_t>(bytes + offset) == value);
            check(static_cast<std::uint16_t>(
                      readUnalignedLE<std::int16_t>(bytes + offset)) == value);
            ++checked;
        }
    const unsigned char four[] = {0, 0x78, 0x56, 0x34, 0x12, 0};
    check(readUnalignedLE<std::uint32_t>(four + 1) == 0x12345678u);
    const unsigned char negative[] = {0, 0, 0, 0x80, 0, 0};
    check(static_cast<std::uint32_t>(readUnalignedLE<std::int32_t>(negative))
          == 0x80000000u);
    std::cout << "PASS: " << checked << " unaligned little-endian round trips\n";
}
