"""pl1's driver: the engine's own Node (src or the flagged copy by PYTHONPATH), with the uniform lay laid by the driver after the
file's lays as ma1 did (src untouched): a `plasma` lay puts one rest record of a plane with a gap at every Node at the sense given,
at the amplitude (i) `amplitude` given, or (ii) fitted to `quanta` (ma1's rule: the least amplitude at which the Node's share at
the vacuum's weight is at least n units), or (iii) `neutral`: the amplitude at which the Node's charge after the lay is nearest 0
(the least |W_standing + W_lay|; exact 0 where an integer gives it; the search over the amplitudes from 1 to the one whose |W| passes
the standing's and back), reading (b). Per interval the driver keeps the board's mean / least / largest X, the turned count, the
counts, W per record row and the Node's total at the Node (0, 0, 0) (every Node alike on a uniform board; the spread e is kept), and
the FULL state of that Node (every line's now, before, rem, wall, wr, wwall) for the retrace reading (read_retrace.py). At the end:
the run back of N intervals by the state hash, the census, the 48 on the levels about the cube's centre, the invariance under the
translations. Integers only. Usage: pl1_run.py <world.json> <out.json> [back N]"""

from __future__ import annotations

import itertools
import json
import sys
from pathlib import Path
from typing import Any

import numpy as np

from event_universe import gram, run
from event_universe.core.ports import AXES, across
from event_universe.loader.world import read_world
from event_universe.node import Node
from event_universe.rows import CARRIER, PLANE, POTENTIAL, zeros
from event_universe.seed import rest_record


def ints(a: Any) -> list[int]:
    return [int(x) for x in np.asarray(a, dtype=object).reshape(-1)]


def at0(a: Any) -> int:
    return int(np.asarray(a, dtype=object).reshape(-1)[0]) if np.ndim(a) else int(a)


def uniform_lines(node: Node, row: Any, amplitude: int, sense: int) -> list[Any]:
    return rest_record(node, row, zeros(node.shape) + 1, 1, amplitude, sense, [1, 0])


def share_at(node: Node, row: Any, rec: int, amplitude: int, sense: int) -> int:
    rule = node.rule(row.pair, node.content(), node.link_factors())
    return at0(node.share(uniform_lines(node, row, amplitude, sense), rule))


def charge_of(node: Node, row: Any, amplitude: int, sense: int) -> int:
    return at0(gram.charge(row.shape, uniform_lines(node, row, amplitude, sense)))


def fitted(node: Node, row: Any, rec: int, target: int, sense: int) -> int:
    """ma1's rule: the least amplitude whose share at the Node is at least the target (a search by comparisons)."""
    high = 1
    while share_at(node, row, rec, high, sense) < target:
        high = high + high
    low = 0
    while high - low > 1:
        middle = (low + high) // 2
        if share_at(node, row, rec, middle, sense) < target:
            low = middle
        else:
            high = middle
    return high


def standing_charge(node: Node) -> int:
    total = 0
    for r in node.records():
        if r.gap:
            total += at0(gram.charge(r.shape, r.lines))
    return total


def neutral(node: Node, row: Any, sense: int, near: int | None) -> tuple[int, int]:
    """Reading (b): the amplitude at which |W_standing + W_lay| is least (0 where an integer gives it); W_lay = sense A (A s div den) grows with A, so the amplitudes run upward from 1 until the lay's charge passes twice the standing's; among them the least |total|, the nearest to `near` on a tie."""
    standing = standing_charge(node)
    best = None
    a = 1
    while True:
        own = charge_of(node, row, a, sense)
        total = standing + own
        key = (abs(total), abs(a - (near if near is not None else a)))
        if best is None or key < best[0]:
            best = (key, a, total)
        if abs(own) > 2 * abs(standing) + 1 or a > 1 << 20:
            break
        a += 1
    return best[1], best[2]


def lay_plasma(node: Node, lay: dict[str, Any]) -> dict[str, Any]:
    row = node.by_index[int(lay["row"])]
    rec = node.records().index(row)
    sense = int(lay.get("sense", 1))
    node.start_content, node.start_x = node.content(), node.row(CARRIER).lines[0].now
    standing = standing_charge(node)
    if "amplitude" in lay:
        amplitude, how = int(lay["amplitude"]), "given"
    elif lay.get("neutral"):
        amplitude, _total = neutral(node, row, sense, lay.get("near"))
        how = "neutral"
    else:
        amplitude, how = fitted(node, row, rec, int(lay["quanta"]) * node.units[rec], sense), "fitted"
    lines = uniform_lines(node, row, amplitude, sense)
    node.lay(rec, Ellipsis, tuple(x for line in lines for x in (line.now, line.before)))
    found = {
        "event": "plasma",
        "row": int(lay["row"]),
        "sense": sense,
        "how": how,
        "amplitude": amplitude,
        "unit": node.units[rec],
        "share at the Node": share_at(node, row, rec, amplitude, sense),
        "levels (re_now, re_before, im_now, im_before)": [at0(lines[0].now), at0(lines[0].before), at0(lines[1].now), at0(lines[1].before)],
        "W of the lay": charge_of(node, row, amplitude, sense),
        "W standing before": standing,
        "W of the Node after": standing_charge(node),
    }
    node.log.append(found)
    return found


def node_state(node: Node) -> list[list[Any]]:
    """Every line's six integers at the Node (0, 0, 0): now, before, rem, wall, wr, wwall (None where the line has no write)."""
    found = []
    for line in node.all_lines():
        found.append([at0(line.now), at0(line.before), at0(line.rem), at0(line.wall), None if line.wr is None else at0(line.wr), None if line.wwall is None else int(line.wwall)])
    return found


def rows_table(node: Node) -> list[dict[str, Any]]:
    return [{"shape": r.shape, "gap": None if r.gap is None else str(r.gap), "pair_num": None if r.pair is None else str(r.pair[0]), "lines": r.shape, "K": gram.conjugation(r.shape), "is_record": r in node.records(), "is_gap0": r.shape == PLANE and r.gap == 0, "is_potential": r.shape == POTENTIAL, "is_carrier": r.shape == CARRIER, "is_walled": r.wall is not None} for r in node.rows_]


def diag(node: Node) -> dict[str, Any]:
    x = ints(node.row(CARRIER).lines[0].now)
    w_rows = [at0(gram.charge(r.shape, r.lines)) for r in node.records()]
    return {
        "i": node.interval,
        "X mean/min/max": [sum(x) // len(x), min(x), max(x)],
        "turned": int(node.turned.sum()),
        "W per record (Node 0)": w_rows,
        "W total (Node 0)": sum(w for w, r in zip(w_rows, node.records(), strict=True) if r.gap),
        "counts": dict(node.counts),
    }


def invariance(node: Node) -> dict[str, int]:
    held = total = 0
    for line in node.all_lines():
        for a in (line.now, line.before, line.rem, line.wr):
            if a is None or not np.ndim(a):
                continue
            total += 1
            ok = all(bool(np.all(np.asarray(a, dtype=object) == np.roll(a, 1, axis=axis))) for axis in range(AXES))
            held += 1 if ok else 0
    return {"arrays constant over the board": held, "of": total}


def cube48(node: Node) -> dict[str, int]:
    lines = node.all_lines()
    im = node.is_im()
    levels = [(a, i) for line, i in zip(lines, im, strict=True) for a in (line.now, line.before)]
    equal = apart = 0
    for perm in itertools.permutations(range(AXES)):
        for flips in itertools.product((False, True), repeat=AXES):
            ok = True
            for a, _is_im in levels:
                b = np.transpose(np.asarray(a, dtype=object), perm)
                for axis in range(AXES):
                    if flips[axis]:
                        b = np.flip(b, axis=axis)
                ok = ok and bool(np.all(b == a))
            equal += 1 if ok else 0
            apart += 0 if ok else 1
    return {"levels equal": equal, "apart": apart}


def main(argv: list[str]) -> None:
    sys.set_int_max_str_digits(0)
    where = Path(argv[1])
    world = json.loads(where.read_text(encoding="utf-8"))
    universe = json.loads(where.parent.joinpath(world["universe"]).read_text(encoding="utf-8"))
    plasma = [lay for lay in world.get("seed", []) if lay.get("lay") == "plasma"]
    stripped = dict(world, seed=[lay for lay in world.get("seed", []) if lay.get("lay") != "plasma"])
    universe, stripped = read_world(stripped, universe)
    back = int(argv[argv.index("back") + 1]) if "back" in argv else 0
    node = Node(universe, stripped)
    laid = [lay_plasma(node, lay) for lay in plasma]
    print(json.dumps({"laid": laid}), flush=True)
    intervals = int(stripped["intervals"])
    diags = [diag(node)]
    states = [node_state(node)]
    hashes: list[str] = []
    maxbits = node.census()[1]
    for t in range(intervals):
        if back and t >= intervals - back:
            hashes.append(node.state_hash())
        node.step()
        maxbits = max(maxbits, node.census()[1])
        diags.append(diag(node))
        states.append(node_state(node))
        if node.interval % 20 == 0 or node.turned.any():
            d = diags[-1]
            print(json.dumps({"i": d["i"], "X": d["X mean/min/max"], "turned": d["turned"], "W": d["W total (Node 0)"], "W rows": d["W per record (Node 0)"], "clicks": d["counts"]["body_clicks"], "laid": d["counts"]["laid"]}), flush=True)
    end48 = cube48(node)
    end_inv = invariance(node)
    kept_log = list(node.log)
    returned = run.run_back(node, hashes) if back else None
    n, _bits = node.census()
    summary = {"run back": returned, "counts": {k: int(v) for k, v in node.counts.items()}, "integers": n, "max bits": maxbits, "max transient bits": node.max_transient, "48": end48, "invariance at the end": end_inv, "turns": node.turns}
    print(json.dumps(summary), flush=True)
    out = {"world": world, "gamma": node.gamma, "T": node.T, "den": str(node.den), "cube": node.cube, "intervals": intervals, "rows": rows_table(node), "laid": laid, "summary": summary, "diag": diags, "states": states, "log": kept_log}
    Path(argv[2]).write_text(json.dumps(out), encoding="utf-8")


if __name__ == "__main__":
    main(sys.argv)
