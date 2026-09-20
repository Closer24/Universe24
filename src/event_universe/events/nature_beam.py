"""The Beam Law (beam-v1): the record `NatureBeam`, the store of records,
the two pure tables and the one function `nature_beam`, a Node's whole
interval for the rays present (docs/BEAM_LAW.md, the model owner's decision of
2026-09-19, Highlights 5.4, "DECIDED: the law of the ray").

The Node holds no coherent sum. A unit is a ray with a record and moves
along the digital line of its momentum at one speed for every direction, a
bijection; rays that meet at a Node are permuted by the eight-slot collision
table, a bijection; the interference is the squared record a detector reads
of a crowd of rays and lives nowhere else; the click is the only one-way
border. The law is ONE generic
function (the owner's name): `nature_beam` performs the interval's steps in
order, each a bijection on the GameBoard's state except the border:

1. the walk: every ray whose flight table steps this interval is created at
   the neighbour along its step (the wrap on a periodic axis; through an
   open face it clicks on the face detector), its age advanced by one (the
   age is the count of intervals since the measured event that created the
   ray, kept whole on the record since 2026-09-20; the flight reads it
   modulo the direction's period and nothing else of the GameBoard reads it),
   its phase turned by the family's `phase_per_link`;
2. the readings: at every Node the amount-weighted moments of order 0, 1
   and 2 of the direction vectors of the arrivals, taken ONCE by
   `read_arrivals` over the one reading set (at the measured events in
   step 4; the dense arrays of the whole GameBoard are the engine's
   diagnostics, decomposed on request): the arrived amount (split outside /
   here, a ray that did not step this interval having the direction
   (0, 0, 0) and entering the zeroth moment alone), the net flow (the
   vector sum of amount x D[direction]), the traceless tensor (three
   times the sum of amount x D (x) D with its trace removed) and the age
   moment (the sum of amount x age, split the same way: a reading aid of
   the measured event, the external thing, that changes nothing on the
   GameBoard); valid for a fan as for the six headings; every coupling reads
   its component by key;
3. the collision: at every Node of free space (a Node that holds no
   measured event: rays meet the table there, not each other), per
   (number, content) class, the single units in the eight slots (six
   headings, two rest slots) permuted by the collision table, the forward
   map a cyclic shift inside the class; the age is never read here and a
   moved unit keeps it;
4. the measured events' tables and the detectors: a measured event meets
   the rays that arrived this interval at its Node, of every number but its
   own, as one set (the threshold on the set), then each ray by its own
   phase (the window), then the rule: `read` (the push, the rays go on),
   `measure` (the click: the content joins, the border; the detector's
   record is the square of the first moment of the same reading taken over
   the clicked rays on the circle's unit vectors (C[phase], S[phase], 0)
   with their amplitudes as weights, the pointer, an exact integer: a
   report of the host, never refused; `coherent_pointer`, the four
   unifications of 2026-09-20), `rerelease` (re-emitted at the next self-creation on the
   declared directions), `pass`; own-number rays are home. The push is ONE
   product per arriving free ray (`push_form`, the model owner's decision
   of 2026-09-20: charge is per unit of content of a family, rho): with
   `V_B` the label flow of the rays (the vector moment of
   `read_arrivals` with the labels as weights), M_A the reader's content
   as the frame read it and rho_A, rho_B the families' charges per unit
   of content, `push_A = M_A x (rho_A rho_B - 1) x V_B` for a free
   family's rays (gravity -M_A V_B and electricity rho_A rho_B M_A V_B,
   the latter the whole part off the reader's clock by the declared
   pairs, `sign x by_clock(age_A, |V n_A n_B M_A|, d_A d_B)`), and
   `push_A = V_B` for a paid family's rays (their label already carries
   h s); every input is the reader's or the arriving family's key,
   nothing is looked up by number and the record carries no factor. What
   the clock counts is read here too, over every ray of another number at
   the Node: the presence, or on a table entry that reads `age` the age
   moment (`measured.count_component`), the measured event's reading of
   the whole age;
5. the self-creations: the free release, what came home or is re-released
   apportioned whole over the declared directions, the lamp's release at
   its rate, every new ray at age 0 with its emitter's number;
6. merge identical rows and sort by Node; a row whose age passed the
   world's `age_bound` refuses the run (the store's bound; the world must
   be small enough or declare its bound).

Every momentum the law reads or moves is the one label of the rows,
`momentum_labels` (content x amount x u_d for a paid family, amount x u_d
for a free one, u_d the unit vector of the direction at the flight table's
scale Q = 64: the integer vector nearest Q D / |D|, `unit_label`, one
world constant per direction on the flight table, exactly Q e_d on a
heading; the model owner's decision of 2026-09-19 on the physics-rule
reviewer's verdict, BEAM_LAW section 2 and note 23): the push's moment, the
click's momentum, the face click's, the recoil at a release or a
re-emission and the transit line of the books; no momentum is read off a
Port, and the reading's vector and tensor moments are taken on u_d as
well, so a fan's flow reads Q per unit of amount direction-blind. No other
function holds a piece of the law: `flight_table`, `collision_table` and
`read_arrivals` are the pure tables and the one reading it takes;
`NatureBeamStore` is the structure of arrays it moves. Integers only. The engine
(`engine.py`) schedules and books; it computes no physics.
"""

from __future__ import annotations

import functools
import itertools
from collections.abc import Callable
from dataclasses import dataclass, field

import numpy as np

from event_universe.core.game_board import PORT_HEADINGS, Address3
from event_universe.core.integer import apportion_whole, bounded_gcd, by_clock, integer_root
from event_universe.core.phase import PHASE_COSINE_SCALE, phase_cosines, phase_sines
from event_universe.events.measured import Ledger, Measured, count_component
from event_universe.events.world import (
    AGE_READS,
    BEAM_LAW,
    FACE_NAMES,
    FIXED_DIRECTIONS,
    HEADING_OFFSET,
    LIFETIME_NAME,
    MOMENTUM_BOUND,
    REST_DIRECTIONS,
    NatureBeamWorld,
    Q,
    Vector,
)

Record = Callable[[dict[str, object]], None]
# The one scale of the law is the world's constant `world.Q`: the time
# resolution of the flight table, T_d = isqrt(3 |v|^2 Q^2), and the length of
# a unit's momentum label, u_d the integer vector nearest Q D / |D|
# (`world.LABEL_SCALE` is the same number); the parser derives the age bound
# from it.
# The arrival of a ray that did not step this interval: the first rest
# direction, whose vector is (0, 0, 0), so "here" enters the zeroth moment
# of the reading alone.
NO_ARRIVAL = 0
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
# (`test_nature_beam_detector` (e) checks it), so one unit's amplitude at a phase
# is a vector shorter than 32 x 257.
LONGEST_PHASE_ENTRY = 257
# The pointer (X, Y) of a detector set is the first moment of the one
# reading over the circle (`coherent_pointer`: the moment table on the
# unit vectors (C[phase], S[phase], 0) with the amplitudes 32 x amount as
# the weights; the four unifications, the model owner, 2026-09-20). It is
# taken in the int64 register where the reading's own bound holds for that
# table (`reading_fits`: the amplitude times 256^2 times the rows of a
# group within 2^62 - 1, the second moment's bound, which the pointer does
# not read but the one table forms) and in Python integers otherwise
# (`moment_table(exact=True)`, the same table); the square X^2 + Y^2 and
# the record that accumulates it are Python integers always. The record is
# a report of the host, not the law's local work: it is exact and never
# refused (BEAM_LAW, section 5 and notes 19 and 33; the former affordable
# amount 261123 refused a lawful world).
ZERO3 = (0, 0, 0)


@dataclass(frozen=True)
class NatureBeam:
    """The record of a ray: its Node, its direction (an index of the world's
    table), its age (the count of intervals since the measured event that
    created it, whole; the flight reads it modulo the direction's period,
    a measured event may read it whole), its
    phase (a step of the circle), its number (the last emitter), its amount
    (whole units) and the content one unit carries. Nothing else: the
    family (the store it is in) suffices for the electric push, whose
    factor is the family's charge per unit of content (the model owner,
    2026-09-20; until then a free family's ray carried its emitter's charge
    and content at birth)."""

    node: Address3
    direction: int
    age: int
    phase: int
    number: int
    amount: int
    content: int

    def record(self, vectors: np.ndarray) -> dict[str, object]:
        """The row as `state.json` writes it, the direction as its vector."""
        return {
            "direction": [int(v) for v in vectors[self.direction]],
            "age": self.age,
            "phase": self.phase,
            "number": self.number,
            "amount": self.amount,
            "content": self.content,
        }


# -- the one reading: the moments ------------------------------------------------

# The six independent entries of the symmetric second moment, (i, j) with
# i <= j, in the order the packed column holds them: xx, yy, zz, xy, xz, yz.
PAIR_I = np.array([0, 1, 2, 0, 0, 1], dtype=np.int64)
PAIR_J = np.array([0, 1, 2, 1, 2, 2], dtype=np.int64)
IDENTITY = np.eye(DIMENSIONS, dtype=np.int64)
# The columns of the per-row moment table: the two counts (outside, here),
# the three components of amount x D, the six entries of amount x D_i D_j
# and the two age moments (amount x age, outside and here).
AGE_COLUMN = 2 + DIMENSIONS + PAIR_I.shape[0]
MOMENT_COLUMNS = AGE_COLUMN + 2


@dataclass(frozen=True)
class Moments:
    """The moments of order 0, 1 and 2 of the direction vectors of one
    reading set, weighted by the amounts (the model owner, 2026-09-19): the
    zeroth moment split into `outside` (the rays that arrived, their
    direction nonzero) and `here` (the rays that did not step, their
    direction zero), `flow` the first moment (the net flow, sum amount x
    D) and `second` the six entries of the second moment (sum amount x
    D_i D_j for xx, yy, zz, xy, xz, yz), whose traceless part is `tensor`
    (3 x the second moment less its trace on the diagonal, a symmetric
    3 x 3 integer matrix of trace zero), and `age_outside`, `age_here` the
    age moment (sum amount x age, a first moment in the age, split as the
    count is), whose whole is `age`. The age moment is a reading aid of the
    measured event, the external thing (the model owner, 2026-09-19, "it
    must be checked in the detector and not on the GameBoard"): the age is
    read whole only by a measured event; the GameBoard's rules (the flight,
    the collision) never read it whole; this component only helps the
    detector's computation and changes nothing on the GameBoard. Every
    coupling selects its component by key. Keyed over Nodes the arrays
    carry a leading axis."""

    outside: np.ndarray
    here: np.ndarray
    flow: np.ndarray
    second: np.ndarray
    age_outside: np.ndarray
    age_here: np.ndarray

    @property
    def presence(self) -> np.ndarray:
        """The presence: everything in the set, outside and here."""
        result: np.ndarray = self.outside + self.here
        return result

    @property
    def age(self) -> np.ndarray:
        """The age moment of the set, sum amount x age, outside and here."""
        result: np.ndarray = self.age_outside + self.age_here
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
            return self.presence
        if key == "outside":
            return self.outside
        if key == "here":
            return self.here
        if key == "vector":
            return self.flow
        if key == "tensor":
            return self.tensor
        if key == AGE_READS:
            return self.age
        raise ValueError(f"{BEAM_LAW}: no reading component {key!r}")


def reading_bound_error(rows: int, per_row: int) -> OverflowError:
    """The refusal of a reading whose moments could pass the bound."""
    return OverflowError(
        f"{BEAM_LAW}: the moments of a reading of {rows} rows of up to {per_row} exceed the "
        f"integer bound {MOMENTUM_BOUND} (lower the amounts or the direction bound)"
    )


def moment_table(
    v: np.ndarray, a: np.ndarray, ages: np.ndarray | None = None, exact: bool = False
) -> np.ndarray:
    """The per-row table of the moments of `read_arrivals`: the two counts
    (outside, here), the three components of amount x v, the six entries
    of amount x v v^T and the two age moments amount x age (outside, here;
    zero without `ages`); the caller has checked the bound. With `exact`
    the table is Python integers (the dtype `object`; the one use is the
    pointer of a detector set, a report of the host that is never refused,
    where the register would not hold the table): the same table."""
    dtype = object if exact else np.int64
    if exact:
        v, a = v.astype(dtype), a.astype(dtype)
    table = np.empty((a.shape[0], MOMENT_COLUMNS), dtype=dtype)
    table[:, 0] = a * v.any(axis=1)
    table[:, 1] = a - table[:, 0]
    table[:, 2 : 2 + DIMENSIONS] = v * a[:, None]
    table[:, 2 + DIMENSIONS : AGE_COLUMN] = a[:, None] * v[:, PAIR_I] * v[:, PAIR_J]
    if ages is None:
        table[:, AGE_COLUMN:] = 0
    else:
        weighted = a * np.asarray(ages).reshape(-1).astype(dtype)
        table[:, AGE_COLUMN] = weighted * v.any(axis=1)
        table[:, AGE_COLUMN + 1] = weighted - table[:, AGE_COLUMN]
    return table


def reading_of(sums: np.ndarray) -> Moments:
    """The `Moments` of summed moment-table rows (a leading axis kept)."""
    return Moments(
        sums[..., 0],
        sums[..., 1],
        sums[..., 2 : 2 + DIMENSIONS],
        sums[..., 2 + DIMENSIONS : AGE_COLUMN],
        sums[..., AGE_COLUMN],
        sums[..., AGE_COLUMN + 1],
    )


def moment_bound(amounts: np.ndarray, vectors: np.ndarray, ages: np.ndarray | None) -> int:
    """The largest entry a row of the moment table can hold: the amount
    times the larger of P^2 (the second moment) and the age (the age
    moment), so that one bound check covers every column."""
    per_row = max(1, int(np.abs(vectors).max(initial=0))) ** 2
    if ages is not None:
        per_row = max(per_row, int(np.abs(np.asarray(ages)).max(initial=0)))
    return int(np.abs(amounts).max(initial=0)) * per_row


def reading_fits(amounts: np.ndarray, vectors: np.ndarray, ages: np.ndarray | None, widest: int) -> bool:
    """Whether the moment table of `widest` rows of these amounts, vectors
    and ages fits the register: every entry at most `moment_bound` and
    every sum over at most `widest` rows, the product tested in Python
    integers before any product is formed. The one bound of the reading:
    `read_arrivals` refuses where it fails, `first_reading_overflow` looks
    per group where it fails, and the pointer takes its exact path there."""
    return moment_bound(amounts, vectors, ages) * widest <= MOMENTUM_BOUND


def read_groups(
    vectors: np.ndarray,
    weights: np.ndarray,
    starts: np.ndarray,
    ages: np.ndarray | None = None,
    exact: bool = False,
) -> Moments:
    """The one reading per contiguous group of rows (`starts` the first row
    of each group, the rows of a group adjacent): the moment table summed
    per group, in the register, the caller having checked the bound
    (`first_reading_overflow`), or, with `exact`, in Python integers (the
    pointer of a detector set where the register would not hold its table:
    a report of the host, never refused)."""
    return moments_of_groups(moment_table(vectors, weights, ages, exact=exact), starts)


def moments_of_groups(table: np.ndarray, starts: np.ndarray) -> Moments:
    """The `Moments` of a moment table summed per contiguous group of its
    rows (`starts` the first row of each group)."""
    return reading_of(np.add.reduceat(table, starts, axis=0))


def read_arrivals(
    vectors: np.ndarray,
    amounts: np.ndarray,
    keys: np.ndarray | None = None,
    size: int | None = None,
    ages: np.ndarray | None = None,
) -> Moments:
    """The one reading of a set of rays: `vectors` (rows, 3) the direction
    vector of each ray's arrival (D[direction] for a ray that arrived this
    interval, (0, 0, 0) for one that did not step) and `amounts` (rows,)
    its weight (the amount; the amplitude at the detector), summed as the
    moments of order 0, 1 and 2, exact integers: outside = the amounts on
    a nonzero vector, here = the amounts on the zero vector, the vector sum
    of amount x v, and the second moment sum amount x v v^T (its traceless
    part the tensor); with `ages` (rows,) also the age moment, sum amount x
    age, split outside and here the same way (zero without it). The age
    moment is a reading aid of the measured event, the external thing: the
    age is read whole only by a measured event (its clock's count on a
    table entry that reads `age`, its record); the GameBoard's rules (the
    flight, the collision) never read it whole; this component only helps
    the detector's computation and changes nothing on the GameBoard. With
    `keys` (rows,) and `size` the moments are taken per key (one reading
    per Node), the arrays gaining a leading axis of `size`. Valid for a fan
    as for the six headings: no projection onto the Ports."""
    v = np.asarray(vectors, dtype=np.int64).reshape(-1, DIMENSIONS)
    a = np.asarray(amounts, dtype=np.int64).reshape(-1)
    bins = None if keys is None else np.asarray(keys, dtype=np.int64).reshape(-1)
    # Every entry of the table is at most amount x P^2 (or amount x age)
    # and every sum has at most the rows of one key: the bound is checked
    # before a product is formed, so the integers below never wrap.
    rows = a.shape[0] if bins is None else int(np.bincount(bins, minlength=1).max(initial=0))
    if not reading_fits(a, v, ages, rows):
        raise reading_bound_error(rows, moment_bound(a, v, ages))
    table = moment_table(v, a, ages)
    if bins is None:
        sums = table.sum(axis=0)
    else:
        if size is None:
            raise ValueError(f"{BEAM_LAW}: a keyed reading needs its size")
        sums = np.zeros((size, MOMENT_COLUMNS), dtype=np.int64)
        np.add.at(sums, bins, table)
    return reading_of(sums)


# -- the clock's primitive over rows ----------------------------------------------


def by_clock_rows(age: np.ndarray, numerator: np.ndarray | int, denominator: int) -> np.ndarray:
    """`core.integer.by_clock` over rows: what the whole part of age x
    numerator / denominator gains at the self-creation that takes each
    row's age from `age` to `age + 1`, the first difference of a floor,
    exact on average with no remainder anywhere; the caller has bounded
    (age + 1) x numerator to the register. The one primitive of every
    rate of the law (the turn, the release, the lamp, the owed count, the
    step, the columns) and, since the four unifications (2026-09-20,
    BEAM_LAW note 33), of every age read against a key (`ages_at_key`)."""
    if denominator < 1:
        raise ValueError("positive denominator required")
    result: np.ndarray = ((age + 1) * numerator) // denominator - (age * numerator) // denominator
    return result


def ages_at_key(age: np.ndarray, key: int) -> np.ndarray:
    """The rows whose walk this interval brought their age to the key (a
    family's lifetime L; the world's age bound as the key age_bound + 1):
    `by_clock(age - 1, 1, key)` = 1, the one primitive read on the age
    before the walk against the key, exactly as the clock reads a measured
    event's turn off its age against K (the mathematician's clock_checks
    4: first at the age L, then every L). A row at age 0 (born this
    interval, or declared at rest at 0) has not walked and is never at
    the key."""
    result: np.ndarray = (age > 0) & (by_clock_rows(age - 1, 1, key) == 1)
    return result


# -- the flight table ------------------------------------------------------------


@dataclass(frozen=True)
class FlightTable:
    """One world constant per direction: v, S_1 = |a| + |b| + |c|,
    T_d = isqrt(3 |v|^2 Q^2), the Bresenham line of v (S_1 unit steps), the
    least period L_d of the flight phase, the step table (the Link a ray of
    direction d crosses at age tau: a heading, or zero for no move) and
    `labels`, the unit vector u_d of each direction at the scale Q
    (`unit_label`; (0, 0, 0) for a rest direction): the momentum label of
    one unit of amount along d, the same length within sqrt 3 / (2 Q) for
    every direction and exactly Q e_d on a heading."""

    vectors: np.ndarray
    manhattan: np.ndarray
    resolution: np.ndarray
    period: np.ndarray
    lines: np.ndarray
    steps: np.ndarray
    labels: np.ndarray

    def manhattan_steps(self, direction: np.ndarray, age: np.ndarray) -> np.ndarray:
        """m(tau) = (2 tau S_1 Q + T_d) // (2 T_d): the Manhattan steps made
        by age tau."""
        s1, t = self.manhattan[direction], self.resolution[direction]
        result: np.ndarray = (2 * age * s1 * Q + t) // (2 * t)
        return result


def unit_label(vector: Vector) -> Vector:
    """The unit vector of a direction at the scale Q: the integer vector
    nearest Q D / |D|, in integers only (the physics-rule reviewer's exact
    rule, 2026-09-19): with n = |D|^2, each component |a| is rounded as
    k(|a|) = (isqrt((2 Q |a|)^2 // n) + 1) // 2 and the sign restored, so
    that u_{-D} = -u_D exactly and u_{gD} = g u_D for the 48 signed axis
    permutations (k depends on |a| and n alone). Equal to the float
    rounding of Q |a| / |D| on every primitive direction with components
    in -64 .. 64 (0 mismatches over 1780418) and free of ties for any
    direction bound below 147 (a half-integer needs |D| a multiple of
    256). The six headings give exactly Q e_d; the zero vector gives the
    zero vector. Every component is within Q."""
    n = sum(c * c for c in vector)
    if n == 0:
        return ZERO3
    found = []
    for a in vector:
        t = 2 * Q * abs(a)
        k = (integer_root(t * t // n) + 1) // 2
        found.append(k if a >= 0 else -k)
    return found[0], found[1], found[2]


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
    resolution = np.ones(count, dtype=np.int64)
    period = np.ones(count, dtype=np.int64)
    lines_list: list[list[tuple[int, int, int]]] = []
    for index, vector in enumerate(vectors):
        s1 = sum(abs(c) for c in vector)
        manhattan[index] = s1
        if s1 == 0:
            lines_list.append([])
            continue
        t = integer_root(3 * sum(c * c for c in vector) * Q * Q)
        resolution[index] = t
        p = t // bounded_gcd(s1 * Q, t)
        per_period = s1 * Q * p // t
        period[index] = p * (s1 // bounded_gcd(per_period, s1))
        lines_list.append(_bresenham(vector))
    longest = max(1, int(manhattan.max(initial=0)))
    lines = np.zeros((count, longest, 3), dtype=np.int64)
    for index, line in enumerate(lines_list):
        for j, step in enumerate(line):
            lines[index, j] = step
    # The label table: the unit vector of every direction at the scale Q.
    labels = np.array([unit_label(vector) for vector in vectors], dtype=np.int64).reshape(count, 3)
    table = FlightTable(
        np.array(vectors, dtype=np.int64).reshape(count, 3),
        manhattan,
        resolution,
        period,
        lines,
        np.zeros(0),
        labels,
    )
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
    return FlightTable(table.vectors, manhattan, resolution, period, lines, steps, labels)


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


@functools.lru_cache(maxsize=1)
def collision_table() -> CollisionTable:
    """Generated from its rule over the classes, never written by hand: the
    members of a class sorted as 8-tuples, the forward map the cyclic shift
    by +1, the inverse by -1; a class of one is fixed. A constant of the
    law (the 3^8 states), generated once per process and shared read-only
    by every `NatureBeamSimulation` (the arrays refuse a write)."""
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
    for array in (forward, inverse, singles, powers):
        array.setflags(write=False)
    return CollisionTable(forward, inverse, singles, powers)


@dataclass(frozen=True)
class NatureBeamTables:
    """The two pure tables of a world and the circle's tables: the flight
    table of its direction set, the collision table, the cosines and sines
    at 1/256 and the window table (whether a phase distance is inside the
    half circle centred on the setting)."""

    flight: FlightTable
    collision: CollisionTable
    cosines: np.ndarray
    sines: np.ndarray
    window: np.ndarray


def nature_beam_tables(world: NatureBeamWorld) -> NatureBeamTables:
    modulus = world.phase_steps
    distance = np.arange(modulus, dtype=np.int64)
    window = (4 * distance < modulus) | (4 * distance >= 3 * modulus)
    return NatureBeamTables(
        flight_table(world.directions),
        collision_table(),
        np.array(phase_cosines(modulus), dtype=np.int64),
        np.array(phase_sines(modulus), dtype=np.int64),
        window,
    )


# -- the store -------------------------------------------------------------------

FIELDS = ("node", "direction", "age", "phase", "number", "amount", "content", "arrival")
# The fields that make two rows identical (the amount is what the merge adds).
IDENTITY_FIELDS = ("node", "direction", "age", "phase", "number", "content")


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


def label_bound_error(
    amount: int, content: int, free: bool, unit: Vector, node: Address3 | None
) -> OverflowError:
    """The refusal of a row whose momentum label could pass the bound,
    naming the Node, the amount, the content, the unit vector of the
    direction and the product that would leave the register."""
    weight = amount if free else amount * content
    reach = max(abs(component) for component in unit)
    where = "" if node is None else f" at Node {list(node)}"
    return OverflowError(
        f"{BEAM_LAW}: the momentum label of a row of amount {amount} and content {content}{where} "
        f"along {list(unit)}, its weight {weight} times the largest component {reach} = "
        f"{weight * reach}, exceeds the integer bound {MOMENTUM_BOUND}"
    )


def label_overflow_rows(
    amount: np.ndarray, content: np.ndarray, free: bool, unit: np.ndarray
) -> np.ndarray:
    """The pre-check of the one label, per row and BEFORE any product is
    formed (ARCHITECTURE: never wrap): a row overflows when its weight
    (the amount for a free family, content x amount for a paid one) cannot
    be formed in the register, or when the weight times the largest
    component of its unit vector `unit` (rows, 3) exceeds the bound. Both
    products are tested by division, so nothing wraps in the test itself.
    Returns the mask of the overflowing rows."""
    a = np.abs(np.asarray(amount, dtype=np.int64))
    if free:
        fits = np.ones(a.shape, dtype=bool)
        weight = a
    else:
        c = np.abs(np.asarray(content, dtype=np.int64))
        fits = a <= MOMENTUM_BOUND // np.maximum(c, 1)
        weight = a * np.where(fits, c, 0)
    reach = np.abs(np.asarray(unit, dtype=np.int64)).max(axis=1)
    result: np.ndarray = ~fits | ((reach > 0) & (weight > MOMENTUM_BOUND // np.maximum(reach, 1)))
    return result


def label_weights(amount: np.ndarray, content: np.ndarray, free: bool) -> np.ndarray:
    """The weight of a row's momentum label: the amount for a free family
    (its unit carries no content; its label is the unit), content x amount
    for a paid one. The product is bounded before it is formed: a row
    whose content x amount could leave the register is refused. The label
    itself, the weight along the unit vector, is bounded per direction by
    `momentum_labels`, the one place a label is formed."""
    weight = np.asarray(amount, dtype=np.int64)
    if free:
        return weight
    c = np.asarray(content, dtype=np.int64)
    over = np.flatnonzero(np.abs(weight) > MOMENTUM_BOUND // np.maximum(np.abs(c), 1))
    if over.shape[0]:
        i = int(over[0])
        raise label_bound_error(int(weight[i]), int(c[i]), free, ZERO3, None)
    result: np.ndarray = weight * c
    return result


def momentum_labels(
    labels: np.ndarray,
    direction: np.ndarray,
    amount: np.ndarray,
    content: np.ndarray,
    free: bool,
    node: np.ndarray | Address3 | None = None,
) -> np.ndarray:
    """The one momentum label of rows of rays, (rows, 3): the label weight
    (`label_weights`) along the unit vector of the direction at the scale
    Q (`labels`, the flight table's `labels`), content x amount x u_d for
    a paid family, amount x u_d for a free one. The product is checked
    BEFORE it is formed, per row, weight x max|u_d| within 2^62 - 1
    (`label_overflow_rows`); the first row beyond it is refused loudly
    naming its Node (`node`: the coordinates per row, (rows, 3), or the
    one Node of every row) and its amount. Every place a label is formed
    (a birth, a re-emission, a home, a face click, the transit line's
    recount) comes through here or through the same per-row rule taken
    in bulk (`first_label_overflow`)."""
    d = np.asarray(direction, dtype=np.int64)
    unit = labels[d]
    over = np.flatnonzero(label_overflow_rows(amount, content, free, unit))
    if over.shape[0]:
        i = int(over[0])
        where: Address3 | None
        if node is None:
            where = None
        elif isinstance(node, np.ndarray):
            where = (int(node[i, 0]), int(node[i, 1]), int(node[i, 2]))
        else:
            where = node
        raise label_bound_error(
            int(amount[i]),
            int(content[i]),
            free,
            (int(unit[i, 0]), int(unit[i, 1]), int(unit[i, 2])),
            where,
        )
    weight = label_weights(amount, content, free)
    result: np.ndarray = unit * weight[:, None]
    return result


def circle_vectors(phase: np.ndarray, cosines: np.ndarray, sines: np.ndarray) -> np.ndarray:
    """The unit vectors of the circle at the rows' phases, (rows, 3): the
    table entries (C[phase], S[phase], 0) in 256ths, the vectors the one
    reading takes the pointer on as it takes the flow on the directions'
    unit vectors u_d."""
    return np.stack([cosines[phase], sines[phase], np.zeros(phase.shape[0], dtype=np.int64)], axis=1)


def coherent_pointer(
    amount: np.ndarray,
    phase: np.ndarray,
    starts: np.ndarray,
    cosines: np.ndarray,
    sines: np.ndarray,
) -> tuple[list[int], list[int]]:
    """The coherent pointer (X, Y) of rows per contiguous group (a detector
    set's arrivals or its clicks of one family this interval; a face's or
    the border's): the first moment of the one reading over the circle
    (the four unifications, the model owner, 2026-09-20; BEAM_LAW note
    33), `read_groups` on the circle's unit vectors (C[phase], S[phase],
    0) with the amplitudes 32 x amount (`AMPLITUDE_SCALE`) as the weights,
    so that X = sum 32 x amount x C[phase] and Y = sum 32 x amount x
    S[phase] integer by integer; the record is |M_1|^2 and the set's phase
    its nearest step (`pointer_phases`). Taken in the int64 register where
    the reading's bound holds for the table (`reading_fits`) and in Python
    integers where the reading would refuse (`exact`): exact either way, a
    report never refused. Python integers out."""
    vectors = circle_vectors(phase, cosines, sines)
    widest = int(group_sizes(starts, amount.shape[0]).max(initial=0))
    # The amplitude 32 x amount is formed in the register only where it
    # fits (tested by division) and where the reading's bound then holds.
    if int(np.abs(amount).max(initial=0)) <= MOMENTUM_BOUND // AMPLITUDE_SCALE:
        weights = amount * AMPLITUDE_SCALE
        exact = not reading_fits(weights, vectors, None, widest)
    else:
        weights = amount.astype(object) * AMPLITUDE_SCALE
        exact = True
    flow = read_groups(vectors, weights, starts, exact=exact).flow
    x: list[int] = flow[:, 0].tolist()
    y: list[int] = flow[:, 1].tolist()
    return x, y


# The square of the pointer of one unit at phase 0: (32 x 256)^2 = 2^26,
# the unit in which a `wave` set's threshold reads the pointer's square
# (`pointer_units`).
POINTER_UNIT = (AMPLITUDE_SCALE * PHASE_COSINE_SCALE) ** 2


def pointer_units(x: int, y: int) -> int:
    """The square of the coherent pointer (X, Y) in units of one ray: the
    nearest integer to (X^2 + Y^2) / 2^26, the square of one unit's pointer
    at phase 0 (the model owner, 2026-09-20, issue #359: under `wave` a
    detector's threshold reads the pointer's square, so that rays which
    cancel do not click). One unit at any phase reads 1 for every N through
    4096 (the tables' C^2 + S^2 is within 361 of 65536, section 5), a rays
    in phase read a^2 (exactly through a = 11 at N = 64, the tables'
    rounding entering beyond), two opposite rays 0, two a quarter turn apart
    2. Python integers, exact, never refused."""
    return (x * x + y * y + POINTER_UNIT // 2) // POINTER_UNIT


# The pointer's components up to which the nearest step is read in the
# int64 register (a component times a table entry inside 2^62 - 1).
POINTER_STEP_BOUND = MOMENTUM_BOUND // LONGEST_PHASE_ENTRY


def pointer_phases(
    x: list[int], y: list[int], cosines: np.ndarray, sines: np.ndarray
) -> list[int | None]:
    """The nearest step of the phase circle to each pointer (X, Y): the
    step k whose table entry (C[k], S[k]) is nearest in direction, the
    one with the smallest |X S[k] - Y C[k]| among those with X C[k] + Y
    S[k] > 0 (the lowest k on a tie), exact integers; a pointer of one
    ray at phase p reads p wherever the 1/256 tables tell the steps apart
    (`test_nature_beam_detector` (g)); a zero pointer has no step (None). In the
    register while every component is within `POINTER_STEP_BOUND`, in
    Python integers beyond it."""
    if not x:
        return []
    if max(max(map(abs, x)), max(map(abs, y))) <= POINTER_STEP_BOUND:
        px = np.array(x, dtype=np.int64)[:, None]
        py = np.array(y, dtype=np.int64)[:, None]
        cross = np.abs(px * sines[None, :] - py * cosines[None, :])
        ahead = px * cosines[None, :] + py * sines[None, :] > 0
        cross[~ahead] = np.iinfo(np.int64).max
        steps = cross.argmin(axis=1).tolist()
        return [None if not ahead[k].any() else int(steps[k]) for k in range(len(x))]
    found: list[int | None] = []
    for px_k, py_k in zip(x, y, strict=True):
        best: int | None = None
        least = 0
        for k, (c, s) in enumerate(zip(cosines.tolist(), sines.tolist(), strict=True)):
            if px_k * c + py_k * s <= 0:
                continue
            distance = abs(px_k * s - py_k * c)
            if best is None or distance < least:
                best, least = k, distance
        found.append(best)
    return found


class NatureBeamStore:
    """The records of one family as a structure of arrays, one row per
    record: `node` the flat index, `direction`, `age` (whole: the intervals
    since the measured event that created the ray; rows of different ages
    are distinct rows, the host cost of the whole age), `phase`, `number`,
    `amount`, `content` (per unit) and `arrival`, the direction the ray arrived on this interval (its
    direction at the walk; the reading is of the arrivals) or `NO_ARRIVAL` for a
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

    def merge_key(self) -> np.ndarray | None:
        """The identity fields packed into one integer key per row, in the
        order of `IDENTITY_FIELDS` (the Node first) with every field offset
        to its least value, so that the keys order the rows exactly as the
        lexsort of the fields does and equal keys are identical rows; None
        when the fields' ranges do not fit the register (62 bits), the
        lexsort then taking the same total order."""
        columns = [getattr(self, name) for name in IDENTITY_FIELDS]
        lows = [int(column.min()) for column in columns]
        widths = [
            (int(column.max()) - low).bit_length() for column, low in zip(columns, lows, strict=True)
        ]
        if sum(widths) > 62:
            return None
        key = np.zeros(self.size, dtype=np.int64)
        for column, low, width in zip(columns, lows, widths, strict=True):
            key = (key << width) + (column - low)
        return key

    def merge(self) -> None:
        """Identical rows (equal in every field but the amount) merged, the
        amounts added, the rows in the total order of the identity fields,
        the Node first (so no second sort by Node is needed). A bijection: a
        permutation of rows and a sum of interchangeable units. The order
        is taken by the one packed key (`merge_key`) where the fields fit
        the register, by the lexsort of the fields otherwise: the same
        total order either way."""
        if self.size == 0:
            return
        key = self.merge_key()
        same = np.zeros(self.size, dtype=bool)
        if key is None:
            order = np.lexsort(tuple(getattr(self, name) for name in reversed(IDENTITY_FIELDS)))
            self.take(order)
            same[1:] = True
            for name in IDENTITY_FIELDS:
                column = getattr(self, name)
                same[1:] &= column[1:] == column[:-1]
        else:
            order = np.argsort(key, kind="stable")
            self.take(order)
            key = key[order]
            same[1:] = key[1:] == key[:-1]
        starts = np.flatnonzero(~same)
        # The merged amounts are exact: in the register when no group's sum
        # can leave it, in Python integers otherwise, and bounded.
        if int(self.amount.max()) * self.size <= MOMENTUM_BOUND:
            amount = np.add.reduceat(self.amount, starts)
        else:
            merged = np.add.reduceat(self.amount.astype(object), starts)
            if max(int(v) for v in merged) > MOMENTUM_BOUND:
                raise OverflowError(
                    f"{BEAM_LAW}: the amount of a merged row exceeds the integer bound {MOMENTUM_BOUND}"
                )
            amount = merged.astype(np.int64)
        self.keep(~same)
        self.amount = amount
        self.arrival[:] = NO_ARRIVAL

    def slice(self, flat: int) -> tuple[int, int]:
        """The contiguous rows of one Node in the sorted store."""
        lo = int(np.searchsorted(self.node, flat, side="left"))
        hi = int(np.searchsorted(self.node, flat, side="right"))
        return lo, hi

    def rows(self, lo: int = 0, hi: int | None = None) -> list[NatureBeam]:
        """The records of the rows `lo` to `hi` (every row by default): the
        one materialization of a ray's record (`NatureBeam`)."""
        stop = self.size if hi is None else hi
        x, y, z = self.coordinates(self.node[lo:stop])
        return [
            NatureBeam(
                (int(x[k]), int(y[k]), int(z[k])),
                int(self.direction[i]),
                int(self.age[i]),
                int(self.phase[i]),
                int(self.number[i]),
                int(self.amount[i]),
                int(self.content[i]),
            )
            for k, i in enumerate(range(lo, stop))
        ]

    def labels(self, rows: np.ndarray, unit: np.ndarray, free: bool) -> np.ndarray:
        """The momentum labels of the given rows (`momentum_labels`, the one
        label of the law) along the unit vectors `unit` (the flight table's
        `labels`)."""
        return momentum_labels(
            unit,
            self.direction[rows],
            self.amount[rows],
            self.content[rows],
            free,
            np.stack(self.coordinates(self.node[rows]), axis=1),
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
            f"{BEAM_LAW}: the {quantity} of measured event {entry.number} at "
            f"{list(entry.position)} exceeds the integer bound {MOMENTUM_BOUND}"
        )
    return value


@dataclass(frozen=True)
class ArrivalRows:
    """One family's rows as the walk left them, held for the readings on
    request: the Node, the direction each row arrived on (`NO_ARRIVAL` for a row
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


class GameBoardDiagnostics:
    """The interval's readings per family, dense over the GameBoard, decomposed
    on request from the rows of the walk (diagnostics for the engine's
    shell means and flux; the law reads none of them, its own readings
    being taken at the measured events in step 4): the amount that arrived
    per Node (the zeroth moment outside), its net flow (the first moment,
    on the unit vectors u_d at the scale Q: Q per unit of amount along a
    heading, the same length for a fan direction), the presence of every
    ray (the zeroth moment whole) and, a diagnostic of the walk and not of
    the reading, the amount that crossed into each Node through each of
    its six Ports this interval (`per_port`, the Links crossed, for
    Gauss's flux, in units of amount). Only the active Nodes (the Nodes
    with rows) are decomposed, by the one keyed `read_arrivals` with its
    bound; every other Node is zero."""

    def __init__(self, shape: Address3, vectors: np.ndarray, rows: list[ArrivalRows]) -> None:
        self.shape = shape
        # The unit vectors of the directions (the flight table's `labels`).
        self.vectors = vectors
        self.rows = rows
        self._moments: tuple[list[np.ndarray], list[np.ndarray], list[np.ndarray]] | None = None
        self._per_port: list[np.ndarray] | None = None

    @property
    def nodes(self) -> int:
        return self.shape[0] * self.shape[1] * self.shape[2]

    def _decompose(self) -> tuple[list[np.ndarray], list[np.ndarray], list[np.ndarray]]:
        if self._moments is None:
            arrived: list[np.ndarray] = []
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
                    vector[active] = reading.flow
                    scalar[active] = reading.presence
                arrived.append(outside.reshape(self.shape))
                flow.append(vector.reshape((*self.shape, DIMENSIONS)))
                presence.append(scalar.reshape(self.shape))
            self._moments = (arrived, flow, presence)
        return self._moments

    @property
    def arrived(self) -> list[np.ndarray]:
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


FIRST = np.zeros(1, dtype=np.int64)
NEW_RUN = np.ones(1, dtype=bool)


def group_starts(keys: np.ndarray) -> np.ndarray:
    """The first index of every run of equal keys in a grouped array."""
    if keys.shape[0] == 0:
        return np.zeros(0, dtype=np.int64)
    return np.concatenate((FIRST, np.flatnonzero(keys[1:] != keys[:-1]) + 1))


def group_sizes(starts: np.ndarray, count: int) -> np.ndarray:
    """The rows of every group given the group starts and the row count."""
    result: np.ndarray = np.append(starts[1:], count) - starts
    return result


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
    group: np.ndarray,
    groups: int,
    amounts: np.ndarray,
    vectors: np.ndarray,
    ages: np.ndarray | None = None,
) -> tuple[int, OverflowError] | None:
    """The bound of `read_arrivals` taken per group in bulk, the same
    condition per group as the per-set reading: None when every group
    passes (decided by the maxima over all groups where they suffice),
    else the first failing group in group order with the error the per-set
    reading raises."""
    if amounts.shape[0] == 0:
        return None
    a = np.abs(amounts)
    counts = np.bincount(group, minlength=groups)
    if reading_fits(a, vectors, ages, int(counts.max())):
        return None
    a_max = np.zeros(groups, dtype=np.int64)
    np.maximum.at(a_max, group, a)
    per_max = np.zeros(groups, dtype=np.int64)
    np.maximum.at(per_max, group, np.abs(vectors).max(axis=1) ** 2)
    if ages is not None:
        np.maximum.at(per_max, group, np.abs(ages))
    for g in range(groups):
        per_row = int(a_max[g]) * max(1, int(per_max[g]))
        if per_row * int(counts[g]) > MOMENTUM_BOUND:
            return g, reading_bound_error(int(counts[g]), per_row)
    return None


def first_label_overflow(
    group: np.ndarray,
    amount: np.ndarray,
    content: np.ndarray,
    free: bool,
    unit: np.ndarray,
    node_of: Callable[[int], Address3],
) -> tuple[int, OverflowError] | None:
    """The pre-check of `momentum_labels` taken per group in bulk, the same
    per-row rule (`label_overflow_rows`: the weight times the largest
    component of the row's unit vector `unit` within the bound, tested
    before any product): None when every row passes, else the lowest
    failing group with the error the per-row check raises, naming the
    Node of its first failing row (`node_of` maps a row index to its
    Node) and the row's amount."""
    if amount.shape[0] == 0:
        return None
    over = np.flatnonzero(label_overflow_rows(amount, content, free, unit))
    if over.shape[0] == 0:
        return None
    g = int(group[over].min())
    i = int(over[group[over] == g][0])
    return g, label_bound_error(
        int(amount[i]),
        int(content[i]),
        free,
        (int(unit[i, 0]), int(unit[i, 1]), int(unit[i, 2])),
        node_of(i),
    )


def first_moment_overflow(
    group: np.ndarray, groups: int, weights: np.ndarray, unit: np.ndarray
) -> tuple[int, OverflowError] | None:
    """The bound of a label flow taken per group in bulk: the sum of
    weight x u_d over a group's rows, each component within the weight
    times the largest component of u_d (Q at most) per row, so the check
    is weight x |u| x rows against the bound (a first moment: no second
    moment is formed). None when every group passes, else the first
    failing group in group order with the reading's error."""
    if weights.shape[0] == 0:
        return None
    w = np.abs(weights)
    v = np.abs(unit).max(axis=1)
    counts = np.bincount(group, minlength=groups)
    if int(w.max()) * max(1, int(v.max())) * int(counts.max()) <= MOMENTUM_BOUND:
        return None
    w_max = np.zeros(groups, dtype=np.int64)
    np.maximum.at(w_max, group, w)
    v_max = np.zeros(groups, dtype=np.int64)
    np.maximum.at(v_max, group, v)
    for g in range(groups):
        per_row = int(w_max[g]) * max(1, int(v_max[g]))
        if per_row * int(counts[g]) > MOMENTUM_BOUND:
            return g, reading_bound_error(int(counts[g]), per_row)
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
    t_amount: list[int] = field(default_factory=list)
    t_content: list[int] = field(default_factory=list)
    t_phase: list[int] = field(default_factory=list)
    t_carried: list[int] = field(default_factory=list)
    t_label: list[list[int]] = field(default_factory=list)
    # The detector set's reading of what clicked, per set: under `wave` the
    # coherent pointer (X, Y), exact; under `beam` the count clicked; and
    # the set's phase (None for a zero pointer). The units a beam set
    # paired and passed on, per measured event: (number, amount, phase).
    pointer: dict[int, tuple[int, int]] = field(default_factory=dict)
    count: dict[int, int] = field(default_factory=dict)
    set_phase: dict[int, int | None] = field(default_factory=dict)
    cancelled: dict[int, list[tuple[int, int, int]]] = field(default_factory=dict)
    # The label sum of the rows that leave the store this interval (the
    # home rows and the rows a table absorbs): off the running transit line.
    left_momentum: list[int] = field(default_factory=lambda: [0, 0, 0])


# -- the push -------------------------------------------------------------------


def column_bound_error(entry: Measured, name: str, moment: int, factor: int) -> OverflowError:
    """The refusal of a column's product |V| x |E n| that would leave the
    register, naming the measured event, its Node and the column."""
    return OverflowError(
        f"{BEAM_LAW}: the push of measured event {entry.number} at {list(entry.position)} exceeds "
        f"the integer bound {MOMENTUM_BOUND} in the column {name!r}: |V| x |E n| = {abs(moment)} x "
        f"{factor}"
    )


def push_form(
    free: bool,
    moment: list[int],
    charges: list[tuple[int, int]],
    values: tuple[tuple[int, int], ...],
    columns: tuple[tuple[str, int], ...],
    age: int,
    entry: Measured,
) -> list[int]:
    """The push a measured event A takes from one group of arriving rays:
    ONE signed inner product over the columns (the model owner's decision
    of 2026-09-20, "one mechanism for all the laws on the GameBoard"; the
    mathematician's verified form). `moment` is V_B, the label flow of
    the group (Python integers, exact); `charges` the reader's charge in
    every column as the frame read it, the pairs (E_c, D_c) (gravity: its
    content M_A over 1; charge: rho_A M_A; a declared column: its value
    times the content, summed over the families it holds); `values` the
    arriving family's value per unit of content in every column, the pairs
    (n_c, d_c) (gravity (1, 1), charge rho_B, a declared column's value or
    (0, 1)); `columns` the world's (name, sign) per column; `age` the
    reader's clock age, the age before this interval's self-creation, at
    which every rate of the law is read (the turn, the release, the owed
    count, the step; the four unifications, the model owner, 2026-09-20,
    (4), BEAM_LAW note 33: until then the columns alone were floored at
    the age after the frame's advance, note 20). For a free family's rays,
    per axis,

        push_A = sum over the columns c of
                 epsilon_c x sign(V E_c n_c) x by_clock(age_A, |V x E_c x n_c|, D_c x d_c),

    every column's rational part the whole part off the reader's clock by
    its own denominators, floored on its own and never summed before the
    floor (the mathematician's section 4: the sum of the columns' whole
    parts is today's integer, a whole part of the sum is not); a column
    with E_c n_c = 0 adds nothing. The gravity column, (1, 1) on every
    family with the sign minus, is `by_clock(age, |V M_A|, 1) = |V M_A|`
    exactly, the law's -M_A V_B; the charge column is the electric part as
    landed, `sign(V n_A n_B) x by_clock(age_A, |V n_A n_B M_A|, d_A d_B)`
    (the same rational at the same clock), so a world without a declared
    column reads the two-column form M_A (rho_A rho_B - 1) x V_B integer by
    integer, and the strong force is a third column with the sign minus,
    not a term of this function. For a paid family's rays the push is V_B
    itself (kappa = 1, the label carries h s). The bounds (the
    mathematician's R1 to R3): each column's product |V| x |E_c n_c| is
    tested by division BEFORE it is formed and refused naming the column;
    the partial sum is bounded after every column (`bounded`); the caller
    bounds the momentum it joins."""
    if not free:
        return [bounded(moment[axis], entry, "push") for axis in range(3)]
    push = [0, 0, 0]
    for (name, sign), (numerator, denominator), (n, d) in zip(columns, charges, values, strict=True):
        if not numerator or not n:
            continue
        divisor = denominator * d
        for axis in range(3):
            v = moment[axis]
            if not v:
                continue
            # |V| x |E n| tested by division before either product is formed.
            if abs(numerator) > MOMENTUM_BOUND // abs(n):
                raise column_bound_error(entry, name, v, abs(numerator) * abs(n))
            factor = numerator * n
            if abs(v) > MOMENTUM_BOUND // abs(factor):
                raise column_bound_error(entry, name, v, abs(factor))
            total = v * factor
            whole = abs(total) if divisor == 1 else by_clock(age, abs(total), divisor)
            push[axis] = bounded(push[axis] + sign * (-whole if total < 0 else whole), entry, "push")
    return push


# -- the law ---------------------------------------------------------------------


def nature_beam(
    stores: list[NatureBeamStore],
    world: NatureBeamWorld,
    tables: NatureBeamTables,
    measured: dict[int, Measured],
    tick: int,
    record: Record | None,
    ledger: Ledger,
    inverse: bool = False,
) -> GameBoardDiagnostics:
    """A Node's whole interval for the rays present, at every Node (the
    module docstring, steps 1 to 6). With `inverse` the bijective steps are
    run in reverse order with their inverses (the collision, then the walk)
    on a GameBoard without measured events; the border has no inverse."""
    families = world.families
    free_of = [definition.free for definition in families]
    # The columns of the world, (name, sign), and every family's value per
    # column: the arriving side of the push (the reader's side is the
    # charges the frame read).
    columns = world.columns
    values_of = [definition.values for definition in families]
    flight, collision = tables.flight, tables.collision
    # The unit vectors of the directions at the scale Q: what every label
    # and every vector or tensor moment of the reading is taken on.
    unit = flight.labels
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
    # Every Node of every set maps to its measured event (`DetectorSet.nodes`,
    # the one set object of a body and a detector): the rows at any Node of
    # a body are its arrivals, read as one set (the threshold over the
    # detector set, the presence and the push over the body), and no
    # collision acts at any of them.
    node_event = np.full(nodes, -1, dtype=np.int64)
    if events:
        which_of = {entry.number: which for which, entry in enumerate(entries)}
        for detector_set in {entry.detector_set.index: entry.detector_set for entry in entries}.values():
            for member_node, number in detector_set.nodes.items():
                node_event[stores[0].flat(member_node)] = which_of[number]
    occupied = node_event >= 0

    def collide(store: NatureBeamStore, backward: bool) -> None:
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
                f"{BEAM_LAW}: the inverse interval is defined on a GameBoard without measured events"
            )
        for definition in families:
            if definition.lifetime is not None:
                raise ValueError(
                    f"{BEAM_LAW}: the inverse interval is refused with the family "
                    f"{definition.name!r} of lifetime {definition.lifetime} on the GameBoard: the "
                    "click on the border `lifetime` has no inverse (as a face click has none)"
                )
        for family, store in enumerate(stores):
            if store.size == 0:
                continue
            collide(store, backward=True)
            resting = store.direction < REST_DIRECTIONS
            # The age back by one (whole; a rest ray keeps its age); the
            # flight table is read modulo the period. A ray at age 0 is at
            # its birth, which has no inverse.
            back = np.where(resting, store.age, store.age - 1)
            if (back < 0).any():
                raise ValueError(
                    f"{BEAM_LAW}: the inverse walk of a ray at age 0 (its birth has no inverse)"
                )
            step = flight.steps[store.direction, back % flight.period[store.direction]].astype(np.int64)
            moved = step.any(axis=1)
            x, y, z = store.coordinates(store.node)
            coordinates = np.stack([x, y, z], axis=1) - step
            for axis in range(3):
                if world.periodic[axis]:
                    coordinates[:, axis] %= extents[axis]
                elif ((coordinates[:, axis] < 0) | (coordinates[:, axis] >= extents[axis])).any():
                    raise ValueError(
                        f"{BEAM_LAW}: the inverse walk crosses an open face (a click has no inverse)"
                    )
            store.node = coordinates @ np.array(store.strides, dtype=np.int64)
            store.age = back
            store.phase = (store.phase - families[family].phase_per_link * moved) % modulus
            store.arrival[:] = NO_ARRIVAL
            store.merge()
        return GameBoardDiagnostics(shape, unit, [])

    # 1. The walk: departures become arrivals; the escapes click on the faces.
    arrivals: list[ArrivalRows] = []
    for family, store in enumerate(stores):
        definition = families[family]
        if store.size == 0:
            arrivals.append(ArrivalRows.empty())
            continue
        # The flight reads the age modulo the direction's period, its
        # place on the digital line; the age itself is kept whole.
        step = flight.steps[store.direction, store.age % flight.period[store.direction]].astype(np.int64)
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
        arrival = np.where(moved, store.direction, NO_ARRIVAL)
        if escaped.any():
            gone = np.flatnonzero(escaped)
            labels = store.labels(gone, unit, definition.free)
            for face in ledger.open_faces:
                on_face = port[gone] == face
                through = gone[on_face]
                if through.shape[0] == 0:
                    continue
                amounts = store.amount[through]
                # The face's record: the clicked amount summed exactly, the
                # coherent pointer of what clicked (the amplitudes at their
                # phases) and its square, exact Python integers (a report,
                # never refused; the face's record is one sum per face).
                total = int(exact_sum(amounts))
                ledger.face_amount[face][family] += total
                ledger.face_content[face][family] += int(exact_sum(amounts * store.content[through]))
                face_x, face_y = coherent_pointer(
                    amounts, store.phase[through], FIRST, tables.cosines, tables.sines
                )
                ledger.face_record[face][family] += face_x[0] * face_x[0] + face_y[0] * face_y[0]
                escaped_momentum = exact_column_sums(labels[on_face])
                ledger.face_momentum[face][family] = [
                    a + b
                    for a, b in zip(ledger.face_momentum[face][family], escaped_momentum, strict=True)
                ]
                ledger.transit_momentum = [
                    a - b for a, b in zip(ledger.transit_momentum, escaped_momentum, strict=True)
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
        # alphabet, whose line it resumes when a collision moves it); a
        # moving ray's age advances by one, whole.
        resting = store.direction < REST_DIRECTIONS
        store.age = np.where(resting, store.age, store.age + 1)
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
    # local sets) and, for the diagnostics of the whole GameBoard, on request
    # from the rows of the walk (the active Nodes only; `GameBoardDiagnostics`).
    readings = GameBoardDiagnostics(shape, unit, arrivals)

    # 3. The collision.
    for store in stores:
        collide(store, backward=False)

    # 4. The measured events' tables and the detectors, the same rule at
    # every measured event taken in bulk by the host: the rows at measured
    # events found by one gather per family, the reading sets grouped by
    # detector set (the threshold and, under `wave`, the window on the set's
    # phase; the model owner, 2026-09-19: a detector is a set of Nodes with
    # ONE record) and by (measured event, number) with one segmented sum per
    # moment, every bound checked per group in bulk; then the records and
    # the side effects applied per group in the order of the records (by
    # number, family, other number, row), Python integers only, no
    # reduction reordered. The physics of an arrival stays at its Node (the
    # content joins, the push, the labels, the re-emission); only the
    # reading is over the set.
    keep = [np.ones(store.size, dtype=bool) for store in stores]
    for entry in entries:
        entry.presence = 0
        entry.counted = 0
    if events:
        count = len(families)
        ev_number = np.array([e.number for e in entries], dtype=np.int64)
        ev_rule = np.array([[RULE_CODES[r] for r in e.table] for e in entries], dtype=np.int64)
        ev_window = np.array(
            [[-1 if w is None else w for w in e.windows] for e in entries], dtype=np.int64
        )
        # The detector set of every measured event, its threshold and its
        # reading, indexed by the set's index.
        ev_set = np.array([e.detector_set.index for e in entries], dtype=np.int64)
        set_of = {e.detector_set.index: e.detector_set for e in entries}
        set_count = int(ev_set.max()) + 1
        st_threshold = np.ones(set_count, dtype=np.int64)
        st_wave = np.zeros(set_count, dtype=bool)
        for set_index, detector_set in set_of.items():
            st_threshold[set_index] = detector_set.threshold
            st_wave[set_index] = detector_set.wave
        half = modulus // 2
        presence = np.zeros((count, events), dtype=np.int64)
        # The age moment over the same set, the measured event's reading of
        # the whole age (a reading aid of the external thing; the GameBoard's
        # rules never read the age whole), and per (family, measured event)
        # whether its table entry counts it in place of the presence.
        age_moment = np.zeros((count, events), dtype=np.int64)
        counts_age = np.array(
            [[count_component(reads) == AGE_READS for reads in e.reads] for e in entries],
            dtype=bool,
        ).T.reshape(count, events)
        # The refusals found in bulk, keyed by the point at which the rule
        # taken per set raises them, (measured event, family, part, group
        # rank, stage), and raised at that point below.
        failures: dict[tuple[int, int, int, int, int], OverflowError] = {}

        def family_plan(family: int, store: NatureBeamStore) -> FamilyPlan | None:
            free = free_of[family]
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
            age_at = store.age[at]
            own = number == ev_number[ev]
            arrived = arrival != NO_ARRIVAL
            plan = FamilyPlan()
            # The rows of the one reading over the set: every row at the set
            # of another number, rest and moving alike, on the unit vector of
            # its arrival (a row that did not step on the zero vector; at a
            # measured event's Node the arrival is the direction, no
            # collision acting there), the amounts as the weights and the
            # ages among them; the bound of the table checked in bulk here,
            # the table itself taken once below with the admitted rows.
            others = np.flatnonzero(~own)
            v_others = unit[arrival[others]]
            if others.shape[0]:
                overflow = first_reading_overflow(
                    ev[others], events, amount[others], v_others, age_at[others]
                )
                if overflow is not None:
                    failures[(overflow[0], family, 0, 0, 0)] = overflow[1]
            # Home: the own number's arrivals, taken to be created again; a
            # paid family's labels join the momentum (the units are moved,
            # not copied: the recoil at the re-creation gives them back).
            home = np.flatnonzero(own & arrived)
            if home.shape[0]:
                ev_h = ev[home]
                starts = group_starts(ev_h)
                sizes = group_sizes(starts, home.shape[0])
                widest = int(sizes.max())
                total = grouped_sums(amount[home], starts, widest)
                carried = grouped_sums(amount[home] * content[home], starts, widest)
                taken_in = np.zeros((starts.shape[0], DIMENSIONS), dtype=np.int64)
                home_unit = unit[direction[home]]
                overflow = first_label_overflow(
                    ev_h,
                    amount[home],
                    content[home],
                    free,
                    home_unit,
                    lambda i: entries[int(ev_h[i])].position,
                )
                if overflow is not None:
                    failures[(overflow[0], family, 0, 0, 1)] = overflow[1]
                weights = amount[home] if free else amount[home] * content[home]
                home_labels = home_unit * weights[:, None]
                if not free:
                    taken_in = grouped_sums(home_labels, starts, widest)
                # The home rows leave the store: their labels leave the
                # running transit line (a paid family's join the momentum).
                plan.left_momentum = exact_column_sums(home_labels)
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

            def admit() -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray] | None:
                """The rows the threshold, the window and the rule admit,
                grouped by (measured event, number): the rows, the amounts
                that click (after `beam`'s pairing), the units the pairing
                keeps, the rules and the sets; None when nothing is met."""
                # Met: the arrivals of every other number at a table that is
                # not `pass`, ordered by detector set (then measured event,
                # then row): the threshold on the amount summed over the set.
                rule = ev_rule[ev, family]
                met = np.flatnonzero(~own & arrived & (rule != PASS_RULE))
                if met.shape[0] == 0:
                    return None
                met = met[np.argsort(ev_set[ev[met]], kind="stable")]
                ev_m = ev[met]
                st_m = ev_set[ev_m]
                s_starts = group_starts(st_m)
                s_sizes = group_sizes(s_starts, met.shape[0])
                total = grouped_sums(amount[met], s_starts, int(s_sizes.max()))
                # The threshold: under `beam` on the amount summed over the
                # set; under `wave` (since 2026-09-20, issue #359 step A) on
                # the square of the coherent pointer of the set's arrivals in
                # units of one ray (`pointer_units`), so that rays which
                # cancel pass whether or not a window is declared. No memory
                # between intervals: the pointer is this interval's arrivals.
                # The pointer gate is the click's (the entries that absorb:
                # `measure`, `rerelease`); a `read` entry, the push of a
                # body, keeps the amount gate under both readings, since the
                # push reads the flow and not the pointer (the closing gate's
                # finding F1, 2026-09-20; BEAM_LAW note 32).
                set_threshold = st_threshold[st_m[s_starts]]
                below_set = np.asarray(total < set_threshold, dtype=bool)
                absorbs = rule[met] != READ_RULE
                # The window: under `wave` it reads the set's phase, the
                # nearest step of the coherent pointer of the arrivals the
                # threshold admitted (a zero pointer has no phase and is
                # outside every window); under `beam` each ray's own phase.
                window = ev_window[ev_m, family]
                read_phase = phase[met].copy()
                wave_rows = st_wave[st_m]
                if wave_rows.any():
                    px, py = coherent_pointer(
                        amount[met], phase[met], s_starts, tables.cosines, tables.sines
                    )
                    below_wave = np.array(
                        [
                            pointer_units(x, y) < t
                            for x, y, t in zip(px, py, set_threshold.tolist(), strict=True)
                        ],
                        dtype=bool,
                    )
                    steps = pointer_phases(px, py, tables.cosines, tables.sines)
                    set_step = np.array([-1 if s is None else s for s in steps], dtype=np.int64)
                    read_phase = np.where(wave_rows, np.repeat(set_step, s_sizes), read_phase)
                below = np.repeat(below_set, s_sizes)
                if wave_rows.any():
                    below = np.where(wave_rows & absorbs, np.repeat(below_wave, s_sizes), below)
                inside = (window < 0) | (
                    (read_phase >= 0) & tables.window[(read_phase - window) % modulus]
                )
                passing = below | ~inside
                p = np.flatnonzero(passing)
                if p.shape[0]:
                    ev_p = ev_m[p]
                    p_starts = group_starts(ev_p)
                    p_ends = np.append(p_starts[1:], p.shape[0])
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
                    return None
                # The taken rows grouped by (measured event, number), the
                # rows of a group in row order.
                taken = taken[np.lexsort((number[taken], ev[taken]))]
                a_t = amount[taken].copy()
                rule_t = ev_rule[ev[taken], family]
                st_t = ev_set[ev[taken]]
                # The `beam` reading (the model owner, 2026-09-19, "only
                # events"): over a beam set, the rays that would click are
                # paired by opposite phase, greedily in the order of the rows
                # (measured event, number, row), a row pairing its units with
                # the first later rows of the set whose phase is opposite
                # (with a window on the row's Node, within the half circle
                # centred on the opposite phase; without one, exactly
                # opposite); a paired couple passes on whole, the rest of a
                # row clicks.
                cancelled = np.zeros(taken.shape[0], dtype=np.int64)
                pairing = np.flatnonzero((rule_t == MEASURE_RULE) & ~st_wave[st_t])
                if pairing.shape[0] >= 2:
                    sets_p = st_t[pairing]
                    for set_index in np.unique(sets_p).tolist():
                        rows = pairing[sets_p == set_index]
                        if rows.shape[0] < 2:
                            continue
                        phases = phase[taken[rows]].tolist()
                        left = a_t[rows].tolist()
                        arcs = ev_window[ev[taken[rows]], family].tolist()
                        for i, phase_i in enumerate(phases):
                            if left[i] == 0:
                                continue
                            for j in range(i + 1, len(phases)):
                                if left[j] == 0:
                                    continue
                                d = (phases[j] - phase_i - half) % modulus
                                if not (d == 0 if arcs[i] < 0 else bool(tables.window[d])):
                                    continue
                                part = min(left[i], left[j])
                                left[i] -= part
                                left[j] -= part
                                cancelled[rows[i]] += part
                                cancelled[rows[j]] += part
                                if left[i] == 0:
                                    break
                        a_t[rows] = left
                if cancelled.any():
                    c_rows = np.flatnonzero(cancelled > 0)
                    for k in c_rows.tolist():
                        plan.cancelled.setdefault(int(ev[taken[k]]), []).append(
                            (int(number[taken[k]]), int(cancelled[k]), int(phase[taken[k]]))
                        )
                    # The paired units go on: the row keeps them and stays.
                    store.amount[at[taken[c_rows]]] = cancelled[c_rows]
                    plan.events.update(ev[taken[c_rows]].tolist())
                return taken, a_t, cancelled, rule_t, st_t

            admitted = admit()
            # The one reading over the set: ONE moment table with the two
            # masks (the four unifications, the model owner, 2026-09-20, (3);
            # note 33). The present rows: every row of another number at
            # the set at its amount, the admitted rows at the amount that
            # clicks (`beam`'s pairing having split a row into the units
            # that go on, a row of their own in the table, present and not
            # admitted, and the units that click). The presence and the age
            # moment, what the clock counts, are the zeroth moment and the
            # age moment over the present rows per measured event; the
            # record's component and the flow the push reads are the
            # moments over the admitted rows per (measured event, number).
            position = np.full(at.shape[0], -1, dtype=np.int64)
            position[others] = np.arange(others.shape[0], dtype=np.int64)
            present_weight = amount[others].copy()
            rows_v, rows_w, rows_age, rows_ev = v_others, present_weight, age_at[others], ev[others]
            if admitted is not None:
                taken_all, a_t_all, cancelled_all = admitted[0], admitted[1], admitted[2]
                present_weight[position[taken_all]] = a_t_all
                parts = np.flatnonzero(cancelled_all > 0)
                if parts.shape[0]:
                    split = taken_all[parts]
                    rows_v = np.concatenate((v_others, unit[arrival[split]]))
                    rows_w = np.concatenate((present_weight, cancelled_all[parts]))
                    rows_age = np.concatenate((age_at[others], age_at[split]))
                    rows_ev = np.concatenate((ev[others], ev[split]))
            if rows_w.shape[0] == 0:
                return plan
            table = moment_table(rows_v, rows_w, rows_age)
            np.add.at(presence[family], rows_ev, table[:, 0] + table[:, 1])
            np.add.at(age_moment[family], rows_ev, table[:, AGE_COLUMN] + table[:, AGE_COLUMN + 1])
            if admitted is None:
                return plan
            # The rows that click after the pairing (every taken row without
            # a pairing), in their group order.
            survivors = a_t_all > 0
            if not survivors.any():
                return plan
            taken, a_t, cancelled = taken_all[survivors], a_t_all[survivors], cancelled_all[survivors]
            rule_t, st_t = admitted[3][survivors], admitted[4][survivors]
            ev_t, num_t = ev[taken], number[taken]
            new = np.concatenate((NEW_RUN, (ev_t[1:] != ev_t[:-1]) | (num_t[1:] != num_t[:-1])))
            g_starts = np.flatnonzero(new)
            groups = g_starts.shape[0]
            g_sizes = group_sizes(g_starts, taken.shape[0])
            widest = int(g_sizes.max())
            of_row = np.cumsum(new) - 1
            g_ev = ev_t[g_starts]
            e_starts = group_starts(g_ev)

            def fail(group: int, stage: int, error: OverflowError) -> None:
                first = int(e_starts[int(np.searchsorted(e_starts, group, side="right")) - 1])
                failures[(int(g_ev[group]), family, 1, group - first, stage)] = error

            c_t, ph_t = content[taken], phase[taken]
            age_t = age_at[taken]
            v_arrival = unit[arrival[taken]]
            # The admitted rows of the one table (their arrival's unit vector
            # weighted by the amount that clicks, the age moment among them;
            # the measured event reads the age whole), summed per group: the
            # reading's component on the record.
            overflow = first_reading_overflow(of_row, groups, a_t, v_arrival, age_t)
            if overflow is not None:
                fail(overflow[0], 2, overflow[1])
            admitted_rows = table[position[taken]]
            reading = moments_of_groups(admitted_rows, g_starts)
            for key in {entries[e].reads[family] for e in set(g_ev.tolist())}:
                plan.readings[key] = reading.component(key).tolist()
            # The push, ONE product per group of arriving rays (`push_form`):
            # the label flow per group is the first moment of the same rows
            # with the label's weight, the amount for a free family (the
            # table's own flow) and content x amount for a paid one (the
            # flow times the content per unit), the weights bounded before
            # the product; the electric factor is the family's charge per
            # unit of content, so no class of rows is kept.
            overflow = first_label_overflow(
                of_row, a_t, c_t, free, v_arrival, lambda i: entries[int(ev_t[i])].position
            )
            if overflow is not None:
                fail(overflow[0], 3, overflow[1])
            weights = a_t if free else a_t * c_t
            overflow = first_moment_overflow(of_row, groups, weights, v_arrival)
            if overflow is not None:
                fail(overflow[0], 4, overflow[1])
            flow = admitted_rows[:, 2 : 2 + DIMENSIONS]
            labels = flow if free else flow * c_t[:, None]
            plan.g_moment = np.add.reduceat(labels, g_starts, axis=0).tolist()
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
            e_ends = np.append(e_starts[1:], groups)
            g_events = g_ev[e_starts].tolist()
            e_lo, e_hi = e_starts.tolist(), e_ends.tolist()
            for k, event in enumerate(g_events):
                plan.groups[event] = (e_lo[k], e_hi[k])
            plan.events.update(g_events)
            # The rows a table absorbs leave the store (a row that kept
            # paired units stays with them). The set's reading of what
            # clicked: under `wave` the clicked amount summed exactly per
            # set, then the coherent pointer of the clicked rows (the
            # amplitudes at their phases), exact and never refused, and its
            # nearest step; under `beam` the count clicked and the phase of
            # the last clicked row of the set.
            absorbed = rule_t != READ_RULE
            keep[family][at[taken[absorbed & (cancelled == 0)]]] = False
            plan.left_momentum = [
                a + b
                for a, b in zip(plan.left_momentum, exact_column_sums(labels[absorbed]), strict=True)
            ]
            clicked = np.flatnonzero(rule_t == MEASURE_RULE)
            if clicked.shape[0]:
                clicked = clicked[np.argsort(st_t[clicked], kind="stable")]
                st_c = st_t[clicked]
                c_starts = group_starts(st_c)
                c_sizes = group_sizes(c_starts, clicked.shape[0])
                totals_c = grouped_sums(a_t[clicked], c_starts, int(c_sizes.max())).tolist()
                pointer_x, pointer_y = coherent_pointer(
                    a_t[clicked], ph_t[clicked], c_starts, tables.cosines, tables.sines
                )
                steps = pointer_phases(pointer_x, pointer_y, tables.cosines, tables.sines)
                last_phase = ph_t[clicked][(c_starts + c_sizes - 1)].tolist()
                for k, set_index in enumerate(st_c[c_starts].tolist()):
                    if st_wave[set_index]:
                        plan.pointer[set_index] = (pointer_x[k], pointer_y[k])
                        plan.set_phase[set_index] = steps[k]
                    else:
                        plan.count[set_index] = totals_c[k]
                        plan.set_phase[set_index] = last_phase[k]
            return plan

        plans = [family_plan(family, store) for family, store in enumerate(stores)]
        for plan in plans:
            if plan is not None:
                ledger.transit_momentum = [
                    a - b for a, b in zip(ledger.transit_momentum, plan.left_momentum, strict=True)
                ]
        # The presence read back, and what the clock counts (the presence,
        # or the age moment where the table entry reads `age`), exact over
        # the families.
        totals = presence[0].tolist() if count == 1 else [sum(c) for c in presence.T.tolist()]
        counted = np.where(counts_age, age_moment, presence)
        counted_totals = counted[0].tolist() if count == 1 else [sum(c) for c in counted.T.tolist()]
        for i, entry in enumerate(entries):
            entry.presence = totals[i]
            entry.counted = counted_totals[i]
        active: set[int] = {key[0] for key in failures}
        for plan in plans:
            if plan is not None:
                active |= plan.events
        # The set's record line and the phase it returns follow the last
        # active measured event of the set, after every click of the set.
        last_active: dict[int, int] = {}
        for i in sorted(active):
            last_active[int(ev_set[i])] = i

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
            detector_set = entry.detector_set
            detector = detector_set.name
            for family, plan in enumerate(plans):
                if failures:
                    refuse((i, family, 0, 0, 0))
                if plan is None:
                    continue
                name = families[family].name
                free = free_of[family]
                rule = entry.table[family]
                home_plan = plan.home.get(i)
                if home_plan is not None:
                    k0, k1, total, carried, taken_in = home_plan
                    pending = entry.pending[family]
                    for k in range(k0, k1):
                        pending.append((plan.h_amount[k], plan.h_content[k], plan.h_phase[k]))
                    entry.taken[family]["home"] += total
                    ledger.transit_absorbed[family] += total
                    ledger.content_absorbed[family] += carried
                    if failures:
                        refuse((i, family, 0, 0, 1))
                    if not free:
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
                if record is not None:
                    for other, amount_c, phase_c in plan.cancelled.get(i, ()):
                        record(
                            {
                                "event": "pass",
                                "tick": tick,
                                "node": node,
                                "measured": entry.number,
                                "detector": detector,
                                "family": name,
                                "number": other,
                                "amount": amount_c,
                                "phase": phase_c,
                                "cancelled": True,
                            }
                        )
                span = plan.groups.get(i)
                if span is not None:
                    reading_values = plan.readings[entry.reads[family]]
                    for gi in range(span[0], span[1]):
                        if failures:
                            for stage in (2, 3, 4):
                                refuse((i, family, 1, gi - span[0], stage))
                        other = plan.g_number[gi]
                        # The reader's charges are what the frame read at the
                        # start of the interval (`frame_charges`, gravity's the
                        # content M_A), the same for every family's rays
                        # whatever the family order: a click of this interval
                        # joins `held` and is read by the next frame (the
                        # orchestrator's D1, 2026-09-20); the arriving side is
                        # the family's value per column; the columns are
                        # floored at the reader's clock age, as every rate of
                        # the law is (the four unifications (4)).
                        push = push_form(
                            free,
                            plan.g_moment[gi],
                            entry.frame_charges,
                            values_of[family],
                            columns,
                            entry.clock_age,
                            entry,
                        )
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
                        entry.taken[family][rule] += group_total
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
                        entry.held[family] = bounded(
                            entry.held[family] + group_content, entry, "content"
                        )
                        entry.clicks[family] += group_total
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
                # The set's record, once per set per family per interval,
                # after the set's last active measured event: under `wave`
                # the pointer's square, under `beam` the count clicked,
                # exact Python integers (a report of the host, never
                # refused; a record may pass 2^63 and its readers parse it
                # as an arbitrary-precision integer); and the set's phase,
                # returned to every measured event of the set (the model
                # owner: the detector returns to the GameBoard the information
                # it received), the frame's turn added after it.
                set_index = detector_set.index
                if last_active.get(set_index) == i and set_index in plan.set_phase:
                    set_phase = plan.set_phase[set_index]
                    if detector_set.wave:
                        pointer_x, pointer_y = plan.pointer[set_index]
                        value = pointer_x * pointer_x + pointer_y * pointer_y
                    else:
                        value = plan.count[set_index]
                    detector_set.record[family] += value
                    if set_phase is not None:
                        detector_set.phase[family] = set_phase
                        for member in detector_set.numbers:
                            if member in measured:
                                measured[member].phase = set_phase
                    if record is not None:
                        one = len(detector_set.numbers) == 1
                        line = {
                            "event": "record",
                            "tick": tick,
                            "node": node if one else None,
                            "measured": entry.number if one else None,
                            "detector": detector,
                            "family": name,
                            "number": 0,
                            "record": value,
                        }
                        if detector_set.wave:
                            line["pointer"] = [pointer_x, pointer_y]
                        line["phase"] = set_phase
                        record(line)
    for family, store in enumerate(stores):
        if not keep[family].all():
            store.keep(keep[family])

    # 5. The self-creations: the releases into the store.
    numerator, denominator_release = world.release
    # Only a measured event that can release anything is visited (in number
    # order): a lamp, a holder of a free family's content, or one with rows
    # pending (home or re-released); any other would find nothing to create.
    for entry in entries:
        if not entry.creating or not (
            entry.lamp_rate is not None
            or any(free and held > 0 for free, held in zip(free_of, entry.held, strict=True))
            or any(entry.pending)
        ):
            continue
        age, turn = entry.clock_age, entry.turn
        for family, store in enumerate(stores):
            definition = families[family]
            free = free_of[family]
            born: list[tuple[int, int, int, int]] = []  # (direction, amount, content, phase)
            if free and entry.held[family] > 0:
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
            # A body on a set of Nodes releases at every Node of the set
            # with whole units only: each born row's amount is apportioned
            # whole over the body's Nodes in their fixed order, equal
            # weights, the leftover units to the Nodes counted from `age mod
            # w` (the tie rule of the re-emission over the directions), so
            # that the total released is the content's release whatever the
            # width, no Node is favoured over w self-creations and the books
            # balance (the shares sum to the amount, every share keeps the
            # row's content per unit and phase, the labels' sum is the same
            # recoil). A body of one Node (every measured event until
            # 2026-09-20) releases every row at its one Node, unchanged.
            body = entry.nodes
            if len(body) > 1:
                ways = len(body)
                split: list[tuple[int, int, int, int, int]] = []  # (node, direction, amount, ...)
                for direction, amount, content, phase in born:
                    shares = apportion_whole(amount, [1] * ways, age % ways)
                    split.extend(
                        (store.flat(node), direction, share, content, phase)
                        for node, share in zip(body, shares, strict=True)
                        if share
                    )
                node_column = np.array([b[0] for b in split], dtype=np.int64)
                born = [b[1:] for b in split]
            else:
                node_column = np.full(len(born), store.flat(entry.position), dtype=np.int64)
            count = len(born)
            direction_column = np.array([b[0] for b in born], dtype=np.int64)
            amount_column = np.array([b[1] for b in born], dtype=np.int64)
            content_column = np.array([b[2] for b in born], dtype=np.int64)
            # The labels of the born rows (the one label, its product checked
            # per row before it is formed, refused naming the Node and the
            # amount): a paid family's emitter takes their sum as its
            # recoil, a lamp's release and a re-emission alike.
            labels = momentum_labels(
                unit, direction_column, amount_column, content_column, free, entry.position
            )
            born_momentum = exact_column_sums(labels)
            if not free:
                entry.momentum = [
                    bounded(a - b, entry, "momentum")
                    for a, b in zip(entry.momentum, born_momentum, strict=True)
                ]
            ledger.transit_momentum = [
                a + b for a, b in zip(ledger.transit_momentum, born_momentum, strict=True)
            ]
            store.append(
                node=node_column,
                direction=direction_column,
                age=np.zeros(count, dtype=np.int64),
                phase=np.array([b[3] for b in born], dtype=np.int64),
                number=np.full(count, entry.number, dtype=np.int64),
                amount=amount_column,
                content=content_column,
                arrival=np.full(count, NO_ARRIVAL, dtype=np.int64),
            )
            ledger.transit_released[family] += int(exact_sum(amount_column))

    # 6. The border `lifetime` (the model owner, 2026-09-20: "the event
    # whose age reaches L makes no next event but an escape click in the
    # ledger, as at an open face"): every row of a family with a lifetime
    # whose age reached it in this interval's walk (read by a table in
    # step 4 where it arrived at a measured event; unread in free space)
    # clicks on the border, its amount, content and label booked as an
    # open face books an escape, one `click` record per row naming the
    # border, the border's record the square of the coherent pointer of
    # what clicked, per family; then the rows leave the store. Local (the
    # row's own age against its family's key, read by the one primitive:
    # `ages_at_key`, `by_clock(age - 1, 1, L)` = 1 at the walk that brought
    # the age to L, as the clock reads the turn; note 33), fixed work (one
    # comparison per row), no draw, no register; the one-way border of the
    # interval beside the click.
    for family, store in enumerate(stores):
        lifetime = families[family].lifetime
        if lifetime is None or store.size == 0:
            continue
        gone = np.flatnonzero(ages_at_key(store.age, lifetime))
        if gone.shape[0] == 0:
            continue
        definition = families[family]
        labels = store.labels(gone, unit, definition.free)
        amounts = store.amount[gone]
        total = int(exact_sum(amounts))
        ledger.lifetime_amount[family] += total
        ledger.lifetime_content[family] += int(exact_sum(amounts * store.content[gone]))
        border_x, border_y = coherent_pointer(
            amounts, store.phase[gone], FIRST, tables.cosines, tables.sines
        )
        ledger.lifetime_record[family] += border_x[0] * border_x[0] + border_y[0] * border_y[0]
        left = exact_column_sums(labels)
        ledger.lifetime_momentum[family] = [
            a + b for a, b in zip(ledger.lifetime_momentum[family], left, strict=True)
        ]
        ledger.transit_momentum = [a - b for a, b in zip(ledger.transit_momentum, left, strict=True)]
        if record is not None:
            x, y, z = store.coordinates(store.node[gone])
            for k, index in enumerate(gone):
                record(
                    {
                        "event": "click",
                        "tick": tick,
                        "node": [int(x[k]), int(y[k]), int(z[k])],
                        "measured": None,
                        "detector": LIFETIME_NAME,
                        "family": definition.name,
                        "number": int(store.number[index]),
                        "amount": int(store.amount[index]),
                        "phase": int(store.phase[index]),
                        "momentum": [int(v) for v in labels[k]],
                        "content": int(store.amount[index] * store.content[index]),
                    }
                )
        keep_alive = np.ones(store.size, dtype=bool)
        keep_alive[gone] = False
        store.keep(keep_alive)

    # Merge identical rows; sort by Node. A row whose age passed the
    # world's bound refuses the run: the store's promise of fixed storage
    # is the bound, and the world must be small enough or declare it (the
    # same primitive as the border: the age against the key age_bound + 1,
    # `ages_at_key`; note 33).
    for store in stores:
        store.merge()
        if store.size and ages_at_key(store.age, world.age_bound + 1).any():
            raise OverflowError(
                f"{BEAM_LAW}: a ray carries the age {int(store.age.max())} beyond the world's "
                f"age_bound {world.age_bound} (declare a larger age_bound or a smaller GameBoard)"
            )
    return readings
