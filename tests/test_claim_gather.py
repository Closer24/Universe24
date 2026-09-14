"""Claim and gather: a captured train turns homeward and arrives whole; rivals yield; closed."""

import importlib.util
import json
from pathlib import Path

import pytest

from event_universe import Simulation
from event_universe.core.spatial_state import Claim, Ray, merge_rays, validate_claims, validate_rays
from event_universe.initialization import parse_initial_state
from event_universe.runner import run_initialization

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "claim_gather_probe", ROOT / "examples/claim-gather/run_experiments.py"
)
PROBE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(PROBE)


def test_a_claim_floods_the_world_and_every_quantum_of_the_train_comes_home():
    result = PROBE.gather(PROBE.gather_document())
    # The wave at a quarter link per tick reaches the screen six links away after
    # the two-tick delay; the first click opens the claim, the flood reaches all
    # 25 x 25 x 3 Nodes, and the whole particle is at the screen by tick 60.
    assert result["first_claim_tick"] == 27 and result["nodes_claimed"] == 25 * 25 * 3
    assert result["screens"] == {PROBE.SCREEN_X: PROBE.MATTER} and result["escaped"] == 0
    assert result["gathered_tick"] is not None and result["gathered_tick"] <= 60
    assert result["screen_momenta"] == {PROBE.SCREEN_X: [0, 0, 0]}
    assert result["roots"] == [{"position": [PROBE.SCREEN_X, 0], "since": 26}]
    assert result["matter_closed"]


def test_without_a_claim_the_screen_keeps_only_its_own_line_and_the_rest_escapes():
    result = PROBE.gather(PROBE.gather_document(claim=False))
    assert result["screens"] == {PROBE.SCREEN_X: PROBE.MATTER // len(PROBE.PLANAR_HEADINGS)}
    assert result["nodes_claimed"] == 0 and result["roots"] == []
    # At a quarter link per tick only the axis rays have left the world by tick 80;
    # the diagonals are still on their way out.
    assert result["escaped"] == 24 and result["timeline"][-1]["free"] == 32
    assert result["matter_closed"]


def test_where_two_claims_meet_the_earlier_capture_wins_and_the_later_root_yields():
    result = PROBE.gather(PROBE.gather_document(rival=True))
    # The rival four links away clicks first (tick 18) and gathers everything but
    # the two quanta the farther screen took before its claim yielded.
    assert result["screens"] == {PROBE.RIVAL_X: PROBE.MATTER - 2, PROBE.SCREEN_X: 2}
    assert [root["position"] for root in result["roots"]] == [[PROBE.RIVAL_X, 0]]
    assert result["first_claim_tick"] == 19 and result["escaped"] == 0
    assert result["matter_closed"]


def test_the_double_slit_landing_composes_gathers_at_one_root_and_closes():
    raw = PROBE.landing_document(3)
    initial = parse_initial_state(raw)
    field = initial.spatial_fields[0]
    assert field.claims and field.pace_numerator == 1 and field.pace_denominator == 2
    assert initial.emissions[0].train_field is not None and initial.emissions[1].train_carried
    assert [rule.claim for rule in initial.spatial_couplings] == [False, False, True]
    result = PROBE.landing(PROBE.landing_document(3, ticks=150))
    assert result["matter_closed"] and len(result["roots"]) == 1 and result["in_flight"] == 0
    assert result["winner"] == result["roots"][0]
    assert result["winner_matter"] > result["other_screens"]


def test_claims_and_homing_rays_are_validated_and_identified(tmp_path):
    definition = parse_initial_state(PROBE.gather_document()).spatial_fields[0]
    plain = parse_initial_state(PROBE.gather_document(claim=False))
    plain_field = plain.spatial_fields[0]
    assert plain_field.claims  # the field keeps claims; only the rule stopped claiming
    validate_claims((Claim(7, -1, 3, 1, (1, 2, 3)), Claim(8, 2, 5)), definition)
    for claims in (
        (Claim(7, -1, 3), Claim(7, 1, 4)),
        (Claim(0, -1, 3),),
        (Claim(7, 6, 3),),
        (Claim(7, -1, -1),),
        tuple(Claim(train, 0, 0) for train in range(1, PROBE.CLAIM_SLOTS + 2)),
    ):
        with pytest.raises(ValueError):
            validate_claims(claims, definition)
    field = plain.fields[definition.field]
    validate_rays((Ray(0, (0, 0, 0), 2, train=7, homing=1),), definition, field)
    with pytest.raises(ValueError, match="homing"):
        validate_rays((Ray(0, (0, 0, 0), 2, homing=1),), definition, field)
    with pytest.raises(ValueError, match="train"):
        validate_rays((Ray(0, (0, 0, 0), 2, train=-1),), definition, field)
    # Rays merge only within one train and one direction of travel.
    merged = merge_rays(
        (
            Ray(0, (0, 0, 0), 1, train=7),
            Ray(0, (0, 0, 0), 1, train=8),
            Ray(0, (0, 0, 0), 1, train=7, homing=1),
        )
    )
    assert len(merged) == 3
    raw = PROBE.gather_document(ticks=2)
    del raw["emissions"][0]["recoil_field"]
    del raw["spatial_couplings"][0]["momentum_field"]
    path = tmp_path / "gather.json"
    path.write_text(json.dumps(raw))
    run_initialization(path, tmp_path / "out", ticks=2)
    metadata = json.loads((tmp_path / "out" / "run.json").read_text())
    assert metadata["spatial_claims"] == "claim-gather-ray-field-v1"
    for patch, message in (
        ({"pace": [3, 2]}, "one link per tick"),
        ({"claim": {"ticks": 0, "slots": 4}}, "claim.ticks"),
        ({"claim": {"ticks": 10, "slots": 65}}, "at most 64"),
    ):
        broken = PROBE.gather_document()
        broken["spatial_fields"][0].update(patch)
        with pytest.raises(ValueError, match=message):
            parse_initial_state(broken)
    broken = PROBE.gather_document()
    del broken["spatial_fields"][0]["claim"]
    with pytest.raises(ValueError, match="train_field requires"):
        parse_initial_state(broken)
    broken = PROBE.gather_document()
    del broken["spatial_fields"][0]["claim"]
    del broken["emissions"][0]["train_field"]
    with pytest.raises(ValueError, match="claiming absorb rule requires"):
        parse_initial_state(broken)
    broken = PROBE.gather_document()
    broken["emissions"][0]["train_field"] = "carried"
    with pytest.raises(ValueError, match="requires an absorb rule"):
        parse_initial_state(broken)
    broken = PROBE.gather_document()
    broken["emissions"][0]["train_field"] = "momentum"
    with pytest.raises(ValueError, match="scalar owned"):
        parse_initial_state(broken)


def test_a_slow_pace_keeps_the_causal_bound_and_a_waiting_ray_stays_resident():
    raw = PROBE.gather_document(ticks=8, claim=False)
    world = Simulation(parse_initial_state(raw))
    farthest = []
    for _ in range(8):
        world.step()
        far = 0
        for node in world.inventory_view().nodes:
            if node.rays and node.rays[0]:
                far = max(
                    far, abs(node.position[0] - PROBE.CENTER) + abs(node.position[1] - PROBE.CENTER)
                )
        farthest.append(far)
    # Nothing for two ticks, then a quarter link per tick: one link by tick 6.
    assert farthest == [0, 0, 0, 0, 0, 1, 1, 1]


def test_the_event_audit_closes_through_capture_flood_and_gather():
    raw = PROBE.gather_document(ticks=30, matter=16)
    raw["shape"] = [13, 13, 3]
    raw["spatial_fields"][0]["pace"] = [1, 2]
    raw["seeds"] = [
        {"position": [6, 6, 1], "type": "particle"},
        {"position": [9, 6, 1], "type": "screen"},
    ]
    raw["conservation"] = {
        "name": "matter",
        "energy_units": "matter quantum",
        "momentum_units": "matter quantum times heading",
        "carriers": [
            {
                "requires": ["matter", "momentum"],
                "energy": {"field": "matter"},
                "momentum": {"field": "momentum"},
            }
        ],
        "spatial": {
            "energy": {"field": "matter", "side": "right"},
            "momentum": {"op": "vector", "args": [0, 0, 0]},
        },
    }
    world = Simulation(parse_initial_state(raw))
    initial = world.totals()["matter"][0]
    for _ in range(30):
        world.step()
    screen = next(
        world.record_values(record)
        for node in world.nodes.values()
        for record in node.records
        if record is not None and record.type_index == 1
    )
    # The three axis quanta that reached the small world's edge before the flood
    # escaped; the thirteen the claim caught are at the screen with the momentum
    # of the one ray it captured itself.
    assert screen["matter"] == (13,) and screen["momentum"] == (1, 0, 0)
    assert world.escaped_totals()["matter"][0] == 3
    assert world.totals()["matter"][0] + 3 == initial
    report = world.conservation_report()
    assert report["status"] == "passed" and report["checked_node_events"] > 100000
