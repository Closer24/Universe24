"""Explicit bounded port waiting from a frozen local vector, not a force law."""

from dataclasses import dataclass

from event_universe.core.disturbance_state import (
    Address3,
    CostMeter,
    OperationCosts,
    Payload,
    bounded,
    unpack,
)
from event_universe.core.integer import ceil_div, checked_work, dot_product
from event_universe.core.spatial_state import SpatialState


@dataclass(frozen=True, slots=True)
class DirectionalWaitLaw:
    spatial_index: int
    baseline: Payload
    offsets: tuple[Address3, ...]
    divisor: int
    link_ticks: int
    costs: OperationCosts

    def __call__(self, states: tuple[SpatialState, ...]) -> tuple[tuple[int, ...], int]:
        meter = CostMeter(self.costs)
        vector = list(unpack(self.baseline))
        for population in states[self.spatial_index].populations:
            for axis, value in enumerate(unpack(population)):
                vector[axis] = checked_work(vector[axis] + value)
        vector = [bounded(value) for value in vector]
        meter.charge("read", 9)
        meter.charge("update", 24)
        waits = []
        for offset in self.offsets:
            score = max(0, dot_product(tuple(vector), offset))
            waits.append(bounded(checked_work(ceil_div(score, self.divisor) * self.link_ticks)))
            meter.charge("evaluate", 5)
        return tuple(waits), meter.total
