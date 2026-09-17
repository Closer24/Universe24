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
from event_universe.core.integer import bounded_gcd, checked_work, signed_divrem
from event_universe.core.source_envelope_state import (
    EnvelopeAmplitude,
    EnvelopeRemainder,
    EnvelopeScale,
    NullRecord,
)

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


def scaled_weight(
    amplitude: EnvelopeAmplitude, scale: EnvelopeScale | None, meter: CostMeter
) -> tuple[int, int]:
    """Local squared weight times the delivered null-notice scale, clipped at one.

    The clip is explicit: notices from nulls that were decided before an
    earlier notice reached the deciding Node can overshoot. The Node never
    emits above its full configured strength.
    """
    weight_n, weight_d = squared_weight(amplitude, meter)
    if scale is None or (scale.numerator == scale.denominator):
        return weight_n, weight_d
    if type(scale) is not EnvelopeScale:
        raise TypeError("an immutable source weight scale is required")
    meter.charge("evaluate", 3)
    first = _gcd(weight_n, scale.denominator, meter)
    second = _gcd(scale.numerator, weight_d, meter)
    numerator, denominator = _ratio(
        checked_work((weight_n // first) * (scale.numerator // second)),
        checked_work((weight_d // second) * (scale.denominator // first)),
        meter,
    )
    if numerator > denominator:
        return 1, 1
    return numerator, denominator


def null_factor(
    amplitude: EnvelopeAmplitude, scale: EnvelopeScale, meter: CostMeter
) -> tuple[int, int] | None:
    """The conditional renormalization factor 1 / (1 - p) from this Node's own weight.

    ``p`` is the Node's scaled local weight before the null. A weight of one
    admits no null; the caller then sends no notice. The factor is exact and
    rational; it multiplies squared weights, so no square root is needed.
    """
    numerator, denominator = scaled_weight(amplitude, scale, meter)
    remaining = checked_work(denominator - numerator)
    if remaining <= 0:
        return None
    meter.charge("evaluate", 2)
    return _ratio(denominator, remaining, meter)


def null_correction(
    record: NullRecord, delivered: tuple[int, int], meter: CostMeter
) -> tuple[tuple[int, int], tuple[int, int]] | None:
    """Correct a null factor sent before an earlier-ordered notice arrived.

    The Node sent ``1 / (1 - w s_old)`` from its unscaled weight ``w`` and the
    scale ``s_old`` it held at the null. The delivered factor ``g`` from a null
    ordered before its own makes the exact prior scale ``s_new = s_old g``, so
    the factor should have been ``1 / (1 - w s_new)``. The correction is the
    quotient ``(1 - w s_old) / (1 - w s_new)``, a rational of at least one, and
    ``s_new`` becomes the assumed scale for later corrections; a chain of
    corrections telescopes. Returns nothing when the corrected weight would
    reach one, which no null decided by the quantum owner can produce.
    """
    if type(record) is not NullRecord:
        raise TypeError("a null correction requires the Node's own null record")
    if bounded(delivered[1]) < 1 or bounded(delivered[0]) < delivered[1]:
        raise ValueError("a delivered null factor must be a rational of at least one")
    meter.charge("read", 3)
    meter.charge("evaluate", 4)
    new_n, new_d = _ratio(
        checked_work(record.scale_numerator * delivered[0]),
        checked_work(record.scale_denominator * delivered[1]),
        meter,
    )
    old_remaining = checked_work(
        checked_work(record.weight_denominator * record.scale_denominator)
        - checked_work(record.weight_numerator * record.scale_numerator)
    )
    new_remaining = checked_work(
        checked_work(record.weight_denominator * new_d) - checked_work(record.weight_numerator * new_n)
    )
    if old_remaining <= 0 or new_remaining <= 0:
        return None
    correction = _ratio(
        checked_work(old_remaining * new_d),
        checked_work(new_remaining * record.scale_denominator),
        meter,
    )
    return correction, (new_n, new_d)


def weighted_emission(
    full_numerator: tuple[int, ...],
    full_denominator: int,
    amplitude: EnvelopeAmplitude,
    residuals: tuple[EnvelopeRemainder, ...],
    remaining: Payload,
    field: FieldDefinition,
    meter: CostMeter,
    scale: EnvelopeScale | None = None,
) -> tuple[Payload, tuple[EnvelopeRemainder, ...], Payload]:
    """Emit full strength times local weight, preserving changing-denominator residue.

    The absolute finite allowance is consumed by the existing generic primitive.
    Exhaustion discards un-emitted demand, including the fractional remainder;
    clipped demand is not a debt. Returned values are a single immutable proposal.
    An optional delivered scale multiplies the weight before emission.
    """
    if bounded(full_denominator) < 1:
        raise ValueError("full source denominator must be positive")
    if not 1 <= field.components <= MAX_COMPONENTS or any(
        len(values) != field.components for values in (full_numerator, residuals, remaining)
    ):
        raise ValueError("weighted source component count differs from the field")
    weight_n, weight_d = scaled_weight(amplitude, scale, meter)
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
