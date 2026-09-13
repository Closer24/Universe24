"""The configured pulse response behaves like q(E + v x B); the formula lives in JSON only.

Variants of examples/local_lorentz_field.json check the structure of the
supplied law without any physical name in the engine: sign follows charge,
magnitude is linear in charge, the magnetic part flips with velocity and is
perpendicular to both v and B, a neutral probe is untouched, combined carrier
plus reservoir momentum is exact, and a free electron meeting the pulse is
deflected by exactly the supplied impulse.
"""

import copy
import json
from pathlib import Path

import pytest

from event_universe import Simulation
from event_universe.initialization import parse_initial_state

BASE = json.loads(
    (Path(__file__).resolve().parents[1] / "examples" / "local_lorentz_field.json").read_text(
        encoding="utf-8"
    )
)
ELECTRON, PROTON, NEUTRON = (5, 1, 1), (5, 3, 1), (5, 5, 1)


def variant(
    *, keep=("electric", "magnetic"), magnetic=None, electric=None, momentum_sign=1, charge_scale=1
):
    doc = copy.deepcopy(BASE)
    doc["spatial_seeds"] = [s for s in doc["spatial_seeds"] if s["field"] in keep]
    for seed in doc["spatial_seeds"]:
        if seed["field"] == "magnetic" and magnetic is not None:
            seed["populations"] = [list(magnetic)] + [[0, 0, 0]] * 7
        if seed["field"] == "electric" and electric is not None:
            seed["populations"] = [list(electric)] + [[0, 0, 0]] * 7
    for kind in doc["disturbance_types"]:
        kind["defaults"]["momentum"] = [momentum_sign * kind["defaults"]["mass"], 0, 0]
        kind["defaults"]["charge"] = charge_scale * kind["defaults"]["charge"]
    return doc


def impulses(doc):
    world = Simulation(parse_initial_state(doc))
    start = {
        r.type_index: world.record_values(r)["momentum"]
        for n in world.nodes.values()
        for r in n.records
        if r
    }
    before = world.totals()["momentum"]
    for _ in range(doc["ticks"]):
        world.step()
    result = {}
    for position, node in world.nodes.items():
        for record in node.records:
            if record is not None:
                momentum = world.record_values(record)["momentum"]
                result[position] = tuple(
                    a - b for a, b in zip(momentum, start[record.type_index], strict=True)
                )
    assert world.totals()["momentum"] == before
    return result


def test_sign_follows_charge_and_the_neutral_probe_is_untouched():
    delta = impulses(variant())
    assert delta[ELECTRON] == (0, 100000, 0)
    assert delta[PROTON] == (0, -100000, 0)
    assert delta[NEUTRON] == (0, 0, 0)


def test_electric_part_is_linear_in_charge_and_independent_of_mass():
    single = impulses(variant(keep=("electric",)))
    double = impulses(variant(keep=("electric",), charge_scale=2))
    assert single[ELECTRON] == (0, -200000, 0) and single[PROTON] == (0, 200000, 0)
    assert double[ELECTRON] == (0, -400000, 0) and double[PROTON] == (0, 400000, 0)


def test_magnetic_part_flips_with_velocity_and_is_perpendicular_to_v_and_b():
    forward = impulses(variant(keep=("magnetic",)))
    backward = impulses(variant(keep=("magnetic",), momentum_sign=-1))
    assert forward[ELECTRON] == (0, 300000, 0) and forward[PROTON] == (0, -300000, 0)
    assert backward[ELECTRON] == (0, -300000, 0) and backward[PROTON] == (0, 300000, 0)
    rotated = impulses(variant(keep=("magnetic",), magnetic=(0, 300000, 0)))
    assert rotated[ELECTRON] == (0, 0, -300000) and rotated[PROTON] == (0, 0, 300000)


def test_electric_part_follows_the_field_direction():
    delta = impulses(variant(keep=("electric",), electric=(0, 0, 200000)))
    assert delta[ELECTRON] == (0, 0, -200000) and delta[PROTON] == (0, 0, 200000)


def test_free_electron_meeting_the_pulse_is_deflected_by_the_supplied_impulse():
    doc = variant(momentum_sign=-1)
    doc["disturbance_types"][0]["transport"] = {
        "mode": "move",
        "direction_field": "momentum",
        "routing": "balanced",
        "rate": 1,
        "rate_denominator": 1,
    }
    doc["seeds"] = [s for s in doc["seeds"] if s["type"] == "electron"]
    doc["spatial_seeds"] = [s for s in doc["spatial_seeds"] if s["position"][1] == 1]
    doc["ticks"] = 8
    events = []
    world = Simulation(parse_initial_state(doc), observer=events.append)
    for _ in range(doc["ticks"]):
        world.step()
    path = [
        (e["tick"], tuple(e["position"]), tuple(e["values"]["momentum"]))
        for e in events
        if e.get("event") == "received" and e.get("disturbance") == "electron"
    ]
    assert path[:2] == [(1, (4, 1, 1), (-100000, 0, 0)), (2, (3, 1, 1), (-100000, 0, 0))]
    assert path[2][2] == (-100000, -500000, 0)
    later = [p for _, p, _ in path[2:]]
    assert all(m == (-100000, -500000, 0) for _, _, m in path[2:])
    assert sum(1 for p in later if p[0] == 3) >= 1 and later[-1][1] != 1
    assert world.totals()["momentum"] == (-100000, 0, 0)


@pytest.mark.parametrize(
    "name", ["lorentz", "coulomb", "maxwell", "electron", "proton", "electric", "magnetic"]
)
def test_engine_sources_carry_no_physical_name_branch(name):
    root = Path(__file__).resolve().parents[1] / "src" / "event_universe"
    offenders = []
    for path in (
        list((root / "core").glob("*.py"))
        + list((root / "fields").glob("*.py"))
        + [root / "initialization.py"]
    ):
        text = path.read_text(encoding="utf-8").lower()
        if f'"{name}"' in text or f"'{name}'" in text:
            offenders.append(path.name)
    assert offenders == []
