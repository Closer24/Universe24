"""The world of the law of the ray (rays-v1): its keys and their refusals.

A world of this law is a JSON object with `"law": "rays"` and nothing of the
earlier engines' schemas (no `contents`, no `initial_shadows`, no
`wait_per_quantum`, no `dynamics`; none of the old engine's keys): the
refusal names the key at fault. `"law": "events"` is refused naming the law
of the ray and docs/MIGRATION.md (the law of events, `events-v1`, was deleted
on 2026-09-19). What a world declares ([the law of the ray](../../../docs/RAY_LAW.md),
the model owner, 2026-09-19):

- `shape`, three positive extents; `boundary` `"open"` (the default: the edge
  is infinity on every face, what leaves clicks on the face detector) or an
  object with any of the keys `x`, `y`, `z`, each `"open"` or `"periodic"`,
  the missing axes open; `ticks`;
- `K`, the content per phase step per self-creation, one for the world; `N`,
  the steps of the phase circle (64 by default, a power of two from 2 through
  4096); `release` `[n, d]`, the rays a measured event of a free family
  releases per self-creation per declared direction per unit of content,
  read off its clock; `suspension` `[n, d]`, the fractional width of the
  clock's count: a measured event owes `by_clock(age, presence x n, d)`
  intervals after its self-creation, the presence being the amount of every
  ray at its Node of every number but its own (an integer w is accepted as
  `[w, 1]`; `[1, 1]` by default; 0 or `[0, d]` for none); `width`, the
  width S of the push (the model owner's D1, 2026-09-19): a free measured
  event of content M with the momentum component p on an axis steps one
  Link per (S x M + p) / p self-creations on that axis, an integer from 1
  (the default: the rule as it was, one Link per (M + p) / p); 0 or a
  negative width is refused;
- `directions`, optional: integer vectors beyond the six headings that a
  lamp, a measured event or a ray in transit may name; the world's direction
  table `D` is the two rest vectors (0, 0, 0) ("here a", "here b"), the six
  headings in Port order and these, in that order; each declared vector is
  primitive with every component in -P .. P, P = `direction_bound` (64 by
  default, at most 4096 entries in the table);
- `families`: each with a `name`, its `quantum` (h, required: the content
  of one unit of it per phase step of its emitter's turn; the kind of the
  family follows from it and is not declared: h = 0 is a free family,
  matter, whose measured events release at the world's rate, whose rays
  carry no content and are read for gravity and electricity, their label
  the amount along the direction; h >= 1 is a paid family, light, released
  only by a lamp that spends its content: a release costs the emitter
  quantum x s per unit at a self-creation whose turn is s steps, the unit
  carries that content and the momentum quantum x s along its direction,
  and a click measures it, E = h f), for a free family its `charge`, the
  charge per unit of content, rho, an integer or a pair `[n, d]` (d from
  1; an integer c is `[c, 1]`; 0 by default; refused on a paid family; the
  model owner's decision of 2026-09-20, Highlights 5.4: a measured event's
  charge is rho times its content, and the electric push is one product
  per arriving free ray, M_A x (rho_A rho_B - 1) x V_B),
  `phase` (true by default; false: the family has no phase circle, its rays
  carry phase 0 and never turn, its measured events never turn, no
  `phase_window` is accepted for it) and `phase_per_link` (an integer
  0 .. N - 1, 0 by default: the phase steps a ray of the family turns at
  every Link crossed). The key `kind` of the first ray worlds is refused
  naming this derivation and docs/MIGRATION.md (one canonical form);
- `measured`: the measured events at the start, one per Node, each with a
  `position`, its `family`, its `amount` (a positive whole number of units,
  below K x N / 2 for a family with a phase circle), and optionally its
  `phase`, its `momentum` (three integers), `fixed` (true: an apparatus held in place, it takes
  pushes into its momentum and never steps), its `directions` (the
  directions it releases on and re-emits on, as vectors or indices of the
  world's table; the six headings by default), its `table` (family name to
  `read`, `measure`, `rerelease` or `pass`, or to an object `{"rule": ...,
  "phase_window": s, "reads": key}`; the table is generated from the
  families' keys by `default_table`, a free family read, the push taken and
  the rays going on, a paid family measured, the click, and a world declares
  only the entries that differ: a window, a rule off the default, a `reads`
  component; an entry equal to the default is accepted and changes nothing)
  and, for a measured event of a paid family, its `lamp` (`rate` `[n, d]` units
  per self-creation per direction, `directions` the directions it releases
  on, the six headings by default, and optionally its `phase_window`);
  every measured event is given its number at parsing, 1, 2, ... in
  declaration order;
- `phase_window`, the declared width of a detector and of an emitter: a
  setting `s`, an integer from 0 through N - 1, and the half circle centred
  on it (with d = (phase - s) mod N, d < N / 4 or d >= 3 N / 4: exactly
  N / 2 steps; for N = 2 the one step d = 0). On a table entry (any rule but
  `pass`) the response is made only to a ray whose own phase falls in the
  window; a ray outside it passes. On a lamp, a release only at the
  self-creations whose clock phase falls in the window;
- `reads` on a table entry: the component of the Node's one reading that
  the response's record carries, `scalar` (the presence), `outside`, `here`,
  `vector` (the net flow) or `tensor` (the traceless part); `vector` by
  default on `read`, `scalar` otherwise. No rule changes with it: every
  coupling reads the one reading, the moments of the arrivals (`nature_beam.read_arrivals`);
- `in_transit`, optional: rays at the start, each with a `position`,
  `family`, `number` (the measured event whose continuation it is),
  `direction` (a vector of the world's table or its index), `amount`,
  `phase` and optionally `age`, booked as initial content of the transit
  line; the default is an empty board that the releases fill;
- `detectors`, optional: named sets of measured events, each with a `name`,
  its `positions` (Nodes of measured events, each in at most one detector),
  its `threshold` (1 by default): the smallest amount of a family arriving
  at the detector's Nodes in one interval, summed over the whole set and
  over every number but each Node's own; a smaller set passes; and its
  `reading`, `"wave"` (the default since 2026-09-20; the model owner: "on
  the board a ray, in the world a wave") or `"beam"` (the model owner,
  2026-09-19): a detector is a set of Nodes with ONE record (a click says
  "here, in one of these" and not which; the declared width is the
  position's uncertainty). Under `wave` the record is the square of the
  coherent pointer of the rays the set clicked in the interval, the
  window reads the set's phase and the set's phase is returned to its
  measured events; under `beam` the arriving rays are paired by opposite
  phase over the set, a paired couple passes on and the rest click, the
  record is the plain count. A measured event outside every detector is a
  detector of one Node with the default reading.

Refused, naming the key: `kind` on a family (the quantum decides it),
`charge` on a measured event (since 2026-09-20 the charge is the family's
per unit of content, docs/MIGRATION.md), a family `charge` whose
denominator is 0 or whose parts are not integers, a detector named as a
face detector is (`face:+x` and the five others), `headings` on a lamp
(`directions` replaces it),
`heading` on a ray in transit (`direction` replaces it), `dynamics`,
`max_active_owners`, `port_map`, `output`, `capacity`, `groups`, a direction
that is not primitive, a component beyond P, a direction the world does not
declare, a label `Q x content x amount` beyond 2^62 - 1 on a declared ray or
a lamp's release (Q = `LABEL_SCALE` = 64: the momentum label of a ray is
along the unit vector of its direction at the flight table's scale, the
model owner's decision of 2026-09-19 on the physics-rule reviewer's
verdict, [RAY_LAW section 2](../../../docs/RAY_LAW.md), so every declared
`momentum` and every momentum of the record is in label units, Q per unit
of amount along a heading), `phase_per_link` outside 0 .. N - 1.
"""

from __future__ import annotations

from dataclasses import dataclass

from event_universe.core.integer import bounded_gcd
from event_universe.core.lattice import MAX_VALUE, PORT_HEADINGS, Address3

RAYS_LAW = "rays-v1"
LAW_VALUE = "rays"
TABLES = ("read", "measure", "rerelease", "pass")
# The quantum of a free family: its unit costs nothing and carries no content.
FREE_QUANTUM = 0
# The components of the one reading a table entry may select for its record.
READS = ("scalar", "outside", "here", "vector", "tensor")
MAX_PHASE_STEPS = 4096
# The bound of an amount, a content, a clock and a momentum component of this
# law: the 64-bit work register with a bit to spare for one more sum.
AMOUNT_BOUND = (1 << 62) - 1
MOMENTUM_BOUND = (1 << 62) - 1
# The one scale Q of the flight table and of the momentum label: the label
# of a unit is the integer vector nearest Q D / |D| (`nature_beam.unit_label`,
# exactly Q e_d on a heading), so a label component is within Q x content
# x amount per row, and the parser's bound is that product (the model
# owner's decision of 2026-09-19, the physics-rule reviewer's correction 3).
LABEL_SCALE = 64
# The direction table: two rest vectors, the six headings, the declared rest.
REST_DIRECTIONS = 2
HEADING_OFFSET = REST_DIRECTIONS
FIXED_DIRECTIONS = REST_DIRECTIONS + 6
DEFAULT_DIRECTION_BOUND = 64
MAX_DIRECTIONS = 4096
Vector = tuple[int, int, int]
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
# Keys of the law of events (`events-v1`, deleted on 2026-09-19) that the law
# of the ray refuses by name.
EVENTS_KEYS = ("dynamics", "max_active_owners")
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
    "width",
    "directions",
    "direction_bound",
    "families",
    "measured",
    "in_transit",
    "detectors",
}
FAMILY_KEYS = {"name", "quantum", "charge", "phase", "phase_per_link"}
# The key of the first ray worlds that named the kind; the quantum decides it.
KIND_KEY = "kind"
# The key of the ray worlds before 2026-09-20 that gave a measured event its
# own whole charge; the charge is the family's per unit of content.
CHARGE_KEY = "charge"
# The charge per unit of content of a family with none: 0 as the pair [0, 1].
NO_CHARGE = (0, 1)
MEASURED_KEYS = {
    "position",
    "family",
    "amount",
    "phase",
    "momentum",
    "fixed",
    "directions",
    "table",
    "lamp",
}
LAMP_KEYS = {"rate", "directions", "phase_window"}
# A table entry's object form: the rule, a window on any rule but `pass`,
# and the reading's component the record carries.
TABLE_ENTRY_KEYS = {"rule", "phase_window", "reads"}
TRANSIT_KEYS = {"position", "family", "number", "direction", "amount", "phase", "age"}
DETECTOR_KEYS = {"name", "positions", "threshold", "reading"}
# The readings a detector may declare; the first is the default: `wave`
# since 2026-09-20 (the model owner: "on the board a ray, in the world a
# wave"; `beam` was the default from 2026-09-19 to 2026-09-20).
DETECTOR_READINGS = ("wave", "beam")
# The keys of the deleted `reversible-detector-v1`, refused by name.
REVERSIBLE_KEYS = ("port_map", "output", "capacity", "groups", "reference_phase")
# The face detectors, one per open face of the board, named by the face in
# Port order (an open face is a detector, the model owner, 2026-09-19); a
# declared detector may not take one of these names.
FACE_NAMES = ("face:+x", "face:-x", "face:+y", "face:-y", "face:+z", "face:-z")
# The board's faces per axis: open (the default) or periodic (the wrap).
AXES = ("x", "y", "z")
BOUNDARIES = ("open", "periodic")


@dataclass(frozen=True)
class FamilyDefinition:
    """One family of the world: its name, the content of one unit of it per
    phase step of its emitter's turn (`quantum`, h; 0 for a free family,
    1 or more for a paid one: the kind is derived, never declared), its
    charge per unit of content (`charge`, rho, the pair (n, d) with d from
    1: a measured event of the family of content M carries the charge
    rho x M, and its rays push a charged reader by rho; (0, 1) for a paid
    family, whose rays push by their content), whether it has a phase
    circle and the phase steps its rays turn per Link crossed."""

    name: str
    quantum: int
    charge: tuple[int, int] = NO_CHARGE
    phase: bool = True
    phase_per_link: int = 0

    @property
    def free(self) -> bool:
        """A free family (h = 0): its release costs nothing and its rays
        carry no content."""
        return self.quantum == FREE_QUANTUM

    @property
    def unit_label(self) -> int:
        """The content one declared unit of the family carries for its
        momentum label: the quantum (one phase step of content, no emitter
        having declared its turn) for a paid family, the unit for a free
        one, whose label is the amount along the direction."""
        return max(self.quantum, 1)


def default_rule(family: FamilyDefinition) -> str:
    """The rule the family's key gives: a free family (h = 0) is read, the
    push taken and the rays going on; a paid one (h >= 1) is measured, the
    click."""
    return "read" if family.free else "measure"


def default_reads(rule: str) -> str:
    """The component of the one reading a rule's record carries unless the
    entry declares one: the net flow on `read`, the presence otherwise."""
    return "vector" if rule == "read" else "scalar"


def default_table(
    families: tuple[FamilyDefinition, ...],
) -> tuple[tuple[str, int | None, str], ...]:
    """The table generated from the keys (the model owner, 2026-09-19): per
    family in family order its rule, no window and the rule's component. A
    measured event's declared `table` overrides only the entries it names;
    an entry equal to this default is accepted and changes nothing."""
    return tuple(
        (default_rule(family), None, default_reads(default_rule(family))) for family in families
    )


@dataclass(frozen=True)
class LampDefinition:
    """A measured event of a paid family that releases it at a declared rate,
    `rate` = (n, d) units per self-creation on each of its `directions`
    (indices of the world's table), spending its content; with a `window`
    (a phase setting), only at the self-creations whose clock phase falls in
    the half circle centred on it."""

    rate: tuple[int, int]
    directions: tuple[int, ...]
    window: int | None


@dataclass(frozen=True)
class MeasuredDefinition:
    """One measured event as declared: its Node, its family, its amount, its
    phase, its momentum, whether it is held in place, the directions it
    releases and re-emits on, its table per family (in family order) with
    the phase window and the reading key of each entry, and its lamp. Its
    charge is its family's charge per unit of content times its content
    and is not declared."""

    position: Address3
    family: int
    amount: int
    phase: int
    momentum: Vector
    fixed: bool
    directions: tuple[int, ...]
    table: tuple[str, ...]
    windows: tuple[int | None, ...]
    reads: tuple[str, ...]
    lamp: LampDefinition | None


@dataclass(frozen=True)
class TransitDefinition:
    """A ray at the start: at its Node, of its family and number, on its
    direction (an index of the world's table), its amount, its phase and its
    age."""

    position: Address3
    family: int
    number: int
    direction: int
    amount: int
    phase: int
    age: int


@dataclass(frozen=True)
class DetectorDefinition:
    """A named set of measured events, its threshold and its reading
    (`beam` or `wave`)."""

    name: str
    positions: tuple[Address3, ...]
    threshold: int
    reading: str = DETECTOR_READINGS[0]


@dataclass(frozen=True)
class RayWorld:
    """A parsed world of the law of the ray. `boundary` is the declared value
    as the record carries it (the string `"open"` or the object per axis);
    `periodic` says per axis (x, y, z) whether the walk wraps; `directions`
    is the table `D`: the two rest vectors, the six headings and the declared
    rest."""

    model_id: str
    shape: Address3
    boundary: str | dict[str, str]
    periodic: tuple[bool, bool, bool]
    ticks: int
    clock: int
    phase_steps: int
    release: tuple[int, int]
    suspension: tuple[int, int]
    width: int
    directions: tuple[Vector, ...]
    direction_bound: int
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
        """The numbers whose rays of a family can exist: the measured events
        that hold the family and are free (they release it), the lamps of it,
        the measured events whose table re-releases it (their number is
        stamped on what leaves them) and the numbers of the rays in transit
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

    def detector_of(self, position: Address3) -> int | None:
        """The index of the detector a Node belongs to, if any."""
        for index, detector in enumerate(self.detectors):
            if position in detector.positions:
                return index
        return None


def is_ray_world(document: object) -> bool:
    """Whether a document declares the law of the ray (`"law": "rays"`)."""
    return isinstance(document, dict) and document.get("law") == LAW_VALUE


def _object(value: object, label: str, allowed: set[str], required: set[str]) -> dict[str, object]:
    if not isinstance(value, dict):
        raise ValueError(f"{RAYS_LAW}: {label} must be a JSON object")
    retired = [key for key in (*REVERSIBLE_KEYS, "headings", "heading") if key in value]
    if retired:
        raise ValueError(
            f"{RAYS_LAW}: {label} declares {', '.join(retired)}, a key of the deleted law of "
            "events or its reversible detector (see docs/MIGRATION.md; a lamp and a ray declare "
            "`directions` and `direction`)"
        )
    unknown = set(value) - allowed
    if unknown:
        raise ValueError(f"{RAYS_LAW}: {label} has unknown keys: {', '.join(sorted(unknown))}")
    missing = required - set(value)
    if missing:
        raise ValueError(f"{RAYS_LAW}: {label} lacks keys: {', '.join(sorted(missing))}")
    return {str(key): item for key, item in value.items()}


def _integer(value: object, label: str, minimum: int, maximum: int = AMOUNT_BOUND) -> int:
    if type(value) is not int or value < minimum or value > maximum:
        raise ValueError(f"{RAYS_LAW}: {label} must be an integer from {minimum} through {maximum}")
    return value


def _ratio(value: object, label: str, zero: bool) -> tuple[int, int]:
    """A rate n / d as `[n, d]` (n from 0 with `zero`, d positive) or one integer."""
    if type(value) is int:
        return _integer(value, label, 0 if zero else 1), 1
    if not isinstance(value, list) or len(value) != 2:
        raise ValueError(f"{RAYS_LAW}: {label} must be an integer or [numerator, denominator]")
    numerator = _integer(value[0], f"{label} numerator", 0 if zero else 1)
    denominator = _integer(value[1], f"{label} denominator", 1)
    return numerator, denominator


def _signed_ratio(value: object, label: str) -> tuple[int, int]:
    """A charge per unit of content n / d as an integer c (the pair (c, 1))
    or as `[n, d]`, n an integer of either sign and d an integer from 1,
    each within the bound of a declared charge; a denominator of 0 and a
    part that is not an integer are refused naming the key."""
    if type(value) is int:
        return _integer(value, label, -MAX_VALUE, MAX_VALUE), 1
    if not isinstance(value, list) or len(value) != 2:
        raise ValueError(
            f"{RAYS_LAW}: {label} must be an integer or [numerator, denominator], the charge "
            "per unit of content"
        )
    numerator = _integer(value[0], f"{label} numerator", -MAX_VALUE, MAX_VALUE)
    denominator = _integer(value[1], f"{label} denominator", 1, MAX_VALUE)
    return numerator, denominator


def _address(value: object, label: str, shape: Address3) -> Address3:
    if not isinstance(value, list) or len(value) != 3:
        raise ValueError(f"{RAYS_LAW}: {label} must be three integers")
    found = tuple(
        _integer(item, label, 0, extent - 1) for item, extent in zip(value, shape, strict=True)
    )
    return found[0], found[1], found[2]


def _vector(value: object, label: str, bound: int) -> Vector:
    """A primitive integer vector with every component in -bound .. bound."""
    if not isinstance(value, list) or len(value) != 3:
        raise ValueError(f"{RAYS_LAW}: {label} must be three integers")
    found = tuple(_integer(item, label, -bound, bound) for item in value)
    if found == (0, 0, 0):
        raise ValueError(
            f"{RAYS_LAW}: {label} must not be the zero vector (the rest slots are the table's)"
        )
    if bounded_gcd(bounded_gcd(found[0], found[1]), found[2]) != 1:
        raise ValueError(f"{RAYS_LAW}: {label} must be a primitive vector (its components coprime)")
    return found[0], found[1], found[2]


def _direction_table(value: object, bound: int) -> tuple[Vector, ...]:
    """The table `D`: the two rest vectors, the six headings, the declared."""
    table: list[Vector] = [(0, 0, 0), (0, 0, 0), *PORT_HEADINGS]
    if not isinstance(value, list):
        raise ValueError(f"{RAYS_LAW}: directions must be a list of integer vectors")
    for index, item in enumerate(value):
        vector = _vector(item, f"directions[{index}]", bound)
        if vector in table:
            raise ValueError(f"{RAYS_LAW}: directions[{index}] repeats a direction of the table")
        table.append(vector)
    if len(table) > MAX_DIRECTIONS:
        raise ValueError(f"{RAYS_LAW}: the direction table holds at most {MAX_DIRECTIONS} entries")
    return tuple(table)


def _direction(value: object, label: str, table: tuple[Vector, ...], *, rest: bool = False) -> int:
    """A direction named by its vector or by its index in the world's table;
    a rest vector only where `rest` allows it (a ray in transit)."""
    if type(value) is int:
        index = _integer(value, label, 0, len(table) - 1)
    else:
        if not isinstance(value, list) or len(value) != 3 or any(type(v) is not int for v in value):
            raise ValueError(f"{RAYS_LAW}: {label} must be a direction vector or an index of the table")
        vector = (value[0], value[1], value[2])
        if vector not in table:
            raise ValueError(
                f"{RAYS_LAW}: {label} names a direction the world does not declare {list(vector)} "
                "(the six headings or a vector of `directions`)"
            )
        index = table.index(vector)
    if index < REST_DIRECTIONS and not rest:
        raise ValueError(f"{RAYS_LAW}: {label} must not be a rest direction")
    return index


def _directions(value: object, label: str, table: tuple[Vector, ...]) -> tuple[int, ...]:
    if not isinstance(value, list) or not value:
        raise ValueError(f"{RAYS_LAW}: {label} must be a nonempty list of directions")
    found = tuple(_direction(item, label, table) for item in value)
    if len(set(found)) != len(found):
        raise ValueError(f"{RAYS_LAW}: {label} repeats a direction")
    return found


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
        f"{RAYS_LAW}: the board is open (its edge is infinity) unless an axis is declared "
        'periodic (boundary "open" or an object of "x", "y", "z" to "open" or "periodic"); '
        "a closed board is refused"
    )


def _families(value: object, phase_steps: int) -> tuple[FamilyDefinition, ...]:
    if not isinstance(value, list) or not value:
        raise ValueError(f"{RAYS_LAW}: families must be a nonempty list")
    found: list[FamilyDefinition] = []
    for index, entry in enumerate(value):
        if isinstance(entry, dict) and KIND_KEY in entry:
            raise ValueError(
                f"{RAYS_LAW}: families[{index}] declares {KIND_KEY}, a key removed on 2026-09-19: "
                "the kind of a family follows from its quantum (0 free, 1 or more paid) and is "
                "not declared; see docs/MIGRATION.md"
            )
        obj = _object(entry, f"families[{index}]", FAMILY_KEYS, {"name", "quantum"})
        name = obj["name"]
        if not isinstance(name, str) or not name:
            raise ValueError(f"{RAYS_LAW}: families[{index}].name must be a nonempty string")
        if any(item.name == name for item in found):
            raise ValueError(f"{RAYS_LAW}: two families named {name!r}")
        quantum = _integer(obj["quantum"], f"families[{index}].quantum", FREE_QUANTUM, MAX_VALUE)
        charge = _signed_ratio(obj.get("charge", 0), f"families[{index}].charge")
        if quantum != FREE_QUANTUM and charge[0]:
            raise ValueError(f"{RAYS_LAW}: a paid family (quantum {quantum}) carries no charge ({name})")
        phase = obj.get("phase", True)
        if type(phase) is not bool:
            raise ValueError(f"{RAYS_LAW}: families[{index}].phase must be true or false")
        per_link = _integer(
            obj.get("phase_per_link", 0), f"families[{index}].phase_per_link", 0, phase_steps - 1
        )
        if per_link and not phase:
            raise ValueError(
                f"{RAYS_LAW}: families[{index}].phase_per_link is refused for a family without a "
                "phase circle"
            )
        found.append(FamilyDefinition(name, quantum, charge, phase, per_link))
    return tuple(found)


def _window(value: object, label: str, phase_steps: int) -> int:
    """A phase window's setting: a step of the circle, 0 through N - 1."""
    return _integer(value, label, 0, phase_steps - 1)


def _label_bound(
    amount: int, content: int, table: tuple[Vector, ...], directions: tuple[int, ...], label: str
) -> None:
    """The momentum label of a release or a declared ray, `content x amount x
    u_d` with u_d the unit vector of the direction at the scale Q (no
    component beyond Q), must fit the bound on every component: Q x content
    x amount within 2^62 - 1, that is content x amount below 2^56."""
    for direction in directions:
        if LABEL_SCALE * content * amount > MOMENTUM_BOUND:
            raise ValueError(
                f"{RAYS_LAW}: {label}: the momentum label {LABEL_SCALE} x {content} x {amount} = "
                f"{LABEL_SCALE * content * amount} along {list(table[direction])} exceeds the "
                f"integer bound {MOMENTUM_BOUND} (content x amount at most {MOMENTUM_BOUND // LABEL_SCALE})"
            )


def _lamp(
    value: object,
    label: str,
    phase_steps: int,
    phased: bool,
    table: tuple[Vector, ...],
    quantum: int,
    amount: int,
    clock: int,
) -> LampDefinition:
    obj = _object(value, label, LAMP_KEYS, {"rate"})
    rate = _ratio(obj["rate"], f"{label}.rate", zero=True)
    directions = _directions(
        obj.get("directions", list(range(HEADING_OFFSET, FIXED_DIRECTIONS))),
        f"{label}.directions",
        table,
    )
    window = None
    if "phase_window" in obj:
        if not phased:
            raise ValueError(
                f"{RAYS_LAW}: {label}.phase_window is refused on a lamp of a family without a "
                "phase circle (a window is a width on the circle, and the family has none)"
            )
        window = _window(obj["phase_window"], f"{label}.phase_window", phase_steps)
    # The largest label a release can carry: the rate's numerator units at
    # the largest turn the content allows (the whole part of amount / K).
    largest_turn = max(1, amount // clock)
    _label_bound(max(1, rate[0]), quantum * largest_turn, table, directions, f"{label} (the release)")
    return LampDefinition(rate, directions, window)


def _table_entry(
    value: object, label: str, phase_steps: int, phased: bool, default: str
) -> tuple[str, int | None, str]:
    """One table entry: a rule string, or `{"rule": ..., "phase_window": s,
    "reads": key}` (the rule the family's default when the object omits it,
    so a window alone is a lawful entry; a window refused on `pass`, which
    responds to nothing, and for a family without a phase circle, whose
    rays carry no phase; the reading's component `vector` by default on
    `read`, `scalar` otherwise)."""
    reads: object = None
    if isinstance(value, dict):
        obj = _object(value, label, TABLE_ENTRY_KEYS, set())
        rule = obj.get("rule", default)
        window = None
        if "phase_window" in obj:
            window = _window(obj["phase_window"], f"{label}.phase_window", phase_steps)
        reads = obj.get("reads")
    else:
        rule, window = value, None
    if rule not in TABLES:
        raise ValueError(f"{RAYS_LAW}: {label} must be one of {TABLES}")
    if window is not None and rule == "pass":
        raise ValueError(
            f"{RAYS_LAW}: {label}.phase_window is refused on pass: a window is a width of a "
            "response, and pass responds to nothing"
        )
    if window is not None and not phased:
        raise ValueError(
            f"{RAYS_LAW}: {label}.phase_window is refused for a family without a phase circle: "
            "its rays carry no phase to read"
        )
    if reads is None:
        reads = default_reads(str(rule))
    if reads not in READS:
        raise ValueError(f"{RAYS_LAW}: {label}.reads must be one of {READS}")
    return str(rule), window, str(reads)


def _measured(
    value: object,
    shape: Address3,
    families: tuple[FamilyDefinition, ...],
    clock: int,
    phase_steps: int,
    release: tuple[int, int],
    table: tuple[Vector, ...],
) -> tuple[MeasuredDefinition, ...]:
    if not isinstance(value, list):
        raise ValueError(f"{RAYS_LAW}: measured must be a list")
    names = {family.name: index for index, family in enumerate(families)}
    found: list[MeasuredDefinition] = []
    for index, entry in enumerate(value):
        label = f"measured[{index}]"
        if isinstance(entry, dict) and CHARGE_KEY in entry:
            raise ValueError(
                f"{RAYS_LAW}: {label} declares {CHARGE_KEY}, a key removed on 2026-09-20: the "
                "charge of a measured event is its family's charge per unit of content times "
                "its content (the family's `charge`, an integer or [n, d]); see docs/MIGRATION.md"
            )
        obj = _object(entry, label, MEASURED_KEYS, {"position", "family", "amount"})
        position = _address(obj["position"], f"{label}.position", shape)
        if any(item.position == position for item in found):
            raise ValueError(f"{RAYS_LAW}: two measured events at one Node {list(position)}")
        family_name = obj["family"]
        if not isinstance(family_name, str) or family_name not in names:
            raise ValueError(f"{RAYS_LAW}: {label}.family names an unknown family")
        family = names[family_name]
        amount = _integer(obj["amount"], f"{label}.amount", 1)
        phased = families[family].phase
        if phased and 2 * amount >= clock * phase_steps:
            raise ValueError(
                f"{RAYS_LAW}: {label}.amount must keep 2 x content below K x N (the phase step "
                "per self-creation below half the circle)"
            )
        # A measured event of a family without a phase circle has phase 0.
        phase = _integer(obj.get("phase", 0), f"{label}.phase", 0, phase_steps - 1 if phased else 0)
        momentum_value = obj.get("momentum", [0, 0, 0])
        if not isinstance(momentum_value, list) or len(momentum_value) != 3:
            raise ValueError(f"{RAYS_LAW}: {label}.momentum must be three integers")
        momentum = tuple(_integer(item, f"{label}.momentum", -AMOUNT_BOUND) for item in momentum_value)
        fixed = obj.get("fixed", False)
        if type(fixed) is not bool:
            raise ValueError(f"{RAYS_LAW}: {label}.fixed must be true or false")
        directions = _directions(
            obj.get("directions", list(range(HEADING_OFFSET, FIXED_DIRECTIONS))),
            f"{label}.directions",
            table,
        )
        # The table the keys give; the declared entries override what they name.
        rules: list[str] = []
        windows: list[int | None] = []
        reads: list[str] = []
        for rule, window, component in default_table(families):
            rules.append(rule)
            windows.append(window)
            reads.append(component)
        declared = obj.get("table", {})
        if not isinstance(declared, dict):
            raise ValueError(f"{RAYS_LAW}: {label}.table must map family names to rules")
        for key, entry_value in declared.items():
            if key not in names:
                raise ValueError(f"{RAYS_LAW}: {label}.table names an unknown family {key!r}")
            rules[names[key]], windows[names[key]], reads[names[key]] = _table_entry(
                entry_value,
                f"{label}.table[{key!r}]",
                phase_steps,
                families[names[key]].phase,
                rules[names[key]],
            )
        if families[family].free:
            # The label of a free release: amount x D along a heading.
            _label_bound(amount * release[0] // release[1] or 1, 1, table, directions, label)
        lamp = None
        if "lamp" in obj:
            if families[family].free:
                raise ValueError(f"{RAYS_LAW}: {label}: a lamp is a measured event of a paid family")
            lamp = _lamp(
                obj["lamp"],
                f"{label}.lamp",
                phase_steps,
                phased,
                table,
                families[family].quantum,
                amount,
                clock,
            )
        found.append(
            MeasuredDefinition(
                position,
                family,
                amount,
                phase,
                (momentum[0], momentum[1], momentum[2]),
                fixed,
                directions,
                tuple(rules),
                tuple(windows),
                tuple(reads),
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
    table: tuple[Vector, ...],
) -> tuple[TransitDefinition, ...]:
    if not isinstance(value, list):
        raise ValueError(f"{RAYS_LAW}: in_transit must be a list")
    names = {family.name: index for index, family in enumerate(families)}
    found: list[TransitDefinition] = []
    for index, entry in enumerate(value):
        label = f"in_transit[{index}]"
        obj = _object(
            entry, label, TRANSIT_KEYS, {"position", "family", "number", "direction", "amount"}
        )
        family_name = obj["family"]
        if not isinstance(family_name, str) or family_name not in names:
            raise ValueError(f"{RAYS_LAW}: {label}.family names an unknown family")
        family = names[family_name]
        top = phase_steps - 1 if families[family].phase else 0
        direction = _direction(obj["direction"], f"{label}.direction", table, rest=True)
        amount = _integer(obj["amount"], f"{label}.amount", 1)
        # A declared ray of a paid family carries one phase step of content
        # per unit, quantum x 1 (no emitter declared its turn); a free one
        # carries none and its label is the amount along the direction.
        _label_bound(amount, families[family].unit_label, table, (direction,), label)
        found.append(
            TransitDefinition(
                _address(obj["position"], f"{label}.position", shape),
                family,
                _integer(obj["number"], f"{label}.number", 1, max(1, len(measured))),
                direction,
                amount,
                _integer(obj.get("phase", 0), f"{label}.phase", 0, top),
                _integer(obj.get("age", 0), f"{label}.age", 0),
            )
        )
    return tuple(found)


def _detectors(
    value: object, shape: Address3, measured: tuple[MeasuredDefinition, ...]
) -> tuple[DetectorDefinition, ...]:
    if not isinstance(value, list):
        raise ValueError(f"{RAYS_LAW}: detectors must be a list")
    at = {entry.position for entry in measured}
    taken: set[Address3] = set()
    found: list[DetectorDefinition] = []
    for index, entry in enumerate(value):
        label = f"detectors[{index}]"
        obj = _object(entry, label, DETECTOR_KEYS, {"name", "positions"})
        name = obj["name"]
        if not isinstance(name, str) or not name:
            raise ValueError(f"{RAYS_LAW}: {label}.name must be a nonempty string")
        if any(item.name == name for item in found):
            raise ValueError(f"{RAYS_LAW}: two detectors named {name!r}")
        if name in FACE_NAMES:
            raise ValueError(
                f"{RAYS_LAW}: {label}.name {name!r} is the name of a face detector (an open face "
                "of the board is a detector of that name; declare another)"
            )
        positions_value = obj["positions"]
        if not isinstance(positions_value, list) or not positions_value:
            raise ValueError(f"{RAYS_LAW}: {label}.positions must be a nonempty list of Nodes")
        positions = []
        for item in positions_value:
            position = _address(item, f"{label}.positions", shape)
            if position not in at:
                raise ValueError(
                    f"{RAYS_LAW}: {label}.positions names a Node without a measured event {list(position)}"
                )
            if position in taken:
                raise ValueError(f"{RAYS_LAW}: a Node in two detectors {list(position)}")
            taken.add(position)
            positions.append(position)
        threshold = _integer(obj.get("threshold", 1), f"{label}.threshold", 1)
        reading = obj.get("reading", DETECTOR_READINGS[0])
        if reading not in DETECTOR_READINGS:
            raise ValueError(
                f"{RAYS_LAW}: {label}.reading must be one of {list(DETECTOR_READINGS)}, not {reading!r}"
            )
        found.append(DetectorDefinition(name, tuple(positions), threshold, str(reading)))
    return tuple(found)


def parse_ray_world(document: object) -> RayWorld:
    """Reject anything but a lawful world of the law of the ray."""
    if not isinstance(document, dict):
        raise ValueError(f"{RAYS_LAW}: a world is a JSON object")
    old = [key for key in OLD_KEYS if key in document]
    if old:
        raise ValueError(
            f"{RAYS_LAW}: a world of the law of the ray declares none of the earlier engines' "
            f"keys ({', '.join(old)}); see docs/MIGRATION.md"
        )
    if document.get("law") == "events":
        raise ValueError(
            f'{RAYS_LAW}: "law": "events" names the law of events (events-v1), deleted on '
            '2026-09-19; a world of the law of the ray declares "law": "rays" (docs/MIGRATION.md)'
        )
    if document.get("law") != LAW_VALUE:
        raise ValueError(f'{RAYS_LAW}: a world of the law of the ray declares "law": "rays"')
    events = [key for key in EVENTS_KEYS if key in document]
    if events:
        raise ValueError(
            f"{RAYS_LAW}: a world of the law of the ray declares none of the law of events' keys "
            f"({', '.join(events)}); see docs/MIGRATION.md"
        )
    obj = _object(
        document,
        "the world",
        WORLD_KEYS,
        {"law", "model_id", "shape", "ticks", "K", "release", "families", "measured"},
    )
    model_id = obj["model_id"]
    if not isinstance(model_id, str) or not model_id:
        raise ValueError(f"{RAYS_LAW}: model_id must be a nonempty string")
    shape_value = obj["shape"]
    if not isinstance(shape_value, list) or len(shape_value) != 3:
        raise ValueError(f"{RAYS_LAW}: shape must be three positive extents")
    extents = tuple(_integer(item, "shape", 1, 4096) for item in shape_value)
    shape: Address3 = (extents[0], extents[1], extents[2])
    boundary, periodic = _boundary(obj.get("boundary", BOUNDARIES[0]))
    ticks = _integer(obj["ticks"], "ticks", 0)
    clock = _integer(obj["K"], "K", 1)
    phase_steps = _integer(obj.get("N", 64), "N", 2, MAX_PHASE_STEPS)
    if phase_steps & (phase_steps - 1):
        raise ValueError(f"{RAYS_LAW}: N must be a power of two from 2 through {MAX_PHASE_STEPS}")
    release = _ratio(obj["release"], "release", zero=True)
    suspension = _ratio(obj.get("suspension", 1), "suspension", zero=True)
    if suspension[0] == 0:
        # Off: 0 and [0, d] alike, recorded as [0, 1].
        suspension = (0, 1)
    # The width S of the push: one Link per (S x M + p) / p self-creations;
    # 1 (the rule as it was) unless the world declares it, never below 1.
    width = _integer(obj.get("width", 1), "width", 1)
    bound = _integer(obj.get("direction_bound", DEFAULT_DIRECTION_BOUND), "direction_bound", 1, 4096)
    table = _direction_table(obj.get("directions", []), bound)
    families = _families(obj["families"], phase_steps)
    measured = _measured(obj["measured"], shape, families, clock, phase_steps, release, table)
    in_transit = _in_transit(obj.get("in_transit", []), shape, families, measured, phase_steps, table)
    detectors = _detectors(obj.get("detectors", []), shape, measured)
    world = RayWorld(
        model_id,
        shape,
        boundary,
        periodic,
        ticks,
        clock,
        phase_steps,
        release,
        suspension,
        width,
        table,
        bound,
        families,
        measured,
        in_transit,
        detectors,
    )
    return world
