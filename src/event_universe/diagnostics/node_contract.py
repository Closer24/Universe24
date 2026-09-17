"""Read-only audit of formula-free evolving NodeState, records and transit state."""

from dataclasses import fields, is_dataclass
from typing import cast

from event_universe.core.disturbance_node import DisturbanceNode
from event_universe.core.disturbance_state import (
    Departure,
    DisturbanceNodeState,
    DisturbanceRecord,
    LocalPlan,
    NodeView,
    Packet,
    PendingCycle,
)
from event_universe.core.node_ports import PortBank
from event_universe.core.source_emission import EnvelopeEmissionState, PendingEnvelopeEmission
from event_universe.core.source_emission_node import EmittingEnvelopeNode
from event_universe.core.source_envelope_node import (
    EnvelopeGate,
    EnvelopePacket,
    PendingEnvelopeCorrection,
    PendingEnvelopeGate,
    PendingEnvelopeScale,
    PendingEnvelopeStop,
    SourceEnvelopeNode,
)
from event_universe.core.source_envelope_state import (
    EnvelopeAmplitude,
    EnvelopeRemainder,
    EnvelopeScale,
    NullRecord,
)
from event_universe.core.spatial_node import PendingSpatialCycle, SpatialNode
from event_universe.core.spatial_state import (
    Claim,
    FieldInteractionGuard,
    FieldRuleGuard,
    Ray,
    SpatialNodeState,
    SpatialPacket,
    SpatialPlan,
    SpatialState,
)

STATE_RECORDS = (
    DisturbanceNode,
    SpatialNode,
    PortBank,
    PendingSpatialCycle,
    NodeView,
    DisturbanceNodeState,
    DisturbanceRecord,
    LocalPlan,
    Packet,
    PendingCycle,
    FieldInteractionGuard,
    FieldRuleGuard,
    Ray,
    Claim,
    SpatialNodeState,
    SpatialPacket,
    SpatialPlan,
    SpatialState,
    EnvelopeAmplitude,
    EnvelopeRemainder,
    EnvelopeScale,
    NullRecord,
    EnvelopeGate,
    EnvelopePacket,
    PendingEnvelopeGate,
    PendingEnvelopeScale,
    PendingEnvelopeStop,
    SourceEnvelopeNode,
    EnvelopeEmissionState,
    PendingEnvelopeEmission,
    EmittingEnvelopeNode,
    PendingEnvelopeCorrection,
)


def node_state_violations(value: object) -> tuple[str, ...]:
    """Inspect the complete reachable NodeState graph without evaluating any law."""
    errors: list[str] = []
    active: set[int] = set()

    def visit(item: object, path: str) -> None:
        if item is None or type(item) is int:
            return
        if id(item) in active:
            errors.append(f"{path}: cyclic evolving state")
            return
        active.add(id(item))
        try:
            if type(item) in STATE_RECORDS and is_dataclass(item):
                for member in fields(item):
                    visit(getattr(item, member.name), f"{path}.{member.name}")
            elif type(item) in (tuple, Departure):
                for index, child in enumerate(cast(tuple[object, ...], item)):
                    visit(child, f"{path}[{index}]")
            else:
                errors.append(f"{path}: forbidden NodeState object {type(item).__name__}")
        finally:
            active.remove(id(item))

    visit(value, "state")
    return tuple(errors)
