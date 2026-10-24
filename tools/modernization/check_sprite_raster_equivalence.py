"""Compare actual legacy PC/Amiga rasterizers with explicit-data drawing.

Checks every destination byte, transparency, palettes, register compatibility,
borrowed input preservation and repeated drawing. GPL-3.0-or-later.
"""
import argparse
import os
from pathlib import Path
import subprocess
import tempfile
from check_final_timer_equivalence import function

BASELINE = '77dac5410a7e92eee574a8da6aa231c8c0f5e88c'

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--compiler', default='g++')
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[2]
    def old(path, signature):
        return function(subprocess.check_output(['git', 'show', BASELINE + ':' + path], cwd=root, text=True), signature)
    harness = r'''
#include "Utils/IndexedProducer.hpp"
#include "Utils/SpriteRaster.hpp"
#include <array>
#include <vector>
#include <iostream>
using uint8 = uint8_t;
using uint16 = uint16_t;
using int16 = int16_t;
using namespace openfodder;
struct Engine {
    uint8* mVideo_Draw_FrameDataPtr;
    int16 mVideo_Draw_PosX, mVideo_Draw_PosY, mVideo_Draw_Columns, mVideo_Draw_Rows;
    uint8 mVideo_Draw_PaletteIndex;
    size_t mDraw_Source_SkipPixelsPerRow = 123, mDraw_Dest_SkipPixelsPerRow = 456;
};
struct cSurface {
    uint8* data; size_t width;
    uint8* GetSurfaceBuffer() { return data; }
    size_t GetWidth() { return width; }
};
struct Header { uint16 mWidth, mHeight; uint8 mPlanes; };
namespace legacy {
struct cGraphics_PC {
    Engine* mFodder; cSurface* mSurface;
    void Video_Draw_8(cSurface*, const uint8*);
};
struct cGraphics_Amiga {
    Engine* mFodder; cSurface* mSurface; Header* mBMHD_Current;
    void Video_Draw_8(cSurface*, const uint8*);
    void DrawPixels_8(uint8*, uint8*);
};
'''
    harness += old('Source/PC/Graphics_PC.cpp', 'void cGraphics_PC::Video_Draw_8(')
    harness += old('Source/Amiga/Graphics_Amiga.cpp', 'void cGraphics_Amiga::Video_Draw_8(')
    harness += old('Source/Amiga/Graphics_Amiga.cpp', 'void cGraphics_Amiga::DrawPixels_8(')
    harness += r'''
} // legacy
struct cGraphics {
    Engine* mFodder; cSurface* mSurface; SpriteRasterLayout layout;
    SpriteRasterLayout GetSpriteRasterLayout() const { return layout; }
    void Video_Draw_8(cSurface*, const uint8*);
    void Video_Draw_8_Prepared(const SpriteDrawState&, cSurface*, const uint8*);
};
'''
    current = (root / 'Source/Graphics.cpp').read_text()
    harness += function(current, 'void cGraphics::Video_Draw_8(')
    harness += function(current, 'void cGraphics::Video_Draw_8_Prepared(')
    harness += r'''
bool same(const Engine& a, const Engine& b) {
    return a.mVideo_Draw_FrameDataPtr == b.mVideo_Draw_FrameDataPtr &&
        a.mVideo_Draw_PosX == b.mVideo_Draw_PosX && a.mVideo_Draw_PosY == b.mVideo_Draw_PosY &&
        a.mVideo_Draw_Columns == b.mVideo_Draw_Columns && a.mVideo_Draw_Rows == b.mVideo_Draw_Rows &&
        a.mVideo_Draw_PaletteIndex == b.mVideo_Draw_PaletteIndex &&
        a.mDraw_Source_SkipPixelsPerRow == b.mDraw_Source_SkipPixelsPerRow &&
        a.mDraw_Dest_SkipPixelsPerRow == b.mDraw_Dest_SkipPixelsPerRow;
}
bool same(const SpriteDrawState& a, const SpriteDrawState& b) {
    return a.source == b.source && a.sourceOffset == b.sourceOffset && a.x == b.x && a.y == b.y &&
        a.columns == b.columns && a.rows == b.rows && a.palette == b.palette &&
        a.visible == b.visible && a.format == b.format;
}
int main() {
    std::array<uint8, 65536> source;
    std::array<uint8, 256> palettes;
    for (size_t i=0; i<palettes.size(); ++i) palettes[i] = (i % 16) << 4;
    size_t cases = 0;
    for (int pattern : {0,1,2}) {
      for (size_t i=0; i<source.size(); ++i)
        source[i] = pattern == 0 ? 0 : pattern == 1 ? 255 : uint8((i * 37 + i / 11) & 255);
      const auto savedSource = source;
      for (auto format : {SpriteDrawFormat::PC, SpriteDrawFormat::Amiga8})
      for (int planes : {1,4,5,8}) {
       if (format == SpriteDrawFormat::PC && planes != 1) continue;
       for (int width : {352,672})
       for (int x : {0,1,63})
       for (int y : {0,1,17})
       for (int columns : {1,2,3,4,8,16})
       for (int rows : {1,2,32})
       for (int offset : {0,7,160})
       for (bool usePalette : {false,true}) {
        // Guard regions are included in the full output comparison.
        std::vector<uint8> expected(width * 256 + 128, 0xA5), actual = expected;
        cSurface oldTarget{expected.data()+64,size_t(width)}, newTarget{actual.data()+64,size_t(width)};
        Header header{uint16(width == 352 ? 320 : 640),128,uint8(planes)};
        SpriteRasterLayout layout;
        layout.format = format; layout.width = header.mWidth; layout.height = header.mHeight; layout.planes = planes;
        const auto savedLayout = layout;
        SpriteDrawState draw;
        draw.source = source.data(); draw.sourceOffset = offset;
        draw.x = x; draw.y = y; draw.columns = columns; draw.rows = rows;
        draw.palette = 0x30; draw.format = format; draw.visible = true;
        const auto savedDraw = draw;
        Engine oldEngine{source.data()+offset,int16(x),int16(y),int16(columns),int16(rows),0x30};
        const auto initial = oldEngine;
        const uint8* rowPalette = usePalette ? palettes.data() : nullptr;
        legacy::cGraphics_PC pc{&oldEngine,&oldTarget};
        legacy::cGraphics_Amiga amiga{&oldEngine,&oldTarget,&header};
        // Exercise both the default and explicit destination paths.
        if (format == SpriteDrawFormat::PC) pc.Video_Draw_8(usePalette ? &oldTarget : nullptr,rowPalette);
        else amiga.Video_Draw_8(usePalette ? &oldTarget : nullptr,rowPalette);
        for (int repeat=0; repeat<3; ++repeat) {
          RasterizeSprite8(draw,layout,{newTarget.data,newTarget.width},rowPalette);
          if (actual != expected || !same(draw,savedDraw) || source != savedSource ||
              layout.format != savedLayout.format || layout.width != savedLayout.width ||
              layout.height != savedLayout.height || layout.planes != savedLayout.planes) {
            std::cerr << "FAIL pure/repeat case " << cases << '\n'; return 1;
          }
        }
        std::fill(actual.begin(), actual.end(), 0xA5);
        Engine newEngine = initial;
        cGraphics graphics{&newEngine,&newTarget,layout};
        graphics.Video_Draw_8(usePalette ? &newTarget : nullptr,rowPalette);
        if (actual != expected || !same(oldEngine,newEngine)) {
          std::cerr << "FAIL legacy adapter case " << cases << '\n'; return 2;
        }
        std::fill(actual.begin(), actual.end(), 0xA5);
        // Prepared route must not read engine geometry/source/palette registers.
        newEngine = initial;
        newEngine.mVideo_Draw_FrameDataPtr = nullptr;
        newEngine.mVideo_Draw_PosX = -123; newEngine.mVideo_Draw_PosY = -456;
        newEngine.mVideo_Draw_Rows = -10; newEngine.mVideo_Draw_PaletteIndex = 0xFF;
        Engine expectedEngine = newEngine;
        expectedEngine.mVideo_Draw_Columns = oldEngine.mVideo_Draw_Columns;
        expectedEngine.mDraw_Source_SkipPixelsPerRow = oldEngine.mDraw_Source_SkipPixelsPerRow;
        expectedEngine.mDraw_Dest_SkipPixelsPerRow = oldEngine.mDraw_Dest_SkipPixelsPerRow;
        graphics.Video_Draw_8_Prepared(draw,usePalette ? &newTarget : nullptr,rowPalette);
        if (actual != expected || !same(expectedEngine,newEngine) || !same(draw,savedDraw)) {
          std::cerr << "FAIL prepared adapter case " << cases << '\n'; return 3;
        }
        ++cases;
       }
      }
    }
    std::cout << "PASS: " << cases << " raster cases match legacy pixels and registers; inputs unchanged; repeated drawing identical\n";
}
'''
    with tempfile.TemporaryDirectory(prefix='openfodder-raster-') as folder:
        source = Path(folder) / 'raster.cpp'
        binary = Path(folder) / 'raster'
        source.write_text(harness)
        subprocess.run([args.compiler, '-std=c++14', '-O1', '-fsanitize=address,undefined',
                        '-fno-sanitize-recover=all', '-I' + str(root / 'Source'),
                        str(source), '-o', str(binary)], check=True)
        subprocess.run([str(binary)], env=dict(os.environ, ASAN_OPTIONS='detect_leaks=0'), check=True)

if __name__ == '__main__':
    main()
