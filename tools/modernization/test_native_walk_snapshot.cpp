// GPL-3.0-or-later. Synthetic fixture for real-snapshot exporter/reconstruction.
#include "walk_native_probe.hpp"
#include "native_walk_snapshot.hpp"
#include <cassert>
using namespace openfodder;
int main(int argc,char** argv){
    if(argc!=2)return 2;
#ifdef _WIN32
    _putenv_s("OPENFODDER_NATIVE_WALK_OUT",argv[1]);
#else
    setenv("OPENFODDER_NATIVE_WALK_OUT",argv[1],1);
#endif
    std::array<uint32_t,255> colors;
    for(size_t i=0;i<colors.size();++i)colors[i]=uint32_t(i*0x010203)&0xffffffu;
    for(int format:{0,1}){
        PreparedSpriteDraw p;auto& s=p.soldier;auto& g=s.geometry;auto& r=p.resource;
        s.valid=true;s.sheet=7;s.frame=0;
        g.format=SpriteDrawFormat(format);g.columns=format?2:16;g.rows=14;g.palette=format?0:0x30;
        r.layout.format=g.format;r.layout.width=320;r.layout.height=14;r.layout.planes=format?2:0;
        auto bytes=std::make_shared<std::vector<uint8_t>>(format?40*14*2:160*14,0);
        for(size_t y=0;y<14;++y){
            if(format){for(size_t x=0;x<2;++x){(*bytes)[40*y+x]=0xaa;(*bytes)[40*14+40*y+x]=0x55;}}
            else for(size_t x=0;x<8;++x)(*bytes)[160*y+x]=0x12;
        }
        r.bytes=bytes;r.palette=g.palette;p.draw.format=g.format;p.draw.palette=g.palette;
        const auto key=SoldierVariantKey(p,colors);ExportWalkNativeSnapshot(p,colors,key);
        nlohmann::json row;{std::ifstream file(std::string(argv[1])+"/"+key+".json");file>>row;assert(file);}
        const auto restored=LoadNativeWalkSnapshot(row,argv[1]);
        assert(SoldierVariantKey(restored,colors)==key && *restored.resource.bytes==*bytes);
        ExportWalkNativeSnapshot(p,colors,key); // Duplicates do not produce more rows.
    }
}
