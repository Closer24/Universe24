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


if __name__ == "__main__":
    main()
