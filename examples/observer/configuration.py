"""Build translated local-reception experiments using existing generic laws.

This is initialization data, not a Maxwell model or an optical eye model. Two
conserved spatial pulses cross the selected node from different directions. A
whole record arrives later carrying arbitrary raw scalar/vector quantities.
The held phase toggle is a local process; counting its completed cycles supplies
the observer's clock without relabeling host ticks as measured time.

The default nine- and fifteen-node cubes have identical initial neighborhoods.
All three incoming paths stay inside either open domain. No source identities,
remote coordinates or global history are carried in the physical payloads.
"""

import argparse
import json
from pathlib import Path

from event_universe.core.disturbance_state import OPERATIONS, bounded
from event_universe.initialization import parse_initial_state

MODEL_ID = "observer-transport-demo-v1"
LINK_TICKS = 2
DEFAULT_TICKS = 8
DEFAULT_NORMAL_BUDGET = 8


def observer_position(size: int) -> tuple[int, int, int]:
    """Return the common translation origin with room for all incoming paths."""
    if type(size) is not int or size < 9 or size % 2 == 0:
        raise ValueError("size must be an odd integer of at least nine")
    bounded(size)
    return (size // 2,) * 3


def _inventory(field: str, port: int) -> dict[str, object]:
    return {
        "name": f"{field}_owned_total",
        "expression": {
            "op": "add",
            "args": [{"field": field, "side": "right"}, {"outgoing": field, "port": port}],
        },
    }


def _spatial_seed(position: list[int], field: str, value: int | list[int]) -> dict[str, object]:
    return {
        "position": position,
        "field": field,
        "populations": (
            [value, *[[0] * len(value) for _ in range(7)]]
            if isinstance(value, list)
            else [value, *[0 for _ in range(7)]]
        ),
    }


def build_configuration(
    size: int = 9,
    *,
    ticks: int = DEFAULT_TICKS,
    normal_budget: int = DEFAULT_NORMAL_BUDGET,
) -> dict[str, object]:
    """Build a small open world with strictly local whole-stock forwarding.

    Default analytic forecast, to verify against recorded events: scalar field
    receipt at host tick 4 from -X; vector field receipt at 6 from +Y;
    moving record receipt at 8 from +Z. Their travel directions are +X, -Y
    and -Z respectively. Each field hop takes two ticks. The
    record's five-unit initial and six-unit received cycle costs fit budget 8.

    The phase update alone costs seven units and initially commits at ticks 0
    and 2. At tick 4, existing field work also prices the next local cycle, so
    its completion is delayed. With this five-field schema the expected field
    cost is 281, giving a frozen combined cost of 288 and a commit at tick 74.
    This is a schedule forecast, not a substitute for recording the actual run.
    Arriving information remains locally available
    while the frozen cycle waits. The moving record continues only when this
    cell can process it; arrival does not promise immediate onward departure.
    Other budgets deliberately change carrier/clock timing, not field transit.
    """
    center = observer_position(size)
    for name, value, minimum in (("ticks", ticks, 0), ("normal_budget", normal_budget, 1)):
        if type(value) is not int or value < minimum:
            raise ValueError(f"{name} must be an integer of at least {minimum}")
        bounded(value)
    x, y, z = center
    return {
        "schema_version": 1,
        "model_id": MODEL_ID,
        "observer": {"position": list(center), "max_receipts": 100000},
        "shape": [size, size, size],
        "boundary": "open",
        "slots_per_cell": 2,
        "link_ticks": LINK_TICKS,
        "normal_budget": normal_budget,
        "ticks": ticks,
        "operation_costs": dict.fromkeys(OPERATIONS, 1),
        "fields": [
            {
                "name": "pulse_inventory",
                "components": 1,
                "units": "raw inventory unit",
                "signed": False,
                "conserved": True,
            },
            {
                "name": "pulse_vector",
                "components": 3,
                "units": "raw signed vector unit",
                "signed": True,
                "conserved": True,
            },
            {
                "name": "phase",
                "components": 1,
                "units": "local toggle state",
                "signed": False,
                "conserved": False,
                "extensive": False,
            },
            {
                "name": "message_inventory",
                "components": 1,
                "units": "raw inventory unit",
                "signed": False,
                "conserved": True,
            },
            {
                "name": "message_vector",
                "components": 3,
                "units": "raw signed vector unit",
                "signed": True,
                "conserved": True,
            },
        ],
        "disturbance_types": [
            {
                "name": "held_clock",
                "fields": ["phase"],
                "defaults": {"phase": 1},
                "transport": {"mode": "hold"},
                "updates": [
                    {
                        "field": "phase",
                        "expression": {"op": "sub", "args": [1, {"field": "phase"}]},
                    }
                ],
            },
            {
                "name": "passing_message",
                "fields": ["message_inventory", "message_vector"],
                "defaults": {"message_inventory": 11, "message_vector": [2, -3, 1]},
                "transport": {"mode": "move", "weights": [0, 0, 0, 0, 0, 1]},
            },
        ],
        "seeds": [
            {"position": list(center), "type": "held_clock"},
            {"position": [x, y, z + 4], "type": "passing_message"},
        ],
        "spatial_fields": [
            {"field": "pulse_inventory", "baseline": 0, "transport": "local"},
            {"field": "pulse_vector", "baseline": [0, 0, 0], "transport": "local"},
        ],
        "spatial_seeds": [
            _spatial_seed([x - 2, y, z], "pulse_inventory", 7),
            _spatial_seed([x, y + 3, z], "pulse_vector", [3, -2, 1]),
        ],
        "field_rules": [
            {
                "name": "forward_owned_stock_through_selected_links",
                "assignments": [
                    {"field": "pulse_inventory", "expression": 0},
                    {
                        "field": "pulse_inventory",
                        "port": 0,
                        "expression": {"field": "pulse_inventory", "side": "right"},
                    },
                    {"field": "pulse_vector", "expression": [0, 0, 0]},
                    {
                        "field": "pulse_vector",
                        "port": 3,
                        "expression": {"field": "pulse_vector", "side": "right"},
                    },
                ],
                "invariants": [_inventory("pulse_inventory", 0), _inventory("pulse_vector", 3)],
            }
        ],
    }


def main() -> None:
    """Write validated run inputs into a new or empty directory without running."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--size", type=int, default=9, help="Odd cube size, at least nine")
    parser.add_argument("--output", type=Path, required=True, help="New or empty output directory")
    args = parser.parse_args()
    try:
        initialization = build_configuration(args.size)
        parse_initial_state(initialization)
    except ValueError as error:
        parser.error(str(error))
    documents = {
        "initialization.json": initialization,
    }
    if args.output.exists() and (not args.output.is_dir() or any(args.output.iterdir())):
        parser.error("output must be a new or empty directory; existing inputs are not overwritten")
    args.output.mkdir(parents=True, exist_ok=True)
    for name, document in documents.items():
        with (args.output / name).open("x", encoding="utf-8") as output:
            output.write(json.dumps(document, indent=2) + "\n")


if __name__ == "__main__":
    main()
