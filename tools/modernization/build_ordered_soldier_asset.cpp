// GPL-3.0-or-later. Exact RGBA export; no implicit resampling or pose inference.
#define STB_IMAGE_IMPLEMENTATION
#include "Utils/stb_image.h"
#include "Utils/SoldierVariant.hpp"
#include "Utils/json.hpp"
#include <fstream>
#include <iostream>
int main(int argc,char** argv) {
    if(argc!=7)return 2;
    try {
        auto number=[](const char* text,int limit){
            size_t end=0;const std::string s=text;const int value=std::stoi(s,&end);
            if(end!=s.size() || value<=0 || value>limit)throw std::invalid_argument("asset integer");return value;
        };
        const int width=number(argv[4],352),height=number(argv[5],272),density=number(argv[6],12);
        const std::string id=argv[3],path=argv[2];
        if((density!=8 && density!=12) || id.empty() || id.size()>128)return 2;
        int w=0,h=0,channels=0;
        if(!stbi_info(argv[1],&w,&h,&channels) || w!=width*density || h!=height*density)return 3;
        auto data=std::unique_ptr<unsigned char,void(*)(void*)>(stbi_load(argv[1],&w,&h,&channels,4),stbi_image_free);
        if(!data || w!=width*density || h!=height*density)return 3;
        const size_t bytes=size_t(w)*h*4;
        std::vector<uint8_t> rgba(data.get(),data.get()+bytes);
        const auto hash=openfodder::SoldierSHA256(rgba);
        std::ifstream existing(path,std::ios::binary|std::ios::ate);
        if(existing){
            // Repeating an identical export is safe; never overwrite a master
            // or a different derivative through an accidental output path.
            if(existing.tellg()!=std::streamoff(bytes))return 4;
            existing.seekg(0);std::vector<uint8_t> previous(bytes);
            if(!existing.read(reinterpret_cast<char*>(previous.data()),bytes) || previous!=rgba)return 4;
        } else {
            std::ofstream out(path,std::ios::binary);out.write(reinterpret_cast<const char*>(rgba.data()),std::streamsize(bytes));
            out.close();if(!out)return 4;
        }
        const auto slash=path.find_last_of("/\\");
        std::cout<<nlohmann::json({{"id",id},{"file",slash==std::string::npos?path:path.substr(slash+1)},
            {"width",width},{"height",height},{"density",density},{"sha256",hash}}).dump()<<"\n";
        return 0;
    } catch(const std::exception& e){std::cerr<<e.what()<<"\n";return 2;}
}
