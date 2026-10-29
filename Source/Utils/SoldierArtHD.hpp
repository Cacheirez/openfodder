// GPL-3.0-or-later. Isolated CPU pilot; deliberately not connected to SDL.
#pragma once
#include "SoldierArt.hpp"
namespace openfodder {
struct SoldierArtHDAsset {
    unsigned density = 0;
    std::shared_ptr<const std::vector<uint32_t>> pixels; // straight ARGB, 16d x 14d
};
enum class SoldierArtHDStatus { Replaced, UnsupportedDensity, MissingAsset,
    BudgetExceeded, UnsupportedPitch, ClassicGuard };
struct SoldierArtHDResult {
    PresentationTarget target; // native classic on fallback; packed HD on success
    SoldierArtHDStatus status = SoldierArtHDStatus::ClassicGuard;
    unsigned density = 1;
    int logicalX = 0, logicalY = 0;
    uint64_t scene = 0;
};
// All commands must already satisfy MissionLayers' retained-kernel contract.
// Density 1 is an equivalence oracle only; production candidates are 8 and 12.
// No engine state, resource selection, simulation, palette or SDL calls here.
inline SoldierArtHDResult ComposeSoldierArtHD(const MissionLayerSequence& scene,
        const PresentationDestinationId& destination, bool paletteStable,
        const SoldierArtHDAsset& asset, size_t maxOutputBytes = 64u*1024u*1024u) {
    SoldierArtHDResult out;
    out.target = RasterizeMissionLayers(scene, destination);
    const unsigned d = asset.density;
    if (d != 1 && d != 8 && d != 12) {
        out.status = SoldierArtHDStatus::UnsupportedDensity; return out;
    }
    if (!asset.pixels || asset.pixels->size() != size_t(224)*d*d) {
        out.status = SoldierArtHDStatus::MissingAsset; return out;
    }
    // Native conversion has historical packed/pitched behavior. Do not silently
    // reinterpret padded backing as a modern packed image in this first pilot.
    if (out.target.stride != out.target.width) {
        out.status = SoldierArtHDStatus::UnsupportedPitch; return out;
    }
    const size_t width = out.target.width, height = out.target.height;
    const size_t limit = maxOutputBytes / sizeof(uint32_t) / d / d;
    if (!width || !height || width > limit / height) {
        out.status = SoldierArtHDStatus::BudgetExceeded; return out;
    }
    // Reuse the reviewed eligibility/order/clip/destination policy. Transparent
    // native art removes the selected original body, exposing its actual ground.
    // Later overlapping writes (including same-color and OR) cause full fallback.
    const std::array<uint32_t,224> transparent{};
    const auto ground = ComposeSoldierArt(scene, destination, paletteStable, &transparent);
    if (!ground.replaced) return out;
    PresentationTarget modern;
    modern.destination = destination;
    modern.width = modern.stride = width*d; modern.height = height*d;
    modern.pixels.resize(modern.width*modern.height);
    for (size_t y=0; y<modern.height; ++y)
        for (size_t x=0; x<modern.width; ++x)
            modern.pixels[y*modern.stride+x] = ground.target.pixels[(y/d)*width+x/d];
    for (size_t y=0; y<size_t(14)*d; ++y) for (size_t x=0; x<size_t(16)*d; ++x) {
        const uint32_t src = (*asset.pixels)[y*16*d+x];
        const unsigned alpha = src>>24;
        auto& dst = modern.pixels[(size_t(ground.y)*d+y)*modern.stride+size_t(ground.x)*d+x];
        uint32_t rgb = 0;
        for (unsigned shift : {0u,8u,16u})
            rgb |= ((((src>>shift)&255)*alpha+((dst>>shift)&255)*(255-alpha)+127)/255)<<shift;
        dst = (dst&0xFF000000u)|rgb;
    }
    out.target = std::move(modern); out.status = SoldierArtHDStatus::Replaced;
    out.density = d; out.logicalX = ground.x; out.logicalY = ground.y; out.scene = ground.scene;
    return out;
}
} // namespace openfodder
