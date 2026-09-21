"""The birth wheel: the bit-reversed ordinal against the golden rate
(read-only, the mathematician, 2026-09-20; TWO_SLITS.md section 8). Two
wheels of W = 4096 for the click's u: `bitreverse_12(ordinal mod W)` (the
van der Corput sequence) and `(ordinal x 2531) mod W` (the Weyl sequence
at the golden ratio conjugate, r / W = 0.6179; 2531 is odd, so coprime to
W), the second being the counts' one mechanism (acc += r; e = [acc >= W];
acc -= e W) with the accumulator itself as u. The three cases of
TWO_SLITS.md section 4 (the registered fan of 91; the screen's fan with
the wheel alone; the screen's fan with the wheel and the exact phase) at
256 and 4096 births: the empty cells per prefix, the bright and dark
counts, the Pearson with the Euclidean cosine, the visibility, and the
worst prefix discrepancy max_j |count_j - B x weight_j / total| at B =
4096. The rows' birth phase stays the lamp's clock (ordinal mod 64) on
both wheels; the wheel changes only the ladder's u.

Run from the repository root with PYTHONPATH=src:

    python docs/designs/fraction_free/wheel_map.py > docs/designs/fraction_free/wheel_map.out
"""

from __future__ import annotations

import math
from fractions import Fraction

from two_slits_map import (
    COS,
    HEIGHT,
    LAMP,
    LAMP_DIRECTIONS,
    OPENINGS,
    PHASE_PER_LINK,
    SCREEN_X,
    SIN,
    N,
    bit_reverse,
    choose,
    exact_phase,
    pearson,
    phase_by_clock,
    resolution,
    rungs,
    stop_fan,
    stop_lamp,
    walk,
)

W = 4096
GOLDEN = 2531
PREFIXES = (64, 256, 1024, 4096)


def cosine(y: int) -> float:
    wavelength = 8 * 64 / 110
    r1 = math.hypot(SCREEN_X - OPENINGS[0][0], y - OPENINGS[0][1])
    r2 = math.hypot(SCREEN_X - OPENINGS[1][0], y - OPENINGS[1][1])
    return 1 + math.cos(2 * math.pi * (r1 - r2) / wavelength)


def build(fan_of_screen: bool):
    """The record's sets: name -> {node: [(built phase, exact phase)]}
    with the multiplicity per set; the registered fan of 91 or the
    screen's fan of one direction per pixel from each opening."""
    n, d = PHASE_PER_LINK
    sets: dict[str, dict[tuple[int, int], list[tuple[int, Fraction]]]] = {}
    mult: dict[str, int] = {}
    lamp_rows = [(v, *walk(LAMP, v, stop_lamp)) for v in LAMP_DIRECTIONS]
    leg = {}
    leg_exact = {}
    for v, end, node, age, made in lamp_rows:
        s1, t = sum(map(abs, v)), resolution(v)
        if end == "wall":
            name = f"wall {node}"
            sets.setdefault(name, {}).setdefault(node, []).append(
                (phase_by_clock(age, n, d), exact_phase(made, s1, t, n, d) % N)
            )
            mult[name] = 5
        else:
            leg[node] = phase_by_clock(age, n, d)
            leg_exact[node] = exact_phase(made, s1, t, n, d)
    if fan_of_screen:
        fans = {o: [(SCREEN_X - o[0], y - o[1]) for y in range(HEIGHT)] for o in OPENINGS}
    else:
        fan = [(1, 0)] + [
            (a, b)
            for a in range(1, 12)
            for b in range(-11, 12)
            if b and a + abs(b) <= 12 and math.gcd(a, b) == 1
        ]
        fans = {o: fan for o in OPENINGS}
    ways = len(fans[OPENINGS[0]])
    for opening in OPENINGS:
        for v in fans[opening]:
            end, node, age, made = walk(opening, v, stop_fan)
            s1, t = sum(map(abs, v)), resolution(v)
            built = (leg[opening] + phase_by_clock(age, n, d)) % N
            exact = (leg_exact[opening] + exact_phase(made, s1, t, n, d)) % N
            if end == "screen":
                name = f"screen_{node[1]}"
            else:
                name = "face +y" if node[1] >= HEIGHT else "face -y"
            sets.setdefault(name, {}).setdefault(node, []).append((built, exact))
            mult[name] = 5 * ways
    order = (
        [k for k in sets if k.startswith("wall")]
        + [f"screen_{y}" for y in range(HEIGHT)]
        + [k for k in ("face +y", "face -y") if k in sets]
    )
    return sets, mult, order


def cell_weights(sets, mult, order, u: int, exact: bool) -> list[Fraction]:
    found = []
    for name in order:
        total = Fraction(0)
        for rows in sets.get(name, {}).values():
            if exact:
                z = 0j
                for _, ph in rows:
                    p = math.floor((ph + u) * 4096 / N) % 4096
                    z += complex(math.cos(2 * math.pi * p / 4096), math.sin(2 * math.pi * p / 4096))
                total += Fraction(round(abs(z) ** 2 * 65536)) / (65536 * mult[name])
            else:
                x = sum(COS[(ph + u) % N] for ph, _ in rows)
                s = sum(SIN[(ph + u) % N] for ph, _ in rows)
                total += Fraction(x * x + s * s, 65536 * mult[name])
        found.append(total)
    return found


def ladders(sets, mult, order, exact: bool):
    """The rungs at W for each of the 64 birth phases, and the weights."""
    found = {}
    for u in range(N):
        weights = cell_weights(sets, mult, order, u, exact)
        common = 1
        for w in weights:
            common = common * w.denominator // math.gcd(common, w.denominator)
        found[u] = (rungs([int(w * common) for w in weights], W), weights)
    return found


def wheel_index(birth: int, golden: bool) -> int:
    return (birth * GOLDEN) % W if golden else bit_reverse(birth % W, 12)


def main() -> None:
    cos = [cosine(y) for y in range(HEIGHT)]
    bright = [y for y in range(HEIGHT) if cos[y] > 1.9]
    dark = [y for y in range(HEIGHT) if cos[y] < 0.1]
    print(
        f"W = {W}; the golden rate {GOLDEN} / {W} = {GOLDEN / W:.4f}; the bright pixels {bright}; the dark {dark}"
    )
    cases = (
        ("the registered fan of 91, the built phase", False, False),
        ("the screen's fan, the built phase (the wheel alone)", True, False),
        ("the screen's fan, the exact phase (the wheel and the exact phase)", True, True),
    )
    for title, of_screen, exact in cases:
        sets, mult, order = build(of_screen)
        table = ladders(sets, mult, order, exact)
        weights0 = table[0][1]
        total0 = sum(weights0)
        cells_with_weight = sum(1 for w in weights0 if w)
        print(f"\n== {title}: {len(order)} cells, {cells_with_weight} with weight")
        for golden in (False, True):
            name = "golden" if golden else "bit-reversed"
            counts = [0] * len(order)
            empty_by_prefix = []
            worst = 0.0
            for birth in range(max(PREFIXES)):
                u_phase = birth % N
                found, weights = table[u_phase]
                counts[choose(found, wheel_index(birth, golden))] += 1
                if birth + 1 in PREFIXES:
                    empty = sum(1 for k, w in enumerate(weights0) if w and counts[k] == 0)
                    empty_by_prefix.append((birth + 1, empty))
                    if birth + 1 == 256:
                        counts_256 = list(counts)
                if birth + 1 == max(PREFIXES):
                    worst = max(
                        abs(counts[k] - float((birth + 1) * weights0[k] / total0))
                        for k in range(len(order))
                    )
            for births, snapshot in ((256, counts_256), (4096, counts)):
                screen = [snapshot[order.index(f"screen_{y}")] for y in range(HEIGHT)]
                b = [screen[y] for y in bright]
                dk = [screen[y] for y in dark]
                mb, md = sum(b) / len(b), sum(dk) / len(dk)
                vis = (mb - md) / (mb + md) if mb + md else float("nan")
                wall = sum(snapshot[k] for k, o in enumerate(order) if o.startswith("wall"))
                faces = sum(snapshot[k] for k, o in enumerate(order) if o.startswith("face"))
                print(
                    f"  {name:12s} {births:4d} births: wall {wall}, screen {sum(screen)} on {sum(1 for c in screen if c)} pixels, faces {faces}; "
                    f"bright {b}; dark {dk}; Pearson {pearson(screen, cos):.3f}; visibility {vis:.3f}"
                )
            print(
                f"  {name:12s} empty cells (with weight) per prefix: {empty_by_prefix}; worst |count - B w / T| at 4096: {worst:.2f}"
            )


if __name__ == "__main__":
    main()
