#include "Utils/MissionLayers.hpp"
#include <cassert>
#include <iostream>
using namespace openfodder;
int main() {
    size_t scenarios = 0;
    for (auto format : {SpriteDrawFormat::PC, SpriteDrawFormat::Amiga8}) {
        PreparedSpriteDraw p;
        p.resource.bytes = std::make_shared<const std::vector<uint8_t>>(16384, 0xA0);
        p.resource.layout = {format, 320, 32, 4};
        p.resource.generation = 1;
        auto& s = p.soldier;
        s.valid = true; s.scene = 1; s.generation = 2; s.interval = 3;
        s.slot = 4; s.sheet = 1; s.frame = 7; s.direction = 3;
        auto& g = s.geometry;
        g.format = format; g.columns = format == SpriteDrawFormat::PC ? 8 : 2;
        g.rows = 6; g.spriteX = 20; g.spriteY = 30; g.xBias = 0; g.palette = 32;
        g.modX = -2; g.modY = 3;
        auto prepare = [](PreparedSpriteDraw& v) {
            auto input = v.soldier.geometry; input.source = v.resource.source();
            v.draw = PrepareSpriteDraw(input); v.draw.source = nullptr;
        };
        prepare(p);
        auto pose = CaptureOriginalSoldierPose(p); assert(pose);
        const auto original = p;
        for (int shift : {0, 1, 7}) for (int camera : {0, 2}) {
            p = original;
            p.soldier.geometry.spriteX += shift;
            p.soldier.geometry.spriteY += shift;
            p.soldier.geometry.mapX += camera;
            p.soldier.geometry.mapY += camera;
            p.soldier.geometry.height += 2;
            p.soldier.interval += shift; // allowed only within the same live scene/actor
            prepare(p);
            std::vector<uint8_t> classic(80*64, 9), replacement = classic;
            auto draw = p.draw; draw.source = p.resource.source();
            RasterizeSprite8(draw, p.resource.layout, {classic.data(), 80});
            assert(TryRasterizeSoldierPose(pose, p, replacement.data(), 80, 64));
            assert(classic == replacement);
            // Transparent pixels preserve a nonzero background.
            assert(replacement[size_t(draw.y)*80+draw.x+1] == 9);
            // A real replacement must affect pixels, not merely record metadata.
            auto changed = std::make_shared<SoldierPose>(*pose);
            changed->indices[0] = 99;
            replacement.assign(80*64, 9);
            assert(TryRasterizeSoldierPose(changed, p, replacement.data(), 80, 64));
            assert(replacement != classic && replacement[size_t(draw.y)*80+draw.x] == 99);
            ++scenarios;
        }
        p = original;
        for (int miss = 0; miss < 17; ++miss) {
            auto changed = p; auto candidate = pose;
            switch (miss) {
            case 0: candidate.reset(); break;
            case 1: ++changed.soldier.frame; break;
            case 2: ++changed.soldier.scene; break;
            case 3: ++changed.soldier.generation; break;
            case 4: ++changed.soldier.slot; break;
            case 5: ++changed.soldier.direction; break;
            case 6: ++changed.soldier.sheet; break;
            case 7: ++changed.soldier.animation; break;
            case 8: ++changed.soldier.geometry.modX; prepare(changed); break;
            case 9: ++changed.soldier.geometry.palette; prepare(changed); break;
            case 10: changed.resource.bytes = std::make_shared<const std::vector<uint8_t>>(16384, 0x11); break;
            case 11: ++changed.resource.offset; break;
            case 12: changed.soldier.geometry.spriteY = -30; prepare(changed); break;
            case 13: changed.soldier.geometry.spriteX = 79; prepare(changed); break;
            case 14: changed.soldier.interval = 0; break;
            case 15: { auto invalid = std::make_shared<SoldierPose>(*pose); invalid->indices.pop_back(); candidate = invalid; break; }
            case 16: ++changed.resource.generation; break;
            }
            std::vector<uint8_t> pixels(80*64, 17), before = pixels;
            assert(!TryRasterizeSoldierPose(candidate, changed, pixels.data(), 80, 64));
            assert(pixels == before); // atomic miss; classic can draw afterwards
            ++scenarios;
        }
        auto truncated = p; truncated.resource.bytes = std::make_shared<const std::vector<uint8_t>>(1, 0);
        assert(!CaptureOriginalSoldierPose(truncated));
        // Real compositor chooses the fallback and preserves layer order.
        MissionLayerSequence scene;
        MissionLayerDestination dest;
        dest.initial.destination = std::make_shared<const PresentationDestination>();
        dest.initial.indexed.indices = std::make_shared<const std::vector<uint8_t>>(80*64, 9);
        dest.initial.indexed.width = 80; dest.initial.indexed.height = 64;
        dest.saved = {std::make_shared<const std::vector<uint8_t>>(80*64, 9),80,64,80};
        dest.initial.backing = {std::make_shared<const std::vector<uint32_t>>(80*64, 0),80,64,80};
        scene.destinations.push_back(dest);
        MissionLayer layer; layer.destination = dest.initial.destination;
        layer.operation = MissionLayerOperation::Soldier; layer.soldier = p; layer.pose = pose;
        scene.layers.push_back(layer);
        auto classic = ComposeMissionLayers(scene);
        auto replacement = ComposeMissionLayers(scene, true);
        assert(replacement.poseReplacements == 1 && replacement.poseFallbacks == 0);
        assert(*classic.surfaces[0].indexed.indices == *replacement.surfaces[0].indexed.indices);
        ++scene.layers[0].soldier.soldier.frame;
        auto fallback = ComposeMissionLayers(scene, true);
        assert(fallback.poseFallbacks == 1 && fallback.poseReplacements == 0);
        assert(*fallback.surfaces[0].indexed.indices == *classic.surfaces[0].indexed.indices);
        // A following layer still occludes the selected soldier.
        MissionLayer overlay; overlay.destination = dest.initial.destination;
        overlay.pixels.put(size_t(p.draw.y)*80+p.draw.x, 77);
        scene.layers.push_back(overlay);
        assert((*ComposeMissionLayers(scene, true).surfaces[0].indexed.indices)[size_t(p.draw.y)*80+p.draw.x] == 77);
        p.resource = {}; pose.reset(); // retained layer still owns both original and pose
        assert(ComposeMissionLayers(scene, true).poseFallbacks == 1);
    }
    std::cout << "PASS: " << scenarios << " PC/Amiga pose cases; anchors, camera, height, transparency, real pixel substitution, atomic misses, resource ownership and ordered classic fallback\n";
}
