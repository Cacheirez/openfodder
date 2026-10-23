/*
 *  Open Fodder
 *  ---------------
 *
 *  Copyright (C) 2008-2026 Open Fodder
 *
 *  This program is free software; you can redistribute it and/or modify
 *  it under the terms of the GNU General Public License as published by
 *  the Free Software Foundation; either version 3 of the License, or
 *  (at your option) any later version.
 *
 *  This program is distributed in the hope that it will be useful,
 *  but WITHOUT ANY WARRANTY; without even the implied warranty of
 *  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 *  GNU General Public License for more details.
 *
 *  You should have received a copy of the GNU General Public License along
 *  with this program; if not, write to the Free Software Foundation, Inc.,
 *  51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
 *
 */
 
#include "stdafx.hpp"
#include <cmath>

cGraphics::cGraphics() {

	Heli_VeryBack = 0;
	Heli_Back = 0;
	Heli_middle = 0;
	Heli_Front = 0;
	Heli_TextPos = 0;
	Heli_TextPosBottom = 0;

    mFodder = g_Fodder;
	mSurface = g_Fodder->mSurface;
	mImageOriginal = mSurface;

	mImageTemporary.mData->resize(100000);
}

void cGraphics::SetImage( cSurface* pImage ) {
	mSurface = pImage;
}

void cGraphics::SetImageOriginal() {

	mSurface = mImageOriginal;
}

void cGraphics::SetSurfaceOriginal(cSurface* pImage) {
	mImageOriginal = pImage;
}

std::string cGraphics::EnsureExtension(const std::string& pFilename, const char* pExtension) const {
	if (pFilename.find('.') != std::string::npos)
		return pFilename;
	return pFilename + pExtension;
}

bool cGraphics::Sprite_OnScreen_ClipY(int16 pRowStrideBytes) {
	if (mFodder->mVideo_Draw_PosY >= 0)
		return true;

	int16 ax = mFodder->mVideo_Draw_PosY + mFodder->mVideo_Draw_Rows;
	--ax;
	if (ax < 0)
		return false;

	ax -= mFodder->mVideo_Draw_Rows;
	++ax;
	ax = -ax;
	mFodder->mVideo_Draw_PosY += ax;
	mFodder->mVideo_Draw_Rows -= ax;

	ax *= pRowStrideBytes;
	mFodder->mVideo_Draw_FrameDataPtr += ax;
	return true;
}

bool cGraphics::Sprite_OnScreen_ClipBottom() {
	int16 ax = mFodder->mVideo_Draw_PosY + mFodder->mVideo_Draw_Rows;
	--ax;

	auto maxHeight = g_Window->GetScreenSize().getHeight() + 31;
	if (ax > maxHeight) {
		if (mFodder->mVideo_Draw_PosY > maxHeight)
			return false;

		ax -= maxHeight;
		mFodder->mVideo_Draw_Rows -= ax;
	}

	return true;
}

openfodder::SidebarDraw cGraphics::CaptureSidebarDraw(int16 startY, bool offsetSource) const {
    return openfodder::CaptureSidebar(reinterpret_cast<const uint8*>(mFodder->mSidebar_Screen_Buffer),
        mSurface->GetWidth(), mSurface->GetHeight(), startY, offsetSource);
}

void cGraphics::Sidebar_Copy_To_Surface_Common(int16 pStartY, cSurface* pSurface, bool pOffsetSource) {
    const auto draw = CaptureSidebarDraw(pStartY, pOffsetSource);
    auto* target = pSurface ? pSurface : mSurface;
    openfodder::RasterizeSidebar(draw, target->GetSurfaceBuffer());
}

void cGraphics::Sidebar_Copy_ScreenBuffer_Common(uint16 pRow, int16 pRows, int16 pCopyToScreen, uint32*& pBuffer,
	int pRowOffset, int pRowScale) {
	pRow += (uint16)pRowOffset;
	pRows = (int16)(pRows * pRowScale);

	uint8* sptPtr = (uint8*)mFodder->mSidebar_Screen_Buffer;
	uint32* buffPtr = (uint32*)(sptPtr + (0x30 * pRow));

	if (pCopyToScreen == 0) {
		for (int16 cx = pRows; cx > 0; --cx) {
			*pBuffer++ = *buffPtr++;
			*pBuffer++ = *buffPtr++;
			*pBuffer++ = *buffPtr++;
			*pBuffer++ = *buffPtr++;

			*pBuffer++ = *buffPtr++;
			*pBuffer++ = *buffPtr++;
			*pBuffer++ = *buffPtr++;
			*pBuffer++ = *buffPtr++;

			*pBuffer++ = *buffPtr++;
			*pBuffer++ = *buffPtr++;
			*pBuffer++ = *buffPtr++;
			*pBuffer++ = *buffPtr++;
		}
	} else {
		for (int16 cx = pRows; cx > 0; --cx) {
			*buffPtr++ = *pBuffer++;
			*buffPtr++ = *pBuffer++;
			*buffPtr++ = *pBuffer++;
			*buffPtr++ = *pBuffer++;

			*buffPtr++ = *pBuffer++;
			*buffPtr++ = *pBuffer++;
			*buffPtr++ = *pBuffer++;
			*buffPtr++ = *pBuffer++;

			*buffPtr++ = *pBuffer++;
			*buffPtr++ = *pBuffer++;
			*buffPtr++ = *pBuffer++;
			*buffPtr++ = *pBuffer++;
		}
	}
}


void cGraphics::HeliIntro_TickParallaxAndText()
{
	const float scale = mFodder->mBriefingHelicopter_TimeScale;

	if (Heli_TextPosBottom != 0x0C) {
		Heli_TextPosBottom -= static_cast<int32_t>(4 * scale);

		if (Heli_TextPosBottom <= 0x0C)
			Heli_TextPosBottom = 0x0C;
	}
	Heli_TextPos = 344 - Heli_TextPosBottom;

	int32_t baseSpeed = static_cast<int32_t>(0x8000 * scale);
	int32_t d0 = baseSpeed;

	Heli_VeryBack -= d0;
	if (Heli_VeryBack < 0)
		Heli_VeryBack += 320 << 16;

	d0 <<= 1;
	Heli_Back -= d0;
	if (Heli_Back < 0)
		Heli_Back += 320 << 16;

	d0 <<= 1;
	Heli_middle -= d0;
	if (Heli_middle < 0)
		Heli_middle += 320 << 16;

	d0 <<= 1;
	Heli_Front -= d0;
	if (Heli_Front < 0)
		Heli_Front += 320 << 16;
}

// Compatibility entry point for callers still using legacy drawing registers.
void cGraphics::Video_Draw_8(cSurface* target, const uint8* rowPalette) {
    openfodder::SpriteDrawState draw;
    draw.source = mFodder->mVideo_Draw_FrameDataPtr;
    draw.x = mFodder->mVideo_Draw_PosX;
    draw.y = mFodder->mVideo_Draw_PosY;
    draw.columns = mFodder->mVideo_Draw_Columns;
    draw.rows = mFodder->mVideo_Draw_Rows;
    draw.palette = mFodder->mVideo_Draw_PaletteIndex;
    draw.format = GetSpriteRasterLayout().format;
    Video_Draw_8_Prepared(draw, target, rowPalette);
}

// Stateful coordinator: preserve old register writes immediately before rasterization.
// Reusable rendering calls RasterizeSprite8 with explicit layout/target instead.
void cGraphics::Video_Draw_8_Prepared(const openfodder::SpriteDrawState& draw,
                                    cSurface* target, const uint8* rowPalette) {
    if (!target)
        target = mSurface;
    const auto layout = GetSpriteRasterLayout();
    const openfodder::SpriteRasterTarget output{target->GetSurfaceBuffer(), target->GetWidth()};
    const auto registers = openfodder::PrepareSpriteRasterRegisters(draw, layout, output.width);
    mFodder->mVideo_Draw_Columns = registers.columns;
    mFodder->mDraw_Source_SkipPixelsPerRow = registers.sourceSkip;
    mFodder->mDraw_Dest_SkipPixelsPerRow = registers.destinationSkip;
    openfodder::RasterizeSprite8(draw, layout, output, rowPalette);
}

openfodder::ResolvedSpriteResource cGraphics::ResolveSpriteResource(uint16 segment,
        size_t frameOffset, uint8 tablePalette) {
    // Exact classic order: table palette first, then backend selection effects.
    mFodder->mVideo_Draw_PaletteIndex = tablePalette;
    auto source = GetSpriteData(segment);
    const auto storage = GetSpriteResourceStorage(segment);
    if (!source || !storage || storage->empty()) return {};
    // Valid GetSpriteData segments point inside their corresponding storage.
    const size_t segmentOffset = static_cast<size_t>(source - storage->data());
    if (segmentOffset >= storage->size() || frameOffset >= storage->size() - segmentOffset)
        return {};
    const auto layout = GetSpriteRasterLayout();
    auto result = mFrozenSpriteResources.capture(segment, *storage,
        segmentOffset + frameOffset, layout, mFodder->mVideo_Draw_PaletteIndex);
    // Legacy registers must still refer to original storage, not a retained copy.
    mFodder->mVideo_Draw_FrameDataPtr = source + frameOffset;
    return result;
}

void cGraphics::Video_Draw_8_Resolved(const openfodder::PreparedSpriteDraw& prepared,
                                     cSurface* target) {
    if (!target) target = mSurface;
    const auto& draw = prepared.draw;
    const auto& layout = prepared.resource.layout;
    const openfodder::SpriteRasterTarget output{target->GetSurfaceBuffer(), target->GetWidth()};
    const auto registers = openfodder::PrepareSpriteRasterRegisters(draw, layout, output.width);
    mFodder->mVideo_Draw_Columns = registers.columns;
    mFodder->mDraw_Source_SkipPixelsPerRow = registers.sourceSkip;
    mFodder->mDraw_Dest_SkipPixelsPerRow = registers.destinationSkip;
    openfodder::RasterizeSprite8(draw, layout, output);
}

// Capture after the backend's classic cursor selection. Do not call the
// effectful GetSpriteData again or replace its legacy source register.
openfodder::PreparedSpriteDraw cGraphics::CaptureCursorDraw() {
    openfodder::PreparedSpriteDraw prepared;
    const auto storage = GetSpriteResourceStorage(eGFX_PSTUFF);
    const auto layout = GetSpriteRasterLayout();
    const size_t offset = static_cast<size_t>(mFodder->mVideo_Draw_FrameDataPtr - storage->data());
    prepared.resource = mFrozenSpriteResources.capture(eGFX_PSTUFF, *storage, offset,
        layout, mFodder->mVideo_Draw_PaletteIndex);
    auto& draw = prepared.draw;
    draw.source = prepared.resource.source();
    draw.x = mFodder->mVideo_Draw_PosX;
    draw.y = mFodder->mVideo_Draw_PosY;
    draw.columns = mFodder->mVideo_Draw_Columns;
    draw.rows = mFodder->mVideo_Draw_Rows;
    draw.palette = mFodder->mVideo_Draw_PaletteIndex;
    draw.format = layout.format;
    draw.visible = true;
    return prepared;
}
