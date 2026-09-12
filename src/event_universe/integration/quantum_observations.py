"""Read-only exact host diagnostics; never inputs to physical scheduling."""

from fractions import Fraction

from event_universe.quantum.event_rules import State, squared_norm
from event_universe.quantum.mode_rules import occupation_totals


def rational(value: Fraction) -> dict[str, int]:
    return {"numerator": value.numerator, "denominator": value.denominator}


def reduced_state(state: State, sites: tuple[int, ...]) -> dict[str, object]:
    """Trace all other modes, preserving complex off-diagonal elements.

    Sparse pairs avoid assuming fixed excitation number or real amplitudes.
    Normalization is a diagnostic rational number, not an evolving register.
    """
    mask = sum(1 << q for q in sites)
    norm = squared_norm(state)
    entries: dict[tuple[int, int], tuple[int, int]] = {}
    environments: dict[int, list[tuple[int, int, int]]] = {}
    for bits, amp in state:
        local = sum(((bits >> q) & 1) << j for j, q in enumerate(sites))
        environments.setdefault(bits & ~mask, []).append((local, amp.real, amp.imag))
    for terms in environments.values():
        for row, ar, ai in terms:
            for column, br, bi in terms:
                real, imag = entries.get((row, column), (0, 0))
                entries[row, column] = (real + ar * br + ai * bi, imag + ai * br - ar * bi)
    purity = Fraction(0)
    off_diagonal = Fraction(0)
    elements = []
    for (row, column), (real, imag) in sorted(entries.items()):
        if real or imag:
            elements.append(
                {
                    "row": row,
                    "column": column,
                    "real": rational(Fraction(real, norm)),
                    "imaginary": rational(Fraction(imag, norm)),
                }
            )
        weight = Fraction(real * real + imag * imag, norm * norm)
        purity += weight
        if row != column:
            off_diagonal += weight
    return {
        "elements": elements,
        "purity": rational(purity),
        "off_diagonal_squared": rational(off_diagonal),
    }


def sector_distribution(
    state: State, quantities: tuple[tuple[int, ...], ...]
) -> list[dict[str, object]]:
    weights: dict[tuple[int, ...], int] = {}
    for bits, amp in state:
        totals = occupation_totals(bits, quantities)
        weights[totals] = weights.get(totals, 0) + amp.real * amp.real + amp.imag * amp.imag
    norm = squared_norm(state)
    return [
        {"values": totals, "probability": rational(Fraction(weight, norm))}
        for totals, weight in sorted(weights.items())
    ]


def occupation_probability(state: State, site: int) -> Fraction:
    return Fraction(
        sum(a.real * a.real + a.imag * a.imag for bits, a in state if bits & (1 << site)),
        squared_norm(state),
    )
