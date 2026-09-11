"""Exact local face diagnostics remain separate from aggregate field and velocity."""

import html
import json
import re
from copy import deepcopy
from types import MappingProxyType, SimpleNamespace
from unittest.mock import patch

import pytest
from PIL import Image

from event_universe import CellState, Config, ParticleState
from event_universe.diagnostics.frames import Slice, capture_frame, capture_volume
from event_universe.diagnostics.render import FACE_LABELS, render_run, render_volume


@pytest.fixture
def face_records():
    return SimpleNamespace(
        config=Config(nx=16, ny=16, nz=16),
        tick=1,
        cells=MappingProxyType({(4, 5, 6): CellState(9)}),
        particles=MappingProxyType({0: ParticleState(4, 5, 6, 3)}),
        field_faces=MappingProxyType({(4, 5, 6): (1, -2, 3, -4, 5, -6), (2, 3, 8): (8, 0, 0, 0, 0, 0)}),
    )


def test_capture_keeps_exact_signed_faces_separate_from_scalar_and_world(face_records):
    volume = capture_volume(face_records)
    plane = capture_frame(face_records, Slice("XY", 6))
    assert volume.field == {(4, 5, 6): 9}
    assert volume.field_kind == "scalar"
    assert volume.field_faces == dict(face_records.field_faces)
    assert plane.field_faces == {(4, 5, 6): (1, -2, 3, -4, 5, -6)}
    assert plane.faces_available and volume.faces_available
    volume.field_faces.clear()
    plane.field_faces[(4, 5, 6)] = (0, 0, 0, 0, 0, 0)
    assert face_records.field_faces[(4, 5, 6)] == (1, -2, 3, -4, 5, -6)
    assert face_records.cells[(4, 5, 6)] == CellState(9)


def test_sparse_faces_copy_zero_at_occupied_cell_without_creating_physical_record(face_records):
    face_records.field_faces = MappingProxyType({})
    frame = capture_volume(face_records)
    assert frame.faces_available
    assert frame.field_faces == {(4, 5, 6): (0, 0, 0, 0, 0, 0)}
    assert dict(face_records.field_faces) == {}
    del face_records.field_faces
    legacy = capture_volume(face_records)
    assert not legacy.faces_available and legacy.field_faces == {}


@pytest.mark.parametrize("volume", [False, True])
def test_faces_have_exact_html_records_and_visible_volume_before_after(tmp_path, face_records, volume):
    import event_universe.diagnostics.render as renderer

    after = capture_volume(face_records) if volume else capture_frame(face_records, Slice("XY", 6))
    before = deepcopy(after)
    before.tick = 0
    before.field_faces = {(4, 5, 6): (0, 0, 0, 0, 0, 0)}
    frames = [before, after]
    original_frames = deepcopy(frames)
    metadata = {"case": "face-diagnostic"}
    path = tmp_path / "faces.html"
    original = renderer._save_animation_html

    def inspect(fig, draw, *args, **kwargs):
        if volume:
            draw(0)
            labels = [text.get_text() for text in fig.texts]
            assert all(f"{label}: 0" in labels for label in FACE_LABELS)
            draw(1)
            labels = [text.get_text() for text in fig.texts]
            assert all(
                f"{label}: {value}" in labels
                for label, value in zip(FACE_LABELS, (1, -2, 3, -4, 5, -6), strict=True)
            )
            assert any("not velocity or phi" in label for label in labels)
        return original(fig, draw, *args, **kwargs)

    with patch.object(renderer, "_save_animation_html", side_effect=inspect):
        if volume:
            render_volume(frames, path, title="Delivered faces before and after", metadata=metadata)
        else:
            render_run(frames, Slice("XY", 6), path, title="Delivered faces", metadata=metadata)
    details = json.loads(html.unescape(re.search(r"<pre>(.*?)</pre>", path.read_text(), re.S).group(1)))
    assert details["delivered_faces"]["order"] == list(FACE_LABELS)
    assert details["delivered_faces"]["frames"][1]["cells"][0]["values"] == (
        [8, 0, 0, 0, 0, 0] if volume else [1, -2, 3, -4, 5, -6]
    )
    assert frames == original_frames and metadata == {"case": "face-diagnostic"}
    with Image.open(path.with_suffix(".gif")) as gif:
        assert gif.n_frames == 2 and "loop" not in gif.info
        if volume:
            assert gif.size == (1500, 1275)


def test_generic_primary_projection_keeps_named_fields_distinct(face_records):
    from unittest.mock import Mock

    from event_universe.core.generic_engine import GenericEngine
    from event_universe.diagnostics.render import _face_metadata

    primary = dict(face_records.field_faces)
    secondary = {(4, 5, 6): (100, 200, 300, 400, 500, 600)}
    world = Mock(
        spec=GenericEngine,
        **vars(face_records),
        display_field_name="density",
        field_faces_by_name={"density": primary, "outward": secondary},
        field_inventory_by_name={
            "density": {(4, 5, 6): (7,)},
            "outward": {(4, 5, 6): (1, 2, 3, 4, 5, 6, 7, 8)},
        },
    )
    frame = capture_volume(world)
    assert frame.field_kind == "face-magnitude"
    assert frame.primary_field_name == "density"
    assert frame.field == {(4, 5, 6): 21, (2, 3, 8): 8}
    assert frame.field_faces_by_name == {"density": primary, "outward": secondary}
    details = _face_metadata([frame], {})["delivered_faces"]["frames"][0]
    assert details["primary_field_name"] == "density"
    assert details["local_inventory"]["density"] == [{"position": (4, 5, 6), "channels": (7,)}]
    assert frame.field_inventory_by_name["outward"][(4, 5, 6)] == (1, 2, 3, 4, 5, 6, 7, 8)
    frame.field_inventory_by_name["density"].clear()
    assert world.field_inventory_by_name["density"] == {(4, 5, 6): (7,)}
    assert details["fields"]["outward"] == [
        {"position": (4, 5, 6), "values": (100, 200, 300, 400, 500, 600)}
    ]
    plane = capture_frame(world, Slice("XY", 6))
    assert plane.field == {(4, 5): 21}
    assert plane.field_faces_by_name["density"] == {(4, 5, 6): (1, -2, 3, -4, 5, -6)}
    frame.field_faces_by_name["outward"].clear()
    assert secondary == {(4, 5, 6): (100, 200, 300, 400, 500, 600)}
