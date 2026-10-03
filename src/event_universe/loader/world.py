"""The world's files read into the GameBoard's world: the universe file (the integers and the families), the world file (the GameBoard with its inner faces, the bodies, the messages, the detectors) and the generator's mode file beside it (every body's and message's levels, `loader/mode.py`); every key checked, every other key refused as unknown by name, no default written (ALGEBRA.md #a-familys-declaration)."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass

import numpy as np

from event_universe.core.integer import MAX_WORK_INT
from event_universe.loader import derived
from event_universe.loader.derived import FamilyRule
from event_universe.loader.faces import RecedingFace, faces_of, layer_of, receding_of
from event_universe.loader.instrument import (
    NODE_INSTRUMENT_KEYS,
    Instrument,
    NodeInstrument,
    Pattern,
    basis_of,
    instrument_of,
    node_instrument_of,
    pattern_of,
    patterns_of_the_law,
    ports_of,
)
from event_universe.loader.keys import AXES, Node, document_at, integer, keyed, node_of, weights_of
from event_universe.loader.lay import Lay, budget_gate, lay_of
from event_universe.loader.messages import MessageRow, messages_of
from event_universe.loader.mode import Levels, entry_of, levels_of, mode_entries
from event_universe.loader.universe import universe_of

FACES = ("open", "periodic", "closed")
FACE_NAME = "face"  # the one detector of the open faces' layer
WORLD_KEYS: tuple[str, ...] = ("shape", "boundary", "face_depth", "faces", "ticks", "universe", "engine")
WORLD_KEYS += ("measured", "messages", "detectors", "receding", "instrument", "lay")
WORLD_REQUIRED = ("shape", "boundary", "ticks", "universe", "engine", "measured", "detectors")
BODY_KEYS, BODY_REQUIRED, NODE_KEYS = (
    ("family", "nodes", "weights", *NODE_INSTRUMENT_KEYS),
    ("family", "nodes"),
    ("node", "count"),
)
DETECTOR_KEYS, START_KEYS = ("name", "positions", "block", "basis", "pattern"), ("mode",)


@dataclass(frozen=True)
class BodyRow:
    """A body as declared: its family, its Nodes in the declared order with their counts (checked at the start against its record's share in quanta, a reading), and its family's two levels and its second level pair (the rotation sense, 0 for a neutral body) from the mode file, each the nonzero Nodes' flat x-major indexes with their levels; or, a body laid in its parts at one Node (`instrument`, `loader/instrument.py`: its parts the modes' labels with the count in one of them, and as an instrument its transitions, its givings and its own draw), whose lay is the engine's own at the start and whose levels the mode file does not hold (ALGEBRA.md, The click writes on the GameBoard (j); the owner's word of 2026-10-03, the body is at a Node). A laid body carries the weight of its laid pair on each line of its record (`weights`, 1 on every line without the key; `keys.weights_of`)."""

    family: int
    nodes: tuple[Node, ...]
    counts: tuple[int, ...]
    now: Levels
    before: Levels
    im_now: Levels
    im_before: Levels
    weights: tuple[int, ...] = ()
    instrument: NodeInstrument | None = None


@dataclass(frozen=True)
class DetectorRow:
    """A detector: its name and its Nodes (`positions`), one region whose click is its report of the net current into it through its front boundary Ports each interval, or the body whose Nodes report each interval (`block`); `declared` where it is a region of the declared instrument, and not for a body's detector nor for the open faces' layer, the board's own region named `face` (`FACE_NAME`), which the loader adds last where an open face does not recede; `basis`, the instrument's declared setting (p, q), the coefficients of its credit, and `pattern`, one integer pair per part of the record it reads, how each part reads the setting at the + port and the - port (the pair's (p, q) and (-q, p), ALGEBRA.md #the-click-is-the-meeting; `loader/instrument.py`), read by the reader and by the instrument's draw through the root in the run, each empty where none is declared."""

    name: str
    positions: tuple[Node, ...]
    body: int | None
    declared: bool
    basis: tuple[int, ...]
    pattern: Pattern


@dataclass(frozen=True)
class World:
    """The world as loaded: the GameBoard's shape, which axes wrap and which are open, the open faces' depth, the Nodes declared beyond the board by its inner faces, the intervals, Gamma, T, the largest integer of the file's width, the kind of the run's arrays chosen by the width (`kind_of`), the amplitude bound A derived, the families, the bodies, the messages, the detectors, the receding faces, the instrument and the lay declared with its tolerance (the budget's gate on T at load, `loader/lay.py`)'s draw (`instrument`, None where the world declares none: no draw and no write, the run as before the click entered the engine)."""

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
    detectors: tuple[DetectorRow, ...]
    receding: tuple[RecedingFace, ...]
    instrument: Instrument | None
    lay: Lay | None  # the lay the world declares for its bodies and its tolerance (`loader/lay.py`)


def kind_of(width: int) -> type:
    """The kind of the run's arrays from the declared width, the one place the engine's integers are chosen (the owner, 2026-10-01, 02:35, "choose 64 or 128 bits outside the engine, at the start"): the host's 64-bit integers where the width is at or under the host's signed bits, Python's integers (arrays of objects, exact at any width and slow) above it; the amplitude bound A is derived at the declared width either way (ENGINE.md, the loader)."""
    return np.int64 if width <= MAX_WORK_INT.bit_length() else object


def bodies_of(
    value: object,
    mode: object,
    digest: str,
    families: tuple[FamilyRule, ...],
    shape: Node,
    bound: int,
    beyond: tuple[Node, ...],
) -> tuple[BodyRow, ...]:
    """The bodies: each its family (a family of quanta), its Nodes with their counts (no Node shared, none beyond the board) and its two levels from the mode file beside the world, which stands for this world by its digest, the mode's entries in the order of the bodies it lays; a body with no mode entry is refused by name; a body declaring its `parts` (and as an instrument its `transitions`, `rates` and `instrument`) takes no mode entry, its lay the engine's own at its one Node (`node_instrument_of`), and optionally `weights`, the laid pair's weight per line of its record (`keys.weights_of`, a record of real lines')."""
    names = {family.name: index for index, family in enumerate(families)}
    quanta = {name: index for name, index in names.items() if families[index].quanta}
    if not isinstance(value, list):
        raise ValueError("measured must be a list of bodies")
    laid = [entry for entry in value if not any(key in entry for key in NODE_INSTRUMENT_KEYS)]
    entries = mode_entries(mode, digest, "bodies") if laid else []
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
        parted = entry not in laid
        if parted and len(lines) != 1:
            raise ValueError(
                f"{label} is laid in its parts at one Node and declares {len(lines)}: a body that is an instrument "
                "is one Node, its record there (the owner's word of 2026-10-03; ALGEBRA.md, The bound body is one Node)"
            )
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
        if parted:
            parts = node_instrument_of(body, label, families[family], family, quanta, sum(counts))
            found.append(BodyRow(family, tuple(nodes), tuple(counts), (), (), (), (), (), parts))
            continue
        placed = laid.index(entry)
        now, before, im_now, im_before = levels_of(
            entry_of(entries, placed, label),
            f"the mode file's bodies[{placed}]",
            families[family],
            shape,
            bound,
            beyond,
        )
        weights = weights_of(
            body.get("weights"), f"{label}.weights", families[family].width, families[family].plane
        )
        found.append(
            BodyRow(family, tuple(nodes), tuple(counts), now, before, im_now, im_before, weights)
        )
    return tuple(found)


def detectors_of(
    value: object,
    shape: Node,
    bodies: int,
    beyond: tuple[Node, ...],
    layer: tuple[Node, ...],
) -> tuple[DetectorRow, ...]:
    """The detectors: each a name of its own (not the faces' `face`) with its Nodes (none beyond the board), one region of the declared instrument, optionally with its `basis`, the instrument's setting (p, q), a list of integers not all 0, and its `pattern`, one integer pair per part of the record it reads (the reader's declaration and the instrument's draw's through the root, `loader/instrument.py`; a pattern without a basis, and two ports not orthogonal, are refused by name), or the body it names by its number (no basis); after them the open faces' layer where there is one (`layer`), the board's own region under the name `face`, no part of the instrument."""
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
                    f"{label}.basis: a basis is declared on a region, not on a body's detector"
                )
            body = integer(row["block"], f"{label}.block", 0, bodies - 1)
            found.append(DetectorRow(name, (), body, False, (), ()))
            continue
        positions = row["positions"]
        if not isinstance(positions, list) or not positions:
            raise ValueError(f"{label}.positions must list its Nodes")
        nodes = tuple(
            node_of(node, f"{label}.positions[{i}]", shape, beyond) for i, node in enumerate(positions)
        )
        found.append(DetectorRow(name, nodes, None, True, basis, pattern))
    if layer:
        found.append(DetectorRow(FACE_NAME, layer, None, False, (), ()))
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
    detectors: tuple[DetectorRow, ...],
    messages: tuple[MessageRow, ...],
    shape: Node,
    periodic: tuple[bool, bool, bool],
    families: tuple[FamilyRule, ...],
) -> None:
    """The size rule of a detector's region (ALGEBRA.md #the-count-is-the-records-share, No click names a Node; the owner's words of 2026-09-30 and of 2026-10-01, 03:20, the uncertainty principle upheld): a declared region is one connected region of Nodes, never one Node, and, the finest structure the amplitudes of a family can carry being half its wavelength, at least half the wavelength of every message of its family across the beam, q / p Nodes for the wave [p, q], on every axis of more than one Node other than the axis the message travels along: one Node, a region in pieces and a region whose extent on such an axis, from its least to its greatest coordinate, is under q / p (extent x |p| < q) are refused by name; a detector reading a body declares no region and the open faces' layer is the board's own; the depth along the beam is not gated."""
    for detector in detectors:
        if not detector.declared:
            continue
        if len(detector.positions) < 2:
            raise ValueError(
                f"detector {detector.name!r} is one Node: a detector is a region of Nodes, never one Node "
                "(no click names a Node)"
            )
        if not connected(detector.positions, shape, periodic):
            raise ValueError(
                f"detector {detector.name!r} is not one connected region: its Nodes fall into pieces with "
                "no Link between them"
            )
        for message in messages:
            p, q = message.wave
            for axis in range(3):
                if axis == message.along or shape[axis] < 2:
                    continue
                coordinates = [node[axis] for node in detector.positions]
                extent = max(coordinates) - min(coordinates) + 1
                if extent * abs(p) < q:
                    raise ValueError(
                        f"detector {detector.name!r} is {extent} Node(s) across the {AXES[axis]} axis, under half "
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
    bodies = bodies_of(world["measured"], mode, digest, families, shape, bound, beyond)
    messages = messages_of(world.get("messages", []), mode, digest, families, shape, bound, beyond)
    receding = receding_of(world["receding"], shape, faces) if "receding" in world else ()
    layer = layer_of(shape, (open_axes[0], open_axes[1], open_axes[2]), depth, receding)
    detectors = detectors_of(world["detectors"], shape, len(bodies), beyond, layer)
    regions_of_the_law(detectors, messages, shape, (periodic[0], periodic[1], periodic[2]), families)
    laid = [message.family for message in messages] + [body.family for body in bodies]
    patterns_of_the_law([(d.name, d.pattern) for d in detectors], laid, families)
    # the world's records: a charged family's bodies each a record owning one row of the sign, every
    # holder of the sign one row per charged record beside the free row (derived.with_records)
    counted = [body.family for body in bodies]
    families = derived.with_records(families, [counted.count(index) for index in range(len(families))])
    instrument = instrument_of(world["instrument"], "instrument") if "instrument" in world else None
    lay = lay_of(world["lay"], "lay") if "lay" in world else None
    ticks, pairs = integer(world["ticks"], "ticks", 0), [families[b.family].pair for b in bodies]
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
        detectors,
        receding,
        instrument,
        lay,
    )
