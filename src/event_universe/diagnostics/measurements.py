"""Read-only world measurements. Their global cost is not local physics cost."""

from dataclasses import asdict
from fractions import Fraction

from event_universe.core.engine import Engine
from event_universe.core.faces import FACE_REGISTERS
from event_universe.core.linked_engine import LinkedEngine
from event_universe.core.links import LINK_REGISTERS
from event_universe.core.state import (
    CELL_REGISTERS,
    EMPTY_SLOT,
    PARTICLE_REGISTERS,
    Vector,
    checked,
    validate_cell,
    validate_particle,
)
from event_universe.core.streaming_engine import StreamingEngine
from event_universe.core.streams import STREAM_CELL_REGISTERS

ExactVector = tuple[int | Fraction, int | Fraction, int | Fraction]


def exact_component(value: Fraction) -> int | Fraction:
    return value.numerator if value.denominator == 1 else value


def particle_momentum(world: Engine) -> ExactVector:
    def component(axis: int) -> int | Fraction:
        return exact_component(
            sum(
                (Fraction(p.momentum[axis], p.momentum_den) for p in world.particles.values()),
                Fraction(0),
            )
        )

    return component(0), component(1), component(2)


def field_momentum(world: Engine) -> Vector:
    return (
        sum(c.px for c in world.cells.values()),
        sum(c.py for c in world.cells.values()),
        sum(c.pz for c in world.cells.values()),
    )


def total_momentum(world: Engine) -> ExactVector:
    matter, field = particle_momentum(world), field_momentum(world)
    return matter[0] + field[0], matter[1] + field[1], matter[2] + field[2]


def audit(world: Engine) -> dict[str, bool]:
    """Validate actual state using exceptions, also when Python runs with -O."""
    checked(world.tick)
    if world._face_transport is not None:
        world._face_transport.validate()
    if isinstance(world, StreamingEngine):
        world.streams.validate()
    seen: set[int] = set()
    for address, cell in world.cells.items():
        validate_cell(cell)
        if address != world.addr(*address):
            raise ValueError("non-canonical field address")
        if abs(cell.remainder) >= world.config.field_den:
            raise ValueError("invalid field remainder")
    for address, slots in world.occupancy.items():
        if address != world.addr(*address) or len(slots) != world.config.max_particles_per_cell:
            raise ValueError("invalid occupancy address or capacity")
        for pid in slots:
            checked(pid)
            if pid == EMPTY_SLOT:
                continue
            if pid < 0 or pid in seen or pid not in world.particles:
                raise ValueError("duplicate, unknown or invalid particle in occupancy")
            if world.particles[pid].position != address:
                raise ValueError("particle and occupancy disagree")
            seen.add(pid)
    if seen != set(world.particles):
        raise ValueError("a particle is missing from occupancy")
    for particle in world.particles.values():
        validate_particle(particle)
        if not 0 <= particle.move_budget < world.config.c_units * particle.move_budget_den:
            raise ValueError("movement budget outside one-tick interval")
        if particle.axis_phase < 0 or not -1 <= particle.last_update_tick < world.tick:
            raise ValueError("invalid particle phase or last-update marker")
        if any(
            abs(r) >= world.config.force_den
            for r in (particle.force_rx, particle.force_ry, particle.force_rz)
        ):
            raise ValueError("invalid force remainder")
    if isinstance(world, LinkedEngine):
        world.links.validate()
        for pid, transit in world.transits.items():
            if pid not in world.particles:
                raise ValueError("transit has no resident particle")
            for value in transit:
                checked(value)
            if (
                not 0 <= transit.direction < 6
                or not 0 <= transit.departure < world.tick
                or transit.due < world.tick
                or transit.length < 1
                or transit.due - transit.departure < transit.length
            ):
                raise ValueError("invalid or superluminal frozen transit")
    return {
        "bounded_integer_state": True,
        "fixed_records": True,
        "occupancy_consistent": True,
        "valid_remainders": True,
    }


def report(world: Engine) -> dict[str, object]:
    """Distinguish runtime checks from declared architecture and untested physical claims."""
    return {
        "tick": world.tick,
        "config": asdict(world.config),
        "faulted": world.faulted,
        "particles": len(world.particles),
        "active_cells": len(world.active),
        "materialized_cells": len(world.cells),
        "particle_momentum": particle_momentum(world),
        "field_momentum": field_momentum(world),
        "total_momentum": total_momentum(world),
        "checks": audit(world),
        "architecture": {
            "dimensions": 3,
            "nearest_neighbors": 6,
            "cell_registers": CELL_REGISTERS,
            "delivered_face_registers_per_cell": FACE_REGISTERS,
            "separate_scalar_face_registers_per_cell": (
                FACE_REGISTERS if world._face_transport is not None else 0
            ),
            "response_snapshot_work_registers_per_cell": (
                FACE_REGISTERS if world._old_face_response else 0
            ),
            "eligibility_snapshot_slots_per_cell": (
                world.config.max_particles_per_cell if world._old_face_response else 0
            ),
            "stream_registers_per_cell": (
                STREAM_CELL_REGISTERS if isinstance(world, StreamingEngine) else 0
            ),
            "link_registers_per_cell": LINK_REGISTERS if isinstance(world, LinkedEngine) else 0,
            "transit_registers_per_particle": 4 if isinstance(world, LinkedEngine) else 0,
            "particle_registers": PARTICLE_REGISTERS,
            "local_work_bound": "six neighbors and K fixed slots",
            "global_scheduler_constant_time": False,
        },
        "energy_conservation": "not established by this model",
    }
