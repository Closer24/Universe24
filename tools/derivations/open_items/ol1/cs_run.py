"""cs1's runner: the engine's own Node (src untouched), the world file's lays, then a light pattern laid by this script on the plane at the gap 0 (the gap-0 plane's re and im lines), the record written as run.py writes it (the gates read it) with a diag line per interval.

The pattern (the lay by phase): at every Node a phase p(k) in Z_4, a quarter turn's multiple, p(x, y, z) = (a_x y + b_x z + c_x) mod 4 for the layer x along the axis 0 (the layered form; the helix along the diagonal is a_x = b_x = 1, c_x = x; a plane wave along x alone is a_x = b_x = 0, c_x = x); the levels z_now = A i^p, z_before = i z_now (the quarter turn per interval, the exact eigenmode of the gap-0 line where the six neighbours' phases sum to 0 at every Node): (re_now, re_before, im_now, im_before) = A (1, 0, 0, 1), A (0, -1, 1, 0), A (-1, 0, 0, -1), A (0, 1, -1, 0) at p = 0, 1, 2, 3. The amplitude A the least whose share per Node at the vacuum's weight is at or above n quanta of the light's unit. With "mirror" 1 the rotation remainders of the negated lines (re at p 1 and 2, im at p 2 and 3) are laid at the mirror wall - 1 - r of the half wall (the exact image of the lines under the plane's quarter turn; a departure from the letter's lay, named).

Usage: python cs_run.py <world.json> <out.json> <pattern.json> [back N]
pattern.json: {"a": [..4..], "b": [..4..], "c": [..4..], "quanta": n, "mirror": 0 or 1}. Integers only."""

from __future__ import annotations

import json
import sys
from typing import Any

import numpy as np

from event_universe import readings, run, seed
from event_universe.core.ports import AXES, across
from event_universe.core.rule3 import quotient
from event_universe.links import link_current, twist, wronskian
from event_universe.loader.world import load_world
from event_universe.node import Node
from event_universe.rows import CARRIER, PLANE, Line, zeros

THOUSAND = 1000
HUNDRED = 100
TURNS = 4  # the quarter turns of a whole turn
RE_SIGN = (1, 0, -1, 0)  # Re(i^p)
IM_SIGN = (0, 1, 0, -1)  # Im(i^p)


def ints(a: Any) -> list[int]:
    return [int(x) for x in np.asarray(a, dtype=object).reshape(-1)]


def phases(shape: tuple[int, ...], pattern: dict[str, Any]) -> Any:
    """The phase p(k) in Z_4 at every Node, the layered form along the axis 0."""
    a, b, c = pattern["a"], pattern["b"], pattern["c"]
    found = zeros(shape)
    for at in np.ndindex(*shape):
        x, y, z = at
        found[at] = (int(a[x % len(a)]) * y + int(b[x % len(b)]) * z + int(c[x % len(c)])) % TURNS
    return found


def levels_of(p: Any, amplitude: int) -> tuple[Any, Any, Any, Any]:
    """The four levels at the amplitude from the phases: z_now = A i^p, z_before = i z_now."""
    re_now = zeros(p.shape)
    im_now = zeros(p.shape)
    re_before = zeros(p.shape)
    im_before = zeros(p.shape)
    for at in np.ndindex(*p.shape):
        q = int(p[at])
        re_now[at] = amplitude * RE_SIGN[q]
        im_now[at] = amplitude * IM_SIGN[q]
        re_before[at] = amplitude * RE_SIGN[(q + 1) % TURNS]
        im_before[at] = amplitude * IM_SIGN[(q + 1) % TURNS]
    return re_now, re_before, im_now, im_before


def share_min(node: Node, rec: int, levels: tuple[Any, Any, Any, Any], base: tuple[Any, Any, Any, Any]) -> int:
    """The least share over the board of the gap-0 plane were the levels added to the base (the sea's lines)."""
    row = node.records()[rec]
    rule = node.rule_of(row, node.content(), node.link_factors())
    re = Line(base[0] + levels[0], base[1] + levels[1], None, node.w)
    im = Line(base[2] + levels[2], base[3] + levels[3], None, node.w)
    sh = node.share(re, rule, vacuum=True) + node.share(im, rule, vacuum=True)
    return min(ints(sh))


def fitted(node: Node, rec: int, p: Any, base: tuple[Any, Any, Any, Any], target: int) -> int:
    """The least amplitude whose least share over the board is at or above the target (a search by comparisons)."""
    high = 1
    while share_min(node, rec, levels_of(p, high), base) < target:
        high = high + high
    low = 0
    while high - low > 1:
        middle = int(quotient(low + high, 2))
        if share_min(node, rec, levels_of(p, middle), base) < target:
            low = middle
        else:
            high = middle
    return high


def lay_pattern(node: Node, pattern: dict[str, Any]) -> dict[str, Any]:
    """The pattern laid on the gap-0 plane: the amplitude fitted, the levels added by the one lay act, the remainders mirrored where asked; the lay logged."""
    gap0 = node.row(PLANE, gap=0)
    rec = node.records().index(gap0)
    re, im = gap0.lines
    base = (re.now.copy(), re.before.copy(), im.now.copy(), im.before.copy())
    p = phases(node.shape, pattern)
    n = int(pattern.get("quanta", 1))
    amplitude = fitted(node, rec, p, base, n * node.unit_gap0)
    levels = levels_of(p, amplitude)
    node.lay(rec, Ellipsis, levels)
    mirrored_count = 0
    if int(pattern.get("mirror", 0)) == 1:
        for at in np.ndindex(*node.shape):
            q = int(p[at])
            wall_at = int(np.asarray(re.wall)[at]) if np.ndim(re.wall) else int(re.wall)
            if q in (1, 2):
                re.rem[at] = wall_at - 1 - int(re.rem[at])
                mirrored_count += 1
            if q in (2, 3):
                im.rem[at] = wall_at - 1 - int(im.rem[at])
                mirrored_count += 1
    node.start_content = node.content()
    entry = {
        "event": "lay_pattern",
        "i": 0,
        "pattern": pattern,
        "line_pair": rec,
        "amplitude": amplitude,
        "share_min": share_min(node, rec, levels, base),
        "unit": node.unit_gap0,
        "mirrored_lines": mirrored_count,
        "phase_counts": [sum(1 for v in ints(p) if v == q) for q in range(TURNS)],
    }
    node.log.append(entry)
    return entry


def spread(x: Any) -> int:
    """The spread in thousandths, the largest over the Links of 1000 |X_j - X_i| div min(X_i, X_j)."""
    worst = 0
    for axis in range(AXES):
        xj = across(x, 2 * axis)
        for a, b in zip(ints(x), ints(xj), strict=True):
            d = abs(a - b) * THOUSAND
            m = min(a, b)
            if m > 0:
                worst = max(worst, d // m)
    return worst


class CsNode(Node):
    """The engine's Node with a diag line per interval (no act changed)."""

    def __init__(self, universe: dict[str, Any], world: dict[str, Any], pattern: dict[str, Any]) -> None:
        super().__init__(universe, world)
        self.lay_line = lay_pattern(self, pattern)
        self.diag: list[dict[str, Any]] = [self.read_diag()]

    def step(self) -> None:
        super().step()
        self.diag.append(self.read_diag())

    def read_diag(self) -> dict[str, Any]:
        node = self
        x = node.row(CARRIER).lines[0].now
        xs = ints(x)
        layers = [ints(x[k]) for k in range(node.cube)]
        c = node.content()
        node.start_content = c
        frozen = readings.frozen_of(node, c)
        factors = node.link_factors(None, frozen)
        pace = readings.paces_of(node, c)[1]
        gap0 = node.row(PLANE, gap=0)
        rec0 = node.records().index(gap0)
        rr = node.rule_of(gap0, c, factors)
        re, im = gap0.lines
        sh0 = ints(node.share(re, rr, pace, vacuum=True) + node.share(im, rr, pace, vacuum=True))
        u0 = node.unit_gap0
        taken = re
        f_nonzero = []
        h_nonzero = []
        both_nonzero = []
        f_max = 0
        h_max = 0
        for axis in range(AXES):
            f = ints(link_current(taken, 2 * axis))
            h = ints(twist(taken, axis))
            f_nonzero.append(sum(1 for v in f if v != 0))
            h_nonzero.append(sum(1 for v in h if v != 0))
            both_nonzero.append(sum(1 for v, hv in zip(f, h, strict=True) if v != 0 and hv != 0))
            f_max = max(f_max, max(abs(v) for v in f))
            h_max = max(h_max, max(abs(v) for v in h))
        w0 = ints(wronskian(re, im))
        w_gap = zeros(node.shape)
        for r in node.gapped:
            w_gap = w_gap + wronskian(*r.lines)
        energy = sum(a * a + b * b for a, b in zip(ints(re.now), ints(im.now), strict=True))
        return {
            "i": node.interval,
            "X_mean": sum(xs) // len(xs),
            "X_min": min(xs),
            "X_max": max(xs),
            "X_layers_mean": [sum(v) // len(v) for v in layers],
            "e_max": spread(x),
            "turned": int(node.turned.sum()),
            "frozen": int(sum(1 for v in ints(frozen) if v)),
            "births": node.counts["births"],
            "body_clicks": node.counts["body_clicks"],
            "refused_orientation": node.counts["refused_orientation"],
            "refused_twist": node.counts["refused_twist"],
            "refused_lay": node.counts["refused_lay"],
            "refused_stop": node.counts["refused_stop"],
            "refused_origin": node.counts["refused_origin"],
            "F_links_nonzero_per_axis": f_nonzero,
            "twist_links_nonzero_per_axis": h_nonzero,
            "F_and_twist_nonzero_per_axis": both_nonzero,
            "F_abs_max": f_max,
            "twist_abs_max": h_max,
            "light_W_total": sum(w0),
            "light_W_abs_max": max(abs(v) for v in w0),
            "light_energy_min_max": [
                min(a * a + b * b for a, b in zip(ints(re.now), ints(im.now), strict=True)),
                max(a * a + b * b for a, b in zip(ints(re.now), ints(im.now), strict=True)),
            ],
            "light_energy_total": energy,
            "gap_W_total": sum(ints(w_gap)),
            "light_share_min_max_hundredths": [min(sh0) * HUNDRED // u0, max(sh0) * HUNDRED // u0],
            "light_share_whole_nodes": sum(1 for v in sh0 if v >= u0),
            "bits": node.census()[1],
        }


def main(argv: list[str]) -> None:
    sys.set_int_max_str_digits(0)
    universe, world = load_world(argv[1])
    with open(argv[3], encoding="utf-8") as f:
        pattern = json.load(f)
    back = int(argv[argv.index("back") + 1]) if "back" in argv else 0
    node = CsNode(universe, world, pattern)
    intervals = int(world["intervals"])
    out = lambda line: print(line, flush=True)
    out(json.dumps({"lay": node.lay_line, "diag0": node.diag[0]}))
    rows, nodes, hashes = run.forward(node, intervals, back, out)
    kept_log = list(node.log)
    returned = run.run_back(node, hashes) if back else None
    if returned:
        out(json.dumps({"run back": returned}))
    counts = {k: str(v) for k, v in node.counts.items()}
    out(json.dumps({"counts": counts}))
    found = {
        "world": world,
        "universe": universe,
        "pattern": pattern,
        "den": node.den,
        "cube": node.cube,
        "intervals": intervals,
        "gapped": [(str(r.pair[0]), str(seed.sine_den(r.pair[0], node.den))) for r in node.gapped if r.pair],
        "planes": [str(r.pair[0]) for r in node.records() if r.pair],
        "T": node.T,
        "gamma": node.gamma,
        "G": node.G,
        "counts": counts,
        "turns": node.turns,
        "rows": rows,
        "nodes": nodes,
        "run_back": returned,
        "log": kept_log,
        "diag": node.diag,
    }
    with open(argv[2], "w", encoding="utf-8") as f:
        json.dump(found, f)


if __name__ == "__main__":
    main(sys.argv)
