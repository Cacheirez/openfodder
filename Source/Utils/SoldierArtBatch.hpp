// GPL-3.0-or-later. Six explicit keys; immutable derivatives of preserved masters.
#pragma once
#include "SoldierArtHD.hpp"
#include "c01_8.hpp"
#include "c01_12.hpp"
#include "pilot_2_0_8.hpp"
#include "pilot_2_0_12.hpp"
#include "pilot_2_1_8.hpp"
#include "pilot_2_1_12.hpp"
#include "pilot_2_2_8.hpp"
#include "pilot_2_2_12.hpp"
#include "pilot_7_1_8.hpp"
#include "pilot_7_1_12.hpp"
#include "pilot_7_2_8.hpp"
#include "pilot_7_2_12.hpp"
namespace openfodder {
template<size_t N> inline std::shared_ptr<const std::vector<uint32_t>> OwnSoldierPixels(const std::array<uint32_t,N>& p){
 return std::make_shared<const std::vector<uint32_t>>(p.begin(),p.end());
}
inline SoldierArtHDAsset SoldierBatchAsset(int sheet,int frame,unsigned density){
 SoldierArtHDAsset out;out.sheet=sheet;out.frame=frame;out.density=density;
 if((sheet!=2&&sheet!=7)||frame<0||frame>2||(density!=8&&density!=12))return out;
 static const std::shared_ptr<const std::vector<uint32_t>> pixels[2][6]={
  {OwnSoldierPixels(Pilot2_0_8()),OwnSoldierPixels(Pilot2_1_8()),OwnSoldierPixels(Pilot2_2_8()),OwnSoldierPixels(SoldierArtPixels8()),OwnSoldierPixels(Pilot7_1_8()),OwnSoldierPixels(Pilot7_2_8())},
  {OwnSoldierPixels(Pilot2_0_12()),OwnSoldierPixels(Pilot2_1_12()),OwnSoldierPixels(Pilot2_2_12()),OwnSoldierPixels(SoldierArtPixels12()),OwnSoldierPixels(Pilot7_1_12()),OwnSoldierPixels(Pilot7_2_12())}};
 out.pixels=pixels[density==12?1:0][(sheet==2?0:3)+frame];return out;
}
inline SoldierArtHDAsset SelectSoldierBatch(const MissionLayerSequence& scene,const PresentationDestinationId& id,unsigned density){
 for(const auto& l:scene.layers){
  const auto& s=l.soldier.soldier;
  if(l.destination==id&&l.operation==MissionLayerOperation::Soldier&&SoldierArtEligible(l.soldier,s.sheet,s.frame))
   return SoldierBatchAsset(s.sheet,s.frame,density);
 }
 SoldierArtHDAsset out;out.density=density;return out;
}
}
