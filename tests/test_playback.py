import pytest

from event_universe.diagnostics.frames import Frame, Slice, VolumeFrame


@pytest.mark.visualization
@pytest.mark.parametrize("volume", [False, True])
def test_exported_animation_stops_at_final_frame(tmp_path, volume):
    from PIL import Image

    from event_universe.diagnostics.render import render_run, render_volume

    # Synthetic snapshots: no world runs or physical interpolation.
    output = tmp_path / "playback.html"
    if volume:
        frames = [VolumeFrame(t, {}, [(0, t, 0, 0, 1, 0, 0)], (1, 0, 0)) for t in (0, 1)]
        render_volume(frames, output, title="Playback contract")
    else:
        frames = [Frame(t, {}, [(0, t, 0, 1, 0, 0)], (1, 0, 0)) for t in (0, 1)]
        render_run(frames, Slice(), output, title="Playback contract")
    with Image.open(output.with_suffix(".gif")) as animation:
        assert animation.n_frames == 2
        assert "loop" not in animation.info  # No repeat extension, including finite repeats.
        first = animation.convert("RGB").tobytes()
        animation.seek(1)
        assert animation.convert("RGB").tobytes() != first
        assert animation.info["duration"] > 0
    assert "Playback stops at the final frame" in output.read_text()
