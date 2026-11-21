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
const auto* slot=FindCF1PlayerNativeSlot(int(g.format),s.type,s.sheet,s.frame);assert(slot && (slot->role==1 || slot->role==0 || slot->role==3));
p.nativeAmiga8={s.type,s.sheet,s.frame,s.segment,uint16_t(p.resource.offset),g.columns,g.rows,g.modX,g.modY,
    s.scene,s.generation,s.slot,p.resource.generation,p.resource.bytes};
p.nativeAmiga8.cf1=true;p.nativeAmiga8.role=slot->role;p.nativeAmiga8.layout=p.resource.layout;
p.nativeAmiga8.palette=p.resource.palette;p.nativeAmiga8.frameOffset=slot->offset;
auto prepare=[](PreparedSpriteDraw& draw){auto input=draw.soldier.geometry;input.source=draw.resource.source();
    draw.draw=PrepareSpriteDraw(input);draw.draw.source=nullptr;};
const bool invisible=slot->invisible;
const bool nativeOnly=invisible || slot->role==0;
const bool ownedShadow=slot->role==3;
if(ownedShadow){auto& n=p.nativeAmiga8;n.ownerType=0;n.ownerPerson=0;n.ownerSlot=4;n.ownerGeneration=1;}
assert(row.value("test_invisible",false)==invisible);
auto anchor=body;
if(nativeOnly){
    const auto anchorRoot=root+"/"+row.at("test_visible_anchor").get<std::string>();
    nlohmann::json anchorRow;{std::ifstream file(anchorRoot+"/native.json");file>>anchorRow;assert(file);}
    anchor.soldier=LoadNativeWalkSnapshot(anchorRow,anchorRoot+"/native-resources");
    auto& a=anchor.soldier;auto& as=a.soldier;auto& ag=as.geometry;a.resource.generation=1;
    as.scene=fodder.mPresentationScene;as.interval=1;as.generation=1;as.slot=2;as.animation=0;
    ag.spriteX=64;ag.spriteY=20;ag.xBias=0;ag.viewWidth=96;ag.viewHeight=64;
    const auto* anchorSlot=FindCF1PlayerNativeSlot(int(ag.format),as.type,as.sheet,as.frame);
    assert(anchorSlot && anchorSlot->produced && !anchorSlot->invisible);
    a.nativeAmiga8={as.type,as.sheet,as.frame,as.segment,uint16_t(a.resource.offset),ag.columns,ag.rows,ag.modX,ag.modY,
        as.scene,as.generation,as.slot,a.resource.generation,a.resource.bytes};
    a.nativeAmiga8.cf1=true;a.nativeAmiga8.role=1;a.nativeAmiga8.layout=a.resource.layout;
    a.nativeAmiga8.palette=a.resource.palette;a.nativeAmiga8.frameOffset=anchorSlot->offset;prepare(a);
}
size_t cases=0;
const auto animations=row.value("test_animations",std::vector<int>{1,10});
assert(!animations.empty() && animations.size()<=14);
for(int animation:animations)assert(IsCF1PlayerAnimation(animation));
for(int animation:animations)for(int variant:{0,1,2,3})for(unsigned density:{8u,12u}){
    s.animation=animation;g.height=!ownedShadow && variant==1?12:0;g.rowsToSkip=variant==2?(ownedShadow?1:3):0;
    if(ownedShadow){auto& n=p.nativeAmiga8;n.ownerHeight=s.frame==0?(variant==1?20:12):(variant==1?8:0);
        n.ownerX=32;n.ownerY=20;g.spriteX=n.ownerX+(n.ownerHeight>>2)+5;g.spriteY=n.ownerY+(n.ownerHeight>>2)-3;}
    prepare(p);
    auto second=first;second.soldier.soldier.slot=1;second.soldier.nativeAmiga8.slot=1;
    second.soldier.soldier.geometry.spriteX+=4;
    if(ownedShadow){second.soldier.nativeAmiga8.ownerX+=4;second.soldier.nativeAmiga8.ownerSlot=5;}
    prepare(second.soldier);
    image.scene.layers={first,second};
    if(nativeOnly)image.scene.layers.push_back(anchor);
    const auto& coveredDraw=nativeOnly?anchor.soldier.draw:p.draw;
    const size_t coverAt=size_t(coveredDraw.y+(ownedShadow?1:5))*96+coveredDraw.x+(ownedShadow?3:6);
    if(variant==3){MissionLayer cover;cover.destination=body.destination;cover.pixels.put(coverAt,0);image.scene.layers.push_back(cover);}
    const auto resolve=[&](const PreparedSpriteDraw& draw){return registry.resolve(draw,SoldierVariantKey(draw,colors),density,true,96,96*64);};
    const auto composed=ComposeOrderedSoldierArt(image.scene,body.destination,density,resolve);
    assert(composed.complete()&&composed.replaced==(nativeOnly?1u:2u)&&!composed.cells.empty());
    if(nativeOnly)assert(composed.kept==2);
    if(invisible){for(const auto& hidden:{first,second}){
        auto draw=hidden.soldier.draw;draw.source=hidden.soldier.resource.source();
        assert(CaptureSprite8Producer(draw,hidden.soldier.resource.layout,96).writes.empty());}}
    if(variant==3)assert(!composed.cells.count(coverAt));
    for(int mutation=0;mutation<(ownedShadow?3:2);++mutation){auto bad=p;if(mutation==0){if(slot->role==0)++bad.nativeAmiga8.frameOffset;else if(ownedShadow)bad.nativeAmiga8.ownerGeneration=0;else bad.soldier.animation=777;}
        else if(mutation==1)++bad.resource.offset;
        else {if(ownedShadow)++bad.nativeAmiga8.ownerX;else ++bad.nativeAmiga8.frameOffset;}
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
