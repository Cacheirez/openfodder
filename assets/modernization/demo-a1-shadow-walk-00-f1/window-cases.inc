// Focused Window/SDL checks for one exact ordinary key, not a new engine path.
const std::string root=std::getenv("OPENFODDER_A1_RANK_F4");
nlohmann::json row;{std::ifstream f(root+"/native.json");f>>row;assert(f);}
const auto colors=row.at("colors").get<std::array<uint32_t,255>>();
image.scene.destinations[0].initial.indexed.colors=colors;
const auto nativeData=std::getenv("OPENFODDER_NATIVE_SNAPSHOTS");
const auto manifest=root+"/candidate/candidate-manifest.json";
const auto registry=OrderedSoldierRegistry::Load(manifest);
const auto originalRegistry=OrderedSoldierRegistry::Load(root+"/original-candidate/candidate-manifest.json");
env("OPENFODDER_SOLDIER_ORDERED_MANIFEST",manifest.c_str());
auto first=body;first.soldier=LoadNativeWalkSnapshot(row,nativeData);
auto prepare=[](PreparedSpriteDraw& p){auto g=p.soldier.geometry;g.source=p.resource.source();p.draw=PrepareSpriteDraw(g);};
auto& state=first.soldier.soldier;state.scene=fodder.mPresentationScene;state.interval=1;state.generation=1;
state.geometry.spriteX=32;state.geometry.spriteY=20;state.geometry.xBias=0;state.geometry.viewWidth=64;state.geometry.viewHeight=31;prepare(first.soldier);
assert(SoldierVariantKey(first.soldier,colors)==row.at("key"));
auto second=first;second.soldier.soldier.slot=1;second.soldier.soldier.geometry.spriteX+=4;prepare(second.soldier);
for(unsigned d:{8u,12u})for(const char* hybrid:{"0","1"}){
 env("OPENFODDER_SOLDIER_HD",std::to_string(d).c_str());env("OPENFODDER_SOLDIER_ORDERED_HYBRID",hybrid);
 for(int variant=0;variant<7;++variant){
  auto a=first,b=second;
  MissionLayer cover;cover.destination=body.destination;
  const size_t target=(a.soldier.draw.y+12)*96+a.soldier.draw.x+10;
  cover.pixels.put(target,0);
  if(variant==3){a.soldier.soldier.geometry.spriteX=84;prepare(a.soldier);}
  if(variant==4){a.soldier.soldier.geometry.spriteY=50;prepare(a.soldier);}
  if(variant==6){a.soldier.soldier.geometry.rowsToSkip=3;b.soldier.soldier.geometry.rowsToSkip=3;prepare(a.soldier);prepare(b.soldier);}
  image.scene.layers={a,b};
  if(variant==1)image.scene.layers.push_back(cover);
  if(variant==2)image.scene.layers={cover,a,b};
  if(variant==5){MissionLayer save,restore;save.destination=restore.destination=body.destination;save.operation=MissionLayerOperation::Save;restore.operation=MissionLayerOperation::Restore;image.scene.layers={a,b,save,cover,restore};}
  std::cout<<"CASE "<<d<<" "<<hybrid<<" "<<variant<<std::endl;
  const auto nativeClassic=RasterizeMissionLayers(image.scene,body.destination);
  const auto resolve=[&](const PreparedSpriteDraw& p){return registry.resolve(p,SoldierVariantKey(p,colors),d);};
  const auto frame=ComposeOrderedSoldierArt(image.scene,body.destination,d,resolve);
  assert(frame.complete()&&frame.replaced==2&&!frame.cells.empty());
  const auto before=ComposeOrderedSoldierArt(image.scene,body.destination,d,[&](const PreparedSpriteDraw& p){return originalRegistry.resolve(p,SoldierVariantKey(p,colors),d);});
  assert(before.complete());
  if(variant==0)assert(frame.cells!=before.cells); // actual visible ground shadow
  if(variant==6)assert(frame.cells==before.cells); // rows 11-13 omitted: no retained shadow in water crop
  if(variant==1)assert(!frame.cells.count(target));
  std::vector<uint32_t> expanded(96*64*d*d);
  for(size_t y=0;y<64*d;++y)for(size_t x=0;x<96*d;++x){const size_t n=(y/d)*96+x/d;const auto cell=frame.cells.find(n);expanded[y*96*d+x]=cell==frame.cells.end()?frame.background.pixels[n]:cell->second[(y%d)*d+x%d];}
  auto oracle=texture(renderer,expanded,96*d,64*d);SDL_FRect full{0,0,96.f*d,64.f*d};clear(renderer);assert(SDL_RenderTexture(renderer,oracle,&full,&dst));const auto expected=read(renderer);SDL_DestroyTexture(oracle);
  assert(SDL_UpdateTexture(image.tex,nullptr,nativeClassic.pixels.data(),96*4));clear(renderer);assert(SDL_RenderTexture(renderer,image.tex,&src,&dst));const auto classicPixels=read(renderer);
  clear(renderer);callNumber=0;assert(win.TryRenderMissionHD(&image,src,dst)==1&&read(renderer)==expected);
  const int calls=callNumber;clear(renderer);callNumber=0;failAt=calls;assert(win.TryRenderMissionHD(&image,src,dst)==1&&read(renderer)==classicPixels&&live==0);failAt=0;
  env("OPENFODDER_SOLDIER_HD","0");assert(win.TryRenderMissionHD(&image,src,dst)==-1);env("OPENFODDER_SOLDIER_HD",std::to_string(d).c_str());
  std::cout<<"PASS shadow walk: density "<<d<<" hybrid "<<hybrid<<" case "<<variant<<"; exact SDL, full recovery, classic independent\n";
 }
 // State changes must not inherit the corrected walk or its embedded shadow.
 for(int sheet:{0x28,0x2d,0xb0,0x18,0x9e,0x97}){auto changed=first.soldier;changed.soldier.sheet=sheet;assert(registry.resolve(changed,SoldierVariantKey(changed,colors),d).decision==SoldierArtDecision::Missing);}
 auto wrong=first.soldier;wrong.soldier.animation=1;assert(registry.resolve(wrong,SoldierVariantKey(wrong,colors),d).decision==SoldierArtDecision::Missing);
 std::cout<<"PASS pilot scope: damage, fall, water, death, independent shadow and animation changes excluded\n";
}
