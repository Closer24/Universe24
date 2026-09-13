"""Independent exact expectations for the opt-in generic particle contracts."""

import json
from copy import deepcopy
from fractions import Fraction
from pathlib import Path

import pytest

from event_universe import Simulation
from event_universe.core.disturbance_state import MAX_VALUE, CostMeter, OperationCosts
from event_universe.fields.ratios import Ratio, project
from event_universe.fields.routing import balanced_port, rate_credit
from event_universe.initialization import parse_initial_state

HERE = Path(__file__).resolve().parents[1] / "examples/particle-contracts"


def meter():
    return CostMeter(OperationCosts((1,) * 9))


def load(name):
    return json.loads((HERE / (name + ".json")).read_text(encoding="utf-8"))


def bodies(world):
    snap = world.snapshot()
    return [r["values"] for c in snap["nodes"] for r in c["disturbances"]] + [
        r["values"] for r in snap["transfers"]
    ]


def momentum(values):
    return tuple(
        Fraction(w) + Fraction(r, values["denominator"][0])
        for w, r in zip(values["whole"], values["remainder"], strict=True)
    )


def totals(world):
    records = bodies(world)
    p = tuple(sum(momentum(v)[i] for v in records) for i in range(3))
    kinetic = sum(sum(x * x for x in momentum(v)) / (2 * v["mass"][0]) for v in records)
    return p, kinetic


def test_balanced_prefixes_scale_changes_and_large_weights():
    def ports(weights, count):
        counts, previous, result = (0,) * 6, (0,) * 6, []
        for _ in range(count):
            port, counts, previous = balanced_port(weights, counts, previous, meter())
            result.append(port)
        return result

    assert ports((1, 0, 1, 0, 0, 0), 60) == ports((1000, 0, 1000, 0, 0, 0), 60) == [0, 2] * 30
    assert ports((2, 0, 1, 0, 0, 0), 3) == [0, 2, 0]
    assert ports((1000, 0, 999, 0, 0, 0), 4) == [0, 2, 0, 2]
    assert ports((MAX_VALUE, 0, MAX_VALUE, 0, 0, 0), 4) == [0, 2, 0, 2]
    port, counts, weights = balanced_port(
        (0, 1, 0, 0, 0, 0), (1, 0, 0, 0, 0, 0), (1, 0, 1, 0, 0, 0), meter()
    )
    assert (port, counts, weights) == (1, (0, 1, 0, 0, 0, 0), (0, 1, 0, 0, 0, 0))


def test_fractional_clock_keeps_credit_across_denominator_change():
    move, n, d = rate_credit(0, 1, 1, 3, meter())
    assert (move, n, d) == (False, 1, 3)
    move, n, d = rate_credit(n, d, 1, 2, meter())
    assert (move, n, d) == (False, 5, 6)
    assert rate_credit(n, d, 1, 2, meter()) == (True, 1, 3)
    with pytest.raises(ValueError, match="bound"):
        rate_credit(1, MAX_VALUE, 1, MAX_VALUE - 1, meter())


def test_ratio_mixed_projection_exactness_and_fixed_bounds():
    values = (Ratio(-7, 3), Ratio(1, 2), Ratio(0))
    assert project("rational_whole", values) == (-2, 0, 0)
    assert project("rational_remainder", values) == (-2, 3, 0)
    assert project("rational_denominator", values) == (6,)
    assert Ratio(1 << 100, 3).mul(Ratio(3, 1 << 100)) == Ratio(1)
    with pytest.raises(OverflowError):
        Ratio(1 << 127)
    with pytest.raises(ValueError, match="nonzero"):
        Ratio(1, 0)
    with pytest.raises(OverflowError):
        Ratio((1 << 127) - 1).mul(Ratio((1 << 127) - 1))


@pytest.mark.parametrize("name", ["electron-positron", "electron-proton", "proton-neutron"])
def test_fractional_elastic_contact_preserves_decoded_values_every_tick(name):
    raw = load(name)
    world = Simulation(parse_initial_state(raw))
    initial = totals(world)
    first, second = bodies(world)
    m1, m2 = first["mass"][0], second["mass"][0]
    u1, u2 = momentum(first)[0] / m1, momentum(second)[0] / m2
    # Independent center-of-mass reflection, rather than the configured expanded formula.
    center = (m1 * u1 + m2 * u2) / (m1 + m2)
    expected = (m1 * (2 * center - u1), m2 * (2 * center - u2))
    world.step()
    assert tuple(momentum(v)[0] for v in bodies(world)) == expected
    for _ in range(179):
        world.step()
        assert totals(world) == initial
        assert all(
            all(0 < code for code in record.route_count_codes)
            for node in world.nodes.values()
            for record in node.records
            if record is not None
        )


def test_bad_denominator_rejects_all_carrier_assignments():
    raw = load("electron-proton")
    raw["interactions"][0]["assignments"][-1]["expression"] = {
        "op": "rational_denominator",
        "args": [{"op": "ratio", "args": [1, 0]}],
    }
    world = Simulation(parse_initial_state(raw))
    before = deepcopy(bodies(world))
    with pytest.raises(ValueError, match="nonzero"):
        world.step()
    assert bodies(world) == before


@pytest.mark.parametrize(
    "name,expected", [("massless-axis", [50, 0, 0]), ("massless-oblique", [30, 40, 0])]
)
def test_massless_mass_shell_and_common_half_speed(name, expected):
    raw = load(name)
    steps = [0, 0, 0]

    def observe(e):
        if e["event"] == "sent":
            steps[e["port"] // 2] += 1 if e["port"] % 2 == 0 else -1

    world = Simulation(parse_initial_state(raw), observer=observe)
    for _ in range(100):
        world.step()
        for v in bodies(world):
            assert sum(x * x for x in momentum(v)) == 4 * v["energy"][0] ** 2
    assert steps == expected
    invalid = deepcopy(raw)
    invalid["disturbance_types"][0]["defaults"]["energy"] = 4
    world = Simulation(parse_initial_state(invalid))
    with pytest.raises(ValueError, match="mass_shell"):
        world.step()


def test_joint_energy_and_momentum_reservoir_including_transit():
    raw = load("energy-reservoir")
    raw["link_ticks"] = 2
    world = Simulation(parse_initial_state(raw))
    for _ in range(12):
        world.step()
        p, k = totals(world)
        node = world.spatial_values((8, 8, 8))
        assert k + node["reservoir"]["value"][0] == 14
        assert tuple(p[i] + node["reaction"]["value"][i] for i in range(3)) == (4, 0, 0)
    raw["spatial_seeds"][0]["populations"][0] = 4
    world = Simulation(parse_initial_state(raw))
    before = deepcopy(bodies(world))
    stock = world.spatial_values((8, 8, 8))
    with pytest.raises(ValueError, match="negative"):
        world.step()
    assert bodies(world) == before
    assert world.spatial_values((8, 8, 8)) == stock


def test_rational_regions_are_explicit_and_representation_cannot_split():
    raw = load("electron-proton")
    raw["disturbance_types"][0]["transport"]["rate"] = {"op": "ratio", "args": [1, 2]}
    with pytest.raises(ValueError, match="explicit rational"):
        parse_initial_state(raw)
    raw = load("electron-proton")
    raw["disturbance_types"][0]["transport"] = {"mode": "split"}
    with pytest.raises(ValueError, match="extensive"):
        parse_initial_state(raw)


def test_local_check_rejects_quiescent_zero_record():
    raw = load("massless-axis")
    kind = raw["disturbance_types"][0]
    kind["transport"] = {"mode": "hold"}
    kind["defaults"] = {
        name: [0] * len(value) if isinstance(value, list) else 0
        for name, value in kind["defaults"].items()
    }
    kind["checks"] = [
        {"name": "positive_mass", "expression": {"op": "gt", "args": [{"field": "mass"}, 0]}}
    ]
    world = Simulation(parse_initial_state(raw))
    with pytest.raises(ValueError, match="positive_mass"):
        world.step()


@pytest.mark.parametrize("scale", [1, 1000, MAX_VALUE])
def test_balanced_json_weights_preserve_world_prefix(scale):
    raw = load("massless-axis")
    raw["disturbance_types"][0]["transport"] = {
        "mode": "move",
        "routing": "balanced",
        "weights": [scale, 0, scale, 0, 0, 0],
    }
    sent = []
    world = Simulation(
        parse_initial_state(raw),
        observer=lambda e: sent.append(e["port"]) if e["event"] == "sent" else None,
    )
    for _ in range(60):
        world.step()
    assert sent == [0, 2] * 30


def test_rational_keys_cannot_nest_or_enter_regular_arithmetic():
    key = {"op": "rational_key", "args": [1]}
    for expression in [
        {"op": "rational_key", "args": [key]},
        {"op": "sum", "args": [key]},
    ]:
        raw = load("electron-proton")
        raw["interactions"][0]["invariants"][0]["expression"] = expression
        with pytest.raises(ValueError, match="top-level invariant"):
            parse_initial_state(raw)
    raw = load("electron-proton")
    raw["disturbance_types"][0]["transport"]["rate"] = key
    with pytest.raises(ValueError, match="top-level invariant"):
        parse_initial_state(raw)
