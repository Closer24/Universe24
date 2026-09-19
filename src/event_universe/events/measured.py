"""The records the engine keeps beside the rays: a measured event and the
ledger. Records only, no law: the law of the ray is `nature_beam`, the frame
around it (the clocks, the steps, the books' identities) is `engine.py`.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from event_universe.core.lattice import Address3

RULES = ("home", "read", "measure", "rerelease")
# The face detectors, one per open face of the board, named by the face in
# Port order (an open face is a detector, the model owner, 2026-09-19).
FACE_NAMES = ("face:+x", "face:-x", "face:+y", "face:-y", "face:+z", "face:-z")
Pending = tuple[int, int, int]


@dataclass
class Measured:
    """A measured event at a Node: its declaration, its clock and its
    counters. `pending` holds, per family, what came home or is re-released
    and waits for the next self-creation: (amount, content per unit, phase)
    per arriving record. `record` is the detector's squared coherent reading
    per family, cumulative: an exact Python integer, a report of the host
    that is never refused and may pass 2^63 (its readers in `run.json` and
    `state.json` parse it as an arbitrary-precision integer). The engine
    sets `creating`, `clock_age` and
    `turn` before every interval (the clock's frame) and reads `presence`
    after it (the clock's count)."""

    number: int
    position: Address3
    family: int
    held: list[int]
    phase: int
    charge: int
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
    threshold: int
    age: int = 0
    owed: int = 0
    pending: list[list[Pending]] = field(default_factory=list)
    waited: int = 0
    phase_steps: int = 0
    steps: int = 0
    measured: list[dict[str, int]] = field(default_factory=list)
    events: list[int] = field(default_factory=list)
    pushed: list[int] = field(default_factory=lambda: [0, 0, 0])
    record: list[int] = field(default_factory=list)
    # The interval's frame, set by the engine: whether this interval is a
    # self-creation, the age before it and the turn read off the clock; and
    # what the law read back: the presence at the Node of every other number.
    creating: bool = False
    clock_age: int = 0
    turn: int = 0
    presence: int = 0

    @property
    def content(self) -> int:
        return sum(self.held)

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
            "charge": self.charge,
            "momentum": list(self.momentum),
            "fixed": self.fixed,
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
            "record": list(self.record),
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
