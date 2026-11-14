// GPL-3.0-or-later. Differential scheduler cases.
struct Result {
 std::vector<std::vector<uint32>> trace;
 std::vector<std::vector<std::vector<uint32>>> groups;
 std::vector<std::pair<std::vector<uint32>,int>> retained;
 std::vector<uint32> state;
};
Result run(int w,int h,int mode,int repeats,int variant){
 Window window;Params params,start;cFodder f;Graphics graphics{&f};
 f.mWindow=&window;f.mGraphics=&graphics;f.mParams=&params;f.mStartParams=&start;
 f.repeats=repeats;f.variant=variant;f.mode=mode;
 f.mSurface=new cSurface(w,h);f.mSurface2=new cSurface(w,h);f.alternate=new cSurface(w,h);
 fill(*f.mSurface,3,false);fill(*f.mSurface2,7,false);fill(*f.alternate,13,false);
 params.mDemoRecord=true;
 // Normal route plus each exclusion, including different disable-video flags.
 if(mode==1) f.mInterruptCallback=[&f](){f.stamp(17);};
 if(mode==2) f.mPhase_ShowMapOverview=true;
 if(mode==3) f.mPhase_In_Progress=false;
 if(mode==4) start.mDisableVideo=params.mDisableVideo=true;
 if(mode==5) f.mSurface->mIsLoadedImage=true;
 if(mode==9) params.mDisableVideo=true;
 auto render=[&](){
  cSurface* s=mode==6?f.alternate:nullptr;
  if(mode==8){
   if(variant==0)f.LegacyVideo_SurfaceRender(false,false,s,false);
   else if(variant==1)f.Video_SurfaceRender(false,false,s,false);
   else f.ScheduledVideo_SurfaceRender(false,false,s,false);
  }else{
   if(variant==0)f.LegacyVideo_Sleep(s,mode==7,true);
   else if(variant==1)f.Video_Sleep(s,mode==7,true);
   else f.ScheduledVideo_Sleep(s,mode==7,true);
  }
 };
 for(int step=0;step<4;++step){
  f.interrupt();
  // Main-cycle writes AFTER interrupt: catching a snapshot at the wrong point
  // would lose these pixels / use the earlier effective fade palette.
  f.stamp(19);f.mSurface->palette_FadeTowardNew();render();f.checkpoint();
 }
 // Transitions exercised on the normal mission route only. Other modes prove
 // guards/fallback, not unsupported PNG pause or alternate scene transitions.
 if(mode==0 || mode==9){
  f.mPhase_Paused=true;
  if(variant==0)f.LegacyPhase_Paused();else if(variant==1)f.Phase_Paused();else f.ScheduledPhase_Paused();
  f.checkpoint();
  for(int step=0;step<3;++step){f.interrupt();f.stamp(19);render();f.checkpoint();}
  f.replace(31);f.interrupt();render();f.checkpoint();
 }
 Result r{f.trace,window.groups,{},logical(*f.mSurface)};
 delete f.mSurface;delete f.mSurface2;delete f.alternate;
 for(const auto& saved:f.missionFrames){
  const auto copy=saved.first;auto expected=openfodder::RasterizeMissionPresentation(copy);
  r.retained.push_back({expected.pixels,saved.second});
  for(int i=0;i<3;++i){auto out=openfodder::RasterizeMissionPresentation(copy);
   assert(out.pixels==expected.pixels);out.pixels[0]^=123;
   assert(openfodder::RasterizeMissionPresentation(copy).pixels==expected.pixels);}
 }
 for(const auto& saved:f.pauseFrames){
  const auto copy=saved.first;auto expected=openfodder::RasterizePausePresentation(copy);
  r.retained.push_back({expected.background.pixels,saved.second});
  for(int i=0;i<3;++i){auto out=openfodder::RasterizePausePresentation(copy);
   assert(out.background.pixels==expected.background.pixels && out.text.pixels==expected.text.pixels);
   out.background.pixels[0]^=123;out.text.pixels[0]^=321;}
 }
 return r;
}
int main(){size_t cases=0,retained=0;
 for(int w:{80,400})for(int h:{64,96})for(int padding:{0,3})for(int mode=0;mode<10;++mode){
  pad=padding;const auto old=run(w,h,mode,1,0),actual=run(w,h,mode,1,1);
  assert(old.groups==actual.groups && old.trace==actual.trace && old.state==actual.state);
  for(int n:{0,1,5}){
   const auto r=run(w,h,mode,n,2);
   assert(r.trace==old.trace && r.state==old.state && r.groups.size()==old.groups.size());
   std::vector<bool> scheduled(r.groups.size(),false);
   for(const auto& frame:r.retained){
    assert(old.groups[frame.second].size()==1);
    if(frame.first!=old.groups[frame.second][0]){std::cerr<<"retained mismatch w="<<w<<" h="<<h<<" pad="<<padding<<" mode="<<mode<<" n="<<n<<" group="<<frame.second<<"\n";for(size_t k=0;k<frame.first.size();++k)if(frame.first[k]!=old.groups[frame.second][0][k]){std::cerr<<"pixel "<<k<<" actual "<<frame.first[k]<<" expected "<<old.groups[frame.second][0][k]<<"\n";break;}std::abort();}scheduled[frame.second]=true;++retained;
   }
   for(size_t j=0;j<r.groups.size();++j){
    if(!scheduled[j]){assert(r.groups[j]==old.groups[j]);continue;}
    assert(r.groups[j].size()==size_t(n));
    for(const auto& frame:r.groups[j])assert(frame==old.groups[j][0]);
   }
   ++cases;
  }
 }
 std::cout<<"PASS: "<<cases<<" mission/pause schedules; "<<retained
 <<" retained frames match pre-change pixels after source destruction; real Interrupt_Redraw/Video_Sleep/Phase_Paused bodies; 0/1/5, guards, late main-cycle writes, fades, Save/Restore, resource changes and resume\n";
}
