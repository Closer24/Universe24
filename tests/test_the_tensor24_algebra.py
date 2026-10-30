"""Tensor24's algebra, its two generic parts: Rule3's carry with the fine tooth's flip, and the Gaussian ring of the hands,
exact at every size; each law holds and fails on its own mutant."""

from types import SimpleNamespace

import numpy as np

from tensor24.algebra import carry as algebra
from tensor24.algebra import ring
from tests.frame import same, wide


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


def hands(seed, count=3):
    """Hands whose every coefficient's bit is drawn across 2**256, as rows of Python integers."""
    rng = np.random.default_rng(seed)
    return [(wide(rng, 64), wide(rng, 64)) for _ in range(count)]


def ringed(m):
    """The product is commutative, associative and distributive, and i i is -1: four quarter turns are the identity."""
    z, w, v = hands(1)
    i, one = (0 * z[0], 0 * z[0] + 1), (0 * z[0] + 1, 0 * z[0])
    commutes = same(m.mul(z, w), m.mul(w, z))
    associates = same(m.mul(m.mul(z, w), v), m.mul(z, m.mul(w, v)))
    distributes = same(m.mul(z, m.add(w, v)), m.add(m.mul(z, w), m.mul(z, v)))
    quarter = m.mul(i, m.mul(i, m.mul(i, m.mul(i, z))))
    return (
        commutes
        and associates
        and distributes
        and same(m.mul(i, i), (-one[0], one[1]))
        and same(quarter, z)
    )


def conjugate(m):
    """conj is an involution, multiplicative, and z conj(z) is real: T on a hand, its T T +1."""
    z, w, _ = hands(2)
    involution = same(m.conj(m.conj(z)), z)
    multiplicative = same(m.conj(m.mul(z, w)), m.mul(m.conj(z), m.conj(w)))
    return involution and multiplicative and same(m.mul(z, m.conj(z)), (m.norm(z), 0 * z[0]))


def sized(m):
    """The norm is multiplicative: the size of a product is the product of the sizes."""
    z, w, _ = hands(3)
    return same([m.norm(m.mul(z, w))], [m.norm(z) * m.norm(w)])


def paired(m):
    """conj(z) w: its real part the dot a c + b d, its imaginary part the cross a d - b c."""
    (a, b), (c, d), _ = hands(4)
    return same(m.pair((a, b), (c, d)), (a * c + b * d, a * d - b * c))


def reversed_twice(m):
    """T T is -1 on a twin hand, and T keeps its size and turns its spin over."""
    up, down, _ = hands(5)
    psi = (up, down)
    twice = m.reverse(m.reverse(psi))
    rho, s = m.axis(psi)
    rho2, s2 = m.axis(m.reverse(psi))
    turned = [-up[0], -up[1], -down[0], -down[1], rho, *(-x for x in s)]
    return same([*twice[0], *twice[1], rho2, *s2], turned)


def lagrange(m):
    """The two parts of a split share the whole exactly: N<phi, psi> + N<T phi, psi> = rho_phi rho_psi."""
    a, b, c = hands(6)
    _, d, _ = hands(7)
    phi, psi = (a, b), (c, d)
    parts = m.norm(m.overlap(phi, psi)) + m.norm(m.overlap(m.reverse(phi), psi))
    return same([parts], [m.axis(phi)[0] * m.axis(psi)[0]])


def axial(m):
    """A twin hand's reading has S . S = rho rho: its spin as long as its size."""
    up, down, _ = hands(8)
    rho, (x, y, z) = m.axis((up, down))
    return same([x * x + y * y + z * z], [rho * rho])


def shared(m):
    """The split's share read through (rho, S): 2 N<phi, psi> = rho_phi rho_psi + S_phi . S_psi, one trace of two readings."""
    a, b, c = hands(9)
    _, d, _ = hands(10)
    phi, psi = (a, b), (c, d)
    rho, (x, y, z) = m.axis(phi)
    rho_d, (u, v, w) = m.axis(psi)
    up = m.norm(m.overlap(phi, psi))
    return same([up + up], [rho * rho_d + x * u + y * v + z * w])


def joint(m):
    """The pair's joint dial det[phi, psi] = phi_up psi_down - phi_down psi_up is <T phi, psi>: T's sign as the plan writes it."""
    a, b, c = hands(11)
    _, d, _ = hands(12)
    ad, bc = m.mul(a, d), m.mul(b, c)
    return same(m.overlap(m.reverse((a, b)), (c, d)), (ad[0] - bc[0], ad[1] - bc[1]))


def oriented(m):
    """S's axes as derive/D reads them: the up hand alone along +z, up and down alike along +x, down a quarter turn ahead +y."""
    zero = 0 * hands(13)[0][0]
    one, two = zero + 1, zero + 1 + 1
    up, ahead, none = (one, zero), (zero, one), (zero, zero)
    readings = (m.axis((up, none)), m.axis((up, up)), m.axis((up, ahead)))
    wanted = ((one, (zero, zero, one)), (two, (two, zero, zero)), (two, (zero, two, zero)))
    return all(same([r, *s], [q, *t]) for (r, s), (q, t) in zip(readings, wanted, strict=True))


def ring_mutants():
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
        "share": {
            "overlap": lambda phi, psi: ring.add(ring.pair(phi[0], psi[1]), ring.pair(phi[1], psi[0]))
        },
        "joint": {"reverse": lambda psi: (ring.conj(psi[1]), (-psi[0][0], psi[0][1]))},
        "orient": {
            "axis": lambda psi: (
                ring.axis(psi)[0],
                (ring.axis(psi)[1][0], -ring.axis(psi)[1][1], ring.axis(psi)[1][2]),
            )
        },
    }


RING = {"ring": ringed, "conj": conjugate, "norm": sized, "pair": paired}
RING |= {"reverse": reversed_twice, "lagrange": lagrange, "axis": axial}
RING |= {"share": shared, "joint": joint, "orient": oriented}


CARRY = {"exact": exact, "odd": odd, "involution": involution}


def holds(laws, module, mutants):
    """Every law holds on the module and fails on its own mutant, the module's other parts kept."""
    broken = {name: SimpleNamespace(**{**vars(module), **mutants[name]}) for name in laws}
    return all(law(module) and not law(broken[name]) for name, law in laws.items())


def test_the_carry_keeps_its_laws_and_each_mutant_breaks_its_own():
    assert holds(CARRY, algebra, carry_mutants())


def test_the_ring_keeps_its_laws_and_each_mutant_breaks_its_own():
    assert holds(RING, ring, ring_mutants())
