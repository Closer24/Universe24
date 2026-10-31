"""The decoder's tool (Animate's): one record of the schema read, with its ledger beside it where one is named, and its
readings printed: the ledger read or the cause it is not, and the basic part on schema 1.3's click lines: the lines
listed in the schema's order and counted per train and per Node-clock (the lines, the given, the taken and the net),
and the places (a round and a Node-clock) where the sum of q over the trains is not 0, counted; then the click world's
block (decoder/shadow.py, the owner's law of 23:4x UTC: the physics read in the board's shadow, no claim on a board
reading alone): the books at each click, D6 and D7, and the cone check by click, then the click board's three (the
owner's word of 00:3x UTC: the clocks' meetings), the meetings, each clock's line of meetings and light's echo, each
read SHOWN, or NOT SHOWN, or NOT READ, or NO CLICK where the record holds no click line, with its cause, every train
card's lines, given, taken and net beside the books, every clock's meetings counted with no duration and its books
beside its line, and one refusal line where the record holds no click of either kind, no click line and no whole
click; before it, the three clicks' block on schema 1.4's sides (decoder/three.py, DECODE3 on its readers' folds): the
structure per place, which side lands, R2 within one record on the readings file's past ladder, the passings and the
split's weights as a check against the board's passing, and the checks on two records named beside: R1 (--twin, the
lay run again), R2's two-record form (--apart, a lay one hidden unit apart) and the swap (--swap, the lay with the
--trains exchanged). Nothing is raised: a record or a ledger that is not read is named with its cause. The
interpreter's bound on a whole number's digits is lifted, since the schema's numbers are whole numbers of any width.

Usage: python -I tools/tensor24_decode.py <record .jsonl> [<ledger .jsonl>] [--readings <.json>] [--twin <record>]
       [--apart <record>] [--swap <record> --trains <t> <u>]
"""

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from tensor24.decoder import clicks, records, shadow, three  # noqa: E402

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
    """The click world's block: shadow's four verdicts and the click board's three with their causes, every train card's counts under the books (the Node-clocks' stand in the listing above), every clock's under its line of meetings, and the refusal line where the record holds no click of either kind."""
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
    if not (clicks.listed(record) or record.of("whole")):
        print(f"  {REFUSAL}")


def chosen(path: str | None) -> object:
    """The reading parameters from the readings file, a JSON object, or None where none is named or it is not read."""
    try:
        return json.loads(Path(path).read_text(encoding="utf-8")) if path else None
    except OSError, ValueError, RecursionError:
        return None


def thirds(record: records.Record, held: argparse.Namespace) -> None:
    """The three clicks' block: three's readings on the record, then each check on two records whose second is named, the second not read named with its cause, and the readings owed."""
    print("the three clicks (DECODE3, by the structure of each place, never a label):")
    found = three.readings(record, chosen(held.readings))
    for name, path, check in (
        (three.RUN_TWICE, held.twin, three.twice),
        (three.APART, held.apart, three.apart),
        (three.SWAP, held.swap, lambda a, b: three.swapped(a, b, held.trains or [])),
    ):
        other, why = records.read(path) if path else (None, "")
        found |= {name: check(record, other)} if other else {}
        found |= {name: {"kind": "NOT READ", "cause": f"the second record {why}"}} if why else {}
    for name, verdict in found.items():
        print(f"  {name}: {verdict['kind']}: {verdict['cause']}")
    print(f"  {three.OWED}")


def main(argv: list[str]) -> int:
    """Read the record and its ledger, print the readings and the click lines, and return 0; a usage error is argparse's."""
    parser = argparse.ArgumentParser(
        prog="tensor24_decode.py", description="Tensor24's decoder: one record read."
    )
    parser.add_argument("record")
    parser.add_argument("ledger", nargs="?")
    parser.add_argument(
        "--readings", help="the reading parameters: R2's past ladder, its count, the parts"
    )
    parser.add_argument("--twin", help="a record of the same lay, run again (R1's check)")
    parser.add_argument(
        "--apart", help="a record of a lay one hidden unit apart (R2's two-record check)"
    )
    parser.add_argument("--swap", help="a record of the lay with the trains named by --trains exchanged")
    parser.add_argument("--trains", type=int, nargs="+", help="the trains the swap exchanged")
    held = parser.parse_args(argv[1:])
    sys.set_int_max_str_digits(0)
    record, cause = records.read(held.record)
    if record is None:
        print(f"not read: {cause}")
        return 0
    ledger, why = records.read_ledger(held.ledger) if held.ledger else (None, "the ledger is absent")
    print(f"the ledger: {why if ledger is None else f'read, {len(ledger)} lines'}")
    printed(clicks.counted(record))
    thirds(record, held)
    world(record)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
