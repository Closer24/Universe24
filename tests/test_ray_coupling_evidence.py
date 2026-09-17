"""Independent evidence checks; synthetic records do not demonstrate dynamics."""

import copy
import importlib.util
from pathlib import Path
from types import SimpleNamespace

import pytest

from event_universe.core.spatial_state import Ray

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "ray_coupling_evidence", ROOT / "examples/generic-ray-coupling/evidence.py"
)
EVIDENCE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(EVIDENCE)


def row(*, phase, owner, amount=5, heading=(1, 0, 0)):
    return {
        "field": "beam",
        "owner": owner,
        "heading_vector": list(heading),
        "ray": {"amount": amount, "phase": phase},
    }


def test_inventory_counts_resident_and_packet_owners_with_opposite_momentum():
    frame = {
        "tick": 0,
        "rays": [row(phase=1, owner="node"), row(phase=1, owner="link", heading=(-1, 0, 0))],
    }
    original = copy.deepcopy(frame)
    assert EVIDENCE.ray_inventory(frame, "beam") == {
        "amount": 10,
        "momentum": [0, 0, 0],
        "resident_count": 1,
        "link_count": 1,
    }
    assert frame == original


def test_phase_or_missing_tick_is_not_repaired_by_expected_sequence():
    frames = [
        {"tick": tick, "rays": [row(phase=phase, owner="node")]} for tick, phase in ((1, 1), (2, 2))
    ]
    expected = {1: {"phases": [1]}, 2: {"phases": [2]}}
    assert EVIDENCE.compare_expected(frames, expected, field="beam")["pass"]
    changed = copy.deepcopy(frames)
    changed[1]["rays"][0]["ray"]["phase"] = 1
    assert not EVIDENCE.compare_expected(changed, expected, field="beam")["pass"]
    assert not EVIDENCE.compare_expected(frames[:1], expected, field="beam")["pass"]
    with pytest.raises(ValueError, match="duplicate"):
        EVIDENCE.compare_expected(frames + frames, expected, field="beam")


def test_copied_owner_trace_preserves_metadata_without_counting_pending_shadow():
    ray = Ray(0, (0, 0, 0), 5, phase=3, advance=1, wait=0, interaction_delay=2)
    node = SimpleNamespace(rays=((ray,),), pending=SimpleNamespace(rays=((ray,),)))
    packet = SimpleNamespace(rays=((ray,),), origin=(1, 1, 1), port=0, arrival_tick=4)
    spatial = SimpleNamespace(
        nodes={(1, 1, 1): node},
        links={(1, 1, 1): (packet, None, None, None, None, None)},
        _neighbor=lambda origin, port: (2, 1, 1),
    )
    world = SimpleNamespace(
        _spatial=spatial,
        initial=SimpleNamespace(
            fields=(SimpleNamespace(name="beam"),),
            spatial_fields=(SimpleNamespace(field=0, headings=((1, 0, 0),), phase_steps=8),),
        ),
    )
    owners = EVIDENCE.owned_rays(world)
    assert [item["owner"] for item in owners] == ["node", "link"]
    assert [item["ray"]["advance"] for item in owners] == [1, 1]
    assert [item["ray"]["interaction_delay"] for item in owners] == [2, 2]
    assert owners[1]["arrival_tick"] == 4
    owners[0]["ray"]["phase"] = 0
    assert ray.phase == 3
