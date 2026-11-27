// GPL-3.0-or-later. Explicit CF1 enemy source coverage; no animation selection.
#pragma once
#include "NativePlayerCatalog.hpp"
#include "EnemyPoseTable.hpp"
namespace openfodder {
inline std::string CF1EmptyEnemyPoseSignature(size_t width,size_t height) {
    std::vector<uint8_t> bytes={'C','F','1','P','O','S','E',1};
    for(size_t value:{width,height})for(unsigned i=0;i<8;++i)bytes.push_back(uint8_t(value>>(8*i)));
    bytes.resize(bytes.size()+width*height,0);return SoldierSHA256(std::move(bytes));
}
class NativeEnemyCatalog {
    using Key=std::tuple<int,int,int,int>;
    struct Pose {std::set<std::string> signatures,noWrites;std::string asset;};
    std::map<Key,Pose> poses;
    std::map<std::pair<int,int>,std::set<std::string>> resources;
    mutable std::vector<std::pair<std::weak_ptr<const std::vector<uint8_t>>,std::string>> hashes;
    mutable std::mutex hashMutex;
    unsigned density=0;bool completeArt=false;
    static bool hash(const std::string& s){return s.size()==64 && s.find_first_not_of("0123456789abcdef")==std::string::npos;}
    static int integer(const nlohmann::json& row,const char* key,int limit){
        const auto& v=row.at(key);
        if(!v.is_number_integer() || v.get<int64_t>()<0 || v.get<uint64_t>()>unsigned(limit))
            throw std::invalid_argument("enemy catalog integer");
        return v.get<int>();
    }
public:
    NativeEnemyCatalog(const nlohmann::json& input,const std::map<std::string,OrderedSoldierAsset>& artwork,unsigned selected):density(selected) {
        if((density!=8 && density!=12) || integer(input,"schema",1)!=1 ||
           !input.contains("density") || !input["density"].is_number_integer() || input["density"]!=density ||
           !input.contains("complete_art") || !input["complete_art"].is_boolean())
            throw std::invalid_argument("enemy catalog schema/density");
        completeArt=input["complete_art"];
        const auto& sources=input.at("native_resources");
        if(!sources.is_array() || sources.empty() || sources.size()>128)throw std::invalid_argument("enemy catalog resources");
        for(const auto& source:sources){
            const int fmt=integer(source,"format",1),segment=integer(source,"segment",1);const std::string sha=source.at("sha256");
            if((fmt!=0 && fmt!=1) || (segment!=0 && segment!=1) || !hash(sha) ||
               !resources[{fmt,segment}].insert(sha).second)throw std::invalid_argument("enemy catalog resource identity");
        }
        const auto& entries=input.at("poses");
        if(!entries.is_array() || entries.size()!=RequiredCF1EnemyNativeSlotCount())throw std::invalid_argument("enemy catalog source completeness");
        for(const auto& entry:entries){
            const int fmt=integer(entry,"format",1),type=integer(entry,"type",106),sheet=integer(entry,"sheet",255),frame=integer(entry,"frame",23);
            const auto* slot=FindCF1EnemyNativeSlot(fmt,type,sheet,frame);
            if(!slot || !slot->produced)throw std::invalid_argument("enemy catalog unknown or unproduced slot");
            const size_t width=fmt==0?size_t(slot->columns):size_t(slot->columns-1)*16;
            Pose pose;const auto& signatures=entry.at("native_signatures");const auto& empty=entry.at("no_write_signatures");
            if(!signatures.is_array() || signatures.empty() || signatures.size()>32 || !empty.is_array() || empty.size()>1)
                throw std::invalid_argument("enemy catalog signatures");
            for(const auto& item:signatures){const auto value=item.get<std::string>();if(!hash(value)||!pose.signatures.insert(value).second)throw std::invalid_argument("enemy catalog signature");}
            for(const auto& item:empty){const auto value=item.get<std::string>();
                if(!pose.signatures.count(value) || value!=CF1EmptyEnemyPoseSignature(width,size_t(slot->rows)))
                    throw std::invalid_argument("enemy catalog no-write signature");
                pose.noWrites.insert(value);
            }
            if(slot->invisible && pose.noWrites!=pose.signatures)throw std::invalid_argument("enemy catalog hidden raster");
            const auto& ids=entry.at("assets");
            if(!ids.is_object() || ids.size()>1 || (slot->role==6 && !ids.empty()))throw std::invalid_argument("enemy catalog assets");
            if(!ids.empty()){
                pose.asset=ids.at(std::to_string(density)).get<std::string>();const auto found=artwork.find(pose.asset);
                if(found==artwork.end() || found->second.density!=density || found->second.width!=width || found->second.height!=size_t(slot->rows))
                    throw std::invalid_argument("enemy catalog asset geometry");
            }
            if(completeArt && slot->role!=6 && pose.signatures!=pose.noWrites && pose.asset.empty())
                throw std::invalid_argument("enemy catalog incomplete art");
            if(!poses.emplace(Key{fmt,type,sheet,frame},std::move(pose)).second)throw std::invalid_argument("enemy catalog duplicate");
        }
        for(const auto& slot:CF1EnemyNativeSlots)if(slot.produced && !poses.count(Key{slot.format,slot.type,slot.sheet,slot.frame}))
            throw std::invalid_argument("enemy catalog missing source slot");
    }
    OrderedSoldierAsset resolve(const PreparedSpriteDraw& p,unsigned requested,size_t targetWidth,size_t targetSize,
                               const std::map<std::string,OrderedSoldierAsset>& artwork) const {
        if(requested!=density)throw std::invalid_argument("enemy catalog requested density");
        ValidateCF1NativeSprite(p,targetWidth,targetSize);
        const auto& s=p.soldier;const auto& g=s.geometry;const auto& n=p.nativeAmiga8;
        const auto* slot=FindCF1EnemyNativeSlot(int(g.format),s.type,s.sheet,s.frame);
        if(!slot || !slot->produced || n.role!=slot->role || n.frameOffset!=size_t(slot->offset) || s.segment!=slot->segment ||
           g.columns!=slot->columns || g.rows!=slot->rows || g.modX!=slot->modX || g.modY!=slot->modY || g.palette!=slot->palette)
            throw std::invalid_argument("enemy catalog source slot");
        if(slot->role==2 && (s.personType<0 || s.personType>2 || !(slot->personMask&(1<<s.personType)) || !IsCF1PlayerAnimation(s.animation)))
            throw std::invalid_argument("enemy catalog logical state");
        // Owner type is captured from the shadow's native creation field. Its
        // current person/height may change after this draw was prepared.
        if(slot->role==4 && ((n.ownerType!=5 && n.ownerType!=36) || !n.ownerGeneration ||
           n.ownerSlot==s.slot || n.ownerPerson<0 || g.height))throw std::invalid_argument("enemy catalog shadow owner");
        std::string resourceHash;
        {
            std::lock_guard<std::mutex> lock(hashMutex);
            for(const auto& cached:hashes)if(cached.first.lock()==p.resource.bytes){resourceHash=cached.second;break;}
            if(resourceHash.empty()){
                resourceHash=SoldierSHA256(*p.resource.bytes);if(hashes.size()==32)hashes.erase(hashes.begin());
                hashes.emplace_back(p.resource.bytes,resourceHash);
            }
        }
        const auto source=resources.find({int(g.format),s.segment});
        if(source==resources.end() || !source->second.count(resourceHash))throw std::invalid_argument("enemy catalog unverified resource");
        const auto& pose=poses.at(Key{int(g.format),s.type,s.sheet,s.frame});const auto signature=CF1NativePoseSignature(p);
        if(!pose.signatures.count(signature))throw std::invalid_argument("enemy catalog unverified raster");
        if(pose.noWrites.count(signature)){
            auto draw=p.draw;draw.source=p.resource.source();
            if(!CaptureSprite8Producer(draw,p.resource.layout,targetWidth).writes.empty())throw std::invalid_argument("enemy catalog no-write draw writes");
            return OrderedSoldierAsset{SoldierArtDecision::KeepClassic};
        }
        if(slot->role==6 || pose.asset.empty())return OrderedSoldierAsset{SoldierArtDecision::KeepClassic};
        auto out=artwork.at(pose.asset);
        if(out.groundShadow.pixels && !OrderedGroundShadowEligible(p,out.groundShadow.ownerType))out.groundShadow={};
        return out;
    }
    bool isArtComplete()const{return completeArt;}
};
} // namespace openfodder
