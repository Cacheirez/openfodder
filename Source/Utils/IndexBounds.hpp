/* GPL-3.0-or-later. Bounds-safe mapping for legacy flat array layout. */
#pragma once
#include <cstddef>
inline bool gameIndexInBounds(long long index, std::size_t count) {
    return index >= 0 && static_cast<unsigned long long>(index) < count;
}
struct GameFlattenedIndex { bool valid; std::size_t group; std::size_t offset; };
inline GameFlattenedIndex gameFlattenedIndex(long long index, std::size_t perGroup,
                                            std::size_t groups) {
    if (index < 0 || perGroup == 0)
        return {false, 0, 0};
    const auto unsignedIndex = static_cast<unsigned long long>(index);
    const auto group = unsignedIndex / perGroup;
    if (group >= groups)
        return {false, 0, 0};
    return {true, static_cast<std::size_t>(group),
            static_cast<std::size_t>(unsignedIndex % perGroup)};
}
