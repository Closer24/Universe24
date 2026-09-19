"""The Node reads what is present: the coherent sum at a Node runs over all
the arrivals there, whatever their number (node-mixing-v3; the model owner,
2026-09-19: the number is a label for the detector, not a kind), isolated on
one Node of the engine's transit (`Transit` of shape (1, 1, 1), two numbers,
N = 8, the tick 0 unless stated) through the kernels of
`event_universe.events.mixing`.

The rule: the amplitude vectors of every number are summed per Port before
the coherent sum; the leaving amplitude of each side is the common sum less
three times what came in through its Port over all numbers; the weights per
side, the squared leaving amplitudes, are common to every number at the
Node; each number places its own units by the common weights (whole units
by the largest remainder, ties in the tick's Port order, per number), a
number with no whole for any side going whole to its own momentum's
heading; the leaving phase of a side is the common leaving amplitude's
phase for every number; every unit keeps its number. The expected integers
of docs/TEST_EXPECTATIONS.md ("The coherent sum over the numbers"), written
down before the first run, with a = 32 sqrt 9 = 96 the amplitude of 9 units
in 32nds:

(a) two numbers, 9 units each, arriving through opposite Ports at phase 0
    (number 1 travelling +X, number 2 travelling -X): the common sum 2a; the
    leaving amplitude 2a - 3a = -a on each x side (phase 4) and 2a on each
    of the four transverse sides (phase 0); the weights 1 : 1 : 4 : 4 : 4 : 4
    of 18, so each number's 9 units are 1/2, 1/2, 2, 2, 2, 2: the floors
    0, 0, 2, 2, 2, 2 and the one unit left to the tie of +X and -X, which
    the tick 0 gives to +X; each number leaves 1, 0, 2, 2, 2, 2, the Node
    2, 0, 4, 4, 4, 4 in all, the phases 4 on +X and 0 across; with the tick
    1 the tie goes to -X, 0, 1, 2, 2, 2, 2 per number;
(b) the same in antiphase (number 2 at phase 4): the common sum 0; the
    leaving amplitudes 3a on +X (phase 0) and -3a on -X (phase 4), 0 on the
    transverse sides; the weights 1 : 1 : 0 : 0 : 0 : 0, so each number's 9
    units are 4.5 each way: the floors 4, 4 and the unit left to the tie,
    which the tick 0 gives to +X; each number leaves 5, 4, 0, 0, 0, 0, the
    Node 10, 8 in all, nothing sideways, the phases 0 on +X and 4 on -X;
    with the tick 1, 4, 5 per number;
(c) a number with no whole goes by its own momentum while the other places
    by the common weights: number 1 with 9 units travelling +X at phase 0
    carrying (9, 0, 0), number 2 with one unit (amplitude 32) travelling -X
    at phase 0 carrying (-1, 0, 0): the common sum 128 (in 32nds); the
    leaving amplitudes 128 - 96 = 32 on +X, 128 - 288 = -160 on -X (phase 4)
    and 128 across; the weights 1024 : 25600 : 16384 (four times) of 92160,
    so number 1's 9 units are 0.1, 2.5, 1.6, 1.6, 1.6, 1.6: the floors
    0, 2, 1, 1, 1, 1 and the three left to the largest remainders, the four
    transverse at 0.6 tied, the tick 0 giving them to +Y, -Y and +Z:
    0, 2, 2, 2, 2, 1, carrying (9, 0, 0) shared by the units, 0, 2, 2, 2,
    2, 1; number 2's unit reaches no whole on any side and goes whole on -X,
    its momentum's heading, at the common phase of that side, 4, carrying
    (-1, 0, 0);
(d) the control: a number alone at the Node with 9 units on +X places
    1, 4, 1, 1, 1, 1 as before (`test_node_mixing` (a)) whether or not the
    other number's slots exist;
(e) nothing is kept: after every cycle the arrivals are empty and every
    number's departures sum to what arrived of it.
"""

from __future__ import annotations

from event_universe.events.transit import Transit

PLUS_X, MINUS_X, PLUS_Y, MINUS_Y, PLUS_Z, MINUS_Z = range(6)
FIRST, SECOND = 0, 1


def one_node(tick: int = 0) -> Transit:
    """One Node, the numbers 1 and 2, the phase circle of 8 steps."""
    transit = Transit(0, (1, 1, 1), (1, 2), 8, 1 << 20)
    transit.tick = tick
    return transit


def arrive(
    transit: Transit,
    rank: int,
    port: int,
    amount: int,
    phase: int = 0,
    momentum: tuple[int, int, int] = (0, 0, 0),
) -> None:
    """An arrival of one number travelling on `port`'s heading into an empty slot."""
    cell = (0, 0, 0, rank, port)
    assert not transit.arr_amt[cell]
    transit.arr_amt[cell] = amount
    transit.arr_ph[cell] = phase
    transit.arr_mom[cell] = momentum


def mixed(transit: Transit) -> tuple[list[list[int]], list[list[int]], list[list[list[int]]]]:
    """One cycle: per number the departures per Port, their phases and their
    momenta; nothing kept and every number's total kept (e)."""
    arrived = [int(v) for v in transit.arr_amt[0, 0, 0].sum(axis=-1)]
    transit.cycle()
    assert not transit.arr_amt.any() and not transit.suspended.any()
    assert [int(v) for v in transit.fly_amt[0, 0, 0].sum(axis=-1)] == arrived
    return (
        transit.fly_amt[0, 0, 0].tolist(),
        transit.fly_ph[0, 0, 0].tolist(),
        transit.fly_mom[0, 0, 0].tolist(),
    )


def test_two_numbers_in_phase_share_the_common_sum_and_each_places_by_the_common_weights():
    """(a)."""
    transit = one_node()
    arrive(transit, FIRST, PLUS_X, 9)
    arrive(transit, SECOND, MINUS_X, 9)
    amounts, phases, _ = mixed(transit)
    assert amounts == [[1, 0, 2, 2, 2, 2], [1, 0, 2, 2, 2, 2]]
    assert phases == [[4, 0, 0, 0, 0, 0], [4, 0, 0, 0, 0, 0]]
    transit = one_node(tick=1)
    arrive(transit, FIRST, PLUS_X, 9)
    arrive(transit, SECOND, MINUS_X, 9)
    amounts, phases, _ = mixed(transit)
    assert amounts == [[0, 1, 2, 2, 2, 2], [0, 1, 2, 2, 2, 2]]
    assert phases == [[0, 4, 0, 0, 0, 0], [0, 4, 0, 0, 0, 0]]


def test_two_numbers_in_antiphase_cancel_the_transverse_sides_for_both():
    """(b)."""
    transit = one_node()
    arrive(transit, FIRST, PLUS_X, 9, 0)
    arrive(transit, SECOND, MINUS_X, 9, 4)
    amounts, phases, _ = mixed(transit)
    assert amounts == [[5, 4, 0, 0, 0, 0], [5, 4, 0, 0, 0, 0]]
    assert phases == [[0, 4, 0, 0, 0, 0], [0, 4, 0, 0, 0, 0]]
    transit = one_node(tick=1)
    arrive(transit, FIRST, PLUS_X, 9, 0)
    arrive(transit, SECOND, MINUS_X, 9, 4)
    amounts, phases, _ = mixed(transit)
    assert amounts == [[4, 5, 0, 0, 0, 0], [4, 5, 0, 0, 0, 0]]
    assert phases == [[0, 4, 0, 0, 0, 0], [0, 4, 0, 0, 0, 0]]


def test_a_number_with_no_whole_goes_by_its_own_momentum_at_the_common_phase():
    """(c)."""
    transit = one_node()
    arrive(transit, FIRST, PLUS_X, 9, 0, (9, 0, 0))
    arrive(transit, SECOND, MINUS_X, 1, 0, (-1, 0, 0))
    amounts, phases, momenta = mixed(transit)
    assert amounts == [[0, 2, 2, 2, 2, 1], [0, 1, 0, 0, 0, 0]]
    assert phases[FIRST] == [0, 4, 0, 0, 0, 0] and phases[SECOND] == [0, 4, 0, 0, 0, 0]
    assert [m[0] for m in momenta[FIRST]] == [0, 2, 2, 2, 2, 1]
    assert momenta[SECOND] == [[0, 0, 0], [-1, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]]


def test_a_number_alone_at_the_node_places_as_before():
    """(d)."""
    for rank in (FIRST, SECOND):
        transit = one_node()
        arrive(transit, rank, PLUS_X, 9)
        amounts, phases, _ = mixed(transit)
        assert amounts[rank] == [1, 4, 1, 1, 1, 1] and phases[rank] == [0, 4, 0, 0, 0, 0]
        assert amounts[1 - rank] == [0] * 6 and phases[1 - rank] == [0] * 6
