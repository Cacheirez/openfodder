"""Compare retained terrain with actual classic PC/Amiga MapTiles_Draw bodies.

Uses synthetic indexed maps/atlases, actual PC pointer-table preparation and
surface effects recorded by a stub. Does not claim SDL or full CD32 coverage.
GPL-3.0-or-later.
"""
import os
from pathlib import Path
import subprocess
import tempfile
from check_final_timer_equivalence import function

BASELINE = 'ff82fb6049def3d784bc09a3a3c2d7fc685f4ea5'

def main():
    root = Path(__file__).resolve().parents[2]
    def body(backend, signature, original=False):
        path = f'Source/{backend}/Graphics_{backend}.cpp'
        text = subprocess.check_output(['git', 'show', BASELINE+':'+path],cwd=root,text=True) if original else (root/path).read_text()
        return function(text, signature)
    harness = r'''
#include "Utils/TerrainDraw.hpp"
#include <iostream>
#include <array>
using namespace openfodder;
using uint8=uint8_t;using uint16=uint16_t;
using Buffer=std::shared_ptr<std::vector<uint8>>;
template<class T> T readLE(const uint8* p) { return T(p[0] | (uint16(p[1])<<8)); }
uint16 readBEWord(const uint8* p) { return (uint16(p[0])<<8)|p[1]; }
struct Map { size_t getWidth() const { return 29; } } map;
struct Engine {
 Buffer mMap,mTile_BaseBlk,mTile_SubBlk;
 int32_t mMapTile_Ptr=0;
 uint16 mMapTile_RowOffset=0,mMapTile_ColumnOffset=0;
 int rows=12,cols=20;
 Map* mMapLoaded=&map;
 int getWindowRows() const {return rows;} int getWindowColumns() const {return cols;}
};
Engine* g_Fodder;
struct cSurface {
 std::vector<uint8> pixels=std::vector<uint8>(400*256,0xA5),saved=pixels;
 std::vector<int> events;
 uint8* GetSurfaceBuffer(){return pixels.data();}
 size_t GetWidth() const{return 400;}
 size_t GetSurfaceBufferSize()const{return pixels.size();}
 void clearBuffer(){events.push_back(1);std::fill(pixels.begin(),pixels.end(),0);std::fill(saved.begin(),saved.end(),0);}
 void Save(){events.push_back(2);saved=pixels;}
};
'''
    classes=r'''
struct cGraphics_PC {
 Engine* mFodder; cSurface* mSurface; uint8* mTile_Gfx_Ptrs[480]{};
 TerrainAtlasCache mTerrainAtlas;
 void Tile_Prepare_Gfx(); void MapTiles_Draw(); TerrainDraw CaptureVisibleTerrain();
};
struct cGraphics_Amiga {
 Engine* mFodder; cSurface* mSurface; Buffer mBlkData;
 TerrainAtlasCache mTerrainAtlas;
 void MapTiles_Draw(); TerrainDraw CaptureVisibleTerrain();
};
'''
    harness+='namespace legacy {\n'+classes
    harness+=body('PC','void cGraphics_PC::Tile_Prepare_Gfx(',True)
    for backend in ('PC','Amiga'):
        harness+=body(backend,f'void cGraphics_{backend}::MapTiles_Draw(',True)
    harness+='}\nnamespace current {\n'+classes
    for backend in ('PC','Amiga'):
        harness+=body(backend,f'openfodder::TerrainDraw cGraphics_{backend}::CaptureVisibleTerrain(')
        harness+=body(backend,f'void cGraphics_{backend}::MapTiles_Draw(')
    harness+=r'''
}
int main(){
 Engine e;g_Fodder=&e;
 e.mMap=std::make_shared<std::vector<uint8>>(29*20*2);
 e.mTile_BaseBlk=std::make_shared<std::vector<uint8>>(61440);
 e.mTile_SubBlk=std::make_shared<std::vector<uint8>>(61440);
 auto amigaBytes=std::make_shared<std::vector<uint8>>(61440);
 for(size_t i=0;i<61440;++i){(*e.mTile_BaseBlk)[i]=(i*31+i/17)&255;(*e.mTile_SubBlk)[i]=(i*17+i/29+99)&255;(*amigaBytes)[i]=(i*19+i/43)&255;}
 for(size_t i=0;i<e.mMap->size()/2;++i){uint16 id=((i*37)&511)|0xB600;(*e.mMap)[i*2]=id;(*e.mMap)[i*2+1]=id>>8;}
 legacy::cGraphics_PC oldPC;oldPC.mFodder=&e;oldPC.Tile_Prepare_Gfx();
 current::cGraphics_PC newPC;newPC.mFodder=&e;
 legacy::cGraphics_Amiga oldAmiga;oldAmiga.mFodder=&e;oldAmiga.mBlkData=amigaBytes;
 current::cGraphics_Amiga newAmiga;newAmiga.mFodder=&e;newAmiga.mBlkData=amigaBytes;
 size_t count=0;
 for(bool amiga:{false,true}) for(int size:{0,1,2})
 for(int offset:{0,2,290,1154,1160}) for(int y=0;y<16;++y) for(int x=0;x<16;++x){
  e.rows=size==0?1:size==1?11:12;e.cols=size==0?2:size==1?18:20;
  e.mMapTile_Ptr=offset;e.mMapTile_RowOffset=y;e.mMapTile_ColumnOffset=x;
  cSurface before,after;
  TerrainDraw retained;
  if(amiga){oldAmiga.mSurface=&before;newAmiga.mSurface=&after;oldAmiga.MapTiles_Draw();retained=newAmiga.CaptureVisibleTerrain();if(!after.events.empty() || after.pixels!=after.saved || after.pixels[0]!=0xA5)return 9;newAmiga.MapTiles_Draw();}
  else{oldPC.mSurface=&before;newPC.mSurface=&after;oldPC.MapTiles_Draw();retained=newPC.CaptureVisibleTerrain();if(!after.events.empty() || after.pixels!=after.saved || after.pixels[0]!=0xA5)return 9;newPC.MapTiles_Draw();}
  if(before.pixels!=after.pixels || before.saved!=after.saved || before.events!=after.events){std::cerr<<"FAIL "<<amiga<<' '<<size<<' '<<offset<<' '<<x<<' '<<y<<'\n';return 1;}
  if(e.mMapTile_Ptr!=offset || e.mMapTile_RowOffset!=y || e.mMapTile_ColumnOffset!=x)return 2;
  cSurface pure;
  for(int i=0;i<3;++i)RasterizeTerrain(retained,pure.pixels.data(),pure.GetWidth(),pure.pixels.size());
  if(pure.pixels!=before.pixels || !pure.events.empty())return 3;
  ++count;
 }
 // Atlas contents and tile IDs outlive map edits, reloads and producer teardown.
 for(bool amiga:{false,true}){
  TerrainDraw retained;std::weak_ptr<const std::vector<uint8>> lifetime;
  cSurface expected;
  {
   TerrainAtlasCache cache;
   std::vector<uint8> bytes(61440,0x69),sub(61440,0xB3),mapBytes(64,0);
   for(size_t i=0;i<mapBytes.size();i+=2)mapBytes[i]=240;
   retained=PrepareTerrain(mapBytes,0,4,1,1,7,9,amiga?TerrainFormat::Amiga:TerrainFormat::PC,cache.capture(0,bytes),cache.capture(1,sub));
   auto reused=cache.capture(0,bytes);if(reused!=retained.base || reused.get()==&bytes)return 4;
   lifetime=retained.base;
   RasterizeTerrain(retained,expected.pixels.data(),400,expected.pixels.size());
   bytes[0]^=255;sub[0]^=255;mapBytes.assign(2,255);
   if(cache.capture(0,bytes)==retained.base || cache.capture(1,sub)==retained.sub)return 5;
   bytes.assign(123,0);cache.capture(0,bytes);
  }
  auto copied=retained;retained={};auto moved=std::move(copied);
  cSurface actual;RasterizeTerrain(moved,actual.pixels.data(),400,actual.pixels.size());
  if(actual.pixels!=expected.pixels || lifetime.expired())return 6;
  moved={};if(!lifetime.expired())return 7;
 }
 // Negative map origin skips a row without forming an invalid source pointer.
 std::vector<uint8> tinyMap(8,0);
 auto edge=PrepareTerrain(tinyMap,-8,4,0,0,0,0,TerrainFormat::PC,{});
 if(edge.tiles.size()!=2 || edge.tiles[0].y!=16)return 8;
 std::cout<<"PASS: "<<count<<" terrain pixel/background/effect cases; all 256 camera offsets, both atlas formats, retained lifetime and repeated rendering\n";
}
'''
    with tempfile.TemporaryDirectory(prefix='openfodder-terrain-') as folder:
        source=Path(folder)/'test.cpp'; binary=Path(folder)/'test'
        source.write_text(harness)
        subprocess.run(['g++','-std=c++14','-O1','-fsanitize=address,undefined','-fno-sanitize-recover=all','-I'+str(root/'Source'),str(source),'-o',str(binary)],check=True)
        subprocess.run([str(binary)],env=dict(os.environ,ASAN_OPTIONS=os.environ.get('ASAN_OPTIONS','detect_leaks=1')),check=True)

if __name__=='__main__':
    main()
