"""The records' bookkeeping the loop steps (HOST classes, no line of the law): the live record with its arrays, a body's record on its one Node, the block (a body on the GameBoard), the books per family and the runner's layer of lines."""

from __future__ import annotations

from collections.abc import Iterator
from dataclasses import dataclass, field

import numpy as np

from event_universe.events.output import Ratio
from event_universe.loader.world import BlockDefinition


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
    # THE RESIDUE FROM THE LAW (ALGEBRA.md #a-familys-declaration; BUILD.md section 26 item
    # 15): the record's own wheel W, given with its residue u, both read from
    # the rule's remainder at the giving Node of the record that clicked to
    # giving it (`residue_of`); a planted record carries the test's W. The
    # rung's wheel is the record's, never a set's or the world's. UNDER THE
    # NODE CLOCK (ALGEBRA.md #the-paces; BUILD.md section 26 item 31) W
    # = 3 den f / gcd(Gamma num, 6 den M, 3 den f) at that Node with f =
    # Gamma + M (`wheel_at`): the pair's own where the content M is 0,
    # content-dependent at a body's Nodes, read from the rule and never
    # declared.
    wheel: int = 1
    # massive-record-v1: the emitter's number for a record a body emitted
    # (None for a planted record and for a block's own record); the
    # coupling's folded denominator (`scale`) is HISTORY since the model
    # owner's decision (2) of the record (the wall 3 den alone, one D per
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
    # HOST (the record (b); BUILD.md section 26 item 43): the record's support
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

    # THE INCREMENT LADDER (ALGEBRA.md #the-ladder): the record's running total
    # C of its one-way flux into the detectors of its ladder, every detector's
    # increment in the ladder's order, against the record's threshold
    # (2 u + 1) T / (2 W) fixed at its giving; the click at the interval C
    # crosses it, at the detector whose segment of that interval's increment
    # holds the threshold.
    total: int = 0
    # whether the record's line was written (the record is deleted whole at
    # that interval, ALGEBRA.md 8.8, the record)
    clicked: bool = False
    # THE BOOKING IN THE BODY'S FRAME (ALGEBRA.md #the-ladder; BUILD.md section
    # 26 item 56): per detector of a moving set, the fraction of the face's
    # booking below one unit of the flux, carried to the next interval's
    # booking (a remainder kept on the record, exact); empty at rest
    carry: dict[int, Ratio] = field(default_factory=dict)
    # THE FOUR-VECTOR CLICK'S SPACE PART (ALGEBRA.md #the-primitives, #the-interval,
    # ALGEBRA.md #the-ladder; commit 5 without the recoil): per detector, per
    # axis, the flux booked through the detector's Ports on its -a side minus
    # the flux booked through those on its +a side, summed over the record's
    # walk (the taken quantum's direction of travel: a quantum moving toward
    # +a enters through the -a face); the sign per axis is sigma_a on the
    # click line. Nothing is added to any body's momentum: the recoil of
    # ALGEBRA.md #the-primitives waits on the closing of the record (the click that keeps the
    # momentum, 9.109, is a decision of three).
    momentum_tally: dict[int, list[int]] = field(default_factory=dict)
    # THE GIVEN QUANTUM'S DIRECTION (ALGEBRA.md #the-interval, the giving's tally): per axis, the
    # outward flux through the body's +a Ports minus through its -a Ports over
    # the window, the sign per axis on the giving line at the close
    outward_tally: list[int] = field(default_factory=lambda: [0, 0, 0])
    # THE POINT EMITTER'S WINDOW (ALGEBRA.md; BUILD.md section 26 item
    # 50): open from the giving click until the outward norm through the
    # body's Node's six Ports reaches T; the intervals written and the outward norm
    # summed; the giving line held until the close names the record
    window_open: bool = False
    window: int = 0
    # THE FAMILY GENERICITY (the record; item 51): a body's own standing
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
    # THE RECORD'S PAIR (ALGEBRA.md #the-primitives, #the-interval; the one stroke, commit
    # 1): the rest pair its rows step with, its family's declared pair or, on
    # a family whose pair is the body's, the body's `kind` or the emitter's
    # `pair`; the board's pair arrays are read by (family, pair); None reads
    # the family's declared pair (a record made without one, the tests')
    pair: tuple[int, int] | None = None
    # THE COMPONENT (ALGEBRA.md #the-primitives, #the-interval): the index of the record's
    # component in its family's parts (0 the time part; a wave of light in
    # one transverse component of the charge family, commit 4)
    part: int = 0
    # THE HELD PART (item 51; ALGEBRA.md #the-interval): a field family's component
    # record, stepped plain at the pace 1, written by the hold at the bodies'
    # Nodes, booked by no detector; marked on the record, not on its family
    # (the charge family is held and has waves, ALGEBRA.md #the-primitives)
    held_part: bool = False
    # HOST (the record (b); ALGEBRA.md #the-interval "the support-box shortcut keeps a zero
    # part free of work"): a held part never written nonzero: its two levels
    # and remainder are zero everywhere and step to zero exactly, so the step
    # is skipped; cleared by the first nonzero hold
    silent: bool = False
    # THE NORM'S DENOMINATOR (ALGEBRA.md #the-direction; BUILD.md section 26 item
    # 36): the record's conserved form is the exact rational norm / pace (the
    # Node's terms weighted by 1 / p_i); at one level p times the form is
    # whole and the pair reduces from (p x form, p), the pace Gamma - c + q
    # Lambda d at the body's Nodes as written; the ladder reads the plain
    # flux against it, 2 W pace C against (2 u + 1) norm. 1 for a record
    # whose norm is set in the form's own units.
    pace: int = 1
    # THE SECOND LEVEL of a phase-2 record (ALGEBRA.md #the-interval; commit 4): the pair's
    # second component, (now, before, r) over the board, None until a rotation of the
    # transport writes it (a second level that starts zero and meets no twist stays
    # exactly zero, ALGEBRA.md #the-interval)
    im_now: np.ndarray | None = None
    im_before: np.ndarray | None = None
    im_remainder: np.ndarray | None = None
    # THE TWIST "OWN" (ALGEBRA.md #the-primitives): round(2^16 omega_0), the record's own
    # rotation in the table's unit, the loader's integer; 0 for a record with none (a
    # held part, a planted record without one)
    twist: int = 0

    def arrays(self) -> Iterator[np.ndarray]:
        """The record's arrays on the GameBoard: its two levels and remainder, and the second level's where the family has one."""
        for array in (
            self.now,
            self.before,
            self.remainder,
            self.im_now,
            self.im_before,
            self.im_remainder,
        ):
            if isinstance(array, np.ndarray):
                yield array


@dataclass
class NodeRecord:
    """A body's record on its one Node: the two levels and the remainder of its standing wave, stepped by the rule alone with the count's wall."""

    identity: int
    now: int
    before: int
    remainder: int = 0
    u: int = 0
    wheel: int = 1
    norm: int = 0


@dataclass
class Block:
    """A block on the board (massive-record-v1, MASSIVE_RECORD.md sections 4 to 7; BUILD.md section 2): its Nodes R (the mask over the board, the cube of `side` at `corner`), its own massive record (the seed on its Nodes), the light records it emitted, its clock (its record's cycles across R), its momentum per axis with the drive's accumulators against its wall W = 3 Q M (`wall_of`, live with its quanta; ALGEBRA.md #the-primitives), and its detector among the simulation's detectors."""

    number: int
    family: int
    definition: BlockDefinition
    corner: list[int]
    mask: np.ndarray
    detector: int
    momentum: list[int]
    # THE SPIN AS STATE (ALGEBRA.md #a-familys-declaration, #the-interval; commit 6): S now and S one
    # interval back, the leapfrog's two integers; the load's write is the body's
    # declared `spin` at both
    spin: list[int] = field(default_factory=lambda: [0, 0, 0])
    spin_before: list[int] = field(default_factory=lambda: [0, 0, 0])
    # A TOOL HELD IN PLACE (ALGEBRA.md #the-primitives; the Boss's the record): the world's
    # word `fixed`; the feed, when it lands, acts on a body without the word alone
    fixed: bool = False
    # THE COUNT AT A NODE (ALGEBRA.md #the-counts-line; the count's line bound): the body's
    # quanta per Node and the line's remainder, laid at the line's first act; the body's Nodes
    # follow the count's centroid by whole Links, `moved` where they shifted in the last act
    counts: np.ndarray | None = None
    count_remainder: np.ndarray | None = None
    count_norm: int = 0
    moved: bool = False
    previous_sum: int = 0
    own: LiveRecord | None = None
    # THE BODY'S RECORD AT ITS BODY'S NODE (ALGEBRA.md #what-a-body-is; item 42, item 37
    # HISTORY): the standing record on the body's Node under the world key
    # `body_record`, its own rows then nowhere else on the GameBoard (`own`
    # None); None under the lattice body
    node_record: NodeRecord | None = None
    emitted: list[int] = field(default_factory=list)
    current: int | None = None
    givings: int = 0
    # THE POINT EMITTER (item 50): the identity of the given record whose
    # window is open at this body, None when none is
    window: int | None = None
    new_cycle: bool = False
    # the interval the current cycle began and the last cycle's length (the
    # emitted record's period for its grace, the block's grace for its emitted records)
    cycle_start: int = 0
    cycle_length: int = 0
    # the emitter as a clicking body (ALGEBRA.md #the-click, #the-ladder
    # (c)): the excitations started (k), the intervals counted since the
    # residue's read (the count t against (2 u + 1) P / (2 W), no running
    # total), and whether the tick fired this interval
    excitations: int = 0
    wait: int = 0
    emit_now: bool = False
    # THE READ POINT OF THE FIRST RESIDUE (ALGEBRA.md #rule3, #the-ladder):
    # the load's seed has the remainders 0 at the write and nonzero after
    # one step of the rule, so the first u and W are read from the body's
    # own remainder at the first shell Node after its first advance; every
    # later residue is read at the click (ALGEBRA.md #the-ladder)
    residue_pending: bool = False
    # THE HOLDS' REMAINDERS (ALGEBRA.md #the-interval; the one stroke, commit 2): per
    # held family and part, the division's remainder carried between intervals
    # and the value written, (family, part) for the support's writes and ("d",
    # family, i, j, sigma) for the dipole's on the Node + sigma e_j; exact and
    # inverted with the body
    hold_carry: dict[tuple[object, ...], int] = field(default_factory=dict)
    hold_value: dict[tuple[object, ...], int] = field(default_factory=dict)


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
