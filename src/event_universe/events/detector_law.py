"""The engine (one engine, no law's name and no version, ALGEBRA.md #the-primitives;
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

from collections.abc import Callable
from math import gcd
from typing import cast

import numpy as np

from event_universe.core.game_board import box_centre
from event_universe.core.main_loop import MainLoop, Stage, read_only
from event_universe.core.ports import Ports, port_of
from event_universe.core.register import Register, discover
from event_universe.core.rule3 import (
    ISOTROPIC,
    NO_READ,
    SPAN,
    THE_ADVANCE,
    THE_INVERSE,
    THE_REWRITE,
    THE_UNHOLD,
    coefficients,
    form_term,
    rule3,
)
from event_universe.events import assembly, guards, output
from event_universe.events import live as live_records
from event_universe.events.geometry import GameBoardGeometry, PairView
from event_universe.events.output import ZERO, Ratio, ratio, ratio_sum
from event_universe.events.output import form_json as form_json
from event_universe.events.records import Block, DetectorLawLayer, Ledger, LiveRecord, NodeRecord
from event_universe.features import self_source
from event_universe.features import signed_read as sr
from event_universe.features.counts_line import CountStart, CountTerm, CountWrites, Levels
from event_universe.features.giving import (
    THE_CLOSE,
    THE_OPEN,
    THE_WRITE,
    GivingOwn,
    GivingStart,
    GivingTerm,
    GivingWrites,
)
from event_universe.features.hold import HoldOwn, HoldStart, HoldTerm, HoldWrites, booking
from event_universe.features.receive import Link, ReceiveStart, ReceiveTerm, ReceiveWrites, TwistRead
from event_universe.features.source import SourceOwn, SourceStart, SourceTerm, SourceWrites
from event_universe.features.spins_step import (
    KEYS,
    SpinRead,
    SpinStepOwn,
    SpinStepStart,
    SpinStepTerm,
    SpinStepWrites,
)
from event_universe.loader.world import (
    AXES,
    BlockDefinition,
    MeasuredDefinition,
    NatureBeamWorld,
    TwistTable,
)

Record = Callable[[dict[str, object]], None]

# ONE ENGINE, NO LAW'S NAME AND NO VERSION (ALGEBRA.md #the-primitives): the constant that named the law and its version is CANCELLED; the books and the state carry no law entry
FACE_NAMES = ("face:-x", "face:+x", "face:-y", "face:+y", "face:-z", "face:+z")
# The receiver's take (DESIGN.md sections 1 and 5): a Node that receives does not send the wave back (a mirror is a receiver body that re-emits, never a wall). The record's row at a receiver holds one amplitude per Port that faces a free Node (the NodeState's Ports), the wave entering by that Port, following it one way: g(t + 1) = a_f(t) + k (a_f(t + 1) - g(t)) with a_f the free neighbour's amplitude and k = (c - 1) / (c + 1) at c = 1 / sqrt 3, the declared pair [-15, 56] (-0.2679 against sqrt 3 - 2 = -0.2679), a rounding declared at load, not a root at run time; the free neighbour reads g as the receiver's amplitude on that Link, and the receiver books g^2 as the offer arriving by that Port.


class DetectorLawSimulation(GameBoardGeometry[Block]):
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

    # a body's records' identities: the body's number times the stride, its own record at giving 0
    OWN_IDENTITY_STRIDE = 1 << 32

    # The state the assembly fills once from the parsed world (`events/assembly.py`): the names and types
    held: list[list[int]]
    detector_names: list[str]
    detector_measured: list[int | None]
    detector_face: list[bool]
    detector_set: list[str]
    detector_channel: list[int]
    detector_at_node: np.ndarray
    _inflow_port_pairs: dict[int, tuple[np.ndarray, np.ndarray, np.ndarray]]
    _inflow_port_faces: dict[int, tuple[np.ndarray, np.ndarray]]
    set_block: dict[int, int]
    set_detectors: list[int]
    set_nodes: dict[int, np.ndarray | None]
    face_detector: int | None
    momentum_unit: int
    twist_table: TwistTable | None
    _fine: np.ndarray
    _coarse: np.ndarray
    _receive_term: ReceiveTerm
    _sources: dict[tuple[int, bool], tuple[int, np.ndarray]]
    node_clock: int
    held_families: list[int]
    family_charge: list[int]
    node_level: dict[int, np.ndarray]
    _effective: dict[int, np.ndarray]
    _pace_carry: dict[tuple[int, int, int], np.ndarray]
    _axis_effective: dict[int, tuple[int, bool, tuple[np.ndarray, ...] | None]]
    _sourced_ever: dict[tuple[int, int], bool]
    span_masks: dict[int, np.ndarray]
    records: dict[int, LiveRecord]
    _kind_walls: dict[tuple[int, int, int], int]
    dead: list[int]
    blocks: list[Block]
    block_by_number: dict[int, Block]
    rung_counts: dict[tuple[int, int], int]
    _pairs: dict[tuple[int, int, int], tuple[np.ndarray, np.ndarray]]
    kind_wrap: list[tuple[bool, bool, bool]]
    receiver_detector: dict[int, int]
    has_receiver: bool
    held_records: dict[int, LiveRecord]
    held_parts: dict[int, list[LiveRecord]]
    sourced_records: dict[int, LiveRecord]
    _source_argument: dict[int, np.ndarray]
    _source_remainders: dict[int, np.ndarray]

    def __init__(self, world: NatureBeamWorld, observer: Record | None = None) -> None:
        self.world = world
        self.record = observer
        self.tick = 0
        self.shape = tuple(int(n) for n in world.shape)
        self.ports = Ports(world.periodic)
        self.families = world.families
        self.fast_steps = 0
        self.hypotheses = list(world.hypotheses)
        self.layer = DetectorLawLayer()
        self.held = assembly.held_table(world)
        count = len(world.families)
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
        # the state built once from the parsed world, in this order (`events/assembly.py`)
        assembly.detectors(self, world)
        assembly.universe_values(self, world)
        assembly.state_arrays(self, world)
        self.kind_num = PairView(self, 0)
        self.kind_den = PairView(self, 1)
        assembly.bodies(self, world)
        assembly.held_records(self)
        # the register: the folders' primitives by name, the step file's acts bound to the loop's stages
        self.register = self._engine_register()
        self.register.check_step(world.step)
        self.register.check_writers(world.step)
        self.register.check_terms(self.family_terms())
        self.main_loop = MainLoop.plan(
            self.register, world.step, self._stages(), self.CHAIN, self.family_terms()
        )
        self._hold(self.register.at("the hold", "(iv)"), advance=True)

    def _block(
        self,
        number: int,
        entry: MeasuredDefinition,
        definition: BlockDefinition,
        corner: list[int],
        mask: np.ndarray,
    ) -> Block:
        # a body's block from its measured entry: its Nodes, the detector under its position, its momentum, its spin
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
        return block

    def _node_record(self, identity: int, level: int) -> NodeRecord:
        # a body's record at its centre Node: the profile's level at both levels, the remainder 0
        return NodeRecord(identity, level, level)

    # The register of primitives: one register, name to function, read by the loop alone

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

    def _stages(self) -> dict[str, Stage]:
        """The loop's whole-board stages by the file's names, each with the words it takes and the cards whose writes it carries (the records' pass carries the chain's cards but the clicks, whose act is nested in it)."""
        chain = tuple(name for name in self.CHAIN if name != "the clicks")
        return {
            "the count's line": Stage(self._counts_stage, (), ("the count's line", "the hop")),
            "the hold": Stage(self._hold_stage, ("advance",), ("the hold",)),
            "the operation": Stage(self._records_stage, (), chain),
            "the giving": Stage(self._giving_stage, (), ("the giving",), creates=True),
            "the source": Stage(self._source_stage, (), ("the source",)),
            "the spin's step": Stage(self._spins_stage, (), ("the spin's step",)),
        }

    _card_writes = guards.card_writes
    start_arrays = guards.start_arrays
    grants = guards.grants
    apply_write = guards.apply_write
    term_of = guards.term_of
    start_view = guards.start_view
    own_of = guards.own_of
    _guard = guards.guard_paces

    fingerprints_of = live_records.fingerprints_of
    fingerprints = live_records.fingerprints
    held_record = live_records.held_record
    level_of = live_records.level_of
    _massive_record = live_records.massive_record
    planted_record = live_records.planted_record
    _receiver_of = live_records.receiver_of
    _detector = live_records.add_detector
    _ladder_of = live_records.ladder_of
    _release = live_records.release

    def _counts_stage(self, function: Callable[..., None]) -> None:
        """The count's line's act: each body's quanta moved by its record's current through its Nodes' Ports."""
        for block in self.blocks:
            self._counts_act(function, block, 1)

    def _counts_act(self, line: Callable[..., object], block: Block, direction: int) -> None:
        """THE COUNT'S LINE ON A BODY (ALGEBRA.md #the-counts-line): the line's levels laid at its
        first act (`_lay_count`: at every Node T c + r the Node's share of the record's form plus the origin T / 2), then per interval the record's levels
        here and across the six Ports (the Ports' arrivals), the count and its remainder stepped by
        the line forward or back (the direction +1 or -1), the body's Nodes following the count's centroid."""
        live = block.own
        if live is None:
            return
        if block.counts is None or block.count_remainder is None:
            block.counts, block.count_remainder = self._lay_count(block, live)
        term = CountTerm(
            block.count_norm,
            self.kind_wall(block.family, block.definition.pair),
            self.world.amplitude_bound,
            int(block.counts.sum()),
        )
        wrap = self.kind_wrap[block.family]
        levels = (live.now, live.before, live.im_now, live.im_before)
        arrived = [None if a is None else self.ports.arrivals(a, wrap) for a in levels]
        links = tuple(Levels(*(None if a is None else a[port] for a in arrived)) for port in range(6))
        start = CountStart(block.counts, block.count_remainder, Levels(*levels), links, direction)
        writes = cast(CountWrites, line(term, start, None))
        block.counts, block.count_remainder = writes.count, writes.remainder
        self._follow_count(block)

    def _body_count(self, block: Block) -> int:
        """The count at the body, its quanta: the declared count per Node over its Nodes (the record's norm in quanta, ALGEBRA.md #what-a-body-is; the count's line moves them between the Nodes and loses none)."""
        return self.body_quanta(block, self.world.measured[block.number].amount)

    def _lay_count(self, block: Block, live: LiveRecord) -> tuple[np.ndarray, np.ndarray]:
        """THE COUNT'S LAY (ALGEBRA.md #the-counts-line, the remainder's origin): T, the count's wall, the record's conserved form per quantum of the body's declared count, read once by Rule3's division act; then at every Node of the record T c + r is the Node's share of the form plus the origin T / 2 (the share's exact rational n / d: c = (n + d T / 2) div (d T), r the rest div d, Rule3's division act twice), so the count follows the norm with the margin T / 2 against the rounding's walk; a form below one per quantum is the line's refusal."""
        numerator, denominator = self.conserved_form(live)
        block.count_norm = int(
            rule3(NO_READ, NO_READ, 1, denominator * self._body_count(block), 0, 0, numerator)[0]
        )
        half = int(rule3(NO_READ, NO_READ, 1, SPAN, 0, 0, block.count_norm)[0])
        counts = self.declared_counts(block)
        remainder = np.full(self.shape, half, dtype=np.int64)
        if block.definition.counts is not None:
            return counts, remainder
        terms, read_coefficient = self.form_terms(live)
        for node in zip(*np.nonzero((live.now != 0) | (live.before != 0)), strict=True):
            share = ratio_sum(
                [(int(part[node]), int(read_coefficient[node])) for part, _ in terms]
                + [(-int(links[node]), 1) for _, links in terms]
            )
            count, rest = rule3(
                NO_READ, NO_READ, 1, share[1] * block.count_norm, 0, 0, share[0] + share[1] * half
            )
            counts[node] = int(count)
            remainder[node] = int(rule3(NO_READ, NO_READ, 1, share[1], 0, 0, rest)[0])
        return counts, remainder

    def _follow_count(self, block: Block) -> None:
        """The body's Nodes follow the count's centroid by whole Links (ALGEBRA.md #the-counts-line, the velocity: the centroid moves at the current's velocity; #the-velocity: the well moves with the count): along an axis where the centroid of the quanta shown (the counts above 0; a hole nature does not show) lies a whole Link beyond the body's centre, the mask, the corner, the family's pair region and the detector map shift one Link that way (the hop's HOST bookkeeping, now the count's); a resting body's quanta jitter within its Nodes (the open point 1) and move nothing."""
        shown = np.maximum(cast(np.ndarray, block.counts), 0)
        total = int(shown.sum())
        wrap = self.kind_wrap[block.family]
        shift = [0, 0, 0]
        for axis in range(3):
            extent, span = int(block.definition.extents[axis]), int(self.shape[axis])
            offsets = np.arange(span) - block.corner[axis]
            if wrap[
                axis
            ]:  # every Node at its nearest image to the corner (the halves compared, no division)
                offsets = np.where(2 * offsets > span, offsets - span, offsets)
                offsets = np.where(2 * offsets <= -span, offsets + span, offsets)
            along = shown.sum(axis=tuple(other for other in range(3) if other != axis))
            moment = 2 * int((along * offsets).sum())
            if moment >= total * (extent + 1):
                shift[axis] = 1
            elif moment <= total * (extent - 3):
                shift[axis] = -1
        block.moved = total > 0 and any(shift)
        if not block.moved:
            return
        old_mask = block.mask
        for axis in range(3):
            corner, span = block.corner[axis] + shift[axis], int(self.shape[axis])
            if wrap[axis]:
                corner = corner - span if corner >= span else corner + span if corner < 0 else corner
            elif corner < 0 or corner + int(block.definition.extents[axis]) > span:
                raise ValueError(
                    f"block {block.number}'s Nodes would leave the board through the face on axis "
                    f"{axis} at interval {self.tick}: its count's centroid crossed a whole Link toward a "
                    "face with no Port (ALGEBRA.md #the-counts-line)"
                )
            block.corner[axis] = corner
        block.mask = self._box(block.corner, block.definition.extents, block.family)
        self._inflow_port_pairs.clear()
        self._inflow_port_faces.clear()
        self._write_pair(block)
        for node in zip(*np.nonzero(old_mask & ~block.mask), strict=True):
            self.detector_at_node[(int(node[0]), int(node[1]), int(node[2]))] = -1
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

    def _hold_stage(self, function: Callable[..., None], advance: bool) -> None:
        """The hold's two acts: at the interval's start the moved bodies' Nodes rewritten; after the records, the held families' own step, the hold and the pace guard."""
        if advance:
            self._advance_fields(function)
        else:
            self._hold(function)

    def _sourced_record(self, family: int) -> LiveRecord:
        """The record a sourced family's level lives in: its held record where it is held, else its own."""
        return self.held_records.get(family) or self.sourced_records[family]

    def _count_source(self, live: LiveRecord, nxt: np.ndarray) -> None:
        """The record's count D_i = now^2 - next x before at the step's end, summed into its family's argument for the source's act (ALGEBRA.md #the-primitives row "the source"); nothing where no family is sourced by it."""
        argument = self._source_argument.get(live.family)
        if argument is not None:
            argument += live.now * live.now - nxt * live.before

    def _source_stage(self, function: Callable[..., object]) -> None:
        """The source's act (features/source): per sourced family the folder's line on its record family's counts summed at the step, the count's write added into the family's level after its own step, the remainder per Node kept; the counts cleared for the next interval."""
        for family, definition in enumerate(self.families):
            if definition.sourced is None:
                continue
            of, weight, scale, cap = definition.sourced
            writes = cast(
                SourceWrites,
                function(
                    SourceTerm(family, of, weight, scale, cap),
                    SourceStart(self.shape, self._source_argument[of]),
                    SourceOwn(self._source_remainders[family]),
                ),
            )
            self._sourced_record(family).now[writes.at] += writes.integers[writes.at]
            self._source_remainders[family] = writes.remainders
        for argument in self._source_argument.values():
            argument[...] = 0

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
        """The giving's act: the point emitters' windows close after the interval's bookings, then each body due gives; `function` is the folder's `apply`, reached through `_giving_act` at the three acts."""
        self._point_windows()
        for block in self.blocks:
            if block.emit_now:
                self._emit(block)

    def _spins_stage(self, function: Callable[..., None]) -> None:
        """The spin's step's act: each body's spin from the fields as the interval leaves them."""
        for block in self.blocks:
            self._spins_act(function, block, False)

    def close_interval(self) -> None:
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
        [name, target, of, degree, weight, table] of ALGEBRA.md #the-primitives is the loader's
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
        """THE ONE WALL OF A BODY (ALGEBRA.md #the-primitives, #the-well): W = 3 Q M, Q the
        universe's momentum unit and M the body's quanta as it holds them now (its
        own and its stocks, ALGEBRA.md #the-paces; a click moves M, ALGEBRA.md #the-interval, #the-primitives); the hop,
        the holds' divisions and the recoil read this one wall, the momentum's
        whole part n on it the body's velocity n / W in Links per interval."""
        return 3 * self.momentum_unit * sum(self.held[block.number])

    def _held_part(self, position: int, family: int, part: int) -> LiveRecord:
        """A held family's component record over the board (item 51; ALGEBRA.md #the-interval):
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
        found.extend(self.sourced_records.values())
        return found

    # The held families (ALGEBRA.md #the-paces, #the-counts-line; BUILD.md section 26
    # items 31, 32, 35 and 51): the operations, written once for any family

    def body_source(self, number: int, source: str) -> int:
        """A body's declared source for a held family (item 51): its content,
        the quanta it holds of every family ("content", ALGEBRA.md #the-counts-line),
        or its signed charge Q ("sign", ALGEBRA.md #the-paces)."""
        if source == "sign":
            return self._body_charge(number)
        return sum(self.held[number])

    def _hold(self, line: Callable[..., object], advance: bool = False, inverse: bool = False) -> None:
        """The hold: at every body's Nodes a held family's level is the body's declared source, written whole at both levels with the remainder 0 (the one write not the step's own); the parts beyond the time part and the dipoles are the hold's line `line` (features/hold), one call per body and held family with the act the loop names (the advance, the rewrite of a moved body's Nodes, the inverse); `node_level` is then each held family's level as every reading family's step reads it."""
        self.ports.begin()
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
            # THE VECTOR AND TENSOR PARTS AT THE BODIES (ALGEBRA.md #the-interval): the
            # body's numbers times the held factors over the wall, the remainder
            # carried, at every Node of the body at both levels; the interval's start
            # rewrites a moved body's Nodes alone (a body at rest keeps them)
            held = {
                block.number: self._held_writes(line, block, family, act)
                for block in self.blocks
                if advance or inverse or block.moved
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
                    degree = self.main_loop.function_of("the degree", "(i)")
                    group, axes = degree(self.families[family].parts, part)
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
        a dipole's term beyond an open face is dropped with its Node (ALGEBRA.md #the-interval)."""
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

    def _advance_fields(self, hold: Callable[..., object]) -> None:
        """The held families' own steps after every other family's (the plain step at every Node), then the hold at the bodies' Nodes, then the guard: every reading family's pace stays positive at every Node, else the run is refused."""
        held = self.held_component_records()
        with self.main_loop.act(
            "the operation",
            "(iii)",
            self._card_writes("the operation"),
            lambda: self.fingerprints_of(*held),
        ):
            for record in held:
                self._advance(record)
        self._hold(hold, advance=True)
        paces = self._card_writes("the signed read")
        with self.main_loop.act(
            "the signed read",
            "(i)",
            paces,
            lambda: {"the paces": {key: id(a) for key, a in self._pace_carry.items()}},
        ):
            self._guard()

    def wheel_at(
        self, family: int, node: tuple[int, ...], pair: tuple[int, int] | None = None
    ) -> tuple[int, int]:
        """The remainder's step g and the wheel W of the family's rule at a
        Node under the fixed wall (ALGEBRA.md #a-familys-declaration, #the-direction and (13);
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
        # the rule's three integers at the Node (ALGEBRA.md #the-line; item 44): the
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
        """The content a record of `family` reads at every Node, the folder's `apply` (features/signed_read, the function the main loop looked up at (i); ALGEBRA.md #the-primitives row 1, #the-paces) with its floor and guard, one array per family per interval; zeros for a family with no read."""
        cached = self._effective.get(family)
        if cached is not None:
            return cached
        definition = self.families[family]
        content = np.zeros(self.shape, dtype=np.int64)
        if definition.reads:
            read = self.main_loop.function_of("the signed read", "(i)")
            pair = (int(definition.pair[0]), int(definition.pair[1]))
            reads = tuple((other, weight, by) for other, weight, by, _twist in definition.reads)
            term = sr.SignedReadTerm(reads, self.family_charge[family], pair, self.node_clock)
            levels = {family: read_only(level) for family, level in self.node_level.items()}
            start = sr.SignedReadStart(self.shape, levels, None)
            own = sr.SignedReadOwn(family, definition.name, self.tick)
            content = cast(sr.SignedReadWrites, read(term, start, own)).content
        content.flags.writeable = False
        self._effective[family] = content
        return content

    def _body_charge(self, number: int) -> int:
        """A body's charge Q (ALGEBRA.md #the-paces): the sum of the signs of the
        quanta it holds, an integer of either sign, moved with the labels at
        the clicks (the held books)."""
        block = self.block_by_number.get(number)
        declared = block.definition.q if block is not None else 0
        return declared + sum(
            sign * quanta for sign, quanta in zip(self.family_charge, self.held[number], strict=True)
        )

    # The blocks (massive-record-v1)

    def stock_of(self, block: Block) -> int:
        """THE STOCK of the family a body gives (ALGEBRA.md #the-paces, #the-primitives): its
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

    # THE BODIES ON ONE NODE (ALGEBRA.md #the-interval, #a-familys-declaration, #the-primitives; the
    # one stroke, commit 6): the contraction, the feed, the induction, the spin's step,
    # written once for any body and any read

    def _spins_act(self, line: Callable[..., object], block: Block, inverse: bool) -> None:
        """THE BODY'S STEP AT (v) (ALGEBRA.md #the-interval, #a-familys-declaration): the spin's step's line
        (features/spins_step) on the body, from the fields as the interval leaves them (their
        `now` levels, which the inverse meets first): per read with a dipole, the read family's
        vector part and, for the spin's dipole, its time part at the body's Node's six
        neighbours with the row's two weights; the body's momentum, wall, spin and spin
        before; its remainders under the line's keys; the writes the spin, the spin before
        and the remainders back. THE FEED AND THE INDUCTION of ALGEBRA.md #a-familys-declaration are NOT here: built
        and held back (BUILD.md section 26 item 65; ALGEBRA.md #the-primitives)."""
        definition = self.families[block.family]
        if not definition.reads:
            return
        centre = self._window_centre(block)
        wrap = self.kind_wrap[block.family]
        reads: list[SpinRead] = []
        for position, (other, weight, by, _) in enumerate(definition.reads):
            read = self.families[other]
            if len(read.parts) < 2 or read.held_dipole is None:
                continue
            factor = weight if by == "plain" else -self._body_charge(block.number) * weight
            x, y, z = (self._ports_of(p.now, p.silent, centre, wrap) for p in self.held_parts[other][:3])
            time = turn = None
            if read.held_dipole == "spin":
                time = self._ports_of(self.held_records[other].now, False, centre, wrap)
                turn = read.spin_weights
            reads.append(SpinRead(position, read.held_dipole, factor, weight, (x, y, z), time, turn))
        momentum = self._momentum_now(block)
        start = SpinStepStart(
            THE_INVERSE if inverse else THE_ADVANCE,
            tuple(reads),
            (int(momentum[0]), int(momentum[1]), int(momentum[2])),
            self.wall_of(block),
            (int(block.spin[0]), int(block.spin[1]), int(block.spin[2])),
            (int(block.spin_before[0]), int(block.spin_before[1]), int(block.spin_before[2])),
        )
        own = SpinStepOwn(
            {key: value for key, value in block.hold_value.items() if key[0] in KEYS},
            {key: value for key, value in block.hold_carry.items() if key[0] in KEYS},
        )
        moment = block.definition.moment
        term = SpinStepTerm((int(moment[0]), int(moment[1]), int(moment[2])), self.node_clock)
        writes = cast(SpinStepWrites, line(term, start, own))
        block.spin, block.spin_before = list(writes.spin), list(writes.spin_before)
        block.hold_value.update(writes.own.values)
        block.hold_carry.update(writes.own.carries)

    def residue_of(self, live: LiveRecord | NodeRecord, block: Block) -> tuple[int, int]:
        """The residue from the law under the Node clock, read at the first shell Node: the record's rule remainder r at the body's first shell Node in the declared order, read now, in units of the remainder's step g = gcd(Gamma num, 6 den M, 3 den f) at that Node, and the wheel W = 3 den f / g (`wheel_at`); no declaration, no draw; which Node is read is a convention."""
        if isinstance(live, NodeRecord):
            # THE BODY'S NODE'S RECORD (ALGEBRA.md #what-a-body-is): its residue its
            # own remainder on its own wheel, read at the body's Node
            step, wheel = self.node_record_wheel(block)
            return live.remainder // step, wheel
        node = self.first_shell_node(block)
        step, wheel = self.wheel_at(live.family, node, live.pair)
        return int(live.remainder[node]) // step, wheel

    def _excite(self, block: Block, own_record: LiveRecord | NodeRecord) -> None:
        """The body's own record at the load, the one write of a body's record: its norm T one period's action of its own mode (the emitter's declared integer `norm`, the generator's, under the input stamp); its first residue and wheel from the law (`residue_of`) are read after its first advance (the load's seed has the remainders 0); every later residue is read at the click (`_emit`); called at the load alone."""
        emitter = block.definition.emitter
        assert emitter is not None
        if block.definition.profile is None:
            # the mathematician's gate item 8: the excited record is the body's
            # composed mode (ALGEBRA.md #what-a-body-is, #the-click), the generator's
            # profile; a flat seed is no mode and is refused where a body
            # givings (at the engine's construction: the generator parses the
            # world with the scalar seed to compute the profile)
            raise ValueError(
                f"measured[{block.number}].emitter needs the body's `seed` as its "
                "composed mode's profile (one integer per Node, the generator's "
                "`seed_on_the_mode`; a flat scalar seed is no mode and givings nothing lawful, "
                "ALGEBRA.md #the-click)"
            )
        # THE GIVING IS THE WINDOW'S (ALGEBRA.md #the-primitives; record 2082 (4);
        # commit 7): every emitter gives by the window at its centre Node at its declared
        # weight; the given train is CANCELLED (`_write_given_train_cancelled`, disconnected)
        if emitter.weight is None or emitter.norm_denominator is None:
            raise ValueError(
                f"measured[{block.number}].emitter declares no `weight` or no "
                "`norm_denominator`: the giving is the window's, the body's rotation written into "
                "the given row at its Node at the weight g until the outward norm reaches the "
                "excitation's action norm / norm_denominator (ALGEBRA.md #the-primitives; the "
                "generator's integers; the given train is retired, commit 7)"
            )
        if emitter.norm is None:
            raise ValueError(
                f"measured[{block.number}].emitter declares no `norm`: one period's "
                "action of the body's mode, its conserved form's share at the centre Node summed "
                "over the period, the generator's integer (ALGEBRA.md #the-click and (f), 9.19 "
                "(3); `excite_on_the_mode` of the massive record generator)"
            )
        if emitter.period is None:
            raise ValueError(
                f"measured[{block.number}].emitter declares no `period`: P, the "
                "nearest integer to 2 pi / omega_b of the body's mode, the generator's integer "
                "(ALGEBRA.md #the-click, #the-ladder: the tick counts intervals against "
                "(2 u + 1) P / (2 W))"
            )
        block.excitations += 1
        block.residue_pending = True
        own_record.norm = emitter.norm
        block.wait = 0
        block.emit_now = False

    def node_record_clock(self, block: Block) -> tuple[int, int]:
        """The body's Node's pair this interval: the declared clock pair [num_c, den_c] of the body's mode at rest, and on a moving body the proper pair of the drive's momentum now (the world's `proper_clock` at the momentum's whole part along its one axis, the same m the drive hops with), the moving mode's rotation at its moving centre per interval; the rest pair at m = 0."""
        clock = block.definition.clock
        assert clock is not None
        table = block.definition.proper_clock
        if table is None:
            return int(clock[0]), int(clock[1])
        index = max(abs(int(component)) for component in self._momentum_now(block))
        num_c, den_c = table[index]
        return int(num_c), int(den_c)

    def node_record_rule(self, block: Block) -> tuple[int, int, int, int]:
        """THE ONE RULE AT THE BODY'S NODE (ALGEBRA.md #what-a-body-is; item 42): the
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
        six times ALGEBRA.md #what-a-body-is's (K, den_c Gamma): the same rotation as rationals
        (ALGEBRA.md #what-a-body-is)."""
        num, den, gamma, content = self.node_record_rule(block)
        reads, self_coefficient, wall = coefficients(num, den, gamma, content)
        return 6 * reads[0] + self_coefficient, wall

    def _advance_node_record(self, block: Block, direction: int = 1) -> None:
        """One interval of the body's Node record by rule3 in `direction`, its six reads its own level, (2 a, 2 a, 2 a); the amplitude bound as the rows' (ALGEBRA.md #what-a-body-is, #the-direction)."""
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
            argument = self._source_argument.get(block.family)
            if argument is not None:
                argument[block.mask] += now * now - result * other
            node_record.before, node_record.now = node_record.now, result
        else:
            node_record.now, node_record.before = node_record.before, result

    def node_record_wheel(self, block: Block) -> tuple[int, int]:
        """The remainder's step g and the wheel W of the one rule at the body's Node
        (ALGEBRA.md #what-a-body-is, #a-familys-declaration; `wheel_at`'s reading with the six reads
        the body's Node): g the gcd of the rule's coefficients (on a and the wall), W
        = wall / g; ALGEBRA.md #what-a-body-is's wheel of the body record, the remainder six
        times its (the coefficients and the wall six times)."""
        coefficient, wall = self.node_record_coefficients(block)
        step = gcd(wall, coefficient)
        return step, wall // step

    def node_record_form(self, block: Block) -> int:
        """The body's Node's record's invariant (ALGEBRA.md #what-a-body-is):
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

    def _excitation_rung(self, block: Block) -> None:
        """The count of intervals to the body's next click, started at a click and lowered every interval; the body gives when it reaches zero."""
        own: LiveRecord | NodeRecord | None = (
            block.node_record if block.node_record is not None else block.own
        )
        emitter = block.definition.emitter
        if own is None or emitter is None or block.emit_now or block.window is not None:
            return
        # the stock is the given family's content held at the body (ALGEBRA.md
        # ALGEBRA.md #the-paces; item 47), or the body's own quanta set aside (ALGEBRA.md #the-primitives; commit
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
        # the given record's residue and wheel from the law (ALGEBRA.md #a-familys-declaration, #the-ladder
        # (c)): the body's own remainder at its first shell Node in the
        # declared order, read at the click on the body's wheel there
        residue, wheel = self.residue_of(own, block)
        wait = block.wait
        # the read Node: the first shell Node of the lattice body (item 33),
        # the body's Node (the centre Node) of a body on one Node (ALGEBRA.md #what-a-body-is; item 42)
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
        # the body's own record is not ended and never rewritten (ALGEBRA.md #the-ladder)
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
            # ALGEBRA.md #the-second-level, #the-primitives; commit 4), the loader's integers
            part=emitter.part,
            twist=emitter.twist,
        )
        # E^T: the given clock's character on the body's Nodes, written once at both levels, every Node at the vertex's phase (the one-Node broadband giving; a line's travelling character, the per-Link pair of ALGEBRA.md ALGEBRA.md #the-click, is owed until that pair is declared) NO TABLE IN THE ENGINE (the cleanup order's step 2; ALGEBRA.md #the-click (6), ALGEBRA.md #a-familys-declaration): the given pair is the world's two integers `given: [now, before]`, the generator's, checked at load (before = -now), written on every Node of the body THE GIVEN TRAIN (ALGEBRA.md #the-click; BUILD.md section 26 item 27): the train's two levels written on the body's Nodes in the box's x-major order (`body_node_indices`, the loader's and the generator's one convention), the norm T the written one (the conserved form on the given family's vacuum, the generator's integer checked at load) THE WINDOW (ALGEBRA.md #what-a-body-is, #the-primitives; item 50; commit 7, the one giving): no train; the window opens at the click, the given row at the body's Node written from its rotation every interval (`_point_windows`) until the outward norm reaches T; the record named at the close
        live.window_open = True
        live.box = self.mask_box(block.mask)  # HOST (item 43): the body's own Nodes
        block.window = identity
        if emitter.receiver is not None:
            # the named sets in the NAMED order (ALGEBRA.md #rule3: the
            # ladder cumulative in its declared order), a set's detectors in the
            # detectors' order within it
            live.ladder = [
                detector
                for name in emitter.receiver
                for detector, set_name in enumerate(self.detector_set)
                if set_name == name
            ]
        # THE STOCK IS GIVEN-FAMILY CONTENT (ALGEBRA.md #the-paces; item 47): the
        # giving lowers the given family's content held at the body by one,
        # the body's own quanta and its charge untouched (under the point
        # emitter too, item 50: the quantum moves at the open, the window
        # shapes its rows, the close names the record)
        opened = self._giving_act(
            block,
            GivingStart(
                THE_OPEN,
                self.held[number][family],
                (int(block.momentum[0]), int(block.momentum[1]), int(block.momentum[2])),
                None,
                0,
                (0, 0, 0),
            ),
            None,
        )
        self.held[number][family] += opened.count
        self.ledger.held_spent[family] += 1
        # THE NORM UNDER THE NODE CLOCK (BUILD.md section 26 items 31 and 36; ALGEBRA.md #the-direction): the given record's T is p times its conserved form as written on the board, the engine's own integer with the content at the body's Nodes AS IT STANDS this interval: ONE ORDER FOR BOTH CLICKS (ALGEBRA.md #the-primitives; BUILD.md section 26 item 58): a click's writes enter at the next interval (ALGEBRA.md #the-line), so the giving's lowered quanta are held after the held families' step with the takings' (`_advance_fields`), no hold here (the hold at once, item 47, HISTORY: a defect against ALGEBRA.md #the-line) THE POINT EMITTER (item 50): the record's norm is T from the open, the excitation's action the window will reach (ALGEBRA.md), as the exact rational norm / norm_denominator, so the ladder reads its bookings from the first interval (Born's rule's walk as now)
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
                # the tick's count (ALGEBRA.md #the-ladder): the intervals from the
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
            # the body's Node's record (ALGEBRA.md #what-a-body-is): its level is the standing record's
            # coefficient, the sum over the Nodes and the centre alike
            total += block.node_record.now
            at_centre += block.node_record.now
        elif block.own is not None:
            total += int(np.sum(block.own.now[block.mask]))
            at_centre += int(block.own.now[centre])
        if block.previous_sum <= 0 < total:
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
        """One interval of the rule backwards on a record: from (a_next, a_now, r') to (a_now, a_before, r) with 3 den Gamma a_before - r = num SUM_j (Gamma - c_j) a_now,j + 6 den c a_now - (3 den Gamma a_next + r') under the fixed wall (the forward step's integers, the clock field of the interval's start), the remainder in [0, 3 den Gamma), exact at every Node; with a tensor part read, a twist or a second level the arrivals are stepped back per axis after the transport's inverse (`_transport`), both levels."""
        if live.silent:
            return  # a zero held part steps to zero exactly (HOST; ALGEBRA.md #the-interval)
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
        twisted = None if field else self._twist_reads(live, True)
        sigma_self = self._self_source(live, True)
        plain = axis_contents is None and twisted is None and live.im_now is None and sigma_self is None
        if not plain:
            receive = self.main_loop.function_of("the receive", "(i)")
            level_step = self.main_loop.function_of("the phase", "(i)")
            reads_re, reads_im = self._transport(receive, live, twisted, True)
            a_before, live.remainder = level_step(
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
                a_before -= sigma_self  # the same multiple of the wall off (ALGEBRA.md #the-interval)
            if live.im_now is not None and live.im_before is not None and live.im_remainder is not None:
                ir = self.main_loop.function_of("the internal representation", "(i)")
                rule = (num, den, gamma, content, axis_contents)
                im = ir(
                    level_step,
                    rule,
                    reads_im,
                    live.im_before,
                    live.im_now,
                    live.im_remainder,
                    not field,
                    -1,
                )
                im_a_before, live.im_remainder, live.im_now, _ = im
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
        self.ports.begin()
        # the bodies' step back first (ALGEBRA.md #the-interval; commit 6): the momentum and the
        # spin as the interval began, from the fields as it left them
        for block in self.blocks:
            self._spins_act(self.register.at("the spin's step", "(v)"), block, True)
        # the count's line back (its own inverse, the current reversed; ALGEBRA.md
        # #the-counts-line): the quanta return to their Nodes before the records step back
        counts_line = self.register.at("the count's line", "(ii)")
        for block in self.blocks:
            self._counts_act(counts_line, block, -1)
            if block.moved:
                raise ValueError(
                    f"the inverse map is defined for a body whose Nodes stood through the interval (block "
                    f"{block.number} moved at interval {self.tick}; the field moved back through the body, "
                    "ALGEBRA.md #the-primitives, is not built)"
                )
        # the joint inverse (ALGEBRA.md #the-counts-line; item 51): every
        # family backward at the held levels of the interval's start (their
        # `before` level: the held families stepped last), then the held
        # families backward and their hold
        for family, record in self.held_records.items():
            self.node_level[family] = record.before
        self._effective.clear()
        # the interval's dipole writes taken back first (ALGEBRA.md #the-interval; commit 2): they
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
        self.tick -= 1

    # The rule

    def _axis_sums(
        self, a: np.ndarray, wrap: tuple[bool, bool, bool] | None = None
    ) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
        """The two arrivals summed per axis at every Node, the three arrival sums rule3 reads; their sum is the send's (ALGEBRA.md #the-line)."""
        arr = self.ports.arrivals(a, wrap)
        sums = tuple(arr[port_of(axis, 1)] + arr[port_of(axis, -1)] for axis in range(3))
        return sums[0], sums[1], sums[2]

    def _axis_contents(self, family: int, inverse: bool = False) -> tuple[np.ndarray, ...] | None:
        """THE AXIS CONTENTS t_a of a reading family (ALGEBRA.md #the-interval): SUM over its reads of weight x by x (the read family's aa component div 2), one division per read per axis with the remainder kept at the Node (`_pace_carry`), advanced once per interval, backward the same values with the remainder stepped back (r_(t-1) = (r_t - S) mod 2); None where no read's tensor part was ever sourced, the isotropic rule bit for bit."""
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

    # THE TRANSPORT (ALGEBRA.md #the-transport, #the-interval, #the-primitives; the one stroke, commit 4):
    # the operations, written once for any phase-2 family and any read with a twist

    def _arrival(
        self, a: np.ndarray, axis: int, sigma: int, wrap: tuple[bool, bool, bool]
    ) -> np.ndarray:
        """The level arriving through the Port toward `sigma` on the axis (the wrap on a periodic axis, 0 beyond an open face, the Node itself on a folded axis)."""
        arrived: np.ndarray = self.ports.arrivals(a, wrap)[port_of(axis, sigma)]
        return arrived

    def _twist_reads(self, live: LiveRecord, inverse: bool) -> tuple[TwistRead, ...] | None:
        """THE TWIST READS of a record's family (ALGEBRA.md #the-transport, #the-interval, #the-primitives): per read with a twist whose vector part is not silent, its factor on the record
        (the weight times the record's own rotation for the twist "own", else the declared
        twist, by q the family's charge sign) and the read family's vector part at the Node,
        the `before` levels backward; None where no read turns the transport (the identity,
        bit for bit) or on a family with one level."""
        definition = self.families[live.family]
        if definition.levels < 2:
            return None
        sign = self.family_charge[live.family]
        found: list[TwistRead] = []
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
            x, y, z = (part.before if inverse else part.now for part in vector)
            found.append(TwistRead(factor, (x, y, z)))
        return tuple(found) if found else None

    def _transport(
        self,
        line: Callable[..., object],
        live: LiveRecord,
        reads: tuple[TwistRead, ...] | None,
        inverse: bool,
    ) -> tuple[list[np.ndarray], list[np.ndarray] | None]:
        """THE SIX ARRIVALS AFTER THE TRANSPORT (ALGEBRA.md #the-transport, #the-interval),
        summed per axis for the two levels by the receive's line (features/receive): the
        record's pair at the Node, its family's twist reads and the six Links as the Ports
        read them (`_arrival`), the `before` levels backward; the second level's sums None
        while the record has no second level and no rotation writes one. NO REMAINDER IS
        KEPT ON THE PORT (BUILD.md item 64): the rounding is the line's nearest unit and the
        inverse recomputes the same arrivals from the `before` levels, exact."""
        wrap = self.kind_wrap[live.family]
        re = live.before if inverse else live.now
        im = None if live.im_now is None else (live.im_before if inverse else live.im_now)
        twisted = () if reads is None else reads
        links = []
        for axis in range(3):
            for sigma in (1, -1):
                links.append(
                    Link(
                        self._arrival(re, axis, sigma, wrap),
                        None if im is None else self._arrival(im, axis, sigma, wrap),
                        tuple(self._arrival(read.here[axis], axis, sigma, wrap) for read in twisted),
                    )
                )
        start = ReceiveStart(re, im, twisted, tuple(links))
        writes = cast(ReceiveWrites, line(self._receive_term, start, None))
        return list(writes.re), None if writes.im is None else list(writes.im)

    def _self_source(self, live: LiveRecord, inverse: bool) -> np.ndarray | None:
        """THE SELF-SOURCE'S SLOT (ALGEBRA.md #a-familys-declaration, #the-interval, #the-second-level): per family with a unit
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
        """THE TRANSVERSE BOOKING (ALGEBRA.md #the-second-level): the axis of a record's own
        vector component, whose Ports book nothing of it (the longitudinal component
        along the Port's axis carries the near field and no count); None for a scalar
        family's record or a time part (booked through every Port)."""
        if len(self.families[live.family].parts) > 1 and 1 <= live.part <= 3:
            return live.part - 1
        return None

    # The flux reading (ALGEBRA.md #rule3, the mathematician's derivation of 2026-09-24 from 8.2; BUILD.md section 26 item 13): the flux into a Node i from a read j of it, 3 G_ij = A_ij (now_i before_j - before_i now_j), a bilinear form of the record's own two levels at the two ends of a Link, pair-free and antisymmetric; a receiver's offer the one-way inward flux through its Ports, summed over intervals; the record's norm its conserved form I. Both in the integers 3 G x wall and 3 I x wall, wall the family's common wall (the least common multiple of its pairs' numerators over the board).

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
        """The Ports of every detector for the flux reading: per axis of extent above one and per side, the Nodes of a detector whose neighbour across the Link (on the family's faces) is a Node of no set or of another set; a Link inside one set is no Port, a folded axis carries none, beyond an open face there is no Link."""
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
                neighbour = self.ports.arrivals(set_index, wrap, -2)[port_of(axis, side)]
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
            across = self.ports.arrivals(flat, wrap, -1)[port_of(axis, side)]
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
        # i's face toward j is side along the axis (ALGEBRA.md #the-ladder)
        self._inflow_port_faces[family] = (
            np.concatenate(axes) if axes else np.zeros(0, dtype=np.int64),
            np.concatenate(sides) if sides else np.zeros(0, dtype=np.int64),
        )
        return pairs

    def detector_inflow_tally(self, live: LiveRecord) -> dict[int, int]:
        """The detectors' inflow per record over the Ports alone: this interval's one-way inward flux into every detector, 3 G_ij = now_i before_j - before_i now_j where positive per Port, times the family's wall (the form's units), from the record's two levels after the interval's step, by the detector's index; read at the Port pairs only (one gather per pair, exact Python integers), never over the board."""
        port_i, port_j, port_detector = self._inflow_ports(live.family)
        port_axis, port_side = self._inflow_port_faces[live.family]
        # THE TRANSVERSE BOOKING (ALGEBRA.md #the-second-level; commit 4): the Ports along
        # the record's own vector component book nothing of it
        own_axis = self.booked_axis(live)
        if own_axis is not None:
            keep = port_axis != own_axis
            port_i, port_j, port_detector = port_i[keep], port_j[keep], port_detector[keep]
            port_axis, port_side = port_axis[keep], port_side[keep]
        if port_i.size == 0:
            return {}
        # THE CURRENT IS UNWEIGHTED (ALGEBRA.md #the-direction and (13); BUILD.md
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
            # the pair's norm (ALGEBRA.md #the-second-level): the second level's current added
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
        # THE BOOKING IN THE BODY'S FRAME (ALGEBRA.md #the-ladder; BUILD.md section 26 item 56): a face of a body moving at v with outward normal n books per interval (G_in + (v . n) e_out) cut at zero AFTER the sum: G_in the board's inward current through the face's Link (the Port booking above), e_out the record's density on the Node outside the face (`node_density`, the same units), v . n = side x momentum / wall along the face's axis, positive at a face advancing into the outside (the front) and negative at a face receding from it (the back). One rule for every face of every moving set, per interval, not per hop: at the front an oncoming record books G_in + v e_out, a standing or transverse one v e_out, a record outrunning the body nothing; at the back a record overtaking from behind books G_in - v e_out, the norm once, with no negative booking. The whole part is booked, the fraction carried on the record per detector (`carry`, exact). The three tests: the face's Link, the outside Node's density and the body's own pace, fixed work; sums and products; no name. At v = 0 the rule is the Port booking above, bit for bit.
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
        """THE FOUR-VECTOR CLICK'S TALLY (ALGEBRA.md #the-interval, #the-ladder; commit 5
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
        """The sign per axis of a tally, sigma_a of ALGEBRA.md #the-primitives, #the-interval:
        -1, 0 or 1 (DETECTOR: the quantum's direction of travel, not its size)."""
        return [(value > 0) - (value < 0) for value in tally]

    def inward_flux(self, live: LiveRecord, mask: np.ndarray) -> int:
        """The one-way inward flux into the Nodes of `mask` through the Links from outside: wall times (now_i before_j - before_i now_j) where positive from the record's two levels after the step, the second level added, the Ports along the record's own component skipped."""
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
                port = self.ports.outward(mask, wrap)[port_of(axis, side)]
                if not port.any():
                    continue
                flux = np.zeros(self.shape, dtype=object)
                for level_now, level_before in levels:
                    now_j = self.ports.arrivals(level_now, wrap)[port_of(axis, side)].astype(object)
                    before_j = self.ports.arrivals(level_before, wrap)[port_of(axis, side)].astype(
                        object
                    )
                    flux = (
                        flux + level_now.astype(object) * before_j - level_before.astype(object) * now_j
                    )
                total += int(np.sum(np.where(port & (flux > 0), flux, 0)))
        return total * wall

    def conserved_form(self, live: LiveRecord) -> Ratio:
        """The record's conserved form I in the form's units, 3 I x wall in the vacuum: over the Nodes [3 wall (den_i / num_i) Gamma (now_i^2 + before_i^2) - 6 wall (den_i / num_i) c_i now_i before_i] / p_i - wall now_i SUM_j before_j, p_i = Gamma - c_i (+ q Lambda d_i) the pace at the Node, the six reads with the family's faces; the sum of every Node's share (`form_share`), an exact rational (each Node's share read in the world's time by its own pace)."""
        return self.form_share(live, np.ones(self.shape, dtype=bool))

    def form_share(self, live: LiveRecord, mask: np.ndarray) -> Ratio:
        """The Nodes' share e of the record's conserved form (ALGEBRA.md #the-click, #rule3, #the-direction) on the Nodes of `mask`, in the form's units: a bilinear form of the record's two levels at the Node, its six reads and the pace at the Node (verb B, local), the Node's terms weighted by 1 / p_i (`form_terms`, summed exactly); its change over an interval is the sum of the plain currents through the Node's Links plus the remainders' term, so a bound mode's share is constant where nothing flows."""
        terms, read_coefficient = self.form_terms(live)
        total: Ratio = ZERO
        for node, links in terms:
            total = ratio_sum(
                [total, self._weighted_sum(node, read_coefficient, mask), (-int(np.sum(links[mask])), 1)]
            )
        return total

    def form_terms(self, live: LiveRecord) -> tuple[list[tuple[np.ndarray, np.ndarray]], np.ndarray]:
        """The per-Node terms of the record's conserved form, one pair per level pair: the Node term L [w_i (now^2 + before^2) - S_i now before] over the rule's read coefficient R_i (the third value) and the Link term L now_i SUM_j before_j, L the family's common wall (ALGEBRA.md #the-line; item 44); a Node's share is the quotient less the Link term."""
        family = live.family
        wall = self.kind_wall(family, live.pair)
        # THE SHARE UNDER THE NODE'S OWN PACE (ALGEBRA.md #the-direction and (13); BUILD.md section 26 item 36; the form's units, the plain share in the vacuum): with the pace p_i at every Node, e_i = [3 wall (den_i / num_i) Gamma (now_i^2 + before_i^2) - 6 wall (den_i / num_i) c_i now_i before_i] / p_i - wall now_i SUM_j before_j; the step's operator is symmetric under the weight den_i / (num_i p_i), so the sum over the board is exactly invariant where the clock field stands still, and the share's change over an interval is the sum of the plain currents wall (now_i before_j - before_i now_j) through the Node's Links plus the remainders' term (wall / (num_i p_i)) (a_next - a_before)(r - r'), an exact rational per Node (the weights p_i p_j at one integer scale, form (B) of item 34, HISTORY)
        field = live.held_part
        gamma = 1 if field else self.node_clock
        content = (
            np.zeros(self.shape, dtype=object)
            if field
            else self._effective_content(live.family).astype(object)
        )
        num_all, den_all = self.pair_arrays(family, live.pair)
        # THE FORM FROM THE RULE'S OWN INTEGERS (ALGEBRA.md #the-line; item 44): with (R_i, S_i, w_i) the rule's coefficients at the Node, the Node's term is L [w_i (now^2 + before^2) - S_i now before] / R_i and the Link term L now_i SUM_j before_j, L the family's common wall; exact where the field stands (the step's operator symmetric under the weight 1 / R_i), the work term where it moves; the first-order form of item 36, [3 den Gamma (a^2 + b^2) - 6 den c a b] / (p num), is this at R = p num, S = 6 den c, w = 3 den Gamma
        (read_coefficient, _, _), self_coefficient, wall_at = coefficients(
            num_all.astype(object), den_all.astype(object), gamma, content, ISOTROPIC, not field
        )
        # the pair's two levels summed (ALGEBRA.md #the-interval; commit 4): the form of each level, the
        # plain Link term (exact where every twist is 0, a reading elsewhere)
        levels = [(live.now, live.before)]
        if live.im_now is not None and live.im_before is not None:
            levels.append((live.im_now, live.im_before))
        terms = []
        for level_now, level_before in levels:
            now = level_now.astype(object)
            before = level_before.astype(object)
            send = self.main_loop.function_of("the send", "(i)")
            reads = send(self.ports, level_before, self.kind_wrap[family]).astype(object)
            terms.append((wall * form_term(self_coefficient, wall_at, now, before), wall * now * reads))
        return terms, read_coefficient

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
        """The norm as the exact rational: the given record's conserved form Q, the Node's terms weighted by 1 / p_i, as the pair (numerator, denominator) in lowest terms, the record's `norm` and `pace`; the ladder reads the plain flux C against Q in integers; for a record written at one level p Q is whole (the integer T in the body's own units) and the pair reduces from (p Q, p); a record written across levels has a rational Q, its world energy, and the same reading."""
        return self.conserved_form(live)

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
        # THE EMITTER'S NODES ARE NODES LIKE EVERY OTHER (ALGEBRA.md #the-click; the Boss's line of 2026-09-24 on the knot): no grace, no exemption, no own take, no fresh Port; the given record is written once and the law advances it (the retired forms in BUILD.md section 26). Every given record, light's kind or a massive kind alike, books its flux at the Nodes and clicks on its ladder (the click is the law's one action on any record, POSTULATES 10); a BLOCK'S own record (a massive kind, given of no emitter) books nothing and is on no ladder (massive-record-v1, MUST 2). THE BOOKING BY ATTRIBUTE (item 51; item 53): a held family's record and a body's own standing record are read by no detector; every other record is booked at the Ports (nothing declared: derived from `held`)
        if live.silent:
            return  # a zero held part steps to zero exactly (HOST; ALGEBRA.md #the-interval)
        field = live.held_part
        booked = not field and not live.standing
        # The rule with the record's pair on the six-neighbour term
        # (massive-record-v1, MASSIVE_RECORD.md section 1): G over the six
        # neighbours, then D by 3 den with the remainder kept, then T; at
        # light's pair [1, 1] the first build's integers bit for bit.
        num, den = self.pair_arrays(live.family, live.pair)
        # THE COUPLING IS THE CLICK ALONE (the model owner's decision (2) of record 1962; ALGEBRA.md #the-line (B); BUILD.md section 26 item 30): no coupling's term and no folded denominator (MASSIVE_RECORD.md section 7 HISTORY); the wall 3 den, one division per row per interval, the remainder kept in [0, wall) THE NODE CLOCK UNDER THE FIXED WALL (the model owner's decision (5) of record 1962 and his word of 2026-09-25 in Nature24's session, record 1994: the backward run exact everywhere; ALGEBRA.md #the-paces amended, the mathematician's section asked; BUILD.md section 26 item 34): the wall is 3 den Gamma at every Node, a constant of the declared region, and the clock enters the numerator as the pace Gamma - c_j of each of the six reads: 3 den Gamma a_next + r' = num SUM_j (Gamma - c_j) a_j + 6 den c a_now - 3 den Gamma a_before + r, c the family of clicks' level at a Node, the remainder in [0, 3 den Gamma). The remainder's range never changes, so the step is one to one at every Node for every clock history (the wall 3 den (Gamma + c) of item 31, which shrank where the level fell and merged two states into one, HISTORY). In the vacuum (c = 0) the levels are the plain rule's bit for bit and the remainder Gamma times its; at uniform content 1 - cos omega' = (1 - cos omega)(Gamma - c) / Gamma. One division per row per interval, the int64 total under the load bound of `_pair_bound`. THE FAMILY OF CLICKS ITSELF steps plain (the pace 1, the wall 3 den): it reads no other family and not its own level (ALGEBRA.md #the-counts-line)
        gamma = 1 if field else self.node_clock
        content = 0 if field else self._effective_content(live.family)
        # THE NODE'S OWN PACE (the model owner's ruling of record 2003, "take only from the current Node, not from the neighbours"; ALGEBRA.md ALGEBRA.md #the-direction; BUILD.md section 26 item 36): the pace p_i = Gamma - c_i (+ q Lambda d_i) multiplies the Node's own six-neighbour sum, the reads plain as S_6 reads them: 3 den Gamma a_next + r' = p_i num S_6(a_now)_i + 6 den c_i a_now - 3 den Gamma a_before + r; the Node steps the vacuum's rule at its own pace (the pace on each read's far end, form (B) of item 34, HISTORY)
        axis_contents = None if field else self._axis_contents(live.family)
        twisted = None if field else self._twist_reads(live, False)
        sigma_self = self._self_source(live, False)
        window = self._window(live.box, self.kind_wrap[live.family])
        im_next: np.ndarray | None = None
        plain = axis_contents is None and twisted is None and live.im_now is None and sigma_self is None
        if not plain:
            # THE FOUR PACES AND THE TRANSPORT (ALGEBRA.md #the-interval; commits 3 and 4):
            # the arrivals per axis after the transport, the rule per level on the whole
            # board (HOST: no window shortcut here); the second level allocated by the
            # first rotation that writes it
            receive = self.main_loop.function_of("the receive", "(i)")
            level_step = self.main_loop.function_of("the phase", "(i)")
            reads_re, reads_im = self._transport(receive, live, twisted, False)
            nxt, live.remainder = level_step(
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
                nxt -= sigma_self  # the self-source's term, w Sigma_self off the right side (ALGEBRA.md #the-interval)
            if reads_im is not None or live.im_now is not None:
                ir = self.main_loop.function_of("the internal representation", "(i)")
                rule = (num, den, gamma, content, axis_contents)
                im = ir(
                    level_step,
                    rule,
                    reads_im,
                    live.im_now,
                    live.im_before,
                    live.im_remainder,
                    not field,
                    1,
                    live.now,
                )
                im_next, live.im_remainder, live.im_now, live.im_before = im
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
        self._count_source(live, nxt)
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
            # the window's write right after the record's own step, before any booking reads the rows
            with self.main_loop.act(
                "the giving", "(ii)", self._card_writes("the giving"), lambda: self.fingerprints_of(live)
            ):
                self._window_write(live)
        # the flux reading: the one-way inward flux into every detector, booked to its pointer, then the click
        with self.main_loop.act(
            "the clicks", "(ii)", self._card_writes("the clicks"), lambda: self.fingerprints_of(live)
        ):
            before_booking = list(live.pointers)
            for detector, value in self.detector_inflow_tally(live).items():
                live.pointers[detector] += value
                live.absorbed += value
            increments = [now - then for now, then in zip(live.pointers, before_booking, strict=True)]
            self._ladder_click(live, increments)

    def _giving_act(self, block: Block, start: GivingStart, live: LiveRecord | None) -> GivingWrites:
        """One act of the giving through the folder's `apply` (the function the main loop looked up at (ii)): the term from the emitter's declaration, the own record from the window's record (`live`), none at the open."""
        emitter = block.definition.emitter
        if emitter is None:
            raise ValueError(f"the body {block.number} gives with no emitter declared")
        norm = emitter.norm if emitter.norm is not None else 1
        denominator = emitter.norm_denominator if emitter.norm_denominator is not None else 1
        weight = emitter.weight if emitter.weight is not None else 1
        term = GivingTerm(weight, norm, denominator, emitter.family)
        own = (
            GivingOwn(None, 0, (0, 0, 0))
            if live is None
            else GivingOwn(
                live.window,
                live.outward,
                (live.outward_tally[0], live.outward_tally[1], live.outward_tally[2]),
            )
        )
        function = self.main_loop.function_of("the giving", "(ii)")
        return cast(GivingWrites, function(term, start, own))

    def _window_write(self, live: LiveRecord) -> None:
        """One interval of an open window right after the record's own step: the body's rotation written into the given row at the body's Nodes, the norm that left the body read as the outward flux through its outer Ports, the window's count grown and the box taking the body in."""
        block = self.block_by_number.get(live.emitter) if live.emitter is not None else None
        if block is None or block.window != live.identity:
            return
        emitter = block.definition.emitter
        if emitter is None or emitter.weight is None:
            return
        written = self._giving_act(
            block, GivingStart(THE_WRITE, 0, (0, 0, 0), self._body_levels(block), 0, (0, 0, 0)), live
        )
        if written.level is not None:
            live.now[block.mask] += written.level
        flux_tally = [0, 0, 0]
        flux = self.body_outward_flux(live, block, flux_tally)
        closing = self._giving_act(
            block,
            GivingStart(
                THE_CLOSE, 0, (0, 0, 0), None, flux, (flux_tally[0], flux_tally[1], flux_tally[2])
            ),
            live,
        )
        live.outward = closing.own.outward
        live.outward_tally = list(closing.own.tally)
        live.window += 1
        if live.box is not None:
            live.box = tuple(
                (min(lo, low), max(hi, high))
                for (lo, hi), (low, high) in zip(live.box, self.mask_box(block.mask), strict=True)
            )

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
        """The outward flux through the body's outer Ports this interval, wall times (now_j before_i - before_j now_i) where positive over the Ports to Nodes outside the body (none beyond an open face, on a folded axis or along the record's own component), the second level added; with `tally` the flux per axis signed by the side."""
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
                ports = self.ports.outward(mask, wrap)[port_of(axis, side)]
                if not ports.any():
                    continue
                flux = np.zeros(int(np.count_nonzero(ports)), dtype=np.int64)
                for now, before in levels:
                    now_j = self.ports.arrivals(now, wrap)[port_of(axis, side)][ports]
                    before_j = self.ports.arrivals(before, wrap)[port_of(axis, side)][ports]
                    flux += now_j * before[ports] - before_j * now[ports]
                outward = int(flux[flux > 0].sum()) * wall
                total += outward
                if tally is not None:
                    tally[axis] += side * outward
        return total

    def _point_windows(self) -> None:
        """The point emitters' windows closed after the interval's bookings: the given record's norm, residue and wheel fixed from what left the body, the window's count and the record's box settled, the giving line written."""
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
            # (d) the close: the folder's close act on the outward norm summed over the window
            if self._giving_act(
                block, GivingStart(THE_CLOSE, 0, (0, 0, 0), None, 0, (0, 0, 0)), live
            ).closed:
                self._close_window(block, live)

    def _close_window(self, block: Block, live: LiveRecord) -> None:
        """The window's close (ALGEBRA.md; item 50): the writing
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
            # THE GIVEN QUANTUM'S FOUR-VECTOR (ALGEBRA.md #the-primitives, #the-interval; commit 5
            # without the recoil): the count 1, the space part the sign per axis of
            # the outward flux through the body's Ports over the window (DETECTOR);
            # a symmetric emitter's tallies cancel (ALGEBRA.md #the-primitives); no body's momentum moves
            line["momentum"] = self.direction_of(live.outward_tally)
            self.record(line)
        live.giving_line = None
        block.wait = 0
        if self.stock_of(block) > 0:
            block.excitations += 1

    def _point_window_inverse(self, block: Block) -> None:
        """One interval of an open window backwards (ALGEBRA.md):
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
        indices) alone, as the send reads them over the board (the wrap
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
        units; read on the Nodes outside a moving set's faces (ALGEBRA.md #the-ladder; item 56; the hop's reading of item 48 HISTORY)."""
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

    def _ladder_click(self, live: LiveRecord, increments: list[int]) -> None:
        """The click through the folder's ladder (features/clicks, the function the main loop looked up at (ii)): the record's total and the chosen detector from its residue, norm, wheel, pace, ladder and the interval's increments; at a click the first rung, the rung's count at a set with a body, the click line, the record deleted whole after the interval's advances."""
        if live.clicked:
            return
        click = self.main_loop.function_of("the clicks", "(ii)")
        ladder = self._ladder_of(live)
        detector, live.total = click(
            live.u, live.norm, live.wheel, live.pace, live.total, ladder, increments
        )
        if detector is None:
            return
        live.first_rung[detector] = self.tick
        if detector in self.set_block:
            block = self.block_by_number[self.set_block[detector]]
            self.rung_counts[(live.identity, detector)] = self._body_count(block)
        self._gather_line(live, detector)
        live.clicked = True
        self.dead.append(live.identity)

    def record_form(self, live: LiveRecord) -> Ratio:
        """The conserved form I of the record, a GAMEBOARD diagnostic read by the books: the one form of the rule, `conserved_form`, from the rule's own integers, L [w (a^2 + b^2) - S a b] / R at the Nodes and L now_i SUM_j before_j on the Links, L the least common multiple of the distinct numerators, an exact rational, conserved by the rule up to the remainders' bounded jitter."""
        return self.conserved_form(live)

    def step(self) -> None:
        """One interval, walked by the main loop: the clock, the file's acts through the register under its guards, the closing."""
        self.main_loop.run(self)

    # The readings and the output lines: the functions of events/output.py bound as methods
    leaks = output.leaks
    _gather_line = output.gather_line
    books = output.books
    contents = output.contents
    snapshot_stream = output.snapshot_stream
