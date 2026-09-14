"""Bonded pairs: the declared exception to the causal bound, one number per pair.

Two rays emitted together share a bond, the code of their birth Node and tick.
When a detector takes a bonded ray it does not draw a local ticket: it asks the
bond registry, which holds the pair's joint outcome. The pair's one number is a
fixed function of the registry seed and the bond; its upper half answers the
first end evenly, and its lower half, read against the difference of the two
settings, decides whether the second end agrees, with the singlet's law that
the two answers agree with probability sin^2 of half the difference. The
registry is one object for the whole world, so the second answer knows the
first at once, at any distance: that is the one influence that skips Nodes.
It carries no energy, no momentum and no message, since each end alone sees an
even coin, so postulate 4 keeps its hold on everything physical.

The registry's state is bounded: it holds at most MAX_OPEN_BONDS pairs whose
first end has answered and whose second has not, and releases a pair at its
second answer. A question repeated by the same end with the same setting gets
the same answer, so a proposal that is prepared twice does not move the
registry. Every number is a bounded integer.
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

MAX_OPEN_BONDS = 4096


class BondRegistry:
    """The joint outcomes of bonded pairs, one number per pair, a bounded open bank."""

    def __init__(self, seed: int, phase_steps: int) -> None:
        if type(seed) is not int or not 0 <= seed < TICKET_MODULUS:
            raise ValueError("bond seed must be below the ticket modulus")
        self.seed = seed
        self.phase_steps = phase_steps
        # bond -> (asking end's salt, its setting, its outcome, the pair's number)
        self.open: dict[int, tuple[int, int, int, int]] = {}
        self.questions = 0
        self.numbers = 0
        self.released = 0

    def number(self, bond: int) -> int:
        """The pair's one number: a fixed function of the seed and the bond."""
        if bond <= 0:
            raise ValueError("a bond must be a positive integer")
        salt = bond % TICKET_MODULUS
        # Two salted steps with a square between them: consecutive bonds, which are
        # consecutive birth codes, must not draw numbers that move together.
        state = ticket_draw(next_ticket(self.seed, salt))
        return ticket_draw(next_ticket(state, salt))

    def draw(self, bond: int, setting: int, salt: int) -> int:
        """+1 (take the ray) or -1 (leave it) for this end of the bond at this setting."""
        number = self.number(bond)
        self.questions += 1
        setting %= self.phase_steps
        salt %= TICKET_MODULUS
        entry = self.open.get(bond)
        if entry is None:
            if len(self.open) >= MAX_OPEN_BONDS:
                raise OverflowError("the bond registry holds at most 4096 open pairs")
            self.numbers += 1
            outcome = 1 if checked_work(2 * number) < TICKET_MODULUS else -1
            self.open[bond] = (salt, setting, outcome, number)
            return outcome
        first_salt, first_setting, first_outcome, _ = entry
        if salt == first_salt and setting == first_setting:
            # The same end asks again: the deposit is idempotent.
            return first_outcome
        difference = (setting - first_setting) % self.phase_steps
        cosine = phase_cosines(self.phase_steps)[difference]
        # The singlet: the two ends agree with probability (1 - cos) / 2, decided by
        # the lower half of the same number, independent of the coin in its upper half.
        rest = checked_work(2 * number) % TICKET_MODULUS
        agree = checked_work(rest * 2 * PHASE_COSINE_SCALE) < checked_work(
            (PHASE_COSINE_SCALE - cosine) * TICKET_MODULUS
        )
        del self.open[bond]
        self.released += 1
        return first_outcome if agree else -first_outcome
