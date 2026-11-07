// GPL-3.0-or-later. Stable content identity; never a process generation or pointer.
#pragma once
#include "OrderedSoldierArt.hpp"
#include <string>
namespace openfodder {
// SHA-256 of a canonical byte sequence. Identity does not imply art approval.
inline std::string SoldierSHA256(std::vector<uint8_t> data) {
    static const uint32_t k[]={
        0x428a2f98,0x71374491,0xb5c0fbcf,0xe9b5dba5,0x3956c25b,0x59f111f1,0x923f82a4,0xab1c5ed5,
        0xd807aa98,0x12835b01,0x243185be,0x550c7dc3,0x72be5d74,0x80deb1fe,0x9bdc06a7,0xc19bf174,
        0xe49b69c1,0xefbe4786,0x0fc19dc6,0x240ca1cc,0x2de92c6f,0x4a7484aa,0x5cb0a9dc,0x76f988da,
        0x983e5152,0xa831c66d,0xb00327c8,0xbf597fc7,0xc6e00bf3,0xd5a79147,0x06ca6351,0x14292967,
        0x27b70a85,0x2e1b2138,0x4d2c6dfc,0x53380d13,0x650a7354,0x766a0abb,0x81c2c92e,0x92722c85,
        0xa2bfe8a1,0xa81a664b,0xc24b8b70,0xc76c51a3,0xd192e819,0xd6990624,0xf40e3585,0x106aa070,
        0x19a4c116,0x1e376c08,0x2748774c,0x34b0bcb5,0x391c0cb3,0x4ed8aa4a,0x5b9cca4f,0x682e6ff3,
        0x748f82ee,0x78a5636f,0x84c87814,0x8cc70208,0x90befffa,0xa4506ceb,0xbef9a3f7,0xc67178f2};
    uint32_t h[]={0x6a09e667,0xbb67ae85,0x3c6ef372,0xa54ff53a,0x510e527f,0x9b05688c,0x1f83d9ab,0x5be0cd19};
    const uint64_t bits=uint64_t(data.size())*8;data.push_back(0x80);
    while(data.size()%64!=56)data.push_back(0);
    for(int i=7;i>=0;--i)data.push_back(uint8_t(bits>>(8*i)));
    auto rotate=[](uint32_t x,unsigned n){return (x>>n)|(x<<(32-n));};
    for(size_t at=0;at<data.size();at+=64){
        uint32_t w[64];
        for(size_t i=0;i<16;++i){w[i]=0;for(size_t j=0;j<4;++j)w[i]=(w[i]<<8)|data[at+4*i+j];}
        for(size_t i=16;i<64;++i){const auto a=w[i-15],b=w[i-2];w[i]=w[i-16]+(rotate(a,7)^rotate(a,18)^(a>>3))+w[i-7]+(rotate(b,17)^rotate(b,19)^(b>>10));}
        uint32_t a=h[0],b=h[1],c=h[2],d=h[3],e=h[4],f=h[5],g=h[6],v=h[7];
        for(size_t i=0;i<64;++i){const uint32_t t=v+(rotate(e,6)^rotate(e,11)^rotate(e,25))+((e&f)^(~e&g))+k[i]+w[i];
            const uint32_t u=(rotate(a,2)^rotate(a,13)^rotate(a,22))+((a&b)^(a&c)^(b&c));
            v=g;g=f;f=e;e=d+t;d=c;c=b;b=a;a=t+u;}
        h[0]+=a;h[1]+=b;h[2]+=c;h[3]+=d;h[4]+=e;h[5]+=f;h[6]+=g;h[7]+=v;
    }
    const char hex[]="0123456789abcdef";std::string out;
    for(auto x:h)for(int i=7;i>=0;--i)out+=hex[(x>>(i*4))&15];return out;
}
inline std::string SoldierVariantKey(const PreparedSpriteDraw& p,const std::array<uint32_t,255>& colors) {
    const auto& s=p.soldier;const auto& g=s.geometry;const auto& r=p.resource;
    if(!s.valid || !r || g.source || g.format!=r.layout.format || p.draw.format!=g.format ||
       p.draw.palette!=g.palette)throw std::invalid_argument("soldier variant snapshot");
    const bool pc=g.format==SpriteDrawFormat::PC;
    const size_t stride=pc?160:r.layout.width/8;
    const int columns=pc?g.columns/2:(g.columns-1)*2;
    const size_t planes=pc?1:r.layout.planes;
    if((!pc && g.format!=SpriteDrawFormat::Amiga8) || !stride || columns<=0 ||
       size_t(columns)>stride || g.rows<=0 || g.rows>272 || !planes || planes>8 ||
       (!pc && (r.layout.width!=320 || !r.layout.height)))throw std::invalid_argument("soldier variant layout");
    const size_t last=(planes-1)*size_t(r.layout.height)*40+(size_t(g.rows)-1)*stride+size_t(columns);
    if(last>r.available())throw std::out_of_range("soldier variant resource extent");
    std::vector<uint8_t> bytes;
    auto value=[&](uint64_t v){for(unsigned i=0;i<8;++i)bytes.push_back(uint8_t(v>>(8*i)));};
    // Fixed-width LE metadata. Position, scene/slot/generation, clipping and clock
    // are absent: they do not select another artwork or animation phase.
    for(int64_t v:{int64_t(1),int64_t(g.format),int64_t(s.type),int64_t(s.personType),int64_t(s.sheet),
        int64_t(s.frame),int64_t(s.animation),int64_t(s.segment),int64_t(s.inVehicle),int64_t(s.pendingDestroy),
        int64_t(r.offset),int64_t(r.layout.width),int64_t(r.layout.height),int64_t(r.layout.planes),
        int64_t(r.palette),int64_t(g.palette),int64_t(g.columns),int64_t(g.rows),int64_t(g.modX),int64_t(g.modY)})value(uint64_t(v));
    for(size_t plane=0;plane<planes;++plane)for(size_t y=0;y<size_t(g.rows);++y){
        const auto first=r.source()+plane*size_t(r.layout.height)*40+y*stride;
        bytes.insert(bytes.end(),first,first+columns);
    }
    // Effective presentation colors, not a palette slot ID or fade target.
    for(auto color:colors)value(color&0xffffffu);
    return SoldierSHA256(std::move(bytes));
}
} // namespace openfodder
