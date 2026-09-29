"""The engine (one engine, no law's name and no version, ALGEBRA.md #the-primitives): the GameBoard of Nodes, every family's record stepped by Rule3 at every Node from its two levels and the six arrivals through its Ports (core/rule3.py), a remainder kept per division; every primitive one folder found by its name, walked in the step file's order by the main loop (law/step.json, core/main_loop.py). A body is its record and its count (ALGEBRA.md #what-a-body-is); THE CLICK IS THE COUNT'S LINE FOR EVERY RECORD (the model owner's word of 2026-09-29 on #1495, finding 10; ALGEBRA.md #the-counts-line): every bound body gives at its click, the given record laid with one quantum from its form; the count's line moves every record's quanta, a body's and a free record's alike, and a Node told to report (a detector set's Node, an open face's layer) reports each quantum standing on it to its body (the `gather` line); the record ends where its last quantum left it. The books balance: held content initial + measured == current + spent + escaped; transit released == current + absorbed + escaped."""

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
    THE_ADVANCE,
    THE_INVERSE,
    THE_REWRITE,
    THE_UNHOLD,
    coefficients,
    form_term,
    rule3,
)
from event_universe.events import after_step, assembly, body_language, guards, output, record_well
from event_universe.events import live as live_records
from event_universe.events import momentum_reading as momentum
from event_universe.events.free_record import scaled_to_one_quantum
from event_universe.events.geometry import GameBoardGeometry, PairView
from event_universe.events.inverse import block_clock_inverse
from event_universe.events.output import ZERO, Ratio, ratio_sum
from event_universe.events.output import form_json as form_json
from event_universe.events.records import Block, DetectorLawLayer, Ledger, LiveRecord
from event_universe.features import self_source
from event_universe.features import signed_read as sr
from event_universe.features.counts_line import CountStart, CountTerm, CountWrites, Levels
from event_universe.features.giving import (
    THE_BIRTH,
    THE_WRITE,
    GivingOwn,
    GivingStart,
    GivingTerm,
    GivingWrites,
)
from event_universe.features.hold import HoldOwn, HoldStart, HoldTerm, HoldWrites, booking
from event_universe.features.receive import Link, ReceiveStart, ReceiveTerm, ReceiveWrites, TwistRead
from event_universe.features.receive import triple as receive_triple
from event_universe.features.recoil import TAKING, RecoilOwn, RecoilStart, RecoilTerm, RecoilWrites
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
FAMILY_TERMS = (
    "the pair",
    "the degree",
    "the phase",
    "the send",
    "the receive",
    "the wait",
    "the operation",
)


HoldMap = dict[tuple[int, int], HoldWrites]  # the hold's writes by (family, body) between its two phases


class DetectorLawSimulation(GameBoardGeometry[Block]):
    """One world under the engine, stepped interval by interval."""

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
    )

    next_identity = 1
    next_held = 0

    # The state the assembly fills once from the parsed world (`events/assembly.py`): the names and types
    held: list[list[int]]
    detector_names: list[str]
    detector_measured: list[int | None]
    detector_face: list[bool]
    detector_set: list[str]
    detector_channel: list[int]
    detector_at_node: np.ndarray
    set_block: dict[int, int]
    set_detectors: list[int]
    set_nodes: dict[int, np.ndarray | None]
    face_detector: int | None
    lifetime_detector: int | None
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
    _axis_effective: dict[int, tuple[int, bool, tuple[np.ndarray, ...] | None]]
    _sourced_ever: dict[tuple[int, int], bool]
    span_masks: dict[int, np.ndarray]
    span_hold: dict[tuple[int, int], HoldOwn]  # a span body's remainders of the hold by (family, number)
    records: dict[int, LiveRecord]
    _kind_walls: dict[tuple[int, int, int], int]
    dead: list[int]
    blocks: list[Block]
    block_by_number: dict[int, Block]
    _pairs: dict[tuple[int, int, int], tuple[np.ndarray, np.ndarray]]
    kind_wrap: list[tuple[bool, bool, bool]]
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
        )
        assembly.detectors(self, world)
        self.lifetime_detector = (
            self._detector("lifetime", None, True)
            if any(row.lifetime is not None for row in world.families)
            else None
        )
        assembly.universe_values(self, world)
        self._recoils: list[tuple[int, int, tuple[int, int, int], int]] = []
        self.recoil_turns: dict[int, list[int]] = {}
        assembly.state_arrays(self, world)
        self.kind_num = PairView(self, 0)
        self.kind_den = PairView(self, 1)
        assembly.bodies(self, world)
        assembly.held_records(self)
        self.register = self._engine_register()
        self.register.check_step(world.step)
        self.register.check_writers(world.step)
        self.register.check_terms(self.family_terms())
        self.main_loop = MainLoop.plan(
            self.register, world.step, self._stages(), self.CHAIN, self.family_terms()
        )
        self.write = self.register.at("the write", "any")
        self._hold(self.register.at("the hold", "(iv)"), THE_ADVANCE)
        assembly.start_at_rest(self)

    def _block(
        self,
        number: int,
        entry: MeasuredDefinition,
        definition: BlockDefinition,
        corner: list[int],
        mask: np.ndarray,
    ) -> Block:
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
        block.spin_before = list(definition.spin_before)
        block.momentum_before = [int(component) for component in entry.momentum_before]
        return block

    def _engine_register(self) -> Register:
        """The register filled from the features' folders and bound to this loop: a built primitive's function is its folder's or the loop's method of today; a row not built has none."""
        register = discover()
        register.bind(self)
        return register

    def _stages(self) -> dict[str, Stage]:
        """The loop's whole-board stages by the file's names, each with the words it takes and the cards whose writes it carries (the records' pass carries the chain's cards)."""
        return {
            "the count's line": Stage(self._counts_stage, (), ("the count's line",)),
            "the hold": Stage(self._hold_stage, ("advance",), ("the hold",)),
            "the operation": Stage(self._records_stage, (), self.CHAIN),
            "the giving": Stage(self._giving_stage, (), ("the giving",), creates=True),
            "the source": Stage(self._source_stage, (), ("the source",)),
            "the recoil": Stage(self._recoil_stage, (), ("the recoil",)),
            "the lifetime": Stage(self._lifetime_stage, (), ("the lifetime",)),
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
    _detector = live_records.add_detector
    _release = live_records.release
    _lifetime_stage = after_step.lifetime_stage
    _block_clock_inverse = block_clock_inverse
    _write_line = after_step.write_line
    _record_form = record_well.record_form
    _read_momentum = momentum.read_momentum

    def _counts_stage(self, function: Callable[..., None]) -> None:
        """THE COUNT'S LINE FOR EVERY RECORD (the model owner's word of 2026-09-29 on #1495, finding 10; ALGEBRA.md #the-counts-line): each body's quanta moved by its record's current through its Nodes' Ports, then every free record's count by its own current, each followed by the reports at the Nodes told to report (`_report`)."""
        for block in self.blocks:
            self._counts_act(function, block, 1)
        reporting = self.reporting_nodes()
        for identity in list(self.records):
            live = self.records[identity]
            if live.counts is None or live.reported:
                continue
            self._report(live, reporting, self._free_counts_act(function, live, 1))

    def _line_act(
        self,
        line: Callable[..., object],
        family: int,
        pair: tuple[int, int],
        live: LiveRecord,
        counts: tuple[np.ndarray, np.ndarray],
        direction: int,
    ) -> tuple[CountWrites, list[tuple[np.ndarray, ...] | None], int]:
        """One act of the count's line on one record's count (ALGEBRA.md #the-counts-line): the line's term (the count's wall of the family at the rest pair, the current's weight the family's common wall, the amplitude bound, the largest count), the record's levels here and across the six Ports (the Ports' arrivals), the count and its remainder stepped forward or back (the direction +1 or -1); the writes, the arrivals read and the weight."""
        wall, wrap = self.kind_wall(family, pair), self.kind_wrap[family]
        term = CountTerm(
            self.pair_count_wall(pair, f"a record of {self.families[family].name!r}"),
            wall,
            self.world.amplitude_bound,
            int(counts[0].max()),
        )
        levels = (live.now, live.before, live.im_now, live.im_before)
        arrived = [None if a is None else self.ports.arrivals(a, wrap) for a in levels]
        links = tuple(Levels(*(None if a is None else a[port] for a in arrived)) for port in range(6))
        start = CountStart(counts[0], counts[1], Levels(*levels), links, direction)
        return cast(CountWrites, line(term, start, None)), arrived, wall

    def _counts_act(self, line: Callable[..., object], block: Block, direction: int) -> None:
        """THE COUNT'S LINE ON A BODY (ALGEBRA.md #the-counts-line): the line's levels laid at its first act (`_lay_count`: at every Node T c + r the Node's share of the record's form plus the origin T / 2), then per interval the line's act on the body's own record (`_line_act`), the body's Nodes then the Nodes where its count stands (`_follow_count`)."""
        live = block.own
        if live is None:
            return
        if block.counts is None or block.count_remainder is None:
            block.counts, block.count_remainder = self._lay_count(block, live)
        pair = block.definition.pair
        found = (block.counts, block.count_remainder)
        writes, arrived, wall = self._line_act(line, block.family, pair, live, found, direction)
        block.counts, block.count_remainder = writes.count, writes.remainder
        self._follow_count(block)
        if direction > 0:
            self._read_momentum(block, arrived, wall)

    def _free_counts_act(
        self, line: Callable[..., object], live: LiveRecord, direction: int
    ) -> CountWrites:
        """THE COUNT'S LINE ON A FREE RECORD (the model owner's word of 2026-09-29 on #1495, finding 10): the same act as a body's (`_line_act`) on the record's own count, laid at its birth (`_emit`), the count and its remainder written back."""
        assert live.counts is not None and live.count_remainder is not None
        pair = self.record_pair(live)
        found = (live.counts, live.count_remainder)
        writes, _, _ = self._line_act(line, live.family, pair, live, found, direction)
        live.counts, live.count_remainder = writes.count, writes.remainder
        return writes

    def record_pair(self, live: LiveRecord) -> tuple[int, int]:
        """The rest pair a free record steps with: its own, or its family's declared pair."""
        pair = live.pair if live.pair is not None else self.families[live.family].pair
        return int(pair[0]), int(pair[1])

    def reporting_nodes(self) -> np.ndarray:
        """THE NODES TOLD TO REPORT (ALGEBRA.md #the-counts-line, the free record): per Node the detector that reports there, -1 elsewhere: every detector set's Nodes (a set bound to a body without positions at the body's current Nodes) and the open faces' slab; a body's own Nodes report nothing (its count there is its family's level, nothing is handed over)."""
        reporting = np.full(self.shape, -1, dtype=np.int64)
        for detector in self.set_detectors:
            nodes = self.set_nodes.get(detector)
            if nodes is None and detector in self.set_block:
                nodes = self.block_by_number[self.set_block[detector]].mask
            elif nodes is None:
                nodes = self.detector_at_node == detector
            reporting[nodes] = detector
        if self.face_detector is not None:
            reporting[self.detector_at_node == self.face_detector] = self.face_detector
        return reporting

    def _report(self, live: LiveRecord, reporting: np.ndarray, writes: CountWrites) -> None:
        """A REPORTING NODE REPORTS (the model owner's word of 2026-09-29 on #1495, finding 10: a detector is a Node told to report the count arriving; ALGEBRA.md #the-counts-line, the free record): at every Node told to report where the record's count stands at 1 or more, each quantum standing there is handed to the detector's body on its `gather` line, the taker's recoil queued with the line's travel into that Node this interval, and the count there lowered by one per quantum, the remainder kept; a record that reported this interval and whose count stands below 1 at every Node after the reports ends, the quanta it still carries booked as escaped (none where its count summed to its quanta)."""
        assert live.counts is not None
        standing = np.argwhere((reporting >= 0) & (live.counts >= 1))
        if not len(standing):
            return
        counts, reported = live.counts.copy(), False
        for found in standing:
            node = (int(found[0]), int(found[1]), int(found[2]))
            detector = int(reporting[node])
            travel = (
                int(writes.travel[0][node]),
                int(writes.travel[1][node]),
                int(writes.travel[2][node]),
            )
            for _ in range(int(counts[node])):
                self._gather_line(live, detector, node)
                self._recoil_at_taking(live, detector, travel)
                counts[node] -= 1
                reported = True
        live.counts = counts
        if reported and not bool((counts >= 1).any()):
            self.ledger.transit_escaped[live.family] += live.content
            live.content, live.reported = 0, True
            self.dead.append(live.identity)

    def _follow_count(self, block: Block) -> None:
        """THE BODY'S NODES ARE WHERE ITS COUNT STANDS (ALGEBRA.md #what-a-body-is (c), the surface rule): after the line the body's set is the Nodes whose count is not 0, its corner the set's lower corner, so the shell that reads its clicks moves with its quanta; the line alone moves it."""
        if block.counts is None:
            return
        standing = block.counts != 0
        if not bool(standing.any()) or np.array_equal(standing, block.mask):
            return
        block.mask = standing
        block.corner = [int(low) for low in np.argwhere(standing).min(axis=0)]

    def _body_count(self, block: Block) -> int:
        """The count at the body, its quanta: the declared count per Node over its Nodes (the record's norm in quanta, ALGEBRA.md #what-a-body-is; the count's line moves them between the Nodes and loses none)."""
        return self.body_quanta(block, self.world.measured[block.number].amount)

    def count_wall(self, block: Block) -> int:
        """THE COUNT'S WALL of a body (`pair_count_wall` at the body's rest pair)."""
        return self.pair_count_wall(block.definition.pair, f"the body {block.number}")

    def pair_count_wall(self, pair: tuple[int, int], who: str) -> int:
        """THE COUNT'S WALL W_c = 3 den T (issue #1495 finding 6): the family's plain wall at the rest pair times the universe's one T, refused by name where the files declare no T."""
        action = self.world.quantum_action
        if action < 1:
            raise ValueError(
                f"{who} carries a record and the universe declares no quantum_action T: "
                "the count's wall is 3 den T (ALGEBRA.md #the-counts-line, #a-familys-declaration)"
            )
        return 3 * int(pair[1]) * action

    def count_share(
        self, family: int, pair: tuple[int, int], levels: list[tuple[np.ndarray, np.ndarray]]
    ) -> np.ndarray:
        """The record's form's share at every Node in the current's units, E_i / 2 = 3 den (now^2 + before^2) - num now S_6(before) over the record's level pairs (ALGEBRA.md #the-counts-line; issue #1495 finding 6): the form's Node term at the plain wall 3 den less the Link term by the read act with the level as the coefficient, core.rule3 alone; its change over one interval is the six Ports' currents exactly in the vacuum, and a body laid by it stands (the pace-weighted share, exact at every Node, lays a body that flows out: the Paper Writer's measurement of 2026-09-29)."""
        weight = self.kind_wall(family, pair)
        wrap = self.kind_wrap[family]
        share = np.zeros(self.shape, dtype=np.int64)
        for now, before in levels:
            share += form_term(0, 3 * int(pair[1]), now, before)
            arrived = self.ports.arrivals(before, wrap)
            sums = (arrived[0] + arrived[1], arrived[2] + arrived[3], arrived[4] + arrived[5])
            share -= rule3((weight * now,) * 3, sums, 0, 1, 0, 0, 0)[0]
        return share

    @staticmethod
    def level_pairs(live: LiveRecord) -> list[tuple[np.ndarray, np.ndarray]]:
        """A record's level pairs, (now, before) and the second level's where it has one."""
        pairs = [(live.now, live.before)]
        if live.im_now is not None and live.im_before is not None:
            pairs.append((live.im_now, live.im_before))
        return pairs

    def lay_count(
        self, family: int, pair: tuple[int, int], levels: list[tuple[np.ndarray, np.ndarray]]
    ) -> tuple[np.ndarray, np.ndarray]:
        """THE COUNT'S LAY (ALGEBRA.md #the-counts-line, THE COUNT IS THE RECORD'S FORM; issue #1495 finding 6): at every Node W_c c_i + r_i = E_i / 2 + W_c div 2 by Rule3's division act, W_c div 2 the remainder's origin; a body's lay and a free record's alike, no gate here."""
        wall = self.pair_count_wall(pair, f"a record of {self.families[family].name!r}")
        share = self.count_share(family, pair, levels)
        counts, remainder = rule3(NO_READ, NO_READ, 1, wall, 0, 0, share + wall // 2)
        return counts.astype(np.int64), remainder.astype(np.int64)

    def _lay_count(self, block: Block, live: LiveRecord) -> tuple[np.ndarray, np.ndarray]:
        """A BODY'S LAY (`lay_count` at the body's rest pair): the declared count is a reading, refused by name where it is off the laid total by more than 2 isqrt(c) + 1 ((|c - laid| - 1) div 2 squared above c, no root)."""
        counts, remainder = self.lay_count(block.family, block.definition.pair, self.level_pairs(live))
        declared, laid = self._body_count(block), int(counts[block.mask].sum())
        off = abs(declared - laid)
        if off > 1 and ((off - 1) // 2) ** 2 > declared:
            raise ValueError(
                f"the body {block.number} declares the count {declared} and its record's form lays "
                f"{laid} quanta at its Nodes at T = {self.world.quantum_action}: a declared count is within "
                "2 isqrt(c) + 1 of SUM D_i div T (ALGEBRA.md #the-counts-line, THE COUNT IS THE RECORD'S FORM)"
            )
        return counts, remainder

    def _hold_stage(self, function: Callable[..., None], advance: bool) -> None:
        """The hold's two acts: at the interval's start the moved bodies' Nodes rewritten; after the records, the held families' own step, the hold and the pace guard."""
        if advance:
            self._advance_fields(function)
        else:
            self._hold(function, THE_REWRITE)

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
            of, weight, scale = definition.sourced
            writes = cast(
                SourceWrites,
                function(
                    SourceTerm(family, of, weight, scale),
                    SourceStart(self.shape, self._source_argument[of], self._write_line),
                    SourceOwn(self._source_remainders[family]),
                ),
            )
            self._sourced_record(family).now[writes.at] += writes.integers[writes.at]
            self._source_remainders[family] = writes.remainders
        for argument in self._source_argument.values():
            argument[...] = 0

    def _write_at_mask(
        self, live: LiveRecord, mask: np.ndarray, levels: tuple[np.ndarray, np.ndarray], sign: int
    ) -> None:
        """The loop's one site for levels written at a body's Nodes into a record's two levels, added (+1) or taken back (-1): the recoil's turn (the write's gate)."""
        live.now[mask] += sign * levels[0]
        live.before[mask] += sign * levels[1]

    def _recoil_stage(self, function: Callable[..., object]) -> None:
        """The recoil's act (features/recoil): per click of the interval on a body with a record of its own, a mode clock and a mode reading of the quantum's wave number on a world with a twist table, the folder's turn of the record's two levels at the body's Nodes by delta k = sigma_a (k_q div M) per Link along each axis with a tally (the Node's offset from the body's centre; the triple the receive's reading of the table), the angle's remainder carried at the body through the write's line, the taker at +1 (a report's recoil), the turned levels written at the loop's one site (`_write_at_mask`); a body without them takes no recoil; the momentum n is a reading of the record's current (`_read_momentum`), no level of the click's."""
        for number, sense, tally, identity in self._recoils:
            block = self.block_by_number.get(number)
            if block is None or block.own is None or block.definition.emitter is None:
                continue
            emitter, live = block.definition.emitter, block.own
            clock, sine = block.definition.clock, block.definition.clock_sine
            if (
                emitter.wave_number is None
                or clock is None
                or sine is None
                or self._receive_term is None
            ):
                continue
            nodes, centre = np.argwhere(block.mask), self._window_centre(block)
            offsets = tuple(tuple(int(v) for v in nodes[:, axis] - centre[axis]) for axis in range(3))
            before = (live.now[block.mask].copy(), live.before[block.mask].copy())
            levels = tuple(tuple(int(v) for v in level) for level in before)

            def triple_of(k: int, axis: int) -> tuple[int, int, int]:
                c, sine, d = receive_triple(self._receive_term, k, port_of(axis, 1))
                return int(c), int(sine), int(d)

            term = RecoilTerm(
                emitter.wave_number, self._body_count(block), clock, sine, sense, triple_of
            )
            values = {k[1:]: v for k, v in block.hold_value.items() if k[0] == "recoil"}
            carries = {k[1:]: v for k, v in block.hold_carry.items() if k[0] == "recoil"}
            start = RecoilStart(
                tally, (levels[0], levels[1]), (offsets[0], offsets[1], offsets[2]), self._write_line
            )
            writes = cast(RecoilWrites, function(term, start, RecoilOwn(values, carries)))
            turned = tuple(np.asarray(level, dtype=np.int64) for level in writes.levels)
            self._write_at_mask(live, block.mask, (turned[0] - before[0], turned[1] - before[1]), 1)
            body_language.recoil(self, block, number, sense, identity, tally, before, writes)
        self._recoils.clear()

    def _records_stage(self, function: Callable[..., None]) -> None:
        """The records' act: the bodies' own records first, each by the rule alone, then every other live record's step; `function` is the rule the steps apply."""
        for block in self.blocks:
            if block.node_record is None and block.own is None:
                continue
            self._record_form(block)
        for identity in list(self.records):
            live = self.records[identity]
            if live.standing:
                continue
            self._advance(live)

    def _giving_stage(self, function: Callable[..., None]) -> None:
        """THE GIVING FIRES AT THE BODY'S CLICK (the model owner's word of 2026-09-29 on #1495, finding 10: every bound body gives at its click): a body with an emitter and a stock of the given family from 1 gives once when its clock clicked at the last interval's close (`new_cycle`, `_block_clock`), the click then spent; `function` is the folder's `apply`."""
        for block in self.blocks:
            if block.new_cycle and block.definition.emitter is not None and self.stock_of(block) >= 1:
                self._emit(block, function)
                block.new_cycle = False

    def _spins_stage(self, function: Callable[..., None]) -> None:
        """The spin's step's act: each body's spin from the fields as the interval leaves them."""
        for block in self.blocks:
            self._spins_act(function, block, False)

    def close_interval(self) -> None:
        """The interval's closing: each body's clock, the ended records deleted whole, then the host's probe and mode readings."""
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
        """The primitives each family of the run declares, as (label, name) pairs read from its attributes (the loader's words of today; the term form [name, target, of, degree, weight, table] of ALGEBRA.md #the-primitives is the loader's next cut): every family the shape and the step's four words; `reads` the signed read; `held` the hold; `self_source.unit` the self-source; `lifetime` the lifetime."""
        terms: list[tuple[str, str]] = []
        for index, family in enumerate(self.families):
            label = f"universe.families[{index}]"
            terms.extend((label, name) for name in FAMILY_TERMS)
            if family.reads:
                terms.append((f"{label}.reads", "the signed read"))
            if family.held is not None:
                terms.append((f"{label}.held", "the hold"))
            if family.self_unit > 0:
                terms.append((f"{label}.self_source", "the self-source"))
            if family.lifetime is not None:
                terms.append((f"{label}.lifetime", "the lifetime"))
        for number, entry in enumerate(self.world.measured):
            if entry.block is not None and entry.block.emitter is not None:
                terms.append((f"measured[{number}].emitter", "the giving"))
        return terms

    def wall_of(self, block: Block) -> int:
        """THE ONE WALL OF A BODY (ALGEBRA.md #the-primitives, #the-well): W = 3 Q M, Q the universe's momentum unit and M the body's quanta as it holds them now (its own and its stocks, ALGEBRA.md #the-paces; a click moves M, ALGEBRA.md #the-interval, #the-primitives); the hop, the holds' divisions and the recoil read this one wall, the momentum's whole part n on it the body's velocity n / W in Links per interval."""
        return 3 * self.momentum_unit * sum(self.held[block.number])

    def _held_part(self, position: int, family: int, part: int) -> LiveRecord:
        """A held family's component record over the board (item 51; ALGEBRA.md #the-interval): its identity the next name below the bodies' own (-1 - number), one per held family and part; its pair the one its family's row declares (`pair` None reads it), no shortcut."""
        self.next_held += 1
        del position  # the held families' order names the identity alone
        return LiveRecord(
            -len(self.world.measured) - self.next_held,
            family,
            0,
            self.tick,
            0,
            np.zeros(self.shape, dtype=np.int64),
            np.zeros(self.shape, dtype=np.int64),
            np.zeros(self.shape, dtype=np.int64),
            part=part,
            held_part=True,
        )

    def held_component_records(self) -> list[LiveRecord]:
        """Every held family's component records in the declared order, the time part first, then the other parts (the interval's field step)."""
        found: list[LiveRecord] = []
        for family, record in self.held_records.items():
            found += [record, *self.held_parts[family]]
        return found + list(self.sourced_records.values())

    def body_source(self, number: int, source: str) -> int:
        """A body's declared source for a held family (item 51): its content, the quanta it holds of every family ("content", ALGEBRA.md #the-counts-line), or its signed charge Q ("sign", ALGEBRA.md #the-paces)."""
        return self._body_charge(number) if source == "sign" else sum(self.held[number])

    def node_sources(self, number: int, source: str) -> list[tuple[tuple[int, int, int], int]]:
        """A body in the law's form: its source per Node, the count laid THERE by the count's line (the declared count at the first act, then the record's form over its whole period, THE COUNT IS THE RECORD'S FORM OVER ITS PERIOD; never the well of one interval) or the count declared there before any lay ("content"), or the family's charge times it ("sign"), ALGEBRA.md #what-a-body-is and the hold's row, the quanta where the count's line moved them; a body with a record under a declared T its well's form, D_i div T at every Node of its record (`_record_form`), its declared count a reading; empty for a body of the old form with no well, whose one source stands at every Node of its mask."""
        block = self.block_by_number.get(number)
        if block is None or (block.well is None and not block.definition.counts):
            return []
        weight = 1 if source == "content" else block.definition.q + self.families[block.family].charge[0]
        laid = block.well if block.well is not None else block.counts
        if laid is not None:
            moved = zip(*np.nonzero(laid), strict=True)
            return [((int(x), int(y), int(z)), weight * int(laid[x, y, z])) for x, y, z in moved]
        nodes, counts = block.definition.nodes or (), block.definition.counts or ()
        return [(node, weight * int(count)) for node, count in zip(nodes, counts, strict=True)]

    def _hold(
        self, line: Callable[..., object], act: str, held: HoldMap | None = None, body: int | None = None
    ) -> HoldMap:
        """The hold in two phases, both in the forward order and apart at the inverse (`step_inverse`). The first: at every body's Nodes a held family's level gains the body's count over the row's divisor each interval, the folder's carried division, and at a body in the law's form (ALGEBRA.md #what-a-body-is; ENGINE.md the `nodes` row) each Node gains the count declared THERE over the divisor with a remainder of its own, never the whole body's count at every Node (a wall of 460 Nodes at 8,000 would source 3.68 million at each), a signed source the family's charge times the Node's count (the count a source into the field's line, ALGEBRA.md #the-primitives the row "the hold"), subtracted on the inverse; one call per body and held family with the act the loop names (the advance, the rewrite of a moved body's Nodes, the inverse), a body with a block by `_held_writes`, a span body (no block) its time part alone by the same line on its own remainders (`span_hold`); `node_level` is then each held family's level as every reading family's step reads it; the inverse returns here with the writes. The second, from the first's writes `held`: the vector and tensor parts at the bodies (ALGEBRA.md #the-interval), the body's numbers times the held factors over the wall, the remainder carried, at every Node of the body at both levels (the interval's start rewrites a moved body's Nodes alone), then the dipoles on the body's Node's six neighbours (forward with the division advanced, at the inverse with the values the unhold stepped back; none beyond an open face). A body whose well is its record's form steps its first phase back apart, `body`, after its record stepped back and laid the counts the forward hold read (`step_inverse`)."""
        if held is None or body is not None:
            self.ports.begin()
            held = {} if held is None else held
            for number in range(len(self.held)) if body is None else (body,):
                block = self.block_by_number.get(number)
                if body is None and act == THE_INVERSE and block is not None and block.well is not None:
                    continue
                for family, record in self.held_records.items():
                    definition = self.families[family]
                    source = cast(str, definition.held)
                    if self.body_source(number, source):
                        self._sourced_ever[(family, 0)] = True
                    if act == THE_REWRITE and not (block is not None and block.moved):
                        continue
                    if block is not None:
                        if act == THE_INVERSE and self.held_parts[family]:
                            unhold = self._held_writes(line, block, family, THE_UNHOLD)
                            for (i, j, s), value, _ in unhold.dipoles:
                                node = self._dipole_node(self._centre_node(block), family, j, s)
                                if node is not None:
                                    self.held_parts[family][i].now[node] -= value
                        w = self._held_writes(line, block, family, act)
                    else:
                        divisor = cast(int, definition.held_divisor)
                        term = HoldTerm(source, (1,), (definition.held_factors[0],), None, 1, divisor)
                        count = self.body_source(number, source)
                        start = HoldStart(act, count, (0, 0, 0), 1, None, (), self._write_line)
                        own = self.span_hold.get((family, number), HoldOwn({}, {}))
                        w = cast(HoldWrites, line(term, start, own))
                        self.span_hold[(family, number)] = w.own
                    held[(family, number)] = w
                    sign = -1 if act == THE_INVERSE else 1
                    for key, level in w.node_levels:
                        node = cast(tuple[int, int, int], key[1:])
                        record.now[node] = int(record.now[node]) + sign * level
                    if not w.node_levels:
                        mask = block.mask if block is not None else self.span_masks[number]
                        record.now[mask] += sign * w.time_level
            for family, record in self.held_records.items() if body is None else ():
                self.node_level[family] = record.now
            if act == THE_INVERSE:
                return held
        for family in self.held_records:
            source = cast(str, self.families[family].held)
            if not self.held_parts[family]:
                continue
            for block in self.blocks:
                writes = held.get((family, block.number))
                if writes is None:
                    continue
                m = self._momentum_now(block)
                for part, at, value, before in writes.parts:
                    record = self.held_parts[family][part - 1]
                    degree = self.main_loop.function_of("the degree", "(i)")
                    group, axes = degree(self.families[family].parts, part)
                    factor = self.families[family].held_factors[group]
                    count = self.body_source(block.number, source)
                    if booking(factor, count, (int(m[0]), int(m[1]), int(m[2])), axes):
                        self._sourced_ever[(family, part)] = True
                    if value == 0 and before == 0 and record.silent:
                        continue
                    record.silent = False
                    where = block.mask if at is None else cast(tuple[int, int, int], at[1:])
                    record.now[where], record.remainder[where] = value, 0
                    record.before[where] = before
                centre = self._centre_node(block) if writes.dipoles else []
                for (i, j, sigma), value, before in writes.dipoles if act != THE_REWRITE else ():
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
        return held

    def _held_writes(
        self, line: Callable[..., object], block: Block, family: int, act: str
    ) -> HoldWrites:
        """One body's hold into one held family by the hold's line, the act named by the loop: the family's row, the body's count, its momentum now, its wall and its dipole's vector, and its remainders of the family under the line's keys (a part's index, ("d", i, j, sigma) a dipole's term), written back after the call; a dipole's term beyond an open face is dropped with its Node (ALGEBRA.md #the-interval)."""
        row = self.families[family]
        source = row.held
        assert source is not None
        values: dict[tuple[object, ...], int] = {}
        carries: dict[tuple[object, ...], int] = {}
        for stored, found in ((block.hold_value, values), (block.hold_carry, carries)):
            for key, value in stored.items():
                if key[0] == family or (key[0] == "d" and key[1] == family):
                    found[key[1:] if key[0] == family else ("d", *key[2:])] = value
        dipole = block.spin if row.held_dipole == "spin" else block.definition.moment
        vector = None if row.held_dipole is None else (int(dipole[0]), int(dipole[1]), int(dipole[2]))
        momentum = self._momentum_now(block)
        sources = self.node_sources(block.number, source)
        per_node = tuple((("n", *node), value) for node, value in sources)
        parts, factors, divisor = tuple(row.parts), tuple(row.held_factors), cast(int, row.held_divisor)
        term = HoldTerm(source, parts, factors, row.held_dipole, row.held_dipole_div, divisor)
        count = self.body_source(block.number, source)
        n = (int(momentum[0]), int(momentum[1]), int(momentum[2]))
        start = HoldStart(act, count, n, self.wall_of(block), vector, per_node, self._write_line)
        writes = cast(HoldWrites, line(term, start, HoldOwn(values, carries)))
        centre = self._centre_node(block) if any(key[0] == "d" for key in writes.own.values) else []
        for stored, written in (
            (block.hold_value, writes.own.values),
            (block.hold_carry, writes.own.carries),
        ):
            for key, value in written.items():
                if key[0] != "d":
                    stored[(family, *key)] = value
                elif self._dipole_node(centre, family, *cast(tuple[int, int], key[2:4])) is not None:
                    stored[("d", family, *key[1:])] = value
        return writes

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
        self._hold(hold, THE_ADVANCE)
        paces = self._card_writes("the signed read")
        with self.main_loop.act(
            "the signed read",
            "(i)",
            paces,
            lambda: {},
        ):
            self._guard()

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
        """A body's charge Q (ALGEBRA.md #the-paces): the sum of the signs of the quanta it holds, an integer of either sign, moved with the labels at the clicks (the held books)."""
        block = self.block_by_number.get(number)
        declared = block.definition.q * sum(self.held[number]) if block is not None else 0
        return declared + sum(
            sign * quanta for sign, quanta in zip(self.family_charge, self.held[number], strict=True)
        )

    def stock_of(self, block: Block) -> int:
        """THE STOCK of the family a body gives (ALGEBRA.md #the-paces, #the-primitives): its held quanta of another family; of its own family, its declared `stock` less its givings (each giving lowered M by one, the held count of its own)."""
        emitter = block.definition.emitter
        assert emitter is not None
        if emitter.family == block.family:
            return block.definition.stock - block.givings
        return self.held[block.number][emitter.family]

    def _momentum_now(self, block: Block) -> list[int]:
        """The block's momentum at this interval: the declared P, or under a ramp the whole part P x t // ramp until the ramp ends (the pushing agent's declaration)."""
        ramp = block.definition.ramp
        elapsed = self.tick - block.definition.start
        if elapsed < 0:
            return [0, 0, 0]
        if ramp <= 0 or elapsed >= ramp:
            return list(block.momentum)
        return [component * elapsed // ramp for component in block.momentum]

    # THE BODIES ON ONE NODE (ALGEBRA.md #the-interval, #a-familys-declaration, #the-primitives; the one stroke, commit 6): the spin's step, written once for any body and any read (the feed and the induction left: derived, ALGEBRA.md #the-primitives)

    def _spins_act(self, line: Callable[..., object], block: Block, inverse: bool) -> None:
        """THE BODY'S STEP AT (v): the spin's step's line (features/spins_step) on the body from the fields as the interval leaves them (per read with a dipole the read family's vector part and, for the spin's dipole, its time part at the body's Node's six neighbours with the row's two weights), the body's momentum, wall, spin and spin before and its remainders under the line's keys; the writes the spin, the spin before and the remainders back; a body with no spin and no moment reads no spin's holder and skips the act (a pixel of the rule's universe, the Closer's ruling of 2026-09-28, 15:32 Israel), and with a moment alone it reads the moment's holder and not a spin's holder without the row: Omega x S vanishes at S = 0, the torque mu x B_q stands (a light's giver of the rule's universe, the Closer's order of 17:04 Israel)."""
        definition = self.families[block.family]
        still = not any((*block.spin, *block.spin_before))
        if not definition.reads or (still and not any(block.definition.moment)):
            return
        centre = self._window_centre(block)
        wrap = self.kind_wrap[block.family]
        reads: list[SpinRead] = []
        for position, (other, weight, by, _) in enumerate(definition.reads):
            read = self.families[other]
            unrowed = still and read.held_dipole == "spin" and read.spin_weights is None
            if len(read.parts) < 2 or read.held_dipole is None or unrowed:
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
        pair = block.hold_value, block.hold_carry
        own = SpinStepOwn(*({k: v for k, v in h.items() if k[0] in KEYS} for h in pair))
        moment = block.definition.moment
        term = SpinStepTerm((int(moment[0]), int(moment[1]), int(moment[2])), self.node_clock)
        writes = cast(SpinStepWrites, line(term, start, own))
        block.spin, block.spin_before = list(writes.spin), list(writes.spin_before)
        block.hold_value.update(writes.own.values)
        block.hold_carry.update(writes.own.carries)

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
        """THE ONE RULE AT THE BODY'S NODE (ALGEBRA.md #what-a-body-is; item 42): the integers the body's Node's record is stepped with, (num, den, Gamma, c): the body's Node's pair this interval as [num_c, 2 den_c] (`node_record_clock`: the body's clock pair in the rule's convention, 2 cos omega = num_c / den_c, the proper pair of its momentum on a moving body), the world's Gamma and the body's Node's own effective content c (Gamma - p at the body's centre Node, the family of clicks' level less the charge's read, uniform over its Nodes); the wall 3 den Gamma = 6 den_c Gamma."""
        num_c, den_c = self.node_record_clock(block)
        centre = tuple(int(axis[0]) for axis in np.nonzero(self.centre_mask(block)))
        return num_c, 2 * den_c, self.node_clock, int(self._effective_content(block.family)[centre])

    def node_record_coefficients(self, block: Block) -> tuple[int, int]:
        """The one rule's coefficients at the body's Node with the six reads returning the body's Node (S_6 = 6 a): (the coefficient on a, the wall) = (6 num (Gamma - c) + 6 den c, 3 den Gamma) = (6 num_c p + 12 den_c c, 6 den_c Gamma), six times ALGEBRA.md #what-a-body-is's (K, den_c Gamma): the same rotation as rationals (ALGEBRA.md #what-a-body-is)."""
        num, den, gamma, content = self.node_record_rule(block)
        reads, self_coefficient, wall = coefficients(num, den, gamma, content)
        return 6 * reads[0] + self_coefficient, wall

    def _advance_node_record(self, block: Block, direction: int = 1) -> None:
        """One interval of the body's Node record by rule3 in `direction`, its six reads its own level, (2 a, 2 a, 2 a); the amplitude bound as the rows' (ALGEBRA.md #what-a-body-is, #the-direction)."""
        node_record = block.node_record
        assert node_record is not None
        num, den, gamma, content = self.node_record_rule(block)
        reads, self_coefficient, wall = coefficients(num, den, gamma, content)
        forward = direction == 1
        now, other = (
            (node_record.now, node_record.before) if forward else (node_record.before, node_record.now)
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

    def node_record_form(self, block: Block) -> int:
        """The body's Node's record's invariant (ALGEBRA.md #what-a-body-is): e = wall (a^2 + b^2) - coefficient a b, the one rule's own at the body's Node (a' = (coefficient / wall) a - b leaves it fixed); constant between the remainders' jitter (GAMEBOARD)."""
        node_record = block.node_record
        assert node_record is not None
        coefficient, wall = self.node_record_coefficients(block)
        return (
            wall * (node_record.now * node_record.now + node_record.before * node_record.before)
            - coefficient * node_record.now * node_record.before
        )

    def _emit(self, block: Block, function: Callable[..., object]) -> None:
        """THE GIVING AT THE BODY'S CLICK (the model owner's word of 2026-09-29 on #1495, finding 10; ALGEBRA.md #the-counts-line, the free record): the given record's two levels written once at the body's Nodes by the giving's write at the emitter's weight g (the body's rotation now and before), scaled by the generator's act so that the count its form lays over the board is exactly one quantum (`scaled_to_one_quantum`), its count laid by the same act a body's is (`lay_count`), and the birth: the given family's content at the body falls by one, the books with it; the giving line names the record."""
        emitter = block.definition.emitter
        assert emitter is not None
        family, number = emitter.family, block.number
        pair = self.families[family].pair
        term = GivingTerm((emitter.weight, 1), family)
        levels = (self._body_levels(block), self._body_levels(block, before=True))
        written = cast(
            GivingWrites,
            function(term, GivingStart(THE_WRITE, 0, levels, self._write_line), GivingOwn()),
        )
        assert written.level is not None
        now, before = np.zeros(self.shape, dtype=np.int64), np.zeros(self.shape, dtype=np.int64)
        now[block.mask], before[block.mask] = written.level[0], written.level[1]

        def laid(a: np.ndarray, b: np.ndarray) -> int:
            return int(self.lay_count(family, pair, [(a, b)])[0].sum())

        label = f"measured[{number}].emitter"
        now, before = scaled_to_one_quantum(now, before, laid, self.world.amplitude_bound, label)
        counts, remainder = self.lay_count(family, pair, [(now, before)])
        born = cast(
            GivingWrites, function(term, GivingStart(THE_BIRTH, int(counts.sum()), None), GivingOwn())
        )
        identity, self.next_identity = self.next_identity, self.next_identity + 1
        block.givings += 1
        live = LiveRecord(
            identity,
            family,
            block.givings,
            self.tick,
            -born.count,
            now,
            before,
            np.zeros(self.shape, dtype=np.int64),
            emitter=number,
            box=self.mask_box(block.mask),
            counts=counts,
            count_remainder=remainder,
            pair=pair,
            part=emitter.part,
            twist=emitter.twist,
        )
        self.held[number][family] += born.count
        self.ledger.held_spent[family] -= born.count
        self.ledger.transit_released[family] += live.content
        block.emitted.append(identity)
        self.records[identity] = live
        self.layer.given += 1
        if self.record is not None:
            self.record(
                {
                    "event": "giving",
                    "tick": self.tick,
                    "measured": number,
                    "family": self.families[family].name,
                    "record": identity,
                    "node": list(block.corner),
                    "content": live.content,
                }
            )

    def _block_clock(self, block: Block) -> None:
        """The block's clock (MASSIVE_RECORD.md sections 4 and 6): its total record summed across its Nodes (G over R: its own record), one count per cycle (the sum's crossing from at most 0 to above 0, verb D's comparison), a `click` line per count; the body's click, read by the giving of the next interval (`new_cycle`)."""
        total = 0
        # the co-moving centre Node (the design's reading of the clock in motion, MASSIVE_RECORD.md section 8: "the clock read at the co-moving centre"): the total record's value there, on the line
        centre = box_centre(block.corner, block.definition.extents, self.shape)
        at_centre = 0
        if block.node_record is not None:
            # the body's Node's record (ALGEBRA.md #what-a-body-is): its level is the standing record's coefficient, the sum over the Nodes and the centre alike
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
            event = {"event": "block", "tick": self.tick, "measured": block.number}
            self.record({**event, "corner": list(block.corner), "sum": total, "centre": at_centre})

    # The inverse map (ALGEBRA.md 8.8): the step is a bijection but for the click; the property test of 9.20 (B) 4 runs it backwards

    def _advance_inverse(self, live: LiveRecord) -> None:
        """One interval of the rule backwards on a record: from (a_next, a_now, r') to (a_now, a_before, r) with 3 den Gamma a_before - r = num SUM_j (Gamma - c_j) a_now,j + 6 den c a_now - (3 den Gamma a_next + r') under the fixed wall (the forward step's integers, the clock field of the interval's start), the remainder in [0, 3 den Gamma), exact at every Node; with a tensor part read, a twist or a second level the arrivals are stepped back per axis after the transport's inverse (`_transport`), both levels."""
        if live.silent:
            return  # a zero held part steps to zero exactly
        num, den = self.pair_arrays(live.family, live.pair)
        field = live.held_part
        gamma = 1 if field else self.node_clock
        content = 0 if field else self._effective_content(live.family)
        # the same integers as the forward step's: the pace on the Node's own sum (item 36) HOST (item 43): the record's box holds the reach of `before`'s rows (it was the window of the step that wrote `now`), so the inverse is read on the box itself, zeros elsewhere; the box stays (a superset)
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
        """One interval backward in the joint inverse's fixed order (the bodies' step back, every family at the interval's start levels, the held families and their hold last); no hop, report or giving in the interval (a report breaks the bijection: the click is the one act the inverse does not undo)."""
        self.ports.begin()
        # the bodies' step back first (ALGEBRA.md #the-interval; commit 6): the momentum and the spin as the interval began, from the fields as it left them
        for block in self.blocks:
            self._spins_act(self.register.at("the spin's step", "(v)"), block, True)
        # the interval's dipole writes taken back first (ALGEBRA.md #the-interval; commit 2): they were the last writes of the forward interval, after the fields' step; then the hold's first phase back at the count the forward hold read (the store stepped back, the time part's increment off the end level) before the count's line returns the quanta
        hold = self.register.at("the hold", "(iv)")
        held = self._hold(hold, THE_INVERSE)
        # the count's line back (its own inverse, the current reversed; ALGEBRA.md #the-counts-line): the quanta return to their Nodes before the records step back
        counts_line = self.register.at("the count's line", "(ii)")
        for block in self.blocks:
            self._counts_act(counts_line, block, -1)
            if block.moved:
                raise ValueError(
                    f"the inverse map is defined for a body whose Nodes stood through the interval (block "
                    f"{block.number} moved at interval {self.tick}; the field moved back through the body, "
                    "ALGEBRA.md #the-primitives, is not built)"
                )
        for live in self.records.values():
            if live.counts is not None and not live.reported:
                self._free_counts_act(counts_line, live, -1)
        # the joint inverse (ALGEBRA.md #the-counts-line; item 51): every family backward at the held levels of the interval's start (their `before` level: the held families stepped last), then the held families backward and their hold
        for family, record in self.held_records.items():
            self.node_level[family] = record.before
        self._effective.clear()
        for identity in list(self.records):
            live = self.records[identity]
            if live.standing:
                continue
            self._advance_inverse(live)
        for block in self.blocks:
            self._record_form(block, -1)
            self._block_clock_inverse(block)
            if block.well is not None:
                self._hold(hold, THE_INVERSE, held, block.number)
        for record in reversed(self.held_component_records()):
            self._advance_inverse(record)
        self._hold(hold, THE_INVERSE, held)
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
        """THE AXIS CONTENTS t_a of a reading family (ALGEBRA.md #the-interval, #the-paces): SUM over its reads of weight x by x (the read family's aa component div 2), one division per read per axis rounded at the read and no remainder kept (the pace is a coefficient of the interval and no level; issue #1495 finding 3), backward the same read on the tensor's before level; None where no read's tensor part was ever sourced, the isotropic rule bit for bit."""
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
                level = record.before if inverse else record.now
                found[axis] += rule3(NO_READ, NO_READ, factor * level, 2, 1, 0, 1)[0]
        result = None if found is None else (found[0], found[1], found[2])
        self._axis_effective[family] = (self.tick, inverse, result)
        return result

    # THE TRANSPORT (ALGEBRA.md #the-transport, #the-interval, #the-primitives; the one stroke, commit 4): the operations, written once for any phase-2 family and any read with a twist

    def _arrival(
        self, a: np.ndarray, axis: int, sigma: int, wrap: tuple[bool, bool, bool]
    ) -> np.ndarray:
        """The level arriving through the Port toward `sigma` on the axis (the wrap on a periodic axis, 0 beyond an open face, the Node itself on a folded axis)."""
        arrived: np.ndarray = self.ports.arrivals(a, wrap)[port_of(axis, sigma)]
        return arrived

    def _twist_reads(self, live: LiveRecord, inverse: bool) -> tuple[TwistRead, ...] | None:
        """THE TWIST READS of a record's family (ALGEBRA.md #the-transport, #the-interval, #the-primitives): per read with a twist whose vector part is not silent, its factor on the record (the weight times the record's own rotation for the twist "own", else the declared twist, by q the family's charge sign) and the read family's vector part at the Node, the `before` levels backward; None where no read turns the transport (the identity, bit for bit) or on a family with one level."""
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
            factor = factor if by == "plain" else factor * sign
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
        """THE SIX ARRIVALS AFTER THE TRANSPORT (ALGEBRA.md #the-transport, #the-interval), summed per axis for the two levels by the receive's line (features/receive): the record's pair at the Node, its family's twist reads and the six Links as the Ports read them (`_arrival`), the `before` levels backward; the second level's sums None while the record has no second level and no rotation writes one. NO REMAINDER IS KEPT ON THE PORT (BUILD.md item 64): the rounding is the line's nearest unit and the inverse recomputes the same arrivals from the `before` levels, exact."""
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
        """THE SELF-SOURCE'S SLOT (ALGEBRA.md #a-familys-declaration, #the-interval, #the-second-level): per family with a unit P_2 above 0, the folder's line (features/self_source) through the register on every level of the family at the interval's start (backward the `before` levels) with its six Links; the step's right side loses w Sigma_self. None at P_2 = 0 (every shipped family). HOST: once per family per interval, before any record of the family steps."""
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

    def kind_wall(self, family: int, pair: tuple[int, int] | None = None) -> int:
        """The family's common wall: the least common multiple of the numerators of its pair over the board (the vacuum's and every body's), so that wall x den_i / num_i is an integer at every Node; HOST: read once per family from the board's pair array and kept until a pair is written (`_write_pair`, the load and a hop), the same integer at every call."""
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
        # the pair's two levels summed (ALGEBRA.md #the-interval; commit 4): the form of each level, the plain Link term (exact where every twist is 0, a reading elsewhere)
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
        """SUM_i node_i / divisor_i over the Nodes of `mask`, exact (one pair per distinct divisor: the rule's read coefficients present are few, the body's and the field's levels; the pairs summed by `rational_sum`)."""
        chosen = divisor[mask]
        values = node[mask]
        return ratio_sum(
            [
                (int(np.sum(values[chosen == value])), value)
                for value in sorted(set(int(v) for v in chosen.tolist()))
            ]
        )

    def _window(
        self, box: tuple[tuple[int, int], ...] | None, wrap: tuple[bool, bool, bool]
    ) -> tuple[tuple[slice, ...], tuple[bool, bool, bool], tuple[tuple[int, int], ...]] | None:
        """HOST: the box grown by one Link per axis, the rule's reach, as the slices to step, the faces the reads wrap on inside the window and the window itself as the record's next box; None when the window is the whole board; on a periodic axis a window that would touch the axis's ends is the whole axis with its wrap, elsewhere the reads beyond the window are zeros, the rows there (or the open face's nothing)."""
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
        """One interval of Rule3 on a record (ALGEBRA.md #the-line): every record, a body's own, a free one or a held part, steps by the rule alone; its count moves after, by the count's line (`_counts_stage`)."""
        if live.silent:
            return  # a zero held part steps to zero exactly
        field = live.held_part
        # The rule with the record's pair on the six-neighbour term (massive-record-v1, MASSIVE_RECORD.md section 1): G over the six neighbours, then D by 3 den with the remainder kept, then T; at light's pair [1, 1] the first build's integers bit for bit.
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
            # THE FOUR PACES AND THE TRANSPORT (ALGEBRA.md #the-interval; commits 3 and 4): the arrivals per axis after the transport, the rule per level on the whole board (HOST: no window shortcut here); the second level allocated by the first rotation that writes it
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
            # HOST (record 2039 (b); item 43): the rule on the support box grown by one, zeros elsewhere; the same integers at every Node
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
        if largest > self.world.amplitude_bound:
            raise RuntimeError(
                f"the record {live.identity} reached the level {largest} at interval {self.tick}, above "
                f"the world's declared amplitude bound A = {self.world.amplitude_bound} (issue #1085; "
                "MUST 3's bound holds only below A): the run is refused"
            )
        if im_next is not None:
            live.im_before = live.im_now
            live.im_now = im_next
        self._count_source(live, nxt)
        live.before = live.now
        live.now = nxt
        live.age += 1

    def _body_levels(self, block: Block, before: bool = False) -> np.ndarray:
        """The body's rotation's level now (or before) at each of its Nodes, in the mask's order: the standing record at its one Node (the body's Node, item 42) or its own rows there (the lattice body)."""
        if block.node_record is not None:
            level = block.node_record.before if before else block.node_record.now
            return np.full(int(np.count_nonzero(block.mask)), int(level), dtype=np.int64)
        assert block.own is not None
        return np.asarray((block.own.before if before else block.own.now)[block.mask], dtype=np.int64)

    def _recoil_at_taking(self, live: LiveRecord, detector: int, tally: tuple[int, int, int]) -> None:
        """The taker's recoil term at a report on a set with a body: the body's number, the sense +1, the tally per axis (the count's line's travel into the reporting Node this interval) and the record, for the (iv) act."""
        measured = self.detector_measured[detector]
        if measured is None or self.detector_face[detector]:
            return
        self._recoils.append((measured, TAKING, tally, live.identity))

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
