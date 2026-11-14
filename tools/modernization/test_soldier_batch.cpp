// GPL-3.0-or-later. Reuse the original oracle and scene fixtures.
#define main OriginalC01Contract
#include "test_soldier_art_hd.cpp"
#undef main
#include "Utils/SoldierArtBatch.hpp"
int main(){
 for(bool amiga:{false,true})for(unsigned density:{8u,12u})for(int sheet:{2,7})for(int frame:{0,1,2}){
  MissionLayerSequence scene;scene.destinations={destination(96,64)};
  auto id=scene.destinations[0].initial.destination;auto l=soldier(amiga,0);l.destination=id;
  l.soldier.soldier.sheet=sheet;l.soldier.soldier.frame=frame;
  l.soldier.resource.offset=(amiga?(sheet==2?12:562):(sheet==2?48:2248))+frame*(amiga?2:8);
  scene.layers={l};auto a=SelectSoldierBatch(scene,id,density);
  assert(a.pixels && a.sheet==sheet && a.frame==frame);
  checkLayers(scene,id,a);auto result=ComposeSoldierArtHDLayers(scene,id,true,a);
  assert(result.status==SoldierArtHDStatus::Replaced);
  auto wrong=a;wrong.frame=(frame+1)%3;
  assert(ComposeSoldierArtHDLayers(scene,id,true,wrong).status!=SoldierArtHDStatus::Replaced);
  auto blocked=scene;blocked.layers[0].soldier.resource.offset++;
  assert(!SelectSoldierBatch(blocked,id,density).pixels);
  blocked=scene;blocked.layers[0].soldier.soldier.animation=1;
  assert(!SelectSoldierBatch(blocked,id,density).pixels);
  blocked=scene;blocked.layers[0].soldier.soldier.sheet=3;
  assert(!SelectSoldierBatch(blocked,id,density).pixels);
  blocked=scene;blocked.layers.push_back(l);fallback(blocked,id,a);
  blocked=scene;MissionLayer late;late.destination=id;late.pixels.put(32*96+64,5);blocked.layers.push_back(late);fallback(blocked,id,a);
  fallback(scene,id,a,false);
 }
 assert(!SoldierBatchAsset(7,3,12).pixels && !SoldierBatchAsset(3,0,12).pixels);
 assert(!SoldierBatchAsset(2,0,4).pixels);
 std::cout<<"PASS batch: 24 key/platform/density combinations, wrong key/resource/animation, repeated actor, overlap, palette, full/layered equality\n";
}
