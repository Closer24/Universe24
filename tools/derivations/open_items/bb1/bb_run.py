"""bb1's runner (2026-10-25): the engine's own Node and Interval (src untouched; the subclass reads what the acts
compute, forward alone, and writes one JSON line per interval): the board's mean, least and largest X, the mass term
SUM quotient(D X, w), the Links' term SUM quotient(SUM_j R_j (X_j - X_i), w), the write's quotient, the spread e
(the neighbours' X ratio less 1, in thousandths: the largest over the Links and the mean over the Links), the sum
over the Nodes of largest_below(Gamma X) (the lift's unit), the turns, the births, the refusals.
Usage: bb_run.py <world.json> <out_prefix> [back N] [pulse A] [wave A] [sym]
`pulse A` lays A levels (below one quantum) on the gap-0 line's now at the board's centre after the file's lays, the
fourth form the file would need; `wave A` lays R4's standing wave about the centre on the 3-cube, now = A P(x) P(y) P(z)
with P = (-1/2, 1, -1/2) (A a multiple of 8), before = -now div 2; `sym` counts the 48 about the centre at the end.
Writes <out_prefix>.jsonl (the summary line, then one line per interval), <out_prefix>_record.json (the record with the
Node lines' X alone, for the gates). Integers only."""
from __future__ import annotations

import itertools
import json
import os
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.environ.get("BB1_SRC", os.path.join(HERE, "..", "..", "..", "src")))

import numpy as np  # noqa: E402

from event_universe import interval as interval_module  # noqa: E402
from event_universe import run as run_module  # noqa: E402
from event_universe.core.paces import sine_den  # noqa: E402
from event_universe.core.ports import AXES, across  # noqa: E402
from event_universe.core.rule3 import held_numerator, largest_below, quotient  # noqa: E402
from event_universe.loader.world import load_world  # noqa: E402
from event_universe.node import Node  # noqa: E402
from event_universe.rows import PLANE, TRACE  # noqa: E402

LINES: list[dict] = []
THOUSAND = 1000


def total(a) -> int:
    return int(sum(int(x) for x in np.asarray(a, dtype=object).reshape(-1)))


def spread(x) -> tuple[int, int, int]:
    """The spread over the Links: max and mean of |X_j - X_i| 1000 div min(X_i, X_j), and the Link count."""
    emax, esum, n = 0, 0, 0
    for axis in range(AXES):
        xj = across(x, 2 * axis)
        for a, b in zip(x.reshape(-1), xj.reshape(-1), strict=True):
            a, b = int(a), int(b)
            e = abs(b - a) * THOUSAND // max(1, min(a, b))
            emax = max(emax, e)
            esum += e
            n += 1
    return emax, esum // n, n


class Diag(interval_module.Interval):
    def carrier_act(self) -> None:
        node, carrier = self.node, self.carrier
        if self.direction == 1:
            rule = node.rule_of(carrier, self.c, self.factors)
            x = self.x_now
            line = self.rows[self.where[id(carrier)]][0]
            arrivals = node.arrivals([x], rule, None)[0]
            links = quotient(arrivals - sum(rule.reaches) * x, rule.wall)
            mass = quotient(rule.mass * x, rule.wall)
            numerator = held_numerator(TRACE, x, self.forms, self.trace, self.p0, node.den, node.gamma)
            write = (numerator + line.wr) // line.wwall
            emax, emean, _n = spread(x)
            roots = sum(largest_below(node.gamma * int(v)) for v in x.reshape(-1))
            self.diag_carrier = {
                "x_mean": total(x) // x.size,
                "x_min": int(min(int(v) for v in x.reshape(-1))),
                "x_max": int(max(int(v) for v in x.reshape(-1))),
                "mass_sum": total(mass),
                "links_sum": total(links),
                "write_sum": total(write),
                "forms_sum": total(self.forms),
                "e_max": emax,
                "e_mean": emean,
                "sqrt_gx_sum": roots,
                "num_bits": int(max(abs(int(v)).bit_length() for v in numerator.reshape(-1))),
                "content_max": int(max(int(v) for v in self.c.reshape(-1))),
                "content_min": int(min(int(v) for v in self.c.reshape(-1))),
            }
        super().carrier_act()

    def close(self) -> None:
        super().close()
        node = self.node
        LINES.append(
            {
                "i": node.interval,
                **self.diag_carrier,
                "turned": int(node.turned.sum()),
                "births": node.counts["births"],
                "body_clicks": node.counts["body_clicks"],
                "turns": node.counts["turns"],
                "refused_lay": node.counts["refused_lay"],
                "refused_orientation": node.counts["refused_orientation"],
                "refused_stop": node.counts["refused_stop"],
                "transient_bits": node.max_transient,
            }
        )


def images48(cube: int):
    """The 48 signed permutations of the axes about the centre of an odd cube, each as an index map."""
    centre = cube // 2
    idx = np.indices((cube,) * AXES)
    found = []
    for perm in itertools.permutations(range(AXES)):
        for signs in itertools.product((1, -1), repeat=AXES):
            coords = tuple((centre + signs[a] * (idx[perm[a]] - centre)) % cube for a in range(AXES))
            found.append(coords)
    return found


def count48(node: Node) -> int:
    """How many of the 48 leave every level and remainder array of the state unchanged."""
    arrays = [a for line in node.all_lines() for a in (line.now, line.before, line.rem)]
    arrays += [line.wr for line in node.all_lines() if line.wr is not None]
    kept = 0
    for coords in images48(node.cube):
        ok = True
        for a in arrays:
            b = np.asarray(a, dtype=object)
            if np.ndim(b) == 0:
                continue
            if not np.array_equal(b[coords], b):
                ok = False
                break
        kept += ok
    return kept


def extra_lays(node: Node, argv: list[str]) -> dict:
    rec = node.records().index(node.row(PLANE, gap=0))
    centre = (node.cube // 2,) * AXES
    laid = {}
    if "pulse" in argv:
        amp = int(argv[argv.index("pulse") + 1])
        node.lay(rec, centre, (amp, 0, 0, 0))
        laid["pulse"] = amp
    if "wave" in argv:
        amp = int(argv[argv.index("wave") + 1])
        p = {0: -1, 1: 2, 2: -1}  # doubled P over the 3-cube about the centre 1
        now = np.zeros(node.shape, dtype=object)
        for at in np.ndindex(*node.shape):
            now[at] = amp * p[at[0]] * p[at[1]] * p[at[2]] // 8
        before = np.vectorize(lambda v: (-int(v)) // 2, otypes=[object])(now)
        node.lay(rec, Ellipsis, (now, before, 0, 0))
        laid["wave"] = amp
    return laid


def runs_of(series: list[tuple[int, int]]) -> list[tuple[int, int, int, int]]:
    """The series' monotone runs as (start interval, end interval, start value, end value)."""
    found = []
    start = 0
    for k in range(1, len(series)):
        d_now = series[k][1] - series[k - 1][1]
        d_prev = series[k - 1][1] - series[max(0, k - 2)][1] if k >= 2 else d_now
        if (d_now < 0) != (d_prev < 0) and k >= 2:
            found.append((series[start][0], series[k - 1][0], series[start][1], series[k - 1][1]))
            start = k - 1
    found.append((series[start][0], series[-1][0], series[start][1], series[-1][1]))
    return found


def main() -> None:
    sys.set_int_max_str_digits(0)
    argv = sys.argv[1:]
    universe, world = load_world(argv[0])
    back = int(argv[argv.index("back") + 1]) if "back" in argv else 0
    interval_module.Interval = Diag
    t0 = time.monotonic()
    node = Node(universe, world)
    laid = extra_lays(node, argv)
    intervals = int(world["intervals"])
    rows, nodes, hashes = run_module.forward(node, intervals, back, lambda line: None)
    kept_log = list(node.log)
    sym_end = count48(node) if "sym" in argv else None
    returned = run_module.run_back(node, hashes) if back else None
    counts = {k: int(v) for k, v in node.counts.items()}
    record = {
        "world": world,
        "universe": universe,
        "den": node.den,
        "cube": node.cube,
        "intervals": intervals,
        "gapped": [(str(r.pair[0]), str(sine_den(r.pair[0], node.den))) for r in node.gapped if r.pair],
        "planes": [str(r.pair[0]) for r in node.records() if r.pair],
        "T": node.T,
        "gamma": node.gamma,
        "G": node.G,
        "counts": {k: str(v) for k, v in counts.items()},
        "turns": node.turns,
        "rows": rows,
        "nodes": nodes,
        "run_back": returned,
        "log": kept_log,
    }
    xs = [(line["i"], line["x_mean"]) for line in LINES]
    tops = [xs[k] for k in range(1, len(xs) - 1) if xs[k][1] > xs[k - 1][1] and xs[k][1] >= xs[k + 1][1]]
    at_seed = [i for i, v in xs if v == node.gamma]
    uniform = [line["i"] for line in LINES if line["x_min"] == line["x_max"]]
    summary = {
        "world": argv[0],
        "laid": laid,
        "intervals": intervals,
        "counts": counts,
        "run_back": returned,
        "state_bits": max(int(r["max bits"]) for r in rows),
        "transient_bits": max(int(r["max transient bits"]) for r in rows),
        "integers": rows[-1]["integers"],
        "seconds": int(time.monotonic() - t0),
        "tops (interval, mean X)": tops[:12],
        "intervals at the seed's mean X": at_seed[:12],
        "uniform intervals (x_min == x_max)": len(uniform),
        "runs of the mean (start, end, X start, X end)": runs_of(xs)[:12],
        "e_max course at every 20": [(line["i"], line["e_max"], line["e_mean"]) for line in LINES[::20]],
        "links_sum max / mass_sum max": [max(line["links_sum"] for line in LINES), max(line["mass_sum"] for line in LINES)],
        "48 at the end": sym_end,
        "births_by_interval": sorted({e["i"] for e in kept_log if e["event"] == "birth"}),
        "credits": sum(1 for e in kept_log if e["event"] == "credit"),
        "marks": [[r["i"], r["volume mean"], r["content min/mean/max"]] for r in rows],
    }
    with open(argv[1] + ".jsonl", "w", encoding="utf-8") as out:
        out.write(json.dumps({"summary": summary}) + "\n")
        for line in LINES:
            out.write(json.dumps(line) + "\n")
    with open(argv[1] + "_record.json", "w", encoding="utf-8") as out:
        json.dump(record, out)
    print(json.dumps(summary))


if __name__ == "__main__":
    main()
