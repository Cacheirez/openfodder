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
#include <chrono>
#include <cstdlib>
#include <stdexcept>

void cUnitTesting::ProbeMissionPause() {
    auto& game = *g_Fodder;
    if (!game.mStartParams->mUnitTesting || !game.mStartParams->mDemoPlayback ||
        game.mStartParams->mDemoRecord || game.mStartParams->mDisableVideo)
        return;
    const char* enabled = std::getenv("OPENFODDER_TEST_MISSION_PAUSE");
    if (!enabled || std::string(enabled) != "1") return;

    // The replay caller owns mSurfaceMtx throughout. No worker can advance
    // producers while this bounded SDL-input probe borrows the pause loop.
    static std::string previous;
    static bool awaitingResume = false;
    if (awaitingResume) {
        if (game.mPhase_Paused || !game.mSurface->MissionAuditActive())
            throw std::runtime_error("pause probe: mission recording did not resume");
        game.mSurface->VerifyMissionAudit(game.mSurfaceFinal);
        std::fprintf(stderr, "MISSION_PAUSE_PROBE: resumed %s\n", previous.c_str());
        awaitingResume = false;
    }
    if (!game.mPhase_In_Progress || game.mPhase_Paused || game.mPhase_ShowMapOverview) return;
    // Saved replays may start with a nonzero engine clock. Schedule this test
    // by eligible replay steps within each phase; never reset the game clock.
    static std::string phase;
    static unsigned steps = 0;
    const std::string currentPhase = game.mStartParams->mCampaignName + ":" +
        std::to_string(game.mGame_Data.mMission_Number) + ":" +
        std::to_string(game.mGame_Data.mMission_Phase);
    if (phase != currentPhase) { phase = currentPhase; steps = 0; }
    if (steps < 17) ++steps;
    if (steps != 8 && steps != 16) return;
    const std::string key = currentPhase + ":" + std::to_string(steps);
    if (previous == key) return;
    previous = key;
    if (!game.mSurface->MissionAuditActive())
        throw std::runtime_error("pause probe: missing pre-pause recording");
    game.mSurface->VerifyMissionAudit(game.mSurfaceFinal);
    const auto demoTick = game.mGame_Data.mDemoRecorded.mTick;
    const auto engineTick = game.mMission_EngineTicks;
    int16 r0, r1, r2, r3, s0, s1, s2, s3;
    game.mRandom.getSeeds(r0, r1, r2, r3);
    auto pressP = []() {
        for (auto type : {SDL_EVENT_KEY_DOWN, SDL_EVENT_KEY_UP}) {
            SDL_Event event{};
            event.type = type;
            event.key.scancode = SDL_SCANCODE_P;
            event.key.down = type == SDL_EVENT_KEY_DOWN;
            if (!SDL_PushEvent(&event))
                throw std::runtime_error("pause probe: SDL rejected key event");
        }
    };
    // Route input through SDL and eventsProcess, not a direct pause flag write.
    // Restore replay input even if a strict check fails. Production flags and
    // the demo's recorded events are not edited.
    struct RestorePlayback {
        bool& target; bool value;
        ~RestorePlayback() { target = value; }
    } restore{game.mParams->mDemoPlayback, game.mParams->mDemoPlayback};
    game.mParams->mDemoPlayback = false;
    pressP();
    game.mWindow->Cycle();
    game.eventsProcess();
    if (!game.mPhase_Paused)
        throw std::runtime_error("pause probe: SDL did not enter pause");
    pressP(); // Consumed after the first real pause frame, without a helper thread.
    game.Phase_Paused();
    game.mRandom.getSeeds(s0, s1, s2, s3);
    if (game.mPhase_Paused || game.mSurface->MissionAuditActive() ||
        game.mSurfaceFinal->MissionAuditActive() ||
        demoTick != game.mGame_Data.mDemoRecorded.mTick || engineTick != game.mMission_EngineTicks ||
        r0 != s0 || r1 != s1 || r2 != s2 || r3 != s3)
        throw std::runtime_error("pause probe: pause changed clocks/RNG or retained a stale recording");
    std::fprintf(stderr, "MISSION_PAUSE_PROBE: completed %s\n", key.c_str());
    awaitingResume = true;
}

cUnitTesting::cUnitTesting() {

    g_Fodder->mStartParams->mSinglePhase = true;
    g_Fodder->mStartParams->mSkipBriefing = true;
    g_Fodder->mStartParams->mSkipIntro = true;
    g_Fodder->mStartParams->mSkipService = true;
    g_Fodder->mStartParams->mSkipRecruit = true;

    if (!g_Fodder->mStartParams->mDemoRecord)
        g_Fodder->mStartParams->mDemoPlayback = true;
}

std::string cUnitTesting::getCurrentTestFileName() {
    std::string MissionPhase = "";
    MissionPhase += "m" + std::to_string(g_Fodder->mGame_Data.mMission_Number);
    MissionPhase += "p" + std::to_string(g_Fodder->mGame_Data.mMission_Phase);
    return MissionPhase;
}

std::string cUnitTesting::getCurrentTestName() {
    std::string MissionTitle = "Mission " + std::to_string(g_Fodder->mGame_Data.mMission_Number);
    MissionTitle += " Phase " + std::to_string(g_Fodder->mGame_Data.mMission_Phase);
    MissionTitle += ": " + g_Fodder->mGame_Data.mMission_Current->mName;
    if(g_Fodder->mGame_Data.mPhase_Current->mName != g_Fodder->mGame_Data.mMission_Current->mName)
        MissionTitle += " (" + g_Fodder->mGame_Data.mPhase_Current->mName + ")";
    return MissionTitle;

}
void cUnitTesting::EngineSetup() {
    g_Fodder->mIntroDone = false;

    g_Fodder->mSurface->palette_SetToBlack();
    g_Fodder->mSurface->paletteNew_SetToBlack();
    g_Fodder->mSurface->surfaceSetToPalette();
    g_Fodder->mSurface->resetPaletteAdjusting();

    g_Fodder->mPhase_TryingAgain = false;
    g_Fodder->Mouse_Setup();
}

void cUnitTesting::setDemoName() {
    // Set demo file name
    g_Fodder->mStartParams->mDemoFile = g_ResourceMan->GetTestPath(g_Fodder->mVersionCurrent, g_Fodder->mStartParams->mCampaignName) + "/" + getCurrentTestFileName();
    if (!g_ResourceMan->FileExists(g_Fodder->mStartParams->mDemoFile + ".ofd")) {

        bool AmigaExists = g_ResourceMan->FileExists(g_Fodder->mStartParams->mDemoFile + "-amiga.ofd");
        bool PcExists = g_ResourceMan->FileExists(g_Fodder->mStartParams->mDemoFile + "-pc.ofd");

        // If we a PC or Amiga specific test exists, then use it as the name
        if (AmigaExists || PcExists) {

            if (g_Fodder->mVersionCurrent->isAmiga()) {
                g_Fodder->mStartParams->mDemoFile += "-amiga";
            } else {
                g_Fodder->mStartParams->mDemoFile += "-pc";
            }
        }
    }

    g_Fodder->mStartParams->mDemoFile += ".ofd";
}

bool cUnitTesting::RunTests(const std::string pCampaign) {
    bool Retry = false;
    g_Fodder->Game_Setup();

	if (g_Fodder->mStartParams->mUnitTesting && g_Fodder->mStartParams->mDemoPlayback) {
		//g_Fodder->mStartParams->mSleepDelta = 0;
		g_Fodder->SetInterruptSleepDelta(0);
	}

    // Explicit bounded diagnostic scope; normal test suites still run every phase.
    const char* firstPhase = std::getenv("OPENFODDER_TEST_FIRST_PHASE");
    const bool firstPhaseOnly = firstPhase && std::string(firstPhase) == "1" &&
        !g_Fodder->mStartParams->mDemoRecord;
    while (g_Fodder->mGame_Data.mMission_Current) {
        EngineSetup();
        setDemoName();

        std::string MissionTitle = getCurrentTestName();

        if (g_Fodder->mStartParams->mDemoRecord && !Retry) {
            if (g_ResourceMan->FileExists(g_Fodder->mStartParams->mDemoFile)) {
                g_Debugger->Notice("Test exists for " + MissionTitle + ", skipping");
                g_Fodder->mGame_Data.Phase_Next();
                continue;
            }
        }

        Retry = false;
        g_Debugger->TestStart(MissionTitle, g_Fodder->mStartParams->mCampaignName);

        if (g_Fodder->mStartParams->mDemoPlayback) {
            if (!g_Fodder->mStartParams->mDemoRecord) {
                if (!g_Fodder->Demo_Load()) {
                    g_Debugger->TestComplete(MissionTitle, g_Fodder->mStartParams->mCampaignName, "No test found", 0, eTest_Skipped);
                    g_Fodder->mGame_Data.Phase_Next();
                    continue;
                }
            }

            g_Fodder->mGame_Data.mDemoRecorded.playback();
        }

        // If demo is recording
        if (g_Fodder->mStartParams->mDemoRecord) {
            // And we have a resume cycle set
            if (g_Fodder->mStartParams->mDemoRecordResumeCycle) {
                g_Debugger->Notice("Resuming " + MissionTitle);
                g_Fodder->SetInterruptSleepDelta(0);
            }
            else {
                g_Fodder->mGame_Data.mDemoRecorded.clear();
                g_Debugger->Notice("Recording " + MissionTitle);
            }
        }

        // Reset demo status
        {
            std::lock_guard<std::mutex> lock(g_Fodder->mSurfaceMtx);
            g_Fodder->mParams->mDemoFile = g_Fodder->mStartParams->mDemoFile;
            g_Fodder->mParams->mDemoRecord = g_Fodder->mStartParams->mDemoRecord;
            g_Fodder->mParams->mDemoPlayback = g_Fodder->mStartParams->mDemoPlayback;
            g_Fodder->mParams->mAppVeyor = g_Fodder->mStartParams->mAppVeyor;
        }
        // Keep game state
        g_Fodder->mGame_Data_Backup = g_Fodder->mGame_Data;

        // Run the phase
        
        auto missionStartTime = std::chrono::steady_clock::now();
        g_Fodder->Mission_Loop();
        auto missionDuration = std::chrono::duration_cast<std::chrono::milliseconds>(std::chrono::steady_clock::now() - missionStartTime);

        // If recording
        if (g_Fodder->mStartParams->mDemoRecord) {
            if (g_Fodder->mPhase_Complete) {
                g_Fodder->mGame_Data.mDemoRecorded.save();
            } else {

                Retry = true;
                // If the phase was aborted (ESC key), don't replay it.. start over
                if (!g_Fodder->mPhase_EscapeKeyAbort) {

                    // Less than 200 cycles, player can start over
                    if (g_Fodder->mGame_Data.mDemoRecorded.mTick > 200) {
                        g_Fodder->mStartParams->mDemoRecordResumeCycle = (g_Fodder->mGame_Data.mDemoRecorded.mTick - 200);
                        g_Fodder->mStartParams->mDemoPlayback = true;
                        
                        // Delete events occruing after resume cycle
                        g_Fodder->mGame_Data.mDemoRecorded.removeFrom(g_Fodder->mStartParams->mDemoRecordResumeCycle);
                        g_Fodder->mGame_Data_Backup.mDemoRecorded = g_Fodder->mGame_Data.mDemoRecorded;
                        // Disable video output for speed
                        g_Fodder->mStartParams->mDisableVideo = true;
                        g_Fodder->mStartParams->mDisableSound = true;
                    }
                }
                // Reset game to before start of phase
                g_Fodder->mGame_Data = g_Fodder->mGame_Data_Backup;
                continue;
            }
        }

        if (!g_Fodder->mPhase_Complete) {
            g_Debugger->TestComplete(MissionTitle, g_Fodder->mStartParams->mCampaignName, "Phase Failed", (size_t)missionDuration.count(), eTest_Failed);
            return false;
        }

        g_Debugger->TestComplete(MissionTitle, g_Fodder->mStartParams->mCampaignName, "Phase Complete", (size_t)missionDuration.count(), eTest_Passed);

        g_Fodder->mGame_Data = g_Fodder->mGame_Data_Backup;
        g_Fodder->mGame_Data.Phase_Next();
        if (firstPhaseOnly) {
            g_Debugger->Notice("DIAGNOSTIC_SCOPE: first phase only; remaining campaign not executed");
            break;
        }
    }

    return true;
}

bool cUnitTesting::Start() {
    std::vector<std::string> Campaigns;

    // No Campaign Name
    if (!g_Fodder->mStartParams->mCampaignName.size())
        Campaigns = g_Fodder->mVersions->GetCampaignNames();
    else
        Campaigns.push_back(g_Fodder->mStartParams->mCampaignName);

    bool TotalResult = true;
    for (auto& CampaignName : Campaigns) {
        bool Result = true;

        if (CampaignName == "Random Map" || CampaignName == "Single Map")
            continue;

        {
            // Interrupt_Redraw consults mParams while holding mSurfaceMtx.
            // Replace the parameter snapshot under the same lock, and
            // publish the cadence atomically for Interrupt_Sim.
            std::lock_guard<std::mutex> lock(g_Fodder->mSurfaceMtx);
            *g_Fodder->mParams = *g_Fodder->mStartParams;
            g_Fodder->mInterruptSleepDelta.store(g_Fodder->mParams->mSleepDelta);
        }
        g_Fodder->mStartParams->mCampaignName = CampaignName;

        g_Debugger->TestStart(CampaignName, "Campaign");

        g_Fodder->mGame_Data.mCampaign.Clear();
        if (!g_Fodder->Campaign_Load(CampaignName)) {
            g_Debugger->Error("Campaign " + CampaignName + " not found");
            g_Debugger->TestComplete(CampaignName, "Campaign", "not found", 0, eTest_Skipped);
            continue;
        }

        // FIXME: Create test folder
        if (!g_ResourceMan->FileExists(g_ResourceMan->GetTestPath(g_Fodder->mVersionCurrent, "")) && g_Fodder->mStartParams->mDemoRecord) {

            std::string Command = "mkdir \"" + g_ResourceMan->GetTestPath(g_Fodder->mVersionCurrent, "") + "\"";
            system(Command.c_str());
        }

        auto campaignStartTime = std::chrono::steady_clock::now();
        if (!RunTests(CampaignName))
            Result = false;
        auto campaignDuration = std::chrono::duration_cast<std::chrono::milliseconds>(std::chrono::steady_clock::now() - campaignStartTime);

        g_Debugger->TestComplete(CampaignName, "Campaign", "", (size_t)campaignDuration.count(), Result ? eTest_Passed : eTest_Failed);

        if (!Result)
            TotalResult = false;
    }

    return TotalResult;
}
