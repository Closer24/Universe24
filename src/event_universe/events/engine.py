"""The frame around the Beam Law (beam-v1): the tick, the measured
events' clocks, the books, the record and the snapshot. The law itself is
the one function `nature_beam` (docs/BEAM_LAW.md); this module schedules and
books, it computes no physics.

The interval (`NatureBeamSimulation.step`): the engine sets every measured event's
clock frame (whether it owes a count and pays one, or self-creates: its age
advances by one and its turn is read off its clock, s = `by_clock(age,
content x n, d)` phase steps at the clock's rate `K` = [n, d], an integer K
being [1, K] (`NatureBeamWorld.turn`, the free release's own form; the four
unifications (2), 2026-09-20), refused at half the circle), calls `nature_beam`
once for the whole GameBoard (the walk, the readings, the collision, the tables
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
initial + measured = current + spent + escaped; the transit line, in amount,
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

from event_universe.core.game_board import Address3, adjacent_node
from event_universe.core.integer import apportion_whole, by_clock, by_drive
from event_universe.events.amplitude import Layer
from event_universe.events.measured import TALLIES, DetectorSet, Ledger, Measured, rational_sum
from event_universe.events.nature_beam import (
    NO_ARRIVAL,
    NO_BRANCH,
    NO_RECORD,
    ONE_PATH,
    ArrivalRows,
    GameBoardDiagnostics,
    NatureBeamStore,
    NatureBeamTables,
    Record,
    bounded,
    by_clock_rows,
    exact_column_sums,
    exact_sum,
    momentum_labels,
    nature_beam,
    nature_beam_tables,
)
from event_universe.events.world import (
    BEAM_LAW,
    BINDING_RULE,
    CONTACT_DEFAULT,
    DETECTOR_READINGS,
    FACE_NAMES,
    LIFETIME_NAME,
    MOMENTUM_BOUND,
    NO_CHARGE,
    NO_HAND,
    MeasuredDefinition,
    NatureBeamWorld,
    body_nodes,
    step_divisor,
)

__all__ = ["TALLIES", "Measured", "NatureBeamSimulation", "count_owed", "step_axis"]


def step_axis(drive: int, momentum: int, content: int, width: int) -> tuple[int | None, int]:
    """The step rule of one axis (BEAM_LAW section 3 step 5 and note 17 as
    amended on 2026-09-20, the step drive; `_move` calls it): the sign of
    the Link a free measured event of content M = `content` steps this
    self-creation on an axis whose momentum component is p = `momentum`,
    and the drive after it. The drive is the SIGNED distance the momentum
    has driven since the last step, in label units, on the body's own
    record: `drive + p` is compared with D = Q x S x M + |p|, S the
    world's `width`; at or beyond +D the body steps one Link on the axis's
    + side and D is subtracted, at or beyond -D one Link on the - side and
    D is added, otherwise it waits (record 126 of 2026-09-20: the drive was
    |p| with the direction from the sign at the fire until then, so a
    momentum reversed by a hand-over discharged the distance driven toward
    the partner as a Link away). With a momentum of one sign the step
    fires exactly when `floor(n |p| / D)` increments over the
    self-creations n, the rule as it was (`by_clock(age - 1, |p|, D)`: the
    drive is the signed remainder of that division); under a changing
    momentum the Links made follow the momentum's signed history, a
    reversal first cancelling what was driven the other way, never two in
    one self-creation (one D is subtracted per self-creation; a residual
    earned at a larger momentum fires at the following self-creations,
    one Link each). A momentum of 0 never steps and leaves the drive as it
    is. The count primitive is `core.integer.by_drive` (the model owner's
    record 108: the whole part of an accumulated rate on the reader's own
    record, `by_clock` where the rate is constant), with `at_most` 1: the
    step's own rule of one Link per interval, the residual of a larger
    momentum kept in the drive (the primitive's default since the
    fraction-free primitive of 2026-09-20 is the whole part, which no
    step may take: a body crosses one Link per interval); the one place
    the step rule lives, the readings tools read it from here. The
    divisor D is `world.step_divisor`, which the reading's weight at the
    relative speed reads too (note 38)."""
    if momentum == 0:
        return None, drive
    fired, drive = by_drive(drive, momentum, step_divisor(momentum, content, width), at_most=1)
    return (fired or None), drive


def count_owed(age: int, counted: int, suspension: tuple[int, int]) -> int:
    """The count a measured event owes after its self-creation (ENGINE,
    the frame; `_suspend` calls it): what its clock counted (`counted`, the
    presence or the age moment) times the width n / d of the world's
    `suspension`, off its clock, `by_clock(age, counted x n, d)` with `age`
    the age before the self-creation; 0 when the width is 0. The same
    count as `by_drive` where the rate is constant (record 108): the owed
    count reads a rate no push changes and keeps the clock's form, as the
    release and the lamp do."""
    numerator, denominator = suspension
    if not numerator:
        return 0
    return by_clock(age, counted * numerator, denominator)


class NatureBeamSimulation:
    """One world of the Beam Law, stepped interval by interval."""

    def __init__(self, world: NatureBeamWorld, observer: Record | None = None) -> None:
        self.world = world
        self.record = observer
        self.tick = 0
        self.shape = world.shape
        self.families = world.families
        self._phased = [family.phase for family in world.families]
        count = len(world.families)
        self.tables: NatureBeamTables = nature_beam_tables(world)
        self.stores = [NatureBeamStore(world.shape) for _ in world.families]
        # The six headings of the direction table by (axis, sign): the
        # heading a refused body gives its carried paid content on is the
        # one opposite to its refused step (`_give`; the table always holds
        # the six, `world._direction_table`).
        self.headings: dict[tuple[int, int], int] = {}
        for index, vector in enumerate(world.directions):
            if sum(abs(component) for component in vector) == 1:
                axis = max(range(3), key=lambda a: abs(vector[a]))
                self.headings[(axis, 1 if vector[axis] > 0 else -1)] = index
        # The binding that costs content as a fact of the run: true at load
        # when a body holds a paid family (`world.binding`), and raised at
        # the first give otherwise (a body of a free family that took paid
        # content under `measure` gives it at its next contact); from then
        # on every `contact` record carries `given` and the run's record the
        # identity `binding-v1` (`hypotheses`).
        self.binding = world.binding
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
        # The index of the GameBoard's occupied Nodes: every Node of every
        # body to the set it belongs to (the set maps the Node to its
        # measured event, `DetectorSet.nodes`; `occupant`): a step onto any
        # of them is refused (the parser refused a shared Node).
        self.at: dict[Address3, DetectorSet] = {}
        for index, definition in enumerate(world.measured):
            entry = self._measured(index + 1, definition)
            self.measured[entry.number] = entry
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
                arrival=np.array([NO_ARRIVAL]),
                # A declared ray is a row of no record: it ends without an
                # offer under the amplitude key (a record is born by a lamp).
                record=np.array([NO_RECORD]),
                branch=np.array([NO_BRANCH]),
                multiplicity=np.array([ONE_PATH]),
                # The row's hand as declared, or its family's (`hand-v1`).
                hand=np.array([item.hand]),
            )
            self.transit_initial[item.family] += item.amount
            self.content_initial[item.family] += content * item.amount
        for store in self.stores:
            store.merge()
        # The running transit line of the momentum starts from the declared
        # rows, counted once.
        self.ledger.transit_momentum = self.recount()["momentum"]
        # The apparatus's layer (the amplitude law): the sets in the
        # design's order, the measured events outside every declared
        # detector by number, the declared detectors, the faces in Port
        # order and the border.
        self.layer: Layer | None = None
        keys: list[tuple[str, int]] = []
        names: list[str] = []
        declared = len(world.detectors)
        for detector_set in self.detector_sets[declared:]:
            keys.append(("set", detector_set.index))
            names.append(f"measured:{detector_set.numbers[0]}")
        for detector_set in self.detector_sets[:declared]:
            keys.append(("set", detector_set.index))
            names.append(str(detector_set.name))
        for port in self.open_faces:
            keys.append(("face", port))
            names.append(FACE_NAMES[port])
        if world.lifetimes:
            keys.append(("border", 0))
            names.append(LIFETIME_NAME)
        self.layer = Layer(
            names,
            keys,
            self.detector_sets,
            [family.name for family in world.families],
            world.phase_steps,
        )
        # The readings of the last interval (diagnostics, decomposed on
        # request): per family the arrivals per Node, their net flow, the
        # Links crossed per Port and the presence.
        self.readings = GameBoardDiagnostics(
            world.shape, self.tables.flight.labels, [ArrivalRows.empty() for _ in range(count)]
        )

    @property
    def arrived(self) -> list[np.ndarray]:
        return self.readings.arrived

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
        # What the event holds per family at the start: its amount under its
        # own family and what `held` declared of the others.
        held = list(definition.held) + [0] * (count - len(definition.held))
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
        # refused a body outside the GameBoard): the set's map takes them in
        # their fixed order, the engine's index the set.
        nodes = body_nodes(definition.position, definition.span, self.shape, self.world.periodic)
        assert nodes is not None
        for node in nodes:
            detector_set.nodes[node] = number
            self.at[node] = detector_set
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
            phase_by_momentum=definition.phase_by_momentum,
            column_names=tuple(name for name, _ in self.world.columns),
            family_values=tuple(family.values for family in self.families),
            pending=[[] for _ in range(count)],
            taken=[dict.fromkeys(TALLIES, 0) for _ in range(count)],
            clicks=[0] * count,
            contact=tuple(definition.contact) + (CONTACT_DEFAULT,) * (count - len(definition.contact)),
            contacts=[0] * count,
            widths=list(definition.widths),
            lamp_width=None if definition.lamp is None else definition.lamp.width,
            unit_charges=tuple(NO_CHARGE if f.free else f.charge for f in self.families),
            become=definition.become,
            transforms=list(definition.transforms),
            window_reads=tuple(definition.window_reads)
            + (None,) * (count - len(definition.window_reads)),
            splits=list(definition.splits) + [None] * (count - len(definition.splits)),
            lamp_turns=() if definition.lamp is None else definition.lamp.turns,
            lamp_branches=((0, 1),) if definition.lamp is None else definition.lamp.branches,
            lamp_arms=1 if definition.lamp is None else definition.lamp.arms,
            label_turns=list(definition.label_turns) + [0] * (count - len(definition.label_turns)),
            rotations=list(definition.rotations) + [None] * (count - len(definition.rotations)),
            gates=list(definition.gates) + [None] * (count - len(definition.gates)),
            # The hand (`hand-v1`): the axis, the entries' parity filters,
            # the lamp's hand (its own, or its family's) and the hands of
            # its labels.
            axis=definition.axis,
            hands=tuple(definition.hands) + (NO_HAND,) * (count - len(definition.hands)),
            lamp_hand=(
                NO_HAND
                if definition.lamp is None
                else (definition.lamp.hand or self.families[definition.family].hand)
            ),
            lamp_label_hands=None if definition.lamp is None else definition.lamp.label_hands,
        )

    def occupant(self, node: Address3) -> int | None:
        """The number of the measured event whose body holds the Node, None
        for a Node of free space: the engine's index to the set, the set's
        map to its event."""
        detector_set = self.at.get(node)
        return None if detector_set is None else detector_set.nodes[node]

    def _place(self, entry: Measured, nodes: tuple[Address3, ...]) -> None:
        """The body's Nodes moved to `nodes` (in their fixed order) in its
        set's map and in the engine's index; an empty `nodes` removes it."""
        detector_set = entry.detector_set
        for node in entry.nodes:
            del detector_set.nodes[node]
            del self.at[node]
        for node in nodes:
            detector_set.nodes[node] = entry.number
            self.at[node] = detector_set

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
            layer=self.layer,
        )
        for number in sorted(self.measured):
            entry = self.measured[number]
            if entry.creating:
                entry.phase = (entry.phase + entry.turn) & self.world.phase_mask
                entry.turned += entry.turn
                self._suspend(entry)
        for number in sorted(self.measured):
            if number in self.measured:
                self._move(self.measured[number])

    def inverse_step(self) -> None:
        """The inverse interval on a GameBoard without measured events: the
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
        read once into `frame_content` (M_A of the interval's push, BEAM_LAW
        step 4), its charge in every column into `frame_charges` (the
        reader's side of the push over the columns, gravity's the content)
        and its momentum into `frame_momentum` (the p_a of the reading's
        weight at the relative speed under `doppler`, note 38: the speed
        the body had over this interval, the same for every group of rays
        whatever the family order, as the charges are);
        one that owes a count pays it by one (no self-creation, no
        release, no turn; `waited` counts the interval); one that owes
        nothing self-creates: its age advances and its turn is read off its
        clock, `by_clock(age, content x n, d)` at the clock's rate [n, d]
        (`NatureBeamWorld.turn`; `by_clock_rows` over the phased events in
        one array where their products fit the register, the scalar
        `turn` row by row otherwise), and refused at half the circle."""
        phased: list[Measured] = []
        for entry in self.measured.values():
            entry.turn = 0
            # The content and the charges the frame reads, once, for the
            # turn and for the push of this interval (M_A and the columns'
            # E_c at the frame: the clicks of the interval join `held`
            # after it).
            entry.frame_content = entry.content
            entry.frame_charges = entry.charges(for_push=True)
            entry.frame_momentum = list(entry.momentum)
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
        numerator, denominator = self.world.turn_rate
        ages = [entry.clock_age for entry in phased]
        contents = [entry.frame_content for entry in phased]
        if (max(ages) + 1) * max(contents) * numerator <= MOMENTUM_BOUND:
            turns = by_clock_rows(
                np.array(ages, dtype=np.int64),
                np.array(contents, dtype=np.int64) * numerator,
                denominator,
            ).tolist()
        else:
            turns = [self.world.turn(age, content) for age, content in zip(ages, contents, strict=True)]
        for entry, turn in zip(phased, turns, strict=True):
            if 2 * turn >= self.world.phase_steps:
                raise ValueError(
                    f"{BEAM_LAW}: measured event {entry.number} turns its phase by half the circle "
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
        """The step by the momentum, at most one per interval, when nothing
        is owed: on an axis whose momentum component is p (in label units),
        one Link per (Q x S x M + p) / p self-creations, since 2026-09-20 by
        the step drive (`step_axis`, BEAM_LAW note 17 as amended: the
        body's record carries per axis the distance the momentum has
        driven since its last step, and at a constant momentum the same
        self-creations as `by_clock(age, |p|, Q x S x M + |p|)`), with M
        the content, S the world's `width` (the model owner's D1 of
        2026-09-19) and Q = 64 the
        label's scale (the physics-rule reviewer's correction 2 of the
        label along the unit vector, 2026-09-19: the width in units of one
        free unit's label, Q x M, so that one unit of net flow gives the
        speed 1 / (S + 1) for every content and every step registered
        before the change is the same, `by_clock(age, Q n, Q k) =
        by_clock(age, n, k)`); the drive of every axis advances at every
        self-creation in which the body may step, the first axis whose
        rule fires makes the step, and a later axis's coincident fire is
        lost, its D subtracted, nothing carried (the frame's rule as it
        was). A step onto a measured event is refused and is
        a contact read through the occupant's table (`_contact`); an
        escape is a click on the face; a periodic axis wraps.

        A body on a set of Nodes (`span`; the model owner, 2026-09-20)
        steps as one: its centre moves one Link and its set with it, the
        step refused when any Node of the moved set holds another measured
        event, the whole body clicking on the face detector when any of
        its Nodes would leave the GameBoard through an open face, every Node
        wrapping on a periodic axis.

        The turn by momentum (`phase_by_momentum` with the world's
        `action`, h; the model owner's decision of 2026-09-20 on Bohr, "put
        it as parameters outside the GameBoard like the age"): a rule of the
        measured event, the external thing, read from its own record. At
        the Link the body steps on an axis whose momentum component is p,
        its phase turns by the difference of two floors,

            floor(k1 x |p| x N / h) - floor(k0 x |p| x N / h),

        with k0 the count of the step rule's fires on that axis before this
        one (the record's `axis_steps` less one, a lost or refused step
        counted; at a constant momentum floor((age - 1) x |p| / (Q S M +
        |p|)), the count the rule gave at the age before this
        self-creation) and k1 = k0 + 1 the count after it (with a constant
        momentum k1 is the Links
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
        # The drive of every axis advances at this self-creation; the first
        # axis whose rule fires makes the step, and a fire on a later axis
        # in the same self-creation is lost (its D subtracted, no Link
        # crossed, the rule's count `axis_steps` raised): the frame's rule
        # as it was, one Link per interval, x before y before z.
        fired: tuple[int, int, int] | None = None
        for axis in range(3):
            momentum = entry.momentum[axis]
            stepped, entry.drive[axis] = step_axis(
                entry.drive[axis], momentum, content, self.world.width
            )
            if stepped is None:
                continue
            entry.axis_steps[axis] += 1
            if fired is None:
                fired = (axis, momentum, stepped)
        if fired is None:
            return
        axis, momentum, sign = fired
        magnitude = abs(momentum)
        entry.steps += 1
        origin = entry.position
        port = 2 * axis + (0 if sign > 0 else 1)
        destination = adjacent_node(origin, port, self.shape, self.world.periodic)
        if destination == origin:
            return
        # The moved set: None when the centre or any Node of the body
        # would leave the GameBoard through an open face (the escape).
        nodes = (
            None
            if destination is None
            else body_nodes(destination, entry.span, self.shape, self.world.periodic)
        )
        if destination is None or nodes is None:
            for index in range(len(self.families)):
                self.ledger.held_escaped[index] += entry.held[index]
                self.ledger.units_escaped[index] += entry.clicks[index]
                # What waits to be created again leaves with the body:
                # the home and re-released rows off the absorbed line,
                # the products of a transformation (never absorbed) on
                # the released line, all of them on the face.
                thrown_amount = entry.pending_thrown_amount(index)
                thrown_content = entry.pending_thrown_content(index)
                self.ledger.transit_absorbed[index] -= entry.pending_amount(index) - thrown_amount
                self.ledger.transit_released[index] += thrown_amount
                self.ledger.content_absorbed[index] -= entry.pending_content(index) - thrown_content
                self.ledger.content_released[index] += thrown_content
                self.ledger.face_measured_content[port][index] += entry.held[index]
                self.ledger.face_amount[port][index] += entry.pending_amount(index)
                self.ledger.face_content[port][index] += entry.pending_content(index)
            self.ledger.face_momentum[port][entry.family] = [
                int(a) + int(b)
                for a, b in zip(
                    self.ledger.face_momentum[port][entry.family], entry.momentum, strict=True
                )
            ]
            self._place(entry, ())
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
                        "home_content": [entry.pending_content(f) for f in range(len(self.families))],
                    }
                )
            return
        found = {self.occupant(node) for node in nodes}
        occupants = sorted(number for number in found if number not in (None, entry.number))
        if occupants:
            self._contact(entry, axis, sign, origin, destination, occupants)
            return
        self._place(entry, nodes)
        entry.position = destination
        if entry.phase_by_momentum and self.world.action is not None:
            # k0, the Links stepped on this axis before this one: the
            # step rule's count, read off the body's record since the
            # step drive (the same count as the floor at a constant
            # momentum).
            links = entry.axis_steps[axis] - 1
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
                    "drive": list(entry.drive),
                }
            )
        return

    def _contact(
        self,
        entry: Measured,
        axis: int,
        step: int,
        origin: Address3,
        destination: Address3,
        occupants: list[int],
    ) -> None:
        """The contact through the table (the model owner, 2026-09-20, on
        the physicist's design of the strong force, section 4.4): a body
        whose step on an axis is refused because the destination holds
        another measured event has arrived at that occupant, and the
        occupant's table entry for the body's family decides, as it decides
        for a ray (`Measured.contact`): `measure` hands the body's momentum
        component on that axis to the occupant (the body's 0, the
        occupant's raised by it: what a click takes, kappa = 1, the body's
        momentum being its own label); `rerelease` returns it (the body's
        component reversed, the occupant's raised by twice it: what a
        mirror does); `read` and `pass` leave the step refused and the
        labels as they are (the rule as it was until 2026-09-20: the two
        bodies where they were, the component accumulating on the body
        under every push until the integer bound refuses the run; a world
        that wants it declares the rule). Where the entry is the keys' own
        rule for the body's family (declared or not: an entry equal to the
        default changes nothing) the contact is `measure`: a body arriving
        at a body is a paid arrival, its momentum its own label, and the
        keys' rule for a paid arrival is `measure` (`world.CONTACT_DEFAULT`);
        so `read` on a free family, the keys' own, is the hand-over, and
        `read` declared on a paid family the accumulation.
        The sum of the momenta on the measured events is unchanged by a
        hand-over (a transfer from one line to another; the books'
        measured momentum line is their sum), each label bounded by what
        one push accumulates between attempts. A body on a set of Nodes
        whose destination set holds several occupants hands the component
        apportioned whole over them by their contents
        (`apportion_whole`, the units left to the largest remainders, ties
        from the body's age modulo their count, in number order); an
        occupant of content 0 takes nothing. One `contact` record per
        occupant that took a hand-over (the tick, the body's number, its
        Node and the destination, the occupant, the body's family, the
        rule, the axis and the signed component the occupant gained); no
        record under `read` or `pass`. Local (the destination Node is read
        by the step already; the transfer crosses one Link in one
        interval, as a ray's step does), fixed work (one entry per
        occupant of the destination set), the steps the frame's, outside
        the walk and the collision.

        The binding that costs content (`binding-v1`, the model owner's
        record 115 of 2026-09-20 and the physicist's design, BEAM_LAW note
        40): at the first hand-over under `measure` of a contact the
        refused body also GIVES the paid content it carries to the flight
        (`_give`), once per contact, whole, on the heading opposite to the
        refused step (`step`, the sign of the Link the drive fired on that
        axis: under the signed drive of record 126 the momentum's sign can
        differ from the step's at a reversal, and the heading is the step's);
        a body that carries none gives nothing and the contact is the
        hand-over alone, bit for bit. The `contact` record then carries
        `given` (the content given at this hand-over, 0 on a later one)
        from the moment the run holds the fact (`binding`: at load when a
        body holds a paid family, else from the first give on); before it
        the record is as it was."""
        component = entry.momentum[axis]
        magnitude = abs(component)
        if magnitude == 0:
            return
        sign = 1 if component > 0 else -1
        contents = [self.measured[number].content for number in occupants]
        shares = apportion_whole(magnitude, contents, entry.age % len(occupants))
        family = self.families[entry.family].name
        gave = False
        for number, share in zip(occupants, shares, strict=True):
            occupant = self.measured[number]
            rule = occupant.contact[entry.family]
            if rule == "measure":
                handed = sign * share
            elif rule == "rerelease":
                handed = 2 * sign * share
            else:
                continue
            if handed == 0:
                continue
            occupant.momentum[axis] = bounded(occupant.momentum[axis] + handed, occupant, "momentum")
            entry.momentum[axis] = bounded(entry.momentum[axis] - handed, entry, "momentum")
            occupant.contacts[entry.family] += 1
            given = 0
            if rule == "measure" and not gave:
                gave = True
                given = self._give(entry, axis, step, origin)
            if self.record is not None:
                line: dict[str, object] = {
                    "event": "contact",
                    "tick": self.tick,
                    "number": entry.number,
                    "node": list(origin),
                    "to": list(destination),
                    "occupant": number,
                    "family": family,
                    "rule": rule,
                    "axis": axis,
                    "component": handed,
                }
                if self.binding:
                    line["given"] = given
                line["momentum"] = list(entry.momentum)
                self.record(line)

    def _give(self, entry: Measured, axis: int, step: int, origin: Address3) -> int:
        """The give of the binding that costs content (`binding-v1`; the
        model owner's record 115 of 2026-09-20, the physicist's design
        docs/designs/binding_v1/DESIGN.md section 1, candidate A; BEAM_LAW
        note 40): at a contact under `measure` the refused body gives to
        the flight the content it carries of every paid family other than
        its own (`held`; a lamp's own content is not carried), per such
        family with the quantum h `held // h` units of content h as one row
        (age 0, the body's phase and number, no record) at the body's Node
        on the heading opposite to the refused step (`step`, the sign of
        the Link the step fired on the axis), away from the occupant;
        `held mod h` stays held. The body's held content of the
        family falls by the content given, booked on the family's `spent`
        line as a lamp's release is, and the row on the transit and content
        lines (`released`) and on the transit momentum line; the body takes
        the recoil, minus the row's label (Q x content per unit along the
        heading, the one label of the law, checked before it is formed:
        `momentum_labels`), toward the occupant. The rows then have the
        law's fates by the tables and the border: the border `lifetime`
        clicks them with their content (the released binding energy), a
        body on their line takes them under the keys' `measure`. Returns
        the content given, summed over the families (0 for a body that
        carries none: nothing happens). Local (the giver's own held content
        and the heading of its own refused step; the row crosses one Link
        per interval), fixed work (one row per paid family carried), the
        division by h exact with its remainder held, every intermediate
        bounded."""
        direction = self.headings[(axis, -step)]
        given = 0
        for family, definition in enumerate(self.families):
            if definition.free or family == entry.family:
                continue
            units = entry.held[family] // definition.quantum
            if units == 0:
                continue
            content = units * definition.quantum
            store = self.stores[family]
            direction_column = np.array([direction], dtype=np.int64)
            amount_column = np.array([units], dtype=np.int64)
            content_column = np.array([definition.quantum], dtype=np.int64)
            labels = momentum_labels(
                self.tables.flight.labels, direction_column, amount_column, content_column, False, origin
            )
            born = exact_column_sums(labels)
            entry.momentum = [
                bounded(a - b, entry, "momentum") for a, b in zip(entry.momentum, born, strict=True)
            ]
            entry.held[family] -= content
            self.ledger.held_spent[family] += content
            self.ledger.content_released[family] += content
            self.ledger.transit_released[family] += units
            self.ledger.transit_momentum = [
                a + b for a, b in zip(self.ledger.transit_momentum, born, strict=True)
            ]
            store.append(
                node=np.array([store.flat(origin)], dtype=np.int64),
                direction=direction_column,
                age=np.zeros(1, dtype=np.int64),
                phase=np.array([entry.phase], dtype=np.int64),
                number=np.array([entry.number], dtype=np.int64),
                amount=amount_column,
                content=content_column,
                arrival=np.array([NO_ARRIVAL], dtype=np.int64),
                record=np.array([NO_RECORD], dtype=np.int64),
                branch=np.array([NO_BRANCH], dtype=np.int64),
                multiplicity=np.array([ONE_PATH], dtype=np.int64),
            )
            given += content
        if given:
            self.binding = True
        return given

    @property
    def hypotheses(self) -> list[str]:
        """The identities of the physical hypotheses the run carries: the
        world's at load (`NatureBeamWorld.hypotheses`) and `binding-v1` once
        a body gave paid content it took during the run (`binding`, the
        run-time fact; the parser knows only what is held at load)."""
        found = list(self.world.hypotheses)
        if self.binding and BINDING_RULE not in found:
            found.append(BINDING_RULE)
        return found

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
        # The `cancelled` and `remainder` lines are written in a recorded
        # world alone (a lamp declared): a world without a lamp has no
        # record and no line.
        amplitude = self.world.recorded
        handed = self.world.handed
        # One pass over the measured events: what they hold per family,
        # their momentum and their charge (rho x content of the free
        # families and, since 2026-09-20 (D-1), the paid families' whole
        # charge per unit of amount times the units held; the sum an exact
        # rational reported as the reduced pair [n, d]). The charge line
        # adds the paid rows in transit and the paid units escaped, so that
        # it is conserved through a click, a home, an escape and a
        # transformation; a world without a charged paid family reads the
        # same pair as before.
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
                # The content that entered the family's line by
                # transformations (the weak force, 2026-09-20): positive
                # into the family become, negative out of the family left.
                "became": ledger.held_became[index],
                "current": held_current[index],
                "spent": ledger.held_spent[index],
                "escaped": ledger.held_escaped[index],
            }
            measured["balanced"] = measured["initial"] + measured["measured"] + measured["became"] == (
                measured["current"] + measured["spent"] + measured["escaped"]
            )
            if handed:
                # The `left` and `right` lines (`hand-v1`): the units the
                # tables clicked of each hand, a report; only where a hand
                # is declared, as the amplitude columns are.
                measured["left"] = ledger.taken_left[index]
                measured["right"] = ledger.taken_right[index]
            in_transit = {
                "initial": self.transit_initial[index],
                "released": ledger.transit_released[index],
                "current": (
                    counted["transit"][index]
                    if counted is not None
                    else self.transit_initial[index]
                    + ledger.transit_released[index]
                    - ledger.escaped_amount(index)
                    - ledger.transit_absorbed[index]
                    - ledger.cancelled_amount[index]
                ),
                "escaped": ledger.escaped_amount(index),
                "absorbed": ledger.transit_absorbed[index],
            }
            # The `cancelled` line (the amplitude law): what the merge's
            # cancel removed, on the transit and content lines under the key
            # only (zero without it, the lines as they were).
            if amplitude:
                in_transit["cancelled"] = ledger.cancelled_amount[index]
            in_transit["balanced"] = in_transit["initial"] + in_transit["released"] == (
                in_transit["current"]
                + in_transit["escaped"]
                + in_transit["absorbed"]
                + ledger.cancelled_amount[index]
            )
            if not family.free and family.charge[0]:
                charges.append((family.charge[0] * int(in_transit["current"]), 1))
                charges.append(
                    (family.charge[0] * (ledger.escaped_amount(index) + ledger.units_escaped[index]), 1)
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
                    - ledger.cancelled_content[index]
                ),
                "escaped": ledger.escaped_content(index),
                "absorbed": ledger.content_absorbed[index],
            }
            if amplitude:
                content["cancelled"] = ledger.cancelled_content[index]
            content["balanced"] = content["initial"] + content["released"] == (
                content["current"]
                + content["escaped"]
                + content["absorbed"]
                + ledger.cancelled_content[index]
            )
            balanced = (
                balanced
                and bool(measured["balanced"])
                and bool(in_transit["balanced"])
                and bool(content["balanced"])
            )
            lines: dict[str, object] = {
                "measured": measured,
                "transit": in_transit,
                "content": content,
                # The `turned` line (the meeting, 2026-09-20): what the turns
                # of the family's units in transit moved the transit momentum
                # line by, a report as `pushed` is; zero without `meeting`.
                "turned": list(ledger.turned_momentum[index]),
            }
            if amplitude:
                # The labels the cancel removed from the transit momentum line.
                lines["cancelled"] = list(ledger.cancelled_momentum[index])
                # The labels of a record's rows beyond the shares matter took
                # (the push by share, stage (vii) step 3).
                lines["remainder"] = list(ledger.remainder_momentum[index])
            families[family.name] = lines
        momentum: dict[str, object] = {
            "measured": held_momentum,
            "transit": counted["momentum"] if counted is not None else self.transit_momentum(),
            "escaped": ledger.escaped_momentum(),
            "turned": ledger.turned_momentum_total(),
        }
        if amplitude:
            momentum["cancelled"] = ledger.cancelled_momentum_total()
            momentum["remainder"] = ledger.remainder_momentum_total()
        return {
            "tick": self.tick,
            "families": families,
            "momentum": momentum,
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
        detectors, one per open face of the GameBoard (`face_detectors`)."""
        found = []
        for index, detector in enumerate(self.world.detectors):
            detector_set = self.detector_sets[index]
            members = [self.measured[n] for n in detector_set.numbers if n in self.measured]
            families = {
                family.name: {
                    "measured": sum(entry.taken[f]["measure"] for entry in members),
                    "clicks": sum(entry.clicks[f] for entry in members),
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
        `momentum` that left; then, when a family declares a lifetime, the
        border `lifetime` with the same fields (no Nodes: the border is
        wherever an event's age reaches its family's lifetime)."""
        found: list[dict[str, object]] = []
        ledger = self.ledger
        if self.world.lifetimes:
            found.append(
                {
                    "name": LIFETIME_NAME,
                    "nodes": 0,
                    "threshold": 1,
                    "families": {
                        family.name: {
                            "measured": ledger.lifetime_amount[f],
                            "clicks": ledger.lifetime_amount[f],
                            "content": ledger.lifetime_content[f],
                            "record": ledger.lifetime_record[f],
                            "measured_content": 0,
                            "momentum": list(ledger.lifetime_momentum[f]),
                        }
                        for f, family in enumerate(self.families)
                    },
                    "momentum": ledger.lifetime_momentum_total(),
                }
            )
        for port in self.open_faces:
            axis = port >> 1
            nodes = 1
            for other in range(3):
                if other != axis:
                    nodes *= self.shape[other]
            found.insert(
                len(found) - (1 if self.world.lifetimes else 0),
                {
                    "name": FACE_NAMES[port],
                    "nodes": nodes,
                    "threshold": 1,
                    "families": {
                        family.name: {
                            "measured": ledger.face_amount[port][f],
                            "clicks": ledger.face_amount[port][f],
                            "content": ledger.face_content[port][f],
                            "record": ledger.face_record[port][f],
                            "measured_content": ledger.face_measured_content[port][f],
                            "momentum": list(ledger.face_momentum[port][f]),
                        }
                        for f, family in enumerate(self.families)
                    },
                    "momentum": ledger.face_momentum_total(port),
                },
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
        node_offsets = np.indices(self.shape).reshape(3, -1).T - np.array(centre)
        distance = np.sqrt((node_offsets * node_offsets).sum(axis=1))
        chosen = np.abs(distance - radius) < 0.5
        chosen &= distance > 0
        positions = node_offsets[chosen]
        radial = positions / distance[chosen][:, None]
        cells = tuple((positions + np.array(centre)).T)
        arrived = self.readings.arrived[family][cells]
        flow = self.readings.flow[family][cells]
        presence = self.readings.presence[family][cells]
        return {
            "nodes": float(chosen.sum()),
            "arrived": float(arrived.mean()),
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
            raise ValueError("cube_flux supports only the all-open GameBoard")
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
        yield "law", BEAM_LAW
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
                    "amount": self.ledger.escaped_amount(f),
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
        materialization of a ray's record (`NatureBeamStore.rows`, `NatureBeam`),
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
                beams = [beam.record_line(vectors, self.world.handed) for beam in store.rows(lo, hi)]
                families.append({"family": family.name, "rays": beams})
            yield entry
