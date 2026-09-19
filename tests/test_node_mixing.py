"""The Node's computation of the sides with one number present (node-mixing-v3,
the control of one number; Highlights 5.4, point 24 read under the law of
events, the model owner, 2026-09-19), isolated on one Node of the engine's
transit: the kernels of `event_universe.events.mixing` over a `Transit` of
shape (1, 1, 1) with one number and the phase circle N = 8. With one number
the coherent sum over the numbers is that number's own, so these integers are
those of node-mixing-v2 unchanged; two numbers at one Node are
`test_node_mixing_numbers.py`.

The rule: the events that arrived on each heading are one amplitude,
sqrt(amount) in 32nds at their phase; the leaving amplitude of a heading is
the coherent sum less three times the arrival that came in through its Port;
the total is shared by the squared leaving amplitudes in whole units, the
floors and the units left to the largest remainders, ties in the tick's
Port order; a group with no whole for any side goes whole to the heading
nearest the momentum it carries; nothing parks, the Node keeps nothing. The
expected integers are those of docs/TEST_EXPECTATIONS.md ("The Node's
computation of the sides"), written down before the first run:

(a) 9 on +X carrying nothing: 4 back through the Port it came in by at the
    opposite phase and 1 each other way, nothing left over;
(b) 9 on +X and 9 on -X in phase: 1 back each way at the opposite phase and 4
    on each transverse heading;
(c) 9 on +X at phase 0 and 9 on -X at phase 4 (antiphase): each sent back whole;
(d) two arrivals on one heading are one amplitude at the phase of their sum
    (9 at 0 and 9 at 2 on +X: 18 at step 1, then as (a) doubled);
(e) 24 on +X carrying (24, 0, 0) and 8 on -X carrying (-8, 0, 0): the shares
    6.22, 11.56 and 3.56 on each transverse heading, every heading within one
    unit of its share and all 32 placed; the momentum (16, 0, 0) shared over
    the six by the units, exact in total;
(f) a single unit carrying its momentum leaves whole on it, its phase kept;
    one carrying nothing leaves whole by the largest share, back; two
    carrying nothing, no side reaching a whole, leave back together;
(g) the momentum carried: 9 on +X carrying (9, 0, 0): the x momentum
    1, 4, 1, 1, 1, 1 with the departures, the sum (9, 0, 0);
(h) nothing is kept: after every cycle the arrivals are empty and the
    departures sum to what arrived.
"""

from __future__ import annotations

import numpy as np

from event_universe.events.transit import Transit

PLUS_X, MINUS_X, PLUS_Y, MINUS_Y, PLUS_Z, MINUS_Z = range(6)


def one_node(steps: int = 8) -> Transit:
    """One Node, one number, the phase circle of `steps`."""
    return Transit(0, (1, 1, 1), (1,), steps, 1 << 20)


def arrive(
    transit: Transit, port: int, amount: int, phase: int = 0, momentum: tuple[int, int, int] = (0, 0, 0)
) -> None:
    """An arrival travelling on `port`'s heading: it came in through the
    opposite Port; where the slot holds one already, one amplitude."""
    cell = (0, 0, 0, 0, port)
    if transit.arr_amt[cell]:
        transit.receive(*_single(transit, cell, amount, phase, momentum))
        return
    transit.arr_amt[cell] = amount
    transit.arr_ph[cell] = phase
    transit.arr_mom[cell] = momentum


def _single(
    transit: Transit, cell: tuple[int, ...], amount: int, phase: int, momentum: tuple[int, int, int]
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    amounts = np.zeros_like(transit.arr_amt)
    phases = np.zeros_like(transit.arr_ph)
    momenta = np.zeros_like(transit.arr_mom)
    amounts[cell] = amount
    phases[cell] = phase
    momenta[cell] = momentum
    return amounts, phases, momenta


def mixed(transit: Transit) -> tuple[list[int], list[int], list[list[int]]]:
    """One cycle: the departures per Port, their phases and their momenta;
    nothing kept (h)."""
    arrived = int(transit.arr_amt.sum())
    transit.cycle()
    assert not transit.arr_amt.any() and not transit.suspended.any()
    assert int(transit.fly_amt.sum()) == arrived
    return (
        [int(v) for v in transit.fly_amt[0, 0, 0, 0]],
        [int(v) for v in transit.fly_ph[0, 0, 0, 0]],
        transit.fly_mom[0, 0, 0, 0].tolist(),
    )


def test_a_lone_arrival_mostly_turns_back_and_the_shares_are_exact_at_nine():
    """(a): 9 on +X: 4 back at the opposite phase, 1 each other way."""
    transit = one_node()
    arrive(transit, PLUS_X, 9)
    amounts, phases, _ = mixed(transit)
    assert amounts == [1, 4, 1, 1, 1, 1]
    assert phases == [0, 4, 0, 0, 0, 0]


def test_two_equal_arrivals_in_phase_and_in_antiphase():
    """(b) and (c)."""
    transit = one_node()
    arrive(transit, PLUS_X, 9)
    arrive(transit, MINUS_X, 9)
    amounts, phases, _ = mixed(transit)
    assert amounts == [1, 1, 4, 4, 4, 4]
    assert phases == [4, 4, 0, 0, 0, 0]
    transit = one_node()
    arrive(transit, PLUS_X, 9, 0)
    arrive(transit, MINUS_X, 9, 4)
    amounts, phases, _ = mixed(transit)
    assert amounts == [9, 9, 0, 0, 0, 0]
    assert phases == [0, 4, 0, 0, 0, 0]


def test_two_arrivals_on_one_heading_are_one_amplitude():
    """(d): 9 at 0 and 9 at 2 on +X are 18 at step 1, then (a) doubled."""
    transit = one_node()
    arrive(transit, PLUS_X, 9, 0)
    arrive(transit, PLUS_X, 9, 2)
    assert int(transit.arr_amt[0, 0, 0, 0, PLUS_X]) == 18
    assert int(transit.arr_ph[0, 0, 0, 0, PLUS_X]) == 1
    amounts, phases, _ = mixed(transit)
    assert amounts == [2, 8, 2, 2, 2, 2]
    assert phases == [1, 5, 1, 1, 1, 1]


def test_the_units_left_go_whole_by_the_momentum_and_the_momentum_goes_with_the_units():
    """(e) and (g)."""
    transit = one_node()
    arrive(transit, PLUS_X, 24, 0, (24, 0, 0))
    arrive(transit, MINUS_X, 8, 2, (-8, 0, 0))
    amounts, phases, momenta = mixed(transit)
    assert sum(amounts) == 32
    assert 6 <= amounts[PLUS_X] <= 7 and 11 <= amounts[MINUS_X] <= 12
    assert all(3 <= amounts[port] <= 4 for port in (PLUS_Y, MINUS_Y, PLUS_Z, MINUS_Z))
    assert phases == [7, 4, 1, 1, 1, 1]
    assert sum(m[0] for m in momenta) == 16 and all(m[1] == m[2] == 0 for m in momenta)
    assert all(abs(m[0] * 32 - 16 * amount) < 32 for m, amount in zip(momenta, amounts, strict=True))
    transit = one_node()
    arrive(transit, PLUS_X, 9, 0, (9, 0, 0))
    amounts, _, momenta = mixed(transit)
    assert amounts == [1, 4, 1, 1, 1, 1]
    assert [m[0] for m in momenta] == [1, 4, 1, 1, 1, 1]


def test_a_single_unit_leaves_whole_by_its_momentum_or_back_without_one():
    """(f): one unit on +X carrying (1, 0, 0) leaves on +X at its phase; one
    carrying nothing leaves back, the largest share; two carrying nothing
    leave back together."""
    transit = one_node()
    arrive(transit, PLUS_X, 1, 5, (1, 0, 0))
    amounts, phases, momenta = mixed(transit)
    assert amounts == [1, 0, 0, 0, 0, 0] and phases[PLUS_X] == 5 and momenta[PLUS_X] == [1, 0, 0]
    transit = one_node()
    arrive(transit, PLUS_X, 1, 5)
    amounts, phases, _ = mixed(transit)
    assert amounts == [0, 1, 0, 0, 0, 0] and phases[MINUS_X] == 1
    transit = one_node()
    arrive(transit, PLUS_X, 2, 0)
    amounts, _, _ = mixed(transit)
    assert amounts == [0, 2, 0, 0, 0, 0]
