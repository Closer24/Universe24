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
that cell (a measured event's own cell `measured:<number>`, a set's cell
by the set's name, a face's `face:<axis>`), and the Node's amplitude is
taken (0 re-emitted). The record completes when its train has ended and
its offer on the board has been exhausted into the cells (below one rung
of the wheel of what the cells hold); the click's cell is chosen by
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
cells carry a lowered pair there, the build's step 3), the kind's own faces
(`faces`: periodic by default, an open face a zero face) and the conserved
form I of section 3 read by the books as a GAMEBOARD diagnostic
(`record_form`). Without the key every world reads as it did, byte for
byte (`tests/test_massive_record.py`).
"""

from __future__ import annotations

from collections.abc import Callable, Iterator
from dataclasses import dataclass, field
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
    # the rule's remainder at the birth cell of the record that clicked to
    # birth it (`residue_of`); a planted record carries the test's W. The
    # rung's wheel is the record's, never a set's or the world's.
    wheel: int = 1
    # massive-record-v1: the emitter's number for a record a body emitted
    # (None for a planted record and for a block's own record), and the
    # coupling's denominator folded into the row's wall (MASSIVE_RECORD.md
    # section 7, MUST A: one D per row per interval; the wall 3 den x
    # scale, the remainder in [0, wall)).
    emitter: int | None = None
    scale: int = 1
    # The pair's arms (detector-law-v1, build 2, component 2; DECLARATIONS.md
    # rows 1a and 1d, DESIGN.md 6.3): a lamp with `arms` births one record
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
    # 7): the cells among which u chooses, None for every cell as built. A
    # cell outside the ladder is a SINK for this record: it takes and books
    # as every cell does (the pointer, `absorbed`, the rung), but the click
    # never chooses it and its share is not in the ladder's sum.
    ladder: list[int] | None = None

    # THE INCREMENT LADDER (ALGEBRA.md 9.25 (2)): the record's running total
    # C of its one-way flux into the cells of its ladder, every cell's
    # increment in the ladder's order, against the record's threshold
    # (2 u + 1) T / (2 W) fixed at its birth; the click at the interval C
    # crosses it, at the cell whose segment of that interval's increment
    # holds the threshold.
    total: int = 0
    # whether the record's line was written (the record is deleted whole at
    # that interval, ALGEBRA.md 8.8, record 1888)
    clicked: bool = False
    # The sinks' take of a record under the receiver by name (HOST, the
    # pointer's unit): what the faces and every set but the receiver took,
    # inside `absorbed` (the completion's measure) and on no pointer.
    escaped: int = 0


@dataclass
class Block:
    """A block on the board (massive-record-v1, MASSIVE_RECORD.md sections 4
    to 7; BUILD.md section 2): its cells R (the mask over the board, the
    cube of `side` at `corner`), its own massive record (the seed on its
    cells), its responses (one massive record per light record reaching
    it), the light records it emitted, its clock (its record's cycles
    across R), its momentum per axis with the drive's accumulators against
    the wall 3 Q S M, and its cell in the simulation's cells."""

    number: int
    family: int
    definition: BlockDefinition
    corner: list[int]
    mask: np.ndarray
    cell: int
    wall: int
    momentum: list[int]
    drive: list[int] = field(default_factory=lambda: [0, 0, 0])
    count: int = 0
    previous_sum: int = 0
    own: LiveRecord | None = None
    responses: dict[int, LiveRecord] = field(default_factory=dict)
    emitted: list[int] = field(default_factory=list)
    current: int | None = None
    births: int = 0
    hop: tuple[int, int, int] = (0, 0, 0)
    new_cycle: bool = False
    # the interval the current cycle began and the last cycle's length (the
    # emitted record's period for its grace, line B)
    cycle_start: int = 0
    cycle_length: int = 0
    stepped: int = 0
    answered: int = 0
    # the emitter as a clicking body (ALGEBRA.md 9.17 (4)): the excitations
    # started (k), the current excited record's booked offer C (its own
    # motion through its cells), and whether its rung fired this interval
    excitations: int = 0
    offer: int = 0
    emit_now: bool = False
    # THE READ POINT OF THE EXCITED RECORD'S RESIDUE (ALGEBRA.md 9.19 (4e),
    # the mathematician's word of 2026-09-25 on BUILD.md section 26 item
    # 15's finding): the seed's remainders are 0 at the write and nonzero
    # after one step of the rule, so u and W are read from the record's own
    # remainder at the centre cell at the first rung after its first
    # advance, and the offer C counts from that interval
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
        # The cells: index 0 .. K - 1 with a name, the Nodes of each, and the
        # measured event (if any) that receives the content of a click there.
        # A detector set is ONE cell over its whole cube (record 1899): the
        # flux into the cube through its Ports from outside is its increment,
        # the click is the detector's, reported by its name, never by a Node.
        self.cell_names: list[str] = []
        self.cell_measured: list[int | None] = []
        self.cell_face: list[bool] = []
        # The gather's cell triple [set, channel, label]: a cell's set name
        # (its own name but for a table body's two cells, which carry their
        # set's name) and its channel (0, the + channel; 1 the - channel of
        # a table body); every cell as built is [name, 0, "0"].
        self.cell_set: list[str] = []
        self.cell_channel: list[int] = []
        self.cell_index = np.full(self.shape, -1, dtype=np.int64)
        for number, entry in enumerate(world.measured):
            nodes = self._span_nodes(entry.position, entry.span)
            own = self._cell(f"measured:{number}", number, False)
            for node in nodes:
                self.cell_index[node] = own
        # The sets bound to a block (DECLARATIONS.md section 10 item 9, section
        # 13 item 1, section 15 M1-4; line 7): RECEIVERS in the form of
        # DESIGN.md section 5, their Nodes take Nodes (the one-way Port take,
        # the row held at 0, the offer booked to the set's cell, `absorbed`
        # moved, the click at the first rung stamped with the block's own
        # count), FREE for the emitting block's own record during that
        # record's grace (the masks per record by its emitter and age). A set
        # with one declared position is the receiving Node beside the block
        # (the light clock's x = 612); a set without positions takes at the
        # block's current cells (R2's blocks, a stepping block's cells follow
        # it). `set_block`: the set's cell to its block; `set_nodes`: the
        # set's declared Nodes' mask, None where the Nodes are the block's.
        self.set_block: dict[int, int] = {}
        # the detector sets' cells in their declared order: the ladder of a
        # record that names no receiver (ALGEBRA.md 9.19 (3) (b))
        self.set_cells: list[int] = []
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
                    "tables (the polariser's two cells at one Node, the splitter's linear form) "
                    "retired with the flux reading (BUILD.md section 26 item 17); a polariser is "
                    "a body with an axis and two receivers named, a splitter a region of the one "
                    "operator (ALGEBRA.md 9.21)"
                )
        for detector in world.detectors:
            set_cell: int | None = None
            if detector.block is not None:
                set_cell = self._cell(detector.name, detector.block, False)
                self.set_block[set_cell] = detector.block
                self.set_cells.append(set_cell)
                if detector.positions:
                    nodes_mask = np.zeros(self.shape, dtype=bool)
                    for position in detector.positions:
                        node = (int(position[0]), int(position[1]), int(position[2]))
                        nodes_mask[node] = True
                        self.cell_index[node] = set_cell
                    self.set_nodes[set_cell] = nodes_mask
                else:
                    self.set_nodes[set_cell] = None
                continue
            for position in detector.positions:
                node = (int(position[0]), int(position[1]), int(position[2]))
                existing = int(self.cell_index[node])
                measured = self.cell_measured[existing] if existing >= 0 else None
                if set_cell is None:
                    set_cell = self._cell(detector.name, measured, False)
                    self.set_cells.append(set_cell)
                elif measured is not None and self.cell_measured[set_cell] is None:
                    self.cell_measured[set_cell] = measured
                self.cell_index[node] = set_cell
        # THE FACE RECEIVER (ALGEBRA.md 9.19 (3) (a); Highlights' record 15
        # kept): an open axis carries the receiver `face` at its border, last
        # on every ladder, so that what leaves the board clicks there; a
        # periodic axis has none; a `closed` face (DECLARATIONS.md section
        # 10's mirror B) is a zero row with no receiver, the level 0 beyond it
        # as `_shift` fills. Nothing takes: the sponge is retired. THE FACE
        # SLAB (9.25 (10); BUILD.md section 26 item 23): the receiver is the
        # slab of the world's `face_depth` free Nodes nearest every open
        # border, one cell, its Ports toward the interior alone (a Link inside
        # the slab carries no offer, the zero row beyond the border no Node).
        self.face_cell: int | None = None
        for axis in range(3):
            if world.periodic[axis] or world.closed[axis] or self.shape[axis] < 2:
                continue
            if self.face_cell is None:
                self.face_cell = self._cell("face", None, True)
            depth = min(world.face_depth, self.shape[axis])
            for index in [*range(depth), *range(self.shape[axis] - depth, self.shape[axis])]:
                view = np.moveaxis(self.cell_index, axis, 0)[index]
                free = view < 0
                view[free] = self.face_cell
        self.records: dict[int, LiveRecord] = {}
        # the records clicked this interval, deleted whole after the advances
        self.dead: list[int] = []
        self.blocks: list[Block] = []
        self.block_by_number: dict[int, Block] = {}
        # The block's count at a light record's first rung at its cell
        # (the click's `clock`, the body's event in the body's own clock).
        self.rung_counts: dict[tuple[int, int], int] = {}
        # The record kinds (massive-record-v1): per family the pair on the
        # six-neighbour term as two dense int64 arrays over the board
        # (light's kind the value [1, 1] everywhere; a massive kind its
        # declared pair; a block's cells a lowered pair there, the build's
        # step 3) and the faces its rows read (the kind's `faces` for a
        # massive kind, the world's `boundary` for light's).
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
        # its cells written into its kind's pair arrays, its own record
        # seeded on its cells, its momentum and the drive's wall 3 Q S M.
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
                int(self.cell_index[tuple(entry.position)]),
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
                    # its norm the seed's squares over the body's cells
                    self._excite(block, own_record)
            self.blocks.append(block)
            self.block_by_number[number] = block
        # Light's wall under the coupling (MASSIVE_RECORD.md section 7, MUST
        # A): 3 L with L the least common multiple of the blocks' source
        # denominators G_d, one number for the kind (1 without a block: the
        # first build's rows bit for bit), so that every light row divides
        # once per interval; a block's source term is scaled by L / G_d.
        self.light_scale = 1
        for block in self.blocks:
            denominator = block.definition.source[1]
            self.light_scale = self.light_scale * denominator // gcd(self.light_scale, denominator)
        # The blocks' cells: a block's cells carry its cell's index (the flux
        # into them booked to it, never chosen: the cell is on no ladder); a
        # set bound to a block without positions owns the block's cells
        # instead (the flux into them booked to the set; line 7). Nothing
        # takes (ALGEBRA.md 9.19 (3)): the rows evolve at every cell.
        if self.blocks:
            for block in self.blocks:
                for node in zip(*np.nonzero(block.mask), strict=True):
                    address = (int(node[0]), int(node[1]), int(node[2]))
                    self.cell_index[address] = block.cell
            for set_cell, number in self.set_block.items():
                if self.set_nodes[set_cell] is None:
                    block = self.block_by_number[number]
                    self.cell_index[block.mask] = set_cell
        # The receiver by name (DECLARATIONS.md section 13 item 7): an
        # emitting block's `receiver` names the detector set whose one cell
        # is the ladder of every record it emits (the click line at that
        # cell's first rung after the train; the faces and every other set
        # sinks for it, their take into `absorbed` alone and onto no pointer).
        # A block without the key keeps the ladder of every cell and the line
        # at the close, as before the key (the registered worlds byte for byte).
        self.receiver_cell: dict[int, int] = {}
        for block in self.blocks:
            name = block.definition.receiver
            if name is None:
                continue
            if name not in self.cell_names:
                raise ValueError(
                    f"{BEAM_LAW}: measured[{block.number}].receiver {name!r} names no cell of the "
                    f"simulation (the cells: {self.cell_names})"
                )
            self.receiver_cell[block.number] = self.cell_names.index(name)
        self.has_receiver = bool(self.receiver_cell)

    def _receiver_of(self, live: LiveRecord) -> int | None:
        """The one cell of the record's ladder under the receiver by name
        (its emitting block's `receiver`); None for a record without one (a
        lamp's record, or a block's without the key: the ladder every cell,
        the line at the close)."""
        if live.emitter is None:
            return None
        return self.receiver_cell.get(live.emitter)

    def _cell(
        self, name: str, measured: int | None, face: bool, set_name: str | None = None, channel: int = 0
    ) -> int:
        self.cell_names.append(name)
        self.cell_measured.append(measured)
        self.cell_face.append(face)
        self.cell_set.append(name if set_name is None else set_name)
        self.cell_channel.append(channel)
        return len(self.cell_names) - 1

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
        """The cells R of a block: the box of `extents` per axis (a cube's
        side three times; the slabs of ALGEBRA.md 9.22 (8)) from its lower
        corner, wrapped on an axis the kind's faces make periodic, cut on an
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
        """The block's pair written on its cells into its kind's arrays; the
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
            pointers=[0] * len(self.cell_names),
            first_rung=[None] * len(self.cell_names),
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

    def motion_pair(self, block: Block) -> tuple[int, int]:
        """The index in motion (MASSIVE_RECORD.md section 7, record 1418): the
        coupling's g carried as [W_d^2, W_d^2 - 3 P . P] with W_d the drive's
        wall 3 Q S M and P the block's momentum, integers the stepping cell
        has (on one axis with K = W_d / abs(P_a) whole, [K^2, K^2 - 3]);
        [1, 1] at rest; reduced by the gcd."""
        momentum = self._momentum_now(block)
        square = block.wall * block.wall
        numerator = square
        denominator = square - 3 * sum(component * component for component in momentum)
        common = gcd(numerator, denominator)
        return numerator // common, denominator // common

    def _move_block(self, block: Block) -> None:
        """The block's step (MASSIVE_RECORD.md section 5): per axis the
        accumulator gains the momentum's component against the wall 3 Q S M
        (verb T, then D with the remainder kept, at most one Link per
        interval, `core.integer.by_drive`), x before y before z, a second
        Link in one interval lost to the earlier axis (its wall subtracted,
        the frame's tie); the cells and the pair region translate by T; the
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
            # stepping block whose cell would leave the board by a zero face
            # (the cube cut by `_cube` on a non-periodic axis) refuses the
            # interval naming the block, instead of running on with the block
            # gone and the books balanced; the margin rule refuses the same
            # block at load, not at a hop, so this is the run's own check.
            raise RuntimeError(
                f"{BEAM_LAW}: measured[{block.number}] stepped off the board at interval "
                f"{self.tick} (its corner {list(block.corner)}, extents {list(block.definition.extents)}, "
                f"{int(np.count_nonzero(block.mask))} of {int(np.count_nonzero(old_mask))} cells "
                "left on the board): a block's cells must stay on the board; the run is refused"
            )
        self._write_pair(block)
        block.stepped += 1
        # The block's cell follows its cells (a set bound to it without
        # positions with them); the Nodes it left are free Nodes.
        for node in zip(*np.nonzero(old_mask & ~block.mask), strict=True):
            address = (int(node[0]), int(node[1]), int(node[2]))
            self.cell_index[address] = -1
        set_cell = next(
            (
                cell
                for cell, number in self.set_block.items()
                if number == block.number and self.set_nodes[cell] is None
            ),
            None,
        )
        for node in zip(*np.nonzero(block.mask), strict=True):
            address = (int(node[0]), int(node[1]), int(node[2]))
            self.cell_index[address] = block.cell if set_cell is None else set_cell

    def _difference(self, live: LiveRecord, block: Block) -> np.ndarray:
        """The first difference of a record's row the coupling reads at the
        block's cells: the SAME-NODE difference, now less before at the
        Node, on every interval, a hop interval included (the design's word
        of records 1444 and 1445: the hop moves the cells' set and the pair
        region only, the rows stay and re-form by the rule; an along-path
        difference is pumped parametrically by the hop's pair resonance with
        light's band and is not built). The block's hop is kept on the block
        for the record and read by nothing here."""
        _ = block
        difference: np.ndarray = live.now - live.before
        return difference

    def _coupled_term(
        self, target: LiveRecord, delta: np.ndarray, mask: np.ndarray, numerator: int
    ) -> np.ndarray:
        """One entry of the coupling (verb B): the term added to the target's
        total at the cells, 3 den x numerator x delta, the coupling's
        denominator folded into the row's wall (MASSIVE_RECORD.md section 7,
        MUST A: one D per row per interval, no second division; the row's
        `scale` carries the denominator, `_advance` divides once)."""
        term: np.ndarray = np.where(mask, 3 * self.kind_den[target.family] * numerator * delta, 0)
        return term

    def receive_scale(self, block: Block) -> int:
        """The wall's factor of a block's massive rows: g's denominator times
        the drive's pair's (the index in motion), the one division's wall
        3 den g_d x pair_d."""
        return block.definition.receive[1] * self.motion_pair(block)[1]

    def _receive(self, block: Block, response: LiveRecord, light: LiveRecord) -> np.ndarray:
        """The receive: the block's massive row gains g times light's first
        difference at its cells; in motion g carried as the drive's pair;
        the term 3 den g_n pair_n x delta against the wall 3 den g_d pair_d."""
        delta = self._difference(light, block)
        return self._coupled_term(
            response, delta, block.mask, block.definition.receive[0] * self.motion_pair(block)[0]
        )

    def _source(self, block: Block, massive: LiveRecord, light: LiveRecord) -> np.ndarray:
        """The source term (the same entry): light's row gains -G times the
        massive record's current at the block's cells, the term
        -3 G_n (L / G_d) x delta against light's wall 3 L (L the least common
        multiple of the blocks' G_d, `light_scale`)."""
        delta = self._difference(massive, block)
        numerator, denominator = block.definition.source
        return self._coupled_term(
            light, delta, block.mask, -numerator * (self.light_scale // denominator)
        )

    def residue_of(self, live: LiveRecord, block: Block) -> tuple[int, int]:
        """THE RESIDUE FROM THE LAW (ALGEBRA.md 9.22 (4); BUILD.md section 26
        item 15): the record's rule remainder r at the body's centre cell,
        read now, in units of the remainder's step g = gcd(num x scale,
        wall) (r moves on the multiples of g from 0), and the wheel W =
        wall / g = 3 den / gcd(num, 3 den) values (the pair at that cell;
        700 on [801, 700], 2403 on [800, 801]); no declaration, no draw."""
        centre = self.centre_mask(block)
        node = tuple(int(axis[0]) for axis in np.nonzero(centre))
        num = int(self.kind_num[live.family][node]) * live.scale
        wall = 3 * int(self.kind_den[live.family][node]) * live.scale
        step = gcd(num, wall)
        return int(live.remainder[node]) // step, wall // step

    def _excite(self, block: Block, own_record: LiveRecord) -> None:
        """The excited record's norm and the residue owed (ALGEBRA.md 9.17
        (4) item 1, (5) item 1, 9.19 (3), 9.19 (4e) and 9.22 (4)): the norm
        T the one-way flux into the body's centre cell its own mode books
        over one period of its clock (the emitter's declared integer `norm`,
        the generator's, recomputed at load); its residue and wheel from the
        law (`residue_of`) are read at the first rung AFTER ITS FIRST ADVANCE
        (the seed's remainders are 0 at the write; the mathematician's word
        on item 15's finding), the offer C counting from that interval."""
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
        if emitter.born is None:
            raise ValueError(
                f"{BEAM_LAW}: measured[{block.number}].emitter declares no `born`: the born pair's "
                "two integers [now, before] on every cell of the body, the generator's (ALGEBRA.md "
                "9.17 (6); `excite_on_the_mode` of the massive record generator; no table in the "
                "engine)"
            )
        if emitter.norm is None:
            raise ValueError(
                f"{BEAM_LAW}: measured[{block.number}].emitter declares no `norm`: the one-way flux "
                "into the body's centre cell over one period of its clock, the generator's integer "
                "(ALGEBRA.md 9.17 (5) item 1, 9.19 (3); `excite_on_the_mode` of the massive record "
                "generator)"
            )
        block.excitations += 1
        block.residue_pending = True
        own_record.norm = emitter.norm
        block.offer = 0
        block.emit_now = False

    def centre_mask(self, block: Block) -> np.ndarray:
        """The excited record's named set (ALGEBRA.md 9.19 (3)): the body's
        centre cell, the lower corner plus the extent // 2 on each axis, one
        Node (the cell itself for a body of side 1); it follows the body's
        steps."""
        return self._box(
            [int(block.corner[axis]) + block.definition.extents[axis] // 2 for axis in range(3)],
            (1, 1, 1),
            block.family,
        )

    def _excitation_rung(self, block: Block) -> None:
        """E then D on the excited record (ALGEBRA.md 9.17 (4) item 1 and 9.19
        (3)): the one-way inward flux into its centre cell this interval,
        booked to its offer C (read-through, nothing taken), and the rung
        2 T u + T <= 2 W C on the record's own wheel W fires the click (the
        birth follows once the interval's records are advanced). The flux
        is read from the two levels AFTER the interval's advance (the block's
        record is advanced before this is called). At the first call after
        a (re)seed the record's residue u and wheel W are read from its own
        remainder at the centre cell, now nonzero after its first advance
        (9.19 (4e)), and C counts from this interval."""
        own = block.own
        emitter = block.definition.emitter
        if own is None or emitter is None or block.emit_now:
            return
        if block.residue_pending:
            own.u, own.wheel = self.residue_of(own, block)
            block.residue_pending = False
            block.offer = 0
        block.offer += self.inward_flux(own, self.centre_mask(block))
        if 2 * own.norm * own.u + own.norm <= 2 * own.wheel * block.offer:
            block.emit_now = True

    def _emit(self, block: Block) -> None:
        """The click of the excited record and the birth (ALGEBRA.md 9.17 (4)
        items 1 to 3, (5) items 2 to 4 and (6); 9.13: E, then X, then E^T): X
        ends the excited record; E^T writes the born record ONCE at both
        levels: the world's two integers `born` [now, before] on every cell
        of the body (the generator's now = A C_2N[3 N / 2 + s] on the circle
        of 2 N steps with s = floor(n / d) the born clock's step and before =
        -now, the character half a step either side of its zero, no static
        part, A the amplitude unit; no table in the engine); the
        norm T the record's conserved form (9.19 (3)), its residue and
        wheel from the law (9.22 (4): the clicking record's remainder at the
        centre cell, read at the click), the content one quantum moved from
        the body's stock; then, while the stock lasts, the next excited
        record (the seed again). Nothing drives the born record afterwards:
        the law advances it."""
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
        # the born record's residue and wheel from the law (9.22 (4)): the
        # clicking record's remainder at the birth's centre cell, read at the
        # click
        residue, wheel = self.residue_of(own, block)
        offer = block.offer
        # X: the excited record ends
        del self.records[own.identity]
        block.own = None
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
            pointers=[0] * len(self.cell_names),
            first_rung=[None] * len(self.cell_names),
            wheel=wheel,
            labels=tuple(emitter.branches),
            emitter=number,
        )
        # E^T: the born clock's character on the body's cells, written once at
        # both levels, every cell at the vertex's phase (the one-cell broadband
        # birth; a line's travelling character, the per-Link pair of ALGEBRA.md
        # 9.17 (4) item 2, is owed until that pair is declared)
        # NO TABLE IN THE ENGINE (the cleanup order's step 2; ALGEBRA.md 9.17
        # (6), 9.22 (2)): the born pair is the world's two integers `born:
        # [now, before]`, the generator's, checked at load (before = -now),
        # written on every cell of the body
        assert emitter.born is not None
        live.now[block.mask] = emitter.born[0]
        live.before[block.mask] = emitter.born[1]
        # the norm T the record's conserved form I in the flux's units (9.19 (3))
        live.norm = self.conserved_form(live)
        if emitter.receiver is not None:
            # the named sets in the NAMED order (ALGEBRA.md 9.19 (3) (b): the
            # ladder cumulative in its declared order), a set's cells in the
            # cells' order within it
            live.ladder = [
                cell
                for name in emitter.receiver
                for cell, set_name in enumerate(self.cell_set)
                if set_name == name
            ]
        self.held[number][block.family] -= 1
        self.ledger.held_spent[block.family] += 1
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
                    "excitation_offer": offer,
                    "norm": live.norm,
                    "cells": int(np.sum(block.mask)),
                    "cycle": block.count,
                    **({"clock": block.count} if world.clock_stamp else {}),
                }
            )
        # the next excitation while the stock lasts
        if self.held[number][block.family] > 0:
            fresh = self._massive_record(
                number * (1 << 32) + (1 << 30) + block.excitations, number, block.family
            )
            # the seed is the body's composed mode (9.9, 9.17 (4) item 1): the
            # loader requires the profile on a body that births
            assert block.definition.profile is not None
            profile = np.array(block.definition.profile, dtype=np.int64).reshape(self.shape)
            fresh.now[:] = profile
            fresh.before[:] = profile
            block.own = fresh
            self.records[fresh.identity] = fresh
            block.previous_sum = int(np.sum(fresh.now[block.mask]))
            self._excite(block, fresh)
        else:
            block.emit_now = False
            block.offer = 0

    def _block_clock(self, block: Block) -> None:
        """The block's clock (MASSIVE_RECORD.md sections 4 and 6): its total
        record summed across its cells (G over R: its own record and the
        responses light drives), one count per cycle (the sum's crossing
        from at most 0 to above 0, verb D's comparison), a `click` line per
        count with its own count (the self-click of row (g)); a new cycle
        births its emission at the next interval."""
        total = 0
        # the co-moving centre cell (the design's reading of the clock in
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
        for response in block.responses.values():
            total += int(np.sum(response.now[block.mask]))
            at_centre += int(response.now[centre])
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

    def _advance_inverse(
        self, live: LiveRecord, extra: np.ndarray | None = None, scale: int = 1
    ) -> None:
        """One interval of the rule backwards on a record: from (a_next, a_now,
        r') to (a_now, a_before, r) with 3 den a_before - r = num S_6(a_now)
        + extra - (3 den a_next + r'), the remainder in [0, wall): a_before the
        ceiling of that quotient, r the difference (board_algebra.py's
        `step_inverse`)."""
        if live.scale != scale:
            live.remainder = live.remainder * scale // live.scale
            live.scale = scale
        num = self.kind_num[live.family]
        den = self.kind_den[live.family]
        wall = 3 * den * scale
        total = num * scale * self._neighbours(live.before, self.kind_wrap[live.family])
        total -= wall * live.now + live.remainder
        if extra is not None:
            total += extra
        a_before = -np.floor_divide(-total, wall)
        live.remainder = wall * a_before - total
        live.now = live.before
        live.before = a_before
        live.age -= 1

    def step_inverse(self) -> None:
        """One interval backwards (8.8), in the reverse column order of `step`:
        the light records first (their sources from the massive records'
        current differences), then the responses and the bodies' own records
        (their receive from the light records' recovered differences); no
        push, no click, no birth (the bodies at rest and no click in the
        interval, the property test's world)."""
        for block in self.blocks:
            if any(int(component) != 0 for component in block.momentum):
                raise ValueError(
                    f"{BEAM_LAW}: the inverse map is defined at rest (block {block.number} moves)"
                )
        for identity in list(self.records):
            live = self.records[identity]
            if self.families[live.family].massive_kind and live.emitter is None:
                continue
            sources: np.ndarray | None = None
            if self.blocks:
                sources = np.zeros(self.shape, dtype=np.int64)
            for block in self.blocks:
                if live.emitter == block.number:
                    continue
                if block.definition.receive == (0, 1) and block.definition.source == (0, 1):
                    continue
                response = block.responses.get(identity)
                if response is not None and sources is not None:
                    sources += self._source(block, response, live)
            self._advance_inverse(live, sources, self.light_scale)
        for block in self.blocks:
            for identity, response in block.responses.items():
                light = self.records.get(identity)
                if light is not None:
                    self._advance_inverse(
                        response, self._receive(block, response, light), self.receive_scale(block)
                    )
            if block.own is not None:
                extra = np.zeros(self.shape, dtype=np.int64)
                for identity in block.emitted:
                    light = self.records.get(identity)
                    if light is not None:
                        extra += self._receive(block, block.own, light)
                self._advance_inverse(block.own, extra, self.receive_scale(block))
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
        `boundary` by default; a massive kind's own `faces`)."""
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
        the row itself on an axis of one layer; `wrap` the kind's faces
        (the world's by default). Nothing is read through a Port: the take
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
        """The Ports of every cell for the flux reading (ALGEBRA.md 9.25 (2),
        the mathematician's gate item 2): per axis of extent above 1 and
        per side s, the Nodes of a cell whose neighbour on that side (the
        read across the Link, on the family's faces) is a Node of no set or
        of ANOTHER set; a Link between two Nodes of one set (inside a
        detector's cube) is no Port, so the energy that entered the set at
        one Node is not offered again at its neighbour. A self-read of a folded
        axis carries no flux; beyond an open face there is no Node and no
        Link."""
        wrap = self.kind_wrap[family]
        set_names = sorted(set(self.cell_set))
        set_of_cell = [set_names.index(name) for name in self.cell_set]
        set_index = np.full(self.shape, -1, dtype=np.int64)
        occupied = self.cell_index >= 0
        set_index[occupied] = np.array(set_of_cell, dtype=np.int64)[self.cell_index[occupied]]
        ports: list[tuple[int, int, np.ndarray]] = []
        for axis in range(3):
            if self.shape[axis] == 1:
                continue
            for side in (1, -1):
                neighbour = self._shift(set_index, axis, -side, fill=-2, wrap=wrap)
                mask = occupied & (neighbour != -2) & (neighbour != set_index)
                ports.append((axis, side, mask))
        return ports

    def flux_offer(self, live: LiveRecord) -> dict[int, int]:
        """The one-way inward flux into every cell this interval (9.19 (3)):
        over the cell's Ports, 3 G_ij = now_i before_j - before_i now_j where
        positive, times the family's wall, from the record's two levels AFTER
        the interval's step (`_advance` books it once `now` and `before` have
        moved; the prototype's reading); by the cell's index."""
        wrap = self.kind_wrap[live.family]
        wall = self.kind_wall(live.family)
        now = live.now.astype(object)
        before = live.before.astype(object)
        inward = np.zeros(self.shape, dtype=object)
        for axis, side, mask in self._flux_ports(live.family):
            now_j = self._shift(live.now, axis, -side, wrap=wrap).astype(object)
            before_j = self._shift(live.before, axis, -side, wrap=wrap).astype(object)
            flux = now * before_j - before * now_j
            inward = inward + np.where(mask & (flux > 0), flux, 0)
        offers: dict[int, int] = {}
        for node in zip(*np.nonzero(inward), strict=True):
            cell = int(self.cell_index[node])
            offers[cell] = offers.get(cell, 0) + int(inward[node]) * wall
        return offers

    def inward_flux(self, live: LiveRecord, mask: np.ndarray) -> int:
        """The one-way inward flux into the Nodes of `mask` through the Links
        from Nodes outside it (9.19 (3)): 3 G_ij = now_i before_j - before_i
        now_j where positive, times the family's wall, from the record's two
        levels after the interval's step (`now`, `before`; the prototype's
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

    def conserved_form(self, live: LiveRecord) -> int:
        """The record's conserved form I (ALGEBRA.md 8.2) in the flux's units,
        3 I x wall: over the Nodes 3 wall (den_i / num_i) (now_i^2 +
        before_i^2) - wall now_i (A before)_i, A the read matrix with the
        family's faces (the six reads, the folded axes' self-reads)."""
        family = live.family
        wall = self.kind_wall(family)
        weight = (3 * wall * self.kind_den[family] // self.kind_num[family]).astype(object)
        now = live.now.astype(object)
        before = live.before.astype(object)
        read = self._neighbours(live.before, self.kind_wrap[family]).astype(object)
        return int(np.sum(weight * (now * now + before * before) - wall * now * read))

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

    def _advance(self, live: LiveRecord, extra: np.ndarray | None = None, scale: int = 1) -> None:
        # THE EMITTER'S CELLS ARE CELLS LIKE EVERY OTHER (ALGEBRA.md 9.17; the
        # Boss's line of 2026-09-24 on the knot): no grace, no exemption, no
        # own take, no fresh Port; the born record is written once and the
        # law advances it (the retired forms in BUILD.md section 26).
        # Every born record, light's kind or a massive kind alike, books its
        # flux at the cells and clicks on its ladder (the click is the law's
        # one action on any record, POSTULATES 10); a BLOCK'S own record and
        # its responses (a massive kind, born of no emitter) book nothing and
        # are on no ladder (massive-record-v1, MUST 2).
        booked = not self.families[live.family].massive_kind or live.emitter is not None
        # The rule with the kind's pair on the six-neighbour term
        # (massive-record-v1, MASSIVE_RECORD.md section 1): G over the six
        # neighbours, then D by 3 den with the remainder kept, then T; at
        # light's pair [1, 1] the first build's integers bit for bit.
        num = self.kind_num[live.family]
        den = self.kind_den[live.family]
        # The coupling's denominator folded into the wall (MASSIVE_RECORD.md
        # section 7, MUST A): the wall 3 den x scale, the six-neighbour term
        # num x scale x S_6, the coupling's term 3 den x numerator x delta,
        # one division; a scale that changes (the drive's pair under a
        # ramp) rescales the remainder to the new wall, r x new // old.
        if live.scale != scale:
            live.remainder = live.remainder * scale // live.scale
            live.scale = scale
        wall = 3 * den * scale
        neighbours = self._neighbours(live.now, self.kind_wrap[live.family])
        total = num * scale * neighbours
        total -= wall * live.before
        total += live.remainder
        if extra is not None:
            # The coupling's term (massive-record-v1, section 7): one entry
            # of the declared matrix over the other record's two columns at
            # a block's cells, undivided, the wall its divisor.
            total += extra
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
        # inward flux into every cell this interval, from the record's two
        # levels, booked to the cell's pointer C; nothing is taken, the rows
        # evolve at every Node
        before_booking = list(live.pointers)
        for cell, value in self.flux_offer(live).items():
            live.pointers[cell] += value
            live.absorbed += value
        # this interval's increment per cell
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
            ladder = [receiver] if receiver is not None else list(self.set_cells)
        if self.face_cell is not None and self.face_cell not in ladder:
            ladder.append(self.face_cell)
        return ladder

    def _ladder_click(self, live: LiveRecord, increments: list[int]) -> None:
        """THE INCREMENT LADDER (ALGEBRA.md 9.25 (2), the mathematician's word
        of 2026-09-25 on the finding of BUILD.md section 26 item 14; the
        cumulative sums of 9.19 (3) (b) withdrawn): the record's threshold
        theta = (2 u + 1) T / (2 W) is fixed at its birth (u its residue, T
        its norm, W its own wheel); at every interval the record's running
        total C gains this interval's one-way flux into the cells of its
        ladder, the cells in the ladder's declared order (the named sets in
        the named order, the face last); the click fires at the first
        interval at which C crosses theta, at the cell whose segment of that
        interval's increment, laid out in the ladder's order, holds theta
        (the walk: the cell k at which 2 W (C + f_1 + ... + f_k) >= (2 u + 1)
        T first). Born's rule is its theorem (9.25 (3): the cell's share of
        the record's total inward flux, whatever the time profile). A cell is
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
        threshold = (2 * live.u + 1) * live.norm
        running = 2 * live.wheel * live.total
        for cell in ladder:
            running += 2 * live.wheel * increments[cell]
            live.total += increments[cell]
            if running >= threshold:
                live.first_rung[cell] = self.tick
                if cell in self.set_block:
                    self.rung_counts[(live.identity, cell)] = self.block_by_number[
                        self.set_block[cell]
                    ].count
                self._gather_line(live, cell)
                live.clicked = True
                self.dead.append(live.identity)
                return

    def record_form(self, live: LiveRecord) -> int:
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
        weight = (3 * den * scale).astype(object)
        squares = int(np.sum(weight * (now * now + before * before)))
        links = 0
        wrap = self.kind_wrap[live.family]
        link_weight = common
        for axis in range(3):
            # Each Link once: the Node and its neighbour on the + side (the
            # wrap on a periodic axis closes the last Link, an open face
            # has none); an axis of one layer reads the row itself as its
            # two neighbours (DESIGN.md section 2), two self-Links the form
            # carries (the roll on a length-one axis is the identity).
            if wrap[axis] or self.shape[axis] == 1:
                now_next = np.roll(now, -1, axis=axis)
                before_next = np.roll(before, -1, axis=axis)
                links += int(np.sum(link_weight * (now * before_next + now_next * before)))
            else:
                lower = [slice(None)] * 3
                upper = [slice(None)] * 3
                lower[axis] = slice(None, -1)
                upper[axis] = slice(1, None)
                a_now = now[tuple(lower)]
                a_before = before[tuple(lower)]
                b_now = now[tuple(upper)]
                b_before = before[tuple(upper)]
                links += int(np.sum(link_weight * (a_now * b_before + b_now * a_before)))
        return squares - links

    def _release(self, live: LiveRecord) -> None:
        """The record's rows leave the board: the
        blocks' responses, the emitters' lists and the rung counts of the
        record are dropped."""
        for block in self.blocks:
            block.responses.pop(live.identity, None)
            if live.identity in block.emitted:
                block.emitted.remove(live.identity)
        for key in [key for key in self.rung_counts if key[0] == live.identity]:
            del self.rung_counts[key]

    def _gather_line(self, live: LiveRecord, chosen: int | None) -> None:
        """The record's one click line (`gather`, the amplitude law's keys):
        the content handed to the measured event at the chosen cell (or
        booked as escaped at a face or a set without a body; with no cell
        chosen, to the escaped row or, where the record's own emitter took
        it wholly, to `taken_by_emitter`), the line written with `click` the
        chosen cell's first rung (or the completion where no rung was
        crossed) and `clock` the detector's own count. Called once per
        record: at the close (`_click`) or, under the receiver by name, at
        the receiver's rung (`_line_at_rung`)."""
        # the ladder's weights: the record's ladder of `_ladder_of` (the
        # emitter's named sets, or the block's receiver, or every declared
        # set, the face receiver last on every ladder; ALGEBRA.md 9.19 (3)
        # (b)), every cell off it at 0, so that the cell of u is over the
        # ladder's own sum and a cell off the ladder is never chosen
        ladder_cells = set(self._ladder_of(live))
        on_ladder = [cell in ladder_cells for cell in range(len(live.pointers))]
        weights = [(p if here else 0, 1) for p, here in zip(live.pointers, on_ladder, strict=True)]
        family = live.family
        ladder, total = rungs(weights, live.wheel)
        sunk = sum(p for p, here in zip(live.pointers, on_ladder, strict=True) if not here)
        if chosen is None:
            self.ledger.transit_escaped[family] += live.content
            self.ledger.held_escaped[family] += 0
        else:
            measured = self.cell_measured[chosen]
            if measured is not None and not self.cell_face[chosen]:
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
                [[self.cell_set[chosen], self.cell_channel[chosen], "0"]] if chosen is not None else None
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
            "cells": [
                [[[set_name, channel, "0"]], rung]
                for set_name, channel, rung, pointer in zip(
                    self.cell_set, self.cell_channel, ladder, live.pointers, strict=True
                )
                if pointer
            ],
            # the ladder by name (the lamp's `receiver`): the sets on it, and
            # HOST the pointers' sum at the sinks (the cells off the ladder,
            # taken and booked, never chosen); None and 0 for every cell
            **(
                {"ladder": sorted({self.cell_set[cell] for cell in live.ladder}), "sunk": sunk}
                if live.ladder is not None
                else {}
            ),
            "birth": live.birth_tick,
            # The click's time: the interval at which the chosen cell's pointer
            # crossed its first rung (the counting form, s_D = 1 / W), the
            # detector's own count on the click line; the record completed at
            # `tick`, when its offer was exhausted.
            "click": (
                live.first_rung[chosen]
                if chosen is not None and live.first_rung[chosen] is not None
                else self.tick
            ),
            # Reviewer 3's line 2 (the Boss's 01:40Z): which the click's time
            # is, the chosen cell's first rung or, where no rung was crossed
            # (a screen row's Node at 1e-4 of the norm), the completion
            # interval; a reader never reads a completion as a rung.
            "click_at": (
                "rung" if chosen is not None and live.first_rung[chosen] is not None else "completion"
            ),
            # whose count the `clock` stamp is: a block's own count where the
            # chosen cell is a block's cell or a set bound to a block (keys (i)
            # and (ii)), else the interval
            "clock_source": (
                f"measured:{self.cell_measured[chosen]}"
                if chosen is not None and (live.identity, chosen) in self.rung_counts
                else "interval"
            ),
            **(
                {
                    "clock": (
                        # A block's cell: the block's own count at the first
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
        # The massive records first (each block's own record driven by its
        # emitted light's first differences, the responses by their light
        # record's), then the light records with the source terms (the
        # massive currents just formed): the order of the interval,
        # MASSIVE_RECORD.md section 7 (the massive step first).
        for block in self.blocks:
            if block.own is None:
                continue
            extra = np.zeros(self.shape, dtype=np.int64)
            for identity in block.emitted:
                light = self.records.get(identity)
                if light is not None:
                    extra += self._receive(block, block.own, light)
            self._advance(block.own, extra, self.receive_scale(block))
            if block.definition.cavity:
                block.own.now[~block.mask] = 0
                block.own.remainder[~block.mask] = 0
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
                # coupled to no block (the coupling is declared on light's
                # row, MASSIVE_RECORD.md section 7), its faces the kind's
                # (a zero face a mirror).
                if live.emitter is not None:
                    self._advance(live)
                continue
            sources: np.ndarray | None = None
            if self.blocks:
                sources = np.zeros(self.shape, dtype=np.int64)
            for block in self.blocks:
                if live.emitter == block.number:
                    # a body answers no record of its own (its own record
                    # received the born light's difference above)
                    continue
                if block.definition.receive == (0, 1) and block.definition.source == (0, 1):
                    continue
                response = block.responses.get(identity)
                if response is None:
                    block.answered += 1
                    response = self._massive_record(
                        block.number * (1 << 32) + (1 << 31) + block.answered, block.number, block.family
                    )
                    block.responses[identity] = response
                self._advance(response, self._receive(block, response, live), self.receive_scale(block))
                if sources is not None:
                    sources += self._source(block, response, live)
            self._advance(live, sources, self.light_scale)
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
                lines["form"] = sum(
                    self.record_form(live) for live in self.records.values() if live.family == index
                ) + sum(
                    self.record_form(response)
                    for block in self.blocks
                    for response in block.responses.values()
                    if response.family == index
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
        identity, age, train and the cells' pointers), not their rows."""
        yield "law", DETECTOR_LAW_RULE
        yield "tick", self.tick
        yield "measured", self.contents()
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
                        "responses": len(block.responses),
                        "emitted": list(block.emitted),
                        "rows": None if block.own is None else block.own.now.ravel().tolist(),
                        "form": None if block.own is None else self.record_form(block.own),
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
                    "pointers": dict(zip(self.cell_names, live.pointers, strict=True)),
                    **({"form": self.record_form(live)} if self.world.massive_record else {}),
                }
                for live in self.records.values()
            ],
        )
