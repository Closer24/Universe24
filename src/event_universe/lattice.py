"""The lattice: every family's NodeState over the Nodes (node.py), a flat list of lines of dimension one per family, and the node_detectors, stepped one interval at a time in the law's order (ALGEBRA.md #the-interval): the read and Rule3 on every line, the node_detectors' reports, the one write per held line; `step_inverse` runs the same acts back, and `step` with no act is the step at the Nodes alone, the run forward of the meeting that runs back (`meeting_back`); the observers (`Lattice.observers`, callables the lattice calls after every step and every step back with the interval, the direction and the pass) are the look's, nothing of the law. The lattice groups the lines into families for the readings and the sources as the loader derived them (loader/derived.py): the form D summed over a record's lines, the Wronskian W the bilinear of a plane's two, the share over every line, the axis lines of a holder read into the paces. The board's face rule (core/ports.py) is the file's: the wraps, the Nodes its inner faces declare beyond the board and its receding faces, beyond which it grows by layers of zeros as the front reaches them (growth.py), every declared coordinate staying the file's. No record's count of bodies is kept: a body's Nodes are where its family's share stands about its declared Nodes, derived when a report needs them (reports.standing_nodes); a packet is a laid record and no body; a reader is a region of Nodes declared in the file, a declared NodeDetector, its click its report of the net current into it through its front boundary Ports, with the region's name and never a Node (ALGEBRA.md #the-count-is-the-records-share), the count of every family the share of its record, a reading, and every other reading a lattice diagnostic; the guard reads the initial state once at load and no act of the interval. Where the world declares the `draw` (its window) the NodeDetectors draw inside the run at every window's end from the window's inflows the reports gathered, by the click's read of the board (`digits.read_of`), and write their click on the lattice at one Node (`credit.py`, features/click; HIGHLIGHTS.md, the owner's decision): the loop's act from outside the Node, as the lay and the receding face are, forward only; the Node knows nothing of it, and a world without the key runs as before bit for bit."""

from __future__ import annotations

from collections.abc import Callable, Sequence
from dataclasses import replace
from typing import Any

import numpy as np

import event_universe.board_readings as board_readings
import event_universe.covector as covector
import event_universe.meeting_back as meeting_back
import event_universe.readings as readings
import event_universe.records as records
from event_universe import credit, emission, front, growth, lists, meeting, node, reports, share, take
from event_universe.board_readings import Currents, Stresses
from event_universe.bookings import Bookings, booked_of, booked_sources, record_lines, sources_of
from event_universe.core import paces
from event_universe.core.ports import Wrap
from event_universe.core.rule3 import division_forward, wall_of
from event_universe.features import volume
from event_universe.features.start import Sourced
from event_universe.features.start.rests import held_rests
from event_universe.features.write import carried
from event_universe.lay import laid
from event_universe.loader.derived import PLANE, held_write_of, quanta_records, readers_of, turns
from event_universe.loader.instrument import laid_parts
from event_universe.loader.interval import kicks_refused
from event_universe.loader.keys import Node
from event_universe.loader.mode import Levels
from event_universe.loader.packets import PacketRow
from event_universe.loader.world import BodyRow, World
from event_universe.node_detector import Weighed, booked_inflows, node_detector_nodes, weighed_currents
from event_universe.reports import NodeDetector, book, click, entering, level_sums, parts, standing_nodes
from event_universe.resonance import clear_memo

Output = Callable[[dict[str, object]], None]
Observer = Callable[[int, int, int], None]
# per record of quanta the paces of its read, the write's rulers
Rulers = dict[records.Sourcing, records.Rulers]


class Lattice:
    """One world on the lattice, stepped interval by interval; `output` receives the lines (`reports.py`: `click`, `parts` and `credit` the node_detectors', `field`, `erasure`, `lay` and `face` the lattice's diagnostics); `observers`, empty at the start, the callables a host registers (the look's reader, tools/look/record.py) and the lattice calls after every `step` and every `step_inverse` with (the interval, the direction, +1 or -1, and the pass, `passes`, from 1 and one more at every change of direction: 1 the forward run, 2 the run back of the meeting that runs back, 3 the forward run again), the last direction kept as `heading`; a reading of the board at the call and no act; `tick`, the board's own clock, the count of the loop's forward steps with their acts (the owner's word of 2026-10-19: the board advances by its tick alone), advanced in `step` with its acts and never by the step at the Nodes alone nor by `step_inverse`, so that through the click's act the tick stands at the close while `interval`, the state's time the frames read, runs back to the birth and forward again; the Nodes' own clocks, the paces, run as ever (`credit.clocked_regions`), honoured by the exact inverse; `off_diagonals`, whether a held row of the world declares the shear (the shear's readings made then alone); `covector.gate` after the lay, the lattice Lorenz constraint on every holder under the Lorentz form; `unit`, G, the Link's unit, the run's declaration like Gamma."""

    def __init__(self, world: World, output: Output | None = None) -> None:
        clear_memo()
        self.world, self.interval, self.passes, self.heading, self.tick = world, 0, 1, 1, 0
        self.output: Output | None = None
        self.observers: list[Observer] = []
        self.shape, self.offset = world.shape, (0, 0, 0)
        self.growths: list[growth.Growth] = []
        self.ended: dict[str, object] | None = None
        self.wrap = Wrap(*world.periodic, self.mask(world.beyond) if world.beyond else None)
        self.families, self.kind, self.unit = (
            volume.at_start(world.families),
            world.kind,
            world.link_unit,
        )
        self.order = [index for index, family in enumerate(self.families) if family.quanta]
        self.held = [index for index, family in enumerate(self.families) if family.held]
        self.turning = [index for index in self.order if turns(self.families, index)]
        self.fixed_walls: dict[int, list[Any]] = {}
        self.off_diagonals = any(family.off_diagonal for family in self.families)
        self.writes = {
            i: held_write_of(self.families, i, world.quantum_action, world.link_unit) for i in self.held
        }
        self.states = [
            records.empty_state(family, self.shape, self.walls(i), self.kind, self.half_wall(i))
            for i, family in enumerate(self.families)
        ]
        # each line born at the half wall, the lay's origin and the start's alike (ALGEBRA.md, The start)
        self.origins = [self.half_wall(index) for index in range(len(self.families))]
        self.amplitude = node.seed_phases(self.families, self.states, self.shape, self.kind, world)
        for number, (record, row) in enumerate(self.laid_rows()):
            if isinstance(row, BodyRow) and row.detector is not None and not row.region:
                meeting.laid_record(self, number, record)
            elif self.families[row.family].quanta:
                self.lay(row, record)  # a kick on a holder of the content is laid after the start
        self.start()
        for record, row in self.laid_rows():
            if not self.families[row.family].quanta:
                kicks_refused(world.unobservable, self.families, [self.families[row.family].name])
                self.lay(row, record)  # the kick: the row's own travelling events on its rest, no count
        covector.gate(self)
        self.output = output
        self.densities: dict[tuple[int, str], tuple[int | None, int | None]] = {}  # the last readings
        for index in self.order:
            node.guarded(index, self.families, self.states, self.world.node_clock, self.wrap, self.unit)
        rows = ((r, self.mask(r.positions) if r.body is None else None) for r in world.node_detectors)
        self.node_detectors = [NodeDetector(r.name, at, r.body, r.declared) for r, at in rows]
        self.laid = {index: self.total_share(index)[0] for index in self.order}  # the books' origin
        self.credit = credit.Books.of(self)
        self.gate()

    def half_wall(self, index: int) -> int:
        """The half wall of the rule a family's lines step by, w div 2 with w = 6 den Gamma^2 G^2 (`wall_of`), the remainder every line is born with: every Node's remainder is born at the half wall, the vacuum (0, 0, w div 2) at every Node, the lay's origin and the start's alike, so that the one rounding of Rule3 is half up at every Node and no neighbour reads a floor (ALGEBRA.md, the start; the owner's word; the mathematician's hand with the advisor's hand, two hands: under the floor a lone massless quantum laid at one Node of an even periodic box grew as t^2 on the uniform mode's double root)."""
        wall = wall_of(self.families[index].pair[1], self.world.node_clock, self.unit)
        return int(division_forward(wall, 2, 0)[0])

    def walls(self, index: int) -> tuple[int, ...]:
        """The walls of a family's one write per line, none for a family that holds nothing."""
        return self.writes[index].walls if index in self.writes else ()

    def laid_rows(self) -> list[tuple[int, BodyRow | PacketRow]]:
        """The records the file lays with their record numbers: the bodies, each the next record of its family (a charged family's bodies each own one row of the sign, `derived.row_of`; every other family's bodies add into its one record), then the packets, each on its family's first record (a packet is no standing record)."""
        found: list[tuple[int, BodyRow | PacketRow]] = []
        for n, body in enumerate(self.world.bodies):
            record = [b.family for b in self.world.bodies[:n]].count(body.family)
            found.append((min(record, self.families[body.family].records - 1), body))
        return found + [(0, packet) for packet in self.world.packets]

    def lay(self, row: BodyRow | PacketRow, record: int = 0) -> None:
        """A body's or a packet's levels from the mode file added to its family's lines of the record `record` (`records.record_slice`), one event laid on every part of the record alike (the pair family's two parts laid equal, ALGEBRA.md #the-click-is-the-meeting), or, for a bound body declared an instrument body through the mode file (`BodyRow.region`, 2026-10-21), on the part carrying its declared count alone, the level it stands in (the other parts empty, a lay in one mode having no amplitude in any other, The click writes on the lattice (j)), and on every real line of a part at the line's declared weight (`weights`, the world file's key on the body or the packet, `keys.weights_of`: the pair times the weight, 1 on every line without the key, so a record of three real lines is laid at (a, b, c) over its three lines and a family of dimension 1 as ever): its real pair to each real line, and to each plane's first line with its second pair, the sense, to the plane's second line (every plane of a record of three planes alike; the loader admits a second pair on no family of real lines), the generator's lay (tools/pixel_mode.py, `one_pass`, `pixel_record`) the same. The loader's door of the one lay act (`lay.laid`; ALGEBRA.md, No write from outside Rule3 wakes the massless row's zero mode): a packet's levels are the generator's, corrected at the lay, so the weights handed to the act are all 0, which means no correction and the guard alone, the board's refusal of a massless packet whose two sums are not 0 (the loader builds no board and refuses nothing of this); a body's levels and a kick on a holder of the content are laid as declared; a plane's second pair, its sense, on the plane's second line; the remainders stand at the half wall every line was born with (`records.empty_state`), the origin None; the lay is the initial state and no event of the run, so it reports no lay line (the output is handed to the lattice after its construction)."""
        family = self.families[row.family]
        span, step = records.record_slice(family, record), PLANE if family.plane else 1
        guarded = isinstance(row, PacketRow) and family.quanta
        weights = records.zeros(self.shape, object) if guarded else None
        for first in (span.start + part * family.width for part in laid_parts(row, family)):
            for line, weight in zip(range(first, first + family.width, step), row.weights, strict=True):
                pairs = [(row.now, row.before), (row.second_now, row.second_before)]
                for number, (now, before) in enumerate(pairs[: 2 if family.plane else 1]):
                    change = (weight * self.board_array(now), weight * self.board_array(before))
                    laid(self, row.family, line + number, change, weights, None)

    def board_array(self, values: Levels) -> np.ndarray:
        """The levels the mode file lays as an array over the lattice: the nonzero Nodes' flat x-major indexes with their levels, 0 elsewhere."""
        found = records.zeros(self.shape, self.kind).reshape(-1)
        for at, value in values:
            found[at] += value
        return found.reshape(self.shape)

    def mask(self, nodes: tuple[Node, ...]) -> np.ndarray:
        """The mask of a set of Nodes declared at the file's coordinates, on the lattice as grown."""
        found = np.zeros(self.shape, dtype=bool)
        found[tuple((np.array(nodes) + np.array(self.offset)).T)] = True
        return found

    def start(self) -> None:
        """The start (ALGEBRA.md #the-generator (g), the start; #what-a-body-is, the four lines (a) and (c)): every held family's time line at the rest of its line, with or without a gap, under the sources the laid records write, the massless row's rest with its vacuum content added at every Node (the row's `rest`, the same rest read beyond every face; ALGEBRA.md #what-is-open, item 22): the form of the laid record as the held write's write books it, D_i = now^2 - next x before over the record's lines with next the step of Rule3 at the paces of the held rows' rests, for a row sourced by the form, and the Wronskian of the step's booking for the holder of the sign (`records.form`, `records.wronskian` on the booking of `stepped`), each at the weight with which the record's family reads the row (the held write's reciprocity, `readers_of`, `weight_of`), over the write's wall E_s T, scaled per proper volume and per proper interval at the paces of the rest as the write scales it (`rest`, `paces.write_factor`; no tension stands at the start); the lay and the rest iterated to the fixed point where the sources return themselves (features/start, `held_rests`): the rests laid, every record stepped once at their paces and booked as the held write books it, the rests solved again from those bookings, until the levels repeat (or repeat an earlier state one unit off at most, a rounding tie; a cycle refused by name), from nothing, so the held write's first write is the start's source within Rule3's rounding; both levels, the remainder at the half wall of the rule the row steps by; every write remainder stands at half its wall from `records.empty_state`; a held row of the content with no source at 0 (or its rest) with the same remainder; every held row's record at the start its laid packet plus its sourced rest, the level now and the level before alike (the rest the static solution of the row's line at the paces and the laid packet a travelling one, so their sum is the record; the holder of the sign keeps its laid light where nothing sources it); the declared count stays the body's, read from the laid record by the gate. On a board periodic on every axis a massless row's rest needs a sink and the start refuses it by name, unless the world declares `interval: unobservable` (`World.unobservable`, loader/interval.py; ALGEBRA.md, The board's interval is no observable, a hypothesis under its own name, 2026-10-22) or the law's `uniform: carried` (`World.uniform`, loader/world.py `uniform_of`, the carried mean as written 2026-10-21): then every massless row rests on the zero-mean part of its sources (features/start `rest`, the torus's own static line) and the sources' mean, the k = 0 component, is carried from the first interval by Rule3's own line at k = 0 (`step`), under the hypothesis's key less the row's own kinetic form at the symmetry's weight in the one write (`held_write`, records.write_sources): no act is added, the Node knows nothing of the board, and a world without either key runs as before bit for bit. Under the key every massless row's two levels are converted once to the volume's (features/volume `started`, the flag off during the start so the rests are solved in the level), and a row under `factor: carried` has its write remainders born at half the wall per Node at the rest's paces (`records.walls_at`, `records.write_origins`: the half wall of the division the line takes, so its one rounding is half up as every line's), the walls kept for the run (`fixed_walls`, the wall fixed per Node under either key: the carried factor's one form, the moving wall, which folds the run back, no form; the reader's keep list and the Boss's decision of 2026-10-22)."""
        holders = [(i, 0) for i in self.held if not self.families[i].wronskian]
        signs = [
            (i, row)
            for i in self.held
            if self.families[i].wronskian and self.sourced(i)
            for row in range(self.families[i].records)
        ]
        rows, gamma, world = holders + signs, self.world.node_clock, self.world

        line_of = {row: int(records.record_slice(self.families[row[0]], row[1]).start) for row in rows}
        walls = {row: self.walls(row[0])[0] for row in rows}
        packets = {row: self.states[row[0]].lines[line_of[row]] for row in rows}
        reads = (self.families, self.states, rows, holders, walls, packets)

        def booked(levels: Sequence[np.ndarray]) -> tuple[list[Sourced], list[Sourced]]:
            return booked_sources(*reads, levels, self.wrap, gamma, self.unit, self.amplitude)

        seed = [records.zeros(self.shape, self.kind) for _ in rows]
        try:
            free = world.uniform or world.unobservable
            fields = held_rests(booked, seed, self.wrap, world.width, gamma, self.unit, free)
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
        self.families = world.families
        carried = [i for i in self.held if self.families[i].factor_carried]
        rulers = self.rulers(1) if carried else {}
        for index in carried:
            born = records.walls_at(index, self.families, self.writes[index], rulers, gamma)
            born = [
                records.exact(wall) for wall in born
            ]  # Python's integers, beyond 63 bits at the shipped weights
            self.states[index].write_remainders = records.write_origins(born, self.shape, object)
            self.fixed_walls[index] = born

    def vacuum_walls(self, index: int) -> list[int]:
        """A held row's fixed walls at a Node with no level, one integer per line: the walls per Node of the carried factor (`records.walls_at`) at the rulers every source reads at the rest, the clock from the content of the holders it reads at their rests (the fill beyond a face, the level the volume's reading gives the rest's volume) and the pace along every axis the Node's pace under no tension; the walls a layer grown beyond a receding face is born with (growth.resize), the same the start gives every Node standing at the rest."""
        gamma = self.world.node_clock
        rulers: Rulers = {}
        for source in sources_of(self.families, self.order):
            reads = [r for r in self.families[source[0]].reads if not self.families[r.family].rotation]
            if not reads:
                rulers[source] = (gamma, (gamma, gamma, gamma))
                continue
            content = np.full((1, 1, 1), sum(r.weight * self.families[r.family].rest for r in reads))
            clock, pace = paces.node_paces(gamma, content)
            axis = paces.axis_pace(pace, gamma, 0, 0)
            rulers[source] = (clock, (axis, axis, axis))
        walls = records.walls_at(index, self.families, self.writes[index], rulers, gamma)
        return [int(np.asarray(wall, dtype=object).reshape(-1)[0]) for wall in walls]

    def sourced(self, index: int) -> bool:
        """Whether anything sources a held row at the start: a reader's laid record with a Wronskian other than 0 at a Node for the holder of the sign (a real record sources none of it, so the holder keeps its laid record, light)."""
        return any(
            bool(np.asarray(records.wronskian(self.record(reader), self.families[reader].plane)).any())
            for reader in readers_of(self.families, index)
        )

    def gate(self) -> None:
        """The gate on every declared body at the start (ALGEBRA.md #the-count-is-the-records-share): a body's declared count is within the rounding of its family's count in quanta over its declared Nodes (a bound record's the board's whole count, its charge; `credit.gate_count`), ((|c - read| - 1) div 2)^2 <= c, refused by name beyond it; a reading of the laid record, no lay."""
        for number, row in enumerate(self.world.bodies):
            declared = sum(row.detector.counts if row.detector is not None else row.counts)
            read = lists.gate_count(self, row)
            off = abs(declared - read)
            half = int(carried(off - 1, 2, 0)[0])  # (|c - read| - 1) div 2, the division act
            if off > 1 and half * half > declared:
                raise ValueError(
                    f"the body {number} declares the count {declared} and its family's share reads {read} "
                    f"quanta at its Nodes at T = {self.world.quantum_action}: a declared count is within the "
                    "rounding of the share in quanta, ((|c - read| - 1) div 2)^2 <= c (ALGEBRA.md #the-count-is-the-records-share)"
                )

    def lines_of(self, index: int, record: int) -> list[records.Record]:
        """The lines of one record of a family of quanta as they stand (`bookings.record_lines`)."""
        return record_lines(self.families, index, record, self.states[index].lines)

    def read(self, index: int, direction: int = 1, record: int = 0) -> tuple[Any, node.Factors]:
        """A record's read at the interval's start in `direction`: the content and its six Links' factors (`meeting.read_with_cuts`, every sign row but the record's own, the Links the world cuts at 0 among them)."""
        return meeting.read_with_cuts(self, index, direction, record)

    def rulers(self, direction: int) -> Rulers:
        """Every record of quanta's paces at the interval's start in `direction`, the clock and the three axes' paces of its read at every Node (`node.rulers`), the write's factor's rulers for the bookings it sources (ALGEBRA.md, The write per proper volume and per proper interval); read from the held rows' levels the step in `direction` starts from, the same numbers forward and back."""
        gamma = self.world.node_clock
        return {
            s: node.rulers(s[0], self.families, self.states, direction, self.wrap, gamma, s[1])
            for s in sources_of(self.families, self.order)
        }

    def share_of(self, index: int, direction: int = 1, at: Any = None) -> tuple[np.ndarray, np.ndarray]:
        """A family of quanta's share at every Node in the current's units, a reading of the energy, rest and kinetic, in the free rotation's unit (no count: a plane record's count is its charge, `credit.count_of`, the ruling of 2026-10-22) from each of its records' lines at the paces of that record's read at the level a step in `direction` starts from, summed over the records (share.family_share; ALGEBRA.md #the-count-is-the-records-share), a turned record's from its plain levels too (under the temporal gauge the time Link carries no phase, plane.step_plane), computed at the Nodes the mask `at` names (None: where a level stands) and 0 elsewhere, with the mask of its frozen Nodes, every Link pace 0 under any record's read, where the share is not read (`share.frozen`)."""
        family, gamma = self.families[index], self.world.node_clock
        found: Any = 0
        weights = covector.weights(family)
        frozen = np.zeros(self.shape, dtype=bool)
        for record in quanta_records(self.families, index):
            content, factors = self.read(index, direction, record)
            lines = self.record(index) if family.lorentz else self.lines_of(index, record)
            found = found + share.family_share(
                family, lines, self.wrap, gamma, content, factors, self.unit, at, None, weights
            )
            frozen |= np.broadcast_to(share.frozen(gamma, content), self.shape)
        return np.asarray(found), frozen

    def quanta(self, index: int, at: Any = None) -> tuple[np.ndarray, np.ndarray]:
        """A family's share in quanta at every Node, (share + W_rec div 2) div W_rec in the record's own unit (`credit.record_unit`, C1), a reading at the Node in the free unit (the record's count over the board is its charge for a plane family, `credit.count_of`, the ruling of 2026-10-22; here the Node's share as the sides and the gate read it), computed at the Nodes the mask `at` names (None: where a level stands, `share_of`) and 0 elsewhere, with the mask of its frozen Nodes, where it is not read."""
        found, frozen = self.share_of(index, 1, at)
        return share.quanta_of(found, self.credit.units[index], self.kind), frozen

    def total_share(self, index: int) -> tuple[int | None, int]:
        """A family's share summed over the lattice in the current's units, a reading, None over a lattice holding a frozen Node (its share is not read, no number invented), and the count of its frozen Nodes."""
        found, frozen = self.share_of(index)
        return (None if frozen.any() else int(found.sum(dtype=object))), int(frozen.sum())

    def body_nodes(self, number: int) -> np.ndarray:
        """A body's Nodes as a report needs them: where its family's share stands in quanta about its declared Nodes, a frozen Node among them standing, derived now and kept nowhere (`reports.standing_nodes`)."""
        row = self.world.bodies[number]
        quanta, frozen = self.quanta(row.family)
        return standing_nodes(self.mask(row.nodes), (quanta != 0) | frozen, self.wrap)

    def books(self) -> dict[str, dict[str, int | None]]:
        """The books per family of quanta, a lattice diagnostic (`reports.book`): its share summed over the lattice in the current's units and in quanta over its own unit W_rec and the written coefficients' norm (`count`, the record's count read from the board, `credit.count_of`, bound as the lattice's method: ALGEBRA.md, The count on the board, 2026-10-20; `credit.record_unit`, C1), its count in the credit's books and its deficit, the quanta taken from it and written nowhere (the undepleted beam, `take.faced`, `credit.Books.deficits`: the board's share in quanta stands above the books' count by the deficit, the three read side by side), the share's drift from the one it started with (Rule3's own rounding over the run, 0 on an exact record), share, quanta and drift None while a Node is frozen, the least Link pace of the final state and the frozen Nodes' count."""
        found: dict[str, dict[str, int | None]] = {}
        for index in self.order:
            family, gamma, books = self.families[index], self.world.node_clock, self.credit
            (total, cold), laid = self.total_share(index), self.laid[index]
            quanta, deficit = self.count(index), books.deficits.get(index, 0)
            drift = None if total is None or laid is None else total - laid
            pace = node.least_pace(index, self.families, self.states, gamma, self.wrap, self.unit)
            found[family.name] = book(total, quanta, books.counts[index], deficit, drift, pace, cold)
        return found

    count = credit.count_of

    def stepped(self, index: int, direction: int) -> tuple[list[records.Record], list[records.Booking]]:
        """Every record of a family stepped by Rule3 in `direction` with the rule of its own read (from the held rows' levels the step starts from, the Node's content and its six Links' contents, the Node's twice with each Link's own tension, every sign row but the record's own, the Links the world cuts at 0), every held row of the content among them, with or without a gap, the time line of the massless row reading its rest beyond every face, a turned record's planes under the rotation (`meeting.stepped`, `flux.step_records`), with one booking per record its form and its Wronskian are read from."""
        return meeting.stepped(self, index, direction)

    def record(self, index: int) -> list[records.Record]:
        """A family's record, the lines its share, its currents, its tension, its form and its Wronskian are read from: every line of a family of quanta (every record's), the time line of a held row of the content, and for a holder of the sign its light, the sum of its rows (`records.rows_total`); a turned record's plain lines (under the temporal gauge the time Link carries no phase, plane.step_plane)."""
        family, lines = self.families[index], self.states[index].lines
        if family.lorentz:  # the four lines, each summed over the rows: the covector (covector.weights)
            return covector.lines_total(family, lines)
        return [records.rows_total(family, lines)] if family.wronskian else lines[: family.record]

    def step(self, acts: bool = True) -> None:
        """One interval forward, each act one loop over the families or the node_detectors (ALGEBRA.md #the-interval), every act one Link's reach so that the whole interval's dependency radius is one Link (#the-paces, The Link's two ends, the local test): the receding faces grown where the front reaches them (`growth.grow`; at the largest size the run ends, named in `ended`, and no act is taken); the sign holder's phase act, each Link's pair iterated by the potential's difference across it read at the start (`phased`, features/phase), first, so that every reading of a turned record takes the Link pairs the step reads (2026-10-21; the act moves the phase lines alone and no level a plain reading takes, every plain record's readings bit for bit); then the bookings' read of every record of quanta (node_detector.weighed_currents) and from it the currents, with the turned records' sign currents and the tensions' parts, read from every record at the pair the step starts from (a turned record's currents the flux line's own with those pairs, read once per interval: board_readings.currents takes a turned family's from the bookings' read), and every family of quanta's paces, the write's rulers, from the held rows' levels at the start (`rulers`), the lines of the start kept for the parts' report; the turned records' sign currents under the Lorentz form the fluxes with the pairs the step reads (board_readings.sense_currents); the read and Rule3 on every line, the form D and the Wronskian W read about the step from its booking; the node_detectors' reports with the faces the step presented as `face` lines; the one write per held line from the bookings of the start; then the NodeDetectors' acts from outside the Node (`credit.counted_windows` with `meeting.closed` at the window's close, `meeting.jumped`, `emission.sourced`, `front.advanced_fronts`); last the observers, with the interval, the direction +1 and the pass. With `acts` False the step at the Nodes alone, the run forward of the meeting that runs back (`meeting_back.run_forward`): no report, no booking and no act of the NodeDetectors, the faces presented from the books' log as ever and the acts' lays of the interval re-applied from the books' log (`meeting_back.logged`), so that the board returns bit for bit the one the run forward had left; no output line."""
        if self.ended is not None:
            raise RuntimeError(f"the run ended at interval {self.interval}: {self.ended}")
        if not growth.grow(self):
            return
        self.interval, forms, turns = self.interval + 1, Bookings(), Bookings()
        node.phase_act(self.held, self.families, self.states, 1, self.wrap, self.world.node_clock)
        weighed = weighed_currents(self) if acts else {}
        currents, stresses = board_readings.currents(self, weighed), board_readings.stresses(self)
        rulers, begun = self.rulers(1), [s.lines for s in self.states]
        senses = board_readings.sense_currents(self)
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
        if acts:
            self.report(currents, weighed, forms, begun)
        for index in self.held:
            self.held_write(index, forms, turns, 1, stresses, senses, rulers, begun)
        if acts:
            self.tick += 1
            if credit.counted_windows(self):
                meeting.closed(self)
            meeting.jumped(self)
            emission.sourced(self)
            front.advanced_fronts(self)
        else:
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
        """The one write per line of one held family, forward or back (ALGEBRA.md #the-primitives, the row "the held write"; The write per proper volume and per proper interval): the numerators from the bookings of the families that source it, the Wronskians for the holder of the sign and the forms for a row sourced by the form, each scaled by the write's factor at the sourcing family's paces of the interval's start (`rulers`), and from their axis bookings at the interval's start, the tensions' parts read from the records for a row of the content, the shear's parts, the products of the Node's two axis differences, for a row declaring the shear, and the sign currents for the holder of the sign under the rotation (`records.write_sources`), each line's division at its wall with its one remainder (`node.held_write_at`, the Node knowing no line's kind). On a board periodic on every axis the write's mean over the Nodes has no sink and is carried by Rule3's own line at k = 0 (ALGEBRA.md, The closed lattice has no rest; item 6 of what is open; the world's `uniform: carried`, the law as written, or `interval: unobservable`, the hypothesis of 2026-10-22): the step's Links' sum over the torus vanishes at the vacuum's paces (every Link's difference counted once from each end) and the massless mass D is 0, so the mean level's second difference is the mean write per Node per interval, each Node's write dimmed by its own content factor as this one act applies it, the double root carrying the mean level and the mean velocity exactly in integers (a uniform level with the half wall steps to itself, a uniform velocity to itself); under `interval: unobservable` the massless row of the content carries its time line as the volume's level X = Gamma (Gamma / p_0)^(d + 1) (features/volume; the momentum hand's derivation M12a read cold by the reader), and its one write is the volume's, ((d + 1) X_now c + r) div (Gamma E_s T) at the one fixed wall, X_now the row's own level at the interval's start as the direction finds it (`begun` forward, the post-state's before back; records.write_sources `motion`), the chain rule between the level and the volume and no hill as an act (ALGEBRA.md, The uniform mode carried by Rule3's own k = 0 line; The mean's velocity is the content's; the owner's locality decision of 2026-10-22: the Node's own two numbers and nothing of the board); at the Node this write is the same division it has always been, fed by the same declared sources, and nothing here tests the board or the family (`uniform_mode` reads the mean, one division with one remainder, a lattice diagnostic)."""
        family, state = self.families[index], self.states[index]
        bookings, axes = turns if family.wronskian else forms, senses if family.rotation else stresses
        line, gamma = state.lines[0] if begun is None else begun[index][0], self.world.node_clock
        motion = (line.now, line.before) if family.motion_volume else None
        write, fixed = self.writes[index], self.fixed_walls.get(index)
        numerators, walls, _terms = records.write_sources(
            index, self.families, bookings, axes, write, rulers, gamma, motion, direction, fixed
        )
        state.lines, state.write_remainders = node.held_write_at(
            state.lines, numerators, walls, state.write_remainders, direction
        )
        for line in state.lines:
            self.bounded(family.name, line)

    def bounded(self, name: str, record: records.Record) -> None:
        """The amplitude bound A of the world: a level beyond it refuses the run by name."""
        if records.largest(record) > self.world.amplitude_bound:
            raise RuntimeError(
                f"the family {name!r} reached the level {records.largest(record)} at interval {self.interval}, above the world's amplitude bound A = {self.world.amplitude_bound}: the run is refused"
            )

    def declared_board(self) -> np.ndarray:
        """The declared board: the file's own Nodes over the lattice as grown, the layers a receding face has grown beyond them (what leaves into those layers has left the world, `growth`)."""
        found = np.zeros(self.shape, dtype=bool)
        found[tuple(slice(f, f + e) for f, e in zip(self.offset, self.world.shape, strict=True))] = True
        return found

    def report(
        self, currents: Currents, weighed: Weighed, forms: Bookings, begun: list[list[records.Record]]
    ) -> None:
        """The node_detectors' reports, the clicks (ALGEBRA.md #the-count-is-the-records-share; the owner's words, no click names a Node, the reader a declared NodeDetector): per family of quanta and reader (a reader's declared Nodes, the Nodes of the body it names derived now, the open faces' layer), one `click` line where it is not 0: the net plain current into the region through the NodeDetector's front boundary Ports at its Nodes this interval, in the current's units (the front: the Ports leading in from the declared board outside the declared NodeDetector, `declared_board`; not the Ports between two declared regions and not those toward a receding face's grown layers; the region's Nodes and its front read once per reader and interval, `reports.region_of`, `reports.front`, for every family), the density that entered from the declared board, the host's reading; never a Node (`reports.click`, the line labelled the measurement). The credit's book of a declared region, and a reader record's own (`node_detector.booked_inflows`), takes through the same front Ports the conserved form's own current, each record's current times its Link's factor Q_ij in the unit G^2 (`node_detector.weighed_currents`, `reports.weighted`, `credit.booked`; ALGEBRA.md #the-click-is-the-meeting, the credit's booking: the Link's factor squared the one weight, the plain current times G^2 where no tension stands). For a family of several parts (the pair family) or of several real lines (a record of dimension 3; `FamilyRule.several`), per declared region one `parts` line where a sum is not 0: the signed sums of each line's two levels over the region at the interval's start (`begun`, the lines the step started from), the NodeDetector's read the sides' books take for a record of several parts (`credit.moments_booked`) (ALGEBRA.md #the-click-is-the-meeting; `reports.level_sums`, `reports.parts`), and for a record of several real lines each line's share of the record, read as the squares of its sums over the sum of the squares; first the faces the click act presented at this interval's step, one `face` line each (`take.faces_reported`)."""
        take.faces_reported(self)
        own, union, wrap = self.declared_board(), node_detector_nodes(self), self.wrap
        where = [(d, reports.region_of(d, self.body_nodes)) for d in self.node_detectors]
        fronts = [(d, at, reports.front(at, wrap, union if d.declared else at, own)) for d, at in where]
        sums: dict[int, dict[str, list[list[int]]]] = {}
        for index, through in currents.items():
            family = self.families[index]
            for detector, nodes, facing in fronts:
                came = entering(facing, through)
                seen = int(came.sum(dtype=object))
                if seen != 0 and self.output is not None:
                    self.output(click(self.interval, family.name, detector.name, seen))
                if detector.declared:
                    credit.booked(self, index, detector.name, nodes, facing, weighed)
                if family.several and detector.declared:
                    levels = level_sums(nodes, begun[index])
                    if any(any(level) for level in levels) and self.output is not None:
                        self.output(parts(self.interval, family.name, detector.name, levels))
                    sums.setdefault(index, {})[detector.name] = levels
        for index, found in sums.items():  # the sides' own books of a record of several parts
            if self.families[index].parts > 1:
                credit.moments_booked(self, index, found)
        booked_inflows(self, weighed, wrap, own)
        board_readings.densities_read(self, forms, union)

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
        for record in quanta_records(self.families, index):
            own = record_lines(self.families, index, record, lines)
            stresses[(index, record)] = readings.axis_sources_of(
                family.pair[0], own, self.wrap, self.off_diagonals
            )
            if index in self.turning:
                senses[(index, record)] = board_readings.sense_fluxes(self, (index, record), own, -1)
        books[index] = lines

    def step_inverse(self) -> None:
        """One interval back, the same acts in reverse order with Rule3's direction -1 (ALGEBRA.md #the-direction): first the acts' lays of the interval undone from the books' log where the world's draw runs back (`meeting_back.logged`; where the books hold no log, a world with no record of several parts at declared sides, the host tool crosses them from the lines), then the write's rulers read from the held rows' levels at the interval's start, which the state after the interval still holds as their `before` (the write touched the level now alone), then a held family's write back once every family that sources it is booked back, a family of quanta booked back once its own write is off (the holder of the sign before the rows it sources), then every held row of the content stepped back, and last, every line standing at the previous interval's start again, the sign holder's phase lines back by the potentials read there (`phased` at -1, features/phase); the lay is not taken back; the observers called with the interval, the direction -1 and the pass; refused by name first on a world declaring `interval: unobservable` (`motion_back`)."""
        meeting_back.logged(self, -1)
        forms, turns, stresses, senses = Bookings(), Bookings(), Stresses(), Stresses()
        rulers = self.rulers(-1)  # the held rows' levels the interval started from, their `before`
        books: dict[int, list[records.Record]] = {}
        pending = list(self.held)
        while True:
            for index in self.order:
                if index not in books and (index not in self.held or index not in pending):
                    self.booked_back(index, books, forms, turns, stresses, senses)
            ready = [h for h in pending if all(i in books for i in readers_of(self.families, h))]
            if not pending:
                break
            assert ready, "the held rows' sources form a cycle"
            for held in ready:
                self.held_write(held, forms, turns, -1, stresses, senses, rulers)
            pending = [held for held in pending if held not in ready]
        for index in (held for held in self.held if held not in books):
            books[index] = self.stepped(index, -1)[0]
        for index, lines in books.items():
            self.states[index].lines = lines
        node.phase_act(self.held, self.families, self.states, -1, self.wrap, self.world.node_clock)
        self.interval, self.ended = self.interval - 1, None
        while self.growths and self.growths[-1][0] == self.interval + 1:
            growth.resize(self, *self.growths.pop()[1:], -1)
        self.passes, self.heading = self.passes + (self.heading > 0), -1
        for observer in self.observers:
            observer(self.interval, -1, self.passes)
