"""Exact sparse density operators for discarded, unobserved alternatives.

Only pure sources and completely positive local maps construct these states.
The common positive trace is implicit; reduce only a GLOBAL integer factor.
No eigensolver, root, float, random hidden label or physical-node history is used.
"""

from dataclasses import dataclass

from event_universe.core.state import bounded_gcd, checked, checked_work

from .event_rules import (
    BasisLayout,
    Matrix,
    State,
    apply_matrix,
    multiply,
    plus,
    reduce_state,
    squared_norm,
)
from .state import Amplitude, checked_amp


@dataclass(frozen=True, slots=True)
class DensityState:
    """Internal unnormalized density numerator, constructed by CP evolution."""

    entries: tuple[tuple[int, int, Amplitude], ...]


QuantumState = State | DensityState


def conjugate(value: Amplitude) -> Amplitude:
    return checked_amp(value.real, -value.imag)


def term_count(state: QuantumState) -> int:
    return len(state.entries) if isinstance(state, DensityState) else len(state)


def density(state: QuantumState, limit: int) -> DensityState:
    if isinstance(state, DensityState):
        return state
    if len(state) * len(state) > limit:
        raise OverflowError("density term budget exceeded")
    return DensityState(tuple((a, b, multiply(x, conjugate(y))) for a, x in state for b, y in state))


def trace(state: QuantumState) -> int:
    if not isinstance(state, DensityState):
        return squared_norm(state)
    value = 0
    for a, b, amp in state.entries:
        if a == b:
            if amp.imag or amp.real < 0:
                raise ArithmeticError("invalid density diagonal")
            value = checked_work(value + amp.real)
    return checked(value)


def reduce_quantum(state: QuantumState) -> QuantumState:
    if not isinstance(state, DensityState):
        return reduce_state(state)
    divisor = 0
    for _, _, amp in state.entries:
        divisor = bounded_gcd(divisor, amp.real)
        divisor = bounded_gcd(divisor, amp.imag)
    if not divisor or trace(state) <= 0:
        raise ArithmeticError("zero conditional density state")
    return DensityState(
        tuple((a, b, checked_amp(v.real // divisor, v.imag // divisor)) for a, b, v in state.entries)
    )


def _add(
    out: dict[tuple[int, int], Amplitude], key: tuple[int, int], value: Amplitude, limit: int
) -> None:
    if value == (0, 0):
        return
    if key not in out and len(out) >= limit:
        raise OverflowError("density term budget exceeded")
    value = plus(out.get(key, Amplitude(0, 0)), value)
    if value == (0, 0):
        out.pop(key, None)
    else:
        out[key] = value


def evolve(
    state: QuantumState,
    matrices: tuple[Matrix, ...],
    sites: tuple[int, ...],
    limit: int,
    dimensions: tuple[int, ...],
) -> QuantumState:
    """Apply sum K rho K* WITHOUT branch normalization before summing weights."""
    if not isinstance(state, DensityState) and len(matrices) == 1:
        return apply_matrix(state, matrices[0], sites, limit, dimensions)
    source = density(state, limit)
    layout = BasisLayout(dimensions)
    out: dict[tuple[int, int], Amplitude] = {}
    for matrix in matrices:
        for a, b, amp in source.entries:
            col_a, col_b = layout.extract(a, sites), layout.extract(b, sites)
            for r, row in enumerate(matrix):
                left = multiply(row[col_a], amp)
                if left == (0, 0):
                    continue
                for s, other in enumerate(matrix):
                    value = multiply(left, conjugate(other[col_b]))
                    key = (layout.replace(a, sites, r), layout.replace(b, sites, s))
                    _add(out, key, value, limit)
    return DensityState(tuple((a, b, v) for (a, b), v in sorted(out.items())))


def tensor(a: QuantumState, b: QuantumState, limit: int) -> QuantumState:
    """Inputs have disjoint register support, checked by the graph evaluator."""
    if not isinstance(a, DensityState) and not isinstance(b, DensityState):
        if len(a) * len(b) > limit:
            raise OverflowError("quantum tensor-product budget exceeded")
        return tuple(sorted((checked(x + y), multiply(u, v)) for x, u in a for y, v in b))
    x, y = density(a, limit), density(b, limit)
    if len(x.entries) * len(y.entries) > limit:
        raise OverflowError("density tensor-product budget exceeded")
    return DensityState(
        tuple(
            sorted(
                (checked(a + c), checked(b + d), multiply(u, v))
                for a, b, u in x.entries
                for c, d, v in y.entries
            )
        )
    )


def marginal(state: QuantumState, site: int, dimensions: tuple[int, ...]) -> tuple[int, ...]:
    layout = BasisLayout(dimensions)
    weights = [0] * dimensions[site]
    rows = (
        ((a, v.real) for a, b, v in state.entries if a == b)
        if isinstance(state, DensityState)
        else ((a, squared_norm(((a, v),))) for a, v in state)
    )
    for index, value in rows:
        level = layout.digit(index, site)
        weights[level] = checked(weights[level] + value)
    checked(sum(weights))
    return tuple(weights)


def partial_trace(
    state: QuantumState, sites: tuple[int, ...], dimensions: tuple[int, ...], limit: int
) -> DensityState:
    """Read-only reduced state; never supplied to an ordinary remote physical node."""
    layout = BasisLayout(dimensions)
    outside = tuple(q for q in range(len(dimensions)) if q not in sites)
    out: dict[tuple[int, int], Amplitude] = {}
    for a, b, value in density(state, limit).entries:
        if layout.extract(a, outside) == layout.extract(b, outside):
            _add(out, (layout.extract(a, sites), layout.extract(b, sites)), value, limit)
    result = reduce_quantum(DensityState(tuple((a, b, v) for (a, b), v in sorted(out.items()))))
    assert isinstance(result, DensityState)
    return result
