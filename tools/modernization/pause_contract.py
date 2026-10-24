"""The sole approved pause-loop replacement; all surrounding effects stay guarded."""
OLD = '''        // Draw background with faded palette, then overlay text using its own palette.
        mSurface->draw();
        mSurface2->draw();
        mSurface->mergeSurfaceBuffer(mSurface2);'''
NEW = '''        // Capture after the original fade step. Replaying this scene cannot
        // advance fades, consume input or select resources.
        const openfodder::PausePresentation scene{
            mSurface->CapturePresentation(), mSurface2->CapturePresentation()
        };
        const auto presented = openfodder::RasterizePausePresentation(scene);
        mSurface->ApplyPresentation(presented.background);
        mSurface2->ApplyPresentation(presented.text);'''
def canonical_pause(source):
    assert source.count(NEW) == 1, 'Pause presentation block changed; update its equivalence test'
    return source.replace(NEW, OLD)
