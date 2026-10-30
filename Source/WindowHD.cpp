// GPL-3.0-or-later. Experimental per-draw HD presentation; classic by default.
#include "stdafx.hpp"
#include "Utils/SoldierArtSDL.hpp"
#include "c01_8.hpp"
#include "c01_12.hpp"

int cWindow::TryRenderMissionHD(cSurface* image,const SDL_FRect& src,const SDL_FRect& dst) {
    const char* option=std::getenv("OPENFODDER_SOLDIER_HD");
    if(!option || (std::string(option)!="8" && std::string(option)!="12"))return -1;
    const char* native=std::getenv("OPENFODDER_SOLDIER_ART");
    if((native && std::string(native)=="1") || !cSurface::MissionPublicationEnabled() ||
       image!=g_Fodder->mSurface || !g_Fodder->mPhase_In_Progress ||
       g_Fodder->mPhase_Paused || g_Fodder->mPhase_ShowMapOverview ||
       g_Fodder->mInterruptCallback || image->isLoadedImage() ||
       image->isPaletteAdjusting() || !image->MissionAuditActive())return -1;
    float sx=0,sy=0;int w=0,h=0;
    SDL_RendererLogicalPresentation logical=SDL_LOGICAL_PRESENTATION_DISABLED;
    if(SDL_GetRenderTarget(mRenderer) || SDL_RenderClipEnabled(mRenderer) ||
       !SDL_GetRenderScale(mRenderer,&sx,&sy) || sx!=1 || sy!=1 ||
       !SDL_GetRenderLogicalPresentation(mRenderer,&w,&h,&logical) ||
       logical!=SDL_LOGICAL_PRESENTATION_DISABLED)return -1;
    // Verify the actual current interval and late palette, never a cached frame.
    // Oracle mismatches propagate, not an artistic fallback.
    const auto scene=image->VerifyMissionAudit(g_Fodder->mSurfaceFinal);
    const auto current=image->CapturePresentation();
    bool nonBlack=false;for(auto color:current.indexed.colors)nonBlack|=(color&0xffffffu)!=0;
    if(!nonBlack)return -1;
    for(const auto& layer:scene.layers)
        if(layer.operation==openfodder::MissionLayerOperation::Soldier &&
           layer.soldier.soldier.scene!=g_Fodder->mPresentationScene)return -1;
    try {
        static const auto a8=std::make_shared<const std::vector<uint32_t>>(
            openfodder::SoldierArtPixels8().begin(),openfodder::SoldierArtPixels8().end());
        static const auto a12=std::make_shared<const std::vector<uint32_t>>(
            openfodder::SoldierArtPixels12().begin(),openfodder::SoldierArtPixels12().end());
        const bool high=std::string(option)=="12";
        openfodder::SoldierArtHDAsset asset;asset.density=high?12:8;asset.pixels=high?a12:a8;
        const auto frame=openfodder::ComposeSoldierArtHDLayers(scene,current.destination,true,asset);
        if(frame.status!=openfodder::SoldierArtHDStatus::Replaced)return -1;
        bool replaced=false;
        const bool drawn=openfodder::RenderSoldierHD(mRenderer,frame,image->GetTexture(),src,dst,replaced);
        if(replaced){
            static bool reported=false;
            if(!reported){std::fprintf(stderr,"SOLDIER_HD_SDL: published native background and HD patch\n");reported=true;}
        }
        return drawn?1:0;
    } catch(const std::bad_alloc&) {return -1;}
}
