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

#include "Utils/ScreenTransform.hpp"
#include <mutex>
#include <atomic>

class cWindow {
	
	protected:
		SDL_Window*			mWindow;
		SDL_Renderer*		mRenderer;

        std::vector<cEvent> mEvents;
        std::mutex mScreenTransformMutex;
        openfodder::ScreenTransform mPendingScreenTransform, mPresentedScreenTransform;
        bool mPendingScreenClassic=false, mPresentedScreenClassic=false;
        unsigned mPendingScreenScene=0, mPresentedScreenScene=0;
        std::atomic<bool> mMissionCursorInBand{false};
        bool mSystemMissionCursorShown=false;

		cDimension			mOriginalResolution;

		cDimension			mScreenSize;

		uint8				mScaler, mScalerPrevious;

		bool				mWindowMode;
        bool                mHasFocus;
		bool				mResized;

	protected:


	public:

							cWindow();
		virtual				~cWindow();

        int TryRenderMissionHD(cSurface*,const SDL_FRect&,const SDL_FRect&);
        struct PresentationState {
            int x=0, y=0, w=0, h=0, scaler=1, previousScaler=1;
            bool fullscreen=false, maximized=false, resizable=false, relative=false;
        };
        bool CapturePresentation(PresentationState& state) const;
        bool ApplyPresentation(const PresentationState& state);
        bool PreviewPresentation(bool windowed, int scale, bool resizable, bool relative);
		void		        CalculateWindowSize();
		int16				CalculateFullscreenSize();

		bool				CanChangeToMultiplier( const int pNewMultiplier );

        void SetMissionCursorInBand(bool outside) { mMissionCursorInBand.store(outside); }
        bool IsMissionCursorInBand() const;
        unsigned FittedInputScene() const;
        void InvalidateScreenTransform();
        void BeginVideoPresentation();
        openfodder::ScreenMouseResult MapMissionMouse(int x, int y, int16& mappedX, int16& mappedY);
        bool                Cycle();

        std::vector<cEvent>* EventGet();
		virtual void		EventCheck();
		virtual void		FrameEnd();

		virtual bool		InitWindow( const std::string& pWindowTitle );
			
		virtual void		PositionWindow();

		virtual void		RenderAt( cSurface* pImage, bool pMission = false );
		virtual void		RenderShrunk( cSurface* pImage );

		void				WindowIncrease();
		void				WindowDecrease();

        bool                isFullscreen() const;
        bool                isGrabbed() const;
		bool				isMouseInside() const;
		bool				isResized() const;
        bool                isMouseButtonPressed_Global() const;

        void				SetMousePosition(const cPosition& pPosition);
        void                SetMousePositionInWindow(float pX, float pY);
		void				SetMouseSpeed(float pSpeed);

		void				SetScreenSize( const cDimension& pDimension );
		void				SetOriginalRes( const cDimension& pDimension );

		void				SetWindowTitle( const std::string& pWindowTitle );
		void				SetWindowSize(const int pMultiplier);
        bool                GetWindowBordersSize(int* pTop, int* pLeft, int* pBottom, int* pRight) const;

		void				ToggleFullscreen();
		void				ClearResized();

		SDL_Renderer*		GetRenderer() const { return mRenderer; };

        cPosition           GetWindowPosition() const;
        int32				GetWindowWidth() const;
		int32				GetWindowHeight() const;
        int                 GetScaler() const { return mScaler; }

		cDimension	        GetWindowSize() const;
		cDimension	        GetScreenSize() const { return mScreenSize; }
		bool			    GetWindowMode() const { return mWindowMode; }
        bool                hasFocusEvent() const { return mHasFocus; }
		void				clearFocus() { mHasFocus = false; }
        cDimension          GetScale() const;

		void				SetRelativeMouseMode(bool pEnable);
		void				ToggleVSync(bool pEnabled);
		float				GetRefreshRate();


};

class cWindowNull : public cWindow {

public:
	virtual ~cWindowNull() {}
    virtual bool InitWindow(const std::string& pWindowTitle);
};
