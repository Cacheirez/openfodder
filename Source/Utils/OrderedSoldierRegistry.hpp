// GPL-3.0-or-later. Explicit bindings; observing a key never approves it.
#pragma once
#include "SoldierVariant.hpp"
#include "SoldierArtBatch.hpp"
#include "json.hpp"
#include <fstream>
namespace openfodder {
class OrderedSoldierRegistry {
    struct Binding {bool keep=false;int sheet=0,frame=0;};
    std::map<std::string,Binding> entries;
public:
    explicit OrderedSoldierRegistry(const nlohmann::json& root) {
        if(root.at("version")!=1 || !root.at("bindings").is_array() || root.at("bindings").size()>8192)
            throw std::invalid_argument("ordered manifest version/size");
        for(const auto& row:root.at("bindings")){
            const auto key=row.at("key").get<std::string>();
            if(key.size()!=64 || key.find_first_not_of("0123456789abcdef")!=std::string::npos)
                throw std::invalid_argument("ordered manifest key");
            Binding b;const auto decision=row.at("decision").get<std::string>();
            if(decision=="keep-associated")b.keep=true;
            else if(decision=="replace-pilot"){
                b.sheet=row.at("sheet").get<int>();b.frame=row.at("frame").get<int>();
                if((b.sheet!=2 && b.sheet!=7) || b.frame<0 || b.frame>2)
                    throw std::invalid_argument("ordered manifest pilot asset");
            } else throw std::invalid_argument("ordered manifest decision");
            if(!entries.emplace(key,b).second)throw std::invalid_argument("ordered manifest duplicate");
        }
    }
    static OrderedSoldierRegistry Load(const std::string& path) {
        std::ifstream file(path,std::ios::binary|std::ios::ate);
        if(!file || file.tellg()<0 || file.tellg()>8*1024*1024)throw std::invalid_argument("ordered manifest file");
        file.seekg(0);nlohmann::json root;file>>root;return OrderedSoldierRegistry(root);
    }
    OrderedSoldierAsset resolve(const PreparedSpriteDraw& p,const std::string& key,unsigned density) const {
        OrderedSoldierAsset result;
        const auto found=entries.find(key);if(found==entries.end())return result;
        const auto& b=found->second;const auto& s=p.soldier;const auto& g=s.geometry;
        if(b.keep){
            // Explicit associated sheets only; never a body/civilian exemption.
            const bool effectType=s.type==2||s.type==3||s.type==6||s.type==21||s.type==22||s.type==23||
                s.type==33||s.type==35||s.type==93||s.type==94||s.type==95||s.type==96||s.type==98;
            if(s.sheet==0x7c || (effectType && (s.sheet==0x8d||s.sheet==0x97||s.sheet==0x95||s.sheet==0xe5||s.sheet==0xe6)))
                result.decision=SoldierArtDecision::KeepClassic;
            return result;
        }
        // Six existing 16x14 masters only; clipping is handled by composition.
        if(s.type!=0 || s.animation!=0 || s.sheet!=b.sheet || s.frame!=b.frame ||
           s.inVehicle || s.pendingDestroy || g.rows!=14 || g.modX || g.modY ||
           (g.format==SpriteDrawFormat::PC?g.columns!=16:g.columns!=2))return result;
        const auto art=SoldierBatchAsset(b.sheet,b.frame,density);
        if(!art.pixels)return result;
        result.decision=SoldierArtDecision::Replace;result.width=16;result.height=14;
        result.density=density;result.pixels=art.pixels;return result;
    }
};
} // namespace openfodder
