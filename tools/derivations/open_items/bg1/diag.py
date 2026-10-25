"""bg1's diagnostic runner (2026-10-25): the engine's own Node and Interval (src untouched; the subclass below reads what the
acts compute and writes one JSON line per interval), decomposing the carrier's time line at every interval into the law's terms:
the mass term SUM quotient(D X_now, w) (the pair's gap, the negative exponent-2 term of The sign side of the exponent), the Links'
term SUM quotient(SUM_j R_j (X_j - X_i), w), the write's quotient SUM ((numerator + wr) div wwall) and the forms by row (the sum
over the board of u_in u_out + (-a F) div w per riding row), with the board's mean X, the max content, the turns, the births and
the body clicks. Usage: diag.py <world.json> <out.jsonl> [intervals N] [back N] [flag NAME]
`flag NAME` runs the flagged copy under tools/derivations/bg1/engine (BG1=NAME in the environment) in place of src; absent, src."""
from __future__ import annotations

import json
import os
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
argv = sys.argv[1:]
if "flag" in argv:
    os.environ["BG1"] = argv[argv.index("flag") + 1]
    sys.path.insert(0, os.path.join(HERE, "engine"))
else:
    os.environ.pop("BG1", None)
    sys.path.insert(0, os.path.join(HERE, "..", "..", "..", "src"))

import numpy as np  # noqa: E402

from event_universe import interval as interval_module  # noqa: E402
from event_universe import run as run_module  # noqa: E402
from event_universe.core import paces  # noqa: E402
from event_universe.core.rule3 import held_numerator, quotient  # noqa: E402
from event_universe.loader.world import load_world  # noqa: E402
from event_universe.node import Node  # noqa: E402
from event_universe.rows import TRACE  # noqa: E402

LINES: list[dict] = []


def total(a) -> int:
    return int(sum(int(x) for x in np.asarray(a, dtype=object).reshape(-1)))


class Diag(interval_module.Interval):
    """The engine's Interval with the readings written beside the acts, forward alone."""

    def kicks(self) -> None:
        super().kicks()
        if self.direction != 1:
            return
        node = self.node
        d = 2 * node.w * self.x_now
        by_row = {}
        for r in self.riders:
            k = self.where[id(r)]
            w_side = self.mean_wall()
            p_side = [w_side * (line.now - line.before) + line.rem - (w_side // 2) for line in self.rows[k]]
            uu, af = 0, 0
            for a, f, p1, p2 in zip(self.starts[k], self.force[k], p_side, self.kicked[k], strict=True):
                uu += total(paces.odd_rounded(2 * p1 + 1, d) * paces.odd_rounded(2 * p2 + 1, d))
                af += total(quotient(-a * f, node.w))
            name = f"shape{r.shape}" + ("" if r.pair is None else f"_gap{'0' if r.gap == 0 else 'N'}_{node.rows_.index(r)}")
            by_row[name] = [uu, af]
        self.diag_rows = by_row

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
            pi = np.asarray(self.pi, dtype=object)
            weights = np.vectorize(lambda p: node.gamma**4 // (int(p) * int(p)) if int(p) else 0, otypes=[object])(pi)
            self.diag_carrier = {
                "x_mean": total(x) // x.size,
                "xw_mean": total(x * weights) // max(1, total(weights)),
                "x_max": int(max(int(v) for v in x.reshape(-1))),
                "mass_sum": total(mass),
                "links_sum": total(links),
                "write_sum": total(write),
                "write_min": int(min(int(v) for v in write.reshape(-1))),
                "write_max": int(max(int(v) for v in write.reshape(-1))),
                "forms_sum": total(self.forms),
                "trace_sum": total(self.trace),
                "num_bits": int(max(abs(int(v)).bit_length() for v in numerator.reshape(-1))),
                "content_max": int(max(int(v) for v in self.c.reshape(-1))),
                "p0_min": int(min(int(v) for v in np.asarray(self.p0, dtype=object).reshape(-1))),
            }
        super().carrier_act()

    def close(self) -> None:
        super().close()
        node = self.node
        row = {"i": node.interval, **self.diag_carrier, "rows": self.diag_rows,
               "turned": int(node.turned.sum()), "births": node.counts["births"],
               "body_clicks": node.counts["body_clicks"], "turns": node.counts["turns"],
               "laid": node.counts["laid"], "transient_bits": node.max_transient}
        LINES.append(row)


def main() -> None:
    sys.set_int_max_str_digits(0)
    universe, world = load_world(argv[0])
    if "intervals" in argv:
        world = dict(world, intervals=int(argv[argv.index("intervals") + 1]))
    back = int(argv[argv.index("back") + 1]) if "back" in argv else 0
    interval_module.Interval = Diag
    t0 = time.monotonic()
    found = run_module.record(universe, world, back, lambda line: None)
    node_bits = max(int(r["max bits"]) for r in found["rows"])
    summary = {"world": argv[0], "flag": os.environ.get("BG1"), "intervals": int(world["intervals"]),
               "counts": found["counts"], "turns_list_len": len(found["turns"]), "run_back": found["run_back"],
               "state_bits": node_bits, "transient_bits": max(int(r["max transient bits"]) for r in found["rows"]),
               "integers": found["rows"][-1]["integers"], "seconds": int(time.monotonic() - t0),
               "volume_mean_marks": [[r["i"], r["volume mean"], r["content min/mean/max"]] for r in found["rows"]],
               "credits": sum(1 for e in found["log"] if e["event"] == "credit"),
               "births_log": sum(1 for e in found["log"] if e["event"] == "birth")}
    with open(argv[1], "w", encoding="utf-8") as out:
        out.write(json.dumps({"summary": summary}) + "\n")
        for line in LINES:
            out.write(json.dumps(line) + "\n")
    with open(argv[1].replace(".jsonl", "_record.json"), "w", encoding="utf-8") as out:
        json.dump({k: v for k, v in found.items() if k != "nodes"}, out)
    print(json.dumps(summary))


if __name__ == "__main__":
    main()
