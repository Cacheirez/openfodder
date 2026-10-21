#pragma once

#include <cstdint>

// Original direction table is indexed as (y << 5) | x, with each
// coordinate normalized to five bits. No engine state is accessed here.
constexpr unsigned kDirectionLutSide = 32u;
constexpr unsigned kDirectionLutEntries = kDirectionLutSide * kDirectionLutSide;

struct DirectionLutSample {
    unsigned index;
    int shift;
    unsigned x;
    unsigned y;
};

inline DirectionLutSample directionLutNormalize(int32_t deltaX, int32_t deltaY) {
    // Widen before negation: even INT32_MIN has a defined magnitude.
    uint32_t x = static_cast<uint32_t>(deltaX < 0 ? -int64_t(deltaX) : int64_t(deltaX));
    uint32_t y = static_cast<uint32_t>(deltaY < 0 ? -int64_t(deltaY) : int64_t(deltaY));
    int bit = 31;
    while (bit >= 0 && !((x | y) & (uint32_t(1) << bit))) --bit;
    const int shift = bit - 4;
    if (shift > 0) {
        x >>= shift;
        y >>= shift;
    }
    return {(y << 5) | x, shift, x, y};
}
