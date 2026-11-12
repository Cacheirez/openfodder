"""Emit the actual Window HD method with SDL software and controlled scene inputs."""
from pathlib import Path
import argparse, json
ROOT=Path(__file__).resolve().parents[2]
def build():
    method=(ROOT/'Source/WindowHD.cpp').read_text().split('int cWindow::TryRenderMissionHD',1)[1]
    matrix=json.loads((ROOT/'docs/modernization/evidence/soldier-coverage-matrix.json').read_text())
    tables=[]
    for platform in ('PC','Amiga'):
        rows=[r for r in matrix['walk24'] if r['platform']==platform and r['actor']=='player']
        rows.sort(key=lambda r:(r['direction'],r['frame']))
        assert [(r['direction'],r['frame']) for r in rows]==[(d,f) for d in range(8) for f in range(3)]
        tables.append('{'+','.join('{'+','.join(map(str,[r['sheet'],r['frame'],*[int(r['metadata'][i],0) for i in (0,2,3,4,5)]]))+'}' for r in rows)+'}')
    walk='static const int orderedWalkFixture[2][24][7]={'+','.join(tables)+'};\n'
    catalog=json.loads((ROOT/'docs/modernization/evidence/soldier-catalog.json').read_text())
    aim=[]
    for platform in ('PC','Amiga'):
        rows=catalog['platforms'][platform]['player']['groups'][6]['directions']
        assert [r['sheet'] for r in rows]==list(range(16,24))
        aim.append('{'+','.join('{'+','.join(map(str,[r['sheet'],0,*[int(r['frames'][0][i],0) for i in (0,2,3,4,5)]]))+'}' for r in rows)+'}')
    walk+='static const int orderedAimFixture[2][8][7]={'+','.join(aim)+'};\n'
    grenades=[]
    for platform in ('PC','Amiga'):
        rows=catalog['platforms'][platform]['player']['groups'][5]['directions']
        grenades.append('{'+','.join('{'+','.join(map(str,[r['sheet'],f,*[int(metadata[i],0) for i in (0,2,3,4,5)]]))+'}' for r in rows for f,metadata in enumerate(r['frames']))+'}')
    walk+='static const int orderedGrenadeFixture[2][24][7]={'+','.join(grenades)+'};\n'
    rockets=[]
    for platform in ('PC','Amiga'):
        rows=catalog['platforms'][platform]['player']['groups'][7]['directions']
        rockets.append('{'+','.join('{'+','.join(map(str,[r['sheet'],f,*[int(metadata[i],0) for i in (0,2,3,4,5)]]))+'}' for r in rows for f,metadata in enumerate(r['frames'][:3]))+'}')
    walk+='static const int orderedRocketFixture[2][24][7]={'+','.join(rockets)+'};\n'



    return r'''
#define OPENFODDER_HD_WINDOW_FIXTURE
#include "test_soldier_art_sdl.cpp"
#include "Utils/SoldierArtCompare.hpp"
#include "Utils/SoldierArtBatch.hpp"
#define SDL_CreateTexture create
#define SDL_DestroyTexture destroy
#define SDL_SetTextureBlendMode blend
#define SDL_SetTextureScaleMode scale
#define SDL_UpdateTexture update
#define SDL_RenderTexture render
#include "Utils/OrderedSoldierSDL.hpp"
#undef SDL_CreateTexture
#undef SDL_DestroyTexture
#undef SDL_SetTextureBlendMode
#undef SDL_SetTextureScaleMode
#undef SDL_UpdateTexture
#undef SDL_RenderTexture
#include "Utils/OrderedSoldierRegistry.hpp"
#include "Utils/OrderedSoldierCoverage.hpp"
#include "native_walk_snapshot.hpp"
#include <set>
#undef OPENFODDER_HD_WINDOW_FIXTURE
struct cSurface {
    MissionLayerSequence scene;bool active=true,adjusting=false,loaded=false;SDL_Texture* tex=nullptr;int verified=0;
    static bool MissionPublicationEnabled(){return std::string(std::getenv("OPENFODDER_PRESENT_MISSION_LAYERS"))=="1";}
    bool MissionAuditActive(){return active;}bool isLoadedImage(){return loaded;}bool isPaletteAdjusting(){return adjusting;}
    MissionLayerSequence VerifyMissionAudit(cSurface*){++verified;return scene;}
    PresentationSurface CapturePresentation(){return scene.destinations[0].initial;}
    SDL_Texture* GetTexture(){return tex;}
};
struct cFodder {
    cSurface* mSurface=nullptr; cSurface* mSurfaceFinal=nullptr;
    bool mPhase_In_Progress=true,mPhase_Paused=false,mPhase_ShowMapOverview=false,mInterruptCallback=false;
    uint64_t mPresentationScene=1;
} fodder; cFodder* g_Fodder=&fodder;
struct cWindow {SDL_Renderer* mRenderer=nullptr;int TryRenderMissionHD(cSurface*,const SDL_FRect&,const SDL_FRect&);};
'''+'int cWindow::TryRenderMissionHD'+method+r'''
static void env(const char* k,const char* v){
#ifdef _WIN32
    _putenv_s(k,v);
#else
    setenv(k,v,1);
#endif
}
'''+walk+r'''
int main(){
    env("OPENFODDER_PRESENT_MISSION_LAYERS","1");env("OPENFODDER_SOLDIER_ART","0");
    cSurface image,other;image.scene.destinations={destination(96,64)};
    auto body=soldier(false,0);body.destination=image.scene.destinations[0].initial.destination;image.scene.layers={body};
    auto checkReason=[&](MissionLayerSequence scene,const char* reason){
        auto result=ComposeSoldierArtHDLayers(scene,body.destination,true,asset(8));
        assert(result.status!=SoldierArtHDStatus::Replaced);
        assert(std::string(result.reason)==reason);
    };
    auto rejected=image.scene;rejected.layers[0].soldier.soldier.frame=1;
    checkReason(rejected,"no-eligible-c01");
    rejected=image.scene;rejected.destinations[0].initial.indexed.skipX=80;checkReason(rejected,"body-clipped");
    rejected=image.scene;rejected.layers.push_back(body);checkReason(rejected,"repeated-actor");
    rejected=image.scene;MissionLayer occluder;occluder.destination=body.destination;
    occluder.pixels.put(body.soldier.draw.y*96+body.soldier.draw.x,5);
    rejected.layers.push_back(occluder);checkReason(rejected,"later-layer-overlap");
    fodder.mSurface=&image;fodder.mSurfaceFinal=&other;
    auto surface=SDL_CreateSurface(192,128,SDL_PIXELFORMAT_XRGB8888);auto renderer=SDL_CreateSoftwareRenderer(surface);assert(renderer);
    auto classic=RasterizeMissionLayers(image.scene,body.destination);image.tex=texture(renderer,classic.pixels,96,64);
    cWindow win;win.mRenderer=renderer;SDL_FRect src{0,0,96,64},dst{0,0,192,128};
#ifdef OPENFODDER_EXTERNAL_ASSET_FIXTURE
    const auto checkWalkC01 = [](const std::vector<uint32_t>& pixels, unsigned density) {
        const auto original = SoldierBatchAsset(7, 0, density).pixels;
        assert(original && pixels.size() == original->size() && pixels != *original);
        for (size_t i = 0; i < pixels.size(); ++i)
            assert((pixels[i] >> 24) == ((*original)[i] >> 24));
    };
    if(std::getenv("OPENFODDER_A1_RANK_F4")){
        #include "rank_f4_cases.inc"
    } else if(std::getenv("OPENFODDER_ROCKET_ART")){
        #include "rocket_art_cases.inc"
    } else if(std::getenv("OPENFODDER_GRENADE_ART")){
        #include "grenade_art_cases.inc"
    } else if(std::getenv("OPENFODDER_AIM_ART")){
        #include "aim_art_cases.inc"
    } else if(std::getenv("OPENFODDER_WALK24_ART")){
        #include "walk24_art_cases.inc"
    } else if(std::getenv("OPENFODDER_WALK_NATIVE_REVIEW")){
        #include "walk_native_cases.inc"
    } else if(std::getenv("OPENFODDER_WALK_ART_REVIEW")){
        #include "walk_art_cases.inc"
    } else {
        #include "ordered_asset_cases.inc"
    }
#else
    for(const char* d:{"8","12"}){
        env("OPENFODDER_SOLDIER_HD",d);assert(win.TryRenderMissionHD(&image,src,dst)==1);
        for(bool* blocked:{&fodder.mPhase_Paused,&fodder.mPhase_ShowMapOverview,&fodder.mInterruptCallback,&image.adjusting,&image.loaded}){
            *blocked=true;int checks=image.verified;assert(win.TryRenderMissionHD(&image,src,dst)==-1 && image.verified==checks);*blocked=false;
            assert(win.TryRenderMissionHD(&image,src,dst)==1);
        }
        image.active=false;assert(win.TryRenderMissionHD(&image,src,dst)==-1);image.active=true;
        ++fodder.mPresentationScene;assert(win.TryRenderMissionHD(&image,src,dst)==-1);--fodder.mPresentationScene;
        assert(win.TryRenderMissionHD(&other,src,dst)==-1);
        assert(SDL_SetRenderScale(renderer,2,2));assert(win.TryRenderMissionHD(&image,src,dst)==-1);assert(SDL_SetRenderScale(renderer,1,1));
        env("OPENFODDER_SOLDIER_ART","1");assert(win.TryRenderMissionHD(&image,src,dst)==-1);env("OPENFODDER_SOLDIER_ART","0");
        env("OPENFODDER_PRESENT_MISSION_LAYERS","0");assert(win.TryRenderMissionHD(&image,src,dst)==-1);env("OPENFODDER_PRESENT_MISSION_LAYERS","1");
        assert(win.TryRenderMissionHD(&image,src,dst)==1);
    }
    env("OPENFODDER_SOLDIER_BATCH","1");
    for(const char* d:{"8","12"})for(int sheet:{2,7})for(int frame:{0,1,2}){
        env("OPENFODDER_SOLDIER_HD",d);auto selected=body;
        selected.soldier.soldier.sheet=sheet;selected.soldier.soldier.frame=frame;
        selected.soldier.resource.offset=(sheet==2?48:2248)+frame*8;
        image.scene.layers={selected};assert(win.TryRenderMissionHD(&image,src,dst)==1);
        image.adjusting=true;assert(win.TryRenderMissionHD(&image,src,dst)==-1);image.adjusting=false;
        assert(win.TryRenderMissionHD(&image,src,dst)==1);
        image.scene.layers[0].soldier.resource.offset++;assert(win.TryRenderMissionHD(&image,src,dst)==-1);
    }
    env("OPENFODDER_SOLDIER_BATCH","0");image.scene.layers={body};
    for(const char* d:{"0","bad","9"}){env("OPENFODDER_SOLDIER_HD",d);assert(win.TryRenderMissionHD(&image,src,dst)==-1);}
    #include "ordered_window_cases.inc"
#endif
    assert(live==0);SDL_DestroyTexture(image.tex);SDL_DestroyRenderer(renderer);SDL_DestroySurface(surface);
    std::cout<<"PASS actual Window HD method: enable/disable, pause/map/callback, palette, destination, scene generation, renderer state and resume\n";
}
'''
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--emit',type=Path,required=True);a=p.parse_args();a.emit.write_text(build())
