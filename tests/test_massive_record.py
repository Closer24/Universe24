"""The massive record kind (`massive-record-v1`, docs/designs/detector_law/MASSIVE_RECORD.md;
the build's plan BUILD.md section 6, the expected integers written there before the code):
the rule with a pair per record kind on the six-neighbour term, (a) on a chain and (b) at a
corner against section 1's integers, (c) light's pair [1, 1] the first build's integers bit
for bit, (d) the conserved form I to the remainders' jitter; (p) the byte identity of the
light record without the key (the digests of the head f4a3971a); (q) the loader's refusals
of the step's keys; (r) the record's keys under the key and none without it."""

from __future__ import annotations

import hashlib
import json

import numpy as np
import pytest

from event_universe.events.detector_law import UNIT, DetectorLawSimulation, LiveRecord
from event_universe.events.world import LIGHT_PAIR, MASSIVE_RECORD_RULE, parse_nature_beam_world
from tests.test_detector_law import chain_world


def massive_world(
    shape: list[int], boundary: object, pair: list[int], faces: dict[str, str] | None = None
) -> dict:
    """A world of the massive kind `matter` (its pair on the six-neighbour term) beside light,
    no lamp, no block (the rule's tests construct a record's rows directly)."""
    matter: dict = {"name": "matter", "quantum": 1, "pair": pair}
    if faces is not None:
        matter["faces"] = faces
    return {
        "law": "beam",
        "model_id": "beam-massive-record-rule-v1",
        "shape": shape,
        "boundary": boundary,
        "ticks": 10,
        "K": 1073741824,
        "N": 64,
        "release": [1, 128],
        "suspension": 0,
        "detector_law": True,
        "massive_record": True,
        "directions": [],
        "families": [{"name": "light", "quantum": 1, "phase_per_link": [77, 25]}, matter],
        "measured": [],
        "detectors": [],
    }


def planted(
    simulation: DetectorLawSimulation, family: int, now: np.ndarray, before: np.ndarray, r: np.ndarray
) -> LiveRecord:
    """A record's rows given to the rule's step directly (the test's device: no lamp births a
    massive record; the rule reads the rows and nothing else)."""
    return LiveRecord(
        1,
        0,
        family,
        0,
        1,
        0,
        1,
        1,
        1,
        0,
        1,
        now.astype(np.int64),
        before.astype(np.int64),
        r.astype(np.int64),
        pointers=[0] * len(simulation.cell_names),
        first_rung=[None] * len(simulation.cell_names),
        ports=[np.zeros(simulation.shape, dtype=np.int64) for _ in simulation.take_masks],
        age=10,
    )


def step_once(simulation: DetectorLawSimulation, live: LiveRecord) -> tuple[np.ndarray, np.ndarray]:
    """One step of the rule; returns (a_next, r') from the record's rows after the step."""
    simulation._advance(live)
    return live.now.copy(), live.remainder.copy()


def test_a_the_rule_on_a_chain_against_section_ones_integers():
    """BUILD.md (a): the kind [2, 3] on a 5-Node open chain (y, z one layer periodic, so
    S_6 = a_W + a_E + 4 a_now with 0 beyond the ends); the totals num S_6 - 9 a_before + r
    are [1, 27, -56, 19, 7], a_next = [0, 3, -7, 2, 0], r' = [1, 0, 7, 1, 7]."""
    world = parse_nature_beam_world(
        massive_world([5, 1, 1], {"x": "open", "y": "periodic", "z": "periodic"}, [2, 3], {"x": "open"})
    )
    simulation = DetectorLawSimulation(world)
    now = np.array([0, 5, -7, 3, 0]).reshape(5, 1, 1)
    before = np.array([1, 0, 2, -1, 0]).reshape(5, 1, 1)
    r = np.array([0, 1, 2, 0, 1]).reshape(5, 1, 1)
    live = planted(simulation, 1, now, before, r)
    a_next, r_next = step_once(simulation, live)
    assert a_next.ravel().tolist() == [0, 3, -7, 2, 0]
    assert r_next.ravel().tolist() == [1, 0, 7, 1, 7]
    assert all(0 <= value < 9 for value in r_next.ravel().tolist())
    # T: the row's past is the amplitude the step read
    assert live.before.ravel().tolist() == [0, 5, -7, 3, 0]


def test_b_the_rule_at_a_corner_of_an_open_board():
    """BUILD.md (b): the kind [1, 2] (3 den = 6) at the corner (0, 0, 0) of an open 2^3 board
    of the massive kind (its faces declared open on every axis): a_now 4 with the three
    neighbours 3, -2, 5 and three zero faces, a_before 1, r 5: the total 5, a_next 0, r' 5;
    with a_before -2 the total 23, a_next 3, r' 5."""
    faces = {"x": "open", "y": "open", "z": "open"}
    world = parse_nature_beam_world(massive_world([2, 2, 2], "open", [1, 2], faces))
    simulation = DetectorLawSimulation(world)
    for past, expected in ((1, 0), (-2, 3)):
        now = np.zeros((2, 2, 2), dtype=np.int64)
        now[0, 0, 0] = 4
        now[1, 0, 0] = 3
        now[0, 1, 0] = -2
        now[0, 0, 1] = 5
        before = np.zeros((2, 2, 2), dtype=np.int64)
        before[0, 0, 0] = past
        r = np.zeros((2, 2, 2), dtype=np.int64)
        r[0, 0, 0] = 5
        live = planted(simulation, 1, now, before, r)
        a_next, r_next = step_once(simulation, live)
        assert int(a_next[0, 0, 0]) == expected
        assert int(r_next[0, 0, 0]) == 5


def test_c_lights_pair_is_the_first_builds_integers_bit_for_bit():
    """BUILD.md (c): on the first build's random chain the step at light's pair [1, 1] gives the
    same total, quotient and remainder as the line 3 a_next + r' = S_6 - 3 a_before + r."""
    world = parse_nature_beam_world(chain_world())
    simulation = DetectorLawSimulation(world)
    assert world.families[0].pair == LIGHT_PAIR
    assert np.all(simulation.kind_num[0] == 1) and np.all(simulation.kind_den[0] == 1)
    rng = np.random.default_rng(7)
    now = rng.integers(-UNIT, UNIT, size=(80, 1, 1), dtype=np.int64)
    before = rng.integers(-UNIT, UNIT, size=(80, 1, 1), dtype=np.int64)
    remainder = rng.integers(0, 3, size=(80, 1, 1), dtype=np.int64)
    live = planted(simulation, 0, now, before, remainder)
    live.age = 1000  # past the grace: the lamp's Nodes read their own record
    total = simulation._neighbours(now, live.ports, None) - 3 * before + remainder
    expected_next = np.floor_divide(total, 3)
    expected_remainder = total - 3 * expected_next
    a_next, r_next = step_once(simulation, live)
    free = ~simulation.absorbing
    assert np.array_equal(a_next[free], expected_next[free])
    assert np.array_equal(r_next[free], expected_remainder[free])


def checkerboard_seed(n: int) -> tuple[np.ndarray, np.ndarray]:
    """The seed of massive_corner_stability.py: a smooth 2^20 cosine along x plus one unit of
    checkerboard, the cosine's table taken at the integers (the phase table's scale 256)."""
    x, y, z = np.meshgrid(*[np.arange(n)] * 3, indexing="ij")
    checker = (x + y + z) % 2 * 2 - 1
    # cos(2 pi x / 6) at the six residues, in the unit 2^20: 1, 1/2, -1/2, -1, -1/2, 1/2
    table = np.array([UNIT, UNIT // 2, -(UNIT // 2), -UNIT, -(UNIT // 2), UNIT // 2], dtype=np.int64)
    smooth = table[x % 6]
    before = smooth + checker
    # a_now = smooth x cos(0.3) (0.9553, the integer 1001 / 1048 to 4 digits) - checker
    now = np.floor_divide(smooth * 1001, 1048) - checker
    return now.astype(np.int64), before.astype(np.int64)


def test_d_the_conserved_form_holds_to_the_remainders_jitter():
    """BUILD.md (d): on a periodic 6^3 board at [128, 129] and at [1600, 1618] the form I stays
    within 10^-3 of its start over 200 intervals (measured: 3 x 10^-6) and the amplitude stays
    bounded (below 2 x 2^20); the books read the form under the key (GAMEBOARD). The edge case:
    light's pair [1, 1] on the same seed keeps the checkerboard component at its one unit (the
    double root's stationary alternation: the seed's checkerboard carries no velocity, so the
    secular solution of DESIGN.md 2.1 is not excited; the growing form is the withdrawn
    self-term form (A), not built), and the massive kind keeps it below 40 units (measured 11
    and 18)."""
    now, before = checkerboard_seed(6)
    x, y, z = np.meshgrid(*[np.arange(6)] * 3, indexing="ij")
    checker = (x + y + z) % 2 * 2 - 1
    periodic = {"x": "periodic", "y": "periodic", "z": "periodic"}
    for pair in ([128, 129], [1600, 1618]):
        document = massive_world([6, 6, 6], periodic, pair)
        document["age_bound"] = 100000
        world = parse_nature_beam_world(document)
        simulation = DetectorLawSimulation(world)
        live = planted(simulation, 1, now, before, np.zeros((6, 6, 6), dtype=np.int64))
        start = simulation.record_form(live)
        assert start > 0
        peak = 0
        projection = 0
        for _ in range(200):
            step_once(simulation, live)
            peak = max(peak, int(np.abs(live.now).max()))
            projection = max(projection, abs(int(np.sum(live.now * checker)) // 216))
            assert abs(simulation.record_form(live) - start) < start // 1000
        assert peak < 2 * UNIT
        assert projection < 40
        simulation.records[live.identity] = live
        assert simulation.books()["families"]["matter"]["form"] == simulation.record_form(live)
        # light's pair on the same seed: the checkerboard's stationary alternation, one unit
        light = planted(simulation, 0, now, before, np.zeros((6, 6, 6), dtype=np.int64))
        light.age = 1000
        for _ in range(200):
            step_once(simulation, light)
            assert abs(int(np.sum(light.now * checker)) // 216) == 1


def test_m_the_massive_kinds_faces_are_periodic_by_default_and_a_zero_face_when_open():
    """BUILD.md (m): on a 5 x 1 x 1 board whose world `boundary` is open on x the massive kind
    wraps on x by default (Node 0 reads Node 4 as its -x neighbour); with faces {"x": "open"}
    the neighbour beyond the face reads 0."""
    for faces, expected in ((None, 9), ({"x": "open"}, 0)):
        world = parse_nature_beam_world(
            massive_world([5, 1, 1], {"x": "open", "y": "periodic", "z": "periodic"}, [1, 2], faces)
        )
        simulation = DetectorLawSimulation(world)
        now = np.array([0, 0, 0, 0, 9]).reshape(5, 1, 1)
        zero = np.zeros((5, 1, 1), dtype=np.int64)
        live = planted(simulation, 1, now, zero, zero)
        a_next, r_next = step_once(simulation, live)
        # at Node 0: the total num S_6 = 1 x (a_W + a_E + 4 x 0) = a_W, divided by 6
        total = 6 * int(a_next[0, 0, 0]) + int(r_next[0, 0, 0])
        assert total == expected
    assert world.kind_periodic(1) == (False, True, True)
    assert world.kind_periodic(0) == (False, True, True)
    default = parse_nature_beam_world(massive_world([5, 1, 1], "open", [1, 2]))
    assert default.kind_periodic(1) == (True, True, True)
    assert default.kind_periodic(0) == (False, False, False)


def run_chain_digests() -> dict[str, str]:
    lines: list[dict] = []
    world = parse_nature_beam_world(chain_world())
    simulation = DetectorLawSimulation(world, observer=lines.append)
    books = []
    for _ in range(600):
        simulation.step()
        books.append(simulation.books())
    events = "\n".join(json.dumps(line) for line in lines).encode()
    state = json.dumps(dict(simulation.snapshot_stream()), sort_keys=True).encode()
    audit = json.dumps(books, sort_keys=True).encode()
    return {
        "events": hashlib.sha256(events).hexdigest(),
        "state": hashlib.sha256(state).hexdigest(),
        "audit": hashlib.sha256(audit).hexdigest(),
    }


def test_p_the_light_record_is_byte_identical_without_the_key():
    """BUILD.md (p): the first build's chain world over 600 intervals gives the digests read at
    the head f4a3971a before any line of the build was written."""
    assert run_chain_digests() == {
        "events": "f6b6f273d08c0a2d278fff1b2f4967ceb48e8d5b7a906d7351f86d142080372d",
        "state": "9787e732df52846928e55c7466f979bfbf119b40f5e1f62db0b1269f24f7e962",
        "audit": "1000ac3f0b5d84f26958d70cc75e9c2484ff697e45418a7a83720689fe48535a",
    }


def test_q_the_loaders_refusals_name_the_key():
    """BUILD.md (q): the step's keys refused one by one, each naming the key."""
    base = massive_world([4, 4, 4], "open", [2, 3])
    without_key = json.loads(json.dumps(base))
    without_key["massive_record"] = False
    with pytest.raises(ValueError, match="pair is refused without the world key"):
        parse_nature_beam_world(without_key)
    reversed_pair = json.loads(json.dumps(base))
    reversed_pair["families"][1]["pair"] = [3, 2]
    with pytest.raises(ValueError, match="den >= num"):
        parse_nature_beam_world(reversed_pair)
    faces_on_light = json.loads(json.dumps(base))
    faces_on_light["families"][0]["faces"] = {"x": "open"}
    with pytest.raises(ValueError, match="faces is refused on light's kind"):
        parse_nature_beam_world(faces_on_light)
    bad_face = json.loads(json.dumps(base))
    bad_face["families"][1]["faces"] = {"x": "closed"}
    with pytest.raises(ValueError, match="faces must be an object"):
        parse_nature_beam_world(bad_face)
    clocked = json.loads(json.dumps(base))
    clocked["families"][1]["phase_per_link"] = [1, 2]
    with pytest.raises(ValueError, match="clock is its gap"):
        parse_nature_beam_world(clocked)
    no_law = json.loads(json.dumps(base))
    no_law["detector_law"] = False
    with pytest.raises(ValueError, match="massive_record needs detector_law"):
        parse_nature_beam_world(no_law)
    not_bool = json.loads(json.dumps(base))
    not_bool["massive_record"] = 1
    with pytest.raises(ValueError, match="massive_record must be true or false"):
        parse_nature_beam_world(not_bool)
    lamp_on_kind = json.loads(json.dumps(base))
    lamp_on_kind["measured"] = [
        {
            "position": [1, 1, 1],
            "family": "matter",
            "amount": 4,
            "phase": 0,
            "momentum": [0, 0, 0],
            "fixed": True,
            "lamp": {"rate": [1, 40], "wheel": [1, 64], "train": 2},
        }
    ]
    with pytest.raises(ValueError, match="lamp on the massive kind"):
        parse_nature_beam_world(lamp_on_kind)
    # light's kind written out, [1, 1], is a value and not a massive kind
    written = json.loads(json.dumps(base))
    written["families"][1]["pair"] = [1, 1]
    written["families"][1]["phase_per_link"] = [77, 25]
    world = parse_nature_beam_world(written)
    assert not world.families[1].massive_kind


def test_r_the_records_keys_under_the_key_and_none_without_it():
    """BUILD.md (r): the identity under `hypotheses`, the families' pair and faces and the books'
    form under the key; nothing of them without it (the first build's world)."""
    world = parse_nature_beam_world(massive_world([4, 4, 4], "open", [2, 3], {"z": "open"}))
    assert MASSIVE_RECORD_RULE in world.hypotheses
    assert world.families[1].pair == (2, 3) and world.families[1].massive_kind
    assert world.families[1].faces == (True, True, False)
    simulation = DetectorLawSimulation(world)
    assert "form" in simulation.books()["families"]["matter"]
    plain = parse_nature_beam_world(chain_world())
    assert MASSIVE_RECORD_RULE not in plain.hypotheses
    assert plain.families[0].faces is None
    assert "form" not in DetectorLawSimulation(plain).books()["families"]["light"]
