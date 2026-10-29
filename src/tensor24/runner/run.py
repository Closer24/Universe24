"""The run: the three files checked and loaded, the rounds to the setting's ticks, every due beat firing or the caller's masks, the rewind checked, the record written."""

import hashlib
import json
from collections.abc import Callable
from pathlib import Path
from typing import Any, NamedTuple

import numpy as np

from tensor24.record import schema
from tensor24.runner.files import OPERANDS, departures, sites_of
from tensor24.runner.load import load, promises
from tensor24.runner.rewind import rewind

ORDER = "z fastest: the site (x sy + y) sz + z"  # runner/board.py's
TIME = "the time gear"  # the clock's own train, after the file's trains: its count is the tick's weight


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


def ran(
    engine: Engine, layout: Any, start: Any, ticks: int, bits: Callable[[int, int], list[int]]
) -> tuple[Any, list[Any], list[dict[str, Any]]]:
    """Rounds until every Node-clock's count stands at the ticks, each round's mask the bits where a count falls short; a Node-clock's k written at its first beat and wherever it changes."""
    s: Any = start
    outs: list[Any] = []  # the undo log
    rates: list[dict[str, Any]] = []
    last: dict[int, int] = {}  # each Node-clock's k at its last beat
    while any(c < ticks for c in s.c[0].tolist()):
        short = [int(c < ticks) for c in s.c[0].tolist()]
        mask = [bit * held for bit, held in zip(bits(len(outs) + 1, len(short)), short, strict=True)]
        s, out = engine.tick(layout, s, np.array([mask], dtype=object))
        outs.append(out)
        beats = zip(
            out.fire[0].tolist(), out.k[0].tolist(), s.c[0].tolist(), s.ph[0].tolist(), strict=True
        )
        for site, (fire, k, count, dial) in enumerate(beats):
            if fire and last.get(site) != k:
                rates.append(
                    {
                        "kind": "rate",
                        "round": len(outs),
                        "site": site,
                        "count": count,
                        "dial": dial,
                        "k": k,
                    }
                )
                last[site] = k
    return s, outs, rates


def header(
    record: Path,
    files: list[tuple[Path, str]],
    universe: dict[str, Any],
    shape: list[int],
    kinds: Any,
    loaded: Any,
    layout: Any,
    runner: str,
) -> dict[str, Any]:
    """The record's first line: the files verbatim with their digests, the board, the kinds, the trains with their windings."""
    labels = [*(train["name"] for train in universe["trains"]), TIME]
    return {
        "kind": "header",
        "record": record.name,
        "major": schema.MAJOR,
        "minor": schema.MINOR,
        "engine": "tensor24",
        "runner": runner,
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


def run(
    engine: Engine, paths: list[Path], record: Path, bits: Callable[[int, int], list[int]] | None = None
) -> list[str]:
    """The three files run to the record at its path, every due beat firing or the caller's masks (a test's), every departure named and nothing written past one."""
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
    found = promises(
        start.r, layout.gearing.rest, layout.rate, layout.gamma
    )  # the clocks stand at 0 as laid
    if found:
        return found
    every = bits or (lambda _, n: [1] * n)
    end, outs, rates = ran(engine, layout, start, setting["ticks"], every)
    back = rewind(engine.untick, layout, end, outs)
    runner = "synchronous" if bits is None else "under the caller's masks"
    exact = int(stated(back) == stated(start))
    lines = [
        header(record, files, universe, shape, kinds, loaded, layout, runner),
        *rates,
        {
            "kind": "end",
            "rounds": len(outs),
            "digest": digest(stated(end)),
            "undone": len(outs),
            "exact": exact,
        },
    ]
    record.write_text("".join(json.dumps(line) + "\n" for line in lines), encoding="utf-8")
    return []
