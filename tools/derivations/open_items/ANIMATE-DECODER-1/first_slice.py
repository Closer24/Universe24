"""The decoder's first slice, read on the committed records (Animate): each head record in examples/records is written in
the schema by tools/tensor24_convert.py, read back by records.py with the schema's rules, counted by line kind against
the head's own counts, and read for row 15's first reading by books.py, beside the head reader's verdict for the row
(examples/records/<name>.reading.jsonl). Run from the tree's root: python -I <this file> <scratch folder>.
"""

import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))
sys.path[:0] = [HERE, os.path.join(ROOT, "tools")]

from books import row_15  # noqa: E402
from records import read  # noqa: E402
from tensor24_convert import converted, ledger  # noqa: E402

NAMES = ("bodies", "chiral", "hole")
ROW = "15 conservation at the click"


def head_reading(name):
    with open(os.path.join(ROOT, "examples", "records", f"{name}.reading.jsonl")) as f:
        for text in f:
            line = json.loads(text)
            if ROW in line:
                return line[ROW]
    return None


def main():
    scratch = sys.argv[1]
    for name in NAMES:
        with open(os.path.join(ROOT, "examples", "records", f"{name}.json")) as f:
            head = json.load(f)
        target = os.path.join(scratch, f"{name}.v1.jsonl")
        with open(target, "w") as f:
            for line in converted(head, "head"):
                f.write(json.dumps(line, separators=(",", ":")) + "\n")
        record, cause = read(target)
        if record is None:
            print(f"{name}: not read: {cause}")
            continue
        log = head["log"]
        kinds = {k: len(record.of(k)) for k in ("whole", "books", "turnover", "rate")}
        print(f"{name}: {len(record.events)} events after the header; by kind {kinds}")
        print(
            f"  the head's log: {sum(e['event'] == 'credit' for e in log)} credits and "
            f"{sum(e['event'] == 'birth' for e in log)} births (whole clicks), "
            f"{sum(len(e['booked']) for e in log if e['event'] == 'books')} books entries, "
            f"{sum(len(n['turned']) for n in head['nodes'])} turnovers in its nodes; the counts' turns {head['counts']['turns']}"
        )
        print(f"  the end: {record.end}")
        verdict = row_15(record, ledger(head))
        old = head_reading(name)
        print(f"  row 15, the new decoder: {verdict['kind']}: {verdict['cause']}")
        print(f"    its first reading: {verdict['first']}")
        if "second" in verdict:
            print(f"    its second reading: {verdict['second']}")
        print(f"  row 15, the head's reader: {old['kind']}: {old['verdict']}")


if __name__ == "__main__":
    main()
