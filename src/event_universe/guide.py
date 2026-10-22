"""The guide clause of the emission (ALGEBRA.md, The click writes on the lattice (5), BUILT 2026-10-22; the reader's derivation of the box's 0.09 and his design read): a source in time at one Node lays the form S it writes, and the law's line reads S on the guide of width one, where the four folded reads fall on the Node and two Ports stay open, den cos k = 3 num - 2 den and S = (2 / 3) T sin k, one quantum in the two outgoing waves (`emission.radiated_total`). On a board whose cross-section is wider the guide is its longest axis and the two other axes are its cross-section; each transverse axis carries modes with a cosine c_m and a weight at the Node: an axis of one layer the one uniform mode, c = 1 and the weight 1 (the chain); an axis of w layers with faces, closed or open, the fill 0 beyond either, the modes sin(pi m (y + 1) / (w + 1)), m = 1 .. w, with c_m = cos(pi m / (w + 1)) and the weight 2 sin^2(pi m (y0 + 1) / (w + 1)) / (w + 1) at the Node's coordinate y0; a periodic axis of w layers the modes cos(2 pi m y / w), c_m = cos(2 pi m / w), the weight 1 / w. The guide's wave of the mode (m, n) at the resonance has den cos k_mn = 3 num - den c_m - den c_n; the mode travels where |den cos k_mn| < den and stands at the Node otherwise. A point source's share into a travelling mode is its weight at the Node over sin k_mn, so the share of the width-one S that travels is R = SUM over the travelling modes of weight_m weight_n sin k / sin k_mn, sin k the width-one guide's, and the clause lays S / R, one quantum travelling in the travelling modes (on the box of 61 x 7 x 7 at the resonance [5414, 6000] the mode (1, 1) alone travels, the weight 1 / 16 at the centre, R = 0.0864 and the factor 11.58). Integers alone, by the acts table's acts: the transverse cosines by the half-angle chain of searches, den cos(theta / 2) the largest integer whose square is at most den (den + den cos theta) div 2, from den cos(pi / 2) = 0 down to pi / (w + 1) where w + 1 is a power of two, and the multiples cos(m theta) by the angle-sum's recurrence on the integer pairs, one division act each; den sin by the search on den^2 - (den cos)^2; R as one rational, S / R by one division act whose remainder is discarded as the root of S discards its own; a width whose cosines the table's acts do not reach (w + 1 no power of two) keeps the width-one line, named here (`base_cosine` answers None and `guide_total` returns S), so the worlds laid before this clause load and run as they did; a board whose modes are reached and none of them travels at the resonance is refused by name at load (`loader/world.py`, a one-Node body with a declared rate) and again in the clause. On the width-one guide R is 1 exactly and S stands as the line has it, bit for bit."""

from __future__ import annotations

from event_universe.core.ports import PORTS, SIDES
from event_universe.core.rule3 import division_forward, largest_below

Shape = tuple[int, int, int]


def half_angle(den: int, cosine: int) -> int:
    """den cos(theta / 2) from den cos theta: the largest integer whose square is at most den (den + den cos theta) div 2 (one division, one search)."""
    return largest_below(int(division_forward(den * (den + cosine), SIDES, 0)[0]))


def base_cosine(den: int, layers: int) -> int | None:
    """den cos(pi / (w + 1)) for a faced axis of w layers by the half-angle chain from den cos(pi / 2) = 0, where w + 1 is a power of two; None where it is not (the path's cosines are then roots the table's acts do not reach, and the width-one line stands as before, named)."""
    size, steps = SIDES, 0
    while size < layers + 1:
        size, steps = size * SIDES, steps + 1
    if size != layers + 1:
        return None
    cosine = 0  # den cos(pi / 2)
    for _ in range(steps):
        cosine = half_angle(den, cosine)
    return cosine


def multiples(den: int, cosine: int, count: int) -> list[int]:
    """den cos(m theta) for m = 0 .. count from den cos theta by the angle-sum's recurrence on the integer pairs, cos((m + 1) theta) = 2 cos theta cos(m theta) - cos((m - 1) theta), one division act each."""
    found = [den, cosine]
    while len(found) <= count:
        found.append(int(division_forward(SIDES * cosine * found[-1], den, 0)[0]) - found[-2])
    return found[: count + 1]


def sine_of(den: int, cosine: int) -> int:
    """den sin from den cos by the search on den^2 - (den cos)^2, 0 where the cosine stands on or outside the circle."""
    square = den * den - cosine * cosine
    return largest_below(square) if square > 0 else 0


def modes_of(den: int, layers: int, periodic: bool, at: int) -> list[tuple[int, int, int, int]] | None:
    """A transverse axis's modes as (the mode's label, den c_m, the weight's numerator, the weight's denominator) at the Node's coordinate `at`: one layer the uniform mode (0, den, 1, 1); a faced axis of w layers the sines' modes m = 1 .. w with the weight 2 sin^2(pi m (at + 1) / (w + 1)) / (w + 1); a periodic axis of w layers the cosines' modes m = 0 .. w - 1 with the weight 1 / w; None where the width's cosines are out of the table's reach."""
    if layers == 1:
        return [(0, den, 1, 1)]
    if periodic:
        base = (
            base_cosine(den, layers // SIDES - 1) if layers % SIDES == 0 else None
        )  # cos(2 pi / w) = cos(pi / (w / 2))
        if base is None:
            return None
        cosines = multiples(den, base, layers)
        return [(m, cosines[m], 1, layers) for m in range(layers)]
    base = base_cosine(den, layers)
    if base is None:
        return None
    cosines = multiples(den, base, layers)
    angle = multiples(den, base, at + 1)[at + 1]  # den cos((at + 1) pi / (w + 1)), the Node's own angle
    at_node = multiples(den, angle, layers)  # den cos(m (at + 1) pi / (w + 1)) for m = 0 .. w
    found = []
    for m in range(1, layers + 1):
        sine = sine_of(den, at_node[m])
        found.append((m, cosines[m], SIDES * sine * sine, (layers + 1) * den * den))
    return found


def travelling(
    shape: Shape, periodic: tuple[bool, bool, bool], node: Shape, resonance: tuple[int, int]
) -> tuple[list[tuple[int, int]], int, int] | None:
    """The guide's travelling modes at the resonance and the share R of the width-one S they carry, as the rational (numerator, denominator): the guide the board's longest axis (the first of equals), the cross-section the two others; den cos k_mn = 3 num - den c_m - den c_n, travelling where |den cos k_mn| < den; R = SUM weight_m weight_n sin k / sin k_mn with sin k the width-one guide's; None where a transverse width's cosines are out of the table's reach."""
    num, den = resonance
    axis = max(range(len(shape)), key=lambda a: shape[a])
    across = [a for a in range(len(shape)) if a != axis]
    sides = [modes_of(den, shape[a], periodic[a], node[a]) for a in across]
    if sides[0] is None or sides[1] is None:
        return None
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
    """S laid on the guide: the width-one S over R by one division act, the remainder discarded; S itself where R is 1 (the width-one guide, bit for bit) and where the cross-section's cosines are out of the table's reach (the width-one line as before, named); refused by name where the modes are reached and none travels."""
    read = travelling(shape, periodic, node, resonance)
    if read is None:
        return total
    modes, numerator, denominator = read
    if not modes or numerator == 0:
        raise ValueError(
            f"no mode of the guide travels at the resonance {list(resonance)} on the board {list(shape)}: the emission "
            "lays nothing that leaves (the guide clause, ALGEBRA.md (5))"
        )
    if numerator == denominator:
        return total
    return int(division_forward(total * denominator, numerator, 0)[0])
