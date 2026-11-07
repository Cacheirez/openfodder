// GPL-3.0-or-later. Isolated retained-command HD contract, no SDL/game data.
#ifdef NDEBUG
#undef NDEBUG
#endif
#include "Utils/SoldierArtHDLayers.hpp"
#include "c01_8.hpp"
#include "c01_12.hpp"
#include <cassert>
#include <iostream>
using namespace openfodder;
static MissionLayerDestination destination(size_t w,size_t h,size_t padding=0) {
    std::vector<uint8_t> p(w*h,5); std::vector<uint32_t> b((w+padding)*h,0);
    uint32_t colors[255];for(unsigned i=0;i<255;++i)colors[i]=0xff000000u+i*7919;
    MissionLayerDestination d;
    d.initial={CaptureSurfaceDraw(p.data(),p.size(),colors,w,h,16,16),
        CaptureLayer(b.data(),b.size(),w,h,w+padding),std::make_shared<const PresentationDestination>()};
    d.saved=CaptureLayer(p.data(),p.size(),w,h,w);return d;
}
static SoldierArtHDAsset asset(unsigned d) {
    SoldierArtHDAsset a;a.density=d;
    if(d==1)a.pixels=std::make_shared<const std::vector<uint32_t>>(SoldierArtPixels().begin(),SoldierArtPixels().end());
    if(d==8)a.pixels=std::make_shared<const std::vector<uint32_t>>(SoldierArtPixels8().begin(),SoldierArtPixels8().end());
    if(d==12)a.pixels=std::make_shared<const std::vector<uint32_t>>(SoldierArtPixels12().begin(),SoldierArtPixels12().end());
    return a;
}
static MissionLayer soldier(bool amiga,int shift) {
    MissionLayer l;l.operation=MissionLayerOperation::Soldier;
    auto& p=l.soldier;
    p.resource.bytes=std::make_shared<const std::vector<uint8_t>>(32768,0x51);
    p.resource.offset=amiga?562:2248;p.resource.layout={amiga?SpriteDrawFormat::Amiga8:SpriteDrawFormat::PC,320,32,4};
    auto& s=p.soldier;s.valid=true;s.scene=1;s.generation=2;s.interval=3;s.sheet=7;
    auto& g=s.geometry;g.format=p.resource.layout.format;g.columns=amiga?2:16;g.rows=14;
    g.spriteX=shift;g.spriteY=30+shift;
    auto input=g;input.source=p.resource.source();p.draw=PrepareSpriteDraw(input);
    return l;
}
// Full HD oracle is expanded only in tests, never by the layered producer.
static void checkLayers(const MissionLayerSequence& scene,const PresentationDestinationId& id,
        const SoldierArtHDAsset& a,bool stable=true) {
    const auto full=ComposeSoldierArtHD(scene,id,stable,a);
    const auto layers=ComposeSoldierArtHDLayers(scene,id,stable,a);
    assert(layers.status==full.status && layers.density==full.density);
    assert(layers.background.destination==full.target.destination);
    if(layers.status!=SoldierArtHDStatus::Replaced){
        assert(layers.patch.empty() && layers.background.pixels==full.target.pixels);return;
    }
    assert(layers.logicalX==full.logicalX && layers.logicalY==full.logicalY && layers.scene==full.scene);
    const auto d=layers.density;
    assert(layers.patch.size()==224*d*d);
    for(size_t y=0;y<full.target.height;++y)for(size_t x=0;x<full.target.width;++x){
        uint32_t pixel=layers.background.pixels[(y/d)*layers.background.width+x/d];
        const size_t left=size_t(layers.logicalX)*d,top=size_t(layers.logicalY)*d;
        if(x>=left && x<left+16*d && y>=top && y<top+14*d)
            pixel=layers.patch[(y-top)*16*d+x-left];
        assert(pixel==full.target.pixels[y*full.target.stride+x]);
    }
    const auto denied=ComposeSoldierArtHDLayers(scene,id,stable,a,layers.patch.size()*4-1);
    assert(denied.status==SoldierArtHDStatus::BudgetExceeded && denied.patch.empty());
    assert(denied.background.pixels==RasterizeMissionLayers(scene,id).pixels);
}
static void fallback(const MissionLayerSequence& scene,const PresentationDestinationId& id,
        const SoldierArtHDAsset& a, bool stable=true, size_t budget=64u*1024u*1024u) {
    if(budget==64u*1024u*1024u)checkLayers(scene,id,a,stable);
    auto result=ComposeSoldierArtHD(scene,id,stable,a,budget);
    auto reference=RasterizeMissionLayers(scene,id);
    assert(result.status!=SoldierArtHDStatus::Replaced && result.density==1);
    assert(result.target.destination==id && result.target.width==reference.width &&
        result.target.stride==reference.stride && result.target.pixels==reference.pixels);
}
int main() {
    size_t cases=0;
    for(bool amiga:{false,true})for(int shift:{0,5})for(unsigned d:{1u,8u,12u}) {
        MissionLayerSequence scene;scene.destinations={destination(96,64),destination(96,64)};
        const auto id=scene.destinations[0].initial.destination;
        auto l=soldier(amiga,shift);l.destination=id;
        MissionLayer early;early.destination=id;early.role=MissionLayerRole::Cursor;
        early.pixels.put((32+shift)*96+72+shift,50);scene.layers={early,l};
        auto a=asset(d);checkLayers(scene,id,a);auto hd=ComposeSoldierArtHD(scene,id,true,a);
        assert(hd.status==SoldierArtHDStatus::Replaced && hd.density==d && hd.target.destination==id);
        assert(hd.logicalX==64+shift && hd.logicalY==32+shift && hd.scene==1);
        assert(hd.target.width==96*d && hd.target.height==64*d && hd.target.stride==96*d);
        auto classic=RasterizeMissionLayers(scene,id);
        for(size_t y=0;y<64*d;++y)for(size_t x=0;x<96*d;++x)
            if(x<size_t(hd.logicalX)*d || x>=size_t(hd.logicalX+16)*d ||
               y<size_t(hd.logicalY)*d || y>=size_t(hd.logicalY+14)*d)
                assert(hd.target.pixels[y*96*d+x]==classic.pixels[(y/d)*96+x/d]);
        if(d>1) {
            auto native=ComposeSoldierArt(scene,id,true); bool detail=false;
            for(size_t y=0;y<64*d;++y)for(size_t x=0;x<96*d;++x)
                detail |= hd.target.pixels[y*96*d+x]!=native.target.pixels[(y/d)*96+x/d];
            assert(detail); // Actual HD samples, not an enlarged 16x14 reduction.
        }
        if(d==1)assert(hd.target.pixels==ComposeSoldierArt(scene,id,true).target.pixels);
        // Transparent body must expose ground, not the old soldier; partial alpha
        // is checked against an independent pixel equation at every output pixel.
        for(uint32_t color:{0u,0xff123456u,0x80123456u}) {
            auto solid=a;solid.pixels=std::make_shared<const std::vector<uint32_t>>(224*d*d,color);
            checkLayers(scene,id,solid);auto got=ComposeSoldierArtHD(scene,id,true,solid);auto ground=scene;ground.layers.pop_back();
            auto bg=RasterizeMissionLayers(ground,id);
            for(size_t y=0;y<14*d;++y)for(size_t x=0;x<16*d;++x) {
                size_t ox=size_t(hd.logicalX)*d+x,oy=size_t(hd.logicalY)*d+y;
                uint32_t before=bg.pixels[(oy/d)*96+ox/d],expected=before&0xff000000u;
                for(unsigned s:{0u,8u,16u})expected|=((((color>>s)&255)*(color>>24)+((before>>s)&255)*(255-(color>>24))+127)/255)<<s;
                assert(got.target.pixels[oy*96*d+ox]==expected);
            }
        }
        for(int count:{0,1,5})for(int n=0;n<count;++n)
            {checkLayers(scene,id,a);assert(ComposeSoldierArtHD(scene,id,true,a).target.pixels==hd.target.pixels);}
        assert(RasterizeMissionLayers(scene,id).pixels==classic.pixels);
        fallback(scene,id,a,false);fallback(scene,id,{});auto wrong=a;wrong.density=9;fallback(scene,id,wrong);
        wrong.density=d;wrong.pixels=std::make_shared<const std::vector<uint32_t>>(3,0);fallback(scene,id,wrong);
        fallback(scene,id,a,true,hd.target.pixels.size()*4-1);
        for(int guard=0;guard<11;++guard) {
            auto blocked=scene;auto& p=blocked.layers[1].soldier;
            if(guard==0)++p.soldier.frame;
            if(guard==1)++p.soldier.animation;
            if(guard==2)++p.resource.offset;
            if(guard>=3) {
                MissionLayer occluder;occluder.destination=id;
                if(guard==3)occluder.pixels.put((32+shift)*96+72+shift,5); // same as ground still occludes
                if(guard==4)occluder.pixels.put((32+shift)*96+72+shift,0);
                if(guard==5)occluder.pixels.addBits((32+shift)*96+72+shift,0);
                if(guard==6)occluder.operation=MissionLayerOperation::Save;
                if(guard==7)occluder.operation=MissionLayerOperation::Restore;
                if(guard==8)occluder.operation=MissionLayerOperation::Clear;
                if(guard==9)occluder=l;
                if(guard==10) { // explicit clip in the destination, not a new logical anchor
                    blocked.destinations[0].initial.indexed.skipX=70+shift;
                } else blocked.layers.push_back(occluder);
            }
            fallback(blocked,id,a);++cases;
        }
        // Identical coordinates on another destination never occlude this one.
        auto other=early;other.destination=scene.destinations[1].initial.destination;
        scene.layers.push_back(other);
        {checkLayers(scene,id,a);assert(ComposeSoldierArtHD(scene,id,true,a).target.pixels==hd.target.pixels);}
        fallback(scene,other.destination,a);
        scene.destinations[0]=destination(96,64,3);auto padded=scene.destinations[0].initial.destination;
        for(auto& cmd:scene.layers)if(cmd.destination==id)cmd.destination=padded;
        fallback(scene,padded,a);
    }
    // Bound the largest supported candidate independently of machine RAM.
    MissionLayerSequence large;large.destinations={destination(352,272)};
    auto l=soldier(false,0);l.destination=large.destinations[0].initial.destination;large.layers={l};
    checkLayers(large,l.destination,asset(12));
    auto hd=ComposeSoldierArtHD(large,l.destination,true,asset(12));
    assert(hd.status==SoldierArtHDStatus::Replaced && hd.target.pixels.size()*4==55148544);
    std::cout<<"PASS full/layered pixel equality; HD C01: "<<cases<<" guards; PC/Amiga 1x/8x/12x, native oracle, alpha, order, destinations, pitch, budget, retained 0/1/5\n";
    return 0;
}
