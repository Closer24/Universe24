"""The world's files read into the GameBoard's world: the universe file (the integers and the families), the world file (the GameBoard with its inner faces, the bodies, the messages, the node_readers) and the generator's mode file beside it (every body's and message's levels, `loader/mode.py`); every key checked, every other key refused as unknown by name, no default written (ALGEBRA.md #a-familys-declaration)."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass

import numpy as np

from event_universe.core.integer import MAX_WORK_INT
from event_universe.loader import derived
from event_universe.loader.derived import FamilyRule
from event_universe.loader.draw import (
    Draw,
    Pattern,
    basis_of,
    draw_of,
    pattern_of,
    patterns_of_the_law,
    ports_of,
)
from event_universe.loader.faces import RecedingFace, faces_of, layer_of, receding_of
from event_universe.loader.keys import AXES, Node, document_at, integer, keyed, node_of, weights_of
from event_universe.loader.lay import Lay, budget_gate, lay_of
from event_universe.loader.messages import MessageRow, WholeMessage, messages_of, wholes_of
from event_universe.loader.mode import Levels, entry_of, levels_of, mode_entries
from event_universe.loader.node_reader_declaration import (
    READER_RECORD_KEYS,
    NodeReaderDeclaration,
    node_reader_of,
    packet_form,
)
from event_universe.loader.node_reader_rows import reader_count
from event_universe.loader.universe import universe_of

FACES = ("open", "periodic", "closed")
FACE_NAME = "face"  # the one node_reader of the open faces' layer
WORLD_KEYS: tuple[str, ...] = ("shape", "boundary", "face_depth", "faces", "ticks", "universe", "engine")
WORLD_KEYS += ("bodies", "messages", "node_readers", "receding", "draw", "lay")
WORLD_REQUIRED = ("shape", "boundary", "ticks", "universe", "engine", "bodies", "node_readers")
BODY_KEYS, BODY_REQUIRED, NODE_KEYS = (
    ("family", "nodes", "weights", "count", *READER_RECORD_KEYS),
    ("family", "nodes"),
    ("node", "count", "weight"),
)
READER_NODE_KEYS = (
    "node",
    "weight",
)  # a reader's Node: its lay's weight, the record's count declared once
NODEREADER_KEYS = ("name", "positions", "block", "basis", "pattern")  # a node_reader's keys
TRANSITION = (
    "transition"  # a region's own quantum, declared by no region: its unit is its record's own share
)
START_KEYS = ("mode",)


@dataclass(frozen=True)
class BodyRow:
    """A body as declared: its family, its Nodes in the declared order with their counts (checked at the start against its record's share in quanta, a reading), and its family's two levels and its second level pair (the rotation sense, 0 for a neutral body) from the mode file, each the nonzero Nodes' flat x-major indexes with their levels; or, a body laid in its parts at one Node (`reader`, `loader/node_reader_declaration.py`: its parts the modes' labels with the count in one of them, and as a NodeReader its transitions, its givings and its own draw), whose lay is the engine's own at the start and whose levels the mode file does not hold (ALGEBRA.md, The click writes on the GameBoard (j); the owner's word, the body is at a Node). A laid body carries the weight of its laid pair on each line of its record (`weights`, 1 on every line without the key; `keys.weights_of`)."""

    family: int
    nodes: tuple[Node, ...]
    counts: tuple[int, ...]
    now: Levels
    before: Levels
    second_now: Levels
    second_before: Levels
    weights: tuple[int, ...] = ()
    reader: NodeReaderDeclaration | None = None


@dataclass(frozen=True)
class NodeReaderRow:
    """A node_reader: its name and its Nodes (`positions`), one region whose click is its report of the net current into it through its front boundary Ports each interval, or the body whose Nodes report each interval (`block`); `declared` where it is a region of the declared NodeReader, and not for a body's node_reader nor for the open faces' layer, the board's own region named `face` (`FACE_NAME`), which the loader adds last where an open face does not recede; `basis`, the reader's declared setting (p, q), the coefficients of its credit, and `pattern`, one integer pair per part of the record it reads, how each part reads the setting at the + port and the - port (the pair's (p, q) and (-q, p), ALGEBRA.md #the-click-is-the-meeting; `loader/draw.py`), read by the reader and by the draw through the root in the run, each empty where none is declared; no quantum of its own, a region counting in its record's own unit (`credit.record_unit`; the key `transition` refused by name)."""

    name: str
    positions: tuple[Node, ...]
    body: int | None
    declared: bool
    basis: tuple[int, ...]
    pattern: Pattern


@dataclass(frozen=True)
class World:
    """The world as loaded: the GameBoard's shape, which axes wrap and which are open, the open faces' depth, the Nodes declared beyond the board by its inner faces, the intervals, Gamma, T, the largest integer of the file's width, the kind of the run's arrays chosen by the width (`kind_of`), the amplitude bound A derived, the families, the bodies, the messages laid at the start, the node_readers, the receding faces, the lay declared with its tolerance (the budget's gate on T at load, `loader/lay.py`), the NodeReaders' draw (`draw`, `loader/draw.py`, None where the world declares none: no draw and no write, the run as before the click entered the engine), and the messages laid whole at a tick of the run (`wholes`, `loader/messages.py`, the probe of the pulsed gate)."""

    shape: Node
    periodic: tuple[bool, bool, bool]
    open_axes: tuple[bool, bool, bool]
    face_depth: int
    beyond: tuple[Node, ...]
    ticks: int
    node_clock: int
    quantum_action: int
    width: int
    link_unit: int
    kind: type
    amplitude_bound: int
    families: tuple[FamilyRule, ...]
    bodies: tuple[BodyRow, ...]
    messages: tuple[MessageRow, ...]
    node_readers: tuple[NodeReaderRow, ...]
    receding: tuple[RecedingFace, ...]
    draw: Draw | None
    lay: Lay | None  # the lay the world declares for its bodies and its tolerance (`loader/lay.py`)
    wholes: tuple[
        WholeMessage, ...
    ] = ()  # the messages laid whole at a tick of the run (`loader/messages.py`)


def kind_of(width: int) -> type:
    """The kind of the run's arrays from the declared width, the one place the engine's integers are chosen (the owner, "choose 64 or 128 bits outside the engine, at the start"): the host's 64-bit integers where the width is at or under the host's signed bits, Python's integers (arrays of objects, exact at any width and slow) above it; the amplitude bound A is derived at the declared width either way (ENGINE.md, the loader)."""
    return np.int64 if width <= MAX_WORK_INT.bit_length() else object


def bodies_of(
    value: object,
    mode: object,
    digest: str,
    families: tuple[FamilyRule, ...],
    shape: Node,
    bound: int,
    beyond: tuple[Node, ...],
    action: int,
    periodic: tuple[bool, bool, bool] = (False, False, False),
) -> tuple[BodyRow, ...]:
    """The bodies: each its family (a family of quanta), its Nodes with their counts (no Node shared, none beyond the board; a body of a family that reads a holder of the sign, `derived.charged`, is one quantum of its family, one Node with the count 1, and a count above it is refused by name with the way to declare many quanta, that many bodies of count 1, each its own record and its own row of the sign, ALGEBRA.md, No record reads its own write of the sign) and its two levels from the mode file beside the world, which stands for this world by its digest, the mode's entries in the order of the bodies it lays; a body with no mode entry is refused by name; a body declaring its `parts` (and as a reader its `transitions`, `rates` and `node_reader`) or its `conversion` (the record converted whole, with its `node_reader` and its `count`) takes no mode entry, its Nodes listed with the lay's `weight` each (1 where absent, no `count` on a reader's Node: the record's count is declared once, by its parts or by `count`) and its lay the engine's own over its region (`node_reader_of`; its givings' lay decided by the board's shape against the declared width at the quantum action T, `packet_form`), and optionally `weights`, the laid pair's weight per line of its record (`keys.weights_of`, a record of real lines')."""
    names = {family.name: index for index, family in enumerate(families)}
    quanta = {name: index for name, index in names.items() if families[index].quanta}
    if not isinstance(value, list):
        raise ValueError("bodies must be a list of bodies")
    laid = [entry for entry in value if not any(key in entry for key in READER_RECORD_KEYS)]
    entries = mode_entries(mode, digest, "bodies") if laid else []
    taken, found = set(), []
    for number, entry in enumerate(value):
        label = f"bodies[{number}]"
        body = keyed(entry, label, BODY_KEYS, BODY_REQUIRED)
        family = names.get(body["family"])
        if family is None or not families[family].quanta:
            raise ValueError(f"{label}.family must name a family of quanta, got {body['family']!r}")
        lines = body["nodes"]
        if not isinstance(lines, list) or not lines:
            raise ValueError(f"{label}.nodes must list the body's Nodes with their counts")
        parted = entry not in laid  # a reader with its own record: one Node or more
        nodes, counts = [], []
        for index, line in enumerate(lines):
            if parted:  # a reader's Node carries the lay's weight (1 where absent); its count is the record's, once
                keyed(line, f"{label}.nodes[{index}]", READER_NODE_KEYS, ("node",))
            else:
                keyed(line, f"{label}.nodes[{index}]", ("node", "count"), ("node", "count"))
            node = node_of(line["node"], f"{label}.nodes[{index}].node", shape, beyond)
            if node in taken:
                raise ValueError(
                    f"{label}: two bodies share the Node {list(node)}; they stand apart or are one body"
                )
            taken.add(node)
            nodes.append(node)
            key = "weight" if parted else "count"
            counts.append(integer(line.get(key, 1), f"{label}.nodes[{index}].{key}", 1))
        if not parted and derived.charged(families, family) and sum(counts) > 1:
            raise ValueError(
                f"{label} declares the count {sum(counts)} of {body['family']!r}, a family that reads the holder "
                "of the sign: such a record is one quantum of its family, one Node with the count 1, and many "
                "quanta are that many bodies of count 1, each laid by the generator as the one-Node record of "
                "its quantum (tools/pixel_mode.py, --pixel) and its own record with its own row of the sign "
                "(ALGEBRA.md, No record reads its own write of the sign)"
            )
        if parted:
            if not connected(tuple(nodes), shape, periodic):
                raise ValueError(
                    f"{label} declares its own record over a region in pieces: a reader's Nodes are one connected "
                    "region through the six Ports (ALGEBRA.md, The NodeReader is one declaration kind for every "
                    "experiment); its Nodes are {[list(n) for n in nodes]}"
                )
            count = reader_count(body, label, families, family)
            parts = node_reader_of(body, label, families, family, quanta, count)
            parts = packet_form(parts, label, families, nodes[0], shape, action)
            found.append(BodyRow(family, tuple(nodes), tuple(counts), (), (), (), (), (), parts))
            continue
        placed = laid.index(entry)
        now, before, second_now, second_before = levels_of(
            entry_of(entries, placed, label),
            f"the mode file's bodies[{placed}]",
            families[family],
            shape,
            bound,
            beyond,
        )
        weights = weights_of(
            body.get("weights"), f"{label}.weights", families[family].laid, families[family].plane
        )
        found.append(
            BodyRow(family, tuple(nodes), tuple(counts), now, before, second_now, second_before, weights)
        )
    return tuple(found)


def node_readers_of(
    value: object,
    shape: Node,
    bodies: int,
    beyond: tuple[Node, ...],
    layer: tuple[Node, ...],
) -> tuple[NodeReaderRow, ...]:
    """The node_readers: each a name of its own (not the faces' `face`) with its Nodes (none beyond the board), one region of the declared NodeReader, optionally with its `basis`, the reader's setting (p, q), a list of integers not all 0, and its `pattern`, one integer pair per part of the record it reads (the reader's declaration and the draw's through the root, `loader/draw.py`; a pattern without a basis, and two ports not orthogonal, are refused by name), or the body it names by its number (no basis); a region declares no quantum of its own, its unit of one quantum being its record's own share per quantum read from the credit's books (`credit.record_unit`; the advisor's line with the mathematician's second, two hands), so the key `transition` is refused by name; after them the open faces' layer where there is one (`layer`), the board's own region under the name `face`, no part of the declared NodeReader."""
    if not isinstance(value, list):
        raise ValueError("node_readers must be a list")
    found: list[NodeReaderRow] = []
    for index, entry in enumerate(value):
        label = f"node_readers[{index}]"
        if isinstance(entry, dict) and TRANSITION in entry:
            raise ValueError(
                f"{label} holds the key {TRANSITION!r}: a region declares no quantum of its own, its unit of one "
                "quantum being its record's own share per quantum, read from the credit's books and not declared"
            )
        row = keyed(entry, label, NODEREADER_KEYS, ("name",))
        name = row["name"]
        if not isinstance(name, str) or name == FACE_NAME or name in [d.name for d in found]:
            raise ValueError(f"{label}.name must be a name of its own, not {FACE_NAME!r}")
        if ("positions" in row) == ("block" in row):
            raise ValueError(f"{label} declares its `positions` or the `block` it reads, one of the two")
        basis = basis_of(row["basis"], f"{label}.basis") if "basis" in row else ()
        if "pattern" in row and not basis:
            raise ValueError(f"{label}.pattern reads the setting `basis` declares, and none is declared")
        pattern = pattern_of(row["pattern"], f"{label}.pattern", basis) if "pattern" in row else ()
        if pattern:
            ports_of(
                basis, pattern
            )  # the two ports orthogonal with equal norms, refused by name otherwise
        if "block" in row:
            if basis:
                raise ValueError(
                    f"{label}: a basis is declared on a region, not on a body's node_reader"
                )
            body = integer(row["block"], f"{label}.block", 0, bodies - 1)
            found.append(NodeReaderRow(name, (), body, False, (), ()))
            continue
        positions = row["positions"]
        if not isinstance(positions, list) or not positions:
            raise ValueError(f"{label}.positions must list its Nodes")
        nodes = tuple(
            node_of(node, f"{label}.positions[{i}]", shape, beyond) for i, node in enumerate(positions)
        )
        found.append(NodeReaderRow(name, nodes, None, True, basis, pattern))
    if layer:
        found.append(NodeReaderRow(FACE_NAME, layer, None, False, (), ()))
    return tuple(found)


def connected(nodes: tuple[Node, ...], shape: Node, periodic: tuple[bool, bool, bool]) -> bool:
    """Whether a set of Nodes is one region: every Node reached from the first along the Links, across a periodic wrap too."""
    region, seen, front = set(nodes), {nodes[0]}, [nodes[0]]
    while front:
        node = front.pop()
        for axis in range(3):
            for side in (1, -1):
                there = list(node)
                there[axis] += side
                if periodic[axis]:
                    there[axis] %= shape[axis]
                at = (there[0], there[1], there[2])
                if at in region and at not in seen:
                    seen.add(at)
                    front.append(at)
    return seen == region


def regions_of_the_law(
    node_readers: tuple[NodeReaderRow, ...],
    messages: tuple[MessageRow, ...],
    shape: Node,
    periodic: tuple[bool, bool, bool],
    families: tuple[FamilyRule, ...],
) -> None:
    """The size rule of a node_reader's region (ALGEBRA.md #the-count-is-the-records-share, No click names a Node; the owner's words, the uncertainty principle upheld): a declared region, a reader with Nodes alone, is one connected region of Nodes, never one Node (it reads the net current through its boundary Ports, and through one Node what enters leaves, the net current over a passing wave about 0, so one Node counts no quantum; a reader with a record of its own may stand on one Node, `bodies_of`, the relation seen from its two ends), and, the finest structure the amplitudes of a family can carry being half its wavelength, at least half the wavelength of every message of its family across the beam, q / p Nodes for the wave [p, q], on every axis of more than one Node other than the axis the message travels along: one Node, a region in pieces and a region whose extent on such an axis, from its least to its greatest coordinate, is under q / p (extent x |p| < q) are refused by name; a node_reader reading a body declares no region and the open faces' layer is the board's own; the depth along the beam is not gated."""
    for node_reader in node_readers:
        if not node_reader.declared:
            continue
        if len(node_reader.positions) < 2:
            raise ValueError(
                f"node_reader {node_reader.name!r} is one Node: a region of a travelling wave, a reader with Nodes alone, "
                "reads the net current through its boundary Ports, and through one Node what enters leaves, so it "
                "stands on two Nodes or more, never one Node; a reader with a record of its own may stand on one "
                "Node (ALGEBRA.md, The NodeReader is one declaration kind for every experiment)"
            )
        if not connected(node_reader.positions, shape, periodic):
            raise ValueError(
                f"node_reader {node_reader.name!r} is not one connected region: its Nodes fall into pieces with "
                "no Link between them"
            )
        for message in messages:
            p, q = message.wave
            for axis in range(3):
                if axis == message.along or shape[axis] < 2:
                    continue
                coordinates = [node[axis] for node in node_reader.positions]
                extent = max(coordinates) - min(coordinates) + 1
                if extent * abs(p) < q:
                    raise ValueError(
                        f"node_reader {node_reader.name!r} is {extent} Node(s) across the {AXES[axis]} axis, under half "
                        f"the wavelength of the {families[message.family].name!r} message's wave [{p}, {q}], "
                        f"{q} / {abs(p)} Nodes: no click names a position finer than the amplitudes carry"
                    )


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
    gamma, action = integers["node_clock"], integers["quantum_action"]
    width = integers["width"]
    bound = derived.amplitude_bound(families, gamma, action, width, integers["link_unit"])
    mode = next((doc for doc in files.values() if isinstance(doc, dict) and "world_digest" in doc), None)
    bodies = bodies_of(
        world["bodies"],
        mode,
        digest,
        families,
        shape,
        bound,
        beyond,
        action,
        (periodic[0], periodic[1], periodic[2]),
    )
    messages = messages_of(world.get("messages", []), mode, digest, families, shape, bound, beyond)
    ticks = integer(world["ticks"], "ticks", 0)
    wholes = wholes_of(world.get("messages", []), families, shape, beyond, ticks)
    receding = receding_of(world["receding"], shape, faces) if "receding" in world else ()
    layer = layer_of(shape, (open_axes[0], open_axes[1], open_axes[2]), depth, receding)
    node_readers = node_readers_of(world["node_readers"], shape, len(bodies), beyond, layer)
    regions_of_the_law(node_readers, messages, shape, (periodic[0], periodic[1], periodic[2]), families)
    laid = [message.family for message in messages] + [body.family for body in bodies]
    laid += [whole.family for whole in wholes]
    patterns_of_the_law([(d.name, d.pattern) for d in node_readers], laid, families)
    # the world's records: a charged family's bodies each a record owning one row of the sign, every
    # holder of the sign one row per charged record beside the free row (derived.with_records)
    counted = [body.family for body in bodies]
    families = derived.with_records(families, [counted.count(index) for index in range(len(families))])
    draw = draw_of(world["draw"], "draw") if "draw" in world else None
    lay = lay_of(world["lay"], "lay") if "lay" in world else None
    pairs = [families[b.family].pair for b in bodies]
    budget_gate(lay, pairs, [max(b.counts) for b in bodies], ticks, action)
    return World(
        shape,
        (periodic[0], periodic[1], periodic[2]),
        (open_axes[0], open_axes[1], open_axes[2]),
        depth,
        beyond,
        ticks,
        gamma,
        action,
        derived.largest_of(width),
        integers["link_unit"],
        kind_of(width),
        bound,
        families,
        bodies,
        messages,
        node_readers,
        receding,
        draw,
        lay,
        wholes,
    )
