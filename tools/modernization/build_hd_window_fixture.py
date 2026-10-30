"""Emit the actual Window HD method with SDL software and controlled scene inputs."""
from pathlib import Path
import argparse
ROOT=Path(__file__).resolve().parents[2]
def build():
    method=(ROOT/'Source/WindowHD.cpp').read_text().split('int cWindow::TryRenderMissionHD',1)[1]
    return r'''
#define OPENFODDER_HD_WINDOW_FIXTURE
#include "test_soldier_art_sdl.cpp"
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
int main(){
    env("OPENFODDER_PRESENT_MISSION_LAYERS","1");env("OPENFODDER_SOLDIER_ART","0");
    cSurface image,other;image.scene.destinations={destination(96,64)};
    auto body=soldier(false,0);body.destination=image.scene.destinations[0].initial.destination;image.scene.layers={body};
    fodder.mSurface=&image;fodder.mSurfaceFinal=&other;
    auto surface=SDL_CreateSurface(192,128,SDL_PIXELFORMAT_XRGB8888);auto renderer=SDL_CreateSoftwareRenderer(surface);assert(renderer);
    auto classic=RasterizeMissionLayers(image.scene,body.destination);image.tex=texture(renderer,classic.pixels,96,64);
    cWindow win;win.mRenderer=renderer;SDL_FRect src{0,0,96,64},dst{0,0,192,128};
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
    for(const char* d:{"0","bad","9"}){env("OPENFODDER_SOLDIER_HD",d);assert(win.TryRenderMissionHD(&image,src,dst)==-1);}
    assert(live==0);SDL_DestroyTexture(image.tex);SDL_DestroyRenderer(renderer);SDL_DestroySurface(surface);
    std::cout<<"PASS actual Window HD method: enable/disable, pause/map/callback, palette, destination, scene generation, renderer state and resume\n";
}
'''
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--emit',type=Path,required=True);a=p.parse_args();a.emit.write_text(build())
