"""The arithmetic of docs/designs/flow_weight/DESIGN.md (the Flow Weight
Designer, 2026-09-22): the hypothesis `flow-link-v1`, the arrival flow
weighted per line by the line's Euclidean length per Node, |D| / S_1, so
that the push's shell mean carries no L1 factor and the law's two
constants of gravity are one.

Integers only, no engine import, nothing run on the engine. The six verbs
of the key `optical` are transcribed from `src/event_universe/events/
nature_beam.py` on main exactly as the Bending Algebraist's
step_algebra_map.py transcribed them (docs/designs/light_bending/ at
23ef9ce93721963098c45e0add3f846a7154a1fb, PR #821: the walk
`optical_walk_step`, the wall `core.integer.age_wall`, the push and the
label `optical_turn`, the pair `momentum_pair`, the weight `unit_weights`,
the neighbours `fan_neighbours`, the line `world.bresenham_line`, the
label `unit_label`), the pieces needed here copied so that this file
stands alone on main. What this file adds: the flow label of a direction,
f_D = the integer vector nearest Q D / S_1 (the exact Q D L / S_1 beside
it, L the table's common multiple of S_1), read by the push in place of
u_D, and every reading of the step algebra repeated under it.
Every number is GAMEBOARD, the step algebra's simulation of the board,
not a run, never a measurement of nature.

    python docs/designs/flow_weight/flow_weight_map.py > docs/designs/flow_weight/flow_weight_map.out
"""

from __future__ import annotations

import functools
import math
from collections import defaultdict
from fractions import Fraction

Q = 64  # the label's scale (BEAM_LAW section 2)
PAIR = (1, 16384)  # the optical worlds' `suspension` [n, d]
FAN_BOUND = 6  # series K's fan: primitive directions with |a| + |b| + |c| <= 6 (290)
BEAM = ((1, 0, 0), (24, 1, 0), (24, -1, 0), (12, 1, 0), (12, -1, 0))  # lensing/make_worlds.py
HEADINGS = ((1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1))
X_LAMP, X_SCREEN = -26, 26  # the lamp at x = 2, the mass at 28, the screen at 54 (shape 57)
BOX = ((-26, 28), (-20, 20), (-20, 20))
FAN_NEIGHBOURS = 6
LINKS = 80
PLANE_RADIUS = 8  # series D's plane fan: primitive (a, b, 0) with 0 < a^2 + b^2 <= 64 (120)
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


def plane_fan(radius: int) -> list[Vector]:
    found = []
    for a in range(-radius, radius + 1):
        for b in range(-radius, radius + 1):
            if (a or b) and a * a + b * b <= radius * radius and math.gcd(abs(a), abs(b)) == 1:
                found.append((a, b, 0))
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


def flow_label(vector: Vector) -> Vector:
    """flow-link-v1's flow label: the integer vector nearest Q D / S_1,
    per component (2 Q |a| + S_1) // (2 S_1) with the sign of a, the one
    Euclidean division of the rule, taken once at load; no root."""
    s1 = sum(abs(c) for c in vector)
    if s1 == 0:
        return (0, 0, 0)
    found = []
    for a in vector:
        k = (2 * Q * abs(a) + s1) // (2 * s1)
        found.append(k if a >= 0 else -k)
    return (found[0], found[1], found[2])


def bresenham_line(vector: Vector) -> list[Vector]:
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
    """The world's direction table with Flight's integers per direction:
    S_1, T_D = isqrt(3 |D|^2 Q^2), the line, u_D, e_D, the weight per
    unit at gamma, the neighbours; and, under the hypothesis, the flow
    label f_D and the exact Q D L / S_1 with L the table's lcm of S_1."""

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
        self.flow_labels = [flow_label(v) for v in self.vectors]
        self.lcm = 1
        for s in self.s1:
            if s:
                self.lcm = self.lcm * s // math.gcd(self.lcm, s)
        self.exact_labels = [
            tuple(Q * c * self.lcm // s for c in v) if s else (0, 0, 0)
            for v, s in zip(self.vectors, self.s1, strict=True)
        ]


def age_of(made: int, s1: int, t: int) -> int:
    return max(0, -(-(made * 2 * t - t) // (2 * s1 * Q)))


class Crowd:
    """The stationary crowd of the mass at the origin (one row of amount
    `scale` per direction per interval, each walking its line by the
    flight rule): per Node the age moment A, the arrival flow V on the
    labels u_D, the flow V_f on the flow labels f_D, and the exact flow
    V_L on Q D L / S_1 (in units of 1 / L)."""

    def __init__(self, fan: list[Vector], scale: int, lcm: int) -> None:
        self.age_moment: dict[Vector, int] = defaultdict(int)
        self.flow: dict[Vector, list[int]] = defaultdict(lambda: [0, 0, 0])
        self.flow_f: dict[Vector, list[int]] = defaultdict(lambda: [0, 0, 0])
        self.flow_exact: dict[Vector, list[int]] = defaultdict(lambda: [0, 0, 0])
        self.lcm = lcm
        for vector in fan:
            s1 = sum(abs(c) for c in vector)
            t = math.isqrt(3 * sum(c * c for c in vector) * Q * Q)
            steps = bresenham_line(vector)
            label = unit_label(vector)
            f_label = flow_label(vector)
            exact = [Q * c * lcm // s1 for c in vector]
            node = [0, 0, 0]
            for made in range(1, LINKS + 1):
                step = steps[(made - 1) % s1]
                node = [node[i] + step[i] for i in range(3)]
                key = (node[0], node[1], node[2])
                if not in_box(key):
                    break
                ages = range(age_of(made, s1, t), age_of(made + 1, s1, t))
                self.age_moment[key] += scale * sum(ages)
                for i in range(3):
                    self.flow[key][i] += scale * label[i]
                    self.flow_f[key][i] += scale * f_label[i]
                    self.flow_exact[key][i] += scale * exact[i]


def momentum_pair(momentum: list[int]) -> tuple[int, int]:
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
    form: str,
) -> dict[str, object]:
    """One row of light from the lamp (X_LAMP, b, z) on the line `start`,
    walked by the key's three rules interval by interval as
    step_algebra_map.walk does (content 1, amount 1). `form` selects the
    flow the push reads: "unit" the law as built (u_D per arrival),
    "flow" the hypothesis (f_D per arrival), "exact" the hypothesis in
    its fraction-free form (Q D L / S_1 per arrival, the accumulator and
    the label scale in units of 1 / L; the label's verb 3 is homogeneous
    in P, the pair takes P over its gcd, so the walk is the same rule)."""
    n, d = PAIR
    f = 1 + gamma
    direction = table.index[start]
    node = [X_LAMP, b, z]
    made = 0
    pushed = False
    w_acc = [0, 0, 0]
    cross = [0, 0, 0]
    residue = table.t[direction] * d
    age = 0
    label_scale = Q * d * (table.lcm if form == "exact" else 1)
    p0 = [label_scale * c for c in table.labels[direction]]
    flows = (
        {"unit": crowd.flow, "flow": crowd.flow_f, "exact": crowd.flow_exact}[form] if crowd else None
    )

    def momentum(dir_index: int) -> list[int]:
        return [label_scale * table.labels[dir_index][i] + w_acc[i] for i in range(3)]

    def pair(dir_index: int) -> tuple[int, int]:
        if not pushed:
            return 2 * table.s1[dir_index] * Q, 2 * table.t[dir_index]
        s1, t = momentum_pair(momentum(dir_index))
        return 2 * s1 * Q, 2 * t

    while True:
        age += 1
        a = crowd.age_moment.get((node[0], node[1], node[2]), 0) if crowd else 0
        rate0, wall0 = pair(direction)
        rate, wall = rate0 * d, wall0 * (d + f * n * a)
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
                return {"node": key, "age": age, "made": made, "momentum": p, "tangent": tangent}
            if key == (0, 0, 0):
                return {"node": key, "age": age, "taken": True}
            if not in_box(key):
                return {"node": key, "age": age, "escaped": True}
        if crowd is None or flows is None or (node[0], node[1], node[2]) == (X_LAMP, b, z):
            continue
        v = flows.get((node[0], node[1], node[2]), [0, 0, 0])
        if any(v):
            old_rate = pair(direction)[0]
            weight = table.weight[direction]
            for i in range(3):
                w_acc[i] -= n * weight * v[i]
            pushed = True
            new_rate = pair(direction)[0]
            residue = residue * new_rate // old_rate
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


def ring_starts(b: int) -> list[tuple[int, int]]:
    found = []
    for y in range(-b - 1, b + 2):
        for z in range(-b - 1, b + 2):
            if abs(math.sqrt(y * y + z * z) - b) <= 0.5:
                found.append((y, z))
    found.sort()
    return found


def shell_nodes(r: int) -> list[Vector]:
    return [
        (x, y, z)
        for x in range(-15, 16)
        for y in range(-15, 16)
        for z in range(-15, 16)
        if abs(math.sqrt(x * x + y * y + z * z) - r) < 0.5
    ]


def norm(v: list[int]) -> float:
    return math.sqrt(sum(a * a for a in v))


def main() -> None:
    n, d = PAIR
    fan = primitive_fan(FAN_BOUND)
    q_lines = len(fan)
    tables = {gamma: Table(fan, BEAM, gamma) for gamma in (0, 1)}
    table0 = tables[0]
    heading = table0.index[(1, 0, 0)]
    t_h = table0.t[heading]
    print("THE FLOW WEIGHT MAP: THE STEP ALGEBRA'S SIMULATION OF THE BOARD, NOT A RUN")
    print("(docs/designs/flow_weight/DESIGN.md; the walk of step_algebra_map.py at 23ef9ce9)")
    print(f"the fan: {q_lines} directions within Manhattan {FAN_BOUND}; [n, d] = [{n}, {d}]; Q = {Q}")
    print(f"the heading's T_h = {t_h}; the table's lcm of S_1 (fan, headings, beam) L = {table0.lcm}")
    print()

    # 1. The fan's means: the incidence S_1 / |D| against the weights.
    print(
        "1. THE FAN'S MEANS over the 290 directions (the incidence S_1 / |D| times the weight per line)"
    )
    incidence = [sum(abs(c) for c in v) / norm(list(v)) for v in fan]
    exact_w = [norm(list(v)) / sum(abs(c) for c in v) for v in fan]
    f_w = [norm(list(flow_label(v))) / Q for v in fan]
    dwell_w = [
        math.isqrt(3 * sum(c * c for c in v) * Q * Q) / (sum(abs(c) for c in v) * t_h) for v in fan
    ]
    print(f"   mean S_1 / |D| (F_L1 of the fan)                       = {sum(incidence) / q_lines:.4f}")
    print(
        f"   mean (S_1 / |D|) x (|D| / S_1), the exact weight         = "
        f"{sum(i * w for i, w in zip(incidence, exact_w, strict=True)) / q_lines:.4f} (1 by identity)"
    )
    print(
        f"   mean (S_1 / |D|) x |f_D| / Q, the flow label f_D          = "
        f"{sum(i * w for i, w in zip(incidence, f_w, strict=True)) / q_lines:.4f}"
    )
    print(
        f"   mean (S_1 / |D|) x T_D / (S_1 T_h), the dwell in units of the heading's = "
        f"{sum(i * w for i, w in zip(incidence, dwell_w, strict=True)) / q_lines:.4f}"
    )
    rounding = [
        abs(norm(list(flow_label(v))) / Q - norm(list(v)) / sum(abs(c) for c in v))
        / (norm(list(v)) / sum(abs(c) for c in v))
        for v in fan
    ]
    print(
        f"   f_D against Q D / S_1 per line: the largest relative error of |f_D| {max(rounding):.4f}, "
        f"the mean {sum(rounding) / q_lines:.4f}"
    )
    worst = max(
        fan, key=lambda v: abs(norm(list(flow_label(v))) / Q - norm(list(v)) / sum(abs(c) for c in v))
    )
    print(
        f"   the worst line {worst}: f_D = {flow_label(worst)}, Q D / S_1 = {tuple(Fraction(Q * c, sum(abs(a) for a in worst)) for c in worst)}"
    )
    print(
        "   the beam's flow labels: "
        + ", ".join(f"{v}: f = {flow_label(v)}, u = {unit_label(v)}" for v in BEAM)
    )
    plane = plane_fan(PLANE_RADIUS)
    plane_incidence = [sum(abs(c) for c in v) / norm(list(v)) for v in plane]
    print(
        f"   series D's plane fan ({len(plane)} directions): mean S_1 / |D| = "
        f"{sum(plane_incidence) / len(plane):.4f} (4 / pi = {4 / math.pi:.4f} in the isotropic limit)"
    )
    print()

    # 2. The shell means from the same crowd.
    scale = 16
    q = q_lines * scale
    crowd = Crowd(fan, scale, table0.lcm)
    print(f"2. THE SHELL MEANS over r = 4 .. 14 from the crowd at M = 2^16 (q = {q} units per interval)")
    means = {"unit": [], "flow": [], "exact": [], "age": []}
    for r in range(4, 15):
        nodes = shell_nodes(r)
        count = len(nodes)
        means["unit"].append(
            sum(norm(crowd.flow.get(k, [0, 0, 0])) / scale for k in nodes) / count * r * r / Q
        )
        means["flow"].append(
            sum(norm(crowd.flow_f.get(k, [0, 0, 0])) / scale for k in nodes) / count * r * r / Q
        )
        means["exact"].append(
            sum(norm(crowd.flow_exact.get(k, [0, 0, 0])) / scale / crowd.lcm for k in nodes)
            / count
            * r
            * r
            / Q
        )
        means["age"].append(sum(crowd.age_moment.get(k, 0) / scale for k in nodes) / count * r)
    continuum = q_lines / (4 * math.pi)
    unit_mean = sum(means["unit"]) / len(means["unit"])
    flow_mean = sum(means["flow"]) / len(means["flow"])
    exact_mean = sum(means["exact"]) / len(means["exact"])
    print(
        f"   |V| r^2 / Q on u_D (the law as built)        = {unit_mean:.2f} against q / (4 pi) = {continuum:.2f}: the factor {unit_mean / continuum:.3f}"
    )
    print(
        f"   |V_f| r^2 / Q on f_D (flow-link-v1)          = {flow_mean:.2f} against {continuum:.2f}: the factor {flow_mean / continuum:.3f}"
    )
    print(
        f"   |V_L| r^2 / (Q L) on Q D L / S_1 (exact form) = {exact_mean:.2f} against {continuum:.2f}: the factor {exact_mean / continuum:.3f}"
    )
    print(
        f"   A r (the clock's word, unchanged)              = {sum(means['age']) / len(means['age']):.2f} "
        f"against 3 q / (4 pi) = {3 * continuum:.2f}: the factor {sum(means['age']) / len(means['age']) / (3 * continuum):.3f}"
    )
    print("   per shell r: |V| r^2 / Q, |V_f| r^2 / Q, |V_L| r^2 / (Q L), A r")
    for r, u, fl, ex, ag in zip(
        range(4, 15), means["unit"], means["flow"], means["exact"], means["age"], strict=True
    ):
        print(f"     r = {r:2d}: {u:6.2f}  {fl:6.2f}  {ex:6.2f}  {ag:6.2f}")
    print()

    # 3. The registered worlds under the rule.
    gm = Fraction(q) / (4 * Fraction(d, n))  # G M = q / (4 pi S) at the pin, the pi kept aside
    print(
        "3. THE REGISTERED IN-PLANE WORLDS (b = 6 mass, 8 far, 3 near) under each form: the five lines'"
    )
    print(
        "   shifts (pixels) and delays (intervals) against the control; the mean; tan alpha from the momentum;"
    )
    print("   C = alpha b c^2 / (G M) at the pin n S = d")
    controls = {b: [walk(table0, None, line, b, 0, 0, "unit") for line in BEAM] for b in (3, 6, 8)}
    for form in ("unit", "flow", "exact"):
        print(f"   form {form}:")
        for b in (6, 8, 3):
            for gamma in (0, 1):
                rows = [walk(tables[gamma], crowd, line, b, 0, gamma, form) for line in BEAM]
                base = controls[b]
                shifts = [r["node"][1] - c["node"][1] for r, c in zip(rows, base, strict=True)]
                delays = [r["age"] - c["age"] for r, c in zip(rows, base, strict=True)]
                mean_tan = sum((r["tangent"] for r in rows), Fraction(0)) / len(rows)
                c_pin = float(mean_tan * b / (3 * gm) * math.pi)
                print(
                    f"     b = {b}, gamma {gamma}: shifts {shifts}, mean {sum(shifts) / 5:+.3f}; delays {delays}, "
                    f"mean {sum(delays) / 5:.2f}; tan alpha {float(mean_tan):.5f}; C = {c_pin:.2f}"
                )
    print()

    # 4. The ring of starts under the rule.
    print(
        "4. THE RING OF STARTS (STEP_ALGEBRA.md section 9) under each form: the ring's mean tan alpha_r,"
    )
    print(
        "   C_ring against 4 on the clock's G M = q / (4 pi S), the mean radial shift of the arrival Node"
    )
    print("   (Links), the mean delay, the grain on C_ring")
    for b in (3, 6, 8):
        starts = ring_starts(b)
        for form in ("unit", "flow", "exact"):
            for gamma in (0, 1):
                table = tables[gamma]
                radial_sum = Fraction(0)
                tangential_sum = 0.0
                node_sum = 0.0
                delay_sum = 0
                count = 0
                per_start = []
                for y, z in starts:
                    base = walk(table, None, (1, 0, 0), y, z, gamma, "unit")
                    out = walk(table, crowd, (1, 0, 0), y, z, gamma, form)
                    if "tangent" not in out or "tangent" not in base:
                        per_start.append(f"({y:+d},{z:+d}) lost")
                        continue
                    r = math.sqrt(y * y + z * z)
                    p = out["momentum"]
                    radial_sum += Fraction(-(p[1] * y + p[2] * z), p[0])
                    tangential_sum += float(Fraction(-(p[1] * (-z) + p[2] * y), p[0])) / r
                    dy, dz = out["node"][1] - base["node"][1], out["node"][2] - base["node"][2]
                    node_sum += -(dy * y + dz * z) / r
                    delay_sum += out["age"] - base["age"]
                    count += 1
                    per_start.append(f"({y:+d},{z:+d}) {dy:+d},{dz:+d}")
                c_ring = float(radial_sum / count / (3 * gm) * math.pi)
                grain = (1 / 26) / float(3 * gm / (math.pi * b)) / count
                print(
                    f"   b = {b}, {count} starts, form {form}, gamma {gamma}: tan alpha_r "
                    f"{float(radial_sum / count) / b:.5f} (tangential {tangential_sum / count:+.5f}); "
                    f"C_ring = {c_ring:.3f} against 4; the arrival Node's radial shift {node_sum / count:.3f} Links; "
                    f"the delay {delay_sum / count:.2f}; the grain {grain:.3f}"
                )
                if form == "flow":
                    print(f"       the arrival Nodes (dy, dz per start): {'; '.join(per_start)}")
    print()

    # 5. Series D's plane pins under the rule (the fall's g, the orbit's T), by formula.
    print("5. SERIES D3's PINS ON THE PLANE UNDER THE RULE, BY FORMULA (GAMEBOARD)")
    f_plane = sum(plane_incidence) / len(plane)
    s_width = 32
    balance = 9.0 * 9.0 / (s_width + 9.0)  # the circular orbit's n^2 / (S + n) at the pinned n = 9
    balance_rule = balance / f_plane
    n_rule = (balance_rule + math.sqrt(balance_rule * balance_rule + 4 * s_width * balance_rule)) / 2
    for r in (12, 24):
        t_old = 2 * math.pi * r * (s_width + 9) / 9
        t_new = 2 * math.pi * r * (s_width + n_rule) / n_rule
        print(
            f"   r = {r}: T = 2 pi r (S + n) / n = {t_old:.0f} at n = 9 becomes {t_new:.0f} at n = {n_rule:.3f}"
        )
    print(f"   the push per interval, and the fall's g = v^2 / r, divided by F_plane = {f_plane:.4f}")
    print("   T(24) / T(12) = 2.00 unchanged (the ratio carries no constant)")


if __name__ == "__main__":
    main()
