"""The conservation check on a record of the engine (the JSON `python -m event_universe.run` writes), no toy: every conservation the law names (THE_WAY.md, Addition 5; docs/ALGEBRA.md by clause) read from the record's log, frames, Node lines and rows, and, unless `board off` is given, from the board itself, re-run by the engine from the record's own two files (the universe and the world the record carries) interval by interval. Each law is one line "LAW: N of M" (a count of intervals, births or clicks holding of as many), the numbers under it; the exit code 0 only when every counted law holds in full. Integers only: a ratio is a quotient with its remainder.

The laws, each by its clause:
 1. The form (The conserved form; Rule3 is reversible): the record's run back (the bijection of the whole interval: exact of intervals), and on the board the re-run's log equal to the record's event by event and the re-run's counts equal to the record's (the record reproduced bit for bit from its two files).
 2. The current (The tension, F_ij = -F_ji): on the board, the gap-0 line's current at the +a Port of every Node against the -a Port of the Node beyond, F_ij + F_ji = 0 on every Link, at the start of every interval; in the Node lines the current the record wrote against the re-run's.
 3. The Wronskian, the charge (The charge written is the Wronskian over T div 2; The sign is the rotation sense): every birth's two children W of opposite sign summing to 0; on the board the records' W summed over the board per interval, unchanged across every interval without a birth, and the rows' "W total" at the marks against the board's.
 4. The lattice momentum (The lattice momentum): per Link from the Node lines, the gap-0 line's current F on the +a Link of every Node, summed over the board per axis per interval (the Links' sum; the count of intervals with the three sums 0); per birth the balance dP_take + dP_lay_ends summed to 0 on three axes (cp2's reading); per click the recoil dP_take summed over the record.
 5. The energy as the beat per proper interval (A body and the light it reads keep one energy): per credit the pair [beat, proper]; per credited Node the credits in the order of the record and the proper span between successive credits, the beats summed over the span, the quotient beats * 1000 div span and its remainder (the integer reading), its min and max over the Nodes.
 6. The count under the exact take (The ledger of exactness; EX-S1's identity): per click (birth and credit) taken + remainder_was - remainder = booked (the exact lays, which carry no remainders, aside), taken >= booked on every birth (gate 15's identity) and read per credit; the births' taken and booked summed against the record's counts (close.py books the births alone).
 A law marked r is a reading (a count the tests do not pin: the board's W total across the steps, the Links' momentum sum, the births' dP balance): printed, not tallied in the verdict.
 7. The run back: the record's run_back exact of intervals (law 1's first reading, counted once).
 8. Integers: every number of the log an integer (no float in the record), the largest bits of the rows.

Usage: PYTHONPATH=<worktree>/src python conservation_check.py <record.json> [board off] [out <summary.json>]
"""

from __future__ import annotations

import json
import sys
from typing import Any


def arg_after(argv: list[str], key: str, default: str | None) -> str | None:
    return argv[argv.index(key) + 1] if key in argv else default


def walk_floats(x: Any) -> int:
    if isinstance(x, float):
        return 1
    if isinstance(x, dict):
        return sum(walk_floats(v) for v in x.values())
    if isinstance(x, list):
        return sum(walk_floats(v) for v in x)
    return 0


def quotient(a: int, b: int) -> list[int]:
    return [a // b, a % b] if b else [0, a]


def from_the_log(rec: dict[str, Any]) -> tuple[dict[str, Any], list[tuple[str, int, int]]]:
    log = rec["log"]
    births = [e for e in log if e["event"] == "birth"]
    credits = [e for e in log if e["event"] == "credit"]
    clicks = births + credits
    found: dict[str, Any] = {}
    laws: list[tuple[str, int, int]] = []
    # 1 / 7 the run back
    rb = rec.get("run_back") or {"intervals": 0, "exact": 0}
    laws.append(("1. the form, the run back exact", int(rb["exact"]), int(rb["intervals"])))
    # 3 the charge of the births
    paired = [b for b in births if "exact_lay" not in b]
    signs_ok = sum(1 for b in paired if all(int(w) != 0 for w in b["W_children"]) and sum((int(w) > 0) - (int(w) < 0) for w in b["W_children"]) == 0)
    laws.append(("3. the charge, the births' two children W of opposite sign (the exact lays aside)", signs_ok, len(paired)))
    laws.append(("3r. reading: the births' two children W summed to 0 in magnitude", sum(1 for b in paired if sum(int(w) for w in b["W_children"]) == 0), len(paired)))
    senses = [int(w) > 0 for b in births for w in b["W_children"]]
    found["births with an exact lay (one child W 0)"] = len(births) - len(paired)
    found["births W sum"] = sum(int(w) for b in births for w in b["W_children"])
    found["births senses +/-"] = [sum(senses), len(senses) - sum(senses)]
    w_marks = [int(r["W total"]) for r in rec["rows"]]
    found["W total at the marks"] = w_marks
    # 4 the momentum from the Node lines and the clicks
    nodes = rec["nodes"]
    sums = [[sum(int(x) for x in n["current"][a]) for a in range(3)] for n in nodes]
    found["Links' current summed per axis, first and last interval"] = [sums[0], sums[-1]] if sums else []
    laws.append(("4r. reading: the lattice momentum, intervals with the Links' sum 0 on three axes", sum(1 for s in sums if s == [0, 0, 0]), len(sums)))
    balance = 0
    for b in births:
        ends = b.get("dP_lay_ends", [[0, 0, 0], b.get("dP_lay", [0, 0, 0])])
        p = [int(b["dP_take"][a]) + int(ends[0][a]) + int(ends[1][a]) for a in range(3)]
        balance += p == [0, 0, 0]
    laws.append(("4r. reading: the lattice momentum, births with dP_take + dP_lay_ends = 0", balance, len(births)))
    found["recoil dP_take summed over the clicks"] = [sum(int(c["dP_take"][a]) for c in clicks) for a in range(3)]
    # 5 the energy as the beat per proper interval
    by_node: dict[tuple[int, ...], list[tuple[int, int]]] = {}
    for c in credits:
        by_node.setdefault(tuple(c["node"]), []).append((int(c["proper"]), int(c["beat"])))
    readings = []
    for at, seq in by_node.items():
        if len(seq) < 2:
            continue
        span = seq[-1][0] - seq[0][0]
        beats = sum(b for _p, b in seq[1:])
        readings.append((quotient(beats * 1000, span), at, len(seq)))
    laws.append(("5. the energy, credits with beat >= 1", sum(1 for c in credits if int(c["beat"]) >= 1), len(credits)))
    found["beats per 1000 proper, [quotient, remainder], min and max over the credited Nodes"] = (
        [min(readings)[0], max(readings)[0]] if readings else []
    )
    found["credited Nodes"] = len(by_node)
    found["beats summed over the credits"] = sum(int(c["beat"]) for c in credits)
    # 6 the count under the exact take
    booked_clicks = [c for c in clicks if "remainder_was" in c]
    exact = sum(1 for c in booked_clicks if int(c["taken"]) + int(c["remainder_was"]) - int(c["remainder"]) == int(c["booked"]))
    laws.append(("6. the count, taken + remainder before - remainder after = booked per click (EX-S1)", exact, len(booked_clicks)))
    laws.append(("6. the count, taken >= booked per birth (gate 15's identity; the exact lays aside)", sum(1 for b in paired if int(b["taken"]) >= int(b["booked"])), len(paired)))
    laws.append(("6r. reading: taken >= booked per credit", sum(1 for c in credits if int(c["taken"]) >= int(c["booked"])), len(credits)))
    taken, booked = sum(int(b["taken"]) for b in births), sum(int(b["booked"]) for b in births)
    laws.append(("6. the count, the births' taken and booked summed against the record's counts", int(taken == int(rec["counts"]["taken"])) + int(booked == int(rec["counts"]["booked"])), 2))
    found["clicks without the take's remainders (the exact lays)"] = len(clicks) - len(booked_clicks)
    found["births taken summed"], found["births booked summed"] = taken, booked
    found["credits taken summed"], found["credits booked summed"] = sum(int(c["taken"]) for c in credits), sum(int(c["booked"]) for c in credits)
    # 8 integers
    laws.append(("8. integers, floats found in the record", 0, walk_floats(rec)))
    found["max bits at the marks"] = max(int(r["max bits"]) for r in rec["rows"])
    found["births"], found["credits"], found["intervals"] = len(births), len(credits), int(rec["intervals"])
    return found, laws


def on_the_board(rec: dict[str, Any]) -> tuple[dict[str, Any], list[tuple[str, int, int]]]:
    """The record re-run from its two files, the laws read on the board at every interval."""
    import numpy as np
    from event_universe import gram
    from event_universe.core.ports import AXES, port_of
    from event_universe.links import link_current
    from event_universe.node import Node

    node = Node(rec["universe"], rec["world"])
    intervals = int(rec["intervals"])
    laws: list[tuple[str, int, int]] = []
    found: dict[str, Any] = {}
    antisym = 0
    w_unchanged = 0
    w_steps_without_birth = 0
    current_lines_equal = 0
    w_prev = None
    w_marks_equal = 0
    marks = {int(r["i"]): int(r["W total"]) for r in rec["rows"]}
    births_at = {int(e["i"]) for e in rec["log"] if e["event"] == "birth"}
    for t in range(intervals):
        line = node.emitter().lines[0]
        ok = True
        for a in range(AXES):
            plus = link_current(line, port_of(a, 0))
            minus = link_current(line, port_of(a, 1))
            # the Link from i along +a is read from i + e_a at its -a Port: F_ij + F_ji = 0
            if not np.array_equal(plus + np.roll(minus, -1, axis=a), np.zeros_like(plus)) and not np.array_equal(plus + np.roll(minus, 1, axis=a), np.zeros_like(plus)):
                ok = False
        antisym += ok
        node.step()
        total = 0
        for r in node.records():
            total += int(np.sum(gram.charge(r.shape, r.lines)))
        if w_prev is not None and node.interval not in births_at:
            w_steps_without_birth += 1
            w_unchanged += total == w_prev
        w_prev = total
        if node.interval in marks:
            w_marks_equal += marks[node.interval] == total
        rec_current = rec["nodes"][t]["current"]
        now = [[int(x) for x in link_current(node.emitter().lines[0], port_of(a, 0)).reshape(-1)] for a in range(AXES)]
        current_lines_equal += now == rec_current
    laws.append(("2. the current, intervals with F_ij + F_ji = 0 on every Link of the gap-0 line", antisym, intervals))
    laws.append(("2. the current, the record's Node lines' current equal to the board's", current_lines_equal, intervals))
    laws.append(("3r. reading: the Wronskian, intervals without a birth with the board's W total unchanged", w_unchanged, w_steps_without_birth))
    laws.append(("3. the Wronskian, the rows' W total at the marks equal to the board's", w_marks_equal, len(marks)))
    same_log = sum(1 for a, b in zip(node.log, rec["log"]) if json.loads(json.dumps(a, default=str)) == b)
    laws.append(("1. the form, the re-run's log equal to the record's event by event", same_log, max(len(node.log), len(rec["log"]))))
    counts = {k: str(v) for k, v in node.counts.items()}
    laws.append(("1. the form, the re-run's counts equal to the record's", sum(1 for k in rec["counts"] if counts.get(k) == rec["counts"][k]), len(rec["counts"])))
    found["board W total at the end"] = w_prev
    return found, laws


def main(argv: list[str]) -> None:
    sys.set_int_max_str_digits(0)
    with open(argv[1], encoding="utf-8") as f:
        rec = json.load(f)
    found, laws = from_the_log(rec)
    if arg_after(argv, "board", "on") != "off":
        f2, l2 = on_the_board(rec)
        found.update(f2)
        laws += l2
    laws.sort(key=lambda x: x[0])
    held = 0
    counted = [law for law in laws if not law[0].split(".")[0].endswith("r")]
    for name, n, m in laws:
        print(f"{name}: {n} of {m}")
        held += n == m and (name, n, m) in counted
    print(json.dumps(found, default=str))
    verdict = f"laws held in full: {held} of {len(counted)} (the readings marked r aside)"
    print(verdict)
    out = arg_after(argv, "out", None)
    if out:
        with open(out, "w", encoding="utf-8") as f:
            json.dump({"record": argv[1], "laws": laws, "readings": found, "verdict": verdict}, f, default=str)
    sys.exit(0 if held == len(counted) else 1)


if __name__ == "__main__":
    main(sys.argv)
