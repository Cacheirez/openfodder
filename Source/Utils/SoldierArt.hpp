// GPL-3.0-or-later. Bounded RGBA pose pilot, after mandatory classic contrast.
#pragma once
#include "MissionLayers.hpp"
#include "SoldierArtPixels.hpp"
namespace openfodder {
struct SoldierArtResult {
    PresentationTarget target;
    bool replaced = false;
    uint64_t scene = 0;
    int x = 0, y = 0;
};
inline bool SoldierArtEligible(const PreparedSpriteDraw& p) {
    size_t w=0,h=0;
    const auto& s=p.soldier;const auto& g=s.geometry;
    // Actual PC stru_330FC[0] / Amiga stru_8C4A8[0], 16x14, modX=modY=0.
    return SoldierPoseGeometry(p,w,h) && w==16 && h==14 && s.type==0 &&
        s.sheet==7 && s.frame==0 && s.animation==0 && g.rowsToSkip==0 &&
        g.modX==0 && g.modY==0 && g.rows==14 &&
        ((g.format==SpriteDrawFormat::PC && p.resource.offset==2248 && g.columns==16) ||
         (g.format==SpriteDrawFormat::Amiga8 && p.resource.offset==562 && g.columns==2));
}
inline bool SoldierArtTouches(size_t offset,size_t stride,int x,int y) {
    return offset/stride>=size_t(y) && offset/stride<size_t(y+14) &&
           offset%stride>=size_t(x) && offset%stride<size_t(x+16);
}
// Conservative ordering policy: if ANY later command can touch this body,
// keep the classic body. Never draw a new body over a cursor, HUD or occluder.
inline bool SoldierArtLaterOverlap(const MissionLayerSequence& scene,size_t selected,size_t width) {
    const auto& chosen=scene.layers[selected];int x=chosen.soldier.draw.x,y=chosen.soldier.draw.y;
    for(size_t i=selected+1;i<scene.layers.size();++i){
        const auto& l=scene.layers[i];if(l.destination!=chosen.destination)continue;
        switch(l.operation){
        case MissionLayerOperation::Pixels:
            for(const auto& write:l.pixels.writes)
                if(write.offset<0 || SoldierArtTouches(size_t(write.offset),width,x,y))return true;
            break;
        case MissionLayerOperation::Sidebar:
            for(size_t row=0;row<l.sidebar.rows;++row)for(size_t col=0;col<48;++col)
                if(SoldierArtTouches(l.sidebar.destinationOffset+row*l.sidebar.destinationStride+col,width,x,y))return true;
            break;
        case MissionLayerOperation::Soldier: {
            const auto& d=l.soldier.draw;
            int columns=d.format==SpriteDrawFormat::PC?(d.columns/2)*2:(d.columns-1)*16;
            if(d.x<x+16 && d.x+columns>x && d.y<y+14 && d.y+d.rows>y)return true;
            break;
        }
        default: return true; // terrain, Save, Restore, Clear: retained classic fallback
        }
    }
    return false;
}
inline SoldierArtResult ComposeSoldierArt(const MissionLayerSequence& scene,
        const PresentationDestinationId& destination,bool paletteStable,
        const std::array<uint32_t,224>* asset=&SoldierArtPixels()) {
    SoldierArtResult result;
    result.target=RasterizeMissionLayers(scene,destination); // pure reference; no simulation
    if(!paletteStable || !asset)return result;
    size_t slot=0;while(slot<scene.destinations.size() && scene.destinations[slot].initial.destination!=destination)++slot;
    if(slot==scene.destinations.size())return result;
    const auto& surface=scene.destinations[slot].initial;
    const size_t width=surface.indexed.width,height=surface.indexed.height;
    // Indexed conversion uses packed rows, including padded SDL backing.
    for(size_t i=0;i<scene.layers.size();++i){
        const auto& l=scene.layers[i];if(l.destination!=destination || l.operation!=MissionLayerOperation::Soldier || !SoldierArtEligible(l.soldier))continue;
        // A repeated body of the same actor earlier in this interval is not
        // background. Do not expose its pixels through the new alpha margin.
        bool repeated=false;
        for(size_t prior=0;prior<i;++prior){
            const auto& old=scene.layers[prior];
            if(old.destination==destination && old.operation==MissionLayerOperation::Soldier &&
               old.soldier.soldier.scene==l.soldier.soldier.scene &&
               old.soldier.soldier.slot==l.soldier.soldier.slot &&
               old.soldier.soldier.generation==l.soldier.soldier.generation) repeated=true;
        }
        if(repeated)continue;
        int x=l.soldier.draw.x,y=l.soldier.draw.y;
        if(x<surface.indexed.skipX || y<surface.indexed.skipY || size_t(x)+16>width || size_t(y)+14>height ||
           SoldierArtLaterOverlap(scene,i,width))continue;
        // Remove only this original body before drawing RGBA. Its old opaque
        // pixels must not survive behind the new transparent margins.
        auto without=scene;without.layers.erase(without.layers.begin()+i);
        auto modern=RasterizeMissionLayers(without,destination);
        for(size_t py=0;py<14;++py)for(size_t px=0;px<16;++px){
            const uint32_t source=(*asset)[py*16+px];unsigned alpha=source>>24;
            auto& target=modern.pixels[(size_t(y)+py)*width+size_t(x)+px];
            uint32_t rgb=0;
            for(unsigned shift:{0u,8u,16u}){
                const unsigned a=(source>>shift)&255,b=(target>>shift)&255;
                rgb|=((a*alpha+b*(255-alpha)+127)/255)<<shift;
            }
            target=(target&0xFF000000u)|rgb;
        }
        // Differences are authorized only inside the removed body's rectangle.
        for(size_t n=0;n<modern.pixels.size();++n)
            if(!SoldierArtTouches(n,width,x,y) && modern.pixels[n]!=result.target.pixels[n])
                throw std::runtime_error("soldier art changed pixels outside its permitted body");
        result.target=std::move(modern);result.replaced=true;result.scene=l.soldier.soldier.scene;result.x=x;result.y=y;
        return result; // exactly one command at most
    }
    return result;
}
} // namespace openfodder
