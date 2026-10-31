// GPL-3.0-or-later. Actual methods appended by the Python driver.
#include "Utils/ResolvedSpriteResource.hpp"
#include <functional>
#include <mutex>
using uint16=uint16_t;using int32=int32_t;using int64=int64_t;
using Buffer=std::shared_ptr<std::vector<uint8>>;
struct Map { size_t getWidth()const{return 8;} } map;
struct Params {bool mUnitTesting=true;bool mDemoPlayback=false,mDemoRecord=false,mDisableVideo=false;};
struct Recording {int ticks=0;void Tick(){++ticks;}};
struct Game {Recording mDemoRecorded;};
struct Window {int frames=0,cycles=0;std::vector<std::vector<uint32>> pixels;void RenderAt(cSurface* s,bool=false){pixels.push_back(*s->CaptureRGBLayer().pixels);}void RenderShrunk(cSurface*){}void FrameEnd(){++frames;}void Cycle(){++cycles;}};
struct cFodder;
struct cGraphics {
 cFodder* mFodder; cSurface* mSurface;
 openfodder::SpriteRasterLayout layout;
 openfodder::SpriteRasterLayout GetSpriteRasterLayout()const{return layout;}
 virtual ~cGraphics()=default;
 virtual void MapTiles_Draw()=0;
 openfodder::SidebarDraw CaptureSidebarDraw(int16,bool)const;
 void Sidebar_Copy_To_Surface_Common(int16,cSurface*,bool);
 int paletteSets=0;
 void PaletteSet(){++paletteSets;}
 void Sidebar_Copy_To_Surface(int16 y=0,cSurface* s=nullptr){Sidebar_Copy_To_Surface_Common(y,s,false);}
 void Video_Draw_8_Prepared(const openfodder::SpriteDrawState&,cSurface*,const uint8*);
 void Video_Draw_8_Resolved(const openfodder::PreparedSpriteDraw&,cSurface* =nullptr);
};
struct cGraphics_PC:cGraphics {
 openfodder::TerrainAtlasCache mTerrainAtlas;
 openfodder::TerrainDraw CaptureVisibleTerrain();void MapTiles_Draw()override;
};
struct cGraphics_Amiga:cGraphics {
 Buffer mBlkData;
 openfodder::TerrainAtlasCache mTerrainAtlas;
 openfodder::TerrainDraw CaptureVisibleTerrain();void MapTiles_Draw()override;
};
struct cFodder {
 cSurface *mSurface,*mSurfaceFinal,*mSurface2=nullptr; cGraphics* mGraphics;Window* mWindow;
 Params *mParams,*mStartParams;Game mGame_Data;std::mutex mSurfaceMtx;
 bool mPhase_In_Progress=true,mPhase_Paused=false,mPhase_ShowMapOverview=false;
 bool mPhase_Aborted=true;
 int pausePrepares=0,pauseEvents=0;
 std::function<void()> pauseEvent;
 void Draw_Phase_Paused(){++pausePrepares;mSurface->paletteNew_SetDimmed(64);}
 void eventsProcess(){++pauseEvents;if(pauseEvent)pauseEvent();}
 void Phase_Paused();
 bool mVideo_Done=false,mVideo_Ticked=false;
 std::function<void()> mInterruptCallback;
 Buffer mMap,mTile_BaseBlk,mTile_SubBlk;Map* mMapLoaded=&map;
 int32 mMapTile_Ptr=0;uint16 mMapTile_RowOffset=0,mMapTile_ColumnOffset=0;
 uint16* mSidebar_Screen_Buffer;
 int16 mVideo_Draw_Columns=0;size_t mDraw_Source_SkipPixelsPerRow=0,mDraw_Dest_SkipPixelsPerRow=0;
 std::vector<uint8> sprite=std::vector<uint8>(65536,0x59);
 int effects=0,requests=0;
 int getWindowRows()const{return 1;}int getWindowColumns()const{return 2;}
 void draw(cSurface* target,bool cursor){
  openfodder::PreparedSpriteDraw p;p.resource.layout=mGraphics->layout;
  p.draw.source=sprite.data();p.draw.format=mGraphics->layout.format;
  p.draw.visible=true;
  p.draw.x=cursor?24:16;p.draw.y=cursor?24:16;p.draw.rows=4;
  p.draw.columns=p.draw.format==openfodder::SpriteDrawFormat::PC?8:2;
  p.draw.palette=cursor?0xF0:0x20;p.isCursor=cursor;
  if(!cursor) {
   p.resource.bytes=std::make_shared<const std::vector<uint8>>(sprite);
   p.draw.source=p.resource.source();
   auto& v=p.soldier;v.valid=true;v.scene=1;v.generation=2;
   v.geometry.spriteX=p.draw.x-64;v.geometry.spriteY=p.draw.y+p.draw.rows-16;
   v.geometry.rows=p.draw.rows;v.geometry.columns=p.draw.columns;
   v.geometry.palette=p.draw.palette;v.geometry.format=p.draw.format;
   v.geometry.viewWidth=48;v.geometry.viewHeight=32;
  }
  mGraphics->Video_Draw_8_Resolved(p,target);
 }
 void Sprites_Draw(cSurface* s=nullptr){++effects;draw(s,false);}
 void Mouse_DrawCursor(){++effects;++requests;draw(mSurface,true);}
 void Phase_Loop_Interrupt(){Mouse_DrawCursor();}
 void Interrupt_Redraw();
 void Video_SurfaceRender(bool=false,bool=false,cSurface* =nullptr,bool=true);
};
cFodder* g_Fodder;
