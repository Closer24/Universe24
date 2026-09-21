"""An independent count of the crossing rule on the streams beyond the axis
(DESIGN.md section 5 (c); the implementer, 2026-09-21), written before the
engine ran `tests/test_crossing.py` (c): rows on parallel digital lines of
one direction, one row per interval per line, every Node of the plane (but
one corner) on exactly one line; a body at (40, 40) stepping +x once per k
intervals. The rule is transcribed from DESIGN.md section 2 (C1, C2, C2',
C3, C3', C3'') on the lines' geometry; the flight is the engine's own
`Flight` (the positions off the age); no reading code of the engine is
used. Integers only. Its output on 2026-09-21: the transverse stream 32 in
32; (1, 1, 0) with the step 24 in 32, the pattern 1, 1, 1, 0, 0, 1, 1, 1;
(-1, 1, 0) against the step 36 in 32, 2 at the ticks 4, 12, 20, 28 (C1); no
row twice, no resident row against the step at any entered Node.

    PYTHONPATH=src python docs/designs/crossing/crossing_2d.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "src"))
import numpy as np  # noqa: E402

from event_universe.events.nature_beam import direction_flight

SIDE = 64
K = 4
TICKS = 32
START = (40, 40)


def positions(flight, index, ages):
    """The point of the line at each age: the sum of the first m unit steps."""
    made = flight.manhattan_steps(np.full(len(ages), index), np.array(ages))
    line = flight.lines[index, : max(1, int(flight.manhattan[index]))]
    s1 = int(flight.manhattan[index])
    out = []
    for m in made.tolist():
        whole, part = divmod(m, s1)
        p = whole * flight.vectors[index] + line[:part].sum(axis=0)
        out.append((int(p[0]), int(p[1])))
    return out


def lamps_for(vector):
    """Lamps so that every Node lies on exactly one digital line of `vector`."""
    if vector == (0, 1, 0):
        return [(x, 0) for x in range(SIDE)]
    if vector == (1, 1, 0):
        # lines from (x0, 0), x0 even, and (0, y0), y0 even >= 2
        return [(x, 0) for x in range(0, SIDE, 2)] + [(0, y) for y in range(2, SIDE, 2)]
    if vector == (-1, 1, 0):
        return [(x, 0) for x in range(SIDE - 1, -1, -2)] + [(SIDE - 1, y) for y in range(2, SIDE, 2)]
    raise ValueError(vector)


def run(vector, ticks=TICKS, k=K, verbose=False):
    table = (
        (0, 0, 0),
        (0, 0, 0),
        (1, 0, 0),
        (-1, 0, 0),
        (0, 1, 0),
        (0, -1, 0),
        (0, 0, 1),
        (0, 0, -1),
        vector,
    )
    flight = direction_flight(table)
    index = 8
    u = np.array(vector[:2], dtype=float)
    u = u / np.linalg.norm(u)
    # the stream: per lamp, rows of birth b <= 0 pre-filled (ages 0.. while on board) and births 1..ticks
    max_age = 400
    rel = positions(flight, index, list(range(max_age + 2)))
    rows = []  # (lamp, birth)
    for lamp in lamps_for(vector):
        for b in range(-max_age, ticks + 1):
            rows.append((lamp, b))

    def pos(lamp, b, t):
        a = t - b
        if a < 0:
            return None
        if a > max_age:
            return None
        p = (lamp[0] + rel[a][0], lamp[1] + rel[a][1])
        if not (0 <= p[0] < SIDE and 0 <= p[1] < SIDE):
            return None
        return p

    # check: every Node on exactly one line (at t = 0, count rows per Node over a window)
    R = {0: START}
    mark = {0: (0, 0)}
    reads = {}
    ever = {}
    for t in range(1, ticks + 1):
        e = (1, 0) if t % k == 0 else (0, 0)
        R[t] = (R[t - 1][0] + e[0], R[t - 1][1] + e[1])
        mark[t] = e
        X, origin = R[t], R[t - 1]
        got = []
        for lamp, b in rows:
            p1, p0 = pos(lamp, b, t), pos(lamp, b, t - 1)
            if p1 is None:
                continue
            s1 = None if p0 is None else (p1[0] - p0[0], p1[1] - p0[1])
            arrived = s1 is not None and s1 != (0, 0)
            if e != (0, 0):
                # C1: at O, crossed the Link backward
                if p1 == origin and arrived and s1 == (-e[0], -e[1]):
                    got.append((lamp, b, "C1"))
                    continue
                if p1 != X:
                    continue
                if not arrived:
                    if u[0] * e[0] + u[1] * e[1] < 0:
                        got.append((lamp, b, "C2"))
                    continue
                if s1 == e:
                    continue  # C3'
                got.append((lamp, b, "C3"))
            else:
                if p1 != X or not arrived:
                    continue
                ep = mark[t - 1]
                p_2 = pos(lamp, b, t - 2)
                s2 = None if (p0 is None or p_2 is None) else (p0[0] - p_2[0], p0[1] - p_2[1])
                if ep != (0, 0) and s1 == ep and s2 == (0, 0):
                    continue  # C3''
                got.append((lamp, b, "C3"))
        reads[t] = got
        for lamp, b, _ in got:
            ever.setdefault((lamp, b), []).append(t)
    twice = {k_: v for k_, v in ever.items() if len(v) > 1}
    per_step = {t: [tag for _, _, tag in reads[t]] for t in reads if t % k == 0}
    counts = [len(reads[t]) for t in range(1, ticks + 1)]
    return counts, twice, per_step


if __name__ == "__main__":
    for vector in ((0, 1, 0), (1, 1, 0), (-1, 1, 0)):
        counts, twice, per_step = run(vector)
        print(vector, "total", sum(counts), "per tick", counts, "twice", len(twice))
        print("   at the steps:", {t: sorted(v) for t, v in per_step.items()})
