"""Inspect supported contact outcomes without claiming emergent trajectories.

The three controls share all physical laws and differ only in prescribed random
tickets. They establish supported sequences, not typical ensemble frequencies.
Localized output is held by the input and retains explicitly unknown momentum.
"""

import json
import time
from copy import deepcopy
from pathlib import Path

from event_universe import Simulation
from event_universe.configuration_validation import prepare_initialization, validate_configuration

EXAMPLE = Path(__file__).resolve().with_name("repeated_contacts.json")
TICKS = 96


def _run_control(base, name, tickets, expected_capture_tick, expected_draws, expected_source):
    raw = deepcopy(base)
    raw["ticks"] = TICKS
    raw["event_program"]["tickets"] = tickets
    prepared = prepare_initialization(raw)
    samples = []
    with Simulation(prepared.initial) as world:
        for _ in range(TICKS):
            world.step()
            assert world.totals()["charge"] == (-1,)
            assert world.totals()["mass"] == (1,)
            assert all(item["balanced"] for item in world.spatial_accounting().values())
            for node in world.snapshot()["nodes"]:
                for record in node["disturbances"]:
                    if record["type"] == "localized_charge":
                        assert tuple(node["position"]) == (2, 1, 1)
                        assert record["values"]["momentum_known"] == (0,)
                        samples.append(
                            {
                                "audit_tick": world.tick,
                                "position": list(node["position"]),
                                "momentum_known": list(record["values"]["momentum_known"]),
                            }
                        )
        resolver = world.computation_report()["resolver"]
        transfers = resolver["contact_transfers"]
        captures = [item for item in transfers if item["direction"] == "to_localized"]
        assert resolver["random_draws"] == expected_draws
        if expected_capture_tick is None:
            assert not captures and not samples
            assert sum(item["direction"] == "continued" for item in transfers) == 31
            assert resolver["quantum_inventory"]["charge"] == (-1,)
            assert resolver["quantum_inventory"]["mass"] == (1,)
        else:
            assert [item["tick"] for item in captures] == [expected_capture_tick]
            assert [sample["audit_tick"] for sample in samples] == list(
                range(expected_capture_tick + 1, TICKS + 1)
            )
            assert resolver["quantum_inventory"]["charge"] == (0,)
            assert resolver["quantum_inventory"]["mass"] == (0,)
        accounting = world.spatial_accounting()
        assert accounting["electric_signal"]["current"] == (0,)
        assert accounting["electric_signal"]["sources"] == (expected_source,)
        assert accounting["electric_signal"]["dissipated"] == (expected_source,)
        return {
            "name": name,
            "audit_ticks": TICKS,
            "prescribed_tickets": tickets,
            "capture_event_tick": expected_capture_tick,
            "random_draws": resolver["random_draws"],
            "contact_transfers": transfers,
            "localized_samples": samples,
            "localized_sample_count": len(samples),
            "final_totals": world.totals(),
            "quantum_inventory": resolver["quantum_inventory"],
            "spatial_accounting": accounting,
            "conserved_at_every_completed_tick": True,
            "field_accounting_balanced_at_every_completed_tick": True,
        }


def _moving_capture_rejection(base):
    raw = deepcopy(base)
    raw["fields"].append(
        {
            "name": "heading",
            "components": 3,
            "units": "direction",
            "signed": True,
            "conserved": False,
            "extensive": False,
        }
    )
    for kind in raw["disturbance_types"][:2]:
        kind["fields"].append("heading")
        kind["defaults"]["heading"] = [1, 0, 0]
    raw["disturbance_types"][1]["transport"] = {"mode": "move", "direction_field": "heading"}
    report = validate_configuration(json.dumps(raw))
    expected = "localized capture must retain undefined momentum and hold until a local rule acts"
    assert not report.valid
    assert [issue.message for issue in report.issues] == [expected]
    return report.to_dict()


def run_trajectory_controls():
    """Return measured finite controls and a negative existing-schema check."""
    base = json.loads(EXAMPLE.read_text(encoding="utf-8"))
    started = time.perf_counter()
    cases = [
        _run_control(base, "early_localization", [0], 3, 1, -18),
        _run_control(
            base,
            "repeated_then_localization",
            base["event_program"]["tickets"],
            24,
            8,
            -36,
        ),
        _run_control(base, "continued_contacts", [25] * 40, None, 31, -42),
    ]
    return {
        "numerical_checks": "pass",
        "kind": "controlled_outcome_support",
        "input": "examples/quantum/repeated_contacts.json",
        "laws_and_geometry_identical_between_cases": True,
        "cases": cases,
        "moving_capture_rejection": _moving_capture_rejection(base),
        "elapsed_seconds": time.perf_counter() - started,
        "classical_trajectory_emergence": "not_established",
        "limits": [
            "Prescribed tickets test supported sequences, not typical ensemble frequencies.",
            "Localized endpoints are held by configuration and retain unknown momentum.",
            "A stationary record does not establish a derived classical equation of motion.",
            "This is an outcome control, not an environment-strength sweep.",
            "Source/dissipation balance and single inventory do not establish physical energy closure.",
        ],
    }
