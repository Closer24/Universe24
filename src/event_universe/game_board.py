"""The GameBoard: every family's NodeState over the Nodes (node.py), a flat list of lines of dimension one per family, and the detectors, stepped one interval at a time in the law's order (ALGEBRA.md #the-interval): the read and Rule3 on every line, the detectors' reports, the one write per held line; `step_inverse` runs the same acts back. The GameBoard groups the lines into families for the readings and the sources as the loader derived them (loader/derived.py): the form D summed over a record's lines, the Wronskian W the bilinear of a plane's two, the share over every line, the axis lines of a holder read into the paces. The board's face rule (core/ports.py) is the file's: the wraps, the Nodes its inner faces declare beyond the board and its receding faces, beyond which it grows by layers of zeros as the front reaches them (growth.py), every declared coordinate staying the file's. No record's count of bodies is kept: a body's Nodes are where its family's share stands about its declared Nodes, derived when a report needs them (reports.standing); a message is a laid record and no body; a detector is a region of Nodes declared in the file, a declared instrument, its click its report of the net current into it through its front boundary Ports, with the region's name and never a Node (ALGEBRA.md #the-count-is-the-records-share), the count of every family the share of its record, a reading, and every other reading a GameBoard diagnostic; the guard reads the initial state once at load and no act of the interval. Where the world declares the `instrument` (its window, its seed and its generator) the instrument draws inside the run at every window's end from the window's inflows the reports gathered and writes its click on the GameBoard at one Node (`credit.py`, features/click; HIGHLIGHTS.md, the owner's decision of 2026-10-02): the loop's act from outside the Node, as the lay and the receding face are, forward only; the Node knows nothing of it, and a world without the key runs as before bit for bit."""

from __future__ import annotations

from collections.abc import Callable, Sequence
from dataclasses import replace
from typing import Any

import numpy as np

from event_universe import credit, front, growth, meeting, node, share
from event_universe.bookings import Bookings, booked_of, booked_sources, record_lines, sources_of
from event_universe.core import paces
from event_universe.core.ports import Wrap
from event_universe.features.currents import Vector
from event_universe.features.start import Sourced, held_rests
from event_universe.features.write import carried
from event_universe.loader.derived import count_wall, held_write, quanta_records, readers_of, turns
from event_universe.loader.keys import Node
from event_universe.loader.messages import MessageRow
from event_universe.loader.mode import Levels
from event_universe.loader.world import BodyRow, World
from event_universe.reports import Detector, book, click, entering, field, level_sums, parts, standing

Observer = Callable[[dict[str, object]], None]
Currents = dict[int, tuple[np.ndarray, ...]]  # per family of quanta its current through each Port
Stresses = dict[node.Sourcing, Vector]  # per record of quanta its tension on each axis
Rulers = dict[
    node.Sourcing, node.Rulers
]  # per record of quanta the paces of its read, the write's rulers


class GameBoard:
    """One world on the GameBoard, stepped interval by interval; `observer` receives the output lines `click`, `parts` and `field`."""

    def __init__(self, world: World, observer: Observer | None = None) -> None:
        paces.clear_memo()  # the paces computed once per content value within this run, kept between none
        self.world, self.observer, self.tick = world, observer, 0
        self.shape, self.offset = world.shape, (0, 0, 0)
        self.growths: list[growth.Growth] = []
        self.ended: dict[str, object] | None = None
        self.wrap = Wrap(*world.periodic, self.mask(world.beyond) if world.beyond else None)
        self.families, self.kind = world.families, world.kind
        self.unit = world.link_unit  # the Link's unit G, the run's declaration like Gamma
        self.order = [index for index, family in enumerate(self.families) if family.quanta]
        self.held = [index for index, family in enumerate(self.families) if family.held]
        self.turning = [index for index in self.order if turns(self.families, index)]  # turned records
        action = self.world.quantum_action
        self.writes = {index: held_write(self.families, index, action) for index in self.held}
        self.states = [
            node.empty_state(family, self.shape, self.walls(index), self.kind)
            for index, family in enumerate(self.families)
        ]
        self.origins = [0] * len(self.families)  # the remainder the start gave each held row
        for number, (record, row) in enumerate(self.laid_rows()):
            if isinstance(row, BodyRow) and row.instrument is not None:
                meeting.laid_record(self, number, record)
            elif self.families[row.family].quanta:
                self.lay(row, record)  # a kick on a holder of the content is laid after the start
        self.start()
        for record, row in self.laid_rows():
            if not self.families[row.family].quanta:
                self.lay(row, record)  # the kick: the row's own travelling events on its rest, no count
        self.fields: dict[tuple[int, str], tuple[int | None, int | None]] = {}  # the last field readings
        for index in self.order:
            node.guarded(index, self.families, self.states, self.world.node_clock, self.wrap, self.unit)
        self.detectors = [
            Detector(r.name, None if r.body is not None else self.mask(r.positions), r.body, r.declared)
            for r in world.detectors
        ]
        self.laid = {index: self.total_share(index)[0] for index in self.order}  # the books' origin
        self.gate()
        self.credit = credit.Books.of(self)

    def walls(self, index: int) -> tuple[int, ...]:
        """The walls of a family's one write per line, none for a family that holds nothing."""
        return self.writes[index].walls if index in self.writes else ()

    def laid_rows(self) -> list[tuple[int, BodyRow | MessageRow]]:
        """The records the file lays with their record numbers: the bodies, each the next record of its family (a charged family's bodies each own one row of the sign, `derived.row_of`; every other family's bodies add into its one record), then the messages, each on its family's first record (a packet is no standing record)."""
        found: list[tuple[int, BodyRow | MessageRow]] = []
        for n, body in enumerate(self.world.bodies):
            record = [b.family for b in self.world.bodies[:n]].count(body.family)
            found.append((min(record, self.families[body.family].records - 1), body))
        return found + [(0, message) for message in self.world.messages]

    def lay(self, row: BodyRow | MessageRow, record: int = 0) -> None:
        """A body's or a message's levels from the mode file added to its family's lines of the record `record` (`node.record_slice`), one event laid on every part of the record alike (the pair family's two parts laid equal, ALGEBRA.md #the-click-is-the-meeting): its real pair to each part's first line, its second pair to the part's second line where the family is a plane (the loader admits none otherwise)."""
        family, lines = self.families[row.family], self.states[row.family].lines
        span = node.record_slice(family, record)
        for first in range(span.start, span.stop, family.width):
            lines[first] = self.added(lines[first], row.now, row.before)
            if family.plane:
                lines[first + 1] = self.added(lines[first + 1], row.im_now, row.im_before)

    def added(self, record: node.Record, now: Levels, before: Levels) -> node.Record:
        """A line with a body's or a message's two levels from the mode file added over the GameBoard."""
        added = record.now + self.board_array(now), record.before + self.board_array(before)
        return replace(record, now=added[0], before=added[1])

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
        """The start (ALGEBRA.md #the-generator (g), the start; #what-a-body-is, the four lines (a) and (c)): every held family's time line at the rest of its line, with or without a gap, under the sources the laid records write, the massless row's rest with its vacuum content added at every Node (the row's `rest`, the same rest read beyond every face; ALGEBRA.md #what-is-open, item 22): the form of the laid record as the hold's write books it, D_i = now^2 - next x before over the record's lines with next the step of Rule3 at the paces of the held rows' rests, for a row sourced by the form, and the Wronskian of the step's booking for the holder of the sign (`node.form`, `node.wronskian` on the booking of `stepped`), each at the weight with which the record's family reads the row (the hold's reciprocity, `readers_of`, `weight_of`), over the write's wall E_s T, scaled per proper volume and per proper interval at the paces of the rest as the write scales it (`rest`, `paces.write_factor`; no tension stands at the start); the lay and the rest iterated to the fixed point where the sources return themselves (features/start, `held_rests`): the rests laid, every record stepped once at their paces and booked as the hold books it, the rests solved again from those bookings, until the levels repeat (or repeat an earlier state one unit off at most, a rounding tie; a cycle refused by name), from nothing, so the hold's first write is the start's source within Rule3's rounding; both levels, the remainder at the half wall of the rule the row steps by; every write remainder stands at half its wall from `node.empty_state`; a held row of the content with no source at 0 (or its rest) with the same remainder; every held row's record at the start its laid message plus its sourced rest, the level now and the level before alike (the rest the static solution of the row's line at the paces and the laid message a travelling one, so their sum is the record; the holder of the sign keeps its laid light where nothing sources it); the declared count stays the body's, read from the laid record by the gate."""
        holders = [(i, 0) for i in self.held if not self.families[i].wronskian]
        signs = [
            (i, row)
            for i in self.held
            if self.families[i].wronskian and self.sourced(i)
            for row in range(self.families[i].records)
        ]
        rows, gamma = holders + signs, self.world.node_clock

        line_of = {row: int(node.record_slice(self.families[row[0]], row[1]).start) for row in rows}
        walls = {row: self.walls(row[0])[0] for row in rows}
        messages = {row: self.states[row[0]].lines[line_of[row]] for row in rows}

        def booked(levels: Sequence[np.ndarray]) -> tuple[list[Sourced], list[Sourced]]:
            return booked_sources(
                self.families,
                self.states,
                rows,
                holders,
                walls,
                messages,
                levels,
                self.wrap,
                gamma,
                self.unit,
            )

        seed = [node.zeros(self.shape, self.kind) for _ in rows]
        try:
            fields = held_rests(booked, seed, self.wrap, self.world.width, gamma, self.unit)
        except ValueError as refusal:
            raise ValueError(f"the start of the held families: {refusal}") from refusal
        for row in rows:
            self.states[row[0]].lines[line_of[row]] = messages[row]
        for row, found in zip(rows, fields, strict=True):
            remainder = node.full(self.shape, found.remainder, self.kind)
            index, line, message = row[0], line_of[row], self.states[row[0]].lines[line_of[row]]
            self.states[index].lines[line] = node.Record(
                message.now + found.levels, message.before + found.levels, remainder
            )
            self.origins[index] = found.remainder
        for index in self.held:
            family, lines = self.families[index], self.states[index].lines
            if family.rest:
                time = lines[0]
                lines[0] = replace(time, now=time.now + family.rest, before=time.before + family.rest)

    def sourced(self, index: int) -> bool:
        """Whether anything sources a held row at the start: a reader's laid record with a Wronskian other than 0 at a Node for the holder of the sign (a real record sources none of it, so the holder keeps its laid record, light)."""
        return any(
            bool(np.asarray(node.wronskian(self.record(reader), self.families[reader].plane)).any())
            for reader in readers_of(self.families, index)
        )

    def gate(self) -> None:
        """The gate on every declared body at the start (ALGEBRA.md #the-count-is-the-records-share): a body's declared count is within the rounding of its family's share in quanta over its declared Nodes, ((|c - read| - 1) div 2)^2 <= c, refused by name beyond it; a reading of the laid record, no lay."""
        for number, row in enumerate(self.world.bodies):
            declared = sum(row.counts)
            read = int(self.quanta(row.family)[0][self.mask(row.nodes)].sum())
            off = abs(declared - read)
            half = int(carried(off - 1, 2, 0)[0])  # (|c - read| - 1) div 2, the division act
            if off > 1 and half * half > declared:
                raise ValueError(
                    f"the body {number} declares the count {declared} and its family's share reads {read} "
                    f"quanta at its Nodes at T = {self.world.quantum_action}: a declared count is within the "
                    "rounding of the share in quanta, ((|c - read| - 1) div 2)^2 <= c (ALGEBRA.md #the-count-is-the-records-share)"
                )

    def lines_of(self, index: int, record: int) -> list[node.Record]:
        """The lines of one record of a family of quanta as they stand (`bookings.record_lines`)."""
        return record_lines(self.families, index, record, self.states[index].lines)

    def read(self, index: int, direction: int = 1, record: int = 0) -> tuple[Any, node.Factors]:
        """A record's read at the interval's start in `direction`: the content and its six Links' factors (`meeting.read`, every sign row but the record's own, the Links the world cuts at 0 among them)."""
        return meeting.read(self, index, direction, record)

    def rulers(self, direction: int) -> Rulers:
        """Every record of quanta's paces at the interval's start in `direction`, the clock and the three axes' paces of its read at every Node (`node.rulers`), the write's factor's rulers for the bookings it sources (ALGEBRA.md, The write per proper volume and per proper interval); read from the held rows' levels the step in `direction` starts from, the same numbers forward and back."""
        gamma = self.world.node_clock
        return {
            s: node.rulers(s[0], self.families, self.states, direction, self.wrap, gamma, s[1])
            for s in sources_of(self.families, self.order)
        }

    def share_of(self, index: int, direction: int = 1) -> tuple[np.ndarray, np.ndarray]:
        """A family of quanta's share at every Node in the current's units, a reading of each of its records' lines at the paces of that record's read at the level a step in `direction` starts from, summed over the records (share.family_share; ALGEBRA.md #the-count-is-the-records-share), with the mask of its frozen Nodes, every Link pace 0 under any record's read, where the share is not read (`share.frozen`)."""
        family, gamma = self.families[index], self.world.node_clock
        found: Any = 0
        frozen = np.zeros(self.shape, dtype=bool)
        for record in quanta_records(self.families, index):
            content, factors = self.read(index, direction, record)
            lines = self.lines_of(index, record)
            found = found + share.family_share(
                family, lines, self.wrap, gamma, content, factors, self.unit
            )
            frozen |= np.broadcast_to(share.frozen(gamma, content), self.shape)
        return np.asarray(found), frozen

    def quanta(self, index: int) -> tuple[np.ndarray, np.ndarray]:
        """A family's share in quanta at every Node, (share + W_c div 2) div W_c, a reading, with the mask of its frozen Nodes, where it is not read."""
        found, frozen = self.share_of(index)
        return share.quanta_of(
            found, count_wall(self.families[index], self.world.quantum_action), self.kind
        ), frozen

    def total_share(self, index: int) -> tuple[int | None, int]:
        """A family's share summed over the GameBoard in the current's units, a reading, None over a GameBoard holding a frozen Node (its share is not read, no number invented), and the count of its frozen Nodes."""
        found, frozen = self.share_of(index)
        return (None if frozen.any() else int(found.sum(dtype=object))), int(frozen.sum())

    def body_nodes(self, number: int) -> np.ndarray:
        """A body's Nodes as a report needs them: where its family's share stands in quanta about its declared Nodes, a frozen Node among them standing, derived now and kept nowhere (`reports.standing`)."""
        row = self.world.bodies[number]
        quanta, frozen = self.quanta(row.family)
        return standing(self.mask(row.nodes), (quanta != 0) | frozen, self.wrap)

    def books(self) -> dict[str, dict[str, int | None]]:
        """The books per family of quanta, a GameBoard diagnostic (`reports.book`): its share summed over the GameBoard in the current's units and in quanta over its wall W_c, the share's drift from the one it started with (Rule3's own rounding over the run, 0 on an exact record), the three None while a Node is frozen, the least Link pace of the final state and the frozen Nodes' count."""
        found: dict[str, dict[str, int | None]] = {}
        for index in self.order:
            family, gamma = self.families[index], self.world.node_clock
            wall = count_wall(family, self.world.quantum_action)
            (total, cold), laid = self.total_share(index), self.laid[index]
            quanta = drift = None
            if total is not None:
                quanta = int(share.quanta_of(np.array([total], dtype=object), wall, object)[0])
                drift = None if laid is None else total - laid
            pace = node.least_pace(index, self.families, self.states, gamma, self.wrap, self.unit)
            found[family.name] = book(total, quanta, drift, pace, cold)
        return found

    def stepped(self, index: int, direction: int) -> tuple[list[node.Record], list[node.Booking]]:
        """Every record of a family stepped by Rule3 in `direction` with the rule of its own read (from the held rows' levels the step starts from, the Node's content and its six Links' contents, the Node's twice with each Link's own tension, every sign row but the record's own, the Links the world cuts at 0), every held row of the content among them, with or without a gap, the time line of the massless row reading its rest beyond every face, a turned record's planes under the rotation (`meeting.stepped`, `node.step_records`), with one booking per record its form and its Wronskian are read from."""
        return meeting.stepped(self, index, direction)

    def record(self, index: int) -> list[node.Record]:
        """A family's record, the lines its share, its currents, its tension, its form and its Wronskian are read from: every line of a family of quanta (every record's), the time line of a held row of the content, and for a holder of the sign its light, the sum of its rows (`node.light_record`)."""
        family, lines = self.families[index], self.states[index].lines
        return [node.light_record(family, lines)] if family.wronskian else lines[: family.record]

    def currents(self) -> Currents:
        """Every family of quanta's current through each Port at every Node, read from its record as it stands (`node.currents_of`): before Rule3 acts, the pair the step starts from, so that the share's change over the step is exactly their sum (ALGEBRA.md #the-count-is-the-records-share); a charged family's records' currents added, light's the current of its rows' sum."""
        return {
            index: node.currents_of(self.families[index].pair[0], self.record(index), self.wrap)
            for index in self.order
        }

    def stresses(self) -> Stresses:
        """Every record of quanta's tension's part on each axis at every Node, read from its lines as they stand, the pair the step starts from (`node.stresses_of`): the Node's own part h_a(i) the content's axis lines take in their one write, the Link's tension being the sum of its two ends' parts, read through the Ports at the next interval (ALGEBRA.md #the-primitives, The tension)."""
        return {
            s: node.stresses_of(self.families[s[0]].pair[0], self.lines_of(*s), self.wrap)
            for s in sources_of(self.families, self.order)
        }

    def sense_currents(self) -> Stresses:
        """Every turned record's sign current on each axis at every Node, the mean of the Node's two a-Links' Wronskian currents, J_a / 2 with J_a = Im(conj(z_i) (z_(+a) - z_(-a))), read from its lines as they stand at the interval's start (`node.sense_current_of`): the source the odd lines of the record's own row take in their one write under the rotation at the wall den T."""
        return {
            s: node.sense_current_of(self.lines_of(*s), self.wrap)
            for s in sources_of(self.families, self.order)
            if s[0] in self.turning
        }

    def step(self) -> None:
        """One interval forward, each act one loop over the families or the detectors (ALGEBRA.md #the-interval), every act one Link's reach so that the whole interval's dependency radius is one Link (#the-paces, The Link's two ends, the local test): the receding faces grown where the front reaches them (`growth.grow`; at the largest size the run ends, named in `ended`, and no act is taken); the currents, the turned records' sign currents and the tensions' parts read from every record at the pair the step starts from, and every family of quanta's paces, the write's rulers, from the held rows' levels at the start (`rulers`), the lines of the start kept for the parts' report; the read and Rule3 on every line, the form D and the Wronskian W read about the step from its booking; the detectors' reports; the one write per held line from the bookings of the start."""
        if self.ended is not None:
            raise RuntimeError(f"the run ended at interval {self.tick}: {self.ended}")
        if not growth.grow(self):
            return
        self.tick += 1
        forms, turns = Bookings(), Bookings()
        currents, senses, stresses = self.currents(), self.sense_currents(), self.stresses()
        rulers, begun = self.rulers(1), [state.lines for state in self.states]
        found = {index: self.stepped(index, 1) for index in range(len(self.families))}
        for index, (lines, bookings) in found.items():
            family, state = self.families[index], self.states[index]
            for record in lines:
                self.bounded(family.name, record)
            if family.quanta:
                booked = booked_of(self.families, index, bookings)
                for held, gained in zip((forms, turns), booked, strict=True):
                    held.update(gained)
            state.lines = lines
        self.report(currents, forms, begun)
        for index in self.held:
            self.hold(index, forms, turns, 1, stresses, senses, rulers)
        credit.windowed(self)
        meeting.jumped(self)
        front.advanced(self)

    def hold(
        self,
        index: int,
        forms: Bookings,
        turns: Bookings,
        direction: int,
        stresses: Stresses,
        senses: Stresses,
        rulers: Rulers,
    ) -> None:
        """The one write per line of one held family, forward or back (ALGEBRA.md #the-primitives, the row "the hold"; The write per proper volume and per proper interval): the numerators from the bookings of the families that source it, the Wronskians for the holder of the sign and the forms for a row sourced by the form, each scaled by the write's factor at the sourcing family's paces of the interval's start (`rulers`), and from their axis bookings at the interval's start, the tensions' parts read from the records for a row of the content and the sign currents for the holder of the sign under the rotation (`node.write_sources`), each line's division at its wall with its one remainder (`node.held_write`)."""
        family, state = self.families[index], self.states[index]
        bookings, axes = turns if family.wronskian else forms, senses if family.rotation else stresses
        numerators = node.write_sources(
            index, self.families, bookings, axes, self.writes[index], rulers, self.world.node_clock
        )
        state.lines, state.write_remainders = node.held_write(
            state.lines, numerators, self.walls(index), state.write_remainders, direction
        )
        for line in state.lines:
            self.bounded(family.name, line)

    def bounded(self, name: str, record: node.Record) -> None:
        """The amplitude bound A of the world: a level beyond it refuses the run by name."""
        if node.largest(record) > self.world.amplitude_bound:
            raise RuntimeError(
                f"the family {name!r} reached the level {node.largest(record)} at interval {self.tick}, above the world's amplitude bound A = {self.world.amplitude_bound}: the run is refused"
            )

    def declared_board(self) -> np.ndarray:
        """The declared board: the file's own Nodes over the GameBoard as grown, the layers a receding face has grown beyond them (what leaves into those layers has left the world, `growth`)."""
        found = np.zeros(self.shape, dtype=bool)
        found[tuple(slice(f, f + e) for f, e in zip(self.offset, self.world.shape, strict=True))] = True
        return found

    def report(self, currents: Currents, forms: Bookings, begun: list[list[node.Record]]) -> None:
        """The detectors' reports, the clicks (ALGEBRA.md #the-count-is-the-records-share; the owner's words of 2026-09-30, no click names a Node, the detector a declared instrument): per family of quanta and detector (a detector's declared Nodes, the Nodes of the body it names derived now, the open faces' layer), one `click` line where it is not 0: the net current into the region through the instrument's front boundary Ports at its Nodes this interval, in the current's units (the front: the Ports leading in from the declared board outside the instrument, `declared_board`; not the Ports between two regions of one instrument and not those toward a receding face's grown layers), the density that entered from the declared board, the host's reading for the credit by the shares; never a Node (`reports.inflow`, `reports.click`, the line labelled the measurement). For a family of several parts (the pair family), per declared region one `parts` line where a sum is not 0: the signed sums of each part's two levels over the region at the interval's start (`begun`, the lines the step started from), the instrument's read the credit pairs through the root (ALGEBRA.md #the-click-is-the-meeting; `reports.level_sums`, `reports.parts`)."""
        own, union = self.declared_board(), credit.instrument_nodes(self)
        sums: dict[int, dict[str, list[list[int]]]] = {}
        for index, through in currents.items():
            family = self.families[index]
            for detector in self.detectors:
                nodes = self.body_nodes(detector.body) if detector.body is not None else detector.nodes
                assert nodes is not None
                came = entering(nodes, through, self.wrap, union if detector.declared else nodes, own)
                seen = int(came.sum(dtype=object))
                if seen != 0 and self.observer is not None:
                    self.observer(click(self.tick, family.name, detector.name, seen))
                if detector.declared:
                    credit.booked(self, index, detector.name, came)
                if family.parts > 1 and detector.declared:
                    levels = level_sums(nodes, begun[index])
                    if any(any(level) for level in levels) and self.observer is not None:
                        self.observer(parts(self.tick, family.name, detector.name, levels))
                    sums.setdefault(index, {})[detector.name] = levels
        for index, found in sums.items():
            credit.joined(self, index, found)
        self.fields_read(forms)

    def fields_read(self, forms: Bookings) -> None:
        """A GameBoard reading, no measurement, labelled so (`reports.field`): per family and declared region, the family's density over the region this interval, one `field` line where it differs from the last interval's: for a family of quanta its share in quanta summed over the region (the packet's passage), None over a region holding a frozen Node, every Link pace 0 (its share is not read and no number is invented; ALGEBRA.md #the-count-is-the-records-share, the frozen Node), with the frozen Nodes' wells D div T of the interval summed beside as their content reading (`well`); for a holder of the content the square of its time line's deviation from the row's rest summed over the region (a row with no count, its travelling events' passage; the advisor's reading of a kick's arrival, #1563 comment 5916154126)."""
        for index, (family, state) in enumerate(zip(self.families, self.states, strict=True)):
            frozen, well = np.zeros(self.shape, dtype=bool), None
            if family.quanta:
                density, frozen = self.quanta(index)
                form: Any = sum(
                    forms[(index, record)] for record in quanta_records(self.families, index)
                )
                well = node.well(form, self.world.quantum_action)
            else:
                deviation = state.lines[0].now - family.rest
                density = deviation * deviation
            for detector in self.detectors:
                if not detector.declared or detector.nodes is None:
                    continue
                cold = detector.nodes & frozen
                reading = None if cold.any() else int(density[detector.nodes].sum(dtype=object))
                content = int(well[cold].sum(dtype=object)) if well is not None and cold.any() else None
                if self.fields.get((index, detector.name)) == (reading, content):
                    continue
                self.fields[(index, detector.name)] = (reading, content)
                if self.observer is not None:
                    self.observer(field(self.tick, family.name, detector.name, reading, content))

    def booked_back(
        self,
        index: int,
        books: dict[int, list[node.Record]],
        forms: Bookings,
        turns: Bookings,
        stresses: Stresses,
        senses: Stresses,
    ) -> None:
        """A family of quanta's lines one interval back, its record free of any write: every line back, its form and its Wronskian read about the step from the same levels the forward write read (its booking, the same numbers; a turned plane's from z_now and the un-turned levels u and v alone, with no z_before in them), its tension's parts and a turned record's sign current from the pair the interval started with, the lines the inverse returns (as the forward bookings read them), the lines kept aside until every read of the interval's start is done; a turned plane's level before comes back as u, the inverse's first stage (`node.step_plane`)."""
        family = self.families[index]
        lines, bookings = self.stepped(index, -1)
        booked = booked_of(self.families, index, bookings)
        for held, gained in zip((forms, turns), booked, strict=True):
            held.update(gained)
        for record in quanta_records(self.families, index):
            own = record_lines(self.families, index, record, lines)
            stresses[(index, record)] = node.stresses_of(family.pair[0], own, self.wrap)
            if index in self.turning:
                senses[(index, record)] = node.sense_current_of(own, self.wrap)
        books[index] = lines

    def step_inverse(self) -> None:
        """One interval back, the same acts in reverse order with Rule3's direction -1 (ALGEBRA.md #the-direction): the write's rulers read first from the held rows' levels at the interval's start, which the state after the interval still holds as their `before` (the write touched the level now alone), then a held family's write back once every family that sources it is booked back, a family of quanta booked back once its own write is off (the holder of the sign before the rows it sources), then every held row of the content stepped back, and last, every held row standing at the previous interval's start again, each turned plane's level before turned back by that interval's angle (`node.turned_before` at -1, the inverse's second stage around the holders' write back: the mathematician's 119); the lay is not taken back."""
        forms, turns, stresses, senses = Bookings(), Bookings(), Stresses(), Stresses()
        rulers = self.rulers(-1)  # the held rows' levels the interval started from, their `before`
        books: dict[int, list[node.Record]] = {}
        pending, gamma = list(self.held), self.world.node_clock
        while True:
            for index in self.order:
                if index not in books and (index not in self.held or index not in pending):
                    self.booked_back(index, books, forms, turns, stresses, senses)
            sources = {held: readers_of(self.families, held) for held in pending}
            ready = [held for held in pending if all(index in books for index in sources[held])]
            if not pending:
                break
            assert ready, "the held rows' sources form a cycle"
            for held in ready:
                self.hold(held, forms, turns, -1, stresses, senses, rulers)
            pending = [held for held in pending if held not in ready]
        for index in (held for held in self.held if held not in books):
            books[index] = self.stepped(index, -1)[0]
        for index, lines in books.items():
            self.states[index].lines = lines
        for index in self.turning:
            self.states[index].lines = node.turned_back(index, self.families, self.states, gamma)
        self.tick, self.ended = self.tick - 1, None
        while self.growths and self.growths[-1][0] == self.tick + 1:
            growth.resize(self, *self.growths.pop()[1:], -1)
