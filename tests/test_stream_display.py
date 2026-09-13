"""Stream intensity is a copied, explicitly named diagnostic, never scalar phi."""

from copy import deepcopy

import pytest

from event_universe import Config
from event_universe.core.streaming_engine import StreamingEngine
from event_universe.core.streams import ZERO_OCTANTS, StreamNodeState
from event_universe.diagnostics.frames import Slice, capture_frame, capture_volume
from event_universe.models.scalar_field import update_particle


@pytest.fixture
def stream_world():
    world = StreamingEngine(
        Config(nx=8, ny=8, nz=8),
        update_particle,
        lambda *args: (ZERO_OCTANTS,) * 6,
        0,
        lambda values: values,
    )
    # Fixed diagnostic fixture, with nonzero flux deliberately distinct from intensity.
    world.streams._nodes.update(
        {
            (2, 3, 4): StreamNodeState((1, 2, 3, 4, 5, 6, 7, 8), (99, 0, 0, 0, 0, 0)),
            (6, 7, 5): StreamNodeState((0, 0, 0, 0, 0, 0, 0, 9)),
            (1, 1, 4): StreamNodeState(),
        }
    )
    return world


def test_stream_projection_copies_population_sums_and_never_materializes_nodes(stream_world):
    before = dict(stream_world.streams.nodes)
    volume = capture_volume(stream_world)
    plane = capture_frame(stream_world, Slice("XY", 4))
    assert volume.field == {(2, 3, 4): 36, (6, 7, 5): 9}
    assert plane.field == {(2, 3): 36}
    assert volume.field_kind == plane.field_kind == "stream-magnitude"
    volume.field[(2, 3, 4)] = 1000
    plane.field.clear()
    assert dict(stream_world.streams.nodes) == before
    assert dict(stream_world.nodes) == {}


@pytest.mark.visualization
@pytest.mark.parametrize("volume", [False, True])
def test_stream_output_names_its_quantity_in_image_and_html(tmp_path, stream_world, volume):
    from unittest.mock import patch

    from PIL import Image

    import event_universe.diagnostics.render as renderer
    from event_universe.diagnostics.render import render_run, render_volume

    path = tmp_path / "streams.html"
    frame = capture_volume(stream_world) if volume else capture_frame(stream_world, Slice("XY", 4))
    before = deepcopy(frame)
    original = renderer._save_animation_html

    def inspect(fig, draw, *args, **kwargs):
        draw(0)
        text = " ".join(
            [item.get_text() for item in fig.texts] + [axis.get_title() for axis in fig.axes]
        )
        assert "Stream magnitude = sum populations (not scalar phi)" in text
        return original(fig, draw, *args, **kwargs)

    with patch.object(renderer, "_save_animation_html", side_effect=inspect):
        if volume:
            render_volume([frame], path, title="Stream intensity")
        else:
            render_run([frame], Slice("XY", 4), path, title="Stream intensity")
    assert "not scalar phi" in path.read_text()
    assert frame == before
    with Image.open(path.with_suffix(".gif")) as gif:
        assert "loop" not in gif.info
        if volume:
            assert gif.size == (1500, 1275)


@pytest.mark.parametrize("volume", [False, True])
def test_one_animation_cannot_mix_stream_and_scalar_quantities(tmp_path, stream_world, volume):
    from event_universe.diagnostics.render import render_run, render_volume

    stream = capture_volume(stream_world) if volume else capture_frame(stream_world, Slice())
    scalar = deepcopy(stream)
    scalar.field_kind = "scalar"
    with pytest.raises(ValueError, match="one field quantity"):
        if volume:
            render_volume([scalar, stream], tmp_path / "mixed.html", title="Mixed")
        else:
            render_run([scalar, stream], Slice(), tmp_path / "mixed.html", title="Mixed")
