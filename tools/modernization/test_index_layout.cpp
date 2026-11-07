/* GPL-3.0-or-later: guard real table indexing and legacy leaf aliases. */
#include "../../Source/Utils/IndexBounds.hpp"
#include "../../Source/PC/HuffmanLayout.hpp"
#include <cstdint>
#include <iostream>
int main() {
    std::size_t checks=0;
    for(int n=-40;n<=40;++n) {
        if(gameIndexInBounds(n,9)!=(n>=0 && n<9)) return 1;
        ++checks;
    }
    // Preserve the original contiguous layout of five adjacent 9-slot
    // squads, including indices 9..30 used by follower AI.
    for(int index=-5; index<50; ++index) {
        const auto slot=gameFlattenedIndex(index, 9, 5);
        const bool valid=index>=0 && index<45;
        if(slot.valid!=valid) return 1;
        if(valid && (slot.group!=static_cast<std::size_t>(index/9) ||
                     slot.offset!=static_cast<std::size_t>(index%9))) return 1;
        ++checks;
    }
    if(gameFlattenedIndex(0,0,5).valid || gameFlattenedIndex(0,9,0).valid) return 1;
    using namespace PC_Huffman;
    if(Symbols!=314 || Nodes!=627 || Root!=626 ||
       FrequencyEntries!=628 || ParentEntries!=941) return 1;
    int16_t nodeParents[Nodes]={};
    int16_t leafParents[Symbols]={};
    for(std::size_t i=0;i<ParentEntries;++i) {
        const auto loc=parentLocation(i);
        if(loc.kind==ParentKind::Invalid) return 1;
        int16_t &real=loc.kind==ParentKind::Node
                      ?nodeParents[loc.offset]:leafParents[loc.offset];
        real=static_cast<int16_t>(i);
        ++checks;
    }
    if(nodeParents[626]!=626 || leafParents[0]!=627 ||
       leafParents[313]!=940) return 1;
    if(parentLocation(ParentEntries).kind!=ParentKind::Invalid) return 1;
    int16_t frequencies[Nodes]={};
    int16_t sentinel=-1;
    if(static_cast<uint16_t>(sentinel)!=65535 ||
       frequencies[Nodes-1]!=0) return 1;
    std::cout << "PASS " << checks << " squad/Huffman alias & index cases\n";
}
