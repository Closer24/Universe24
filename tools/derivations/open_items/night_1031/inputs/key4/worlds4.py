"""The shipped worlds' records by the run tool's own function, main.ran, on whichever tree is first on sys.path: the
procedure of node-all 9d75a4904's prefixes/write.py for every world but our bang (each world run REACH rounds, its first
click round read off that record, then run to it, then PREFIX rounds), and our bang run whole (its own ticks, as the
run test runs it). Each record's readings: its rounds, its count of click lines and their digest (SHA-256 of the click
lines' text as the run wrote them, a line feed between two), its end line, each train's key on the header's cards, the
header's dial and birth, the header's file digests, three digests that compare the record byte for byte (the
header's text with its files left out, every line after the header, and the ledger beside the record), and the cause
the decoder's reader names, if any, on the same tree. No digest is typed.
"""

import hashlib
import json
from pathlib import Path

from tensor24 import main
from tensor24.decoder import records as decoding
from tensor24.runner.files import NAMES

PREFIX = 4  # write.py's
BANG = "tensor24"  # write.py's: our bang's folder, which the run test runs whole
REACH = 200  # write.py's window for each world's first click


def sha(text):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def ran(examples, world, rounds, scratch):
    """The world's own three files run out and back for the rounds (None: its own ticks), as write.py's ran: the
    setting's ticks set, every other field of it kept."""
    *paths, setting = [examples.joinpath(world, f"{name}.json") for name in NAMES]
    record = Path(scratch).joinpath(f"{world}.jsonl")
    if rounds is not None:
        held = json.loads(setting.read_text(encoding="utf-8"))
        held["ticks"] = rounds
        setting = Path(scratch).joinpath(f"{world}.json")
        setting.write_text(json.dumps(held), encoding="utf-8")
    found = main.ran([*paths, setting], record)
    assert not found, found
    text = record.read_text(encoding="utf-8").splitlines()
    header, end = json.loads(text[0]), json.loads(text[-1])
    assert end["exact"] == 1, end
    clicks = [x for x in text if json.loads(x)["kind"] == "click"]
    ledger = record.with_name(f"{record.stem}.ledger{record.suffix}").read_text(encoding="utf-8")
    return {
        "world": world,
        "rounds": end["rounds"],
        "clicks": len(clicks),
        "lines": sha("\n".join(clicks)),
        "end": end,
        "keys": [t["key"] for t in header["trains"]],
        "dial": header["dial"],
        "birth": header["birth"],
        "files": {f["name"]: f["digest"] for f in header["files"]},
        "head": sha(json.dumps({k: v for k, v in header.items() if k != "files"})),
        "body": sha("\n".join(text[1:])),
        "ledger": sha(ledger),
        "cause": decoding.read(str(record))[1],
    }


def records(examples, scratch):
    """Every shipped world's records, in write.py's order (the folders sorted), our bang last."""
    out = []
    for world in sorted(f.name for f in examples.glob("*/") if f.name != BANG):
        reach = ran(examples, world, REACH, scratch)
        out.append({"run": "reach", **reach})
        text = Path(scratch).joinpath(f"{world}.jsonl").read_text(encoding="utf-8").splitlines()
        first = min([json.loads(x)["round"] for x in text if json.loads(x)["kind"] == "click"] or [PREFIX])
        out.append({"run": "first", **ran(examples, world, first, scratch)})
        out.append({"run": "prefix", **ran(examples, world, PREFIX, scratch)})
    out.append({"run": "whole", **ran(examples, BANG, None, scratch)})
    return out


def pinned(rows):
    """The lines write.py writes, from the records: per world but our bang, its first-click record's end line (its
    PREFIX rounds where it has no click) with the world's name, its count of click lines and their digest, the no case's
    PREFIX rounds and the world's own digest at them."""
    lines, by = [], {}
    for row in rows:
        by.setdefault(row["world"], {})[row["run"]] = row
    for world in sorted(w for w in by if w != BANG):
        runs = by[world]
        head = runs["first"]
        lines.append(
            json.dumps(
                {
                    "world": world,
                    "clicks": head["clicks"],
                    "lines": head["lines"],
                    "no": PREFIX,
                    "own": runs["prefix"]["end"]["digest"],
                    **head["end"],
                }
            )
        )
    return lines
