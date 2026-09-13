"""Small bridge for legacy notebook imports and diagnostic method names.

State is now read-only. Replace private `_node(...)[PHI] = value` initialization
with `seed_field(...)`. self_tests lives in pytest; report checks are explicit.
"""

from event_universe.core.state import Config, Vector
from event_universe.diagnostics.frames import Slice, capture_frame
from event_universe.diagnostics.measurements import (
    ExactVector,
    audit,
    field_momentum,
    particle_momentum,
    report,
    total_momentum,
)
from event_universe.diagnostics.recorder import TraceRecorder
from event_universe.particle_api import ScalarSimulation as Simulation


class IntegerO1Field3D(Simulation):
    """Legacy history-enabled facade. Modern applications opt into a recorder explicitly."""

    def __init__(self, config: Config | None = None) -> None:
        self.recorder = TraceRecorder()
        super().__init__(config, observer=self.recorder)
        self.paths = self.recorder.paths
        self.force_records = self.recorder.force_records
        self.collisions = self.recorder.collisions

    def total_particle_momentum(self) -> ExactVector:
        return particle_momentum(self)

    def total_field_momentum(self) -> Vector:
        return field_momentum(self)

    def total_momentum(self) -> ExactVector:
        return total_momentum(self)

    def xy_slice(self, z: int) -> dict[tuple[int, int], int]:
        return capture_frame(self, Slice("XY", z)).field

    def particles_on_xy_slice(self, z: int) -> list[tuple[int, int, int, int, int, int]]:
        return capture_frame(self, Slice("XY", z)).particles

    def audit(self) -> bool:
        audit(self)
        return True

    def report(self) -> dict[str, object]:
        return report(self)


IntegerO1Field = IntegerO1Field3D
