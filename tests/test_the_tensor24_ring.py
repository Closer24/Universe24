"""Tensor24's Gaussian ring: the hand's and the twin hand's laws, exact at every size, each failing on its own mutant."""

from types import SimpleNamespace

import numpy as np
import pytest

from tensor24.algebra import ring
from tests.frame import wide


def hands(seed, count=3):
    """Hands whose every coefficient's bit is drawn across 2**256, as rows of Python integers."""
    rng = np.random.default_rng(seed)
    return [(wide(rng, 64), wide(rng, 64)) for _ in range(count)]


def equal(z, w):
    """Two hands, or two rows of whole numbers, equal at every entry."""
    return all(np.array_equal(x, y) for x, y in zip(z, w, strict=True))


def ringed(m):
    """The product is commutative, associative and distributive, and i i is -1: four quarter turns are the identity."""
    z, w, v = hands(1)
    i, one = (0 * z[0], 0 * z[0] + 1), (0 * z[0] + 1, 0 * z[0])
    commutes = equal(m.mul(z, w), m.mul(w, z))
    associates = equal(m.mul(m.mul(z, w), v), m.mul(z, m.mul(w, v)))
    distributes = equal(m.mul(z, m.add(w, v)), m.add(m.mul(z, w), m.mul(z, v)))
    quarter = m.mul(i, m.mul(i, m.mul(i, m.mul(i, z))))
    return (
        commutes
        and associates
        and distributes
        and equal(m.mul(i, i), (-one[0], one[1]))
        and equal(quarter, z)
    )


def conjugate(m):
    """conj is an involution, multiplicative, and z conj(z) is real: T on a hand, its T T +1."""
    z, w, _ = hands(2)
    involution = equal(m.conj(m.conj(z)), z)
    multiplicative = equal(m.conj(m.mul(z, w)), m.mul(m.conj(z), m.conj(w)))
    return involution and multiplicative and equal(m.mul(z, m.conj(z)), (m.norm(z), 0 * z[0]))


def sized(m):
    """The norm is multiplicative: the size of a product is the product of the sizes."""
    z, w, _ = hands(3)
    return np.array_equal(m.norm(m.mul(z, w)), m.norm(z) * m.norm(w))


def paired(m):
    """conj(z) w: its real part the dot a c + b d, its imaginary part the cross a d - b c."""
    (a, b), (c, d), _ = hands(4)
    return equal(m.pair((a, b), (c, d)), (a * c + b * d, a * d - b * c))


def reversed_twice(m):
    """T T is -1 on a twin hand, and T keeps its size and turns its spin over."""
    up, down, _ = hands(5)
    psi = (up, down)
    twice = m.reverse(m.reverse(psi))
    rho, s = m.axis(psi)
    rho2, s2 = m.axis(m.reverse(psi))
    flipped = all(np.array_equal(x, -y) for x, y in zip(s2, s, strict=True))
    return (
        equal(twice[0], (-up[0], -up[1]))
        and equal(twice[1], (-down[0], -down[1]))
        and np.array_equal(rho2, rho)
        and flipped
    )


def lagrange(m):
    """The two parts of a split share the whole exactly: N<phi, psi> + N<T phi, psi> = rho_phi rho_psi."""
    a, b, c = hands(6)
    _, d, _ = hands(7)
    phi, psi = (a, b), (c, d)
    parts = m.norm(m.overlap(phi, psi)) + m.norm(m.overlap(m.reverse(phi), psi))
    return np.array_equal(parts, m.axis(phi)[0] * m.axis(psi)[0])


def axial(m):
    """A twin hand's reading has S . S = rho rho: its spin as long as its size."""
    up, down, _ = hands(8)
    rho, (x, y, z) = m.axis((up, down))
    return np.array_equal(x * x + y * y + z * z, rho * rho)


def mutants():
    """One broken copy of the ring per law, each changing one thing the law must see."""
    return {
        "ring": {"mul": lambda z, w: (z[0] * w[0] + z[1] * w[1], z[0] * w[1] + z[1] * w[0])},
        "conj": {"conj": lambda z: z},
        "norm": {"norm": lambda z: z[0] * z[0] - z[1] * z[1]},
        "pair": {"pair": lambda z, w: ring.mul(z, ring.conj(w))},
        "reverse": {"reverse": lambda psi: (ring.conj(psi[1]), ring.conj(psi[0]))},
        "lagrange": {"overlap": lambda phi, psi: ring.pair(phi[0], psi[0])},
        "axis": {
            "axis": lambda psi: (ring.axis(psi)[0], (*ring.pair(psi[0], psi[1]), ring.axis(psi)[1][2]))
        },
    }


LAWS = {"ring": ringed, "conj": conjugate, "norm": sized, "pair": paired}
LAWS |= {"reverse": reversed_twice, "lagrange": lagrange, "axis": axial}


@pytest.mark.parametrize("name", list(LAWS))
def test_each_law_of_the_ring_holds_and_fails_on_its_mutant(name):
    assert LAWS[name](ring)
    assert not LAWS[name](SimpleNamespace(**{**vars(ring), **mutants()[name]}))
