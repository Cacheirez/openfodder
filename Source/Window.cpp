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
#include <sstream>
#include <cstdlib>
#include <cstdio>

cWindow::cWindow() {

	mOriginalResolution.mWidth = 320;
	mOriginalResolution.mHeight = 200;

	mScaler = mScalerPrevious = 2;

	mScreenSize.mWidth = mOriginalResolution.mWidth;
	mScreenSize.mHeight = mOriginalResolution.mHeight;

	mWindowMode = true;

	mWindow = 0;

	mRenderer = 0;

    mHasFocus = true;
	mResized = false;
}

cWindow::~cWindow() {

	SDL_DestroyRenderer( mRenderer );
	SDL_DestroyWindow( mWindow );

	SDL_Quit();
}

bool cWindow::InitWindow( const std::string& pWindowTitle ) {
	
	if (!SDL_Init(SDL_INIT_VIDEO | SDL_INIT_AUDIO)) {
        g_Debugger->Error("Failed to initialise SDL");
		exit( 1 );
		return false;
	}
	
    ToggleFullscreen();

    const bool fitWindow=g_Fodder->mStartParams->ScreenTransformEnabled() &&
        g_Fodder->mStartParams->ScreenFitEnabled() &&
        g_Fodder->mStartParams->mMouseAlternative && !g_Fodder->mParams->mMouseLocked;
    mWindow = SDL_CreateWindow(pWindowTitle.c_str(), GetWindowSize().mWidth, GetWindowSize().mHeight,
        fitWindow ? SDL_WINDOW_RESIZABLE | SDL_WINDOW_HIGH_PIXEL_DENSITY : 0);
	if (!mWindow) {
        g_Debugger->Error("Failed to create window");
		exit( 1 );
		return false;
	}

    PositionWindow();
	mRenderer = SDL_CreateRenderer(mWindow, nullptr);
	if (!mRenderer) {
        g_Debugger->Error("Failed to create rendered");
		exit( 1 );
		return false;
	}

	SDL_SetHintWithPriority(SDL_HINT_MOUSE_RELATIVE_WARP_MOTION, "1", SDL_HINT_OVERRIDE);
	SetMouseSpeed(g_Fodder ? (float)g_Fodder->mStartParams->mMouseSpeed : 1.5f);


    if (g_Fodder->mParams->mWindowMode) {
        ToggleFullscreen();
        CalculateWindowSize();
    }
    else {
        ToggleFullscreen();
        ToggleFullscreen();
    }

	if (!g_Fodder->mParams->mMouseAlternative || (g_Fodder->mParams->mMouseAlternative && g_Fodder->mParams->mMouseLocked)) {
		SDL_SetWindowRelativeMouseMode(mWindow, true);

		// Warp mouse to 0,0 to fix an issue with the mouse cursor appearing on first click in the window
		SDL_WarpMouseInWindow(mWindow, 0, 0);
	}
	
	SDL_HideCursor();

	return true;
}

void cWindow::ToggleVSync(bool pEnabled) {
	#ifdef EMSCRIPTEN
	return;
	#endif
	SDL_SetRenderVSync(mRenderer, pEnabled ? 1 : 0);
}

void cWindow::SetRelativeMouseMode(bool pEnable) {

    if (mWindow) {
        SDL_SetWindowRelativeMouseMode(mWindow, pEnable);
    }
}

void cWindow::SetMouseSpeed(float pSpeed) {
	if (pSpeed < 1.0f)
		pSpeed = 1.0f;
	if (pSpeed > 10.0f)
		pSpeed = 10.0f;

	std::ostringstream speed;
	speed.setf(std::ios::fixed);
	speed.precision(1);
	speed << pSpeed;
	SDL_SetHint(SDL_HINT_MOUSE_RELATIVE_SPEED_SCALE, speed.str().c_str());
}

std::vector<cEvent>* cWindow::EventGet() {
    return &mEvents;
}

bool cWindow::Cycle() {

    EventCheck();


    return true;
}

void cWindow::EventCheck() {
	SDL_Event SysEvent;
    static float sMouseMotionRemainderX = 0.0f;
    static float sMouseMotionRemainderY = 0.0f;

	while (SDL_PollEvent(&SysEvent)) {

		cEvent Event;

		switch (SysEvent.type) {
        case SDL_EVENT_WINDOW_RESIZED:
        case SDL_EVENT_WINDOW_PIXEL_SIZE_CHANGED:
        case SDL_EVENT_WINDOW_DISPLAY_CHANGED:
            InvalidateScreenTransform();
            break;
		case SDL_EVENT_WINDOW_FOCUS_LOST:
            InvalidateScreenTransform();
			Event.mType = eEvent_Focus;
			Event.mHasFocus = false;
			mHasFocus = false;
			break;

		case SDL_EVENT_WINDOW_FOCUS_GAINED:
			Event.mType = eEvent_Focus;
			Event.mHasFocus = true;
			mHasFocus = true;
			break;
		case SDL_EVENT_WINDOW_MOUSE_ENTER:
			Event.mType = eEvent_MouseEnter;
			break;
		case SDL_EVENT_WINDOW_MOUSE_LEAVE:
			Event.mType = eEvent_MouseLeave;
			break;

		case SDL_EVENT_KEY_DOWN:
			Event.mType = eEvent_KeyDown;
			Event.mButton = SysEvent.key.scancode;
			break;

		case SDL_EVENT_KEY_UP:
			Event.mType = eEvent_KeyUp;
			Event.mButton = SysEvent.key.scancode;
			break;

		case SDL_EVENT_FINGER_MOTION:
			Event.mType = eEvent_MouseMove;
			Event.mPosition = cPosition((unsigned int)(SysEvent.tfinger.x * GetWindowWidth()),
										(unsigned int)(SysEvent.tfinger.y * GetWindowHeight()));
			break;

		case SDL_EVENT_FINGER_DOWN:
			
			Event.mType = eEvent_MouseLeftDown;
			Event.mButton = 1;
			Event.mPosition = cPosition((unsigned int)(SysEvent.tfinger.x * GetWindowWidth()),
										(unsigned int)(SysEvent.tfinger.y * GetWindowHeight()));

			Event.mButtonCount = 1;

			break;

		case SDL_EVENT_FINGER_UP:
			Event.mType = eEvent_MouseLeftUp;
			Event.mButton = 1;

			Event.mPosition = cPosition((unsigned int)(SysEvent.tfinger.x * GetWindowWidth()),
										(unsigned int)(SysEvent.tfinger.y * GetWindowHeight()));

			Event.mButtonCount = 1;
			mEvents.push_back(Event);

			Event.mType = eEvent_MouseRightUp;
			Event.mButton = 3;

			break;

		case SDL_EVENT_MOUSE_MOTION:
		{
            sMouseMotionRemainderX += SysEvent.motion.xrel;
            sMouseMotionRemainderY += SysEvent.motion.yrel;
            const int Xrel = (int)sMouseMotionRemainderX;
            const int Yrel = (int)sMouseMotionRemainderY;
            sMouseMotionRemainderX -= (float)Xrel;
			sMouseMotionRemainderY -= (float)Yrel;

			Event.mType = eEvent_MouseMove;
			Event.mPosition = cPosition((int)SysEvent.motion.x, (int)SysEvent.motion.y);
			Event.mPositionRelative = cPosition(Xrel, Yrel);
			break;
		}
		case SDL_EVENT_MOUSE_WHEEL:
			Event.mType = eEvent_MouseWheel;
			Event.mPosition = cPosition((int)SysEvent.wheel.x, (int)SysEvent.wheel.y);
			break;

		case SDL_EVENT_MOUSE_BUTTON_DOWN:

			switch (SysEvent.button.button) {

			case 1:
				Event.mType = eEvent_MouseLeftDown;
				Event.mButton = 1;
				break;

			case 3:
				Event.mType = eEvent_MouseRightDown;
				Event.mButton = 3;
				break;
			}

			Event.mPosition = cPosition((int)SysEvent.button.x, (int)SysEvent.button.y);
			Event.mButtonCount = SysEvent.button.clicks;
			break;

		case SDL_EVENT_MOUSE_BUTTON_UP:

			switch (SysEvent.button.button) {

			case 1:
				Event.mType = eEvent_MouseLeftUp;
				Event.mButton = 1;
				break;

			case 3:
				Event.mType = eEvent_MouseRightUp;
				Event.mButton = 3;
				break;
			}

			Event.mPosition = cPosition((int)SysEvent.button.x, (int)SysEvent.button.y);
			Event.mButtonCount = SysEvent.button.clicks;
			break;

		case SDL_EVENT_QUIT:
			Event.mType = eEvent_Quit;
			break;
		}

#ifdef EMSCRIPTEN
		// Drop events which have no x/y
		if (SysEvent.type == SDL_EVENT_MOUSE_MOTION || 
			SysEvent.type == SDL_EVENT_MOUSE_BUTTON_DOWN || 
			SysEvent.type == SDL_EVENT_MOUSE_BUTTON_UP) {

			if (Event.mPosition.mX == 0 || Event.mPosition.mY == 0)
				continue;
		}
#endif
		if ( Event.mType != eEvent_None )
			mEvents.push_back( Event );
	}
}

void cWindow::CalculateWindowSize() {
	SDL_DisplayID display = mWindow ? SDL_GetDisplayForWindow(mWindow) : SDL_GetPrimaryDisplay();
	const SDL_DisplayMode* current = SDL_GetCurrentDisplayMode(display);
	if (!current) {
		return;
	}

	while ((mOriginalResolution.mWidth * mScaler) <= (unsigned int) (current->w / 2) && 
			(mOriginalResolution.mHeight * mScaler) <= (unsigned int) (current->h / 2) ) {
		++mScaler;
	}

	SetWindowSize( mScaler );
}

int16 cWindow::CalculateFullscreenSize() {
	SDL_DisplayID display = mWindow ? SDL_GetDisplayForWindow(mWindow) : SDL_GetPrimaryDisplay();
	const SDL_DisplayMode* current = SDL_GetCurrentDisplayMode(display);
	if (!current) {
		return 1;
	}
	int16 Multiplier = 1;

	while ((mOriginalResolution.mWidth * Multiplier) <= (unsigned int) current->w && (mOriginalResolution.mHeight * Multiplier) <= (unsigned int) current->h ) {
		++Multiplier;
	}

	return --Multiplier;
}

bool cWindow::CanChangeToMultiplier( const int pNewMultiplier ) {
	SDL_DisplayID display = mWindow ? SDL_GetDisplayForWindow(mWindow) : SDL_GetPrimaryDisplay();
	const SDL_DisplayMode* current = SDL_GetCurrentDisplayMode(display);
	if (!current) {
		return false;
	}

	if (	(mOriginalResolution.getWidth()  * pNewMultiplier >= current->w ||
			mOriginalResolution.getHeight() * pNewMultiplier >= current->h) ||
			pNewMultiplier <= 0 )
		return false;

	return true;
}

void cWindow::FrameEnd() {
    #ifndef EMSCRIPTEN
    const bool presented=SDL_RenderPresent(mRenderer);
    {
        std::lock_guard<std::mutex> lock(mScreenTransformMutex);
        mPresentedScreenTransform=presented ? mPendingScreenTransform : openfodder::ScreenTransform{};
        mPresentedScreenClassic=presented && mPendingScreenClassic;
        mPresentedScreenScene=presented ? mPendingScreenScene : 0;
        mPendingScreenTransform={};mPendingScreenClassic=false;mPendingScreenScene=0;
        // OS cursor follows the pointer through letterbox bands; presentation only.
        const bool systemCursor=mPresentedScreenTransform.valid && IsMissionCursorInBand();
        if(systemCursor!=mSystemMissionCursorShown) {
            if(systemCursor) SDL_ShowCursor(); else SDL_HideCursor();
            mSystemMissionCursorShown=systemCursor;
        }
        if(mPresentedScreenTransform.valid && g_Fodder->mStartParams->mUnitTesting) {
            const auto& t=mPresentedScreenTransform;
            for(const auto& point : {openfodder::ScreenPoint{0.5,0.5},
                    openfodder::ScreenPoint{t.source.w/2,t.source.h/2},
                    openfodder::ScreenPoint{t.source.w-0.5,t.source.h-0.5}}) {
                openfodder::ScreenPoint roundtrip;
                if(!t.WindowToCanvas(t.CanvasToWindow(point),roundtrip) ||
                   std::abs(roundtrip.x-point.x)>1e-8 || std::abs(roundtrip.y-point.y)>1e-8)
                    throw std::runtime_error("presented screen mouse inverse mismatch");
            }
            static bool reported=false;
            if(!reported) {
                std::fprintf(stderr,"SCREEN_TRANSFORM: presented mission and verified mouse inverse\n");
                reported=true;
            }
        }
    }
    
	SDL_SetRenderDrawColor(mRenderer, 0, 0, 0, 0);
	SDL_RenderClear( mRenderer );
	#else
	SDL_SetRenderDrawColor(mRenderer, 0, 0, 0, 0);
	//SDL_RenderClear( mRenderer );
#endif
}

void cWindow::PositionWindow() {
	
	SDL_SetWindowPosition( mWindow, SDL_WINDOWPOS_CENTERED, SDL_WINDOWPOS_CENTERED );
}

void cWindow::WindowIncrease() {
	
	if (!mWindowMode)
			return;

	// Once we reach the max window size, go to full screen
	if (!CanChangeToMultiplier( mScaler + 1 )) {

		ToggleFullscreen();
		mWindowMode = false;
		return;
	}

	if (!mWindowMode)
		return;

	SetWindowSize( mScaler + 1 );
}

void cWindow::WindowDecrease() {

	// If we're in full screen mode remove it
	if (!mWindowMode) { 

		mWindowMode = true;
		SetWindowSize(mScaler);
		//ToggleFullscreen();
		return;
	}

	if (!CanChangeToMultiplier(mScaler - 1))
		return;

	SetWindowSize( mScaler - 1 );
}

void cWindow::RenderAt( cSurface* pImage, bool pMission ) {
    {
        std::lock_guard<std::mutex> lock(mScreenTransformMutex);
        mPendingScreenTransform = {};
        mPendingScreenClassic = false;
        mPendingScreenScene = 0;
    }
	SDL_FRect Src, Dest;

	Src.w = (float)mScreenSize.mWidth;
	Src.h = (float)mScreenSize.mHeight;
	Src.x = 16.0f;
	Src.y = 16.0f;

	if (g_Fodder->mParams->mIntegerScaling || mWindowMode) {
		Dest.w = (float)GetWindowSize().mWidth;
		Dest.h = (float)GetWindowSize().mHeight;
	}
	else {
		int windowW = 0;
		int windowH = 0;
		SDL_GetWindowSize(mWindow, &windowW, &windowH);
		Dest.h = (float)windowH;
		Dest.w = (float)(Dest.h * (float)(4.0/3.0));
	}

	if (mWindowMode) {
		Dest.x = 0.0f;
		Dest.y = 0.0f;
	}
	else {
		SDL_DisplayID display = mWindow ? SDL_GetDisplayForWindow(mWindow) : SDL_GetPrimaryDisplay();
		const SDL_DisplayMode* current = SDL_GetCurrentDisplayMode(display);
		if (current) {
			Dest.x = (float)((current->w - Dest.w) / 2.0f);
			Dest.y = (float)((current->h - Dest.h) / 2.0f);
		} else {
			Dest.x = 0.0f;
			Dest.y = 0.0f;
		}
	}

    const SDL_FRect classicDestination=Dest;
    openfodder::ScreenTransform transform;
    const bool flag = g_Fodder->mStartParams->ScreenTransformEnabled();
    const bool fitFlag=g_Fodder->mStartParams->ScreenFitEnabled();
    // The existing pause loop presents the main mission surface with the
    // default pMission=false. Fit that scene without publishing world input.
    const bool fitPause=!pMission && fitFlag &&
        pImage==g_Fodder->mSurface && g_Fodder->mPhase_In_Progress &&
        g_Fodder->mPhase_Paused && !g_Fodder->mPhase_ShowMapOverview &&
        !g_Fodder->mInterruptCallback && !pImage->isLoadedImage();
    const unsigned inputScene=FittedInputScene();
    // FIT is a presentation policy for every RenderAt scene, not a list of
    // named screens. Preserve each source crop and share its inverse with GUI.
    if ((pMission || fitFlag) && flag && (mWindowMode || fitFlag) &&
        g_Fodder->mStartParams->mMouseAlternative && !g_Fodder->mParams->mMouseLocked)
    {
        int ww=0,wh=0,pw=0,ph=0,lw=0,lh=0;
        float sx=0,sy=0;
        SDL_Rect viewport{};
        SDL_RendererLogicalPresentation logicalMode=SDL_LOGICAL_PRESENTATION_DISABLED;
        if (SDL_GetWindowSize(mWindow,&ww,&wh) && SDL_GetRenderOutputSize(mRenderer,&pw,&ph) &&
            !SDL_GetRenderTarget(mRenderer) && SDL_GetRenderScale(mRenderer,&sx,&sy) && sx==1 && sy==1 &&
            SDL_GetRenderViewport(mRenderer,&viewport) && viewport.x==0 && viewport.y==0 &&
            viewport.w==pw && viewport.h==ph && !SDL_RenderClipEnabled(mRenderer) &&
            SDL_GetRenderLogicalPresentation(mRenderer,&lw,&lh,&logicalMode) &&
            logicalMode==SDL_LOGICAL_PRESENTATION_DISABLED) {
            const bool fit=g_Fodder->mStartParams->ScreenFitEnabled();
            if(fit && ww>0 && wh>0 && pw>0 && ph>0) {
                const auto rect=openfodder::ScreenTransform::FitSource(pw,ph,
                    {Src.x,Src.y,Src.w,Src.h});
                // Quantize once to SDL's actual draw precision before retaining the inverse.
                if(openfodder::ScreenTransform::RectValid(rect))
                    Dest={float(rect.x),float(rect.y),float(rect.w),float(rect.h)};
            }
            transform=openfodder::ScreenTransform::FromDraw(ww,wh,pw,ph,
                {Src.x,Src.y,Src.w,Src.h},{Dest.x,Dest.y,Dest.w,Dest.h});
        }
    }
    if(!transform.valid) Dest=classicDestination; // Draw and input always fall back together.
    if (transform.valid) {
        // Source origin is storage padding, not a second camera translation.
        const auto origin=transform.StorageToOutput({Src.x,Src.y});
        const auto end=transform.CanvasToOutput({Src.w,Src.h});
        if (origin.x!=Dest.x || origin.y!=Dest.y ||
            std::abs(end.x-(double(Dest.x)+Dest.w))>1e-8 ||
            std::abs(end.y-(double(Dest.y)+Dest.h))>1e-8)
            throw std::runtime_error("screen transform differs from draw rectangle");
        // Dest is already the SDL-precision rectangle retained by FromDraw.
    }
    const int hd=pMission ? TryRenderMissionHD(pImage,Src,Dest) : -1;
    const bool drawn=hd<0 ? SDL_RenderTexture(mRenderer,pImage->GetTexture(),&Src,&Dest) : hd==1;
    if(drawn && fitPause && transform.valid && g_Fodder->mStartParams->mUnitTesting) {
        static bool reportedPause=false;
        if(!reportedPause) {
            std::fprintf(stderr,"SCREEN_TRANSFORM: fitted pause without mission input\n");
            reportedPause=true;
        }
    }
    std::lock_guard<std::mutex> lock(mScreenTransformMutex);
    // A fitted pause never publishes a world-input snapshot. On resume input
    // stays blocked until a fresh mission frame has actually been presented.
    const bool inputAllowed=inputScene!=0 && (inputScene!=1 || pMission);
    mPendingScreenTransform = drawn && inputAllowed ? transform : openfodder::ScreenTransform{};
    mPendingScreenScene = drawn && inputAllowed ? inputScene : 0;
    mPendingScreenClassic = drawn && !transform.valid;
}

void cWindow::RenderShrunk( cSurface* pImage ) {
    InvalidateScreenTransform();
	SDL_FRect Src, Dest;
	Src.w = (float)pImage->GetWidth();
	Src.h = (float)pImage->GetHeight();
	Src.x = 0.0f;
	Src.y = 0.0f;

	Dest.w = (float)GetWindowSize().mWidth;
	Dest.h = (float)GetWindowSize().mHeight;

	if (mWindowMode) {
		Dest.x = 0.0f;
		Dest.y = 0.0f;
	}
	else {
		SDL_DisplayID display = mWindow ? SDL_GetDisplayForWindow(mWindow) : SDL_GetPrimaryDisplay();
		const SDL_DisplayMode* current = SDL_GetCurrentDisplayMode(display);
		if (current) {
			Dest.x = (float)((current->w - Dest.w) / 2.0f);
			Dest.y = (float)((current->h - Dest.h) / 2.0f);
		} else {
			Dest.x = 0.0f;
			Dest.y = 0.0f;
		}
	}

    const SDL_FRect classicDestination=Dest;
    openfodder::ScreenTransform transform;
    const bool screen=g_Fodder->mStartParams->ScreenTransformEnabled();
    const bool fit=g_Fodder->mStartParams->ScreenFitEnabled();
    if(screen && fit && g_Fodder->mStartParams->mMouseAlternative && !g_Fodder->mParams->mMouseLocked) {
        int ww=0,wh=0,pw=0,ph=0,lw=0,lh=0;
        float sx=0,sy=0;
        SDL_Rect viewport{};
        SDL_RendererLogicalPresentation logicalMode=SDL_LOGICAL_PRESENTATION_DISABLED;
        if(SDL_GetWindowSize(mWindow,&ww,&wh) && SDL_GetRenderOutputSize(mRenderer,&pw,&ph) && pw>0 && ph>0 &&
           !SDL_GetRenderTarget(mRenderer) && SDL_GetRenderScale(mRenderer,&sx,&sy) && sx==1 && sy==1 &&
           SDL_GetRenderViewport(mRenderer,&viewport) && viewport.x==0 && viewport.y==0 &&
           viewport.w==pw && viewport.h==ph && !SDL_RenderClipEnabled(mRenderer) &&
           SDL_GetRenderLogicalPresentation(mRenderer,&lw,&lh,&logicalMode) &&
           logicalMode==SDL_LOGICAL_PRESENTATION_DISABLED) {
            // Shrink presentations retain their classic logical aspect (the
            // square overview is intentionally shown in the legacy screen aspect).
            const auto rect=openfodder::ScreenTransform::FitSource(pw,ph,{0,0,Dest.w,Dest.h});
            if(openfodder::ScreenTransform::RectValid(rect))
                Dest={float(rect.x),float(rect.y),float(rect.w),float(rect.h)};
            // GUI overlays are in screen coordinates, not PNG/map texel coordinates.
            transform=openfodder::ScreenTransform::FromDraw(ww,wh,pw,ph,
                {0,0,double(mScreenSize.mWidth),double(mScreenSize.mHeight)},
                {Dest.x,Dest.y,Dest.w,Dest.h});
        }
    }
    if(!transform.valid) Dest=classicDestination;
    const bool drawn=SDL_RenderTexture(mRenderer,pImage->GetTexture(),&Src,&Dest);
    const unsigned inputScene=FittedInputScene();
    std::lock_guard<std::mutex> lock(mScreenTransformMutex);
    // Never publish a world inverse from an overview or a shrink presentation.
    const bool inputAllowed=inputScene>1;
    mPendingScreenTransform=drawn && inputAllowed ? transform : openfodder::ScreenTransform{};
    mPendingScreenScene=drawn && inputAllowed ? inputScene : 0;
    mPendingScreenClassic=drawn && !transform.valid;

}

bool cWindow::isFullscreen() const {
    return !mWindowMode;
}

bool cWindow::isMouseInside() const {
	return mWindow == SDL_GetMouseFocus();
}

bool cWindow::isResized() const {
	return mResized;
}

/**
 * Is either mouse button currently pressed
 */
bool cWindow::isMouseButtonPressed_Global() const {
    return  (SDL_GetMouseState(NULL, NULL) & SDL_BUTTON_MASK(SDL_BUTTON_LEFT)) ||
            (SDL_GetMouseState(NULL, NULL) & SDL_BUTTON_MASK(SDL_BUTTON_RIGHT));
}

/**
 * Is the window currently grabbed
 */
bool cWindow::isGrabbed() const {
    if (!mWindow) {
        return false;
    }
    return SDL_GetWindowMouseGrab(mWindow);
}

void cWindow::ToggleFullscreen() {
    InvalidateScreenTransform();

	if (mWindowMode) {

		mScalerPrevious = mScaler;
		SetWindowSize( CalculateFullscreenSize() );

        if (mWindow) {
		    SDL_SetWindowFullscreen( mWindow, true );
        }
		mWindowMode = false;
	} else {
		mWindowMode = true;
		SetWindowSize( mScalerPrevious );
	}
}

void cWindow::ClearResized() {
	mResized = false;
}

void cWindow::SetMousePosition(const cPosition& pPosition) {

    SDL_WarpMouseGlobal((float)pPosition.getX(), (float)pPosition.getY());
}

void cWindow::SetMousePositionInWindow(float pX, float pY) {
    if (!mWindow) {
        return;
    }
    SDL_WarpMouseInWindow(mWindow, pX, pY);
}

void cWindow::SetScreenSize( const cDimension& pDimension ) {

    InvalidateScreenTransform();
	mScreenSize = pDimension;
}

/**
 * Set the window size / resolution using the aspect ratio of the original resolution
 * 
 * @param pDimension Original resolution
 */
void cWindow::SetOriginalRes( const cDimension& pDimension ) {

    if (mOriginalResolution == pDimension)
        return;

	mOriginalResolution = pDimension;
    // Scene resolution changes must not undo a user-maximized fitted window.
    if (mWindow && mWindowMode && g_Fodder->mStartParams->ScreenTransformEnabled() &&
        g_Fodder->mStartParams->ScreenFitEnabled() &&
        (SDL_GetWindowFlags(mWindow) & SDL_WINDOW_MAXIMIZED)) {
        InvalidateScreenTransform();
        return;
    }

	if (!mWindowMode) {
		ToggleFullscreen();
		ToggleFullscreen();
	} else
		SetWindowSize( mScaler );
}

void cWindow::SetWindowTitle( const std::string& pWindowTitle ) {

	SDL_SetWindowTitle( mWindow, pWindowTitle.c_str() );
}

bool cWindow::GetWindowBordersSize(int* pTop, int* pLeft, int* pBottom, int* pRight) const {
    if (!mWindow) {
        if (pTop) *pTop = 0;
        if (pLeft) *pLeft = 0;
        if (pBottom) *pBottom = 0;
        if (pRight) *pRight = 0;
        return false;
    }
    return SDL_GetWindowBordersSize(mWindow, pTop, pLeft, pBottom, pRight);
}

void cWindow::SetWindowSize( const int pMultiplier ) {

	if (pMultiplier < 1 )
		return;

	mScaler = pMultiplier;

	if (mWindow) {
		if (mWindowMode) {
			SDL_SetWindowFullscreen( mWindow, false );
		}
		SDL_SetWindowSize( mWindow, GetWindowSize().mWidth, GetWindowSize().mHeight );
		PositionWindow();
		
		mResized = true;
	}
}

cPosition cWindow::GetWindowPosition() const {
    cPosition Pos;

    SDL_GetWindowPosition(mWindow, &Pos.mX, &Pos.mY);

    return Pos;
}

cDimension cWindow::GetWindowSize() const {
	return cDimension( mOriginalResolution.mWidth * mScaler, mOriginalResolution.mHeight * mScaler ); 
}

int32 cWindow::GetWindowWidth() const {
	return mOriginalResolution.mWidth * mScaler;
}

int32 cWindow::GetWindowHeight() const {
	return mOriginalResolution.mHeight * mScaler;
}

cDimension cWindow::GetScale() const {
    cDimension Result = GetWindowSize() / GetScreenSize();
    if (Result.mHeight == 0)
        Result.mHeight = 1;
    if (Result.mWidth == 0)
        Result.mWidth = 1;
    return Result;
}

float cWindow::GetRefreshRate() {
	SDL_DisplayID display = mWindow ? SDL_GetDisplayForWindow(mWindow) : SDL_GetPrimaryDisplay();
	const SDL_DisplayMode* mode = SDL_GetCurrentDisplayMode(display);
	if (!mode) {
		std::cerr << "SDL_GetCurrentDisplayMode failed: " << SDL_GetError() << std::endl;
		return 50; // Fallback to 50Hz if query fails
	}
	return mode->refresh_rate;
}

bool cWindowNull::InitWindow(const std::string& pWindowTitle) {


    return true;
}

void cWindow::InvalidateScreenTransform() {
    std::lock_guard<std::mutex> lock(mScreenTransformMutex);
    mPendingScreenTransform={};mPresentedScreenTransform={};
    mPendingScreenClassic=false;mPresentedScreenClassic=false;
    mPendingScreenScene=0;mPresentedScreenScene=0;
}

openfodder::ScreenMouseResult cWindow::MapMissionMouse(int x,int y,int16& mappedX,int16& mappedY) {
    using openfodder::ScreenMouseResult;
#ifdef EMSCRIPTEN
    return ScreenMouseResult::Classic; // Browser presentation lifecycle is a separate adapter.
#endif
    const bool flag=g_Fodder->mStartParams->ScreenTransformEnabled();
    if (!flag || (!mWindowMode && !g_Fodder->mStartParams->ScreenFitEnabled()) ||
        !g_Fodder->mStartParams->mMouseAlternative || g_Fodder->mParams->mMouseLocked ||
        !FittedInputScene())
        return ScreenMouseResult::Classic;
    if(!g_Fodder->mWindow_Focus)return ScreenMouseResult::Blocked;
    openfodder::ScreenTransform t;
    {
        std::lock_guard<std::mutex> lock(mScreenTransformMutex);
        if(mPresentedScreenClassic)return ScreenMouseResult::Classic;
        if(mPresentedScreenScene!=FittedInputScene())return ScreenMouseResult::Blocked;
        t=mPresentedScreenTransform;
    }
    // Unsupported renderer configuration retains classic input; an invalidated
    // snapshot must not reuse the geometry of a previous window/scene.
    if(!t.valid)return ScreenMouseResult::Blocked;
    int ww=0,wh=0,pw=0,ph=0;
    if(!SDL_GetWindowSize(mWindow,&ww,&wh) || !SDL_GetRenderOutputSize(mRenderer,&pw,&ph) ||
       ww!=t.windowW || wh!=t.windowH || pw!=t.outputW || ph!=t.outputH)
        return ScreenMouseResult::Blocked;
    openfodder::ScreenPoint canvas;
    if(!t.WindowToCanvas({double(x),double(y)},canvas)) {
        const bool fit=g_Fodder->mStartParams->ScreenFitEnabled();
        return fit ? ScreenMouseResult::Band : ScreenMouseResult::Blocked;
    }
    // Same legacy cursor domain as Mouse.cpp. Downstream HUD/camera/hotspot
    // adjustments stay in their original functions; do not apply them twice.
    const double mx=std::floor(canvas.x)-32,my=std::floor(canvas.y)+4;
    if(mx<-32768 || mx>32767 || my<-32768 || my>32767)return ScreenMouseResult::Blocked;
    mappedX=static_cast<int16>(mx);mappedY=static_cast<int16>(my);
    return ScreenMouseResult::Mapped;
}

// Used by cursor capture on the simulation thread: no SDL operations here.
unsigned cWindow::FittedInputScene() const {
    const bool fit=g_Fodder->mStartParams->ScreenFitEnabled();
    if (g_Fodder->mPhase_In_Progress) {
        if(g_Fodder->mPhase_ShowMapOverview || (g_Fodder->mPhase_Paused && !g_Fodder->mInterruptCallback)) return 0;
        if(!g_Fodder->mInterruptCallback) return 1;
        return fit ? 4 : 0; // In-mission dialog: GUI coordinates, never world input.
    }
    if (!fit) return 0;
    if (g_Fodder->mBriefing_Screen_Active && !g_Fodder->mInterruptCallback) return 2;
    if (g_Fodder->mRecruit_Screen_Active && g_Fodder->mInterruptCallback) return 3;
    return 4; // Service, intro, selection, save/load, options, credits, endings.
}

bool cWindow::IsMissionCursorInBand() const {
    return mMissionCursorInBand.load() && (mWindowMode || g_Fodder->mStartParams->ScreenFitEnabled()) &&
        g_Fodder->mStartParams->mMouseAlternative && !g_Fodder->mParams->mMouseLocked &&
        !g_Fodder->mParams->mDemoPlayback && FittedInputScene()!=0;
}

// Video has no logical GUI hitboxes; keep raw click-to-skip and discard an
// earlier menu/world inverse before the external texture is presented.
void cWindow::BeginVideoPresentation() {
    InvalidateScreenTransform();
    SetMissionCursorInBand(false);
    std::lock_guard<std::mutex> lock(mScreenTransformMutex);
    mPendingScreenClassic=true;
}

// Options-only transaction. F11 and the classic sizing functions are unchanged.
bool cWindow::CapturePresentation(PresentationState& s) const {
    if (!mWindow || !SDL_GetWindowSize(mWindow,&s.w,&s.h) ||
        !SDL_GetWindowPosition(mWindow,&s.x,&s.y)) return false;
    const auto flags=SDL_GetWindowFlags(mWindow);
    s.fullscreen=(flags & SDL_WINDOW_FULLSCREEN)!=0;
    s.maximized=(flags & SDL_WINDOW_MAXIMIZED)!=0;
    s.resizable=(flags & SDL_WINDOW_RESIZABLE)!=0;
    s.relative=SDL_GetWindowRelativeMouseMode(mWindow);
    s.scaler=mScaler; s.previousScaler=mScalerPrevious;
    return s.w>0 && s.h>0;
}

bool cWindow::ApplyPresentation(const PresentationState& s) {
    InvalidateScreenTransform();
    SetMissionCursorInBand(false);
    if (!mWindow || s.w<=0 || s.h<=0 || s.scaler<1 || s.scaler>255) return false;
    // A resize request is ignored while maximized/fullscreen. Verify the
    // actual state after SDL's asynchronous transitions, not just its request.
    if (!SDL_SetWindowFullscreen(mWindow,false) || !SDL_SyncWindow(mWindow) ||
        !SDL_RestoreWindow(mWindow) || !SDL_SyncWindow(mWindow) ||
        !SDL_SetWindowResizable(mWindow,s.resizable) ||
        !SDL_SetWindowSize(mWindow,s.w,s.h) ||
        !SDL_SetWindowPosition(mWindow,s.x,s.y) || !SDL_SyncWindow(mWindow)) return false;
    if (s.maximized && (!SDL_MaximizeWindow(mWindow) || !SDL_SyncWindow(mWindow))) return false;
    if (s.fullscreen && (!SDL_SetWindowFullscreen(mWindow,true) || !SDL_SyncWindow(mWindow))) return false;
    if (!SDL_SetWindowRelativeMouseMode(mWindow,s.relative)) return false;
    PresentationState actual;
    if (!CapturePresentation(actual) || actual.fullscreen!=s.fullscreen ||
        (!s.fullscreen && actual.maximized!=s.maximized) || actual.resizable!=s.resizable ||
        actual.relative!=s.relative ||
        (!s.fullscreen && !s.maximized && (actual.w!=s.w || actual.h!=s.h))) return false;
    mWindowMode=!s.fullscreen; mScaler=static_cast<uint8>(s.scaler);
    mScalerPrevious=static_cast<uint8>(s.previousScaler); mResized=true;
    return true;
}

bool cWindow::PreviewPresentation(bool windowed,int scale,bool resizable,bool relative) {
    PresentationState target;
    if (!CapturePresentation(target)) return false;
    target.fullscreen=!windowed; target.maximized=false;
    target.resizable=resizable; target.relative=relative;
    const auto* display=SDL_GetCurrentDisplayMode(SDL_GetDisplayForWindow(mWindow));
    if (!display) return false;
    if (scale==0) {
        scale=1;
        while (scale<6 && mOriginalResolution.mWidth*scale<=unsigned(display->w/2) &&
               mOriginalResolution.mHeight*scale<=unsigned(display->h/2)) ++scale;
    }
    if (scale<1 || scale>6) return false;
    target.previousScaler=scale;
    target.scaler=windowed ? scale : CalculateFullscreenSize();
    target.w=mOriginalResolution.mWidth*scale; target.h=mOriginalResolution.mHeight*scale;
    return ApplyPresentation(target);
}
