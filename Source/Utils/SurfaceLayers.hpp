// GPL-3.0-or-later. Retained layers and independently owned composition targets.
#pragma once
#include <algorithm>
#include <cstddef>
#include <cstdint>
#include <memory>
#include <vector>

namespace openfodder {
template<class Pixel> struct SurfaceLayer {
    std::shared_ptr<const std::vector<Pixel>> pixels;
    size_t width = 0, height = 0, stride = 0; // stride in Pixel elements
};
template<class Pixel> struct LayerTarget {
    std::vector<Pixel> pixels;
    size_t width = 0, height = 0, stride = 0;
};
using IndexedLayer = SurfaceLayer<uint8_t>;
using RGBLayer = SurfaceLayer<uint32_t>;
using IndexedLayerTarget = LayerTarget<uint8_t>;
using RGBLayerTarget = LayerTarget<uint32_t>;

template<class Pixel>
inline SurfaceLayer<Pixel> CaptureLayer(const Pixel* pixels, size_t count,
                                        size_t width, size_t height, size_t stride) {
    SurfaceLayer<Pixel> layer;
    layer.pixels = std::make_shared<const std::vector<Pixel>>(pixels, pixels + count);
    layer.width = width; layer.height = height; layer.stride = stride;
    return layer;
}
template<class Pixel>
inline LayerTarget<Pixel> MakeLayerTarget(const SurfaceLayer<Pixel>& layer) {
    LayerTarget<Pixel> target;
    if (layer.pixels) target.pixels = *layer.pixels;
    target.width = layer.width; target.height = layer.height; target.stride = layer.stride;
    return target;
}
// Preserve legacy linear traversal, including RGB pitch padding. This is not
// scaling, row alignment, alpha blending, or conversion between palette indices.
template<class Pixel>
inline void CompositeLayer(LayerTarget<Pixel>& target, const SurfaceLayer<Pixel>& source,
                            bool skipZero) {
    if (!source.pixels) return;
    const size_t count = std::min(target.pixels.size(), source.pixels->size());
    for (size_t i = 0; i < count; ++i) {
        const Pixel pixel = (*source.pixels)[i];
        if (!skipZero || pixel) target.pixels[i] = pixel;
    }
}
} // namespace openfodder
