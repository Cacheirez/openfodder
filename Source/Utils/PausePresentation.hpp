// GPL-3.0-or-later. A retained pause scene; no engine or SDL handles.
#pragma once
#include "SurfaceDraw.hpp"
#include "SurfaceLayers.hpp"

namespace openfodder {
// A lifetime identity only. It owns no surface, SDL object or engine state.
// Retained frames keep old identities alive, so allocator address reuse cannot
// make them accidentally match a replacement destination.
struct PresentationDestination {};
using PresentationDestinationId = std::shared_ptr<const PresentationDestination>;
struct PresentationSurface {
    SurfaceDraw indexed;
    RGBLayer backing; // Also preserves legacy pitch padding; PNG uses only this.
    PresentationDestinationId destination;
};
struct PresentationTarget : RGBLayerTarget {
    PresentationDestinationId destination;
};
struct PausePresentation {
    PresentationSurface background, text;
};
struct PausePresentationTarget {
    PresentationTarget background, text;
};
// RGB bytes that survive the next indexed conversion are producer state:
// loaded images, or tail pitch padding outside the packed conversion. Pausing
// used to update these as a side effect of publication. Commit that feedback
// once even when consumers omit presentation, otherwise resuming a mission
// can capture different backing bytes. No texture upload is needed here.
inline bool PresentationKeepsBacking(const PresentationSurface& source, size_t i) {
    return !source.indexed.indices ||
        (i >= source.indexed.width * source.indexed.height &&
         i % source.backing.stride >= source.backing.width);
}
inline uint32_t PresentationPixelAt(const PresentationSurface& source, size_t i) {
    if (PresentationKeepsBacking(source, i)) return (*source.backing.pixels)[i];
    const auto& draw = source.indexed;
    if (i >= draw.width * draw.height || i >= draw.indices->size() ||
        i / draw.width < size_t(draw.skipY) || i % draw.width < size_t(draw.skipX)) return 0;
    const auto index = (*draw.indices)[i];
    return index && index < draw.colors.size() ? draw.colors[index] : 0;
}
inline void CommitPauseBacking(const PausePresentation& scene, uint32_t* background) {
    const auto count = std::min(scene.background.backing.pixels->size(),
                                scene.text.backing.pixels->size());
    const size_t begin = scene.background.indexed.indices
        ? scene.background.indexed.width * scene.background.indexed.height : 0;
    for (size_t i = begin; i < count; ++i) {
        if (!PresentationKeepsBacking(scene.background, i)) continue;
        const auto value = PresentationPixelAt(scene.text, i);
        if (value) background[i] = value;
    }
}
inline PresentationTarget RasterizePresentationSurface(const PresentationSurface& source) {
    PresentationTarget target;
    static_cast<RGBLayerTarget&>(target) = MakeLayerTarget(source.backing);
    target.destination = source.destination;
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
