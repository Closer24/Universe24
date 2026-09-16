"""Particle interaction probes with deterministic axis rays: signs, recoil and emission."""

import importlib.util
import json
from pathlib import Path

from event_universe.runner import run_initialization

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "particle_interactions", ROOT / "examples/particle-interactions/run_experiments.py"
)
PROBE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(PROBE)
AXES = [[1, 0, 0], [-1, 0, 0], [0, 1, 0], [0, -1, 0], [0, 0, 1], [0, 0, -1]]


def axis_document(bodies, ticks, shared_field=True):
    PROBE.SIZE, PROBE.CENTER = 15, 7
    raw = PROBE.charged_document(bodies, ticks, shared_field=shared_field)
    for definition in raw["spatial_fields"]:
        if definition["transport"] == "ray":
            definition["headings"] = AXES
            definition["rays_per_tick"] = 6
    return raw


def positions(history, name):
    return [(e["tick"], e["offset"][0], e["momentum"][0]) for e in history[name] if e.get("offset")]


def test_like_charges_repel_head_on_and_never_share_a_node():
    bodies = [
        {"name": "left", "mass": 4, "charge": 3, "momentum": [16, 0, 0], "position": [-4, 0, 0]},
        {"name": "right", "mass": 4, "charge": 3, "momentum": [-16, 0, 0], "position": [4, 0, 0]},
    ]
    world, history = PROBE.track(axis_document(bodies, 16))
    left, right = positions(history, "left"), positions(history, "right")
    closest = min(right_x[1] - left_x[1] for left_x, right_x in zip(left, right, strict=True))
    assert closest > 0
    # Both momenta reverse; the changes are equal and opposite between the bodies.
    assert left[-1][2] < 0 < right[-1][2]
    assert left[-1][2] + right[-1][2] == 0
    assert world.totals()["momentum"] == (0, 0, 0)


def test_opposite_charges_attract_and_neutral_bodies_pass_through():
    attracting = [
        {"name": "left", "mass": 4, "charge": 3, "momentum": [0, 0, 0], "position": [-3, 0, 0]},
        {"name": "right", "mass": 4, "charge": -3, "momentum": [0, 0, 0], "position": [3, 0, 0]},
    ]
    _, history = PROBE.track(axis_document(attracting, 8))
    left, right = positions(history, "left"), positions(history, "right")
    assert left[-1][2] > 0 > right[-1][2] and left[-1][1] > -3 and right[-1][1] < 3
    neutral = [
        {"name": "left", "mass": 4, "charge": 0, "momentum": [64, 0, 0], "position": [-3, 0, 0]},
        {"name": "right", "mass": 4, "charge": 0, "momentum": [-64, 0, 0], "position": [3, 0, 0]},
    ]
    _, history = PROBE.track(axis_document(neutral, 8))
    left, right = positions(history, "left"), positions(history, "right")
    # Edge case: without charge nothing is emitted; the bodies cross unchanged.
    assert left[-1][2] == 64 and right[-1][2] == -64 and left[-1][1] > right[-1][1]


def test_light_body_recoils_more_than_the_heavy_one_with_equal_kicks_per_hit():
    bodies = [
        {"name": "heavy", "mass": 64, "charge": 3, "momentum": [0, 0, 0], "position": [0, 0, 0]},
        {"name": "light", "mass": 1, "charge": 3, "momentum": [0, 0, 0], "position": [3, 0, 0]},
    ]
    _, history = PROBE.track(axis_document(bodies, 7))
    heavy, light = positions(history, "heavy"), positions(history, "light")
    kick = 3 * (3 * PROBE.EMISSION_PER_CHARGE // 6)  # charge x one axis ray of the other body
    assert light[-1][2] > 0 > heavy[-1][2]
    assert light[-1][2] % kick == 0 and heavy[-1][2] % kick == 0
    # The light body rides along its outgoing ray front and is kicked every tick; the
    # heavy body waits for rays from ever farther away, so its kicks lag (retardation).
    assert abs(heavy[-1][2]) <= light[-1][2]
    assert light[-1][1] - 3 > 0 >= heavy[-1][1]


def test_bound_pair_emits_a_proton_after_its_timer_with_conserved_momentum_and_mass():
    PROBE.SIZE, PROBE.CENTER = 15, 7
    raw = PROBE.emission_document(ticks=12, delay=4, proton_momentum=16, residual_mass=3)
    world, history = PROBE.track(raw)
    proton = [e for e in history["free_proton"] if e.get("offset")]
    core = [e for e in history["recoiling_core"] if e.get("offset")]
    # The pair converts on the cycle after the timer passes the delay.
    assert proton[0]["tick"] == 6 and not [
        e for e in history["bound_proton"] if e.get("offset") and e["tick"] > 5
    ]
    assert proton[-1]["offset"][0] > 0 > core[-1]["offset"][0]
    assert proton[-1]["momentum"] == [16, 0, 0] and core[-1]["momentum"] == [-16, 0, 0]
    # The light proton leaves at one hop per tick; the heavier core recoils at a third.
    assert proton[-1]["offset"][0] >= 3 * abs(core[-1]["offset"][0]) - 1
    assert world.totals()["mass"] == (4,) and world.totals()["momentum"] == (0, 0, 0)


def test_self_exclusion_removes_the_push_from_a_moving_body_s_own_rays():
    body = [{"name": "mover", "mass": 4, "charge": 3, "momentum": [16, 0, 0], "position": [-5, 0, 0]}]
    _, excluded = PROBE.track(axis_document(body, 8))
    raw = axis_document(body, 8)
    raw["spatial_fields"][1]["self_exclusion"] = False
    _, pushed = PROBE.track(raw)
    kept = positions(excluded, "mover")
    self_pushed = positions(pushed, "mover")
    # With exclusion the lone body keeps its momentum while moving; without it,
    # every move lands it among the rays it emitted one tick earlier.
    assert all(m == 16 for _, _, m in kept)
    assert self_pushed[-1][2] > 16
    assert kept[-1][1] > -5


def test_like_charges_repel_through_one_shared_field_with_self_exclusion():
    bodies = [
        {"name": "left", "mass": 4, "charge": 3, "momentum": [16, 0, 0], "position": [-4, 0, 0]},
        {"name": "right", "mass": 4, "charge": 3, "momentum": [-16, 0, 0], "position": [4, 0, 0]},
    ]
    raw = axis_document(bodies, 16)
    assert [f["field"] for f in raw["spatial_fields"]] == ["momentum", "charge_field"]
    _, history = PROBE.track(raw)
    left, right = positions(history, "left"), positions(history, "right")
    assert min(r[1] - l_[1] for l_, r in zip(left, right, strict=True)) > 0
    assert left[-1][2] < 0 < right[-1][2] and left[-1][2] + right[-1][2] == 0


def test_oblique_transport_uses_tangential_momentum_before_radial_weight_is_exhausted(tmp_path):
    # Independent 1:2 lane quota: Y, X, Y. A cyclic weight block gives X, X, X
    # for the unnormalized (400, 800) data and hides tangential motion entirely.
    body = [
        {"name": "probe", "mass": 75, "charge": 0, "momentum": [-400, 800, 0], "position": [0, 0, 0]}
    ]
    raw = axis_document(body, 6)
    path = tmp_path / "oblique.json"
    path.write_text(json.dumps(raw), encoding="utf-8")
    output = tmp_path / "oblique"
    run_initialization(path, output)
    events = [json.loads(line) for line in (output / "events.jsonl").read_text().splitlines()]
    sent = [event for event in events if event["event"] == "sent"]
    assert [event["port"] for event in sent[:3]] == [2, 1, 2]
    assert all(event["values"]["momentum"] == [-400, 800, 0] for event in sent)
    assert all(event["arrival_tick"] == event["tick"] + 1 for event in sent)
    report = json.loads((output / "run.json").read_text())
    assert report["status"] == "completed" and report["accounting_balanced_at_every_completed_tick"]
