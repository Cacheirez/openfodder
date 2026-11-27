/* Verify RNC-1 valid public demo fixtures and reject invalid length/CRC inputs.
 * Run this harness with AddressSanitizer and UndefinedBehaviorSanitizer.
 * GPL-3.0-or-later.
 */
#include "Amiga/dernc.hpp"
#include <fstream>
#include <iostream>
#include <vector>
#include <cstring>
#include <cstdint>
#include <algorithm>

long rnc_crc(void* p, long n) {
    unsigned short t[256];
    for (unsigned i=0;i<256;++i) {
        unsigned short v=i;
        for (int k=0;k<8;++k) v=(v&1)?(v>>1)^0xA001:(v>>1);
        t[i]=v;
    }
    unsigned short v=0;
    auto b=static_cast<uint8_t*>(p);
    while (n--) { v^=*b++; v=(v>>8)^t[v&0xff]; }
    return v;
}
int main(int argc, char** argv) {
    size_t valid=0, rejected=0;
    for (int i=1;i<argc;++i) {
        std::ifstream f(argv[i],std::ios::binary);
        std::vector<uint8_t> bytes((std::istreambuf_iterator<char>(f)),{});
        if (bytes.size()<18 || std::memcmp(bytes.data(),"RNC\1",4)!=0) continue;
        size_t expected=(uint32_t(bytes[4])<<24)|(uint32_t(bytes[5])<<16)|
                        (uint32_t(bytes[6])<<8)|bytes[7];
        if (!expected || expected>64u*1024u*1024u) continue;
        std::vector<uint8_t> out(expected,0);
        auto unpack=[&](const std::vector<uint8_t>& b,size_t capacity){
            return rnc_unpack_bounded(b.data(),b.size(),out.data(),capacity);
        };
        if (unpack(bytes,out.size()) != static_cast<long>(expected)) {
            std::cerr << "Valid fixture failed: " << argv[i] << '\n';
            return 1;
        }
        ++valid;
        auto b=bytes; b[18]^=1;
        if (unpack(b,out.size())>=0) { std::cerr << "CRC accepted\n"; return 1; }
        ++rejected;
        b=bytes; b.resize(17);
        if (unpack(b,out.size())>=0) { std::cerr << "Short header accepted\n"; return 1; }
        ++rejected;
        b=bytes; b.pop_back();
        if (unpack(b,out.size())>=0) { std::cerr << "Truncated accepted\n"; return 1; }
        ++rejected;
        if (unpack(bytes,expected-1)>=0) { std::cerr << "Small output accepted\n"; return 1; }
        ++rejected;
        for (size_t k=0;k<bytes.size();k+=std::max(size_t(1),bytes.size()/7)) {
            b=bytes; b.resize(k);
            if (unpack(b,out.size())>=0) {
                std::cerr << "Truncated prefix accepted: " << argv[i] << '\n';
                return 1;
            }
            ++rejected;
        }
    }
    std::cout << "RNC bounded audit: valid=" << valid
              << ", rejected_invalid=" << rejected << '\n';
    return valid ? 0 : 2;
}
