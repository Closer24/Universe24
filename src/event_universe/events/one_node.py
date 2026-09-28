"""THE BOUND BODY IS ONE NODE (ALGEBRA.md #the-primitives, THE RULE'S OWN UNIVERSE), out of the loop's module: a body of one declared Node on a massive pair in a universe whose every held divisor is 1 (the well is the count) is a bound body, derived from the files and no flag; its record is the one-Node line at its Node, made from the two levels of its mode there, and no record of it lies on the GameBoard; in the universe of record (divisors above 1) no body is one and every body keeps its lattice record."""

from __future__ import annotations

from typing import Any, cast

import numpy as np

from event_universe.events.records import NodeRecord
from event_universe.loader.world import BlockDefinition, NatureBeamWorld


def one_node_body(world: NatureBeamWorld, definition: BlockDefinition) -> bool:
    """Whether the body is a bound body of one Node: one declared Node, a massive pair (den above |num|) and every held divisor of the universe 1."""
    held = [row.held_divisor for row in world.families if row.held_divisor is not None]
    one_node = definition.nodes is not None and len(definition.nodes) == 1
    massive = definition.kind[1] > abs(definition.kind[0])
    return one_node and massive and bool(held) and all(divisor == 1 for divisor in held)


def node_record_of(
    world: NatureBeamWorld, definition: BlockDefinition, shape: tuple[int, ...], identity: int
) -> NodeRecord | None:
    """The one-Node record of a bound body with a seed: its two levels read at its Node from the mode's two levels or its profile (both levels the profile at rest); None for a body that is not one Node."""
    if definition.seed <= 0 or not one_node_body(world, definition):
        return None
    flat = int(
        np.ravel_multi_index(cast("tuple[tuple[int, int, int], ...]", definition.nodes)[0], shape)
    )
    now, before = definition.levels or (definition.profile, definition.profile)
    return NodeRecord(identity, int(cast(Any, now)[flat]), int(cast(Any, before)[flat]))
