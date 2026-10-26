int main(){
 size_t count=0,frames=0,transitions=0;
 uint64_t transitionDigest=1469598103934665603ull;
 auto digest=[&](uint32 value){transitionDigest^=value;transitionDigest*=1099511628211ull;};
 const int repeats=cSurface::MissionPresentationRepeats(true);
 assert(cSurface::MissionPresentationRepeats(false)==1);
 const bool publishing=cSurface::MissionPublicationEnabled();
 for(bool amiga:{false,true})for(int padding:{0,3})for(int n:{0,1,5})for(int seed:{1,7}){
  pad=padding;cSurface a(80,64),b(80,64);fill(a,seed,false);fill(b,seed+5,false);
  Params params;Window window;cGraphics_PC pc;cGraphics_Amiga ag;
  cGraphics* graphics=amiga?static_cast<cGraphics*>(&ag):static_cast<cGraphics*>(&pc);
  cFodder engine;engine.mSurface=&a;engine.mSurfaceFinal=&b;engine.mGraphics=graphics;
  engine.mWindow=&window;engine.mParams=engine.mStartParams=&params;g_Fodder=&engine;
  graphics->mFodder=&engine;graphics->mSurface=&a;
  graphics->layout.format=amiga?openfodder::SpriteDrawFormat::Amiga8:openfodder::SpriteDrawFormat::PC;
  graphics->layout.width=320;graphics->layout.height=32;graphics->layout.planes=4;
  engine.mMap=std::make_shared<std::vector<uint8>>(8*8*2,0);
  engine.mTile_BaseBlk=std::make_shared<std::vector<uint8>>(320*256,0x31);
  engine.mTile_SubBlk=std::make_shared<std::vector<uint8>>(320*256,0x21);
  ag.mBlkData=std::make_shared<std::vector<uint8>>(512*128,0xAA);
  std::vector<uint16> sidebar(48*64/2,0x4949);engine.mSidebar_Screen_Buffer=sidebar.data();
  engine.Interrupt_Redraw(); // actual coordinator, early cursor, terrain/Save, sprite, HUD, cursor
  assert(a.MissionAuditActive()&&b.MissionAuditActive());
  // Exercise the actual prepared hook as well as the resolved producer.
  openfodder::SpriteDrawState prepared;prepared.format=graphics->layout.format;
  prepared.source=engine.sprite.data();prepared.x=32;prepared.y=32;prepared.rows=2;
  prepared.columns=amiga?1:4;prepared.palette=0x30;
  graphics->Video_Draw_8_Prepared(prepared,&a,nullptr);
  engine.Sprites_Draw(&b); // late main-cycle sprites must stay in the secondary destination
  a.paletteNew_SetDimmed(32);a.palette_FadeTowardNew();
  auto scene=a.VerifyMissionAudit(&b);assert(scene.destinations.size()==2);
  assert(scene.layers.front().role==openfodder::MissionLayerRole::Cursor);
  assert(scene.layers.back().destination==b.mPresentationDestination);
  auto expected=openfodder::RasterizePresentationSurface(a.CapturePresentation());
  const auto logicalBefore=logical(a);const int effects=engine.effects,requests=engine.requests;
  for(int i=0;i<n;++i){engine.Video_SurfaceRender();frames+=repeats;if(repeats)assert(window.pixels.back()==expected.pixels);}
  assert(window.frames==n*repeats);
  for(const auto& pixels:window.pixels)assert(pixels==expected.pixels);
  assert(logical(a)==logicalBefore&&engine.effects==effects&&engine.requests==requests);
  std::fill(engine.sprite.begin(),engine.sprite.end(),0);engine.sprite.clear();engine.sprite.shrink_to_fit();
  engine.mTile_BaseBlk.reset();engine.mTile_SubBlk.reset();ag.mBlkData.reset();sidebar.clear();
  assert(openfodder::RasterizeMissionLayers(scene,a.mPresentationDestination).pixels==expected.pixels);
  a.Restore();a.VerifyMissionAudit(&b); // real Restore registered, including zero presentations
  // Deliberate untracked write must be detected, not patched from a pixel diff.
  a.GetSurfaceBuffer()[40*80+70]^=1;bool rejected=false;
  try{if(publishing)engine.Video_SurfaceRender();else a.VerifyMissionAudit(&b);}catch(const std::runtime_error&){rejected=true;}assert(rejected);
  a.GetSurfaceBuffer()[40*80+70]^=1;
  auto prior=a.mMissionAudit;
  a.BeginMissionAudit(&b,true);assert(a.mMissionAudit!=prior&&a.mMissionAudit->scene.layers.empty());
  a.clearBuffer(17);a.Restore();a.VerifyMissionAudit(&b);
  // Pause/unsupported scenes discard the diagnostic interval; re-entry takes fresh state.
  a.BeginMissionAudit(&b,false);assert(!a.MissionAuditActive()&&!b.MissionAuditActive());
  fill(a,seed+10,false);a.BeginMissionAudit(&b,true);a.VerifyMissionAudit(&b);
  // Even same-sized replacement has a new identity and must not satisfy the old interval.
  cSurface replacement(80,64);fill(replacement,99,false);rejected=false;
  try{a.VerifyMissionAudit(&replacement);}catch(const std::runtime_error&){rejected=true;}assert(rejected);
  if(publishing){
   auto before=logical(a);assert(!a.PresentRecordedMission(&replacement));
   assert(!a.MissionAuditActive()&&!replacement.MissionAuditActive()&&logical(a)==before);
   // No capture: the real coordinator publishes classic and does not create an interval.
   engine.Video_SurfaceRender();assert(!a.MissionAuditActive());
   if(repeats)assert(window.pixels.back()==openfodder::RasterizePresentationSurface(a.CapturePresentation()).pixels);
   // Restart after a transition, then publish without an intervening producer mutation.
   a.BeginMissionAudit(&b,true);assert(a.PresentRecordedMission(&b));
   assert(logical(a)==before);
  }
  // Diagnostic scheduling must not affect unsupported scenes or normal play.
  for(int guard=0;guard<5;++guard){
   const int before=window.frames;
   if(guard==0)engine.mPhase_Paused=true;
   if(guard==1)engine.mPhase_ShowMapOverview=true;
   if(guard==2)engine.mPhase_In_Progress=false;
   if(guard==3)params.mUnitTesting=false;
   engine.Video_SurfaceRender(false,false,nullptr,guard!=4);
   assert(window.frames==before+1);
   engine.mPhase_Paused=false;engine.mPhase_ShowMapOverview=false;
   engine.mPhase_In_Progress=true;params.mUnitTesting=true;
  }
  // Join the actual pause loop to the actual mission coordinators. SDL, input
  // and loading remain doubles; both same-size and resized replacements die
  // during pause, while the pre-pause command frame must remain usable.
  std::unique_ptr<cSurface> main(new cSurface(80,64)),final(new cSurface(80,64)),text(new cSurface(80,64));
  auto attach=[&](){engine.mSurface=main.get();engine.mSurfaceFinal=final.get();engine.mSurface2=text.get();graphics->mSurface=main.get();};
  auto resources=[&](int tag){
   engine.sprite.assign(65536,uint8(tag));
   engine.mTile_BaseBlk=std::make_shared<std::vector<uint8>>(320*256,uint8(tag+1));
   engine.mTile_SubBlk=std::make_shared<std::vector<uint8>>(320*256,uint8(tag+2));
   ag.mBlkData=std::make_shared<std::vector<uint8>>(512*128,uint8(tag+3));
   sidebar.assign(48*main->GetHeight()/2,uint16(tag*257));engine.mSidebar_Screen_Buffer=sidebar.data();
  };
  fill(*main,seed,false);fill(*final,seed+2,false);fill(*text,seed+3,true);attach();resources(19);
  for(int transition=0;transition<2;++transition){
   engine.Interrupt_Redraw();
   const auto retained=main->VerifyMissionAudit(final.get());
   const auto retainedDestination=main->mPresentationDestination;
   const auto retainedPixels=openfodder::RasterizeMissionLayers(retained,retainedDestination).pixels;
   engine.Video_SurfaceRender();
   int eventsBefore=engine.pauseEvents,cyclesBefore=window.cycles,framesBefore=window.frames;
   int effectsBefore=engine.effects,requestsBefore=engine.requests,paletteBefore=graphics->paletteSets;
   engine.mPhase_Paused=true;engine.mPhase_Aborted=true;
   engine.pauseEvent=[&](){
    assert(!main->MissionAuditActive()&&!final->MissionAuditActive());
    int tick=engine.pauseEvents-eventsBefore;
    if(tick==1||tick==2){
     size_t width=tick==1?main->GetWidth():main->GetWidth()+16;
     main.reset(new cSurface(width,64));final.reset(new cSurface(width,64));text.reset(new cSurface(width,64));
     fill(*main,seed+tick+transition,false);fill(*final,seed+tick+9,false);fill(*text,seed+tick+13,true);
     attach();resources(31+tick+transition);
     assert(main->mPresentationDestination!=retainedDestination);
    }
    assert(openfodder::RasterizeMissionLayers(retained,retainedDestination).pixels==retainedPixels);
    if(tick==3)engine.mPhase_Paused=false;
   };
   engine.Phase_Paused();
   assert(window.frames==framesBefore+3&&window.cycles==cyclesBefore+3);
   assert(engine.pauseEvents==eventsBefore+3&&!engine.mPhase_Aborted);
   assert(graphics->paletteSets==paletteBefore+1&&engine.effects==effectsBefore+1&&engine.requests==requestsBefore);
   assert(!main->MissionAuditActive()&&!final->MissionAuditActive());
   engine.Interrupt_Redraw(); // A new interval owns only the current destinations/resources.
   const auto resumed=main->VerifyMissionAudit(final.get());
   const auto resumedPixels=openfodder::RasterizeMissionLayers(resumed,main->mPresentationDestination).pixels;
   framesBefore=window.frames;effectsBefore=engine.effects;requestsBefore=engine.requests;
   engine.Video_SurfaceRender();
   assert(window.frames==framesBefore+repeats&&engine.effects==effectsBefore&&engine.requests==requestsBefore);
   if(repeats)assert(window.pixels.back()==resumedPixels);
   for(auto s:{main.get(),final.get(),text.get()})for(auto value:logical(*s))digest(value);
   digest(engine.effects);digest(engine.requests);digest(engine.pauseEvents);digest(engine.pausePrepares);
   assert(openfodder::RasterizeMissionLayers(retained,retainedDestination).pixels==retainedPixels);
   ++transitions;
  }
  engine.pauseEvent=nullptr;
  ++count;
 }
 std::cout<<"PASS: "<<count<<" actual PC/Amiga producer scenarios, repeats="<<repeats<<", "<<frames
          <<(publishing?" recorded presentations;":" classic presentations;")<<" 0/1/5, two destinations, early/late cursor, late sprites/palette, resource release, Clear/Save/Restore, reset and missing-write detection\n";
 std::cout<<"TRANSITIONS: "<<transitions<<" digest="<<transitionDigest<<"\n";
}
