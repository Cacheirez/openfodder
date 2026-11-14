#include "../../Source/Utils/DirectionLUT.hpp"
#include <cstdint>
#include <iostream>
#include <cstdlib>

static void expect(bool ok, const char* message) {
    if (!ok) { std::cerr << "FAIL: " << message << '\n'; std::exit(1); }
}

// Previous normalization for in-range magnitudes: test the exact prior logic.
static DirectionLutSample legacy(unsigned x, unsigned y) {
    int bit = 9;
    for (; bit >= 0; --bit) {
        if ((x & (1u << bit)) || (y & (1u << bit))) break;
    }
    const int shift = bit - 4;
    if (shift > 0) { x >>= shift; y >>= shift; }
    return {(y << 5) | x, shift, x, y};
}

int main() {
    static_assert(kDirectionLutSide == 32u, "Expected 32x32 direction table");
    static_assert(kDirectionLutEntries == 1024u, "Unexpected direction table size");
    unsigned long long checked = 0;
    // Every pair within the original accepted magnitude range.
    for (unsigned x = 0; x <= 1023u; ++x) {
        for (unsigned y = 0; y <= 1023u; ++y) {
            const auto now = directionLutNormalize(static_cast<int32_t>(x), static_cast<int32_t>(y));
            const auto old = legacy(x, y);
            expect(now.index == old.index && now.shift == old.shift &&
                   now.x == old.x && now.y == old.y,
                   "normalization changed a legacy-valid pair");
            expect(now.index < kDirectionLutEntries && now.x < 32 && now.y < 32,
                   "legacy pair produced an out-of-range index");
            ++checked;
        }
    }
    expect(directionLutNormalize(0, 0).index == 0, "zero-vector sentinel");
    expect(directionLutNormalize(31, 31).index == 1023, "last LUT entry");
    expect(directionLutNormalize(65535, 65535).index == 1023, "maximum int16 delta");
    expect(directionLutNormalize(-65535, 65535).index == 1023, "negative direction");
    constexpr int32_t coords[] =
        {-32768, -32767, -1024, -512, -1, 0, 1, 512, 1024, 32766, 32767};
    for (auto x1 : coords) for (auto x2 : coords)
        for (auto y1 : coords) for (auto y2 : coords) {
            const auto now = directionLutNormalize(x1 - x2, y1 - y2);
            expect(now.index < 1024 && now.x < 32 && now.y < 32,
                   "int16-coordinate extremes produced invalid index");
            ++checked;
        }
    std::cout << "PASS: " << checked << " bounded direction lookup tests\n";
}
