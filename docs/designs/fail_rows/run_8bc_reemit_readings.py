"""The readings of RUN_8BC.md section 6.3 (the FAIL Runner B, 2026-09-23,
STEP 3b): the runs of `j2_reemit.json` and `j2_reemit_control.json` read
against the pins B0 to B4 and C1 to C3 of section 6.2 as written before
the runs, every number with its kind; the books' line first (the
admissibility gate of the reviewer's line (i)). DETECTOR: the readers' and
the far detector's `events` and `pass` lines, the re-emitter's `gather`
lines (its completions) and `split` lines with `rebirth` (its rebirths).
GAMEBOARD: the lamp's `birth` lines, the books, the `phase - u` of the
pass lines (the row's columns on the reader's line), the re-emitter's
`held`. No pin is moved: a differing integer prints FAIL beside the pin.

    PYTHONPATH=src .venv/bin/python docs/designs/fail_rows/run_8bc_reemit_readings.py artifacts/fail_rows/j2_reemit artifacts/fail_rows/j2_reemit_control
"""

from __future__ import annotations

import collections
import json
import sys
from pathlib import Path

MODULUS = 64
R, FIRST, SECOND, FAR = 4, 8, 9, 190
# The pins of section 6.2 as written: (clicks, arrivals) per reader, the far detector's clicks and arrivals,
# the re-emitter's completions and rebirths, the classes, the phase - u form at x = 8.
PINS = {
    "beam-fail-rows-j2_reemit-v1": {
        "B0": (1031, 1031),
        "B1": (16, 1024, 46),
        "B2": (16, 1007, 59),
        "B3": (683, 705),
        "B4": 46,
    },
    "beam-fail-rows-j2_reemit_control-v1": {
        "B0": (1031, 1031),
        "C1": (0, 1024),
        "C2": (0, 1023),
        "C3": (705, 705),
    },
}


def read(folder: Path) -> None:
    record = json.loads((folder / "run.json").read_text(encoding="utf-8"))
    model = str(record["model"])
    pins = PINS[model]
    measured = record["measured"]
    by_x = {int(m["position"][0]): m for m in measured}
    number_of = {int(m["number"]): int(m["position"][0]) for m in measured}
    births = 0
    gathers_at: collections.Counter[str] = collections.Counter()
    splits: list[dict[str, object]] = []
    passes: dict[int, list[dict[str, object]]] = collections.defaultdict(list)
    clicks: dict[int, list[dict[str, object]]] = collections.defaultdict(list)
    reemit_gather_content: collections.Counter[tuple[int, str]] = collections.Counter()
    with (folder / "events.jsonl").open(encoding="utf-8") as stream:
        for text in stream:
            event = json.loads(text)
            kind = event["event"]
            if kind == "birth":
                births += 1
            elif kind == "gather":
                chosen = event["chosen"]
                name = str(chosen[0][0]) if isinstance(chosen, list) and chosen else str(chosen)
                gathers_at[name] += 1
                if name == "reemit":
                    reemit_gather_content[(int(event["content"]), json.dumps(event["momentum"]))] += 1
            elif kind == "split" and int(event["node"][0]) == R:
                splits.append(event)
            elif kind == "pass" and event.get("measured") is not None:
                passes[number_of[int(event["measured"])]].append(event)
            elif kind == "click" and event.get("measured") is not None:
                clicks[number_of[int(event["measured"])]].append(event)
    print(
        f"THE RUN {model}: status {record['status']}, {record['completed_ticks']} intervals; source sha256 "
        f"{record['source_sha256'][:16]}, world sha256 {record['initialization_sha256'][:16]}; the engine's own elapsed "
        f"{record['elapsed_seconds']:.2f} s (HOST)"
    )
    balanced = bool(record["conserved_at_every_completed_tick"])
    print(
        f"  THE BOOKS FIRST (GAMEBOARD, the admissibility gate): balanced at every completed tick: {balanced}; "
        f"the re-emitter's `held` at the end {by_x[R]['held']} (the placed quantum carried on by the rebirth, none kept), "
        f"the re-emitter's own `events` {by_x[R]['events']}; the `gather` lines at reemit carry (content, momentum) "
        f"{dict(reemit_gather_content)}"
    )
    print(
        f"  the lamp's births (GAMEBOARD): {births} over {record['completed_ticks']} intervals (one per interval, none skipped: "
        f"{'PASS' if births == record['completed_ticks'] else 'FAIL'})"
    )
    verdicts = []
    # B0
    completions = gathers_at["reemit"]
    rebirths = sum(1 for s in splits if s.get("rebirth"))
    plain = sum(1 for s in splits if not s.get("rebirth"))
    us = sorted({int(s["u"]) for s in splits})
    ok = (completions, rebirths) == pins["B0"] and plain == 0
    verdicts.append(("B0", "PASS" if ok else "FAIL"))
    print(
        f"  B0 the re-emitter: {completions} completions (`gather` lines chosen 'reemit'), {rebirths} `split` lines with "
        f"`rebirth` and {plain} without; the rebirths' u: {len(us)} values {us[:6]}..{us[-3:]} (DETECTOR); "
        f"pinned {pins['B0']}: {'PASS' if ok else 'FAIL'}"
    )

    def counts(x: int) -> tuple[int, int]:
        n_clicks = int(by_x[x]["events"][0])
        assert n_clicks == len(clicks.get(x, []))
        return n_clicks, n_clicks + len(passes.get(x, []))

    for pin, x in (("B1", FIRST), ("B2", SECOND), ("C1", FIRST), ("C2", SECOND)):
        if pin not in pins:
            continue
        n_clicks, n_arrivals = counts(x)
        want = pins[pin]
        ok = (n_clicks, n_arrivals) == (want[0], want[1])
        line = f"  {pin} the reader at x = {x}: {n_clicks} clicks of {n_arrivals} arrivals (DETECTOR), pinned {want[0]} of {want[1]}"
        if len(want) == 3:
            # The class: the admitted rows' birth ordinal j mod 64, read off the lamp's record identity (the ordinal is the
            # low 32 bits of the record the reborn record replaced; the pass and click lines carry the reborn record's u = 2 k,
            # so the class is read as the click lines' u = 2 j mod 64: the set of u values of the clicks).
            u_clicked = sorted({int(c["u"]) for c in clicks[x]})
            expect_u = sorted({(2 * j) % MODULUS for j in range(want[2], 1024, MODULUS)})
            ok = ok and u_clicked == expect_u
            line += f"; the clicked rows' u {u_clicked} (the class j = {want[2]} mod 64 carries u = 2 j mod 64 = {expect_u})"
        verdicts.append((pin, "PASS" if ok else "FAIL"))
        print(line + f": {'PASS' if ok else 'FAIL'}")
    far_pin = pins.get("B3") or pins.get("C3")
    far_name = "B3" if "B3" in pins else "C3"
    n_clicks, n_arrivals = counts(FAR)
    # The pin's second number is the flight table's count of births that would reach x = 190 within the run
    # (GAMEBOARD, section 6.2); the far detector's own arrivals are its clicks plus its passes (DETECTOR). The two
    # meet through the rows taken before it: the taken rows' birth ordinals k (the reborn record's low 32 bits less
    # one, k = j) at or below that count - 1.
    reach = far_pin[1]
    taken_before = sum(
        1
        for x in (FIRST, SECOND)
        for c in clicks.get(x, [])
        if (int(c["record"]) & 0xFFFFFFFF) - 1 < reach
    )
    ok = n_clicks == far_pin[0] and n_arrivals == n_clicks and n_clicks + taken_before == reach
    verdicts.append((far_name, "PASS" if ok else "FAIL"))
    print(
        f"  {far_name} the far detector at x = {FAR}: {n_clicks} clicks of {n_arrivals} arrivals, {len(passes.get(FAR, []))} passes "
        f"(DETECTOR), pinned {far_pin[0]} clicks; the births that reach x = {FAR} within the run {reach} (GAMEBOARD, the flight "
        f"table) less the {taken_before} taken before it among those births = {reach - taken_before}: {'PASS' if ok else 'FAIL'}"
    )
    # B4 / the control's phase - u.
    dist = collections.Counter(
        (int(p["phase"]) - int(p["u"])) % MODULUS for p in passes[FIRST] + clicks[FIRST]
    )
    if "B4" in pins:
        ok = (
            len(dist) == MODULUS
            and set(dist.values()) == {16}
            and all((int(c["phase"]) - int(c["u"])) % MODULUS == 0 for c in clicks[FIRST])
        )
        verdicts.append(("B4", "PASS" if ok else "FAIL"))
        print(
            f"  B4 the lines at x = {FIRST}: `phase - u` takes {len(dist)} values, {min(dist.values())} to {max(dist.values())} rows each, "
            f"the clicked rows all at 0 (GAMEBOARD, the row's columns): {'PASS' if ok else 'FAIL'}"
        )
    else:
        print(
            f"  the lines at x = {FIRST} (the control): `phase - u` {dict(dist)} (GAMEBOARD): the plane wave, one value"
        )
    print("  THE VERDICTS against the pins as written: " + ", ".join(f"{p} {v}" for p, v in verdicts))


def main() -> None:
    for folder in sys.argv[1:]:
        read(Path(folder))


if __name__ == "__main__":
    main()
