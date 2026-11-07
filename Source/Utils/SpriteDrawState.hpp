// GPL-3.0-or-later. Value-only preparation of legacy sprite draw geometry.
// Clipping rules extracted from OpenFodder cGraphics / PC / Amiga backends.
#pragma once
#include <cstdint>
#include <cstddef>

namespace openfodder {
enum class SpriteDrawFormat { PC, Amiga8, Amiga16 };

// source is borrowed and read-only; the owner must keep the resource alive.
// sourceOffset records clipping without touching pixels or engine registers.
struct SpriteDrawState {
    const uint8_t* source = nullptr;
    std::ptrdiff_t sourceOffset = 0;
    int16_t x = 0, y = 0, columns = 0, rows = 0;
    uint8_t palette = 0;
    bool visible = false;
    SpriteDrawFormat format = SpriteDrawFormat::PC;
};
struct SpriteDrawInput {
    const uint8_t* source = nullptr;
    int16_t columns = 0, rows = 0, rowsToSkip = 0;
    int16_t spriteX = 0, spriteY = 0, height = 0;
    int16_t modX = 0, modY = 0;
    int16_t mapX = 0, mapY = 0;
    int16_t xBias = 64;
    uint8_t palette = 0;
    int16_t viewWidth = 320, viewHeight = 200;
    SpriteDrawFormat format = SpriteDrawFormat::PC;
};
namespace detail {
inline bool ClipY(SpriteDrawState& state, int16_t pRowStrideBytes) {
	if (state.y >= 0)
		return true;

	int16_t ax = state.y + state.rows;
	--ax;
	if (ax < 0)
		return false;

	ax -= state.rows;
	++ax;
	ax = -ax;
	state.y += ax;
	state.rows -= ax;

	ax *= pRowStrideBytes;
	state.sourceOffset += ax;
	return true;
}

inline bool ClipBottom(SpriteDrawState& state, int16_t viewHeight) {
	int16_t ax = state.y + state.rows;
	--ax;

	auto maxHeight = viewHeight + 31;
	if (ax > maxHeight) {
		if (state.y > maxHeight)
			return false;

		ax -= maxHeight;
		state.rows -= ax;
	}

	return true;
}

inline bool ClipPC(SpriteDrawState& state, int16_t viewWidth, int16_t viewHeight) {
	int16_t ax;

	if (!ClipY(state, 0xA0))
		return false;
	if (!ClipBottom(state, viewHeight))
		return false;

	if (state.x < 0) {
		ax = state.x + state.columns;
		--ax;
		if (ax < 0)
			return false;

		ax -= state.columns;
		++ax;
		ax = -ax;
		--ax;

		state.x += ax;
		state.columns -= ax;
		ax >>= 1;
		state.sourceOffset += ax;

		// Ensure the destination X never remains negative after clipping.
		// A remaining -1 here would underflow the destination pointer in Video_Draw_8.
		if (state.x < 0)
		{
			++state.x;
			--state.columns;
		}
	}

	ax = state.x + state.columns;
	--ax;
	int16_t maxWindowX = viewWidth + 31; // 351

	if (ax > maxWindowX) {
		if (state.x > maxWindowX)
			return false;

		ax -= maxWindowX;
		--ax;

		do {
			++ax;
		} while (ax & 8);

		state.columns -= ax;
	}

	if (state.columns <= 0)
		return false;

	if (state.rows <= 0)
		return false;

	return true;
}

inline bool ClipAmiga(SpriteDrawState& state, int16_t viewWidth, int16_t viewHeight, bool p16bit) {
	int16_t ax;
	int16_t drawColumns;

	if (p16bit)
		drawColumns = (state.columns);
	else
		drawColumns = (state.columns * 8);

	if (!ClipY(state, 40))
		return false;
	if (!ClipBottom(state, viewHeight))
		return false;

	if (state.x < 0) {

		ax = state.x + drawColumns;
		--ax;
		if (ax < 0)
			return false;

		ax -= drawColumns;
		++ax;
		ax = -ax;
		--ax;

		drawColumns -= ax;

		if (!p16bit) {
			ax >>= 1;
			state.x += (ax << 1);
			state.columns -= (ax << 1);
		}
		else {
			ax >>= 3;
			state.x += (ax << 3);
			state.columns -= (ax << 3);
		}

		state.sourceOffset += ax;
	}

	ax = state.x + drawColumns;
	--ax;

	int16_t maxWindowX = viewWidth + 31; // 351

	if (ax > maxWindowX) {
		if (state.x > maxWindowX)
			return false;

		ax -= maxWindowX;
		--ax;

		do {
			++ax;
		} while (ax & 8);

		state.columns -= (ax >> 3);
	}

	if (state.columns <= 0)
		return false;

	if (state.rows <= 0)
		return false;

	return true;
}

} // namespace detail

// Pass by value: even early clipping rejection cannot modify the input state.
inline SpriteDrawState ClipSpriteDraw(SpriteDrawState state, SpriteDrawFormat format,
                                     int16_t viewWidth, int16_t viewHeight) {
    state.format = format;
    state.visible = format == SpriteDrawFormat::PC
        ? detail::ClipPC(state, viewWidth, viewHeight)
        : detail::ClipAmiga(state, viewWidth, viewHeight, format == SpriteDrawFormat::Amiga16);
    return state;
}

inline SpriteDrawState PrepareSpriteDraw(const SpriteDrawInput& input) {
    SpriteDrawState state;
    state.source = input.source;
    state.palette = input.palette;
    state.columns = input.columns;
    state.rows = static_cast<int16_t>(input.rows - input.rowsToSkip);
    state.x = static_cast<int16_t>(input.modX + input.spriteX - input.mapX + input.xBias);
    state.y = static_cast<int16_t>(input.modY + input.spriteY - state.rows - input.height - input.mapY);
    state.y += 0x10;
    return ClipSpriteDraw(state, input.format, input.viewWidth, input.viewHeight);
}
} // namespace openfodder
