"""The world's files read into the GameBoard's world: the universe file (the integers and the families), the world file (the GameBoard with its inner faces, the bodies, the messages, the detectors) and the generator's mode file beside it (every body's and message's levels, `loader/mode.py`); every key checked, every other key refused as unknown by name, no default written (ALGEBRA.md #a-familys-declaration)."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass

from event_universe.core.integer import MAX_WORK_INT
from event_universe.core.rule3 import division_forward
from event_universe.loader import derived
from event_universe.loader.derived import CONTENT, SIGN, FamilyRule, count_wall
from event_universe.loader.faces import faces_of
from event_universe.loader.keys import AXES, Node, document_at, integer, keyed, node_of
from event_universe.loader.messages import MessageRow, messages_of
from event_universe.loader.mode import Levels, entry_of, levels_of, mode_entries

FACES = ("open", "periodic", "closed")
FACE_NAME = "face"  # the one detector of the open faces' layer
WORLD_KEYS: tuple[str, ...] = ("shape", "boundary", "face_depth", "faces", "ticks", "universe", "engine")
WORLD_KEYS += ("measured", "messages", "detectors")
WORLD_REQUIRED = ("shape", "boundary", "ticks", "universe", "engine", "measured", "detectors")
UNIVERSE_KEYS = ("integers", "families")
INTEGER_KEYS = ("node_clock", "quantum_action", "width")
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
DETECTOR_KEYS, START_KEYS = ("name", "positions", "block", "remainder"), ("mode",)


@dataclass(frozen=True)
class BodyRow:
    """A body as declared: its family, its Nodes in the declared order with their counts, the quanta of other families it holds laid over its Nodes (family, count per Node), and its family's two levels and its second level pair (the rotation sense, 0 for a neutral body) from the mode file, each the nonzero Nodes' flat x-major indexes with their levels."""

    family: int
    nodes: tuple[Node, ...]
    counts: tuple[int, ...]
    holds: tuple[tuple[int, tuple[int, ...]], ...]
    now: Levels
    before: Levels
    im_now: Levels
    im_before: Levels


@dataclass(frozen=True)
class DetectorRow:
    """A detector: its name and its Nodes (`positions`), one group whose click is a whole quantum's entry through one of its boundary Ports, or the body whose Nodes report each interval (`block`); and the count remainders the file declares at its Nodes at the start (`remainder`), per family of quanta by its index one value per Node in the positions' order, none for a body."""

    name: str
    positions: tuple[Node, ...]
    body: int | None
    remainders: tuple[tuple[int, tuple[int, ...]], ...]


@dataclass(frozen=True)
class World:
    """The world as loaded: the GameBoard's shape, which axes wrap and which are open, the open faces' depth, the Nodes declared beyond the board by its inner faces, the intervals, Gamma, T, the largest integer of the file's width, the amplitude bound A derived, the families, the bodies, the messages and the detectors."""

    shape: Node
    periodic: tuple[bool, bool, bool]
    open_axes: tuple[bool, bool, bool]
    face_depth: int
    beyond: tuple[Node, ...]
    ticks: int
    node_clock: int
    quantum_action: int
    width: int
    amplitude_bound: int
    families: tuple[FamilyRule, ...]
    bodies: tuple[BodyRow, ...]
    messages: tuple[MessageRow, ...]
    detectors: tuple[DetectorRow, ...]


def universe_of(document: object) -> tuple[dict[str, int], tuple[FamilyRule, ...]]:
    """The universe file: its integers and its families, each row its name, its pair and what it holds, the rest derived by the rule."""
    universe = keyed(document, "the universe file", UNIVERSE_KEYS, UNIVERSE_KEYS)
    raw = keyed(universe["integers"], "integers", INTEGER_KEYS, INTEGER_KEYS)
    integers = {key: integer(value, f"integers.{key}", 1) for key, value in raw.items()}
    integer(integers["width"], "integers.width", 1, MAX_WORK_INT.bit_length())
    entries = universe["families"]
    if not isinstance(entries, list) or not entries:
        raise ValueError("families must be a list of the families' rows")
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
        num = integer(pair[0], f"{label}.pair's num", -den, den)
        if abs(num) == den and num != den:
            raise ValueError(
                f"{label}.pair [{num}, {den}]: a massive pair has den above |num| (ALGEBRA.md)"
            )
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


def bodies_of(
    value: object,
    mode: object,
    digest: str,
    families: tuple[FamilyRule, ...],
    shape: Node,
    bound: int,
    beyond: tuple[Node, ...],
) -> tuple[BodyRow, ...]:
    """The bodies: each its family (a family of quanta), its Nodes with their counts (no Node shared, none beyond the board), the quanta of other families of quanta it holds, and its two levels from the mode file beside the world, which stands for this world by its digest; a body with no mode entry is refused by name."""
    names = {family.name: index for index, family in enumerate(families)}
    if not isinstance(value, list):
        raise ValueError("measured must be a list of bodies")
    entries = mode_entries(mode, digest, "bodies") if value else []
    taken, found = set(), []
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
            node = node_of(line["node"], f"{label}.nodes[{index}].node", shape, beyond)
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
        now, before, im_now, im_before = levels_of(
            entry_of(entries, number, label),
            f"the mode file's bodies[{number}]",
            families[family],
            shape,
            bound,
            beyond,
        )
        found.append(
            BodyRow(family, tuple(nodes), tuple(counts), tuple(holds), now, before, im_now, im_before)
        )
    return tuple(found)


def remainders_of(
    value: object, label: str, families: tuple[FamilyRule, ...], action: int, nodes: int
) -> tuple[tuple[int, tuple[int, ...]], ...]:
    """A detector's declared count remainders at the start (the advisor, #1515 comment 5907540901: the warm screen is declared, not earned): per family of quanta named as a key, an integer from 0 below that family's count wall W_c = 3 den T laid at every Node of the group, or a list of one such integer per Node in the positions' order; the engine holds no rule for their values."""
    names = {family.name: index for index, family in enumerate(families)}
    found = []
    for key, given in keyed(value, label, tuple(names), ()).items():
        index = names[key]
        if not families[index].quanta:
            raise ValueError(f"{label} names {key!r}, which carries no count: a family of quanta")
        wall = count_wall(families[index], action)
        values = given if isinstance(given, list) else [given] * nodes
        if len(values) != nodes:
            raise ValueError(
                f"{label}.{key} lists {len(values)} remainders for {nodes} Nodes: one per Node"
            )
        found.append((index, tuple(integer(v, f"{label}.{key}", 0, wall - 1) for v in values)))
    return tuple(found)


def detectors_of(
    value: object,
    shape: Node,
    bodies: int,
    beyond: tuple[Node, ...],
    families: tuple[FamilyRule, ...],
    action: int,
) -> tuple[DetectorRow, ...]:
    """The detectors: each a name of its own (not the faces' `face`) with its Nodes (none beyond the board), one group, or the body it names by its number; a group may declare its count remainders at the start (`remainder`), a body may not."""
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
            if "remainder" in row:
                raise ValueError(
                    f"{label} reads a body and lays no remainder: the body's start is the lay's"
                )
            body = integer(row["block"], f"{label}.block", 0, bodies - 1)
            found.append(DetectorRow(name, (), body, ()))
            continue
        positions = row["positions"]
        if not isinstance(positions, list) or not positions:
            raise ValueError(f"{label}.positions must list its Nodes")
        nodes = tuple(
            node_of(node, f"{label}.positions[{i}]", shape, beyond) for i, node in enumerate(positions)
        )
        declared = row.get("remainder", {})
        remainders = remainders_of(declared, f"{label}.remainder", families, action, len(nodes))
        found.append(DetectorRow(name, nodes, None, remainders))
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
    beyond = faces_of(world["faces"], shape) if "faces" in world else ()
    most = largest_count(world["measured"])
    gamma, action = integers["node_clock"], integers["quantum_action"]
    width = integers["width"]
    bound = derived.amplitude_bound(families, gamma, action, most, width)
    mode = next((doc for doc in files.values() if isinstance(doc, dict) and "world_digest" in doc), None)
    bodies = bodies_of(world["measured"], mode, digest, families, shape, bound, beyond)
    messages = messages_of(world.get("messages", []), mode, digest, families, shape, bound, beyond)
    detectors = detectors_of(world["detectors"], shape, len(bodies), beyond, families, action)
    return World(
        shape,
        (periodic[0], periodic[1], periodic[2]),
        (open_axes[0], open_axes[1], open_axes[2]),
        depth,
        beyond,
        integer(world["ticks"], "ticks", 0),
        gamma,
        action,
        derived.largest_of(width),
        bound,
        families,
        bodies,
        messages,
        detectors,
    )
