"""Engine extension for one-link causal outward field streaming."""

from collections.abc import Callable

from .contracts import NullObserver, Observer, ParticleRule
from .engine import Engine
from .state import Address, CellState, Config, Neighbors
from .streams import Octants, Outgoing, StreamTransport

StreamRule = Callable[[Octants, int, int, int], Outgoing]
SampleRule = Callable[[Neighbors], Neighbors]


def _unused_field_rule(cell: CellState, neighbors: Neighbors, sources: int, config: Config) -> CellState:
    """Streaming transport replaces the scalar field phase in this candidate."""
    return cell


class StreamingEngine(Engine):
    """Advance field streams first, then let particles read only delivered flux."""

    def __init__(
        self,
        config: Config,
        particle_rule: ParticleRule,
        stream_rule: StreamRule,
        source_per_octant: int,
        sample_rule: SampleRule,
        observer: Observer | None = None,
    ) -> None:
        super().__init__(config, _unused_field_rule, particle_rule, observer or NullObserver())
        self.streams = StreamTransport(self._lattice, stream_rule, source_per_octant)
        self._sample_rule = sample_rule

    def _begin_tick(self) -> None:
        source_counts = {
            position: sum(pid >= 0 for pid in slots)
            for position, slots in self._occupancy.items()
            if any(pid >= 0 for pid in slots)
        }
        self.streams.advance(source_counts, self.tick)

    def _field_step(self) -> None:
        """The stream transport already completed the candidate field phase."""

    def _particle_neighbors(self, position: Address) -> Neighbors:
        return self._sample_rule(self.streams.at(position).flux)
