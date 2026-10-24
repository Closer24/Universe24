"""The lay's numbers of the chain worlds, read from the loaded worlds before any run (the click's plan, B2 and B3: the bounds written as the blind's numbers before the run): per world the light's unit W_rec (C1), its share and its count at the lay (the books), and per body its Nodes, the lay's amplitudes, D4's bound on |dP_a| per axis at a re-lay, SUM over the body's axis-Links of (|now_i| + |before_i| + |now_j| + |before_j| + 2) over the record's lines (at most one level's change per line and Node), in T's unit as the credit line reads the piece (`take.scaled`) and times num in the current's unit, and per transition the declared weight beside the weight from the unit (C9 (a), `resonance.unit_weight`: the phase line's quarter turn over S_1, the two integers); written to `lay_bounds.json` beside the worlds. No interval is stepped: the lay alone is read. A host tool: it holds no number of the law and writes nothing to the engine.

PYTHONPATH=src python examples/events/chain/lay_bounds.py [--folder <folder>]
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np

from event_universe.features.phase import quarter_turn
from event_universe.lattice import Lattice
from event_universe.resonance import unit_weight
from event_universe.world_files import load_world

HERE = Path(__file__).resolve().parent


def body_bound(board: Lattice, books) -> tuple[list[int], list[int]]:  # type: ignore[no-untyped-def]
    """D4's bound per axis for one body at the lay, in T's unit: over the Links along the axis with an end at a body Node (a Link to the Node itself across a folded axis is no Link) and over the record's lines, |now_i| + |before_i| + |now_j| + |before_j| + 2; and the Links' count per axis, for the amplitude form (`amplitude_form`)."""
    lines = board.lines_of(books.index, books.record)
    nodes = [tuple(int(v) for v in np.add(node, board.offset)) for node in books.nodes]
    found, counts = [], []
    for axis in range(3):
        links = set()
        for here in nodes:
            for step in (-1, 1):
                there = list(here)
                there[axis] += step
                if board.world.periodic[axis]:
                    there[axis] %= board.shape[axis]
                elif not 0 <= there[axis] < board.shape[axis]:
                    continue
                if tuple(there) != here:
                    links.add(frozenset((here, tuple(there))))
        total = 0
        for link in links:
            for at in link:
                total += sum(abs(int(r.now[at])) + abs(int(r.before[at])) for r in lines)
            total += 2 * len(lines)
        found.append(total)
        counts.append(len(links))
    return found, counts


def amplitude_form(amplitude: int, links: list[int], lines: int) -> list[int]:
    """D4's bound in the amplitude form, per axis in T's unit (the cold reader's line of 2026-10-19): 4 A + 2 per line of the part per Link along the axis, A the body's lay amplitude at a Node, the bound of a re-lay at any phase (|re| + |im| up to sqrt 2 larger than the lay's phase-0 value, which `body_bound` reads)."""
    return [count * lines * (4 * amplitude + 2) for count in links]


def lay_of(path: Path) -> dict:
    """One world's lay: the light's books and unit, and per body its Nodes, amplitudes and D4's bound."""
    board = Lattice(load_world(path))
    light = next(i for i, f in enumerate(board.families) if f.name == "photon")
    quarter, action = quarter_turn(board.amplitude, board.world.node_clock), board.world.quantum_action
    bodies = []
    for books in board.credit.bodies:
        family = board.families[books.index]
        num, (bound, links) = family.pair[0], body_bound(board, books)
        form = amplitude_form(max(books.amplitudes), links, family.width)
        window, transitions = books.declared.draw.window, books.declared.transitions
        bodies.append(
            {
                "body": books.number,
                "nodes": [list(node) for node in books.nodes],
                "amplitudes": list(books.amplitudes),
                "D4_bound_T_unit": bound,
                "D4_bound_current_unit": [num * b for b in bound],
                "D4_amplitude_form_T_unit": form,
                "links_along_axis": links,
                "weight_declared": [t.weight for t in transitions],
                "weight_from_the_unit": [
                    unit_weight(quarter, window, action, board.families[t.drive].pair, t.resonance)
                    for t in transitions
                ],
            }
        )
    return {
        "world": path.stem,
        "light": {"unit_W_rec": board.credit.units[light], **board.books()["photon"]},
        "bodies": bodies,
    }


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--folder", type=Path, default=HERE)
    args = parser.parse_args(argv)
    design = json.loads((args.folder / "design.json").read_text(encoding="utf-8"))
    names = list(design["worlds"])
    found = [lay_of(args.folder / f"{name}.json") for name in names]
    (args.folder / "lay_bounds.json").write_text(json.dumps(found, indent=1) + "\n", encoding="utf-8")
    for entry in found:
        print(json.dumps(entry))


if __name__ == "__main__":
    main()
