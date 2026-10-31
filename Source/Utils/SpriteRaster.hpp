// GPL-3.0-or-later. Rasterization extracted from OpenFodder PC/Amiga backends.
#pragma once
#include "SpriteDrawState.hpp"

namespace openfodder {
// Borrowed buffers must remain alive and must not alias the draw/layout inputs.
// Callers supply already-clipped valid PC/Amiga8 geometry and sufficient buffer
// extents (including Amiga planes). Amiga16 and other draw paths are not handled.
struct SpriteRasterTarget {
    uint8_t* pixels;
    size_t width;
};
struct SpriteRasterLayout {
    SpriteDrawFormat format = SpriteDrawFormat::PC;
    uint16_t width = 320, height = 0;
    uint8_t planes = 0;
};
struct SpriteRasterRegisters {
    int16_t columns;
    size_t sourceSkip, destinationSkip;
};
// These values were legacy engine writes. Calculation itself has no side effects.
inline SpriteRasterRegisters PrepareSpriteRasterRegisters(const SpriteDrawState& draw,
        const SpriteRasterLayout& layout, size_t targetWidth) {
    SpriteRasterRegisters r;
    if (draw.format == SpriteDrawFormat::PC) {
        r.columns = draw.columns >> 1;
        r.sourceSkip = 160 - r.columns;
        r.destinationSkip = static_cast<uint16_t>(targetWidth - r.columns * 2);
    } else {
        r.columns = static_cast<int16_t>(draw.columns - 1);
        r.columns = static_cast<int16_t>(r.columns * 2);
        r.sourceSkip = (layout.width >> 3) - r.columns;
        r.destinationSkip = targetWidth - r.columns * 8;
    }
    return r;
}
namespace detail {
inline void RasterPixelsAmiga8(const uint8_t* pSource, uint8_t* pDestination,
        const SpriteRasterLayout& layout, uint8_t palette) {
	uint8_t	Planes[8];

	// Load bits for all planes
	for (uint8_t Plane = 0; Plane < layout.planes; ++Plane)
		Planes[Plane] = *(pSource + ((layout.height * 40) * Plane));

	// Loop each pixel 
	for (uint8_t X = 0; X < 8; ++X) {
		uint16_t Bit = (0x80 >> X);
		uint8_t Result = 0;

		// Value for each plane
		for (uint8_t Plane = 0; Plane < layout.planes; ++Plane) {
			Result |= Planes[Plane] & Bit ? (1 << Plane) : 0;
		}

		if (Result)
			pDestination[X] = palette | Result;
	}
}
inline void RasterPC8(const SpriteDrawState& draw, const SpriteRasterLayout&,
        SpriteRasterTarget target, const SpriteRasterRegisters& registers, const uint8_t* RowPallete) {
	uint8_t*	di = target.pixels;
	const uint8_t* si = draw.source + draw.sourceOffset;

	di += target.width * draw.y;
	di += draw.x;

	for (int16_t dx = 0; dx < draw.rows; ++dx) {
		uint8_t Palette = draw.palette;
		if (RowPallete) {
			int16_t bx = draw.y + dx;

			Palette = RowPallete[bx];
		}

		for (int16_t cx = registers.columns; cx > 0; --cx) {
			uint8_t ah = *si;

			uint8_t al = ah >> 4;
			if (al)
				*di = al | Palette;

			al = ah & 0x0F;
			if (al)
				*(di + 1) = al | Palette;

			si++;
			di+=2;
		}

		si += registers.sourceSkip;
		di += registers.destinationSkip;
	}
}
inline void RasterAmiga8(const SpriteDrawState& draw, const SpriteRasterLayout& layout,
        SpriteRasterTarget target, const SpriteRasterRegisters& registers, const uint8_t*) {
	uint8_t* di = target.pixels;
	const uint8_t* si = draw.source + draw.sourceOffset;

	di += target.width * draw.y;
	di += draw.x;

	// Height
	for (int16_t dx = draw.rows; dx > 0; --dx) {

		// Width
		for (int16_t cx = 0; cx < registers.columns; ++cx) {

			RasterPixelsAmiga8(si, di, layout, draw.palette);

			di += 8;
			si += 1;
		}

		si += registers.sourceSkip;
		di += registers.destinationSkip;
	}
}
} // namespace detail

// Only destination pixels are written. No engine, sprite, surface or backend access.
// Row palettes apply to PC only, matching the original Amiga path that ignores them.
inline void RasterizeSprite8(const SpriteDrawState& draw, const SpriteRasterLayout& layout,
                            SpriteRasterTarget target, const uint8_t* rowPalette = nullptr) {
    const auto registers = PrepareSpriteRasterRegisters(draw, layout, target.width);
    if (draw.format == SpriteDrawFormat::PC)
        detail::RasterPC8(draw, layout, target, registers, rowPalette);
    else
        detail::RasterAmiga8(draw, layout, target, registers, rowPalette);
}
} // namespace openfodder
