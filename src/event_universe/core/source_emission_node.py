"""The local envelope also owns its finite pending ordinary-source cycle."""

from dataclasses import dataclass

from .source_emission import EnvelopeEmissionState, PendingEnvelopeEmission
from .source_envelope_node import SourceEnvelopeNode


@dataclass(slots=True)
class EmittingEnvelopeNode(SourceEnvelopeNode):
    emission_state: EnvelopeEmissionState | None = None
    pending_emission: PendingEnvelopeEmission | None = None
    emission_next_tick: int = 0
