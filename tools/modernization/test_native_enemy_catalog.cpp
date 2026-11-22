// GPL-3.0-or-later. Synthetic full-source enemy contracts, no commercial data.
#ifdef NDEBUG
#undef NDEBUG
#endif
#include "Utils/NativeEnemyCatalog.hpp"
#include "Utils/OrderedSoldierRegistry.hpp"
#include <cassert>
#include <cstdio>
using namespace openfodder;
template<class F> static void rejects(F f){bool caught=false;try{f();}catch(const std::exception&){caught=true;}assert(caught);}
static PreparedSpriteDraw enemyFixture(const EnemyNativeSlot& slot,bool empty=false){
    PreparedSpriteDraw p;auto& s=p.soldier;auto& g=s.geometry;auto& n=p.nativeAmiga8;auto& r=p.resource;
    s.valid=true;s.scene=1;s.generation=2;s.interval=3;s.slot=4;s.type=slot.type;
    s.sheet=slot.sheet;s.frame=slot.frame;s.segment=slot.segment;
    s.personType=slot.personMask&1?0:slot.personMask&2?1:slot.personMask&4?2:0;
    g.format=SpriteDrawFormat(slot.format);g.columns=slot.columns;g.rows=slot.rows;g.palette=slot.palette;
    g.modX=slot.modX;g.modY=slot.modY;g.spriteX=50;g.spriteY=50;
    r.offset=slot.offset;r.layout={g.format,320,256,4};r.palette=g.palette;r.generation=5;
    static const auto solid=std::make_shared<const std::vector<uint8_t>>(200000,255);
    static const auto zero=std::make_shared<const std::vector<uint8_t>>(200000,0);
    r.bytes=(empty || slot.invisible)?zero:solid;
    n={s.type,s.sheet,s.frame,s.segment,uint16_t(r.offset),g.columns,g.rows,g.modX,g.modY,s.scene,s.generation,s.slot,r.generation,r.bytes};
    n.cf1=true;n.role=slot.role;n.layout=r.layout;n.palette=r.palette;n.frameOffset=slot.offset;
    if(slot.role==4){n.ownerType=5;n.ownerPerson=1;n.ownerGeneration=6;n.ownerSlot=0;}
    auto input=g;input.source=r.source();p.draw=PrepareSpriteDraw(input);p.draw.source=nullptr;
    return p;
}
static void enemyOption(const char* key,const char* value){
#ifdef _WIN32
    _putenv_s(key,value);
#else
    setenv(key,value,1);
#endif
}
int main(){
    size_t cases=0;
    for(unsigned d:{8u,12u}){
        std::map<std::string,OrderedSoldierAsset> art;
        nlohmann::json input={{"schema",1},{"density",d},{"complete_art",false},
            {"native_resources",nlohmann::json::array()},{"poses",nlohmann::json::array()}};
        std::set<std::tuple<int,int,std::string>> resources;
        for(const auto& slot:CF1EnemyNativeSlots)if(slot.produced){
            auto p=enemyFixture(slot);auto zero=enemyFixture(slot,true);
            const auto sig=CF1NativePoseSignature(p),empty=CF1NativePoseSignature(zero);
            resources.emplace(slot.format,slot.segment,SoldierSHA256(*p.resource.bytes));
            resources.emplace(slot.format,slot.segment,SoldierSHA256(*zero.resource.bytes));
            auto signatures=nlohmann::json::array({sig});if(empty!=sig)signatures.push_back(empty);
            nlohmann::json ids=nlohmann::json::object();
            // A deliberate gap represents incomplete enemy artwork, never an
            // unknown source slot or a corrupt native raster.
            if(!slot.invisible && slot.role!=6 && !(slot.sheet==0x4a && slot.frame==1)){
                const auto id=std::to_string(NativeSpriteWidth(p))+"x"+std::to_string(slot.rows)+"-"+std::to_string(d);
                if(!art.count(id)){OrderedSoldierAsset a;a.decision=SoldierArtDecision::Replace;a.width=NativeSpriteWidth(p);
                    a.height=slot.rows;a.density=d;a.pixels=std::make_shared<const std::vector<uint32_t>>(a.width*a.height*d*d,0xff654321u);art[id]=a;}
                ids[std::to_string(d)]=id;
            }
            input["poses"].push_back({{"format",slot.format},{"type",slot.type},{"sheet",slot.sheet},{"frame",slot.frame},
                {"native_signatures",signatures},{"no_write_signatures",nlohmann::json::array({empty})},{"assets",ids}});
        }
        for(const auto& r:resources)input["native_resources"].push_back({{"format",std::get<0>(r)},{"segment",std::get<1>(r)},{"sha256",std::get<2>(r)}});
        NativeEnemyCatalog catalog(input,art,d);assert(!catalog.isArtComplete());
        for(const auto& slot:CF1EnemyNativeSlots){
            auto p=enemyFixture(slot);auto resolve=[&](){return catalog.resolve(p,d,384,384*272,art);};
            if(!slot.produced){rejects(resolve);++cases;continue;}
            const auto expected=(slot.invisible || slot.role==6 || (slot.sheet==0x4a && slot.frame==1))?SoldierArtDecision::KeepClassic:SoldierArtDecision::Replace;
            assert(resolve().decision==expected);++cases;
            p=enemyFixture(slot,true);assert(resolve().decision==SoldierArtDecision::KeepClassic);++cases;
            p=enemyFixture(slot);p.nativeAmiga8.role=0;rejects(resolve);++cases;
            p=enemyFixture(slot);p.nativeAmiga8.cf1=false;rejects(resolve);++cases;
            p=enemyFixture(slot);p.resource.generation++;rejects(resolve);++cases;
            p=enemyFixture(slot);p.soldier.geometry.rows++;rejects(resolve);++cases;
            p=enemyFixture(slot);p.nativeAmiga8.frameOffset++;rejects(resolve);++cases;
            p=enemyFixture(slot);p.draw.x++;rejects(resolve);++cases;
            p=enemyFixture(slot);rejects([&](){catalog.resolve(p,d==8?12:8,384,384*272,art);});++cases;
            p=enemyFixture(slot);auto changed=std::make_shared<std::vector<uint8_t>>(*p.resource.bytes);(*changed)[p.resource.offset]^=0x40;
            p.resource.bytes=changed;p.nativeAmiga8.bytes=changed;rejects(resolve);++cases;
            p=enemyFixture(slot);
            if(slot.role==2){
                p.soldier.personType=slot.personMask==4?1:2;rejects(resolve);++cases;
                p=enemyFixture(slot);p.soldier.animation=99;rejects(resolve);++cases;
            }
            if(slot.role==4){
                for(int owner:{5,36}){p=enemyFixture(slot);p.nativeAmiga8.ownerType=owner;
                    assert(resolve().decision==expected);++cases;
                    p.nativeAmiga8.ownerPerson=0;p.nativeAmiga8.ownerX+=7;p.nativeAmiga8.ownerHeight=30;
                    assert(resolve().decision==expected);++cases;}
                p=enemyFixture(slot);p.nativeAmiga8.ownerType=0;rejects(resolve);++cases;
                p=enemyFixture(slot);p.nativeAmiga8.ownerGeneration=0;rejects(resolve);++cases;
                p=enemyFixture(slot);p.nativeAmiga8.ownerSlot=p.soldier.slot;rejects(resolve);++cases;
            }
        }
        auto bad=input;bad["complete_art"]=true;rejects([&](){NativeEnemyCatalog c(bad,art,d);});++cases;
        bad=input;bad["poses"].erase(bad["poses"].begin());rejects([&](){NativeEnemyCatalog c(bad,art,d);});++cases;
        bad=input;bad["poses"][0]["sheet"]=999;rejects([&](){NativeEnemyCatalog c(bad,art,d);});++cases;
        bad=input;bad["poses"][0]["no_write_signatures"]=bad["poses"][0]["native_signatures"];
        rejects([&](){NativeEnemyCatalog c(bad,art,d);});++cases;
        bad=input;bad["poses"].back()=bad["poses"].front();rejects([&](){NativeEnemyCatalog c(bad,art,d);});++cases;
        bad=input;bad["density"]=double(d);rejects([&](){NativeEnemyCatalog c(bad,art,d);});++cases;
        bad=input;bad["poses"][0]["frame"]=0.5;rejects([&](){NativeEnemyCatalog c(bad,art,d);});++cases;
        bad=input;bad["schema"]=true;rejects([&](){NativeEnemyCatalog c(bad,art,d);});++cases;
        auto full=input;full["complete_art"]=true;
        for(auto& row:full["poses"])if(row["sheet"]==0x4a && row["frame"]==1)
            row["assets"]={{std::to_string(d),"16x14-"+std::to_string(d)}};
        NativeEnemyCatalog complete(full,art,d);assert(complete.isArtComplete());++cases;
        const auto& first=CF1EnemyNativeSlots[0];auto p=enemyFixture(first);
        auto bytes=std::make_shared<std::vector<uint8_t>>(*p.resource.bytes);(*bytes)[p.resource.offset]^=0x40;
        p.resource.bytes=bytes;p.nativeAmiga8.bytes=bytes;
        auto signedCorruption=input;signedCorruption["native_resources"].push_back({{"format",first.format},{"segment",first.segment},{"sha256",SoldierSHA256(*bytes)}});
        NativeEnemyCatalog guarded(signedCorruption,art,d);bool raster=false;
        try{guarded.resolve(p,d,384,384*272,art);}catch(const std::invalid_argument& e){raster=std::string(e.what())=="enemy catalog unverified raster";}
        assert(raster);++cases;
        // Exercise the actual manifest loader/dispatch, not only the resolver.
        nlohmann::json manifest={{"version",4},{"density",d},{"assets",nlohmann::json::array()},
            {"bindings",nlohmann::json::array()},{"enemy_catalog",input},
            {"player_catalog",{{"schema",2},{"density",d},{"complete",false},{"keep_verified_native",true},
                {"native_resources",input["native_resources"]},{"poses",nlohmann::json::array()}}}};
        for(const auto& item:art){const auto& a=item.second;std::vector<uint8_t> raw(a.pixels->size()*4);
            for(size_t i=0;i<a.pixels->size();++i){const auto c=(*a.pixels)[i];raw[4*i]=uint8_t(c>>16);raw[4*i+1]=uint8_t(c>>8);raw[4*i+2]=uint8_t(c);raw[4*i+3]=uint8_t(c>>24);}
            const auto file="enemy-fixture-"+item.first+".rgba";std::ofstream stream(file,std::ios::binary);
            stream.write(reinterpret_cast<const char*>(raw.data()),raw.size());stream.close();assert(stream);
            manifest["assets"].push_back({{"id",item.first},{"file",file},{"width",a.width},{"height",a.height},
                {"density",d},{"sha256",SoldierSHA256(raw)}});
        }
        enemyOption("OPENFODDER_PLAYER_CATALOG","1");enemyOption("OPENFODDER_ENEMY_CATALOG","1");
        OrderedSoldierRegistry registry(manifest);
        for(const auto& slot:CF1EnemyNativeSlots)if(slot.produced){
            auto command=enemyFixture(slot);
            assert(registry.resolve(command,"",d,true,384,384*272).decision==catalog.resolve(command,d,384,384*272,art).decision);++cases;
        }
        auto command=enemyFixture(*FindCF1EnemyNativeSlot(0,5,0x42,0));
        enemyOption("OPENFODDER_ENEMY_CATALOG","0");command.nativeAmiga8.role=0;
        assert(registry.resolve(command,"",d,true,384,384*272).decision==SoldierArtDecision::KeepClassic);++cases;
        enemyOption("OPENFODDER_ENEMY_CATALOG","1");rejects([&](){registry.resolve(command,"",d,true,384,384*272);});++cases;
        command=enemyFixture(*FindCF1EnemyNativeSlot(0,22,0x97,1));command.nativeAmiga8.role=0;
        rejects([&](){registry.resolve(command,"",d,true,384,384*272);});++cases;
        auto missingCatalog=manifest;missingCatalog.erase("enemy_catalog");OrderedSoldierRegistry missing(missingCatalog);
        command=enemyFixture(*FindCF1EnemyNativeSlot(0,5,0x42,0));
        rejects([&](){missing.resolve(command,"",d,true,384,384*272);});++cases;
        auto badFile=manifest;badFile["assets"][0]["sha256"]=std::string(64,'0');rejects([&](){OrderedSoldierRegistry invalid(badFile);});++cases;
        enemyOption("OPENFODDER_ENEMY_CATALOG","0");enemyOption("OPENFODDER_PLAYER_CATALOG","0");
        for(const auto& row:manifest["assets"])std::remove(row["file"].get<std::string>().c_str());
    }
    std::printf("PASS enemy native catalog: %zu cases, 679 produced source slots at 8x/12x; verified classic gaps, resource-specific zero draws, owners and corruption rejection\n",cases);
}
