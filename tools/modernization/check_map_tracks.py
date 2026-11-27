"""Exercise the actual Map_Collect_TileTracks body with synthetic map buffers.

Requires g++ (Linux diagnostic harness, not the Windows build workflow).
The body is extracted from source so this does not test a duplicate algorithm.
SPDX-License-Identifier: GPL-3.0-or-later
"""
from pathlib import Path
import subprocess
import tempfile

root = Path(__file__).resolve().parents[2]
source = (root / "Source/Map/MapRuntime.cpp").read_text()
body = source.split("void cFodder::Map_Collect_TileTracks()", 1)[1].split("void cFodder::Map_Load_Resources()", 1)[0]
harness = r'''
#include <cassert>
#include <cstdint>
#include <cstdio>
#include <memory>
#include <tuple>
#include <vector>
using uint8 = uint8_t;
using uint16 = uint16_t;
template <class T> T readLE(const void* p) {
    const auto* b = static_cast<const uint8*>(p);
    return static_cast<T>(b[0] | (b[1] << 8));
}
struct Map { uint16 w=2, h=2; uint16 getWidth(){return w;} uint16 getHeight(){return h;} };
struct cFodder {
    std::shared_ptr<std::vector<uint8>> mMap = std::make_shared<std::vector<uint8>>();
    std::shared_ptr<Map> mMapLoaded = std::make_shared<Map>();
    std::vector<std::tuple<uint16,uint16,uint16>> mMapTileTracks;
    void Map_Collect_TileTracks();
};
void cFodder::Map_Collect_TileTracks()
''' + body + r'''
int main() {
    for (size_t size : {size_t(0), size_t(0x61), size_t(0x62), size_t(0x63)}) {
        cFodder f; f.mMap->resize(size);
        f.mMapTileTracks.emplace_back(99,99,99);
        f.Map_Collect_TileTracks(); assert(f.mMapTileTracks.empty());
    }
    for (size_t size : {size_t(0x64), size_t(0x65)}) {
        cFodder f; f.mMap->resize(size); (*f.mMap)[0x63]=0x20;
        f.Map_Collect_TileTracks();
        assert(f.mMapTileTracks.size()==1);
        assert(f.mMapTileTracks[0]==std::make_tuple(uint16(0),uint16(0),uint16(1)));
    }
    {
        cFodder f; f.mMap->resize(0x6a); (*f.mMap)[0x63]=0x20; (*f.mMap)[0x69]=0xe0;
        f.Map_Collect_TileTracks(); assert(f.mMapTileTracks.size()==2);
        assert(f.mMapTileTracks[1]==std::make_tuple(uint16(1),uint16(1),uint16(7)));
    }
    {
        cFodder f; f.mMapLoaded->w=65535; f.mMapLoaded->h=65535;
        f.mMap->resize(0x64); f.Map_Collect_TileTracks(); assert(f.mMapTileTracks.empty());
    }
    puts("PASS: 8 map-boundary cases using the actual source function.");
}
'''
with tempfile.TemporaryDirectory() as directory:
    path = Path(directory)
    (path / "test.cpp").write_text(harness)
    subprocess.run(["g++", "-std=c++14", "-g", "-fsanitize=address,undefined",
                    "-fno-omit-frame-pointer", str(path / "test.cpp"), "-o", str(path / "test")], check=True)
    subprocess.run([str(path / "test")], check=True)
