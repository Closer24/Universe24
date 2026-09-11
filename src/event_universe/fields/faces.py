"""Pure response inputs from six locally delivered, source-facing field values.

The order is +x, -x, +y, -y, +z, -z. A positive-axis face points toward
the neighbor that supplied its value, not the packet's travel direction.
Transport and causal delivery are caller contracts; this module reads no world.
"""

from event_universe.core.state import Neighbors, Vector, checked, checked_work

FaceValues = Neighbors


def delivered_faces(incoming: FaceValues) -> FaceValues:
    """Preserve the canonical source-facing orientation after validating it."""
    if len(incoming) != 6:
        raise ValueError("exactly six delivered face values are required")
    for value in incoming:
        checked(value)
    return incoming


def scalar_broadcast(value: int) -> FaceValues:
    """Publish one bounded scalar snapshot on each of the six outgoing faces."""
    checked(value)
    return value, value, value, value, value, value


def face_imbalance(incoming: FaceValues) -> Vector:
    """Return opposite-face differences with bounded signed inputs and work.

    Nonnegative populations are a transport policy, not a restriction on this
    generic calculation. A difference may exceed one physical register and is
    therefore a working value for the shared bounded impulse accumulator.
    """
    if len(incoming) != 6:
        raise ValueError("exactly six delivered face values are required")
    for value in incoming:
        checked(value)
    return (
        checked_work(incoming[0] - incoming[1]),
        checked_work(incoming[2] - incoming[3]),
        checked_work(incoming[4] - incoming[5]),
    )
