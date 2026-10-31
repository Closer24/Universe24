"""The decoder's tool (Animate's): one record of the schema read, with its ledger beside it where one is named, and its
readings printed: row 15's verdict with its two readings, row 46's with its two, the ledger read or the cause it is
not, the measurement's rules (the cone check by click and the twin reading), and the basic part on schema 1.3's click
lines: the lines listed in the schema's order and counted per train and per Node-clock (the lines, the given, the
taken and the net), and the places (a round and a Node-clock) where the sum of q over the trains is not 0, counted;
then the click world's block (decoder/shadow.py, the owner's law of 23:4x UTC: the physics read in the board's shadow,
no claim on a board reading alone): the books at each click, D6 and D7, and the cone check by click, each read SHOWN,
or NOT SHOWN, or NOT READ, or NO CLICK where the record holds no click line, with its cause, every train card's lines,
given, taken and net beside the books, and one refusal line where the record holds no click line.
Nothing is raised: a record or a ledger that is not read is named with its cause, and the rows that need it read NOT
READ. The interpreter's bound on a whole number's digits is lifted, since the schema's numbers are whole numbers of
any width.

Usage: python -I tools/tensor24_decode.py <record .jsonl> [<ledger .jsonl>]
"""

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from tensor24.decoder import bangs, books, clicks, measure, records, shadow  # noqa: E402

# the claims of physics the record carries no click line for, refused by name (a constant of the tool's text, no reading)
REFUSAL = (
    "the record holds no click line, so no claim of physics is shown on it: light's speed, the well and its deeper"
    " clock, gamma and the books' form, the clock's beat and light on matter are not in the click world"
)


def printed(held: clicks.Counted) -> None:
    """The click lines listed, then counted per train and per Node-clock, then the places with a sum of q not 0."""
    print(f"the click lines: {len(held.lines)}")
    for line in held.lines:
        where = f"round {line['round']}, site {line['site']}, train {line.get('train')}"
        print(f"  {where}: q {line.get('q')}, tooth {line.get('tooth')}")
    for name, tallies in (("train", held.trains), ("site", held.sites)):
        for at, tally in tallies.items():
            print(
                f"{name} {at}: {tally.lines} lines, given {tally.given}, taken {tally.taken}, net {tally.net}"
            )
    print(
        "the sum of q over the trains at a round and site:"
        f" not 0 at {held.nonzero} of {held.places} places"
    )


def world(record: records.Record) -> None:
    """The click world's block: the four verdicts with their causes, every train card's counts under the books (the Node-clocks' stand in the listing above), and the refusal line where the record holds no click line."""
    print("the click world (the owner's law of 23:4x UTC):")
    labels = {t.get("index"): t.get("label") for t in record.header.get("trains", [])}
    held = shadow.shadow(record)
    for name, verdict in held.items():
        print(f"  {name}: {verdict['kind']}: {verdict['cause']}")
        for at, tally in verdict.get("trains", {}).items():
            print(
                f"    train {at} ({labels.get(at)}): {tally.lines} lines, given {tally.given}, taken {tally.taken},"
                f" net {tally.net}"
            )
    if held[shadow.BOOKS]["kind"] == shadow.ABSENT:
        print(f"  {REFUSAL}")


def main(argv: list[str]) -> int:
    """Read the record and its ledger, print the readings and the click lines, and return 0; a usage error is argparse's."""
    parser = argparse.ArgumentParser(
        prog="tensor24_decode.py", description="Tensor24's decoder: one record read."
    )
    parser.add_argument("record")
    parser.add_argument("ledger", nargs="?")
    held = parser.parse_args(argv[1:])
    sys.set_int_max_str_digits(0)
    record, cause = records.read(held.record)
    if record is None:
        print(f"not read: {cause}")
        return 0
    ledger, why = records.read_ledger(held.ledger) if held.ledger else (None, "the ledger is absent")
    print(f"row 15: {books.row_15(record, ledger, why)}")
    print(f"row 46: {bangs.row_46(record, ledger, why)}")
    print(f"the ledger: {why if ledger is None else f'read, {len(ledger)} lines'}")
    print(f"the cone check (D8): {measure.cone_check(record)}")
    print(f"the twin reading (D6): {measure.twins(record)}")
    printed(clicks.counted(record))
    world(record)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
