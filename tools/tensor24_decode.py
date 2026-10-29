"""The decoder's tool (Animate's): one record of the schema read, with its ledger beside it where one is named, and its
readings printed: row 15's verdict with its two readings, row 46's with its two, the measurement's rules (the cone
check by click, proper time read twice and the twin reading), and each whole click's ticks from the rate lines.
Nothing is raised: a record or a ledger that is not read is named with its cause, and the rows that need it read NOT
READ. The interpreter's bound on a whole number's digits is lifted, since the schema's numbers are whole numbers of
any width. Each Node-clock's rate lines are read once for all its whole clicks.

Usage: python -I tools/tensor24_decode.py <record .jsonl> [<ledger .jsonl>]
"""

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from tensor24.decoder import bangs, books, clocks, measure, records  # noqa: E402


def ticks(record: records.Record) -> str:
    """Each whole click's ticks from its Node-clock's rate lines: how many are read, the first not read, the last."""
    lines, clicks = clocks.stretches(record), record.of("whole")
    by_site: dict[int, list[int]] = {}
    for at, c in enumerate(clicks):
        by_site.setdefault(c["site"], []).append(at)
    found: dict[int, int | None] = {}
    for site, ats in by_site.items():
        found |= dict(
            zip(
                ats,
                clocks.ticks_at(lines.get(site, []), [clicks[at].get("count") for at in ats]),
                strict=True,
            )
        )
    read = [found[at] for at in range(len(clicks)) if found[at] is not None]
    unread = [c for at, c in enumerate(clicks) if found[at] is None]
    first = (
        f", the first not read at round {unread[0]['round']}, site {unread[0]['site']}: "
        f"{clocks.unread(lines.get(unread[0]['site'], []), unread[0].get('count'))}"
        if unread
        else ""
    )
    return f"the whole clicks' ticks from the rate lines: {len(read)} read, {len(unread)} not read{first}; the last read {read[-1:]}"


def main(argv: list[str]) -> int:
    """Read the record and its ledger, print the readings, and return 0; a usage error is argparse's."""
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
    print(f"the cone check (D8): {measure.cone_check(record)}")
    print(f"proper time (D6): {measure.proper(record)}")
    print(f"the twin reading (D6): {measure.twins(record)}")
    print(ticks(record))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
