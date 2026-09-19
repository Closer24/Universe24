"""Bounded local operators for the reversible-detector-v1 candidate.

The contract is docs/DETECTOR_REQUIREMENTS.md. These immutable values are
temporary local inputs and proposals, not additional physical storage.
"""

from dataclasses import dataclass

from event_universe.core.integer import checked_work
from event_universe.core.lattice import PORT_HEADINGS

STATE_BOUND = (1 << 62) - 1
MAX_PHASE_STEPS = 4096


@dataclass(frozen=True)
class CarrierState:
    """One intact local carrier, including its canonical momentum."""

    family: int
    number: int
    amount: int
    phase: int
    port: int
    momentum: tuple[int, int, int]


@dataclass(frozen=True)
class ContactState:
    """The existing material Event's pointer and recoil."""

    phase: int
    momentum: tuple[int, int, int]


def _integer(value: int, name: str, low: int = 0, high: int = STATE_BOUND) -> int:
    if type(value) is not int or not low <= value <= high:
        raise ValueError(f"reversible detector: {name} must be an integer in [{low}, {high}]")
    return value


def _phase_modulus(phase_steps: int) -> int:
    value = _integer(phase_steps, "phase_steps", 2, MAX_PHASE_STEPS)
    if value & (value - 1):
        raise ValueError("reversible detector: phase_steps must be a power of two")
    return value


def _result(value: int) -> int:
    checked_work(value)
    if not -STATE_BOUND <= value <= STATE_BOUND:
        raise OverflowError("reversible detector: physical state range exceeded")
    return value


def _momentum(momentum: tuple[int, int, int]) -> None:
    if not isinstance(momentum, tuple) or len(momentum) != 3:
        raise ValueError("reversible detector: momentum must have three integer components")
    for component in momentum:
        _integer(component, "momentum", -STATE_BOUND)


def canonical_momentum(amount: int, quantum: int, port: int) -> tuple[int, int, int]:
    """Canonical carrier momentum; check the product before any assignment."""
    _integer(amount, "amount", 1)
    _integer(quantum, "quantum", 1)
    _integer(port, "port", 0, 5)
    magnitude = _result(checked_work(amount * quantum))
    x, y, z = PORT_HEADINGS[port]
    return magnitude * x, magnitude * y, magnitude * z


def validate_carrier(carrier: CarrierState, phase_steps: int, quantum: int) -> None:
    """Validate the full carrier domain without changing any owner."""
    modulus = _phase_modulus(phase_steps)
    _integer(carrier.family, "family")
    _integer(carrier.number, "number", 1)
    _integer(carrier.phase, "carrier phase", 0, modulus - 1)
    _momentum(carrier.momentum)
    if carrier.momentum != canonical_momentum(carrier.amount, quantum, carrier.port):
        raise ValueError("reversible detector: noncanonical carrier momentum")


def _contact_inputs(
    carrier: CarrierState,
    material: ContactState,
    port_map: tuple[int, ...],
    phase_steps: int,
    quantum: int,
) -> None:
    validate_carrier(carrier, phase_steps, quantum)
    _integer(material.phase, "material phase", 0, phase_steps - 1)
    _momentum(material.momentum)
    if (
        not isinstance(port_map, tuple)
        or len(port_map) != 6
        or any(type(port) is not int for port in port_map)
        or set(port_map) != set(range(6))
    ):
        raise ValueError("reversible detector: port_map must be a permutation of 0 through 5")


def transduce(
    carrier: CarrierState,
    material: ContactState,
    port_map: tuple[int, ...],
    phase_steps: int,
    quantum: int,
) -> tuple[CarrierState, ContactState]:
    """Scatter one carrier and increment the existing pointer reversibly."""
    _contact_inputs(carrier, material, port_map, phase_steps, quantum)
    port = port_map[carrier.port]
    momentum = canonical_momentum(carrier.amount, quantum, port)
    recoil = tuple(
        _result(checked_work(checked_work(held + incoming) - outgoing))
        for held, incoming, outgoing in zip(
            material.momentum, carrier.momentum, momentum, strict=True
        )
    )
    phase = checked_work(material.phase + carrier.amount) % phase_steps
    return (
        CarrierState(carrier.family, carrier.number, carrier.amount, carrier.phase, port, momentum),
        ContactState(phase, (recoil[0], recoil[1], recoil[2])),
    )


def inverse_transduce(
    carrier: CarrierState,
    material: ContactState,
    port_map: tuple[int, ...],
    phase_steps: int,
    quantum: int,
) -> tuple[CarrierState, ContactState]:
    """Undo one contact using only its physical output and immutable rule."""
    _contact_inputs(carrier, material, port_map, phase_steps, quantum)
    port = port_map.index(carrier.port)
    momentum = canonical_momentum(carrier.amount, quantum, port)
    recoil = tuple(
        _result(checked_work(checked_work(held - incoming) + outgoing))
        for held, incoming, outgoing in zip(
            material.momentum, momentum, carrier.momentum, strict=True
        )
    )
    phase = checked_work(material.phase - carrier.amount) % phase_steps
    return (
        CarrierState(carrier.family, carrier.number, carrier.amount, carrier.phase, port, momentum),
        ContactState(phase, (recoil[0], recoil[1], recoil[2])),
    )


def clock_step(
    age: int, content: int, clock: int, phase_steps: int, phase: int
) -> tuple[int, int]:
    """Advance the material clock, preserving its exact integer reference."""
    modulus = _phase_modulus(phase_steps)
    _integer(age, "age")
    _integer(content, "content", 1)
    _integer(clock, "clock", 1)
    _integer(phase, "material phase", 0, modulus - 1)
    next_age = _result(checked_work(age + 1))
    before = checked_work(age * content) // clock
    after = checked_work(next_age * content) // clock
    turn = checked_work(after - before)
    return next_age, checked_work(phase + turn) % modulus


def pointer_displacement(
    phase: int,
    age: int,
    content: int,
    reference_phase: int,
    clock: int,
    phase_steps: int,
) -> int:
    """Read one physical pointer relative to its fixed local calibration."""
    modulus = _phase_modulus(phase_steps)
    _integer(phase, "material phase", 0, modulus - 1)
    _integer(reference_phase, "reference phase", 0, modulus - 1)
    _integer(age, "age")
    _integer(content, "content", 1)
    _integer(clock, "clock", 1)
    reference = checked_work(age * content) // clock
    return checked_work(checked_work(phase - reference_phase) - reference) % modulus
