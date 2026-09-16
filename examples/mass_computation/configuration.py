"""Author explicit ordinary-engine inputs for the frozen mass-clock candidate."""

from __future__ import annotations

import json
from pathlib import Path

from event_universe.core.disturbance_state import OPERATIONS

HERE = Path(__file__).resolve().parent
SOURCE = (2, 3, 3)
RECEIVER = (3, 3, 3)
DIRECTIONS = ((1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1))


def expectations() -> dict:
    return json.loads((HERE / "expectations.json").read_text(encoding="utf-8"))


def probe(position: tuple[int, int, int], direction: tuple[int, int, int]) -> dict:
    return {
        "position": list(position),
        "type": "probe",
        "values": {"direction": list(direction)},
    }


def document(name: str) -> dict:
    """Build a fixture from immutable family data, without supplying observed answers."""
    expected = expectations()["cases"][name]
    raw = {
        "schema_version": 1,
        "model_id": "mass-clock-ray-v1",
        "shape": [9, 7, 7],
        "boundary": "open",
        "slots_per_node": 8,
        "link_ticks": 1,
        "normal_budget": 1_000_000,
        "ticks": 25 if name == "L1" else 10,
        "operation_costs": {operation: 1 for operation in OPERATIONS},
        "computation_field": "computation",
        "output_clock": {"gain": expected["coupling"]},
        "fields": [
            {
                "name": "mass",
                "components": 1,
                "units": "configured mass property",
                "signed": False,
                "conserved": True,
                "extensive": True,
            },
            {
                "name": "computation",
                "components": 1,
                "units": "computation token; no physical energy assignment",
                "signed": False,
                "conserved": True,
                "extensive": True,
            },
            {
                "name": "probe_token",
                "components": 1,
                "units": "probe identity unit",
                "signed": False,
                "conserved": True,
                "extensive": True,
            },
            {
                "name": "direction",
                "components": 3,
                "units": "configured lattice direction",
                "signed": True,
                "conserved": False,
                "extensive": False,
            },
        ],
        "disturbance_types": [
            {
                "name": "held_source",
                "fields": ["mass", "computation"],
                "defaults": {"mass": expected["mass"], "computation": expected["reserve"]},
                "transport": {"mode": "hold"},
            },
            {
                "name": "probe",
                "fields": ["probe_token", "direction"],
                "defaults": {"probe_token": 1, "direction": [1, 0, 0]},
                "transport": {"mode": "move", "direction_field": "direction"},
            },
        ],
        "spatial_fields": [
            {
                "field": "computation",
                "baseline": 0,
                "transport": "ray",
                "headings": [[1, 0, 0]],
                "rays_per_tick": 1,
                "ray_slots": 16,
            }
        ],
        "emissions": [
            {
                "type": "held_source",
                "field": "computation",
                "amount": {"field": "mass"},
                "denominator": 1,
                "source": False,
                "interval": 8,
                "first_tick": 0,
                "whole_pulse": True,
            }
        ],
        "seeds": [{"position": list(SOURCE), "type": "held_source"}],
    }
    if name in {"C1", "C2"}:
        # The ordinary probe reaches the receiving Node through actual Links.
        # Its release time is not an external scheduled physical input.
        ready = expected["probe_ready_tick"]
        raw["seeds"].append(probe((RECEIVER[0], RECEIVER[1] + ready, RECEIVER[2]), (0, -1, 0)))
    elif name == "P6":
        raw["seeds"].extend(probe(SOURCE, direction) for direction in DIRECTIONS)
    elif name == "P2":
        raw["seeds"].append(probe(SOURCE, (0, 1, 0)))
        raw["seeds"].append(probe((SOURCE[0], SOURCE[1] + 1, SOURCE[2]), (0, -1, 0)))
    return raw
