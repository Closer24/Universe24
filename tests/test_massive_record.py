"""The massive record kind: the rule with a pair per record kind on the six-neighbour term, on a chain and at a corner, light's pair [1, 1] bit for bit, the conserved form to the remainders' jitter, the byte identity of the light record without the key, and the loader's refusals; every source is an emitter body seeded on its bound mode."""

from __future__ import annotations

import hashlib
import json
from fractions import Fraction

import numpy as np
import pytest

from event_universe.core.rule3 import coefficients
from event_universe.diagnostics.massive_record_margin import (
    block_margin,
    check_margins,
    iterated_mode,
)
from event_universe.events.detector_law import DetectorLawSimulation, LiveRecord, form_json
from event_universe.loader.world import (
    MASSLESS_PAIR,
)
from event_universe.world_files import input_stamp, parse_nature_beam_world
from tests.bodies import (
    block_world,
    emitter_at,
    light_clock_world,
    massive_world,
    matter_emitter_world,
    seed_source,
    source_family,
)
from tests.running import planted
from tests.worlds import (
    NODE_CLOCK,
    chain_world,
    cube_positions,
    lawful_wheel,
    receiver_body,
    receiver_cube,
)

# A, the amplitude unit of the planted rows: the worlds' amplitude_bound (ALGEBRA.md #the-line;
# the engine's constant UNIT retired by the model owner's record 2089, BUILD.md section 26 item 57)
UNIT = 1 << 20


def step_once(simulation: DetectorLawSimulation, live: LiveRecord) -> tuple[np.ndarray, np.ndarray]:
    """One step of the rule; returns (a_next, r') from the record's rows after the step."""
    simulation._advance(live)
    return live.now.copy(), live.remainder.copy()


def test_the_rule_on_a_chain_against_section_ones_integers():
    """BUILD.md (a): the kind [2, 3] on a 5-Node open chain (y, z one layer periodic, so
    S_6 = a_W + a_E + 4 a_now with 0 beyond the ends); the totals num S_6 - 9 a_before + r
    are [1, 27, -56, 19, 7], a_next = [0, 3, -7, 2, 0], r' = [1, 0, 7, 1, 7]. UNDER THE
    WEAK-FIELD RULE (ALGEBRA.md #the-line; BUILD.md section 26 item 44) the vacuum's wall is 9
    times 2 Gamma^2 and the remainder 2 Gamma^2 times the line's, the levels bit for bit: r
    and r' here are the line's times 2 Gamma^2."""
    world = parse_nature_beam_world(
        massive_world([5, 1, 1], {"x": "open", "y": "periodic", "z": "periodic"}, [2, 3])
    )
    simulation = DetectorLawSimulation(world)
    now = np.array([0, 5, -7, 3, 0]).reshape(5, 1, 1)
    before = np.array([1, 0, 2, -1, 0]).reshape(5, 1, 1)
    vacuum_scale = 2 * NODE_CLOCK**2
    r = np.array([0, 1, 2, 0, 1]).reshape(5, 1, 1) * vacuum_scale
    live = planted(simulation, 1, now, before, r)
    a_next, r_next = step_once(simulation, live)
    assert a_next.ravel().tolist() == [0, 3, -7, 2, 0]
    assert r_next.ravel().tolist() == [value * vacuum_scale for value in (1, 0, 7, 1, 7)]
    assert all(0 <= value < 9 * vacuum_scale for value in r_next.ravel().tolist())
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
    assert world.families[0].pair == MASSLESS_PAIR
    assert np.all(simulation.kind_num[0] == 1) and np.all(simulation.kind_den[0] == 1)
    rng = np.random.default_rng(7)
    now = rng.integers(-UNIT, UNIT, size=(80, 1, 1), dtype=np.int64)
    before = rng.integers(-UNIT, UNIT, size=(80, 1, 1), dtype=np.int64)
    vacuum_scale = 2 * NODE_CLOCK**2  # the weak-field rule at c = 0: the plain rule times 2 Gamma^2
    remainder = rng.integers(0, 3, size=(80, 1, 1), dtype=np.int64) * vacuum_scale
    live = planted(simulation, 0, now, before, remainder)
    live.age = 1000
    total = vacuum_scale * (simulation._neighbours(now) - 3 * before) + remainder
    expected_next = np.floor_divide(total, 3 * vacuum_scale)
    expected_remainder = total - 3 * vacuum_scale * expected_next
    a_next, r_next = step_once(simulation, live)
    content = simulation.level_of("content")
    free = (content == 0) & (simulation._neighbours(content, simulation.kind_wrap[0]) == 0)
    assert 30 <= int(np.sum(free)) <= 45
    assert np.array_equal(a_next[free], expected_next[free])
    assert np.array_equal(r_next[free], expected_remainder[free])
    # the weak-field rule at every Node from its three integers (ALGEBRA.md #the-line; item 44)
    (read, _, _), self_coefficient, wall = coefficients(
        simulation.kind_num[0], simulation.kind_den[0], NODE_CLOCK, content
    )
    clocked = read * simulation._neighbours(now, simulation.kind_wrap[0])
    clocked += self_coefficient * now - wall * before + remainder
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


@pytest.mark.diagnostic
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
        document["amplitude_bound"] = (
            1 << 21
        )  # the pair's room under the weak field (ALGEBRA.md #the-rows-against-nature)
        world = parse_nature_beam_world(document)
        simulation = DetectorLawSimulation(world)
        live = planted(simulation, 1, now, before, np.zeros((6, 6, 6), dtype=np.int64))
        start = Fraction(*simulation.record_form(live))
        assert start > 0
        peak = 0
        projection = 0
        for _ in range(200):
            step_once(simulation, live)
            peak = max(peak, int(np.abs(live.now).max()))
            projection = max(projection, abs(int(np.sum(live.now * checker)) // 216))
            # GAMEBOARD: the books' form, a diagnostic bound on the remainders' jitter, not a measurement
            assert abs(Fraction(*simulation.record_form(live)) - start) < start // 1000
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
        # at Node 0: the total R S_6 = R (a_W + a_E + 4 x 0) = R a_W over the vacuum's wall w
        # (the weak-field rule's integers at c = 0, item 44)
        (read, _, _), _self, wall = coefficients(1, 2, NODE_CLOCK, 0)
        total = wall * int(a_next[0, 0, 0]) + int(r_next[0, 0, 0])
        assert total == read * expected
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


def test_the_loaders_refusals_name_the_key():
    """BUILD.md (q): the step's keys refused one by one, each naming the key."""
    base = massive_world([4, 4, 4], "open", [2, 3])
    without_key = json.loads(json.dumps(base))
    without_key["massive_record"] = False
    del without_key["amplitude_bound"]
    with pytest.raises(ValueError, match="is refused without the world key `massive_record`"):
        parse_nature_beam_world(without_key)
    reversed_pair = json.loads(json.dumps(base))
    reversed_pair["universe"][1]["pair"] = [3, 2]
    with pytest.raises(ValueError, match="den >= num"):
        parse_nature_beam_world(reversed_pair)
    # one border for every family (BUILD.md section 26 item 28): the family key `faces`
    # refused by name on the massive kind and on light's alike
    for family in (0, 1):
        faced = json.loads(json.dumps(base))
        faced["universe"][family]["faces"] = {"x": "open"}
        with pytest.raises(ValueError, match=rf"universe\[{family}\] has unknown keys: faces"):
            parse_nature_beam_world(faced)
    turned = json.loads(json.dumps(base))
    turned["universe"][1]["clock"] = 5
    with pytest.raises(ValueError, match="clock must be a list, not 5"):
        parse_nature_beam_world(turned)
    # the pair form is the family's clock, admitted (test (z): a matter lamp)
    clocked = json.loads(json.dumps(base))
    clocked["universe"][1]["clock"] = [1, 2]
    assert parse_nature_beam_world(clocked).families[1].phase_per_age == (1, 2)
    no_law = json.loads(json.dumps(base))
    no_law["detector_law"] = (
        False  # the flag was the law's name: refused by name (ALGEBRA.md #the-primitives)
    )
    with pytest.raises(ValueError, match="the world has unknown keys: detector_law"):
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
            "stocks": {},
            "momentum": [0, 0, 0],
            "fixed": False,
            "lamp": {"rate": [1, 40], "wheel": [1, 64], "train": 2},
        }
    ]
    with pytest.raises(ValueError, match="has unknown keys: lamp"):
        parse_nature_beam_world(lamp_on_kind)
    # light's kind written out, [1, 1], is a value and not a massive kind
    written = json.loads(json.dumps(base))
    written["universe"][1]["pair"] = [1, 1]
    written["universe"][1]["clock"] = [77, 25]
    world = parse_nature_beam_world(written)
    assert not world.families[1].massive_kind


def test_the_records_keys_under_the_key_and_none_without_it():
    """BUILD.md (r): the identity under `hypotheses`, the families' pair and the books'
    form under the key; nothing of them without it (the first build's world); every
    family's faces the world's (one border, BUILD.md section 26 item 28)."""
    world = parse_nature_beam_world(
        massive_world([4, 4, 4], {"x": "open", "y": "periodic", "z": "open"}, [2, 3])
    )
    assert world.hypotheses == []  # no identity beside the engine (ALGEBRA.md #the-primitives)
    assert world.families[1].pair == (2, 3) and world.families[1].massive_kind
    assert world.kind_periodic(1) == (False, True, False) == world.kind_periodic(0)
    simulation = DetectorLawSimulation(world)
    assert "form" in simulation.books()["families"]["matter"]
    # without the key there is no block, so no emitter body (the lamp refused under the
    # detector law): the rule's world with the key withdrawn and light alone
    without = massive_world([4, 4, 4], "open", [2, 3])
    without["massive_record"] = False
    # every family declares its pair (the pair's card), admitted under massive_record alone
    with pytest.raises(ValueError, match="is refused without the world key `massive_record`"):
        parse_nature_beam_world(without)


# The block (STEP 3 of the build: BUILD.md section 6, (e) to (l))


def with_screen(document: dict, x: int) -> dict:
    """The receiver by name for a test world's emitter body (DECLARATIONS.md section 13
    item 7): the cube of side 3 of light bodies at [x, x + 2] read as the set `screen`
    (record 1899; no wheel: the rung's wheel is the record's own, ALGEBRA.md #a-familys-declaration)."""
    receiver_cube(document, "screen", [x, 0, 0])
    document["stamp"] = input_stamp(document)  # the stamp over the whole file (item 28)
    return document


CHAIN = {"x": "open", "y": "periodic", "z": "periodic"}
PERIODIC_CHAIN = {"x": "periodic", "y": "periodic", "z": "periodic"}


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
    the lamp; an emitter is a clicking body, ALGEBRA.md #the-click): an emitter body of the
    source kind (the one-Node well SOURCE_WELL at x = 100 seeded on its mode, the stock 3)
    on the chain of 240 with the screen at 230: three givings in turn, the residues the
    law's, each given record of content 1 moved from the stock (`held_spent` 3 of the
    source family, `transit_released` 3 of light), the body's own record continuing under its
    one identity after every giving and after the stock is spent, never rewritten (ALGEBRA.md #the-ladder; item 33), the books balanced at every tick. The
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
    # the residues from the law (ALGEBRA.md #a-familys-declaration) on the body's own wheel (700
    # on the source well in the vacuum; at its Node the wheel of its content under
    # the Node clock, ALGEBRA.md #the-paces, read from the rule), spread from the remainder
    # kept at the Nodes (the model owner's decisions (1) and (2) of record 1962;
    # the coupling's back-action HISTORY)
    assert all(lawful_wheel(world, line) for line in givings)
    assert [line["content"] for line in givings] == [4, 3, 2]  # one own quantum beside the stock
    assert len({line["u"] for line in givings}) > 1
    # the spent quanta on the given family's row, light (item 47; the own family's HISTORY)
    assert simulation.ledger.held_spent[0] == 3 and simulation.ledger.transit_released[0] == 3
    own = simulation.blocks[0].own
    assert (
        own is not None and own.identity == 0
    )  # the standing record continues (ALGEBRA.md #the-ladder)
    assert all(
        live.family == 0 and live.content == 1 for live in simulation.records.values() if live is not own
    )
    base = with_screen(block_world([240, 1, 1], CHAIN, [156, 157], [], emitter_at(100, 3)), 230)
    for key in ("emits", "own_grace"):
        bad = json.loads(json.dumps(base))
        bad["measured"][0].update({"emits": "light", "own_grace": 70, "receiver": "screen"})
        if key == "own_grace":
            del bad["measured"][0]["emits"]
        with pytest.raises(ValueError, match=f"has unknown keys: {key}"):
            parse_nature_beam_world(bad)
    on_light = json.loads(json.dumps(base))
    on_light["measured"][0]["family"] = "light"
    on_light["measured"][0]["seed"] = 100
    on_light["measured"][0]["pair"] = [1, 2]
    on_light["measured"][0]["stocks"] = {"matter": 1}  # the stock, not the own family (item 47)
    with pytest.raises(ValueError, match="of light's kind"):
        parse_nature_beam_world(on_light)
    empty = json.loads(json.dumps(base))
    empty["measured"][0]["amount"] = 0
    with pytest.raises(ValueError, match="amount"):
        parse_nature_beam_world(empty)


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


@pytest.mark.diagnostic
def test_the_margin_rule_refuses_below_the_margin_and_prints_the_extent():
    """The margin rule (its extent and mode a GameBoard reading, a diagnostic) refuses a block
    whose extent passes its board or a face (naming the axis, the extent and the side needed),
    an unbound well, and a runaway well on a chain, and admits a control."""
    for margin, admitted in (("pin", False), ("control", True)):
        document = block_world(
            [48, 48, 48],
            PERIODIC,
            [1600, 1618],
            [
                {
                    "position": [10, 10, 10],
                    "side": 28,
                    "q": 0,
                    "spin": [0, 0, 0],
                    "twist": 0,
                    "moment": [0, 0, 0],
                    "pair": [1600, 1609],
                    "margin": margin,
                    "seed": 1
                    << 18,  # below the pair's amplitude bound (ALGEBRA.md #the-rows-against-nature)
                }
            ],
        )
        document["age_bound"] = 100000
        document["amplitude_bound"] = (
            1 << 19
        )  # the pair's room under the weak field (ALGEBRA.md #the-rows-against-nature)
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
        with pytest.raises(ValueError, match=r"measured\[0\] has unknown keys: cavity"):
            parse_nature_beam_world(document)


# The series' two keys of step 5 (BUILD.md section 4 step 7 and section 5 (v-m))


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
    unkeyed = json.loads(json.dumps(document))
    unkeyed["massive_record"] = False  # declared false, never absent (item 57)
    with pytest.raises(ValueError, match="is refused without the world key `massive_record`"):
        parse_nature_beam_world(unkeyed)


# Reviewer 3's three MUSTs on step 2 (the Boss's 16:42Z) and his layer line (18:12Z)


def test_the_load_bound_of_a_pair_names_the_bound_and_the_pair():
    """A pair whose rule total at the declared amplitude bound, the clock and the content reaches 2^63 is refused at load naming them ([800, 809] and [3200, 3236] admitted); the amplitude bound is required, capped at 2^28, and a seed or a row above it is refused naming it."""
    big = 1 << 20
    document = massive_world([6, 6, 6], PERIODIC, [big, big + 1])
    document["age_bound"] = 100
    with pytest.raises(
        ValueError,
        match=r"6 A R \+ A \|S\| \+ w \(A \+ 1\).*Gamma = 10000 and the content M = 0 .*not below 2\^63",
    ):
        parse_nature_beam_world(document)
    with pytest.raises(ValueError, match=r"families\[1\]\.pair \[1048576, 1048577\]"):
        parse_nature_beam_world(document)
    for pair, amplitude in (([800, 809], 1 << 22), ([3200, 3236], 1 << 19)):
        admitted_pair = massive_world([6, 6, 6], PERIODIC, pair)
        admitted_pair["age_bound"] = 100
        admitted_pair["amplitude_bound"] = (
            amplitude  # the integers of ALGEBRA.md #the-rows-against-nature per pair
        )
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
                ValueError, match=r"measured\[0\]\.pair .*the content M = 2 .*not below 2\^63"
            ):
                parse_nature_beam_world(world)
    unbounded = massive_world([6, 6, 6], PERIODIC, [800, 809])
    unbounded["age_bound"] = 100
    del unbounded["amplitude_bound"]
    with pytest.raises(ValueError, match="amplitude_bound is required with `massive_record`"):
        parse_nature_beam_world(unbounded)
    ceiling = massive_world([6, 6, 6], PERIODIC, [800, 809])
    ceiling["age_bound"] = 100
    ceiling["amplitude_bound"] = 1 << 29
    with pytest.raises(ValueError, match="A = 536870912.*not below 2\\^63"):
        parse_nature_beam_world(ceiling)
    huge_seed = block_world(
        [24, 24, 24],
        PERIODIC,
        [800, 809],
        [{"position": [10, 10, 10], "side": 3, "pair": [800, 800], "seed": 1 << 60}],
    )
    huge_seed["age_bound"] = 100
    with pytest.raises(ValueError, match=r"above the world's amplitude bound A = 4194304 on the pair"):
        parse_nature_beam_world(huge_seed)
    bounded = massive_world([6, 6, 6], PERIODIC, [800, 809])
    bounded["age_bound"] = 100
    world = parse_nature_beam_world(bounded)
    simulation = DetectorLawSimulation(world)
    planted_row = planted(
        simulation,
        1,
        np.full((6, 6, 6), (1 << 22) + 1),  # just above A: the next level about twice it, inside int64
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
        previous = Fraction(*simulation.record_form(live))
        for _ in range(60):
            a_before = live.before.astype(object)
            r = live.remainder.astype(object)
            simulation._advance(live)
            current = Fraction(*simulation.record_form(live))
            remainders = int(
                np.sum((live.now.astype(object) - a_before) * (r - live.remainder.astype(object)))
            )
            # the vacuum's R = 2 Gamma^2 num at every Node: R (I(t) - I(t - 1)) = L x the sum
            read = coefficients(2, 3, NODE_CLOCK, 0)[0][0]
            assert read * (current - previous) == simulation.kind_wall(1) * remainders, boundary
            previous = current


def test_the_mode_seeded_layer_blocks_clicks_read_the_bound_mode():
    """The seed as the bound mode's integer profile (MASSIVE_RECORD.md section 11 item 7, the
    reader of record and the seed; EXPLORATORY, the cheap 128^2 rest layer): the block s = 14 at
    g = mu^2 / 4 (the kind [3200, 3236], the well [3200, 3227]) seeded flat reads its clicks at a
    beat (the mean interval 39.3 against the mode's period 42.36), seeded with the module's mode
    as integers at 2^18 over the whole layer (the generator's integers in the world file, the
    same at both levels) it reads the mode: the clicks' mean interval over [200, 1500] within
    0.5 percent of the mode's period 2 pi / omega_b, 42.36 intervals on this layer (the
    detector's clicks; the loader's residual bound is the law's check of the profile). The edge
    cases: a profile without `margin` refused; a profile of the wrong length refused; an
    all-zero profile refused."""
    block = {
        "position": [57, 57, 0],
        "side": 14,
        "q": 0,
        "spin": [0, 0, 0],
        "twist": 0,
        "moment": [0, 0, 0],
        "pair": [3200, 3227],
        "margin": "control",
        "seed": 1 << 18,  # below the pair's amplitude bound (ALGEBRA.md #the-rows-against-nature)
    }
    document = block_world([128, 128, 1], PERIODIC, [3200, 3236], [block], ticks=1500)
    document["age_bound"] = 100000
    document["amplitude_bound"] = (
        1 << 19
    )  # the pair's room under the weak field (ALGEBRA.md #the-rows-against-nature)
    world = parse_nature_beam_world(document)
    # the mode's period 2 pi / omega_b on this 128^2 layer (omega_b 0.14833, a COMPUTATION)
    period = 42.36
    # the generator as the operator iterated with the stop (the owner's word of
    # 2026-09-25): the profile with its clock beside it (record 1886; ALGEBRA.md #a-familys-declaration)
    profile, clock, _ = iterated_mode(
        world, 0, 1 << 18
    )  # below the pair's amplitude bound 2^19 (ALGEBRA.md #the-rows-against-nature)
    seeded = dict(document)
    seeded["measured"] = [dict(document["measured"][0], seed=profile, clock=list(clock))]
    seeded["stamp"] = input_stamp(seeded)
    world = parse_nature_beam_world(seeded)
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


def test_a_matter_emitters_record_is_a_massive_record_advanced_by_the_kinds_pair():
    """An emitter giving the massive kind: its record is advanced by the kind's pair, leaves both ways
    with the books balanced, and light's rows match until the body's field reaches them; no clock is refused."""
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
            differs = simulation.held_record("content").now != other.held_record("content").now
            if field_reached is None and np.any(differs & (light.now != 0)):
                field_reached = tick
            if field_reached is None:
                assert np.array_equal(simulation.records[light_identity].now, light.now), tick
                compared += 1
        if given is not None and tick == given + 100:
            break
    assert compared > 1 and (field_reached is None or field_reached > 1)
    # the first giving within the well's period (the residue's wait, ALGEBRA.md #the-click)
    assert given is not None and given < 120
    live = simulation.records[identity]
    ahead = int(np.max(np.abs(live.now[140:180, 0, 0])))
    behind = int(np.max(np.abs(live.now[40:90, 0, 0])))
    # SINCE COMMIT 7 the window's record leaves the body both ways (no train's way; COMPUTATION)
    assert ahead > 1000 and behind > 1000, (ahead, behind)
    with pytest.raises(ValueError, match="clock is required: the given family 'matter' declares no"):
        parse_nature_beam_world(matter_emitter_world(True))


def test_a_matter_emitters_record_clicks_once_at_the_rung():
    """A massive record clicks once at the screen, at the first interval 2 W C >= (2 u + 1) T on its
    pointer, and is deleted whole there; two gather lines, the books balanced every interval."""
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
    document["detectors"] = [{"name": "screen", "positions": positions}]
    document["stamp"] = input_stamp(document)  # the stamp of the rebuilt list (record 1886)
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
    # ALGEBRA.md #the-click the second is given (2 u + 1) P / (2 W) after the first's
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
    """The wheel is the record's own (ALGEBRA.md #a-familys-declaration; BUILD.md section 26 item 15): the
    world key `wheel`, a detector set's `wheel`, a block's `wheel` and an emitter's `wheel`
    are each refused by name with the successor named; the same for `residue_order` and
    `residue_seed` on an emitter, `absorbing` and `take` on a block, `take` on a family. The
    edge case: a world without any of them loads."""
    base = with_screen(block_world([240, 1, 1], CHAIN, [156, 157], [], emitter_at(100, 3)), 230)
    parse_nature_beam_world(base)
    for mutate, message in (
        (lambda d: d.__setitem__("wheel", 64), "the world has unknown keys: wheel"),
        (
            lambda d: d["detectors"][0].__setitem__("wheel", 64),
            r"detectors\[0\] has unknown keys: wheel",
        ),
        (lambda d: d["measured"][0].__setitem__("wheel", 64), r"measured\[0\] has unknown keys: wheel"),
        (
            lambda d: d["measured"][0]["emitter"].__setitem__("wheel", [1, 64]),
            r"measured\[0\]\.emitter has unknown keys: wheel",
        ),
        (
            lambda d: d["measured"][0]["emitter"].__setitem__("residue_order", "ordinal"),
            "emitter has unknown keys: residue_order",
        ),
        (
            lambda d: d["measured"][0]["emitter"].__setitem__("residue_seed", 7),
            "emitter has unknown keys: residue_seed",
        ),
        (lambda d: d["measured"][0].__setitem__("absorbing", True), "has unknown keys: absorbing"),
        (
            lambda d: d["measured"][0].__setitem__("take", [-15, 56]),
            r"measured\[0\] has unknown keys: take",
        ),
        (
            lambda d: d["universe"][1].__setitem__("take", [-19, 86]),
            r"universe\[1\] has unknown keys: take",
        ),
    ):
        document = json.loads(json.dumps(base))
        mutate(document)
        document["stamp"] = input_stamp(document)  # the stamp over the whole file (item 28)
        with pytest.raises(ValueError, match=message):
            parse_nature_beam_world(document)


def test_the_receiving_set_beside_the_emitter_books_the_flux_and_clicks_at_its_rung():
    """The receiving set at the emitter's head books the one-way flux and clicks at the record's rung,
    closed or open; a set off the ladder is never chosen; the loader refuses the malformed forms."""
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
            count_before = simulation._body_count(block)
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
    bad["detector_law"] = (
        False  # the flag was the law's name: refused by name (ALGEBRA.md #the-primitives)
    )
    with pytest.raises(ValueError, match="the world has unknown keys: detector_law"):
        parse_nature_beam_world(bad)
    on_body = light_clock_world("open", False)
    on_body["detectors"] = [{"name": "A_face", "block": 0, "positions": [[100, 0, 0]]}]
    on_body["stamp"] = input_stamp(on_body)  # the stamp over the whole file (item 28)
    with pytest.raises(ValueError, match="names a Node of a measured event"):
        parse_nature_beam_world(on_body)
    two = light_clock_world("open", False)
    two["detectors"] = [{"name": "A_face", "block": 0, "positions": [[132, 0, 0], [133, 0, 0]]}]
    two["stamp"] = input_stamp(two)
    with pytest.raises(ValueError, match=r"is a box of sides \[2, 1, 1\]"):
        parse_nature_beam_world(two)
    no_block = light_clock_world("open", True)
    no_block["detectors"] = [{"name": "B", "block": 1}]
    no_block["stamp"] = input_stamp(no_block)
    with pytest.raises(ValueError, match="a receiver set on a BODY is `positions`"):
        parse_nature_beam_world(no_block)
    graced = light_clock_world("open", False)
    graced["measured"][0]["own_grace"] = 70
    with pytest.raises(ValueError, match="has unknown keys: own_grace"):
        parse_nature_beam_world(graced)
    empty = light_clock_world("open", False)
    empty["measured"][0]["amount"] = 0
    with pytest.raises(ValueError, match="amount"):
        parse_nature_beam_world(empty)


def test_a_set_at_a_blocks_cells_books_the_flux_into_them_and_steps_with_the_block():
    """A set bound to a block WITHOUT positions is a receiver (Sagnac's form, DECLARATIONS.md section 13
    item 1) under the flux reading (ALGEBRA.md #rule3): the block's twelve Nodes are the
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
        document["universe"].append(source_family())
        document["measured"] = [
            dict(emitter_at(100, 2), receiver="B_nodes"),
            {
                "position": [200, 0, 0],
                "family": "matter",
                "amount": 1,
                "stocks": {},
                "ramp": 0,
                "start": 0,
                "momentum": momentum,
                "fixed": False,
                "side": 12,
                "q": 0,
                "spin": [0, 0, 0],
                "twist": 0,
                "moment": [0, 0, 0],
                "pair": [800, 801],
                "seed": 50 << 12,
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
            count_before = simulation._body_count(block)
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
        assert np.array_equal(simulation.detector_at_node == detector, block.mask)
    bad = document
    bad["detectors"] = [{"name": "B_nodes", "block": 1, "wheel": 64}]
    bad["stamp"] = input_stamp(bad)  # the stamp over the whole file (item 28)
    with pytest.raises(ValueError, match="has unknown keys: wheel"):
        parse_nature_beam_world(bad)


def test_a_wall_of_lights_kind_is_a_mirror_line():
    """A line of blocks of light's kind at the pair [1, 2], four Nodes deep, is a mirror: beyond it the largest level stays below four percent of the level before it over 200 intervals (COMPUTATION), the books balanced; a light-kind block with seed or margin, and any block with coupling, refused by name."""
    document = chain_world()  # the closed chain (BUILD.md section 26 item 14)
    document["massive_record"] = True
    document["amplitude_bound"] = 1 << 22
    document["ticks"] = 200
    for x in (40, 41, 42, 43):
        document["measured"].append(
            {
                "position": [x, 0, 0],
                "family": "light",
                "amount": 1,
                "stocks": {},
                "ramp": 0,
                "start": 0,
                "momentum": [0, 0, 0],
                "fixed": False,
                "side": 1,
                "q": 0,
                "spin": [0, 0, 0],
                "twist": 0,
                "moment": [0, 0, 0],
                "pair": [1, 2],
            }
        )
    document["stamp"] = input_stamp(document)  # the stamp over the whole file (item 28)
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
    lines: list[dict] = []
    simulation = DetectorLawSimulation(world, observer=lines.append)
    assert all(block.own is None for block in simulation.blocks[1:])
    assert int(simulation.kind_den[0][40, 0, 0]) == 2 and int(simulation.kind_den[0][41, 0, 0]) == 2
    assert int(simulation.kind_den[0][39, 0, 0]) == 1 and int(simulation.kind_num[0][40, 0, 0]) == 1
    for _ in range(200):
        simulation.step()
        assert simulation.books()["balanced"], simulation.tick
    # the measurement: nothing given crosses the wall to click at `screen` at [70, 72]
    givings = [line for line in lines if line["event"] == "giving"]
    gathers = [line for line in lines if line["event"] == "gather"]
    assert len(givings) == 2 and gathers == []
    assert all(line["record"] in simulation.records for line in givings)
    for key, value in (("seed", 5), ("margin", "control")):
        bad = json.loads(json.dumps(document))
        bad["measured"][4][key] = value
        with pytest.raises(ValueError, match="refused on a block of light's kind"):
            parse_nature_beam_world(bad)
    coupled = json.loads(json.dumps(document))
    coupled["measured"][4]["coupling"] = {"G": [1, 1], "g": [1, 2]}
    with pytest.raises(ValueError, match="has unknown keys: coupling"):
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
