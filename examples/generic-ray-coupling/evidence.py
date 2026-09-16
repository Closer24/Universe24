"""Read actual ray owners for research evidence without advancing the world.

The spatial Node owns retained inputs during pending work. Pending proposals
are deliberately not counted a second time. A Link packet owns dispatched rays.
This is an audit over the world, not a local physical law or operational detector.
"""

from dataclasses import asdict


def owned_rays(world):
    """Copy all real resident and Link ray owners, including complete metadata."""
    spatial = world._spatial
    if spatial is None:
        return []
    owners = []

    def append(bundle, location):
        for index, rays in enumerate(bundle):
            definition = world.initial.spatial_fields[index]
            name = world.initial.fields[definition.field].name
            for slot, ray in enumerate(rays):
                owners.append(
                    {
                        **location,
                        "field": name,
                        "slot": slot,
                        "heading_vector": list(definition.headings[ray.heading]),
                        "phase_steps": definition.phase_steps,
                        "ray": asdict(ray),
                    }
                )

    for position, node in sorted(spatial.nodes.items()):
        append(node.rays, {"owner": "node", "position": list(position)})
    for bank in spatial.links.values():
        for packet in bank:
            if packet is not None:
                append(
                    packet.rays,
                    {
                        "owner": "link",
                        "origin": list(packet.origin),
                        "target": spatial._neighbor(packet.origin, packet.port),
                        "port": packet.port,
                        "arrival_tick": packet.arrival_tick,
                    },
                )
    return owners


def capture(world):
    """Copied canonical display state and detailed ray inventory at one tick."""
    return {
        "tick": world.tick,
        "rays": owned_rays(world),
        "snapshot": world.snapshot(),
        "totals": world.totals(),
        "escaped_totals": world.escaped_totals(),
        "source_totals": world.source_totals(),
        "dissipation_totals": world.dissipation_totals(),
        "spatial_accounting": world.spatial_accounting(),
    }


def ray_inventory(frame, field):
    """Independent integer sum over actual owners, without aggregation heuristics."""
    rows = [item for item in frame["rays"] if item["field"] == field]
    return {
        "amount": sum(item["ray"]["amount"] for item in rows),
        "momentum": [
            sum(item["ray"]["amount"] * item["heading_vector"][axis] for item in rows)
            for axis in range(3)
        ],
        "resident_count": sum(item["owner"] == "node" for item in rows),
        "link_count": sum(item["owner"] == "link" for item in rows),
    }


def compare_expected(frames, expected, *, field):
    """Compare preregistered Node/Link counts and phases with recorded facts.

    Expectations are literal independent fixture rows supplied before execution.
    A missing tick or repeated phase is not filled from playback or a model law.
    """
    indexed = {frame["tick"]: frame for frame in frames}
    if len(indexed) != len(frames):
        raise ValueError("Evidence contains duplicate ticks")
    observations = []
    for tick, row in expected.items():
        frame = indexed.get(tick)
        if frame is None:
            observations.append({"tick": tick, "pass": False, "error": "missing tick"})
            continue
        rays = [item for item in frame["rays"] if item["field"] == field]
        measured = {
            **ray_inventory(frame, field),
            "phases": sorted(item["ray"]["phase"] for item in rays),
            "delays": sorted(item["ray"].get("interaction_delay", 0) for item in rays),
        }
        observations.append(
            {
                "tick": tick,
                "expected": row,
                "actual": measured,
                "pass": all(measured[key] == value for key, value in row.items()),
            }
        )
    return {"pass": bool(observations) and all(r["pass"] for r in observations), "rows": observations}
