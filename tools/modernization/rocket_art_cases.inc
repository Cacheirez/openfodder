// Actual WindowHD method; two independently selected bodies, ordered occlusion.
const std::string directory=std::getenv("OPENFODDER_ROCKET_ART");
nlohmann::json manifest,input;
{std::ifstream f(directory+"/candidate-manifest.json");f>>manifest;assert(f);}
{std::ifstream f(directory+"/transition-input.json");f>>input;assert(f);}
const auto directions=input.at("directions").get<std::vector<int>>();
assert(manifest["assets"].size()==input.at("assets").get<size_t>() && manifest["bindings"].size()==input.at("bindings").get<size_t>());
struct AimCase {PreparedSpriteDraw p;std::array<uint32_t,255> colors;};
std::map<std::string,std::map<int,AimCase>> groups;
const bool native=input.at("native");
std::string selectedPath=directory+"/candidate-manifest.json";
if(native){
 for(const auto& item:input.at("rows")){
  const auto& row=item.at("row");assert(row.at("animation")==0);
  auto p=LoadNativeWalkSnapshot(row,item.at("directory").get<std::string>());
  p.soldier.faceDirection=row.at("face");p.soldier.direction=row.at("direction");
  const auto colors=row.at("colors").get<std::array<uint32_t,255>>();
  const auto group=row.at("format").dump()+":"+row.at("resource_sha256").get<std::string>()+":"+row.at("colors").dump();
  assert(groups[group].emplace(p.soldier.sheet*3+p.soldier.frame,AimCase{p,colors}).second);
 }
 assert(groups.size()==4);
}else{
 manifest["bindings"]=nlohmann::json::array();
 for(int platform:{0,1})for(int variant:{0,1})for(int pose=0;pose<80;++pose){
  if(pose>=56 && std::find(directions.begin(),directions.end(),(pose-56)/3)==directions.end())continue;
  auto p=soldier(platform==1,0).soldier;
  const auto* data=pose<24?orderedWalkFixture[platform][pose]:pose<32?orderedAimFixture[platform][pose-24]:pose<56?orderedGrenadeFixture[platform][pose-32]:orderedRocketFixture[platform][pose-56];
  auto& s=p.soldier;auto& g=s.geometry;
  s.sheet=data[0];s.frame=data[1];s.personType=variant;s.faceDirection=(pose<24?pose/3:pose<32?pose-24:pose<56?(pose-32)/3:(pose-56)/3)*2;
  p.resource.offset=data[2];g.modX=data[3];g.modY=data[4];g.columns=data[5];g.rows=data[6];p.draw.format=g.format;p.draw.palette=g.palette;
  auto colors=image.scene.destinations[0].initial.indexed.colors;colors[5]^=variant;
  const auto key=SoldierVariantKey(p,colors);
  const auto prefix="s"+std::to_string(s.sheet)+"-f"+std::to_string(s.frame)+"-";
  manifest["bindings"].push_back({{"key",key},{"decision","replace-art"},{"assets",{{"8",prefix+"8"},{"12",prefix+"12"}}}});
  assert(groups[std::to_string(platform)+":"+std::to_string(variant)].emplace(s.sheet*3+s.frame,AimCase{p,colors}).second);
 }
 selectedPath=directory+"/controlled-manifest.json";{std::ofstream f(selectedPath);f<<manifest.dump();assert(f);}
}
const auto registry=OrderedSoldierRegistry::Load(selectedPath);env("OPENFODDER_SOLDIER_ORDERED_MANIFEST",selectedPath.c_str());
size_t steps=0,sequences=0;
const auto& sequencesInput=input.at("sequences");
const size_t sequenceLength=input.at("sequence_length");
for(unsigned density:{8u,12u})for(const auto& group:groups)for(size_t choice=0;choice<sequencesInput.size();++choice){
 const auto sequence=sequencesInput[choice].at("rows").get<std::vector<nlohmann::json>>();
 const auto otherSequence=sequencesInput[(choice+input.at("other_choice_offset").get<size_t>())%sequencesInput.size()].at("rows").get<std::vector<nlohmann::json>>();
 assert(sequence.size()==sequenceLength && otherSequence.size()==sequenceLength);
 bool complete=true;
 for(const auto& r:sequence)complete&=group.second.count(r.at("sheet").get<int>()*3+r.at("frame").get<int>())!=0;
 for(const auto& r:otherSequence)complete&=group.second.count(r.at("sheet").get<int>()*3+r.at("frame").get<int>())!=0;
 if(!complete){assert(native);continue;} // Never synthesize unobserved walking variants.
 ++sequences;
 for(size_t phase=0;phase<sequence.size();++phase){
  const auto& a=sequence[phase];const auto& b=otherSequence[(phase+5)%sequenceLength];
  const auto& firstPose=group.second.at(a.at("sheet").get<int>()*3+a.at("frame").get<int>());
  const auto& secondPose=group.second.at(b.at("sheet").get<int>()*3+b.at("frame").get<int>());
  assert(firstPose.colors==secondPose.colors);
  image.scene.destinations[0].initial.indexed.colors=firstPose.colors;
  auto layer=[&](const AimCase& item,int slot){
   auto result=body;result.soldier=item.p;auto& s=result.soldier.soldier;auto& g=s.geometry;
   s.scene=fodder.mPresentationScene;s.interval=3000+steps;s.slot=slot;s.generation=1;
   g.spriteX=32+slot*4;g.spriteY=20;g.xBias=0;g.viewWidth=96;g.viewHeight=64;g.rowsToSkip=slot?3:0;
   auto geometry=g;geometry.source=result.soldier.resource.source();result.soldier.draw=PrepareSpriteDraw(geometry);
   const auto art=registry.resolve(result.soldier,SoldierVariantKey(result.soldier,item.colors),density);
   assert(art.decision==SoldierArtDecision::Replace);
   if(s.sheet==7 && s.frame==0)checkWalkC01(*art.pixels,density);
   return result;
  };
  auto first=layer(firstPose,0),second=layer(secondPose,1);
  MissionLayer cover;cover.destination=body.destination;
  const size_t covered=(first.soldier.draw.y+9)*96+first.soldier.draw.x+6;
  for(int y=0;y<2;++y)for(int x=0;x<9;++x)cover.pixels.put(covered+y*96+x,5);
  image.scene.layers={first,second,cover};
  const auto composed=ComposeOrderedSoldierArt(image.scene,body.destination,density,[&](const PreparedSpriteDraw& p){return registry.resolve(p,SoldierVariantKey(p,firstPose.colors),density);});
  assert(composed.complete() && composed.replaced==2 && composed.cells.count(covered)==0);
  std::vector<uint32_t> expanded(96*64*density*density);
  for(size_t y=0;y<64*density;++y)for(size_t x=0;x<96*density;++x){size_t n=(y/density)*96+x/density;auto cell=composed.cells.find(n);expanded[y*96*density+x]=cell==composed.cells.end()?composed.background.pixels[n]:cell->second[(y%density)*density+x%density];}
  auto oracle=texture(renderer,expanded,96*density,64*density);SDL_FRect full{0,0,96.f*density,64.f*density};
  clear(renderer);assert(SDL_RenderTexture(renderer,oracle,&full,&dst));auto expected=read(renderer);
  env("OPENFODDER_SOLDIER_HD",std::to_string(density).c_str());clear(renderer);
  assert(win.TryRenderMissionHD(&image,src,dst)==1 && read(renderer)==expected);SDL_DestroyTexture(oracle);++steps;
 }
}
assert(steps==input.at("expected_intervals").get<size_t>() && sequences*sequenceLength==steps);
const auto supported=image.scene;
for(int missing=0;missing<3;++missing){
 image.scene=supported;
 // One unsupported body must reject the whole interval without a partial publication.
 auto& p=image.scene.layers[1].soldier;
 for(auto& l:image.scene.layers)if(l.operation==MissionLayerOperation::Soldier)l.soldier.soldier.interval=5000+missing;
 if(missing==0)p.soldier.type=5;
 if(missing==1)p.soldier.animation=0x32;
 if(missing==2)image.scene.destinations[0].initial.indexed.colors[5]^=1;
 clear(renderer);auto before=read(renderer);assert(win.TryRenderMissionHD(&image,src,dst)==-1 && read(renderer)==before);
}
env("OPENFODDER_SOLDIER_ORDERED_MANIFEST","");
if(!native)std::remove(selectedPath.c_str());
std::cout<<"PASS rocket transition "<<(native?"real-source":"controlled")<<": "<<steps<<" intervals; "<<sequences<<" sequences; two independently selected soldiers; option A and C01 alpha; three rejection cases\n";
