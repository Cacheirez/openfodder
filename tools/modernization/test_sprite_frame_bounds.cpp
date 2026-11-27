/* GPL-3.0-or-later: independent sprite index/frames bounds test. */
#include "../../Source/Utils/SpriteFrameBounds.hpp"
#include <iostream>
int main() {
    constexpr std::size_t limits[] = {1,3,83,0,66};
    constexpr std::size_t count=sizeof(limits)/sizeof(limits[0]);
    unsigned cases=0;
    for(int type=-3;type<=9;++type) for(int frame=-3;frame<=89;++frame) {
        const bool shouldPass=type>=0 && frame>=0 && static_cast<std::size_t>(type)<count &&
                            static_cast<std::size_t>(frame)<limits[type];
        if(spriteFrameInRange(type,frame,limits,count)!=shouldPass) return 1;
        ++cases;
    }
    if(spriteFrameInRange(0,0,nullptr,count) || spriteFrameInRange(0,0,limits,0)) return 1;
    std::cout << "PASS: " << cases << " frame index cases\n";
}
