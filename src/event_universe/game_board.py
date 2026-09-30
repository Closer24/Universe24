"""The GameBoard: every family's NodeState over the Nodes (node.py) and the detectors, stepped one interval at a time in the law's order (ALGEBRA.md #the-interval): the signed read and Rule3 on every record, the count's and the sense's lines, the clicks, the hold; `step_inverse` runs the same acts back. The board's face rule (core/ports.py) is the file's: the wraps, the Nodes its inner faces declare beyond the board and its receding faces, beyond which it grows by layers of zeros as the front reaches them (growth.py), every declared coordinate staying the file's. No ledger of bodies is kept: a body's Nodes are where its family's count stands about its declared Nodes, derived when a report needs them (reports.standing); a message is a laid record and no body; a detector is a region of Nodes declared in the file, a declared instrument, its click a whole quantum's entry through its boundary reported with the region and never a Node, the one measurement, what it saw at its boundary a `seen` line for the host's credit, every other reading a GameBoard diagnostic; the guard reads the initial state once at load and no act of the interval."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import replace

import numpy as np

from event_universe import flow, growth, lay, node
from event_universe.core.ports import Wrap
from event_universe.features.counts_line import CountWrites
from event_universe.features.start import rest
from event_universe.features.write import carried
from event_universe.loader.derived import BY_PLAIN, BY_SIGN, count_wall
from event_universe.loader.keys import Node
from event_universe.loader.messages import MessageRow
from event_universe.loader.mode import Levels
from event_universe.loader.world import FACE_NAME, BodyRow, World
from event_universe.reports import Detector, book, clicks, standing

Observer = Callable[[dict[str, object]], None]
Lines = dict[int, tuple[CountWrites, CountWrites]]
Books = dict[int, tuple[list[node.Record], np.ndarray | None, np.ndarray | None]]


class GameBoard:
    """One world on the GameBoard, stepped interval by interval; `observer` receives the output lines `click`."""

    def __init__(self, world: World, observer: Observer | None = None) -> None:
        self.world, self.observer, self.tick = world, observer, 0
        self.shape, self.offset = world.shape, (0, 0, 0)
        self.growths: list[growth.Growth] = []
        self.ended: dict[str, object] | None = None
        beyond = self.mask(world.beyond) if world.beyond else None
        self.wrap = Wrap(world.periodic[0], world.periodic[1], world.periodic[2], beyond)
        self.families = world.families
        self.states = [node.empty_state(family, self.shape) for family in self.families]
        self.order = [index for index, family in enumerate(self.families) if family.quanta]
        self.held = [index for index, family in enumerate(self.families) if family.held is not None]
        count = len(self.families)
        self.laid_total, self.laid_sense, self.reports = [0] * count, [0] * count, [0] * count
        self.origins = [0] * count  # the remainder the start gave each held row, 0 where it gave none
        for row in self.laid_rows():
            state = self.states[row.family]
            if state.levels is None:
                continue  # a kick on a holder of the content is laid after the start, on the row's rest
            assert state.second is not None
            real = self.added(state.levels, row.now, row.before)
            second = self.added(state.second, row.im_now, row.im_before)
            node.with_records(state, [real, second, *node.records(state)[2:]])
        self.start()
        for row in self.laid_rows():
            state = self.states[row.family]
            if state.levels is None:  # the kick: the row's own travelling events on its rest, no count
                node.with_parts(
                    state, [self.added(state.parts[0], row.now, row.before), *state.parts[1:]]
                )
        self.fields: dict[tuple[int, str], int] = {}  # the last field reading per holder and region
        for index in self.order:
            node.guarded(index, self.families, self.states, self.world.node_clock, self.shape)
        self.detectors = [
            Detector(row.name, self.mask(row.positions) if row.body is None else None, row.body)
            for row in world.detectors
        ]
        face = np.zeros(self.shape, dtype=bool)
        receding = [(row.axis, row.side) for row in world.receding]
        for axis in range(3):
            if world.open_axes[axis]:
                layer = np.moveaxis(face, axis, 0)
                layer[: world.face_depth] = (axis, -1) not in receding
                layer[self.shape[axis] - world.face_depth :] = (axis, 1) not in receding
        if bool(face.any()):
            self.detectors.append(Detector(FACE_NAME, face, None))

    def laid_rows(self) -> list[BodyRow | MessageRow]:
        """The records the file lays: the bodies and the messages, in the file's order."""
        return [*self.world.bodies, *self.world.messages]

    def added(self, record: node.Record, now: Levels, before: Levels) -> node.Record:
        """A level pair with a body's or a message's two levels from the mode file added over the GameBoard."""
        return replace(
            record,
            now=record.now + self.board_array(now),
            before=record.before + self.board_array(before),
        )

    def board_array(self, values: Levels) -> np.ndarray:
        """The levels the mode file lays as an array over the GameBoard: the nonzero Nodes' flat x-major indexes with their levels, 0 elsewhere."""
        found = node.zeros(self.shape).reshape(-1)
        for at, value in values:
            found[at] += value
        return found.reshape(self.shape)

    def mask(self, nodes: tuple[Node, ...]) -> np.ndarray:
        """The mask of a set of Nodes declared at the file's coordinates, on the GameBoard as grown."""
        found = np.zeros(self.shape, dtype=bool)
        found[tuple((np.array(nodes) + np.array(self.offset)).T)] = True
        return found

    def start(self) -> None:
        """The start (ALGEBRA.md #the-generator (g), the start): every held family's time part at the rest of its line, with or without a gap, under the sources of the bodies at their Nodes and of the messages over the whole GameBoard, the massless row's rest with its vacuum content added at every Node (the row's `rest`, the same rest read beyond every face; ALGEBRA.md #what-is-open, item 22), the form that sources the fields (the vacuum's share of the two level pairs, laid at the count's wall) at the weight with which the record's family sources the row by plain and the Wronskian's quanta at the written moment, W div T, at the weight by sign (the holder of the sign's rest, of either sign), over its divisor (features/start), both levels, the remainder at the half wall of the rule the row steps by and the hold's carry E_s div 2 at the sources' Nodes."""
        forms = []
        for row in self.laid_rows():
            family = self.families[row.family]
            if not family.quanta:
                continue  # a kick on a holder of the content sources nothing: it is the row's own events
            records = [
                node.Record(self.board_array(now), self.board_array(before), node.zeros(self.shape))
                for now, before in ((row.now, row.before), (row.im_now, row.im_before))
            ]
            total = sum(
                lay.share(family.pair, record, self.wrap, self.world.node_clock) for record in records
            )
            laid = lay.laid(np.asarray(total), count_wall(family, self.world.quantum_action))[0]
            turn = node.well(
                node.wronskian(*records), node.zeros(self.shape), self.world.quantum_action
            )[0]
            everywhere = np.ones(self.shape, dtype=bool)
            on = self.mask(row.nodes) if isinstance(row, BodyRow) else everywhere
            forms.append((row.family, np.where(on, laid, 0), np.where(on, turn, 0)))
        for index in self.held:
            family = self.families[index]
            assert family.divisor is not None
            counts = node.zeros(self.shape)
            for source, form, turn in forms:
                counts = counts + node.weight_of(index, self.families[source]) * form
                counts = counts + node.weight_of(index, self.families[source], BY_SIGN) * turn
            if not counts.any() and not family.rest:
                continue  # a row with a rest and no source rests by the line too, its remainder at the half wall
            state = self.states[index]
            wall = node.rule_of(family, self.world.node_clock, 0)[2]
            try:
                field = rest(counts, family.pair, self.wrap, family.divisor, self.world.width, wall)
            except ValueError as refusal:
                raise ValueError(f"the start of the held family {family.name!r}: {refusal}") from refusal
            remainder = np.full(self.shape, field.remainder, dtype=np.int64)
            time = node.Record(field.levels.copy(), field.levels.copy(), remainder)
            node.with_parts(state, [time, *state.parts[1:]])
            state.carry, self.origins[index] = field.carries, field.remainder
        for index in self.held:
            family, state = self.families[index], self.states[index]
            if family.rest:
                time = state.parts[0]
                time = replace(time, now=time.now + family.rest, before=time.before + family.rest)
                node.with_parts(state, [time, *state.parts[1:]])

    def emit(self, line: dict[str, object]) -> None:
        """One output line to the observer, if any."""
        if self.observer is not None:
            self.observer(line)

    def instrument(self) -> np.ndarray:
        """The instrument: the union of the declared regions (every detector with its own positions, the faces' layer and the bodies' detectors aside), whose boundary is where the clicks and the seen inflows are read (ALGEBRA.md #the-click-ends-nothing): what moves between two regions of one screen is neither an entry nor seen twice."""
        found = np.zeros(self.shape, dtype=bool)
        for detector in self.detectors:
            if detector.body is None and detector.name != FACE_NAME and detector.nodes is not None:
                found |= detector.nodes
        return found

    def body_nodes(self, number: int) -> np.ndarray:
        """A body's Nodes as a report needs them: where its family's count stands about its declared Nodes, derived now and kept nowhere (`reports.standing`)."""
        row = self.world.bodies[number]
        count = self.states[row.family].count
        declared = self.mask(row.nodes)
        return standing(declared, count, self.wrap) if count is not None else declared

    def contents(self) -> list[dict[str, int]]:
        """Every body's quanta per family of quanta: that family's count summed over the body's Nodes (a GameBoard reading)."""
        return [
            {
                family.name: int(state.count[self.body_nodes(number)].sum())
                for family, state in zip(self.families, self.states, strict=True)
                if state.count is not None
            }
            for number in range(len(self.world.bodies))
        ]

    def books(self) -> dict[str, dict[str, int | bool]]:
        """The books per family of quanta, a GameBoard diagnostic (`reports.book`), the least Link pace of the final state among them."""
        found: dict[str, dict[str, int | bool]] = {}
        for index in self.order:
            family, state = self.families[index], self.states[index]
            wall = count_wall(family, self.world.quantum_action)
            laid = (self.laid_total[index], self.laid_sense[index])
            pace = node.least_pace(index, self.families, self.states, self.world.node_clock, self.shape)
            found[family.name] = book(state, wall, laid, self.reports[index], pace)
        return found

    def stepped(
        self, index: int, level: str, direction: int
    ) -> tuple[tuple[np.ndarray, tuple[np.ndarray, ...]], list[node.Record]]:
        """A family's read (from the held parts' `level`) and every record of it stepped by Rule3 in `direction` with the rule of that read: a family of quanta's two level pairs and a held family's parts (`node.records`), every held row of the content among them, with or without a gap, the time part of the massless row reading its rest beyond every face (`node.step`, `fill`)."""
        family, state = self.families[index], self.states[index]
        read = node.signed_read(
            index, self.families, self.states, self.world.node_clock, level, self.shape
        )
        rule = node.rule_of(family, self.world.node_clock, *read)
        time = state.parts[0] if state.parts else None
        found = [
            node.step(record, rule, self.wrap, direction, family.rest if record is time else 0)
            for record in node.records(state)
        ]
        return read, found

    def step(self) -> None:
        """One interval forward, each act one loop over the families or the detectors (ALGEBRA.md #the-interval): the receding faces grown where the front reaches them (`growth.grow`; at the largest size the run ends, named in `ended`, and no act is taken); the signed read and Rule3 on every record with the wells and the Wronskian's quanta; the count's and the sense's lines (laid at the first act); the clicks; the holds."""
        if self.ended is not None:
            raise RuntimeError(f"the run ended at interval {self.tick}: {self.ended}")
        if not growth.grow(self):
            return
        self.tick += 1
        action = self.world.quantum_action
        wells: dict[int, np.ndarray] = {}
        turns: dict[int, np.ndarray] = {}
        reads = {}
        found = {index: self.stepped(index, "now", 1) for index in range(len(self.families))}
        for index, (read, records) in found.items():
            state = self.states[index]
            reads[index] = read
            for record in records:
                self.bounded(self.families[index].name, record)
            if state.levels is not None and state.second is not None:
                assert state.well_remainder is not None and state.wronskian_remainder is not None
                booking = node.form(state.levels, records[0]) + node.form(state.second, records[1])
                wells[index], state.well_remainder = node.well(booking, state.well_remainder, action)
                turns[index], state.wronskian_remainder = node.well(
                    node.wronskian(records[0], records[1]), state.wronskian_remainder, action
                )
            node.with_records(state, records)
        if all(self.states[index].count is None for index in self.order):
            self.lay(reads)
        writes, remainders = {}, {}
        for index in self.order:
            state = self.states[index]
            assert state.count_remainder is not None
            remainders[index] = state.count_remainder.copy()
            writes[index] = self.lines(index, 1)
        self.report(writes, remainders)
        for index in self.held:
            self.hold(index, wells, turns, 1, writes)

    def lines(self, index: int, direction: int) -> tuple[CountWrites, CountWrites]:
        """The count's line and the sense's line of a family of quanta in `direction`, their writes set in its NodeState; the writes returned for the flows."""
        family, state = self.families[index], self.states[index]
        action, bound = self.world.quantum_action, self.world.amplitude_bound
        count = node.count_line(family, state, action, bound, self.wrap, direction)
        sense = node.sense_line(family, state, action, bound, self.wrap, direction)
        state.count, state.count_remainder = np.asarray(count.count), np.asarray(count.remainder)
        state.sense, state.sense_remainder = np.asarray(sense.count), np.asarray(sense.remainder)
        return count, sense

    def sources_of(self, held: int) -> list[int]:
        """The families of quanta that source a held family, by plain or by sign."""
        return [
            index
            for index in self.order
            if node.weight_of(held, self.families[index], BY_PLAIN)
            or node.weight_of(held, self.families[index], BY_SIGN)
        ]

    def flows(self, held: int, writes: Lines) -> dict[int, flow.Flow]:
        """Every family of quanta's flow into a held family this interval: the stress of its count's line where it sources the row by plain, of its sense's line where by sign, and its wall."""
        found = {}
        for index, (count, sense) in writes.items():
            family = self.families[index]
            for by, written in ((BY_PLAIN, count), (BY_SIGN, sense)):
                weight = node.weight_of(held, family, by)
                if weight:
                    wall = count_wall(family, self.world.quantum_action)
                    stress = tuple(np.asarray(value) for value in written.stress)
                    found[index] = flow.Flow(weight, (stress[0], stress[1], stress[2]), wall)
        return found

    def hold(
        self,
        index: int,
        wells: dict[int, np.ndarray],
        turns: dict[int, np.ndarray],
        direction: int,
        writes: Lines,
    ) -> None:
        """The hold of one held family, forward or back (ALGEBRA.md #the-primitives, the row "the hold"): the time part from the wells and the Wronskian's quanta, the tensions from the lines' stresses."""
        family, state = self.families[index], self.states[index]
        source = node.source(index, self.families, wells, turns, self.shape)
        parts, state.carry, state.flows = node.held_step(
            family, state, source, direction, self.flows(index, writes)
        )
        node.with_parts(state, parts)
        for part in parts:
            self.bounded(family.name, part)

    def bounded(self, name: str, record: node.Record) -> None:
        """The amplitude bound A of the world: a level beyond it refuses the run by name."""
        if node.largest(record) > self.world.amplitude_bound:
            raise RuntimeError(
                f"the family {name!r} reached the level {node.largest(record)} at interval {self.tick}, above "
                f"the world's amplitude bound A = {self.world.amplitude_bound}: the run is refused"
            )

    def lay(self, reads: dict[int, tuple[np.ndarray, tuple[np.ndarray, ...]]]) -> None:
        """The lay at the first act (ALGEBRA.md #the-counts-line): every family's count from the weighted share of its two level pairs and its sense from their Wronskian, at the paces of this interval's read, the quanta the bodies hold of other families added at their declared Nodes, the gate (a body's declared count within the rounding of the count laid at its Nodes, ((|c - laid| - 1) div 2)^2 <= c, refused by name beyond it) and the carries of the holds' tensions at their origin."""
        action, gamma = self.world.quantum_action, self.world.node_clock
        for index in self.order:
            family, state = self.families[index], self.states[index]
            assert state.levels is not None and state.second is not None
            content, axis = reads[index]
            state.count, state.count_remainder = lay.lay(
                family, (state.levels, state.second), action, self.wrap, gamma, content, axis
            )
            state.sense, state.sense_remainder = lay.lay_sense(
                family, state.levels, state.second, action, gamma, content, axis
            )
        for number, row in enumerate(self.world.bodies):
            for other, counts in row.holds:
                others = self.states[other].count
                assert others is not None
                for at, value in zip(row.nodes, counts, strict=True):
                    others[at] += value
            laid = self.states[row.family].count
            assert laid is not None
            declared, found = sum(row.counts), int(laid[self.mask(row.nodes)].sum())
            off = abs(declared - found)
            half = int(carried(off - 1, 2, 0)[0])  # (|c - laid| - 1) div 2, the division act
            if off > 1 and half * half > declared:
                raise ValueError(
                    f"the body {number} declares the count {declared} and its family's form lays "
                    f"{found} quanta at its Nodes at T = {self.world.quantum_action}: a declared count is within "
                    "the rounding of SUM D_i div T, ((|c - laid| - 1) div 2)^2 <= c (ALGEBRA.md #the-counts-line, "
                    "the lay and the wall)"
                )
        for detector in self.world.detectors:
            for index, values in detector.remainders:
                remainder = self.states[index].count_remainder
                assert remainder is not None
                for at, value in zip(detector.positions, values, strict=True):
                    remainder[at] = value
        for index in self.order:
            family, state = self.families[index], self.states[index]
            assert state.count is not None and state.count_remainder is not None
            assert state.sense is not None and state.sense_remainder is not None
            wall = count_wall(family, action)
            self.laid_total[index] = int(
                (wall * state.count.astype(object) + state.count_remainder).sum()
            )
            self.laid_sense[index] = int(
                (wall * state.sense.astype(object) + state.sense_remainder).sum()
            )
        for held in self.held:
            if len(self.families[held].parts) == 1:
                continue
            for index in self.sources_of(held):
                wall = count_wall(self.families[index], action)
                self.states[held].flows[index] = flow.flow_origins(self.families[held], wall, self.shape)

    def declared_board(self) -> np.ndarray:
        """The declared board: the file's own Nodes over the GameBoard as grown, the layers a receding face has grown beyond them (what leaves into those layers has left the world, `growth`)."""
        found = np.zeros(self.shape, dtype=bool)
        first, extent = self.offset, self.world.shape
        found[
            first[0] : first[0] + extent[0],
            first[1] : first[1] + extent[1],
            first[2] : first[2] + extent[2],
        ] = True
        return found

    def report(self, writes: Lines, remainders: dict[int, np.ndarray]) -> None:
        """The clicks of every detector per family of quanta (a detector's declared Nodes, the Nodes of the body it names derived now, the open faces' layer), each one region: the whole quanta the count's line's currents carried into it through its boundary Ports this interval, from the remainders before the line, reported with the region's name and never a Node (`reports.clicks`); and what each detector saw this interval, one `seen` line per family and detector where it is not 0: the net current through the instrument's front boundary at its Nodes, in integers (the front: the Ports leading in from the declared board outside the instrument, `declared_board`; not the Ports between two regions and not those toward a receding face's grown layers), the density that entered from the declared board, the host's reading for the credit by the shares and no click."""
        own = self.declared_board()
        for index, (count_line, _sense) in writes.items():
            family, count = self.families[index], self.states[index].count
            assert count is not None
            wall = count_wall(family, self.world.quantum_action)
            for detector in self.detectors:
                nodes = self.body_nodes(detector.body) if detector.body is not None else detector.nodes
                assert nodes is not None
                declared = detector.body is None and detector.name != FACE_NAME
                boundary_of = self.instrument() if declared else nodes
                through, before = count_line.through, remainders[index]
                lines, inflow = clicks(
                    detector,
                    nodes,
                    through,
                    before,
                    count,
                    wall,
                    self.wrap,
                    family.name,
                    self.tick,
                    boundary_of,
                    own,
                )
                for line in lines:
                    self.reports[index] += 1
                    self.emit(line)
                if inflow != 0:
                    self.emit(
                        {
                            "event": "seen",
                            "tick": self.tick,
                            "family": family.name,
                            "detector": detector.name,
                            "inflow": inflow,
                        }
                    )
        self.fields_read()

    def fields_read(self) -> None:
        """A GameBoard reading, no measurement, labelled so: per family and declared region, the family's density over the region this interval, one `field` line where it differs from the last interval's: for a family of quanta its count summed over the region (what its clicks count, the packet's passage), for a holder of the content the square of its time part's deviation from the row's rest summed over the region (a row with no count's line, its travelling events' passage; the advisor's reading of a kick's arrival, #1563 comment 5916154126)."""
        for index, (family, state) in enumerate(zip(self.families, self.states, strict=True)):
            if family.quanta:
                assert state.count is not None
                density = state.count
            else:
                deviation = state.parts[0].now - family.rest
                density = deviation * deviation
            for detector in self.detectors:
                if detector.body is not None or detector.name == FACE_NAME or detector.nodes is None:
                    continue
                total = int(density[detector.nodes].sum(dtype=object))
                if self.fields.get((index, detector.name)) == total:
                    continue
                self.fields[(index, detector.name)] = total
                self.emit(
                    {
                        "event": "field",
                        "tick": self.tick,
                        "family": family.name,
                        "detector": detector.name,
                        "reading": total,
                    }
                )

    def booked_back(
        self,
        index: int,
        books: Books,
        wells: dict[int, np.ndarray],
        turns: dict[int, np.ndarray],
        writes: Lines,
    ) -> None:
        """A family of quanta's books one interval back, its record free of any write: the count's and the sense's lines back (their currents read from the levels as the step left them), every record back and the wells and the Wronskian's quanta back, the records kept aside until every read of the interval's start is done."""
        state = self.states[index]
        assert state.levels is not None and state.second is not None
        assert state.well_remainder is not None and state.wronskian_remainder is not None
        writes[index] = self.lines(index, -1)
        _read, records = self.stepped(index, "before", -1)
        booking = node.form(records[0], state.levels) + node.form(records[1], state.second)
        wells[index], start = node.well(booking, state.well_remainder, self.world.quantum_action, -1)
        turns[index], turned = node.well(
            node.wronskian(state.levels, state.second),
            state.wronskian_remainder,
            self.world.quantum_action,
            -1,
        )
        books[index] = (records, start, turned)

    def step_inverse(self) -> None:
        """One interval back, the same acts in reverse order with Rule3's direction -1 (ALGEBRA.md #the-direction, #the-counts-line): a held family's hold back once every family that sources it is booked back, a family of quanta booked back once its own hold is off (the holder of the sign before the rows it sources), then every held row of the content stepped back; the lay is not taken back."""
        wells: dict[int, np.ndarray] = {}
        turns: dict[int, np.ndarray] = {}
        writes: Lines = {}
        books: Books = {}
        pending = list(self.held)
        while True:
            for index in self.order:
                if index not in books and (index not in self.held or index not in pending):
                    self.booked_back(index, books, wells, turns, writes)
            ready = [held for held in pending if all(index in books for index in self.sources_of(held))]
            if not pending:
                break
            assert ready, "the held rows' sources form a cycle"
            for held in ready:
                self.hold(held, wells, turns, -1, writes)
            pending = [held for held in pending if held not in ready]
        for index in self.held:
            if index not in books:
                books[index] = (self.stepped(index, "before", -1)[1], None, None)
        for index, (records, start, turned) in books.items():
            state = self.states[index]
            node.with_records(state, records)
            if start is not None:
                state.well_remainder, state.wronskian_remainder = start, turned
        self.tick, self.ended = self.tick - 1, None
        while self.growths and self.growths[-1][0] == self.tick + 1:
            growth.resize(self, *self.growths.pop()[1:], -1)
