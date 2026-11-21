// GPL-3.0-or-later. Read-only colour transfer for verified native mission fades.
#pragma once
#include "OrderedSoldierArt.hpp"
#include <array>
namespace openfodder {
struct MissionPaletteTransfer {
    std::array<std::array<uint8_t,256>,3> channels{};
    bool build(const std::array<uint32_t,255>& reference,const std::array<uint32_t,255>& current){
        bool nonBlack=false;
        for(unsigned c=0;c<3;++c){
            std::array<int,256> knots;knots.fill(-1);knots[0]=0;
            const unsigned shift=c*8;
            for(size_t i=0;i<reference.size();++i){
                const unsigned from=(reference[i]>>shift)&255,to=(current[i]>>shift)&255;
                nonBlack|=from!=0;
                // A black-based native fade maps equal components equally,
                // preserves their order and never brightens the reference.
                if(to>from || (knots[from]>=0 && knots[from]!=int(to)))return false;
                knots[from]=int(to);
            }
            unsigned last=0;
            for(unsigned x=1;x<256;++x)if(knots[x]>=0){if(knots[x]<knots[last])return false;last=x;}
            if(!last){for(unsigned x=0;x<256;++x)channels[c][x]=0;continue;}
            if(last<255)knots[255]=knots[last]*255/int(last);
            unsigned left=0;
            for(unsigned right=1;right<256;++right)if(knots[right]>=0){
                for(unsigned x=left;x<=right;++x)channels[c][x]=uint8_t(knots[left]+
                    (knots[right]-knots[left])*int(x-left)/int(right-left));
                left=right;
            }
        }
        return nonBlack;
    }
    uint32_t pixel(uint32_t value)const{
        return (value&0xff000000u)|(uint32_t(channels[2][(value>>16)&255])<<16)|
            (uint32_t(channels[1][(value>>8)&255])<<8)|channels[0][value&255];
    }
};
// Per-publication cache: immutable source art stays untouched; repeated actors
// share the same transfer. The temporary allocation has a separate fixed cap.
struct MissionPaletteArt {
    MissionPaletteTransfer transfer;
    size_t bytes=0;
    std::map<const std::vector<uint32_t>*,std::shared_ptr<const std::vector<uint32_t>>> cache;
    std::shared_ptr<const std::vector<uint32_t>> pixels(const std::shared_ptr<const std::vector<uint32_t>>& source){
        if(!source)return source;
        const auto found=cache.find(source.get());if(found!=cache.end())return found->second;
        if(source->size()>(8u*1024u*1024u-bytes)/4)throw std::length_error("mission palette transfer budget");
        auto result=std::make_shared<std::vector<uint32_t>>();result->reserve(source->size());
        for(auto value:*source)result->push_back(transfer.pixel(value));
        bytes+=result->size()*4;cache.emplace(source.get(),result);return result;
    }
    OrderedSoldierAsset apply(OrderedSoldierAsset art){
        if(art.decision==SoldierArtDecision::Replace){art.pixels=pixels(art.pixels);art.groundShadow.pixels=pixels(art.groundShadow.pixels);}
        return art;
    }
};
} // namespace openfodder
