"""Finite integer attenuation of a delivered packet, before merging neighbors."""

from dataclasses import dataclass

from event_universe.core.disturbance_state import (
    CostMeter,
    FieldDefinition,
    OperationCosts,
    Values,
    bounded,
    pack,
    unpack,
)
from event_universe.core.integer import checked_work
from event_universe.core.spatial_state import (
    DecayDefinition,
    SpatialBundle,
    SpatialFieldDefinition,
    SpatialPopulations,
)


def decay_populations(
    populations: SpatialPopulations,
    definition: DecayDefinition,
    field: FieldDefinition,
    meter: CostMeter,
) -> tuple[SpatialPopulations, tuple[int, ...]]:
    """Discard fractional survivors; signed components shrink toward zero."""
    numerator = bounded(definition.retain_numerator)
    denominator = bounded(definition.retain_denominator)
    if not 0 <= numerator < denominator:
        raise ValueError("decay requires 0 <= retain_numerator < retain_denominator")
    if len(populations) != 8:
        raise ValueError("spatial decay requires exactly eight octants")
    survivors = []
    losses = [0] * field.components
    for payload in populations:
        field.validate(payload)
        meter.charge("read")
        retained = []
        for component, value in enumerate(unpack(payload)):
            magnitude = checked_work(abs(value) * numerator) // denominator
            survivor = -magnitude if value < 0 else magnitude
            retained.append(survivor)
            losses[component] = checked_work(losses[component] + value - survivor)
            # Multiplication/division, sign application and the population write.
            meter.charge("update", 3)
        survivors.append(pack(tuple(retained)))
    return tuple(survivors), tuple(losses)


@dataclass(frozen=True, slots=True)
class SpatialDecayLaw:
    fields: tuple[FieldDefinition, ...]
    definitions: tuple[SpatialFieldDefinition, ...]
    costs: OperationCosts

    def __call__(self, bundle: SpatialBundle) -> tuple[SpatialBundle, Values, int]:
        if len(bundle) != len(self.definitions):
            raise ValueError("decay packet field count differs from its definitions")
        meter = CostMeter(self.costs)
        survivors = []
        losses = [(0,) * field.components for field in self.fields]
        for populations, definition in zip(bundle, self.definitions, strict=True):
            field = self.fields[definition.field]
            if definition.decay is None:
                raise ValueError("dissipative delivery requires an explicit decay for every field")
            retained, losses[definition.field] = decay_populations(
                populations, definition.decay, field, meter
            )
            survivors.append(retained)
        return tuple(survivors), tuple(losses), meter.total
