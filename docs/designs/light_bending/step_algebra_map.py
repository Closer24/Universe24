"""The step algebra's simulation of the board for light beside a mass under
the key `optical` (the Bending Algebraist, 2026-09-22; the owner's order
of record 838's session, "an algebra of steps can simulate a board";
docs/designs/light_bending/STEP_ALGEBRA.md).

Integers only, no engine import, nothing run on the engine: the six verbs
of the key's three rules are transcribed from `src/event_universe/events/
nature_beam.py` on main (the walk `optical_walk_step`, the wall
`core.integer.age_wall`, the push and the label `optical_turn`, the pair of
a pushed row `momentum_pair`, the weight `unit_weights`, the neighbour
table `fan_neighbours`, the digital line `world.bresenham_line`, the label
`unit_label`) and applied interval by interval to ONE row of light on each
of series K's five beam lines, on the stationary crowd of series K's mass
(the same lines the engine walks, one row per direction per interval,
16 units at M = 2^16). The reading is the arrival Node on the screen of
Nodes (every Node of the screen a detector, record 721), the shift between
the world and its control, and the click's age against the control's:
THE STEP ALGEBRA'S SIMULATION OF THE BOARD, NOT A RUN, never a measurement
of nature. The pins are declared in STEP_ALGEBRA.md before this file's
arithmetic.

    python docs/designs/light_bending/step_algebra_map.py > docs/designs/light_bending/step_algebra_map.out
"""

from __future__ import annotations

import functools
import math
from collections import defaultdict
from fractions import Fraction

Q = 64  # the label's scale (BEAM_LAW section 2; TERMINOLOGY N_l)
PAIR = (1, 16384)  # the optical worlds' `suspension` [n, d] (examples/events/optical/*.json)
FAN_BOUND = 6  # series K's fan: primitive directions with |a| + |b| + |c| <= 6 (290)
BEAM = ((1, 0, 0), (24, 1, 0), (24, -1, 0), (12, 1, 0), (12, -1, 0))  # lensing/make_worlds.py
HEADINGS = ((1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1))  # PORT_HEADINGS
X_LAMP, X_SCREEN = -26, 26  # the lamp at x = 2, the mass at 28, the screen at 54 (shape 57)
BOX = ((-26, 28), (-20, 20), (-20, 20))  # the box 57 x 41 x 41 about the mass at (28, 20, 20)
FAN_NEIGHBOURS = 6
SOURCE = 4096  # the mass's `release` [1, 4096]: M / 4096 units per direction per interval
LINKS = 80  # the crowd's lines followed this far (the box's Manhattan radius is 68)
Vector = tuple[int, int, int]


def primitive_fan(bound: int) -> list[Vector]:
    found = []
    for a in range(-bound, bound + 1):
        for b in range(-bound, bound + 1):
            for c in range(-bound, bound + 1):
                if (a or b or c) and abs(a) + abs(b) + abs(c) <= bound:
                    if math.gcd(math.gcd(abs(a), abs(b)), abs(c)) == 1:
                        found.append((a, b, c))
    found.sort()
    return found


def unit_label(vector: Vector) -> Vector:
    """nature_beam.unit_label: the integer vector nearest Q D / |D|."""
    n = sum(c * c for c in vector)
    if n == 0:
        return (0, 0, 0)
    found = []
    for a in vector:
        t = 2 * Q * abs(a)
        k = (math.isqrt(t * t // n) + 1) // 2
        found.append(k if a >= 0 else -k)
    return (found[0], found[1], found[2])


def bresenham_line(vector: Vector) -> list[Vector]:
    """world.bresenham_line: the S_1 unit steps of one period, the axis
    furthest behind first, the lowest axis first."""
    s1 = sum(abs(c) for c in vector)
    line: list[Vector] = []
    position = [0, 0, 0]
    for j in range(s1):
        best = max(range(3), key=lambda i: (abs(vector[i]) * (j + 1) - s1 * abs(position[i]), -i))
        step = [0, 0, 0]
        step[best] = 1 if vector[best] > 0 else -1
        position[best] += step[best]
        line.append((step[0], step[1], step[2]))
    return line


def fan_neighbours(vectors: list[Vector]) -> list[list[int]]:
    """nature_beam.fan_neighbours: per direction its six nearest moving
    directions within a right angle by the exact comparison of cosines,
    ties by index."""
    norms = [sum(c * c for c in v) for v in vectors]
    table: list[list[int]] = []
    for index, vector in enumerate(vectors):
        if norms[index] == 0:
            table.append([])
            continue
        candidates = []
        for other, candidate in enumerate(vectors):
            if other == index or norms[other] == 0:
                continue
            dot = sum(a * b for a, b in zip(vector, candidate, strict=True))
            if dot <= 0:
                continue
            candidates.append((dot, norms[other], other))

        def nearer(left: tuple[int, int, int], right: tuple[int, int, int]) -> int:
            lhs = left[0] * left[0] * right[1]
            rhs = right[0] * right[0] * left[1]
            if lhs != rhs:
                return -1 if lhs > rhs else 1
            return -1 if left[2] < right[2] else (1 if left[2] > right[2] else 0)

        candidates.sort(key=functools.cmp_to_key(nearer))
        table.append([other for _, _, other in candidates[:FAN_NEIGHBOURS]])
    return table


def in_box(node: tuple[int, int, int]) -> bool:
    return all(lo <= c <= hi for c, (lo, hi) in zip(node, BOX, strict=True))


class Table:
    """The world's direction table as the loader builds it (world.py:1449:
    two rest slots, the six headings, then the declared list: series K's
    fan without its headings, then the beam's four), with Flight's tables
    per direction: S_1, T_D = isqrt(3 |D|^2 Q^2), the line, the label u_D,
    the energy e_D = isqrt(3 u_D . u_D), the weight per unit at gamma
    (`unit_weights`: (e_D^2 + 3 gamma u_D . u_D) // e_D) and the neighbours."""

    def __init__(self, fan: list[Vector], beam: tuple[Vector, ...], gamma: int) -> None:
        declared = [v for v in fan if v not in HEADINGS] + [v for v in beam if v not in HEADINGS]
        self.vectors: list[Vector] = [(0, 0, 0), (0, 0, 0), *HEADINGS, *declared]
        self.index = {v: i for i, v in enumerate(self.vectors) if i >= 2}
        self.s1 = [sum(abs(c) for c in v) for v in self.vectors]
        self.t = [math.isqrt(3 * sum(c * c for c in v) * Q * Q) for v in self.vectors]
        self.lines = [bresenham_line(v) if s else [] for v, s in zip(self.vectors, self.s1, strict=True)]
        self.labels = [unit_label(v) for v in self.vectors]
        self.energy = [math.isqrt(3 * sum(c * c for c in u)) for u in self.labels]
        self.weight = [
            ((e * e + 3 * gamma * sum(c * c for c in u)) // e if e else 0)
            for e, u in zip(self.energy, self.labels, strict=True)
        ]
        self.neighbours = fan_neighbours(self.vectors)


def manhattan_steps(tau: int, s1: int, t: int) -> int:
    """m(tau) = (2 tau S_1 Q + T_D) // (2 T_D): the Links made by age tau (BEAM_LAW 359-402)."""
    return (2 * tau * s1 * Q + t) // (2 * t)


def age_of(made: int, s1: int, t: int) -> int:
    """The first age at which m(tau) >= made."""
    return max(0, -(-(made * 2 * t - t) // (2 * s1 * Q)))


class Crowd:
    """The stationary crowd of the mass at the origin: one row of amount
    `scale` per direction of the fan per interval (M = scale x 4096 at
    `release` [1, 4096]), each walking its line by the flight rule. Per
    Node inside the box: the age moment A = sum amount x age over the rows
    present there at the end of an interval (the ages tau with m(tau) =
    the Node's Link), and the arrival flow V = sum amount x u_D over the
    rows that arrive there in an interval (one per line per interval);
    both exact integers, the same every interval once the oldest row that
    reaches the Node has been born (the ages at the beam's Nodes are below
    60, so from tick 60 on; the window of the register begins at 110)."""

    def __init__(self, fan: list[Vector], scale: int) -> None:
        self.age_moment: dict[Vector, int] = defaultdict(int)
        self.flow: dict[Vector, list[int]] = defaultdict(lambda: [0, 0, 0])
        self.presence: dict[Vector, int] = defaultdict(int)
        self.lines_through: dict[Vector, int] = defaultdict(int)
        for vector in fan:
            s1 = sum(abs(c) for c in vector)
            t = math.isqrt(3 * sum(c * c for c in vector) * Q * Q)
            steps = bresenham_line(vector)
            label = unit_label(vector)
            node = [0, 0, 0]
            for made in range(1, LINKS + 1):
                step = steps[(made - 1) % s1]
                node = [node[i] + step[i] for i in range(3)]
                key = (node[0], node[1], node[2])
                if not in_box(key):
                    break
                ages = range(age_of(made, s1, t), age_of(made + 1, s1, t))
                self.age_moment[key] += scale * sum(ages)
                self.presence[key] += scale * len(ages)
                self.lines_through[key] += 1
                for i in range(3):
                    self.flow[key][i] += scale * label[i]


def momentum_pair(momentum: list[int]) -> tuple[int, int]:
    """nature_beam.momentum_pair for the photon (the rest term 0): (S_1, T)
    of P over the gcd of its components."""
    g = math.gcd(*momentum)
    primitive = [c // g for c in momentum]
    return sum(abs(c) for c in primitive), math.isqrt(3 * sum(c * c for c in primitive) * Q * Q)


def cross_product(h: Vector, p: list[int]) -> list[int]:
    return [h[1] * p[2] - h[2] * p[1], h[2] * p[0] - h[0] * p[2], h[0] * p[1] - h[1] * p[0]]


def walk(
    table: Table,
    crowd: Crowd | None,
    start: Vector,
    b: int,
    z: int,
    gamma: int,
    coefficient: int | None = None,
) -> dict[str, object]:
    """One row of light born at the lamp (X_LAMP, b, z) on the beam line
    `start`, walked by the key's three rules interval by interval exactly
    as `nature_beam.py` walks it (content 1, amount 1: the push and the
    momentum both scale with the content, so the turn is the same for any
    content): (1) the walk, the accumulator at the rate 2 S_1 Q d against
    the wall 2 T (d + f n A) with A the crowd's age moment at the row's
    Node, one Link at most, the Link the label's line step at the place
    made mod S_1, the error accumulator c += h x P on a pushed row; (2) the
    push at the Node reached, W -= n x weight x V, the residue rescaled by
    S_1(P') / S_1(P); (3) the label among D and its fan neighbours whose
    next Link keeps |c + h x P|^2 smallest, P conserved. The click: the
    arrival Node on the screen x = X_SCREEN and the row's age there; a row
    that reaches the mass's Node is measured by the mass (the paid family's
    default table rule `measure`, `world.default_rule` :855 and
    `default_table` :868, ENGINE.md :671: the registered mass declares no
    table; the engine pushes and turns nothing at that occupied Node); one
    that leaves the box escapes through a face.
    `coefficient` overrides f = 1 + gamma on the wall (the wall unstretched
    at 0, a reading that would refute verb 1)."""
    n, d = PAIR
    f = 1 + gamma if coefficient is None else coefficient
    direction = table.index[start]
    node = [X_LAMP, b, z]
    made = 0
    pushed = False
    w_acc = [0, 0, 0]
    cross = [0, 0, 0]
    residue = table.t[direction] * d  # the fresh row's accumulator (0, T_D) at age 0, times d
    age = 0
    label_scale = Q * d  # Q d content at content 1
    p0 = [label_scale * c for c in table.labels[direction]]
    stretch_total = 0

    def momentum(dir_index: int) -> list[int]:
        return [label_scale * table.labels[dir_index][i] + w_acc[i] for i in range(3)]

    def pair(dir_index: int) -> tuple[int, int]:
        if not pushed:
            return 2 * table.s1[dir_index] * Q, 2 * table.t[dir_index]
        s1, t = momentum_pair(momentum(dir_index))
        return 2 * s1 * Q, 2 * t

    while True:
        age += 1
        # Verb 1: the walk against the wall the crowd's age moment stretches.
        a = crowd.age_moment.get((node[0], node[1], node[2]), 0) if crowd else 0
        rate0, wall0 = pair(direction)
        rate, wall = rate0 * d, wall0 * (d + f * n * a)
        stretch_total += f * n * a
        residue += rate
        moved = min(residue // wall, 1)
        residue -= moved * wall
        if moved:
            h = table.lines[direction][made % table.s1[direction]]
            if pushed:
                p = momentum(direction)
                cross = [c + e for c, e in zip(cross, cross_product(h, p), strict=True)]
            made += 1
            node = [node[i] + h[i] for i in range(3)]
            key = (node[0], node[1], node[2])
            if node[0] >= X_SCREEN:
                p = momentum(direction)
                tangent = Fraction(
                    -(p0[0] * p[1] - p0[1] * p[0]), p0[0] * p[0] + p0[1] * p[1] + p0[2] * p[2]
                )
                return {
                    "node": key,
                    "age": age,
                    "exact_age": age - Fraction(residue, rate),
                    "made": made,
                    "momentum": p,
                    "tangent": tangent,
                    "label": table.vectors[direction],
                    "stretch": Fraction(stretch_total, d),
                }
            if key == (0, 0, 0):
                return {"node": key, "age": age, "taken": True}
            if not in_box(key):
                return {"node": key, "age": age, "escaped": True}
        if crowd is None or (node[0], node[1], node[2]) == (X_LAMP, b, z):
            # No push and no turn at an occupied Node (`optical_turn` reads
            # the rows of free space only): the lamp's own Node holds the
            # lamp, so a row that does not move in its first walk waits there.
            continue
        # Verb 2: the push at the Node reached, every interval of dwell.
        v = crowd.flow.get((node[0], node[1], node[2]), [0, 0, 0])
        if any(v):
            old_rate = pair(direction)[0]
            weight = table.weight[direction]
            for i in range(3):
                w_acc[i] -= n * weight * v[i]
            pushed = True
            new_rate = pair(direction)[0]
            residue = residue * new_rate // old_rate
        # Verb 3: the label along P, for a row that holds a push.
        if not any(w_acc):
            continue
        p = momentum(direction)
        best, best_error = direction, -1
        for candidate in [direction, *table.neighbours[direction]]:
            h = table.lines[candidate][made % table.s1[candidate]]
            if h[0] * p[0] + h[1] * p[1] + h[2] * p[2] <= 0:
                continue
            e = [c + x for c, x in zip(cross, cross_product(h, p), strict=True)]
            error = e[0] * e[0] + e[1] * e[1] + e[2] * e[2]
            if best_error < 0 or error < best_error:
                best, best_error = candidate, error
        if best != direction:
            for i in range(3):
                w_acc[i] += label_scale * (table.labels[direction][i] - table.labels[best][i])
            direction = best


def beam_reading(
    table: Table, crowd: Crowd | None, b: int, z: int, gamma: int, coefficient: int | None = None
) -> list[dict[str, object]]:
    return [walk(table, crowd, line, b, z, gamma, coefficient) for line in BEAM]


def fmt_fraction(x: Fraction, digits: int = 4) -> str:
    return f"{float(x):.{digits}f}"


def main() -> None:
    n, d = PAIR
    fan = primitive_fan(FAN_BOUND)
    q_lines = len(fan)
    tables = {gamma: Table(fan, BEAM, gamma) for gamma in (0, 1)}
    control = {}
    print(
        "THE STEP ALGEBRA'S SIMULATION OF THE BOARD, NOT A RUN (docs/designs/light_bending/STEP_ALGEBRA.md)"
    )
    print(
        f"the fan: {q_lines} directions within Manhattan {FAN_BOUND}; the pair [n, d] = [{n}, {d}]; Q = {Q}"
    )
    heading = tables[0].index[(1, 0, 0)]
    print(
        f"the heading's T_D = {tables[0].t[heading]}, e_D = {tables[0].energy[heading]}, the weight per unit "
        f"{tables[0].weight[heading]} at gamma 0 and {tables[1].weight[heading]} at gamma 1; the beam's labels "
        + ", ".join(
            f"{v}: u = {tables[0].labels[tables[0].index[v]]}, e = {tables[0].energy[tables[0].index[v]]}, "
            f"w(1) = {tables[1].weight[tables[1].index[v]]}"
            for v in BEAM
        )
    )
    print()
    print(
        "1. THE CONTROL (no mass): the arrival Node per line, the click's age; the mean age against the register's 89.40"
    )
    for b in (3, 6, 8, 10, 14, 16, 18):
        rows = beam_reading(tables[0], None, b, 0, 0)
        control[b] = rows
        ages = [r["age"] for r in rows]
        print(
            f"   b = {b:2d}: "
            + "; ".join(
                f"{r['label']} -> y = {r['node'][1]:+d} (age {r['age']}, {r['made']} Links)"
                if "label" in r
                else f"{BEAM[k]} -> ESCAPED at {r['node']} (age {r['age']})"
                for k, r in enumerate(rows)
            )
            + f"; the mean age {sum(ages) / 5:.2f}"
        )
    print()

    def world_block(
        title: str, b: int, z: int, scale: int, crowd: Crowd, gammas=(0, 1)
    ) -> dict[int, dict]:
        out = {}
        q = q_lines * scale
        s_pin = Fraction(d, n)  # the pin n S = d
        gm = Fraction(q) / (4 * s_pin)  # G M = q / (4 pi S), the pi kept aside
        a_b = crowd.age_moment.get((0, b, z), 0)
        k_b = Fraction(n * a_b, d)
        print(
            f"   {title}: M = 2^{12 + int(math.log2(scale))} ({scale} units per direction per interval, "
            f"q = {q} units per interval), b = {b}, z = {z}; the crowd at (0, {b}, {z}): A = {a_b} "
            f"(lines through it {crowd.lines_through.get((0, b, z), 0)}), k(b) = n A / d = {fmt_fraction(k_b, 6)}; "
            f"at the pin S = d / n = {s_pin}: G M / c^2 = 3 q / (4 pi S) = {float(3 * gm / math.pi):.6f}, "
            f"G M / (c^2 b) = {float(3 * gm / (math.pi * b)):.6f}"
        )
        base = control[b] if z == 0 else beam_reading(tables[0], None, b, z, 0)
        for gamma in gammas:
            rows = beam_reading(tables[gamma], crowd, b, z, gamma)
            out[gamma] = rows
            kept = [(r, c) for r, c in zip(rows, base, strict=True) if "tangent" in r and "tangent" in c]
            landed = [r for r, _ in kept]
            shifts = [r["node"][1] - c["node"][1] for r, c in kept]
            delays = [r["age"] - c["age"] for r, c in kept]
            exact_delays = [r["exact_age"] - c["age"] for r, c in kept]
            per_line = "; ".join(
                (
                    f"{r['label'] if 'label' in r else ''} -> y = {r['node'][1]:+d}, dy = {r['node'][1] - c['node'][1]:+d}, "
                    f"age {r['age']} ({r['age'] - c['age']:+d}), {r['made']} Links, tan = {fmt_fraction(r['tangent'], 5)}"
                )
                if "tangent" in r and "tangent" in c
                else f"{BEAM[k]} -> {'MEASURED BY THE MASS' if r.get('taken') else 'ESCAPED'} at {r['node']} (age {r['age']})"
                for k, (r, c) in enumerate(zip(rows, base, strict=True))
            )
            print(f"     gamma {gamma} (f = {1 + gamma}): {per_line}")
            if not landed:
                continue
            mean_shift = Fraction(sum(shifts), len(shifts))
            mean_delay = Fraction(sum(delays), len(delays))
            mean_exact = sum(exact_delays, Fraction(0)) / len(exact_delays)
            mean_tan = sum((r["tangent"] for r in landed), Fraction(0)) / len(landed)
            c_pin = mean_tan * b / (3 * gm) * math.pi  # alpha b c^2 / (G M) = tan x b x 4 pi S / (3 q)
            c_lat = mean_tan / k_b if k_b else Fraction(0)
            print(
                f"       the beam ({len(landed)} lines): the mean shift {mean_shift} = {fmt_fraction(mean_shift, 3)} px, "
                f"the mean delay {mean_delay} = {fmt_fraction(mean_delay, 2)} intervals (the exact last Link "
                f"{fmt_fraction(mean_exact, 2)}); the mean tan alpha = {mean_tan} = {fmt_fraction(mean_tan, 5)}; "
                f"alpha b / (26 px): {fmt_fraction(-mean_shift / 26, 5)} rad"
            )
            print(
                f"       C = alpha b c^2 / (G M) at the pin (tan alpha x b x 4 pi S / (3 q)) = {c_pin:.4f} against 4; "
                f"C' = tan alpha / k(b) (exact) = {c_lat} = {fmt_fraction(c_lat, 4)} against 4; "
                f"C from the arrival Nodes (-shift / 26 in place of tan) = "
                f"{float(-mean_shift / 26 * b * 4 * math.pi * s_pin / (3 * q)):.4f}; "
                f"the delay against Shapiro's c_f (n S / d) (G M / c^3) ln(4 L^2 / b^2) = "
                f"{float((1 + gamma) * gm * 3 * math.sqrt(3) / math.pi * math.log(4 * 26 * 26 / (b * b))):.3f}"
            )
        if 0 in out and 1 in out:
            t0 = [r["tangent"] for r in out[0] if "tangent" in r]
            t1 = [r["tangent"] for r in out[1] if "tangent" in r]
            if t0 and t1 and sum(t0):
                ratio = (sum(t1, Fraction(0)) / len(t1)) / (sum(t0, Fraction(0)) / len(t0))
                print(
                    f"       the ratio gamma 1 / gamma 0 of the mean tan alpha: {ratio} = {fmt_fraction(ratio, 4)}"
                )
        return out

    crowd16 = Crowd(fan, 16)
    crowd1 = Crowd(fan, 1)
    print("2. THE CALIBRATION: the registered worlds (examples/events/optical/), M = 2^16 at [1, 16384]")
    world_block("mass (registered -1.993 / -3.989 px, 2.95 / 4.94 intervals)", 6, 0, 16, crowd16)
    world_block("far (registered -1.773 / -3.403 px, 2.56 / 4.33 intervals)", 8, 0, 16, crowd16)
    world_block("near (registered -2.608 / -6.412 px, 2.99 / 6.20 intervals)", 3, 0, 16, crowd16)
    print()
    print("3. THE SIMULATION PER b UNDER THE PIN n S = d (S = 16384), c_f = 2 (gamma 1) beside gamma 0")
    for b in (10, 14, 16, 18):
        world_block(f"b = {b}", b, 0, 16, crowd16)
    print("   M = 2^12 (one unit per direction per interval):")
    for b in (6, 8):
        world_block(f"b = {b}", b, 0, 1, crowd1)
    print()
    print(
        "4. THE WALL ALONE (the push off, a reading that would refute verb 2) and THE PUSH ALONE (the wall unstretched)"
    )
    for b in (6, 8):
        base = control[b]
        rows = beam_reading(tables[1], crowd16, b, 0, 1, coefficient=0)
        shifts = [r["node"][1] - c["node"][1] for r, c in zip(rows, base, strict=True)]
        delays = [r["age"] - c["age"] for r, c in zip(rows, base, strict=True)]
        print(
            f"   b = {b}, gamma 1, the wall unstretched (coefficient 0): the shifts {shifts}, the delays {delays}"
        )
        # the push off: a crowd with the flow zeroed
        quiet = Crowd(fan, 16)
        quiet.flow = defaultdict(lambda: [0, 0, 0])
        rows = beam_reading(tables[1], quiet, b, 0, 1)
        shifts = [r["node"][1] - c["node"][1] for r, c in zip(rows, base, strict=True)]
        delays = [r["age"] - c["age"] for r, c in zip(rows, base, strict=True)]
        print(f"   b = {b}, gamma 1, the push off (V = 0): the shifts {shifts}, the delays {delays}")
    print()
    print(
        "5. THE REASON, SHOWN: the flow's line sum along each beam line against the continuum's, per b (gamma 1, M = 2^16)"
    )
    print(
        "   sum over the row's path of V_y at its Nodes (the push's integrand, label units x dwell) against the"
    )
    print(
        "   continuum's 2 q Q b / (4 pi) x L / (b sqrt(L^2 + b^2)) x (1 / c) per unit path ... stated as the ratio"
    )
    for b in (3, 6, 8, 10, 14, 16, 18):
        row = control[b][0]
        # the heading's path: the Nodes (x, b, 0), x from -26 to 25, the dwell from the flight rule
        s1, t = tables[0].s1[heading], tables[0].t[heading]
        total = 0
        for made in range(0, row["made"]):
            dwell = age_of(made + 1, s1, t) - age_of(made, s1, t)
            total += dwell * crowd16.flow.get((X_LAMP + made, b, 0), [0, 0, 0])[1]
        cont = 2 * q_lines * 16 * Q * 26 / (4 * math.pi * b * math.sqrt(26 * 26 + b * b)) * math.sqrt(3)
        print(
            f"   b = {b:2d}: the heading's path sum of V_y x dwell = {total} (label units x intervals); "
            f"the continuum's {cont:.1f}; the ratio {total / cont:.3f}"
        )
    print()
    print(
        "6. A DENSER FAN AND A BEAM OFF THE PLANE (the reason tested; not a registered world; no pin moved)"
    )
    for bound in (6, 8, 10, 12):
        fan_b = primitive_fan(bound)
        crowd_b = Crowd(fan_b, 16)
        table_b = Table(fan_b, BEAM, 1)
        table_0 = Table(fan_b, BEAM, 0)
        q = len(fan_b) * 16
        gm3 = Fraction(3 * q, 4 * 16384)
        for b in (6, 8):
            base = beam_reading(table_0, None, b, 0, 0)
            rows = beam_reading(table_b, crowd_b, b, 0, 1)
            landed = [r for r in rows if "tangent" in r]
            mean_tan = sum((r["tangent"] for r in landed), Fraction(0)) / max(1, len(landed))
            shifts = [
                r["node"][1] - c["node"][1] for r, c in zip(rows, base, strict=True) if "tangent" in r
            ]
            c_pin = float(mean_tan * b / gm3 * math.pi)
            print(
                f"   P = {bound:2d} ({len(fan_b)} directions, q = {q}), b = {b}, gamma 1: the shifts {shifts}, "
                f"the mean tan alpha {fmt_fraction(mean_tan, 5)}, C = {c_pin:.3f} against 4 "
                f"({len(landed)} of 5 lines landed)"
            )
    for z in (1, 2):
        for b in (6, 8):
            base = beam_reading(tables[0], None, b, z, 0)
            rows = beam_reading(tables[1], crowd16, b, z, 1)
            landed = [r for r in rows if "tangent" in r]
            mean_tan = sum((r["tangent"] for r in landed), Fraction(0)) / max(1, len(landed))
            shifts = [
                r["node"][1] - c["node"][1] for r, c in zip(rows, base, strict=True) if "tangent" in r
            ]
            gm3 = Fraction(3 * q_lines * 16, 4 * 16384)
            r_perp = math.sqrt(b * b + z * z)
            c_pin = float(mean_tan * r_perp / gm3 * math.pi)
            print(
                f"   P = 6, the beam {z} Node off the plane, b = {b} (the distance {r_perp:.2f}), gamma 1: the shifts "
                f"{shifts}, the mean tan alpha {fmt_fraction(mean_tan, 5)}, C = {c_pin:.3f} against 4"
            )


def ring_starts(b: int) -> list[tuple[int, int]]:
    """The ring of impact distance b: every Node (y, z) of the screen's
    plane with |sqrt(y^2 + z^2) - b| <= 1 / 2, in a fixed order."""
    found = []
    for y in range(-b - 1, b + 2):
        for z in range(-b - 1, b + 2):
            if abs(math.sqrt(y * y + z * z) - b) <= 0.5:
                found.append((y, z))
    found.sort()
    return found


def ring_section() -> None:
    """Section 9 of STEP_ALGEBRA.md: the same fan and the same M, one row
    of light on the heading from every start of the ring of impact
    distance b, read at the whole screen; the mean over the ring of the
    radial deflection (toward the mass's line) is the orientation average
    of the comb. GAMEBOARD arithmetic, the step algebra's simulation of
    the board, not a run."""
    n, d = PAIR
    fan = primitive_fan(FAN_BOUND)
    q = len(fan) * 16
    s_pin = Fraction(d, n)
    gm = Fraction(q) / (4 * s_pin)  # G M with the pi kept aside
    crowd = Crowd(fan, 16)
    tables = {gamma: Table(fan, BEAM, gamma) for gamma in (0, 1)}
    print()
    print(
        "9. THE RING OF STARTS (the orientation average of the comb): one row on the heading from every Node"
    )
    print(
        "   (y, z) with |sqrt(y^2 + z^2) - b| <= 1/2, read at the whole screen; per start the radial deflection"
    )
    print(
        "   toward the mass's line, tan alpha_r = -(P_y y + P_z z) / (P_x r) from the momentum and the radial"
    )
    print(
        "   shift of the arrival Node; the ring's mean; C_ring = mean(tan alpha_r x r) x 4 pi S / (3 q) against 4"
    )
    # The fan's L1 factor of the flow: the shell mean of |V| r^2 / Q over
    # r = 4 .. 14 against the continuum's q / (4 pi) (the one-wall note's
    # section 5, 32.79 against 23.08), from the same crowd's lines.
    shells = []
    for r in range(4, 15):
        nodes = [
            (x, y, z)
            for x in range(-15, 16)
            for y in range(-15, 16)
            for z in range(-15, 16)
            if abs(math.sqrt(x * x + y * y + z * z) - r) < 0.5
        ]
        total = sum(
            math.sqrt(sum(a * a for a in crowd.flow.get(node, [0, 0, 0]))) / 16 for node in nodes
        )
        shells.append(total / len(nodes) * r * r / Q)
    shell_mean = sum(shells) / len(shells)
    l1_factor = shell_mean / (len(fan) / (4 * math.pi))
    manhattan_ratio = sum(sum(abs(a) for a in v) / math.sqrt(sum(a * a for a in v)) for v in fan) / len(
        fan
    )
    print(
        f"   the fan's L1 factor of the flow: the shell mean of |V| r^2 / Q over r = 4 .. 14 is "
        f"{shell_mean:.2f} against the continuum's q / (4 pi) = {len(fan) / (4 * math.pi):.2f}: "
        f"F_L1 = {l1_factor:.3f} (the fan's mean S_1 / |D| is {manhattan_ratio:.3f})"
    )
    for b in (3, 6, 8):
        starts = ring_starts(b)
        print(f"   b = {b}: {len(starts)} starts: {starts}")
        for gamma in (0, 1):
            table = tables[gamma]
            rows = []
            for y, z in starts:
                base = walk(table, None, (1, 0, 0), y, z, gamma)
                out = walk(table, crowd, (1, 0, 0), y, z, gamma)
                r = math.sqrt(y * y + z * z)
                if "tangent" not in out or "tangent" not in base:
                    rows.append((y, z, r, None, None, None, out))
                    continue
                p = out["momentum"]
                radial = Fraction(-(p[1] * y + p[2] * z), p[0])  # tan alpha_r times r
                tangential = Fraction(-(p[1] * (-z) + p[2] * y), p[0])  # the component along (-z, y)
                dy, dz = out["node"][1] - base["node"][1], out["node"][2] - base["node"][2]
                node_radial = -(dy * y + dz * z) / r  # Links toward the line, from the arrival Node
                delay = out["age"] - base["age"]
                rows.append((y, z, r, radial, tangential, (dy, dz, node_radial, delay), out))
            landed = [row for row in rows if row[3] is not None]
            per_start = "; ".join(
                f"({y:+d}, {z:+d}) r {r:.2f}: dy, dz = {t[0]:+d}, {t[1]:+d}, radial {t[2]:+.2f} Links, delay {t[3]:+d}, "
                f"tan alpha_r {float(rad) / r:.5f}"
                if rad is not None
                else f"({y:+d}, {z:+d}): {'MEASURED AT THE MASS' if o.get('taken') else 'ESCAPED'} at {o['node']}"
                for y, z, r, rad, _tan, t, o in rows
            )
            print(f"     gamma {gamma}: {per_start}")
            if not landed:
                continue
            count = len(landed)
            mean_radial_r = (
                sum((row[3] for row in landed), Fraction(0)) / count
            )  # mean of tan alpha_r x r
            mean_tan = sum(float(row[3]) / row[2] for row in landed) / count
            mean_tangential = sum(float(row[4]) / row[2] for row in landed) / count
            mean_node = sum(row[5][2] for row in landed) / count
            mean_delay = Fraction(sum(row[5][3] for row in landed), count)
            c_ring = float(mean_radial_r / (3 * gm) * math.pi)
            c_nodes = mean_node / 26 * b * 4 * math.pi * float(s_pin) / (3 * q)
            grain = (1 / 26) / float(3 * gm / (math.pi * b))
            print(
                f"       the ring's mean over {count} starts: tan alpha_r {mean_tan:.5f} (the tangential component "
                f"{mean_tangential:+.5f}), the radial shift of the arrival Node {mean_node:.3f} Links, the delay "
                f"{fmt_fraction(mean_delay, 2)} intervals; C_ring = {c_ring:.3f} against 4 (from the arrival Nodes "
                f"{c_nodes:.3f}); against the lattice's own push constant, C_ring / F_L1 = "
                f"{c_ring / l1_factor:.3f}; the grain on C per start {grain:.2f}, on the ring's mean "
                f"{grain / count:.3f}; "
                f"Shapiro's delay {float((1 + gamma) * gm * 3 * math.sqrt(3) / math.pi * math.log(4 * 26 * 26 / (b * b))):.2f}"
            )


if __name__ == "__main__":
    main()
    ring_section()
