"""THE SIGNED READ WITH THE TWO-SIDED GUARD, its own folder (ALGEBRA.md 9.117 item 2, the first row;
9.108 item 12; record 2224): the folder's read equals the engine's bit for bit on the emitter's world,
the hand identity holds, the guard's edge (the checkerboard factor at -2) admits and refuses by name."""

from __future__ import annotations

import numpy as np
import pytest

from event_universe.core.register import folder_of
from event_universe.core.rule3 import coefficients
from event_universe.events.detector_law import DetectorLawSimulation
from event_universe.features import signed_read
from event_universe.features.signed_read import (
    DECLARATION,
    THE_WORD,
    SignedReadOwn,
    SignedReadStart,
    SignedReadTerm,
    apply,
    bind,
    pace_bound,
    stability_bound,
)
from event_universe.world_files import parse_nature_beam_world
from tests.bodies import GAMMA as CHAIN_GAMMA
from tests.bodies import MATTER, QUANTA, charged_chain
from tests.worlds import PERIODIC, emitter_world

GAMMA = 10_000
SHAPE = (3, 3, 3)


def term_of(simulation: DetectorLawSimulation, family: int) -> SignedReadTerm:
    definition = simulation.families[family]
    return SignedReadTerm(
        tuple((other, weight, by) for other, weight, by, _twist in definition.reads),
        simulation.family_charge[family],
        (int(definition.pair[0]), int(definition.pair[1])),
        simulation.node_clock,
    )


def start_of(simulation: DetectorLawSimulation, family: int) -> SignedReadStart:
    return SignedReadStart(
        simulation.shape, dict(simulation.node_level), simulation._axis_contents(family)
    )


def own_of(simulation: DetectorLawSimulation, family: int) -> SignedReadOwn:
    return SignedReadOwn(family, simulation.families[family].name, simulation.tick)


def hand_line(simulation: DetectorLawSimulation, family: int, node: tuple[int, ...]) -> int:
    """The trace's line of the pace's read at one Node (ALGEBRA.md 9.112 item 5): per read the family,
    the signed weight, the level, by plain or by sign with q, the product; p_0 = Gamma - the sum."""
    q = simulation.family_charge[family]
    products = []
    for other, weight, by, _twist in simulation.families[family].reads:
        level = int(simulation.node_level[other][node])
        products.append(weight * level if by == "plain" else -q * weight * level)
    return simulation.node_clock - sum(products)


def test_apply_equals_the_engines_read_bit_for_bit_on_the_emitters_world():
    """The emitter's unit world: the folder's content equals `_effective_content` at every reading family
    over twenty intervals, the guard passes, and the hand identity p_0 = Gamma - the sum holds."""
    simulation = DetectorLawSimulation(parse_nature_beam_world(emitter_world(stock=1, ticks=20)))
    readers = [family for family, definition in enumerate(simulation.families) if definition.reads]
    assert readers
    nodes = [(x, 0, 0) for x in (0, 5, 21, 36, 71)]
    for _ in range(20):
        simulation.step()
        for family in readers:
            writes = apply(
                term_of(simulation, family), start_of(simulation, family), own_of(simulation, family)
            )
            assert np.array_equal(writes.content, simulation._effective_content(family))
            assert writes.content.dtype == np.int64
            for node in nodes:
                pace = simulation.node_clock - int(writes.content[node])
                assert pace == hand_line(simulation, family, node)
                assert pace == simulation.node_clock_pair(node, family)[0]


def test_the_edge_is_where_the_rules_checkerboard_factor_crosses_minus_two():
    """The guard's bound P = isqrt(Gamma^2 (18 den + 6 num) div (18 num + 6 den)) is the last pace with
    (S - 6 R) + 2 w >= 0 on the rule's (R, S, w): 1002 for [800, 809], 1015 for [800, 850], 1000 for [1, 1]"""
    for pair, expected in (((800, 809), 1002), ((800, 850), 1015), ((1, 1), 1000)):
        bound = pace_bound(pair, CHAIN_GAMMA)
        assert bound == expected
        left, right = stability_bound(pair, CHAIN_GAMMA)
        assert bound * bound * left <= right < (bound + 1) * (bound + 1) * left
        for pace, admitted in ((bound, True), (bound + 1, False)):
            (read, _, _), self_coefficient, wall = coefficients(
                pair[0], pair[1], CHAIN_GAMMA, CHAIN_GAMMA - pace
            )
            assert (self_coefficient - 6 * read + 2 * wall >= 0) is admitted


@pytest.mark.diagnostic
def test_a_like_charge_hill_is_admitted_to_the_edge_and_refused_beyond_it_naming_the_node():
    """The charged chain: a matter record of charge +1 reads c - Lambda d; at Lambda = 1 p = 1000 <=
    1002, admitted (the largest pace over the GameBoard is a GameBoard reading, a diagnostic,
    not a measurement); at Lambda = 3 p = 1020 beyond the edge of [800, 809], refused naming a slab Node."""
    admitted = DetectorLawSimulation(
        parse_nature_beam_world(charged_chain(60, PERIODIC, range(20, 30), QUANTA, 1, 1, 1))
    )
    for _ in range(3):
        admitted.step()
        writes = apply(term_of(admitted, MATTER), start_of(admitted, MATTER), own_of(admitted, MATTER))
        assert np.array_equal(writes.content, admitted._effective_content(MATTER))
        # a GameBoard reading (a diagnostic), not a measurement
        assert int(np.max(admitted.node_clock - writes.content)) == CHAIN_GAMMA
    refused = DetectorLawSimulation(
        parse_nature_beam_world(charged_chain(60, PERIODIC, range(20, 30), QUANTA, 1, 1, 3))
    )
    with pytest.raises(RuntimeError, match=r"is 1020 at the Node \(20, 0, 0\) at interval 0, above"):
        apply(term_of(refused, MATTER), start_of(refused, MATTER), own_of(refused, MATTER))


def test_the_guard_refuses_a_hill_beyond_the_stability_edge_naming_the_node():
    """A hill raises the pace above Gamma; [800, 850] admits it up to p = 1.0152 Gamma: at Gamma = 10^4 a
    hill of 152 passes, 153 ends the run naming the Node, and 10^8 is refused with no pace squared."""
    left, right = stability_bound((800, 850), GAMMA)
    assert (left, right) == (19_500, GAMMA * GAMMA * 20_100) and pace_bound((800, 850), GAMMA) == 10_152
    term = SignedReadTerm(((1, -1, signed_read.BY_PLAIN),), 0, (800, 850), GAMMA)
    own = SignedReadOwn(0, "matter", 7)

    def hill(depth: int) -> SignedReadStart:
        level = np.zeros(SHAPE, dtype=np.int64)
        level[1, 1, 1] = depth
        return SignedReadStart(SHAPE, {1: level}, None)

    passing = apply(term, hill(152), own)
    assert int(passing.content[1, 1, 1]) == -152 and int(passing.content[0, 0, 0]) == 0
    with pytest.raises(RuntimeError, match=r"is 10153 at the Node \(1, 1, 1\) at interval 7, above"):
        apply(term, hill(153), own)
    with pytest.raises(RuntimeError, match=r"is 100010000 at the Node \(1, 1, 1\)"):
        apply(term, hill(100_010_000 - GAMMA), own)
    # the same hill on the axis contents alone is caught on that axis
    flat = np.zeros(SHAPE, dtype=np.int64)
    axis = np.zeros(SHAPE, dtype=np.int64)
    axis[2, 0, 1] = -153
    with pytest.raises(RuntimeError, match=r"axis 2\) is 10153 at the Node \(2, 0, 1\)"):
        apply(
            SignedReadTerm(((1, 1, signed_read.BY_PLAIN),), 0, (800, 850), GAMMA),
            SignedReadStart(SHAPE, {1: flat}, (flat, axis, flat)),
            own,
        )


def test_a_massless_family_admits_no_hill_and_every_family_needs_a_pace_above_zero():
    """For den = num the edge is p <= Gamma exactly, so any hill ends the run; a content
    at Gamma (the pace 0) ends the run on the lower side; Gamma - 1 passes."""
    massless = SignedReadTerm(((1, 1, signed_read.BY_PLAIN),), 0, (1, 1), GAMMA)
    own = SignedReadOwn(2, "light", 3)
    shape = (2, 2, 2)
    hollow = np.zeros(shape, dtype=np.int64)
    hollow[0, 1, 0] = -1
    with pytest.raises(RuntimeError, match=r"is 10001 at the Node \(0, 1, 0\) at interval 3, above"):
        apply(massless, SignedReadStart(shape, {1: hollow}, None), own)
    deep = np.zeros(shape, dtype=np.int64)
    deep[1, 1, 1] = GAMMA
    with pytest.raises(RuntimeError, match=r"is 0 at the Node \(1, 1, 1\) at interval 3: the pace"):
        apply(massless, SignedReadStart(shape, {1: deep}, None), own)
    deep[1, 1, 1] = GAMMA - 1
    assert (
        int(apply(massless, SignedReadStart(shape, {1: deep}, None), own).content[1, 1, 1]) == GAMMA - 1
    )


def test_a_multi_read_sum_by_sign_and_the_argument_of_a_pair_as_d_i():
    """Three reads (2 a - 3 b plain, + 4 c by sign with q = -1) sum per Node exactly; no reads give 0; a
    phase-2 read takes D_i = now^2 - next x before as handed in, times the weight (9.108 item 13)."""
    shape = (2, 1, 1)
    a = np.array([[[5]], [[7]]], dtype=np.int64)
    b = np.array([[[1]], [[-2]]], dtype=np.int64)
    c = np.array([[[3]], [[0]]], dtype=np.int64)
    term = SignedReadTerm(
        ((1, 2, signed_read.BY_PLAIN), (2, -3, signed_read.BY_PLAIN), (3, 4, signed_read.BY_SIGN)),
        -1,
        (800, 850),
        GAMMA,
    )
    writes = apply(term, SignedReadStart(shape, {1: a, 2: b, 3: c}, None), SignedReadOwn(0, "matter", 0))
    assert writes.content.tolist() == [[[2 * 5 - 3 * 1 + 4 * 3]], [[2 * 7 + 3 * 2]]]
    silent = apply(
        SignedReadTerm((), 0, (1, 1), GAMMA), SignedReadStart(shape, {}, None), SignedReadOwn(1, "x", 0)
    )
    assert not silent.content.any() and silent.content.shape == shape
    before = np.array([[[3]], [[-4]]], dtype=np.int64)
    now = np.array([[[5]], [[6]]], dtype=np.int64)
    after = np.array([[[7]], [[2]]], dtype=np.int64)
    invariant = now * now - after * before  # formed by the loop from the last step's three levels
    assert invariant.tolist() == [[[25 - 21]], [[36 + 8]]]
    sourced = SignedReadTerm(((5, -2, signed_read.BY_PLAIN),), 0, (800, 850), GAMMA)
    writes = apply(sourced, SignedReadStart(shape, {5: invariant}, None), SignedReadOwn(0, "matter", 1))
    assert writes.content.tolist() == [[[-8]], [[-88]]]


def test_a_read_by_an_unknown_word_and_a_sum_that_could_leave_int64_are_refused_by_name():
    """A read by a word other than plain or sign is refused naming the family and the word; a read whose
    reach leaves int64 is refused before any product; two reads whose reach together leaves int64 too."""
    shape = (2, 1, 1)
    level = np.array([[[3]], [[-4]]], dtype=np.int64)
    own = SignedReadOwn(0, "matter", 0)
    with pytest.raises(ValueError, match="the read of family 1 is by 'signed': by 'plain' or by 'sign'"):
        apply(
            SignedReadTerm(((1, 1, "signed"),), 1, (800, 850), GAMMA),
            SignedReadStart(shape, {1: level}, None),
            own,
        )
    huge = np.array([[[10**16]], [[-(10**16)]]], dtype=np.int64)
    with pytest.raises(
        ValueError, match=r"family 1 at the weight 1000 reaches 10000000000000000000 .*int64"
    ):
        apply(
            SignedReadTerm(((1, 1000, signed_read.BY_PLAIN),), 0, (800, 850), GAMMA),
            SignedReadStart(shape, {1: huge}, None),
            own,
        )
    half = np.array([[[5 * 10**18]], [[0]]], dtype=np.int64)
    two = SignedReadTerm(
        ((1, 1, signed_read.BY_PLAIN), (2, -1, signed_read.BY_PLAIN)), 0, (800, 850), GAMMA
    )
    assert signed_read.content_of(
        SignedReadTerm(two.reads[1:], 0, (800, 850), GAMMA), SignedReadStart(shape, {2: half}, None)
    ).tolist() == [[[-(5 * 10**18)]], [[0]]]
    with pytest.raises(
        ValueError, match=r"the read of family 2 at the weight -1 reaches 10000000000000000000"
    ):
        signed_read.content_of(two, SignedReadStart(shape, {1: half, 2: half}, None))
    assert signed_read.TOTAL_BOUND == 2**63 - 1


def test_the_declaration_is_the_ledgers_row():
    """The folder declares the row of ALGEBRA.md 9.117: the name, the place (i), the four reads in the
    row's words, the paces as its one write with no order, its function `apply`, its section."""
    assert DECLARATION.name == "the signed read"
    assert DECLARATION.place == "(i)"
    assert DECLARATION.reads == (
        "the read families' arguments at the interval's start (a level, or D_i for a pair)",
        "the signed weights",
        "by (plain, or q)",
        "the axis contents with their remainders",
    )
    assert DECLARATION.writes == ("the paces",)
    assert DECLARATION.function is apply and DECLARATION.built
    assert DECLARATION.word == "the right side"
    assert DECLARATION.section.startswith(THE_WORD) and THE_WORD.startswith("from the rule")
    assert "9.117" in DECLARATION.section and "9.108" in DECLARATION.section
    assert folder_of(DECLARATION.name) == "signed_read"
    # the engine's register finds this folder and, until the loop calls apply, binds the
    # loop's read of today through `bind`, which apply equals bit for bit
    simulation = DetectorLawSimulation(parse_nature_beam_world(emitter_world(stock=1, ticks=2)))
    assert bind(simulation)(1) is simulation._effective_content(1)
    registered = simulation.register.declarations["the signed read"]
    assert registered.reads == DECLARATION.reads and registered.built
