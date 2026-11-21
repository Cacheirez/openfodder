// GPL-3.0-or-later. Offline authoring for ONE pilot, not engine shadow logic.
// The native 0x00/F1 lower dark component is the explicit placement mask.
#include <cstdint>
#include <cstdlib>
#include <fstream>
#include <vector>
int main(int argc,char**argv){
 if(argc!=5)return 2;
 const int d=std::atoi(argv[4]);if(d!=8&&d!=12)return 2;
 const size_t count=16*14*d*d*4;
 auto load=[&](const char* path){std::ifstream in(path,std::ios::binary|std::ios::ate);std::vector<uint8_t> v;
  if(in&&in.tellg()==std::streamoff(count)){in.seekg(0);v.resize(count);if(!in.read(reinterpret_cast<char*>(v.data()),count))v.clear();}return v;};
 const auto body=load(argv[1]),paint=load(argv[2]);if(body.empty()||paint.empty())return 3;
 std::vector<uint8_t> out=body;
 for(int y=0;y<14*d;++y)for(int x=0;x<16*d;++x){
  const int lx=x/d,ly=y/d;
  const bool mask=(ly==11&&lx>=5&&lx<=11)||(ly==12&&lx>=6&&lx<=11)||(ly==13&&lx>=8&&lx<=10);
  if(!mask)continue;
  const size_t n=4*(y*16*d+x);const unsigned b=body[n+3],s=paint[n+3];
  if(!s||b==255)continue;
  // Straight-alpha source-over: immutable body over generated shadow paint.
  const unsigned alphaNumerator=b*255+s*(255-b);
  if(!alphaNumerator)continue;
  for(int c=0;c<3;++c)out[n+c]=uint8_t((body[n+c]*b*255+paint[n+c]*s*(255-b)+alphaNumerator/2)/alphaNumerator);
  out[n+3]=uint8_t((alphaNumerator+127)/255);
 }
 std::ofstream file(argv[3],std::ios::binary);file.write(reinterpret_cast<const char*>(out.data()),out.size());return file?0:4;
}
