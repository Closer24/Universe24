"""The world of the law of events (events-v1): its keys and their refusals.

A world of this law is a JSON object with `"law": "events"` and nothing of the
earlier engines' schemas (no `contents`, no `initial_shadows`, no
`wait_per_quantum`, no `phase_turn`; none of the old engine's keys): the
refusal names the key at fault. What a world declares (Highlights 5.4, the
law of events, the model owner, 2026-09-19):

- `shape`, three positive extents; `boundary` `"open"` (the default: the edge
  is infinity on every face, what leaves is booked as escaped) or an object
  with any of the keys `x`, `y`, `z`, each `"open"` or `"periodic"`, the
  missing axes open (the declared exception of the model owner, 2026-09-19:
  on a periodic axis the departures that would leave through one face are
  created at the first Node of the opposite face, nothing escapes on that
  axis; a closed board and every other word are refused); `ticks`;
- `K`, the content per phase step per self-creation, one for the world; `N`,
  the steps of the phase circle (64 by default, a power of two from 2 through
  4096); `release` `[n, d]`, the events a measured event of a free family
  releases per self-creation per Port heading per unit of content, read off
  its clock; `suspension` `[n, d]`, the fractional width of the suspension:
  a reader owes `presence x n // d` intervals, the presence being the amount
  that arrived at its Node this interval over every family and every number
  but its own (an integer w is accepted as `[w, 1]`; `[1, 1]` by default; 0
  or `[0, d]` for none);
- `families`: each with a `name`, a `kind` (`free`: matter, whose measured
  events release at the world's rate and whose events are read for gravity
  and electricity; `paid`: light, released only by a lamp that spends its
  content, its events carrying their own momentum), for a free family the
  whole `charge` of a measured event of it (0 by default), for a paid
  family `quantum`, the content of one unit of it (1 by default): the momentum
  one unit carries from birth is its quantum times its heading; and `phase`
  (true by default): a family declaring `"phase": false` has no phase circle
  (the model owner, 2026-09-19): its events carry phase 0 and never turn, its
  measured events' phase never turns (K does not apply to their content), no
  `phase_window` is accepted on its lamps or on a table entry for it, its
  measured events and its events in transit declare no phase but 0, and at a
  Node its arrivals do not sum coherently: each Port's arrival scatters on
  its own (`mixing.scatter_arrivals`);
- `measured`: the measured events at the start, one per Node, each with a
  `position`, its `family`, its `amount` (a positive whole number of units,
  below K x N / 2), and optionally its `phase`, its whole `charge` (the
  family's by default), its `momentum` (three integers), `fixed` (true: an
  apparatus held in place, it takes pushes into its momentum and never
  steps), its `table` (family name to `read`, `measure`, `rerelease` or
  `pass`, or to an object `{"rule": ..., "phase_window": s}`; a free family
  is read by default, the push taken and the units mixed on, a paid family
  measured, the click) and, for a measured event of a paid family, its
  `lamp` (`rate` `[n, d]` units per self-creation per heading, `headings`
  the Port headings it releases on, all six by default, and optionally its
  `phase_window`); every measured event is given its number at parsing, 1,
  2, ... in declaration order;
- `phase_window`, the declared width of a detector and of an emitter
  (Highlights 5.4, the model owner, 2026-09-19: "Approve the phase window
  as a declared width of a detector, and of the emitter too"): a setting
  `s`, an integer from 0 through N - 1, and the half circle centred on it
  (with d = (phase - s) mod N, d < N / 4 or d >= 3 N / 4: exactly N / 2
  steps; for N = 2 the one step d = 0). On a table entry (any rule but
  `pass`, which responds to nothing and is refused a window) the response
  is made only to a bundle whose phase at the Node falls in the window; a
  bundle outside it passes. On a lamp, a release only at the self-creations
  whose clock phase falls in the window; the clock and the phase turn
  regardless;
- `in_transit`, optional: events in transit at the start, each with a
  `position`, `family`, `number` (the measured event whose continuation it
  is), `heading`, `amount` and `phase`, booked as initial content of the
  transit line; the default is an empty board that the releases fill;
- `detectors`, optional: named sets of measured events, each with a `name`,
  its `positions` (Nodes of measured events, each in at most one detector)
  and its `threshold` (1 by default): the smallest bundle of one number the
  detector measures in one interval; a smaller arrival passes. A detector's
  sensitivity is its Nodes and its threshold (Highlights 5.4, "a kind of
  detector sensitivity"); the record of a run reports its measurements per
  detector as well as per Node.
"""

from __future__ import annotations

from dataclasses import dataclass

from event_universe.core.integer import bounded_gcd, checked_work
from event_universe.core.lattice import MAX_VALUE, PORT_HEADINGS, Address3

EVENTS_LAW = "events-v1"
LAW_VALUE = "events"
KINDS = ("free", "paid")
TABLES = ("read", "measure", "rerelease", "pass")
MAX_PHASE_STEPS = 4096
# The bound of an amount, a clock and a momentum component of this law: the
# arrays hold 64-bit integers and the mixing's own guards bound a cell.
AMOUNT_BOUND = (1 << 62) - 1
# Keys of the earlier engines' worlds, refused by name so that the refusal
# says which law the world belongs to.
OLD_KEYS = (
    "contents",
    "initial_shadows",
    "wait_per_quantum",
    "schema_version",
    "fields",
    "disturbance_types",
    "seeds",
    "spatial_fields",
    "emissions",
    "spatial_seeds",
    "external_bodies",
    "initial_field",
    "ray_interactions",
    "couplings",
    "interactions",
    "dense_field",
    "standing_field",
    "wait_reads",
    "shadow_wait",
    "slots_per_node",
    "link_ticks",
    "normal_budget",
    "operation_costs",
)
WORLD_KEYS = {
    "law",
    "model_id",
    "shape",
    "boundary",
    "ticks",
    "K",
    "N",
    "release",
    "suspension",
    "families",
    "measured",
    "in_transit",
    "detectors",
}
FAMILY_KEYS = {"name", "kind", "charge", "quantum", "phase"}
MEASURED_KEYS = {"position", "family", "amount", "phase", "charge", "momentum", "fixed", "table", "lamp"}
LAMP_KEYS = {"rate", "headings", "phase_window"}
# A table entry's object form: the rule and, on any rule but `pass`, a window.
TABLE_ENTRY_KEYS = {"rule", "phase_window"}
TRANSIT_KEYS = {"position", "family", "number", "heading", "amount", "phase"}
DETECTOR_KEYS = {"name", "positions", "threshold"}
# The board's faces per axis: open (the default) or periodic (the wrap).
AXES = ("x", "y", "z")
BOUNDARIES = ("open", "periodic")


@dataclass(frozen=True)
class FamilyDefinition:
    """One family of the world: its name, its kind, the whole charge of a
    measured event of it, the content of one unit of it, and whether it has
    a phase circle (`phase` false: its events carry phase 0 and never turn,
    and at a Node each Port's arrival scatters on its own)."""

    name: str
    kind: str
    charge: int
    quantum: int
    phase: bool = True

    @property
    def free(self) -> bool:
        return self.kind == "free"


@dataclass(frozen=True)
class LampDefinition:
    """A measured event of a paid family that releases it at a declared rate,
    `rate` = (n, d) units per self-creation on each of its `headings` (Port
    indices), spending its content; with a `window` (a phase setting), only
    at the self-creations whose clock phase falls in the half circle centred
    on it."""

    rate: tuple[int, int]
    headings: tuple[int, ...]
    window: int | None


@dataclass(frozen=True)
class MeasuredDefinition:
    """One measured event as declared: its Node, its family, its amount, its
    phase, its whole charge, its momentum, whether it is held in place, its
    table per family (in family order) with the phase window of each entry
    (None without one) and its lamp."""

    position: Address3
    family: int
    amount: int
    phase: int
    charge: int
    momentum: tuple[int, int, int]
    fixed: bool
    table: tuple[str, ...]
    windows: tuple[int | None, ...]
    lamp: LampDefinition | None


@dataclass(frozen=True)
class TransitDefinition:
    """An event in transit at the start: at its Node, of its family and
    number, on its travel heading (a Port index), its amount and its phase."""

    position: Address3
    family: int
    number: int
    port: int
    amount: int
    phase: int


@dataclass(frozen=True)
class DetectorDefinition:
    """A named set of measured events and its threshold."""

    name: str
    positions: tuple[Address3, ...]
    threshold: int


@dataclass(frozen=True)
class EventWorld:
    """A parsed world of the law of events. `boundary` is the declared value
    as the record carries it (the string `"open"` or the object per axis);
    `periodic` says per axis (x, y, z) whether the walk wraps."""

    model_id: str
    shape: Address3
    boundary: str | dict[str, str]
    periodic: tuple[bool, bool, bool]
    ticks: int
    clock: int
    phase_steps: int
    release: tuple[int, int]
    # The suspension's fractional width (n, d): a reader owes presence x n // d
    # intervals; (0, d) is none.
    suspension: tuple[int, int]
    families: tuple[FamilyDefinition, ...]
    measured: tuple[MeasuredDefinition, ...]
    in_transit: tuple[TransitDefinition, ...]
    detectors: tuple[DetectorDefinition, ...]

    @property
    def phase_mask(self) -> int:
        return self.phase_steps - 1

    @property
    def boundary_per_axis(self) -> dict[str, str]:
        """The board's faces per axis, `x`, `y`, `z` to `open` or `periodic`."""
        return {
            axis: BOUNDARIES[1] if wraps else BOUNDARIES[0]
            for axis, wraps in zip(AXES, self.periodic, strict=True)
        }

    def owners(self, family: int) -> tuple[int, ...]:
        """The numbers whose events of a family can exist: the measured events
        that hold the family and are free (they release it), the lamps of it,
        the measured events whose table re-releases it (their number is
        stamped on what leaves them) and the numbers of the events in transit
        at the start."""
        found = []
        for index, entry in enumerate(self.measured):
            number = index + 1
            definition = self.families[family]
            if (
                (entry.family == family and (definition.free or entry.lamp is not None))
                or entry.table[family] == "rerelease"
                or any(item.number == number and item.family == family for item in self.in_transit)
            ):
                found.append(number)
        return tuple(found)

    def content_lcm(self) -> int:
        """The denominator of the electric reading, the least common multiple of
        the declared contents of the charged measured events (1 without any)."""
        result = 1
        for entry in self.measured:
            if entry.charge:
                result = checked_work(result * entry.amount) // bounded_gcd(result, entry.amount)
        if result > AMOUNT_BOUND:
            raise ValueError(
                f"{EVENTS_LAW}: the charged events' denominator exceeds the bounded integer"
            )
        return result

    def detector_of(self, position: Address3) -> int | None:
        """The index of the detector a Node belongs to, if any."""
        for index, detector in enumerate(self.detectors):
            if position in detector.positions:
                return index
        return None


def is_event_world(document: object) -> bool:
    """Whether a document declares the law of events (`"law": "events"`)."""
    return isinstance(document, dict) and document.get("law") == LAW_VALUE


def _object(value: object, label: str, allowed: set[str], required: set[str]) -> dict[str, object]:
    if not isinstance(value, dict):
        raise ValueError(f"{EVENTS_LAW}: {label} must be a JSON object")
    unknown = set(value) - allowed
    if unknown:
        raise ValueError(f"{EVENTS_LAW}: {label} has unknown keys: {', '.join(sorted(unknown))}")
    missing = required - set(value)
    if missing:
        raise ValueError(f"{EVENTS_LAW}: {label} lacks keys: {', '.join(sorted(missing))}")
    return {str(key): item for key, item in value.items()}


def _integer(value: object, label: str, minimum: int, maximum: int = AMOUNT_BOUND) -> int:
    if type(value) is not int or value < minimum or value > maximum:
        raise ValueError(f"{EVENTS_LAW}: {label} must be an integer from {minimum} through {maximum}")
    return value


def _ratio(value: object, label: str, zero: bool) -> tuple[int, int]:
    """A rate n / d as `[n, d]` (n from 0 with `zero`, d positive) or one integer."""
    if type(value) is int:
        return _integer(value, label, 0 if zero else 1), 1
    if not isinstance(value, list) or len(value) != 2:
        raise ValueError(f"{EVENTS_LAW}: {label} must be an integer or [numerator, denominator]")
    numerator = _integer(value[0], f"{label} numerator", 0 if zero else 1)
    denominator = _integer(value[1], f"{label} denominator", 1)
    return numerator, denominator


def _address(value: object, label: str, shape: Address3) -> Address3:
    if not isinstance(value, list) or len(value) != 3:
        raise ValueError(f"{EVENTS_LAW}: {label} must be three integers")
    found = tuple(
        _integer(item, label, 0, extent - 1) for item, extent in zip(value, shape, strict=True)
    )
    return found[0], found[1], found[2]


def _heading(value: object, label: str) -> int:
    if not isinstance(value, list) or len(value) != 3 or tuple(value) not in PORT_HEADINGS:
        raise ValueError(f"{EVENTS_LAW}: {label} must be one of the six Port headings")
    return PORT_HEADINGS.index((int(value[0]), int(value[1]), int(value[2])))


def _boundary(value: object) -> tuple[str | dict[str, str], tuple[bool, bool, bool]]:
    """The board's faces: `"open"` on every face, or an object with any of
    the keys `x`, `y`, `z`, each `"open"` or `"periodic"`, the missing axes
    open. Returns the value as declared (what the record carries) and, per
    axis, whether the walk wraps. A closed board and every other word are
    refused."""
    if value == BOUNDARIES[0]:
        return BOUNDARIES[0], (False, False, False)
    if (
        isinstance(value, dict)
        and set(value) <= set(AXES)
        and all(item in BOUNDARIES for item in value.values())
    ):
        declared = {str(key): str(item) for key, item in value.items()}
        wraps = tuple(declared.get(axis, BOUNDARIES[0]) == BOUNDARIES[1] for axis in AXES)
        return declared, (wraps[0], wraps[1], wraps[2])
    raise ValueError(
        f"{EVENTS_LAW}: the board is open (its edge is infinity) unless an axis is declared "
        'periodic (boundary "open" or an object of "x", "y", "z" to "open" or "periodic"); '
        "a closed board is refused"
    )


def _families(value: object) -> tuple[FamilyDefinition, ...]:
    if not isinstance(value, list) or not value:
        raise ValueError(f"{EVENTS_LAW}: families must be a nonempty list")
    found: list[FamilyDefinition] = []
    for index, entry in enumerate(value):
        obj = _object(entry, f"families[{index}]", FAMILY_KEYS, {"name", "kind"})
        name = obj["name"]
        if not isinstance(name, str) or not name:
            raise ValueError(f"{EVENTS_LAW}: families[{index}].name must be a nonempty string")
        if any(item.name == name for item in found):
            raise ValueError(f"{EVENTS_LAW}: two families named {name!r}")
        kind = obj["kind"]
        if kind not in KINDS:
            raise ValueError(f"{EVENTS_LAW}: families[{index}].kind must be free or paid")
        charge = _integer(obj.get("charge", 0), f"families[{index}].charge", -MAX_VALUE, MAX_VALUE)
        if kind == "paid" and charge:
            raise ValueError(f"{EVENTS_LAW}: a paid family carries no charge ({name})")
        quantum = _integer(obj.get("quantum", 1), f"families[{index}].quantum", 1, MAX_VALUE)
        if kind == "free" and quantum != 1:
            raise ValueError(f"{EVENTS_LAW}: a free family's unit is the unit of content ({name})")
        phase = obj.get("phase", True)
        if type(phase) is not bool:
            raise ValueError(f"{EVENTS_LAW}: families[{index}].phase must be true or false")
        found.append(FamilyDefinition(name, str(kind), charge, quantum, phase))
    return tuple(found)


def _window(value: object, label: str, phase_steps: int) -> int:
    """A phase window's setting: a step of the circle, 0 through N - 1."""
    return _integer(value, label, 0, phase_steps - 1)


def _lamp(value: object, label: str, phase_steps: int, phased: bool) -> LampDefinition:
    obj = _object(value, label, LAMP_KEYS, {"rate"})
    rate = _ratio(obj["rate"], f"{label}.rate", zero=True)
    headings_value = obj.get("headings", [list(heading) for heading in PORT_HEADINGS])
    if not isinstance(headings_value, list) or not headings_value:
        raise ValueError(f"{EVENTS_LAW}: {label}.headings must be a nonempty list of Port headings")
    headings = tuple(_heading(item, f"{label}.headings") for item in headings_value)
    if len(set(headings)) != len(headings):
        raise ValueError(f"{EVENTS_LAW}: {label}.headings repeats a heading")
    window = None
    if "phase_window" in obj:
        if not phased:
            raise ValueError(
                f"{EVENTS_LAW}: {label}.phase_window is refused on a lamp of a family without a "
                "phase circle (a window is a width on the circle, and the family has none)"
            )
        window = _window(obj["phase_window"], f"{label}.phase_window", phase_steps)
    return LampDefinition(rate, headings, window)


def _table_entry(value: object, label: str, phase_steps: int, phased: bool) -> tuple[str, int | None]:
    """One table entry: a rule string, or `{"rule": ..., "phase_window": s}`
    (the rule required; a window refused on `pass`, which responds to nothing,
    and for a family without a phase circle, whose bundles carry no phase)."""
    if isinstance(value, dict):
        obj = _object(value, label, TABLE_ENTRY_KEYS, {"rule"})
        rule = obj["rule"]
        window = None
        if "phase_window" in obj:
            window = _window(obj["phase_window"], f"{label}.phase_window", phase_steps)
    else:
        rule, window = value, None
    if rule not in TABLES:
        raise ValueError(f"{EVENTS_LAW}: {label} must be one of {TABLES}")
    if window is not None and rule == "pass":
        raise ValueError(
            f"{EVENTS_LAW}: {label}.phase_window is refused on pass: a window is a width of a "
            "response, and pass responds to nothing"
        )
    if window is not None and not phased:
        raise ValueError(
            f"{EVENTS_LAW}: {label}.phase_window is refused for a family without a phase circle: "
            "its bundles carry no phase to read"
        )
    return str(rule), window


def _measured(
    value: object,
    shape: Address3,
    families: tuple[FamilyDefinition, ...],
    clock: int,
    phase_steps: int,
) -> tuple[MeasuredDefinition, ...]:
    if not isinstance(value, list):
        raise ValueError(f"{EVENTS_LAW}: measured must be a list")
    names = {family.name: index for index, family in enumerate(families)}
    found: list[MeasuredDefinition] = []
    for index, entry in enumerate(value):
        label = f"measured[{index}]"
        obj = _object(entry, label, MEASURED_KEYS, {"position", "family", "amount"})
        position = _address(obj["position"], f"{label}.position", shape)
        if any(item.position == position for item in found):
            raise ValueError(f"{EVENTS_LAW}: two measured events at one Node {list(position)}")
        family_name = obj["family"]
        if not isinstance(family_name, str) or family_name not in names:
            raise ValueError(f"{EVENTS_LAW}: {label}.family names an unknown family")
        family = names[family_name]
        amount = _integer(obj["amount"], f"{label}.amount", 1)
        phased = families[family].phase
        if phased and 2 * amount >= clock * phase_steps:
            raise ValueError(
                f"{EVENTS_LAW}: {label}.amount must keep 2 x content below K x N (the phase step "
                "per self-creation below half the circle)"
            )
        # A measured event of a family without a phase circle has phase 0.
        phase = _integer(obj.get("phase", 0), f"{label}.phase", 0, phase_steps - 1 if phased else 0)
        charge = _integer(
            obj.get("charge", families[family].charge), f"{label}.charge", -MAX_VALUE, MAX_VALUE
        )
        if not families[family].free and charge:
            raise ValueError(
                f"{EVENTS_LAW}: {label}: a measured event of a paid family carries no charge"
            )
        momentum_value = obj.get("momentum", [0, 0, 0])
        if not isinstance(momentum_value, list) or len(momentum_value) != 3:
            raise ValueError(f"{EVENTS_LAW}: {label}.momentum must be three integers")
        momentum = tuple(_integer(item, f"{label}.momentum", -AMOUNT_BOUND) for item in momentum_value)
        fixed = obj.get("fixed", False)
        if type(fixed) is not bool:
            raise ValueError(f"{EVENTS_LAW}: {label}.fixed must be true or false")
        table = ["read" if item.free else "measure" for item in families]
        windows: list[int | None] = [None] * len(families)
        declared = obj.get("table", {})
        if not isinstance(declared, dict):
            raise ValueError(f"{EVENTS_LAW}: {label}.table must map family names to rules")
        for key, entry_value in declared.items():
            if key not in names:
                raise ValueError(f"{EVENTS_LAW}: {label}.table names an unknown family {key!r}")
            table[names[key]], windows[names[key]] = _table_entry(
                entry_value, f"{label}.table[{key!r}]", phase_steps, families[names[key]].phase
            )
        lamp = None
        if "lamp" in obj:
            if families[family].free:
                raise ValueError(f"{EVENTS_LAW}: {label}: a lamp is a measured event of a paid family")
            lamp = _lamp(obj["lamp"], f"{label}.lamp", phase_steps, phased)
        found.append(
            MeasuredDefinition(
                position,
                family,
                amount,
                phase,
                charge,
                (momentum[0], momentum[1], momentum[2]),
                fixed,
                tuple(table),
                tuple(windows),
                lamp,
            )
        )
    return tuple(found)


def _in_transit(
    value: object,
    shape: Address3,
    families: tuple[FamilyDefinition, ...],
    measured: tuple[MeasuredDefinition, ...],
    phase_steps: int,
) -> tuple[TransitDefinition, ...]:
    if not isinstance(value, list):
        raise ValueError(f"{EVENTS_LAW}: in_transit must be a list")
    names = {family.name: index for index, family in enumerate(families)}
    found: list[TransitDefinition] = []
    for index, entry in enumerate(value):
        label = f"in_transit[{index}]"
        obj = _object(entry, label, TRANSIT_KEYS, {"position", "family", "number", "heading", "amount"})
        family_name = obj["family"]
        if not isinstance(family_name, str) or family_name not in names:
            raise ValueError(f"{EVENTS_LAW}: {label}.family names an unknown family")
        family = names[family_name]
        top = phase_steps - 1 if families[family].phase else 0
        found.append(
            TransitDefinition(
                _address(obj["position"], f"{label}.position", shape),
                family,
                _integer(obj["number"], f"{label}.number", 1, len(measured)),
                _heading(obj["heading"], f"{label}.heading"),
                _integer(obj["amount"], f"{label}.amount", 1),
                _integer(obj.get("phase", 0), f"{label}.phase", 0, top),
            )
        )
    return tuple(found)


def _detectors(
    value: object, shape: Address3, measured: tuple[MeasuredDefinition, ...]
) -> tuple[DetectorDefinition, ...]:
    if not isinstance(value, list):
        raise ValueError(f"{EVENTS_LAW}: detectors must be a list")
    at = {entry.position for entry in measured}
    taken: set[Address3] = set()
    found: list[DetectorDefinition] = []
    for index, entry in enumerate(value):
        label = f"detectors[{index}]"
        obj = _object(entry, label, DETECTOR_KEYS, {"name", "positions"})
        name = obj["name"]
        if not isinstance(name, str) or not name:
            raise ValueError(f"{EVENTS_LAW}: {label}.name must be a nonempty string")
        if any(item.name == name for item in found):
            raise ValueError(f"{EVENTS_LAW}: two detectors named {name!r}")
        positions_value = obj["positions"]
        if not isinstance(positions_value, list) or not positions_value:
            raise ValueError(f"{EVENTS_LAW}: {label}.positions must be a nonempty list of Nodes")
        positions = []
        for item in positions_value:
            position = _address(item, f"{label}.positions", shape)
            if position not in at:
                raise ValueError(
                    f"{EVENTS_LAW}: {label}.positions names a Node without a measured event {list(position)}"
                )
            if position in taken:
                raise ValueError(f"{EVENTS_LAW}: a Node in two detectors {list(position)}")
            taken.add(position)
            positions.append(position)
        threshold = _integer(obj.get("threshold", 1), f"{label}.threshold", 1)
        found.append(DetectorDefinition(name, tuple(positions), threshold))
    return tuple(found)


def parse_event_world(document: object) -> EventWorld:
    """Reject anything but a lawful world of the law of events."""
    if not isinstance(document, dict):
        raise ValueError(f"{EVENTS_LAW}: a world is a JSON object")
    old = [key for key in OLD_KEYS if key in document]
    if old:
        raise ValueError(
            f"{EVENTS_LAW}: a world of the law of events declares none of the earlier engines' "
            f"keys ({', '.join(old)}); see docs/MIGRATION.md"
        )
    if document.get("law") != LAW_VALUE:
        raise ValueError(f'{EVENTS_LAW}: a world of the law of events declares "law": "events"')
    obj = _object(
        document,
        "the world",
        WORLD_KEYS,
        {"law", "model_id", "shape", "ticks", "K", "release", "families", "measured"},
    )
    model_id = obj["model_id"]
    if not isinstance(model_id, str) or not model_id:
        raise ValueError(f"{EVENTS_LAW}: model_id must be a nonempty string")
    shape_value = obj["shape"]
    if not isinstance(shape_value, list) or len(shape_value) != 3:
        raise ValueError(f"{EVENTS_LAW}: shape must be three positive extents")
    extents = tuple(_integer(item, "shape", 1, 4096) for item in shape_value)
    shape: Address3 = (extents[0], extents[1], extents[2])
    boundary, periodic = _boundary(obj.get("boundary", BOUNDARIES[0]))
    ticks = _integer(obj["ticks"], "ticks", 0)
    clock = _integer(obj["K"], "K", 1)
    phase_steps = _integer(obj.get("N", 64), "N", 2, MAX_PHASE_STEPS)
    if phase_steps & (phase_steps - 1):
        raise ValueError(f"{EVENTS_LAW}: N must be a power of two from 2 through {MAX_PHASE_STEPS}")
    release = _ratio(obj["release"], "release", zero=True)
    suspension = _ratio(obj.get("suspension", 1), "suspension", zero=True)
    if suspension[0] == 0:
        # Off: 0 and [0, d] alike, recorded as [0, 1].
        suspension = (0, 1)
    families = _families(obj["families"])
    measured = _measured(obj["measured"], shape, families, clock, phase_steps)
    in_transit = _in_transit(obj.get("in_transit", []), shape, families, measured, phase_steps)
    detectors = _detectors(obj.get("detectors", []), shape, measured)
    world = EventWorld(
        model_id,
        shape,
        boundary,
        periodic,
        ticks,
        clock,
        phase_steps,
        release,
        suspension,
        families,
        measured,
        in_transit,
        detectors,
    )
    world.content_lcm()
    return world
