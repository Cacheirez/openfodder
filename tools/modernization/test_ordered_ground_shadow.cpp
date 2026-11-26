// GPL-3.0-or-later. Tiny independent scenes, no private/native artwork needed.
#define main legacy_ordered_cpu_main
#include "test_ordered_soldier_art.cpp"
#undef main
#include "Utils/OrderedSoldierRegistry.hpp"
#include <cstdio>
#include <limits>
static nlohmann::json writeGroundAsset(const std::string& name,unsigned d,size_t w,size_t h,uint32_t pixel){
    std::vector<uint8_t> rgba(w*h*d*d*4);
    for(size_t i=0;i<rgba.size();i+=4){rgba[i]=uint8_t(pixel>>16);rgba[i+1]=uint8_t(pixel>>8);rgba[i+2]=uint8_t(pixel);rgba[i+3]=uint8_t(pixel>>24);}
    const std::string path=name+".rgba";std::ofstream f(path,std::ios::binary);f.write(reinterpret_cast<const char*>(rgba.data()),rgba.size());f.close();assert(f);
    return {{"id",name},{"file",path},{"width",w},{"height",h},{"density",d},{"sha256",SoldierSHA256(rgba)}};
}
int main(){
    size_t cases=0;
    for(bool amiga:{false,true})for(unsigned d:{8u,12u}){
        MissionLayerSequence scene;scene.destinations={surface()};auto id=scene.destinations[0].initial.destination;
        const auto colors=scene.destinations[0].initial.indexed.colors;
        auto a=body(amiga,id,20,20);auto& geometry=a.soldier.soldier.geometry;
        geometry.viewWidth=64;geometry.viewHeight=31;prepare(a);
        const auto key=SoldierVariantKey(a.soldier,colors);
        auto bodyAsset=writeGroundAsset("ground-test-body",d,16,14,0xffff0000u);
        auto shadowAsset=writeGroundAsset("ground-test-paint",d,2,3,0x80000000u);
        bodyAsset["ground_shadow"]={{"asset","ground-test-paint"},{"x_quarters",13},{"y_quarters",52},{"owner_type",0}};
        nlohmann::json manifest={{"version",2},{"assets",nlohmann::json::array({bodyAsset,shadowAsset})},
            {"bindings",nlohmann::json::array({{{"key",key},{"decision","replace-art"},{"assets",{{std::to_string(d),"ground-test-body"}}}}})}};
        OrderedSoldierRegistry registry(manifest);
        const auto resolve=[&](const PreparedSpriteDraw& p){return registry.resolve(p,SoldierVariantKey(p,colors),d);};
        const auto art=resolve(a.soldier);assert(art.groundShadow.pixels);
        for(int type:{5,36})for(int sheet=0x52;sheet<=0x59;++sheet)for(int animation:{0,1,50,51,52,90}){
            auto low=a.soldier;low.soldier.type=type;low.soldier.sheet=sheet;low.soldier.animation=animation;
            assert(OrderedGroundShadowEligible(low,type)==(animation==0 || animation==51));
            low.soldier.geometry.height=1;assert(!OrderedGroundShadowEligible(low,type));
            low.soldier.geometry.height=0;low.soldier.geometry.rowsToSkip=1;assert(!OrderedGroundShadowEligible(low,type));
        }
        for(int sheet:{0x38,0x9f,0xa4})for(int animation:{0,1,50,51,52}){
            auto pose=a.soldier;pose.soldier.sheet=sheet;pose.soldier.animation=animation;
            const bool eligible=sheet==0xa4?(animation>=50 && animation<=52):animation==0;
            assert(OrderedGroundShadowEligible(pose,0)==eligible);
            pose.soldier.geometry.rowsToSkip=1;assert(!OrderedGroundShadowEligible(pose,0));
            pose.soldier.geometry.rowsToSkip=0;pose.soldier.geometry.height=1;assert(!OrderedGroundShadowEligible(pose,0));
        }
        auto compose=[&](){return ComposeOrderedSoldierArt(scene,id,d,resolve);};
        {
            auto owner=a;owner.soldier.soldier.generation=9;owner.soldier.soldier.slot=3;
            auto owned=body(amiga,id,40,20);auto& proof=owned.soldier.nativeAmiga8;
            proof.cf1=true;proof.role=3;proof.scene=owner.soldier.soldier.scene;
            proof.ownerType=0;proof.ownerPerson=0;proof.ownerGeneration=9;proof.ownerSlot=3;
            scene.layers={owned,owner};
            auto withGround=[&](const PreparedSpriteDraw& p){return p.soldier.slot==3?art:OrderedSoldierAsset{SoldierArtDecision::KeepClassic};};
            auto noGround=[&](const PreparedSpriteDraw& p){auto v=withGround(p);v.groundShadow={};return v;};
            assert(ComposeOrderedSoldierArt(scene,id,d,withGround).cells==ComposeOrderedSoldierArt(scene,id,d,noGround).cells);
            scene.layers[0].soldier.nativeAmiga8.ownerGeneration=8;
            assert(ComposeOrderedSoldierArt(scene,id,d,withGround).cells!=ComposeOrderedSoldierArt(scene,id,d,noGround).cells);
        }
        const auto shade=SoldierBlend(0x80000000u,0xff112233u);
        // An enemy's separately ordered native shadow suppresses the optional
        // ground component even after its owner's person field changes late.
        for(int context:{0,1,2,3,4}){
            const int type=(context==2 || context==4)?36:5;
            auto owner=a;owner.soldier.soldier.generation=9;owner.soldier.soldier.slot=3;
            owner.soldier.soldier.type=type;owner.soldier.soldier.personType=context==0?0:1;
            owner.soldier.soldier.sheet=context>=3?0xa7:context==0?0x10:type==5?0x42:0xa8;
            owner.soldier.soldier.animation=(context==0 || context>=3)?51:0;
            owner.soldier.soldier.frame=context>=3?3:type==5?0:2;
            auto enemyArt=art;enemyArt.groundShadow.ownerType=type;
            auto owned=body(amiga,id,40,20);auto& proof=owned.soldier.nativeAmiga8;
            proof.cf1=true;proof.role=4;proof.scene=owner.soldier.soldier.scene;
            proof.ownerType=type;proof.ownerPerson=0;proof.ownerGeneration=9;proof.ownerSlot=3;
            scene.layers={owned,owner};
            auto withGround=[&](const PreparedSpriteDraw& p){return p.soldier.slot==3?enemyArt:OrderedSoldierAsset{SoldierArtDecision::KeepClassic};};
            auto noGround=[&](const PreparedSpriteDraw& p){auto v=withGround(p);v.groundShadow={};return v;};
            assert(ComposeOrderedSoldierArt(scene,id,d,withGround).cells==ComposeOrderedSoldierArt(scene,id,d,noGround).cells);
            scene.layers[0].soldier.nativeAmiga8.ownerGeneration=8;
            assert(ComposeOrderedSoldierArt(scene,id,d,withGround).cells!=ComposeOrderedSoldierArt(scene,id,d,noGround).cells);
        }
        scene.layers={a};auto f=compose();
        assert(f.complete()&&at(f,23,33,d/4)==0xffff0000u); // body covers its own shadow
        assert(at(f,23,34,0)==0xff112233u&&at(f,23,34,d/4)==shade);
        assert(at(f,24,35)==shade&&at(f,24,36)==0xff112233u);
        const size_t n=35*96+24;
        MissionLayer cover;cover.destination=id;
        for(uint8_t value:{uint8_t(0),uint8_t(5)}){
            cover.pixels.writes.clear();cover.pixels.put(n,value);
            scene.layers={a,cover};assert(!compose().cells.count(n));
            scene.layers={cover,a};assert(compose().cells.count(n));
        }
        MissionLayer save,restore;save.destination=restore.destination=id;
        save.operation=MissionLayerOperation::Save;restore.operation=MissionLayerOperation::Restore;
        scene.layers={a,save,cover,restore};assert(at(compose(),24,35)==shade);
        scene.layers={save,a,restore};assert(!compose().cells.count(n));
        auto b=body(amiga,id,23,34,1);b.soldier.soldier.geometry.viewWidth=64;b.soldier.soldier.geometry.viewHeight=31;prepare(b);
        auto actorResolve=[&](const PreparedSpriteDraw& p){auto selected=art;if(p.soldier.slot){selected.groundShadow={};selected.pixels=std::make_shared<const std::vector<uint32_t>>(224*d*d,0xff00ff00u);}return selected;};
        scene.layers={a,b};assert(at(ComposeOrderedSoldierArt(scene,id,d,actorResolve),24,35)==0xff00ff00u);
        scene.layers={b,a};assert(at(ComposeOrderedSoldierArt(scene,id,d,actorResolve),24,35)==SoldierBlend(0x80000000u,0xff00ff00u));
        MissionLayer terrain;terrain.destination=id;terrain.operation=MissionLayerOperation::Terrain;
        terrain.terrain.base=std::make_shared<const std::vector<uint8_t>>(5120,5);terrain.terrain.tiles={{0,23,34,0,0}};
        scene.layers={a,terrain};assert(at(compose(),24,35)==0xff112233u);
        scene.layers={a};bool rejected=false;
        try{ComposeOrderedSoldierArt(scene,id,d,resolve,224*4*d*d);}catch(const std::length_error&){rejected=true;}assert(rejected);
        for(int which=0;which<6;++which){
            auto changed=a;
            if(which==0)changed.soldier.soldier.geometry.height=12;
            if(which==1)changed.soldier.soldier.geometry.rowsToSkip=3;
            if(which==2)changed.soldier.soldier.animation=1;
            if(which==3)changed.soldier.soldier.sheet=0x28;
            if(which==4)changed.soldier.soldier.inVehicle=true;
            if(which==5)changed.soldier.soldier.pendingDestroy=true;
            prepare(changed);
            auto binding=manifest;binding["bindings"][0]["key"]=SoldierVariantKey(changed.soldier,colors);
            const OrderedSoldierRegistry selected(binding);
            auto selectedArt=selected.resolve(changed.soldier,SoldierVariantKey(changed.soldier,colors),d);
            assert(selectedArt.decision==SoldierArtDecision::Replace&&!selectedArt.groundShadow.pixels);
            scene.layers={changed};auto plain=selectedArt;plain.groundShadow={};
            assert(ComposeOrderedSoldierArt(scene,id,d,[&](const PreparedSpriteDraw&){return selectedArt;}).cells==
                   ComposeOrderedSoldierArt(scene,id,d,[&](const PreparedSpriteDraw&){return plain;}).cells);
        }
        auto badGeometry=a.soldier;badGeometry.soldier.geometry.rows=15;
        assert(registry.resolve(badGeometry,key,d).decision==SoldierArtDecision::Missing);
        for(int which=0;which<7;++which){
            auto bad=manifest;auto& shadow=bad["assets"][0]["ground_shadow"];
            if(which==0)shadow["asset"]="missing";
            if(which==1)shadow["asset"]="ground-test-body";
            if(which==2)shadow["x_quarters"]=0.5;
            if(which==3)shadow["y_quarters"]=1536;
            if(which==4)shadow["owner_type"]=1;
            if(which==5)shadow["x_quarters"]=std::numeric_limits<uint64_t>::max();
            if(which==6)shadow["extra"]=true;
            rejected=false;try{OrderedSoldierRegistry invalid(bad);}catch(const std::exception&){rejected=true;}assert(rejected);
        }
        // Cropping must preserve the quarter-cell screen offset of the shadow.
        auto left=body(amiga,id,-2,20);left.soldier.soldier.geometry.viewWidth=64;left.soldier.soldier.geometry.viewHeight=31;prepare(left);
        scene.layers={left};f=compose();assert(at(f,1,34,0)==0xff112233u&&at(f,1,34,d/4)==shade);
        auto bottom=body(amiga,id,20,48);bottom.soldier.soldier.geometry.viewWidth=64;bottom.soldier.soldier.geometry.viewHeight=31;prepare(bottom);
        scene.layers={bottom};f=compose();assert(!f.cells.count(62*96+24));
        std::remove("ground-test-body.rgba");std::remove("ground-test-paint.rgba");++cases;
    }
    std::cout<<"PASS ordered ground shadow: "<<cases<<" format/density groups; dimensions retained, ordered occlusion, Save/Restore, clipping, budgets, height/water/state exclusions and invalid metadata\n";
}
