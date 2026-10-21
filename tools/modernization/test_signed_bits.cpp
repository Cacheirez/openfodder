/* GPL-3.0-or-later: 16/32-bit signed wrap and word packing invariants. */
#include "../../Source/Utils/SignedBits.hpp"
#include <cstdint>
#include <cstring>
#include <cstdlib>
#include <iostream>
static void check(bool ok) { if (!ok) std::abort(); }
int main() {
    unsigned long checked=0;
    for (std::uint32_t bits=0; bits<65536; ++bits) {
        const auto raw=static_cast<std::uint16_t>(bits);
        std::int16_t value;
        std::memcpy(&value,&raw,sizeof(raw));
        for (unsigned shift : {1u,3u,4u}) {
            check(static_cast<std::uint16_t>(wrapShiftLeft16(value,shift))
                == static_cast<std::uint16_t>(bits<<shift));
            ++checked;
        }
    }
    const int boundary[] = {-32768,-31459,-5,-1,0,1,32767};
    for (int high : boundary) for (int low : boundary) {
        const auto packed=packWords32(static_cast<std::int16_t>(high),
                                       static_cast<std::int16_t>(low));
        const std::uint32_t reference =
            (static_cast<std::uint32_t>(static_cast<std::uint16_t>(high))<<16) |
             static_cast<std::uint16_t>(low);
        check(static_cast<std::uint32_t>(packed)==reference);
        check(static_cast<std::uint32_t>(wrapShiftLeft32(static_cast<std::int32_t>(high),16))
              == (static_cast<std::uint32_t>(high)<<16));
        checked+=2;
    }
    std::cout << "PASS: " << checked << " 16/32-bit bit-packing cases\n";
}
