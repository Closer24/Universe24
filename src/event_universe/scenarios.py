"""Named, reproducible initial conditions. No physical laws live in scenarios."""

from dataclasses import dataclass

from event_universe.api import LinkedSimulation, Simulation
from event_universe.core.contracts import Observer
from event_universe.core.engine import Engine
from event_universe.core.links import LinkConfig
from event_universe.core.state import Config
from event_universe.diagnostics.frames import Slice

ParticleSeed = tuple[int, int, int, int, int, int, int]


@dataclass(frozen=True, slots=True)
class Scenario:
    name: str
    config: Config
    particles: tuple[ParticleSeed, ...]
    ticks: int
    view: Slice
    links: LinkConfig | None = None

    def create(self, observer: Observer | None = None) -> Engine:
        world: Engine = (
            Simulation(self.config, observer=observer)
            if self.links is None
            else LinkedSimulation(self.config, links=self.links, observer=observer)
        )
        for particle in self.particles:
            world.add_particle(*particle)
        return world


def get_scenario(name: str) -> Scenario:
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
