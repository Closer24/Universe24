"""The record module's proof: the engine run through one_record's writer with every log line, the frame, the census and the counts taken from one_record (the engine's spellings replaced in-process: close.refused, bodies.credit, close.children, merger.read_ends' stop line, Interval.close, Node.census/arrays/state_bytes/state_hash, node.COUNTS), the record compared bit for bit with the committed record (the rows' milliseconds struck). Usage: python prove_record.py <world.json> <committed record.json> <out.json> [back N]."""

from __future__ import annotations

import json
import os
import sys
from typing import Any

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import one_record as rec  # noqa: E402
from event_universe.loader.world import load_world  # noqa: E402


def main(argv: list[str]) -> int:
    sys.set_int_max_str_digits(0)
    world_path, committed_path, out_path = argv[1], argv[2], argv[3]
    back = int(argv[argv.index("back") + 1]) if "back" in argv else 0
    close = sys.modules["event_universe.close"]
    bodies = sys.modules["event_universe.bodies"]
    merger = sys.modules["event_universe.merger"]
    interval = sys.modules["event_universe.interval"]
    node_mod = sys.modules["event_universe.node"]

    # the refusal's one spelling
    close.refused = rec.refused

    # the credit's one spelling, the body's frame read by the close as before
    def credit(node: Any, r: int, at: Any, plane_starts: Any, fall: int, levels: int, taken_was: int, taken_before: int, line: int, rem_was: int, rem: int) -> dict[str, Any]:
        row = node.records()[r]
        read = bodies.frame_of(node, r, at, plane_starts) if row.shape == close.PLANE else bodies.bilinears_of(node, r, at)
        return rec.credit(node, r, at, read, fall, levels, taken_was, taken_before, line, rem_was, rem)

    bodies.credit = credit

    # close.children with the birth's dict through rec.birth (the stroke on close.py:223-252)
    def children(node: Any, at: Any, kids: Any, take: Any, r: int, c: Any, factors: Any) -> set[Any]:
        touched = {at}
        for kid in kids:
            s, minus, plus, _room = kid
            exact: list[Any] = []
            if "takes" in take:
                row = node.records()[s]
                walls = [t["booked"] for t in take["takes"]]
                rule = node.rule(row.pair, c, factors)
                dp_lay, w_children, stood, exact, ends = merger.light_children(node, s, minus, plus, walls, rule)
            else:
                dp_lay, w_children, stood, ends = close.child_laid(node, s, minus, plus)
            touched |= {minus, plus}
            node.counts["births"] += 1
            node.closes[at] += 1
            node.log.append(rec.birth(node, at, kid, take, r, dp_lay, w_children, stood, ends, len(kids), exact))
        return touched

    close.children = children

    # merger.read_ends with the stop refusal through rec.refused (the stroke on merger.py:138-139)
    def read_ends(node: Any, ends: Any, rule: Any, cause: int, r: int, cache: Any = None) -> Any:
        row = node.records()[r]
        found = []
        for where, wall in ends:
            rem_was = 0 if row is not node.emitter() else int(node.take_rem[where])
            owed = wall - rem_was
            if row is not node.emitter():
                levels: Any = merger.levels_at(row, where)
                fall, k = merger.share_fall(node, r, rule, where, levels, cache or {}), None
                short = fall < wall
            else:
                levels, fall, k = merger.fall_of(node, where, owed, rule, row)
                short = levels is None
            if short:
                rec.refused(node, where, "stop", cause, fall=fall, walls=wall, owed=owed, row=r)
                return None
            found.append((where, wall, levels, fall, k, rem_was, owed))
        return found

    merger.read_ends = read_ends

    # the frame through rec.frame (interval.py:256-268)
    def close_act(self: Any) -> None:
        node = self.node
        log_from = len(node.log)
        kept = rec.frame(node, self.top, log_from, self.frozen)
        node.click(self.plane_starts, self.held)
        node.stack.append(kept)

    interval.Interval.close = close_act

    # the census and the counts through the record module
    node_mod.Node.arrays = rec.arrays
    node_mod.Node.census = rec.census
    node_mod.Node.state_bytes = rec.state_bytes
    node_mod.Node.state_hash = rec.state_hash
    node_mod.COUNTS = rec.COUNTS

    universe, world = load_world(world_path)
    out: list[str] = []
    mine = rec.record(universe, world, back, out.append)
    with open(committed_path, encoding="utf-8") as f:
        committed = json.load(f)

    def struck(record: dict[str, Any]) -> dict[str, Any]:
        found = json.loads(json.dumps(record))
        for row in found["rows"]:
            row.pop("milliseconds", None)
        return found

    a, b = struck(mine), struck(committed)
    keys = sorted(set(a) | set(b))
    verdict = {k: (a.get(k) == b.get(k)) for k in keys}
    log_equal = sum(1 for x, y in zip(a["log"], b["log"], strict=False) if x == y)
    summary = {
        "world": world_path,
        "committed": committed_path,
        "keys": verdict,
        "log entries mine": len(a["log"]),
        "log entries committed": len(b["log"]),
        "log entries equal": log_equal,
        "counts": a["counts"],
        "run_back": a["run_back"],
        "equal": all(verdict.values()),
    }
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=1)
    print(json.dumps({k: v for k, v in summary.items() if k != "keys"}))
    print("keys apart:", [k for k, v in verdict.items() if not v])
    return 0 if summary["equal"] else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
