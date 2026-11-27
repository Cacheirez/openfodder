// GPL-3.0-or-later. Owned indexed terrain commands; no engine/surface pointers.
#pragma once
#include <cstdint>
#include <cstddef>
#include <cstring>
#include <memory>
#include <vector>

namespace openfodder {
enum class TerrainFormat { PC, Amiga };
using TerrainBytes = std::shared_ptr<const std::vector<uint8_t>>;

// Producer-only, under the existing serialization. Private copies have no
// mutable aliases. Recheck once per capture to detect in-place legacy edits.
class TerrainAtlasCache {
    TerrainBytes versions[2];
public:
    TerrainBytes capture(size_t slot, const std::vector<uint8_t>& source) {
        auto& version = versions[slot];
        if (!version || *version != source)
            version = std::make_shared<const std::vector<uint8_t>>(source);
        return version;
    }
};
struct TerrainTile {
    uint16_t id;
    size_t x, y;
    uint16_t startX, startY;
};
struct TerrainDraw {
    TerrainFormat format = TerrainFormat::PC;
    TerrainBytes base, sub;
    std::vector<TerrainTile> tiles;
};

// Copy the legacy visible rectangle, including its extra border tiles. Offsets
// are signed indices rather than pointers formed before the map allocation.
inline TerrainDraw PrepareTerrain(const std::vector<uint8_t>& map, int64_t mapOffset,
        size_t mapWidth, int rows, int columns, uint16_t rowOffset,
        uint16_t columnOffset, TerrainFormat format, TerrainBytes base, TerrainBytes sub = {}) {
    TerrainDraw result;
    result.format = format;
    result.base = std::move(base);
    result.sub = std::move(sub);
    size_t y = 0;
    for (int row = 0; row <= rows + 1; ++row) {
        const uint16_t sy = row == 0 ? rowOffset : 0;
        int64_t index = mapOffset + static_cast<int64_t>(row) * static_cast<int64_t>(mapWidth) * 2;
        size_t x = 0;
        // Both original backends leave a row before the map untouched.
        for (int col = 0; index >= 0 && col <= columns + 1; ++col) {
            if (static_cast<size_t>(index) >= map.size() || map.size() - index < 2) break;
            uint16_t id = (map[index] | (uint16_t(map[index + 1]) << 8)) & 0x1FF;
            if (id > (format == TerrainFormat::PC ? 0x1DF : 0x1C0)) id = 0;
            const uint16_t sx = col == 0 ? columnOffset : 0;
            result.tiles.push_back({id, x, y, sx, sy});
            index += 2;
            x += 16 - sx;
        }
        y += 16 - sy;
    }
    return result;
}

// Only target pixels are written. Target must hold the legacy rectangle and
// offsets must be in [0,15]. RGB palettes and Save/SDL effects remain separate.
inline void RasterizeTerrain(const TerrainDraw& draw, uint8_t* target, size_t width, size_t size) {
    if (draw.format == TerrainFormat::Amiga) std::memset(target, 0, size);
    for (const auto& tile : draw.tiles) {
        if (draw.format == TerrainFormat::PC) {
            const auto& atlas = tile.id < 240 ? draw.base : draw.sub;
            const size_t id = tile.id % 240;
            const size_t offset = (id / 20) * 5120 + (id % 20) * 16;
            for (size_t row = tile.startY; row < 16; ++row) {
                const size_t source = offset + row * 320 + tile.startX;
                const size_t count = 16 - tile.startX;
                if (atlas && source <= atlas->size() && count <= atlas->size() - source)
                    std::memcpy(target + (tile.y + row - tile.startY) * width + tile.x,
                                atlas->data() + source, count);
            }
        } else {
            // Preserve the classic cropped-plane stepping and destination X:
            // after a partial first row, planes advance by the consumed rows.
            size_t source = (size_t(tile.id) << 7) + tile.startY * 2;
            for (uint16_t plane = 0; plane < 4; ++plane) {
                for (size_t row = tile.startY; row < 16; ++row) {
                    if (!draw.base || source >= draw.base->size() || draw.base->size() - source < 2) continue;
                    uint16_t bits = (uint16_t((*draw.base)[source]) << 8) | (*draw.base)[source + 1];
                    source += 2;
                    bits <<= tile.startX;
                    for (size_t x = tile.startX; x < 16; ++x) {
                        if (bits & 0x8000)
                            target[(tile.y + row - tile.startY) * width + tile.x + x] |= uint8_t(1 << plane);
                        bits <<= 1;
                    }
                }
            }
        }
    }
}
} // namespace openfodder
