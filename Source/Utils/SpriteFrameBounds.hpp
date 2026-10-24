/* GPL-3.0-or-later: range checks without touching game state. */
#pragma once
#include <cstddef>
inline bool spriteFrameInRange(int type, int frame, const std::size_t* limits, std::size_t count) {
    return limits && type >= 0 && frame >= 0 &&
           static_cast<std::size_t>(type) < count &&
           static_cast<std::size_t>(frame) < limits[type];
}
