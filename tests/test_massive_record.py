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
its exemption and its own take are retired: its Nodes are Nodes like every other)."""

from __future__ import annotations

import hashlib
import json

import numpy as np
import pytest

from event_universe.diagnostics.massive_record_margin import (
    block_margin,
    check_margins,
    iterated_mode,
    profile_check,
)
from event_universe.events.detector_law import UNIT, DetectorLawSimulation, LiveRecord, form_json
from event_universe.events.world import (
    LIGHT_PAIR,
    MASSIVE_RECORD_RULE,
    input_stamp,
    parse_nature_beam_world,
)
from tests.test_detector_law import (
    chain_world,
    cube_positions,
    emitter_body,
    receiver_body,
    receiver_cube,
)
from tests.test_emitter import (
    CHARGE_FAMILY,
    CHARGE_FAMILY_NAME,
    CHARGE_STRENGTH,
    CLOCK_FAMILY,
    CLOCK_FAMILY_NAME,
    NODE_CLOCK,
    lawful_wheel,
    massive_generator,
)


def massive_world(shape: list[int], boundary: object, pair: list[int]) -> dict:
    """A world of the massive kind `matter` (its pair on the six-neighbour term) beside light,
    no lamp, no block (the rule's tests construct a record's rows directly); every family
    reads the world's `boundary` (one border, BUILD.md section 26 item 28) and the face slab
    is one Node deep where the board is open (`face_depth`, declared: no default)."""
    matter: dict = {"name": "matter", "quantum": 1, "pair": pair, "charge": 0}
    return {
        "law": "beam",
        "model_id": "beam-massive-record-rule-v1",
        "shape": shape,
        "boundary": boundary,
        "face_depth": 1,
        "ticks": 10,
        "K": 1073741824,
        "N": 1024,
        "release": [1, 128],
        "suspension": 0,
        "detector_law": True,
        "massive_record": True,
        "amplitude_bound": 1 << 28,
        "node_clock": NODE_CLOCK,
        "clock_family": CLOCK_FAMILY_NAME,
        "charge_family": CHARGE_FAMILY_NAME,
        "charge_strength": CHARGE_STRENGTH,
        "directions": [],
        "families": [
            {"name": "light", "quantum": 1, "phase_per_link": [512, 1], "charge": 0},
            matter,
            dict(CLOCK_FAMILY),
            dict(CHARGE_FAMILY),
        ],
        "measured": [],
        "detectors": [],
    }


def planted(
    simulation: DetectorLawSimulation, family: int, now: np.ndarray, before: np.ndarray, r: np.ndarray
) -> LiveRecord:
    """A record's rows given to the rule's step directly (the test's device: no lamp givings a
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
        pointers=[0] * len(simulation.detector_names),
        first_rung=[None] * len(simulation.detector_names),
        age=10,
    )


def step_once(simulation: DetectorLawSimulation, live: LiveRecord) -> tuple[np.ndarray, np.ndarray]:
    """One step of the rule; returns (a_next, r') from the record's rows after the step."""
    simulation._advance(live)
    return live.now.copy(), live.remainder.copy()


def test_the_rule_on_a_chain_against_section_ones_integers():
    """BUILD.md (a): the kind [2, 3] on a 5-Node open chain (y, z one layer periodic, so
    S_6 = a_W + a_E + 4 a_now with 0 beyond the ends); the totals num S_6 - 9 a_before + r
    are [1, 27, -56, 19, 7], a_next = [0, 3, -7, 2, 0], r' = [1, 0, 7, 1, 7]. UNDER THE NODE
    CLOCK (BUILD.md section 26 item 31) the vacuum's wall is 9 Gamma and the remainder Gamma
    times the line's, the levels bit for bit: r and r' here are the line's times Gamma."""
    world = parse_nature_beam_world(
        massive_world([5, 1, 1], {"x": "open", "y": "periodic", "z": "periodic"}, [2, 3])
    )
    simulation = DetectorLawSimulation(world)
    now = np.array([0, 5, -7, 3, 0]).reshape(5, 1, 1)
    before = np.array([1, 0, 2, -1, 0]).reshape(5, 1, 1)
    r = np.array([0, 1, 2, 0, 1]).reshape(5, 1, 1) * NODE_CLOCK
    live = planted(simulation, 1, now, before, r)
    a_next, r_next = step_once(simulation, live)
    assert a_next.ravel().tolist() == [0, 3, -7, 2, 0]
    assert r_next.ravel().tolist() == [value * NODE_CLOCK for value in (1, 0, 7, 1, 7)]
    assert all(0 <= value < 9 * NODE_CLOCK for value in r_next.ravel().tolist())
    # T: the row's past is the amplitude the step read
    assert live.before.ravel().tolist() == [0, 5, -7, 3, 0]


def test_the_rule_at_a_corner_of_an_open_board():
    """BUILD.md (b): the kind [1, 2] (3 den = 6) at the corner (0, 0, 0) of an open 2^3 board
    of the massive kind (the world's faces open on every axis, one border): a_now 4 with the three
    neighbours 3, -2, 5 and three zero faces, a_before 1, r 5: the total 5, a_next 0, r' 5;
    with a_before -2 the total 23, a_next 3, r' 5."""
    world = parse_nature_beam_world(massive_world([2, 2, 2], "open", [1, 2]))
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


def test_lights_pair_is_the_first_builds_integers_bit_for_bit():
    """BUILD.md (c): on the first build's random chain the step at light's pair [1, 1] gives the
    same quotient as the line 3 a_next + r' = S_6 - 3 a_before + r, the total and the remainder
    Gamma times the line's (the Node clock in the vacuum, BUILD.md section 26 item 31) on
    every Node without content whose six reads have none; at the emitter body's 32 Nodes and
    the screen's three (their content M) and at the Nodes beside them the line under the
    Node's own pace (item 36), 3 Gamma a_next + r' = (Gamma - c_i) S_6(a_now)_i + 6 c_i a_now -
    3 Gamma a_before + r (tests/test_node_clock.py reads it on random rows too)."""
    world = parse_nature_beam_world(chain_world())
    simulation = DetectorLawSimulation(world)
    assert world.families[0].pair == LIGHT_PAIR
    assert np.all(simulation.kind_num[0] == 1) and np.all(simulation.kind_den[0] == 1)
    rng = np.random.default_rng(7)
    now = rng.integers(-UNIT, UNIT, size=(80, 1, 1), dtype=np.int64)
    before = rng.integers(-UNIT, UNIT, size=(80, 1, 1), dtype=np.int64)
    remainder = rng.integers(0, 3, size=(80, 1, 1), dtype=np.int64) * NODE_CLOCK
    live = planted(simulation, 0, now, before, remainder)
    live.age = 1000
    total = NODE_CLOCK * (simulation._neighbours(now) - 3 * before) + remainder
    expected_next = np.floor_divide(total, 3 * NODE_CLOCK)
    expected_remainder = total - 3 * NODE_CLOCK * expected_next
    a_next, r_next = step_once(simulation, live)
    content = simulation.node_content
    free = (content == 0) & (simulation._neighbours(content, simulation.kind_wrap[0]) == 0)
    assert 30 <= int(np.sum(free)) <= 45
    assert np.array_equal(a_next[free], expected_next[free])
    assert np.array_equal(r_next[free], expected_remainder[free])
    wall = 3 * NODE_CLOCK
    # the Node's own pace on its six-neighbour sum (item 36)
    clocked = (NODE_CLOCK - content) * simulation._neighbours(now, simulation.kind_wrap[0])
    clocked += 6 * content * now - wall * before + remainder
    assert np.array_equal(a_next, np.floor_divide(clocked, wall))
    assert np.array_equal(r_next, clocked - wall * np.floor_divide(clocked, wall))


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


def test_the_conserved_form_holds_to_the_remainders_jitter():
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
        assert simulation.books()["families"]["matter"]["form"] == form_json(
            simulation.record_form(live)
        )
        # light's pair on the same seed: the checkerboard's stationary alternation, one unit
        light = planted(simulation, 0, now, before, np.zeros((6, 6, 6), dtype=np.int64))
        light.age = 1000
        for _ in range(200):
            step_once(simulation, light)
            assert abs(int(np.sum(light.now * checker)) // 216) == 1


def test_every_family_reads_the_worlds_border_and_a_zero_face_when_open():
    """ONE BORDER FOR EVERY FAMILY (BUILD.md section 26 item 28; was BUILD.md (m), the
    kind's own periodic faces): on a 5 x 1 x 1 board whose world `boundary` is periodic on
    x the massive kind wraps (Node 0 reads Node 4 as its -x neighbour); on a board open on
    x the neighbour beyond the face reads 0 for the massive kind as for light."""
    for boundary, expected in (({"x": "periodic", "y": "periodic", "z": "periodic"}, 9), (CHAIN, 0)):
        document = massive_world([5, 1, 1], boundary, [1, 2])
        document["age_bound"] = 100000
        world = parse_nature_beam_world(document)
        assert world.kind_periodic(1) == world.periodic == world.kind_periodic(0)
        simulation = DetectorLawSimulation(world)
        now = np.array([0, 0, 0, 0, 9]).reshape(5, 1, 1)
        zero = np.zeros((5, 1, 1), dtype=np.int64)
        live = planted(simulation, 1, now, zero, zero)
        a_next, r_next = step_once(simulation, live)
        # at Node 0: the total Gamma num S_6 = Gamma x (a_W + a_E + 4 x 0) = Gamma a_W,
        # divided by the vacuum's wall 6 Gamma (the Node clock, item 31)
        total = 6 * NODE_CLOCK * int(a_next[0, 0, 0]) + int(r_next[0, 0, 0])
        assert total == NODE_CLOCK * expected
    assert world.kind_periodic(1) == (False, True, True)
    assert world.kind_periodic(0) == (False, True, True)
    # the world open on every axis: every family open on every axis (the massive kind's
    # periodic default of the first builds, HISTORY)
    everywhere = parse_nature_beam_world(massive_world([5, 1, 1], "open", [1, 2]))
    assert everywhere.kind_periodic(1) == everywhere.kind_periodic(0) == (False, False, False)


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


def test_the_light_record_is_byte_identical_without_the_key():
    """BUILD.md (p): the first build's chain world over 600 intervals gives the digests read at
    the head f4a3971a before any line of the build was written: the state and the audit
    the witness that the rows are byte for byte; the events' digest moved ONCE, at the GO's
    fold (BUILD.md section 14), by the two fields added to every gather line (`click_at`,
    `clock_source`; the gate reviewer's line on the click's time and key (i)), and the audit's digest once, by issue
    #1086's momentum books (the blocks' held momentum, the transit and escape not accounted,
    the scope of `balanced` named), every other field byte for byte; then all three once more
    by item 10 (the lamp's own take of its record from the first interval after the train, the
    record alive at 600 carrying its pointers; BUILD.md section 18); then all three once more
    by the emitter as a clicking body (BUILD.md section 26: the chain world's lamp an emitter
    body of the kind [7, 8] on the well [8, 7], six givings at their rungs, the grace and the
    own take retired), then once more by the write on the circle of 2 N with before = -now
    and the excited record's norm as the one-way flux into its centre Node over one period
    (ALGEBRA.md 9.17 (5) and (6), 9.19 (3); BUILD.md section 26 item 13), then once more by
    the flux reading at every detector with the cumulative ladder and the deletion at the click,
    on the chain world's faces closed (item 14), then once more by the residue from the law
    on the rich well [801, 700] with the take's data gone (item 15), then the events and the
    audit once more by the given pair on the clock's half step (item 17), then the state and the
    audit once more by the detector cube at [70, 72] (item 18; the events unchanged, the six
    clicks at the same intervals), then all three by the emitter's coupling to the light it
    givings and the residue read after the excited record's first advance (item 19), the
    digests read at that head; then the state once more by the `extents` of every block
    written beside its `side` on the snapshot (item 23; the events and the audit unchanged),
    then the events and the audit by the click rule of ALGEBRA.md 9.17 (7) (f) (the model
    owner's word, record 1918; item 24: the excited record's running total accruing its
    centre Node's share of its conserved form, the emitter's seed raised to 2^20, the six
    givings at (2 u + 1) P / (2 W) after their reads; the state at 600 unchanged), then all
    three by the generator as the operator iterated with the stop (the owner's word of
    2026-09-25; item 25: the emitter's seed and clock the iteration's, within the floor of
    the eigensolver's), then all three by the generator's working amplitude 2^28 (the names'
    regeneration of 2026-09-25, item 25 amended: the muon layer's well hovered at 1.5 times
    the bound at 2^20; the emitter's profile and clock the iteration's at 2^28), then all
    three by THE GIVEN TRAIN (ALGEBRA.md 9.17 (6a); item 27: the chain world's emitter body
    the train's 32 Nodes at [2, 34) with the well [699, 700], light on the given clock
    [512, 1] of N = 1024, every giving the train written on the Nodes), the digests read at
    that head; SINCE THE TIGHTENINGS (BUILD.md section 26 item 28) the closed chain bounds
    matter too (one border for every family: the events and the audit moved, the state
    digest unchanged); SINCE THE REMAINDER KEPT (the model owner's decision (1) of record
    1962; BUILD.md section 26 item 29) the residues of the stock's givings spread from the
    kept remainder and all three digests moved; SINCE THE COUPLING RETIRED (decision (2),
    item 30) the excited record and the given light advance by the rule alone and all three
    moved once more; SINCE THE NODE CLOCK (decision (5), item 31) all three moved once more
    (the remainders Gamma times the plain ones in the vacuum and the wall of the body's
    content at its Nodes, the wheel and the residues read there, the norms on the lines in
    the clock's units); SINCE THE RENAME (record 1978, no cell) the events digest moved once
    more with the two line fields' names, the giving line's `nodes` and the gather line's
    `detectors` (the state and the audit unchanged); SINCE THE FAMILY OF CLICKS (ALGEBRA.md
    9.45; item 32) all three moved once more (the fourth family declared in the chain world,
    one record of it over the board, held at the bodies' Nodes at their content and
    spreading from them by the plain step, every Node's clock pair read from its level);
    SINCE THE RESEED RETIRED (ALGEBRA.md 9.43 (3), 9.44 (5) (c); item 33) all three moved
    once more (the body's own record continuing under its one identity, its levels never
    rewritten, the residues read at the click at the first shell Node, the givings at the
    counted intervals, the giving lines' fields); SINCE THE FIXED WALL (the model owner's
    record 1994; item 34) all three moved once more (the paced reads at and beside the
    bodies, the forms' units Gamma squared, the giving lines' `read_clocks`); SINCE THE FAMILY
    OF CHARGE (ALGEBRA.md 9.48; item 35) all three moved once more (the fifth family declared
    in the chain world, one record of it over the board held at the bodies' Nodes at their
    charge 0, the giving lines' `charge`, the snapshot's `charge` entry; the rows bit for bit);
    SINCE THE NODE'S OWN PACE (ALGEBRA.md 9.50 (13); item 36) all three moved once more (the
    pace on the Node's own sum at and beside the bodies, the forms as exact rationals, the
    giving lines' `pace`, the plain flux); SINCE THE BODY RECORD (ALGEBRA.md 9.46; item 37)
    the state digest moved once more (the block entry's `rotation`, None under the lattice
    body; the events and the audit unchanged); SINCE THE GIVING CLICK (record 2016) the events
    and the state digests moved with the lines' names alone (`giving` for `birth`,
    `given_norm` for `born_norm`; the state's record entries carry `giving`); SINCE THE SEAT (ALGEBRA.md 9.60; item 42) the state digest moved once more (the block
    entry's `seat` for `rotation`, None under the lattice body; the events and the audit
    unchanged: the one rule factored and the support box of item 43 bit for bit); read again at
    this head."""
    assert run_chain_digests() == {
        "events": "43abd129081c637469bf0a39795c2e0bd1db59c2e94f1e6c75ddfc10ab5fd844",
        "state": "387a7111fd1ba06d7d86a4e90edbc40f9efedc9f5a67b7922c5cb4016fce6abb",
        "audit": "18fceec9b9d8e12e478abd84633b08f013658858f3ccb76d17fe61c28b53597e",
    }


def test_the_loaders_refusals_name_the_key():
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
    # one border for every family (BUILD.md section 26 item 28): the family key `faces`
    # refused by name on the massive kind and on light's alike
    for family in (0, 1):
        faced = json.loads(json.dumps(base))
        faced["families"][family]["faces"] = {"x": "open"}
        with pytest.raises(ValueError, match=rf"families\[{family}\]\.faces is refused: one border"):
            parse_nature_beam_world(faced)
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
    del no_law["face_depth"]  # the face slab is the detector law's (refused without it)
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


def test_the_records_keys_under_the_key_and_none_without_it():
    """BUILD.md (r): the identity under `hypotheses`, the families' pair and the books'
    form under the key; nothing of them without it (the first build's world); every
    family's faces the world's (one border, BUILD.md section 26 item 28)."""
    world = parse_nature_beam_world(
        massive_world([4, 4, 4], {"x": "open", "y": "periodic", "z": "open"}, [2, 3])
    )
    assert MASSIVE_RECORD_RULE in world.hypotheses
    assert world.families[1].pair == (2, 3) and world.families[1].massive_kind
    assert world.kind_periodic(1) == (False, True, False) == world.kind_periodic(0)
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
    assert plain.kind_periodic(0) == plain.periodic
    assert "form" not in DetectorLawSimulation(plain).books()["families"]["light"]


# The block (STEP 3 of the build: BUILD.md section 6, (e) to (l))


def block_world(
    shape: list[int],
    boundary: object,
    kind: list[int],
    blocks: list[dict],
    source: dict | None = None,
    ticks: int = 100,
) -> dict:
    """A world of the massive kind `matter` with blocks (measured events of `matter` with
    `side`), a light family with the chain test's clock [77, 25] (the period 20.8 intervals,
    lambda 12 Links), and optionally an emitter body of light (`emitter_at`, a well of the
    source family) as the first measured event, seeded on its bound mode (the generator's
    profile at its scalar seed); every well declares its seed (the suite's amplitude 2^20
    where a test names none: no loader default, BUILD.md section 26 item 28) and the face
    slab is one Node deep where the board is open."""
    matter: dict = {"name": "matter", "quantum": 1, "pair": kind, "charge": 0}
    # light on the given clock [512, 1] of N = 1024 (the given train, ALGEBRA.md 9.17 (6a))
    families = [{"name": "light", "quantum": 1, "phase_per_link": [512, 1], "charge": 0}, matter]
    measured: list[dict] = []
    if source is not None:
        measured.append(source)
        families.append(source_family())
    families.append(dict(CHARGE_FAMILY))  # the family of charge (item 35)
    families.append(dict(CLOCK_FAMILY))  # the family of clicks (BUILD.md section 26 item 32)
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
            "seed",
            "ramp",
            "start",
            "margin",
            "held",
            "receiver",
            "emitter",
        ):
            if key in block:
                entry[key] = block[key]
        if "seed" not in entry and block["pair"][0] * kind[1] > block["pair"][1] * kind[0]:
            # every well declares its seed (no loader default, BUILD.md section 26 item
            # 28): the suite's amplitude 2^20 where a test names none
            entry["seed"] = 1 << 20
        measured.append(entry)
    document: dict = {
        "law": "beam",
        "model_id": "beam-massive-record-block-v1",
        "shape": shape,
        "boundary": boundary,
        "face_depth": 1,
        "ticks": ticks,
        "K": 1073741824,
        "N": 1024,
        "release": [1, 128],
        "suspension": 0,
        "clock_stamp": True,
        "detector_law": True,
        "massive_record": True,
        "amplitude_bound": 1 << 28,
        "node_clock": NODE_CLOCK,
        "clock_family": CLOCK_FAMILY_NAME,
        "charge_family": CHARGE_FAMILY_NAME,
        "charge_strength": CHARGE_STRENGTH,
        "directions": [],
        "families": families,
        "measured": measured,
        "detectors": [],
    }
    if source is not None:
        seed_source(document, 0)
    return document


def seed_source(document: dict, number: int) -> None:
    """The measured event `number` (an emitter body, a one-Node well) seeded on its bound
    mode at its scalar seed (the generator's `mode_profile`, the world's other blocks left as
    declared), its `margin` made explicit."""
    entry = document["measured"][number]
    entry.setdefault("margin", "control")
    generator = massive_generator()
    entry["seed"] = generator.mode_profile(document, number, amplitude=entry["seed"])
    if "emitter" in entry:
        generator.given_train(document, number)
    # the input stamp (record 1886): the law and the hash of the integers
    document["input"] = input_stamp(document)


def with_screen(document: dict, x: int) -> dict:
    """The receiver by name for a test world's emitter body (DECLARATIONS.md section 13
    item 7): the cube of side 3 of light bodies at [x, x + 2] read as the set `screen`
    (record 1899; no wheel: the rung's wheel is the record's own, ALGEBRA.md 9.22 (4))."""
    receiver_cube(document, "screen", [x, 0, 0])
    document["input"] = input_stamp(document)  # the stamp over the whole file (item 28)
    return document


SOURCE_KIND = [7, 8]  # the emitter bodies' own kind (omega_0 = 0.505; the index worlds')
SOURCE_WELL = [
    699,
    700,
]  # its well over the train's 32 Nodes, rich (W = 700, ALGEBRA.md 9.22 (4)) and bound (2 cos omega_b = 1.9944 on a chain; the one-Node giving's [801, 700] is a runaway over 32 Nodes, its interior above 1)


def source_family() -> dict:
    """The emitter bodies' massive family `source` (the kind SOURCE_KIND, no clock)."""
    return {"name": "source", "quantum": 1, "pair": list(SOURCE_KIND), "charge": 0}


def emitter_at(
    x: int,
    stock: int = 1,
    family: str = "light",
    own: str = "source",
    pair: list[int] | None = None,
    receiver: object = None,
) -> dict:
    """An emitter body on a chain (ALGEBRA.md 9.17 (4), 9.17 (6a)): the well of the massive
    family `own` (the well `pair`, SOURCE_WELL by default) over the train's 32 Nodes from x,
    its train along +x, with the scalar seed 2^20
    (its profile on the mode by `seed_source`; at 100 the given light's back-action swamps
    the excited record, ALGEBRA.md 9.17 (7) (c)), `stock` excitations, the given family
    `family`; with `receiver`, the given records' ladder by name. The residue and the wheel
    are the law's (9.22 (4): W = 700 on SOURCE_WELL); the cadence of the excitations under
    the click rule of 9.17 (7) (f) (BUILD.md section 26 item 24): the residue u clicks
    (2 u + 1) P / (2 W) intervals after its read, P the mode's period."""
    entry = emitter_body([x, 0, 0], stock, receiver=receiver, family=family)
    entry["family"] = own
    entry["pair"] = list(pair or SOURCE_WELL)
    return entry


CHAIN = {"x": "open", "y": "periodic", "z": "periodic"}


def test_the_blocks_cells_and_its_pair_on_them():
    """BUILD.md (e): a block of side 3 at (2, 2, 2) on an open 8^3 board of the kind [800, 809]
    with the well [800, 800]: den reads 809 on every Node but the 27 Nodes, 800 there, num 800
    everywhere; the Nodes are the cube. The edge case: a pair that is no well is refused."""
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
    # its seed and clock keys refused; the kind's own pair refused (no cavity, item 28)
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


def test_the_blocks_drive_steps_its_cells_and_leaves_the_rows():
    """BUILD.md (f): a block of content 1 with P = 64 on x (the wall 3 Q S M = 192) steps at the
    intervals 3, 6, 9 with the remainder 0; with P = 70 at 3, 6, 9 with the remainders 18, 36,
    54 and at 11 with the remainder 2; the Nodes and the pair arrays move, the record's rows
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
    # the rows stayed: the seeded record's rows are still centred on the old Nodes
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


def test_an_emitter_body_givings_in_turn_each_giving_one_quantum_of_its_stock():
    """BUILD.md (h) SINCE section 26 (the emission by the coupling's source term retired with
    the lamp; an emitter is a clicking body, ALGEBRA.md 9.17 (4)): an emitter body of the
    source kind (the one-Node well SOURCE_WELL at x = 100 seeded on its mode, the stock 3)
    on the chain of 240 with the screen at 230: three givings in turn, the residues the
    law's, each given record of content 1 moved from the stock (`held_spent` 3 of the
    source family, `transit_released` 3 of light), the body's own record continuing under its
    one identity after every giving and after the stock is spent, never rewritten (ALGEBRA.md
    9.43 (3); item 33), the books balanced at every tick. The
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
            ),
            230,
        )
    )
    lines: list[dict] = []
    simulation = DetectorLawSimulation(world, observer=lines.append)
    for _ in range(600):
        simulation.step()
        assert simulation.books()["balanced"], simulation.tick
    givings = [line for line in lines if line["event"] == "giving"]
    assert len(givings) == 3
    # the residues from the law (ALGEBRA.md 9.22 (4)) on the body's own wheel (700
    # on the source well in the vacuum; at its Node the wheel of its content under
    # the Node clock, 9.35 (2), read from the rule), spread from the remainder
    # kept at the Nodes (the model owner's decisions (1) and (2) of record 1962;
    # the coupling's back-action HISTORY)
    assert all(lawful_wheel(world, line) for line in givings)
    assert [line["content"] for line in givings] == [3, 2, 1]
    assert len({line["u"] for line in givings}) > 1
    assert simulation.ledger.held_spent[2] == 3 and simulation.ledger.transit_released[0] == 3
    own = simulation.blocks[0].own
    assert own is not None and own.identity == 0  # the standing record continues (9.43 (3))
    assert all(
        live.family == 0 and live.content == 1 for live in simulation.records.values() if live is not own
    )
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


def test_a_seeded_block_at_rest_counts_its_cycles():
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


def test_the_pace_bound_refuses_one_link_per_interval():
    """The pace bound 3 (P . P) < (3 Q S M)^2 (MASSIVE_RECORD.md section 5): K = 1 (P = 192
    on x, one Link every interval) is refused naming the bound. The index in motion (the
    drive's pair carried as the coupling's g, BUILD.md (l)) is HISTORY with the coupling
    (the model owner's decision (2) of record 1962)."""
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


def test_the_margin_rule_refuses_below_the_margin_and_prints_the_extent():
    """BUILD.md (n): (1) the s = 28 block of world (i-b) on the periodic 48^3 board is refused as
    a pin world naming x, the extent (about 7.9 Links) and the side needed (about 60 > 48), and
    admitted as a control (44 < 48); (2) a block of s = 20 whose Nodes lie 3 Links from an open
    massive face is refused as a control (3 < 5.7) naming the axis and the distance; (3) the
    kind [800, 809] with the well [800, 808] at s = 3 (far below the threshold) is refused: on a
    finite periodic box the unbound case reads as an extent beyond the board (261 Links against
    24), the refusal the margin's; (4) the extent printed for (i-a) on 48^3 is 5.73 within 0.05
    Links (the float scratch of the plan) and its mode 0.1105 (the design's 96^3 box 0.1107);
    (5) BUILD.md section 26: a well too deep for its board is a RUNAWAY (the largest
    eigenvalue at or above 2, no oscillation, a level growing every interval; the one-Node
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
        CHAIN,
        [800, 809],
        [{"position": [3, 14, 14], "side": 20, "pair": [800, 800], "margin": "control"}],
    )
    near["age_bound"] = 100000
    with pytest.raises(ValueError, match="Nodes lie 3 Links from a zero face"):
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
    runaway = block_world([200, 1, 1], CHAIN, [800, 809], [deep])
    runaway["age_bound"] = 100000
    reading = block_margin(parse_nature_beam_world(runaway), 0)
    assert reading.runaway and reading.omega_b == 0.0 and abs(reading.lambda_max - 2.032) < 0.002
    with pytest.raises(ValueError, match="the block's mode is a runaway"):
        check_margins(parse_nature_beam_world(runaway))
    cube = block_world([24, 24, 24], PERIODIC, [800, 809], [dict(deep, position=[10, 10, 10])])
    cube["age_bound"] = 100000
    assert not block_margin(parse_nature_beam_world(cube), 0).runaway


def test_the_cavity_is_refused_by_name():
    """THE CAVITY RETIRED (BUILD.md section 26 item 28; was BUILD.md (o), the cavity of form
    (I) counting the separable form's cycles): a block declaring `cavity` is refused by name
    with what stands in its place (a body's record held by the law alone, its border the
    world's), true and false alike; the kind's own pair stays no body."""
    for value in (True, False):
        document = block_world(
            [24, 24, 24],
            PERIODIC,
            [800, 809],
            [{"position": [10, 10, 10], "side": 5, "pair": [800, 800], "margin": "control"}],
        )
        document["age_bound"] = 100000
        document["measured"][0]["cavity"] = value
        with pytest.raises(ValueError, match=r"measured\[0\]\.cavity is refused .*the cavity retired"):
            parse_nature_beam_world(document)


# The series' two keys of step 5 (BUILD.md section 4 step 7 and section 5 (v-m))


def test_the_drives_start_and_the_ramp_counted_from_it():
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


def test_the_mode_line_sums_lights_field_by_residue_class():
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


def test_the_load_bound_of_a_pair_names_the_bound_and_the_pair():
    """MUST 3 UNDER THE NODE CLOCK (BUILD.md section 26 item 31): a kind's pair whose rule total
    at the world's declared amplitude bound A with the clock Gamma = 10^6 and the world's
    content M reaches 2^63 is refused at load naming the bound, the clock, the content and
    the pair (A = 2^28, [2^20, 2^20 + 1]: 10^6 x 2^20 x 6 x 2^28 above 2^63, admitted by the
    plain rule's first pass on the pair alone); [800, 809] is admitted (1.9 x 10^18) and so
    is the muon layer's [3200, 3236] (7.8 x 10^18, the largest registered pair); a block's
    pair is checked the same way with the world's content, M twice it for the family of
    clicks' waves ([big, big + 1] refused naming measured[0] and M = 2, [800, 800] admitted). The world key (issue #1085): a massive world
    without `amplitude_bound` is refused naming it; the ceiling 2^28 (2^29 refused naming
    it); a seed above the bound is refused naming the bound and the pair (a seed of 2^60 at
    A = 2^28); the key without `massive_record` refused; a planted row above the bound stops
    the run at its interval."""
    big = 1 << 20
    document = massive_world([6, 6, 6], PERIODIC, [big, big + 1])
    document["age_bound"] = 100
    with pytest.raises(
        ValueError,
        match=r"\(Gamma \+ M\) x num x 6 x A .*Gamma = 1000000 and the content M = 0 is .*not below 2\^63",
    ):
        parse_nature_beam_world(document)
    with pytest.raises(ValueError, match=r"families\[1\]\.pair \[1048576, 1048577\]"):
        parse_nature_beam_world(document)
    for pair in ([800, 809], [3200, 3236]):
        admitted_pair = massive_world([6, 6, 6], PERIODIC, pair)
        admitted_pair["age_bound"] = 100
        parse_nature_beam_world(admitted_pair)
    # the block's own pair under the bound with the world's content (one well of one
    # quantum, M = 1): a well [big, big + 1] refused, [800, 800] admitted
    for pair, admitted in (([big, big + 1], False), ([800, 800], True)):
        world = block_world(
            [24, 24, 24],
            PERIODIC,
            [800, 809],
            [{"position": [10, 10, 10], "side": 3, "pair": pair}],
        )
        world["age_bound"] = 100
        if admitted:
            parse_nature_beam_world(world)
        else:
            with pytest.raises(
                ValueError, match=r"measured\[0\]\.pair .*the content M = 2 is .*not below 2\^63"
            ):
                parse_nature_beam_world(world)
    unbounded = massive_world([6, 6, 6], PERIODIC, [800, 809])
    unbounded["age_bound"] = 100
    del unbounded["amplitude_bound"]
    with pytest.raises(ValueError, match="declares `amplitude_bound`"):
        parse_nature_beam_world(unbounded)
    ceiling = massive_world([6, 6, 6], PERIODIC, [800, 809])
    ceiling["age_bound"] = 100
    ceiling["amplitude_bound"] = 1 << 29
    with pytest.raises(ValueError, match="above the ceiling 2\\^28"):
        parse_nature_beam_world(ceiling)
    huge_seed = block_world(
        [24, 24, 24],
        PERIODIC,
        [800, 809],
        [{"position": [10, 10, 10], "side": 3, "pair": [800, 800], "seed": 1 << 60}],
    )
    huge_seed["age_bound"] = 100
    with pytest.raises(ValueError, match=r"above the world's amplitude bound A = 268435456 on the pair"):
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


def test_the_form_on_a_chain_is_exact_with_the_remainders_term():
    """MUST 1's test: on the chain 6 x 1 x 1 (y and z folded, the Node reading itself twice on
    each) at the pair [2, 3], open on x, the form I of section 3 as the books read it
    (`record_form`, the weights L / num, L the numerators' lcm, here 2) changes by the
    remainders' term exactly on every interval: num x Gamma x (I(t) - I(t - 1)) = L x SUM_i
    (a_next - a_before)_i (r - r')_i (the pace Gamma at every Node of the vacuum, the Node's
    terms weighted by 1 / Gamma, item 36), integers, no tolerance, 60 intervals from random
    rows; the same on a periodic x."""
    for boundary in (CHAIN, PERIODIC_CHAIN):
        document = massive_world([6, 1, 1], boundary, [2, 3])
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
            # the vacuum's pace Gamma at every Node: num Gamma (I(t) - I(t - 1)) = L x the sum
            assert 2 * NODE_CLOCK * (current - previous) == 2 * remainders, boundary
            previous = current


def test_the_margin_rule_on_a_layer_keeps_the_folded_axis_self_reads():
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


def test_the_mode_seeded_layer_blocks_clicks_read_the_bound_mode():
    """The seed as the bound mode's integer profile (MASSIVE_RECORD.md section 11 item 7, the
    reader of record and the seed; EXPLORATORY, the cheap 128^2 rest layer): the block s = 14 at
    g = mu^2 / 4 (the kind [3200, 3236], the well [3200, 3227]) seeded flat reads its clicks at a
    beat (the mean interval 39.3 against the mode's period 42.32), seeded with the module's mode
    as integers at 2^20 over the whole layer (the generator's integers in the world file, the
    same at both levels) it reads the mode: the clicks' mean interval over [200, 1500] within
    0.5 percent of 2 pi / omega_b; the load-time diagnostic of the profile against the
    eigensolver's mode reads the generator's floor on this layer's small gap (3497 units, at
    most 4000; the loader's residual bound is the law's check). The edge cases: a profile without `margin` refused; a profile of the wrong
    length refused; an all-zero profile refused."""
    block = {"position": [57, 57, 0], "side": 14, "pair": [3200, 3227], "margin": "control"}
    document = block_world([128, 128, 1], PERIODIC, [3200, 3236], [block], ticks=1500)
    document["age_bound"] = 100000
    world = parse_nature_beam_world(document)
    reading = block_margin(world, 0)
    period = 2 * np.pi / reading.omega_b
    # the generator as the operator iterated with the stop (the owner's word of
    # 2026-09-25): the profile with its clock beside it (record 1886; ALGEBRA.md 9.22 (7))
    profile, clock, _ = iterated_mode(world, 0, 1 << 20)
    seeded = dict(document)
    seeded["measured"] = [dict(document["measured"][0], seed=profile, clock=list(clock))]
    seeded["input"] = input_stamp(seeded)
    world = parse_nature_beam_world(seeded)
    deviation, amplitude = profile_check(world, 0)
    # the diagnostic against the eigensolver's rounded mode reads the iteration's floor:
    # on this layer the gap is small and the loader's bound admits about 3 / gap units
    # of the neighbouring mode (3497 read, COMPUTATION; the bound is the law's check)
    assert amplitude == 1 << 20 and deviation <= 4000
    lines: list[dict] = []
    simulation = DetectorLawSimulation(world, observer=lines.append)
    assert np.array_equal(simulation.blocks[0].own.now, np.array(profile).reshape(world.shape))
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
    first build at [2, 34) (chain_world's, its family named `source`) beside the massive kind
    `matter`, pair [156, 157], the given clock [512, 1] on N = 1024 declared as its
    `phase_per_link` (the pair form: the matter train at K = pi / 2, cos omega = 0.6624),
    and, when asked, an emitter body of the source kind at [100, 132) whose given family is
    `matter` (`stock` givings, the train along +x); no detector; `clock` None declares no
    clock on the kind (the refusal's edge case); every emitter body seeded on its mode."""
    document = chain_world(on_mode=False)
    document["shape"] = [200, 1, 1]
    document["ticks"] = 160
    document["families"][1]["name"] = "source"
    document["measured"][0]["family"] = "source"
    matter: dict = {"name": "matter", "quantum": 1, "pair": [156, 157], "charge": 0}
    if clock is not None:
        matter["phase_per_link"] = clock  # None: no clock (the refusal's edge case)
    document["families"].append(matter)
    document["measured"] = document["measured"][:1]
    if matter_emitter:
        document["measured"].append(emitter_at(100, stock, family="matter"))
    document["detectors"] = []
    massive_generator().seed_on_the_mode(document)
    return document


def test_a_matter_emitters_record_is_a_massive_record_advanced_by_the_kinds_pair():
    """The emitter of a massive kind (the matter lamp's successor, ALGEBRA.md 9.17; the Boss's
    23:32Z on the lamp verb): an emitter body of the source kind at x = 100 whose given family
    is `matter` (the kind [156, 157] with the declared clock [512, 1] on N = 1024) givings a
    record of the matter kind, written once on its 32 Nodes at both levels as the train
    (ALGEBRA.md 9.17 (6a)) and advanced by the rule with the kind's pair (a massive kind's
    given record is driven by nothing and completes as light's: its `driven` set empty); the
    train TRAVELS +x: a hundred intervals after its giving its levels ahead of the body (x in
    [140, 180)) are large and those behind it (x in [40, 90)) below a tenth of them (the
    tapers' dispersion alone goes back, 3.9 percent in the matter family); the books balance
    at every interval; light's rows are identical with and without the matter emitter beside
    it UNTIL the matter body's content field, the family of clicks (BUILD.md section 26 item
    32), reaches a light record's support: the field spreads from the body at [100, 132)
    within the plain step's cone and bends every record it reaches (ALGEBRA.md 9.46 (6)
    (b)), so the rows are compared bit for bit while the field is the same on the record's
    Nodes, on more than one interval, and not after (the first build's chain digests stand,
    test (p)). The edge cases: an emitter whose given family is a massive kind WITHOUT the
    clock is refused at load naming the pair form."""
    world = parse_nature_beam_world(matter_emitter_world(True, [512, 1]))
    beside = parse_nature_beam_world(matter_emitter_world(False, [512, 1]))
    matter = [family.name for family in world.families].index("matter")
    assert world.families[matter].massive_kind
    assert world.families[matter].phase_per_age == (512, 1)
    simulation = DetectorLawSimulation(world)
    other = DetectorLawSimulation(beside)
    identity = 1 * (1 << 32) + 1
    given: int | None = None
    field_reached: int | None = None
    compared = 0
    for tick in range(1, 301):
        simulation.step()
        other.step()
        assert simulation.books()["balanced"], tick
        live = simulation.records.get(identity)
        if live is not None:
            given = given if given is not None else tick
            assert live.family == matter and live.emitter == 1
        # light's rows unchanged beside the matter emitter while the family of clicks'
        # field is the same on their Nodes (the source body's own standing record is of
        # the source kind, its tail reached by the field too: not light's row)
        for light_identity, light in other.records.items():
            if other.families[light.family].massive_kind:
                continue
            differs = simulation.clock_record.now != other.clock_record.now
            if field_reached is None and np.any(differs & (light.now != 0)):
                field_reached = tick
            if field_reached is None:
                assert np.array_equal(simulation.records[light_identity].now, light.now), tick
                compared += 1
        if given is not None and tick == given + 100:
            break
    assert compared > 1 and (field_reached is None or field_reached > 1)
    # the first giving within the well's period (the residue's wait, 9.17 (7) (f))
    assert given is not None and given < 120
    live = simulation.records[identity]
    ahead = int(np.max(np.abs(live.now[140:180, 0, 0])))
    behind = int(np.max(np.abs(live.now[40:90, 0, 0])))
    # the matter train's tapers disperse more than light's: 3.9 percent behind (COMPUTATION)
    assert ahead > 1000 and behind * 10 < ahead, (ahead, behind)
    with pytest.raises(ValueError, match="pair form of its clock"):
        parse_nature_beam_world(matter_emitter_world(True))


def test_a_matter_emitters_record_clicks_once_at_the_rung():
    """Reviewer 3's line on the matter lamp (the Boss's 01:10Z), on the matter emitter under
    the flux reading (ALGEBRA.md 9.19 (3)): an emitter's record of a massive kind goes
    through the same pointer path as light's (the click is the law's one action on any
    record, POSTULATES 10). The chain world of test (z) without light's emitter (the matter
    kind's faces periodic), the matter emitter's stock 2 (the residues from the law on
    W = 700), the cube of matter bodies at [184, 186] read as the set `screen`
    named by the emitter: each record clicks ONCE at the screen, at the first interval at
    which 2 W C >= (2 u + 1) T on its pointer there (read through the engine's
    `_ladder_click`; the interval before it below the rung), after the train's flight (53
    Links from the head at 131 at v_g = 0.442, 120 intervals, and as much of the passage of
    72 as the residue asks: between 100 and 400 intervals after the giving), the line's
    `tick` its `click`, the record deleted whole at it; two gather lines in all, the books
    balanced at every interval."""
    document = matter_emitter_world(True, [512, 1], stock=2)
    document["ticks"] = 3000
    # the cube of matter bodies at [184, 186] read as `screen` (record 1899), the
    # emitter kept at measured[1] (its records' identities carry its number)
    positions = cube_positions(document["shape"], [184, 0, 0])
    document["measured"] = [
        receiver_body(positions[0], "matter"),
        dict(document["measured"][1], receiver="screen"),
        *(receiver_body(position, "matter") for position in positions[1:]),
    ]
    document["detectors"] = [{"name": "screen", "positions": positions, "threshold": 1}]
    document["input"] = input_stamp(document)  # the stamp of the rebuilt list (record 1886)
    world = parse_nature_beam_world(document)
    lines: list[dict] = []
    simulation = DetectorLawSimulation(world, observer=lines.append)
    identities = [1 * (1 << 32) + 1, 1 * (1 << 32) + 2]
    screen = simulation.detector_names.index("screen")
    at_click: dict[int, tuple[int, int, int, int]] = {}
    original = simulation._ladder_click

    def spy(live, increments):
        pointer = live.pointers[screen]
        original(live, increments)
        if live.clicked and live.identity not in at_click:
            at_click[live.identity] = (pointer, live.u, live.norm, live.wheel, live.pace)

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
    # both records click, each once, in either order (under the click rule of
    # 9.17 (7) (f) the second is given (2 u + 1) P / (2 W) after the first's
    # click and may reach its rung at the screen first when its residue is
    # the smaller)
    assert sorted(gather["record"] for gather in gathers) == identities
    for gather in gathers:
        identity = gather["record"]
        assert gather["chosen"][0][0] == "screen" and gather["click"] == gather["tick"]
        pointer, u, norm, wheel, pace = at_click[identity]
        givings = {line["record"]: line for line in lines if line["event"] == "giving"}
        assert wheel == givings[identity]["W"] and lawful_wheel(world, givings[identity])
        assert 0 <= u < wheel and u == gather["u"] and pace == givings[identity]["pace"]
        # the plain flux against the norm's rational norm / pace (item 36)
        assert 2 * wheel * pace * pointer >= (2 * u + 1) * norm
        assert below[identity] == gather["click"] - 1
        # the flight: the train's head over 53 Links at v_g = 0.442, then as
        # much of the passage as the residue asks (the residues spread from
        # the kept remainder, record 1962 (1))
        assert 100 < gather["click"] - gather["giving"] < 400
        assert identity not in simulation.records


def test_every_declared_wheel_is_refused_by_name():
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
        document["input"] = input_stamp(document)  # the stamp over the whole file (item 28)
        with pytest.raises(ValueError, match=message):
            parse_nature_beam_world(document)


def light_clock_world(faces: str, far_body: bool) -> dict:
    """DECLARATIONS.md section 10 with section 15's lines (M1-1, M1-3, M1-4, M1-10) and item 9,
    SINCE BUILD.md section 26 and THE GIVEN TRAIN (item 27): a chain of 173 (x `closed` for
    light, the zero face at 172 the mirror B forty Links from A's head at 131; or x open,
    the sponges), the matter kind [800, 809], the emitter A of the extents [32, 1, 1] at
    [100, 132) with the seed 50 x 2^20 on its bound mode, its `emitter` of light on the given
    clock [512, 1] of N = 1024 with its train along +x and the stock 1 (one giving); the
    receiving set `A_face` bound to A at the cube of three free Nodes adjacent to A's head
    (x in [132, 134]; item 9, record 1899), A's `receiver` by name; with `far_body`, the cube
    of light bodies at [160, 162] read as the set `far`; the amplitude bound 2^32; no wheel
    (the record's own, 9.22 (4))."""
    document = massive_world([173, 1, 1], {"x": faces, "y": "periodic", "z": "periodic"}, [800, 809])
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
            "extents": [32, 1, 1],
            "pair": [800, 801],
            "seed": 50 << 20,
            "emitter": {"family": "light", "train": {"direction": [1, 0, 0], "periods": 8}},
            "margin": "control",
            # the receiver by name (section 13 item 7): A's own bound set
            "receiver": "A_face",
        }
    ]
    document["detectors"] = [
        {"name": "A_face", "block": 0, "positions": [[132, 0, 0], [133, 0, 0], [134, 0, 0]]}
    ]
    if far_body:
        receiver_cube(document, "far", [160, 0, 0])
    seed_source(document, 0)
    return document


def test_the_receiving_set_beside_the_emitter_books_the_flux_and_clicks_at_its_rung():
    """A set bound to a block is a receiver (the receiving set at ONE free Node) on the light clock's chain of 173 (W = 64;
    the world's `wheel` 64) SINCE THE FLUX READING (ALGEBRA.md 9.19 (3); BUILD.md section 26
    item 14): A's one given record is written once on A's 32 Nodes as the train and leaves toward +x;
    the set's cube at [132, 134] books the one-way flux into it from the first interval (its
    pointer above 0 and its rung at the record's own residue from the law, the click line written
    at that rung and stamped with A's count as the interval begins, named by
    `clock_source`), and the record is deleted whole at its click, with the faces closed
    and open alike (no `face` detector on the closed chain; `face` on the open one, last on the
    ladder and never reached first); nothing absorbs (the take retired). A receiver body at
    x = 160 read as `far` is a declared set off A's ladder (A names A_face): never chosen.
    The loader: `block` with a position on a measured Node refused, with two positions
    refused as a box of sides [2, 1, 1] (the cube of record 1899), `block` naming a body
    refused naming the positions form, `closed` without
    `detector_law` refused, `own_grace` on the emitter refused, a stock below 1 refused."""
    first = 1  # A's given record: block 0, giving 1
    for faces in ("closed", "open"):
        world = parse_nature_beam_world(light_clock_world(faces, faces == "open"))
        if faces == "closed":
            assert world.closed == (True, False, False) and world.boundary_per_axis["x"] == "closed"
        lines: list[dict] = []
        simulation = DetectorLawSimulation(world, observer=lines.append)
        assert ("face" in simulation.detector_names) == (faces == "open")
        a_face = simulation.detector_names.index("A_face")
        assert int(simulation.detector_at_node[132, 0, 0]) == a_face
        block = simulation.blocks[0]
        pointer_at_click: int | None = None
        original = simulation._ladder_click

        def spy(live, increments, original=original, a_face=a_face):
            nonlocal pointer_at_click
            pointer = live.pointers[a_face]
            original(live, increments)
            if live.clicked and live.identity == first and pointer_at_click is None:
                pointer_at_click = pointer

        simulation._ladder_click = spy  # type: ignore[method-assign]
        giving: int | None = None
        count_then: int | None = None
        for _ in range(600):
            count_before = block.count
            simulation.step()
            books = simulation.books()
            assert books["balanced"], simulation.tick
            live = simulation.records.get(first)
            if live is not None:
                giving = live.giving_tick
            if pointer_at_click is not None and count_then is None:
                count_then = count_before
        assert giving is not None and pointer_at_click is not None and pointer_at_click > 0
        gathers = [g for g in lines if g["event"] == "gather" and g["record"] == first]
        assert len(gathers) == 1 and gathers[0]["chosen"][0][0] == "A_face"
        line = gathers[0]
        # the rung (2 u + 1) T / (2 W) on the record's own residue from the law
        # decides how much of the record must pass the set before its click
        assert 0 <= line["click"] - giving <= 600 and line["tick"] == line["click"]
        given = next(b for b in lines if b["event"] == "giving" and b["record"] == first)
        assert 0 <= line["u"] < given["W"] and lawful_wheel(world, given)
        assert line["clock_source"] == "measured:0" and line["clock"] == count_then
        assert first not in simulation.records
        assert all(g["chosen"][0][0] != "far" for g in lines if g["event"] == "gather")
    # the loader's refusals
    bad = light_clock_world("closed", False)
    bad["detector_law"] = False
    bad["massive_record"] = False
    del bad["amplitude_bound"]
    del bad["face_depth"]  # the face slab is the detector law's (refused without it)
    with pytest.raises(ValueError, match="closed"):
        parse_nature_beam_world(bad)
    on_body = light_clock_world("open", False)
    on_body["detectors"] = [{"name": "A_face", "block": 0, "positions": [[100, 0, 0]]}]
    on_body["input"] = input_stamp(on_body)  # the stamp over the whole file (item 28)
    with pytest.raises(ValueError, match="names a Node of a measured event"):
        parse_nature_beam_world(on_body)
    two = light_clock_world("open", False)
    two["detectors"] = [{"name": "A_face", "block": 0, "positions": [[132, 0, 0], [133, 0, 0]]}]
    two["input"] = input_stamp(two)
    with pytest.raises(ValueError, match=r"is a box of sides \[2, 1, 1\]"):
        parse_nature_beam_world(two)
    no_block = light_clock_world("open", True)
    no_block["detectors"] = [{"name": "B", "block": 1}]
    no_block["input"] = input_stamp(no_block)
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


def test_a_set_at_a_blocks_cells_books_the_flux_into_them_and_steps_with_the_block():
    """A set bound to a block WITHOUT positions is a receiver (Sagnac's form, DECLARATIONS.md section 13
    item 1) under the flux reading (ALGEBRA.md 9.19 (3)): the block's twelve Nodes are the
    set's Nodes (the detector index at them the set's); an emitter's record (the emitter
    body of the source kind at [100, 132) on a chain of 300, its train along +x toward the
    block 68 Links ahead, two givings, the emitter naming the set) books its one-way flux into the
    block's Nodes to the set and clicks once there, the click stamped with the block's own
    count as the interval began and named by `clock_source`, the record deleted whole at
    it, the books balanced; nothing absorbs. Pushed toward the emitter at k = 3 (the block
    stepping, its Nodes and the set's Nodes following it): the record still clicks once at
    the set, the books balanced. The loader: a set's `wheel` refused by name."""
    for momentum in ([0, 0, 0], [-64, 0, 0]):
        document = massive_world([300, 1, 1], CHAIN, [800, 809])
        document["ticks"] = 1200
        document["age_bound"] = 1 << 20
        document["clock_stamp"] = True
        document["families"].append(source_family())
        document["measured"] = [
            dict(emitter_at(100, 2), receiver="B_nodes"),
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
        document["detectors"] = [{"name": "B_nodes", "block": 1}]
        seed_source(document, 0)
        world = parse_nature_beam_world(document)
        lines: list[dict] = []
        simulation = DetectorLawSimulation(world, observer=lines.append)
        block = simulation.blocks[1]
        detector = simulation.detector_names.index("B_nodes")
        assert int(simulation.detector_at_node[205, 0, 0]) == detector
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
        assert len(gathers) == 1 and gathers[0]["chosen"][0][0] == "B_nodes", gathers
        assert gathers[0]["clock_source"] == "measured:1" and gathers[0]["clock"] == count_at_rung
        assert gathers[0]["tick"] == gathers[0]["click"] and identity not in simulation.records
        assert block.stepped > 0 if momentum[0] else block.stepped == 0
        assert np.array_equal(simulation.detector_at_node == detector, block.mask)
    bad = document
    bad["detectors"] = [{"name": "B_nodes", "block": 1, "wheel": 64}]
    bad["input"] = input_stamp(bad)  # the stamp over the whole file (item 28)
    with pytest.raises(ValueError, match="wheel is refused"):
        parse_nature_beam_world(bad)


def test_a_block_that_steps_off_the_board_refuses_the_interval():
    """Reviewer 3's line from the redshift dry run (BUILD.md section 18): a block pushed toward
    a zero face (momentum [-64, 0, 0] from x = 30 on the open chain of 300, one hop per three
    intervals) refuses the run at the interval its Nodes would leave the board, naming the block
    and the interval, instead of running on with the block gone; before that interval it steps
    and the books balance. The edge case: on a periodic chain the same block wraps and steps on
    through 400 intervals with no refusal."""
    for boundary, refused in ((CHAIN, True), (PERIODIC_CHAIN, False)):
        document = massive_world([300, 1, 1], boundary, [800, 809])
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


def test_a_wall_of_lights_kind_is_a_mirror_line():
    """DECLARATIONS.md section 15 L-1 (the (M) wall's path): a mirror line of blocks of light's
    kind with the pair [1, 2], FOUR Nodes deep (the mirror's depth of ALGEBRA.md A.3 at the
    train's wavelength 4), on the first build's chain (x = 40 to 43; the emitter body at
    [2, 34), the screen cube at [70, 72]): the blocks have no own record, no clock and no
    coupling (the loader sets their seed 0; the engine's blocks' loop skips them; the margin
    rule skips light's kind), light's pair arrays carry [1, 2] at the four Nodes and [1, 1]
    elsewhere; over 200 intervals the largest level beyond the wall (x in [48, 69]) stays below
    four percent of the largest level before it (x in [10, 38], the train's own Nodes; the
    reading on this head in the test's assertion, COMPUTATION), the books balanced at every
    interval; a light-kind block with
    `seed` or `margin` refused, and `coupling` refused by name on any block. The chain's source is the emitter body of
    section 26 (a block itself, of the matter kind, with its own record)."""
    document = chain_world()  # the closed chain (BUILD.md section 26 item 14)
    document["massive_record"] = True
    document["amplitude_bound"] = 1 << 28
    document["ticks"] = 200
    for x in (40, 41, 42, 43):
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
    document["input"] = input_stamp(document)  # the stamp over the whole file (item 28)
    world = parse_nature_beam_world(document)
    assert [entry.block is not None for entry in world.measured] == [
        True,
        False,
        False,
        False,
        True,
        True,
        True,
        True,
    ]
    assert world.measured[4].block is not None and world.measured[4].block.seed == 0
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
            beyond = max(beyond, int(np.max(np.abs(live.now[48:70, 0, 0]))))
    assert before > 0 and beyond * 100 < 4 * before, (before, beyond)
    for key, value in (("seed", 5), ("margin", "control")):
        bad = json.loads(json.dumps(document))
        bad["measured"][4][key] = value
        with pytest.raises(ValueError, match="refused on a block of light's kind"):
            parse_nature_beam_world(bad)
    coupled = json.loads(json.dumps(document))
    coupled["measured"][4]["coupling"] = {"G": [1, 1], "g": [1, 2]}
    with pytest.raises(ValueError, match="coupling is refused"):
        parse_nature_beam_world(coupled)


def test_the_momentum_books_carry_the_blocks_held_momentum_and_nothing_else():
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
