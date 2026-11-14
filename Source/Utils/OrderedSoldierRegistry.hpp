// GPL-3.0-or-later. Explicit bindings; observing a key never approves it.
#pragma once
#include "SoldierVariant.hpp"
#include "SoldierArtBatch.hpp"
#include "json.hpp"
#include <fstream>
namespace openfodder {
class OrderedSoldierRegistry {
    struct Binding {bool keep=false;int sheet=0,frame=0;std::map<unsigned,std::string> assets;};
    std::map<std::string,OrderedSoldierAsset> artwork;
    std::map<std::string,Binding> entries;
    static bool validHash(const std::string& hash) {
        return hash.size()==64 && hash.find_first_not_of("0123456789abcdef")==std::string::npos;
    }
    static bool relativeAssetPath(const std::string& path) {
        if(path.empty() || path.size()>512)return false;
        size_t start=0;
        for(size_t i=0;i<=path.size();++i){
            if(i!=path.size() && path[i]!='/'){
                const unsigned char c=path[i];
                if(!((c>='a'&&c<='z') || (c>='A'&&c<='Z') || (c>='0'&&c<='9') ||
                     c=='_' || c=='-' || c=='.'))return false;
                continue;
            }
            const auto part=path.substr(start,i-start);
            if(part.empty() || part=="." || part=="..")return false;
            start=i+1;
        }
        return true;
    }
    static size_t integer(const nlohmann::json& row,const char* field,size_t limit) {
        const auto& value=row.at(field);
        if(!value.is_number_integer() || value.get<int64_t>()<=0 || value.get<uint64_t>()>limit)
            throw std::invalid_argument("ordered asset integer");
        return value.get<size_t>();
    }
    void loadArtwork(const nlohmann::json& assets,const std::string& directory) {
        if(!assets.is_array() || assets.size()>8192)throw std::invalid_argument("ordered assets size");
        size_t total=0;const size_t budget=64u*1024u*1024u;
        // Preflight the entire budget before opening files or allocating pixels.
        for(const auto& row:assets){
            const auto width=integer(row,"width",352),height=integer(row,"height",272);
            const auto density=integer(row,"density",12);
            if(density!=8 && density!=12)throw std::invalid_argument("ordered asset density");
            const size_t bytes=width*height*density*density*4;
            if(bytes>budget-total)throw std::length_error("ordered assets budget");
            total+=bytes;
        }
        for(const auto& row:assets){
            const auto id=row.at("id").get<std::string>();
            const auto path=row.at("file").get<std::string>();
            const auto hash=row.at("sha256").get<std::string>();
            if(id.empty() || id.size()>128 || !relativeAssetPath(path) || !validHash(hash) || artwork.count(id))
                throw std::invalid_argument("ordered asset identity/path/hash");
            OrderedSoldierAsset asset;asset.decision=SoldierArtDecision::Replace;
            asset.width=integer(row,"width",352);asset.height=integer(row,"height",272);
            asset.density=unsigned(integer(row,"density",12));
            if(asset.density!=8 && asset.density!=12)throw std::invalid_argument("ordered asset density");
            const size_t count=asset.width*asset.height*asset.density*asset.density;
            const size_t bytes=count*4;
            // Size and digest are checked before the immutable pixels are exposed.
            std::ifstream file(directory+path,std::ios::binary|std::ios::ate);
            if(!file || file.tellg()!=std::streamoff(bytes))throw std::invalid_argument("ordered asset file size");
            file.seekg(0);std::vector<uint8_t> rgba(bytes);
            if(!file.read(reinterpret_cast<char*>(rgba.data()),std::streamsize(bytes)) || SoldierSHA256(rgba)!=hash)
                throw std::invalid_argument("ordered asset content hash");
            auto pixels=std::make_shared<std::vector<uint32_t>>(count);
            for(size_t i=0;i<count;++i){const auto* p=rgba.data()+i*4;
                (*pixels)[i]=(uint32_t(p[3])<<24)|(uint32_t(p[0])<<16)|(uint32_t(p[1])<<8)|p[2];}
            asset.pixels=pixels;artwork.emplace(id,std::move(asset));
        }
    }
public:
    explicit OrderedSoldierRegistry(const nlohmann::json& root,const std::string& directory="") {
        const auto& v=root.at("version");
        if(!v.is_number_integer() || (v!=1 && v!=2))throw std::invalid_argument("ordered manifest version");
        if(v==2)loadArtwork(root.at("assets"),directory);
        if(!root.at("bindings").is_array() || root.at("bindings").size()>8192)
            throw std::invalid_argument("ordered manifest version/size");
        for(const auto& row:root.at("bindings")){
            const auto key=row.at("key").get<std::string>();
            if(!validHash(key))
                throw std::invalid_argument("ordered manifest key");
            Binding b;const auto decision=row.at("decision").get<std::string>();
            if(decision=="keep-associated")b.keep=true;
            else if(decision=="replace-pilot"){
                b.sheet=row.at("sheet").get<int>();b.frame=row.at("frame").get<int>();
                if((b.sheet!=2 && b.sheet!=7) || b.frame<0 || b.frame>2)
                    throw std::invalid_argument("ordered manifest pilot asset");
            } else if(decision=="replace-art" && v==2){
                const auto& ids=row.at("assets");
                if(!ids.is_object() || ids.empty() || ids.size()>2)throw std::invalid_argument("ordered binding assets");
                for(auto it=ids.begin();it!=ids.end();++it){
                    if(it.key()!="8" && it.key()!="12")throw std::invalid_argument("ordered binding density");
                    const unsigned density=it.key()=="8"?8:12;
                    const auto id=it.value().get<std::string>();const auto found=artwork.find(id);
                    if(found==artwork.end() || found->second.density!=density)
                        throw std::invalid_argument("ordered binding asset reference");
                    b.assets.emplace(density,id);
                }
            } else throw std::invalid_argument("ordered manifest decision");
            if(!entries.emplace(key,b).second)throw std::invalid_argument("ordered manifest duplicate");
        }
    }
    static OrderedSoldierRegistry Load(const std::string& path) {
        std::ifstream file(path,std::ios::binary|std::ios::ate);
        if(!file || file.tellg()<0 || file.tellg()>8*1024*1024)throw std::invalid_argument("ordered manifest file");
        file.seekg(0);nlohmann::json root;file>>root;
        const auto slash=path.find_last_of("/\\");
        return OrderedSoldierRegistry(root,slash==std::string::npos?"":path.substr(0,slash+1));
    }
    // The Window census derives key from the complete frozen resource and the
    // current palette. Composition still validates the draw before rasterizing.
    OrderedSoldierAsset resolve(const PreparedSpriteDraw& p,const std::string& key,unsigned density,
                                bool hybrid=false) const {
        OrderedSoldierAsset result;
        const auto found=entries.find(key);
        const auto& s=p.soldier;const auto& g=s.geometry;
        if(found==entries.end()){
            // Initial hybrid scope: the audited Amiga8 tree table entry.
            // This is a native resource contract, independent of palette keys.
            if(hybrid && s.valid && s.scene && s.generation && s.interval &&
               !s.inVehicle && !s.pendingDestroy && !p.isCursor &&
               s.type==14 && s.sheet==0x90 && s.frame==0 && s.segment==1 &&
               g.format==SpriteDrawFormat::Amiga8 && g.columns==2 && g.rows==28 &&
               g.modX==0 && g.modY==0 && g.palette==0 && p.resource.palette==0 &&
               p.resource && p.resource.generation && p.resource.offset==1942 &&
               p.resource.layout.format==g.format && p.resource.layout.width==320 &&
               p.resource.layout.height==256 && p.resource.layout.planes==4)
                result.decision=SoldierArtDecision::KeepClassic;
            return result;
        }
        const auto& b=found->second;
        if(b.keep){
            // Explicit associated sheets only; never a body/civilian exemption.
            const bool effectType=s.type==2||s.type==3||s.type==6||s.type==21||s.type==22||s.type==23||
                s.type==33||s.type==35||s.type==93||s.type==94||s.type==95||s.type==96||s.type==98;
            // Bird2_Left is scenery, not a human body. Only its original two
            // Amiga frames may be retained, and only after an exact-key lookup.
            const bool bird=s.type==19 && s.sheet==0x98 && (s.frame==0||s.frame==1) &&
                g.format==SpriteDrawFormat::Amiga8 && s.valid && p.resource &&
                !s.inVehicle && !s.pendingDestroy;
            // Only the audited tree variant can stay in its original draw order.
            const bool tree=s.type==14 && s.sheet==0x90 &&
                key=="a835b7ae71451ea0a37ea0a0c1e77da13a45f003b0cf218314edc6e0c79a1a2d";
            const bool bullet=s.type==6 && s.sheet==0x7f &&
                key=="6c2cdf76311d72391780febb69499a2f1b94325ed1509838b7af65f3141d5981";
            const bool retainedNative=(tree || bullet || (s.type==15 && s.sheet==0x91) ||
                (s.type==37 && s.sheet==0xc2)) && s.frame==0 &&
                g.format==SpriteDrawFormat::Amiga8 && s.valid && p.resource &&
                !s.inVehicle && !s.pendingDestroy;
            if(bird || retainedNative || s.sheet==0x7c || (effectType && (s.sheet==0x8d||s.sheet==0x97||s.sheet==0x95||s.sheet==0xe5||s.sheet==0xe6)))
                result.decision=SoldierArtDecision::KeepClassic;
            return result;
        }
        if(!b.assets.empty()){
            const auto selected=b.assets.find(density);if(selected==b.assets.end())return result;
            const auto& art=artwork.at(selected->second);
            const int width=g.format==SpriteDrawFormat::PC?(g.columns/2)*2:(g.columns-1)*16;
            if(!s.valid || !p.resource || s.sheet==0x7c ||
               (g.format!=SpriteDrawFormat::PC && g.format!=SpriteDrawFormat::Amiga8) ||
               width<=0 || g.rows<=0 || art.width!=size_t(width) || art.height!=size_t(g.rows))return result;
            // The caller supplies the full content/state/palette key. Position,
            // facing, animation phase, offsets and cropping remain engine-owned.
            return art;
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
