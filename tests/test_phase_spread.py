"""The phase-steered spread (phase-spread-v1; Highlights 5.4, point 17, the model
owner's decision of 2026-09-18, with the polarization amendment of that day):
the shares of one owner that meet at a Node combine by the coherence rule and
steer each other by the Born table, each continuing on its own heading by the
table at its phase difference to the others and sending the rest apart through
its four transverse headings; a lone share keeps the split table; shares of
different owners, or of differing polarization, are lone to each other.

Expected integers are pinned in docs/TEST_EXPECTATIONS.md ("The phase-steered
spread") before the first run: (a) a pair in phase continues, (b) a pair in
opposite phase is sent apart, (c) unequal shares each by their own difference,
(d) three shares each reading the others, (e) two owners are lone to each other,
(f) differing polarization does not steer, (g) the table written from the phase
width, never declared, and recorded, (h) the dense layer agrees.
"""

import json
from copy import deepcopy

import pytest

from event_universe import Simulation
from event_universe.core.spatial_state import (
    PHASE_SPREAD,
    steering_table,
    validate_steering_table,
)
from event_universe.initialization import parse_initial_state
from event_universe.runner import run_initialization

HEADINGS = [[1, 0, 0], [-1, 0, 0], [0, 1, 0], [0, -1, 0], [0, 0, 1], [0, 0, -1]]
X, MINUS_X, Y, MINUS_Y, Z, MINUS_Z = (tuple(h) for h in HEADINGS)
COSTS = ("receive", "read", "evaluate", "update", "couple", "route", "split", "send", "commit")
REFERENCE = (8, 7, 4, 1, 0, 1, 4, 7)
HOME = (5, 2, 2)


def shadow(position, heading, amount, phase=0, owner=1, polarization=None):
    entry = {
        "position": list(position),
        "heading": list(heading),
        "amount": amount,
        "phase": phase,
        "owner": owner,
    }
    if polarization is not None:
        entry["polarization"] = polarization
    return entry


def document(shadows, *, ticks=1, phase_bits=3, holders=1, polarization_bits=None, dense=None):
    """An open 11 x 5 x 5 board with one family `m` spreading by [6, 1, 1, 1, 1, 1]
    at the given phase width, `holders` never-seeded holder types (things 1..),
    and the shadows given with the board as content that arrived (steps 1)."""
    family = {
        "field": "m",
        "baseline": 0,
        "transport": "ray",
        "headings": HEADINGS,
        "rays_per_tick": 1,
        "ray_slots": 8,
        "metric": "links",
        "pace": [1, 1],
        "phase_bits": phase_bits,
        "charge": -1,
        "release": [1, 1],
        "spread": [6, 1, 1, 1, 1, 1],
    }
    if polarization_bits is not None:
        family["polarization_bits"] = polarization_bits
    doc = {
        "schema_version": 1,
        "model_id": "phase-spread-test-v1",
        "shape": [11, 5, 5],
        "boundary": "open",
        "slots_per_node": 2,
        "link_ticks": 1,
        "normal_budget": 100000,
        "ticks": ticks,
        "operation_costs": dict.fromkeys(COSTS, 1),
        "fields": [
            {
                "name": "m",
                "components": 1,
                "units": "quantum",
                "signed": False,
                "conserved": True,
                "extensive": True,
            }
        ],
        "disturbance_types": [
            {
                "name": f"holder_{index}",
                "fields": ["m"],
                "defaults": {"m": 0},
                "transport": {"mode": "hold"},
            }
            for index in range(holders)
        ],
        "spatial_fields": [family],
        "emissions": [],
        "seeds": [],
        "ray_interactions": [],
        "initial_field": {"m": {"rays": list(shadows)}},
    }
    if dense is not None:
        doc["dense_field"] = dense
    return doc


def run(doc, ticks):
    """Per tick the board (every Node's rays as (amount, heading, phase, owner,
    polarization), sorted), the ledger and the shadows' content; the events;
    the remainder registers of sign 0 per (Node, owner) after the run."""
    events = []
    boards, ledgers, contents = [], [], []
    with Simulation(parse_initial_state(doc), observer=events.append) as world:
        for _ in range(ticks):
            world.step()
            boards.append(
                {
                    node.position: sorted(
                        (
                            ray.amount,
                            tuple(HEADINGS[ray.heading]),
                            ray.phase,
                            ray.owner,
                            ray.polarization,
                        )
                        for family in node.rays
                        for ray in family
                    )
                    for node in world.inventory_view().nodes
                    if any(node.rays)
                }
            )
            ledgers.append(world.audit())
            contents.append(world.shadows_content())
        registers = {
            (tuple(entry["position"]), entry["owner"]): (entry["registers"], entry["phases"])
            for entry in world.snapshot()["field_remainders"]
            if entry["sign"] == 0
        }
    return {
        "boards": boards,
        "ledgers": ledgers,
        "contents": contents,
        "events": events,
        "registers": registers,
    }


def only(board, position, heading, amount, phase=0, owner=1, polarization=-1):
    assert board.get(position) == [(amount, heading, phase, owner, polarization)], position


def no_node_events(events):
    return {e["event"] for e in events} <= {"cycle_started", "cycle_committed"}


IN_PHASE = [shadow(HOME, X, 23), shadow(HOME, MINUS_X, 23)]
OPPOSITE = [shadow(HOME, X, 23), shadow(HOME, MINUS_X, 23, phase=4)]
UNEQUAL = [shadow(HOME, X, 24), shadow(HOME, MINUS_X, 8, phase=2)]
THREE = [shadow(HOME, X, 8), shadow(HOME, Y, 8), shadow(HOME, Z, 8, phase=4)]


def test_a_pair_in_phase_continues_forward():
    """(a): two shares of 23 meeting head on in phase continue whole, each on its
    own heading; lone shares beyond keep the split table; the pair that meets
    again in phase continues again; no Node publishes an event."""
    result = run(document(IN_PHASE, ticks=3, dense=False), 3)
    after_1, after_2, after_3 = result["boards"]
    assert set(after_1) == {(6, 2, 2), (4, 2, 2)}
    only(after_1, (6, 2, 2), X, 23)
    only(after_1, (4, 2, 2), MINUS_X, 23)
    only(after_2, (7, 2, 2), X, 12)
    only(after_2, (3, 2, 2), MINUS_X, 12)
    assert after_2[HOME] == [(2, MINUS_X, 0, 1, -1), (2, X, 0, 1, -1)]
    for position, heading in (
        ((6, 3, 2), Y),
        ((6, 1, 2), MINUS_Y),
        ((6, 2, 3), Z),
        ((6, 2, 1), MINUS_Z),
    ):
        only(after_2, position, heading, 2)
    assert len(after_2) == 11
    only(after_3, (8, 2, 2), X, 6)
    only(after_3, (2, 2, 2), MINUS_X, 6)
    assert after_3[(6, 2, 2)] == [(1, MINUS_X, 0, 1, -1), (2, X, 0, 1, -1)]
    assert after_3[(4, 2, 2)] == [(1, X, 0, 1, -1), (2, MINUS_X, 0, 1, -1)]
    only(after_3, (7, 3, 2), Y, 1)
    only(after_3, (6, 4, 2), Y, 1)
    assert result["contents"] == [46, 46, 46]
    assert all(entry["balanced"] and entry["things_conserved"] for entry in result["ledgers"])
    assert no_node_events(result["events"])
    registers = result["registers"]
    assert len(registers) == 12
    assert registers[((6, 2, 2), 1)] == ([6, 1, 1, 1, 1, 1], [0] * 6)
    assert registers[((7, 2, 2), 1)] == ([6, 1, 1, 1, 1, 1], [0] * 6)
    assert registers[((3, 2, 2), 1)] == ([1, 6, 1, 1, 1, 1], [0] * 6)
    assert registers[((6, 3, 2), 1)] == ([2, 2, 1, 2, 2, 2], [0] * 6)
    assert registers[((4, 1, 2), 1)] == ([2, 2, 2, 1, 2, 2], [0] * 6)
    assert (HOME, 1) not in registers


def test_a_pair_in_opposite_phase_is_sent_apart():
    """(b): two shares of 23 in opposite phase: nothing continues, all of it goes
    through the four transverse headings, 5 each and the remaining 3 one to
    each of the first three in Port order; the departures carry the phase of
    the cancelled sum, 0; nothing enters the registers."""
    result = run(document(OPPOSITE, dense=False), 1)
    (board,) = result["boards"]
    assert set(board) == {(5, 3, 2), (5, 1, 2), (5, 2, 3), (5, 2, 1)}
    only(board, (5, 3, 2), Y, 12)
    only(board, (5, 1, 2), MINUS_Y, 12)
    only(board, (5, 2, 3), Z, 12)
    only(board, (5, 2, 1), MINUS_Z, 10)
    assert result["contents"] == [46] and result["registers"] == {}
    assert result["ledgers"][0]["balanced"]


def test_unequal_shares_steer_each_by_its_own_difference():
    """(c): 24 at phase 0 and 8 at phase 2 head on: each reads its difference to
    the other, two steps, half continues (12 and 4), the rest apart (3 and 1 per
    transverse heading); every departure at the phase of the sum, 0."""
    result = run(document(UNEQUAL, dense=False), 1)
    (board,) = result["boards"]
    only(board, (6, 2, 2), X, 12)
    only(board, (4, 2, 2), MINUS_X, 4)
    for position, heading in (
        ((5, 3, 2), Y),
        ((5, 1, 2), MINUS_Y),
        ((5, 2, 3), Z),
        ((5, 2, 1), MINUS_Z),
    ):
        only(board, position, heading, 4)
    assert len(board) == 6
    assert result["contents"] == [32] and result["registers"] == {}


def test_three_shares_each_read_the_others():
    """(d): 8 on +X at phase 0, 8 on +Y at phase 0 and 8 on +Z at phase 4: the +X
    and +Y shares read the others' cancelled sum as step 0 and continue whole;
    the +Z share reads the others at 0, a difference of four steps, and is sent
    apart, 2 on each of +X, -X, +Y, -Y."""
    result = run(document(THREE, dense=False), 1)
    (board,) = result["boards"]
    only(board, (6, 2, 2), X, 10)
    only(board, (5, 3, 2), Y, 10)
    only(board, (4, 2, 2), MINUS_X, 2)
    only(board, (5, 1, 2), MINUS_Y, 2)
    assert len(board) == 4
    assert result["contents"] == [24] and result["registers"] == {}


def test_shares_of_different_owners_are_lone_to_each_other():
    """(e): a share of thing 1 at phase 0 and one of thing 2 at phase 4 meeting
    head on do not combine: each spreads by the split table at its own phase
    into its own registers."""
    shadows = [shadow(HOME, X, 23), shadow(HOME, MINUS_X, 23, phase=4, owner=2)]
    result = run(document(shadows, holders=2, dense=False), 1)
    (board,) = result["boards"]
    assert board[(6, 2, 2)] == [(2, X, 4, 2, -1), (12, X, 0, 1, -1)]
    assert board[(4, 2, 2)] == [(2, MINUS_X, 0, 1, -1), (12, MINUS_X, 4, 2, -1)]
    assert board[(5, 3, 2)] == [(2, Y, 0, 1, -1), (2, Y, 4, 2, -1)]
    assert len(board) == 6
    assert result["contents"] == [46]
    assert result["registers"] == {
        (HOME, 1): ([6, 1, 1, 1, 1, 1], [0] * 6),
        (HOME, 2): ([1, 6, 1, 1, 1, 1], [4] * 6),
    }


def test_differing_polarization_does_not_steer():
    """(f): two shares of one owner in opposite phase with orthogonal polarizations
    are lone to each other (the model owner, 2026-09-18): each spreads by the
    split table at its own phase and polarization, their fractions into the
    owner's one register block; with one polarization they steer as in (b)."""
    orthogonal = [
        shadow(HOME, X, 23, polarization=0),
        shadow(HOME, MINUS_X, 23, phase=4, polarization=2),
    ]
    result = run(document(orthogonal, polarization_bits=2), 1)
    (board,) = result["boards"]
    assert board[(6, 2, 2)] == [(2, X, 4, 1, 2), (12, X, 0, 1, 0)]
    assert board[(4, 2, 2)] == [(2, MINUS_X, 0, 1, 0), (12, MINUS_X, 4, 1, 2)]
    assert board[(5, 3, 2)] == [(2, Y, 0, 1, 0), (2, Y, 4, 1, 2)]
    assert result["contents"] == [46]
    assert result["registers"] == {(HOME, 1): ([7, 7, 2, 2, 2, 2], [0, 4, 0, 0, 0, 0])}
    aligned = [
        shadow(HOME, X, 23, polarization=0),
        shadow(HOME, MINUS_X, 23, phase=4, polarization=0),
    ]
    result = run(document(aligned, polarization_bits=2), 1)
    (board,) = result["boards"]
    assert set(board) == {(5, 3, 2), (5, 1, 2), (5, 2, 3), (5, 2, 1)}
    only(board, (5, 3, 2), Y, 12, polarization=0)
    only(board, (5, 2, 1), MINUS_Z, 10, polarization=0)
    assert result["contents"] == [46] and result["registers"] == {}


def test_the_steering_table_is_written_from_the_phase_width(tmp_path):
    """(g): the steering table is computed once from the family's phase width
    (the model owner, 2026-09-18) and never declared: [8, 7, 4, 1, 0, 1, 4, 7]
    at eight steps; a declared table, on the family or on a split, is refused;
    the runner records the identity and the table used."""
    assert steering_table(8) == REFERENCE
    assert steering_table(1) == (1,)
    assert steering_table(4) == (4, 2, 0, 2)
    assert steering_table(16)[:5] == (16, 15, 14, 11, 8)
    assert parse_initial_state(document(IN_PHASE)).spatial_fields[0].steering == REFERENCE
    assert parse_initial_state(document(IN_PHASE, phase_bits=0)).spatial_fields[0].steering == (1,)
    declared = document(IN_PHASE)
    declared["spatial_fields"][0]["steering"] = list(REFERENCE)
    with pytest.raises(ValueError, match="it is not declared"):
        parse_initial_state(declared)
    split = document(IN_PHASE)
    split["ray_interactions"] = [
        {
            "name": "steer",
            "participants": [{"type": "m"}, {"type": "m"}],
            "outputs": [
                {
                    "field": "m",
                    "amount": {"table": list(REFERENCE), "of": "sum", "index": "phase_difference"},
                    "heading": 2,
                },
                {"field": "m", "amount": {"rest_of": 0}, "heading": 3, "phase": {"of": 1}},
            ],
            "invariants": [{"name": "energy", "expression": {"field": "amount"}}],
        }
    ]
    with pytest.raises(ValueError, match="it is not declared"):
        parse_initial_state(split)
    del split["ray_interactions"][0]["outputs"][0]["amount"]["table"]
    (rule,) = parse_initial_state(split).ray_interactions
    assert rule.splits[0].table == REFERENCE
    with pytest.raises(ValueError, match="through the modulus"):
        validate_steering_table((8, 7, 4, 1, 0, 1, 4, 9), 8)
    path = tmp_path / "world.json"
    path.write_text(json.dumps(document(IN_PHASE, ticks=2)))
    run_initialization(path, tmp_path / "out")
    metadata = json.loads((tmp_path / "out" / "run.json").read_text())
    assert metadata["phase_spread"] == PHASE_SPREAD == "phase-spread-v1"
    assert metadata["shadow_families"][0]["steering"] == list(REFERENCE)
    assert metadata["shadows_content"] == [46, 46]
    recorded = [
        json.loads(line) for line in (tmp_path / "out" / "events.jsonl").read_text().splitlines()
    ]
    assert no_node_events(recorded)


@pytest.mark.parametrize("name", ["in_phase", "opposite", "unequal", "three"])
def test_the_dense_layer_agrees(name):
    """(h): the shadow layer (dense, the default) and the engine give one board,
    one ledger and one content at every tick (point 13)."""
    shadows = {"in_phase": IN_PHASE, "opposite": OPPOSITE, "unequal": UNEQUAL, "three": THREE}[name]
    ticks = 4
    engine = run(document(deepcopy(shadows), ticks=ticks, dense=False), ticks)
    assert parse_initial_state(document(deepcopy(shadows), ticks=ticks)).dense_field
    dense = run(document(deepcopy(shadows), ticks=ticks), ticks)
    assert engine["boards"] == dense["boards"]
    assert engine["ledgers"] == dense["ledgers"]
    assert engine["contents"] == dense["contents"]
    assert engine["registers"] == dense["registers"]
    assert no_node_events(dense["events"])
