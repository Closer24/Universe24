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
from event_universe.loader.interval import volume_rows
from event_universe.loader.keys import Node, connected, document_at, integer, keyed, node_of
from event_universe.loader.node_detector_declaration import (
    READER_RECORD_KEYS,
    NodeDetectorDeclaration,
    node_detector_of,
    packet_form,
)
from event_universe.loader.node_detector_rows import reader_count
from event_universe.loader.seed import seed_of
from event_universe.loader.universe import universe_of

WORLD_KEYS: tuple[str, ...] = ("shape", "intervals", "universe", "bodies")
WORLD_REQUIRED = ("shape", "intervals", "universe")  # bodies and node_detectors optional, 2026-10-24
TORUS = (
    True,
    True,
    True,
)  # the board is a torus, every axis wrapping (ALGEBRA.md, The board is a torus)
BODY_KEYS = ("family", "nodes", *READER_RECORD_KEYS)
BODY_REQUIRED = ("family", "nodes")
READER_NODE_KEYS = (
    "node",
    "weight",
)  # a reader's Node: the lay's weight, the record's count declared once


@dataclass(frozen=True)
class BodyRow:
    """A body as declared: its family, its Nodes in the declared order with the lay's weights (`counts`), and its declaration as a NodeDetector at a Node (`detector`, `loader/node_detector_declaration.py`: its parts the modes' labels with the count in one of them, its transitions, its emissions and its own draw), whose lay is the engine's own at the start (ALGEBRA.md, The click writes on the lattice (j); the owner's word, the body is at a Node). A body laid from the generator's mode file, and the bound body the frame tool declared an instrument, left with the generator (2026-10-24, the owner's word): every body declares its parts."""

    family: int
    nodes: tuple[Node, ...]
    counts: tuple[int, ...]
    detector: NodeDetectorDeclaration


@dataclass(frozen=True)
class World:
    """The world as loaded: the lattice's shape, the torus (`periodic`, every axis wrapping; the open and closed faces, the inner faces and the receding faces of the record worlds left 2026-10-24), the intervals, Gamma, T, the largest integer of the file's width, the kind of the run's arrays chosen by the width (`kind_of`), the amplitude bound A derived, the families, the bodies (each a NodeDetector at a Node), the node_detectors, the receding faces, the NodeDetectors' draw (`draw`, `loader/draw.py`, None where the world declares none: no draw and no write) and the seed family of a world that declares nothing (`loader/seed.seed_of`)."""

    shape: Node
    periodic: tuple[bool, bool, bool]
    intervals: int
    node_clock: int
    quantum_action: int
    width: int
    link_unit: int
    kind: type
    amplitude_bound: int
    families: tuple[FamilyRule, ...]
    bodies: tuple[BodyRow, ...]
    seed: int | None = None  # the seed family of a world that declares nothing (`loader/seed.seed_of`)


def kind_of(width: int) -> type:
    """The kind of the run's arrays from the declared width, the one place the engine's integers are chosen (the owner, "choose 64 or 128 bits outside the engine, at the start"): the host's 64-bit integers where the width is at or under the host's signed bits, Python's integers (arrays of objects, exact at any width and slow) above it; the amplitude bound A is derived at the declared width either way (ENGINE.md, the loader)."""
    return np.int64 if width <= MAX_WORK_INT.bit_length() else object


def bodies_of(
    value: object, families: tuple[FamilyRule, ...], shape: Node, action: int
) -> tuple[BodyRow, ...]:
    """The bodies: each its family (a family of quanta) and its Nodes (no Node shared), each Node with the lay's `weight` (1 where absent), a body declaring its `parts` (and as a reader its `transitions`, `rates` and `node_detector`) or its `conversion` (the record converted whole, with its `node_detector` and its `count`), its lay the engine's own over its region (`node_detector_of`; its emissions' lay decided by the board's shape against the declared width at the quantum action T, `packet_form`); a body declaring neither, the generator's laid body whose levels stood in the mode file, is refused by name (2026-10-24, the owner's word: the generator goes)."""
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
            node = node_of(line["node"], f"{label}.nodes[{index}].node", shape)
            if node in taken:
                raise ValueError(
                    f"{label}: two bodies share the Node {list(node)}; they stand apart or are one body"
                )
            taken.add(node)
            nodes.append(node)
            counts.append(integer(line.get("weight", 1), f"{label}.nodes[{index}].weight", 1))
        if not connected(tuple(nodes), shape, TORUS):
            raise ValueError(
                f"{label} declares its own record over a region in pieces: a NodeDetector's Nodes are one connected "
                "region through the six Ports (ALGEBRA.md, The NodeDetector is one declaration kind for every "
                "world); its Nodes are {[list(n) for n in nodes]}"
            )
        count = reader_count(body, label, families, family)
        parts = node_detector_of(body, label, families, family, quanta, count)
        parts = packet_form(parts, label, families, tuple(nodes), shape, TORUS, action)
        found.append(BodyRow(family, tuple(nodes), tuple(counts), parts))
    return tuple(found)


def even_box_refused(shape: Node, families: tuple[FamilyRule, ...]) -> None:
    """The board against the massless row's second double root (ALGEBRA.md, the two hands' line; the mathematician's reading of the shelved ion's refusal, branch `front-two-modes`): the massless band cos omega_k = (1 / 3) SUM_a cos k_a has two double roots, the uniform mode at k = 0 and the staggered mode (-1)^(x + y + z + t) at k = (pi, pi, pi), omega = pi, each of zero form and zero share; on a board periodic on all three axes with every extent even the staggered mode is an exact mode of a massless family (num = den), and Rule3's own rounding walks it as t^(3/2) / (3 N^(1/2)) with no bound, so such a board is refused by name with the family and the shape, the way out one odd extent or an open axis, where the mode is a bounded response; a gapped family has no double root there and is admitted; the extents' parity by the division act, no number of the law."""
    if not any(division_forward(extent, 2, 0)[1] for extent in shape):
        for family in (f for f in families if f.pair[0] == f.pair[1]):
            raise ValueError(
                f"the massless family {family.name!r} on the board {list(shape)} periodic on all three axes with "
                "every extent even: the staggered mode (-1)^(x + y + z + t), the band's top, is an exact mode of such "
                "a board and Rule3's own rounding walks it without bound; give one axis an odd extent"
            )


def parse_world(document: object, files: Mapping[str, object], digest: str) -> World:
    """The world from its document, the files it names (the universe, read by the host) and its digest; every defect refused by name; the board the torus (the owner's words of 2026-10-23 and 2026-10-24: the default a torus, then the torus the one board, the keys `boundary`, `face_depth`, `faces` and `receding` refused as unknown); a document naming neither `bodies` nor `node_detectors` declares nothing (the owner's word of 2026-10-24, the fold: a world of the universe, the board's shape and the run's length alone), its seed the universe's one massless family of quanta laid by the engine at one quantum on every Node and its reader the board itself (`loader/seed.seed_of`); a document naming them empty declares an empty board and runs as before (the former requirement of the two keys kept by name)."""
    world = keyed(document, "the world", WORLD_KEYS, WORLD_REQUIRED)
    integers, families = universe_of(document_at(files, world["universe"], "universe"))
    shape_value = world["shape"]
    if not isinstance(shape_value, list) or len(shape_value) != 3:
        raise ValueError("shape must be [X, Y, Z]")
    extents = tuple(integer(extent, f"shape[{axis}]", 1) for axis, extent in enumerate(shape_value))
    shape = (extents[0], extents[1], extents[2])
    even_box_refused(shape, families)
    gamma, action = integers["node_clock"], integers["quantum_action"]
    width = integers["width"]
    bound = derived.amplitude_bound(families, gamma, action, width, integers["link_unit"])
    bodies = bodies_of(world.get("bodies", []), families, shape, action)
    families = volume_rows(families, gamma)  # the held rows sourced by the tensions carry their volume
    bodies = window.windowed(bodies, families, shape, TORUS, action)  # the derived windows
    conversion.together(families, bodies)  # the multisets a close can credit, refused by name
    intervals = integer(world["intervals"], "intervals", 0)
    counted = [body.family for body in bodies]  # a charged family's bodies each own a row of the sign
    families = derived.with_records(families, [counted.count(index) for index in range(len(families))])
    declared = "bodies" in world  # named, even empty
    seed = seed_of(families, declared)  # the uniform seed of a world that declares nothing
    return World(
        shape,
        TORUS,
        intervals,
        gamma,
        action,
        derived.largest_of(width),
        integers["link_unit"],
        kind_of(width),
        bound,
        families,
        bodies,
        seed,
    )
