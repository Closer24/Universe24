"""The massive record kind (`massive-record-v1`, docs/designs/detector_law/MASSIVE_RECORD.md;
the build's plan BUILD.md section 6, the expected integers written there before the code):
the rule with a pair per record kind on the six-neighbour term, (a) on a chain and (b) at a
corner against section 1's integers, (c) light's pair [1, 1] the first build's integers bit
for bit, (d) the conserved form I to the remainders' jitter; (p) the byte identity of the
light record without the key (the digests of the head f4a3971a); (q) the loader's refusals
of the step's keys; (r) the record's keys under the key and none without it. SINCE THE
EMITTER AS A CLICKING BODY (ALGEBRA.md 9.17 (4); BUILD.md section 26) every source in these
worlds is an emitter body of a massive kind seeded on its bound mode (the lamp is refused
under the detector law; the emission by the coupling's source term, the emitter's grace,
its exemption and its own take are retired: its cells are cells like every other)."""

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
from tests.test_detector_law import chain_world, emitter_body
from tests.test_emitter import massive_generator


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
    live.age = 1000
    total = simulation._neighbours(now) - 3 * before + remainder
    expected_next = np.floor_divide(total, 3)
    expected_remainder = total - 3 * expected_next
    a_next, r_next = step_once(simulation, live)
    free = np.ones(simulation.shape, dtype=bool)
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
    the scope of `balanced` named), every other field byte for byte; then all three once more
    by item 10 (the lamp's own take of its record from the first interval after the train, the
    record alive at 600 carrying its pointers; BUILD.md section 18); then all three once more
    by the emitter as a clicking body (BUILD.md section 26: the chain world's lamp an emitter
    body of the kind [7, 8] on the well [8, 7], six births at their rungs, the grace and the
    own take retired), then once more by the write on the circle of 2 N with before = -now
    and the excited record's norm as the one-way flux into its centre cell over one period
    (ALGEBRA.md 9.17 (5) and (6), 9.19 (3); BUILD.md section 26 item 13), then once more by
    the flux reading at every cell with the cumulative ladder and the deletion at the click,
    on the chain world's faces closed (item 14), then once more by the residue from the law
    on the rich well [801, 700] with the take's data gone (item 15), the digests read at
    that head."""
    assert run_chain_digests() == {
        "events": "2322e1f6adfc975c27f015ddfd31645948be76a25b299518e9c2d5dd4d69c4c6",
        "state": "d67c9eb9f0392759598c7479900b3a5015b4a9d6076c27bd17d6902b55e3334a",
        "audit": "a69f0145570bce15b2b8e9996e0116004b55fee850040efd65d3ee9a6e487276",
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
    with pytest.raises(ValueError, match="lamp is refused under detector-law-v1"):
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
    # without the key there is no block, so no emitter body (the lamp refused under the
    # detector law): the rule's world with the key withdrawn and light alone
    without = massive_world([4, 4, 4], "open", [2, 3])
    without["massive_record"] = False
    del without["amplitude_bound"]
    del without["families"][1]
    plain = parse_nature_beam_world(without)
    assert MASSIVE_RECORD_RULE not in plain.hypotheses
    assert plain.families[0].faces is None
    assert "form" not in DetectorLawSimulation(plain).books()["families"]["light"]


# The block (STEP 3 of the build: BUILD.md section 6, (e) to (l))


def block_world(
    shape: list[int],
    boundary: object,
    kind: list[int],
    blocks: list[dict],
    source: dict | None = None,
    ticks: int = 100,
    faces: dict[str, str] | None = None,
) -> dict:
    """A world of the massive kind `matter` with blocks (measured events of `matter` with
    `side`), a light family with the chain test's clock [77, 25] (the period 20.8 intervals,
    lambda 12 Links), and optionally an emitter body of light (`emitter_at`, a well of the
    source family) as the first measured event, seeded on its bound mode (the generator's
    profile at its scalar seed)."""
    matter: dict = {"name": "matter", "quantum": 1, "pair": kind}
    if faces is not None:
        matter["faces"] = faces
    families = [{"name": "light", "quantum": 1, "phase_per_link": [77, 25]}, matter]
    measured: list[dict] = []
    if source is not None:
        measured.append(source)
        families.append(source_family())
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
            "seed",
            "cavity",
            "ramp",
            "start",
            "margin",
            "held",
            "receiver",
            "emitter",
        ):
            if key in block:
                entry[key] = block[key]
        measured.append(entry)
    document: dict = {
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
        "families": families,
        "measured": measured,
        "detectors": [],
    }
    if source is not None:
        seed_source(document, 0)
    return document


def seed_source(document: dict, number: int) -> None:
    """The measured event `number` (an emitter body, a one-cell well) seeded on its bound
    mode at its scalar seed (the generator's `mode_profile`, the world's other blocks left as
    declared), its `margin` made explicit."""
    entry = document["measured"][number]
    entry.setdefault("margin", "control")
    generator = massive_generator()
    entry["seed"] = generator.mode_profile(document, number, amplitude=entry["seed"])
    if "emitter" in entry:
        generator.excite_on_the_mode(document, number)


def with_screen(document: dict, x: int) -> dict:
    """The receiver by name for a test world's emitter body (DECLARATIONS.md section 13
    item 7): a receiver body of light at x read as the set `screen` (no wheel: the rung's
    wheel is the record's own, ALGEBRA.md 9.22 (4))."""
    document["measured"].append(
        {
            "position": [x, 0, 0],
            "family": "light",
            "amount": 1,
            "phase": 0,
            "momentum": [0, 0, 0],
            "fixed": True,
            "directions": [[-1, 0, 0]],
        }
    )
    document["detectors"].append({"name": "screen", "positions": [[x, 0, 0]]})
    return document


SOURCE_KIND = [7, 8]  # the emitter bodies' own kind (omega_0 = 0.505; the index worlds')
SOURCE_WELL = [
    801,
    700,
]  # its one-cell well, rich (W = 700, ALGEBRA.md 9.22 (4)): bound on a chain and on a layer


def source_family() -> dict:
    """The emitter bodies' massive family `source` (the kind SOURCE_KIND, no clock)."""
    return {"name": "source", "quantum": 1, "pair": list(SOURCE_KIND)}


def emitter_at(
    x: int,
    stock: int = 1,
    family: str = "light",
    own: str = "source",
    pair: list[int] | None = None,
    receiver: object = None,
) -> dict:
    """An emitter body at a Node of a chain (ALGEBRA.md 9.17 (4)): a one-cell well of the
    massive family `own` (the well `pair`, SOURCE_WELL by default) with the scalar seed 100
    (its profile on the mode by `seed_source`), `stock` excitations, the born family
    `family`; with `receiver`, the born records' ladder by name. The residue and the wheel
    are the law's (9.22 (4): W = 700 on SOURCE_WELL); the cadence of the excitations
    (COMPUTATION, BUILD.md section 26): the residue u clicks about (2 u + 1) P / (2 W)
    intervals after its excitation, P the mode's period."""
    entry = emitter_body([x, 0, 0], stock, receiver=receiver, family=family)
    entry["family"] = own
    entry["pair"] = list(pair or SOURCE_WELL)
    return entry


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


def test_h_an_emitter_body_births_in_turn_each_birth_one_quantum_of_its_stock():
    """BUILD.md (h) SINCE section 26 (the emission by the coupling's source term retired with
    the lamp; an emitter is a clicking body, ALGEBRA.md 9.17 (4)): an emitter body of the
    source kind (the one-cell well SOURCE_WELL at x = 100 seeded on its mode, the stock 3)
    on the chain of 240 with the screen at 230: three births in turn, the residues the
    law's, each born record of content 1 moved from the stock (`held_spent` 3 of the
    source family, `transit_released` 3 of light), the excited record ended at each birth (no
    record of the matter kind once the stock is spent), the books balanced at every tick. The
    edge cases: `emits` and `own_grace` beside `emitter` refused naming the key; `emitter` on
    a body of light's kind refused; a stock below 1 refused."""
    world = parse_nature_beam_world(
        with_screen(
            block_world(
                [240, 1, 1],
                CHAIN,
                [156, 157],
                [],
                emitter_at(100, 3),
                ticks=600,
                faces={"x": "open"},
            ),
            230,
        )
    )
    lines: list[dict] = []
    simulation = DetectorLawSimulation(world, observer=lines.append)
    for _ in range(600):
        simulation.step()
        assert simulation.books()["balanced"], simulation.tick
    births = [line for line in lines if line["event"] == "birth"]
    assert len(births) == 3
    # the residues from the law (ALGEBRA.md 9.22 (4)) on W = 700; the same at
    # every birth of a body without a coupling (BUILD.md section 26 item 15)
    assert all(line["W"] == 700 and 0 <= line["u"] < 700 for line in births)
    assert len({line["u"] for line in births}) == 1
    assert simulation.ledger.held_spent[2] == 3 and simulation.ledger.transit_released[0] == 3
    assert simulation.blocks[0].own is None
    assert all(live.family == 0 and live.content == 1 for live in simulation.records.values())
    base = with_screen(block_world([240, 1, 1], CHAIN, [156, 157], [], emitter_at(100, 3)), 230)
    for key in ("emits", "own_grace"):
        bad = json.loads(json.dumps(base))
        bad["measured"][0].update({"emits": "light", "own_grace": 70, "receiver": "screen"})
        if key == "own_grace":
            del bad["measured"][0]["emits"]
        with pytest.raises(ValueError, match=f"{key} is refused"):
            parse_nature_beam_world(bad)
    on_light = json.loads(json.dumps(base))
    on_light["measured"][0]["family"] = "light"
    on_light["measured"][0]["seed"] = 100
    on_light["measured"][0]["pair"] = [1, 2]
    with pytest.raises(ValueError, match="of light's kind"):
        parse_nature_beam_world(on_light)
    empty = json.loads(json.dumps(base))
    empty["measured"][0]["amount"] = 0
    with pytest.raises(ValueError, match="amount"):
        parse_nature_beam_world(empty)


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
    Links (the float scratch of the plan) and its mode 0.1105 (the design's 96^3 box 0.1107);
    (5) BUILD.md section 26: a well too deep for its board is a RUNAWAY (the largest
    eigenvalue at or above 2, no oscillation, a level growing every interval; the one-cell
    well [800, 700] on the kind [800, 809] on a chain, 2 cos omega_b = 2.03, its level
    growing by 1.2 per interval) and is refused naming it, while the same well on a cube of
    24^3 is no runaway (the folded axes' self-reads count fully on a chain)."""
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
    deep = {"position": [40, 0, 0], "side": 1, "pair": [800, 700], "margin": "control"}
    runaway = block_world([200, 1, 1], CHAIN, [800, 809], [deep], faces={"x": "open"})
    runaway["age_bound"] = 100000
    reading = block_margin(parse_nature_beam_world(runaway), 0)
    assert reading.runaway and reading.omega_b == 0.0 and abs(reading.lambda_max - 2.032) < 0.002
    with pytest.raises(ValueError, match="the block's mode is a runaway"):
        check_margins(parse_nature_beam_world(runaway))
    cube = block_world([24, 24, 24], PERIODIC, [800, 809], [dict(deep, position=[10, 10, 10])])
    cube["age_bound"] = 100000
    assert not block_margin(parse_nature_beam_world(cube), 0).runaway


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


def matter_emitter_world(matter_emitter: bool, clock: list[int] | None = None, stock: int = 1) -> dict:
    """A chain of 200 Nodes (x open; y and z periodic of one layer): the light emitter of the
    first build at x = 2 (chain_world's, its family named `source`) beside the massive kind
    `matter`, pair [156, 157], the SAME clock [77, 25] on N = 64 declared as its
    `phase_per_link` (the pair form) and its take [-19, 86], and, when asked, an emitter body
    of the source kind at x = 100 whose born family is `matter` (`stock` births on the wheel
    [1, 64]); no detector; `clock` None declares no clock on the kind (the refusal's edge
    case); every emitter body seeded on its mode."""
    document = chain_world(on_mode=False)
    document["shape"] = [200, 1, 1]
    document["ticks"] = 160
    document["families"][1]["name"] = "source"
    document["measured"][0]["family"] = "source"
    matter: dict = {"name": "matter", "quantum": 1, "pair": [156, 157]}
    if clock is not None:
        matter["phase_per_link"] = clock  # None: no clock (the refusal's edge case)
    document["families"].append(matter)
    document["measured"] = document["measured"][:1]
    if matter_emitter:
        document["measured"].append(emitter_at(100, stock, family="matter"))
    document["detectors"] = []
    massive_generator().seed_on_the_mode(document)
    return document


def test_z_a_matter_emitters_record_is_a_massive_record_advanced_by_the_kinds_pair():
    """The emitter of a massive kind (the matter lamp's successor, ALGEBRA.md 9.17; the Boss's
    23:32Z on the lamp verb): an emitter body of the source kind at x = 100 whose born family
    is `matter` (the kind [156, 157] with the declared clock [77, 25] on N = 64) births a
    record of the matter kind, written once on its cell at both levels and advanced by the rule
    with the kind's pair (a massive kind's born record is driven by nothing and completes as
    light's: its `driven` set empty); the record leaves the cell both ways (the levels at
    x = 94 and x = 106 nonzero by the interval 100 and equal, the rule's mirror symmetry about
    the cell; the band's one-Link phase of the old train's reading returns with the line's
    per-Link pair, owed); the books balance at every interval; light's rows at every interval
    are identical with and without the matter emitter beside it (and the first build's chain
    digests stand, test (p)). The edge cases: an emitter whose born family is a massive kind
    WITHOUT the clock is refused at load naming the pair form."""
    world = parse_nature_beam_world(matter_emitter_world(True, [77, 25]))
    beside = parse_nature_beam_world(matter_emitter_world(False, [77, 25]))
    assert world.families[2].massive_kind and world.families[2].phase_per_age == (77, 25)
    simulation = DetectorLawSimulation(world)
    other = DetectorLawSimulation(beside)
    identity = 1 * (1 << 32) + 1
    born: int | None = None
    for tick in range(1, 101):
        simulation.step()
        other.step()
        assert simulation.books()["balanced"], tick
        live = simulation.records.get(identity)
        if live is not None:
            born = born if born is not None else tick
            assert live.family == 2 and live.emitter == 1
            assert live.emitter == 1
        # light's rows unchanged beside the matter emitter
        for light_identity, light in other.records.items():
            assert np.array_equal(simulation.records[light_identity].now, light.now), tick
    assert born is not None and born < 20
    live = simulation.records[identity]
    assert int(live.now[94, 0, 0]) != 0 and int(live.now[94, 0, 0]) == int(live.now[106, 0, 0])
    assert int(live.now[90, 0, 0]) == int(live.now[110, 0, 0])
    with pytest.raises(ValueError, match="pair form of its clock"):
        parse_nature_beam_world(matter_emitter_world(True))


def test_aa_a_matter_emitters_record_clicks_once_at_the_rung():
    """Reviewer 3's line on the matter lamp (the Boss's 01:10Z), on the matter emitter under
    the flux reading (ALGEBRA.md 9.19 (3)): an emitter's record of a massive kind goes
    through the same pointer path as light's (the click is the law's one action on any
    record, POSTULATES 10). The chain world of test (z) without light's emitter (the matter
    kind's faces periodic), the matter emitter's stock 2 (the residues from the law on
    W = 700), a receiver body of the matter family at x = 184 read as the set `screen`
    named by the emitter: each record clicks ONCE at the screen, at the first interval at
    which 2 W C >= (2 u + 1) T on its pointer there (read through the engine's
    `_ladder_click`; the interval before it below the rung), after the front's flight (84
    Links at the band's group pace 0.5: between 100 and 250 intervals after the birth), the
    line's `tick` its `click`, the record deleted whole at it; two gather lines in all, the
    books balanced at every interval."""
    document = matter_emitter_world(True, [77, 25], stock=2)
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
        dict(document["measured"][1], receiver="screen"),
    ]
    document["detectors"] = [{"name": "screen", "positions": [[184, 0, 0]], "threshold": 1}]
    world = parse_nature_beam_world(document)
    lines: list[dict] = []
    simulation = DetectorLawSimulation(world, observer=lines.append)
    identities = [1 * (1 << 32) + 1, 1 * (1 << 32) + 2]
    screen = simulation.cell_names.index("screen")
    at_click: dict[int, tuple[int, int, int, int]] = {}
    original = simulation._ladder_click

    def spy(live):
        pointer = live.pointers[screen]
        original(live)
        if live.clicked and live.identity not in at_click:
            at_click[live.identity] = (pointer, live.u, live.norm, live.wheel)

    simulation._ladder_click = spy  # type: ignore[method-assign]
    below: dict[int, int] = {}
    for _ in range(3000):
        simulation.step()
        assert simulation.books()["balanced"], simulation.tick
        for identity in identities:
            live = simulation.records.get(identity)
            if (
                live is not None
                and 2 * live.wheel * live.pointers[screen] < (2 * live.u + 1) * live.norm
            ):
                below[identity] = simulation.tick
        if len([line for line in lines if line["event"] == "gather"]) == 2:
            break
    gathers = [line for line in lines if line["event"] == "gather"]
    assert [gather["record"] for gather in gathers] == identities
    for gather in gathers:
        identity = gather["record"]
        assert gather["chosen"][0][0] == "screen" and gather["click"] == gather["tick"]
        pointer, u, norm, wheel = at_click[identity]
        assert wheel == 700 and 0 <= u < wheel and u == gather["u"]
        assert 2 * wheel * pointer >= (2 * u + 1) * norm and below[identity] == gather["click"] - 1
        assert 100 < gather["click"] - gather["birth"] < 250
        assert identity not in simulation.records


def test_ab_every_declared_wheel_is_refused_by_name():
    """The wheel is the record's own (ALGEBRA.md 9.22 (4); BUILD.md section 26 item 15): the
    world key `wheel`, a detector set's `wheel`, a block's `wheel` and an emitter's `wheel`
    are each refused by name with the successor named; the same for `residue_order` and
    `residue_seed` on an emitter, `absorbing` and `take` on a block, `take` on a family. The
    edge case: a world without any of them loads."""
    base = with_screen(block_world([240, 1, 1], CHAIN, [156, 157], [], emitter_at(100, 3)), 230)
    parse_nature_beam_world(base)
    for mutate, message in (
        (lambda d: d.__setitem__("wheel", 64), "the world.wheel is refused"),
        (lambda d: d["detectors"][0].__setitem__("wheel", 64), r"detectors\[0\]\.wheel is refused"),
        (lambda d: d["measured"][0].__setitem__("wheel", 64), r"measured\[0\]\.wheel is refused"),
        (
            lambda d: d["measured"][0]["emitter"].__setitem__("wheel", [1, 64]),
            r"measured\[0\]\.emitter\.wheel is refused",
        ),
        (
            lambda d: d["measured"][0]["emitter"].__setitem__("residue_order", "ordinal"),
            "residue_order is refused",
        ),
        (
            lambda d: d["measured"][0]["emitter"].__setitem__("residue_seed", 7),
            "residue_seed is refused",
        ),
        (lambda d: d["measured"][0].__setitem__("absorbing", True), "absorbing is refused"),
        (lambda d: d["measured"][0].__setitem__("take", [-15, 56]), r"measured\[0\]\.take is refused"),
        (lambda d: d["families"][1].__setitem__("take", [-19, 86]), r"families\[1\]\.take is refused"),
    ):
        document = json.loads(json.dumps(base))
        mutate(document)
        with pytest.raises(ValueError, match=message):
            parse_nature_beam_world(document)


def light_clock_world(faces: str, far_body: bool) -> dict:
    """DECLARATIONS.md section 10 with section 15's lines (M1-1, M1-3, M1-4, M1-10) and item 9,
    SINCE BUILD.md section 26: a chain of 173 (x `closed` for light, the zero face at 172 the
    mirror B sixty Links from A's face at 111; or x open, the sponges), the matter kind
    [800, 809], the emitter A of side 12 at [100, 112) at full depth with the seed 50 x 2^20
    on its bound mode, its `emitter` of light on the wheel [1, 64] with the stock 1 (one birth),
    W = 64; light's clock [1, 1]; the receiving set `A_face` bound to A at ONE declared Node,
    the free Node adjacent to A's face toward the mirror (x = 112; item 9), with its own wheel
    64 (line 7: a receiver), A's `receiver` by name; with `far_body`, a receiver body at x =
    160 read as the set `far` with its own wheel 64; the amplitude bound 2^32."""
    document = massive_world([173, 1, 1], {"x": faces, "y": "periodic", "z": "periodic"}, [800, 809])
    document["families"][0]["phase_per_link"] = [1, 1]
    document["ticks"] = 600
    document["clock_stamp"] = True
    document["measured"] = [
        {
            "position": [100, 0, 0],
            "family": "matter",
            "amount": 1,
            "phase": 0,
            "momentum": [0, 0, 0],
            "fixed": True,
            "side": 12,
            "pair": [800, 801],
            "seed": 50 << 20,
            "emitter": {"family": "light"},
            "margin": "control",
            # the receiver by name (section 13 item 7): A's own bound set
            "receiver": "A_face",
        }
    ]
    document["detectors"] = [{"name": "A_face", "block": 0, "positions": [[112, 0, 0]]}]
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
        document["detectors"].append({"name": "far", "positions": [[160, 0, 0]]})
    seed_source(document, 0)
    return document


def test_ac_the_receiving_set_beside_the_emitter_books_the_flux_and_clicks_at_its_rung():
    """Line 7 (the receiving set at ONE free Node) on the light clock's chain of 173 (W = 64;
    the world's `wheel` 64) SINCE THE FLUX READING (ALGEBRA.md 9.19 (3); BUILD.md section 26
    item 14): A's one born record is written once on A's twelve cells and leaves both ways;
    the set's Node x = 112 books the one-way flux into it from the first interval (its
    pointer above 0 and its rung at the record's own residue from the law, the click line written
    at that rung and stamped with A's count as the interval begins, named by
    `clock_source`), and the record is deleted whole at its click, with the faces closed
    and open alike (no `face` cell on the closed chain; `face` on the open one, last on the
    ladder and never reached first); nothing absorbs (the take retired). A receiver body at
    x = 160 read as `far` is a declared set off A's ladder (A names A_face): never chosen.
    The loader: `block` with a position on a measured Node refused, with two positions
    refused, `block` naming a body refused naming the positions form, `closed` without
    `detector_law` refused, `own_grace` on the emitter refused, a stock below 1 refused."""
    first = 1  # A's born record: block 0, birth 1
    for faces in ("closed", "open"):
        world = parse_nature_beam_world(light_clock_world(faces, faces == "open"))
        if faces == "closed":
            assert world.closed == (True, False, False) and world.boundary_per_axis["x"] == "closed"
        lines: list[dict] = []
        simulation = DetectorLawSimulation(world, observer=lines.append)
        assert ("face" in simulation.cell_names) == (faces == "open")
        a_face = simulation.cell_names.index("A_face")
        assert int(simulation.cell_index[112, 0, 0]) == a_face
        block = simulation.blocks[0]
        pointer_at_click: int | None = None
        original = simulation._ladder_click

        def spy(live, original=original, a_face=a_face):
            nonlocal pointer_at_click
            pointer = live.pointers[a_face]
            original(live)
            if live.clicked and live.identity == first and pointer_at_click is None:
                pointer_at_click = pointer

        simulation._ladder_click = spy  # type: ignore[method-assign]
        birth: int | None = None
        count_then: int | None = None
        for _ in range(600):
            count_before = block.count
            simulation.step()
            books = simulation.books()
            assert books["balanced"], simulation.tick
            live = simulation.records.get(first)
            if live is not None:
                birth = live.birth_tick
            if pointer_at_click is not None and count_then is None:
                count_then = count_before
        assert birth is not None and pointer_at_click is not None and pointer_at_click > 0
        gathers = [g for g in lines if g["event"] == "gather" and g["record"] == first]
        assert len(gathers) == 1 and gathers[0]["chosen"][0][0] == "A_face"
        line = gathers[0]
        # the rung (2 u + 1) T / (2 W) on the record's own residue from the law
        # decides how much of the record must pass the set before its click
        assert 0 <= line["click"] - birth <= 600 and line["tick"] == line["click"]
        assert 0 <= line["u"] < 2403
        assert line["clock_source"] == "measured:0" and line["clock"] == count_then
        assert first not in simulation.records
        assert all(g["chosen"][0][0] != "far" for g in lines if g["event"] == "gather")
    # the loader's refusals
    bad = light_clock_world("closed", False)
    bad["detector_law"] = False
    bad["massive_record"] = False
    del bad["amplitude_bound"]
    with pytest.raises(ValueError, match="closed"):
        parse_nature_beam_world(bad)
    on_body = light_clock_world("open", False)
    on_body["detectors"] = [{"name": "A_face", "block": 0, "positions": [[100, 0, 0]]}]
    with pytest.raises(ValueError, match="names a Node of a measured event"):
        parse_nature_beam_world(on_body)
    two = light_clock_world("open", False)
    two["detectors"] = [{"name": "A_face", "block": 0, "positions": [[112, 0, 0], [113, 0, 0]]}]
    with pytest.raises(ValueError, match="names ONE Node"):
        parse_nature_beam_world(two)
    no_block = light_clock_world("open", True)
    no_block["detectors"] = [{"name": "B", "block": 1}]
    with pytest.raises(ValueError, match="a receiver set on a BODY is `positions`"):
        parse_nature_beam_world(no_block)
    graced = light_clock_world("open", False)
    graced["measured"][0]["own_grace"] = 70
    with pytest.raises(ValueError, match="own_grace is refused"):
        parse_nature_beam_world(graced)
    empty = light_clock_world("open", False)
    empty["measured"][0]["amount"] = 0
    with pytest.raises(ValueError, match="amount"):
        parse_nature_beam_world(empty)


def test_ah_a_set_at_a_blocks_cells_books_the_flux_into_them_and_steps_with_the_block():
    """Line 7 for a set bound to a block WITHOUT positions (R2's form, DECLARATIONS.md section 13
    item 1) under the flux reading (ALGEBRA.md 9.19 (3)): the block's twelve cells are the
    set's Nodes (the cell index at them the set's cell); an emitter's record (the emitter
    body of the source kind at x = 150 on a chain of 300, fifty Links before the block, two
    births on the wheel [1, 64], the emitter naming the set) books its one-way flux into the
    block's cells to the set and clicks once there, the click stamped with the block's own
    count as the interval began and named by `clock_source`, the record deleted whole at
    it, the books balanced; nothing absorbs. Pushed toward the emitter at k = 3 (the block
    stepping, its cells and the set's Nodes following it): the record still clicks once at
    the set, the books balanced. The loader: a set's `wheel` refused by name."""
    for momentum in ([0, 0, 0], [-64, 0, 0]):
        document = massive_world([300, 1, 1], CHAIN, [800, 809])
        document["ticks"] = 1200
        document["age_bound"] = 1 << 20
        document["clock_stamp"] = True
        document["families"].append(source_family())
        document["measured"] = [
            dict(emitter_at(150, 2), receiver="B_cells"),
            {
                "position": [200, 0, 0],
                "family": "matter",
                "amount": 1,
                "phase": 0,
                "momentum": momentum,
                "fixed": True,
                "side": 12,
                "pair": [800, 801],
                "seed": 50 << 20,
                "margin": "control",
            },
        ]
        document["detectors"] = [{"name": "B_cells", "block": 1}]
        seed_source(document, 0)
        world = parse_nature_beam_world(document)
        lines: list[dict] = []
        simulation = DetectorLawSimulation(world, observer=lines.append)
        block = simulation.blocks[1]
        cell = simulation.cell_names.index("B_cells")
        assert int(simulation.cell_index[205, 0, 0]) == cell
        identity = 0 * (1 << 32) + 1
        count_at_rung: int | None = None
        for _ in range(1200):
            count_before = block.count
            simulation.step()
            assert simulation.books()["balanced"], simulation.tick
            found = [g for g in lines if g["event"] == "gather" and g["record"] == identity]
            if found and count_at_rung is None:
                count_at_rung = count_before
                break
        gathers = [g for g in lines if g["event"] == "gather" and g["record"] == identity]
        assert len(gathers) == 1 and gathers[0]["chosen"][0][0] == "B_cells", gathers
        assert gathers[0]["clock_source"] == "measured:1" and gathers[0]["clock"] == count_at_rung
        assert gathers[0]["tick"] == gathers[0]["click"] and identity not in simulation.records
        assert block.stepped > 0 if momentum[0] else block.stepped == 0
        assert np.array_equal(simulation.cell_index == cell, block.mask)
    bad = document
    bad["detectors"] = [{"name": "B_cells", "block": 1, "wheel": 64}]
    with pytest.raises(ValueError, match="wheel is refused"):
        parse_nature_beam_world(bad)


def test_al_a_block_that_steps_off_the_board_refuses_the_interval():
    """Reviewer 3's line from the redshift dry run (BUILD.md section 18): a block pushed toward
    a zero face (momentum [-64, 0, 0] from x = 30 on the open chain of 300, one hop per three
    intervals) refuses the run at the interval its cells would leave the board, naming the block
    and the interval, instead of running on with the block gone; before that interval it steps
    and the books balance. The edge case: on a periodic chain the same block wraps and steps on
    through 400 intervals with no refusal."""
    for boundary, faces, refused in ((CHAIN, {"x": "open"}, True), (PERIODIC_CHAIN, None, False)):
        document = massive_world([300, 1, 1], boundary, [800, 809], faces=faces)
        document["ticks"] = 400
        document["age_bound"] = 1 << 20
        document["clock_stamp"] = True
        document["measured"] = [
            {
                "position": [30, 0, 0],
                "family": "matter",
                "amount": 1,
                "phase": 0,
                "momentum": [-64, 0, 0],
                "fixed": True,
                "side": 12,
                "pair": [800, 800],
                "seed": 50 << 20,
                "margin": "control",
            }
        ]
        simulation = DetectorLawSimulation(parse_nature_beam_world(document))
        block = simulation.blocks[0]
        if refused:
            with pytest.raises(RuntimeError, match=r"measured\[0\] stepped off the board at interval"):
                for _ in range(400):
                    simulation.step()
                    assert simulation.books()["balanced"]
            assert block.stepped > 20 and simulation.tick < 400
        else:
            for _ in range(400):
                simulation.step()
            assert block.stepped > 100 and int(np.count_nonzero(block.mask)) == 12


def test_ad_a_wall_of_lights_kind_is_a_mirror_line():
    """DECLARATIONS.md section 15 L-1 (the (M) wall's path): a mirror line of blocks of light's
    kind with the pair [1, 2], two Nodes deep, on the first build's chain (x = 40 and 41; the
    lamp at x = 2, the screen at x = 70): the blocks have no own record, no clock and no
    coupling (the loader sets their seed 0; the engine's blocks' loop skips them; the margin
    rule skips light's kind), light's pair arrays carry [1, 2] at the two cells and [1, 1]
    elsewhere; over 200 intervals the largest level beyond the wall (x in [45, 69]) stays below
    four percent of the largest level before it (x in [10, 38]; the engine reads 3.1 percent
    on the one-cell birth beside the declaration's 0.7 percent of the amplitude and the
    train's 1.45, the front's precursor included, COMPUTATION), the books balanced at every
    interval; a light-kind block with
    `seed`, `coupling` or `margin` refused. The chain's source is the emitter body of
    section 26 (a block itself, of the matter kind, with its own record)."""
    document = chain_world()  # the closed chain (BUILD.md section 26 item 14)
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
    assert [entry.block is not None for entry in world.measured] == [True, False, True, True]
    assert world.measured[2].block is not None and world.measured[2].block.seed == 0
    simulation = DetectorLawSimulation(world)
    assert all(block.own is None for block in simulation.blocks[1:])
    assert int(simulation.kind_den[0][40, 0, 0]) == 2 and int(simulation.kind_den[0][41, 0, 0]) == 2
    assert int(simulation.kind_den[0][39, 0, 0]) == 1 and int(simulation.kind_num[0][40, 0, 0]) == 1
    before = beyond = 0
    for _ in range(200):
        simulation.step()
        assert simulation.books()["balanced"], simulation.tick
        for live in simulation.records.values():
            if live.family != 0:
                continue
            before = max(before, int(np.max(np.abs(live.now[10:39, 0, 0]))))
            beyond = max(beyond, int(np.max(np.abs(live.now[45:70, 0, 0]))))
    assert before > 0 and beyond * 100 < 4 * before, (before, beyond)
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
    world = parse_nature_beam_world(matter_emitter_world(False, [77, 25]))
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
