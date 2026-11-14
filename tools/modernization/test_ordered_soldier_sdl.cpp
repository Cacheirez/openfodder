// GPL-3.0-or-later. Ordered compositor through real SDL, with failure injection.
#include <SDL3/SDL.h>
#define main ordered_cpu_contract_main
#include "test_ordered_soldier_art.cpp"
#undef main
static int calls=0,failAt=0,secondFail=0,live=0;
static bool fail(){return ++calls==failAt || calls==secondFail;}
static SDL_Texture* create(SDL_Renderer*r,SDL_PixelFormat f,SDL_TextureAccess a,int w,int h){
    if(fail())return nullptr;auto t=SDL_CreateTexture(r,f,a,w,h);if(t)++live;return t;
}
static void destroy(SDL_Texture*t){if(t)--live;SDL_DestroyTexture(t);}
static bool blend(SDL_Texture*t,SDL_BlendMode b){return !fail()&&SDL_SetTextureBlendMode(t,b);}
static bool scale(SDL_Texture*t,SDL_ScaleMode m){return !fail()&&SDL_SetTextureScaleMode(t,m);}
static bool update(SDL_Texture*t,const SDL_Rect*r,const void*p,int pitch){return !fail()&&SDL_UpdateTexture(t,r,p,pitch);}
static bool render(SDL_Renderer*r,SDL_Texture*t,const SDL_FRect*s,const SDL_FRect*d){return !fail()&&SDL_RenderTexture(r,t,s,d);}
#define SDL_CreateTexture create
#define SDL_DestroyTexture destroy
#define SDL_SetTextureBlendMode blend
#define SDL_SetTextureScaleMode scale
#define SDL_UpdateTexture update
#define SDL_RenderTexture render
#include "Utils/OrderedSoldierSDL.hpp"
#undef SDL_CreateTexture
#undef SDL_DestroyTexture
#undef SDL_SetTextureBlendMode
#undef SDL_SetTextureScaleMode
#undef SDL_UpdateTexture
#undef SDL_RenderTexture
static SDL_Texture* texture(SDL_Renderer*r,const std::vector<uint32_t>&p,int w,int h){
    auto t=SDL_CreateTexture(r,SDL_PIXELFORMAT_XRGB8888,SDL_TEXTUREACCESS_STREAMING,w,h);assert(t);
    assert(SDL_SetTextureBlendMode(t,SDL_BLENDMODE_NONE));assert(SDL_SetTextureScaleMode(t,SDL_SCALEMODE_NEAREST));
    assert(SDL_UpdateTexture(t,nullptr,p.data(),w*4));return t;
}
static std::vector<uint32_t> read(SDL_Renderer*r){
    auto s=SDL_RenderReadPixels(r,nullptr);assert(s);auto c=SDL_ConvertSurface(s,SDL_PIXELFORMAT_XRGB8888);assert(c);
    std::vector<uint32_t> out;
    for(int y=0;y<c->h;++y)for(int x=0;x<c->w;++x)out.push_back(((uint32_t*)((char*)c->pixels+y*c->pitch))[x]&0xffffffu);
    SDL_DestroySurface(c);SDL_DestroySurface(s);return out;
}
int main(){
 size_t cases=0;
 for(bool amiga:{false,true})for(unsigned d:{8u,12u}){
    MissionLayerSequence scene;scene.destinations={surface()};const auto id=scene.destinations[0].initial.destination;
    auto a=body(amiga,id,20,20),b=body(amiga,id,24,22,1);
    a.soldier.soldier.geometry.rowsToSkip=3;prepare(a);
    MissionLayer cover;cover.destination=id;
    for(int y=25;y<28;++y)for(int x=25;x<28;++x)cover.pixels.writes.push_back({y*96+x,5,false});
    scene.layers={a,b,cover};
    auto frame=ComposeOrderedSoldierArt(scene,id,d,[&](const PreparedSpriteDraw& p){
        OrderedSoldierAsset art;art.decision=SoldierArtDecision::Replace;art.width=16;art.height=14;art.density=d;
        auto pixels=std::make_shared<std::vector<uint32_t>>(224*d*d);
        for(size_t y=0;y<14*d;++y)for(size_t x=0;x<16*d;++x)
            (*pixels)[y*16*d+x]=0xff000000u|uint32_t((x*3)%256)<<16|uint32_t((y*5)%256)<<8|uint32_t(p.soldier.slot*255);
        art.pixels=pixels;return art;
    });
    auto classicPixels=RasterizeMissionLayers(scene,id).pixels;
    auto output=SDL_CreateSurface(240,180,SDL_PIXELFORMAT_XRGB8888);assert(output);
    auto r=SDL_CreateSoftwareRenderer(output);assert(r);auto classic=texture(r,classicPixels,96,64);
    auto clear=[&](){assert(SDL_SetRenderDrawColor(r,0,0,0,255));assert(SDL_RenderClear(r));};
    std::vector<uint32_t> expanded(96*64*d*d);
    for(size_t y=0;y<64*d;++y)for(size_t x=0;x<96*d;++x)expanded[y*96*d+x]=at(frame,x/d,y/d,x%d,y%d);
    auto oracle=texture(r,expanded,96*d,64*d);
    // Crops through both bodies and occluder. Integer mapping permits exact oracle.
    SDL_FRect src{22,24,60,40},dst{9,11,120,80},hd{22.f*d,24.f*d,60.f*d,40.f*d};
    clear();assert(SDL_RenderTexture(r,classic,&src,&dst));auto expectedClassic=read(r);
    clear();assert(SDL_RenderTexture(r,oracle,&hd,&dst));auto expected=read(r);
    clear();calls=failAt=0;bool replaced=false;
    assert(RenderOrderedSoldierHD(r,frame,classic,src,dst,replaced)&&replaced&&live==0);
    assert(read(r)==expected);const int successCalls=calls;
    // Every upload/configuration/draw operation can fail. No partial HD survives.
    for(int fault=1;fault<=successCalls;++fault){
        clear();calls=0;failAt=fault;
        assert(RenderOrderedSoldierHD(r,frame,classic,src,dst,replaced)&&!replaced&&live==0);
        assert(read(r)==expectedClassic);++cases;
    }
    // Classic blending restored even after multiple modern strips were drawn.
    assert(SDL_SetTextureBlendMode(classic,SDL_BLENDMODE_BLEND));
    clear();calls=0;failAt=successCalls;
    assert(RenderOrderedSoldierHD(r,frame,classic,src,dst,replaced)&&!replaced);
    SDL_BlendMode saved;assert(SDL_GetTextureBlendMode(classic,&saved)&&saved==SDL_BLENDMODE_BLEND);
    assert(read(r)==expectedClassic);
    // Failure of recovery itself is not reported as a successful presentation.
    clear();calls=0;failAt=successCalls;secondFail=successCalls+2;
    assert(!RenderOrderedSoldierHD(r,frame,classic,src,dst,replaced)&&!replaced&&live==0);
    secondFail=failAt=0;assert(SDL_SetTextureBlendMode(classic,SDL_BLENDMODE_NONE));
    auto missing=frame;missing.missing=1;
    clear();assert(RenderOrderedSoldierHD(r,missing,classic,src,dst,replaced)&&!replaced&&read(r)==expectedClassic);
    auto malformed=frame;malformed.cells.begin()->second.clear();
    clear();assert(RenderOrderedSoldierHD(r,malformed,classic,src,dst,replaced)&&!replaced&&read(r)==expectedClassic);
    // Re-entry uses only the current interval; no texture or prior patch survives.
    clear();assert(RenderOrderedSoldierHD(r,frame,classic,src,dst,replaced)&&replaced&&read(r)==expected);
    // Fractional scale: uniform red cells expose cracks in the row-strip borders.
    auto solid=frame;for(auto& cell:solid.cells)std::fill(cell.second.begin(),cell.second.end(),0xffff0000u);
    SDL_FRect fractional{9,11,173,117};
    clear();assert(RenderOrderedSoldierHD(r,solid,classic,src,fractional,replaced)&&replaced);
    auto actual=read(r);
    for(int y=13;y<35;++y)for(int x=17;x<45;++x){
        // Check strictly inside a contiguous body region, away from the occluder.
        const float lx=src.x+(x+.5f-fractional.x)*src.w/fractional.w;
        const float ly=src.y+(y+.5f-fractional.y)*src.h/fractional.h;
        if(lx>29&&lx<38&&ly>24&&ly<32)assert(actual[y*240+x]==0xff0000u);
    }
    SDL_DestroyTexture(oracle);SDL_DestroyTexture(classic);SDL_DestroyRenderer(r);SDL_DestroySurface(output);cases+=7;
 }
 std::cout<<"PASS ordered SDL: "<<cases<<" failure/crop/coverage/re-entry cases, PC/Amiga at 8x/12x\n";
}
