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
import math
from fractions import Fraction

import numpy as np
import pytest

from event_universe.core.phase import phase_cosines
from event_universe.diagnostics.massive_record_margin import (
    block_margin,
    bound_mode,
    check_margins,
    profile_check,
)
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
        "amplitude_bound": 1 << 32,
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
    the head f4a3971a before any line of the build was written: the state and the audit
    the witness that the rows are byte for byte; the events' digest moved ONCE, at the GO's
    fold (BUILD.md section 14), by the two fields added to every gather line (`click_at`,
    `clock_source`; Reviewer 3's line 2 and key (i)), and the audit's digest once, by issue
    #1086's momentum books (the blocks' held momentum, the transit and escape not accounted,
    the scope of `balanced` named), every other field byte for byte."""
    assert run_chain_digests() == {
        "events": "9e29e924a2f7ba63d34d9fb1bdaa30123006a554e42781ecf29804664c3832b3",
        "state": "9787e732df52846928e55c7466f979bfbf119b40f5e1f62db0b1269f24f7e962",
        "audit": "5cd95d38d58d8ccb1da6808b9da635fdc905786722f5bf9a05f0d7f2036374e1",
    }


def test_q_the_loaders_refusals_name_the_key():
    """BUILD.md (q): the step's keys refused one by one, each naming the key."""
    base = massive_world([4, 4, 4], "open", [2, 3])
    without_key = json.loads(json.dumps(base))
    without_key["massive_record"] = False
    del without_key["amplitude_bound"]
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
    turned = json.loads(json.dumps(base))
    turned["families"][1]["phase_per_link"] = 5
    with pytest.raises(ValueError, match="never a declared turn"):
        parse_nature_beam_world(turned)
    # the pair form is the family's clock, admitted (test (z): a matter lamp)
    clocked = json.loads(json.dumps(base))
    clocked["families"][1]["phase_per_link"] = [1, 2]
    assert parse_nature_beam_world(clocked).families[1].phase_per_age == (1, 2)
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
            "start",
            "margin",
            "emits",
            "held",
            "own_grace",
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
        "amplitude_bound": 1 << 32,
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
    # a raised pair is a BARRIER (DECLARATIONS.md section 15 M1-6): admitted, no own record,
    # its seed and clock keys refused; the kind's own pair without `cavity` refused
    barrier = parse_nature_beam_world(
        block_world(
            [8, 8, 8], "open", [800, 809], [{"position": [2, 2, 2], "side": 3, "pair": [800, 810]}]
        )
    )
    assert barrier.measured[0].block is not None and barrier.measured[0].block.seed == 0
    assert DetectorLawSimulation(barrier).blocks[0].own is None
    with pytest.raises(ValueError, match="refused on a barrier"):
        parse_nature_beam_world(
            block_world(
                [8, 8, 8],
                "open",
                [800, 809],
                [{"position": [2, 2, 2], "side": 3, "pair": [800, 810], "seed": 5}],
            )
        )
    with pytest.raises(ValueError, match="is the kind's own pair"):
        parse_nature_beam_world(
            block_world(
                [8, 8, 8], "open", [800, 809], [{"position": [2, 2, 2], "side": 3, "pair": [800, 809]}]
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


def coupled_invariant(g: list[int], G: list[int] | None = None) -> tuple[int, Fraction, Fraction, bool]:
    """The chain of (g) stepped 400 intervals with the identity of section 7 asserted on each:
    returns the count of intervals with a nonzero cross term, light's form at the start and at
    the end, and whether the response's rows stayed 0. G other than [1, 1] puts G_n in alpha's
    denominator and G_d in light's wall (the scale 3 L g_d G_n, Reviewer 3's token)."""
    G = G or [1, 1]
    block: dict = {
        "position": [200, 0, 0],
        "side": 12,
        "pair": [314, 315],
        "coupling": {"G": G, "g": g},
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
    G_n, G_d = G
    assert simulation.light_scale == G_d
    num_m = simulation.kind_num[1].ravel().tolist()
    den_m = simulation.kind_den[1].ravel().tolist()
    weight_m = np.array([Fraction(d, n) for n, d in zip(num_m, den_m, strict=True)], dtype=object)
    weight_m = weight_m.reshape(shape)
    inverse_walls = np.array([Fraction(1, 3 * n * g_d) for n in num_m], dtype=object).reshape(shape)
    weight_l = np.full(shape, Fraction(1), dtype=object)
    cells = block_live.mask
    alpha = Fraction(g_n, g_d) * Fraction(315, 314) * Fraction(G_d, G_n)

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
        light_remainders = Fraction(int(np.sum((y_n - y_b) * (r_l - r_l2))), 3 * G_d)
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
    for g, G in (([1, 20], None), ([1, 5], None), ([1, 20], [2, 3])):
        crosses, first, last, silent = coupled_invariant(g, G)
        assert crosses > 0
        assert not silent
        assert abs(last - first) > Fraction(1, 10) * abs(first)


def test_h_a_seeded_block_emits_one_record_per_cycle_paying_the_quantum():
    """BUILD.md (h): a seeded block (the kind [156, 157], the well [314, 315], G [1, 1], g
    [1, 500]: at G g = 0.2 the emitted light's back-drive breaks the mode's cycles within one
    period on the chain, so the weak coupling keeps them) that emits light: one birth at each
    of its cycles (its mode's period about 60 intervals: the clicks at 45, 107, 167, 227, 287),
    the record born at content 0 and consuming no stock (DECLARATIONS.md section 15 M1-2: the
    emission is the coupling's source term; no `held` on an emitter, a `held` book inert), the
    books balanced at every tick. The edge cases: an emitter without `own_grace` (N_s) is
    refused at load naming it; `own_grace` on a block that emits nothing is refused."""
    block = {
        "position": [100, 0, 0],
        "side": 12,
        "pair": [314, 315],
        "coupling": {"G": [1, 1], "g": [1, 500]},
        "emits": "light",
        "own_grace": 70,
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
    assert len(births) == len(cycles) - 1 or len(births) == len(cycles)
    assert [line["cycle"] for line in births] == list(range(1, len(births) + 1))
    assert all(live.content == 0 for live in simulation.records.values() if live.emitter == 0)
    assert simulation.ledger.held_spent[0] == 0 and simulation.ledger.transit_released[0] == 0
    ungraced = dict(block)
    del ungraced["own_grace"]
    with pytest.raises(ValueError, match="declares no `own_grace`"):
        parse_nature_beam_world(block_world([240, 1, 1], CHAIN, [156, 157], [ungraced]))
    silent = dict(block)
    del silent["emits"]
    with pytest.raises(ValueError, match="own_grace is refused on a block that emits nothing"):
        parse_nature_beam_world(block_world([240, 1, 1], CHAIN, [156, 157], [silent]))


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
                        "own_grace": 70,
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


# The series' two keys of step 5 (BUILD.md section 4 step 7 and section 5 (v-m))


def test_s_the_drives_start_and_the_ramp_counted_from_it():
    """The block key `start` (the pushing agent's declaration, like `ramp`): a block of side 3
    with the momentum 64 on x (one Link every three intervals against the wall 192) and
    `start` 30 has not moved by interval 30, has stepped once by interval 33 and ten times by
    interval 60; with `ramp` 30 as well the ramp counts from the start (no step before 30,
    the momentum reaching 64 at interval 60). The edge case: `start` below 0 is refused."""
    for extra, expected in (
        ({"start": 30}, {30: 0, 33: 1, 60: 10}),
        ({"start": 30, "ramp": 30}, {30: 0, 45: None}),
    ):
        document = block_world(
            [64, 8, 8],
            PERIODIC_CHAIN,
            [800, 809],
            [{"position": [10, 2, 2], "side": 3, "pair": [800, 800], "momentum": [64, 0, 0], **extra}],
            ticks=100,
        )
        document["age_bound"] = 100000
        simulation = DetectorLawSimulation(parse_nature_beam_world(document))
        block = simulation.blocks[0]
        steps: dict[int, int] = {}
        for _ in range(60):
            simulation.step()
            steps[simulation.tick] = block.corner[0] - 10
        for tick, count in expected.items():
            if count is not None:
                assert steps[tick] == count, (extra, tick, steps[tick])
        if "ramp" in extra:
            assert steps[30] == 0 and 0 < steps[45] < 5 and steps[60] > steps[45]
    refused = block_world(
        [64, 8, 8],
        PERIODIC_CHAIN,
        [800, 809],
        [{"position": [10, 2, 2], "side": 3, "pair": [800, 800], "momentum": [64, 0, 0], "start": -1}],
    )
    refused["age_bound"] = 100000
    with pytest.raises(ValueError, match="start"):
        parse_nature_beam_world(refused)


def test_t_the_mode_line_sums_lights_field_by_residue_class():
    """The world key `mode_axis` ("x"): the record's `mode` line per interval carries the
    three sums of light's total field over the Nodes whose x coordinate is 0, 1, 2 modulo 3,
    equal to the sums formed from the records' rows at that interval; on a chain of 30 with
    a planted packet the three sums are the packet's residue sums. The edge case:
    `mode_axis` without `massive_record` is refused, as is an axis not x, y or z."""
    document = block_world([30, 1, 1], PERIODIC_CHAIN, [800, 809], [], ticks=20)
    document["age_bound"] = 100000
    document["mode_axis"] = "x"
    lines: list[dict] = []
    simulation = DetectorLawSimulation(parse_nature_beam_world(document), observer=lines.append)
    now = np.arange(30, dtype=np.int64).reshape(30, 1, 1) * 7 - 100
    light = planted(simulation, 0, now, now, np.zeros((30, 1, 1), dtype=np.int64))
    simulation.records[light.identity] = light
    simulation.step()
    field = light.now.ravel().tolist()
    modes = [line for line in lines if line["event"] == "mode"]
    assert len(modes) == 1 and modes[0]["axis"] == "x"
    assert modes[0]["sums"] == [sum(field[r::3]) for r in range(3)]
    bad = dict(document)
    bad["mode_axis"] = "w"
    with pytest.raises(ValueError, match="mode_axis"):
        parse_nature_beam_world(bad)
    unkeyed = dict(document)
    del unkeyed["massive_record"]
    del unkeyed["amplitude_bound"]
    del unkeyed["measured"]
    unkeyed["measured"] = []
    with pytest.raises(ValueError, match="mode_axis"):
        parse_nature_beam_world(unkeyed)


# Reviewer 3's three MUSTs on step 2 (the Boss's 16:42Z) and his layer line (18:12Z)


def test_u_a_massive_record_never_completes_nor_clicks_as_escaped():
    """MUST 2: a massive record with zero motion after its train plus two intervals (a planted
    static level) does not complete; a light record with the same rows does. The block's own
    record and its responses are read by the block's clock and taken by nothing."""
    world = parse_nature_beam_world(
        massive_world([6, 1, 1], {"x": "open", "y": "periodic", "z": "periodic"}, [2, 3], {"x": "open"})
    )
    simulation = DetectorLawSimulation(world)
    level = np.full((6, 1, 1), 5, dtype=np.int64)
    massive = planted(simulation, 1, level, level, np.zeros((6, 1, 1), dtype=np.int64))
    light = planted(simulation, 0, level, level, np.zeros((6, 1, 1), dtype=np.int64))
    assert simulation._complete(light)
    assert not simulation._complete(massive)


def test_v_the_load_bound_of_a_pair_names_the_bound_and_the_pair():
    """MUST 3: a kind's pair whose rule total at the world's declared amplitude bound A reaches
    2^63 is refused at load naming the bound and the pair (A = 2^40 declared, [2^20, 2^20 + 1]:
    6 x 2^60 + ... above 2^63); [800, 809] is admitted; a block's pair with its g_d folded into
    the wall is checked with that scale ([800, 800] with g = [1, 2^20] refused at A = 2^40, with
    g = [1, 20] admitted). The world key (issue #1085, section 15 M1-10): a massive world
    without `amplitude_bound` is refused naming it; a seed above the bound is refused naming
    the bound and the pair (a seed of 2^60 at A = 2^32); the key without `massive_record`
    refused; a planted row above the bound stops the run at its interval."""
    big = 1 << 20
    document = massive_world([6, 6, 6], PERIODIC, [big, big + 1])
    document["age_bound"] = 100
    document["amplitude_bound"] = 1 << 40
    with pytest.raises(ValueError, match=r"num x 6 x A \+ 3 x den x \(A \+ 1\).*not below 2\^63"):
        parse_nature_beam_world(document)
    with pytest.raises(ValueError, match=r"\[1048576, 1048577\]"):
        parse_nature_beam_world(document)
    for g, admitted in (([1, big], False), ([1, 20], True)):
        world = block_world(
            [24, 24, 24],
            PERIODIC,
            [800, 809],
            [
                {
                    "position": [10, 10, 10],
                    "side": 3,
                    "pair": [800, 800],
                    "coupling": {"G": [1, 1], "g": g},
                }
            ],
        )
        world["age_bound"] = 100
        world["amplitude_bound"] = 1 << 40
        if admitted:
            parse_nature_beam_world(world)
        else:
            with pytest.raises(ValueError, match="with the coupling's denominator 1048576"):
                parse_nature_beam_world(world)
    unbounded = massive_world([6, 6, 6], PERIODIC, [800, 809])
    unbounded["age_bound"] = 100
    del unbounded["amplitude_bound"]
    with pytest.raises(ValueError, match="declares `amplitude_bound`"):
        parse_nature_beam_world(unbounded)
    ceiling = massive_world([6, 6, 6], PERIODIC, [800, 809])
    ceiling["age_bound"] = 100
    ceiling["amplitude_bound"] = 1 << 41
    with pytest.raises(ValueError, match="above the ceiling 2\\^40"):
        parse_nature_beam_world(ceiling)
    huge_seed = block_world(
        [24, 24, 24],
        PERIODIC,
        [800, 809],
        [{"position": [10, 10, 10], "side": 3, "pair": [800, 800], "seed": 1 << 60}],
    )
    huge_seed["age_bound"] = 100
    with pytest.raises(
        ValueError, match=r"above the world's amplitude bound A = 4294967296 on the pair"
    ):
        parse_nature_beam_world(huge_seed)
    bounded = massive_world([6, 6, 6], PERIODIC, [800, 809])
    bounded["age_bound"] = 100
    world = parse_nature_beam_world(bounded)
    simulation = DetectorLawSimulation(world)
    planted_row = planted(
        simulation,
        1,
        np.full((6, 6, 6), 1 << 33),
        np.zeros((6, 6, 6)),
        np.zeros((6, 6, 6)),
    )
    with pytest.raises(RuntimeError, match="above the world's declared amplitude bound"):
        simulation._advance(planted_row)


def test_w_the_form_on_a_chain_is_exact_with_the_remainders_term():
    """MUST 1's test: on the chain 6 x 1 x 1 (y and z folded, the Node reading itself twice on
    each) at the pair [2, 3], open on x, the form I of section 3 as the books read it
    (`record_form`, the weights L / num, L the numerators' lcm, here 2) changes by the
    remainders' term exactly on every interval: num x (I(t) - I(t - 1)) = L x SUM_i (a_next
    - a_before)_i (r - r')_i, integers, no tolerance, 60 intervals from random rows; the
    same on a periodic x."""
    for boundary, faces in ((CHAIN, {"x": "open"}), (PERIODIC_CHAIN, None)):
        document = massive_world([6, 1, 1], boundary, [2, 3], faces)
        document["age_bound"] = 1000
        simulation = DetectorLawSimulation(parse_nature_beam_world(document))
        rng = np.random.default_rng(7)
        now = rng.integers(-50, 51, size=(6, 1, 1)).astype(np.int64)
        before = rng.integers(-50, 51, size=(6, 1, 1)).astype(np.int64)
        live = planted(simulation, 1, now, before, np.zeros((6, 1, 1), dtype=np.int64))
        previous = simulation.record_form(live)
        for _ in range(60):
            a_before = live.before.astype(object)
            r = live.remainder.astype(object)
            simulation._advance(live)
            current = simulation.record_form(live)
            remainders = int(
                np.sum((live.now.astype(object) - a_before) * (r - live.remainder.astype(object)))
            )
            assert 2 * (current - previous) == 2 * remainders, boundary
            previous = current


def test_x_the_margin_rule_on_a_layer_keeps_the_folded_axis_self_reads():
    """Reviewer 3's line (18:12Z): on a periodic 256 x 256 x 1 layer the mode's operator keeps
    the folded axis's two self-reads (S_4 + 2 a_now), so the layer row of MASSIVE_RECORD.md
    section 11 item 7 (mu = 0.15, s = 14, g = mu^2 / 4: the kind [3200, 3236], the well
    [3200, 3227]) reads omega_b 0.14846 within 0.0002 and the extent 36.2 within 1 Link
    (`massive_layer_pins.out`), and the rule compares x and y only (z folded)."""
    document = block_world(
        [256, 256, 1],
        PERIODIC,
        [3200, 3236],
        [{"position": [121, 121, 0], "side": 14, "pair": [3200, 3227], "margin": "control"}],
    )
    document["age_bound"] = 100000
    reading = check_margins(parse_nature_beam_world(document))[0]
    assert abs(reading.omega_b - 0.14846) < 0.0002
    assert abs(reading.extent - 36.2) < 1.0
    assert [axis for axis, _, _, _ in reading.axes] == ["x", "y"]


def test_y_the_mode_seeded_layer_blocks_clicks_read_the_bound_mode():
    """The seed as the bound mode's integer profile (MASSIVE_RECORD.md section 11 item 7, the
    reader of record and the seed; EXPLORATORY, the cheap 128^2 rest layer): the block s = 14 at
    g = mu^2 / 4 (the kind [3200, 3236], the well [3200, 3227]) seeded flat reads its clicks at a
    beat (the mean interval 39.3 against the mode's period 42.32), seeded with the module's mode
    as integers at 2^20 over the whole layer (the generator's integers in the world file, the
    same at both levels) it reads the mode: the clicks' mean interval over [200, 1500] within
    0.5 percent of 2 pi / omega_b; the load-time check of the profile against the module's mode
    reads 0 units. The edge cases: a profile without `margin` refused; a profile of the wrong
    length refused; an all-zero profile refused."""
    block = {"position": [57, 57, 0], "side": 14, "pair": [3200, 3227], "margin": "control"}
    document = block_world([128, 128, 1], PERIODIC, [3200, 3236], [block], ticks=1500)
    document["age_bound"] = 100000
    world = parse_nature_beam_world(document)
    reading = block_margin(world, 0)
    period = 2 * np.pi / reading.omega_b
    mode = bound_mode(world, 0)
    profile = np.rint(mode * (1 << 20)).astype(np.int64)
    seeded = dict(document)
    seeded["measured"] = [dict(document["measured"][0], seed=[int(v) for v in profile.ravel()])]
    world = parse_nature_beam_world(seeded)
    assert profile_check(world, 0) == (0, 1 << 20)
    lines: list[dict] = []
    simulation = DetectorLawSimulation(world, observer=lines.append)
    assert np.array_equal(simulation.blocks[0].own.now, profile)
    for _ in range(1500):
        simulation.step()
    clicks = [line["tick"] for line in lines if line["event"] == "click" and line["tick"] >= 200]
    mean = (clicks[-1] - clicks[0]) / (len(clicks) - 1)
    assert abs(mean - period) < 0.005 * period, (mean, period)
    for bad, match in (
        ({"seed": [1] * (128 * 128)}, "admitted only with margin"),
        ({"seed": [1, 2, 3], "margin": "control"}, "must be 16384 integers"),
        ({"seed": [0] * (128 * 128), "margin": "control"}, "must not be all zero"),
    ):
        entry = {k: v for k, v in document["measured"][0].items() if k != "margin"}
        entry.update(bad)
        refused = dict(document)
        refused["measured"] = [entry]
        with pytest.raises(ValueError, match=match):
            parse_nature_beam_world(refused)


def matter_lamp_world(matter_lamp: bool, clock: list[int] | None = None) -> dict:
    """A chain of 200 Nodes (x open; y and z periodic of one layer): light's lamp of the first
    build at x = 2 (chain_world) beside the massive kind `matter`, pair [156, 157], the SAME
    clock [77, 25] on N = 64 declared as its `phase_per_link` (the pair form), and, when asked,
    a lamp of that kind at x = 100 (one birth, a train of 6 periods); no detector; `clock` None declares no clock on the kind (the refusal's edge case)."""
    document = chain_world()
    document["shape"] = [200, 1, 1]
    document["ticks"] = 160
    document["massive_record"] = True
    document["amplitude_bound"] = 1 << 32
    matter: dict = {"name": "matter", "quantum": 1, "pair": [156, 157]}
    if clock is not None:
        matter["phase_per_link"] = clock  # None: no clock (the refusal's edge case)
    document["families"].append(matter)
    document["measured"] = document["measured"][:1]
    if matter_lamp:
        document["measured"].append(
            {
                "position": [100, 0, 0],
                "family": "matter",
                "amount": 1,
                "phase": 0,
                "momentum": [0, 0, 0],
                "fixed": True,
                "directions": [[1, 0, 0]],
                "lamp": {"rate": [1, 1], "wheel": [1, 64], "directions": [[1, 0, 0]], "train": 6},
            }
        )
    document["detectors"] = []
    return document


def test_z_a_matter_lamps_train_carries_the_kinds_band():
    """The lamp verb on a massive kind (the Boss's 23:32Z): a lamp of the kind [156, 157] at the
    declared clock [77, 25] on N = 64 (omega = 2 pi x 77 / (25 x 64), above the gap cos omega_0 =
    156 / 157) births a record driven at its Node for its train and advanced by the rule with the
    kind's pair; the train's one-Link phase is the band's at that clock, on a chain cos k =
    3 den cos omega / num - 2 (the rule's plane wave a_next + a_before = (num / 3 den) S_6 with
    S_6 = 2 cos k + 4 on a chain): k = 4.99 steps of 64. Read: the record's phase at the Nodes
    x = 106 and x = 110 (and x = 94, x = 90 on the other side) at the interval 100 by `read_phase`
    at each Node's peak register, the span over 4 Links within 3 steps of 4 k on either side (the
    reading's grain, BUILD.md section 11: read 22 beside 19.97 with the record through the take,
    21 before it); the record does not complete within the train (its click is test (aa)) and
    the books balance at every interval. The edge cases: a lamp on a massive kind WITHOUT the clock is
    refused at load naming the pair form; light's [1, 1] unchanged: light's record's rows at
    every interval are identical with and without the matter lamp beside it (and the first
    build's chain digests stand, test (p))."""
    import math

    num, den = 156, 157
    steps = 64
    omega = 2 * math.pi * 77 / (25 * steps)
    assert math.cos(omega) < num / den, "the clock above the gap"
    k_steps = math.acos(3 * den * math.cos(omega) / num - 2) * steps / (2 * math.pi)
    assert abs(k_steps - 4.99) < 0.01

    world = parse_nature_beam_world(matter_lamp_world(True, [77, 25]))
    beside = parse_nature_beam_world(matter_lamp_world(False, [77, 25]))
    simulation = DetectorLawSimulation(world)
    other = DetectorLawSimulation(beside)
    identity = 1 * (1 << 32) + 1
    nodes = [(x, 0, 0) for x in (90, 94, 106, 110)]
    peaks = dict.fromkeys(nodes, 0)
    for tick in range(1, 101):
        simulation.step()
        other.step()
        assert simulation.books()["balanced"], tick
        live = simulation.records.get(identity)
        assert live is not None, "the matter lamp's record is in flight through its train"
        for node in nodes:
            peaks[node] = max(peaks[node], abs(int(live.now[node])))
        # light's rows unchanged beside the matter lamp
        for light_identity, light in other.records.items():
            assert np.array_equal(simulation.records[light_identity].now, light.now), tick
    live = simulation.records[identity]
    assert world.families[1].massive_kind and live.driven is not None
    phase = {}
    for node in nodes:
        reading = simulation.read_phase(live, node, peaks[node])
        assert reading is not None, node
        phase[node] = reading[0]
    # the wave leaves the lamp both ways: the phase lags by k per Link away from it
    right = (phase[(106, 0, 0)] - phase[(110, 0, 0)]) % steps
    left = (phase[(94, 0, 0)] - phase[(90, 0, 0)]) % steps
    assert abs(right - 4 * k_steps) < 3, (right, 4 * k_steps)
    assert abs(left - 4 * k_steps) < 3, (left, 4 * k_steps)
    with pytest.raises(ValueError, match="needs the pair form of phase_per_link on the family"):
        parse_nature_beam_world(matter_lamp_world(True))


def test_aa_a_matter_lamps_record_is_taken_and_clicks_once_at_the_rung():
    """Reviewer 3's line on the matter lamp (the Boss's 01:10Z): a lamp's record of a massive
    kind goes through the same take and pointer path as light's (the click is the law's one
    action on any record, POSTULATES 10); a block's record keeps MUST 2. The chain world of
    test (z) without light's lamp (the matter kind's faces periodic, so that the train's two
    halves both arrive at the screen, one round the chain), the matter lamp's stock 2 at the
    rate [1, 1] (two births on consecutive intervals, u = 0 and u = 1 on the wheel [1, 64],
    W = 64), a receiver body of the matter family at x = 184 read as the set `screen`: each
    record clicks ONCE, its `click` stamp the first interval its pointer at the chosen cell
    reached 1 / W of the norm, after the front's flight (84 Links at the band's group pace
    0.5, so more than 100 intervals after the birth) and before its completion interval; the
    screen's pointer reaches nine tenths of each record's norm (the lamp's own body takes the
    train's reflections off the screen's Ports after its grace, the take's pair being light's); the second record (u = 1) is chosen at the screen (the
    ladder's u = 0 falls on the first cell with a rung, the lamp's own body, an artefact of the
    order, not of the take); both records then gone from the board, the books balanced at
    every interval, two gather lines in all. A block's record (test (u)) still never
    completes."""
    document = matter_lamp_world(True, [77, 25])
    document["ticks"] = 3000
    document["measured"] = [
        {
            "position": [184, 0, 0],
            "family": "matter",
            "amount": 1,
            "phase": 0,
            "momentum": [0, 0, 0],
            "fixed": True,
            "directions": [[-1, 0, 0]],
        },
        dict(document["measured"][1], amount=2),
    ]
    document["detectors"] = [{"name": "screen", "positions": [[184, 0, 0]], "threshold": 1}]
    world = parse_nature_beam_world(document)
    lines: list[dict] = []
    simulation = DetectorLawSimulation(world, observer=lines.append)
    assert simulation.wheel == 64
    identities = [1 * (1 << 32) + 1, 1 * (1 << 32) + 2]
    screen = simulation.cell_names.index("screen")
    crossed: dict[int, dict[str, int]] = {identity: {} for identity in identities}
    shares: dict[int, tuple[int, int]] = {}
    for _ in range(3000):
        simulation.step()
        assert simulation.books()["balanced"], simulation.tick
        for identity in identities:
            live = simulation.records.get(identity)
            if live is None:
                continue
            shares[identity] = (live.pointers[screen], live.norm)
            for cell, pointer in enumerate(live.pointers):
                name = simulation.cell_names[cell]
                if name not in crossed[identity] and pointer * 64 >= live.norm:
                    crossed[identity][name] = simulation.tick
        gathers = [line for line in lines if line["event"] == "gather"]
        if len(gathers) == 2:
            break
    gathers = [line for line in lines if line["event"] == "gather"]
    assert [gather["record"] for gather in gathers] == identities
    assert [gather["u"] for gather in gathers] == [0, 1]
    for gather in gathers:
        chosen = gather["chosen"][0][0]
        assert gather["click"] == crossed[gather["record"]][chosen], (chosen, gather["click"])
        assert gather["click"] - gather["birth"] > 100
        assert gather["click"] < gather["tick"]
        assert gather["record"] not in simulation.records
    assert gathers[1]["chosen"][0][0] == "screen"
    assert "screen" in crossed[identities[0]] and "screen" in crossed[identities[1]]
    for identity in identities:
        at_screen, norm = shares[identity]
        assert at_screen * 10 >= norm * 9, (identity, at_screen, norm)
    assert simulation.books()["balanced"]


def test_ab_the_world_key_wheel_declares_the_detectors_rung_without_a_lamp():
    """The world key `wheel` (detector-law-v1; RUN_LIST.md's light detectors at W = 64 in worlds
    whose records a block emits, which have no lamp): the detector sets' rung W where no lamp
    declares a larger birth wheel; 1 by default; a lamp's larger wheel wins; refused below 1
    and without `detector_law`."""
    base = massive_world([8, 8, 1], {"x": "open", "y": "periodic", "z": "periodic"}, [156, 157])
    assert DetectorLawSimulation(parse_nature_beam_world(base)).wheel == 1
    keyed = json.loads(json.dumps(base))
    keyed["wheel"] = 64
    assert parse_nature_beam_world(keyed).wheel == 64
    assert DetectorLawSimulation(parse_nature_beam_world(keyed)).wheel == 64
    with_lamp = matter_lamp_world(True, [77, 25])  # light's lamp [2531, 4096], matter's [1, 64]
    with_lamp["wheel"] = 16
    assert DetectorLawSimulation(parse_nature_beam_world(with_lamp)).wheel == 4096
    with_lamp["wheel"] = 8192
    assert DetectorLawSimulation(parse_nature_beam_world(with_lamp)).wheel == 8192
    zero = json.loads(json.dumps(base))
    zero["wheel"] = 0
    with pytest.raises(ValueError, match="wheel"):
        parse_nature_beam_world(zero)
    no_law = json.loads(json.dumps(base))
    no_law["detector_law"] = False
    no_law["massive_record"] = False
    del no_law["amplitude_bound"]
    no_law["wheel"] = 64
    with pytest.raises(ValueError, match="refused without `detector_law`"):
        parse_nature_beam_world(no_law)


def light_clock_world(faces: str, far_body: bool) -> dict:
    """DECLARATIONS.md section 10 with section 15's lines (M1-1, M1-3, M1-4, M1-10): a chain of
    173 (x `closed` for light, the zero face at 172 the mirror B sixty Links from A's face at
    112; or x open, the sponges), the matter kind [800, 809], the emitter A of side 12 at
    [100, 112) at full depth with the seed 50 x 2^20, `emits` light with G = [1, 50] and
    g = [1, 1000], W = 64; light's clock [1, 1]; the receiving set `A_face` bound to A with its
    own wheel 64 (key (i)); with `far_body`, a receiver body at x = 160 read as the set `far`
    with its own wheel 64; the amplitude bound 2^32."""
    document = massive_world([173, 1, 1], {"x": faces, "y": "periodic", "z": "periodic"}, [800, 809])
    document["families"][0]["phase_per_link"] = [1, 1]
    document["ticks"] = 600
    document["measured"] = [
        {
            "position": [100, 0, 0],
            "family": "matter",
            "amount": 1,
            "phase": 0,
            "momentum": [0, 0, 0],
            "fixed": True,
            "side": 12,
            "pair": [800, 800],
            "seed": 50 << 20,
            "coupling": {"G": [1, 50], "g": [1, 1000]},
            "wheel": 64,
            "emits": "light",
            "margin": "control",
            "own_grace": 70,
        }
    ]
    document["detectors"] = [{"name": "A_face", "block": 0, "wheel": 64}]
    if far_body:
        document["measured"].append(
            {
                "position": [160, 0, 0],
                "family": "light",
                "amount": 1,
                "phase": 0,
                "momentum": [0, 0, 0],
                "fixed": True,
                "directions": [[-1, 0, 0]],
            }
        )
        document["detectors"].append({"name": "far", "positions": [[160, 0, 0]], "wheel": 64})
    return document


def test_ac_the_blocks_grace_the_bound_set_and_the_closed_face():
    """Line B (the block's grace), key (i) (a detector set bound to a block, its own wheel, the
    block's count on the stamp) and the closed face (Reviewer 3's blocking line), on the light
    clock's chain (section 10 with section 15's lines; A's `own_grace` 70 = N_s). (1) With the
    faces OPEN and no body: A's first emitted record books nothing at `A_face` while A sources
    it (its cycle, 70 intervals) and for the 70 intervals of `own_grace` after (no pointer, no
    rung); at the grace's end the set's rung is crossed AT ONCE by the record's own residual at
    the cells (a tenth of the emission's peak, decaying slowly; a READING for the physicist:
    the first rung after the grace is the residual's, in the open world and the closed alike,
    so the return of the light clock is not this rung), stamped with A's own count as the
    interval begins (the count the block carries when the offer arrives, before the block's
    clock of the same interval; `rung_counts`, as `_book_response` stamps a block's cell) and
    named by `clock_source` on the gather line when the set is
    chosen; with a receiver body at x = 160 beside, the far set crosses its rung after the
    grace as well. (2) With the faces CLOSED (the zero face at 172 the mirror, no take, no face
    cell): the record's level at x = 160 between the intervals 250 and 320 (after the wave's
    front passed toward the face and the return came back, 2 L / c = 208 after the emission)
    stays above one hundredth of the emission's peak and above ten times the open world's
    (where the wave is taken at the face: 7.0 x 10^6 against 1.7 x 10^5 read, the peak
    1.6 x 10^7); the books balanced at every interval in both
    worlds; `click_at` on every gather line. The loader: `closed` without `detector_law`
    refused, a set with both `block` and `positions` refused, `block` naming no block refused,
    `own_grace` on a block that emits nothing refused."""
    first = 1  # A's first emitted record: block 0, birth 1
    levels: dict[str, int] = {}
    peak = 0
    for faces in ("open", "closed"):
        world = parse_nature_beam_world(light_clock_world(faces, False))
        assert world.closed == (faces == "closed", False, False)
        assert world.boundary_per_axis["x"] == faces
        lines: list[dict] = []
        simulation = DetectorLawSimulation(world, observer=lines.append)
        assert ("face:+x" in simulation.cell_names) == (faces == "open")
        a_face = simulation.cell_names.index("A_face")
        block = simulation.blocks[0]
        in_grace_pointer_seen = 0
        grace_end: int | None = None
        rung: int | None = None
        stamp: int | None = None
        count_then: int | None = None
        late = 0
        for _ in range(320):
            count_before = block.count
            simulation.step()
            assert simulation.books()["balanced"], simulation.tick
            live = simulation.records.get(first)
            if live is None:
                continue
            peak = max(peak, int(np.max(np.abs(live.now))))
            if simulation._in_grace(live):
                in_grace_pointer_seen = max(in_grace_pointer_seen, live.pointers[a_face])
                assert live.first_rung[a_face] is None
            elif grace_end is None:
                grace_end = simulation.tick
            if rung is None and live.first_rung[a_face] is not None:
                rung = live.first_rung[a_face]
                stamp = simulation.rung_counts[(first, a_face)]
                count_then = count_before
            if simulation.tick >= 250:
                late = max(late, int(abs(live.now[160, 0, 0])))
        assert in_grace_pointer_seen == 0 and grace_end is not None
        assert rung is not None and rung >= grace_end and rung - grace_end <= 2, (rung, grace_end)
        assert stamp == count_then and stamp is not None and stamp >= 1
        assert block.cycle_length > 0
        gathers = [line for line in lines if line["event"] == "gather"]
        assert all("click_at" in gather and "clock_source" in gather for gather in gathers)
        for gather in gathers:
            if gather["chosen"] and gather["chosen"][0][0] == "A_face":
                assert gather["clock_source"] == "measured:0" and gather["click_at"] == "rung"
        levels[faces] = late
    assert peak > 0
    assert levels["closed"] * 100 > peak, (levels, peak)
    assert levels["closed"] > 10 * levels["open"], (levels, peak)
    # a receiver beyond the grace clicks: the far body's set crosses its rung after the grace
    beside = DetectorLawSimulation(parse_nature_beam_world(light_clock_world("open", True)))
    far = beside.cell_names.index("far")
    far_rung: int | None = None
    for _ in range(320):
        beside.step()
        live = beside.records.get(first)
        if live is not None and far_rung is None and live.first_rung[far] is not None:
            far_rung = live.first_rung[far]
    assert far_rung is not None and far_rung > 100
    # the loader's refusals
    with pytest.raises(ValueError, match="closed"):
        bad = light_clock_world("closed", False)
        bad["detector_law"] = False
        bad["massive_record"] = False
        del bad["amplitude_bound"]
        parse_nature_beam_world(bad)
    both = light_clock_world("open", False)
    both["detectors"] = [{"name": "A_face", "block": 0, "positions": [[100, 0, 0]]}]
    with pytest.raises(ValueError, match="both `block` and `positions`"):
        parse_nature_beam_world(both)
    no_block = light_clock_world("open", True)
    no_block["detectors"] = [{"name": "B", "block": 1}]
    with pytest.raises(ValueError, match="names a measured event that is no block"):
        parse_nature_beam_world(no_block)
    silent = light_clock_world("open", False)
    del silent["measured"][0]["emits"]
    silent["detectors"] = []
    with pytest.raises(ValueError, match="own_grace is refused on a block that emits nothing"):
        parse_nature_beam_world(silent)


def test_ad_a_wall_of_lights_kind_is_a_mirror_line():
    """DECLARATIONS.md section 15 L-1 (the (M) wall's path): a mirror line of blocks of light's
    kind with the pair [1, 2], two Nodes deep, on the first build's chain (x = 40 and 41; the
    lamp at x = 2, the screen at x = 70): the blocks have no own record, no clock and no
    coupling (the loader sets their seed 0; the engine's blocks' loop skips them; the margin
    rule skips light's kind), light's pair arrays carry [1, 2] at the two cells and [1, 1]
    elsewhere; over 200 intervals the largest level beyond the wall (x in [45, 69]) stays below
    three percent of the largest level before it (x in [10, 38]; the engine reads 1.45 percent
    beside the declaration's 0.7 percent of the amplitude, the front's precursor included),
    the books balanced at every interval; a light-kind block with `seed`,
    `coupling` or `margin` refused."""
    document = chain_world()
    document["massive_record"] = True
    document["amplitude_bound"] = 1 << 32
    document["ticks"] = 200
    for x in (40, 41):
        document["measured"].append(
            {
                "position": [x, 0, 0],
                "family": "light",
                "amount": 1,
                "phase": 0,
                "momentum": [0, 0, 0],
                "fixed": True,
                "side": 1,
                "pair": [1, 2],
            }
        )
    world = parse_nature_beam_world(document)
    assert [entry.block is not None for entry in world.measured] == [False, False, True, True]
    assert world.measured[2].block is not None and world.measured[2].block.seed == 0
    simulation = DetectorLawSimulation(world)
    assert all(block.own is None for block in simulation.blocks)
    assert int(simulation.kind_den[0][40, 0, 0]) == 2 and int(simulation.kind_den[0][41, 0, 0]) == 2
    assert int(simulation.kind_den[0][39, 0, 0]) == 1 and int(simulation.kind_num[0][40, 0, 0]) == 1
    before = beyond = 0
    for _ in range(200):
        simulation.step()
        assert simulation.books()["balanced"], simulation.tick
        for live in simulation.records.values():
            before = max(before, int(np.max(np.abs(live.now[10:39, 0, 0]))))
            beyond = max(beyond, int(np.max(np.abs(live.now[45:70, 0, 0]))))
    assert before > 0 and beyond * 100 < 3 * before, (before, beyond)
    for key, value in (("seed", 5), ("coupling", {"G": [1, 1], "g": [1, 2]}), ("margin", "control")):
        bad = json.loads(json.dumps(document))
        bad["measured"][2][key] = value
        with pytest.raises(ValueError, match="refused on a block of light's kind"):
            parse_nature_beam_world(bad)


def test_ae_the_momentum_books_carry_the_blocks_held_momentum_and_nothing_else():
    """Issue #1086 (a GAMEBOARD diagnostic, no law, no pin): the books' `momentum` carries
    `held` as the sum of the blocks' declared momentum vectors ([64, 0, 0] for one block
    pushed to k = 3; [0, 0, 0] at rest), `transit` and `escaped` null with the note that
    they are not accounted, and `balanced_scope` naming content alone; the run's record
    carries the same scope line."""
    world = parse_nature_beam_world(
        block_world(
            [24, 24, 24],
            PERIODIC,
            [800, 809],
            [{"position": [10, 10, 10], "side": 3, "pair": [800, 800], "momentum": [64, 0, 0]}],
        )
        | {"age_bound": 100}
    )
    simulation = DetectorLawSimulation(world)
    simulation.step()
    books = simulation.books()
    assert books["momentum"]["held"] == [64, 0, 0]
    assert books["momentum"]["transit"] is None and books["momentum"]["escaped"] is None
    assert "not accounted" in books["momentum"]["note"]
    assert books["balanced_scope"].startswith("content alone")
    rest = DetectorLawSimulation(parse_nature_beam_world(massive_world([4, 4, 4], "open", [2, 3])))
    rest.step()
    assert rest.books()["momentum"]["held"] == [0, 0, 0]


def test_af_the_tables_rotation_reads_the_pair_by_the_linear_form():
    """DECLARATIONS.md section 15 T-1 (the fourth component's reading): a record of declared A
    and phi at a bar Node reads A cos(phi + t) for t in {0, N / 8, N / 4, 3 N / 8} by
    `read_pair` (the linear form on the pair, section 14 item 1), within the coefficients'
    rounding (the tables' 1 / 256 and by_clock's step: A / 64 at N = 64 with the clock
    [77, 25]), at every phi of the circle; a block's massive record reads 0; a clock whose
    step has a sine of 0 raises naming the step."""
    world = parse_nature_beam_world(matter_lamp_world(False, [77, 25]))
    simulation = DetectorLawSimulation(world)
    steps = world.phase_steps
    cosines = phase_cosines(steps)
    unit_per_cell = UNIT // 256
    k = 3  # by_clock(0, 77, 25)
    for phi in range(steps):
        live = LiveRecord(
            phi + 1,
            0,
            0,
            0,
            1,
            0,
            1,
            77,
            25,
            200,
            21,
            np.zeros(simulation.shape, dtype=np.int64),
            np.zeros(simulation.shape, dtype=np.int64),
            np.zeros(simulation.shape, dtype=np.int64),
            pointers=[0] * len(simulation.cell_names),
            first_rung=[None] * len(simulation.cell_names),
            ports=[np.zeros(simulation.shape, dtype=np.int64) for _ in simulation.take_masks],
            age=1,
        )
        live.now[50, 0, 0] = cosines[phi] * unit_per_cell
        live.before[50, 0, 0] = cosines[(phi - k) % steps] * unit_per_cell
        for turn in (0, steps // 8, steps // 4, 3 * steps // 8):
            reading = simulation.read_pair(live, (50, 0, 0), turn)
            closed = UNIT * math.cos(2 * math.pi * (phi + turn) / steps)
            assert abs(reading - closed) <= UNIT // 64, (phi, turn, reading, closed)
    block_record = simulation._massive_record(7, 0, 1)
    assert simulation.read_pair(block_record, (50, 0, 0), 8) == 0
    zero_step = LiveRecord(
        99,
        0,
        0,
        0,
        1,
        0,
        1,
        32,
        1,
        200,
        2,
        np.zeros(simulation.shape, dtype=np.int64),
        np.zeros(simulation.shape, dtype=np.int64),
        np.zeros(simulation.shape, dtype=np.int64),
        pointers=[0] * len(simulation.cell_names),
        first_rung=[None] * len(simulation.cell_names),
        age=1,
    )
    with pytest.raises(ValueError, match="has a sine of 0"):
        simulation.read_pair(zero_step, (50, 0, 0), 0)


def test_ag_an_absorbing_block_of_the_matter_kind_takes_with_its_declared_pair():
    """DECLARATIONS.md section 15 M1-6 and the Boss's item 6b (the take on the massive kind;
    the take's pair per kind a declaration of kind 2): on the chain of test (aa) the receiver
    at x = 184 is an ABSORBING block of the matter kind (side 1, the kind's own pair
    [156, 157], admitted on an absorbing block: a take line, not a well and not a barrier)
    with its declared take [-19, 86] (the phase pace at lambda_dB = 12), read as the set
    `screen`: the matter lamp's record is taken there and completes with ONE click, the books
    balanced at every interval; the take arrays carry [-19, 86] at the block's cell and
    light's [-15, 56] elsewhere. The pair that leaves least (the test the declaration asks
    for), read at the interval 300 of each world: the screen's pointer (the offer taken) with
    the declared pair 7.08 x 10^12 above light's 6.48 x 10^12, and the group-pace pair
    [-33, 100] below light's, 5.73 x 10^12; the largest level left between the lamp and the
    screen (x in [150, 182]) with the declared pair below light's (945542 against 951825).
    The loader: `take` on a block that is not absorbing refused; a pair outside (-1, 0]
    refused; a pair with n > 0 refused."""
    taken: dict[str, int] = {}
    left: dict[str, int] = {}
    for label, take in (("light", None), ("declared", [-19, 86]), ("group", [-33, 100])):
        document = matter_lamp_world(True, [77, 25])
        document["ticks"] = 3000
        block: dict = {
            "position": [184, 0, 0],
            "family": "matter",
            "amount": 1,
            "phase": 0,
            "momentum": [0, 0, 0],
            "fixed": True,
            "side": 1,
            "pair": [156, 157],
            "absorbing": True,
        }
        if take is not None:
            block["take"] = take
        document["measured"] = [block, dict(document["measured"][1], amount=1)]
        document["detectors"] = [{"name": "screen", "positions": [[184, 0, 0]], "threshold": 1}]
        world = parse_nature_beam_world(document)
        lines: list[dict] = []
        simulation = DetectorLawSimulation(world, observer=lines.append)
        expected = tuple(take) if take else (-15, 56)
        assert (int(simulation.take_num[184, 0, 0]), int(simulation.take_den[184, 0, 0])) == expected
        assert (int(simulation.take_num[100, 0, 0]), int(simulation.take_den[100, 0, 0])) == (-15, 56)
        identity = 1 * (1 << 32) + 1
        screen = simulation.cell_names.index("screen")
        for _ in range(3000):
            simulation.step()
            assert simulation.books()["balanced"], simulation.tick
            live = simulation.records.get(identity)
            if live is not None and simulation.tick == 300:
                taken[label] = live.pointers[screen]
                left[label] = int(np.max(np.abs(live.now[150:183, 0, 0])))
            if any(line["event"] == "gather" for line in lines):
                break
        gathers = [line for line in lines if line["event"] == "gather"]
        assert len(gathers) == 1 and gathers[0]["record"] == identity
        assert identity not in simulation.records
    assert taken["declared"] > taken["light"] > taken["group"], taken
    assert left["declared"] < left["light"], left
    bad = matter_lamp_world(True, [77, 25])
    bad["measured"].append(
        {
            "position": [184, 0, 0],
            "family": "matter",
            "amount": 1,
            "phase": 0,
            "momentum": [0, 0, 0],
            "fixed": True,
            "side": 1,
            "pair": [314, 315],
            "take": [-19, 86],
        }
    )
    with pytest.raises(ValueError, match="take is refused on a block that is not absorbing"):
        parse_nature_beam_world(bad)
    for pair, message in (([-90, 86], r"lies in \(-1, 0\]"), ([19, 86], "take numerator")):
        wrong = json.loads(json.dumps(bad))
        wrong["measured"][-1]["absorbing"] = True
        wrong["measured"][-1]["take"] = pair
        with pytest.raises(ValueError, match=message):
            parse_nature_beam_world(wrong)
