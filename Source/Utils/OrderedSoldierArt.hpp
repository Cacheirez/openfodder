// GPL-3.0-or-later. Internal ordered compositor; not yet the SDL publication path.
#pragma once
#include "MissionLayers.hpp"
#include <map>
#include <functional>
namespace openfodder {
// A resolver must match the complete retained resource/variant key, not just a
// sheet number. KeepClassic is an explicit out-of-scope classification (effects,
// civilians, etc.); it must never be used to excuse a missing soldier asset.
enum class SoldierArtDecision { Replace, KeepClassic, Missing };
struct OrderedSoldierAsset {
    SoldierArtDecision decision = SoldierArtDecision::Missing;
    size_t width = 0, height = 0;
    unsigned density = 1;
    std::shared_ptr<const std::vector<uint32_t>> pixels;
};
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
        const auto& p=l.soldier;const auto a=resolve(p);
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
