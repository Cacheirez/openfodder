// GPL-3.0-or-later. Experimental per-draw HD presentation; classic by default.
#include "stdafx.hpp"
#include "Utils/SoldierArtSDL.hpp"
#include "Utils/SoldierArtCompare.hpp"
#include "c01_8.hpp"
#include "c01_12.hpp"
#include "Utils/SoldierArtBatch.hpp"

int cWindow::TryRenderMissionHD(cSurface* image,const SDL_FRect& src,const SDL_FRect& dst) {
    const char* option=std::getenv("OPENFODDER_SOLDIER_HD");
    if(!option || (std::string(option)!="8" && std::string(option)!="12"))return -1;
    // Opt-in, bounded diagnostics: each distinct reason once per process.
    auto report=[&](const char* reason){
        const char* trace=std::getenv("OPENFODDER_HD_DIAGNOSTICS");
        if(!trace || std::string(trace)!="1")return;
        static const char* seen[40]={};static unsigned count=0;
        for(unsigned i=0;i<count;++i)if(std::strcmp(seen[i],reason)==0)return;
        if(count<40){seen[count++]=reason;std::fprintf(stderr,
            "SOLDIER_HD_REASON: %s density=%s\n",reason,option);
            if(std::strncmp(reason,"sdl-error",9)==0)std::fprintf(stderr,"SOLDIER_HD_SDL_ERROR: %s\n",SDL_GetError());}
    };
    auto classic=[&](const char* reason){report(reason);return -1;};
    const char* native=std::getenv("OPENFODDER_SOLDIER_ART");
    if(native && std::string(native)=="1")return classic("native-art-enabled");
    if(!cSurface::MissionPublicationEnabled())return classic("publication-disabled");
    if(image!=g_Fodder->mSurface)return classic("not-mission-surface");
    if(!g_Fodder->mPhase_In_Progress)return classic("outside-mission");
    if(g_Fodder->mPhase_Paused)return classic("paused");
    if(g_Fodder->mPhase_ShowMapOverview)return classic("map-overview");
    if(g_Fodder->mInterruptCallback)return classic("scene-callback");
    if(image->isLoadedImage())return classic("loaded-image");
    if(image->isPaletteAdjusting())return classic("palette-transition");
    if(!image->MissionAuditActive())return classic("missing-audit-interval");
    float sx=0,sy=0;int w=0,h=0;
    SDL_RendererLogicalPresentation logical=SDL_LOGICAL_PRESENTATION_DISABLED;
    if(SDL_GetRenderTarget(mRenderer))return classic("renderer-target");
    if(SDL_RenderClipEnabled(mRenderer))return classic("renderer-clip");
    if(!SDL_GetRenderScale(mRenderer,&sx,&sy) || sx!=1 || sy!=1)return classic("renderer-scale");
    if(!SDL_GetRenderLogicalPresentation(mRenderer,&w,&h,&logical) ||
       logical!=SDL_LOGICAL_PRESENTATION_DISABLED)return classic("renderer-logical-presentation");
    // Verify the actual current interval and late palette, never a cached frame.
    // Oracle mismatches propagate, not an artistic fallback.
    const auto scene=image->VerifyMissionAudit(g_Fodder->mSurfaceFinal);
    const auto current=image->CapturePresentation();
    bool nonBlack=false;for(auto color:current.indexed.colors)nonBlack|=(color&0xffffffu)!=0;
    if(!nonBlack)return classic("black-palette");
    for(const auto& layer:scene.layers)
        if(layer.operation==openfodder::MissionLayerOperation::Soldier &&
           layer.soldier.soldier.scene!=g_Fodder->mPresentationScene)return classic("stale-scene");
    try {
        static const auto a8=std::make_shared<const std::vector<uint32_t>>(
            openfodder::SoldierArtPixels8().begin(),openfodder::SoldierArtPixels8().end());
        static const auto a12=std::make_shared<const std::vector<uint32_t>>(
            openfodder::SoldierArtPixels12().begin(),openfodder::SoldierArtPixels12().end());
        const bool high=std::string(option)=="12";
        openfodder::SoldierArtHDAsset asset;asset.density=high?12:8;asset.pixels=high?a12:a8;
        const char* batch=std::getenv("OPENFODDER_SOLDIER_BATCH");
        const bool useBatch=batch && std::string(batch)=="1";
        if(useBatch){
            asset=openfodder::SelectSoldierBatch(scene,current.destination,high?12:8);
            if(!asset.pixels)return classic("no-eligible-batch-key");
        }
        const auto composeStart=SDL_GetTicksNS();
        const auto frame=openfodder::ComposeSoldierArtHDLayers(scene,current.destination,true,asset);
        if(frame.status!=openfodder::SoldierArtHDStatus::Replaced)return classic(frame.reason);
        const auto composeNS=SDL_GetTicksNS()-composeStart;
        SDL_FRect patchRect;
        if(!openfodder::SoldierHDRect(frame,src,dst,patchRect))return classic("viewport-body-clipped");
        bool replaced=false;
        const auto renderStart=SDL_GetTicksNS();
        const bool drawn=openfodder::RenderSoldierHD(mRenderer,frame,image->GetTexture(),src,dst,replaced);
        if(!replaced)report(drawn?"sdl-error-classic-recovered":"sdl-error-recovery-failed");
        if(replaced){
            const char* diagnostics=std::getenv("OPENFODDER_HD_DIAGNOSTICS");
            if(useBatch && diagnostics && std::string(diagnostics)=="1"){
                static uint64_t published[6]={};
                const int key=(asset.sheet==2?0:3)+asset.frame;
                const auto count=++published[key];
                if(count==1 || count%256==0)std::fprintf(stderr,
                    "SOLDIER_BATCH_PUBLISHED: sheet=%d frame=%d count=%llu compose_ns=%llu sdl_ns=%llu\n",
                    asset.sheet,asset.frame,(unsigned long long)count,
                    (unsigned long long)composeNS,(unsigned long long)(SDL_GetTicksNS()-renderStart));
            }
            openfodder::SaveSoldierArtComparison(scene,current.destination,frame,src);
            static bool reported=false;
            if(!reported){std::fprintf(stderr,"SOLDIER_HD_SDL: published native background and HD patch\n");reported=true;}
        }
        return drawn?1:0;
    } catch(const std::bad_alloc&) {return classic("allocation-failed");}
}
