"""Clock: the run from the three files to the record: every Node-clock steps every round, then all the rounds run back.
Algebra: the act iterated; before each round the promise, every tooth within its edge's dial of both slots' teeth, the wave's window, the Spokes' grips within the teeth per sense, and the width, every count of both slots within the universe's width, are read; the start returns bit for bit.
Board: the files checked and loaded, the rounds run, the rewind checked, the record and its ledger written.
Clicks: it writes what the act gives: the record's header (schema 3.0: each kind's characters on the 24, each train's key, the edge key, and its square flag, and the edge dial), its click lines and its end, and the ledger beside them; wherever an edge side carried in a round, a click line for every train joined to it at that Node-clock, q the sum of its sides' quotients signed (a give below 0, a take above it), and every edge side of its train, the other train and the side's q, 0 included (DECODE3), and in across each Mesh side that carried, the other train, the partner's place and the side's q; the end's edges, every own edge side's two trains, and its across, every Mesh edge side's partner place; no tooth, no birth and no end tooth (the owner's word on Q11, "out entirely"): the teeth are the board's; the forward run's lines alone (the run back negates the quotients and writes none).
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
from tensor24.runner.files import OPERANDS, departures, held_departures, sites_of, star, vocabulary
from tensor24.runner.load import load
from tensor24.runner.rewind import rewind
from tensor24.runner.rounds import rounds

ORDER = "z fastest: the site (x sy + y) sz + z"  # runner/board.py's
STEP = "step"  # a count line's place in its round: after the step


class Engine(NamedTuple):
    """The engine's functions as main.py passes them: the kinds and their tables, the layout, the round's act (the state reached and its clicks), its run back, the state, every gear's teeth at a state's two slots and every Spoke's grip at its now slot."""

    made: Callable[..., Any]
    layout: Callable[..., Any]
    act: Callable[..., Any]
    untick: Callable[..., Any]
    state: Callable[..., Any]
    dials: Callable[..., Any]
    grips: Callable[..., Any]


def promises(s: Any, wa: Any, wb: Any) -> list[str]:
    """The round's promise on the state it reads, read from outside, each departure named where it stands: both slots' teeth at least 1, named as teeth where they are not, and every tooth within its edge's dial, -D <= s < D, D = W(b) + W(a), where they are."""
    _, _, tooth, _, _ = s
    wa, wb = np.broadcast_to(wa, tooth.shape), np.broadcast_to(wb, tooth.shape)
    d, low = wa + wb, (wa < 1) | (wb < 1)
    off = ~low & ((tooth < -d) | (tooth >= d))
    teeth = [
        f"row {g}, site {x}: the teeth {wb[g, x]} and {wa[g, x]}, not both at least 1"
        for g, x in np.argwhere(low)
    ]
    return teeth + [
        f"row {g}, site {x}: the tooth {tooth[g, x]} not within the edge's dial [-{d[g, x]}, {d[g, x]}) of the teeth {wb[g, x]} and {wa[g, x]}"
        for g, x in np.argwhere(off)
    ]


def window(held: Any, w: Any, spokes: Any) -> list[str]:
    """The wave's window on the state the round reads, read from outside, each departure named where it stands: the Spokes' grips summed within [0, W] per sense where the teeth are at least 1 (below, the promise names the teeth), the senses along one axis counted from the star, so that the pull's sharpest mode, every neighbour opposite, stays a wave and does not grow unseen."""
    senses, _ = carry(spokes.shape[0], spokes.shape[1], 0)
    total, reach = np.broadcast_to(held.sum(axis=1), w.shape), senses * w
    return [
        f"row {g}, site {x}: the Spokes' grips {total[g, x]} not within [0, {reach[g, x]}], the wave's window"
        for g, x in np.argwhere((w >= 1) & ((total < 0) | (total > reach)))
    ]


def wide(s: Any, width: int) -> list[str]:
    """The width's promise on the state the round reads, read from outside, each departure named where it stands: every count of both slots within the universe's width, as the files' every integer is, so that a run whose counts leave it (a runaway, whatever its cause) is named at the round it first stands there, and not left to raise in the ledger's text."""
    a, b, _, _, _ = s
    return [
        f"row {g}, site {x}: the count {n} takes more bits than the width, {width}"
        for slot in (a, b)
        for (g, x), n in np.ndenumerate(slot)
        if int(n).bit_length() > width
    ]


def promised(engine: Engine, layout: Any, s: Any, width: int) -> list[str]:
    """The promises of the round that reads a state, read from outside: every tooth within its edge's dial, the wave's window at the now slot's teeth, and every count within the width."""
    wa, wb = engine.dials(layout, s)
    return promises(s, wa, wb) + window(engine.grips(layout, s), wa, layout.spokes) + wide(s, width)


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


def joined(click: Any, trains: int) -> list[list[int]]:
    """Each train's edges at its own Node-clock as the edge plan lays them, the other trains u, in u's order, onto which a leg of the train weighs: the pairs a monomial joins, the diagonal and a pair no monomial joins never listed."""
    partners: list[set[int]] = [set() for _ in range(trains)]
    for term, u in np.argwhere(click.weight != 0):
        partners[int(click.train[term])].add(int(u))
    return [sorted(others - {t}) for t, others in enumerate(partners)]


def crossed(click: Any, trains: int) -> list[tuple[int, int, int]]:
    """The Mesh's edges as the plan lays them, (Spoke, t, u) in that order: the trains a pair of rows with a coupling joins across the Spoke, t here and u across it."""
    found: set[tuple[int, int, int]] = set()
    for s, r, p in np.argwhere(click.across != 0):
        spoke, t, u = np.unravel_index(click.onto[s, r, p], (len(click.across), trains, trains))
        found.add((int(spoke), int(t), int(u)))
    return sorted(found)


def meeting(partners: list[list[int]]) -> list[int]:
    """Each train's set of clocks joined to it by edges at its own Node-clock, told by its least train: the clocks that meet at a place together."""
    least = list(range(len(partners)))
    # every train's least reaches each train joined to it within as many passes as there are trains
    for _ in partners:
        least = [min([least[t], *(least[u] for u in us)]) for t, us in enumerate(partners)]
    return least


def clicked(round_: int, clicks: Any, partners: list[list[int]], nb: Any) -> list[dict[str, Any]]:
    """One round's Click lines of the record, in the schema's order (site, then train): wherever an edge side carried, every clock joined to it at its Node-clock writes its line, schema.Click's fields: the line's place; its q, the sum of all its sides'; in sides every edge side of its clock at its own Node-clock in the other train's order, q_tu 0 included (DECODE3), [u, q_tu]; and in across each of its Mesh edge sides that carried, in the order of the partner's place and train, [u, the place across the Spoke, q_tu]. So every listed side's mirror stands in the other clock's line, at its place; a Mesh side of q 0 is listed nowhere, as that would chain every clock of the board into every round's lines."""
    trains, met, sites = len(partners), meeting(partners), clicks.shape[-1]
    own = trains * trains
    inner, outer = (
        clicks[:own].reshape(trains, trains, sites),
        clicks[own:].reshape(-1, trains, trains, sites),
    )
    # each clock with a side that carried, at its own Node-clock or across a Spoke
    lines, moved = [], (inner != 0).any(axis=1) | (outer != 0).any(axis=0).any(axis=1)
    for site in (int(x) for x in np.flatnonzero(moved.any(axis=0))):
        carried = {met[t] for t in np.flatnonzero(moved[:, site])}
        for train in (t for t in range(trains) if met[t] in carried):
            listed = [[u, int(inner[train, u, site])] for u in partners[train]]
            # each Mesh side that carried, by the partner's place and then its train
            ends = sorted(
                (int(nb[s, site]), int(u), int(outer[s, train, u, site]))
                for s, u in np.argwhere(outer[:, train, :, site] != 0)
            )
            across = [[u, place, q] for place, u, q in ends]
            q = sum(q for _, q in listed) + sum(q for _, _, q in across)
            line = {
                "kind": "click",
                "round": round_,
                "site": site,
                "train": train,
                "q": q,
                "sides": listed,
                "across": across,
            }
            lines.append(line)
    return lines


def characters(kinds: Any) -> list[list[int]]:
    """Each kind's character on the 24 turns in the turns' order: its trace on the candidates the star's weight keeps, where the kinds' matrices are not 0."""
    kept = sum(np.einsum("gij,gij->g", k, k) for k in kinds)  # 0 off the 24 for every kind
    return [[int(t) for t, w in zip(np.einsum("gii->g", k), kept, strict=True) if w] for k in kinds]


def header(
    record: Path,
    files: list[tuple[Path, str]],
    universe: dict[str, Any],
    shape: list[int],
    kinds: Any,
    loaded: Any,
    layout: Any,
) -> dict[str, Any]:
    """The record's first line: the files verbatim with their digests, the board, the kinds with their characters, the trains with their windings (a train's winding the drive's dial at its first row, so the square's card reads its 00 row's, senses, while its 0i and jk rows run at 1), the edge key and square flags."""
    labels = [train["name"] for train in universe["trains"]]
    traits = zip(kinds._fields, kinds, characters(kinds), strict=True)
    return {
        "kind": "header",
        "record": record.name,
        "version": schema.VERSION,
        "engine": "tensor24",
        "runner": "synchronous",
        "files": [{"name": path.name, "text": text, "digest": digest(text)} for path, text in files],
        "sides": shape,
        "order": ORDER,
        "kinds": [
            {"index": at, "label": name.upper(), "dimension": kind.shape[-1], "characters": trace}
            for at, (name, kind, trace) in enumerate(traits)
        ],
        "trains": [
            {
                "index": at,
                "label": label,
                "kinds": list(train.kinds),
                "part": train.part,
                "winding": layout.gearing.drive[train.first, 0],
                "key": layout.click.key.reshape(len(labels), -1)[at, 0],  # the edge key, every side's
                "square": train.square,
            }
            for at, (label, train) in enumerate(
                zip(labels, (loaded.trains[n] for n in range(len(labels))), strict=True)
            )
        ],
        "operands": list(OPERANDS),
        "width": universe["integers"]["width"],
        "dial": layout.click.key[0, 0],  # the edge dial D, every side's key
    }


def run(engine: Engine, paths: list[Path], record: Path) -> list[str]:
    """The three files run to the record at its path and the ledger beside it, every Node-clock in every round, every departure named and nothing written past one."""
    found = departures(*paths)
    if found:
        return found
    files = [(path, path.read_text(encoding="utf-8")) for path in paths]
    universe, piece, setting = (json.loads(text) for _, text in files)
    shape = piece["shape"]
    kinds, tables, square, lifted = engine.made(star(len(shape)))
    found = held_departures(universe, setting, vocabulary(kinds, square, lifted))
    if found:
        return found
    loaded, found = load(universe, setting, sites_of(shape), kinds, tables, square, lifted)
    if found:
        return found
    layout = engine.layout(universe, shape, loaded)
    start = engine.state(*loaded.state)
    ticks, end, ledger = setting["ticks"], start, ledger_of(record)
    # every promise is the round's that reads the state: none where no round runs
    width = universe["integers"]["width"]
    found = promised(engine, layout, start, width) if ticks else []
    if found:
        return [f"round 1: {line}" for line in found]
    events: list[dict[str, Any]] = []
    # the edges the structure lays, a chosen 0 their factor alone (MIN1's (c)): the Mesh's by its plan at strength 1
    built = engine.layout(universe, shape, loaded._replace(mesh=loaded.meshed)).click
    partners, edges = joined(layout.click, len(loaded.trains)), crossed(built, len(loaded.trains))
    with ledger.open("w", encoding="utf-8") as counted:
        for at, (end, clicks) in enumerate(rounds(engine.act, layout, start, ticks), start=1):
            counted.writelines(json.dumps(line) + "\n" for line in counts(at, end, loaded.trains))
            events += clicked(at, clicks, partners, layout.nb)
            # the promises of the round that reads this state, read from outside: every kept tooth within its
            # teeth, the grips within the window, and every count within the width; the end state, which no round
            # reads, its width alone, so that a count past the width in the last round is named too
            found = promised(engine, layout, end, width) if at < ticks else wide(end, width)
            if found:
                ledger.unlink()
                return [f"round {at + 1}: {line}" for line in found]
    exact = int(stated(rewind(engine.untick, layout, end, ticks)) == stated(start))
    lines = [
        header(record, files, universe, shape, kinds, loaded, layout),
        *events,
        {
            "kind": "end",
            "rounds": ticks,
            "digest": digest(stated(end)),
            "undone": ticks,
            "exact": exact,
            # each edge side (t, u) at its own Node-clock; each Mesh edge side (Spoke, t, u), its partner's place
            # across the Spoke at every Node-clock: the structure's edges, no tooth
            "edges": [[t, u] for t, us in enumerate(partners) for u in us],
            "across": [[t, u, layout.nb[x].tolist()] for x, t, u in edges],
        },
    ]
    record.write_text("".join(json.dumps(line) + "\n" for line in lines), encoding="utf-8")
    return []
