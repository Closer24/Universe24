"""An exact one-channel ternary divider inside the unchanged Rule3 Engine.

This is an arithmetic experiment, not a coupled Einstein integrator. A
passive readout uses the retained core remainder; tensor factors cannot read
that remainder. Autonomous quotient handoff/reuse is an open compilation
problem and is deliberately not simulated by a runtime callback.
"""
from dataclasses import dataclass

import numpy as np

from universe24.algebra.null_covector import integer_array
from universe24.core import GearType, State, Tensor
from universe24.core.lattice import ZERO, lattice


def division_tensor():
    """One linear channel, u=10b; no old-a reads, scratch, or clock."""
    return Tensor([GearType('division.ternary', label='audit')],
                  [('division.ternary', 10, (('division.ternary', ZERO, 'b'),))],
                  strict_support=True)


def prepare(values, *, L=3):
    """Initialize a=b=integer input and r=0 independently at each node."""
    values = integer_array(values)
    size = lattice(L).N
    if values.ndim == 0:
        values = np.full((1, size), int(values), dtype=object)
    elif values.shape == (size,):
        values = values.reshape(1, size)
    if values.shape != (1, size):
        raise ValueError(f'Expected one integer or {size} node integers')
    return State(L, values.copy(), values.copy(), np.zeros_like(values))


@dataclass(frozen=True)
class DivisionReadout:
    quotient: np.ndarray
    history: np.ndarray
    digit: np.ndarray


def readout(state):
    """Proved exact integer coordinates on the even-remainder sector.

    e=r/2, z=(3a-b-e)/2, w=(3b-a+e)/2. The invariant sector is
    r even and 3a-b-e even. The induced transition is
       e_next = z mod 3,
       z_next = (z-e_next)/3 = floor(z/3),
       w_next = 3w-e.
    Thus preparation above gives z_n=floor(input/3**n). The growing w
    retains the information removed from z; one channel means three retained
    integer entries, not bounded bit memory.
    """
    if state.G != 1:
        raise ValueError('Expected the standalone one-channel divider')
    a, b, r = (np.asarray(value, dtype=object) for value in (state.a, state.b, state.r))
    if np.any(r < 0) or np.any(r > 5) or np.any(r % 2):
        raise ValueError('Expected legal even core remainders')
    digit = r//2
    numerator = 3*a-b-digit
    if np.any(numerator % 2):
        raise ValueError('State is outside the integer-coordinate sector')
    quotient = numerator//2
    history = (3*b-a+digit)//2
    if np.any((history-quotient+digit) % 4):
        raise AssertionError('Coordinate congruence is inconsistent')
    return DivisionReadout(quotient, history, digit)


def coordinate_inverse(quotient, history, digit):
    """Exact inverse coordinate chart, including its modulo-four domain."""
    quotient, history, digit = (integer_array(v) for v in (quotient, history, digit))
    if quotient.shape != history.shape or quotient.shape != digit.shape:
        raise ValueError('Coordinate shapes must agree')
    if np.any(digit < 0) or np.any(digit > 2) or np.any((history-quotient+digit) % 4):
        raise ValueError('Illegal coordinate sector')
    return (3*quotient+history+digit)//4, (quotient+3*history-digit)//4, 2*digit


def coordinate_inverse_step(after):
    """Independent inverse of the derived arithmetic map, not Engine code."""
    old_digit = (-after.history) % 3
    return DivisionReadout(3*after.quotient+after.digit,
                           (after.history+old_digit)//3, old_digit)
