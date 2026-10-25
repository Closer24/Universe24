"""ma2's runner: the engine's own Node (src untouched), the world file's lays, then the fourth form laid by this script (a sea of a plane with a gap at one sense, the pair, or the checkerboard of the senses), the record written as run.py writes it (the gates read it) with a diag line per interval: the board's X (mean, least, largest, the spread in thousandths over the Links, the even and the odd Nodes' means), the turns, the counts, the charge (the Wronskian of the planes with a gap summed over the even and the odd Nodes), the light's current and twist, the shares in hundredths of a quantum, the group's invariance (X uniform; W odd under one Link's translation), and the mergers' premises per gapped record (gate 24: both ends whole, the Wronskians opposite, the row's current, the twist, the lay's refusal at the light's standing, the stop at one end for 2 u_0 and at each end for u_0).

Usage: python ma_run.py <world.json> <out.json> [back N] [lays <lays.json>]
The lays file is a list of the fourth form: {"lay": "sea", "row": r, "quanta": n, "sense": s} with s in -1, 0 (the pair), 1; {"lay": "checker", "row": r, "quanta": n, "flip": [[x, y, z], ...]} (the sense (-1)^(x + y + z), flipped at the Nodes listed; refused on an odd cube). Integers only."""

from __future__ import annotations

import json
import sys
from typing import Any

import numpy as np

from event_universe import readings, run, seed, take
from event_universe.core.ports import AXES, across, shifted
from event_universe.core.rule3 import quotient
from event_universe.links import cross, link_current, net_current, twist, wronskian
from event_universe.loader.world import load_world
from event_universe.node import Node
from event_universe.rows import CARRIER, PLANE, zeros

THOUSAND = 1000
HUNDRED = 100


def ints(a: Any) -> list[int]:
    return [int(x) for x in np.asarray(a, dtype=object).reshape(-1)]


def parity(shape: tuple[int, ...]) -> Any:
    """The sense (-1)^(x + y + z) at every Node."""
    idx = np.indices(shape)
    s = (idx[0] + idx[1] + idx[2]) % 2
    return np.array([1 - 2 * int(v) for v in s.reshape(-1)], dtype=object).reshape(shape)


def uniform_record(node: Node, row: Any, amplitude: int, sense: int) -> tuple[Any, Any, Any, Any]:
    """One record at rest at every Node (seed.rest_record with the envelope 1 and the centre weight 1): the four levels (re_now, re_before, im_now, im_before)."""
    env = zeros(node.shape) + 1
    re, im = seed.rest_record(node, row, env, 1, amplitude, sense)
    return re.now, re.before, im.now, im.before


def levels_of(node: Node, row: Any, amplitude: int, sense: int) -> tuple[Any, Any, Any, Any]:
    """The form's levels at the amplitude: one sense (s = 1 or -1) or the pair (s = 0: both senses summed, the im line 0)."""
    if sense == 0:
        a = uniform_record(node, row, amplitude, 1)
        b = uniform_record(node, row, amplitude, -1)
        return tuple(x + y for x, y in zip(a, b, strict=True))
    return uniform_record(node, row, amplitude, sense)


def share_at_origin(node: Node, rec: int, levels: tuple[Any, Any, Any, Any]) -> int:
    """The record's share at the Node (0, 0, 0) at the vacuum's weight were the levels laid alone over the board."""
    from event_universe.rows import Line

    row = node.records()[rec]
    rule = node.rule_of(row, node.content(), node.link_factors())
    re = Line(levels[0], levels[1], None, node.w)
    im = Line(levels[2], levels[3], None, node.w)
    sh = node.share(re, rule, vacuum=True) + node.share(im, rule, vacuum=True)
    return int(sh.reshape(-1)[0])


def fitted_uniform(node: Node, rec: int, sense: int, target: int) -> int:
    """The least amplitude whose share per Node is at least the target (the child's lay_amplitude reads one quantum the same way: at or above; seed.fitted's search, its answer plus one)."""
    row = node.records()[rec]
    high = 1
    while share_at_origin(node, rec, levels_of(node, row, high, sense)) <= target:
        high = high + high
    low = 0
    while high - low > 1:
        middle = int(quotient(low + high, 2))
        if share_at_origin(node, rec, levels_of(node, row, middle, sense)) <= target:
            low = middle
        else:
            high = middle
    return low + 1


def lay_fourth(node: Node, lays: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """The fourth form laid: a sea of a plane with a gap at one sense or the pair, or the checkerboard; the lay logged with its amplitude and share."""
    logged = []
    for lay in lays:
        row = node.by_index[int(lay["row"])]
        if row.shape != PLANE or not row.gap:
            raise ValueError("the fourth form lays a plane with a gap")
        rec = node.records().index(row)
        n = int(lay["quanta"])
        form = lay["lay"]
        if form == "sea":
            sense = int(lay["sense"])
            amplitude = fitted_uniform(node, rec, sense, n * node.units[rec])
            levels = levels_of(node, row, amplitude, sense)
            node.lay(rec, Ellipsis, levels)
            senses = zeros(node.shape) + sense
        elif form == "checker":
            if node.cube % 2:
                raise ValueError("the checkerboard of the senses is refused on an odd cube: the wrap breaks the parity")
            amplitude = fitted_uniform(node, rec, 1, n * node.units[rec])
            re_now, re_before, im_now, im_before = levels_of(node, row, amplitude, 1)
            senses = parity(node.shape)
            for xyz in lay.get("flip", []):
                at = node.node_of(xyz)
                senses[at] = -senses[at]
            node.lay(rec, Ellipsis, (re_now, re_before, im_now * senses, im_before * senses))
        else:
            raise ValueError(f"no such fourth form: {form!r}")
        node.start_content = node.content()
        sh = share_at_origin(node, rec, levels_of(node, row, amplitude, 1 if form == "checker" else int(lay["sense"])))
        entry = {
            "event": "lay_fourth",
            "i": 0,
            "form": form,
            "line_pair": rec,
            "row_index": int(lay["row"]),
            "quanta": n,
            "amplitude": amplitude,
            "share": sh,
            "unit": node.units[rec],
            "senses_sum": sum(ints(senses)),
            "nodes": int(np.prod(node.shape)),
        }
        node.log.append(entry)
        logged.append(entry)
    return logged


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


def row_twist(lines: list[Any], axis: int) -> Any:
    """The twist of a row's summed transverse currents (SL's row_twist)."""
    a, b, c = axis, (axis + 1) % AXES, (axis + 2) % AXES
    ub = sum(net_current(line, b) for line in lines)
    uc = sum(net_current(line, c) for line in lines)
    return cross(ub, uc, across(ub, 2 * a), across(uc, 2 * a))


class MaNode(Node):
    """The engine's Node with a diag line per interval (no act changed)."""

    def __init__(self, universe: dict[str, Any], world: dict[str, Any], lays: list[dict[str, Any]]) -> None:
        super().__init__(universe, world)
        self.par = parity(self.shape)
        self.lay_lines = lay_fourth(self, lays)
        self.laid_recs = sorted({int(e["line_pair"]) for e in self.lay_lines})
        self.diag: list[dict[str, Any]] = []
        self.hashes: list[str] = []

    def step(self) -> None:
        super().step()
        self.diag.append(self.read_diag())

    def read_diag(self) -> dict[str, Any]:
        node = self
        x = node.row(CARRIER).lines[0].now
        xs = ints(x)
        par = ints(self.par)
        even = [v for v, p in zip(xs, par, strict=True) if p == 1]
        odd = [v for v, p in zip(xs, par, strict=True) if p == -1]
        c = node.content()
        node.start_content = c
        frozen = readings.frozen_of(node, c)
        factors = node.link_factors(None, frozen)
        pace = readings.paces_of(node, c)[1]
        gap0 = node.row(PLANE, gap=0)
        rec0 = node.records().index(gap0)
        owns = []
        for rec, r in enumerate(node.records()):
            rr = node.rule_of(r, c, factors)
            re, im = r.lines
            owns.append(node.share(re, rr, pace, vacuum=True) + node.share(im, rr, pace, vacuum=True))
        sh0 = ints(owns[rec0])
        u0 = node.unit_gap0
        w_gap = zeros(node.shape)
        for r in node.gapped:
            w_gap = w_gap + wronskian(*r.lines)
        wg = ints(w_gap)
        w_even = sum(v for v, p in zip(wg, par, strict=True) if p == 1)
        w_odd = sum(v for v, p in zip(wg, par, strict=True) if p == -1)
        # the group: W odd under one Link's translation on every axis
        w_odd_fail = 0
        for axis in range(AXES):
            w_odd_fail += sum(1 for v in ints(w_gap + shifted(w_gap, axis, 1)) if v != 0)
        # the light's current and twist
        taken = gap0.lines[0]
        f_abs_max = 0
        f_from_even = 0
        f_from_odd = 0
        f_zero = 0
        h_nonzero = 0
        for axis in range(AXES):
            f = ints(link_current(taken, 2 * axis))
            h = ints(twist(taken, axis))
            for v, p, hv in zip(f, par, h, strict=True):
                f_abs_max = max(f_abs_max, abs(v))
                if v == 0:
                    f_zero += 1
                elif (v > 0) == (p == 1):
                    f_from_even += 1  # positive flow is from the Node toward +a: the + end is the odd Node
                else:
                    f_from_odd += 1
                if hv != 0:
                    h_nonzero += 1
        # the mergers' premises per laid record
        mergers = {}
        for rec in self.laid_recs:
            r = node.records()[rec]
            re, im = r.lines
            unit = node.units[rec]
            own = owns[rec]
            w_rec = wronskian(re, im)
            rule = node.rule_of(r, c, factors)
            met = opposite = orient0 = twist0 = lay_former = lay_s3 = stop_one = stop_each_ends = 0
            checked_stop = 0
            for axis in range(AXES):
                f_row = link_current(re, 2 * axis) + link_current(im, 2 * axis)
                h_row = row_twist([re, im], axis)
                own_j = across(own, 2 * axis)
                w_j = across(w_rec, 2 * axis)
                sh0_j = across(owns[rec0], 2 * axis)
                for at in np.ndindex(*node.shape):
                    if int(own[at]) < unit or int(own_j[at]) < unit:
                        continue
                    met += 1
                    if int(w_rec[at]) * int(w_j[at]) >= 0:
                        continue
                    opposite += 1
                    flow = int(f_row[at])
                    if flow == 0:
                        orient0 += 1
                    if int(h_row[at]) == 0:
                        twist0 += 1
                    j = take.neighbour(node, at, 2 * axis)
                    if int(owns[rec0][at]) > 0 or int(sh0_j[at]) > 0:
                        lay_former += 1
                    if int(owns[rec0][at]) >= u0 or int(sh0_j[at]) >= u0:
                        lay_s3 += 1
                    if checked_stop < 64:
                        checked_stop += 1
                        into = j if flow > 0 else at
                        if take.fall_of(node, into, 2 * u0, rule, re)[0] is None:
                            stop_one += 1
                        for end in (at, j):
                            if take.fall_of(node, end, u0, rule, re)[0] is None:
                                stop_each_ends += 1
            mergers[str(rec)] = {
                "met": met,
                "opposite": opposite,
                "orientation_0": orient0,
                "twist_0": twist0,
                "lay_former": lay_former,
                "lay_s3": lay_s3,
                "stop_checked": checked_stop,
                "stop_one_2u0": stop_one,
                "stop_each_u0_ends": stop_each_ends,
                "share_min_max_hundredths": [min(ints(own)) * HUNDRED // unit, max(ints(own)) * HUNDRED // unit],
                "W_abs_min_max": [min(abs(v) for v in ints(w_rec)), max(abs(v) for v in ints(w_rec))],
            }
        w_per_rec = {str(rec): sum(ints(wronskian(*r.lines))) for rec, r in enumerate(node.records())}
        return {
            "i": node.interval,
            "W_per_rec": w_per_rec,
            "X_mean": sum(xs) // len(xs),
            "X_min": min(xs),
            "X_max": max(xs),
            "X_even_mean": sum(even) // len(even) if even else 0,
            "X_odd_mean": sum(odd) // len(odd) if odd else 0,
            "e_max": spread(x),
            "turned": int(node.turned.sum()),
            "births": node.counts["births"],
            "body_clicks": node.counts["body_clicks"],
            "refused_orientation": node.counts["refused_orientation"],
            "refused_twist": node.counts["refused_twist"],
            "refused_lay": node.counts["refused_lay"],
            "refused_stop": node.counts["refused_stop"],
            "refused_origin": node.counts["refused_origin"],
            "W_even": w_even,
            "W_odd": w_odd,
            "W_total": w_even + w_odd,
            "W_odd_under_translation_fail": w_odd_fail,
            "F_abs_max": f_abs_max,
            "F_links_zero": f_zero,
            "F_links_from_even": f_from_even,
            "F_links_from_odd": f_from_odd,
            "twist_links_nonzero": h_nonzero,
            "light_share_min_max_hundredths": [min(sh0) * HUNDRED // u0, max(sh0) * HUNDRED // u0],
            "mergers": mergers,
            "bits": node.census()[1],
        }


def main(argv: list[str]) -> None:
    sys.set_int_max_str_digits(0)
    universe, world = load_world(argv[1])
    back = int(argv[argv.index("back") + 1]) if "back" in argv else 0
    lays = []
    if "lays" in argv:
        with open(argv[argv.index("lays") + 1], encoding="utf-8") as f:
            lays = json.load(f)
    node = MaNode(universe, world, lays)
    intervals = int(world["intervals"])
    out = lambda line: print(line, flush=True)
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
        "lays_fourth": lays,
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
