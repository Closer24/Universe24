"""Named, reproducible initial conditions. No physical laws live in scenarios."""

from dataclasses import dataclass

from event_universe.api import LinkedSimulation, SharedActionSimulation, Simulation
from event_universe.core.contracts import Observer
from event_universe.core.engine import Engine
from event_universe.core.links import LinkConfig
from event_universe.core.state import Config
from event_universe.diagnostics.frames import Slice
from event_universe.models.shared_action import SharedActionConfig

ParticleSeed = tuple[int, int, int, int, int, int, int]


@dataclass(frozen=True, slots=True)
class Scenario:
    name: str
    config: Config
    particles: tuple[ParticleSeed, ...]
    ticks: int
    view: Slice
    links: LinkConfig | None = None
    action: SharedActionConfig | None = None

    def create(self, observer: Observer | None = None) -> Engine:
        world: Engine
        if self.action is not None:
            if self.links is not None or self.config != self.action.engine_config():
                raise ValueError("shared-action settings must match Config; mixed models unsupported")
            world = SharedActionSimulation(self.action, observer=observer)
        elif self.links is not None:
            world = LinkedSimulation(self.config, links=self.links, observer=observer)
        else:
            world = Simulation(self.config, observer=observer)
        for particle in self.particles:
            world.add_particle(*particle)
        return world


def get_scenario(name: str) -> Scenario:
    if name in ("action-contact", "action-isolated", "action-rest", "action-free"):
        # Explicit demonstration scale, NOT a new default or physical calibration.
        settings = SharedActionConfig(impulse_units=64, coupling=0 if name == "action-free" else 64)
        seeds: tuple[ParticleSeed, ...] = ((0, 24, 23, 16, 3, 2, 1),)
        if name == "action-contact":
            seeds = ((0, 25, 23, 16, 3, 0, 0), (1, 35, 25, 16, -3, 0, 0))
        elif name == "action-rest":
            seeds = ((0, 32, 24, 16, 0, 0, 0),)
        return Scenario(name, settings.engine_config(), seeds, 72, Slice("XY", 16), action=settings)
    if name == "links":
        return Scenario(
            name,
            Config(nx=32, ny=24, nz=12, c_units=12, force_den=12),
            ((0, 12, 11, 6, 6, 0, 0), (1, 19, 13, 6, -6, 0, 0)),
            360,
            Slice("XY", 6),
            LinkConfig(base_length=10),
        )
    if name == "contact":
        return Scenario(
            name,
            Config(nx=64, ny=48, nz=24, c_units=12, force_den=1),
            ((0, 28, 23, 12, 3, 0, 0), (1, 36, 25, 12, -3, 0, 0)),
            48,
            Slice("XY", 12),
        )
    if name == "turning":
        return Scenario(
            name,
            Config(nx=128, ny=96, nz=32, c_units=12, force_den=12),
            ((0, 44, 47, 16, 3, 0, 0), (1, 84, 49, 16, -3, 0, 0)),
            110,
            Slice("XY", 16),
        )
    if name == "stationary":
        return Scenario(
            name, Config(nx=48, ny=48, nz=48), ((0, 24, 24, 24, 0, 0, 0),), 120, Slice("XY", 24)
        )
    raise ValueError(f"unknown scenario: {name}")
