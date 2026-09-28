"""THE BOUND BODY IS ONE NODE (ALGEBRA.md #the-primitives, THE RULE'S OWN UNIVERSE) as a GameBoard reading beside the lattice record: a body of one declared Node on a massive pair in a universe whose every held divisor is 1 (the well is the count) is bound per the files and no flag; the reading gives its lattice record's two levels and remainder at its Node and the one-Node line's coefficient and wall there, the rotation the line reads at the pixel (GAMEBOARD, a diagnostic and no step): the pixel keeps its lattice record and Rule3 steps at every Node; in the universe of record (divisors above 1) no body is bound."""

from __future__ import annotations

from typing import TYPE_CHECKING, cast

from event_universe.loader.world import BlockDefinition, NatureBeamWorld

if TYPE_CHECKING:
    from event_universe.events import detector_law, records


def one_node_body(world: NatureBeamWorld, definition: BlockDefinition) -> bool:
    """Whether the body is bound per the files: one declared Node, a massive pair (den above |num|) and every held divisor of the universe 1."""
    held = [row.held_divisor for row in world.families if row.held_divisor is not None]
    one_node = definition.nodes is not None and len(definition.nodes) == 1
    massive = definition.kind[1] > abs(definition.kind[0])
    return one_node and massive and bool(held) and all(divisor == 1 for divisor in held)


def rotation_reading(
    loop: detector_law.DetectorLawSimulation, block: records.Block
) -> dict[str, list[int]] | None:
    """GAMEBOARD: on a bound body with its lattice record, `node` its Node, `levels` the record's (now, before, remainder) there and `line` the one-Node line's (coefficient, wall) there (`node_record_coefficients`: 2 cos omega = coefficient / wall as the line reads it at the pixel, ALGEBRA.md #what-a-body-is); None on any other body."""
    if block.own is None or not one_node_body(loop.world, block.definition):
        return None
    node = tuple(cast("tuple[tuple[int, int, int], ...]", block.definition.nodes)[0])
    own = block.own
    levels = [int(own.now[node]), int(own.before[node]), int(own.remainder[node])]
    return {"node": list(node), "levels": levels, "line": list(loop.node_record_coefficients(block))}
