"""Passive projection of private input, channel and retained owners."""

from collections.abc import Iterable

from ..core.disturbance_state import unpack
from ..core.private_register import PrivateKey
from ..core.private_worklist import PrivateSimulation


def frame(world: PrivateSimulation, detectors: Iterable[PrivateKey] = ()) -> dict[str, object]:
    """Keep ordinary lattice Nodes; expose Register addresses only as readouts."""
    nodes: list[dict[str, object]] = []

    def append(key: PrivateKey, kind: str, codes: tuple[int, ...]) -> None:
        nodes.append(
            {
                "position": key.node,
                "waiting_until": None,
                "disturbances": [
                    {
                        "type": kind,
                        "values": {"components": unpack(codes)},
                        "register": [key.from_port, key.to_port],
                    }
                ],
            }
        )

    for key in sorted(detectors):
        append(key, "detector_binding", ())
    for key, datum in sorted(world.transport.inputs.items()):
        append(key, "opaque_token", datum.codes)
    for address, node in sorted(world.nodes.items()):
        for pair, unit in zip(node.pairs, node.units, strict=True):
            if unit.state.codes:
                append(PrivateKey(address, *pair), "retained_token", unit.state.codes)
    transfers = []
    for source, packet in sorted(world.transport.channels.items()):
        offset = world.wiring.channels[source].offset
        axis = next(axis for axis, value in enumerate(offset) if value)
        transfers.append(
            {
                "origin": source.node,
                "target": packet.target.node,
                "port": 2 * axis + (0 if offset[axis] == 1 else 1),
                "arrival_tick": packet.due_tick,
                "type": "opaque_token",
                "values": {"components": unpack(packet.datum.codes)},
                "source_register": [source.from_port, source.to_port],
                "target_register": [packet.target.from_port, packet.target.to_port],
            }
        )
    return {"tick": world.tick, "boundary": "periodic", "nodes": nodes, "transfers": transfers}
