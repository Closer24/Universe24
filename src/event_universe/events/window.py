"""The window out of the loop's module: THE WINDOW WRITES BOTH LEVELS (the body's rotation set at the giver's Nodes on both levels, the pair g q M(n) over E_s, the interval's outward reading), and THE CLOSE RETURNS THE CURRENT (the zero mode's velocity B taken off the given record on its support, both remainders carried at the giver); Cheshbon's lines of 2026-09-28, 12:23, 13:16 and 13:27 Israel."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

import numpy as np

from event_universe.core.rule3 import division_forward
from event_universe.events import after_step
from event_universe.events.records import Block, LiveRecord
from event_universe.features.giving import THE_CLOSE, GivingStart, GivingTerm

if TYPE_CHECKING:
    from event_universe.events.detector_law import DetectorLawSimulation


def giving_coupling(loop: DetectorLawSimulation, block: Block, emitter: Any) -> tuple[np.ndarray, int]:
    """The window's write as a pair (Cheshbon's lines of 2026-09-28, 13:16 and 13:27 Israel): at every Node of the giver the numerator g q M(n), the emitter's weight g times the body's sign q (its key `q`, +1 or -1; a body with no sign gives no light) times the body's count there, over the given family's divisor E_s (over 1 where the given family holds nothing)."""
    weight = emitter.weight if emitter.weight is not None else 1
    counts = np.array(
        [count for _node, count in loop.node_sources(block.number, "content")], dtype=np.int64
    )
    if counts.shape[0] != int(np.count_nonzero(block.mask)):
        counts = np.full(
            int(np.count_nonzero(block.mask)), loop.body_source(block.number, "content"), dtype=np.int64
        )
    if block.definition.q == 0:
        raise ValueError(
            f"the body {block.number} gives {loop.families[emitter.family].name!r} with no sign q: a neutral body gives no light (Cheshbon's line of 2026-09-28, 13:27 Israel); declare `q` on the giver"
        )
    divisor = loop.families[emitter.family].held_divisor
    return weight * block.definition.q * counts, divisor or 1


def zero_mode(loop: DetectorLawSimulation, block: Block, live: LiveRecord) -> None:
    """THE CLOSE RETURNS THE CURRENT (Cheshbon's lines of 2026-09-28, 12:23 and 13:16 Israel; the click the law's one non-local act, ALGEBRA.md #the-primitives): at the close the zero mode's velocity B = (SUM q_n (now_n - before_n) + r) div SUM q_n over the record's support, q_n = ((Gamma 2^8)^2 + r') div p_n^2 the weight of the Node's pace p_n = Gamma - c_n, both remainders carried at the giver; now -= B on the support, booked on the giving line and kept on the record for the inverse."""
    gamma = int(loop.node_clock)
    support = (live.now != 0) | (live.before != 0)
    content = loop._effective_content(live.family)
    carries = block.close_carry
    unit = (gamma << 8) * (gamma << 8)
    weights = np.zeros(loop.shape, dtype=np.int64)
    weight_carry = carries[0]
    for node in zip(*np.nonzero(support), strict=True):
        pace = gamma - int(content[node])
        weights[node], weight_carry = division_forward(unit, pace * pace, weight_carry)
    total = int(weights.sum())
    velocity, mode_carry = 0, carries[1]
    if total > 0:
        current = int(
            (weights.astype(object) * (live.now.astype(object) - live.before.astype(object))).sum()
        )
        velocity, mode_carry = division_forward(current, total, carries[1])
        count = int(np.count_nonzero(support))
        loop._write_at_mask(
            live,
            support,
            (np.full(count, velocity, dtype=np.int64), np.zeros(count, dtype=np.int64)),
            -1,
        )
    live.zero_mode, block.close_carry = (int(velocity), support, carries), (weight_carry, mode_carry)
    if live.giving_line is not None:
        live.giving_line["zero_mode"] = int(velocity)  # booked on the giving line, the click's books


def giving_term(loop: DetectorLawSimulation, block: Block, emitter: Any) -> GivingTerm:
    """The window's term: the write's pair at the giver's Nodes and the quantum action T (the emitter's norm over its denominator until the loader reads the universe's T)."""
    norm = emitter.norm if emitter.norm is not None else 1
    denominator = emitter.norm_denominator if emitter.norm_denominator is not None else 1
    return GivingTerm(
        giving_coupling(loop, block, emitter), division_forward(norm, denominator, 0)[0], emitter.family
    )


def point_windows(loop: DetectorLawSimulation) -> None:
    """The point emitters' windows closed after the interval's bookings: the given record's norm, residue and wheel fixed from what left the body, the window's count and the record's box settled, the giving line written."""
    for block in loop.blocks:
        if block.window is None:
            continue
        live = loop.records.get(block.window)
        emitter = after_step.emitter_of(block)
        if live is None or emitter is None or emitter.weight is None or emitter.norm is None:
            block.window = None
            continue
        if live.clicked:
            # taken while its window was open (its own body's Node's set reading the returning light, the light clock): the window closes at the click, the record named
            loop._close_window(block, live)
            continue
        # (d) the close: the folder's close act on the outward norm summed over the window
        if loop._giving_act(
            block, GivingStart(THE_CLOSE, 0, (0, 0, 0), None, 0, (0, 0, 0)), live
        ).closed:
            loop._close_window(block, live)
