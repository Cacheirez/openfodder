// GPL-3.0-or-later. Independent destination/order oracle and retained kernels.
#include "Utils/MissionLayers.hpp"
#include <cassert>
#include <iostream>
using namespace openfodder;

static MissionLayerDestination destination(size_t width, size_t height, size_t padding, int seed) {
    std::vector<uint8_t> pixels(width*height), saved(width*height);
    std::vector<uint32_t> backing((width+padding)*height);
    uint32_t colors[255];
    for(size_t i=0;i<pixels.size();++i) { pixels[i]=uint8_t((i+seed)%255); saved[i]=uint8_t((i*3+seed)%255); }
    for(size_t i=0;i<backing.size();++i)backing[i]=uint32_t(i+seed*65536);
    for(size_t i=0;i<255;++i)colors[i]=uint32_t(0xFF000000|((i+seed)*17237));
    MissionLayerDestination d;
    d.initial={CaptureSurfaceDraw(pixels.data(),pixels.size(),colors,width,height,16,16),
        CaptureLayer(backing.data(),backing.size(),width,height,width+padding),
        std::make_shared<const PresentationDestination>()};
    d.saved=CaptureLayer(saved.data(),saved.size(),width,height,width);
    return d;
}
static void checkPixels(const PresentationTarget& a,const PresentationTarget& b) {
    assert(a.destination==b.destination && a.width==b.width && a.height==b.height && a.stride==b.stride);
    assert(a.pixels==b.pixels);
}
int main() {
    size_t cases=0, retained=0;
    for(auto format:{TerrainFormat::PC,TerrainFormat::Amiga})
    for(size_t width:{size_t(80),size_t(112)})
    for(size_t padding:{size_t(0),size_t(3)})
    for(bool restoreFirst:{false,true})
    for(bool resume:{false,true})
    for(bool clearBefore:{false,true})
    for(int presentations:{0,1,5}) {
        const size_t height=64;
        MissionLayerSequence scene;
        scene.destinations={destination(width,height,padding,1),destination(width,height,padding,9)};
        auto visible=scene.destinations[0].initial.destination;
        auto secondary=scene.destinations[1].initial.destination;
        std::vector<std::vector<uint8_t>> expected, saved;
        std::vector<std::vector<uint32_t>> backing;
        for(auto& d:scene.destinations){expected.push_back(*d.initial.indexed.indices);saved.push_back(*d.saved.pixels);}
        for(auto& d:scene.destinations)backing.push_back(*d.initial.backing.pixels);
        auto emit=[&](MissionLayer layer,size_t slot){
            layer.destination=scene.destinations[slot].initial.destination;
            scene.layers.push_back(std::move(layer));
        };
        auto state=[&](MissionLayerOperation op,size_t slot){
            MissionLayer layer;layer.operation=op;emit(layer,slot);
            if(op==MissionLayerOperation::Save)saved[slot]=expected[slot];
            else expected[slot]=saved[slot];
        };
        auto pixel=[&](MissionLayerRole role,size_t slot,size_t offset,uint8_t value,bool bits=false){
            MissionLayer layer;layer.role=role;
            if(bits)layer.pixels.addBits(offset,value);else layer.pixels.put(offset,value);
            emit(layer,slot);
            if(bits)expected[slot][offset]|=value;else expected[slot][offset]=value;
        };
        if(restoreFirst)state(MissionLayerOperation::Restore,0);
        if(clearBefore){
            MissionLayer clear;clear.operation=MissionLayerOperation::Clear;clear.clearIndex=11;
            emit(clear,0);std::fill(expected[0].begin(),expected[0].end(),11);
            std::fill(saved[0].begin(),saved[0].end(),11);
            for(size_t y=0;y<height;++y)for(size_t x=0;x<width;++x)backing[0][y*(width+padding)+x]=0;
            state(MissionLayerOperation::Restore,0);
        }
        // Early cursor can be covered by terrain. Never reorder by role.
        pixel(MissionLayerRole::Cursor,0,17*width+17,0xFE);
        std::vector<uint8_t> base(format==TerrainFormat::PC?320*256:512*128,0x5A),sub(320*256,0xA5);
        TerrainDraw terrain;terrain.format=format;
        terrain.base=std::make_shared<const std::vector<uint8_t>>(base);
        terrain.sub=std::make_shared<const std::vector<uint8_t>>(sub);
        terrain.tiles={{1,16,16,0,0},{241,32,16,0,0}};
        MissionLayer land;land.role=MissionLayerRole::Terrain;
        land.operation=MissionLayerOperation::Terrain;land.terrain=terrain;emit(land,0);
        RasterizeTerrain(terrain,expected[0].data(),width,expected[0].size());
        state(MissionLayerOperation::Save,0);
        // An actual decoded sprite retains opaque writes equal to terrain.
        std::vector<uint8_t> resource(160*32,0x55),rowPalette(height,0x10);
        SpriteDrawState draw;draw.source=resource.data();draw.x=16;draw.y=16;draw.columns=8;draw.rows=4;
        SpriteRasterLayout layout;layout.format=SpriteDrawFormat::PC;
        MissionLayer sprite;sprite.role=MissionLayerRole::Sprite;
        sprite.pixels=CaptureSprite8Producer(draw,layout,width,rowPalette.data());emit(sprite,0);
        RasterizeSprite8(draw,layout,{expected[0].data(),width},rowPalette.data());
        // Same-sized mSurfaceFinal-like destination stays separate.
        pixel(MissionLayerRole::Sprite,1,17*width+17,199);
        state(MissionLayerOperation::Save,1);
        pixel(MissionLayerRole::Sprite,1,17*width+17,77);
        state(MissionLayerOperation::Restore,1);
        std::vector<uint8_t> sidebar(48*height,37);
        MissionLayer hud;hud.role=MissionLayerRole::Sidebar;hud.operation=MissionLayerOperation::Sidebar;
        hud.sidebar=CaptureSidebar(sidebar.data(),width,height,0,false);emit(hud,0);
        RasterizeSidebar(hud.sidebar,expected[0].data());
        // Explicit zero and OR are operations, not transparency inferred from diffs.
        pixel(MissionLayerRole::Cursor,0,20*width+70,0);
        pixel(MissionLayerRole::Cursor,0,20*width+70,4,true);
        pixel(MissionLayerRole::Cursor,0,20*width+70,8,true);
        if(resume){state(MissionLayerOperation::Restore,0);pixel(MissionLayerRole::Cursor,0,18*width+18,99);}
        std::fill(resource.begin(),resource.end(),0);resource.clear();resource.shrink_to_fit();
        rowPalette.clear();sidebar.clear();base.clear();sub.clear();
        terrain={};land={};hud={};sprite={};
        // A late fade changes the effective palette without rebuilding layers.
        for(auto& color:scene.destinations[0].initial.indexed.colors)color^=0x00010101;
        std::vector<PresentationTarget> oracle;
        for(size_t i=0;i<2;++i){
            auto source=scene.destinations[i].initial;
            source.backing.pixels=std::make_shared<const std::vector<uint32_t>>(backing[i]);
            source.indexed.indices=std::make_shared<const std::vector<uint8_t>>(expected[i]);
            oracle.push_back(RasterizePresentationSurface(source));
        }
        for(int n=0;n<presentations;++n){
            checkPixels(RasterizeMissionLayers(scene,visible),oracle[0]);
            checkPixels(RasterizeMissionLayers(scene,secondary),oracle[1]);
        }
        // Retain across a pause conversion and replacement of both destinations.
        const auto captured=scene;
        scene.destinations.clear();scene.layers.clear();
        const auto result=ComposeMissionLayers(captured);
        for(size_t i=0;i<2;++i){
            assert(*result.surfaces[i].indexed.indices==expected[i]);
            assert(*result.saved[i].pixels==saved[i]);
            assert(*result.surfaces[i].backing.pixels==backing[i]);
            checkPixels(RasterizeMissionLayers(captured,captured.destinations[i].initial.destination),oracle[i]);
            ++retained;
        }
        PausePresentation pause{result.surfaces[0],result.surfaces[1]};
        const auto paused=RasterizePausePresentation(pause);
        auto pauseExpected=oracle[0];
        for(size_t i=0;i<pauseExpected.pixels.size();++i)if(oracle[1].pixels[i])pauseExpected.pixels[i]=oracle[1].pixels[i];
        checkPixels(paused.background,pauseExpected);
        checkPixels(RasterizeMissionLayers(captured,visible),oracle[0]);
        auto output=RasterizeMissionLayers(captured,visible);output.pixels[0]^=123;
        checkPixels(RasterizeMissionLayers(captured,visible),oracle[0]);
        ++cases;
    }
    // Order and equal-colour coverage are observable, even after moving a layer
    // between two terrain commands. No image-difference mask is used.
    MissionLayerSequence scene;scene.destinations={destination(80,64,0,3)};
    auto id=scene.destinations[0].initial.destination;
    MissionLayer a;a.destination=id;a.pixels.put(0,42);
    MissionLayer b=a;b.pixels.writes[0].value=7;
    scene.layers={a,b,a};assert((*ComposeMissionLayers(scene).surfaces[0].indexed.indices)[0]==42);
    scene.layers={a,a,b};assert((*ComposeMissionLayers(scene).surfaces[0].indexed.indices)[0]==7);
    auto reject=[](const MissionLayerSequence& s){bool rejected=false;try{ComposeMissionLayers(s);}catch(const std::invalid_argument&){rejected=true;}assert(rejected);};
    scene.layers.back().destination=std::make_shared<const PresentationDestination>();reject(scene);
    scene.layers.clear();scene.destinations.push_back(scene.destinations[0]);reject(scene);
    scene.destinations.pop_back();scene.destinations[0].saved.stride++;reject(scene);
    scene.destinations[0].saved.stride--;scene.destinations[0].initial.destination.reset();reject(scene);
    bool missing=false;
    try{RasterizeMissionLayers(MissionLayerSequence{},id);}catch(const std::invalid_argument&){missing=true;}
    assert(missing);
    std::cout<<"PASS: "<<cases<<" ordered multi-destination mission layer schedules, "<<retained
             <<" retained outputs; 0/1/5, terrain/sprites/HUD/cursor, Save/Restore, pause composition, resource release, exact writes and rejection contracts\n";
}
