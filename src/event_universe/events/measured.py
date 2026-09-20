"""The records the engine keeps beside the rays: a measured event and the
ledger. Records only, no law: the Beam Law is `nature_beam`, the frame
around it (the clocks, the steps, the books' identities) is `engine.py`.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from event_universe.core.game_board import Address3
from event_universe.core.integer import rational_sum, reduced
from event_universe.events.world import AGE_READS, BEAM_LAW, CHARGE_INDEX, MOMENTUM_BOUND

__all__ = [
    "TALLIES",
    "DetectorSet",
    "Ledger",
    "Measured",
    "column_charges",
    "count_component",
    "rational_sum",
    "reduced",
]
TALLIES = ("home", "read", "measure", "rerelease")
# The component of the one reading a measured event's clock counts by
# default: the presence, the scalar over every ray at its Node of another
# number.
PRESENCE_READS = "scalar"
Pending = tuple[int, int, int]
Pair = tuple[int, int]


def column_charges(
    held: list[tuple[tuple[Pair, ...], int]], columns: int, number: int, position: Address3
) -> list[Pair]:
    """A measured event's charge in every column from what it holds: per
    column c the exact rational sum over the families f held of n_f^c x
    M_f / d_f^c, the reduced pair (E, D) (`rational_sum`, the books' rule
    for the charge line since 2026-09-20). `held` lists, per family with a
    content, its aligned column values and its content M_f. The gravity
    column ((1, 1) on every family) sums to the content, (M, 1); the
    charge column is rho x M for a one-family event, the report it was.
    Each product n_f^c x M_f is checked before it is formed and a charge
    whose sum leaves the register refuses the run naming the measured
    event and the column."""
    charges: list[Pair] = []
    for column in range(columns):
        terms: list[Pair] = []
        for values, content in held:
            numerator, denominator = values[column]
            if not numerator or not content:
                continue
            if abs(numerator) > MOMENTUM_BOUND // content:
                raise OverflowError(
                    f"{BEAM_LAW}: the charge of measured event {number} at {list(position)} in "
                    f"column {column} ({numerator} per unit on the content {content}) exceeds the "
                    f"integer bound {MOMENTUM_BOUND}"
                )
            terms.append((numerator * content, denominator))
        try:
            charges.append(rational_sum(terms))
        except OverflowError as error:
            raise OverflowError(
                f"{BEAM_LAW}: the charge of measured event {number} at {list(position)} in column "
                f"{column} (the sum over the families held) exceeds the work register"
            ) from error
    return charges


def count_component(reads: str) -> str:
    """The component of the one reading a measured event's clock counts for
    a family, selected by its table entry's `reads` key: the age moment
    (`age`, sum amount x age over every ray of another number at its Node)
    on an entry that reads `age`, the presence (`scalar`) on every other
    entry, whose key names only what its record carries. A reading aid of
    the measured event, the external thing (the model owner, 2026-09-19,
    "it must be checked in the detector and not on the GameBoard"): it only
    helps the detector's computation of its count and changes nothing of
    the GameBoard; the GameBoard's rules (the flight, the collision) never read the
    age whole."""
    return AGE_READS if reads == AGE_READS else PRESENCE_READS


@dataclass
class DetectorSet:
    """A detector at run time: a set of measured events with ONE record (the
    model owner, 2026-09-19: a detector measuring three Nodes sees one
    electron that can be on any of the three; a click says "here, in one
    of these" and not which). A declared detector (`name` its name) or a
    measured event outside every declared detector, a detector of one Node
    (`name` None, the reading the default). `reading` is `wave` (the record
    the square of the coherent pointer of what the set clicked in an
    interval) or `beam` (the arriving rays paired by opposite phase over
    the set, the record the plain count of what clicked); `threshold` the
    smallest amount of a family arriving over the set in one interval that
    the set responds to; `numbers` its measured events; `record` per
    family, cumulative: an exact Python integer, a report of the host that
    is never refused and may pass 2^63 (its readers in `run.json` and
    `state.json` parse it as an arbitrary-precision integer); `phase` per
    family the set's phase at its last click (None before one), the phase
    its measured events took; `nodes` the set's Nodes, each mapped to the
    number of the measured event there (the four unifications, the model
    owner, 2026-09-20, (3): one set object shared by a body and a
    detector, the data only: a body on a set of Nodes is a set with one
    measured event, a detector a set with several, each with one record,
    one phase and the map of its Nodes to its measured events, the one
    reading summed over the set in both; the engine keeps the map as a
    body steps, inserting a body's Nodes in their fixed order, x, then
    y, then z ascending, so `Measured.nodes` reads them from it)."""

    index: int
    name: str | None
    reading: str
    threshold: int
    numbers: list[int] = field(default_factory=list)
    record: list[int] = field(default_factory=list)
    phase: list[int | None] = field(default_factory=list)
    nodes: dict[Address3, int] = field(default_factory=dict)

    @property
    def wave(self) -> bool:
        return self.reading == "wave"


@dataclass
class Measured:
    """A measured event at a Node: its declaration, its clock and its
    counters. `pending` holds, per family, what came home or is re-released
    and waits for the next self-creation: (amount, content per unit, phase)
    per arriving record. `detector_set` is the detector the event belongs
    to (a declared one, or itself as a detector of one Node): the threshold
    and the record are the set's, not the Node's. The engine
    sets `creating`, `clock_age` and
    `turn` before every interval (the clock's frame) and reads `counted`
    after it (the clock's count: per family the component its table entry
    selects, `count_component`, the presence or the age moment, summed
    over the families; `presence` is the presence alone, reported)."""

    number: int
    position: Address3
    family: int
    held: list[int]
    phase: int
    # The family's charge per unit of content, rho = (n, d), the value of
    # its `charge` column; the event's charge in every column is read from
    # what it holds (`charges`: the `charge` column's pair is `charge`, a
    # report) and the push reads the charges the frame read.
    rho: tuple[int, int]
    momentum: list[int]
    fixed: bool
    directions: tuple[int, ...]
    table: tuple[str, ...]
    windows: list[int | None]
    reads: tuple[str, ...]
    lamp_rate: tuple[int, int] | None
    lamp_directions: tuple[int, ...]
    lamp_window: int | None
    declared_content: int
    detector: int | None
    detector_set: DetectorSet
    # A body on a set of Nodes (the model owner, 2026-09-20, "the electron
    # of width 3"): `span` the three odd extents of the block centred on
    # `position`, (1, 1, 1) for a measured event of one Node; the set
    # itself is the body's `detector_set` (`nodes` reads the body's Nodes
    # from its map; the engine keeps the map as the body steps);
    # `phase_by_momentum` whether the body turns its phase by its momentum
    # label at every Link it steps, over the world's `action` (the turn by
    # momentum, a rule of the measured event, the external thing).
    span: tuple[int, int, int] = (1, 1, 1)
    phase_by_momentum: bool = False
    # The world's columns (their names, gravity first, charge second) and
    # every family's aligned values per unit of content, (n, d) per column:
    # what the event's charges are read from (`charges`).
    column_names: tuple[str, ...] = ()
    family_values: tuple[tuple[Pair, ...], ...] = ()
    # The width of each entry's window in steps (`phase_width`, per family;
    # None where none is declared: the half circle N / 2) and the lamp's.
    widths: list[int | None] = field(default_factory=list)
    lamp_width: int | None = None
    # Every family's whole charge per unit of amount (D-1, 2026-09-20): the
    # paid family's declared `charge`, (0, 1) for a free family, whose
    # charge is per unit of content and enters the columns instead. Read by
    # `charges` for the charge line of the books and the report, never by
    # the push (`charges(for_push=True)` leaves it out).
    unit_charges: tuple[Pair, ...] = ()
    age: int = 0
    owed: int = 0
    pending: list[list[Pending]] = field(default_factory=list)
    waited: int = 0
    turned: int = 0
    steps: int = 0
    taken: list[dict[str, int]] = field(default_factory=list)
    clicks: list[int] = field(default_factory=list)
    pushed: list[int] = field(default_factory=lambda: [0, 0, 0])
    # The contact through the table (2026-09-20): per family the rule by
    # which this event reads a body of that family whose step onto it is
    # refused (`measure` hands the body's component on the axis of the
    # step to this event, `rerelease` returns it, `pass` and a `read`
    # declared against the keys leave the labels as they are), and per
    # family the hand-overs taken.
    contact: tuple[str, ...] = ()
    contacts: list[int] = field(default_factory=list)
    # The interval's frame, set by the engine: whether this interval is a
    # self-creation, the age before it, the turn read off the clock and the
    # content the frame read (`frame_content`, M_A of the push: taken once
    # before the law's step 4, so the push of an interval is independent of
    # the order in which the families' clicks join `held` within it; the
    # orchestrator's D1 on the architect's B3, 2026-09-20); and what the
    # law read back: the presence at the Node of every other number.
    creating: bool = False
    clock_age: int = 0
    turn: int = 0
    frame_content: int = 0
    frame_charges: list[Pair] = field(default_factory=list)
    presence: int = 0
    counted: int = 0

    @property
    def content(self) -> int:
        return sum(self.held)

    @property
    def nodes(self) -> tuple[Address3, ...]:
        """The set of Nodes the measured event is a body on, in the fixed
        order of the set (x, then y, then z ascending: the order the
        releases are apportioned in), read from its detector set's map
        (the one set object of a body and a detector, the four
        unifications (3))."""
        return tuple(node for node, number in self.detector_set.nodes.items() if number == self.number)

    def units(self, family: int) -> int:
        """The units of a paid family the event holds: the units it clicked
        (`clicks`) and the units waiting to be created again (`pending`:
        what came home, is re-released or is a product of a
        transformation). Its charge in the `charge` column is their count
        times the family's whole charge per unit of amount (D-1)."""
        return self.clicks[family] + self.pending_amount(family)

    def charges(self, for_push: bool = False) -> list[Pair]:
        """The event's charge in every column of the world, from what it
        holds (`column_charges`): the reduced pair (E, D) per column,
        gravity first (the content, (M, 1)), charge second (rho x M over
        the free families held, the report of 2026-09-20, plus since
        2026-09-20 the paid families' whole charge per unit of amount times
        the units held, D-1), the declared columns after. The frame reads
        it once per interval into `frame_charges` with `for_push`, the
        reader's side of the push (`nature_beam.push_form`), which leaves
        the paid units out: the charge of a measured event is rho times
        its content for a free family and the declared whole charge times
        the amount for a paid family, and the push reads only the former."""
        charges = column_charges(
            [
                (self.family_values[family], content)
                for family, content in enumerate(self.held)
                if content
            ],
            len(self.column_names),
            self.number,
            self.position,
        )
        if for_push or not self.unit_charges:
            return charges
        terms = [
            (numerator * self.units(family), denominator)
            for family, (numerator, denominator) in enumerate(self.unit_charges)
            if numerator and self.units(family)
        ]
        if terms:
            charges[CHARGE_INDEX] = rational_sum([charges[CHARGE_INDEX], *terms])
        return charges

    @property
    def charge(self) -> Pair:
        """The event's charge in the `charge` column, rho x its content as
        a reduced pair (n, d): a report (the model owner, 2026-09-20:
        charge is per unit of content of a family)."""
        return self.charges()[CHARGE_INDEX]

    @property
    def threshold(self) -> int:
        """The threshold of the detector the event belongs to."""
        return self.detector_set.threshold

    def pending_amount(self, family: int) -> int:
        return sum(amount for amount, _, _ in self.pending[family])

    def pending_content(self, family: int) -> int:
        return sum(amount * content for amount, content, _ in self.pending[family])

    def state(self) -> dict[str, object]:
        charges = self.charges()
        return {
            "number": self.number,
            "position": list(self.position),
            "family": self.family,
            "held": list(self.held),
            "content": self.content,
            "phase": self.phase,
            "charge": list(charges[CHARGE_INDEX]),
            # The charge in every column by name (the columns of 2026-09-20).
            "charges": {name: list(pair) for name, pair in zip(self.column_names, charges, strict=True)},
            "momentum": list(self.momentum),
            "fixed": self.fixed,
            "span": list(self.span),
            "windows": list(self.windows),
            "widths": list(self.widths),
            "detector": self.detector,
            "age": self.age,
            "owed": self.owed,
            "home": [self.pending_amount(f) for f in range(len(self.held))],
            "home_content": [self.pending_content(f) for f in range(len(self.held))],
            "waited": self.waited,
            "phase_steps": self.turned,
            "steps": self.steps,
            "measured": [dict(entry) for entry in self.taken],
            "events": list(self.clicks),
            "pushed": list(self.pushed),
            "contacts": list(self.contacts),
        }


@dataclass
class Ledger:
    """The cumulative books of a run, per family: the measured line (in
    content), the transit line (in amount), the content line (the content
    carried) and the momentum escaped; the face detectors' tallies per open
    face and family (the escaped lines are their sums); and the running
    transit line of the momentum, `transit_momentum`, the one label of
    every row in the stores, kept as the rows come and go (born, escaped,
    home, absorbed; the collision and the merge conserve it) so that the
    books need no pass over the store. The engine owns the identities;
    `nature_beam` adds what the interval moved."""

    families: int
    open_faces: tuple[int, ...]
    transit_momentum: list[int] = field(default_factory=lambda: [0, 0, 0])
    held_measured: list[int] = field(default_factory=list)
    held_spent: list[int] = field(default_factory=list)
    held_escaped: list[int] = field(default_factory=list)
    transit_released: list[int] = field(default_factory=list)
    transit_absorbed: list[int] = field(default_factory=list)
    content_released: list[int] = field(default_factory=list)
    content_absorbed: list[int] = field(default_factory=list)
    face_amount: dict[int, list[int]] = field(default_factory=dict)
    face_content: dict[int, list[int]] = field(default_factory=dict)
    face_measured_content: dict[int, list[int]] = field(default_factory=dict)
    face_record: dict[int, list[int]] = field(default_factory=dict)
    # The momentum that left through each face, per family (since
    # 2026-09-20, issue #360: the escaped line of the books is reported per
    # family; until then one vector per face and the world's total written
    # into every family's line).
    face_momentum: dict[int, list[list[int]]] = field(default_factory=dict)
    # The border `lifetime` (the model owner, 2026-09-20: an event in
    # transit whose age reaches its family's lifetime makes no next event
    # but a click on the border), booked as a face books an escape: per
    # family the amount, the content, the record and the momentum.
    lifetime_amount: list[int] = field(default_factory=list)
    lifetime_content: list[int] = field(default_factory=list)
    lifetime_record: list[int] = field(default_factory=list)
    lifetime_momentum: list[list[int]] = field(default_factory=list)
    # The units a measured event had clicked when it left the GameBoard
    # through a face, per family (D-1, 2026-09-20): their charge stays on
    # the charge line as escaped, with the rows that left.
    units_escaped: list[int] = field(default_factory=list)

    def __post_init__(self) -> None:
        count = self.families
        for name in (
            "held_measured",
            "held_spent",
            "held_escaped",
            "transit_released",
            "transit_absorbed",
            "content_released",
            "content_absorbed",
            "lifetime_amount",
            "lifetime_content",
            "lifetime_record",
            "units_escaped",
        ):
            setattr(self, name, [0] * count)
        self.lifetime_momentum = [[0, 0, 0] for _ in range(count)]
        for port in self.open_faces:
            self.face_amount[port] = [0] * count
            self.face_content[port] = [0] * count
            self.face_measured_content[port] = [0] * count
            self.face_record[port] = [0] * count
            self.face_momentum[port] = [[0, 0, 0] for _ in range(count)]

    def escaped_amount(self, family: int) -> int:
        """What left the GameBoard: through the open faces and on the border
        `lifetime`."""
        faces = sum(self.face_amount[port][family] for port in self.open_faces)
        return faces + self.lifetime_amount[family]

    def escaped_content(self, family: int) -> int:
        faces = sum(self.face_content[port][family] for port in self.open_faces)
        return faces + self.lifetime_content[family]

    def escaped_momentum(self, family: int | None = None) -> list[int]:
        """The momentum that left the GameBoard, through the open faces and
        on the border `lifetime`: one family's (since 2026-09-20), or the
        world's total over the families (None)."""
        rows = range(self.families) if family is None else (family,)
        return [
            sum(self.face_momentum[port][f][axis] for port in self.open_faces for f in rows)
            + sum(self.lifetime_momentum[f][axis] for f in rows)
            for axis in range(3)
        ]

    def face_momentum_total(self, port: int) -> list[int]:
        """The momentum that left through one face, summed over the families."""
        return [
            sum(self.face_momentum[port][f][axis] for f in range(self.families)) for axis in range(3)
        ]

    def lifetime_momentum_total(self) -> list[int]:
        """The momentum that left on the border `lifetime`, summed over the families."""
        return [sum(self.lifetime_momentum[f][axis] for f in range(self.families)) for axis in range(3)]
