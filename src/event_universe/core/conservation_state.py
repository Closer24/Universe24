"""Immutable contracts for optional read-only energy and momentum observations."""

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .disturbance_state import Address3, DisturbanceRecord, Expression
    from .spatial_state import BoundMotion, Rays, Remainders, SpatialPopulations, SpatialState


@dataclass(frozen=True, slots=True)
class QuantityExpressions:
    energy: Expression
    momentum: Expression


@dataclass(frozen=True, slots=True)
class CarrierMeasurement:
    types: tuple[int, ...]
    quantities: QuantityExpressions


@dataclass(frozen=True, slots=True)
class ConservationDefinition:
    name: str
    energy_units: str
    momentum_units: str
    carriers: tuple[CarrierMeasurement, ...]
    spatial: QuantityExpressions | None = None


@dataclass(frozen=True, slots=True)
class InventoryNode:
    position: Address3
    records: tuple[DisturbanceRecord | None, ...]
    spatial: tuple[SpatialState, ...]
    incoming_spatial: tuple[SpatialState, ...] = ()
    rays: tuple[Rays, ...] = ()
    # The momentum register of the bound group held here (bound-group-motion-v1).
    group: BoundMotion | None = None
    # The remainder registers of the spreading families (field-remainder-v1).
    remainders: Remainders = ()


@dataclass(frozen=True, slots=True)
class InventoryPacket:
    kind: str
    origin: Address3
    slot: int
    port: int
    arrival_tick: int
    record: DisturbanceRecord | None = None
    spatial: tuple[SpatialPopulations, ...] = ()
    rays: tuple[Rays, ...] = ()
    # The register of a bound group stepping on this Link (bound-group-motion-v1).
    group: BoundMotion | None = None


@dataclass(frozen=True, slots=True)
class InventoryView:
    nodes: tuple[InventoryNode, ...]
    packets: tuple[InventoryPacket, ...]
