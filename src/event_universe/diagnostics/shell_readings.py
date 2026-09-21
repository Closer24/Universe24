"""The shell means of the engine's readings: a host diagnostic that reads the
dense per-Node arrays of the last interval (`NatureBeamSimulation.readings`)
and never supplies a physical update. Moved out of the engine class on
2026-09-21 (the architecture audit's item 4, docs/MIGRATION.md): the one
floating-point calculation of the package lives with the other host
diagnostics, and the events package holds integer arithmetic only.
"""

from __future__ import annotations

import numpy as np

from event_universe.core.game_board import Address3
from event_universe.events.engine import NatureBeamSimulation


def shell_readings(
    simulation: NatureBeamSimulation, family: int, centre: Address3, radius: int
) -> dict[str, float]:
    """The shell means at one radius of the last interval's readings: the
    Nodes at Euclidean distance within a half Link of `radius` from the
    centre, their number, the mean count (the amount that arrived per
    Node), the mean radial flow (amount x the arrival's unit vector at
    the scale Q projected on the radial unit vector, summed per Node: Q
    per unit of amount moving radially) and the mean presence (every
    ray at the Node). Read-only: a report of the host in floating point,
    never an input of the law."""
    node_offsets = np.indices(simulation.shape).reshape(3, -1).T - np.array(centre)
    distance = np.sqrt((node_offsets * node_offsets).sum(axis=1))
    chosen = np.abs(distance - radius) < 0.5
    chosen &= distance > 0
    positions = node_offsets[chosen]
    radial = positions / distance[chosen][:, None]
    cells = tuple((positions + np.array(centre)).T)
    arrived = simulation.readings.arrived[family][cells]
    flow = simulation.readings.flow[family][cells]
    presence = simulation.readings.presence[family][cells]
    return {
        "nodes": float(chosen.sum()),
        "arrived": float(arrived.mean()),
        "flow": float((flow * radial).sum(axis=1).mean()),
        "presence": float(presence.mean()),
    }
