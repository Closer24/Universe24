"""The host map of `drive-b-v1`, the directional drive of a body (form B in
the integer form (c) of light_speed/FORM.md section 3.1): the pins of the
deciding worlds computed from the rule's integers BEFORE any run of the
engine, the refuting numbers of the per-axis drive `main` runs, the
reviewer's two pins of record 348, the cap on every direction and the
accumulators' bound. Every number here is a HOST computation of the count
rule (a replay of the integer arithmetic on the body's own record, not a
detector reading and not a run); the runs of the registered worlds read
the same numbers after a face detector, or refute them.

Run: python docs/designs/drive_b/drive_b_map.py > docs/designs/drive_b/drive_b_map.out
"""

from __future__ import annotations

import math

Q = 64  # the label's scale (world.LABEL_SCALE)
T_H = math.isqrt(3 * Q * Q)  # 110, the flight table's resolution on a heading, formed at load
S, M = 1, 64  # the deciding worlds' width and content: Q S M = 4096, Q^2 S M = 262144
BOX = 41  # the deciding worlds' GameBoard, 41 x 41 x 41, the body at its centre
CENTRE = BOX // 2  # 20
P1 = 6000  # |p|_1 of the three deciding worlds

Vec = tuple[int, int, int]


def manhattan(p: list[int]) -> int:
    return sum(abs(c) for c in p)


def euclid(p: list[int]) -> float:
    return math.sqrt(sum(c * c for c in p))


# --- the rule under the key ----------------------------------------------------------


class DriveB:
    """`drive-b-v1`: three signed accumulators on the body's record, the rate
    p_a Q on each, ONE wall W = Q^2 S M + |p|_1 T_h (Q^2 S M alone under
    `covariant_readings`, the cap term keyed off as `step_divisor` keys it
    off today); every accumulator whose momentum component is not 0
    advances at every self-creation; at most one Link per interval, on the
    axis furthest over the wall (the lowest axis on a tie), with the
    accumulator's sign; that accumulator loses W with the Link's sign, the
    others keep their overflow for the following self-creations (the
    coincident fire deferred, never dropped). A component of 0 leaves its
    accumulator as it is and never steps (note 17's rule); p = 0 never
    steps. The same integers as light_speed/drive_residue_map.py's
    `PerAxis` (the mathematician's (c))."""

    def __init__(self, content: int, width: int, cap: bool = True) -> None:
        self.content, self.width, self.cap = content, width, cap
        self.drives = [0, 0, 0]
        self.largest = 0  # the largest |drive_a| seen, against the bound

    def wall(self, p: list[int]) -> int:
        return Q * Q * self.width * self.content + (manhattan(p) * T_H if self.cap else 0)

    def step(self, p: list[int]) -> tuple[int, int] | None:
        wall = self.wall(p)
        for axis in range(3):
            if p[axis]:
                self.drives[axis] += p[axis] * Q
        over = [a for a in range(3) if p[a] and abs(self.drives[a]) >= wall]
        chosen = None
        if over:
            chosen = max(over, key=lambda a: (abs(self.drives[a]), -a))
            sign = 1 if self.drives[chosen] > 0 else -1
            self.drives[chosen] -= sign * wall
        self.largest = max(self.largest, max(abs(d) for d in self.drives))
        return None if chosen is None else (chosen, sign)


class PerAxisMain:
    """The per-axis drive `main` runs (BEAM_LAW note 17 as amended, the step
    drive; engine._move): per axis `by_drive(drive_a, p_a, Q S M + |p_a|,
    at_most 1)`; every axis advances; the first axis whose count is not 0
    makes the Link, a later axis's coincident fire is lost (its D
    subtracted, no Link crossed)."""

    def __init__(self, content: int, width: int) -> None:
        self.content, self.width = content, width
        self.drives = [0, 0, 0]
        self.lost = 0

    def step(self, p: list[int]) -> tuple[int, int] | None:
        fired = None
        for axis in range(3):
            if p[axis] == 0:
                continue
            divisor = Q * self.width * self.content + abs(p[axis])
            self.drives[axis] += p[axis]
            count = abs(self.drives[axis]) // divisor
            count = min(count, 1)
            if self.drives[axis] < 0:
                count = -count
            self.drives[axis] -= count * divisor
            if count and fired is None:
                fired = (axis, count)
            elif count:
                self.lost += 1
        return fired


def escape(body: DriveB | PerAxisMain, p: list[int], ticks: int) -> dict[str, object]:
    """The body from the centre of the open box: the tick and face of its
    escape (the click's Node the last Node inside), the Links per axis made
    before it, and every Node's distance from the line of p (the largest
    over the walk, in Links, a GameBoard diagnostic)."""
    position = [CENTRE, CENTRE, CENTRE]
    links = [0, 0, 0]
    farthest = 0.0
    norm = euclid(p)
    for tick in range(1, ticks + 1):
        st = body.step(p)
        if st is None:
            continue
        axis, sign = st
        links[axis] += sign
        if not 0 <= position[axis] + sign < BOX:
            face = ("+" if sign > 0 else "-") + "xyz"[axis]
            return {
                "tick": tick,
                "face": face,
                "node": list(position),
                "links": links,
                "off_line": round(farthest, 3),
            }
        position[axis] += sign
        # The distance of the Node from the line through the centre along p.
        r = [position[a] - CENTRE for a in range(3)]
        along = sum(r[a] * p[a] for a in range(3)) / norm
        farthest = max(farthest, math.sqrt(max(0.0, sum(c * c for c in r) - along * along)))
    return {
        "tick": None,
        "face": None,
        "node": list(position),
        "links": links,
        "off_line": round(farthest, 3),
    }


WORLDS = {
    "axis": [P1, 0, 0],
    "plane": [P1 // 2, P1 // 2, 0],
    "cube": [P1 // 3, P1 // 3, P1 // 3],
}

print("drive-b-v1: the host map of the directional drive (HOST computations of the count rule; no run)")
print(f"Q = {Q}, T_h = isqrt(3 Q^2) = {T_H}; the deciding worlds M = {M}, S = {S}: Q S M = {Q * S * M},")
print(
    f"Q^2 S M = {Q * Q * S * M}; |p|_1 = {P1}, the wall W = Q^2 S M + |p|_1 T_h = {Q * Q * S * M + P1 * T_H}"
)
print(
    f"the box {BOX}^3 open, the body at ({CENTRE}, {CENTRE}, {CENTRE}); the escape through a face is the DETECTOR reading"
)
print()

print(
    "(A) The deciding worlds: the pace, the escape and the line, under the key and on main's per-axis drive."
)
print("    pace per axis = |p_a| Q / W Links per interval (the key); |p_a| / (Q S M + |p_a|) (main).")
W = Q * Q * S * M + P1 * T_H
for name, p in WORLDS.items():
    per_axis_b = [abs(c) * Q / W for c in p]
    per_axis_main = [abs(c) / (Q * S * M + abs(c)) if c else 0.0 for c in p]
    print(f"  {name:5s} p = {p}: |p|_2 = {euclid(p):.1f}")
    print(
        f"    the key : pace per axis {[round(v, 4) for v in per_axis_b]}, Manhattan {manhattan(p) * Q / W:.4f},"
        f" Euclidean {euclid(p) * Q / W:.4f} Links per interval"
    )
    b = escape(DriveB(M, S), p, 400)
    first = math.ceil(21 * W / (abs(p[0]) * Q))
    print(
        f"              escape at tick {b['tick']} through face {b['face']} from Node {b['node']} after the Links {b['links']};"
        f" the 21st x fire alone would be at ceil(21 W / (|p_x| Q)) = {first} (the deferral {b['tick'] - first} interval)"
    )
    print(
        f"              every Node within {b['off_line']} Link of the line of p (GAMEBOARD, the step lines)"
    )
    m = PerAxisMain(M, S)
    r = escape(m, p, 400)
    print(
        f"    main    : pace per axis {[round(v, 4) for v in per_axis_main]}; escape at tick {r['tick']} through {r['face']}"
        f" from Node {r['node']} after the Links {r['links']}; coincident fires lost {m.lost};"
        f" farthest from the line of p {r['off_line']} Links"
    )
print()

print(
    "(B) The reviewer's pins of record 348 replayed with this map's rule (must equal light_speed/drive_residue_map.out (B)):"
)
cycle = [[6000, 0, 0], [3000, 1000, 2000], [0, 6000, 0], [2000, 2000, 2000], [-3000, -1000, 2000]]
body = DriveB(M, S)
exact = [0, 0, 0]
count = [0, 0, 0]
worst = 0
for n in range(1000):
    p = cycle[(n // 50) % len(cycle)]
    st = body.step(p)
    if st:
        count[st[0]] += st[1]
    for a in range(3):
        exact[a] += p[a] * Q
        floor_a = exact[a] // W if exact[a] >= 0 else -((-exact[a]) // W)
        worst = max(worst, abs(count[a] - floor_a))
print(f"  pin 1: |p|_1 = 6000 wandering over five lines, 1000 intervals: the Links per axis {count},")
print(
    f"         the whole parts floor(sum_t p_a(t) Q / W) {[e // W for e in exact]}, the largest deviation at any n {worst} Link"
)
body = DriveB(M, S)
p0 = [6000, 0, 0]
for _ in range(50):
    body.step(p0)
before = list(body.drives)
fired = body.step([6000, -720, 0])  # the transient: a hand-over of 720 label units on y for one interval
residue_y = body.drives[1]  # the momentum back on the axis from the next interval
later = 0
for _ in range(100):
    st = body.step(p0)
    later += 1 if st and st[0] == 1 else 0
print(
    f"  pin 2: a hand-over transient of -720 on y for the one interval 51 (fired: {fired}) leaves the y residue {residue_y}"
)
print(
    f"         = {residue_y / W:+.4f} Link (at most |delta_y| Q / W = {720 * Q / W:.4f}), and fires no y Link in the 100 intervals after ({later} fired)"
)
print()

print("(C) The cap (record 301's condition: no body outruns its family's rows on any line).")
print("    the body's Euclidean pace |p|_2 Q / W <= Q / T_h = 64 / 110 = 0.5818 on every direction;")
print("    on the line of D the body at most |D| Q / (S_1 T_h) against the rows' |D| Q / T_D there:")
for d in [(1, 0, 0), (1, 1, 0), (1, 1, 1), (2, 1, 0), (3, 1, 2)]:
    s1 = manhattan(list(d))
    t_d = math.isqrt(3 * sum(c * c for c in d) * Q * Q)
    body_cap = euclid(list(d)) * Q / (s1 * T_H)
    rows = euclid(list(d)) * Q / t_d
    print(
        f"    D = {d}: S_1 = {s1}, T_D = {t_d}: the body at most {body_cap:.4f}, the rows {rows:.4f}, the ratio {body_cap / rows:.4f}"
    )
print(
    f"    today's per-axis drive on a heading: |p| / (Q S M + |p|) -> 1 Link per interval = {1 / (Q / T_H):.2f} c (the defect of record 301)"
)
print(
    f"    at |p|_1 = {P1} on the axis today's pace {P1 / (Q * S * M + P1):.4f} > the rows' {Q / T_H:.4f}; under the key {P1 * Q / W:.4f}"
)
print()

print(
    "(D) Newton's limit and the isotropy: at |p|_1 << Q S M the pace per axis is p_a / (Q S M) x Q / (Q + |p|_1 T_h / (Q S M)):"
)
for p in ([64, 0, 0], [32, 32, 0], [24, 24, 24]):
    w = Q * Q * S * M + manhattan(p) * T_H
    print(
        f"    p = {p}: Euclidean pace {euclid(p) * Q / w:.6f} against |p|_2 / (Q S M) = {euclid(p) / (Q * S * M):.6f}, the ratio {(euclid(p) * Q / w) / (euclid(p) / (Q * S * M)):.5f}"
    )
print()

print(
    "(E) Under `covariant_readings` and the key together: W = Q^2 S M (the cap term off), the domain |p|_1 <= Q S M;"
)
print(
    "    the J4 muon's |p|_2 = 3640 (17.6 M2) put on the plane and the cube diagonals (the chief physicist's worlds, record 642):"
)
E0 = Q * S * 207
for p in ([3640, 0, 0], [2574, 2574, 0], [2101, 2101, 2101]):
    w = Q * Q * S * 207
    square = E0 * E0 + 3 * sum(c * c for c in p)
    energy = math.isqrt(square)
    print(
        f"    p = {p}: |p|_1 = {manhattan(p)} <= Q S M = {E0}: admitted; |p|_2 = {euclid(p):.1f}; E' = isqrt(W) = {energy} (gamma {energy / E0:.4f});"
        f" pace per self-creation per axis {[round(abs(c) * Q / w, 4) for c in p]}, Euclidean {euclid(p) * Q / w:.4f};"
        f" per lattice interval x E'_0 / E' = {euclid(p) * Q / w * E0 / energy:.4f}"
    )
print()

print(
    "(F) The accumulators' bound: the largest |drive_a| seen in (A) and (B), against W and the working bound 2^63 - 1:"
)
for name, p in WORLDS.items():
    body = DriveB(M, S)
    escape(body, p, 400)
    print(
        f"    {name:5s}: largest |drive_a| {body.largest} = {body.largest / W:.3f} W, below W + 2 max|p_a| Q = {W + 2 * max(abs(c) for c in p) * Q}"
    )
body = DriveB(M, S)
for n in range(1000):
    body.step(cycle[(n // 50) % len(cycle)])
print(
    f"    the wandering body of (B): largest |drive_a| {body.largest} = {body.largest / W:.3f} W, below W + 2 x 6000 Q = {W + 2 * 6000 * Q}"
)
print(
    "    (observed, not proved: an axis over the wall waits at most while the two others are further over)"
)
print(
    "    the check before every addition: |drive_a| + |p_a| Q within 2^62 - 1 (`bounded`), else refused naming the rule;"
)
print(
    "    the wall's two products Q^2 S M and |p|_1 T_h tested by division before they are formed, at load and at every push."
)
