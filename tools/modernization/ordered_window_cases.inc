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
    // Resolution is not publication: exercise both SDL recovery outcomes.
    clear(renderer);callNumber=0;failAt=1;
    assert(win.TryRenderMissionHD(&image,src,dst)==1 && live==0);
    callNumber=0;secondFail=2;
    assert(win.TryRenderMissionHD(&image,src,dst)==0 && live==0);
    failAt=secondFail=0;
    assert(win.TryRenderMissionHD(&image,src,dst)==1);
    image.scene.layers={cover};assert(win.TryRenderMissionHD(&image,src,dst)==-1);
    image.scene.layers={body,second,cover};
    image.scene.layers[1].soldier.resource.bytes=std::make_shared<const std::vector<uint8_t>>(1,0);
    assert(win.TryRenderMissionHD(&image,src,dst)==-1); // Partial census is not publication.
    image.scene.layers={body,second,cover};
}
// A.1: explicit scenery classification, native writes over modern cells,
// cropped sprites, and whole-interval rejection/recovery with real SDL.
{
    const char* associatedPath="ordered-window-associated-bindings.json";
    const char* absentPath="ordered-window-absent-body.json";
    auto bird=body;auto& p=bird.soldier;auto& s=p.soldier;
    s.type=19;s.sheet=0x98;s.frame=0;
    p.resource.bytes=std::make_shared<const std::vector<uint8_t>>(40*32*4,0xaa);
    p.resource.offset=0;p.resource.layout={SpriteDrawFormat::Amiga8,320,32,4};
    s.geometry.format=SpriteDrawFormat::Amiga8;s.geometry.columns=2;
    s.geometry.rowsToSkip=3;s.geometry.spriteX+=4;
    auto prepareBird=[&](){auto g=s.geometry;g.source=p.resource.source();p.draw=PrepareSpriteDraw(g);};
    prepareBird();
    auto associated=manifest;
    for(int frame:{0,1}){
        s.frame=frame;associated["bindings"].push_back({{"key",SoldierVariantKey(p,colors)},{"decision","keep-associated"}});
    }
    auto rank=bird;rank.soldier.soldier.type=21;rank.soldier.soldier.sheet=0x95;rank.soldier.soldier.frame=0;
    associated["bindings"].push_back({{"key",SoldierVariantKey(rank.soldier,colors)},{"decision","keep-associated"}});
    const OrderedSoldierRegistry scoped(associated);
    for(int frame:{0,1}){
        s.frame=frame;prepareBird();
        assert(scoped.resolve(p,SoldierVariantKey(p,colors),12).decision==SoldierArtDecision::KeepClassic);
        assert(scoped.resolve(p,SoldierVariantKey(p,recolored),12).decision==SoldierArtDecision::Missing);
        for(const char* density:{"8","12"}){
            {std::ofstream file(associatedPath);file<<associated.dump();}
            env("OPENFODDER_SOLDIER_HD",density);const unsigned d=unsigned(std::stoi(density));
            env("OPENFODDER_SOLDIER_ORDERED_MANIFEST",associatedPath);
            image.scene.layers={body,bird,rank,cover};
            const auto composed=ComposeOrderedSoldierArt(image.scene,body.destination,d,[&](const PreparedSpriteDraw& q){
                return scoped.resolve(q,SoldierVariantKey(q,colors),d);});
            assert(composed.complete()&&composed.replaced==1&&composed.kept==2);
            const auto classic=RasterizeMissionLayers(image.scene,body.destination);
            // Native associated producer writes erase HD cells, including equal
            // colours; their clipped pixels retain the independently drawn RGB.
            for(const auto& layer:{bird,rank}){
                auto draw=layer.soldier.draw;draw.source=layer.soldier.resource.source();
                for(const auto& v:CaptureSprite8Producer(draw,layer.soldier.resource.layout,96).writes){
                    assert(!composed.cells.count(size_t(v.offset)));
                    assert(composed.background.pixels[size_t(v.offset)]==classic.pixels[size_t(v.offset)]);
                }
            }
            std::vector<uint32_t> expectedPixels(96*64*d*d);
            for(size_t y=0;y<64*d;++y)for(size_t x=0;x<96*d;++x){
                const size_t n=(y/d)*96+x/d;const auto cell=composed.cells.find(n);
                expectedPixels[y*96*d+x]=cell==composed.cells.end()?composed.background.pixels[n]:cell->second[(y%d)*d+x%d];
            }
            auto oracle=texture(renderer,expectedPixels,96*d,64*d);
            SDL_FRect full{0,0,96.f*d,64.f*d};
            clear(renderer);assert(SDL_RenderTexture(renderer,oracle,&full,&dst));const auto expected=read(renderer);
            clear(renderer);assert(win.TryRenderMissionHD(&image,src,dst)==1&&read(renderer)==expected);
            SDL_DestroyTexture(oracle);
            auto absent=associated;absent["bindings"].erase(absent["bindings"].begin());
            {std::ofstream file(absentPath);file<<absent.dump();}
            env("OPENFODDER_SOLDIER_ORDERED_MANIFEST",absentPath);
            clear(renderer);const auto before=read(renderer);
            assert(win.TryRenderMissionHD(&image,src,dst)==-1&&read(renderer)==before);
            {std::ofstream file(associatedPath);file<<associated.dump();}
            env("OPENFODDER_SOLDIER_ORDERED_MANIFEST",associatedPath);
            assert(win.TryRenderMissionHD(&image,src,dst)==1);
        }
    }
    // Even a deliberately bound key cannot exempt another body, civilian,
    // bird frame/sheet/format, vehicle or destroyed sprite.
    for(int variant=0;variant<9;++variant){
        auto bad=p;auto& b=bad.soldier;
        if(variant<3)b.type=variant==0?0:variant==1?5:61;
        if(variant==3)b.frame=2;if(variant==4)b.sheet=0x97;
        if(variant==5)b.geometry.format=SpriteDrawFormat::PC;
        if(variant==6)b.inVehicle=true;if(variant==7)b.pendingDestroy=true;
        if(variant==8)b.valid=false;
        const auto bound=SoldierSHA256({uint8_t(variant)});
        const OrderedSoldierRegistry deny({{"version",1},{"bindings",nlohmann::json::array({{{"key",bound},{"decision","keep-associated"}}})}});
        assert(deny.resolve(bad,bound,12).decision==SoldierArtDecision::Missing);
    }
    std::remove(associatedPath);std::remove(absentPath);
    image.scene.layers={body,second,cover};
    std::cout<<"PASS A.1 associated: two bird frames, rank, explicit keys, classic clipped writes, body rejection and SDL recovery\n";
}
env("OPENFODDER_SOLDIER_ORDERED_MANIFEST","nonexistent-ordered-bindings.json");
assert(win.TryRenderMissionHD(&image,src,dst)==-1);
if(std::getenv("OPENFODDER_TEST_ORDERED_HYBRID")){
    auto tree=body;
    auto& p=tree.soldier;
    auto& s=p.soldier;
    auto& g=s.geometry;
    s.slot=2;s.type=14;s.sheet=0x90;s.segment=1;
    g.format=SpriteDrawFormat::Amiga8;g.columns=2;g.rows=28;
    g.spriteX+=5;g.spriteY+=14;
    p.resource.offset=1942;p.resource.layout={g.format,320,256,4};p.resource.generation=1;
    auto treeBytes=std::make_shared<std::vector<uint8_t>>(40*256*4,0);
    // One equal-index write and one transparent pixel in each first byte.
    for(size_t y=0;y<28;++y)
        for(size_t plane:{0u,2u}) (*treeBytes)[plane*40*256+1942+y*40]=0x80;
    p.resource.bytes=treeBytes;
    g.source=p.resource.source();p.draw=PrepareSpriteDraw(g);g.source=nullptr;
    const auto treeKey=SoldierVariantKey(p,colors);
    const auto tx=p.draw.x,ty=p.draw.y;
    const size_t first=size_t(ty)*96+tx;
    const size_t later=size_t(ty+7)*96+tx;
    MissionLayer zero=cover;zero.pixels.writes.clear();zero.pixels.put(later+1,0);
    auto save=cover;save.operation=MissionLayerOperation::Save;
    auto restore=save;restore.operation=MissionLayerOperation::Restore;
    auto afterSave=zero;afterSave.pixels.put(first+1,0);
    env("OPENFODDER_SOLDIER_ORDERED_MANIFEST",path);
    for(const char* density:{"8","12"}){
        env("OPENFODDER_SOLDIER_HD",density);
        const unsigned d=unsigned(std::stoi(density));
        image.scene.layers={body,tree,second,cover,zero,save,afterSave,restore};
        assert(registry.resolve(p,treeKey,d).decision==SoldierArtDecision::Missing);
        clear(renderer);assert(win.TryRenderMissionHD(&image,src,dst)==-1);
        env("OPENFODDER_SOLDIER_ORDERED_HYBRID","1");
        const auto mixed=ComposeOrderedSoldierArt(image.scene,body.destination,d,[&](const PreparedSpriteDraw& q){
            return registry.resolve(q,SoldierVariantKey(q,colors),d,true);});
        assert(mixed.complete() && mixed.replaced==2 && mixed.kept==1);
        assert(!mixed.cells.count(first) && mixed.background.pixels[first]==colors[5]);
        assert(mixed.cells.count(first+1)); // Transparent tree pixel leaves the first HD body.
        assert(mixed.cells.count(later));   // Second HD body overlaps the tree's opaque run.
        assert(!mixed.cells.count(later+1) && mixed.background.pixels[later+1]==0);
        std::vector<uint32_t> expanded(96*64*d*d);
        for(size_t y=0;y<64*d;++y)for(size_t x=0;x<96*d;++x){
            const size_t n=(y/d)*96+x/d;
            const auto cell=mixed.cells.find(n);
            expanded[y*96*d+x]=cell==mixed.cells.end()?mixed.background.pixels[n]:cell->second[(y%d)*d+x%d];
        }
        auto oracle=texture(renderer,expanded,96*d,64*d);
        SDL_FRect full{0,0,96.f*d,64.f*d};
        clear(renderer);assert(SDL_RenderTexture(renderer,oracle,&full,&dst));const auto expected=read(renderer);
        SDL_DestroyTexture(oracle);
        const auto native=RasterizeMissionLayers(image.scene,body.destination);
        assert(SDL_UpdateTexture(image.tex,nullptr,native.pixels.data(),96*4));
        clear(renderer);assert(SDL_RenderTexture(renderer,image.tex,&src,&dst));const auto expectedClassic=read(renderer);
        clear(renderer);callNumber=0;
        assert(win.TryRenderMissionHD(&image,src,dst)==1 && read(renderer)==expected && expected!=expectedClassic);
        const int lastDraw=callNumber;
        clear(renderer);callNumber=0;failAt=lastDraw;
        assert(win.TryRenderMissionHD(&image,src,dst)==1 && read(renderer)==expectedClassic && live==0);
        failAt=0;
        const auto expectRejection=[&](){
            clear(renderer);callNumber=0;
            assert(win.TryRenderMissionHD(&image,src,dst)==-1 && callNumber==0);
        };
        auto& retained=image.scene.layers[1].soldier;
        retained.soldier.type=5;expectRejection();retained=p;
        retained.resource.bytes=std::make_shared<const std::vector<uint8_t>>(1943,0);
        expectRejection();
        bool rejected=false;
        try { RasterizeMissionLayers(image.scene,body.destination); }
        catch(const std::out_of_range&) { rejected=true; }
        assert(rejected);
        retained=p;retained.draw.sourceOffset+=40000;expectRejection();
        retained=p;retained.soldier.generation=0;expectRejection();
        retained=p;
        assert(win.TryRenderMissionHD(&image,src,dst)==1 && read(renderer)==expected);
        env("OPENFODDER_SOLDIER_HD","0");expectRejection();
        env("OPENFODDER_SOLDIER_ORDERED_HYBRID","0");
    }
    assert(SDL_UpdateTexture(image.tex,nullptr,classic.pixels.data(),96*4));
    std::cout<<"PASS hybrid Window: two HD actors, native tree, ordered writes, Save/Restore and complete SDL recovery at 8x/12x\n";
}
env("OPENFODDER_SOLDIER_ORDERED_MANIFEST","");std::remove(path);
std::cout<<"PASS ordered Window: resource/palette identity, multiple bodies, water, occlusion, missing binding and load failure\n";
