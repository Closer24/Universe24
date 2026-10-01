"""The GameBoard: every family's NodeState over the Nodes (node.py), a flat list of lines of dimension one per family, and the detectors, stepped one interval at a time in the law's order (ALGEBRA.md #the-interval): the read and Rule3 on every line, the detectors' reports, the one write per held line; `step_inverse` runs the same acts back. The GameBoard groups the lines into families for the readings and the sources as the loader derived them (loader/derived.py): the form D summed over a record's lines, the Wronskian W the bilinear of a plane's two, the share over every line, the axis lines of a holder read into the paces. The board's face rule (core/ports.py) is the file's: the wraps, the Nodes its inner faces declare beyond the board and its receding faces, beyond which it grows by layers of zeros as the front reaches them (growth.py), every declared coordinate staying the file's. No ledger of bodies is kept: a body's Nodes are where its family's share stands about its declared Nodes, derived when a report needs them (reports.standing); a message is a laid record and no body; a detector is a region of Nodes declared in the file, a declared instrument, its click its report of the net current into it through its front boundary Ports, with the region's name and never a Node (ALGEBRA.md #the-count-is-the-records-share), the count of every family the share of its record, a reading, and every other reading a GameBoard diagnostic; the guard reads the initial state once at load and no act of the interval."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import replace

import numpy as np

from event_universe import growth, node, share
from event_universe.core.ports import Wrap
from event_universe.features.currents import Vector
from event_universe.features.start import rest
from event_universe.features.write import carried
from event_universe.loader.derived import HeldWrite, count_wall, held_write, readers_of, weight_of
from event_universe.loader.keys import Node
from event_universe.loader.messages import MessageRow
from event_universe.loader.mode import Levels
from event_universe.loader.world import FACE_NAME, BodyRow, World
from event_universe.reports import Detector, inflow, standing

Observer = Callable[[dict[str, object]], None]
Currents = dict[int, tuple[np.ndarray, ...]]  # per family of quanta its current through each Port
Stresses = dict[int, Vector]  # per family of quanta its tension on each axis
Bookings = dict[int, np.ndarray]


class GameBoard:
    """One world on the GameBoard, stepped interval by interval; `observer` receives the output lines `click` and `field`."""

    def __init__(self, world: World, observer: Observer | None = None) -> None:
        self.world, self.observer, self.tick = world, observer, 0
        self.shape, self.offset = world.shape, (0, 0, 0)
        self.growths: list[growth.Growth] = []
        self.ended: dict[str, object] | None = None
        beyond = self.mask(world.beyond) if world.beyond else None
        self.wrap = Wrap(world.periodic[0], world.periodic[1], world.periodic[2], beyond)
        self.families, self.kind = world.families, world.kind
        self.order = [index for index, family in enumerate(self.families) if family.quanta]
        self.held = [index for index, family in enumerate(self.families) if family.held]
        action = self.world.quantum_action
        self.writes: dict[int, HeldWrite] = {
            index: held_write(self.families, index, action) for index in self.held
        }
        self.states = [
            node.empty_state(family, self.shape, self.walls(index), self.kind)
            for index, family in enumerate(self.families)
        ]
        self.origins = [0] * len(self.families)  # the remainder the start gave each held row
        for row in self.laid_rows():
            if self.families[row.family].quanta:
                self.lay(row)  # a kick on a holder of the content is laid after the start, on its rest
        self.start()
        for row in self.laid_rows():
            if not self.families[row.family].quanta:
                self.lay(row)  # the kick: the row's own travelling events on its rest, no count
        self.fields: dict[tuple[int, str], int] = {}  # the last field reading per family and region
        for index in self.order:
            node.guarded(index, self.families, self.states, self.world.node_clock)
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
        self.laid = {index: self.total_share(index) for index in self.order}  # the books' origin
        self.gate()

    def walls(self, index: int) -> tuple[int, ...]:
        """The walls of a family's one write per line, none for a family that holds nothing."""
        return self.writes[index].walls if index in self.writes else ()

    def laid_rows(self) -> list[BodyRow | MessageRow]:
        """The records the file lays: the bodies and the messages, in the file's order."""
        return [*self.world.bodies, *self.world.messages]

    def lay(self, row: BodyRow | MessageRow) -> None:
        """A body's or a message's levels from the mode file added to its family's lines: its real pair to the first line, its second pair to the second where the family is a plane (the loader admits none otherwise)."""
        lines = self.states[row.family].lines
        lines[0] = self.added(lines[0], row.now, row.before)
        if len(lines) > 1 and self.families[row.family].plane:
            lines[1] = self.added(lines[1], row.im_now, row.im_before)

    def added(self, record: node.Record, now: Levels, before: Levels) -> node.Record:
        """A line with a body's or a message's two levels from the mode file added over the GameBoard."""
        return replace(
            record,
            now=record.now + self.board_array(now),
            before=record.before + self.board_array(before),
        )

    def board_array(self, values: Levels) -> np.ndarray:
        """The levels the mode file lays as an array over the GameBoard: the nonzero Nodes' flat x-major indexes with their levels, 0 elsewhere."""
        found = node.zeros(self.shape, self.kind).reshape(-1)
        for at, value in values:
            found[at] += value
        return found.reshape(self.shape)

    def mask(self, nodes: tuple[Node, ...]) -> np.ndarray:
        """The mask of a set of Nodes declared at the file's coordinates, on the GameBoard as grown."""
        found = np.zeros(self.shape, dtype=bool)
        found[tuple((np.array(nodes) + np.array(self.offset)).T)] = True
        return found

    def start(self) -> None:
        """The start (ALGEBRA.md #the-generator (g), the start): every held family's time line at the rest of its line, with or without a gap, under the sources of the bodies at their Nodes and of the messages over the whole GameBoard, the massless row's rest with its vacuum content added at every Node (the row's `rest`, the same rest read beyond every face; ALGEBRA.md #what-is-open, item 22): the share of the record's lines in quanta over the count's wall (a reading of the form that sources the fields) for a row sourced by the form and the Wronskian's quanta at the written moment, W div T (`node.well`, a reading), for the holder of the sign (its rest, of either sign), each at the weight with which the record's family reads the row, over the row's divisor (features/start), both levels, the remainder at the half wall of the rule the row steps by; every write remainder stands at half its wall from `node.empty_state`; a held row of the content with no source at 0 (or its rest) with the same remainder, the holder of the sign keeping its laid record where nothing sources it."""
        forms = []
        for row in self.laid_rows():
            family = self.families[row.family]
            if not family.quanta:
                continue  # a kick on a holder of the content sources nothing: it is the row's own events
            pairs = [(row.now, row.before), (row.im_now, row.im_before)][: family.lines]
            records = [
                node.Record(
                    self.board_array(now), self.board_array(before), node.zeros(self.shape, self.kind)
                )
                for now, before in pairs
            ]
            total = share.family_share(family, records, self.wrap, self.world.node_clock)
            laid = share.quanta_of(total, count_wall(family, self.world.quantum_action), self.kind)
            turn = node.well(node.wronskian(records), self.world.quantum_action)
            everywhere = np.ones(self.shape, dtype=bool)
            on = self.mask(row.nodes) if isinstance(row, BodyRow) else everywhere
            forms.append((row.family, np.where(on, laid, 0), np.where(on, turn, 0)))
        for index in self.held:
            family = self.families[index]
            assert family.divisor is not None
            counts = node.zeros(self.shape, self.kind)
            for source, form, turn in forms:
                booking = turn if family.wronskian else form
                counts = counts + weight_of(index, self.families[source]) * booking
            if family.quanta and not counts.any():
                continue  # the holder of the sign keeps its laid record where nothing sources it
            wall = node.rule_of(family, self.world.node_clock, 0)[2]
            try:
                field = rest(counts, family.pair, self.wrap, family.divisor, self.world.width, wall)
            except ValueError as refusal:
                raise ValueError(f"the start of the held family {family.name!r}: {refusal}") from refusal
            remainder = node.full(self.shape, field.remainder, self.kind)
            self.states[index].lines[0] = node.Record(
                field.levels.copy(), field.levels.copy(), remainder
            )
            self.origins[index] = field.remainder
        for index in self.held:
            family, lines = self.families[index], self.states[index].lines
            if family.rest:
                time = lines[0]
                lines[0] = replace(time, now=time.now + family.rest, before=time.before + family.rest)

    def gate(self) -> None:
        """The gate on every declared body at the start (ALGEBRA.md #the-count-is-the-records-share): a body's declared count is within the rounding of its family's share in quanta over its declared Nodes, ((|c - read| - 1) div 2)^2 <= c, refused by name beyond it; a reading of the laid record, no lay."""
        for number, row in enumerate(self.world.bodies):
            declared = sum(row.counts)
            read = int(self.quanta(row.family)[self.mask(row.nodes)].sum())
            off = abs(declared - read)
            half = int(carried(off - 1, 2, 0)[0])  # (|c - read| - 1) div 2, the division act
            if off > 1 and half * half > declared:
                raise ValueError(
                    f"the body {number} declares the count {declared} and its family's share reads "
                    f"{read} quanta at its Nodes at T = {self.world.quantum_action}: a declared count is within "
                    "the rounding of the share in quanta, ((|c - read| - 1) div 2)^2 <= c (ALGEBRA.md "
                    "#the-count-is-the-records-share)"
                )

    def emit(self, line: dict[str, object]) -> None:
        """One output line to the observer, if any."""
        if self.observer is not None:
            self.observer(line)

    def instrument(self) -> np.ndarray:
        """The instrument: the union of the declared regions (every detector with its own positions, the faces' layer and the bodies' detectors aside), whose boundary is where the reports are read (ALGEBRA.md #the-click-ends-nothing): what moves between two regions of one screen is not seen twice."""
        found = np.zeros(self.shape, dtype=bool)
        for detector in self.detectors:
            if detector.body is None and detector.name != FACE_NAME and detector.nodes is not None:
                found |= detector.nodes
        return found

    def share_of(self, index: int, level: str = "now") -> np.ndarray:
        """A family of quanta's share at every Node in the current's units, a reading of its record's lines at the paces of its read from `level` (share.family_share; ALGEBRA.md #the-count-is-the-records-share)."""
        family, state = self.families[index], self.states[index]
        content, axis = node.read(index, self.families, self.states, level)
        return share.family_share(family, state.lines, self.wrap, self.world.node_clock, content, axis)

    def quanta(self, index: int) -> np.ndarray:
        """A family's share in quanta at every Node, (share + W_c div 2) div W_c, a reading."""
        wall = count_wall(self.families[index], self.world.quantum_action)
        return share.quanta_of(self.share_of(index), wall, self.kind)

    def total_share(self, index: int) -> int:
        """A family's share summed over the GameBoard in the current's units, a reading."""
        return int(self.share_of(index).sum(dtype=object))

    def body_nodes(self, number: int) -> np.ndarray:
        """A body's Nodes as a report needs them: where its family's share stands in quanta about its declared Nodes, derived now and kept nowhere (`reports.standing`)."""
        row = self.world.bodies[number]
        return standing(self.mask(row.nodes), self.quanta(row.family) != 0, self.wrap)

    def contents(self) -> list[dict[str, int]]:
        """Every body's quanta per family of quanta: that family's share in quanta summed over the body's Nodes (a GameBoard reading)."""
        return [
            {
                self.families[index].name: int(self.quanta(index)[self.body_nodes(number)].sum())
                for index in self.order
            }
            for number in range(len(self.world.bodies))
        ]

    def books(self) -> dict[str, dict[str, int]]:
        """The books per family of quanta, a GameBoard diagnostic: its share summed over the GameBoard in the current's units and in quanta over its wall W_c, the share's drift from the one it started with (Rule3's own rounding over the run, 0 on an exact record), and the least Link pace of the final state."""
        found: dict[str, dict[str, int]] = {}
        for index in self.order:
            family = self.families[index]
            wall = count_wall(family, self.world.quantum_action)
            total = self.total_share(index)
            quanta = int(share.quanta_of(np.array([total], dtype=object), wall, object)[0])
            pace = node.least_pace(index, self.families, self.states, self.world.node_clock)
            found[family.name] = {
                "share": total,
                "quanta": quanta,
                "drift": total - self.laid[index],
                "pace": pace,
            }
        return found

    def stepped(
        self, index: int, level: str, direction: int
    ) -> tuple[tuple[np.ndarray, tuple[np.ndarray, ...]], list[node.Record]]:
        """A family's read (from the held rows' `level`) and every line of it stepped by Rule3 in `direction` with the rule of that read, every held row of the content among them, with or without a gap, the time line of the massless row reading its rest beyond every face (`node.step`, `fill`)."""
        family, state = self.families[index], self.states[index]
        read = node.read(index, self.families, self.states, level)
        rule = node.rule_of(family, self.world.node_clock, *read)
        found = [
            node.step(record, rule, self.wrap, direction, family.rest if number == 0 else 0)
            for number, record in enumerate(state.lines)
        ]
        return read, found

    def currents(self) -> Currents:
        """Every family of quanta's current through each Port at every Node, read from its lines as they stand (`node.currents_of`): before Rule3 acts, the pair the step starts from, so that the share's change over the step is exactly their sum (ALGEBRA.md #the-count-is-the-records-share)."""
        return {
            index: node.currents_of(self.families[index].pair[0], self.states[index].lines, self.wrap)
            for index in self.order
        }

    def stresses(self) -> Stresses:
        """Every family of quanta's tension on each axis at every Node, read from its levels now (`node.stresses_of`), the stress the held rows' axis lines take in their one write."""
        return {
            index: node.stresses_of(self.families[index].pair[0], self.states[index].lines, self.wrap)
            for index in self.order
        }

    def step(self) -> None:
        """One interval forward, each act one loop over the families or the detectors (ALGEBRA.md #the-interval): the receding faces grown where the front reaches them (`growth.grow`; at the largest size the run ends, named in `ended`, and no act is taken); the currents read from every record at the pair the step starts from; the read and Rule3 on every line, the form D and the Wronskian W read about the step; the detectors' reports; the one write per held line with the tensions read from the stepped levels."""
        if self.ended is not None:
            raise RuntimeError(f"the run ended at interval {self.tick}: {self.ended}")
        if not growth.grow(self):
            return
        self.tick += 1
        forms: Bookings = {}
        turns: Bookings = {}
        currents = self.currents()
        found = {index: self.stepped(index, "now", 1) for index in range(len(self.families))}
        for index, (_read, lines) in found.items():
            state = self.states[index]
            for record in lines:
                self.bounded(self.families[index].name, record)
            if self.families[index].quanta:
                forms[index] = node.form(state.lines, lines)
                turns[index] = node.wronskian(lines)
            state.lines = lines
        stresses = self.stresses()
        self.report(currents)
        for index in self.held:
            self.hold(index, forms, turns, 1, stresses)

    def hold(
        self, index: int, forms: Bookings, turns: Bookings, direction: int, stresses: Stresses
    ) -> None:
        """The one write per line of one held family, forward or back (ALGEBRA.md #the-primitives, the row "the hold"): the numerators from the bookings of the families that source it, the Wronskians for the holder of the sign and the forms for a row sourced by the form, and from their tensions read from the records (`node.write_sources`), each line's division at its wall with its one remainder (`node.held_write`)."""
        family, state = self.families[index], self.states[index]
        bookings = turns if family.wronskian else forms
        numerators = node.write_sources(index, self.families, bookings, stresses, self.writes[index])
        state.lines, state.write_remainders = node.held_write(
            state.lines, numerators, self.walls(index), state.write_remainders, direction
        )
        for line in state.lines:
            self.bounded(family.name, line)

    def bounded(self, name: str, record: node.Record) -> None:
        """The amplitude bound A of the world: a level beyond it refuses the run by name."""
        if node.largest(record) > self.world.amplitude_bound:
            raise RuntimeError(
                f"the family {name!r} reached the level {node.largest(record)} at interval {self.tick}, above "
                f"the world's amplitude bound A = {self.world.amplitude_bound}: the run is refused"
            )

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

    def report(self, currents: Currents) -> None:
        """The detectors' reports, the clicks (ALGEBRA.md #the-count-is-the-records-share; the owner's words of 2026-09-30, no click names a Node, the detector a declared instrument): per family of quanta and detector (a detector's declared Nodes, the Nodes of the body it names derived now, the open faces' layer), one `click` line where it is not 0: the net current into the region through the instrument's front boundary Ports at its Nodes this interval, in the current's units (the front: the Ports leading in from the declared board outside the instrument, `declared_board`; not the Ports between two regions of one instrument and not those toward a receding face's grown layers), the density that entered from the declared board, the host's reading for the credit by the shares; never a Node (`reports.inflow`)."""
        own = self.declared_board()
        for index, through in currents.items():
            family = self.families[index]
            for detector in self.detectors:
                nodes = self.body_nodes(detector.body) if detector.body is not None else detector.nodes
                assert nodes is not None
                declared = detector.body is None and detector.name != FACE_NAME
                boundary_of = self.instrument() if declared else nodes
                seen = inflow(nodes, through, self.wrap, boundary_of, own)
                if seen != 0:
                    self.emit(
                        {
                            "event": "click",
                            "tick": self.tick,
                            "family": family.name,
                            "detector": detector.name,
                            "inflow": seen,
                        }
                    )
        self.fields_read()

    def fields_read(self) -> None:
        """A GameBoard reading, no measurement, labelled so: per family and declared region, the family's density over the region this interval, one `field` line where it differs from the last interval's: for a family of quanta its share in quanta summed over the region (the packet's passage), for a holder of the content the square of its time line's deviation from the row's rest summed over the region (a row with no count, its travelling events' passage; the advisor's reading of a kick's arrival, #1563 comment 5916154126)."""
        for index, (family, state) in enumerate(zip(self.families, self.states, strict=True)):
            if family.quanta:
                density = self.quanta(index)
            else:
                deviation = state.lines[0].now - family.rest
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
        books: dict[int, list[node.Record]],
        forms: Bookings,
        turns: Bookings,
        stresses: Stresses,
    ) -> None:
        """A family of quanta's lines one interval back, its record free of any write: its tension read from the levels as the step left them (as the forward write read it), every line back, its form and its Wronskian read about the step from the same three levels the forward write read, the lines kept aside until every read of the interval's start is done."""
        state = self.states[index]
        stresses[index] = node.stresses_of(self.families[index].pair[0], state.lines, self.wrap)
        _read, lines = self.stepped(index, "before", -1)
        forms[index] = node.form(lines, state.lines)
        turns[index] = node.wronskian(state.lines)
        books[index] = lines

    def step_inverse(self) -> None:
        """One interval back, the same acts in reverse order with Rule3's direction -1 (ALGEBRA.md #the-direction): a held family's write back once every family that sources it is booked back, a family of quanta booked back once its own write is off (the holder of the sign before the rows it sources), then every held row of the content stepped back; the lay is not taken back."""
        forms: Bookings = {}
        turns: Bookings = {}
        stresses: Stresses = {}
        books: dict[int, list[node.Record]] = {}
        pending = list(self.held)
        while True:
            for index in self.order:
                if index not in books and (index not in self.held or index not in pending):
                    self.booked_back(index, books, forms, turns, stresses)
            sources = {held: readers_of(self.families, held) for held in pending}
            ready = [held for held in pending if all(index in books for index in sources[held])]
            if not pending:
                break
            assert ready, "the held rows' sources form a cycle"
            for held in ready:
                self.hold(held, forms, turns, -1, stresses)
            pending = [held for held in pending if held not in ready]
        for index in self.held:
            if index not in books:
                books[index] = self.stepped(index, "before", -1)[1]
        for index, lines in books.items():
            self.states[index].lines = lines
        self.tick, self.ended = self.tick - 1, None
        while self.growths and self.growths[-1][0] == self.tick + 1:
            growth.resize(self, *self.growths.pop()[1:], -1)
