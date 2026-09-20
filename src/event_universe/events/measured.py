"""The records the engine keeps beside the rays: a measured event and the
ledger. Records only, no law: the law of the ray is `nature_beam`, the frame
around it (the clocks, the steps, the books' identities) is `engine.py`.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from event_universe.core.game_board import Address3
from event_universe.core.integer import bounded_gcd
from event_universe.events.world import AGE_READS

RULES = ("home", "read", "measure", "rerelease")
# The component of the one reading a measured event's clock counts by
# default: the presence, the scalar over every ray at its Node of another
# number.
PRESENCE_READS = "scalar"
Pending = tuple[int, int, int]


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


def reduced(numerator: int, denominator: int) -> tuple[int, int]:
    """A rational as the pair (n, d) in lowest terms with d positive."""
    common = bounded_gcd(abs(numerator), denominator) or 1
    return numerator // common, denominator // common


def rational_sum(terms: list[tuple[int, int]]) -> tuple[int, int]:
    """The exact sum of rationals (n, d), reduced: a report of the books."""
    numerator, denominator = 0, 1
    for n, d in terms:
        numerator, denominator = reduced(numerator * d + n * denominator, denominator * d)
    return numerator, denominator


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
    its measured events took."""

    index: int
    name: str | None
    reading: str
    threshold: int
    numbers: list[int] = field(default_factory=list)
    record: list[int] = field(default_factory=list)
    phase: list[int | None] = field(default_factory=list)

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
    # The family's charge per unit of content, rho = (n, d): the event's
    # charge is rho x its content (`charge`, a report), and the electric
    # push reads rho and the content the frame read.
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
    # `position`, `nodes` the set itself (the engine keeps it as the body
    # steps), (1, 1, 1) and the one Node for a measured event of one Node;
    # `phase_by_momentum` whether the body turns its phase by its momentum
    # label at every Link it steps, over the world's `action` (the turn by
    # momentum, a rule of the measured event, the external thing).
    span: tuple[int, int, int] = (1, 1, 1)
    nodes: tuple[Address3, ...] = ()
    phase_by_momentum: bool = False
    age: int = 0
    owed: int = 0
    pending: list[list[Pending]] = field(default_factory=list)
    waited: int = 0
    phase_steps: int = 0
    steps: int = 0
    measured: list[dict[str, int]] = field(default_factory=list)
    events: list[int] = field(default_factory=list)
    pushed: list[int] = field(default_factory=lambda: [0, 0, 0])
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
    presence: int = 0
    counted: int = 0

    @property
    def content(self) -> int:
        return sum(self.held)

    @property
    def charge(self) -> tuple[int, int]:
        """The event's charge, rho x its content, as a reduced pair (n, d):
        a report (the model owner, 2026-09-20: charge is per unit of
        content of a family); the law reads rho and the content."""
        return reduced(self.rho[0] * self.content, self.rho[1])

    @property
    def threshold(self) -> int:
        """The threshold of the detector the event belongs to."""
        return self.detector_set.threshold

    def pending_amount(self, family: int) -> int:
        return sum(amount for amount, _, _ in self.pending[family])

    def pending_content(self, family: int) -> int:
        return sum(amount * content for amount, content, _ in self.pending[family])

    def state(self) -> dict[str, object]:
        return {
            "number": self.number,
            "position": list(self.position),
            "family": self.family,
            "held": list(self.held),
            "content": self.content,
            "phase": self.phase,
            "charge": list(self.charge),
            "momentum": list(self.momentum),
            "fixed": self.fixed,
            "span": list(self.span),
            "windows": list(self.windows),
            "detector": self.detector,
            "age": self.age,
            "owed": self.owed,
            "home": [self.pending_amount(f) for f in range(len(self.held))],
            "home_content": [self.pending_content(f) for f in range(len(self.held))],
            "waited": self.waited,
            "phase_steps": self.phase_steps,
            "steps": self.steps,
            "measured": [dict(entry) for entry in self.measured],
            "events": list(self.events),
            "pushed": list(self.pushed),
        }


@dataclass
class Ledger:
    """The cumulative books of a run, per family: the measured line (in
    content), the transit line (in units), the content line (the content
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
    face_units: dict[int, list[int]] = field(default_factory=dict)
    face_content: dict[int, list[int]] = field(default_factory=dict)
    face_measured_content: dict[int, list[int]] = field(default_factory=dict)
    face_record: dict[int, list[int]] = field(default_factory=dict)
    face_momentum: dict[int, list[int]] = field(default_factory=dict)

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
        ):
            setattr(self, name, [0] * count)
        for port in self.open_faces:
            self.face_units[port] = [0] * count
            self.face_content[port] = [0] * count
            self.face_measured_content[port] = [0] * count
            self.face_record[port] = [0] * count
            self.face_momentum[port] = [0, 0, 0]

    def escaped_units(self, family: int) -> int:
        return sum(self.face_units[port][family] for port in self.open_faces)

    def escaped_content(self, family: int) -> int:
        return sum(self.face_content[port][family] for port in self.open_faces)

    def escaped_momentum(self) -> list[int]:
        return [sum(self.face_momentum[port][axis] for port in self.open_faces) for axis in range(3)]
