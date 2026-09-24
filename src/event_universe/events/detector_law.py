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
from event_universe.core.integer import by_clock, by_drive, integer_root, keyed_permutation
from event_universe.core.phase import PHASE_COSINE_SCALE, nearest_phase, phase_cosines, phase_sines
from event_universe.events.amplitude import cell_of, rungs
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
TAKE_NUMERATOR = -15
TAKE_DENOMINATOR = 56


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
    ports: list[np.ndarray] = field(default_factory=list)
    driven: np.ndarray | None = None
    # line 7: whether the record's last interval was exempt at the sets bound
    # to its emitter (the grace's end books the set Nodes' own content once)
    was_exempt: bool = False
    # massive-record-v1: the emitter's number for a record a block emitted
    # (None for a lamp's record), whether the block is still sourcing it
    # (the current cycle's record), and the coupling's denominator folded
    # into the row's wall (MASSIVE_RECORD.md section 7, MUST A: one D per
    # row per interval; the wall 3 den x scale, the remainder in [0, wall)).
    emitter: int | None = None
    sourcing: bool = False
    scale: int = 1
    # The Ports' first differences summed (a taken record): what an absorbing
    # block's cells read of light, the field its coupling receives.
    port_motion: np.ndarray | None = None
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


@dataclass
class Splitter:
    """A splitter of the TABLE form (detector-law-v1, build 2, component 3;
    DECLARATIONS.md row 2b, ALGEBRA.md 4.6): a measured event whose `table`
    declares a `rerelease` split with `inputs`, one weights row and one
    turns row per input direction, its `directions` the outputs; one
    table Node per Node of the line across a corridor (DECLARATIONS.md
    section 14 item 4, a list of splitters). Its Node is held at 0 and
    takes the arriving wave (a receiver that books no offer); per
    interval, per light record, the table acts on the record's PAIR
    (a_before, a_now) at each input Node (the Node the input direction
    arrives from) by the LINEAR FORM of section 14, A cos(phi + t) =
    (a_now S[k + t] - a_before S[t]) / S[k] (S the sine table, cos x 256's
    companion; k the interval's own whole step of the clock, `by_clock`),
    and each output's term SUM_i w_ij (a_now,i S[k + t_ij] - a_before,i
    S[t_ij]) / (S[k] R_i), R_i the root of the row's norm (exact, checked
    at load: the split an isometry, 21^2 + 20^2 = 29^2), is ADDED to what
    the rule gave the output Node (a partial re-emission with a phase, the
    mirror its model; never a hard level): verbs B (the matrix on the two
    columns), D (one division per output per interval by the wall S[k] x
    L, L the least common multiple of the rows' roots, the remainder
    carried per output as the rule's) and G (the term added). No reading,
    no register: the record's own levels and the division's remainder,
    nothing else."""

    number: int
    family: int
    node: tuple[int, int, int]
    inputs: list[tuple[tuple[int, int, int], tuple[int, ...], tuple[int, ...], int]]
    outputs: list[tuple[int, int, int]]
    remainders: dict[int, list[int]] = field(default_factory=dict)


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
    # a block bound by a detector set without positions: its cells are the
    # set's take Nodes (a receiver, DECLARATIONS.md section 10 item 9 and
    # section 13 item 1), the absorbing path for every record but its own
    # during that record's grace
    taking: bool = False
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
        )
        # The cells: index 0 .. K - 1 with a name, the Nodes of each, and the
        # measured event (if any) that receives the content of a click there.
        self.cell_names: list[str] = []
        self.cell_measured: list[int | None] = []
        self.cell_face: list[bool] = []
        self.cell_index = np.full(self.shape, -1, dtype=np.int64)
        self.absorbing = np.zeros(self.shape, dtype=bool)
        self.lamp_nodes: dict[int, list[tuple[int, int, int]]] = {}
        self.lamp_accumulator: dict[int, int] = {}
        self.lamp_births: dict[int, int] = {}
        # The order channel's key (DECLARATIONS.md section 2 item 8): a pair
        # lamp under `residue_order` "seed" births the residues of its wheel's
        # Z_W in the order of a keyed permutation, formed once here from its
        # `residue_seed` (an input of kind 1, written to no line; the hash the
        # declaration's, verbatim); a lamp under "ordinal" keeps the counter.
        self.birth_orders: dict[int, list[int]] = {}
        for number, entry in enumerate(world.measured):
            lamp_definition = entry.lamp
            if lamp_definition is not None and lamp_definition.residue_order == "seed":
                assert lamp_definition.residue_seed is not None
                self.birth_orders[number] = keyed_permutation(
                    lamp_definition.wheel[1], lamp_definition.residue_seed
                )
        for number, entry in enumerate(world.measured):
            nodes = self._span_nodes(entry.position, entry.span)
            if entry.lamp is not None:
                self.lamp_nodes[number] = nodes
                self.lamp_accumulator[number] = 0
                self.lamp_births[number] = 0
            own = self._cell(f"measured:{number}", number, False)
            for node in nodes:
                self.cell_index[node] = own
                self.absorbing[node] = True
        # The rung W per cell: the world's wheel, or a set's own `wheel`
        # (DECLARATIONS.md section 15 M1-4: the receivers of 4b, the light
        # clock and R2 at their own W = 64 in a lamp-less world).
        self.cell_wheel: dict[int, int] = {}
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
        self.set_nodes: dict[int, np.ndarray | None] = {}
        for detector in world.detectors:
            set_cell: int | None = None
            if detector.block is not None:
                set_cell = self._cell(detector.name, detector.block, False)
                self.set_block[set_cell] = detector.block
                if detector.wheel is not None:
                    self.cell_wheel[set_cell] = detector.wheel
                if detector.positions:
                    nodes_mask = np.zeros(self.shape, dtype=bool)
                    for position in detector.positions:
                        node = (int(position[0]), int(position[1]), int(position[2]))
                        nodes_mask[node] = True
                        self.cell_index[node] = set_cell
                        self.absorbing[node] = True
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
                elif measured is not None and self.cell_measured[set_cell] is None:
                    self.cell_measured[set_cell] = measured
                self.cell_index[node] = set_cell
                self.absorbing[node] = True
            if set_cell is not None and detector.wheel is not None:
                self.cell_wheel[set_cell] = detector.wheel
        # The faces: an open face's layer is a cell that takes (light's
        # sponge); a periodic axis has none; a CLOSED face (detector-law-v1,
        # DECLARATIONS.md section 10's mirror B) is a zero face with no cell
        # and no take, the level 0 beyond it as `_shift` fills.
        for axis in range(3):
            if world.periodic[axis] or world.closed[axis] or self.shape[axis] < 2:
                continue
            for side, index in ((0, 0), (1, self.shape[axis] - 1)):
                cell = self._cell(FACE_NAMES[2 * axis + side], None, True)
                view = np.moveaxis(self.cell_index, axis, 0)[index]
                mask = np.moveaxis(self.absorbing, axis, 0)[index]
                free = view < 0
                view[free] = cell
                mask[:] = True
        self.records: dict[int, LiveRecord] = {}
        self.blocks: list[Block] = []
        self.block_by_number: dict[int, Block] = {}
        # The splitters of the TABLE form (build 2, component 3): their Nodes
        # take and book nothing; their outputs are driven from the read phase.
        self.splitters: list[Splitter] = []
        self.splitter_mask = np.zeros(self.shape, dtype=bool)
        for number, entry in enumerate(world.measured):
            for family, split in enumerate(entry.splits):
                if split is None or split.inputs is None:
                    continue
                node = (int(entry.position[0]), int(entry.position[1]), int(entry.position[2]))
                inputs = []
                for k, direction in enumerate(split.inputs):
                    vector = world.directions[direction]
                    weights, turns = split.weights[k], split.turns[k]
                    norm = sum(w * w for w in weights)
                    root = integer_root(norm)
                    if root * root != norm:
                        raise ValueError(
                            f"{BEAM_LAW}: measured[{number}].table: the split's row {list(weights)} has the "
                            f"norm {norm}, no square: under {DETECTOR_LAW_RULE} the splitter's isometry "
                            "divides by the root of the norm exactly (21, 20 against 29)"
                        )
                    source = (
                        (node[0] - int(vector[0])) % self.shape[0],
                        (node[1] - int(vector[1])) % self.shape[1],
                        (node[2] - int(vector[2])) % self.shape[2],
                    )
                    inputs.append((source, weights, turns, root))
                outputs: list[tuple[int, int, int]] = []
                for direction in entry.directions:
                    vector = world.directions[direction]
                    outputs.append(
                        (
                            (node[0] + int(vector[0])) % self.shape[0],
                            (node[1] + int(vector[1])) % self.shape[1],
                            (node[2] + int(vector[2])) % self.shape[2],
                        )
                    )
                self.splitters.append(Splitter(number, family, node, inputs, outputs))
                self.splitter_mask[node] = True
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
        # The rung W of every detector set: the lamps' birth wheels' largest
        # denominator, or the world key `wheel` where it is larger (a world
        # without a lamp, whose records a block emits, declares its W so;
        # RUN_LIST.md's light detectors at W = 64).
        self.wheel = max(
            (entry.lamp.wheel[1] for entry in world.measured if entry.lamp is not None),
            default=1,
        )
        self.wheel = max(self.wheel, world.wheel)
        for cell_number, _ in enumerate(self.cell_names):
            self.cell_wheel.setdefault(cell_number, self.wheel)
        self.cosine: dict[int, np.ndarray] = {}
        self.sine: dict[int, np.ndarray] = {}
        # The receivers' free neighbours per direction (for the one-way take):
        # for each of the six shifts, the absorbing Nodes whose neighbour on
        # that side is a free Node.
        self.take_masks: list[tuple[int, int, np.ndarray]] = []
        free = ~self.absorbing
        for axis in range(3):
            if self.shape[axis] == 1:
                continue
            for sign in (1, -1):
                neighbour_free = self._shift(free, axis, sign, fill=False)
                mask = self.absorbing & neighbour_free
                if mask.any():
                    self.take_masks.append((axis, sign, mask))
        self.take_count = np.zeros(self.shape, dtype=np.int64)
        for _, _, mask in self.take_masks:
            self.take_count += mask
        # The take's pair per Node (DECLARATIONS.md section 15, a declaration
        # of kind 2): light's [-15, 56] everywhere, an absorbing block's own
        # `take` at its cells (written with its pair, moved with it).
        self.take_num = np.full(self.shape, TAKE_NUMERATOR, dtype=np.int64)
        self.take_den = np.full(self.shape, TAKE_DENOMINATOR, dtype=np.int64)
        # The blocks (massive-record-v1): every measured event with a block,
        # its cells written into its kind's pair arrays, its own record
        # seeded on its cells, its momentum and the drive's wall 3 Q S M.
        for number, entry in enumerate(world.measured):
            if entry.block is None:
                continue
            definition = entry.block
            corner = [int(entry.position[axis]) for axis in range(3)]
            mask = self._cube(corner, definition.side, entry.family)
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
        # The blocks' cells: an absorbing block's cells take light's rows (the
        # first build's receivers); a clock body's cells and a wall's are
        # free Nodes for light with the pair and the coupling alone, so its
        # own cell (set by the measured event's Node above) is cleared from
        # the absorbing mask and the take masks are formed again.
        if self.blocks:
            for block in self.blocks:
                for node in zip(*np.nonzero(block.mask), strict=True):
                    address = (int(node[0]), int(node[1]), int(node[2]))
                    self.cell_index[address] = block.cell
                    self.absorbing[address] = block.definition.absorbing
            # a set bound to a block without positions: the block's cells are
            # the set's take Nodes, booked to the set's cell (line 7)
            for set_cell, number in self.set_block.items():
                if self.set_nodes[set_cell] is None:
                    block = self.block_by_number[number]
                    block.taking = True
                    self.cell_index[block.mask] = set_cell
                    self.absorbing[block.mask] = True
            self.take_masks = []
            free = ~self.absorbing
            for axis in range(3):
                if self.shape[axis] == 1:
                    continue
                for sign in (1, -1):
                    neighbour_free = self._shift(free, axis, sign, fill=False)
                    mask = self.absorbing & neighbour_free
                    if mask.any():
                        self.take_masks.append((axis, sign, mask))
            self.take_count = np.zeros(self.shape, dtype=np.int64)
            for _, _, mask in self.take_masks:
                self.take_count += mask

    def _cell(self, name: str, measured: int | None, face: bool) -> int:
        self.cell_names.append(name)
        self.cell_measured.append(measured)
        self.cell_face.append(face)
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

    def _cube(self, corner: list[int], side: int, family: int) -> np.ndarray:
        """The cells R of a block: the cube of `side` from its lower corner,
        wrapped on an axis the kind's faces make periodic, cut on an open
        one (a G_48-set of Nodes, world data)."""
        mask = np.zeros(self.shape, dtype=bool)
        wrap = self.kind_wrap[family]
        ranges = []
        for axis in range(3):
            extent = self.shape[axis]
            indices = [corner[axis] + offset for offset in range(side)]
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
        kind's own pair elsewhere on the Nodes the block left; an absorbing
        block's own take pair on its cells, light's where it left."""
        if block.definition.take is not None:
            self.take_num[~block.mask] = TAKE_NUMERATOR
            self.take_den[~block.mask] = TAKE_DENOMINATOR
            for other in self.blocks:
                if other is not block and other.definition.take is not None:
                    self.take_num[other.mask & ~block.mask] = other.definition.take[0]
                    self.take_den[other.mask & ~block.mask] = other.definition.take[1]
            self.take_num[block.mask] = block.definition.take[0]
            self.take_den[block.mask] = block.definition.take[1]
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
        block.mask = self._cube(block.corner, block.definition.side, block.family)
        self._write_pair(block)
        block.stepped += 1
        # The block's cell follows its cells: an absorbing block's take masks
        # move with it; a clock body's cells stay free Nodes.
        for node in zip(*np.nonzero(old_mask & ~block.mask), strict=True):
            address = (int(node[0]), int(node[1]), int(node[2]))
            self.cell_index[address] = -1
            self.absorbing[address] = False
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
            self.absorbing[address] = block.definition.absorbing or block.taking
        if block.definition.absorbing or block.taking:
            old_masks = self.take_masks
            self.take_masks = []
            free = ~self.absorbing
            for axis in range(3):
                if self.shape[axis] == 1:
                    continue
                for sign in (1, -1):
                    neighbour_free = self._shift(free, axis, sign, fill=False)
                    mask = self.absorbing & neighbour_free
                    if mask.any():
                        self.take_masks.append((axis, sign, mask))
            # THE HOP RULE OF THE MOVING TAKE (DECLARATIONS.md section 13 item
            # 4, declared 04:20Z): at a hop the face's Port is a NEW Port whose
            # ghost starts at its free neighbour's own level (no jump booked; a
            # Port that persists keeps its ghost); the content of a Node the
            # set steps into is taken that interval, its motion squared booked
            # to the set's pointer and to `absorbed` before its row is held at
            # 0; no stale ghost is carried across the hop. The block's own
            # record in its grace is exempt (its row evolves at the cells).
            entered = block.mask & ~old_mask
            for live in self.records.values():
                if not live.ports:
                    continue
                exempt = live.emitter == block.number and self._in_grace(live)
                ports = []
                for axis, sign, mask in self.take_masks:
                    kept = next(
                        (
                            old
                            for old_axis, old_sign, old in old_masks
                            if old_axis == axis and old_sign == sign
                        ),
                        None,
                    )
                    old_index = next(
                        (
                            i
                            for i, (old_axis, old_sign, _) in enumerate(old_masks)
                            if old_axis == axis and old_sign == sign
                        ),
                        None,
                    )
                    fresh = np.where(mask, self._shift(live.now, axis, sign), 0)
                    if kept is not None and old_index is not None and old_index < len(live.ports):
                        fresh = np.where(mask & kept, live.ports[old_index], fresh)
                    ports.append(fresh)
                live.ports = ports
                if exempt or not entered.any():
                    continue
                motion = np.where(entered, live.now - live.before, 0).astype(object)
                value = int(np.sum(motion * motion))
                cell = block.cell if set_cell is None else set_cell
                if value:
                    live.pointers[cell] += value
                    live.absorbed += value
                    if (
                        live.first_rung[cell] is None
                        and live.pointers[cell] * self.cell_wheel[cell] >= live.norm
                    ):
                        live.first_rung[cell] = self.tick
                        if cell in self.set_block:
                            self.rung_counts[(live.identity, cell)] = block.count
                live.now[entered] = 0
                live.before[entered] = 0

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
        difference at its cells (an absorbing block reads its Ports' motion,
        the field its cells read); in motion g carried as the drive's pair;
        the term 3 den g_n pair_n x delta against the wall 3 den g_d pair_d."""
        if block.definition.absorbing or block.taking:
            delta = light.port_motion if light.port_motion is not None else np.zeros_like(light.now)
        else:
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

    def _block_births(self) -> None:
        """A block that emits births one light record at each new cycle of its
        clock, paying the family's quantum from its held content (as a lamp
        does); the record's rows are sourced by the block's own current at
        its cells while the cycle lasts."""
        world = self.world
        for block in self.blocks:
            if not block.new_cycle:
                continue
            block.new_cycle = False
            family = block.definition.emits
            if family is None or block.own is None:
                continue
            # The emission is the coupling's source term: the record is born
            # at content 0 and consumes no stock (DECLARATIONS.md section 15
            # M1-2; the books balance with 0 content as a response's do).
            cost = 0
            block.births += 1
            identity = block.number * (1 << 32) + block.births
            definition = self.families[family]
            assert definition.phase_per_age is not None
            numerator, denominator = definition.phase_per_age
            # No train and no grace: the block's cells are no lamp's Nodes
            # (the record is sourced at the cells by the block's current,
            # not driven), so the record's period and train are 0 and its
            # completion waits on the cycle's end (`sourcing`).
            live = LiveRecord(
                identity,
                block.number,
                family,
                0,
                block.births,
                self.tick,
                cost,
                numerator,
                denominator,
                0,
                0,
                np.zeros(self.shape, dtype=np.int64),
                np.zeros(self.shape, dtype=np.int64),
                np.zeros(self.shape, dtype=np.int64),
                pointers=[0] * len(self.cell_names),
                first_rung=[None] * len(self.cell_names),
                ports=[np.zeros(self.shape, dtype=np.int64) for _ in self.take_masks],
                emitter=block.number,
                sourcing=True,
            )
            live.driven = np.zeros(self.shape, dtype=bool)
            if block.current is not None and block.current in self.records:
                previous = self.records[block.current]
                previous.sourcing = False
                previous.train = previous.age
                previous.period = block.cycle_length
            block.current = identity
            block.emitted.append(identity)
            self.records[identity] = live
            self.layer.born += 1
            if self.record is not None:
                self.record(
                    {
                        "event": "birth",
                        "tick": self.tick,
                        "node": list(block.corner),
                        "measured": block.number,
                        "family": definition.name,
                        "record": identity,
                        "u": 0,
                        "labels": [[0, 1]],
                        "arms": 1,
                        "units": 1,
                        "multiplicity": 1,
                        "train": 0,
                        "cycle": block.count,
                        **({"clock": block.count} if world.clock_stamp else {}),
                    }
                )

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
            (block.corner[axis] + block.definition.side // 2) % self.shape[axis] for axis in range(3)
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

    def _book_response(self, block: Block, response: LiveRecord, light: LiveRecord) -> None:
        """The click's pointer at a clock body: the response's motion across
        the cells (the evaluation E of the object's record across R) added
        to the light record's pointer for the block's cell, the first rung
        at 1 / W of the record's norm stamped with the block's count; an
        absorbing block books its Ports' offer as built and nothing here."""
        if block.definition.absorbing or block.taking:
            return
        if light.emitter == block.number and self._in_grace(light):
            return
        motion = (response.now - response.before).astype(object)
        value = int(np.sum(np.where(block.mask, motion * motion, 0)))
        if value == 0:
            return
        cell = block.cell
        light.pointers[cell] += value
        light.absorbed += value
        wheel = block.definition.wheel if block.definition.wheel is not None else self.wheel
        if light.first_rung[cell] is None and light.pointers[cell] * wheel >= light.norm:
            light.first_rung[cell] = self.tick
            self.rung_counts[(light.identity, cell)] = block.count

    # The source

    def _sine_table(self, steps: int) -> np.ndarray:
        """The sine table of the circle (`core.phase.phase_sines`, sin x 256,
        immutable law data) as an integer array, formed once: the linear
        form's coefficients (DECLARATIONS.md section 14)."""
        if steps not in self.sine:
            self.sine[steps] = np.array(phase_sines(steps), dtype=np.int64)
        table: np.ndarray = self.sine[steps]
        return table

    def _cosine_table(self, steps: int) -> np.ndarray:
        """The clock's cosine on the amplitude unit: the phase circle's integer
        table (`core.phase.phase_cosines`, cos x 256, immutable law data)
        scaled to UNIT, formed once."""
        if steps not in self.cosine:
            factor = UNIT // PHASE_COSINE_SCALE
            self.cosine[steps] = np.array([c * factor for c in phase_cosines(steps)], dtype=np.int64)
        table: np.ndarray = self.cosine[steps]
        return table

    def _births(self) -> None:
        world = self.world
        for number in self.lamp_nodes:
            entry = world.measured[number]
            lamp = entry.lamp
            assert lamp is not None
            family = entry.family
            definition = world.families[family]
            cost = definition.quantum
            rate_numerator, rate_denominator = lamp.rate
            self.lamp_accumulator[number] += rate_numerator
            while (
                self.lamp_accumulator[number] >= rate_denominator and self.held[number][family] >= cost
            ):
                self.lamp_accumulator[number] -= rate_denominator
                ordinal = self.lamp_births[number] + 1
                self.lamp_births[number] = ordinal
                u = (ordinal - 1) * lamp.wheel[0] % lamp.wheel[1]
                if number in self.birth_orders:
                    # the seed-set order: u = order[(ordinal - 1) mod W], one
                    # residue per birth over W births (the stride 1 at load)
                    u = self.birth_orders[number][(ordinal - 1) % lamp.wheel[1]]
                identity = number * (1 << 32) + ordinal
                pair = definition.phase_per_age
                if pair is None:
                    raise ValueError(
                        f"{BEAM_LAW}: {DETECTOR_LAW_RULE} needs the pair form of phase_per_link on the family "
                        f"{definition.name!r} (its clock)"
                    )
                numerator, denominator = pair
                steps = world.phase_steps
                if steps % 4:
                    raise ValueError(
                        f"{BEAM_LAW}: {DETECTOR_LAW_RULE} needs N divisible by 4 (the clock's zero)"
                    )
                if numerator <= 0:
                    raise ValueError(
                        f"{BEAM_LAW}: {DETECTOR_LAW_RULE} needs a positive clock on the family {definition.name!r}"
                    )
                # The period in intervals, N d / n, its ceiling as an integer.
                period = (steps * denominator + numerator - 1) // numerator
                train_periods = lamp.train if lamp.train is not None else DEFAULT_TRAIN
                # The train begins at the clock's zero (the phase 3 N / 4, the
                # cosine 0 and rising) and ends at the first zero after the
                # declared periods, so that the insertion starts and stops
                # smoothly: a step in the inserted amplitude would leave a
                # static level on the board (the wave's zero-frequency mode),
                # which no receiver takes.
                train = max(1, (train_periods * steps * denominator + numerator - 1) // numerator)
                while self._phase(train, numerator, denominator, steps) not in (
                    steps // 4,
                    3 * steps // 4,
                ):
                    train += 1
                self.held[number][family] -= cost
                self.ledger.held_spent[family] += cost
                self.ledger.transit_released[family] += cost
                # The pair's arms (build 2, component 2): one record per arm on
                # this birth stamp; the pair's one quantum is carried by arm 0
                # (the joint click books it once, the table rows' gather), the
                # other arms carry 0; each arm's row is confined to the
                # half-space of its first direction from the lamp's Node.
                per_arm = len(lamp.directions) // lamp.arms if lamp.arms > 1 else 0
                identities = []
                for arm in range(lamp.arms):
                    arm_identity = identity + (arm << 24) if lamp.arms > 1 else identity
                    identities.append(arm_identity)
                    live = LiveRecord(
                        arm_identity,
                        number,
                        family,
                        u,
                        ordinal,
                        self.tick,
                        cost if arm == 0 else 0,
                        numerator,
                        denominator,
                        train,
                        period,
                        np.zeros(self.shape, dtype=np.int64),
                        np.zeros(self.shape, dtype=np.int64),
                        np.zeros(self.shape, dtype=np.int64),
                        pointers=[0] * len(self.cell_names),
                        first_rung=[None] * len(self.cell_names),
                        ports=[np.zeros(self.shape, dtype=np.int64) for _ in self.take_masks],
                        arm=arm,
                        arms=lamp.arms,
                        labels=tuple(lamp.branches),
                    )
                    if lamp.arms > 1:
                        vector = world.directions[lamp.directions[arm * per_arm]]
                        live.mask = self._half_space(entry.position, vector)
                    driven = np.zeros(self.shape, dtype=bool)
                    for node in self.lamp_nodes[number]:
                        driven[node] = True
                    live.driven = driven
                    # The record's norm: the offer its train inserts (the squared
                    # amplitudes over the train at the lamp's Nodes), the wheel's
                    # rungs divide it; the first rung of a cell is the click's time.
                    table = self._cosine_table(world.phase_steps)
                    # The record's norm: the motion its train inserts (the squared
                    # steps of the driven amplitude over the train at the lamp's
                    # Nodes); the wheel's rungs divide it, the first rung of a cell
                    # is the click's time.
                    values = [
                        int(table[self._phase(t, numerator, denominator, steps)])
                        for t in range(train + 1)
                    ]
                    values[-1] = 0
                    live.norm = len(self.lamp_nodes[number]) * sum(
                        (values[t + 1] - values[t]) ** 2 for t in range(train)
                    )
                    self.records[arm_identity] = live
                self.layer.born += 1
                if self.record is not None:
                    self.record(
                        {
                            "event": "birth",
                            "tick": self.tick,
                            "node": list(entry.position),
                            "measured": number,
                            "family": definition.name,
                            "record": identity,
                            "u": u,
                            "labels": [list(branch) for branch in lamp.branches],
                            "arms": lamp.arms,
                            **({"arm_records": identities} if lamp.arms > 1 else {}),
                            "units": 1,
                            "multiplicity": 1,
                            "train": train,
                            **({"clock": self.tick} if world.clock_stamp else {}),
                        }
                    )

    @staticmethod
    def _phase(age: int, numerator: int, denominator: int, steps: int) -> int:
        """The record's clock at its age: the zero (3 N / 4) advanced by the
        whole part of age x n / d on the circle of N steps."""
        return (3 * steps // 4 + age * numerator // denominator) % steps

    def _drive(self, live: LiveRecord) -> None:
        """The record's clock at the lamp's Nodes for the train."""
        if live.age >= live.train:
            return
        steps = self.world.phase_steps
        phase = self._phase(live.age, live.period_numerator, live.period_denominator, steps)
        value = int(self._cosine_table(steps)[phase])
        for node in self.lamp_nodes[live.lamp]:
            live.now[node] = value

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

    def _neighbours(
        self,
        a: np.ndarray,
        ports: list[np.ndarray] | None = None,
        driven: np.ndarray | None = None,
        wrap: tuple[bool, bool, bool] | None = None,
    ) -> np.ndarray:
        """The sum of the six neighbours' amplitudes at every Node (verb G):
        the wrap on a periodic axis, 0 beyond an open face (light's sponge
        face or a massive kind's zero face), the row itself on an axis of
        one layer; a receiver neighbour read through its Port's amplitude
        (`ports`, one per take mask) where one is given; `wrap` the kind's
        faces (the world's by default)."""
        total = np.zeros_like(a)
        for axis in range(3):
            if self.shape[axis] == 1:
                total += 2 * a
                continue
            for sign in (1, -1):
                source = a
                if ports is not None:
                    for index, (mask_axis, mask_sign, mask) in enumerate(self.take_masks):
                        # The receiver r with a free neighbour on its -mask_sign side
                        # (the mask) is read by that neighbour as the +mask_sign
                        # neighbour of the free Node: the shift by -mask_sign.
                        if mask_axis == axis and mask_sign == -sign:
                            read = mask if driven is None else (mask & ~driven)
                            source = np.where(read, ports[index], source)
                total += self._shift(source, axis, sign, wrap=wrap)
        return total

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
        # The inserter's own Nodes are driven for the train and read their own
        # record only after its tail has left them (two periods after the
        # train; the first build's grace, DESIGN.md section 11): a receiver's
        # Port books the wave's motion beside it, and the tail leaving the
        # lamp is not an arrival.
        # Line B (Reviewer 3, DECLARATIONS.md section 10's cycle sentence): a
        # BLOCK'S emitted record has the same grace, its driven set the
        # block's current cells while the block sources it and for two of
        # the block's periods after the cycle's end, the offer dropped at the
        # block's own cell; the first rung after the grace is the receive.
        in_grace = self._in_grace(live)
        driven = self._driven(live) if in_grace else None
        # the sets bound to the emitting block are FREE for its own record
        # during the record's grace (line 7; DECLARATIONS.md section 10 item
        # 9): no take, no zero, the row evolving there
        exempt = self._exempt(live) if in_grace else None
        if exempt is not None:
            driven = exempt if driven is None else (driven | exempt)
        # The take (the receivers' Ports, the faces' sponge) reads every
        # LAMP'S record, light's kind or a massive kind alike (the click is
        # the law's one action on any record, POSTULATES 10; Reviewer 3's
        # line on the matter lamp): a BLOCK'S massive record (den > num,
        # born of no lamp) is taken by nothing and reads no Port, its faces
        # its own (massive-record-v1; DESIGN.md section 5, MASSIVE_RECORD.md
        # section 7, MUST 2: no take for a clock body, the sink a
        # declaration on light's row).
        taken = not self.families[live.family].massive_kind or live.driven is not None
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
        neighbours = self._neighbours(
            live.now, live.ports if taken else None, driven, self.kind_wrap[live.family]
        )
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
        if not taken:
            live.before = live.now
            live.now = nxt
            live.age += 1
            # A matter lamp's record is driven at the lamp's Nodes for its
            # train as light's (the same verb at the family's clock; a
            # block's record has no train and is driven by nothing here).
            self._drive(live)
            return
        ended: list[tuple[int, int]] = []
        if exempt is None:
            if live.was_exempt:
                # The grace's end (Reviewer 3's line on 906d3635): the set
                # Nodes' own row, which evolved freely, is taken now as the
                # hop rule takes an entered Node's content: this interval's
                # motion there squared, booked to the set's pointer and to
                # `absorbed` below, before the row is held at 0.
                freed = self._exempt(live)
                if freed is not None:
                    motion = np.where(freed, nxt - live.now, 0).astype(object)
                    for node in zip(*np.nonzero(freed), strict=True):
                        ended.append((int(self.cell_index[node]), int(motion[node]) ** 2))
                live.was_exempt = False
            nxt[self.absorbing] = 0
        else:
            live.was_exempt = True
            nxt[self.absorbing & ~exempt] = 0
        if live.mask is not None:
            # the arm's row lives on its own side of the lamp (component 2)
            nxt[~live.mask] = 0
        port_motion = np.zeros(self.shape, dtype=np.int64) if self.blocks else None
        # The receivers: each Port facing a free Node follows the wave entering
        # by it one way (the take, no reflection); the offer booked to the cell
        # is the sum over the Ports of the squared Port amplitudes. The
        # record's own lamp is driven during its train and receives nothing
        # from that record then.
        offer = np.zeros(self.shape, dtype=np.int64)
        for index, (axis, sign, mask) in enumerate(self.take_masks):
            free_now = self._shift(live.now, axis, sign)
            free_next = self._shift(nxt, axis, sign)
            ghost = np.floor_divide(
                self.take_den * free_now + self.take_num * (free_next - live.ports[index]),
                self.take_den,
            )
            ghost = np.where(mask if driven is None else (mask & ~driven), ghost, 0)
            if exempt is not None:
                # A set's Port free for its block's own record (line 7): its
                # ghost follows the free neighbour's level and books no
                # motion, so the Port's take at the grace's end starts at
                # that level with no jump booked (the hop rule's principle,
                # DECLARATIONS.md section 13 item 4: no stale ghost carried).
                ghost = np.where(mask & exempt, free_next, ghost)
            # The offer arriving by the Port is the Port's motion, (g(t + 1) -
            # g(t))^2: a wave moves the receiver, a static level on the board
            # (the rule's zero-frequency mode, which no receiver takes and
            # which carries nothing) does not.
            motion = ghost - live.ports[index]
            if exempt is not None:
                motion[exempt] = 0
            live.ports[index] = ghost
            offer += motion * motion
            if port_motion is not None:
                port_motion += motion
        live.port_motion = port_motion
        live.before = live.now
        # a splitter's Node takes and books nothing (component 3)
        offer[self.splitter_mask] = 0
        offer = offer[self.absorbing]
        cells = self.cell_index[self.absorbing]
        if in_grace:
            own = (
                np.array(
                    [self.block_by_number[live.emitter].cell]
                    + [cell for cell, number in self.set_block.items() if number == live.emitter]
                )
                if live.emitter is not None
                else self.cell_index[tuple(zip(*self.lamp_nodes[live.lamp], strict=True))]
            )
            keep = ~np.isin(cells, own)
            offer = offer[keep]
            cells = cells[keep]
        squares = offer.astype(object)
        for cell, value in list(zip(cells.tolist(), squares.tolist(), strict=True)) + ended:
            if value:
                live.pointers[cell] += int(value)
                live.absorbed += int(value)
                if (
                    live.first_rung[cell] is None
                    and live.pointers[cell] * self.cell_wheel[cell] >= live.norm
                ):
                    live.first_rung[cell] = self.tick
                    if cell in self.set_block:
                        # the click of a set bound to a block is stamped with
                        # the block's own count as the interval begins
                        self.rung_counts[(live.identity, cell)] = self.block_by_number[
                            self.set_block[cell]
                        ].count
        live.now = nxt
        self._drive(live)
        self._split(live)

    def read_pair(self, live: LiveRecord, node: tuple[int, int, int], turn: int) -> int:
        """The table's action on a record's pair at a Node by the linear form
        of DECLARATIONS.md section 14 item 1 (the polariser's rotation U_s
        on the record's two columns, section 15 T-1): the level A cos(phi + t)
        = (a_now S[k + t] - a_before S[t]) / S[k] at the turn t, S the sine
        table and k the interval's own whole step of the record's clock
        (`by_clock`), one division, the remainder dropped (a reading, not a
        row); the click's weights of ALGEBRA.md 4.12 are the table's own and
        unchanged. A record of a massive kind born of no lamp has no clock
        and reads 0."""
        if self.families[live.family].massive_kind and live.driven is None:
            return 0
        steps = self.world.phase_steps
        sines = self._sine_table(steps)
        k = by_clock(max(live.age - 1, 0), live.period_numerator, live.period_denominator)
        s_k = int(sines[k % steps])
        if s_k == 0:
            raise ValueError(
                f"{BEAM_LAW}: the record's clock step {k} of {steps} has a sine of 0; the linear "
                "form divides by S[k] (DECLARATIONS.md section 14)"
            )
        now = int(live.now[node])
        before = int(live.before[node])
        return (now * int(sines[(k + turn) % steps]) - before * int(sines[turn % steps])) // s_k

    def _in_grace(self, live: LiveRecord) -> bool:
        """The record's grace: its train and two periods after it (a lamp's
        record); for a block's emitted record the cycle it is sourced in and
        two of the block's periods after the cycle's end (line B)."""
        if live.emitter is not None and live.sourcing:
            return True
        if live.emitter is not None:
            # the emitter's declared own_grace (N_s), required at load
            declared = self.block_by_number[live.emitter].definition.own_grace
            return live.age < live.train + (declared if declared is not None else 0)
        measured = self.world.measured
        lamp = measured[live.lamp].lamp if 0 <= live.lamp < len(measured) else None
        if lamp is not None and lamp.own_grace is not None:
            # a lamp's declared own_grace (the matter lamp's whole hold, M1-6)
            return live.age < live.train + lamp.own_grace
        return live.age < live.train + 2 * live.period

    def _exempt(self, live: LiveRecord) -> np.ndarray | None:
        """The Nodes of the sets bound to the record's emitting block: free for
        the block's own record during its grace (the declared Nodes, or the
        block's current cells); None for a record with no such set."""
        if live.emitter is None:
            return None
        found: np.ndarray | None = None
        for cell, number in self.set_block.items():
            if number != live.emitter:
                continue
            nodes = self.set_nodes[cell]
            mask = self.block_by_number[number].mask if nodes is None else nodes
            found = mask.copy() if found is None else (found | mask)
        return found

    def _driven(self, live: LiveRecord) -> np.ndarray | None:
        """The Nodes the record's own object holds during its grace: the lamp's
        Nodes, or the emitting block's CURRENT cells (a stepping block's follow
        it)."""
        if live.emitter is not None:
            return self.block_by_number[live.emitter].mask
        return live.driven

    def _split(self, live: LiveRecord) -> None:
        """The splitters' action on a light record after its step (component
        3; DECLARATIONS.md section 14): the linear form on the record's pair
        at each input Node, the outputs' terms added to the rule's values
        with the remainder carried (the `Splitter` docstring)."""
        if self.splitters:
            steps = self.world.phase_steps
            sines = self._sine_table(steps)
            # The pair at a Node after the step is (the level at age - 1, the
            # level at age): the clock's step between them is what the floor
            # of age x n / d gained at the interval that took the age from
            # age - 1 to age (`by_clock`; at the first interval the pair is
            # (0, the first level) and the step is the first interval's).
            k = by_clock(max(live.age - 1, 0), live.period_numerator, live.period_denominator)
            s_k = int(sines[k % steps])
            for splitter in self.splitters:
                if splitter.family != live.family or s_k == 0:
                    continue
                common = 1
                for _, _, _, root in splitter.inputs:
                    common = common * root // gcd(common, root)
                wall = s_k * common
                remainders = splitter.remainders.setdefault(live.identity, [0] * len(splitter.outputs))
                totals = [0] * len(splitter.outputs)
                for source, weights, turns, root in splitter.inputs:
                    now = int(live.now[source])
                    before = int(live.before[source])
                    if now == 0 and before == 0:
                        continue
                    factor = common // root
                    for j, (weight, turn) in enumerate(zip(weights, turns, strict=True)):
                        totals[j] += (
                            weight
                            * factor
                            * (now * int(sines[(k + turn) % steps]) - before * int(sines[turn % steps]))
                        )
                for j, output in enumerate(splitter.outputs):
                    quotient, remainders[j] = divmod(totals[j] + remainders[j], wall)
                    live.now[output] += quotient
        live.age += 1

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

    def _complete(self, live: LiveRecord) -> bool:
        """The record completes when its train has ended and the motion left on
        the board (the squared steps of every row, the wave's energy in the
        rule's own terms; a static level moves nothing) is below one rung of
        what the receivers hold."""
        if live.sourcing or live.age <= live.train:
            return False
        # A block's massive record never completes and is never clicked as
        # escaped (Reviewer 3's MUST 2 on step 2): its rows are the block's
        # own, read by the block's clock, taken by nothing. A lamp's record
        # of a massive kind completes and clicks as light's.
        if self.families[live.family].massive_kind and live.driven is None:
            return False
        motion = (live.now - live.before).astype(object)
        energy = int(np.sum(motion * motion))
        if live.absorbed == 0:
            return energy == 0 and live.age > live.train + 2
        return energy * self.wheel < live.absorbed

    def _click(self, live: LiveRecord) -> None:
        weights = [(p, 1) for p in live.pointers]
        chosen = cell_of(weights, self.wheel, live.u) if live.absorbed else None
        family = live.family
        ladder, total = rungs(weights, self.wheel)
        if chosen is None:
            self.ledger.transit_escaped[family] += live.content
            self.ledger.held_escaped[family] += 0
            name = None
        else:
            name = self.cell_names[chosen]
            measured = self.cell_measured[chosen]
            if measured is not None and not self.cell_face[chosen]:
                self.held[measured][family] += live.content
                self.ledger.held_measured[family] += live.content
                self.ledger.transit_absorbed[family] += live.content
            else:
                self.ledger.transit_escaped[family] += live.content
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
            "born": live.born,
            "chosen": [[name, 0, "0"]] if name is not None else None,
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
                [[[cell_name, 0, "0"]], rung]
                for cell_name, rung, pointer in zip(self.cell_names, ladder, live.pointers, strict=True)
                if pointer
            ],
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
        for splitter in self.splitters:
            splitter.remainders.pop(live.identity, None)
        for block in self.blocks:
            block.responses.pop(live.identity, None)
            if live.identity in block.emitted:
                block.emitted.remove(live.identity)
            if block.current == live.identity:
                block.current = None
        for key in [key for key in self.rung_counts if key[0] == live.identity]:
            del self.rung_counts[key]
        self.layer.gathers.append(gather)
        if self.record is not None:
            self.record(gather)

    def step(self) -> None:
        self.tick += 1
        self._births()
        self._block_births()
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
        for identity in list(self.records):
            live = self.records[identity]
            if self.families[live.family].massive_kind:
                # A block's massive record is advanced with its block above;
                # a matter lamp's record (a massive kind with a declared
                # clock, born of a lamp) is advanced by the rule with the
                # family's pair alone, through the take and the detector
                # sets' pointers as light's (the click at W, one per record),
                # coupled to no block (the coupling is declared on light's
                # row, MASSIVE_RECORD.md section 7), its faces the kind's
                # (a zero face a mirror).
                if live.driven is not None:
                    self._advance(live)
                continue
            sources: np.ndarray | None = None
            if self.blocks:
                sources = np.zeros(self.shape, dtype=np.int64)
            for block in self.blocks:
                if live.emitter == block.number:
                    if block.current == identity and block.own is not None and sources is not None:
                        term = self._source(block, block.own, live)
                        sources += term
                        added = np.floor_divide(term, 3 * self.kind_den[live.family] * self.light_scale)
                        live.norm += int(np.sum(added.astype(object) * added.astype(object)))
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
                self._book_response(block, response, live)
                if sources is not None:
                    sources += self._source(block, response, live)
            self._advance(live, sources, self.light_scale)
        for block in self.blocks:
            self._block_clock(block)
        for identity in list(self.records):
            live = self.records[identity]
            if self.families[live.family].massive_kind and live.driven is None:
                continue
            if self._complete(live):
                self._click(live)
                del self.records[identity]
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

    def read_phase(
        self, live: LiveRecord, node: tuple[int, int, int], amplitude: int | None = None
    ) -> tuple[int, int] | None:
        """The phase reading of a record at a Node (the TABLE form's input,
        DECLARATIONS.md's head): the angle on the world's circle nearest
        to the pair (a_before, a_now) at the Node at the record's clock and
        amplitude, with the reading's residual (`core.phase.nearest_phase`);
        the amplitude the lamp's unit by default (the level the clock drives,
        UNIT: exact on a bar, where the train keeps its amplitude), or the
        amplitude the reader declares (a table Node's peak register on a
        board where the wave spreads); None where the record has no level
        at the Node. A block's massive record has no clock on the circle and
        is not read; a matter lamp's record is read at the family's clock as
        light's (a GAMEBOARD diagnostic: the tables act on the pair by the
        linear form, DECLARATIONS.md section 14, not on this reading)."""
        if self.families[live.family].massive_kind and live.driven is None:
            return None
        return nearest_phase(
            int(live.before[node]),
            int(live.now[node]),
            UNIT if amplitude is None else amplitude,
            (live.period_numerator, live.period_denominator),
            self.world.phase_steps,
        )

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
            }
            transit["balanced"] = transit["released"] == (
                transit["current"] + transit["absorbed"] + transit["escaped"]
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
