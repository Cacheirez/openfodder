// GPL-3.0-or-later. Synthetic source contracts; no commercial sprite data.
#ifdef NDEBUG
#undef NDEBUG
#endif
#include "Utils/NativePlayerCatalog.hpp"
#include <cassert>
#include <cstdio>
using namespace openfodder;
static PreparedSpriteDraw fixture(const PlayerNativeSlot& slot){
    PreparedSpriteDraw p;auto& s=p.soldier;auto& g=s.geometry;auto& n=p.nativeAmiga8;auto& r=p.resource;
    s.valid=true;s.scene=1;s.generation=2;s.interval=3;s.slot=4;s.type=slot.type;
    s.sheet=slot.sheet;s.frame=slot.frame;s.segment=slot.segment;s.personType=0;
    g.format=SpriteDrawFormat(slot.format);g.columns=slot.columns;g.rows=slot.rows;g.palette=slot.palette;
    g.modX=slot.modX;g.modY=slot.modY;g.spriteX=50;g.spriteY=50;
    r.offset=slot.offset;r.layout={g.format,320,256,4};r.palette=g.palette;r.generation=5;
    static const auto bytes=std::make_shared<const std::vector<uint8_t>>(200000,0);
    r.bytes=bytes;n={s.type,s.sheet,s.frame,s.segment,uint16_t(r.offset),g.columns,g.rows,g.modX,g.modY,
        s.scene,s.generation,s.slot,r.generation,r.bytes};
    n.cf1=true;n.role=slot.role;n.layout=r.layout;n.palette=r.palette;n.frameOffset=slot.offset;
    if(slot.role==3){n.ownerType=0;n.ownerPerson=0;n.ownerGeneration=6;n.ownerHeight=slot.frame?0:12;
        n.ownerX=45-(n.ownerHeight>>2);n.ownerY=53-(n.ownerHeight>>2);}
    auto input=g;input.source=r.source();p.draw=PrepareSpriteDraw(input);p.draw.source=nullptr;
    return p;
}
template<class F> static void rejects(F f){bool caught=false;try{f();}catch(const std::exception&){caught=true;}assert(caught);}
int main(){
    std::map<std::string,OrderedSoldierAsset> art;
    nlohmann::json input={{"schema",1},{"complete",true},{"keep_verified_native",true},{"poses",nlohmann::json::array()},
        {"native_resources",nlohmann::json::array()}};
    std::set<std::tuple<int,int,std::string>> resources;
    for(const auto& slot:CF1PlayerNativeSlots){
        if(!slot.produced)continue;
        auto p=fixture(slot);nlohmann::json ids=nlohmann::json::object();
        resources.emplace(slot.format,slot.segment,SoldierSHA256(*p.resource.bytes));
        if(!slot.invisible)for(unsigned d:{8u,12u}){
            const auto id=std::to_string(NativeSpriteWidth(p))+"x"+std::to_string(slot.rows)+"-"+std::to_string(d);
            if(!art.count(id)){OrderedSoldierAsset a;a.decision=SoldierArtDecision::Replace;a.width=NativeSpriteWidth(p);
                a.height=slot.rows;a.density=d;a.pixels=std::make_shared<const std::vector<uint32_t>>(a.width*a.height*d*d,0xff123456u);art[id]=a;}
            ids[std::to_string(d)]=id;
        }
        input["poses"].push_back({{"format",slot.format},{"type",slot.type},{"sheet",slot.sheet},{"frame",slot.frame},
            {"native_signatures",nlohmann::json::array({CF1NativePoseSignature(p)})},{"assets",ids}});
    }
    // One immutable synthetic sheet; production has one per format/segment.
    for(const auto& resource:resources)input["native_resources"].push_back({{"format",std::get<0>(resource)},
        {"segment",std::get<1>(resource)},{"sha256",std::get<2>(resource)}});
    NativePlayerCatalog catalog(input,art);assert(catalog.isComplete());size_t cases=0;
    for(const auto& slot:CF1PlayerNativeSlots)for(unsigned d:{8u,12u}){
        auto p=fixture(slot);auto resolve=[&](){return catalog.resolve(p,d,384,384*272,art);};
        if(!slot.produced){assert(resolve().decision==SoldierArtDecision::Missing);++cases;continue;}
        auto result=resolve();assert(result.decision==(slot.invisible?SoldierArtDecision::KeepClassic:SoldierArtDecision::Replace));++cases;
        // Every legal logical state resolves independently of full-key churn.
        if(slot.role==1)for(int animation:{0,1,2,3,5,6,7,9,10,50,51,52,90,91}){p.soldier.animation=animation;assert(resolve().decision==result.decision);++cases;}
        p.soldier.animation=0;p.soldier.geometry.spriteX+=1; // position is engine-owned
        if(slot.role!=3){assert(resolve().decision==result.decision);++cases;}
        p=fixture(slot);p.nativeAmiga8.cf1=false;rejects(resolve);++cases;
        p=fixture(slot);p.resource.generation++;rejects(resolve);++cases;
        p=fixture(slot);p.nativeAmiga8.columns++;rejects(resolve);++cases;
        p=fixture(slot);auto changed=std::make_shared<std::vector<uint8_t>>(*p.resource.bytes);(*changed)[p.resource.offset]^=0x40;
        p.resource.bytes=changed;p.nativeAmiga8.bytes=changed;rejects(resolve);++cases;
        p=fixture(slot);p.soldier.geometry.rows++;rejects(resolve);++cases;
        p=fixture(slot);if(slot.role==1){p.soldier.animation=99;rejects(resolve);++cases;}
        p=fixture(slot);if(slot.role==3){p.nativeAmiga8.ownerGeneration=0;rejects(resolve);++cases;}
        p=fixture(slot);if(slot.role==1){p.nativeAmiga8.role=0;p.soldier.type=5;p.nativeAmiga8.type=5;
            assert(resolve().decision==SoldierArtDecision::KeepClassic);++cases;}
    }
    auto missing=input;missing["poses"].erase(missing["poses"].begin());rejects([&](){NativePlayerCatalog c(missing,art);});
    auto duplicate=input;duplicate["poses"].back()=duplicate["poses"].front();rejects([&](){NativePlayerCatalog c(duplicate,art);});
    auto unknown=input;unknown["poses"][0]["sheet"]=999;rejects([&](){NativePlayerCatalog c(unknown,art);});
    auto wrong=input;wrong["poses"][0]["native_signatures"][0]=std::string(64,'0');NativePlayerCatalog badSignature(wrong,art);
    auto first=fixture(CF1PlayerNativeSlots[0]);rejects([&](){badSignature.resolve(first,8,384,384*272,art);});
    auto oversized=first;oversized.resource.bytes=std::make_shared<const std::vector<uint8_t>>(1024*1024+1,0);
    oversized.nativeAmiga8.bytes=oversized.resource.bytes;bool budget=false;
    try{catalog.resolve(oversized,8,384,384*272,art);}catch(const std::length_error&){budget=true;}assert(budget);
    auto latent=input;latent["complete"]=false;auto entry=input["poses"][0];entry["sheet"]=0x30;entry["frame"]=0;
    latent["poses"]=nlohmann::json::array({entry});rejects([&](){NativePlayerCatalog c(latent,art);});
    std::printf("PASS CF1 native catalog: %zu resolution/mutation cases; complete %zu produced slots; 48 declared-only rows remain unbound; unknown/corrupt/incomplete rejected\n",cases+6,RequiredCF1PlayerNativeSlotCount());
}
