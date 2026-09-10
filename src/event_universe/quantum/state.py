"""Bounded integer records for deferred quantum evaluation.

This module deliberately does not import the simulator world, fields, dynamics,
models, diagnostics, or integration layer. Quantum history is global sidecar
state, never per-cell physical state.
"""

from dataclasses import dataclass
from typing import NamedTuple

from event_universe.core.state import Address, checked, checked_work

EMPTY_NODE = -1
Q_SOURCE = 1
Q_PHASE = 2
Q_SUM2 = 3
Q_MEASURE = 4


class Amplitude(NamedTuple):
    real: int
    imag: int


ZERO_AMP = Amplitude(0, 0)


class QuantumNode(NamedTuple):
    """Fixed-width node. Every field is an integer; two parents maximum."""

    kind: int
    parent_a: int
    parent_b: int
    value_a: int
    value_b: int
    param: int
    x: int
    y: int
    z: int
    tick: int


@dataclass(frozen=True, slots=True)
class QuantumConfig:
    max_nodes: int = 1_000_000
    max_eval_nodes: int = 100_000
    max_cached_results: int = 4_096

    def __post_init__(self) -> None:
        checked(self.max_nodes)
        checked(self.max_eval_nodes)
        checked(self.max_cached_results)
        if min(self.max_nodes, self.max_eval_nodes, self.max_cached_results) <= 0:
            raise ValueError("quantum budgets must be positive")


def checked_address(address: Address) -> Address:
    if type(address) is not tuple or len(address) != 3:
        raise ValueError("quantum address must be an immutable 3D tuple")
    x, y, z = address
    return checked(x), checked(y), checked(z)


def checked_amp(real: int, imag: int) -> Amplitude:
    return Amplitude(checked(real), checked(imag))


def add_amp(a: Amplitude, b: Amplitude) -> Amplitude:
    checked_amp(a.real, a.imag)
    checked_amp(b.real, b.imag)
    return checked_amp(a.real + b.real, a.imag + b.imag)


def phase_quarter_turns(a: Amplitude, turns: int) -> Amplitude:
    """Exact multiplication by i**turns using integers only."""
    checked_amp(a.real, a.imag)
    checked(turns)
    turn = turns % 4
    if turn == 0:
        return a
    if turn == 1:
        return checked_amp(-a.imag, a.real)
    if turn == 2:
        return checked_amp(-a.real, -a.imag)
    return checked_amp(a.imag, -a.real)


def amplitude_weight(a: Amplitude) -> int:
    """Born numerator |a|^2, exact integer work with bounded result."""
    checked_amp(a.real, a.imag)
    real_squared = checked_work(a.real * a.real)
    imag_squared = checked_work(a.imag * a.imag)
    return checked(checked_work(real_squared + imag_squared))
