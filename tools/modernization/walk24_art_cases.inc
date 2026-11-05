// Full artistic walk: actual Window/SDL, either controlled or real source keys.
const std::string directory=std::getenv("OPENFODDER_WALK24_ART");
const std::string manifestPath=directory+"/candidate-manifest.json";
nlohmann::json manifest;
{std::ifstream file(manifestPath);file>>manifest;assert(file);}
assert(manifest["assets"].size()==48 && manifest["bindings"].size()==94);
struct WalkCase {PreparedSpriteDraw p;std::array<uint32_t,255> colors;};
std::vector<WalkCase> cases;
const auto baseColors=image.scene.destinations[0].initial.indexed.colors;
const char* nativePath=std::getenv("OPENFODDER_WALK24_NATIVE_INPUT");
const bool native=nativePath && *nativePath;
std::string selectedPath=manifestPath;
if(native){
    nlohmann::json input;{std::ifstream file(nativePath);file>>input;assert(file);}
    std::map<std::string,std::map<int,WalkCase>> groups;
    for(const auto& row:input.at("rows")){
        assert(row.at("animation")==0);
        const auto p=LoadNativeWalkSnapshot(row,input.at("snapshots").get<std::string>());
        const auto colors=row.at("colors").get<std::array<uint32_t,255>>();
        const auto key=SoldierVariantKey(p,colors);assert(key==row.at("key").get<std::string>());
        const auto group=row.at("format").dump()+":"+row.at("resource_sha256").get<std::string>()+":"+row.at("colors").dump();
        assert(groups[group].emplace(p.soldier.sheet*3+p.soldier.frame,WalkCase{p,colors}).second);
    }
    assert(groups.size()==4);
    size_t complete=0,partial=0;
    for(const auto& group:groups){
        if(group.second.size()==24){
            ++complete;
            for(int direction=0;direction<8;++direction)for(int frame:{0,1,2,1})cases.push_back(group.second.at(direction*3+frame));
        }else{
            assert(group.second.size()==22);++partial;
            for(const auto& entry:group.second)cases.push_back(entry.second);
        }
    }
    assert(complete==3 && partial==1 && cases.size()==118);
}else{
    // Controlled keys are explicit test-only rebinding; never claimed as real variants.
    manifest["bindings"]=nlohmann::json::array();
    for(int platform:{0,1})for(int variant:{0,1}){
        std::vector<WalkCase> poses;
        for(int pose=0;pose<24;++pose){
            auto p=soldier(platform==1,0).soldier;
            const auto* data=orderedWalkFixture[platform][pose];
            auto& s=p.soldier;auto& g=s.geometry;
            s.sheet=data[0];s.frame=data[1];s.faceDirection=(pose/3)*2;s.personType=variant;
            p.resource.offset=data[2];g.modX=data[3];g.modY=data[4];g.columns=data[5];g.rows=data[6];
            p.draw.format=g.format;p.draw.palette=g.palette;
            auto colors=baseColors;colors[5]^=variant;
            const auto key=SoldierVariantKey(p,colors);
            manifest["bindings"].push_back({{"key",key},{"decision","replace-art"},
                {"assets",{{"8","s"+std::to_string(s.sheet)+"-f"+std::to_string(s.frame)+"-8"},
                           {"12","s"+std::to_string(s.sheet)+"-f"+std::to_string(s.frame)+"-12"}}}});
            poses.push_back({p,colors});
        }
        for(int direction=0;direction<8;++direction)for(int frame:{0,1,2,1})cases.push_back(poses[direction*3+frame]);
    }
    selectedPath=directory+"/controlled-manifest.json";
    {std::ofstream file(selectedPath);file<<manifest.dump();assert(file);}
    assert(cases.size()==128);
}
const auto registry=OrderedSoldierRegistry::Load(selectedPath);
env("OPENFODDER_SOLDIER_ORDERED_MANIFEST",selectedPath.c_str());
size_t steps=0;
for(unsigned d:{8u,12u})for(const auto& item:cases){
    auto first=body;first.soldier=item.p;
    image.scene.destinations[0].initial.indexed.colors=item.colors;
    auto& s=first.soldier.soldier;auto& g=s.geometry;
    s.scene=fodder.mPresentationScene;s.interval=1000+steps;s.slot=0;s.generation=1;
    g.spriteX=32;g.spriteY=20;g.xBias=0;g.viewWidth=96;g.viewHeight=64;
    auto geometry=g;geometry.source=first.soldier.resource.source();first.soldier.draw=PrepareSpriteDraw(geometry);
    const auto art=registry.resolve(first.soldier,SoldierVariantKey(first.soldier,item.colors),d);
    assert(art.decision==SoldierArtDecision::Replace);
    if(s.sheet==7 && s.frame==0)assert(*art.pixels==*SoldierBatchAsset(7,0,d).pixels);
    auto second=first;second.soldier.soldier.slot=1;
    second.soldier.soldier.geometry.spriteX+=4;second.soldier.soldier.geometry.rowsToSkip=3;
    geometry=second.soldier.soldier.geometry;geometry.source=second.soldier.resource.source();second.soldier.draw=PrepareSpriteDraw(geometry);
    MissionLayer cover;cover.destination=body.destination;
    cover.pixels.put((first.soldier.draw.y+5)*96+first.soldier.draw.x+5,5);
    image.scene.layers={first,second,cover};
    const auto composed=ComposeOrderedSoldierArt(image.scene,body.destination,d,[&](const PreparedSpriteDraw& p){
        return registry.resolve(p,SoldierVariantKey(p,item.colors),d);});
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
assert(steps==(native?236u:256u));
// Scope does not silently expand into enemies, damage/sliding or unknown palettes.
const auto supported=image.scene;
for(int missing=0;missing<3;++missing){
    image.scene=supported;
    for(auto& layer:image.scene.layers)if(layer.operation==MissionLayerOperation::Soldier){
        layer.soldier.soldier.interval=2000+missing;
        if(missing==0)layer.soldier.soldier.type=5;
        if(missing==1)layer.soldier.soldier.animation=0x32;
    }
    if(missing==2)image.scene.destinations[0].initial.indexed.colors[5]^=1;
    clear(renderer);const auto before=read(renderer);
    assert(win.TryRenderMissionHD(&image,src,dst)==-1 && read(renderer)==before);
}
env("OPENFODDER_SOLDIER_ORDERED_MANIFEST","");
if(!native)std::remove(selectedPath.c_str());
std::cout<<"PASS walk24 "<<(native?"real":"controlled")<<": 24 artistic keys, "<<steps<<" published SDL intervals, C01 exact, three scope rejections\n";
