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
from fractions import Fraction

import numpy as np
import pytest

from event_universe.diagnostics.massive_record_margin import block_margin, check_margins
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


# The block (STEP 3 of the build: BUILD.md section 6, (e) to (l))


def block_world(
    shape: list[int],
    boundary: object,
    kind: list[int],
    blocks: list[dict],
    light_lamp: dict | None = None,
    ticks: int = 100,
    faces: dict[str, str] | None = None,
) -> dict:
    """A world of the massive kind `matter` with blocks (measured events of `matter` with
    `side`), a light family with the chain test's clock [77, 25] (the period 20.8 intervals,
    lambda 12 Links), and optionally a lamp of light at a Node."""
    matter: dict = {"name": "matter", "quantum": 1, "pair": kind}
    if faces is not None:
        matter["faces"] = faces
    measured: list[dict] = []
    if light_lamp is not None:
        measured.append(light_lamp)
    for block in blocks:
        entry = {
            "position": block["position"],
            "family": "matter",
            "amount": block.get("amount", 1),
            "phase": 0,
            "momentum": block.get("momentum", [0, 0, 0]),
            "fixed": True,
            "side": block["side"],
            "pair": block["pair"],
        }
        for key in (
            "coupling",
            "wheel",
            "seed",
            "absorbing",
            "cavity",
            "ramp",
            "margin",
            "emits",
            "held",
        ):
            if key in block:
                entry[key] = block[key]
        measured.append(entry)
    return {
        "law": "beam",
        "model_id": "beam-massive-record-block-v1",
        "shape": shape,
        "boundary": boundary,
        "ticks": ticks,
        "K": 1073741824,
        "N": 64,
        "release": [1, 128],
        "suspension": 0,
        "clock_stamp": True,
        "detector_law": True,
        "massive_record": True,
        "directions": [],
        "families": [{"name": "light", "quantum": 1, "phase_per_link": [77, 25]}, matter],
        "measured": measured,
        "detectors": [],
    }


def lamp_at(x: int, amount: int = 1, train: int = 4) -> dict:
    return {
        "position": [x, 0, 0],
        "family": "light",
        "amount": amount,
        "phase": 0,
        "momentum": [0, 0, 0],
        "fixed": True,
        "directions": [[1, 0, 0]],
        "lamp": {"rate": [1, 1], "wheel": [2531, 4096], "directions": [[1, 0, 0]], "train": train},
    }


CHAIN = {"x": "open", "y": "periodic", "z": "periodic"}


def test_e_the_blocks_cells_and_its_pair_on_them():
    """BUILD.md (e): a block of side 3 at (2, 2, 2) on an open 8^3 board of the kind [800, 809]
    with the well [800, 800]: den reads 809 on every Node but the 27 cells, 800 there, num 800
    everywhere; the cells are the cube. The edge case: a pair that is no well is refused."""
    world = parse_nature_beam_world(
        block_world(
            [8, 8, 8], "open", [800, 809], [{"position": [2, 2, 2], "side": 3, "pair": [800, 800]}]
        )
    )
    simulation = DetectorLawSimulation(world)
    block = simulation.blocks[0]
    assert int(block.mask.sum()) == 27
    assert block.mask[2:5, 2:5, 2:5].all()
    den = simulation.kind_den[1]
    assert np.all(simulation.kind_num[1] == 800)
    assert np.all(den[block.mask] == 800) and np.all(den[~block.mask] == 809)
    assert block.own is not None and int(block.own.now[3, 3, 3]) == UNIT
    with pytest.raises(ValueError, match="no well of the kind's pair"):
        parse_nature_beam_world(
            block_world(
                [8, 8, 8], "open", [800, 809], [{"position": [2, 2, 2], "side": 3, "pair": [800, 810]}]
            )
        )


def test_f_the_blocks_drive_steps_its_cells_and_leaves_the_rows():
    """BUILD.md (f): a block of content 1 with P = 64 on x (the wall 3 Q S M = 192) steps at the
    intervals 3, 6, 9 with the remainder 0; with P = 70 at 3, 6, 9 with the remainders 18, 36,
    54 and at 11 with the remainder 2; the cells and the pair arrays move, the record's rows
    stay. The edge case: P = [112, 112, 112] and [64, 64, 64] refused by the pace bound,
    [64, 64, 0] admitted."""
    for momentum, ticks_and_remainders in (
        ([64, 0, 0], [(3, 0), (6, 0), (9, 0), (12, 0)]),
        ([70, 0, 0], [(3, 18), (6, 36), (9, 54), (11, 2)]),
    ):
        world = parse_nature_beam_world(
            block_world(
                [24, 1, 1],
                CHAIN,
                [800, 809],
                [
                    {
                        "position": [4, 0, 0],
                        "side": 3,
                        "pair": [800, 800],
                        "momentum": momentum,
                        "seed": 5,
                    }
                ],
                faces={"x": "open"},
            )
        )
        simulation = DetectorLawSimulation(world)
        block = simulation.blocks[0]
        assert block.wall == 192
        steps = []
        for _ in range(12):
            simulation.step()
            if block.hop != (0, 0, 0):
                steps.append((simulation.tick, block.drive[0]))
        assert steps == ticks_and_remainders
        corner = 4 + len(steps)
        assert block.corner == [corner, 0, 0]
        assert block.mask[corner : corner + 3, 0, 0].all() and not block.mask[4, 0, 0]
        assert np.all(simulation.kind_den[1][corner : corner + 3, 0, 0] == 800)
        assert int(simulation.kind_den[1][4, 0, 0]) == 809
    # the rows stayed: the seeded record's rows are still centred on the old cells
    assert block.own is not None
    rows = block.own.now[:, 0, 0]
    assert abs(rows[4:7]).sum() > abs(rows[corner + 3 : corner + 6]).sum()
    for bad in ([112, 112, 112], [64, 64, 64]):
        with pytest.raises(ValueError, match="pace bound"):
            parse_nature_beam_world(
                block_world(
                    [24, 1, 1],
                    CHAIN,
                    [800, 809],
                    [{"position": [4, 0, 0], "side": 3, "pair": [800, 800], "momentum": bad}],
                )
            )
    parse_nature_beam_world(
        block_world(
            [24, 1, 1],
            CHAIN,
            [800, 809],
            [{"position": [4, 0, 0], "side": 3, "pair": [800, 800], "momentum": [64, 64, 0]}],
        )
    )


def coupled_chain(
    g: list[int], absorbing: bool = False, wheel: int | None = None, seed: int = 0
) -> dict:
    """The chain of (g): 400 Nodes, the kind [156, 157], a block of side 12 with the well
    [314, 315] at x = 200, G [1, 1], the lamp at x = 40 with a train of 4 periods."""
    block: dict = {
        "position": [200, 0, 0],
        "side": 12,
        "pair": [314, 315],
        "coupling": {"G": [1, 1], "g": g},
        "seed": seed,
        "absorbing": absorbing,
    }
    if wheel is not None:
        block["wheel"] = wheel
    return block_world(
        [400, 1, 1], CHAIN, [156, 157], [block], lamp_at(40), ticks=700, faces={"x": "open"}
    )


PERIODIC_CHAIN = {"x": "periodic", "y": "periodic", "z": "periodic"}


def six_reads(row: np.ndarray) -> np.ndarray:
    """The six directed reads of the rule on a periodic board (an axis of extent 1 reads the
    Node itself twice), summed: the S_6 of MASSIVE_RECORD.md section 3."""
    total = np.zeros(row.shape, dtype=object)
    for axis in range(3):
        for shift in (1, -1):
            total = total + np.roll(row, shift, axis=axis)
    return total


def conserved_form(a_next: np.ndarray, a_now: np.ndarray, weight: np.ndarray) -> Fraction:
    """The form I of section 3 with a Node weight den / num and the Link weight one:
    SUM_i w_i (a_next^2 + a_now^2) - SUM_i a_next,i S_6(a_now)_i / 3."""
    nodes = np.sum(weight * (a_next * a_next + a_now * a_now))
    links = np.sum(a_next * six_reads(a_now))
    return Fraction(nodes) - Fraction(links, 3)


def rows(live: LiveRecord | None, shape: tuple[int, ...]) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """A record's three columns as exact integers (zeros for a record not yet formed)."""
    if live is None:
        zero = np.zeros(shape, dtype=object)
        return zero, zero, zero
    return live.now.astype(object), live.before.astype(object), live.remainder.astype(object)


def light_packet(shape: tuple[int, ...], amplitude: int = 1 << 16) -> tuple[np.ndarray, np.ndarray]:
    """A wave packet of light on the chain, moving +x at c = 1 / sqrt(3): the two columns
    of MASSIVE_RECORD.md's script `massive_conserved_form.py` at integer amplitude."""
    x = np.arange(shape[0], dtype=np.float64)
    step = 1.0 / np.sqrt(3.0)
    now = amplitude * np.exp(-((x - 100) ** 2) / 200.0) * np.cos(0.2 * (x - 100))
    before = amplitude * np.exp(-((x - 100 + step) ** 2) / 200.0) * np.cos(0.2 * (x - 100 + step))
    return np.rint(now).astype(np.int64).reshape(shape), np.rint(before).astype(np.int64).reshape(shape)


def coupled_invariant(g: list[int]) -> tuple[int, Fraction, Fraction, bool]:
    """The chain of (g) stepped 400 intervals with the identity of section 7 asserted on each:
    returns the count of intervals with a nonzero cross term, light's form at the start and at
    the end, and whether the response's rows stayed 0."""
    block: dict = {
        "position": [200, 0, 0],
        "side": 12,
        "pair": [314, 315],
        "coupling": {"G": [1, 1], "g": g},
    }
    document = block_world([400, 1, 1], PERIODIC_CHAIN, [156, 157], [block], ticks=500)
    document["age_bound"] = 100000
    simulation = DetectorLawSimulation(parse_nature_beam_world(document))
    # the test's device: the completion's wheel raised so the packet lives the 400
    # intervals (a lamp's record clicks at the block at its rung, test (i))
    simulation.wheel = 1 << 20
    block_live = simulation.blocks[0]
    shape = simulation.shape
    now, before = light_packet(shape)
    light = planted(simulation, 0, now, before, np.zeros(shape, dtype=np.int64))
    simulation.records[light.identity] = light
    g_n, g_d = g
    num_m = simulation.kind_num[1].ravel().tolist()
    den_m = simulation.kind_den[1].ravel().tolist()
    weight_m = np.array([Fraction(d, n) for n, d in zip(num_m, den_m, strict=True)], dtype=object)
    weight_m = weight_m.reshape(shape)
    inverse_walls = np.array([Fraction(1, 3 * n * g_d) for n in num_m], dtype=object).reshape(shape)
    weight_l = np.full(shape, Fraction(1), dtype=object)
    cells = block_live.mask
    alpha = Fraction(g_n, g_d) * Fraction(315, 314)

    def invariant(response: LiveRecord | None) -> Fraction:
        x_n, x, _ = rows(response, shape)
        y_n, y, _ = rows(light, shape)
        cross = Fraction(g_n, g_d) * np.sum((weight_m * (x_n - x) * (y_n - y))[cells])
        return conserved_form(x_n, x, weight_m) + alpha * conserved_form(y_n, y, weight_l) + cross

    previous = invariant(None)
    crosses = 0
    silent = True
    first_light = conserved_form(*rows(light, shape)[:2], weight_l)
    for _ in range(400):
        response = block_live.responses.get(light.identity)
        x_n0, x_b, r_m = rows(response, shape)
        y_n0, y_b, r_l = rows(light, shape)
        simulation.step()
        assert light.identity in simulation.records
        response = block_live.responses.get(light.identity)
        x_n, _, r_m2 = rows(response, shape)
        y_n, _, r_l2 = rows(light, shape)
        silent = silent and (response is None or not np.any(response.now))
        light_remainders = Fraction(int(np.sum((y_n - y_b) * (r_l - r_l2))), 3)
        if g_n == 0:
            # light's own identity, the form I with the remainders' term (section 3)
            assert (
                conserved_form(y_n, y_n0, weight_l) - conserved_form(y_n0, y_b, weight_l)
                == light_remainders
            )
            continue
        current = invariant(response)
        massive_term = np.sum((x_n - x_b) * (r_m - r_m2) * inverse_walls)
        assert current - previous == massive_term + alpha * light_remainders, simulation.tick
        previous = current
        if np.any(((x_n - x_n0) * (y_n - y_n0))[cells]):
            crosses += 1
    last_light = conserved_form(*rows(light, shape)[:2], weight_l)
    return crosses, first_light, last_light, silent


def test_g_the_coupling_both_ways_conserves_the_schemes_exact_invariant():
    """BUILD.md (g), MASSIVE_RECORD.md section 7 (MUSTs A and B): on a periodic chain of 400
    Nodes (the kind [156, 157], a block of side 12 with the well [314, 315] at x = 200, G [1, 1])
    a planted light packet and the block's response to it, 400 intervals: at g = 1 / 20 and at
    g = 1 / 5 the identity J(t) - J(t - 1) = SUM_i (x_next - x_before)_i (r - r')_i / (3 num_i
    g_d) + alpha SUM_i (y_next - y_before)_i (r - r')_i / (3 G_d) holds EXACTLY on every
    interval (J = I_m + alpha I_l + (g_n / g_d) SUM_cells w_i dx_i dy_i, alpha = g W_in / G, the
    forms in exact rationals; the remainders' term of each row with its own folded wall the
    whole correction, no tolerance), the cross term nonzero on some interval (the coupling's
    grain, a GAMEBOARD reading), and light's own form moved by more than 10 percent between
    the packet's arrival and the end. The edge case: g = [0, 1] leaves the response's rows 0
    and light's form its own identity, I_l(t) - I_l(t - 1) = SUM (y_next - y_before)(r - r') / 3."""
    crosses, first, last, silent = coupled_invariant([0, 1])
    assert silent
    for g in ([1, 20], [1, 5]):
        crosses, first, last, silent = coupled_invariant(g)
        assert crosses > 0
        assert not silent
        assert abs(last - first) > Fraction(1, 10) * abs(first)


def test_h_a_seeded_block_emits_one_record_per_cycle_paying_the_quantum():
    """BUILD.md (h): a seeded block (the kind [156, 157], the well [314, 315], G [1, 1], g
    [1, 500]: at G g = 0.2 the emitted light's back-drive breaks the mode's cycles within one
    period on the chain, so the weak coupling keeps them) that emits light holding 3 units of
    it: three births, one at each of its first three cycles (its mode's period about 60
    intervals: the clicks at 45, 107, 167, 227, 287), each paying 1, the books balanced at every
    tick; the fourth and fifth cycles birth nothing. The edge case: `emits` without held content of that family is
    refused at load."""
    block = {
        "position": [100, 0, 0],
        "side": 12,
        "pair": [314, 315],
        "coupling": {"G": [1, 1], "g": [1, 500]},
        "emits": "light",
        "held": {"light": 3},
    }
    world = parse_nature_beam_world(
        block_world([240, 1, 1], CHAIN, [156, 157], [block], ticks=300, faces={"x": "open"})
    )
    lines: list[dict] = []
    simulation = DetectorLawSimulation(world, observer=lines.append)
    for _ in range(300):
        simulation.step()
        assert simulation.books()["balanced"], simulation.tick
    births = [line for line in lines if line["event"] == "birth"]
    cycles = [line for line in lines if line["event"] == "click"]
    assert len(cycles) >= 4
    assert len(births) == 3
    assert [line["cycle"] for line in births] == [1, 2, 3]
    assert simulation.held[0][0] == 0
    assert simulation.ledger.held_spent[0] == 3 and simulation.ledger.transit_released[0] == 3
    unheld = dict(block)
    del unheld["held"]
    with pytest.raises(ValueError, match="holds none of it"):
        parse_nature_beam_world(block_world([240, 1, 1], CHAIN, [156, 157], [unheld]))


def test_i_the_click_at_the_wheel_stamped_with_the_blocks_count():
    """BUILD.md (i): on the coupled chain with W = 64 the block's first rung on the lamp's
    record is crossed between 10 and 60 intervals after the train's front reaches its near
    face (about 40 + 160 / c = 317), the crossing stamped with the block's count; a gather
    line whose chosen cell is the block carries `clock` equal to that count. The edge case:
    W = 4096 (the rung 1 / 4096 of the norm) crosses no later than W = 64 and after the first
    motion (the edge case as first written, W = 1 stamping the first motion, read the wheel
    backwards: W = 1 is the whole norm)."""
    for wheel, window in ((64, (10, 60)), (4096, (1, 60))):
        world = parse_nature_beam_world(coupled_chain([1, 10], wheel=wheel))
        lines: list[dict] = []
        simulation = DetectorLawSimulation(world, observer=lines.append)
        block = simulation.blocks[0]
        record = None
        first_motion = None
        rung = None
        for _ in range(700):
            simulation.step()
            if simulation.tick == 5:
                record = next(live for live in simulation.records.values() if live.family == 0)
            if record is None or record.identity not in simulation.records:
                continue
            response = block.responses.get(record.identity)
            if response is not None and first_motion is None and np.any(response.now[block.mask]):
                first_motion = simulation.tick
            if rung is None and record.first_rung[block.cell] is not None:
                rung = record.first_rung[block.cell]
                assert (record.identity, block.cell) in simulation.rung_counts
                assert simulation.rung_counts[(record.identity, block.cell)] == block.count
        assert first_motion is not None and rung is not None
        assert window[0] <= rung - first_motion <= window[1], (rung, first_motion)
        if wheel == 64:
            coarse = rung
        else:
            assert rung <= coarse
        for gather in (line for line in lines if line["event"] == "gather"):
            chosen = gather["chosen"]
            if chosen is not None and chosen[0][0] == "measured:1":
                assert gather["clock"] <= block.count


def test_j_a_seeded_block_at_rest_counts_its_cycles():
    """BUILD.md (j): a seeded block (the kind [800, 809], the well [800, 800], s = 10) on a
    periodic 32^3 board, no light: over 500 intervals its count equals the upward zero crossings
    of its summed record on the `block` lines, one `click` line per count, the mean period
    between 30 and 80 intervals. The edge case: seed 0 counts nothing."""
    for seed, expected_counts in ((UNIT, None), (0, 0)):
        document = block_world(
            [32, 32, 32],
            {"x": "periodic", "y": "periodic", "z": "periodic"},
            [800, 809],
            [
                {
                    "position": [11, 11, 11],
                    "side": 10,
                    "pair": [800, 800],
                    "seed": seed,
                    "margin": "control",
                }
            ],
            ticks=500,
        )
        document["age_bound"] = 100000
        world = parse_nature_beam_world(document)
        lines: list[dict] = []
        simulation = DetectorLawSimulation(world, observer=lines.append)
        for _ in range(500):
            simulation.step()
        block = simulation.blocks[0]
        sums = [line["sum"] for line in lines if line["event"] == "block"]
        crossings = sum(1 for a, b in zip(sums, sums[1:], strict=False) if a <= 0 < b)
        clicks = [line for line in lines if line["event"] == "click"]
        if expected_counts is None:
            assert block.count == crossings == len(clicks) >= 6
            assert 30 <= 500 / block.count <= 80
            assert [line["clock"] for line in clicks] == list(range(1, block.count + 1))
        else:
            assert block.count == 0 and not clicks


def test_k_the_take_only_for_an_absorbing_block():
    """BUILD.md (k): the coupled chain with the block declared absorbing: light's row at every
    cell is 0 after every step, the Ports book an offer into the block's cell and the record
    clicks at the block with `clock` the block's count; with the block a clock body light's
    row at the cells is nonzero after the front and the record's far face reads it. The edge
    case: `absorbing` with `emits` is refused at load."""
    for absorbing in (True, False):
        world = parse_nature_beam_world(coupled_chain([1, 10], absorbing=absorbing, seed=UNIT))
        lines: list[dict] = []
        simulation = DetectorLawSimulation(world, observer=lines.append)
        block = simulation.blocks[0]
        record = None
        seen_at_cells = False
        for _ in range(1200):
            simulation.step()
            if simulation.tick == 5:
                record = next(live for live in simulation.records.values() if live.family == 0)
            if record is not None and record.identity in simulation.records:
                at_cells = record.now[block.mask]
                if absorbing:
                    assert not np.any(at_cells)
                elif np.any(at_cells):
                    seen_at_cells = True
        gathers = [
            line for line in lines if line["event"] == "gather" and line["record"] == record.identity
        ]
        assert len(gathers) == 1
        chosen = gathers[0]["chosen"]
        face = simulation.cell_names.index("face:+x")
        if absorbing:
            # the block took the train: nothing reached the far face; its Ports
            # booked the offer; a click at the block carries the block's count
            # (on a chain the lamp's own cell may win the ladder, the afterglow
            # of one dimension, the first build's)
            assert record.pointers[block.cell] > 0 and record.pointers[face] == 0
            if chosen is not None and chosen[0][0] == "measured:1":
                assert gathers[0]["clock"] <= block.count
        else:
            assert seen_at_cells
            assert record.pointers[face] > 0
    with pytest.raises(ValueError, match="absorbing block emits nothing"):
        parse_nature_beam_world(
            block_world(
                [240, 1, 1],
                CHAIN,
                [156, 157],
                [
                    {
                        "position": [100, 0, 0],
                        "side": 12,
                        "pair": [314, 315],
                        "absorbing": True,
                        "emits": "light",
                        "held": {"light": 3},
                    }
                ],
            )
        )


def test_l_the_index_in_motion_is_the_drives_pair():
    """BUILD.md (l): a block of content 1 with P = 64 on x (K = 3) carries g as [3, 2] (the
    pair [K^2, K^2 - 3] = [9, 6] reduced); at rest [1, 1]; with P = [64, 64, 0] the pair
    [36864, 12288] = [3, 1]. The edge case: K = 1 (P = 192) is refused by the pace bound."""
    for momentum, expected in (([64, 0, 0], (3, 2)), ([0, 0, 0], (1, 1)), ([64, 64, 0], (3, 1))):
        world = parse_nature_beam_world(
            block_world(
                [24, 1, 1],
                CHAIN,
                [800, 809],
                [{"position": [4, 0, 0], "side": 3, "pair": [800, 800], "momentum": momentum}],
            )
        )
        simulation = DetectorLawSimulation(world)
        assert simulation.motion_pair(simulation.blocks[0]) == expected
    with pytest.raises(ValueError, match="pace bound"):
        parse_nature_beam_world(
            block_world(
                [24, 1, 1],
                CHAIN,
                [800, 809],
                [{"position": [4, 0, 0], "side": 3, "pair": [800, 800], "momentum": [192, 0, 0]}],
            )
        )


# The faces and the margin rule (STEP 4 of the build: BUILD.md section 6, (n) and (o))

PERIODIC = {"x": "periodic", "y": "periodic", "z": "periodic"}


def test_n_the_margin_rule_refuses_below_the_margin_and_prints_the_extent():
    """BUILD.md (n): (1) the s = 28 block of world (i-b) on the periodic 48^3 board is refused as
    a pin world naming x, the extent (about 7.9 Links) and the side needed (about 60 > 48), and
    admitted as a control (44 < 48); (2) a block of s = 20 whose cells lie 3 Links from an open
    massive face is refused as a control (3 < 5.7) naming the axis and the distance; (3) the
    kind [800, 809] with the well [800, 808] at s = 3 (far below the threshold) is refused: on a
    finite periodic box the unbound case reads as an extent beyond the board (261 Links against
    24), the refusal the margin's; (4) the extent printed for (i-a) on 48^3 is 5.73 within 0.05
    Links (the float scratch of the plan) and its mode 0.1105 (the design's 96^3 box 0.1107)."""
    for margin, admitted in (("pin", False), ("control", True)):
        document = block_world(
            [48, 48, 48],
            PERIODIC,
            [1600, 1618],
            [{"position": [10, 10, 10], "side": 28, "pair": [1600, 1609], "margin": margin}],
        )
        document["age_bound"] = 100000
        world = parse_nature_beam_world(document)
        if admitted:
            readings = check_margins(world)
            assert 7.8 < readings[0].extent < 8.1
            assert readings[0].axes[0][3] < 48
        else:
            with pytest.raises(ValueError, match="below the margin rule on x for a pin world"):
                check_margins(world)
    near = block_world(
        [48, 48, 48],
        PERIODIC,
        [800, 809],
        [{"position": [3, 14, 14], "side": 20, "pair": [800, 800], "margin": "control"}],
        faces={"x": "open"},
    )
    near["age_bound"] = 100000
    with pytest.raises(ValueError, match="cells lie 3 Links from a zero face"):
        check_margins(parse_nature_beam_world(near))
    shallow = block_world(
        [24, 24, 24],
        PERIODIC,
        [800, 809],
        [{"position": [10, 10, 10], "side": 3, "pair": [800, 808], "margin": "control"}],
    )
    shallow["age_bound"] = 100000
    with pytest.raises(ValueError, match="below the margin rule"):
        check_margins(parse_nature_beam_world(shallow))
    assert block_margin(parse_nature_beam_world(shallow), 0).extent > 100
    rest = block_world(
        [48, 48, 48],
        PERIODIC,
        [800, 809],
        [{"position": [14, 14, 14], "side": 20, "pair": [800, 800], "margin": "control"}],
    )
    rest["age_bound"] = 100000
    reading = check_margins(parse_nature_beam_world(rest))[0]
    assert abs(reading.extent - 5.73) < 0.05
    assert abs(reading.omega_b - 0.1105) < 0.0005
    assert abs(reading.omega_0 - 0.1493) < 0.0001
    assert reading.lines() and reading.to_record()["kind"] == "COMPUTATION"


def test_o_the_cavity_counts_the_separable_forms_cycles():
    """BUILD.md (o): a cavity of side 5 with the kind's own pair [800, 809] on a periodic 24^3
    board: the exact separable form cos omega = (800 / 809) cos(pi / 6), omega 0.5423, the
    period 11.58 intervals; over 1159 intervals the block's count between 99 and 101 (one
    interval's grain; measured 99), and its rows outside the cube 0 at every interval."""
    document = block_world(
        [24, 24, 24],
        PERIODIC,
        [800, 809],
        [{"position": [10, 10, 10], "side": 5, "pair": [800, 809], "cavity": True, "margin": "control"}],
    )
    document["age_bound"] = 100000
    world = parse_nature_beam_world(document)
    simulation = DetectorLawSimulation(world)
    block = simulation.blocks[0]
    assert block.own is not None
    for _ in range(1159):
        simulation.step()
        assert not np.any(block.own.now[~block.mask])
    assert 99 <= block.count <= 101
