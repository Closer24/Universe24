"""The lattice: every family's NodeState over the Nodes (node.py), a flat list of lines of dimension one per family, and the node_detectors, stepped one interval at a time in the law's order (ALGEBRA.md #the-interval): the read and Rule3 on every line, the node_detectors' reports, the one write per held line; `step_inverse` runs the same acts back, and `step` with no act is the step at the Nodes alone, the run forward of the meeting that runs back (`meeting_back`); the observers (`Lattice.observers`, callables the lattice calls after every step and every step back with the interval, the direction and the pass) are the look's, nothing of the law. The lattice groups the lines into families for the readings and the sources as the loader derived them (loader/derived.py): the form D summed over a record's lines, the Wronskian W the bilinear of a plane's two, the share over every line, the axis lines of a holder read into the paces. The board's face rule (core/ports.py) is the file's: the wraps, the Nodes its inner faces declare beyond the board and its receding faces, beyond which it grows by layers of zeros as the front reaches them (growth.py), every declared coordinate staying the file's. No record's count of bodies is kept: a body's Nodes are where its family's share stands about its declared Nodes, derived when a report needs them (reports.standing_nodes); a packet is a laid record and no body; a reader is a region of Nodes declared in the file, a declared NodeDetector, its click its report of the net current into it through its front boundary Ports, with the region's name and never a Node (ALGEBRA.md #the-count-is-the-records-share), the count of every family the share of its record, a reading, and every other reading a lattice diagnostic; the guard reads the initial state once at load and no act of the interval. Where the world declares the `draw` (its window) the NodeDetectors draw inside the run at every window's end from the window's inflows the reports gathered, by the click's read of the board (`digits.read_of`), and write their click on the lattice at one Node (`credit.py`, features/click; HIGHLIGHTS.md, the owner's decision): the loop's act from outside the Node, as the lay and the receding face are, forward only; the Node knows nothing of it, and a world without the key runs as before bit for bit."""

from __future__ import annotations

from collections.abc import Callable, Sequence
from dataclasses import replace
from typing import Any

import numpy as np

import event_universe.board_readings as board_readings
import event_universe.meeting_back as meeting_back
import event_universe.readings as readings
import event_universe.records as records
from event_universe import (
    credit,
    emission,
    meeting,
    meeting_board,
    node,
    registry,
    seed,
    share,
    shear,
    swap,
)
from event_universe.board_readings import Stresses
from event_universe.bookings import Bookings, booked_of, booked_sources, record_lines, sources_of
from event_universe.core import paces
from event_universe.core.rule3 import division_forward, wall_of
from event_universe.features import phase, read, volume
from event_universe.features.start import Sourced
from event_universe.features.start.rests import held_rests
from event_universe.frames import frames_of
from event_universe.loader.derived import charged, held_write_of, readers_of, turns
from event_universe.loader.keys import Node
from event_universe.loader.world import World
from event_universe.reports import book
from event_universe.walls import sourced

Output = Callable[[dict[str, object]], None]
Observer = Callable[[int, int, int], None]
# per record of quanta the paces of its read, the write's rulers
Rulers = dict[records.Sourcing, records.Rulers]


class Lattice:
    """One world on the lattice, stepped interval by interval; `output` receives the lines (`reports.py`: `click`, `parts` and `credit` the node_detectors', `field`, `erasure`, `lay` and `face` the lattice's diagnostics); `observers`, empty at the start, the callables a host registers (the look's reader, tools/look/record.py) and the lattice calls after every `step` and every `step_inverse` with (the interval, the direction, +1 or -1, and the pass, `passes`, from 1 and one more at every change of direction: 1 the forward run, 2 the run back of the meeting that runs back, 3 the forward run again), the last direction kept as `heading`; a world that declares nothing is laid before the start by `seed.uniform_seed` and read by its own board after the readers' acts, `meeting_board.closed` (ALGEBRA.md, The uniform seed is a lay, The board reads itself, 2026-10-24); a reading of the board at the call and no act; `tick`, the board's own clock, the count of the loop's forward steps with their acts (the owner's word of 2026-10-19: the board advances by its tick alone), advanced in `step` with its acts and never by the step at the Nodes alone nor by `step_inverse`, so that through the click's act the tick stands at the close while `interval`, the state's time the frames read, runs back to the birth and forward again; the Nodes' own clocks, the paces, run as ever (`credit.clocked_regions`), honoured by the exact inverse; `off_diagonals`, whether a held row of the world declares the shear (the shear's readings made then alone); `covector.gate` after the lay, the lattice Lorenz constraint on every holder under the Lorentz form; `unit`, G, the Link's unit, the run's declaration like Gamma. The swap at the top (swap.py; ALGEBRA.md, The swap at the top): `write_walls` every held line's write wall as the last held write took it, read by the swap's complement, `swaps` the swaps at the top as (interval, direction, Nodes), a reading, `swap.kept` the pre-state before the act and the post-state before the inverse; every line is born at the half wall, the lay's origin and the start's alike (ALGEBRA.md, The start), every held row's wall fixed per Node at the start in Python's integers, beyond 63 bits at the shipped weights; the gate's rounding half is (|c - read| - 1) div 2, the division act."""

    def __init__(self, world: World, output: Output | None = None) -> None:
        paces.clear_memo()  # the memos cleared at a run's start: the paces per (Gamma, content), the volume's levels per Gamma, the orbits' table
        volume.LEVELS.clear()
        phase.ORBITS.clear()  # SEEDED keeps a living lattice's states on their orbit
        read.READS.clear()  # the records' reads, made once per interval and given again
        self.world, self.interval, self.passes, self.heading, self.tick = world, 0, 1, 1, 0
        self.output: Output | None = None
        self.observers = list[Observer]()
        self.shape = world.shape
        self.families = volume.at_start(world.families)
        self.kind, self.unit = world.kind, world.link_unit
        self.order = [index for index, family in enumerate(self.families) if family.quanta]
        self.held = [index for index, family in enumerate(self.families) if family.held]
        self.turning = [index for index in self.order if turns(self.families, index)]
        self.fixed_walls, self.write_walls = dict[int, list[Any]](), dict[int, list[Any]]()
        self.swaps: list[tuple[int, int, int]] = []
        self.writes = {i: held_write_of(self.families, i, world.quantum_action) for i in self.held}
        self.states = [
            records.empty_state(
                family,
                self.shape,
                self.walls(i),
                self.kind,
                self.half_wall(i),
                registry.start_records(self.families, i),
            )
            for i, family in enumerate(self.families)
        ]
        self.row_walls: dict[
            int, list[Any]
        ] = {}  # per charged family the walls of one row of the sign at the start's paces, the walls its rows are born with (`start`, `born_point`)
        self.born_at: dict[
            int, list[int]
        ] = {}  # per interval the points whose records were born at its close (`born_point`), undone by the step back and born again by the replay
        self.origins = [self.half_wall(index) for index in range(len(self.families))]
        self.amplitude = node.seed_phases(self, world)
        if world.seed is not None:
            seed.uniform_seed(self, world.seed)
        self.start()
        self.output = output
        self.densities: dict[tuple[int, str], tuple[int | None, int | None]] = {}  # the last readings
        for index in self.order:
            node.guarded(index, self.families, self.states, self.world.node_clock, self.unit)
        self.laid = {index: self.total_share(index)[0] for index in self.order}  # the books' origin
        self.credit = credit.Books.of(self)
        self.proper_count = records.zeros(
            self.shape, object
        )  # the law's time count at every Node, SUM over the intervals of the Node's composed clock p_0 at the interval's start, in the unit Gamma one vacuum interval (ALGEBRA.md, The paces compose; The clock near matter): a reading kept beside the states and no act, read by the click's view as `proper` (meeting_board.readings_at)
        self.closes = np.zeros(
            self.shape, dtype=np.int64
        )  # the count of every Node's own closes, the board's own clicks there, read by the click's view as `windows`
        self.turned = np.zeros(
            self.shape, dtype=bool
        )  # the Nodes the fifth act turned this interval (swap.acted), a reading beside `swaps`, read per slab by the slabs' runner (slabs.py)

    def half_wall(self, index: int) -> int:
        """The half wall of the rule a family's lines step by, w div 2 with w = 6 den Gamma^2 G^2 (`wall_of`), the remainder every line is born with: every Node's remainder is born at the half wall, the vacuum (0, 0, w div 2) at every Node, the lay's origin and the start's alike, so that the one rounding of Rule3 is half up at every Node and no neighbour reads a floor (ALGEBRA.md, the start; the owner's word; the mathematician's hand with the advisor's hand, two hands: under the floor a lone massless quantum laid at one Node of an even periodic box grew as t^2 on the uniform mode's double root)."""
        wall = wall_of(self.families[index].pair[1], self.world.node_clock, self.unit)
        return int(division_forward(wall, 2, 0)[0])

    def walls(self, index: int) -> tuple[int, ...]:
        """The walls of a family's one write per line, none for a family that holds nothing."""
        return self.writes[index].walls if index in self.writes else ()

    def mask(self, nodes: tuple[Node, ...]) -> np.ndarray:
        """The mask of a set of Nodes declared at the file's coordinates."""
        found = np.zeros(self.shape, dtype=bool)
        found[tuple(np.array(nodes).T)] = True
        return found

    def start(self) -> None:
        """The start (ALGEBRA.md #the-generator (g), the start; #what-a-body-is, the four lines (a) and (c)): every held family's time line at the rest of its line, with or without a gap, under the sources the laid records write (the one exception the gapped row carrying its volume under the volume form, laid at the vacuum, its two levels the empty state's 0 converted once to the volume Gamma with the remainder at the half wall, the seed at rest the design's initial condition: ALGEBRA.md, The carried momentum, the clause of 2026-10-23; The closed lattice has no rest, the vacuum no rest state of a gapped uniform mode), the massless row's rest with its vacuum content added at every Node (the row's `rest`, the same rest read beyond every face; ALGEBRA.md #what-is-open, item 22): the form of the laid record as the held write's write books it, D_i = now^2 - next x before over the record's lines with next the step of Rule3 at the paces of the held rows' rests, for a row sourced by the form, and the Wronskian of the step's booking for the holder of the sign (`records.form`, `records.wronskian` on the booking of `stepped`), each at the weight with which the record's family reads the row (the held write's reciprocity, `readers_of`, `weight_of`), over the write's wall E_s T, scaled per proper volume and per proper interval at the paces of the rest as the write scales it (`rest`, `paces.write_factor`; no tension stands at the start); the lay and the rest iterated to the fixed point where the sources return themselves (features/start, `held_rests`): the rests laid, every record stepped once at their paces and booked as the held write books it, the rests solved again from those bookings, until the levels repeat (or repeat an earlier state one unit off at most, a rounding tie; a cycle refused by name), from nothing, so the held write's first write is the start's source within Rule3's rounding; both levels, the remainder at the half wall of the rule the row steps by; every write remainder stands at half its wall from `records.empty_state`; a held row of the content with no source at 0 (or its rest) with the same remainder; every held row's record at the start its laid packet plus its sourced rest, the level now and the level before alike (the rest the static solution of the row's line at the paces and the laid packet a travelling one, so their sum is the record; the holder of the sign keeps its laid light where nothing sources it); the declared count stays the body's, read from the laid record by the gate. On a board periodic on every axis every massless row rests free on the zero-mean part of its sources (features/start `rest`, the torus's own static line; ALGEBRA.md, The board's interval is no observable; The closed lattice has no rest) and the sources' mean, the k = 0 component, is carried from the first interval by Rule3's own line at k = 0 (`step`) as the volume's level less the row's own kinetic form at the symmetry's weight in the one write (`held_write`, records.write_sources): no act is added and the Node knows nothing of the board. Every row carrying its volume has its two levels converted once to the volume's (features/volume `started`, the conversion after the start so the rests are solved in the level), and its write remainders born at half the wall per Node at the rest's paces (`records.walls_at`, `records.divided_walls`, `records.write_origins`: the half of the wall the line's write divides at, the volume's time line's Gamma E_s T and not its fixed wall E_s T alone, so its one rounding is half up as every line's; to 2026-10-24 the volume row's origin was the half of the fixed wall, 1 / (2 Gamma) of the wall its write divides at, the builder's finding of #2187, and Universe24's first write read 2 where the half wall gives 3), the walls kept for the run (`fixed_walls`, the wall fixed per Node: the carried factor's one form, the moving wall, which folds the run back; the Boss's decision of 2026-10-22)."""
        holders = volume.resting(self.held, self.families, self.world.families)
        signs = [
            (i, row)
            for i in self.held
            if self.families[i].wronskian and sourced(self, i)
            for row in range(registry.records_of(self.families[i], self.states[i].lines))
        ]
        rows, gamma, world = holders + signs, self.world.node_clock, self.world

        line_of = {row: int(records.record_slice(self.families[row[0]], row[1]).start) for row in rows}
        walls = {row: self.walls(row[0])[0] for row in rows}
        packets = {row: self.states[row[0]].lines[line_of[row]] for row in rows}
        reads = (self.families, self.states, rows, holders, walls, packets)

        def booked(levels: Sequence[np.ndarray]) -> tuple[list[Sourced], list[Sourced]]:
            return booked_sources(*reads, levels, gamma, self.unit, self.amplitude)

        seed = [records.zeros(self.shape, self.kind) for _ in rows]
        try:
            fields = held_rests(booked, seed, world.width, gamma, self.unit)
        except ValueError as refusal:
            raise ValueError(f"the start of the held families: {refusal}") from refusal
        for row, found in zip(rows, fields, strict=True):
            remainder = records.full(self.shape, found.remainder, self.kind)
            index, line, packet = row[0], line_of[row], packets[row]
            self.states[index].lines[line] = records.Record(
                packet.now + found.levels, packet.before + found.levels, remainder
            )
            self.origins[index] = found.remainder
        for index in self.held:
            family, lines = self.families[index], self.states[index].lines
            if family.rest:
                time = lines[0]
                lines[0] = replace(time, now=time.now + family.rest, before=time.before + family.rest)
            lines[0] = volume.started(gamma, world.families[index], lines[0])
            shear.born(self, family, lines)
        self.families = world.families
        rulers = self.rulers(1) if self.held else {}
        for index in self.held:
            sourcing = registry.sourcing(self.families, self.states, index)
            born = records.walls_at(index, self.families, self.writes[index], rulers, gamma, sourcing)
            born = [records.exact(wall) for wall in born]
            divided = records.divided_walls(
                self.families[index], born, gamma
            )  # the wall each write divides at
            self.states[index].write_remainders = records.write_origins(divided, self.shape, object)
            self.fixed_walls[index] = born
        for index in self.order:  # the walls of one row of the sign for a record of a charged family at the start's paces (the same numbers every row of the family had at the start to 2026-10-24: every record's read of the start's content alike), kept for the rows born later (`born_point`)
            if charged(self.families, index):
                sign = next(
                    r.family for r in self.families[index].reads if self.families[r.family].wronskian
                )
                virtual = {(index, 0): node.rulers(index, self.families, self.states, 1, gamma, 0)}
                at_start = records.walls_at(
                    sign, self.families, self.writes[sign], virtual, gamma, [[], [(index, 0)]]
                )
                self.row_walls[index] = [records.exact(w) for w in at_start[self.families[sign].width :]]

    def born_point(self, index: int) -> None:
        """A point's records and rows of the sign born at its first lay by the count (`emission.born_point`, 2026-10-24)."""
        emission.born_point(self, index)

    def unborn_point(self, index: int) -> None:
        """The inverse of `born_point` for the step back (`emission.unborn_point`)."""
        emission.unborn_point(self, index)

    def lines_of(self, index: int, record: int) -> list[records.Record]:
        """The lines of one record of a family of quanta as they stand (`bookings.record_lines`)."""
        return record_lines(self.families, index, record, self.states[index].lines)

    def read(self, index: int, direction: int = 1, record: int = 0) -> tuple[Any, node.Factors]:
        """A record's read at the interval's start in `direction`: the content and its six Links' factors (`node.read`, every sign row but the record's own)."""
        gamma, unit = self.world.node_clock, self.unit
        return node.read(index, self.families, self.states, direction, gamma, unit, record)

    def rulers(self, direction: int) -> Rulers:
        """Every record of quanta's paces at the interval's start in `direction`, the clock and the three axes' paces of its read at every Node (`node.rulers`), the write's factor's rulers for the bookings it sources (ALGEBRA.md, The write per proper volume and per proper interval); read from the held rows' levels the step in `direction` starts from, the same numbers forward and back."""
        return node.rulers_of(self, sources_of(self.families, self.states, self.order), direction)

    def share_of(self, index: int, direction: int = 1, at: Any = None) -> tuple[np.ndarray, np.ndarray]:
        """A family of quanta's share at every Node in the current's units, a reading of the energy, rest and kinetic, in the free rotation's unit (no count: a plane record's count is its charge, `credit.count_of`, the ruling of 2026-10-22) from each of its records' lines at the paces of that record's read at the level a step in `direction` starts from, summed over the records, the share over the whole board read once per interval on the same records and given again to the readers (features/read READS; the architect's second round of 2026-10-24) (share.family_share; ALGEBRA.md #the-count-is-the-records-share), a turned record's from its plain levels too (under the temporal gauge the time Link carries no phase, plane.step_plane), computed at the Nodes the mask `at` names (None: where a level stands) and 0 elsewhere, with the mask of its frozen Nodes, every Link pace 0 under any record's read, where the share is not read (`share.frozen`)."""
        return share.board_share(self, index, direction, at)

    def quanta(self, index: int, at: Any = None) -> tuple[np.ndarray, np.ndarray]:
        """A family's share in quanta at every Node, (share + W_rec div 2) div W_rec in the record's own unit (`credit.record_unit`, C1), a reading at the Node in the free unit (the record's count over the board is its charge for a plane family, `credit.count_of`, the ruling of 2026-10-22; here the Node's share as the sides read it; a body's declared Nodes and the start's count gate read the lay's own support, `share.plain_quanta`), computed at the Nodes the mask `at` names (None: where a level stands, `share_of`) and 0 elsewhere, with the mask of its frozen Nodes, where it is not read."""
        found, frozen = self.share_of(index, 1, at)
        return share.quanta_of(found, self.credit.units[index], self.kind), frozen

    def total_share(self, index: int) -> tuple[int | None, int]:
        """A family's share summed over the lattice in the current's units, a reading, None over a lattice holding a frozen Node (its share is not read, no number invented), and the count of its frozen Nodes."""
        found, frozen = self.share_of(index)
        return (None if frozen.any() else int(found.sum(dtype=object))), int(frozen.sum())

    def books(self) -> dict[str, dict[str, int | None]]:
        """The books per family of quanta, a lattice diagnostic (`reports.book`): its share summed over the lattice in the current's units and in quanta over its own unit W_rec and the written coefficients' norm (`count`, the record's count read from the board, `credit.count_of`, bound as the lattice's method: ALGEBRA.md, The count on the board, 2026-10-20; `credit.record_unit`, C1), its count in the credit's books and its deficit, the quanta taken from it and written nowhere (the undepleted beam, `take.faced`, `credit.Books.deficits`: the board's share in quanta stands above the books' count by the deficit, the three read side by side), the share's drift from the one it started with (Rule3's own rounding over the run, 0 on an exact record), share, quanta and drift None while a Node is frozen, the least Link pace of the final state and the frozen Nodes' count."""
        found: dict[str, dict[str, int | None]] = {}
        for index in self.order:
            family, gamma, books = self.families[index], self.world.node_clock, self.credit
            (total, cold), laid = self.total_share(index), self.laid[index]
            quanta, deficit = self.count(index), books.deficits.get(index, 0)
            drift = None if total is None or laid is None else total - laid
            pace = node.least_pace(index, self.families, self.states, gamma, self.unit)
            found[family.name] = book(total, quanta, books.counts[index], deficit, drift, pace, cold)
        return found

    count = credit.count_of

    def stepped(self, index: int, direction: int) -> tuple[list[records.Record], list[records.Booking]]:
        """Every record of a family stepped by Rule3 in `direction` with the rule of its own read (from the held rows' levels the step starts from, the Node's content and its six Links' contents, the Node's twice with each Link's own tension, every sign row but the record's own, the Links the world cuts at 0), every held row of the content among them, with or without a gap, the time line of the massless row reading its rest beyond every face, a turned record's planes under the rotation (`meeting.stepped`, `flux.step_records`), with one booking per record its form and its Wronskian are read from."""
        return meeting.stepped(self, index, direction)

    def record(self, index: int) -> list[records.Record]:
        """A family's record, the lines its share, its currents, its tension, its form and its Wronskian are read from: every line of a family of quanta (every record's), the time line of a held row of the content, and for a holder of the sign its light, the sum of its rows (`records.rows_total`); a turned record's plain lines (under the temporal gauge the time Link carries no phase, plane.step_plane)."""
        family, lines = self.families[index], self.states[index].lines
        return [records.rows_total(family, lines)] if family.wronskian else lines[: family.record]

    def step(self, acts: bool = True) -> None:
        """One interval forward, each act one loop over the families or the node_detectors (ALGEBRA.md #the-interval), every act one Link's reach so that the whole interval's dependency radius is one Link (#the-paces, The Link's two ends, the local test): the receding faces grown where the front reaches them (`growth.grow`; at the largest size the run ends, named in `ended`, and no act is taken); the sign holder's phase act, each Link's pair iterated by the potential's difference across it read at the start (`phased`, features/phase), first, so that every reading of a turned record takes the Link pairs the step reads (2026-10-21; the act moves the phase lines alone and no level a plain reading takes, every plain record's readings bit for bit); then the bookings' read of every record of quanta (node_detector.weighed_currents) and from it the currents, with the turned records' sign currents and the tensions' parts, read from every record at the pair the step starts from (a turned record's currents the flux line's own with those pairs, read once per interval: board_readings.currents takes a turned family's from the bookings' read), and every family of quanta's paces, the write's rulers, from the held rows' levels at the start (`rulers`), the lines of the start kept for the parts' report; the turned records' sign currents under the Lorentz form the fluxes with the pairs the step reads (board_readings.sense_currents); the read and Rule3 on every line, the form D and the Wronskian W read about the step from its booking; the node_detectors' reports with the faces the step presented as `face` lines; the one write per held line from the bookings of the start; then the NodeDetectors' acts from outside the Node (`credit.counted_windows` with `meeting.closed` at the window's close, `meeting.jumped`, `emission.sourced`, `front.advanced_fronts`); last the observers, with the interval, the direction +1 and the pass. With `acts` False the step at the Nodes alone, the run forward of the meeting that runs back (`meeting_back.run_forward`): no report, no booking and no act of the NodeDetectors, the faces presented from the books' log as ever and the acts' lays of the interval re-applied from the books' log (`meeting_back.logged`), so that the board returns bit for bit the one the run forward had left; no output line. The densities' reading (`board_readings.densities_read`, the one report that reads the state) is taken after the held writes and the fifth act, the state at the interval's end, so that no reading reads an output the floor's turn discards (ALGEBRA.md, The floor, 2026-10-23)."""
        self.interval, forms, turns = self.interval + 1, Bookings(), Bookings()
        kept_state = swap.kept(self)
        node.phase_act(self.held, self.families, self.states, 1, self.world.node_clock)
        rulers, begun = self.rulers(1), [s.lines for s in self.states]
        if (
            self.world.seed is not None
        ):  # the time count: the clock the seed's record reads at the interval's start, summed (every family of quanta reads the same content, so the same clock)
            self.proper_count = self.proper_count + np.asarray(
                rulers[(self.world.seed, 0)][0], dtype=object
            )
        stresses, senses = board_readings.stresses(self), board_readings.sense_currents(self)
        found = {index: self.stepped(index, 1) for index in range(len(self.families))}
        for index, (lines, bookings) in found.items():
            family, state = self.families[index], self.states[index]
            for number, record in enumerate(lines):
                self.bounded(family.name, record, number == 0 and family.motion_volume)
            if family.quanta:
                booked = booked_of(self.families, index, bookings)
                for held, gained in zip((forms, turns), booked, strict=True):
                    held.update(gained)
            state.lines = lines
        for index in self.held:
            self.held_write(index, forms, turns, 1, stresses, senses, rulers, begun)
        swap.stepped(self, kept_state)
        if acts:
            self.tick += 1
            meeting_board.closed(self, kept_state)
        else:
            for index in self.born_at.get(
                self.interval, []
            ):  # the points born at this close, born again before the lays are re-applied
                self.born_point(index)
            meeting_back.logged(self, 1)
        self.passes, self.heading = self.passes + (self.heading < 0), 1
        for observer in self.observers:
            observer(self.interval, 1, self.passes)

    def held_write(
        self,
        index: int,
        forms: Bookings,
        turns: Bookings,
        direction: int,
        stresses: Stresses,
        senses: Stresses,
        rulers: Rulers,
        begun: list[list[records.Record]] | None = None,
    ) -> None:
        """The one write per line of one held family, forward or back (ALGEBRA.md #the-primitives, the row "the held write"; The write per proper volume and per proper interval): the numerators from the bookings of the families that source it, the Wronskians for the holder of the sign and the forms for a row sourced by the form, each scaled by the write's factor at the sourcing family's paces of the interval's start (`rulers`), and from their axis bookings at the interval's start, the tensions' parts read from the records for a row of the content, the shear's parts, the products of the Node's two axis differences, for a row declaring the shear, and the sign currents for the holder of the sign under the rotation (`records.write_sources`), each line's division at its wall with its one remainder (`node.held_write_at`, the Node knowing no line's kind). On a board periodic on every axis the write's mean over the Nodes has no sink and is carried by Rule3's own line at k = 0 (ALGEBRA.md, The closed lattice has no rest; item 6 of what is open; the world's the level form's uniform line, the law as written, or the volume form, the hypothesis of 2026-10-22): the step's Links' sum over the torus vanishes at the vacuum's paces (every Link's difference counted once from each end) and the massless mass D is 0, so the mean level's second difference is the mean write per Node per interval, each Node's write dimmed by its own content factor as this one act applies it, the double root carrying the mean level and the mean velocity exactly in integers (a uniform level with the half wall steps to itself, a uniform velocity to itself); under the volume form the massless row of the content carries its time line as the volume's level X = Gamma (Gamma / p_0)^(d + 1) (features/volume; the momentum hand's derivation M12a read cold by the reader), and its one write is the volume's, ((d + 1) X_now c + r) div (Gamma E_s T) at the one fixed wall, X_now the row's own level at the interval's start as the direction finds it (`begun` forward, the post-state's before back; records.write_sources `motion`), the chain rule between the level and the volume and no hill as an act (ALGEBRA.md, The uniform mode carried by Rule3's own k = 0 line; The mean's velocity is the content's; the owner's locality decision of 2026-10-22: the Node's own two numbers and nothing of the board); at the Node this write is the same division it has always been, fed by the same declared sources, and nothing here tests the board or the family (`uniform_mode` reads the mean, one division with one remainder, a lattice diagnostic)."""
        family, state = self.families[index], self.states[index]
        bookings, axes = turns if family.wronskian else forms, senses if family.rotation else stresses
        line, gamma = state.lines[0] if begun is None else begun[index][0], self.world.node_clock
        motion = (line.now, line.before) if family.motion_volume else None
        write, fixed = self.writes[index], self.fixed_walls.get(index)
        sourcing = registry.sourcing(self.families, self.states, index)
        numerators, walls, _terms = records.write_sources(
            index,
            self.families,
            bookings,
            axes,
            write,
            rulers,
            gamma,
            sourcing,
            motion,
            direction,
            fixed,
        )
        self.write_walls[index] = walls
        state.lines, state.write_remainders = shear.written(
            self, index, numerators, walls, direction, begun
        )
        for number, line in enumerate(state.lines):
            self.bounded(family.name, line, number == 0 and family.motion_volume)

    def bounded(self, name: str, record: records.Record, carried: bool = False) -> None:
        """The amplitude bound A of the world: a level beyond it refuses the run by name; a time line carrying its volume (`carried`) is read through the volume's wall at A (features/volume `bounds_of`, X(A)), its level reading above A where X passes it; downward the carried line has no wall but the crunch, the volume at most 0 at a Node, which the volume's reading refuses by name (features/volume `level_of`; the test of the law's course, the small board's end)."""
        if carried:
            high = volume.bounds_of(self.world.node_clock, self.world.amplitude_bound)[1]
            if (largest := int(np.max(record.now))) > high:
                raise RuntimeError(
                    f"the family {name!r} reached the volume {largest} at interval {self.interval}, beyond the world's amplitude bound A = {self.world.amplitude_bound} read through the volume's level: the run is refused"
                )
            return
        if records.largest(record) > self.world.amplitude_bound:
            raise RuntimeError(
                f"the family {name!r} reached the level {records.largest(record)} at interval {self.interval}, above the world's amplitude bound A = {self.world.amplitude_bound}: the run is refused"
            )

    def booked_back(
        self,
        index: int,
        books: dict[int, list[records.Record]],
        forms: Bookings,
        turns: Bookings,
        stresses: Stresses,
        senses: Stresses,
    ) -> None:
        """A family of quanta's lines one interval back, its record free of any write: every line back, its form and its Wronskian read about the step from the same levels the forward write read (its booking, the same numbers), its tension's parts and a turned record's sign current from the pair the interval started with, the lines the inverse returns (as the forward bookings read them), the lines kept aside until every read of the interval's start is done."""
        family = self.families[index]
        lines, bookings = self.stepped(index, -1)
        booked = booked_of(self.families, index, bookings)
        for held, gained in zip((forms, turns), booked, strict=True):
            held.update(gained)
        for record in registry.quanta_records(self.families, self.states, index):
            own = record_lines(self.families, index, record, lines)
            stresses[(index, record)] = readings.axis_sources_of(
                family.pair[0], own, frames_of(index, self.families, self.states, record)
            )
            if index in self.turning:
                senses[(index, record)] = board_readings.sense_fluxes(self, (index, record), own)
        books[index] = lines

    def step_inverse(self) -> None:
        """One interval back, the same acts in reverse order with Rule3's direction -1 (ALGEBRA.md #the-direction): first the acts' lays of the interval undone from the books' log where the world's draw runs back (`meeting_back.logged`; where the books hold no log, a world with no record of several parts at declared sides, the host tool crosses them from the lines), then the write's rulers read from the held rows' levels at the interval's start, which the state after the interval still holds as their `before` (the write touched the level now alone), then a held family's write back once every family that sources it is booked back, a family of quanta booked back once its own write is off (the holder of the sign before the rows it sources), then every held row of the content stepped back, and last, every line standing at the previous interval's start again, the sign holder's phase lines back by the potentials read there (`phased` at -1, features/phase); the lay is not taken back; the observers called with the interval, the direction -1 and the pass; refused by name first on a world (every board's interval unobservable) (`motion_back`)."""
        meeting_back.logged(self, -1)
        for index in reversed(
            self.born_at.get(self.interval, [])
        ):  # the points born at this interval's close: gone before the step back, as the step ran without them
            self.unborn_point(index)
        forms, turns, stresses, senses = Bookings(), Bookings(), Stresses(), Stresses()
        rulers, ended = self.rulers(-1), [s.lines for s in self.states]
        kept_state = swap.kept(self)
        books: dict[int, list[records.Record]] = {}
        queued = list(self.held)
        while True:
            for index in self.order:
                if index not in books and (index not in self.held or index not in queued):
                    self.booked_back(index, books, forms, turns, stresses, senses)
            ready = [h for h in queued if all(i in books for i in readers_of(self.families, h))]
            if not queued:
                break
            assert ready, "the held rows' sources form a cycle"
            for held in ready:
                self.held_write(held, forms, turns, -1, stresses, senses, rulers)
            queued = [held for held in queued if held not in ready]
        for index in (held for held in self.held if held not in books):
            books[index] = self.stepped(index, -1)[0]
        for index, lines in books.items():
            self.states[index].lines = lines
        shear.inverted(self, ended)
        swap.inverted(self, kept_state)
        node.phase_act(self.held, self.families, self.states, -1, self.world.node_clock)
        self.interval -= 1
        self.passes, self.heading = self.passes + (self.heading > 0), -1
        for observer in self.observers:
            observer(self.interval, -1, self.passes)
