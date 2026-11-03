// Actual Window method, explicit resource bindings and real SDL renderer.
assert(SoldierSHA256({})=="e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855");
assert(SoldierSHA256({'a','b','c'})=="ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad");
const std::string longVector="abcdbcdecdefdefgefghfghighijhijkijkljklmklmnlmnomnopnopq";
assert(SoldierSHA256(std::vector<uint8_t>(longVector.begin(),longVector.end()))=="248d6a61d20638b8e5c026930c3e6039a33ce45964ff2167f6ecedd419db06c1");
const auto colors=image.scene.destinations[0].initial.indexed.colors;
const auto key=SoldierVariantKey(body.soldier,colors);
auto moved=body.soldier;moved.soldier.slot=9;moved.soldier.scene=77;moved.resource.generation=999;
moved.soldier.geometry.spriteX+=3;moved.soldier.geometry.rowsToSkip=4;
auto input=moved.soldier.geometry;input.source=moved.resource.source();moved.draw=PrepareSpriteDraw(input);
assert(SoldierVariantKey(moved,colors)==key);
auto changed=body.soldier;
auto bytes=std::make_shared<std::vector<uint8_t>>(*changed.resource.bytes);(*bytes)[changed.resource.offset]^=1;
changed.resource.bytes=bytes;assert(SoldierVariantKey(changed,colors)!=key);
auto recolored=colors;recolored[5]^=1;assert(SoldierVariantKey(body.soldier,recolored)!=key);
changed=body.soldier;changed.soldier.personType++;assert(SoldierVariantKey(changed,colors)!=key);
changed=body.soldier;changed.resource.palette++;assert(SoldierVariantKey(changed,colors)!=key);
changed=body.soldier;changed.resource.offset++;assert(SoldierVariantKey(changed,colors)!=key);
// Full uncut pose must remain in bounds even if the current draw is cropped.
changed=body.soldier;changed.resource.bytes=std::make_shared<const std::vector<uint8_t>>(changed.resource.offset+1,0);
bool badExtent=false;try{SoldierVariantKey(changed,colors);}catch(const std::out_of_range&){badExtent=true;}assert(badExtent);
nlohmann::json manifest={{"version",1},{"bindings",nlohmann::json::array({
    {{"key",key},{"decision","replace-pilot"},{"sheet",7},{"frame",0}}})}};
const auto registry=OrderedSoldierRegistry(manifest);
assert(registry.resolve(moved,key,8).decision==SoldierArtDecision::Replace);
assert(registry.resolve(body.soldier,SoldierVariantKey(body.soldier,recolored),8).decision==SoldierArtDecision::Missing);
auto duplicate=manifest;duplicate["bindings"].push_back(duplicate["bindings"][0]);
bool rejectedDuplicate=false;try{OrderedSoldierRegistry bad(duplicate);}catch(const std::invalid_argument&){rejectedDuplicate=true;}assert(rejectedDuplicate);
auto keep=manifest;keep["bindings"][0]["decision"]="keep-associated";
assert(OrderedSoldierRegistry(keep).resolve(body.soldier,key,8).decision==SoldierArtDecision::Missing);
const char* path="ordered-window-test-bindings.json";
{std::ofstream file(path);file<<manifest.dump();}
env("OPENFODDER_SOLDIER_ORDERED_MANIFEST",path);
auto second=body;second.soldier.soldier.slot=1;
second.soldier.soldier.geometry.spriteX+=4;second.soldier.soldier.geometry.rowsToSkip=3;
input=second.soldier.soldier.geometry;input.source=second.soldier.resource.source();second.soldier.draw=PrepareSpriteDraw(input);
MissionLayer cover;cover.destination=body.destination;
cover.pixels.put((body.soldier.draw.y+5)*96+body.soldier.draw.x+5,5);
image.scene.layers={body,second,cover};
for(const char* density:{"8","12"}){
    env("OPENFODDER_SOLDIER_HD",density);const unsigned d=unsigned(std::stoi(density));
    const auto composed=ComposeOrderedSoldierArt(image.scene,body.destination,d,[&](const PreparedSpriteDraw& p){
        return registry.resolve(p,SoldierVariantKey(p,colors),d);});
    assert(composed.complete()&&composed.replaced==2);
    std::vector<uint32_t> expanded(96*64*d*d);
    for(size_t y=0;y<64*d;++y)for(size_t x=0;x<96*d;++x){
        const size_t n=(y/d)*96+x/d;const auto cell=composed.cells.find(n);
        expanded[y*96*d+x]=cell==composed.cells.end()?composed.background.pixels[n]:cell->second[(y%d)*d+x%d];
    }
    auto oracle=texture(renderer,expanded,96*d,64*d);SDL_FRect full{0,0,96.f*d,64.f*d};
    clear(renderer);assert(SDL_RenderTexture(renderer,oracle,&full,&dst));auto expected=read(renderer);
    clear(renderer);assert(win.TryRenderMissionHD(&image,src,dst)==1);assert(read(renderer)==expected);
    SDL_DestroyTexture(oracle);
    image.scene.layers[1].soldier.soldier.frame=1;
    clear(renderer);const auto before=read(renderer);assert(win.TryRenderMissionHD(&image,src,dst)==-1);assert(read(renderer)==before);
    image.scene.layers[1]=second;
    image.scene.destinations[0].initial.indexed.colors=recolored;assert(win.TryRenderMissionHD(&image,src,dst)==-1);
    image.scene.destinations[0].initial.indexed.colors=colors;assert(win.TryRenderMissionHD(&image,src,dst)==1);
    image.adjusting=true;assert(win.TryRenderMissionHD(&image,src,dst)==-1);image.adjusting=false;
    assert(win.TryRenderMissionHD(&image,src,dst)==1);
}
env("OPENFODDER_SOLDIER_ORDERED_MANIFEST","nonexistent-ordered-bindings.json");
assert(win.TryRenderMissionHD(&image,src,dst)==-1);
env("OPENFODDER_SOLDIER_ORDERED_MANIFEST","");std::remove(path);
std::cout<<"PASS ordered Window: resource/palette identity, multiple bodies, water, occlusion, missing binding and load failure\n";
