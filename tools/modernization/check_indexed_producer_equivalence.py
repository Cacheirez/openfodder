"""Compare GUI raster/scene/minimap producers against their original bodies."""
import os,subprocess,tempfile
from pathlib import Path
from check_final_timer_equivalence import function
from pause_contract import canonical_pause
BASELINE='793e347cd9f118da1c9ec6a84f88caf3257b74c2'
def main():
 root=Path(__file__).resolve().parents[2]
 def get(path,sig,old=False):
  text=subprocess.check_output(['git','show',BASELINE+':'+path],cwd=root,text=True) if old else (root/path).read_text()
  return function(text,sig)
 for path in ['Source/GUI_Element.cpp','Source/Fodder.cpp','Source/Recruits.cpp','Source/Window.cpp']:
  current=(root/path).read_text()
  if path=='Source/Fodder.cpp': current=canonical_pause(current)
  assert current==subprocess.check_output(['git','show',BASELINE+':'+path],cwd=root,text=True),path
 for backend in ('PC','Amiga'):
  path=f'Source/{backend}/Graphics_{backend}.cpp'
  for name in ('Recruit_Sprite_Draw','Briefing_Intro_Helicopter_Play','Mission_Intro_DrawHelicopter'):
   sig=f'void cGraphics_{backend}::{name}('
   assert get(path,sig)==get(path,sig,True),sig
 h=r'''
#include "Utils/IndexedProducer.hpp"
#include <iostream>
#include <memory>
#include <cassert>
using namespace openfodder;
using uint8=uint8_t;using int8=int8_t;using uint16=uint16_t;using int16=int16_t;using uint32=uint32_t;
using tSharedBuffer=std::shared_ptr<std::vector<uint8>>;
uint16 readBEWord(const uint8* p){return (uint16(p[0])<<8)|p[1];}
struct cSurface {
 size_t w,h;std::vector<uint8> pixels;int clears=0;
 cSurface(size_t a=400,size_t b=280):w(a),h(b),pixels(a*(b+32),0xA5){}
 uint8* GetSurfaceBuffer(){return pixels.data()+16*w;}size_t GetWidth()const{return w;}size_t GetHeight()const{return h;}
 void clearBuffer(){++clears;std::fill(pixels.begin()+16*w,pixels.begin()+16*w+w*h,0);}
};
struct Header {uint16 mWidth=320,mHeight=256;uint8 mPlanes=4;};
struct Image {tSharedBuffer mData=std::make_shared<std::vector<uint8>>(120000);Header header;Header* GetHeader(){return &header;}};
struct Sheet {int mSpriteSheet=0;int16 mWidth=1,mHeight=3;size_t mOffset=10;};
struct Map {uint16 w,h;uint16 getWidth(){return w;}uint16 getHeight(){return h;}};
struct Params {bool mUnitTesting=false;};struct cGraphics;
struct cFodder {
 int16 mVideo_Draw_PosX=16,mVideo_Draw_PosY=16,mVideo_Draw_Columns=4,mVideo_Draw_Rows=3,mVideo_Draw_ColumnsMax=320;
 uint8 mVideo_Draw_PaletteIndex=0xE0;uint8* mVideo_Draw_FrameDataPtr=nullptr;
 size_t mDraw_Source_SkipPixelsPerRow=123,mDraw_Dest_SkipPixelsPerRow=456;
 cSurface* mSurfaceMapOverview=nullptr;cGraphics* mGraphics=nullptr;Params* mParams;Map* mMapLoaded;tSharedBuffer mMap;
 int16 mSurfaceMapTop=0,mSurfaceMapLeft=0;
 void OldOverview();void Map_Overview_Prepare();
};
struct cGraphics {
 cFodder* mFodder;cSurface* mSurface;bool legacy=false;
 virtual void MapOverview_Render_Tiles(uint16,uint16,uint16)=0;
 virtual IndexedProducerDraw CaptureOverviewTile(uint16,uint16,uint16)const=0;
 virtual ~cGraphics()=default;
};
struct Resource {tSharedBuffer bytes;tSharedBuffer fileGet(const std::string&){return bytes;}};
Resource* g_Resource;
std::string EnsureExtension(const std::string& s,const char*){return s;}
struct cGraphics_PC:cGraphics {
 uint32 paletteCount=0;const uint8* paletteSource=nullptr;
 void PaletteLoad(const uint8* p,uint32 n,uint32=0){paletteCount=n;paletteSource=p;}
 void OldImage(const std::string&,unsigned int,size_t);void Load_And_Draw_Image(const std::string&,unsigned int,size_t);
 std::vector<uint8*> mTile_Gfx_Ptrs;
 uint16 mMission_Intro_DrawX=3,mMission_Intro_DrawY=6416;
 SpriteRasterLayout GetSpriteRasterLayout()const{return {};}
 void Old16(const uint8* =nullptr);void Video_Draw_16(const uint8* =nullptr);
 void OldTile(uint16,uint16,uint16);void NewTile(uint16,uint16,uint16);
 void MapOverview_Render_Tiles(uint16 a,uint16 b,uint16 c)override{if(legacy)OldTile(a,b,c);else NewTile(a,b,c);}
 IndexedProducerDraw CaptureOverviewTile(uint16,uint16,uint16)const override;
 void OldMasked(tSharedBuffer,int16);void HeliIntro_BlitMaskedAlignedX(tSharedBuffer,int16);
 void OldOpaque(tSharedBuffer,int16);void HeliIntroBlit_OpaqueAlignedX(tSharedBuffer,int16);
};
struct cGraphics_Amiga:cGraphics {
 Header* mBMHD_Current; tSharedBuffer mBlkData;Image mImageService,mSpriteSheet_RankFont;Sheet stru_A918A[2];
 SpriteRasterLayout GetSpriteRasterLayout()const{SpriteRasterLayout l;l.format=SpriteDrawFormat::Amiga8;l.width=mBMHD_Current->mWidth;l.height=mBMHD_Current->mHeight;l.planes=mBMHD_Current->mPlanes;return l;}
 void Old16(const uint8* =nullptr);void Video_Draw_16(const uint8* =nullptr);
 void OldAlt(const uint8* =nullptr);void Video_Draw_8_Alt(const uint8* =nullptr);
 void OldOffset(int16);void Video_Draw_16_Offset(int16);
 void DrawPixels_8(uint8*,uint8*);void DrawPixels_16(uint8*,uint8*,uint8);void DrawPixel(uint8*,uint8*,uint16,uint16,uint16,uint16);
 void OldTile(uint16,uint16,uint16);void NewTile(uint16,uint16,uint16);
 void MapOverview_Render_Tiles(uint16 a,uint16 b,uint16 c)override{if(legacy)OldTile(a,b,c);else NewTile(a,b,c);}
 IndexedProducerDraw CaptureOverviewTile(uint16,uint16,uint16)const override;
 void OldService(int16,int16,int16);void Service_Draw(int16,int16,int16);
};
'''
 for backend,entries in [('PC',[('Load_And_Draw_Image','OldImage'),('Video_Draw_16','Old16'),('MapOverview_Render_Tiles','OldTile'),('HeliIntro_BlitMaskedAlignedX','OldMasked'),('HeliIntroBlit_OpaqueAlignedX','OldOpaque')]),('Amiga',[('Video_Draw_16','Old16'),('Video_Draw_8_Alt','OldAlt'),('Video_Draw_16_Offset','OldOffset'),('MapOverview_Render_Tiles','OldTile'),('Service_Draw','OldService')])]:
  path=f'Source/{backend}/Graphics_{backend}.cpp'
  for name,oldname in entries:
   sig=f'void cGraphics_{backend}::{name}('
   h+=get(path,sig,True).replace('::'+name+'(','::'+oldname+'(')
   body=get(path,sig)
   if name=='MapOverview_Render_Tiles':body=body.replace('::'+name+'(','::NewTile(')
   h+=body
  h+=get(path,f'openfodder::IndexedProducerDraw cGraphics_{backend}::CaptureOverviewTile(')
 for name in ['DrawPixel','DrawPixels_8','DrawPixels_16']:h+=get('Source/Amiga/Graphics_Amiga.cpp','void cGraphics_Amiga::'+name+'(',True)
 h+=get('Source/Map/MapRuntime.cpp','void cFodder::Map_Overview_Prepare(',True).replace('::Map_Overview_Prepare(','::OldOverview(')
 h+=get('Source/Map/MapRuntime.cpp','void cFodder::Map_Overview_Prepare(')
 h+=r'''
void stateEqual(const cFodder&a,const cFodder&b){assert(a.mVideo_Draw_Columns==b.mVideo_Draw_Columns&&a.mDraw_Source_SkipPixelsPerRow==b.mDraw_Source_SkipPixelsPerRow&&a.mDraw_Dest_SkipPixelsPerRow==b.mDraw_Dest_SkipPixelsPerRow&&a.mVideo_Draw_FrameDataPtr==b.mVideo_Draw_FrameDataPtr&&a.mVideo_Draw_PaletteIndex==b.mVideo_Draw_PaletteIndex);}
int main(){size_t raster=0,scenes=0,tiles=0,maps=0;
 auto data=std::make_shared<std::vector<uint8>>(120000);for(size_t i=0;i<data->size();++i)(*data)[i]=uint8(i*37+(i>>5));
 Header header;
 for(int kind=0;kind<4;++kind)for(uint8 planes:{1,4,5,8})for(int16 columns:{2,3,4,8})for(int16 rows:{0,1,9})for(int16 x:{0,16,392,400})for(int16 y:{-1,0,16,279}){
  // Guard legacy unbounded PC16/Amiga16 output while retaining Alt's peculiar edge rule.
  if(kind!=2&&(x>16||y<0||y+rows>280))continue;
  cSurface oldTarget,newTarget;cFodder a,b;a.mVideo_Draw_FrameDataPtr=data->data();a.mVideo_Draw_Columns=columns;a.mVideo_Draw_Rows=rows;a.mVideo_Draw_PosX=x;a.mVideo_Draw_PosY=y;b=a;
  cGraphics_PC pc1,pc2;cGraphics_Amiga am1,am2;pc1.mFodder=&a;pc2.mFodder=&b;am1.mFodder=&a;am2.mFodder=&b;pc1.mSurface=am1.mSurface=&oldTarget;pc2.mSurface=am2.mSurface=&newTarget;header.mPlanes=planes;am1.mBMHD_Current=am2.mBMHD_Current=&header;
  uint8 rowPalette[400]={};
  if(kind==0){pc1.Old16(rowPalette);pc2.Video_Draw_16(rowPalette);}if(kind==1){am1.Old16(rowPalette);am2.Video_Draw_16(rowPalette);}if(kind==2){am1.OldAlt(rowPalette);am2.Video_Draw_8_Alt(rowPalette);}if(kind==3){am1.OldOffset(17);am2.Video_Draw_16_Offset(17);}
  assert(oldTarget.pixels==newTarget.pixels);stateEqual(a,b);++raster;
 }
 for(int16 shift=0;shift<=320;++shift)for(uint16 rows:{1,3,9})for(bool masked:{false,true}){
  cSurface a,b;cFodder e;cGraphics_PC x,y;x.mFodder=y.mFodder=&e;x.mSurface=&a;y.mSurface=&b;x.mMission_Intro_DrawX=y.mMission_Intro_DrawX=rows;
  if(masked){x.OldMasked(data,shift==320?0:shift);y.HeliIntro_BlitMaskedAlignedX(data,shift);}else{x.OldOpaque(data,shift==320?0:shift);y.HeliIntroBlit_OpaqueAlignedX(data,shift);}assert(a.pixels==b.pixels);++scenes;
 }
 for(size_t length:{1,79,80,81,319})for(int16 shift:{0,17,319,320}){
  auto shortData=std::make_shared<std::vector<uint8>>(length,37);cSurface a,b;cFodder e;cGraphics_PC ga,gb;ga.mFodder=gb.mFodder=&e;ga.mSurface=&a;gb.mSurface=&b;
  ga.OldMasked(shortData,shift==320?0:shift);gb.HeliIntro_BlitMaskedAlignedX(shortData,shift);assert(a.pixels==b.pixels);++scenes;
 }
 for(int id=0;id<2;++id)for(int16 x:{0,17,80})for(int16 y:{0,19}){
  cSurface a,b;cFodder ea,eb;cGraphics_Amiga ga,gb;ga.mSurface=&a;gb.mSurface=&b;ga.mFodder=&ea;gb.mFodder=&eb;ga.mImageService.mData=gb.mImageService.mData=data;ga.mSpriteSheet_RankFont.mData=gb.mSpriteSheet_RankFont.mData=data;ga.stru_A918A[1].mSpriteSheet=gb.stru_A918A[1].mSpriteSheet=1;
  ga.OldService(id,x,y);gb.Service_Draw(id,x,y);assert(a.pixels==b.pixels);stateEqual(ea,eb);assert(ga.mBMHD_Current->mHeight==gb.mBMHD_Current->mHeight);++scenes;
 }
 for(unsigned colors:{0,16,255})for(size_t back:{0,7}){
  Resource resource{data};g_Resource=&resource;cSurface a,b;cGraphics_PC ga,gb;ga.mSurface=&a;gb.mSurface=&b;
  ga.OldImage("fixture",colors,back);gb.Load_And_Draw_Image("fixture",colors,back);
  assert(a.pixels==b.pixels&&a.clears==b.clears&&ga.paletteCount==gb.paletteCount&&ga.paletteSource==gb.paletteSource);++scenes;
 }
 std::vector<uint8*> tilePointers(512);for(size_t i=0;i<512;++i)tilePointers[i]=data->data()+(i%20)*16;
 for(int platform=0;platform<2;++platform)for(uint16 id=0;id<512;++id){
  cSurface a,b;cFodder ea,eb;ea.mSurfaceMapOverview=&a;eb.mSurfaceMapOverview=&b;cGraphics_PC pa,pb;cGraphics_Amiga aa,ab;pa.mFodder=aa.mFodder=&ea;pb.mFodder=ab.mFodder=&eb;pa.mTile_Gfx_Ptrs=pb.mTile_Gfx_Ptrs=tilePointers;aa.mBlkData=ab.mBlkData=data;
  if(platform==0){pa.OldTile(id,2,3);pb.NewTile(id,2,3);}else{aa.OldTile(id,2,3);ab.NewTile(id,2,3);}assert(a.pixels==b.pixels);++tiles;
 }
 for(int platform=0;platform<2;++platform)for(uint16 w:{1,3,6})for(uint16 h:{1,2,5})for(bool unit:{false,true})for(bool truncated:{false,true}){
  Map map{w,h};Params params{unit};auto bytes=std::make_shared<std::vector<uint8>>(0x60+w*h*2,0);for(size_t i=0;i<w*h;++i){uint16 id=(i*97)&511;memcpy(bytes->data()+0x60+i*2,&id,2);}if(truncated)bytes->resize(bytes->size()-2);
  cFodder a,b;a.mParams=b.mParams=&params;a.mMapLoaded=b.mMapLoaded=&map;a.mMap=b.mMap=bytes;a.mSurfaceMapOverview=new cSurface(32,32);b.mSurfaceMapOverview=new cSurface(32,32);
  cGraphics_PC pa,pb;cGraphics_Amiga aa,ab;cGraphics* ga=platform?static_cast<cGraphics*>(&aa):static_cast<cGraphics*>(&pa);cGraphics* gb=platform?static_cast<cGraphics*>(&ab):static_cast<cGraphics*>(&pb);ga->mFodder=&a;gb->mFodder=&b;ga->legacy=true;a.mGraphics=ga;b.mGraphics=gb;pa.mTile_Gfx_Ptrs=pb.mTile_Gfx_Ptrs=tilePointers;aa.mBlkData=ab.mBlkData=data;
  a.OldOverview();b.Map_Overview_Prepare();assert(a.mSurfaceMapTop==b.mSurfaceMapTop&&a.mSurfaceMapLeft==b.mSurfaceMapLeft);assert(a.mSurfaceMapOverview->pixels==b.mSurfaceMapOverview->pixels);assert(a.mSurfaceMapOverview->clears==b.mSurfaceMapOverview->clears);delete a.mSurfaceMapOverview;delete b.mSurfaceMapOverview;++maps;
 }
 ProducerGeometry g;g.x=16;g.y=16;g.columns=4;g.rows=3;auto capture=CaptureProducerRaster(ProducerRaster::Amiga16,data->data(),g,SpriteRasterLayout{SpriteDrawFormat::Amiga8,320,256,4},400,280);
 auto retained=capture.draw;std::fill(data->begin(),data->end(),0);data.reset();cSurface a,b;RasterizeIndexedProducer(capture.draw,a.GetSurfaceBuffer());capture={};RasterizeIndexedProducer(retained,b.GetSurfaceBuffer());assert(a.pixels==b.pixels);for(int i=0;i<3;++i){cSurface again;RasterizeIndexedProducer(retained,again.GetSurfaceBuffer());assert(a.pixels==again.pixels);}
 std::cout<<"PASS: "<<raster<<" raster, "<<scenes<<" scenes, "<<tiles<<" tiles, "<<maps<<" minimap constructors; original pixels/registers, owned decoded operations and repeated rendering\n";
}
'''
 with tempfile.TemporaryDirectory() as d:
  src=Path(d)/'test.cpp';src.write_text(h);exe=Path(d)/'test'
  subprocess.run(['g++','-std=c++14','-O1','-g','-fsanitize=address,undefined','-fno-sanitize-recover=all','-I'+str(root/'Source'),str(src),'-o',str(exe)],check=True)
  subprocess.run([str(exe)],check=True,env={**os.environ,'ASAN_OPTIONS':os.environ.get('ASAN_OPTIONS','detect_leaks=1')})
if __name__=='__main__':main()
