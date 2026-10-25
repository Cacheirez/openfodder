"""Exact diagnostic-only hooks removed by legacy isolated fixtures.
check_mission_recording.py executes them and guards all original producer bodies.
"""
HOOKS = ['    target->RecordMissionSidebar(draw);\n',
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

def without_audit(source):
    source = source.replace(PUBLICATION, CLASSIC_PUBLICATION)
    for hook in HOOKS:
        source = source.replace(hook, "")
    return source
