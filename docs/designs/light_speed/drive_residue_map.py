"""The residue of the directional drive across lines (M1 of the physics-rule
review of form B, PR #526) and the correction: the integer map beside
FORM.md section 3.1 (read-only, the mathematician, 2026-09-21). Nothing
built, nothing run; the engine's `by_drive` is the one primitive imported.

(A) Form B as built (BEAM_LAW note 49 on the branch `directional-drive`:
one accumulator on the line of D with the rate |p|_1 S_1 Q and the wall
Q S M S_1 Q + |p|_1 T_D, the Bresenham deficits of the line), spelled here
in the same integers: the residue carried across lines at a constant |p|_1
fires Links at one per interval on the shorter line (M1), and the deficits
carried across lines put Links on an axis the new momentum does not have
(M1b, found here). (B) The correction (c) of FORM.md 3.1: three signed
accumulators, one per axis, with the rate p_a Q and the one wall Q^2 S M +
|p|_1 T_h, T_h = isqrt(3 Q^2) = 110 the heading's resolution, one Link per
interval on the axis furthest over its wall; the reviewer's pins on it.
(C) The pace of the two forms on three directions, and the cap over every
primitive direction within 8.

Run from the repository root with PYTHONPATH=src:

    python docs/designs/light_speed/drive_residue_map.py > docs/designs/light_speed/drive_residue_map.out
"""

from __future__ import annotations

import math
from itertools import product

from event_universe.core.integer import by_drive

Q = 64
T_H = math.isqrt(3 * Q * Q)  # 110, the heading's resolution
Vec = tuple[int, int, int]


def isqrt3(v: Vec) -> int:
    return math.isqrt(3 * sum(c * c for c in v) * Q * Q)


def primitive(p: list[int]) -> Vec:
    g = math.gcd(math.gcd(abs(p[0]), abs(p[1])), abs(p[2]))
    return (p[0] // g, p[1] // g, p[2] // g)


def manhattan(p: list[int] | Vec) -> int:
    return sum(abs(c) for c in p)


# --- form B as built -------------------------------------------------------------


def line_step(deficits: list[int], direction: Vec) -> int:
    """`engine.line_step` of the branch: every deficit gains |D_a|, the
    largest (the lowest axis on a tie) is stepped and loses S_1."""
    for axis in range(3):
        deficits[axis] += abs(direction[axis])
    chosen = max(range(3), key=lambda a: (deficits[a], -a))
    deficits[chosen] -= manhattan(direction)
    return chosen


class FormB:
    """The directional drive as built, for momenta whose primitive is
    within the bound (the direction read is then the primitive itself)."""

    def __init__(self, content: int, width: int, bound: int = 64) -> None:
        self.content, self.width, self.bound = content, width, bound
        self.drive = 0
        self.deficits = [0, 0, 0]
        self.direction: Vec = (0, 0, 0)

    def step(self, p: list[int]) -> tuple[int, int] | None:
        heading = primitive(p)
        assert max(abs(c) for c in heading) <= self.bound
        if heading != self.direction:
            if sum(a * b for a, b in zip(self.direction, heading, strict=True)) < 0:
                self.drive = -self.drive
            self.direction = heading
        s1, t_d = manhattan(heading), isqrt3(heading)
        rate = manhattan(p) * s1 * Q
        wall = Q * self.width * self.content * s1 * Q + manhattan(p) * t_d
        fired, self.drive = by_drive(self.drive, rate, wall, at_most=1)
        if not fired:
            return None
        axis = line_step(self.deficits, heading)
        return axis, fired * (1 if heading[axis] > 0 else -1)


# --- the correction (c) ------------------------------------------------------------


class PerAxis:
    """Three signed accumulators with one wall: rate_a = p_a Q, wall = Q^2 S M
    + |p|_1 T_h; every accumulator advances at every self-creation; one
    Link per interval at most, on the axis furthest over the wall (the
    lowest axis on a tie), the others keeping their overflow for the
    following intervals. No direction read, no deficits."""

    def __init__(self, content: int, width: int) -> None:
        self.content, self.width = content, width
        self.drives = [0, 0, 0]

    def wall(self, p: list[int]) -> int:
        return Q * Q * self.width * self.content + manhattan(p) * T_H

    def step(self, p: list[int]) -> tuple[int, int] | None:
        wall = self.wall(p)
        for axis in range(3):
            self.drives[axis] += p[axis] * Q
        over = [a for a in range(3) if abs(self.drives[a]) >= wall]
        if not over:
            return None
        chosen = max(over, key=lambda a: (abs(self.drives[a]), -a))
        sign = 1 if self.drives[chosen] > 0 else -1
        self.drives[chosen] -= sign * wall
        return chosen, sign


def links(steps: list[tuple[int, int] | None]) -> list[int]:
    total = [0, 0, 0]
    for st in steps:
        if st:
            total[st[0]] += st[1]
    return total


M, S = 64, 1
print("(A) Form B as built, M = 64, S = 1 (Q S M = 4096).")
print("  M1: a body at |p|_1 = 6000 on the line (3, 1, 2) for 200 intervals, then the same")
print("      |p|_1 on the heading (1, 0, 0):")
body = FormB(M, S)
p_line, p_head = [3000, 1000, 2000], [6000, 0, 0]
for _ in range(200):
    body.step(p_line)
wall_line = Q * S * M * 6 * Q + 6000 * isqrt3((3, 1, 2))
wall_head = Q * S * M * 1 * Q + 6000 * T_H
print(
    f"      the residue after 200 intervals {body.drive} of the line's wall {wall_line}"
    f" ({body.drive / wall_line:.3f} Link on the line); read on the heading's wall {wall_head}:"
    f" {body.drive / wall_head:.3f} Links, the ratio of the walls {wall_line / wall_head:.3f}"
)
burst = [body.step(p_head) for _ in range(12)]
print(
    "      the Links on the heading in the next 12 intervals: "
    + " ".join("x" if st else "." for st in burst)
    + f" ({sum(1 for st in burst if st)} of 12; the pace earned there {6000 * Q / wall_head:.3f})"
)
print("  M1b: a body on the line (1, 64, 0) (|p|_1 = 6500) until its x deficit reaches 30,")
print("       then the momentum (0, 6500, 0), purely along +y:")
body = FormB(M, S)
p_line = [100, 6400, 0]
switch = 0
while not (body.deficits[0] >= 30 and body.deficits[0] >= body.deficits[1]):
    body.step(p_line)
    switch += 1
print(f"       the switch at interval {switch}, the deficits {body.deficits}")
after = [body.step([0, 6500, 0]) for _ in range(200)]
first_y = next(i for i, st in enumerate(after) if st and st[0] == 1)
print(
    f"       the Links after the switch: {links(after[:first_y])} before the first y Link,"
    f" which comes at interval {first_y + 1}: {first_y and links(after[:first_y])[0]} Links on -x"
    " for a momentum with no x component (the deficit's sign rule gives -1 on an axis D lacks)"
)

print()
print("(B) The correction (c): three accumulators, one wall Q^2 S M + |p|_1 T_h.")
print("  The reviewer's pin 1: a constant |p|_1 = 6000 with a wandering direction (the")
print("  components cycling every 50 intervals through (6000, 0, 0), (3000, 1000, 2000),")
print("  (0, 6000, 0), (2000, 2000, 2000), (-3000, -1000, 2000)); the Links on every axis")
print("  against floor(sum_t p_a(t) Q / wall) at every n over 1000 intervals:")
cycle = [[6000, 0, 0], [3000, 1000, 2000], [0, 6000, 0], [2000, 2000, 2000], [-3000, -1000, 2000]]
body_c = PerAxis(M, S)
body_b = FormB(M, S)
wall = body_c.wall(cycle[0])
exact = [0, 0, 0]
count_c = [0, 0, 0]
count_b = [0, 0, 0]
worst_c = 0
worst_b = 0
worst_total_b = 0.0
exact_b = 0.0
for n in range(1000):
    p = cycle[(n // 50) % len(cycle)]
    st = body_c.step(p)
    if st:
        count_c[st[0]] += st[1]
    st = body_b.step(p)
    if st:
        count_b[st[0]] += st[1]
    heading = primitive(p)
    s1, t_d = manhattan(heading), isqrt3(heading)
    exact_b += manhattan(p) * s1 * Q / (Q * S * M * s1 * Q + manhattan(p) * t_d)
    for a in range(3):
        exact[a] += p[a] * Q
        floor_a = exact[a] // wall if exact[a] >= 0 else -((-exact[a]) // wall)
        worst_c = max(worst_c, abs(count_c[a] - floor_a))
    worst_total_b = max(worst_total_b, abs(sum(abs(c) for c in count_b) - exact_b))
print(f"  the wall {wall} (constant: |p|_1 constant); the correction's Links per axis {count_c},")
print(
    f"  the exact whole parts {[e // wall for e in exact]}: the largest deviation at any n {worst_c} Link"
)
print(
    f"  form B as built on the same momenta: {count_b} Links, {sum(abs(c) for c in count_b)} in all against"
    f" the distance driven {exact_b:.2f}: the largest deviation at any n {worst_total_b:.2f} Links"
)
print("  The reviewer's pin 2: a one-interval hand-over transient, p = (1000, 0, 0) with")
print("  (1000, -500, 0) at one interval and (1000, 0, 0) again:")
body_c = PerAxis(M, S)
for _ in range(100):
    body_c.step([1000, 0, 0])
before = list(body_c.drives)
body_c.step([1000, -500, 0])
transient = list(body_c.drives)
for _ in range(100):
    body_c.step([1000, 0, 0])
print(
    f"  the y accumulator after the transient {transient[1]} of the wall {body_c.wall([1000, 0, 0])}"
    f" ({transient[1] / body_c.wall([1000, 0, 0]):.4f} Link, kept as the residue; no Link on y in the"
    f" following 100 intervals: {body_c.drives[1] == transient[1]}); the x accumulator unaffected beyond"
    f" the wall's change for that interval ({before[0]} -> {transient[0]})"
)
print("  The pin 2 on form B as built: the same transient reads the line (2, -1, 0) for one")
print("  interval, the residue re-read twice:")
body_b = FormB(M, S)
for _ in range(100):
    body_b.step([1000, 0, 0])
r0 = body_b.drive
w_head = Q * S * M * Q + 1000 * T_H
w_line = Q * S * M * 3 * Q + 1500 * isqrt3((2, -1, 0))
body_b.step([1000, -500, 0])
r1 = body_b.drive
print(
    f"  the residue {r0} ({r0 / w_head:.4f} Link on the heading) read on the line's wall {w_line}:"
    f" {r0 / w_line:.4f} Link; after the interval {r1} ({r1 / w_line:.4f} of the line, then"
    f" {r1 / w_head:.4f} of the heading): the distance the body holds changed by"
    f" {r1 / w_head - (r0 / w_head + 1000 * Q / w_head):+.4f} Link beyond what the interval earned"
)

print()
print("(C) The pace on three directions (Euclidean, in units of the rows' 64 / 110 on a")
print("    heading), p = k Q S M along D, form B against the correction:")
print("  p / (Q S M) | D | form B | correction (c)")
for k in (0.0625, 0.25, 1, 3, 9):
    row = []
    for d in ((1, 0, 0), (1, 1, 0), (1, 1, 1)):
        p1 = k * Q * S * M * manhattan(d) / math.sqrt(sum(c * c for c in d))  # |p|_2 = k Q S M
        s1, t_d = manhattan(d), isqrt3(d)
        v_b = p1 * s1 * Q / (Q * S * M * s1 * Q + p1 * t_d) * math.sqrt(sum(c * c for c in d)) / s1
        v_c = p1 * Q / (Q * Q * S * M + p1 * T_H) * math.sqrt(sum(c * c for c in d)) / s1
        row.append((v_b / (Q / T_H), v_c / (Q / T_H)))
    print(
        f"  {k:<11g} | (1,0,0) {row[0][0]:.3f} {row[0][1]:.3f} | (1,1,0) {row[1][0]:.3f} {row[1][1]:.3f}"
        f" | (1,1,1) {row[2][0]:.3f} {row[2][1]:.3f}"
    )
print("  The cap over every primitive direction within 8 (the limit |p| -> infinity): the")
print("  correction's Euclidean pace |D| Q / (S_1 T_h) against the rows' |D| Q / T_D on the line:")
worst = 0.0
count = 0
equal = 0
for d in product(range(-8, 9), repeat=3):
    if d == (0, 0, 0) or math.gcd(math.gcd(abs(d[0]), abs(d[1])), abs(d[2])) != 1:
        continue
    count += 1
    norm = math.sqrt(sum(c * c for c in d))
    body_cap = norm * Q / (manhattan(d) * T_H)
    row_cap = norm * Q / isqrt3(d)
    worst = max(worst, body_cap / row_cap)
    equal += body_cap == row_cap
print(
    f"  {count} directions: the body's cap over the row's at most {worst:.4f} (equality on the {equal}"
    f" headings), the smallest {min(math.sqrt(sum(c * c for c in d)) / manhattan(d) for d in ((1, 1, 1),)) * Q / T_H / (Q / T_H):.4f}"
    " of the heading's on the cube diagonal"
)
