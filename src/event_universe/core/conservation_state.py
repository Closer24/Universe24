"""Immutable contracts for optional read-only energy and momentum observations."""

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .disturbance_state import Address3, DisturbanceRecord, Expression
    from .spatial_state import Rays, SpatialPopulations, SpatialState


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
    # The resident rays per spatial field, on their way or waiting, and beside
    # them the parked shadows (node-is-ports-v1): the shares below one quantum,
    # in units of the family's split denominator, and the traces (amount 0).
    rays: tuple[Rays, ...] = ()
    parked: tuple[Rays, ...] = ()


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


@dataclass(frozen=True, slots=True)
class InventoryView:
    nodes: tuple[InventoryNode, ...]
    packets: tuple[InventoryPacket, ...]
