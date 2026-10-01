"""The world's files read into the GameBoard's world: the universe file (the integers and the families), the world file (the GameBoard with its inner faces, the bodies, the messages, the detectors) and the generator's mode file beside it (every body's and message's levels, `loader/mode.py`); every key checked, every other key refused as unknown by name, no default written (ALGEBRA.md #a-familys-declaration)."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from typing import Any

import numpy as np

from event_universe.core.integer import MAX_WORK_INT
from event_universe.loader import derived
from event_universe.loader.derived import FamilyRule, Row
from event_universe.loader.faces import RecedingFace, faces_of, layer_of, receding_of
from event_universe.loader.keys import AXES, Node, document_at, integer, keyed, node_of
from event_universe.loader.messages import MessageRow, messages_of
from event_universe.loader.mode import Levels, entry_of, levels_of, mode_entries

FACES = ("open", "periodic", "closed")
FACE_NAME = "face"  # the one detector of the open faces' layer
WORLD_KEYS: tuple[str, ...] = ("shape", "boundary", "face_depth", "faces", "ticks", "universe", "engine")
WORLD_KEYS += ("measured", "messages", "detectors", "receding")
WORLD_REQUIRED = ("shape", "boundary", "ticks", "universe", "engine", "measured", "detectors")
UNIVERSE_KEYS = ("integers", "families")
INTEGER_KEYS = ("node_clock", "quantum_action", "width")
FAMILY_KEYS, FAMILY_REQUIRED, HELD_KEYS, HELD_REQUIRED = (
    ("name", "pair", "dimension", "held"),
    ("name", "pair"),
    ("sources", "divisor", "rest"),
    ("sources", "divisor"),
)
FORM, TENSIONS, WRONSKIAN = (
    "form",
    "tensions",
    "wronskian",
)  # what sources a held row: one real line each
SOURCES = ((FORM,), (FORM, TENSIONS), (WRONSKIAN,))  # the lists a held row may declare, in this order
PLANE = 2  # the dimension of a plane, re and im: charged matter; 1 one real line
BODY_KEYS, BODY_REQUIRED, NODE_KEYS = (
    ("family", "nodes"),
    ("family", "nodes"),
    ("node", "count"),
)
DETECTOR_KEYS, START_KEYS = ("name", "positions", "block"), ("mode",)


@dataclass(frozen=True)
class BodyRow:
    """A body as declared: its family, its Nodes in the declared order with their counts (checked at the start against its record's share in quanta, a reading), and its family's two levels and its second level pair (the rotation sense, 0 for a neutral body) from the mode file, each the nonzero Nodes' flat x-major indexes with their levels."""

    family: int
    nodes: tuple[Node, ...]
    counts: tuple[int, ...]
    now: Levels
    before: Levels
    im_now: Levels
    im_before: Levels


@dataclass(frozen=True)
class DetectorRow:
    """A detector: its name and its Nodes (`positions`), one region whose click is its report of the net current into it through its front boundary Ports each interval, or the body whose Nodes report each interval (`block`); `declared` where it is a region of the declared instrument, and not for a body's detector nor for the open faces' layer, the board's own region named `face` (`FACE_NAME`), which the loader adds last where an open face does not recede."""

    name: str
    positions: tuple[Node, ...]
    body: int | None
    declared: bool


@dataclass(frozen=True)
class World:
    """The world as loaded: the GameBoard's shape, which axes wrap and which are open, the open faces' depth, the Nodes declared beyond the board by its inner faces, the intervals, Gamma, T, the largest integer of the file's width, the kind of the run's arrays chosen by the width (`kind_of`), the amplitude bound A derived, the families, the bodies, the messages, the detectors and the receding faces."""

    shape: Node
    periodic: tuple[bool, bool, bool]
    open_axes: tuple[bool, bool, bool]
    face_depth: int
    beyond: tuple[Node, ...]
    ticks: int
    node_clock: int
    quantum_action: int
    width: int
    kind: type
    amplitude_bound: int
    families: tuple[FamilyRule, ...]
    bodies: tuple[BodyRow, ...]
    messages: tuple[MessageRow, ...]
    detectors: tuple[DetectorRow, ...]
    receding: tuple[RecedingFace, ...]


def shape_of(row: dict[str, Any], label: str) -> tuple[int, bool, bool]:
    """A family's shape from its row, (lines, plane, wronskian): a family of quanta declares its `dimension`, 1 (one real line) or 2 (a plane, re and im), and nothing of what sources it; a held row declares its `sources`, the form alone, the form and the tensions, or the Wronskian (one real line per source: 1, 1 + 3 or 1 lines), and no dimension, a held row never being a plane; refused by name otherwise (ALGEBRA.md #a-familys-declaration, the dimension's table)."""
    if "held" in row:
        if "dimension" in row:
            raise ValueError(
                f"{label} is a held row and declares no dimension: its shape is its sources' count"
            )
        sources = keyed(row["held"], f"{label}.held", HELD_KEYS, HELD_REQUIRED)["sources"]
        if not isinstance(sources, list) or tuple(sources) not in SOURCES:
            raise ValueError(
                f"{label}.held.sources is one of {[list(s) for s in SOURCES]}, got {sources!r}"
            )
        return 1 + 3 * (TENSIONS in sources), False, WRONSKIAN in sources
    if "dimension" not in row:
        raise ValueError(f"{label} lacks the key 'dimension': a family of quanta declares 1 or {PLANE}")
    lines = integer(row["dimension"], f"{label}.dimension", 1, PLANE)
    return lines, lines == PLANE, False


def kind_of(width: int) -> type:
    """The kind of the run's arrays from the declared width, the one place the engine's integers are chosen (the owner, 2026-10-01, 02:35, "choose 64 or 128 bits outside the engine, at the start"): the host's 64-bit integers where the width is at or under the host's signed bits, Python's integers (arrays of objects, exact at any width and slow) above it; the amplitude bound A is derived at the declared width either way (ENGINE.md, the loader)."""
    return np.int64 if width <= MAX_WORK_INT.bit_length() else object


def universe_of(document: object) -> tuple[dict[str, int], tuple[FamilyRule, ...]]:
    """The universe file: its integers and its families, each row its name, its pair and its dimension (a family of quanta) or its sources with its divisor and its rest (a held row; the vacuum content `rest`, the level at which the massless row holding the content rests everywhere, an integer from 0 within the width; refused by name on the holder of the sign and on a row with a gap, which has no constant rest, ALGEBRA.md #what-is-open, item 22), everything else derived by the rule from the pair and the shape."""
    universe = keyed(document, "the universe file", UNIVERSE_KEYS, UNIVERSE_KEYS)
    raw = keyed(universe["integers"], "integers", INTEGER_KEYS, INTEGER_KEYS)
    integers = {key: integer(value, f"integers.{key}", 1) for key, value in raw.items()}
    entries = universe["families"]
    if not isinstance(entries, list) or not entries:
        raise ValueError("families must be a list of the families' rows")
    rows: list[Row] = []
    for index, entry in enumerate(entries):
        label = f"families[{index}]"
        row = keyed(entry, label, FAMILY_KEYS, FAMILY_REQUIRED)
        name = row["name"]
        if not isinstance(name, str) or not name or name in [found.name for found in rows]:
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
        lines, plane, wronskian = shape_of(row, label)
        divisor, rest = None, 0
        if "held" in row:
            holds = row["held"]
            divisor = integer(holds["divisor"], f"{label}.held.divisor", 1)
            if "rest" in holds:
                if wronskian or num != den:
                    raise ValueError(
                        f"{label}.held.rest: only the massless row holding the content rests at a level"
                    )
                rest = integer(
                    holds["rest"], f"{label}.held.rest", 0, derived.largest_of(integers["width"])
                )
        rows.append(Row(name, (num, den), lines, plane, wronskian, divisor, rest))
    return integers, derived.family_rules(rows)


def bodies_of(
    value: object,
    mode: object,
    digest: str,
    families: tuple[FamilyRule, ...],
    shape: Node,
    bound: int,
    beyond: tuple[Node, ...],
) -> tuple[BodyRow, ...]:
    """The bodies: each its family (a family of quanta), its Nodes with their counts (no Node shared, none beyond the board) and its two levels from the mode file beside the world, which stands for this world by its digest; a body with no mode entry is refused by name."""
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
        now, before, im_now, im_before = levels_of(
            entry_of(entries, number, label),
            f"the mode file's bodies[{number}]",
            families[family],
            shape,
            bound,
            beyond,
        )
        found.append(BodyRow(family, tuple(nodes), tuple(counts), now, before, im_now, im_before))
    return tuple(found)


def detectors_of(
    value: object,
    shape: Node,
    bodies: int,
    beyond: tuple[Node, ...],
    layer: tuple[Node, ...],
) -> tuple[DetectorRow, ...]:
    """The detectors: each a name of its own (not the faces' `face`) with its Nodes (none beyond the board), one region of the declared instrument, or the body it names by its number; after them the open faces' layer where there is one (`layer`), the board's own region under the name `face`, no part of the instrument."""
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
            body = integer(row["block"], f"{label}.block", 0, bodies - 1)
            found.append(DetectorRow(name, (), body, False))
            continue
        positions = row["positions"]
        if not isinstance(positions, list) or not positions:
            raise ValueError(f"{label}.positions must list its Nodes")
        nodes = tuple(
            node_of(node, f"{label}.positions[{i}]", shape, beyond) for i, node in enumerate(positions)
        )
        found.append(DetectorRow(name, nodes, None, True))
    if layer:
        found.append(DetectorRow(FACE_NAME, layer, None, False))
    return tuple(found)


def regions_no_finer_than_half_a_wavelength(
    detectors: tuple[DetectorRow, ...],
    messages: tuple[MessageRow, ...],
    shape: Node,
    families: tuple[FamilyRule, ...],
) -> None:
    """The size rule of a detector's region (ALGEBRA.md #the-count-is-the-records-share, No click names a Node; the owner's word of 2026-09-30, the uncertainty principle upheld): the finest structure the amplitudes of a family can carry is half its wavelength, so a declared region is at least half the wavelength of every message of its family across the beam, q / p Links for the wave [p, q], on every axis of more than one Node other than the axis the message travels along: a region whose extent on such an axis, from its least to its greatest coordinate, is under q / p (extent x |p| < q) is refused by name; a detector reading a body declares no region and the open faces' layer is the board's own."""
    for detector in detectors:
        if not detector.declared:
            continue
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
                        f"{q} / {abs(p)} Links: no click names a position finer than the amplitudes carry"
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
    bound = derived.amplitude_bound(families, gamma, action, width)
    mode = next((doc for doc in files.values() if isinstance(doc, dict) and "world_digest" in doc), None)
    bodies = bodies_of(world["measured"], mode, digest, families, shape, bound, beyond)
    messages = messages_of(world.get("messages", []), mode, digest, families, shape, bound, beyond)
    receding = receding_of(world["receding"], shape, faces) if "receding" in world else ()
    layer = layer_of(shape, (open_axes[0], open_axes[1], open_axes[2]), depth, receding)
    detectors = detectors_of(world["detectors"], shape, len(bodies), beyond, layer)
    regions_no_finer_than_half_a_wavelength(detectors, messages, shape, families)
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
        kind_of(width),
        bound,
        families,
        bodies,
        messages,
        detectors,
        receding,
    )
