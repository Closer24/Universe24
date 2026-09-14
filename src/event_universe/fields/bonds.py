"""Bonded pairs: the declared exception to the causal bound, one number per pair.

Two rays emitted together may share a bond. When a detector takes a bonded ray
it does not draw a local ticket: it asks the bond registry, which holds the
pair's joint outcome. The first question on a bond draws one bounded integer;
its upper half answers that end evenly. The second question, at another
setting, draws nothing: the same integer's lower half answers it, conditioned
on the first, with the singlet's law that the two answers agree with
probability sin^2 of half the difference of the settings. One number decides
the pair, whichever end asks first. The registry is one object for the whole
world, so the second answer knows the first at once, at any distance: that is
the one influence that skips Nodes. It carries no energy, no momentum and no
message, since each end alone sees an even coin, so postulate 4 keeps its
hold on everything physical. Every number is a bounded integer.
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
    """The joint outcomes of bonded pairs, one number drawn for both ends."""

    def __init__(self, seed: int, phase_steps: int) -> None:
        if type(seed) is not int or not 0 <= seed < TICKET_MODULUS:
            raise ValueError("bond seed must be below the ticket modulus")
        self.state = seed
        self.phase_steps = phase_steps
        self.first: dict[int, tuple[int, int, int]] = {}
        self.questions = 0
        self.numbers = 0

    def draw(self, bond: int, setting: int, salt: int) -> int:
        """+1 (take the ray) or -1 (leave it) for this end of the bond at this setting."""
        if bond <= 0:
            raise ValueError("a bond must be a positive integer")
        self.questions += 1
        if bond not in self.first:
            # The pair's one number: its upper half is this end's even coin, its
            # lower half is kept for the other end.
            self.state = next_ticket(self.state, (salt + bond) % TICKET_MODULUS)
            self.numbers += 1
            number = ticket_draw(self.state)
            outcome = 1 if checked_work(2 * number) < TICKET_MODULUS else -1
            self.first[bond] = (setting % self.phase_steps, outcome, number)
            return outcome
        first_setting, first_outcome, number = self.first[bond]
        difference = (setting - first_setting) % self.phase_steps
        cosine = phase_cosines(self.phase_steps)[difference]
        # The singlet: the two ends agree with probability (1 - cos) / 2, decided by
        # the lower half of the same number, independent of the coin in its upper half.
        rest = checked_work(2 * number) % TICKET_MODULUS
        agree = checked_work(rest * 2 * PHASE_COSINE_SCALE) < checked_work(
            (PHASE_COSINE_SCALE - cosine) * TICKET_MODULUS
        )
        return first_outcome if agree else -first_outcome
