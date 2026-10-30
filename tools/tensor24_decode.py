"""The decoder's tool (Animate's): one record of the schema read, with its ledger beside it where one is named, and its
readings printed: row 15's verdict with its two readings, row 46's with its two, the ledger read or the cause it is
not, the measurement's rules (the cone check by click and the twin reading), and the basic part on schema 1.3's click
lines: the lines listed in the schema's order and counted per train and per Node-clock (the lines, the given, the
taken and the net), and the places (a round and a Node-clock) where the sum of q over the trains is not 0, counted;
no verdict stands on the click lines until the clicks are closed (the owner's word).
Nothing is raised: a record or a ledger that is not read is named with its cause, and the rows that need it read NOT
READ. The interpreter's bound on a whole number's digits is lifted, since the schema's numbers are whole numbers of
any width.

Usage: python -I tools/tensor24_decode.py <record .jsonl> [<ledger .jsonl>]
"""

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from tensor24.decoder import bangs, books, clicks, measure, records  # noqa: E402


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
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
