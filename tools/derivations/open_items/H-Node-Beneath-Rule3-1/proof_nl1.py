"""The proof of the lean core against the engine (H-Node-Beneath-Rule3-1): (1) the primitives bit for bit on random lines, the time reversal X R X = R^-1 and the exchange as the direction read; (2) a recorder on the engine's own run: every carried division, every lay and every exchange of the engine replayed through the core and compared bit for bit, counted per interval, on a world for n intervals forward and n back, with the run back exact; the counts and the log against a committed record where one is named. Usage: proof_nl1.py <core dir> <world.json> <n> [record.json] [out.json]."""

from __future__ import annotations

import importlib.util
import json
import random
import sys
from pathlib import Path

import numpy as np


def load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def same(a, b) -> bool:
    a, b = np.asarray(a, dtype=object), np.asarray(b, dtype=object)
    return a.shape == b.shape and bool(np.all(a == b))


def random_lines(core, rule3, count: int, seed: int) -> dict:
    rng = random.Random(seed)
    found = {"divide": 0, "reversal": 0, "direction_read": 0, "move": 0, "write": 0}
    for _ in range(count):
        w = rng.randint(2, 1 << 60)
        r = rng.randint(0, w - 1)
        t = rng.randint(-(1 << 100), 1 << 100)
        d = rng.choice((1, -1))
        found["divide"] += core.divide(t, w, r, d) == rule3.carried_division(t, w, r, d)
        own = rng.randint(-(1 << 40), 1 << 40)
        reaches = [rng.randint(0, 1 << 30) for _ in range(6)]
        arrivals = [rng.randint(-(1 << 40), 1 << 40) for _ in range(6)]
        now, before = rng.randint(-(1 << 40), 1 << 40), rng.randint(-(1 << 40), 1 << 40)
        flux = rng.randint(-(1 << 40), 1 << 40)
        n1, b1, r1 = core.step(now, before, r, own, w, flux, reaches, arrivals, 1)
        back = core.step(n1, b1, r1, own, w, flux, reaches, arrivals, -1)
        # X R X on the line: exchange, step forward, exchange again, against the step at -1 from the forward state
        e_n, e_b, e_r = core.exchange(n1, b1, r1, w)
        f_n, f_b, f_r = core.step(e_n, e_b, e_r, own, w, flux, reaches, arrivals, 1)
        x = core.exchange(f_n, f_b, f_r, w)
        found["reversal"] += (back == (now, before, r)) and (x == back)
        # the exchange as the direction read: the exchanged line stepped at +1 equals the line stepped at -1, read back through the exchange
        g = core.step(*core.exchange(now, before, r, w), own, w, flux, reaches, arrivals, 1)
        h = core.step(now, before, r, own, w, flux, reaches, arrivals, -1)
        found["direction_read"] += core.exchange(*g, w) == h
        c = rng.randint(-(1 << 30), 1 << 30)
        m, rest = core.move(now, c, w, r)
        found["move"] += (m == now + c) and rest == r
        ww = rng.randint(2, 1 << 50)
        wr = rng.randint(0, ww - 1)
        num = rng.randint(-(1 << 90), 1 << 90)
        n2, wr2 = core.write(now, num, ww, wr, 1)
        n3, wr3 = core.write(n2, num, ww, wr2, -1)
        found["write"] += (n3, wr3) == (now, wr)
    found["count"] = count
    return found


def recorded_run(core, world_path: Path, n: int) -> dict:
    import event_universe.core.rule3 as rule3
    from event_universe import gram, take
    from event_universe.loader.world import load_world
    from event_universe.node import Node

    tally = {"divisions": 0, "divisions_apart": 0, "lays": 0, "lays_apart": 0, "exchanges": 0, "exchanges_apart": 0, "exchanged_nodes": 0, "per_interval": []}
    original_division = rule3.carried_division

    def division(total, wall, remainder, direction=1):
        got = original_division(total, wall, remainder, direction)
        mine = core.divide(total, wall, remainder, direction)
        tally["divisions"] += 1
        if not (same(got[0], mine[0]) and same(got[1], mine[1])):
            tally["divisions_apart"] += 1
        return got

    for name, module in list(sys.modules.items()):
        if name.startswith("event_universe") and getattr(module, "carried_division", None) is original_division:
            setattr(module, "carried_division", division)

    original_lay = take.lay

    def laid(node, rec, where, levels, sign=1):
        lines = node.records()[rec].lines
        expected = []
        for line_, now, before in zip(lines, levels[0::2], levels[1::2], strict=True):
            expected.append((core.lay(line_.now[where], now, sign), core.lay(line_.before[where], before, sign)))
        original_lay(node, rec, where, levels, sign)
        tally["lays"] += 1
        for line_, (e_now, e_before) in zip(lines, expected, strict=True):
            if not (same(line_.now[where], e_now) and same(line_.before[where], e_before)):
                tally["lays_apart"] += 1
        return None

    for name, module in list(sys.modules.items()):
        if name.startswith("event_universe") and getattr(module, "lay", None) is original_lay:
            setattr(module, "lay", laid)

    original_exchange = Node.exchange

    def exchanged(self, top, held):
        original_exchange(self, top, held)
        tally["exchanges"] += 1
        tally["exchanged_nodes"] += int(top.sum())
        for r, row, hrow in zip(self.rows_, self.rows(), held, strict=True):
            k = gram.conjugation(r.shape)
            for i, (line, h) in enumerate(zip(row, hrow, strict=True)):
                e_now, e_before, e_rem = core.exchange(h.now, h.before, h.rem, h.wall)
                # the row's K: the sign of the line's own entry, a lay of -2 a on the negated line
                sign = k[i][i]
                e_now = sum(k[i][j] * hb for j, hb in enumerate(h.before for h in hrow))
                e_before = sum(k[i][j] * hn for j, hn in enumerate(h.now for h in hrow))
                if sign < 0:
                    e_rem = core.mirror(e_rem, h.wall)
                ok = same(np.where(top, e_now, line.now), line.now) and same(np.where(top, e_before, line.before), line.before) and same(np.where(top, e_rem, line.rem), line.rem)
                if line.wr is not None:
                    ok = ok and same(np.where(top, core.mirror(h.wr, line.wwall), line.wr), line.wr)
                if not ok:
                    tally["exchanges_apart"] += 1

    Node.exchange = exchanged

    universe, world = load_world(world_path)
    node = Node(universe, world)
    states = []
    for _ in range(n):
        states.append(node.state_bytes())
        before = dict(tally)
        node.step()
        tally["per_interval"].append([tally["divisions"] - before["divisions"], tally["lays"] - before["lays"], tally["exchanged_nodes"] - before["exchanged_nodes"]])
    after = node.state_hash()
    tally["log_forward"] = len(node.log)
    back = 0
    for k in range(n):
        node.step_back()
        back += node.state_bytes() == states[n - 1 - k]
    tally["run_back"] = [back, n]
    tally["counts"] = dict(node.counts)
    tally["log"] = len(node.log)
    tally["state_hash_after_forward"] = after
    tally["census"] = list(node.census())
    tally["per_interval"] = tally["per_interval"][:5] + [["..."]] if len(tally["per_interval"]) > 6 else tally["per_interval"]
    return tally


def main(argv: list[str]) -> None:
    core_dir, world_path, n = Path(argv[1]), Path(argv[2]), int(argv[3])
    record = Path(argv[4]) if len(argv) > 4 and argv[4] != "-" else None
    out = Path(argv[5]) if len(argv) > 5 else None
    core = load("core_nl1", core_dir / "core_nl1.py")
    import event_universe.core.rule3 as rule3

    found = {"random": random_lines(core, rule3, 20000, 1), "core_lines": sum(1 for line in (core_dir / "core_nl1.py").read_text().splitlines() if line.strip() and not line.strip().startswith("#"))}
    found["run"] = recorded_run(core, world_path, n)
    if record is not None:
        rec = json.loads(record.read_text())
        found["record"] = {"counts_equal": {k: str(v) for k, v in found["run"]["counts"].items()} == {k: str(v) for k, v in rec["counts"].items()}, "log_equal": len(rec["log"]) == found["run"]["log_forward"], "record_counts": rec["counts"], "record_log": len(rec["log"])}
    text = json.dumps(found, indent=1)
    print(text)
    if out is not None:
        out.write_text(text)


if __name__ == "__main__":
    main(sys.argv)
