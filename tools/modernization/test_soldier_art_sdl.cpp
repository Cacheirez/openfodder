// GPL-3.0-or-later. Real SDL software raster + injected SDL call failures.
#include <SDL3/SDL.h>
#define main isolated_hd_contract_main
#include "test_soldier_art_hd.cpp"
#undef main
static int callNumber=0,failAt=0,secondFail=0,live=0;
static bool fail(){++callNumber;return callNumber==failAt||callNumber==secondFail;}
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
#include "Utils/SoldierArtSDL.hpp"
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
    auto s=SDL_RenderReadPixels(r,nullptr);assert(s);auto x=SDL_ConvertSurface(s,SDL_PIXELFORMAT_XRGB8888);assert(x);
    std::vector<uint32_t> pixels;for(int y=0;y<x->h;++y){auto row=(uint32_t*)((char*)x->pixels+y*x->pitch);for(int i=0;i<x->w;++i)pixels.push_back(row[i]&0xffffffu);}
    SDL_DestroySurface(x);SDL_DestroySurface(s);return pixels;
}
static void clear(SDL_Renderer*r){assert(SDL_SetRenderDrawColor(r,0,0,0,255));assert(SDL_RenderClear(r));}
#ifndef OPENFODDER_HD_WINDOW_FIXTURE
int main(){
    size_t cases=0;
    for(bool amiga:{false,true})for(unsigned d:{8u,12u})for(auto size:{std::pair<int,int>{192,128},{1001,777},{384,216},{640,480}}){
        MissionLayerSequence scene;scene.destinations={destination(96,64)};auto id=scene.destinations[0].initial.destination;
        auto pattern=std::make_shared<std::vector<uint8_t>>(*scene.destinations[0].initial.indexed.indices);
        for(size_t i=0;i<pattern->size();++i)(*pattern)[i]=uint8_t(1+(i*37)%254);
        scene.destinations[0].initial.indexed.indices=pattern;
        auto body=soldier(amiga,0);body.destination=id;scene.layers={body};
        auto frame=ComposeSoldierArtHDLayers(scene,id,true,asset(d));auto full=ComposeSoldierArtHD(scene,id,true,asset(d));
        auto old=RasterizeMissionLayers(scene,id);
        auto surface=SDL_CreateSurface(size.first,size.second,SDL_PIXELFORMAT_XRGB8888);assert(surface);
        auto r=SDL_CreateSoftwareRenderer(surface);assert(r);
        auto classic=texture(r,old.pixels,96,64);auto oracle=texture(r,full.target.pixels,96*d,64*d);
        SDL_FRect src{16,16,80,48},dst{7,9,float(size.first-14),float(size.second-18)},hs{16.f*d,16.f*d,80.f*d,48.f*d};
        if(size.first==192)dst={7,9,160,96}; // exact integer logical scale
        clear(r);assert(SDL_RenderTexture(r,classic,&src,&dst));auto classicPixels=read(r);
        clear(r);assert(SDL_RenderTexture(r,oracle,&hs,&dst));auto expected=read(r);
        clear(r);callNumber=0;failAt=0;bool replaced=false;
        assert(RenderSoldierHD(r,frame,classic,src,dst,replaced)&&replaced&&live==0);
        auto actual=read(r);
        if(size.first==192)assert(actual==expected);
        else {
            // SDL samples independently scaled textures at fractional ratios.
            // Outside the body, preserve the CLASSIC native SDL draw exactly.
            // Expanding the full canvas first changes fractional sampling even in terrain.
            SDL_FRect bodyRect;assert(SoldierHDRect(frame,src,dst,bodyRect));
            size_t differences=0;
            for(int y=0;y<size.second;++y)for(int x=0;x<size.first;++x)
                {
                    const bool inside=x>=std::floor(bodyRect.x)&&x<std::ceil(bodyRect.x+bodyRect.w)&&
                        y>=std::floor(bodyRect.y)&&y<std::ceil(bodyRect.y+bodyRect.h);
                    if(!inside)assert(actual[y*size.first+x]==classicPixels[y*size.first+x]);
                    differences+=actual[y*size.first+x]!=expected[y*size.first+x];
                }
            std::cout<<"fractional sampling "<<size.first<<"x"<<size.second<<" d="<<d<<" expanded-oracle differences="<<differences<<"\n";
        }
        for(int fault=1;fault<=10;++fault){
            clear(r);callNumber=0;failAt=fault;replaced=true;
            assert(RenderSoldierHD(r,frame,classic,src,dst,replaced)&&!replaced&&live==0);
            assert(read(r)==classicPixels);SDL_BlendMode b;assert(SDL_GetTextureBlendMode(classic,&b)&&b==SDL_BLENDMODE_NONE);++cases;
        }
        // A failed recovery must report failure, never publish valid input.
        clear(r);callNumber=0;failAt=10;secondFail=12;
        assert(!RenderSoldierHD(r,frame,classic,src,dst,replaced)&&!replaced&&live==0);
        secondFail=0;
        // Fade/occlusion/missing body returns a native classic frame, never stale HD.
        auto fallback=ComposeSoldierArtHDLayers(scene,id,false,asset(d));
        clear(r);failAt=0;assert(RenderSoldierHD(r,fallback,classic,src,dst,replaced)&&!replaced);
        assert(read(r)==classicPixels);
        // Re-enter after rejected interval; no GPU object survives the previous call.
        clear(r);assert(RenderSoldierHD(r,frame,classic,src,dst,replaced)&&replaced);assert(read(r)==actual);
        auto cropped=src;cropped.w=60;SDL_FRect unused;assert(!SoldierHDRect(frame,cropped,dst,unused));
        SDL_DestroyTexture(oracle);SDL_DestroyTexture(classic);SDL_DestroyRenderer(r);SDL_DestroySurface(surface);++cases;
    }
    std::cout<<"PASS SDL software: integer-scale oracle, fractional body bounds and "<<cases<<" failure/transition cases\n";
}

#endif
