// GPL-3.0-or-later. Private candidate validation with retained native banks.
#include "Utils/OrderedSoldierRegistry.hpp"
#include <iostream>
using namespace openfodder;
static void option(const char* key){
#ifdef _WIN32
    _putenv_s(key,"1");
#else
    setenv(key,"1",1);
#endif
}
static nlohmann::json jsonFile(const std::string& file){std::ifstream in(file);if(!in)throw std::runtime_error("candidate input missing");nlohmann::json v;in>>v;return v;}
int main(int argc,char** argv){try{
    if(argc!=4)throw std::invalid_argument("usage: validator candidate-directory pc-bank-directory amiga-bank-directory");
    option("OPENFODDER_PLAYER_CATALOG");option("OPENFODDER_ENEMY_CATALOG");
    const std::string directory=std::string(argv[1])+"/";
    const auto manifest=jsonFile(directory+"candidate-manifest.json");const unsigned density=manifest.at("density");
    OrderedSoldierRegistry registry=OrderedSoldierRegistry::Load(directory+"candidate-manifest.json");
    std::map<std::string,std::shared_ptr<const std::vector<uint8_t>>> banks;
    std::set<std::tuple<int,int,int,int,std::string>> seen;
    size_t modern=0,classic=0,hidden=0,shadows=0,ground=0,cases=0,aimTransitions=0,formatAnchors=0,fallHeights=0,initialShadows=0,initialAimRejections=0,initialAimOffStates=0,sinkingCrops=0;
    for(const auto& row:jsonFile(directory+"native-evidence.json")){
        const int fmt=row.at("format"),type=row.at("type"),sheet=row.at("sheet"),frame=row.at("frame");
        const auto* slot=FindCF1EnemyNativeSlot(fmt,type,sheet,frame);
        if(!slot || !slot->produced)throw std::runtime_error("candidate evidence source slot");
        const std::string sha=row.at("resource_sha256"),file=row.at("resource_file");
        if(sha.size()!=64 || sha.find_first_not_of("0123456789abcdef")!=std::string::npos || file!=sha+".bin")throw std::runtime_error("candidate evidence bank path");
        if(!seen.emplace(fmt,type,sheet,frame,sha).second)throw std::runtime_error("candidate duplicate evidence");
        if(!banks.count(sha)){
            const auto bankPath=std::string{argv[fmt+2]}+"/"+file;
            std::ifstream in(bankPath,std::ios::binary|std::ios::ate);
            if(!in || in.tellg()<=0 || in.tellg()>1024*1024)throw std::runtime_error("candidate native resource size");
            auto bytes=std::make_shared<std::vector<uint8_t>>(size_t(in.tellg()));in.seekg(0);
            if(!in.read(reinterpret_cast<char*>(bytes->data()),bytes->size()) || SoldierSHA256(*bytes)!=sha)throw std::runtime_error("candidate native resource hash");
            banks[sha]=bytes;
        }
        PreparedSpriteDraw p;auto& s=p.soldier;auto& g=s.geometry;auto& n=p.nativeAmiga8;auto& r=p.resource;
        s.valid=true;s.scene=1;s.generation=2;s.interval=3;s.slot=4;s.type=type;s.sheet=sheet;s.frame=frame;s.segment=slot->segment;
        s.personType=slot->personMask&1?0:slot->personMask&2?1:slot->personMask&4?2:0;
        g.format=SpriteDrawFormat(fmt);g.columns=slot->columns;g.rows=slot->rows;g.modX=slot->modX;g.modY=slot->modY;
        g.palette=slot->palette;g.spriteX=50;g.spriteY=50;
        const auto layoutHeight=row.at("layout_height").get<int>();
        if(layoutHeight<0 || layoutHeight>1024 || (fmt==1 && !layoutHeight))throw std::runtime_error("candidate native layout height");
        r.offset=slot->offset;r.layout={g.format,320,uint16_t(layoutHeight),uint8_t(fmt==1?4:1)};r.palette=g.palette;r.generation=5;r.bytes=banks.at(sha);
        n={s.type,s.sheet,s.frame,s.segment,uint16_t(r.offset),g.columns,g.rows,g.modX,g.modY,s.scene,s.generation,s.slot,r.generation,r.bytes};
        n.cf1=true;n.role=slot->role;n.layout=r.layout;n.palette=r.palette;n.frameOffset=slot->offset;
        if(slot->role==4){n.ownerType=5;n.ownerPerson=1;n.ownerGeneration=6;n.ownerSlot=0;}
        auto input=g;input.source=r.source();p.draw=PrepareSpriteDraw(input);p.draw.source=nullptr;
        if(CF1NativePoseSignature(p)!=row.at("native_signature"))throw std::runtime_error("candidate evidence raster differs");
        const bool empty=CF1NativePoseSignature(p)==CF1EmptyEnemyPoseSignature(NativeSpriteWidth(p),size_t(g.rows));
        if(empty!=row.at("no_write").get<bool>())throw std::runtime_error("candidate evidence no-write differs");
        const auto result=registry.resolve(p,"",density,true,384,384*272);
        if(type==5 && sheet>=0x5a && sheet<=0x61 && result.groundShadow.pixels)
            throw std::runtime_error("candidate swim unexpectedly received ground shadow");
        if((type==5 || type==36) && sheet>=0x62 && sheet<=0x71 && result.groundShadow.pixels)
            throw std::runtime_error("candidate damage unexpectedly received ground shadow");
        if(type==5 && sheet>=0x20 && sheet<=0x2f && result.groundShadow.pixels)
            throw std::runtime_error("candidate initial-person damage unexpectedly received ground shadow");
        if(type==5 && sheet>=0x72 && sheet<=0x74 && result.groundShadow.pixels)
            throw std::runtime_error("candidate mode-zero unexpectedly received ground shadow");
        if(type==5 && sheet==0x74 && frame==2 && result.decision==SoldierArtDecision::Replace){
            size_t bottom=0;
            for(size_t i=0;i<result.pixels->size();++i)
                if((*result.pixels)[i]>>24)bottom=i/(result.width*density)+1;
            if(bottom!=size_t(fmt==0?14:12)*density)
                throw std::runtime_error("candidate format-specific native foot anchor differs");
            ++formatAnchors;
        }
        if(((type==5 && sheet>=0xb0 && sheet<=0xbf) || (type==36 && sheet>=0xb8 && sheet<=0xbf)) && result.decision==SoldierArtDecision::Replace){
            for(const int height:{1,16}){
                auto falling=p;falling.soldier.geometry.height=height;
                auto geometry=falling.soldier.geometry;geometry.source=falling.resource.source();
                falling.draw=PrepareSpriteDraw(geometry);falling.draw.source=nullptr;
                const auto raised=registry.resolve(falling,"",density,true,384,384*272);
                if(raised.decision!=SoldierArtDecision::Replace || raised.pixels!=result.pixels || raised.groundShadow.pixels)
                    throw std::runtime_error("candidate falling height lost HD or gained ground");
                ++fallHeights;
            }
        }
        if((((type==5 || type==36) && sheet==0x7a) || (type==5 && sheet==0x38)) && result.decision==SoldierArtDecision::Replace){
            for(int skip=5;skip<13;++skip){
                auto sinking=p;sinking.soldier.geometry.rowsToSkip=skip;
                auto geometry=sinking.soldier.geometry;geometry.source=sinking.resource.source();
                sinking.draw=PrepareSpriteDraw(geometry);sinking.draw.source=nullptr;
                const auto cropped=registry.resolve(sinking,"",density,true,384,384*272);
                if(cropped.decision!=SoldierArtDecision::Replace || cropped.pixels!=result.pixels ||
                   cropped.groundShadow.pixels || sinking.draw.rows!=p.draw.rows-skip ||
                   sinking.draw.y!=p.draw.y+skip)
                    throw std::runtime_error("candidate sinking crop lost HD, anchor or gained ground");
                ++sinkingCrops;
            }
        }
        if(slot->role==4 && result.decision==SoldierArtDecision::Replace){
            auto initial=p;initial.nativeAmiga8.ownerPerson=0;
            const auto shadow=registry.resolve(initial,"",density,true,384,384*272);
            if(shadow.decision!=SoldierArtDecision::Replace || shadow.pixels!=result.pixels || shadow.groundShadow.pixels)
                throw std::runtime_error("candidate initial-person owned shadow lost HD");
            ++initialShadows;
        }
        if(type==36 && sheet>=0xa8 && sheet<=0xaf && frame==2 &&
           result.decision==SoldierArtDecision::Replace && !result.groundShadow.pixels)
            throw std::runtime_error("candidate rocket missing owner-specific ground");
        const bool initialAim=type==5 && sheet>=0x10 && sheet<=0x17;
        if((((type==5 || type==36) && sheet>=0x52 && sheet<=0x59) || initialAim) && result.decision==SoldierArtDecision::Replace){
            if(!result.groundShadow.pixels)throw std::runtime_error("candidate aim missing owner-specific ground");
            auto transition=p;transition.soldier.animation=51;
            if(!registry.resolve(transition,"",density,true,384,384*272).groundShadow.pixels)
                throw std::runtime_error("candidate post-slide aim missing ground");
            transition.soldier.geometry.height=1;
            auto airborne=transition.soldier.geometry;airborne.source=transition.resource.source();
            transition.draw=PrepareSpriteDraw(airborne);transition.draw.source=nullptr;
            if(registry.resolve(transition,"",density,true,384,384*272).groundShadow.pixels)
                throw std::runtime_error("candidate airborne aim retained ground");
            ++aimTransitions;
            if(initialAim){
                for(int animation:{50,52}){
                    auto off=p;off.soldier.animation=animation;
                    const auto excluded=registry.resolve(off,"",density,true,384,384*272);
                    if(excluded.decision!=SoldierArtDecision::Replace || excluded.groundShadow.pixels)
                        throw std::runtime_error("candidate initial aim off-state ground exclusion");
                    ++initialAimOffStates;
                }
                auto wrongPerson=p;wrongPerson.soldier.personType=1;
                bool rejected=false;
                try{registry.resolve(wrongPerson,"",density,true,384,384*272);}
                catch(const std::invalid_argument& e){rejected=std::string(e.what())=="enemy catalog logical state";}
                if(!rejected)throw std::runtime_error("candidate initial aim accepted wrong native person");
                ++initialAimRejections;
            }
        }
        if(result.decision==SoldierArtDecision::Replace){++modern;if(slot->role==4)++shadows;if(result.groundShadow.pixels)++ground;}
        else if(result.decision==SoldierArtDecision::KeepClassic){++classic;if(row.at("no_write")==true)++hidden;}
        else throw std::runtime_error("candidate known source became missing");
        ++cases;
    }
    for(const auto& slot:CF1EnemyNativeSlots)if(slot.produced)
        for(const auto& source:manifest.at("enemy_catalog").at("native_resources"))
            if(source.at("format")==slot.format && source.at("segment")==slot.segment &&
               !seen.count({slot.format,slot.type,slot.sheet,slot.frame,source.at("sha256").get<std::string>()}))
                throw std::runtime_error("candidate incomplete retained source evidence");
    std::cout<<"PASS private enemy candidate: "<<cases<<" retained native draws, density="<<density
        <<", modern="<<modern<<", classic="<<classic<<", resource-specific no-write="<<hidden<<", modern-owned-shadows="<<shadows<<", ground-components="<<ground<<", aim-owner-transitions="<<aimTransitions<<", format-native-anchors="<<formatAnchors<<", fall-height-transitions="<<fallHeights<<", initial-person-shadow-associations="<<initialShadows<<", initial-aim-source-rejections="<<initialAimRejections<<", initial-aim-off-state-exclusions="<<initialAimOffStates<<", sinking-native-crops="<<sinkingCrops<<"; not gameplay acceptance\n";
    return 0;
}catch(const std::exception& e){std::cerr<<"FAIL private enemy candidate: "<<e.what()<<"\n";return 1;}}
