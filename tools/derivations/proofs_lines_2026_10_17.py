"""The law's lines of 2026-10-17 (docs/ALGEBRA.md at b254f4d2: The bilinears of one pair, The Gram determinant of the planes, The charge of a plane is bounded by its share, The Ports' three readings, The staggering is exact, The quarter turn of a two-plane record, the integer rotations of The exact bands and the Hartree-Fock identity of The nucleon is a compact body of its family), the rows L86 to L93 of proofs_inventory.json: each a theorem checked exactly in Python's integers, fractions.Fraction and Gaussian rationals at random witnesses with the symmetric cases forced, every identity built from the line's coefficients as rule3.py and proofs_ground.py hold them and never from the conclusion, with a contrast beside it where the law names one (the wrong weight, the odd lay, the missing complement, the massless pair, the parallel spins); where the law prints a run's count the count is recomputed on a lay of this module and reported beside the law's.

Usage: `python tools/derivations/proofs_lines_2026_10_17.py` prints every verdict.
"""

from __future__ import annotations

import math
import random
import sys
from collections.abc import Sequence
from fractions import Fraction
from itertools import permutations, product
from math import isqrt
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import rule3  # noqa: E402
from proofs_ground import (
    PORTS,
    SEED,
    Check,
    Gaussian,
    angles,
    box_arrivals,
    box_index,
    box_nodes,
    integer_witness,
    link_factors,
    pairs,
    read,
    run,
    step_integer,
    step_line,
)  # noqa: E402

Line = tuple[list[Fraction], list[Fraction]]  # a solution's two levels, (now, before), over the Nodes
Plane = tuple[Line, Line]  # (re, im)
Board = tuple[tuple[int, int, int], list[list[int]]]
Matrix = list[list[Fraction]]
Coefficients = tuple[Fraction, list[list[Fraction]], list[Fraction], list[Fraction]]  # (w, R, S, p)
BOARDS: tuple[Board, ...] = tuple(
    (shape, box_arrivals(shape)) for shape in ((3, 1, 1), (4, 1, 1), (2, 2, 1), (2, 2, 2))
)
EXACT_PAIRS = (
    (1, 2),
    (0, 1),
    (-1, 2),
)  # 2 cos omega_0 = 1, 0, -1, the periods 6, 4, 3 (The exact bands)
PYTHAGOREAN_PAIRS = ((3, 5), (4, 5), (5, 13), (12, 13), (8, 17), (15, 17), (7, 25), (24, 25))
ONE = Fraction(1)
ABOUT_Z = ((0, -1, 0), (1, 0, 0), (0, 0, 1))  # the quarter turn about z: x -> y, y -> -x
ABOUT_X = ((1, 0, 0), (0, 0, -1), (0, 1, 0))  # the quarter turn about x: y -> z, z -> -y
BODY_DIAGONAL = ((0, 0, 1), (1, 0, 0), (0, 1, 0))  # the cube's C3: (x, y, z) -> (y, z, x)


def well(
    draw: random.Random, arrivals: Sequence[Sequence[int]], gamma: int
) -> tuple[list[int], list[list[int]]]:
    """Clocks that differ between Nodes (a static well) and Link factors read the same from both ends."""
    count = len(arrivals)
    while True:
        clocks = [draw.randint(max(1, gamma // 2), gamma) for _ in range(count)]
        if len(set(clocks)) > 1:
            return clocks, link_factors(arrivals, draw, gamma, spread=gamma // 3)


def random_line(draw: random.Random, count: int, size: int = 40) -> Line:
    return (
        [Fraction(draw.randint(-size, size)) for _ in range(count)],
        [Fraction(draw.randint(-size, size)) for _ in range(count)],
    )


def stepped(arrivals: Sequence[Sequence[int]], line: Coefficients, u: Line) -> Line:
    """The line without its division applied to a solution: (next, now)."""
    wall, reads, selves, _ = line
    return step_line(arrivals, reads, selves, wall, u[0], u[1]), list(u[0])


def omega(paces: Sequence[Fraction], u: Line, v: Line) -> Fraction:
    """Omega(u, v) = SUM_i (u_now v_before - v_now u_before) / p_i^2 (The bilinears of one pair), W at (re, im)."""
    return sum((u[0][i] * v[1][i] - v[0][i] * u[1][i]) / paces[i] ** 2 for i in range(len(paces)))


def polarised(arrivals: Sequence[Sequence[int]], line: Coefficients, u: Line, v: Line) -> Fraction:
    """E polarised over two solutions, (E(u + v) - E(u) - E(v)) / 2 for the law's E of The conserved form: SUM_i [w (u_now v_now + u_before v_before) - S_i (u_now v_before + v_now u_before) / 2] / p_i^2 - (1 / 2) SUM_i SUM_j (R_ij / p_i^2) (u_now,i v_before,j + v_now,i u_before,j); E(u, u) is E."""
    wall, reads, selves, paces = line
    total = Fraction(0)
    for i, ports in enumerate(arrivals):
        node = (
            wall * (u[0][i] * v[0][i] + u[1][i] * v[1][i])
            - selves[i] * (u[0][i] * v[1][i] + v[0][i] * u[1][i]) / 2
        )
        link = (
            sum(reads[i][port] * (u[0][i] * v[1][j] + v[0][i] * u[1][j]) for port, j in enumerate(ports))
            / 2
        )
        total += (node - link) / paces[i] ** 2
    return total


def bilinears(
    arrivals: Sequence[Sequence[int]], line: Coefficients, lines: Sequence[Line]
) -> tuple[dict, dict]:
    """The n (n - 1) / 2 Omegas and the n (n + 1) / 2 polarised forms of n lines, the n^2 numbers."""
    n = len(lines)
    omegas = {(a, b): omega(line[3], lines[a], lines[b]) for a in range(n) for b in range(a + 1, n)}
    forms = {
        (a, b): polarised(arrivals, line, lines[a], lines[b]) for a in range(n) for b in range(a, n)
    }
    return omegas, forms


def hermitian_matrix(paces: Sequence[Fraction], planes: Sequence[Plane]) -> list[list[Gaussian]]:
    """H_ab = Omega_C(z_a, z_b) / (2 i) over the planes as Gaussian levels, Omega_C(z, w) = SUM_i (conj(z_now) w_before - conj(z_before) w_now) / p_i^2: H_aa is the plane's weighted W."""
    count = len(paces)
    levels = [
        (
            [Gaussian(re[0][i], im[0][i]) for i in range(count)],
            [Gaussian(re[1][i], im[1][i]) for i in range(count)],
        )
        for re, im in planes
    ]
    matrix = []
    for z_a in levels:
        row = []
        for z_b in levels:
            total = Gaussian(0)
            for i in range(count):
                total = total + (z_a[0][i].conj() * z_b[1][i] - z_a[1][i].conj() * z_b[0][i]) * (
                    ONE / paces[i] ** 2
                )
            row.append(total * Gaussian(0, Fraction(-1, 2)))
        matrix.append(row)
    return matrix


def determinant(matrix: Matrix) -> Fraction:
    """The determinant by elimination in exact fractions."""
    rows = [list(row) for row in matrix]
    size, result = len(rows), Fraction(1)
    for column in range(size):
        pivot = next((r for r in range(column, size) if rows[r][column] != 0), None)
        if pivot is None:
            return Fraction(0)
        if pivot != column:
            rows[column], rows[pivot] = rows[pivot], rows[column]
            result = -result
        result *= rows[column][column]
        for r in range(column + 1, size):
            factor = rows[r][column] / rows[column][column]
            rows[r] = [a - factor * b for a, b in zip(rows[r], rows[column], strict=True)]
    return result


def rank(matrix: Sequence[Sequence[Fraction]]) -> int:
    """The rank by elimination in exact fractions."""
    rows = [list(row) for row in matrix if any(row)]
    found = 0
    for column in range(len(matrix[0]) if matrix else 0):
        pivot = next((r for r in range(found, len(rows)) if rows[r][column] != 0), None)
        if pivot is None:
            continue
        rows[found], rows[pivot] = rows[pivot], rows[found]
        for r in range(len(rows)):
            if r != found and rows[r][column] != 0:
                factor = rows[r][column] / rows[found][column]
                rows[r] = [a - factor * b for a, b in zip(rows[r], rows[found], strict=True)]
        found += 1
    return found


def positive_definite(matrix: Matrix) -> bool:
    """Sylvester's criterion: every leading principal minor positive."""
    return all(determinant([row[:k] for row in matrix[:k]]) > 0 for k in range(1, len(matrix) + 1))


def check_the_bilinears_of_one_pair() -> Check:
    """The bilinears of one pair (ALGEBRA.md at b254f4d2, The conserved form): two solutions u, v of one line conserve Omega(u, v) = SUM_i (u_now v_before - v_now u_before) / p_i^2 and E polarised over them exactly in the rationals at fixed paces, since D M is symmetric (D = diag(1 / p_i^2)): Omega(next, now) - Omega(now, before) = u_now . (D M - (D M)^T) v_now = 0 and E's polarisation is the conserved quadratic form's; so n lines carry n^2 conserved numbers, the n (n - 1) / 2 Omegas and the n (n + 1) / 2 polarised forms, 36 for the six lines of three planes, W = Omega(re, im) among them; in integers Omega walks by exactly SUM_i (epsilon_u,i v_now,i - epsilon_v,i u_now,i) / p_i^2 with epsilon = (r - r') / w, the remainders' term; a line stepped by another pair ([3, 4] beside the record's) conserves none with them, every cross Omega and cross form moving; three planes of one pair carry the Hermitian 3 x 3 matrix H_ab = Omega_C(z_a, z_b) / (2 i), Omega_C the sesquilinear Omega over the Gaussian levels, nine real conserved numbers whose trace is the record's weighted W, eight of them traceless; the contrast, the clock's weight 1 / p_0^2 for the pace's 1 / p_i^2, moves the cross Omega in a well. Four boards, five pairs with the symmetric ones forced, random clocks and Link factors read the same from both ends, the zero line among the six; a wrong coefficient, a wrong weight or a Link factor booked at one end breaks the equalities."""
    draw = random.Random(SEED)
    records, swung, moved_by_the_wrong_weight = 0, 0, 0
    for num, den in pairs(draw, 5):
        other = (3, 4) if (num, den) != (3, 4) else (2, 3)
        for shape, arrivals in BOARDS:
            gamma = draw.randint(6, 12)
            clocks, factors = well(draw, arrivals, gamma)
            line = read(arrivals, clocks, factors, num, den, gamma)
            paces = line[3]
            count = len(arrivals)
            lines = [random_line(draw, count) for _ in range(5)]
            lines.append(([Fraction(0)] * count, [Fraction(0)] * count))
            before = bilinears(arrivals, line, lines)
            after = bilinears(arrivals, line, [stepped(arrivals, line, u) for u in lines])
            if before != after:
                return False, {"pair": (num, den), "board": shape, "moved": "a bilinear of one pair"}
            if len(before[0]) + len(before[1]) != 36:
                return False, {"bilinears": len(before[0]) + len(before[1])}
            planes: list[Plane] = [(lines[0], lines[1]), (lines[2], lines[3]), (lines[4], lines[1])]
            h_before = hermitian_matrix(paces, planes)
            h_after = hermitian_matrix(
                paces, [(stepped(arrivals, line, re), stepped(arrivals, line, im)) for re, im in planes]
            )
            trace = h_before[0][0] + h_before[1][1] + h_before[2][2]
            wronskians = sum(omega(paces, re, im) for re, im in planes)
            if (
                h_before != h_after
                or any(h_before[a][b] != h_before[b][a].conj() for a in range(3) for b in range(3))
                or trace != Gaussian(wronskians, 0)
            ):
                return False, {"pair": (num, den), "board": shape, "moved": "the three planes' u(3)"}
            other_line = read(arrivals, clocks, factors, *other, gamma)
            u, v = lines[0], lines[1]
            u_next, v_other = stepped(arrivals, line, u), stepped(arrivals, other_line, v)
            cross_omega = (omega(paces, u, v), omega(paces, u_next, v_other))
            cross_form = (polarised(arrivals, line, u, v), polarised(arrivals, line, u_next, v_other))
            swung += cross_omega[0] != cross_omega[1] and cross_form[0] != cross_form[1]
            clock_paces = [Fraction(c) for c in clocks]
            moved_by_the_wrong_weight += omega(clock_paces, u, v) != omega(
                clock_paces, u_next, stepped(arrivals, line, v)
            )
            records += 1
    walks = 0
    for num, den in pairs(draw, 4):
        for _shape, arrivals in BOARDS:
            gamma, clocks, factors = integer_witness(draw, arrivals, draw.randint(2, 7), tension=True)
            wall, reads, selves, paces = read(arrivals, clocks, factors, num, den, gamma)
            count = len(arrivals)
            u, v = random_line(draw, count, 80), random_line(draw, count, 80)
            r_u = [draw.randint(0, int(wall) - 1) for _ in range(count)]
            r_v = [draw.randint(0, int(wall) - 1) for _ in range(count)]
            u_levels, u_carried = step_integer(arrivals, reads, selves, wall, u[0], u[1], r_u)
            v_levels, v_carried = step_integer(arrivals, reads, selves, wall, v[0], v[1], r_v)
            u_next = ([Fraction(x) for x in u_levels], list(u[0]))
            v_next = ([Fraction(x) for x in v_levels], list(v[0]))
            term = sum(
                (
                    Fraction(r_u[i] - u_carried[i], int(wall)) * v[0][i]
                    - Fraction(r_v[i] - v_carried[i], int(wall)) * u[0][i]
                )
                / paces[i] ** 2
                for i in range(count)
            )
            if omega(paces, u_next, v_next) - omega(paces, u, v) != term:
                return False, {"pair": (num, den), "integer walk": "not the remainders' term"}
            walks += 1
    held = swung == records and moved_by_the_wrong_weight == records
    return held, {
        "records of six lines, four boards and five pairs": records,
        "bilinears conserved per record, n^2 at n = 6": 36,
        "three planes' Hermitian numbers, the trace the weighted W": 9,
        "records whose cross numbers a line of another pair swung": swung,
        "records whose cross Omega the clock's weight moved": moved_by_the_wrong_weight,
        "integer walks equal to the remainders' term": walks,
    }


def gram(arrivals: Sequence[Sequence[int]], line: Coefficients, planes: Sequence[Plane]) -> Matrix:
    """K_ab, E polarised over the planes a and b, the sum over the planes' two lines (The Gram determinant of the planes)."""
    return [
        [
            polarised(arrivals, line, planes[a][0], planes[b][0])
            + polarised(arrivals, line, planes[a][1], planes[b][1])
            for b in range(len(planes))
        ]
        for a in range(len(planes))
    ]


def states(planes: Sequence[Plane]) -> list[list[Fraction]]:
    """Each plane's four levels over the Nodes as one vector, for the planes' rank."""
    return [[*re[0], *re[1], *im[0], *im[1]] for re, im in planes]


def combined(planes: Sequence[Plane], weights: Sequence[Fraction]) -> Plane:
    """SUM_a weights[a] planes[a], line by line."""
    count = len(planes[0][0][0])
    parts = []
    for part in (0, 1):
        levels = []
        for level in (0, 1):
            levels.append(
                [
                    sum(w * plane[part][level][i] for w, plane in zip(weights, planes, strict=True))
                    for i in range(count)
                ]
            )
        parts.append((levels[0], levels[1]))
    return parts[0], parts[1]


def packet(
    draw: random.Random, nodes: int, amplitude: float, centre: int, num: int, den: int
) -> list[list[int]]:
    """A plane's four integer lines, re now, re before, im now, im before, on a periodic chain: a wave at a random wave number under a bell of width 25 Nodes about the centre, the level before at the band's rotation (the lay of a packet, in the law's words)."""
    k = 2 * math.pi * draw.randint(5, 30) / nodes
    rotation = math.acos(num / (3 * den) * (2 + math.cos(k)))
    phase = draw.random() * 2 * math.pi
    lines: list[list[int]] = [[], [], [], []]
    for x in range(nodes):
        distance = min(abs(x - centre), nodes - abs(x - centre))
        bell = amplitude * math.exp(-((distance / 25.0) ** 2))
        lines[0].append(round(bell * math.cos(k * x + phase)))
        lines[1].append(round(bell * math.cos(k * x + phase + rotation)))
        lines[2].append(round(bell * math.sin(k * x + phase)))
        lines[3].append(round(bell * math.sin(k * x + phase + rotation)))
    return lines


def step_plane(
    arrivals: Sequence[Sequence[int]],
    lines: Sequence[Sequence[int]],
    remainders: Sequence[Sequence[int]],
    num: int,
    den: int,
    gamma: int,
) -> tuple[list[list[int]], list[list[int]]]:
    """rule3.step on a plane's two integer lines: ([re next, re now, im next, im now], the two lines' remainders)."""
    new_lines, new_remainders = [], []
    for now, before, rem in ((lines[0], lines[1], remainders[0]), (lines[2], lines[3], remainders[1])):
        out = [
            rule3.step(now[i], before[i], [now[j] for j in arrivals[i]], num, den, rem[i], gamma)
            for i in range(len(arrivals))
        ]
        new_lines += [[o[0] for o in out], list(now)]
        new_remainders.append([o[1] for o in out])
    return new_lines, new_remainders


def as_planes(records: Sequence[Sequence[Sequence[int]]]) -> list[Plane]:
    return [
        (
            ([Fraction(x) for x in lines[0]], [Fraction(x) for x in lines[1]]),
            ([Fraction(x) for x in lines[2]], [Fraction(x) for x in lines[3]]),
        )
        for lines in records
    ]


def check_the_gram_determinant_of_the_planes() -> Check:
    """The Gram determinant of the planes (ALGEBRA.md at b254f4d2, The count is the record's share): for n planes of one pair K_ab, E polarised over the planes a and b (the sum over their two lines), is their Gram matrix in the form's inner product, symmetric and conserved, its trace the record's form E (the share in the form's units), and at the vacuum's coefficients of a gapped family E is positive definite (row L84), so K is positive definite for independent planes (Sylvester's minors), its rank the planes' rank as vectors of their four levels, and det K = 0 exactly when they are dependent: identical planes, a plane laid as two others' sum and a rational combination all give det K = 0 and the rank n - 1, in the rationals before and after the step; the massless contrast, light's static uniform plane with E = 0 beside an independent one, has det K = 0 with the rank 2, so the gap is the condition. In integers on the law's chain of 221 at [4000, 6000]: two bit-identical planes step bit-identically under rule3.step and det K = 0 exactly; the plane laid as two overlapping packets' sum departs from their sum by the floors of the remainders, det K no longer 0, its smallest eigenvalue over the trace (det K over the second elementary symmetric function over the trace) after five intervals between 10^-5 and 10^-3 at the lay amplitudes 30 and 100, the law's range. Four boards and five pairs in Fractions; E at the vacuum anchored to rule3.conserved_form."""
    draw = random.Random(SEED)
    boards, dependent_lays = 0, 0
    for num, den in pairs(draw, 5):
        for shape, arrivals in BOARDS:
            gamma = draw.randint(2, 9)
            count = len(arrivals)
            line = read(arrivals, [gamma] * count, [[gamma] * PORTS] * count, num, den, gamma)
            planes = [(random_line(draw, count), random_line(draw, count)) for _ in range(3)]
            matrix = gram(arrivals, line, planes)
            after = gram(
                arrivals,
                line,
                [(stepped(arrivals, line, re), stepped(arrivals, line, im)) for re, im in planes],
            )
            form = sum(
                rule3.conserved_form(part[0], part[1], arrivals, num, den, gamma)
                for plane in planes
                for part in plane
            )
            trace = sum(matrix[a][a] for a in range(3))
            if (
                matrix != after
                or any(matrix[a][b] != matrix[b][a] for a in range(3) for b in range(3))
                or trace != form
            ):
                return False, {
                    "pair": (num, den),
                    "board": shape,
                    "failed": "symmetric, conserved, trace E",
                }
            if num < den:
                if not positive_definite(matrix) or rank(matrix) != 3 or rank(states(planes)) != 3:
                    return False, {
                        "pair": (num, den),
                        "board": shape,
                        "failed": "positive definite of rank 3",
                    }
                thirds = (
                    planes[0],
                    combined(planes[:2], (ONE, ONE)),
                    combined(planes[:2], (Fraction(2, 3), Fraction(-5))),
                )
                for third in thirds:
                    lay = [planes[0], planes[1], third]
                    later = [
                        (stepped(arrivals, line, re), stepped(arrivals, line, im)) for re, im in lay
                    ]
                    for record in (lay, later):
                        k = gram(arrivals, line, record)
                        if determinant(k) != 0 or rank(k) != 2 or rank(states(record)) != 2:
                            return False, {
                                "pair": (num, den),
                                "board": shape,
                                "failed": "a dependent lay",
                            }
                    dependent_lays += 1
            boards += 1
    arrivals = BOARDS[3][1]
    count = len(arrivals)
    line = read(arrivals, [1] * count, [[1] * PORTS] * count, 1, 1, 1)
    static: Plane = (
        ([Fraction(7)] * count, [Fraction(7)] * count),
        ([Fraction(-3)] * count, [Fraction(-3)] * count),
    )
    lay = [(random_line(draw, count), random_line(draw, count)), static]
    k = gram(arrivals, line, lay)
    massless_contrast = determinant(k) == 0 and rank(states(lay)) == 2 and k[1][1] == 0
    num, den, gamma, nodes = 4000, 6000, 6000, 221
    arrivals = rule3.chain_arrivals(nodes)
    half = rule3.coefficients(num, den, gamma)[0] // 2
    line = read(arrivals, [gamma] * nodes, [[gamma] * PORTS] * nodes, num, den, gamma)
    ratios, identical_bits = {}, True
    for amplitude in (30, 100):
        centre = draw.randint(0, nodes - 1)
        first = packet(draw, nodes, amplitude, centre, num, den)
        second = packet(draw, nodes, amplitude, centre + 8, num, den)
        total = [[a + b for a, b in zip(first[part], second[part], strict=True)] for part in range(4)]
        records = [first, second, total, [list(part) for part in first]]
        remainders = [[[half] * nodes, [half] * nodes] for _ in records]
        if determinant(gram(arrivals, line, as_planes(records[:3]))) != 0:
            return False, {"chain of 221": "det K not 0 at the lay of the sum"}
        for _ in range(5):
            for index in range(len(records)):
                records[index], remainders[index] = step_plane(
                    arrivals, records[index], remainders[index], num, den, gamma
                )
        identical_bits &= records[0] == records[3] and remainders[0] == remainders[3]
        twins = gram(arrivals, line, as_planes([records[0], records[1], records[3]]))
        if determinant(twins) != 0:
            return False, {"chain of 221": "det K not 0 for bit-identical planes"}
        k = gram(arrivals, line, as_planes(records[:3]))
        det = determinant(k)
        minors = sum(k[a][a] * k[b][b] - k[a][b] * k[b][a] for a in range(3) for b in range(a + 1, 3))
        trace = k[0][0] + k[1][1] + k[2][2]
        if det == 0:
            return False, {"chain of 221": "the sum plane did not depart"}
        ratios[amplitude] = float(det / minors / trace)
    in_range = all(1e-5 <= ratio <= 1e-3 for ratio in ratios.values())
    return massless_contrast and identical_bits and in_range, {
        "boards and pairs": boards,
        "dependent lays with det K = 0 and the rank 2, before and after the step": dependent_lays,
        "massless contrast, det K = 0 with independent planes at [1, 1]": massless_contrast,
        "bit-identical planes on the chain of 221, det K = 0": identical_bits,
        "the sum plane's smallest eigenvalue over the trace after five intervals": {
            f"amplitude {a}": f"{r:.1e}" for a, r in ratios.items()
        },
    }


def mode_form(cosine: Fraction, a: tuple[Fraction, Fraction]) -> Fraction:
    """q(a) = a_now^2 + a_before^2 - 2 cos omega a_now a_before, one mode's form, the 2 x 2 form of determinant sin^2 omega."""
    return a[0] ** 2 + a[1] ** 2 - 2 * cosine * a[0] * a[1]


def mode_cross(cosine: Fraction, a: tuple[Fraction, Fraction], b: tuple[Fraction, Fraction]) -> Fraction:
    """<a, b>_q = a_now b_now + a_before b_before - cos omega (a_now b_before + a_before b_now), the form's polarisation."""
    return a[0] * b[0] + a[1] * b[1] - cosine * (a[0] * b[1] + a[1] * b[0])


def mode_wronskian(a: tuple[Fraction, Fraction], b: tuple[Fraction, Fraction]) -> Fraction:
    return a[0] * b[1] - b[0] * a[1]


def lagrange_holds(cosine: Fraction, re, im) -> bool:
    """W^2 sin^2 omega = q(re) q(im) - <re, im>_q^2 (Lagrange's identity for the 2 x 2 form) and 2 |W| sin omega <= q(re) + q(im) as its square, exact in the rationals."""
    w = mode_wronskian(re, im)
    forms = mode_form(cosine, re), mode_form(cosine, im)
    identity = w * w * (1 - cosine * cosine) == forms[0] * forms[1] - mode_cross(cosine, re, im) ** 2
    return identity and 4 * w * w * (1 - cosine * cosine) <= (forms[0] + forms[1]) ** 2


def circular_plane(
    amplitude: int, phase: Gaussian, rotation: Gaussian, sense: int
) -> tuple[tuple[Fraction, Fraction], tuple[Fraction, Fraction]]:
    """re = A cos phi, A cos(phi - omega); im = sense x (A sin phi, A sin(phi - omega)): a circular plane of one sense at a rational angle."""
    earlier = phase * rotation.conj()
    return (amplitude * phase.re, amplitude * earlier.re), (
        sense * amplitude * phase.im,
        sense * amplitude * earlier.im,
    )


def fourier_vectors(shape: tuple[int, int, int]) -> list[tuple[int, list[int]]]:
    """The real Fourier vectors of a periodic box whose extents are 1, 2 or 4, entries in {0, 1, -1}: cos(k . x) and sin(k . x) at every k the box allows, each an eigenvector of the arrival sum S_6 with the eigenvalue 2 SUM_a cos k_a, returned as (SUM_a cos k_a, vector), orthogonal and complete."""
    nodes = box_nodes(shape)
    quarter = [(1, 0), (0, 1), (-1, 0), (0, -1)]  # (cos, sin) at the quarter turns
    found: list[tuple[int, list[int]]] = []
    seen: set[tuple[int, ...]] = set()
    for k in product(*(range(n) for n in shape)):
        cosines = sum(quarter[(k[axis] * (4 // shape[axis])) % 4][0] for axis in range(3))
        vector_cos, vector_sin = [], []
        for x in nodes:
            unit = Gaussian(1, 0)
            for axis in range(3):
                c, s = quarter[(k[axis] * x[axis] * (4 // shape[axis])) % 4]
                unit = unit * Gaussian(c, s)
            vector_cos.append(int(unit.re))
            vector_sin.append(int(unit.im))
        for vector in (vector_cos, vector_sin):
            key, negated = tuple(vector), tuple(-e for e in vector)
            if any(vector) and key not in seen and negated not in seen:
                seen.add(key)
                found.append((cosines, vector))
    return found


def projected(vector: Sequence[Fraction], weights: Sequence[Fraction], norm: Fraction, u: Line):
    """A line's two levels along a mode: (<phi, u_now>_D, <phi, u_before>_D) / <phi, phi>_D with the weights d_i."""
    return tuple(
        sum(v * x * d for v, x, d in zip(vector, level, weights, strict=True)) / norm for level in u
    )


def check_the_charge_of_a_plane_is_bounded_by_its_share() -> Check:
    """The charge of a plane is bounded by its share (ALGEBRA.md at b254f4d2, The paces): a plane at fixed paces has |W| <= I / 2 with I the invariant read mode by mode, since D M is self-adjoint in the D metric and the form and the Wronskian split over its eigenmodes, where each mode's form q(a) = a_now^2 + a_before^2 - 2 cos omega_k a_now a_before has the determinant sin^2 omega_k and Lagrange's identity W_k^2 sin^2 omega_k = q(re) q(im) - <re, im>_q^2 with the arithmetic mean's bound gives 2 |W_k| sin omega_k <= q(re) + q(im), equality iff q(re) = q(im) and <re, im>_q = 0, the mode circular; summed, |W| <= SUM_k E_k / (2 sin omega_k) = I / 2 with equality iff every mode is circular and of one sense. Checked exactly: the one-Node line at the Pythagorean pairs [3, 5] to [24, 25], whose rotation rule3.coefficients gives as 2 num / den and whose sine is rational, at random planes and at circular planes of either sense built at rational angles (equality), an elliptical, a real and a zero plane (strict), and records of several planes (equality iff all circular and of one sense); the vacuum's boxes of extents 1, 2 and 4 by Parseval, the Fourier vectors in {0, 1, -1} the eigenvectors of the line's read, the identity and the bound per mode exact and the summed bound in floats; the two-Node well at Gamma = 3, [5, 9], the clocks 1 and 2, whose D-symmetric matrix has rational eigenvalues, the split by its D-orthogonal modes exact. The fractions (2, 2, -1) / 3 give |W| / (I / 2) = 3 / 5 at the circular equality, the count 5 / 3 at the unit; 16,384 is T / 2 at T = 32,768. A wrong determinant (sin omega for sin^2), a wrong bound (I / 4, I) or a wrong weight breaks the identities or the equality cases."""
    draw = random.Random(SEED)
    one_node = [[0] * PORTS]  # every axis folded: the six arrivals are the Node's own level
    planes_checked, equalities, strict = 0, 0, 0
    for num, den in PYTHAGOREAN_PAIRS:
        wall, reads, selves, _ = read(one_node, [1], [[1] * PORTS], num, den, 1)
        cosine = (selves[0] + sum(reads[0])) / (2 * wall)
        square = 1 - cosine * cosine
        sine = Fraction(isqrt(square.numerator), isqrt(square.denominator))
        if cosine != Fraction(num, den) or sine * sine != square:
            return False, {"pair": (num, den), "cos omega from the line": cosine}
        rotation = Gaussian(cosine, sine)
        witnesses: list[tuple[tuple, tuple, bool]] = []  # (re, im, circular)
        for _ in range(6):
            re = (Fraction(draw.randint(-50, 50)), Fraction(draw.randint(-50, 50)))
            im = (Fraction(draw.randint(-50, 50)), Fraction(draw.randint(-50, 50)))
            witnesses.append((re, im, False))
        for phase in angles(draw, 8):
            amplitude = draw.randint(1, 30)
            for sense in (1, -1):
                witnesses.append((*circular_plane(amplitude, phase, rotation, sense), True))
            re, im = circular_plane(amplitude, phase, rotation, 1)
            witnesses.append((re, (im[0] * Fraction(2, 3), im[1] * Fraction(2, 3)), False))  # elliptical
            witnesses.append((re, (Fraction(0), Fraction(0)), False))  # a real plane
        witnesses.append(((Fraction(0), Fraction(0)), (Fraction(0), Fraction(0)), False))
        for re, im, circular in witnesses:
            if not lagrange_holds(cosine, re, im):
                return False, {"pair": (num, den), "plane": (re, im), "failed": "Lagrange or the bound"}
            w = mode_wronskian(re, im)
            invariant = (mode_form(cosine, re) + mode_form(cosine, im)) / sine
            equality = 2 * abs(w) == invariant
            expected = mode_form(cosine, re) == mode_form(cosine, im) and mode_cross(cosine, re, im) == 0
            if (
                equality != expected
                or (circular and not equality)
                or (equality and not circular and any(re + im))
            ):
                return False, {"pair": (num, den), "plane": (re, im), "failed": "equality iff circular"}
            planes_checked += 1
            equalities += equality
            strict += not equality
        phases = angles(draw, 3)[1:]
        same = [
            circular_plane(draw.randint(1, 20), phases[0], rotation, 1),
            circular_plane(draw.randint(1, 20), phases[1], rotation, 1),
        ]
        opposite = [same[0], circular_plane(draw.randint(1, 20), phases[1], rotation, -1)]
        mixed = [same[0], (same[1][0], (same[1][1][0] / 2, same[1][1][1] / 2))]
        for record, expected in ((same, True), (opposite, False), (mixed, False)):
            total_w = sum(mode_wronskian(re, im) for re, im in record)
            total_invariant = sum(
                (mode_form(cosine, re) + mode_form(cosine, im)) / sine for re, im in record
            )
            if 2 * abs(total_w) > total_invariant or (2 * abs(total_w) == total_invariant) != expected:
                return False, {"pair": (num, den), "record": "the senses' equality"}
    modes_checked = 0
    for num, den in [p for p in pairs(draw, 6) if p[0] < p[1]]:
        for shape in ((2, 1, 1), (4, 1, 1), (2, 2, 1), (2, 2, 2), (4, 2, 1)):
            arrivals = box_arrivals(shape)
            count = len(arrivals)
            line = read(arrivals, [1] * count, [[1] * PORTS] * count, num, den, 1)
            wall, reads, selves, paces = line
            re, im = random_line(draw, count), random_line(draw, count)
            total_w = omega(paces, re, im)
            form = polarised(arrivals, line, re, re) + polarised(arrivals, line, im, im)
            split_w, split_form, bound = Fraction(0), Fraction(0), 0.0
            for cosines, vector in fourier_vectors(shape):
                weight = Fraction(sum(e * e for e in vector))
                cosine = Fraction(num, 3 * den) * cosines
                image = [
                    selves[i] * vector[i]
                    + sum(reads[i][port] * vector[j] for port, j in enumerate(ports))
                    for i, ports in enumerate(arrivals)
                ]
                if image != [wall * 2 * cosine * e for e in vector]:
                    return False, {"box": shape, "mode": vector, "failed": "an eigenvector of the line"}
                phi = [Fraction(e) for e in vector]
                a = projected(phi, [ONE] * count, weight, re)
                b = projected(phi, [ONE] * count, weight, im)
                if not lagrange_holds(cosine, a, b):
                    return False, {
                        "box": shape,
                        "pair": (num, den),
                        "failed": "a mode's Lagrange identity",
                    }
                split_w += weight * mode_wronskian(a, b)
                mode_total = mode_form(cosine, a) + mode_form(cosine, b)
                split_form += weight * mode_total
                bound += float(weight * mode_total) / (2 * math.sqrt(1 - float(cosine) ** 2))
                modes_checked += 1
            if (
                split_w != total_w
                or split_form * wall != form
                or abs(float(total_w)) > bound * (1 + 1e-12)
            ):
                return False, {
                    "box": shape,
                    "pair": (num, den),
                    "failed": "Parseval's split or the bound",
                }
    arrivals = box_arrivals((2, 1, 1))
    num, den, gamma = 5, 9, 3
    line = read(arrivals, [1, 2], [[gamma] * PORTS] * 2, num, den, gamma)
    wall, reads, selves, paces = line
    m = [[selves[i] / wall if i == j else Fraction(0) for j in range(2)] for i in range(2)]
    for i, ports in enumerate(arrivals):
        for port, j in enumerate(ports):
            m[i][j] += reads[i][port] / wall
    symmetric = [[m[i][j] * paces[j] / paces[i] for j in range(2)] for i in range(2)]
    if symmetric[0][1] != symmetric[1][0]:
        return False, {"well": "D^(1/2) M D^(-1/2) not symmetric"}
    discriminant = (symmetric[0][0] - symmetric[1][1]) ** 2 + 4 * symmetric[0][1] ** 2
    root = Fraction(isqrt(discriminant.numerator), isqrt(discriminant.denominator))
    if root * root != discriminant:
        return False, {"well": "the modes are not rational"}
    weights = [ONE / p**2 for p in paces]
    modes = []
    for sign in (1, -1):
        value = (symmetric[0][0] + symmetric[1][1] + sign * root) / 2
        v = [symmetric[0][1], value - symmetric[0][0]]
        phi = [v[0] * paces[0], v[1] * paces[1]]  # D^(-1/2) v, a mode of M
        if [sum(m[i][j] * phi[j] for j in range(2)) for i in range(2)] != [value * x for x in phi]:
            return False, {"well": "not a mode of M"}
        modes.append((value / 2, phi, sum(x * x * d for x, d in zip(phi, weights, strict=True))))
    if sum(modes[0][1][i] * modes[1][1][i] * weights[i] for i in range(2)) != 0:
        return False, {"well": "the modes are not D-orthogonal"}
    re, im = random_line(draw, 2), random_line(draw, 2)
    split_w, split_form, bound = Fraction(0), Fraction(0), 0.0
    for cosine, phi, norm in modes:
        a, b = projected(phi, weights, norm, re), projected(phi, weights, norm, im)
        if not lagrange_holds(cosine, a, b) or not -1 < cosine < 1:
            return False, {"well": "a mode's Lagrange identity", "cos omega_k": cosine}
        mode_total = mode_form(cosine, a) + mode_form(cosine, b)
        split_w += norm * mode_wronskian(a, b)
        split_form += norm * mode_total
        bound += float(norm * mode_total) / (2 * math.sqrt(1 - float(cosine) ** 2))
    form = polarised(arrivals, line, re, re) + polarised(arrivals, line, im, im)
    well_holds = (
        split_w == omega(paces, re, im)
        and split_form * wall == form
        and abs(float(split_w)) <= bound * (1 + 1e-12)
    )
    fractions = (Fraction(2, 3), Fraction(2, 3), Fraction(-1, 3))
    share_of_the_unit = abs(sum(fractions)) / sum(abs(f) for f in fractions)
    count_at_the_unit = sum(abs(f) for f in fractions) / abs(sum(fractions))
    arithmetic = (share_of_the_unit, count_at_the_unit, 32768 // 2) == (
        Fraction(3, 5),
        Fraction(5, 3),
        16384,
    )
    return well_holds and arithmetic, {
        "one-Node planes at the Pythagorean pairs (equalities, strict)": (
            planes_checked,
            equalities,
            strict,
        ),
        "Fourier modes of the vacuum's boxes with the identity and the bound": modes_checked,
        "the well's modes, cos omega_k": [str(c) for c, _, _ in modes],
        "fractions (2, 2, -1) / 3: |W| over the unit, the count at the unit": (
            str(share_of_the_unit),
            str(count_at_the_unit),
        ),
    }


def signed_permutations() -> list[tuple[tuple[int, ...], tuple[int, ...]]]:
    """The cube's 48: a permutation of the three axes with a sign on each."""
    return [(perm, signs) for perm in permutations(range(3)) for signs in product((1, -1), repeat=3)]


def carried(perm: Sequence[int], signs: Sequence[int], arrivals: Sequence) -> list:
    """The six arrivals carried by a signed permutation: the Port (+a) goes to (sign_a perm(a))."""
    found: list = [None] * PORTS
    for axis in range(3):
        for index, sign in enumerate((1, -1)):
            found[2 * perm[axis] + (0 if sign * signs[axis] == 1 else 1)] = arrivals[2 * axis + index]
    return found


def pieces(arrivals: Sequence[int]) -> tuple[Fraction, list[Fraction], list[Fraction]]:
    """The sum, the quadrupole pair (the three axis sums less their mean, two independent) and the three signed differences."""
    total = Fraction(sum(arrivals))
    sums = [Fraction(arrivals[2 * a] + arrivals[2 * a + 1]) for a in range(3)]
    return (
        total,
        [s - total / 3 for s in sums],
        [Fraction(arrivals[2 * a] - arrivals[2 * a + 1]) for a in range(3)],
    )


def inflow(num: int, now_i: int, before_i: int, neighbours: Sequence[tuple[int, int]]) -> Fraction:
    """The click's inflow into a Node's region: SUM over the six Ports of F_ij from rule3.link_current."""
    return sum((rule3.link_current(num, now_i, before_i, n, b) for n, b in neighbours), Fraction(0))


def momentum(
    num: int, now_i: int, before_i: int, neighbours: Sequence[tuple[int, int]]
) -> list[Fraction]:
    """P_a(i) = (F_(i, i-a) - F_(i, i+a)) / num, the lattice momentum density (row 5 of The conventions and the units)."""
    return [
        (
            rule3.link_current(num, now_i, before_i, *neighbours[2 * a + 1])
            - rule3.link_current(num, now_i, before_i, *neighbours[2 * a])
        )
        / num
        for a in range(3)
    ]


def shifted(
    neighbours: Sequence[tuple[int, int]], ports: Sequence[int], shift: tuple[int, int], sign: int = 1
):
    """The neighbours with (now, before) moved by sign x shift at the Ports named."""
    found = list(neighbours)
    for port in ports:
        found[port] = (neighbours[port][0] + sign * shift[0], neighbours[port][1] + sign * shift[1])
    return found


def check_the_ports_three_readings() -> Check:
    """The Ports' three readings (ALGEBRA.md at b254f4d2, The click is the meeting): under the 48 signed permutations of the axes a Node's six arrivals split into their sum (invariant), the quadrupole pair (the axis sums less their mean, carried among themselves) and the three signed differences along the axes (carried as a vector, the sign of the axis on each), three orthogonal pieces of the dimensions 1 + 2 + 3 = 6 that rebuild the arrivals exactly; Rule3's numerator SUM_a R_a (arr(+a) + arr(-a)) + S a_now (rule3.numerator) is even in every axis, unchanged under the swap of an axis's two arrivals, so it reads the sum alone at uniform paces (unchanged when a level moves between axes), the sum and the pair where the Link paces differ by axis (moved by (R_x - R_y) delta) and the differences never, and rule3.step is bit-identical, level and remainder, under any change of the differences, 2,000 trials per pair at eight pairs at random by-axis Link paces; the click's inflow through a region's front Ports, SUM over the Ports of F_ij with F from rule3.link_current, depends on the six neighbours' sums alone (unchanged under any permutation of the neighbours), the lattice momentum density P_a = (F_(i, i-a) - F_(i, i+a)) / num on the differences alone (unchanged when a level is added at both ends of the axis, its sign reversed with the ends), and both stand under a move of the quadrupole pair, which no line reads; a traceless symmetric tensor's 5 components split as the diagonal pair's 2 and the off-diagonal 3, and the line's read is one coefficient per axis, diag(R_x, R_y, R_z), the + and no x. A read of a difference anywhere in the step or the bookings, or a pair read at uniform paces, breaks the equalities."""
    draw = random.Random(SEED)
    group = signed_permutations()
    if len(set(group)) != 48:
        return False, {"group": len(set(group))}
    for _ in range(20):
        arrivals = [draw.randint(-99, 99) for _ in range(PORTS)]
        total, pair, differences = pieces(arrivals)
        rebuilt = [total / 6 + pair[a] / 2 + s * differences[a] / 2 for a in range(3) for s in (1, -1)]
        vectors = (
            [total / 6] * PORTS,
            [pair[a] / 2 for a in range(3) for _ in (0, 1)],
            [s * differences[a] / 2 for a in range(3) for s in (1, -1)],
        )
        orthogonal = all(
            sum(x * y for x, y in zip(vectors[p], vectors[q], strict=True)) == 0
            for p in range(3)
            for q in range(p)
        )
        if rebuilt != [Fraction(x) for x in arrivals] or not orthogonal:
            return False, {"arrivals": arrivals, "failed": "the three pieces"}
        for perm, signs in group:
            image_total, image_pair, image_differences = pieces(carried(perm, signs, arrivals))
            if (
                image_total != total
                or any(image_pair[perm[a]] != pair[a] for a in range(3))
                or any(image_differences[perm[a]] != signs[a] * differences[a] for a in range(3))
            ):
                return False, {"element": (perm, signs), "failed": "the pieces under the 48"}
    trials, identical, pair_read_by_axis = 0, 0, 0
    for num, den in pairs(draw, 8):
        gamma = draw.randint(3, 40)
        for _ in range(2000):
            by_axis = tuple(draw.randint(1, gamma) for _ in range(3))
            now, before = draw.randint(-999, 999), draw.randint(-999, 999)
            arrivals = [draw.randint(-999, 999) for _ in range(PORTS)]
            delta = draw.randint(1, 50)
            for links in ((gamma, gamma, gamma), by_axis):
                wall, reads, self_coefficient = rule3.coefficients(num, den, gamma, None, links)
                value = rule3.numerator(now, arrivals, reads, self_coefficient)
                for axis in range(3):
                    swapped = list(arrivals)
                    swapped[2 * axis], swapped[2 * axis + 1] = swapped[2 * axis + 1], swapped[2 * axis]
                    moved = list(arrivals)
                    moved[2 * axis] += delta
                    moved[2 * axis + 1] -= delta
                    if (
                        rule3.numerator(now, swapped, reads, self_coefficient) != value
                        or rule3.numerator(now, moved, reads, self_coefficient) != value
                    ):
                        return False, {"pair": (num, den), "failed": "the numerator read a difference"}
                    remainder = draw.randint(0, wall - 1)
                    if rule3.step(
                        now, before, arrivals, num, den, remainder, gamma, None, links
                    ) != rule3.step(now, before, moved, num, den, remainder, gamma, None, links):
                        return False, {"pair": (num, den), "failed": "the step read a difference"}
                    identical += 1
                between = list(
                    arrivals
                )  # the quadrupole pair moved: a level from the x axis to the y axis
                between[0] += delta
                between[2] -= delta
                change = rule3.numerator(now, between, reads, self_coefficient) - value
                if change != (reads[0] - reads[1]) * delta:
                    return False, {
                        "pair": (num, den),
                        "failed": "the pair's read is not (R_x - R_y) delta",
                    }
                pair_read_by_axis += change != 0
            trials += 1
    bookings = 0
    for _ in range(200):
        num = draw.randint(1, 9)
        now_i, before_i = draw.randint(-99, 99), draw.randint(-99, 99)
        neighbours = [(draw.randint(-99, 99), draw.randint(-99, 99)) for _ in range(PORTS)]
        shuffled = list(neighbours)
        draw.shuffle(shuffled)
        axis, shift = draw.randint(0, 2), (draw.randint(-50, 50), draw.randint(-50, 50))
        both_ends = shifted(neighbours, (2 * axis, 2 * axis + 1), shift)
        swapped = list(neighbours)
        swapped[2 * axis], swapped[2 * axis + 1] = swapped[2 * axis + 1], swapped[2 * axis]
        moved_pair = shifted(shifted(neighbours, (0, 1), shift), (2, 3), shift, -1)
        expected_swap = momentum(num, now_i, before_i, neighbours)
        expected_swap[axis] = -expected_swap[axis]
        if (
            inflow(num, now_i, before_i, shuffled) != inflow(num, now_i, before_i, neighbours)
            or momentum(num, now_i, before_i, both_ends) != momentum(num, now_i, before_i, neighbours)
            or momentum(num, now_i, before_i, swapped) != expected_swap
            or inflow(num, now_i, before_i, moved_pair) != inflow(num, now_i, before_i, neighbours)
            or momentum(num, now_i, before_i, moved_pair) != momentum(num, now_i, before_i, neighbours)
        ):
            return False, {"failed": "the inflow or the momentum read the wrong piece"}
        bookings += 1
    reads = rule3.coefficients(2, 3, 5, None, (5, 4, 3))[1]
    tensor = len(reads) == 3 and 5 == 2 + 3
    return tensor and pair_read_by_axis > 0, {
        "pieces under the 48": "the sum invariant, the pair among itself, the differences a vector",
        "trials per pair, eight pairs": trials // 8,
        "steps bit-identical under a change of the differences": identical,
        "trials whose pair the by-axis paces read": pair_read_by_axis,
        "bookings: the inflow the sum, the momentum the differences, neither the pair": bookings,
        "the read's tensor diagonal": tensor,
    }


def staggered_records(
    draw: random.Random,
    arrivals: Sequence[Sequence[int]],
    parity: Sequence[int],
    wall: int,
    gamma: int,
    complement: bool,
    paces: tuple,
    intervals: int,
) -> tuple[int, int]:
    """The [1, 2] record and its staggered copy stepped by rule3.step as [-1, 2] side by side, from random levels and remainders, the odd Nodes' levels negated and their remainders complemented where asked: (Nodes broken at the first interval, Nodes broken over all the intervals)."""
    clock, links = paces
    count = len(arrivals)
    now = [draw.randint(-1000, 1000) for _ in range(count)]
    before = [draw.randint(-1000, 1000) for _ in range(count)]
    remainders = [draw.randint(0, wall - 1) for _ in range(count)]
    s_now = [p * x for p, x in zip(parity, now, strict=True)]
    s_before = [p * x for p, x in zip(parity, before, strict=True)]
    s_remainders = [
        (wall - 1 - r) if (p < 0 and complement) else r for p, r in zip(parity, remainders, strict=True)
    ]
    first, total = 0, 0
    for interval in range(intervals):
        plain = [
            rule3.step(
                now[i],
                before[i],
                [now[j] for j in arrivals[i]],
                1,
                2,
                remainders[i],
                gamma,
                clock,
                links,
            )
            for i in range(count)
        ]
        signed = [
            rule3.step(
                s_now[i],
                s_before[i],
                [s_now[j] for j in arrivals[i]],
                -1,
                2,
                s_remainders[i],
                gamma,
                clock,
                links,
            )
            for i in range(count)
        ]
        broken = sum(
            1
            for i in range(count)
            if signed[i][0] != parity[i] * plain[i][0]
            or signed[i][1]
            != ((wall - 1 - plain[i][1]) if (parity[i] < 0 and complement) else plain[i][1])
        )
        first, total = (broken if interval == 0 else first), total + broken
        before, now, remainders = now, [x[0] for x in plain], [x[1] for x in plain]
        s_before, s_now, s_remainders = s_now, [x[0] for x in signed], [x[1] for x in signed]
    return first, total


def space_time_staggered(
    draw: random.Random,
    arrivals: Sequence[Sequence[int]],
    parity: Sequence[int],
    wall: int,
    gamma: int,
    complement: bool,
) -> int:
    """A [1, 2] record and its space-time staggered copy (-1)^(t + x + y + z) a stepped by rule3.step over two intervals, the copy's remainders complemented at the odd space-time parity where asked: the Nodes whose level departs from the signed record at the second interval."""
    count = len(arrivals)
    now = [draw.randint(-1000, 1000) for _ in range(count)]
    before = [draw.randint(-1000, 1000) for _ in range(count)]
    remainders = [draw.randint(0, wall - 1) for _ in range(count)]
    sign_now, sign_before = list(parity), [-p for p in parity]  # the sign at t = 0 and at t = -1
    s_now = [s * x for s, x in zip(sign_now, now, strict=True)]
    s_before = [s * x for s, x in zip(sign_before, before, strict=True)]
    s_remainders = [
        (wall - 1 - r) if (s < 0 and complement) else r
        for s, r in zip(sign_now, remainders, strict=True)
    ]
    differing = 0
    for _ in range(2):
        plain = [
            rule3.step(now[i], before[i], [now[j] for j in arrivals[i]], 1, 2, remainders[i], gamma)
            for i in range(count)
        ]
        signed = [
            rule3.step(
                s_now[i], s_before[i], [s_now[j] for j in arrivals[i]], 1, 2, s_remainders[i], gamma
            )
            for i in range(count)
        ]
        sign_next = [-s for s in sign_now]
        differing = sum(1 for i in range(count) if signed[i][0] != sign_next[i] * plain[i][0])
        before, now, remainders = now, [x[0] for x in plain], [x[1] for x in plain]
        s_before, s_now, s_remainders = s_now, [x[0] for x in signed], [x[1] for x in signed]
        sign_now = sign_next
    return differing


def check_the_staggering_is_exact() -> Check:
    """The staggering is exact (ALGEBRA.md at b254f4d2, A family's declaration): b = (-1)^(x + y + z) a signs every arrival against its Node, so b obeys the line with R_a -> -R_a and S unchanged, exact in the rationals at any clocks and Link factors on a box of even extents; at the vacuum S = 0 and rule3.coefficients gives [-num, den] the same w and S and the negated R, so a record of [num, den] and one of [-num, den] are one record read on the two sublattices with opposite signs, while in a content their S differ by 24 num (p_a^2 - p_0^2); in integers the odd Nodes' numerators are negated, so with their remainders complemented, w - 1 - r, the floor commutes (row L23) and rule3.step keeps the two records bit for bit, level and remainder, on the 4 x 4 x 4 box over 60 intervals at [1, 2] against [-1, 2] from random levels and remainders; without the complement Nodes break at the first interval, and in the content c = 20 of Gamma = 6,000 (S / w = 0.0199) nearly every Node breaks, the counts recomputed on this lay beside the law's 18 and 63 of 64. The space-time (-1)^(t + x + y + z) a maps a pair's line to itself with S -> -S exactly in the rationals (b_before carries the opposite sign to b_now and the neighbours the opposite sign to the Node), and not in integers: the staggered copy stepped by rule3.step with the complement at the odd space-time parity, or without it, departs from the signed record by the second interval, no remainder alternating its sign with the interval. A sign kept on S, a remainder kept uncomplemented or an odd extent breaks the bit-for-bit equality."""
    draw = random.Random(SEED)
    rational_boxes = 0
    for num, den in pairs(draw, 4):
        for shape in ((2, 2, 2), (4, 2, 2), (2, 4, 2)):
            arrivals = box_arrivals(shape)
            nodes = box_nodes(shape)
            parity = [(-1) ** (x + y + z) for x, y, z in nodes]
            gamma = draw.randint(6, 12)
            clocks, factors = well(draw, arrivals, gamma)
            wall, reads, selves, _ = read(arrivals, clocks, factors, num, den, gamma)
            negated = [[-r for r in row] for row in reads]
            a = random_line(draw, len(nodes))
            a_next = step_line(arrivals, reads, selves, wall, a[0], a[1])
            b_now = [p * x for p, x in zip(parity, a[0], strict=True)]
            b_before = [p * x for p, x in zip(parity, a[1], strict=True)]
            if step_line(arrivals, negated, selves, wall, b_now, b_before) != [
                p * x for p, x in zip(parity, a_next, strict=True)
            ]:
                return False, {
                    "pair": (num, den),
                    "box": shape,
                    "failed": "the spatial sign in the rationals",
                }
            minus = [-s for s in selves]
            if step_line(arrivals, reads, minus, wall, b_now, [-x for x in b_before]) != [
                -p * x for p, x in zip(parity, a_next, strict=True)
            ]:
                return False, {
                    "pair": (num, den),
                    "box": shape,
                    "failed": "the space-time sign in the rationals",
                }
            rational_boxes += 1
    gamma = 6000
    clock = round(rule3.clock_pace(gamma, 20))
    pace = round(rule3.node_pace(clock, gamma))
    for num, den in ((1, 2), (2, 3), (4000, 6000)):
        wall, reads, self_vacuum = rule3.coefficients(num, den, gamma)
        if (
            rule3.coefficients(-num, den, gamma) != (wall, tuple(-r for r in reads), 0)
            or self_vacuum != 0
        ):
            return False, {"pair": (num, den), "failed": "[-num, den] at the vacuum"}
        in_content = rule3.coefficients(num, den, gamma, clock, (pace,) * 3)
        minus_content = rule3.coefficients(-num, den, gamma, clock, (pace,) * 3)
        if minus_content[2] - in_content[2] != 24 * num * (pace * pace - clock * clock) or minus_content[
            1
        ] != tuple(-r for r in in_content[1]):
            return False, {"pair": (num, den), "failed": "[-num, den] in a content"}
    shape = (4, 4, 4)
    arrivals, nodes = box_arrivals(shape), box_nodes(shape)
    parity = [(-1) ** (x + y + z) for x, y, z in nodes]
    wall = 6 * 2 * gamma * gamma
    content_ratio = rule3.coefficients(1, 2, gamma, clock, (pace,) * 3)[2] / wall
    exact = staggered_records(draw, arrivals, parity, wall, gamma, True, (None, None), 60)
    without = staggered_records(draw, arrivals, parity, wall, gamma, False, (None, None), 1)
    in_content = staggered_records(draw, arrivals, parity, wall, gamma, True, (clock, (pace,) * 3), 1)
    departures = [space_time_staggered(draw, arrivals, parity, wall, gamma, c) for c in (True, False)]
    held = exact == (0, 0) and without[0] > 0 and in_content[0] > 0 and all(d > 0 for d in departures)
    return held, {
        "boxes of even extents, the two signs exact in the rationals": rational_boxes,
        "4 x 4 x 4 at the vacuum over 60 intervals, Nodes broken (first interval, all)": exact,
        "without the complement, Nodes broken at the first interval of 64 (the law's lay 18)": without[
            0
        ],
        "in the content S / w = 0.0199, Nodes broken at the first interval of 64 (the law's lay 63)": in_content[
            0
        ],
        "S / w of the content": round(content_ratio, 4),
        "space-time sign in integers, Nodes departing at the second interval (complement, none)": departures,
    }


def pauli_lift(a: int, b: int, c: int, d: int) -> list[list[Gaussian]]:
    """The quaternion a + b i + c j + d k as a I - i (b sigma_x + c sigma_y + d sigma_z) = [[a - i d, -c - i b], [c - i b, a + i d]], over the scale sqrt(a^2 + b^2 + c^2 + d^2) left out."""
    return [[Gaussian(a, -d), Gaussian(-c, -b)], [Gaussian(c, -b), Gaussian(a, d)]]


def times(left: list[list[Gaussian]], right: list[list[Gaussian]]) -> list[list[Gaussian]]:
    return [[left[i][0] * right[0][j] + left[i][1] * right[1][j] for j in range(2)] for i in range(2)]


def adjoint(matrix: list[list[Gaussian]]) -> list[list[Gaussian]]:
    return [[matrix[j][i].conj() for j in range(2)] for i in range(2)]


PAULI = (
    [[Gaussian(0), Gaussian(1)], [Gaussian(1), Gaussian(0)]],
    [[Gaussian(0), Gaussian(0, -1)], [Gaussian(0, 1), Gaussian(0)]],
    [[Gaussian(1), Gaussian(0)], [Gaussian(0), Gaussian(-1)]],
)


def rotation_of(lift: list[list[Gaussian]]) -> tuple[tuple[tuple[int, ...], ...], Fraction]:
    """The rotation a lift turns the axis vector by, read off exactly: U sigma_a U^dagger = s^2 SUM_b R_ba sigma_b with s^2 the lift's row norm; (R, s^2)."""
    norm = lift[0][0].abs2() + lift[0][1].abs2()
    columns = []
    for sigma in PAULI:
        image = times(times(lift, sigma), adjoint(lift))
        x, y, z = image[0][1].re, -image[0][1].im, image[0][0].re
        if image != [[Gaussian(z), Gaussian(x, -y)], [Gaussian(x, y), Gaussian(-z)]]:
            raise ValueError("not a rotation of the Pauli axes")
        column = [x / norm, y / norm, z / norm]
        if any(e.denominator != 1 for e in column):
            raise ValueError("not a signed permutation")
        columns.append([int(e) for e in column])
    return tuple(tuple(columns[a][b] for a in range(3)) for b in range(3)), norm


def binary_octahedral() -> list[tuple[int, int, int, int]]:
    """The 48 unit quaternions of the cube's rotations, each scaled to integers: the eight units, the sixteen (+-1 +-i +-j +-k) / 2 and the twenty-four (+-e +-f) / sqrt 2."""
    found = []
    for i in range(4):
        for sign in (1, -1):
            q = [0, 0, 0, 0]
            q[i] = sign
            found.append(tuple(q))
    found += list(product((1, -1), repeat=4))
    for i in range(4):
        for j in range(i + 1, 4):
            for s_i in (1, -1):
                for s_j in (1, -1):
                    q = [0, 0, 0, 0]
                    q[i], q[j] = s_i, s_j
                    found.append(tuple(q))
    return found


def box_map(shape: tuple[int, int, int], rotation: Sequence[Sequence[int]]) -> list[int]:
    """The index of every Node's image under a signed permutation of the axes on a periodic box: image[i] is where the Node i goes."""
    return [
        box_index(shape, *[sum(rotation[b][a] * x[a] for a in range(3)) for b in range(3)])
        for x in box_nodes(shape)
    ]


def monomial_turn(
    mixing: list[list[Gaussian]],
    levels: Sequence[Sequence[int]],
    remainders: Sequence[Sequence[int]],
    image: Sequence[int],
    wall: int,
) -> tuple[list[list[int]], list[list[int]]]:
    """A two-plane record carried by a lift whose entries are units: at the image Node z'_a = u z_b for the one unit u of the row a, so re'_a and im'_a are signed copies of re_b or im_b (Re(u z_b), Im(u z_b)) and a negated line's remainder is complemented, w - 1 - r; the lines re1, im1, re2, im2 now and the same before, the four remainders."""
    count = len(image)
    moved = [[0] * count for _ in range(8)]
    moved_rem = [[0] * count for _ in range(4)]
    for a in range(2):
        b = next(j for j in range(2) if mixing[a][j].abs2() == 1)
        unit = mixing[a][b]
        for part, (on_re, on_im) in enumerate(((unit.re, -unit.im), (unit.im, unit.re))):
            source, sign = (2 * b, int(on_re)) if on_re else (2 * b + 1, int(on_im))
            for i in range(count):
                for half in (0, 4):
                    moved[half + 2 * a + part][image[i]] = sign * levels[half + source][i]
                r = remainders[source][i]
                moved_rem[2 * a + part][image[i]] = r if sign == 1 else wall - 1 - r
    return moved, moved_rem


def mixed(mixing: list[list[Gaussian]], record: Sequence[Line], image: Sequence[int]) -> list[Line]:
    """A two-plane record carried by a lift in the rationals: z' = mixing z at the image Node, the lines re1, im1, re2, im2 of both levels."""
    count = len(image)
    out: list[Line] = [([Fraction(0)] * count, [Fraction(0)] * count) for _ in range(4)]
    for i in range(count):
        for level in (0, 1):
            z = (
                Gaussian(record[0][level][i], record[1][level][i]),
                Gaussian(record[2][level][i], record[3][level][i]),
            )
            for a in range(2):
                w = mixing[a][0] * z[0] + mixing[a][1] * z[1]
                out[2 * a][level][image[i]], out[2 * a + 1][level][image[i]] = w.re, w.im
    return out


def axis_vectors(re1, im1, re2, im2) -> list[tuple[Fraction, Fraction, Fraction]]:
    """The record's axis vector at every Node, n_a = z^dagger sigma_a z over the two planes: (2 Re(conj(z_1) z_2), 2 Im(conj(z_1) z_2), |z_1|^2 - |z_2|^2)."""
    found = []
    for a, b, c, d in zip(re1, im1, re2, im2, strict=True):
        z_1, z_2 = Gaussian(a, b), Gaussian(c, d)
        cross = z_1.conj() * z_2
        found.append((2 * cross.re, 2 * cross.im, z_1.abs2() - z_2.abs2()))
    return found


def momentum_density(
    arrivals: Sequence[Sequence[int]], now: Sequence[Sequence], before: Sequence[Sequence]
) -> list[tuple[Fraction, Fraction, Fraction]]:
    """The record's lattice momentum density at every Node, P_a(i) = SUM over the four lines of (F_(i, i-a) - F_(i, i+a)) / num with F from rule3.link_current (row 5 of The conventions and the units): a spatial vector of the record, unchanged by a unitary mixing of its planes and carried by the Node map alone."""
    found = []
    for i, ports in enumerate(arrivals):
        components = []
        for a in range(3):
            total = Fraction(0)
            for line_now, line_before in zip(now, before, strict=True):
                total += rule3.link_current(
                    1,
                    line_now[i],
                    line_before[i],
                    line_now[ports[2 * a + 1]],
                    line_before[ports[2 * a + 1]],
                )
                total -= rule3.link_current(
                    1, line_now[i], line_before[i], line_now[ports[2 * a]], line_before[ports[2 * a]]
                )
            components.append(total)
        found.append((components[0], components[1], components[2]))
    return found


def carried_as_a_vector(
    before: Sequence[tuple[Fraction, Fraction, Fraction]],
    after: Sequence[tuple[Fraction, Fraction, Fraction]],
    image: Sequence[int],
    rotation: Sequence[Sequence[int]],
) -> bool:
    """Whether the axis vector turned as a vector: after[g x] = R before[x] at every Node, R the signed permutation that maps the Nodes."""
    return all(
        after[image[i]] == tuple(sum(rotation[b][a] * before[i][a] for a in range(3)) for b in range(3))
        for i in range(len(image))
    )


def step_two_planes(
    arrivals: Sequence[Sequence[int]],
    levels: Sequence[Sequence[int]],
    remainders: Sequence[Sequence[int]],
    num: int,
    den: int,
    gamma: int,
) -> tuple[list[list[int]], list[list[int]]]:
    """rule3.step on the four lines of a two-plane record, the levels now in the first four rows and before in the last four."""
    new_levels, new_rem = [list(row) for row in levels], []
    for line in range(4):
        out = [
            rule3.step(
                levels[line][i],
                levels[4 + line][i],
                [levels[line][j] for j in arrivals[i]],
                num,
                den,
                remainders[line][i],
                gamma,
            )
            for i in range(len(arrivals))
        ]
        new_levels[line], new_levels[4 + line] = [o[0] for o in out], list(levels[line])
        new_rem.append([o[1] for o in out])
    return new_levels, new_rem


def check_the_quarter_turn_of_a_two_plane_record() -> Check:
    """The quarter turn of a two-plane record (ALGEBRA.md at b254f4d2, The direction): the 48 unit quaternions of the cube's rotations, written as Pauli matrices in Gaussian integers over the scales 1, sqrt 2 and 2, turn the three Pauli axes exactly as the 24 signed permutations of determinant 1, two lifts each; up to a common phase a lift is exact in integers iff it is monomial with its two entries in the ratio of a unit (1, -1, i, -i), which holds for the 8 rotations of one axis's dihedral group (the z axis carried to itself), the other 16 have entries of modulus 1 / 2 or 1 / sqrt 2 whose common phase 1 or (1 + i) / sqrt 2 leaves every entry in Z[i] / 2, a halving, and none keeps a 1 / sqrt 2; the quarter turn about z is diag(1 - i, 1 + i) / sqrt 2 = e^(-i pi / 4) diag(1, i), plane 2's (re, im) -> (-im, re), and with the Nodes carried by the same signed permutation that the lift turns the Pauli axes by, the record's axis vector n_a = z^dagger sigma_a z (2 Re(conj(z_1) z_2), 2 Im(conj(z_1) z_2), |z_1|^2 - |z_2|^2) turns as a vector, n'(g x) = R n(x) at every Node, and so does the record's lattice momentum density P_a(i) = SUM over the four lines of (F_(i, i-a) - F_(i, i+a)), P'(g x) = R P(x), which the mixing leaves alone and the Node map carries, so the one R ties the Node map to the mixing (the inverse map, no map or a sign flipped in the mixing breaks it); on the 4 x 4 x 2 box at the vacuum of [2, 3] and [4000, 6000] the turned record, the Nodes carried by the turn and plane 2's re line laid as the negated im line with its remainder complemented, steps under rule3.step to the turn of the stepped record bit for bit over 40 intervals; the quarter turn about x, (1 + i) [[1, -i], [-i, 1]] / 2 after the phase, mixes the planes with a halving, exact under the line without its division on the 5 x 5 x 5 box and off the integers at the Node-lines whose turned level is a half, counted of 500 beside the law's 210. A lift that turned the axes wrongly, a wrong count of the integer lifts, a remainder left uncomplemented or a Node map in the wrong sense breaks the equalities."""
    draw = random.Random(SEED)
    rotations: dict[tuple, list] = {}
    for q in binary_octahedral():
        lift = pauli_lift(*q)
        rotation, norm = rotation_of(lift)
        rotations.setdefault(rotation, []).append((norm, lift))
    if len(rotations) != 24 or any(len(lifts) != 2 for lifts in rotations.values()):
        return False, {"rotations": len(rotations)}
    for rotation in rotations:
        entries = [abs(e) for row in rotation for e in row]
        if entries.count(1) != 3 or determinant([[Fraction(e) for e in row] for row in rotation]) != 1:
            return False, {"rotation": rotation, "failed": "a signed permutation of determinant 1"}
    kinds = {"integer": 0, "halving": 0, "root two": 0}
    dihedral = 0
    units = (Gaussian(1), Gaussian(-1), Gaussian(0, 1), Gaussian(0, -1))
    for rotation, lifts in rotations.items():
        found = set()
        for norm, lift in lifts:
            moduli = [lift[i][j].abs2() for i in range(2) for j in range(2)]
            if all(m in (0, norm) for m in moduli):
                nonzero = [lift[i][j] for i in range(2) for j in range(2) if lift[i][j].abs2()]
                found.add("integer" if nonzero[0] / nonzero[1] in units else "root two")
            else:
                phase = Gaussian(1) if norm == 4 else Gaussian(1, 1)  # 2 e^(i phi) U = phase x U_int
                halves = [phase * lift[i][j] for i in range(2) for j in range(2)]
                integral = all(h.re.denominator == 1 and h.im.denominator == 1 for h in halves)
                found.add("halving" if integral and norm in (2, 4) else "root two")
        if len(found) != 1:
            return False, {"rotation": rotation, "lifts": found}
        kind = found.pop()
        kinds[kind] += 1
        dihedral += kind == "integer" and abs(rotation[2][2]) == 1
    z_lifts = [lift for _n, lift in rotations.get(ABOUT_Z, []) if lift[0][0] == Gaussian(1, -1)]
    x_lifts = [lift for _n, lift in rotations.get(ABOUT_X, []) if lift[0][0] == Gaussian(1)]
    if len(z_lifts) != 1 or len(x_lifts) != 1:
        return False, {"lifts of the quarter turns about z and x": (len(z_lifts), len(x_lifts))}
    half_phase = Gaussian(
        Fraction(1, 2), Fraction(1, 2)
    )  # (1 + i) / 2: the phase e^(i pi / 4) over sqrt 2
    z_mixing = [[half_phase * z_lifts[0][i][j] for j in range(2)] for i in range(2)]
    x_mixing = [[half_phase * x_lifts[0][i][j] for j in range(2)] for i in range(2)]
    z_turn_is_diag_1_i = z_mixing == [[Gaussian(1), Gaussian(0)], [Gaussian(0), Gaussian(0, 1)]]
    one_plus_i, one_minus_i = half_phase, Gaussian(Fraction(1, 2), Fraction(-1, 2))
    x_is_a_halving = x_mixing == [[one_plus_i, one_minus_i], [one_minus_i, one_plus_i]]
    if not (z_turn_is_diag_1_i and x_is_a_halving):
        return False, {"z mixing": z_mixing, "x mixing": x_mixing}
    shape = (4, 4, 2)
    arrivals, image = box_arrivals(shape), box_map(shape, ABOUT_Z)
    count = len(arrivals)
    bit_for_bit, z_vector = 0, True
    for num, den in ((2, 3), (4000, 6000)):
        gamma = 6000
        wall = 6 * den * gamma * gamma
        levels = [[draw.randint(-1000, 1000) for _ in range(count)] for _ in range(8)]
        remainders = [[draw.randint(0, wall - 1) for _ in range(count)] for _ in range(4)]
        t_levels, t_rem = monomial_turn(z_mixing, levels, remainders, image, wall)
        for half in (0, 4):
            z_vector &= carried_as_a_vector(
                axis_vectors(*levels[half : half + 4]),
                axis_vectors(*t_levels[half : half + 4]),
                image,
                ABOUT_Z,
            )
        z_vector &= carried_as_a_vector(
            momentum_density(arrivals, levels[:4], levels[4:]),
            momentum_density(arrivals, t_levels[:4], t_levels[4:]),
            image,
            ABOUT_Z,
        )
        for _ in range(40):
            levels, remainders = step_two_planes(arrivals, levels, remainders, num, den, gamma)
            t_levels, t_rem = step_two_planes(arrivals, t_levels, t_rem, num, den, gamma)
            if (t_levels, t_rem) != monomial_turn(z_mixing, levels, remainders, image, wall):
                return False, {"pair": (num, den), "failed": "the z turn to the bit"}
            bit_for_bit += 1
        z_vector &= carried_as_a_vector(
            axis_vectors(*levels[:4]), axis_vectors(*t_levels[:4]), image, ABOUT_Z
        )
    shape = (5, 5, 5)
    arrivals, image = box_arrivals(shape), box_map(shape, ABOUT_X)
    count = len(arrivals)
    line = read(arrivals, [1] * count, [[1] * PORTS] * count, 2, 3, 1)
    record = [random_line(draw, count, 1000) for _ in range(4)]  # re1, im1, re2, im2
    turned_record = mixed(x_mixing, record, image)
    x_vector = all(
        carried_as_a_vector(
            axis_vectors(*(u[level] for u in record)),
            axis_vectors(*(u[level] for u in turned_record)),
            image,
            ABOUT_X,
        )
        for level in (0, 1)
    )
    x_vector &= carried_as_a_vector(
        momentum_density(arrivals, [u[0] for u in record], [u[1] for u in record]),
        momentum_density(arrivals, [u[0] for u in turned_record], [u[1] for u in turned_record]),
        image,
        ABOUT_X,
    )
    halves = sum(1 for part in turned_record for x in part[0] if x.denominator == 2)
    x_exact_in_rationals = [stepped(arrivals, line, u) for u in turned_record] == mixed(
        x_mixing, [stepped(arrivals, line, u) for u in record], image
    )
    held = (
        kinds == {"integer": 8, "halving": 16, "root two": 0}
        and dihedral == 8
        and z_vector
        and x_vector
        and x_exact_in_rationals
        and halves > 0
    )
    return held, {
        "rotations and lifts": (len(rotations), sum(len(v) for v in rotations.values())),
        "lifts exact in integers, needing a halving, keeping a 1 / sqrt 2": (
            kinds["integer"],
            kinds["halving"],
            kinds["root two"],
        ),
        "integer lifts carrying the z axis to itself, one axis's dihedral group": dihedral,
        "the z quarter turn is (1 - i) diag(1, i)": z_turn_is_diag_1_i,
        "the axis vector and the momentum density carried as vectors, z turn and x turn": (
            z_vector,
            x_vector,
        ),
        "z turn to the bit, intervals at two pairs": bit_for_bit,
        "the x turn after the phase (1 + i) [[1, -i], [-i, 1]] / 2": x_is_a_halving,
        "x turn exact in the rationals": x_exact_in_rationals,
        "Node-lines the halving leaves off the integers, of 500 (the law's lay 210)": halves,
    }


def cycle_of_the_third(lines: Sequence[Sequence[int]]) -> list[list[int]]:
    """(L_0, L_1, L_2) -> (L_2, L_0, L_1), the 3-cycle of three lines of [-1, 2]."""
    return [list(lines[2]), list(lines[0]), list(lines[1])]


def signed_cycle(lines: Sequence[Sequence[int]]) -> list[list[int]]:
    """(L_0, L_1, L_2) -> (-L_2, L_0, L_1), the signed 3-cycle of three lines of [1, 2]."""
    return [[-x for x in lines[2]], list(lines[0]), list(lines[1])]


def quarter_of_the_plane(lines: Sequence[Sequence[int]]) -> list[list[int]]:
    """(re, im) -> (-im, re), the plane of [0, 1]."""
    return [[-x for x in lines[1]], list(lines[0])]


def check_the_exact_bands_integer_rotations() -> Check:
    """The exact bands, the integer rotations (ALGEBRA.md at b254f4d2, A family's declaration): at the vacuum the one-Node line a_next = 2 cos omega_0 a_now - a_before is exact in integers at the three exact pairs (row L07), so on the 2 x 2 x 2 box rule3.step turns three uniform lines of [-1, 2] laid as the third's phases (1000, -500, -500), L_m(t) = s(t - m) with s of period 3, by the 3-cycle (L_0, L_1, L_2) -> (L_2, L_0, L_1) with remainder 0 at every Node, three lines of [1, 2] laid on s of period 6 by the signed 3-cycle (-L_2, L_0, L_1), and a plane of [0, 1] by (re, im) -> (-im, re), each over 30 intervals to the bit; the lines' cycle is the uniform lay's identity and no act of the step, a random lay of three lines of [-1, 2] on the 5 x 5 x 5 box stepping off the cycle at most of its 375 Node-lines (the count recomputed beside the law's 374); the cube's C3, (x, y, z) -> (y, z, x), commutes with rule3.step on every lay of the 5 x 5 x 5 box at [-1, 2] and [2, 3], random levels and remainders carried to the image Nodes bit for bit; and the cycle's matrix P has P^3 = I, det P = 1 and the characteristic polynomial x^3 - 1 with three distinct roots, a regular element of SU(3) in a maximal torus (a Cartan element) and no scalar, so not in the centre, while the Node map has order 3 too, one group of order 3 in two actions. A nonzero remainder, a lay off the phases, a pair off the exact three or a cycle in the wrong sense breaks the equalities."""
    shape = (2, 2, 2)
    arrivals = box_arrivals(shape)
    count, gamma = len(arrivals), 6000
    third, sixth = [1000, -500, -500], [1000, 500, -500, -1000, -500, 500]
    lays = {
        (-1, 2): (
            [[third[(-m) % 3]] * count for m in range(3)],
            [[third[(-1 - m) % 3]] * count for m in range(3)],
            cycle_of_the_third,
        ),
        (1, 2): (
            [[sixth[(-m) % 6]] * count for m in range(3)],
            [[sixth[(-1 - m) % 6]] * count for m in range(3)],
            signed_cycle,
        ),
        (0, 1): ([[1000] * count, [0] * count], [[0] * count, [-1000] * count], quarter_of_the_plane),
    }
    cycles = {}
    for num, den in EXACT_PAIRS:
        if Fraction(2 * num, den).denominator != 1:
            return False, {"pair": (num, den)}
        lines, before, cycle = lays[(num, den)]
        remainders = [[0] * count for _ in lines]
        intervals = 0
        for _ in range(30):
            expected = cycle(lines)
            new_lines, new_remainders = [], []
            for line, line_before, rem in zip(lines, before, remainders, strict=True):
                out = [
                    rule3.step(
                        line[i], line_before[i], [line[j] for j in arrivals[i]], num, den, rem[i], gamma
                    )
                    for i in range(count)
                ]
                new_lines.append([o[0] for o in out])
                new_remainders.append([o[1] for o in out])
            if new_lines != expected or any(any(r) for r in new_remainders):
                return False, {
                    "pair": (num, den),
                    "interval": intervals,
                    "failed": "the cycle with remainder 0",
                }
            before, lines, remainders = lines, new_lines, new_remainders
            intervals += 1
        cycles[f"[{num}, {den}]"] = intervals
    draw = random.Random(SEED)
    shape = (5, 5, 5)
    arrivals = box_arrivals(shape)
    count = len(arrivals)
    lines = [[draw.randint(-1000, 1000) for _ in range(count)] for _ in range(3)]
    before = [[draw.randint(-1000, 1000) for _ in range(count)] for _ in range(3)]
    stepped_lines = [
        [
            rule3.step(line[i], line_before[i], [line[j] for j in arrivals[i]], -1, 2, 0, gamma)[0]
            for i in range(count)
        ]
        for line, line_before in zip(lines, before, strict=True)
    ]
    off_the_cycle = sum(
        1
        for line, expected in zip(stepped_lines, cycle_of_the_third(lines), strict=True)
        for a, b in zip(line, expected, strict=True)
        if a != b
    )
    image = box_map(shape, BODY_DIAGONAL)
    order, composed = 1, list(image)
    while composed != list(range(count)):
        composed = [image[i] for i in composed]
        order += 1
    commuted = 0
    for num, den in ((-1, 2), (2, 3)):
        wall = 6 * den * gamma * gamma
        now = [draw.randint(-1000, 1000) for _ in range(count)]
        before_levels = [draw.randint(-1000, 1000) for _ in range(count)]
        remainders = [draw.randint(0, wall - 1) for _ in range(count)]
        plain = [
            rule3.step(
                now[i], before_levels[i], [now[j] for j in arrivals[i]], num, den, remainders[i], gamma
            )
            for i in range(count)
        ]
        moved_now, moved_before, moved_rem = [0] * count, [0] * count, [0] * count
        for i in range(count):
            moved_now[image[i]], moved_before[image[i]], moved_rem[image[i]] = (
                now[i],
                before_levels[i],
                remainders[i],
            )
        moved = [
            rule3.step(
                moved_now[i],
                moved_before[i],
                [moved_now[j] for j in arrivals[i]],
                num,
                den,
                moved_rem[i],
                gamma,
            )
            for i in range(count)
        ]
        if any(moved[image[i]] != plain[i] for i in range(count)):
            return False, {"pair": (num, den), "failed": "the C3 against the step"}
        commuted += 1
    p = [
        [Fraction(0), Fraction(0), Fraction(1)],
        [Fraction(1), Fraction(0), Fraction(0)],
        [Fraction(0), Fraction(1), Fraction(0)],
    ]

    def product_of(a: Matrix, b: Matrix) -> Matrix:
        return [[sum(a[i][k] * b[k][j] for k in range(3)) for j in range(3)] for i in range(3)]

    identity = [[Fraction(int(i == j)) for j in range(3)] for i in range(3)]
    squared = product_of(p, p)
    trace = sum(p[i][i] for i in range(3))
    minors = sum(p[a][a] * p[b][b] - p[a][b] * p[b][a] for a in range(3) for b in range(a + 1, 3))
    cartan = (
        product_of(squared, p) == identity
        and determinant(p) == 1
        and (trace, minors) == (0, 0)
        and p != identity
        and squared != identity
    )
    held = len(cycles) == 3 and off_the_cycle > 0 and order == 3 and commuted == 2 and cartan
    return held, {
        "intervals cycled to the bit with remainder 0, per exact pair": cycles,
        "Node-lines of a random lay off the cycle, of 375 (the law's lay 374)": off_the_cycle,
        "order of the cube's C3 on the box": order,
        "pairs at which the C3 commutes with the step bit for bit": commuted,
        "the cycle's matrix: P^3 = I, det 1, characteristic polynomial x^3 - 1, no scalar": cartan,
    }


def expectation(
    kernel: Sequence[Sequence[Fraction]], orbital_1, spin_1: int, orbital_2, spin_2: int
) -> tuple[Fraction, Fraction]:
    """<Psi| V |Psi> and <Psi|Psi> for Psi = chi_1(1) chi_2(2) - chi_2(1) chi_1(2), chi_k = orbital_k x spin_k, summed over the positions and the spins of both electrons, the state checked antisymmetric under the exchange of the two electrons at every term."""
    positions = range(len(kernel))

    def amplitude(x1: int, s1: int, x2: int, s2: int) -> Fraction:
        return orbital_1[x1] * (s1 == spin_1) * orbital_2[x2] * (s2 == spin_2) - orbital_2[x1] * (
            s1 == spin_2
        ) * orbital_1[x2] * (s2 == spin_1)

    energy, norm = Fraction(0), Fraction(0)
    for x1, s1, x2, s2 in product(positions, (0, 1), positions, (0, 1)):
        value = amplitude(x1, s1, x2, s2)
        if value != -amplitude(x2, s2, x1, s1):
            raise ValueError("the two-electron state is not antisymmetric under the exchange")
        norm += value * value
        energy += value * value * kernel[x1][x2]
    return energy, norm


def coulomb(kernel: Sequence[Sequence[Fraction]], a, b) -> Fraction:
    """J_ab = SUM_xy a(x)^2 V(x, y) b(y)^2, one cloud in the other's field."""
    positions = range(len(kernel))
    return sum(a[x] ** 2 * kernel[x][y] * b[y] ** 2 for x in positions for y in positions)


def exchange(kernel: Sequence[Sequence[Fraction]], a, b) -> Fraction:
    """K_ab = SUM_xy a(x) b(x) V(x, y) a(y) b(y), the exchange integral."""
    positions = range(len(kernel))
    return sum(a[x] * b[x] * kernel[x][y] * a[y] * b[y] for x in positions for y in positions)


def check_the_hartree_fock_identity_of_the_closed_shell() -> Check:
    """The Hartree-Fock identity of The nucleon is a compact body of its family (ALGEBRA.md at b254f4d2, The hypotheses under their own names): in the 1s^2 singlet the opposite-spin exchange vanishes and the self-exchange cancels the self-Hartree that No record reads its own write of the sign removes, so the mean field without exchange in which each electron reads the other's cloud alone is the Hartree-Fock energy itself, and helium's -2.8617 against -2.9037 hartree (the quantum-chemical numbers, taken as input) leaves 1.4 percent, the correlation alone. Checked exactly in Fractions on random positions, orbitals and symmetric kernels V(x, y): the antisymmetrised two-electron state's expectation of V summed over positions and spins is J / N^2 for two electrons of opposite spin in one orbital phi (J = SUM phi^2 V phi^2, N = SUM phi^2), equal to (2 J - K) / N^2 with the self-exchange K = J and to the pair's mutual energy, and apart from the self-read mean field 2 J / N^2 by the self-Hartree J / N^2; two orbitals of parallel spin carry (J_ab - K_ab) / (N_a N_b - S_ab^2), the exchange present, and of opposite spin J_ab / (N_a N_b), the exchange gone; the same orbital with parallel spins is the zero state. A spin factor misplaced in the exchange, a spin label swapped (the state no longer antisymmetric), a self-read kept or a zero norm returns False; the percent is the two numbers' quotient."""
    draw = random.Random(SEED)
    cases = 0
    while cases < 12:
        positions = draw.randint(3, 6)
        kernel = [[Fraction(0)] * positions for _ in range(positions)]
        for x in range(positions):
            for y in range(x, positions):
                kernel[x][y] = kernel[y][x] = Fraction(draw.randint(1, 9), draw.randint(1, 4))
        phi = [Fraction(draw.randint(-9, 9)) for _ in range(positions)]
        chi = [Fraction(draw.randint(-9, 9)) for _ in range(positions)]
        if not any(phi) or not any(chi) or exchange(kernel, phi, chi) == 0:
            continue
        n_phi, n_chi = sum(x * x for x in phi), sum(x * x for x in chi)
        overlap = sum(a * b for a, b in zip(phi, chi, strict=True))
        try:
            energy, norm = expectation(kernel, phi, 0, phi, 1)
            singlet = energy / norm
            parallel_energy, parallel_norm = expectation(kernel, phi, 0, chi, 0)
            energy_opposite, norm_opposite = expectation(kernel, phi, 0, chi, 1)
            parallel_measured = parallel_energy / parallel_norm
            opposite_measured = energy_opposite / norm_opposite
        except (ValueError, ZeroDivisionError) as reason:
            return False, {"orbitals": (phi, chi), "failed": str(reason)}
        self_coulomb = coulomb(kernel, phi, phi)
        mutual = self_coulomb / n_phi**2
        hartree_fock = (2 * self_coulomb - exchange(kernel, phi, phi)) / n_phi**2
        self_read = 2 * self_coulomb / n_phi**2
        if (
            singlet != mutual
            or singlet != hartree_fock
            or exchange(kernel, phi, phi) != self_coulomb
            or self_read - singlet != self_coulomb / n_phi**2
            or self_read == singlet
        ):
            return False, {"orbital": phi, "failed": "the singlet of one orbital"}
        parallel = (coulomb(kernel, phi, chi) - exchange(kernel, phi, chi)) / (
            n_phi * n_chi - overlap**2
        )
        if parallel_measured != parallel or opposite_measured != coulomb(kernel, phi, chi) / (
            n_phi * n_chi
        ):
            return False, {"orbitals": (phi, chi), "failed": "the exchange of two orbitals"}
        if expectation(kernel, phi, 0, phi, 0) != (0, 0):
            return False, {"orbital": phi, "failed": "the parallel pair in one orbital"}
        cases += 1
    hartree_fock_helium, exact_helium = -2.8617, -2.9037
    percent = (exact_helium - hartree_fock_helium) / exact_helium * 100
    return round(percent, 1) == 1.4, {
        "random cases of positions, orbitals and kernels": cases,
        "the singlet of one orbital": "J / N^2 = (2 J - K) / N^2, the self-read mean field 2 J / N^2 apart by J / N^2",
        "two orbitals": "parallel spins (J - K) / (N_a N_b - S^2), opposite spins J / (N_a N_b)",
        "helium's correlation, percent of the exact energy": round(percent, 2),
    }


if __name__ == "__main__":
    sys.exit(run(sys.modules[__name__]))
