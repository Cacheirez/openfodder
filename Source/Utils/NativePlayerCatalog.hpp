// GPL-3.0-or-later. Finite source-defined CF1 poses; no simulation or frame selection.
#pragma once
#include "SoldierVariant.hpp"
#include "PlayerPoseTable.hpp"
#include "json.hpp"
#include <set>
#include <tuple>
#include <mutex>
namespace openfodder {
inline size_t NativeSpriteWidth(const PreparedSpriteDraw& p) {
    const auto& g=p.soldier.geometry;
    if(g.format==SpriteDrawFormat::PC && g.columns>0 && !(g.columns&1))return size_t(g.columns);
    if(g.format==SpriteDrawFormat::Amiga8 && g.columns>1)return size_t(g.columns-1)*16;
    throw std::invalid_argument("native CF1 sprite columns/format");
}
// Prove the complete source extent, even when the visible draw is cropped.
inline void ValidateCF1NativeSprite(const PreparedSpriteDraw& p,size_t targetWidth,size_t targetSize) {
    const auto& s=p.soldier;const auto& g=s.geometry;const auto& r=p.resource;const auto& n=p.nativeAmiga8;
    if(r.bytes && r.bytes->size()>1024u*1024u)throw std::length_error("native CF1 resource budget");
    if(!n.cf1 || !s.valid || !s.scene || !s.generation || !s.interval || p.isCursor ||
       !r || !r.generation || !n.bytes || r.bytes!=n.bytes || r.generation!=n.resourceGeneration ||
       s.type!=n.type || s.sheet!=n.sheet || s.frame!=n.frame || s.segment!=n.segment ||
       s.scene!=n.scene || s.slot!=n.slot || s.generation!=n.generation || r.offset!=n.offset ||
       g.columns!=n.columns || g.rows!=n.rows || g.modX!=n.modX || g.modY!=n.modY ||
       g.source || g.palette!=r.palette || r.palette!=n.palette ||
       r.layout.format!=g.format || n.layout.format!=r.layout.format ||
       n.layout.width!=r.layout.width || n.layout.height!=r.layout.height || n.layout.planes!=r.layout.planes ||
       r.layout.width!=320 || r.offset<n.frameOffset || g.rows<=0 || g.rows>272)
        throw std::invalid_argument("native CF1 source-table provenance");
    const bool pc=g.format==SpriteDrawFormat::PC;
    const size_t width=NativeSpriteWidth(p),stride=pc?160:40,planes=pc?1:r.layout.planes;
    const size_t columns=pc?width/2:width/8;
    if(width>352 || columns>stride || (!pc && (planes!=4 || !r.layout.height || r.layout.height>1024)))
        throw std::invalid_argument("native CF1 layout");
    const size_t last=(planes-1)*size_t(r.layout.height)*40+(size_t(g.rows)-1)*stride+columns;
    if(last>r.available())throw std::out_of_range("native CF1 complete extent");
    auto draw=p.draw;draw.source=r.source();
    ValidateMissionSpriteRaster(draw,r,targetWidth,targetSize);
}
// Hash visible source indices/mask, not animation, address or unrelated palette
// colors. The slot separately fixes the action, native table geometry and palette.
inline std::string CF1NativePoseSignature(const PreparedSpriteDraw& p) {
    const auto& g=p.soldier.geometry;const auto& r=p.resource;
    const size_t width=NativeSpriteWidth(p),height=size_t(g.rows);
    if(!r || g.rows<=0 || g.rows>272 || width>352)throw std::invalid_argument("native pose extent");
    const bool pc=g.format==SpriteDrawFormat::PC;
    const size_t stride=pc?160:40,planes=pc?1:r.layout.planes,columns=pc?width/2:width/8;
    if((!pc && (planes!=4 || !r.layout.height || r.layout.width!=320)) ||
       (planes-1)*size_t(r.layout.height)*40+(height-1)*stride+columns>r.available())
        throw std::out_of_range("native pose source");
    std::vector<uint8_t> bytes={'C','F','1','P','O','S','E',1};
    for(size_t value:{width,height})for(unsigned i=0;i<8;++i)bytes.push_back(uint8_t(value>>(8*i)));
    for(size_t y=0;y<height;++y)for(size_t x=0;x<width;++x){
        uint8_t index=0;
        if(pc){const auto pixel=r.source()[y*160+x/2];index=(x&1)?pixel&15:pixel>>4;}
        else for(size_t plane=0;plane<4;++plane)
            if(r.source()[plane*size_t(r.layout.height)*40+y*40+x/8]&(0x80>>(x&7)))index|=uint8_t(1u<<plane);
        bytes.push_back(index);
    }
    return SoldierSHA256(std::move(bytes));
}
class NativePlayerCatalog {
    using Key=std::tuple<int,int,int,int>;
    struct Pose {std::set<std::string> signatures;std::map<unsigned,std::string> assets;};
    std::map<Key,Pose> poses;
    std::map<std::pair<int,int>,std::set<std::string>> resources;
    mutable std::vector<std::pair<std::weak_ptr<const std::vector<uint8_t>>,std::string>> resourceHashes;
    mutable std::mutex resourceHashMutex;
    bool complete=false,keepAssociated=false;
    static bool hash(const std::string& s){return s.size()==64 && s.find_first_not_of("0123456789abcdef")==std::string::npos;}
public:
    NativePlayerCatalog(const nlohmann::json& input,const std::map<std::string,OrderedSoldierAsset>& artwork) {
        if(input.value("schema",0)!=1 || !input.contains("complete") || !input["complete"].is_boolean() ||
           !input.contains("keep_verified_native") || !input["keep_verified_native"].is_boolean())
            throw std::invalid_argument("player catalog schema");
        complete=input["complete"];keepAssociated=input["keep_verified_native"];
        const auto& sources=input.at("native_resources");
        if(!sources.is_array() || sources.empty() || sources.size()>128)throw std::invalid_argument("player catalog native resources");
        for(const auto& source:sources){
            const int fmt=source.at("format"),segment=source.at("segment");const std::string sha=source.at("sha256");
            if((fmt!=0 && fmt!=1) || segment<0 || segment>15 || !hash(sha) ||
               !resources[{fmt,segment}].insert(sha).second)throw std::invalid_argument("player catalog native resource identity");
        }
        const auto& entries=input.at("poses");
        if(!entries.is_array() || entries.size()>RequiredCF1PlayerNativeSlotCount())
            throw std::invalid_argument("player catalog size");
        for(const auto& entry:entries){
            const int fmt=entry.at("format"),type=entry.at("type"),sheet=entry.at("sheet"),frame=entry.at("frame");
            const auto* slot=FindCF1PlayerNativeSlot(fmt,type,sheet,frame);
            if(!slot || !slot->produced)throw std::invalid_argument("player catalog unknown or unproduced slot");
            Pose pose;const auto& signatures=entry.at("native_signatures");
            if(!signatures.is_array() || signatures.empty() || signatures.size()>32)throw std::invalid_argument("player catalog signatures");
            for(const auto& item:signatures){const auto value=item.get<std::string>();if(!hash(value)||!pose.signatures.insert(value).second)throw std::invalid_argument("player catalog signature");}
            const auto& ids=entry.at("assets");
            if(!ids.is_object() || (slot->invisible?!ids.empty():ids.size()!=2))throw std::invalid_argument("player catalog assets");
            for(unsigned d:{8u,12u})if(!slot->invisible){
                const auto id=ids.at(std::to_string(d)).get<std::string>();const auto asset=artwork.find(id);
                const size_t width=fmt==0?size_t(slot->columns):size_t(slot->columns-1)*16;
                if(asset==artwork.end() || asset->second.density!=d || asset->second.width!=width || asset->second.height!=size_t(slot->rows))
                    throw std::invalid_argument("player catalog asset geometry");
                pose.assets.emplace(d,id);
            }
            if(!poses.emplace(Key{fmt,type,sheet,frame},std::move(pose)).second)throw std::invalid_argument("player catalog duplicate");
        }
        if(complete)for(const auto& slot:CF1PlayerNativeSlots)
            if(slot.produced && !poses.count(Key{slot.format,slot.type,slot.sheet,slot.frame}))throw std::invalid_argument("player catalog incomplete");
    }
    OrderedSoldierAsset resolve(const PreparedSpriteDraw& p,unsigned density,size_t targetWidth,size_t targetSize,
                               const std::map<std::string,OrderedSoldierAsset>& artwork) const {
        OrderedSoldierAsset out;const auto& s=p.soldier;const auto& g=s.geometry;const auto& n=p.nativeAmiga8;
        ValidateCF1NativeSprite(p,targetWidth,targetSize);
        std::string resourceHash;
        {
            std::lock_guard<std::mutex> lock(resourceHashMutex);
            for(const auto& cached:resourceHashes)if(cached.first.lock()==p.resource.bytes){resourceHash=cached.second;break;}
            if(resourceHash.empty()){
                resourceHash=SoldierSHA256(*p.resource.bytes);
                if(resourceHashes.size()==32)resourceHashes.erase(resourceHashes.begin());
                resourceHashes.emplace_back(p.resource.bytes,resourceHash);
            }
        }
        const auto source=resources.find({int(g.format),s.segment});
        if(source==resources.end() || !source->second.count(resourceHash))throw std::invalid_argument("player catalog unverified source resource");
        if(!n.role){
            if(keepAssociated)out.decision=SoldierArtDecision::KeepClassic;
            return out;
        }
        const auto* slot=FindCF1PlayerNativeSlot(int(g.format),s.type,s.sheet,s.frame);
        if(!slot || slot->role!=n.role || n.frameOffset!=size_t(slot->offset) || s.segment!=slot->segment ||
           g.columns!=slot->columns || g.rows!=slot->rows || g.modX!=slot->modX || g.modY!=slot->modY || g.palette!=slot->palette)
            throw std::invalid_argument("player catalog source slot");
        if(n.role==1 && (s.personType!=0 || !IsCF1PlayerAnimation(s.animation)))throw std::invalid_argument("player catalog logical state");
        if(!slot->produced)return out; // Valid retained native data, dormant selector: never inferred artwork.
        if(n.role==3 && (n.ownerType!=0 || n.ownerPerson!=0 || !n.ownerGeneration ||
           g.spriteX!=int16_t(n.ownerX+(n.ownerHeight>>2)+5) || g.spriteY!=int16_t(n.ownerY+(n.ownerHeight>>2)-3) ||
           g.height || s.frame!=(n.ownerHeight>8?0:1)))throw std::invalid_argument("player shadow owner/anchor");
        const auto found=poses.find(Key{int(g.format),s.type,s.sheet,s.frame});
        if(found==poses.end())return out; // Explicit incomplete development catalog; no inferred art.
        if(!found->second.signatures.count(CF1NativePoseSignature(p)))throw std::invalid_argument("player catalog unverified native raster");
        if(slot->invisible){
            auto draw=p.draw;draw.source=p.resource.source();
            if(!CaptureSprite8Producer(draw,p.resource.layout,targetWidth).writes.empty())throw std::invalid_argument("player catalog hidden draw writes");
            out.decision=SoldierArtDecision::KeepClassic;return out;
        }
        const auto id=found->second.assets.find(density);if(id==found->second.assets.end())return out;
        out=artwork.at(id->second);
        if(out.groundShadow.pixels && !OrderedGroundShadowEligible(p,out.groundShadow.ownerType))out.groundShadow=OrderedSoldierGroundShadow{};
        return out;
    }
    bool isComplete()const{return complete;}
};
} // namespace openfodder
