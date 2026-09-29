"""The world's files read into the GameBoard's world: the universe file (the integers and the families), the world file (the GameBoard, the bodies, the detectors) and the generator's mode file beside it (every body's levels); every key checked, every other key refused as unknown by name, no default written (ALGEBRA.md #a-familys-declaration)."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from typing import Any

from event_universe.core.integer import MAX_WORK_INT
from event_universe.core.rule3 import division_forward
from event_universe.loader import derived
from event_universe.loader.derived import CONTENT, SIGN, FamilyRule

Node = tuple[int, int, int]
AXES = ("x", "y", "z")
FACES = ("open", "periodic", "closed")
FACE_NAME = "face"  # the one detector of the open faces' layer
WORLD_KEYS = ("shape", "boundary", "face_depth", "ticks", "universe", "engine", "measured", "detectors")
WORLD_REQUIRED = ("shape", "boundary", "ticks", "universe", "engine", "measured", "detectors")
UNIVERSE_KEYS = ("integers", "families")
INTEGER_KEYS = ("node_clock", "quantum_action", "width", "most_families")
INTEGER_REQUIRED = ("node_clock", "quantum_action")
FAMILY_KEYS, FAMILY_REQUIRED, HELD_KEYS = (
    ("name", "pair", "held"),
    ("name", "pair"),
    ("count", "divisor"),
)
BODY_KEYS, BODY_REQUIRED, NODE_KEYS = (
    ("family", "nodes", "holds"),
    ("family", "nodes"),
    ("node", "count"),
)
DETECTOR_KEYS, START_KEYS = ("name", "positions", "block"), ("mode",)
MODE_KEYS = ("world_digest", "bodies")
MODE_BODY_KEYS = (
    "family",
    "pair",
    "count",
    "seed",
    "carried",
    "period",
    "amplitude",
    "clock",
    "profile",
    "moving",
)
MOVING_KEYS = ("now", "before")


@dataclass(frozen=True)
class BodyRow:
    """A body as declared: its family, its Nodes in the declared order with their counts, the quanta of other families it holds laid over its Nodes (family, count per Node), and its family's two levels from the mode file over the whole GameBoard in x-major order."""

    family: int
    nodes: tuple[Node, ...]
    counts: tuple[int, ...]
    holds: tuple[tuple[int, tuple[int, ...]], ...]
    now: tuple[int, ...]
    before: tuple[int, ...]


@dataclass(frozen=True)
class DetectorRow:
    """A detector: its name and its Nodes (`positions`), or the body whose Nodes report each interval (`block`)."""

    name: str
    positions: tuple[Node, ...]
    body: int | None


@dataclass(frozen=True)
class World:
    """The world as loaded: the GameBoard's shape, which axes wrap and which are open, the open faces' depth, the intervals, Gamma, T, the amplitude bound A derived, the families, the bodies and the detectors."""

    shape: Node
    periodic: tuple[bool, bool, bool]
    open_axes: tuple[bool, bool, bool]
    face_depth: int
    ticks: int
    node_clock: int
    quantum_action: int
    amplitude_bound: int
    families: tuple[FamilyRule, ...]
    bodies: tuple[BodyRow, ...]
    detectors: tuple[DetectorRow, ...]


def keyed(
    value: object, label: str, allowed: tuple[str, ...], required: tuple[str, ...]
) -> dict[str, Any]:
    """An object of the files: every key it holds among `allowed` and every key of `required` present, refused by name otherwise."""
    if not isinstance(value, dict):
        raise ValueError(f"{label} must be an object")
    unknown = sorted(set(value) - set(allowed))
    if unknown:
        raise ValueError(f"{label} holds the unknown key {unknown[0]!r}: its keys are {list(allowed)}")
    lacking = [key for key in required if key not in value]
    if lacking:
        raise ValueError(f"{label} lacks the key {lacking[0]!r}")
    return value


def integer(value: object, label: str, least: int, most: int = MAX_WORK_INT) -> int:
    """An integer of the files within [least, most], refused by name otherwise."""
    if type(value) is not int or not least <= value <= most:
        raise ValueError(f"{label} must be an integer from {least} through {most}, got {value!r}")
    return value


def node_of(value: object, label: str, shape: Node) -> Node:
    """A Node's address on the GameBoard, three integers inside the shape."""
    if not isinstance(value, list) or len(value) != 3:
        raise ValueError(f"{label} must be a Node [x, y, z]")
    found = tuple(integer(value[axis], f"{label}[{axis}]", 0, shape[axis] - 1) for axis in range(3))
    return found[0], found[1], found[2]


def document_at(files: Mapping[str, object], path: object, label: str) -> object:
    """The document the world names by its repository path, refused by name where the host read no file there."""
    if not isinstance(path, str) or path not in files:
        raise ValueError(f"{label} names {path!r}, and no file stands at that repository path")
    return files[path]


def universe_of(document: object) -> tuple[dict[str, int], tuple[FamilyRule, ...]]:
    """The universe file: its integers and its families, each row its name, its pair and what it holds, the rest derived by the rule."""
    universe = keyed(document, "the universe file", UNIVERSE_KEYS, UNIVERSE_KEYS)
    raw = keyed(universe["integers"], "integers", INTEGER_KEYS, INTEGER_REQUIRED)
    integers = {key: integer(value, f"integers.{key}", 1) for key, value in raw.items()}
    if "width" in integers and integers["width"] != MAX_WORK_INT.bit_length():
        raise ValueError(
            f"integers.width {integers['width']} is not this host's working width {MAX_WORK_INT.bit_length()} bits"
        )
    entries = universe["families"]
    if not isinstance(entries, list) or not entries:
        raise ValueError("families must be a list of the families' rows")
    if len(entries) > integers.get("most_families", len(entries)):
        raise ValueError(f"the universe holds {len(entries)} families, above most_families")
    rows: list[tuple[str, tuple[int, int], str | None, int | None]] = []
    for index, entry in enumerate(entries):
        label = f"families[{index}]"
        row = keyed(entry, label, FAMILY_KEYS, FAMILY_REQUIRED)
        name = row["name"]
        if not isinstance(name, str) or not name or name in [found[0] for found in rows]:
            raise ValueError(f"{label}.name must be a name of its own")
        pair = row["pair"]
        if not isinstance(pair, list) or len(pair) != 2:
            raise ValueError(f"{label}.pair must be [num, den]")
        den = integer(pair[1], f"{label}.pair's den", 1)
        num = integer(pair[0], f"{label}.pair's num", 1, den)
        held, divisor = None, None
        if "held" in row:
            holds = keyed(row["held"], f"{label}.held", HELD_KEYS, HELD_KEYS)
            if holds["count"] not in (CONTENT, SIGN):
                raise ValueError(
                    f"{label}.held.count is {CONTENT!r} or {SIGN!r}, got {holds['count']!r}"
                )
            held, divisor = str(holds["count"]), integer(holds["divisor"], f"{label}.held.divisor", 1)
        rows.append((name, (num, den), held, divisor))
    return integers, derived.family_rules(rows)


def spread(total: int, counts: tuple[int, ...]) -> tuple[int, ...]:
    """A body's held quanta laid over its Nodes in proportion to its own counts by Rule3's carried division, the remainder carried from Node to Node in the declared order, so no quantum is lost to a Node's rounding."""
    whole, carry, found = sum(counts), 0, []
    for count in counts:
        share, carry = division_forward(total * count, whole, carry)
        found.append(int(share))
    return tuple(found)


def levels_of(
    entry: object, label: str, family: FamilyRule, size: int, bound: int
) -> tuple[tuple[int, ...], ...]:
    """A body's two levels from its mode entry: `moving`'s now and before where written, else the profile at both levels, each one integer per Node in x-major order, not all zero and within the amplitude bound A."""
    mode = keyed(entry, label, MODE_BODY_KEYS, ("family", "pair", "profile"))
    if mode["family"] != family.name or mode["pair"] != list(family.pair):
        raise ValueError(
            f"{label} is of the family {mode['family']!r} with the pair {mode['pair']}, the body of "
            f"{family.name!r} with {list(family.pair)}"
        )
    words = (
        keyed(mode["moving"], f"{label}.moving", MOVING_KEYS, MOVING_KEYS) if "moving" in mode else {}
    )
    found = []
    for word in MOVING_KEYS:
        values = words.get(word, mode["profile"])
        if (
            not isinstance(values, list)
            or len(values) != size
            or any(type(v) is not int for v in values)
        ):
            raise ValueError(
                f"{label}'s {word} level must be {size} integers, one per Node in x-major order"
            )
        largest = max(abs(v) for v in values)
        if largest == 0 or largest > bound:
            raise ValueError(
                f"{label}'s {word} level reaches {largest}: not all zero and at most A = {bound}"
            )
        found.append(tuple(values))
    return found[0], found[1]


def bodies_of(
    value: object, mode: object, digest: str, families: tuple[FamilyRule, ...], shape: Node, bound: int
) -> tuple[BodyRow, ...]:
    """The bodies: each its family (a family of quanta), its Nodes with their counts (no Node shared), the quanta of other families of quanta it holds, and its two levels from the mode file beside the world, which stands for this world by its digest; a body with no mode entry is refused by name."""
    names = {family.name: index for index, family in enumerate(families)}
    if not isinstance(value, list):
        raise ValueError("measured must be a list of bodies")
    entries: list[object] = []
    if value:
        written = keyed(mode, "the mode file beside the world", MODE_KEYS, MODE_KEYS)
        if written["world_digest"] != digest:
            raise ValueError(
                f"the mode file's world_digest {written['world_digest']} is not this world's digest {digest}: "
                "the mode file stands beside another world, or the world changed after the generator wrote it"
            )
        entries = written["bodies"] if isinstance(written["bodies"], list) else []
    size, taken, found = shape[0] * shape[1] * shape[2], set(), []
    for number, entry in enumerate(value):
        label = f"measured[{number}]"
        body = keyed(entry, label, BODY_KEYS, BODY_REQUIRED)
        family = names.get(body["family"])
        if family is None or not families[family].quanta:
            raise ValueError(f"{label}.family must name a family of quanta, got {body['family']!r}")
        lines = body["nodes"]
        if not isinstance(lines, list) or not lines:
            raise ValueError(f"{label}.nodes must list the body's Nodes with their counts")
        nodes, counts = [], []
        for index, line in enumerate(lines):
            keyed(line, f"{label}.nodes[{index}]", NODE_KEYS, NODE_KEYS)
            node = node_of(line["node"], f"{label}.nodes[{index}].node", shape)
            if node in taken:
                raise ValueError(
                    f"{label}: two bodies share the Node {list(node)}; they stand apart or are one body"
                )
            taken.add(node)
            nodes.append(node)
            counts.append(integer(line["count"], f"{label}.nodes[{index}].count", 1))
        holds = []
        for key, total in keyed(body.get("holds", {}), f"{label}.holds", tuple(names), ()).items():
            other = names[key]
            if other == family or not families[other].quanta:
                raise ValueError(f"{label}.holds names {key!r}: the quanta of another family of quanta")
            holds.append((other, spread(integer(total, f"{label}.holds.{key}", 1), tuple(counts))))
        if number >= len(entries):
            raise ValueError(
                f"{label} has no entry in the mode file beside the world: its levels are the generator's"
            )
        now, before = levels_of(
            entries[number], f"the mode file's bodies[{number}]", families[family], size, bound
        )
        found.append(BodyRow(family, tuple(nodes), tuple(counts), tuple(holds), now, before))
    return tuple(found)


def detectors_of(value: object, shape: Node, bodies: int) -> tuple[DetectorRow, ...]:
    """The detectors: each a name of its own (not the faces' `face`) with its Nodes or the body it names by its number."""
    if not isinstance(value, list):
        raise ValueError("detectors must be a list")
    found: list[DetectorRow] = []
    for index, entry in enumerate(value):
        label = f"detectors[{index}]"
        row = keyed(entry, label, DETECTOR_KEYS, ("name",))
        name = row["name"]
        if not isinstance(name, str) or name == FACE_NAME or name in [d.name for d in found]:
            raise ValueError(f"{label}.name must be a name of its own, not {FACE_NAME!r}")
        if ("positions" in row) == ("block" in row):
            raise ValueError(f"{label} declares its `positions` or the `block` it reads, one of the two")
        if "block" in row:
            found.append(DetectorRow(name, (), integer(row["block"], f"{label}.block", 0, bodies - 1)))
            continue
        positions = row["positions"]
        if not isinstance(positions, list) or not positions:
            raise ValueError(f"{label}.positions must list its Nodes")
        nodes = tuple(
            node_of(node, f"{label}.positions[{i}]", shape) for i, node in enumerate(positions)
        )
        found.append(DetectorRow(name, nodes, None))
    return tuple(found)


def largest_count(measured: object) -> int:
    """The largest count a body declares at a Node, the count's line's bound reads it (0 where none is declared; the counts are checked with their bodies)."""
    found = [0]
    for body in measured if isinstance(measured, list) else []:
        for line in body.get("nodes", []) if isinstance(body, dict) else []:
            if isinstance(line, dict) and type(line.get("count")) is int:
                found.append(line["count"])
    return max(found)


def parse_world(document: object, files: Mapping[str, object], digest: str) -> World:
    """The world from its document, the files it names (the universe, the engine start file, the mode file beside it, read by the host) and its digest; every defect refused by name."""
    world = keyed(document, "the world", WORLD_KEYS, WORLD_REQUIRED)
    keyed(document_at(files, world["engine"], "engine"), "the engine start file", START_KEYS, START_KEYS)
    integers, families = universe_of(document_at(files, world["universe"], "universe"))
    shape_value = world["shape"]
    if not isinstance(shape_value, list) or len(shape_value) != 3:
        raise ValueError("shape must be [X, Y, Z]")
    extents = tuple(integer(extent, f"shape[{axis}]", 1) for axis, extent in enumerate(shape_value))
    shape = (extents[0], extents[1], extents[2])
    faces = keyed(world["boundary"], "boundary", AXES, AXES)
    if any(faces[axis] not in FACES for axis in AXES):
        raise ValueError(f"boundary gives every axis one of {list(FACES)}")
    periodic = tuple(faces[axis] == "periodic" for axis in AXES)
    open_axes = tuple(faces[axis] == "open" for axis in AXES)
    if any(open_axes) and "face_depth" not in world:
        raise ValueError(
            "face_depth is required on a GameBoard with an open face: the depth of its layer"
        )
    depth = integer(world["face_depth"], "face_depth", 1) if "face_depth" in world else 0
    most = largest_count(world["measured"])
    gamma, action = integers["node_clock"], integers["quantum_action"]
    bound = derived.amplitude_bound(families, gamma, action, most)
    mode = next((doc for doc in files.values() if isinstance(doc, dict) and "world_digest" in doc), None)
    bodies = bodies_of(world["measured"], mode, digest, families, shape, bound)
    detectors = detectors_of(world["detectors"], shape, len(bodies))
    return World(
        shape,
        (periodic[0], periodic[1], periodic[2]),
        (open_axes[0], open_axes[1], open_axes[2]),
        depth,
        integer(world["ticks"], "ticks", 0),
        gamma,
        action,
        bound,
        families,
        bodies,
        detectors,
    )
