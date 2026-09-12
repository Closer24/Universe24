"""Render the balanced-halo acceptance cases and one failing legacy control.

Run with PYTHONPATH=src python tools/check_diagonal_motion.py. The legacy control
documents grouped movement; every candidate case must pass for exit status zero.
"""

import json
from pathlib import Path
from uuid import uuid4

from event_universe.api import BalancedSimulation, Simulation
from event_universe.core.state import Config
from event_universe.diagnostics.frames import capture_volume
from event_universe.diagnostics.measurements import total_momentum
from event_universe.diagnostics.render import render_volume
from event_universe.retention import ArtifactLease, cleanup_expired, validate_output_path
from event_universe.runner import source_fingerprint


def check_case(
    output, label, simulation, source_strength, ticks=30, initial=(600, 400, 0), c_units=1000
):
    world = simulation(
        Config(nx=128, ny=128, nz=32, source_strength=source_strength, force_den=1, c_units=c_units)
    )
    world.add_particle(0, 40, 40, 16, *initial)
    frames = [capture_volume(world)]
    first_impulse = None
    max_error = 0
    conserved = True
    for _ in range(ticks):
        previous = world.particles[0].position
        world.step()
        particle = world.particles[0]
        assert sum(abs(a - b) for a, b in zip(previous, particle.position, strict=True)) <= 1
        conserved = conserved and total_momentum(world) == initial
        max_error = max(max_error, abs((particle.x - 40) * initial[1] - (particle.y - 40) * initial[0]))
        frames.append(capture_volume(world))
        if particle.momentum != initial:
            first_impulse = {"tick": world.tick, "momentum": particle.momentum}
            break
    passed = first_impulse is None and max_error < sum(abs(v) for v in initial)
    result = dict(
        case=label,
        ticks=world.tick,
        source_strength=source_strength,
        c_units=c_units,
        initial_particle_momentum=initial,
        final_particle_momentum=world.particles[0].momentum,
        final_position=world.particles[0].position,
        first_self_impulse=first_impulse,
        max_cross_product_error=max_error,
        total_momentum_conserved=conserved,
        straight_motion_passed=passed,
        source_sha256=source_fingerprint(),
        upstream_base="76676d48ffbe7fc53913f4d26464921cb20f72df",
    )
    (output / f"{label}.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result), flush=True)
    render_volume(
        frames,
        output / f"{label}.html",
        title=f"{'PASS' if passed else 'FAIL'}: {label}",
        metadata=result,
    )
    return result


def main():
    output = Path("artifacts/diagonal-motion") / uuid4().hex
    validate_output_path(output)
    cleanup_expired(output.parent)
    output.mkdir(parents=True)
    with ArtifactLease(output.parent, [output.absolute()]):
        status = run_cases(output)
    raise SystemExit(status)


def run_cases(output):
    results = [
        check_case(output, "legacy-no-field", Simulation, 0),
        check_case(output, "balanced-no-field", BalancedSimulation, 0),
        check_case(output, "balanced-own-field", BalancedSimulation, 64),
        check_case(
            output,
            "balanced-own-field-slower",
            BalancedSimulation,
            64,
            ticks=72,
            initial=(6, 4, 0),
            c_units=12,
        ),
        check_case(
            output,
            "balanced-own-field-slow",
            BalancedSimulation,
            64,
            ticks=72,
            initial=(1, 1, 0),
            c_units=12,
        ),
    ]
    (output / "results.json").write_text(json.dumps(results, indent=2) + "\n")
    return 0 if all(r["straight_motion_passed"] for r in results[1:]) else 1


if __name__ == "__main__":
    main()
