"""ck1's runner (ma2's ma_run.py extended; src untouched, the engine from PYTHONPATH, flagged or not): the world file's lays, then the fourth form laid by the script, the record as run.py writes it (python -m event_universe.gates reads it) with a diag line per interval.
The fourth forms (a lays file, a list): {"lay": "sea", "row": r, "quanta": n, "sense": s} (ma2's: one record at rest at every Node, s in -1, 0, 1); {"lay": "checker", "row": r, "quanta": n, "flip": [...]} (ma2's: the sense (-1)^(x+y+z), refused on an odd cube); {"lay": "parity_sea", "mode": "drift" | "standing", "amplitude": A} the gap-0 re line laid with the parity: "drift" lays (s v, 0) as now, before (the staggered drift, v the sea's drift when A is absent), "standing" lays (-s A, s A) (the period-2 alternation, exact at the vacuum paces).
The diag per interval: X (mean, least, largest, the even and the odd colours' means, the spread in thousandths), the turns, the counts, the colour exchange C' (the translation by one Link composed with the sign per line: the planes' im lines, the shape-4 row's lines and, where the flag "light_odd" is set in the lays file's first entry, the gap-0 re line are odd; every other line even) read on every line: the levels held per line and the remainders' offsets (the two's complement test r_o = (W - r_e) mod W for an odd line, r_o = r_e for an even one; the set of offsets over the board), the light's current and twist, the shares, the credits and refusals per colour and per line this interval, the mergers' premises (met, opposite, orientation 0, twist 0), the Wronskian per record and per colour.
Usage: python ck1_run.py <world.json> <out.json> [back N] [lays <lays.json>]. Integers only."""

from __future__ import annotations

import json
import sys
from typing import Any

import numpy as np

from event_universe import readings, run, seed
from event_universe.core.ports import AXES, across, shifted
from event_universe.core.rule3 import quotient
from event_universe.links import cross, link_current, net_current, twist, wronskian
from event_universe.loader.world import load_world
from event_universe.node import Node
from event_universe.rows import CARRIER, zeros
from event_universe.rows import PLANE
from event_universe.rows import POTENTIAL

THOUSAND = 1000
HUNDRED = 100


def ints(a: Any) -> list[int]:
    return [int(x) for x in np.asarray(a, dtype=object).reshape(-1)]


def parity(shape: tuple[int, ...]) -> Any:
    idx = np.indices(shape)
    s = (idx[0] + idx[1] + idx[2]) % 2
    return np.array([1 - 2 * int(v) for v in s.reshape(-1)], dtype=object).reshape(shape)


def uniform_record(node: Node, row: Any, amplitude: int, sense: int) -> tuple[Any, Any, Any, Any]:
    env = zeros(node.shape) + 1
    re, im = seed.rest_record(node, row, env, 1, amplitude, sense)
    return re.now, re.before, im.now, im.before


def levels_of(node: Node, row: Any, amplitude: int, sense: int) -> tuple[Any, Any, Any, Any]:
    if sense == 0:
        a = uniform_record(node, row, amplitude, 1)
        b = uniform_record(node, row, amplitude, -1)
        return tuple(x + y for x, y in zip(a, b, strict=True))
    return uniform_record(node, row, amplitude, sense)


def share_at_origin(node: Node, rec: int, levels: tuple[Any, Any, Any, Any]) -> int:
    from event_universe.rows import Line

    row = node.records()[rec]
    rule = node.rule_of(row, node.content(), node.link_factors())
    re = Line(levels[0], levels[1], None, node.w)
    im = Line(levels[2], levels[3], None, node.w)
    sh = node.share(re, rule, vacuum=True) + node.share(im, rule, vacuum=True)
    return int(sh.reshape(-1)[0])


def fitted_uniform(node: Node, rec: int, sense: int, target: int) -> int:
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
    logged = []
    par = parity(node.shape)
    for lay in lays:
        form = lay["lay"]
        if form == "parity_sea":
            if node.cube % 2:
                raise ValueError("the parity sea is refused on an odd cube: the wrap breaks the parity")
            gap0 = node.row(PLANE, gap=0)
            rec = node.records().index(gap0)
            a = int(lay.get("amplitude", node.drift))
            mode = lay.get("mode", "drift")
            if mode == "drift":
                node.lay(rec, Ellipsis, (par * a, zeros(node.shape), zeros(node.shape), zeros(node.shape)))
            elif mode == "standing":
                node.lay(rec, Ellipsis, (-par * a, par * a, zeros(node.shape), zeros(node.shape)))
            else:
                raise ValueError(f"no such parity sea mode: {mode!r}")
            node.start_content = node.content()
            entry = {"event": "lay_fourth", "i": 0, "form": form, "mode": mode, "amplitude": a, "line_pair": rec, "nodes": int(np.prod(node.shape))}
            node.log.append(entry)
            logged.append(entry)
            continue
        row = node.by_index[int(lay["row"])]
        if row.shape != PLANE or not row.gap:
            raise ValueError("the fourth form lays a plane with a gap")
        rec = node.records().index(row)
        n = int(lay["quanta"])
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
            senses = par.copy()
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
    a, b, c = axis, (axis + 1) % AXES, (axis + 2) % AXES
    ub = sum(net_current(line, b) for line in lines)
    uc = sum(net_current(line, c) for line in lines)
    return cross(ub, uc, across(ub, 2 * a), across(uc, 2 * a))


class CkNode(Node):
    """The engine's Node with a diag line per interval (no act changed)."""

    def __init__(self, universe: dict[str, Any], world: dict[str, Any], lays: list[dict[str, Any]]) -> None:
        super().__init__(universe, world)
        self.par = parity(self.shape)
        self.light_odd = bool(lays and lays[0].get("light_odd", 0))
        self.lay_lines = lay_fourth(self, lays)
        self.laid_recs = sorted({int(e["line_pair"]) for e in self.lay_lines})
        self.diag: list[dict[str, Any]] = []
        self.log_seen = len(self.log)
        self.line_names = self.names()
        self.first_parting: dict[str, Any] | None = None

    def names(self) -> list[tuple[str, int]]:
        """Every line's name and its sign under the colour exchange (+1 even, -1 odd)."""
        found = []
        gap0 = self.row(PLANE, gap=0)
        for r in self.rows_:
            for k in range(len(r.lines)):
                if r.wall is not None:
                    found.append(("walled", -1 if self.light_odd else 1))  # the phase row is the sign level: odd on a checkerboard
                elif r.shape == PLANE:
                    if r is gap0:
                        found.append((f"light_{'re' if k == 0 else 'im'}", (-1 if self.light_odd else 1) if k == 0 else -1))
                    else:
                        found.append((f"plane{self.by_index.index(r)}_{'re' if k == 0 else 'im'}", 1 if k == 0 else -1))
                elif r.shape == POTENTIAL:
                    found.append((f"potential_{k}", -1))
                elif r.shape == CARRIER:
                    found.append((f"carrier_{k}", 1))
                else:
                    found.append((f"row{r.shape}_{k}", 1))
        return found

    def step(self) -> None:
        super().step()
        self.diag.append(self.read_diag())

    def colour_check(self) -> dict[str, Any]:
        """The colour exchange on every line: the levels held (now and before equal to sgn times the one-Link translate on every axis), the remainders' offsets (the translate less the mirror: 0 held)."""
        levels_held = []
        levels_failed = []
        rem_offsets = {}
        wr_offsets = {}
        for (name, sgn), line in zip(self.line_names, self.all_lines(), strict=True):
            ok = True
            for a in (line.now, line.before):
                for axis in range(AXES):
                    if not bool(np.all(shifted(a, axis, 1) == sgn * a)):
                        ok = False
            (levels_held if ok else levels_failed).append(name)
            for which, rem, wall in (("rem", line.rem, line.wall), ("wr", line.wr, line.wwall)):
                if rem is None:
                    continue
                wl = np.asarray(wall, dtype=object) if np.ndim(wall) else wall
                mirror = rem if sgn == 1 else (wl - rem) % wl
                offs = set()
                for axis in range(AXES):
                    offs |= set(ints(shifted(rem, axis, 1) - mirror))
                offs = sorted(offs)
                if len(offs) > 6:
                    offs = offs[:3] + ["..."] + offs[-3:]
                (rem_offsets if which == "rem" else wr_offsets)[name] = offs
        return {"levels_held": len(levels_held), "levels_of": len(self.line_names), "levels_failed": levels_failed, "rem_offsets": {k: v for k, v in rem_offsets.items() if v != [0]}, "wr_offsets": {k: v for k, v in wr_offsets.items() if v != [0]}}

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
        taken = gap0.lines[0]
        f_abs_max = 0
        f_zero = 0
        h_nonzero = 0
        h_abs_max = 0
        u_abs_max = 0
        for axis in range(AXES):
            f = ints(link_current(taken, 2 * axis))
            h = ints(twist(taken, axis))
            u = ints(net_current(taken, axis))
            for v, hv, uv in zip(f, h, u, strict=True):
                f_abs_max = max(f_abs_max, abs(v))
                if v == 0:
                    f_zero += 1
                if hv != 0:
                    h_nonzero += 1
                h_abs_max = max(h_abs_max, abs(hv))
                u_abs_max = max(u_abs_max, abs(uv))
        # the light's even and odd parts under the one-Link translate
        lt = ints(taken.now)
        lt_x = ints(shifted(taken.now, 0, 1))
        light_even = max(abs(a + b) for a, b in zip(lt, lt_x, strict=True))
        light_odd = max(abs(a - b) for a, b in zip(lt, lt_x, strict=True))
        # the mergers' premises per laid gapped record (met, opposite, orientation 0, twist 0)
        mergers = {}
        for rec in self.laid_recs:
            r = node.records()[rec]
            if not r.gap:
                continue
            re, im = r.lines
            unit = node.units[rec]
            own = owns[rec]
            w_rec = wronskian(re, im)
            met = opposite = orient0 = twist0 = 0
            for axis in range(AXES):
                f_row = link_current(re, 2 * axis) + link_current(im, 2 * axis)
                h_row = row_twist([re, im], axis)
                own_j = across(own, 2 * axis)
                w_j = across(w_rec, 2 * axis)
                for at in np.ndindex(*node.shape):
                    if int(own[at]) < unit or int(own_j[at]) < unit:
                        continue
                    met += 1
                    if int(w_rec[at]) * int(w_j[at]) >= 0:
                        continue
                    opposite += 1
                    if int(f_row[at]) == 0:
                        orient0 += 1
                    if int(h_row[at]) == 0:
                        twist0 += 1
            mergers[str(rec)] = {"met": met, "opposite": opposite, "orientation_0": orient0, "twist_0": twist0, "share_min_max_hundredths": [min(ints(own)) * HUNDRED // unit, max(ints(own)) * HUNDRED // unit]}
        # the clicks of this interval per colour and per line
        clicks: dict[str, int] = {}
        for e in node.log[self.log_seen:]:
            if e["event"] in ("credit", "refused", "birth"):
                col = "even" if sum(e["node"]) % 2 == 0 else "odd"
                tag = e.get("line", e.get("line_pair", e.get("cause")))
                key = f"{e['event']}_{tag}_{col}"
                clicks[key] = clicks.get(key, 0) + 1
                if e["event"] == "credit":
                    lk = f"levels_{tag}_{col}"
                    clicks[lk] = clicks.get(lk, 0) + int(e["levels"])
        self.log_seen = len(node.log)
        check = self.colour_check()
        if self.first_parting is None and check["levels_failed"]:
            self.first_parting = {"i": node.interval, "lines": check["levels_failed"]}
        w_per_rec = {str(rec): sum(ints(wronskian(*r.lines))) for rec, r in enumerate(node.records())}
        return {
            "i": node.interval,
            "X_mean": sum(xs) // len(xs),
            "X_min": min(xs),
            "X_max": max(xs),
            "X_even_mean": sum(even) // len(even) if even else 0,
            "X_odd_mean": sum(odd) // len(odd) if odd else 0,
            "e_max": spread(x),
            "turned": int(node.turned.sum()),
            "turned_even": int(sum(1 for t, p in zip(node.turned.reshape(-1).tolist(), par, strict=True) if t and p == 1)),
            "counts": {k: v for k, v in node.counts.items()},
            "W_per_rec": w_per_rec,
            "W_even": w_even,
            "W_odd": w_odd,
            "F_abs_max": f_abs_max,
            "F_links_zero": f_zero,
            "u_abs_max": u_abs_max,
            "twist_links_nonzero": h_nonzero,
            "twist_abs_max": h_abs_max,
            "light_even_part_max": light_even,
            "light_odd_part_max": light_odd,
            "light_level_min_max": [min(lt), max(lt)],
            "light_share_min_max_hundredths": [min(sh0) * HUNDRED // u0, max(sh0) * HUNDRED // u0],
            "light_nodes_whole": sum(1 for v in sh0 if v >= u0),
            "mergers": mergers,
            "clicks": clicks,
            "colour": check,
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
    node = CkNode(universe, world, lays)
    intervals = int(world["intervals"])
    out = lambda line: print(line, flush=True)
    rows, nodes, hashes = run.forward(node, intervals, back, out)
    kept_log = list(node.log)
    returned = run.run_back(node, hashes) if back else None
    if returned:
        out(json.dumps({"run back": returned}))
    counts = {k: str(v) for k, v in node.counts.items()}
    out(json.dumps({"counts": counts}))
    out(json.dumps({"first_parting": node.first_parting, "max_transient_bits": node.max_transient, "integers": node.census()[0]}))
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
        "first_parting": node.first_parting,
        "line_names": node.line_names,
    }
    with open(argv[2], "w", encoding="utf-8") as f:
        json.dump(found, f)


if __name__ == "__main__":
    main(sys.argv)
