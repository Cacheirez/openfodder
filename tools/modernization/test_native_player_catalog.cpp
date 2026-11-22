// GPL-3.0-or-later. Synthetic source contracts; no commercial sprite data.
#ifdef NDEBUG
#undef NDEBUG
#endif
#include "Utils/NativePlayerCatalog.hpp"
#include "Utils/OrderedSoldierRegistry.hpp"
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
        n.ownerX=slot.sheet==0x8d?46:45-(n.ownerHeight>>2);n.ownerY=slot.sheet==0x8d?50:53-(n.ownerHeight>>2);}
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
        if(!slot.invisible && slot.role)for(unsigned d:{8u,12u}){
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
        auto result=resolve();assert(result.decision==((slot.invisible || !slot.role)?SoldierArtDecision::KeepClassic:SoldierArtDecision::Replace));++cases;
        // Every legal logical state resolves independently of full-key churn.
        if(slot.role==1)for(int animation:{0,1,2,3,5,6,7,9,10,50,51,52,90,91}){p.soldier.animation=animation;assert(resolve().decision==result.decision);++cases;}
        p.soldier.animation=0;p.soldier.geometry.spriteX+=1; // position is engine-owned
        if(slot.role!=3){auto geometry=p.soldier.geometry;geometry.source=p.resource.source();p.draw=PrepareSpriteDraw(geometry);p.draw.source=nullptr;
            assert(resolve().decision==result.decision);++cases;}
        p=fixture(slot);p.nativeAmiga8.cf1=false;rejects(resolve);++cases;
        p=fixture(slot);p.resource.generation++;rejects(resolve);++cases;
        p=fixture(slot);p.nativeAmiga8.columns++;rejects(resolve);++cases;
        p=fixture(slot);auto changed=std::make_shared<std::vector<uint8_t>>(*p.resource.bytes);(*changed)[p.resource.offset]^=0x40;
        p.resource.bytes=changed;p.nativeAmiga8.bytes=changed;rejects(resolve);++cases;
        p=fixture(slot);p.soldier.geometry.rows++;rejects(resolve);++cases;
        p=fixture(slot);if(slot.role==1){p.soldier.animation=99;rejects(resolve);++cases;}
        p=fixture(slot);if(slot.role==3){p.nativeAmiga8.ownerGeneration=0;rejects(resolve);++cases;}
        p=fixture(slot);if(slot.role==3){p.nativeAmiga8.role=0;rejects(resolve);++cases;}
        p=fixture(slot);if(slot.role==3){p.nativeAmiga8.ownerX+=7;p.nativeAmiga8.ownerY-=3;
            p.nativeAmiga8.ownerHeight=slot.frame==0?0:16;assert(resolve().decision==result.decision);++cases;
            p.nativeAmiga8.ownerSlot=p.soldier.slot;rejects(resolve);++cases;
            p=fixture(slot);++p.soldier.geometry.spriteX;rejects(resolve);++cases;}
        p=fixture(slot);if(slot.role==1){p.nativeAmiga8.role=0;p.soldier.type=5;p.nativeAmiga8.type=5;
            assert(resolve().decision==SoldierArtDecision::KeepClassic);++cases;}
    }
    // Even a deliberately whitelisted/signed nonempty resource cannot turn a
    // hidden transition into an ignored draw: the real producer must write nothing.
    for(const auto& slot:CF1PlayerNativeSlots)if(slot.produced && slot.invisible){
        auto p=fixture(slot);auto bytes=std::make_shared<std::vector<uint8_t>>(*p.resource.bytes);
        (*bytes)[p.resource.offset]=slot.format?0x80:0x10;p.resource.bytes=bytes;p.nativeAmiga8.bytes=bytes;
        auto nonempty=input;nonempty["native_resources"].push_back({{"format",slot.format},{"segment",slot.segment},{"sha256",SoldierSHA256(*bytes)}});
        for(auto& row:nonempty["poses"])if(row["format"]==slot.format && row["type"]==slot.type && row["sheet"]==slot.sheet && row["frame"]==slot.frame)
            row["native_signatures"]=nlohmann::json::array({CF1NativePoseSignature(p)});
        NativePlayerCatalog guarded(nonempty,art);bool writesRejected=false;
        try{guarded.resolve(p,8,384,384*272,art);}catch(const std::invalid_argument& e){writesRejected=std::string(e.what())=="player catalog hidden draw writes";}
        assert(writesRejected);++cases;
    }
    for(const auto& slot:CF1PlayerNativeSlots)if(slot.produced && !slot.role){
        auto wrongArt=input;for(auto& row:wrongArt["poses"])if(row["format"]==slot.format && row["type"]==slot.type && row["sheet"]==slot.sheet && row["frame"]==slot.frame)
            row["assets"]={{"8",art.begin()->first},{"12",art.begin()->first}};
        bool rejected=false;try{NativePlayerCatalog c(wrongArt,art);}catch(const std::invalid_argument& e){rejected=std::string(e.what())=="player catalog assets";}
        assert(rejected);++cases;
        auto wrongRaster=input;for(auto& row:wrongRaster["poses"])if(row["format"]==slot.format && row["type"]==slot.type && row["sheet"]==slot.sheet && row["frame"]==slot.frame)
            row["native_signatures"]=nlohmann::json::array({std::string(64,'f')});
        NativePlayerCatalog badRaster(wrongRaster,art);auto p=fixture(slot);bool rasterRejected=false;
        try{badRaster.resolve(p,8,384,384*272,art);}catch(const std::invalid_argument& e){rasterRejected=std::string(e.what())=="player catalog unverified native raster";}
        assert(rasterRejected);++cases;
    }
    size_t densityCases=0;
    for(unsigned d:{8u,12u}){
        auto single=input;single["schema"]=2;single["density"]=d;
        for(auto& row:single["poses"])if(!row["assets"].empty())row["assets"].erase(std::to_string(d==8?12:8));
        std::map<std::string,OrderedSoldierAsset> selected;
        for(const auto& a:art)if(a.second.density==d)selected.emplace(a);
        NativePlayerCatalog one(single,selected,d);assert(one.isComplete());
        for(const auto& slot:CF1PlayerNativeSlots)if(slot.produced){
            auto p=fixture(slot);
            const auto result=one.resolve(p,d,384,384*272,selected);
            assert(result.decision==((slot.invisible || !slot.role)?SoldierArtDecision::KeepClassic:SoldierArtDecision::Replace));
            bool wrongDensity=false;
            try{one.resolve(p,d==8?12:8,384,384*272,selected);}catch(const std::invalid_argument& e){wrongDensity=std::string(e.what())=="player catalog requested density";}
            assert(wrongDensity);densityCases+=2;
        }
        auto wrongLabel=single;wrongLabel["density"]=d==8?12:8;rejects([&](){NativePlayerCatalog c(wrongLabel,selected,d);});
        auto fractional=single;fractional["density"]=double(d);rejects([&](){NativePlayerCatalog c(fractional,selected,d);});
        auto pair=single;pair["poses"]=input["poses"];rejects([&](){NativePlayerCatalog c(pair,art,d);});
        rejects([&](){NativePlayerCatalog c(single,selected);}); // schema2 cannot weaken schema1's paired contract
        auto incomplete=single;incomplete["poses"].erase(incomplete["poses"].begin());rejects([&](){NativePlayerCatalog c(incomplete,selected,d);});
        nlohmann::json manifest={{"version",4},{"density",d},{"assets",nlohmann::json::array()},
            {"bindings",nlohmann::json::array()},{"player_catalog",single}};
        for(const auto& a:selected){
            const auto& asset=a.second;std::vector<uint8_t> bytes(asset.pixels->size()*4);
            for(size_t i=0;i<asset.pixels->size();++i){auto c=(*asset.pixels)[i];bytes[4*i]=uint8_t(c>>16);bytes[4*i+1]=uint8_t(c>>8);bytes[4*i+2]=uint8_t(c);bytes[4*i+3]=uint8_t(c>>24);}
            const auto file="density-fixture-"+a.first+".rgba";std::ofstream out(file,std::ios::binary);
            out.write(reinterpret_cast<const char*>(bytes.data()),bytes.size());out.close();assert(out);
            manifest["assets"].push_back({{"id",a.first},{"file",file},{"width",asset.width},{"height",asset.height},
                {"density",d},{"sha256",SoldierSHA256(bytes)}});
        }
        OrderedSoldierRegistry registry(manifest);
        auto bad=manifest;bad["density"]=d==8?12:8;
        bool rejectedBeforeFiles=false;try{OrderedSoldierRegistry c(bad);}catch(const std::invalid_argument& e){rejectedBeforeFiles=std::string(e.what())=="ordered selected asset density";}
        assert(rejectedBeforeFiles);
        bad=manifest;bad["density"]=9;rejects([&](){OrderedSoldierRegistry c(bad);});
        bad=manifest;bad["player_catalog"]["density"]=d==8?12:8;rejects([&](){OrderedSoldierRegistry c(bad);});
        bad=manifest;bad["assets"]=nlohmann::json::array();
        auto huge=manifest["assets"][0];huge["width"]=352;huge["height"]=272;huge["file"]="never-open-budget.rgba";
        for(int i=0;i<4;++i){huge["id"]="budget-"+std::to_string(i);bad["assets"].push_back(huge);}
        bool unchangedBudget=false;try{OrderedSoldierRegistry c(bad);}catch(const std::length_error& e){unchangedBudget=std::string(e.what())=="ordered assets budget";}
        assert(unchangedBudget);
        for(const auto& row:manifest["assets"])std::remove(row["file"].get<std::string>().c_str());
        densityCases+=10;
    }
    std::printf("PASS selected-density catalog: %zu cases; complete 8x/12x independently, mismatch/corruption/incomplete and 64 MiB preflight rejected\n",densityCases);
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
