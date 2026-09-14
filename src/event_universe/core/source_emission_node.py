"""The local envelope also owns its finite pending ordinary-source cycle."""

from dataclasses import dataclass

from .source_emission import EnvelopeEmissionState, PendingEnvelopeEmission
from .source_envelope_node import SourceEnvelopeNode


@dataclass(slots=True)
class EmittingEnvelopeNode(SourceEnvelopeNode):
    emission_state: EnvelopeEmissionState | None = None
    pending_emission: PendingEnvelopeEmission | None = None
    emission_next_tick: int = 0
    generations: tuple[EmittingEnvelopeNode, ...] = ()

    def __post_init__(self) -> None:
        super(EmittingEnvelopeNode, self).__post_init__()
        if type(self.generations) is not tuple or len(self.generations) > 5:
            raise ValueError("a source Node supports at most six fixed generation banks")
        if any(
            type(node) is not EmittingEnvelopeNode or node.position != self.position or node.generations
            for node in self.generations
        ):
            raise ValueError("source generations must be flat colocated envelope banks")
