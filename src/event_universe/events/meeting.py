"""The meeting (`meeting-v1`): an event in transit reads the crowd as a body
does, a report, not a balance (the model owner, 2026-09-20, Highlights 5.4,
"DECIDED: the meeting, M-R"; the physicist's and the mathematician's design
of the same day, M-R, the signed read; docs/BEAM_LAW.md section 3 step 3 and
section 10, note 35).

At every Node of free space, after the collision table (step 3), every PAID
unit present (a row of a family with the quantum h >= 1) reads the free units
of every number but its own at the Node, exactly the one reading set a
measured event reads (rest and moving alike, everything at the Node but the
reader's own number), by the vector moment with the labels as weights,
V_B = sum amount x u_d over the free rows of the family B, and the column sum
of its family against theirs, kappa_AB = sum over the columns c of eps_c x
c_A x c_B (gravity the universal column, the value (1, 1) on every family
with the sign minus; the other columns of a paid family are 0 today, so
kappa = -1: the gravity of the crowd). The target is t = sum_B kappa_AB V_B
(for gravity t = -V: against the flow, toward the source, the direction of
the push a body takes), and the unit's direction is turned by k steps of the
arc permutation pi_t of the direction table toward t, k read off the register
the unit already carries, its PHASE:

    adv   = (|t| + Q // 2) // Q      the crowd met, in whole units of Q (the nearest)
    total = phase + adv
    k     = total // N,   phase' = total % N

with |t| = isqrt(t . t) the exact integer norm: N crowd units met turn the
unit by one grain step whatever the order and the spacing of the meetings,
and the phase carries the crowd met modulo N (a phase delay by the crowd:
the interferometric Shapiro reading at a detector). The inverse recomputes t
from the untouched crowd and reads the register back, k = (adv - phase' +
N - 1) // N, phase = phase' + k N - adv, the direction pi_t^-k(d'): for every
fixed crowd the map (direction, phase) -> (pi_t^k(direction), phase') is a
bijection (the design's section 2.1), so the interval stays a bijection up
to the click.

The arc permutation: the moving directions are partitioned into sectors
about t by the sign pattern of their part perpendicular to t (the frame
e1 = t x a, a the axis of the smallest |t| component, the lowest axis first
at a tie, and e2 = t x e1; the sector the signs of p = u . e1, q = u . e2
and |p| - |q|; the directions on the line of t a sector of their own; at
most 16 sectors in space, the two sides of t on a plane world), each sector
is totally ordered by the exact angle to t (the signed cos^2 as the fraction
sign(u . t) (u . t)^2 / |u|^2, compared by cross-multiplication in integers,
ties by the direction's index, a declared tie as the collision's Port order
is) and cyclically shifted by one step toward t, the closest wrapping to the
farthest; k steps are k shifts. The rest directions are not in the alphabet
(fixed points: a parked unit is the table's, not the meeting's). Built once
per direction table and cached per target, the target as read (t = kappa V
whole: the sector boundary |p| = |q| lies at the angle 1 / |t| off the
e1 axis, so the sectors of a crowd of one unit and of three are not the
same partition, and the offline flight of the design was flown so).

Untouched: the free units (the crowd goes on as it did, so two masses'
crowds never turn each other), and the paid unit's content, amount, age and
number; two or more paid units at one Node each read the same V and turn
independently; paid units never read each other; a row of amount above 1
turns as one record (its units are interchangeable). The books: the transit
momentum line moves at every turn by weight x (u_d' - u_d), booked as the
`turned` line per family (`Ledger.turned_momentum`), a report as the free
push on a body is (`pushed`). Fixed local work (one segmented reading per
Node, one sector sort per new target) and fixed local storage (nothing on
the record beyond the phase it carries, nothing at the Node). Every product
is bounded before it is formed; a crowd whose flow, norm or angle keys would
leave the register refuses the run naming the Node or the target.
"""

from __future__ import annotations

import functools
from dataclasses import dataclass, field
from typing import TYPE_CHECKING

import numpy as np

from event_universe.core.integer import bounded_gcd, integer_root, rational_sum
from event_universe.events.world import BEAM_LAW, MOMENTUM_BOUND, NatureBeamWorld, Q

if TYPE_CHECKING:
    from event_universe.events.measured import Ledger
    from event_universe.events.nature_beam import NatureBeamStore, NatureBeamTables

# The bound of a target's component: t . t must fit the work register for the
# exact integer root (3 x 2^60 < 2^63), so a crowd whose signed flow passes
# 2^30 on an axis (2^24 units on one heading) refuses the run.
TARGET_BOUND = 1 << 30
# The bound of a target's component before its frame is formed: the frame's
# e2 = t x (t x a) has components within 2 x reach^2, and p, q and u . t
# within 384 x reach^2 for unit vectors within Q, all inside the register
# for a reach within 2^20; the angle keys are bounded on their own (the
# design's bound: the products within (Q^2 |t|)^2, a crowd of about 2^13
# units at one Node).
REACH_BOUND = 1 << 20
# The permutations kept per direction table: cleared when full (host memory
# only; a permutation is a pure function of the table and the target).
CACHE_LIMIT = 4096
Target = tuple[int, int, int]
Pair = tuple[int, int]


def cross(a: Target, b: Target) -> Target:
    return (a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0])


def sign(value: int) -> int:
    return (value > 0) - (value < 0)


def frame(target: Target) -> tuple[Target, Target]:
    """The frame of a target: e1 = t x a with a the axis of the smallest |t|
    component (the lowest axis first at a tie) and e2 = t x e1, both
    perpendicular to t."""
    axis = min(range(3), key=lambda k: (abs(target[k]), k))
    unit = [0, 0, 0]
    unit[axis] = 1
    e1 = cross(target, (unit[0], unit[1], unit[2]))
    return e1, cross(target, e1)


@dataclass
class ArcTable:
    """The arc permutations of one direction table: the unit vectors u_d of
    the directions (the flight table's `labels`), their squared lengths, the
    moving directions (a rest direction has the zero vector and is a fixed
    point of every permutation) and the permutations built so far, per
    target, forward and inverse."""

    units: np.ndarray
    norms: list[int]
    moving: np.ndarray
    cache: dict[Target, tuple[np.ndarray, np.ndarray]] = field(default_factory=dict)

    def permutation(self, target: Target) -> tuple[np.ndarray, np.ndarray]:
        """pi_t and its inverse as index arrays over the table, built once
        per target."""
        found = self.cache.get(target)
        if found is None:
            if len(self.cache) >= CACHE_LIMIT:
                self.cache.clear()
            forward = arc_shift(self, target, 1)
            inverse = np.empty_like(forward)
            inverse[forward] = np.arange(forward.shape[0], dtype=np.int64)
            found = (forward, inverse)
            self.cache[target] = found
        return found


def arc_table(units: np.ndarray) -> ArcTable:
    """The arc table of a direction table from its unit vectors (rows, 3)."""
    u = np.asarray(units, dtype=np.int64).reshape(-1, 3)
    norms = [int(v) for v in (u * u).sum(axis=1)]
    return ArcTable(u, norms, u.any(axis=1))


def target_bound_error(target: Target, what: str) -> OverflowError:
    return OverflowError(
        f"{BEAM_LAW}: the meeting's target {list(target)} {what} beyond the integer bound "
        f"{MOMENTUM_BOUND} (a sparser crowd at the Node)"
    )


def sectors(table: ArcTable, target: Target) -> tuple[np.ndarray, np.ndarray]:
    """The sector of every moving direction about the target (an integer
    code; -1 for a rest direction) and the signed inner product u . t of
    every direction, the numerator of its angle key; the products bounded
    before they are formed."""
    reach = max(abs(component) for component in target)
    if reach > REACH_BOUND:
        raise target_bound_error(target, f"reaches {reach} on an axis, whose frame would be")
    e1, e2 = frame(target)
    t = np.array(target, dtype=np.int64)
    p = table.units @ np.array(e1, dtype=np.int64)
    q = table.units @ np.array(e2, dtype=np.int64)
    d = table.units @ t
    on_line = (p == 0) & (q == 0)
    code = np.where(
        on_line,
        0,
        1 + (np.sign(p) + 1) * 9 + (np.sign(q) + 1) * 3 + (np.sign(np.abs(p) - np.abs(q)) + 1),
    )
    code[~table.moving] = -1
    return code, d


def arc_shift(table: ArcTable, target: Target, steps: int) -> np.ndarray:
    """pi_t^steps as an index array over the direction table: every sector
    of the moving directions sorted by the exact angle to the target
    (farthest first, the signed cos^2 compared by cross-multiplication,
    ties by index) and cyclically shifted by `steps` toward it; the rest
    directions fixed."""
    code, d = sectors(table, target)
    # The angle keys sign(d) d^2 / |u|^2 are compared as a n' against a' n:
    # the largest product is tested by division before any is formed.
    widest = int(np.abs(d).max(initial=0))
    if widest and widest > integer_root(MOMENTUM_BOUND // max(table.norms)):
        raise target_bound_error(target, f"forms angle keys of {widest}^2 x {max(table.norms)},")
    numerators = [sign(int(v)) * int(v) * int(v) for v in d]
    norms = table.norms

    def compare(i: int, j: int) -> int:
        left, right = numerators[i] * norms[j], numerators[j] * norms[i]
        if left != right:
            return -1 if left < right else 1
        return -1 if i < j else (1 if i > j else 0)

    permutation = np.arange(code.shape[0], dtype=np.int64)
    for sector in np.unique(code[code >= 0]).tolist():
        members = sorted(np.flatnonzero(code == sector).tolist(), key=functools.cmp_to_key(compare))
        count = len(members)
        for rank, index in enumerate(members):
            permutation[index] = members[(rank + steps) % count]
    return permutation


def column_sum(
    reader: tuple[Pair, ...], crowd: tuple[Pair, ...], columns: tuple[tuple[str, int], ...]
) -> Pair:
    """kappa of a paid family against a free one: the signed sum over the
    columns of the two families' values per unit of content, the reduced
    pair (n, d); (-1, 1) for a paid family whose columns beyond gravity are
    0, the gravity of the crowd."""
    terms = [
        (column_sign * n_a * n_b, d_a * d_b)
        for (_, column_sign), (n_a, d_a), (n_b, d_b) in zip(columns, reader, crowd, strict=True)
        if n_a and n_b
    ]
    return rational_sum(terms) if terms else (0, 1)


def register(phase: np.ndarray, norm: np.ndarray, modulus: int) -> tuple[np.ndarray, np.ndarray]:
    """The register read forward: the crowd met in whole units of Q (the
    nearest), added to the phase; k the wraps of the circle, the phase after."""
    total = phase + (norm + Q // 2) // Q
    return total // modulus, total % modulus


def register_inverse(after: np.ndarray, norm: np.ndarray, modulus: int) -> tuple[np.ndarray, np.ndarray]:
    """The register read back from the phase after and the same crowd: the
    unique k with the phase before in 0 .. N - 1, and that phase."""
    advance = (norm + Q // 2) // Q
    k = (advance - after + modulus - 1) // modulus
    return k, after + k * modulus - advance


def crowd_flow(
    crowd_node: np.ndarray,
    crowd_number: np.ndarray,
    crowd_label: np.ndarray,
    node: np.ndarray,
    number: np.ndarray,
) -> np.ndarray:
    """The label flow of one free family's crowd read by paid rows: per paid
    row (its Node, its number) the sum of the crowd's labels at its Node
    less those of its own number, (rows, 3). The sums are bounded before
    they are formed (the largest label times the rows at the fullest
    Node)."""
    keys, inverse = np.unique(crowd_node, return_inverse=True)
    fullest = int(np.bincount(inverse).max())
    if int(np.abs(crowd_label).max()) * fullest > MOMENTUM_BOUND:
        raise OverflowError(
            f"{BEAM_LAW}: the meeting's reading of {fullest} crowd rows at one Node exceeds the "
            f"integer bound {MOMENTUM_BOUND}"
        )
    totals = np.zeros((keys.shape[0], 3), dtype=np.int64)
    np.add.at(totals, inverse, crowd_label)
    found = np.searchsorted(keys, node)
    found = np.minimum(found, keys.shape[0] - 1)
    hit = keys[found] == node
    flow = np.where(hit[:, None], totals[found], 0)
    # The own number's rows at the Node, keyed by (Node, number) without a
    # collision between the pairs.
    span = int(max(crowd_number.max(), number.max())) + 1
    pair_keys, pair_inverse = np.unique(crowd_node * span + crowd_number, return_inverse=True)
    pair_totals = np.zeros((pair_keys.shape[0], 3), dtype=np.int64)
    np.add.at(pair_totals, pair_inverse, crowd_label)
    wanted = node * span + number
    at = np.minimum(np.searchsorted(pair_keys, wanted), pair_keys.shape[0] - 1)
    own = pair_keys[at] == wanted
    result: np.ndarray = flow - np.where(own[:, None], pair_totals[at], 0)
    return result


def meet(
    stores: list[NatureBeamStore],
    world: NatureBeamWorld,
    tables: NatureBeamTables,
    occupied: np.ndarray,
    ledger: Ledger,
    inverse: bool = False,
) -> None:
    """The meeting at every Node of free space (`occupied` False), forward
    or, with `inverse`, read back from the after-state; the module
    docstring. The one call site of each is `nature_beam` (step 3 after the
    table; the inverse before it)."""
    from event_universe.events.nature_beam import exact_column_sums, momentum_labels

    families = world.families
    unit = tables.flight.labels
    arcs = tables.arcs
    modulus = world.phase_steps
    columns = world.columns
    # The crowd: the free rows at the Nodes of free space, per family (its
    # index, the Nodes, the numbers, the labels amount x u_d, each row's
    # label bounded before it is formed).
    crowd: list[tuple[int, np.ndarray, np.ndarray, np.ndarray]] = []
    for family, definition in enumerate(families):
        store = stores[family]
        if not definition.free or store.size == 0:
            continue
        rows = np.flatnonzero(~occupied[store.node])
        if rows.shape[0]:
            crowd.append((family, store.node[rows], store.number[rows], store.labels(rows, unit, True)))
    if not crowd:
        return
    for family, definition in enumerate(families):
        store = stores[family]
        if definition.free or store.size == 0:
            continue
        rows = np.flatnonzero(~occupied[store.node])
        if rows.shape[0] == 0:
            continue
        node, number = store.node[rows], store.number[rows]
        # The target t = sum over the crowd's families of kappa V, kappa the
        # reduced pair (n, d) per pair of families, the sum taken over the
        # common denominator D: t = sum n (D / d) V, |t| = isqrt(t . t) // D.
        kappas = [column_sum(definition.values, families[other].values, columns) for other, *_ in crowd]
        denominator = 1
        for _, d in kappas:
            denominator = denominator * d // bounded_gcd(denominator, d)
        target = np.zeros((rows.shape[0], 3), dtype=np.int64)
        for (other, crowd_node, crowd_number, crowd_label), (n, d) in zip(crowd, kappas, strict=True):
            if n == 0:
                continue
            factor = n * (denominator // d)
            flow = crowd_flow(crowd_node, crowd_number, crowd_label, node, number)
            widest = int(np.abs(flow).max(initial=0))
            if widest and abs(factor) > MOMENTUM_BOUND // (widest * len(crowd)):
                raise OverflowError(
                    f"{BEAM_LAW}: the meeting's target of the family {definition.name!r} against "
                    f"{families[other].name!r}, kappa {n}/{d} on a flow of {widest}, exceeds the "
                    f"integer bound {MOMENTUM_BOUND}"
                )
            target += factor * flow
        reach = int(np.abs(target).max(initial=0))
        if reach > TARGET_BOUND:
            index = int(np.flatnonzero(np.abs(target).max(axis=1) == reach)[0])
            x, y, z = store.coordinates(node[index : index + 1])
            raise OverflowError(
                f"{BEAM_LAW}: the meeting's target at Node [{int(x[0])}, {int(y[0])}, {int(z[0])}] "
                f"reaches {reach} on an axis beyond the bound {TARGET_BOUND} (a sparser crowd)"
            )
        norm = np.zeros(rows.shape[0], dtype=np.int64)
        for index in np.flatnonzero(target.any(axis=1)).tolist():
            t = target[index]
            norm[index] = integer_root(
                int(t[0]) * int(t[0]) + int(t[1]) * int(t[1]) + int(t[2]) * int(t[2])
            )
        if denominator > 1:
            norm //= denominator
        # The register reads the path phase of a record's row (stage (vii),
        # the K finding: the birth phase u is the record's own field, unread
        # by the GameBoard), the phase itself of a row of no record.
        birth = store.birth[rows]
        phase = (store.phase[rows] - birth) % modulus
        if inverse:
            k, phase_after = register_inverse(phase, norm, modulus)
        else:
            k, phase_after = register(phase, norm, modulus)
        direction = store.direction[rows]
        turning = np.flatnonzero((k > 0) & arcs.moving[direction])
        if turning.shape[0]:
            turned = direction[turning].copy()
            for at, index in enumerate(turning.tolist()):
                forward, backward = arcs.permutation(
                    (int(target[index, 0]), int(target[index, 1]), int(target[index, 2]))
                )
                permutation = backward if inverse else forward
                d = int(turned[at])
                for _ in range(int(k[index])):
                    d = int(permutation[d])
                turned[at] = d
            chosen = rows[turning]
            coordinates = np.stack(store.coordinates(store.node[chosen]), axis=1)
            before = momentum_labels(
                unit, direction[turning], store.amount[chosen], store.content[chosen], False, coordinates
            )
            after = momentum_labels(
                unit, turned, store.amount[chosen], store.content[chosen], False, coordinates
            )
            delta = [
                a - b for a, b in zip(exact_column_sums(after), exact_column_sums(before), strict=True)
            ]
            ledger.transit_momentum = [
                a + b for a, b in zip(ledger.transit_momentum, delta, strict=True)
            ]
            ledger.turned_momentum[family] = [
                a + b for a, b in zip(ledger.turned_momentum[family], delta, strict=True)
            ]
            store.direction[chosen] = turned
        store.phase[rows] = (phase_after + birth) % modulus


__all__ = [
    "ArcTable",
    "arc_shift",
    "arc_table",
    "column_sum",
    "crowd_flow",
    "meet",
    "register",
    "register_inverse",
]
