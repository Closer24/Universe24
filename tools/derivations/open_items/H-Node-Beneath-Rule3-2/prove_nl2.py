"""The core's proof against the engine's own acts, bit for bit, on a real run (H-Node-Beneath-Rule3-2): every state-moving act of the engine is wrapped (nothing under src edited; the wrappers compare and return the engine's own result), the core's composition of the three primitives computed from the same reads at every call and compared bit for bit; the counts per act and the mismatches printed. Mode `node`: the node world (the 3-cube at 20) forward 20 and back 20 through tests/laws.run_back_exact. Mode `hole` or `chiral`: the hole 60 or the chiral 60 with back 20 through event_universe.run.main, the record compared key by key with the committed record under examples/records (the rows' milliseconds struck).

Usage: PYTHONPATH=<worktree>/src python prove_nl2.py <worktree> node|hole|chiral <out dir>
"""

from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

import numpy as np

worktree = Path(sys.argv[1])
mode, out_dir = sys.argv[2], Path(sys.argv[3])
sys.path.insert(0, str(worktree))
sys.path.insert(0, str(worktree / "src"))

spec = importlib.util.spec_from_file_location("core_nl2", Path(__file__).with_name("core_nl2.py"))
core = importlib.util.module_from_spec(spec)
spec.loader.exec_module(core)

import event_universe.bodies as B  # noqa: E402
import event_universe.close as C  # noqa: E402
import event_universe.core.rule3 as R  # noqa: E402
import event_universe.gram as G  # noqa: E402
import event_universe.interval as I  # noqa: E402
import event_universe.merger as M  # noqa: E402
import event_universe.node as N  # noqa: E402
import event_universe.take as T  # noqa: E402

counts: dict[str, int] = {}
mismatch: dict[str, int] = {}


def same(x, y) -> bool:
    a, b = np.asarray(x, dtype=object), np.asarray(y, dtype=object)
    return a.shape == b.shape and bool(np.all(a == b))


def same_at(top, x, y) -> bool:
    a, b = np.asarray(x, dtype=object), np.asarray(y, dtype=object)
    if a.ndim == 0:
        a = a + np.zeros(np.shape(top), dtype=object)
    if b.ndim == 0:
        b = b + np.zeros(np.shape(top), dtype=object)
    return bool(np.all(a[top] == b[top]))


def tally(name: str, ok: bool) -> None:
    counts[name] = counts.get(name, 0) + 1
    if not ok:
        mismatch[name] = mismatch.get(name, 0) + 1


orig_cd = R.carried_division


def cd(total, wall, remainder, direction=1):
    found = orig_cd(total, wall, remainder, direction)
    q, r = core.divide(total, wall, remainder, direction)
    tally("divide", same(found[0], q) and same(found[1], r))
    return found


R.carried_division = cd
N.carried_division = cd
I.carried_division = cd

orig_rotate = N.Node.rotate


def rotate(self, lines, r, turn, direction, flux, starts):
    pairs = [(line.now, line.before)[::direction] for line in lines]
    at = starts or [a for a, _y in pairs]
    fluxes = flux or [0] * len(lines)
    ms = self.arrivals(at, r, turn)
    rems = [line.rem for line in lines]
    found = orig_rotate(self, lines, r, turn, direction, flux, starts)
    for (_a, y), aa, f, m, rem, out in zip(pairs, at, fluxes, ms, rems, found, strict=True):
        q, start, rem2 = core.rotate(aa, y, rem, r.self_coefficient, r.wall, f + m, direction)
        now, before = core.placed(q, start, direction)
        tally("rotate", same(out.now, now) and same(out.before, before) and same(out.rem, rem2))
    return found


N.Node.rotate = rotate

orig_write = N.Node.write


def write(self, line, numerator, direction):
    now0, wr0 = line.now, line.wr
    orig_write(self, line, numerator, direction)
    n2, w2 = core.write(now0, wr0, numerator, line.wwall, direction)
    tally("write", same(line.now, n2) and same(line.wr, w2))


N.Node.write = write

orig_exchange = N.Node.exchange


def exchange(self, top, held):
    orig_exchange(self, top, held)
    for r, row, hrow in zip(self.rows_, self.rows(), held, strict=True):
        k = G.conjugation(r.shape)
        nn, nb, nr = core.exchange_row(
            [h.now for h in hrow], [h.before for h in hrow], [h.rem for h in hrow], [h.wall for h in hrow], k
        )
        for i, (line, h) in enumerate(zip(row, hrow, strict=True)):
            ok = same_at(top, line.now, nn[i]) and same_at(top, line.before, nb[i]) and same_at(top, line.rem, nr[i])
            if line.wr is not None:
                ok = ok and same_at(top, line.wr, core.mirror(h.wr, line.wwall, 1))
            tally("exchange", ok)


N.Node.exchange = exchange

orig_move = T.move


def move(node, rec, k, at, count):
    lines = node.records()[rec].lines
    wall, now0, rem0 = T.at_node(lines[k].wall, at), int(lines[k].now[at]), int(lines[k].rem[at])
    orig_move(node, rec, k, at, count)
    tally("move", int(lines[k].now[at]) == core.move(now0, rem0, count, wall))


for module in (T, C, M, B):
    module.move = move

orig_lay = T.lay


def lay(node, rec, where, levels, sign=1):
    lines = node.records()[rec].lines
    before = [(np.asarray(z.now[where], dtype=object).copy(), np.asarray(z.before[where], dtype=object).copy()) for z in lines]
    orig_lay(node, rec, where, levels, sign)
    for z, (n0, b0), n, b in zip(lines, before, levels[0::2], levels[1::2], strict=True):
        tally("lay", same(z.now[where], core.lay(n0, n, sign)) and same(z.before[where], core.lay(b0, b, sign)))


for module in (T, C, M):
    module.lay = lay


def report(extra: dict) -> None:
    found = {"mode": mode, "calls": counts, "mismatches": mismatch, **extra}
    print(json.dumps(found))
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / f"proof_{mode}.json").write_text(json.dumps(found, indent=1) + "\n")


if mode == "node":
    from tests.laws import node_of, run_back_exact

    node = node_of("world_node.json")
    n = 20
    got = run_back_exact(node, n)
    report({"intervals": n, "run_back_exact": got, "births": node.counts["births"], "turns": node.counts["turns"]})
elif mode in ("hole", "chiral"):
    from event_universe.run import main

    world = {"hole": "world_hole.json", "chiral": "world_nature.json"}[mode]
    out = out_dir / f"{mode}_nl2.json"
    main(["run", str(worktree / "tests" / "worlds" / world), str(out), "back", "20"])
    mine = json.loads(out.read_text())
    theirs = json.loads((worktree / "examples" / "records" / f"{mode}.json").read_text())
    verdict = {}
    for key in sorted(set(mine) | set(theirs)):
        a, b = mine.get(key), theirs.get(key)
        if key == "rows":
            a = [{k: v for k, v in row.items() if k != "milliseconds"} for row in a]
            b = [{k: v for k, v in row.items() if k != "milliseconds"} for row in b]
        verdict[key] = "EQUAL" if a == b else "APART"
    report({"record": verdict, "log_entries": len(mine["log"]), "counts": mine["counts"]})
