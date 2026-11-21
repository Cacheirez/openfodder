// GPL-3.0-or-later. Controlled successful image loads and SDL storage.
#include <limits>
#include <new>
using int32=int32_t;using SDL_PixelFormat=int;
struct SDL_Renderer{};
constexpr int SDL_PIXELFORMAT_UNKNOWN=0,SDL_BLENDMODE_ADD=1;
#define SDL_LIL_ENDIAN 1234
#define SDL_BYTEORDER 1234
// The real LoadPng body assigns metadata from these deterministic fixtures.
int pngWidth=80,pngHeight=64,pngBytes=4;
void* stbi_load(const char*,int32* w,int32* h,int32* bytes,int){
 *w=pngWidth;*h=pngHeight;*bytes=pngBytes;
 const size_t pitch=(size_t(pngWidth*pngBytes)+3)&~size_t(3);
 return new uint32[pitch/4*pngHeight]{};
}
SDL_PixelFormat SDL_GetPixelFormatForMasks(int bits,uint32,uint32,uint32,uint32){return bits==32?1:2;}
SDL_Surface* SDL_CreateSurfaceFrom(int w,int h,int format,void* data,int pitch){return new SDL_Surface{w,h,pitch,format,data};}
void SDL_DestroySurface(SDL_Surface* s){delete[] static_cast<uint32*>(s->pixels);delete s;}
void SDL_DestroyTexture(SDL_Texture*){}
SDL_Texture* SDL_CreateTextureFromSurface(SDL_Renderer*,SDL_Surface*){return nullptr;}
void SDL_SetTextureBlendMode(SDL_Texture*,int){}
void SDL_SetTextureAlphaMod(SDL_Texture*,int){}
void SDL_SetTextureColorMod(SDL_Texture*,int,int,int){}
struct Window{SDL_Renderer* GetRenderer(){return nullptr;}} window;
Window* g_Window=&window;
std::vector<uint32> allState(cSurface& s){auto v=logical(s);auto rgb=s.CaptureRGBLayer();v.insert(v.end(),rgb.pixels->begin(),rgb.pixels->end());return v;}
void reject(cSurface& s,const openfodder::PresentationTarget& target){
 const auto before=allState(s);const int uploads=updates;
 assert(!s.ApplyPresentation(target));assert(allState(s)==before);assert(updates==uploads);
}
