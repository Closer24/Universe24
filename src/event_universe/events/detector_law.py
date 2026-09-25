"""The local detector law (`detector-law-v1`; the model owner's words of
2026-09-23, docs/designs/detector_law/DESIGN.md): the ray splits at every
free Node inside the board and holds its amplitudes; outside there is no
board, only clicks, and nothing passes from Node to Node except through a
detector, at rest or moving. Selected by the world key `detector_law`,
beside the ray law as built, which stays the default.

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
are the Nodes it has reached, the rest zero), one record per birth.

The Outside (DESIGN.md sections 1 and 5): two things only on the board,
the free Node and the receiver-inserter. A measured event with a lamp
INSERTS: each birth is a record driven at the lamp's Nodes by the
family's clock (the pair `phase_per_link` [n, d] on the circle of N steps)
for the lamp's train (the key `train`, in periods); the lamp pays the
family's quantum h at the birth. Every measured event's Nodes, every
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
and `birth` the record's birth stamp) is written, the record's content h
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

from collections.abc import Callable, Iterator, Sequence
from dataclasses import dataclass, field
from fractions import Fraction
from math import gcd

import numpy as np

from event_universe.core.game_board import Address3
from event_universe.core.integer import by_drive
from event_universe.events.amplitude import rungs
from event_universe.events.world import (
    AXES,
    BEAM_LAW,
    LABEL_SCALE,
    BlockDefinition,
    NatureBeamWorld,
    Vector,
    body_node_indices,
)

Record = Callable[[dict[str, object]], None]

DETECTOR_LAW_RULE = "detector-law-v1"
UNIT = 1 << 20  # the amplitude unit (the wheel's resolution)
FACE_NAMES = ("face:-x", "face:+x", "face:-y", "face:+y", "face:-z", "face:+z")
DEFAULT_TRAIN = 32  # periods of the record's clock (DESIGN.md section 6.2)
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


def form_json(value: Fraction) -> list[int]:
    """A form's exact rational for the books and the state (GAMEBOARD): the
    pair [numerator, denominator] in lowest terms (the denominator 1 for a
    record at one level and for the fields; ALGEBRA.md 9.50 (13))."""
    return [value.numerator, value.denominator]


@dataclass
class LiveRecord:
    """One record on the board: its dense rows and its ledger."""

    identity: int
    lamp: int
    family: int
    u: int
    born: int
    birth_tick: int
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
    # 15): the record's own wheel W, born with its residue u, both read from
    # the rule's remainder at the birth Node of the record that clicked to
    # birth it (`residue_of`); a planted record carries the test's W. The
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
    # Bell's four settings and the no-signalling control, DESIGN.md 6.3): a lamp with `arms` births one record
    # per arm on one birth stamp (the same ordinal, u and tick), each arm's
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
    # (2 u + 1) T / (2 W) fixed at its birth; the click at the interval C
    # crosses it, at the detector whose segment of that interval's increment
    # holds the threshold.
    total: int = 0
    # whether the record's line was written (the record is deleted whole at
    # that interval, ALGEBRA.md 8.8, record 1888)
    clicked: bool = False
    # The sinks' take of a record under the receiver by name (HOST, the
    # pointer's unit): what the faces and every set but the receiver took,
    # inside `absorbed` (the completion's measure) and on no pointer.
    escaped: int = 0
    # THE NORM'S DENOMINATOR (ALGEBRA.md 9.50 (13); BUILD.md section 26 item
    # 36): the record's conserved form is the exact rational norm / pace (the
    # Node's terms weighted by 1 / p_i); at one level p times the form is
    # whole and the pair reduces from (p x form, p), the pace Gamma - c + q
    # Lambda d at the body's Nodes as written; the ladder reads the plain
    # flux against it, 2 W pace C against (2 u + 1) norm. 1 for a record
    # whose norm is set in the form's own units.
    pace: int = 1


@dataclass
class Block:
    """A block on the board (massive-record-v1, MASSIVE_RECORD.md sections 4
    to 7; BUILD.md section 2): its Nodes R (the mask over the board, the
    cube of `side` at `corner`), its own massive record (the seed on its
    Nodes), the light records it emitted, its clock (its record's cycles
    across R), its momentum per axis with the drive's accumulators against
    the wall 3 Q S M, and its detector among the simulation's detectors."""

    number: int
    family: int
    definition: BlockDefinition
    corner: list[int]
    mask: np.ndarray
    detector: int
    wall: int
    momentum: list[int]
    drive: list[int] = field(default_factory=lambda: [0, 0, 0])
    count: int = 0
    previous_sum: int = 0
    own: LiveRecord | None = None
    emitted: list[int] = field(default_factory=list)
    current: int | None = None
    births: int = 0
    hop: tuple[int, int, int] = (0, 0, 0)
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

    def escaped_amount(self, family: int) -> int:
        return self.transit_escaped[family]

    def escaped_content(self, family: int) -> int:
        return self.transit_escaped[family]

    def escaped_momentum(self, family: int) -> list[int]:
        return [0, 0, 0]


class DetectorLawLayer:
    """The record's lines the runner writes into run.json (the amplitude law's shape)."""

    def __init__(self) -> None:
        self.gathers: list[dict[str, object]] = []
        self.born = 0
        self.gathered = 0

    def open_records(self) -> list[dict[str, object]]:
        return []

    def report(self) -> dict[str, object]:
        return {"law": DETECTOR_LAW_RULE, "born": self.born, "gathered": self.gathered, "open": 0}


class DetectorLawSimulation:
    """One world under the local detector law, stepped interval by interval."""

    def __init__(self, world: NatureBeamWorld, observer: Record | None = None) -> None:
        if not world.detector_law:
            raise ValueError(f"{BEAM_LAW}: the world does not declare detector_law")
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
                    f"{BEAM_LAW}: measured[{number}].table is refused under {DETECTOR_LAW_RULE}: the "
                    "tables (the polariser's two detectors at one Node, the splitter's linear form) "
                    "retired with the flux reading (the born pair on the circle; BUILD.md section 26 item 17); a polariser is "
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
        # Node. M changes only at the law's events (a birth, a click, a
        # step of a body), so the array is rebuilt from the held books as
        # each interval begins (`_refresh_node_content`) and after a birth.
        self.node_clock = int(world.node_clock)
        if self.node_clock < 1:
            raise ValueError(
                f"{BEAM_LAW}: the world declares no Node clock (`node_clock`, Gamma from 1; "
                "ALGEBRA.md 9.35 (3); BUILD.md section 26 item 31)"
            )
        # THE FAMILY OF CLICKS (the model owner's record 1982; ALGEBRA.md 9.41,
        # 9.44 (3), 9.45; BUILD.md section 26 item 32): the fourth family,
        # whose level c at a Node IS the Node clock (Gamma, Gamma + c); one
        # record of it over the board (`clock_record`), its level held at
        # every body's Nodes at the body's content (both levels, the
        # remainder 0, not the step's own there), written at the load and at
        # every click; elsewhere it moves by its own plain step after the
        # other families' (so the joint step inverts); no residue, no ladder,
        # no click of its own, never booked. `node_content` is its level as
        # every other family's step reads it: the static M of decision (5)
        # was its value at a body's own Nodes.
        if world.clock_family is None:
            raise ValueError(
                f"{BEAM_LAW}: the world declares no family of clicks (`clock_family`; ALGEBRA.md "
                "9.45; BUILD.md section 26 item 32)"
            )
        self.clock_family = int(world.clock_family)
        self.node_content = np.zeros(self.shape, dtype=np.int64)
        # THE FAMILY OF CHARGE (the model owner's decision of 2026-09-25;
        # ALGEBRA.md 9.48; BUILD.md section 26 item 35): the fifth family, on
        # the scaffold of the family of clicks: one record over the board
        # (`charge_record`), its level held at every body's Nodes at the
        # body's signed charge Q (the sum of the signs of the quanta it
        # holds, `_body_charge`), elsewhere its own plain step; a record of
        # charge q reads at every Node the effective content c - q Lambda d
        # in place of c, the sign opposite to its own (a hill beside a body
        # of its own sign, a well beside the other sign; light, q = 0, reads
        # the content alone), Lambda the world's `charge_strength`
        if world.charge_family is None:
            raise ValueError(
                f"{BEAM_LAW}: the world declares no family of charge (`charge_family`; ALGEBRA.md "
                "9.48; BUILD.md section 26 item 35)"
            )
        self.charge_family = int(world.charge_family)
        self.charge_strength = int(world.charge_strength)
        self.family_charge = [int(family.charge[0]) for family in world.families]
        self.node_charge = np.zeros(self.shape, dtype=np.int64)
        self.span_masks: dict[int, np.ndarray] = {}
        for number, entry in enumerate(world.measured):
            if entry.block is None:
                span = np.zeros(self.shape, dtype=bool)
                for node in self._span_nodes(entry.position, entry.span):
                    span[node] = True
                self.span_masks[number] = span
        self.records: dict[int, LiveRecord] = {}
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
        self.kind_num: list[np.ndarray] = [
            np.full(self.shape, family.pair[0], dtype=np.int64) for family in world.families
        ]
        self.kind_den: list[np.ndarray] = [
            np.full(self.shape, family.pair[1], dtype=np.int64) for family in world.families
        ]
        self.kind_wrap: list[tuple[bool, bool, bool]] = [
            world.kind_periodic(index) for index in range(len(world.families))
        ]
        # The blocks (massive-record-v1): every measured event with a block,
        # its Nodes written into its kind's pair arrays, its own record
        # seeded on its Nodes, its momentum and the drive's wall 3 Q S M.
        for number, entry in enumerate(world.measured):
            if entry.block is None:
                continue
            definition = entry.block
            corner = [int(entry.position[axis]) for axis in range(3)]
            mask = self._box(corner, definition.extents, entry.family)
            wall = 3 * LABEL_SCALE * world.width * entry.amount
            block = Block(
                number,
                entry.family,
                definition,
                corner,
                mask,
                int(self.detector_at_node[tuple(entry.position)]),
                wall,
                [int(component) for component in entry.momentum],
            )
            self._write_pair(block)
            if definition.seed > 0:
                own_record = self._massive_record(number * (1 << 32), number, entry.family)
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
                    f"{BEAM_LAW}: measured[{block.number}].receiver {name!r} names no detector of the "
                    f"simulation (the detectors: {self.detector_names})"
                )
            self.receiver_detector[block.number] = self.detector_names.index(name)
        self.has_receiver = bool(self.receiver_detector)
        # the family of clicks' record: the load's write, the content held at
        # every body's Nodes and 0 elsewhere (ALGEBRA.md 9.45 (2))
        self.clock_record = LiveRecord(
            -1,
            -1,
            self.clock_family,
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
        )
        # the family of charge's record: the load's write, the signed charge
        # held at every body's Nodes and 0 elsewhere (ALGEBRA.md 9.48 (2))
        self.charge_record = LiveRecord(
            -2,
            -2,
            self.charge_family,
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
        )
        self._hold_clock()

    # The Node clock as the family of clicks (ALGEBRA.md 9.35 (2), 9.45; BUILD.md
    # section 26 items 31 and 32)

    def _hold_clock(self) -> None:
        """THE HOLD (ALGEBRA.md 9.45 (2)): at every body's Nodes the family of
        clicks' level is the body's content, the held quanta of every family
        (a block's Nodes as they stand this interval, a measured event's
        span), written whole at both levels with the remainder 0: the one
        place where a family's level is not the step's own, the same write as
        the load's, at the load and at every click (up by one at a taking,
        down by one at a giving). `node_content` is then the level every
        other family's step reads at the Node. THE FAMILY OF CHARGE is held
        the same way at the body's signed charge Q (ALGEBRA.md 9.48 (1) and
        (2); item 35), `node_charge` its level."""
        clock = self.clock_record
        charge = self.charge_record
        for number in range(len(self.held)):
            quanta = sum(self.held[number])
            signed = self._body_charge(number)
            block = self.block_by_number.get(number)
            mask = block.mask if block is not None else self.span_masks[number]
            clock.now[mask] = quanta
            clock.before[mask] = quanta
            clock.remainder[mask] = 0
            charge.now[mask] = signed
            charge.before[mask] = signed
            charge.remainder[mask] = 0
        self.node_content = clock.now
        self.node_charge = charge.now

    def _advance_clock(self) -> None:
        """The family of clicks' own step and the family of charge's, after every
        other family's (ALGEBRA.md 9.45 (2), 9.48 (2)): the plain step of the
        pair [1, 1] at every Node (the pace 1 for its own level: a field
        family reads no other family and not itself), then the hold at the
        bodies' Nodes; the joint step inverts (`step_inverse`).
        THE GUARD: the pace Gamma - c stays positive at every Node and the
        level above -Gamma (|c| below Gamma, the loader's bound on twice the
        world's content); the run is refused where it does not."""
        self._advance(self.clock_record)
        self._advance(self.charge_record)
        self._hold_clock()
        # the pace Gamma - c + q Lambda d of every family's reads stays
        # positive (ALGEBRA.md 9.45 (3), 9.48 (3); items 34 and 35)
        for sign in sorted(set(self.family_charge)):
            most = int(
                np.max(np.abs(self.node_content - sign * self.charge_strength * self.node_charge))
            )
            if most >= self.node_clock:
                raise RuntimeError(
                    f"{BEAM_LAW}: the effective content c - q Lambda d for the charge q = {sign} "
                    f"reached {most} in size at interval {self.tick}, at or beyond Gamma = "
                    f"{self.node_clock}: the pace Gamma - c + q Lambda d of every read stays "
                    "positive under the fixed wall (ALGEBRA.md 9.45 (3), 9.48 (3); BUILD.md "
                    "section 26 items 34 and 35); the run is refused"
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

    def wheel_at(self, family: int, node: tuple[int, ...]) -> tuple[int, int]:
        """The remainder's step g and the wheel W of the family's rule at a
        Node under the fixed wall (ALGEBRA.md 9.22 (4), 9.50 (8) and (13);
        BUILD.md section 26 items 34 and 36): the wall 3 den Gamma, the step
        g the gcd of the total's coefficients (p_i num on the six reads, 6
        den c_i at the Node and the wall itself: the remainder moves on the
        multiples of g), W = wall / g values; the pair's own 3 den / gcd(num, 3 den) in
        the vacuum (2403 on [800, 801]), content-dependent at and beside a
        body; read from the rule, never declared."""
        num = int(self.kind_num[family][node])
        den = int(self.kind_den[family][node])
        gamma = self.node_clock
        wall = 3 * den * gamma
        effective = self._effective_content(family)
        content = int(effective[node])
        # the pace on the Node's own sum (item 36): the coefficients p_i num
        # on the six reads, 6 den c_i at the Node and the wall
        step = gcd(wall, 6 * den * content, num * (gamma - content))
        return step, wall // step

    def node_clock_pair(self, node: tuple[int, ...], family: int) -> tuple[int, int]:
        """The clock pair a record of `family` reads at a Node under the fixed
        wall (items 34 and 35): (e, f) = (Gamma - c + q Lambda d, Gamma), the
        pace over the wall's Gamma; f - e the effective content there."""
        return self.node_clock - int(self._effective_content(family)[node]), self.node_clock

    def _effective_content(self, family: int) -> np.ndarray:
        """THE READING WITH ONE SIGN (ALGEBRA.md 9.48 (3); BUILD.md section 26
        item 35): the content a record of `family` reads at every Node, c -
        q Lambda d, the family of clicks' level less the family's charge q
        times the strength times the family of charge's level; the content
        alone for q = 0 (light)."""
        sign = self.family_charge[family]
        if sign == 0:
            return self.node_content
        return self.node_content - sign * self.charge_strength * self.node_charge

    def _body_charge(self, number: int) -> int:
        """A body's charge Q (ALGEBRA.md 9.48 (1)): the sum of the signs of the
        quanta it holds, an integer of either sign, moved with the labels at
        the clicks (the held books)."""
        return sum(
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

    def _write_pair(self, block: Block) -> None:
        """The block's pair written on its Nodes into its kind's arrays; the
        kind's own pair elsewhere on the Nodes the block left."""
        family = self.families[block.family]
        num = self.kind_num[block.family]
        num[~block.mask] = family.pair[0]
        den_all = self.kind_den[block.family]
        den_all[~block.mask] = family.pair[1]
        den = self.kind_den[block.family]
        num[block.mask] = block.definition.pair[0]
        den[block.mask] = block.definition.pair[1]
        for other in self.blocks:
            if other is not block and other.family == block.family:
                num[other.mask & ~block.mask] = other.definition.pair[0]
                den[other.mask & ~block.mask] = other.definition.pair[1]

    def _massive_record(self, identity: int, number: int, family: int) -> LiveRecord:
        """A record of the massive kind on the board: a block's own record or
        its response to a light record; no train, no clock, no Ports."""
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
        )

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
        accumulator gains the momentum's component against the wall 3 Q S M
        (verb T, then D with the remainder kept, at most one Link per
        interval, `core.integer.by_drive`), x before y before z, a second
        Link in one interval lost to the earlier axis (its wall subtracted,
        the frame's tie); the Nodes and the pair region translate by T; the
        records' rows stay on their Nodes (12.7 (d))."""
        momentum = self._momentum_now(block)
        hop = [0, 0, 0]
        stepped = False
        for axis in range(3):
            count, block.drive[axis] = by_drive(block.drive[axis], momentum[axis], block.wall, at_most=1)
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
        if int(np.count_nonzero(block.mask)) < int(np.count_nonzero(old_mask)):
            # Reviewer 3's line from the redshift dry run (the Boss's 09:45Z): a
            # stepping block whose Nodes would leave the board by a zero face
            # (the cube cut by `_cube` on a non-periodic axis) refuses the
            # interval naming the block, instead of running on with the block
            # gone and the books balanced; the margin rule refuses the same
            # block at load, not at a hop, so this is the run's own check.
            raise RuntimeError(
                f"{BEAM_LAW}: measured[{block.number}] stepped off the board at interval "
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
                f"{BEAM_LAW}: measured[{block.number}] has no shell (no Node of it has a Port to "
                "a Node outside it), so no Node reads its residue (ALGEBRA.md 9.44 (5) (c))"
            )
        return int(where[0][0]), int(where[1][0]), int(where[2][0])

    def residue_of(self, live: LiveRecord, block: Block) -> tuple[int, int]:
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
        node = self.first_shell_node(block)
        step, wheel = self.wheel_at(live.family, node)
        return int(live.remainder[node]) // step, wheel

    def _excite(self, block: Block, own_record: LiveRecord) -> None:
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
            # births (at the engine's construction: the generator parses the
            # world with the scalar seed to compute the profile)
            raise ValueError(
                f"{BEAM_LAW}: measured[{block.number}].emitter needs the body's `seed` as its "
                "composed mode's profile (one integer per Node, the generator's "
                "`seed_on_the_mode`; a flat scalar seed is no mode and births nothing lawful, "
                "ALGEBRA.md 9.17 (4) item 1)"
            )
        if emitter.train is None or emitter.born is None:
            raise ValueError(
                f"{BEAM_LAW}: measured[{block.number}].emitter declares no born train: `train` "
                "(the direction and the periods) with `born` (the train's two levels over the "
                "body's Nodes and its norm on the vacuum), the generator's integers (ALGEBRA.md "
                "9.17 (6a); `born_train` of the massive record generator; no table in the engine)"
            )
        if emitter.norm is None:
            raise ValueError(
                f"{BEAM_LAW}: measured[{block.number}].emitter declares no `norm`: one period's "
                "action of the body's mode, its conserved form's share at the centre Node summed "
                "over the period, the generator's integer (ALGEBRA.md 9.17 (7) (e) and (f), 9.19 "
                "(3); `excite_on_the_mode` of the massive record generator)"
            )
        if emitter.period is None:
            raise ValueError(
                f"{BEAM_LAW}: measured[{block.number}].emitter declares no `period`: P, the "
                "nearest integer to 2 pi / omega_b of the body's mode, the generator's integer "
                "(ALGEBRA.md 9.17 (7) (f), 9.44 (5) (c): the tick counts intervals against "
                "(2 u + 1) P / (2 W))"
            )
        block.excitations += 1
        block.residue_pending = True
        own_record.norm = emitter.norm
        block.wait = 0
        block.emit_now = False

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
        own = block.own
        emitter = block.definition.emitter
        if own is None or emitter is None or block.emit_now:
            return
        if self.held[block.number][block.family] <= 0:
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
        """The click of the body's own record and the birth (ALGEBRA.md 9.17 (4)
        items 1 to 3, (5) items 2 to 4 and (6); 9.43 (3): the giving end sets
        the born rows, lowers the stock and the content, and LEAVES THE
        BODY'S OWN LEVELS, PHASE AND REMAINDERS AS THEY ARE, the step alone
        carrying the standing record between its clicks; no X on the own
        record, no reseed: the reseed of 9.17 (4) item 1 and the remainder
        kept through it, items 29 and 30, HISTORY). E^T writes the born
        record ONCE at both
        of the body (the generator's now = A C_2N[3 N / 2 + s] on the circle
        of 2 N steps with s = floor(n / d) the born clock's step and before =
        -now, the character half a step either side of its zero, no static
        part, A the amplitude unit; no table in the engine); the
        norm T the record's conserved form (9.19 (3)), its residue and
        wheel from the law (9.22 (4), 9.44 (5) (c): the body's own remainder
        at the first shell Node in the declared order, read at the click,
        the born record's residue and the next excitation's alike: every
        Node of the body holds (M, u)), the content one quantum moved from
        the body's stock; the count of intervals to the next click starts
        here (`_excitation_rung`). Nothing drives the born record
        afterwards: the law advances it."""
        world = self.world
        emitter = block.definition.emitter
        own = block.own
        assert emitter is not None and own is not None
        number = block.number
        family = emitter.family
        definition = self.families[family]
        assert definition.phase_per_age is not None
        numerator, denominator = definition.phase_per_age
        steps = world.phase_steps
        period = (steps * denominator + numerator - 1) // numerator
        cost = definition.quantum
        excitation = block.excitations
        # the born record's residue and wheel from the law (9.22 (4), 9.44 (5)
        # (c)): the body's own remainder at its first shell Node in the
        # declared order, read at the click on the body's wheel there
        residue, wheel = self.residue_of(own, block)
        wait = block.wait
        read_node = self.first_shell_node(block)
        # the family of clicks' level at the read Node and at its reads as the
        # wheel was read, before the birth lowers the content (item 34; GAMEBOARD)
        read_clocks = [
            int(self.node_content[read_node]),
            [
                int(self.node_content[j])
                for j in self._neighbour_nodes(read_node, self.kind_wrap[block.family])
            ],
        ]
        # the body's clock pair as the clicking record was advanced (the
        # content at its centre Node; GAMEBOARD, on the birth line)
        centre = tuple(int(axis[0]) for axis in np.nonzero(self.centre_mask(block)))
        clock_pair = self.node_clock_pair(centre, block.family)
        # the content and the charge the clicking record was advanced under
        # (before this birth lowers them; item 35's line reads them here,
        # the pair no longer the content alone for a charged family)
        centre_content = int(self.node_content[centre])
        body_charge = self._body_charge(number)
        # the body's own record is not ended and never rewritten (9.43 (3))
        block.births += 1
        identity = number * (1 << 32) + block.births
        live = LiveRecord(
            identity,
            number,
            family,
            residue,
            block.births,
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
        )
        # E^T: the born clock's character on the body's Nodes, written once at
        # both levels, every Node at the vertex's phase (the one-Node broadband
        # birth; a line's travelling character, the per-Link pair of ALGEBRA.md
        # 9.17 (4) item 2, is owed until that pair is declared)
        # NO TABLE IN THE ENGINE (the cleanup order's step 2; ALGEBRA.md 9.17
        # (6), 9.22 (2)): the born pair is the world's two integers `born:
        # [now, before]`, the generator's, checked at load (before = -now),
        # written on every Node of the body
        # THE BORN TRAIN (ALGEBRA.md 9.17 (6a); BUILD.md section 26 item 27):
        # the train's two levels written on the body's Nodes in the box's
        # x-major order (`body_node_indices`, the loader's and the generator's
        # one convention), the norm T the written one (the conserved form on
        # the born family's vacuum, the generator's integer checked at load)
        assert emitter.born is not None
        self.write_levels(live, block, emitter.born.now, emitter.born.before)
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
        self.held[number][block.family] -= 1
        self.ledger.held_spent[block.family] += 1
        # THE NORM UNDER THE NODE CLOCK (BUILD.md section 26 items 31 and
        # 36; ALGEBRA.md 9.50 (13)): the born record's T is p times its
        # conserved form as written on the board, the engine's own integer
        # with the content at the body's Nodes as the birth leaves it (one
        # quantum fewer: the pace p the record is advanced at from the next
        # interval): the form the plain flux booking sums to over the
        # record's passage (the share's identity, `form_share`), read on
        # the ladder as T / p
        self._hold_clock()
        live.norm, live.pace = self.born_norm(live)
        self.ledger.transit_released[family] += cost
        block.emitted.append(identity)
        self.records[identity] = live
        self.layer.born += 1
        if self.record is not None:
            self.record(
                {
                    "event": "birth",
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
                    # the norm's denominator (item 36): the born record's
                    # form is norm / pace, whole in the body's own units at
                    # the body's level as written
                    "pace": live.pace,
                    # the file's vacuum norm (p times it the born record's T
                    # in the vacuum) and the body's content and clock pair
                    # as the clicking record was advanced (GAMEBOARD; item 31)
                    "born_norm": emitter.born.norm,
                    "content": centre_content,
                    "charge": body_charge,
                    "node_clock": list(clock_pair),
                    "nodes": int(np.sum(block.mask)),
                    "cycle": block.count,
                    **({"clock": block.count} if world.clock_stamp else {}),
                }
            )
        # THE NEXT EXCITATION while the stock lasts (9.43 (3), 9.44 (5) (c)):
        # the body's own record continues as it is, its levels, phase and
        # remainders untouched by the click; the residue read at this click
        # at the first shell Node is the born record's and the next
        # excitation's alike (every Node of the body holds (M, u)); the count
        # of intervals starts from this click (`_excitation_rung`)
        block.emit_now = False
        block.wait = 0
        own.u, own.wheel = residue, wheel
        if self.held[number][block.family] > 0:
            block.excitations += 1

    def _block_clock(self, block: Block) -> None:
        """The block's clock (MASSIVE_RECORD.md sections 4 and 6): its total
        record summed across its Nodes (G over R: its own record), one
        count per cycle (the sum's crossing
        from at most 0 to above 0, verb D's comparison), a `click` line per
        count with its own count (the self-click of row (g)); a new cycle
        births its emission at the next interval."""
        total = 0
        # the co-moving centre Node (the design's reading of the clock in
        # motion, MASSIVE_RECORD.md section 8: "the clock read at the
        # co-moving centre"): the total record's value there, on the line
        centre = tuple(
            (block.corner[axis] + block.definition.extents[axis] // 2) % self.shape[axis]
            for axis in range(3)
        )
        at_centre = 0
        if block.own is not None:
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
                        "record": None if block.own is None else block.own.identity,
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
        `step_inverse`)."""
        num = self.kind_num[live.family]
        den = self.kind_den[live.family]
        field = live is self.clock_record or live is self.charge_record
        gamma = 1 if field else self.node_clock
        content = 0 if field else self._effective_content(live.family)
        wall = 3 * den * gamma
        # the same integers as the forward step's: the pace on the Node's own
        # sum (item 36)
        total = num * (gamma - content) * self._neighbours(live.before, self.kind_wrap[live.family])
        total += 6 * den * content * live.before
        total -= wall * live.now + live.remainder
        a_before = -np.floor_divide(-total, wall)
        live.remainder = wall * a_before - total
        live.now = live.before
        live.before = a_before
        live.age -= 1

    def step_inverse(self) -> None:
        """One interval backwards (8.8), in the reverse column order of `step`:
        the light records first, then the bodies' own records (the coupling
        HISTORY, the model owner's decision (2) of record 1962: no source, no
        receive, every record by the rule alone); no push, no click, no birth
        (the bodies at rest and no click in the interval, the property test's
        world)."""
        for block in self.blocks:
            if any(int(component) != 0 for component in block.momentum):
                raise ValueError(
                    f"{BEAM_LAW}: the inverse map is defined at rest (block {block.number} moves)"
                )
        # the joint inverse (ALGEBRA.md 9.41 (2), 9.45 (2)): every family backward
        # at the family of clicks' level of the interval's start (its `before`
        # level: the clock stepped last), then the clock backward and its hold
        self.node_content = self.clock_record.before
        self.node_charge = self.charge_record.before
        for identity in list(self.records):
            live = self.records[identity]
            if self.families[live.family].massive_kind and live.emitter is None:
                continue
            self._advance_inverse(live)
        for block in self.blocks:
            if block.own is not None:
                self._advance_inverse(block.own)
        self._advance_inverse(self.clock_record)
        self._advance_inverse(self.charge_record)
        self._hold_clock()
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

    # The flux reading (ALGEBRA.md 9.19 (3), the mathematician's derivation
    # of 2026-09-24 from 8.2; BUILD.md section 26 item 13): the flux into a
    # Node i from a read j of it, 3 G_ij = A_ij (now_i before_j - before_i
    # now_j), a bilinear form of the record's own two levels at the two ends
    # of a Link, pair-free and antisymmetric; a receiver's offer the one-way
    # inward flux through its Ports, summed over intervals; the record's
    # norm its conserved form I. Both in the integers 3 G x wall and 3 I x
    # wall, wall the family's common wall (the least common multiple of its
    # pairs' numerators over the board).

    def kind_wall(self, family: int) -> int:
        """The family's common wall: the least common multiple of the
        numerators of its pair over the board (the vacuum's and every body's),
        so that wall x den_i / num_i is an integer at every Node."""
        wall = 1
        for value in np.unique(self.kind_num[family]).tolist():
            value = int(value)
            wall = wall * value // gcd(wall, value)
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
        for axis, side, mask in self._flux_ports(family):
            across = self._shift(flat, axis, -side, fill=-1, wrap=wrap)
            where = mask & (across >= 0)
            nodes.append(flat[where])
            neighbours.append(across[where])
        port_i = np.concatenate(nodes) if nodes else np.zeros(0, dtype=np.int64)
        port_j = np.concatenate(neighbours) if neighbours else np.zeros(0, dtype=np.int64)
        port_detector = self.detector_at_node.ravel()[port_i]
        pairs = (port_i, port_j, port_detector)
        self._inflow_port_pairs[family] = pairs
        return pairs

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
        offers: dict[int, int] = {}
        for value, detector in zip(flux.tolist(), port_detector.tolist(), strict=True):
            if value > 0:
                offers[detector] = offers.get(detector, 0) + int(value) * wall
        return offers

    def inward_flux(self, live: LiveRecord, mask: np.ndarray) -> int:
        """The one-way inward flux into the Nodes of `mask` through the Links
        from Nodes outside it (9.19 (3)): 3 G_ij = now_i before_j - before_i
        now_j where positive, times the family's wall (the form's units; the
        current unweighted, item 36), from the record's two levels
        after the interval's step (`now`, `before`; the prototype's
        reading, board_algebra.py)."""
        wrap = self.kind_wrap[live.family]
        wall = self.kind_wall(live.family)
        level_now, level_before = live.now, live.before
        now = level_now.astype(object)
        before = level_before.astype(object)
        total = 0
        for axis in range(3):
            if self.shape[axis] == 1:
                continue
            for side in (1, -1):
                outside = ~self._shift(mask, axis, -side, fill=False, wrap=wrap)
                present = self._shift(
                    np.ones(self.shape, dtype=bool), axis, -side, fill=False, wrap=wrap
                )
                port = mask & outside & present
                if not port.any():
                    continue
                now_j = self._shift(level_now, axis, -side, wrap=wrap).astype(object)
                before_j = self._shift(level_before, axis, -side, wrap=wrap).astype(object)
                flux = now * before_j - before * now_j
                total += int(np.sum(np.where(port & (flux > 0), flux, 0)))
        return total * wall

    def write_levels(
        self, live: LiveRecord, block: Block, now: Sequence[int], before: Sequence[int]
    ) -> None:
        """The two levels written on the block's Nodes in the box's x-major
        order (`body_node_indices` on the block's current corner and its
        family's faces), the one convention of the loader, the generator and
        the engine (ALGEBRA.md 9.17 (6a))."""
        nodes = body_node_indices(
            (int(self.shape[0]), int(self.shape[1]), int(self.shape[2])),
            (int(block.corner[0]), int(block.corner[1]), int(block.corner[2])),
            block.definition.extents,
            self.kind_wrap[block.family],
        )
        flat_now = live.now.reshape(-1)
        flat_before = live.before.reshape(-1)
        for index, now_value, before_value in zip(nodes, now, before, strict=True):
            flat_now[index] = now_value
            flat_before[index] = before_value

    def planted_record(
        self, family: int, now: np.ndarray, before: np.ndarray, norm: int = 0
    ) -> LiveRecord:
        """A record of the family given to the rule directly, its two levels
        as given and its remainder 0 (the generator's checks of the born
        train, ALGEBRA.md 9.17 (6a) and 9.22 (7a) (iv), and the tests'
        device): registered in no ledger, advanced by `_advance` and read by
        `inward_flux` and `conserved_form` alone; `norm` its T where given."""
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
        )

    def conserved_form(self, live: LiveRecord) -> Fraction:
        """The record's conserved form I (ALGEBRA.md 8.2; under the Node's own
        pace, 9.50 (9) and (13); BUILD.md section 26 item 36) in the form's
        units, 3 I x wall in the vacuum: over the Nodes [3 wall (den_i /
        num_i) Gamma (now_i^2 + before_i^2) - 6 wall (den_i / num_i) c_i
        now_i before_i] / p_i - wall now_i SUM_j before_j, p_i = Gamma - c_i
        (+ q Lambda d_i) the pace at the Node, the six reads with the
        family's faces (the folded axes' self-reads); the sum of every Node's
        share (`form_share`), an exact rational (the Killing energy: each
        Node's share read in the world's time by its own pace; whole in the
        body's own units, p times it, at a uniform level, `born_norm`)."""
        return self.form_share(live, np.ones(self.shape, dtype=bool))

    def form_share(self, live: LiveRecord, mask: np.ndarray) -> Fraction:
        """The Nodes' share e of the record's conserved form (ALGEBRA.md 9.17
        (7) (e), 9.19 (3), 9.50 (9)) on the Nodes of `mask`, in the form's
        units: a bilinear form of the record's two levels at the Node, its
        six reads and the pace at the Node (verb B, local), the Node's terms
        weighted by 1 / p_i; its change over an interval is the sum of the
        plain currents through the Node's Links plus the remainders' term,
        so a bound mode's share is constant where nothing flows."""
        family = live.family
        wall = self.kind_wall(family)
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
        field = live is self.clock_record or live is self.charge_record
        gamma = 1 if field else self.node_clock
        content = (
            np.zeros(self.shape, dtype=object)
            if field
            else self._effective_content(live.family).astype(object)
        )
        pace = gamma - content
        weight = (3 * wall * self.kind_den[family] // self.kind_num[family]).astype(object)
        now = live.now.astype(object)
        before = live.before.astype(object)
        read = self._neighbours(live.before, self.kind_wrap[family]).astype(object)
        node = weight * (gamma * (now * now + before * before) - 2 * content * now * before)
        links = wall * now * read
        return self._weighted_sum(node, pace, mask) - int(np.sum(links[mask]))

    @staticmethod
    def _weighted_sum(node: np.ndarray, pace: np.ndarray, mask: np.ndarray) -> Fraction:
        """SUM_i node_i / pace_i over the Nodes of `mask`, exact (one Fraction
        per distinct pace: the paces present are few, the body's and the
        field's levels)."""
        total = Fraction(0)
        chosen = pace[mask]
        values = node[mask]
        for value in set(int(v) for v in chosen.tolist()):
            total += Fraction(int(np.sum(values[chosen == value])), value)
        return total

    def born_norm(self, live: LiveRecord) -> tuple[int, int]:
        """THE NORM AS THE EXACT RATIONAL (ALGEBRA.md 9.46 (1), 9.50 (9) and
        (13); BUILD.md section 26 item 36): the born record's conserved form
        Q, the Node's terms weighted by 1 / p_i, as the pair (numerator,
        denominator) in lowest terms, the record's `norm` and `pace`; the
        ladder reads the plain flux C against Q, 2 W pace C against (2 u +
        1) norm, in integers. For a record written at one level (a body's
        Nodes at rest, the content and the charge uniform there) p Q is
        whole, the integer T of 9.46 (1) in the body's own units, and the
        pair reduces from (p Q, p); a record written across levels (a moving
        body's Nodes as the hold leaves them) has a rational Q, its world
        energy, and the same reading."""
        form = self.conserved_form(live)
        return form.numerator, form.denominator

    def _half_space(self, origin: Address3, vector: Vector) -> np.ndarray:
        """The Nodes on the arm's side of the lamp: (node - origin) . vector at
        least 0 on the board's raw coordinates (the arm's own half-space, the
        lamp's Node included; the pair's two arms on a bar the two half-lines)."""
        grids = np.indices(self.shape, dtype=np.int64)
        dot = np.zeros(self.shape, dtype=np.int64)
        for axis in range(3):
            dot += (grids[axis] - int(origin[axis])) * int(vector[axis])
        mask: np.ndarray = dot >= 0
        return mask

    def _advance(self, live: LiveRecord) -> None:
        # THE EMITTER'S NODES ARE NODES LIKE EVERY OTHER (ALGEBRA.md 9.17; the
        # Boss's line of 2026-09-24 on the knot): no grace, no exemption, no
        # own take, no fresh Port; the born record is written once and the
        # law advances it (the retired forms in BUILD.md section 26).
        # Every born record, light's kind or a massive kind alike, books its
        # flux at the Nodes and clicks on its ladder (the click is the law's
        # one action on any record, POSTULATES 10); a BLOCK'S own record (a
        # massive kind, born of no emitter) books nothing and is on no
        # ladder (massive-record-v1, MUST 2).
        field = live is self.clock_record or live is self.charge_record
        booked = not field and (not self.families[live.family].massive_kind or live.emitter is not None)
        # The rule with the kind's pair on the six-neighbour term
        # (massive-record-v1, MASSIVE_RECORD.md section 1): G over the six
        # neighbours, then D by 3 den with the remainder kept, then T; at
        # light's pair [1, 1] the first build's integers bit for bit.
        num = self.kind_num[live.family]
        den = self.kind_den[live.family]
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
        wall = 3 * den * gamma
        # THE NODE'S OWN PACE (the model owner's ruling of record 2003, "take
        # only from the current Node, not from the neighbours"; ALGEBRA.md
        # 9.50 (13); BUILD.md section 26 item 36): the pace p_i = Gamma - c_i
        # (+ q Lambda d_i) multiplies the Node's own six-neighbour sum, the
        # reads plain as S_6 reads them: 3 den Gamma a_next + r' = p_i num
        # S_6(a_now)_i + 6 den c_i a_now - 3 den Gamma a_before + r; the
        # Node steps the vacuum's rule at its own pace (the pace on each
        # read's far end, form (B) of item 34, HISTORY)
        neighbours = self._neighbours(live.now, self.kind_wrap[live.family])
        total = num * (gamma - content) * neighbours
        total += 6 * den * content * live.now
        total -= wall * live.before
        total += live.remainder
        nxt = np.floor_divide(total, wall)
        live.remainder = total - wall * nxt
        if self.world.massive_record and int(np.max(np.abs(nxt))) > self.world.amplitude_bound:
            raise RuntimeError(
                f"{BEAM_LAW}: the record {live.identity} reached the level "
                f"{int(np.max(np.abs(nxt)))} at interval {self.tick}, above the world's declared "
                f"amplitude bound A = {self.world.amplitude_bound} (issue #1085; MUST 3's bound "
                "holds only below A): the run is refused"
            )
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
        self._ladder_click(live, increments)

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
        """THE INCREMENT LADDER (ALGEBRA.md 9.25 (2), the mathematician's word
        of 2026-09-25 on the finding of BUILD.md section 26 item 14; the
        cumulative sums of 9.19 (3) (b) withdrawn): the record's threshold
        theta = (2 u + 1) T / (2 W) is fixed at its birth (u its residue, T
        its norm, W its own wheel); at every interval the record's running
        total C gains this interval's one-way flux into the detectors of its
        ladder, the detectors in the ladder's declared order (the named sets in
        the named order, the face last); the click fires at the first
        interval at which C crosses theta, at the detector whose segment of that
        interval's increment, laid out in the ladder's order, holds theta
        (the walk: the detector k at which 2 W (C + f_1 + ... + f_k) >= (2 u + 1)
        T first). Born's rule is its theorem (9.25 (3): the detector's share of
        the record's total inward flux, whatever the time profile). A detector is
        a detector's whole cube (record 1899): its increment the flux into
        the cube through its Ports from outside, the click the detector's,
        named on the line and never placed at a Node. The click line, the
        content handed to the set's body, the record deleted whole after the
        interval's advances (8.8's one deletion, record 1888). A set bound to
        a block stamps the line with the block's count as the interval
        began."""
        if live.clicked or live.norm <= 0:
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

    def record_form(self, live: LiveRecord) -> Fraction:
        """The conserved form I of the record (MASSIVE_RECORD.md section 3, a
        GAMEBOARD diagnostic read by the books): the invariant of the rule
        written as a_next + a_before = D^-1 (S_6 / 3) with D_x = den_x /
        num_x, I = a_next . D a_next + a_now . D a_now - a_next . (S_6 / 3)
        a_now, scaled by 3 L to integers: 3 den_x (L / num_x) (a_now^2 +
        a_before^2) summed over the Nodes less L (a_now,i a_before,j +
        a_now,j a_before,i) summed over the Links, L the least common
        multiple of the distinct numerators (at one numerator L = num and
        the form is section 3's line, 3 den (a^2 + b^2) less num over the
        Links). Verb B with the declared matrix and G; conserved by the
        rule up to the remainders' bounded jitter; positive definite for
        den > num."""
        num = self.kind_num[live.family]
        den = self.kind_den[live.family]
        distinct = [int(value) for value in np.unique(num)]
        common = 1
        for value in distinct:
            common = common * value // gcd(common, value)
        scale = np.floor_divide(common, num)
        now = live.now.astype(object)
        before = live.before.astype(object)
        # THE WEIGHTS UNDER THE NODE'S OWN PACE (ALGEBRA.md 9.50 (9) and
        # (13); BUILD.md section 26 item 36), the plain form in the vacuum:
        # with the pace p_i, [3 den_i (L / num_i) Gamma (a^2 + b^2) - 6 den_i
        # (L / num_i) c_i a b] / p_i at the Node, L on the Link ij, plain; an
        # exact rational (the weights p_i p_j at one integer scale, item 34,
        # HISTORY); the family of clicks' own form plain (its pace 1)
        field = live is self.clock_record or live is self.charge_record
        gamma = 1 if field else self.node_clock
        content = (
            np.zeros(self.shape, dtype=object)
            if field
            else self._effective_content(live.family).astype(object)
        )
        pace = gamma - content
        weight = (3 * den * scale).astype(object)
        node = weight * (gamma * (now * now + before * before) - 2 * content * now * before)
        squares = self._weighted_sum(node, pace, np.ones(self.shape, dtype=bool))
        links = 0
        wrap = self.kind_wrap[live.family]
        for axis in range(3):
            # Each Link once: the Node and its neighbour on the + side (the
            # wrap on a periodic axis closes the last Link, an open face
            # has none); an axis of one layer reads the row itself as its
            # two neighbours (DESIGN.md section 2), two self-Links the form
            # carries (the roll on a length-one axis is the identity).
            if wrap[axis] or self.shape[axis] == 1:
                now_next = np.roll(now, -1, axis=axis)
                before_next = np.roll(before, -1, axis=axis)
                links += int(np.sum(common * (now * before_next + now_next * before)))
            else:
                lower = [slice(None)] * 3
                upper = [slice(None)] * 3
                lower[axis] = slice(None, -1)
                upper[axis] = slice(1, None)
                a_now = now[tuple(lower)]
                a_before = before[tuple(lower)]
                b_now = now[tuple(upper)]
                b_before = before[tuple(upper)]
                links += int(np.sum(common * (a_now * b_before + b_now * a_before)))
        return squares - links

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
            # HOST: the birth residue, the input of the diagnostic E_N and never
            # a reader-of-record field (the reader reads `click`, `birth` and
            # `chosen`; DECLARATIONS.md section 2 item 8)
            "u": live.u,
            # HOST: the ledger's row `taken_by_emitter` is 0 since the emitter's
            # own take retired (ALGEBRA.md 9.17); kept for the readers' form
            "taken_by_emitter": 0,
            # HOST (the receiver by name): the sinks' take of the record by
            # this line, in the pointer's unit (the faces and every set but
            # the receiver; on no pointer); on a record with a receiver alone
            "born": live.born,
            "chosen": (
                [[self.detector_set[chosen], self.detector_channel[chosen], "0"]]
                if chosen is not None
                else None
            ),
            "node": [],
            "windows": [],
            "content": live.content,
            "momentum": [0, 0, 0],
            "weight": [live.pointers[chosen] if chosen is not None else 0, 1],
            "total": list(total),
            "unit": UNIT,
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
            "birth": live.birth_tick,
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
        self.tick += 1
        for block in self.blocks:
            self._move_block(block)
        # the family of clicks' level as the interval begins: the hold follows
        # the bodies' steps (a stepping body's Nodes), ALGEBRA.md 9.45 (2)
        self._hold_clock()
        # The massive records first (each block's own record by the rule
        # alone), then the light records: the order of the interval
        # (MASSIVE_RECORD.md section 7's massive step first; the coupling's
        # terms HISTORY, the model owner's decision (2) of record 1962).
        for block in self.blocks:
            if block.own is None:
                continue
            self._advance(block.own)
            if block.definition.emitter is not None:
                self._excitation_rung(block)
        for identity in list(self.records):
            live = self.records[identity]
            if live.arm_done:
                # a completed arm of a pair waits for the other arms
                continue
            if self.families[live.family].massive_kind:
                # A block's massive record is advanced with its block above;
                # a matter lamp's record (a massive kind with a declared
                # clock, born of a lamp) is advanced by the rule with the
                # family's pair alone, through the take and the detector
                # sets' pointers as light's (the click at W, one per record),
                # coupled to nothing (the coupling HISTORY, decision (2) of
                # record 1962), its faces the world's (a zero face a mirror).
                if live.emitter is not None:
                    self._advance(live)
                continue
            self._advance(live)
        for block in self.blocks:
            if block.emit_now:
                self._emit(block)
        for block in self.blocks:
            self._block_clock(block)
        # the clicked records are deleted whole (ALGEBRA.md 8.8, 9.19 (3) (b));
        # a record alive at the run's last interval is reported alive
        for identity in self.dead:
            if identity in self.records:
                self._release(self.records.pop(identity))
        self.dead = []
        # the family of clicks steps last, after every family read its level,
        # and is held at the bodies' Nodes at the content the interval's clicks
        # and births left (ALGEBRA.md 9.45 (2))
        self._advance_clock()
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
            # The mode k = 2 pi / 3 along the declared axis (MASSIVE_RECORD.md
            # section 7, the hop pump's signature; a GAMEBOARD reading): the
            # three sums of light's total field over the residue classes of
            # the axis coordinate modulo 3 (verb G); the tool forms
            # abs(S_0 + w S_1 + w^2 S_2)^2 with w the cube root of unity.
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
                    sum(
                        (
                            self.record_form(live)
                            for live in self.records.values()
                            if live.family == index
                        ),
                        Fraction(0),
                    )
                    + (
                        self.record_form(self.clock_record)
                        if index == self.clock_family
                        else self.record_form(self.charge_record)
                        if index == self.charge_family
                        else Fraction(0)
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

    def detectors(self) -> list[dict[str, object]]:
        found = []
        for detector in self.world.detectors:
            clicks = 0
            for gather in self.layer.gathers:
                chosen = gather["chosen"]
                if isinstance(chosen, list) and chosen and chosen[0][0] == detector.name:
                    clicks += 1
            found.append(
                {
                    "name": detector.name,
                    "positions": [list(p) for p in detector.positions],
                    "clicks": clicks,
                }
            )
        return found

    def covariant_report(self) -> dict[str, object]:
        return {}

    def snapshot_stream(self) -> Iterator[tuple[str, object]]:
        """The state's (key, value) pairs for state.json: the law, the tick,
        the held content per measured event and the live records (their
        identity, age, train and the detectors' pointers), not their rows."""
        yield "law", DETECTOR_LAW_RULE
        yield "tick", self.tick
        yield "measured", self.contents()
        # the family of clicks' level over the board, the Node clock's c at
        # every Node (GAMEBOARD; ALGEBRA.md 9.45)
        yield (
            "clock",
            {
                "family": self.families[self.clock_family].name,
                "node_clock": self.node_clock,
                "rows": self.clock_record.now.ravel().tolist(),
                "form": form_json(self.record_form(self.clock_record)),
            },
        )
        # the family of charge's level over the board (ALGEBRA.md 9.48; item
        # 35): a GAMEBOARD diagnostic beside the family of clicks'
        yield (
            "charge",
            {
                "family": self.families[self.charge_family].name,
                "charge_strength": self.charge_strength,
                "rows": self.charge_record.now.ravel().tolist(),
                "form": form_json(self.record_form(self.charge_record)),
            },
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
                        "emitted": list(block.emitted),
                        "rows": None if block.own is None else block.own.now.ravel().tolist(),
                        "form": None if block.own is None else form_json(self.record_form(block.own)),
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
                    "born": live.born,
                    "birth": live.birth_tick,
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
