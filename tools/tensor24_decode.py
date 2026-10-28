"""The decoder's tool (Animate's): one record of the schema read, with its ledger beside it where one is named, and its
readings printed: row 15's verdict with its two readings, and each whole click's ticks from the rate lines. Nothing is
raised: a record or a ledger that is not read is named with its cause, and the rows that need it read NOT READ. The
interpreter's bound on a whole number's digits is lifted, since the schema's numbers are whole numbers of any width.

Usage: python -I tools/tensor24_decode.py <record .jsonl> [<ledger .jsonl>]
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from tensor24.decoder import books, clocks, records  # noqa: E402

USAGE = "usage: python -I tools/tensor24_decode.py <record .jsonl> [<ledger .jsonl>]"


def ticks(record: records.Record) -> str:
    """Each whole click's ticks from its Node-clock's rate lines: how many are read, the first not read, the last."""
    lines = clocks.stretches(record)
    read, unread = [], []
    for c in record.of("whole"):
        held = lines.get(c["site"], [])
        tick = clocks.ticks_to(held, c.get("count"))
        if tick is None:
            unread.append(f"round {c['round']}, site {c['site']}: {clocks.unread(held, c.get('count'))}")
        else:
            read.append(tick)
    first = f", the first not read at {unread[0]}" if unread else ""
    return f"the whole clicks' ticks from the rate lines: {len(read)} read, {len(unread)} not read{first}; the last read {read[-1:]}"


def main(argv: list[str]) -> int:
    """Read the record and its ledger, print the readings, and return the exit code: 2 for a usage error, else 0."""
    if len(argv) not in (2, 3):
        print(USAGE, file=sys.stderr)
        return 2
    sys.set_int_max_str_digits(0)
    record, cause = records.read(argv[1])
    if record is None:
        print(f"not read: {cause}")
        return 0
    ledger, why = records.read_ledger(argv[2]) if len(argv) == 3 else (None, "the ledger is absent")
    print(f"row 15: {books.row_15(record, ledger, why)}")
    print(ticks(record))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
