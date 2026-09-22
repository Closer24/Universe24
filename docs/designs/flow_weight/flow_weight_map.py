"""The arithmetic of docs/designs/flow_weight/DESIGN.md and ALGEBRA.md (the
Flow Weight Designer, 2026-09-22): the hypothesis `flow-link-v1`, the
arrival flow weighted per line by the line's Euclidean length per Node,
|D| / S_1, so that the push's shell mean carries no L1 factor and the
law's two constants of gravity are one.

Integers only, no engine import, nothing run on the engine. The step
algebra is the Bending Algebraist's, REUSED BY IMPORT and not copied (one
canonical copy, the Boss's order of record 888's session):
docs/designs/light_bending/step_algebra_map.py (the walk of one row of
light under the key `optical`, transcribed integer for integer from
`nature_beam.py`: `walk`; the world's table `Table`; the stationary crowd
`Crowd`; the fan `primitive_fan`; the labels `unit_label`; the digital
line `bresenham_line`; the box `in_box`; the ring `ring_starts`; the
constants Q, PAIR, FAN_BOUND, BEAM, HEADINGS, LINKS). What this file adds:
the flow label of a direction, f_D = the integer vector nearest Q D / S_1
(`flow_label`); a crowd whose flow is summed on f_D (`WeightedCrowd`, the
Algebraist's `Crowd` with its flow rebuilt on the same lines) so that the
Algebraist's `walk` reads the weighted flow unchanged; the exact form
beside it (`ExactTable`, the labels in units of 1 / L, L the table's
common multiple of S_1, with the flow Q D L / S_1; the walk homogeneous);
and every reading of the step algebra repeated under the rule. Every
number is GAMEBOARD, the step algebra's simulation of the board, not a
run, never a measurement of nature.

    python docs/designs/flow_weight/flow_weight_map.py > docs/designs/flow_weight/flow_weight_map.out
"""

from __future__ import annotations

import importlib.util
import math
from collections import defaultdict
from collections.abc import Callable
from fractions import Fraction
from pathlib import Path

_SPEC = importlib.util.spec_from_file_location(
    "step_algebra_map", Path(__file__).resolve().parents[1] / "light_bending" / "step_algebra_map.py"
)
assert _SPEC is not None and _SPEC.loader is not None
sam = importlib.util.module_from_spec(_SPEC)
_SPEC.loader.exec_module(sam)

Q = sam.Q
PAIR = sam.PAIR
BEAM = sam.BEAM
PLANE_RADIUS = 8  # series D's plane fan: primitive (a, b, 0) with 0 < a^2 + b^2 <= 64 (120)
Vector = tuple[int, int, int]


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


def table_lcm(table: sam.Table) -> int:
    """L, the least common multiple of S_1 over the world's table."""
    found = 1
    for s in table.s1:
        if s:
            found = found * s // math.gcd(found, s)
    return found


def plane_fan(radius: int) -> list[Vector]:
    found = []
    for a in range(-radius, radius + 1):
        for b in range(-radius, radius + 1):
            if (a or b) and a * a + b * b <= radius * radius and math.gcd(abs(a), abs(b)) == 1:
                found.append((a, b, 0))
    found.sort()
    return found


class WeightedCrowd(sam.Crowd):
    """The Algebraist's stationary crowd (its age moment, presence and
    lines untouched) with the arrival flow rebuilt on the same lines with
    the label `label_of(D)` per arriving unit in place of u_D: the flow
    the push reads under flow-link-v1 (`label_of = flow_label`). The
    Algebraist's `walk` reads `crowd.flow` and `crowd.age_moment` and
    nothing else of the crowd, so it walks the rule unchanged."""

    def __init__(self, fan: list[Vector], scale: int, label_of: Callable[[Vector], Vector]) -> None:
        super().__init__(fan, scale)
        self.flow = defaultdict(lambda: [0, 0, 0])
        for vector in fan:
            s1 = sum(abs(c) for c in vector)
            steps = sam.bresenham_line(vector)
            label = label_of(vector)
            node = [0, 0, 0]
            for made in range(1, sam.LINKS + 1):
                step = steps[(made - 1) % s1]
                node = [node[i] + step[i] for i in range(3)]
                key = (node[0], node[1], node[2])
                if not sam.in_box(key):
                    break
                for i in range(3):
                    self.flow[key][i] += scale * label[i]


class ExactTable(sam.Table):
    """The exact form: the labels in units of 1 / L (L u_D), the weight
    per unit kept as the Algebraist's table forms it from u_D; with the
    flow Q D L / S_1 the walk is homogeneous in P (the label's argmin,
    the pair over the gcd, the turn's shift all scale)."""

    def __init__(self, fan: list[Vector], beam: tuple[Vector, ...], gamma: int) -> None:
        super().__init__(fan, beam, gamma)
        self.lcm = table_lcm(self)
        self.labels = [(self.lcm * u[0], self.lcm * u[1], self.lcm * u[2]) for u in self.labels]


def exact_label(lcm: int) -> Callable[[Vector], Vector]:
    def label_of(vector: Vector) -> Vector:
        s1 = sum(abs(c) for c in vector)
        if s1 == 0:
            return (0, 0, 0)
        return (Q * vector[0] * lcm // s1, Q * vector[1] * lcm // s1, Q * vector[2] * lcm // s1)

    return label_of


def shell_nodes(r: int) -> list[Vector]:
    return [
        (x, y, z)
        for x in range(-15, 16)
        for y in range(-15, 16)
        for z in range(-15, 16)
        if abs(math.sqrt(x * x + y * y + z * z) - r) < 0.5
    ]


def norm(v) -> float:
    return math.sqrt(sum(a * a for a in v))


def mean_and_spread(values: list[float]) -> tuple[float, float, float]:
    """The mean, the standard deviation of the values and the standard
    error of the mean."""
    m = sum(values) / len(values)
    sd = math.sqrt(sum((v - m) ** 2 for v in values) / (len(values) - 1))
    return m, sd, sd / math.sqrt(len(values))


def main() -> None:
    n, d = PAIR
    fan = sam.primitive_fan(sam.FAN_BOUND)
    q_lines = len(fan)
    tables = {
        "unit": {g: sam.Table(fan, BEAM, g) for g in (0, 1)},
        "flow": {g: sam.Table(fan, BEAM, g) for g in (0, 1)},
        "exact": {g: ExactTable(fan, BEAM, g) for g in (0, 1)},
    }
    table0 = tables["unit"][0]
    heading = table0.index[(1, 0, 0)]
    t_h = table0.t[heading]
    lcm = tables["exact"][0].lcm
    print("THE FLOW WEIGHT MAP: THE STEP ALGEBRA'S SIMULATION OF THE BOARD, NOT A RUN")
    print(
        "(docs/designs/flow_weight/DESIGN.md and ALGEBRA.md; the Algebraist's step_algebra_map.py imported)"
    )
    print(
        f"the fan: {q_lines} directions within Manhattan {sam.FAN_BOUND}; [n, d] = [{n}, {d}]; Q = {Q}"
    )
    print(f"the heading's T_h = {t_h}; the table's lcm of S_1 (fan, headings, beam) L = {lcm}")
    print()

    # 1. The fan's means: the incidence S_1 / |D| against the weights.
    print(
        "1. THE FAN'S MEANS over the 290 directions (the incidence S_1 / |D| times the weight per line)"
    )
    incidence = [sum(abs(c) for c in v) / norm(v) for v in fan]
    exact_w = [norm(v) / sum(abs(c) for c in v) for v in fan]
    f_w = [norm(flow_label(v)) / Q for v in fan]
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
    rounding = [abs(f - e) / e for f, e in zip(f_w, exact_w, strict=True)]
    print(
        f"   f_D against Q D / S_1 per line: the largest relative error of |f_D| {max(rounding):.4f}, "
        f"the mean {sum(rounding) / q_lines:.4f}"
    )
    worst = fan[max(range(q_lines), key=lambda k: rounding[k])]
    print(
        f"   the worst line {worst}: f_D = {flow_label(worst)}, Q D / S_1 = "
        f"{tuple(Fraction(Q * c, sum(abs(a) for a in worst)) for c in worst)}"
    )
    print(
        "   the beam's flow labels: "
        + ", ".join(f"{v}: f = {flow_label(v)}, u = {sam.unit_label(v)}" for v in BEAM)
    )
    plane = plane_fan(PLANE_RADIUS)
    plane_incidence = [sum(abs(c) for c in v) / norm(v) for v in plane]
    f_plane = sum(plane_incidence) / len(plane)
    print(
        f"   series D's plane fan ({len(plane)} directions): mean S_1 / |D| = {f_plane:.4f} "
        f"(4 / pi = {4 / math.pi:.4f} in the isotropic limit)"
    )
    print()

    # 2. The shell means from the same crowd.
    scale = 16
    q = q_lines * scale
    crowds = {
        "unit": sam.Crowd(fan, scale),
        "flow": WeightedCrowd(fan, scale, flow_label),
        "exact": WeightedCrowd(fan, scale, exact_label(lcm)),
    }
    print(f"2. THE SHELL MEANS over r = 4 .. 14 from the crowd at M = 2^16 (q = {q} units per interval)")
    per_shell: dict[str, list[float]] = {"unit": [], "flow": [], "exact": [], "age": []}
    for r in range(4, 15):
        nodes = shell_nodes(r)
        count = len(nodes)
        for form, divisor in (("unit", 1), ("flow", 1), ("exact", lcm)):
            total = sum(norm(crowds[form].flow.get(k, [0, 0, 0])) / scale / divisor for k in nodes)
            per_shell[form].append(total / count * r * r / Q)
        per_shell["age"].append(
            sum(crowds["unit"].age_moment.get(k, 0) / scale for k in nodes) / count * r
        )
    continuum = q_lines / (4 * math.pi)
    for form, name, ref in (
        ("unit", "|V| r^2 / Q on u_D (the law as built)       ", continuum),
        ("flow", "|V_f| r^2 / Q on f_D (flow-link-v1)         ", continuum),
        ("exact", "|V_L| r^2 / (Q L) on Q D L / S_1 (exact form)", continuum),
        ("age", "A r (the clock's word, unchanged)            ", 3 * continuum),
    ):
        m, sd, se = mean_and_spread(per_shell[form])
        print(
            f"   {name} = {m:.2f} against {ref:.2f}: the factor {m / ref:.3f}; the shells' spread "
            f"{sd:.2f} (sd), the mean's error {se:.2f} ({se / ref:.3f} of the continuum's)"
        )
    print("   per shell r: |V| r^2 / Q, |V_f| r^2 / Q, |V_L| r^2 / (Q L), A r")
    for k, r in enumerate(range(4, 15)):
        print(
            f"     r = {r:2d}: {per_shell['unit'][k]:6.2f}  {per_shell['flow'][k]:6.2f}  "
            f"{per_shell['exact'][k]:6.2f}  {per_shell['age'][k]:6.2f}"
        )
    print()

    # 3. The calibration and the registered worlds under the rule.
    gm = Fraction(q) / (4 * Fraction(d, n))  # G M = q / (4 pi S) at the pin, the pi kept aside
    print(
        "3. THE CONTROL AND THE REGISTERED IN-PLANE WORLDS (b = 6 mass, 8 far, 3 near) under each form:"
    )
    print("   the five lines' shifts (pixels) and delays (intervals) against the control; the mean;")
    print("   tan alpha from the momentum; C = alpha b c^2 / (G M) at the pin n S = d")
    controls = {b: [sam.walk(table0, None, line, b, 0, 0) for line in BEAM] for b in (3, 6, 8)}
    ages = [r["age"] for r in controls[6]]
    print(
        f"   the control (no crowd, no push, the rule reads nothing): the click ages {ages}, "
        f"the mean {sum(ages) / 5:.2f}"
    )
    for form in ("unit", "flow", "exact"):
        print(f"   form {form}:")
        for b in (6, 8, 3):
            for gamma in (0, 1):
                rows = [sam.walk(tables[form][gamma], crowds[form], line, b, 0, gamma) for line in BEAM]
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
    print("   (Links) and C from the Nodes, the mean delay, the grain on C_ring")
    for b in (3, 6, 8):
        starts = sam.ring_starts(b)
        for form in ("unit", "flow", "exact"):
            for gamma in (0, 1):
                table = tables[form][gamma]
                radial_sum = Fraction(0)
                tangential_sum = 0.0
                node_sum = 0.0
                delay_sum = 0
                count = 0
                moved: dict[int, int] = defaultdict(int)
                per_start = []
                for y, z in starts:
                    base = sam.walk(tables["unit"][gamma], None, (1, 0, 0), y, z, gamma)
                    out = sam.walk(table, crowds[form], (1, 0, 0), y, z, gamma)
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
                    moved[abs(dy) + abs(dz)] += 1
                    per_start.append(f"({y:+d},{z:+d}) {dy:+d},{dz:+d}")
                c_ring = float(radial_sum / count / (3 * gm) * math.pi)
                c_nodes = node_sum / count / 26 * b * 4 * math.pi * float(Fraction(d, n)) / (3 * q)
                grain = (1 / 26) / float(3 * gm / (math.pi * b)) / count
                print(
                    f"   b = {b}, {count} starts, form {form}, gamma {gamma}: tan alpha_r "
                    f"{float(radial_sum / count) / b:.5f} (tangential {tangential_sum / count:+.5f}); "
                    f"C_ring = {c_ring:.3f} against 4; the arrival Node's radial shift {node_sum / count:.3f} Links "
                    f"(C from the Nodes {c_nodes:.3f}); the delay {delay_sum / count:.2f}; the grain {grain:.3f}; "
                    f"starts moved by 0 / 1 / 2 / 3 Nodes: {moved[0]} / {moved[1]} / {moved[2]} / {moved[3]}"
                )
                if form == "flow":
                    print(f"       the arrival Nodes (dy, dz per start): {'; '.join(per_start)}")
    print()

    # 5. Series D's plane pins under the rule (the fall's g, the orbit's T), by formula.
    print("5. SERIES D3's PINS ON THE PLANE UNDER THE RULE, BY FORMULA (GAMEBOARD)")
    s_width = 32
    balance = 9.0 * 9.0 / (s_width + 9.0)  # the circular orbit's n^2 / (S + n) at the pinned n = 9
    balance_rule = balance / f_plane
    n_rule = (balance_rule + math.sqrt(balance_rule * balance_rule + 4 * s_width * balance_rule)) / 2
    for r in (12, 24):
        t_old = 2 * math.pi * r * (s_width + 9) / 9
        t_new = 2 * math.pi * r * (s_width + n_rule) / n_rule
        t_whole = 2 * math.pi * r * (s_width + 8) / 8
        print(
            f"   r = {r}: T = 2 pi r (S + n) / n = {t_old:.0f} at n = 9 becomes {t_new:.0f} at n = {n_rule:.3f} "
            f"({t_whole:.0f} at the nearest whole n = 8)"
        )
    print(f"   the push per interval, and the fall's g = v^2 / r, divided by F_plane = {f_plane:.4f}")
    print("   T(24) / T(12) = 2.00 unchanged: the same fan, the same weight per line at both radii")


if __name__ == "__main__":
    main()
