// GPL-3.0-or-later. Owned native background plus one precomposited HD patch.
#pragma once
#include "SoldierArtHD.hpp"
namespace openfodder {
struct SoldierArtHDLayers {
    PresentationTarget background; // native size; exact classic on fallback
    std::vector<uint32_t> patch; // replacement pixels, NOT a second alpha blend
    SoldierArtHDStatus status = SoldierArtHDStatus::ClassicGuard;
    unsigned density = 1;
    int logicalX = 0, logicalY = 0;
    uint64_t scene = 0;
};
// Independent from the full-output oracle's budget: only HD patch bytes.
// The native background and retained commands are additional memory.
inline SoldierArtHDLayers ComposeSoldierArtHDLayers(const MissionLayerSequence& scene,
        const PresentationDestinationId& destination, bool paletteStable,
        const SoldierArtHDAsset& asset, size_t maxPatchBytes=129024) {
    SoldierArtHDLayers out;
    out.background=RasterizeMissionLayers(scene,destination);
    const unsigned d=asset.density;
    if(d!=1 && d!=8 && d!=12){out.status=SoldierArtHDStatus::UnsupportedDensity;return out;}
    if(!asset.pixels || asset.pixels->size()!=size_t(224)*d*d){
        out.status=SoldierArtHDStatus::MissingAsset;return out;
    }
    if(out.background.stride!=out.background.width){
        out.status=SoldierArtHDStatus::UnsupportedPitch;return out;
    }
    if(size_t(224)*d*d>maxPatchBytes/sizeof(uint32_t)){
        out.status=SoldierArtHDStatus::BudgetExceeded;return out;
    }
    const std::array<uint32_t,224> transparent{};
    auto ground=ComposeSoldierArt(scene,destination,paletteStable,&transparent);
    if(!ground.replaced)return out;
    out.patch.resize(size_t(224)*d*d);
    for(size_t y=0;y<14*d;++y)for(size_t x=0;x<16*d;++x){
        const uint32_t src=(*asset.pixels)[y*16*d+x];const unsigned alpha=src>>24;
        const uint32_t bg=ground.target.pixels[(size_t(ground.y)+y/d)*ground.target.width+size_t(ground.x)+x/d];
        uint32_t rgb=bg&0xff000000u;
        for(unsigned shift:{0u,8u,16u})
            rgb|=((((src>>shift)&255)*alpha+((bg>>shift)&255)*(255-alpha)+127)/255)<<shift;
        out.patch[y*16*d+x]=rgb;
    }
    out.background=std::move(ground.target);out.status=SoldierArtHDStatus::Replaced;
    out.density=d;out.logicalX=ground.x;out.logicalY=ground.y;out.scene=ground.scene;
    return out;
}
} // namespace openfodder
