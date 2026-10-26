// GPL-3.0-or-later. Presentation-only identity and value snapshot; no gameplay calls.
#pragma once
#include "SpriteDrawState.hpp"
#include <atomic>
#include <stdexcept>
namespace openfodder {
inline uint64_t NextPresentationSerial() {
    static std::atomic<uint64_t> serial{0};
    return serial.fetch_add(1, std::memory_order_relaxed) + 1;
}
struct SoldierSemantic {
    bool valid = false;
    uint64_t scene = 0, generation = 0, interval = 0;
    size_t slot = 0;
    int32_t cameraX = 0, cameraY = 0;
    int16_t tick = 0, xFraction = 0, yFraction = 0, heightFraction = 0;
    int16_t type = 0, sheet = 0, frame = 0, animation = 0, direction = 0;
    uint16_t segment = 0;
    // source is always null in snapshots: resolved resource owns the bytes.
    SpriteDrawInput geometry;
};
}
