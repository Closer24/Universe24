"""cs6's runner: cs5_run.py (cs4's runner: the light pattern laid by the script on the gap-0 plane, the diag line per interval, the landing census) with the twin lays of this round, each laid at the interval 0 after the world file's lays and the pattern:
  "no_pattern": 1              no light pattern (the world file's sea alone beneath the matter: ma2's board);
  "rest_pairs": [{"row": r, "quanta": n, "sense": s}, ...]
                               ma2's uniform lay of a record with a gap at rest at every Node (seed.rest_record over the envelope 1 at the vector (1, 0)), the least amplitude whose share at a Node is at or above n units of the record (ma2's fitted_uniform: seed.fitted's search, its answer plus one); s in -1, 1;
  "children_from": "<record.json>", "children_at": i
                               the born board's twin by hand: every birth of that record at the interval i laid as the close lays it (close.child_at: the - child at its - end and the + child at its + end, (A, 0, 0, sense B) with A B = T div 2), no light taken;
Usage: python cs6_run.py <world.json> <out.json> <pattern.json> [back N]"""

from __future__ import annotations

import json
import sys
from typing import Any

import numpy as np

import cs5_run as base
from event_universe import close, run, seed
from event_universe.core.rule3 import quotient
from event_universe.loader.world import load_world
from event_universe.node import Node
from event_universe.rows import PLANE, Line, zeros


def rest_levels(node: Node, rec: int, amplitude: int, sense: int) -> list[Line]:
    row = node.records()[rec]
    env = zeros(node.shape) + 1
    return seed.rest_record(node, row, env, 1, amplitude, sense, [1, 0])


def share_at_origin(node: Node, rec: int, lines: list[Line]) -> int:
    row = node.records()[rec]
    rule = node.rule_of(row, node.content(), node.link_factors())
    re = Line(lines[0].now, lines[0].before, None, node.w)
    im = Line(lines[1].now, lines[1].before, None, node.w)
    return int(node.share([re, im], rule).reshape(-1)[0])


def fitted_uniform(node: Node, rec: int, sense: int, target: int) -> int:
    """The least amplitude whose share per Node is at least the target (ma2's search: seed.fitted's form, its answer plus one)."""
    high = 1
    while share_at_origin(node, rec, rest_levels(node, rec, high, sense)) <= target:
        high = high + high
    low = 0
    while high - low > 1:
        middle = int(quotient(low + high, 2))
        if share_at_origin(node, rec, rest_levels(node, rec, middle, sense)) <= target:
            low = middle
        else:
            high = middle
    return low + 1


def lay_rest_pairs(node: Node, lays: list[dict[str, Any]]) -> None:
    for lay in lays:
        row = node.by_index[int(lay["row"])]
        rec = node.records().index(row)
        n, sense = int(lay["quanta"]), int(lay["sense"])
        amplitude = fitted_uniform(node, rec, sense, n * node.units[rec])
        lines = rest_levels(node, rec, amplitude, sense)
        node.lay(rec, Ellipsis, tuple(x for line in lines for x in (line.now, line.before)))
        node.start_content = node.content()
        node.log.append(
            {
                "event": "lay_rest_pair",
                "i": 0,
                "line_pair": rec,
                "row_index": int(lay["row"]),
                "quanta": n,
                "sense": sense,
                "amplitude": amplitude,
                "share": share_at_origin(node, rec, lines),
                "unit": node.units[rec],
                "levels_at_origin": [int(x.reshape(-1)[0]) for line in lines for x in (line.now, line.before)],
            }
        )


def lay_children(node: Node, path: str, at_interval: int) -> None:
    """The births of a record at the named interval laid by hand as the close laid them (close.child_at), no light taken."""
    with open(path, encoding="utf-8") as f:
        rec = json.load(f)
    births = [e for e in rec["log"] if e["event"] == "birth" and int(e["i"]) == at_interval]
    laid = 0
    for e in births:
        s = int(e["line_pair"])
        close.child_at(node, s, tuple(int(x) for x in e["minus"]), -1)
        close.child_at(node, s, tuple(int(x) for x in e["plus"]), 1)
        laid += 2
    node.start_content = node.content()
    node.log.append({"event": "lay_children", "i": 0, "from": path, "at": at_interval, "births": len(births), "children": laid, "amplitude": [node.A, node.B]})


class Cs6Node(base.CsNode):
    def __init__(self, universe: dict[str, Any], world: dict[str, Any], pattern: dict[str, Any]) -> None:
        Node.__init__(self, universe, world)
        if int(pattern.get("no_pattern", 0)) == 1:
            self.lay_line = {"event": "no_pattern", "i": 0}
            base.PHASES[:] = []
        else:
            self.lay_line = base.lay_pattern(self, pattern)
        if "rest_pairs" in pattern:
            lay_rest_pairs(self, pattern["rest_pairs"])
        if "children_from" in pattern:
            lay_children(self, pattern["children_from"], int(pattern["children_at"]))
        self.dump_at = {int(v) for v in pattern.get("dump_at", [])}
        self.dumps: list[dict[str, Any]] = []
        self.diag: list[dict[str, Any]] = [self.read_diag()]


def main(argv: list[str]) -> None:
    sys.set_int_max_str_digits(0)
    universe, world = load_world(argv[1])
    with open(argv[3], encoding="utf-8") as f:
        pattern = json.load(f)
    back = int(argv[argv.index("back") + 1]) if "back" in argv else 0
    node = Cs6Node(universe, world, pattern)
    intervals = int(world["intervals"])
    out = lambda line: print(line, flush=True)
    out(json.dumps({"lay": {k: v for k, v in node.lay_line.items() if k != "phases"}, "extra": [e for e in node.log if e["event"] in ("lay_rest_pair", "lay_children")], "diag0": node.diag[0]}))
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


if __name__ == "__main__":
    main(sys.argv)
