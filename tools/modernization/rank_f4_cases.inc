// GPL-3.0-or-later. Exact Amiga F4, roof F0 and grenade box F0 with five native bodies.
nlohmann::json fixture;
{
    std::ifstream file(std::getenv("OPENFODDER_A1_RANK_F4"));
    file >> fixture;
}
const auto& rows = fixture.at("bodies");
const auto& rankRow = fixture.at("rank");
const std::string rankKey = "84a0ee13d651ee9f27afe2d9284cacb3b3b53c18658c934effc0ba0942a0be5f";
const std::string roofKey = "5fc9fc6b277ef4b4f27f2552b6a212827b18f31e8e3dc4c6979cb98c4e64d9f7";
const std::string boxKey = "c967c720f08747d3eae8abb253c3ed16d3684ca547ca65df3627d275f9c3e6e5";
const bool withRoof = fixture.contains("roof");
const bool withBox = fixture.contains("grenade_box");
assert(!withBox || withRoof);
const auto colors = rankRow.at("colors").get<std::array<uint32_t, 255>>();
image.scene.destinations[0].initial.indexed.colors = colors;
if (withRoof)
    image.scene.destinations[0].initial.indexed.skipY = 0; // Observe writes at the top edge.
assert(rows.size() == 5 && rankRow.at("key") == rankKey);

auto nativeLayer = [&](const nlohmann::json& row, const std::string& directory,
                       int slot, int x, int y) {
    auto layer = body;
    auto& prepared = layer.soldier;
    assert(row.at("colors") == rankRow.at("colors"));
    prepared = LoadNativeWalkSnapshot(row, directory);
    auto& sprite = prepared.soldier;
    sprite.scene = fodder.mPresentationScene;
    sprite.interval = 1;
    sprite.slot = slot;
    sprite.generation = 1;
    sprite.geometry.spriteX = x;
    sprite.geometry.spriteY = y;
    sprite.geometry.xBias = 0;
    sprite.geometry.viewWidth = 96;
    sprite.geometry.viewHeight = 64;
    auto geometry = sprite.geometry;
    geometry.source = prepared.resource.source();
    prepared.draw = PrepareSpriteDraw(geometry);
    return layer;
};

const auto rank = nativeLayer(rankRow, fixture.at("rank_snapshots"), 5, 32, 20);
auto retained = rank;
if (withRoof)
    retained = nativeLayer(fixture.at("roof"), fixture.at("rank_snapshots"), 6, 32, -9);
image.scene.layers.clear();
if (withRoof)
    image.scene.layers.push_back(rank);
if (withBox) {
    image.scene.layers.push_back(retained);
    retained = nativeLayer(fixture.at("grenade_box"), fixture.at("rank_snapshots"), 7, 32, 20);
}
const std::array<int, 5> positions{8, 32, 61, 76, 39};
for (size_t i = 0; i < rows.size(); ++i)
    image.scene.layers.push_back(nativeLayer(rows[i], fixture.at("body_snapshots"),
                                            int(i), positions[i], withRoof && !withBox ? 0 : 20));
auto prefix = image.scene;
prefix.layers.pop_back();
auto throughRetained = prefix;
throughRetained.layers.push_back(retained);
const size_t retainedIndex = prefix.layers.size();
image.scene.layers.insert(image.scene.layers.begin() + retainedIndex, retained);

const std::string manifestPath = fixture.at("manifest");
const auto registry = OrderedSoldierRegistry::Load(manifestPath);
env("OPENFODDER_SOLDIER_ORDERED_MANIFEST", manifestPath.c_str());
auto draw = retained.soldier.draw;
draw.source = retained.soldier.resource.source();
const auto writes = CaptureSprite8Producer(draw, retained.soldier.resource.layout, 96).writes;
if (withRoof) {
    const auto& exactKey = withBox ? boxKey : roofKey;
    assert(SoldierVariantKey(retained.soldier, colors) == exactKey);
    assert(registry.resolve(retained.soldier, exactKey, 8).decision == SoldierArtDecision::KeepClassic);
    auto invalid = retained.soldier;
    invalid.soldier.inVehicle = true;
    assert(registry.resolve(invalid, exactKey, 8).decision == SoldierArtDecision::Missing);
    invalid = retained.soldier;
    invalid.soldier.pendingDestroy = true;
    assert(registry.resolve(invalid, exactKey, 8).decision == SoldierArtDecision::Missing);
    invalid = retained.soldier;
    invalid.resource = {};
    assert(registry.resolve(invalid, exactKey, 8).decision == SoldierArtDecision::Missing);
}
if (withBox) {
    assert(writes.size() == 102);
} else if (withRoof) {
    auto unclipped = retained.soldier.soldier.geometry;
    unclipped.spriteY = -4;
    unclipped.source = draw.source;
    const auto fullWrites = CaptureSprite8Producer(PrepareSpriteDraw(unclipped),
                                                   retained.soldier.resource.layout, 96).writes;
    assert(fullWrites.size() == 189 && draw.y == 0 && draw.rows == 7);
    size_t clippedWrites = 0;
    for (const auto& write : fullWrites) {
        if (write.offset < 5 * 96)
            continue;
        const auto& actual = writes.at(clippedWrites++);
        assert(actual.offset == write.offset - 5 * 96 && actual.value == write.value);
    }
    assert(clippedWrites == writes.size() && clippedWrites && clippedWrites < fullWrites.size());
} else {
    assert(writes.size() == 57);
}

const auto scene = image.scene;
auto renderClassic = [&](const MissionLayerSequence& current) {
    const auto raster = RasterizeMissionLayers(current, body.destination);
    assert(SDL_UpdateTexture(image.tex, nullptr, raster.pixels.data(), 96 * 4));
    clear(renderer);
    assert(SDL_RenderTexture(renderer, image.tex, &src, &dst));
    return read(renderer);
};
for (unsigned density : {8u, 12u}) {
    env("OPENFODDER_SOLDIER_HD", std::to_string(density).c_str());
    auto compose = [&](const MissionLayerSequence& current) {
        return ComposeOrderedSoldierArt(current, body.destination, density, [&](const PreparedSpriteDraw& sprite) {
            return registry.resolve(sprite, SoldierVariantKey(sprite, colors), density);
        });
    };
    const auto beforeRetained = compose(prefix);
    const auto afterRetained = compose(throughRetained);
    const auto frame = compose(scene);
    const size_t kept = 1 + withRoof + withBox;
    assert(beforeRetained.complete() && beforeRetained.replaced == 4 && beforeRetained.kept == kept - 1);
    assert(afterRetained.complete() && afterRetained.replaced == 4 && afterRetained.kept == kept);
    assert(frame.complete() && frame.replaced == 5 && frame.kept == kept);
    const auto classicRetained = RasterizeMissionLayers(throughRetained, body.destination);
    size_t coversHD = 0, coveredByHD = 0, visible = 0;
    for (const auto& write : writes) {
        const size_t offset = write.offset;
        coversHD += beforeRetained.cells.count(offset);
        coveredByHD += frame.cells.count(offset);
        visible += !frame.cells.count(offset);
        assert(!afterRetained.cells.count(offset));
        assert(afterRetained.background.pixels.at(offset) == classicRetained.pixels.at(offset));
    }
    assert(coversHD && coveredByHD && visible);

    const size_t width = 96 * density, height = 64 * density;
    auto renderExpected = [&](const OrderedSoldierFrame& expectedFrame) {
        std::vector<uint32_t> expectedPixels(width * height);
        for (size_t y = 0; y < height; ++y) {
            for (size_t x = 0; x < width; ++x) {
                const size_t offset = (y / density) * 96 + x / density;
                const auto cell = expectedFrame.cells.find(offset);
                expectedPixels[y * width + x] = cell == expectedFrame.cells.end()
                    ? expectedFrame.background.pixels[offset] : cell->second[(y % density) * density + x % density];
            }
        }
        auto oracle = texture(renderer, expectedPixels, int(width), int(height));
        const SDL_FRect full{0, 0, float(width), float(height)};
        clear(renderer);
        assert(SDL_RenderTexture(renderer, oracle, &full, &dst));
        const auto pixels = read(renderer);
        SDL_DestroyTexture(oracle);
        return pixels;
    };
    const auto expected = renderExpected(frame);
    const auto classic = renderClassic(scene);
    assert(expected != classic);
    clear(renderer);
    assert(win.TryRenderMissionHD(&image, src, dst) == 1 && read(renderer) == expected);

    // Change one key at a time while keeping drawable native pixels.
    auto checkFallback = [&](const MissionLayerSequence& orderedScene,
                             size_t slot, const std::vector<uint32_t>& hdPixels) {
        image.scene = orderedScene;
        auto& missing = image.scene.layers[slot].soldier;
        missing.soldier.frame = 99;
        assert(registry.resolve(missing, SoldierVariantKey(missing, colors), density).decision
               == SoldierArtDecision::Missing);
        assert(compose(image.scene).missing == 1);
        const auto expectedClassic = renderClassic(image.scene);
        clear(renderer);
        const auto before = read(renderer);
        const int hd = win.TryRenderMissionHD(&image, src, dst);
        assert(hd == -1 && read(renderer) == before && live == 0);
        // Same fallback draw as cWindow::Draw.
        assert(SDL_RenderTexture(renderer, image.tex, &src, &dst));
        assert(read(renderer) == expectedClassic);
        image.scene = orderedScene;
        clear(renderer);
        assert(win.TryRenderMissionHD(&image, src, dst) == 1 && read(renderer) == hdPixels);
    };
    for (size_t slot : {retainedIndex, retainedIndex + 1})
        checkFallback(scene, slot, expected);
    if (fixture.contains("ground_hole")) {
        const std::string key = "b27064e821fb760e4ec5e37a830ac2e35b81b46490abf208da81cc928cf63cf4";
        const auto hole = nativeLayer(fixture.at("ground_hole"), fixture.at("ground_hole_snapshots"),
                                      10, 38, 20);
        assert(SoldierVariantKey(hole.soldier, colors) == key);
        assert(registry.resolve(hole.soldier, key, density).decision == SoldierArtDecision::KeepClassic);
        auto draw = hole.soldier.draw;
        draw.source = hole.soldier.resource.source();
        assert(draw.visible && draw.columns == 2 && draw.rows == 1);
        assert(CaptureSprite8Producer(draw, hole.soldier.resource.layout, 96).writes.empty());

        auto ordered = scene;
        const size_t holeIndex = ordered.layers.size() - 1;
        assert(frame.cells.count(size_t(draw.y) * 96 + size_t(draw.x)));
        ordered.layers.insert(ordered.layers.begin() + holeIndex, hole);
        const auto withHole = compose(ordered);
        assert(withHole.complete() && withHole.replaced == frame.replaced && withHole.kept == kept + 1);
        assert(withHole.observations.at(holeIndex).decision == SoldierArtDecision::KeepClassic);
        assert(withHole.observations.at(holeIndex + 1).decision == SoldierArtDecision::Replace);
        assert(withHole.cells == frame.cells && withHole.background.pixels == frame.background.pixels);
        assert(renderClassic(ordered) == classic);
        image.scene = ordered;
        clear(renderer);
        assert(win.TryRenderMissionHD(&image, src, dst) == 1 && read(renderer) == expected);
        checkFallback(ordered, holeIndex, expected);
        image.scene = scene;
        std::cout << density << "x GroundHole 0x7C/F0: zero writes, identical SDL pixels, "
                  << "whole-frame classic fallback and HD recovery\n";
    }
    if (fixture.contains("tree_90")) {
        const std::string key = "a835b7ae71451ea0a37ea0a0c1e77da13a45f003b0cf218314edc6e0c79a1a2d";
        const auto tree = nativeLayer(fixture.at("tree_90"), fixture.at("tree_90_snapshots"),
                                      11, 38, 20);
        assert(SoldierVariantKey(tree.soldier, colors) == key);
        assert(registry.resolve(tree.soldier, key, density).decision == SoldierArtDecision::KeepClassic);
        auto otherTree = tree.soldier;
        ++otherTree.soldier.animation;
        const auto otherKey = SoldierVariantKey(otherTree, colors);
        assert(otherKey != key);
        const OrderedSoldierRegistry unapproved(nlohmann::json{
            {"version", 1}, {"bindings", {{{"key", otherKey}, {"decision", "keep-associated"}}}}
        });
        assert(unapproved.resolve(otherTree, otherKey, density).decision == SoldierArtDecision::Missing);

        auto draw = tree.soldier.draw;
        draw.source = tree.soldier.resource.source();
        const auto treeWrites = CaptureSprite8Producer(draw, tree.soldier.resource.layout, 96).writes;
        assert(treeWrites.size() == 299);
        auto throughTree = throughRetained;
        throughTree.layers.push_back(tree);
        auto ordered = throughTree;
        ordered.layers.push_back(scene.layers.back());
        const auto afterTree = compose(throughTree);
        const auto withTree = compose(ordered);
        const auto nativeTree = RasterizeMissionLayers(throughTree, body.destination);
        assert(afterTree.complete() && afterTree.replaced == 4 && afterTree.kept == kept + 1);
        assert(withTree.complete() && withTree.replaced == 5 && withTree.kept == kept + 1);
        assert(withTree.observations.at(throughTree.layers.size() - 1).decision == SoldierArtDecision::KeepClassic);
        assert(withTree.observations.back().decision == SoldierArtDecision::Replace);
        size_t coversBody = 0, coveredByBody = 0, treeVisible = 0;
        for (const auto& write : treeWrites) {
            const auto offset = write.offset;
            coversBody += afterRetained.cells.count(offset);
            coveredByBody += withTree.cells.count(offset);
            treeVisible += !withTree.cells.count(offset);
            assert(!afterTree.cells.count(offset));
            assert(afterTree.background.pixels.at(offset) == nativeTree.pixels.at(offset));
        }
        assert(coversBody && coveredByBody && treeVisible);

        const auto expectedTree = renderExpected(withTree);
        assert(expectedTree != expected && expectedTree != renderClassic(ordered));
        image.scene = ordered;
        clear(renderer);
        assert(win.TryRenderMissionHD(&image, src, dst) == 1 && read(renderer) == expectedTree);
        checkFallback(ordered, throughTree.layers.size() - 1, expectedTree);
        image.scene = scene;
        std::cout << density << "x tree 0x90/F0: " << treeWrites.size() << " native writes, "
                  << coversBody << " occlude HD and " << coveredByBody << " are occluded by HD, "
                  << "whole-frame classic fallback and HD recovery\n";
    }
    if (fixture.contains("player_shadow")) {
        assert(withBox);
        const auto& row = fixture.at("player_shadow");
        const std::string shadowKey = "c7fcc929ce1739035307df6e6b084f2a5d05dea74dba4ec2c8487cf3cdef04e1";
        const auto shadow = nativeLayer(row, fixture.at("rank_snapshots"), 9, 38, 16);
        assert(SoldierVariantKey(shadow.soldier, colors) == shadowKey);
        assert(registry.resolve(shadow.soldier, shadowKey, density).decision == SoldierArtDecision::KeepClassic);
        auto shadowDraw = shadow.soldier.draw;
        shadowDraw.source = shadow.soldier.resource.source();
        const auto shadowWrites = CaptureSprite8Producer(shadowDraw, shadow.soldier.resource.layout, 96).writes;
        assert(shadowWrites.size() == 24);

        auto ordered = throughRetained;
        ordered.layers.push_back(shadow);
        const auto afterShadow = compose(ordered);
        assert(afterShadow.complete() && afterShadow.replaced == 4 && afterShadow.kept == kept + 1);
        const auto classicShadow = RasterizeMissionLayers(ordered, body.destination);
        ordered.layers.push_back(scene.layers.back());
        const auto orderedFrame = compose(ordered);
        assert(orderedFrame.complete() && orderedFrame.replaced == 5 && orderedFrame.kept == kept + 1);
        size_t overEarlier = 0, underLater = 0;
        for (const auto& write : shadowWrites) {
            const size_t offset = write.offset;
            overEarlier += afterRetained.cells.count(offset);
            underLater += orderedFrame.cells.count(offset);
            assert(!afterShadow.cells.count(offset));
            assert(afterShadow.background.pixels.at(offset) == classicShadow.pixels.at(offset));
        }
        assert(overEarlier && underLater && underLater < shadowWrites.size());
        image.scene = ordered;
        const auto orderedPixels = renderExpected(orderedFrame);
        clear(renderer);
        assert(win.TryRenderMissionHD(&image, src, dst) == 1 && read(renderer) == orderedPixels);
        checkFallback(ordered, retainedIndex + 1, orderedPixels);

        const auto clipped = nativeLayer(row, fixture.at("rank_snapshots"), 9, 38, -14);
        auto clippedDraw = clipped.soldier.draw;
        clippedDraw.source = clipped.soldier.resource.source();
        assert(clippedDraw.y == 0 && clippedDraw.rows == 2);
        assert(SoldierVariantKey(clipped.soldier, colors) == shadowKey);
        const auto clippedWrites = CaptureSprite8Producer(clippedDraw, clipped.soldier.resource.layout, 96).writes;
        size_t clippedCount = 0;
        for (const auto& write : shadowWrites) {
            const auto y = write.offset / 96 - shadowDraw.y;
            if (y < 2)
                continue;
            const auto& actual = clippedWrites.at(clippedCount++);
            assert(actual.offset == (y - 2) * 96 + write.offset % 96 && actual.value == write.value);
        }
        assert(clippedCount == clippedWrites.size() && clippedCount && clippedCount < shadowWrites.size());
        image.scene = scene;
        image.scene.layers.push_back(clipped);
        const auto clippedFrame = compose(image.scene);
        assert(clippedFrame.complete() && clippedFrame.replaced == 5 && clippedFrame.kept == kept + 1);
        const auto clippedClassic = RasterizeMissionLayers(image.scene, body.destination);
        for (const auto& write : clippedWrites)
            assert(clippedFrame.background.pixels.at(write.offset) == clippedClassic.pixels.at(write.offset));
        const auto clippedPixels = renderExpected(clippedFrame);
        clear(renderer);
        assert(win.TryRenderMissionHD(&image, src, dst) == 1 && read(renderer) == clippedPixels);
        image.scene = scene;
        std::cout << "PASS A.1 player shadow 0x97/F1 SDL " << density
                  << "x: 24 writes, overlaps " << overEarlier << '/' << underLater
                  << ", visible " << shadowWrites.size() - underLater << ", clipped " << clippedCount
                  << " writes, whole-frame classic fallback and recovery\n";
    }
    if (withBox) {
        // The interval after pickup has no draw command for this slot.
        image.scene.layers.erase(image.scene.layers.begin() + retainedIndex);
        const auto collected = compose(image.scene);
        assert(collected.complete() && collected.replaced == 5 && collected.kept == 2);
        const auto afterPickup = renderExpected(collected);
        assert(afterPickup != expected);
        renderClassic(image.scene);
        clear(renderer);
        assert(win.TryRenderMissionHD(&image, src, dst) == 1 && read(renderer) == afterPickup);
        image.scene = scene;
    }
    struct EnemyCase {
        const char* field;
        const char* label;
        const char* key;
    };
    const EnemyCase enemies[] = {
        {"enemy_prone", "0x59/F0", "0ae80fd93ee8120c3e003e5b0e9383b2514910c7353812e498a587247d5455d8"},
        {"enemy_walk", "0x45/F1", "77d34d3f0593010865c1185e626929f4491ff2303b6656397cd640fb0334356a"},
        {"enemy_death", "0x71/F1", "f06b98d0debe93b676cd17ba89a9b76e2b91484a08507c83e8d66215dc8237fb"},
        {"enemy_hit", "0x71/F1 Hit", "d615161944fbf97e9e07f29f4de6849c927c0d4e20087cbb981ec3c73e11dc45"},
        {"enemy_walk_44", "0x44/F1", "af38382eee31380c6ba6d0469c9237f48400fa21bdeb3e8f09efbdd149988d77"},
    };
    for (const auto& enemyCase : enemies) {
        if (!fixture.contains(enemyCase.field))
            continue;
        assert(withBox);
        const auto& row = fixture.at(enemyCase.field);
        const std::string enemyKey = enemyCase.key;
        auto enemy = nativeLayer(row, fixture.at("enemy_snapshots"), 8, 39, 20);
        assert(SoldierVariantKey(enemy.soldier, colors) == enemyKey);
        const auto art = registry.resolve(enemy.soldier, enemyKey, density);
        assert(art.decision == SoldierArtDecision::Replace && art.width == 16 && art.height == 14);

        auto withoutLast = scene;
        const auto lastBody = withoutLast.layers.back();
        withoutLast.layers.pop_back();
        // Place an earlier body under the enemy as well as the later body over it.
        withoutLast.layers[3] = nativeLayer(rows[1], fixture.at("body_snapshots"), 1, 37, 20);
        auto withEnemy = withoutLast;
        withEnemy.layers.push_back(enemy);
        const auto earlier = compose(withoutLast);
        const auto enemyFrame = compose(withEnemy);
        withEnemy.layers.push_back(lastBody);
        const auto ordered = compose(withEnemy);
        withoutLast.layers.push_back(lastBody);
        const auto withoutEnemy = compose(withoutLast);
        assert(ordered.complete() && ordered.replaced == 6 && ordered.kept == 3);
        size_t overEarlier = 0, underLater = 0, visibleEnemy = 0;
        for (const auto& entry : enemyFrame.cells) {
            const auto offset = entry.first;
            const auto& cell = entry.second;
            const auto previous = earlier.cells.find(offset);
            if (previous == earlier.cells.end() || previous->second == cell)
                continue;
            const auto background = earlier.background.pixels.at(offset);
            overEarlier += std::any_of(previous->second.begin(), previous->second.end(),
                                       [background](auto pixel) { return pixel != background; });
            underLater += ordered.cells.at(offset) != cell;
        }
        for (const auto& entry : ordered.cells) {
            const auto offset = entry.first;
            const auto& cell = entry.second;
            const auto previous = withoutEnemy.cells.find(offset);
            visibleEnemy += previous == withoutEnemy.cells.end() || previous->second != cell;
        }
        assert(overEarlier && underLater && visibleEnemy);
        image.scene = withEnemy;
        const auto orderedPixels = renderExpected(ordered);
        clear(renderer);
        assert(win.TryRenderMissionHD(&image, src, dst) == 1 && read(renderer) == orderedPixels);

        auto& unresolved = image.scene.layers[image.scene.layers.size() - 2].soldier;
        unresolved.soldier.frame = 99;
        assert(compose(image.scene).missing == 1);
        const auto fallback = renderClassic(image.scene);
        clear(renderer);
        const auto untouched = read(renderer);
        assert(win.TryRenderMissionHD(&image, src, dst) == -1 && read(renderer) == untouched && live == 0);
        assert(SDL_RenderTexture(renderer, image.tex, &src, &dst) && read(renderer) == fallback);
        image.scene = withEnemy;
        clear(renderer);
        assert(win.TryRenderMissionHD(&image, src, dst) == 1 && read(renderer) == orderedPixels);

        auto clipped = nativeLayer(row, fixture.at("enemy_snapshots"), 8, 39, -7);
        const auto& clippedDraw = clipped.soldier.draw;
        assert(clippedDraw.y == 0 && clippedDraw.rows == 9 && clippedDraw.sourceOffset == 200);
        assert(SoldierVariantKey(clipped.soldier, colors) == enemyKey);
        image.scene = scene;
        image.scene.layers.push_back(clipped);
        const auto clippedFrame = compose(image.scene);
        assert(clippedFrame.complete() && clippedFrame.replaced == 6);
        size_t painted = 0;
        for (size_t y = 0; y < 9; ++y) {
            for (size_t x = 0; x < 16; ++x) {
                const size_t offset = y * 96 + clippedDraw.x + x;
                const auto previous = frame.cells.find(offset);
                const auto& cell = clippedFrame.cells.at(offset);
                for (size_t sy = 0; sy < density; ++sy) {
                    for (size_t sx = 0; sx < density; ++sx) {
                        const auto source = ((y + 5) * density + sy) * 16 * density + x * density + sx;
                        const auto i = sy * density + sx;
                        const auto basePixel = previous == frame.cells.end()
                            ? frame.background.pixels.at(offset) : previous->second.at(i);
                        const auto pixel = SoldierBlend(art.pixels->at(source), basePixel);
                        assert(cell.at(i) == pixel);
                        painted += pixel != basePixel;
                    }
                }
            }
        }
        assert(painted);
        const auto clippedPixels = renderExpected(clippedFrame);
        clear(renderer);
        assert(win.TryRenderMissionHD(&image, src, dst) == 1 && read(renderer) == clippedPixels);
        image.scene = scene;
        std::cout << "PASS A.1 enemy " << enemyCase.label << " SDL " << density << "x: 6 bodies, overlaps "
                  << overEarlier << '/' << underLater << ", visible " << visibleEnemy
                  << ", 5 rows clipped, classic fallback and recovery\n";
    }
    const char* label = withBox ? "grenade box F0 + roof + F4" : withRoof ? "roof F0 + F4" : "F4";
    std::cout << "PASS A.1 " << label << " SDL " << density
              << "x: 5 native bodies, " << writes.size()
              << " retained writes, overlaps " << coversHD << '/' << coveredByHD
              << ", visible " << visible << ", 2 whole-frame classic returns and recovery"
              << (withBox ? ", HD after pickup" : "") << '\n';
}
