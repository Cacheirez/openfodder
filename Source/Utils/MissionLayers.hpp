// GPL-3.0-or-later. Ordered retained mission operations with explicit destinations.
#pragma once
#include "PausePresentation.hpp"
#include "IndexedProducer.hpp"
#include "TerrainDraw.hpp"
#include "SidebarDraw.hpp"
#include "ResolvedSpriteResource.hpp"
#include "SoldierPose.hpp"
#include <cstdlib>
#include <cstring>
#include <stdexcept>

namespace openfodder {
// Names describe provenance, never sorting priority. In particular an early
// cursor command must not be moved after terrain just because it is a cursor.
enum class MissionLayerRole { Terrain, Sprite, Sidebar, Cursor, Surface };
enum class MissionLayerOperation { Pixels, Terrain, Sidebar, Clear, Save, Restore, Soldier };
struct MissionLayer {
    PresentationDestinationId destination;
    MissionLayerRole role = MissionLayerRole::Surface;
    MissionLayerOperation operation = MissionLayerOperation::Pixels;
    IndexedProducerDraw pixels;
    PreparedSpriteDraw soldier;
    std::shared_ptr<const SoldierPose> pose;
    TerrainDraw terrain;
    SidebarDraw sidebar;
    uint8_t clearIndex = 0;
};
struct MissionLayerDestination {
    // Initial indices/backing plus the palette effective at presentation time.
    // Saved indices are independent: Restore may precede the first Save.
    PresentationSurface initial;
    IndexedLayer saved;
};
struct MissionLayerSequence {
    std::vector<MissionLayerDestination> destinations;
    std::vector<MissionLayer> layers; // global production order, including other targets
};
struct MissionLayerComposition {
    size_t poseReplacements = 0, poseFallbacks = 0;
    std::vector<PresentationSurface> surfaces;
    std::vector<IndexedLayer> saved;
};
inline bool HybridMissionArtEnabled() {
    const auto* hybrid = std::getenv("OPENFODDER_SOLDIER_ORDERED_HYBRID");
    const auto* path = std::getenv("OPENFODDER_SOLDIER_ORDERED_MANIFEST");
    const auto* density = std::getenv("OPENFODDER_SOLDIER_HD");
    return hybrid && std::strcmp(hybrid, "1") == 0 && path && *path && density &&
        (std::strcmp(density, "8") == 0 || std::strcmp(density, "12") == 0);
}

// Check the actual clipped reads and writes before the independent classic
// replay invokes its unchecked native kernel. Amiga8 can span row edges.
inline void ValidateMissionSpriteRaster(const SpriteDrawState& draw,
        const ResolvedSpriteResource& resource, size_t width, size_t targetSize) {
    const auto& layout = resource.layout;
    const bool pc = draw.format == SpriteDrawFormat::PC;
    if (draw.format != layout.format || draw.palette != resource.palette ||
        (!pc && (draw.format != SpriteDrawFormat::Amiga8 || layout.width != 320 ||
                 !layout.height || !layout.planes || layout.planes > 8)) ||
        draw.sourceOffset < 0 || draw.rows <= 0 || draw.y < 0 || !width ||
        width > targetSize)
        throw std::invalid_argument("semantic soldier raster layout");

    const auto registers = PrepareSpriteRasterRegisters(draw, layout, width);
    const size_t stride = pc ? 160 : layout.width / 8;
    if (registers.columns < 0 || size_t(registers.columns) > stride ||
        (pc && size_t(registers.columns) * 2 > width))
        throw std::invalid_argument("semantic soldier raster columns");
    const size_t planeOffset = pc ? 0 : size_t(layout.planes - 1) * layout.height * 40;
    const size_t sourceEnd = size_t(draw.sourceOffset) + size_t(draw.rows - 1) * stride +
        size_t(registers.columns) + planeOffset;
    const auto start = std::ptrdiff_t(width) * draw.y + draw.x;
    const auto end = start + std::ptrdiff_t(width) * (draw.rows - 1) +
        registers.columns * (pc ? 2 : 8);
    if (sourceEnd > resource.available() || start < 0 || end > std::ptrdiff_t(targetSize))
        throw std::out_of_range("semantic soldier raster bounds");
}

// Inputs obey the same clipped geometry/extents contracts as the retained
// kernels. Identity is checked before invoking any kernel. Outputs are private;
// no engine Save/Restore, registers, visibility, resource selection or SDL calls.
inline MissionLayerComposition ComposeMissionLayers(const MissionLayerSequence& scene, bool replacePose = false) {
    std::vector<std::vector<uint8_t>> indices, saved;
    MissionLayerComposition result;
    for (const auto& source : scene.destinations) {
        const auto& initial = source.initial;
        if (!initial.destination || !initial.indexed.indices || !source.saved.pixels || !initial.backing.pixels)
            throw std::invalid_argument("mission destination requires identity, indices and backing");
        for (const auto& existing : result.surfaces)
            if (existing.destination == initial.destination)
                throw std::invalid_argument("duplicate mission destination");
        if (source.saved.width != initial.indexed.width ||
            source.saved.height != initial.indexed.height ||
            source.saved.stride != initial.indexed.width ||
            source.saved.pixels->size() != initial.indexed.indices->size())
            throw std::invalid_argument("incompatible saved mission destination");
        indices.push_back(*initial.indexed.indices);
        saved.push_back(*source.saved.pixels);
        result.surfaces.push_back(initial);
    }
    for (const auto& layer : scene.layers) {
        size_t slot = 0;
        while (slot < result.surfaces.size() &&
               result.surfaces[slot].destination != layer.destination) ++slot;
        if (!layer.destination || slot == result.surfaces.size())
            throw std::invalid_argument("unknown mission layer destination");
        auto& target = indices[slot];
        switch (layer.operation) {
        case MissionLayerOperation::Soldier:
        {
            const auto& prepared = layer.soldier;
            const auto& state = prepared.soldier;
            if (!state.valid || !state.scene || !state.generation || !state.interval ||
                state.geometry.source || !prepared.resource)
                throw std::invalid_argument("invalid semantic soldier snapshot");
            auto input = state.geometry;
            input.source = prepared.resource.source();
            const auto draw = PrepareSpriteDraw(input);
            const auto& classic = prepared.draw;
            if (!draw.visible || !classic.visible || draw.x != classic.x || draw.y != classic.y ||
                draw.columns != classic.columns || draw.rows != classic.rows ||
                draw.sourceOffset != classic.sourceOffset || draw.palette != classic.palette ||
                draw.format != classic.format)
                throw std::invalid_argument("semantic soldier geometry differs from classic preparation");
            ValidateMissionSpriteRaster(draw, prepared.resource, result.surfaces[slot].indexed.width, target.size());
            if (replacePose && TryRasterizeSoldierPose(layer.pose, prepared, target.data(),
                    result.surfaces[slot].indexed.width, result.surfaces[slot].indexed.height)) {
                ++result.poseReplacements;
                break;
            }
            if (replacePose) ++result.poseFallbacks;
            RasterizeSprite8(draw, prepared.resource.layout,
                {target.data(), result.surfaces[slot].indexed.width});
            break;
        }
        case MissionLayerOperation::Pixels:
            RasterizeIndexedProducer(layer.pixels, target.data()); break;
        case MissionLayerOperation::Terrain:
            RasterizeTerrain(layer.terrain, target.data(),
                             result.surfaces[slot].indexed.width, target.size()); break;
        case MissionLayerOperation::Sidebar:
            RasterizeSidebar(layer.sidebar, target.data()); break;
        case MissionLayerOperation::Clear:
        {
            std::fill(target.begin(), target.end(), layer.clearIndex);
            std::fill(saved[slot].begin(), saved[slot].end(), layer.clearIndex);
            auto& backing = result.surfaces[slot].backing;
            auto pixels = *backing.pixels;
            // clearBuffer also clears visible SDL rows, preserving pitch padding.
            for (size_t y = 0; y < backing.height; ++y)
                std::fill_n(pixels.begin() + y * backing.stride, backing.width, 0);
            backing.pixels = std::make_shared<const std::vector<uint32_t>>(std::move(pixels));
            break;
        }
        case MissionLayerOperation::Save:
            saved[slot] = target; break;
        case MissionLayerOperation::Restore:
            target = saved[slot]; break;
        }
    }
    for (size_t i = 0; i < result.surfaces.size(); ++i) {
        auto& draw = result.surfaces[i].indexed;
        draw.indices = std::make_shared<const std::vector<uint8_t>>(std::move(indices[i]));
        result.saved.push_back({std::make_shared<const std::vector<uint8_t>>(std::move(saved[i])),
                               draw.width, draw.height, draw.width});
    }
    return result;
}
inline PresentationTarget RasterizeMissionLayers(const MissionLayerSequence& scene,
                                                 const PresentationDestinationId& destination) {
    const auto composed = ComposeMissionLayers(scene);
    for (const auto& surface : composed.surfaces)
        if (surface.destination == destination) return RasterizePresentationSurface(surface);
    throw std::invalid_argument("unknown mission presentation destination");
}
} // namespace openfodder
