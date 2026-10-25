"""bh2's FLAGGED COPY of the engine's Node (src_e5, the merged head d752d586f, never edited): a subclass with the one key `frozen` read from the world file's `control` (the engine's loader refuses the key; this file strips it as David's toy.py strips its controls).
`frozen` absent or "law": the engine's path bit for bit (every call passes to the Node). `frozen` = "wall" (the form (a') of the report): a Link with a frozen end (the Link pace 0 at either end, read from the start content) is at the wall, its factor 0 read the same from both ends, so the frozen Node is read by no neighbour (R_ji = 0 at them too) and reads nothing; no book (the factors are read from the start levels in both directions as every factor is). `frozen` = "hold+wall": both. `frozen` = "hold" (the form (a) of the brief, the clock stopped): a Node whose Link pace is 0 at the interval's start (the frozen content) ends the interval in the state it started from on every line (levels, rotation remainders, write remainders, the riding wall) and its proper count rests; its neighbours read its frozen levels through their own reaches as before (the one-way valve); no act of its own, no write into it, no click (the close skips it already). The frozen mask of each interval is kept beside the swap's turned mask for the run back (a BOOK: the identity on the pair (now, before) is no bijection without it, ALGEBRA.md What it carries, derived); backward the mask is popped, the frozen Nodes' start level is read from their now slot (set into the before slot for the inverse's reads, every other Node's inverse unchanged), and their state is restored after. Integers only."""
from __future__ import annotations

import os
import sys
from typing import Any

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, 'src_e5', 'src'))
import numpy as np

from event_universe import run
from event_universe.core import paces
from event_universe.loader.world import read_world
from event_universe.node import Node
from event_universe.rows import CARRIER

CONTROLS = ('control',)


def load_flagged_world(path: str):
    import json
    from pathlib import Path
    where = Path(path)
    world = json.loads(where.read_text(encoding='utf-8'))
    universe = json.loads((where.parent / world['universe']).read_text(encoding='utf-8'))
    read_world({k: v for k, v in world.items() if k not in CONTROLS}, universe)
    return universe, world


class Flagged(Node):
    def __init__(self, universe: dict[str, Any], world: dict[str, Any]) -> None:
        self.form = world.get('control', {}).get('frozen', 'law')
        self.frozen_stack: list[Any] = []
        self.frozen_count = 0
        self.direction_level = None
        super().__init__(universe, {k: v for k, v in world.items() if k not in CONTROLS})

    def link_factors(self, axis_levels: list[Any] | None = None) -> tuple[Any, ...]:
        found = super().link_factors(axis_levels)
        if 'wall' not in self.form:
            return found
        from event_universe.core.ports import across
        from event_universe.features import volume
        carrier = self.row(CARRIER).lines[0]
        level = carrier.now if self.direction_level is None else self.direction_level
        c = np.asarray(volume.level_of(self.gamma, level), dtype=object)
        mask = np.asarray(paces.link_pace_of(self.gamma, c), dtype=object) == 0
        return tuple(np.where(mask | across(mask, port), 0, f) for port, f in enumerate(found))

    def frozen_mask(self) -> Any:
        pace = paces.link_pace_of(self.gamma, self.content())
        return np.asarray(pace, dtype=object) == 0

    def restore_at(self, mask: Any, saved: list[list[Any]], proper: Any) -> None:
        for line, h in zip(self.all_lines(), [l for row in saved for l in row], strict=True):
            line.now = np.where(mask, h.now, line.now)
            line.before = np.where(mask, h.before, line.before)
            line.rem = np.where(mask, h.rem, line.rem)
            if np.ndim(h.wall):
                line.wall = np.where(mask, h.wall, line.wall)
            if line.wr is not None:
                line.wr = np.where(mask, h.wr, line.wr)
        self.proper = np.where(mask, proper, self.proper)

    def run(self, direction: int = 1) -> None:
        if 'hold' not in self.form:
            if 'wall' in self.form and direction == -1:
                self.direction_level = self.row(CARRIER).lines[0].before
                try:
                    return super().run(direction)
                finally:
                    self.direction_level = None
            return super().run(direction)
        if direction == 1:
            self.mask = self.frozen_mask()
            self.proper0 = self.proper.copy()
            self.frozen_count += int(self.mask.sum())
            super().run(1)
            self.frozen_stack.append(self.mask)
            return
        mask = self.frozen_stack.pop()
        saved = [[l.copy() for l in row] for row in self.rows()]
        proper0 = self.proper.copy()
        for line in self.all_lines():
            line.before = np.where(mask, line.now, line.before)
        self.direction_level = self.row(CARRIER).lines[0].before
        try:
            super().run(-1)
        finally:
            self.direction_level = None
        self.restore_at(mask, saved, proper0)

    def click(self, plane_starts: list[list[Any]], held: list[list[Any]]) -> None:
        if 'hold' in self.form and self.mask.any():
            self.restore_at(self.mask, held, self.proper0)
            self.turned[self.mask] = False
        super().click(plane_starts, held)


def main(argv: list[str]) -> None:
    sys.set_int_max_str_digits(0)
    universe, world = load_flagged_world(argv[1])
    back = int(argv[argv.index('back') + 1]) if 'back' in argv else 0
    run.Node = Flagged  # type: ignore[misc]
    found = run.record(universe, world, back, lambda line: print(line, flush=True))
    import json
    with open(argv[2], 'w', encoding='utf-8') as out:
        json.dump(found, out)


if __name__ == '__main__':
    main(sys.argv)
