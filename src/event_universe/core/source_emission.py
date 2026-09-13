"""Bounded ordinary source proposals; no quantum query or executable payload."""

from dataclasses import dataclass

from .disturbance_state import Values
from .source_envelope_state import EnvelopeRemainder
from .spatial_state import SpatialBundle, SpatialState


@dataclass(frozen=True, slots=True)
class EnvelopeEmissionState:
    remainders: tuple[tuple[EnvelopeRemainder, ...], ...]
    phases: Values
    remaining: Values


@dataclass(frozen=True, slots=True)
class PendingEnvelopeEmission:
    ready_tick: int
    next_tick: int
    source_id: int
    populations: SpatialBundle
    source_delta: Values
    following: EnvelopeEmissionState
    cost: int
    cause_id: int | None = None


@dataclass(frozen=True, slots=True)
class SourceDeposit:
    states: tuple[SpatialState, ...]
    source_delta: Values
    cause_id: int | None = None
