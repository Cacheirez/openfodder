// Actual Window/SDL route with private native data and a v3 pose manifest.
const std::string root=std::getenv("OPENFODDER_PLAYER_POSE_CASE");
nlohmann::json row;{std::ifstream file(root+"/native.json");file>>row;assert(file);}
const auto colors=row.at("colors").get<std::array<uint32_t,255>>();
image.scene.destinations[0].initial.indexed.colors=colors;
const std::string manifest=std::getenv("OPENFODDER_PLAYER_MANIFEST");
const auto registry=OrderedSoldierRegistry::Load(manifest);
env("OPENFODDER_SOLDIER_ORDERED_MANIFEST",manifest.c_str());
env("OPENFODDER_SOLDIER_ORDERED_HYBRID","1");env("OPENFODDER_PLAYER_CATALOG","1");
auto first=body;first.soldier=LoadNativeWalkSnapshot(row,root+"/native-resources");
auto& p=first.soldier;auto& s=p.soldier;auto& g=s.geometry;
p.resource.generation=1; // The private loader predates producer cache generations.
s.scene=fodder.mPresentationScene;s.interval=1;s.generation=1;s.slot=0;
g.spriteX=32;g.spriteY=20;g.xBias=0;g.viewWidth=96;g.viewHeight=64;
const auto* slot=FindCF1PlayerNativeSlot(int(g.format),s.type,s.sheet,s.frame);assert(slot && slot->role==1);
p.nativeAmiga8={s.type,s.sheet,s.frame,s.segment,uint16_t(p.resource.offset),g.columns,g.rows,g.modX,g.modY,
    s.scene,s.generation,s.slot,p.resource.generation,p.resource.bytes};
p.nativeAmiga8.cf1=true;p.nativeAmiga8.role=1;p.nativeAmiga8.layout=p.resource.layout;
p.nativeAmiga8.palette=p.resource.palette;p.nativeAmiga8.frameOffset=slot->offset;
auto prepare=[](PreparedSpriteDraw& draw){auto input=draw.soldier.geometry;input.source=draw.resource.source();
    draw.draw=PrepareSpriteDraw(input);draw.draw.source=nullptr;};
size_t cases=0;
const auto animations=row.value("test_animations",std::vector<int>{1,10});
assert(!animations.empty() && animations.size()<=14);
for(int animation:animations)assert(IsCF1PlayerAnimation(animation));
for(int animation:animations)for(int variant:{0,1,2,3})for(unsigned density:{8u,12u}){
    s.animation=animation;g.height=variant==1?12:0;g.rowsToSkip=variant==2?3:0;prepare(p);
    auto second=first;second.soldier.soldier.slot=1;second.soldier.nativeAmiga8.slot=1;
    second.soldier.soldier.geometry.spriteX+=4;prepare(second.soldier);
    image.scene.layers={first,second};
    const size_t coverAt=size_t(p.draw.y+5)*96+p.draw.x+6;
    if(variant==3){MissionLayer cover;cover.destination=body.destination;cover.pixels.put(coverAt,0);image.scene.layers.push_back(cover);}
    const auto resolve=[&](const PreparedSpriteDraw& draw){return registry.resolve(draw,SoldierVariantKey(draw,colors),density,true,96,96*64);};
    const auto composed=ComposeOrderedSoldierArt(image.scene,body.destination,density,resolve);
    assert(composed.complete()&&composed.replaced==2&&!composed.cells.empty());
    if(variant==3)assert(!composed.cells.count(coverAt));
    for(int mutation:{0,1}){auto bad=p;if(mutation==0)bad.soldier.animation=777;else ++bad.resource.offset;
        bool caught=false;try{resolve(bad);}catch(const std::invalid_argument&){caught=true;}assert(caught);}
    std::vector<uint32_t> expanded(96*64*density*density);
    for(size_t y=0;y<64*density;++y)for(size_t x=0;x<96*density;++x){
        const size_t at=(y/density)*96+x/density;const auto cell=composed.cells.find(at);
        expanded[y*96*density+x]=cell==composed.cells.end()?composed.background.pixels[at]:cell->second[(y%density)*density+x%density];
    }
    auto oracle=texture(renderer,expanded,96*density,64*density);SDL_FRect full{0,0,96.f*density,64.f*density};clear(renderer);
    assert(SDL_RenderTexture(renderer,oracle,&full,&dst));const auto expected=read(renderer);SDL_DestroyTexture(oracle);
    const auto native=RasterizeMissionLayers(image.scene,body.destination);
    assert(SDL_UpdateTexture(image.tex,nullptr,native.pixels.data(),96*4));clear(renderer);
    assert(SDL_RenderTexture(renderer,image.tex,&src,&dst));const auto classicPixels=read(renderer);
    env("OPENFODDER_SOLDIER_HD",std::to_string(density).c_str());clear(renderer);callNumber=0;
    assert(win.TryRenderMissionHD(&image,src,dst)==1&&read(renderer)==expected&&expected!=classicPixels);
    const auto lastCall=callNumber;clear(renderer);callNumber=0;failAt=lastCall;
    assert(win.TryRenderMissionHD(&image,src,dst)==1&&read(renderer)==classicPixels&&live==0);failAt=0;
    image.scene.destinations[0].initial.indexed.colors[254]^=1;clear(renderer);
    assert(win.TryRenderMissionHD(&image,src,dst)==1&&read(renderer)==expected);
    image.scene.destinations[0].initial.indexed.colors=colors;
    ++cases;
}
std::cout<<"PASS pose Window: "<<cases<<" cases, two actors, exact SDL, height/crop/zero occlusion, state/palette aliases, negatives and recovery\n";
