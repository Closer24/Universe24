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
    if type(matrix) is not tuple or not 2 <= len(matrix) <= 16:
        raise ValueError("local matrix dimension must be between two and sixteen")
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
    if type(matrices) is not tuple or not 1 <= len(matrices) <= 16:
        raise ValueError("one to sixteen Kraus matrices are supported")
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
    """Explicit one-node instrument, including every no-event branch.

    This compatibility form has one Kraus matrix per outcome. Use
    GroupedInstrument for indistinguishable terms within one recorded outcome;
    their density contributions are added without a hidden random draw.
    """

    branches: tuple[Matrix, ...]

    def __post_init__(self) -> None:
        common_scale(self.branches)
        if len(self.branches) > 4 or len(self.branches[0]) > 4:
            raise ValueError(
                "instruments support at most four outcomes on one register of dimension at most four"
            )


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


def apply_matrix(
    state: State,
    matrix: Matrix,
    sites: tuple[int, ...],
    max_terms: int,
    dimensions: tuple[int, ...] = (),
) -> State:
    """Host evaluation on a bounded sparse joint state; never a local-node loop."""
    out: dict[int, Amplitude] = {}
    layout = BasisLayout(dimensions or (2,) * (max(sites) + 1))
    for bits, amp in state:
        column = layout.extract(bits, sites)
        for row in range(len(matrix)):
            value = multiply(matrix[row][column], amp)
            if value == (0, 0):
                continue
            target = layout.replace(bits, sites, row)
            if target not in out and len(out) >= max_terms:
                raise OverflowError("quantum term budget exceeded")
            value = plus(out.get(target, Amplitude(0, 0)), value)
            if value == (0, 0):
                out.pop(target, None)
            else:
                out[target] = value
    return tuple(sorted(out.items()))


@dataclass(frozen=True, slots=True)
class BasisLayout:
    """Bounded mixed-radix basis; binary defaults preserve existing state keys."""

    dimensions: tuple[int, ...]

    def __post_init__(self) -> None:
        if type(self.dimensions) is not tuple or not 1 <= len(self.dimensions) <= 30:
            raise ValueError("one to thirty immutable register dimensions required")
        size = 1
        for dimension in self.dimensions:
            if not 2 <= checked(dimension) <= 4:
                raise ValueError("register dimension must be two, three or four")
            size = checked(size * dimension)

    def stride(self, site: int) -> int:
        value = 1
        for d in self.dimensions[:site]:
            value = checked(value * d)
        return value

    def digit(self, index: int, site: int) -> int:
        return (index // self.stride(site)) % self.dimensions[site]

    def extract(self, index: int, sites: tuple[int, ...]) -> int:
        local, stride = 0, 1
        for site in sites:
            local = checked(local + self.digit(index, site) * stride)
            stride = checked(stride * self.dimensions[site])
        return local

    def replace(self, index: int, sites: tuple[int, ...], local: int) -> int:
        for site in sites:
            local, value = divmod(local, self.dimensions[site])
            index = checked(index + (value - self.digit(index, site)) * self.stride(site))
        return index


@dataclass(frozen=True, slots=True)
class LocalChannel:
    """Unobserved trace-preserving local operation: no outcome is sampled."""

    kraus: tuple[Matrix, ...]

    def __post_init__(self) -> None:
        common_scale(self.kraus)
        if len(self.kraus) > 4 or len(self.kraus[0]) > 4:
            raise ValueError("channel requires at most four Kraus matrices on one register")


@dataclass(frozen=True, slots=True)
class GroupedInstrument:
    """Observed outcomes may each retain several indistinguishable Kraus terms.

    The group is an incoherent sum, NOT a coherent sum of matrices and NOT a
    second random draw of a hidden Kraus label. All matrices share one scale.
    """

    outcomes: tuple[tuple[Matrix, ...], ...]

    def __post_init__(self) -> None:
        if type(self.outcomes) is not tuple or not 1 <= len(self.outcomes) <= 4:
            raise ValueError("one to four immutable outcome groups required")
        for group in self.outcomes:
            if type(group) is not tuple or not 1 <= len(group) <= 4:
                raise ValueError("one to four immutable Kraus matrices per outcome required")
        matrices = tuple(m for group in self.outcomes for m in group)
        common_scale(matrices)
        if len(matrices[0]) > 4:
            raise ValueError("grouped instrument acts on one register")


def outcome_groups(instrument: LocalInstrument | GroupedInstrument) -> tuple[tuple[Matrix, ...], ...]:
    return (
        instrument.outcomes
        if isinstance(instrument, GroupedInstrument)
        else tuple((matrix,) for matrix in instrument.branches)
    )
