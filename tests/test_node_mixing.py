"""The Node mixes the six (node-mixing-v1; Highlights 5.4, point 24, the model
owner's decision of 2026-09-18): at every Node the shadows of one group (owner,
sign, polarization) that arrived through the six Ports are six amplitudes,
sqrt(amount) at their phase; each Port sends out a third of their coherent sum
less the arrival that came in through it, sent back; the total is shared among
the six headings by the squared leaving amplitudes in whole quanta with the
ninths below one quantum parked in the Node's registers, each share at the
phase of its leaving amplitude. Nothing is declared: the family's phase width
is the mixing's one input.

Expected integers are pinned in docs/TEST_EXPECTATIONS.md ("The Node mixes the
six") before the first run: (a) a lone arrival of 9 sends 4 back and 1 on each
other heading, (b) two equal arrivals head on in phase send a/9 on the axis and
4a/9 transverse, (c) two in antiphase are each sent back whole, (d) two owners
do not mix, (e) two shadows on one heading are one amplitude, (f) unequal
amounts and phases in the integers of the rule, (g) the registers and the sign,
(h) nothing declared and the record, (i) the dense layer agrees.
"""

import json
from copy import deepcopy

import pytest

from event_universe import Simulation
from event_universe.core.spatial_state import (
    BIT_SHADOW,
    MIXING_DENOMINATOR,
    NODE_MIXING,
    PORT_HEADINGS,
    Ray,
    node_mixing,
    phase_cosines,
    phase_sines,
    spread_content,
    steering_table,
)
from event_universe.initialization import parse_initial_state
from event_universe.runner import run_initialization

HEADINGS = [[1, 0, 0], [-1, 0, 0], [0, 1, 0], [0, -1, 0], [0, 0, 1], [0, 0, -1]]
X, MINUS_X, Y, MINUS_Y, Z, MINUS_Z = (tuple(h) for h in HEADINGS)
COSTS = ("receive", "read", "evaluate", "update", "couple", "route", "split", "send", "commit")
REFERENCE = (8, 7, 4, 1, 0, 1, 4, 7)
HOME = (5, 2, 2)
ZERO = (0, 0)


def shadow(position, heading, amount, phase=0, owner=1):
    return {
        "position": list(position),
        "heading": list(heading),
        "amount": amount,
        "phase": phase,
        "owner": owner,
    }


def document(shadows, *, ticks=1, phase_bits=3, holders=1, dense=None):
    """An open 11 x 5 x 5 board with one family `m` of the given phase width,
    `holders` never-seeded holder types (things 1..) and the shadows given with
    the board as content that arrived (steps 1); nothing declared of the spread."""
    family = {
        "field": "m",
        "baseline": 0,
        "transport": "ray",
        "headings": HEADINGS,
        "rays_per_tick": 1,
        "metric": "links",
        "pace": [1, 1],
        "charge": -1,
        "release": [1, 1],
    }
    doc = {
        "schema_version": 1,
        "N": 1 << phase_bits,
        "model_id": "node-mixing-test-v1",
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


def parked_blocks(snapshot):
    """The parked shares of sign 0 per (Node, owner): the ninths and their phases
    in Port order, read from the parked shadows of the snapshot (node-is-ports-v1)."""
    blocks = {}
    for entry in snapshot["parked"]:
        if entry["sign"] != 0 or not entry["amount"]:
            continue
        key = (tuple(entry["position"]), entry["owner"])
        amounts, phases = blocks.setdefault(key, ([0] * 6, [0] * 6))
        port = PORT_HEADINGS.index(tuple(entry["heading"]))
        amounts[port], phases[port] = entry["amount"], entry["phase"]
    return blocks


def run(doc, ticks):
    """Per tick the board (every Node's rays on their way as (amount, heading,
    phase, owner), sorted, the parked shares beside them left out), the ledger
    and the shadows' content; the events; the parked shares of sign 0 per
    (Node, owner) after every tick, in Port order with their phases."""
    events = []
    boards, ledgers, contents, registers = [], [], [], []
    with Simulation(parse_initial_state(doc), observer=events.append) as world:
        for _ in range(ticks):
            world.step()
            boards.append(
                {
                    node.position: sorted(
                        (ray.amount, tuple(HEADINGS[ray.heading]), ray.phase, ray.owner)
                        for family in node.rays
                        for ray in family
                        if not ray.parked
                    )
                    for node in world.inventory_view().nodes
                    if any(not ray.parked for family in node.rays for ray in family)
                }
            )
            ledgers.append(world.audit())
            contents.append(world.shadow_content())
            registers.append(parked_blocks(world.snapshot()))
    return {
        "boards": boards,
        "ledgers": ledgers,
        "contents": contents,
        "events": events,
        "registers": registers,
    }


def only(board, position, heading, amount, phase=0, owner=1):
    assert board.get(position) == [(amount, heading, phase, owner)], position


def no_node_events(events):
    return {e["event"] for e in events} <= {"cycle_started", "cycle_committed"}


def balanced(result):
    return all(entry["balanced"] and entry["real_conserved"] for entry in result["ledgers"])


def lone(heading, amount, phase=0, sign=0):
    """A shadow of thing 1 that arrived on a heading, for `spread_content`."""
    return Ray(
        heading, (0, 0, 0), amount, phase=phase, steps=1, detector=BIT_SHADOW, source_sign=sign, owner=1
    )


LONE = [shadow(HOME, X, 9)]
IN_PHASE = [shadow(HOME, X, 9), shadow(HOME, MINUS_X, 9)]
ANTIPHASE = [shadow(HOME, X, 9), shadow(HOME, MINUS_X, 9, phase=4)]
TWO_OWNERS = [shadow(HOME, X, 9), shadow(HOME, MINUS_X, 9, owner=2)]
LAYERS = [shadow(HOME, X, 9), shadow(HOME, X, 9, phase=2)]
UNEQUAL = [shadow(HOME, X, 24), shadow(HOME, MINUS_X, 8, phase=2)]
TRANSVERSE = (((5, 3, 2), Y), ((5, 1, 2), MINUS_Y), ((5, 2, 3), Z), ((5, 2, 1), MINUS_Z))


def test_a_lone_arrival_sends_four_ninths_back_and_a_ninth_each_way():
    """(a): 9 on +X: 4 back through the Port it came in by at the opposite phase,
    1 through each of the other five; the 4 and the 1s then park their ninths."""
    cosines, sines = phase_cosines(8), phase_sines(8)
    assert node_mixing(((9, 0), ZERO, ZERO, ZERO, ZERO, ZERO), cosines, sines) == (
        (1, 0, 0),
        (4, 0, 4),
        (1, 0, 0),
        (1, 0, 0),
        (1, 0, 0),
        (1, 0, 0),
    )
    result = run(document(LONE, ticks=3, dense=False), 3)
    after_1, after_2, after_3 = result["boards"]
    only(after_1, (4, 2, 2), MINUS_X, 4, phase=4)
    only(after_1, (6, 2, 2), X, 1)
    for position, heading in TRANSVERSE:
        only(after_1, position, heading, 1)
    assert len(after_1) == 6 and result["registers"][0] == {}
    assert after_2 == {HOME: [(1, X, 0, 1)]}
    assert result["registers"][1] == {
        ((4, 2, 2), 1): ([7, 4, 4, 4, 4, 4], [0, 4, 4, 4, 4, 4]),
        ((6, 2, 2), 1): ([1, 4, 1, 1, 1, 1], [0, 4, 0, 0, 0, 0]),
        ((5, 3, 2), 1): ([1, 1, 1, 4, 1, 1], [0, 0, 0, 4, 0, 0]),
        ((5, 1, 2), 1): ([1, 1, 4, 1, 1, 1], [0, 0, 4, 0, 0, 0]),
        ((5, 2, 3), 1): ([1, 1, 1, 1, 1, 4], [0, 0, 0, 0, 0, 4]),
        ((5, 2, 1), 1): ([1, 1, 1, 1, 4, 1], [0, 0, 0, 0, 4, 0]),
    }
    assert after_3 == {}
    assert result["registers"][2] == result["registers"][1] | {
        (HOME, 1): ([1, 4, 1, 1, 1, 1], [0, 4, 0, 0, 0, 0])
    }
    assert result["contents"] == [9, 9, 9] and balanced(result)
    assert no_node_events(result["events"])


def test_two_equal_arrivals_in_phase_go_a_ninth_on_axis_and_four_ninths_transverse():
    """(b): 9 on +X and 9 on -X in phase: a/9 = 1 back each way at the opposite
    phase, 4a/9 = 4 on each transverse heading; the four 1s that come back mix
    in phase into 1 on +X and 1 on -X."""
    cosines, sines = phase_cosines(8), phase_sines(8)
    assert node_mixing(((9, 0), (9, 0), ZERO, ZERO, ZERO, ZERO), cosines, sines) == (
        (1, 0, 4),
        (1, 0, 4),
        (4, 0, 0),
        (4, 0, 0),
        (4, 0, 0),
        (4, 0, 0),
    )
    result = run(document(IN_PHASE, ticks=3, dense=False), 3)
    after_1, after_2, after_3 = result["boards"]
    only(after_1, (6, 2, 2), X, 1, phase=4)
    only(after_1, (4, 2, 2), MINUS_X, 1, phase=4)
    for position, heading in TRANSVERSE:
        only(after_1, position, heading, 4)
    assert len(after_1) == 6 and result["registers"][0] == {}
    assert after_2 == {
        HOME: sorted([(1, MINUS_Y, 4, 1), (1, Y, 4, 1), (1, MINUS_Z, 4, 1), (1, Z, 4, 1)])
    }
    assert result["registers"][1] == {
        ((6, 2, 2), 1): ([1, 4, 1, 1, 1, 1], [4, 0, 4, 4, 4, 4]),
        ((4, 2, 2), 1): ([4, 1, 1, 1, 1, 1], [0, 4, 4, 4, 4, 4]),
        ((5, 3, 2), 1): ([4, 4, 4, 7, 4, 4], [0, 0, 0, 4, 0, 0]),
        ((5, 1, 2), 1): ([4, 4, 7, 4, 4, 4], [0, 0, 4, 0, 0, 0]),
        ((5, 2, 3), 1): ([4, 4, 4, 4, 4, 7], [0, 0, 0, 0, 0, 4]),
        ((5, 2, 1), 1): ([4, 4, 4, 4, 7, 4], [0, 0, 0, 0, 4, 0]),
    }
    assert after_3 == {(6, 2, 2): [(1, X, 4, 1)], (4, 2, 2): [(1, MINUS_X, 4, 1)]}
    assert result["registers"][2] == result["registers"][1] | {
        (HOME, 1): ([7, 7, 1, 1, 1, 1], [4, 4, 4, 4, 4, 4])
    }
    assert result["contents"] == [18, 18, 18] and balanced(result)
    assert no_node_events(result["events"])


def test_two_equal_arrivals_in_antiphase_are_each_sent_back_whole():
    """(c): 9 on +X at phase 0 and 9 on -X at phase 4: each turned back whole
    through the Port it came in by, a half turn on its phase, nothing
    transverse; the pair meets again in antiphase and turns back again."""
    cosines, sines = phase_cosines(8), phase_sines(8)
    assert node_mixing(((9, 0), (9, 4), ZERO, ZERO, ZERO, ZERO), cosines, sines) == (
        (9, 0, 0),
        (9, 0, 4),
        (0, 0, 0),
        (0, 0, 0),
        (0, 0, 0),
        (0, 0, 0),
    )
    result = run(document(ANTIPHASE, ticks=3, dense=False), 3)
    after_1, after_2, after_3 = result["boards"]
    assert after_1 == {(6, 2, 2): [(9, X, 0, 1)], (4, 2, 2): [(9, MINUS_X, 4, 1)]}
    assert after_2[HOME] == [(4, MINUS_X, 4, 1), (4, X, 0, 1)]
    only(after_2, (7, 2, 2), X, 1)
    only(after_2, (3, 2, 2), MINUS_X, 1, phase=4)
    for dx, phase in ((1, 0), (-1, 4)):
        for position, heading in (
            ((5 + dx, 3, 2), Y),
            ((5 + dx, 1, 2), MINUS_Y),
            ((5 + dx, 2, 3), Z),
            ((5 + dx, 2, 1), MINUS_Z),
        ):
            only(after_2, position, heading, 1, phase=phase)
    assert len(after_2) == 11 and result["registers"][1] == {}
    assert after_3 == {(6, 2, 2): [(4, X, 0, 1)], (4, 2, 2): [(4, MINUS_X, 4, 1)]}
    assert len(result["registers"][2]) == 10
    assert result["registers"][2][((7, 2, 2), 1)] == ([1, 4, 1, 1, 1, 1], [0, 4, 0, 0, 0, 0])
    assert result["registers"][2][((3, 2, 2), 1)] == ([4, 1, 1, 1, 1, 1], [0, 4, 4, 4, 4, 4])
    assert result["registers"][2][((4, 3, 2), 1)] == ([1, 1, 1, 4, 1, 1], [4, 4, 4, 0, 4, 4])
    assert result["contents"] == [18, 18, 18] and balanced(result)
    assert no_node_events(result["events"])


def test_two_owners_at_one_node_do_not_mix():
    """(d): 9 on +X of thing 1 and 9 on -X of thing 2 are lone to each other and
    each mixes as (a); the same amounts of one owner give (b)."""
    result = run(document(TWO_OWNERS, holders=2, dense=False), 1)
    (board,) = result["boards"]
    assert board[(6, 2, 2)] == [(1, X, 0, 1), (4, X, 4, 2)]
    assert board[(4, 2, 2)] == [(1, MINUS_X, 0, 2), (4, MINUS_X, 4, 1)]
    for position, heading in TRANSVERSE:
        assert board[position] == [(1, heading, 0, 1), (1, heading, 0, 2)]
    assert len(board) == 6 and result["registers"][0] == {}
    assert result["contents"] == [18] and balanced(result)


def test_two_shadows_on_one_heading_are_one_amplitude():
    """(e): 9 on +X at phase 0 and 9 on +X at phase 2 mix as 18 at the phase of
    their sum, 1: 8 back at phase 5, 2 on each other heading at phase 1."""
    result = run(document(LAYERS, dense=False), 1)
    (board,) = result["boards"]
    only(board, (4, 2, 2), MINUS_X, 8, phase=5)
    only(board, (6, 2, 2), X, 2, phase=1)
    for position, heading in TRANSVERSE:
        only(board, position, heading, 2, phase=1)
    assert len(board) == 6 and result["registers"][0] == {}
    assert result["contents"] == [18] and balanced(result)


def test_unequal_amounts_and_phases_in_the_integers_of_the_rule():
    """(f): 24 on +X at phase 0 and 8 on -X at phase 2: amplitudes 156 and 90 in
    32nds, the weights reduced by seven bits, the 288 ninths shared 56, 104,
    32, 32, 32, 32 by the largest remainder: 6 on +X at phase 7, 11 on -X at
    phase 4, 3 transverse at phase 1, (2, 5, 5, 5, 5, 5) parked."""
    cosines, sines = phase_cosines(8), phase_sines(8)
    assert node_mixing(((24, 0), (8, 2), ZERO, ZERO, ZERO, ZERO), cosines, sines) == (
        (6, 2, 7),
        (11, 5, 4),
        (3, 5, 1),
        (3, 5, 1),
        (3, 5, 1),
        (3, 5, 1),
    )
    result = run(document(UNEQUAL, dense=False), 1)
    (board,) = result["boards"]
    only(board, (6, 2, 2), X, 6, phase=7)
    only(board, (4, 2, 2), MINUS_X, 11, phase=4)
    for position, heading in TRANSVERSE:
        only(board, position, heading, 3, phase=1)
    assert len(board) == 6
    assert result["registers"][0] == {(HOME, 1): ([2, 5, 5, 5, 5, 5], [7, 4, 1, 1, 1, 1])}
    assert result["contents"] == [32] and balanced(result)


def test_the_registers_park_the_ninths_and_keep_the_sign():
    """(g): lone quanta of 1 park 4 ninths back and 1 each way per arrival; the
    back register releases at the third, fifth, seventh and ninth arrival, the
    others at the ninth; opposite signs are two groups."""
    light = parse_initial_state(document(LONE)).spatial_fields[0]
    assert light.spread is True and MIXING_DENOMINATOR == 9
    # The block is thirty-six per owner since return-field-v1: the outgoing
    # shares' eighteen, then the returning shares' (empty here).
    held, held_phases = (0,) * 36, (0,) * 36
    left = [0] * 6
    for n in range(1, 10):
        departures, taken, held, held_phases, _ = spread_content(
            0, (lone(0, 1),), light, held, held_phases
        )
        back = (4 * n) % 9
        others = n % 9
        assert held[6:12] == (others, back, others, others, others, others), n
        expected = [0] * 6
        if n in (3, 5, 7, 9):
            expected[1] = 1
        if n == 9:
            expected = [1, 1, 1, 1, 1, 1]
        assert list(taken.released) == expected, n
        for ray in departures:
            left[ray.heading] += ray.amount
            assert ray.phase == (4 if ray.heading == 1 else 0), n
        if n == 2:
            assert held[6:12] == (2, 8, 2, 2, 2, 2)
    assert left == [1, 4, 1, 1, 1, 1] and held == (0,) * 36 and held_phases == (0,) * 36
    departures, taken, held, held_phases, _ = spread_content(
        0, (lone(0, 3, 0, 1), lone(0, 3, 0, -1)), light
    )
    assert [(r.heading, r.amount, r.phase, r.source_sign) for r in departures] == [
        (1, 1, 4, -1),
        (1, 1, 4, 1),
    ]
    both = ((3,) * 6, (0,) * 6, (3,) * 6)
    assert held == both[0] + both[1] + both[2] + (0,) * 18
    assert taken.signs == (-1, 1) and taken.stored == 4
    assert taken.arrived == (6, 0, 0, 0, 0, 0) and taken.amounts == (0, 2, 0, 0, 0, 0)


def test_nothing_is_declared_and_the_runner_records_the_mixing(tmp_path):
    """(h): a `spread` or `steering` key on a family is refused naming point 24;
    a split's `table` is refused as before and the split carries the family's
    table (section 5.2 stands); the runner records `node_mixing` with N."""
    for key, value in (("spread", [6, 1, 1, 1, 1, 1]), ("steering", list(REFERENCE))):
        declared = document(LONE)
        declared["spatial_fields"][0][key] = value
        with pytest.raises(ValueError, match="the Node mixes the six"):
            parse_initial_state(declared)
    split = document(LONE)
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
    assert rule.splits[0].table == REFERENCE == steering_table(8)
    assert not hasattr(parse_initial_state(document(LONE)).spatial_fields[0], "steering")
    path = tmp_path / "world.json"
    path.write_text(json.dumps(document(LONE, ticks=2)))
    run_initialization(path, tmp_path / "out")
    metadata = json.loads((tmp_path / "out" / "run.json").read_text())
    assert metadata["node_mixing"] == NODE_MIXING == "node-mixing-v1"
    assert metadata["mixing_fields"] == [{"field": "m", "phase_width": 8}]
    assert metadata["shadow_families"] == [
        {"field": "m", "release": [1, 1], "phase_width": 8, "owners": [1]}
    ]
    assert not {"phase_spread", "field_spreading", "spreading_fields"} & metadata.keys()
    assert metadata["shadow_content"] == [9, 9]
    recorded = [
        json.loads(line) for line in (tmp_path / "out" / "events.jsonl").read_text().splitlines()
    ]
    assert no_node_events(recorded)


@pytest.mark.parametrize("name", ["lone", "in_phase", "antiphase", "two_owners", "layers", "unequal"])
def test_the_dense_layer_agrees(name):
    """(i): the shadow layer (dense, the default) and the engine give one board,
    one ledger, one content and one set of registers at every tick."""
    shadows, holders = {
        "lone": (LONE, 1),
        "in_phase": (IN_PHASE, 1),
        "antiphase": (ANTIPHASE, 1),
        "two_owners": (TWO_OWNERS, 2),
        "layers": (LAYERS, 1),
        "unequal": (UNEQUAL, 1),
    }[name]
    ticks = 4
    engine = run(document(deepcopy(shadows), ticks=ticks, holders=holders, dense=False), ticks)
    assert parse_initial_state(document(deepcopy(shadows), ticks=ticks, holders=holders)).dense_field
    dense = run(document(deepcopy(shadows), ticks=ticks, holders=holders), ticks)
    assert engine["boards"] == dense["boards"]
    assert engine["ledgers"] == dense["ledgers"]
    assert engine["contents"] == dense["contents"]
    assert engine["registers"] == dense["registers"]
    assert no_node_events(dense["events"])
