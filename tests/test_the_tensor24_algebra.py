"""Tensor24's algebra: Rule3's carry and the fine tooth's flip, each law holding and failing on its own mutant."""

from types import SimpleNamespace

import numpy as np

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
    """The tie rule: a carry negated, its fine tooth flipped, negates the quotient and flips the tooth it keeps."""
    n, d, r = numbers()
    tooth = algebra.carry(r, d, 0)[1]
    q, kept = m.carry(n, d, tooth)
    q2, kept2 = m.carry(-n, d, m.flip(tooth, d))
    return (q2 == -q).all() and (kept2 == m.flip(kept, d)).all()


def involution(m):
    """The flip stays within the teeth and, twice, is the identity."""
    _, d, r = numbers()
    tooth = algebra.carry(r, d, 0)[1]
    once = m.flip(tooth, d)
    inside = ((once >= 0) & (once < d)).all() and (m.flip(0 * d, d) < d).all()
    return inside and (m.flip(once, d) == tooth).all()


def carry_mutants():
    """One broken copy of the algebra per law, each changing one thing the law must see."""
    return {
        "exact": {
            "carry": lambda n, d, r: (
                -((-(n + r)) // d),
                (n + r) + ((-(n + r)) // d) * d,
            )
        },
        "odd": {"flip": lambda r, w: r},
        "involution": {"flip": lambda r, w: w - r},
    }


CARRY = {"exact": exact, "odd": odd, "involution": involution}


def holds(laws, module, mutants):
    """Every law holds on the module and fails on its own mutant, the module's other parts kept."""
    broken = {name: SimpleNamespace(**{**vars(module), **mutants[name]}) for name in laws}
    return all(law(module) and not law(broken[name]) for name, law in laws.items())


def test_the_carry_keeps_its_laws_and_each_mutant_breaks_its_own():
    assert holds(CARRY, algebra, carry_mutants())
