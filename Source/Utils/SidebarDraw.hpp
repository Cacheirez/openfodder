// GPL-3.0-or-later. Retained indexed HUD pixels, after legacy composition.
#pragma once
#include <cstddef>
#include <cstdint>
#include <cstring>
#include <memory>
#include <vector>

namespace openfodder {
struct SidebarDraw {
    std::shared_ptr<const std::vector<uint8_t>> pixels;
    size_t destinationOffset = 0;
    size_t destinationStride = 0;
    size_t rows = 0;
};
// Source contains the legacy 48-byte rows; valid startY/source/target extents
// are the caller's contract. Width/height come from the active legacy surface,
// even when the eventual destination is a different surface.
inline SidebarDraw CaptureSidebar(const uint8_t* source, size_t width, size_t height,
                                   int16_t startY, bool offsetSource) {
    SidebarDraw draw;
    draw.destinationStride = width;
    draw.destinationOffset = 16 * width + 16;
    const unsigned int firstRow = 17 + startY;
    if (firstRow >= height) return draw;
    draw.rows = height - firstRow;
    if (offsetSource && startY) {
        draw.destinationOffset += width * startY;
        source += 48 * startY;
    }
    draw.pixels = std::make_shared<const std::vector<uint8_t>>(source, source + draw.rows * 48);
    return draw;
}
inline void RasterizeSidebar(const SidebarDraw& draw, uint8_t* destination) {
    for (size_t y = 0; y < draw.rows; ++y)
        std::memcpy(destination + draw.destinationOffset + y * draw.destinationStride,
                    draw.pixels->data() + y * 48, 48);
}
} // namespace openfodder
