"""Read-only run acceptance checks; never repair a physical result."""

from event_universe.core.state import Vector


class InertialMotionViolation(RuntimeError):
    """An isolated particle changed momentum without an external influence."""


def require_inertial_momentum(expected: Vector, actual: Vector, *, pid: int, tick: int) -> None:
    """Reject any momentum change, including a single integer unit.

    The caller must establish that the particle is isolated and no external field
    was initialized. This does not identify self-fields in a multi-particle world.
    """
    if actual != expected:
        raise InertialMotionViolation(
            f"Isolated particle {pid} changed momentum at tick {tick}: "
            f"expected {expected}, actual {actual}. Run rejected; state was not repaired."
        )
