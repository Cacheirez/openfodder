"""Compare value-only clipping with actual accepted legacy PC/Amiga bodies.

The legacy reference is compiled with minimal register/window stubs, not SDL.
Checks visible and rejected geometry, offsets and repeatability. GPL-3.0-or-later.
"""
import argparse
from pathlib import Path
import subprocess
import tempfile
from check_final_timer_equivalence import function

BASELINE = 'a2f63090fc0732787df8ba56cc142e9938771d9c'

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--compiler', default='g++')
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[2]
    def original(path, signature):
        text = subprocess.check_output(['git', 'show', BASELINE + ':' + path], cwd=root, text=True)
        return function(text, signature)
    bodies = '\n'.join([
        original('Source/Graphics.cpp', 'bool cGraphics::Sprite_OnScreen_ClipY('),
        original('Source/Graphics.cpp', 'bool cGraphics::Sprite_OnScreen_ClipBottom()'),
        original('Source/PC/Graphics_PC.cpp', 'bool cGraphics_PC::Sprite_OnScreen_Check()'),
        original('Source/Amiga/Graphics_Amiga.cpp', 'bool cGraphics_Amiga::Sprite_OnScreen_Check(bool p16bit)'),
    ])
    harness = r'''
#include "Utils/SpriteDrawState.hpp"
#include <array>
#include <iostream>
using int16 = int16_t;
struct Engine {
    int16 mVideo_Draw_PosX, mVideo_Draw_PosY, mVideo_Draw_Columns, mVideo_Draw_Rows;
    uint8_t* mVideo_Draw_FrameDataPtr;
    int16 width;
    int16 getWindowWidth() const { return width; }
};
struct Window {
    int16 height;
    Window GetScreenSize() const { return *this; }
    int16 getHeight() const { return height; }
};
Window window;
Window* g_Window = &window;
struct cGraphics {
    Engine* mFodder;
    bool Sprite_OnScreen_ClipY(int16);
    bool Sprite_OnScreen_ClipBottom();
};
struct cGraphics_PC : cGraphics { bool Sprite_OnScreen_Check(); };
struct cGraphics_Amiga : cGraphics { bool Sprite_OnScreen_Check(bool); };
'''
    harness += bodies
    harness += r'''
using namespace openfodder;
bool same(const SpriteDrawState& a, const SpriteDrawState& b) {
    return a.source == b.source && a.sourceOffset == b.sourceOffset &&
           a.x == b.x && a.y == b.y && a.columns == b.columns &&
           a.rows == b.rows && a.palette == b.palette && a.visible == b.visible && a.format == b.format;
}
int main() {
    std::array<uint8_t, 131072> bytes{};
    uint8_t* source = bytes.data() + 32768;
    size_t cases = 0;
    for (auto format : {SpriteDrawFormat::PC, SpriteDrawFormat::Amiga8, SpriteDrawFormat::Amiga16})
    for (int width : {320, 640})
    for (int height : {200, 240})
    for (int x : {-300,-129,-65,-33,-17,-9,-2,-1,0,1,15,31,319,320,350,351,352,639,670,671,672})
    for (int y : {-129,-65,-33,-17,-2,-1,0,1,15,199,200,230,231,232,239,240,270,271,272})
    for (int columns : {0,1,2,3,4,8,16,32})
    for (int rows : {0,1,2,8,16,32,64,128}) {
        SpriteDrawState input;
        input.source = source;
        input.x = x; input.y = y; input.columns = columns; input.rows = rows;
        input.palette = 0xA0;
        const auto saved = input;
        Engine e{int16(x),int16(y),int16(columns),int16(rows),source,int16(width)};
        window.height = height;
        cGraphics_PC pc; pc.mFodder = &e;
        cGraphics_Amiga amiga; amiga.mFodder = &e;
        const bool visible = format == SpriteDrawFormat::PC ? pc.Sprite_OnScreen_Check()
            : amiga.Sprite_OnScreen_Check(format == SpriteDrawFormat::Amiga16);
        const auto result = ClipSpriteDraw(input, format, width, height);
        if (result.visible != visible || result.x != e.mVideo_Draw_PosX || result.y != e.mVideo_Draw_PosY ||
            result.columns != e.mVideo_Draw_Columns || result.rows != e.mVideo_Draw_Rows ||
            result.sourceOffset != e.mVideo_Draw_FrameDataPtr - source || result.source != source ||
            result.palette != 0xA0 || result.format != format || !same(input, saved)) {
            std::cerr << "FAIL clipping case " << cases << '\n'; return 1;
        }
        for (int repeat = 0; repeat < 4; ++repeat)
            if (!same(result, ClipSpriteDraw(input, format, width, height)) || !same(input, saved)) {
                std::cerr << "FAIL repeat changed input/result\n"; return 1;
            }
        ++cases;
    }
    // Explicit preparation example: rows-to-skip, anchor, camera, height and bias.
    SpriteDrawInput input;
    input.source = source; input.columns = 16; input.rows = 20; input.rowsToSkip = 4;
    input.spriteX = 100; input.spriteY = 100; input.modX = -2; input.modY = 3;
    input.mapX = 25; input.mapY = 50; input.height = 8; input.palette = 32;
    for (auto format : {SpriteDrawFormat::PC, SpriteDrawFormat::Amiga8}) {
        input.format = format;
        const auto result = PrepareSpriteDraw(input);
        if (!result.visible || result.x != 137 || result.y != 45 || result.rows != 16 ||
            result.columns != 16 || result.source != source || result.sourceOffset != 0 || result.palette != 32)
            return 2;
        for (int n = 0; n < 100; ++n)
            if (!same(result, PrepareSpriteDraw(input))) return 3;
    }
    for (auto value : bytes) if (value != 0) return 4;
    std::cout << "PASS: " << cases << " clipping cases match legacy PC/Amiga, input and pixels unchanged, repeated calls identical\n";
}
'''
    with tempfile.TemporaryDirectory(prefix='openfodder-draw-') as folder:
        source = Path(folder) / 'draw.cpp'
        binary = Path(folder) / 'draw'
        source.write_text(harness)
        subprocess.run([args.compiler, '-std=c++14', '-O1', '-fsanitize=address,undefined',
                        '-fno-sanitize-recover=all', '-I' + str(root / 'Source'),
                        str(source), '-o', str(binary)], check=True)
        import os
        subprocess.run([str(binary)], env=dict(os.environ, ASAN_OPTIONS='detect_leaks=0'), check=True)

if __name__ == '__main__':
    main()
