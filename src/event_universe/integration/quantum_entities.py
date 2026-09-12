"""Compile finite quantum-mode entity profiles into the ordinary Simulation.

This authoring adapter reads explicit register data, never dispatches by species,
and delegates all dynamics to the shared event program. Mode labels describe a
chosen finite sector; they do not derive a particle's Hamiltonian or statistics.
"""

from collections.abc import Sequence
from typing import Any

from event_universe.core.disturbance_state import OPERATIONS
from event_universe.initialization import _array, _integer, _object, _text, parse_initial_state

from .event_program import parse_event_program


def compile_quantum_entities(
    indexed: dict[str, dict[str, Any]],
    entity_ids: Sequence[str],
    *,
    shape: tuple[int, int, int],
    ticks: int,
    link_ticks: int,
) -> dict[str, Any]:
    """Build a held, unmeasured local-mode preparation; callers add explicit laws.

    All selected modes are colocated in this preparation fixture. No classical
    particle is copied into the register world. A dummy unoccupied carrier type
    satisfies the shared schema but supplies no physical record or hidden force.
    """
    addresses: list[list[int]] = []
    dimensions: list[int] = []
    levels: list[int] = []
    names: list[str] = []
    center = [n // 2 for n in shape]
    for identity in entity_ids:
        if identity not in indexed:
            raise ValueError(f"unknown entity: {identity}")
        profile = _object(
            indexed[identity].get("quantum_profile"),
            "quantum profile",
            {"claim_level", "assumptions", "registers", "missing_dynamics"},
            {"claim_level", "assumptions", "registers", "missing_dynamics"},
        )
        if profile["claim_level"] != "finite_mode_representation":
            raise ValueError("quantum profiles must declare finite_mode_representation")
        for key in ("assumptions", "missing_dynamics"):
            for item in _array(profile[key], key, 16, 1):
                _text(item, key)
        seen: set[str] = set()
        for raw in _array(profile["registers"], "registers", 30, 1):
            register = _object(
                raw,
                "register",
                {"name", "basis", "initial_level", "interpretation"},
                {"name", "basis", "initial_level", "interpretation"},
            )
            name = _text(register["name"], "register name")
            if name in seen:
                raise ValueError("duplicate register name in entity profile")
            seen.add(name)
            basis = tuple(
                _text(label, "basis label") for label in _array(register["basis"], "basis", 4, 2)
            )
            if len(set(basis)) != len(basis):
                raise ValueError("basis labels must be distinct")
            level = _integer(register["initial_level"], "initial_level", 0)
            if level >= len(basis):
                raise ValueError("initial level outside the declared basis")
            _text(register["interpretation"], "mode interpretation")
            names.append(identity + ":" + name)
            dimensions.append(len(basis))
            levels.append(level)
            addresses.append(center.copy())
    program: dict[str, Any] = {
        "model": "local-quantum-events-v2",
        "capacity": 10000,
        "addresses": addresses,
        "dimensions": dimensions,
        "initial_levels": levels,
        "register_names": names,
        "layers": [],
        "bindings": [],
    }
    result: dict[str, Any] = {
        "schema_version": 1,
        "model_id": "catalog-finite-quantum-modes-v1",
        "shape": list(shape),
        "boundary": "open",
        "slots_per_cell": 1,
        "link_ticks": link_ticks,
        "normal_budget": 10000,
        "ticks": ticks,
        "operation_costs": dict.fromkeys(OPERATIONS, 1),
        "fields": [
            {
                "name": "record",
                "components": 1,
                "units": "unobserved placeholder",
                "signed": False,
                "conserved": False,
                "extensive": False,
            }
        ],
        "disturbance_types": [
            {"name": "unoccupied recorder", "fields": ["record"], "transport": {"mode": "hold"}}
        ],
        "seeds": [],
        "event_program": program,
    }
    initial = parse_initial_state(result)
    parse_event_program(initial)
    return result
