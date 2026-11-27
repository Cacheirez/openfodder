// GPL-3.0-or-later. Internal ordered compositor; not yet the SDL publication path.
#pragma once
#include "MissionLayers.hpp"
#include <map>
#include <functional>
namespace openfodder {
// A resolver must match the complete retained resource/variant key, not just a
// sheet number. KeepClassic is an explicit native classification; only the
// resolver can authorize it for a verified resource.
enum class SoldierArtDecision { Replace, KeepClassic, Missing };
// Optional presentation-only ground component, emitted in the body's turn.
// Coordinates are screen-space quarters, independent of the actor's facing.
struct OrderedSoldierGroundShadow {
    size_t width = 0, height = 0;
    unsigned density = 1;
    int xQuarters = 0, yQuarters = 0, ownerType = 0;
    std::shared_ptr<const std::vector<uint32_t>> pixels;
};
struct OrderedSoldierAsset {
    SoldierArtDecision decision = SoldierArtDecision::Missing;
    size_t width = 0, height = 0;
    unsigned density = 1;
    std::shared_ptr<const std::vector<uint32_t>> pixels;
    OrderedSoldierGroundShadow groundShadow;
};
inline bool OrderedGroundShadowEligible(const PreparedSpriteDraw& p,int ownerType) {
    const auto& s=p.soldier;const auto& g=s.geometry;
    const bool normal=s.type==0 ? ((s.sheet>=0 && s.sheet<=23) || (s.sheet>=57 && s.sheet<=64))
        : (s.type==5 && s.sheet>=0x42 && s.sheet<=0x59) ||
          (s.type==36 && s.sheet>=0xa8 && s.sheet<=0xaf && s.frame==2);
    // Native 38/9f contain a planted ground tail; A4 is the verified sliding
    // body with embedded ground, selected by the three native slide states.
    const bool celebration=s.type==0 && (s.sheet==0x38 || s.sheet==0x9f) && s.animation==0;
    const bool slide=s.type==0 && s.sheet==0xa4 && (s.animation==50 || s.animation==51 || s.animation==52);
    const bool enemySlide=(s.type==5 || s.type==36) && s.personType==1 && s.sheet==0xa7 &&
        (s.animation==50 || s.animation==51 || s.animation==52);
    const bool initialEnemySlide=s.type==5 && s.personType==0 && s.sheet==0xa4 &&
        (s.animation==50 || s.animation==51 || s.animation==52);
    // The shared Slide2 controller selects the AI low-aim table (offset0x30)
    // before clearing animation51 on the following update. Preserve that
    // planted body phase for both infantry and rocket enemies.
    const bool enemyAim=(s.type==5 || s.type==36) && s.sheet>=0x52 && s.sheet<=0x59 &&
        (s.animation==0 || s.animation==51);
    // Before its first AI update, type5 can leave Slide2 using the human aim
    // table. That path bypasses generic independent-shadow creation.
    const bool initialEnemyAim=s.type==5 && s.personType==0 && s.sheet>=0x10 && s.sheet<=0x17 &&
        (s.animation==0 || s.animation==51);
    // The follower's PC idle has an embedded down-right ground tail. Its
    // audited Amiga resource is empty; never attach a visible component there.
    const bool enemyGuard=s.type==5 && s.personType==1 && s.sheet==0xdc && s.frame==0 &&
        s.animation==0 && g.format==SpriteDrawFormat::PC;
    // Audited leader body/contact resources are PC-only; Amiga commands are
    // signed empty. DA is a three-frame resting head turn, not eight directions.
    const bool enemyLeader=s.type==106 && s.personType==2 && s.animation==0 &&
        g.format==SpriteDrawFormat::PC && s.frame>=0 &&
        (((s.sheet==0xd8 || s.sheet==0xd9) && s.frame<24) || (s.sheet==0xda && s.frame<3));
    return (ownerType==0 || ownerType==5 || ownerType==36 || ownerType==106) && s.type==ownerType &&
        ((normal && s.animation==0) || celebration || slide || enemySlide || initialEnemySlide || enemyAim || initialEnemyAim || enemyGuard || enemyLeader) &&
        !s.inVehicle && !s.pendingDestroy && g.height==0 && g.rowsToSkip==0;
}
struct SoldierArtObservation {
    size_t order = 0;
    PreparedSpriteDraw command; // Owns bytes and identity; no borrowed source.
    SoldierArtDecision decision = SoldierArtDecision::Missing;
};
struct OrderedSoldierFrame {
    PresentationTarget background;
    // Disjoint native cells containing precomposited d*d HD pixels. Later writes
    // remove cells even if they write the SAME index/color as the background.
    std::map<size_t,std::vector<uint32_t>> cells;
    std::vector<SoldierArtObservation> observations;
    unsigned density = 1;
    size_t replaced = 0, missing = 0, kept = 0;
    bool complete() const { return replaced != 0 && missing == 0; }
};
inline uint32_t SoldierBlend(uint32_t src,uint32_t dst) {
    const unsigned alpha=src>>24;uint32_t out=dst&0xff000000u;
    for(unsigned shift:{0u,8u,16u})
        out|=(( ((src>>shift)&255)*alpha+((dst>>shift)&255)*(255-alpha)+127)/255)<<shift;
    return out;
}
// The native pause producer merges nonzero RGB text after its indexed mission.
// Apply that same final operation to the background and erase covered HD cells.
inline void ApplyOrderedPauseText(OrderedSoldierFrame& frame,const PresentationTarget& text) {
    auto& bg=frame.background;
    if(text.width!=bg.width || text.height!=bg.height || text.stride!=bg.stride ||
       text.pixels.size()!=bg.pixels.size())throw std::invalid_argument("ordered pause text geometry");
    for(size_t i=0;i<text.pixels.size();++i)if(text.pixels[i]){
        bg.pixels[i]=text.pixels[i];frame.cells.erase(i);
    }
}
// CPU reference for A2. Original indexed composition is independently executed
// first. Modern indices omit replaced bodies; ordered HD cells survive Save and
// Restore. No sorting by entity, no new animation clock, no simulation writes.
inline OrderedSoldierFrame ComposeOrderedSoldierArt(const MissionLayerSequence& scene,
        const PresentationDestinationId& id,unsigned density,
        const std::function<OrderedSoldierAsset(const PreparedSpriteDraw&)>& resolve,
        size_t maxCellBytes=64u*1024u*1024u) {
    OrderedSoldierFrame out;
    out.background=RasterizeMissionLayers(scene,id); // independent classic validation
    if(density!=1 && density!=8 && density!=12)throw std::invalid_argument("ordered art density");
    const MissionLayerDestination* destination=nullptr;
    for(const auto& d:scene.destinations)if(d.initial.destination==id)destination=&d;
    if(!destination)throw std::invalid_argument("ordered art destination");
    auto surface=destination->initial;
    const auto w=surface.indexed.width,h=surface.indexed.height;
    if(surface.backing.stride!=w || surface.backing.width!=w || surface.backing.height!=h ||
       surface.indexed.indices->size()!=w*h)throw std::invalid_argument("ordered art extents/pitch");
    auto indices=*surface.indexed.indices,saved=*destination->saved.pixels;
    std::map<size_t,std::vector<uint32_t>> savedCells;
    out.density=density;
    auto color=[&](size_t n){const auto v=indices[n];return v && v<surface.indexed.colors.size()?surface.indexed.colors[v]:0u;};
    auto visible=[&](size_t n){return n/w>=size_t(surface.indexed.skipY)&&n%w>=size_t(surface.indexed.skipX);};
    auto budget=[&](size_t active,size_t savedCount){
        const size_t limit=maxCellBytes/(sizeof(uint32_t)*density*density);
        if(active>limit || savedCount>limit-active)throw std::length_error("ordered art cell budget");
    };
    auto write=[&](const IndexedWrite& v){
        if(v.offset<0 || size_t(v.offset)>=indices.size())throw std::out_of_range("ordered art write");
        auto& index=indices[size_t(v.offset)];
        index=v.bitwiseOr?uint8_t(index|v.value):v.value;
        out.cells.erase(size_t(v.offset));
    };
    for(size_t order=0;order<scene.layers.size();++order){
        const auto& l=scene.layers[order];if(l.destination!=id)continue;
        if(l.operation==MissionLayerOperation::Save){budget(out.cells.size(),out.cells.size());saved=indices;savedCells=out.cells;continue;}
        if(l.operation==MissionLayerOperation::Restore){budget(savedCells.size(),savedCells.size());indices=saved;out.cells=savedCells;continue;}
        if(l.operation==MissionLayerOperation::Clear){
            std::fill(indices.begin(),indices.end(),l.clearIndex);saved=indices;
            out.cells.clear();savedCells.clear();continue;
        }
        if(l.operation==MissionLayerOperation::Pixels){for(const auto& v:l.pixels.writes)write(v);continue;}
        if(l.operation==MissionLayerOperation::Sidebar){
            for(size_t y=0;y<l.sidebar.rows;++y)for(size_t x=0;x<48;++x)
                write({ptrdiff_t(l.sidebar.destinationOffset+y*l.sidebar.destinationStride+x),(*l.sidebar.pixels)[y*48+x],false});
            continue;
        }
        if(l.operation==MissionLayerOperation::Terrain){
            // Two distinct sentinels reveal writes of zero AND same-color writes;
            // comparing the result with the old image alone loses occlusions.
            std::vector<uint8_t> a(w*h,0),b(w*h,255);
            RasterizeTerrain(l.terrain,a.data(),w,a.size());RasterizeTerrain(l.terrain,b.data(),w,b.size());
            for(size_t n=0;n<a.size();++n)if(a[n]==b[n])write({ptrdiff_t(n),a[n],false});
            continue;
        }
        const auto& p=l.soldier;auto a=resolve(p);
        // An independently retained native shadow owns its original draw turn.
        // Do not duplicate it with the optional component in the body's turn.
        if(a.groundShadow.pixels)for(const auto& other:scene.layers){
            if(other.destination!=id || other.operation!=MissionLayerOperation::Soldier)continue;
            const auto& n=other.soldier.nativeAmiga8;
            if(n.cf1 && (n.role==3 || n.role==4) && n.scene==p.soldier.scene && n.ownerType==p.soldier.type &&
               (n.role==4 || n.ownerPerson==p.soldier.personType) && n.ownerGeneration &&
               n.ownerGeneration==p.soldier.generation && n.ownerSlot==p.soldier.slot){
                a.groundShadow=OrderedSoldierGroundShadow{};break;
            }
        }
        out.observations.push_back({order,p,a.decision});
        out.observations.back().command.draw.source=nullptr;
        if(a.decision!=SoldierArtDecision::Replace){
            if(a.decision==SoldierArtDecision::Missing)++out.missing;else ++out.kept;
            auto draw=p.draw;draw.source=p.resource.source();
            for(const auto& v:CaptureSprite8Producer(draw,p.resource.layout,w).writes)write(v);
            continue;
        }
        const auto& g=p.soldier.geometry;const auto& d=p.draw;
        const bool pc=d.format==SpriteDrawFormat::PC;
        const size_t stride=pc?160:p.resource.layout.width/8;
        const size_t factor=pc?2:8;
        const int width=pc?(g.columns/2)*2:(g.columns-1)*16;
        const auto regs=PrepareSpriteRasterRegisters(d,p.resource.layout,w);
        if((d.format!=SpriteDrawFormat::PC && d.format!=SpriteDrawFormat::Amiga8) ||
           !stride || d.sourceOffset<0 || width<=0 || g.rows<=0 || a.width!=size_t(width) ||
           a.height!=size_t(g.rows) || a.width>352 || a.height>272 || a.density!=density ||
           !a.pixels || a.pixels->size()!=a.width*a.height*density*density)
            throw std::invalid_argument("ordered art asset/geometry mismatch");
        const size_t cropY=size_t(d.sourceOffset)/stride,cropX=(size_t(d.sourceOffset)%stride)*factor;
        const size_t columns=size_t(regs.columns)*factor;
        if(cropX+columns>a.width || cropY+size_t(d.rows)>a.height || d.rows<=0 || d.y<0 ||
           size_t(d.y)+size_t(d.rows)>h || (pc && (d.x<0 || size_t(d.x)+columns>w)))
            throw std::out_of_range("ordered art clipped geometry");
        // Amiga's word-oriented clipper can leave pixels across a row edge.
        // The native renderer addresses the backing store linearly in that case.
        const auto start=std::ptrdiff_t(w)*d.y+d.x;
        const auto end=start+std::ptrdiff_t(w)*(d.rows-1)+std::ptrdiff_t(columns);
        if(start<0 || end>std::ptrdiff_t(indices.size()))
            throw std::out_of_range("ordered art clipped geometry");
        if(a.groundShadow.pixels){
            const auto& shadow=a.groundShadow;
            if((density!=8 && density!=12) || shadow.density!=density || !shadow.width || !shadow.height ||
               shadow.width>64 || shadow.height>32 ||
               shadow.pixels->size()!=shadow.width*shadow.height*density*density ||
               shadow.xQuarters < -128 || shadow.yQuarters < -128 ||
               shadow.xQuarters>1536 || shadow.yQuarters>1536 ||
               shadow.xQuarters+int(shadow.width)*4>int(a.width+32)*4 ||
               shadow.yQuarters+int(shadow.height)*4>int(a.height+32)*4 ||
               !OrderedGroundShadowEligible(p,shadow.ownerType))
                throw std::invalid_argument("ordered ground shadow contract");
            // Use the original pose anchor, not the word-rounded native source
            // crop. PC/Amiga left clipping can round those by different amounts.
            const auto originX=std::ptrdiff_t(int16_t(g.modX+g.spriteX-g.mapX+g.xBias));
            const auto originY=std::ptrdiff_t(int16_t(int16_t(g.modY+g.spriteY-g.rows-g.height-g.mapY)+16));
            const auto left=originX*density+shadow.xQuarters*int(density)/4;
            const auto top=originY*density+shadow.yQuarters*int(density)/4;
            // Keep the native logical eligibility and crop the extra visual
            // footprint to the same view/backing. No new native reads/writes.
            const auto maxX=std::min<std::ptrdiff_t>(w,std::ptrdiff_t(g.viewWidth)+32)*density;
            const auto maxY=std::min<std::ptrdiff_t>(h,std::ptrdiff_t(g.viewHeight)+31)*density;
            for(size_t sy=0;sy<shadow.height*density;++sy)for(size_t sx=0;sx<shadow.width*density;++sx){
                const auto pixel=(*shadow.pixels)[sy*shadow.width*density+sx];
                if(!(pixel>>24))continue;
                const auto x=left+std::ptrdiff_t(sx),y=top+std::ptrdiff_t(sy);
                if(x<0 || y<0 || x>=maxX || y>=maxY)continue;
                const size_t n=size_t(y/density)*w+size_t(x/density);if(!visible(n))continue;
                auto found=out.cells.find(n);
                if(found==out.cells.end()){
                    budget(out.cells.size()+1,savedCells.size());
                    found=out.cells.emplace(n,std::vector<uint32_t>(density*density,color(n))).first;
                }
                const size_t at=size_t(y%density)*density+size_t(x%density);
                found->second[at]=SoldierBlend(pixel,found->second[at]);
            }
        }
        for(size_t y=0;y<size_t(d.rows);++y)for(size_t x=0;x<columns;++x){
            const size_t n=size_t(start)+y*w+x;if(!visible(n))continue;
            auto found=out.cells.find(n);
            if(found==out.cells.end()){
                budget(out.cells.size()+1,savedCells.size());
                found=out.cells.emplace(n,std::vector<uint32_t>(density*density,color(n))).first;
            }
            auto& cell=found->second;
            for(size_t sy=0;sy<density;++sy)for(size_t sx=0;sx<density;++sx){
                const size_t source=((cropY+y)*density+sy)*a.width*density+(cropX+x)*density+sx;
                cell[sy*density+sx]=SoldierBlend((*a.pixels)[source],cell[sy*density+sx]);
            }
        }
        ++out.replaced;
    }
    surface.indexed.indices=std::make_shared<const std::vector<uint8_t>>(std::move(indices));
    out.background=RasterizePresentationSurface(surface);
    return out;
}
} // namespace openfodder
