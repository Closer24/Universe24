"""The run: the three files checked and loaded, every Node-clock stepping in every round to the setting's ticks, the rewind checked, the record and its ledger written."""

import hashlib
import json
from collections.abc import Callable
from pathlib import Path
from typing import Any, NamedTuple

from tensor24.record import schema
from tensor24.runner.files import OPERANDS, departures, sites_of
from tensor24.runner.load import load, promises
from tensor24.runner.rewind import rewind
from tensor24.runner.rounds import rounds

ORDER = "z fastest: the site (x sy + y) sz + z"  # runner/board.py's
CLOCK = "the clock"  # the clock's own train, after the file's trains: every gear's teeth read its count
STEP = "step"  # a count line's place in its round: after the step


class Engine(NamedTuple):
    """The engine's functions as main.py passes them: the kinds and their tables, the layout, the round, its run back, the state."""

    made: Callable[..., Any]
    layout: Callable[..., Any]
    tick: Callable[..., Any]
    untick: Callable[..., Any]
    state: Callable[..., Any]


def digest(text: str) -> str:
    """SHA-256 in hex, the record's digest."""
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def stated(s: Any) -> str:
    """The state's integers as one JSON text, array by array: its digest's text and its comparison's."""
    return json.dumps([x.tolist() for x in s])


def ledger_of(record: Path) -> Path:
    """The ledger's own file, beside the record: its name with ".ledger" before its suffix."""
    return record.with_name(f"{record.stem}.ledger{record.suffix}")


def counts(round_: int, s: Any, trains: list[Any]) -> list[dict[str, Any]]:
    """One round's count lines of the ledger: per Node-clock and train, the train's now counts there, row by row."""
    return [
        {
            "round": round_,
            "at": STEP,
            "site": site,
            "train": at,
            "count": s.a[train.first : train.first + train.rows(), site].tolist(),
        }
        for site in range(s.a.shape[-1])
        for at, train in enumerate(trains)
    ]


def header(
    record: Path,
    files: list[tuple[Path, str]],
    universe: dict[str, Any],
    shape: list[int],
    kinds: Any,
    loaded: Any,
    layout: Any,
) -> dict[str, Any]:
    """The record's first line: the files verbatim with their digests, the board, the kinds, the trains with their windings."""
    labels = [*(train["name"] for train in universe["trains"]), CLOCK]
    return {
        "kind": "header",
        "record": record.name,
        "major": schema.MAJOR,
        "minor": schema.MINOR,
        "engine": "tensor24",
        "runner": "synchronous",
        "files": [{"name": path.name, "text": text, "digest": digest(text)} for path, text in files],
        "sides": shape,
        "order": ORDER,
        "kinds": [
            {"index": at, "label": name.upper(), "dimension": kind.shape[-1]}
            for at, (name, kind) in enumerate(zip(kinds._fields, kinds, strict=True))
        ],
        "trains": [
            {
                "index": at,
                "label": label,
                "kinds": list(train.kinds),
                "part": train.part,
                "winding": layout.gearing.drive[train.first, 0],
            }
            for at, (label, train) in enumerate(zip(labels, loaded.trains, strict=True))
        ],
        "couplings": universe.get("couplings", []),
        "operands": list(OPERANDS),
        "width": universe["integers"]["width"],
    }


def run(engine: Engine, paths: list[Path], record: Path) -> list[str]:
    """The three files run to the record at its path and the ledger beside it, every Node-clock in every round, every departure named and nothing written past one."""
    found = departures(*paths)
    if found:
        return found
    files = [(path, path.read_text(encoding="utf-8")) for path in paths]
    universe, piece, setting = (json.loads(text) for _, text in files)
    shape = piece["shape"]
    kinds, tables = engine.made(tuple(shape))
    loaded, found = load(universe, setting, sites_of(shape), kinds, tables)
    if loaded is None:
        return found
    layout = engine.layout(universe, shape, loaded)
    start = engine.state(*loaded.state)
    # the clocks stand at 0 as laid, so the teeth are the rest; a moving clock's are read at G2
    found = promises(start.r, layout.gearing.rest)
    if found:
        return found
    ticks, end, ledger = setting["ticks"], start, []
    for at, end in enumerate(rounds(engine.tick, layout, start, ticks), start=1):
        ledger += counts(at, end, loaded.trains)
    exact = int(stated(rewind(engine.untick, layout, end, ticks)) == stated(start))
    lines = [
        header(record, files, universe, shape, kinds, loaded, layout),
        {"kind": "end", "rounds": ticks, "digest": digest(stated(end)), "undone": ticks, "exact": exact},
    ]
    record.write_text("".join(json.dumps(line) + "\n" for line in lines), encoding="utf-8")
    ledger_of(record).write_text("".join(json.dumps(line) + "\n" for line in ledger), encoding="utf-8")
    return []
