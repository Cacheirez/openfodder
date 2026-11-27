// GPL-3.0-or-later.
// Synthetic producers exercise coordinator order; real blitters have separate
// differential suites. All surfaces and conversion/fade/Save/Restore are real.
#include <functional>
#include <mutex>
struct Window {
 int ends=0,cycles=0; size_t first=0;
 std::vector<std::vector<std::vector<uint32>>> groups;
 std::vector<std::vector<uint32>> pending;
 void RenderAt(cSurface* s,bool=false){pending.push_back(*s->CaptureRGBLayer().pixels);}
 void RenderShrunk(cSurface* s){RenderAt(s);}
 void FrameEnd(){groups.push_back(pending);pending.clear();++ends;}
 void Cycle(){++cycles;}
};
struct cFodder;
struct Graphics {
 cFodder* owner;
 void PaletteSet();void MapTiles_Draw();void Sidebar_Copy_To_Surface(int=0,cSurface* =nullptr);
};
struct Params{bool mDemoPlayback=false,mDemoRecord=false,mDisableVideo=false;};
struct Recording{int tick=0;void Tick(){++tick;}};
struct Game{Recording mDemoRecorded;};
struct cFodder {
 cSurface *mSurface=nullptr,*mSurface2=nullptr,*alternate=nullptr;
 Window* mWindow;Graphics* mGraphics;Params *mParams,*mStartParams;Game mGame_Data;
 std::mutex mSurfaceMtx;std::function<void()> mInterruptCallback;
 bool mPhase_In_Progress=true,mPhase_Paused=false,mPhase_ShowMapOverview=false;
 bool mPhase_Aborted=true,mVideo_Ticked=false,mVideo_Done=false;
 int repeats=1,events=0,pauseEvents=0,ticks=0,prepares=0,requested=3,cursor=0;
 int variant=0,mode=0;std::vector<uint32> effects;
 std::vector<std::vector<uint32>> trace;
 std::vector<std::pair<openfodder::MissionPresentation,int>> missionFrames;
 std::vector<std::pair<openfodder::PausePresentation,int>> pauseFrames;
 void stamp(int tag){ // Overlap makes reordering producers observable.
  for(size_t i=0;i<mSurface->mSurfaceBufferSize;++i)
   if((i+tag)%5) mSurface->mSurfaceBuffer[i]=uint8(mSurface->mSurfaceBuffer[i]*3+tag+ticks);
  effects.push_back(tag);
 }
 void Phase_Loop_Interrupt(){++ticks;effects.push_back(1);}
 void Sprites_Draw(){stamp(3);}
 void Mouse_DrawCursor(){if(mParams->mDisableVideo)return;if(requested>=0){cursor=requested;requested=-1;}stamp(5+cursor);}
 void Draw_Phase_Paused(){++prepares;effects.push_back(20);mSurface->paletteNew_SetDimmed(64);}
 void checkpoint(){
  auto a=logical(*mSurface),b=logical(*mSurface2);a.insert(a.end(),b.begin(),b.end());
  a.insert(a.end(),effects.begin(),effects.end());
  a.insert(a.end(),{uint32(events),uint32(ticks),uint32(prepares),uint32(requested),uint32(cursor),
   uint32(mPhase_Paused),uint32(mPhase_Aborted),uint32(mVideo_Ticked),uint32(mVideo_Done),
   uint32(mGame_Data.mDemoRecorded.tick),uint32(mWindow->cycles),uint32(mWindow->ends)});
  trace.push_back(a);
 }
 void replace(int seed){
  size_t w=mSurface->GetWidth()+16,h=mSurface->GetHeight()+1;
  delete mSurface;delete mSurface2;
  mSurface=new cSurface(w,h);mSurface2=new cSurface(w,h);
  fill(*mSurface,seed,false);fill(*mSurface2,seed+17,false);
  requested=seed%4;effects.push_back(40+seed);
 }
 void interrupt(){if(variant==0)LegacyInterrupt_Redraw();else Interrupt_Redraw();}
 void eventsProcess(){
  ++events;
  if(mPhase_Paused){
   ++pauseEvents;
   if(pauseEvents==2 || pauseEvents==4)replace(pauseEvents+10);
   // Model timer progress between event-loop iterations. Production still
   // happens once even if the retained image is presented zero/five times.
   interrupt();
   if(pauseEvents==6)mPhase_Paused=false;
  }
  checkpoint();
 }
 void Video_SurfaceRender(bool=false,bool=false,cSurface* =nullptr,bool=true);
 void LegacyVideo_SurfaceRender(bool=false,bool=false,cSurface* =nullptr,bool=true);
 void ScheduledVideo_SurfaceRender(bool=false,bool=false,cSurface* =nullptr,bool=true);
 void Video_Sleep(cSurface* =nullptr,bool=false,bool=true);
 void LegacyVideo_Sleep(cSurface* =nullptr,bool=false,bool=true);
 void ScheduledVideo_Sleep(cSurface* =nullptr,bool=false,bool=true);
 void Interrupt_Redraw();void LegacyInterrupt_Redraw();
 void Phase_Paused();void LegacyPhase_Paused();void ScheduledPhase_Paused();
};
void Graphics::PaletteSet(){owner->effects.push_back(21);}
void Graphics::MapTiles_Draw(){owner->stamp(2);owner->mSurface->Save();owner->effects.push_back(12);}
void Graphics::Sidebar_Copy_To_Surface(int,cSurface*){owner->stamp(4);}
