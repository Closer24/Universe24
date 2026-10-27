"""The one act beneath Rule3 and its three names (NL-S1, 2026-10-26, the Boss's approval under the owner's delegation of 08:3x UTC; H-Node-Beneath-Rule3-1 and -2, both hands one core): the clock adds; each gear holds one number w a + r, and every act of the clock on a gear is the carry of a sum it reads, at a slot, in a going (`carry`, the former rule3.carried_division kept by name), the two slots reversed with the fine tooth's flip (`reverse`, the turnover at the top) or the advance of a count on a slot (`advance`); the flip w - 1 - r once per reversal of the gear (`flip`, the former rule3.mirrored) is the one asymmetric letter (CA-S1: the direction is the slot). Rule3's step, the drive, the unwind's move and advance, the driven gears' carries and the turnover are their compositions; integers or integer arrays over the whole great clock alike, no name, no number, no branch on a train's kind."""

from __future__ import annotations

from typing import Any


def flip(fine: Any, teeth: Any, reversals: int) -> Any:
    """The one rule of the fine tooth's flip (fd1's form, the owner's word of 2026-10-25): a fine tooth born at the half teeth of its carry (`mid`) is flipped to teeth - 1 - r once for every reversal of its gear (time's reverse, the sign's negation), two reversals leaving it; the identity for an even count. A fine tooth has two flips and this is the going's (The-48-Holds_COMPARISON.md, 2026-10-26, F48-S1 derived and not built): the flip of a negated gear, a reflection or a sweep's negation, is the two's complement (teeth - r) mod teeth, one apart at every nonzero fine tooth, whose fixed point at even teeth is the mid tooth; the acts spell the going's alone until F48-S1 is built."""
    return teeth - 1 - fine if reversals & 1 else fine


def mid(teeth: Any) -> Any:
    """The fine tooth every gear is born with, the half teeth by the carry on 2 (the engine's one mid tooth, spelt once; the former half(wall) at the trains' gears, the driven teeth, the driven carry, the standard and the vernier's origin kept by name): the fixed point of the negated gear's flip, (teeth - r) mod teeth = r, at even teeth, which the going's flip teeth - 1 - r sends to the half teeth less one; so the mid tooth fits the negation's flip and not the going's, the third spelling the 48's pair named (The-48-Holds_COMPARISON.md section 5, 2026-10-26)."""
    return carry(teeth, 2, 0)[0]


def carry(total: Any, teeth: Any, fine: Any, going: int = 1) -> tuple[Any, Any]:
    """The one carry of the law (ALGEBRA.md #the-four-acts, #the-direction): u = total + r, the carries u div w and the fine tooth u mod w kept in [0, w) for a total of either sign; the act at -1 is the act at +1 conjugated by the fine tooth's flip, written once (CA-S1, the owner's word of 2026-10-26, 07:04 UTC: the direction is the slot; RW-S1)."""
    carried = total + flip(fine, teeth, going == -1)
    carries = carried // teeth
    return carries, flip(carried - teeth * carries, teeth, going == -1)


def reverse(
    nows: list[Any], befores: list[Any], fines: list[Any], train_teeth: list[Any], signs: list[int]
) -> tuple[list[Any], list[Any], list[Any]]:
    """The two slots of a train reversed at the top with the flip (X2, the turnover; Clock.reverse): the two slots exchanged through the train's reflection K (the hand's twelve-o'clock gear negated), the fine tooth flipped once for time's reverse and once more where its own K entry negates the gear; an involution."""
    new_nows = [s * b for s, b in zip(signs, befores, strict=True)]
    new_befores = [s * n for s, n in zip(signs, nows, strict=True)]
    return (
        new_nows,
        new_befores,
        [flip(f, w, 1 + (s < 0)) for f, w, s in zip(fines, train_teeth, signs, strict=True)],
    )


def advance(slot: Any, count: Any, going: int = 1) -> Any:
    """The advance: a count of notches advanced on one slot in the going (the drive's carries, the unwind's move, the setting's, the fitted hands' and the release's advances, each undone at -1)."""
    return slot + going * count
