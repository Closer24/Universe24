"""Tensor24's algebra: Rule3's carry, the one division with its remainder kept, the fine tooth's flip and the whether."""

import numpy as np

from tensor24.algebra.carry import carry, flip, lit


def numbers():
    """Whole numbers across 0 and past 2**112, every teeth count from 1 at both parities, as Python integers."""
    rng, edges = np.random.default_rng(20261028), [-(1 << 112) - 7, (1 << 112) + 5, -1, 0, 1]
    n = [int(x) for x in rng.integers(-(1 << 40), 1 << 40, size=300)] + edges
    d = [int(x) for x in rng.integers(1, 40, size=len(n))]
    r = [int(x) for x in rng.integers(-50, 50, size=len(n))]
    return [np.array(v, dtype=object) for v in (n, d, r)]


def test_the_carry_turns_the_dial_on_a_whole_turn_and_keeps_the_rest_short_of_one():
    """Yes: n + r = q d + r' with 0 <= r' < d, on integers and arrays alike, and the tie rule, the flip its own inverse.
    No: a push one notch short of a turn carries nothing and keeps itself; the whether is 0 at 0 alone."""
    n, d, r = numbers()
    q, kept = carry(n, d, r)
    # the third review (81521e0f4): a quotient through a float passed at a few teeth; these run past 2**112
    assert (q * d + kept == n + r).all() and ((kept >= 0) & (kept < d)).all()
    assert all(carry(*v) == (a, b) for v, a, b in zip(zip(n, d, r, strict=True), q, kept, strict=True))
    tooth = carry(r, d, 0)[1]  # a fine tooth within its teeth
    q, kept = carry(n, d, tooth)
    negated, flipped = carry(-n, d, flip(tooth, d))
    assert (negated == -q).all() and (flipped == flip(kept, d)).all()
    assert (flip(flip(tooth, d), d) == tooth).all()
    short, held = carry(d - 1 - tooth, d, tooth)
    assert not short.any() and (held == d - 1).all() and (carry(d - tooth, d, tooth)[0] == 1).all()
    assert (lit(n) == (n != 0)).all()
