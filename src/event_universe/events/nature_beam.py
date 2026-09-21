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

1. the walk: every ray whose flight rule steps this interval is created at
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
   own, and, since the crossing rule (the model owner's record 158 of
   2026-09-20; docs/BEAM_LAW.md note 47), the rays it meets by its own
   step (the rows that crossed its Link the other way and the rows at the
   Node it entered moving against it), never again a row that came over
   its Link behind it (a row and a body meet once, at the crossing of
   their world lines), as one set (the threshold on the set), then each ray by its own
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
for a free one, u_d the unit vector of the direction at the flight's
scale Q = 64: the integer vector nearest Q D / |D|, `unit_label`, one
world constant per direction of the flight, exactly Q e_d on a
heading; the model owner's decision of 2026-09-19 on the physics-rule
reviewer's verdict, BEAM_LAW section 2 and note 23): the push's moment, the
click's momentum, the face click's, the recoil at a release or a
re-emission and the transit line of the books; no momentum is read off a
Port, and the reading's vector and tensor moments are taken on u_d as
well, so a fan's flow reads Q per unit of amount direction-blind. No other
function holds a piece of the law: `direction_flight`, `collision_table` and
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

from event_universe.core.game_board import PORT_HEADINGS, Address3, adjacent_node
from event_universe.core.integer import (
    apportion_whole,
    bounded_gcd,
    integer_root,
)
from event_universe.core.phase import PHASE_COSINE_SCALE, PhaseCircle, phase_circle
from event_universe.events.amplitude import (
    AMPLITUDE_SCALE,
    LABEL_BITS,
    LABEL_MASK,
    Layer,
    arm_of,
    branch_of,
    half_angle,
    label_of,
)
from event_universe.events.measured import (
    CountTable,
    DetectorSet,
    Ledger,
    Measured,
    PendingRow,
    count_component,
)
from event_universe.events.meeting import ArcTable, arc_table, meet
from event_universe.events.world import (
    AGE_READS,
    AMOUNT_BOUND,
    BEAM_LAW,
    BECOME_RULE,
    CHARGE_INDEX,
    CONTACT_DEFAULT,
    FACE_NAMES,
    FIXED_DIRECTIONS,
    HEADING_OFFSET,
    LIFETIME_NAME,
    MOMENTUM_BOUND,
    NO_HAND,
    REST_DIRECTIONS,
    FamilyDefinition,
    Gate,
    NatureBeamWorld,
    Q,
    Rotation,
    Transformation,
    Vector,
    axis_sign,
    default_reads,
    default_rule,
    default_width,
)

Record = Callable[[dict[str, object]], None]
# The one scale of the law is the world's constant `world.Q`: the time
# resolution of the flight, T_d = isqrt(3 |v|^2 Q^2), and the length of
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
# The amplitude of one unit in 32nds (`AMPLITUDE_SCALE`, defined once in the
# layer's module): a row of `amount` identical rays (one phase) is the
# coherent sum of its units, A = 32 x amount, so that the merge of identical
# rows (a bookkeeping bijection) leaves the reading unchanged; two rows in
# phase add their amplitudes.
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
    # The amplitude law's three columns (`amplitude-v1`, 2026-09-20; BEAM_LAW
    # note 37): the record the row belongs to (the birth's identity, the
    # emitter's number x 2^32 + the birth's ordinal at the emitter; 0 for a
    # row of no record), the row's branch (the
    # joint label of the row within its record, with the arm it flies on in
    # the high bits; 0 without) and its multiplicity m (the product of the
    # norms of the splits the row's path passed; 1 without). The flight and
    # the collision never read them; the merge reads them as identity.
    record: int = 0
    branch: int = 0
    multiplicity: int = 1
    # The birth phase u of the row's record (stage (vii), the K finding of
    # 2026-09-20): the record's own field beside the running phase, the
    # lamp's count of births mod N at the birth, uniform over births
    # whatever the lamp's turn; every rule of the GameBoard that reads a
    # record row's phase reads the path phase, phase - u, and the click
    # alone reads u (the ladder). 0 on a row of no record.
    birth: int = 0

    # The hand (`hand-v1`, 2026-09-20; BEAM_LAW note 39): the sense in which
    # the row turns about its own direction, +1 right, -1 left, 0 none
    # (every row of every world without a declaration): a pseudoscalar,
    # kept by the 24 proper rotations of the cube and negated by the 24
    # improper ones, carried unchanged through every re-creation and an
    # identity field of the merge. The flight, the collision, the push and
    # every moment never read it; a table entry's parity filter does.
    hand: int = 0
    # The share's accumulators (the model owner's record 155 of 2026-09-20,
    # "no remainder discarded"; BEAM_LAW note 41 (viii)): per axis the part
    # of the row's push on a body not yet delivered, `share_of`; 0 on a row
    # of no record and on every row that never pushed; summed at a merge;
    # left with the row when it is absorbed or escapes.
    share_x: int = 0
    share_y: int = 0
    share_z: int = 0

    def record_line(self, vectors: np.ndarray, handed: bool = False) -> dict[str, object]:
        """The row as `state.json` writes it, the direction as its vector;
        a row of a record with its columns, a row of no record without
        them; in a world that declares a hand with its `hand`; a row that
        holds an undelivered share with its `share`."""
        line: dict[str, object] = {
            "direction": [int(v) for v in vectors[self.direction]],
            "age": self.age,
            "phase": self.phase,
            "number": self.number,
            "amount": self.amount,
            "content": self.content,
        }
        if self.record != NO_RECORD:
            line["record"] = self.record
            line["branch"] = self.branch
            line["multiplicity"] = self.multiplicity
            line["u"] = self.birth
        if handed:
            line["hand"] = self.hand
        if self.share_x or self.share_y or self.share_z:
            line["share"] = [self.share_x, self.share_y, self.share_z]
        return line


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
    numerator / denominator gains at the walk that takes each row's age
    from `age` to `age + 1`, the first difference of a floor, exact on
    average with no remainder anywhere; the caller has bounded (age + 1)
    x numerator to the register. The rows' phase per interval of age
    (`phase_per_age`, a count on a row of the store, whose age is its
    record) reads it; every count of a BODY is `core.integer.by_drive` on
    an accumulator of the body's record since the fraction-free law
    (2026-09-20, BEAM_LAW note 41), of which this is the constant-rate
    identity from age 0."""
    if denominator < 1:
        raise ValueError("positive denominator required")
    result: np.ndarray = ((age + 1) * numerator) // denominator - (age * numerator) // denominator
    return result


def window_admits(
    distance: np.ndarray | int, width: np.ndarray | int, modulus: int
) -> np.ndarray | bool:
    """Whether a phase at the distance d = (phase - s) mod N from a
    window's setting s is inside the window of width w (`phase_width`; the
    weak force, 2026-09-20, BEAM_LAW note 36): the w consecutive steps of
    the circle centred on the setting, [s - floor(w / 2), s - floor(w / 2)
    + w), that is (d + floor(w / 2)) mod N < w, the one floor of the window
    and its width (the mathematician's ONE_FORMULA row 11). At the default
    width N / 2 (`world.default_width`) it is the half circle as it was,
    d < N / 4 or d >= 3 N / 4, on every pair (phase, setting) of every N
    (`tests/test_window_width.py` (a)). Rows or one value alike."""
    result: np.ndarray | bool = ((distance + width // 2) % modulus) < width
    return result


def ages_at_key(age: np.ndarray, key: int) -> np.ndarray:
    """The rows whose walk this interval brought their age to the key (a
    family's lifetime L; the world's age bound as the key age_bound + 1):
    `by_clock(age - 1, 1, key)` = 1, the one primitive read on the age
    before the walk against the key, exactly as the clock reads a measured
    event's turn off its age against K (the mathematician's clock_checks
    4: first at the age L, then every L); since the fraction-free law
    (2026-09-20, BEAM_LAW note 41) spelled as the comparison it is, `age
    mod key = 0`, the same rows (no rate, no accumulator: `by_clock(age -
    1, 1, key)` is 1 exactly when the key divides the age). A row at age 0
    (born this interval, or declared at rest at 0) has not walked and is
    never at the key."""
    result: np.ndarray = (age > 0) & (age % key == 0)
    return result


# -- the flight ------------------------------------------------------------------


@dataclass(frozen=True)
class Flight:
    """The flight of a direction set, one world constant per direction: v,
    S_1 = |a| + |b| + |c|, T_d = isqrt(3 |v|^2 Q^2), the Bresenham line of
    v (its S_1 unit steps, `lines`), the least period L_d of the flight's
    phase (a fact about the rate, which the readers use for c) and
    `labels`, the unit vector u_d of each direction at the scale Q
    (`unit_label`; (0, 0, 0) for a rest direction): the momentum label of
    one unit of amount along d, the same length within sqrt 3 / (2 Q) for
    every direction and exactly Q e_d on a heading. The Link a ray crosses
    at an age is the position's accumulator rule (`walk_step`; the model
    owner's record 155 of 2026-09-20, "no tables": until then a step table
    per direction over its period, built from the same rule at load). A
    direction's velocity is (Q / T_d) v per axis."""

    vectors: np.ndarray
    manhattan: np.ndarray
    resolution: np.ndarray
    period: np.ndarray
    lines: np.ndarray
    labels: np.ndarray

    def manhattan_steps(self, direction: np.ndarray, age: np.ndarray) -> np.ndarray:
        """m(tau) = (2 tau S_1 Q + T_d) // (2 T_d): the Manhattan steps made
        by age tau, the whole count of the position's accumulator (below)
        over the ages 0 .. tau - 1."""
        s1, t = self.manhattan[direction], self.resolution[direction]
        result: np.ndarray = (2 * age * s1 * Q + t) // (2 * t)
        return result

    def accumulator(self, direction: np.ndarray, age: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
        """The position's accumulator of a ray of direction d at age tau,
        formed in this one place (BEAM_LAW note 41 (viii)): the pair (m,
        the residue), m = m(tau) the count of Manhattan steps made by the
        age and the residue (tau r + T_d) mod d what the accumulator holds
        toward the next step, r = 2 S_1 Q its rate and d = 2 T_d its wall
        (T_d the direction's resolution, S_1 its Manhattan length, Q the
        label's scale). `walk_step` reads it for the interval's step; the
        click's exact phase reads the residue at an arrival (TWO_SLITS.md
        section 2). A ray's rate never changes over its flight (a
        re-release or a split is a new row at age 0), so both are off the
        age and the row carries no field for them."""
        s1, t = self.manhattan[direction], self.resolution[direction]
        held = age * (2 * s1 * Q) + t
        denominator = 2 * t
        return held // denominator, held % denominator

    def walk_step(self, direction: np.ndarray, age: np.ndarray) -> np.ndarray:
        """The Link a ray of direction d crosses at age tau (a heading, or
        zero for no move), by the position's accumulator on the row, the
        one count rule of the law (BEAM_LAW note 41 (viii); the digital
        line of the flight): the accumulator gains r = 2 S_1 Q at every
        interval over d = 2 T_d from the start T_d (`accumulator`), e =
        [acc + r >= d] is the Manhattan step of the interval (r <= d, so e
        is 0 or 1), and the step is the m-th unit step of the direction's
        line, m the count made before it (FORM.md section 1 (i))."""
        s1, t = self.manhattan[direction], self.resolution[direction]
        rate = 2 * s1 * Q
        made, residue = self.accumulator(direction, age)
        moved = (residue + rate) // (2 * t)
        place = np.where(s1 > 0, made % np.maximum(s1, 1), 0)
        result: np.ndarray = self.lines[direction, place] * moved[:, None]
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


def direction_flight(vectors: tuple[tuple[int, int, int], ...]) -> Flight:
    """The flight of a direction set, its constants computed once at load."""
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
    # The labels: the unit vector of every direction at the scale Q.
    labels = np.array([unit_label(vector) for vector in vectors], dtype=np.int64).reshape(count, 3)
    return Flight(
        np.array(vectors, dtype=np.int64).reshape(count, 3), manhattan, resolution, period, lines, labels
    )


# -- the collision table ---------------------------------------------------------


@dataclass(frozen=True)
class CollisionTable:
    """The collision as a group action (named on 2026-09-21, the vector
    program, record 191): the cyclic group acts on the 3^8 slot states by
    the shift `forward` (its inverse `inverse`), and the orbits of the
    action are the classes of section 4 (a crowd mask, a number of singles
    and their headings' sum: the invariants of every move). Per code:
    `orbit`, the index of its class; `period`, the size of its class, the
    least power of the shift that returns the code; `singles`, its single
    slots in order (padded with -1). `act(code)` is one step of the
    action."""

    forward: np.ndarray
    inverse: np.ndarray
    singles: np.ndarray
    powers: np.ndarray
    orbit: np.ndarray
    period: np.ndarray

    def act(self, code: np.ndarray, backward: bool = False) -> np.ndarray:
        """One step of the action on slot-state codes: the shift, or its
        inverse under `backward`."""
        result: np.ndarray = (self.inverse if backward else self.forward)[code]
        return result


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
    orbit = np.zeros(size, dtype=np.int64)
    period = np.zeros(size, dtype=np.int64)
    for index, members in enumerate(classes.values()):
        members.sort()
        count = len(members)
        for i, state in enumerate(members):
            target = members[(i + 1) % count]
            forward[state_code(state)] = state_code(target)
            inverse[state_code(target)] = state_code(state)
            orbit[state_code(state)] = index
            period[state_code(state)] = count
    for state in itertools.product(range(SLOT_STATES), repeat=COLLISION_SLOTS):
        code = state_code(state)
        found = [i for i, s in enumerate(state) if s == 1]
        singles[code, : len(found)] = found
    powers = SLOT_STATES ** np.arange(COLLISION_SLOTS, dtype=np.int64)
    for array in (forward, inverse, singles, powers, orbit, period):
        array.setflags(write=False)
    return CollisionTable(forward, inverse, singles, powers, orbit, period)


@dataclass(frozen=True)
class NatureBeamTables:
    """The constants of a world's law: the flight of its direction set (the
    position's accumulator rule per direction, `Flight`), the collision
    table (the group action of the shift on the slot states), the phase
    circle (`circle`, the cyclic group of N steps with its unit vectors)
    and its cosines and sines at 1/256 as arrays for the vectorized
    readings. The window is not a table but the one floor `window_admits`
    of a distance against a width (since 2026-09-20; until then a table
    over the distances of the half circle)."""

    flight: Flight
    collision: CollisionTable
    circle: PhaseCircle
    cosines: np.ndarray
    sines: np.ndarray
    # The arc permutations of the direction table (the meeting, 2026-09-20;
    # `meeting.ArcTable`): built per target on demand and cached.
    arcs: ArcTable


def nature_beam_tables(world: NatureBeamWorld) -> NatureBeamTables:
    circle = phase_circle(world.phase_steps)
    flight = direction_flight(world.directions)
    return NatureBeamTables(
        flight,
        collision_table(),
        circle,
        np.array(circle.cosines, dtype=np.int64),
        np.array(circle.sines, dtype=np.int64),
        arc_table(flight.labels),
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
    "arrival",
    "record",
    "branch",
    "multiplicity",
    "birth",
    "hand",
    "share_x",
    "share_y",
    "share_z",
)
# The fields that make two rows identical (the amount is what the merge
# adds); since `amplitude-v1` the record, the branch and the multiplicity
# too (constant 0, 0, 1 on a row of no record, so the packed key and the order of
# the merge are what they were), and since `hand-v1` the hand (constant 0
# without a declaration, a width of 0 bits in the packed key: two rows of
# opposite hands are two rows and never merge or cancel).
IDENTITY_FIELDS = (
    "node",
    "direction",
    "age",
    "phase",
    "number",
    "content",
    "record",
    "branch",
    "multiplicity",
    "hand",
)
# The three columns of the amplitude law as a row of no record carries them.
NO_RECORD = 0
NO_BRANCH = 0
ONE_PATH = 1
NO_RECORD_COLUMNS = {"record": NO_RECORD, "branch": NO_BRANCH, "multiplicity": ONE_PATH, "birth": 0}
# The columns a caller may leave out of `append`: the record's four and
# the hand (a row without a declaration has none).
COLUMN_DEFAULTS = {**NO_RECORD_COLUMNS, "hand": NO_HAND, "share_x": 0, "share_y": 0, "share_z": 0}
# The place of `phase` in the identity fields: the merge of a record's rows
# reads it modulo the half circle with a sign (the cancel).
PHASE_FIELD = IDENTITY_FIELDS.index("phase")


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


def share_of(label: int, amount: int, multiplicity: int, accumulator: int = 0) -> tuple[int, int]:
    """A record row's push on a body along one axis (stage (vii) step 3,
    the K finding of 2026-09-20): its share amount^2 / m of the quantum's
    unit label (the record's norm is in m: the shares of a record's rows
    sum to one), the whole part of `accumulator + label x amount` in units
    of m toward zero (`label` the row's label, amount x content x u_d) and
    the remainder kept: since the model owner's record 155 of 2026-09-20
    (BEAM_LAW note 41 (viii)) the row's own accumulator, the part of its
    push not yet delivered, so that a row read at every interval of its
    passage pushes the exact sum over the passage and nothing is
    discarded while the row lives; the remainder leaves with the row when
    it is absorbed (to the books' `remainder` line with the rest of the
    label, label - share) or escapes. Returns (the share, the accumulator
    after). A row of no record (m 1, the label its own) pushes by its
    label."""
    total = accumulator + label * amount
    whole = abs(total) // multiplicity
    share = -whole if total < 0 else whole
    return share, total - share * multiplicity


def place_over_nodes(counts: CountTable, amount: int, ways: int) -> list[int]:
    """`amount` whole units placed over the `ways` Nodes of a body on a
    set (BEAM_LAW note 41 (viii); the model owner's record 155): every
    Node's `place` row of the body's table gains the amount, the whole
    part `amount // ways` goes to every Node and is taken off every row,
    and the `amount mod ways` units left go one each to the Nodes whose
    row holds the largest claim (ties to the lower Node), each taking
    `ways` off its row; the rows sum to zero after every placement and
    each stays within `ways` of zero, so every Node is within one unit of
    its equal share of everything the body has ever released, and no
    remainder is discarded: the claim carries to the next row and the
    next self-creation. Until record 155 the leftover units went to the
    Nodes counted from `age mod ways`, an exact apportioning within the
    row whose ties were reset at every row (`apportion_whole`)."""
    rows = counts.of("place")
    if len(rows) != ways:
        raise ValueError(f"{BEAM_LAW}: a body of {ways} Nodes has {len(rows)} place rows")
    base, left = divmod(amount, ways)
    shares = [base] * ways
    for row in rows:
        row.accumulator += amount - base * ways
    if left:
        order = sorted(range(ways), key=lambda k: (-rows[k].accumulator, k))
        for k in order[:left]:
            shares[k] += 1
            rows[k].accumulator -= ways
    return shares


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
    Q (`labels`, the flight's `labels`), content x amount x u_d for
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


def setting_steps(
    store: NatureBeamStore,
    node_event: np.ndarray,
    ev_number: np.ndarray,
    ev_set: np.ndarray,
    set_count: int,
    cosines: np.ndarray,
    sines: np.ndarray,
    modulus: int,
) -> list[int | None]:
    """The setting a detector set reads off one family's rows present at
    it this interval (a window read from a reading, `phase_window`
    `{"reads": ..., "offset": ...}`; issue #363, 2026-09-20): per set the
    nearest step of the coherent pointer of the store's rows at the set's
    Nodes of every number but the Node's own (the one reading set, rest and
    moving alike, as the presence counts them), None where no such row is
    present or the pointer is zero. The same first moment over the circle
    as the detector's record (`coherent_pointer`, `pointer_phases`), read
    once per named family from the rows after the walk and the collision,
    before any table acts."""
    steps: list[int | None] = [None] * set_count
    found = node_event[store.node]
    at = np.flatnonzero(found >= 0)
    if at.shape[0] == 0:
        return steps
    ev = found[at]
    others = store.number[at] != ev_number[ev]
    at, ev = at[others], ev[others]
    if at.shape[0] == 0:
        return steps
    sets = ev_set[ev]
    order = np.argsort(sets, kind="stable")
    at, sets = at[order], sets[order]
    starts = group_starts(sets)
    # The path phase of a record's row (stage (vii)), the phase itself of
    # a row of no record.
    path = (store.phase[at] - store.birth[at]) % modulus
    x, y = coherent_pointer(store.amount[at], path, starts, cosines, sines)
    for set_index, step in zip(sets[starts].tolist(), pointer_phases(x, y, cosines, sines), strict=True):
        steps[set_index] = step
    return steps


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
        self.record: np.ndarray
        self.branch: np.ndarray
        self.multiplicity: np.ndarray
        self.birth: np.ndarray
        self.hand: np.ndarray
        self.share_x: np.ndarray
        self.share_y: np.ndarray
        self.share_z: np.ndarray

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
        """Rows appended column by column; the three columns of the
        amplitude law default to a row of no record (0, 0, 1) and the hand
        to none (0) when the caller names none of them (a declared ray, the
        tests' bare rows)."""
        count = columns["node"].shape[0]
        for name, default in COLUMN_DEFAULTS.items():
            if name not in columns:
                columns[name] = np.full(count, default, dtype=np.int64)
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

    def identity_columns(self, modulus: int = 0) -> tuple[list[np.ndarray], np.ndarray]:
        """The identity fields as columns in the order of `IDENTITY_FIELDS`
        and the sign of every row's amount in the merge's sum. Without the
        amplitude key (`modulus` 0) the columns are the fields and every
        sign is +1. Under the key (`modulus` the circle's N) a row of a
        record reads its phase modulo the half circle with the sign -1 on
        the far half: two rows of one record, label and multiplicity equal
        in every other field and opposite in phase are then one group whose
        signed sum is their difference (the cancel, the design's normal
        form, section 2.3); a row of no record keeps its phase whole."""
        columns = [getattr(self, name) for name in IDENTITY_FIELDS]
        sign = np.ones(self.size, dtype=np.int64)
        if modulus:
            recorded = self.record != NO_RECORD
            if recorded.any():
                half = modulus // 2
                far = recorded & (self.phase >= half)
                columns[PHASE_FIELD] = np.where(recorded, self.phase % half, self.phase)
                sign = np.where(far, -1, 1)
        return columns, sign

    def merge_key(self, columns: list[np.ndarray] | None = None) -> np.ndarray | None:
        """The identity fields packed into one integer key per row, in the
        order of `IDENTITY_FIELDS` (the Node first) with every field offset
        to its least value, so that the keys order the rows exactly as the
        lexsort of the fields does and equal keys are identical rows; None
        when the fields' ranges do not fit the register (62 bits), the
        lexsort then taking the same total order. The three columns of the
        amplitude law are constant on rows of no record (a width of 0 bits each)
        and leave the key and the order what they were."""
        if columns is None:
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

    def merge(self, modulus: int = 0) -> dict[tuple[int, int, int], int]:
        """Identical rows (equal in every field but the amount) merged, the
        amounts added, the rows in the total order of the identity fields,
        the Node first (so no second sort by Node is needed). A bijection: a
        permutation of rows and a sum of interchangeable units. The order
        is taken by the one packed key (`merge_key`) where the fields fit
        the register, by the lexsort of the fields otherwise: the same
        total order either way.

        Under the amplitude key (`modulus` the circle's N; BEAM_LAW note 37)
        the merge is the design's normal form: two rows of one record equal
        in every identity field but a phase difference of exactly N / 2
        cancel, the amounts subtract, the difference stays at the larger's
        phase and an equal pair leaves nothing (the row disappears: in a
        dark fringe the sum is zero). Rows with any other phase difference
        stay two rows; a row of no record never cancels, so without a lamp
        (every record 0) nothing cancels and the merge is what it was.
        Returns what the cancel removed, {(record, direction, content per
        unit): units} summed over the groups, so that the caller books the
        units, the content (units x content, exact by the packed key) and the
        labels that left (the ledger's `cancelled` lines and the layer's
        live count); empty without a record."""
        removed: dict[tuple[int, int, int], int] = {}
        if self.size == 0:
            return removed
        columns, sign = self.identity_columns(modulus)
        key = self.merge_key(columns)
        same = np.zeros(self.size, dtype=bool)
        if key is None:
            order = np.lexsort(tuple(reversed(columns)))
            self.take(order)
            columns = [column[order] for column in columns]
            sign = sign[order]
            same[1:] = True
            for column in columns:
                same[1:] &= column[1:] == column[:-1]
        else:
            order = np.argsort(key, kind="stable")
            self.take(order)
            sign = sign[order]
            key = key[order]
            same[1:] = key[1:] == key[:-1]
        starts = np.flatnonzero(~same)
        # The merged amounts are exact: in the register when no group's sum
        # can leave it, in Python integers otherwise, and bounded.
        signed = self.amount if not modulus else self.amount * sign
        if int(self.amount.max()) * self.size <= MOMENTUM_BOUND:
            amount = np.add.reduceat(signed, starts)
            whole = np.add.reduceat(self.amount, starts) if modulus else amount
        else:
            merged = np.add.reduceat(signed.astype(object), starts)
            if max(abs(int(v)) for v in merged) > MOMENTUM_BOUND:
                raise OverflowError(
                    f"{BEAM_LAW}: the amount of a merged row exceeds the integer bound {MOMENTUM_BOUND}"
                )
            amount = merged.astype(np.int64)
            whole = (
                np.add.reduceat(self.amount.astype(object), starts).astype(np.int64)
                if modulus
                else amount
            )
        # The undelivered shares of merged rows add (the momentum a row has
        # not yet delivered is the group's); bounded like the amounts.
        shares_summed: dict[str, np.ndarray] = {}
        for name in ("share_x", "share_y", "share_z"):
            column = getattr(self, name)
            if column.any():
                summed = np.add.reduceat(column.astype(object), starts)
                if max(abs(int(v)) for v in summed) > MOMENTUM_BOUND:
                    raise OverflowError(
                        f"{BEAM_LAW}: the undelivered share of a merged row exceeds the integer "
                        f"bound {MOMENTUM_BOUND}"
                    )
                shares_summed[name] = summed.astype(np.int64)
        self.keep(~same)
        for name, summed in shares_summed.items():
            setattr(self, name, summed)
        if modulus:
            # The cancel: the signed sum's magnitude stays, at the phase of
            # the larger side (the half-circle phase of the group, plus the
            # half circle when the far side was larger, which a lone row on
            # the far half is); an empty group leaves, its units booked per
            # (record, direction).
            half = modulus // 2
            cancelled = whole - np.abs(amount)
            for k in np.flatnonzero(cancelled > 0).tolist():
                slot = (int(self.record[k]), int(self.direction[k]), int(self.content[k]))
                removed[slot] = removed.get(slot, 0) + int(cancelled[k])
            recorded = self.record != NO_RECORD
            base = np.where(recorded, self.phase % half, self.phase)
            self.phase = np.where(recorded & (amount < 0), base + half, base)
            self.amount = np.abs(amount)
            self.arrival[:] = NO_ARRIVAL
            alive = self.amount > 0
            if not alive.all():
                self.keep(alive)
            return removed
        self.amount = amount
        self.arrival[:] = NO_ARRIVAL
        return removed

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
                int(self.record[i]),
                int(self.branch[i]),
                int(self.multiplicity[i]),
                int(self.birth[i]),
                int(self.hand[i]),
                int(self.share_x[i]),
                int(self.share_y[i]),
                int(self.share_z[i]),
            )
            for k, i in enumerate(range(lo, stop))
        ]

    def labels(self, rows: np.ndarray, unit: np.ndarray, free: bool) -> np.ndarray:
        """The momentum labels of the given rows (`momentum_labels`, the one
        label of the law) along the unit vectors `unit` (the flight's
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
        # The unit vectors of the directions (the flight's `labels`).
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
RULE_CODES = {"pass": 0, "read": 1, "measure": 2, "rerelease": 3, BECOME_RULE: 4}
PASS_RULE, READ_RULE, MEASURE_RULE = RULE_CODES["pass"], RULE_CODES["read"], RULE_CODES["measure"]
RERELEASE_RULE = RULE_CODES["rerelease"]
TRANSFORM_RULE = RULE_CODES[BECOME_RULE]
RULE_NAMES = {code: name for name, code in RULE_CODES.items()}
MEASURE_RULE_NAME = "measure"


# -- the transformation ------------------------------------------------------------


def transform(
    entry: Measured,
    rule: Transformation,
    trigger: str,
    tick: int,
    ledger: Ledger,
    families: tuple[FamilyDefinition, ...],
) -> None:
    """The one rule `become` (the weak force in the world's terms, the model
    owner's "go on everything", 2026-09-20; the physicist's design, WEAK.md
    2.2; BEAM_LAW note 36 (iii)), called from its two triggers, the click
    (step 4: an arrival of the entry's family clicked as `measure` clicks
    it) and the clock (step 5: the self-creation whose age is at the key
    `at`, `ages_at_key`, the gate `crowd` open): the measured event becomes
    an event of the family `into` and releases the rest as products.

    1. The products are paid from what the event holds of its own family:
       R = the sum of amount x content; an event that holds less refuses
       the run naming itself (a declared transformation that cannot be
       paid is a defect of the world, loud, never silent).
    2. The family line moves: held[into] += held[from] - R, held[from] = 0,
       the event's family is `into`; every other family held (the strong
       unit, absorbed content, clicked units) stays where it is; the
       event's number, position, set, momentum, age, phase, owed count and
       detector set are untouched (it is the same measured event with
       another family's content; its rays come home as before). The books'
       `became` line takes -held[from] on the family left and +(held[from]
       - R) on the family become.
    3. The products become pending rows (`PendingRow`): product k with its
       amount, its content per unit, the parent's phase at the trigger,
       the tie offset k (born in step 5 apportioned whole over the event's
       directions with the leftover counted from (clock age + k) mod n, as
       a re-release is, so that two products of amount 1 leave on
       different directions) and `thrown` (the recoil over all the
       products, free and paid: a free product is a thing thrown, not the
       field).
    4. The record: the `become` line is written at the products' birth
       (step 5), when their directions and the recoil are known, with the
       trigger and its tick.
    5. The transformation is the event's one change of family: its clock
       trigger and every `become` entry of its table are consumed, the
       entries reset to the keys' own rule for their family with no
       window (a `become` entry is the transformation's; the other entries
       stay as declared), the contact under them the default.

    One-way (a change of a measured event's record, as a click and a
    release are; the walk and the collision read nothing of it), local
    (the event's own record, the arrival at its Node), fixed work (one
    comparison per self-creation at the trigger, one apportioning per
    product at the birth), fixed storage (the declaration), no draw, no
    register, no formula in a payload."""
    source = entry.family
    needed = rule.needed
    held = entry.held[source]
    if held < needed:
        raise ValueError(
            f"{BEAM_LAW}: measured event {entry.number} at {list(entry.position)} cannot pay its "
            f"transformation into {families[rule.into].name!r} at tick {tick}: it holds {held} of "
            f"{families[source].name!r} and the products need {needed}"
        )
    moved = held - needed
    entry.held[rule.into] = bounded(entry.held[rule.into] + moved, entry, "content")
    entry.held[source] = 0
    ledger.held_became[source] -= held
    ledger.held_became[rule.into] += moved
    entry.family = rule.into
    entry.rho = entry.family_values[rule.into][CHARGE_INDEX]
    for k, (family, amount, content) in enumerate(rule.products):
        # The product's hand is its family's (`hand-v1`); the right-hand
        # rule reads it against the parent's axis at the birth (step 5).
        entry.pending[family].append(
            PendingRow(amount, content, entry.phase, k, True, hand=families[family].hand)
        )
    entry.became += 1
    entry.transformed.append((trigger, tick, source, rule.into, entry.counted))
    entry.become = None
    entry.transforms = [None] * len(entry.transforms)
    rules: list[str] = []
    windows: list[int | None] = []
    reads: list[str] = []
    widths: list[int | None] = []
    contact: list[str] = []
    for f, (rule_f, window, component, width, contact_f) in enumerate(
        zip(entry.table, entry.windows, entry.reads, entry.widths, entry.contact, strict=True)
    ):
        if rule_f == BECOME_RULE:
            rule_f = default_rule(families[f])
            window, component, width, contact_f = None, default_reads(rule_f), None, CONTACT_DEFAULT
        rules.append(rule_f)
        windows.append(window)
        reads.append(component)
        widths.append(width)
        contact.append(contact_f)
    entry.table = tuple(rules)
    entry.windows = windows
    entry.reads = tuple(reads)
    entry.widths = widths
    entry.contact = tuple(contact)


FIRST = np.zeros(1, dtype=np.int64)
NEW_RUN = np.ones(1, dtype=bool)
# A row born at a self-creation, before it is placed: (direction, amount,
# content per unit, phase, thrown, record, branch, multiplicity, birth, hand).
BornRow = tuple[int, int, int, int, bool, int, int, int, int, int]
# The record's identity (the amplitude law): the emitter's number x 2^32 +
# the birth's ordinal at the emitter, below 2^62 (the number below 2^30 and
# the ordinal below 2^32).
RECORD_SHIFT = 32
RECORD_BOUND = (1 << 62) - 1


def record_identity(number: int, ordinal: int) -> int:
    """The identity of a record born by a measured event: its number x 2^32
    + the ordinal of the birth at it (from 1), refused beyond the bound
    naming the emitter."""
    identity = (number << RECORD_SHIFT) + ordinal
    if ordinal >= (1 << RECORD_SHIFT) or identity > RECORD_BOUND:
        raise OverflowError(
            f"{BEAM_LAW}: the record identity of measured event {number} at its birth {ordinal} "
            f"exceeds the integer bound {RECORD_BOUND}"
        )
    return identity


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
    # The amplitude law's columns of the home rows and of the taken rows,
    # carried into their re-creation and onto the click lines of a record.
    h_record: list[int] = field(default_factory=list)
    h_branch: list[int] = field(default_factory=list)
    h_multiplicity: list[int] = field(default_factory=list)
    t_record: list[int] = field(default_factory=list)
    t_branch: list[int] = field(default_factory=list)
    t_multiplicity: list[int] = field(default_factory=list)
    h_birth: list[int] = field(default_factory=list)
    t_birth: list[int] = field(default_factory=list)
    # The shares of the taken rows (their push on a body, `share_of`; the
    # label itself on a row of no record), the remainder per group (the
    # labels less the shares of an absorbed group, to the books) and the
    # remainder per measured event of the home rows.
    t_share: list[list[int]] = field(default_factory=list)
    g_remainder: list[list[int]] = field(default_factory=list)
    h_remainder: dict[int, list[int]] = field(default_factory=dict)
    t_age: list[int] = field(default_factory=list)
    t_arrival: list[int] = field(default_factory=list)
    # The hand of the home rows, of the taken rows and of the rows that
    # pass (`hand-v1`): carried into the re-creation and onto the lines.
    h_hand: list[int] = field(default_factory=list)
    t_hand: list[int] = field(default_factory=list)
    p_hand: list[int] = field(default_factory=list)
    # The rows that pass a gate: per measured event (k0, k1).
    passes: dict[int, tuple[int, int]] = field(default_factory=dict)
    p_number: list[int] = field(default_factory=list)
    p_amount: list[int] = field(default_factory=list)
    p_phase: list[int] = field(default_factory=list)
    p_below: list[bool] = field(default_factory=list)
    # The record and the birth phase of the rows that pass (the pass line
    # carries them as the click line does, BEAM_LAW note 41).
    p_record: list[int] = field(default_factory=list)
    p_birth: list[int] = field(default_factory=list)
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
    # The window used per taken row, for the entries whose window is read
    # from a reading (issue #363; empty for a family without one).
    t_window: list[int] = field(default_factory=list)
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


def gate_ready(
    pending: list[PendingRow], gate: Gate, entry: Measured, vectors: np.ndarray
) -> list[int] | None:
    """The records a gate acts on, read from the rows pending at the entry
    alone (the design's local hold, section 10; the review of (v), B3: the
    GameBoard never reads the layer): one record per emitter (the lamp of
    the identity's number; a row of a joined record already carries the
    survivor's identity), the earliest born of each, at least `parties`
    of them; the control the record whose rows arrive on the entry's
    declared `control` direction (refused unless exactly one emitter's
    record does), then the others in the order of their identities; None
    while fewer than `parties` emitters have rows pending."""
    by_emitter: dict[int, int] = {}
    arrivals: dict[int, set[int]] = {}
    for row in pending:
        if row.record == NO_RECORD:
            continue
        emitter = row.record >> 32
        by_emitter[emitter] = min(by_emitter.get(emitter, row.record), row.record)
        arrivals.setdefault(row.record, set()).add(row.arrival)
    if len(by_emitter) < gate.parties:
        return None
    identities = sorted(by_emitter.values())
    if gate.control is None:
        return identities[:1]
    controls = [identity for identity in identities if gate.control in arrivals[identity]]
    if len(controls) != 1:
        raise ValueError(
            f"{BEAM_LAW}: the gate of measured event {entry.number} at {list(entry.position)} "
            f"finds {len(controls)} records arriving on its control direction "
            f"{[int(v) for v in vectors[gate.control]]} among {len(identities)} pending: one "
            "control record"
        )
    control = controls[0]
    return [control] + [identity for identity in identities if identity != control][: gate.parties - 1]


def apply_gate(
    layer: Layer,
    tick: int,
    entry: Measured,
    family_name: str,
    pending: list[PendingRow],
    records: list[int],
    record: Record | None,
) -> tuple[list[PendingRow], list[PendingRow]]:
    """The CNOT on the pending rows of the records: the layer joins them
    into the first (the control), every row replicated over the other
    records' labels with its multiplicity times the copies, relabelled by
    the joint label after the permutation, on the survivor's identity; the
    units the copies add are booked on the layer's live count as a split
    books its rows (the review of (v), B1). Returns the rows to re-emit and
    the rows of other records, kept."""
    survivor, others = records[0], records[1:]
    present: dict[int, set[int]] = {}
    here: dict[int, int] = {}
    for row in pending:
        live = layer.resolve(row.record) if row.record != NO_RECORD else None
        if live is not None and live.identity in records:
            present.setdefault(live.identity, set()).add(label_of(row.branch))
            here[live.identity] = here.get(live.identity, 0) + row.amount
    label_map, arm_offsets = layer.join(tick, survivor, others, present, here)
    found: list[PendingRow] = []
    kept: list[PendingRow] = []
    added = 0
    for row in pending:
        live = layer.resolve(row.record) if row.record != NO_RECORD else None
        if live is None:
            found.append(row)
            continue
        if live.identity != survivor:
            kept.append(row)
            continue
        origin = row.record
        joints = label_map[(origin, label_of(row.branch))]
        copies = len(joints)
        if row.multiplicity > MOMENTUM_BOUND // copies:
            raise OverflowError(
                f"{BEAM_LAW}: the multiplicity {row.multiplicity} x {copies} of the gate at measured "
                f"event {entry.number} at {list(entry.position)} exceeds the integer bound "
                f"{MOMENTUM_BOUND}"
            )
        arm = arm_of(row.branch) + arm_offsets[origin]
        for joint in joints:
            found.append(
                row._replace(
                    record=survivor,
                    branch=branch_of(arm, joint),
                    multiplicity=row.multiplicity * copies,
                )
            )
        if copies > 1:
            layer.split(survivor, row.amount, row.amount * copies)
            added += row.amount * (copies - 1)
    if record is not None:
        joined = layer.records[survivor]
        record(
            {
                "event": "gate",
                "tick": tick,
                "node": list(entry.position),
                "measured": entry.number,
                "family": family_name,
                "kind": "cnot",
                "survivor": survivor,
                "joined": list(others),
                "present": [[identity, sorted(labels)] for identity, labels in sorted(present.items())],
                "labels": [[label, weight] for label, weight in sorted(joined.labels.items())],
                "arms": joined.arms,
                "rows": len(found),
                "added": added,
            }
        )
    return found, kept


def rotate_rows(
    pending: list[PendingRow],
    rotation: Rotation,
    modulus: int,
    entry: Measured,
    layer: Layer | None,
    record: Record | None,
    tick: int,
) -> list[PendingRow]:
    """The rotation of one label bit on the rows pending (the design's 2.2):
    per row two rows on the bit cleared and set, the amounts w C' and w S'
    of the half-angle tables at the setting, the multiplicity m x 65536,
    the phases as the matrix's signs and the turn say."""
    c, s = half_angle(rotation.setting, modulus)
    scale = PHASE_COSINE_SCALE * PHASE_COSINE_SCALE
    found: list[PendingRow] = []
    # Per row of a record the units before and after (the layer's live
    # count follows the amounts: w becomes w C' + w S').
    turned: list[list[int]] = []
    for row in pending:
        if row.record == NO_RECORD:
            found.append(row)
            continue
        if row.multiplicity > MOMENTUM_BOUND // scale or row.amount > AMOUNT_BOUND // PHASE_COSINE_SCALE:
            raise OverflowError(
                f"{BEAM_LAW}: the multiplicity {row.multiplicity} x {scale} of the rotation at "
                f"measured event {entry.number} at {list(entry.position)} exceeds the integer "
                f"bound {MOMENTUM_BOUND}"
            )
        arm, label = arm_of(row.branch), label_of(row.branch)
        mask = 1 << rotation.bit
        clear, set_ = label & ~mask, label | mask
        if label & mask:
            born = [(clear, s, rotation.turn), (set_, c, rotation.turn)]
        else:
            born = [(clear, c, 0), (set_, s, modulus // 2)]
        units = 0
        for joint, amplitude, turn in born:
            if amplitude:
                units += row.amount * amplitude
                found.append(
                    row._replace(
                        amount=row.amount * amplitude,
                        phase=(row.phase + turn) % modulus,
                        branch=branch_of(arm, joint),
                        multiplicity=row.multiplicity * scale,
                    )
                )
        turned.append([row.record, row.amount, units])
        if layer is not None:
            layer.split(row.record, row.amount, units)
    if layer is not None:
        for identity in sorted({row.record for row in pending if row.record != NO_RECORD}):
            layer.rotate(identity, rotation.bit)
    if record is not None and turned:
        record(
            {
                "event": "rotate",
                "tick": tick,
                "node": list(entry.position),
                "measured": entry.number,
                "setting": rotation.setting,
                "bit": rotation.bit,
                "turn": rotation.turn,
                "rows": len(found),
                "records": turned,
            }
        )
    return found


def entry_rotation(
    plan: FamilyPlan, detector_set: DetectorSet, turn: int, k: int
) -> tuple[int, int] | None:
    """The rotation a `sum` set's entry applies to a taken row (the
    amplitude law): its window's setting (declared, or read from a reading)
    and the entry's turn; None without a window or on another reading."""
    if not detector_set.sum or not plan.t_window:
        return None
    setting = plan.t_window[k]
    if setting < 0:
        return None
    return setting, turn


def taken_rows(plan: FamilyPlan, k0: int, k1: int) -> list[list[int]]:
    """The taken rows of a record: their record, branch, multiplicity,
    amount, phase and arrival, for the group lines (empty where no row of
    the group carries a record, and the key is then not written)."""
    return [
        [
            plan.t_record[k],
            plan.t_branch[k],
            plan.t_multiplicity[k],
            plan.t_amount[k],
            plan.t_phase[k],
            plan.t_arrival[k],
        ]
        for k in range(k0, k1)
        if plan.t_record[k] != NO_RECORD
    ]


def row_hand(plan: FamilyPlan, k: int, measured: dict[int, Measured]) -> int:
    """The hand a click line carries for a taken row (`hand-v1`): the
    meaning of its label bit on its arm when the lamp of its record named
    the hands of its labels (the hand as a label bit named, the amplitude
    law's branched family), else the row's own `hand` column. A report of
    the record; nothing of the law reads it."""
    identity = plan.t_record[k]
    if identity != NO_RECORD:
        emitter = measured.get(identity >> RECORD_SHIFT)
        if emitter is not None and emitter.lamp_label_hands is not None:
            branch = plan.t_branch[k]
            return emitter.lamp_label_hands[(label_of(branch) >> arm_of(branch)) & 1]
    return plan.t_hand[k]


def read_hands(
    hand: np.ndarray, record: np.ndarray, branch: np.ndarray, entries: list[Measured]
) -> np.ndarray:
    """The hand a parity filter reads of each row (`hand-v1`, BEAM_LAW note
    39): the row's `hand` column, or, for a row of a record whose lamp
    named the hands of its labels, the hand its label bit means on its arm
    (the reading `row_hand` makes for the click line), so that a filter on
    a branched family is the which-path click on the label (the design's
    section 4, FORM.md section 4: the rows of a hand are the rows of a
    channel). The lamp is found by the record's identity, whose high bits
    are the emitter's number: a world constant, nothing of the law."""
    found = hand.copy()
    recorded = record != NO_RECORD
    if not recorded.any():
        return found
    emitter = record >> RECORD_SHIFT
    for entry in entries:
        if entry.lamp_label_hands is None:
            continue
        rows = np.flatnonzero(recorded & (emitter == entry.number))
        if rows.shape[0] == 0:
            continue
        zero, one = entry.lamp_label_hands
        arm = branch[rows] >> LABEL_BITS
        bit = ((branch[rows] & LABEL_MASK) >> arm) & 1
        found[rows] = np.where(bit == 0, zero, one)
    return found


def group_hand(plan: FamilyPlan, k0: int, k1: int) -> int | None:
    """The hand of a group of taken rows for its `read` or `rerelease`
    line: the one hand of its rows, None where they differ."""
    hands = {plan.t_hand[k] for k in range(k0, k1)}
    return hands.pop() if len(hands) == 1 else None


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
    scales: tuple[int, ...],
    counts: CountTable,
    entry: Measured,
) -> list[int]:
    """The push a measured event A takes from one group of arriving rays:
    ONE signed inner product over the columns (the model owner's decision
    of 2026-09-20, "one mechanism for all the laws on the GameBoard"; the
    mathematician's verified form), since the fraction-free push of the
    same day (BEAM_LAW note 41) on the reader's own accumulators. `moment`
    is V_B, the label flow of the group (Python integers, exact);
    `charges` the reader's charge in every column as the frame read it,
    the pairs (E_c, D_c) (gravity: its content M_A over 1; charge: rho_A
    M_A; a declared column: its value times the content, summed over the
    families it holds); `values` the arriving family's value per unit of
    content in every column, the pairs (n_c, d_c) (gravity (1, 1), charge
    rho_B, a declared column's value or (0, 1)); `columns` the world's
    (name, sign) per column; `scales` the columns' common denominators
    Lambda_c (`world.column_scales`: every D_c and every d_c divides its
    column's); `accumulators` the reader's `acc_push`, per column and axis
    one bounded integer. For a free family's rays, per axis and column,

        X = V x E_c x n_c x (Lambda_c / D_c) x (Lambda_c / d_c),
        push_A += epsilon_c x the count `by_drive(acc_push[c][a], X, Lambda_c^2)` gains,

    the whole part the accumulator then holds with the sign of the sum
    (the drive's rule: a reversed flow first cancels what it had
    accumulated the other way), the remainder kept on the record below
    Lambda_c^2 in magnitude; every column on its own accumulator, never
    summed before the count (the mathematician's section 4). At a flow of
    one sign the count is the same integer as the whole part off the
    reader's clock, `sign(V E_c n_c) x by_clock(age_A, |V E_c n_c|, D_c
    d_c)`, from an empty accumulator at the first read, and differs from
    it by at most one unit per column, axis and interval as the flow
    varies or the read begins at a later age, the sum over any period
    exact (FORM.md section 2; until then the floor off the clock at the
    reader's age, its remainder discarded). A column with E_c n_c = 0
    adds nothing. The gravity column, (1, 1) on every family with the sign
    minus, has Lambda = 1 and the count is |V M_A| exactly, the law's -M_A
    V_B; the charge column is the electric part as landed, exact wherever
    the charges are whole (Lambda = 1, the register's every world but the
    series 7 pair), so a world without a declared column reads the
    two-column form M_A (rho_A rho_B - 1) x V_B integer by integer, and the
    strong force is a third column with the sign minus, not a term of this
    function. For a paid family's rays the push is V_B itself (kappa = 1,
    the label carries h s). The bounds (the mathematician's R1 to R3):
    each column's product |V| x |E_c n_c| x Lambda_c^2 / (D_c d_c) is
    tested by division BEFORE it is formed and refused naming the column;
    the partial sum is bounded after every column (`bounded`); the caller
    bounds the momentum it joins."""
    if not free:
        return [bounded(moment[axis], entry, "push") for axis in range(3)]
    push = [0, 0, 0]
    for column, ((name, sign), (numerator, denominator), (n, d)) in enumerate(
        zip(columns, charges, values, strict=True)
    ):
        if not numerator or not n:
            continue
        scale = scales[column]
        # |V| x |E n| x (Lambda / D) x (Lambda / d) tested by division
        # before any product is formed.
        if abs(numerator) > MOMENTUM_BOUND // abs(n):
            raise column_bound_error(entry, name, moment[0], abs(numerator) * abs(n))
        factor = numerator * n
        lift = (scale // denominator) * (scale // d)
        if abs(factor) > MOMENTUM_BOUND // lift:
            raise column_bound_error(entry, name, moment[0], abs(factor) * lift)
        factor *= lift
        totals = []
        for axis in range(3):
            v = moment[axis]
            if v and abs(v) > MOMENTUM_BOUND // abs(factor):
                raise column_bound_error(entry, name, v, abs(factor))
            totals.append(v * factor)
        # The column's three rows of the table gain X over Lambda_c^2 in
        # one loop (at Lambda 1 the whole part is X itself, the row 0).
        wholes = counts.advance("push", index=column, values=totals)
        for axis in range(3):
            push[axis] = bounded(push[axis] + sign * wholes[axis], entry, "push")
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
    layer: Layer | None = None,
) -> GameBoardDiagnostics:
    """A Node's whole interval for the rays present, at every Node (the
    module docstring, steps 1 to 6). With `inverse` the bijective steps are
    run in reverse order with their inverses (the collision, then the walk)
    on a GameBoard without measured events; the border has no inverse.
    Under the amplitude law `layer` is the apparatus's layer
    (`amplitude.Layer`): it is told of every end of a row of a record (a
    click, a face, the border), of every birth and split, and of the
    merge's cancels, and its completions are read after step 4 and after
    the merge; steps 1 to 3 never read it."""
    families = world.families
    free_of = [definition.free for definition in families]
    # The columns of the world, (name, sign), and every family's value per
    # column: the arriving side of the push (the reader's side is the
    # charges the frame read).
    columns = world.columns
    values_of = [definition.values for definition in families]
    # The columns' common denominators, the accumulators' (`push_form`).
    scales = world.column_scales
    flight, collision = tables.flight, tables.collision
    # The unit vectors of the directions at the scale Q: what every label
    # and every vector or tensor moment of the reading is taken on.
    unit = flight.labels
    modulus = world.phase_steps
    # Whether the world declares a hand anywhere (`hand-v1`): the lines of
    # the record then carry `hand`, and only then.
    handed = world.handed
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
    # The crossing rule (the model owner's record 158 of 2026-09-20; BEAM_LAW
    # note 47): a row and a body meet once, at the crossing of their world
    # lines. Per measured event the heading e of the Link its body crossed
    # this interval (the zero vector without a step) and e' of the interval
    # before, off its own record (`Measured.step_port`, `last_step_port`,
    # set by `_move` before the law); the Nodes a body ENTERED this
    # interval (the leading face of its moved set: its neighbour along e
    # is not in the set) and, on the trailing face (an origin Node the
    # moved set left, of free space), the Node with the event whose Link
    # ends there: a few flat indices per stepping body, looked up per row
    # (host work per row, not per Node of the GameBoard). A body without
    # a step this interval marks nothing; the step of a body on a set is
    # the set's, each Node with its own origin.
    ev_step = np.zeros((events, DIMENSIONS), dtype=np.int64)
    ev_last = np.zeros((events, DIMENSIONS), dtype=np.int64)
    entered_nodes: list[int] = []
    trail_pairs: list[tuple[int, int]] = []
    for which, entry in enumerate(entries):
        if entry.last_step_port >= 0:
            ev_last[which] = PORT_HEADINGS[entry.last_step_port]
        if entry.step_port < 0:
            continue
        step_link_port = entry.step_port
        ev_step[which] = PORT_HEADINGS[step_link_port]
        set_nodes = set(entry.nodes)
        for member_node in set_nodes:
            ahead_node = adjacent_node(member_node, step_link_port, shape, world.periodic)
            if ahead_node is None or ahead_node not in set_nodes:
                entered_nodes.append(int(stores[0].flat(member_node)))
            origin_node = adjacent_node(member_node, step_link_port ^ 1, shape, world.periodic)
            if origin_node is not None and origin_node not in set_nodes:
                origin_index = int(stores[0].flat(origin_node))
                if not occupied[origin_index]:
                    trail_pairs.append((origin_index, which))
    entered = np.array(sorted(entered_nodes), dtype=np.int64)
    trail_pairs.sort()
    trail_nodes = np.array([flat for flat, _ in trail_pairs], dtype=np.int64)
    trail_events = np.array([which for _, which in trail_pairs], dtype=np.int64)

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
        target = collision.act(code, backward)
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
        # The meeting's inverse first (the inverse order of the interval:
        # the meeting, then the table, then the walk), read back from the
        # untouched crowd (`meeting.meet`).
        if world.meeting:
            meet(stores, world, tables, occupied, ledger, inverse=True)
        for family, store in enumerate(stores):
            if store.size == 0:
                continue
            collide(store, backward=True)
            resting = store.direction < REST_DIRECTIONS
            # The age back by one (whole; a rest ray keeps its age); the
            # Link crossed at that age by the flight's rule. A ray at age 0
            # is at its birth, which has no inverse.
            back = np.where(resting, store.age, store.age - 1)
            if (back < 0).any():
                raise ValueError(
                    f"{BEAM_LAW}: the inverse walk of a ray at age 0 (its birth has no inverse)"
                )
            step = flight.walk_step(store.direction, back)
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
            turned = families[family].phase_per_link * moved
            per_age = families[family].phase_per_age
            if per_age is not None:
                turned = turned + np.where(resting, 0, by_clock_rows(back, per_age[0], per_age[1]))
            store.phase = (store.phase - turned) % modulus
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
        # The flight's rule at the row's age: the position's accumulator
        # per direction, off the age (the rate constant over the flight).
        step = flight.walk_step(store.direction, store.age)
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
                    amounts,
                    (store.phase[through] - store.birth[through]) % modulus,
                    FIRST,
                    tables.cosines,
                    tables.sines,
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
            if layer is not None:
                gone_x, gone_y, gone_z = store.coordinates(store.node[gone])
                for k, row_index in enumerate(gone.tolist()):
                    if store.record[row_index] != NO_RECORD:
                        layer.end(
                            tick,
                            layer.face_index[int(port[row_index])],
                            int(store.record[row_index]),
                            int(store.branch[row_index]),
                            int(store.multiplicity[row_index]),
                            int(store.amount[row_index]),
                            int(store.phase[row_index]),
                            node=(int(gone_x[k]), int(gone_y[k]), int(gone_z[k])),
                            content=int(store.amount[row_index] * store.content[row_index]),
                            momentum=[int(v) for v in labels[k]],
                        )
            if record is not None:
                for k, index in enumerate(gone):
                    face_line: dict[str, object] = {
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
                    if store.record[index] != NO_RECORD:
                        face_line["record"] = int(store.record[index])
                        face_line["branch"] = int(store.branch[index])
                        face_line["multiplicity"] = int(store.multiplicity[index])
                        face_line["u"] = int(store.birth[index])
                    if handed:
                        face_line["hand"] = int(store.hand[index])
                    record(face_line)
        store.node = coordinates @ np.array(store.strides, dtype=np.int64)
        crossed = moved & ~escaped
        crossed_node, crossed_port = store.node[crossed], port[crossed]
        crossed_amount = store.amount[crossed]
        # A rest ray keeps its age (the rest slots belong to the six-heading
        # alphabet, whose line it resumes when a collision moves it); a
        # moving ray's age advances by one, whole.
        resting = store.direction < REST_DIRECTIONS
        # The phase per Link crossed (the integer `phase_per_link`) and,
        # under the amplitude law, the phase per interval of age (the pair
        # form: `by_clock(age, n, d)` at every walk that advances the age,
        # the one primitive of every rate, carried through a re-emission).
        turned = definition.phase_per_link * moved
        if definition.phase_per_age is not None:
            rate_n, rate_d = definition.phase_per_age
            turned = turned + np.where(resting, 0, by_clock_rows(store.age, rate_n, rate_d))
        store.age = np.where(resting, store.age, store.age + 1)
        store.phase = (store.phase + turned) % modulus
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
    # Then the meeting (the model owner, 2026-09-20, "DECIDED: the meeting,
    # M-R"; under the world key `meeting`): at every Node of free space every
    # paid unit reads the free crowd of the other numbers and turns toward
    # it by its phase register; the crowd untouched (`meeting.meet`).
    if world.meeting:
        meet(stores, world, tables, occupied, ledger)

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
        # The width of every entry's window: the declared `phase_width`, the
        # half circle where none is declared.
        ev_width = np.array(
            [[default_width(modulus) if w is None else w for w in e.widths] for e in entries],
            dtype=np.int64,
        )
        # The parity filter of every entry (`hand-v1`): the hand it admits,
        # 0 where it admits every hand.
        ev_hand = np.array([list(e.hands) for e in entries], dtype=np.int64).reshape(events, count)
        # The detector set of every measured event, its threshold and its
        # reading, indexed by the set's index.
        ev_set = np.array([e.detector_set.index for e in entries], dtype=np.int64)
        set_of = {e.detector_set.index: e.detector_set for e in entries}
        set_count = int(ev_set.max()) + 1
        st_threshold = np.ones(set_count, dtype=np.int64)
        st_pointer = np.zeros(set_count, dtype=bool)
        st_sum = np.zeros(set_count, dtype=bool)
        for set_index, detector_set in set_of.items():
            st_threshold[set_index] = detector_set.threshold
            st_pointer[set_index] = detector_set.pointer
            st_sum[set_index] = detector_set.sum
        # The windows read from a reading (issue #363, 2026-09-20): per
        # (measured event, family) the family whose rows at the set give the
        # centre (-1 for a declared or absent centre) and the offset; the
        # settings per set, read once per named family from the rows
        # present after the walk and the collision, before any table acts
        # (-1 where the set holds no such row or the pointer is zero).
        ev_read_family = np.array(
            [[-1 if w is None else w[0] for w in e.window_reads] for e in entries], dtype=np.int64
        ).reshape(events, count)
        ev_read_offset = np.array(
            [[0 if w is None else w[1] for w in e.window_reads] for e in entries], dtype=np.int64
        ).reshape(events, count)
        settings = np.full((count, set_count), -1, dtype=np.int64)
        for named in np.unique(ev_read_family[ev_read_family >= 0]).tolist():
            steps_of = setting_steps(
                stores[named],
                node_event,
                ev_number,
                ev_set,
                set_count,
                tables.cosines,
                tables.sines,
                modulus,
            )
            for set_index, chosen_step in enumerate(steps_of):
                if chosen_step is not None:
                    settings[named, set_index] = chosen_step
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
            ev = found[at]
            # The swap (C1 of the crossing rule, note 47): the rows of
            # another number at a trailing Node of a stepping body that
            # crossed its Link the other way this interval (their step
            # this interval -e, off the flight's rule at their age),
            # gathered with the rows at the set into the group of the
            # event; the reading's bound covers the larger group, at most
            # the rows at one more Node per Node of the set.
            swap = (
                np.flatnonzero(np.isin(store.node, trail_nodes))
                if trail_nodes.shape[0]
                else np.zeros(0, dtype=np.int64)
            )
            if swap.shape[0]:
                ev_swap = trail_events[np.searchsorted(trail_nodes, store.node[swap])]
                backward = (
                    flight.walk_step(store.arrival[swap], np.maximum(store.age[swap] - 1, 0))
                    == -ev_step[ev_swap]
                ).all(axis=1) & (store.number[swap] != ev_number[ev_swap])
                swap, ev_swap = swap[backward], ev_swap[backward]
                at = np.concatenate((at, swap))
                ev = np.concatenate((ev, ev_swap))
            if at.shape[0] == 0:
                return None
            order = np.argsort(ev, kind="stable")
            at, ev = at[order], ev[order]
            number = store.number[at]
            amount = store.amount[at]
            content = store.content[at]
            phase = store.phase[at]
            # The path phase (stage (vii)): what every rule of the GameBoard
            # reads of a record row's phase, the running phase less the
            # record's birth phase u (0 on a row of no record: the phase
            # itself). The re-creation carries the running phase.
            path = (phase - store.birth[at]) % modulus
            direction = store.direction[at]
            arrival = store.arrival[at]
            age_at = store.age[at]
            record_at = store.record[at]
            hand_at = store.hand[at]
            # The hand the parity filter reads: the column, or the label's
            # meaning on a branched family whose lamp named its hands.
            read_at = read_hands(hand_at, record_at, store.branch[at], entries)
            own = number == ev_number[ev]
            arrived = arrival != NO_ARRIVAL
            # The crossing (note 47), per row: the step it made this
            # interval s_1 and the one before s_2, off its arrival
            # direction and its age by the flight's rule (nothing kept),
            # and the headings e and e' of its measured event's step this
            # interval and the one before. A row that stepped in is met
            # (C3) unless it came over the body's own Link with the body
            # (C3': s_1 = e) or, in the interval after a step, comes over
            # that Link having rested at the origin during the step (C3'':
            # e = 0, s_1 = e', s_2 = 0, the leapfrog; a row younger than
            # two intervals made no step before); a row resident at a Node
            # the body entered this interval is met when its motion is
            # against the step (C2: u . e < 0), not when with it (C2') and
            # not when at rest (u = 0); a swap row (C1, gathered above)
            # stepped in against e and is met by the same line. A body
            # without a step reads its arrivals as before the rule.
            e_rows = ev_step[ev]
            stepped = e_rows.any(axis=1)
            s_1 = flight.walk_step(arrival, np.maximum(age_at - 1, 0))
            with_step = stepped & (s_1 == e_rows).all(axis=1)
            e_last = ev_last[ev]
            rested = (age_at >= 2) & ~flight.walk_step(arrival, np.maximum(age_at - 2, 0)).any(axis=1)
            leapfrog = ~stepped & e_last.any(axis=1) & (s_1 == e_last).all(axis=1) & rested
            against = (unit[direction] * e_rows).sum(axis=1) < 0
            crossing = (arrived & ~with_step & ~leapfrog) | (
                ~arrived & stepped & against & np.isin(store.node[at], entered)
            )
            # The direction a row is read on: an arrival's the direction it
            # arrived on (at a body's Node its direction, no collision
            # acting there; a swap row's the direction it crossed the Link
            # on), a resident row met by the step (C2) its own direction
            # (met at the crossing, its label along its motion), a resident
            # row not met the zero vector (`here`, as before the rule).
            read_on = np.where(arrived, arrival, np.where(crossing, direction, NO_ARRIVAL))
            plan = FamilyPlan()
            # The rows of the one reading over the set: every row at the set
            # of another number, rest and moving alike, on the unit vector of
            # its arrival (a row that did not step on the zero vector; at a
            # measured event's Node the arrival is the direction, no
            # collision acting there), the amounts as the weights and the
            # ages among them; the bound of the table checked in bulk here,
            # the table itself taken once below with the admitted rows.
            others = np.flatnonzero(~own)
            v_others = unit[read_on[others]]
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
                    # A record's row that came home joins its emitter by its
                    # share (stage (vii) step 3), the rest to the remainder.
                    home_record = store.record[at[home]]
                    home_shares = home_labels.tolist()
                    for k in np.flatnonzero(home_record != NO_RECORD).tolist():
                        i = int(at[home[k]])
                        m = int(store.multiplicity[i])
                        home_shares[k] = [
                            share_of(int(v), int(amount[home[k]]), m, int(acc[i]))[0]
                            for v, acc in zip(
                                home_labels[k].tolist(),
                                (store.share_x, store.share_y, store.share_z),
                                strict=True,
                            )
                        ]
                    taken_in = np.array(
                        [
                            [sum(home_shares[k][axis] for k in range(s, e)) for axis in range(3)]
                            for s, e in zip(starts.tolist(), (starts + sizes).tolist(), strict=True)
                        ],
                        dtype=object,
                    ).reshape(starts.shape[0], DIMENSIONS)
                    for event, s, e in zip(
                        ev_h[starts].tolist(), starts.tolist(), (starts + sizes).tolist(), strict=True
                    ):
                        plan.h_remainder[event] = [
                            sum(int(home_labels[k, axis]) - home_shares[k][axis] for k in range(s, e))
                            for axis in range(3)
                        ]
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
                plan.h_record = store.record[at[home]].tolist()
                plan.h_branch = store.branch[at[home]].tolist()
                plan.h_multiplicity = store.multiplicity[at[home]].tolist()
                plan.h_birth = store.birth[at[home]].tolist()
                plan.h_hand = hand_at[home].tolist()
                plan.events.update(h_events)

            def admit() -> (
                tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray] | None
            ):
                """The rows the threshold, the window and the rule admit,
                grouped by (measured event, number): the rows, the amounts
                that click (after `beam`'s pairing), the units the pairing
                keeps, the rules, the sets and the windows used; None when
                nothing is met."""
                # Met: the crossings of every other number at a table that
                # is not `pass`, ordered by detector set (then measured
                # event, then row): the threshold on the amount summed over
                # the set.
                rule = ev_rule[ev, family]
                met = np.flatnonzero(~own & crossing & (rule != PASS_RULE))
                if met.shape[0] == 0:
                    return None
                met = met[np.argsort(ev_set[ev[met]], kind="stable")]
                ev_m = ev[met]
                st_m = ev_set[ev_m]
                s_starts = group_starts(st_m)
                s_sizes = group_sizes(s_starts, met.shape[0])
                total = grouped_sums(amount[met], s_starts, int(s_sizes.max()))
                # The threshold: the amount summed over the set under both
                # readings (the pointer's square as a gate under `wave`,
                # issue #359 step A, is deleted at stage (vii) step 4, the
                # one click: a record's click is its ladder's, and the
                # crowd's pointer gives the set's phase and its record, not
                # a gate). No memory between intervals.
                set_threshold = st_threshold[st_m[s_starts]]
                below_set = np.asarray(total < set_threshold, dtype=bool)
                # The window: under `wave` it reads the set's phase, the
                # nearest step of the coherent pointer of the arrivals the
                # threshold admitted (a zero pointer has no phase and is
                # outside every window); under `beam` each ray's own phase.
                # Its width is the entry's (`phase_width`, the half circle
                # by default): the one floor `window_admits`.
                window = ev_window[ev_m, family]
                width_m = ev_width[ev_m, family]
                read_phase = path[met].copy()
                pointer_rows = st_pointer[st_m]
                if pointer_rows.any():
                    px, py = coherent_pointer(
                        amount[met], path[met], s_starts, tables.cosines, tables.sines
                    )
                    steps = pointer_phases(px, py, tables.cosines, tables.sines)
                    set_step = np.array([-1 if s is None else s for s in steps], dtype=np.int64)
                    read_phase = np.where(pointer_rows, np.repeat(set_step, s_sizes), read_phase)
                below = np.repeat(below_set, s_sizes)
                # A window read from a reading: the centre is the setting of
                # the row's set off the named family plus the offset; a set
                # without a setting (-2 on the row) admits nothing, and the
                # row passes naming `window` None.
                read_family = ev_read_family[ev_m, family]
                reading_window = read_family >= 0
                unset = np.zeros(window.shape[0], dtype=bool)
                if reading_window.any():
                    centre = settings[read_family[reading_window], st_m[reading_window]]
                    unset[reading_window] = centre < 0
                    window = window.copy()
                    window[reading_window] = np.where(
                        centre < 0,
                        -2,
                        (centre + ev_read_offset[ev_m, family][reading_window]) % modulus,
                    )
                inside = (window < 0) | (
                    (read_phase >= 0) & window_admits((read_phase - window) % modulus, width_m, modulus)
                )
                # Under `sum` (the amplitude law) a window is the rotation's
                # setting and gates nothing: every row is admitted, the
                # setting carried on the row (`t_window`); a split takes no
                # window either (a split is not a click).
                inside |= st_sum[st_m] | ((rule[met] == RERELEASE_RULE) & (record_at[met] != NO_RECORD))
                inside &= ~unset
                # The parity filter (`hand-v1`, BEAM_LAW note 39): an entry
                # with a hand admits the arrivals of that hand only; the
                # other hand and hand 0 pass, as an arrival outside the
                # window passes. Admitted = the threshold and the window
                # and the hand, three comparisons of what the row carries
                # with what the reader declares.
                admits = ev_hand[ev_m, family]
                inside &= (admits == NO_HAND) | (read_at[met] == admits)
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
                    plan.p_hand = read_at[met[p]].tolist()
                    plan.p_record = record_at[met[p]].tolist()
                    plan.p_birth = store.birth[at][met[p]].tolist()
                    plan.events.update(p_events)
                kept = np.flatnonzero(~passing)
                if kept.shape[0] == 0:
                    return None
                # The taken rows grouped by (measured event, number), the
                # rows of a group in row order.
                kept = kept[np.lexsort((number[met[kept]], ev[met[kept]]))]
                taken = met[kept]
                window_t = window[kept]
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
                pairing = np.flatnonzero(
                    ((rule_t == MEASURE_RULE) | (rule_t == TRANSFORM_RULE)) & ~st_pointer[st_t]
                )
                if pairing.shape[0] >= 2:
                    sets_p = st_t[pairing]
                    for set_index in np.unique(sets_p).tolist():
                        rows = pairing[sets_p == set_index]
                        if rows.shape[0] < 2:
                            continue
                        phases = path[taken[rows]].tolist()
                        left = a_t[rows].tolist()
                        arcs = ev_window[ev[taken[rows]], family].tolist()
                        arc_widths = ev_width[ev[taken[rows]], family].tolist()
                        for i, phase_i in enumerate(phases):
                            if left[i] == 0:
                                continue
                            for j in range(i + 1, len(phases)):
                                if left[j] == 0:
                                    continue
                                d = (phases[j] - phase_i - half) % modulus
                                if not (
                                    d == 0
                                    if arcs[i] < 0
                                    else bool(window_admits(d, arc_widths[i], modulus))
                                ):
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
                return taken, a_t, cancelled, rule_t, st_t, window_t

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
                    rows_v = np.concatenate((v_others, unit[read_on[split]]))
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
            plan.t_window = admitted[5][survivors].tolist()
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

            c_t, ph_t, path_t = content[taken], phase[taken], path[taken]
            age_t = age_at[taken]
            v_arrival = unit[read_on[taken]]
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
            # The push of a record's row on a body is its share of the
            # quantum's label (stage (vii) step 3, `share_of`); a row of no
            # record pushes by its label, so the moments are what they were
            # without a record.
            record_t = store.record[at[taken]]
            shares = labels.tolist()
            columns = (store.share_x, store.share_y, store.share_z)
            for k in np.flatnonzero(record_t != NO_RECORD).tolist():
                i = int(at[taken[k]])
                m = int(store.multiplicity[i])
                found = [
                    share_of(int(v), int(a_t[k]), m, int(column[i]))
                    for v, column in zip(labels[k].tolist(), columns, strict=True)
                ]
                shares[k] = [share for share, _ in found]
                if rule_t[k] == READ_RULE:
                    # The row goes on: the undelivered part stays on it.
                    for column, (_, rest) in zip(columns, found, strict=True):
                        column[i] = rest
            g_ends = (g_starts + g_sizes).tolist()
            plan.g_moment = [
                [sum(shares[k][axis] for k in range(s, e)) for axis in range(3)]
                for s, e in zip(g_starts.tolist(), g_ends, strict=True)
            ]
            plan.g_remainder = [
                [sum(int(labels[k, axis]) - shares[k][axis] for k in range(s, e)) for axis in range(3)]
                for s, e in zip(g_starts.tolist(), g_ends, strict=True)
            ]
            plan.t_share = shares
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
            plan.t_record = store.record[at[taken]].tolist()
            plan.t_branch = store.branch[at[taken]].tolist()
            plan.t_multiplicity = store.multiplicity[at[taken]].tolist()
            plan.t_birth = store.birth[at[taken]].tolist()
            plan.t_hand = hand_at[taken].tolist()
            plan.t_age = age_t.tolist()
            plan.t_arrival = read_on[taken].tolist()
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
            clicked = np.flatnonzero((rule_t == MEASURE_RULE) | (rule_t == TRANSFORM_RULE))
            if clicked.shape[0]:
                clicked = clicked[np.argsort(st_t[clicked], kind="stable")]
                st_c = st_t[clicked]
                c_starts = group_starts(st_c)
                c_sizes = group_sizes(c_starts, clicked.shape[0])
                totals_c = grouped_sums(a_t[clicked], c_starts, int(c_sizes.max())).tolist()
                pointer_x, pointer_y = coherent_pointer(
                    a_t[clicked], path_t[clicked], c_starts, tables.cosines, tables.sines
                )
                steps = pointer_phases(pointer_x, pointer_y, tables.cosines, tables.sines)
                last_phase = path_t[clicked][(c_starts + c_sizes - 1)].tolist()
                for k, set_index in enumerate(st_c[c_starts].tolist()):
                    if st_pointer[set_index]:
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
                # The rule as the interval's plan read it (a `become` entry
                # consumed by a transformation of this interval is applied
                # as the plan made it: the click).
                rule = RULE_NAMES[int(ev_rule[i, family])]
                # The entry's window read from a reading, if any: its
                # `pass` and `click` lines name the family read and the
                # centre used (issue #363).
                window_read = entry.window_reads[family]
                home_plan = plan.home.get(i)
                if home_plan is not None:
                    k0, k1, total, carried, taken_in = home_plan
                    pending = entry.pending[family]
                    for k in range(k0, k1):
                        pending.append(
                            PendingRow(
                                plan.h_amount[k],
                                plan.h_content[k],
                                plan.h_phase[k],
                                record=plan.h_record[k],
                                branch=plan.h_branch[k],
                                multiplicity=plan.h_multiplicity[k],
                                birth=plan.h_birth[k],
                                hand=plan.h_hand[k],
                            )
                        )
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
                        remainder = plan.h_remainder.get(i)
                        if remainder is not None:
                            ledger.remainder_momentum[family] = [
                                a + b
                                for a, b in zip(
                                    ledger.remainder_momentum[family], remainder, strict=True
                                )
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
                            centre = plan.p_window[k]
                            line["window"] = None if centre < 0 else centre
                        if window_read is not None:
                            line["reads"] = families[window_read[0]].name
                        if plan.p_record[k] != NO_RECORD:
                            # The record and its birth phase on the pass line
                            # as on the click line (since the fraction-free law,
                            # 2026-09-20, BEAM_LAW note 41: the Bell readers
                            # pair a row by its record, not by its tick).
                            line["record"] = plan.p_record[k]
                            line["u"] = plan.p_birth[k]
                        if handed:
                            line["hand"] = plan.p_hand[k]
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
                        # the family's value per column; every column's count is
                        # its accumulator's on the reader's record (the
                        # fraction-free push, note 41; until then floored at
                        # the reader's clock age).
                        k0, k1 = plan.g_start[gi], plan.g_end[gi]
                        # The flow is the rows' shares (a record's row
                        # pushes by its share of the label, stage (vii)
                        # step 3; a row of no record's share is its label),
                        # as `g_moment` is.
                        moment = plan.g_moment[gi]
                        push = push_form(
                            free,
                            moment,
                            entry.frame_charges,
                            values_of[family],
                            columns,
                            scales,
                            entry.counts,
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
                        # A `become` entry's click is tallied as the
                        # measure-click it is; the transformation is
                        # counted on `became`.
                        entry.taken[family][MEASURE_RULE_NAME if rule == BECOME_RULE else rule] += (
                            group_total
                        )
                        if rule == "read":
                            if layer is not None and detector_set.sum:
                                for k in range(k0, k1):
                                    if plan.t_record[k] != NO_RECORD:
                                        layer.end(
                                            tick,
                                            layer.set_index[detector_set.index],
                                            plan.t_record[k],
                                            plan.t_branch[k],
                                            plan.t_multiplicity[k],
                                            plan.t_amount[k],
                                            plan.t_phase[k],
                                            absorbed=False,
                                        )
                            if record is not None:
                                read_line: dict[str, object] = {
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
                                recorded_rows = taken_rows(plan, k0, k1)
                                if recorded_rows:
                                    read_line["rows"] = recorded_rows
                                if handed:
                                    read_line["hand"] = group_hand(plan, k0, k1)
                                record(read_line)
                            continue
                        ledger.transit_absorbed[family] += group_total
                        ledger.content_absorbed[family] += group_content
                        # The labels of an absorbed group beyond the shares
                        # matter took, to the books' `remainder` line.
                        ledger.remainder_momentum[family] = [
                            a + b
                            for a, b in zip(
                                ledger.remainder_momentum[family], plan.g_remainder[gi], strict=True
                            )
                        ]
                        k0, k1 = plan.g_start[gi], plan.g_end[gi]
                        if rule == "rerelease":
                            pending = entry.pending[family]
                            for k in range(k0, k1):
                                # Under the amplitude law the re-emission is
                                # the split by the entry's weights (an equal
                                # split where none is declared); the row's
                                # record, branch and multiplicity go with it.
                                pending.append(
                                    PendingRow(
                                        plan.t_amount[k],
                                        plan.t_content[k],
                                        plan.t_phase[k],
                                        record=plan.t_record[k],
                                        branch=plan.t_branch[k],
                                        multiplicity=plan.t_multiplicity[k],
                                        split=plan.t_record[k] != NO_RECORD,
                                        arrival=plan.t_arrival[k],
                                        offered=detector_set.sum,
                                        birth=plan.t_birth[k],
                                        hand=plan.t_hand[k],
                                    )
                                )
                            if layer is not None:
                                # A re-emitter that reads `sum` is a set that
                                # can be chosen: its rows offer there and are
                                # split again (the design's section 6). At
                                # any other re-emitter the units stay live
                                # until the split re-creates them.
                                for k in range(k0, k1):
                                    if plan.t_record[k] != NO_RECORD and detector_set.sum:
                                        layer.end(
                                            tick,
                                            layer.set_index[detector_set.index],
                                            plan.t_record[k],
                                            plan.t_branch[k],
                                            plan.t_multiplicity[k],
                                            plan.t_amount[k],
                                            plan.t_phase[k],
                                            rotation=entry_rotation(
                                                plan, detector_set, entry.label_turns[family], k
                                            ),
                                            node=(node[0], node[1], node[2]),
                                            content=plan.t_carried[k],
                                            momentum=list(plan.t_label[k]),
                                        )
                            if record is not None:
                                group_line: dict[str, object] = {
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
                                recorded_rows = taken_rows(plan, k0, k1)
                                if recorded_rows:
                                    group_line["rows"] = recorded_rows
                                    # A rotated `sum` re-emitter: the setting
                                    # and the turn of its rows (one per group:
                                    # the set's setting), as on a click.
                                    setting = entry_rotation(
                                        plan, detector_set, entry.label_turns[family], k0
                                    )
                                    if setting is not None:
                                        group_line["window"] = setting[0]
                                        group_line["turn"] = setting[1]
                                if handed:
                                    group_line["hand"] = group_hand(plan, k0, k1)
                                record(group_line)
                            continue
                        # The click: the content joins, one click per unit.
                        entry.held[family] = bounded(
                            entry.held[family] + group_content, entry, "content"
                        )
                        entry.clicks[family] += group_total
                        ledger.held_measured[family] += group_content
                        if handed:
                            # The books' `left` and `right` lines: the units
                            # clicked of each hand (a report).
                            for k in range(k0, k1):
                                if plan.t_hand[k] < 0:
                                    ledger.taken_left[family] += plan.t_amount[k]
                                elif plan.t_hand[k] > 0:
                                    ledger.taken_right[family] += plan.t_amount[k]
                        if layer is not None:
                            for k in range(k0, k1):
                                if plan.t_record[k] != NO_RECORD:
                                    layer.end(
                                        tick,
                                        layer.set_index[detector_set.index],
                                        plan.t_record[k],
                                        plan.t_branch[k],
                                        plan.t_multiplicity[k],
                                        plan.t_amount[k],
                                        plan.t_phase[k],
                                        rotation=entry_rotation(
                                            plan, detector_set, entry.label_turns[family], k
                                        ),
                                        node=(node[0], node[1], node[2]),
                                        content=plan.t_carried[k],
                                        momentum=list(plan.t_label[k]),
                                    )
                        if record is not None:
                            for k in range(k0, k1):
                                click_line: dict[str, object] = {
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
                                if window_read is not None:
                                    click_line["window"] = plan.t_window[k]
                                if plan.t_record[k] != NO_RECORD:
                                    click_line["record"] = plan.t_record[k]
                                    click_line["branch"] = plan.t_branch[k]
                                    click_line["multiplicity"] = plan.t_multiplicity[k]
                                    click_line["u"] = plan.t_birth[k]
                                    click_line["share"] = plan.t_share[k]
                                    click_line["age"] = plan.t_age[k]
                                    setting = entry_rotation(
                                        plan, detector_set, entry.label_turns[family], k
                                    )
                                    if setting is not None:
                                        click_line["window"] = setting[0]
                                        click_line["turn"] = setting[1]
                                if handed:
                                    click_line["hand"] = row_hand(plan, k, measured)
                                record(click_line)
                        # The click trigger of the transformation: the
                        # first click of a `become` entry in the interval
                        # fires it (the entry is consumed with it; the
                        # groups of the same interval admitted in bulk
                        # still click), the products born at the reader's
                        # next self-creation.
                        transformation = entry.transforms[family]
                        if rule == BECOME_RULE and transformation is not None:
                            transform(entry, transformation, "click", tick, ledger, families)
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
                    if detector_set.pointer:
                        pointer_x, pointer_y = plan.pointer[set_index]
                        value = pointer_x * pointer_x + pointer_y * pointer_y
                    else:
                        value = plan.count[set_index]
                    # Under `sum` the set's record is the layer's (one
                    # record's rows squared at its completion, below); the
                    # crowd's pointer still returns the set's phase.
                    if not detector_set.sum:
                        detector_set.record[family] += value
                    if set_phase is not None:
                        detector_set.phase[family] = set_phase
                        for member in detector_set.numbers:
                            if member in measured:
                                measured[member].phase = set_phase
                    if record is not None and not detector_set.sum:
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
                        if detector_set.pointer:
                            line["pointer"] = [pointer_x, pointer_y]
                        line["phase"] = set_phase
                        record(line)
    for family, store in enumerate(stores):
        if not keep[family].all():
            store.keep(keep[family])
    if layer is not None:
        gather_records(layer, tick, entries, measured, families, record)

    # 5. The self-creations: the releases into the store.
    numerator, denominator_release = world.release
    # Only a measured event that can release anything is visited (in number
    # order): a lamp, a holder of a free family's content, one with rows
    # pending (home, re-released or a product) or one with a clock trigger
    # of a transformation; any other would find nothing to create.
    for entry in entries:
        if not entry.creating or not (
            entry.lamp_rate is not None
            or any(free and held > 0 for free, held in zip(free_of, entry.held, strict=True))
            or any(entry.pending)
            or entry.become is not None
        ):
            continue
        age, turn = entry.clock_age, entry.turn
        # The clock trigger of the transformation, before this
        # self-creation's releases: the event's own age against the key
        # `at` by the one primitive (`ages_at_key`: the self-creation that
        # takes the clock from at - 1 to at, then every `at`), the gate
        # `crowd` open when the count the clock read this interval is
        # below it; the products are born below with age 0.
        clock_trigger = entry.become
        if (
            clock_trigger is not None
            and clock_trigger.at is not None
            and bool(ages_at_key(np.array([entry.age], dtype=np.int64), clock_trigger.at)[0])
            and (clock_trigger.crowd is None or entry.counted < clock_trigger.crowd)
        ):
            transform(entry, clock_trigger, "clock", tick, ledger, families)
        # The lamp's count at this self-creation: its rate [n, d] on its
        # accumulator, advanced at every self-creation of the lamp whether
        # or not it releases (the fraction-free law, BEAM_LAW note 41: the
        # count a self-creation of turn 0 or outside the window cannot
        # release is discarded, as the count off the clock was unread).
        lamp_count = 0
        if entry.lamp_rate is not None:
            (lamp_count,) = entry.counts.advance("lamp")
        # The release per family: every family's row of the table gains
        # `held x n` in one loop (a paid family's row has the rate 0).
        released = entry.counts.advance("release", values=entry.held)
        # The products born this self-creation (family, amount, content,
        # direction) and their recoil, for the `become` record.
        thrown_rows: list[list[object]] = []
        thrown_recoil = [0, 0, 0]
        for family, store in enumerate(stores):
            definition = families[family]
            free = free_of[family]
            # (direction, amount, content, phase, thrown, record, branch,
            # multiplicity)
            born: list[BornRow] = []
            if free and entry.held[family] > 0:
                # The release's rate is the held content: the count the
                # family's release accumulator gains (the fraction-free
                # law, BEAM_LAW note 41; the remainder below d on the
                # body's record, exact over any period of a changing
                # content; the count off the clock, `by_clock(age, held x
                # n, d)`, at a constant content from age 0).
                amount = released[family]
                if amount:
                    born.extend(
                        (
                            direction,
                            amount,
                            0,
                            entry.phase,
                            False,
                            NO_RECORD,
                            NO_BRANCH,
                            ONE_PATH,
                            0,
                            definition.hand,
                        )
                        for direction in entry.directions
                    )
            if entry.pending[family]:
                ways = len(entry.directions)
                reborn = NO_RECORD
                pending_rows = entry.pending[family]
                held_back: list[PendingRow] = []
                gate = entry.gates[family] if entry.gates else None
                if gate is not None and layer is not None:
                    # The gate between records (the design's section 10):
                    # act when rows of `parties` distinct emitters are
                    # pending here (read from the rows alone); hold
                    # otherwise, or pass them as a plain re-emission
                    # without `hold`.
                    ready = gate_ready(pending_rows, gate, entry, flight.vectors)
                    if ready is None and gate.hold:
                        continue
                    if ready is not None:
                        pending_rows, kept = apply_gate(
                            layer, tick, entry, definition.name, pending_rows, ready, record
                        )
                        if kept:
                            # The rows of records the gate did not take
                            # wait for their partners.
                            held_back = kept
                rotation = entry.rotations[family] if entry.rotations else None
                if rotation is not None:
                    pending_rows = rotate_rows(
                        pending_rows, rotation, modulus, entry, layer, record, tick
                    )
                for row in pending_rows:
                    if row.split:
                        # The split (the amplitude law, BEAM_LAW note 37): the
                        # rows (w a_i, m x A, p + t_i) on the directions, A =
                        # sum a_i^2, the norm w^2 / m exact for any integer
                        # weights; every weight 1 where none is declared;
                        # the multiplicity bounded before it is formed and
                        # refused naming the Node. A row of a record gathered
                        # at this re-emitter is born again as a new record
                        # of this emitter (`rebirth`: a new u from its own
                        # clock, its own number and ordinal, the multiplicity
                        # the split's norm; the design's section 6).
                        row_record, row_branch, row_multiplicity = (
                            row.record,
                            row.branch,
                            row.multiplicity,
                        )
                        row_birth = row.birth
                        if row.rebirth:
                            if reborn == NO_RECORD:
                                entry.births += 1
                                reborn = record_identity(entry.number, entry.births)
                                reborn_birth = (entry.births - 1) % modulus
                            row_record, row_branch, row_multiplicity = reborn, NO_BRANCH, 1
                            row_birth = reborn_birth
                        table_split = entry.splits[family]
                        if table_split is None:
                            weights, turns = (1,) * ways, (0,) * ways
                        else:
                            chosen = table_split.row(row.arrival)
                            if chosen is None:
                                raise ValueError(
                                    f"{BEAM_LAW}: a row arrived at the splitter of measured event "
                                    f"{entry.number} at {list(entry.position)} on the direction "
                                    f"{[int(v) for v in flight.vectors[row.arrival]]}, which its "
                                    "`inputs` do not name"
                                )
                            weights, turns = chosen
                        norm = sum(a * a for a in weights)
                        if row.multiplicity > MOMENTUM_BOUND // norm:
                            raise OverflowError(
                                f"{BEAM_LAW}: the multiplicity {row.multiplicity} x {norm} of a "
                                f"split at measured event {entry.number} at {list(entry.position)} "
                                f"exceeds the integer bound {MOMENTUM_BOUND}"
                            )
                        for direction, weight, turn_i in zip(
                            entry.directions, weights, turns, strict=True
                        ):
                            if not weight:
                                continue
                            if row.amount > AMOUNT_BOUND // weight:
                                raise OverflowError(
                                    f"{BEAM_LAW}: the amount {row.amount} x {weight} of a split at "
                                    f"measured event {entry.number} at {list(entry.position)} "
                                    f"exceeds the integer bound {AMOUNT_BOUND}"
                                )
                            born.append(
                                (
                                    direction,
                                    row.amount * weight,
                                    row.content,
                                    (row.phase + turn_i) % modulus,
                                    False,
                                    row_record,
                                    row_branch,
                                    row_multiplicity * norm,
                                    row_birth,
                                    row.hand,
                                )
                            )
                            ledger.content_released[family] += row.amount * weight * row.content
                        born_units = row.amount * sum(weights)
                        if layer is not None and row_record != NO_RECORD:
                            if row.rebirth:
                                # What follows a click is ONE new record with
                                # all its re-created rows: one birth per
                                # rebirth (with 0 units), every row's units
                                # added by its split.
                                if layer.resolve(row_record) is None:
                                    layer.birth(tick, row_record, family, row_birth, {0: 1}, 1, 0)
                                layer.split(row_record, 0, born_units)
                            else:
                                layer.split(row_record, 0 if row.offered else row.amount, born_units)
                        if record is not None:
                            record(
                                {
                                    "event": "split",
                                    "tick": tick,
                                    "node": list(entry.position),
                                    "measured": entry.number,
                                    "family": definition.name,
                                    "record": row_record,
                                    "branch": row_branch,
                                    "absorbed": row.amount,
                                    "born": born_units,
                                    "multiplicity": row_multiplicity * norm,
                                    "rebirth": row.rebirth,
                                    "u": row_birth,
                                }
                            )
                        continue
                    # The right-hand rule (`hand-v1`, BEAM_LAW note 39): a
                    # product born at a parent with an axis A leaves on the
                    # parent's directions on its hand's side of the axis,
                    # sign(A . u_d) = h (a left-handed product AGAINST the
                    # axis, a right-handed one along it: Wu's electrons
                    # leave against the nuclear spin; the physicist's choice
                    # (i) of record 128); a product without a hand leaves on
                    # every direction stamped sign(A . u_d), +1 along, -1
                    # against, 0 on the equator. The apportioning is today's
                    # over the admitted directions in declared order. A
                    # home, a re-emission and every birth at a parent
                    # without an axis keep the row's hand on every
                    # direction, as today (the parser refused an empty set).
                    admitted, hands_d = list(entry.directions), [row.hand] * ways
                    if row.thrown and entry.axis is not None:
                        signs = [
                            axis_sign(flight.vectors[entry.axis], flight.vectors[d])
                            for d in entry.directions
                        ]
                        if row.hand:
                            admitted = [d for d, s in zip(admitted, signs, strict=True) if s == row.hand]
                            hands_d = [row.hand] * len(admitted)
                        else:
                            hands_d = signs
                    if not admitted:
                        raise ValueError(
                            f"{BEAM_LAW}: a product of hand {row.hand:+d} at measured event "
                            f"{entry.number} at {list(entry.position)} has no direction on its side "
                            f"of the axis {[int(v) for v in flight.vectors[entry.axis or 0]]}"
                        )
                    count_d = len(admitted)
                    shares = apportion_whole(row.amount, [1] * count_d, (age + row.first) % count_d)
                    for direction, share, hand_d in zip(admitted, shares, hands_d, strict=True):
                        if share:
                            born.append(
                                (
                                    direction,
                                    share,
                                    row.content,
                                    row.phase,
                                    row.thrown,
                                    row.record,
                                    row.branch,
                                    row.multiplicity,
                                    row.birth,
                                    hand_d,
                                )
                            )
                            ledger.content_released[family] += share * row.content
                entry.pending[family] = held_back
            if (
                entry.lamp_rate is not None
                and family == entry.family
                and turn > 0
                and (
                    entry.lamp_window is None
                    or bool(
                        window_admits(
                            (entry.phase - entry.lamp_window) % modulus,
                            default_width(modulus) if entry.lamp_width is None else entry.lamp_width,
                            modulus,
                        )
                    )
                )
            ):
                cost = definition.quantum * turn
                # Under the amplitude law a lamp's release is the birth of
                # records: per self-creation as many records as the rate
                # says units per direction (`lamp_count`, the count the
                # lamp's accumulator gained above), each k rows of amount 1 on its k
                # directions with the multiplicity k, the record's identity
                # the lamp's number x 2^32 + the birth's ordinal at the
                # lamp, the birth phase of the j-th record of a
                # self-creation the clock's phase advanced by j strides
                # (the design's 2.1, the extension; stage (vii)).
                ways = len(entry.lamp_directions)
                lamp_turns = entry.lamp_turns or (0,) * ways
                if entry.held[family] // cost >= 1:
                    # The pair (the design's section 4): the joint labels
                    # with their weights (`branches`, [[0, 1]] by default)
                    # on `arms` separate quanta, the directions shared
                    # equally by the arms; per direction one row per label
                    # of amount the label's weight, the multiplicity the
                    # paths per arm times the norm (the sum of the squared
                    # weights); the row's branch packs its arm and label.
                    branches = entry.lamp_branches
                    arms = entry.lamp_arms
                    paths = ways // arms
                    norm = sum(weight * weight for _, weight in branches)
                    per_direction = sum(weight for _, weight in branches)
                    quanta = ways * per_direction
                    count = lamp_count
                    if count and entry.held[family] // cost < quanta:
                        # The birth is every label's weight on every
                        # direction: a lamp that cannot pay it would birth a
                        # record of a norm below its own, refused.
                        raise ValueError(
                            f"{BEAM_LAW}: the lamp of measured event {entry.number} at "
                            f"{list(entry.position)} holds {entry.held[family]} of "
                            f"{definition.name}, short of {per_direction} quanta ({cost} each) on "
                            f"each of its {ways} directions for the birth of a record"
                        )
                    count = min(count, entry.held[family] // (cost * quanta))
                    for _ in range(count):
                        entry.births += 1
                        record_id = record_identity(entry.number, entry.births)
                        # The birth phase: the lamp's count of births mod N
                        # (the record's own field, unread by the GameBoard),
                        # uniform over births whatever the lamp's turn.
                        u = (entry.births - 1) % modulus
                        if layer is not None:
                            layer.birth(tick, record_id, family, u, dict(branches), arms, quanta)
                        if record is not None:
                            record(
                                {
                                    "event": "birth",
                                    "tick": tick,
                                    "node": list(entry.position),
                                    "measured": entry.number,
                                    "family": definition.name,
                                    "record": record_id,
                                    "u": u,
                                    "labels": [list(pair) for pair in branches],
                                    "arms": arms,
                                    "units": quanta,
                                    "multiplicity": paths * norm,
                                }
                            )
                        for way, (direction, lamp_turn) in enumerate(
                            zip(entry.lamp_directions, lamp_turns, strict=True)
                        ):
                            lamp_arm = way // paths
                            for joint, weight in branches:
                                born.append(
                                    (
                                        direction,
                                        weight,
                                        cost,
                                        (u + lamp_turn) % modulus,
                                        False,
                                        record_id,
                                        branch_of(lamp_arm, joint),
                                        paths * norm,
                                        u,
                                        entry.lamp_hand,
                                    )
                                )
                                content = cost * weight
                                entry.held[family] -= content
                                ledger.held_spent[family] += content
                                ledger.content_released[family] += content
            if not born:
                continue
            # A body on a set of Nodes releases at every Node of the set
            # with whole units only: each born row's amount is placed whole
            # over the body's Nodes, `amount // w` at every Node and the
            # `amount mod w` units left at the Nodes whose claim is largest
            # (`place_over_nodes`: the claims are the `place` rows of the
            # body's table of counts, one per Node, the fractional share
            # each Node is owed carried from row to row and self-creation
            # to self-creation; the model owner's record 155 of 2026-09-20,
            # "no remainder discarded"; until then the leftover went to the
            # Nodes counted from `age mod w`, the tie reset at every row),
            # so that the total released is the content's release whatever
            # the width, every Node is within one unit of its equal share
            # at every row and the books balance (the shares sum to the
            # amount, every share keeps the row's content per unit and
            # phase, the labels' sum is the same recoil). A body of one Node
            # (every measured event until 2026-09-20) releases every row at
            # its one Node, unchanged.
            body = entry.nodes
            if len(body) > 1:
                ways = len(body)
                placed: list[tuple[int, BornRow]] = []
                for row_born in born:
                    shares = place_over_nodes(entry.counts, row_born[1], ways)
                    placed.extend(
                        (store.flat(node), (row_born[0], share, *row_born[2:]))
                        for node, share in zip(body, shares, strict=True)
                        if share
                    )
                node_column = np.array([b[0] for b in placed], dtype=np.int64)
                born = [b[1] for b in placed]
            else:
                node_column = np.full(len(born), store.flat(entry.position), dtype=np.int64)
            count = len(born)
            direction_column = np.array([b[0] for b in born], dtype=np.int64)
            amount_column = np.array([b[1] for b in born], dtype=np.int64)
            content_column = np.array([b[2] for b in born], dtype=np.int64)
            thrown_mask = np.array([b[4] for b in born], dtype=bool)
            # The labels of the born rows (the one label, its product checked
            # per row before it is formed, refused naming the Node and the
            # amount): a paid family's emitter takes their sum as its
            # recoil, a lamp's release and a re-emission alike; a free
            # family's emitter takes the recoil of its products alone (the
            # things thrown by a transformation; a free release is the
            # field and takes none).
            labels = momentum_labels(
                unit, direction_column, amount_column, content_column, free, entry.position
            )
            born_momentum = exact_column_sums(labels)
            if not free:
                # The recoil of a paid re-creation is the born rows' shares
                # (stage (vii) step 3: one quantum's label over a record's
                # rows), the rest of their labels off the `remainder` line;
                # the labels of rows of no record whole, as they were.
                recoil = list(born_momentum)
                born_records = [k for k, b in enumerate(born) if b[5] != NO_RECORD]
                if born_records:
                    recoil = [0, 0, 0]
                    for k, b in enumerate(born):
                        for axis in range(3):
                            label = int(labels[k, axis])
                            recoil[axis] += (
                                share_of(label, b[1], b[7])[0] if b[5] != NO_RECORD else label
                            )
                    ledger.remainder_momentum[family] = [
                        a - (whole - taken)
                        for a, whole, taken in zip(
                            ledger.remainder_momentum[family], born_momentum, recoil, strict=True
                        )
                    ]
                entry.momentum = [
                    bounded(a - b, entry, "momentum")
                    for a, b in zip(entry.momentum, recoil, strict=True)
                ]
            if thrown_mask.any():
                thrown_momentum = exact_column_sums(labels[thrown_mask])
                if free:
                    entry.momentum = [
                        bounded(a - b, entry, "momentum")
                        for a, b in zip(entry.momentum, thrown_momentum, strict=True)
                    ]
                thrown_recoil = [a - b for a, b in zip(thrown_recoil, thrown_momentum, strict=True)]
                # The `become` line's products: family, amount, content per
                # unit, the direction born on and, in a world with a hand,
                # the product's hand.
                thrown_rows.extend(
                    [
                        definition.name,
                        b[1],
                        b[2],
                        [int(v) for v in flight.vectors[b[0]]],
                        *([b[9]] if handed else []),
                    ]
                    for b in born
                    if b[4]
                )
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
                record=np.array([b[5] for b in born], dtype=np.int64),
                branch=np.array([b[6] for b in born], dtype=np.int64),
                multiplicity=np.array([b[7] for b in born], dtype=np.int64),
                birth=np.array([b[8] for b in born], dtype=np.int64),
                hand=np.array([b[9] for b in born], dtype=np.int64),
            )
            ledger.transit_released[family] += int(exact_sum(amount_column))
        # The `become` record, at the products' birth: the trigger and its
        # tick, the families, the products with their directions and the
        # recoil over them, the count the clock read at the trigger.
        if entry.transformed:
            if record is not None:
                for trigger, triggered, source, into, count_read in entry.transformed:
                    record(
                        {
                            "event": "become",
                            "tick": tick,
                            "node": list(entry.position),
                            "measured": entry.number,
                            "trigger": trigger,
                            "triggered": triggered,
                            "from": families[source].name,
                            "into": families[into].name,
                            "products": thrown_rows,
                            "recoil": thrown_recoil,
                            "counted": count_read,
                        }
                    )
            entry.transformed = []

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
            amounts,
            (store.phase[gone] - store.birth[gone]) % modulus,
            FIRST,
            tables.cosines,
            tables.sines,
        )
        ledger.lifetime_record[family] += border_x[0] * border_x[0] + border_y[0] * border_y[0]
        left = exact_column_sums(labels)
        ledger.lifetime_momentum[family] = [
            a + b for a, b in zip(ledger.lifetime_momentum[family], left, strict=True)
        ]
        ledger.transit_momentum = [a - b for a, b in zip(ledger.transit_momentum, left, strict=True)]
        if layer is not None:
            gone_x, gone_y, gone_z = store.coordinates(store.node[gone])
            for k, row_index in enumerate(gone.tolist()):
                if store.record[row_index] != NO_RECORD:
                    layer.end(
                        tick,
                        layer.border_index,
                        int(store.record[row_index]),
                        int(store.branch[row_index]),
                        int(store.multiplicity[row_index]),
                        int(store.amount[row_index]),
                        int(store.phase[row_index]),
                        node=(int(gone_x[k]), int(gone_y[k]), int(gone_z[k])),
                        content=int(store.amount[row_index] * store.content[row_index]),
                        momentum=[int(v) for v in labels[k]],
                    )
        if record is not None:
            x, y, z = store.coordinates(store.node[gone])
            for k, index in enumerate(gone):
                border_line: dict[str, object] = {
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
                if store.record[index] != NO_RECORD:
                    border_line["record"] = int(store.record[index])
                    border_line["branch"] = int(store.branch[index])
                    border_line["multiplicity"] = int(store.multiplicity[index])
                    border_line["u"] = int(store.birth[index])
                if handed:
                    border_line["hand"] = int(store.hand[index])
                record(border_line)
        keep_alive = np.ones(store.size, dtype=bool)
        keep_alive[gone] = False
        store.keep(keep_alive)

    # Merge identical rows; sort by Node. A row whose age passed the
    # world's bound refuses the run: the store's promise of fixed storage
    # is the bound, and the world must be small enough or declare it (the
    # same primitive as the border: the age against the key age_bound + 1,
    # `ages_at_key`; note 33).
    for family, store in enumerate(stores):
        # Under the amplitude key the merge is the normal form with the
        # cancel (BEAM_LAW note 37): what it removed leaves the transit
        # lines on the ledger's `cancelled` lines (the units, the content
        # carried and the labels of the units removed, per family).
        removed = store.merge(modulus)
        if removed:
            free = free_of[family]
            for (cancelled_record, direction, per_unit), amount in removed.items():
                # The units removed per (record, direction, content): the
                # content carried is amount x content, exact by the packed key
                # (no division).
                carried = amount * per_unit
                if layer is not None:
                    layer.cancel(cancelled_record, amount)
                if record is not None:
                    record(
                        {
                            "event": "cancel",
                            "tick": tick,
                            "family": families[family].name,
                            "record": cancelled_record,
                            "direction": [int(v) for v in flight.vectors[direction]],
                            "amount": amount,
                            "content": carried,
                        }
                    )
                ledger.cancelled_amount[family] += amount
                ledger.cancelled_content[family] += carried
                label = momentum_labels(
                    unit,
                    np.array([direction], dtype=np.int64),
                    np.array([amount], dtype=np.int64),
                    np.array([per_unit], dtype=np.int64),
                    free,
                )[0].tolist()
                ledger.cancelled_momentum[family] = [
                    a + b for a, b in zip(ledger.cancelled_momentum[family], label, strict=True)
                ]
                ledger.transit_momentum = [
                    a - b for a, b in zip(ledger.transit_momentum, label, strict=True)
                ]
        if store.size and ages_at_key(store.age, world.age_bound + 1).any():
            raise OverflowError(
                f"{BEAM_LAW}: a ray carries the age {int(store.age.max())} beyond the world's "
                f"age_bound {world.age_bound} (declare a larger age_bound or a smaller GameBoard)"
            )
    if layer is not None:
        gather_records(layer, tick, entries, measured, families, record)
    return readings


def gather_records(
    layer: Layer,
    tick: int,
    entries: list[Measured],
    measured: dict[int, Measured],
    families: tuple[FamilyDefinition, ...],
    record: Record | None,
) -> None:
    """The layer's completions (the ladder, the world's row): every record
    whose units all ended; the `gather` line, per `sum` set with an offer
    of the record the set's record (the square of the record's pointer per
    label, accumulated) with a `record` line, and the pending rows of the
    record at a chosen re-emitter marked for their rebirth as a new
    record."""
    for live in layer.complete(tick):
        identity, family = live.identity, live.family
        gather = live.gather
        assert gather is not None
        for (set_index, arm), offer in sorted(live.offers.items()):
            key = layer.keys[set_index]
            if key[0] != "set" or offer.read:
                continue
            detector_set = layer.sets[key[1]]
            if not detector_set.sum:
                continue
            for label, (x, y) in sorted(offer.pointers.items()):
                square = x * x + y * y
                detector_set.record[family] += square
                if record is not None:
                    record(
                        {
                            "event": "record",
                            "tick": tick,
                            "detector": layer.names[set_index],
                            "family": families[family].name,
                            "reading": "sum",
                            "scope": detector_set.scope,
                            "of": identity,
                            "arm": arm,
                            "label": label,
                            "pointer": [x, y],
                            "record": square,
                            "multiplicity": offer.multiplicity,
                        }
                    )
        chosen = gather["chosen"]
        if isinstance(chosen, list):
            for name, _, _ in chosen:
                set_index = layer.names.index(str(name))
                key = layer.keys[set_index]
                if key[0] != "set":
                    continue
                for number in layer.sets[key[1]].numbers:
                    holder = measured.get(number)
                    if holder is None:
                        continue
                    for pending in holder.pending:
                        for k, row in enumerate(pending):
                            if row.record == identity and row.split:
                                pending[k] = row._replace(rebirth=True)
        if record is not None:
            record(dict(gather))
