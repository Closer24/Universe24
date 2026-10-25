"""cs5's runner (cs4's cs4_run.py rebuilt word for word from cs4's text: cs3's runner with the landing census widened by the draws per phase class of the into-Node; the share calls at this head's signature; the engine's own Node, src untouched): the world file's lays, then a light pattern laid by this script on the plane at the gap 0, the record written as run.py writes it with a diag line per interval, a landing census at every close that reaches the lay (the draws per Node and per phase class, the children per Node and per plane, the crowd), and the gap-0 plane's four levels dumped at named intervals.

The pattern file (integers only), one of the forms of the phase p(k) in Z_4 at every Node:
  {"a": [..], "b": [..], "c": [..]}             cs1's layered form
  {"cell": [8 digits], "eta": [3 digits]}        cs2's cell form
  {"p1": [16 digits], "cz": c}                   cs3's cycle form, p(x, y, z) = (p1[4 x + y] + c z) mod 4
  {"phases": [64 digits]}                        explicit, the Nodes in np.ndindex order
  {"levels": "<dump.json>", "at": i}             explicit four levels per Node read from a dump
with the keys: "sense" 1 or -1, default 1; "A" the amplitude, or "quanta" n (the least A whose least share over the board is at or above n units of the light); "mirror" 1 or 0; "dump_at": [i, ...].

Usage: python cs5_run.py <world.json> <out.json> <pattern.json> [back N]"""

from __future__ import annotations

import json
import sys
from typing import Any

import numpy as np

from event_universe import close, readings, run, seed
from event_universe.core.ports import AXES, across
from event_universe.core.rule3 import quotient
from event_universe.links import link_current, twist, wronskian
from event_universe.loader.world import load_world
from event_universe.node import Node
from event_universe.rows import CARRIER, PLANE, Line, zeros

THOUSAND = 1000
HUNDRED = 100
TURNS = 4
RE_SIGN = (1, 0, -1, 0)
IM_SIGN = (0, 1, 0, -1)


def ints(a: Any) -> list[int]:
    return [int(x) for x in np.asarray(a, dtype=object).reshape(-1)]


def phases(shape: tuple[int, ...], pattern: dict[str, Any]) -> Any:
    """The phase p(k) in Z_4 at every Node by the pattern's form."""
    found = zeros(shape)
    if "phases" in pattern:
        flat = [int(v) for v in pattern["phases"]]
        for n, at in enumerate(np.ndindex(*shape)):
            found[at] = flat[n] % TURNS
        return found
    if "cell" in pattern:
        cell, eta = [int(v) for v in pattern["cell"]], [int(v) for v in pattern["eta"]]
        for at in np.ndindex(*shape):
            x, y, z = at
            base = cell[((x % 2) * 2 + (y % 2)) * 2 + (z % 2)]
            found[at] = (base + 2 * (eta[0] * (x // 2) + eta[1] * (y // 2) + eta[2] * (z // 2))) % TURNS
        return found
    if "p1" in pattern:
        p1, cz = [int(v) for v in pattern["p1"]], int(pattern.get("cz", 1))
        side = shape[0]
        for at in np.ndindex(*shape):
            x, y, z = at
            found[at] = (p1[(x % side) * side + (y % side)] + cz * z) % TURNS
        return found
    a, b, c = pattern["a"], pattern["b"], pattern["c"]
    for at in np.ndindex(*shape):
        x, y, z = at
        found[at] = (int(a[x % len(a)]) * y + int(b[x % len(b)]) * z + int(c[x % len(c)])) % TURNS
    return found


def levels_of(p: Any, amplitude: int, sense: int) -> tuple[Any, Any, Any, Any]:
    """The four levels at the amplitude from the phases: z_now = A i^p, z_before = i^sense z_now."""
    re_now, im_now, re_before, im_before = zeros(p.shape), zeros(p.shape), zeros(p.shape), zeros(p.shape)
    for at in np.ndindex(*p.shape):
        q = int(p[at])
        re_now[at] = amplitude * RE_SIGN[q]
        im_now[at] = amplitude * IM_SIGN[q]
        re_before[at] = amplitude * RE_SIGN[(q + sense) % TURNS]
        im_before[at] = amplitude * IM_SIGN[(q + sense) % TURNS]
    return re_now, re_before, im_now, im_before


def share_min(node: Node, rec: int, levels: tuple[Any, Any, Any, Any], base: tuple[Any, Any, Any, Any]) -> int:
    row = node.records()[rec]
    rule = node.rule_of(row, node.content(), node.link_factors())
    re = Line(base[0] + levels[0], base[1] + levels[1], None, node.w)
    im = Line(base[2] + levels[2], base[3] + levels[3], None, node.w)
    sh = node.share([re, im], rule)
    return min(ints(sh))


def fitted(node: Node, rec: int, p: Any, sense: int, base: tuple[Any, Any, Any, Any], target: int) -> int:
    """The least amplitude whose least share over the board is at or above the target (a search by comparisons)."""
    high = 1
    while share_min(node, rec, levels_of(p, high, sense), base) < target:
        high = high + high
    low = 0
    while high - low > 1:
        middle = int(quotient(low + high, 2))
        if share_min(node, rec, levels_of(p, middle, sense), base) < target:
            low = middle
        else:
            high = middle
    return high


def lay_pattern(node: Node, pattern: dict[str, Any]) -> dict[str, Any]:
    """The pattern laid on the gap-0 plane by the one lay act; the remainders mirrored where asked; the lay logged."""
    gap0 = node.row(PLANE, gap=0)
    rec = node.records().index(gap0)
    re, im = gap0.lines
    base = (re.now.copy(), re.before.copy(), im.now.copy(), im.before.copy())
    entry: dict[str, Any] = {"event": "lay_pattern", "i": 0, "pattern": {k: v for k, v in pattern.items() if k != "phases"}, "line_pair": rec, "unit": node.unit_gap0}
    if "levels" in pattern:
        with open(pattern["levels"], encoding="utf-8") as f:
            dumps = json.load(f)
        d = next(x for x in dumps if int(x["i"]) == int(pattern["at"]))
        levels = tuple(np.array([int(v) for v in d["gap0"][k]], dtype=object).reshape(node.shape) for k in range(4))
        node.lay(rec, Ellipsis, levels)
        entry["levels_from"] = [pattern["levels"], int(pattern["at"])]
        entry["share_min"] = share_min(node, rec, levels, base)
        node.start_content = node.content()
        node.log.append(entry)
        return entry
    sense = int(pattern.get("sense", 1))
    p = phases(node.shape, pattern)
    if "A" in pattern:
        amplitude = int(pattern["A"])
    else:
        amplitude = fitted(node, rec, p, sense, base, int(pattern.get("quanta", 1)) * node.unit_gap0)
    levels = levels_of(p, amplitude, sense)
    node.lay(rec, Ellipsis, levels)
    mirrored_count = 0
    if int(pattern.get("mirror", 0)) == 1:
        for at in np.ndindex(*node.shape):
            q = int(p[at])
            wall_at = int(np.asarray(re.wall)[at]) if np.ndim(re.wall) else int(re.wall)
            if RE_SIGN[q] < 0 or RE_SIGN[(q + sense) % TURNS] < 0:
                re.rem[at] = wall_at - 1 - int(re.rem[at])
                mirrored_count += 1
            if IM_SIGN[q] < 0 or IM_SIGN[(q + sense) % TURNS] < 0:
                im.rem[at] = wall_at - 1 - int(im.rem[at])
                mirrored_count += 1
    node.start_content = node.content()
    entry.update(
        {
            "amplitude": amplitude,
            "sense": sense,
            "share_min": share_min(node, rec, levels, base),
            "mirrored_lines": mirrored_count,
            "phase_counts": [sum(1 for v in ints(p) if v == q) for q in range(TURNS)],
            "phases": ints(p),
        }
    )
    node.log.append(entry)
    PHASES[:] = ints(p)
    return entry


def spread(x: Any) -> int:
    worst = 0
    for axis in range(AXES):
        xj = across(x, 2 * axis)
        for a, b in zip(ints(x), ints(xj), strict=True):
            d = abs(a - b) * THOUSAND
            m = min(a, b)
            if m > 0:
                worst = max(worst, d // m)
    return worst


ORIGINAL_REFUSE = close.refuse
PHASES: list[int] = []


def refuse_with_census(node: Node, born: list[Any], owns: list[Any]) -> list[Any]:
    """The landing census logged before the letter's refusals (a reader hooked on the act; the act's answer untouched)."""
    if born:
        landing: dict[tuple[int, ...], dict[int, int]] = {}
        indeg: dict[tuple[int, ...], int] = {}
        draws: dict[tuple[int, ...], set[int]] = {}
        for at, s, minus, plus, _room, _rec in born:
            indeg[at] = indeg.get(at, 0) + 1
            draws.setdefault(at, set()).add(s)
            for end in (minus, plus):
                landing.setdefault(end, {})
                landing[end][s] = landing[end].get(s, 0) + 1
        per_node = [sum(v.values()) for v in landing.values()]
        crowded = sum(1 for v in landing.values() if max(v.values()) > 1)
        light = node.records().index(node.row(PLANE, gap=0))
        standing = sum(1 for v in landing.values() if light in v)
        planes: dict[int, int] = {}
        for _at, s, _m, _p, _r, _rec in born:
            planes[s] = planes.get(s, 0) + 1
        by_class: dict[str, dict[str, int]] = {}
        if PHASES:
            for at, s, _m, _p, _r, _rec in born:
                c = str(PHASES[(at[0] * node.cube + at[1]) * node.cube + at[2]])
                by_class.setdefault(c, {})
                by_class[c][str(s)] = by_class[c].get(str(s), 0) + 1
        node.log.append(
            {
                "event": "landing",
                "i": node.interval,
                "node": [0, 0, 0],
                "draws_per_class": by_class,
                "links": len(born),
                "draws_per_plane": {str(k): v for k, v in sorted(planes.items())},
                "distinct_draws": len({s for _a, s, _m, _p, _r, _rec in born}),
                "taken_rows": {str(k): sum(1 for b in born if b[5] == k) for k in sorted({b[5] for b in born})},
                "into_nodes": len(indeg),
                "indegree_hist": {str(k): v for k, v in sorted({k: list(indeg.values()).count(k) for k in set(indeg.values())}.items())},
                "nodes_with_children": len(landing),
                "children_per_node_hist": {str(k): per_node.count(k) for k in sorted(set(per_node))},
                "nodes_crowded": crowded,
                "nodes_with_light_child": standing,
                "nodes_one_child_one_plane": sum(1 for v in landing.values() if sum(v.values()) == 1 and light not in v),
                "nodes_clean": sum(1 for v in landing.values() if max(v.values()) == 1 and light not in v),
            }
        )
    return ORIGINAL_REFUSE(node, born, owns)


close.refuse = refuse_with_census


class CsNode(Node):
    """The engine's Node with a diag line per interval and the dumps (no act changed)."""

    def __init__(self, universe: dict[str, Any], world: dict[str, Any], pattern: dict[str, Any]) -> None:
        super().__init__(universe, world)
        self.lay_line = lay_pattern(self, pattern)
        self.dump_at = {int(v) for v in pattern.get("dump_at", [])}
        self.dumps: list[dict[str, Any]] = []
        self.diag: list[dict[str, Any]] = [self.read_diag()]

    def step(self) -> None:
        super().step()
        self.diag.append(self.read_diag())
        if self.interval in self.dump_at:
            gap0 = self.row(PLANE, gap=0)
            re, im = gap0.lines
            self.dumps.append(
                {
                    "i": self.interval,
                    "gap0": [ints(re.now), ints(re.before), ints(im.now), ints(im.before)],
                    "gap0_rem": [ints(re.rem), ints(im.rem)],
                    "X": ints(self.row(CARRIER).lines[0].now),
                    "records_now": [[ints(l.now) for l in r.lines] for r in self.records()],
                }
            )

    def read_diag(self) -> dict[str, Any]:
        node = self
        x = node.row(CARRIER).lines[0].now
        xs = ints(x)
        c = node.content()
        node.start_content = c
        frozen = readings.frozen_of(node, c)
        factors = node.link_factors(None, frozen)
        gap0 = node.row(PLANE, gap=0)
        rr = node.rule_of(gap0, c, factors)
        re, im = gap0.lines
        sh0 = ints(node.share([re, im], rr))
        u0 = node.unit_gap0
        f_nonzero, h_nonzero, both_nonzero = [], [], []
        deg = zeros(node.shape)
        indeg = zeros(node.shape)
        for axis in range(AXES):
            f = link_current(re, 2 * axis)
            h = twist(re, axis)
            m = np.vectorize(lambda a, b: 1 if (int(a) != 0 and int(b) != 0) else 0, otypes=[object])(f, h)
            f_nonzero.append(sum(1 for v in ints(f) if v != 0))
            h_nonzero.append(sum(1 for v in ints(h) if v != 0))
            both_nonzero.append(sum(ints(m)))
            deg = deg + m + across(m, 2 * axis + 1)
            into_plus = np.vectorize(lambda a, b: 1 if (int(a) == 1 and int(b) > 0) else 0, otypes=[object])(m, f)
            into_self = np.vectorize(lambda a, b: 1 if (int(a) == 1 and int(b) < 0) else 0, otypes=[object])(m, f)
            indeg = indeg + into_self + across(into_plus, 2 * axis + 1)
        d = ints(deg)
        ind = ints(indeg)
        w0 = ints(wronskian(re, im))
        owns_whole = []
        for k, r in enumerate(node.records()):
            if r is gap0:
                continue
            rk = node.rule_of(r, c, factors)
            shk = ints(node.share(r.lines, rk))
            owns_whole.append(sum(1 for v in shk if v >= node.units[k]))
        return {
            "i": node.interval,
            "X_mean": sum(xs) // len(xs),
            "X_min": min(xs),
            "X_max": max(xs),
            "X_distinct": len(set(xs)),
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
            "pass_degree_hist": {str(k): d.count(k) for k in sorted(set(d))},
            "pass_indegree_hist": {str(k): ind.count(k) for k in sorted(set(ind))},
            "light_W_total": sum(w0),
            "light_energy_min_max": [
                min(a * a + b * b for a, b in zip(ints(re.now), ints(im.now), strict=True)),
                max(a * a + b * b for a, b in zip(ints(re.now), ints(im.now), strict=True)),
            ],
            "light_share_min_max_hundredths": [min(sh0) * HUNDRED // u0, max(sh0) * HUNDRED // u0],
            "light_share_whole_nodes": sum(1 for v in sh0 if v >= u0),
            "gapped_whole_nodes": owns_whole,
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
    out(json.dumps({"lay": {k: v for k, v in node.lay_line.items() if k != "phases"}, "diag0": node.diag[0]}))
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
        "integers": node.census()[0],
    }
    with open(argv[2], "w", encoding="utf-8") as f:
        json.dump(found, f)
    if node.dumps:
        with open(argv[2].replace(".json", "_dump.json"), "w", encoding="utf-8") as f:
            json.dump(node.dumps, f)


if __name__ == "__main__":
    main(sys.argv)
