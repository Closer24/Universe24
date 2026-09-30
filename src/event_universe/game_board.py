"""The GameBoard: every family's NodeState over the Nodes (node.py), the bodies' ledgers and the detectors, stepped one interval at a time in the law's order (ALGEBRA.md #the-interval): the signed read and Rule3 on every record's two level pairs, the count's and the sense's lines, the givings at the Ports the line crossed, the reports, the hold, and the bodies' clocks as readings; `step_inverse` runs the same acts back. A body is a ledger and no state of the law: its family, its Nodes (where its family's count stands), its clock; a detector is a Node told to report; only a detector's report is a measurement, every other reading is a GameBoard diagnostic."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import replace

import numpy as np

from event_universe import flow, node
from event_universe.bodies import Body, converted, crossings, following
from event_universe.features.counts_line import CountWrites
from event_universe.features.start import rest
from event_universe.features.write import carried
from event_universe.loader.derived import BY_PLAIN, BY_SIGN
from event_universe.loader.world import FACE_NAME, Node, World
from event_universe.reports import Detector, book, clock_lines, gathers, giving_line

Observer = Callable[[dict[str, object]], None]


class GameBoard:
    """One world on the GameBoard, stepped interval by interval; `observer` receives the output lines `click`, `giving`, `gather` and `block`."""

    def __init__(self, world: World, observer: Observer | None = None) -> None:
        self.world, self.observer, self.tick = world, observer, 0
        self.shape, self.wrap = world.shape, world.periodic
        self.families = world.families
        self.states = [node.empty_state(family, self.shape) for family in self.families]
        self.order = [index for index, family in enumerate(self.families) if family.quanta]
        count = len(self.families)
        self.laid_total, self.laid_sense, self.given, self.taken, self.reports = (
            [0] * count,
            [0] * count,
            [0] * count,
            [0] * count,
            [0] * count,
        )
        self.bodies: list[Body] = []
        for number, row in enumerate(world.bodies):
            state = self.states[row.family]
            assert state.levels is not None and state.second is not None
            state.levels = self.added(state.levels, row.now, row.before)
            state.second = self.added(state.second, row.im_now, row.im_before)
            self.bodies.append(Body(number, row.family, self.mask(row.nodes), sum(row.counts), 0))
        for body in self.bodies:
            body.total = self.clock_total(body)
        self.start()
        self.detectors = [
            Detector(row.name, self.mask(row.positions) if row.body is None else None, row.body)
            for row in world.detectors
        ]
        face = np.zeros(self.shape, dtype=bool)
        for axis in range(3):
            if world.open_axes[axis]:
                layer = np.moveaxis(face, axis, 0)
                layer[: world.face_depth], layer[self.shape[axis] - world.face_depth :] = True, True
        if bool(face.any()):
            self.detectors.append(Detector(FACE_NAME, face, None))

    def added(self, record: node.Record, now: tuple[int, ...], before: tuple[int, ...]) -> node.Record:
        """A level pair with a body's two levels from the mode file added over the GameBoard."""
        return replace(
            record,
            now=record.now + self.board_array(now),
            before=record.before + self.board_array(before),
        )

    def board_array(self, values: tuple[int, ...]) -> np.ndarray:
        """One integer per Node in x-major order as an array over the GameBoard."""
        return np.array(values, dtype=np.int64).reshape(self.shape)

    def mask(self, nodes: tuple[Node, ...]) -> np.ndarray:
        """The mask of a set of Nodes."""
        found = np.zeros(self.shape, dtype=bool)
        found[tuple(np.array(nodes).T)] = True
        return found

    def start(self) -> None:
        """The start (ALGEBRA.md #the-generator (g), the start): every held family's time part without a gap at the rest of its line, and every one with a gap laid, under the bodies' sources, the form that sources the fields (the vacuum's share of a body's two level pairs, laid at the count's wall) at its Nodes at the weight with which the body's family sources the row, over its divisor (features/start), both levels, the remainder at the half wall and the hold's carry E_s div 2 at the sources' Nodes."""
        forms = []
        for body, row in zip(self.bodies, self.world.bodies, strict=True):
            family = self.families[row.family]
            records = [
                node.Record(self.board_array(now), self.board_array(before), node.zeros(self.shape))
                for now, before in ((row.now, row.before), (row.im_now, row.im_before))
            ]
            total = sum(
                node.share(family.pair, record, self.wrap, self.world.node_clock) for record in records
            )
            laid = node.laid(np.asarray(total), node.count_wall(family, self.world.quantum_action))[0]
            forms.append(np.where(body.nodes, laid, 0))
        for index, family in enumerate(self.families):
            if family.held is None or family.divisor is None:
                continue
            counts = node.zeros(self.shape)
            for row, form in zip(self.world.bodies, forms, strict=True):
                counts = counts + node.weight_of(index, self.families[row.family]) * form
            if not counts.any():
                continue
            state = self.states[index]
            if (
                family.gap
            ):  # a held row with a gap is laid, the sources through its divisor, never stepped
                origin = np.where(counts != 0, carried(family.divisor, 2, 0)[0], 0)
                laid, state.carry = (np.asarray(a) for a in carried(counts, family.divisor, origin))
                state.parts[0] = node.Record(laid, laid.copy(), node.zeros(self.shape))
                continue
            try:
                field = rest(counts, family.pair, self.wrap, family.divisor, self.world.width)
            except ValueError as refusal:
                raise ValueError(f"the start of the held family {family.name!r}: {refusal}") from refusal
            remainder = np.full(self.shape, field.remainder, dtype=np.int64)
            state.parts[0] = node.Record(field.levels.copy(), field.levels.copy(), remainder)
            state.carry = field.carries

    def clock_total(self, body: Body) -> int:
        """The body's clock: its family's level now summed over its Nodes."""
        levels = self.states[body.family].levels
        assert levels is not None
        return int(levels.now[body.nodes].sum(dtype=object))

    def emit(self, line: dict[str, object]) -> None:
        """One output line to the observer, if any."""
        if self.observer is not None:
            self.observer(line)

    def contents(self) -> list[dict[str, int]]:
        """Every body's quanta per family of quanta: that family's count summed over the body's Nodes (a GameBoard reading)."""
        return [
            {
                family.name: int(state.count[body.nodes].sum())
                for family, state in zip(self.families, self.states, strict=True)
                if state.count is not None
            }
            for body in self.bodies
        ]

    def books(self) -> dict[str, dict[str, int | bool]]:
        """The books per family of quanta, a GameBoard diagnostic (`reports.book`)."""
        found: dict[str, dict[str, int | bool]] = {}
        for index, (family, state) in enumerate(zip(self.families, self.states, strict=True)):
            if state.count is not None:
                wall = node.count_wall(family, self.world.quantum_action)
                laid = (self.laid_total[index], self.laid_sense[index])
                moved = (self.given[index], self.taken[index], self.reports[index])
                found[family.name] = book(state, wall, laid, moved)
        return found

    def stepped(
        self, index: int, level: str, direction: int
    ) -> tuple[tuple[np.ndarray, tuple[np.ndarray, ...]], node.Record, node.Record]:
        """A family of quanta's read (from the held parts' `level`) and its two level pairs stepped by Rule3 in `direction` with the rule of that read."""
        family, state = self.families[index], self.states[index]
        assert state.levels is not None and state.second is not None
        read = node.signed_read(
            index, self.families, self.states, self.world.node_clock, level, self.tick, self.shape
        )
        rule = node.quanta_rule(family, self.world.node_clock, *read)
        return (
            read,
            node.step(state.levels, rule, self.wrap, direction),
            node.step(state.second, rule, self.wrap, direction),
        )

    def step(self) -> None:
        """One interval forward, each act one loop over the families or the bodies and detectors (ALGEBRA.md #the-interval): the signed read and Rule3 on both level pairs with the wells and the Wronskian's quanta; the count's and the sense's lines (laid at the first act); the givings at the Ports the line crossed out of every body; the bodies' Nodes and the reports; the held families' parts and holds; the clocks as readings."""
        self.tick += 1
        action = self.world.quantum_action
        wells: dict[int, np.ndarray] = {}
        turns: dict[int, np.ndarray] = {}
        reads = {}
        for index in self.order:
            state = self.states[index]
            assert state.levels is not None and state.second is not None
            assert state.well_remainder is not None and state.wronskian_remainder is not None
            reads[index], after, second = self.stepped(index, "now", 1)
            self.bounded(self.families[index].name, after)
            self.bounded(self.families[index].name, second)
            booking = node.form(state.levels, after) + node.form(state.second, second)
            wells[index], state.well_remainder = node.well(booking, state.well_remainder, action)
            turns[index], state.wronskian_remainder = node.well(
                node.wronskian(after, second), state.wronskian_remainder, action
            )
            state.levels, state.second = after, second
        if all(self.states[index].count is None for index in self.order):
            self.lay(reads)
        writes, starts, rises = {}, {}, {}
        for index in self.order:
            state = self.states[index]
            assert state.count is not None and state.count_remainder is not None
            starts[index] = (state.count.copy(), state.count_remainder.copy())
            writes[index] = self.lines(index, 1)
        for body in self.bodies:
            self.give(body, writes[body.family], starts[body.family][1], reads)
        for index in self.order:
            rises[index] = np.asarray(self.states[index].count) - starts[index][0]
        for body in self.bodies:
            count = self.states[body.family].count
            assert count is not None
            body.nodes = following(body.nodes, count, self.wrap)
        self.report(rises)
        counted = {index: np.asarray(self.states[index].count) for index in self.order}
        self.hold(wells, turns, 1, writes, counted)
        for body in self.bodies:
            self.clock(body)

    def lines(self, index: int, direction: int) -> tuple[CountWrites, CountWrites]:
        """The count's line and the sense's line of a family of quanta in `direction`, their writes set in its NodeState; the writes returned for the givings and the flows."""
        family, state = self.families[index], self.states[index]
        action, bound = self.world.quantum_action, self.world.amplitude_bound
        count = node.count_line(family, state, action, bound, self.wrap, direction)
        sense = node.sense_line(family, state, action, bound, self.wrap, direction)
        state.count, state.count_remainder = np.asarray(count.count), np.asarray(count.remainder)
        state.sense, state.sense_remainder = np.asarray(sense.count), np.asarray(sense.remainder)
        return count, sense

    def flows(
        self,
        held: int,
        writes: dict[int, tuple[CountWrites, CountWrites]],
        counts: dict[int, np.ndarray],
    ) -> dict[int, flow.Flow]:
        """Every family of quanta's flow into a held family this interval: the travel of its count's line where it sources the row by plain, of its sense's line where by sign, its count after the line and its wall."""
        found = {}
        for index, (count, sense) in writes.items():
            family = self.families[index]
            for by, written in ((BY_PLAIN, count), (BY_SIGN, sense)):
                weight = node.weight_of(held, family, by)
                if weight:
                    wall = node.count_wall(family, self.world.quantum_action)
                    travel = tuple(np.asarray(value) for value in written.travel)
                    found[index] = flow.Flow(
                        weight, (travel[0], travel[1], travel[2]), counts[index], wall
                    )
        return found

    def hold(
        self,
        wells: dict[int, np.ndarray],
        turns: dict[int, np.ndarray],
        direction: int,
        writes: dict[int, tuple[CountWrites, CountWrites]],
        counts: dict[int, np.ndarray],
    ) -> None:
        """The hold of every held family, forward or back (ALGEBRA.md #the-primitives, the row "the hold"): the time part from the wells and the Wronskian's quanta, the vector and tensor parts from the lines' flows."""
        for index, family in enumerate(self.families):
            if family.held is None:
                continue
            state = self.states[index]
            source = node.source(index, self.families, wells, turns, self.shape)
            flows = self.flows(index, writes, counts)
            state.parts, state.carry, state.flows = node.held_step(
                family, state, source, self.wrap, direction, flows
            )
            for part in state.parts:
                self.bounded(family.name, part)

    def bounded(self, name: str, record: node.Record) -> None:
        """The amplitude bound A of the world: a level beyond it refuses the run by name."""
        if node.largest(record) > self.world.amplitude_bound:
            raise RuntimeError(
                f"the family {name!r} reached the level {node.largest(record)} at interval {self.tick}, above "
                f"the world's amplitude bound A = {self.world.amplitude_bound}: the run is refused"
            )

    def lay(self, reads: dict[int, tuple[np.ndarray, tuple[np.ndarray, ...]]]) -> None:
        """The lay at the first act (ALGEBRA.md #the-counts-line): every family's count from the weighted share of its two level pairs and its sense from their Wronskian, at the paces of this interval's read, the quanta the bodies hold of other families added at their Nodes, the gate (a body's declared count within 2 isqrt(c) + 1 of the count laid at its Nodes, refused by name beyond it) and the carries of the holds' vector and tensor parts at their origin."""
        action, gamma = self.world.quantum_action, self.world.node_clock
        for index in self.order:
            family, state = self.families[index], self.states[index]
            assert state.levels is not None and state.second is not None
            content, axis = reads[index]
            state.count, state.count_remainder = node.lay(
                family, (state.levels, state.second), action, self.wrap, gamma, content, axis
            )
            state.sense, state.sense_remainder = node.lay_sense(
                family, state.levels, state.second, action, gamma, content, axis
            )
        for body, row in zip(self.bodies, self.world.bodies, strict=True):
            for other, counts in row.holds:
                others = self.states[other].count
                assert others is not None
                for at, value in zip(row.nodes, counts, strict=True):
                    others[at] += value
            laid = self.states[body.family].count
            assert laid is not None
            found, off = int(laid[body.nodes].sum()), abs(body.declared - int(laid[body.nodes].sum()))
            half = int(carried(off - 1, 2, 0)[0])  # (|c - laid| - 1) div 2, the division act
            if off > 1 and half * half > body.declared:
                raise ValueError(
                    f"the body {body.number} declares the count {body.declared} and its family's form lays "
                    f"{found} quanta at its Nodes at T = {self.world.quantum_action}: a declared count is within "
                    "2 isqrt(c) + 1 of SUM D_i div T (ALGEBRA.md #the-counts-line, the lay and the wall)"
                )
        for index in self.order:
            family, state = self.families[index], self.states[index]
            assert state.count is not None and state.count_remainder is not None
            assert state.sense is not None and state.sense_remainder is not None
            wall = node.count_wall(family, action)
            self.laid_total[index] = int(
                (wall * state.count.astype(object) + state.count_remainder).sum()
            )
            self.laid_sense[index] = int(
                (wall * state.sense.astype(object) + state.sense_remainder).sum()
            )
        for held, family in enumerate(self.families):
            if family.held is None or len(family.parts) == 1:
                continue
            for index in self.order:
                for by in (BY_PLAIN, BY_SIGN):
                    weight = node.weight_of(held, self.families[index], by)
                    count = self.states[index].count
                    if weight and count is not None:
                        wall = node.count_wall(self.families[index], action)
                        self.states[held].flows[index] = flow.flow_origins(family, wall, count)

    def report(self, rises: dict[int, np.ndarray]) -> None:
        """The reports of every detector per family (a detector's Nodes, the Nodes of the body it names, the open faces' layer), the net inflow of the family's count across its boundary this interval (`reports.gathers`)."""
        for index, rise in rises.items():
            count = self.states[index].count
            assert count is not None
            for detector in self.detectors:
                nodes = self.bodies[detector.body].nodes if detector.body is not None else detector.nodes
                assert nodes is not None
                for line in gathers(detector, nodes, rise, count, self.families[index].name, self.tick):
                    self.reports[index] += 1
                    self.emit(line)

    def clock(self, body: Body) -> None:
        """The body's clock, a GameBoard reading that fires nothing (`reports.clock_lines`)."""
        total = self.clock_total(body)
        name = self.families[body.family].name
        for line in clock_lines(body.number, name, body.corner(), body.total, total, self.tick):
            self.emit(line)
        body.total = total

    def give(
        self,
        body: Body,
        written: tuple[CountWrites, CountWrites],
        remainder: np.ndarray,
        reads: dict[int, tuple[np.ndarray, tuple[np.ndarray, ...]]],
    ) -> None:
        """The giving is the line's click at the shell (ALGEBRA.md #the-primitives, the row "the giving"): every quantum the count's line carries out through an outer Port of the body's Nodes (`bodies.crossings`) converted at the Node it enters into the family its family gives (`bodies.converted`), one `giving` line per quantum."""
        family = self.families[body.family]
        if family.gives is None:
            return
        given, action = family.gives, self.world.quantum_action
        own, other = self.states[body.family], self.states[given]
        assert own.count is not None
        wall = node.count_wall(family, action)
        paces = (self.world.node_clock, *reads[given])
        label = f"the giving of measured[{body.number}] at interval {self.tick}"
        for at, there, axis, side, quanta in crossings(
            body.nodes, written[0].through, remainder, wall, self.wrap
        ):
            for _ in range(quanta):
                bound = self.world.amplitude_bound
                converted(
                    own, other, self.families[given], there, action, self.wrap, bound, label, paces
                )
                self.given[body.family] += 1
                self.taken[given] += 1
                name, after = self.families[given].name, int(own.count[body.nodes].sum())
                self.emit(giving_line(body.number, name, at, axis, side, after, self.tick))

    def step_inverse(self) -> None:
        """One interval back, the same acts in reverse order with Rule3's direction -1 (ALGEBRA.md #the-direction, #the-counts-line): the count's and the sense's lines back (from the levels as the step left them, so the reads find the interval's start), the reads and both level pairs back with the wells and the Wronskian's quanta, the held families' holds and parts back; the givings, the bodies' Nodes and the lay are not taken back."""
        action = self.world.quantum_action
        after = {index: np.asarray(self.states[index].count) for index in self.order}
        writes = {index: self.lines(index, -1) for index in self.order}
        wells: dict[int, np.ndarray] = {}
        turns: dict[int, np.ndarray] = {}
        backs = {}
        for index in self.order:
            state = self.states[index]
            assert state.levels is not None and state.second is not None
            assert state.well_remainder is not None and state.wronskian_remainder is not None
            _read, back, second = self.stepped(index, "before", -1)
            booking = node.form(back, state.levels) + node.form(second, state.second)
            wells[index], start = node.well(booking, state.well_remainder, action, -1)
            turns[index], turned = node.well(
                node.wronskian(state.levels, state.second), state.wronskian_remainder, action, -1
            )
            backs[index] = (back, second, start, turned)
        self.hold(wells, turns, -1, writes, after)
        for index, (back, second, start, turned) in backs.items():
            state = self.states[index]
            state.levels, state.second, state.well_remainder, state.wronskian_remainder = (
                back,
                second,
                start,
                turned,
            )
        for body in self.bodies:
            body.total = self.clock_total(body)
        self.tick -= 1
