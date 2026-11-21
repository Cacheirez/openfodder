using namespace openfodder;
int main(){
 int cases=0;
 for(bool amiga:{false,true})for(int padding:{0,3})for(int shift:{0,5}){
  pad=padding;cSurface a(96,64);fill(a,3,false);a.mPaletteAdjusting=false;
  // Real Begin / Record / Verify / Publish adapters, synthetic original bytes.
  a.BeginMissionAudit(nullptr,true);
  PreparedSpriteDraw p;p.resource.bytes=std::make_shared<const std::vector<uint8_t>>(32768,0x51);
  p.resource.offset=amiga?562:2248;p.resource.layout={amiga?SpriteDrawFormat::Amiga8:SpriteDrawFormat::PC,320,32,4};
  p.soldier.valid=true;p.soldier.scene=1;p.soldier.generation=2;p.soldier.interval=3;
  p.soldier.sheet=7;auto& g=p.soldier.geometry;
  g.format=p.resource.layout.format;g.columns=amiga?2:16;g.rows=14;g.spriteX=shift;g.spriteY=30+shift;
  auto input=g;input.source=p.resource.source();p.draw=PrepareSpriteDraw(input);
  a.RecordMissionSoldier(p);RasterizeSprite8(p.draw,p.resource.layout,{a.GetSurfaceBuffer(),a.GetWidth()});
  const auto logicalBefore=logical(a);
  PresentationTarget actual;auto scene=a.VerifyMissionAudit(nullptr,&actual);
  const auto classic=RasterizeMissionLayers(scene,a.mPresentationDestination);
  const auto art=ComposeSoldierArt(scene,a.mPresentationDestination,true);
  assert(art.replaced && actual.pixels==art.target.pixels && classic.pixels!=actual.pixels);
  assert(art.x==64+shift && art.y==32+shift); // unchanged original (0,14) anchor
  for(size_t n=0;n<actual.pixels.size();++n)
   if(!SoldierArtTouches(n,96,art.x,art.y))assert(actual.pixels[n]==classic.pixels[n]);
  for(int n:{0,1,5}){for(int i=0;i<n;++i)assert(a.PresentRecordedMission(nullptr));assert(logical(a)==logicalBefore);}
  assert(!ComposeSoldierArt(scene,a.mPresentationDestination,false).replaced);
  assert(!ComposeSoldierArt(scene,a.mPresentationDestination,true,nullptr).replaced);
  // Alpha 0 exposes the underlying scene, not remnants of the old soldier.
  std::array<uint32_t,224> transparent{};
  auto removed=scene;removed.layers.clear();
  assert(ComposeSoldierArt(scene,a.mPresentationDestination,true,&transparent).target.pixels==RasterizeMissionLayers(removed,a.mPresentationDestination).pixels);
  auto duplicate=scene;duplicate.layers.push_back(duplicate.layers[0]);
  assert(!ComposeSoldierArt(duplicate,a.mPresentationDestination,true).replaced);
  for(int guard=0;guard<8;++guard){
   auto blocked=scene;
   if(guard==0)++blocked.layers[0].soldier.soldier.frame;
   if(guard==1)++blocked.layers[0].soldier.soldier.sheet;
   if(guard==2)blocked.layers[0].soldier.soldier.animation=1;
   if(guard==3)blocked.layers[0].soldier.resource.offset++;
   if(guard>=4){MissionLayer l;l.destination=a.mPresentationDestination;
    if(guard==4)l.pixels.put(size_t(art.y)*96+art.x,0); // even zero / same-color writes occlude
    if(guard==5)l.pixels.addBits(size_t(art.y)*96+art.x,0);
    if(guard==6)l.operation=MissionLayerOperation::Save;
    if(guard==7)l.operation=MissionLayerOperation::Restore;
    blocked.layers.push_back(l);
   }
   const auto fallback=ComposeSoldierArt(blocked,a.mPresentationDestination,true);
   assert(!fallback.replaced && fallback.target.pixels==RasterizeMissionLayers(blocked,a.mPresentationDestination).pixels);++cases;
  }
  // Geometry mismatch and unrecorded engine write still fail the original oracle.
  a.GetSurfaceBuffer()[0]^=1;bool rejected=false;
  try{a.VerifyMissionAudit(nullptr);}catch(const std::runtime_error&){rejected=true;}assert(rejected);a.GetSurfaceBuffer()[0]^=1;
  a.BeginMissionAudit(nullptr,false);assert(!a.PresentRecordedMission(nullptr));
  assert(ComposeSoldierArt(scene,a.mPresentationDestination,true).target.pixels==art.target.pixels);
  p.resource={};assert(ComposeSoldierArt(scene,a.mPresentationDestination,true).replaced);
 }
 std::cout<<"PASS C01: "<<cases<<" fallback cases; actual surface hooks, PC/Amiga anchor, alpha, pitch, camera, 0/1/5, pause invalidation, retained resources, original oracle\n";
}
