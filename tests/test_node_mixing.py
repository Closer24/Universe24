"""The Node mixes the six (node-mixing-v1; Highlights 5.4, point 24, the model
owner's decision of 2026-09-18), isolated on one Node of the engine's layer:
the kernels of `event_universe.shadow.mixing` over a `ShadowLayer` of shape
(1, 1, 1) with one number and the phase circle N = 8.

The rule: the shadows that arrived on each heading are one amplitude,
sqrt(amount) in 32nds at the step nearest their coherent sum; the leaving
amplitude of a heading is the coherent sum less three times the arrival that
came in through its Port; the total in ninths is shared by the squared leaving
amplitudes with the largest-remainder rule, ties to the lower Port; the whole
quanta leave at the phase of the leaving amplitude and the ninths below one
quantum park at the Node (the remainder rule, point 22), leaving whole when
they reach nine; the momentum a group carries goes with the shares. The
expected integers are those of docs/TEST_EXPECTATIONS.md ("The Node's
mixing"), written down before the first run:

(a) 9 on +X: 4 back through the Port it came in by at the opposite phase and
    1 each other way, nothing parked;
(b) 9 on +X and 9 on -X in phase: 1 back each way at the opposite phase and 4
    on each transverse heading;
(c) 9 on +X at phase 0 and 9 on -X at phase 4 (antiphase): each sent back whole;
(d) two arrivals on one heading are one amplitude at the phase of their sum
    (9 at 0 and 9 at 2 on +X: 18 at step 1, then as (a) doubled);
(e) 24 on +X at 0 and 8 on -X at 2: 6 on +X at phase 7, 11 on -X at phase 4,
    3 transverse at phase 1, ninths (2, 5, 5, 5, 5, 5) parked;
(f) the remainder rule: 5 on +X parks (5, 2, 5, 5, 5, 5) ninths and sends 2
    back; the same again releases one whole quantum on every heading but the
    back one, (1, 4, 1, 1, 1, 1) left;
(g) the momentum carried, (9, 0, 0) on 9 arriving on +X, is shared over the
    departures as (1, 4, 1, 1, 1, 1) on x, nothing parked.
"""

from __future__ import annotations

import numpy as np

from event_universe.core.lattice import PORT_HEADINGS
from event_universe.shadow.layer import ShadowLayer
from event_universe.shadow.mixing import (
    MIXING_DENOMINATOR,
    MIXING_OPPOSITE,
    mix_arrivals,
    release_parked,
)

X, MINUS_X = 0, 1


def one_node(steps: int = 8) -> ShadowLayer:
    """One Node, one number, the circle of `steps` steps; no phase turn in flight."""
    return ShadowLayer(0, (1, 1, 1), (1,), steps, 1 << 20, rotates=False)


def arrive(layer: ShadowLayer, port: int, amount: int, phase: int = 0, slot: int = 0) -> None:
    layer.arr_amt[0, 0, 0, 0, port, slot] = amount
    layer.arr_ph[0, 0, 0, 0, port, slot] = phase


def mixed(layer: ShadowLayer) -> tuple[list[int], list[int], list[int], list[int]]:
    whole, phase, _ = mix_arrivals(layer)
    return (
        whole[0, 0, 0, 0].tolist(),
        phase[0, 0, 0, 0].tolist(),
        layer.reg[0, 0, 0, 0].tolist(),
        layer.regph[0, 0, 0, 0].tolist(),
    )


def test_a_lone_arrival_sends_four_ninths_back_and_a_ninth_each_way():
    """(a): the back Port is the opposite of the travel heading."""
    assert PORT_HEADINGS[MINUS_X] == (-1, 0, 0) and MIXING_OPPOSITE[X] == MINUS_X
    layer = one_node()
    arrive(layer, X, 9)
    whole, phase, ninths, _ = mixed(layer)
    assert whole == [1, 4, 1, 1, 1, 1]
    assert phase == [0, 4, 0, 0, 0, 0]
    assert ninths == [0, 0, 0, 0, 0, 0]


def test_two_equal_arrivals_in_phase_go_a_ninth_on_axis_and_four_ninths_transverse():
    """(b)."""
    layer = one_node()
    arrive(layer, X, 9)
    arrive(layer, MINUS_X, 9)
    whole, phase, ninths, _ = mixed(layer)
    assert whole == [1, 1, 4, 4, 4, 4]
    assert phase == [4, 4, 0, 0, 0, 0]
    assert ninths == [0, 0, 0, 0, 0, 0]


def test_two_equal_arrivals_in_antiphase_are_each_sent_back_whole():
    """(c): a heading with no leaving amplitude gets nothing and phase 0."""
    layer = one_node()
    arrive(layer, X, 9, phase=0)
    arrive(layer, MINUS_X, 9, phase=4)
    whole, phase, ninths, _ = mixed(layer)
    assert whole == [9, 9, 0, 0, 0, 0]
    assert phase == [0, 4, 0, 0, 0, 0]
    assert ninths == [0, 0, 0, 0, 0, 0]


def test_two_shadows_on_one_heading_are_one_amplitude():
    """(d): the two layers of one Port sum on the circle before the mixing."""
    layer = one_node()
    arrive(layer, X, 9, phase=0, slot=0)
    arrive(layer, X, 9, phase=2, slot=1)
    whole, phase, ninths, _ = mixed(layer)
    assert whole == [2, 8, 2, 2, 2, 2]
    assert phase == [1, 5, 1, 1, 1, 1]
    assert ninths == [0, 0, 0, 0, 0, 0]


def test_unequal_amounts_and_phases_in_the_integers_of_the_rule():
    """(e): amplitudes 156 and 90 in 32nds, the 288 ninths shared 56, 104, 32,
    32, 32, 32 by the largest remainder."""
    layer = one_node()
    arrive(layer, X, 24, phase=0)
    arrive(layer, MINUS_X, 8, phase=2)
    whole, phase, ninths, parked_phase = mixed(layer)
    assert whole == [6, 11, 3, 3, 3, 3]
    assert phase == [7, 4, 1, 1, 1, 1]
    assert ninths == [2, 5, 5, 5, 5, 5]
    assert parked_phase == [7, 4, 1, 1, 1, 1]
    assert sum(whole) * MIXING_DENOMINATOR + sum(ninths) == 32 * MIXING_DENOMINATOR


def test_the_registers_park_the_ninths_and_release_whole_quanta():
    """(f): the parked ninths of two lone arrivals of 5 release at nine."""
    layer = one_node()
    arrive(layer, X, 5)
    whole, phase, ninths, parked_phase = mixed(layer)
    assert whole == [0, 2, 0, 0, 0, 0] and ninths == [5, 2, 5, 5, 5, 5]
    assert parked_phase == [0, 4, 0, 0, 0, 0]
    released, released_phase, taken = release_parked(layer)
    assert released[0, 0, 0, 0].tolist() == [0, 0, 0, 0, 0, 0]
    layer.arr_amt[...] = 0
    layer.arr_ph[...] = 0
    arrive(layer, X, 5)
    whole, phase, ninths, parked_phase = mixed(layer)
    assert whole == [0, 2, 0, 0, 0, 0] and ninths == [10, 4, 10, 10, 10, 10]
    released, released_phase, taken = release_parked(layer)
    assert released[0, 0, 0, 0].tolist() == [1, 0, 1, 1, 1, 1]
    assert released_phase[0, 0, 0, 0].tolist() == [0, 4, 0, 0, 0, 0]
    assert layer.reg[0, 0, 0, 0].tolist() == [1, 4, 1, 1, 1, 1]
    # The second arrival of 5 is still on the layer, and the ninths left park
    # one whole quantum: the layer holds 5 + 1.
    assert not taken.any() and int(layer.reg.sum()) == MIXING_DENOMINATOR
    assert layer.current() == 6


def test_the_momentum_carried_goes_with_the_shares():
    """(g): exact per axis by the largest remainder; nothing parked when the
    shares are whole."""
    layer = one_node()
    arrive(layer, X, 9)
    layer.arr_mom[0, 0, 0, 0, X, 0] = (9, 0, 0)
    whole, _, momenta = mix_arrivals(layer)
    assert whole[0, 0, 0, 0].tolist() == [1, 4, 1, 1, 1, 1]
    assert momenta[0, 0, 0, 0, :, 0].tolist() == [1, 4, 1, 1, 1, 1]
    assert not momenta[0, 0, 0, 0, :, 1:].any()
    assert not layer.reg_mom.any()
    # The arrivals stay on the layer until the cycle places the departures, so
    # the momentum carried is still the arrivals' (9, 0, 0), exactly what left.
    assert np.array_equal(momenta[0, 0, 0, 0].sum(axis=0), np.array([9, 0, 0]))
    assert np.array_equal(layer.carried(), np.array([9, 0, 0]))
