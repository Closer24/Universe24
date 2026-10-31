"""Tensor24's page: one run's record drawn as one self-contained page, the worlds seen running (the owner's word of
about 06:50 UTC, VIEW1). The page shows two views, each named as what it is: the board, the Node-clocks and their
trains by their cards' names (a clock fact), and the click world, each round's click lines in the record's order,
each a quantum passing between two clocks at one place; beside them the decoder's readings, each with its verdict as
the decoder gives it. The record, and the ledger beside it where one is named, are read by the decoder's own
readers, and the readings are the decoder's own, called as tools/tensor24_decode.py calls them: the tool computes
no reading and no physics, and the page draws only what the record and its ledger hold. The data goes into the page
as JSON; a record too long for the page's bound is thinned by rounds, and the page says so. A whole number wider
than a page script reads exactly is written as its digits.

Usage: python -I tools/look/tensor24_page.py <record .jsonl> [<ledger .jsonl>] --page <page .html> [--world <name>]
"""

import argparse
import html
import json
import sys
from collections.abc import Callable
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT.joinpath("src")))
sys.path.insert(0, str(ROOT.joinpath("tools")))

import tensor24_decode  # noqa: E402, I001
from tensor24.decoder import clicks, records, shadow  # noqa: E402

TEMPLATE = Path(__file__).with_name("tensor24_page.html")
LIMIT = 15_000_000  # the page's bound in bytes, below the 16 MB a published page may take
# the widest whole number a page script reads exactly; a wider one goes in as its digits
SAFE = 2**53 - 1
# a click line's fields as the page holds them, in this order
FIELDS = ("site", "train", "q", "sides", "across")
Readings = Callable[[records.Record], dict[str, dict[str, Any]]]
# the decoder's readings, block by block: a block's name, where the decoder holds it, and its reader, which gives
# its verdicts by name; a reading the decoder gains is one more entry here, drawn as one more row of the panel
READERS: tuple[tuple[str, str, Readings], ...] = (
    ("The click world, read in the board's shadow", "decoder/shadow.py, shadow", shadow.shadow),
    ("The click board, the clocks' meetings", "decoder/shadow.py, click_board", shadow.click_board),
)


def plain(value: Any) -> Any:
    """A value as JSON holds it: a row of the decoder's counts by its fields' names, a key of several parts by its parts joined, a whole number past SAFE as its digits."""
    if hasattr(value, "_asdict"):
        return plain(value._asdict())
    if isinstance(value, dict):
        named = {", ".join(map(str, k)) if isinstance(k, tuple) else str(k): v for k, v in value.items()}
        return {k: plain(v) for k, v in named.items()}
    if isinstance(value, list | tuple):
        return [plain(item) for item in value]
    if isinstance(value, int) and not isinstance(value, bool) and abs(value) > SAFE:
        return str(value)
    return value


def thinned(rounds: int, stride: int) -> list[int]:
    """The rounds drawn at a stride: the first, every stride-th after it, and the last."""
    return [r for r in range(1, rounds + 1) if (r - 1) % stride == 0 or r == rounds]


def ledger_counts(
    ledger: list[records.Line], kept: list[int], sites: int, trains: int
) -> dict[str, Any]:
    """The ledger's Count lines at the rounds drawn, by round, Node-clock and train: the train's now counts there."""
    keep = set(kept)
    held: dict[str, list[list[Any]]] = {}
    for line in ledger:
        site, train, round_ = line.get("site"), line.get("train"), line.get("round")
        if round_ in keep and line.get("at") == "step" and isinstance(site, int) and 0 <= site < sites:
            if isinstance(train, int) and 0 <= train < trains:
                rows = held.setdefault(str(round_), [[None] * trains for _ in range(sites)])
                rows[site][train] = plain(line.get("count"))
    return held


def readings(record: records.Record) -> list[dict[str, Any]]:
    """The decoder's readings, block by block, each a row: its name, its verdict, its cause and the readings it stands on."""
    blocks = []
    for name, source, reader in READERS:
        rows = [
            {
                "name": reading,
                "kind": verdict["kind"],
                "cause": verdict["cause"],
                "more": plain({k: v for k, v in verdict.items() if k not in ("kind", "cause")}),
            }
            for reading, verdict in reader(record).items()
        ]
        blocks.append({"block": name, "source": source, "rows": rows})
    return blocks


def data_of(
    record: records.Record, ledger: list[records.Line] | None, why: str, world: str, stride: int
) -> dict[str, Any]:
    """The page's data: the header and the end as the record holds them, the click lines and the ledger's counts at the rounds drawn, each round's count of click lines, the decoder's counts and readings."""
    rounds = record.end.get("rounds")
    rounds = rounds if isinstance(rounds, int) and rounds >= 1 else 0
    kept = thinned(rounds, stride) if stride else []
    _, sites = records.board(record.header)
    trains = len(record.header.get("trains", []))
    lines = clicks.listed(record)
    per: dict[str, int] = {}
    drawn: dict[str, list[list[Any]]] = {}
    keep = set(kept)
    for line in lines:
        per[str(line["round"])] = per.get(str(line["round"]), 0) + 1
        if line["round"] in keep:
            drawn.setdefault(str(line["round"]), []).append([plain(line.get(f)) for f in FIELDS])
    counted = clicks.counted(record)
    return {
        "world": world,
        "read": "",
        "header": plain(record.header),
        "end": plain(record.end),
        "rounds": rounds,
        "kept": kept,
        "thinned": len(kept) < rounds,
        "stride": stride,
        "fields": list(FIELDS),
        "total": len(lines),
        "per": per,
        "clicks": drawn,
        "ledger": why,
        "counts": ledger_counts(ledger, kept, sites, trains)
        if ledger and isinstance(sites, int)
        else {},
        "basic": {
            "lines": len(counted.lines),
            "places": counted.places,
            "crossed": counted.crossed,
            "trains": plain(counted.trains),
        },
        "readings": readings(record),
        "refusal": "" if lines else tensor24_decode.REFUSAL,
    }


def summary(data: dict[str, Any]) -> str:
    """The page's first sentence, written into it before any script runs."""
    if data["read"]:
        return f"The record is not read: {data['read']}."
    sides = " x ".join(str(s) for s in data["header"].get("sides", []))
    rounds = data["rounds"]
    if not data["total"]:
        return f"The record holds no click line: not in the click world. {rounds} rounds on a board of {sides}."
    return f"{data['total']} click lines in the run's {rounds} rounds, on a board of {sides}."


def escaped(text: str) -> str:
    """A text for the page's markup, in ASCII."""
    return html.escape(text, quote=False).encode("ascii", "xmlcharrefreplace").decode()


def page_of(data: dict[str, Any]) -> str:
    """The template filled: the title, the first sentence and the data, the data's markup characters escaped."""
    text = json.dumps(data, separators=(",", ":"), ensure_ascii=True)
    text = text.replace("<", "\\u003c").replace(">", "\\u003e").replace("&", "\\u0026")
    filled = TEMPLATE.read_text(encoding="utf-8").replace(
        "@@TITLE@@", escaped(f"{data['world']} running")
    )
    return filled.replace("@@SUMMARY@@", escaped(summary(data))).replace("@@DATA@@", text)


def written(record: records.Record, ledger: list[records.Line] | None, why: str, world: str) -> str:
    """The page within its bound: every round drawn where it fits, else the record thinned to the least stride that fits (stride 0 draws no round, the page's fixed part)."""
    text = page_of(data_of(record, ledger, why, world, 1))
    if len(text) <= LIMIT:
        return text
    bare = len(page_of(data_of(record, ledger, why, world, 0)))
    stride = max(2, -(-(len(text) - bare) // max(1, LIMIT - bare)))
    while True:
        data = data_of(record, ledger, why, world, stride)
        text = page_of(data)
        if len(text) <= LIMIT or len(data["kept"]) <= 2:
            return text
        stride += 1


def main(argv: list[str]) -> int:
    """Read the record and its ledger, write the page, print its path and size, and return 0; a usage error is argparse's."""
    parser = argparse.ArgumentParser(
        prog="tensor24_page.py", description="Tensor24's page: one run's record drawn."
    )
    parser.add_argument("record")
    parser.add_argument("ledger", nargs="?")
    parser.add_argument("--page", required=True, type=Path, help="the page to write")
    parser.add_argument(
        "--world", help="the world's name on the page; the record's file name by default"
    )
    held = parser.parse_args(argv[1:])
    sys.set_int_max_str_digits(0)
    world = held.world or Path(held.record).stem
    record, cause = records.read(held.record)
    if record is None:
        text = page_of({"world": world, "read": cause})
    else:
        ledger, why = records.read_ledger(held.ledger) if held.ledger else (None, "the ledger is absent")
        text = written(
            record, ledger, f"read, {len(ledger)} lines" if ledger is not None else why, world
        )
    held.page.write_text(text, encoding="ascii")
    print(f"{held.page}: written, {len(text)} bytes")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
