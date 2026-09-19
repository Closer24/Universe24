"""The law of the ray (rays-v1): the record `NatureBeam`, the store of records,
the two pure tables and the one function `nature_beam`, a Node's whole
interval for the rays present (docs/RAY_LAW.md, the model owner's decision of
2026-09-19, Highlights 5.4, "DECIDED: the law of the ray").

The Node holds no coherent sum. A unit is a ray with a record and moves
along the digital line of its momentum at one speed for every direction, a
bijection; rays that meet at a Node are permuted by the eight-slot collision
table, a bijection; the interference is the squared record a detector reads
of a crowd of rays and lives nowhere else; the click is the only one-way
border. The law is ONE generic
function (the owner's name): `nature_beam` performs the interval's steps in
order, each a bijection on the board's state except the border:

1. the walk: every ray whose flight table steps this interval is created at
   the neighbour along its step (the wrap on a periodic axis; through an
   open face it clicks on the face detector), its age advanced modulo its
   direction's period, its phase turned by the family's `phase_per_link`;
2. the readings: at every Node the amount-weighted moments of order 0, 1
   and 2 of the direction vectors of the arrivals, taken ONCE by
   `read_arrivals` over the one reading set (at the measured events in
   step 4; the dense arrays of the whole board are the engine's
   diagnostics, decomposed on request): the count (split outside /
   here, a ray that did not step this interval having the direction
   (0, 0, 0) and entering the zeroth moment alone), the net flow (the
   vector sum of amount x D[direction]) and the traceless tensor (three
   times the sum of amount x D (x) D with its trace removed); valid for a
   fan as for the six headings; every coupling reads its component by key;
3. the collision: at every Node of free space (a Node that holds no
   measured event: rays meet the table there, not each other), per
   (number, content) class, the single units in the eight slots (six
   headings, two rest slots) permuted by the collision table, the forward
   map a cyclic shift inside the class;
4. the measured events' tables and the detectors: a measured event meets
   the rays that arrived this interval at its Node, of every number but its
   own, as one set (the threshold on the set), then each ray by its own
   phase (the window), then the rule: `read` (the push, the rays go on),
   `measure` (the click: the content joins, the border; the detector's
   record is the squared scalar of the same moments taken over the clicked
   rays with their amplitudes as weights, the clicked amount bounded before
   any product), `rerelease` (re-emitted at the next self-creation on the
   declared directions), `pass`; own-number rays are home. The push is ONE
   bilinear form over the arriving rays, `push_A = sum kappa(A, B) . V_B`
   with `V_B` the label moment of the rays (the vector moment of
   `read_arrivals` with the labels as weights) and `kappa` = -M_A for a
   free family's ray (gravity), + q_A x q_B / M_B for a charged one
   (electricity, the whole part off the reader's clock), + 1 for a paid
   ray (its label already carries h s); the emitter's factor (q_B, M_B)
   travels on the ray's record, nothing is looked up by number;
5. the self-creations: the free release, what came home or is re-released
   apportioned whole over the declared directions, the lamp's release at
   its rate, every new ray at age 0 with its emitter's number and, for a
   free family, its emitter's charge and content at birth;
6. merge identical rows and sort by Node.

Every momentum the law reads or moves is the one label of the rows,
`momentum_labels` (content x amount x D[direction] for a paid family,
amount x D[direction] for a free one): the push's moment, the click's
momentum, the face click's, the recoil at a release or a re-emission and
the transit line of the books; no momentum is read off a Port. No other
function holds a piece of the law: `flight_table`, `collision_table` and
`read_arrivals` are the pure tables and the one reading it takes;
`RayStore` is the structure of arrays it moves. Integers only. The engine
(`engine.py`) schedules and books; it computes no physics.
"""

from __future__ import annotations

import itertools
from collections.abc import Callable
from dataclasses import dataclass, field

import numpy as np

from event_universe.core.integer import apportion_whole, bounded_gcd, by_clock, integer_root
from event_universe.core.lattice import PORT_HEADINGS, Address3
from event_universe.core.phase import phase_cosines, phase_sines
from event_universe.events.measured import FACE_NAMES, Ledger, Measured
from event_universe.events.world import (
    FIXED_DIRECTIONS,
    HEADING_OFFSET,
    MOMENTUM_BOUND,
    RAYS_LAW,
    REST_DIRECTIONS,
    RayWorld,
)

Record = Callable[[dict[str, object]], None]
# The time resolution of the flight table: T_d = isqrt(3 |v|^2 Q^2).
Q = 64
# The arrival of a ray that did not step this interval: the first rest
# direction, whose vector is (0, 0, 0), so "here" enters the zeroth moment
# of the reading alone.
HERE = 0
# The Ports of a Node, the Links a ray may cross into it (a walk diagnostic).
PORTS = 6
DIMENSIONS = 3
# The collision's slots: the six headings in Port order and the two rest slots.
COLLISION_SLOTS = 8
SLOT_STATES = 3
# The amplitude of one unit in 32nds: a row of `amount` identical rays (one
# phase) is the coherent sum of its units, A = 32 x amount, so that the
# merge of identical rows (a bookkeeping bijection) leaves the reading
# unchanged; two rows in phase add their amplitudes.
AMPLITUDE_SCALE = 32
# The cosine and sine tables are in 256ths; their rounding puts the length
# of an entry (C, S) below 257 for every N from 2 through 4096
# (`test_ray_detector` (e) checks it), so one unit's amplitude at a phase
# is a vector shorter than 32 x 257.
LONGEST_PHASE_ENTRY = 257
# The affordable amount per detector Node per interval per family: the
# pointer (X, Y) is a sum of vectors of length at most 32 x 257 per unit
# (the triangle inequality), so its length is at most 32 x 257 x the
# clicked amount, and the record X^2 + Y^2 must fit 2^62 - 1: the clicked
# amount of one interval is bounded by isqrt(2^62 - 1) // (32 x 257) =
# 261124 (2^17 inside, 2^18 refused) and a larger set is refused before any
# product is formed (RAY_LAW, section 5).
RECORD_AMOUNT_BOUND = integer_root(MOMENTUM_BOUND) // (AMPLITUDE_SCALE * LONGEST_PHASE_ENTRY)
ZERO3 = (0, 0, 0)


@dataclass(frozen=True)
class NatureBeam:
    """The record of a ray: its Node, its direction (an index of the world's
    table), its age (the flight phase, modulo the direction's period), its
    phase (a step of the circle), its number (the last emitter), its amount
    (whole units), the content one unit carries and, for a free family's
    ray, its emitter's charge and content at birth (`charge`, `mass`: the
    emitter's factor of the electric push, carried on the record; 0 and 0
    on a paid family's ray, whose factor is its content)."""

    node: Address3
    direction: int
    age: int
    phase: int
    number: int
    amount: int
    content: int
    charge: int = 0
    mass: int = 0


# -- the one reading: the moments ------------------------------------------------

# The six independent entries of the symmetric second moment, (i, j) with
# i <= j, in the order the packed column holds them: xx, yy, zz, xy, xz, yz.
PAIR_I = np.array([0, 1, 2, 0, 0, 1], dtype=np.int64)
PAIR_J = np.array([0, 1, 2, 1, 2, 2], dtype=np.int64)
IDENTITY = np.eye(DIMENSIONS, dtype=np.int64)
# The columns of the per-row moment table: the two counts (outside, here),
# the three components of amount x D and the six entries of amount x D_i D_j.
MOMENT_COLUMNS = 2 + DIMENSIONS + PAIR_I.shape[0]


@dataclass(frozen=True)
class Reading:
    """The moments of order 0, 1 and 2 of the direction vectors of one
    reading set, weighted by the amounts (the model owner, 2026-09-19): the
    zeroth moment split into `outside` (the rays that arrived, their
    direction nonzero) and `here` (the rays that did not step, their
    direction zero), `vector` the first moment (the net flow, sum amount x
    D) and `second` the six entries of the second moment (sum amount x
    D_i D_j for xx, yy, zz, xy, xz, yz), whose traceless part is `tensor`
    (3 x the second moment less its trace on the diagonal, a symmetric
    3 x 3 integer matrix of trace zero). Every coupling selects its
    component by key. Keyed over Nodes the arrays carry a leading axis."""

    outside: np.ndarray
    here: np.ndarray
    vector: np.ndarray
    second: np.ndarray

    @property
    def scalar(self) -> np.ndarray:
        """The presence: everything in the set, outside and here."""
        result: np.ndarray = self.outside + self.here
        return result

    @property
    def tensor(self) -> np.ndarray:
        """The traceless second moment, 3 x sum amount x D D^T - tr I: exact
        integers, the trace removed times the number of dimensions."""
        matrix = np.zeros((*self.second.shape[:-1], DIMENSIONS, DIMENSIONS), dtype=np.int64)
        matrix[..., PAIR_I, PAIR_J] = self.second
        matrix[..., PAIR_J, PAIR_I] = self.second
        trace = self.second[..., 0] + self.second[..., 1] + self.second[..., 2]
        result: np.ndarray = DIMENSIONS * matrix - trace[..., None, None] * IDENTITY
        return result

    def component(self, key: str) -> np.ndarray:
        if key == "scalar":
            return self.scalar
        if key == "outside":
            return self.outside
        if key == "here":
            return self.here
        if key == "vector":
            return self.vector
        if key == "tensor":
            return self.tensor
        raise ValueError(f"{RAYS_LAW}: no reading component {key!r}")


def reading_bound_error(rows: int, per_row: int) -> OverflowError:
    """The refusal of a reading whose moments could pass the bound."""
    return OverflowError(
        f"{RAYS_LAW}: the moments of a reading of {rows} rows of up to {per_row} exceed the "
        f"integer bound {MOMENTUM_BOUND} (lower the amounts or the direction bound)"
    )


def moment_table(v: np.ndarray, a: np.ndarray) -> np.ndarray:
    """The per-row table of the moments of `read_arrivals`: the two counts
    (outside, here), the three components of amount x v and the six entries
    of amount x v v^T; the caller has checked the bound."""
    table = np.empty((a.shape[0], MOMENT_COLUMNS), dtype=np.int64)
    table[:, 0] = a * v.any(axis=1)
    table[:, 1] = a - table[:, 0]
    table[:, 2 : 2 + DIMENSIONS] = v * a[:, None]
    table[:, 2 + DIMENSIONS :] = a[:, None] * v[:, PAIR_I] * v[:, PAIR_J]
    return table


def read_arrivals(
    vectors: np.ndarray,
    amounts: np.ndarray,
    keys: np.ndarray | None = None,
    size: int | None = None,
) -> Reading:
    """The one reading of a set of rays: `vectors` (rows, 3) the direction
    vector of each ray's arrival (D[direction] for a ray that arrived this
    interval, (0, 0, 0) for one that did not step) and `amounts` (rows,)
    its weight (the amount; the amplitude at the detector), summed as the
    moments of order 0, 1 and 2, exact integers: outside = the amounts on
    a nonzero vector, here = the amounts on the zero vector, the vector sum
    of amount x v, and the second moment sum amount x v v^T (its traceless
    part the tensor). With `keys` (rows,) and `size` the moments are taken
    per key (one reading per Node), the arrays gaining a leading axis of
    `size`. Valid for a fan as for the six headings: no projection onto
    the Ports."""
    v = np.asarray(vectors, dtype=np.int64).reshape(-1, DIMENSIONS)
    a = np.asarray(amounts, dtype=np.int64).reshape(-1)
    bins = None if keys is None else np.asarray(keys, dtype=np.int64).reshape(-1)
    # Every entry of the table is at most amount x P^2 and every sum has at
    # most the rows of one key: the bound is checked before a product is
    # formed, so the integers below never wrap.
    per_row = int(np.abs(a).max(initial=0)) * max(1, int(np.abs(v).max(initial=0))) ** 2
    rows = a.shape[0] if bins is None else int(np.bincount(bins, minlength=1).max(initial=0))
    if per_row * rows > MOMENTUM_BOUND:
        raise reading_bound_error(rows, per_row)
    table = moment_table(v, a)
    if bins is None:
        sums = table.sum(axis=0)
    else:
        if size is None:
            raise ValueError(f"{RAYS_LAW}: a keyed reading needs its size")
        sums = np.zeros((size, MOMENT_COLUMNS), dtype=np.int64)
        np.add.at(sums, bins, table)
    return Reading(
        sums[..., 0], sums[..., 1], sums[..., 2 : 2 + DIMENSIONS], sums[..., 2 + DIMENSIONS :]
    )


# -- the flight table ------------------------------------------------------------


@dataclass(frozen=True)
class FlightTable:
    """One world constant per direction: v, S_1 = |a| + |b| + |c|,
    T_d = isqrt(3 |v|^2 Q^2), the Bresenham line of v (S_1 unit steps), the
    least period L_d of the flight phase, and the step table: the Link a ray
    of direction d crosses at age tau (a heading, or zero for no move)."""

    vectors: np.ndarray
    manhattan: np.ndarray
    turns: np.ndarray
    period: np.ndarray
    lines: np.ndarray
    steps: np.ndarray

    def manhattan_steps(self, direction: np.ndarray, age: np.ndarray) -> np.ndarray:
        """m(tau) = (2 tau S_1 Q + T_d) // (2 T_d): the Manhattan steps made
        by age tau."""
        s1, t = self.manhattan[direction], self.turns[direction]
        result: np.ndarray = (2 * age * s1 * Q + t) // (2 * t)
        return result


def _bresenham(vector: tuple[int, int, int]) -> list[tuple[int, int, int]]:
    """The S_1 unit steps of one period of the digital line of v: at each
    step the axis whose progress is furthest behind, the lowest axis first."""
    s1 = sum(abs(c) for c in vector)
    line: list[tuple[int, int, int]] = []
    position = [0, 0, 0]
    for j in range(s1):
        best = max(range(3), key=lambda i: (abs(vector[i]) * (j + 1) - s1 * abs(position[i]), -i))
        step = [0, 0, 0]
        step[best] = 1 if vector[best] > 0 else -1
        position[best] += step[best]
        line.append((step[0], step[1], step[2]))
    return line


def flight_table(vectors: tuple[tuple[int, int, int], ...]) -> FlightTable:
    """The flight table of a direction set, computed once at load."""
    count = len(vectors)
    manhattan = np.zeros(count, dtype=np.int64)
    turns = np.ones(count, dtype=np.int64)
    period = np.ones(count, dtype=np.int64)
    lines_list: list[list[tuple[int, int, int]]] = []
    for index, vector in enumerate(vectors):
        s1 = sum(abs(c) for c in vector)
        manhattan[index] = s1
        if s1 == 0:
            lines_list.append([])
            continue
        t = integer_root(3 * sum(c * c for c in vector) * Q * Q)
        turns[index] = t
        p = t // bounded_gcd(s1 * Q, t)
        per_period = s1 * Q * p // t
        period[index] = p * (s1 // bounded_gcd(per_period, s1))
        lines_list.append(_bresenham(vector))
    longest = max(1, int(manhattan.max(initial=0)))
    lines = np.zeros((count, longest, 3), dtype=np.int64)
    for index, line in enumerate(lines_list):
        for j, step in enumerate(line):
            lines[index, j] = step
    table = FlightTable(np.array(vectors, dtype=np.int64), manhattan, turns, period, lines, np.zeros(0))
    longest_period = int(period.max(initial=1))
    # The step table is small integers (a heading or zero): one byte each.
    steps = np.zeros((count, longest_period, 3), dtype=np.int8)
    for index in range(count):
        s1 = int(manhattan[index])
        if s1 == 0:
            continue
        ages = np.arange(int(period[index]), dtype=np.int64)
        direction = np.full(ages.shape, index, dtype=np.int64)
        m0 = table.manhattan_steps(direction, ages)
        m1 = table.manhattan_steps(direction, ages + 1)
        moved = m1 > m0
        steps[index, : len(ages)] = np.where(moved[:, None], lines[index, m0 % s1], 0)
    return FlightTable(table.vectors, manhattan, turns, period, lines, steps)


# -- the collision table ---------------------------------------------------------


@dataclass(frozen=True)
class CollisionTable:
    """The permutation of the 3^8 slot states: `forward[code]`, `inverse[code]`
    and, per code, its single slots in order (`singles`, padded with -1)."""

    forward: np.ndarray
    inverse: np.ndarray
    singles: np.ndarray
    powers: np.ndarray


def slot_heading(slot: int) -> tuple[int, int, int]:
    return PORT_HEADINGS[slot] if slot < 6 else ZERO3


def class_key(state: tuple[int, ...]) -> tuple[tuple[int, ...], int, tuple[int, int, int]]:
    """The class of a slot state (0 empty, 1 single, 2 crowd per slot): the
    crowd mask, the number of singles and the vector sum of their headings."""
    crowd = tuple(1 if s == 2 else 0 for s in state)
    singles = [i for i, s in enumerate(state) if s == 1]
    total = tuple(sum(slot_heading(i)[k] for i in singles) for k in range(3))
    return crowd, len(singles), (total[0], total[1], total[2])


def state_code(state: tuple[int, ...]) -> int:
    return sum(s * SLOT_STATES**k for k, s in enumerate(state))


def collision_table() -> CollisionTable:
    """Generated from its rule over the classes, never written by hand: the
    members of a class sorted as 8-tuples, the forward map the cyclic shift
    by +1, the inverse by -1; a class of one is fixed."""
    classes: dict[object, list[tuple[int, ...]]] = {}
    for state in itertools.product(range(SLOT_STATES), repeat=COLLISION_SLOTS):
        classes.setdefault(class_key(state), []).append(state)
    size = SLOT_STATES**COLLISION_SLOTS
    forward = np.zeros(size, dtype=np.int64)
    inverse = np.zeros(size, dtype=np.int64)
    singles = np.full((size, COLLISION_SLOTS), -1, dtype=np.int64)
    for members in classes.values():
        members.sort()
        count = len(members)
        for i, state in enumerate(members):
            target = members[(i + 1) % count]
            forward[state_code(state)] = state_code(target)
            inverse[state_code(target)] = state_code(state)
    for state in itertools.product(range(SLOT_STATES), repeat=COLLISION_SLOTS):
        code = state_code(state)
        found = [i for i, s in enumerate(state) if s == 1]
        singles[code, : len(found)] = found
    powers = SLOT_STATES ** np.arange(COLLISION_SLOTS, dtype=np.int64)
    return CollisionTable(forward, inverse, singles, powers)


@dataclass(frozen=True)
class RayTables:
    """The two pure tables of a world and the circle's tables: the flight
    table of its direction set, the collision table, the cosines and sines
    at 1/256 and the window table (whether a phase distance is inside the
    half circle centred on the setting)."""

    flight: FlightTable
    collision: CollisionTable
    cosines: np.ndarray
    sines: np.ndarray
    window: np.ndarray


def ray_tables(world: RayWorld) -> RayTables:
    modulus = world.phase_steps
    distance = np.arange(modulus, dtype=np.int64)
    window = (4 * distance < modulus) | (4 * distance >= 3 * modulus)
    return RayTables(
        flight_table(world.directions),
        collision_table(),
        np.array(phase_cosines(modulus), dtype=np.int64),
        np.array(phase_sines(modulus), dtype=np.int64),
        window,
    )


# -- the store -------------------------------------------------------------------

FIELDS = (
    "node",
    "direction",
    "age",
    "phase",
    "number",
    "amount",
    "content",
    "charge",
    "mass",
    "arrival",
)
# The fields that make two rows identical (the amount is what the merge adds).
IDENTITY_FIELDS = ("node", "direction", "age", "phase", "number", "content", "charge", "mass")


def exact_sum(values: np.ndarray) -> int:
    """The exact integer sum of an int64 array: in the register when no
    partial sum can leave it (the largest value times the count within the
    bound), in Python integers otherwise. Never wraps."""
    if values.size == 0:
        return 0
    if int(np.abs(values).max()) * values.size <= MOMENTUM_BOUND:
        return int(values.sum())
    return int(values.sum(dtype=object))


def exact_column_sums(values: np.ndarray) -> list[int]:
    """The exact sum of a (rows, 3) array over the rows, three Python
    integers, by the rule of `exact_sum`."""
    if values.shape[0] == 0:
        return [0] * values.shape[1]
    if int(np.abs(values).max()) * values.shape[0] <= MOMENTUM_BOUND:
        return [int(v) for v in values.sum(axis=0)]
    return [int(v) for v in values.sum(axis=0, dtype=object)]


def label_bound_error(largest: int) -> OverflowError:
    """The refusal of a row whose label weight could pass the bound."""
    return OverflowError(
        f"{RAYS_LAW}: the momentum label of a row, content x amount up to {largest}, "
        f"exceeds the integer bound {MOMENTUM_BOUND}"
    )


def label_weights(amount: np.ndarray, content: np.ndarray, free: bool) -> np.ndarray:
    """The weight of a row's momentum label: the amount for a free family
    (its unit carries no content; its label is the unit), content x amount
    for a paid one, bounded before the product is formed (a row whose
    weight could pass the integer bound is refused)."""
    weight = np.asarray(amount, dtype=np.int64)
    if free:
        return weight
    largest = int(np.abs(weight).max(initial=0)) * int(np.abs(content).max(initial=0))
    if largest > MOMENTUM_BOUND:
        raise label_bound_error(largest)
    result: np.ndarray = weight * np.asarray(content, dtype=np.int64)
    return result


def momentum_labels(
    vectors: np.ndarray, direction: np.ndarray, amount: np.ndarray, content: np.ndarray, free: bool
) -> np.ndarray:
    """The one momentum label of rows of rays, (rows, 3): the label weight
    (`label_weights`) along D[direction], content x amount x D[direction]
    for a paid family, amount x D[direction] for a free one."""
    weight = label_weights(amount, content, free)
    result: np.ndarray = vectors[np.asarray(direction, dtype=np.int64)] * weight[:, None]
    return result


def check_record_amount(total: int, where: str) -> int:
    """The amount a detector clicks in one interval, summed exactly by the
    caller, checked against the affordable amount before the record's
    products are formed; beyond it the run is refused naming the detector
    and the sum."""
    if total > RECORD_AMOUNT_BOUND:
        raise OverflowError(
            f"{RAYS_LAW}: the amount {total} clicked at {where} in one interval exceeds the "
            f"affordable amount per detector Node per interval, {RECORD_AMOUNT_BOUND} "
            "(the record's pointer would pass the integer bound); lower the rate or the amount"
        )
    return total


def record_amount(amounts: np.ndarray, where: str) -> int:
    """`check_record_amount` of the exact sum of `amounts`."""
    return check_record_amount(int(exact_sum(amounts)), where)


class RayStore:
    """The records of one family as a structure of arrays, one row per
    record: `node` the flat index, `direction`, `age`, `phase`, `number`,
    `amount`, `content` (per unit), `charge` and `mass` (the emitter's
    charge and content at the ray's birth for a free family, the factor of
    the electric push carried on the record; 0 and 0 for a paid family) and
    `arrival`, the direction the ray arrived on this interval (its
    direction at the walk; the reading is of the arrivals) or `HERE` for a
    ray that did not step. Rows sorted by `node` after every interval;
    identical rows merged."""

    def __init__(self, shape: Address3) -> None:
        self.shape = shape
        self.strides = (shape[1] * shape[2], shape[2], 1)
        for name in FIELDS:
            setattr(self, name, np.zeros(0, dtype=np.int64))
        self.node: np.ndarray
        self.direction: np.ndarray
        self.age: np.ndarray
        self.phase: np.ndarray
        self.number: np.ndarray
        self.amount: np.ndarray
        self.content: np.ndarray
        self.charge: np.ndarray
        self.mass: np.ndarray
        self.arrival: np.ndarray

    @property
    def size(self) -> int:
        return int(self.node.shape[0])

    def flat(self, position: Address3) -> int:
        return position[0] * self.strides[0] + position[1] * self.strides[1] + position[2]

    def coordinates(self, node: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
        x = node // self.strides[0]
        rest = node - x * self.strides[0]
        y = rest // self.strides[1]
        return x, y, rest - y * self.strides[1]

    def append(self, **columns: np.ndarray) -> None:
        for name in FIELDS:
            setattr(self, name, np.concatenate([getattr(self, name), columns[name].astype(np.int64)]))

    def keep(self, mask: np.ndarray) -> None:
        for name in FIELDS:
            setattr(self, name, getattr(self, name)[mask])

    def take(self, order: np.ndarray) -> None:
        for name in FIELDS:
            setattr(self, name, getattr(self, name)[order])

    def sort(self) -> None:
        self.take(np.argsort(self.node, kind="stable"))

    def merge(self) -> None:
        """Identical rows (equal in every field but the amount) merged, the
        amounts added; then sorted by Node. A bijection: a permutation of
        rows and a sum of interchangeable units."""
        if self.size == 0:
            return
        order = np.lexsort(tuple(getattr(self, name) for name in reversed(IDENTITY_FIELDS)))
        self.take(order)
        same = np.zeros(self.size, dtype=bool)
        same[1:] = True
        for name in IDENTITY_FIELDS:
            column = getattr(self, name)
            same[1:] &= column[1:] == column[:-1]
        starts = np.flatnonzero(~same)
        # The merged amounts are exact: in the register when no group's sum
        # can leave it, in Python integers otherwise, and bounded.
        if int(self.amount.max()) * self.size <= MOMENTUM_BOUND:
            amount = np.add.reduceat(self.amount, starts)
        else:
            merged = np.add.reduceat(self.amount.astype(object), starts)
            if max(int(v) for v in merged) > MOMENTUM_BOUND:
                raise OverflowError(
                    f"{RAYS_LAW}: the amount of a merged row exceeds the integer bound {MOMENTUM_BOUND}"
                )
            amount = merged.astype(np.int64)
        self.keep(~same)
        self.amount = amount
        self.arrival[:] = HERE
        self.sort()

    def slice(self, flat: int) -> tuple[int, int]:
        """The contiguous rows of one Node in the sorted store."""
        lo = int(np.searchsorted(self.node, flat, side="left"))
        hi = int(np.searchsorted(self.node, flat, side="right"))
        return lo, hi

    def rows(self) -> list[NatureBeam]:
        x, y, z = self.coordinates(self.node)
        return [
            NatureBeam(
                (int(x[i]), int(y[i]), int(z[i])),
                int(self.direction[i]),
                int(self.age[i]),
                int(self.phase[i]),
                int(self.number[i]),
                int(self.amount[i]),
                int(self.content[i]),
                int(self.charge[i]),
                int(self.mass[i]),
            )
            for i in range(self.size)
        ]

    def labels(self, rows: np.ndarray, vectors: np.ndarray, free: bool) -> np.ndarray:
        """The momentum labels of the given rows (`momentum_labels`, the one
        label of the law)."""
        return momentum_labels(
            vectors, self.direction[rows], self.amount[rows], self.content[rows], free
        )


def segment_sums(keys: np.ndarray, values: np.ndarray, size: int) -> np.ndarray:
    """Exact integer sums of `values` by `keys` into `size` bins."""
    result = np.zeros(size, dtype=np.int64)
    np.add.at(result, keys, values)
    return result


def bounded(value: int, entry: Measured, quantity: str) -> int:
    """A quantity of a measured event checked before it is assigned against
    the bound of the law, 2^62 - 1; beyond it the run is refused naming the
    measured event, its Node and the quantity."""
    if not -MOMENTUM_BOUND <= value <= MOMENTUM_BOUND:
        raise OverflowError(
            f"{RAYS_LAW}: the {quantity} of measured event {entry.number} at "
            f"{list(entry.position)} exceeds the integer bound {MOMENTUM_BOUND}"
        )
    return value


@dataclass(frozen=True)
class ArrivalRows:
    """One family's rows as the walk left them, held for the readings on
    request: the Node, the direction each row arrived on (`HERE` for a row
    that did not step), its amount, and the rows that crossed a Link this
    interval with their Port (the walk's diagnostic). Arrays the store
    does not write again (every later step replaces its columns)."""

    node: np.ndarray
    arrival: np.ndarray
    amount: np.ndarray
    crossed_node: np.ndarray
    crossed_port: np.ndarray
    crossed_amount: np.ndarray

    @classmethod
    def empty(cls) -> ArrivalRows:
        none = np.zeros(0, dtype=np.int64)
        return cls(none, none, none, none, none, none)


class Readings:
    """The interval's readings per family, dense over the board, decomposed
    on request from the rows of the walk (diagnostics for the engine's
    shell means and flux; the law reads none of them, its own readings
    being taken at the measured events in step 4): the amount that arrived
    per Node (the zeroth moment outside), its net flow (the first moment),
    the presence of every ray (the zeroth moment whole) and, a diagnostic
    of the walk and not of the reading, the amount that crossed into each
    Node through each of its six Ports this interval (`per_port`, the
    Links crossed, for Gauss's flux). Only the active Nodes (the Nodes with
    rows) are decomposed, by the one keyed `read_arrivals` with its bound;
    every other Node is zero."""

    def __init__(self, shape: Address3, vectors: np.ndarray, rows: list[ArrivalRows]) -> None:
        self.shape = shape
        self.vectors = vectors
        self.rows = rows
        self._moments: tuple[list[np.ndarray], list[np.ndarray], list[np.ndarray]] | None = None
        self._per_port: list[np.ndarray] | None = None

    @property
    def nodes(self) -> int:
        return self.shape[0] * self.shape[1] * self.shape[2]

    def _decompose(self) -> tuple[list[np.ndarray], list[np.ndarray], list[np.ndarray]]:
        if self._moments is None:
            count: list[np.ndarray] = []
            flow: list[np.ndarray] = []
            presence: list[np.ndarray] = []
            for rows in self.rows:
                outside = np.zeros(self.nodes, dtype=np.int64)
                vector = np.zeros((self.nodes, DIMENSIONS), dtype=np.int64)
                scalar = np.zeros(self.nodes, dtype=np.int64)
                if rows.node.shape[0]:
                    active, inverse = np.unique(rows.node, return_inverse=True)
                    reading = read_arrivals(
                        self.vectors[rows.arrival], rows.amount, inverse, active.shape[0]
                    )
                    outside[active] = reading.outside
                    vector[active] = reading.vector
                    scalar[active] = reading.scalar
                count.append(outside.reshape(self.shape))
                flow.append(vector.reshape((*self.shape, DIMENSIONS)))
                presence.append(scalar.reshape(self.shape))
            self._moments = (count, flow, presence)
        return self._moments

    @property
    def count(self) -> list[np.ndarray]:
        return self._decompose()[0]

    @property
    def flow(self) -> list[np.ndarray]:
        return self._decompose()[1]

    @property
    def presence(self) -> list[np.ndarray]:
        return self._decompose()[2]

    @property
    def per_port(self) -> list[np.ndarray]:
        if self._per_port is None:
            self._per_port = [
                segment_sums(
                    rows.crossed_node * PORTS + rows.crossed_port,
                    rows.crossed_amount,
                    self.nodes * PORTS,
                ).reshape((*self.shape, PORTS))
                for rows in self.rows
            ]
        return self._per_port


# -- the host's batching of step 4 -------------------------------------------------

# The codes of a measured event's table entries, an array over (measured
# event, family) for the bulk gates of step 4.
RULE_CODES = {"pass": 0, "read": 1, "measure": 2, "rerelease": 3}
PASS_RULE, READ_RULE, MEASURE_RULE = RULE_CODES["pass"], RULE_CODES["read"], RULE_CODES["measure"]


def group_starts(keys: np.ndarray) -> np.ndarray:
    """The first index of every run of equal keys in a grouped array."""
    if keys.shape[0] == 0:
        return np.zeros(0, dtype=np.int64)
    return np.flatnonzero(np.r_[True, keys[1:] != keys[:-1]])


def grouped_sums(values: np.ndarray, starts: np.ndarray, widest: int) -> np.ndarray:
    """`exact_sum` per contiguous group of the rows (a 1-D array) or
    `exact_column_sums` (a 2-D array): in the register when no group's sum
    can leave it (the largest value times the widest group within the
    bound), in Python integers otherwise. Never wraps."""
    if values.shape[0] == 0:
        return np.zeros((0, *values.shape[1:]), dtype=np.int64)
    if int(np.abs(values).max()) * widest <= MOMENTUM_BOUND:
        result: np.ndarray = np.add.reduceat(values, starts, axis=0)
        return result
    result = np.add.reduceat(values.astype(object), starts, axis=0)
    return result


def first_reading_overflow(
    group: np.ndarray, groups: int, amounts: np.ndarray, vectors: np.ndarray
) -> tuple[int, OverflowError] | None:
    """The bound of `read_arrivals` taken per group in bulk, the same
    condition per group as the per-set reading: None when every group
    passes (decided by the maxima over all groups where they suffice),
    else the first failing group in group order with the error the per-set
    reading raises."""
    if amounts.shape[0] == 0:
        return None
    a = np.abs(amounts)
    v = np.abs(vectors).max(axis=1)
    counts = np.bincount(group, minlength=groups)
    if int(a.max()) * max(1, int(v.max())) ** 2 * int(counts.max()) <= MOMENTUM_BOUND:
        return None
    a_max = np.zeros(groups, dtype=np.int64)
    np.maximum.at(a_max, group, a)
    v_max = np.zeros(groups, dtype=np.int64)
    np.maximum.at(v_max, group, v)
    for g in range(groups):
        per_row = int(a_max[g]) * max(1, int(v_max[g])) ** 2
        if per_row * int(counts[g]) > MOMENTUM_BOUND:
            return g, reading_bound_error(int(counts[g]), per_row)
    return None


def first_label_overflow(
    group: np.ndarray, groups: int, amount: np.ndarray, content: np.ndarray
) -> tuple[int, OverflowError] | None:
    """The bound of `label_weights` of a paid family taken per group in
    bulk: None when every group passes, else the first failing group in
    group order with the error `label_weights` raises."""
    if amount.shape[0] == 0:
        return None
    a = np.abs(amount)
    c = np.abs(content)
    if int(a.max()) * int(c.max()) <= MOMENTUM_BOUND:
        return None
    a_max = np.zeros(groups, dtype=np.int64)
    np.maximum.at(a_max, group, a)
    c_max = np.zeros(groups, dtype=np.int64)
    np.maximum.at(c_max, group, c)
    for g in range(groups):
        largest = int(a_max[g]) * int(c_max[g])
        if largest > MOMENTUM_BOUND:
            return g, label_bound_error(largest)
    return None


@dataclass
class FamilyPlan:
    """What step 4 computed in bulk for one family: the rows at measured
    events grouped by measured event (the home rows and the rows that pass
    a gate) and by (measured event, number) (the rows taken by a table),
    with every sum, moment, push moment, label and pointer as Python
    integers, and the slices of each measured event into them; the records
    and the side effects are then applied per group in the order of the
    records. A host structure, no law."""

    events: set[int] = field(default_factory=set)
    # The home rows: per measured event (k0, k1, total, content, taken_in).
    home: dict[int, tuple[int, int, int, int, list[int]]] = field(default_factory=dict)
    h_amount: list[int] = field(default_factory=list)
    h_content: list[int] = field(default_factory=list)
    h_phase: list[int] = field(default_factory=list)
    # The rows that pass a gate: per measured event (k0, k1).
    passes: dict[int, tuple[int, int]] = field(default_factory=dict)
    p_number: list[int] = field(default_factory=list)
    p_amount: list[int] = field(default_factory=list)
    p_phase: list[int] = field(default_factory=list)
    p_below: list[bool] = field(default_factory=list)
    p_window: list[int] = field(default_factory=list)
    # The groups of taken rows by (measured event, number): per measured
    # event (g0, g1) into the group lists; per group its rows (t_*).
    groups: dict[int, tuple[int, int]] = field(default_factory=dict)
    g_number: list[int] = field(default_factory=list)
    g_start: list[int] = field(default_factory=list)
    g_end: list[int] = field(default_factory=list)
    g_total: list[int] = field(default_factory=list)
    g_content: list[int] = field(default_factory=list)
    g_moment: list[list[int]] = field(default_factory=list)
    readings: dict[str, list[object]] = field(default_factory=dict)
    classes: dict[int, list[tuple[int, int, list[int]]]] = field(default_factory=dict)
    t_amount: list[int] = field(default_factory=list)
    t_content: list[int] = field(default_factory=list)
    t_phase: list[int] = field(default_factory=list)
    t_carried: list[int] = field(default_factory=list)
    t_label: list[list[int]] = field(default_factory=list)
    # The detector's pointer per measured event: (clicked amount, X, Y).
    pointer: dict[int, tuple[int, int, int]] = field(default_factory=dict)


# -- the law ---------------------------------------------------------------------


def nature_beam(
    stores: list[RayStore],
    world: RayWorld,
    tables: RayTables,
    measured: dict[int, Measured],
    tick: int,
    record: Record | None,
    ledger: Ledger,
    inverse: bool = False,
) -> Readings:
    """A Node's whole interval for the rays present, at every Node (the
    module docstring, steps 1 to 6). With `inverse` the bijective steps are
    run in reverse order with their inverses (the collision, then the walk)
    on a board without measured events; the border has no inverse."""
    families = world.families
    flight, collision = tables.flight, tables.collision
    vectors = flight.vectors
    modulus = world.phase_steps
    nodes = world.shape[0] * world.shape[1] * world.shape[2]
    shape = world.shape
    extents = np.array(shape, dtype=np.int64)

    def heading_port(step: np.ndarray) -> np.ndarray:
        """The Port index of a unit step (a heading): 2 axis + (0 forward,
        1 backward)."""
        axis = np.abs(step).argmax(axis=1)
        sign = step[np.arange(step.shape[0]), axis]
        result: np.ndarray = 2 * axis + (sign < 0)
        return result

    # The measured events in number order (the order of the records) and
    # the index of the one at each Node, -1 without: the collision is a
    # rule of free space and does not act at a measured event's Node (rays
    # meet the table there, not each other).
    entries = [measured[number] for number in sorted(measured)]
    events = len(entries)
    node_event = np.full(nodes, -1, dtype=np.int64)
    if events:
        node_event[[stores[0].flat(entry.position) for entry in entries]] = np.arange(events)
    occupied = node_event >= 0

    def collide(store: RayStore, backward: bool) -> None:
        """Step 3: at every Node of free space, per (number, content) class,
        the single units in the eight slots permuted by the table
        (`inverse` with `backward`); the same rule forward and back."""
        eligible = np.flatnonzero((store.direction < FIXED_DIRECTIONS) & ~occupied[store.node])
        if eligible.shape[0] < 2:
            return
        node = store.node[eligible]
        number = store.number[eligible]
        content = store.content[eligible]
        order = np.lexsort((content, number, node))
        eligible = eligible[order]
        node, number, content = node[order], number[order], content[order]
        new_group = np.ones(eligible.shape[0], dtype=bool)
        new_group[1:] = (
            (node[1:] != node[:-1]) | (number[1:] != number[:-1]) | (content[1:] != content[:-1])
        )
        group = np.cumsum(new_group) - 1
        groups = int(group[-1]) + 1
        direction = store.direction[eligible]
        slot = np.where(direction < REST_DIRECTIONS, 6 + direction, direction - HEADING_OFFSET)
        key = group * COLLISION_SLOTS + slot
        counts = segment_sums(key, np.ones(key.shape[0], dtype=np.int64), groups * COLLISION_SLOTS)
        heavy = segment_sums(
            key, (store.amount[eligible] != 1).astype(np.int64), groups * COLLISION_SLOTS
        )
        state = np.where(counts == 0, 0, np.where((counts == 1) & (heavy == 0), 1, 2))
        code = (state.reshape(groups, COLLISION_SLOTS) * collision.powers).sum(axis=1)
        target = (collision.inverse if backward else collision.forward)[code]
        moving = target != code
        if not moving.any():
            return
        single = (state[key] == 1) & moving[group]
        rows = np.flatnonzero(single)
        by_slot = rows[np.lexsort((slot[rows], group[rows]))]
        own_group = group[by_slot]
        first = np.ones(by_slot.shape[0], dtype=bool)
        first[1:] = own_group[1:] != own_group[:-1]
        start = np.maximum.accumulate(np.where(first, np.arange(by_slot.shape[0]), 0))
        rank = np.arange(by_slot.shape[0]) - start
        new_slot = collision.singles[target[own_group], rank]
        new_direction = np.where(new_slot >= 6, new_slot - 6, new_slot + HEADING_OFFSET)
        store.direction[eligible[by_slot]] = new_direction

    if inverse:
        if measured:
            raise ValueError(
                f"{RAYS_LAW}: the inverse interval is defined on a board without measured events"
            )
        for family, store in enumerate(stores):
            if store.size == 0:
                continue
            collide(store, backward=True)
            resting = store.direction < REST_DIRECTIONS
            back = np.where(resting, store.age, (store.age - 1) % flight.period[store.direction])
            step = flight.steps[store.direction, back].astype(np.int64)
            moved = step.any(axis=1)
            x, y, z = store.coordinates(store.node)
            coordinates = np.stack([x, y, z], axis=1) - step
            for axis in range(3):
                if world.periodic[axis]:
                    coordinates[:, axis] %= extents[axis]
                elif ((coordinates[:, axis] < 0) | (coordinates[:, axis] >= extents[axis])).any():
                    raise ValueError(
                        f"{RAYS_LAW}: the inverse walk crosses an open face (a click has no inverse)"
                    )
            store.node = coordinates @ np.array(store.strides, dtype=np.int64)
            store.age = back
            store.phase = (store.phase - families[family].phase_per_link * moved) % modulus
            store.arrival[:] = HERE
            store.merge()
        return Readings(shape, vectors, [])

    # 1. The walk: departures become arrivals; the escapes click on the faces.
    arrivals: list[ArrivalRows] = []
    for family, store in enumerate(stores):
        definition = families[family]
        if store.size == 0:
            arrivals.append(ArrivalRows.empty())
            continue
        step = flight.steps[store.direction, store.age].astype(np.int64)
        moved = step.any(axis=1)
        x, y, z = store.coordinates(store.node)
        coordinates = np.stack([x, y, z], axis=1) + step
        escaped = np.zeros(store.size, dtype=bool)
        for axis in range(3):
            if world.periodic[axis]:
                coordinates[:, axis] %= extents[axis]
            else:
                escaped |= (coordinates[:, axis] < 0) | (coordinates[:, axis] >= extents[axis])
        # The Port of the Link crossed (a diagnostic of the walk, and the
        # face a ray leaves through) and the direction the ray arrived on.
        port = np.full(store.size, -1, dtype=np.int64)
        port[moved] = heading_port(step[moved])
        arrival = np.where(moved, store.direction, HERE)
        if escaped.any():
            gone = np.flatnonzero(escaped)
            labels = store.labels(gone, vectors, definition.free)
            for face in ledger.open_faces:
                on_face = port[gone] == face
                through = gone[on_face]
                if through.shape[0] == 0:
                    continue
                amounts = store.amount[through]
                # The face's record: the clicked amount bounded before any
                # product, then the same reading over what clicked with the
                # amplitudes as weights, its scalar squared.
                ledger.face_units[face][family] += record_amount(amounts, FACE_NAMES[face])
                ledger.face_content[face][family] += int(exact_sum(amounts * store.content[through]))
                amplitude = amounts * AMPLITUDE_SCALE
                directions = vectors[store.direction[through]]
                pointer_x = int(
                    read_arrivals(directions, amplitude * tables.cosines[store.phase[through]]).scalar
                )
                pointer_y = int(
                    read_arrivals(directions, amplitude * tables.sines[store.phase[through]]).scalar
                )
                ledger.face_record[face][family] += pointer_x * pointer_x + pointer_y * pointer_y
                ledger.face_momentum[face] = [
                    int(a) + int(b)
                    for a, b in zip(
                        ledger.face_momentum[face], exact_column_sums(labels[on_face]), strict=True
                    )
                ]
            if record is not None:
                for k, index in enumerate(gone):
                    record(
                        {
                            "event": "click",
                            "tick": tick,
                            "node": [int(x[index]), int(y[index]), int(z[index])],
                            "measured": None,
                            "detector": FACE_NAMES[int(port[index])],
                            "family": definition.name,
                            "number": int(store.number[index]),
                            "amount": int(store.amount[index]),
                            "phase": int(store.phase[index]),
                            "momentum": [int(v) for v in labels[k]],
                            "content": int(store.amount[index] * store.content[index]),
                        }
                    )
        store.node = coordinates @ np.array(store.strides, dtype=np.int64)
        crossed = moved & ~escaped
        crossed_node, crossed_port = store.node[crossed], port[crossed]
        crossed_amount = store.amount[crossed]
        # A rest ray keeps its age (the rest slots belong to the six-heading
        # alphabet, whose period it resumes when a collision moves it).
        resting = store.direction < REST_DIRECTIONS
        store.age = np.where(resting, store.age, (store.age + 1) % flight.period[store.direction])
        store.phase = (store.phase + definition.phase_per_link * moved) % modulus
        store.arrival = arrival
        if escaped.any():
            store.keep(~escaped)
        store.sort()
        arrivals.append(
            ArrivalRows(
                store.node, store.arrival, store.amount, crossed_node, crossed_port, crossed_amount
            )
        )

    # 2. The readings: the moments of every Node's arrivals, taken once,
    # where they are read: at the measured events in step 4 (their own
    # local sets) and, for the diagnostics of the whole board, on request
    # from the rows of the walk (the active Nodes only; `Readings`).
    readings = Readings(shape, vectors, arrivals)

    # 3. The collision.
    for store in stores:
        collide(store, backward=False)

    # 4. The measured events' tables and the detectors, the same rule at
    # every measured event taken in bulk by the host: the rows at measured
    # events found by one gather per family, the reading sets grouped by
    # (measured event, number) with one segmented sum per moment, the
    # threshold and the window as masks, every bound checked per group in
    # bulk; then the records and the side effects applied per group in the
    # order of the records (by number, family, other number, row), Python
    # integers only, no reduction reordered.
    keep = [np.ones(store.size, dtype=bool) for store in stores]
    for entry in entries:
        entry.presence = 0
    if events:
        count = len(families)
        ev_number = np.array([e.number for e in entries], dtype=np.int64)
        ev_threshold = np.array([e.threshold for e in entries], dtype=np.int64)
        ev_charge = np.array([e.charge for e in entries], dtype=np.int64)
        ev_rule = np.array([[RULE_CODES[r] for r in e.table] for e in entries], dtype=np.int64)
        ev_window = np.array(
            [[-1 if w is None else w for w in e.windows] for e in entries], dtype=np.int64
        )
        presence = np.zeros((count, events), dtype=np.int64)
        # The refusals found in bulk, keyed by the point at which the rule
        # taken per set raises them, (measured event, family, part, group
        # rank, stage), and raised at that point below.
        failures: dict[tuple[int, int, int, int, int], OverflowError] = {}

        def family_plan(family: int, store: RayStore) -> FamilyPlan | None:
            free = families[family].free
            if store.size == 0:
                return None
            found = node_event[store.node]
            at = np.flatnonzero(found >= 0)
            if at.shape[0] == 0:
                return None
            ev = found[at]
            order = np.argsort(ev, kind="stable")
            at, ev = at[order], ev[order]
            number = store.number[at]
            amount = store.amount[at]
            content = store.content[at]
            phase = store.phase[at]
            direction = store.direction[at]
            arrival = store.arrival[at]
            own = number == ev_number[ev]
            arrived = arrival != HERE
            plan = FamilyPlan()
            # The presence for the clock: every ray at the Node of another
            # number, rest and moving alike (the scalar of the one reading).
            others = np.flatnonzero(~own)
            if others.shape[0]:
                overflow = first_reading_overflow(
                    ev[others], events, amount[others], vectors[arrival[others]]
                )
                if overflow is not None:
                    failures[(overflow[0], family, 0, 0, 0)] = overflow[1]
                np.add.at(presence[family], ev[others], amount[others])
            # Home: the own number's arrivals, taken to be created again; a
            # paid family's labels join the momentum (the units are moved,
            # not copied: the recoil at the re-creation gives them back).
            home = np.flatnonzero(own & arrived)
            if home.shape[0]:
                ev_h = ev[home]
                starts = group_starts(ev_h)
                sizes = np.diff(np.r_[starts, home.shape[0]])
                widest = int(sizes.max())
                total = grouped_sums(amount[home], starts, widest)
                carried = grouped_sums(amount[home] * content[home], starts, widest)
                taken_in = np.zeros((starts.shape[0], DIMENSIONS), dtype=np.int64)
                if not free:
                    overflow = first_label_overflow(ev_h, events, amount[home], content[home])
                    if overflow is not None:
                        failures[(overflow[0], family, 0, 0, 1)] = overflow[1]
                    weights = amount[home] * content[home]
                    taken_in = grouped_sums(vectors[direction[home]] * weights[:, None], starts, widest)
                keep[family][at[home]] = False
                h_events = ev_h[starts].tolist()
                h_starts, h_ends = starts.tolist(), (starts + sizes).tolist()
                totals, carrieds, takens = total.tolist(), carried.tolist(), taken_in.tolist()
                for k, event in enumerate(h_events):
                    plan.home[event] = (h_starts[k], h_ends[k], totals[k], carrieds[k], takens[k])
                plan.h_amount = amount[home].tolist()
                plan.h_content = content[home].tolist()
                plan.h_phase = phase[home].tolist()
                plan.events.update(h_events)
            # Met: the arrivals of every other number at a table that is not
            # `pass`, the threshold on the set, then the window per ray.
            rule = ev_rule[ev, family]
            met = np.flatnonzero(~own & arrived & (rule != PASS_RULE))
            if met.shape[0] == 0:
                return plan
            ev_m = ev[met]
            starts = group_starts(ev_m)
            sizes = np.diff(np.r_[starts, met.shape[0]])
            total = grouped_sums(amount[met], starts, int(sizes.max()))
            below = np.repeat(np.asarray(total < ev_threshold[ev_m[starts]], dtype=bool), sizes)
            window = ev_window[ev_m, family]
            inside = (window < 0) | tables.window[(phase[met] - window) % modulus]
            passing = below | ~inside
            p = np.flatnonzero(passing)
            if p.shape[0]:
                ev_p = ev_m[p]
                p_starts = group_starts(ev_p)
                p_ends = np.r_[p_starts[1:], p.shape[0]]
                p_events = ev_p[p_starts].tolist()
                p_lo, p_hi = p_starts.tolist(), p_ends.tolist()
                for k, event in enumerate(p_events):
                    plan.passes[event] = (p_lo[k], p_hi[k])
                plan.p_number = number[met[p]].tolist()
                plan.p_amount = amount[met[p]].tolist()
                plan.p_phase = phase[met[p]].tolist()
                plan.p_below = below[p].tolist()
                plan.p_window = window[p].tolist()
                plan.events.update(p_events)
            taken = met[~passing]
            if taken.shape[0] == 0:
                return plan
            # The taken rows grouped by (measured event, number), the rows
            # of a group in row order.
            taken = taken[np.lexsort((number[taken], ev[taken]))]
            ev_t, num_t = ev[taken], number[taken]
            new = np.r_[True, (ev_t[1:] != ev_t[:-1]) | (num_t[1:] != num_t[:-1])]
            g_starts = np.flatnonzero(new)
            groups = g_starts.shape[0]
            g_sizes = np.diff(np.r_[g_starts, taken.shape[0]])
            widest = int(g_sizes.max())
            of_row = np.cumsum(new) - 1
            g_ev = ev_t[g_starts]
            e_starts = group_starts(g_ev)

            def fail(group: int, stage: int, error: OverflowError) -> None:
                first = int(e_starts[int(np.searchsorted(e_starts, group, side="right")) - 1])
                failures[(int(g_ev[group]), family, 1, group - first, stage)] = error

            a_t, c_t, ph_t = amount[taken], content[taken], phase[taken]
            v_arrival = vectors[arrival[taken]]
            v_direction = vectors[direction[taken]]
            # The reading's component on the record: the moments of the
            # arrivals' vectors weighted by the amounts (no collision at
            # this Node: the arrival is the direction).
            overflow = first_reading_overflow(of_row, groups, a_t, v_arrival)
            if overflow is not None:
                fail(overflow[0], 2, overflow[1])
            moments = np.add.reduceat(moment_table(v_arrival, a_t), g_starts, axis=0)
            reading = Reading(
                moments[:, 0],
                moments[:, 1],
                moments[:, 2 : 2 + DIMENSIONS],
                moments[:, 2 + DIMENSIONS :],
            )
            for key in {entries[e].reads[family] for e in set(g_ev.tolist())}:
                plan.readings[key] = reading.component(key).tolist()
            # The push, ONE bilinear form over the rows: the label moment per
            # group (the weights bounded before the product), and per
            # (charge, mass) class of the charged rows a charged reader met,
            # in the order of first appearance, the part the electric push
            # reads off the clock.
            if free:
                weights = a_t
            else:
                overflow = first_label_overflow(of_row, groups, a_t, c_t)
                if overflow is not None:
                    fail(overflow[0], 3, overflow[1])
                weights = a_t * c_t
            overflow = first_reading_overflow(of_row, groups, weights, v_direction)
            if overflow is not None:
                fail(overflow[0], 4, overflow[1])
            labels = v_direction * weights[:, None]
            plan.g_moment = np.add.reduceat(labels, g_starts, axis=0).tolist()
            if free:
                charge_t, mass_t = store.charge[at[taken]], store.mass[at[taken]]
                electric = np.flatnonzero((charge_t != 0) & (ev_charge[ev_t] != 0))
                if electric.shape[0]:
                    keys = np.stack([of_row[electric], charge_t[electric], mass_t[electric]], axis=1)
                    unique, first, inverse = np.unique(
                        keys, axis=0, return_index=True, return_inverse=True
                    )
                    parts = np.zeros((unique.shape[0], DIMENSIONS), dtype=np.int64)
                    np.add.at(parts, inverse.reshape(-1), labels[electric])
                    unique_list, parts_list = unique.tolist(), parts.tolist()
                    for c in np.lexsort((first, unique[:, 0])).tolist():
                        group, charge, mass = unique_list[c]
                        plan.classes.setdefault(group, []).append((charge, mass, parts_list[c]))
            carried_t = a_t * c_t
            plan.g_number = num_t[g_starts].tolist()
            plan.g_start = g_starts.tolist()
            plan.g_end = (g_starts + g_sizes).tolist()
            plan.g_total = grouped_sums(a_t, g_starts, widest).tolist()
            plan.g_content = grouped_sums(carried_t, g_starts, widest).tolist()
            plan.t_amount = a_t.tolist()
            plan.t_content = c_t.tolist()
            plan.t_phase = ph_t.tolist()
            plan.t_carried = carried_t.tolist()
            plan.t_label = labels.tolist()
            e_ends = np.r_[e_starts[1:], groups]
            g_events = g_ev[e_starts].tolist()
            e_lo, e_hi = e_starts.tolist(), e_ends.tolist()
            for k, event in enumerate(g_events):
                plan.groups[event] = (e_lo[k], e_hi[k])
            plan.events.update(g_events)
            # The rows a table absorbs leave the store. The detector's
            # record: the clicked amount summed exactly (bounded below
            # before any product), then the same reading over the clicked
            # rows with their amplitudes as weights, its scalar.
            rule_t = ev_rule[ev_t, family]
            keep[family][at[taken[rule_t != READ_RULE]]] = False
            clicked = np.flatnonzero(rule_t == MEASURE_RULE)
            if clicked.shape[0]:
                ev_c = ev_t[clicked]
                c_starts = group_starts(ev_c)
                c_sizes = np.diff(np.r_[c_starts, clicked.shape[0]])
                totals_c = grouped_sums(a_t[clicked], c_starts, int(c_sizes.max())).tolist()
                amplitude = a_t[clicked] * AMPLITUDE_SCALE
                weights_x = amplitude * tables.cosines[ph_t[clicked]]
                weights_y = amplitude * tables.sines[ph_t[clicked]]
                v_c = v_direction[clicked]
                of_click = np.repeat(np.arange(c_starts.shape[0]), c_sizes)
                for stage, weights_c in ((1, weights_x), (2, weights_y)):
                    overflow = first_reading_overflow(of_click, c_starts.shape[0], weights_c, v_c)
                    if overflow is not None:
                        failures[(int(ev_c[c_starts[overflow[0]]]), family, 2, 0, stage)] = overflow[1]
                pointer_x = np.add.reduceat(weights_x, c_starts).tolist()
                pointer_y = np.add.reduceat(weights_y, c_starts).tolist()
                for k, event in enumerate(ev_c[c_starts].tolist()):
                    plan.pointer[event] = (totals_c[k], pointer_x[k], pointer_y[k])
            return plan

        plans = [family_plan(family, store) for family, store in enumerate(stores)]
        # The presence read back (the clock's count), exact over the families.
        totals = presence[0].tolist() if count == 1 else [sum(c) for c in presence.T.tolist()]
        for i, entry in enumerate(entries):
            entry.presence = totals[i]
        active: set[int] = {key[0] for key in failures}
        for plan in plans:
            if plan is not None:
                active |= plan.events

        def refuse(key: tuple[int, int, int, int, int]) -> None:
            error = failures.get(key)
            if error is not None:
                raise error

        # The records and the side effects, per measured event in number
        # order, per family, per group in the order of the other numbers,
        # per row: what the rule taken per set did, in its order.
        for i in sorted(active):
            entry = entries[i]
            node = list(entry.position)
            detector = None if entry.detector is None else world.detectors[entry.detector].name
            for family, plan in enumerate(plans):
                if failures:
                    refuse((i, family, 0, 0, 0))
                if plan is None:
                    continue
                name = families[family].name
                free = families[family].free
                rule = entry.table[family]
                home_plan = plan.home.get(i)
                if home_plan is not None:
                    k0, k1, total, carried, taken_in = home_plan
                    pending = entry.pending[family]
                    for k in range(k0, k1):
                        pending.append((plan.h_amount[k], plan.h_content[k], plan.h_phase[k]))
                    entry.measured[family]["home"] += total
                    ledger.transit_absorbed[family] += total
                    ledger.content_absorbed[family] += carried
                    if not free:
                        if failures:
                            refuse((i, family, 0, 0, 1))
                        entry.momentum = [
                            bounded(a + b, entry, "momentum")
                            for a, b in zip(entry.momentum, taken_in, strict=True)
                        ]
                    if record is not None:
                        record(
                            {
                                "event": "home",
                                "tick": tick,
                                "node": node,
                                "measured": entry.number,
                                "detector": detector,
                                "family": name,
                                "number": entry.number,
                                "amount": total,
                                "push": taken_in,
                                "content": carried,
                            }
                        )
                passes = plan.passes.get(i)
                if passes is not None and record is not None:
                    for k in range(passes[0], passes[1]):
                        line: dict[str, object] = {
                            "event": "pass",
                            "tick": tick,
                            "node": node,
                            "measured": entry.number,
                            "detector": detector,
                            "family": name,
                            "number": plan.p_number[k],
                            "amount": plan.p_amount[k],
                            "phase": plan.p_phase[k],
                        }
                        if plan.p_below[k]:
                            line["window"] = None
                            line["threshold"] = entry.threshold
                        else:
                            line["window"] = plan.p_window[k]
                        record(line)
                span = plan.groups.get(i)
                if span is None:
                    continue
                reading_values = plan.readings[entry.reads[family]]
                for gi in range(span[0], span[1]):
                    if failures:
                        for stage in (2, 3, 4):
                            refuse((i, family, 1, gi - span[0], stage))
                    other = plan.g_number[gi]
                    moment = plan.g_moment[gi]
                    if free:
                        push = [
                            bounded(-moment[axis] * entry.content, entry, "push") for axis in range(3)
                        ]
                        if entry.charge:
                            for charge, mass, part in plan.classes.get(gi, ()):
                                for axis in range(3):
                                    total = bounded(
                                        part[axis] * entry.charge * charge, entry, "electric push"
                                    )
                                    whole = by_clock(entry.age, abs(total), mass)
                                    push[axis] = bounded(
                                        push[axis] + (-whole if total < 0 else whole), entry, "push"
                                    )
                    else:
                        push = [bounded(moment[axis], entry, "push") for axis in range(3)]
                    entry.momentum = [
                        bounded(a + b, entry, "momentum")
                        for a, b in zip(entry.momentum, push, strict=True)
                    ]
                    entry.pushed = [
                        bounded(a + b, entry, "push taken")
                        for a, b in zip(entry.pushed, push, strict=True)
                    ]
                    group_total = plan.g_total[gi]
                    group_content = plan.g_content[gi]
                    reading_value = reading_values[gi]
                    entry.measured[family][rule] += group_total
                    if rule == "read":
                        if record is not None:
                            record(
                                {
                                    "event": "read",
                                    "tick": tick,
                                    "node": node,
                                    "measured": entry.number,
                                    "detector": detector,
                                    "family": name,
                                    "number": other,
                                    "amount": group_total,
                                    "push": push,
                                    "content": group_content,
                                    "reading": reading_value,
                                }
                            )
                        continue
                    ledger.transit_absorbed[family] += group_total
                    ledger.content_absorbed[family] += group_content
                    k0, k1 = plan.g_start[gi], plan.g_end[gi]
                    if rule == "rerelease":
                        pending = entry.pending[family]
                        for k in range(k0, k1):
                            pending.append((plan.t_amount[k], plan.t_content[k], plan.t_phase[k]))
                        if record is not None:
                            record(
                                {
                                    "event": "rerelease",
                                    "tick": tick,
                                    "node": node,
                                    "measured": entry.number,
                                    "detector": detector,
                                    "family": name,
                                    "number": other,
                                    "amount": group_total,
                                    "push": push,
                                    "content": group_content,
                                    "reading": reading_value,
                                }
                            )
                        continue
                    # The click: the content joins, one click per unit.
                    entry.held[family] = bounded(entry.held[family] + group_content, entry, "content")
                    entry.events[family] += group_total
                    ledger.held_measured[family] += group_content
                    if record is not None:
                        for k in range(k0, k1):
                            record(
                                {
                                    "event": "click",
                                    "tick": tick,
                                    "node": node,
                                    "measured": entry.number,
                                    "detector": detector,
                                    "family": name,
                                    "number": other,
                                    "amount": plan.t_amount[k],
                                    "push": plan.t_label[k],
                                    "phase": plan.t_phase[k],
                                    "content": plan.t_carried[k],
                                    "reading": reading_value,
                                }
                            )
                if rule == "measure":
                    total, pointer_x, pointer_y = plan.pointer[i]
                    check_record_amount(total, f"measured event {entry.number} at {node}")
                    if failures:
                        refuse((i, family, 2, 0, 1))
                        refuse((i, family, 2, 0, 2))
                    square = bounded(pointer_x * pointer_x + pointer_y * pointer_y, entry, "record")
                    entry.record[family] = bounded(entry.record[family] + square, entry, "record")
                    if record is not None:
                        record(
                            {
                                "event": "record",
                                "tick": tick,
                                "node": node,
                                "measured": entry.number,
                                "detector": detector,
                                "family": name,
                                "number": 0,
                                "record": square,
                                "pointer": [pointer_x, pointer_y],
                            }
                        )
    for family, store in enumerate(stores):
        if not keep[family].all():
            store.keep(keep[family])

    # 5. The self-creations: the releases into the store.
    numerator, denominator_release = world.release
    for number in sorted(measured):
        entry = measured[number]
        if not entry.creating:
            continue
        age, turn = entry.clock_age, entry.turn
        for family, store in enumerate(stores):
            definition = families[family]
            born: list[tuple[int, int, int, int]] = []  # (direction, amount, content, phase)
            # The emitter's factor a free family's ray carries from birth:
            # its charge and the content the release rate reads (its held
            # content of the family at this self-creation).
            charge, mass = (entry.charge, entry.held[family]) if definition.free else (0, 0)
            if definition.free and entry.held[family] > 0:
                amount = by_clock(age, entry.held[family] * numerator, denominator_release)
                if amount:
                    born.extend((direction, amount, 0, entry.phase) for direction in entry.directions)
            if entry.pending[family]:
                ways = len(entry.directions)
                for amount, content, phase in entry.pending[family]:
                    shares = apportion_whole(amount, [1] * ways, age % ways)
                    for direction, share in zip(entry.directions, shares, strict=True):
                        if share:
                            born.append((direction, share, content, phase))
                            ledger.content_released[family] += share * content
                entry.pending[family] = []
            if (
                entry.lamp_rate is not None
                and family == entry.family
                and turn > 0
                and (
                    entry.lamp_window is None
                    or bool(tables.window[(entry.phase - entry.lamp_window) % modulus])
                )
            ):
                rate_n, rate_d = entry.lamp_rate
                cost = definition.quantum * turn
                for direction in entry.lamp_directions:
                    amount = min(by_clock(age, rate_n, rate_d), entry.held[family] // cost)
                    if amount:
                        born.append((direction, amount, cost, entry.phase))
                        content = cost * amount
                        entry.held[family] -= content
                        ledger.held_spent[family] += content
                        ledger.content_released[family] += content
            if not born:
                continue
            count = len(born)
            direction_column = np.array([b[0] for b in born], dtype=np.int64)
            amount_column = np.array([b[1] for b in born], dtype=np.int64)
            content_column = np.array([b[2] for b in born], dtype=np.int64)
            # The labels of the born rows (the one label; bounded before the
            # product): a paid family's emitter takes their sum as its
            # recoil, a lamp's release and a re-emission alike.
            labels = momentum_labels(
                vectors, direction_column, amount_column, content_column, definition.free
            )
            if int(np.abs(labels).max(initial=0)) > MOMENTUM_BOUND:
                raise OverflowError(
                    f"{RAYS_LAW}: the momentum label of a release of measured event {entry.number} at "
                    f"{list(entry.position)} exceeds the integer bound {MOMENTUM_BOUND}"
                )
            if not definition.free:
                entry.momentum = [
                    bounded(int(a) - int(b), entry, "momentum")
                    for a, b in zip(entry.momentum, exact_column_sums(labels), strict=True)
                ]
            store.append(
                node=np.full(count, store.flat(entry.position), dtype=np.int64),
                direction=direction_column,
                age=np.zeros(count, dtype=np.int64),
                phase=np.array([b[3] for b in born], dtype=np.int64),
                number=np.full(count, entry.number, dtype=np.int64),
                amount=amount_column,
                content=content_column,
                charge=np.full(count, charge, dtype=np.int64),
                mass=np.full(count, mass, dtype=np.int64),
                arrival=np.full(count, HERE, dtype=np.int64),
            )
            ledger.transit_released[family] += int(exact_sum(amount_column))

    # 6. Merge identical rows; sort by Node.
    for store in stores:
        store.merge()
    return readings
