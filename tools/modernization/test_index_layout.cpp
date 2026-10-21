/* GPL-3.0-or-later. Pure table-index and Huffman-layout checks. */
#include "../../Source/Utils/IndexBounds.hpp"
#include "../../Source/PC/HuffmanLayout.hpp"
#include <cstdint>
#include <iostream>
int main() {
    std::size_t checks=0;
    for(int n=-40;n<=40;n++) {
        const bool valid=(n>=0 && n<9);
        if(gameIndexInBounds(n,9)!=valid) return 1;
        ++checks;
    }
    using namespace PC_Huffman;
    if(Symbols!=314 || Nodes!=627 || Root!=626 ||
       FrequencyEntries!=628 || ParentEntries!=941) return 1;
    // All legal Huffman tree and leaf references fit their actual tables.
    for(std::size_t leaf=0;leaf<Symbols;++leaf) {
        if(Nodes+leaf>=ParentEntries) return 1;
        ++checks;
    }
    for(std::size_t node=0;node<Nodes;++node) {
        if(node>=FrequencyEntries || node>=Nodes) return 1;
        ++checks;
    }
    if(Root>=Nodes || Nodes>=FrequencyEntries) return 1;
    std::cout << "PASS " << checks << " squad/Huffman boundary cases\n";
}
