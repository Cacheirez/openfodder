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
    for (size_t slot : {retainedIndex, retainedIndex + 1}) {
        auto& missing = image.scene.layers[slot].soldier;
        missing.soldier.frame = 99;
        assert(registry.resolve(missing, SoldierVariantKey(missing, colors), density).decision
               == SoldierArtDecision::Missing);
        assert(!compose(image.scene).complete());
        const auto expectedClassic = renderClassic(image.scene);
        clear(renderer);
        const auto before = read(renderer);
        const int hd = win.TryRenderMissionHD(&image, src, dst);
        assert(hd == -1 && read(renderer) == before && live == 0);
        // Same fallback draw as cWindow::Draw.
        assert(SDL_RenderTexture(renderer, image.tex, &src, &dst));
        assert(read(renderer) == expectedClassic);
        image.scene = scene;
        clear(renderer);
        assert(win.TryRenderMissionHD(&image, src, dst) == 1 && read(renderer) == expected);
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
    if (fixture.contains("enemy_prone")) {
        assert(withBox);
        const auto& row = fixture.at("enemy_prone");
        const std::string enemyKey = "0ae80fd93ee8120c3e003e5b0e9383b2514910c7353812e498a587247d5455d8";
        auto enemy = nativeLayer(row, fixture.at("enemy_snapshots"), 8, 39, 20);
        assert(SoldierVariantKey(enemy.soldier, colors) == enemyKey);
        const auto art = registry.resolve(enemy.soldier, enemyKey, density);
        assert(art.decision == SoldierArtDecision::Replace && art.width == 16 && art.height == 14);

        auto withoutLast = scene;
        const auto lastBody = withoutLast.layers.back();
        withoutLast.layers.pop_back();
        auto withEnemy = withoutLast;
        withEnemy.layers.push_back(enemy);
        const auto earlier = compose(withoutLast);
        const auto enemyFrame = compose(withEnemy);
        withEnemy.layers.push_back(lastBody);
        const auto ordered = compose(withEnemy);
        assert(ordered.complete() && ordered.replaced == 6 && ordered.kept == 3);
        size_t overEarlier = 0, underLater = 0, visibleEnemy = 0;
        for (const auto& [offset, cell] : enemyFrame.cells) {
            const auto previous = earlier.cells.find(offset);
            if (previous == earlier.cells.end() || previous->second == cell)
                continue;
            ++overEarlier;
            underLater += ordered.cells.at(offset) != cell;
        }
        for (const auto& [offset, cell] : ordered.cells) {
            const auto withoutEnemy = frame.cells.find(offset);
            visibleEnemy += withoutEnemy == frame.cells.end() || withoutEnemy->second != cell;
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
        std::cout << "PASS A.1 enemy 0x59/F0 SDL " << density << "x: 6 bodies, overlaps "
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
