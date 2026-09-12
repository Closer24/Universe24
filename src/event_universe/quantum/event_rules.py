"""Bounded local matrix rules for the deferred event-network candidate.

Matrices have a common implicit scale. Coherent rules obey U*U = scale I;
instruments obey sum(K* K) = scale I. No square roots or float normalization
are needed. Selecting an instrument is an explicit model input, not a universal
criterion for collapse. This module does not own a physical world.
"""

from dataclasses import dataclass

from event_universe.core.state import bounded_gcd, checked, checked_work

from .state import Amplitude, checked_amp

Matrix = tuple[tuple[Amplitude, ...], ...]
State = tuple[tuple[int, Amplitude], ...]


def multiply(a: Amplitude, b: Amplitude) -> Amplitude:
    """Check products before adding; cancellation cannot conceal overflow."""
    real = checked_work(checked_work(a.real * b.real) - checked_work(a.imag * b.imag))
    imag = checked_work(checked_work(a.real * b.imag) + checked_work(a.imag * b.real))
    return checked_amp(real, imag)


def plus(a: Amplitude, b: Amplitude) -> Amplitude:
    return checked_amp(checked_work(a.real + b.real), checked_work(a.imag + b.imag))


def matrix_shape(matrix: Matrix) -> int:
    if type(matrix) is not tuple or len(matrix) not in (2, 4, 8, 16):
        raise ValueError("local matrix must have dimension two, four, eight or sixteen")
    size = len(matrix)
    for row in matrix:
        if type(row) is not tuple or len(row) != size:
            raise ValueError("matrix rows must be immutable and square")
        for value in row:
            if type(value) is not Amplitude:
                raise TypeError("matrix coefficients require Amplitude records")
            checked_amp(value.real, value.imag)
    return size


def common_scale(matrices: tuple[Matrix, ...]) -> int:
    """Validate completeness with bounded work, including off-diagonal terms."""
    if type(matrices) is not tuple or not 1 <= len(matrices) <= 4:
        raise ValueError("one to four matrices are supported")
    size = matrix_shape(matrices[0])
    if any(matrix_shape(matrix) != size for matrix in matrices):
        raise ValueError("all branch matrices must have the same dimension")
    scale = 0
    for a in range(size):
        for b in range(size):
            real = imag = 0
            for matrix in matrices:
                for row in matrix:
                    x, y = row[a], row[b]
                    real = checked_work(real + checked_work(x.real * y.real))
                    real = checked_work(real + checked_work(x.imag * y.imag))
                    imag = checked_work(imag + checked_work(x.real * y.imag))
                    imag = checked_work(imag - checked_work(x.imag * y.real))
            if a == b == 0:
                scale = checked(real)
            if imag or real != (scale if a == b else 0):
                raise ValueError("matrices do not preserve total Born probability")
    if scale <= 0:
        raise ValueError("a positive common matrix scale is required")
    return scale


@dataclass(frozen=True, slots=True)
class LocalUnitary:
    """A configured coherent rule; names have no physical interpretation."""

    matrix: Matrix

    def __post_init__(self) -> None:
        common_scale((self.matrix,))


@dataclass(frozen=True, slots=True)
class LocalInstrument:
    """Explicit one-cell instrument, including every no-event branch.

    One Kraus matrix per outcome is the supported pure conditional-state
    contract. Multiple indistinguishable Kraus branches need a mixed-state
    extension and must not be represented as the same sampled record here.
    """

    branches: tuple[Matrix, ...]

    def __post_init__(self) -> None:
        common_scale(self.branches)
        if len(self.branches[0]) != 2:
            raise ValueError("instruments act on one cell only")


def squared_norm(state: State) -> int:
    total = 0
    for _, amp in state:
        total = checked_work(total + checked_work(amp.real * amp.real))
        total = checked_work(total + checked_work(amp.imag * amp.imag))
    return checked(total)


def reduce_state(state: State) -> State:
    """Remove only an exact common integer factor, not quantum normalization."""
    divisor = 0
    for _, amp in state:
        divisor = bounded_gcd(divisor, amp.real)
        divisor = bounded_gcd(divisor, amp.imag)
    if not divisor:
        raise ArithmeticError("zero conditional state")
    return tuple((bits, checked_amp(amp.real // divisor, amp.imag // divisor)) for bits, amp in state)


def apply_matrix(state: State, matrix: Matrix, sites: tuple[int, ...], max_terms: int) -> State:
    """Host evaluation on a bounded sparse joint state; never a local-cell loop."""
    out: dict[int, Amplitude] = {}
    mask = sum(1 << q for q in sites)
    for bits, amp in state:
        column = sum(((bits >> q) & 1) << j for j, q in enumerate(sites))
        for row in range(len(matrix)):
            value = multiply(matrix[row][column], amp)
            if value == (0, 0):
                continue
            target = (bits & ~mask) | sum(((row >> j) & 1) << q for j, q in enumerate(sites))
            if target not in out and len(out) >= max_terms:
                raise OverflowError("quantum term budget exceeded")
            value = plus(out.get(target, Amplitude(0, 0)), value)
            if value == (0, 0):
                out.pop(target, None)
            else:
                out[target] = value
    return tuple(sorted(out.items()))
