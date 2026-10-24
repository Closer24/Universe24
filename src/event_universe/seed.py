"""The uniform seed is a lay (ALGEBRA.md, The uniform seed is a lay, the owner's word of 2026-10-24, the fold: a world of the universe, the board's shape and the run's length alone, no body, no detector, no option key): a world that declares nothing is seeded by the engine with the universe's one massless family of quanta at one quantum on every Node of the torus (`loader/seed.seed_of`, refused by name where the universe holds none or more than one), laid before the start by the one lay act (`lay.laid`, no weights: the uniform part IS the lay, as a one-Node lay's is) on every line of the family's first record alike (`emission.emitted_lines`), the level now the drift v and the level before 0 at every Node, v the largest integer with v^2 <= T: the massless uniform mode is a double root whose share per Node in the vacuum is 3 den (now - before)^2 (share.py, the vacuum's form exactly), so one quantum, W_rec = 3 den T, is the drift v^2 <= T to the integer, the level itself a gauge no act reads; the start then solves every held row's rest from this record's form as from any laid record (features/start, the former start from the laid records kept by name) and no iteration is spent on the lay itself, a uniform state being its own fixed point under Rule3 (every Link's two ends alike, the Links' sum 0), the remainder at the half wall, the lay's origin; the seed's own count in the books is its share read at the start (`credit.Books.of`), one quantum per Node."""

from __future__ import annotations

from typing import TYPE_CHECKING

from event_universe import records
from event_universe.core.rule3 import largest_below
from event_universe.emission import emitted_lines
from event_universe.lay import laid

if TYPE_CHECKING:
    from event_universe.lattice import Lattice

ORIGIN = (
    0,
    0,
    0,
)  # the lay's origin, the one Node of the torus with no quantum of the seed (every Node the origin under the roll)


def drift_of(action: int) -> int:
    """One quantum's drift of the massless uniform mode, the largest integer v with v^2 <= T (the share 3 den v^2 against the unit 3 den T, the count's rounding to one), by the search on comparisons alone."""
    return largest_below(action)


def uniform_seed(board: Lattice, index: int) -> None:
    """The seed laid (ALGEBRA.md, The uniform seed is a lay, the closure of 2026-10-24 on the owner's directive, "nothing is to be left open; everything must close and match nature"): every line of the first record of the family `index` at the level now v and the level before 0 on every Node of the torus but one, the lay's origin, the Node `ORIGIN`, where no quantum is laid; the uniform sea, the law's seed to 2026-10-24, births nothing (the builder's finding: a sea alike at every Node has no digits for the draw, and the shipped births were the declared row's), and the hole parts the Nodes at the first interval and opens the draw, which births the pairs the law gives; on the torus every Node is the origin under the roll and the draw reads the Node's own frame, so no label enters a number, and the hole seed's run is the rolled run bit for bit; through the one lay act with no weights and the remainder left at the lay's origin."""
    family = board.families[index]
    drift = drift_of(board.world.quantum_action)
    now = records.full(board.shape, drift, board.kind)
    now[ORIGIN] = 0  # the hole: the lay's origin carries no quantum
    before = records.zeros(board.shape, board.kind)
    first = records.record_slice(family, 0).start
    for line in emitted_lines(family):
        laid(board, index, first + line, (now, before), None, None)
