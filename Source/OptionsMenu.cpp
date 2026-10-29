#include "stdafx.hpp"

#include <algorithm>
#include <sstream>
#include <string>
#include <vector>
#include <iostream>

// Opt-in, flushed breadcrumbs: no paths, settings contents or private data.
static void OptionsTrace(const char* stage) {
    if (std::getenv("OPENFODDER_OPTIONS_TRACE"))
        std::cerr << "[options] " << stage << std::endl;
}

static int clamp_int(int v, int lo, int hi) {
    if (v < lo) return lo;
    if (v > hi) return hi;
    return v;
}


static std::string trunc_label_px(const std::string& s, int maxPx) {
    if (maxPx <= 0) return "";
    std::string upper = s;
    std::transform(upper.begin(), upper.end(), upper.begin(), ::toupper);
    const int ellipsisW = g_Fodder->String_MeasureWidth(mFont_Briefing_Width, "...");
    if (ellipsisW >= maxPx)
        return "...";

    const int maxContent = maxPx - ellipsisW;
    int w = 0;
    size_t cut = 0;
    for (; cut < upper.size(); ++cut) {
        const unsigned char c = (unsigned char)upper[cut];
        const int cw = (int)mFont_Briefing_Width[c];
        if (w + cw > maxContent)
            break;
        w += cw;
    }

    if (cut >= upper.size())
        return upper;

    return upper.substr(0, cut) + "...";
}

static void SetupRowHitbox(const size_t x1, const size_t x2, const size_t y, const int rowH) {
    g_Fodder->mGUI_Temp_X = (int16)x1;
    g_Fodder->mGUI_Temp_Y = (int16)y;
    const int32 w = (int32)x2 - (int32)x1;
    g_Fodder->mGUI_Temp_Width = (int16)((w > 0) ? w : 0);
    g_Fodder->mGUI_Draw_LastHeight = (int16)((rowH > 5) ? (rowH - 5) : 0);
}
static inline uint32_t now_ms_u32() {
    using clock = std::chrono::steady_clock;
    const auto ms = std::chrono::duration_cast<std::chrono::milliseconds>(
        clock::now().time_since_epoch()
    ).count();
    return (uint32_t)ms;
}

enum eGUI_Action : int16 {
    GUIACT_NONE = 0,

    // Chrome (buttons on the right) - removed from rendering, but actions kept
    GUIACT_OPT_UP,
    GUIACT_OPT_DOWN,
    GUIACT_OPT_BACK,

    // Row clicks
    GUIACT_OPT_ROW_PRIMARY,   // click row => toggle/inc
    GUIACT_OPT_LEFT,          // decrement (hover arrow)
    GUIACT_OPT_RIGHT,         // increment (hover arrow)
    GUIACT_OPT_TAB,           // arg = page index
    GUIACT_OPT_SAVE,
    GUIACT_OPT_CANCEL,

    // Action rows (Defaults / Back)
    GUIACT_OPT_ACTION,        // arg = OPT_DEFAULTS / OPT_BACK
};

static inline bool IsAdjustAction(int16 action) {
    return action == GUIACT_OPT_LEFT
        || action == GUIACT_OPT_RIGHT
        || action == GUIACT_OPT_ROW_PRIMARY
        || action == GUIACT_OPT_ACTION;
}

// Generic callback thunk for all options-menu GUI elements.
static void Gui_OptionsMenu_Click(void* ctx, int16 action, int16 arg) {
    cOptionsMenu* menu = static_cast<cOptionsMenu*>(ctx);
    if (!menu) return;
    menu->OnRowClick(action, arg);
}

cOptionsMenu::cOptionsMenu() = default;
cOptionsMenu::~cOptionsMenu() = default;

void cOptionsMenu::Open() {
    mDone = false;
    mApplied = false;
    mCurrentIndex = 0;
    mCurrentPage = 0;
    mConfirmation.Clear(); mPreviewApplied=false; mStatus.clear();

    // Reset input limiter state
    mLastInputMs = 0;
    mLastInputAction = 0;
    mLastInputArg = 0;

    if (g_Fodder && g_Fodder->mStartParams) {
        mSnapshot = *g_Fodder->mStartParams;
        mDraft = mSnapshot;
        if (g_Fodder->mWindow) mDraft.mWindowMode = !g_Fodder->mWindow->isFullscreen();
        mSnapshotValid = true;
    }
    else {
        mSnapshotValid = false;
    }

    BuildItems();
    BuildPageItems();
}

void cOptionsMenu::Close() {
    mItems.clear();
    mDrawStrings.clear();
    mDone = true;
}

bool cOptionsMenu::AllowInput(int16 action, int16 arg) {
    // Tune to taste:
    //  - Debounce prevents "double fire" in the same click/frame sequence
    //  - Repeat limits "machine-gun" behaviour if something keeps triggering
    const uint32_t kDebounceMs = 120;
    const uint32_t kRepeatMs = 90;

    if (!IsAdjustAction(action))
        return true;

    const uint32_t t = now_ms_u32();

    // Same exact event spamming? Rate limit.
    if (action == mLastInputAction && arg == mLastInputArg) {
        const uint32_t dt = t - mLastInputMs;
        if (dt < kRepeatMs)
            return false;
    }
    else {
        // Different action/target very soon after last input: debounce.
        const uint32_t dt = t - mLastInputMs;
        if (dt < kDebounceMs)
            return false;
    }

    mLastInputMs = t;
    mLastInputAction = action;
    mLastInputArg = arg;
    return true;
}

void cOptionsMenu::BuildItems() {
    mItems.clear();

    // -------------------------------------------------------------------------
    // Video / Window
    // -------------------------------------------------------------------------
    mItems.push_back({ eOptType::Toggle, eOptSection::Video, "Presentation", OPT_PRESENTATION });
    mItems.push_back({ eOptType::Toggle, eOptSection::Video, "Window mode",     OPT_WINDOW_MODE });
    mItems.push_back({ eOptType::IntRange, eOptSection::Video, "Window scale",    OPT_WINDOW_SCALE, 0, 6, 1 });
    mItems.push_back({ eOptType::Toggle, eOptSection::Video, "Integer scaling", OPT_INTEGER_SCALING });

    // These were in INI but missing from menu
    //mItems.push_back({ eOptType::IntRange, "Window columns",  OPT_WINDOW_COLUMNS, 0, 80, 1 }); // 0=AUTO
    //mItems.push_back({ eOptType::IntRange, "Window rows",     OPT_WINDOW_ROWS,    0, 60, 1 }); // 0=AUTO

    // -------------------------------------------------------------------------
    // Input
    // -------------------------------------------------------------------------
    mItems.push_back({ eOptType::Toggle, eOptSection::Input, "Alternate mouse", OPT_ALTERNATE_MOUSE });
    mItems.push_back({ eOptType::Toggle, eOptSection::Input, "Mouse locked",    OPT_MOUSE_LOCKED });
    mItems.push_back({ eOptType::IntRange, eOptSection::Input, "Mouse speed x10", OPT_MOUSE_SPEED, 5, 100, 5 });

    // -------------------------------------------------------------------------
    // Audio (no separate page)
    // -------------------------------------------------------------------------

    // Skip flags from INI
    mItems.push_back({ eOptType::Toggle, eOptSection::Skip, "Skip intro",    OPT_SKIP_INTRO });
    mItems.push_back({ eOptType::Toggle, eOptSection::Skip, "Skip briefing", OPT_SKIP_BRIEFING });
    mItems.push_back({ eOptType::Toggle, eOptSection::Skip, "Skip service",  OPT_SKIP_SERVICE });
    mItems.push_back({ eOptType::Toggle, eOptSection::Skip, "Skip hill",     OPT_SKIP_RECRUIT });

    // -------------------------------------------------------------------------
    // Engine
    // -------------------------------------------------------------------------
    // (platform/engine)
    {
        sOptItem plat{ eOptType::EnumCycle, eOptSection::Engine, "Default platform", OPT_DEFAULT_PLATFORM };
        plat.enumCount = 2; // Amiga / PC
        mItems.push_back(plat);

        sOptItem game{ eOptType::EnumCycle, eOptSection::Engine, "Default game", OPT_DEFAULT_GAME };
        game.enumCount = 1; // CF1 / CF2
        mItems.push_back(game);
    }

    mItems.push_back({ eOptType::Toggle, eOptSection::Engine, "Copy protection", OPT_COPY_PROTECTION });
    mItems.push_back({ eOptType::Toggle, eOptSection::Video, "Disable CF1 CD32 Video", OPT_DISABLE_INTRO_VIDEO });

    //mItems.push_back({ eOptType::IntRange, eOptSection::Engine, "Engine speed", OPT_SLEEP_DELTA, 5, 40, 1 });
    //mItems.push_back({ eOptType::IntRange, eOptSection::Engine, "Max sprites",  OPT_MAX_SPRITES, 16, 100000, 1 });
    //mItems.push_back({ eOptType::IntRange, eOptSection::Engine, "Max spawn",    OPT_MAX_SPAWN,   0, 1000, 1 });
    mItems.push_back({ eOptType::Toggle, eOptSection::Engine, "Disable sound", OPT_DISABLE_SOUND });
    mItems.push_back({ eOptType::Toggle, eOptSection::Engine, "Enable cheats", OPT_CHEATS });


    mCount = (int16_t)mItems.size();
}

void cOptionsMenu::BuildPageItems() {
    mPageItems.clear();

    const eOptSection pageSections[4] = {
        eOptSection::Video,
        eOptSection::Input,
        eOptSection::Skip,
        eOptSection::Engine
    };
    const eOptSection pageSection = pageSections[mCurrentPage];
    for (size_t i = 0; i < mItems.size(); ++i) {
        if (mItems[i].section == pageSection)
            mPageItems.push_back((int)i);
    }

    mCount = (int16_t)mPageItems.size();
    if (mCurrentIndex < 0) mCurrentIndex = 0;
    if (mCurrentIndex > mCount) mCurrentIndex = mCount;
}

void cOptionsMenu::ChangePage(int pageIndex) {
    const int pageCount = 4;
    if (pageIndex < 0) pageIndex = 0;
    if (pageIndex >= pageCount) pageIndex = pageCount - 1;

    if (mCurrentPage == pageIndex)
        return;

    mCurrentPage = (int16_t)pageIndex;
    mCurrentIndex = 0;
    BuildPageItems();
}

void cOptionsMenu::RestoreSnapshot() {
    mConfirmation.Clear();
    if (mPreviewApplied) {
        *g_Fodder->mStartParams=mSnapshot;
        *g_Fodder->mParams=mRuntimeSnapshot;
        const bool restored=g_Fodder->mWindow->ApplyPresentation(mWindowSnapshot);
        g_Fodder->mWindow->SetMouseSpeed(mSnapshot.mMouseSpeed);
        if (!restored) mStatus="RESTORE FAILED";
        // Keep the recovery snapshot alive and prevent saving until recovery succeeds.
        mPreviewApplied=!restored;
    }
    mDraft=mSnapshot;
    mApplied=false;
}

bool cOptionsMenu::PresentationChanged() const {
    return mDraft.mFitPresentation!=mSnapshot.mFitPresentation ||
        mDraft.mWindowMode!=!g_Fodder->mWindow->isFullscreen() ||
        mDraft.mWindowScale!=mSnapshot.mWindowScale ||
        mDraft.mIntegerScaling!=mSnapshot.mIntegerScaling ||
        mDraft.mMouseAlternative!=mSnapshot.mMouseAlternative ||
        mDraft.mMouseLocked!=mSnapshot.mMouseLocked;
}

void cOptionsMenu::SaveOrPreview() {
    if (mPreviewApplied) { RestoreSnapshot(); return; }
    OptionsTrace("SAVE begin");
    mStatus.clear();
    if (!PresentationChanged()) { Confirm(); return; }
    if (!g_Fodder->mWindow->CapturePresentation(mWindowSnapshot)) {
        mStatus="WINDOW ERROR"; return;
    }
    OptionsTrace("SAVE window captured");
    mRuntimeSnapshot=*g_Fodder->mParams;
    mPreviewApplied=true;
    *g_Fodder->mStartParams=mDraft;
    g_Fodder->mParams->mFitPresentation=mDraft.mFitPresentation;
    g_Fodder->mParams->mWindowMode=mDraft.mWindowMode;
    g_Fodder->mParams->mIntegerScaling=mDraft.mIntegerScaling;
    g_Fodder->mParams->mMouseAlternative=mDraft.mMouseAlternative;
    g_Fodder->mParams->mMouseLocked=mDraft.mMouseLocked;
    const bool fit=mDraft.ScreenTransformEnabled() && mDraft.ScreenFitEnabled() &&
        mDraft.mMouseAlternative && !mDraft.mMouseLocked;
    OptionsTrace("SAVE applying preview");
    if (!g_Fodder->mWindow->PreviewPresentation(mDraft.mWindowMode,int(mDraft.mWindowScale),fit,
            !mDraft.mMouseAlternative || mDraft.mMouseLocked)) {
        mStatus="WINDOW ERROR"; RestoreSnapshot(); return;
    }
    OptionsTrace("SAVE preview applied");
    if (!g_Fodder->mWindow->CapturePresentation(mPreviewState)) {
        mStatus="WINDOW ERROR"; RestoreSnapshot(); return;
    }
    mConfirmation.Begin(now_ms_u32());
    mTracePreviewDrawn=false;
    OptionsTrace("SAVE confirmation pending");
}

void cOptionsMenu::Confirm() {
    OptionsTrace("KEEP or direct SAVE begin");
    if (mConfirmation.Expired(now_ms_u32())) {
        mStatus="TIME EXPIRED"; RestoreSnapshot(); return;
    }
    if (mConfirmation.pending) {
        cWindow::PresentationState actual;
        if (!g_Fodder->mWindow->CapturePresentation(actual) ||
            actual.fullscreen!=mPreviewState.fullscreen || actual.maximized!=mPreviewState.maximized ||
            actual.w!=mPreviewState.w || actual.h!=mPreviewState.h ||
            actual.relative!=mPreviewState.relative || actual.resizable!=mPreviewState.resizable) {
            mStatus="WINDOW CHANGED"; RestoreSnapshot(); return;
        }
    }
    // Write only an explicitly confirmed candidate. Save failure leaves the
    // last confirmed file intact and restores the live preview.
    OptionsTrace("SAVE writing INI");
    if (!mDraft.SaveIni()) { mStatus="SAVE FAILED"; RestoreSnapshot(); return; }
    *g_Fodder->mStartParams=mDraft;
    g_Fodder->mParams->mCopyProtection=mDraft.mCopyProtection;
    g_Fodder->mWindow->SetMouseSpeed(mDraft.mMouseSpeed);
    mConfirmation.Clear(); mPreviewApplied=false;
    mApplied=true; mDone=true;
    OptionsTrace("SAVE committed");
}

int cOptionsMenu::GetInt(int optId) const {
    switch (optId) {
    case OPT_PRESENTATION: return mDraft.mFitPresentation ? 1 : 0;
    case OPT_WINDOW_MODE:
        return mDraft.mWindowMode ? 1 : 0;
    case OPT_WINDOW_SCALE:
        return (int)mDraft.mWindowScale;
    case OPT_INTEGER_SCALING:  return mDraft.mIntegerScaling ? 1 : 0;

    case OPT_WINDOW_COLUMNS:   return (int)mDraft.mWindowColumns;
    case OPT_WINDOW_ROWS:      return (int)mDraft.mWindowRows;
    case OPT_COPY_PROTECTION:  return mDraft.mCopyProtection ? 1 : 0;

    case OPT_ALTERNATE_MOUSE:  return mDraft.mMouseAlternative ? 1 : 0;
    case OPT_MOUSE_LOCKED:     return mDraft.mMouseLocked ? 1 : 0;
    case OPT_MOUSE_SPEED:      return (int)(mDraft.mMouseSpeed * 10.0f + 0.5f);

    case OPT_DISABLE_SOUND:    return mDraft.mDisableSound ? 1 : 0;
    case OPT_CHEATS:           return mDraft.mCheatsEnabled ? 1 : 0;

    case OPT_SKIP_INTRO:       return mDraft.mSkipIntro ? 1 : 0;
    case OPT_DISABLE_INTRO_VIDEO: return mDraft.mDisableIntroVideo ? 1 : 0;
    case OPT_SKIP_BRIEFING:    return mDraft.mSkipBriefing ? 1 : 0;
    case OPT_SKIP_SERVICE:     return mDraft.mSkipService ? 1 : 0;
    case OPT_SKIP_RECRUIT:     return mDraft.mSkipRecruit ? 1 : 0;

    case OPT_SLEEP_DELTA:      return (int)mDraft.mSleepDelta;
    case OPT_MAX_SPRITES:      return (int)mDraft.mSpritesMax;
    case OPT_MAX_SPAWN:        return (int)mDraft.mSpawnEnemyMax;

    case OPT_DEFAULT_PLATFORM: return (mDraft.mDefaultPlatform == ePlatform::PC) ? 1 : 0;
    case OPT_DEFAULT_GAME:     return (mDraft.mDefaultGame == eGame::CF2) ? 1 : 0;

    default: return 0;
    }
}

void cOptionsMenu::SetInt(int optId, int v) {
    switch (optId) {
    case OPT_PRESENTATION: mDraft.mFitPresentation=(v!=0); break;
    case OPT_WINDOW_MODE: mDraft.mWindowMode=(v!=0); break;
    case OPT_INTEGER_SCALING: mDraft.mIntegerScaling=(v!=0); break;
    case OPT_COPY_PROTECTION: mDraft.mCopyProtection=(v!=0); break;
    case OPT_ALTERNATE_MOUSE: mDraft.mMouseAlternative=(v!=0); break;
    case OPT_MOUSE_LOCKED: mDraft.mMouseLocked=(v!=0); break;
    case OPT_DISABLE_SOUND: mDraft.mDisableSound=(v!=0); break;
    case OPT_CHEATS: mDraft.mCheatsEnabled=(v!=0); break;
    case OPT_SKIP_INTRO: mDraft.mSkipIntro=(v!=0); break;
    case OPT_DISABLE_INTRO_VIDEO: mDraft.mDisableIntroVideo=(v!=0); break;
    case OPT_SKIP_BRIEFING: mDraft.mSkipBriefing=(v!=0); break;
    case OPT_SKIP_SERVICE: mDraft.mSkipService=(v!=0); break;
    case OPT_SKIP_RECRUIT: mDraft.mSkipRecruit=(v!=0); break;
    case OPT_WINDOW_SCALE: mDraft.mWindowScale=clamp_int(v,0,6); break;
    case OPT_WINDOW_COLUMNS: mDraft.mWindowColumns=clamp_int(v,0,80); break;
    case OPT_WINDOW_ROWS: mDraft.mWindowRows=clamp_int(v,0,60); break;
    case OPT_SLEEP_DELTA: mDraft.mSleepDelta=clamp_int(v,5,40); break;
    case OPT_MAX_SPRITES: mDraft.mSpritesMax=clamp_int(v,45,100000); break;
    case OPT_MAX_SPAWN: mDraft.mSpawnEnemyMax=clamp_int(v,0,1000); break;
    case OPT_MOUSE_SPEED: mDraft.mMouseSpeed=clamp_int(v,5,100)/10.0f; break;
    case OPT_DEFAULT_PLATFORM: mDraft.mDefaultPlatform=v==1 ? ePlatform::PC : ePlatform::Amiga; break;
    case OPT_DEFAULT_GAME: mDraft.mDefaultGame=v==1 ? eGame::CF2 : eGame::CF1; break;
    default: break;
    }
    mStatus.clear();
}

std::string cOptionsMenu::FormatValue(const sOptItem& it) const {
    const int v = GetInt(it.id);

    if (it.id == OPT_PRESENTATION) return v ? "FIT" : "CLASSIC";
    if (it.type == eOptType::Toggle)
        return v ? "ON" : "OFF";

    if (it.id == OPT_WINDOW_SCALE) {
        if (v == 0) return "AUTO";
        return std::to_string(v);
    }

    if (it.id == OPT_WINDOW_COLUMNS) {
        if (v == 0) return "AUTO";
        return std::to_string(v);
    }

    if (it.id == OPT_WINDOW_ROWS) {
        if (v == 0) return "AUTO";
        return std::to_string(v);
    }

    if (it.id == OPT_DEFAULT_PLATFORM) {
        return (v == 1) ? "PC" : "AMIGA";
    }

    if (it.id == OPT_DEFAULT_GAME) {
        return (v == 1) ? "CF2" : "CF1";
    }

    if (it.id == OPT_MOUSE_SPEED) {
        return std::to_string(v);
    }

    return std::to_string(v);
}

void cOptionsMenu::Draw() {
    g_Fodder->mSurface->clearBuffer();
    g_Fodder->mGraphics->SetActiveSpriteSheet(eGFX_BRIEFING);
    g_Fodder->GUI_Element_Reset();

    g_Fodder->mString_GapCharID = 0x25;
    g_Fodder->String_Print_Large(mStatus.empty() ? "OPTIONS" : mStatus, false, 0x01);
    g_Fodder->mString_GapCharID = 0;

    if (mConfirmation.pending) {
        if (!mTracePreviewDrawn) OptionsTrace("confirmation draw begin");
        const std::string question="KEEP CHANGES? " + std::to_string(mConfirmation.Seconds(now_ms_u32()));
        g_Fodder->String_Print_Small_LeftInBox(question,32,288,64);
        g_Fodder->String_Print_Small_LeftInBox("REVERTS AFTER 15 SECONDS",32,288,88);
        g_Fodder->GUI_Button_Draw_SmallBoxAt("KEEP",48,144,120,0xB2,0xB3,eTextAlign::Centre);
        g_Fodder->GUI_Button_Setup_New(Gui_OptionsMenu_Click,this,GUIACT_OPT_SAVE,0);
        g_Fodder->GUI_Button_Draw_SmallBoxAt("REVERT",160,256,120,0xB2,0xB3,eTextAlign::Centre);
        g_Fodder->GUI_Button_Setup_New(Gui_OptionsMenu_Click,this,GUIACT_OPT_CANCEL,0);
        if (!mTracePreviewDrawn) OptionsTrace("confirmation draw complete");
        mTracePreviewDrawn=true;
        return;
    }
    const int tabY = PLATFORM_BASED(0x1A, 0x18);
    const int rowBaseY = tabY + 0x18;
    const int rowH = RowH();
    const int16 pageCount = 4;
    const char* pageLabels[pageCount] = { "VID", "IN", "SKIP", "ENG" };

    // Layout
    const size_t xRowL = 0x20;
    const size_t xRowR = 0x120;
    const size_t gap = 2;

    const size_t arrowW = 0x10;
    const size_t valueW = 0x30;

    const size_t xArrowRightR = xRowR - 2;
    const size_t xArrowRightL = xArrowRightR - arrowW;
    const size_t xValueR = xArrowRightL - gap;
    const size_t xValueL = xValueR - valueW;
    const size_t xArrowLeftR = xValueL - gap;
    const size_t xArrowLeftL = xArrowLeftR - arrowW;
    const size_t xLabelL = xRowL + 2;
    const size_t xLabelR = (xArrowLeftL > gap) ? (xArrowLeftL - gap) : xLabelL;

    int maxLabelPx = (int)xLabelR - (int)xLabelL - 6;
    if (maxLabelPx < 0)
        maxLabelPx = 0;

    // Top page tabs
    {
        const size_t tabGap = 6;
        const size_t totalW = xRowR - xRowL + 1;
        const size_t tabW = (totalW - (tabGap * (pageCount - 1))) / pageCount;
        for (int16 i = 0; i < pageCount; ++i) {
            const size_t x1 = xRowL + (i * (tabW + tabGap));
            const size_t x2 = x1 + tabW - 1;
            const bool selected = (i == mCurrentPage);
            const size_t shade = selected ? 0xF3 : 0xB2;
            const size_t prim = selected ? 0xF2 : 0xB3;
            g_Fodder->GUI_Button_Draw_SmallBoxAt(pageLabels[i], x1, x2, tabY, prim, shade, eTextAlign::Centre);
            g_Fodder->GUI_Button_Setup_New(Gui_OptionsMenu_Click, this, GUIACT_OPT_TAB, i);
        }
    }

    // Visible rows for current page
    struct sVisibleRow {
        int idx;
        size_t y;
    };

    std::vector<sVisibleRow> visible;
    visible.reserve(mShownItems);

    for (int16_t vis = 0; vis < mShownItems; ++vis) {
        const int pageIdx = (int)mCurrentIndex + vis;
        if (pageIdx < 0 || pageIdx >= mCount) break;
        const size_t y = (size_t)(rowBaseY + (vis * rowH));
        visible.push_back({ mPageItems[(size_t)pageIdx], y });
    }

    // Single group box for the page
    if (!visible.empty()) {
        const int groupPadTop = 4;
        const int groupPadBottom = 5;
        const int16 boxX = (int16)(xRowL - 2);
        const int16 boxY = (int16)(visible.front().y - groupPadTop);
        const int16 boxW = (int16)(xRowR - xRowL + 4);
        const int16 boxH = (int16)((visible.back().y + rowH + groupPadBottom) - visible.front().y);
        g_Fodder->Briefing_DrawBox(boxX, boxY, boxW, boxH, 0xF3);
        g_Fodder->Briefing_DrawBox(boxX - 1, boxY - 1, boxW, boxH, 0xF2);
    }

    // Row separators inside the page box
    for (size_t i = 0; i + 1 < visible.size(); ++i) {
        const int16 yLine = (int16)(visible[i].y + rowH - 5);
        g_Fodder->Briefing_Draw_Horizontal_Line((int16)xRowL + 0x10, (int16)xRowR + 0x10, (int16)(yLine + 0x10), 0xF2);
    }

    for (size_t i = 0; i < visible.size(); ++i) {
        const int idx = visible[i].idx;
        const size_t y = visible[i].y;
        const sOptItem& it = mItems[(size_t)idx];

        const std::string label = trunc_label_px(it.label, maxLabelPx);
        g_Fodder->String_Print_Small_LeftInBox(label, xLabelL, xLabelR, y);

        g_Fodder->GUI_Button_Draw_SmallBoxAt(FormatValue(it), xValueL, xValueR, y, 0xB2, 0xB3, eTextAlign::Centre);

        const bool hasArrows = (it.type == eOptType::IntRange || it.type == eOptType::EnumCycle);
        if (hasArrows) {
            g_Fodder->GUI_Button_Draw_SmallBoxAt("N", xArrowLeftL, xArrowLeftR, y, 0xB2, 0xB3, eTextAlign::Centre);
            g_Fodder->GUI_Button_Setup_New(Gui_OptionsMenu_Click, this, GUIACT_OPT_LEFT, (int16)idx);

            g_Fodder->GUI_Button_Draw_SmallBoxAt("P", xArrowRightL, xArrowRightR, y, 0xB2, 0xB3, eTextAlign::Centre);
            g_Fodder->GUI_Button_Setup_New(Gui_OptionsMenu_Click, this, GUIACT_OPT_RIGHT, (int16)idx);
        }

        SetupRowHitbox(xRowL, xRowR, y, rowH);
        g_Fodder->GUI_Button_Setup_New(Gui_OptionsMenu_Click, this, GUIACT_OPT_ROW_PRIMARY, (int16)idx);
    }

    if (mCurrentPage==0) {
        const bool overridden=std::getenv("OPENFODDER_MISSION_SCREEN_TRANSFORM") || std::getenv("OPENFODDER_MISSION_SCREEN_FIT");
        const char* hint=overridden ? "LAUNCHER OVERRIDES PRESENTATION" :
            "FIT: FREE ALTERNATE MOUSE";
        g_Fodder->String_Print_Small_LeftInBox(hint,32,288,158);
    }
    // Bottom actions (fixed to bottom of the screen)
    {
        const size_t screenH = (size_t)g_Fodder->mWindow->GetScreenSize().getHeight();
        const size_t yBottom = (screenH > 0x20) ? (screenH - 0x1C) : (rowBaseY + (mShownItems * rowH) + 6);
        const size_t buttonW = 0x40;
        const size_t gapW = 0x08;
        const size_t totalW = (buttonW * 3) + (gapW * 2);
        const size_t xStart = ((xRowL + xRowR) / 2) - (totalW / 2);
        const size_t xDefaultsL = xStart;
        const size_t xDefaultsR = xDefaultsL + buttonW;
        const size_t xSaveL = xDefaultsR + gapW;
        const size_t xSaveR = xSaveL + buttonW;
        const size_t xCancelL = xSaveR + gapW;
        const size_t xCancelR = xCancelL + buttonW;

        g_Fodder->GUI_Button_Draw_SmallBoxAt("DEFAULTS", xDefaultsL, xDefaultsR, yBottom, 0xB2, 0xB3, eTextAlign::Centre);
        g_Fodder->GUI_Button_Setup_New(Gui_OptionsMenu_Click, this, GUIACT_OPT_ACTION, OPT_DEFAULTS);

        g_Fodder->GUI_Button_Draw_SmallBoxAt("SAVE", xSaveL, xSaveR, yBottom, 0xB2, 0xB3, eTextAlign::Centre);
        g_Fodder->GUI_Button_Setup_New(Gui_OptionsMenu_Click, this, GUIACT_OPT_SAVE, 0);

        g_Fodder->GUI_Button_Draw_SmallBoxAt("CANCEL", xCancelL, xCancelR, yBottom, 0xB2, 0xB3, eTextAlign::Centre);
        g_Fodder->GUI_Button_Setup_New(Gui_OptionsMenu_Click, this, GUIACT_OPT_CANCEL, 0);
    }
}

void cOptionsMenu::Tick() {
    if (mConfirmation.Expired(now_ms_u32())) {
        mStatus="TIME EXPIRED"; RestoreSnapshot();
    }
}

void cOptionsMenu::OnUp() {
    if (mCurrentIndex > 0) --mCurrentIndex;
}

void cOptionsMenu::OnDown() {
    if (mCurrentIndex + mShownItems < mCount) ++mCurrentIndex;
}

void cOptionsMenu::OnBack() {
    const bool testing=mConfirmation.pending || mPreviewApplied;
    RestoreSnapshot();
    if (!testing && !mPreviewApplied) mDone=true;
}

int cOptionsMenu::MouseToItemIndex() const {
    const int my = (int)g_Fodder->mMouseY;
    const int rowBaseY = 0x20 + (int)PLATFORM_BASED(0, 25);

    const int rel = my - rowBaseY;
    if (rel < 0) return -1;

    const int row = rel / RowH();
    if (row < 0 || row >= mShownItems) return -1;

    const int idx = (int)mCurrentIndex + row;
    if (idx < 0 || idx >= mCount) return -1;

    if ((size_t)idx >= mPageItems.size())
        return -1;

    return mPageItems[(size_t)idx];
}

void cOptionsMenu::Adjust(sOptItem& it, int dir) {
    if (it.type == eOptType::Toggle) {
        SetInt(it.id, GetInt(it.id) ? 0 : 1);
        return;
    }

    if (it.type == eOptType::IntRange) {
        int v = GetInt(it.id);
        v += dir * it.step;
        v = clamp_int(v, it.minv, it.maxv);
        SetInt(it.id, v);
        return;
    }

    if (it.type == eOptType::EnumCycle) {
        int v = GetInt(it.id);
        v += dir;
        if (v < 0) v = it.enumCount - 1;
        if (v >= it.enumCount) v = 0;
        SetInt(it.id, v);
        return;
    }
}

void cOptionsMenu::ResetDefaults() {
    mDraft.clear(); mStatus.clear();
}

void cOptionsMenu::OnRowClick(int16 action, int16 arg) {
    // IMPORTANT: cooldown / debounce (prevents 60Hz flicker changes)
    if (!AllowInput(action, arg))
        return;

    if (mPreviewApplied && !mConfirmation.pending) { RestoreSnapshot(); return; }
    if (mConfirmation.pending) {
        if (action==GUIACT_OPT_SAVE) Confirm();
        else if (action==GUIACT_OPT_CANCEL || action==GUIACT_OPT_BACK) RestoreSnapshot();
        return;
    }
    if (action == GUIACT_OPT_UP) { OnUp(); return; }
    if (action == GUIACT_OPT_DOWN) { OnDown(); return; }
    if (action == GUIACT_OPT_BACK) { OnBack(); return; }
    if (action == GUIACT_OPT_TAB) { ChangePage(arg); return; }
    if (action == GUIACT_OPT_SAVE) { SaveOrPreview(); return; }
    if (action == GUIACT_OPT_CANCEL) { RestoreSnapshot(); mApplied = false; mDone = true; return; }

    if (action == GUIACT_OPT_ACTION) {
        const int actionId = (int)arg;
        if (actionId == OPT_DEFAULTS) { ResetDefaults(); return; }
        if (actionId == OPT_BACK) { OnBack(); return; }
        return;
    }

    const int idx = (int)arg;
    if (idx < 0 || idx >= (int)mItems.size()) return;

    sOptItem& it = mItems[(size_t)idx];
    if (it.type == eOptType::Spacer) return;

    if (action == GUIACT_OPT_LEFT) { Adjust(it, -1); return; }
    if (action == GUIACT_OPT_RIGHT) { Adjust(it, +1); return; }

    if (it.type == eOptType::Toggle) {
        Adjust(it, +1);
    }
}

std::unique_ptr<cOptionsMenu> mOptionsMenu;

bool cFodder::Options_Menu_Run() {
    mOptionsMenu = std::make_unique<cOptionsMenu>();
    mOptionsMenu->Open();

    mMap_Destroy_Tiles.clear();
    mMouse_Button_Left_Toggle = 0;

    std::function<void()> prevInterruptCallback;
    mGraphics->PaletteSet();
    mSurface->palette_FadeTowardNew();

    {
    std::lock_guard<std::mutex> lock(mSurfaceMtx);
    prevInterruptCallback=mInterruptCallback;
    mInterruptCallback = [this]() {
        Sprites_Draw();
        mOptionsMenu->Draw();
        mGraphics->SetActiveSpriteSheet(eGFX_IN_GAME);
        Mouse_DrawCursor();
        };
    }

    while (!mOptionsMenu->IsDone()) {

        if (mSurface->isPaletteAdjusting())
            mSurface->palette_FadeTowardNew();

        {
        std::lock_guard<std::mutex> lock(mSurfaceMtx);
        // Mouse wheel scroll (one "tick" per frame)
        if (mMouse_EventLastWheel.mY > 0) {
            mOptionsMenu->OnUp();
            mMouse_EventLastWheel.mY = 0;
        }
        else if (mMouse_EventLastWheel.mY < 0) {
            mOptionsMenu->OnDown();
            mMouse_EventLastWheel.mY = 0;
        }

        // Consume the press edge once. A held button is +1 after consumption,
        // not another click; release rearms it in Mouse_UpdateButtons.
        // Mouse click processing
        if (Mouse_Button_Left_Toggled() > 0)
            GUI_Handle_Element_Mouse_Check(mGUI_Elements);

        if (mPhase_EscapeKeyAbort || mPhase_Aborted) {
            mPhase_EscapeKeyAbort = false;
            mPhase_Aborted = false;
            mOptionsMenu->OnBack();
        }

        mOptionsMenu->Tick();
        }

        Video_Sleep();
    }

    const bool applied = mOptionsMenu->WasApplied();

    {
        std::lock_guard<std::mutex> lock(mSurfaceMtx);
        mInterruptCallback = prevInterruptCallback;
        mOptionsMenu->Close();
        mOptionsMenu.reset();
    }

    //Image_FadeOut();
    if (applied && mVersions) {
        VersionSwitch(mVersions->GetRetail(mStartParams->mDefaultPlatform,mStartParams->mDefaultGame));
        mVersionDefault=mVersionCurrent;
    }
    mMouse_Button_Left_Toggle = 0;
    mMouse_EventLastButtonsPressed = 0;
    mKeyCode = 0;
    mKeyCodeAscii = 0;
    mInput_LastKey = 0;
    return applied;
}
