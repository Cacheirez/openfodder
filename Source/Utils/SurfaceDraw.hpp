// GPL-3.0-or-later. Owned indexed input and packed RGB output for presentation.
#pragma once
#include <array>
#include <cstddef>
#include <cstdint>
#include <memory>
#include <vector>

namespace openfodder {
struct SurfaceDraw {
    std::shared_ptr<const std::vector<uint8_t>> indices;
    // Effective SDL-mapped XRGB8888 colors, not the current/target fade palette.
    std::array<uint32_t, 255> colors{};
    size_t width = 0, height = 0;
    int16_t skipX = 16, skipY = 16;
};
struct SurfaceDrawTarget {
    size_t width = 0, height = 0;
    std::vector<uint32_t> pixels;
};
// Valid nonnegative skips within the surface and matching source extents are
// the legacy caller's contract. No SDL objects or engine buffers are retained.
inline SurfaceDraw CaptureSurfaceDraw(const uint8_t* indices, size_t size,
                                      const uint32_t* colors, size_t width, size_t height,
                                      int16_t skipX, int16_t skipY) {
    SurfaceDraw draw;
    draw.indices = std::make_shared<const std::vector<uint8_t>>(indices, indices + size);
    for (size_t i = 0; i < draw.colors.size(); ++i) draw.colors[i] = colors[i];
    draw.width = width; draw.height = height;
    draw.skipX = skipX; draw.skipY = skipY;
    return draw;
}
inline SurfaceDrawTarget RasterizeSurface(const SurfaceDraw& draw) {
    SurfaceDrawTarget target;
    target.width = draw.width; target.height = draw.height;
    target.pixels.resize(draw.width * draw.height, 0);
    size_t source = draw.width * draw.skipY, destination = source;
    for (size_t y = draw.skipY; y < draw.height; ++y) {
        source += draw.skipX; destination += draw.skipX;
        for (size_t x = draw.skipX; x < draw.width; ++x) {
            if (source >= draw.indices->size()) break;
            const uint8_t pixel = (*draw.indices)[source++];
            if (pixel) target.pixels[destination] = pixel < draw.colors.size() ? draw.colors[pixel] : 0;
            ++destination;
        }
    }
    return target;
}
} // namespace openfodder
