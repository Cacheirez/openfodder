// GPL-3.0-or-later. Independent tiny scenes; no generated/commercial artwork.
#ifdef NDEBUG
#undef NDEBUG
#endif
#include "Utils/OrderedSoldierArt.hpp"
#include <cassert>
#include <iostream>
using namespace openfodder;
static MissionLayerDestination surface(){
    MissionLayerDestination s;std::vector<uint8_t> pixels(96*64,5);
    std::vector<uint32_t> backing(96*64,0);uint32_t colors[255]{};
    colors[5]=0xff112233;colors[1]=0xff445566;colors[7]=0xff778899;
    s.initial={CaptureSurfaceDraw(pixels.data(),pixels.size(),colors,96,64,0,0),
        CaptureLayer(backing.data(),backing.size(),96,64,96),std::make_shared<const PresentationDestination>()};
    s.saved=CaptureLayer(pixels.data(),pixels.size(),96,64,96);return s;
}
static MissionLayer body(bool amiga,PresentationDestinationId id,int x,int y,int slot=0){
    MissionLayer l;l.destination=id;l.operation=MissionLayerOperation::Soldier;
    auto& p=l.soldier;p.resource.bytes=std::make_shared<const std::vector<uint8_t>>(32768,0x11);
    p.resource.layout={amiga?SpriteDrawFormat::Amiga8:SpriteDrawFormat::PC,320,32,4};
    auto& s=p.soldier;s.valid=true;s.scene=1;s.generation=2;s.interval=3;s.slot=slot;
    auto& g=s.geometry;g.format=p.resource.layout.format;g.columns=amiga?2:16;g.rows=14;
    g.xBias=0;g.spriteX=x;g.spriteY=y+14-16;
    auto input=g;input.source=p.resource.source();p.draw=PrepareSpriteDraw(input);return l;
}
static void prepare(MissionLayer& l){auto g=l.soldier.soldier.geometry;g.source=l.soldier.resource.source();l.soldier.draw=PrepareSpriteDraw(g);}
static uint32_t at(const OrderedSoldierFrame& f,size_t x,size_t y,size_t sx=0,size_t sy=0){
    size_t n=y*f.background.width+x;auto c=f.cells.find(n);
    return c==f.cells.end()?f.background.pixels[n]:c->second[sy*f.density+sx];
}
int main(){
 size_t cases=0;
 for(bool amiga:{false,true})for(unsigned density:{1u,8u,12u}){
    MissionLayerSequence scene;scene.destinations={surface(),surface()};auto id=scene.destinations[0].initial.destination;
    auto a=body(amiga,id,20,20),b=body(amiga,id,24,22,1);
    b.soldier.soldier.type=5;
    auto resolver=[&](const PreparedSpriteDraw& p){
        OrderedSoldierAsset a;a.decision=SoldierArtDecision::Replace;a.width=16;a.height=14;a.density=density;
        a.pixels=std::make_shared<const std::vector<uint32_t>>(224*density*density,
            p.soldier.slot?0xff00ff00:0xffff0000);return a;};
    auto compose=[&](){return ComposeOrderedSoldierArt(scene,id,density,resolver);};
    scene.layers={a,b};auto classic=RasterizeMissionLayers(scene,id);auto f=compose();
    assert(f.complete()&&f.replaced==2&&f.observations.size()==2);
    assert(at(f,20,20)==0xffff0000&&at(f,24,22)==0xff00ff00);
    assert(at(f,19,20)==0xff112233&&RasterizeMissionLayers(scene,id).pixels==classic.pixels);
    scene.layers={b,a};assert(at(compose(),24,22)==0xffff0000);
    scene.layers={a,a};assert(compose().replaced==2); // repeated actor obeys command order
    for(bool bits:{false,true})for(uint8_t value:{uint8_t(0),uint8_t(5),uint8_t(7)}){
        MissionLayer late;late.destination=id;late.pixels.writes.push_back({20*96+20,value,bits});
        scene.layers={a,late};f=compose();
        uint8_t index=bits?uint8_t(5|value):value;
        assert(at(f,20,20)==(index?scene.destinations[0].initial.indexed.colors[index]:0));
        assert(at(f,21,20)==0xffff0000);++cases;
    }
    MissionLayer save,restore,clear;save.destination=restore.destination=clear.destination=id;
    save.operation=MissionLayerOperation::Save;restore.operation=MissionLayerOperation::Restore;clear.operation=MissionLayerOperation::Clear;
    scene.layers={a,save,b,restore};f=compose();assert(at(f,24,22)==0xffff0000&&at(f,39,22)==0xff112233);
    scene.layers={a,restore};assert(compose().cells.empty());
    scene.layers={a,save,clear,restore};f=compose();assert(f.cells.empty()&&at(f,20,20)==0);
    auto other=b;other.destination=scene.destinations[1].initial.destination;
    scene.layers={a,other};assert(compose().replaced==1&&at(compose(),24,22)==0xffff0000);
    // Water removes bottom rows while the engine shifts its anchor. Top clipping
    // must sample the corresponding SOURCE row, not stretch the remaining body.
    auto water=a;water.soldier.soldier.geometry.rowsToSkip=5;prepare(water);
    scene.layers={water};f=compose();assert(at(f,20,24)==0xff112233&&at(f,20,25)==0xffff0000&&at(f,20,34)==0xff112233);
    auto top=body(amiga,id,20,-3);scene.layers={top};
    auto gradient=resolver(top.soldier);auto pixels=std::make_shared<std::vector<uint32_t>>(224*density*density);
    for(size_t y=0;y<14*density;++y)for(size_t x=0;x<16*density;++x)(*pixels)[y*16*density+x]=0xff000000u+uint32_t(y*256+x);
    gradient.pixels=pixels;f=ComposeOrderedSoldierArt(scene,id,density,[&](const PreparedSpriteDraw&){return gradient;});
    assert(at(f,20,0)==(*pixels)[3*density*16*density]);assert(at(f,20,11)==0xff112233);
    scene.layers={a};scene.destinations[0].initial.indexed.skipX=24;
    f=compose();assert(at(f,23,20)==0&&at(f,24,20)==0xffff0000);scene.destinations[0].initial.indexed.skipX=0;
    // Engine-selected bottom/left/right clipping, preserving its rounded columns.
    auto bottom=body(amiga,id,20,60);bottom.soldier.soldier.geometry.viewHeight=32;prepare(bottom);
    scene.layers={bottom};f=compose();assert(at(f,20,59)==0xff112233&&at(f,20,63)==0xffff0000);
    if(!amiga){
        auto left=body(false,id,-3,20);scene.layers={left};f=compose();assert(at(f,0,20)==0xffff0000&&at(f,12,20)==0xff112233);
        auto right=body(false,id,84,20);right.soldier.soldier.geometry.viewWidth=64;prepare(right);
        scene.layers={right};f=compose();assert(at(f,83,20)==0xff112233&&at(f,95,20)==0xffff0000);
    }
    scene.layers={a};
    // Transparent margins remove the old body, partial alpha blends once.
    auto transparent=resolver(a.soldier);transparent.pixels=std::make_shared<const std::vector<uint32_t>>(224*density*density,0);
    f=ComposeOrderedSoldierArt(scene,id,density,[&](const PreparedSpriteDraw&){return transparent;});assert(at(f,20,20)==0xff112233);
    auto half=transparent;half.pixels=std::make_shared<const std::vector<uint32_t>>(224*density*density,0x80ff0000);
    f=ComposeOrderedSoldierArt(scene,id,density,[&](const PreparedSpriteDraw&){return half;});assert(at(f,20,20)==0xff881119);
    auto missing=OrderedSoldierAsset{};
    scene.layers={a,b};f=ComposeOrderedSoldierArt(scene,id,density,[&](const PreparedSpriteDraw& p){return p.soldier.slot?missing:resolver(p);});
    assert(!f.complete()&&f.replaced==1&&f.missing==1); // publishing one key cannot pass coverage
    missing.decision=SoldierArtDecision::KeepClassic;f=ComposeOrderedSoldierArt(scene,id,density,[&](const PreparedSpriteDraw&){return missing;});
    assert(!f.complete()&&f.kept==2&&f.background.pixels==RasterizeMissionLayers(scene,id).pixels);
    bool denied=false;try{ComposeOrderedSoldierArt(scene,id,density,resolver,0);}catch(const std::length_error&){denied=true;}assert(denied);
    // Native terrain and HUD written after a modern body must cover it.
    MissionLayer terrain;terrain.destination=id;terrain.operation=MissionLayerOperation::Terrain;
    terrain.terrain.base=std::make_shared<const std::vector<uint8_t>>(5120,5);terrain.terrain.tiles={{0,20,20,0,0}};
    scene.layers={a,terrain};f=compose();assert(at(f,20,20)==0xff112233&&f.cells.empty());
    terrain.terrain.format=TerrainFormat::Amiga;terrain.terrain.tiles.clear();scene.layers={a,terrain};assert(compose().cells.empty());
    MissionLayer sidebar;sidebar.destination=id;sidebar.operation=MissionLayerOperation::Sidebar;
    sidebar.sidebar={std::make_shared<const std::vector<uint8_t>>(48,7),20*96,96,1};
    scene.layers={a,sidebar};assert(at(compose(),20,20)==0xff778899&&at(compose(),20,21)==0xffff0000);
    cases+=17+(amiga?0:2);
 }
 std::cout<<"PASS ordered compositor: "<<cases<<" scenarios; PC/Amiga 1x/8x/12x, multiple/repeated bodies, alpha, water/top crop, destinations, same-color/zero/OR, Save/Restore/Clear, terrain/HUD, missing coverage, budget\n";
}
