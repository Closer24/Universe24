"""The world's files read into the lattice's world: the universe file (the integers and the families) and the world file (the lattice with its inner faces, the bodies declared NodeDetectors at a Node, the node_detectors); every key checked, every other key refused as unknown by name (the generator's mode file, its `lay` key and its laid bodies and `packets` among them since 2026-10-24, the owner's word: the generator goes, the seed is light at one quantum on every Node), no default written (ALGEBRA.md #a-familys-declaration)."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass

import numpy as np

from event_universe.core.integer import MAX_WORK_INT
from event_universe.core.rule3 import division_forward
from event_universe.loader import derived
from event_universe.loader.derived import FamilyRule
from event_universe.loader.interval import volume_rows
from event_universe.loader.keys import Node, document_at, integer, keyed
from event_universe.loader.seed import seed_of
from event_universe.loader.universe import universe_of

WORLD_KEYS: tuple[str, ...] = ("shape", "intervals", "universe")
WORLD_REQUIRED = WORLD_KEYS  # the three keys, every one required, 2026-10-24
TORUS = (
    True,
    True,
    True,
)  # the board is a torus, every axis wrapping (ALGEBRA.md, The board is a torus)


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
    seed: int  # the seed family, the universe's one massless family of quanta (`loader/seed.seed_of`)


def kind_of(width: int) -> type:
    """The kind of the run's arrays from the declared width, the one place the engine's integers are chosen (the owner, "choose 64 or 128 bits outside the engine, at the start"): the host's 64-bit integers where the width is at or under the host's signed bits, Python's integers (arrays of objects, exact at any width and slow) above it; the amplitude bound A is derived at the declared width either way (ENGINE.md, the loader)."""
    return np.int64 if width <= MAX_WORK_INT.bit_length() else object


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
    families = volume_rows(families, gamma)  # the held rows sourced by the tensions carry their volume
    intervals = integer(world["intervals"], "intervals", 0)
    families = derived.with_records(families, [0] * len(families))  # no declared record, 2026-10-24
    seed = seed_of(families)  # the uniform seed, the universe's one massless family of quanta
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
        seed,
    )
