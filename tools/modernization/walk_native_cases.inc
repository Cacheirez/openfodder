// Actual replay resource bytes, palette and key, without fixture rebinding.
const std::string directory=std::getenv("OPENFODDER_WALK_NATIVE_REVIEW");
nlohmann::json input;
{std::ifstream file(directory+"/native-input.json");file>>input;assert(file);}
const std::string manifestPath=input.at("manifest"),snapshotDirectory=input.at("snapshots");
const auto registry=OrderedSoldierRegistry::Load(manifestPath);
env("OPENFODDER_SOLDIER_ORDERED_MANIFEST",manifestPath.c_str());
std::map<std::string,std::map<int,nlohmann::json>> cycles;
std::vector<nlohmann::json> special;
for(const auto& row:input.at("rows")){
    assert(row.at("sheet")==7);
    if(row.at("animation")!=0){special.push_back(row);continue;}
    const std::string group=std::to_string(row.at("format").get<int>())+":"+
        row.at("resource_sha256").get<std::string>()+":"+row.at("colors").dump()+":"+row.at("person").dump();
    assert(cycles[group].emplace(row.at("frame").get<int>(),row).second);
}
assert(cycles.size()==4 && special.size()==1 && special[0].at("animation")==0x32);
std::vector<nlohmann::json> sequence;
for(const auto& group:cycles){
    assert(group.second.size()==3);
    for(int frame:{0,1,2,1})sequence.push_back(group.second.at(frame));
}
sequence.push_back(special[0]); // Slide1 shares this native body; separate state, not ordinary walk.
size_t steps=0;
for(unsigned d:{8u,12u})for(const auto& row:sequence){
    auto first=body;
    first.soldier=LoadNativeWalkSnapshot(row,snapshotDirectory);
    const auto colors=row.at("colors").get<std::array<uint32_t,255>>();
    image.scene.destinations[0].initial.indexed.colors=colors;
    auto& s=first.soldier.soldier;auto& g=s.geometry;
    s.scene=fodder.mPresentationScene;s.interval=300+steps;s.slot=0;s.generation=1;
    g.spriteX=32;g.spriteY=20;g.xBias=0;g.viewWidth=96;g.viewHeight=64;
    auto geometry=g;geometry.source=first.soldier.resource.source();first.soldier.draw=PrepareSpriteDraw(geometry);
    const auto key=SoldierVariantKey(first.soldier,colors);
    assert(key==row.at("key").get<std::string>());
    const auto art=registry.resolve(first.soldier,key,d);
    assert(art.decision==SoldierArtDecision::Replace);
    if(s.frame==0)assert(*art.pixels==*SoldierBatchAsset(7,0,d).pixels);
    auto second=first;second.soldier.soldier.slot=1;
    second.soldier.soldier.geometry.spriteX+=4;second.soldier.soldier.geometry.rowsToSkip=3;
    geometry=second.soldier.soldier.geometry;geometry.source=second.soldier.resource.source();second.soldier.draw=PrepareSpriteDraw(geometry);
    MissionLayer cover;cover.destination=body.destination;
    cover.pixels.put((first.soldier.draw.y+5)*96+first.soldier.draw.x+5,5);
    image.scene.layers={first,second,cover};
    const auto composed=ComposeOrderedSoldierArt(image.scene,body.destination,d,[&](const PreparedSpriteDraw& p){
        return registry.resolve(p,SoldierVariantKey(p,colors),d);});
    assert(composed.complete() && composed.replaced==2);
    std::vector<uint32_t> expanded(96*64*d*d);
    for(size_t y=0;y<64*d;++y)for(size_t x=0;x<96*d;++x){
        const size_t n=(y/d)*96+x/d;const auto cell=composed.cells.find(n);
        expanded[y*96*d+x]=cell==composed.cells.end()?composed.background.pixels[n]:cell->second[(y%d)*d+x%d];
    }
    auto oracle=texture(renderer,expanded,96*d,64*d);SDL_FRect full{0,0,96.f*d,64.f*d};
    clear(renderer);assert(SDL_RenderTexture(renderer,oracle,&full,&dst));const auto expected=read(renderer);
    env("OPENFODDER_SOLDIER_HD",std::to_string(d).c_str());
    clear(renderer);assert(win.TryRenderMissionHD(&image,src,dst)==1 && read(renderer)==expected);
    SDL_DestroyTexture(oracle);++steps;
}
assert(steps==34);
env("OPENFODDER_SOLDIER_ORDERED_MANIFEST","");
std::cout<<"PASS native walk: 13 real keys, four original-resource cycles and separate Slide1, 34 SDL intervals / 68 bodies, C01 exact\n";
