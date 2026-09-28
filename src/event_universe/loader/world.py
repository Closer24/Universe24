"""The world file translated to the loop's classes: the frame (loader/frame.py) reads the three files through the schemas and hands the checked values here; this module builds the loop's classes from them (NatureBeamWorld, FamilyDefinition, MeasuredDefinition, BlockDefinition, EmitterDefinition, DetectorDefinition, TwistTable), keeps the rules between keys the cards do not state, and runs the loop's load-time checks (the node clock's bound, the held bodies, the initial state, the body's fit); it leaves with the loop's reads of the old form's keys (ALGEBRA.md #the-primitives.90 (1))."""

from __future__ import annotations

import math
from collections.abc import Mapping, Sequence
from dataclasses import dataclass, field
from typing import cast

from event_universe.core.game_board import MAX_VALUE, Address3
from event_universe.core.integer import MAX_WORK_INT
from event_universe.core.readings import Reading, world_readings
from event_universe.core.register import discover
from event_universe.core.rule3 import ISOTROPIC, coefficients, division_forward
from event_universe.core.schema import Context
from event_universe.core.step import STEP_FILE, Step
from event_universe.loader import derived, frame
from event_universe.loader.frame import EngineStart
from event_universe.loader.mode import Levels, moving_levels, period_by_the_rule

# the ray law's table rules, read by the loop's fixed values alone (DEAD, the paper writer's)
TABLES = ("read", "measure", "rerelease", "pass", "become")
# the readings a record may carry (the loop's words)
AGE_READS = "age"
PRESENCE_WORD = "presence"
READS = ("scalar", "outside", "here", "vector", "tensor", AGE_READS, PRESENCE_WORD)
# the bounds of an amount, a norm and a momentum component, from the one width of the work register
AMOUNT_BOUND = MAX_WORK_INT // 2
NORM_BOUND = (MAX_WORK_INT + 1) ** 2 - 1
MOMENTUM_BOUND = MAX_WORK_INT // 2
Vector = tuple[int, int, int]


# the ceiling of a row's amplitude is the width's (the rule's total and the transport's room bound it below); the rule's int64 total
AMPLITUDE_BOUND = MAX_WORK_INT
TOTAL_BOUND = MAX_WORK_INT + 1
# light's kind: the pair [1, 1], the value every family without a declared pair reads (no branch on a name)
MASSLESS_PAIR = (1, 1)
# a body of one Node
ONE_NODE: tuple[int, int, int] = (1, 1, 1)
# the border's name no detector may take
LIFETIME_NAME = "lifetime"
# the charge per unit of content of a family with none: 0 as the pair [0, 1]
NO_CHARGE = (0, 1)
# the three forms of a family's parts (ALGEBRA.md #the-primitives)
PARTS_FORMS = ((1,), (1, 3), (1, 3, 6))


@dataclass(frozen=True)
class TwistTable:
    """THE TWIST TABLE as read (ALGEBRA.md #the-transport, #the-primitives): the unit's
    integer as the file gives it (theta_unit = 1 / unit radians), the fine triples for
    k_0 in [0, F) with F the fine table's length, a power of two, and the coarse triples
    for k_1 in [0, bound); the transport's triple for |k| = k_1 F + k_0 is their exact product."""

    unit: int
    fine: tuple[tuple[int, int, int], ...]
    coarse: tuple[tuple[int, int, int], ...]
    fine_bits: int  # the fine table's size as a power of two: |k| = k_1 2^fine_bits + k_0


def _twist_table(value: object, label: str, amplitude_bound: int | None) -> TwistTable:
    """The twist table read and checked in integers (ALGEBRA.md #the-primitives): {unit, fine, coarse},
    the unit an integer from 1 as the file gives it (theta_unit = 1 / unit radians per unit of k) and
    the fine table's length F a power of two (|k| = k_1 F + k_0), no number of the loader's own; the
    coarse from 1; each triple three integers, c from 1, s from 0, d from 1 with c^2 + s^2 = d^2, the
    first the angle 0's and the angles never falling along the table (the nearest triple of each angle
    is the generator's number, checked by its own test); the product of the largest d of each part
    times 3 (A + 1) inside the width (the transport's total), which bounds every d and the coarse count."""
    obj = _object(value, label, {"unit", "fine", "coarse"}, {"unit", "fine", "coarse"})
    if amplitude_bound is None:
        raise ValueError(f"{label}: a world with a twist table declares `amplitude_bound`")
    unit = _integer(obj["unit"], f"{label}.unit", 1)
    parts: list[tuple[tuple[int, int, int], ...]] = []
    for name in ("fine", "coarse"):
        rows = obj[name]
        if not isinstance(rows, list | tuple) or not rows:
            raise ValueError(
                f"{label}.{name} must be a list of triples [c, s, d] (ALGEBRA.md #the-primitives)"
            )
        if name == "fine" and len(rows) & (len(rows) - 1):
            raise ValueError(
                f"{label}.fine holds {len(rows)} triples, not a power of two: |k| = k_1 F + k_0 with F "
                "the fine table's length (ALGEBRA.md #the-primitives)"
            )
        triples: list[tuple[int, int, int]] = []
        for index, row in enumerate(rows):
            where = f"{label}.{name}[{index}]"
            if (
                not isinstance(row, list | tuple)
                or len(row) != 3
                or any(type(item) is not int for item in row)
            ):
                raise ValueError(f"{where} must be three integers [c, s, d]")
            c, s, d = (int(item) for item in row)
            if c < 1 or s < 0 or d < 1 or c * c + s * s != d * d:
                raise ValueError(
                    f"{where} [{c}, {s}, {d}] is no triple of the table: c from 1, s from 0, "
                    "d from 1, c^2 + s^2 = d^2 exactly (ALGEBRA.md #the-transport)"
                )
            if index == 0 and (c, s, d) != (1, 0, 1):
                raise ValueError(f"{where} [{c}, {s}, {d}] is not the angle 0's triple [1, 0, 1]")
            if triples and s * triples[-1][0] < triples[-1][1] * c:
                # the angles in order: tan (s / c) never falls from one entry to the next (the nearest-triple property is the generator's, checked by its own test)
                raise ValueError(
                    f"{where} [{c}, {s}, {d}] turns back below the entry before it: the table's "
                    "angles rise with k (ALGEBRA.md #the-primitives; the generator writes the "
                    "nearest triples, the loader checks the identities, the bound and the order)"
                )
            triples.append((c, s, d))
        parts.append(tuple(triples))
    room = 3 * max(d for _, _, d in parts[0]) * max(d for _, _, d in parts[1]) * (amplitude_bound + 1)
    if room >= TOTAL_BOUND:
        raise ValueError(
            f"{label}: the transport's total at A = {amplitude_bound}, {room}, leaves int64 "
            "(3 d_1 d_0 (A + 1) below 2^63; ALGEBRA.md #the-transport)"
        )
    return TwistTable(unit, parts[0], parts[1], len(parts[0]).bit_length() - 1)


def _require_under_law(obj: dict[str, object], label: str, keys: set[str]) -> None:
    """NO DEFAULT (record 2089): every key the engine or
    the loader reads is declared; a missing one is refused by name."""
    missing = keys - set(obj)
    if missing:
        raise ValueError(
            f"{label} lacks keys the engine reads: "
            f"{', '.join(sorted(missing))} (no default; the model owner's record 2089)"
        )


def _refuse_under_law(obj: dict[str, object], label: str, keys: set[str]) -> None:
    """A key the engine never reads is refused by name: a flag the engine does not need is deleted, not defaulted."""
    present = [key for key in sorted(keys) if key in obj]
    if present:
        raise ValueError(
            f"{label} declares {', '.join(present)}, which the engine never reads "
            "(refused by name; the model owner's records 2089 and 2094)"
        )


STAMP_KEYS = {"hash"}
BLOCK_KEYS = {
    "side",
    # the box's extents per axis in place of `side` (the slabs of ALGEBRA.md #a-familys-declaration; BUILD.md section 26 item 23)
    "extents",
    "pair",
    # THE BODY'S KIND (ALGEBRA.md #the-primitives, #the-interval; the one stroke, commit 1): the body's rest pair on a family whose pair is the body's
    "kind",
    # THE BODY'S NUMBERS the holds read (ALGEBRA.md #the-interval; commit 2): its charge Q (`q`), its spin S and its moment mu (the momentum n is `momentum`)
    "spin",
    "moment",
    # the body's own record's twist "own", the generator's integer (item 73)
    "twist",
    "seed",
    # the bound mode's clock [a, b] beside a profile (ALGEBRA.md #a-familys-declaration)
    "clock",
    # the moving body's Node's proper pairs by the momentum's whole part (ALGEBRA.md
    # ALGEBRA.md #the-velocity; BUILD.md section 26 item 46), beside `clock` on a moving block
    "proper_clock",
    "ramp",
    "start",
    "margin",
    # the emitter as a clicking body (ALGEBRA.md #the-click; LAB_TOOLS.md A.1):
    # the excited records in turn on the body's Nodes, each clicking at its own rung, the given record written once by E^T at that interval
    "emitter",
    # detector-law-v1, the receiver by name (DECLARATIONS.md section 13 item
    # 7): an emitting block names the detector set whose one detector is its record's ladder; admitted on an emitting block alone
    "receiver",
    # the stock of the body's own family where its emitter gives it (ALGEBRA.md #the-primitives; commit 6)
    "stock",
}
# a well's margin kind, the loader's rule between keys: a pin world's margins or a control world's
MARGIN_KINDS = ("pin", "control")
# the detector's readings, the loop's words; the first is every detector's (the key is gone)
DETECTOR_READINGS = ("wave", "beam")
# the face detectors' names in Port order, and the prefix of a body's own set; a declared detector takes neither
FACE_NAMES = ("face:+x", "face:-x", "face:+y", "face:-y", "face:+z", "face:-z")
RESERVED_SET_PREFIX = "measured:"
# the GameBoard's axes and the words of a face: open, periodic, or closed (a zero face without the take)
AXES = ("x", "y", "z")
BOUNDARIES = ("open", "periodic")
CLOSED_FACE = "closed"


@dataclass(frozen=True)
class FamilyDefinition:
    """One family of the world as the universe file declares it: its name, its quantum (the content of one unit
    per phase step of a giving), its charge sign, its lifetime L (None for ever) and its hand (the click's sign
    check, None for none), its clock, its pair and what it is (`held`, `reads`, `parts`), read as attributes alone."""

    name: str
    quantum: int
    charge: tuple[int, int] = NO_CHARGE
    lifetime: int | None = None
    hand: int | None = None
    phase_per_age: tuple[int, int] | None = None
    # The record kind's pair [num, den] on the six-neighbour term of the local detector law's rule
    # (`massive-record-v1`, MASSIVE_RECORD.md section 1): light's kind is the value (1, 1) (every family without the key `pair`); a massive kind declares den > num, its rest
    # frequency cos omega_0 = num / den.
    pair: tuple[int, int] = MASSLESS_PAIR
    # THE FAMILY GENERICITY (record 2066; item 53): what a family IS is declared here and read by the engine as
    # attributes alone, never by a name or a role: `held`, the source a body writes at its Nodes ("content" its
    # quanta, "sign" the signed sum of them by the rows' signs); `reads`, the held families whose levels enter its
    # pace, (family index, weight, by) each, by "plain" or "sign"; `components`, the representation's count.
    held: str | None = None
    reads: tuple[tuple[int, int, str, int | str], ...] = ()
    # THE REPRESENTATION AS A LIST OF PARTS (ALGEBRA.md #the-primitives, #the-interval
    # (1); the one stroke, commit 1): (1,) a scalar, (1, 3) the time part and
    # the vector, (1, 3, 6) the symmetric tensor over the four directions; the
    # component order fixed once, (t), (x, y, z), (xx, yy, zz, xy, xz, yz)
    parts: tuple[int, ...] = (1,)
    # the levels at a Node (ALGEBRA.md #the-interval): 1 the pair (a_now, a_before, r); 2 the
    # two levels with their remainders (the second level not yet allocated:
    # it enters with the transport, commit 4)
    levels: int = 2
    # THE HELD SOURCE'S WRITES (ALGEBRA.md #the-interval): the factor per part (gravity (1, 4, 2): s,
    # 4 s n div W, 2 s n n div W^2; the charge (1, 1)), the body's dipole number written on the
    # six neighbours ("spin", "moment") and its divisor; one factor per part, (1,) on a scalar
    held_factors: tuple[int, ...] = (1,)
    held_dipole: str | None = None
    held_dipole_div: int = 1
    # THE SUM'S DIVISOR E_s (the owner's word of 21:35Z): the body's count enters the held line over it; the row's key
    held_divisor: int | None = None
    # THE SPIN'S STEP'S ROW (ALGEBRA.md #a-familys-declaration): the curl and tidal pairs, read by the spin's step's
    # folder; required on a family that holds the spin's dipole, None on every other
    spin_weights: tuple[tuple[int, int], tuple[int, int]] | None = None
    # THE SOURCE (9.117 row "the source"): the target family by index, the signed weight, the
    # scale and the cap or None; the loop builds the source's term from it (Main Loop, #1236)
    sourced: tuple[int, int, int, int | None] | None = None
    # the self-source's unit P_2 (ALGEBRA.md #a-familys-declaration, #the-interval): 0, off
    self_unit: int = 0
    # THE CLICKS (ALGEBRA.md #a-familys-declaration, #the-interval): (gives, takes) for a family of records,
    # None for a field family that is never given or taken
    clicks: tuple[bool, bool] | None = None
    # THE PAIR ON THE BODY (ALGEBRA.md #the-primitives, #the-interval): the family declares no pair
    # of its own; every body and every given record of it declares its own
    # (`kind` on the body, `pair` on the emitter); `pair` then a placeholder
    pair_on_body: bool = False

    @property
    def booked(self) -> bool:
        """The detectors book the family's records at their Ports: exactly a
        family with clicks (derived, item 53; ALGEBRA.md #the-interval)."""
        return self.clicks is not None

    @property
    def components(self) -> int:
        """The count of components, the parts summed (ALGEBRA.md #the-interval)."""
        return sum(self.parts)

    @property
    def massive_kind(self) -> bool:
        """A family of the massive record kind: its pair has den > num (a
        gap), or its bodies declare their pairs; light's kind reads den =
        num."""
        return self.pair_on_body or self.pair[1] > self.pair[0]


@dataclass(frozen=True)
class EmitterDefinition:
    """The giving of a clicking body (ALGEBRA.md #the-click, #the-primitives): the given family (its row's
    `clock` [p, q] the given record's clock), the given record's pair, the period P_body by the one-Node
    rule from the body's own mode's clock pair, the norm T (the generator's integer), the ladder by name,
    the weight g of the window and the twist "own" the body's; none of them a key of the emitter but the
    given family, the weight, the norm and its denominator, the receiver and (where the family has none) the pair."""

    family: int
    branches: tuple[tuple[int, int], ...]
    label_hands: tuple[int, int] | None
    receiver: tuple[str, ...] | None
    # THE GIVEN CLOCK: the given record's clock [p, q], [2 N, lambda_q] of the mode's `wavelength`, or the row's for a mode file without one
    clock: tuple[int, int]
    # THE GIVEN RECORD'S PAIR (ALGEBRA.md #the-primitives; commit 1): the given family's, or the emitter's own `pair` on a family whose pair is the body's
    pair: tuple[int, int] = MASSLESS_PAIR
    period: int | None = None
    norm: int | None = None
    given: None = None  # the ray law's given train, read by the loop as None (its cancelled branch)
    # THE POINT EMITTER'S NORM DENOMINATOR (ALGEBRA.md; item 50): T the exact rational norm / norm_denominator in the form's units, the window's outward norm read against it; required on every emitter (commit 7)
    norm_denominator: int | None = None
    # THE POINT EMITTER'S WEIGHT g (ALGEBRA.md; item 50): the body's coupling to the given family, one integer, the body's Node's
    # rotation copied at that weight into the given row at the body's Node every interval of the window; required on every emitter (commit 7)
    weight: int | None = None
    # THE GIVEN RECORD'S COMPONENT (ALGEBRA.md #the-second-level, #the-interval; commit 4): the
    # index in the given family's parts, 0 on a scalar family, 1 + the axis of the
    # body's moment on a vector family (the component along mu)
    part: int = 0
    # THE GIVEN RECORD'S TWIST "OWN" (ALGEBRA.md #the-primitives; commit 4): round(2^16 omega_0), the giver's
    twist: int = 0
    # THE QUANTUM'S WAVE NUMBER k_q in the twist's unit (the recoil's row): the mode's reading `wave_number`; None off the mode, no recoil
    wave_number: int | None = None


@dataclass(frozen=True)
class BlockDefinition:
    """A body: its Nodes (the box of `extents` at the measured event's position, or its declared `nodes`
    with their `counts` in the law's form), its pair and its kind (its rest pair), the `seed` of its own
    record at interval 0 (an amplitude, or the amplitude of its mode's `profile` over the whole board with
    the mode's `clock`), its momentum's drive (`ramp`, `start`), its charge, spin and moment, its twist, its
    margin kind, its receiver, its emitter, its stock and the keys the cards declare (`declared`)."""

    side: int
    pair: tuple[int, int]
    # THE BODY'S KIND (ALGEBRA.md #the-primitives, #the-interval): the rest pair of the body's own record, its family's declared pair or, on a family whose pair is the body's, the body's own `kind`
    kind: tuple[int, int]
    seed: int  # the well's own record's amplitude on its Nodes at interval 0 (0 silent), or its profile's; declared in the file, no default (the model owner, 2026-09-25; BUILD.md section 26 item 28)
    spin: tuple[int, int, int]
    spin_before: tuple[int, int, int]
    # the box's extents per axis (x, y, z); a cube's (side, side, side), `side` its x extent
    extents: tuple[int, int, int] = (1, 1, 1)
    # the bound mode's integer profile over the whole board (x-major, one per Node) when the seed is declared so; None for a flat seed
    profile: tuple[int, ...] | None = None
    # THE MODE'S CLOCK (ALGEBRA.md #a-familys-declaration; record 1886): 2 cos omega of the
    # body's bound mode as the rational [a, b] the generator wrote, b at
    # least the profile's amplitude; the loader's integer check of the profile against the eigen-equation reads it; None for a flat seed
    clock: tuple[int, int] | None = None
    # the proper pairs of a moving body on one Node by the momentum's whole part, today's form (ALGEBRA.md #the-velocity)
    proper_clock: tuple[tuple[int, int], ...] | None = None
    # a moving body's two levels from the mode file, now and before (ALGEBRA.md #the-generator (e)); None on a body at rest
    levels: Levels | None = None
    ramp: int = 0
    start: int = 0
    # THE BODY'S NUMBERS (ALGEBRA.md #the-interval; the one stroke, commit 2): the
    # signed number q (the held sign's count at its Nodes; the world's word `q`,
    # record 2128 (1)), the spin S and the moment mu (the dipoles on its Node's six neighbours); the momentum n is `momentum`
    q: int = 0
    moment: tuple[int, int, int] = (0, 0, 0)
    # THE BODY'S OWN RECORD'S TWIST "OWN" (ALGEBRA.md #the-primitives; commit 4): round(2^16
    # omega_0), its rotation from its mode's clock [a, b] (2 cos omega) where it has one, else from its kind's pair
    twist: int = 0
    # a well's margin kind (required on a well, record 2089); None on a body that is no well
    margin: str | None = None
    # the receiver by name: the detector set whose one detector is the ladder of every record this block emits; None where the world names none
    receiver: str | None = None
    # the emitter as a clicking body (ALGEBRA.md #the-click): None on a body that emits nothing by the click
    emitter: EmitterDefinition | None = None
    # THE STOCK OF THE BODY'S OWN FAMILY (ALGEBRA.md #the-primitives; commit 6): the count of
    # its own quanta set aside for giving where its emitter gives its own family, 0 elsewhere (another family's stock is the body's `held` quanta of it)
    stock: int = 0
    # A BODY IN THE LAW'S FORM (ALGEBRA.md #what-a-body-is): its Nodes as declared, in the file's
    # order, and the count at each (the family of clicks' level there); None on a body by its position
    nodes: tuple[Address3, ...] | None = None
    counts: tuple[int, ...] | None = None
    # a moving body's phase denominator m, the pair (m, j) of its phase per Link (ALGEBRA.md #the-generator (e))
    phase_denominator: int | None = None
    # THE KEYS THE CARDS DECLARE AT A BODY, as the frame checked them (loader/frame.py `counted_kind`): the
    # loop's hooks read each through its card's own reader; the loader names none (ALGEBRA.md #the-primitives)
    declared: Mapping[str, object] = field(default_factory=dict)


@dataclass(frozen=True)
class MeasuredDefinition:
    """One measured event as declared: its position, its family, its amount, its momentum at two levels, its
    `span` (the Nodes it is a body on), `held` (the content per family at the start, its amount under its own
    family and its stocks) and its block (its body); the ray law's table, windows, reads and lamp are inert."""

    position: Address3
    family: int
    amount: int
    phase: int
    momentum: Vector
    momentum_before: Vector
    table: tuple[str, ...]
    windows: tuple[int | None, ...]
    reads: tuple[str, ...]
    span: tuple[int, int, int] = ONE_NODE
    phase_by_momentum: bool = False
    held: tuple[int, ...] = ()
    # the ray law's splits and lamp, read by the loop as None (its cancelled branches)
    splits: tuple[None, ...] = ()
    lamp: None = None
    # The block (massive-record-v1): the measured event's Nodes, pair,
    # seed and the rest, or None (a body of one Node or a span as before).
    block: BlockDefinition | None = None


@dataclass(frozen=True)
class DetectorDefinition:
    """A named set of measured events, its threshold and its reading
    (`beam` or `wave`): ONE DETECTOR, one cube of side DETECTOR_SIDE or
    more (record 1899), whose click is the detector's and never a Node's;
    under the local detector law a set may instead be BOUND TO A BLOCK
    (`block`, the measured event's number): its Nodes are the block's Nodes
    at every interval (a stepping block's follow it) or a cube of free
    Nodes beside it, its pointer the one-way flux into them; the click
    stamps the block's own count. The rung's wheel is the record's own
    (ALGEBRA.md #a-familys-declaration): a set declares none."""

    name: str
    positions: tuple[Address3, ...]
    threshold: int
    reading: str = DETECTOR_READINGS[0]
    block: int | None = None


@dataclass(frozen=True)
class NatureBeamWorld:
    """A parsed world of the engine (no law's name, no `model_id`: ALGEBRA.md #the-primitives). `boundary` is the declared value
    as the record carries it (the string `"open"` or the object per axis);
    `periodic` says per axis (x, y, z) whether the walk wraps; `directions`
    is the table `D`: the two rest vectors, the six headings and the declared
    rest; `action` is h, the quantum of action of the turn by momentum, or
    None when the world declares none."""

    shape: Address3
    boundary: str | dict[str, str]
    periodic: tuple[bool, bool, bool]
    ticks: int
    phase_steps: int
    families: tuple[FamilyDefinition, ...]
    measured: tuple[MeasuredDefinition, ...]
    detectors: tuple[DetectorDefinition, ...]
    readings: tuple[Reading, ...]
    step: Step
    # the face receiver's depth at every open border (ALGEBRA.md #the-ladder),
    # declared in the file under the detector law (no default, BUILD.md
    # section 26 item 28); 0 on a GameBoard with no open face (no slab)
    face_depth: int = 0
    # massive-record-v1: the probes, Nodes whose light amplitude is written
    # per interval (GAMEBOARD), empty by default.
    probes: tuple[Address3, ...] = ()
    mode_axis: int | None = None
    # detector-law-v1: per axis, whether the face is declared "closed" (a
    # zero face for light with no take); never on a periodic axis.
    closed: tuple[bool, bool, bool] = (False, False, False)
    # massive-record-v1: the world key `amplitude_bound`, the amplitude A
    # every row stays below (declared on a massive world; the ceiling 2^28
    # under the Node clock, BUILD.md section 26 item 31, on a world without
    # the kind, where no row is bounded so).
    amplitude_bound: int = AMPLITUDE_BOUND
    # THE NODE CLOCK (ALGEBRA.md #the-paces; BUILD.md section 26 item 31):
    # Gamma, the world key `node_clock`, the clock pair (Gamma, Gamma + M) at
    # every Node; required under the detector law, 0 on a world without it
    # (the ray law has no rule with a division).
    node_clock: int = 0
    # THE MOMENTUM'S UNIT Q (ALGEBRA.md #the-primitives, #the-well): the universe's
    # integer `momentum_unit`; every body's wall is W = 3 Q M with M its quanta,
    # its velocity n / W Links per interval; required under the detector law,
    # 0 on a world without it
    momentum_unit: int = 0
    # THE QUANTUM'S ACTION T (ALGEBRA.md #a-familys-declaration; the owner's word of 2026-09-28): the
    # universe's integer `quantum_action`, one T for every family; read where declared, 0 where it is not
    quantum_action: int = 0
    # THE TWIST TABLE (ALGEBRA.md #the-transport, #the-primitives; commit 4): the exact
    # triples of the transport's angles, None on a world without one (no transport)
    twist_table: TwistTable | None = None
    # THE ENGINE START FILE (record 2089; BUILD.md section 26 item 57): the
    # world's `engine` as read, None on a world without the detector law
    start: EngineStart | None = None
    # THE ONE FAMILIES FILE (item 59): the world's `families` as a repository
    # path, None when the world lists its families inline
    universe_file: str | None = None

    @property
    def recorded(self) -> bool:
        """Whether a row of this world can carry a record: a lamp is
        declared (a record is given by a lamp, a rebirth follows a lamp's
        record; the amplitude law, the one click of stage (vii)). The
        record's columns, the books' `cancelled` and `remainder` lines and
        the identity `amplitude-v1` belong to a recorded world alone, so
        that a world without a lamp reads as it did before the law."""
        return any(entry.lamp is not None for entry in self.measured)

    @property
    def phase_mask(self) -> int:
        """The mask of the phase circle, N - 1."""
        return self.phase_steps - 1

    @property
    def hypotheses(self) -> list[str]:
        """CANCELLED (ALGEBRA.md #the-primitives): the identities of the physical hypotheses a world of the ray law
        declared beside it, an empty list on every world (one engine, no identity)."""
        # ONE ENGINE (ALGEBRA.md #the-primitives; docs/CANCELLED_WORLDS.md section 9): no
        # identity stands beside the engine; the ray law's identities this property
        # listed (bohr, columns, weak, meeting, amplitude, massive-rows, hand,
        # covariant-readings, drive-b, flow-link, centred-step, atom-level, binding)
        # are CANCELLED and never appended
        return []

    @property
    def held_families(self) -> tuple[int, ...]:
        """THE FAMILY GENERICITY (record 2066; item 51): the indices of the
        families with a held source, in the declared order (the engine's one
        list of held records)."""
        return tuple(index for index, family in enumerate(self.families) if family.held is not None)

    def kind_periodic(self, family: int) -> tuple[bool, bool, bool]:
        """The faces a family's rows read, per axis: the world's `boundary`,
        ONE BORDER FOR EVERY FAMILY (the model owner's rule through the Boss,
        2026-09-25; BUILD.md section 26 item 28); a family's own `faces`
        (`massive-record-v1`, HISTORY) is refused at load, so every family
        reads the same border."""
        if not 0 <= family < len(self.families):
            raise ValueError(f"no family {family} on this world")
        return self.periodic

    @property
    def boundary_per_axis(self) -> dict[str, str]:
        """The GameBoard's faces per axis, `x`, `y`, `z` to `open`, `periodic` or `closed`."""
        return {
            axis: BOUNDARIES[1] if wraps else (CLOSED_FACE if shut else BOUNDARIES[0])
            for axis, wraps, shut in zip(AXES, self.periodic, self.closed, strict=True)
        }

    def detector_of(self, position: Address3) -> int | None:
        """The index of the detector a Node belongs to, if any."""
        for index, detector in enumerate(self.detectors):
            if position in detector.positions:
                return index
        return None


def _object(value: object, label: str, allowed: set[str], required: set[str]) -> dict[str, object]:
    if not isinstance(value, dict):
        raise ValueError(f"{label} must be a JSON object")
    unknown = set(value) - allowed
    if unknown:
        raise ValueError(f"{label} has unknown keys: {', '.join(sorted(unknown))}")
    missing = required - set(value)
    if missing:
        raise ValueError(f"{label} lacks keys: {', '.join(sorted(missing))}")
    return {str(key): item for key, item in value.items()}


def _integer(value: object, label: str, minimum: int, maximum: int = AMOUNT_BOUND) -> int:
    if type(value) is not int or value < minimum or value > maximum:
        raise ValueError(f"{label} must be an integer from {minimum} through {maximum}")
    return value


def _ratio(value: object, label: str, zero: bool) -> tuple[int, int]:
    """A rate n / d as `[n, d]` (n from 0 with `zero`, d positive) or one integer."""
    if type(value) is int:
        return _integer(value, label, 0 if zero else 1), 1
    if not isinstance(value, list | tuple) or len(value) != 2:
        raise ValueError(f"{label} must be an integer or [numerator, denominator]")
    numerator = _integer(value[0], f"{label} numerator", 0 if zero else 1)
    denominator = _integer(value[1], f"{label} denominator", 1)
    return numerator, denominator


def _address(value: object, label: str, shape: Address3) -> Address3:
    if not isinstance(value, list | tuple) or len(value) != 3:
        raise ValueError(f"{label} must be three integers")
    components: list[int] = []
    for item, extent in zip(value, shape, strict=True):
        if type(item) is not int or item < 0 or item >= extent:
            raise ValueError(
                f"{label} components must be integers on the GameBoard, from 0 "
                f"through the extent less one on each axis of the shape {list(shape)}"
            )
        components.append(item)
    return components[0], components[1], components[2]


def body_nodes(
    position: Address3,
    span: tuple[int, int, int],
    shape: Address3,
    periodic: tuple[bool, bool, bool],
) -> tuple[Address3, ...] | None:
    """The set of Nodes a measured event of `span` is a body on: the block
    of span_x x span_y x span_z Nodes centred on `position` (each span odd,
    the offsets -(s - 1) / 2 .. (s - 1) / 2 per axis), in the fixed order
    of the offsets (x, then y, then z, ascending; the order the releases
    are apportioned in). On a periodic axis an offset wraps; on an open
    axis a Node beyond the face means the body has left the GameBoard and the
    result is None (the whole body clicks on the face detector). A span
    of (1, 1, 1) is the one Node `position`."""
    axes: list[list[int]] = []
    for axis in range(3):
        half = (span[axis] - 1) // 2
        coordinates = []
        for offset in range(-half, half + 1):
            coordinate = position[axis] + offset
            if periodic[axis]:
                coordinate %= shape[axis]
            elif not 0 <= coordinate < shape[axis]:
                return None
            coordinates.append(coordinate)
        axes.append(coordinates)
    return tuple((x, y, z) for x in axes[0] for y in axes[1] for z in axes[2])


def _boundary(value: object) -> tuple[str | dict[str, str], tuple[bool, bool, bool]]:
    """The GameBoard's faces: `"open"` on every face, or an object with the three
    keys `x`, `y`, `z`, each `"open"`, `"periodic"` or `"closed"`, every axis
    declared (no default). Returns the value as declared (what the record carries)
    and, per axis, whether the walk wraps. Every other word is refused."""
    if value == BOUNDARIES[0]:
        return BOUNDARIES[0], (False, False, False)
    if (
        isinstance(value, dict)
        and set(value) == set(AXES)
        and all(item in BOUNDARIES or item == CLOSED_FACE for item in value.values())
    ):
        declared = {str(key): str(item) for key, item in value.items()}
        wraps = tuple(declared[axis] == BOUNDARIES[1] for axis in AXES)
        return declared, (wraps[0], wraps[1], wraps[2])
    raise ValueError(
        "the GameBoard is open (its edge is infinity) unless an axis is declared "
        'periodic (boundary "open" or an object of "x", "y", "z" to "open" or "periodic", or '
        '"closed" per axis: a zero face without the take); '
        "a closed GameBoard is refused (the string, and any other word)"
    )


def load_level(
    reads: Sequence[Sequence[tuple[int, int]]],
    sources: Sequence[Sequence[int]],
    node_clock: int | None = None,
) -> int:
    """The content the load bound is read at, the loader's and the generator's one function (ALGEBRA.md #the-counts-line, "The bound"): twice the whole content a family reads, the sum over every body of its reads' weights times the body's source for the read family (`reads` per family its (family, weight) pairs, `sources` per body its source per family), the largest over the families; with the Node clock, at most Gamma - 1 (the level a Node can read, the pace positive; a wave off a zero face doubles), the level the generator derives its amplitude unit at so that its profile stands inside the universe's bound."""
    reach = max(
        (2 * sum(w * body[o] for o, w in family for body in sources) for family in reads), default=0
    )
    return reach if node_clock is None else min(reach, node_clock - 1)


def derived_amplitude(entries: Sequence[object], bodies: object, node_clock: int) -> int:
    """THE AMPLITUDE BOUND A, DERIVED AND NEVER WRITTEN (ALGEBRA.md #a-familys-declaration, #the-line, #the-rows-against-nature; the owner's word of 2026-09-28: a level beyond the integer width is the engine's refusal): the largest level at which the rule's total 6 A R + A |S| + w (A + 1) stays inside the width, (R, S, w) the rule's coefficients at the two levels a Node can read (the vacuum's 0 and the pace's edge Gamma - 1, no body's number), the tightest over every pair the files declare (the families' `pair`, the frame's checked entries, not the word body; every body's `pair` and `kind` as written, a value that is no pair of two integers from 1 left to the frame's refusal); a world with no pair takes the width itself; refused by name where no level fits."""
    pairs: list[tuple[int, int]] = []
    for item, key in [(e, "pair") for e in entries] + [
        (b, k) for b in (bodies if isinstance(bodies, list | tuple) else ()) for k in ("pair", "kind")
    ]:
        value = item.get(key) if isinstance(item, dict) else None
        if (
            isinstance(value, list | tuple)
            and len(value) == 2
            and all(type(v) is int and v >= 1 for v in value)
        ):
            pairs.append((int(value[0]), int(value[1])))
    weak_field = node_clock > 1
    found = MAX_WORK_INT
    for numerator, denominator in pairs:
        for level in (0, node_clock - 1 if weak_field else 0):
            reads, self_coefficient, wall = coefficients(
                numerator, denominator, node_clock, level, ISOTROPIC, weak_field
            )
            room = 6 * abs(reads[0]) + abs(self_coefficient) + wall
            fits = division_forward(TOTAL_BOUND - 1 - wall, room, 0)[0]
            if fits < 1:
                raise ValueError(
                    f"the pair [{numerator}, {denominator}] at the Node clock Gamma = {node_clock}: the rule's "
                    f"total 6 A R + A |S| + w (A + 1) leaves no level inside the width of {TOTAL_BOUND.bit_length() - 1} "
                    "bits (ALGEBRA.md #the-rows-against-nature)"
                )
            found = min(found, fits)
    return found


def _held_bodies_checks(
    families: tuple[FamilyDefinition, ...], measured: tuple[MeasuredDefinition, ...]
) -> None:
    """A held family takes and gives nothing (ALGEBRA.md #the-counts-line, #the-paces;
    item 51): no measured event is of it, none holds its quanta, and no
    emitter givings into it; its level is written by the engine alone, the
    declared source at every body's Nodes."""
    for index, family in enumerate(families):
        if family.held is None or family.clicks is not None:
            # a family that is held and has clicks (the charge with light as its
            # wave, ALGEBRA.md #the-primitives) has bodies of light's kind, a stock
            # and givings; its held part is the engine's write as any held family's
            continue
        name = family.name
        for number, entry in enumerate(measured):
            if entry.family == index:
                raise ValueError(
                    f"measured[{number}] is of the held family {name!r}: no body is of "
                    "it; its level is held at the bodies' Nodes, written by the engine at the "
                    "load and at every click (ALGEBRA.md #the-counts-line)"
                )
            if len(entry.held) > index and entry.held[index]:
                raise ValueError(
                    f"measured[{number}].stocks names the held family {name!r}: nothing "
                    "holds its quanta; its level is held at a body's Nodes (ALGEBRA.md #the-counts-line)"
                )
            if entry.block is not None and entry.block.emitter is not None:
                if entry.block.emitter.family == index:
                    raise ValueError(
                        f"measured[{number}].emitter givings into the held family "
                        f"{name!r}: it takes and gives nothing (ALGEBRA.md #the-counts-line)"
                    )


def _node_clock_bound(
    families: tuple[FamilyDefinition, ...],
    measured: tuple[MeasuredDefinition, ...],
    node_clock: int,
) -> None:
    """THE PACE'S GUARD AT THE LOAD (BUILD.md section 26 item 31; ALGEBRA.md #the-paces), the second pass once
    the content is known: every reading family's pace stays positive at every body's Nodes (the amplitude
    bound A is derived from the pairs alone at the pace's edge, `derived_amplitude`, so no body's content
    is read against the width here)."""

    # THE READS (ALGEBRA.md #the-counts-line, #the-paces): a family reads the pace Gamma - SUM weight x sign x
    # level over its reads; at a Node of a body in the law's form the held level is the body's source THERE (its
    # count at the Node, the stocks over its Nodes) div the held row's divisor E_s (the hold's row): per Node
    def source_of(
        family: FamilyDefinition, entry: MeasuredDefinition, counts: tuple[int, ...] = ()
    ) -> int:
        quanta, counts = sum(entry.held), counts or (sum(entry.held),)
        if family.held == "sign":
            declared = entry.block.q * quanta if entry.block is not None else 0
            quanta = abs(
                declared
                + sum(other.charge[0] * held for other, held in zip(families, entry.held, strict=True))
            )
            return -(-quanta // len(counts))
        return max(counts) - (-(quanta - sum(counts)) // len(counts))

    def divisor_of(other: int) -> int:
        return cast(int, families[other].held_divisor)

    for number, entry in enumerate(measured):
        counts = entry.block.counts or () if entry.block is not None else ()
        for family in families:
            reach = sum(
                weight
                * division_forward(source_of(families[other], entry, counts), divisor_of(other), 0)[0]
                for other, weight, _, _ in family.reads
            )
            if family.reads and reach >= node_clock:
                raise ValueError(
                    f"measured[{number}]: the pace of {family.name!r} could reach 0 at its "
                    f"Nodes: its reads weigh the body's sources to {reach} in size, not below Gamma = "
                    f"{node_clock} (ALGEBRA.md #the-paces: the charge's hill hastens a clock at most to "
                    "the vacuum's; BUILD.md section 26 items 34, 35 and 51)"
                )


def _families_of(
    entries: tuple[dict[str, object], ...],
    amplitude_bound: int | None,
    most_families: int | None,
    gamma: int,
) -> tuple[FamilyDefinition, ...]:
    """The loop's families from the frame's checked entries (the cards' keys, the frame's name and clock), with the rules between keys the cards do not state: at most twenty families, no name twice, the three forms of parts, the pair with its bound and den >= num, the clock's pair [p, q] with q from 1, the quantum on every row and the clicks card's copy equal to it, the held source's factors one per part, its dipole on a vector family with its divisor, spins_step on the family that holds the spin's dipole and no other, the self-source's unit 0 or at least 24 A, a family held, clicking or sourced, a read naming a held family once, and a held family's shape."""
    if most_families is not None and len(entries) > most_families:
        raise ValueError(
            f"families declares {len(entries)}; at most {most_families} families on a "
            "GameBoard (the universe's `most_families`, the owner's number in the file)"
        )
    names = [cast(str, obj["name"]) for obj in entries]
    if len(set(names)) != len(names):
        raise ValueError(f"two families named {next(n for n in names if names.count(n) > 1)!r}")
    found: list[FamilyDefinition] = []
    for index, row in enumerate(entries):
        label = f"families[{index}]"
        obj = derived.filled(row, entries, gamma, label)
        parts_value = tuple(cast(tuple[object, ...], obj["parts"]))
        if parts_value not in PARTS_FORMS:
            raise ValueError(
                f"{label}.parts must be one of {[list(form) for form in PARTS_FORMS]}: the "
                "representation as a list of parts, the time part first (ALGEBRA.md #the-primitives, #the-interval)"
            )
        parts = tuple(int(part) for part in parts_value)
        levels = cast(int, obj["phase"])
        pair_value = obj["pair"]
        pair_on_body = pair_value == "body"
        pair = MASSLESS_PAIR
        if not pair_on_body:
            pair_list = cast(tuple[int, int], pair_value)
            numerator, denominator = int(pair_list[0]), int(pair_list[1])
            if numerator > MAX_VALUE or denominator > MAX_VALUE:
                raise ValueError(f"{label}.pair must be [num, den], two integers up to {MAX_VALUE}")
            if denominator < 1 or (denominator <= abs(numerator) and denominator != numerator):
                raise ValueError(
                    f"{label}.pair [{numerator}, {denominator}]: den from 1, and den > |num| a massive kind "
                    "(its gap cos omega_0 = num / den, a negative numerator the mirror band; den = num light's kind)"
                )
            pair = (numerator, denominator)
        clock: tuple[int, int] | None = None
        if "clock" in obj:
            clock_value = cast(tuple[int, int], obj["clock"])
            clock = (int(clock_value[0]), int(clock_value[1]))
            if clock[1] < 1:
                raise ValueError(
                    f"{label}.clock [{clock[0]}, {clock[1]}]: the pair form [p, q] has q from 1"
                )
        sign = cast(int, obj["sign"])
        held: str | None = None
        held_factors: tuple[int, ...] = tuple(1 for _ in parts)
        held_dipole: str | None = None
        held_dipole_div = 1
        held_divisor: int | None = None
        if "held" in obj:
            source = cast(dict[str, object], obj["held"])
            held = str(source["count"])
            factors = cast(tuple[int, ...], source["factors"])
            if len(factors) != len(parts):
                raise ValueError(
                    f"{label}.held.factors must be {len(parts)} integers from 1, one per part "
                    "(ALGEBRA.md #the-interval: the held factors are the families file's numbers)"
                )
            held_factors = tuple(int(item) for item in factors)
            if "dipole" in source:
                held_dipole = str(source["dipole"])
                if len(parts) < 2:
                    raise ValueError(
                        f"{label}.held.dipole is refused on a scalar family: the dipole is "
                        "written into the vector part (ALGEBRA.md #the-interval)"
                    )
                if "dipole_div" not in source:
                    raise ValueError(
                        f"{label}.held declares a dipole and lacks dipole_div: the dipole's "
                        "divisor is the row's, no default"
                    )
            if "dipole_div" in source:
                held_dipole_div = cast(int, source["dipole_div"])
            held_divisor = cast(int, source["divisor"])
        spin_weights: tuple[tuple[int, int], tuple[int, int]] | None = None
        if "spins_step" in obj:
            if held_dipole != "spin":
                raise ValueError(
                    f"{label} declares spins_step and holds no spin's dipole: the row is the "
                    "spin holder's alone (ALGEBRA.md #a-familys-declaration)"
                )
            weights = cast(dict[str, object], obj["spins_step"])
            curl = cast(tuple[int, int], weights["curl"])
            tidal = cast(tuple[int, int], weights["tidal"])
            spin_weights = ((curl[0], curl[1]), (tidal[0], tidal[1]))
        elif held_dipole == "spin":
            raise ValueError(
                f"{label} holds the spin's dipole and lacks spins_step: the spin's step's two "
                "weights, curl and tidal, are the row's (ALGEBRA.md #a-familys-declaration), no default"
            )
        sourced: tuple[int, int, int, int | None] | None = None
        if "sourced" in obj:
            term = cast(dict[str, object], obj["sourced"])
            cap = cast(int, term["cap"]) if "cap" in term else None
            sourced = (
                names.index(cast(str, term["of"])),
                cast(int, term["weight"]),
                cast(int, term["scale"]),
                cap,
            )
        self_source = cast(dict[str, object], obj["self_source"])
        self_unit = cast(int, self_source["unit"])
        if amplitude_bound is not None and 0 < self_unit < 24 * amplitude_bound:
            raise ValueError(
                f"{label}.self_source.unit {self_unit} is below 24 A = {24 * amplitude_bound}: the "
                "self-source's unit P_2 is 0 (off) or at least 24 A (ALGEBRA.md #the-interval)"
            )
        clicks: tuple[bool, bool] | None = None
        # THE FAMILY'S QUANTUM (the law's owner's row of 2026-09-27; the Boss's word of
        # 09:27Z): one integer from 1 on every row, required; the clicks card's copy agrees
        quantum = cast(int, obj["quantum"])
        lifetime = None if "lifetime" not in obj else cast(int, obj["lifetime"])
        hand = None if "hand" not in obj else cast(int, obj["hand"])
        if quantum > MAX_VALUE:
            raise ValueError(f"{label}.quantum must be an integer up to {MAX_VALUE}")
        if "clicks" in obj:
            value = cast(dict[str, object], obj["clicks"])
            if value["gives"] is not True or value["takes"] is not True:
                raise ValueError(
                    f"{label}.clicks.gives and .takes must be true: a family of records is "
                    "given and taken at clicks (ALGEBRA.md #a-familys-declaration)"
                )
            clicks = (True, True)
            if cast(int, value["quantum"]) != quantum:
                raise ValueError(
                    f"{label}.clicks.quantum {value['quantum']} differs from the row's quantum "
                    f"{quantum}: one quantum per family (the law's owner's row, 2026-09-27)"
                )
        elif held is None and sourced is None:
            raise ValueError(
                f"{label} declares neither held (a field family), clicks (a family of records) "
                "nor sourced (a field written from a record family's count): a family does one "
                "or more (ALGEBRA.md #the-primitives row 'the source')"
            )
        raw_reads = cast(tuple[object, ...], obj["reads"])
        reads: list[tuple[int, int, str, int | str]] = []
        for entry in raw_reads:
            read = cast(dict[str, object], entry)
            other = cast(str, read["family"])
            if any(names[found_index] == other for found_index, _, _, _ in reads):
                raise ValueError(f"{label}.reads names {other!r} twice")
            weight = cast(int, read["weight"])
            twist = cast(int | str, read["twist"])
            reads.append((names.index(other), weight, READ_BY[read["by"]], twist))
        if held is not None and reads and clicks is None:
            raise ValueError(
                f"{label} is held and reads {[names[i] for i, _, _, _ in reads]}: a field "
                "family with no waves steps by the plain rule at the pace 1 of its own and reads no "
                "level (ALGEBRA.md #the-counts-line; BUILD.md section 26 item 51)"
            )
        found.append(
            FamilyDefinition(
                names[index],
                quantum,
                (sign, 1),
                phase_per_age=clock,
                lifetime=lifetime,
                hand=hand,
                pair=pair,
                held=held,
                reads=tuple(reads),
                parts=parts,
                levels=levels,
                held_factors=held_factors,
                held_dipole=held_dipole,
                held_dipole_div=held_dipole_div,
                held_divisor=held_divisor,
                spin_weights=spin_weights,
                sourced=sourced,
                self_unit=self_unit,
                clicks=clicks,
                pair_on_body=pair_on_body,
            )
        )
    families = tuple(found)
    _held_family_shapes(families)
    return families


# a read's word `by` in the file (1 plain, "q" by the reading family's own sign) to the loop's word
READ_BY: dict[object, str] = {1: "plain", "q": "sign"}


def _held_family_shapes(families: tuple[FamilyDefinition, ...]) -> None:
    """A held family's shape by attribute (ALGEBRA.md #a-familys-declaration; item 51):
    its field steps at the pair its row declares, [1, 1] or any other (no
    shortcut: the model owner, 2026-09-27), the quantum 1 (one click writes
    one unit), a clock only where it gives (the given record's), its own charge 0 (its
    level is the source it holds, it carries none); a read names a held family, and
    several families may hold one source, each at its own pair and divisor (the
    short-range well beside gravity: the owner's word of 2026-09-28)."""
    for index, family in enumerate(families):
        label = f"families[{index}] ({family.name!r})"
        if family.held is not None:
            if family.quantum != 1:
                raise ValueError(
                    f"{label} is held with the quantum {family.quantum}: a held family "
                    "is counted in quanta, one click one unit (`quantum` 1; ALGEBRA.md #the-counts-line)"
                )
            if family.phase_per_age is not None and family.clicks is None:
                raise ValueError(
                    f"{label} is held, gives nothing and declares a clock: the clock [p, q] is the given "
                    "record's, lambda_q = 2 N q / p (ALGEBRA.md #the-primitives the recoil's row)"
                )
            if family.charge[0] != 0:
                raise ValueError(
                    f"{label} is held and declares the charge {family.charge[0]}: a held "
                    "family carries none, its level is the source it holds (ALGEBRA.md #the-paces)"
                )
        for other, _, _, _ in family.reads:
            if families[other].held is None:
                raise ValueError(
                    f"{label}.reads names {families[other].name!r}, which is not held: "
                    "a family's pace reads the held families' levels alone (ALGEBRA.md #the-counts-line, "
                    "ALGEBRA.md #the-paces; BUILD.md section 26 item 51)"
                )


def _window(value: object, label: str, phase_steps: int) -> int:
    """A phase window's setting: a step of the circle, 0 through N - 1."""
    return _integer(value, label, 0, phase_steps - 1)


def _receiver_names(obj: dict[str, object], label: str) -> tuple[str, ...] | None:
    """The lamp's `receiver`, its records' ladder by name: a set's name or a
    list of distinct names; None without the key."""
    if "receiver" not in obj:
        return None
    value = obj["receiver"]
    names = [value] if isinstance(value, str) else list(value) if isinstance(value, tuple) else value
    if (
        not isinstance(names, list)
        or not names
        or any(not isinstance(name, str) or not name for name in names)
    ):
        raise ValueError(
            f"{label}.receiver must be a detector set's name or a nonempty list of "
            "names (the lamp record's ladder, SIZING.md)"
        )
    if len(set(names)) != len(names):
        raise ValueError(f"{label}.receiver names a set twice")
    return tuple(names)


def _block(
    obj: dict[str, object],
    label: str,
    family: FamilyDefinition,
    families: tuple[FamilyDefinition, ...],
    names: dict[str, int],
    held: list[int],
    momentum: tuple[int, ...],
    amount: int,
    momentum_unit: int,
    lamp_declared: bool,
    span: tuple[int, int, int],
    shape: Address3,
    amplitude_bound: int,
    phase_steps: int,
    most_steps: int | None,
    periodic: tuple[bool, bool, bool] = (True, True, True),
    least_residues: int | None = None,
) -> BlockDefinition | None:
    """The block's keys on a measured event, each named in its refusal: `side` or `extents` makes a block and
    every other block key without them is refused; its `pair` a well on the massive kind or a gap on light's;
    a giving body's pair rich (at least the universe's `least_residues` remainder values at its Node, ALGEBRA.md
    #a-familys-declaration); the momentum bounded by the pace, 3 (P . P) < (3 Q M)^2 (ALGEBRA.md #the-primitives)."""
    declared = [key for key in BLOCK_KEYS if key in obj]
    if "side" not in obj and "extents" not in obj:
        if declared:
            raise ValueError(
                f"{label}.{declared[0]} belongs to a block (a measured event that "
                "declares `side` or `extents`, massive-record-v1)"
            )
        return None
    if "side" in obj and "extents" in obj:
        raise ValueError(
            f"{label} declares both `side` and `extents`: a cube is `side`, a box is "
            "`extents` [x, y, z] (the bodies with extents per axis; BUILD.md section 26 item 23)"
        )
    if lamp_declared:
        raise ValueError(f"{label}: a block declares no lamp (its record is its own)")
    if span != ONE_NODE:
        raise ValueError(f"{label}: a block declares `side`, never `span`")
    if "side" in obj:
        side = _integer(obj["side"], f"{label}.side", 1)
        extents = (side, side, side)
    else:
        value = obj["extents"]
        if not isinstance(value, list | tuple) or len(value) != 3:
            raise ValueError(
                f"{label}.extents must be [x, y, z], the box's extents per axis, "
                "each from 1 (the bodies with extents per axis; BUILD.md section 26 item 23)"
            )
        extents = (
            _integer(value[0], f"{label}.extents[0]", 1),
            _integer(value[1], f"{label}.extents[1]", 1),
            _integer(value[2], f"{label}.extents[2]", 1),
        )
        side = extents[0]
    if "pair" not in obj:
        raise ValueError(f"{label} lacks keys: pair (the block's pair at its Nodes)")
    value = obj["pair"]
    if not isinstance(value, list | tuple) or len(value) != 2:
        raise ValueError(f"{label}.pair must be [num, den], the pair at the Nodes")
    pair = (
        _integer(value[0], f"{label}.pair numerator", 1, MAX_VALUE),
        _integer(value[1], f"{label}.pair denominator", 1, MAX_VALUE),
    )
    # THE BODY'S KIND (ALGEBRA.md #the-primitives, #the-interval): the family's pair, or the
    # body's own `kind` [num, den] on a family whose pair is the body's,
    # required there and refused elsewhere (one copy)
    if family.pair_on_body:
        if "kind" not in obj:
            raise ValueError(
                f"{label}.kind is required: the family {family.name!r} declares no pair, "
                "so every body of it declares its own rest pair [num, den] (ALGEBRA.md #the-primitives, "
                "ALGEBRA.md #the-interval)"
            )
        kind_value = obj["kind"]
        if not isinstance(kind_value, list | tuple) or len(kind_value) != 2:
            raise ValueError(f"{label}.kind must be [num, den], the body's rest pair")
        kind = (
            _integer(kind_value[0], f"{label}.kind numerator", 1, MAX_VALUE),
            _integer(kind_value[1], f"{label}.kind denominator", 1, MAX_VALUE),
        )
        if kind[1] <= kind[0]:
            raise ValueError(
                f"{label}.kind [{kind[0]}, {kind[1]}] is no massive kind: den > num, "
                "the gap cos omega_0 = num / den (ALGEBRA.md #a-familys-declaration)"
            )
    elif "kind" in obj:
        raise ValueError(
            f"{label}.kind is refused: the family {family.name!r} declares its pair "
            f"{list(family.pair)}; one copy (ALGEBRA.md #the-primitives)"
        )
    else:
        kind = family.pair
    if family.massive_kind:
        # A well lowers the pair; a BARRIER raises it (num' / den' below the
        # kind's: the matter wall of DECLARATIONS.md section 15 M1-6, the
        # mirror line of the matter kind), a block with no bound mode, no
        # seed and no clock; the kind's own pair is no body (the cavity of
        # form (I), a record held by mirror faces of its own, is refused by
        # name: BUILD.md section 26 item 28).
        if pair[0] * kind[1] == pair[1] * kind[0]:
            raise ValueError(
                f"{label}.pair [{pair[0]}, {pair[1]}] is the kind's own pair "
                f"[{kind[0]}, {kind[1]}]: a block lowers the pair at its Nodes (a well) or "
                "raises it (a barrier; MASSIVE_RECORD.md section 4, section 15 M1-6)"
            )
        if pair[0] * kind[1] < pair[1] * kind[0]:
            clock_keys = [key for key in ("seed", "margin") if key in obj]
            if clock_keys:
                raise ValueError(
                    f"{label}.{clock_keys[0]} is refused on a barrier (a raised pair "
                    f"[{pair[0]}, {pair[1]}] on the kind [{kind[0]}, {kind[1]}] has no bound mode "
                    "and no clock; DECLARATIONS.md section 15 M1-6)"
                )
            obj = dict(obj, seed=0)
    else:
        if pair[1] <= pair[0]:
            raise ValueError(
                f"{label}.pair [{pair[0]}, {pair[1]}] on light's kind is no gap: the "
                "(M) wall declares den > num (a lump in the massless surround, "
                "MASSIVE_RECORD.md section 4)"
            )
        clock_keys = [key for key in ("seed", "margin") if key in obj]
        if clock_keys:
            raise ValueError(
                f"{label}.{clock_keys[0]} is refused on a block of light's kind (the "
                "(M) wall has no clock)"
            )
        # the mirror line of light's kind (DECLARATIONS.md section 15 L-1):
        # its Nodes carry the gap's pair and nothing else, no own record
        obj = dict(obj, seed=0)
    if "seed" not in obj:
        # NO IMPLICIT SEED (the model owner, 2026-09-25; BUILD.md section 26 item 28)
        raise ValueError(
            f"{label} lacks keys: seed (a well's own record on its Nodes: its "
            "amplitude at interval 0, 0 silent, or its profile with `margin`; no default, "
            "BUILD.md section 26 item 28)"
        )
    seed: int
    profile: tuple[int, ...] | None = None
    clock: tuple[int, int] | None = None
    if isinstance(obj["seed"], list | tuple):
        # the bound mode's integer profile over the whole board with its clock, admitted with `margin` declared
        if "margin" not in obj:
            raise ValueError(f"{label}.seed as a profile is admitted only with margin declared")
        profile, seed, clock = _profile_and_clock(obj["seed"], obj.get("clock"), shape, label, "seed")
    else:
        seed = _integer(obj["seed"], f"{label}.seed", 0)
        if "clock" in obj:
            raise ValueError(
                f"{label}.clock is admitted only beside a profile (the mode's 2 cos "
                "omega belongs to the mode's integers, ALGEBRA.md #a-familys-declaration)"
            )
    # THE PROPER PAIR OF A MOVING BODY ON ONE NODE (ALGEBRA.md #the-velocity; BUILD.md section 26
    # item 46): beside `clock`, on a block whose momentum lies on one axis, the
    # |P| + 1 pairs [num, den] indexed by the momentum's whole part, the first
    # the clock itself (the rest pair at K = 0)
    proper_clock: tuple[tuple[int, int], ...] | None = None
    if "proper_clock" in obj:
        moving_axes = [axis for axis in range(3) if int(momentum[axis]) != 0]
        if clock is None or len(moving_axes) != 1:
            raise ValueError(
                f"{label}.proper_clock is admitted beside `clock` on a block whose "
                "momentum lies on one axis (the moving body's Node's pairs by the momentum's whole part, "
                "ALGEBRA.md #the-velocity)"
            )
        value = obj["proper_clock"]
        count = abs(int(momentum[moving_axes[0]])) + 1
        if (
            not isinstance(value, list | tuple)
            or len(value) != count
            or any(
                not isinstance(item, list | tuple)
                or len(item) != 2
                or any(type(part) is not int for part in item)
                or item[0] < 1
                or item[1] < seed
                for item in value
            )
        ):
            raise ValueError(
                f"{label}.proper_clock must be {count} pairs [num, den] of positive "
                f"integers, den at least the profile's amplitude {seed}, one for every whole part "
                f"of the momentum from 0 to {count - 1} (ALGEBRA.md #the-velocity)"
            )
        if (int(value[0][0]), int(value[0][1])) != clock:
            raise ValueError(
                f"{label}.proper_clock[0] {value[0]} is not the clock {list(clock)}: at "
                "rest the body's Node rotates at the mode's own pair (ALGEBRA.md #the-velocity)"
            )
        proper_clock = tuple((int(item[0]), int(item[1])) for item in value)
    if seed > amplitude_bound:
        raise ValueError(
            f"{label}.seed {seed} (the scalar seed, or a profile's largest magnitude) "
            f"is above the world's amplitude bound A = {amplitude_bound} on the pair "
            f"[{pair[0]}, {pair[1]}]: every admitted amplitude enters the one declared bound "
            "(issue #1085; MUST 3)"
        )
    ramp = 0 if "ramp" not in obj else _integer(obj["ramp"], f"{label}.ramp", 0)
    start = 0 if "start" not in obj else _integer(obj["start"], f"{label}.start", 0)
    # THE BODY'S NUMBERS (ALGEBRA.md #the-interval; commit 2): charge, spin and moment,
    # required under the law (no default), integers on the axes (record 2084)
    _require_under_law(obj, label, {"q", "spin", "spin_before", "moment", "twist"})
    charge = _integer(obj["q"], f"{label}.q", -AMOUNT_BOUND, AMOUNT_BOUND)
    spin = _axes_vector(obj["spin"], f"{label}.spin")
    spin_before = _axes_vector(obj["spin_before"], f"{label}.spin_before")
    moment = _axes_vector(obj["moment"], f"{label}.moment")
    if "margin" not in obj and pair[0] * kind[1] > pair[1] * kind[0]:
        # NO DEFAULT UNDER THE DETECTOR LAW (record 2089; item 57): a well's
        # margin kind, pin or control, declared (record 2037, per measured
        # event); a barrier or a gap declares none (refused above)
        raise ValueError(
            f"{label}.margin is required on a well: one of "
            f"{list(MARGIN_KINDS)}, no default (the model owner's records 2037 and 2089)"
        )
    margin = cast(str, obj["margin"]) if "margin" in obj else None
    if margin is not None and margin not in MARGIN_KINDS:
        raise ValueError(f"{label}.margin must be one of {list(MARGIN_KINDS)}")
    # THE WALL W = 3 Q M (ALGEBRA.md #the-primitives, #the-well): one wall per body, on its
    # whole content at the load, its own quanta and what it holds (the stock is
    # content, ALGEBRA.md #the-paces); the width S = 1 is gone
    wall = 3 * momentum_unit * sum(held)
    if 3 * sum(component * component for component in momentum) >= wall * wall:
        raise ValueError(
            f"{label}.momentum {list(momentum)}: the pace bound 3 (P . P) < (3 Q M)^2 "
            f"= {wall * wall} fails (the body's velocity v = P / (3 Q M) below c, ALGEBRA.md "
            "ALGEBRA.md #the-primitives; DESIGN.md 5.1 (a))"
        )
    receiver: str | None = None
    if "receiver" in obj:
        if "emitter" not in obj:
            raise ValueError(
                f"{label}.receiver is refused on a block that emits nothing (the "
                "receiver by name is the ladder of the block's emitted records, DECLARATIONS.md "
                "section 13 item 7)"
            )
        value = obj["receiver"]
        if not isinstance(value, str) or not value:
            raise ValueError(
                f"{label}.receiver must be the name of a declared detector set (a nonempty string)"
            )
        receiver = value
    emitter: EmitterDefinition | None = None
    stock = 0
    if "emitter" in obj:
        # the emitter as a clicking body (ALGEBRA.md #the-click): a body of a
        # massive kind with its seed (the excited record) and its stock
        if not family.massive_kind:
            raise ValueError(
                f"{label}.emitter is refused on a body of light's kind: the emitter "
                "is a body of a massive kind whose excited record (its seed, the bound mode) "
                "clicks at its own rung (ALGEBRA.md #the-click)"
            )
        if seed <= 0:
            raise ValueError(
                f"{label}.emitter needs the body's `seed` (its excited record is the "
                "seed at both levels; a silent body excites nothing)"
            )
        if amount < 1:
            raise ValueError(
                f"{label}.emitter needs `amount` from 1, the body's own quanta (its "
                "stock is the given family's content under `held`, ALGEBRA.md #the-paces)"
            )
        # THE RESIDUES OF AN EMITTING BODY spread from the remainder kept at
        # its Nodes (the model owner's decisions (1) and (2) of record 1962;
        # ALGEBRA.md #the-line (A) and (B)): the coupling of ALGEBRA.md #rule3 is HISTORY
        emitter = _emitter(
            obj["emitter"],
            f"{label}.emitter",
            family,
            families,
            names,
            shape,
            phase_steps,
            most_steps,
            extents=extents,
            periodic=periodic,
            momentum=momentum,
            moment=moment,
            clock_pair=clock,
            twist=_integer(obj["twist"], f"{label}.twist", 0),
        )
        # THE STOCK IS GIVEN-FAMILY CONTENT (ALGEBRA.md #the-paces; BUILD.md
        # section 26 item 47): the quanta a body gives are the given family's,
        # held at the body under `held`; a giving lowers them and leaves the
        # body's own quanta and its charge (a body spending its own quantum
        # per giving would lose charge by giving light: refused)
        # A BODY GIVING ITS OWN FAMILY (ALGEBRA.md #the-primitives; commit 6): its stock is `stock`, a
        # count of its own quanta set aside for giving, from 1 to `amount`; each giving lowers
        # M by one; `stock` is refused where the given family is another (its stock is `held`)
        if emitter.family == names[family.name]:
            if "stock" not in obj:
                raise ValueError(
                    f"{label}.stock is required: the emitter gives the body's own family "
                    f"{family.name!r}, so the body declares the count of its own quanta set aside for "
                    "giving, from 1 to `amount` (ALGEBRA.md #the-primitives)"
                )
            stock = _integer(obj["stock"], f"{label}.stock", 1, amount)
        elif "stock" in obj:
            raise ValueError(
                f"{label}.stock is refused: the emitter gives {families[emitter.family].name!r}, "
                "another family, whose stock is the body's `held` quanta of it (ALGEBRA.md #the-paces, "
                "ALGEBRA.md #the-primitives)"
            )
        elif held[emitter.family] < 1:
            raise ValueError(
                f"{label}.emitter needs its stock as the given family's content held "
                f"at the body: `held` naming {families[emitter.family].name!r} from 1 (a world that "
                "needs W givings holds W; ALGEBRA.md #the-paces: a giving lowers the given family's "
                "content, the body's own quanta `amount` and its charge stay)"
            )
        # THE RICHNESS OF THE GIVING NODE (ALGEBRA.md #a-familys-declaration): 3 den / gcd(num, 3 den) residues
        residues = 3 * pair[1] // math.gcd(pair[0], 3 * pair[1])
        if least_residues is not None and residues < least_residues:
            raise ValueError(
                f"{label}.emitter: the body's pair [{pair[0]}, {pair[1]}] gives "
                f"{residues} remainder values at the giving Node (3 den / gcd(num, 3 den)), below "
                f"the universe's least_residues {least_residues}: the residue from the law needs a rich pair "
                "(ALGEBRA.md #a-familys-declaration; [801, 700] on the kind [7, 8] gives 700)"
            )
        if receiver is not None and emitter.receiver is not None:
            raise ValueError(
                f"{label}: one ladder for the given records: the block's `receiver` "
                "(one name, the line at the rung) or the emitter's `receiver` (a list, the "
                "ladder by name), not both"
            )
    return BlockDefinition(
        side,
        pair,
        kind,
        seed,
        extents=extents,
        profile=profile,
        clock=clock,
        proper_clock=proper_clock,
        ramp=ramp,
        start=start,
        q=charge,
        spin=spin,
        spin_before=spin_before,
        moment=moment,
        # THE BODY'S OWN RECORD'S TWIST "OWN" (ALGEBRA.md #the-primitives; item 73): the
        # generator's integer round(2^16 omega_0) declared under `twist` (its mode's
        # rotation, or its kind's rest rotation on a body without a mode), no default
        twist=_integer(obj["twist"], f"{label}.twist", 0),
        margin=margin,
        receiver=receiver,
        emitter=emitter,
        stock=stock,
    )


def _axes_vector(value: object, label: str) -> tuple[int, int, int]:
    """An integer vector on the axes (record 2084: every directed thing an integer
    vector on the axes), three integers."""
    if not isinstance(value, list | tuple) or len(value) != 3:
        raise ValueError(f"{label} must be three integers, a vector on the axes")
    return (
        _integer(value[0], f"{label}[0]", -AMOUNT_BOUND, AMOUNT_BOUND),
        _integer(value[1], f"{label}[1]", -AMOUNT_BOUND, AMOUNT_BOUND),
        _integer(value[2], f"{label}[2]", -AMOUNT_BOUND, AMOUNT_BOUND),
    )


def _emitter(
    value: object,
    label: str,
    family: FamilyDefinition,
    families: Sequence[FamilyDefinition],
    names: dict[str, int],
    shape: Address3,
    phase_steps: int,
    most_steps: int | None,
    extents: tuple[int, int, int] = (1, 1, 1),
    periodic: tuple[bool, bool, bool] = (True, True, True),
    momentum: tuple[int, ...] = (0, 0, 0),
    moment: tuple[int, int, int] = (0, 0, 0),
    clock_pair: tuple[int, int] | None = None,
    twist: int = 0,
    wavelength: int | None = None,
    wave_number: int | None = None,
) -> EmitterDefinition:
    """The `emitter` object of a clicking body (ALGEBRA.md #the-click to (6), #a-familys-declaration): the given family (a paid family), the given record's clock [2 N, lambda_q] with lambda_q the mode's reading `wavelength` (the giver's rotation on the given band; the recoil's row) or, for a giver whose mode file carries none, the row's `clock` [p, q]; the given labels, the ladder by name, the norm (the generator's integer), the period P_body by the one-Node rule from the mode's clock pair, the twist "own" the body's; no wheel, residue order, seed, period, clock or twist of its own: each is the law's, the keys refused by name."""
    obj = cast(dict[str, object], value)  # the frame's checked emitter (loader/frame.py, `EMITTER`)
    name = obj["family"]
    if not isinstance(name, str) or name not in names:
        raise ValueError(f"{label}.family names an unknown family")
    given_family = families[names[name]]
    # THE GIVEN RECORD'S PAIR (ALGEBRA.md #the-primitives, #the-interval): the emitter's `pair` [num, den], required when the
    # given family's pair is the body's (a body giving its own family, its stock its own quanta) and refused when the family declares one
    given_pair: tuple[int, int]
    if given_family.pair_on_body:
        if "pair" not in obj:
            raise ValueError(
                f"{label}.pair is required: the given family {name!r} declares no pair, "
                "so the emitter declares the given record's pair [num, den] (ALGEBRA.md #the-primitives, "
                "ALGEBRA.md #the-interval)"
            )
        given_pair = _ratio(obj["pair"], f"{label}.pair", zero=False)
        if given_pair[1] <= given_pair[0]:
            raise ValueError(
                f"{label}.pair [{given_pair[0]}, {given_pair[1]}] is no massive kind: den "
                "> num (ALGEBRA.md #a-familys-declaration)"
            )
    elif "pair" in obj:
        raise ValueError(
            f"{label}.pair is refused: the given family {name!r} declares its pair "
            f"{list(given_family.pair)}; one copy (ALGEBRA.md #the-primitives)"
        )
    else:
        given_pair = given_family.pair
    if given_family.held is not None and given_family.clicks is None:
        raise ValueError(
            f"{label} givings into the held family {name!r}: it takes and gives "
            "nothing (ALGEBRA.md #the-counts-line)"
        )
    # THE GIVEN CLOCK: [2 N, lambda_q] from the mode's `wavelength` (the giver's rotation on the given band, no key: ALGEBRA.md
    # #the-primitives, the crystal's and the recoil's rows); the family's row's `clock` [p, q] where the mode file carries none
    if wavelength is not None:
        clock = (2 * phase_steps, wavelength)
    elif given_family.phase_per_age is None:
        raise ValueError(
            f"{label}: the given family {name!r} declares no clock and the mode file no wavelength; the "
            "given record's clock is the mode's `wavelength` (ALGEBRA.md #the-primitives, the recoil's row)"
        )
    else:
        clock = (int(given_family.phase_per_age[0]), int(given_family.phase_per_age[1]))
    step = clock[0] // clock[1]
    if step % 2 == 1 and most_steps is not None and 2 * phase_steps > most_steps:
        raise ValueError(
            f"{label}.family {name!r}: the given clock's step floor(n / d) = {step} is "
            f"odd and the write's circle of 2 N = {2 * phase_steps} steps exceeds the universe's "
            f"most_steps {most_steps} (ALGEBRA.md #the-click); declare an even step or a smaller N"
        )
    branches: tuple[tuple[int, int], ...] = ((0, 1),)
    label_hands: tuple[int, int] | None = None
    receiver = _receiver_names(obj, label)
    # THE PERIOD FROM THE BODY'S OWN MODE (the recoil's row: P_body by the one-Node rule from its clock pair, never declared; none off the mode)
    period = None if clock_pair is None else period_by_the_rule(clock_pair[0], clock_pair[1])
    # THE POINT EMITTER'S WEIGHT (ALGEBRA.md; item 50): an integer from 1; `point_emitter` pairs it with no train
    weight = None if "weight" not in obj else _integer(obj["weight"], f"{label}.weight", 1)
    norm_denominator = (
        None
        if "norm_denominator" not in obj
        else _integer(obj["norm_denominator"], f"{label}.norm_denominator", 1)
    )
    norm = None if "norm" not in obj else _integer(obj["norm"], f"{label}.norm", 1, NORM_BOUND)
    # THE GIVEN RECORD'S COMPONENT (ALGEBRA.md #the-second-level): on a vector family the
    # component along the body's moment mu, one axis; a scalar family's one component
    part = 0
    if len(given_family.parts) > 1:
        axes = [axis for axis in range(3) if moment[axis] != 0]
        if len(axes) != 1:
            raise ValueError(
                f"{label}: the given family {name!r} is a vector family and the body's "
                f"moment {list(moment)} lies on {len(axes)} axes: the given record is written into the "
                "component along the body's moment, one axis (ALGEBRA.md #the-second-level; a body with no "
                "moment gives no direction to write)"
            )
        part = 1 + axes[0]
    return EmitterDefinition(
        names[name],
        branches,
        label_hands,
        receiver,
        clock,
        given_pair,
        period,
        norm,
        weight=weight,
        norm_denominator=norm_denominator,
        part=part,
        twist=twist,  # the given record's twist "own" is its giver's (ALGEBRA.md #the-primitives; the files' emitters agree)
        wave_number=wave_number,
    )


def _measured(
    value: object,
    shape: Address3,
    periodic: tuple[bool, bool, bool],
    families: tuple[FamilyDefinition, ...],
    phase_steps: int,
    most_steps: int | None,
    ticks: int,
    action: int | None,
    amplitude_bound: int = AMPLITUDE_BOUND,
    momentum_unit: int = 0,
    least_residues: int | None = None,
    mode_bodies: tuple[dict[str, object] | None, ...] = (),
) -> tuple[MeasuredDefinition, ...]:
    bodies = cast(
        tuple[dict[str, object], ...], value
    )  # the frame's checked bodies (loader/frame.py, `BODY`)
    names = {family.name: index for index, family in enumerate(families)}
    found: list[MeasuredDefinition] = []
    # Every Node of every body so far: two measured events never share one.
    occupied: set[Address3] = set()
    for index, obj in enumerate(bodies):
        label = f"measured[{index}]"
        if "nodes" in obj:
            mode = mode_bodies[index] if index < len(mode_bodies) else None
            bounds = (amplitude_bound, phase_steps, most_steps)
            found.append(
                _counted(
                    obj, label, families, names, shape, occupied, momentum_unit, mode, bounds, periodic
                )
            )
            continue
        if "side" in obj or "extents" in obj:
            # NO DEFAULT UNDER THE DETECTOR LAW (record 2089; item 57): the drive's ramp and
            # start on every block; the momentum and the stocks are the schema's required keys
            _require_under_law(obj, label, {"ramp", "start"})
        position = _address(obj["position"], f"{label}.position", shape)
        if any(item.position == position for item in found):
            raise ValueError(f"two measured events at one Node {list(position)}")
        span = ONE_NODE
        nodes = body_nodes(position, span, shape, periodic)
        if nodes is None:
            raise ValueError(
                f"{label}: a body of span {list(span)} centred on {list(position)} "
                "leaves the GameBoard through an open face"
            )
        shared = [node for node in nodes if node in occupied]
        if shared:
            raise ValueError(
                f"two measured events share the Node {list(shared[0])} "
                f"({label}, a body of span {list(span)})"
            )
        occupied.update(nodes)
        family_name = obj["family"]
        if not isinstance(family_name, str) or family_name not in names:
            raise ValueError(f"{label}.family names an unknown family")
        family = names[family_name]
        amount = _integer(obj["amount"], f"{label}.amount", 1)
        held = [0] * len(families)
        held[family] = amount
        # THE BODY'S STOCKS of other families' quanta (`stocks`, record 2128 (1); beside
        # ALGEBRA.md #the-primitives's `stock` of its own): the given family's content held at the body
        declared_held = cast(dict[str, object], obj["stocks"])
        for key, content in declared_held.items():
            if key not in names:
                raise ValueError(f"{label}.stocks names an unknown family {key!r}")
            if names[key] == family:
                raise ValueError(
                    f"{label}.stocks names the event's own family {key!r}, whose content is `amount`"
                )
            held[names[key]] = _integer(content, f"{label}.stocks[{key!r}]", 1)
        # the ray law's phase, phase_by_momentum, directions, table and become are no keys of
        # the file (the frame refuses them by name); the loop still reads their attributes
        phase = 0
        momentum_value = cast(tuple[object, ...], obj["momentum"])
        momentum = tuple(_integer(item, f"{label}.momentum", -AMOUNT_BOUND) for item in momentum_value)
        before_value = cast(tuple[object, ...], obj["momentum_before"])
        momentum_before = tuple(
            _integer(item, f"{label}.momentum_before", -AMOUNT_BOUND) for item in before_value
        )
        turning = False
        # the ray law's table: every family at the keys' rule `measure` with the scalar
        # component, no window (no family is free: the row's quantum is from 1)
        rules: list[str] = [TABLES[1] for _ in families]
        windows: list[int | None] = [None for _ in families]
        reads: list[str] = ["scalar" for _ in families]
        block = _block(
            obj,
            label,
            families[family],
            families,
            names,
            held,
            momentum,
            amount,
            momentum_unit,
            False,
            span,
            shape,
            amplitude_bound,
            phase_steps,
            most_steps,
            periodic,
            least_residues,
        )
        found.append(
            MeasuredDefinition(
                position,
                family,
                amount,
                phase,
                (momentum[0], momentum[1], momentum[2]),
                (momentum_before[0], momentum_before[1], momentum_before[2]),
                tuple(rules),
                tuple(windows),
                tuple(reads),
                span,
                turning,
                tuple(held),
                block=block,
            )
        )
    return tuple(found)


def _counted(
    obj: dict[str, object],
    label: str,
    families: tuple[FamilyDefinition, ...],
    names: dict[str, int],
    shape: Address3,
    occupied: set[Address3],
    momentum_unit: int,
    mode: dict[str, object] | None,
    bounds: tuple[int, int, int | None],
    periodic: tuple[bool, bool, bool],
) -> MeasuredDefinition:
    """A body in the law's form (ALGEBRA.md #what-a-body-is; the frame's `COUNTED`): its family, its Nodes with their counts, its momentum's two levels, its spin's two levels and its moment where declared, its stocks; the block's corner the Nodes' lowest per axis, its extents their box, its Nodes and counts kept for the loop (the mask and the count's line); the pair its family's, no seed, no well and no giving yet."""
    family_name = obj["family"]
    if not isinstance(family_name, str) or family_name not in names:
        raise ValueError(f"{label}.family names an unknown family")
    family = names[family_name]
    if families[family].pair_on_body:
        raise ValueError(
            f"{label}: the family {family_name!r} declares no pair, and a body in the law's form "
            "declares none (its record is the generator's; ALGEBRA.md #what-a-body-is)"
        )
    lines = cast(tuple[dict[str, object], ...], obj["nodes"])
    nodes = tuple(
        _address(line["node"], f"{label}.nodes[{i}].node", shape) for i, line in enumerate(lines)
    )
    counts = tuple(
        _integer(line["count"], f"{label}.nodes[{i}].count", 1) for i, line in enumerate(lines)
    )
    shared = [node for node in nodes if node in occupied]
    if shared:
        raise ValueError(f"two measured events share the Node {list(shared[0])} ({label})")
    occupied.update(nodes)
    corner = tuple(min(node[axis] for node in nodes) for axis in range(3))
    extents = tuple(max(node[axis] for node in nodes) - corner[axis] + 1 for axis in range(3))
    amount = sum(counts)
    held = [0] * len(families)
    held[family] = amount
    for key, content in cast(dict[str, object], obj["stocks"] if "stocks" in obj else {}).items():
        if key not in names:
            raise ValueError(f"{label}.stocks names an unknown family {key!r}")
        if names[key] == family:
            raise ValueError(
                f"{label}.stocks names the body's own family {key!r}, whose count is its Nodes'"
            )
        held[names[key]] = _integer(content, f"{label}.stocks[{key!r}]", 1)
    momentum = _axes_vector(obj["momentum"], f"{label}.momentum")
    momentum_before = _axes_vector(obj["momentum_before"], f"{label}.momentum_before")
    wall = 3 * momentum_unit * sum(held)
    if 3 * sum(component * component for component in momentum) >= wall * wall:
        raise ValueError(
            f"{label}.momentum {list(momentum)}: the pace bound 3 (P . P) < (3 Q M)^2 = {wall * wall} "
            "fails (the body's velocity below c, ALGEBRA.md #the-primitives)"
        )
    # THE BODY'S OWN RECORD FROM THE MODE FILE (ALGEBRA.md #what-a-body-is): its profile with its clock, its twist "own", a moving body's two levels; a giving body needs the first three
    zero = (0, 0, 0)
    moment = _axes_vector(obj["moment"], f"{label}.moment") if "moment" in obj else zero
    profile: tuple[int, ...] | None = None
    clock: tuple[int, int] | None = None
    levels: Levels | None = None
    amplitude, twist, wavelength, wave_number = 0, None, None, None
    if mode is not None:
        mode_label = f"the mode file's bodies[{label[len('measured[') : -1]}]"
        if (
            mode.get("family") != family_name
            or tuple(cast(list[int], mode.get("pair") or ())) != families[family].pair
        ):
            raise ValueError(
                f"{mode_label} is of the family {mode.get('family')!r} with the pair {mode.get('pair')}, "
                f"the body of {family_name!r} with {list(families[family].pair)}"
            )
        if "profile" in mode:
            profile, amplitude, clock = _profile_and_clock(
                mode["profile"], mode.get("clock"), shape, mode_label, "profile"
            )
            if amplitude > bounds[0]:
                raise ValueError(
                    f"{mode_label}.profile's amplitude {amplitude} is above the world's amplitude bound "
                    f"A = {bounds[0]} (issue #1085; MUST 3)"
                )
        if "twist" in mode:
            twist = _integer(mode["twist"], f"{mode_label}.twist", 0)
        if "wavelength" in mode:
            wavelength = _integer(mode["wavelength"], f"{mode_label}.wavelength", 1)
        if "wave_number" in mode:
            wave_number = _integer(mode["wave_number"], f"{mode_label}.wave_number", 0)
        levels = moving_levels(
            mode.get("moving"), clock, shape[0] * shape[1] * shape[2], mode_label, bounds[0]
        )
    emitter = None
    if "emitter" in obj:
        if profile is None or twist is None:
            lacking = "no entry" if mode is None else "no profile" if profile is None else "no twist"
            raise ValueError(
                f"{label}.emitter on a body in the law's form needs the body's own record from the mode file "
                f"beside the world (`<world>.mode.json`, the generator's): its profile, its clock and its twist; "
                f"the mode file has {lacking} for it"
            )
        if names[cast(str, cast(dict[str, object], obj["emitter"])["family"])] == family:
            raise ValueError(
                f"{label}.emitter gives the body's own family: its stock is today's form's `stock`"
            )
        emitter = _emitter(
            obj["emitter"],
            f"{label}.emitter",
            families[family],
            families,
            names,
            shape,
            bounds[1],
            bounds[2],
            extents=(extents[0], extents[1], extents[2]),
            periodic=periodic,
            momentum=momentum,
            moment=moment,
            clock_pair=clock,
            twist=twist,
            wavelength=wavelength,
            wave_number=wave_number,
        )
    block = BlockDefinition(
        extents[0],
        families[family].pair,
        families[family].pair,
        amplitude,
        spin=_axes_vector(obj["spin"], f"{label}.spin") if "spin" in obj else zero,
        spin_before=_axes_vector(obj["spin_before"], f"{label}.spin_before")
        if "spin_before" in obj
        else zero,
        extents=(extents[0], extents[1], extents[2]),
        moment=moment,
        profile=profile,
        clock=clock,
        levels=levels,
        twist=twist if twist is not None else 0,
        emitter=emitter,
        nodes=nodes,
        counts=counts,
        phase_denominator=_integer(obj["phase_denominator"], f"{label}.phase_denominator", 1)
        if "phase_denominator" in obj
        else None,
        q=_integer(obj["q"], f"{label}.q", -AMOUNT_BOUND, AMOUNT_BOUND) if "q" in obj else 0,
        declared={key: value for key, value in obj.items() if key not in frame.COUNTED.keys},
    )
    return MeasuredDefinition(
        (corner[0], corner[1], corner[2]),
        family,
        amount,
        0,
        momentum,
        momentum_before,
        tuple(TABLES[1] for _ in families),
        tuple(None for _ in families),
        tuple("scalar" for _ in families),
        ONE_NODE,
        False,
        tuple(held),
        block=block,
    )


def block_extents(side: int | tuple[int, int, int]) -> tuple[int, int, int]:
    """A block's extents per axis: the cube's side three times, or the box's
    extents as given."""
    if isinstance(side, int):
        return (side, side, side)
    return (int(side[0]), int(side[1]), int(side[2]))


def body_node_indices(
    shape: tuple[int, int, int],
    corner: tuple[int, int, int],
    side: int | tuple[int, int, int],
    wrap: tuple[bool, bool, bool],
) -> list[int]:
    """The block's Nodes as the engine forms them (`_box`): the box of the
    extents per axis (a cube's side for all three) from its lower corner,
    wrapped on a periodic axis of the kind, cut on an open one; the Nodes'
    flat indices in x-major order (x, then y, then z). The one copy of the
    rule in integers; the margin module's array form (`body_node_mask`) is
    built from it."""
    extents = block_extents(side)
    ranges: list[list[int]] = []
    for axis in range(3):
        indices = [corner[axis] + offset for offset in range(extents[axis])]
        if wrap[axis]:
            indices = [index % shape[axis] for index in indices]
        else:
            indices = [index for index in indices if 0 <= index < shape[axis]]
        ranges.append(sorted(set(indices)))
    if not all(ranges):
        return []
    stride_x, stride_y = shape[1] * shape[2], shape[2]
    return [x * stride_x + y * stride_y + z for x in ranges[0] for y in ranges[1] for z in ranges[2]]


# THE FILE'S DIGEST AND THE STAMP the generator writes (`input_digest`, `input_stamp`)
# live in the host module event_universe.world_files since item 72: the loader
# compares the stamp with the digest handed to it and computes none.


def _profile_and_clock(
    values: object, clock_value: object, shape: Address3, label: str, word: str
) -> tuple[tuple[int, ...], int, tuple[int, int]]:
    """A mode's integer profile over the whole board (a flat list in x-major order, one per Node, not all
    zero) with its clock [a, b], the mode's 2 cos omega as the generator's rational, b at least the
    amplitude (ALGEBRA.md #a-familys-declaration; record 1886): the profile, its amplitude and the clock, each
    defect refused by name; `word` the key the profile was written under."""
    count = int(shape[0]) * int(shape[1]) * int(shape[2])
    if (
        not isinstance(values, list | tuple)
        or len(values) != count
        or any(type(v) is not int for v in values)
    ):
        raise ValueError(
            f"{label}.{word} as a profile must be {count} integers, one per Node of the "
            "board in x-major order"
        )
    profile = tuple(int(value) for value in values)
    if not any(profile):
        raise ValueError(f"{label}.{word} as a profile must not be all zero")
    amplitude = max(abs(value) for value in profile)
    if clock_value is None:
        raise ValueError(
            f"{label}.{word} as a profile needs the mode's `clock` [a, b] beside it (the "
            "generator's rational for 2 cos omega, b at least the amplitude; the loader checks "
            "the profile against the eigen-equation in integers, ALGEBRA.md #a-familys-declaration, record 1886)"
        )
    if (
        not isinstance(clock_value, list | tuple)
        or len(clock_value) != 2
        or any(type(item) is not int for item in clock_value)
        or clock_value[0] < 1
        or clock_value[1] < 1
    ):
        raise ValueError(
            f"{label}.clock must be [a, b], two positive integers, the mode's 2 cos "
            "omega as a rational (ALGEBRA.md #a-familys-declaration)"
        )
    if clock_value[1] < amplitude:
        raise ValueError(
            f"{label}.clock [{clock_value[0]}, {clock_value[1]}]: b must be at least the "
            f"profile's amplitude {amplitude} (the rounding of 2 cos omega to 1 / b at most, "
            "ALGEBRA.md #a-familys-declaration)"
        )
    return profile, amplitude, (int(clock_value[0]), int(clock_value[1]))


def _mode_bodies(
    files: Mapping[str, object], digest: str | None, count: int
) -> tuple[dict[str, object] | None, ...]:
    """The generator's mode file beside the world (`<world>.mode.json`, handed by the host among the files):
    the one handed document carrying `world_digest`, this world's by that digest, its `bodies` one entry per
    measured event in the world's order; None for every body where no mode file was handed."""
    found = [
        document
        for document in files.values()
        if isinstance(document, dict) and "world_digest" in document
    ]
    if not found:
        return tuple(None for _ in range(count))
    if len(found) > 1:
        raise ValueError(
            "two mode files were handed with the world; one mode file stands beside a world"
        )
    mode = found[0]
    if digest is None:
        raise ValueError("the mode file's check needs the world's digest, computed by the host module")
    if mode["world_digest"] != digest:
        raise ValueError(
            f"the mode file's world_digest {mode['world_digest']} is not this world's digest {digest}: "
            "the mode file stands beside another world, or the world changed after the generator wrote it"
        )
    bodies = mode.get("bodies")
    if (
        not isinstance(bodies, list)
        or len(bodies) != count
        or not all(isinstance(b, dict) for b in bodies)
    ):
        raise ValueError(
            f"the mode file's bodies must be {count} objects, one per measured event in the world's order"
        )
    return tuple(bodies)


def _input_stamp_check(
    document: dict[str, object], measured: tuple[MeasuredDefinition, ...], digest: str | None
) -> None:
    """THE FILE'S HASH (the model owner's record 1886; ALGEBRA.md #a-familys-declaration, #the-primitives; BUILD.md section 26 item 28): a world with a seeded body
    carries `stamp` {hash}, the digest of the WHOLE document without `stamp`
    (the generator's stamp over every key, the profiles and the clocks among
    them), so that the file loaded is the one the generator wrote and a file
    changed by hand is regenerated, not run; no law identifier stands beside it
    (one engine, ALGEBRA.md #the-primitives). A world with no profile needs no stamp."""
    seeded = (
        e.block for e in measured if e.block is not None and e.block.nodes is None
    )  # a body by its position
    if not any(block.profile is not None for block in seeded):
        return
    value = document.get("stamp")
    if value is None:
        raise ValueError(
            "the world declares a seeded body and no `stamp`: the generator writes `stamp` "
            '{"hash": ...}, the digest of the whole file (the model owner\'s record 1886; '
            "ALGEBRA.md #a-familys-declaration; BUILD.md section 26 item 28)"
        )
    stamp = _object(value, "stamp", STAMP_KEYS, STAMP_KEYS)
    written = stamp["hash"]
    if not isinstance(written, str):
        raise ValueError("stamp.hash must be a string")
    if digest is None:
        raise ValueError(
            "the stamp's check needs the file's digest, computed by the host module "
            "event_universe.world_files (the loader reads no file and hashes nothing)"
        )
    if written != digest:
        raise ValueError(
            f"stamp.hash {written} is not the digest of the file "
            f"{digest}: the document is not the one the generator stamped (a key changed "
            "after the stamp; the stamp covers the whole file, BUILD.md section 26 item 28; record "
            "1886); regenerate the file"
        )


def _initial_state_checks(
    shape: Address3,
    periodic: tuple[bool, bool, bool],
    families: tuple[FamilyDefinition, ...],
    measured: tuple[MeasuredDefinition, ...],
) -> None:
    """THE INPUT CHECKED LAWFUL OR REFUSED, IN INTEGERS (record 1886; ALGEBRA.md #a-familys-declaration): every
    body's Nodes disjoint from every other body's; for every body seeded with a profile, its clock a / b above
    its kind's band top 2 num / den (a bound mode) and below 2 (stable). The amplitude's bound is checked where
    the body is parsed; the separation rule of 9.35 is retired (ALGEBRA.md #the-primitives)."""
    board = (int(shape[0]), int(shape[1]), int(shape[2]))
    blocks: list[tuple[int, MeasuredDefinition, BlockDefinition, list[int]]] = []
    for number, entry in enumerate(measured):
        block = entry.block
        if block is None:
            continue
        wrap = periodic
        corner = (int(entry.position[0]), int(entry.position[1]), int(entry.position[2]))
        # a cube beyond a face or wrapped onto itself is refused by the fit
        # check on the parsed world (naming the axis and the vertex)
        nodes = body_node_indices(board, corner, block.extents, wrap)
        if block.nodes is not None:
            nodes = [x * board[1] * board[2] + y * board[2] + z for x, y, z in block.nodes]
        own = set(nodes)
        for other_number, _, _, other_nodes in blocks:
            if own.intersection(other_nodes):
                raise ValueError(
                    f"measured[{number}] and measured[{other_number}] overlap: two "
                    "bodies' Nodes are disjoint (ALGEBRA.md #what-a-body-is, #a-familys-declaration)"
                )
        blocks.append((number, entry, block, nodes))
    for number, entry, block, _nodes in blocks:
        if block.profile is None or block.clock is None:
            continue
        family = families[entry.family]
        kind = block.kind  # the body's rest pair (ALGEBRA.md #the-interval; commit 1)
        wrap = periodic
        a, b = block.clock
        # (iii) the band: a / b above the kind's band top 2 num / den and below 2
        if a * kind[1] <= 2 * kind[0] * b:
            raise ValueError(
                f"measured[{number}].clock [{a}, {b}] is not above the band's top "
                f"2 x {kind[0]} / {kind[1]} of the kind of the family {family.name!r}: the "
                "profile is no bound mode (ALGEBRA.md #a-familys-declaration; a well too shallow for its "
                "board, or a mode of the band)"
            )
        if a >= 2 * b:
            raise ValueError(
                f"measured[{number}].clock [{a}, {b}] is at or above 2: the mode is a "
                "runaway (no oscillation, a level growing every interval; ALGEBRA.md #rule3, "
                "ALGEBRA.md #a-familys-declaration)"
            )
        # THE SEPARATION RULE OF 9.35 IS RETIRED (ALGEBRA.md #the-primitives; the one stroke,
        # commit 6): each body's record is its own array and meets another body only
        # through the held families, so two bodies of one family may stand anywhere;
        # the tail check of item 28 is gone


def _connected_pieces(
    positions: list[Address3], shape: Address3, periodic: tuple[bool, bool, bool]
) -> int:
    """The number of pieces of a set of Nodes under the board's Links: two
    Nodes are linked when they differ by one on one axis (modulo the extent
    on a periodic axis); an axis of extent 1 links nothing."""
    remaining = set(positions)
    pieces = 0
    while remaining:
        pieces += 1
        frontier = [remaining.pop()]
        while frontier:
            node = frontier.pop()
            for axis in range(3):
                extent = int(shape[axis])
                if extent < 2:
                    continue
                for step in (1, -1):
                    coordinate = node[axis] + step
                    if periodic[axis]:
                        coordinate %= extent
                    elif not 0 <= coordinate < extent:
                        continue
                    neighbour = list(node)
                    neighbour[axis] = coordinate
                    candidate = (neighbour[0], neighbour[1], neighbour[2])
                    if candidate in remaining:
                        remaining.remove(candidate)
                        frontier.append(candidate)
    return pieces


# THE DETECTOR CUBE (the model owner's word of 2026-09-25, record 1899;
# ALGEBRA.md #the-ladder): a detector is one region, a cube of side 3 or more; its
# sensitivity is its whole cube, read by the flux into it through its Ports
# from outside; the click is the detector's, reported by its name and never
# by a Node. The cube is cut by the GameBoard on an axis whose extent is
# below the side (a chain's or a layer's thin axis), as a block's cube is.
DETECTOR_SIDE = 3


def _box_sides(
    positions: list[Address3], shape: Address3, periodic: tuple[bool, bool, bool]
) -> tuple[int, int, int] | None:
    """The sides of the box a set of Nodes fills, or None where it fills no
    box: per axis the distinct coordinates form one run (the shortest arc
    across a periodic seam) and the count of Nodes is the runs' product."""
    sides: list[int] = []
    for axis in range(3):
        coordinates = sorted({node[axis] for node in positions})
        extent = int(shape[axis])
        if periodic[axis]:
            run = min(max((c - start) % extent for c in coordinates) + 1 for start in coordinates)
        else:
            run = coordinates[-1] - coordinates[0] + 1
        if run != len(coordinates):
            return None
        sides.append(run)
    if sides[0] * sides[1] * sides[2] != len(set(positions)):
        return None
    return (sides[0], sides[1], sides[2])


def _detector_region(
    name: str,
    positions: list[Address3],
    shape: Address3,
    periodic: tuple[bool, bool, bool],
    one_node: bool = False,
) -> None:
    """The three refusals on a detector's Nodes: disconnected pieces (ALGEBRA.md #the-ladder), no box, a side below DETECTOR_SIDE where the GameBoard's extent
    allows it (record 1899). THE ONE-NODE DETECTOR (ALGEBRA.md #what-a-body-is;
    the model owner's word of 2026-09-25 in Nature24's session, "start";
    BUILD.md section 26 item 40; SINCE COMMIT 7 on every world, ALGEBRA.md #the-rows-against-nature, record 2109: several bodies on one Node each are several detectors):
    a detector may be ONE Node, a body's Node, its six Links its Ports (the
    cube's fifty-four HISTORY there, the counts rescaled by the Node's share);
    a set of more than one Node keeps the cube rule."""
    if one_node and len(set(positions)) == 1:
        return
    pieces = _connected_pieces(positions, shape, periodic)
    if pieces > 1:
        raise ValueError(
            f"the receiver {name!r} lies on {pieces} disconnected pieces; a detector "
            "is one connected region, and separate places are separate names (ALGEBRA.md "
            "ALGEBRA.md #the-ladder)"
        )
    sides = _box_sides(positions, shape, periodic)
    if sides is None:
        raise ValueError(
            f"the receiver {name!r} on {len(positions)} Nodes fills no box; a "
            f"detector is one cube of side {DETECTOR_SIDE} or more, its Nodes the whole box of "
            f"its sides, cut by the GameBoard on an axis of extent below {DETECTOR_SIDE} (the "
            "model owner's word of 2026-09-25, record 1899)"
        )
    least = [min(DETECTOR_SIDE, int(shape[axis])) for axis in range(3)]
    if any(sides[axis] < least[axis] for axis in range(3)):
        raise ValueError(
            f"the receiver {name!r} is a box of sides {list(sides)}; a detector is "
            f"one cube of side {DETECTOR_SIDE} or more (at least {least} on this GameBoard), its "
            "sensitivity its whole cube and the click the detector's, never a Node's (the model "
            "owner's word of 2026-09-25, record 1899)"
            + (
                "; a detector is one Node (a body's) or a cube of three or more, nothing between "
                "(ALGEBRA.md #what-a-body-is, #the-rows-against-nature; BUILD.md section 26 item 40; commit 7)"
                if one_node
                else ""
            )
        )


def _detectors(
    value: object,
    shape: Address3,
    periodic: tuple[bool, bool, bool],
    measured: tuple[MeasuredDefinition, ...],
) -> tuple[DetectorDefinition, ...]:
    detectors = cast(
        tuple[dict[str, object], ...], value
    )  # the frame's checked detectors (loader/frame.py, `DETECTOR`)
    at = {entry.position for entry in measured}
    # The Nodes of every body: its declared Nodes in the law's form, else the block centred on its position.
    owned = [
        set(entry.block.nodes)
        if entry.block is not None and entry.block.nodes is not None
        else set(body_nodes(entry.position, entry.span, shape, periodic) or ())
        for entry in measured
    ]
    inside: set[Address3] = set().union(*owned)
    taken: set[Address3] = set()
    found: list[DetectorDefinition] = []
    for index, obj in enumerate(detectors):
        label = f"detectors[{index}]"
        name = obj["name"]
        if not isinstance(name, str) or not name:
            raise ValueError(f"{label}.name must be a nonempty string")
        if any(item.name == name for item in found):
            raise ValueError(f"two detectors named {name!r}")
        if name in FACE_NAMES:
            raise ValueError(
                f"{label}.name {name!r} is the name of a face detector (an open face "
                "of the GameBoard is a detector of that name; declare another)"
            )
        if name == LIFETIME_NAME:
            raise ValueError(
                f"{label}.name {name!r} is the name of the border every event of a "
                "family with a lifetime clicks on; declare another"
            )
        bound_block: int | None = None
        if "block" in obj:
            bound_block = _integer(obj["block"], f"{label}.block", 0, max(0, len(measured) - 1))
            if measured[bound_block].block is None:
                raise ValueError(
                    f"{label}.block {bound_block} names a measured event that is no "
                    "block; a receiver set on a BODY is `positions` on the body's Node "
                    "(DECLARATIONS.md section 15 M1-4)"
                )
        if "positions" not in obj:
            if bound_block is None:
                raise ValueError(f"{label} needs `positions` (or `block`, a set bound to a block)")
            # A BODY IS ITS OWN DETECTOR, whatever its support (ALGEBRA.md #the-rows-against-nature, the
            # detectors' rule approved by the model owner, record 2109: a body of several Nodes is one
            # detector, a body of one Node its own, its six Links its Ports, ALGEBRA.md #what-a-body-is)
            found.append(DetectorDefinition(name, (), 1, block=bound_block))
            continue
        positions_value = obj["positions"]
        if not isinstance(positions_value, list | tuple) or not positions_value:
            raise ValueError(f"{label}.positions must be a nonempty list of Nodes")
        positions: list[Address3] = []
        for item in positions_value:
            position = _address(item, f"{label}.positions", shape)
            if position in taken:
                raise ValueError(f"a Node in two detectors {list(position)}")
            taken.add(position)
            positions.append(position)
        # THE SET'S NODES (ALGEBRA.md #the-ladder): with `block`, free Nodes beside the block (the
        # receiving cube, DECLARATIONS.md section 10 item 9; record 1899) or the block's own Nodes;
        # without it, a body's centre (a body named by its centre) or the Nodes of one body in the
        # law's form, whose set it then is (the strip of a screen)
        own = [number for number, nodes in enumerate(owned) if all(p in nodes for p in positions)]
        if bound_block is not None:
            others = [p for p in positions if p in inside and p not in owned[bound_block]]
            if others:
                raise ValueError(
                    f"{label}.positions with `block` names a Node of another measured event "
                    f"{list(others[0])}: the receiving set is free Nodes beside the block, or its own"
                )
        elif own and (body := measured[own[0]].block) is not None and body.nodes is not None:
            bound_block = own[0]
        else:
            for position in positions:
                if position in inside and position not in at:
                    raise ValueError(
                        f"{label}.positions names a Node of a body on a set "
                        f"{list(position)} that is not its position (a body is one record, "
                        "named by its centre)"
                    )
                if position not in at:
                    raise ValueError(
                        f"{label}.positions names a Node without a measured event "
                        f"{list(position)} (a receiving set at a free Node beside a block declares "
                        "`block` with that one position, DECLARATIONS.md section 10 item 9)"
                    )
        if own == [bound_block]:
            # a set on its body's own Nodes: one connected region, the body's shape its box
            if _connected_pieces(positions, shape, periodic) > 1:
                raise ValueError(f"the receiver {name!r} lies on disconnected Nodes of its body")
        else:
            # THE DETECTOR IS ONE CONNECTED REGION, A CUBE (ALGEBRA.md #the-ladder; record 1899): its
            # Nodes connected by Links (across a periodic seam too), one box, its sides DETECTOR_SIDE
            # or more where the GameBoard's extent allows; separate places are separate names
            _detector_region(name, positions, shape, periodic, one_node=True)
        if name.startswith(RESERVED_SET_PREFIX) or name in FACE_NAMES or name == LIFETIME_NAME:
            raise ValueError(
                f"{label}.name {name!r} is reserved: the layer names the measured "
                f"events outside every detector `{RESERVED_SET_PREFIX}<number>`, the faces and "
                "the border by their own names"
            )
        found.append(DetectorDefinition(name, tuple(positions), 1, block=bound_block))
    return tuple(found)


def _body_fit_check(world: NatureBeamWorld) -> None:
    """A body's cube whole on the board, never cut (the model owner's word of 2026-09-24 through the Boss): on an
    open or closed axis the far vertex is on the board; on a periodic axis the extent is at least the edge (a
    cube across the seam is whole, one wrapped onto itself is not); an axis of extent 1 folds. Refused by name."""
    shape = world.shape
    for number, entry in enumerate(world.measured):
        block = entry.block
        if block is None:
            continue
        wrap = world.kind_periodic(entry.family)
        for axis, name in enumerate(AXES):
            extent = int(shape[axis])
            corner = int(entry.position[axis])
            if extent == 1:
                continue
            side = block.extents[axis]
            if wrap[axis]:
                if extent < side:
                    raise ValueError(
                        f"measured[{number}]: the body of side {side} wraps onto "
                        f"itself on the periodic axis {name} of extent {extent} (a body is a whole "
                        "cube, square or segment on the board, never cut or folded but on an axis "
                        "of extent 1; the model owner's word of 2026-09-24, 16:35Z)"
                    )
            elif corner < 0 or corner + side > extent:
                raise ValueError(
                    f"measured[{number}]: the body of side {side} at {corner} on "
                    f"the axis {name} reaches {corner + side - 1} beyond the face at "
                    f"{extent - 1}: a body lies whole on the board, exactly where it is declared, "
                    "never cut to fit (the model owner's word of 2026-09-24, 16:35Z; move the "
                    "vertex or the edge, or open the axis as periodic)"
                )


def parse_world_document(
    document: object, files: Mapping[str, object], digest: str | None
) -> NatureBeamWorld:
    """Reject anything but a lawful world: the loader reads no file (the host hands it the documents and the digest) and refuses by name a key it does not read, a value outside its bounds and a stamp that is not the generator's."""
    # THE WORLD'S KEYS through the frame (loader/frame.py, `WORLD`): an unknown key, a missing
    # key and a wrong kind refused by name; the universe, the bodies, the detectors, the
    # readings, the records in transit, the covariant readings and an inline twist table
    # handed on as written to their readers below
    obj = frame.world(document)
    # ONE ENGINE (ALGEBRA.md #the-primitives; the model owner's record 2103): every world is the
    # engine's; every branch below on the flag's absence (the ray law's parse) is CANCELLED
    # and unreachable
    word = "universe"
    # THE ENGINE START FILE (ALGEBRA.md #a-familys-declaration): one canonical copy at
    # examples/events/engine_start.json, named by every world by its repository path
    # (`engine`, a required word of the frame's schema) and read by the frame (`START`)
    engine = cast(str, obj["engine"])
    start = frame.start(engine, files)
    step = files.get(STEP_FILE)
    if not isinstance(step, Step):
        raise ValueError(
            f"the step file {STEP_FILE!r} is missing at the repository's root: the interval's order is its"
        )
    families_file: str | None = None
    register = discover()  # the folders' cards, read once for the families' entries and the bodies
    as_written = obj  # the document as the generator stamped it (the universe's path, item 59)
    universe = obj[word]
    obj = dict(obj)
    del obj[word]
    if isinstance(universe, str):
        # THE ONE UNIVERSE FILE (item 59; record 2128 (3)): the path in place of the
        # list; the universe's integers from the file alone, the world's own refused
        families_file = universe
        _refuse_under_law(obj, "the world", set(frame.INTEGERS.keys))
        entries, integers = frame.universe(families_file, files, register)
        obj.update(integers)
    else:
        # the families' list inline (a unit test's world), checked against the cards with
        # the world's own integers
        entries = frame.families(
            universe,
            {key: obj[key] for key in frame.INTEGERS.keys if key in obj},
            register,
            "the world.universe",
        )
    shape_value = cast(tuple[object, ...], obj["shape"])
    extents = tuple(_integer(item, "shape", 1) for item in shape_value)
    shape: Address3 = (extents[0], extents[1], extents[2])
    boundary, periodic = _boundary(obj["boundary"])
    closed = tuple(isinstance(boundary, dict) and boundary.get(axis) == CLOSED_FACE for axis in AXES)
    closed = (closed[0], closed[1], closed[2])
    ticks = _integer(obj["ticks"], "ticks", 0)
    # N declared in every file (no default), a power of two through the universe's `most_steps` where declared
    most_steps = _integer(obj["most_steps"], "most_steps", 2) if "most_steps" in obj else None
    phase_steps = _integer(obj["N"], "N", 2, AMOUNT_BOUND if most_steps is None else most_steps)
    if phase_steps & (phase_steps - 1):
        raise ValueError(
            f"N {phase_steps} must be a power of two from 2 (through the universe's most_steps)"
        )
    # THE FACE SLAB (ALGEBRA.md #the-ladder, the mathematician's reading: a face
    # one Node deep books 0.15 of a packet and reflects the rest, the slab as
    # deep as the packet books 0.96): the receiver `face` at every open
    # border is the slab of this depth, one detector, last on every ladder;
    # REQUIRED on a GameBoard with an open face under the detector law and
    # refused without that law (the slab is its receiver), NO DEFAULT (the
    # model owner's rule through the Boss, 2026-09-25; BUILD.md section 26
    # item 28); 0 on a GameBoard with no open face (no slab)
    open_axes = [name for axis, name in enumerate(AXES) if not periodic[axis] and not closed[axis]]
    if open_axes and "face_depth" not in obj:
        raise ValueError(
            f"face_depth is required on a GameBoard open on {', '.join(open_axes)} "
            "under `detector_law`: the depth of the receiver slab at every open border, no "
            "default (ALGEBRA.md #the-ladder; BUILD.md section 26 item 28)"
        )
    face_depth = _integer(obj["face_depth"], "face_depth", 1) if "face_depth" in obj else 0
    for axis, name in enumerate(AXES):
        if not periodic[axis] and face_depth > 1 and 2 * face_depth >= int(shape[axis]):
            raise ValueError(
                f"face_depth {face_depth} leaves no interior on the open axis {name} of "
                f"extent {shape[axis]} (two slabs of the depth fill it)"
            )
    # THE NODE CLOCK (the model owner's decision (5) of record 1962; ALGEBRA.md
    # ALGEBRA.md #the-paces and (3); BUILD.md section 26 item 31): Gamma, one integer from
    # 1, the clock pair (e, f) = (Gamma, Gamma + M) at every Node under the
    # detector law's rule (M the content held at the Node, 0 in the vacuum);
    # REQUIRED with no default
    if "node_clock" not in obj:
        raise ValueError(
            "node_clock is required: Gamma, the one integer of "
            "the Node clock (e, f) = (Gamma, Gamma + M) at every Node, no default (ALGEBRA.md "
            "ALGEBRA.md #the-paces; BUILD.md section 26 item 31)"
        )
    node_clock = _integer(obj["node_clock"], "node_clock", 1, AMOUNT_BOUND)
    # THE AMPLITUDE BOUND A, derived from the width and the rule's integers of every declared pair at the
    # pace's edge (`derived_amplitude`; ALGEBRA.md #a-familys-declaration: never written, a file's
    # `amplitude_bound` is refused by name as an unknown key)
    amplitude_bound = derived_amplitude(derived.paired(entries, node_clock), obj["measured"], node_clock)
    # THE MOMENTUM'S UNIT Q (ALGEBRA.md #the-primitives, #the-well): the universe's integer
    # `momentum_unit`, REQUIRED with no default (the wall W = 3 Q M of every body)
    if "momentum_unit" not in obj:
        raise ValueError(
            "momentum_unit is required: Q, the momentum's unit "
            "of the universe's integers, the wall W = 3 Q M of every body, no default (ALGEBRA.md "
            "ALGEBRA.md #the-primitives, #the-well; the model owner's record 2089)"
        )
    momentum_unit = _integer(obj["momentum_unit"], "momentum_unit", 1, AMOUNT_BOUND)
    # THE QUANTUM'S ACTION T (ALGEBRA.md #a-familys-declaration; the owner's word of 2026-09-28): one T for
    # every family, the universe's integer `quantum_action`, read where the files declare it and 0 where they
    # do not; the giving's pull request, which retires the emitter's norm, requires it where a body gives
    quantum_action = (
        _integer(obj["quantum_action"], "quantum_action", 1) if "quantum_action" in obj else 0
    )
    # THE WIDTH (Main Loop's ask, 2026-09-27): the universe's `width`, the working integer's bits, is this host's
    if "width" in obj and obj["width"] != MAX_WORK_INT.bit_length():
        raise ValueError(
            f"integers.width {obj['width']} is not this host's working width {MAX_WORK_INT.bit_length()} "
            "bits: the universe's integers are the host's, refused where they differ"
        )
    # THE TWIST TABLE (ALGEBRA.md #the-primitives): the families file's, checked with Gamma and A;
    # admitted on an inline world; an inline world without it has no transport (the
    # engine refuses a nonzero twist naming the Port)
    twist_table: TwistTable | None = None
    if "twist_table" in obj:
        twist_table = _twist_table(obj["twist_table"], "twist_table", amplitude_bound)
    mode_axis: int | None = None
    if "mode_axis" in obj:
        mode_axis = AXES.index(str(obj["mode_axis"]))
    probes: tuple[Address3, ...] = ()
    if "probes" in obj:
        declared_probes = cast(tuple[object, ...], obj["probes"])
        probes = tuple(_address(item, "probes", shape) for item in declared_probes)
    action = None
    most_families = (
        _integer(obj["most_families"], "most_families", 1) if "most_families" in obj else None
    )
    least_residues = (
        _integer(obj["least_residues"], "least_residues", 1) if "least_residues" in obj else None
    )
    families = _families_of(entries, amplitude_bound, most_families, node_clock)
    bound = amplitude_bound
    # THE BODIES AND THE DETECTORS through the frame (loader/frame.py, `BODY`, `DETECTOR`):
    # every key checked with the families known, an unknown key refused by name
    bodies = frame.bodies(obj["measured"], Context(tuple(family.name for family in families)), register)
    measured = _measured(
        bodies,
        shape,
        periodic,
        families,
        phase_steps,
        most_steps,
        ticks,
        action,
        bound,
        momentum_unit,
        least_residues,
        _mode_bodies(files, digest, len(bodies)),
    )
    _held_bodies_checks(families, measured)
    _node_clock_bound(families, measured, node_clock)
    # THE WINDOW IS THE ONE GIVING (ALGEBRA.md #the-primitives; record 2082 (4);
    # commit 7): every emitter declares its weight g and its rung's action; the world
    # key `point_emitter` and the train are retired (RETIRED_KEYS)
    for number, entry in enumerate(measured):
        block = entry.block
        if block is None or block.emitter is None:
            continue
        if block.emitter.weight is None:
            raise ValueError(
                f"measured[{number}].emitter declares no `weight`: the body's rotation is "
                "copied into the given row at its Node at a declared weight g, one integer from 1 "
                "(ALGEBRA.md #the-primitives; commit 7)"
            )
        if block.emitter.norm is not None and block.emitter.norm_denominator is None:
            raise ValueError(
                f"measured[{number}].emitter declares no `norm_denominator`: the window "
                "closes when the outward norm reaches the excitation's action norm / "
                "norm_denominator, the generator's exact rational (ALGEBRA.md)"
            )
    _input_stamp_check(as_written, measured, digest)
    _initial_state_checks(shape, periodic, families, measured)
    detectors = _detectors(frame.detectors(obj["detectors"]), shape, periodic, measured)
    readings = world_readings(obj, shape, detectors, families, measured)
    world = NatureBeamWorld(
        shape,
        boundary,
        periodic,
        ticks,
        phase_steps,
        families,
        measured,
        detectors,
        readings,
        step,
        face_depth=face_depth,
        probes=probes,
        mode_axis=mode_axis,
        closed=closed,
        amplitude_bound=bound,
        node_clock=node_clock,
        momentum_unit=momentum_unit,
        quantum_action=quantum_action,
        twist_table=twist_table,
        start=start,
        universe_file=families_file,
    )
    set_names = {detector.name for detector in detectors}
    for number, entry in enumerate(measured):
        # the emitter body's ladder by name (ALGEBRA.md #the-click): every name a
        # declared set's
        if entry.block is not None and entry.block.emitter is not None:
            for name in entry.block.emitter.receiver or ():
                if name not in set_names:
                    raise ValueError(
                        f"measured[{number}].emitter.receiver names {name!r}, which no "
                        "detector set declares (the record's ladder is made of declared sets; "
                        "a face is never on it)"
                    )
        # the receiver by name (DECLARATIONS.md section 13 item 7): the
        # set named must be declared; the names are listed in the refusal
        if entry.block is not None and entry.block.receiver is not None:
            names_declared = [detector.name for detector in detectors]
            if entry.block.receiver not in names_declared:
                raise ValueError(
                    f"measured[{number}].receiver {entry.block.receiver!r} names no "
                    f"declared detector set (the sets declared: {names_declared}); the receiver "
                    "by name is a set's name (DECLARATIONS.md section 13 item 7)"
                )
    _body_fit_check(world)
    # The push's denominator per column, Lambda_c^2 (`measured.counts_table`),
    # tested where Lambda_c is formed (`column_scales`): a world whose column
    # scales leave the register is refused here, at load, not at its first
    # push (the physics-rule review of the branch, REVIEW.md section 4).
    return world
