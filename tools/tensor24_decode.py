"""The decoder's tool (Animate's): one record of the schema read, with its ledger beside it where one is named, and its
readings printed: the ledger read or the cause it is not, and the basic part on the click lines, each with its edge
sides in its site and across a Mesh: the lines listed in the schema's order and
counted per train and per Node-clock (the lines, the given, the taken and the net),
and the places (a round and a Node-clock) whose across net, their sum of q over the trains, is not 0, counted; then the click world's
block (decoder/shadow.py, the owner's law of 23:4x UTC: the physics read in the board's shadow, no claim on a board
reading alone): the edges' consistency check, a code check that holds by construction, read HOLDS and never
SHOWN, and the cone check by click, then the click board's two (the owner's word of 00:3x UTC: the clocks'
meetings), the meetings and each clock's line of meetings, each read SHOWN, or NOT SHOWN, or NOT READ, or NO CLICK
where the record holds no click line, with its cause, every train card's lines, given, taken and net beside the
consistency check, every clock's meetings counted with no duration and its books beside its line, and one refusal
line where the record holds no click line. Nothing is raised: a record or a
ledger that is not read is named with its cause. The interpreter's bound on a whole number's digits is lifted, since
the schema's numbers are whole numbers of any width.

Usage: python -I tools/tensor24_decode.py <record .jsonl> [<ledger .jsonl>]
"""

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.joinpath("src")))

from tensor24.decoder import clicks, records, shadow  # noqa: E402

# the claims of physics the record carries no click line for, refused by name (a constant of the tool's text, no reading)
REFUSAL = (
    "the record holds no click line, so no claim of physics is shown on it: light's speed, the well and its deeper"
    " clock, gamma and the books' form, the clock's beat and light on matter are not in the click world"
)


def printed(held: clicks.Counted) -> None:
    """The click lines listed, then counted per train and per Node-clock, then the places whose across net is not 0, their sum of q over the trains, the sides in their site cancelling there: a count, no reading of the books."""
    print(f"the click lines: {len(held.lines)}")
    for line in held.lines:
        where = f"round {line['round']}, site {line['site']}, train {line.get('train')}"
        carry = f"sides {line.get('sides', [])}, across {line.get('across', [])}"
        print(f"  {where}: q {line.get('q')}, {carry}")
    for name, tallies in (("train", held.trains), ("site", held.sites)):
        for at, tally in tallies.items():
            print(
                f"{name} {at}: {tally.lines} lines, given {tally.given}, taken {tally.taken}, net {tally.net}"
            )
    print(
        "each place's across net, its sum of q over the trains (its own site's sides cancel there):"
        f" {held.netted} of {held.places} places pass a net across a Mesh"
    )


def world(record: records.Record) -> None:
    """The click world's block: shadow's two, the edges' consistency check and the cone, and the click board's two, each with its kind and cause, every train card's counts under the consistency check (the Node-clocks' stand in the listing above), every clock's under its line of meetings, and the refusal line where the record holds no click line."""
    print("the click world (the owner's law of 23:4x UTC):")
    labels = {t.get("index"): t.get("label") for t in record.header.get("trains", [])}
    for name, verdict in (shadow.shadow(record) | shadow.click_board(record)).items():
        print(f"  {name}: {verdict['kind']}: {verdict['cause']}")
        for at, tally in verdict.get("trains", {}).items():
            print(
                f"    train {at} ({labels.get(at)}): {tally.lines} lines, given {tally.given}, taken {tally.taken},"
                f" net {tally.net}"
            )
        for (site, train), (met, tally) in verdict.get("clocks", {}).items():
            print(
                f"    clock at site {site}, train {train} ({labels.get(train)}): {met} meetings, {shadow.ORDER};"
                f" given {tally.given}, taken {tally.taken}, net {tally.net}"
            )
    if not clicks.listed(record):
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
    print(f"the ledger: {why if ledger is None else f'read, {len(ledger)} lines'}")
    printed(clicks.counted(record))
    world(record)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
