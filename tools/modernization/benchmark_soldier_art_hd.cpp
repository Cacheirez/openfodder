// GPL-3.0-or-later. Synthetic CPU cost probe; not frame rate or GPU measurement.
// Reuse tested scene/resource builders, never alter the production compositor.
#define main isolated_contract_main
#include "test_soldier_art_hd.cpp"
#undef main
#include <chrono>
#include <ctime>
#include <iomanip>
#include <stdexcept>
#ifdef __linux__
#include <sys/resource.h>
#endif
static volatile uint64_t consumed=0;
static uint64_t digest(const std::vector<uint32_t>& p) {
    uint64_t h=1469598103934665603ull;
    for(auto v:p){h^=v;h*=1099511628211ull;}return h;
}
int main(int argc,char** argv) {
    if(argc!=7)return 2;
    const int platform=std::stoi(argv[1]),complexity=std::stoi(argv[2]);
    const int mode=std::stoi(argv[3]),samples=std::stoi(argv[4]),warmup=std::stoi(argv[5]);
    const int round=std::stoi(argv[6]);
    if(platform<0||platform>2||complexity<0||complexity>1||samples<100||samples>10000||warmup<1)return 2;
    if(mode!=0&&mode!=1&&mode!=8&&mode!=12&&mode!=108&&mode!=112&&mode!=208&&mode!=212)return 2;
    const bool amiga=platform==1,layered=mode>200,blocked=mode>100&&!layered;
    const unsigned density=layered?unsigned(mode-200):(blocked?unsigned(mode-100):unsigned(mode));
    const size_t w=platform==2?352:320,h=platform==0?200:(platform==1?225:272);
    MissionLayerSequence scene;scene.destinations.push_back(destination(w,h));
    if(complexity)scene.destinations.push_back(destination(w,h));
    const auto id=scene.destinations[0].initial.destination;
    if(complexity)for(size_t n=0;n<64;++n){
        MissionLayer l;l.destination=scene.destinations[n%2].initial.destination;
        for(size_t k=0;k<1024;++k)l.pixels.put(16*w+16+(n*103+k*17)%((h-32)*w-32),uint8_t(1+(n+k)%254));
        scene.layers.push_back(std::move(l));
    }
    auto l=soldier(amiga,0);l.destination=id;scene.layers.push_back(l);
    if(blocked){MissionLayer occluder;occluder.destination=id;occluder.pixels.put(32*w+72,5);scene.layers.push_back(occluder);}
    const auto a=density>=8?asset(density):SoldierArtHDAsset{};
    const auto before=digest(RasterizeMissionLayers(scene,id).pixels);
    size_t outputBytes=0;unsigned effective=1;uint64_t firstHash=0,lastHash=0;
    auto compose=[&](bool fullHash){
        PresentationTarget target;
        if(mode==0)target=RasterizeMissionLayers(scene,id);
        else if(mode==1){auto result=ComposeSoldierArt(scene,id,true);if(!result.replaced)throw std::runtime_error("native inactive");target=std::move(result.target);}
        else if(layered){
            auto result=ComposeSoldierArtHDLayers(scene,id,true,a);
            if(result.status!=SoldierArtHDStatus::Replaced)throw std::runtime_error("layered inactive");
            outputBytes=result.background.pixels.size()*4+result.patch.size()*4;
            consumed+=result.patch.front()+result.patch.back()+result.background.pixels.front();
            return fullHash?(digest(result.background.pixels)^digest(result.patch)):uint64_t(0);
        }
        else {
            auto result=ComposeSoldierArtHD(scene,id,true,a);
            if((result.status==SoldierArtHDStatus::Replaced)!=!blocked)throw std::runtime_error("wrong HD path");
            effective=result.density;target=std::move(result.target);
        }
        if(target.destination!=id||target.width!=w*effective||target.height!=h*effective)throw std::runtime_error("invalid geometry");
        outputBytes=target.pixels.size()*sizeof(uint32_t);
        consumed+=target.pixels.front()+target.pixels[target.pixels.size()/2]+target.pixels.back();
        return fullHash?digest(target.pixels):uint64_t(0);
    };
    firstHash=compose(true);
    for(int i=0;i<warmup;++i)compose(false);
    std::vector<double> wall,cpu;wall.reserve(samples);cpu.reserve(samples);
    for(int i=0;i<samples;++i){
        const auto c0=std::clock();const auto start=std::chrono::steady_clock::now();
        compose(false); // Includes allocations, composition and destruction of the output.
        const auto end=std::chrono::steady_clock::now();const auto c1=std::clock();
        wall.push_back(std::chrono::duration<double,std::milli>(end-start).count());
        cpu.push_back(1000.0*(c1-c0)/CLOCKS_PER_SEC);
    }
    lastHash=compose(true);
    if(firstHash!=lastHash||before!=digest(RasterizeMissionLayers(scene,id).pixels))throw std::runtime_error("nondeterministic or mutated input");
    if(blocked&&firstHash!=before)throw std::runtime_error("fallback differs from classic");
    long rss=0;
#ifdef __linux__
    rusage usage{};if(getrusage(RUSAGE_SELF,&usage))return 3;rss=usage.ru_maxrss;
#endif
    std::cout<<std::setprecision(9)<<"{\"platform\":"<<platform<<",\"complexity\":"<<complexity
      <<",\"mode\":"<<mode<<",\"round\":"<<round<<",\"width\":"<<w<<",\"height\":"<<h
      <<",\"effective_density\":"<<effective<<",\"samples\":"<<samples<<",\"warmup\":"<<warmup
      <<",\"layers\":"<<scene.layers.size()<<",\"destinations\":"<<scene.destinations.size()
      <<",\"output_bytes\":"<<outputBytes<<",\"asset_bytes\":"<<(a.pixels?a.pixels->size()*4:0)
      <<",\"peak_process_rss_kib\":"<<rss<<",\"output_fnv64\":\""<<firstHash<<"\",\"wall_ms\":[";
    for(size_t i=0;i<wall.size();++i)std::cout<<(i?",":"")<<wall[i];
    std::cout<<"],\"cpu_ms\":[";for(size_t i=0;i<cpu.size();++i)std::cout<<(i?",":"")<<cpu[i];
    std::cout<<"]}\n";
}
