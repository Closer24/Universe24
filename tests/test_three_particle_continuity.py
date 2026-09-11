from dataclasses import asdict
from pathlib import Path

from event_universe import Config, Simulation
from event_universe.runner import source_fingerprint


def test_three_particles_move_at_most_one_neighbor_per_tick(request):
    visualize = request.config.getoption("--visualize-runs")
    if visualize:
        from event_universe.diagnostics.frames import capture_volume
        from event_universe.diagnostics.render import render_volume

    world = Simulation(Config(nx=64, ny=48, nz=32, c_units=12, force_den=1))
    for seed in ((0, 28, 23, 15, 3, 0, 0), (1, 36, 25, 15, -3, 0, 0), (2, 32, 19, 17, 0, 3, 0)):
        world.add_particle(*seed)
    frames = [capture_volume(world)] if visualize else []
    wraps = []
    try:
        for tick in range(1, 65):
            before = {pid: p.position for pid, p in world.particles.items()}
            world.step()
            if visualize:
                frames.append(capture_volume(world))
            assert set(world.particles) == {0, 1, 2}
            for pid, particle in world.particles.items():
                previous = before[pid]
                distances = [abs(a - b) for a, b in zip(previous, particle.position, strict=True)]
                distance = sum(min(d, size - d) for d, size in zip(distances, (64, 48, 32), strict=True))
                assert distance <= 1, (tick, pid, previous, particle.position)
                if sum(distances) > 1:
                    wraps.append((tick, pid, previous, particle.position))
        assert wraps == []  # This reported 64-tick experiment never reaches a periodic seam.
    finally:
        if visualize:
            render_volume(
                frames,
                Path("artifacts/three-particles-continuity.html"),
                title="Three particles: every tick, single playback",
                metadata={
                    "config": asdict(world.config),
                    "initial_particles": frames[0].particles,
                    "source_sha256": source_fingerprint(),
                    "model": "scalar-field-v10-contact",
                    "frame_stride": 1,
                    "test": "Each particle stays in place or moves to one periodic neighbor per tick",
                    "periodic_crossings": wraps,
                },
            )
