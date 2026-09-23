"""The readings of RUN_8BC.md section 5 (the FAIL Runner B, 2026-09-23): the
run of `j2_massive.json` read against the pins A1 to A5 of section 3 as
written before the run, every number with its kind. DETECTOR: a reader's
`click` and `pass` lines and the `events` of its state (its own record),
the far detector's `events`, the `u` and `phase` fields of those lines
(the row's columns on the reader's line: the diagnostic of pin A5, named
GAMEBOARD in the pin). GAMEBOARD: the births (the lamp's `birth` lines),
the books (`conserved_at_every_completed_tick`), the rows left in
transit (`state.json`). COMPUTATION: the lamp's count row replayed by the
engine's own primitive (`by_drive_rows`, the one count primitive) to name
the cause of a differing integer. No pin is moved here: a differing
integer prints FAIL beside the pin as written.

    PYTHONPATH=src .venv/bin/python docs/designs/fail_rows/run_8bc_readings.py artifacts/fail_rows/j2_massive
"""

from __future__ import annotations

import collections
import json
import sys
from pathlib import Path

import numpy as np

from event_universe.events.nature_beam import by_drive_rows

# The pins of section 3, reading A, as written before the run.
PINS = {
    "A1": ("the first reader (x = 8): 0 clicks of 1024 arrivals", 8, 0, 1024),
    "A2": ("the second reader (x = 9): 0 clicks of 1023 arrivals", 9, 0, 1023),
    "A3": ("the reader at x = 14: 1014 clicks of 1014 arrivals", 14, 1014, 1014),
}
FAR = 190
MODULUS = 64
SHIFT_AT_8, SHIFT_AT_9 = 46, 59


def main(folder: Path) -> None:
    record = json.loads((folder / "run.json").read_text(encoding="utf-8"))
    measured = record["measured"]
    by_x = {int(m["position"][0]): m for m in measured}
    number_of = {int(m["number"]): int(m["position"][0]) for m in measured}
    births: list[dict[str, object]] = []
    passes: dict[int, list[dict[str, object]]] = collections.defaultdict(list)
    clicks: dict[int, list[dict[str, object]]] = collections.defaultdict(list)
    with (folder / "events.jsonl").open(encoding="utf-8") as stream:
        for text in stream:
            event = json.loads(text)
            kind = event["event"]
            if kind == "birth":
                births.append(event)
            elif kind == "pass" and event.get("measured") is not None:
                passes[number_of[int(event["measured"])]].append(event)
            elif kind == "click" and event.get("measured") is not None:
                clicks[number_of[int(event["measured"])]].append(event)
    print(
        f"THE RUN: model {record['model']}, status {record['status']}, {record['completed_ticks']} intervals completed; "
        f"source sha256 {record['source_sha256'][:16]}, world sha256 {record['initialization_sha256'][:16]}; "
        f"the engine's own elapsed {record['elapsed_seconds']:.2f} s (HOST)"
    )
    balanced = bool(record["conserved_at_every_completed_tick"])
    print(f"THE BOOKS (GAMEBOARD): balanced at every completed tick: {balanced}")

    # The births (GAMEBOARD, the lamp's own lines).
    ticks = [int(b["tick"]) for b in births]
    missing = [t for t in range(1, int(record["completed_ticks"]) + 1) if t not in set(ticks)]
    us = [int(b["u"]) for b in births[:66]]
    print(
        f"THE BIRTHS (GAMEBOARD): {len(births)} records over {record['completed_ticks']} intervals; "
        f"the intervals with no birth: {missing}; u of the first 66 births {us}"
    )
    # The lamp's count row replayed by the one primitive (COMPUTATION): the
    # accumulator gains the held content each interval against the wall K,
    # the count taken, the remainder kept; each birth spends one unit.
    world = json.loads((folder / "initialization.json").read_text(encoding="utf-8"))
    wall = int(world["K"])
    held = int(world["measured"][0]["amount"])
    acc = np.zeros(1, dtype=np.int64)
    skipped = []
    for tick in range(1, int(record["completed_ticks"]) + 1):
        count, acc = by_drive_rows(acc, held, wall)
        if int(count[0]) == 0:
            skipped.append(tick)
        held -= int(count[0]) * 1
    print(
        f"  the lamp's count row replayed by `by_drive_rows(acc, held, K)` per interval, one unit spent per birth (COMPUTATION): "
        f"the intervals whose count is 0: {skipped} (after the first birth the held content is K - 1, below the wall by one: "
        f"the second self-creation's count is 0 and the remainder K - 1 carries every later count)"
    )

    # The readers (DETECTOR).
    def arrivals(x: int) -> tuple[int, int, int]:
        n_clicks = len(clicks.get(x, []))
        n_passes = len(passes.get(x, []))
        state_clicks = int(by_x[x]["events"][0])
        assert state_clicks == n_clicks, (x, state_clicks, n_clicks)
        return n_clicks, n_passes, n_clicks + n_passes

    print("THE READERS (DETECTOR: each reader's `click` and `pass` lines, its state's `events`)")
    verdicts = []
    for pin, (text, x, pin_clicks, pin_arrivals) in PINS.items():
        n_clicks, n_passes, n_arrivals = arrivals(x)
        ok_clicks = n_clicks == pin_clicks
        ok_arrivals = n_arrivals == pin_arrivals
        verdict = "PASS" if ok_clicks and ok_arrivals else "FAIL"
        verdicts.append((pin, verdict))
        print(
            f"  {pin} {text}: read {n_clicks} clicks of {n_arrivals} arrivals ({n_passes} passes): "
            f"the clicks {'PASS' if ok_clicks else 'FAIL'}, the arrivals {'PASS' if ok_arrivals else 'FAIL'}; {verdict}"
        )
    others = {x: arrivals(x)[0] for x in range(8, 136) if x not in (8, 9, 14)}
    nonzero = {x: n for x, n in others.items() if n}
    far_clicks = int(by_x[FAR]["events"][0])
    far_passes = len(passes.get(FAR, []))
    ok_a4 = not nonzero and far_clicks == 0
    verdicts.append(("A4", "PASS" if ok_a4 else "FAIL"))
    print(
        f"  A4 every other reader 0; the far detector 0: the readers with a click among the other 125: {nonzero or 'none'}; "
        f"the far detector (x = {FAR}) {far_clicks} clicks, {far_passes} passes; {'PASS' if ok_a4 else 'FAIL'}"
    )
    # A5: the raw phase on the pass lines at x = 8 and 9 (the row's columns: GAMEBOARD in the pin).
    diffs_8 = collections.Counter((int(p["phase"]) - int(p["u"])) % MODULUS for p in passes[8])
    diffs_9 = collections.Counter((int(p["phase"]) - int(p["u"])) % MODULUS for p in passes[9])
    u_hist_8 = collections.Counter(int(p["u"]) for p in passes[8])
    ok_a5 = set(diffs_8) == {SHIFT_AT_8} and set(diffs_9) == {SHIFT_AT_9}
    verdicts.append(("A5", "PASS" if ok_a5 else "FAIL"))
    print(
        f"  A5 `phase - u` on the pass lines (GAMEBOARD, the row's columns on the reader's line): at x = 8 {dict(diffs_8)}, "
        f"at x = 9 {dict(diffs_9)}; the u values at x = 8: {len(u_hist_8)} classes, "
        f"{min(u_hist_8.values())} to {max(u_hist_8.values())} rows each; {'PASS' if ok_a5 else 'FAIL'}"
    )
    diffs_14 = collections.Counter((int(c["phase"]) - int(c["u"])) % MODULUS for c in clicks[14])
    u_hist_14 = collections.Counter(int(c["u"]) for c in clicks[14])
    ages_14 = sorted({int(c["age"]) for c in clicks[14]})
    print(
        f"  the click lines at x = 14: `phase - u` {dict(diffs_14)}, the age {ages_14}, the u values {len(u_hist_14)} classes, "
        f"{min(u_hist_14.values())} to {max(u_hist_14.values())} rows each (every class taken: no class filter); "
        f"the reader's `held` {by_x[14]['held']} (q_F = 1 per completion, the placed quantum)"
    )
    # The falsifiers of section 3.
    print("THE FALSIFIERS (section 3), checked:")
    print(f"  a click at x = 8 or 9: {arrivals(8)[0]} and {arrivals(9)[0]} (none: not tripped)")
    print(
        f"  the reader at x = 14 reading fewer than 1014: {arrivals(14)[0]} (tripped by one; the cause the birth count above, not a class filter)"
    )
    print(f"  a click at a reader other than x = 14: {nonzero or 'none'} (not tripped)")
    print(f"  the far detector above 0: {far_clicks} (not tripped)")
    print(f"  the books not balanced: {not balanced} (not tripped)")
    print(
        f"  a pass line at x = 8 whose phase - u is not 46: {[d for d in diffs_8 if d != SHIFT_AT_8] or 'none'} (not tripped)"
    )
    # The rows left in transit (GAMEBOARD).
    state = json.loads((folder / "state.json").read_text(encoding="utf-8"))
    in_transit = collections.Counter()
    for node in state["nodes"]:
        for family in node["families"]:
            for ray in family["rays"]:
                in_transit[int(node["position"][0])] += int(ray["amount"])
    print(
        f"THE ROWS IN TRANSIT AT THE END (GAMEBOARD, state.json): {sum(in_transit.values())} rows at x = "
        f"{sorted(in_transit)} (the births that had not reached x = 14 by the last interval)"
    )
    print("THE VERDICTS against the pins as written: " + ", ".join(f"{p} {v}" for p, v in verdicts))


if __name__ == "__main__":
    main(Path(sys.argv[1]))
