// GPL-3.0-or-later. Reconstruct and verify a real snapshot before native raster.
// Output includes original artwork: local review only, never public by default.
#include "native_walk_snapshot.hpp"
#include <fstream>
#include <iostream>
using namespace openfodder;
int main(int argc,char** argv){
    if(argc!=4)return 2;
    try {
        nlohmann::json row;{std::ifstream file(argv[1]);file>>row;if(!file)return 3;}
        const auto p=LoadNativeWalkSnapshot(row,argv[2]);
        const auto& s=p.soldier;const auto& g=s.geometry;const auto& r=p.resource;
        const auto colors=row.at("colors").get<std::array<uint32_t,255>>();
        const size_t width=g.format==SpriteDrawFormat::PC?g.columns:(g.columns-1)*16;
        if(width==0 || width>352 || g.rows<=0 || g.rows>272)return 3;
        std::vector<uint8_t> indexed(width*g.rows);
        auto draw=p.draw;draw.source=r.source();draw.columns=g.columns;draw.rows=g.rows;draw.visible=true;
        RasterizeSprite8(draw,r.layout,{indexed.data(),width});
        std::vector<uint8_t> rgba;rgba.reserve(indexed.size()*4);
        for(auto index:indexed){
            if(index>=colors.size())return 3;
            const auto color=colors[index];
            for(int shift:{16,8,0})rgba.push_back(uint8_t(color>>shift));
            rgba.push_back(index?255:0);
        }
        {std::ofstream out(argv[3],std::ios::binary);out.write(reinterpret_cast<const char*>(rgba.data()),rgba.size());if(!out)return 3;}
        std::cout<<nlohmann::json({{"key",row.at("key")},{"width",width},{"height",g.rows},
            {"rgba_sha256",SoldierSHA256(rgba)},{"resource_sha256",row.at("resource_sha256")},
            {"format",row.at("format")},{"sheet",s.sheet},{"frame",s.frame}}).dump()<<"\n";
        return 0;
    }catch(const std::exception& e){std::cerr<<e.what()<<"\n";return 3;}
}
