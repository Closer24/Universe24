"""The world file translated to the loop's classes: the frame (loader/frame.py) reads the three files through the schemas and hands the checked values here; this module builds the loop's classes from them (NatureBeamWorld, FamilyDefinition, MeasuredDefinition, BlockDefinition, EmitterDefinition, DetectorDefinition, TwistTable), keeps the rules between keys the cards do not state, and runs the loop's load-time checks (the node clock's bound, the held bodies, the initial state, the body's fit); it leaves with the loop's reads of the old form's keys (ALGEBRA.md #the-primitives.90 (1))."""

from __future__ import annotations

import math
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from typing import cast

from event_universe.core.game_board import MAX_VALUE, Address3
from event_universe.core.phase import MAX_PHASE_STEPS
from event_universe.core.readings import Reading, world_readings
from event_universe.core.register import discover
from event_universe.core.rule3 import rule_total_bound
from event_universe.core.schema import Context
from event_universe.core.step import STEP_FILE, Step
from event_universe.loader import frame
from event_universe.loader.frame import EngineStart

# the ray law's table rules, read by the loop's fixed values alone (DEAD, the paper writer's)
TABLES = ("read", "measure", "rerelease", "pass", "become")
# the readings a record may carry (the loop's words)
AGE_READS = "age"
PRESENCE_WORD = "presence"
READS = ("scalar", "outside", "here", "vector", "tensor", AGE_READS, PRESENCE_WORD)
# the one scale Q of the momentum label and the flight's resolution (LABEL_SCALE); the bounds of an amount, a norm and a momentum component on the 64-bit work register
Q = 64
AMOUNT_BOUND = (1 << 62) - 1
NORM_BOUND = (1 << 126) - 1
MOMENTUM_BOUND = (1 << 62) - 1
Vector = tuple[int, int, int]


# the ceiling A of a row's amplitude where a world declares none, and the rule's int64 total
AMPLITUDE_BOUND = 1 << 28
TOTAL_BOUND = 1 << 63
# light's kind: the pair [1, 1], the value every family without a declared pair reads (no branch on a name)
MASSLESS_PAIR = (1, 1)
# a body of one Node
ONE_NODE: tuple[int, int, int] = (1, 1, 1)
# the border's name no detector may take
LIFETIME_NAME = "lifetime"
# the charge per unit of content of a family with none: 0 as the pair [0, 1]
NO_CHARGE = (0, 1)
# at most twenty families on a GameBoard (the model owner's word of 2026-09-25)
MOST_FAMILIES = 20
# the twist table (ALGEBRA.md #the-transport, #the-primitives): unit = 4 Gamma 2^16, 2^10 fine triples, at most 2^15 coarse triples, d at most 10^9
TWIST_UNIT_SCALE = 1 << 16
TWIST_FINE_BITS = 10
TWIST_COARSE_MOST = 1 << 15
TWIST_TRIPLE_BOUND = 10**9
# the three forms of a family's parts (ALGEBRA.md #the-primitives)
PARTS_FORMS = ((1,), (1, 3), (1, 3, 6))


@dataclass(frozen=True)
class TwistTable:
    """THE TWIST TABLE as read (ALGEBRA.md #the-transport, #the-primitives): the unit's
    integer (theta_unit = 1 / unit radians, unit = 4 Gamma 2^16), the fine triples for
    k_0 in [0, 2^10) and the coarse triples for k_1 in [0, bound); the transport's
    triple for |k| = k_1 2^10 + k_0 is their exact product."""

    unit: int
    fine: tuple[tuple[int, int, int], ...]
    coarse: tuple[tuple[int, int, int], ...]


def _twist_table(value: object, label: str, node_clock: int, amplitude_bound: int) -> TwistTable:
    """The twist table read and checked in integers (ALGEBRA.md #the-primitives):
    {unit, fine, coarse}; unit = 4 Gamma 2^16; fine 2^10 triples, coarse from 1 to 2^15;
    each triple three integers, c from 1, s from 0, d from 1 to 10^9 with c^2 + s^2 = d^2,
    the first the angle 0's and the angles never falling along the table (the nearest
    triple of each angle is the generator's number, `generator_numbers.twist_triple`,
    checked by its own test); the product of the largest d of each part times 3 A inside
    int64 (the transport's total)."""
    obj = _object(value, label, {"unit", "fine", "coarse"}, {"unit", "fine", "coarse"})
    unit = _integer(obj["unit"], f"{label}.unit", 1)
    if unit != 4 * node_clock * TWIST_UNIT_SCALE:
        raise ValueError(
            f"{label}.unit {unit} is not 4 Gamma 2^16 = {4 * node_clock * TWIST_UNIT_SCALE}: "
            "theta_unit = 1 / (4 Gamma 2^16) radians per unit of k (ALGEBRA.md #the-primitives)"
        )
    parts: list[tuple[tuple[int, int, int], ...]] = []
    for name, least, most, _step in (
        ("fine", 1 << TWIST_FINE_BITS, 1 << TWIST_FINE_BITS, 1),
        ("coarse", 1, TWIST_COARSE_MOST, 1 << TWIST_FINE_BITS),
    ):
        rows = obj[name]
        if not isinstance(rows, list | tuple) or not least <= len(rows) <= most:
            raise ValueError(
                f"{label}.{name} must be a list of {least} to {most} triples [c, s, d] "
                "(ALGEBRA.md #the-primitives)"
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
            if c < 1 or s < 0 or d < 1 or d > TWIST_TRIPLE_BOUND or c * c + s * s != d * d:
                raise ValueError(
                    f"{where} [{c}, {s}, {d}] is no triple of the table: c from 1, s from 0, "
                    f"d from 1 to {TWIST_TRIPLE_BOUND}, c^2 + s^2 = d^2 exactly (ALGEBRA.md #the-transport)"
                )
            if index == 0 and (c, s, d) != (1, 0, 1):
                raise ValueError(f"{where} [{c}, {s}, {d}] is not the angle 0's triple [1, 0, 1]")
            if triples and s * triples[-1][0] < triples[-1][1] * c:
                # the angles in order: tan (s / c) never falls from one entry to the next
                # (the nearest-triple property is the generator's, checked by its own test)
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
    return TwistTable(unit, parts[0], parts[1])


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
    # the box's extents per axis in place of `side` (the slabs of ALGEBRA.md
    # ALGEBRA.md #a-familys-declaration; BUILD.md section 26 item 23)
    "extents",
    "pair",
    # THE BODY'S KIND (ALGEBRA.md #the-primitives, #the-interval; the one stroke, commit 1):
    # the body's rest pair on a family whose pair is the body's
    "kind",
    # THE BODY'S NUMBERS the holds read (ALGEBRA.md #the-interval; commit 2): its
    # charge Q (`q`), its spin S and its moment mu (the momentum n is `momentum`)
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
    # the excited records in turn on the body's Nodes, each clicking at its
    # own rung, the given record written once by E^T at that interval
    "emitter",
    # detector-law-v1, the receiver by name (DECLARATIONS.md section 13 item
    # 7): an emitting block names the detector set whose one detector is its
    # record's ladder; admitted on an emitting block alone
    "receiver",
    # the stock of the body's own family where its emitter gives it (ALGEBRA.md
    # ALGEBRA.md #the-primitives; commit 6)
    "stock",
}
# a well's margin kind, the loader's rule between keys: a pin world's margins or a control world's
MARGIN_KINDS = ("pin", "control")
# the detector's readings, the loop's words; the first is every detector's (the key is gone)
DETECTOR_READINGS = ("wave", "beam")
SUM_READING = "sum"
# the face detectors' names in Port order, and the prefix of a body's own set; a declared detector takes neither
FACE_NAMES = ("face:+x", "face:-x", "face:+y", "face:-y", "face:+z", "face:-z")
RESERVED_SET_PREFIX = "measured:"
# the GameBoard's axes and the words of a face: open, periodic, or closed (a zero face without the take)
AXES = ("x", "y", "z")
BOUNDARIES = ("open", "periodic")
CLOSED_FACE = "closed"


@dataclass(frozen=True)
class FamilyDefinition:
    """One family of the world: its name, the content of one unit of it per phase step of its emitter's turn (`quantum`, h; 0 for a free family, 1 or more for a paid one: the kind is derived, never declared), its charge (`charge`: for a free family the charge per unit of content, rho, the pair (n, d) with d from 1, a measured event of the family of content M carrying rho x M and its rays pushing a charged reader by rho; for a paid family, since 2026-09-20 (D-1), the whole charge per unit of amount, the pair (c, 1), read on the charge line of the books alone: its rays push by their label and its `charge` column value is (0, 1)), its columns (`columns`: gravity first, charge second, the declared columns after, aligned by index across the families of the world; `charge` is the value of the second for a free family), whether it has a phase circle, the phase steps its rays turn per Link crossed, and its `lifetime` (L, or None for ever: the age at which an event in transit of the family clicks on the border `lifetime` instead of making its next event, the range of the family's force in Links of flight)."""

    name: str
    quantum: int
    charge: tuple[int, int] = NO_CHARGE
    lifetime: int | None = None
    hand: int | None = None
    phase_per_age: tuple[int, int] | None = None
    # The record kind's pair [num, den] on the six-neighbour term of the
    # local detector law's rule (`massive-record-v1`, MASSIVE_RECORD.md
    # section 1): light's kind is the value (1, 1) (every family without
    # the key `pair`); a massive kind declares den > num, its rest
    # frequency cos omega_0 = num / den. Admitted under the world key
    # `massive_record` alone.
    pair: tuple[int, int] = MASSLESS_PAIR
    # THE FAMILY GENERICITY (the model owner's record 2066 of 2026-09-25
    # through the Boss: "the engine does not know the family's name, does not
    # know what the family does; it only supports the family's operations";
    # BUILD.md section 26 item 51). What a family IS is declared here and
    # read by the engine as attributes alone, never by a name or a role:
    # `held`, the source a body's record writes at the body's Nodes at both
    # levels with the remainder 0, "content" (the quanta the body holds, the
    # Node clock's c of ALGEBRA.md #the-counts-line) or "charge" (the signed sum of its
    # quanta, the d of 9.48), None for a family the step alone moves; `reads`,
    # the held families whose levels enter this family's pace at every Node,
    # (family index, weight, by) each, the effective content SUM weight x
    # level for by = "plain" and - q x weight x level for by = "sign" (q the
    # reading family's own charge sign; ALGEBRA.md #the-paces: c - q Lambda d), empty for
    # a held family (the plain rule, the pace 1 of its own); `components`,
    # the representation's count (1 a scalar; 3 and 6 the vector and tensor
    # families of 9.77, not yet built). The sources and the read modes are
    # the operations' words, never a family's name (item 53: "sign", the
    # signed sum of the quanta by the families' declared signs). A held
    # family is booked by no detector and every other family is (`booked`,
    # derived, item 53); a family declares nothing about detectors or
    # emitters: those are the bodies' mechanisms.
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
    """The emitter as a clicking body (ALGEBRA.md #the-click, the mathematician's
    integers of 2026-09-24; LAB_TOOLS.md A.1): on a body of a massive kind
    with its seed (the excited record: the body's seed at both levels) and
    its stock THE GIVEN FAMILY'S CONTENT HELD AT THE BODY, `held` naming the
    given family (ALGEBRA.md #the-paces; BUILD.md section 26 item 47: a giving
    lowers the given family's content by one; the body's own quanta `amount`
    and its charge stay; the stock as `amount` HISTORY), the key
    `emitter`: {"family": the given family's name (a paid family with the
    pair form of its clock), "branches": the given record's labels (optional,
    [[0, 1]] by the lamp's form), "receiver": the given records' ladder by
    name (optional, a list of set names; the block's own `receiver`, one
    name, is the line at the rung), "period": P, the nearest integer to
    2 pi / omega_b of the body's mode (the generator's integer), "norm":
    T, one period's action P e_c: the share of the body's conserved form
    at its centre Node summed over P intervals advanced alone (the
    generator's integer under the input stamp; ALGEBRA.md #the-click and
    (f) in the flux's units of ALGEBRA.md #rule3), "given": the given record's two levels
    over the whole board as material (optional; {"now": [...], "before":
    [...]}, x-major, one per Node; the engine copies them at the click;
    ALGEBRA.md #the-click)}. Without `given` the given record is the pair on every
    Node of the body: now = A C_2N[3 N / 2 + s] on the circle of 2 N steps
    with s = floor(n / d) the given clock's step and before = -now (the
    character half a step either side of its zero, no static part; ALGEBRA.md #the-click); an odd s where 2 N exceeds the tables' bound is refused. Excited
    record k clicks at its own rung (E the one-way flux into its centre
    Node, D the rung 2 T u_k + T <= 2 W C with T its norm); at that click
    X ends it and E^T givings the photon (content one quantum, its residue
    the excitation's) and, while the stock lasts, excited record k + 1. No
    rate, no train, no drive, no source term, no grace."""

    family: int
    branches: tuple[tuple[int, int], ...]
    label_hands: tuple[int, int] | None
    receiver: tuple[str, ...] | None
    # THE GIVEN CLOCK (ALGEBRA.md #the-primitives; item 59): the given record's clock
    # [p, q], the family's own or the emitter's `clock`
    clock: tuple[int, int]
    # THE GIVEN RECORD'S PAIR (ALGEBRA.md #the-primitives, #the-interval; commit 1): the
    # given family's declared pair, or the emitter's own `pair` on a family
    # whose pair is the body's
    pair: tuple[int, int] = MASSLESS_PAIR
    period: int | None = None
    norm: int | None = None
    given: None = None  # the ray law's given train, read by the loop as None (its cancelled branch)
    # THE POINT EMITTER'S NORM DENOMINATOR (ALGEBRA.md; item 50): the
    # excitation's action T as the exact rational norm / norm_denominator,
    # in the form's units, which the window's outward norm is read against;
    # required on every emitter (commit 7: the window the one giving)
    norm_denominator: int | None = None
    # THE POINT EMITTER'S WEIGHT g (ALGEBRA.md; item 50): the
    # body's coupling to the given family, one integer, the body's Node's rotation
    # copied at that weight into the given row at the body's Node every interval of
    # the window; required on every emitter (commit 7: the window the one giving)
    weight: int | None = None
    # THE GIVEN RECORD'S COMPONENT (ALGEBRA.md #the-second-level, #the-interval; commit 4): the
    # index in the given family's parts, 0 on a scalar family, 1 + the axis of the
    # body's moment on a vector family (the component along mu)
    part: int = 0
    # THE GIVEN RECORD'S TWIST "OWN" (ALGEBRA.md #the-primitives; commit 4): round(2^16
    # omega_0), the record's rest rotation from its pair (a massive kind) or from its
    # wavelength on light's dispersion (a train) or its emitter's rotation (a window)
    twist: int = 0


@dataclass(frozen=True)
class BlockDefinition:
    """A block, the foreign object of the massive record kind
    (`massive-record-v1`, MASSIVE_RECORD.md sections 4 to 7): its Nodes R
    the box of `extents` per axis (the cube of `side` the shorthand for
    equal extents; the slabs of ALGEBRA.md #a-familys-declaration, BUILD.md section 26
    item 23) with its lower corner at the measured event's `position`,
    cut to the board on an open axis and wrapped on a periodic one; its `pair` on the six-neighbour term at its Nodes (a WELL of the
    massive kind's pair, `num' / den' > num / den`; on light's kind a gap,
    the (M) wall); the
    `seed` of its own record on its Nodes at interval 0 (0: silent; declared,
    no default, BUILD.md section 26 item 28); `ramp`
    (the pushing agent's declaration: its momentum reached from 0 over that
    many intervals); `start` (the same agent's: the interval its drive
    begins, 0 by default, the ramp counted from it); `margin` (the margin
    rule's kind of world, a well's; None on a body that is no well). The take (`absorbing`, `take`), the cycle
    emitter (`emits`, `own_grace`) and a declared wheel are retired
    (BUILD.md section 26 items 14 and 15)."""

    side: int
    pair: tuple[int, int]
    # THE BODY'S KIND (ALGEBRA.md #the-primitives, #the-interval): the rest pair of the body's own record, its family's declared pair or, on a family whose pair is the body's, the body's own `kind`
    kind: tuple[int, int]
    # the well's own record's amplitude on its Nodes at interval 0 (0 silent), or its profile's; declared in the file, no default (the model owner, 2026-09-25; BUILD.md section 26 item 28)
    seed: int
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
    # THE PROPER PAIR OF A MOVING BODY ON ONE NODE (ALGEBRA.md #the-velocity; BUILD.md section 26
    # item 46): the pairs [num_m, b] the body's Node rotates at while the drive's
    # momentum is m, indexed by m from 0 (the clock itself) to |P| along the
    # one axis of the declared momentum, the generator's reading of the moving
    # mode at its moving centre, 2 cos(omega_K - K v) at v = m / (3 Q M); None on a body at rest
    proper_clock: tuple[tuple[int, int], ...] | None = None
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
    # detector-law-v1, the receiver by name (DECLARATIONS.md section 13 item
    # 7, the click line): the name of the detector set whose one detector is the
    # ladder of every record this block emits (the click line at that detector's
    # first rung after the record's train; the faces and every other set
    # sinks for it); None where the world names none, the ladder then every detector and the line at the close, as before the key.
    receiver: str | None = None
    # the emitter as a clicking body (ALGEBRA.md #the-click): None on a body that emits nothing by the click
    emitter: EmitterDefinition | None = None
    # THE STOCK OF THE BODY'S OWN FAMILY (ALGEBRA.md #the-primitives; commit 6): the count of
    # its own quanta set aside for giving where its emitter gives its own family, 0 elsewhere (another family's stock is the body's `held` quanta of it)
    stock: int = 0


@dataclass(frozen=True)
class MeasuredDefinition:
    """One measured event as declared: its Node, its family, its amount, its
    phase, its momentum, whether it is held in place, the directions it
    releases and re-emits on, its table per family (in family order) with
    the phase window and the reading key of each entry, and its lamp. Its
    charge is its family's charge per unit of content times its content
    and is not declared. `span` is the set of Nodes it is a body on (three
    odd extents centred on `position`, (1, 1, 1) for one Node),
    `phase_by_momentum` whether it turns its phase by its momentum label
    at every Link it steps (over the world's `action`), and `held` the
    content it holds per family in family order at the start: its
    `amount` under its own family and what `held` declared of the others
    (the ray law's table, one rule per family, `measure` with the scalar
    component: no family is free, the row's quantum is from 1). `window_reads` is, per family in family order, the window
    read from a reading (issue #363): the index of the family whose rows
    at the set give the centre and the offset, or None for a declared or
    absent centre (`windows` then holds the number, or None)."""

    position: Address3
    family: int
    amount: int
    phase: int
    momentum: Vector
    momentum_before: Vector
    fixed: bool
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
    age_bound: int
    families: tuple[FamilyDefinition, ...]
    measured: tuple[MeasuredDefinition, ...]
    detectors: tuple[DetectorDefinition, ...]
    readings: tuple[Reading, ...]
    step: Step
    # The clock stamp (the world key `clock_stamp`, false by default): every
    # line a measured event writes carries `clock`, its own count of
    # self-creations; a record field, no physics, no hypothesis.
    clock_stamp: bool = False
    # the face receiver's depth at every open border (ALGEBRA.md #the-ladder),
    # declared in the file under the detector law (no default, BUILD.md
    # section 26 item 28); 0 on a GameBoard with no open face (no slab)
    face_depth: int = 0
    # massive-record-v1 (2026-09-23): the massive record kind beside light
    # under the local detector law, false by default; under it a family may
    # declare its `pair`; its faces are the world's.
    massive_record: bool = False
    # THE BODY RECORD (ALGEBRA.md #what-a-body-is to (3); BUILD.md section 26 item
    # 37): true holds every seeded block as one rotation on its clock pair
    # (a Node with a shape), its profile read and never stepped; false, the
    # default, the lattice body (its own rows on the GameBoard)
    body_record: bool = False
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
        """CANCELLED (ALGEBRA.md #the-primitives): the identities of the physical hypotheses
        a world of the ray law declared beside it, in a fixed order, now an empty
        list on every world (one engine, no identity); the order as it stood: `bohr-v1` for the turn by momentum
        (`action`), `columns-v1` for the one mechanism of the columns (a
        column beyond `charge`, or a lifetime: a force of nature in this
        law is a column with a sign and a range), `weak-v1` for the
        transformation `become` (the weak force in the world's terms),
        `meeting-v1` and `amplitude-v1` for their keys, `massive-rows-v1`
        for the world key `massive_rows` (the massive rows beside the law),
        `hand-v1` when the world declares a hand or an axis,
        `covariant-readings-v1` when the world declares `covariant_readings`,
        `optical-v1` for the world key `optical`, `drive-b-v1` for the world
        key `drive_b` (the directional drive of a body), `flow-link-v1` for
        the world key `flow_link` (the flow label per Euclidean Link),
        `centred-step-v1` for the world key `centred_step` (the body's step at
        half the wall) and, last,
        `binding-v1` when a measured event holds a paid family (`binding`;
        the engine appends it at the same place from the first give of a
        run, `NatureBeamSimulation.hypotheses`)."""
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


def _pair_bound(
    numerator: int,
    denominator: int,
    label: str,
    bound: int = AMPLITUDE_BOUND,
    node_clock: int = 1,
    content: int = 0,
) -> None:
    """The load bound of a pair (Reviewer 3's MUST 3) under the Node clock
    (ALGEBRA.md #the-line, #the-rows-against-nature; BUILD.md section 26 items 31, 34 and 44):
    the weak-field rule's total at a Node under the amplitude bound A (the
    world's `amplitude_bound`), 6 A R + A |S| + w (A + 1) with the rule's
    integers (R, S, w) at the vacuum's level and at the content M, below
    2^63, Gamma the world's `node_clock` and M the content at the Node (the
    world's whole content at the second pass, `_node_clock_bound`; the plain
    rule at Gamma = 1 and M = 0, the first pass on the pair alone); refused
    otherwise naming the bound, the clock, the content and the pair."""
    # THE BOUND FROM THE RULE'S OWN INTEGERS (ALGEBRA.md #the-line, #the-rows-against-nature;
    # BUILD.md section 26 item 44): 6 A R + A |S| + w (A + 1) with (R, S, w)
    # the weak-field rule's coefficients at the level 0 and at the level M
    # (the two levels a Node can read: the vacuum's and a body's), the larger;
    # the plain rule's at Gamma = 1 on the first pass over the pair alone
    # the level a Node can read stays below Gamma (the pace positive: the load's guard per
    # body, `_node_clock_bound`, and the run's, `_advance_fields`), so the reach is read there
    weak_field = node_clock > 1
    reach = min(content, node_clock - 1) if weak_field else content
    total = max(
        rule_total_bound(numerator, denominator, node_clock, level, bound, weak_field)
        for level in (0, reach)
    )
    if total >= TOTAL_BOUND:
        raise ValueError(
            f"{label}.pair [{numerator}, {denominator}]"
            + ": the rule's total 6 A R + A |S| + w (A + 1) at the amplitude bound A = "
            f"{bound}, the Node clock Gamma = {node_clock} and the content M = {content} (read at "
            f"the level {reach}) is {total}, not below 2^63 (the bound of the rows' int64; ALGEBRA.md #the-line and "
            "ALGEBRA.md #the-rows-against-nature, BUILD.md section 26 item 44)"
        )


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
    amplitude_bound: int,
    node_clock: int,
) -> None:
    """THE LOAD BOUND UNDER THE NODE CLOCK (BUILD.md section 26 item 31), the
    second pass once the content is known: every family's pair and every
    block's pair against the rule's int64 total at the amplitude bound with
    the world's Gamma and M twice its whole content (the sum of every
    measured event's held quanta of every family is the most any one Node
    can hold, since the clicks move the quanta between the bodies and the
    givings return them to the board; the family of clicks' level around the
    bodies is bounded by the held content, and a wave of it off a zero face
    doubles, ALGEBRA.md #the-counts-line; BUILD.md section 26 item 32)."""

    # THE READS (ALGEBRA.md #the-counts-line, #the-paces; BUILD.md section 26 items 34,
    # 35 and 51): a family reads the pace Gamma - SUM weight x sign x level
    # over its reads; at a body's Nodes a held level is the body's source
    # (its content for "content", its signed charge for "charge"), so the
    # effective content a family reads there in size is at most SUM weight x
    # |source|, positive at the load at every body (the run's guard,
    # `_advance_fields`, holds it everywhere afterwards); the rows' int64
    # bound takes the reach of the effective content, twice the world's
    # sources weighted by the largest reads
    def source_of(family: FamilyDefinition, entry: MeasuredDefinition) -> int:
        quanta = sum(entry.held)
        if family.held == "sign":
            declared = entry.block.q if entry.block is not None else 0
            return abs(
                declared
                + sum(other.charge[0] * held for other, held in zip(families, entry.held, strict=True))
            )
        return quanta

    for number, entry in enumerate(measured):
        for family in families:
            reach = sum(
                weight * source_of(families[other], entry) for other, weight, _, _ in family.reads
            )
            if family.reads and reach >= node_clock:
                raise ValueError(
                    f"measured[{number}]: the pace of {family.name!r} could reach 0 at its "
                    f"Nodes: its reads weigh the body's sources to {reach} in size, not below Gamma = "
                    f"{node_clock} (ALGEBRA.md #the-paces: the charge's hill hastens a clock at most to "
                    "the vacuum's; BUILD.md section 26 items 34, 35 and 51)"
                )
    content = 0
    for family in families:
        reach = 2 * sum(
            weight * source_of(families[other], entry)
            for other, weight, _, _ in family.reads
            for entry in measured
        )
        content = max(content, reach)
    for index, family in enumerate(families):
        if family.pair_on_body:
            continue  # the bodies' kinds are read below (ALGEBRA.md #the-interval)
        _pair_bound(
            family.pair[0], family.pair[1], f"families[{index}]", amplitude_bound, node_clock, content
        )
    for number, entry in enumerate(measured):
        if entry.block is not None:
            _pair_bound(
                entry.block.pair[0],
                entry.block.pair[1],
                f"measured[{number}]",
                amplitude_bound,
                node_clock,
                content,
            )
            if families[entry.family].pair_on_body:
                _pair_bound(
                    entry.block.kind[0],
                    entry.block.kind[1],
                    f"measured[{number}].kind",
                    amplitude_bound,
                    node_clock,
                    content,
                )


def _families_of(
    entries: tuple[dict[str, object], ...],
    age_bound: int,
    massive_record: bool,
    amplitude_bound: int,
) -> tuple[FamilyDefinition, ...]:
    """The loop's families from the frame's checked entries (the cards' keys, the frame's name and clock), with the rules between keys the cards do not state: at most twenty families, no name twice, the three forms of parts, the pair under the world key massive_record with its bound and den >= num, the clock's pair [p, q] with q from 1 and p bounded by the world's largest age, the quantum on every row and the clicks card's copy equal to it, the held source's factors one per part, its dipole on a vector family with its divisor, spins_step on the family that holds the spin's dipole and no other, the self-source's unit 0 or at least 24 A, a family held, clicking or sourced, a read naming a held family once, and a held family's shape."""
    if len(entries) > MOST_FAMILIES:
        raise ValueError(
            f"families declares {len(entries)}; at most {MOST_FAMILIES} families on a "
            "GameBoard (the model owner's record 2081 of 2026-09-25: every family works in every "
            "experiment, the cap 20; record 1875's unification and its counts HISTORY)"
        )
    names: list[str] = []
    for obj in entries:
        name = cast(str, obj["name"])
        if name in names:
            raise ValueError(f"two families named {name!r}")
        names.append(name)
    found: list[FamilyDefinition] = []
    for index, obj in enumerate(entries):
        label = f"families[{index}]"
        parts_value = cast(tuple[object, ...], obj["parts"])
        if parts_value not in PARTS_FORMS:
            raise ValueError(
                f"{label}.parts must be one of {[list(form) for form in PARTS_FORMS]}: the "
                "representation as a list of parts, the time part first (ALGEBRA.md #the-primitives, #the-interval)"
            )
        parts = tuple(int(part) for part in parts_value)
        levels = cast(int, obj["phase"])
        if not massive_record:
            raise ValueError(
                f"{label}.pair is refused without the world key `massive_record` "
                f"(the world key `massive_record`, absent by default)"
            )
        pair_value = obj["pair"]
        pair_on_body = pair_value == "body"
        pair = MASSLESS_PAIR
        if not pair_on_body:
            pair_list = cast(tuple[int, int], pair_value)
            numerator, denominator = int(pair_list[0]), int(pair_list[1])
            if numerator > MAX_VALUE or denominator > MAX_VALUE:
                raise ValueError(f"{label}.pair must be [num, den], two integers up to {MAX_VALUE}")
            _pair_bound(numerator, denominator, label, amplitude_bound)
            if denominator < numerator:
                raise ValueError(
                    f"{label}.pair [{numerator}, {denominator}]: a kind's pair has den >= num "
                    "(den > num a massive kind, its gap cos omega_0 = num / den; den = num light's kind)"
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
            # the walk forms (age + 1) x p whole (`by_clock_rows`): bounded here by the world's largest age
            if clock[0] > AMOUNT_BOUND // (age_bound + 1):
                raise ValueError(
                    f"{label}.clock [{clock[0]}, {clock[1]}]: (age_bound + 1) x p "
                    f"= {age_bound + 1} x {clock[0]} exceeds the integer bound {AMOUNT_BOUND}"
                )
        sign = cast(int, obj["sign"])
        held: str | None = None
        held_factors: tuple[int, ...] = tuple(1 for _ in parts)
        held_dipole: str | None = None
        held_dipole_div = 1
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
                divisor = cast(int, source["dipole_div"])
                held_dipole_div = divisor
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
        if 0 < self_unit < 24 * amplitude_bound:
            raise ValueError(
                f"{label}.self_source.unit {self_unit} is below 24 A = {24 * amplitude_bound}: the "
                "self-source's unit P_2 is 0 (off) or at least 24 A (ALGEBRA.md #the-interval)"
            )
        clicks: tuple[bool, bool] | None = None
        # THE FAMILY'S QUANTUM (the law's owner's row of 2026-09-27; the Boss's word of
        # 09:27Z): one integer from 1 on every row, required; the clicks card's copy agrees
        quantum = cast(int, obj["quantum"])
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
                lifetime=cast(int | None, obj.get("lifetime")),
                hand=cast(int | None, obj.get("hand")),
                phase_per_age=clock,
                pair=pair,
                held=held,
                reads=tuple(reads),
                parts=parts,
                levels=levels,
                held_factors=held_factors,
                held_dipole=held_dipole,
                held_dipole_div=held_dipole_div,
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


HELD_SOURCES = ("content", "sign")
# a read's word `by` in the file (1 plain, "q" by the reading family's own sign) to the loop's word
READ_BY: dict[object, str] = {1: "plain", "q": "sign"}


def _held_family_shapes(families: tuple[FamilyDefinition, ...]) -> None:
    """A held family's shape by attribute (ALGEBRA.md #a-familys-declaration; item 51):
    its field steps at the pair its row declares, [1, 1] or any other (no
    shortcut: the model owner, 2026-09-27), the quantum 1 (one click writes
    one unit), no clock of its own (it givings nothing), its own charge 0 (its
    level is the source it holds, it carries none); a read names a held family;
    under the detector law at most one family holds each source (the level
    every other family reads is one array)."""
    for index, family in enumerate(families):
        label = f"families[{index}] ({family.name!r})"
        if family.held is not None:
            if family.quantum != 1:
                raise ValueError(
                    f"{label} is held with the quantum {family.quantum}: a held family "
                    "is counted in quanta, one click one unit (`quantum` 1; ALGEBRA.md #the-counts-line)"
                )
            if family.phase_per_age is not None:
                raise ValueError(
                    f"{label} is held and declares a clock: a held family "
                    "givings nothing and has no clock of its own (ALGEBRA.md #the-counts-line)"
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
    for source in HELD_SOURCES:
        holders = [family.name for family in families if family.held == source]
        if len(holders) > 1:
            raise ValueError(
                f"two families hold {source!r}: {holders}; one family holds each "
                "source (the level the others read is one array; BUILD.md section 26 item 51)"
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
    massive_record: bool,
    lamp_declared: bool,
    span: tuple[int, int, int],
    shape: Address3,
    amplitude_bound: int = AMPLITUDE_BOUND,
    phase_steps: int = 64,
    periodic: tuple[bool, bool, bool] = (True, True, True),
) -> BlockDefinition | None:
    """The block's keys on a measured event (`massive-record-v1`), each named
    in its refusal: `side` makes a block; every other block key without
    `side` is refused; a block needs the world key `massive_record`, no lamp
    and no span; its `pair` is a well on the massive kind (num' / den' >
    num / den) or a gap on light's kind (den' > num', the (M) wall, which
    declares no clock, seed or margin); an emitter's
    giving Node carries a rich pair (at least 500 remainder values, ALGEBRA.md #a-familys-declaration); the momentum is bounded by the pace, 3 (P . P) < (3 Q M)^2 (the wall W
    = 3 Q M of ALGEBRA.md #the-primitives, Q the universe's `momentum_unit`)."""
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
    if not massive_record:
        raise ValueError(
            f"{label}.side is refused without the world key `massive_record` "
            f"(the world key `massive_record`, absent by default)"
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
    # the load bound of MUST 3 on the block's own pair at its Nodes (decision (2) of record 1962)
    _pair_bound(pair[0], pair[1], label, amplitude_bound)
    if "seed" not in obj:
        # NO IMPLICIT SEED (the model owner, 2026-09-25; BUILD.md section 26 item 28)
        raise ValueError(
            f"{label} lacks keys: seed (a well's own record on its Nodes: its "
            "amplitude at interval 0, 0 silent, or its profile with `margin`; no default, "
            "BUILD.md section 26 item 28)"
        )
    seed: int
    profile: tuple[int, ...] | None = None
    if isinstance(obj["seed"], list | tuple):
        # The bound mode's integer profile over the whole board (MASSIVE_RECORD.md
        # section 11 item 7: the pin worlds' seed, the generator's integers, the
        # same at both levels; admitted with `margin` declared): a flat list of
        # integers in x-major order, one per Node.
        if "margin" not in obj:
            raise ValueError(f"{label}.seed as a profile is admitted only with margin declared")
        values = obj["seed"]
        count = int(shape[0]) * int(shape[1]) * int(shape[2])
        if len(values) != count or any(type(value) is not int for value in values):
            raise ValueError(
                f"{label}.seed as a profile must be {count} integers, one per Node of the "
                "board in x-major order"
            )
        profile = tuple(int(value) for value in values)
        if not any(profile):
            raise ValueError(f"{label}.seed as a profile must not be all zero")
        seed = max(abs(value) for value in profile)
    else:
        seed = _integer(obj["seed"], f"{label}.seed", 0)
    # THE MODE'S CLOCK (ALGEBRA.md #a-familys-declaration; record 1886): a profile carries
    # its mode's 2 cos omega as the rational [a, b] the generator wrote, b at
    # least the amplitude; the world's integer check of the profile against
    # the eigen-equation reads it (`_initial_state_checks`)
    clock: tuple[int, int] | None = None
    if "clock" in obj:
        if profile is None:
            raise ValueError(
                f"{label}.clock is admitted only beside a profile (the mode's 2 cos "
                "omega belongs to the mode's integers, ALGEBRA.md #a-familys-declaration)"
            )
        value = obj["clock"]
        if (
            not isinstance(value, list | tuple)
            or len(value) != 2
            or any(type(item) is not int for item in value)
            or value[0] < 1
            or value[1] < 1
        ):
            raise ValueError(
                f"{label}.clock must be [a, b], two positive integers, the mode's 2 cos "
                "omega as a rational (ALGEBRA.md #a-familys-declaration)"
            )
        if value[1] < seed:
            raise ValueError(
                f"{label}.clock [{value[0]}, {value[1]}]: b must be at least the "
                f"profile's amplitude {seed} (the rounding of 2 cos omega to 1 / b at most, "
                "ALGEBRA.md #a-familys-declaration)"
            )
        clock = (int(value[0]), int(value[1]))
    elif profile is not None:
        raise ValueError(
            f"{label}.seed as a profile needs the mode's `clock` [a, b] beside it (the "
            "generator's rational for 2 cos omega, b at least the amplitude; the loader checks "
            "the profile against the eigen-equation in integers, ALGEBRA.md #a-familys-declaration, record 1886)"
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
            extents=extents,
            periodic=periodic,
            momentum=momentum,
            moment=moment,
            clock_pair=clock,
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
        # THE RICHNESS OF THE GIVING NODE (ALGEBRA.md #a-familys-declaration; BUILD.md section
        # 26 item 15): the residue from the law takes 3 den / gcd(num, 3 den)
        # values on the pair at the body's centre Node (its own pair), at
        # least 500 of them ([801, 700] gives 700, [800, 801] 2403; [8, 7]
        # 21 and [800, 800] 3 are refused)
        residues = 3 * pair[1] // math.gcd(pair[0], 3 * pair[1])
        if residues < 500:
            raise ValueError(
                f"{label}.emitter: the body's pair [{pair[0]}, {pair[1]}] gives "
                f"{residues} remainder values at the giving Node (3 den / gcd(num, 3 den)), below "
                "500: the residue from the law needs a rich pair (ALGEBRA.md #a-familys-declaration; [801, 700] "
                "on the kind [7, 8] gives 700, [800, 801] on [800, 809] gives 2403)"
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
    extents: tuple[int, int, int] = (1, 1, 1),
    periodic: tuple[bool, bool, bool] = (True, True, True),
    momentum: tuple[int, ...] = (0, 0, 0),
    moment: tuple[int, int, int] = (0, 0, 0),
    clock_pair: tuple[int, int] | None = None,
) -> EmitterDefinition:
    """The `emitter` object of a clicking body (ALGEBRA.md #the-click to (6),
    ALGEBRA.md #a-familys-declaration): the given family a paid family with the pair form of its
    clock (not the body's own), the given labels, the ladder by name, the
    period and the norm (the generator's integers), the given profile
    (material). No wheel, no residue order and no seed: the residue is the
    law's (the clicking record's remainder at the giving Node, the wheel the
    pair's), and the keys are refused by name."""
    obj = cast(dict[str, object], value)  # the frame's checked emitter (loader/frame.py, `EMITTER`)
    name = obj["family"]
    if not isinstance(name, str) or name not in names:
        raise ValueError(f"{label}.family names an unknown family")
    given_family = families[names[name]]
    # a body may give its own family (ALGEBRA.md #the-primitives; commit 6): the given record
    # carries the emitter's declared pair, the stock is the body's `stock` of its own quanta
    # THE GIVEN RECORD'S PAIR (ALGEBRA.md #the-primitives, #the-interval): the emitter's
    # `pair` [num, den], required when the given family's pair is the body's
    # and refused when the family declares one (one copy)
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
    # THE GIVEN CLOCK (ALGEBRA.md #the-primitives; item 59): a light record's clock is its
    # emitter's, `clock` [p, q] on the emitter, REQUIRED when the given family
    # declares none (the families file's light) and refused when it does (one copy)
    if "clock" in obj:
        if given_family.phase_per_age is not None:
            raise ValueError(
                f"{label}.clock is refused: the given family {name!r} declares its own "
                "clock (phase_per_link); one copy (ALGEBRA.md #the-primitives)"
            )
        clock = _ratio(obj["clock"], f"{label}.clock", zero=False)
    elif given_family.phase_per_age is not None:
        clock = (int(given_family.phase_per_age[0]), int(given_family.phase_per_age[1]))
    else:
        raise ValueError(
            f"{label}.clock is required: the given family {name!r} declares no clock, so "
            "the emitter declares the given record's clock [p, q] (ALGEBRA.md #the-primitives; BUILD.md "
            "section 26 item 59)"
        )
    step = clock[0] // clock[1]
    if step % 2 == 1 and 2 * phase_steps > MAX_PHASE_STEPS:
        raise ValueError(
            f"{label}.family {name!r}: the given clock's step floor(n / d) = {step} is "
            f"odd and the write's circle of 2 N = {2 * phase_steps} steps exceeds the tables' bound "
            f"{MAX_PHASE_STEPS} (ALGEBRA.md #the-click); declare an even step or a smaller N"
        )
    branches: tuple[tuple[int, int], ...] = ((0, 1),)
    label_hands: tuple[int, int] | None = None
    receiver = _receiver_names(obj, label)
    period = None if "period" not in obj else _integer(obj["period"], f"{label}.period", 1)
    # THE POINT EMITTER'S WEIGHT (ALGEBRA.md; item 50): an integer from
    # 1; the world's `point_emitter` key pairs it with the absence of a train
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
    # THE GIVEN RECORD'S TWIST "OWN" (ALGEBRA.md #the-primitives; item 73): the generator's
    # integer declared under `twist` (a massive kind's rest rotation from its pair, or
    # the emitting body's own rotation where the window writes it, ALGEBRA.md #the-primitives), no default
    twist = _integer(obj["twist"], f"{label}.twist", 0)
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
        twist=twist,
    )


def _measured(
    value: object,
    shape: Address3,
    periodic: tuple[bool, bool, bool],
    families: tuple[FamilyDefinition, ...],
    phase_steps: int,
    ticks: int,
    action: int | None,
    massive_record: bool = False,
    amplitude_bound: int = AMPLITUDE_BOUND,
    momentum_unit: int = 0,
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
            raise ValueError(
                f"{label} is a body in the law's form (its Nodes with their counts): "
                "the loop reads a body by its position until the count's line is bound to it"
            )
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
        fixed = cast(bool, obj["fixed"])
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
            massive_record,
            False,
            span,
            shape,
            amplitude_bound,
            phase_steps,
            periodic,
        )
        found.append(
            MeasuredDefinition(
                position,
                family,
                amount,
                phase,
                (momentum[0], momentum[1], momentum[2]),
                (momentum_before[0], momentum_before[1], momentum_before[2]),
                fixed,
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


def _detector_law_load_checks(
    measured: tuple[MeasuredDefinition, ...],
    families: tuple[FamilyDefinition, ...],
    periodic: tuple[bool, bool, bool],
    phase_steps: int,
) -> None:
    """The instruments of the ray law (cancelled, ALGEBRA.md #the-primitives)
    are refused, naming the rule: a lamp's `turns` (a fan of directions
    with phases; the lamp inserts at its Nodes by its clock), a measured
    event's fan `table` (an opening is free Nodes); and every paid family
    needs the pair form of `phase_per_link`, its clock."""
    for number, entry in enumerate(measured):
        if entry.lamp is not None and any(entry.lamp.turns):
            raise ValueError(
                f"measured[{number}].lamp.turns is refused "
                "(a lamp inserts at its Nodes by its clock; there is no fan)"
            )
        # A split with `inputs` is the TABLE form's splitter (build 2, component
        # 3: the split's integer matrix on the record's read phase, the outputs
        # re-emitted at the table's output Nodes); a split without inputs is
        # an opening's fan, refused under the rule.
        if any(split is not None and split.inputs is None for split in entry.splits):
            raise ValueError(
                f"measured[{number}] declares a fan (a rerelease split with weights and "
                f"no inputs), refused (an opening is free Nodes; there is "
                "no fan; a splitter declares its inputs)"
            )
    # A family of records may declare no clock of its own (ALGEBRA.md #the-primitives;
    # item 59): its emitters declare the given record's clock (`_emitter`); a
    # held family gives nothing and has no clock (ALGEBRA.md #the-counts-line; item 51)
    for number, entry in enumerate(measured):
        # A matter lamp (a lamp on a massive kind): the lamp verb is the same
        # verb, the family's clock the pair form; a massive kind without a
        # clock is a block's kind (its record a block's own or a block's
        # response) and a lamp on it has no clock to drive.
        family = families[entry.family]
        if entry.lamp is not None and family.massive_kind and family.phase_per_age is None:
            raise ValueError(
                f"measured[{number}].lamp on the massive kind {family.name!r} needs the "
                f"pair form of phase_per_link on the family under `massive_record` (the clock "
                "the lamp drives; the train carries the kind's band at it)"
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


def six_neighbours_flat(
    values: Sequence[int], shape: tuple[int, int, int], wrap: tuple[bool, bool, bool]
) -> list[int]:
    """S_6 of a flat x-major integer array in exact integers: the sum of the
    six neighbours, a periodic axis wrapped (an axis of extent 1 reads the
    Node itself twice), an open axis reading 0 beyond its faces; the read of
    the law's rule and of the generator's iteration (ALGEBRA.md #a-familys-declaration)."""
    extents = (int(shape[0]), int(shape[1]), int(shape[2]))
    strides = (extents[1] * extents[2], extents[2], 1)
    total = [0] * len(values)
    for axis in range(3):
        extent, stride = extents[axis], strides[axis]
        for index, value in enumerate(values):
            coordinate = (index // stride) % extent
            for step in (1, -1):
                neighbour = coordinate + step
                if wrap[axis]:
                    neighbour %= extent
                elif not 0 <= neighbour < extent:
                    continue
                total[index + (neighbour - coordinate) * stride] += value
    return total


def mode_residual(
    profile: Sequence[int],
    num: Sequence[int],
    den: Sequence[int],
    clock: tuple[int, int],
    shape: tuple[int, int, int],
    wrap: tuple[bool, bool, bool],
    where: Sequence[bool] | None = None,
) -> tuple[int, int, tuple[int, int, int]]:
    """THE EIGEN-EQUATION'S RESIDUAL IN INTEGERS (ALGEBRA.md #a-familys-declaration,
    PROVED there as the bound for the rounded profile of an exact mode): at
    every Node i of `where` (every Node by default) the residual
    abs(b num_i (S_6 p)_i - 3 den_i a p_i) against the bound b (3 num_i + 6
    den_i), the clock [a, b] the mode's 2 cos omega as a rational; the
    Node of the largest excess with its residual and its bound (the
    residual at or below the bound everywhere means the profile is the
    operator's mode to within its rounding). Exact Python integers, the
    same on every host; the arrays flat in x-major order."""
    a, b = clock
    read = six_neighbours_flat(profile, shape, wrap)
    worst_index, worst_excess, worst_residual, worst_bound = 0, None, 0, 0
    for index, (p, n, d, s) in enumerate(zip(profile, num, den, read, strict=True)):
        if where is not None and not where[index]:
            continue
        residual = abs(b * n * s - 3 * d * a * p)
        bound = b * (3 * n + 6 * d)
        excess = residual - bound
        if worst_excess is None or excess > worst_excess:
            worst_index, worst_excess, worst_residual, worst_bound = index, excess, residual, bound
    stride_x, stride_y = int(shape[1]) * int(shape[2]), int(shape[2])
    node = (
        worst_index // stride_x,
        (worst_index // stride_y) % int(shape[1]),
        worst_index % int(shape[2]),
    )
    return worst_residual, worst_bound, node


# THE FILE'S DIGEST AND THE STAMP the generator writes (`input_digest`, `input_stamp`)
# live in the host module event_universe.world_files since item 72: the loader
# compares the stamp with the digest handed to it and computes none.


def _input_stamp_check(
    document: dict[str, object], measured: tuple[MeasuredDefinition, ...], digest: str | None
) -> None:
    """THE FILE'S HASH (the model owner's record 1886; ALGEBRA.md #a-familys-declaration, #the-primitives; BUILD.md section 26 item 28): a world with a seeded body
    carries `stamp` {hash}, the digest of the WHOLE document without `stamp`
    (the generator's stamp over every key, the profiles and the clocks among
    them), so that the file loaded is the one the generator wrote and a file
    changed by hand is regenerated, not run; no law identifier stands beside it
    (one engine, ALGEBRA.md #the-primitives). A world with no profile needs no stamp."""
    if not any(entry.block is not None and entry.block.profile is not None for entry in measured):
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
            f"stamp.hash {written[:12]}... is not the digest of the file "
            f"{digest[:12]}...: the document is not the one the generator stamped (a key changed "
            "after the stamp; the stamp covers the whole file, BUILD.md section 26 item 28; record "
            "1886); regenerate the file"
        )


def _initial_state_checks(
    shape: Address3,
    periodic: tuple[bool, bool, bool],
    families: tuple[FamilyDefinition, ...],
    measured: tuple[MeasuredDefinition, ...],
) -> None:
    """THE INPUT CHECKED LAWFUL OR REFUSED, IN INTEGERS (the model owner's
    record 1886; ALGEBRA.md #a-familys-declaration and (7)): the initial state is stored
    once in the file and the loader says at load whether it is lawful, with
    no float. Every block's Nodes disjoint from every other block's (ALGEBRA.md #what-a-body-is; a cube beyond a face is the fit check's refusal, naming the axis
    and the vertex); for every body seeded with a profile, its clock a / b
    strictly above its family's band top 2 num / den (a bound mode) and
    below 2 (stable), and the eigen-equation's residual within its proved
    bound at every Node of the board outside the other bodies of its family
    (the body's own mode in place on the composed operator: at another
    body's Nodes the operator carries that body's summand, so those Nodes
    are its check, not this one's; Nature's reading for the mathematician's
    word, BUILD.md section 26 item 20); the tail rule of 9.35 (a body's mode
    0 at every Node of every other body of its family) is RETIRED by ALGEBRA.md #the-primitives (commit 6). The remainders are 0 by
    construction (the profile is written at both levels with none); the
    amplitude's bound and the rich giving Nodes are checked where the block
    is parsed."""
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
    body_record: bool,
) -> tuple[DetectorDefinition, ...]:
    detectors = cast(
        tuple[dict[str, object], ...], value
    )  # the frame's checked detectors (loader/frame.py, `DETECTOR`)
    at = {entry.position for entry in measured}
    # The other Nodes of the bodies on a set: a body is named by its centre.
    inside: set[Address3] = set()
    for entry in measured:
        inside.update(body_nodes(entry.position, entry.span, shape, periodic) or ())
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
            threshold = 1  # the ray law's key is gone; the loop still reads the attribute
            bound_positions: list[Address3] = []
            if "positions" in obj:
                # the receiving set on free Nodes beside the block (the light
                # clock's cube adjacent to A's face, section 10 item 9): free
                # Nodes are admitted here, the set their receiver; the cube of
                # record 1899 as any detector
                positions_value = obj["positions"]
                if not isinstance(positions_value, list | tuple) or not positions_value:
                    raise ValueError(
                        f"{label}.positions with `block` must be a nonempty list of "
                        "Nodes, the receiving cube beside the block (DECLARATIONS.md section 10 "
                        "item 9; record 1899)"
                    )
                for item in positions_value:
                    position = _address(item, f"{label}.positions", shape)
                    if position in at or position in inside or position in taken:
                        raise ValueError(
                            f"{label}.positions with `block` names a Node of a measured "
                            f"event or of another set {list(position)}: the receiving set is a cube "
                            "of free Nodes beside the block"
                        )
                    taken.add(position)
                    bound_positions.append(position)
                _detector_region(name, bound_positions, shape, periodic, one_node=True)
            else:
                # A BODY IS ITS OWN DETECTOR, whatever its support (ALGEBRA.md #the-rows-against-nature, the
                # detectors' rule approved by the model owner, record 2109: a body of
                # several Nodes is one detector, a body of one Node its own, its six Links
                # its Ports, ALGEBRA.md #what-a-body-is; item 40; commit 7): the cube rule of record
                # 1899 is the free set's, not a body's
                if measured[bound_block].block is None:
                    raise ValueError(
                        f"{label}.block {bound_block} names a measured event that is no block"
                    )
            found.append(DetectorDefinition(name, tuple(bound_positions), threshold, block=bound_block))
            continue
        if "positions" not in obj:
            raise ValueError(f"{label} needs `positions` (or `block`, a set bound to a block)")
        positions_value = obj["positions"]
        if not isinstance(positions_value, list | tuple) or not positions_value:
            raise ValueError(f"{label}.positions must be a nonempty list of Nodes")
        positions = []
        for item in positions_value:
            position = _address(item, f"{label}.positions", shape)
            if position not in at:
                if position in inside:
                    raise ValueError(
                        f"{label}.positions names a Node of a body on a set "
                        f"{list(position)} that is not its position (a body is one record, "
                        "named by its centre)"
                    )
                raise ValueError(
                    f"{label}.positions names a Node without a measured event "
                    f"{list(position)} (a receiving set at a free Node beside a block declares "
                    "`block` with that one position, DECLARATIONS.md section 10 item 9)"
                )
            if position in taken:
                raise ValueError(f"a Node in two detectors {list(position)}")
            taken.add(position)
            positions.append(position)
        # THE DETECTOR IS ONE CONNECTED REGION, A CUBE (ALGEBRA.md #the-ladder;
        # record 1899): its Nodes are connected by Links (across a periodic
        # seam too), fill one box, and the box's sides are DETECTOR_SIDE or
        # more where the GameBoard's extent allows; separate places are
        # separate names
        _detector_region(name, positions, shape, periodic, one_node=True)
        threshold = 1  # the ray law's key is gone; the loop still reads the attribute
        if name.startswith(RESERVED_SET_PREFIX) or name in FACE_NAMES or name == LIFETIME_NAME:
            raise ValueError(
                f"{label}.name {name!r} is reserved: the layer names the measured "
                f"events outside every detector `{RESERVED_SET_PREFIX}<number>`, the faces and "
                "the border by their own names"
            )
        reading = DETECTOR_READINGS[0]  # the ray law's key is gone; the loop still reads the attribute
        if reading not in DETECTOR_READINGS and reading != SUM_READING:
            raise ValueError(
                f"{label}.reading must be one of {[*DETECTOR_READINGS, SUM_READING]}, not {reading!r}"
            )
        found.append(DetectorDefinition(name, tuple(positions), threshold, str(reading)))
    return tuple(found)


def _body_fit_check(world: NatureBeamWorld) -> None:
    """A body's cube whole on the board, never cut (the model owner's word of
    2026-09-24, 16:35Z and 16:48Z, through the Boss: the experimenter places
    the body exactly where he wants it; SIMULATOR_DEFINITIONS.md, the four
    building blocks, the body's condition 1): the Nodes [x0, x0 + s) on each
    axis from the lower vertex `position` with the edge `side` lie on the
    board on every axis the body's kind does not fold. On an open or closed
    axis the far vertex is on the board; on a periodic axis the extent is at
    least the edge (a cube across the seam is whole, a cube wrapped onto
    itself is not); the folded axis of extent 1 (a layer, a chain) is the
    one exception, the stabiliser's square or segment (ALGEBRA.md 8.2 and
    8.3). Refused naming the body, the axis and the extent; the engine's
    `_cube` and the margin module's `body_node_mask` then never cut."""
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
    as_written = obj  # the document as the generator stamped it (the universe's path, item 59)
    universe = obj[word]
    obj = dict(obj)
    del obj[word]
    if isinstance(universe, str):
        # THE ONE UNIVERSE FILE (item 59; record 2128 (3)): the path in place of the
        # list; the universe's integers from the file alone, the world's own refused
        families_file = universe
        _refuse_under_law(obj, "the world", set(frame.INTEGERS.keys))
        entries, integers = frame.universe(families_file, files, discover())
        obj.update(integers)
    else:
        # the families' list inline (a unit test's world), checked against the cards with
        # the world's own integers
        entries = frame.families(
            universe,
            {key: obj[key] for key in frame.INTEGERS.keys if key in obj},
            discover(),
            "the world.universe",
        )
    shape_value = cast(tuple[object, ...], obj["shape"])
    extents = tuple(_integer(item, "shape", 1, 4096) for item in shape_value)
    shape: Address3 = (extents[0], extents[1], extents[2])
    boundary, periodic = _boundary(obj["boundary"])
    closed = tuple(isinstance(boundary, dict) and boundary.get(axis) == CLOSED_FACE for axis in AXES)
    closed = (closed[0], closed[1], closed[2])
    ticks = _integer(obj["ticks"], "ticks", 0)
    # N declared in every file (no default: the model owner's rule through
    # the Boss, 2026-09-25; BUILD.md section 26 item 28; the 64 of the first
    # worlds HISTORY, written in each)
    phase_steps = _integer(obj["N"], "N", 2, MAX_PHASE_STEPS)
    if phase_steps & (phase_steps - 1):
        raise ValueError(f"N must be a power of two from 2 through {MAX_PHASE_STEPS}")
    # the largest age a record may carry, declared in every file (the loader's default from
    # the ray law's flight bound went with the table)
    age_bound = cast(int, obj["age_bound"])
    clock_stamp = cast(bool, obj["clock_stamp"])
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
    massive_record = cast(bool, obj["massive_record"])
    body_record = cast(bool, obj["body_record"])
    if body_record and not massive_record:
        raise ValueError(
            "body_record needs massive_record: true (a body record is a block held as "
            "one rotation on its clock pair, ALGEBRA.md #what-a-body-is)"
        )
    # massive-record-v1: the amplitude bound A, declared per massive world;
    # REQUIRED under the detector law with `massive_record` (no default, the
    # model owner's record 2089; the ceiling 2^28 of item 31 RETIRED, ALGEBRA.md
    # ALGEBRA.md #a-familys-declaration: A is the one number, the rule's int64 total its bound)
    amplitude_bound = AMPLITUDE_BOUND
    if massive_record and "amplitude_bound" not in obj:
        raise ValueError(
            "amplitude_bound is required with `massive_record`: "
            "A, the amplitude every row stays below, no default (the model owner's record 2089; "
            "ALGEBRA.md #the-line, #a-familys-declaration)"
        )
    if massive_record and "amplitude_bound" in obj:
        amplitude_bound = _integer(obj["amplitude_bound"], "amplitude_bound", 1, AMOUNT_BOUND)
    elif "amplitude_bound" in obj:
        raise ValueError("amplitude_bound is refused without the world key `massive_record`")
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
    # THE MOMENTUM'S UNIT Q (ALGEBRA.md #the-primitives, #the-well): the universe's integer
    # `momentum_unit`, REQUIRED with no default (the wall W = 3 Q M of every body)
    if "momentum_unit" not in obj:
        raise ValueError(
            "momentum_unit is required: Q, the momentum's unit "
            "of the universe's integers, the wall W = 3 Q M of every body, no default (ALGEBRA.md "
            "ALGEBRA.md #the-primitives, #the-well; the model owner's record 2089)"
        )
    momentum_unit = _integer(obj["momentum_unit"], "momentum_unit", 1, AMOUNT_BOUND)
    # THE TWIST TABLE (ALGEBRA.md #the-primitives): the families file's, checked with Gamma and A;
    # admitted on an inline world; an inline world without it has no transport (the
    # engine refuses a nonzero twist naming the Port)
    twist_table: TwistTable | None = None
    if "twist_table" in obj:
        twist_table = _twist_table(obj["twist_table"], "twist_table", node_clock, amplitude_bound)
    # THE FAMILY GENERICITY (the model owner's record 2066; BUILD.md section 26
    # item 51): the families' roles of items 32 and 35 are their own
    # declarations (`held`, `reads`), read by `_families` below; the world
    # keys clock_family, charge_family and charge_strength are retired
    mode_axis: int | None = None
    if "mode_axis" in obj:
        if not massive_record:
            raise ValueError("mode_axis is refused without the world key `massive_record`")
        mode_axis = AXES.index(str(obj["mode_axis"]))
    probes: tuple[Address3, ...] = ()
    if "probes" in obj:
        if not massive_record:
            raise ValueError("probes is refused without the world key `massive_record`")
        declared_probes = cast(tuple[object, ...], obj["probes"])
        probes = tuple(_address(item, "probes", shape) for item in declared_probes)
    action = None
    families = _families_of(entries, age_bound, massive_record, amplitude_bound)
    # The bound is asked of a world with a MASSIVE FAMILY (a pair with den >
    # num; DECLARATIONS.md section 15 M1-10 lists the massive worlds): a
    # light world under `massive_record` (its probes, its mirror blocks of
    # light's kind) loads without it (the Boss's 03:44Z, the gate reviewer's line on the block's grace).
    if massive_record and "amplitude_bound" not in obj and any(f.massive_kind for f in families):
        raise ValueError(
            "a world with a massive family declares `amplitude_bound`, the amplitude "
            "A every row stays below (2^28 in every registered massive world since BUILD.md "
            "section 26 item 31, DECLARATIONS.md section 15 M1-10's 2^32 HISTORY; the load bound "
            "and the rows' run-time assertion use it; no default)"
        )
    # THE BODIES AND THE DETECTORS through the frame (loader/frame.py, `BODY`, `DETECTOR`):
    # every key checked with the families known, an unknown key refused by name
    bodies = frame.bodies(obj["measured"], Context(tuple(family.name for family in families)))
    measured = _measured(
        bodies,
        shape,
        periodic,
        families,
        phase_steps,
        ticks,
        action,
        massive_record,
        amplitude_bound,
        momentum_unit,
    )
    _held_bodies_checks(families, measured)
    _node_clock_bound(families, measured, amplitude_bound, node_clock)
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
    if body_record:
        # every seeded block carries its profile and its clock pair (the
        # generator's, under the stamp): the body record's shape and its
        # rotation's rational (ALGEBRA.md #what-a-body-is)
        for number, entry in enumerate(measured):
            block = entry.block
            if block is None or block.seed <= 0:
                continue
            if block.profile is None or block.clock is None:
                raise ValueError(
                    f"measured[{number}] under body_record declares no `clock` with its "
                    "profile: a body record is its stored profile and one rotation on its clock pair "
                    "[num_c, den_c], the generator's (ALGEBRA.md #what-a-body-is and (9) (a); "
                    "`seed_on_the_mode`)"
                )
            if block.proper_clock is None and any(int(part) != 0 for part in entry.momentum):
                raise ValueError(
                    f"measured[{number}] under body_record moves and declares no "
                    "`proper_clock`: the body's Node of a moving body rotates at the proper pair of its "
                    "momentum, the moving mode's rotation at its moving centre, the generator's "
                    "(ALGEBRA.md #the-velocity; `seed_on_the_mode`)"
                )
    _input_stamp_check(as_written, measured, digest)
    _initial_state_checks(shape, periodic, families, measured)
    detectors = _detectors(frame.detectors(obj["detectors"]), shape, periodic, measured, body_record)
    readings = world_readings(obj, shape, detectors, families, measured)
    world = NatureBeamWorld(
        shape,
        boundary,
        periodic,
        ticks,
        phase_steps,
        age_bound,
        families,
        measured,
        detectors,
        readings,
        step,
        clock_stamp=clock_stamp,
        face_depth=face_depth,
        massive_record=massive_record,
        body_record=body_record,
        probes=probes,
        mode_axis=mode_axis,
        closed=closed,
        amplitude_bound=amplitude_bound,
        node_clock=node_clock,
        momentum_unit=momentum_unit,
        twist_table=twist_table,
        start=start,
        universe_file=families_file,
    )
    _detector_law_load_checks(measured, families, periodic, phase_steps)
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
