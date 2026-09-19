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
made; the count it still owes before its next self-creation). The interval,
in this order:

1. every departure is created one Link on (`Transit.walk`), its record
   unchanged (an event in transit does not turn), the escapes through the
   open faces booked; on an axis the world declares periodic the departures
   through one face are created at the first Node of the opposite face and
   nothing escapes on that axis;
2. at every Node the presence of each number is formed, the amount that
   arrived there this interval, over every family (and, a reading, the size
   of the coherent sum, `Transit.sizes`); the events of a paid family that
   arrived this interval read the presence at their Node of every number but
   their own and carry the count `presence x n // d` at the world's
   `suspension` `[n, d]` (`Transit.suspend`), the same read a measured event
   makes at its self-creation (step 5);
3. a measured event meets the events that arrive at its Node: its own
   number's are home, taken to be created again at its next self-creation,
   pushing nothing and not counted as content (the reading that keeps a
   content constant, Highlights 5.4, the law of the shadow, reading (i));
   another number's are met by its table, at a detector's Node only a
   bundle of one number at or above its threshold in one interval (a
   smaller one passes whatever the table says: no push, the units mix on;
   a release reads no threshold) and, where the entry declares a
   `phase_window`, only a bundle whose phase at the Node (the nearest step
   of the coherent sum of its arrivals, `Transit.phase_at`) falls in the
   half circle centred on the setting (`in_window`; a bundle outside it
   passes, no push, the units mix on, a `pass` record written): `read`
   (the default for a free family: the push taken, the units left to mix on
   as at an empty Node), `measure` (the default for a paid family, the
   click: the push taken and the amount joining the content, one click per
   unit), `rerelease` (the push taken, the amount taken to be created again
   like what came home, with the measured event's number and phase) or
   `pass` (no push, the units mix on);
4. at every Node the arrivals of a family that are not suspended mix
   (node-mixing-v3): the sides' shares from the vectors of every number
   present, the weights common to the numbers at the Node, whole units
   placed per number by the largest remainder with the ties in the tick's
   Port order, a number with no whole for any side going whole by its own
   momentum, the departures into flight; for a family without a phase
   circle (`"phase": false`) each Port's arrival scatters on its own, four
   ninths back and one ninth each other way (`scatter_arrivals`), no sum
   over the numbers; a suspended slot stays, its count paid by one;
5. a measured event that owes a count pays it by one and is created here
   without a self-creation: no release, no turn (`waited` counts these
   intervals; age + waited is the intervals completed). One that owes
   nothing is created here again, the self-creation: its age
   advances by one, and off its clock it releases, per free family it holds,
   content x the world's `release` per Port (`by_clock`: what the whole part
   of age x rate gained this self-creation, no remainder anywhere), a lamp
   its declared rate on its headings spending its content and taking the
   recoil, and what came home or is re-released on the six headings in equal
   whole shares, the units below six going whole to the heading its clock
   points at (the age modulo six), every release stamped with its number and
   phase and carrying its momentum from birth (the family's quantum times the
   amount, along the heading); a lamp with a `phase_window` releases only at
   the self-creations whose clock phase, the one its release is stamped
   with, falls in its window; its phase turns by its content over K off its
   clock at every self-creation, released or not (a measured event of a
   family without a phase circle never turns). After its self-creation it
   reads the presence at its Node of every number but its own, this
   interval's (step 2), and owes `presence x n // d` intervals at the
   world's `suspension` `[n, d]` (`Measured.owed`, written once per
   self-creation, never accumulated), paid before its next self-creation:
   in a steady presence that reads k it is created again once every k + 1
   intervals, its clock slowed by 1 / (k + 1) and never stopped (the
   redshift). The read follows the
   self-creation and never precedes it: a read before it, of the same steady
   size, would owe the count again every time it was spent and the clock
   would never tick (the order of the first `events-v1`, corrected on
   2026-09-19, docs/MIGRATION.md);
6. a measured event steps by its momentum off its clock when it owes
   nothing: in the interval of its self-creation when that read no count,
   else in the interval the last unit of its count is paid, so a suspended
   event is created here for its count and each self-creation's step is
   read once; on an axis with
   momentum p and content M, one Link per (M + p) / p self-creations
   (`by_clock` with p over M + p), at most one step per interval, x before y
   before z, the momentum untouched; a step onto a measured event merges the
   two into the resident, a step off the board through an open face escapes,
   and on a periodic axis the step wraps as the departures do (from the last
   Node along +axis to the first, from the first along -axis to the last;
   with an extent of 1 it lands on its own Node, no move and no merge, the
   step counted in `steps` as every step off the clock is); `fixed` never
   steps.

The push (Highlights 5.4, the law of events, the third law corrected; the
model owner, 2026-09-19, the push as the net flow): the net flow c of the
units of one number of a free family arriving at a measured event, the sum
over the six Ports of amount times travel heading (what `Transit.flow` sums
per Node), pushes it by -M c (gravity, toward the emitter, the content M the
cross-section) and by (q_A / M_A) q c (electricity, the emitter's whole
charge over its declared content times the measured event's whole charge,
the whole part off the clock, no remainder), and the third law is the
symmetry of the two fields; the momentum the units carry from birth stays on
their record and in the books, unread by the push. A group of a paid family
pushes by +c, its own carried momentum, and its emitter took the recoil
(light's pressure). The books, per
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

from event_universe.core.integer import checked_work
from event_universe.core.lattice import PORT_HEADINGS, Address3, adjacent_node
from event_universe.events.mixing import MIXING_AMPLITUDE_SCALE
from event_universe.events.reversible import (
    STATE_BOUND,
    CarrierState,
    ContactState,
    canonical_momentum,
    clock_step,
    pointer_displacement,
    transduce,
    validate_carrier,
    validate_material,
)
from event_universe.events.transit import HEADINGS, Transit
from event_universe.events.world import (
    EVENTS_LAW,
    REVERSIBLE_DETECTOR_DYNAMICS,
    DetectorGroupDefinition,
    EventWorld,
    MeasuredDefinition,
)

Record = Callable[[dict[str, object]], None]
ZERO3 = (0, 0, 0)
RULES = ("home", "read", "measure", "rerelease")


def by_clock(age: int, numerator: int, denominator: int) -> int:
    """What the whole part of age x numerator / denominator gains at the
    self-creation that takes the age from `age` to `age + 1`: a rate read
    off the clock, exact on average, with no remainder kept anywhere. The
    engine calls it with the age before the self-creation."""
    return ((age + 1) * numerator) // denominator - (age * numerator) // denominator


def in_window(phase: int, setting: int, modulus: int) -> bool:
    """Whether a phase falls in the phase window of a setting (Highlights
    5.4, "the phase window as a declared width of a detector, and of the
    emitter too"): the half circle centred on the setting, with
    d = (phase - setting) mod N, d < N / 4 or d >= 3 N / 4, exactly N / 2
    of the N steps; for N = 2 the one step d = 0. Integer arithmetic on N."""
    distance = (phase - setting) % modulus
    return 4 * distance < modulus or 4 * distance >= 3 * modulus


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
    # The phase window of each table entry, None without one.
    windows: list[int | None]
    lamp_rate: tuple[int, int] | None
    lamp_headings: tuple[int, ...]
    lamp_window: int | None
    declared_content: int
    detector: int | None
    threshold: int
    # The clock (the self-creations made) and the count owed: read after a
    # self-creation, paid one per interval before the next.
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
            "windows": list(self.windows),
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
            Transit(
                index,
                world.shape,
                world.owners(index),
                world.phase_steps,
                world.clock,
                exact_transport=world.dynamics == REVERSIBLE_DETECTOR_DYNAMICS,
                periodic=world.periodic,
                phased=family.phase,
            )
            for index, family in enumerate(world.families)
        ]
        self.denominator = world.content_lcm()
        self.measured: dict[int, Measured] = {}
        self.at: dict[Address3, int] = {}
        for index, definition in enumerate(world.measured):
            entry = self._measured(index + 1, definition)
            self.measured[entry.number] = entry
            self.at[entry.position] = entry.number
        # Immutable local readout definitions; they do not collect physical
        # input from the group's coverage Nodes.
        self._output_groups = {
            group.output: group for detector in world.detectors for group in detector.groups
        }
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
            list(definition.windows),
            None if definition.lamp is None else definition.lamp.rate,
            () if definition.lamp is None else definition.lamp.headings,
            None if definition.lamp is None else definition.lamp.window,
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
        transit.arr_mom[cell] = (
            canonical_momentum(amount, self.families[family].quantum, port)
            if self.world.dynamics == REVERSIBLE_DETECTOR_DYNAMICS
            else self._momentum(family, amount, port)
        )
        transit.fresh[cell[:4]] = True

    # -- the interval ----------------------------------------------------------

    def step(self) -> None:
        """One interval, in the order of the module docstring."""
        if self.world.dynamics == REVERSIBLE_DETECTOR_DYNAMICS:
            self._reversible_step()
            return
        self.tick += 1
        world = self.world
        for transit in self.transits:
            transit.tick = self.tick
        arrived = [transit.walk() for transit in self.transits]
        # The presence: per Node and number the amount that arrived this
        # interval, over every family, and its total per Node (what a reader
        # reads less its own number); the readings (the count, the flow and
        # the sizes per family) alongside.
        numbers = len(world.measured)
        presence_by_number = np.zeros((*self.shape, numbers + 1), dtype=np.int64)
        for index, transit in enumerate(self.transits):
            self.count[index] = transit.count()
            self.per_port[index] = transit.arr_amt.sum(axis=3)
            self.flow[index] = self.per_port[index] @ HEADINGS
            self.size[index] = (
                transit.sizes() if transit.owners else np.zeros((*self.shape, 0), dtype=np.int64)
            )
            per_number = transit.arr_amt.sum(axis=-1)
            for rank, number in enumerate(transit.owners):
                presence_by_number[..., number] += per_number[..., rank]
        presence_total = presence_by_number.sum(axis=-1)
        # The suspension of a paid family's events at the Nodes they reached:
        # each number's arrivals read the presence of every other number.
        if world.suspension[0]:
            for index, transit in enumerate(self.transits):
                if self.families[index].free or not transit.owners:
                    continue
                read = presence_total[..., None] - presence_by_number[..., list(transit.owners)]
                transit.suspend(read, world.suspension, arrived[index])
        # The events at the measured events, then the mixing.
        for number in sorted(self.measured):
            self._meet(self.measured[number])
        for transit in self.transits:
            transit.cycle()
        # The self-creations: the releases and the clocks, each followed by
        # the read of the count it owes; the steps last, in number order.
        for number in sorted(self.measured):
            entry = self.measured[number]
            if self._release(entry):
                self._suspend(entry, presence_total, presence_by_number)
        for number in sorted(self.measured):
            if number in self.measured:
                self._move(self.measured[number])

    def _suspend(
        self, entry: Measured, presence_total: np.ndarray, presence_by_number: np.ndarray
    ) -> None:
        """The count a measured event owes after its self-creation: the
        presence at its Node this interval of every number but its own (the
        amount that arrived, over every family) times the width's numerator
        over its denominator, the whole part, written once per self-creation
        and paid one per interval before the next (never accumulated; nothing
        without a width). A steady presence that reads k slows the clock to
        one self-creation per k + 1 intervals and never stops it."""
        numerator, denominator = self.world.suspension
        if not numerator:
            return
        read = int(presence_total[entry.position]) - int(
            presence_by_number[(*entry.position, entry.number)]
        )
        entry.owed = read * numerator // denominator

    # -- the explicitly selected reversible candidate -------------------------

    def _reversible_arrivals(self) -> dict[Address3, list[CarrierState]]:
        """Read bounded local inputs without combining slots or changing state.

        Initial arrivals are already at their Nodes. At later normalized
        boundaries each flight travels exactly one Link. The host gathers
        proposals; every gathered physical input came from that local Link.
        """
        found: dict[Address3, list[CarrierState]] = {}
        initial = self.tick == 0
        for family, transit in enumerate(self.transits):
            if transit.suspended.any() or transit.escaped or transit.escaped_momentum.any():
                raise ValueError("reversible detector: suspension or escaped content is unsupported")
            inactive = (
                (transit.fly_amt, transit.fly_ph, transit.fly_mom)
                if initial
                else (transit.arr_amt, transit.arr_ph, transit.arr_mom)
            )
            if any(values.any() for values in inactive):
                raise ValueError("reversible detector: mixed or nonnormalized boundary state")
            amounts, phases, momenta = (
                (transit.arr_amt, transit.arr_ph, transit.arr_mom)
                if initial
                else (transit.fly_amt, transit.fly_ph, transit.fly_mom)
            )
            empty = amounts == 0
            if phases[empty].any() or momenta[empty].any():
                raise ValueError("reversible detector: empty channel payload must be zero")
            for indices in np.argwhere(amounts != 0):
                x, y, z, rank, port = (int(value) for value in indices)
                cell = (x, y, z, rank, port)
                carried = tuple(int(value) for value in momenta[cell])
                carrier = CarrierState(
                    family,
                    transit.owners[rank],
                    int(amounts[cell]),
                    int(phases[cell]),
                    port,
                    (carried[0], carried[1], carried[2]),
                )
                validate_carrier(carrier, self.world.phase_steps, self.families[family].quantum)
                position = (x, y, z)
                if not initial:
                    destination = adjacent_node(position, port, self.shape, self.world.periodic)
                    if destination is None:
                        raise ValueError("reversible detector: open-edge escape is unsupported")
                    position = destination
                found.setdefault(position, []).append(carrier)
        return found

    def _reversible_material(self, entry: Measured) -> ContactState:
        """Validate the restricted ordinary material Event before proposing."""
        definition = self.world.measured[entry.number - 1]
        expected = [0] * len(self.families)
        expected[definition.family] = definition.amount
        if (
            entry.position != definition.position
            or entry.held != expected
            or not entry.fixed
            or entry.charge != 0
            or entry.lamp_rate is not None
            or entry.owed != 0
            or any(entry.home)
            or any(window is not None for window in entry.windows)
            or entry.table != definition.table
        ):
            raise ValueError("reversible detector: unsupported material state")
        if len(entry.momentum) != 3:
            raise ValueError("reversible detector: material momentum must have three components")
        state = ContactState(entry.phase, (entry.momentum[0], entry.momentum[1], entry.momentum[2]))
        validate_material(state, self.world.phase_steps)
        return state

    def _reversible_capacity(self, entry: Measured, amount: int) -> None:
        """A finite pointer admits only the increment already at its Node."""
        group = self._output_groups.get(entry.position)
        if group is None:
            return
        value = self._pointer(entry, group)
        if checked_work(value + amount) > group.capacity:
            raise ValueError("reversible detector: output capacity exceeded")

    @staticmethod
    def _carrier_record(carrier: CarrierState) -> dict[str, object]:
        """Detached audit payload; an observer cannot mutate the proposal."""
        return {
            "family": carrier.family,
            "number": carrier.number,
            "amount": carrier.amount,
            "phase": carrier.phase,
            "port": carrier.port,
            "momentum": list(carrier.momentum),
        }

    def _reversible_node(
        self, position: Address3, arrivals: list[CarrierState], tick: int
    ) -> tuple[list[CarrierState], tuple[int, ContactState, int] | None, list[dict[str, object]]]:
        """Propose one Node from its arrived channels and resident only."""
        ordered = sorted(arrivals, key=lambda item: (item.family, item.number, item.port))
        local_amount = 0
        input_slots: set[tuple[int, int, int]] = set()
        for carrier in ordered:
            slot = (carrier.family, carrier.number, carrier.port)
            if slot in input_slots:
                raise ValueError("reversible detector: duplicate arrival slot")
            input_slots.add(slot)
            local_amount = checked_work(local_amount + carrier.amount)
            if local_amount > STATE_BOUND:
                raise OverflowError("reversible detector: local amount bound exceeded")
        number = self.at.get(position)
        if number is None:
            return ordered, None, []
        entry = self.measured[number]
        material = self._reversible_material(entry)
        definition = self.world.measured[number - 1]
        increment = 0
        for carrier in ordered:
            if entry.table[carrier.family] == "transduce":
                increment = checked_work(increment + carrier.amount)
        self._reversible_capacity(entry, increment)
        outgoing = []
        records: list[dict[str, object]] = []
        output_slots: set[tuple[int, int, int]] = set()
        for incoming in ordered:
            rule = entry.table[incoming.family]
            after = incoming
            if rule == "transduce":
                before_material = material
                after, material = transduce(
                    incoming,
                    material,
                    definition.port_map,
                    self.world.phase_steps,
                    self.families[incoming.family].quantum,
                )
                if self.record is not None:
                    records.append(
                        {
                            "kind": "transduction",
                            "tick": tick,
                            "node": list(position),
                            "incoming": self._carrier_record(incoming),
                            "outgoing": self._carrier_record(after),
                            "material_before": {
                                "phase": before_material.phase,
                                "momentum": list(before_material.momentum),
                            },
                            "material_after": {
                                "phase": material.phase,
                                "momentum": list(material.momentum),
                            },
                        }
                    )
            elif rule != "pass":
                raise ValueError("reversible detector: unsupported contact rule")
            slot = (after.family, after.number, after.port)
            if slot in output_slots:
                raise ValueError("reversible detector: outgoing slot conflict")
            output_slots.add(slot)
            outgoing.append(after)
        age, phase = clock_step(
            entry.age, entry.content, self.world.clock, self.world.phase_steps, material.phase
        )
        return outgoing, (number, ContactState(phase, material.momentum), age), records

    def _reversible_step(self) -> None:
        """Validate the whole interval before committing any physical owner.

        Proposals are temporary host scheduling data. No prior board, input
        history or proposal survives the commit as hidden physical state.
        """
        tick = checked_work(self.tick + 1)
        if tick > STATE_BOUND:
            raise OverflowError("reversible detector: tick bound exceeded")
        arrivals = self._reversible_arrivals()
        nodes = set(arrivals) | set(self.at)
        departures: list[tuple[Address3, CarrierState]] = []
        material_updates: list[tuple[int, ContactState, int]] = []
        records = []
        for position in sorted(nodes):
            outgoing, material, node_records = self._reversible_node(
                position, arrivals.get(position, []), tick
            )
            departures.extend((position, carrier) for carrier in outgoing)
            if material is not None:
                material_updates.append(material)
            records.extend(node_records)
        # Nothing above this boundary mutates physical state or audit state.
        for transit in self.transits:
            for values in (
                transit.arr_amt,
                transit.arr_ph,
                transit.arr_mom,
                transit.fly_amt,
                transit.fly_ph,
                transit.fly_mom,
                transit.fresh,
            ):
                values[...] = 0
            transit.tick = tick
        for position, carrier in departures:
            transit = self.transits[carrier.family]
            cell = (*position, transit.rank[carrier.number], carrier.port)
            transit.fly_amt[cell] = carrier.amount
            transit.fly_ph[cell] = carrier.phase
            transit.fly_mom[cell] = carrier.momentum
        for number, updated_material, age in material_updates:
            entry = self.measured[number]
            entry.phase = updated_material.phase
            entry.momentum = list(updated_material.momentum)
            entry.age = age
        self.tick = tick
        if self.record is not None:
            for record in records:
                self.record(record)

    def _pointer(self, entry: Measured, group: DetectorGroupDefinition) -> int:
        return pointer_displacement(
            entry.phase,
            entry.age,
            entry.content,
            group.reference_phase,
            self.world.clock,
            self.world.phase_steps,
        )

    def detector_readouts(self) -> list[dict[str, object]]:
        """Read existing output Events; coverage never supplies an input."""
        if self.world.dynamics != REVERSIBLE_DETECTOR_DYNAMICS:
            return []
        result: list[dict[str, object]] = []
        for detector in self.world.detectors:
            groups = []
            for group in detector.groups:
                entry = self.measured[self.at[group.output]]
                value = self._pointer(entry, group)
                groups.append(
                    {"name": group.name, "value": value, "triggered": value >= group.threshold}
                )
            result.append(
                {
                    "name": detector.name,
                    "positions": [list(position) for position in detector.positions],
                    "groups": groups,
                }
            )
        return result

    def _meet(self, entry: Measured) -> None:
        """The events at a measured event's Node: every arrival of its own
        number measured home, every other number's met by the table when the
        bundle reaches the detector's threshold (1 outside a detector: every
        response, read, measure or rerelease, is gated; a smaller bundle
        passes with no push and mixes on) and, where the entry declares a
        phase window, when the bundle's phase at the Node falls in it (a
        bundle outside it passes the same way, and a `pass` record says so).
        The phase read is stamped on every measurement record."""
        position = entry.position
        modulus = self.world.phase_steps
        for index, transit in enumerate(self.transits):
            if not transit.owners:
                continue
            rule = entry.table[index]
            window = entry.windows[index]
            free = self.families[index].free
            for rank, number in enumerate(transit.owners):
                cell = (*position, rank)
                if not transit.arr_amt[cell].any():
                    continue
                total = int(transit.arr_amt[cell].sum())
                # The phase of the bundle at the Node, read only when the
                # window or the record needs it (fixed local work either way).
                phase = None
                if window is not None or self.record is not None:
                    phase = transit.phase_at(position, rank)
                if number == entry.number:
                    transit.take(position, rank)
                    entry.home[index] += total
                    entry.measured[index]["home"] += total
                    self.transit_absorbed[index] += total
                    self._event("home", entry, index, number, total, ZERO3, phase)
                    continue
                if rule == "pass" or total < entry.threshold:
                    continue
                if window is not None:
                    assert phase is not None
                    if not in_window(phase, window, modulus):
                        self._pass(entry, index, number, total, phase, window)
                        continue
                # A free family's push reads the net flow of the bundle, a
                # paid family's the momentum it carries.
                if free:
                    vector = [int(v) for v in transit.arr_amt[cell] @ HEADINGS]
                else:
                    vector = [int(v) for v in transit.arr_mom[cell].sum(axis=0)]
                push = self._push(entry, free, number, vector)
                entry.momentum = [int(a) + int(b) for a, b in zip(entry.momentum, push, strict=True)]
                entry.pushed = [int(a) + int(b) for a, b in zip(entry.pushed, push, strict=True)]
                if rule == "read":
                    entry.measured[index]["read"] += total
                    self._event("read", entry, index, number, total, push, phase)
                    continue
                transit.take(position, rank)
                self.transit_absorbed[index] += total
                entry.measured[index][rule] += total
                if rule == "measure":
                    entry.held[index] += total
                    entry.events[index] += total
                    self.held_measured[index] += total
                    self._event("click", entry, index, number, total, push, phase)
                    continue
                entry.home[index] += total
                self._event("rerelease", entry, index, number, total, push, phase)

    def _pass(
        self, entry: Measured, family: int, number: int, amount: int, phase: int, window: int
    ) -> None:
        """The record of a bundle that passed a measured event's Node outside
        the entry's phase window: no push, the units mixing on."""
        if self.record is None:
            return
        self.record(
            {
                "event": "pass",
                "tick": self.tick,
                "node": list(entry.position),
                "measured": entry.number,
                "detector": None
                if entry.detector is None
                else self.world.detectors[entry.detector].name,
                "family": self.families[family].name,
                "number": number,
                "amount": amount,
                "phase": phase,
                "window": window,
            }
        )

    def _push(self, entry: Measured, free: bool, number: int, vector: list[int]) -> tuple[int, int, int]:
        """The push of the units of one number arriving at a measured event:
        for a free family the gravity and the electric readings of `vector`,
        their net flow (amount times travel heading summed over the six
        Ports); for a paid family `vector` is the momentum they carry and the
        push is it."""
        if not free:
            return vector[0], vector[1], vector[2]
        content = entry.content
        push = [-vector[axis] * content for axis in range(3)]
        owner = self.world.measured[number - 1]
        if owner.charge and entry.charge:
            scale = owner.charge * entry.charge * (self.denominator // owner.amount)
            for axis in range(3):
                total = vector[axis] * scale
                whole = by_clock(entry.age, abs(total), self.denominator)
                push[axis] += -whole if total < 0 else whole
        return push[0], push[1], push[2]

    def _release(self, entry: Measured) -> bool:
        """The self-creation of a measured event that owes nothing: its clock
        advances, its releases and its phase turn read off it (True). One
        that owes a count pays it by one instead, no release and no turn,
        and `waited` counts the interval (False)."""
        if entry.owed > 0:
            entry.owed -= 1
            entry.waited += 1
            return False
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
            if (
                entry.lamp_rate is not None
                and index == entry.family
                and (
                    entry.lamp_window is None
                    or in_window(entry.phase, entry.lamp_window, self.world.phase_steps)
                )
            ):
                # A lamp with a window releases only at the self-creations
                # whose clock phase (the one stamped on the release) falls in
                # it; the clock and the phase turn below either way.
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
        if not self.families[entry.family].phase:
            # A measured event of a family without a phase circle never turns.
            return True
        steps = by_clock(age, entry.content, self.world.clock)
        if 2 * steps >= self.world.phase_steps:
            raise ValueError(
                f"{EVENTS_LAW}: measured event {entry.number} turns its phase by half the circle or "
                "more per self-creation (its content has grown past K x N / 2)"
            )
        entry.phase = (entry.phase + steps) & self.world.phase_mask
        entry.phase_steps += steps
        return True

    def _move(self, entry: Measured) -> None:
        """The step by the momentum off the clock, at most one per interval,
        when nothing is owed: in the self-creation's interval when it read no
        count, else in the interval the last unit of its count is paid (the
        self-creation is then the last, `age - 1` its age before it). One rule
        for the board (the model owner, 2026-09-19): through an open face the
        step escapes with the content; on a periodic axis it wraps as the
        departures do, and with an extent of 1 it lands on its own Node, no
        move and no merge (`steps` counts every step made off the clock,
        wherever it lands: a move, a merge, an escape or its own Node)."""
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
            origin = entry.position
            port = 2 * axis + (0 if sign > 0 else 1)
            destination = adjacent_node(origin, port, self.shape, self.world.periodic)
            if destination == origin:
                # A self-Link counts the step without a coordinate move,
                # a movement record or a merge with the Event itself.
                return
            del self.at[origin]
            if destination is None:
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
        phase: int | None = None,
    ) -> None:
        """A record through the observer; a measurement (`home`, `read`,
        `click`, `rerelease`) carries the phase read at the Node, a `merged`
        or `escaped` measured event none."""
        if self.record is None:
            return
        record: dict[str, object] = {
            "event": kind,
            "tick": self.tick,
            "node": list(entry.position),
            "measured": entry.number,
            "detector": None if entry.detector is None else self.world.detectors[entry.detector].name,
            "family": self.families[family].name,
            "number": number,
            "amount": amount,
            "push": list(push),
        }
        if phase is not None:
            record["phase"] = phase
        self.record(record)

    # -- the books -------------------------------------------------------------

    def books(self) -> dict[str, object]:
        """The ledger at the current tick, every line with its identity."""
        if self.world.dynamics == REVERSIBLE_DETECTOR_DYNAMICS:
            return self._reversible_books()
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

    def _reversible_books(self) -> dict[str, object]:
        """Exact read-only host totals, bounded by the finite world layout.

        These sums may exceed a physical working register. They never enter
        an admission guard or a physical update (DETECTOR_REQUIREMENTS.md).
        """
        families: dict[str, object] = {}
        carried = [0, 0, 0]
        balanced = True
        for index, family in enumerate(self.families):
            transit = self.transits[index]
            amount = sum(int(value) for value in transit.arr_amt.flat) + sum(
                int(value) for value in transit.fly_amt.flat
            )
            for axis in range(3):
                carried[axis] += sum(int(value) for value in transit.arr_mom[..., axis].flat)
                carried[axis] += sum(int(value) for value in transit.fly_mom[..., axis].flat)
            content = sum(entry.held[index] for entry in self.measured.values())
            held_ok = content == self.held_initial[index]
            transit_ok = amount == self.transit_initial[index]
            families[family.name] = {
                "measured": {
                    "initial": self.held_initial[index],
                    "measured": 0,
                    "current": content,
                    "spent": 0,
                    "escaped": 0,
                    "balanced": held_ok,
                },
                "transit": {
                    "initial": self.transit_initial[index],
                    "released": 0,
                    "current": amount,
                    "escaped": 0,
                    "absorbed": 0,
                    "balanced": transit_ok,
                },
            }
            balanced = balanced and held_ok and transit_ok
        return {
            "tick": self.tick,
            "families": families,
            "momentum": {
                "measured": [
                    sum(entry.momentum[axis] for entry in self.measured.values()) for axis in range(3)
                ],
                "transit": carried,
                "escaped": [0, 0, 0],
            },
            "charge": 0,
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
        if self.world.dynamics == REVERSIBLE_DETECTOR_DYNAMICS or any(self.world.periodic):
            raise ValueError("cube_flux supports only the all-open default arrival diagnostic")
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
        if self.world.dynamics == REVERSIBLE_DETECTOR_DYNAMICS:
            yield "dynamics", self.world.dynamics
            yield "detector_readouts", self.detector_readouts()
        yield "tick", self.tick
        yield "shape", list(self.shape)
        yield "boundary", self.world.boundary
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
