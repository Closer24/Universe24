"""The auditor's round-9 question on series D (the orbit against the shell
law): why the inward legs read 1.52 shell means per interval against the
crossing rule's Doppler 1.18, and the outward legs 1.08 against 0.73. The
crossing rule (docs/designs/crossing/DESIGN.md section 2: C1 the swap, C2
the entered Node's residents against the step, C2' with it, C3 the
arrivals, C3' came with the body, C3'' the leapfrog) is transcribed on
series D's own geometry (examples/events/orbit/make_worlds.py: the plane,
the fan of 120 in-plane directions, one shell of 120 rows every 10
intervals, the rows on the engine's own digital lines, `direction_flight`
and `unit_label` the two imports), and a reader is moved on prescribed
paths: radially inward and outward on the axis and on an oblique line at
one Link per k intervals, and on an orbit-like path (the tangential speed
of the S = 32 orbit with a radial drift in and out). Per interval the rows
met by the rule are counted with their labels, and the inward push read is
compared with the rest reading at the same Nodes and with the shell law
q L / N(r_t) (the auditor's normalisation), beside the Doppler 1 -+ v_r / c
with c = 32 / 55. The rows read twice, if any, are listed. Host arithmetic,
no run; every number a derivation of what the GameBoard would read
(GAMEBOARD, the probe's push), labelled.

Run from the repository root:

    PYTHONPATH=src python docs/designs/orbit_read/orbit_read_map.py > docs/designs/orbit_read/orbit_read_map.out
"""

from __future__ import annotations

import importlib.util
import math
from collections import defaultdict
from pathlib import Path

import numpy as np

from event_universe.events.nature_beam import Q, direction_flight, unit_label

ROOT = Path(__file__).resolve().parents[3]
spec = importlib.util.spec_from_file_location(
    "orbit_worlds", ROOT / "examples" / "events" / "orbit" / "make_worlds.py"
)
orbit = importlib.util.module_from_spec(spec)
spec.loader.exec_module(orbit)

FAN = [tuple(v) for v in orbit.FAN]
CENTRE = orbit.CENTRE[:2]
SIDE = orbit.SIDE
CADENCE = orbit.RELEASE_D // orbit.SOURCE  # one shell every 10 intervals
C_LIGHT = 32 / 55
MAX_AGE = 160
HEADINGS = [(1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)]
TABLE = HEADINGS + [v for v in FAN if v not in HEADINGS]
flight = direction_flight(tuple(TABLE))
INDEX = {d: i for i, d in enumerate(TABLE)}
UNIT = {d: np.array(unit_label(d)[:2], dtype=float) / Q for d in FAN}


def positions(d):
    """The point of the line of d at every age 0 .. MAX_AGE, relative to the source."""
    i = INDEX[d]
    ages = np.arange(MAX_AGE + 2)
    made = flight.manhattan_steps(np.full(len(ages), i), ages)
    s1 = int(flight.manhattan[i])
    line = flight.lines[i, :s1]
    out = []
    for m in made.tolist():
        whole, part = divmod(m, s1)
        p = whole * flight.vectors[i] + line[:part].sum(axis=0)
        out.append((int(p[0]), int(p[1])))
    return out


POS = {d: positions(d) for d in FAN}
q_per_interval = len(FAN) / CADENCE


def ring_count(r):
    n = 0
    for x in range(-r - 1, r + 2):
        for y in range(-r - 1, r + 2):
            if abs(math.hypot(x, y) - r) < 0.5:
                n += 1
    return n


RING = {r: ring_count(r) for r in range(2, 45)}


def shell_law(r):
    """The mean inward push per interval on the ring at r, q L / N(r) in units of Q (L = 1)."""
    return q_per_interval / RING[round(r)]


# The rows: every direction, one row per CADENCE intervals; birth ticks b = 0 mod CADENCE.
def row_pos(d, b, t):
    a = t - b
    if a < 0 or a > MAX_AGE:
        return None
    x, y = POS[d][a]
    return (CENTRE[0] + x, CENTRE[1] + y)


def rest_inward(node):
    """The inward push per interval at rest at `node`: every line through it
    delivers one row per CADENCE intervals, read once at its arrival."""
    rx, ry = node[0] - CENTRE[0], node[1] - CENTRE[1]
    r = math.hypot(rx, ry)
    total = 0.0
    lines = 0
    for d in FAN:
        if any((CENTRE[0] + x, CENTRE[1] + y) == node for x, y in POS[d]):
            u = UNIT[d]
            total += (u[0] * rx + u[1] * ry) / r
            lines += 1
    return total / CADENCE, lines


def read_path(path, t0=200):
    """Apply the crossing rule along `path` (a list of Nodes, one per interval
    from tick t0, consecutive Nodes equal or one Link apart). Returns per
    interval the inward push read, the tallies, and the rows read twice."""
    births = list(range(-MAX_AGE - CADENCE, t0 + len(path) + CADENCE, CADENCE))
    R = {t0 - 1: path[0], t0 - 2: path[0]}
    mark = {t0 - 1: (0, 0)}
    inward = []
    tally = defaultdict(int)
    ever = defaultdict(list)
    for k, X in enumerate(path):
        t = t0 + k
        origin = R[t - 1]
        e = (X[0] - origin[0], X[1] - origin[1])
        R[t] = X
        mark[t] = e
        rx, ry = X[0] - CENTRE[0], X[1] - CENTRE[1]
        r = math.hypot(rx, ry)
        push = 0.0
        for d in FAN:
            u = UNIT[d]
            for b in births:
                p1 = row_pos(d, b, t)
                if p1 is None:
                    continue
                p0 = row_pos(d, b, t - 1)
                s1 = None if p0 is None else (p1[0] - p0[0], p1[1] - p0[1])
                arrived = s1 is not None and s1 != (0, 0)
                met = None
                if e != (0, 0):
                    if p1 == origin and arrived and s1 == (-e[0], -e[1]):
                        met = "C1"
                    elif p1 == X:
                        if not arrived:
                            if u[0] * e[0] + u[1] * e[1] < 0:
                                met = "C2"
                            else:
                                tally["C2' skipped"] += 1
                        elif s1 == e:
                            tally["C3' skipped"] += 1
                        else:
                            met = "C3"
                else:
                    if p1 == X and arrived:
                        ep = mark[t - 1]
                        p_2 = row_pos(d, b, t - 2)
                        s2 = None if (p0 is None or p_2 is None) else (p0[0] - p_2[0], p0[1] - p_2[1])
                        if ep != (0, 0) and s1 == ep and s2 == (0, 0):
                            tally["C3'' skipped"] += 1
                        else:
                            met = "C3"
                if met:
                    tally[met] += 1
                    ever[(d, b)].append((t, met, X, t0))
                    push += (u[0] * rx + u[1] * ry) / r
        inward.append(push)
    twice = {key: v for key, v in ever.items() if len(v) > 1}
    return inward, tally, twice


def report(name, path, note=""):
    inward = None
    tally = defaultdict(int)
    twice = {}
    for phase in range(CADENCE):
        inward_p, tally_p, twice_p = read_path(path, t0=200 + phase)
        inward = inward_p if inward is None else [a + b for a, b in zip(inward, inward_p, strict=True)]
        for key, v in tally_p.items():
            tally[key] += v
        twice.update(twice_p)
    inward = [v / CADENCE for v in inward]
    radii = [math.hypot(x - CENTRE[0], y - CENTRE[1]) for x, y in path]
    read = sum(inward) / len(inward)
    law = sum(shell_law(r) for r in radii) / len(radii)
    rest = sum(rest_inward(n)[0] for n in path) / len(path)
    dr = (radii[-1] - radii[0]) / (len(path) - 1)
    doppler = 1 - dr / C_LIGHT
    print(f"   {name}{note}")
    print(
        f"      {len(path)} intervals, r {radii[0]:.1f} -> {radii[-1]:.1f}, <v_r> {dr:+.3f} Links per interval ({dr / C_LIGHT:+.3f} c); the Doppler 1 - v_r / c = {doppler:.3f}"
    )
    print(
        f"      the inward push read {read:.4f} per interval; the shell law {law:.4f}; the rest reading at the same Nodes {rest:.4f}"
    )
    print(
        f"      C_shell = read / law = {read / law:.3f}; read / rest = {read / rest:.3f}; rest / law = {rest / law:.3f}"
    )
    print(
        f"      the tallies over the {CADENCE} shell phases {dict(sorted(tally.items()))}; rows read twice: {len(twice)}"
    )
    for key, v in list(twice.items())[:3]:
        print(f"         twice: direction {key[0][:2]} born {key[1]}: {v}")
        t_a, t_b = v[0][0], v[-1][0]
        base = v[0][3]
        # the reader's Nodes and the row's positions around the two reads
        for t in range(t_a - 2, t_b + 1):
            i = t - base
            reader = path[i] if 0 <= i < len(path) else None
            print(
                f"            tick {t}: the row at {row_pos(key[0], key[1], t)}, the reader at {reader}"
            )
    return read / law, read / rest, rest / law


def radial_path(direction, r_from, r_to, k):
    """The reader stepping one Link per k intervals along the digital line of
    `direction` from radius r_from to r_to (inward when r_to < r_from)."""
    d = direction
    i = INDEX[d]
    s1 = int(flight.manhattan[i])
    line = flight.lines[i, :s1]
    nodes = []
    p = np.zeros(2, dtype=int)
    for m in range(0, 400):
        whole, part = divmod(m, s1)
        p = whole * np.array(d[:2]) + line[:part, :2].sum(axis=0)
        nodes.append((int(p[0]), int(p[1])))
    lo, hi = sorted((r_from, r_to))
    ring = [n for n in nodes if lo - 0.5 <= math.hypot(*n) <= hi + 0.5]
    if r_to < r_from:
        ring = ring[::-1]
    path = []
    for n in ring:
        path.extend([(CENTRE[0] + n[0], CENTRE[1] + n[1])] * k)
    return path


def orbit_path(r0, v_t, v_r, intervals, sense):
    """An orbit-like lattice path: the ideal point on a circle of radius r0
    drifting radially at v_r (sense -1 inward, +1 outward), the reader
    stepping one axis per interval toward it (x before y), as the drive
    steps one Link at a time."""
    path = []
    x, y = CENTRE[0] + r0, CENTRE[1]
    theta = 0.0
    r = float(r0)
    for _t in range(intervals):
        theta += v_t / r
        r += sense * v_r
        ix, iy = CENTRE[0] + r * math.cos(theta), CENTRE[1] + r * math.sin(theta)
        dx, dy = ix - x, iy - y
        if abs(dx) >= 0.5 and abs(dx) >= abs(dy):
            x += 1 if dx > 0 else -1
        elif abs(dy) >= 0.5:
            y += 1 if dy > 0 else -1
        path.append((x, y))
    return path


print("A. SERIES D'S GEOMETRY AND THE SHELL LAW (host)")
print(
    f"   the fan {len(FAN)} in-plane directions, one shell every {CADENCE} intervals: q = {q_per_interval:.0f} rows per interval; c = 32 / 55 = {C_LIGHT:.4f}"
)
print(
    "   the ring counts N(r): "
    + ", ".join(f"{r}: {RING[r]}" for r in (4, 6, 8, 12, 16, 20, 24, 30, 40))
    + " (DERIVATIONS_BEAM 3.2's 32, 40, 48, 68, 112, 112, 144, 200, 264)"
)
n_real, n_whole = orbit.orbit_momentum(32)
v_t = n_whole / (32 + n_whole)
print(
    f"   the S = 32 orbit: n = {n_whole} label units, the tangential pace n / (S + n) = {v_t:.3f} Links per interval ({v_t / C_LIGHT:.2f} c); the auditor's inward legs at v_r / c = 0.16 to 0.23, that is v_r = {0.16 * C_LIGHT:.3f} to {0.23 * C_LIGHT:.3f} Links per interval"
)
print(
    "   the rest reading at a Node against the shell law (the grain): "
    + ", ".join(
        f"({x - CENTRE[0]}, {y - CENTRE[1]}) {rest_inward((x, y))[0] / shell_law(math.hypot(x - CENTRE[0], y - CENTRE[1])):.2f} on {rest_inward((x, y))[1]} lines"
        for x, y in [
            (CENTRE[0] + 12, CENTRE[1]),
            (CENTRE[0] + 24, CENTRE[1]),
            (CENTRE[0] + 10, CENTRE[1] + 7),
            (CENTRE[0] + 17, CENTRE[1] + 17),
            (CENTRE[0] + 20, CENTRE[1] + 9),
        ]
    )
)
print()

print(
    "B. A READER STEPPING RADIALLY ON THE AXIS, ONE LINK PER k INTERVALS (the crossing rule as written)"
)
for k in (5, 8, 10):
    report(f"inward on -x from r = 28 to 10, k = {k}", radial_path((-1, 0, 0), 28, 10, k))
    report(f"outward on +x from r = 10 to 28, k = {k}", radial_path((1, 0, 0), 10, 28, k))
print()

print("C. A READER STEPPING RADIALLY ON AN OBLIQUE LINE OF THE FAN, k = 8")
for d in ((-1, -1, 0), (-2, -1, 0), (-5, -2, 0), (-3, -7, 0)):
    dd = (-d[0], -d[1], 0)
    report(f"inward along {d[:2]} from r = 28 to 10", radial_path(d, 28, 10, 8))
    report(f"outward along {dd[:2]} from r = 10 to 28", radial_path(dd, 10, 28, 8))
print()

print(
    "D. AN ORBIT-LIKE PATH: THE TANGENTIAL PACE OF THE S = 32 ORBIT WITH A RADIAL DRIFT (v_r = 0.11 Links per interval, 0.19 c)"
)
for r0, name in ((24, "from r = 24 inward"), (14, "from r = 14 outward")):
    sense = -1 if "inward" in name else 1
    report(name + " over 90 intervals", orbit_path(r0, v_t, 0.11, 90, sense))
report("a circle at r = 19, no drift, 120 intervals", orbit_path(19, v_t, 0.0, 120, 1))

print()
print("E. THE MANHATTAN FACTOR: A DIGITAL LINE CROSSES THE UNIT-WIDE RING AT S_1 / |D| NODES (host)")
manhattan_mean = sum((abs(a) + abs(b)) / math.hypot(a, b) for a, b, _ in FAN) / len(FAN)
print(
    f"   the fan's mean S_1 / |D| = {manhattan_mean:.4f} (a fan uniform in angle gives 4 / pi = {4 / math.pi:.4f}); series C's six headings give exactly 1"
)
for r in (8, 12, 16, 20, 24, 28):
    nodes = [
        (CENTRE[0] + x, CENTRE[1] + y)
        for x in range(-r - 1, r + 2)
        for y in range(-r - 1, r + 2)
        if abs(math.hypot(x, y) - r) < 0.5
    ]
    readings = [rest_inward(n) for n in nodes]
    mean = sum(v for v, _ in readings) / len(nodes)
    visits = sum(lines for _, lines in readings)
    on_none = sum(1 for _, lines in readings if lines == 0)
    print(
        f"   r = {r:2d}: N(r) = {len(nodes)}, the lines' Node-visits on the ring {visits} ({visits / len(FAN):.3f} per line), {on_none} Nodes on no line; the ring mean of the rest reading over q L / N(r) = {mean / shell_law(r):.3f}"
    )
print()
print("F. THE AUDITOR'S LEGS RE-READ: THE MANHATTAN FACTOR TIMES THE DOPPLER (host)")
for name, doppler, read in (
    ("inward, all four worlds (1536 intervals)", 1.18, 1.52),
    ("outward, all four worlds (2310 intervals)", 0.73, 1.08),
):
    print(
        f"   {name}: the auditor's C_shell {read:.2f} against the Doppler {doppler:.2f}; {manhattan_mean:.3f} x {doppler:.2f} = {manhattan_mean * doppler:.3f}; the map's read / rest on the orbit-like path {'1.135' if 'inward' in name else '0.880'} x {manhattan_mean:.3f} = {manhattan_mean * (1.135 if 'inward' in name else 0.880):.3f}"
    )
print(
    f"   the ratio inward / outward: the auditor's {1.52 / 1.08:.3f}; the Doppler's {1.18 / 0.73:.3f}; the map's orbit-like path {1.361 / 1.180:.3f} (read / law) and {1.135 / 0.880:.3f} (read / rest)"
)
print()
print("G. WHAT FOLLOWS FOR SERIES D'S PIN: THE FLOW CONSTANT C ON THE FAN (host)")
a1 = orbit.EMISSION * orbit.LABEL_MAGNITUDE * 1.0 / (2 * math.pi)
for C in (1.0, manhattan_mean):
    a = a1 * C
    n = (a + math.sqrt(a * a + 4 * 32 * a)) / 2
    print(
        f"   C = {C:.3f}: the S = 32 circular-orbit momentum n = {n:.2f} label units (the whole {round(n)}), the pace {round(n) / (32 + round(n)):.3f}, the period at r = 12: {2 * math.pi * 12 * (32 + round(n)) / round(n):.0f} intervals, at r = 24: {2 * math.pi * 24 * (32 + round(n)) / round(n):.0f}"
    )
