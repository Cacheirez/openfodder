// Presentation preferences and a real-time confirmation deadline. GPL-3.0-or-later.
#pragma once
#include <cstdint>
#include <cstring>
namespace openfodder {
inline bool PresentationFlag(const char* overrideValue, bool preference) {
    return overrideValue ? std::strcmp(overrideValue, "1") == 0 : preference;
}
struct PresentationConfirmation {
    bool pending = false;
    uint32_t started = 0;
    void Begin(uint32_t now) { started = now; pending = true; }
    void Clear() { pending = false; }
    bool Expired(uint32_t now) const { return pending && uint32_t(now-started) >= 15000; }
    unsigned Seconds(uint32_t now) const {
        const auto elapsed = uint32_t(now-started);
        return !pending || elapsed >= 15000 ? 0 : (15000-elapsed+999)/1000;
    }
};
}
