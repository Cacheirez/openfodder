"""Verify the offline C01 density model against the preserved native resource.
Requires C++14 and Node.js, no npm packages; no engine or source image edits.
GPL-3.0-or-later.
"""
from pathlib import Path
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[2]

def main():
    with tempfile.TemporaryDirectory(prefix='density-review-') as td:
        td = Path(td)
        cpp = td / 'decode.cpp'
        cpp.write_text(r'''
#define STB_IMAGE_IMPLEMENTATION
#include "Utils/stb_image.h"
#include <cstdio>
int main(int argc,char**argv){
 if(argc!=3)return 2;int w,h,n;auto p=stbi_load(argv[1],&w,&h,&n,4);
 if(!p||w!=1353||h!=1162){stbi_image_free(p);return 3;}
 auto f=std::fopen(argv[2],"wb");if(!f){stbi_image_free(p);return 4;}
 const auto count=std::fwrite(p,1,w*h*4,f);const int closed=std::fclose(f);
 stbi_image_free(p);return count==size_t(w*h*4)&&closed==0?0:5;
}
''')
        decoder = td / 'decode'
        raw = td / 'source.rgba'
        subprocess.run(['g++', '-std=c++14', '-O2', '-I', str(ROOT/'Source'), str(cpp), '-o', str(decoder)], check=True)
        subprocess.run([str(decoder), str(ROOT/'assets/modernization/soldier-c01/source.png'), str(raw)], check=True)
        subprocess.run(['node', str(ROOT/'tools/modernization/density-preview/check.cjs'), str(raw), str(ROOT)], check=True)

if __name__ == '__main__':
    main()
