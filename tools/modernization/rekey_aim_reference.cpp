// GPL-3.0-or-later. Local diagnostic reconstruction from verified resource bytes.
// Input/output contain original palettes: never commit or distribute them.
#include "native_walk_snapshot.hpp"
#include <iostream>
using namespace openfodder;
int main(int argc,char**argv){
 if(argc!=4)return 2;
 try{
  nlohmann::json input;{std::ifstream f(argv[1]);f>>input;if(!f)return 3;}
  auto row=input.at("template");auto p=LoadNativeWalkSnapshot(row,argv[2]);
  const auto& m=input.at("metadata");auto& s=p.soldier;auto& g=s.geometry;
  s.sheet=input.at("sheet");s.frame=0;s.faceDirection=input.at("direction").get<int>()*2;
  p.resource.offset=m.at(0);g.modX=m.at(2);g.modY=m.at(3);g.columns=m.at(4);g.rows=m.at(5);g.palette=m.at(6);
  p.draw.format=g.format;p.draw.palette=g.palette;
  row["sheet"]=s.sheet;row["frame"]=0;row["face"]=s.faceDirection;
  row["offset"]=p.resource.offset;row["mod_x"]=g.modX;row["mod_y"]=g.modY;row["columns"]=g.columns;row["rows"]=g.rows;row["palette"]=g.palette;
  const auto colors=row.at("colors").get<std::array<uint32_t,255>>();
  row["key"]=SoldierVariantKey(p,colors);row["derivation"]="source-table reconstruction from verified real resource; not runtime observation";
  row["source_key"]=input.at("template").at("key");
  // Reconstruct again through the normal verifier before emitting the reference.
  LoadNativeWalkSnapshot(row,argv[2]);
  std::ofstream f(argv[3]);f<<row.dump(2)<<"\n";return f?0:3;
 }catch(const std::exception&e){std::cerr<<e.what()<<"\n";return 3;}
}
