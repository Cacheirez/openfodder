// GPL-3.0-or-later. Visual proposal ONLY, not a runtime-compatible sprite asset.
// Fixed screen-space shift for shadow paint; body and logical anchor unchanged.
#include <cstdint>
#include <cstdlib>
#include <fstream>
#include <vector>
int main(int argc,char**argv){
 if(argc!=5)return 2;const int d=std::atoi(argv[4]);if(d!=8&&d!=12)return 2;
 const int width=16*d,bodyHeight=14*d,visualHeight=18*d;
 const size_t bytes=size_t(width)*bodyHeight*4;
 auto load=[&](const char* path){std::ifstream f(path,std::ios::binary|std::ios::ate);std::vector<uint8_t> v;
  if(f&&f.tellg()==std::streamoff(bytes)){f.seekg(0);v.resize(bytes);if(!f.read(reinterpret_cast<char*>(v.data()),bytes))v.clear();}return v;};
 const auto body=load(argv[1]),paint=load(argv[2]);if(body.empty()||paint.empty())return 3;
 std::vector<uint8_t> out(size_t(width)*visualHeight*4,0);
 for(int y=0;y<visualHeight;++y)for(int x=0;x<width;++x){
  const size_t n=4*(y*width+x);uint8_t b[4]={0,0,0,0},s[4]={0,0,0,0};
  if(y<bodyHeight)for(int k=0;k<4;++k)b[k]=body[n+k];
  const int px=x-3*d/4,py=y-2*d;
  if(px>=0&&px<width&&py>=0&&py<bodyHeight)for(int k=0;k<4;++k)s[k]=paint[4*(py*width+px)+k];
  if(!s[3]){for(int k=0;k<4;++k)out[n+k]=b[k];continue;}
  const unsigned a=b[3]*255+s[3]*(255-b[3]);if(!a)continue;
  for(int k=0;k<3;++k)out[n+k]=uint8_t((b[k]*b[3]*255+s[k]*s[3]*(255-b[3])+a/2)/a);
  out[n+3]=uint8_t((a+127)/255);
 }
 std::ofstream f(argv[3],std::ios::binary);f.write(reinterpret_cast<const char*>(out.data()),out.size());return f?0:4;
}
