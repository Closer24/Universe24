"""The decoder's first slice, read on the committed records (Animate): each head record in examples/records is written in
the schema 1.0 by tools/tensor24_convert.py, read back by src/tensor24/decoder under the schema's rules, counted by line
kind against the head's own counts, read for row 15 beside the head reader's verdict, and its whole clicks' ticks read
from the rate lines against the head's own proper time. The head's step moving the wind, a reading of its own (the
step's change) and no longer row 15's, is read from the ledger's consecutive rounds. Run from the tree's root:
python -I <this file> <scratch folder>.
"""

import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))
sys.path[:0] = [os.path.join(ROOT, "src"), os.path.join(ROOT, "tools")]

from tensor24_convert import converted, ledger, write  # noqa: E402

from tensor24.decoder import books, clocks, records  # noqa: E402

NAMES = ("bodies", "chiral", "hole")
ROW = "15 conservation at the click"


def head_reading(name):
    with open(os.path.join(ROOT, "examples", "records", f"{name}.reading.jsonl")) as f:
        for text in f:
            line = json.loads(text)
            if ROW in line:
                return line[ROW]
    return None


def step_moves(record, lines):
    """The step's change: per round with no whole click and no books, whether the wind over every train moved."""
    totals = {}
    for line in lines:
        totals[line["round"]] = totals.get(line["round"], 0) + line["wind"]
    clicked = {e["round"] for e in record.events if e["kind"] in ("whole", "books")}
    rounds = sorted(totals)
    quiet = [now for now in rounds[1:] if now not in clicked]
    moved = [
        now
        for before, now in zip(rounds, rounds[1:], strict=False)
        if now not in clicked and totals[now] != totals[before]
    ]
    return len(moved), len(quiet)


def main():
    scratch = sys.argv[1]
    for name in NAMES:
        with open(os.path.join(ROOT, "examples", "records", f"{name}.json")) as f:
            head = json.load(f)
        target = os.path.join(scratch, f"{name}.v1.jsonl")
        write(converted(head, "head"), target)
        record, cause = records.read(target)
        if record is None:
            print(f"{name}: not read: {cause}")
            continue
        log = head["log"]
        kinds = {k: len(record.of(k)) for k in records.KINDS}
        print(f"{name}: {len(record.events)} events after the header; by kind {kinds}")
        print(
            f"  the head's log: {sum(e['event'] == 'credit' for e in log)} credits and "
            f"{sum(e['event'] == 'birth' for e in log)} births (whole clicks), "
            f"{sum(len(e['booked']) for e in log if e['event'] == 'books')} books entries, "
            f"{sum(len(n['turned']) for n in head['nodes'])} turnovers in its nodes"
        )
        print(f"  the end: {record.end}")
        lines = ledger(head)
        verdict = books.row_15(record, lines)
        print(
            f"  row 15, the new decoder: {verdict['kind']}: {verdict['cause']}; its first reading {verdict['first']}"
        )
        old = head_reading(name)
        print(f"  row 15, the head's reader: {old['kind']}: {old['verdict']}")
        full = head["universe"]["integers"]["node_clock"]
        side = head["cube"]
        own = {}
        for e in log:
            if e["event"] in ("credit", "birth"):
                x, y, z = e["node"]
                own[(e["i"], (x * side + y) * side + z)] = e["proper"] // full
        stretches = clocks.stretches(record)
        same = sum(
            clocks.ticks_to(stretches[c["site"]], c["count"]) == own[(c["round"], c["site"])]
            for c in record.of("whole")
        )
        print(
            f"  the ticks at the whole clicks, from the rate lines: {same} of {len(record.of('whole'))} the head's own (proper by the full rate), click by click"
        )
        moved, quiet = step_moves(record, lines)
        print(
            f"  the step's change (a reading of its own): the wind over every train moved on {moved} of {quiet} rounds with no click"
        )


if __name__ == "__main__":
    main()
