/* GPL-3.0-or-later: deterministic oracle captured from original get() on
 * GCC and Clang at O0 and O2, using 512 seeds * 512 consecutive draws.
 * Do not regenerate the oracle when changing the RNG.
 */
#include <cstdint>
#include <cstddef>
#include <ctime>
#include <cstdlib>
#include <cstring>
#include <iostream>
#include "../../Source/Types.hpp"
uint16 tool_DecimalToBinaryCodedDecimal(uint16 n) {
    return static_cast<uint16>((n / 10) * 16 + n % 10);
}
#include "../../Source/Utils/pseudorand.hpp"
static int16 fromBits(std::uint16_t bits) {
    int16 value;
    std::memcpy(&value, &bits, sizeof(value));
    return value;
}
int main() {
    std::uint32_t z = 0xdeadbeefu;
    std::uint64_t hash = UINT64_C(1469598103934665603);
    std::size_t count = 0;
    cPseudorand random(1);
    for(int seed=0;seed<512;++seed) {
        auto next = [&z]() {
            z = 1664525u*z + 1013904223u;
            return fromBits(static_cast<std::uint16_t>(z >> 16));
        };
        const int16 s0=next(), s1=next(), s2=next(), s3=next();
        random.setSeed(s0,s1,s2,s3);
        for(int step=0;step<512;++step) {
            const int16 value = random.get();
            int16 a,b,c,d;
            random.getSeeds(a,b,c,d);
            if(value != a) return 2;
            for(auto component : {a,b,c,d}) {
                hash ^= static_cast<std::uint16_t>(component);
                hash *= UINT64_C(1099511628211);
            }
            ++count;
        }
    }
    if(count != 262144 || hash != UINT64_C(0x6399e004402e9e9d)) {
        std::cerr << "FAIL RNG drift: count=" << count << " hash=" << std::hex << hash << '\n';
        return 1;
    }
    std::cout << "PASS: " << count << " RNG steps match pinned historical state digest\n";
}
