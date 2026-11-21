// GPL-3.0-or-later. Optional, single-pose indexed replacement; classic fallback.
#pragma once
#include "ResolvedSpriteResource.hpp"

namespace openfodder {
// Immutable after capture. Ownership of the original resource also prevents an
// address from being reused to accidentally match a different resource version.
struct SoldierPose {
    PreparedSpriteDraw origin;
    size_t width = 0, height = 0;
    std::vector<uint8_t> indices; // zero is transparent, palette remains indexed
};
inline bool SoldierPoseGeometry(const PreparedSpriteDraw& prepared, size_t& width, size_t& height) {
    const auto& s = prepared.soldier;
    const auto& g = s.geometry;
    const auto& d = prepared.draw;
    const auto& r = prepared.resource;
    if (!s.valid || !s.scene || !s.generation || !s.interval || g.source || !r ||
        !d.visible || d.format != g.format || r.layout.format != g.format ||
        (g.format != SpriteDrawFormat::PC && g.format != SpriteDrawFormat::Amiga8) ||
        d.sourceOffset != 0 || d.columns != g.columns ||
        d.rows != int(g.rows) - g.rowsToSkip || d.rows <= 0 ||
        d.x != int(g.modX) + g.spriteX - g.mapX + g.xBias ||
        d.y != int(g.modY) + g.spriteY - d.rows - g.height - g.mapY + 16 ||
        d.palette != g.palette) return false;
    // This first pilot deliberately falls back for any clipped geometry.
    int bytesPerRow = g.format == SpriteDrawFormat::PC ? d.columns / 2 : (d.columns - 1) * 2;
    const size_t stride = g.format == SpriteDrawFormat::PC ? 160 : r.layout.width / 8;
    if (bytesPerRow <= 0 || size_t(bytesPerRow) > stride) return false;
    if (g.format == SpriteDrawFormat::Amiga8 &&
        (r.layout.width != 320 || !r.layout.height || !r.layout.planes || r.layout.planes > 8)) return false;
    const size_t planes = g.format == SpriteDrawFormat::PC ? 1 : r.layout.planes;
    const size_t last = (size_t(d.rows) - 1) * stride + size_t(bytesPerRow) +
        (planes - 1) * size_t(r.layout.height) * 40;
    if (last > r.available()) return false;
    width = size_t(bytesPerRow) * (g.format == SpriteDrawFormat::PC ? 2 : 8);
    height = size_t(d.rows);
    return width <= 352 && height <= 232; // bounded classic viewport pilot
}
inline std::shared_ptr<const SoldierPose> CaptureOriginalSoldierPose(const PreparedSpriteDraw& prepared) {
    size_t width = 0, height = 0;
    if (!SoldierPoseGeometry(prepared, width, height)) return {};
    auto pose = std::make_shared<SoldierPose>();
    pose->origin = prepared;
    pose->origin.draw.source = nullptr;
    pose->width = width; pose->height = height;
    pose->indices.assign(width * height, 0);
    auto draw = prepared.draw;
    draw.x = draw.y = 0;
    draw.source = prepared.resource.source();
    RasterizeSprite8(draw, prepared.resource.layout, {pose->indices.data(), width});
    return pose;
}
inline bool SoldierPoseMatches(const SoldierPose& pose, const PreparedSpriteDraw& prepared) {
    const auto& a = pose.origin.soldier; const auto& b = prepared.soldier;
    const auto& ga = a.geometry; const auto& gb = b.geometry;
    const auto& ra = pose.origin.resource; const auto& rb = prepared.resource;
    size_t width = 0, height = 0;
    return SoldierPoseGeometry(prepared, width, height) &&
        a.scene == b.scene && a.slot == b.slot && a.generation == b.generation &&
        a.type == b.type && a.sheet == b.sheet && a.frame == b.frame &&
        a.animation == b.animation && a.direction == b.direction && a.segment == b.segment &&
        ga.columns == gb.columns && ga.rows == gb.rows && ga.rowsToSkip == gb.rowsToSkip &&
        ga.modX == gb.modX && ga.modY == gb.modY && ga.xBias == gb.xBias &&
        ga.palette == gb.palette && ga.format == gb.format &&
        ra.bytes == rb.bytes && ra.offset == rb.offset && ra.generation == rb.generation &&
        ra.layout.width == rb.layout.width && ra.layout.height == rb.layout.height &&
        ra.layout.planes == rb.layout.planes && ra.layout.format == rb.layout.format &&
        width == pose.width && height == pose.height && pose.indices.size() == width * height;
}
// Validate everything before the first write. A miss never leaves a partial pose.
// Anchor and camera come from the current command, never from the cached pose.
inline bool TryRasterizeSoldierPose(const std::shared_ptr<const SoldierPose>& pose,
        const PreparedSpriteDraw& prepared, uint8_t* target, size_t width, size_t height) {
    if (!pose || !target || !SoldierPoseMatches(*pose, prepared)) return false;
    const auto& d = prepared.draw;
    if (d.x < 0 || d.y < 0 || size_t(d.x) > width || size_t(d.y) > height ||
        pose->width > width - size_t(d.x) || pose->height > height - size_t(d.y)) return false;
    for (size_t y = 0; y < pose->height; ++y)
        for (size_t x = 0; x < pose->width; ++x) {
            const auto value = pose->indices[y * pose->width + x];
            if (value) target[(size_t(d.y) + y) * width + size_t(d.x) + x] = value;
        }
    return true;
}
} // namespace openfodder
