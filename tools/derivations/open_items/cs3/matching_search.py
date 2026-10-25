"""cs3's search for the matching board (integers only): a light pattern on the 4-cube, z(k) = A i^p(k) with the quarter turn per interval (the exact eigenmode of the gap-0 line at the vacuum: the six neighbours' unit phasors sum to 0 at every Node), whose passing Links (the gap-0 re line's current F not 0 AND the twist h not 0, as close.meet reads them through event_universe.links) form a PERFECT MATCHING of the 64 Nodes: every Node the end of exactly one passing Link, so that one child lands at every Node in one close and the lay's crowd refuses nothing.

The reduction: p(x, y, z) = p1(x, y) + c z with c in {1, 3} (the plane wave along z cancels its own two neighbours, i + 1/i = 0, so the eigenmode condition is the 2D one on p1 over the 4 x 4 torus: the four neighbours' phasors sum to 0); the z-Links carry F and no twist (u independent of z), the x- and y-Links pass where F is not 0 and the transverse current turns along the Link. The 2D eigenmodes are enumerated by backtracking with p1(0, 0) = 0 (the global phase), every eigenmode's 3D passing set measured, the perfect matchings and the partial ones (every degree at most 1) listed.

Usage: python matching_search.py <out.txt> [sense 1|-1]   (sense 1: before = i now, cs1's; -1: before = -i now, cs2's)"""

from __future__ import annotations

import json
import sys
from itertools import product

import numpy as np

from event_universe.core.ports import AXES, across
from event_universe.links import link_current, twist
from event_universe.rows import Line, zeros

N = 4
RE = (1, 0, -1, 0)
IM = (0, 1, 0, -1)
A = 135


def eigenmodes_2d() -> list[tuple[int, ...]]:
    """Every p1 on the 4 x 4 torus with p1(0, 0) = 0 whose four neighbours' phasors sum to 0 at every Node (backtracking, row-major)."""
    cells = [(x, y) for x in range(N) for y in range(N)]
    found: list[tuple[int, ...]] = []
    p = [-1] * (N * N)

    def idx(x: int, y: int) -> int:
        return (x % N) * N + (y % N)

    def ok(x: int, y: int) -> bool:
        nb = [idx(x + 1, y), idx(x - 1, y), idx(x, y + 1), idx(x, y - 1)]
        if any(p[n] < 0 for n in nb):
            return True
        re = sum(RE[p[n]] for n in nb)
        im = sum(IM[p[n]] for n in nb)
        return re == 0 and im == 0

    def rec(k: int) -> None:
        if k == len(cells):
            found.append(tuple(p))
            return
        x, y = cells[k]
        choices = (0,) if k == 0 else (0, 1, 2, 3)
        for v in choices:
            p[idx(x, y)] = v
            # the Nodes whose neighbourhood this cell completes: its four neighbours and itself
            if all(ok(*c) for c in ((x, y), (x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1))):
                rec(k + 1)
            p[idx(x, y)] = -1

    rec(0)
    return found


def lines_of(p: np.ndarray, sense: int) -> Line:
    """The gap-0 re line at the pattern: now = A Re i^p, before = A Re i^(p + sense)."""
    now = zeros(p.shape)
    before = zeros(p.shape)
    for at in np.ndindex(*p.shape):
        q = int(p[at])
        now[at] = A * RE[q]
        before[at] = A * RE[(q + sense) % 4]
    return Line(now, before, None, 1)


def passing(p: np.ndarray, sense: int) -> tuple[list[np.ndarray], list[np.ndarray], list[np.ndarray]]:
    """Per axis: F on the +a Link of every Node, the twist h, and the pass mask (both not 0)."""
    line = lines_of(p, sense)
    fs, hs, ms = [], [], []
    for axis in range(AXES):
        f = link_current(line, 2 * axis)
        h = twist(line, axis)
        fs.append(f)
        hs.append(h)
        ms.append(np.vectorize(lambda a, b: 1 if (int(a) != 0 and int(b) != 0) else 0, otypes=[object])(f, h))
    return fs, hs, ms


def degrees(ms: list[np.ndarray], fs: list[np.ndarray]) -> tuple[np.ndarray, np.ndarray]:
    """Every Node's degree in the passing graph and its in-degree (the passing Links whose current flows into it)."""
    deg = zeros(ms[0].shape)
    indeg = zeros(ms[0].shape)
    for axis in range(AXES):
        m = ms[axis]
        deg = deg + m + across(m, 2 * axis + 1)
        into_plus = np.vectorize(lambda a, b: 1 if (int(a) == 1 and int(b) > 0) else 0, otypes=[object])(m, fs[axis])
        into_self = np.vectorize(lambda a, b: 1 if (int(a) == 1 and int(b) < 0) else 0, otypes=[object])(m, fs[axis])
        indeg = indeg + into_self + across(into_plus, 2 * axis + 1)
    return deg, indeg


def main(argv: list[str]) -> None:
    sys.set_int_max_str_digits(0)
    sense = int(argv[argv.index("sense") + 1]) if "sense" in argv else 1
    modes = eigenmodes_2d()
    lines = [f"2D eigenmodes on the 4x4 torus with p1(0,0) = 0: {len(modes)}"]
    perfect = []
    partial = []
    cycles = []
    by_degree_profile: dict[str, int] = {}
    for p1 in modes:
        for c in (1, 3):
            p = zeros((N, N, N))
            for x, y, z in product(range(N), repeat=3):
                p[x, y, z] = (p1[x * N + y] + c * z) % 4
            fs, hs, ms = passing(p, sense)
            deg, indeg = degrees(ms, fs)
            d = [int(v) for v in deg.reshape(-1)]
            ind = [int(v) for v in indeg.reshape(-1)]
            profile = tuple(sorted(set(d)))
            key = str(profile)
            by_degree_profile[key] = by_degree_profile.get(key, 0) + 1
            count_pass = sum(int(v) for m in ms for v in m.reshape(-1))
            f_count = [sum(1 for v in f.reshape(-1) if int(v) != 0) for f in fs]
            h_count = [sum(1 for v in h.reshape(-1) if int(v) != 0) for h in hs]
            pass_count = [sum(int(v) for v in m.reshape(-1)) for m in ms]
            entry = {
                "p1": list(p1),
                "c": c,
                "F_per_axis": f_count,
                "twist_per_axis": h_count,
                "pass_per_axis": pass_count,
                "passing_links": count_pass,
                "degree_profile": list(profile),
                "indegree_max": max(ind),
                "indegree_profile": sorted(set(ind)),
            }
            if d and max(d) == 1 and min(d) == 1:
                perfect.append(entry)
            elif d and max(d) == 2 and min(d) == 2 and max(ind) == 1 and min(ind) == 1:
                cycles.append(entry)
            elif d and max(d) == 1 and count_pass > 0:
                partial.append(entry)
    lines.append(f"3D patterns p = p1 + c z measured: {2 * len(modes)}")
    lines.append(f"degree profiles (set of degrees over the 64 Nodes) and their counts: {json.dumps(by_degree_profile, sort_keys=True)}")
    lines.append(f"PERFECT matchings (every Node degree 1): {len(perfect)}")
    for e in perfect[:24]:
        lines.append("  " + json.dumps(e))
    lines.append(f"partial matchings (every degree at most 1, some 0): {len(partial)}")
    for e in partial[:12]:
        lines.append("  " + json.dumps(e))
    lines.append(f"CYCLE covers (every Node degree 2 and in-degree 1: one Link in, one out, the take at every Node alike): {len(cycles)}")
    for e in cycles[:16]:
        lines.append("  " + json.dumps(e))
    text = "\n".join(lines)
    print(text)
    with open(argv[1], "w", encoding="utf-8") as f:
        f.write(text + "\n")
        f.write("ALL_PERFECT " + json.dumps(perfect) + "\n")
        f.write("ALL_CYCLES " + json.dumps(cycles) + "\n")


if __name__ == "__main__":
    main(sys.argv)
