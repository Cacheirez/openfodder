/* GPL-3.0-or-later. Preserve two's-complement 16-bit wrap with defined shifts. */
#pragma once
#include <cstdint>
#include <cstring>
inline std::int16_t wrapShiftLeft16(std::int16_t value, unsigned shift) {
    std::uint16_t bits;
    std::memcpy(&bits, &value, sizeof(bits));
    bits = static_cast<std::uint16_t>(static_cast<std::uint32_t>(bits) << shift);
    std::memcpy(&value, &bits, sizeof(value));
    return value;
}
// Exactly the signed 16-bit sign extension used by the historical C++ code.
inline std::uint32_t signExtendedWord32(std::int16_t value) {
    return static_cast<std::uint32_t>(static_cast<std::int32_t>(value));
}

inline std::int32_t wrapShiftLeft32(std::int32_t value, unsigned shift) {
    std::uint32_t bits;
    std::memcpy(&bits, &value, sizeof(bits));
    bits <<= shift;
    std::memcpy(&value, &bits, sizeof(value));
    return value;
}
inline std::int32_t packWords32(std::int16_t high, std::int16_t low) {
    const std::uint32_t bits =
        (static_cast<std::uint32_t>(static_cast<std::uint16_t>(high)) << 16) |
         static_cast<std::uint16_t>(low);
    std::int32_t value;
    std::memcpy(&value, &bits, sizeof(value));
    return value;
}
