"""Read-only countdown projections for deadline-based host execution.

The pending absolute deadline is authoritative. Observation derives remaining
time without visiting or mutating waiting Nodes on every physical tick.
"""

from collections.abc import Mapping
from dataclasses import replace
from types import MappingProxyType

from event_universe.core.disturbance_state import Address3, NodeView


def projected_nodes(nodes: Mapping[Address3, NodeView], tick: int) -> Mapping[Address3, NodeView]:
    return MappingProxyType(
        {
            position: replace(
                node,
                delay_counts=(0 if node.pending is None else max(0, node.pending.ready_tick - tick),)
                * 6,
            )
            for position, node in nodes.items()
        }
    )


def projected_snapshot(snapshot: dict[str, object], tick: int) -> dict[str, object]:
    nodes = snapshot["nodes"]
    assert isinstance(nodes, list)
    for node in nodes:
        assert isinstance(node, dict)
        deadline = node["waiting_until"]
        assert deadline is None or isinstance(deadline, int)
        node["delay_counts"] = (0 if deadline is None else max(0, deadline - tick),) * 6
    return snapshot
