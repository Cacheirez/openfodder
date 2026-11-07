// Synthetic art tests the full dispatch contract, not artistic acceptance.
const auto colors=image.scene.destinations[0].initial.indexed.colors;
nlohmann::json external={{"version",2},{"assets",nlohmann::json::array()},{"bindings",nlohmann::json::array()}};
std::vector<std::string> assetFiles;
for(int pose=0;pose<24;++pose)for(unsigned d:{8u,12u}){
    const std::string id="pose-"+std::to_string(pose)+"-"+std::to_string(d),file=id+".rgba";
    std::vector<uint8_t> rgba(16*14*d*d*4);
    for(size_t y=0;y<14*d;++y)for(size_t x=0;x<16*d;++x){
        const size_t n=(y*16*d+x)*4;
        rgba[n]=uint8_t(17+pose*9);rgba[n+1]=uint8_t(y);rgba[n+2]=uint8_t(x);
        rgba[n+3]=x<d?0:x<2*d?128:255;
    }
    {std::ofstream out(file,std::ios::binary);out.write(reinterpret_cast<const char*>(rgba.data()),rgba.size());assert(out);}
    external["assets"].push_back({{"id",id},{"file",file},{"width",16},{"height",14},{"density",d},{"sha256",SoldierSHA256(rgba)}});
    assetFiles.push_back(file);
}
auto walkBody=[&](int platform,int pose){
    auto result=soldier(platform==1,0);result.destination=body.destination;
    const auto* data=orderedWalkFixture[platform][pose];
    auto& p=result.soldier;auto& s=p.soldier;auto& g=s.geometry;
    s.sheet=data[0];s.frame=data[1];s.faceDirection=(pose/3)*2;s.direction=((pose/3+1)%8)*2;
    p.resource.offset=data[2];g.modX=data[3];g.modY=data[4];g.columns=data[5];g.rows=data[6];
    auto geometry=g;geometry.source=p.resource.source();p.draw=PrepareSpriteDraw(geometry);return result;
};
for(int platform:{0,1})for(int pose=0;pose<24;++pose){
    const auto p=walkBody(platform,pose);
    external["bindings"].push_back({{"key",SoldierVariantKey(p.soldier,colors)},{"decision","replace-art"},
        {"assets",{{"8","pose-"+std::to_string(pose)+"-8"},{"12","pose-"+std::to_string(pose)+"-12"}}}});
}
const char* externalPath="ordered-external-bindings.json";
{std::ofstream out(externalPath);out<<external.dump();assert(out);}
const auto externalRegistry=OrderedSoldierRegistry::Load(externalPath);
env("OPENFODDER_SOLDIER_ORDERED_MANIFEST",externalPath);
size_t steps=0;
for(int platform:{0,1})for(unsigned d:{8u,12u})for(int direction=0;direction<8;++direction)for(int frame:{0,1,2,1}){
    const int pose=direction*3+frame;auto first=walkBody(platform,pose),second=first;
    first.soldier.soldier.interval=100+steps;second.soldier.soldier.interval=100+steps;
    second.soldier.soldier.slot=1;second.soldier.soldier.geometry.spriteX+=4;
    second.soldier.soldier.geometry.rowsToSkip=3;
    auto input=second.soldier.soldier.geometry;input.source=second.soldier.resource.source();second.soldier.draw=PrepareSpriteDraw(input);
    const auto key=SoldierVariantKey(first.soldier,colors);
    const auto art=externalRegistry.resolve(first.soldier,key,d);
    assert(art.decision==SoldierArtDecision::Replace && art.width==16 && art.height==14 && art.density==d);
    // Independent byte/channel check; alpha remains straight, not premultiplied.
    assert((*art.pixels)[2*d]==(0xff000000u|(uint32_t(uint8_t(17+pose*9))<<16)|uint32_t(2*d)));
    MissionLayer cover;cover.destination=body.destination;
    cover.pixels.put((first.soldier.draw.y+5)*96+first.soldier.draw.x+5,5);
    image.scene.layers={first,second,cover};
    const auto composed=ComposeOrderedSoldierArt(image.scene,body.destination,d,[&](const PreparedSpriteDraw& p){
        return externalRegistry.resolve(p,SoldierVariantKey(p,colors),d);});
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
assert(steps==128);
// A loaded registry owns immutable bytes; later file changes do not mutate it.
auto changed=walkBody(0,0);const auto unchangedKey=SoldierVariantKey(changed.soldier,colors);
const auto retained=externalRegistry.resolve(changed.soldier,unchangedKey,8).pixels;
{std::ofstream out(assetFiles[0],std::ios::binary|std::ios::in);out.put(char(0));}
assert(externalRegistry.resolve(changed.soldier,unchangedKey,8).pixels==retained);
auto reject=[&](const nlohmann::json& manifest){
    bool rejected=false;try{OrderedSoldierRegistry bad(manifest);}catch(const std::exception&){rejected=true;}
    assert(rejected);
};
reject(external); // Content hash mismatch on reload.
// Remove assets unrelated to each negative case, then use a still-valid file.
auto minimal=external;minimal["assets"]=nlohmann::json::array({external["assets"][1]});
minimal["bindings"]=nlohmann::json::array({{{"key",unchangedKey},{"decision","replace-art"},{"assets",{{"12","pose-0-12"}}}}});
const auto single=OrderedSoldierRegistry(minimal);
assert(single.resolve(changed.soldier,unchangedKey,8).decision==SoldierArtDecision::Missing);
assert(single.resolve(changed.soldier,unchangedKey,12).decision==SoldierArtDecision::Replace);
auto bad=minimal;bad["assets"][0]["width"]=17;reject(bad);
bad=minimal;bad["assets"][0]["height"]=-1;reject(bad);
bad=minimal;bad["assets"][0]["density"]=9;reject(bad);
bad=minimal;bad["assets"][0]["sha256"]=std::string(64,'b');reject(bad);
for(const char* name:{"../pose.rgba","/pose.rgba","C:/pose.rgba","sub\\pose.rgba","./pose.rgba","missing.rgba"}){
    bad=minimal;bad["assets"][0]["file"]=name;reject(bad);
}
bad=minimal;bad["assets"].push_back(bad["assets"][0]);reject(bad);
bad=minimal;bad["bindings"].push_back(bad["bindings"][0]);reject(bad);
bad=minimal;bad["bindings"][0]["assets"]["12"]="unknown";reject(bad);
bad=minimal;bad["bindings"][0]["assets"]={{"8","pose-0-12"}};reject(bad);
bad=minimal;bad["bindings"][0]["assets"]={{"9","pose-0-12"}};reject(bad);
bad=minimal;bad["version"]=1;reject(bad);
bad=minimal;bad["assets"][0]["width"]=352;bad["assets"][0]["height"]=272;
bad["assets"].push_back(bad["assets"][0]);bad["assets"][1]["id"]="second-large";
bool overBudget=false;try{OrderedSoldierRegistry oversized(bad);}catch(const std::length_error&){overBudget=true;}
assert(overBudget); // Reject before any oversized RGBA allocation/file read.
changed.soldier.soldier.geometry.rows=13;
assert(single.resolve(changed.soldier,unchangedKey,12).decision==SoldierArtDecision::Missing);
// Geometry/state beyond the pilot: enemy, animation state, offsets and 32x10 body.
auto wide=walkBody(1,0);wide.soldier.soldier.type=5;wide.soldier.soldier.animation=3;
wide.soldier.soldier.geometry.columns=3;wide.soldier.soldier.geometry.rows=10;
wide.soldier.soldier.geometry.modX=-2;wide.soldier.soldier.geometry.modY=3;
{auto input=wide.soldier.soldier.geometry;input.source=wide.soldier.resource.source();wide.soldier.draw=PrepareSpriteDraw(input);}
std::vector<uint8_t> wideRGBA(32*10*8*8*4,127);
const std::string wideFile="wide-enemy.rgba";
{std::ofstream out(wideFile,std::ios::binary);out.write(reinterpret_cast<const char*>(wideRGBA.data()),wideRGBA.size());}
const auto wideKey=SoldierVariantKey(wide.soldier,colors);
nlohmann::json wideManifest={{"version",2},{"assets",nlohmann::json::array({{{"id","wide"},{"file",wideFile},
    {"width",32},{"height",10},{"density",8},{"sha256",SoldierSHA256(wideRGBA)}}})},
    {"bindings",nlohmann::json::array({{{"key",wideKey},{"decision","replace-art"},{"assets",{{"8","wide"}}}}})}};
const auto wideRegistry=OrderedSoldierRegistry(wideManifest);
image.scene.layers={wide};
const auto wideFrame=ComposeOrderedSoldierArt(image.scene,body.destination,8,[&](const PreparedSpriteDraw& p){
    return wideRegistry.resolve(p,SoldierVariantKey(p,colors),8);});
assert(wideFrame.complete() && wideFrame.replaced==1);
auto civilian=wide.soldier;civilian.soldier.type=72;
const auto civilianKey=SoldierVariantKey(civilian,colors);
assert(wideRegistry.resolve(civilian,civilianKey,8).decision==SoldierArtDecision::Missing);
auto civilianManifest=wideManifest;civilianManifest["bindings"][0]["key"]=civilianKey;
assert(OrderedSoldierRegistry(civilianManifest).resolve(civilian,civilianKey,8).decision==SoldierArtDecision::Replace);
auto marker=wide.soldier;marker.soldier.sheet=0x7c;
const auto markerKey=SoldierVariantKey(marker,colors);
auto markerManifest=wideManifest;markerManifest["bindings"][0]["key"]=markerKey;
assert(OrderedSoldierRegistry(markerManifest).resolve(marker,markerKey,8).decision==SoldierArtDecision::Missing);
// Relative paths are resolved from the manifest directory, not the working directory.
{std::ofstream out("nested/"+wideFile,std::ios::binary);out.write(reinterpret_cast<const char*>(wideRGBA.data()),wideRGBA.size());assert(out);}
{std::ofstream out("nested/ordered-relative-test.json");out<<wideManifest.dump();assert(out);}
std::remove(wideFile.c_str());
assert(OrderedSoldierRegistry::Load("nested/ordered-relative-test.json").resolve(wide.soldier,wideKey,8).pixels);
for(const auto& file:assetFiles)std::remove(file.c_str());
std::remove(("nested/"+wideFile).c_str());std::remove("nested/ordered-relative-test.json");std::remove(externalPath);
env("OPENFODDER_SOLDIER_ORDERED_MANIFEST","");
std::cout<<"PASS external assets: 24 keys PC/Amiga, original 0-1-2-1 dispatch, 8x/12x, 128 SDL intervals, water/occlusion, immutable RGBA and negative manifests; art acceptance PENDING\n";
