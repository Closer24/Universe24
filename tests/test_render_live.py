"""Live rasters reuse the canonical renderer without changing exported snapshots."""

from copy import deepcopy

import matplotlib
import matplotlib.pyplot as plt
import pytest
from PIL import Image

from event_universe.diagnostics.frames import Frame, Slice, VolumeFrame
from event_universe.diagnostics.render import (
    render_run,
    render_run_preview,
    render_volume,
    render_volume_preview,
)


def _frames(volume):
    if volume:
        return [
            VolumeFrame(
                tick,
                {(2, 3, 4): tick + 1},
                [(0, tick + 2, 3, 4, 1, 0, 0)],
                (1, 0, 0),
                c_units=12,
                shape=(16, 12, 8),
            )
            for tick in (0, 1)
        ]
    return [Frame(tick, {(2, 3): tick + 1}, [(0, tick + 2, 3, 1, 0, 0)], (1, 0, 0)) for tick in (0, 1)]


@pytest.mark.visualization
@pytest.mark.parametrize("volume", [False, True])
@pytest.mark.parametrize("save_settings", [{}, {"savefig.transparent": True}, {"savefig.bbox": "tight"}])
def test_preview_matches_last_canonical_raster_and_callback_precedes_gif(
    tmp_path, volume, save_settings
):
    frames = _frames(volume)
    recorded = deepcopy(frames)
    output = tmp_path / "complete.html"
    preview = tmp_path / "preview" / "latest.png"
    observed = []

    def receive(index, image):
        assert not output.exists()
        assert not output.with_suffix(".gif").exists()
        observed.append((index, image))

    with matplotlib.rc_context(save_settings):
        if volume:
            render_volume(frames, output, title="Canonical sequence", on_frame=receive)
            render_volume_preview(frames, preview)
        else:
            render_run(frames, Slice(), output, title="Canonical sequence", on_frame=receive)
            render_run_preview(frames, Slice(), preview)
    assert [index for index, _ in observed] == [0, 1]
    assert observed[0][1].tobytes() != observed[1][1].tobytes()
    with Image.open(preview) as image:
        assert image.format == "PNG"
        assert image.size == ((1500, 1275) if volume else (900, 550))
        assert image.convert("RGBA").tobytes() == observed[-1][1].convert("RGBA").tobytes()
    assert list(preview.parent.iterdir()) == [preview]
    assert frames == recorded


@pytest.mark.visualization
def test_callback_image_mutation_cannot_change_canonical_gif(tmp_path):
    frames = _frames(False)
    normal = tmp_path / "normal.html"
    observed = tmp_path / "observed.html"
    render_run(frames, Slice(), normal, title="Unobserved export")

    def paint_black(index, image):
        image.paste("black", (0, 0, image.width, image.height))

    render_run(frames, Slice(), observed, title="Observed export", on_frame=paint_black)
    assert normal.with_suffix(".gif").read_bytes() == observed.with_suffix(".gif").read_bytes()


@pytest.mark.parametrize("volume", [False, True])
def test_preview_rejects_empty_history_without_creating_an_artifact(tmp_path, volume):
    output = tmp_path / "empty.png"
    figures_before = plt.get_fignums()
    with pytest.raises(ValueError, match="at least one diagnostic frame"):
        if volume:
            render_volume_preview([], output)
        else:
            render_run_preview([], Slice(), output)
    assert not output.exists()
    assert plt.get_fignums() == figures_before


@pytest.mark.visualization
def test_preview_and_callback_failures_close_their_figures(tmp_path):
    frames = _frames(False)
    figures_before = plt.get_fignums()
    blocked = tmp_path / "blocked"
    blocked.write_text("This file cannot be a preview directory.")
    with pytest.raises(FileExistsError):
        render_run_preview(frames, Slice(), blocked / "latest.png")
    assert plt.get_fignums() == figures_before

    def fail(index, image):
        raise OSError("preview callback failed")

    output = tmp_path / "failed.html"
    with pytest.raises(OSError, match="preview callback failed"):
        render_run(frames, Slice(), output, title="Failed callback", on_frame=fail)
    assert not output.exists()
    assert plt.get_fignums() == figures_before
