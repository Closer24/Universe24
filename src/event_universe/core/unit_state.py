"""Immutable optional calibration metadata; never stored in evolving cells."""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class UnitDefinition:
    name: str
    dimensions: tuple[int, ...]
    si_scale: tuple[int, int]


@dataclass(frozen=True, slots=True)
class UnitSystem:
    base_scales: tuple[tuple[int, int], ...]
    units: tuple[UnitDefinition, ...]
    model_id: str = "si-rational-v1"
