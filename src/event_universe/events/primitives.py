"""THE PRIMITIVES OF THE FREEZE, none naming a force (ALGEBRA.md #what-is-open; the Boss's records
2131 and 2133 (3) of 2026-09-26): (i) THE INTERNAL REPRESENTATION of a family, n pairs of
levels turned together at a Port by generators with exact integer tables, the transport
composing them with one division and a running remainder per level (ALGEBRA.md #the-transport, #what-is-open, the
coarse and fine table of ALGEBRA.md #the-primitives); (iv) THE HELICITY SIGN of a body,
the sign of its spin against its momentum, read at a click (ALGEBRA.md #what-is-open). Primitive (ii), the
self-source polynomial with a structure table (ALGEBRA.md #what-is-open), waits for the mathematician's line on
whether it follows from (i) (record 2131; ALGEBRA.md #a-familys-declaration, #the-transport).

Integers only: a table's angles are the host's (tools/twist_table.py writes and checks them);
this module reads the integers and the identities alone.
"""

from __future__ import annotations

from dataclasses import dataclass

Triple = tuple[int, int, int]
Quadruple = tuple[int, int, int, int, int]
Vector = tuple[int, int, int]

IDENTITY_TRIPLE: Triple = (1, 0, 1)
IDENTITY_QUADRUPLE: Quadruple = (1, 0, 0, 0, 1)


# THE ROTATIONS AS DECLARED INTEGERS (ALGEBRA.md #the-transport, #what-is-open)


def is_triple(triple: tuple[int, ...]) -> bool:
    """A Pythagorean triple (c, s, d): c^2 + s^2 = d^2 exactly, d positive."""
    if len(triple) != 3 or any(type(v) is not int for v in triple):
        return False
    c, s, d = triple
    return d > 0 and c * c + s * s == d * d


def is_quadruple(quadruple: tuple[int, ...]) -> bool:
    """A Pythagorean quadruple (a, b, c, d, e): a^2 + b^2 + c^2 + d^2 = e^2 exactly, e positive:
    a unit quaternion times e, the rotation of a pair of complex components (ALGEBRA.md #what-is-open)."""
    if len(quadruple) != 5 or any(type(v) is not int for v in quadruple):
        return False
    a, b, c, d, e = quadruple
    return e > 0 and a * a + b * b + c * c + d * d == e * e


def compose_triples(first: Triple, second: Triple) -> Triple:
    """The exact product of two rotations: the angles add, the norms multiply
    (c_1 c_0 - s_1 s_0, s_1 c_0 + c_1 s_0, d_1 d_0) (ALGEBRA.md #the-primitives)."""
    c0, s0, d0 = first
    c1, s1, d1 = second
    return (c1 * c0 - s1 * s0, s1 * c0 + c1 * s0, d1 * d0)


def mirror_triple(triple: Triple) -> Triple:
    """The rotation by the opposite angle: k < 0 takes (c, -s, d) (ALGEBRA.md #the-transport)."""
    c, s, d = triple
    return (c, -s, d)


def conjugate_quadruple(quadruple: Quadruple) -> Quadruple:
    a, b, c, d, e = quadruple
    return (a, -b, -c, -d, e)


@dataclass(frozen=True)
class TwistTable:
    """THE TWIST TABLE IN TWO PARTS (ALGEBRA.md #the-primitives): the fine triples for the angles k_0
    theta_unit, k_0 in [0, 2^10), and the coarse triples for the angles k_1 (2^10 theta_unit),
    k_1 in [0, bound]; the triple of k is their exact product, one rotation and one division
    per Port. The unit theta_unit = 1 / (4 Gamma 2^16) radians is the host's; the table holds
    integers. A k beyond the table is refused naming its bound."""

    fine: tuple[Triple, ...]
    coarse: tuple[Triple, ...]

    def check(self) -> None:
        if not self.fine or not self.coarse:
            raise ValueError("the fine or the coarse table is empty")
        for name, table in (("fine", self.fine), ("coarse", self.coarse)):
            if table[0] != IDENTITY_TRIPLE:
                raise ValueError(f"the {name} table's first triple is not the identity (1, 0, 1)")
            for index, triple in enumerate(table):
                if not is_triple(triple):
                    raise ValueError(
                        f"the {name} table's triple {index} {triple} is no Pythagorean triple"
                    )

    @property
    def bound(self) -> int:
        """The largest |k| the table gives."""
        return len(self.coarse) * len(self.fine) - 1

    def triple(self, k: int) -> Triple:
        size = abs(k)
        coarse_index, fine_index = divmod(size, len(self.fine))
        if coarse_index >= len(self.coarse):
            raise ValueError(
                f"the twist {k} is beyond the table's bound {self.bound} (ALGEBRA.md #the-primitives)"
            )
        triple = compose_triples(self.fine[fine_index], self.coarse[coarse_index])
        return mirror_triple(triple) if k < 0 else triple


@dataclass(frozen=True)
class QuadrupleTable:
    """A generator's table of unit quaternions times e, one per |k|; k < 0 the conjugate."""

    entries: tuple[Quadruple, ...]

    def check(self) -> None:
        if not self.entries or self.entries[0] != IDENTITY_QUADRUPLE:
            raise ValueError("the quadruple table's first entry is not the identity (1, 0, 0, 0, 1)")
        for index, quadruple in enumerate(self.entries):
            if not is_quadruple(quadruple):
                raise ValueError(
                    f"the quadruple table's entry {index} {quadruple} is no Pythagorean quadruple"
                )

    def quadruple(self, k: int) -> Quadruple:
        size = abs(k)
        if size >= len(self.entries):
            raise ValueError(f"the twist {k} is beyond the table's bound {len(self.entries) - 1}")
        entry = self.entries[size]
        return conjugate_quadruple(entry) if k < 0 else entry


# THE LINK'S ANGLE AND THE ROTATION WITH ITS REMAINDERS (ALGEBRA.md #the-transport)


def link_angle(sign: int, by: int, weight: int, here: int, arrived: int) -> int:
    """k_port = sigma x q x w x (A here + A arrived): one integer, the same size from both
    ends with the opposite sign (ALGEBRA.md #the-transport)."""
    return sign * by * weight * (here + arrived)


# THE HELICITY SIGN (ALGEBRA.md #what-is-open)


def helicity(spin: Vector, momentum: Vector) -> int:
    """The sign of S . n: +1, -1, or 0 for a body at rest, without spin, or with its spin
    across its motion; an integer, one sign read."""
    dot = spin[0] * momentum[0] + spin[1] * momentum[1] + spin[2] * momentum[2]
    return (dot > 0) - (dot < 0)


def helicity_admits(declared: int, spin: Vector, momentum: Vector) -> bool:
    """A click that declares the helicity it takes or gives admits a body of that sign; a
    declaration of 0 reads no hand."""
    return declared == 0 or helicity(spin, momentum) == declared
