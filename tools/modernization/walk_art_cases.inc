// Real generated masters, controlled resource fixtures. No campaign approval.
const std::string directory=std::getenv("OPENFODDER_WALK_ART_REVIEW");
nlohmann::json art;
{std::ifstream file(directory+"/candidate-manifest.json");file>>art;assert(file);}
assert(art["assets"].size()==6 && art["bindings"].size()==13);
// Observed campaign hashes are only candidates. Rebind controlled test resources
// explicitly; never claim that synthetic source pixels exercise those hashes.
art["bindings"]=nlohmann::json::array();
const auto baseColors=image.scene.destinations[0].initial.indexed.colors;
auto poseBody=[&](int platform,int frame){
    auto result=soldier(platform==1,0);result.destination=body.destination;
    const auto* data=orderedWalkFixture[platform][21+frame];
    auto& p=result.soldier;auto& s=p.soldier;auto& g=s.geometry;
    s.sheet=data[0];s.frame=data[1];s.faceDirection=14;s.direction=2;
    p.resource.offset=data[2];g.modX=data[3];g.modY=data[4];g.columns=data[5];g.rows=data[6];
    auto input=g;input.source=p.resource.source();p.draw=PrepareSpriteDraw(input);return result;
};
for(int platform:{0,1})for(int variant:{0,1})for(int frame:{0,1,2}){
    auto p=poseBody(platform,frame);p.soldier.soldier.personType=variant;
    auto colors=baseColors;colors[5]^=variant;
    art["bindings"].push_back({{"key",SoldierVariantKey(p.soldier,colors)},{"decision","replace-art"},
        {"assets",{{"8","s7-f"+std::to_string(frame)+"-8"},{"12","s7-f"+std::to_string(frame)+"-12"}}}});
}
const auto registry=OrderedSoldierRegistry(art,directory+"/");
const std::string path=directory+"/fixture-manifest.json";
{std::ofstream file(path);file<<art.dump();assert(file);}
env("OPENFODDER_SOLDIER_ORDERED_MANIFEST",path.c_str());
size_t steps=0;
for(int platform:{0,1})for(int variant:{0,1})for(unsigned d:{8u,12u})for(int frame:{0,1,2,1}){
    auto colors=baseColors;colors[5]^=variant;
    image.scene.destinations[0].initial.indexed.colors=colors;
    auto first=poseBody(platform,frame),second=first;
    first.soldier.soldier.personType=variant;second.soldier.soldier.personType=variant;
    first.soldier.soldier.interval=200+steps;second.soldier.soldier.interval=200+steps;
    second.soldier.soldier.slot=1;second.soldier.soldier.geometry.spriteX+=4;
    second.soldier.soldier.geometry.rowsToSkip=3;
    auto input=second.soldier.soldier.geometry;input.source=second.soldier.resource.source();second.soldier.draw=PrepareSpriteDraw(input);
    MissionLayer cover;cover.destination=body.destination;
    cover.pixels.put((first.soldier.draw.y+5)*96+first.soldier.draw.x+5,5);
    image.scene.layers={first,second,cover};
    const auto resolved=registry.resolve(first.soldier,SoldierVariantKey(first.soldier,colors),d);
    assert(resolved.decision==SoldierArtDecision::Replace);
    if(frame==0){
        const auto original=SoldierBatchAsset(7,0,d).pixels;
        assert(original && *resolved.pixels==*original); // C01 exact, not merely same PNG hash.
    }
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
assert(steps==32);
env("OPENFODDER_SOLDIER_ORDERED_MANIFEST","");std::remove(path.c_str());
std::cout<<"PASS real walk art: 32 SDL intervals, 64 published bodies, C01 byte-identical, candidate bindings NOT campaign approval\n";
