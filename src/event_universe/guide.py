"""The guide clause of the emission (ALGEBRA.md, The click writes on the lattice (5), BUILT 2026-10-22; the reader's derivation of the box's 0.09 and his design read): a source in time at one Node lays the form S it writes, and the law's line reads S on the guide of width one, where the four folded reads fall on the Node and two Ports stay open, den cos k = 3 num - 2 den and S = (2 / 3) T sin k, one quantum in the two outgoing waves (`emission.radiated_total`). On a board whose cross-section is wider the guide is its longest axis and the two other axes are its cross-section; each transverse axis carries modes with a cosine c_m and a weight at the Node: an axis of one layer the one uniform mode, c = 1 and the weight 1 (the chain); an axis of w layers with faces, closed or open, the fill 0 beyond either, the modes sin(pi m (y + 1) / (w + 1)), m = 1 .. w, with c_m = cos(pi m / (w + 1)) and the weight 2 sin^2(pi m (y0 + 1) / (w + 1)) / (w + 1) at the Node's coordinate y0; a periodic axis of w layers the modes cos(2 pi m y / w), c_m = cos(2 pi m / w), the weight 1 / w. The guide's wave of the mode (m, n) at the resonance has den cos k_mn = 3 num - den c_m - den c_n; the mode travels where |den cos k_mn| < den and stands at the Node otherwise. A point source's share into a travelling mode is its weight at the Node over sin k_mn, so the share of the width-one S that travels is R = SUM over the travelling modes of weight_m weight_n sin k / sin k_mn, sin k the width-one guide's, and the clause lays S / R, one quantum travelling in the travelling modes (on the box of 61 x 7 x 7 at the resonance [5414, 6000] the mode (1, 1) alone travels, the weight 1 / 16 at the centre exactly, R = 0.08663 and the factor 11.543). Integers alone, by the acts table's acts: every cosine the engine's own cosine of a wave number, `features/click.wave_cosine`, the rotation act's search for den cos(pi t / h) at any t and h (the reader's line of 2026-10-22: one way for the cosines in the engine, the packet's transverse mode's and the clause's alike, no second chain; the half-angle chain of searches with the angle-sum's recurrence, the first build of this day, is withdrawn, its multiples drifting by the recurrence's roundings, den cos(4 pi / 8) at -7 for 0); den sin by the search on den^2 - (den cos)^2; R as one rational, S / R by one division act whose remainder is discarded as the root of S discards its own; every width reached; where no mode travels at the resonance, or the source stands at every travelling mode's zero, the clause has nothing to scale and S stands as the width-one line has it, the near zone's lay (`guide_total`), no refusal. On the width-one guide R is 1 exactly and S stands as the line has it, bit for bit."""

from __future__ import annotations

from event_universe.core.ports import PORTS, SIDES
from event_universe.core.rule3 import division_forward, largest_below
from event_universe.features.click import wave_cosine

Shape = tuple[
    int, ...
]  # the board's shape and a Node's coordinates, three integers each, as the board hands them


def sine_of(den: int, cosine: int) -> int:
    """den sin from den cos by the search: the largest integer whose square is at most den^2 - (den cos)^2, 0 where none is."""
    square = den * den - cosine * cosine
    return largest_below(square) if square > 0 else 0


def modes_of(den: int, layers: int, periodic: bool, at: int) -> list[tuple[int, int, int, int]]:
    """A transverse axis's modes as (the mode's label, den c_m, the weight's numerator, the weight's denominator) at the Node's coordinate `at`: one layer the uniform mode (0, den, 1, 1); a faced axis of w layers the sines' modes m = 1 .. w, den c_m = wave_cosine(m, w + 1, den) and the weight 2 sin^2(pi m (at + 1) / (w + 1)) / (w + 1) with the Node's angle den cos(pi m (at + 1) / (w + 1)) = wave_cosine(m (at + 1), w + 1, den) and its sine by the search; a periodic axis of w layers the cosines' modes m = 0 .. w - 1, den c_m = wave_cosine(2 m, w, den), the weight 1 / w; every cosine the engine's own (the reader's line of 2026-10-22)."""
    if layers == 1:
        return [(0, den, 1, 1)]
    if periodic:
        return [(m, wave_cosine(SIDES * m, layers, den), 1, layers) for m in range(layers)]
    found = []
    for m in range(1, layers + 1):
        sine = sine_of(den, wave_cosine(m * (at + 1), layers + 1, den))
        found.append((m, wave_cosine(m, layers + 1, den), SIDES * sine * sine, (layers + 1) * den * den))
    return found


def travelling(
    shape: Shape, periodic: tuple[bool, bool, bool], node: Shape, resonance: tuple[int, int]
) -> tuple[list[tuple[int, int]], int, int]:
    """The guide's travelling modes at the resonance and the share R of the width-one S they carry, as the rational (numerator, denominator): the guide the board's longest axis (the first of equals), the cross-section the two others; den cos k_mn = 3 num - den c_m - den c_n, travelling where |den cos k_mn| < den; R = SUM weight_m weight_n sin k / sin k_mn with sin k the width-one guide's; None where a transverse width's cosines are out of the table's reach."""
    num, den = resonance
    axis = max(range(len(shape)), key=lambda a: shape[a])
    across = [a for a in range(len(shape)) if a != axis]
    sides = [modes_of(den, shape[a], periodic[a], node[a]) for a in across]
    guide = int(
        division_forward(PORTS * num - (PORTS - SIDES) * den, SIDES, 0)[0]
    )  # den cos k on the width-one guide
    sine = sine_of(den, guide)
    found: list[tuple[int, int]] = []
    numerator, denominator = 0, 1
    for m, c_m, w_m, d_m in sides[0]:
        for n, c_n, w_n, d_n in sides[1]:
            cosine = 3 * num - c_m - c_n
            if -den < cosine < den:
                found.append((m, n))
                t_num, t_den = w_m * w_n * sine, d_m * d_n * sine_of(den, cosine)
                numerator, denominator = numerator * t_den + t_num * denominator, denominator * t_den
    return found, numerator, denominator


def guide_total(
    total: int, shape: Shape, periodic: tuple[bool, bool, bool], node: Shape, resonance: tuple[int, int]
) -> int:
    """S laid on the guide: the width-one S over R by one division act, the remainder discarded; S itself where R is 1 (the width-one guide, bit for bit) and where the cross-section's cosines are out of the table's reach (the width-one line as before, named); refused by name where the modes are reached and none travels. Where the clause's sum is empty, no mode travelling at the resonance, or the source stands at every travelling mode's zero (its weight 0 in each, the share's numerator 0), S stands as the width-one line has it, the near zone's lay, named (the owner's word of 2026-10-22, tests only: the conserve worlds' giver on its 5 x 5 cross-section at [5751, 6000], den cos k_11 = 6865 above den, loads and runs bit for bit as shipped, its taker clicking in the near zone); no refusal."""
    read = travelling(shape, periodic, node, resonance)
    modes, numerator, denominator = read
    if not modes or numerator == 0:
        return total  # no mode travels, or the source stands at every travelling mode's zero: S stands, the near zone's lay
    if numerator == denominator:
        return total
    return int(division_forward(total * denominator, numerator, 0)[0])
