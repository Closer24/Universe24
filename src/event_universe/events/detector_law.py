"""The engine (one engine, no law's name and no version, ALGEBRA.md 9.90 (1);
the model owner's words of 2026-09-23, docs/designs/detector_law/DESIGN.md):
the record splits at every free Node inside the board and holds its
amplitudes; outside there is no board, only clicks, and nothing passes from
Node to Node except through a detector, at rest or moving. Every world is the
engine's: no world key selects it (the ray law is cancelled,
docs/CANCELLED_WORLDS.md).

The Inside (DESIGN.md sections 1 and 2): a record's row at a Node holds
its amplitude now `a_now`, its amplitude one interval ago `a_before`
(integers on the record's wheel, the amplitude unit 2^20) and a
remainder `r`; every interval, at every Node with a row of the record,

    3 a_next + r' = (a_E + a_W + a_N + a_S + a_U + a_D) - 3 a_before + r,  0 <= r' < 3

(the group-ring addition over the six neighbours, verb G, and the
Euclidean division by 3 with the remainder kept on the record's row, verb
D; the pair [1, 3] of the exact square its only constant; a periodic axis
wraps, an open face is a declared wall that is not read). A record is
kept as dense arrays over the board (the first build; the record's rows
are the Nodes it has reached, the rest zero), one record per giving.

The Outside (DESIGN.md sections 1 and 5): two things only on the board,
the free Node and the receiver-inserter. A measured event with a lamp
INSERTS: each giving is a record driven at the lamp's Nodes by the
family's clock (the pair `phase_per_link` [n, d] on the circle of N steps)
for the lamp's train (the key `train`, in periods); the lamp pays the
family's quantum h at the giving. Every measured event's Nodes, every
detector set's Nodes and every open face's layer RECEIVE: the offer
`a_next^2` arriving at such a Node is added to the record's pointer for
that detector (a measured event's own detector `measured:<number>`, a set's detector
by the set's name, a face's `face:<axis>`), and the Node's amplitude is
taken (0 re-emitted). The record completes when its train has ended and
its offer on the board has been exhausted into the detectors (below one rung
of the wheel of what the detectors hold); the click's detector is chosen by
`cell_of` over the pointers on the record's wheel (the counting form,
record 1288; `amplitude.cell_of`), one click per record; the click line
(`gather`, the amplitude law's keys, with `clock` the detector's own count
and `giving` the record's giving stamp) is written, the record's content h
handed to the measured event at the chosen Node (or booked as escaped at a
face or a set without a body), and the record's rows removed. The books
balance as today: held content initial + measured == current + spent +
escaped; transit released == current + absorbed + escaped.

The massive record kind (`massive-record-v1`, MASSIVE_RECORD.md section 1,
the world key `massive_record`, off by default): the same step with a
declared pair `[num, den]` on the six-neighbour term per record KIND (the
family's `pair`; light's kind the value `[1, 1]`),

    3 den a_next + r' = num (a_E + .. + a_D) - 3 den a_before + r,  0 <= r' < 3 den

(verb G, then D by 3 den with the remainder kept, then T), the pair two
dense arrays over the board per family (`kind_num`, `kind_den`; a block's
Nodes carry a lowered pair there, the build's step 3), the world's border
read by every family (one border, `boundary`; a zero face beyond an open
or a closed one, BUILD.md section 26 item 28) and the conserved
form I of section 3 read by the books as a GAMEBOARD diagnostic
(`record_form`). Without the key every world reads as it did, byte for
byte (`tests/test_massive_record.py`).
"""

from __future__ import annotations

from collections.abc import Callable, Iterator
from dataclasses import dataclass, field
from math import gcd
from typing import cast

import numpy as np

from event_universe.core.game_board import box_centre
from event_universe.core.integer import by_drive
from event_universe.core.register import Register, discover
from event_universe.core.rule3 import (
    ISOTROPIC,
    THE_ADVANCE,
    THE_INVERSE,
    THE_REWRITE,
    THE_UNHOLD,
    carried,
    coefficients,
    form_term,
    rule3,
    rungs,
)
from event_universe.features import self_source
from event_universe.features.hold import TENSOR_AXES, HoldOwn, HoldStart, HoldTerm, HoldWrites, booking
from event_universe.features.signed_read import SignedReadStart, SignedReadTerm, content_of
from event_universe.loader.world import (
    AXES,
    TWIST_FINE_BITS,
    BlockDefinition,
    NatureBeamWorld,
)

Record = Callable[[dict[str, object]], None]

# ONE ENGINE, NO LAW'S NAME AND NO VERSION (ALGEBRA.md 9.90 (1)): the constant
# that named the law and its version ("detector-law-v1") is CANCELLED; the books
# and the state carry no law entry
FACE_NAMES = ("face:-x", "face:+x", "face:-y", "face:+y", "face:-z", "face:+z")
# The receiver's take (DESIGN.md sections 1 and 5): a Node that receives does
# not send the wave back (a mirror is a receiver body that re-emits, never a
# wall). The record's row at a receiver holds one amplitude per Port that
# faces a free Node (the NodeState's Ports), the wave entering by that Port,
# following it one way: g(t + 1) = a_f(t) + k (a_f(t + 1) - g(t)) with a_f
# the free neighbour's amplitude and k = (c - 1) / (c + 1) at c = 1 / sqrt 3,
# the declared pair [-15, 56] (-0.2679 against sqrt 3 - 2 = -0.2679), a
# rounding declared at load, not a root at run time; the free neighbour reads
# g as the receiver's amplitude on that Link, and the receiver books g^2 as
# the offer arriving by that Port.


# A RATIONAL IS A PAIR OF INTEGERS (numerator, denominator) in lowest terms with the
# denominator positive: the engine holds no `fractions` (the integer rule, record 2071;
# tests/test_integer_algebra.py). The pairs are Python integers without the working
# bound (the conserved form summed over a board and the body-frame booking's terms
# exceed 2^63, as the exact rationals they replace did); gcd, sums and products alone.
Ratio = tuple[int, int]
ZERO: Ratio = (0, 1)


def ratio(numerator: int, denominator: int) -> Ratio:
    """The pair (n, d) in lowest terms with d positive (one gcd)."""
    if denominator < 0:
        numerator, denominator = -numerator, -denominator
    common = gcd(numerator, denominator) or 1
    return numerator // common, denominator // common


def ratio_sum(terms: list[Ratio]) -> Ratio:
    """The exact sum of pairs, reduced after every addition (sums and products)."""
    numerator, denominator = 0, 1
    for n, d in terms:
        numerator, denominator = ratio(numerator * d + n * denominator, denominator * d)
    return numerator, denominator


def form_json(value: Ratio) -> list[int]:
    """A form's exact rational for the books and the state (GAMEBOARD): the
    pair [numerator, denominator] in lowest terms (the denominator 1 for a
    record at one level and for the fields; ALGEBRA.md 9.50 (13))."""
    numerator, denominator = ratio(value[0], value[1])
    return [numerator, denominator]


@dataclass
class LiveRecord:
    """One record on the board: its dense rows and its ledger."""

    identity: int
    lamp: int
    family: int
    u: int
    given: int
    giving_tick: int
    content: int
    period_numerator: int
    period_denominator: int
    train: int
    period: int
    now: np.ndarray
    before: np.ndarray
    remainder: np.ndarray
    age: int = 0
    pointers: list[int] = field(default_factory=list)
    absorbed: int = 0
    norm: int = 0
    first_rung: list[int | None] = field(default_factory=list)
    # THE RESIDUE FROM THE LAW (ALGEBRA.md 9.22 (4); BUILD.md section 26 item
    # 15): the record's own wheel W, given with its residue u, both read from
    # the rule's remainder at the giving Node of the record that clicked to
    # giving it (`residue_of`); a planted record carries the test's W. The
    # rung's wheel is the record's, never a set's or the world's. UNDER THE
    # NODE CLOCK (ALGEBRA.md 9.35 (2), (3); BUILD.md section 26 item 31) W
    # = 3 den f / gcd(Gamma num, 6 den M, 3 den f) at that Node with f =
    # Gamma + M (`wheel_at`): the pair's own where the content M is 0,
    # content-dependent at a body's Nodes, read from the rule and never
    # declared.
    wheel: int = 1
    # massive-record-v1: the emitter's number for a record a body emitted
    # (None for a planted record and for a block's own record); the
    # coupling's folded denominator (`scale`) is HISTORY since the model
    # owner's decision (2) of record 1962 (the wall 3 den alone, one D per
    # row per interval, the remainder in [0, wall)).
    emitter: int | None = None
    # The pair's arms (detector-law-v1, build 2, component 2; DECLARATIONS.md
    # Bell's four settings and the no-signalling control, DESIGN.md 6.3): a lamp with `arms` givings one record
    # per arm on one giving stamp (the same ordinal, u and tick), each arm's
    # row confined to its own half-space by the arm's first direction (the
    # rows zero beyond the lamp's Node on the other side, verb D's comparison
    # at every interval), the joint labels carried on every arm unchanged;
    # a lamp of one arm has no mask and its record is as it was.
    arm: int = 0
    arms: int = 1
    labels: tuple[tuple[int, int], ...] = ((0, 1),)
    mask: np.ndarray | None = None
    # The joint gather (DECLARATIONS.md section 1 item 3): an arm of a pair
    # that has completed waits, its rows still, for the other arms; the pair
    # gathers once when every arm has completed.
    arm_done: bool = False
    # HOST (record 2039 (b); BUILD.md section 26 item 43): the record's support
    # box, [lo, hi) per axis, outside which its two levels and its remainder
    # are zero; None for the whole board. The step reads and writes the box
    # grown by one Link (the rule's reach) and writes zeros elsewhere: the
    # same integers as the whole-board step, bit for bit, since zero rows with
    # a zero remainder step to zero under the rule. A shortcut of the host,
    # not of the law: the model's local work per Node is unchanged.
    box: tuple[tuple[int, int], ...] | None = None

    # The record's LADDER BY NAME (the lamp's `receiver`, SIZING.md; the
    # click line and the receiver by name, DECLARATIONS.md section 13 item
    # 7): the detectors among which u chooses, None for every detector as built. A
    # detector outside the ladder is a SINK for this record: it takes and books
    # as every detector does (the pointer, `absorbed`, the rung), but the click
    # never chooses it and its share is not in the ladder's sum.
    ladder: list[int] | None = None

    # THE INCREMENT LADDER (ALGEBRA.md 9.25 (2)): the record's running total
    # C of its one-way flux into the detectors of its ladder, every detector's
    # increment in the ladder's order, against the record's threshold
    # (2 u + 1) T / (2 W) fixed at its giving; the click at the interval C
    # crosses it, at the detector whose segment of that interval's increment
    # holds the threshold.
    total: int = 0
    # whether the record's line was written (the record is deleted whole at
    # that interval, ALGEBRA.md 8.8, record 1888)
    clicked: bool = False
    # THE BOOKING IN THE BODY'S FRAME (ALGEBRA.md 9.74 (2); BUILD.md section
    # 26 item 56): per detector of a moving set, the fraction of the face's
    # booking below one unit of the flux, carried to the next interval's
    # booking (a remainder kept on the record, exact); empty at rest
    carry: dict[int, Ratio] = field(default_factory=dict)
    # THE FOUR-VECTOR CLICK'S SPACE PART (ALGEBRA.md 9.86 (1), 9.91 (4), 9.84 (2),
    # 9.25 (12); commit 5 without the recoil, record 2135): per detector, per
    # axis, the flux booked through the detector's Ports on its -a side minus
    # the flux booked through those on its +a side, summed over the record's
    # walk (the taken quantum's direction of travel: a quantum moving toward
    # +a enters through the -a face); the sign per axis is sigma_a on the
    # click line. Nothing is added to any body's momentum: the recoil of
    # 9.84 (2) waits on the closing of record 2135 (the click that keeps the
    # momentum, 9.109, is a decision of three).
    momentum_tally: dict[int, list[int]] = field(default_factory=dict)
    # THE GIVEN QUANTUM'S DIRECTION (9.91 (4), the giving's tally): per axis, the
    # outward flux through the body's +a Ports minus through its -a Ports over
    # the window, the sign per axis on the giving line at the close
    outward_tally: list[int] = field(default_factory=lambda: [0, 0, 0])
    # THE POINT EMITTER'S WINDOW (ALGEBRA.md 9.71 (1); BUILD.md section 26 item
    # 50): open from the giving click until the outward norm through the
    # body's Node's six Ports reaches T; the intervals written and the outward norm
    # summed; the giving line held until the close names the record
    window_open: bool = False
    window: int = 0
    # THE FAMILY GENERICITY (record 2066; item 51): a body's own standing
    # record (the lattice body's, held by the law at the body and read by no
    # detector, its inverse with the body's), marked on the record and not
    # on its family
    standing: bool = False
    outward: int = 0
    giving_line: dict[str, object] | None = None
    # The sinks' take of a record under the receiver by name (HOST, the
    # pointer's unit): what the faces and every set but the receiver took,
    # inside `absorbed` (the completion's measure) and on no pointer.
    escaped: int = 0
    # THE RECORD'S PAIR (ALGEBRA.md 9.85 (3), 9.91 (7); the one stroke, commit
    # 1): the rest pair its rows step with, its family's declared pair or, on
    # a family whose pair is the body's, the body's `kind` or the emitter's
    # `pair`; the board's pair arrays are read by (family, pair); None reads
    # the family's declared pair (a record made without one, the tests')
    pair: tuple[int, int] | None = None
    # THE COMPONENT (ALGEBRA.md 9.86 (2), 9.91 (1)): the index of the record's
    # component in its family's parts (0 the time part; a wave of light in
    # one transverse component of the charge family, commit 4)
    part: int = 0
    # THE HELD PART (item 51; 9.91 (2), (3)): a field family's component
    # record, stepped plain at the pace 1, written by the hold at the bodies'
    # Nodes, booked by no detector; marked on the record, not on its family
    # (the charge family is held and has waves, 9.86 (2) (b))
    held_part: bool = False
    # HOST (record 2039 (b); 9.91 (1) "the support-box shortcut keeps a zero
    # part free of work"): a held part never written nonzero: its two levels
    # and remainder are zero everywhere and step to zero exactly, so the step
    # is skipped; cleared by the first nonzero hold
    silent: bool = False
    # THE NORM'S DENOMINATOR (ALGEBRA.md 9.50 (13); BUILD.md section 26 item
    # 36): the record's conserved form is the exact rational norm / pace (the
    # Node's terms weighted by 1 / p_i); at one level p times the form is
    # whole and the pair reduces from (p x form, p), the pace Gamma - c + q
    # Lambda d at the body's Nodes as written; the ladder reads the plain
    # flux against it, 2 W pace C against (2 u + 1) norm. 1 for a record
    # whose norm is set in the form's own units.
    pace: int = 1
    # THE SECOND LEVEL of a phase-2 record (ALGEBRA.md 9.91 (1); commit 4): the pair's
    # second component, (now, before, r) over the board, None until a rotation of the
    # transport writes it (a second level that starts zero and meets no twist stays
    # exactly zero, 9.91 (2), (9) (c))
    im_now: np.ndarray | None = None
    im_before: np.ndarray | None = None
    im_remainder: np.ndarray | None = None
    # THE TWIST "OWN" (ALGEBRA.md 9.96 (2) (a)): round(2^16 omega_0), the record's own
    # rotation in the table's unit, the loader's integer; 0 for a record with none (a
    # held part, a planted record without one)
    twist: int = 0


@dataclass
class NodeRecord:
    """THE BODY'S RECORD AT ITS BODY'S NODE (ALGEBRA.md 9.60 (1) and (2); BUILD.md
    section 26 item 42; the model owner's question of record 2036, "can it not
    be represented somehow in the Node?"): the standing record of the body's
    own standing family on the body's Node alone (the body's centre Node,
    `centre_mask`), two integer levels and one remainder (a, b, r) at that
    Node, stepped by rule3 (core/rule3.py, ALGEBRA.md 9.50 (13))
    with the standing family's six Ports closed on the body's Node, so that the six
    reads return the body's Node itself, S_6 = 6 a, with the declared pair [num_c,
    2 den_c] (the body's clock pair in the rule's convention) and the body's Node's
    own level: 6 den_c Gamma a' + r' = (6 num_c p + 12 den_c c) a - 6 den_c
    Gamma b + r, 0 <= r' < 6 den_c Gamma, the rotation of 9.46 (2) as
    rationals with the remainder six times its (9.60 (2)); its residue u its
    own remainder on its wheel, read at the click and carried; its norm T the
    emitter's declared integer; the identity the body's record's (number x
    2^32). Nothing physical is kept beside the GameBoard: the record is the
    body's Node's, the content the body's Node's level of the family of clicks, the charge
    the family of charge's; the shape phi and the pairs are the world file's
    declared constants (9.60 (6))."""

    identity: int
    now: int
    before: int
    remainder: int = 0
    u: int = 0
    wheel: int = 1
    norm: int = 0


@dataclass
class Block:
    """A block on the board (massive-record-v1, MASSIVE_RECORD.md sections 4
    to 7; BUILD.md section 2): its Nodes R (the mask over the board, the
    cube of `side` at `corner`), its own massive record (the seed on its
    Nodes), the light records it emitted, its clock (its record's cycles
    across R), its momentum per axis with the drive's accumulators against
    its wall W = 3 Q M (`wall_of`, live with its quanta; ALGEBRA.md 9.96 (1)),
    and its detector among the simulation's detectors."""

    number: int
    family: int
    definition: BlockDefinition
    corner: list[int]
    mask: np.ndarray
    detector: int
    momentum: list[int]
    drive: list[int] = field(default_factory=lambda: [0, 0, 0])
    # THE SPIN AS STATE (ALGEBRA.md 9.78 (5), 9.91 (8) (v); commit 6): S now and S one
    # interval back, the leapfrog's two integers; the load's write is the body's
    # declared `spin` at both
    spin: list[int] = field(default_factory=lambda: [0, 0, 0])
    spin_before: list[int] = field(default_factory=lambda: [0, 0, 0])
    # A TOOL HELD IN PLACE (ALGEBRA.md 9.104 (6) (b); the Boss's record 2157): the world's
    # word `fixed`; the feed, when it lands, acts on a body without the word alone
    fixed: bool = False
    count: int = 0
    previous_sum: int = 0
    own: LiveRecord | None = None
    # THE BODY'S RECORD AT ITS BODY'S NODE (ALGEBRA.md 9.60; item 42, item 37
    # HISTORY): the standing record on the body's Node under the world key
    # `body_record`, its own rows then nowhere else on the GameBoard (`own`
    # None); None under the lattice body
    node_record: NodeRecord | None = None
    emitted: list[int] = field(default_factory=list)
    current: int | None = None
    givings: int = 0
    hop: tuple[int, int, int] = (0, 0, 0)
    # THE POINT EMITTER (item 50): the identity of the given record whose
    # window is open at this body, None when none is
    window: int | None = None
    new_cycle: bool = False
    # the interval the current cycle began and the last cycle's length (the
    # emitted record's period for its grace, the block's grace for its emitted records)
    cycle_start: int = 0
    cycle_length: int = 0
    stepped: int = 0
    # the emitter as a clicking body (ALGEBRA.md 9.17 (4), 9.43 (3), 9.44 (5)
    # (c)): the excitations started (k), the intervals counted since the
    # residue's read (the count t against (2 u + 1) P / (2 W), no running
    # total), and whether the tick fired this interval
    excitations: int = 0
    wait: int = 0
    emit_now: bool = False
    # THE READ POINT OF THE FIRST RESIDUE (ALGEBRA.md 9.19 (4e), 9.43 (4)):
    # the load's seed has the remainders 0 at the write and nonzero after
    # one step of the rule, so the first u and W are read from the body's
    # own remainder at the first shell Node after its first advance; every
    # later residue is read at the click (9.44 (5) (c))
    residue_pending: bool = False
    # THE HOLDS' REMAINDERS (ALGEBRA.md 9.91 (3); the one stroke, commit 2): per
    # held family and part, the division's remainder carried between intervals
    # and the value written, (family, part) for the support's writes and ("d",
    # family, i, j, sigma) for the dipole's on the Node + sigma e_j; exact and
    # inverted with the body
    hold_carry: dict[tuple[object, ...], int] = field(default_factory=dict)
    hold_value: dict[tuple[object, ...], int] = field(default_factory=dict)


class PairView:
    """The tests' view of a family's pair arrays by its own declared pair
    (`kind_num[family]`, `kind_den[family]`; item 51's form): one array of
    the two, from `pair_arrays`."""

    def __init__(self, simulation: DetectorLawSimulation, index: int) -> None:
        self.simulation = simulation
        self.index = index

    def __getitem__(self, family: int) -> np.ndarray:
        return self.simulation.pair_arrays(family)[self.index]


@dataclass
class Ledger:
    """The books per family (Python integers, exact)."""

    held_initial: list[int]
    held_measured: list[int]
    held_spent: list[int]
    held_escaped: list[int]
    transit_released: list[int]
    transit_absorbed: list[int]
    transit_escaped: list[int]
    # item 10 (HOST): the content of the records their own emitters took
    # wholly (the remnant never left the board and is not received back)
    taken_by_emitter: list[int]
    # the receiver by name (HOST): the count of records whose line was
    # written at their receiver's rung and which have since closed (no
    # content: the content moved with the line); shown on a world with a
    # receiver alone
    closed_after_click: list[int]


class DetectorLawLayer:
    """The record's lines the runner writes into run.json (the amplitude law's shape)."""

    def __init__(self) -> None:
        self.gathers: list[dict[str, object]] = []
        self.given = 0
        self.gathered = 0


class DetectorLawSimulation:
    """One world under the engine, stepped interval by interval."""

    # the record's step, one fused call today, its click included: the names of the file's chain
    CHAIN: tuple[str, ...] = (
        "the pair",
        "the degree",
        "the signed read",
        "the send",
        "the wait",
        "the receive",
        "the internal representation",
        "the self-source",
        "the phase",
        "the operation",
        "the clicks",
    )

    def __init__(self, world: NatureBeamWorld, observer: Record | None = None) -> None:
        self.world = world
        self.record = observer
        self.tick = 0
        self.shape = tuple(int(n) for n in world.shape)
        self.families = world.families
        self.fast_steps = 0
        self.hypotheses = list(world.hypotheses)
        self.layer = DetectorLawLayer()
        count = len(world.families)
        self.held: list[list[int]] = [
            list(entry.held) + [0] * (count - len(entry.held)) for entry in world.measured
        ]
        self.ledger = Ledger(
            [sum(h[f] for h in self.held) for f in range(count)],
            [0] * count,
            [0] * count,
            [0] * count,
            [0] * count,
            [0] * count,
            [0] * count,
            [0] * count,
            [0] * count,
        )
        # The detectors: index 0 .. K - 1 with a name, the Nodes of each, and the
        # measured event (if any) that receives the content of a click there.
        # A detector set is ONE detector over its whole cube (record 1899): the
        # flux into the cube through its Ports from outside is its increment,
        # the click is the detector's, reported by its name, never by a Node.
        self.detector_names: list[str] = []
        self.detector_measured: list[int | None] = []
        self.detector_face: list[bool] = []
        # The gather's detector triple [set, channel, label]: a detector's set name
        # (its own name but for a table body's two detectors, which carry their
        # set's name) and its channel (0, the + channel; 1 the - channel of
        # a table body); every detector as built is [name, 0, "0"].
        self.detector_set: list[str] = []
        self.detector_channel: list[int] = []
        self.detector_at_node = np.full(self.shape, -1, dtype=np.int64)
        # the Port pairs per family for the detectors' inflow, listed once on first use
        self._inflow_port_pairs: dict[int, tuple[np.ndarray, np.ndarray, np.ndarray]] = {}
        # the Ports' faces beside the pairs (axis, side), item 56
        self._inflow_port_faces: dict[int, tuple[np.ndarray, np.ndarray]] = {}
        for number, entry in enumerate(world.measured):
            nodes = self._span_nodes(entry.position, entry.span)
            own = self._detector(f"measured:{number}", number, False)
            for node in nodes:
                self.detector_at_node[node] = own
        # The sets bound to a block (DECLARATIONS.md section 10 item 9, section
        # 13 item 1, section 15 M1-4; a set bound to a block is a receiver): RECEIVERS in the form of
        # DESIGN.md section 5, their Nodes take Nodes (the one-way Port take,
        # the row held at 0, the offer booked to the set's detector, `absorbed`
        # moved, the click at the first rung stamped with the block's own
        # count), FREE for the emitting block's own record during that
        # record's grace (the masks per record by its emitter and age). A set
        # with one declared position is the receiving Node beside the block
        # (the light clock's x = 612); a set without positions takes at the
        # block's current Nodes (the Sagnac blocks, a stepping block's Nodes follow
        # it). `set_block`: the set's detector to its block; `set_nodes`: the
        # set's declared Nodes' mask, None where the Nodes are the block's.
        self.set_block: dict[int, int] = {}
        # the detector sets in their declared order: the ladder of a
        # record that names no receiver (ALGEBRA.md 9.19 (3) (b))
        self.set_detectors: list[int] = []
        self.set_nodes: dict[int, np.ndarray | None] = {}
        # THE TABLES ARE RETIRED (the cleanup order's step 3; ALGEBRA.md 9.21):
        # a measured event with a table entry (a polariser's window, a
        # splitter's rows) is refused here; the polariser returns as a body
        # with an axis and two receivers named, a splitter as a region of the
        # one operator
        for number, entry in enumerate(world.measured):
            if any(window is not None for window in entry.windows) or any(
                split is not None for split in entry.splits
            ):
                raise ValueError(
                    f"measured[{number}].table is refused: the "
                    "tables (the polariser's two detectors at one Node, the splitter's linear form) "
                    "retired with the flux reading (the given pair on the circle; BUILD.md section 26 item 17); a polariser is "
                    "a body with an axis and two receivers named, a splitter a region of the one "
                    "operator (ALGEBRA.md 9.21)"
                )
        for detector in world.detectors:
            set_detector: int | None = None
            if detector.block is not None:
                set_detector = self._detector(detector.name, detector.block, False)
                self.set_block[set_detector] = detector.block
                self.set_detectors.append(set_detector)
                if detector.positions:
                    nodes_mask = np.zeros(self.shape, dtype=bool)
                    for position in detector.positions:
                        node = (int(position[0]), int(position[1]), int(position[2]))
                        nodes_mask[node] = True
                        self.detector_at_node[node] = set_detector
                    self.set_nodes[set_detector] = nodes_mask
                else:
                    self.set_nodes[set_detector] = None
                continue
            for position in detector.positions:
                node = (int(position[0]), int(position[1]), int(position[2]))
                existing = int(self.detector_at_node[node])
                measured = self.detector_measured[existing] if existing >= 0 else None
                if set_detector is None:
                    set_detector = self._detector(detector.name, measured, False)
                    self.set_detectors.append(set_detector)
                elif measured is not None and self.detector_measured[set_detector] is None:
                    self.detector_measured[set_detector] = measured
                self.detector_at_node[node] = set_detector
        # THE FACE RECEIVER (ALGEBRA.md 9.19 (3) (a); Highlights' record 15
        # kept): an open axis carries the receiver `face` at its border, last
        # on every ladder, so that what leaves the board clicks there; a
        # periodic axis has none; a `closed` face (DECLARATIONS.md section
        # 10's mirror B) is a zero row with no receiver, the level 0 beyond it
        # as `_shift` fills. Nothing takes: the sponge is retired. THE FACE
        # SLAB (9.25 (10); BUILD.md section 26 item 23): the receiver is the
        # slab of the world's `face_depth` free Nodes nearest every open
        # border, one detector, its Ports toward the interior alone (a Link inside
        # the slab carries no offer, the zero row beyond the border no Node).
        self.face_detector: int | None = None
        for axis in range(3):
            if world.periodic[axis] or world.closed[axis] or self.shape[axis] < 2:
                continue
            if self.face_detector is None:
                self.face_detector = self._detector("face", None, True)
            depth = min(world.face_depth, self.shape[axis])
            for index in [*range(depth), *range(self.shape[axis] - depth, self.shape[axis])]:
                view = np.moveaxis(self.detector_at_node, axis, 0)[index]
                free = view < 0
                view[free] = self.face_detector
        # THE NODE CLOCK (the model owner's decision (5) of record 1962;
        # ALGEBRA.md 9.35 (2) and (3); BUILD.md section 26 item 31): the
        # world's Gamma and the content M at every Node, the held quanta of
        # every family at every measured event (a body's stock and what its
        # clicks brought) on the event's Nodes (a block's Nodes as they
        # stand, a measured event's span), 0 in the vacuum; the clock pair
        # (e, f) = (Gamma, Gamma + M) enters every family's rule at the
        # Node. M changes only at the law's events (a giving, a click, a
        # step of a body), so the array is rebuilt from the held books as
        # each interval begins (`_hold`) and after a giving.
        # THE MOMENTUM'S UNIT Q (ALGEBRA.md 9.96 (1), 9.89 (2)): the universe's
        # integer; every body's wall is W = 3 Q M (`wall_of`)
        self.momentum_unit = int(world.momentum_unit)
        if self.momentum_unit < 1:
            raise ValueError(
                "the world declares no momentum unit (`momentum_unit`, Q from 1; ALGEBRA.md 9.96 (1))"
            )
        # THE TWIST TABLE (ALGEBRA.md 9.81 (2) (b), 9.96 (2) (c); commit 4): the universe's
        # triples as arrays, (c, s, d) by k_0 (fine) and by k_1 (coarse); None on a world
        # without one, where a nonzero twist is refused naming the Port
        self.twist_table = world.twist_table
        if self.twist_table is not None:
            self._fine = np.array(self.twist_table.fine, dtype=np.int64).T
            self._coarse = np.array(self.twist_table.coarse, dtype=np.int64).T
        # HOST: the Ports' angles per (family, own twist, direction) per interval
        self._twists: dict[tuple[int, int, bool], tuple[int, list[np.ndarray] | None]] = {}
        # HOST: the self-source per family per interval (9.91 (5)), None at P_2 = 0
        self._sources: dict[tuple[int, bool], tuple[int, np.ndarray]] = {}
        self.node_clock = int(world.node_clock)
        if self.node_clock < 1:
            raise ValueError(
                "the world declares no Node clock (`node_clock`, Gamma from 1; "
                "ALGEBRA.md 9.35 (3); BUILD.md section 26 item 31)"
            )
        # THE FAMILY GENERICITY (the model owner's record 2066 of 2026-09-25
        # through the Boss; BUILD.md section 26 item 51; the family of clicks
        # of record 1982 and ALGEBRA.md 9.45, item 32, and the family of
        # charge of 9.48, item 35, are its two cases): the engine knows no
        # family's name or role. A family with a declared `held` source has
        # one record over the board (`held_records`), its level held at every
        # body's Nodes at the body's declared source (the quanta it holds, or
        # their signed sum; both levels, the remainder 0, not the step's own
        # there), written at the load and at every click; elsewhere it moves
        # by its own plain step after the other families' (so the joint step
        # inverts); no residue, no ladder, no click of its own, never booked.
        # `node_level` is each held family's level as every reading family's
        # step reads it (`_effective_content`, by the reading family's
        # declared `reads`: SUM weight x level, or - q x weight x level by the
        # reading family's own charge sign q; 9.45 (3), 9.48 (3)). The sources
        # and the read modes are words of the operations ("content", "sign";
        # "plain", "sign"), never a family's name (item 53). The sources
        # and the read modes are words of the operations ("content", "sign";
        # "plain", "sign"), never a family's name (item 53).
        self.held_families: list[int] = list(world.held_families)
        self.family_charge = [int(family.charge[0]) for family in world.families]
        self.node_level: dict[int, np.ndarray] = {
            family: np.zeros(self.shape, dtype=np.int64) for family in self.held_families
        }
        self._effective: dict[int, np.ndarray] = {}  # HOST: per interval, cleared by the hold
        # THE FOUR PACES (ALGEBRA.md 9.91 (2); commit 3): per reading family the
        # three axis contents t_a (the reads' aa components halved, the division's
        # remainder carried per Node, `_pace_carry` keyed (family, read, axis)),
        # computed once per interval (HOST cache by tick); None where every read's
        # tensor part is silent (the isotropic rule, bit for bit)
        self._pace_carry: dict[tuple[int, int, int], np.ndarray] = {}
        self._axis_effective: dict[int, tuple[int, bool, tuple[np.ndarray, ...] | None]] = {}
        # THE LEAK TEST (the model owner's record 2075 (3); BUILD.md section 26
        # item 55): a held family no body has ever sourced must be exactly zero
        # everywhere; the hold marks the first nonzero source (HOST, a flag per
        # held family, read by `leaks`)
        # per part (9.91 (9) (a)): (family, part), the time part 0
        self._sourced_ever: dict[tuple[int, int], bool] = {
            (family, part): False
            for family in self.held_families
            for part in range(self.families[family].components)
        }
        self.span_masks: dict[int, np.ndarray] = {}
        for number, entry in enumerate(world.measured):
            if entry.block is None:
                span = np.zeros(self.shape, dtype=bool)
                for node in self._span_nodes(entry.position, entry.span):
                    span[node] = True
                self.span_masks[number] = span
        self.records: dict[int, LiveRecord] = {}
        # HOST: `kind_wall` per (family, pair), cleared by `_write_pair`
        self._kind_walls: dict[tuple[int, int, int], int] = {}
        # the records clicked this interval, deleted whole after the advances
        self.dead: list[int] = []
        self.blocks: list[Block] = []
        self.block_by_number: dict[int, Block] = {}
        # The block's count at a light record's first rung at its detector
        # (the click's `clock`, the body's event in the body's own clock).
        self.rung_counts: dict[tuple[int, int], int] = {}
        # The record kinds (massive-record-v1): per family the pair on the
        # six-neighbour term as two dense int64 arrays over the board
        # (light's kind the value [1, 1] everywhere; a massive kind its
        # declared pair; a block's Nodes a lowered pair there, the build's
        # step 3) and the faces its rows read (the world's `boundary`, one
        # border for every family, BUILD.md section 26 item 28).
        # THE PAIR ARRAYS BY (FAMILY, PAIR) (ALGEBRA.md 9.85 (3), 9.91 (7); the
        # one stroke, commit 1): a record's rows step with its own rest pair
        # everywhere but at the bodies of its family, whose wells (the lowered
        # pair) are written into every array of the family; the arrays are made
        # once per (family, pair) on first use (`pair_arrays`); `kind_num` and
        # `kind_den` read a family's own declared pair (the tests' view)
        self._pairs: dict[tuple[int, int, int], tuple[np.ndarray, np.ndarray]] = {}
        self.kind_num = PairView(self, 0)
        self.kind_den = PairView(self, 1)
        self.kind_wrap: list[tuple[bool, bool, bool]] = [
            world.kind_periodic(index) for index in range(len(world.families))
        ]
        # The blocks (massive-record-v1): every measured event with a block,
        # its Nodes written into its kind's pair arrays, its own record
        # seeded on its Nodes and its momentum on its wall W = 3 Q M (`wall_of`).
        for number, entry in enumerate(world.measured):
            if entry.block is None:
                continue
            definition = entry.block
            corner = [int(entry.position[axis]) for axis in range(3)]
            mask = self._box(corner, definition.extents, entry.family)
            block = Block(
                number,
                entry.family,
                definition,
                corner,
                mask,
                int(self.detector_at_node[tuple(entry.position)]),
                [int(component) for component in entry.momentum],
            )
            block.spin = list(definition.spin)
            block.spin_before = list(definition.spin)
            block.fixed = bool(entry.fixed)
            self._write_pair(block)
            if definition.seed > 0 and world.body_record:
                # THE BODY RECORD (ALGEBRA.md 9.46 (1), (7) (c); BUILD.md section
                # 26 item 37): the load's one write, the rotation at the
                # profile's value at the body's centre Node at both levels with
                # the remainder 0 (the lattice body's standing start, both
                # levels the profile), the profile a declared constant read at
                # the giving click alone (9.60 (6)), no rows elsewhere on the
                # GameBoard
                assert definition.profile is not None and definition.clock is not None
                profile = np.array(definition.profile, dtype=np.int64).reshape(self.shape)
                centre = tuple(int(axis[0]) for axis in np.nonzero(self.centre_mask(block)))
                level = int(profile[centre])
                block.node_record = NodeRecord(number * (1 << 32), level, level)
                block.previous_sum = level
                if definition.emitter is not None:
                    self._excite(block, block.node_record)
            elif definition.seed > 0:
                own_record = self._massive_record(
                    number * (1 << 32), number, entry.family, definition.kind, definition.twist
                )
                if definition.profile is not None:
                    # the declared integer profile over the whole board at both
                    # levels (a standing start on the bound mode: MASSIVE_RECORD.md
                    # section 11 item 7), the world file's integers and nothing else
                    profile = np.array(definition.profile, dtype=np.int64).reshape(self.shape)
                    own_record.now[:] = profile
                    own_record.before[:] = profile
                else:
                    own_record.now[mask] = definition.seed
                    own_record.before[mask] = definition.seed
                own_record.standing = True  # a body's own record, read by no detector (item 51)
                block.own = own_record
                self.records[own_record.identity] = own_record
                block.previous_sum = int(np.sum(own_record.now[mask]))
                if definition.emitter is not None:
                    # the first excited record (ALGEBRA.md 9.17 (4) item 1): the
                    # seed at both levels, its residue the first of the wheel,
                    # its norm the seed's squares over the body's Nodes
                    self._excite(block, own_record)
            self.blocks.append(block)
            self.block_by_number[number] = block
        # The blocks' Nodes: a block's Nodes carry its detector's index (the flux
        # into them booked to it, never chosen: the detector is on no ladder); a
        # set bound to a block without positions owns the block's Nodes
        # instead (the flux into them booked to the set; a set bound to a block is a receiver). Nothing
        # takes (ALGEBRA.md 9.19 (3)): the rows evolve at every detector.
        if self.blocks:
            for block in self.blocks:
                for node in zip(*np.nonzero(block.mask), strict=True):
                    address = (int(node[0]), int(node[1]), int(node[2]))
                    self.detector_at_node[address] = block.detector
            for set_detector, number in self.set_block.items():
                if self.set_nodes[set_detector] is None:
                    block = self.block_by_number[number]
                    self.detector_at_node[block.mask] = set_detector
        # The receiver by name (DECLARATIONS.md section 13 item 7): an
        # emitting block's `receiver` names the detector set whose one detector
        # is the ladder of every record it emits (the click line at that
        # detector's first rung after the train; the faces and every other set
        # sinks for it, their take into `absorbed` alone and onto no pointer).
        # A block without the key keeps the ladder of every detector and the line
        # at the close, as before the key (the registered worlds byte for byte).
        self.receiver_detector: dict[int, int] = {}
        for block in self.blocks:
            name = block.definition.receiver
            if name is None:
                continue
            if name not in self.detector_names:
                raise ValueError(
                    f"measured[{block.number}].receiver {name!r} names no detector of the "
                    f"simulation (the detectors: {self.detector_names})"
                )
            self.receiver_detector[block.number] = self.detector_names.index(name)
        self.has_receiver = bool(self.receiver_detector)
        # the held families' records (item 51): the load's write, each family's
        # declared source held at every body's Nodes and 0 elsewhere (ALGEBRA.md
        # 9.45 (2), 9.48 (2)); the identities below 0, one per held family
        self.held_records: dict[int, LiveRecord] = {
            family: self._held_part(position, family, 0)
            for position, family in enumerate(self.held_families)
        }
        # THE OTHER PARTS of a held family (ALGEBRA.md 9.86 (2), 9.91 (1); commit
        # 1): one record per component beyond the time part (gravity's nine,
        # the charge's three), zero and silent until a hold writes them (the
        # vector and tensor holds, commit 2); stepped with the time part
        self.held_parts: dict[int, list[LiveRecord]] = {
            family: [
                self._held_part(position, family, part)
                for part in range(1, self.families[family].components)
            ]
            for position, family in enumerate(self.held_families)
        }
        for parts in self.held_parts.values():
            for record in parts:
                record.silent = True
        # the register: the folders' primitives by name, the step file's acts bound to the loop's stages
        self.register = self._engine_register()
        self.register.check_step(world.step)
        self.register.check_writers(world.step)
        self.register.check_terms(self.family_terms())
        self._acts = self._stage_table()
        self._hold(self.register.at("the hold", "(iv)"), advance=True)

    # The register of primitives: one register, name to function, read by the loop alone

    def _wait(self) -> int:
        """WAIT is one interval, always (ALGEBRA.md 9.112 item 1): a value sent at the start of t is combined in t."""
        return 1

    def _method(self, name: str) -> Callable[..., object]:
        """The loop's method `name` resolved at each call (a test's spy set on the instance is honoured); the folders' own functions replace it cut by cut."""

        def call(*args: object, **kwargs: object) -> object:
            return getattr(self, name)(*args, **kwargs)

        return call

    def _engine_register(self) -> Register:
        """The register filled from the features' folders and bound to this loop: a built primitive's function is its folder's or the loop's method of today; a row not built has none."""
        register = discover()
        register.bind(self)
        return register

    def _stage_table(self) -> tuple[tuple[str, str, Callable[..., None], dict[str, object]], ...]:
        """The file's built acts in the file's order, each bound to the loop's stage of its name with the words the stage takes; a built name without a stage, an act with other words, or a file ordering the record's fused chain otherwise is refused at load."""
        stages: dict[str, tuple[Callable[..., None], tuple[str, ...]]] = {
            "the hop": (self._hop_stage, ()),
            "the hold": (self._hold_stage, ("advance",)),
            "the operation": (self._records_stage, ()),
            "the giving": (self._giving_stage, ()),
            "the spin's step": (self._spins_stage, ()),
        }
        for name in self.CHAIN + ("the recoil",):
            stages.setdefault(name, (self._no_stage, ()))
        built = self.register.built_names()
        missing = [name for name in built if name not in stages]
        if missing:
            raise ValueError(
                f"the loop has no stage for the built primitives {missing}: every built primitive of "
                "the step file is bound to one act of the loop"
            )
        acts: list[tuple[str, str, Callable[..., None], dict[str, object]]] = []
        for place, name, words in self.world.step.acts:
            if name not in built:
                continue
            stage, taken = stages[name]
            if sorted(dict(words)) != sorted(taken):
                raise ValueError(
                    f"the step file's act {name!r} at {place} carries the words {sorted(dict(words))}; "
                    f"the loop's stage of {name!r} takes {sorted(taken)}"
                )
            acts.append((place, name, stage, dict(words)))
        chain = [index for index, act in enumerate(acts) if act[1] in self.CHAIN]
        ordered = [acts[index][1] for index in chain]
        between = (
            [
                act[1]
                for act in acts[chain[0] : chain[-1] + 1]
                if act[2] != self._no_stage and act[1] != "the operation"
            ]
            if chain
            else []
        )
        if ordered != [name for name in self.CHAIN if name in built] or between:
            raise ValueError(
                f"the record's step is one chain today: {', '.join(self.CHAIN)}; the file orders them as "
                f"{', '.join(ordered) or 'none of them'}"
                + (f", with {', '.join(between)} between them" if between else "")
            )
        return tuple(acts)

    def _hop_stage(self, function: Callable[..., None]) -> None:
        """The hop's act: each body's step by its drive."""
        for block in self.blocks:
            function(block)

    def _hold_stage(self, function: Callable[..., None], advance: bool) -> None:
        """The hold's two acts: at the interval's start the moved bodies' Nodes rewritten; after the records, the held families' own step, the hold and the pace guard."""
        if advance:
            self._advance_fields(function)
        else:
            self._hold(function)

    def _records_stage(self, function: Callable[..., None]) -> None:
        """The records' act: the bodies' own records first, each by the rule alone, then every live record's fused step (its click included); `function` is the rule the steps apply."""
        for block in self.blocks:
            if block.node_record is not None:
                self._advance_node_record(block)
            elif block.own is not None:
                self._advance(block.own)
            else:
                continue
            if block.definition.emitter is not None:
                self._excitation_rung(block)
        for identity in list(self.records):
            live = self.records[identity]
            if live.arm_done or live.standing:
                continue
            self._advance(live)

    def _giving_stage(self, function: Callable[..., None]) -> None:
        """The giving's act: the point emitters' windows close after the interval's bookings, then each body due gives."""
        self._point_windows()
        for block in self.blocks:
            if block.emit_now:
                function(block)

    def _spins_stage(self, function: Callable[..., None]) -> None:
        """The spin's step's act: each body's momentum and spin from the fields as the interval leaves them."""
        for block in self.blocks:
            function(block, False)

    def _no_stage(self, function: Callable[..., None]) -> None:
        """A primitive with no whole-board act of its own: called per record or part inside another act (the record's step, the hold), or, the recoil, by no act of the loop yet."""

    def _close_interval(self) -> None:
        """The interval's closing: each body's clock, the clicked records deleted whole, then the host's probe and mode readings."""
        for block in self.blocks:
            self._block_clock(block)
        for identity in self.dead:
            if identity in self.records:
                self._release(self.records.pop(identity))
        self.dead = []
        if self.world.probes and self.record is not None:
            values = []
            for probe in self.world.probes:
                value = 0
                for live in self.records.values():
                    if not self.families[live.family].massive_kind:
                        value += int(live.now[probe])
                values.append(value)
            self.record({"event": "probe", "tick": self.tick, "values": values})
        if self.world.mode_axis is not None and self.record is not None:
            axis = self.world.mode_axis
            field = np.zeros(self.shape, dtype=np.int64)
            for live in self.records.values():
                if not self.families[live.family].massive_kind:
                    field += live.now
            sums = []
            for residue in range(3):
                index = [slice(None)] * 3
                index[axis] = slice(residue, None, 3)
                sums.append(int(np.sum(field[tuple(index)].astype(object))))
            self.record({"event": "mode", "tick": self.tick, "axis": AXES[axis], "sums": sums})

    def family_terms(self) -> list[tuple[str, str]]:
        """The primitives each family of the run declares, as (label, name) pairs
        read from its attributes (the loader's words of today; the term form
        [name, target, of, degree, weight, table] of 9.110 item 7 is the loader's
        next cut): every family the shape and the step's four words; `reads` the
        signed read; `held` the hold; `self_source.unit` the self-source; `clicks`
        the clicks; `lifetime` the lifetime."""
        terms: list[tuple[str, str]] = []
        for index, family in enumerate(self.families):
            label = f"universe.families[{index}]"
            for name in (
                "the pair",
                "the degree",
                "the phase",
                "the send",
                "the receive",
                "the wait",
                "the operation",
            ):
                terms.append((label, name))
            if family.reads:
                terms.append((f"{label}.reads", "the signed read"))
            if family.held is not None:
                terms.append((f"{label}.held", "the hold"))
            if family.self_unit > 0:
                terms.append((f"{label}.self_source", "the self-source"))
            if family.clicks is not None:
                terms.append((f"{label}.clicks", "the clicks"))
            if family.lifetime is not None:
                terms.append((f"{label}.lifetime", "the lifetime"))
        for number, entry in enumerate(self.world.measured):
            if entry.block is not None and entry.block.emitter is not None:
                terms.append((f"measured[{number}].emitter", "the giving"))
        return terms

    def wall_of(self, block: Block) -> int:
        """THE ONE WALL OF A BODY (ALGEBRA.md 9.96 (1), 9.89 (2)): W = 3 Q M, Q the
        universe's momentum unit and M the body's quanta as it holds them now (its
        own and its stocks, 9.51 (8); a click moves M, 9.91 (4), 9.96 (5)); the hop,
        the holds' divisions and the recoil read this one wall, the momentum's
        whole part n on it the body's velocity n / W in Links per interval."""
        return 3 * self.momentum_unit * sum(self.held[block.number])

    def _held_part(self, position: int, family: int, part: int) -> LiveRecord:
        """A held family's component record over the board (item 51; 9.91 (1)):
        the identities below 0, one per held family and part; its pair the one
        its family's row declares (`pair` None reads it), no shortcut."""
        return LiveRecord(
            -1 - position - 100 * part,
            -1 - position,
            family,
            0,
            0,
            self.tick,
            0,
            *self.families[family].pair,
            0,
            1,
            np.zeros(self.shape, dtype=np.int64),
            np.zeros(self.shape, dtype=np.int64),
            np.zeros(self.shape, dtype=np.int64),
            pointers=[0] * len(self.detector_names),
            first_rung=[None] * len(self.detector_names),
            part=part,
            held_part=True,
        )

    def held_component_records(self) -> list[LiveRecord]:
        """Every held family's component records in the declared order, the
        time part first, then the other parts (the interval's field step)."""
        found: list[LiveRecord] = []
        for family, record in self.held_records.items():
            found.append(record)
            found.extend(self.held_parts[family])
        return found

    # The held families (ALGEBRA.md 9.35 (2), 9.45, 9.48; BUILD.md section 26
    # items 31, 32, 35 and 51): the operations, written once for any family

    def body_source(self, number: int, source: str) -> int:
        """A body's declared source for a held family (item 51): its content,
        the quanta it holds of every family ("content", ALGEBRA.md 9.45 (2)),
        or its signed charge Q ("sign", 9.48 (1))."""
        if source == "sign":
            return self._body_charge(number)
        return sum(self.held[number])

    def _hold(self, line: Callable[..., object], advance: bool = False, inverse: bool = False) -> None:
        """THE HOLD (ALGEBRA.md 9.45 (2), 9.48 (2); item 51; the vector and tensor
        parts and the dipoles, 9.91 (3)): at every body's
        Nodes a held family's level is the body's declared source (a block's
        Nodes as they stand this interval, a measured event's span), written
        whole at both levels with the remainder 0: the one place where a
        family's level is not the step's own, the same write as the load's,
        at the load and at every click (up by one at a taking, down by one at
        a giving). `node_level` is then each held family's level as every
        reading family's step reads it at the Node. The parts beyond the time
        part and the dipoles are the hold's line `line` (features/hold), one call
        per body and held family with the act the loop names: the advance (the
        load's first value twice), the rewrite of a moved body's Nodes at the
        interval's start, the inverse."""
        act = THE_INVERSE if inverse else THE_ADVANCE if advance else THE_REWRITE
        for family, record in self.held_records.items():
            source = self.families[family].held
            assert source is not None
            for number in range(len(self.held)):
                value = self.body_source(number, source)
                if value:
                    self._sourced_ever[(family, 0)] = True
                block = self.block_by_number.get(number)
                mask = block.mask if block is not None else self.span_masks[number]
                record.now[mask] = value
                record.before[mask] = value
                record.remainder[mask] = 0
            self.node_level[family] = record.now
            if not self.held_parts[family]:
                continue
            # THE VECTOR AND TENSOR PARTS AT THE BODIES (ALGEBRA.md 9.91 (3)): the
            # body's numbers times the held factors over the wall, the remainder
            # carried, at every Node of the body at both levels; the interval's start
            # rewrites a moved body's Nodes alone (a body at rest keeps them)
            held = {
                block.number: self._held_writes(line, block, family, act)
                for block in self.blocks
                if advance or inverse or any(block.hop)
            }
            momentum_of: dict[int, tuple[int, int, int]] = {}
            for block in self.blocks:
                momentum = self._momentum_now(block)
                momentum_of[block.number] = (int(momentum[0]), int(momentum[1]), int(momentum[2]))
            for block in self.blocks:
                writes = held.get(block.number)
                if writes is None:
                    continue
                for part, value, before in writes.parts:
                    record = self.held_parts[family][part - 1]
                    group, axes = self._part_axes(family, part)
                    factor = self.families[family].held_factors[group]
                    if booking(factor, writes.time_level, momentum_of[block.number], axes):
                        self._sourced_ever[(family, part)] = True
                    if value == 0 and before == 0 and record.silent:
                        continue
                    record.silent = False
                    record.now[block.mask] = value
                    record.before[block.mask] = before
                    record.remainder[block.mask] = 0
            # THE DIPOLES on the body's Node's six neighbours, added after the parts:
            # forward with the division advanced, at the inverse with the values the
            # unhold stepped back; none beyond an open face (a hopping body's dipoles
            # at its new Node wait on the next hold)
            if advance or inverse:
                for block in self.blocks:
                    dipoles = held[block.number].dipoles
                    centre = self._centre_node(block) if dipoles else []
                    for (i, j, sigma), value, before in dipoles:
                        node = self._dipole_node(centre, family, j, sigma)
                        if node is None:
                            continue
                        record = self.held_parts[family][i]
                        self._sourced_ever[(family, record.part)] = True
                        if value == 0 and before == 0:
                            continue
                        record.silent = False
                        record.now[node] += value
                        record.before[node] += before
        self._effective.clear()

    def _held_writes(
        self, line: Callable[..., object], block: Block, family: int, act: str
    ) -> HoldWrites:
        """One body's hold into one held family by the hold's line, the act named by the
        loop: the family's row, the body's count, its momentum now, its wall and its
        dipole's vector, and its remainders of the family under the line's keys (a
        part's index, ("d", i, j, sigma) a dipole's term), written back after the call;
        a dipole's term beyond an open face is dropped with its Node (9.91 (3))."""
        definition = self.families[family]
        source = definition.held
        assert source is not None
        values: dict[tuple[object, ...], int] = {}
        carries: dict[tuple[object, ...], int] = {}
        for stored, found in ((block.hold_value, values), (block.hold_carry, carries)):
            for key, value in stored.items():
                if key[0] == family:
                    found[key[1:]] = value
                elif key[0] == "d" and key[1] == family:
                    found[("d", *key[2:])] = value
        vector: tuple[int, int, int] | None = None
        if definition.held_dipole == "spin":
            vector = (int(block.spin[0]), int(block.spin[1]), int(block.spin[2]))
        elif definition.held_dipole is not None:
            moment = block.definition.moment
            vector = (int(moment[0]), int(moment[1]), int(moment[2]))
        momentum = self._momentum_now(block)
        term = HoldTerm(
            source,
            tuple(definition.parts),
            tuple(definition.held_factors),
            definition.held_dipole,
            definition.held_dipole_div,
        )
        start = HoldStart(
            act,
            self.body_source(block.number, source),
            (int(momentum[0]), int(momentum[1]), int(momentum[2])),
            self.wall_of(block),
            vector,
        )
        writes = cast(HoldWrites, line(term, start, HoldOwn(values, carries)))
        centre = self._centre_node(block) if any(key[0] == "d" for key in writes.own.values) else []
        stores = ((block.hold_value, writes.own.values), (block.hold_carry, writes.own.carries))
        for stored, written in stores:
            for key, value in written.items():
                if key[0] != "d":
                    stored[(family, *key)] = value
                elif self._dipole_node(centre, family, *cast(tuple[int, int], key[2:4])) is not None:
                    stored[("d", family, *key[1:])] = value
        return writes

    def _centre_node(self, block: Block) -> list[int]:
        """The body's Node, the centre of its named set."""
        return [int(axis[0]) for axis in np.nonzero(self.centre_mask(block))]

    def _dipole_node(
        self, centre: list[int], family: int, j: int, sigma: int
    ) -> tuple[int, int, int] | None:
        """The Node + sigma e_j of a body's Node on the family's faces, None beyond an open face."""
        node = list(centre)
        node[j] += sigma
        if self.kind_wrap[family][j] or self.shape[j] == 1:
            node[j] %= self.shape[j]
        elif not 0 <= node[j] < self.shape[j]:
            return None
        return node[0], node[1], node[2]

    def _part_axes(self, family: int, part: int) -> tuple[int, tuple[int, ...]]:
        """A component's part group (0 the time part, 1 the vector, 2 the tensor)
        and the axes it multiplies (ALGEBRA.md 9.91 (1), (3): n_a for the vector,
        n_a n_b for the tensor), by the family's parts list."""
        offset = 0
        for group, count in enumerate(self.families[family].parts):
            if part < offset + count:
                index = part - offset
                if group == 0:
                    return 0, ()
                if group == 1:
                    return 1, (index,)
                return 2, TENSOR_AXES[index]
            offset += count
        raise ValueError(f"the part {part} is beyond the family's components")

    def _unhold_dipoles(self, line: Callable[..., object]) -> None:
        """The interval's dipole writes taken back (the inverse, before the fields
        step back) by the hold's line, the unhold act: each term's value off the
        `now` level alone (the `before` level holds the level the step read, which
        the inverse needs) and its division stepped back to the previous interval."""
        for family in self.held_records:
            if not self.held_parts[family]:
                continue
            for block in self.blocks:
                dipoles = self._held_writes(line, block, family, THE_UNHOLD).dipoles
                centre = self._centre_node(block) if dipoles else []
                for (i, j, sigma), value, _ in dipoles:
                    node = self._dipole_node(centre, family, j, sigma)
                    if node is not None:
                        self.held_parts[family][i].now[node] -= value

    def leaks(self) -> list[str]:
        """THE LEAK TEST (the model owner's record 2075 (3): "a family with no
        source stays exactly zero; that is a test in every run: no leak, no
        family doing what it should not"; BUILD.md section 26 item 55): the
        names of the families that carry rows without a source. A held family
        no body has ever sourced (every body's declared source 0 at every
        hold so far) whose record has a nonzero level or remainder anywhere; a
        family the step alone moves with no body of it, no body holding its
        quanta and no emitter giving into it, that has a record. Read by
        attribute, never by a name; a HOST reading of the state, no line."""
        found: list[str] = []
        for family, record in self.held_records.items():
            if self._sourced_ever[(family, 0)]:
                continue
            if record.now.any() or record.before.any() or record.remainder.any():
                found.append(self.families[family].name)
        # every other part of a held family with no source of its own stays
        # exactly zero (9.91 (9) (a): the leak test per part)
        for family, parts in self.held_parts.items():
            for record in parts:
                if self._sourced_ever[(family, record.part)]:
                    continue
                if record.now.any() or record.before.any() or record.remainder.any():
                    name = f"{self.families[family].name}[{record.part}]"
                    if name not in found:
                        found.append(name)
        sourced = set(self.held_families)
        for number, entry in enumerate(self.world.measured):
            sourced.add(entry.family)
            sourced.update(index for index, quanta in enumerate(self.held[number]) if quanta)
            if entry.block is not None and entry.block.emitter is not None:
                sourced.add(entry.block.emitter.family)
        for live in self.records.values():
            if live.family not in sourced:
                name = self.families[live.family].name
                if name not in found:
                    found.append(name)
        return found

    def held_record(self, source: str) -> LiveRecord | None:
        """The held record of the family holding `source` ("content" or
        "sign"), None where no family holds it; a GAMEBOARD reading by the
        declared attribute, never by a name."""
        for family, record in self.held_records.items():
            if self.families[family].held == source:
                return record
        return None

    def level_of(self, source: str) -> np.ndarray:
        """The level over the board of the family holding `source` (the Node
        clock's c for "content", 9.45; the charge field d for "sign", 9.48),
        zeros where no family holds it; a GAMEBOARD reading."""
        for family in self.held_records:
            if self.families[family].held == source:
                return self.node_level[family]
        return np.zeros(self.shape, dtype=np.int64)

    def _advance_fields(self, hold: Callable[..., object]) -> None:
        """The held families' own steps after every other family's (the plain step at every Node), then the hold at the bodies' Nodes, then the guard: every reading family's pace stays positive at every Node, else the run is refused."""
        for record in self.held_component_records():
            self._advance(record)
        self._hold(hold, advance=True)
        for family, definition in enumerate(self.families):
            if not definition.reads:
                continue
            most = int(np.max(np.abs(self._effective_content(family))))
            axis_contents = self._axis_contents(family)
            if axis_contents is not None:
                # every axis pace p_a = Gamma - c - t_a stays positive too (9.91 (2))
                content = self._effective_content(family)
                most = max(most, *(int(np.max(np.abs(content + t))) for t in axis_contents))
            if most >= self.node_clock:
                raise RuntimeError(
                    f"the effective content {definition.name!r} reads reached {most} "
                    f"in size at interval {self.tick}, at or beyond Gamma = {self.node_clock}: "
                    "the pace Gamma minus the weighted held levels of every read stays positive "
                    "under the fixed wall (ALGEBRA.md 9.45 (3), 9.48 (3); BUILD.md section 26 "
                    "items 34, 35 and 51); the run is refused"
                )

    def _neighbour_nodes(
        self, node: tuple[int, ...], wrap: tuple[bool, bool, bool]
    ) -> list[tuple[int, int, int]]:
        """The six reads of a Node as `_neighbours` makes them: the wrap on a
        periodic axis, the Node itself twice on a folded axis of extent 1,
        none beyond an open face."""
        nodes: list[tuple[int, int, int]] = []
        for axis in range(3):
            for side in (1, -1):
                j = list(node)
                j[axis] += side
                if wrap[axis] or self.shape[axis] == 1:
                    j[axis] %= self.shape[axis]
                elif not 0 <= j[axis] < self.shape[axis]:
                    continue
                nodes.append((int(j[0]), int(j[1]), int(j[2])))
        return nodes

    def wheel_at(
        self, family: int, node: tuple[int, ...], pair: tuple[int, int] | None = None
    ) -> tuple[int, int]:
        """The remainder's step g and the wheel W of the family's rule at a
        Node under the fixed wall (ALGEBRA.md 9.22 (4), 9.50 (8) and (13);
        BUILD.md section 26 items 34 and 36): the wall 3 den Gamma, the step
        g the gcd of the total's coefficients (p_i num on the six reads, 6
        den c_i at the Node and the wall itself: the remainder moves on the
        multiples of g), W = wall / g values; the pair's own 3 den / gcd(num, 3 den) in
        the vacuum (2403 on [800, 801]), content-dependent at and beside a
        body; read from the rule, never declared."""
        num_all, den_all = self.pair_arrays(family, pair)
        num = int(num_all[node])
        den = int(den_all[node])
        gamma = self.node_clock
        effective = self._effective_content(family)
        content = int(effective[node])
        # the rule's three integers at the Node (9.57 (1); item 44): the
        # coefficient on the six reads, the coefficient at the Node and the
        # wall; the remainder moves on the multiples of their gcd
        axis_contents = self._axis_contents(family)
        reads, self_coefficient, wall = coefficients(
            num,
            den,
            gamma,
            content,
            ISOTROPIC if axis_contents is None else tuple(int(t[node]) for t in axis_contents),
        )
        step = gcd(wall, self_coefficient, *reads)
        return step, wall // step

    def node_clock_pair(self, node: tuple[int, ...], family: int) -> tuple[int, int]:
        """The clock pair a record of `family` reads at a Node under the fixed
        wall (items 34 and 35): (e, f) = (Gamma - c + q Lambda d, Gamma), the
        pace over the wall's Gamma; f - e the effective content there."""
        return self.node_clock - int(self._effective_content(family)[node]), self.node_clock

    def _effective_content(self, family: int) -> np.ndarray:
        """The content a record of `family` reads at every Node, the signed read's own `content_of` (features/signed_read; ALGEBRA.md 9.117 row 1, 9.48 (3)), one array per family per interval."""
        cached = self._effective.get(family)
        if cached is not None:
            return cached
        definition = self.families[family]
        term = SignedReadTerm(
            tuple((other, weight, by) for other, weight, by, _twist in definition.reads),
            self.family_charge[family],
            (int(definition.pair[0]), int(definition.pair[1])),
            self.node_clock,
        )
        content = content_of(term, SignedReadStart(self.shape, self.node_level, None))
        self._effective[family] = content
        return content

    def _body_charge(self, number: int) -> int:
        """A body's charge Q (ALGEBRA.md 9.48 (1)): the sum of the signs of the
        quanta it holds, an integer of either sign, moved with the labels at
        the clicks (the held books)."""
        block = self.block_by_number.get(number)
        declared = block.definition.q if block is not None else 0
        return declared + sum(
            sign * quanta for sign, quanta in zip(self.family_charge, self.held[number], strict=True)
        )

    def _receiver_of(self, live: LiveRecord) -> int | None:
        """The one detector of the record's ladder under the receiver by name
        (its emitting block's `receiver`); None for a record without one (a
        lamp's record, or a block's without the key: the ladder every detector,
        the line at the close)."""
        if live.emitter is None:
            return None
        return self.receiver_detector.get(live.emitter)

    def _detector(
        self, name: str, measured: int | None, face: bool, set_name: str | None = None, channel: int = 0
    ) -> int:
        self.detector_names.append(name)
        self.detector_measured.append(measured)
        self.detector_face.append(face)
        self.detector_set.append(name if set_name is None else set_name)
        self.detector_channel.append(channel)
        return len(self.detector_names) - 1

    def _span_nodes(
        self, position: tuple[int, int, int], span: tuple[int, int, int]
    ) -> list[tuple[int, int, int]]:
        found: list[tuple[int, int, int]] = []
        for dx in range(int(span[0])):
            for dy in range(int(span[1])):
                for dz in range(int(span[2])):
                    node = (int(position[0]) + dx, int(position[1]) + dy, int(position[2]) + dz)
                    if all(0 <= node[a] < self.shape[a] for a in range(3)):
                        found.append(node)
        return found

    # The blocks (massive-record-v1)

    def _box(self, corner: list[int], extents: tuple[int, int, int], family: int) -> np.ndarray:
        """The Nodes R of a block: the box of `extents` per axis (a cube's
        side three times; the slabs of ALGEBRA.md 9.22 (8)) from its lower
        corner, wrapped on an axis the world's border makes periodic, cut on an
        open one (a G_48-set of Nodes, world data)."""
        mask = np.zeros(self.shape, dtype=bool)
        wrap = self.kind_wrap[family]
        ranges = []
        for axis in range(3):
            extent = self.shape[axis]
            indices = [corner[axis] + offset for offset in range(extents[axis])]
            if wrap[axis]:
                indices = [index % extent for index in indices]
            else:
                indices = [index for index in indices if 0 <= index < extent]
            ranges.append(sorted(set(indices)))
        if all(ranges):
            mask[np.ix_(ranges[0], ranges[1], ranges[2])] = True
        return mask

    def pair_arrays(
        self, family: int, pair: tuple[int, int] | None = None
    ) -> tuple[np.ndarray, np.ndarray]:
        """THE PAIR ARRAYS of a record of `family` at its rest pair (ALGEBRA.md
        9.85 (3), 9.91 (7); commit 1): num and den over the board, the pair
        everywhere but at the family's bodies, whose declared pairs (the wells
        and the gaps) are written at their Nodes; made once per (family, pair)
        and kept up with the bodies' steps (`_write_pair`). `pair` None reads
        the family's own declared pair (refused on a family whose pair is the
        body's: every record of it carries its own)."""
        if pair is None:
            definition = self.families[family]
            if definition.pair_on_body:
                raise ValueError(
                    f"the family {definition.name!r} declares no pair of its own; a "
                    "record's pair is read from the record (ALGEBRA.md 9.85 (3), 9.91 (7))"
                )
            pair = definition.pair
        key = (family, int(pair[0]), int(pair[1]))
        found = self._pairs.get(key)
        if found is None:
            num = np.full(self.shape, key[1], dtype=np.int64)
            den = np.full(self.shape, key[2], dtype=np.int64)
            for block in self.blocks:
                if block.family == family:
                    num[block.mask] = block.definition.pair[0]
                    den[block.mask] = block.definition.pair[1]
            found = (num, den)
            self._pairs[key] = found
        return found

    def _write_pair(self, block: Block) -> None:
        """The block's pair written on its Nodes into every pair array of its
        family; the array's own pair elsewhere on the Nodes the block left."""
        for key in [key for key in self._kind_walls if key[0] == block.family]:
            del self._kind_walls[key]  # the family's walls read anew (`kind_wall`)
        for (family, rest_num, rest_den), (num, den) in self._pairs.items():
            if family != block.family:
                continue
            num[~block.mask] = rest_num
            den[~block.mask] = rest_den
            num[block.mask] = block.definition.pair[0]
            den[block.mask] = block.definition.pair[1]
            for other in self.blocks:
                if other is not block and other.family == block.family:
                    num[other.mask & ~block.mask] = other.definition.pair[0]
                    den[other.mask & ~block.mask] = other.definition.pair[1]

    def _massive_record(
        self, identity: int, number: int, family: int, pair: tuple[int, int], twist: int
    ) -> LiveRecord:
        """A record of the massive kind on the board: a block's own record at
        the body's kind (its rest pair) with its twist "own" (9.96 (2) (a)); no
        train, no clock, no Ports."""
        return LiveRecord(
            identity,
            number,
            family,
            0,
            0,
            self.tick,
            0,
            1,
            1,
            0,
            1,
            np.zeros(self.shape, dtype=np.int64),
            np.zeros(self.shape, dtype=np.int64),
            np.zeros(self.shape, dtype=np.int64),
            pointers=[0] * len(self.detector_names),
            first_rung=[None] * len(self.detector_names),
            pair=(int(pair[0]), int(pair[1])),
            twist=twist,
        )

    def stock_of(self, block: Block) -> int:
        """THE STOCK of the family a body gives (ALGEBRA.md 9.51 (8), 9.96 (5)): its
        held quanta of another family; of its own family, its declared `stock` less
        its givings (each giving lowered M by one, the held count of its own)."""
        emitter = block.definition.emitter
        assert emitter is not None
        if emitter.family == block.family:
            return block.definition.stock - block.givings
        return self.held[block.number][emitter.family]

    def _momentum_now(self, block: Block) -> list[int]:
        """The block's momentum at this interval: the declared P, or under a
        ramp the whole part P x t // ramp until the ramp ends (the pushing
        agent's declaration)."""
        ramp = block.definition.ramp
        elapsed = self.tick - block.definition.start
        if elapsed < 0:
            return [0, 0, 0]
        if ramp <= 0 or elapsed >= ramp:
            return list(block.momentum)
        return [component * elapsed // ramp for component in block.momentum]

    def _move_block(self, block: Block) -> None:
        """The block's step (MASSIVE_RECORD.md section 5): per axis the
        accumulator gains the momentum's component against the wall W = 3 Q M
        (`wall_of`, ALGEBRA.md 9.96 (1))
        (verb T, then D with the remainder kept, at most one Link per
        interval, `core.integer.by_drive`), x before y before z, a second
        Link in one interval lost to the earlier axis (its wall subtracted,
        the frame's tie); the Nodes and the pair region translate by T; the
        records' rows stay on their Nodes (12.7 (d))."""
        momentum = self._momentum_now(block)
        hop = [0, 0, 0]
        stepped = False
        for axis in range(3):
            count, block.drive[axis] = by_drive(
                block.drive[axis], momentum[axis], self.wall_of(block), at_most=1
            )
            if count and not stepped:
                hop[axis] = count
                stepped = True
        block.hop = (hop[0], hop[1], hop[2])
        if not stepped:
            return
        for axis in range(3):
            if hop[axis]:
                block.corner[axis] += hop[axis]
                if self.kind_wrap[block.family][axis]:
                    block.corner[axis] %= self.shape[axis]
        old_mask = block.mask
        block.mask = self._box(block.corner, block.definition.extents, block.family)
        # HOST (item 48, the bug behind finding 2 of the run toward nature, row 2):
        # the detectors' Port pairs are cached per family (`_inflow_ports`) and
        # were never re-read after a hop, so a moving set's Ports stayed at its
        # place of the load; the cache is cleared at every hop, the Ports read
        # again from the Nodes as they stand (at rest bit for bit as before)
        self._inflow_port_pairs.clear()
        self._inflow_port_faces.clear()
        if int(np.count_nonzero(block.mask)) < int(np.count_nonzero(old_mask)):
            # Reviewer 3's line from the redshift dry run (the Boss's 09:45Z): a
            # stepping block whose Nodes would leave the board by a zero face
            # (the cube cut by `_cube` on a non-periodic axis) refuses the
            # interval naming the block, instead of running on with the block
            # gone and the books balanced; the margin rule refuses the same
            # block at load, not at a hop, so this is the run's own check.
            raise RuntimeError(
                f"measured[{block.number}] stepped off the board at interval "
                f"{self.tick} (its corner {list(block.corner)}, extents {list(block.definition.extents)}, "
                f"{int(np.count_nonzero(block.mask))} of {int(np.count_nonzero(old_mask))} Nodes "
                "left on the board): a block's Nodes must stay on the board; the run is refused"
            )
        self._write_pair(block)
        block.stepped += 1
        # The block's detector follows its Nodes (a set bound to it without
        # positions with them); the Nodes it left are free Nodes.
        for node in zip(*np.nonzero(old_mask & ~block.mask), strict=True):
            address = (int(node[0]), int(node[1]), int(node[2]))
            self.detector_at_node[address] = -1
        set_detector = next(
            (
                detector
                for detector, number in self.set_block.items()
                if number == block.number and self.set_nodes[detector] is None
            ),
            None,
        )
        for node in zip(*np.nonzero(block.mask), strict=True):
            address = (int(node[0]), int(node[1]), int(node[2]))
            self.detector_at_node[address] = block.detector if set_detector is None else set_detector

    # THE BODIES ON ONE NODE (ALGEBRA.md 9.91 (8) (v), 9.78 (4), (5), 9.52 (2), (4); the
    # one stroke, commit 6): the contraction, the feed, the induction, the spin's step,
    # written once for any body and any read

    def _read_factor(self, block: Block, weight: int, by: str) -> int:
        """A read's factor on a body (ALGEBRA.md 9.78 (4)): the weight plainly, or minus
        the body's charge Q times the weight for a read by q (the pace's convention,
        `_effective_content`: like signs a hill)."""
        return weight if by == "plain" else -self._body_charge(block.number) * weight

    def _division_now(
        self, block: Block, key: tuple[object, ...], numerator: int, wall: int, inverse: bool
    ) -> int:
        """This interval's value of a carried division on the body, Rule3's division act on the
        body's remainders (core.rule3 `carried`): forward the division advanced; backward the value
        the forward wrote (the carry then stepped back to the interval's start), so the inverse
        subtracts the same term the step added."""
        value = block.hold_value.get(key, 0)
        act = THE_INVERSE if inverse else THE_ADVANCE
        now, _ = carried(act, key, numerator, wall, block.hold_value, block.hold_carry)
        return value if inverse else now

    def _curl(
        self, records: list[LiveRecord], centre: tuple[int, int, int], wrap: tuple[bool, bool, bool]
    ) -> list[int]:
        """The curl of a vector part at the centre Node from its six neighbours' levels
        (ALGEBRA.md 9.77 (3), 9.91 (8) (v)): (curl V)_x = V_z(+y) - V_z(-y) - V_y(+z) +
        V_y(-z) and cyclic; a read beyond an open face is 0."""

        def at(component: int, axis: int, sigma: int) -> int:
            if records[component].silent or self.shape[axis] == 1:
                return 0
            node = list(centre)
            node[axis] += sigma
            if wrap[axis]:
                node[axis] %= self.shape[axis]
            elif not 0 <= node[axis] < self.shape[axis]:
                return 0
            return int(records[component].now[node[0], node[1], node[2]])

        return [
            at(z, y, 1) - at(z, y, -1) - at(y, z, 1) + at(y, z, -1) for y, z in ((1, 2), (2, 0), (0, 1))
        ]

    def _body_step(self, block: Block, inverse: bool) -> None:
        """THE BODY'S STEP AT (v) (ALGEBRA.md 9.91 (8) (v), 9.78 (5); commit 6), from the
        fields as the interval leaves them (their `now` levels, which the inverse meets
        first): THE SPIN'S STEP, S_(t+1) = S_(t-1) + (2 [(Omega x S_t) + mu x B_q] +
        carry) div (W Gamma), the leapfrog of the body's two integers with the doubled
        term (the Euler line's rate, exactly invertible; 9.78 (5) leaves the choice),
        Omega_i = [factor x (curl V)_i + 3 ((grad c) x n)_i div W] div 8 from a read whose
        dipole is the spin (gravity's vector part and its t part c), B_q = (weight x curl
        V_q) div 2 from a read whose dipole is the moment (the read's weight alone, since
        mu carries Q: ALGEBRA.md 9.104 (2), record 2157), the curls and the gradient at
        the body's Node from its six neighbours, every remainder carried on the body.
        Backward the same term is recomputed from S_t and subtracted, the divisions
        stepped back. THE FEED AND THE INDUCTION of 9.78 (4) are NOT here: built and
        held back, since with them the two tools of every chain world fall together
        (the chain's content field is a tent; the light clock's detector hops toward
        its emitter within 300 intervals) and no resting world stays bit for bit; the
        line waits on the mathematician (BUILD.md section 26 item 65); when it lands it
        acts on a body without the world's word `fixed` alone (9.104 (6) (b); the
        word is read into `Block.fixed`, record 2157)."""
        definition = self.families[block.family]
        if not definition.reads:
            return
        advance = not inverse
        gamma = self.node_clock
        wall = self.wall_of(block)
        centre = self._window_centre(block)
        wrap = self.kind_wrap[block.family]
        # the spin's term from S_t (the leapfrog's middle), before the momentum moves
        spin_now = (
            (block.spin[0], block.spin[1], block.spin[2])
            if advance
            else (block.spin_before[0], block.spin_before[1], block.spin_before[2])
        )
        omega = [0, 0, 0]
        torque = [0, 0, 0]
        momentum = self._momentum_now(block)  # n in the tidal term (grad c) x n
        for position, (other, weight, by, _) in enumerate(definition.reads):
            factor = self._read_factor(block, weight, by)
            read = self.families[other]
            if len(read.parts) < 2 or read.held_dipole is None:
                continue
            # THE TORQUE'S FACTOR (ALGEBRA.md 9.104 (2); the Boss's record 2157): mu x B_q
            # with the read's weight alone, since the moment mu carries the charge Q; the
            # spin's turn keeps the read's factor (the weight by the body's sign for a read by q)
            if factor == 0 if read.held_dipole == "spin" else weight == 0:
                continue
            curl = self._curl(self.held_parts[other][:3], centre, wrap)
            if read.held_dipole == "spin":
                content = self.held_records[other].now
                gradient = [0, 0, 0]
                for axis in range(3):
                    if self.shape[axis] == 1:
                        continue
                    ahead, behind = list(centre), list(centre)
                    ahead[axis] += 1
                    behind[axis] -= 1
                    for node in (ahead, behind):
                        if wrap[axis]:
                            node[axis] %= self.shape[axis]
                    inside = all(0 <= node[axis] < self.shape[axis] for node in (ahead, behind))
                    if inside or wrap[axis]:
                        gradient[axis] = int(content[ahead[0], ahead[1], ahead[2]]) - int(
                            content[behind[0], behind[1], behind[2]]
                        )
                cross = (
                    gradient[1] * momentum[2] - gradient[2] * momentum[1],
                    gradient[2] * momentum[0] - gradient[0] * momentum[2],
                    gradient[0] * momentum[1] - gradient[1] * momentum[0],
                )
                for i in range(3):
                    tidal = self._division_now(
                        block, ("gradc", position, i), 3 * cross[i], wall, inverse
                    )
                    omega[i] += self._division_now(
                        block, ("omega", position, i), factor * curl[i] + tidal, 8, inverse
                    )
            else:
                for i in range(3):
                    torque[i] += self._division_now(
                        block, ("bq", position, i), weight * curl[i], 2, inverse
                    )
        mu = block.definition.moment
        turn = [
            omega[1] * spin_now[2] - omega[2] * spin_now[1] + mu[1] * torque[2] - mu[2] * torque[1],
            omega[2] * spin_now[0] - omega[0] * spin_now[2] + mu[2] * torque[0] - mu[0] * torque[2],
            omega[0] * spin_now[1] - omega[1] * spin_now[0] + mu[0] * torque[1] - mu[1] * torque[0],
        ]
        for i in range(3):
            step = self._division_now(block, ("spin", i), 2 * turn[i], wall * gamma, inverse)
            if advance:
                block.spin[i], block.spin_before[i] = block.spin_before[i] + step, block.spin[i]
            else:
                block.spin[i], block.spin_before[i] = block.spin_before[i], block.spin[i] - step

    def shell_mask(self, block: Block) -> np.ndarray:
        """THE SHELL of a body (ALGEBRA.md 9.38 (2), 9.44 (5)): its Nodes with
        a Port, a Link to a Node outside the body on the board (the wrap on
        an axis the family's border makes periodic; beyond an open face there
        is no Node and no Port; a folded axis of extent 1 carries none, as
        the flux reading's Ports)."""
        mask = block.mask
        wrap = self.kind_wrap[block.family]
        shell = np.zeros(self.shape, dtype=bool)
        for axis in range(3):
            if self.shape[axis] == 1:
                continue
            for side in (1, -1):
                inside = self._shift(mask, axis, -side, fill=True, wrap=wrap)
                shell |= mask & ~inside
        return shell

    def first_shell_node(self, block: Block) -> tuple[int, int, int]:
        """THE FIRST SHELL NODE IN THE DECLARED ORDER (ALGEBRA.md 9.44 (5) (c);
        9.47 (5) (ii): which Node is read is a convention): the first Node of
        the body in the engine's x-major order (`body_node_indices`, the
        loader's and the generator's one convention) that has a Port; it
        follows the body's steps. A body with no shell (every Link inside
        it) is refused: nothing reads its residue."""
        where = np.nonzero(self.shell_mask(block))
        if len(where[0]) == 0:
            raise ValueError(
                f"measured[{block.number}] has no shell (no Node of it has a Port to "
                "a Node outside it), so no Node reads its residue (ALGEBRA.md 9.44 (5) (c))"
            )
        return int(where[0][0]), int(where[1][0]), int(where[2][0])

    def residue_of(self, live: LiveRecord | NodeRecord, block: Block) -> tuple[int, int]:
        """THE RESIDUE FROM THE LAW (ALGEBRA.md 9.22 (4); BUILD.md section 26
        item 15) UNDER THE NODE CLOCK (9.35 (2), (3); item 31), READ AT THE
        FIRST SHELL NODE (9.44 (5) (c); item 33): the record's rule remainder
        r at the body's first shell Node in the declared order, read now, in
        units of the remainder's step g = gcd(Gamma num, 6 den M, 3 den f) at
        that Node (r moves on the multiples of g from 0), and the wheel W =
        3 den f / g values (`wheel_at`: the pair's own 3 den / gcd(num, 3
        den) where the content is 0, 700 on [801, 700] and 2403 on [800,
        801]; at a body's Nodes the wheel of its content, 18774639 on [800,
        801] at Gamma = 10^6 with M = 64); no declaration, no draw; which
        Node is read is a convention (9.47 (5) (ii)), the centre Node
        HISTORY."""
        if isinstance(live, NodeRecord):
            # THE BODY'S NODE'S RECORD (ALGEBRA.md 9.60 (1), 9.46 (2)): its residue its
            # own remainder on its own wheel, read at the body's Node
            step, wheel = self.node_record_wheel(block)
            return live.remainder // step, wheel
        node = self.first_shell_node(block)
        step, wheel = self.wheel_at(live.family, node, live.pair)
        return int(live.remainder[node]) // step, wheel

    def _excite(self, block: Block, own_record: LiveRecord | NodeRecord) -> None:
        """The body's own record at the load, the one write of a body's record
        (ALGEBRA.md 9.43 (4); 9.17 (4) item 1): its norm T one period's
        action of its own mode (the emitter's declared integer `norm`, the
        generator's, under the input stamp; the body's T of 9.46 (1), not
        read by the tick since the count in intervals of 9.44 (5) (c)); its
        first residue and wheel from the law (`residue_of`) are read after
        ITS FIRST ADVANCE (the load's seed has the remainders 0, the file's
        integers; 9.19 (4e), 9.43 (4)); every later residue is read at the
        click (`_emit`). SINCE THE RESEED RETIRED (9.43 (3); BUILD.md section
        26 item 33) this is called at the load alone."""
        emitter = block.definition.emitter
        assert emitter is not None
        if block.definition.profile is None:
            # the mathematician's gate item 8: the excited record is the body's
            # composed mode (ALGEBRA.md 9.9, 9.17 (4) item 1), the generator's
            # profile; a flat seed is no mode and is refused where a body
            # givings (at the engine's construction: the generator parses the
            # world with the scalar seed to compute the profile)
            raise ValueError(
                f"measured[{block.number}].emitter needs the body's `seed` as its "
                "composed mode's profile (one integer per Node, the generator's "
                "`seed_on_the_mode`; a flat scalar seed is no mode and givings nothing lawful, "
                "ALGEBRA.md 9.17 (4) item 1)"
            )
        # THE GIVING IS THE WINDOW'S (ALGEBRA.md 9.85 (5), 9.71 (1); record 2082 (4);
        # commit 7): every emitter gives by the window at its centre Node at its declared
        # weight; the given train is CANCELLED (`_write_given_train_cancelled`, disconnected)
        if emitter.weight is None or emitter.norm_denominator is None:
            raise ValueError(
                f"measured[{block.number}].emitter declares no `weight` or no "
                "`norm_denominator`: the giving is the window's, the body's rotation written into "
                "the given row at its Node at the weight g until the outward norm reaches the "
                "excitation's action norm / norm_denominator (ALGEBRA.md 9.71 (1), 9.85 (5); the "
                "generator's integers; the given train is retired, commit 7)"
            )
        if emitter.norm is None:
            raise ValueError(
                f"measured[{block.number}].emitter declares no `norm`: one period's "
                "action of the body's mode, its conserved form's share at the centre Node summed "
                "over the period, the generator's integer (ALGEBRA.md 9.17 (7) (e) and (f), 9.19 "
                "(3); `excite_on_the_mode` of the massive record generator)"
            )
        if emitter.period is None:
            raise ValueError(
                f"measured[{block.number}].emitter declares no `period`: P, the "
                "nearest integer to 2 pi / omega_b of the body's mode, the generator's integer "
                "(ALGEBRA.md 9.17 (7) (f), 9.44 (5) (c): the tick counts intervals against "
                "(2 u + 1) P / (2 W))"
            )
        block.excitations += 1
        block.residue_pending = True
        own_record.norm = emitter.norm
        block.wait = 0
        block.emit_now = False

    def node_record_clock(self, block: Block) -> tuple[int, int]:
        """THE BODY'S NODE'S PAIR THIS INTERVAL (ALGEBRA.md 9.63 (3); BUILD.md section
        26 item 46): the declared clock pair [num_c, den_c] of the body's mode
        at rest, and on a moving body THE PROPER PAIR of the drive's momentum
        now, the world's `proper_clock` at the momentum's whole part along its
        one axis (under the ramp m = P t // ramp, then P, the same m the drive
        hops with): the moving mode's rotation at its moving centre per
        interval, 2 cos(omega_K - K v), which the generator wrote from the
        mode's own dispersion; the rest pair at m = 0. The cube carries the
        dilation in its rows by the rule; the body's Node carries it in its declared
        pair, the seam of the host form (9.46), and the equivalence test is
        what checks that they agree."""
        clock = block.definition.clock
        assert clock is not None
        table = block.definition.proper_clock
        if table is None:
            return int(clock[0]), int(clock[1])
        index = max(abs(int(component)) for component in self._momentum_now(block))
        num_c, den_c = table[index]
        return int(num_c), int(den_c)

    def node_record_rule(self, block: Block) -> tuple[int, int, int, int]:
        """THE ONE RULE AT THE BODY'S NODE (ALGEBRA.md 9.60 (1), (2); item 42): the
        integers the body's Node's record is stepped with, (num, den, Gamma, c): the
        body's Node's pair this interval as [num_c, 2 den_c] (`node_record_clock`: the body's
        clock pair in the rule's convention, 2 cos omega = num_c / den_c, the
        proper pair of its momentum on a moving body), the world's Gamma and
        the body's Node's own effective content c (Gamma - p at the body's centre
        Node, the family of clicks' level less the charge's read, uniform over
        its Nodes); the wall 3 den Gamma = 6 den_c Gamma."""
        num_c, den_c = self.node_record_clock(block)
        centre = tuple(int(axis[0]) for axis in np.nonzero(self.centre_mask(block)))
        pace, gamma = self.node_clock_pair(centre, block.family)
        return num_c, 2 * den_c, gamma, gamma - pace

    def node_record_coefficients(self, block: Block) -> tuple[int, int]:
        """The one rule's coefficients at the body's Node with the six reads returning
        the body's Node (S_6 = 6 a): (the coefficient on a, the wall) = (6 num (Gamma
        - c) + 6 den c, 3 den Gamma) = (6 num_c p + 12 den_c c, 6 den_c Gamma),
        six times 9.46 (2)'s (K, den_c Gamma): the same rotation as rationals
        (9.60 (2))."""
        num, den, gamma, content = self.node_record_rule(block)
        reads, self_coefficient, wall = coefficients(num, den, gamma, content)
        return 6 * reads[0] + self_coefficient, wall

    def _advance_node_record(self, block: Block, direction: int = 1) -> None:
        """One interval of the body's Node record by rule3 in `direction`, its six reads its own level, (2 a, 2 a, 2 a); the amplitude bound as the rows' (ALGEBRA.md 9.60 (2), 9.50 (8))."""
        node_record = block.node_record
        assert node_record is not None
        num, den, gamma, content = self.node_record_rule(block)
        reads, self_coefficient, wall = coefficients(num, den, gamma, content)
        now, other = (
            (node_record.now, node_record.before)
            if direction == 1
            else (node_record.before, node_record.now)
        )
        result, remainder = rule3(
            reads,
            (2 * now, 2 * now, 2 * now),
            self_coefficient,
            wall,
            now,
            other,
            node_record.remainder,
            direction,
        )
        if direction == 1 and abs(result) > self.world.amplitude_bound:
            raise RuntimeError(
                f"the body's Node record of measured[{block.number}] reached the level {result} "
                f"at interval {self.tick}, above the world's declared amplitude bound A = "
                f"{self.world.amplitude_bound}: the run is refused"
            )
        node_record.remainder = remainder
        if direction == 1:
            node_record.before, node_record.now = node_record.now, result
        else:
            node_record.now, node_record.before = node_record.before, result

    def node_record_wheel(self, block: Block) -> tuple[int, int]:
        """The remainder's step g and the wheel W of the one rule at the body's Node
        (ALGEBRA.md 9.60 (2), 9.22 (4); `wheel_at`'s reading with the six reads
        the body's Node): g the gcd of the rule's coefficients (on a and the wall), W
        = wall / g; 9.46 (2)'s wheel of the body record, the remainder six
        times its (the coefficients and the wall six times)."""
        coefficient, wall = self.node_record_coefficients(block)
        step = gcd(wall, coefficient)
        return step, wall // step

    def node_record_form(self, block: Block) -> int:
        """The body's Node's record's invariant (ALGEBRA.md 9.46 (2), (9) (b); 9.60):
        e = wall (a^2 + b^2) - coefficient a b, the one rule's own at the body's Node
        (a' = (coefficient / wall) a - b leaves it fixed); constant between the
        remainders' jitter (GAMEBOARD)."""
        node_record = block.node_record
        assert node_record is not None
        coefficient, wall = self.node_record_coefficients(block)
        return (
            wall * (node_record.now * node_record.now + node_record.before * node_record.before)
            - coefficient * node_record.now * node_record.before
        )

    def centre_mask(self, block: Block) -> np.ndarray:
        """The excited record's named set (ALGEBRA.md 9.19 (3)): the body's
        centre Node, the lower corner plus the extent // 2 on each axis, one
        Node (the Node itself for a body of side 1); it follows the body's
        steps."""
        return self._box(
            [int(block.corner[axis]) + block.definition.extents[axis] // 2 for axis in range(3)],
            (1, 1, 1),
            block.family,
        )

    def _excitation_rung(self, block: Block) -> None:
        """THE TICK OF THE GIVING END (ALGEBRA.md 9.44 (5) (c), 9.47 (5) (i)
        and (6); BUILD.md section 26 item 33): the body counts its intervals
        since the residue's read against (2 u + 1) P / (2 W), P the
        emitter's `period` (the generator's integer, the mode's period in
        intervals) and W the body's wheel at the read Node; the click fires
        at the first count t with 2 W t >= (2 u + 1) P (the interval
        ceil((2 u + 1) P / (2 W)) after the read, at least one), the same
        at every Node of the body (T2); no running total, no share summed,
        no fraction moved (the click rule on the offer C of 9.17 (7) (f),
        item 24, HISTORY). The first residue after the load is read here
        after the body's first advance (the seed's remainders 0 at the
        write), the count starting from that interval; every later residue
        is read at the click (`_emit`). Nothing fires while the stock is
        spent: the body's own record continues (9.43 (3))."""
        own: LiveRecord | NodeRecord | None = (
            block.node_record if block.node_record is not None else block.own
        )
        emitter = block.definition.emitter
        if own is None or emitter is None or block.emit_now or block.window is not None:
            return
        # the stock is the given family's content held at the body (ALGEBRA.md
        # 9.51 (8); item 47), or the body's own quanta set aside (9.96 (5); commit
        # 6): nothing fires once it is spent
        if self.stock_of(block) <= 0:
            return
        if block.residue_pending:
            own.u, own.wheel = self.residue_of(own, block)
            block.residue_pending = False
            block.wait = 0
            return
        assert emitter.period is not None
        block.wait += 1
        if 2 * own.wheel * block.wait >= (2 * own.u + 1) * emitter.period:
            block.emit_now = True

    def _emit(self, block: Block) -> None:
        """The click of the body's own record and the giving: the given record written once at both levels at the body, its norm and residue from the law, one quantum of the given family moved from the body's stock, the body's own levels, phase and remainders as they are, the count to the next click started here."""
        world = self.world
        emitter = block.definition.emitter
        own: LiveRecord | NodeRecord | None = (
            block.node_record if block.node_record is not None else block.own
        )
        assert emitter is not None and own is not None
        number = block.number
        family = emitter.family
        definition = self.families[family]
        numerator, denominator = emitter.clock  # the given clock, the emitter's (item 59)
        steps = world.phase_steps
        period = (steps * denominator + numerator - 1) // numerator
        cost = definition.quantum
        excitation = block.excitations
        # the given record's residue and wheel from the law (9.22 (4), 9.44 (5)
        # (c)): the body's own remainder at its first shell Node in the
        # declared order, read at the click on the body's wheel there
        residue, wheel = self.residue_of(own, block)
        wait = block.wait
        # the read Node: the first shell Node of the lattice body (item 33),
        # the body's Node (the centre Node) of a body on one Node (9.60; item 42)
        read_node = (
            tuple(int(axis[0]) for axis in np.nonzero(self.centre_mask(block)))
            if block.node_record is not None
            else self.first_shell_node(block)
        )
        # the held content's level at the read Node and at its reads as the
        # wheel was read, before the giving lowers the content (item 34;
        # GAMEBOARD; the family holding "content", item 51)
        content_level = self.level_of("content")
        read_clocks = [
            int(content_level[read_node]),
            [
                int(content_level[j])
                for j in self._neighbour_nodes(read_node, self.kind_wrap[block.family])
            ],
        ]
        # the body's clock pair as the clicking record was advanced (the
        # content at its centre Node; GAMEBOARD, on the giving line)
        centre = tuple(int(axis[0]) for axis in np.nonzero(self.centre_mask(block)))
        clock_pair = self.node_clock_pair(centre, block.family)
        # the content and the charge the clicking record was advanced under
        # (before this giving lowers them; item 35's line reads them here,
        # the pair no longer the content alone for a charged family)
        centre_content = int(content_level[centre])
        body_charge = self._body_charge(number)
        # the body's own record is not ended and never rewritten (9.43 (3))
        block.givings += 1
        identity = number * (1 << 32) + block.givings
        live = LiveRecord(
            identity,
            number,
            family,
            residue,
            block.givings,
            self.tick,
            cost,
            numerator,
            denominator,
            0,
            period,
            np.zeros(self.shape, dtype=np.int64),
            np.zeros(self.shape, dtype=np.int64),
            np.zeros(self.shape, dtype=np.int64),
            pointers=[0] * len(self.detector_names),
            first_rung=[None] * len(self.detector_names),
            wheel=wheel,
            labels=tuple(emitter.branches),
            emitter=number,
            pair=(int(emitter.pair[0]), int(emitter.pair[1])),
            # the component along the body's moment and the twist "own" (ALGEBRA.md
            # 9.82 (3) (d), 9.96 (2) (a); commit 4), the loader's integers
            part=emitter.part,
            twist=emitter.twist,
        )
        # E^T: the given clock's character on the body's Nodes, written once at
        # both levels, every Node at the vertex's phase (the one-Node broadband
        # giving; a line's travelling character, the per-Link pair of ALGEBRA.md
        # 9.17 (4) item 2, is owed until that pair is declared)
        # NO TABLE IN THE ENGINE (the cleanup order's step 2; ALGEBRA.md 9.17
        # (6), 9.22 (2)): the given pair is the world's two integers `given:
        # [now, before]`, the generator's, checked at load (before = -now),
        # written on every Node of the body
        # THE GIVEN TRAIN (ALGEBRA.md 9.17 (6a); BUILD.md section 26 item 27):
        # the train's two levels written on the body's Nodes in the box's
        # x-major order (`body_node_indices`, the loader's and the generator's
        # one convention), the norm T the written one (the conserved form on
        # the given family's vacuum, the generator's integer checked at load)
        # THE WINDOW (ALGEBRA.md 9.69 (2), 9.71 (1) (a), 9.85 (5); item 50; commit 7,
        # the one giving): no train; the window opens at the click, the given row at
        # the body's Node written from its rotation every interval (`_point_windows`)
        # until the outward norm reaches T; the record named at the close
        live.window_open = True
        live.box = self.mask_box(block.mask)  # HOST (item 43): the body's own Nodes
        block.window = identity
        if emitter.receiver is not None:
            # the named sets in the NAMED order (ALGEBRA.md 9.19 (3) (b): the
            # ladder cumulative in its declared order), a set's detectors in the
            # detectors' order within it
            live.ladder = [
                detector
                for name in emitter.receiver
                for detector, set_name in enumerate(self.detector_set)
                if set_name == name
            ]
        # THE STOCK IS GIVEN-FAMILY CONTENT (ALGEBRA.md 9.51 (8); item 47): the
        # giving lowers the given family's content held at the body by one,
        # the body's own quanta and its charge untouched (under the point
        # emitter too, item 50: the quantum moves at the open, the window
        # shapes its rows, the close names the record)
        self.held[number][family] -= 1
        self.ledger.held_spent[family] += 1
        # THE NORM UNDER THE NODE CLOCK (BUILD.md section 26 items 31 and
        # 36; ALGEBRA.md 9.50 (13)): the given record's T is p times its
        # conserved form as written on the board, the engine's own integer
        # with the content at the body's Nodes AS IT STANDS this interval:
        # ONE ORDER FOR BOTH CLICKS (ALGEBRA.md 9.85 (2); BUILD.md section 26
        # item 58): a click's writes enter at the next interval (9.57 (1)),
        # so the giving's lowered quanta are held after the held families'
        # step with the takings' (`_advance_fields`), no hold here (the hold
        # at once, item 47, HISTORY: a defect against 9.57 (1))
        # THE POINT EMITTER (item 50): the record's norm is T from the open,
        # the excitation's action the window will reach (9.71 (1) (d)), as the
        # exact rational norm / norm_denominator, so the ladder reads its
        # bookings from the first interval (Born's rule's walk as now)
        assert emitter.norm is not None and emitter.norm_denominator is not None
        live.norm, live.pace = emitter.norm, emitter.norm_denominator
        self.ledger.transit_released[family] += cost
        block.emitted.append(identity)
        self.records[identity] = live
        self.layer.given += 1
        if self.record is not None:
            giving_line: dict[str, object] = {
                "event": "giving",
                "tick": self.tick,
                "node": list(block.corner),
                "measured": number,
                "family": definition.name,
                "record": identity,
                "u": residue,
                "W": wheel,
                "labels": [list(label) for label in emitter.branches],
                "arms": 1,
                "units": 1,
                "multiplicity": 1,
                "train": 0,
                "excitation": excitation,
                "excitation_norm": own.norm,
                # the tick's count (9.44 (5) (c)): the intervals from the
                # residue's read to this click, the period P counted
                # against, and the first shell Node that read u
                "wait": wait,
                "period": emitter.period,
                "read_node": list(read_node),
                # the wheel's ingredients, read with it (item 34; GAMEBOARD)
                "read_clocks": read_clocks,
                "norm": live.norm,
                # the norm's denominator (item 36): the given record's
                # form is norm / pace, whole in the body's own units at
                # the body's level as written
                "pace": live.pace,
                # the file's vacuum norm (p times it the given record's T
                # in the vacuum) and the body's content and clock pair
                # as the clicking record was advanced (GAMEBOARD; item 31)
                "given_norm": emitter.given.norm if emitter.given is not None else 0,
                "content": centre_content,
                "charge": body_charge,
                "node_clock": list(clock_pair),
                "nodes": int(np.sum(block.mask)),
                "cycle": block.count,
                **({"clock": block.count} if world.clock_stamp else {}),
            }
            live.giving_line = giving_line  # named at the close (item 50)
        # the next excitation and the count wait for the window's close
        block.emit_now = False
        block.wait = 0
        own.u, own.wheel = residue, wheel

    def _block_clock(self, block: Block) -> None:
        """The block's clock (MASSIVE_RECORD.md sections 4 and 6): its total
        record summed across its Nodes (G over R: its own record), one
        count per cycle (the sum's crossing
        from at most 0 to above 0, verb D's comparison), a `click` line per
        count with its own count (the self-click of row (g)); a new cycle
        givings its emission at the next interval."""
        total = 0
        # the co-moving centre Node (the design's reading of the clock in
        # motion, MASSIVE_RECORD.md section 8: "the clock read at the
        # co-moving centre"): the total record's value there, on the line
        centre = box_centre(block.corner, block.definition.extents, self.shape)
        at_centre = 0
        if block.node_record is not None:
            # the body's Node's record (9.60 (1)): its level is the standing record's
            # coefficient, the sum over the Nodes and the centre alike
            total += block.node_record.now
            at_centre += block.node_record.now
        elif block.own is not None:
            total += int(np.sum(block.own.now[block.mask]))
            at_centre += int(block.own.now[centre])
        if block.previous_sum <= 0 < total:
            block.count += 1
            block.new_cycle = True
            block.cycle_length = self.tick - block.cycle_start
            block.cycle_start = self.tick
            if self.record is not None:
                self.record(
                    {
                        "event": "click",
                        "tick": self.tick,
                        "node": list(block.corner),
                        "measured": block.number,
                        "family": self.families[block.family].name,
                        "record": (
                            block.node_record.identity
                            if block.node_record is not None
                            else None
                            if block.own is None
                            else block.own.identity
                        ),
                        "cycle": block.count,
                        "clock": block.count,
                    }
                )
        block.previous_sum = total
        if self.record is not None:
            self.record(
                {
                    "event": "block",
                    "tick": self.tick,
                    "measured": block.number,
                    "corner": list(block.corner),
                    "sum": total,
                    "centre": at_centre,
                    "clock": block.count,
                    "steps": block.stepped,
                }
            )

    @staticmethod
    def _phase(age: int, numerator: int, denominator: int, steps: int) -> int:
        """The record's clock at its age: the zero (3 N / 4) advanced by the
        whole part of age x n / d on the circle of N steps."""
        return (3 * steps // 4 + age * numerator // denominator) % steps

    # The inverse map (ALGEBRA.md 8.8): the step is a bijection but for the
    # click; the property test of 9.20 (B) 4 runs it backwards

    def _advance_inverse(self, live: LiveRecord) -> None:
        """One interval of the rule backwards on a record: from (a_next, a_now,
        r') to (a_now, a_before, r) with 3 den Gamma a_before - r = num SUM_j
        (Gamma - c_j) a_now,j + 6 den c a_now - (3 den Gamma a_next + r')
        under the fixed wall (BUILD.md section 26 item 34; the same integers
        as the forward step's, the clock field of the interval's start), the
        remainder in [0, 3 den Gamma): a_before the ceiling of that quotient,
        r the difference; exact at every Node for every clock history, since
        the remainder's range is the wall's, constant (board_algebra.py's
        `step_inverse`). With a tensor part read, a twist on a Port or a
        second level (commits 3 and 4) the arrivals are stepped back per axis
        after the transport's inverse (`_arrivals`), both levels."""
        if live.silent:
            return  # a zero held part steps to zero exactly (HOST; 9.91 (1))
        num, den = self.pair_arrays(live.family, live.pair)
        field = live.held_part
        gamma = 1 if field else self.node_clock
        content = 0 if field else self._effective_content(live.family)
        # the same integers as the forward step's: the pace on the Node's own
        # sum (item 36)
        # HOST (item 43): the record's box holds the reach of `before`'s rows
        # (it was the window of the step that wrote `now`), so the inverse is
        # read on the box itself, zeros elsewhere; the box stays (a superset)
        axis_contents = None if field else self._axis_contents(live.family, inverse=True)
        twists = None if field else self._port_twists(live, True)
        sigma_self = self._self_source(live, True)
        plain = axis_contents is None and twists is None and live.im_now is None and sigma_self is None
        if not plain:
            reads_re, reads_im = self._arrivals(live, twists, True)
            a_before, live.remainder = self._level_step(
                num,
                den,
                gamma,
                content,
                axis_contents,
                reads_re,
                live.before,
                live.now,
                live.remainder,
                not field,
                -1,
            )
            if sigma_self is not None:
                a_before -= sigma_self  # the same multiple of the wall off (9.91 (5))
            if live.im_now is not None:
                assert live.im_before is not None and live.im_remainder is not None
                im_reads = [np.zeros_like(live.now) for _ in range(3)] if reads_im is None else reads_im
                im_a_before, live.im_remainder = self._level_step(
                    num,
                    den,
                    gamma,
                    content,
                    axis_contents,
                    im_reads,
                    live.im_before,
                    live.im_now,
                    live.im_remainder,
                    not field,
                    -1,
                )
                live.im_now = live.im_before
                live.im_before = im_a_before
        elif live.box is None or self._window(live.box, self.kind_wrap[live.family]) is None:
            arrivals = self._axis_sums(live.before, self.kind_wrap[live.family])
            reads, self_coefficient, wall = coefficients(num, den, gamma, content, ISOTROPIC, not field)
            a_before, live.remainder = rule3(
                reads, arrivals, self_coefficient, wall, live.before, live.now, live.remainder, -1
            )
        else:
            slices = tuple(slice(lo, hi) for lo, hi in live.box)
            wraps = tuple(
                self.kind_wrap[live.family][axis] and (lo == 0 and hi == self.shape[axis])
                for axis, (lo, hi) in enumerate(live.box)
            )
            content_w = content[slices] if isinstance(content, np.ndarray) else content
            arrivals = self._axis_sums(live.before[slices], (wraps[0], wraps[1], wraps[2]))
            reads, self_coefficient, wall = coefficients(
                num[slices], den[slices], gamma, content_w, ISOTROPIC, not field
            )
            a_before_w, remainder_w = rule3(
                reads,
                arrivals,
                self_coefficient,
                wall,
                live.before[slices],
                live.now[slices],
                live.remainder[slices],
                -1,
            )
            a_before = np.zeros_like(live.now)
            a_before[slices] = a_before_w
            live.remainder[slices] = remainder_w
        live.now = live.before
        live.before = a_before
        live.age -= 1

    def step_inverse(self) -> None:
        """One interval backward in the joint inverse's fixed order (the bodies' step back, every family at the interval's start levels, the held families and their hold last); no hop, click or giving in the interval."""
        for block in self.blocks:
            if block.stepped > 0 or any(block.hop):
                raise ValueError(
                    f"the inverse map is defined for a body that has not hopped (block "
                    f"{block.number} hopped; the hop's inverse, the field moved back through the "
                    "body, ALGEBRA.md 9.52 (4) (i), is not built)"
                )
        # the bodies' step back first (9.91 (8) (v); commit 6): the momentum and the
        # spin as the interval began, from the fields as it left them
        for block in self.blocks:
            self.register.at("the spin's step", "(v)")(block, True)
        # the joint inverse (ALGEBRA.md 9.41 (2), 9.45 (2); item 51): every
        # family backward at the held levels of the interval's start (their
        # `before` level: the held families stepped last), then the held
        # families backward and their hold
        for family, record in self.held_records.items():
            self.node_level[family] = record.before
        self._effective.clear()
        # the interval's dipole writes taken back first (9.91 (3); commit 2): they
        # were the last writes of the forward interval, after the fields' step
        hold = self.register.at("the hold", "(iv)")
        self._unhold_dipoles(hold)
        for block in self.blocks:
            if block.window is not None:
                self._point_window_inverse(block)
        for identity in list(self.records):
            live = self.records[identity]
            if live.standing:
                continue
            self._advance_inverse(live)
        for block in self.blocks:
            if block.node_record is not None:
                self._advance_node_record(block, -1)
            elif block.own is not None:
                self._advance_inverse(block.own)
        for record in reversed(self.held_component_records()):
            self._advance_inverse(record)
        self._hold(hold, inverse=True)
        # the drive's accumulator back (no hop this interval: drive' = drive + n)
        for block in self.blocks:
            momentum = self._momentum_now(block)
            for axis in range(3):
                block.drive[axis] -= momentum[axis]
        self.tick -= 1

    # The rule

    def _shift(
        self,
        a: np.ndarray,
        axis: int,
        sign: int,
        fill: int | bool = 0,
        wrap: tuple[bool, bool, bool] | None = None,
    ) -> np.ndarray:
        """The neighbour on the side `sign` of `axis`: the wrap on a periodic
        axis, `fill` beyond an open face; `wrap` the faces read (the world's
        `boundary`, one border for every family)."""
        periodic = self.world.periodic if wrap is None else wrap
        if periodic[axis]:
            return np.roll(a, sign, axis=axis)
        out = np.full_like(a, fill)
        lower = [slice(None)] * 3
        upper = [slice(None)] * 3
        if sign > 0:
            lower[axis] = slice(1, None)
            upper[axis] = slice(None, -1)
        else:
            lower[axis] = slice(None, -1)
            upper[axis] = slice(1, None)
        out[tuple(lower)] = a[tuple(upper)]
        return out

    def _neighbours(self, a: np.ndarray, wrap: tuple[bool, bool, bool] | None = None) -> np.ndarray:
        """The sum of the six neighbours' amplitudes at every Node (verb G):
        the wrap on a periodic axis, 0 beyond a zero face (no Node there),
        the row itself on an axis of one layer; `wrap` the world's faces (one
        border for every family). Nothing is read through a Port: the take
        is retired (ALGEBRA.md 9.19 (3))."""
        total = np.zeros_like(a)
        for axis in range(3):
            if self.shape[axis] == 1:
                total += 2 * a
                continue
            for sign in (1, -1):
                total += self._shift(a, axis, sign, wrap=wrap)
        return total

    def _axis_sums(
        self, a: np.ndarray, wrap: tuple[bool, bool, bool] | None = None
    ) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
        """The two neighbours\' levels summed per axis at every Node, the three arrival sums rule3 reads; their sum is `_neighbours` (verb G; ALGEBRA.md 9.57 (1))."""
        sums = []
        for axis in range(3):
            if self.shape[axis] == 1:
                sums.append(2 * a)
                continue
            sums.append(self._shift(a, axis, 1, wrap=wrap) + self._shift(a, axis, -1, wrap=wrap))
        return sums[0], sums[1], sums[2]

    def _axis_contents(self, family: int, inverse: bool = False) -> tuple[np.ndarray, ...] | None:
        """THE AXIS CONTENTS t_a of a reading family (ALGEBRA.md 9.91 (2); commit
        3): SUM over its reads of weight x by x (the read family's aa component
        div 2), one division per read per axis with the remainder kept at the
        Node (`_pace_carry`), advanced once per interval; backward the same
        values with the remainder stepped back (r_(t-1) = (r_t - S) mod 2, the
        value (S + r_(t-1)) div 2), so the inverse reads the paces the step
        read. None where no read's tensor part was ever sourced: the rule is
        then isotropic, p_a = p_0, bit for bit."""
        cached = self._axis_effective.get(family)
        if cached is not None and cached[0] == self.tick and cached[1] == inverse:
            return cached[2]
        sign = self.family_charge[family]
        found: list[np.ndarray] | None = None
        for other, weight, by, _ in self.families[family].reads:
            parts = self.families[other].parts
            if len(parts) < 3:
                continue
            diagonal = self.held_parts[other][parts[1] : parts[1] + 3]  # xx, yy, zz
            if all(record.silent for record in diagonal):
                continue
            factor = weight if by == "plain" else -sign * weight
            if factor == 0:
                continue
            if found is None:
                found = [np.zeros(self.shape, dtype=np.int64) for _ in range(3)]
            for axis, record in enumerate(diagonal):
                key = (family, other, axis)
                carry = self._pace_carry.get(key)
                if carry is None:
                    carry = np.zeros(self.shape, dtype=np.int64)
                level = record.before if inverse else record.now
                numerator = factor * level
                if inverse:
                    carry = np.mod(carry - numerator, 2)
                    value = np.floor_divide(numerator + carry, 2)
                else:
                    total = numerator + carry
                    value = np.floor_divide(total, 2)
                    carry = total - 2 * value
                self._pace_carry[key] = carry
                found[axis] += value
        result = None if found is None else (found[0], found[1], found[2])
        self._axis_effective[family] = (self.tick, inverse, result)
        return result

    # THE TRANSPORT (ALGEBRA.md 9.81 (2), 9.91 (6), 9.96 (2); the one stroke, commit 4):
    # the operations, written once for any phase-2 family and any read with a twist

    def _arrival(
        self, a: np.ndarray, axis: int, sigma: int, wrap: tuple[bool, bool, bool]
    ) -> np.ndarray:
        """The level arriving through the Port toward `sigma` on the axis: the
        neighbour's level (the wrap on a periodic axis, 0 beyond an open face, the
        Node itself on a folded axis of extent 1), as `_neighbours` reads it."""
        if self.shape[axis] == 1:
            return a
        return self._shift(a, axis, -sigma, wrap=wrap)

    def _port_twists(self, live: LiveRecord, inverse: bool) -> list[np.ndarray] | None:
        """THE LINK'S ANGLE PER PORT (ALGEBRA.md 9.81 (2) (a), 9.91 (6)): k = sigma x by x
        twist x (V_a here + V_a arrived), summed over the record's family's reads with a
        twist, V_a the read family's vector component along the Port's axis a at this Node
        and at the neighbour across the Port (sigma +1 toward +a, -1 toward -a; the other
        end forms -k, the transport back the inverse rotation); the twist "own" is the
        record's own rotation times the read's weight (9.96 (2) (b): Lambda_v is Lambda),
        an integer twist as declared, by q the reading family's charge sign. None where
        no read has a twist or every read's vector part is silent: the identity, bit for
        bit. Backward the vector parts' `before` levels, the levels the step read. HOST:
        one list of six arrays per (family, own twist) per interval."""
        definition = self.families[live.family]
        if definition.levels < 2:
            return None
        key = (live.family, live.twist, inverse)
        cached = self._twists.get(key)
        if cached is not None and cached[0] == self.tick:
            return cached[1]
        sign = self.family_charge[live.family]
        wrap = self.kind_wrap[live.family]
        found: list[np.ndarray] | None = None
        for other, weight, by, twist in definition.reads:
            if len(self.families[other].parts) < 2:
                continue
            vector = self.held_parts[other][:3]
            if all(record.silent for record in vector):
                continue
            factor = weight * live.twist if twist == "own" else int(twist)
            if by != "plain":
                factor *= sign
            if factor == 0:
                continue
            if found is None:
                found = [np.zeros(self.shape, dtype=np.int64) for _ in range(6)]
            for axis in range(3):
                level = vector[axis].before if inverse else vector[axis].now
                for side, sigma in enumerate((1, -1)):
                    found[2 * axis + side] += (
                        sigma * factor * (level + self._arrival(level, axis, sigma, wrap))
                    )
        self._twists[key] = (self.tick, found)
        return found

    def _twist_triple(self, k: np.ndarray, port: int) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
        """THE ROTATION'S TRIPLE per Node from the twist table (ALGEBRA.md 9.81 (2) (b),
        9.96 (2) (c)): |k| = k_1 2^10 + k_0, the fine triple of k_0 and the coarse triple
        of k_1 composed exactly, (c_1 c_0 - s_1 s_0, s_1 c_0 + c_1 s_0, d_1 d_0), with
        (c, -s, d) for k < 0 and (1, 0, 1) at k = 0; a k_1 beyond the coarse table, or any
        k on a world without a table, is refused naming the Port."""
        magnitude = np.abs(k)
        coarse_index = magnitude >> TWIST_FINE_BITS
        most = int(coarse_index.max())
        if self.twist_table is None or most >= len(self.twist_table.coarse):
            axis, sigma = port // 2, (1, -1)[port % 2]
            node = np.unravel_index(int(np.argmax(coarse_index)), self.shape)
            raise RuntimeError(
                f"the twist k = {int(k[node])} on the Port toward {'+' if sigma > 0 else '-'}"
                f"{AXES[axis]} of the Node {[int(i) for i in node]} at interval {self.tick} is beyond the "
                f"twist table ({'no table' if self.twist_table is None else f'{len(self.twist_table.coarse)} coarse triples'}; "
                "ALGEBRA.md 9.96 (2) (c)): the run is refused"
            )
        fine_index = magnitude & ((1 << TWIST_FINE_BITS) - 1)
        c0, s0, d0 = self._fine[:, fine_index]
        c1, s1, d1 = self._coarse[:, coarse_index]
        return c1 * c0 - s1 * s0, np.sign(k) * (s1 * c0 + c1 * s0), d1 * d0

    def _arrivals(
        self, live: LiveRecord, twists: list[np.ndarray] | None, inverse: bool
    ) -> tuple[list[np.ndarray], list[np.ndarray] | None]:
        """THE SIX ARRIVALS AFTER THE TRANSPORT (ALGEBRA.md 9.81 (2) (c), (d); 9.91 (6)),
        summed per axis for the two levels: on a Port with the angle k the arriving pair
        (re, im) is rotated by the table's triple, T_re = (c re - s im) / d and T_im = (s
        re + c im) / d, each ROUNDED TO THE NEAREST UNIT ((2 x + d) div (2 d)), a pure
        function of the arrivals and the angle; at k = 0 the neighbour's level exactly.
        NO REMAINDER IS KEPT ON THE PORT: 9.81 (2) (c)'s rho in [0, d) is one to one only
        while d stands, and d changes with the angle every interval (a remainder of up
        to d_old flushed whole into the level when d fell to 1: the moving long Lorentz
        clock's jump at interval 250; sent to the mathematician, BUILD.md item 64); the
        rounding is unbiased in the mean and the inverse recomputes the same T from the
        `before` levels, exact. The second level's sums are None while the record has
        no second level and no rotation writes one."""
        wrap = self.kind_wrap[live.family]
        re = live.before if inverse else live.now
        im = None if live.im_now is None else (live.im_before if inverse else live.im_now)
        reads_re = [np.zeros_like(re) for _ in range(3)]
        reads_im: list[np.ndarray] | None = None if im is None else [np.zeros_like(re) for _ in range(3)]
        for axis in range(3):
            for side, sigma in enumerate((1, -1)):
                port = 2 * axis + side
                re_j = self._arrival(re, axis, sigma, wrap)
                im_j = None if im is None else self._arrival(im, axis, sigma, wrap)
                k = None if twists is None else twists[port]
                if k is None or not k.any():
                    reads_re[axis] += re_j
                    if reads_im is not None and im_j is not None:
                        reads_im[axis] += im_j
                    continue
                c, s, d = self._twist_triple(k, port)
                base_re = c * re_j - (0 if im_j is None else s * im_j)
                base_im = s * re_j + (0 if im_j is None else c * im_j)
                t_re = np.floor_divide(2 * base_re + d, 2 * d)
                t_im = np.floor_divide(2 * base_im + d, 2 * d)
                reads_re[axis] += t_re
                if reads_im is None and t_im.any():
                    reads_im = [np.zeros_like(re) for _ in range(3)]
                if reads_im is not None:
                    reads_im[axis] += t_im
        return reads_re, reads_im

    @staticmethod
    def _level_step(
        num: np.ndarray,
        den: np.ndarray,
        gamma: int,
        content: np.ndarray | int,
        axis_contents: tuple[np.ndarray, ...] | None,
        reads: list[np.ndarray],
        now: np.ndarray,
        other: np.ndarray,
        remainder: np.ndarray,
        weak_field: bool,
        direction: int = 1,
    ) -> tuple[np.ndarray, np.ndarray]:
        """One level's step by rule3 in `direction` from its three per-axis arrival sums, `now` the level read and `other` the far level (ALGEBRA.md 9.91 (2), 9.50 (8))."""
        integers, self_coefficient, wall = coefficients(
            num, den, gamma, content, ISOTROPIC if axis_contents is None else axis_contents, weak_field
        )
        return rule3(
            integers,
            (reads[0], reads[1], reads[2]),
            self_coefficient,
            wall,
            now,
            other,
            remainder,
            direction,
        )

    def _self_source(self, live: LiveRecord, inverse: bool) -> np.ndarray | None:
        """THE SELF-SOURCE'S SLOT (ALGEBRA.md 9.78 (3), 9.91 (5), 9.97): per family with a unit
        P_2 above 0, the folder's line (features/self_source) through the register on every level
        of the family at the interval's start (backward the `before` levels) with its six Links;
        the step's right side loses w Sigma_self. None at P_2 = 0 (every shipped family). HOST:
        once per family per interval, before any record of the family steps."""
        family = live.family
        unit = self.families[family].self_unit
        if unit <= 0:
            return None
        key = (family, inverse)
        cached = self._sources.get(key)
        if cached is not None and cached[0] == self.tick:
            return cached[1]
        wrap = self.kind_wrap[family]
        records = [record for record in self.records.values() if record.family == family]
        if family in self.held_records:
            records.extend([self.held_records[family], *self.held_parts[family]])
        levels = []
        for record in records:
            for level in (
                record.before if inverse else record.now,
                record.im_before if inverse else record.im_now,
            ):
                if level is None or (record.silent and record.held_part):
                    continue
                links = [self._arrival(level, axis, side, wrap) for axis in range(3) for side in (1, -1)]
                levels.append(self_source.OwnLevel(level, tuple(links)))
        term = self_source.SelfSourceTerm(unit, self.world.amplitude_bound)
        start = self_source.SelfSourceStart(tuple(levels))
        writes = self.register.at("the self-source", "(i)")(term, start)
        sigma_self: np.ndarray = cast(self_source.SelfSourceWrites, writes).source
        self._sources[key] = (self.tick, sigma_self)
        return sigma_self

    def booked_axis(self, live: LiveRecord) -> int | None:
        """THE TRANSVERSE BOOKING (ALGEBRA.md 9.82 (3) (b), (c)): the axis of a record's own
        vector component, whose Ports book nothing of it (the longitudinal component
        along the Port's axis carries the near field and no count); None for a scalar
        family's record or a time part (booked through every Port)."""
        if len(self.families[live.family].parts) > 1 and 1 <= live.part <= 3:
            return live.part - 1
        return None

    # The flux reading (ALGEBRA.md 9.19 (3), the mathematician's derivation
    # of 2026-09-24 from 8.2; BUILD.md section 26 item 13): the flux into a
    # Node i from a read j of it, 3 G_ij = A_ij (now_i before_j - before_i
    # now_j), a bilinear form of the record's own two levels at the two ends
    # of a Link, pair-free and antisymmetric; a receiver's offer the one-way
    # inward flux through its Ports, summed over intervals; the record's
    # norm its conserved form I. Both in the integers 3 G x wall and 3 I x
    # wall, wall the family's common wall (the least common multiple of its
    # pairs' numerators over the board).

    def kind_wall(self, family: int, pair: tuple[int, int] | None = None) -> int:
        """The family's common wall: the least common multiple of the
        numerators of its pair over the board (the vacuum's and every body's),
        so that wall x den_i / num_i is an integer at every Node. HOST: read
        once per family from the board's pair array and kept until a pair is
        written (`_write_pair`, the load and a hop); the same integer at every
        call, bit for bit (record 2039: the distinct numerators were gathered
        anew for every record at every interval, a fifth of the run)."""
        num_all, _ = self.pair_arrays(family, pair)
        rest = self.families[family].pair if pair is None else (int(pair[0]), int(pair[1]))
        key = (family, rest[0], rest[1])
        wall = self._kind_walls.get(key)
        if wall is None:
            wall = 1
            for value in np.unique(num_all).tolist():
                value = int(value)
                wall = wall * value // gcd(wall, value)
            self._kind_walls[key] = wall
        return wall

    def _flux_ports(self, family: int) -> list[tuple[int, int, np.ndarray]]:
        """The Ports of every detector for the flux reading (ALGEBRA.md 9.25 (2),
        the mathematician's gate item 2): per axis of extent above 1 and
        per side s, the Nodes of a detector whose neighbour on that side (the
        read across the Link, on the family's faces) is a Node of no set or
        of ANOTHER set; a Link between two Nodes of one set (inside a
        detector's cube) is no Port, so the energy that entered the set at
        one Node is not offered again at its neighbour. A self-read of a folded
        axis carries no flux; beyond an open face there is no Node and no
        Link."""
        wrap = self.kind_wrap[family]
        set_names = sorted(set(self.detector_set))
        set_of_detector = [set_names.index(name) for name in self.detector_set]
        set_index = np.full(self.shape, -1, dtype=np.int64)
        occupied = self.detector_at_node >= 0
        set_index[occupied] = np.array(set_of_detector, dtype=np.int64)[self.detector_at_node[occupied]]
        ports: list[tuple[int, int, np.ndarray]] = []
        for axis in range(3):
            if self.shape[axis] == 1:
                continue
            for side in (1, -1):
                neighbour = self._shift(set_index, axis, -side, fill=-2, wrap=wrap)
                mask = occupied & (neighbour != -2) & (neighbour != set_index)
                ports.append((axis, side, mask))
        return ports

    def _inflow_ports(self, family: int) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
        """The Port pairs of the family's detectors, listed ONCE (the click's cost,
        the model owner's record 1934: the click never counts the board's
        shapes; it reads the Ports alone): the flat index of every Port Node
        i, of its neighbour j across the Link (on the family's faces), and
        the detector of i, from `_flux_ports`."""
        cached = self._inflow_port_pairs.get(family)
        if cached is not None:
            return cached
        wrap = self.kind_wrap[family]
        count = int(np.prod(self.shape))
        flat = np.arange(count, dtype=np.int64).reshape(self.shape)
        nodes: list[np.ndarray] = []
        neighbours: list[np.ndarray] = []
        axes: list[np.ndarray] = []
        sides: list[np.ndarray] = []
        for axis, side, mask in self._flux_ports(family):
            across = self._shift(flat, axis, -side, fill=-1, wrap=wrap)
            where = mask & (across >= 0)
            nodes.append(flat[where])
            neighbours.append(across[where])
            axes.append(np.full(int(np.count_nonzero(where)), axis, dtype=np.int64))
            sides.append(np.full(int(np.count_nonzero(where)), side, dtype=np.int64))
        port_i = np.concatenate(nodes) if nodes else np.zeros(0, dtype=np.int64)
        port_j = np.concatenate(neighbours) if neighbours else np.zeros(0, dtype=np.int64)
        port_detector = self.detector_at_node.ravel()[port_i]
        pairs = (port_i, port_j, port_detector)
        self._inflow_port_pairs[family] = pairs
        # the face of every Port, (axis, side): the outward normal of the Node
        # i's face toward j is side along the axis (ALGEBRA.md 9.74 (2))
        self._inflow_port_faces[family] = (
            np.concatenate(axes) if axes else np.zeros(0, dtype=np.int64),
            np.concatenate(sides) if sides else np.zeros(0, dtype=np.int64),
        )
        return pairs

    def _moving_sets(self) -> dict[int, tuple[Block, list[int]]]:
        """The detectors bound to a block whose momentum is not zero at this
        interval, each with its block and the momentum (ALGEBRA.md 9.74 (2)):
        the faces of these sets book in the body's frame; empty on a board at
        rest, where the rule is the Port booking alone."""
        moving: dict[int, tuple[Block, list[int]]] = {}
        for detector, number in self.set_block.items():
            block = self.block_by_number[number]
            momentum = self._momentum_now(block)
            if any(momentum):
                moving[detector] = (block, momentum)
        return moving

    def detector_inflow_tally(self, live: LiveRecord) -> dict[int, int]:
        """THE DETECTORS' INFLOW, PER RECORD, OVER THE PORTS ALONE (ALGEBRA.md
        9.19 (3), 9.25 (2); the model owner's record 1934): this interval's
        one-way inward flux into every detector, 3 G_ij = now_i before_j -
        before_i now_j where positive per Port, times the family's wall (the
        form's units; the current unweighted, ALGEBRA.md 9.50 (13); BUILD.md
        section 26 item 36), from the record's two levels AFTER the interval's step, by the detector's
        index. The record's levels are read at the Port pairs only (one
        gather per pair, exact Python integers), never over the board: the
        HOST cost is the Ports, not the Nodes (the two levels are still
        board arrays; the advance is the board's cost)."""
        port_i, port_j, port_detector = self._inflow_ports(live.family)
        port_axis, port_side = self._inflow_port_faces[live.family]
        # THE TRANSVERSE BOOKING (ALGEBRA.md 9.82 (3) (b), (c); commit 4): the Ports along
        # the record's own vector component book nothing of it
        own_axis = self.booked_axis(live)
        if own_axis is not None:
            keep = port_axis != own_axis
            port_i, port_j, port_detector = port_i[keep], port_j[keep], port_detector[keep]
            port_axis, port_side = port_axis[keep], port_side[keep]
        if port_i.size == 0:
            return {}
        # THE CURRENT IS UNWEIGHTED (ALGEBRA.md 9.50 (9) and (13); BUILD.md
        # section 26 item 36): wall (now_i before_j - before_i now_j) through
        # the Port ij, the plain current of the form's units (the pace at
        # both ends, form (B) of item 34, HISTORY); Born's rule at the
        # taking end unchanged by one bit
        wall = self.kind_wall(live.family)
        now = live.now.ravel()
        before = live.before.ravel()
        now_i = now[port_i].astype(object)
        before_i = before[port_i].astype(object)
        now_j = now[port_j].astype(object)
        before_j = before[port_j].astype(object)
        flux = now_i * before_j - before_i * now_j
        if live.im_now is not None and live.im_before is not None:
            # the pair's norm (9.82 (3) (b)): the second level's current added
            im_now, im_before = live.im_now.ravel(), live.im_before.ravel()
            flux += im_now[port_i].astype(object) * im_before[port_j].astype(object)
            flux -= im_before[port_i].astype(object) * im_now[port_j].astype(object)
        moving = self._moving_sets() if self.set_block else {}
        offers: dict[int, int] = {}
        if not moving:
            for value, detector, axis, side in zip(
                flux.tolist(),
                port_detector.tolist(),
                port_axis.tolist(),
                port_side.tolist(),
                strict=True,
            ):
                if value > 0:
                    offers[detector] = offers.get(detector, 0) + int(value) * wall
                    self._tally_direction(live, detector, axis, side, int(value) * wall)
            return offers
        # THE BOOKING IN THE BODY'S FRAME (ALGEBRA.md 9.74 (2); BUILD.md section
        # 26 item 56): a face of a body moving at v with outward normal n books
        # per interval (G_in + (v . n) e_out) cut at zero AFTER the sum: G_in
        # the board's inward current through the face's Link (the Port booking
        # above), e_out the record's density on the Node outside the face
        # (`node_density`, the same units), v . n = side x momentum / wall along
        # the face's axis, positive at a face advancing into the outside (the
        # front) and negative at a face receding from it (the back). One rule
        # for every face of every moving set, per interval, not per hop: at
        # the front an oncoming record books G_in + v e_out, a standing or
        # transverse one v e_out, a record outrunning the body nothing; at the
        # back a record overtaking from behind books G_in - v e_out, the norm
        # once, with no negative booking. The whole part is booked, the
        # fraction carried on the record per detector (`carry`, exact). The
        # three tests: the face's Link, the outside Node's density and the
        # body's own pace, fixed work; sums and products; no name. At v = 0
        # the rule is the Port booking above, bit for bit.
        outside = sorted(
            set(
                int(node)
                for node, detector in zip(port_j.tolist(), port_detector.tolist(), strict=True)
                if detector in moving
            )
        )
        density = dict(
            zip(outside, self.node_density(live, np.array(outside, dtype=np.int64)), strict=True)
        )
        frame: dict[int, Ratio] = {}
        for value, detector, node, axis, side in zip(
            flux.tolist(),
            port_detector.tolist(),
            port_j.tolist(),
            port_axis.tolist(),
            port_side.tolist(),
            strict=True,
        ):
            bound = moving.get(detector)
            if value > 0:
                # the direction from the Port booking in the board's frame, for a
                # set at rest and for a moving one alike (the body-frame correction
                # below moves the booked share, not the Port it entered by)
                self._tally_direction(live, detector, axis, side, int(value) * wall)
            if bound is None:
                if value > 0:
                    offers[detector] = offers.get(detector, 0) + int(value) * wall
                continue
            block, momentum = bound
            # G_in + (v . n) e_out as one pair: the Port booking whole, the frame
            # term side x momentum x e_out over the body's wall (exact integers)
            body_wall = self.wall_of(block)
            density_numerator, density_denominator = density[node]
            term = ratio(
                int(value) * wall * body_wall * density_denominator
                + side * momentum[axis] * density_numerator,
                body_wall * density_denominator,
            )
            if term[0] > 0:
                frame[detector] = ratio_sum([frame.get(detector, ZERO), term])
        for detector, share in frame.items():
            numerator, denominator = ratio_sum([share, live.carry.get(detector, ZERO)])
            whole = numerator // denominator
            live.carry[detector] = ratio(numerator - whole * denominator, denominator)
            if whole > 0:
                offers[detector] = offers.get(detector, 0) + whole
        return offers

    @staticmethod
    def _tally_direction(live: LiveRecord, detector: int, axis: int, side: int, booked: int) -> None:
        """THE FOUR-VECTOR CLICK'S TALLY (ALGEBRA.md 9.91 (4), 9.25 (12); commit 5
        without the recoil): the flux booked through a Port of the detector whose
        outward normal is `side` along `axis` counts toward -side on that axis (a
        quantum that enters through the -a face travels toward +a); kept per
        detector on the record, in the flux's units."""
        tally = live.momentum_tally.get(detector)
        if tally is None:
            tally = live.momentum_tally[detector] = [0, 0, 0]
        tally[axis] -= side * booked

    @staticmethod
    def direction_of(tally: list[int]) -> list[int]:
        """The sign per axis of a tally, sigma_a of ALGEBRA.md 9.84 (2) and 9.91 (4):
        -1, 0 or 1 (DETECTOR: the quantum's direction of travel, not its size)."""
        return [(value > 0) - (value < 0) for value in tally]

    def inward_flux(self, live: LiveRecord, mask: np.ndarray) -> int:
        """The one-way inward flux into the Nodes of `mask` through the Links
        from Nodes outside it (9.19 (3)): 3 G_ij = now_i before_j - before_i
        now_j where positive, times the family's wall (the form's units; the
        current unweighted, item 36), from the record's two levels
        after the interval's step (`now`, `before`; the prototype's
        reading, board_algebra.py); the pair's second level added (9.82 (3)
        (b)) and the Ports along the record's own component skipped (9.82
        (3) (c); commit 4)."""
        wrap = self.kind_wrap[live.family]
        wall = self.kind_wall(live.family)
        own_axis = self.booked_axis(live)
        levels = [(live.now, live.before)]
        if live.im_now is not None and live.im_before is not None:
            levels.append((live.im_now, live.im_before))
        total = 0
        for axis in range(3):
            if self.shape[axis] == 1 or axis == own_axis:
                continue
            for side in (1, -1):
                outside = ~self._shift(mask, axis, -side, fill=False, wrap=wrap)
                present = self._shift(
                    np.ones(self.shape, dtype=bool), axis, -side, fill=False, wrap=wrap
                )
                port = mask & outside & present
                if not port.any():
                    continue
                flux = np.zeros(self.shape, dtype=object)
                for level_now, level_before in levels:
                    now_j = self._shift(level_now, axis, -side, wrap=wrap).astype(object)
                    before_j = self._shift(level_before, axis, -side, wrap=wrap).astype(object)
                    flux = (
                        flux + level_now.astype(object) * before_j - level_before.astype(object) * now_j
                    )
                total += int(np.sum(np.where(port & (flux > 0), flux, 0)))
        return total * wall

    def planted_record(
        self,
        family: int,
        now: np.ndarray,
        before: np.ndarray,
        norm: int = 0,
        pair: tuple[int, int] | None = None,
        part: int = 0,
        twist: int = 0,
    ) -> LiveRecord:
        """A record of the family given to the rule directly, its two levels
        as given and its remainder 0 (the generator's checks of the given
        train, ALGEBRA.md 9.17 (6a) and 9.22 (7a) (iv), and the tests'
        device): registered in no ledger, advanced by `_advance` and read by
        `inward_flux` and `conserved_form` alone; `norm` its T where given,
        `part` its component and `twist` its own rotation (commit 4)."""
        return LiveRecord(
            0,
            0,
            family,
            0,
            0,
            self.tick,
            0,
            1,
            1,
            0,
            1,
            np.array(now, dtype=np.int64).reshape(self.shape),
            np.array(before, dtype=np.int64).reshape(self.shape),
            np.zeros(self.shape, dtype=np.int64),
            pointers=[0] * len(self.detector_names),
            first_rung=[None] * len(self.detector_names),
            norm=norm,
            pair=self.families[family].pair if pair is None else (int(pair[0]), int(pair[1])),
            part=part,
            twist=twist,
        )

    def conserved_form(self, live: LiveRecord) -> Ratio:
        """The record's conserved form I (ALGEBRA.md 8.2; under the Node's own
        pace, 9.50 (9) and (13); BUILD.md section 26 item 36) in the form's
        units, 3 I x wall in the vacuum: over the Nodes [3 wall (den_i /
        num_i) Gamma (now_i^2 + before_i^2) - 6 wall (den_i / num_i) c_i
        now_i before_i] / p_i - wall now_i SUM_j before_j, p_i = Gamma - c_i
        (+ q Lambda d_i) the pace at the Node, the six reads with the
        family's faces (the folded axes' self-reads); the sum of every Node's
        share (`form_share`), an exact rational (the Killing energy: each
        Node's share read in the world's time by its own pace; whole in the
        body's own units, p times it, at a uniform level, `given_norm`)."""
        return self.form_share(live, np.ones(self.shape, dtype=bool))

    def form_share(self, live: LiveRecord, mask: np.ndarray) -> Ratio:
        """The Nodes' share e of the record's conserved form (ALGEBRA.md 9.17
        (7) (e), 9.19 (3), 9.50 (9)) on the Nodes of `mask`, in the form's
        units: a bilinear form of the record's two levels at the Node, its
        six reads and the pace at the Node (verb B, local), the Node's terms
        weighted by 1 / p_i; its change over an interval is the sum of the
        plain currents through the Node's Links plus the remainders' term,
        so a bound mode's share is constant where nothing flows."""
        family = live.family
        wall = self.kind_wall(family, live.pair)
        # THE SHARE UNDER THE NODE'S OWN PACE (ALGEBRA.md 9.50 (9) and (13);
        # BUILD.md section 26 item 36; the form's units, the plain share in
        # the vacuum): with the pace p_i at every Node, e_i = [3 wall (den_i
        # / num_i) Gamma (now_i^2 + before_i^2) - 6 wall (den_i / num_i) c_i
        # now_i before_i] / p_i - wall now_i SUM_j before_j; the step's
        # operator is symmetric under the weight den_i / (num_i p_i), so the
        # sum over the board is exactly invariant where the clock field
        # stands still, and the share's change over an interval is the sum
        # of the plain currents wall (now_i before_j - before_i now_j)
        # through the Node's Links plus the remainders' term (wall / (num_i
        # p_i)) (a_next - a_before)(r - r'), an exact rational per Node (the
        # weights p_i p_j at one integer scale, form (B) of item 34, HISTORY)
        field = live.held_part
        gamma = 1 if field else self.node_clock
        content = (
            np.zeros(self.shape, dtype=object)
            if field
            else self._effective_content(live.family).astype(object)
        )
        num_all, den_all = self.pair_arrays(family, live.pair)
        # THE FORM FROM THE RULE'S OWN INTEGERS (ALGEBRA.md 9.57 (1); item 44):
        # with (R_i, S_i, w_i) the rule's coefficients at the Node, the Node's
        # term is L [w_i (now^2 + before^2) - S_i now before] / R_i and the
        # Link term L now_i SUM_j before_j, L the family's common wall; exact
        # where the field stands (the step's operator symmetric under the
        # weight 1 / R_i), the work term where it moves; the first-order form
        # of item 36, [3 den Gamma (a^2 + b^2) - 6 den c a b] / (p num), is
        # this at R = p num, S = 6 den c, w = 3 den Gamma
        (read_coefficient, _, _), self_coefficient, wall_at = coefficients(
            num_all.astype(object), den_all.astype(object), gamma, content, ISOTROPIC, not field
        )
        # the pair's two levels summed (9.91 (1); commit 4): the form of each level, the
        # plain Link term (exact where every twist is 0, a reading elsewhere)
        levels = [(live.now, live.before)]
        if live.im_now is not None and live.im_before is not None:
            levels.append((live.im_now, live.im_before))
        total: Ratio = ZERO
        for level_now, level_before in levels:
            now = level_now.astype(object)
            before = level_before.astype(object)
            reads = self._neighbours(level_before, self.kind_wrap[family]).astype(object)
            node = wall * form_term(self_coefficient, wall_at, now, before)
            links = wall * now * reads
            total = ratio_sum(
                [total, self._weighted_sum(node, read_coefficient, mask), (-int(np.sum(links[mask])), 1)]
            )
        return total

    @staticmethod
    def _weighted_sum(node: np.ndarray, divisor: np.ndarray, mask: np.ndarray) -> Ratio:
        """SUM_i node_i / divisor_i over the Nodes of `mask`, exact (one pair per
        distinct divisor: the rule's read coefficients present are few, the
        body's and the field's levels; the pairs summed by `rational_sum`)."""
        chosen = divisor[mask]
        values = node[mask]
        return ratio_sum(
            [
                (int(np.sum(values[chosen == value])), value)
                for value in sorted(set(int(v) for v in chosen.tolist()))
            ]
        )

    def given_norm(self, live: LiveRecord) -> tuple[int, int]:
        """THE NORM AS THE EXACT RATIONAL (ALGEBRA.md 9.46 (1), 9.50 (9) and
        (13); BUILD.md section 26 item 36): the given record's conserved form
        Q, the Node's terms weighted by 1 / p_i, as the pair (numerator,
        denominator) in lowest terms, the record's `norm` and `pace`; the
        ladder reads the plain flux C against Q, 2 W pace C against (2 u +
        1) norm, in integers. For a record written at one level (a body's
        Nodes at rest, the content and the charge uniform there) p Q is
        whole, the integer T of 9.46 (1) in the body's own units, and the
        pair reduces from (p Q, p); a record written across levels (a moving
        body's Nodes as the hold leaves them) has a rational Q, its world
        energy, and the same reading."""
        return self.conserved_form(live)

    @staticmethod
    def support_box(*arrays: np.ndarray) -> tuple[tuple[int, int], ...] | None:
        """HOST: the bounding box [lo, hi) per axis of the Nodes where any of the
        arrays is not zero; None when every array is zero everywhere (the
        whole board then, the safe default)."""
        nonzero = np.zeros(arrays[0].shape, dtype=bool)
        for array in arrays:
            nonzero |= array != 0
        if not nonzero.any():
            return None
        box = []
        for axis in range(nonzero.ndim):
            along = np.any(nonzero, axis=tuple(other for other in range(nonzero.ndim) if other != axis))
            where = np.nonzero(along)[0]
            box.append((int(where[0]), int(where[-1]) + 1))
        return tuple(box)

    def _window(
        self, box: tuple[tuple[int, int], ...] | None, wrap: tuple[bool, bool, bool]
    ) -> tuple[tuple[slice, ...], tuple[bool, bool, bool], tuple[tuple[int, int], ...]] | None:
        """HOST: the box grown by one Link per axis, the rule's reach, as the
        slices to step, the faces the reads wrap on inside the window and the
        window itself as the record's next box; None when the window is the
        whole board (the whole-board step then, as before). On a periodic axis
        a window that would touch the axis's ends is the whole axis with its
        wrap; elsewhere the reads beyond the window are zeros, which is what
        the rows there are (or the open face's nothing)."""
        if box is None:
            return None
        slices: list[slice] = []
        wraps: list[bool] = []
        grown: list[tuple[int, int]] = []
        whole = True
        for axis in range(3):
            lo, hi = box[axis]
            size = self.shape[axis]
            if size == 1:
                slices.append(slice(0, 1))
                wraps.append(wrap[axis])
                grown.append((0, 1))
                continue
            lo -= 1
            hi += 1
            if wrap[axis] and (lo < 0 or hi > size):
                lo, hi = 0, size
                wraps.append(True)
            else:
                lo, hi = max(lo, 0), min(hi, size)
                wraps.append(False if not (lo == 0 and hi == size) else wrap[axis])
            if lo > 0 or hi < size:
                whole = False
            slices.append(slice(lo, hi))
            grown.append((lo, hi))
        if whole:
            return None
        return tuple(slices), (wraps[0], wraps[1], wraps[2]), tuple(grown)

    def _advance(self, live: LiveRecord) -> None:
        # THE EMITTER'S NODES ARE NODES LIKE EVERY OTHER (ALGEBRA.md 9.17; the
        # Boss's line of 2026-09-24 on the knot): no grace, no exemption, no
        # own take, no fresh Port; the given record is written once and the
        # law advances it (the retired forms in BUILD.md section 26).
        # Every given record, light's kind or a massive kind alike, books its
        # flux at the Nodes and clicks on its ladder (the click is the law's
        # one action on any record, POSTULATES 10); a BLOCK'S own record (a
        # massive kind, given of no emitter) books nothing and is on no
        # ladder (massive-record-v1, MUST 2).
        # THE BOOKING BY ATTRIBUTE (item 51; item 53): a held family's record
        # and a body's own standing record are read by no detector; every other
        # record is booked at the Ports (nothing declared: derived from `held`)
        if live.silent:
            return  # a zero held part steps to zero exactly (HOST; 9.91 (1))
        field = live.held_part
        booked = not field and not live.standing
        # The rule with the record's pair on the six-neighbour term
        # (massive-record-v1, MASSIVE_RECORD.md section 1): G over the six
        # neighbours, then D by 3 den with the remainder kept, then T; at
        # light's pair [1, 1] the first build's integers bit for bit.
        num, den = self.pair_arrays(live.family, live.pair)
        # THE COUPLING IS THE CLICK ALONE (the model owner's decision (2) of
        # record 1962; ALGEBRA.md 9.34 (B); BUILD.md section 26 item 30): no
        # coupling's term and no folded denominator (MASSIVE_RECORD.md
        # section 7 HISTORY); the wall 3 den, one division per row per
        # interval, the remainder kept in [0, wall)
        # THE NODE CLOCK UNDER THE FIXED WALL (the model owner's decision (5)
        # of record 1962 and his word of 2026-09-25 in Nature24's session,
        # record 1994: the backward run exact everywhere; ALGEBRA.md 9.35 (2)
        # amended, the mathematician's section asked; BUILD.md section 26
        # item 34): the wall is 3 den Gamma at every Node, a constant of the
        # declared region, and the clock enters the numerator as the pace
        # Gamma - c_j of each of the six reads: 3 den Gamma a_next + r' = num
        # SUM_j (Gamma - c_j) a_j + 6 den c a_now - 3 den Gamma a_before + r,
        # c the family of clicks' level at a Node, the remainder in [0, 3 den
        # Gamma). The remainder's range never changes, so the step is one to
        # one at every Node for every clock history (the wall 3 den (Gamma +
        # c) of item 31, which shrank where the level fell and merged two
        # states into one, HISTORY). In the vacuum (c = 0) the levels are the
        # plain rule's bit for bit and the remainder Gamma times its; at
        # uniform content 1 - cos omega' = (1 - cos omega)(Gamma - c) / Gamma.
        # One division per row per interval, the int64 total under the load
        # bound of `_pair_bound`. THE FAMILY OF CLICKS ITSELF steps plain (the
        # pace 1, the wall 3 den): it reads no other family and not its own
        # level (ALGEBRA.md 9.41 (2), 9.45 (2))
        gamma = 1 if field else self.node_clock
        content = 0 if field else self._effective_content(live.family)
        # THE NODE'S OWN PACE (the model owner's ruling of record 2003, "take
        # only from the current Node, not from the neighbours"; ALGEBRA.md
        # 9.50 (13); BUILD.md section 26 item 36): the pace p_i = Gamma - c_i
        # (+ q Lambda d_i) multiplies the Node's own six-neighbour sum, the
        # reads plain as S_6 reads them: 3 den Gamma a_next + r' = p_i num
        # S_6(a_now)_i + 6 den c_i a_now - 3 den Gamma a_before + r; the
        # Node steps the vacuum's rule at its own pace (the pace on each
        # read's far end, form (B) of item 34, HISTORY)
        axis_contents = None if field else self._axis_contents(live.family)
        twists = None if field else self._port_twists(live, False)
        sigma_self = self._self_source(live, False)
        window = self._window(live.box, self.kind_wrap[live.family])
        im_next: np.ndarray | None = None
        plain = axis_contents is None and twists is None and live.im_now is None and sigma_self is None
        if not plain:
            # THE FOUR PACES AND THE TRANSPORT (ALGEBRA.md 9.91 (2), (6); commits 3 and 4):
            # the arrivals per axis after the transport, the rule per level on the whole
            # board (HOST: no window shortcut here); the second level allocated by the
            # first rotation that writes it
            reads_re, reads_im = self._arrivals(live, twists, False)
            nxt, live.remainder = self._level_step(
                num,
                den,
                gamma,
                content,
                axis_contents,
                reads_re,
                live.now,
                live.before,
                live.remainder,
                not field,
            )
            if sigma_self is not None:
                nxt -= sigma_self  # the self-source's term, w Sigma_self off the right side (9.91 (5))
            if reads_im is not None or live.im_now is not None:
                if live.im_now is None:
                    live.im_now = np.zeros_like(live.now)
                    live.im_before = np.zeros_like(live.now)
                    live.im_remainder = np.zeros_like(live.now)
                assert live.im_before is not None and live.im_remainder is not None
                im_reads = [np.zeros_like(live.now) for _ in range(3)] if reads_im is None else reads_im
                im_next, live.im_remainder = self._level_step(
                    num,
                    den,
                    gamma,
                    content,
                    axis_contents,
                    im_reads,
                    live.im_now,
                    live.im_before,
                    live.im_remainder,
                    not field,
                )
            live.box = None
        elif window is None:
            arrivals = self._axis_sums(live.now, self.kind_wrap[live.family])
            reads, self_coefficient, wall = coefficients(num, den, gamma, content, ISOTROPIC, not field)
            nxt, live.remainder = rule3(
                reads, arrivals, self_coefficient, wall, live.now, live.before, live.remainder
            )
            live.box = None
        else:
            # HOST (record 2039 (b); item 43): the rule on the support box grown
            # by one, zeros elsewhere; the same integers at every Node
            slices, wraps, grown = window
            content_w = content[slices] if isinstance(content, np.ndarray) else content
            arrivals = self._axis_sums(live.now[slices], wraps)
            reads, self_coefficient, wall = coefficients(
                num[slices], den[slices], gamma, content_w, ISOTROPIC, not field
            )
            nxt_w, remainder_w = rule3(
                reads,
                arrivals,
                self_coefficient,
                wall,
                live.now[slices],
                live.before[slices],
                live.remainder[slices],
            )
            nxt = np.zeros_like(live.now)
            nxt[slices] = nxt_w
            live.remainder[slices] = remainder_w
            live.box = grown
        largest = int(np.max(np.abs(nxt)))
        if im_next is not None:
            largest = max(largest, int(np.max(np.abs(im_next))))
        if self.world.massive_record and largest > self.world.amplitude_bound:
            raise RuntimeError(
                f"the record {live.identity} reached the level "
                f"{largest} at interval {self.tick}, above the world's declared "
                f"amplitude bound A = {self.world.amplitude_bound} (issue #1085; MUST 3's bound "
                "holds only below A): the run is refused"
            )
        if im_next is not None:
            if live.mask is not None:
                im_next[~live.mask] = 0
            live.im_before = live.im_now
            live.im_now = im_next
        if not booked:
            live.before = live.now
            live.now = nxt
            live.age += 1
            return
        if live.mask is not None:
            # the arm's row lives on its own side of the lamp (component 2)
            nxt[~live.mask] = 0
        live.before = live.now
        live.now = nxt
        live.age += 1
        if live.window_open:
            # THE POINT EMITTER (ALGEBRA.md 9.71 (1) (b), (c); item 50): the
            # window's write and its outward reading right after the record's
            # own step, before any booking reads the rows: the bookings read
            # the rows as the interval leaves them, both levels with their
            # writes (a flux read across a write books the write itself)
            self._window_write(live)
        # THE FLUX READING (ALGEBRA.md 9.19 (3)): after the step, the one-way
        # inward flux into every detector this interval, from the record's two
        # levels at the Ports alone (record 1934), booked to the detector's
        # pointer C; nothing is taken, the rows evolve at every Node
        before_booking = list(live.pointers)
        for detector, value in self.detector_inflow_tally(live).items():
            live.pointers[detector] += value
            live.absorbed += value
        # this interval's increment per detector
        increments = [now - then for now, then in zip(live.pointers, before_booking, strict=True)]
        self.register.at("the clicks", "(ii)")(live, increments)

    def _window_centre(self, block: Block) -> tuple[int, int, int]:
        """The body's Node of a block with a window (its centre Node)."""
        axes = np.nonzero(self.centre_mask(block))
        return (int(axes[0][0]), int(axes[1][0]), int(axes[2][0]))

    def _window_write(self, live: LiveRecord) -> None:
        """One interval of an open window (ALGEBRA.md 9.71 (1) (b), (c); item
        50; the body's declared write at its own Nodes, record 2082 (2); commit
        7), right after the record's own step: (b) the body's rotation is
        written into the given row at every Node of the body, a_given(i) += g x
        a_body(i) (the body stepped this interval already, its levels the ones
        written; a one-Node body its one Node, the body's Node of 9.71 (1)); (c) the
        norm that left the body this interval is read as the outward flux
        through its outer Ports from the two levels as the interval leaves
        them, both with their writes, and summed; the window's count grows by
        one and the record's box takes the body in."""
        block = self.block_by_number.get(live.emitter) if live.emitter is not None else None
        if block is None or block.window != live.identity:
            return
        emitter = block.definition.emitter
        if emitter is None or emitter.weight is None:
            return
        live.now[block.mask] += emitter.weight * self._body_levels(block)
        live.outward += self.body_outward_flux(live, block, live.outward_tally)
        live.window += 1
        if live.box is not None:
            live.box = tuple(
                (min(lo, low), max(hi, high))
                for (lo, hi), (low, high) in zip(live.box, self.mask_box(block.mask), strict=True)
            )

    def mask_box(self, mask: np.ndarray) -> tuple[tuple[int, int], ...]:
        """The box of a body's Nodes, [low, high) per axis (HOST)."""
        axes = np.nonzero(mask)
        return tuple((int(axis.min()), int(axis.max()) + 1) for axis in axes)

    def _body_levels(self, block: Block) -> np.ndarray:
        """The body's rotation's level now at each of its Nodes, in the mask's
        order: the standing record at its one Node (the body's Node, item 42) or its
        own rows there (the lattice body)."""
        if block.node_record is not None:
            count = int(np.count_nonzero(block.mask))
            return np.full(count, int(block.node_record.now), dtype=np.int64)
        assert block.own is not None
        return np.asarray(block.own.now[block.mask], dtype=np.int64)

    def body_outward_flux(self, live: LiveRecord, block: Block, tally: list[int] | None = None) -> int:
        """THE OUTWARD FLUX through the body's outer Ports this interval (ALGEBRA.md
        9.71 (1) (c); record 2082 (2); item 50; commit 7): over every Port from a
        Node of the body to a Node outside it, the taking's inward booking with the
        sign reversed, wall (now_j before_i - before_j now_i) where positive (the
        Link to a Node beyond an open face carries none; a folded axis none; the
        Ports along the record's own component none, 9.82 (3) (c)), from the
        record's two levels as the interval leaves them, this interval's write in
        `now` and the last one's in `before`; the pair's second level added (9.82
        (3) (b)).
        With `tally`, the flux through the Ports on the body's +a side is added to
        tally[a] and through its -a side subtracted (the given quantum's direction,
        ALGEBRA.md 9.91 (4); commit 5 without the recoil), in the same units."""
        wall = self.kind_wall(live.family)
        wrap = self.kind_wrap[live.family]
        own_axis = self.booked_axis(live)
        mask = block.mask
        levels = [(live.now, live.before)]
        if live.im_now is not None and live.im_before is not None:
            levels.append((live.im_now, live.im_before))
        total = 0
        for axis in range(3):
            if self.shape[axis] == 1 or axis == own_axis:
                continue
            for side in (1, -1):
                # the Port from i to j = i + side e_axis, j outside the body
                ports = mask & ~np.roll(mask, -side, axis=axis)
                if not wrap[axis]:
                    face: list[slice | int] = [slice(None)] * 3
                    face[axis] = -1 if side == 1 else 0
                    ports[tuple(face)] = False
                if not ports.any():
                    continue
                flux = np.zeros(int(np.count_nonzero(ports)), dtype=np.int64)
                for now, before in levels:
                    now_j = np.roll(now, -side, axis=axis)[ports]
                    before_j = np.roll(before, -side, axis=axis)[ports]
                    flux += now_j * before[ports] - before_j * now[ports]
                outward = int(flux[flux > 0].sum()) * wall
                total += outward
                if tally is not None:
                    tally[axis] += side * outward
        return total

    def _point_windows(self) -> None:
        """THE WINDOW, one interval (ALGEBRA.md 9.69 (2), 9.71 (1); BUILD.md
        section 26 item 50; the law's one giving since commit 7, 9.85 (5),
        9.91 (10) 7, record 2082 (4)): the close, after the interval's
        bookings; the write (b) and the outward reading (c) are the record's
        own, right after its step (`_window_write`). (d) At the first interval
        at which the summed outward norm reaches T (the quantum's norm, the
        emitter's `norm`) the window closes: the writing ends (the
        quantum, the stock and the ledger moved at the open, the norm T from
        there), the giving line names the record with the window's length,
        and the next excitation waits its count from here. What comes out by the law: a train of about n c_l
        Links with the band 1 / n, at the wave number light's dispersion gives
        to the body's Node's frequency; no declared train. The giving is n additive
        writes, each undone by the inverse (`_point_window_inverse`)."""
        for block in self.blocks:
            if block.window is None:
                continue
            live = self.records.get(block.window)
            emitter = block.definition.emitter
            if live is None or emitter is None or emitter.weight is None or emitter.norm is None:
                block.window = None
                continue
            if live.clicked:
                # taken while its window was open (its own body's Node's set reading the
                # returning light, the light clock): the window closes at the
                # click, the record named
                self._close_window(block, live)
                continue
            # (d) the close: the outward norm against the excitation's action T as
            # the exact rational norm / norm_denominator, both in the form's units
            denominator = emitter.norm_denominator if emitter.norm_denominator is not None else 1
            if live.outward * denominator >= emitter.norm:
                self._close_window(block, live)

    def _close_window(self, block: Block, live: LiveRecord) -> None:
        """The window's close (ALGEBRA.md 9.71 (1) (d); item 50): the writing
        ends, the record is named on its giving line with the window's length
        and the open's interval, the next excitation's count starts (the
        quantum moved at the open: the stock, the content and the ledger's
        rows as the train emitter's; the norm T from the open)."""
        emitter = block.definition.emitter
        assert emitter is not None
        live.window_open = False
        block.window = None
        if live.giving_line is not None and self.record is not None:
            line = dict(live.giving_line)
            line["tick"] = self.tick
            line["norm"] = live.norm
            line["pace"] = live.pace
            line["window"] = live.window
            line["outward"] = live.outward
            line["opened"] = self.tick - live.window  # the open's interval (HOST)
            # THE GIVEN QUANTUM'S FOUR-VECTOR (ALGEBRA.md 9.86 (1), 9.91 (4); commit 5
            # without the recoil): the count 1, the space part the sign per axis of
            # the outward flux through the body's Ports over the window (DETECTOR);
            # a symmetric emitter's tallies cancel (9.84 (2)); no body's momentum moves
            line["momentum"] = self.direction_of(live.outward_tally)
            self.record(line)
        live.giving_line = None
        block.wait = 0
        if self.stock_of(block) > 0:
            block.excitations += 1

    def _point_window_inverse(self, block: Block) -> None:
        """One interval of an open window backwards (ALGEBRA.md 9.71 (1) (e)):
        the interval's outward reading taken off the sum on the rows as the
        interval left them, then the write subtracted (an addition inverts),
        before the record's own inverse step; the body's Node's level is the one
        written, its own inverse coming after."""
        live = self.records.get(block.window) if block.window is not None else None
        emitter = block.definition.emitter
        if live is None or emitter is None or emitter.weight is None or live.window <= 0:
            return
        undone = [0, 0, 0]
        live.outward -= self.body_outward_flux(live, block, undone)
        live.outward_tally = [kept - gone for kept, gone in zip(live.outward_tally, undone, strict=True)]
        live.now[block.mask] -= emitter.weight * self._body_levels(block)
        live.window -= 1

    def _reads_at(self, a: np.ndarray, nodes: np.ndarray, wrap: tuple[bool, bool, bool]) -> np.ndarray:
        """The sum of the six neighbours' amplitudes at the Nodes (flat
        indices) alone, as `_neighbours` reads them over the board (the wrap
        on a periodic axis, 0 beyond a zero face, the row itself on an axis
        of one layer); HOST: the cost is the Nodes asked, not the board."""
        coordinates = np.stack(np.unravel_index(nodes, self.shape), axis=0)
        total = np.zeros(nodes.shape[0], dtype=object)
        for axis in range(3):
            if self.shape[axis] == 1:
                total += 2 * a.ravel()[nodes].astype(object)
                continue
            for sign in (1, -1):
                shifted = coordinates.copy()
                shifted[axis] = shifted[axis] - sign
                if wrap[axis]:
                    shifted[axis] %= self.shape[axis]
                    inside = np.ones(nodes.shape[0], dtype=bool)
                else:
                    inside = (shifted[axis] >= 0) & (shifted[axis] < self.shape[axis])
                    shifted[axis] = np.clip(shifted[axis], 0, self.shape[axis] - 1)
                values = a[tuple(shifted)].astype(object)
                total += np.where(inside, values, 0)
        return total

    def node_density(self, live: LiveRecord, nodes: np.ndarray) -> list[Ratio]:
        """The record's density e at each of the Nodes (flat indices), the
        per-Node terms of `form_share` (the Node's term over the rule's read
        coefficient there, less its Link term), exact rationals in the form's
        units; read on the Nodes outside a moving set's faces (ALGEBRA.md 9.74
        (2); item 56; the hop's reading of item 48 HISTORY)."""
        family = live.family
        wall = self.kind_wall(family, live.pair)
        field = live.held_part
        gamma = 1 if field else self.node_clock
        content = self._effective_content(family) if not field else np.zeros(self.shape, dtype=np.int64)
        num_all, den_all = self.pair_arrays(family, live.pair)
        num = num_all.ravel()[nodes]
        den = den_all.ravel()[nodes]
        level = content.ravel()[nodes]
        levels = [(live.now, live.before)]
        if live.im_now is not None and live.im_before is not None:
            levels.append((live.im_now, live.im_before))  # the pair's second level (commit 4)
        out: list[Ratio] = [ZERO for _ in range(len(nodes))]
        for level_now, level_before in levels:
            now = level_now.ravel()[nodes]
            before = level_before.ravel()[nodes]
            reads = self._reads_at(level_before, nodes, self.kind_wrap[family])
            for index in range(len(nodes)):
                (read_coefficient, _, _), self_coefficient, wall_at = coefficients(
                    int(num[index]), int(den[index]), gamma, int(level[index]), ISOTROPIC, not field
                )
                a, b = int(now[index]), int(before[index])
                node = wall * form_term(self_coefficient, wall_at, a, b)
                out[index] = ratio_sum(
                    [
                        out[index],
                        (node - wall * a * int(reads[index]) * read_coefficient, read_coefficient),
                    ]
                )
        return out

    def _ladder_of(self, live: LiveRecord) -> list[int]:
        """The record's ladder in its declared order (ALGEBRA.md 9.19 (3)
        (b)): the emitter's named sets (`receiver`, a list), or the block's
        one receiver, or every detector set as declared; the face receiver
        last on every ladder (record 15)."""
        if live.ladder is not None:
            ladder = list(live.ladder)
        else:
            receiver = self._receiver_of(live)
            ladder = [receiver] if receiver is not None else list(self.set_detectors)
        if self.face_detector is not None and self.face_detector not in ladder:
            ladder.append(self.face_detector)
        return ladder

    def _ladder_click(self, live: LiveRecord, increments: list[int]) -> None:
        """The increment ladder: the record's running total gains this interval's one-way flux into its ladder's detectors in the declared order; the click fires at the first interval at which the total crosses the threshold fixed at the giving, at the detector whose segment holds it (Born's rule its theorem); the record is deleted whole after the interval's advances."""
        if live.clicked:
            return
        if live.norm <= 0:
            # a record without its norm yet (the point emitter's open window, item
            # 50): the bookings enter the running total, the click waits for the norm
            live.total += sum(increments)
            return
        ladder = self._ladder_of(live)
        # the norm as the exact rational norm / pace (item 36): the plain
        # flux C against it, 2 W pace C against (2 u + 1) norm
        threshold = (2 * live.u + 1) * live.norm
        running = 2 * live.wheel * live.pace * live.total
        for detector in ladder:
            running += 2 * live.wheel * live.pace * increments[detector]
            live.total += increments[detector]
            if running >= threshold:
                live.first_rung[detector] = self.tick
                if detector in self.set_block:
                    self.rung_counts[(live.identity, detector)] = self.block_by_number[
                        self.set_block[detector]
                    ].count
                self._gather_line(live, detector)
                live.clicked = True
                self.dead.append(live.identity)
                return

    def record_form(self, live: LiveRecord) -> Ratio:
        """The conserved form I of the record (MASSIVE_RECORD.md section 3, a
        GAMEBOARD diagnostic read by the books): the one form of the rule,
        `conserved_form` (ALGEBRA.md 9.57 (1); item 44: from the rule's own
        integers, L [w (a^2 + b^2) - S a b] / R at the Nodes and L now_i SUM_j
        before_j on the Links, L the least common multiple of the distinct
        numerators, an exact rational; the plain form 3 den (a^2 + b^2) less
        num over the Links in the vacuum); conserved by the rule up to the
        remainders' bounded jitter (the books' second copy of the form, with
        its own Link loop, HISTORY since item 44: one form, one code)."""
        return self.conserved_form(live)

    def _release(self, live: LiveRecord) -> None:
        """The record's rows leave the board: the emitters' lists and the
        rung counts of the record are dropped."""
        for block in self.blocks:
            if live.identity in block.emitted:
                block.emitted.remove(live.identity)
        for key in [key for key in self.rung_counts if key[0] == live.identity]:
            del self.rung_counts[key]

    def _gather_line(self, live: LiveRecord, chosen: int | None) -> None:
        """The record's one click line (`gather`, the amplitude law's keys):
        the content handed to the measured event at the chosen detector (or
        booked as escaped at a face or a set without a body; with no detector
        chosen, to the escaped row or, where the record's own emitter took
        it wholly, to `taken_by_emitter`), the line written with `click` the
        chosen detector's first rung (or the completion where no rung was
        crossed) and `clock` the detector's own count. Called once per
        record: at the close (`_click`) or, under the receiver by name, at
        the receiver's rung (`_line_at_rung`)."""
        # the ladder's weights: the record's ladder of `_ladder_of` (the
        # emitter's named sets, or the block's receiver, or every declared
        # set, the face receiver last on every ladder; ALGEBRA.md 9.19 (3)
        # (b)), every detector off it at 0, so that the detector of u is over the
        # ladder's own sum and a detector off the ladder is never chosen
        ladder_detectors = set(self._ladder_of(live))
        on_ladder = [detector in ladder_detectors for detector in range(len(live.pointers))]
        weights = [(p if here else 0, 1) for p, here in zip(live.pointers, on_ladder, strict=True)]
        family = live.family
        ladder, total = rungs(weights, live.wheel)
        sunk = sum(p for p, here in zip(live.pointers, on_ladder, strict=True) if not here)
        if chosen is None:
            self.ledger.transit_escaped[family] += live.content
            self.ledger.held_escaped[family] += 0
        else:
            measured = self.detector_measured[chosen]
            if measured is not None and not self.detector_face[chosen]:
                self.held[measured][family] += live.content
                self.ledger.held_measured[family] += live.content
                self.ledger.transit_absorbed[family] += live.content
            else:
                # a set without a body (the face receiver, a set on free Nodes):
                # the click consumes the quantum as any click does
                self.ledger.transit_absorbed[family] += live.content
        self.layer.gathered += 1
        gather: dict[str, object] = {
            "event": "gather",
            "tick": self.tick,
            "arrived": self.tick,
            "family": self.families[family].name,
            "record": live.identity,
            # HOST: the giving residue, the input of the diagnostic E_N and never
            # a reader-of-record field (the reader reads `click`, `giving` and
            # `chosen`; DECLARATIONS.md section 2 item 8)
            "u": live.u,
            # HOST: the ledger's row `taken_by_emitter` is 0 since the emitter's
            # own take retired (ALGEBRA.md 9.17); kept for the readers' form
            "taken_by_emitter": 0,
            # HOST (the receiver by name): the sinks' take of the record by
            # this line, in the pointer's unit (the faces and every set but
            # the receiver; on no pointer); on a record with a receiver alone
            "given": live.given,
            "chosen": (
                [[self.detector_set[chosen], self.detector_channel[chosen], "0"]]
                if chosen is not None
                else None
            ),
            "node": [],
            "windows": [],
            "content": live.content,
            # THE FOUR-VECTOR (ALGEBRA.md 9.86 (1); commit 5 without the recoil): the
            # count is `content`, the space part the sign per axis of the chosen
            # detector's tally, the taken quantum's direction of travel (DETECTOR);
            # [0, 0, 0] with no detector chosen. No body's momentum moves (record 2135)
            "momentum": (
                self.direction_of(live.momentum_tally.get(chosen, [0, 0, 0]))
                if chosen is not None
                else [0, 0, 0]
            ),
            "weight": [live.pointers[chosen] if chosen is not None else 0, 1],
            "total": list(total),
            "T": live.absorbed,
            "before": sum(1 for p in live.pointers if p),
            "after": 1 if chosen is not None else 0,
            "detectors": [
                [[[set_name, channel, "0"]], rung]
                for set_name, channel, rung, pointer in zip(
                    self.detector_set, self.detector_channel, ladder, live.pointers, strict=True
                )
                if pointer
            ],
            # the ladder by name (the lamp's `receiver`): the sets on it, and
            # HOST the pointers' sum at the sinks (the detectors off the ladder,
            # taken and booked, never chosen); None and 0 for every detector
            **(
                {
                    "ladder": sorted({self.detector_set[detector] for detector in live.ladder}),
                    "sunk": sunk,
                }
                if live.ladder is not None
                else {}
            ),
            "giving": live.giving_tick,
            # The click's time: the interval at which the chosen detector's pointer
            # crossed its first rung (the counting form, s_D = 1 / W), the
            # detector's own count on the click line; the record completed at
            # `tick`, when its offer was exhausted.
            "click": (
                live.first_rung[chosen]
                if chosen is not None and live.first_rung[chosen] is not None
                else self.tick
            ),
            # the gate reviewer's line on the click's time (the Boss's 01:40Z): which the click's time
            # is, the chosen detector's first rung or, where no rung was crossed
            # (a screen row's Node at 1e-4 of the norm), the completion
            # interval; a reader never reads a completion as a rung.
            "click_at": (
                "rung" if chosen is not None and live.first_rung[chosen] is not None else "completion"
            ),
            # whose count the `clock` stamp is: a block's own count where the
            # chosen detector is a block's detector or a set bound to a block (keys (i)
            # and (ii)), else the interval
            "clock_source": (
                f"measured:{self.detector_measured[chosen]}"
                if chosen is not None and (live.identity, chosen) in self.rung_counts
                else "interval"
            ),
            **(
                {
                    "clock": (
                        # A block's detector: the block's own count at the first
                        # rung (the body's event in the body's own clock);
                        # a receiver as built: its count is the interval.
                        self.rung_counts[(live.identity, chosen)]
                        if chosen is not None and (live.identity, chosen) in self.rung_counts
                        else live.first_rung[chosen]
                        if chosen is not None and live.first_rung[chosen] is not None
                        else self.tick
                    )
                }
                if self.world.clock_stamp
                else {}
            ),
        }
        self.layer.gathers.append(gather)
        if self.record is not None:
            self.record(gather)

    def step(self) -> None:
        """One interval: the clock, then the file's acts in the file's order, each through the register, then the interval's closing (the bodies' clocks, the clicked records leaving, the readings)."""
        self.tick += 1
        for place, name, stage, words in self._acts:
            stage(self.register.at(name, place), **words)
        self._close_interval()

    # The readings

    def books(self, recount: bool = False) -> dict[str, object]:
        families: dict[str, object] = {}
        balanced = True
        ledger = self.ledger
        for index, family in enumerate(self.families):
            current = sum(h[index] for h in self.held)
            measured = {
                "initial": ledger.held_initial[index],
                "measured": ledger.held_measured[index],
                "became": 0,
                "current": current,
                "spent": ledger.held_spent[index],
                "escaped": ledger.held_escaped[index],
            }
            measured["balanced"] = measured["initial"] + measured["measured"] == (
                measured["current"] + measured["spent"] + measured["escaped"]
            )
            transit_current = sum(live.content for live in self.records.values() if live.family == index)
            transit = {
                "initial": 0,
                "released": ledger.transit_released[index],
                "current": transit_current,
                "absorbed": ledger.transit_absorbed[index],
                "escaped": ledger.transit_escaped[index],
                # HOST (item 10): the content the records' own emitters took
                "taken_by_emitter": ledger.taken_by_emitter[index],
                # HOST (the receiver by name): the count of records closed
                # after their line at the receiver's rung; on a world with a
                # receiver alone (a lamp world's books byte for byte)
                **(
                    {"closed_after_click": ledger.closed_after_click[index]} if self.has_receiver else {}
                ),
            }
            transit["balanced"] = transit["released"] == (
                transit["current"]
                + transit["absorbed"]
                + transit["escaped"]
                + transit["taken_by_emitter"]
            )
            balanced = balanced and bool(measured["balanced"]) and bool(transit["balanced"])
            lines: dict[str, object] = {"measured": measured, "transit": transit}
            if self.world.massive_record:
                # The conserved form I summed over the family's live records
                # (massive-record-v1): a GAMEBOARD diagnostic, written under
                # the key alone.
                lines["form"] = form_json(
                    ratio_sum(
                        [
                            self.record_form(live)
                            for live in self.records.values()
                            if live.family == index
                        ]
                        + [
                            self.record_form(record)
                            for record in (
                                [self.held_records[index], *self.held_parts[index]]
                                if index in self.held_records
                                else []
                            )
                            if not record.silent
                        ]
                    )
                )
            families[family.name] = lines
        return {
            "tick": self.tick,
            "families": families,
            # Issue #1086 (the Boss's 02:00Z): the momentum books are a GAMEBOARD
            # diagnostic, no law and no pin: `held` the sum of the blocks'
            # declared momentum vectors (the momentum on the board's bodies);
            # `transit` and `escaped` are not accounted until the massive
            # kind's momentum books are designed (ALGEBRA.md 8.11, the
            # physicist's), and `balanced` counts content alone.
            "momentum": {
                "held": [sum(int(block.momentum[axis]) for block in self.blocks) for axis in range(3)],
                "transit": None,
                "escaped": None,
                "note": "transit and escaped not accounted (the massive kind's momentum books "
                "are not designed, ALGEBRA.md 8.11); balanced counts content alone",
            },
            "records": len(self.records),
            "balanced": balanced,
            "balanced_scope": "content alone (the momentum books are not accounted)",
        }

    def contents(self) -> list[dict[str, object]]:
        return [
            {
                "number": number,
                "position": list(entry.position),
                "family": self.families[entry.family].name,
                "held": list(self.held[number]),
            }
            for number, entry in enumerate(self.world.measured)
        ]

    def snapshot_stream(self) -> Iterator[tuple[str, object]]:
        """The state's (key, value) pairs for state.json: the tick,
        the held content per measured event and the live records (their
        identity, age, train and the detectors' pointers), not their rows."""
        yield "tick", self.tick
        yield "measured", self.contents()
        # the held families' levels over the board (GAMEBOARD; ALGEBRA.md 9.45,
        # 9.48; item 51): each by its declared name and source, the Node
        # clock's Gamma beside them
        yield "node_clock", self.node_clock
        yield (
            "held_fields",
            [
                {
                    "family": self.families[family].name,
                    "held": self.families[family].held,
                    "rows": record.now.ravel().tolist(),
                    "form": form_json(self.record_form(record)),
                }
                for family, record in self.held_records.items()
            ],
        )
        if self.world.massive_record:
            # The blocks (massive-record-v1): the corner, the count, the
            # momentum's accumulators, the steps, and the rows of the block's
            # own record (its amplitude now over the board, GAMEBOARD: the
            # mode's extent is read from them).
            yield (
                "blocks",
                [
                    {
                        "measured": block.number,
                        "family": self.families[block.family].name,
                        "corner": list(block.corner),
                        "side": block.definition.side,
                        "extents": list(block.definition.extents),
                        "clock": block.count,
                        "steps": block.stepped,
                        "drive": list(block.drive),
                        "momentum": list(block.momentum),
                        "spin": list(block.spin),
                        "fixed": block.fixed,
                        "emitted": list(block.emitted),
                        "rows": None if block.own is None else block.own.now.ravel().tolist(),
                        "form": (
                            form_json((self.node_record_form(block), 1))
                            if block.node_record is not None
                            else None
                            if block.own is None
                            else form_json(self.record_form(block.own))
                        ),
                        # the body's Node's record, (a, b, r) at the body's Node (9.60; item 42; GAMEBOARD)
                        "node_record": (
                            None
                            if block.node_record is None
                            else [
                                block.node_record.now,
                                block.node_record.before,
                                block.node_record.remainder,
                            ]
                        ),
                    }
                    for block in self.blocks
                ],
            )
        yield (
            "records",
            [
                {
                    "record": live.identity,
                    "lamp": live.lamp,
                    "family": self.families[live.family].name,
                    "u": live.u,
                    # HOST (the receiver by name): whether the record's line
                    # was written at its receiver's rung (it lives on with
                    # content 0); on a world with a receiver alone
                    **({"clicked": live.clicked, "escaped": live.escaped} if self.has_receiver else {}),
                    "given": live.given,
                    "giving": live.giving_tick,
                    "age": live.age,
                    "train": live.train,
                    "norm": live.norm,
                    "absorbed": live.absorbed,
                    "pointers": dict(zip(self.detector_names, live.pointers, strict=True)),
                    **({"form": form_json(self.record_form(live))} if self.world.massive_record else {}),
                }
                for live in self.records.values()
            ],
        )
