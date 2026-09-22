"""The pins of the deciding world of every family under one wall (the chief
physicist, 2026-09-22; docs/designs/one_wall/EVERY_FAMILY.md section 2): a
slow massive row on the heading at the impact distance b beside series K's
mass, on the lattice's own lines. The crowd's lines, the flow **V** and the
age moment A at every Node are the light-bending map's
(docs/designs/open_problems/light_bending/light_bending_map.py, run here
with its printing silenced). The row is followed Link by Link along its
own momentum, as the rule as built walks it: at each x-Link its momentum
**P** = Q d content **p**_D + **W** (label units) takes the crowd's push
**W** -= n content w **V** per interval of dwell at the weight per unit w =
(E'^2 + 3 gamma p . p) // E' (the content the family's quantum), the time
per x-Link is E'(**P**) (d + f n A) / (d
|P_x|) with E'(**P**) = sqrt((Q d content E'_0)^2 + 3 |**P**|^2) the pair's
wall over its rate (the Manhattan length cancels between them), and its y
moves by P_y / P_x per x-Link (Bresenham along **P**); the crowd is read
at the Node the row is at. So the arrival time carries the wall's stretch
AND the speed-up of a falling row (|**P**| grows under the push: the first
form of this map, the unpushed dwell, missed it, and at b = 6 the row
reached the mass's own line 21 Links past the mass, before the screen:
the first run's finding, its naive pin refuted by the geometry). The
shift is the row's y at the screen less its lamp's; the delay the arrival
time less the control's (52 x E' / p). GAMEBOARD arithmetic of the
declaration, before any run; the generator's expectations.json restates
the chosen world's numbers (examples/events/optical/make_worlds.py).

    python docs/designs/one_wall/every_family_map.py > docs/designs/one_wall/every_family_map.out
"""

from __future__ import annotations

import contextlib
import io
import math
from pathlib import Path

HERE = Path(__file__).resolve().parent
LIGHT_MAP = HERE.parent / "open_problems" / "light_bending" / "light_bending_map.py"
PAIR_D = 16384
SCREEN_LINKS = 26


def light_bending_lines() -> dict[str, object]:
    """The light-bending map's namespace (its FLOW, AGE_MOMENT, X_LAMP,
    X_SCREEN, Q, N_PIN), computed once, its own printing silenced."""
    namespace: dict[str, object] = {"__name__": "light_bending_map", "__file__": str(LIGHT_MAP)}
    with contextlib.redirect_stdout(io.StringIO()):
        exec(compile(LIGHT_MAP.read_text(encoding="utf-8"), str(LIGHT_MAP), "exec"), namespace)
    return namespace


def follow(
    lines: dict[str, object],
    b: int,
    scale: int,
    gamma: int,
    quantum: int,
    p: int,
    *,
    wall_factor: int | None = None,
    weight_form: str = "energy",
    pace: str = "pushed",
) -> tuple[float, float, float, float]:
    """One row from the lamp (x = -26) to the screen (x = +26) at the height
    b: (the shift in pixels, the arrival time in intervals, the control's
    arrival time, the final angle in radians). `wall_factor` overrides f =
    1 + gamma on the massive wall (0: the wall unstretched, the reading
    that would refute the composition's verb 1); `weight_form` "energy" is
    the rule's (E'^2 + 3 gamma p^2) // E', "light" the light-blind (1 +
    gamma) E' (the reading that would refute verb 2); `pace` "pushed" is
    the rule's (the time per x-Link on the pushed momentum's energy and
    x component), "unpushed" holds the pace at the family's own p / E'
    on the Manhattan length walked while the push still bends the row
    (the reading that would refute the speed-up of a falling row, the
    momentum's pace)."""
    flow = lines["FLOW"]  # type: ignore[assignment]
    age_moment = lines["AGE_MOMENT"]  # type: ignore[assignment]
    q, n = int(lines["Q"]), int(lines["N_PIN"])  # type: ignore[arg-type]
    x_lamp, x_screen = int(lines["X_LAMP"]), int(lines["X_SCREEN"])  # type: ignore[arg-type]
    d = PAIR_D
    e0 = q * quantum
    e_row = math.isqrt(e0 * e0 + 3 * p * p)
    if weight_form == "energy":
        w = (e_row * e_row + 3 * gamma * p * p) // e_row
    else:
        w = (1 + gamma) * e_row
    f = 1 + gamma if wall_factor is None else wall_factor
    k = q * d * quantum  # Q d content: the scale of P and of the rest term
    px, py = k * p, 0.0
    rest = k * e0
    y = float(b)
    time = 0.0
    for dx in range(x_lamp, x_screen):
        node = (dx, int(round(y)), 0)
        v = flow.get(node, [0, 0, 0])  # type: ignore[union-attr]
        a = age_moment.get(node, 0) * scale  # type: ignore[union-attr]
        energy = math.sqrt(rest * rest + 3 * (px * px + py * py))
        if pace == "pushed":
            dwell = energy * (d + f * n * a) / (d * abs(px))  # intervals per x-Link
        else:
            # the unpushed pace E' / p on the Manhattan length walked (the y-Links
            # paid at that pace too), the wall's stretch kept
            dwell = e_row * (d + f * n * a) * (abs(px) + abs(py)) / (d * p * abs(px))
        # the push over the dwell at this Node, both components: n x content x
        # w x V, the row's content its quantum (the weight w per unit of amount)
        px -= n * quantum * w * v[0] * scale * dwell
        py -= n * quantum * w * v[1] * scale * dwell
        y += py / px
        time += dwell
    control = (x_screen - x_lamp) * e_row / p
    return y - b, time, control, math.atan2(-py, px)


# -- the engine's integer walk on the stationary crowd (the follow-up of
# EVERY_FAMILY.md section 6: the map walks as the engine walks) ----------
FAN_NEIGHBOURS = 6
BEAM = ((1, 0, 0), (24, 1, 0), (24, -1, 0), (12, 1, 0), (12, -1, 0))


def scaled_label(vector: tuple[int, int, int], scale: int) -> tuple[int, int, int]:
    """world.scaled_label: the integer vector nearest scale x D / |D|."""
    n = sum(c * c for c in vector)
    if n == 0 or scale == 0:
        return (0, 0, 0)
    out = []
    for a in vector:
        k = (math.isqrt((2 * scale * abs(a)) ** 2 // n) + 1) // 2
        out.append(k if a > 0 else -k)
    return (out[0], out[1], out[2])


def bresenham(vector: tuple[int, int, int]) -> list[tuple[int, int, int]]:
    """The S_1 unit steps of one period of the digital line (nature_beam)."""
    s1 = sum(abs(c) for c in vector)
    line: list[tuple[int, int, int]] = []
    position = [0, 0, 0]
    for j in range(s1):
        best = max(range(3), key=lambda i: (abs(vector[i]) * (j + 1) - s1 * abs(position[i]), -i))
        step = [0, 0, 0]
        step[best] = 1 if vector[best] > 0 else -1
        position[best] += step[best]
        line.append((step[0], step[1], step[2]))
    return line


def fan_neighbours(vectors: list[tuple[int, int, int]]) -> list[list[int]]:
    """nature_beam.fan_neighbours: per direction its six nearest moving
    directions within a right angle, by the exact comparison of cosines."""
    import functools

    norms = [sum(c * c for c in v) for v in vectors]
    table: list[list[int]] = []
    for index, vector in enumerate(vectors):
        candidates = []
        for other, candidate in enumerate(vectors):
            if other == index or norms[other] == 0:
                continue
            dot = sum(a * b for a, b in zip(vector, candidate, strict=True))
            if dot > 0:
                candidates.append((dot, norms[other], other))

        def nearer(left, right):
            lhs, rhs = left[0] * left[0] * right[1], right[0] * right[0] * left[1]
            if lhs != rhs:
                return -1 if lhs > rhs else 1
            return -1 if left[2] < right[2] else (1 if left[2] > right[2] else 0)

        candidates.sort(key=functools.cmp_to_key(nearer))
        table.append([other for _, _, other in candidates[:FAN_NEIGHBOURS]])
    return table


class IntegerWalk:
    """The tables of the deciding world's direction set (the fan of 290
    with the beam's four, as series K declares them) for one massive
    family: the labels p_D, the triple, the lines, the neighbours."""

    def __init__(self, lines: dict[str, object], quantum: int, p: int):
        fan = [tuple(v) for v in lines["FAN"]]  # type: ignore[union-attr]
        self.vectors = fan + [v for v in BEAM if v not in set(fan)]
        self.index = {v: i for i, v in enumerate(self.vectors)}
        self.q = int(lines["Q"])  # type: ignore[arg-type]
        self.rest = self.q * quantum  # E'_0 = Q S M at S = 1
        self.labels = [scaled_label(v, p) for v in self.vectors]
        self.energy = [
            math.isqrt(self.rest * self.rest + 3 * sum(c * c for c in lb)) for lb in self.labels
        ]
        self.rate = [2 * sum(abs(c) for c in lb) for lb in self.labels]
        self.wall = [2 * e for e in self.energy]
        self.lines = [bresenham(v) for v in self.vectors]
        self.neighbours = fan_neighbours(self.vectors)

    def weight(self, d: int, gamma: int, form: str) -> int:
        e = self.energy[d]
        if form == "energy":
            return (e * e + 3 * gamma * sum(c * c for c in self.labels[d])) // e
        return (1 + gamma) * e


def momentum_pair(momentum: list[int], rest: int, q: int) -> tuple[int, int]:
    """nature_beam.momentum_pair: (S_1, T) of P and R over their gcd."""
    g = math.gcd(*momentum, rest)
    primitive = [c // g for c in momentum]
    r = rest // g
    return sum(abs(c) for c in primitive), math.isqrt(
        (r * r + 3 * sum(c * c for c in primitive)) * q * q
    )


def walk(
    lines: dict[str, object],
    b: int,
    scale: int,
    gamma: int,
    quantum: int,
    p: int,
    *,
    crowd: bool = True,
    wall_factor: int | None = None,
    weight_form: str = "energy",
    tables: IntegerWalk | None = None,
    start: tuple[int, int, int] = (1, 0, 0),
) -> tuple[int, float, int]:
    """One row of the massive family from the lamp to the screen by the
    engine's verbs, integer for integer, on the stationary crowd of the
    light-bending map (its mean flow and age moment at every Node, the
    one approximation left): per interval the walk (the accumulator at
    the rate x d against the wall x (d + f n A), one Link at most, the
    Link the label's Bresenham step at the row's place), then the push
    (W -= n content w V at the Node reached, the residue rescaled to the
    momentum's rate), then the label (among D and its fan neighbours the
    one whose next Link keeps |c + h x P|^2 smallest, P conserved). The
    click: (the shift in whole pixels, the time of the Link onto the
    screen, the Links walked)."""
    t = tables or IntegerWalk(lines, quantum, p)
    flow = lines["FLOW"]  # type: ignore[assignment]
    age_moment = lines["AGE_MOMENT"]  # type: ignore[assignment]
    n = int(lines["N_PIN"])  # type: ignore[arg-type]
    x_lamp, x_screen = int(lines["X_LAMP"]), int(lines["X_SCREEN"])  # type: ignore[arg-type]
    d_s = PAIR_D
    f = 1 + gamma if wall_factor is None else wall_factor
    q = t.q
    content = quantum  # amount 1, content the quantum
    d = t.index[start]  # the beam's line the row is born on
    node = [x_lamp, b, 0]
    made = 0
    pushed = False
    w_acc = [0, 0, 0]
    cross = [0, 0, 0]
    residue = t.energy[d] * d_s  # the fresh start: the table's start E'_D, times d
    age = 0

    def pair_of(direction: int) -> tuple[int, int]:
        if not pushed:
            return t.rate[direction], t.wall[direction]
        label = q * d_s * content
        momentum = [label * t.labels[direction][a] + w_acc[a] for a in range(3)]
        s1, big_t = momentum_pair(momentum, label * t.rest, q)
        return 2 * s1 * q, 2 * big_t

    while True:
        age += 1
        # verb 1, the walk: the age moment at the row's Node before the step
        a = age_moment.get(tuple(node), 0) * scale if crowd else 0  # type: ignore[union-attr]
        rate0, wall0 = pair_of(d)
        rate, wall = rate0 * d_s, wall0 * (d_s + f * n * a)
        residue += rate
        if residue >= wall:
            residue -= wall
            h = t.lines[d][made % len(t.lines[d])]
            made += 1
            node = [node[i] + h[i] for i in range(3)]
            if pushed:
                label = q * d_s * content
                momentum = [label * t.labels[d][i] + w_acc[i] for i in range(3)]
                cross = [
                    cross[0] + h[1] * momentum[2] - h[2] * momentum[1],
                    cross[1] + h[2] * momentum[0] - h[0] * momentum[2],
                    cross[2] + h[0] * momentum[1] - h[1] * momentum[0],
                ]
            if node[0] >= x_screen:
                r = rate0 * d_s
                return node[1] - b, age - residue / r, made
        if not crowd:
            continue
        # verb 2, the push at the Node reached
        v = flow.get(tuple(node), [0, 0, 0])  # type: ignore[union-attr]
        if any(v):
            old_rate = pair_of(d)[0]
            w = t.weight(d, gamma, weight_form)
            for i in range(3):
                w_acc[i] -= n * content * w * v[i] * scale
            pushed = True
            new_rate = pair_of(d)[0]
            residue = residue * new_rate // old_rate
            # verb 3, the label along P
            label = q * d_s * content
            momentum = [label * t.labels[d][i] + w_acc[i] for i in range(3)]
            best, best_error = d, -1
            for candidate in [d, *t.neighbours[d]]:
                h = t.lines[candidate][made % len(t.lines[candidate])]
                if h[0] * momentum[0] + h[1] * momentum[1] + h[2] * momentum[2] <= 0:
                    continue
                e = [
                    cross[0] + h[1] * momentum[2] - h[2] * momentum[1],
                    cross[1] + h[2] * momentum[0] - h[0] * momentum[2],
                    cross[2] + h[0] * momentum[1] - h[1] * momentum[0],
                ]
                error = e[0] * e[0] + e[1] * e[1] + e[2] * e[2]
                if best_error < 0 or error < best_error:
                    best, best_error = candidate, error
            if best != d:
                for i in range(3):
                    w_acc[i] += label * (t.labels[d][i] - t.labels[best][i])
                d = best


def integer_section() -> None:
    lines = light_bending_lines()
    print("\n  the engine's integer walk on the stationary crowd (the follow-up of section 6; the mean")
    print("  crowd the one approximation left): the shift in whole pixels, the arrival against the")
    print("  control's, the Links walked; GAMEBOARD arithmetic, the engine's own readings beside")
    for quantum, p in ((1, 10), (2, 20)):
        t = IntegerWalk(lines, quantum, p)
        heading = t.index[(1, 0, 0)]
        print(
            f"\n  the family: quantum {quantum}, p = {p}; the heading's neighbours "
            f"{[t.vectors[i] for i in t.neighbours[heading]]}"
        )
        for b in (6, 10):
            _, control, links0 = walk(lines, b, 4, 0, quantum, p, crowd=False, tables=t)
            for gamma in (0, 1):
                shift, time, links = walk(lines, b, 4, gamma, quantum, p, tables=t)
                print(
                    f"    M = 2^14, b = {b:2d}, gamma {gamma}: the shift {shift:+d} px, the arrival "
                    f"{time - control:+.2f} intervals (the control {control:.2f} at {links0} Links; "
                    f"{links} Links walked)"
                )
    t = IntegerWalk(lines, 1, 10)
    _, control, _ = walk(lines, 10, 4, 0, 1, 10, crowd=False, tables=t)
    unstretched = walk(lines, 10, 4, 1, 1, 10, wall_factor=0, tables=t)
    blind = walk(lines, 10, 4, 1, 1, 10, weight_form="light", tables=t)
    print(
        f"    the readings that refute at b = 10 by the integer walk: the massive wall unstretched, "
        f"the gamma 1 arrival {unstretched[1] - control:+.2f} ({unstretched[0]:+d} px); the weight "
        f"blind to the speed, the gamma 1 shift {blind[0]:+d} px ({blind[1] - control:+.2f})"
    )
    # The deciding world of the beam's width (EVERY_FAMILY.md section 6, the
    # second follow-up): the lamp births on series K's five beam directions;
    # per line the integer walk's pixel and arrival against that line's own
    # control, and the beam's means, the pins of that world before its run.
    print("\n  the beam's five lines (the heading and (24, +-1, 0), (12, +-1, 0)) by the integer walk,")
    print("  quantum 1, p = 10, M = 2^14: per line the shift and the arrival against its own control;")
    print("  the beam's mean shift and mean arrival, the pins of the beam-width world; the wall")
    print("  unstretched beside (the reading that would refute verb 1 on matter)")
    for b in (10, 12, 14):
        for gamma in (0, 1):
            rows = []
            for line in BEAM:
                _, control, _ = walk(lines, b, 4, 0, 1, 10, crowd=False, tables=t, start=line)
                shift, time, links = walk(lines, b, 4, gamma, 1, 10, tables=t, start=line)
                flat = walk(lines, b, 4, gamma, 1, 10, wall_factor=0, tables=t, start=line)
                rows.append((line, shift, time - control, links, flat[0], flat[1] - control))
            mean_shift = sum(r[1] for r in rows) / len(rows)
            mean_arrival = sum(r[2] for r in rows) / len(rows)
            mean_flat = sum(r[5] for r in rows) / len(rows)
            per_line = "; ".join(
                f"{r[0]}: {r[1]:+d} px, {r[2]:+.2f} ({r[3]} Links; unstretched {r[4]:+d} px, {r[5]:+.2f})"
                for r in rows
            )
            print(
                f"    b = {b:2d}, gamma {gamma}: the mean shift {mean_shift:+.2f} px, the mean arrival "
                f"{mean_arrival:+.2f} intervals (unstretched {mean_flat:+.2f}); {per_line}"
            )


def main() -> None:
    lines = light_bending_lines()
    print("Every family under one wall, the deciding world: a slow massive row beside series K's")
    print(f"mass at the pair [1, {PAIR_D}], followed along its momentum on the crowd's lines")
    print("(the light-bending map, section E); the shift in pixels toward the mass, the arrival")
    print("time against the control's, DETECTOR if run; GAMEBOARD arithmetic before any run.")
    for quantum, p in ((1, 10), (2, 20)):
        e0 = 64 * quantum
        e = math.isqrt(e0 * e0 + 3 * p * p)
        print(
            f"\n  the family: quantum {quantum}, p = {p}, E'_0 = {e0}, E' = {e}, v^2 = "
            f"{3 * p * p / (e * e):.4f}, the dwell per Link {e / p:.2f} intervals (light 1.72)"
        )
        for scale in (4, 2):
            for b in (6, 8, 10, 12):
                out = []
                for gamma in (0, 1):
                    shift, time, control, angle = follow(lines, b, scale, gamma, quantum, p)
                    out.append((gamma, shift, time - control, angle))
                s0, s1 = out[0][1], out[1][1]
                d0, d1 = out[0][2], out[1][2]
                print(
                    f"    M = 2^{12 + int(math.log2(scale))}, b = {b:2d}: gamma 0 the shift {s0:+.2f} px, "
                    f"the arrival {d0:+.2f} intervals, the angle {out[0][3]:.3f} rad; gamma 1 {s1:+.2f} px, "
                    f"{d1:+.2f} intervals, {out[1][3]:.3f} rad; the shifts' ratio {s1 / s0:.3f}, "
                    f"the arrivals' difference {d1 - d0:+.2f}"
                )
    print("\n  the readings that refute, at the chosen world (quantum 1, p = 10, M = 2^14):")
    for b in (10, 12):
        base0 = follow(lines, b, 4, 0, 1, 10)
        base1 = follow(lines, b, 4, 1, 1, 10)
        unstretched = follow(lines, b, 4, 1, 1, 10, wall_factor=0)
        blind = follow(lines, b, 4, 1, 1, 10, weight_form="light")
        unpushed = follow(lines, b, 4, 0, 1, 10, pace="unpushed")
        print(
            f"    b = {b}: the rule: gamma 1 less gamma 0 arrival {base1[1] - base0[1]:+.2f} intervals, "
            f"the shifts' ratio {base1[0] / base0[0]:.3f}; the massive wall unstretched: the gamma 1 "
            f"arrival {unstretched[1] - unstretched[2]:+.2f} (the rule's {base1[1] - base1[2]:+.2f}); "
            f"the weight blind to the speed, (1 + gamma) E': the gamma 1 shift {blind[0]:+.2f} px "
            f"(the rule's {base1[0]:+.2f}); the pace unpushed (no speed-up): the gamma 0 arrival "
            f"{unpushed[1] - unpushed[2]:+.2f} (the rule's {base0[1] - base0[2]:+.2f})"
        )
    integer_section()


if __name__ == "__main__":
    main()
