// GPL-3.0-or-later. Complete classic mission image, captured after production.
#pragma once
#include "PausePresentation.hpp"

namespace openfodder {
// Terrain, ordered sprites, sidebar and cursor are already composed in indices.
// Keeping this result preserves writes from BOTH legacy update rhythms. This is
// not yet an independently movable layer/command list for interpolation.
struct MissionPresentation {
    PresentationSurface composed;
};
inline RGBLayerTarget RasterizeMissionPresentation(const MissionPresentation& scene) {
    return RasterizePresentationSurface(scene.composed);
}
} // namespace openfodder
