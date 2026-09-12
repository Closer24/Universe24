"""Named, reproducible initial conditions. No physical laws live in scenarios."""

from dataclasses import dataclass

from event_universe.core.contracts import Observer
from event_universe.core.links import LinkConfig
from event_universe.core.scalar_engine import ScalarEngine
from event_universe.core.state import Config
from event_universe.diagnostics.frames import Slice
from event_universe.particle_api import LinkedSimulation
from event_universe.particle_api import ScalarSimulation as Simulation

ParticleSeed = tuple[int, int, int, int, int, int, int]


@dataclass(frozen=True, slots=True)
class Scenario:
    name: str
    config: Config
    particles: tuple[ParticleSeed, ...]
    ticks: int
    view: Slice
    links: LinkConfig | None = None
    masses: tuple[int, ...] = ()
    collisions: bool = False

    def create(self, observer: Observer | None = None) -> ScalarEngine:
        world: ScalarEngine = (
            Simulation(self.config, observer=observer, collisions=self.collisions)
            if self.links is None
            else LinkedSimulation(
                self.config, links=self.links, observer=observer, collisions=self.collisions
            )
        )
        if self.masses and len(self.masses) != len(self.particles):
            raise ValueError("provide one mass per particle seed")
        for index, particle in enumerate(self.particles):
            world.add_particle(*particle, mass=self.masses[index] if self.masses else 1)
        return world


def get_scenario(name: str) -> Scenario:
    if name in ("collision", "collision-masses", "collision-links"):
        return Scenario(
            name,
            Config(nx=40, ny=12, nz=12, c_units=12, source_strength=0),
            ((0, 14, 6, 6, 6, 0, 0), (1, 18, 6, 6, -6, 0, 0)),
            48,
            Slice("XY", 6),
            LinkConfig(base_length=2, stretch_num=0) if name == "collision-links" else None,
            (1, 2) if name == "collision-masses" else (1, 1),
            True,
        )
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
