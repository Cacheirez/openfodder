"""Only the mission conversion block may change; producers stay guarded."""
OLD = '    pSurface->draw(pSkip == true ? 16 : 0, pSkip == true ? 16 : 0);'
NEW = '''    if (mPhase_In_Progress && !mPhase_Paused && !mPhase_ShowMapOverview &&
        !mInterruptCallback && pSurface == mSurface && pSkip && !pShrink &&
        !pSurface->isLoadedImage())
    {
        // Capture at the old conversion point, not at Interrupt_Redraw: the
        // main cycle can still change sprites and the effective palette.
        // All producers, Save/Restore and their logical effects stay in place.
        const openfodder::MissionPresentation scene{pSurface->CapturePresentation()};
        const auto presented = openfodder::RasterizeMissionPresentation(scene);
        pSurface->ApplyPresentation(presented);
    }
    else
    {
        pSurface->draw(pSkip == true ? 16 : 0, pSkip == true ? 16 : 0);
    }'''
def canonical_mission(source):
    assert source.count(NEW) == 1, 'Mission block changed; update its differential test'
    return source.replace(NEW, OLD)
