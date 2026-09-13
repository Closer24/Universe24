"""Bounded local amplitude transport and finite probability-weighted sources.

Only frozen local inputs belong here. Matrix normalization removes the common
vacuum phase; no conditional quantum query or global normalization is performed.
"""

from event_universe.core.disturbance_state import (
    MAX_COMPONENTS,
    CostMeter,
    FieldDefinition,
    OperationCosts,
    Payload,
    bounded,
    pack,
    unpack,
)
from event_universe.core.integer import checked_work, signed_divrem
from event_universe.core.source_envelope_state import EnvelopeAmplitude, EnvelopeRemainder
from event_universe.core.state import bounded_gcd

from .spatial import bounded_emission_amount

Matrix = tuple[tuple[tuple[int, int], ...], ...]
ComplexRatio = tuple[int, int, int]


def _gcd(a: int, b: int, meter: CostMeter) -> int:
    # One configured evaluation tariff for the bounded integer primitive.
    meter.charge("evaluate")
    return bounded_gcd(a, b)


def _ratio(n: int, d: int, meter: CostMeter) -> tuple[int, int]:
    checked_work(n)
    if checked_work(d) < 1:
        raise ValueError("source ratio denominator must be positive")
    factor = _gcd(n, d, meter)
    return n // factor, d // factor


def _parts(real: int, imag: int, denominator: int, meter: CostMeter) -> ComplexRatio:
    checked_work(real)
    checked_work(imag)
    if checked_work(denominator) < 1:
        raise ValueError("source amplitude denominator must be positive")
    factor = _gcd(_gcd(real, imag, meter), denominator, meter)
    return real // factor, imag // factor, denominator // factor


def validate_amplitude(value: EnvelopeAmplitude) -> None:
    """Require bounded local probability at most one; do not renormalize it."""
    if type(value) is not EnvelopeAmplitude:
        raise TypeError("an immutable source amplitude is required")
    real, imag, denominator = bounded(value.real), bounded(value.imag), bounded(value.denominator)
    if denominator < 1:
        raise ValueError("source amplitude denominator must be positive")
    norm = checked_work(checked_work(real * real) + checked_work(imag * imag))
    if norm > checked_work(denominator * denominator):
        raise ValueError("local source probability exceeds one")


def reduce_amplitude(real: int, imag: int, denominator: int, meter: CostMeter) -> EnvelopeAmplitude:
    """Reduce an exact ratio before enforcing the fixed stored-register bounds."""
    value = EnvelopeAmplitude(*_parts(real, imag, denominator, meter))
    validate_amplitude(value)
    meter.charge("update", 3)
    return value


def _multiply(a: ComplexRatio, b: ComplexRatio, meter: CostMeter) -> ComplexRatio:
    ar, ai, ad = a
    br, bi, bd = b
    factor = _gcd(_gcd(ar, ai, meter), bd, meter)
    ar, ai, bd = ar // factor, ai // factor, bd // factor
    factor = _gcd(_gcd(br, bi, meter), ad, meter)
    br, bi, ad = br // factor, bi // factor, ad // factor
    meter.charge("evaluate", 6)
    real = checked_work(checked_work(ar * br) - checked_work(ai * bi))
    imag = checked_work(checked_work(ar * bi) + checked_work(ai * br))
    return _parts(real, imag, checked_work(ad * bd), meter)


def _add(a: ComplexRatio, b: ComplexRatio, meter: CostMeter) -> ComplexRatio:
    ar, ai, ad = a
    br, bi, bd = b
    factor = _gcd(ad, bd, meter)
    am, bm = bd // factor, ad // factor
    meter.charge("evaluate", 6)
    return _parts(
        checked_work(checked_work(ar * am) + checked_work(br * bm)),
        checked_work(checked_work(ai * am) + checked_work(bi * bm)),
        checked_work(ad * am),
        meter,
    )


def local_output(
    matrix: Matrix,
    inputs: tuple[EnvelopeAmplitude, ...],
    output_index: int,
    meter: CostMeter,
) -> EnvelopeAmplitude:
    """Compute one endpoint from its frozen input and delivered neighbor input.

    Initialization validates unitarity. One or two binary modes require a 2x2
    or 4x4 number-preserving matrix. Register zero is basis state one; register
    one is basis state two. Dividing by the vacuum coefficient removes only its
    common phase and the common implicit scale, including a complex vacuum.
    """
    if type(inputs) is not tuple or len(inputs) not in (1, 2):
        raise ValueError("one or two local source inputs are required")
    if type(output_index) is not int or not 0 <= output_index < len(inputs):
        raise ValueError("source output index is outside the local mode group")
    size = 1 << len(inputs)
    if type(matrix) is not tuple or len(matrix) != size:
        raise ValueError("source matrix size differs from its mode count")
    occupations = (0, 1) if size == 2 else (0, 1, 1, 2)
    for i, row in enumerate(matrix):
        if type(row) is not tuple or len(row) != size:
            raise ValueError("source matrix must be immutable and square")
        for j, coefficient in enumerate(row):
            if type(coefficient) is not tuple or len(coefficient) != 2:
                raise ValueError("source matrix requires integer complex pairs")
            real, imag = coefficient
            checked_work(real)
            checked_work(imag)
            if occupations[i] != occupations[j] and (real or imag):
                raise ValueError("source matrix must preserve occupation")
    vr, vi = matrix[0][0]
    vacuum_norm = checked_work(checked_work(vr * vr) + checked_work(vi * vi))
    if not vacuum_norm:
        raise ValueError("source matrix vacuum coefficient must be nonzero")
    meter.charge("read", size * size + len(inputs))
    meter.charge("evaluate", 3)
    total: ComplexRatio = (0, 0, 1)
    for j, value in enumerate(inputs):
        validate_amplitude(value)
        real, imag = matrix[1 << output_index][1 << j]
        meter.charge("evaluate", 6)
        relative = _parts(
            checked_work(checked_work(real * vr) + checked_work(imag * vi)),
            checked_work(checked_work(imag * vr) - checked_work(real * vi)),
            vacuum_norm,
            meter,
        )
        total = _add(
            total, _multiply(relative, (value.real, value.imag, value.denominator), meter), meter
        )
    return reduce_amplitude(*total, meter)


def output_cost(matrix: Matrix, costs: OperationCosts) -> int:
    """Reserve the exact fixed primitive tariff for one local matrix output.

    Each bounded Euclid invocation has one evaluate tariff. The number of these
    primitives and all other charged operations depends only on matrix size,
    never on amplitudes or early termination inside the integer primitive.
    """
    if len(matrix) not in (2, 4):
        raise ValueError("source matrix requires one or two binary modes")
    meter = CostMeter(costs)
    local_output(matrix, (EnvelopeAmplitude(),) * (1 if len(matrix) == 2 else 2), 0, meter)
    return meter.total


def squared_weight(value: EnvelopeAmplitude, meter: CostMeter) -> tuple[int, int]:
    """Return the exact reduced local probability with 64-bit intermediates."""
    validate_amplitude(value)
    meter.charge("read", 3)
    meter.charge("evaluate", 3)
    return _ratio(
        checked_work(checked_work(value.real * value.real) + checked_work(value.imag * value.imag)),
        checked_work(value.denominator * value.denominator),
        meter,
    )


def weighted_emission(
    full_numerator: tuple[int, ...],
    full_denominator: int,
    amplitude: EnvelopeAmplitude,
    residuals: tuple[EnvelopeRemainder, ...],
    remaining: Payload,
    field: FieldDefinition,
    meter: CostMeter,
) -> tuple[Payload, tuple[EnvelopeRemainder, ...], Payload]:
    """Emit full strength times local weight, preserving changing-denominator residue.

    The absolute finite allowance is consumed by the existing generic primitive.
    Exhaustion discards un-emitted demand, including the fractional remainder;
    clipped demand is not a debt. Returned values are a single immutable proposal.
    """
    if bounded(full_denominator) < 1:
        raise ValueError("full source denominator must be positive")
    if not 1 <= field.components <= MAX_COMPONENTS or any(
        len(values) != field.components for values in (full_numerator, residuals, remaining)
    ):
        raise ValueError("weighted source component count differs from the field")
    weight_n, weight_d = squared_weight(amplitude, meter)
    quotients = []
    fractions = []
    for full, old in zip(full_numerator, residuals, strict=True):
        checked_work(full)
        if type(old) is not EnvelopeRemainder:
            raise TypeError("immutable source remainders are required")
        # Cross-cancel before multiplication; all actual intermediates still fit.
        first = _gcd(full, weight_d, meter)
        second = _gcd(weight_n, full_denominator, meter)
        numerator, denominator = _ratio(
            checked_work((full // first) * (weight_n // second)),
            checked_work((full_denominator // second) * (weight_d // first)),
            meter,
        )
        factor = _gcd(denominator, old.denominator, meter)
        left, right = old.denominator // factor, denominator // factor
        total = checked_work(checked_work(numerator * left) + checked_work(old.numerator * right))
        denominator = checked_work(denominator * left)
        whole, fraction = signed_divrem(total, denominator)
        quotients.append(whole)
        fractions.append(_ratio(fraction, denominator, meter))
        meter.charge("evaluate", 6)
    zero = pack((0,) * field.components)
    amount, _, after = bounded_emission_amount(tuple(quotients), zero, 1, remaining, field, meter)
    remainders = tuple(
        EnvelopeRemainder(*fraction) if allowance else EnvelopeRemainder()
        for fraction, allowance in zip(fractions, unpack(after), strict=True)
    )
    meter.charge("update", 2 * field.components)
    return amount, remainders, after
