"""Read directional-mode observables without advancing or repairing a world."""


def add(left, right):
    return tuple(a + b for a, b in zip(left, right, strict=True))


def cross(left, right):
    x, y, z = left
    a, b, c = right
    return (y * c - z * b, z * a - x * c, x * b - y * a)


def measure(snapshot, channels):
    """Count resident stock and actual in-flight owners once; arrivals are views."""
    ports = [(1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)]
    if (
        len(channels) != 6
        or {c["port"] for c in channels} != set(range(6))
        or len({c["field"] for c in channels}) != 6
        or any(tuple(c["direction"]) != ports[c["port"]] for c in channels)
    ):
        raise ValueError("channel metadata must identify six distinct physical ports")
    energy = 0
    momentum = (0, 0, 0)
    nodes = []
    transfers = []

    def quantities(amplitude, direction):
        if sum(a * n for a, n in zip(amplitude, direction, strict=True)) != 0:
            raise ValueError("longitudinal mode is outside this candidate")
        squared = sum(value * value for value in amplitude)
        return squared, tuple(squared * n for n in direction)

    for node in snapshot["spatial_fields"]:
        electric = magnetic = local_momentum = (0, 0, 0)
        local_energy = 0
        modes = []
        for channel in channels:
            state = node["fields"][channel["field"]]
            if any(state["baseline"]):
                raise ValueError("candidate observables require zero baselines")
            amplitude = tuple(state["value"])
            direction = tuple(channel["direction"])
            squared, contribution = quantities(amplitude, direction)
            local_energy += squared
            local_momentum = add(local_momentum, contribution)
            electric = add(electric, amplitude)
            magnetic = add(magnetic, cross(direction, amplitude))
            if squared:
                modes.append({"field": channel["field"], "direction": direction, "amplitude": amplitude})
        energy += local_energy
        momentum = add(momentum, local_momentum)
        if local_energy:
            nodes.append(
                {
                    "position": node["position"],
                    "electric": electric,
                    "magnetic": magnetic,
                    "energy": local_energy,
                    "momentum": local_momentum,
                    "modes": modes,
                }
            )
    for packet in snapshot["spatial_transfers"]:
        packet_energy = 0
        packet_momentum = electric = magnetic = (0, 0, 0)
        modes = []
        for channel in channels:
            amplitude = tuple(sum(v[i] for v in packet["fields"][channel["field"]]) for i in range(3))
            if any(amplitude) and packet["port"] != channel["port"]:
                raise ValueError("mode traveled on a different physical port")
            squared, contribution = quantities(amplitude, channel["direction"])
            energy += squared
            momentum = add(momentum, contribution)
            packet_energy += squared
            packet_momentum = add(packet_momentum, contribution)
            electric = add(electric, amplitude)
            magnetic = add(magnetic, cross(channel["direction"], amplitude))
            if squared:
                modes.append(
                    {
                        "field": channel["field"],
                        "direction": channel["direction"],
                        "amplitude": amplitude,
                    }
                )
        if packet_energy:
            transfers.append(
                {
                    "origin": packet["origin"],
                    "target": packet["target"],
                    "port": packet["port"],
                    "arrival_tick": packet["arrival_tick"],
                    "energy": packet_energy,
                    "momentum": packet_momentum,
                    "electric": electric,
                    "magnetic": magnetic,
                    "modes": modes,
                }
            )
    return {
        "tick": snapshot["tick"],
        "energy": energy,
        "momentum": momentum,
        "nodes": nodes,
        "transfers": transfers,
    }
