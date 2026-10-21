/* GPL-3.0-or-later. Validate table indices without altering valid reads. */
#pragma once
#include <cstddef>
inline bool gameIndexInBounds(long long index, std::size_t count) {
    return index >= 0 && static_cast<unsigned long long>(index) < count;
}
