// Actual ordered Window route, exact independent CPU oracle and native colours.
// The catalogue still verifies resources/raster; only the immutable HD RGB is transferred.
assert(!nativeOnly);image.scene.layers.resize(2);image.adjusting=true;image.paletteTarget=colors;
size_t fadeCases=0;
for(bool fadeOut:{false,true})for(unsigned level:(fadeOut?std::vector<unsigned>{3,2,1}:std::vector<unsigned>{1,2,3,4})){
    auto current=colors;
    for(auto& color:current){uint32_t value=color&0xff000000u;
        for(unsigned shift:{0u,8u,16u})value|=((((color>>shift)&255)*level/4)<<shift);color=value;}
    image.scene.destinations[0].initial.indexed.colors=current;
    image.paletteTarget=fadeOut?std::array<uint32_t,255>{}:colors;
    for(unsigned density:{8u,12u}){
        MissionPaletteArt grading;assert(grading.transfer.build(colors,current));
        auto expectedFrame=ComposeOrderedSoldierArt(image.scene,body.destination,density,[&](const PreparedSpriteDraw& draw){
            auto art=registry.resolve(draw,SoldierVariantKey(draw,current),density,true,96,96*64);
            return grading.apply(art);
        });
        assert(expectedFrame.complete());
        std::vector<uint32_t> pixels(96*64*density*density);
        for(size_t y=0;y<64*density;++y)for(size_t x=0;x<96*density;++x){
            const size_t at=(y/density)*96+x/density;const auto cell=expectedFrame.cells.find(at);
            pixels[y*96*density+x]=cell==expectedFrame.cells.end()?expectedFrame.background.pixels[at]:cell->second[(y%density)*density+x%density];
        }
        auto oracle=texture(renderer,pixels,96*density,64*density);SDL_FRect full{0,0,96.f*density,64.f*density};clear(renderer);
        assert(SDL_RenderTexture(renderer,oracle,&full,&dst));const auto expected=read(renderer);SDL_DestroyTexture(oracle);
        const auto native=RasterizeMissionLayers(image.scene,body.destination);
        assert(SDL_UpdateTexture(image.tex,nullptr,native.pixels.data(),96*4));clear(renderer);
        env("OPENFODDER_SOLDIER_HD",std::to_string(density).c_str());callNumber=0;
        assert(win.TryRenderMissionHD(&image,src,dst)==1 && read(renderer)==expected);
        if(level==1){
            const auto lastCall=callNumber;clear(renderer);assert(SDL_RenderTexture(renderer,image.tex,&src,&dst));const auto classic=read(renderer);
            clear(renderer);callNumber=0;failAt=lastCall;
            assert(win.TryRenderMissionHD(&image,src,dst)==1 && read(renderer)==classic && live==0);failAt=0;
        }
        ++fadeCases;
    }
}
// No reference from a previous scene may qualify an unrelated fade-out.
const auto originalDestination=image.scene.destinations[0].initial.destination;
image.scene.destinations[0].initial.destination=std::make_shared<const PresentationDestination>();
assert(win.TryRenderMissionHD(&image,src,dst)==-1);
image.scene.destinations[0].initial.destination=originalDestination;
++fodder.mPresentationScene;assert(win.TryRenderMissionHD(&image,src,dst)==-1);--fodder.mPresentationScene;
// A component brighter than the reference cannot be a black-based native fade.
image.paletteTarget=colors;auto invalid=colors;bool changed=false;
for(auto& c:invalid)if((c&255)<255){c=(c&0xffffff00u)|((c&255)+1);changed=true;break;}
assert(changed);image.scene.destinations[0].initial.indexed.colors=invalid;
assert(win.TryRenderMissionHD(&image,src,dst)==-1);
image.scene.destinations[0].initial.indexed.colors={};assert(win.TryRenderMissionHD(&image,src,dst)==-1);
image.scene.destinations[0].initial.indexed.colors=colors;image.adjusting=false;
std::cout<<"PASS palette Window: "<<fadeCases<<" ordered fade-in/out cases; exact SDL oracle, current native background, scene isolation and invalid/black recovery\n";
