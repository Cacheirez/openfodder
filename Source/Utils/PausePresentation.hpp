// GPL-3.0-or-later. A retained pause scene; no engine or SDL handles.
#pragma once
#include "SurfaceDraw.hpp"
#include "SurfaceLayers.hpp"

namespace openfodder {
struct PresentationSurface {
    SurfaceDraw indexed;
    RGBLayer backing; // Also preserves legacy pitch padding; PNG uses only this.
};
struct PausePresentation {
    PresentationSurface background, text;
};
struct PausePresentationTarget {
    RGBLayerTarget background, text;
};
inline RGBLayerTarget RasterizePresentationSurface(const PresentationSurface& source) {
    auto target = MakeLayerTarget(source.backing);
    if (source.indexed.indices) {
        // SDL_FillSurfaceRect clears visible rows, not pitch padding. The classic
        // draw then copies packed width*height words, even with padded pitch.
        for (size_t y = 0; y < target.height; ++y)
            std::fill_n(target.pixels.begin() + y * target.stride, target.width, 0);
        const auto converted = RasterizeSurface(source.indexed);
        std::copy(converted.pixels.begin(), converted.pixels.end(), target.pixels.begin());
    }
    return target;
}
inline PausePresentationTarget RasterizePausePresentation(const PausePresentation& scene) {
    PausePresentationTarget target;
    target.background = RasterizePresentationSurface(scene.background);
    target.text = RasterizePresentationSurface(scene.text);
    // Original mergeSurfaceBuffer skips a zero RGB word, not palette index zero.
    const size_t count = std::min(target.background.pixels.size(), target.text.pixels.size());
    for (size_t i = 0; i < count; ++i)
        if (target.text.pixels[i]) target.background.pixels[i] = target.text.pixels[i];
    return target;
}
} // namespace openfodder
