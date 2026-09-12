"""Check genuine metered vector delay and prohibit force substitutions."""

import importlib.util
from pathlib import Path

from event_universe import Simulation
from event_universe.initialization import parse_initial_state

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "computational_star_audit", ROOT / "examples/computational-star/audit.py"
)
assert SPEC is not None and SPEC.loader is not None
AUDIT = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(AUDIT)


def test_candidate_has_no_force_or_field_dependent_probe_transport():
    cases = AUDIT.configurations()
    for raw in cases.values():
        parse_initial_state(raw)
        assert raw["shape"] == [64, 64, 64]
        assert not any(
            raw.get(k)
            for k in (
                "couplings",
                "interactions",
                "spatial_couplings",
                "spatial_interactions",
                "field_rules",
            )
        )
        for kind in raw["disturbance_types"]:
            assert not kind.get("updates")
            if kind["name"] in AUDIT.PROBES:
                assert kind["transport"]["direction_field"] == "momentum"
                assert kind["transport"] == cases["active"]["disturbance_types"][1]["transport"]
    star = sum(s["values"]["mass"] for s in cases["active"]["seeds"] if s["type"] == "star_constituent")
    assert star / 4 == 315000


def test_vector_packet_adds_delay_without_changing_ports_or_momentum():
    raw = {
        "schema_version": 1,
        "model_id": "vector-processing-delay-probe-v1",
        "shape": [9, 9, 9],
        "boundary": "open",
        "slots_per_cell": 4,
        "link_ticks": 1,
        "normal_budget": 80,
        "ticks": 10,
        "operation_costs": {
            k: 1
            for k in (
                "receive",
                "read",
                "evaluate",
                "update",
                "couple",
                "route",
                "split",
                "send",
                "commit",
            )
        },
        "fields": [
            {"name": n, "components": c, "signed": n != "mass", "conserved": True, "units": "test unit"}
            for n, c in (("mass", 1), ("momentum", 3), ("signal", 3))
        ],
        "disturbance_types": [
            {
                "name": "probe",
                "fields": ["mass", "momentum"],
                "transport": {
                    "mode": "move",
                    "direction_field": "momentum",
                    "rate": 1,
                    "rate_denominator": 4,
                },
            }
        ],
        "spatial_fields": [{"field": "signal", "transport": "outward", "baseline": [0, 0, 0]}],
        "seeds": [
            {"position": [4, 4, 4], "type": "probe", "values": {"mass": 4, "momentum": [1, 0, 0]}}
        ],
    }
    observed = []
    for pulse in (False, True):
        raw["spatial_seeds"] = (
            [{"field": "signal", "position": [3, 4, 4], "populations": [[24, 0, 0]] + [[0, 0, 0]] * 7}]
            if pulse
            else []
        )
        events = []
        world = Simulation(parse_initial_state(raw), observer=events.append)
        for _ in range(10):
            world.step()
            assert world.totals()["mass"] == (4,)
            assert world.totals()["momentum"] == (1, 0, 0)
        sent = [e for e in events if e["event"] == "sent"]
        assert [e["port"] for e in sent] == [0, 0]
        observed.append([e["tick"] for e in sent])
        if pulse:
            cycle = next(e for e in events if e["event"] == "cycle_started" and e["tick"] == 1)
            assert cycle["cost"] == 106
            assert cycle["ready_tick"] == 2
    assert observed == [[3, 7], [4, 8]]
