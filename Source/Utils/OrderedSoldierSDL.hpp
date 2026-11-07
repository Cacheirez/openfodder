// GPL-3.0-or-later. Transactional publication of ordered, disjoint HD cells.
#pragma once
#include "OrderedSoldierArt.hpp"
#include <SDL3/SDL.h>
#include <cmath>
namespace openfodder {
struct OrderedSoldierStrip {
    size_t x=0,y=0,width=0;
    std::vector<uint32_t> pixels;
};
// Horizontal runs avoid a texture per cell and preserve gaps made by occluders.
// This is an internal publisher: a production resource resolver is still required.
inline std::vector<OrderedSoldierStrip> PackOrderedSoldierStrips(const OrderedSoldierFrame& frame) {
    const auto& bg=frame.background;const auto d=frame.density;
    if((d!=8 && d!=12) || !bg.width || !bg.height || bg.width>16384 || bg.height>16384 ||
       bg.stride!=bg.width || bg.pixels.size()!=bg.width*bg.height)
        throw std::invalid_argument("ordered SDL frame geometry");
    std::vector<OrderedSoldierStrip> strips;
    auto it=frame.cells.begin();
    while(it!=frame.cells.end()){
        const size_t first=it->first;
        if(first>=bg.width*bg.height)throw std::out_of_range("ordered SDL cell");
        auto end=it;size_t count=0;
        while(end!=frame.cells.end() && end->first==first+count && end->first/bg.width==first/bg.width){
            if(end->second.size()!=size_t(d)*d)throw std::invalid_argument("ordered SDL cell pixels");
            ++count;++end;
        }
        OrderedSoldierStrip strip;strip.x=first%bg.width;strip.y=first/bg.width;strip.width=count;
        strip.pixels.resize(count*d*d);
        for(size_t x=0;it!=end;++it,++x)for(size_t y=0;y<d;++y)
            std::copy_n(it->second.begin()+y*d,d,strip.pixels.begin()+y*count*d+x*d);
        strips.push_back(std::move(strip));
    }
    return strips;
}
struct OrderedSDLTextures {
    std::vector<SDL_Texture*> values;
    ~OrderedSDLTextures(){for(auto t:values)SDL_DestroyTexture(t);}
};
// Upload every texture before the first write. Any later error repaints the WHOLE
// viewport from the independent classic texture, with blending disabled, then
// restores its blend mode. The caller must not publish input if recovery fails.
inline bool RenderOrderedSoldierHD(SDL_Renderer* renderer,const OrderedSoldierFrame& frame,
        SDL_Texture* classic,const SDL_FRect& src,const SDL_FRect& dst,bool& replaced) {
    replaced=false;bool touched=false;
    auto fallback=[&](){
        if(!touched)return SDL_RenderTexture(renderer,classic,&src,&dst);
        SDL_BlendMode savedBlend;
        if(!SDL_GetTextureBlendMode(classic,&savedBlend) || !SDL_SetTextureBlendMode(classic,SDL_BLENDMODE_NONE))return false;
        const bool drawn=SDL_RenderTexture(renderer,classic,&src,&dst);
        const bool restored=SDL_SetTextureBlendMode(classic,savedBlend);
        return drawn && restored;
    };
    const auto& bg=frame.background;
    for(float v:{src.x,src.y,src.w,src.h,dst.x,dst.y,dst.w,dst.h})if(!std::isfinite(v))return false;
    if(src.w<=0 || src.h<=0 || dst.w<=0 || dst.h<=0 || src.x<0 || src.y<0 ||
       src.x+src.w>bg.width || src.y+src.h>bg.height)return false;
    if(!frame.complete())return fallback(); // Missing is never a partial modern success.
    try {
        const auto strips=PackOrderedSoldierStrips(frame);
        OrderedSDLTextures textures;
        textures.values.reserve(strips.size()+1);
        auto upload=[&](const uint32_t* pixels,size_t w,size_t h){
            auto t=SDL_CreateTexture(renderer,SDL_PIXELFORMAT_XRGB8888,SDL_TEXTUREACCESS_STREAMING,int(w),int(h));
            if(!t)return false;
            textures.values.push_back(t);
            return SDL_SetTextureBlendMode(t,SDL_BLENDMODE_NONE) && SDL_SetTextureScaleMode(t,SDL_SCALEMODE_NEAREST) &&
                SDL_UpdateTexture(t,nullptr,pixels,int(w*4));
        };
        if(!upload(bg.pixels.data(),bg.width,bg.height))return fallback();
        struct Draw {SDL_FRect source,destination;size_t texture;};
        std::vector<Draw> draws;
        for(const auto& strip:strips){
            const float left=std::max(float(strip.x),src.x),top=std::max(float(strip.y),src.y);
            const float right=std::min(float(strip.x+strip.width),src.x+src.w),bottom=std::min(float(strip.y+1),src.y+src.h);
            if(left>=right || top>=bottom)continue;
            if(!upload(strip.pixels.data(),strip.width*frame.density,frame.density))return fallback();
            Draw draw{{(left-strip.x)*frame.density,(top-strip.y)*frame.density,
                       (right-left)*frame.density,(bottom-top)*frame.density},
                      {dst.x+(left-src.x)*dst.w/src.w,dst.y+(top-src.y)*dst.h/src.h,
                       (right-left)*dst.w/src.w,(bottom-top)*dst.h/src.h},textures.values.size()-1};
            for(float v:{draw.destination.x,draw.destination.y,draw.destination.w,draw.destination.h})
                if(!std::isfinite(v))return false;
            // Quantize shared endpoints, not position and extent separately.
            // SDL software rounds each RenderTexture extent independently; a
            // one-row strip otherwise leaves cracks at fractional window scales.
            const float x0=std::floor(dst.x+(left-src.x)*dst.w/src.w);
            const float x1=std::floor(dst.x+(right-src.x)*dst.w/src.w);
            const float y0=std::floor(dst.y+(top-src.y)*dst.h/src.h);
            const float y1=std::floor(dst.y+(bottom-src.y)*dst.h/src.h);
            draw.destination={x0,y0,x1-x0,y1-y0};
            if(x1>x0 && y1>y0)draws.push_back(draw);
        }
        touched=true;
        if(!SDL_RenderTexture(renderer,textures.values[0],&src,&dst))return fallback();
        for(const auto& draw:draws)
            if(!SDL_RenderTexture(renderer,textures.values[draw.texture],&draw.source,&draw.destination))return fallback();
        replaced=true;return true;
    } catch(const std::bad_alloc&) {return fallback();}
      catch(const std::invalid_argument&) {return fallback();}
      catch(const std::out_of_range&) {return fallback();}
}
} // namespace openfodder
