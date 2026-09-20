"""The frame around the law of the ray (rays-v1): the tick, the measured
events' clocks, the books, the record and the snapshot. The law itself is
the one function `nature_beam` (docs/RAY_LAW.md); this module schedules and
books, it computes no physics.

The interval (`RaySimulation.step`): the engine sets every measured event's
clock frame (whether it owes a count and pays one, or self-creates: its age
advances by one and its turn is read off its clock, s = `by_clock(age,
content, K)` phase steps, refused at half the circle), calls `nature_beam`
once for the whole board (the walk, the readings, the collision, the tables
and detectors, the releases, the merge), then turns the phase of every
self-created measured event by its turn, reads the count it owes off its
clock from what the law read back for the clock (`by_clock(age, k x n, d)`
at the world's `suspension` `[n, d]`, k the presence, or the age moment for
a family whose table entry reads `age`: `measured.count_component`), and
steps the free measured events by their
momentum off the clock (one Link per (Q x S x M + p) / p self-creations on
an axis whose momentum component is p in label units, M the content, S the
world's `width` and Q = 64 the label's scale, `by_clock(age, |p|, Q x S x M
+ |p|)`: one unit of net flow, the label Q x M, gives the speed 1 / (S + 1)
for every content, as it did when the label of a heading was the unit; at
most one Link per interval, x before y before z; a step onto a Node that
holds a measured event is refused; through an open face the step is a
click on the face detector; on a periodic axis it wraps). The books
(`books`): per family the measured line, in content,
initial + measured = current + spent + escaped; the transit line, in units,
initial + released = current + escaped + absorbed; the content line, the
content carried, initial + released = current + escaped + absorbed; the
momentum reported on the measured events, in transit (the one label of
every row, content x amount x u_d per ray of a paid family, amount x u_d of
a free one, u_d the unit vector of the direction at the scale Q) and
escaped, all in label units; every escaped line the sum of the face
detectors' clicks; every sum exact (`exact_sum`), never a wrapped register.
"""

from __future__ import annotations

from collections.abc import Iterator

import numpy as np

from event_universe.core.integer import by_clock
from event_universe.core.lattice import Address3, adjacent_node
from event_universe.events.measured import RULES, DetectorSet, Ledger, Measured, rational_sum
from event_universe.events.nature_beam import (
    HERE,
    ArrivalRows,
    RayStore,
    RayTables,
    Readings,
    Record,
    bounded,
    exact_column_sums,
    exact_sum,
    nature_beam,
    ray_tables,
)
from event_universe.events.world import (
    DETECTOR_READINGS,
    FACE_NAMES,
    LABEL_SCALE,
    MOMENTUM_BOUND,
    RAYS_LAW,
    MeasuredDefinition,
    RayWorld,
    body_nodes,
)

__all__ = ["RULES", "Measured", "RaySimulation", "count_owed", "step_axis"]


def step_axis(age: int, momentum: int, content: int, width: int) -> int | None:
    """The step rule of one axis (RAY_LAW section 3 step 5; `_move` calls
    it): the sign of the Link a free measured event of content M = `content`
    steps this interval on an axis whose momentum component is p =
    `momentum`, with `age` its age after the frame's advance and `width`
    the world's S, when `by_clock(age - 1, |p|, Q x S x M + |p|)` is 1;
    None when it does not step (a momentum of 0 never steps). The one
    place the rule lives; the readings tools read it from here."""
    if momentum == 0:
        return None
    magnitude = abs(momentum)
    reach = LABEL_SCALE * width * content
    if not by_clock(age - 1, magnitude, reach + magnitude):
        return None
    return 1 if momentum > 0 else -1


def count_owed(age: int, counted: int, suspension: tuple[int, int]) -> int:
    """The count a measured event owes after its self-creation (ENGINE,
    the frame; `_suspend` calls it): what its clock counted (`counted`, the
    presence or the age moment) times the width n / d of the world's
    `suspension`, off its clock, `by_clock(age, counted x n, d)` with `age`
    the age before the self-creation; 0 when the width is 0."""
    numerator, denominator = suspension
    if not numerator:
        return 0
    return by_clock(age, counted * numerator, denominator)


class RaySimulation:
    """One world of the law of the ray, stepped interval by interval."""

    def __init__(self, world: RayWorld, observer: Record | None = None) -> None:
        self.world = world
        self.record = observer
        self.tick = 0
        self.shape = world.shape
        self.families = world.families
        self._phased = [family.phase for family in world.families]
        count = len(world.families)
        self.tables: RayTables = ray_tables(world)
        self.stores = [RayStore(world.shape) for _ in world.families]
        self.open_faces = tuple(port for port in range(6) if not world.periodic[port >> 1])
        self.ledger = Ledger(count, self.open_faces)
        # The detectors at run time: the declared ones first, in their
        # order, then a detector of one Node for every measured event
        # outside them (the model owner, 2026-09-19: a detector is a set
        # of Nodes with one record).
        self.detector_sets: list[DetectorSet] = [
            DetectorSet(
                index,
                detector.name,
                detector.reading,
                detector.threshold,
                [],
                [0] * count,
                [None] * count,
            )
            for index, detector in enumerate(world.detectors)
        ]
        self.measured: dict[int, Measured] = {}
        self.at: dict[Address3, int] = {}
        for index, definition in enumerate(world.measured):
            entry = self._measured(index + 1, definition)
            self.measured[entry.number] = entry
            # Every Node of a body on a set holds its number (a step onto
            # any of them is refused; the parser refused a shared Node).
            for node in entry.nodes:
                self.at[node] = entry.number
        self.held_initial = [sum(m.held[f] for m in self.measured.values()) for f in range(count)]
        self.transit_initial = [0] * count
        self.content_initial = [0] * count
        for item in world.in_transit:
            store = self.stores[item.family]
            # One phase step of content per unit for a paid family; a free
            # family's quantum is 0 and its rays carry none (its family's
            # charge per unit of content is the factor of the electric push;
            # the record carries nothing of its emitter but its number).
            content = self.families[item.family].quantum
            store.append(
                node=np.array([store.flat(item.position)]),
                direction=np.array([item.direction]),
                # The age is kept whole on the record (the parser bounds it
                # by `age_bound`); the flight reads it modulo the period.
                age=np.array([item.age]),
                phase=np.array([item.phase]),
                number=np.array([item.number]),
                amount=np.array([item.amount]),
                content=np.array([content]),
                arrival=np.array([HERE]),
            )
            self.transit_initial[item.family] += item.amount
            self.content_initial[item.family] += content * item.amount
        for store in self.stores:
            store.merge()
        # The running transit line of the momentum starts from the declared
        # rows, counted once.
        self.ledger.transit_momentum = self.recount()["momentum"]
        # The readings of the last interval (diagnostics, decomposed on
        # request): per family the arrivals per Node, their net flow, the
        # Links crossed per Port and the presence.
        self.readings = Readings(
            world.shape, self.tables.flight.labels, [ArrivalRows.empty() for _ in range(count)]
        )

    @property
    def count(self) -> list[np.ndarray]:
        return self.readings.count

    @property
    def flow(self) -> list[np.ndarray]:
        return self.readings.flow

    @property
    def per_port(self) -> list[np.ndarray]:
        return self.readings.per_port

    @property
    def presence(self) -> list[np.ndarray]:
        return self.readings.presence

    def _measured(self, number: int, definition: MeasuredDefinition) -> Measured:
        count = len(self.families)
        held = [0] * count
        held[definition.family] = definition.amount
        detector = self.world.detector_of(definition.position)
        if detector is None:
            detector_set = DetectorSet(
                len(self.detector_sets),
                None,
                DETECTOR_READINGS[0],
                1,
                [number],
                [0] * count,
                [None] * count,
            )
            self.detector_sets.append(detector_set)
        else:
            detector_set = self.detector_sets[detector]
            detector_set.numbers.append(number)
        # The set of Nodes the measured event is a body on (the parser
        # refused a body outside the board).
        nodes = body_nodes(definition.position, definition.span, self.shape, self.world.periodic)
        assert nodes is not None
        return Measured(
            number,
            definition.position,
            definition.family,
            held,
            definition.phase,
            self.families[definition.family].charge,
            list(definition.momentum),
            definition.fixed,
            definition.directions,
            definition.table,
            list(definition.windows),
            definition.reads,
            None if definition.lamp is None else definition.lamp.rate,
            () if definition.lamp is None else definition.lamp.directions,
            None if definition.lamp is None else definition.lamp.window,
            definition.amount,
            detector,
            detector_set,
            span=definition.span,
            nodes=nodes,
            phase_by_momentum=definition.phase_by_momentum,
            column_names=tuple(name for name, _ in self.world.columns),
            family_values=tuple(family.values for family in self.families),
            pending=[[] for _ in range(count)],
            measured=[dict.fromkeys(RULES, 0) for _ in range(count)],
            events=[0] * count,
        )

    # -- the interval ----------------------------------------------------------

    def step(self) -> None:
        """One interval: the clocks' frame, the law, the clocks' count and
        the measured events' steps."""
        self.tick += 1
        self._frame_all()
        self.readings = nature_beam(
            self.stores,
            self.world,
            self.tables,
            self.measured,
            self.tick,
            self.record,
            self.ledger,
        )
        for number in sorted(self.measured):
            entry = self.measured[number]
            if entry.creating:
                entry.phase = (entry.phase + entry.turn) & self.world.phase_mask
                entry.phase_steps += entry.turn
                self._suspend(entry)
        for number in sorted(self.measured):
            if number in self.measured:
                self._move(self.measured[number])

    def inverse_step(self) -> None:
        """The inverse interval on a board without measured events: the
        bijective steps in reverse order with their inverses."""
        self.tick -= 1
        nature_beam(
            self.stores,
            self.world,
            self.tables,
            self.measured,
            self.tick,
            None,
            self.ledger,
            inverse=True,
        )

    def _frame_all(self) -> None:
        """The clocks' frame, every measured event at once: its content is
        read once into `frame_content` (M_A of the interval's push, RAY_LAW
        step 4) and its charge in every column into `frame_charges` (the
        reader's side of the push over the columns, gravity's the content);
        one that owes a count pays it by one (no self-creation, no
        release, no turn; `waited` counts the interval); one that owes
        nothing self-creates: its age advances and its turn is read off its
        clock, `by_clock(age, content, K)`, the turns of the phased families
        taken in one array where their products fit the register (row by
        row otherwise), and refused at half the circle."""
        phased: list[Measured] = []
        for entry in self.measured.values():
            entry.turn = 0
            # The content and the charges the frame reads, once, for the
            # turn and for the push of this interval (M_A and the columns'
            # E_c at the frame: the clicks of the interval join `held`
            # after it).
            entry.frame_content = entry.content
            entry.frame_charges = entry.charges()
            if entry.owed > 0:
                entry.owed -= 1
                entry.waited += 1
                entry.creating = False
                continue
            entry.creating = True
            entry.clock_age = entry.age
            entry.age += 1
            if self._phased[entry.family]:
                phased.append(entry)
        if not phased:
            return
        clock = self.world.clock
        ages = [entry.clock_age for entry in phased]
        contents = [entry.frame_content for entry in phased]
        if (max(ages) + 1) * max(contents) <= MOMENTUM_BOUND:
            age_column = np.array(ages, dtype=np.int64)
            content_column = np.array(contents, dtype=np.int64)
            turns = (
                ((age_column + 1) * content_column) // clock - (age_column * content_column) // clock
            ).tolist()
        else:
            turns = [by_clock(age, content, clock) for age, content in zip(ages, contents, strict=True)]
        for entry, turn in zip(phased, turns, strict=True):
            if 2 * turn >= self.world.phase_steps:
                raise ValueError(
                    f"{RAYS_LAW}: measured event {entry.number} turns its phase by half the circle "
                    "or more per self-creation (its content has grown past K x N / 2)"
                )
            entry.turn = turn

    def _suspend(self, entry: Measured) -> None:
        """The count a measured event owes after its self-creation: what
        its clock counted at its Node over every number but its own, read
        back by the law (`Measured.counted`: the presence k, or for a family
        whose table entry reads `age` the age moment, sum amount x age; the
        selection is `measured.count_component`), times the width n / d, off
        its clock, `by_clock(age, k x n, d)`, written once and paid one per
        interval before the next."""
        if not self.world.suspension[0]:
            return
        entry.owed = count_owed(entry.clock_age, entry.counted, self.world.suspension)

    def _move(self, entry: Measured) -> None:
        """The step by the momentum off the clock, at most one per interval,
        when nothing is owed: on an axis whose momentum component is p (in
        label units), one Link per (Q x S x M + p) / p self-creations,
        `by_clock(age, |p|, Q x S x M + |p|)` with M the content, S the
        world's `width` (the model owner's D1 of 2026-09-19) and Q = 64 the
        label's scale (the physics-rule reviewer's correction 2 of the
        label along the unit vector, 2026-09-19: the width in units of one
        free unit's label, Q x M, so that one unit of net flow gives the
        speed 1 / (S + 1) for every content and every step registered
        before the change is the same, `by_clock(age, Q n, Q k) =
        by_clock(age, n, k)`); no remainder is kept, the count is the whole
        part off the clock. A step onto a measured event is refused; an
        escape is a click on the face; a periodic axis wraps.

        A body on a set of Nodes (`span`; the model owner, 2026-09-20)
        steps as one: its centre moves one Link and its set with it, the
        step refused when any Node of the moved set holds another measured
        event, the whole body clicking on the face detector when any of
        its Nodes would leave the board through an open face, every Node
        wrapping on a periodic axis.

        The turn by momentum (`phase_by_momentum` with the world's
        `action`, h; the model owner's decision of 2026-09-20 on Bohr, "put
        it as parameters outside the board like the age"): a rule of the
        measured event, the external thing, read from its own record. At
        the Link the body steps on an axis whose momentum component is p,
        its phase turns by the difference of two floors,

            floor(k1 x |p| x N / h) - floor(k0 x |p| x N / h),

        with k0 = floor((age - 1) x |p| / (Q S M + |p|)) the count of Links
        the step rule gives on that axis at the age before this
        self-creation and k1 = k0 + 1 the count after it (the count is
        derived from the age by the step rule exactly as the owed count is
        read off the clock; with a constant momentum k1 is the Links
        stepped on the axis, so after k Links the phase has turned
        floor(k x |p| x N / h) mod N in all), that is `by_clock(k0, |p| x
        N, h)`: nothing is kept at a Node and no remainder register
        exists, the count and the turn are functions of the record (the
        age, the momentum). The axes compose: the steps are x before y
        before z, and the phase's turn is the sum of the three components'
        turns at the Links stepped on each (a step lost to an earlier
        axis's step in the same interval turns nothing: no Link was
        crossed). It changes nothing of the rays' flight or collision; the
        rays the body releases carry its phase as before (the clock's turn
        by content over K is added at the self-creation as always, this
        turn at the step after it); without `action` there is no turn. The
        product k1 x |p| x N is bounded before it is formed (`bounded`;
        the parser refused a declared momentum whose product with `ticks`
        x N could pass the bound)."""
        if entry.fixed or entry.owed > 0:
            return
        content = entry.content
        if content <= 0:
            return
        width = LABEL_SCALE * self.world.width * content
        for axis in range(3):
            momentum = entry.momentum[axis]
            stepped = step_axis(entry.age, momentum, content, self.world.width)
            if stepped is None:
                continue
            magnitude = abs(momentum)
            sign = stepped
            entry.steps += 1
            origin = entry.position
            port = 2 * axis + (0 if sign > 0 else 1)
            destination = adjacent_node(origin, port, self.shape, self.world.periodic)
            if destination == origin:
                return
            # The moved set: None when the centre or any Node of the body
            # would leave the board through an open face (the escape).
            nodes = (
                None
                if destination is None
                else body_nodes(destination, entry.span, self.shape, self.world.periodic)
            )
            if destination is None or nodes is None:
                for index in range(len(self.families)):
                    self.ledger.held_escaped[index] += entry.held[index]
                    self.ledger.transit_absorbed[index] -= entry.pending_amount(index)
                    self.ledger.content_absorbed[index] -= entry.pending_content(index)
                    self.ledger.face_measured_content[port][index] += entry.held[index]
                    self.ledger.face_units[port][index] += entry.pending_amount(index)
                    self.ledger.face_content[port][index] += entry.pending_content(index)
                self.ledger.face_momentum[port] = [
                    int(a) + int(b)
                    for a, b in zip(self.ledger.face_momentum[port], entry.momentum, strict=True)
                ]
                for node in entry.nodes:
                    del self.at[node]
                del self.measured[entry.number]
                if self.record is not None:
                    self.record(
                        {
                            "event": "click",
                            "tick": self.tick,
                            "node": list(origin),
                            "measured": entry.number,
                            "detector": FACE_NAMES[port],
                            "family": self.families[entry.family].name,
                            "number": entry.number,
                            "amount": content,
                            "phase": entry.phase,
                            "momentum": list(entry.momentum),
                            "content": content,
                            "held": list(entry.held),
                            "home": [entry.pending_amount(f) for f in range(len(self.families))],
                            "home_content": [
                                entry.pending_content(f) for f in range(len(self.families))
                            ],
                        }
                    )
                return
            if any(self.at.get(node, entry.number) != entry.number for node in nodes):
                return
            for node in entry.nodes:
                del self.at[node]
            entry.position = destination
            entry.nodes = nodes
            for node in nodes:
                self.at[node] = entry.number
            if entry.phase_by_momentum and self.world.action is not None:
                links = ((entry.age - 1) * magnitude) // (width + magnitude)
                bounded((links + 1) * magnitude * self.world.phase_steps, entry, "turn by momentum")
                turn = by_clock(links, magnitude * self.world.phase_steps, self.world.action)
                entry.phase = (entry.phase + turn) & self.world.phase_mask
            if self.record is not None:
                self.record(
                    {
                        "event": "step",
                        "tick": self.tick,
                        "number": entry.number,
                        "node": list(origin),
                        "to": list(destination),
                        "momentum": list(entry.momentum),
                        "phase": entry.phase,
                    }
                )
            return

    # -- the books -------------------------------------------------------------

    def recount(self) -> dict[str, list[int]]:
        """The current lines counted from the store, a pass over every row:
        the units and the content in transit per family and the momentum in
        transit (the one label of every row, `momentum_labels`: content x
        amount x u_d per ray of a paid family, amount x u_d of a free one,
        u_d the unit vector of the direction at the scale Q), every sum
        exact. The check of the running lines of the ledger, on request
        (`books(recount=True)`; the tests assert it equal at every tick)."""
        units: list[int] = []
        content: list[int] = []
        momentum = [0, 0, 0]
        for family, store in enumerate(self.stores):
            units.append(int(exact_sum(store.amount)))
            content.append(int(exact_sum(store.amount * store.content)))
            if store.size:
                definition = self.families[family]
                labels = store.labels(np.arange(store.size), self.tables.flight.labels, definition.free)
                momentum = [a + b for a, b in zip(momentum, exact_column_sums(labels), strict=True)]
        return {"transit": units, "content": content, "momentum": momentum}

    def transit_momentum(self) -> list[int]:
        """The momentum carried in transit: the running line of the ledger,
        the labels of the rows born less the labels of the rows that left
        (escaped, home, absorbed), kept by `nature_beam` (the collision and
        the merge conserve it); `recount` counts it from the rows."""
        return list(self.ledger.transit_momentum)

    def books(self, recount: bool = False) -> dict[str, object]:
        """The ledger at the current tick, every line with its identity. The
        `current` of the transit and content lines and the transit momentum
        are the running lines of the ledger (what was released less what
        left; O(families), no pass over the store); with `recount` they are
        counted from the rows instead, and the identities then check the
        running ledger against the store."""
        counted = self.recount() if recount else None
        families: dict[str, object] = {}
        balanced = True
        ledger = self.ledger
        # One pass over the measured events: what they hold per family,
        # their momentum and their charge (rho x content each, the sum an
        # exact rational reported as the reduced pair [n, d]).
        held_current = [0] * len(self.families)
        held_momentum = [0, 0, 0]
        charges: list[tuple[int, int]] = []
        for entry in self.measured.values():
            for index, held in enumerate(entry.held):
                held_current[index] += held
            held_momentum = [a + b for a, b in zip(held_momentum, entry.momentum, strict=True)]
            charges.append(entry.charge)
        for index, family in enumerate(self.families):
            measured = {
                "initial": self.held_initial[index],
                "measured": ledger.held_measured[index],
                "current": held_current[index],
                "spent": ledger.held_spent[index],
                "escaped": ledger.held_escaped[index],
            }
            measured["balanced"] = measured["initial"] + measured["measured"] == (
                measured["current"] + measured["spent"] + measured["escaped"]
            )
            in_transit = {
                "initial": self.transit_initial[index],
                "released": ledger.transit_released[index],
                "current": (
                    counted["transit"][index]
                    if counted is not None
                    else self.transit_initial[index]
                    + ledger.transit_released[index]
                    - ledger.escaped_units(index)
                    - ledger.transit_absorbed[index]
                ),
                "escaped": ledger.escaped_units(index),
                "absorbed": ledger.transit_absorbed[index],
            }
            in_transit["balanced"] = in_transit["initial"] + in_transit["released"] == (
                in_transit["current"] + in_transit["escaped"] + in_transit["absorbed"]
            )
            content = {
                "initial": self.content_initial[index],
                "released": ledger.content_released[index],
                "current": (
                    counted["content"][index]
                    if counted is not None
                    else self.content_initial[index]
                    + ledger.content_released[index]
                    - ledger.escaped_content(index)
                    - ledger.content_absorbed[index]
                ),
                "escaped": ledger.escaped_content(index),
                "absorbed": ledger.content_absorbed[index],
            }
            content["balanced"] = content["initial"] + content["released"] == (
                content["current"] + content["escaped"] + content["absorbed"]
            )
            balanced = (
                balanced
                and bool(measured["balanced"])
                and bool(in_transit["balanced"])
                and bool(content["balanced"])
            )
            families[family.name] = {"measured": measured, "transit": in_transit, "content": content}
        return {
            "tick": self.tick,
            "families": families,
            "momentum": {
                "measured": held_momentum,
                "transit": counted["momentum"] if counted is not None else self.transit_momentum(),
                "escaped": ledger.escaped_momentum(),
            },
            "charge": list(rational_sum(charges)),
            "balanced": balanced,
        }

    def contents(self) -> list[dict[str, object]]:
        return [self.measured[number].state() for number in sorted(self.measured)]

    def detectors(self) -> list[dict[str, object]]:
        """The measurements per declared detector: its Nodes, its threshold,
        its reading and per family the amount measured and the clicks
        (summed over its Nodes), the set's one `record` (the square of its
        coherent pointer accumulated under `wave`, the count clicked under
        `beam`) and the set's `phase` at its last click; then the face
        detectors, one per open face of the board (`face_detectors`)."""
        found = []
        for index, detector in enumerate(self.world.detectors):
            detector_set = self.detector_sets[index]
            members = [self.measured[n] for n in detector_set.numbers if n in self.measured]
            families = {
                family.name: {
                    "measured": sum(entry.measured[f]["measure"] for entry in members),
                    "clicks": sum(entry.events[f] for entry in members),
                    "record": detector_set.record[f],
                    "phase": detector_set.phase[f],
                }
                for f, family in enumerate(self.families)
            }
            found.append(
                {
                    "name": detector.name,
                    "nodes": len(detector.positions),
                    "threshold": detector.threshold,
                    "reading": detector.reading,
                    "families": families,
                }
            )
        found.extend(self.face_detectors())
        return found

    def face_detectors(self) -> list[dict[str, object]]:
        """The face detectors, one per open face in Port order: per family
        the units that clicked there (`measured`, `clicks`), the `content`
        they carried, their `record` (the same square) and the
        `measured_content` of the measured events that stepped off; and the
        `momentum` that left."""
        found = []
        ledger = self.ledger
        for port in self.open_faces:
            axis = port >> 1
            nodes = 1
            for other in range(3):
                if other != axis:
                    nodes *= self.shape[other]
            found.append(
                {
                    "name": FACE_NAMES[port],
                    "nodes": nodes,
                    "threshold": 1,
                    "families": {
                        family.name: {
                            "measured": ledger.face_units[port][f],
                            "clicks": ledger.face_units[port][f],
                            "content": ledger.face_content[port][f],
                            "record": ledger.face_record[port][f],
                            "measured_content": ledger.face_measured_content[port][f],
                        }
                        for f, family in enumerate(self.families)
                    },
                    "momentum": list(ledger.face_momentum[port]),
                }
            )
        return found

    def shell_readings(self, family: int, centre: Address3, radius: int) -> dict[str, float]:
        """The shell means at one radius of the last interval's readings: the
        Nodes at Euclidean distance within a half Link of `radius` from the
        centre, their number, the mean count (the amount that arrived per
        Node), the mean radial flow (amount x the arrival's unit vector at
        the scale Q projected on the radial unit vector, summed per Node: Q
        per unit of amount moving radially) and the mean presence (every
        ray at the Node)."""
        grid = np.indices(self.shape).reshape(3, -1).T - np.array(centre)
        distance = np.sqrt((grid * grid).sum(axis=1))
        chosen = np.abs(distance - radius) < 0.5
        chosen &= distance > 0
        positions = grid[chosen]
        radial = positions / distance[chosen][:, None]
        cells = tuple((positions + np.array(centre)).T)
        count = self.readings.count[family][cells]
        flow = self.readings.flow[family][cells]
        presence = self.readings.presence[family][cells]
        return {
            "nodes": float(chosen.sum()),
            "count": float(count.mean()),
            "flow": float((flow * radial).sum(axis=1).mean()),
            "presence": float(presence.mean()),
        }

    def cube_flux(self, family: int, centre: Address3, half: int) -> int:
        """The net outward flow through the closed surface between the cube of
        half-width `half` about the centre and its neighbours, this interval:
        the amount that crossed into the Node just outside each face through
        its inner Port (moving outward) less the amount that crossed into the
        face's Node through its outer Port (moving inward), Gauss's flux, read
        off the Links crossed (`per_port`, a diagnostic of the walk)."""
        if any(self.world.periodic):
            raise ValueError("cube_flux supports only the all-open board")
        per_port = self.readings.per_port[family]
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
        """The snapshot as (key, value) pairs, the Nodes with rays as an
        iterator over one entry at a time (`snapshot_writer`)."""
        yield "law", RAYS_LAW
        yield "tick", self.tick
        yield "shape", list(self.shape)
        yield "boundary", self.world.boundary
        yield "measured", self.contents()
        yield "detectors", self.detectors()
        yield (
            "escaped",
            [
                {
                    "family": family.name,
                    "amount": self.ledger.escaped_units(f),
                    "content": self.ledger.escaped_content(f),
                }
                for f, family in enumerate(self.families)
            ],
        )
        yield "nodes", self._node_entries()

    def snapshot(self) -> dict[str, object]:
        return {
            key: (list(value) if isinstance(value, Iterator) else value)
            for key, value in self.snapshot_stream()
        }

    def _node_entries(self) -> Iterator[dict[str, object]]:
        """The Nodes with rays, each with its rows per family: the one
        materialization of a ray's record (`RayStore.rows`, `NatureBeam`),
        written as `NatureBeam.record` says."""
        nodes = sorted({int(node) for store in self.stores for node in np.unique(store.node)})
        vectors = self.tables.flight.vectors
        for flat in nodes:
            x, y, z = self.stores[0].coordinates(np.array([flat]))
            entry: dict[str, object] = {"position": [int(x[0]), int(y[0]), int(z[0])], "families": []}
            families = entry["families"]
            assert isinstance(families, list)
            for family, store in zip(self.families, self.stores, strict=True):
                lo, hi = store.slice(flat)
                if hi == lo:
                    continue
                rays = [ray.record(vectors) for ray in store.rows(lo, hi)]
                families.append({"family": family.name, "rays": rays})
            yield entry
