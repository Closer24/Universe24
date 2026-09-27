"""THE PRIMITIVES OF THE FREEZE, none naming a force (ALGEBRA.md #what-is-open; the Boss's records
2131 and 2133 (3) of 2026-09-26): (i) THE INTERNAL REPRESENTATION of a family, n pairs of
levels turned together at a Port by generators with exact integer tables, the transport
composing them with one division and a running remainder per level (ALGEBRA.md #the-transport, #what-is-open, the
coarse and fine table of ALGEBRA.md #the-primitives); (iii) THE CLICKS LIST, one taking and several givings
with the declared conserved integers checked and the taken momentum shared by the draw from
the residue on the wheel, whole, the sum exact (ALGEBRA.md #what-is-open); (iv) THE HELICITY SIGN of a body,
the sign of its spin against its momentum, read at a click (ALGEBRA.md #what-is-open). Primitive (ii), the
self-source polynomial with a structure table (ALGEBRA.md #what-is-open), waits for the mathematician's line on
whether it follows from (i) (record 2131; ALGEBRA.md #a-familys-declaration, #the-transport).

Integers only: a table's angles are the host's (tools/twist_table.py writes and checks them);
this module reads the integers and the identities alone. The loader's hooks are `internal()`
and `clicks_list()`: one call each on the family entry's objects (docs, the README of the
check-mode worlds, section 4). Nothing here is wired to the engine yet: the engine's writer
(record 2133) takes the two calls.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

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


def rotate_plane(
    levels: tuple[int, int], triple: Triple, remainders: tuple[int, int]
) -> tuple[tuple[int, int], tuple[int, int]]:
    """T d + rho' = c re - s im + rho and s re + c im + rho, 0 <= rho' < d: the rotated pair
    and the Port's two remainders after (ALGEBRA.md #the-transport); the norm of the rotated pair is the
    pair's times d^2 before the division, exactly."""
    re, im = levels
    c, s, d = triple
    t_re, rho_re = divmod(c * re - s * im + remainders[0], d)
    t_im, rho_im = divmod(s * re + c * im + remainders[1], d)
    return (t_re, t_im), (rho_re, rho_im)


def rotate_plane_inverse(
    levels: tuple[int, int], triple: Triple, remainders_after: tuple[int, int]
) -> tuple[tuple[int, int], tuple[int, int]]:
    """The exact inverse per Node (ALGEBRA.md #the-transport): from the arrival (a start value, known
    backward) and the remainders after, the remainders before are the unique values in
    [0, d) with rho = rho' - (c re - s im) mod d, and the rotated pair follows."""
    re, im = levels
    c, s, d = triple
    before_re = (remainders_after[0] - (c * re - s * im)) % d
    before_im = (remainders_after[1] - (s * re + c * im)) % d
    t_re = (c * re - s * im + before_re - remainders_after[0]) // d
    t_im = (s * re + c * im + before_im - remainders_after[1]) // d
    return (t_re, t_im), (before_re, before_im)


def rotate_quaternion(
    levels: tuple[int, int, int, int], quadruple: Quadruple, remainders: tuple[int, int, int, int]
) -> tuple[tuple[int, int, int, int], tuple[int, int, int, int]]:
    """The four real components of a complex pair as a quaternion (w, x, y, z), turned by the
    left product with (a, b, c, d) and divided by e with four remainders."""
    w, x, y, z = levels
    a, b, c, d, e = quadruple
    products = (
        a * w - b * x - c * y - d * z,
        a * x + b * w + c * z - d * y,
        a * y - b * z + c * w + d * x,
        a * z + b * y - c * x + d * w,
    )
    out = []
    after = []
    for product, remainder in zip(products, remainders, strict=True):
        t, rho = divmod(product + remainder, e)
        out.append(t)
        after.append(rho)
    return (out[0], out[1], out[2], out[3]), (after[0], after[1], after[2], after[3])


def rotate_quaternion_inverse(
    levels: tuple[int, int, int, int], quadruple: Quadruple, remainders_after: tuple[int, int, int, int]
) -> tuple[tuple[int, int, int, int], tuple[int, int, int, int]]:
    w, x, y, z = levels
    a, b, c, d, e = quadruple
    products = (
        a * w - b * x - c * y - d * z,
        a * x + b * w + c * z - d * y,
        a * y - b * z + c * w + d * x,
        a * z + b * y - c * x + d * w,
    )
    out = []
    before = []
    for product, rho_after in zip(products, remainders_after, strict=True):
        rho = (rho_after - product) % e
        out.append((product + rho - rho_after) // e)
        before.append(rho)
    return (out[0], out[1], out[2], out[3]), (before[0], before[1], before[2], before[3])


# THE GENERATORS AND THE INTERNAL REPRESENTATION (ALGEBRA.md #what-is-open)


@dataclass(frozen=True)
class PlaneGenerator:
    """A one-parameter rotation in one or more planes of real components, all by the same
    triple of the twist table: one plane (re, im) of one pair is the phase of U(1); the two
    planes (re_i, re_j) and (im_i, im_j) together are a rotation between two complex
    components (the planes of colour's SU(3), ALGEBRA.md #what-is-open). Each plane keeps two remainders."""

    planes: tuple[tuple[int, int], ...]
    table: TwistTable

    @property
    def remainder_count(self) -> int:
        return 2 * len(self.planes)

    def apply(
        self, levels: list[int], k: int, remainders: tuple[int, ...], inverse: bool = False
    ) -> tuple[int, ...]:
        triple = self.table.triple(k)
        rotate = rotate_plane_inverse if inverse else rotate_plane
        out: list[int] = []
        for index, (p, q) in enumerate(self.planes):
            pair = (remainders[2 * index], remainders[2 * index + 1])
            (levels[p], levels[q]), rho = rotate((levels[p], levels[q]), triple, pair)
            out.extend(rho)
        return tuple(out)


@dataclass(frozen=True)
class QuaternionGenerator:
    """A rotation of a pair of complex components, the four real components `block`, by a
    unit quaternion of the table (weak isospin's SU(2), ALGEBRA.md #what-is-open); four remainders."""

    block: tuple[int, int, int, int]
    table: QuadrupleTable

    @property
    def remainder_count(self) -> int:
        return 4

    def apply(
        self, levels: list[int], k: int, remainders: tuple[int, ...], inverse: bool = False
    ) -> tuple[int, ...]:
        quadruple = self.table.quadruple(k)
        rotate = rotate_quaternion_inverse if inverse else rotate_quaternion
        w, x, y, z = self.block
        current = (levels[w], levels[x], levels[y], levels[z])
        four = (remainders[0], remainders[1], remainders[2], remainders[3])
        (levels[w], levels[x], levels[y], levels[z]), rho = rotate(current, quadruple, four)
        return rho


Generator = PlaneGenerator | QuaternionGenerator


@dataclass(frozen=True)
class InternalRepresentation:
    """A family's internal representation: `pairs` complex components (2 pairs real levels) and
    its generators in the order the transport composes them (ALGEBRA.md #what-is-open); the Link's field is a
    vector of integers, one angle per generator."""

    pairs: int
    generators: tuple[Generator, ...]

    @property
    def levels(self) -> int:
        return 2 * self.pairs

    @property
    def remainder_count(self) -> int:
        return sum(generator.remainder_count for generator in self.generators)

    def check(self) -> None:
        if self.pairs < 1:
            raise ValueError("an internal representation holds at least one pair")
        for number, generator in enumerate(self.generators):
            indices = (
                [index for plane in generator.planes for index in plane]
                if isinstance(generator, PlaneGenerator)
                else list(generator.block)
            )
            if len(set(indices)) != len(indices) or any(not (0 <= i < self.levels) for i in indices):
                raise ValueError(
                    f"generator {number} turns the levels {indices}, not distinct indices below {self.levels}"
                )
            generator.table.check()

    def transport(
        self, arrived: tuple[int, ...], angles: tuple[int, ...], remainders: tuple[int, ...]
    ) -> tuple[tuple[int, ...], tuple[int, ...]]:
        """The arrival's levels turned by every generator in sequence, each by its own angle
        with its own division and remainders (ALGEBRA.md #what-is-open); returns the transported levels and the
        remainders after."""
        return self._run(arrived, angles, remainders, inverse=False)

    def transport_inverse(
        self, arrived: tuple[int, ...], angles: tuple[int, ...], remainders_after: tuple[int, ...]
    ) -> tuple[tuple[int, ...], tuple[int, ...]]:
        """The exact inverse (ALGEBRA.md #the-transport): from the arrival, known backward, and the
        remainders after, the transported levels and the remainders before, generator by
        generator in the forward order (each stage's input is the stage before's output)."""
        return self._run(arrived, angles, remainders_after, inverse=True)

    def _run(
        self,
        arrived: tuple[int, ...],
        angles: tuple[int, ...],
        remainders: tuple[int, ...],
        inverse: bool,
    ) -> tuple[tuple[int, ...], tuple[int, ...]]:
        if len(arrived) != self.levels:
            raise ValueError(f"{len(arrived)} levels arrived; the representation holds {self.levels}")
        if len(angles) != len(self.generators):
            raise ValueError(f"{len(angles)} angles for {len(self.generators)} generators")
        if len(remainders) != self.remainder_count:
            raise ValueError(
                f"{len(remainders)} remainders; the representation keeps {self.remainder_count}"
            )
        levels = list(arrived)
        out: list[int] = []
        start = 0
        for generator, k in zip(self.generators, angles, strict=True):
            count = generator.remainder_count
            out.extend(generator.apply(levels, k, remainders[start : start + count], inverse=inverse))
            start += count
        return tuple(levels), tuple(out)


def _plane(row: Any, label: str) -> tuple[int, int]:
    if not isinstance(row, list | tuple) or len(row) != 2:
        raise ValueError(f"{label}: a pair of level indices")
    return (int(row[0]), int(row[1]))


def _quadruple(row: Any, label: str) -> Quadruple:
    if not isinstance(row, list | tuple) or len(row) != 5:
        raise ValueError(f"{label}: five integers (a, b, c, d, e)")
    return (int(row[0]), int(row[1]), int(row[2]), int(row[3]), int(row[4]))


def internal(obj: dict[str, Any], twist: TwistTable) -> InternalRepresentation:
    """THE LOADER'S HOOK for a family's `internal` object: `{"pairs": n, "generators": [...]}`,
    each generator `{"planes": [[p, q], ...]}` (the twist table's triples) or
    `{"quaternion": [w, x, y, z], "table": [[a, b, c, d, e], ...]}`; every index a level below
    2 n, every table checked (ALGEBRA.md #what-is-open)."""
    if not isinstance(obj, dict) or set(obj) != {"pairs", "generators"}:
        raise ValueError('internal: an object with the keys "pairs" and "generators"')
    pairs = obj["pairs"]
    if type(pairs) is not int or pairs < 1:
        raise ValueError("internal.pairs: a whole number of complex components, at least 1")
    generators: list[Generator] = []
    for number, entry in enumerate(obj["generators"]):
        label = f"internal.generators[{number}]"
        if not isinstance(entry, dict):
            raise ValueError(f"{label}: an object")
        if set(entry) == {"planes"}:
            planes = tuple(_plane(plane, f"{label}.planes") for plane in entry["planes"])
            if not planes:
                raise ValueError(f"{label}.planes: pairs of level indices")
            generators.append(PlaneGenerator(planes, twist))
        elif set(entry) == {"quaternion", "table"}:
            block = entry["quaternion"]
            if not isinstance(block, list | tuple) or len(block) != 4:
                raise ValueError(f"{label}.quaternion: the four level indices of a complex pair")
            four = (int(block[0]), int(block[1]), int(block[2]), int(block[3]))
            table = QuadrupleTable(tuple(_quadruple(row, f"{label}.table") for row in entry["table"]))
            generators.append(QuaternionGenerator(four, table))
        else:
            raise ValueError(f'{label}: "planes", or "quaternion" with "table"')
    representation = InternalRepresentation(pairs, tuple(generators))
    representation.check()
    return representation


# THE CLICKS LIST (ALGEBRA.md #what-is-open)


@dataclass(frozen=True)
class Giving:
    family: str
    count: int
    labels: dict[str, int]  # the conserved integers per given quantum (q and the others declared)


@dataclass(frozen=True)
class ClicksList:
    """One taking and several givings: the click loops over the list (ALGEBRA.md #what-is-open); the
    conserved integers are checked once, at load; the helicity the click takes or gives,
    +1, -1 or 0 for none (ALGEBRA.md #what-is-open)."""

    takes: str
    taken_labels: dict[str, int]
    givings: tuple[Giving, ...]
    helicity: int = 0

    def check(self) -> None:
        if self.helicity not in (-1, 0, 1):
            raise ValueError(f"clicks.helicity {self.helicity}: -1, 0 or 1")
        for label, taken in self.taken_labels.items():
            given = sum(giving.count * giving.labels.get(label, 0) for giving in self.givings)
            if given != taken:
                raise ValueError(
                    f"clicks: the conserved integer {label!r} is {taken} taken and {given} given; the declared signs do not balance (ALGEBRA.md #what-is-open)"
                )
        for giving in self.givings:
            if giving.count < 1:
                raise ValueError(
                    f"clicks: the giving into {giving.family!r} counts {giving.count}, at least 1"
                )
            for label in giving.labels:
                if label not in self.taken_labels:
                    raise ValueError(
                        f"clicks: the giving into {giving.family!r} names {label!r}, which the taking does not declare"
                    )

    @property
    def products(self) -> int:
        return sum(giving.count for giving in self.givings)


def clicks_list(obj: dict[str, Any]) -> ClicksList:
    """THE LOADER'S HOOK for a family's `clicks` object: `{"takes": {"labels": {...}}, "gives":
    [{"family": name, "count": n, "labels": {...}}, ...], "helicity": -1 | 0 | 1}`; the
    conserved integers balance or the world is refused (ALGEBRA.md #what-is-open)."""
    if (
        not isinstance(obj, dict)
        or not {"takes", "gives"} <= set(obj)
        or not set(obj) <= {"takes", "gives", "helicity"}
    ):
        raise ValueError('clicks: an object with "takes", "gives" and optionally "helicity"')
    takes = obj["takes"]
    if not isinstance(takes, dict) or set(takes) != {"family", "labels"}:
        raise ValueError('clicks.takes: {"family": name, "labels": {...}}')
    givings = tuple(
        Giving(
            str(entry["family"]),
            int(entry["count"]),
            {str(k): int(v) for k, v in entry.get("labels", {}).items()},
        )
        for entry in obj["gives"]
    )
    result = ClicksList(
        str(takes["family"]),
        {str(k): int(v) for k, v in takes["labels"].items()},
        givings,
        int(obj.get("helicity", 0)),
    )
    result.check()
    return result


def share_momenta(total: Vector, products: int, residue: int, wheel: int) -> tuple[Vector, ...]:
    """THE ONE PRIMITIVE OF ALGEBRA.md #what-is-open: the taken momentum shared among `products` quanta by the
    draw from the residue on the wheel, whole, the sum kept exactly. The products - 1 cuts on
    [0, |n_a|] along each axis are the rungs (residue + i W div products) mod W scaled to |n_a|
    by one division each, i = 1 to products - 1, sorted; the shares are the differences,
    signed as n_a. One product takes the whole; the same residue gives the same shares."""
    if products < 1:
        raise ValueError("a click gives at least one product")
    if not 0 <= residue < wheel:
        raise ValueError(f"the residue {residue} is not on the wheel of {wheel}")
    rungs = sorted((residue + i * wheel // products) % wheel for i in range(1, products))
    shares: list[list[int]] = [[0, 0, 0] for _ in range(products)]
    for axis in range(3):
        size = abs(total[axis])
        sign = 1 if total[axis] >= 0 else -1
        cuts = [0] + [size * rung // wheel for rung in rungs] + [size]
        for index in range(products):
            shares[index][axis] = sign * (cuts[index + 1] - cuts[index])
    return tuple((share[0], share[1], share[2]) for share in shares)


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
