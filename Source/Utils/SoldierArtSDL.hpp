// GPL-3.0-or-later. SDL3 transaction; no engine state or retained GPU resources.
#pragma once
#include "SoldierArtHDLayers.hpp"
#include <cmath>
namespace openfodder {
// Valid rectangles and wholly visible body only. Crop-edge poses keep classic.
inline bool SoldierHDRect(const SoldierArtHDLayers& frame,const SDL_FRect& src,
        const SDL_FRect& dst,SDL_FRect& patch) {
    if(frame.status!=SoldierArtHDStatus::Replaced ||
       (frame.density!=8 && frame.density!=12) ||
       frame.patch.size()!=224u*frame.density*frame.density ||
       !std::isfinite(src.x)||!std::isfinite(src.y)||!std::isfinite(src.w)||!std::isfinite(src.h)||
       !std::isfinite(dst.x)||!std::isfinite(dst.y)||!std::isfinite(dst.w)||!std::isfinite(dst.h)||
       src.w<=0||src.h<=0||dst.w<=0||dst.h<=0 || src.x<0 || src.y<0 ||
       src.x+src.w>frame.background.width || src.y+src.h>frame.background.height ||
       frame.logicalX<src.x || frame.logicalY<src.y ||
       frame.logicalX+16>src.x+src.w || frame.logicalY+14>src.y+src.h)return false;
    patch={dst.x+(frame.logicalX-src.x)*dst.w/src.w,
           dst.y+(frame.logicalY-src.y)*dst.h/src.h,16*dst.w/src.w,14*dst.h/src.h};
    return std::isfinite(patch.x)&&std::isfinite(patch.y)&&std::isfinite(patch.w)&&std::isfinite(patch.h);
}
struct SoldierSDLTexture {
    SDL_Texture* value=nullptr;
    ~SoldierSDLTexture(){if(value)SDL_DestroyTexture(value);}
};
// Classic texture is untouched until recovery after a partial draw; its original
// blend mode is restored. Failure to draw classic returns false to input publication.
inline bool RenderSoldierHD(SDL_Renderer* renderer,const SoldierArtHDLayers& frame,
        SDL_Texture* classic,const SDL_FRect& src,const SDL_FRect& dst,bool& replaced) {
    replaced=false;bool touched=false;
    auto fallback=[&](){
        if(!touched)return SDL_RenderTexture(renderer,classic,&src,&dst);
        SDL_BlendMode savedBlend;
        if(!SDL_GetTextureBlendMode(classic,&savedBlend) ||
           !SDL_SetTextureBlendMode(classic,SDL_BLENDMODE_NONE))return false;
        const bool drawn=SDL_RenderTexture(renderer,classic,&src,&dst);
        const bool restored=SDL_SetTextureBlendMode(classic,savedBlend);
        return drawn && restored;
    };
    SDL_FRect patchRect;
    if(!SoldierHDRect(frame,src,dst,patchRect))return fallback();
    const auto& bg=frame.background;
    if(!bg.width || !bg.height || bg.width>16384 || bg.height>16384 ||
       bg.stride!=bg.width || bg.pixels.size()!=bg.width*bg.height)return fallback();
    SoldierSDLTexture background,patch;
    background.value=SDL_CreateTexture(renderer,SDL_PIXELFORMAT_XRGB8888,
        SDL_TEXTUREACCESS_STREAMING,int(bg.width),int(bg.height));
    patch.value=SDL_CreateTexture(renderer,SDL_PIXELFORMAT_XRGB8888,
        SDL_TEXTUREACCESS_STREAMING,16*frame.density,14*frame.density);
    if(!background.value || !patch.value)return fallback();
    for(auto texture:{background.value,patch.value})
        if(!SDL_SetTextureBlendMode(texture,SDL_BLENDMODE_NONE) ||
           !SDL_SetTextureScaleMode(texture,SDL_SCALEMODE_NEAREST))return fallback();
    if(!SDL_UpdateTexture(background.value,nullptr,bg.pixels.data(),int(bg.stride*4)) ||
       !SDL_UpdateTexture(patch.value,nullptr,frame.patch.data(),int(16*frame.density*4)))return fallback();
    touched=true;
    if(!SDL_RenderTexture(renderer,background.value,&src,&dst) ||
       !SDL_RenderTexture(renderer,patch.value,nullptr,&patchRect))return fallback();
    replaced=true;return true;
}
} // namespace openfodder
