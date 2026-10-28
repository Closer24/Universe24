"""The decoder's tool (Animate's): one record of the schema read, with its ledger beside it where it stands, and its
readings printed: row 15's verdict with its two readings, and each whole click's ticks from the rate lines.

Usage: python -I tools/tensor24_decode.py <record .jsonl> [<ledger .jsonl>]
"""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from tensor24.decoder import books, clocks, records  # noqa: E402


def main() -> None:
    record, cause = records.read(sys.argv[1])
    if record is None:
        print(f"not read: {cause}")
        return
    ledger = None
    if len(sys.argv) > 1 + 1:
        with open(sys.argv[1 + 1], encoding="utf-8") as f:
            ledger = [json.loads(text) for text in f]
    print(f"row 15: {books.row_15(record, ledger)}")
    lines = clocks.stretches(record)
    ticks = [
        clocks.ticks_to(lines.get(c["site"], []), c["count"]) for c in record.of("whole") if "count" in c
    ]
    print(f"the whole clicks' ticks from the rate lines: {len(ticks)} read, the last {ticks[-1:]}")


if __name__ == "__main__":
    main()
