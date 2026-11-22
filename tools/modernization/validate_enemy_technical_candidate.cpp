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
    size_t modern=0,classic=0,hidden=0,shadows=0,ground=0,cases=0;
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
        <<", modern="<<modern<<", classic="<<classic<<", resource-specific no-write="<<hidden<<", modern-owned-shadows="<<shadows<<", ground-components="<<ground<<"; not gameplay acceptance\n";
    return 0;
}catch(const std::exception& e){std::cerr<<"FAIL private enemy candidate: "<<e.what()<<"\n";return 1;}}
