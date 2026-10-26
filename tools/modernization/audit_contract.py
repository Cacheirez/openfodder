"""Exact diagnostic-only hooks removed by legacy isolated fixtures.
check_mission_recording.py executes them and guards all original producer bodies.
"""
HOOKS = ['                cUnitTesting::ProbeMissionPause();\n',
 '    target->RecordMissionSidebar(draw);\n',
 '    target->RecordMissionPixels(captured);\n',
 '    if (target->MissionAuditActive())\n'
 '        target->RecordMissionPixels(openfodder::CaptureSprite8Producer(draw, layout, '
 'output.width),\n'
 '            prepared.isCursor ? openfodder::MissionLayerRole::Cursor : '
 'openfodder::MissionLayerRole::Sprite);\n',
 '    mSurface->RecordMissionTerrain(terrain);\n',
 '    RecordMissionSurface(openfodder::MissionLayerOperation::Save);\n',
 '    RecordMissionSurface(openfodder::MissionLayerOperation::Restore);\n',
 '    RecordMissionSurface(openfodder::MissionLayerOperation::Clear, uint8(pColor));\n',
 '        mSurface->BeginMissionAudit(mSurfaceFinal, mPhase_In_Progress && !mPhase_Paused &&\n'
 '            !mPhase_ShowMapOverview && !mInterruptCallback && !mStartParams->mDisableVideo);\n',
 '        pSurface->VerifyMissionAudit(mSurfaceFinal);\n',
 '        mSurface->VerifyMissionAudit(mSurfaceFinal);\n',
 '    prepared.isCursor = true;\n',
 '    mSurface->BeginMissionAudit(mSurfaceFinal, false);\n']

PUBLICATION = '        if (!pSurface->PresentRecordedMission(mSurfaceFinal))\n        {\n            pSurface->VerifyMissionAudit(mSurfaceFinal);\n            const openfodder::MissionPresentation scene{pSurface->CapturePresentation()};\n            const auto presented = openfodder::RasterizeMissionPresentation(scene);\n            pSurface->ApplyPresentation(presented);\n        }'
CLASSIC_PUBLICATION = '        const openfodder::MissionPresentation scene{pSurface->CapturePresentation()};\n        const auto presented = openfodder::RasterizeMissionPresentation(scene);\n        pSurface->ApplyPresentation(presented);'

SCHEDULED_RENDER = 'void cFodder::Video_SurfaceRender(const bool pRestoreSurface, const bool pShrink, cSurface *pSurface, const bool pSkip)\n{\n\n    if (mStartParams->mDisableVideo)\n        return;\n\n    if (!pSurface)\n    {\n        pSurface = mSurface;\n    }\n\n    const bool missionPresentation = mPhase_In_Progress && !mPhase_Paused && !mPhase_ShowMapOverview &&\n        !mInterruptCallback && pSurface == mSurface && pSkip && !pShrink &&\n        !pSurface->isLoadedImage();\n    const int presentations = missionPresentation\n        ? cSurface::MissionPresentationRepeats(mStartParams->mUnitTesting) : 1;\n    // Omission skips conversion/upload/SDL presentation, never production or events.\n    // The oracle must still run at the late-palette point for a zero-frame test.\n    if (presentations == 0) pSurface->VerifyMissionAudit(mSurfaceFinal);\n    for (int presentation = 0; presentation < presentations; ++presentation)\n    {\n        if (missionPresentation)\n        {\n            // Capture at the old conversion point, not at Interrupt_Redraw: the\n            // main cycle can still change sprites and the effective palette.\n            // All producers, Save/Restore and their logical effects stay in place.\n            if (!pSurface->PresentRecordedMission(mSurfaceFinal))\n            {\n                pSurface->VerifyMissionAudit(mSurfaceFinal);\n                const openfodder::MissionPresentation scene{pSurface->CapturePresentation()};\n                const auto presented = openfodder::RasterizeMissionPresentation(scene);\n                pSurface->ApplyPresentation(presented);\n            }\n        }\n        else\n        {\n            pSurface->draw(pSkip == true ? 16 : 0, pSkip == true ? 16 : 0);\n        }\n        if (pShrink)\n        {\n            mWindow->RenderShrunk(pSurface);\n        }\n        else\n        {\n            mWindow->RenderAt(pSurface);\n        }\n        mWindow->FrameEnd();\n    }\n\n    // if(pRestoreSurface)\n    //     mSurfaceFinal->Restore();\n}'
SINGLE_RENDER = 'void cFodder::Video_SurfaceRender(const bool pRestoreSurface, const bool pShrink, cSurface *pSurface, const bool pSkip)\n{\n\n    if (mStartParams->mDisableVideo)\n        return;\n\n    if (!pSurface)\n    {\n        pSurface = mSurface;\n    }\n\n    if (mPhase_In_Progress && !mPhase_Paused && !mPhase_ShowMapOverview &&\n        !mInterruptCallback && pSurface == mSurface && pSkip && !pShrink &&\n        !pSurface->isLoadedImage())\n    {\n        // Capture at the old conversion point, not at Interrupt_Redraw: the\n        // main cycle can still change sprites and the effective palette.\n        // All producers, Save/Restore and their logical effects stay in place.\n        if (!pSurface->PresentRecordedMission(mSurfaceFinal))\n        {\n            pSurface->VerifyMissionAudit(mSurfaceFinal);\n            const openfodder::MissionPresentation scene{pSurface->CapturePresentation()};\n            const auto presented = openfodder::RasterizeMissionPresentation(scene);\n            pSurface->ApplyPresentation(presented);\n        }\n    }\n    else\n    {\n        pSurface->draw(pSkip == true ? 16 : 0, pSkip == true ? 16 : 0);\n    }\n    if (pShrink)\n    {\n        mWindow->RenderShrunk(pSurface);\n    }\n    else\n    {\n        mWindow->RenderAt(pSurface);\n    }\n    mWindow->FrameEnd();\n\n    // if(pRestoreSurface)\n    //     mSurfaceFinal->Restore();\n}'

def without_audit(source):
    source = source.replace(SCHEDULED_RENDER, SINGLE_RENDER)
    source = source.replace(PUBLICATION, CLASSIC_PUBLICATION)
    for hook in HOOKS:
        source = source.replace(hook, "")
    return source
