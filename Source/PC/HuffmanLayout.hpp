/* GPL-3.0-or-later. Adaptive Huffman (LZHUF) table dimensions. */
#pragma once
#include <cstddef>
namespace PC_Huffman {
constexpr std::size_t Symbols = 0x13A; // 314 symbols
constexpr std::size_t Nodes = 2 * Symbols - 1; // 627 tree nodes
constexpr std::size_t Root = Nodes - 1;
constexpr std::size_t FrequencyEntries = Nodes + 1; // freq[Nodes] is sentinel
constexpr std::size_t ParentEntries = Nodes + Symbols; // parent[leaf+Nodes]
static_assert(Nodes == 0x273 && ParentEntries == 0x3AD, "Unexpected Huffman layout");
}
