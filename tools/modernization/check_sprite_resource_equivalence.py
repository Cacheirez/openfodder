"""Check actual classic resource selection/preparation against retained resources.

Original accessors and pre-encapsulation preparation are extracted from git.
Only window/resource fixtures and clipping dispatch are stubbed; clipping and
raster kernels have their own original-body equivalence suites. GPL-3.0-or-later.
"""
import os
from pathlib import Path
import subprocess
import tempfile
from check_final_timer_equivalence import function

BASELINE = 'a2f63090fc0732787df8ba56cc142e9938771d9c'

def main():
    root = Path(__file__).resolve().parents[2]
    def old(path, signature):
        return function(subprocess.check_output(['git','show',BASELINE+':'+path],cwd=root,text=True), signature)
    def current(path, signature):
        return function((root/path).read_text(), signature)
    enums=(root/'Source/Version.hpp').read_text().split('enum eGFX_Types {',1)[1].split('};',1)[0]
    harness=r'''
#include "Utils/ResolvedSpriteResource.hpp"
#include <iostream>
#include <array>
using uint8=uint8_t; using uint16=uint16_t; using int16=int16_t;
using tSharedBuffer=std::shared_ptr<std::vector<uint8>>;
using namespace openfodder;
'''+ 'enum eGFX_Types {'+enums+'};\n'+r'''
struct Header { uint16 mWidth=320,mHeight=300; uint8 mPlanes=4; };
struct Image {
    tSharedBuffer mData = std::make_shared<std::vector<uint8>>(150000,0x96);
    Header header;
    Header* GetHeader() { return &header; }
};
struct Version {
    bool pc=false; int special=0;
    bool isPC() const { return pc; }
    bool isAmigaXmas() const { return special==1; }
    bool isAmigaNotVeryFestive() const { return special==2; }
    bool isAmigaAlienLevels() const { return special==3; }
};
struct Params { bool mDisableVideo=false; };
struct cSurface {
    std::vector<uint8> pixels=std::vector<uint8>(352*280,0xA5);
    uint8* GetSurfaceBuffer() { return pixels.data(); }
    size_t GetWidth() { return 352; }
};
struct cGraphics;
struct sSpriteSheet {
    uint16 mLoadOffset=0,mLoadSegment=0;
    int16 mColCount=4,mRowCount=16,mPalleteIndex=0;
    int8_t mModX=0,mModY=0;
    uint8* GetGraphicsPtr() const;
};
struct sSprite { int16 mRowsToSkip=0,mPosX=0,mPosY=32,mHeight=0,mWasDrawn=7; };
struct Engine {
    cGraphics* mGraphics; Version* mVersionCurrent; Params* mStartParams;
    sSpriteSheet sheet;
    uint8 mVideo_Draw_PaletteIndex=0x55;
    uint8* mVideo_Draw_FrameDataPtr=nullptr;
    int16 mVideo_Draw_Columns=19,mVideo_Draw_Rows=21,mVideo_Draw_PosX=23,mVideo_Draw_PosY=25;
    int16 mMapTile_DrawX=0,mMapTile_DrawY=0;
    size_t mDraw_Source_SkipPixelsPerRow=111,mDraw_Dest_SkipPixelsPerRow=222;
    const sSpriteSheet* Sprite_Get_Sheet(int16,int16 frame) { return frame<0 ? nullptr : &sheet; }
    int16 getWindowWidth() const { return 320; }
    bool Sprite_OnScreen_Check() {
        SpriteDrawState d;
        d.source=mVideo_Draw_FrameDataPtr; d.x=mVideo_Draw_PosX; d.y=mVideo_Draw_PosY;
        d.columns=mVideo_Draw_Columns; d.rows=mVideo_Draw_Rows;
        auto r=ClipSpriteDraw(d,mVersionCurrent->pc?SpriteDrawFormat::PC:SpriteDrawFormat::Amiga8,320,200);
        mVideo_Draw_FrameDataPtr+=r.sourceOffset; mVideo_Draw_PosX=r.x; mVideo_Draw_PosY=r.y;
        mVideo_Draw_Columns=r.columns; mVideo_Draw_Rows=r.rows;
        return r.visible;
    }
};
Engine* g_Fodder;
struct Window { Window GetScreenSize() const { return {}; } int16 getHeight() const { return 200; } } window;
Window* g_Window=&window;
struct cGraphics {
    Engine* mFodder=nullptr; cSurface surface; cSurface* mSurface=&surface;
    Image mSpriteSheet_InGame1,mSpriteSheet_InGame2,mSpriteSheet_RankFont,mImageFonts,mImagePStuff;
    Image mImageRecruit,mImageHillBackground,mImageHillSprites,mImageService,mImageMissionIntro;
    FrozenSpriteResources mFrozenSpriteResources;
    virtual uint8* GetSpriteData(uint16)=0;
    virtual tSharedBuffer GetSpriteResourceStorage(uint16) const=0;
    virtual SpriteRasterLayout GetSpriteRasterLayout() const=0;
    ResolvedSpriteResource ResolveSpriteResource(uint16,size_t,uint8);
    void Video_Draw_8_Resolved(const PreparedSpriteDraw&,cSurface*);
    void Video_Draw_8(cSurface* target) {
        if(!target) target=mSurface;
        SpriteDrawState d;d.source=mFodder->mVideo_Draw_FrameDataPtr;
        d.x=mFodder->mVideo_Draw_PosX;d.y=mFodder->mVideo_Draw_PosY;
        d.columns=mFodder->mVideo_Draw_Columns;d.rows=mFodder->mVideo_Draw_Rows;
        d.palette=mFodder->mVideo_Draw_PaletteIndex;d.format=GetSpriteRasterLayout().format;
        auto layout=GetSpriteRasterLayout();auto r=PrepareSpriteRasterRegisters(d,layout,target->GetWidth());
        mFodder->mVideo_Draw_Columns=r.columns;mFodder->mDraw_Source_SkipPixelsPerRow=r.sourceSkip;
        mFodder->mDraw_Dest_SkipPixelsPerRow=r.destinationSkip;
        RasterizeSprite8(d,layout,{target->GetSurfaceBuffer(),target->GetWidth()});
    }
};
struct cGraphics_PC:cGraphics {
    uint8* GetSpriteData(uint16) override;
    tSharedBuffer GetSpriteResourceStorage(uint16) const override;
    SpriteRasterLayout GetSpriteRasterLayout() const override;
};
struct cGraphics_Amiga:cGraphics {
    Header* mBMHD_Current=&mImageFonts.header; uint16 mCursorPalette=0x70;
    uint8* GetSpriteData(uint16) override;
    tSharedBuffer GetSpriteResourceStorage(uint16) const override;
    SpriteRasterLayout GetSpriteRasterLayout() const override;
};
struct LegacyFodder:Engine { bool Sprite_PrepareLegacyFrame(sSprite*,int16,int16); void Sprite_Draw_Frame(sSprite*,int16,int16,cSurface*); };
struct CurrentFodder:Engine { bool Sprite_PrepareLegacyFrame(sSprite*,int16,int16,PreparedSpriteDraw&); void Sprite_Draw_Frame(sSprite*,int16,int16,cSurface*); };
'''
    harness+=old('Source/SpriteSheet.cpp','uint8* sSpriteSheet::GetGraphicsPtr() const')
    for backend in ['PC','Amiga']:
        path=f'Source/{backend}/Graphics_{backend}.cpp'
        harness+=old(path,f'uint8* cGraphics_{backend}::GetSpriteData(')
        harness+=current(path,f'tSharedBuffer cGraphics_{backend}::GetSpriteResourceStorage(')
        harness+=current(path,f'openfodder::SpriteRasterLayout cGraphics_{backend}::GetSpriteRasterLayout(')
    harness+=current('Source/Graphics.cpp','openfodder::ResolvedSpriteResource cGraphics::ResolveSpriteResource(')
    harness+=current('Source/Graphics.cpp','void cGraphics::Video_Draw_8_Resolved(')
    harness+=old('Source/Sprites/Sprite_Core.cpp','bool cFodder::Sprite_PrepareLegacyFrame(').replace('cFodder::','LegacyFodder::')
    harness+=current('Source/Sprites/Sprite_Core.cpp','bool cFodder::Sprite_PrepareLegacyFrame(').replace('cFodder::','CurrentFodder::')
    harness+=old('Source/Sprites/Sprite_Core.cpp','void cFodder::Sprite_Draw_Frame(').replace('cFodder::','LegacyFodder::')
    harness+=current('Source/Sprites/Sprite_Core.cpp','void cFodder::Sprite_Draw_Frame(').replace('cFodder::','CurrentFodder::')
    harness+=r'''
bool same(const Engine& a,const Engine& b) {
 return a.mVideo_Draw_FrameDataPtr==b.mVideo_Draw_FrameDataPtr && a.mVideo_Draw_PaletteIndex==b.mVideo_Draw_PaletteIndex &&
 a.mVideo_Draw_Columns==b.mVideo_Draw_Columns && a.mVideo_Draw_Rows==b.mVideo_Draw_Rows &&
 a.mVideo_Draw_PosX==b.mVideo_Draw_PosX && a.mVideo_Draw_PosY==b.mVideo_Draw_PosY &&
 a.mDraw_Source_SkipPixelsPerRow==b.mDraw_Source_SkipPixelsPerRow && a.mDraw_Dest_SkipPixelsPerRow==b.mDraw_Dest_SkipPixelsPerRow;
}
int main() {
 cGraphics_PC pc; cGraphics_Amiga amiga;
 size_t cases=0;
 for (bool batched:{false,true})
 for (bool isPC:{true,false})
 for (int special:{0,1,2,3})
 for (int segment=0;segment<=11;++segment) {
  if (isPC && (segment==5 || segment>8)) continue;
  if (!isPC && segment==6) continue;
  auto* gfx=isPC?static_cast<cGraphics*>(&pc):static_cast<cGraphics*>(&amiga);
  for (int palette:{0,0x30,0xD0,0xF0})
  for (int offset:{0,7,160})
  for (int state:{0,1,2}) // visible, rejected geometry, invalid frame
  for (bool videoOff:{false,true}) {
   std::unique_ptr<FrozenSpriteResources::ReadOnlyBatch> batch;
   if(batched) batch.reset(new FrozenSpriteResources::ReadOnlyBatch(gfx->mFrozenSpriteResources));
   Version version;version.pc=isPC;version.special=special;
   Params params;params.mDisableVideo=videoOff;
   LegacyFodder legacy; legacy.mGraphics=gfx;legacy.mVersionCurrent=&version;legacy.mStartParams=&params;
   legacy.sheet.mLoadSegment=segment;legacy.sheet.mLoadOffset=offset;legacy.sheet.mPalleteIndex=palette;
   const Engine initial=legacy;
   sSprite before;before.mPosX=state==1?1000:0;
   auto after=before;
   gfx->mFodder=&legacy;g_Fodder=&legacy;
   bool visible=legacy.Sprite_PrepareLegacyFrame(&before,0,state==2?-1:0);
   auto oldLayout=gfx->GetSpriteRasterLayout();
   CurrentFodder engine;static_cast<Engine&>(engine)=initial;
   gfx->mFodder=&engine;g_Fodder=&engine;
   PreparedSpriteDraw prepared;
   bool newVisible=engine.Sprite_PrepareLegacyFrame(&after,0,state==2?-1:0,prepared);
   if(visible!=newVisible || before.mWasDrawn!=after.mWasDrawn || !same(legacy,engine)) {
    std::cerr<<"FAIL preparation "<<isPC<<' '<<segment<<' '<<palette<<' '<<state<<'\n';return 1;
   }
   if(state!=2) {
    auto storage=gfx->GetSpriteResourceStorage(segment);
    auto& r=prepared.resource;
    if(!r || r.bytes.get()==storage.get() || *r.bytes!=*storage ||
      r.palette!=legacy.mVideo_Draw_PaletteIndex || r.layout.format!=oldLayout.format ||
      r.layout.width!=oldLayout.width || r.layout.height!=oldLayout.height || r.layout.planes!=oldLayout.planes ||
      r.source()!=prepared.draw.source || r.available()!=r.bytes->size()-r.offset) return 2;
    if(visible && !videoOff) {
      cSurface expected,actual;
      auto reference=prepared.draw;reference.source=legacy.mVideo_Draw_FrameDataPtr;reference.sourceOffset=0;
      RasterizeSprite8(reference,oldLayout,{expected.GetSurfaceBuffer(),expected.GetWidth()});
      // Resolve another image to invalidate the active header/palette. Retained layout must win.
      gfx->GetSpriteData(eGFX_FONT);
      gfx->Video_Draw_8_Resolved(prepared,&actual);
      if(expected.pixels!=actual.pixels) return 3;
    }
   } else if(prepared.resource || after.mWasDrawn!=0) return 4;
   // Exercise actual callers, including video-off and invalid-frame guards.
   cSurface oldTarget,newTarget;
   static_cast<Engine&>(legacy)=initial;static_cast<Engine&>(engine)=initial;
   sSprite oldSprite,newSprite;oldSprite.mPosX=newSprite.mPosX=state==1?1000:0;
   gfx->mFodder=&legacy;g_Fodder=&legacy;
   legacy.Sprite_Draw_Frame(&oldSprite,0,state==2?-1:0,&oldTarget);
   gfx->mFodder=&engine;g_Fodder=&engine;
   engine.Sprite_Draw_Frame(&newSprite,0,state==2?-1:0,&newTarget);
   if(oldTarget.pixels!=newTarget.pixels || !same(legacy,engine) || oldSprite.mWasDrawn!=newSprite.mWasDrawn) return 13;
   ++cases;
  }
 }
 // Read-only passes reuse bytes, but never cache effective metadata or skip
 // checking edits between passes. Unscoped callers continue checking each time.
 {
  FrozenSpriteResources cache;
  std::vector<uint8> bytes(128,0x22);
  SpriteRasterLayout layout;
  ResolvedSpriteResource first,second;
  {
   FrozenSpriteResources::ReadOnlyBatch batch(cache);
   first=cache.capture(1,bytes,0,layout,0x30);
   layout.planes=5;
   second=cache.capture(1,bytes,7,layout,0x40);
   if(first.bytes!=second.bytes || first.generation!=second.generation ||
      second.offset!=7 || second.palette!=0x40 || second.layout.planes!=5) return 16;
  }
  bytes[0]^=0xFF;
  {
   FrozenSpriteResources::ReadOnlyBatch batch(cache);
   auto changed=cache.capture(1,bytes,0,layout,0x50);
   if(changed.bytes==first.bytes || changed.bytes->at(0)==first.bytes->at(0)) return 17;
  }
  bytes[1]^=0xFF;
  auto unscoped=cache.capture(1,bytes,0,layout,0x60);
  if(unscoped.bytes->at(1)!=bytes[1]) return 18;
  try {
   FrozenSpriteResources::ReadOnlyBatch batch(cache);
   cache.capture(1,bytes,0,layout,0);
   throw 1;
  } catch(int) {}
  bytes[2]^=0xFF;
  if(cache.capture(1,bytes,0,layout,0).bytes->at(2)!=bytes[2]) return 19;
 }
 // Retention: actual resolver, cache reuse, mutation/resize/reload and backend destruction.
 PreparedSpriteDraw retained;
 std::weak_ptr<const std::vector<uint8>> oldLifetime;
 cSurface expected;
 {
  cGraphics_Amiga producer;
  Version v;Params p;CurrentFodder e;e.mGraphics=&producer;e.mVersionCurrent=&v;e.mStartParams=&p;
  producer.mFodder=&e;g_Fodder=&e;e.sheet.mLoadSegment=eGFX_FONT;
  sSprite sprite;
  if(!e.Sprite_PrepareLegacyFrame(&sprite,0,0,retained)) return 5;
  if(retained.resource.palette!=0xF0) return 6; // table low byte is zero, original accessor wins
  auto again=producer.ResolveSpriteResource(eGFX_FONT,0,0);
  if(again.bytes!=retained.resource.bytes || again.generation!=retained.resource.generation) return 7;
  oldLifetime=retained.resource.bytes;
  RasterizeSprite8(retained.draw,retained.resource.layout,{expected.GetSurfaceBuffer(),expected.GetWidth()});
  producer.mImageFonts.mData->at(0)^=0xFF;
  auto inPlace=producer.ResolveSpriteResource(eGFX_FONT,0,0);
  if(inPlace.bytes==again.bytes || inPlace.bytes->at(0)==again.bytes->at(0)) return 14;
  producer.mImageFonts.header.mPlanes=5;
  auto layoutOnly=producer.ResolveSpriteResource(eGFX_FONT,0,0);
  if(layoutOnly.bytes!=inPlace.bytes || layoutOnly.layout.planes!=5 || retained.resource.layout.planes!=4) return 15;
  producer.mImageFonts.mData->assign(160000,0xFF);
  producer.mImageFonts.header.mHeight=320;
  producer.mImageFonts.header.mPlanes=5;
  auto changed=producer.ResolveSpriteResource(eGFX_FONT,0,0);
  if(changed.bytes==again.bytes || changed.generation==again.generation || changed.layout.height!=320) return 8;
  producer.mImageFonts.mData=std::make_shared<std::vector<uint8>>(170000,0x33);
  auto reloaded=producer.ResolveSpriteResource(eGFX_FONT,0,0);
  if(reloaded.bytes==changed.bytes || reloaded.bytes->at(0)!=0x33) return 9;
  if(producer.ResolveSpriteResource(eGFX_FONT,170000,0)) return 10;
 }
 cSurface actual;
 auto copy=retained;
 retained={};
 for(int i=0;i<3;++i) RasterizeSprite8(copy.draw,copy.resource.layout,{actual.GetSurfaceBuffer(),actual.GetWidth()});
 if(actual.pixels!=expected.pixels || oldLifetime.expired()) return 11;
 copy={};
 if(!oldLifetime.expired()) return 12;
 std::cout<<"PASS: "<<cases<<" original preparation/resource cases; effective palettes, planes and registers match; retained bytes survive mutation/reload/destruction and release after last owner\n";
}
'''
    with tempfile.TemporaryDirectory(prefix='openfodder-resources-') as folder:
        source=Path(folder)/'test.cpp';binary=Path(folder)/'test'
        source.write_text(harness)
        subprocess.run(['g++','-std=c++14','-O1','-fsanitize=address,undefined','-fno-sanitize-recover=all','-I'+str(root/'Source'),str(source),'-o',str(binary)],check=True)
        subprocess.run([str(binary)],env=dict(os.environ,ASAN_OPTIONS=os.environ.get('ASAN_OPTIONS', 'detect_leaks=1')),check=True)

if __name__=='__main__':
    main()
