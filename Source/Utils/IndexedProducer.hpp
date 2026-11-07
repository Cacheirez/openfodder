// GPL-3.0-or-later. Decoded pixel operations retained independently of resources.
#pragma once
#include "SpriteRaster.hpp"
#include <vector>
#include <algorithm>
#include <cstring>
#include <cstddef>
#include <cstdint>
namespace openfodder {
struct IndexedWrite { ptrdiff_t offset; uint8_t value; bool bitwiseOr; };
struct IndexedProducerDraw {
    std::vector<IndexedWrite> writes;
    void put(ptrdiff_t offset, uint8_t value) { writes.push_back({offset,value,false}); }
    void addBits(ptrdiff_t offset, uint8_t value) { writes.push_back({offset,value,true}); }
};
inline void RasterizeIndexedProducer(const IndexedProducerDraw& draw, uint8_t* target) {
    for (const auto& write : draw.writes) {
        if (write.bitwiseOr) target[write.offset] |= write.value;
        else target[write.offset] = write.value;
    }
}
enum class ProducerRaster { PC16, Amiga16, AmigaAlt, AmigaOffset };
struct ProducerGeometry {
    int16_t x=0,y=0,columns=0,rows=0,columnsMax=320,wrap=0;
    uint8_t palette=0;
};
struct ProducerCapture {
    IndexedProducerDraw draw;
    int16_t columns=0;
    size_t sourceSkip=0,destinationSkip=0;
    bool writesRegisters=true;
};
inline uint8_t ProducerPlanarPixel(const uint8_t* source, const SpriteRasterLayout& layout,
                                  size_t byteOffset, uint8_t bit, uint8_t planes) {
    uint8_t result=0;
    for(uint8_t p=0;p<planes;++p)
        if(source[byteOffset+size_t(layout.height)*40*p]&bit) result|=uint8_t(1<<p);
    return result;
}
// Reads resources only during capture. Commands own decoded indices, including
// explicit writes of zero and OR operations. Valid legacy extents are required.
inline ProducerCapture CaptureProducerRaster(ProducerRaster kind, const uint8_t* source,
        ProducerGeometry g, SpriteRasterLayout layout, size_t width, size_t height) {
    ProducerCapture out;out.columns=g.columns;
    if(kind==ProducerRaster::AmigaOffset){
        out.writesRegisters=false;
        for(int16_t y=0;y<g.rows;++y){
            uint16_t sx=0;
            auto pixel=[&](uint16_t x){
                const auto value=ProducerPlanarPixel(source,layout,(sx/8)+size_t(y)*40,
                    uint8_t(0x80>>(sx%8)),std::min<uint8_t>(layout.planes,5));
                if(value)out.draw.put(16+size_t(g.y)*width+size_t(y)*width+x,g.palette|value);
                ++sx;
            };
            for(uint16_t x=g.wrap;x<width-32;++x)pixel(x);
            for(uint16_t x=0;x<g.wrap;++x)pixel(x);
        }
        return out;
    }
    out.sourceSkip=(kind==ProducerRaster::PC16?g.columnsMax:(layout.width>>3))-g.columns;
    if(kind==ProducerRaster::Amiga16)out.columns>>=1;
    const int pixels=kind==ProducerRaster::PC16?1:(kind==ProducerRaster::Amiga16?16:8);
    out.destinationSkip=width-out.columns*pixels;
    ptrdiff_t dst=ptrdiff_t(width)*g.y+g.x;size_t src=0;
    for(int16_t y=0;y<g.rows;++y){
        const bool validRow=kind!=ProducerRaster::AmigaAlt||(g.y+y>=0&&g.y+y<int(height));
        if(validRow){
            for(int16_t x=0;x<out.columns;++x){
                if(kind==ProducerRaster::PC16){if(source[src])out.draw.put(dst,source[src]);}
                else if(kind!=ProducerRaster::AmigaAlt||(g.x+x*8>=0&&g.x+x*8<=int(width))){
                    for(int bit=0;bit<pixels;++bit){
                        const auto value=ProducerPlanarPixel(source,layout,src+bit/8,uint8_t(0x80>>(bit%8)),layout.planes);
                        if(value)out.draw.put(dst+bit,g.palette|value);
                    }
                }
                src+=pixels==16?2:1;dst+=pixels;
            }
        }else src+=g.columns;
        src+=out.sourceSkip;dst+=out.destinationSkip;
    }
    return out;
}
inline IndexedProducerDraw CaptureOverviewPC(const uint8_t* tile,uint16_t x,uint16_t y,size_t width){
    IndexedProducerDraw draw;x*=16;
    for(size_t row=0;row<16;++row)for(size_t col=0;col<16;++col)
        draw.put((size_t(y)*16+row)*width+x+col,tile[row*320+col]);
    return draw;
}
inline IndexedProducerDraw CaptureOverviewAmiga(const uint8_t* atlas,size_t size,uint16_t tile,
                                               uint16_t x,uint16_t y,size_t width){
    IndexedProducerDraw draw;x*=16;tile<<=7;size_t src=tile;
    for(uint16_t plane=0;plane<4;++plane){
        size_t dst=size_t(y)*16*width+x;
        for(uint16_t row=0;row<16;++row){
            if(src>=size)continue;
            uint16_t bits=(uint16_t(atlas[src])<<8)|atlas[src+1];src+=2;
            for(uint16_t bit=0;bit<16;++bit){if(bits&0x8000)draw.addBits(dst+bit,uint8_t(1<<plane));bits<<=1;}
            dst+=width;
        }
    }
    return draw;
}
inline IndexedProducerDraw CaptureSprite8Producer(const SpriteDrawState& input,
        const SpriteRasterLayout& layout, size_t width, const uint8_t* rowPalette=nullptr) {
    IndexedProducerDraw out;
    const auto regs=PrepareSpriteRasterRegisters(input,layout,width);
    const uint8_t* source=input.source+input.sourceOffset;
    ptrdiff_t dst=ptrdiff_t(width)*input.y+input.x;
    for(int16_t y=0;y<input.rows;++y){
        const uint8_t palette=input.format==SpriteDrawFormat::PC&&rowPalette?rowPalette[int16_t(input.y+y)]:input.palette;
        for(int16_t x=0;x<regs.columns;++x){
            if(input.format==SpriteDrawFormat::PC){
                const uint8_t a=*source>>4,b=*source&15;
                if(a)out.put(dst,palette|a);
                if(b)out.put(dst+1,palette|b);
                ++source;dst+=2;
            }else{
                for(int bit=0;bit<8;++bit){
                    const auto value=ProducerPlanarPixel(source,layout,0,uint8_t(0x80>>bit),layout.planes);
                    if(value)out.put(dst+bit,palette|value);
                }
                ++source;dst+=8;
            }
        }
        source+=regs.sourceSkip;dst+=regs.destinationSkip;
    }
    return out;
}
inline IndexedProducerDraw CapturePCSceneMasked(const uint8_t* data,size_t size,size_t width,uint16_t drawX,uint16_t drawY,int16_t pCx) {
 IndexedProducerDraw out;
    // Full-width wrap is zero; the old 320 branch read data[-1].
    if(pCx==320)pCx=0;

	const uint8_t* pDs = data;
	const uint8_t* pDsEnd = data + size;

	// Original works in 4-pixel groups
	const int16_t groupX = (pCx >> 2);
	int16_t ax = groupX;
	int16_t dx = ax;

	ax -= 80;
	int16_t word_4285F = -ax;

	const int planeShift = (pCx & 3); // <-- sub-pixel (0..3)

	// first 4-pixel group for pCx
	ptrdiff_t base = drawY + (dx * 4);

	++dx;

	// Loop the 4 source planes, but map them to dest planes with shift
	for (uint8_t srcPlane = 0; srcPlane < 4; ++srcPlane)
	{
		const int dstPlane = (srcPlane + planeShift) & 3;
		const int groupCarry = ((srcPlane + planeShift) >> 2) & 1;

		ptrdiff_t destPtr = base + (groupCarry * 4) + dstPlane;
		ptrdiff_t di = destPtr;

		for (int16_t bx = drawX; bx > 0; --bx)
		{
			int16_t cx;

			for (cx = word_4285F; cx > 0; --cx)
			{
				if (pDs >= pDsEnd)
					return out;

				uint8_t al = *pDs;
				if (al)
					out.put(di,al);

				++pDs;
				di += 4;
			}

			di -= width - 12 - 16;
			--pDs;

			for (cx = dx; cx > 0; --cx)
			{
				if (pDs >= pDsEnd)
					return out;

				uint8_t al = *pDs;
				if (al)
					out.put(di,al);

				++pDs;
				di += 4;
			}

			di += width;
		}
	}

 return out;
}
inline IndexedProducerDraw CapturePCSceneOpaque(const uint8_t* data,size_t size,size_t width,uint16_t drawX,uint16_t drawY,int16_t pCx) {
 IndexedProducerDraw out;
    // Full-width wrap is zero; the old 320 branch read data[-1].
    if(pCx==320)pCx=0;

	const uint8_t* Ds = data;

	// Original logic works in 4-pixel groups (80 groups for 320px wide).
	const int16_t groupX = (pCx >> 2);
	int16_t ax = groupX;
	int16_t dx = ax;

	ax -= 80;
	int16_t word_4285F = -ax;

	const int planeShift = (pCx & 3); // <-- the bit the old code discards

	// Base points at the first 4-pixel group for pCx, Y offset unchanged.
	ptrdiff_t base = drawY + (groupX * 4);

	++dx;

	for (uint8_t srcPlane = 0; srcPlane < 4; ++srcPlane)
	{
		// Map source plane (0..3) to the correct destination plane for pixel-accurate X.
		const int dstPlane = (srcPlane + planeShift) & 3;

		// If the plane rotation wraps (e.g. planeShift=3, srcPlane=2 -> 5),
		// that plane's pixels start one 4-pixel group later.
		const int groupCarry = ((srcPlane + planeShift) >> 2) & 1;

		// we might start in the next group depending on carry.
		ptrdiff_t destPtr = base + (groupCarry * 4) + dstPlane;
		ptrdiff_t di = destPtr;

		for (int16_t bx = drawX; bx > 0; --bx)
		{
			int16_t cx = word_4285F;

			if (cx & 1)
			{
				out.put(di,*Ds++);
				di += 4;
			}

			cx >>= 1;
			while (cx > 0)
			{
				out.put(di,*Ds++);
				di += 4;

				out.put(di,*Ds++);
				di += 4;

				--cx;
			}

			cx = dx;

			di -= width - 12 - 16;
			--Ds;

			if (cx & 1)
			{
				out.put(di,*Ds++);
				di += 4;
			}

			cx >>= 1;
			while (cx > 0)
			{
				out.put(di,*Ds++);
				di += 4;

				out.put(di,*Ds++);
				di += 4;

				--cx;
			}

			di += width;
		}
	}

 return out;
}
struct OverviewTilePlacement { uint16_t id,x,y; };
struct OverviewPlan {
    size_t side=0;
    int16_t left=0,top=0;
    std::vector<OverviewTilePlacement> tiles;
};
inline OverviewPlan CaptureOverviewPlan(const uint8_t* map,size_t size,uint16_t width,uint16_t height){
    OverviewPlan plan;plan.side=std::max(width,height);
    if(height<width)plan.top=std::max(0,int(width/2)-int(height/2));
    if(width<height)plan.left=std::max(0,int(height/2)-int(width/2));
    size_t offset=0x60;
    for(uint16_t y=0;y<height;++y)for(uint16_t x=0;x<width;++x,offset+=2){
        if(offset>=size)continue;
        uint16_t id;std::memcpy(&id,map+offset,2); // classic native-word interpretation
        plan.tiles.push_back({uint16_t(id&0x1FF),uint16_t(x+plan.left),uint16_t(y+plan.top)});
    }
    return plan;
}
inline IndexedProducerDraw CapturePCImage(const uint8_t* source,size_t width){
    IndexedProducerDraw draw;
    for(size_t plane=0;plane<4;++plane)for(size_t y=0;y<200;++y)for(size_t x=plane;x<320;x+=4)
        draw.put((16+y)*width+16+x,*source++);
    return draw;
}
} // namespace openfodder
