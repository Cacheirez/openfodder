// GPL-3.0-or-later. Exact Amiga F4 and optional roof F0 with five native bodies.
nlohmann::json fixture;
{
    std::ifstream file(std::getenv("OPENFODDER_A1_RANK_F4"));
    file >> fixture;
}
const auto& rows = fixture.at("bodies");
const auto& rankRow = fixture.at("rank");
const std::string rankKey = "84a0ee13d651ee9f27afe2d9284cacb3b3b53c18658c934effc0ba0942a0be5f";
const std::string roofKey = "5fc9fc6b277ef4b4f27f2552b6a212827b18f31e8e3dc4c6979cb98c4e64d9f7";
const bool withRoof = fixture.contains("roof");
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
const auto retained = withRoof
    ? nativeLayer(fixture.at("roof"), fixture.at("rank_snapshots"), 6, 32, -9)
    : rank;
image.scene.layers.clear();
if (withRoof)
    image.scene.layers.push_back(rank);
const std::array<int, 5> positions{8, 32, 61, 76, 39};
for (size_t i = 0; i < rows.size(); ++i)
    image.scene.layers.push_back(nativeLayer(rows[i], fixture.at("body_snapshots"),
                                            int(i), positions[i], withRoof ? 0 : 20));
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
    assert(SoldierVariantKey(retained.soldier, colors) == roofKey);
    assert(registry.resolve(retained.soldier, roofKey, 8).decision == SoldierArtDecision::KeepClassic);
    auto invalid = retained.soldier;
    invalid.soldier.inVehicle = true;
    assert(registry.resolve(invalid, roofKey, 8).decision == SoldierArtDecision::Missing);
    invalid = retained.soldier;
    invalid.soldier.pendingDestroy = true;
    assert(registry.resolve(invalid, roofKey, 8).decision == SoldierArtDecision::Missing);
    invalid = retained.soldier;
    invalid.resource = {};
    assert(registry.resolve(invalid, roofKey, 8).decision == SoldierArtDecision::Missing);
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
    const size_t kept = withRoof ? 2 : 1;
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
    std::vector<uint32_t> expectedPixels(width * height);
    for (size_t y = 0; y < height; ++y) {
        for (size_t x = 0; x < width; ++x) {
            const size_t offset = (y / density) * 96 + x / density;
            const auto cell = frame.cells.find(offset);
            expectedPixels[y * width + x] = cell == frame.cells.end()
                ? frame.background.pixels[offset] : cell->second[(y % density) * density + x % density];
        }
    }
    auto oracle = texture(renderer, expectedPixels, int(width), int(height));
    const SDL_FRect full{0, 0, float(width), float(height)};
    clear(renderer);
    assert(SDL_RenderTexture(renderer, oracle, &full, &dst));
    const auto expected = read(renderer);
    SDL_DestroyTexture(oracle);
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
    std::cout << "PASS A.1 " << (withRoof ? "roof F0 + F4" : "F4") << " SDL " << density
              << "x: 5 native bodies, " << writes.size()
              << " retained writes, overlaps " << coversHD << '/' << coveredByHD
              << ", visible " << visible << ", 2 whole-frame classic returns and recovery\n";
}
