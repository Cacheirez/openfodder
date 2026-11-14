// GPL-3.0-or-later. Diagnostic snapshot reconstruction, never engine input.
#pragma once
#include "Utils/SoldierVariant.hpp"
#include "Utils/json.hpp"
#include <fstream>
namespace openfodder {
inline PreparedSpriteDraw LoadNativeWalkSnapshot(const nlohmann::json& row,const std::string& directory){
    const std::string digest=row.at("resource_sha256"),name=row.at("resource_file");
    if(digest.size()!=64 || digest.find_first_not_of("0123456789abcdef")!=std::string::npos || name!=digest+".bin")
        throw std::invalid_argument("native resource path");
    std::ifstream file(directory+"/"+name,std::ios::binary|std::ios::ate);
    if(!file || file.tellg()<=0 || file.tellg()>1024*1024)throw std::invalid_argument("native resource size");
    auto bytes=std::make_shared<std::vector<uint8_t>>(size_t(file.tellg()));file.seekg(0);
    if(!file.read(reinterpret_cast<char*>(bytes->data()),bytes->size()) || SoldierSHA256(*bytes)!=digest)
        throw std::invalid_argument("native resource hash");
    PreparedSpriteDraw p;auto& s=p.soldier;auto& g=s.geometry;auto& r=p.resource;
    s.valid=true;s.type=row.at("type");s.personType=row.at("person");s.sheet=row.at("sheet");s.frame=row.at("frame");
    s.animation=row.at("animation");s.segment=row.at("segment");s.inVehicle=row.at("vehicle");s.pendingDestroy=row.at("destroy");
    g.format=SpriteDrawFormat(row.at("format").get<int>());g.columns=row.at("columns");g.rows=row.at("rows");
    g.modX=row.at("mod_x");g.modY=row.at("mod_y");g.palette=row.at("palette");
    r.bytes=bytes;r.offset=row.at("offset");r.palette=row.at("resource_palette");r.layout.format=g.format;
    r.layout.width=row.at("layout_width");r.layout.height=row.at("layout_height");r.layout.planes=row.at("planes");
    p.draw.format=g.format;p.draw.palette=g.palette;
    const auto colors=row.at("colors").get<std::array<uint32_t,255>>();
    if(SoldierVariantKey(p,colors)!=row.at("key").get<std::string>())throw std::invalid_argument("native variant key");
    return p;
}
}
