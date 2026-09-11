"""GIF export preserves decoded frames, timing, resolution and failure cleanup."""

from copy import deepcopy
from math import isnan

import matplotlib
import matplotlib.pyplot as plt
import pytest
from matplotlib.animation import FuncAnimation, PillowWriter
from matplotlib.patches import Rectangle
from PIL import Image, ImageSequence

from event_universe.diagnostics.frames import VolumeFrame
from event_universe.diagnostics.render import _save_animation_html, render_volume


def _figure(transparent=False):
    fig = plt.figure(figsize=(2, 1.5), facecolor="#080f1c")
    if transparent:
        fig.patch.set_alpha(0)
    ax = fig.add_axes((0, 0, 1, 1))
    ax.set_axis_off()
    square = ax.add_patch(Rectangle((0.1, 0.2), 0.25, 0.4, facecolor="#ffd166"))

    def draw(index):
        square.set_x(0.1 + 0.2 * index)
        square.set_facecolor(("#ffd166", "#4cc9ff", "#74ffac")[index])
        return (square,)

    return fig, draw


def _decoded_frames(path):
    with Image.open(path) as animation:
        return (
            [
                (frame.convert("RGBA").tobytes(), frame.info["duration"])
                for frame in ImageSequence.Iterator(animation)
            ],
            animation.size,
            dict(animation.info),
        )


@pytest.mark.parametrize("compact,dpi", [(False, 150), (True, 65)])
@pytest.mark.parametrize(
    "save_settings,transparent",
    [
        ({}, False),
        ({}, True),
        ({"savefig.transparent": True}, False),
        ({"savefig.facecolor": "#f0f0ee", "savefig.edgecolor": "red"}, False),
    ],
)
def test_export_matches_existing_pillow_pixels_and_frame_timing(
    tmp_path, compact, dpi, save_settings, transparent
):
    with matplotlib.rc_context(save_settings):
        _compare_exports(tmp_path, compact, dpi, transparent)


def _compare_exports(tmp_path, compact, dpi, transparent):
    reference = tmp_path / "reference.gif"
    fig, draw = _figure(transparent)
    try:
        animation = FuncAnimation(fig, draw, frames=3, interval=120)
        animation.save(reference, writer=PillowWriter(fps=8), dpi=dpi)
    finally:
        plt.close(fig)
    # Preserve the previous public Pillow export and no-repeat conversion as an oracle.
    with Image.open(reference) as animation_file:
        images = [frame.copy() for frame in ImageSequence.Iterator(animation_file)]
    durations = [frame.info["duration"] for frame in images]
    for frame in images:
        frame.info.pop("loop", None)
    images[0].save(reference, save_all=True, append_images=images[1:], duration=durations)

    fig, draw = _figure(transparent)
    output = tmp_path / "actual.html"
    _save_animation_html(
        fig,
        draw,
        3,
        (0, 2),
        "Synthetic snapshots",
        output,
        title="Export comparison",
        compact=compact,
        dpi=150,
    )
    actual, size, info = _decoded_frames(output.with_suffix(".gif"))
    expected, expected_size, _ = _decoded_frames(reference)
    assert actual == expected
    assert len(actual) == 3
    assert size == expected_size == (int(2 * dpi), int(1.5 * dpi))
    assert all(duration == 120 for _, duration in actual)
    assert "loop" not in info
    assert "data:image/gif;base64," in output.read_text()


def test_single_volume_snapshot_preserves_resolution_and_recorded_state(tmp_path):
    frames = [VolumeFrame(7, {(1, 2, 3): 5}, [(0, 1, 2, 3, 1, 0, 0)], (1, 0, 0), 12)]
    recorded = deepcopy(frames)
    output = render_volume(frames, tmp_path / "single.html", title="Single snapshot")
    with Image.open(output.with_suffix(".gif")) as animation:
        assert animation.size == (1500, 1275)
        assert animation.n_frames == 1
        assert animation.info["duration"] == 120
        assert "loop" not in animation.info
    assert frames == recorded


def test_drawing_failure_closes_figure_and_preserves_original_error(tmp_path):
    fig = plt.figure()

    def draw(index):
        raise RuntimeError("synthetic drawing failure")

    with pytest.raises(RuntimeError, match="synthetic drawing failure"):
        _save_animation_html(
            fig, draw, 1, (0, 0), "Synthetic snapshots", tmp_path / "failed.html", title="Failure"
        )
    assert not plt.fignum_exists(fig.number)
    assert not (tmp_path / "failed.html").exists()


def test_volume_paths_preserve_gaps_jumps_restarts_and_camera(monkeypatch, tmp_path):
    frames = [
        VolumeFrame(0, {}, [], (0, 0, 0), shape=(8, 8, 8)),
        VolumeFrame(1, {}, [(0, 7, 2, 3, 1, 0, 0)], (1, 0, 0), shape=(8, 8, 8)),
        VolumeFrame(2, {}, [], (0, 0, 0), shape=(8, 8, 8)),
        VolumeFrame(3, {}, [(0, 1, 2, 3, 1, 0, 0)], (1, 0, 0), shape=(8, 8, 8)),
        VolumeFrame(4, {}, [(0, 2, 2, 3, 1, 0, 0)], (1, 0, 0), shape=(16, 8, 8)),
    ]
    recorded = deepcopy(frames)

    def inspect(fig, draw, frame_count, ticks, plane_label, html_path, **kwargs):
        ax, compass = fig.axes
        try:
            for index in (0, 1, 2, 3, 4, 1, 4):
                draw(index)
                assert ax.azim == compass.azim == -65 + 35 * index / 4
                assert ax.elev == compass.elev == 26
                trails = [line for line in ax.lines if line.get_linewidth() == 1.8]
                if index in (0, 2):
                    assert trails == []
                else:
                    assert len(trails) == 1
                    xs, ys, zs = trails[0].get_data_3d()
                    if index == 1:
                        assert list(zip(xs, ys, zs, strict=True)) == [(7, 2, 3)]
                    else:
                        assert (xs[0], ys[0], zs[0]) == (7, 2, 3)
                        assert all(isnan(values[1]) for values in (xs, ys, zs))
                        assert (xs[2], ys[2], zs[2]) == (1, 2, 3)
                        if index == 4:
                            assert (xs[3], ys[3], zs[3]) == (2, 2, 3)
        finally:
            plt.close(fig)
        return html_path

    monkeypatch.setattr("event_universe.diagnostics.render._save_animation_html", inspect)
    render_volume(frames, tmp_path / "paths.html", title="Synthetic paths")
    assert frames == recorded
