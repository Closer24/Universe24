"""Bounded local owner views and declarative transition-invariant contracts."""

from dataclasses import dataclass
from typing import TYPE_CHECKING, Protocol

if TYPE_CHECKING:
    from .disturbance_state import DisturbanceRecord, Expression
    from .spatial_state import SpatialBundle


@dataclass(frozen=True, slots=True)
class CarrierReadout:
    types: tuple[int, ...]
    expression: Expression


@dataclass(frozen=True, slots=True)
class ConservedReadout:
    name: str
    components: int
    units: str
    carriers: tuple[CarrierReadout, ...]
    spatial: Expression | None = None


@dataclass(frozen=True, slots=True)
class NodeConservationDefinition:
    name: str
    quantities: tuple[ConservedReadout, ...]


@dataclass(frozen=True, slots=True)
class LocalInventory:
    """Actual local stock and individual transfers, excluding copied samples/plans.

    A caller supplies either before or proposed-after owners for one transition.
    Pending originals remain in records; their proposed replacements are not stock.
    An incoming packet belongs on the before side until acceptance. An outgoing
    packet belongs on the after side once its source gives up ownership.
    """

    records: tuple[DisturbanceRecord | None, ...] = ()
    spatial: SpatialBundle = ()
    carrier_packets: tuple[DisturbanceRecord, ...] = ()
    spatial_packets: tuple[SpatialBundle, ...] = ()


class NodeConservationGuard(Protocol):
    def check(self, before: LocalInventory, after: LocalInventory, label: str) -> None: ...
