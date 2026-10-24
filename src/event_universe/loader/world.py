"""The world's files read into the lattice's world: the universe file (the integers and the families) and the world file (the lattice with its inner faces, the bodies declared NodeDetectors at a Node, the node_detectors); every key checked, every other key refused as unknown by name (the generator's mode file, its `lay` key and its laid bodies and `packets` among them since 2026-10-24, the owner's word: the generator goes, the seed is light at one quantum on every Node), no default written (ALGEBRA.md #a-familys-declaration)."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass

import numpy as np

from event_universe import conversion
from event_universe.core.integer import MAX_WORK_INT
from event_universe.core.rule3 import division_forward
from event_universe.loader import derived, window
from event_universe.loader.derived import FamilyRule
from event_universe.loader.draw import (
    Draw,
    Pattern,
    draw_of,
    pattern_of,
    patterns_of_the_law,
    ports_of,
    setting_of,
    settings_of_the_law,
)
from event_universe.loader.faces import (
    RecedingFace,
    connected,
    faces_of,
    layer_of,
    receding_of,
)
from event_universe.loader.interval import volume_rows
from event_universe.loader.keys import AXES, Node, document_at, integer, keyed, node_of
from event_universe.loader.node_detector_declaration import (
    READER_RECORD_KEYS,
    NodeDetectorDeclaration,
    node_detector_of,
    packet_form,
)
from event_universe.loader.node_detector_rows import reader_count
from event_universe.loader.seed import seed_of
from event_universe.loader.universe import universe_of

FACES = ("open", "periodic", "closed")
FACE_NAME = "face"  # the one node_detector of the open faces' layer
WORLD_KEYS: tuple[str, ...] = ("shape", "boundary", "face_depth", "faces", "intervals", "universe")
WORLD_KEYS += ("bodies", "node_detectors", "receding", "draw")
WORLD_REQUIRED = ("shape", "intervals", "universe")  # bodies and node_detectors optional, 2026-10-24
TORUS = {"x": "periodic", "y": "periodic", "z": "periodic"}  # the board without `boundary`
BODY_KEYS = ("family", "nodes", *READER_RECORD_KEYS)
BODY_REQUIRED = ("family", "nodes")
READER_NODE_KEYS = (
    "node",
    "weight",
)  # a reader's Node: the lay's weight, the record's count declared once
NODEDETECTOR_KEYS = ("name", "positions", "block", "basis", "axis", "pattern", "turn")  # a reader's keys
TRANSITION = "transition"  # a region's own quantum, declared by no region: its unit its record's share


@dataclass(frozen=True)
class BodyRow:
    """A body as declared: its family, its Nodes in the declared order with the lay's weights (`counts`), and its declaration as a NodeDetector at a Node (`detector`, `loader/node_detector_declaration.py`: its parts the modes' labels with the count in one of them, its transitions, its emissions and its own draw), whose lay is the engine's own at the start (ALGEBRA.md, The click writes on the lattice (j); the owner's word, the body is at a Node). A body laid from the generator's mode file, and the bound body the frame tool declared an instrument, left with the generator (2026-10-24, the owner's word): every body declares its parts."""

    family: int
    nodes: tuple[Node, ...]
    counts: tuple[int, ...]
    detector: NodeDetectorDeclaration


@dataclass(frozen=True)
class NodeDetectorRow:
    """A node_detector: its name and its Nodes (`positions`), one region whose click is its report of the net current into it through its front boundary Ports each interval, or the body whose Nodes report each interval (`block`); `declared` where it is a region of the declared NodeDetector, and not for a body's node_detector nor for the open faces' layer, the board's own region named `face` (`FACE_NAME`), which the loader adds last where an open face does not recede; `basis`, the reader's declared setting (p, q), the coefficients of its credit, and `pattern`, one integer pair per part of the record it reads, how each part reads the setting at the + port and the - port (the pair's (p, q) and (-q, p), ALGEBRA.md #the-click-is-the-meeting; `loader/draw.py`), read by the reader and by the sides' draws in the run, each empty where none is declared; no quantum of its own, a region counting in its record's own unit (`credit.record_unit`; the key `transition` refused by name). A side of a record of several parts declares its setting as `basis` (real-line parts, the setting's coefficients at the full angle) or as `axis` (plane parts, the half-angle pair of the detector's axis; the spin branch, 2026-10-19), one of the two, with its `pattern`; the ports' arithmetic is one (`loader/draw.ports_of`)."""

    name: str
    positions: tuple[Node, ...]
    body: int | None
    declared: bool
    basis: tuple[int, ...]
    pattern: Pattern
    axis: tuple[int, ...] = ()  # a plane record's setting, the half-angle pair (the spin branch)
    turn: int = 0  # a plane side's azimuth in quarter turns, i^turn on the second component


@dataclass(frozen=True)
class World:
    """The world as loaded: the lattice's shape, which axes wrap and which are open, the open faces' depth, the Nodes declared beyond the board by its inner faces, the intervals, Gamma, T, the largest integer of the file's width, the kind of the run's arrays chosen by the width (`kind_of`), the amplitude bound A derived, the families, the bodies (each a NodeDetector at a Node), the node_detectors, the receding faces, the NodeDetectors' draw (`draw`, `loader/draw.py`, None where the world declares none: no draw and no write) and the seed family of a world that declares nothing (`loader/seed.seed_of`)."""

    shape: Node
    periodic: tuple[bool, bool, bool]
    open_axes: tuple[bool, bool, bool]
    face_depth: int
    beyond: tuple[Node, ...]
    intervals: int
    node_clock: int
    quantum_action: int
    width: int
    link_unit: int
    kind: type
    amplitude_bound: int
    families: tuple[FamilyRule, ...]
    bodies: tuple[BodyRow, ...]
    node_detectors: tuple[NodeDetectorRow, ...]
    receding: tuple[RecedingFace, ...]
    draw: Draw | None
    seed: int | None = None  # the seed family of a world that declares nothing (`loader/seed.seed_of`)


def kind_of(width: int) -> type:
    """The kind of the run's arrays from the declared width, the one place the engine's integers are chosen (the owner, "choose 64 or 128 bits outside the engine, at the start"): the host's 64-bit integers where the width is at or under the host's signed bits, Python's integers (arrays of objects, exact at any width and slow) above it; the amplitude bound A is derived at the declared width either way (ENGINE.md, the loader)."""
    return np.int64 if width <= MAX_WORK_INT.bit_length() else object


def bodies_of(
    value: object,
    families: tuple[FamilyRule, ...],
    shape: Node,
    beyond: tuple[Node, ...],
    action: int,
    periodic: tuple[bool, bool, bool] = (False, False, False),
) -> tuple[BodyRow, ...]:
    """The bodies: each its family (a family of quanta) and its Nodes (no Node shared, none beyond the board), each Node with the lay's `weight` (1 where absent), a body declaring its `parts` (and as a reader its `transitions`, `rates` and `node_detector`) or its `conversion` (the record converted whole, with its `node_detector` and its `count`), its lay the engine's own over its region (`node_detector_of`; its emissions' lay decided by the board's shape against the declared width at the quantum action T, `packet_form`); a body declaring neither, the generator's laid body whose levels stood in the mode file, is refused by name (2026-10-24, the owner's word: the generator goes)."""
    names = {family.name: index for index, family in enumerate(families)}
    quanta = {name: index for name, index in names.items() if families[index].quanta}
    if not isinstance(value, list):
        raise ValueError("bodies must be a list of bodies")
    taken, found = set(), []
    for number, entry in enumerate(value):
        label = f"bodies[{number}]"
        body = keyed(entry, label, BODY_KEYS, BODY_REQUIRED)
        family = names.get(body["family"])
        if family is None or not families[family].quanta:
            raise ValueError(f"{label}.family must name a family of quanta, got {body['family']!r}")
        if not any(key in body for key in READER_RECORD_KEYS):
            raise ValueError(
                f"{label} declares no parts and no conversion: a body laid from the generator's mode file left with "
                "the generator (2026-10-24, the owner's word); a body is a record declared a NodeDetector at a Node, "
                "and the seed is light at one quantum on every Node (ALGEBRA.md, The uniform seed is a lay)"
            )
        lines = body["nodes"]
        if not isinstance(lines, list) or not lines:
            raise ValueError(f"{label}.nodes must list the body's Nodes with their weights")
        nodes, counts = [], []
        for index, line in enumerate(lines):
            keyed(line, f"{label}.nodes[{index}]", READER_NODE_KEYS, ("node",))
            node = node_of(line["node"], f"{label}.nodes[{index}].node", shape, beyond)
            if node in taken:
                raise ValueError(
                    f"{label}: two bodies share the Node {list(node)}; they stand apart or are one body"
                )
            taken.add(node)
            nodes.append(node)
            counts.append(integer(line.get("weight", 1), f"{label}.nodes[{index}].weight", 1))
        if not connected(tuple(nodes), shape, periodic):
            raise ValueError(
                f"{label} declares its own record over a region in pieces: a NodeDetector's Nodes are one connected "
                "region through the six Ports (ALGEBRA.md, The NodeDetector is one declaration kind for every "
                "world); its Nodes are {[list(n) for n in nodes]}"
            )
        count = reader_count(body, label, families, family)
        parts = node_detector_of(body, label, families, family, quanta, count)
        parts = packet_form(parts, label, families, tuple(nodes), shape, periodic, action)
        found.append(BodyRow(family, tuple(nodes), tuple(counts), parts))
    return tuple(found)


def node_detectors_of(
    value: object,
    shape: Node,
    bodies: int,
    beyond: tuple[Node, ...],
    layer: tuple[Node, ...],
) -> tuple[NodeDetectorRow, ...]:
    """The node_detectors: each a name of its own (not the faces' `face`) with its Nodes (none beyond the board), one region of the declared NodeDetector, optionally with its `basis`, the reader's setting (p, q), a list of integers not all 0, and its `pattern`, one integer pair per part of the record it reads (the NodeDetector's declaration and the sides' draws', `loader/draw.py`; a pattern without a basis, and two ports not orthogonal, are refused by name), or the body it names by its number (no basis); a region declares no quantum of its own, its unit of one quantum being its record's own share per quantum read from the credit's books (`credit.record_unit`; the advisor's line with the mathematician's second, two hands), so the key `transition` is refused by name; after them the open faces' layer where there is one (`layer`), the board's own region under the name `face`, no part of the declared NodeDetector."""
    if not isinstance(value, list):
        raise ValueError("node_detectors must be a list")
    found: list[NodeDetectorRow] = []
    for index, entry in enumerate(value):
        label = f"node_detectors[{index}]"
        if isinstance(entry, dict) and TRANSITION in entry:
            raise ValueError(
                f"{label} holds the key {TRANSITION!r}: a region declares no quantum of its own, its unit of one "
                "quantum being its record's own share per quantum, read from the credit's books and not declared"
            )
        row = keyed(entry, label, NODEDETECTOR_KEYS, ("name",))
        name = row["name"]
        if not isinstance(name, str) or name == FACE_NAME or name in [d.name for d in found]:
            raise ValueError(f"{label}.name must be a name of its own, not {FACE_NAME!r}")
        if ("positions" in row) == ("block" in row):
            raise ValueError(f"{label} declares its `positions` or the `block` it reads, one of the two")
        basis, axis, turn = setting_of(row, label)  # one of the two, refused by name together
        setting = axis or basis
        if "pattern" in row and not setting:
            raise ValueError(
                f"{label}.pattern reads the setting `basis` or `axis` declares, and none is declared"
            )
        pattern = pattern_of(row["pattern"], f"{label}.pattern", setting) if "pattern" in row else ()
        if pattern:
            ports_of(
                setting, pattern, turn
            )  # the two ports orthogonal with equal norms, refused by name otherwise
        if "block" in row:
            if setting:
                raise ValueError(
                    f"{label}: a basis or an axis is declared on a region, not on a body's node_detector"
                )
            body = integer(row["block"], f"{label}.block", 0, bodies - 1)
            found.append(NodeDetectorRow(name, (), body, False, (), ()))
            continue
        positions = row["positions"]
        if not isinstance(positions, list) or not positions:
            raise ValueError(f"{label}.positions must list its Nodes")
        nodes = tuple(
            node_of(node, f"{label}.positions[{i}]", shape, beyond) for i, node in enumerate(positions)
        )
        found.append(NodeDetectorRow(name, nodes, None, True, basis, pattern, axis, turn))
    if layer:
        found.append(NodeDetectorRow(FACE_NAME, layer, None, False, (), ()))
    return tuple(found)


def regions_of_the_law(
    node_detectors: tuple[NodeDetectorRow, ...],
    shape: Node,
    periodic: tuple[bool, bool, bool],
) -> None:
    """The size rule of a node_detector's region (ALGEBRA.md #the-count-is-the-records-share, No click names a Node; the owner's words, the uncertainty principle upheld): a declared region, a NodeDetector with Nodes alone, is one connected region of Nodes, never one Node (it reads the net current through its boundary Ports, and through one Node what enters leaves, the net current over a passing wave about 0, so one Node counts no quantum; a NodeDetector with a record of its own may stand on one Node, `bodies_of`, the relation seen from its two ends), and, the finest structure the amplitudes of a family can carry being half its wavelength, at least half the wavelength of every packet of its family across the beam, q / p Nodes for the wave [p, q], on every axis of more than one Node other than the axis the packet travels along: one Node, a Node named twice (the refusal naming the reader and the Node, as `bodies_of` refuses a body naming one Node twice; the size rule reads the distinct Nodes), a region in pieces and a region whose extent on such an axis, from its least to its greatest coordinate on an open or closed axis and through the wrap on a periodic axis, the smallest arc of the ring that covers its coordinates (`loader/faces.extent_across`), is under q / p (extent x |p| < q) are refused by name (the advisor's breaker over the engine at 7756546d, #1793: a region naming one Node twice was admitted as two Nodes, and a region two Nodes wide through the wrap was read as five); a node_detector reading a body declares no region and the open faces' layer is the board's own; the depth along the beam is not gated."""
    for node_detector in node_detectors:
        if not node_detector.declared:
            continue
        nodes = tuple(dict.fromkeys(node_detector.positions))  # the distinct Nodes, in the order named
        if len(nodes) < len(node_detector.positions):
            twice = [list(node) for node in nodes if node_detector.positions.count(node) > 1]
            raise ValueError(
                f"node_detector {node_detector.name!r} names the Node {twice} twice: a region's Nodes are distinct, "
                "each named once, as a body's Nodes are"
            )
        if len(nodes) < 2:
            raise ValueError(
                f"node_detector {node_detector.name!r} is one Node: a region of a travelling wave, a NodeDetector with Nodes alone, "
                "reads the net current through its boundary Ports, and through one Node what enters leaves, so it "
                "stands on two Nodes or more, never one Node; a NodeDetector with a record of its own may stand on one "
                "Node (ALGEBRA.md, The NodeDetector is one declaration kind for every world)"
            )
        if not connected(nodes, shape, periodic):
            raise ValueError(
                f"node_detector {node_detector.name!r} is not one connected region: its Nodes fall into pieces with "
                "no Link between them"
            )


def even_box_refused(shape: Node, periodic: tuple[bool, ...], families: tuple[FamilyRule, ...]) -> None:
    """The board against the massless row's second double root (ALGEBRA.md, the two hands' line; the mathematician's reading of the shelved ion's refusal, branch `front-two-modes`): the massless band cos omega_k = (1 / 3) SUM_a cos k_a has two double roots, the uniform mode at k = 0 and the staggered mode (-1)^(x + y + z + t) at k = (pi, pi, pi), omega = pi, each of zero form and zero share; on a board periodic on all three axes with every extent even the staggered mode is an exact mode of a massless family (num = den), and Rule3's own rounding walks it as t^(3/2) / (3 N^(1/2)) with no bound, so such a board is refused by name with the family and the shape, the way out one odd extent or an open axis, where the mode is a bounded response; a gapped family has no double root there and is admitted; the extents' parity by the division act, no number of the law."""
    if all(periodic) and not any(division_forward(extent, 2, 0)[1] for extent in shape):
        for family in (f for f in families if f.pair[0] == f.pair[1]):
            raise ValueError(
                f"the massless family {family.name!r} on the board {list(shape)} periodic on all three axes with "
                "every extent even: the staggered mode (-1)^(x + y + z + t), the band's top, is an exact mode of such "
                "a board and Rule3's own rounding walks it without bound; give one axis an odd extent or open it"
            )


def parse_world(document: object, files: Mapping[str, object], digest: str) -> World:
    """The world from its document, the files it names (the universe, read by the host) and its digest; every defect refused by name; a document without `boundary` is the torus, periodic on every axis (the owner's word of 2026-10-23), a face declared by name where an instrument's board needs it; a document naming neither `bodies` nor `node_detectors` declares nothing (the owner's word of 2026-10-24, the fold: a world of the universe, the board's shape and the run's length alone), its seed the universe's one massless family of quanta laid by the engine at one quantum on every Node and its reader the board itself (`loader/seed.seed_of`); a document naming them empty declares an empty board and runs as before (the former requirement of the two keys kept by name)."""
    world = keyed(document, "the world", WORLD_KEYS, WORLD_REQUIRED)
    integers, families = universe_of(document_at(files, world["universe"], "universe"))
    shape_value = world["shape"]
    if not isinstance(shape_value, list) or len(shape_value) != 3:
        raise ValueError("shape must be [X, Y, Z]")
    extents = tuple(integer(extent, f"shape[{axis}]", 1) for axis, extent in enumerate(shape_value))
    shape = (extents[0], extents[1], extents[2])
    faces = keyed(world.get("boundary", TORUS), "boundary", AXES, AXES)  # the torus by default
    if any(faces[axis] not in FACES for axis in AXES):
        raise ValueError(f"boundary gives every axis one of {list(FACES)}")
    periodic = tuple(faces[axis] == "periodic" for axis in AXES)
    open_axes = tuple(faces[axis] == "open" for axis in AXES)
    even_box_refused(shape, periodic, families)
    wraps, opened = (periodic[0], periodic[1], periodic[2]), (open_axes[0], open_axes[1], open_axes[2])
    if any(open_axes) and "face_depth" not in world:
        raise ValueError("face_depth is required on a lattice with an open face: the depth of its layer")
    depth = integer(world["face_depth"], "face_depth", 1) if "face_depth" in world else 0
    beyond = faces_of(world["faces"], shape) if "faces" in world else ()
    gamma, action = integers["node_clock"], integers["quantum_action"]
    width = integers["width"]
    bound = derived.amplitude_bound(families, gamma, action, width, integers["link_unit"])
    bodies = bodies_of(world.get("bodies", []), families, shape, beyond, action, wraps)
    families = volume_rows(families, gamma)  # the held rows sourced by the tensions carry their volume
    bodies = window.windowed(bodies, families, shape, periodic, action)  # the derived windows
    conversion.together(families, bodies)  # the multisets a close can credit, refused by name
    intervals = integer(world["intervals"], "intervals", 0)
    receding = receding_of(world["receding"], shape, faces) if "receding" in world else ()
    layer = layer_of(shape, opened, depth, receding)
    node_detectors = node_detectors_of(
        world.get("node_detectors", []), shape, len(bodies), beyond, layer
    )
    regions_of_the_law(node_detectors, shape, wraps)
    laid = [f for b in bodies for f in b.detector.gives]
    patterns_of_the_law([(d.name, d.pattern) for d in node_detectors], laid, families)
    settings_of_the_law([(d.name, d.axis, d.basis, d.pattern) for d in node_detectors], laid, families)
    counted = [body.family for body in bodies]  # a charged family's bodies each own a row of the sign
    families = derived.with_records(families, [counted.count(index) for index in range(len(families))])
    draw = draw_of(world["draw"], "draw", True) if "draw" in world else None
    draw = window.drawn(
        draw, node_detectors, bodies, families, shape, periodic, action
    )  # the regions' window: the longest passage of every lay with an end over the declared regions
    declared = any(key in world for key in ("bodies", "node_detectors"))  # named, even empty
    seed = seed_of(families, declared)  # the uniform seed of a world that declares nothing
    return World(
        shape,
        wraps,
        opened,
        depth,
        beyond,
        intervals,
        gamma,
        action,
        derived.largest_of(width),
        integers["link_unit"],
        kind_of(width),
        bound,
        families,
        bodies,
        node_detectors,
        receding,
        draw,
        seed,
    )
