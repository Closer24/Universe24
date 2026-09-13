"""Immutable local node views; no evolution, topology traversal or history."""

from dataclasses import dataclass

from .disturbance_state import Address3, NodeView, Packet, Values
from .spatial_state import SpatialPacket, SpatialState


@dataclass(frozen=True, slots=True)
class SpatialNodeView:
    states: tuple[SpatialState, ...]
    last_cost: int
    received_count: int
    reaction_phases: Values
    sample_values: Values
    sample_fluxes: Values
    last_begin_tick: int
    received_decay_cost: int
    sample_ports: tuple[Values, ...]


@dataclass(frozen=True, slots=True)
class NodeSnapshot:
    """Owned local registers and outgoing packets at one audit tick.

    None means that lane has no materialized state. Immutable baseline/type
    definitions remain in initialization, not copied into every snapshot.
    Carrier and spatial lanes preserve their separate commit boundaries.
    """

    position: Address3
    audit_tick: int
    carrier: NodeView | None
    spatial: SpatialNodeView | None
    outgoing: tuple[Packet | None, ...]
    spatial_outgoing: tuple[SpatialPacket | None, ...]
