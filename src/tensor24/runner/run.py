"""Clock: the run from the three files to the record: every Node-clock steps every round, then all the rounds run back.
Algebra: the act iterated; before each round the promise, every fine tooth within its teeth, and the wave's window, the Spokes' grips within the teeth per sense, are read; the start returns bit for bit.
Board: the files checked and loaded, the rounds run, the rewind checked, the record and its ledger written.
Clicks: it writes what the act gives: the record's header and end and the ledger beside them; click lines from G5.
"""

import dataclasses
import hashlib
import json
from collections.abc import Callable
from pathlib import Path
from typing import Any, NamedTuple

import numpy as np

from tensor24.algebra.carry import carry
from tensor24.record import schema
from tensor24.runner.files import OPERANDS, departures, held_departures, sites_of, vocabulary
from tensor24.runner.load import load, star
from tensor24.runner.rewind import rewind
from tensor24.runner.rounds import rounds

ORDER = "z fastest: the site (x sy + y) sz + z"  # runner/board.py's
STEP = "step"  # a count line's place in its round: after the step


class Engine(NamedTuple):
    """The engine's functions as main.py passes them: the kinds and their tables, the layout, the round, its run back, the state, every gear's teeth and every Spoke's grip at a state's now slot."""

    made: Callable[..., Any]
    layout: Callable[..., Any]
    tick: Callable[..., Any]
    untick: Callable[..., Any]
    state: Callable[..., Any]
    teeth: Callable[..., Any]
    grips: Callable[..., Any]


def promises(r: Any, w: Any) -> list[str]:
    """The round's promise on the state it reads, read from outside, each departure named where it stands: every fine tooth within [0, w), its teeth."""
    w = np.broadcast_to(w, r.shape)
    return [
        f"row {g}, site {x}: the fine tooth {r[g, x]} not within [0, {w[g, x]})"
        for g, x in np.argwhere((r < 0) | (r >= w))
    ]


def window(held: Any, w: Any, spokes: Any) -> list[str]:
    """The wave's window on the state the round reads, read from outside, each departure named where it stands: the Spokes' grips summed within [0, W] per sense, the senses along one axis counted from the star, so that the pull's sharpest mode, every neighbour opposite, stays a wave and does not grow unseen."""
    senses, _ = carry(spokes.shape[0], spokes.shape[1], 0)
    total, reach = np.broadcast_to(held.sum(axis=1), w.shape), senses * w
    return [
        f"row {g}, site {x}: the Spokes' grips {total[g, x]} not within [0, {reach[g, x]}], the wave's window"
        for g, x in np.argwhere((total < 0) | (total > reach))
    ]


def promised(engine: Engine, layout: Any, s: Any) -> list[str]:
    """Both promises of the round that reads a state, read from outside: every fine tooth within its teeth, and the wave's window."""
    w = engine.teeth(layout, s)
    return promises(s.r, w) + window(engine.grips(layout, s), w, layout.spokes)


def digest(text: str) -> str:
    """SHA-256 in hex, the record's digest."""
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def stated(s: Any) -> str:
    """The state's integers as one JSON text, array by array: its digest's text and its comparison's."""
    return json.dumps([x.tolist() for x in s])


def ledger_of(record: Path) -> Path:
    """The ledger's own file, beside the record: its name with ".ledger" before its suffix."""
    return record.with_name(f"{record.stem}.ledger{record.suffix}")


def counts(round_: int, s: Any, trains: Any) -> list[dict[str, Any]]:
    """One round's Count lines of the ledger, schema.Count's fields in order: per Node-clock and train, the train's now counts there, row by row."""
    return [
        dataclasses.asdict(
            schema.Count(
                round_,
                STEP,
                site,
                at,
                tuple(s.a[train.first : train.first + train.rows(), site].tolist()),
            )
        )
        for site in range(s.a.shape[-1])
        for at, train in enumerate(trains[n] for n in range(len(trains)))
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
    labels = [train["name"] for train in universe["trains"]]
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
            for at, (label, train) in enumerate(
                zip(labels, (loaded.trains[n] for n in range(len(labels))), strict=True)
            )
        ],
        "couplings": [],  # no file declares a coupling: the header's field stands empty until the schema retires it
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
    kinds, tables, square = engine.made(star(len(shape)))
    found = held_departures(universe, setting, vocabulary(kinds, square))
    if found:
        return found
    loaded, found = load(universe, setting, sites_of(shape), kinds, tables, square)
    if found:
        return found
    layout = engine.layout(universe, shape, loaded)
    start = engine.state(*loaded.state)
    ticks, end, ledger = setting["ticks"], start, ledger_of(record)
    # every promise is the round's that reads the state: none where no round runs
    found = promised(engine, layout, start) if ticks else []
    if found:
        return [f"round 1: {line}" for line in found]
    with ledger.open("w", encoding="utf-8") as counted:
        for at, end in enumerate(rounds(engine.tick, layout, start, ticks), start=1):
            counted.writelines(json.dumps(line) + "\n" for line in counts(at, end, loaded.trains))
            # the promises of the round that reads this state, read from outside: every kept tooth within its
            # teeth, and the grips within the window
            found = promised(engine, layout, end) if at < ticks else []
            if found:
                ledger.unlink()
                return [f"round {at + 1}: {line}" for line in found]
    exact = int(stated(rewind(engine.untick, layout, end, ticks)) == stated(start))
    lines = [
        header(record, files, universe, shape, kinds, loaded, layout),
        {"kind": "end", "rounds": ticks, "digest": digest(stated(end)), "undone": ticks, "exact": exact},
    ]
    record.write_text("".join(json.dumps(line) + "\n" for line in lines), encoding="utf-8")
    return []
