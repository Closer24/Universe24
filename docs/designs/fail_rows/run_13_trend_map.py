"""Row 13 by the algebra before the run: the k_a(b) lamp's count ratio at
the ring's b, the ring's deciding pin restated on that click, and the
walk's trend at larger b and L and on a denser fan (the FAIL Runner C,
2026-09-23; docs/designs/fail_rows/RUN_13_2A.md sections 2 and 3).

The arithmetic is the Bending Algebraist's `step_algebra_map.py` (the
law's integer steps: the flight table, the hop rule with the half-wall
start, the one wall function of the crowd's age moment at the coefficient
c_f = 1 + gamma_PPN under the key `optical`, the push, the label by
Bresenham, the pair of a pushed row) with the Flow Weight Designer's
`flow_weight_map.py` (the flow label f_D of flow-link-v1, the weighted
crowd), imported by their files, one canonical copy each; what this map
adds is (1) the crowd's age moment at the Nodes of a ring of lamps in the
mass's plane at the impact distance b, read as the count ratio 1 + k_a(b)
a lamp's own clock gives at the coefficient 1 (the age wall on the lamp's
self-creations: the rate d against the wall d + n A, one birth when the
accumulator passes the wall; `core.integer.age_wall`), the exact birth
ticks over a window and what series T's inverse slope reads from them;
(2) the ring of starts walked again on boxes of half-length L = 26 (the
registered), 40 and 52 and on the fan of Manhattan 8 beside the fan of 6,
at the impact distances 6, 8, 10, 12 and 14. No engine is imported or
run; every number is the step algebra's simulation of the board
(GAMEBOARD until a run reads a click) or a COMPUTATION on the pins;
Einstein's 4 on the comparison side only.

Run from the repository root:

    .venv/bin/python docs/designs/fail_rows/run_13_trend_map.py > docs/designs/fail_rows/run_13_trend_map.out
"""

from __future__ import annotations

import importlib.util
import math
import sys
from collections import defaultdict
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]


def _script(name: str, path: Path):  # type: ignore[no-untyped-def]
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


FWM = _script("flow_weight_map", ROOT / "docs" / "designs" / "flow_weight" / "flow_weight_map.py")
SAM = FWM.sam  # the one instance of step_algebra_map the weighted crowd reads
Q = SAM.Q
N_SUSP, D_SUSP = SAM.PAIR  # [1, 16384], the ring worlds' pair; the width 16384 (the pin n S = d)
SCALE = 16  # M = 2^16 at `release` [1, 4096]: 16 units per direction per interval
C_F = 2  # 1 + gamma_PPN at gamma_PPN = 1, an input (record 826 (D))
README_K = (
    0.0445  # the gr_rows pin world's k_a(6) at [1, 4096], from the README's age moment 11.4 x 16 / 4096
)
RING_PIN = 0.731  # the deciding pin, the mean radial shift at b = 6, gamma 1, DETECTOR (met 2026-09-22)
RING_BRACKET = 0.025
C_NODES_PIN = 2.496  # the run's C_nodes at b = 6, gamma 1 (COMPUTATION on the DETECTOR reading)
C_RING_PIN = 3.655  # through the lever-arm factor 0.683
WINDOWS = ((200, 400), (200, 1200), (200, 3200))


def shell_nodes(r: float, half: int) -> list[tuple[int, int, int]]:
    return [
        (x, y, z)
        for x in range(-half, half + 1)
        for y in range(-half, half + 1)
        for z in range(-half, half + 1)
        if abs(math.sqrt(x * x + y * y + z * z) - r) < 0.5
    ]


def clock_births(a: int, n: int, d: int, ticks: int) -> list[int]:
    """The lamp's self-creation ticks under the age wall at the coefficient
    1: the accumulator gains d per interval against the wall d + n A, one
    birth when it passes (the lamp's `rate` [1, 1]); A the crowd's age
    moment at the lamp's Node less the lamp's own rows, constant once the
    crowd is stationary."""
    wall = d + n * a
    acc = 0
    births = []
    for tick in range(1, ticks + 1):
        acc += d
        if acc >= wall:
            acc -= wall
            births.append(tick)
    return births


def inverse_slope(births: list[int], window: tuple[int, int]) -> float:
    """Series T's reading: 1 + z as the inverse of the least-squares slope
    of the birth ordinal against the birth's tick over the window."""
    pts = [(t, j) for j, t in enumerate(births) if window[0] <= t < window[1]]
    xs = [float(t) for t, _ in pts]
    ys = [float(j) for _, j in pts]
    mx, my = sum(xs) / len(xs), sum(ys) / len(ys)
    slope = sum((x - mx) * (y - my) for x, y in zip(xs, ys, strict=True)) / sum(
        (x - mx) ** 2 for x in xs
    )
    return 1 / slope


def part_1_lamps() -> dict[int, dict[str, float]]:
    print(
        "1. THE k_a(b) LAMP: THE CROWD'S AGE MOMENT AT A RING OF LAMPS IN THE MASS'S PLANE, READ AS A COUNT RATIO"
    )
    print(
        f"   the ring worlds' crowd: the fan of 290 within Manhattan 6, M = 2^16 (scale {SCALE}), the pair"
        f" [{N_SUSP}, {D_SUSP}], the width {D_SUSP}; the lamps at x = 0 (the mass's plane) at every (y, z) of"
        " ring_starts(b); each lamp's clock counts the age moment of the rows of the mass's family at its Node"
        ' (its entry {"m": {"rule": "pass", "reads": "age"}}), less its own rows; k = n A / d; the count'
        " ratio against the control (no mass) is 1 + k"
    )
    fan = SAM.primitive_fan(SAM.FAN_BOUND)
    q_lines = len(fan)
    crowd = SAM.Crowd(fan, SCALE)
    continuum_a_r = 3 * q_lines / (4 * math.pi)  # the age moment's shell mean times r per unit of scale
    found: dict[int, dict[str, float]] = {}
    for b in (3, 6, 8):
        starts = SAM.ring_starts(b)
        rows = []
        for y, z in starts:
            a = crowd.age_moment.get((0, y, z), 0)
            p = crowd.presence.get((0, y, z), 0)
            lines = crowd.lines_through.get((0, y, z), 0)
            rows.append((y, z, a, p, lines))
        k_age = [Fraction(N_SUSP * a, D_SUSP) for _, _, a, _, _ in rows]
        k_pres = [Fraction(N_SUSP * p, D_SUSP) for _, _, _, p, _ in rows]
        mean_a = sum(a for _, _, a, _, _ in rows) / len(rows)
        shell = shell_nodes(b, 15)
        shell_a = sum(crowd.age_moment.get(k, 0) for k in shell) / len(shell)
        k_ring = float(sum(k_age, Fraction(0)) / len(rows))
        k_shell = shell_a * N_SUSP / D_SUSP
        k_cont = continuum_a_r * SCALE / b * N_SUSP / D_SUSP
        zeros = sum(1 for _, _, a, _, _ in rows if a == 0)
        print(
            f"   b = {b}: {len(starts)} lamps; the age moment per lamp (A, GAMEBOARD until read):"
            + "; ".join(f" ({y:+d},{z:+d}) A {a} P {p} lines {ln}" for y, z, a, p, ln in rows)
        )
        print(
            f"     the ring mean of A {mean_a:.2f} (k_ring = {k_ring:.5f}); lamps with no line through them {zeros} of {len(rows)};"
            f" the 3D shell |r - {b}| < 1/2 over {len(shell)} Nodes: A {shell_a:.2f} (k_shell = {k_shell:.5f});"
            f" the continuum's 3 q / (4 pi r) = {continuum_a_r * SCALE / b:.2f} (k_cont = {k_cont:.5f});"
            f" the presence word's ring mean k {float(sum(k_pres, Fraction(0)) / len(rows)):.5f}"
        )
        print(
            f"     the same A at the gr_rows pair [1, 4096]: k_shell x 4 = {k_shell * 4:.4f} against the README's {README_K}"
            f" (11.4 x 16 / 4096); at [1, 16384] the README's number is {README_K / 4:.4f}"
        )
        found[b] = {
            "k_ring": k_ring,
            "k_shell": k_shell,
            "k_cont": k_cont,
            "mean_a": mean_a,
            "count": len(rows),
        }
        if b != 6:
            continue
        print(
            "     the clock's exact births per lamp and series T's reading of them (COMPUTATION, the reading's grain):"
        )
        for window in WINDOWS:
            ticks = window[1]
            per_lamp = []
            for y, z, a, _, _ in rows:
                births = clock_births(a, N_SUSP, D_SUSP, ticks)
                control = clock_births(0, N_SUSP, D_SUSP, ticks)
                read = inverse_slope(births, window) - 1 if a else 0.0
                count_ratio = (
                    sum(1 for t in control if window[0] <= t < window[1])
                    / sum(1 for t in births if window[0] <= t < window[1])
                    - 1
                )
                per_lamp.append((y, z, a, read, count_ratio))
            exact = k_ring
            mean_read = sum(r for _, _, _, r, _ in per_lamp) / len(per_lamp)
            mean_count = sum(c for _, _, _, _, c in per_lamp) / len(per_lamp)
            worst = max(abs(r - float(Fraction(N_SUSP * a, D_SUSP))) for _, _, a, r, _ in per_lamp)
            print(
                f"       the window [{window[0]}, {window[1]}): the ring mean by the inverse slope {mean_read:.5f}"
                f" (exact {exact:.5f}, off by {(mean_read - exact) / exact * 100:+.2f} percent; the worst lamp off its exact k by {worst:.5f});"
                f" by the count ratio of births {mean_count:.5f} ({(mean_count - exact) / exact * 100:+.2f} percent)"
            )
    print()
    return found


def part_2_restated(lamps: dict[int, dict[str, float]]) -> None:
    print(
        "2. THE DECIDING PIN RESTATED ON THE READ k_a(6): alpha from the arrival Nodes over k from the lamp, both clicks"
    )
    q = 290 * SCALE
    k_cont = 3 * q * N_SUSP / (4 * math.pi * D_SUSP * 6)
    alpha_nodes = RING_PIN / 26
    print(
        f"   the run's 0.731 Links = 26 x C_nodes x k_cont(6): 26 x {C_NODES_PIN} x {k_cont:.5f} = {26 * C_NODES_PIN * k_cont:.3f}"
        f" (k_cont the continuum's 3 q n / (4 pi d b) at q = {q}, the one GAMEBOARD input of the chain)"
    )
    print(
        f"   alpha_nodes = 0.731 / 26 = {alpha_nodes:.5f} radians (DETECTOR, the arrival Nodes' mean over 40 starts; the bracket"
        f" {RING_BRACKET / 26:.5f})"
    )
    for name, k in (
        ("k_ring (the 40 lamps' mean)", lamps[6]["k_ring"]),
        ("k_shell (the 3D shell)", lamps[6]["k_shell"]),
        ("k_cont", k_cont),
    ):
        ratio = alpha_nodes / k
        print(
            f"   alpha_nodes / {name} = {alpha_nodes:.5f} / {k:.5f} = {ratio:.3f}; through the lever-arm factor 0.683 the constant"
            f" {ratio / 0.683:.3f} (the run's C_ring {C_RING_PIN} on k_cont), against 2 c_f = 4 on the comparison side"
        )
    k_ring = lamps[6]["k_ring"]
    print(
        f"   THE PIN: the ring of lamps at b = 6 reads the mean count ratio 1 + k with k = {k_ring:.5f} (the algebra's, DETECTOR when read),"
        f" the bracket 3.4 percent of itself ({RING_BRACKET} / {RING_PIN}, the ring's own) beyond the reading's grain of section 1;"
        f" the 0.731 +- 0.025 restated: alpha_nodes = {alpha_nodes / k_ring:.3f} x k_read within the same bracket, i.e. the"
        f" ratio of the two clicks {alpha_nodes / k_ring:.3f} +- {alpha_nodes / k_ring * 0.034 * 2:.3f} (both brackets); FAIL if the read k"
        f" departs from {k_ring:.5f} by more than the bracket, or the ratio of clicks leaves its bracket"
    )
    print()


def walk_ring(
    fan: list, crowd, tables: dict, b: int, gamma: int, half_length: int, q: int
) -> dict[str, float]:
    starts = SAM.ring_starts(b)
    gm = Fraction(q) / (4 * Fraction(D_SUSP, N_SUSP))
    radial_sum = Fraction(0)
    tangential = 0.0
    node_sum = 0.0
    delay_sum = 0
    count = 0
    lost = 0
    moved: dict[int, int] = defaultdict(int)
    table = tables[gamma]
    for y, z in starts:
        base = SAM.walk(table, None, (1, 0, 0), y, z, gamma)
        out = SAM.walk(table, crowd, (1, 0, 0), y, z, gamma)
        if "tangent" not in out or "tangent" not in base:
            lost += 1
            continue
        r = math.sqrt(y * y + z * z)
        p = out["momentum"]
        radial_sum += Fraction(-(p[1] * y + p[2] * z), p[0])
        tangential += float(Fraction(-(p[1] * (-z) + p[2] * y), p[0])) / r
        dy, dz = out["node"][1] - base["node"][1], out["node"][2] - base["node"][2]
        node_sum += -(dy * y + dz * z) / r
        delay_sum += out["age"] - base["age"]
        moved[abs(dy) + abs(dz)] += 1
        count += 1
    c_ring = float(radial_sum / count / (3 * gm) * math.pi)
    c_nodes = (
        node_sum / count / half_length * b * 4 * math.pi * float(Fraction(D_SUSP, N_SUSP)) / (3 * q)
    )
    grain = (1 / half_length) / float(3 * gm / (math.pi * b)) / count
    return {
        "starts": len(starts),
        "count": count,
        "lost": lost,
        "c_ring": c_ring,
        "c_nodes": c_nodes,
        "shift": node_sum / count,
        "tangential": tangential / count,
        "delay": delay_sum / count,
        "grain": grain,
        "moved": dict(moved),
    }


def part_3_trend() -> None:
    print(
        "3. THE WALK'S TREND: THE RING OF STARTS UNDER flow_link AT gamma_PPN = 1 (and 0) AT LARGER b, LARGER L AND A DENSER FAN"
    )
    print(
        "   the same rule, pair and M; the box (-L .. L + 2) x (-20 .. 20)^2 about the mass, the lamps' plane x = -L,"
        " the screen x = L; C_ring = mean(tan alpha_r x r) x 4 pi S / (3 q) on the one constant; the expected"
        " 2 c_f x (the shells' factor of this crowd) x L / sqrt(L^2 + b^2); the grain one Node per start over L and the count"
    )
    cases = ((6, 26), (6, 40), (6, 52), (8, 26))
    impacts = (6, 8, 10, 12, 14)
    for fan_bound, half_length in cases:
        SAM.BOX = ((-half_length, half_length + 2), (-20, 20), (-20, 20))
        SAM.X_LAMP, SAM.X_SCREEN = -half_length, half_length
        SAM.LINKS = 2 * half_length + 60
        fan = SAM.primitive_fan(fan_bound)
        q_lines = len(fan)
        q = q_lines * SCALE
        crowd = FWM.WeightedCrowd(fan, SCALE, FWM.flow_label)
        tables = {g: SAM.Table(fan, SAM.BEAM, g) for g in (0, 1)}
        shells = []
        for r in range(4, 15):
            nodes = FWM.shell_nodes(r)
            total = sum(FWM.norm(crowd.flow.get(k, [0, 0, 0])) / SCALE for k in nodes)
            shells.append(total / len(nodes) * r * r / Q)
        shells_factor = (sum(shells) / len(shells)) / (q_lines / (4 * math.pi))
        age_shells = []
        for r in range(4, 15):
            nodes = FWM.shell_nodes(r)
            age_shells.append(sum(crowd.age_moment.get(k, 0) / SCALE for k in nodes) / len(nodes) * r)
        age_factor = (sum(age_shells) / len(age_shells)) / (3 * q_lines / (4 * math.pi))
        print()
        print(
            f"   THE FAN OF MANHATTAN {fan_bound} ({q_lines} directions, q = {q} units per interval), L = {half_length}:"
            f" the shells' factor of the weighted flow over r = 4 .. 14 is {shells_factor:.3f} (the registered case 0.990),"
            f" the age moment's {age_factor:.3f} (0.993)"
        )
        print(
            "   | b | starts (lost) | gamma | C_ring on the one constant | expected 2 c_f x shells x L / sqrt(L^2 + b^2) |"
            " residual in grains (the grain) | C_ring bare against 2 c_f, percent | tan alpha_r x b (the M / b form) |"
            " the mean radial shift, Links | C_nodes | lever arm | delay | starts moved 0 / 1 / 2 / 3+ |"
        )
        print("   | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |")
        ratios: dict[int, list[float]] = {0: [], 1: []}
        for b in impacts:
            for gamma in (0, 1):
                out = walk_ring(fan, crowd, tables, b, gamma, half_length, q)
                c_f = 1 + gamma
                path = half_length / math.sqrt(half_length**2 + b * b)
                expected = 2 * c_f * shells_factor * path
                residual = (out["c_ring"] - expected) / out["grain"]
                ratios[gamma].append(out["c_ring"] / expected)
                moved = out["moved"]
                print(
                    f"   | {b} | {out['starts']} ({out['lost']}) | {gamma} | {out['c_ring']:.3f} | {expected:.3f} | "
                    f"{residual:+.2f} ({out['grain']:.3f}) | {(out['c_ring'] / (2 * c_f) - 1) * 100:+.1f} | "
                    f"{out['c_ring'] * 3 * q / (4 * math.pi * D_SUSP / N_SUSP):.4f} | {out['shift']:.3f} | {out['c_nodes']:.3f} | "
                    f"{out['c_nodes'] / out['c_ring']:.3f} | {out['delay']:.2f} | "
                    f"{moved.get(0, 0)} / {moved.get(1, 0)} / {moved.get(2, 0)} / {sum(v for k, v in moved.items() if k >= 3)} |"
                )
        for gamma in (0, 1):
            m, sd, _ = FWM.mean_and_spread(ratios[gamma])
            print(
                f"   the five rings' C_ring over the expected at gamma {gamma}: mean {m:.3f}, spread {sd:.3f} (sd), from"
                f" {min(ratios[gamma]):.3f} to {max(ratios[gamma]):.3f}: 2 c_f read within {max(abs(r - 1) for r in ratios[gamma]) * 100:.0f} percent, the comb's"
            )


def main() -> None:
    print("ROW 13 BY THE ALGEBRA BEFORE THE RUN: THE STEP ALGEBRA'S SIMULATION OF THE BOARD, NOT A RUN")
    print(
        "(step_algebra_map.py and flow_weight_map.py imported by their files; c_f = 2 an input, n S = d a declaration,"
        " f_D the hypothesis flow-link-v1; Einstein's 4 on the comparison side only)"
    )
    print()
    lamps = part_1_lamps()
    part_2_restated(lamps)
    part_3_trend()


if __name__ == "__main__":
    main()
