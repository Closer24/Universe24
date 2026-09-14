"""Standalone nonlocal singlet reference, unavailable to ordinary Simulation.

This historical candidate queries a world-wide mutable registry. Its supplied
conditional law is not derived from local ray transport, and no-signalling has
not been established for every lifecycle or repeated query. The unbounded
history, finite birth-code collisions and nontransactional draws exclude it
from the ordinary physical planner. The existing explicit quantum owner is
separate and unchanged. See docs/SPATIAL_FIELDS.md for the integration boundary.
"""

from __future__ import annotations

from event_universe.core.integer import checked_work
from event_universe.core.spatial_state import (
    PHASE_COSINE_SCALE,
    TICKET_MODULUS,
    next_ticket,
    phase_cosines,
    ticket_draw,
)


class BondRegistry:
    """The joint outcomes of bonded pairs, drawn once for both ends."""

    def __init__(self, seed: int, phase_steps: int) -> None:
        if type(seed) is not int or not 0 <= seed < TICKET_MODULUS:
            raise ValueError("bond seed must be below the ticket modulus")
        self.state = seed
        self.phase_steps = phase_steps
        self.first: dict[int, tuple[int, int]] = {}
        self.questions = 0

    def draw(self, bond: int, setting: int, salt: int) -> int:
        """+1 (take the ray) or -1 (leave it) for this end of the bond at this setting."""
        if bond <= 0:
            raise ValueError("a bond must be a positive integer")
        self.state = next_ticket(self.state, (salt + bond) % TICKET_MODULUS)
        self.questions += 1
        draw = ticket_draw(self.state)
        if bond not in self.first:
            outcome = 1 if checked_work(2 * draw) < TICKET_MODULUS else -1
            self.first[bond] = (setting % self.phase_steps, outcome)
            return outcome
        first_setting, first_outcome = self.first[bond]
        difference = (setting - first_setting) % self.phase_steps
        cosine = phase_cosines(self.phase_steps)[difference]
        # The singlet: the two ends agree with probability (1 - cos) / 2.
        agree = checked_work(draw * 2 * PHASE_COSINE_SCALE) < checked_work(
            (PHASE_COSINE_SCALE - cosine) * TICKET_MODULUS
        )
        return first_outcome if agree else -first_outcome
