"""Only the explicit screen adapter may differ from classic Mouse.cpp. GPL-3.0-or-later."""
ADAPTER = '        static bool blockedPress=false;\n        int16 mappedX=0,mappedY=0;\n        const auto mapping=mWindow->MapMissionMouse(mMouse_EventLastPosition.mX,\n            mMouse_EventLastPosition.mY,mappedX,mappedY);\n        if(mapping!=openfodder::ScreenMouseResult::Classic) {\n            if(!mMouse_EventLastButtonsPressed)blockedPress=false;\n            if(mapping==openfodder::ScreenMouseResult::Blocked) {\n                if(mMouse_EventLastButtonsPressed)blockedPress=true;\n                mMouseButtonStatus=0;\n                return; // Keep prior cursor; never turn a band click into a map order.\n            }\n            mInputMouseX=mappedX;mInputMouseY=mappedY;\n            if(blockedPress)mMouseButtonStatus=0; // Release before re-entering with a held press.\n            return;\n        }\n        blockedPress=false;\n'

def without_screen_mouse(source):
    assert source.count(ADAPTER) == 1, "Screen mouse adapter changed; review its differential tests"
    return source.replace(ADAPTER, "")
