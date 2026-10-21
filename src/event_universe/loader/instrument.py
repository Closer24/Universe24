"""A bound record declared an instrument body by the host's frame tool (2026-10-21; the reader's design of the conserving click, (b): the parts, the transition and the resonance written into the mode file by the tool as a derived declaration, "declaring what the law derives until the body runs"; ALGEBRA.md, The click writes on the lattice (3) and (4); The emission of a bound record is the click's act of the taker): the mode entry's key `instrument` (loader/mode.instrument_of, typed by tools/frame_of.py) read into the declaration the engine holds for every detector body (`instrument_body`, loader/node_detector_declaration.node_detector_of), the body's levels the mode file's as laid into the part carrying its count (`laid_parts`, `Lattice.lay`), its Links uncut and the step untouched (`meeting.cut`), its standing region the Nodes its click writes over (`BodyRow.region`, `BodyRow.shares`, node_detector.books_of); so that the engine's instrument-body click runs on the bound record with no new act and no body-wide re-lay."""

from __future__ import annotations

from dataclasses import replace
from typing import TYPE_CHECKING

from event_universe.loader.derived import FamilyRule
from event_universe.loader.faces import connected
from event_universe.loader.keys import Node, integer, keyed, node_of
from event_universe.loader.mode import instrument_of
from event_universe.loader.node_detector_declaration import node_detector_of, packet_form

if TYPE_CHECKING:
    from event_universe.loader.packets import PacketRow
    from event_universe.loader.world import BodyRow

REGION_NODE_KEYS = ("node", "weight")  # a standing region's Node with the lay's weight (1 where absent)


def declared_body(
    row: BodyRow,
    written: object,
    label: str,
    families: tuple[FamilyRule, ...],
    quanta: dict[str, int],
    shape: Node,
    beyond: tuple[Node, ...],
    action: int,
    periodic: tuple[bool, bool, bool],
) -> BodyRow:
    """A laid body's row with its declaration where its mode entry `written` carries the key `instrument` (`instrument_of`, `instrument_body`), the row otherwise unchanged."""
    instrument = instrument_of(written, label)
    if instrument is None:
        return row
    return instrument_body(
        row, instrument, f"{label}.instrument", families, quanta, shape, beyond, action, periodic
    )


def instrument_body(
    row: BodyRow,
    instrument: dict[str, object],
    label: str,
    families: tuple[FamilyRule, ...],
    quanta: dict[str, int],
    shape: Node,
    beyond: tuple[Node, ...],
    action: int,
    periodic: tuple[bool, bool, bool],
) -> BodyRow:
    """A bound body declared an instrument body by the host's frame tool (the mode entry's `instrument`): the declaration read in the form the loader reads for every detector body (`node_detector_of`: its `parts` with the count in the level it stands in, its `transitions`, its `rates`, its `node_detector`, the emissions' lay decided by the board's shape from every Node of its region, `packet_form`), its `nodes` the standing region with the lay's weights (one connected region of distinct Nodes through the six Ports holding one of the body's declared Nodes, none beyond the board, refused by name otherwise), the body's levels the mode file's as laid (its record standing in its well, its Links uncut, the step untouched); the count the body's declared count, read by the gate at its declared Node as for every laid body."""
    nodes = instrument["nodes"]
    if not isinstance(nodes, list) or not nodes:
        raise ValueError(f"{label}.nodes must list the standing region's Nodes with their weights")
    region, shares = [], []
    for index, line in enumerate(nodes):
        keyed(line, f"{label}.nodes[{index}]", REGION_NODE_KEYS, ("node",))
        region.append(node_of(line["node"], f"{label}.nodes[{index}].node", shape, beyond))
        shares.append(integer(line.get("weight", 1), f"{label}.nodes[{index}].weight", 1))
    if len(set(region)) != len(region) or not connected(tuple(region), shape, periodic):
        raise ValueError(
            f"{label}.nodes is one connected region of distinct Nodes through the six Ports, the body's standing "
            "region (ALGEBRA.md, The NodeDetector is one declaration kind for every experiment)"
        )
    if not any(node in region for node in row.nodes):
        raise ValueError(
            f"{label}.nodes holds none of the body's declared Nodes {[list(n) for n in row.nodes]}: the standing "
            "region stands about the Node the body is declared at"
        )
    declaration = node_detector_of(instrument, label, families, row.family, quanta, sum(row.counts))
    declaration = packet_form(declaration, label, families, tuple(region), shape, action)
    return replace(row, detector=declaration, region=tuple(region), shares=tuple(shares))


def laid_parts(row: BodyRow | PacketRow, family: FamilyRule) -> list[int]:
    """The parts of a record the mode file's levels are laid on (`Lattice.lay`): every part alike for a packet and for a body without a declaration (the pair family's two parts laid equal, ALGEBRA.md #the-click-is-the-meeting), and for a bound body declared an instrument body the part carrying its declared count alone, the level it stands in (the other parts empty, a lay in one mode having no amplitude in any other, The click writes on the lattice (j))."""
    detector = getattr(row, "detector", None)
    if detector is None:
        return list(range(family.parts))
    return [part for part, count in enumerate(detector.counts) if count]
