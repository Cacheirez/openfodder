// GPL-3.0-or-later. Retain immutable sprite bytes with their effective layout/palette.
#pragma once
#include "SpriteRaster.hpp"
#include "SoldierSemantic.hpp"
#include <algorithm>
#include <map>
#include <memory>
#include <vector>

namespace openfodder {
struct ResolvedSpriteResource {
    std::shared_ptr<const std::vector<uint8_t>> bytes;
    size_t offset = 0;
    SpriteRasterLayout layout;
    uint8_t palette = 0;
    uint64_t generation = 0; // Local to the producing cache; ownership is in bytes.

    explicit operator bool() const { return bytes && offset < bytes->size(); }
    const uint8_t* source() const { return *this ? bytes->data() + offset : nullptr; }
    size_t available() const { return *this ? bytes->size() - offset : 0; }
};

// Producer-only cache. Capture under the existing legacy serialization, never
// concurrently with writes to the source vector. Consumers only retain results.
// Compare contents because legacy code may mutate an existing shared vector.
class FrozenSpriteResources {
    struct Entry {
        std::shared_ptr<const std::vector<uint8_t>> bytes;
        uint64_t generation = 0;
        uint64_t checkedBatch = 0;
    };
    std::map<uint16_t, Entry> entries;
    uint64_t nextGeneration = 0;
    uint64_t nextBatch = 0;
    uint64_t activeBatch = 0;
public:
    // The caller guarantees that source vectors are not written or replaced in
    // this scope. Only use around the serialized, read-only sprite draw loop.
    // A new scope rechecks bytes, including in-place edits between draw passes.
    class ReadOnlyBatch {
        FrozenSpriteResources& cache;
        uint64_t previous;
    public:
        explicit ReadOnlyBatch(FrozenSpriteResources& owner)
            : cache(owner), previous(owner.activeBatch) {
            cache.activeBatch = ++cache.nextBatch;
        }
        ~ReadOnlyBatch() { cache.activeBatch = previous; }
        ReadOnlyBatch(const ReadOnlyBatch&) = delete;
        ReadOnlyBatch& operator=(const ReadOnlyBatch&) = delete;
    };

    ResolvedSpriteResource capture(uint16_t segment, const std::vector<uint8_t>& source,
            size_t offset, SpriteRasterLayout layout, uint8_t palette) {
        if (offset >= source.size()) return {};
        auto& entry = entries[segment];
        const bool checked = activeBatch && entry.checkedBatch == activeBatch;
        if (!checked && (!entry.bytes || *entry.bytes != source)) {
            // Construct a const object from a private copy: no mutable alias.
            entry.bytes = std::make_shared<const std::vector<uint8_t>>(source);
            entry.generation = ++nextGeneration;
        }
        entry.checkedBatch = activeBatch;
        ResolvedSpriteResource result;
        result.bytes = entry.bytes;
        result.offset = offset;
        result.layout = layout;
        result.palette = palette;
        result.generation = entry.generation;
        return result;
    }
};

// Copying/moving this object retains the bytes referenced by draw.source.
// This covers a sprite command, not a complete frame or publication protocol.
struct PreparedSpriteDraw {
    ResolvedSpriteResource resource;
    SpriteDrawState draw;
    SoldierSemantic soldier;
    bool isCursor = false; // Presentation provenance only; never a sorting key.
};
} // namespace openfodder
