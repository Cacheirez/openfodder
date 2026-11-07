/*
 * Optional, read-only gameplay trace for modernization regression testing.
 * GPL-3.0-or-later. Enabled only by OPENFODDER_TRACE_DIR.
 */
#include "stdafx.hpp"
#include <cstdlib>
#include <cctype>

namespace {
std::string traceSafeName(const std::string& name) {
    std::string result;
    for (unsigned char ch : name)
        result.push_back((std::isalnum(ch) || ch == '-' || ch == '_') ? char(ch) : '_');
    return result.empty() ? "unknown" : result;
}
std::string traceJsonString(const std::string& name) {
    std::string result = "\"";
    const char *hex = "0123456789abcdef";
    for (unsigned char ch : name) {
        if (ch == '\"' || ch == '\\') { result.push_back('\\'); result.push_back(char(ch)); }
        else if (ch < 32) {
            result += "\\u00"; result.push_back(hex[ch >> 4]); result.push_back(hex[ch & 15]);
        } else result.push_back(char(ch));
    }
    return result + "\"";
}
const char* traceBool(bool value) { return value ? "true" : "false"; }

struct TraceWriter {
    std::ofstream output;
    std::string key;
    unsigned long long sequence = 0;
};
}

void cFodder::GameplayTraceCapture() {
    const char* directory = std::getenv("OPENFODDER_TRACE_DIR");
    if (!directory || !*directory || !mStartParams || !mStartParams->mUnitTesting)
        return; // No effect during normal gameplay.

    static TraceWriter writer; // Only called from the Phase_Cycle game thread.
    const std::string campaign = mStartParams->mCampaignName;
    const std::string phaseKey = campaign + ":"
        + std::to_string(mGame_Data.mMission_Number) + ":"
        + std::to_string(mGame_Data.mMission_Phase);
    if (writer.key != phaseKey) {
        writer.output.close();
        writer.key = phaseKey;
        writer.sequence = 0;
        const std::string file = std::string(directory) + "/" + traceSafeName(campaign)
            + "_m" + std::to_string(mGame_Data.mMission_Number)
            + "_p" + std::to_string(mGame_Data.mMission_Phase) + ".jsonl";
        writer.output.open(file.c_str(), std::ios::out | std::ios::trunc);
        if (!writer.output) {
            std::cerr << "Gameplay trace could not open: " << file << std::endl;
            return;
        }
        const char *replayHash = std::getenv("OPENFODDER_TRACE_REPLAY_SHA256");
        const char *settingsHash = std::getenv("OPENFODDER_TRACE_SETTINGS_SHA256");
#ifdef _WIN32
        const char *hostPlatform = "Windows-x64";
#elif defined(__linux__)
        const char *hostPlatform = "Linux-x64";
#else
        const char *hostPlatform = "Other";
#endif
        writer.output << "{\"kind\":\"meta\",\"schema_version\":1,\"campaign\":"
            << traceJsonString(campaign)
            << ",\"mission\":" << mGame_Data.mMission_Number
            << ",\"phase\":" << mGame_Data.mMission_Phase
            << ",\"platform\":" << traceJsonString(hostPlatform)
            << ",\"resource_platform\":" << traceJsonString(mVersionCurrent && mVersionCurrent->isAmiga() ? "Amiga" : "PC")
            << ",\"replay_sha256\":" << traceJsonString(replayHash ? replayHash : "unverified")
            << ",\"settings_sha256\":" << traceJsonString(settingsHash ? settingsHash : "unverified")
            << ",\"seed\":[";
        for (int i = 0; i < 4; ++i) {
            if (i) writer.output << ',';
            writer.output << mGame_Data.mDemoRecorded.mSeed[i];
        }
        writer.output << "],\"sampling_point\":\"post-phase-cycle\"}\n";
    }
    if (!writer.output)
        return;

    int16 r0 = 0, r1 = 0, r2 = 0, r3 = 0;
    mRandom.getSeeds(r0, r1, r2, r3); // Read only; never consumes RNG.
    const auto& game = mGame_Data;
    const auto& phase = game.mGamePhase_Data;

    writer.output << "{\"kind\":\"tick\",\"tick\":" << writer.sequence++
        << ",\"state\":{\"game\":{\"mission\":" << game.mMission_Number
        << ",\"phase\":" << game.mMission_Phase
        << ",\"engine_ticks\":" << mMission_EngineTicks
        << ",\"demo_tick\":" << game.mDemoRecorded.mTick
        << ",\"phase_complete\":" << traceBool(phase.mIsComplete)
        << ",\"phase_won\":" << traceBool(mPhase_Complete)
        << ",\"phase_aborted\":" << traceBool(mPhase_Aborted)
        << ",\"kills_home\":" << game.mScore_Kills_Home
        << ",\"kills_away\":" << game.mScore_Kills_Away
        << ",\"recruits_available\":" << game.mRecruits_Available_Count
        << ",\"final_time_remaining\":" << mMission_Final_TimeRemain
        << ",\"completion_timer\":" << mPhase_Completed_Timer
        << ",\"squad_select_timer\":" << mSquad_Select_Timer
        << ",\"squad_fire_cooldown\":" << mSquad_Member_Fire_CoolDown
        << ",\"map_destroy_countdown\":" << mMap_Destroy_Tiles_Countdown
        << ",\"map_destroy_queue\":[";
    for (size_t i = 0; i < mMap_Destroy_Tiles.size(); ++i) {
        if (i) writer.output << ',';
        writer.output << '[' << mMap_Destroy_Tiles[i].mX << ','
                      << mMap_Destroy_Tiles[i].mY << ']';
    }
    writer.output << "],\"goals_remaining\":[";
    for (int i = 0; i < 10; ++i) {
        if (i) writer.output << ',';
        writer.output << traceBool(phase.mGoals_Remaining[i]);
    }
    writer.output << "],\"grenades\":[";
    for (int i = 0; i < 3; ++i) { if (i) writer.output << ','; writer.output << mSquad_Grenades[i]; }
    writer.output << "],\"rockets\":[";
    for (int i = 0; i < 3; ++i) { if (i) writer.output << ','; writer.output << mSquad_Rockets[i]; }
    writer.output << "],\"squad_weapons\":[";
    for (int i = 0; i < 3; ++i) { if (i) writer.output << ','; writer.output << mSquad_CurrentWeapon[i]; }
    writer.output << "],\"walk_target_steps\":[";
    for (int i = 0; i < 3; ++i) { if (i) writer.output << ','; writer.output << mSquad_Walk_Target_Steps[i]; }
    writer.output << "],\"vehicle_enter_timers\":[";
    for (int i = 0; i < 3; ++i) { if (i) writer.output << ','; writer.output << mSquad_EnteredVehicleTimer[i]; }
    writer.output << "],\"troops\":[";
    for (int i = 0; i < 9; ++i) {
        if (i) writer.output << ',';
        const sMission_Troop& troop = game.mSoldiers_Allocated[i];
        writer.output << "{\"id\":" << troop.mRecruitID
            << ",\"rank\":" << int(troop.mRank)
            << ",\"selected\":" << int(troop.mSelected)
            << ",\"kills\":" << troop.mNumberOfKills
            << ",\"phase_count\":" << int(troop.mPhaseCount) << "}";
    }
    writer.output << "]},\"controls\":{\"squad_selected\":" << mSquad_Selected
        << ",\"mouse_x\":" << mMouseX
        << ",\"mouse_y\":" << mMouseY
        << ",\"buttons\":" << mMouseButtonStatus
        << ",\"camera_x\":" << mCameraX
        << ",\"camera_y\":" << mCameraY
        << ",\"map_target_x\":" << mMapTile_TargetX
        << ",\"map_target_y\":" << mMapTile_TargetY
        << "},\"rng\":{\"seed\":[" << r0 << ',' << r1 << ',' << r2 << ',' << r3
        << "]},\"sprites\":[";
    bool first = true;
    for (size_t slot = 0; slot < mSprites.size(); ++slot) {
        const sSprite& s = mSprites[slot];
        if (s.mPosX == -32768)
            continue;
        if (!first) writer.output << ',';
        first = false;
        writer.output << "{\"slot\":" << slot
            << ",\"type\":" << s.mSpriteType
            << ",\"x\":" << s.mPosX
            << ",\"x_frac\":" << s.mPosXFrac
            << ",\"y\":" << s.mPosY
            << ",\"y_frac\":" << s.mPosYFrac
            << ",\"direction\":" << s.mDirection
            << ",\"face_direction\":" << s.mFaceDirection
            << ",\"anim_state\":" << s.mAnimState
            << ",\"frame\":" << s.mFrameIndex
            << ",\"pending_destroy\":" << s.mPendingDestroy
            << ",\"weapon_fire_timer\":" << s.mWeaponFireTimer
            << ",\"weapon_cooldown\":" << int(s.mWeaponCooldown)
            << ",\"action_cooldown\":" << int(s.mActionCooldown)
            << ",\"ai_aggression\":" << s.mAIAggression
            << ",\"target_x\":" << s.mTargetX
            << ",\"target_y\":" << s.mTargetY
            << ",\"was_drawn\":" << int(s.mWasDrawn)
            << ",\"in_water\":" << int(s.mInWater)
            << ",\"terrain_type\":" << int(s.mTerrainType)
            << ",\"person_type\":" << s.mPersonType
            << ",\"draw_order\":" << s.mDrawOrder
            << ",\"in_vehicle\":" << int(s.mInVehicle)
            << ",\"sinking\":" << int(s.mIsSinking)
            << ",\"vehicle_enabled\":" << int(s.mVehicleEnabled)
            << ",\"fired_weapon_type\":" << int(s.mFiredWeaponType)
            << ",\"weapon_anim_tick\":" << int(s.mWeaponAnimTick)
            << ",\"has_shadow\":" << int(s.mHasShadow)
            << ",\"rows_to_skip\":" << s.mRowsToSkip
            << "}";
    }
    writer.output << "]}}\n";
}
