/* GPL-3.0-or-later. Original adaptive Huffman table address layout. */
#pragma once
#include <cstddef>
namespace PC_Huffman {
constexpr std::size_t Symbols = 0x13A; // 314 leaves
constexpr std::size_t Nodes = 2 * Symbols - 1; // 627 nodes
constexpr std::size_t Root = Nodes - 1;
constexpr std::size_t ParentEntries = Nodes + Symbols; // 941 logical slots
constexpr std::size_t FrequencyEntries = Nodes + 1; // 627 + sentinel
enum class ParentKind { Node, Leaf, Invalid };
struct ParentSlot { ParentKind kind; std::size_t offset; };
constexpr ParentSlot parentLocation(std::size_t index) {
    return index < Nodes ? ParentSlot{ParentKind::Node, index}
         : index < ParentEntries ? ParentSlot{ParentKind::Leaf, index - Nodes}
         : ParentSlot{ParentKind::Invalid, 0};
}
static_assert(Nodes == 627 && ParentEntries == 941, "Unexpected Huffman layout");
static_assert(parentLocation(626).kind == ParentKind::Node, "Node boundary");
static_assert(parentLocation(627).kind == ParentKind::Leaf, "Leaf boundary");
static_assert(parentLocation(940).offset == 313, "Final leaf parent");
}
