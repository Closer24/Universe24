"""Tensor24's algebra: Rule3's carry and the whethers made of it, each law failing on its own mutant."""

from types import SimpleNamespace

import numpy as np
import pytest

from tensor24.algebra import carry as algebra


def numbers():
    """Whole numbers across 0 and past 112 bits, every teeth count from 1 at both parities, as ints and arrays."""
    rng = np.random.default_rng(20261028)
    n = [int(x) for x in rng.integers(-(1 << 40), 1 << 40, size=300)] + [
        -(1 << 112) - 7,
        (1 << 112) + 5,
        -1,
        0,
        1,
    ]
    d = [int(x) for x in rng.integers(1, 40, size=len(n))]
    r = [int(x) for x in rng.integers(-50, 50, size=len(n))]
    return [np.array(v, dtype=object) for v in (n, d, r)]


def exact(m):
    """n + r = q d + r' with 0 <= r' < d, on integers and on arrays of them alike."""
    n, d, r = numbers()
    q, kept = m.carry(n, d, r)
    ints = all(m.carry(*v) == (a, b) for v, a, b in zip(zip(n, d, r, strict=True), q, kept, strict=True))
    return ints and (q * d + kept == n + r).all() and ((kept >= 0) & (kept < d)).all()


def odd(m):
    """The tie rule: negating a gear, its fine tooth flipped and its going advanced, negates the carry's quotient."""
    n, d, _ = numbers()
    for go in (0, 1):
        q, kept = m.carry(n, d, m.home(d, go))
        q2, kept2 = m.carry(-n, d, m.home(d, 1 - go))
        if not ((q2 == -q).all() and (kept2 == m.flip(kept, d)).all()):
            return False
    return True


def whether(m):
    """The bit of n at least 0, exact across 0 and at every size."""
    n, _, _ = numbers()
    return all(m.nonneg(x) == (x >= 0) for x in [*n, *range(-50, 51)])


def choice(m):
    """The bit 1 chooses x, the bit 0 chooses y."""
    n, d, _ = numbers()
    return (m.choose(1, n, d) == n).all() and (m.choose(0, n, d) == d).all()


def involution(m):
    """The flip stays within the teeth and, twice, is the identity."""
    _, d, r = numbers()
    tooth = algebra.carry(r, d, 0)[1]
    once = m.flip(tooth, d)
    inside = ((once >= 0) & (once < d)).all() and (m.flip(0 * d, d) < d).all()
    return inside and (m.flip(once, d) == tooth).all()


def mutants():
    """One broken copy of the algebra per law, each changing one thing the law must see."""
    return {
        "exact": {
            "carry": lambda n, d, r: (
                -((-(n + r)) // d),
                (n + r) + ((-(n + r)) // d) * d,
            )
        },
        "odd": {"home": lambda w, go: algebra.carry(w, 1 + 1, 0)[0]},
        "whether": {"nonneg": lambda n: algebra.carry(n, n * n + 1, 0)[0]},
        "choice": {"choose": lambda k, x, y: k * x + k * y},
        "involution": {"flip": lambda r, w: w - r},
    }


@pytest.mark.parametrize("name", ["exact", "odd", "whether", "choice", "involution"])
def test_each_law_of_the_carry_holds_and_fails_on_its_mutant(name):
    law = {
        "exact": exact,
        "odd": odd,
        "whether": whether,
        "choice": choice,
    }
    law = law | {"involution": involution}
    assert law[name](algebra)
    assert not law[name](SimpleNamespace(**{**vars(algebra), **mutants()[name]}))
