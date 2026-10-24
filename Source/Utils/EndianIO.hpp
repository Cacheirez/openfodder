/* GPL-3.0-or-later. Independent unaligned little-endian loads and stores. */
#pragma once
#include <cstddef>
#include <cstdint>
#include <cstring>
#include <type_traits>
template <class T> inline T readUnalignedLE(const void* buffer) {
    static_assert(std::is_integral<T>::value && !std::is_same<T, bool>::value,
                  "Little endian reads require an integral non-bool type");
    typedef typename std::make_unsigned<T>::type U;
    const unsigned char* bytes = static_cast<const unsigned char*>(buffer);
    U bits = 0;
    for (std::size_t i = 0; i < sizeof(T); ++i)
        bits |= static_cast<U>(bytes[i]) << (i * 8);
    T result;
    std::memcpy(&result, &bits, sizeof(T));
    return result;
}
inline void writeUnalignedLE16(void* buffer, std::uint16_t value) {
    unsigned char* bytes = static_cast<unsigned char*>(buffer);
    bytes[0] = static_cast<unsigned char>(value);
    bytes[1] = static_cast<unsigned char>(value >> 8);
}
