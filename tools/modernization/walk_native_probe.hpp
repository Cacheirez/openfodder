// GPL-3.0-or-later. Diagnostic-copy only: bounded real resource snapshots.
// Never included by the shipped engine. Outputs may contain original game data;
// keep them local, including when the input is a commercial edition.
#pragma once
#include "Utils/SoldierVariant.hpp"
#include "Utils/json.hpp"
#include <fstream>
#include <set>
#include <cstdlib>
namespace openfodder {
inline void ExportWalkNativeSnapshot(const PreparedSpriteDraw& p,
        const std::array<uint32_t,255>& colors,const std::string& key){
    const char* directory=std::getenv("OPENFODDER_NATIVE_WALK_OUT");
    const auto& s=p.soldier;const auto& g=s.geometry;const auto& r=p.resource;
    if(!directory || !*directory || s.type!=0 || s.sheet<0 || s.sheet>7 ||
       s.frame<0 || s.frame>2 || !s.valid)return;
    static std::set<std::string> seen;
    if(seen.count(key))return;
    if(seen.size()>=512)throw std::length_error("native walk snapshot budget");
    if(!r.bytes || r.bytes->size()>1024*1024)throw std::length_error("native walk resource budget");
    const std::string prefix=std::string(directory)+"/";
    const auto hash=SoldierSHA256(*r.bytes);
    {std::ofstream out(prefix+hash+".bin",std::ios::binary);
     out.write(reinterpret_cast<const char*>(r.bytes->data()),r.bytes->size());
     if(!out)throw std::runtime_error("native walk resource output");}
    nlohmann::json row={
        {"schema",1},{"key",key},{"resource_sha256",hash},{"resource_file",hash+".bin"},
        {"colors",colors},{"format",int(g.format)},{"type",s.type},{"person",s.personType},
        {"sheet",s.sheet},{"frame",s.frame},{"animation",s.animation},{"segment",s.segment},
        {"vehicle",s.inVehicle},{"destroy",s.pendingDestroy},
        {"offset",r.offset},{"layout_width",r.layout.width},{"layout_height",r.layout.height},
        {"planes",r.layout.planes},{"resource_palette",r.palette},{"palette",g.palette},
        {"columns",g.columns},{"rows",g.rows},{"mod_x",g.modX},{"mod_y",g.modY},
        {"face",s.faceDirection},{"direction",s.direction},{"tick",s.tick}};
    {std::ofstream out(prefix+key+".json");out<<row.dump(2)<<"\n";
     if(!out)throw std::runtime_error("native walk metadata output");}
    seen.insert(key);
}
}
