"""The world of the law of the shadow (field-only-v1): its keys and their refusals.

A world of this law is a JSON object with `"law": "shadow"` and nothing of the
old engine's schema (no `schema_version`, no spatial fields, no disturbance
types, no seeds, no marks, no bodies, no prefilled field): the two engines
refuse each other's worlds by name. What a world declares:

- `shape`, three positive extents; `boundary` `"open"` (the edge is infinity,
  what leaves is booked as escaped; a closed board is refused); `ticks`;
- `K`, the content per phase step per interval, one for the world; `N`, the
  steps of the phase circle (64 by default, a power of two from 2 through
  4096); `release` `[n, d]`, the shadows a held content of a free family
  releases per interval per Port heading per quantum of content (whole quanta
  with a remainder per Port); `wait_per_quantum`, the intervals a quantum
  waits per whole unit of size read (1 by default; an integer or `[n, d]`; 0
  for no wait);
- `families`: each with a `name`, a `kind` (`free`: matter, whose held content
  releases shadows at the world's rate and whose quanta are read for gravity
  and electricity; `paid`: light, released only by a lamp that spends its
  content, its quanta carrying their own momentum), for a free family the
  whole `charge` of a held content of it (0 by default), and `turns_in_flight`
  (whether the family's quanta turn their phase in flight by their amount
  over K on every Link: true by default for a paid family, false for a free
  one; what a matter shadow rotates by, a declared width since 2026-09-19),
  and `quantum` (the units of the family that make one event at a holder that
  absorbs them, `keep` or `rerelease`: the units of one number arriving at the
  holder wait in its register until a whole quantum is there, then one click
  or one re-release of that whole; 1 by default, every unit its own event);
- `contents`: the held contents, one per Node, each with a `position`, its
  `family`, its `amount` (a positive whole number of quanta, below K x N / 2),
  and optionally its `phase`, its whole `charge` (the family's by default), its
  `momentum` (three integers), `fixed` (true: an apparatus held in place, it
  takes pushes into its momentum and never steps), its `table` (family name to
  `read`, `keep`, `rerelease` or `pass`; a free family is read by default,
  the push taken and the units mixed on, and a paid family kept, the click)
  and, for a content of
  a paid family, its `lamp` (`rate` `[n, d]` quanta per interval per heading,
  `headings` the Port headings it releases on, all six by default); every
  content is given its number at parsing, 1, 2, ... in declaration order;
- `initial_shadows`, optional: shadows given with the board for speed, each
  with a `position`, `family`, `number` (the content whose field it is),
  `heading`, `amount` and `phase`, booked as initial content on the shadows'
  line; the default is an empty board that the emission fills.
"""

from __future__ import annotations

from dataclasses import dataclass

from event_universe.core.integer import bounded_gcd, checked_work
from event_universe.core.lattice import MAX_VALUE, PORT_HEADINGS, Address3

SHADOW_LAW = "field-only-v1"
LAW_VALUE = "shadow"
KINDS = ("free", "paid")
TABLES = ("read", "keep", "rerelease", "pass")
MAX_PHASE_STEPS = 4096
# The bound of an amount, a clock and a momentum component of this law: the
# layers hold 64-bit integers and the mixing's own guards bound a cell (an
# amount below about 7.6 x 10^9 per Port), so the schema bounds a declared
# number by the work register and not by the old engine's 32-bit cell.
AMOUNT_BOUND = (1 << 62) - 1
# Keys of the old engine's worlds, refused by name so that the refusal says
# which engine the world belongs to.
OLD_KEYS = (
    "schema_version",
    "fields",
    "disturbance_types",
    "seeds",
    "spatial_fields",
    "emissions",
    "spatial_seeds",
    "detectors",
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
    "wait_per_quantum",
    "families",
    "contents",
    "initial_shadows",
}
FAMILY_KEYS = {"name", "kind", "charge", "turns_in_flight", "quantum"}
CONTENT_KEYS = {"position", "family", "amount", "phase", "charge", "momentum", "fixed", "table", "lamp"}
LAMP_KEYS = {"rate", "headings"}
SHADOW_KEYS = {"position", "family", "number", "heading", "amount", "phase"}


@dataclass(frozen=True)
class FamilyDefinition:
    """One family of the world: its name, its kind, the whole charge of a
    held content of it, whether its quanta turn their phase in flight, and the
    units that make one event at a holder that absorbs them."""

    name: str
    kind: str
    charge: int
    turns: bool
    quantum: int

    @property
    def free(self) -> bool:
        return self.kind == "free"


@dataclass(frozen=True)
class LampDefinition:
    """A held content of a paid family that releases it at a declared rate,
    `rate` = (n, d) quanta per interval on each of its `headings` (Port
    indices), spending its content."""

    rate: tuple[int, int]
    headings: tuple[int, ...]


@dataclass(frozen=True)
class ContentDefinition:
    """One held content as declared: its Node, its family, its amount, its
    phase, its whole charge, its momentum, whether it is held in place, its
    table per family (in family order) and its lamp."""

    position: Address3
    family: int
    amount: int
    phase: int
    charge: int
    momentum: tuple[int, int, int]
    fixed: bool
    table: tuple[str, ...]
    lamp: LampDefinition | None


@dataclass(frozen=True)
class InitialShadow:
    """A shadow given with the board: at its Node, of its family and number, on
    its travel heading (a Port index), its amount and its phase."""

    position: Address3
    family: int
    number: int
    port: int
    amount: int
    phase: int


@dataclass(frozen=True)
class ShadowWorld:
    """A parsed world of the law of the shadow."""

    model_id: str
    shape: Address3
    ticks: int
    clock: int
    phase_steps: int
    release: tuple[int, int]
    wait: tuple[int, int]
    families: tuple[FamilyDefinition, ...]
    contents: tuple[ContentDefinition, ...]
    initial_shadows: tuple[InitialShadow, ...]

    @property
    def phase_mask(self) -> int:
        return self.phase_steps - 1

    def owners(self, family: int) -> tuple[int, ...]:
        """The numbers whose quanta of a family can exist: the contents that
        hold the family and are free (they release it), the lamps of it, and
        the contents whose table re-releases it (their number is stamped on
        what leaves them)."""
        found = []
        for index, content in enumerate(self.contents):
            number = index + 1
            definition = self.families[family]
            if (
                (content.family == family and (definition.free or content.lamp is not None))
                or content.table[family] == "rerelease"
                or any(
                    shadow.number == number and shadow.family == family
                    for shadow in self.initial_shadows
                )
            ):
                found.append(number)
        return tuple(found)

    def content_lcm(self) -> int:
        """The denominator of the electric reading, the least common multiple of
        the declared contents of the charged holders (1 without any)."""
        result = 1
        for content in self.contents:
            if content.charge:
                result = checked_work(result * content.amount) // bounded_gcd(result, content.amount)
        if result > AMOUNT_BOUND:
            raise ValueError(
                f"{SHADOW_LAW}: the charged contents' denominator exceeds the bounded integer"
            )
        return result


def is_shadow_world(document: object) -> bool:
    """Whether a document declares the law of the shadow (`"law": "shadow"`)."""
    return isinstance(document, dict) and document.get("law") == LAW_VALUE


def _object(value: object, label: str, allowed: set[str], required: set[str]) -> dict[str, object]:
    if not isinstance(value, dict):
        raise ValueError(f"{SHADOW_LAW}: {label} must be a JSON object")
    unknown = set(value) - allowed
    if unknown:
        raise ValueError(f"{SHADOW_LAW}: {label} has unknown keys: {', '.join(sorted(unknown))}")
    missing = required - set(value)
    if missing:
        raise ValueError(f"{SHADOW_LAW}: {label} lacks keys: {', '.join(sorted(missing))}")
    return {str(key): item for key, item in value.items()}


def _integer(value: object, label: str, minimum: int, maximum: int = AMOUNT_BOUND) -> int:
    if type(value) is not int or value < minimum or value > maximum:
        raise ValueError(f"{SHADOW_LAW}: {label} must be an integer from {minimum} through {maximum}")
    return value


def _ratio(value: object, label: str, zero: bool) -> tuple[int, int]:
    """A rate n / d as `[n, d]` (n from 0 with `zero`, d positive) or one integer."""
    if type(value) is int:
        return _integer(value, label, 0 if zero else 1), 1
    if not isinstance(value, list) or len(value) != 2:
        raise ValueError(f"{SHADOW_LAW}: {label} must be an integer or [numerator, denominator]")
    numerator = _integer(value[0], f"{label} numerator", 0 if zero else 1)
    denominator = _integer(value[1], f"{label} denominator", 1)
    return numerator, denominator


def _address(value: object, label: str, shape: Address3) -> Address3:
    if not isinstance(value, list) or len(value) != 3:
        raise ValueError(f"{SHADOW_LAW}: {label} must be three integers")
    found = tuple(
        _integer(item, label, 0, extent - 1) for item, extent in zip(value, shape, strict=True)
    )
    return found[0], found[1], found[2]


def _heading(value: object, label: str) -> int:
    if not isinstance(value, list) or len(value) != 3 or tuple(value) not in PORT_HEADINGS:
        raise ValueError(f"{SHADOW_LAW}: {label} must be one of the six Port headings")
    return PORT_HEADINGS.index((int(value[0]), int(value[1]), int(value[2])))


def _families(value: object) -> tuple[FamilyDefinition, ...]:
    if not isinstance(value, list) or not value:
        raise ValueError(f"{SHADOW_LAW}: families must be a nonempty list")
    found: list[FamilyDefinition] = []
    for index, entry in enumerate(value):
        obj = _object(entry, f"families[{index}]", FAMILY_KEYS, {"name", "kind"})
        name = obj["name"]
        if not isinstance(name, str) or not name:
            raise ValueError(f"{SHADOW_LAW}: families[{index}].name must be a nonempty string")
        if any(item.name == name for item in found):
            raise ValueError(f"{SHADOW_LAW}: two families named {name!r}")
        kind = obj["kind"]
        if kind not in KINDS:
            raise ValueError(f"{SHADOW_LAW}: families[{index}].kind must be free or paid")
        charge = _integer(obj.get("charge", 0), f"families[{index}].charge", -MAX_VALUE, MAX_VALUE)
        if kind == "paid" and charge:
            raise ValueError(f"{SHADOW_LAW}: a paid family carries no charge ({name})")
        turns = obj.get("turns_in_flight", kind == "paid")
        if type(turns) is not bool:
            raise ValueError(f"{SHADOW_LAW}: families[{index}].turns_in_flight must be true or false")
        quantum = _integer(obj.get("quantum", 1), f"families[{index}].quantum", 1, MAX_VALUE)
        found.append(FamilyDefinition(name, str(kind), charge, turns, quantum))
    return tuple(found)


def _lamp(value: object, label: str) -> LampDefinition:
    obj = _object(value, label, LAMP_KEYS, {"rate"})
    rate = _ratio(obj["rate"], f"{label}.rate", zero=True)
    headings_value = obj.get("headings", [list(heading) for heading in PORT_HEADINGS])
    if not isinstance(headings_value, list) or not headings_value:
        raise ValueError(f"{SHADOW_LAW}: {label}.headings must be a nonempty list of Port headings")
    headings = tuple(_heading(item, f"{label}.headings") for item in headings_value)
    if len(set(headings)) != len(headings):
        raise ValueError(f"{SHADOW_LAW}: {label}.headings repeats a heading")
    return LampDefinition(rate, headings)


def _contents(
    value: object,
    shape: Address3,
    families: tuple[FamilyDefinition, ...],
    clock: int,
    phase_steps: int,
) -> tuple[ContentDefinition, ...]:
    if not isinstance(value, list):
        raise ValueError(f"{SHADOW_LAW}: contents must be a list")
    names = {family.name: index for index, family in enumerate(families)}
    found: list[ContentDefinition] = []
    for index, entry in enumerate(value):
        label = f"contents[{index}]"
        obj = _object(entry, label, CONTENT_KEYS, {"position", "family", "amount"})
        position = _address(obj["position"], f"{label}.position", shape)
        if any(item.position == position for item in found):
            raise ValueError(f"{SHADOW_LAW}: two contents at one Node {list(position)}")
        family_name = obj["family"]
        if not isinstance(family_name, str) or family_name not in names:
            raise ValueError(f"{SHADOW_LAW}: {label}.family names an unknown family")
        family = names[family_name]
        amount = _integer(obj["amount"], f"{label}.amount", 1)
        if 2 * amount >= clock * phase_steps:
            raise ValueError(
                f"{SHADOW_LAW}: {label}.amount must keep 2 x content below K x N (the phase step "
                "per interval below half the circle)"
            )
        phase = _integer(obj.get("phase", 0), f"{label}.phase", 0, phase_steps - 1)
        charge = _integer(
            obj.get("charge", families[family].charge), f"{label}.charge", -MAX_VALUE, MAX_VALUE
        )
        if not families[family].free and charge:
            raise ValueError(f"{SHADOW_LAW}: {label}: a content of a paid family carries no charge")
        momentum_value = obj.get("momentum", [0, 0, 0])
        if not isinstance(momentum_value, list) or len(momentum_value) != 3:
            raise ValueError(f"{SHADOW_LAW}: {label}.momentum must be three integers")
        momentum = tuple(_integer(item, f"{label}.momentum", -AMOUNT_BOUND) for item in momentum_value)
        fixed = obj.get("fixed", False)
        if type(fixed) is not bool:
            raise ValueError(f"{SHADOW_LAW}: {label}.fixed must be true or false")
        table = ["read" if item.free else "keep" for item in families]
        declared = obj.get("table", {})
        if not isinstance(declared, dict):
            raise ValueError(f"{SHADOW_LAW}: {label}.table must map family names to rules")
        for key, rule in declared.items():
            if key not in names:
                raise ValueError(f"{SHADOW_LAW}: {label}.table names an unknown family {key!r}")
            if rule not in TABLES:
                raise ValueError(f"{SHADOW_LAW}: {label}.table[{key!r}] must be one of {TABLES}")
            table[names[key]] = str(rule)
        lamp = None
        if "lamp" in obj:
            if families[family].free:
                raise ValueError(f"{SHADOW_LAW}: {label}: a lamp is a held content of a paid family")
            lamp = _lamp(obj["lamp"], f"{label}.lamp")
        found.append(
            ContentDefinition(
                position,
                family,
                amount,
                phase,
                charge,
                (momentum[0], momentum[1], momentum[2]),
                fixed,
                tuple(table),
                lamp,
            )
        )
    return tuple(found)


def _initial_shadows(
    value: object,
    shape: Address3,
    families: tuple[FamilyDefinition, ...],
    contents: tuple[ContentDefinition, ...],
    phase_steps: int,
) -> tuple[InitialShadow, ...]:
    if not isinstance(value, list):
        raise ValueError(f"{SHADOW_LAW}: initial_shadows must be a list")
    names = {family.name: index for index, family in enumerate(families)}
    found: list[InitialShadow] = []
    for index, entry in enumerate(value):
        label = f"initial_shadows[{index}]"
        obj = _object(entry, label, SHADOW_KEYS, {"position", "family", "number", "heading", "amount"})
        family_name = obj["family"]
        if not isinstance(family_name, str) or family_name not in names:
            raise ValueError(f"{SHADOW_LAW}: {label}.family names an unknown family")
        found.append(
            InitialShadow(
                _address(obj["position"], f"{label}.position", shape),
                names[family_name],
                _integer(obj["number"], f"{label}.number", 1, len(contents)),
                _heading(obj["heading"], f"{label}.heading"),
                _integer(obj["amount"], f"{label}.amount", 1),
                _integer(obj.get("phase", 0), f"{label}.phase", 0, phase_steps - 1),
            )
        )
    return tuple(found)


def parse_shadow_world(document: object) -> ShadowWorld:
    """Reject anything but a lawful world of the law of the shadow."""
    if not isinstance(document, dict):
        raise ValueError(f"{SHADOW_LAW}: a world is a JSON object")
    old = [key for key in OLD_KEYS if key in document]
    if old:
        raise ValueError(
            f"{SHADOW_LAW}: a world of the law of the shadow declares none of the old engine's "
            f"keys ({', '.join(old)}); run it with the old engine or remove them"
        )
    if document.get("law") != LAW_VALUE:
        raise ValueError(f'{SHADOW_LAW}: a world of the law of the shadow declares "law": "shadow"')
    obj = _object(
        document,
        "the world",
        WORLD_KEYS,
        {"law", "model_id", "shape", "ticks", "K", "release", "families", "contents"},
    )
    model_id = obj["model_id"]
    if not isinstance(model_id, str) or not model_id:
        raise ValueError(f"{SHADOW_LAW}: model_id must be a nonempty string")
    shape_value = obj["shape"]
    if not isinstance(shape_value, list) or len(shape_value) != 3:
        raise ValueError(f"{SHADOW_LAW}: shape must be three positive extents")
    extents = tuple(_integer(item, "shape", 1, 4096) for item in shape_value)
    shape: Address3 = (extents[0], extents[1], extents[2])
    if obj.get("boundary", "open") != "open":
        raise ValueError(
            f"{SHADOW_LAW}: the board is open (its edge is infinity); a closed board is refused"
        )
    ticks = _integer(obj["ticks"], "ticks", 0)
    clock = _integer(obj["K"], "K", 1)
    phase_steps = _integer(obj.get("N", 64), "N", 2, MAX_PHASE_STEPS)
    if phase_steps & (phase_steps - 1):
        raise ValueError(f"{SHADOW_LAW}: N must be a power of two from 2 through {MAX_PHASE_STEPS}")
    release = _ratio(obj["release"], "release", zero=True)
    wait = _ratio(obj.get("wait_per_quantum", 1), "wait_per_quantum", zero=True)
    families = _families(obj["families"])
    contents = _contents(obj["contents"], shape, families, clock, phase_steps)
    shadows = _initial_shadows(obj.get("initial_shadows", []), shape, families, contents, phase_steps)
    world = ShadowWorld(
        model_id, shape, ticks, clock, phase_steps, release, wait, families, contents, shadows
    )
    world.content_lcm()
    return world
