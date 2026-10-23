"""Compare actual classic HUD/cursor adapters with retained draws (ASan/UBSan).

Synthetic surfaces/resources; actual accessors, cursor request coordinator,
backend preparation and copy functions. Pixel kernel has its own original-body
suite. No claim of complete SDL/RGB/CD32 validation. GPL-3.0-or-later.
"""
import os
from pathlib import Path
import subprocess
import tempfile
from check_final_timer_equivalence import function
BASELINE='7eeb6f777cc2ddfd9c615a2a94eef69bd3625c41'

def main():
    root=Path(__file__).resolve().parents[2]
    def get(path,signature,old=False):
        s=subprocess.check_output(['git','show',BASELINE+':'+path],cwd=root,text=True) if old else (root/path).read_text()
        return function(s,signature)
    # Decisions/composition and cursor request timing are intentionally unchanged.
    for path in ['Source/Mouse.cpp','Source/GUI_Element.cpp']:
        assert (root/path).read_text()==subprocess.check_output(['git','show',BASELINE+':'+path],cwd=root,text=True),path
    for backend in ('PC','Amiga'):
        p=f'Source/{backend}/Graphics_{backend}.cpp'
        assert get(p,f'uint8* cGraphics_{backend}::GetSpriteData(')==get(p,f'uint8* cGraphics_{backend}::GetSpriteData(',True)
        for name in ('Sidebar_Copy_Sprite_To_ScreenBufPtr','Sidebar_Copy_ScreenBuffer'):
            sig=f'void cGraphics_{backend}::{name}('
            assert get(p,sig)==get(p,sig,True),sig
    sig='void cGraphics::Sidebar_Copy_ScreenBuffer_Common('
    assert get('Source/Graphics.cpp',sig)==get('Source/Graphics.cpp',sig,True)
    enums=(root/'Source/Version.hpp').read_text().split('enum eGFX_Types {',1)[1].split('};',1)[0]
    h=r'''
#include "Utils/SidebarDraw.hpp"
#include "Utils/ResolvedSpriteResource.hpp"
#include <iostream>
#include <array>
using namespace openfodder;
using uint8=uint8_t;using uint16=uint16_t;using int16=int16_t;using uint32=uint32_t;
using tSharedBuffer=std::shared_ptr<std::vector<uint8>>;
constexpr int SIDEBAR_WIDTH=64;
'''+ 'enum eGFX_Types {'+enums+'};\n'+r'''
struct Header{uint16 mWidth=320,mHeight=300;uint8 mPlanes=4;};
struct Image{tSharedBuffer mData=std::make_shared<std::vector<uint8>>(150000);Header header;Header* GetHeader(){return &header;}};
struct Version{int special=0;bool isAmigaXmas()const{return special==1;}bool isAmigaNotVeryFestive()const{return special==2;}bool isAmigaAlienLevels()const{return special==3;}};
struct Params{bool mDisableVideo=false;};
struct cSurface{
 size_t width=400,height=280;
 std::vector<uint8> pixels=std::vector<uint8>(512*320,0xA5);
 uint8* GetSurfaceBuffer(){return pixels.data();}size_t GetWidth()const{return width;}size_t GetHeight()const{return height;}
};
struct cGraphics;
struct Engine{
 cGraphics* mGraphics=nullptr;Version* mVersionCurrent;Params* mParams;
 int16 mMouseSpriteCurrent=0,mMouseSpriteNew=-1,mMouseX=0,mMouseY=0,mMouseX_Offset=0,mMouseY_Offset=0;
 int16 mVideo_Draw_Columns=7,mVideo_Draw_Rows=11,mVideo_Draw_PosX=13,mVideo_Draw_PosY=15;
 uint8 mVideo_Draw_PaletteIndex=0x33;uint8* mVideo_Draw_FrameDataPtr=nullptr;
 size_t mDraw_Source_SkipPixelsPerRow=123,mDraw_Dest_SkipPixelsPerRow=456;
 uint16* mSidebar_Screen_Buffer=nullptr;
 void Mouse_CommitCursorRequest();void Mouse_DrawCursor();
};
Engine* g_Fodder;
struct sSpriteSheet_pstuff{int16 mX=0,mY=0,mColumns=16,mRows=16;uint8* GetGraphicsPtr(uint16)const;};
struct cGraphics{
 Engine* mFodder; cSurface* mSurface;
 Image mSpriteSheet_InGame1,mSpriteSheet_InGame2,mSpriteSheet_RankFont,mImageFonts,mImagePStuff,mImageRecruit,mImageHillBackground,mImageHillSprites,mImageService,mImageMissionIntro;
 std::array<sSpriteSheet_pstuff,8> mSpriteSheet_PStuff;
 FrozenSpriteResources mFrozenSpriteResources;
 bool legacy=false;
 virtual uint8* GetSpriteData(uint16)=0;
 virtual tSharedBuffer GetSpriteResourceStorage(uint16)const=0;
 virtual SpriteRasterLayout GetSpriteRasterLayout()const=0;
 virtual void Mouse_DrawCursor()=0;
 virtual PreparedSpriteDraw Cursor_PrepareLegacyDraw()=0;
 PreparedSpriteDraw CaptureCursorDraw();
 void Video_Draw_8(cSurface* = nullptr,const uint8* = nullptr);
 void Video_Draw_8_Prepared(const SpriteDrawState&,cSurface*,const uint8*);
 void Video_Draw_8_Resolved(const PreparedSpriteDraw&,cSurface* = nullptr);
 SidebarDraw CaptureSidebarDraw(int16,bool)const;
 void Sidebar_Copy_To_Surface_Common(int16,cSurface*,bool);
 void OldSidebar(int16,cSurface*,bool);
};
struct cGraphics_PC:cGraphics{
 uint8* GetSpriteData(uint16)override;tSharedBuffer GetSpriteResourceStorage(uint16)const override;SpriteRasterLayout GetSpriteRasterLayout()const override;
 void OldCursor();void NewCursor();void Mouse_DrawCursor()override{if(legacy)OldCursor();else NewCursor();}
 PreparedSpriteDraw Cursor_PrepareLegacyDraw()override;
};
struct cGraphics_Amiga:cGraphics{
 Header* mBMHD_Current=&mImageFonts.header;uint16 mCursorPalette=0x70;
 uint8* GetSpriteData(uint16)override;tSharedBuffer GetSpriteResourceStorage(uint16)const override;SpriteRasterLayout GetSpriteRasterLayout()const override;
 void OldCursor();void NewCursor();void Mouse_DrawCursor()override{if(legacy)OldCursor();else NewCursor();}
 PreparedSpriteDraw Cursor_PrepareLegacyDraw()override;
};
'''
    h+=get('Source/Mouse.cpp','void cFodder::Mouse_CommitCursorRequest()').replace('cFodder::','Engine::')
    h+=get('Source/Mouse.cpp','void cFodder::Mouse_DrawCursor()').replace('cFodder::','Engine::')
    h+=get('Source/SpriteSheet.cpp','uint8* sSpriteSheet_pstuff::GetGraphicsPtr(')
    for backend in ('PC','Amiga'):
        p=f'Source/{backend}/Graphics_{backend}.cpp';cls=f'cGraphics_{backend}'
        for sig in [f'uint8* {cls}::GetSpriteData(',f'tSharedBuffer {cls}::GetSpriteResourceStorage(',f'openfodder::SpriteRasterLayout {cls}::GetSpriteRasterLayout(',f'openfodder::PreparedSpriteDraw {cls}::Cursor_PrepareLegacyDraw(']:h+=get(p,sig)
        h+=get(p,f'void {cls}::Mouse_DrawCursor(',True).replace('::Mouse_DrawCursor(','::OldCursor(')
        h+=get(p,f'void {cls}::Mouse_DrawCursor(').replace('::Mouse_DrawCursor(','::NewCursor(')
    for sig in ['void cGraphics::Video_Draw_8(','void cGraphics::Video_Draw_8_Prepared(','void cGraphics::Video_Draw_8_Resolved(','openfodder::PreparedSpriteDraw cGraphics::CaptureCursorDraw(','openfodder::SidebarDraw cGraphics::CaptureSidebarDraw(','void cGraphics::Sidebar_Copy_To_Surface_Common(']:h+=get('Source/Graphics.cpp',sig)
    h+=get('Source/Graphics.cpp','void cGraphics::Sidebar_Copy_To_Surface_Common(',True).replace('::Sidebar_Copy_To_Surface_Common(','::OldSidebar(')
    h+=r'''
bool same(const Engine&a,const Engine&b){return a.mMouseSpriteCurrent==b.mMouseSpriteCurrent&&a.mMouseSpriteNew==b.mMouseSpriteNew&&a.mVideo_Draw_FrameDataPtr==b.mVideo_Draw_FrameDataPtr&&a.mVideo_Draw_Columns==b.mVideo_Draw_Columns&&a.mVideo_Draw_Rows==b.mVideo_Draw_Rows&&a.mVideo_Draw_PosX==b.mVideo_Draw_PosX&&a.mVideo_Draw_PosY==b.mVideo_Draw_PosY&&a.mVideo_Draw_PaletteIndex==b.mVideo_Draw_PaletteIndex&&a.mDraw_Source_SkipPixelsPerRow==b.mDraw_Source_SkipPixelsPerRow&&a.mDraw_Dest_SkipPixelsPerRow==b.mDraw_Dest_SkipPixelsPerRow;}
int main(){
 cGraphics_PC pc;cGraphics_Amiga amiga;Version v;Params p;Engine e;e.mVersionCurrent=&v;e.mParams=&p;
 size_t cursors=0,huds=0;
 for(auto* gfx:{static_cast<cGraphics*>(&pc),static_cast<cGraphics*>(&amiga)}){
  for(size_t i=0;i<gfx->mImagePStuff.mData->size();++i)(*gfx->mImagePStuff.mData)[i]=(i*17+i/19)&255;
  for(int i=0;i<8;++i){auto& s=gfx->mSpriteSheet_PStuff[i];s.mX=i*16;s.mY=i==7?300:i*20;s.mColumns=16+(i%3)*16;s.mRows=1+i*3;}
  for(int special=0;special<4;++special)for(int current=0;current<8;++current)for(int request:{-1,0,7})for(bool off:{false,true})for(int pos:{0,37,200})for(bool nullGraphics:{false,true}){
   v.special=special;p.mDisableVideo=off;e.mGraphics=nullGraphics?nullptr:gfx;e.mMouseSpriteCurrent=current;e.mMouseSpriteNew=request;e.mMouseX=pos;e.mMouseY=pos/2;
   Engine before=e,after=e;cSurface oldTarget,newTarget;gfx->legacy=true;gfx->mFodder=&before;gfx->mSurface=&oldTarget;g_Fodder=&before;before.Mouse_DrawCursor();
   gfx->legacy=false;gfx->mFodder=&after;gfx->mSurface=&newTarget;g_Fodder=&after;after.Mouse_DrawCursor();
   if(!same(before,after)||oldTarget.pixels!=newTarget.pixels){std::cerr<<"cursor mismatch\n";return 1;}
   ++cursors;
  }
 }
 // Actual shared HUD copy: active-surface geometry is retained even with a
 // destination whose advertised dimensions differ. No engine fields change.
 std::vector<uint16> sidebar(48*320/2);for(size_t i=0;i<sidebar.size();++i)sidebar[i]=(i*73)&65535;
 e.mSidebar_Screen_Buffer=sidebar.data();pc.mFodder=&e;
 for(bool amigaOffset:{false,true})for(int height:{64,200,224,280})for(int width:{320,352,400})for(int start:{0,1,7,16,40,300})for(bool alternate:{false,true}){
  cSurface activeOld,activeNew,destOld,destNew;activeOld.width=activeNew.width=width;activeOld.height=activeNew.height=height;destOld.width=destNew.width=512;
  pc.mSurface=&activeOld;pc.OldSidebar(start,alternate?&destOld:nullptr,amigaOffset);
  pc.mSurface=&activeNew;const Engine state=e;auto captured=pc.CaptureSidebarDraw(start,amigaOffset);
  if(!same(e,state)||activeNew.pixels!=cSurface{}.pixels)return 2;
  pc.Sidebar_Copy_To_Surface_Common(start,alternate?&destNew:nullptr,amigaOffset);
  if(activeOld.pixels!=activeNew.pixels||destOld.pixels!=destNew.pixels)return 3;
  cSurface pure;for(int i=0;i<3;++i)RasterizeSidebar(captured,pure.pixels.data());
  if(pure.pixels!=(alternate?destOld.pixels:activeOld.pixels))return 4;
  ++huds;
 }
 // Retained HUD survives source replacement and producer destruction.
 SidebarDraw hud;std::weak_ptr<const std::vector<uint8>> hudLife;cSurface expectedHud;
 {std::vector<uint8> bytes(48*300,0x67);hud=CaptureSidebar(bytes.data(),400,224,7,true);hudLife=hud.pixels;RasterizeSidebar(hud,expectedHud.pixels.data());bytes.assign(1,0);}
 auto hudCopy=hud;hud={};cSurface actualHud;RasterizeSidebar(hudCopy,actualHud.pixels.data());if(actualHud.pixels!=expectedHud.pixels||hudLife.expired())return 5;hudCopy={};if(!hudLife.expired())return 6;
 // Real prepared cursor outlives mutable image, header, backend and engine.
 for(bool isAmiga:{false,true}){
  PreparedSpriteDraw retained;cSurface expected;std::weak_ptr<const std::vector<uint8>> life;
  {
   cGraphics_PC producerPC;cGraphics_Amiga producerAmiga;cGraphics* producer=isAmiga?static_cast<cGraphics*>(&producerAmiga):static_cast<cGraphics*>(&producerPC);
   Engine engine=e;engine.mGraphics=producer;engine.mVideo_Draw_PosX=80;engine.mVideo_Draw_PosY=40;engine.mMouseSpriteCurrent=0;
   producer->mFodder=&engine;g_Fodder=&engine;producer->mSurface=&expected;std::fill(producer->mImagePStuff.mData->begin(),producer->mImagePStuff.mData->end(),0x69);
   retained=producer->Cursor_PrepareLegacyDraw();life=retained.resource.bytes;
   auto again=producer->CaptureCursorDraw();if(again.resource.bytes!=retained.resource.bytes)return 7;
   RasterizeSprite8(retained.draw,retained.resource.layout,{expected.pixels.data(),400});
   (*producer->mImagePStuff.mData)[0]^=255;auto changed=producer->CaptureCursorDraw();if(changed.resource.bytes==retained.resource.bytes)return 8;
   producer->GetSpriteData(eGFX_FONT);producer->mImagePStuff.mData->assign(1,0);producer->mImagePStuff.header.mHeight=1;
  }
  auto copy=retained;retained={};auto moved=std::move(copy);cSurface actual;for(int i=0;i<3;++i)RasterizeSprite8(moved.draw,moved.resource.layout,{actual.pixels.data(),400});
  if(actual.pixels!=expected.pixels||life.expired())return 9;moved={};if(!life.expired())return 10;
 }
 std::cout<<"PASS: "<<cursors<<" cursor cases; "<<huds<<" HUD cases; legacy request/guard, source registers, effective palettes, retained lifetimes and repeated pixels\n";
}
'''
    with tempfile.TemporaryDirectory(prefix='openfodder-hud-') as folder:
        source=Path(folder)/'test.cpp';binary=Path(folder)/'test';source.write_text(h)
        subprocess.run(['g++','-std=c++14','-O1','-fsanitize=address,undefined','-fno-sanitize-recover=all','-I'+str(root/'Source'),str(source),'-o',str(binary)],check=True)
        subprocess.run([str(binary)],env=dict(os.environ,ASAN_OPTIONS=os.environ.get('ASAN_OPTIONS','detect_leaks=1')),check=True)
if __name__=='__main__':main()
