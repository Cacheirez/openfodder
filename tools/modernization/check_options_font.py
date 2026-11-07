"""Actual text -> GUI -> bounded sprite lookup, with actual briefing table extents.
No SDL or commercial art. Reproduces pre-fix confirmation null dereference.
"""
from pathlib import Path
import os, re, subprocess, sys, tempfile
from check_final_timer_equivalence import function
from check_sprite_table_lengths import check
ROOT=Path(__file__).resolve().parents[2]
def build(menu_ref=None):
    menu=(ROOT/'Source/OptionsMenu.cpp').read_text() if not menu_ref else subprocess.check_output(['git','show',menu_ref+':Source/OptionsMenu.cpp'],cwd=ROOT,text=True)
    draw=function(menu,'void cOptionsMenu::Draw')
    # Exercise exactly the confirmation heading used by Draw, all countdown values.
    heading=re.search(r'const std::string question="([^"]*)"',draw).group(1)
    table_counts=[]
    for backend in ('PC','Amiga'):
        arrays,tables=check((ROOT/f'Source/{backend}/SpriteData_{backend}.hpp').read_text())
        table_counts.append([arrays[x] for x in tables['mSpriteSheetTypes_Briefing_'+backend]])
    code=r'''
#ifdef NDEBUG
#undef NDEBUG
#endif
#include <cstdint>
#include <cstddef>
#include <cassert>
#include <atomic>
#include <iostream>
#include <string>
#include "Utils/SpriteFrameBounds.hpp"
using uint8=uint8_t;using int16=int16_t;using int32=int32_t;
#define PLATFORM_BASED(a,b) (amiga?(b):(a))
bool amiga=false;int rendered=0;
struct sSpriteSheet {unsigned mPalleteIndex=0;int mColCount=16,mRowCount=6;
 uint8* GetGraphicsPtr()const{static uint8 bytes[512]{};return bytes;}};
struct Graphics {void Video_Draw_8(){++rendered;}void Sidebar_Copy_Sprite_To_ScreenBufPtr(int,size_t,size_t){assert(false);}};
struct cFodder {
 Graphics graphics;Graphics*mGraphics=&graphics;
 size_t mSprite_SheetCount=4;const size_t*mSprite_FrameCounts=nullptr;
 const sSpriteSheet* const*mSprite_SheetPtr=nullptr;
 int16 mGUI_Temp_Y=0,mGUI_Draw_LastHeight=0,mVideo_Draw_PosX=0,mVideo_Draw_PosY=0;
 int mVideo_Draw_PaletteIndex=0,mVideo_Draw_Columns=0,mVideo_Draw_Rows=0,mString_GapCharID=0;
 uint8*mVideo_Draw_FrameDataPtr=nullptr;bool mGUI_Print_String_To_Sidebar=false;
 bool Sprite_OnScreen_Check(){return true;}
 const sSpriteSheet* Sprite_Get_Sheet(int16,int16);
 void GUI_Draw_Frame_8(int32,int32,size_t,size_t);
 void String_Print(const uint8*,int32,size_t,size_t,const char*);
};
'''
    font=(ROOT/'Source/FontData.cpp').read_text()
    for name in ['mFont_Briefing_Width','mGUI_Font_SpecialCharacters']:
        code+=re.search(r'const (?:uint8|unsigned char) '+name+r'\[\] = \{.*?\};',font,re.S).group(0)+'\n'
    for path,sig in [('Source/Sprites/Sprite_Core.cpp','const sSpriteSheet* cFodder::Sprite_Get_Sheet'),('Source/GUI_Element.cpp','void cFodder::GUI_Draw_Frame_8'),('Source/String.cpp','void cFodder::String_Print(const uint8* pWidths, int32 pFontSpriteID, size_t pParam08, size_t pParamC, const char* pText)')]:
        code+=function((ROOT/path).read_text(),sig)+'\n'
    code+='int main(){\n'
    for backend,counts in enumerate(table_counts):
        code+='{amiga='+str(backend)+';cFodder f;\n'
        code+='const size_t counts[]={'+','.join(map(str,counts))+'};\n'
        for i,n in enumerate(counts):code+=f'sSpriteSheet sheet{i}[{n}];\n'
        code+='const sSpriteSheet* sheets[]={sheet0,sheet1,sheet2,sheet3};f.mSprite_FrameCounts=counts;f.mSprite_SheetPtr=sheets;\n'
        code+='for(int seconds=0;seconds<=15;++seconds){rendered=0;std::string text="'+heading+'"+std::to_string(seconds);f.String_Print(mFont_Briefing_Width,0,32,64,text.c_str());assert(rendered>0);}\n'
        for text in ['REVERTS AFTER 15 SECONDS','KEEP','REVERT']:
            assert '"'+text+'"' in draw
            code+='f.String_Print(mFont_Briefing_Width,0,32,88,"'+text+'");\n'
        code+='}\n'
    code+='std::cout<<"PASS: real confirmation glyph route PC/Amiga, countdown 0..15, original font table extents\\n";}\n'
    return code

def main():
    if len(sys.argv)==3 and sys.argv[1]=='--emit':Path(sys.argv[2]).write_text(build());return
    ref=sys.argv[2] if len(sys.argv)==3 and sys.argv[1]=='--menu-ref' else None
    with tempfile.TemporaryDirectory(prefix='options-font-') as td:
        src=Path(td)/'test.cpp';exe=Path(td)/'test';src.write_text(build(ref))
        subprocess.run(['g++','-std=c++14','-O1','-g','-fsanitize=address,undefined','-fno-sanitize-recover=all','-I',str(ROOT/'Source'),str(src),'-o',str(exe)],check=True)
        subprocess.run([str(exe)],check=True,env={**os.environ,'ASAN_OPTIONS':'detect_leaks=0'})
if __name__=='__main__':main()
