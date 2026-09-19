"""The engine of the law of events (events-v1): measured events, the events
in transit and the interval.

There is no shadow and no real; on the board there are only events (the
model owner, 2026-09-19, Highlights 5.4, "The law of events"). At every
interval every event is created at its next place from its record, and the
next place is one of seven: the six neighbours or here. An event in transit
is created at a neighbour, whole, by the sides' shares and its momentum; a
suspended event is created here for its count; a measured event is created
here without end, and its clock is the count of its self-creations. Nothing
is kept at a Node: no register, no remainder, no parked share, no draw.

A measured event (`Measured`): an amount per family, a momentum, a phase, a
number, a whole charge, a table, and its counts (its age, the self-creations
made; the intervals its exit is still suspended). The interval, in this
order:

1. every departure is created one Link on (`Transit.walk`), its record
   unchanged (an event in transit does not turn), the escapes booked;
2. at every Node the size of the coherent sum of each number's arrivals is
   formed; a measured event whose count is spent reads the sizes of the other
   numbers at its Node and is suspended for `suspension` intervals per whole
   unit read (`Measured.owed`, written when the count is spent, never
   accumulated); the events of a paid family that arrived this interval read
   the free families' sizes at their Node and carry the same count
   (`Transit.suspend`);
3. a measured event meets the events that arrive at its Node: its own
   number's are home, taken to be created again at its next self-creation,
   pushing nothing and not counted as content (the reading that keeps a
   content constant, Highlights 5.4, the law of the shadow, reading (i));
   another number's are met by its table, at a detector's Node only a
   bundle of one number at or above its threshold in one interval (a
   smaller one passes whatever the table says: no push, the units mix on;
   a release reads no threshold): `read` (the default for a free family:
   the push taken, the units left to mix on as at an empty Node), `measure`
   (the default for a paid family, the click: the push taken and the amount
   joining the content, one click per unit), `rerelease` (the push taken,
   the amount taken to be created again like what came home, with the
   measured event's number and phase) or `pass` (no push, the units mix
   on);
4. at every Node the arrivals of one number that are not suspended mix
   (node-mixing-v2): the sides' shares from the vectors, whole units placed
   by the largest remainder with the ties in the tick's Port order, a group
   with no whole for any side going whole by its momentum, the departures
   into flight; a suspended slot stays, its count paid by one;
5. a measured event whose count is spent is created here again: its age
   advances by one, and off its clock it releases, per free family it holds,
   content x the world's `release` per Port (`by_clock`: what the whole part
   of age x rate gained this self-creation, no remainder anywhere), a lamp
   its declared rate on its headings spending its content and taking the
   recoil, and what came home or is re-released on the six headings in equal
   whole shares, the units below six going whole to the heading its clock
   points at (the age modulo six), every release stamped with its number and
   phase and carrying its momentum from birth (the family's quantum times the
   amount, along the heading); its phase turns by its content over K off its
   clock; one whose count runs pays it by one and neither releases nor turns;
6. a measured event steps by its momentum off its clock: on an axis with
   momentum p and content M, one Link per (M + p) / p self-creations
   (`by_clock` with p over M + p), at most one step per interval, x before y
   before z, the momentum untouched; a step onto a measured event merges the
   two into the resident, a step off the board escapes; `fixed` never steps.

The push (Highlights 5.4, the law of events, the third law corrected): the
momentum an arriving group of a free family carries, from birth along its
release heading, pushes a measured event by -M c (gravity, toward the
emitter, the content M the cross-section) and by (q_A / M_A) q c (electricity,
the emitter's whole charge over its declared content times the measured
event's whole charge, the whole part off the clock, no remainder), and the
third law is the symmetry of the two fields; a group of a paid family pushes
by +c, its own momentum, and its emitter took the recoil. The books, per
family and interval: the measured line, initial + measured (home and the
clicks) = current + spent (the lamps) + escaped (measured events off the
board); the transit line, initial + released = current + escaped + absorbed
(home, the clicks, the re-releases), exact at every interval; the momentum
reported on the measured events, in transit and escaped.
"""

from __future__ import annotations

from collections.abc import Callable, Iterator
from dataclasses import dataclass, field

import numpy as np

from event_universe.core.lattice import PORT_HEADINGS, Address3
from event_universe.events.mixing import MIXING_AMPLITUDE_SCALE
from event_universe.events.transit import HEADINGS, Transit
from event_universe.events.world import EVENTS_LAW, EventWorld, MeasuredDefinition

Record = Callable[[dict[str, object]], None]
ZERO3 = (0, 0, 0)
RULES = ("home", "read", "measure", "rerelease")


def by_clock(age: int, numerator: int, denominator: int) -> int:
    """What the whole part of age x numerator / denominator gains at the
    self-creation that takes the age from `age` to `age + 1`: a rate read
    off the clock, exact on average, with no remainder kept anywhere. The
    engine calls it with the age before the self-creation."""
    return ((age + 1) * numerator) // denominator - (age * numerator) // denominator


@dataclass
class Measured:
    """A measured event at a Node."""

    number: int
    position: Address3
    family: int
    held: list[int]
    phase: int
    charge: int
    momentum: list[int]
    fixed: bool
    table: tuple[str, ...]
    lamp_rate: tuple[int, int] | None
    lamp_headings: tuple[int, ...]
    declared_content: int
    detector: int | None
    threshold: int
    # The clock (the self-creations made) and the suspension count.
    age: int = 0
    owed: int = 0
    # What came home or is re-released, per family: created again at the
    # next self-creation with this event's number and phase.
    home: list[int] = field(default_factory=list)
    # The counters: intervals suspended, phase steps made, steps walked, per
    # family what was met by each rule, the clicks and the push taken.
    waited: int = 0
    phase_steps: int = 0
    steps: int = 0
    measured: list[dict[str, int]] = field(default_factory=list)
    events: list[int] = field(default_factory=list)
    pushed: list[int] = field(default_factory=lambda: [0, 0, 0])

    @property
    def content(self) -> int:
        return sum(self.held)

    def state(self) -> dict[str, object]:
        return {
            "number": self.number,
            "position": list(self.position),
            "family": self.family,
            "held": list(self.held),
            "content": self.content,
            "phase": self.phase,
            "charge": self.charge,
            "momentum": list(self.momentum),
            "fixed": self.fixed,
            "detector": self.detector,
            "age": self.age,
            "owed": self.owed,
            "home": list(self.home),
            "waited": self.waited,
            "phase_steps": self.phase_steps,
            "steps": self.steps,
            "measured": [dict(entry) for entry in self.measured],
            "events": list(self.events),
            "pushed": list(self.pushed),
        }


class EventSimulation:
    """One world of the law of events, stepped interval by interval."""

    def __init__(self, world: EventWorld, observer: Record | None = None) -> None:
        self.world = world
        self.record = observer
        self.tick = 0
        self.shape = world.shape
        self.families = world.families
        count = len(world.families)
        self.transits = [
            Transit(index, world.shape, world.owners(index), world.phase_steps, world.clock)
            for index in range(count)
        ]
        self.denominator = world.content_lcm()
        self.measured: dict[int, Measured] = {}
        self.at: dict[Address3, int] = {}
        for index, definition in enumerate(world.measured):
            entry = self._measured(index + 1, definition)
            self.measured[entry.number] = entry
            self.at[entry.position] = entry.number
        # The books (cumulative): per family the measured line's initial,
        # measured in, spent and escaped; the transit line's initial, released
        # and absorbed; the momentum escaped with measured events.
        self.held_initial = [sum(m.held[f] for m in self.measured.values()) for f in range(count)]
        self.held_measured = [0] * count
        self.held_spent = [0] * count
        self.held_escaped = [0] * count
        self.transit_initial = [0] * count
        self.transit_released = [0] * count
        self.transit_absorbed = [0] * count
        self.momentum_escaped = [0, 0, 0]
        for item in world.in_transit:
            self._seed(item.position, item.family, item.number, item.port, item.amount, item.phase)
            self.transit_initial[item.family] += item.amount
        # The readings of the last interval (diagnostics): per family the
        # arrivals per Node, their net flow and the sizes per Node and number.
        self.count: list[np.ndarray] = [np.zeros(world.shape, dtype=np.int64) for _ in range(count)]
        self.per_port: list[np.ndarray] = [
            np.zeros((*world.shape, 6), dtype=np.int64) for _ in range(count)
        ]
        self.flow: list[np.ndarray] = [np.zeros((*world.shape, 3), dtype=np.int64) for _ in range(count)]
        self.size: list[np.ndarray] = [
            np.zeros((*world.shape, len(transit.owners)), dtype=np.int64) for transit in self.transits
        ]

    def _measured(self, number: int, definition: MeasuredDefinition) -> Measured:
        count = len(self.families)
        held = [0] * count
        held[definition.family] = definition.amount
        detector = self.world.detector_of(definition.position)
        threshold = 1 if detector is None else self.world.detectors[detector].threshold
        return Measured(
            number,
            definition.position,
            definition.family,
            held,
            definition.phase,
            definition.charge,
            list(definition.momentum),
            definition.fixed,
            definition.table,
            None if definition.lamp is None else definition.lamp.rate,
            () if definition.lamp is None else definition.lamp.headings,
            definition.amount,
            detector,
            threshold,
            home=[0] * count,
            measured=[{rule: 0 for rule in RULES} for _ in range(count)],
            events=[0] * count,
        )

    def _momentum(self, family: int, amount: int, port: int) -> np.ndarray:
        """The momentum a release carries from birth: the family's quantum
        times the amount, along the heading."""
        return np.array(PORT_HEADINGS[port], dtype=np.int64) * (self.families[family].quantum * amount)

    def _seed(
        self, position: Address3, family: int, number: int, port: int, amount: int, phase: int
    ) -> None:
        """An event in transit at the start: as an arrival at its Node on its
        travel heading, the arrivals of tick 0 that the first interval mixes."""
        transit = self.transits[family]
        cell = (*position, transit.rank[number], port)
        if transit.arr_amt[cell]:
            raise ValueError(f"{EVENTS_LAW}: two events in transit on one slot at the start")
        transit.arr_amt[cell] = amount
        transit.arr_ph[cell] = phase
        transit.arr_mom[cell] = self._momentum(family, amount, port)
        transit.fresh[cell[:4]] = True

    # -- the interval ----------------------------------------------------------

    def step(self) -> None:
        """One interval, in the order of the module docstring."""
        self.tick += 1
        world = self.world
        for transit in self.transits:
            transit.tick = self.tick
        arrived = [transit.walk() for transit in self.transits]
        # The readings: the sizes per Node and number, per family; the total
        # over families per number, over numbers per Node, and the free
        # families' total per Node (what a paid family's exit reads).
        numbers = len(world.measured)
        size_by_number = np.zeros((*self.shape, numbers + 1), dtype=np.int64)
        free_size = np.zeros(self.shape, dtype=np.int64)
        for index, transit in enumerate(self.transits):
            self.count[index] = transit.count()
            self.per_port[index] = transit.arr_amt.sum(axis=3)
            self.flow[index] = self.per_port[index] @ HEADINGS
            sizes = transit.sizes() if transit.owners else np.zeros((*self.shape, 0), dtype=np.int64)
            self.size[index] = sizes
            for rank, number in enumerate(transit.owners):
                size_by_number[..., number] += sizes[..., rank]
            if self.families[index].free:
                free_size += sizes.sum(axis=-1)
        size_total = size_by_number.sum(axis=-1)
        # The suspension of a paid family's events at the Nodes they reached.
        if world.suspension:
            for index, transit in enumerate(self.transits):
                if self.families[index].free or not transit.owners:
                    continue
                read = np.repeat(free_size[..., None], len(transit.owners), axis=-1)
                transit.suspend(read, world.suspension, arrived[index])
        # The events at the measured events and their suspension, then the mixing.
        for number in sorted(self.measured):
            entry = self.measured[number]
            self._suspend(entry, size_total, size_by_number)
            self._meet(entry)
        for transit in self.transits:
            transit.cycle()
        # The self-creations: the releases and the clocks; the steps last, in
        # number order.
        for number in sorted(self.measured):
            self._release(self.measured[number])
        for number in sorted(self.measured):
            if number in self.measured:
                self._move(self.measured[number])

    def _suspend(self, entry: Measured, size_total: np.ndarray, size_by_number: np.ndarray) -> None:
        width = self.world.suspension
        if not width or entry.owed > 0:
            return
        read = int(size_total[entry.position]) - int(size_by_number[(*entry.position, entry.number)])
        entry.owed = read * width // MIXING_AMPLITUDE_SCALE

    def _meet(self, entry: Measured) -> None:
        """The events at a measured event's Node: every arrival of its own
        number measured home, every other number's met by the table when the
        bundle reaches the detector's threshold (1 outside a detector: every
        response, read, measure or rerelease, is gated; a smaller bundle
        passes with no push and mixes on)."""
        position = entry.position
        for index, transit in enumerate(self.transits):
            if not transit.owners:
                continue
            rule = entry.table[index]
            free = self.families[index].free
            for rank, number in enumerate(transit.owners):
                cell = (*position, rank)
                if not transit.arr_amt[cell].any():
                    continue
                total = int(transit.arr_amt[cell].sum())
                if number == entry.number:
                    transit.take(position, rank)
                    entry.home[index] += total
                    entry.measured[index]["home"] += total
                    self.transit_absorbed[index] += total
                    self._event("home", entry, index, number, total, ZERO3)
                    continue
                if rule == "pass" or total < entry.threshold:
                    continue
                carried = [int(v) for v in transit.arr_mom[cell].sum(axis=0)]
                push = self._push(entry, free, number, carried)
                entry.momentum = [int(a) + int(b) for a, b in zip(entry.momentum, push, strict=True)]
                entry.pushed = [int(a) + int(b) for a, b in zip(entry.pushed, push, strict=True)]
                if rule == "read":
                    entry.measured[index]["read"] += total
                    self._event("read", entry, index, number, total, push)
                    continue
                transit.take(position, rank)
                self.transit_absorbed[index] += total
                entry.measured[index][rule] += total
                if rule == "measure":
                    entry.held[index] += total
                    entry.events[index] += total
                    self.held_measured[index] += total
                    self._event("click", entry, index, number, total, push)
                    continue
                entry.home[index] += total
                self._event("rerelease", entry, index, number, total, push)

    def _push(
        self, entry: Measured, free: bool, number: int, carried: list[int]
    ) -> tuple[int, int, int]:
        """The push of the units of one number arriving at a measured event:
        the gravity and the electric readings of the momentum they carry for a
        free family, the units' own momentum for a paid one."""
        if not free:
            return carried[0], carried[1], carried[2]
        content = entry.content
        push = [-carried[axis] * content for axis in range(3)]
        owner = self.world.measured[number - 1]
        if owner.charge and entry.charge:
            scale = owner.charge * entry.charge * (self.denominator // owner.amount)
            for axis in range(3):
                total = carried[axis] * scale
                whole = by_clock(entry.age, abs(total), self.denominator)
                push[axis] += -whole if total < 0 else whole
        return push[0], push[1], push[2]

    def _release(self, entry: Measured) -> None:
        """The self-creation of a measured event whose count is spent: its
        clock advances, its releases and its phase turn read off it."""
        if entry.owed > 0:
            entry.owed -= 1
            entry.waited += 1
            return
        age = entry.age
        entry.age += 1
        position = entry.position
        numerator, denominator = self.world.release
        for index, transit in enumerate(self.transits):
            if not transit.owners or entry.number not in transit.rank:
                continue
            own = transit.rank[entry.number]
            family = self.families[index]
            if family.free and entry.held[index] > 0:
                for port in range(6):
                    amount = by_clock(age, entry.held[index] * numerator, denominator)
                    if amount:
                        transit.place(
                            position, own, port, amount, entry.phase, self._momentum(index, amount, port)
                        )
                        self.transit_released[index] += amount
            if entry.home[index] > 0:
                # What came home or is re-released: equal whole shares on the
                # six headings, the units below six to the heading the clock
                # points at; the momentum fresh, the recoil for a paid family.
                share, left = divmod(entry.home[index], 6)
                entry.home[index] = 0
                for port in range(6):
                    amount = share + (left if port == age % 6 else 0)
                    if amount:
                        momentum = self._momentum(index, amount, port)
                        transit.place(position, own, port, amount, entry.phase, momentum)
                        self.transit_released[index] += amount
                        if not family.free:
                            entry.momentum = [
                                int(a) - int(b) for a, b in zip(entry.momentum, momentum, strict=True)
                            ]
            if entry.lamp_rate is not None and index == entry.family:
                rate_n, rate_d = entry.lamp_rate
                for port in entry.lamp_headings:
                    amount = min(by_clock(age, rate_n, rate_d), entry.held[index])
                    if amount:
                        momentum = self._momentum(index, amount, port)
                        transit.place(position, own, port, amount, entry.phase, momentum)
                        entry.held[index] -= amount
                        entry.momentum = [
                            int(a) - int(b) for a, b in zip(entry.momentum, momentum, strict=True)
                        ]
                        self.transit_released[index] += amount
                        self.held_spent[index] += amount
        steps = by_clock(age, entry.content, self.world.clock)
        if 2 * steps >= self.world.phase_steps:
            raise ValueError(
                f"{EVENTS_LAW}: measured event {entry.number} turns its phase by half the circle or "
                "more per self-creation (its content has grown past K x N / 2)"
            )
        entry.phase = (entry.phase + steps) & self.world.phase_mask
        entry.phase_steps += steps

    def _move(self, entry: Measured) -> None:
        """The step by the momentum off the clock, at most one per interval."""
        if entry.fixed or entry.owed > 0:
            return
        content = entry.content
        if content <= 0:
            return
        for axis in range(3):
            momentum = entry.momentum[axis]
            if momentum == 0:
                continue
            magnitude = abs(momentum)
            if not by_clock(entry.age - 1, magnitude, content + magnitude):
                continue
            sign = 1 if momentum > 0 else -1
            entry.steps += 1
            target = list(entry.position)
            target[axis] += sign
            origin = entry.position
            del self.at[origin]
            if not 0 <= target[axis] < self.shape[axis]:
                for index in range(len(self.families)):
                    self.held_escaped[index] += entry.held[index]
                    self.transit_absorbed[index] -= entry.home[index]
                    self.transits[index].escaped += entry.home[index]
                self.momentum_escaped = [
                    int(a) + int(b) for a, b in zip(self.momentum_escaped, entry.momentum, strict=True)
                ]
                del self.measured[entry.number]
                self._event("escaped", entry, entry.family, entry.number, content, ZERO3)
                return
            destination: Address3 = (target[0], target[1], target[2])
            if destination in self.at:
                other = self.measured[self.at[destination]]
                for index in range(len(self.families)):
                    other.held[index] += entry.held[index]
                    other.home[index] += entry.home[index]
                other.momentum = [
                    int(a) + int(b) for a, b in zip(other.momentum, entry.momentum, strict=True)
                ]
                other.charge += entry.charge
                del self.measured[entry.number]
                self._event("merged", entry, entry.family, other.number, content, ZERO3)
                return
            entry.position = destination
            self.at[destination] = entry.number
            if self.record is not None:
                self.record(
                    {
                        "event": "step",
                        "tick": self.tick,
                        "number": entry.number,
                        "node": list(origin),
                        "to": list(destination),
                        "momentum": list(entry.momentum),
                    }
                )
            return

    def _event(
        self,
        kind: str,
        entry: Measured,
        family: int,
        number: int,
        amount: int,
        push: tuple[int, int, int],
    ) -> None:
        if self.record is None:
            return
        self.record(
            {
                "event": kind,
                "tick": self.tick,
                "node": list(entry.position),
                "measured": entry.number,
                "detector": None
                if entry.detector is None
                else self.world.detectors[entry.detector].name,
                "family": self.families[family].name,
                "number": number,
                "amount": amount,
                "push": list(push),
            }
        )

    # -- the books -------------------------------------------------------------

    def books(self) -> dict[str, object]:
        """The ledger at the current tick, every line with its identity."""
        families: dict[str, object] = {}
        balanced = True
        for index, family in enumerate(self.families):
            transit = self.transits[index]
            measured = {
                "initial": self.held_initial[index],
                "measured": self.held_measured[index],
                "current": sum(entry.held[index] for entry in self.measured.values()),
                "spent": self.held_spent[index],
                "escaped": self.held_escaped[index],
            }
            measured["balanced"] = measured["initial"] + measured["measured"] == (
                measured["current"] + measured["spent"] + measured["escaped"]
            )
            in_transit = {
                "initial": self.transit_initial[index],
                "released": self.transit_released[index],
                "current": transit.current(),
                "escaped": transit.escaped,
                "absorbed": self.transit_absorbed[index],
            }
            in_transit["balanced"] = in_transit["initial"] + in_transit["released"] == (
                in_transit["current"] + in_transit["escaped"] + in_transit["absorbed"]
            )
            balanced = balanced and bool(measured["balanced"]) and bool(in_transit["balanced"])
            families[family.name] = {"measured": measured, "transit": in_transit}
        held_momentum = [0, 0, 0]
        for entry in self.measured.values():
            held_momentum = [a + b for a, b in zip(held_momentum, entry.momentum, strict=True)]
        carried = np.zeros(3, dtype=np.int64)
        escaped = np.array(self.momentum_escaped, dtype=np.int64)
        for transit in self.transits:
            carried += transit.carried()
            escaped += transit.escaped_momentum
        return {
            "tick": self.tick,
            "families": families,
            "momentum": {
                "measured": held_momentum,
                "transit": [int(v) for v in carried],
                "escaped": [int(v) for v in escaped],
            },
            "charge": sum(entry.charge for entry in self.measured.values()),
            "balanced": balanced,
        }

    def contents(self) -> list[dict[str, object]]:
        return [self.measured[number].state() for number in sorted(self.measured)]

    def home_pending(self, index: int) -> int:
        """What came home or is re-released and waits for its self-creation,
        on the transit's absorbed line until then."""
        return sum(entry.home[index] for entry in self.measured.values())

    def detectors(self) -> list[dict[str, object]]:
        """The measurements per detector: its Nodes, its threshold and per
        family the amount measured and the clicks."""
        found = []
        for index, detector in enumerate(self.world.detectors):
            members = [entry for entry in self.measured.values() if entry.detector == index]
            families = {
                family.name: {
                    "measured": sum(entry.measured[f]["measure"] for entry in members),
                    "clicks": sum(entry.events[f] for entry in members),
                }
                for f, family in enumerate(self.families)
            }
            found.append(
                {
                    "name": detector.name,
                    "nodes": len(detector.positions),
                    "threshold": detector.threshold,
                    "families": families,
                }
            )
        return found

    def shell_readings(self, family: int, centre: Address3, radius: int) -> dict[str, float]:
        """The shell means at one radius of the last interval's readings: the
        Nodes at Euclidean distance within a half Link of `radius` from the
        centre, their number, the mean count (the amount that arrived per
        Node), the mean radial flow (amount x heading projected on the radial
        unit vector, summed per Node) and the mean size in units^(1/2) (the
        32nds over 32), every number summed."""
        grid = np.indices(self.shape).reshape(3, -1).T - np.array(centre)
        distance = np.sqrt((grid * grid).sum(axis=1))
        chosen = np.abs(distance - radius) < 0.5
        chosen &= distance > 0
        positions = grid[chosen]
        radial = positions / distance[chosen][:, None]
        cells = tuple((positions + np.array(centre)).T)
        count = self.count[family][cells]
        flow = self.flow[family][cells]
        size = self.size[family][cells].sum(axis=-1)
        return {
            "nodes": float(chosen.sum()),
            "count": float(count.mean()),
            "flow": float((flow * radial).sum(axis=1).mean()),
            "size": float(size.mean()) / MIXING_AMPLITUDE_SCALE,
        }

    def cube_flux(self, family: int, centre: Address3, half: int) -> int:
        """The net outward flow through the closed surface between the cube of
        half-width `half` about the centre and its neighbours, this interval:
        the amount that arrived just outside each face moving outward less the
        amount that arrived on the face moving inward, Gauss's flux."""
        per_port = self.per_port[family]
        total = 0
        for axis in range(3):
            for sign in (1, -1):
                face = centre[axis] + sign * half
                outside = face + sign
                if not 0 <= outside < self.shape[axis]:
                    continue
                lows = [max(0, centre[a] - half) for a in range(3)]
                highs = [min(self.shape[a], centre[a] + half + 1) for a in range(3)]
                slices = [slice(lows[a], highs[a]) for a in range(3)]
                outward = 2 * axis + (0 if sign > 0 else 1)
                inward = outward ^ 1
                slices[axis] = slice(outside, outside + 1)
                total += int(per_port[tuple(slices)][..., outward].sum())
                slices[axis] = slice(face, face + 1)
                total -= int(per_port[tuple(slices)][..., inward].sum())
        return total

    # -- the snapshot ----------------------------------------------------------

    def snapshot_stream(self) -> Iterator[tuple[str, object]]:
        """The snapshot as (key, value) pairs, the Nodes with events in transit
        as an iterator over one entry at a time (`snapshot_writer`)."""
        yield "law", EVENTS_LAW
        yield "tick", self.tick
        yield "shape", list(self.shape)
        yield "boundary", "open"
        yield "measured", self.contents()
        yield "detectors", self.detectors()
        yield (
            "escaped",
            [
                {"family": family.name, "amount": transit.escaped}
                for family, transit in zip(self.families, self.transits, strict=True)
            ],
        )
        yield "nodes", self._node_entries()

    def snapshot(self) -> dict[str, object]:
        return {
            key: (list(value) if isinstance(value, Iterator) else value)
            for key, value in self.snapshot_stream()
        }

    def _node_entries(self) -> Iterator[dict[str, object]]:
        present = np.zeros(self.shape, dtype=bool)
        for transit in self.transits:
            if transit.owners:
                present |= transit.arr_amt.any(axis=(3, 4)) | transit.fly_amt.any(axis=(3, 4))
        for x, y, z in zip(*np.nonzero(present), strict=True):
            position = (int(x), int(y), int(z))
            entry: dict[str, object] = {"position": list(position), "families": []}
            families = entry["families"]
            assert isinstance(families, list)
            for family, transit in zip(self.families, self.transits, strict=True):
                if not transit.owners:
                    continue
                arrivals = []
                departures = []
                for rank, number in enumerate(transit.owners):
                    for port in range(6):
                        cell = (*position, rank, port)
                        if transit.arr_amt[cell]:
                            arrivals.append(
                                {
                                    "number": number,
                                    "heading": list(PORT_HEADINGS[port]),
                                    "amount": int(transit.arr_amt[cell]),
                                    "phase": int(transit.arr_ph[cell]),
                                    "momentum": [int(v) for v in transit.arr_mom[cell]],
                                    "suspended": int(transit.suspended[(*position, rank)]),
                                }
                            )
                        if transit.fly_amt[cell]:
                            departures.append(
                                {
                                    "number": number,
                                    "heading": list(PORT_HEADINGS[port]),
                                    "amount": int(transit.fly_amt[cell]),
                                    "phase": int(transit.fly_ph[cell]),
                                    "momentum": [int(v) for v in transit.fly_mom[cell]],
                                }
                            )
                if arrivals or departures:
                    families.append(
                        {"family": family.name, "arrivals": arrivals, "departures": departures}
                    )
            yield entry
