"""The GameBoard: every family's NodeState over the Nodes (node.py), the bodies' ledgers and the detectors, stepped one interval at a time in the law's order (ALGEBRA.md #the-interval): the signed read, Rule3 on every level, the count's line with the reports, the hold, then the bodies' clocks and the givings at their clicks; `step_inverse` runs the same acts back. A body is a ledger and no state of the law: its family, its Nodes (where its family's count stands), its clock; a detector is a Node told to report; only a detector's report is a measurement, every other reading is a GameBoard diagnostic."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass, replace

import numpy as np

from event_universe import node
from event_universe.core.ports import arrival
from event_universe.features.start import rest
from event_universe.features.write import carried
from event_universe.loader.world import FACE_NAME, Node, World

Observer = Callable[[dict[str, object]], None]


@dataclass
class Body:
    """A body's ledger: its number, its family, its Nodes (a mask over the GameBoard), its declared count and its clock's last total."""

    number: int
    family: int
    nodes: np.ndarray
    declared: int
    total: int

    def corner(self) -> list[int]:
        """The lower corner of the body's Nodes, the Node its click names."""
        return [int(low) for low in np.argwhere(self.nodes).min(axis=0)]


@dataclass(frozen=True)
class Detector:
    """A detector: its name, its fixed Nodes (None: the Nodes of its body each interval) and the body it names."""

    name: str
    nodes: np.ndarray | None
    body: int | None


def as_node(found: np.ndarray) -> Node:
    """A Node's address from an index row."""
    return int(found[0]), int(found[1]), int(found[2])


class GameBoard:
    """One world on the GameBoard, stepped interval by interval; `observer` receives the output lines `click`, `giving`, `gather` and `block`."""

    def __init__(self, world: World, observer: Observer | None = None) -> None:
        self.world, self.observer, self.tick = world, observer, 0
        self.shape, self.wrap = world.shape, world.periodic
        self.families = world.families
        self.states = [node.empty_state(family, self.shape) for family in self.families]
        count = len(self.families)
        self.laid_total, self.given, self.taken, self.reports = (
            [0] * count,
            [0] * count,
            [0] * count,
            [0] * count,
        )
        self.bodies: list[Body] = []
        for number, row in enumerate(world.bodies):
            state = self.states[row.family]
            assert state.levels is not None
            now = np.array(row.now, dtype=np.int64).reshape(self.shape)
            before = np.array(row.before, dtype=np.int64).reshape(self.shape)
            state.levels = replace(
                state.levels, now=state.levels.now + now, before=state.levels.before + before
            )
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

    def mask(self, nodes: tuple[Node, ...]) -> np.ndarray:
        """The mask of a set of Nodes."""
        found = np.zeros(self.shape, dtype=bool)
        found[tuple(np.array(nodes).T)] = True
        return found

    def start(self) -> None:
        """THE START (ALGEBRA.md #the-generator (g), the start): every held family's time part at the rest of its line under the bodies' declared counts at the weight with which the body's family reads it, over its divisor (features/start), both levels, the remainder at the half wall and the hold's carry E_s div 2 at the sources' Nodes."""
        for index, family in enumerate(self.families):
            if family.held is None or family.divisor is None:
                continue
            counts = node.zeros(self.shape)
            for row in self.world.bodies:
                weight = node.weight_of(index, self.families[row.family])
                for at, value in zip(row.nodes, row.counts, strict=True):
                    counts[at] += weight * value
            if not counts.any():
                continue
            try:
                field = rest(counts, family.pair, self.wrap, family.divisor, self.world.width)
            except ValueError as refusal:
                raise ValueError(f"the start of the held family {family.name!r}: {refusal}") from refusal
            state = self.states[index]
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
        """THE BOOKS per family of quanta (a GameBoard diagnostic): the count's sum, the remainders' sum, SUM (W_c c + r) against its laid value moved by the givings alone (the line conserves it to the bit), the quanta given and taken at the clicks, and the reports."""
        found: dict[str, dict[str, int | bool]] = {}
        for index, (family, state) in enumerate(zip(self.families, self.states, strict=True)):
            if state.count is None or state.count_remainder is None:
                continue
            wall = node.count_wall(family, self.world.quantum_action)
            total = int((wall * state.count.astype(object) + state.count_remainder).sum())
            moved = self.laid_total[index] + wall * (self.taken[index] - self.given[index])
            found[family.name] = {
                "count": int(state.count.sum()),
                "remainders": int(state.count_remainder.sum(dtype=object)),
                "total": total,
                "given": self.given[index],
                "taken": self.taken[index],
                "reports": self.reports[index],
                "balanced": total == moved,
            }
        return found

    def reads(self, level: str) -> dict[int, tuple[np.ndarray, tuple[np.ndarray, ...]]]:
        """The signed read of every family of quanta from the held parts' `level`."""
        return {
            index: node.signed_read(
                index, self.families, self.states, self.world.node_clock, level, self.tick, self.shape
            )
            for index, family in enumerate(self.families)
            if family.quanta
        }

    def step(self) -> None:
        """One interval forward, the five acts each one loop over the families or the bodies and detectors (ALGEBRA.md #the-interval): the signed read, Rule3 on the levels with the wells, the count's line (laid at the first act) with the bodies' Nodes and the reports, the held families' parts and hold, the clocks and the givings."""
        self.tick += 1
        action, wrap = self.world.quantum_action, self.wrap
        read = self.reads("now")
        wells: dict[int, np.ndarray] = {}
        for index, (content, axis) in read.items():
            family, state = self.families[index], self.states[index]
            assert state.levels is not None and state.well_remainder is not None
            rule = node.quanta_rule(family, self.world.node_clock, content, axis)
            after = node.step(state.levels, rule, wrap)
            self.bounded(family.name, after)
            wells[index], state.well_remainder = node.well(
                state.levels, after, state.well_remainder, action
            )
            state.levels = after
        if all(self.states[index].count is None for index in read):
            self.lay()
        rises = {}
        for index in read:
            family, state = self.families[index], self.states[index]
            before = state.count
            writes = node.count_line(family, state, action, self.world.amplitude_bound, wrap)
            state.count, state.count_remainder = np.asarray(writes.count), np.asarray(writes.remainder)
            rises[index] = state.count - np.asarray(before)
        for body in self.bodies:
            self.follow(body)
        self.report(rises)
        for index, family in enumerate(self.families):
            if family.held is not None:
                state = self.states[index]
                source = node.source(index, self.families, wells, self.shape)
                state.parts, state.carry = node.held_step(family, state, source, wrap)
                for part in state.parts:
                    self.bounded(family.name, part)
        for body in self.bodies:
            self.clock(body)

    def bounded(self, name: str, record: node.Record) -> None:
        """The amplitude bound A of the world: a level beyond it refuses the run by name."""
        if node.largest(record) > self.world.amplitude_bound:
            raise RuntimeError(
                f"the family {name!r} reached the level {node.largest(record)} at interval {self.tick}, above "
                f"the world's amplitude bound A = {self.world.amplitude_bound}: the run is refused"
            )

    def lay(self) -> None:
        """THE LAY at the first act (ALGEBRA.md #the-counts-line): every family's count from its levels, the quanta the bodies hold of other families added at their Nodes, and the gate: a body's declared count within 2 isqrt(c) + 1 of the count laid at its Nodes, refused by name beyond it."""
        for index, family in enumerate(self.families):
            state = self.states[index]
            if state.levels is not None:
                state.count, state.count_remainder = node.lay(
                    family, state.levels, self.world.quantum_action, self.wrap
                )
        for body, row in zip(self.bodies, self.world.bodies, strict=True):
            for other, counts in row.holds:
                held = self.states[other].count
                assert held is not None
                for at, value in zip(row.nodes, counts, strict=True):
                    held[at] += value
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
        for index, (family, state) in enumerate(zip(self.families, self.states, strict=True)):
            if state.count is not None and state.count_remainder is not None:
                wall = node.count_wall(family, self.world.quantum_action)
                self.laid_total[index] = int(
                    (wall * state.count.astype(object) + state.count_remainder).sum()
                )

    def follow(self, body: Body) -> None:
        """THE BODY'S NODES ARE WHERE ITS COUNT STANDS (ALGEBRA.md #what-a-body-is (c)): within one Link of its Nodes, the Nodes where its family's count is not 0; the line alone moves them."""
        count = self.states[body.family].count
        assert count is not None
        region = body.nodes.copy()
        for axis in range(3):
            for side in (1, -1):
                region |= arrival(body.nodes, axis, side, self.wrap[axis], False)
        standing = region & (count != 0)
        if bool(standing.any()):
            body.nodes = standing

    def shell(self, body: Body) -> np.ndarray:
        """The body's shell: its Nodes with a Port to a Node outside it (none beyond an open face; a folded axis carries none)."""
        found = np.zeros(self.shape, dtype=bool)
        for axis in range(3):
            for side in (1, -1):
                found |= body.nodes & ~arrival(body.nodes, axis, side, self.wrap[axis], True)
        return found

    def report(self, rises: dict[int, np.ndarray]) -> None:
        """THE REPORT, a reading of the count's line (ALGEBRA.md #the-counts-line: the count that arrives at a detector's Node is the detector's click): per family and per detector (a detector's Nodes, the Nodes of the body it names, the open faces' layer) the rise of the family's count summed over the detector's Nodes by the line this interval, the net inflow across its boundary (a move between its own Nodes cancels), one `gather` line per unit of rise with the detector's count after; nothing is handed over."""
        for index, rise in rises.items():
            count = self.states[index].count
            assert count is not None
            for detector in self.detectors:
                nodes = self.bodies[detector.body].nodes if detector.body is not None else detector.nodes
                assert nodes is not None
                arrived, held = int(rise[nodes].sum()), int(count[nodes].sum())
                for _ in range(max(arrived, 0)):
                    self.reports[index] += 1
                    self.emit(
                        {
                            "event": "gather",
                            "tick": self.tick,
                            "family": self.families[index].name,
                            "detector": detector.name,
                            "count": held,
                            "taker": detector.body,
                        }
                    )

    def clock(self, body: Body) -> None:
        """The body's clock (a GameBoard reading): a crossing of its total from at most 0 to above 0 is its click, and at its click the body gives."""
        total = self.clock_total(body)
        if body.total <= 0 < total:
            family = self.families[body.family]
            self.emit(
                {
                    "event": "click",
                    "tick": self.tick,
                    "measured": body.number,
                    "family": family.name,
                    "node": body.corner(),
                }
            )
            if family.gives is not None:
                self.give(body, family.gives)
        body.total = total
        self.emit(
            {
                "event": "block",
                "tick": self.tick,
                "measured": body.number,
                "corner": body.corner(),
                "sum": total,
            }
        )

    def give(self, body: Body, given: int) -> None:
        """THE GIVING at the body's click (ALGEBRA.md #the-primitives, the row "the giving"; #the-counts-line, the lay and the wall): the quantum leaves through an outer Port, so from the shell Node where its family's count stands highest (ties in x-major order), and only where that count is at least 1: its family's count there -1 and the given family's +1 (the conversion changes the family), and the given family's two levels at that Node gain the body's family's two levels there scaled so that the form the write adds lays exactly one count over the board (node.one_quantum), the count the record's form (a write at the whole shell of a symmetric body lays 0 or 2, never 1)."""
        shell = self.shell(body)
        own, other = self.states[body.family], self.states[given]
        assert own.count is not None and other.count is not None
        assert own.levels is not None and other.levels is not None
        standing = np.where(shell, own.count, 0)
        at = as_node(np.array(np.unravel_index(int(np.argmax(standing)), self.shape)))
        if not bool(shell.any()) or int(standing[at]) < 1:
            return
        port = np.zeros(self.shape, dtype=bool)
        port[at] = True
        written = node.one_quantum(
            self.families[given],
            (np.where(port, own.levels.now, 0), np.where(port, own.levels.before, 0)),
            self.world.quantum_action,
            self.wrap,
            self.world.amplitude_bound,
            f"the giving of measured[{body.number}] at interval {self.tick}",
        )
        own.count[at] -= 1
        other.count[at] += 1
        self.given[body.family] += 1
        self.taken[given] += 1
        now, before = (carried(level, 1, 0)[0] for level in written)
        other.levels = replace(
            other.levels, now=other.levels.now + now, before=other.levels.before + before
        )
        self.emit(
            {
                "event": "giving",
                "tick": self.tick,
                "measured": body.number,
                "family": self.families[given].name,
                "node": list(at),
                "count": int(own.count[body.nodes].sum()),
            }
        )

    def step_inverse(self) -> None:
        """One interval back, the same loops in reverse order with Rule3's direction -1 (ALGEBRA.md #the-direction, #the-counts-line): the held families' hold and parts back (the wells recomputed from the levels stepped back), the count's line back, the levels back; the givings, the bodies' Nodes and the lay are not taken back."""
        action, wrap = self.world.quantum_action, self.wrap
        backs, wells, starts = {}, {}, {}
        for index, (content, axis) in self.reads("before").items():
            family, state = self.families[index], self.states[index]
            assert state.levels is not None and state.well_remainder is not None
            rule = node.quanta_rule(family, self.world.node_clock, content, axis)
            backs[index] = node.step(state.levels, rule, wrap, -1)
            wells[index], starts[index] = node.well(
                backs[index], state.levels, state.well_remainder, action, -1
            )
        for index, family in enumerate(self.families):
            if family.held is not None:
                state = self.states[index]
                source = node.source(index, self.families, wells, self.shape)
                state.parts, state.carry = node.held_step(family, state, source, wrap, -1)
        for index, back in backs.items():
            family, state = self.families[index], self.states[index]
            if state.count is not None:
                writes = node.count_line(family, state, action, self.world.amplitude_bound, wrap, -1)
                state.count, state.count_remainder = (
                    np.asarray(writes.count),
                    np.asarray(writes.remainder),
                )
            state.levels, state.well_remainder = back, starts[index]
        for body in self.bodies:
            body.total = self.clock_total(body)
        self.tick -= 1
