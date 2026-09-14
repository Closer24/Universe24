"""Directional radiation quanta scattered by a charge: the wave pays for the carrier's momentum.

The configuration in examples/radiation-scattering/build.py holds part of the
+X quantum stream at a charged carrier's node, streams the rest, and in the next
carrier phase turns the held quanta into the -X stream while the carrier gains
twice their momentum. Quanta count and carrier-plus-wave momentum are named
invariants of every rule; the engine performs only generic integer operations.
"""

import importlib.util
from pathlib import Path

import pytest

from event_universe import Simulation
from event_universe.initialization import parse_initial_state

SPEC = importlib.util.spec_from_file_location(
    "radiation_scattering_build",
    Path(__file__).resolve().parents[1] / "examples" / "radiation-scattering" / "build.py",
)
build = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(build)


def readout(world, doc):
    snap = world.snapshot()
    stock = {d: {} for d in build.DIRECTIONS}
    held = {}
    for node in snap["spatial_fields"]:
        x = node["position"][0]
        for d in build.DIRECTIONS:
            amount = sum(p[0] for p in node["fields"][f"rad_{d}"]["populations"])
            if amount:
                stock[d][x] = amount
        kept = sum(p[0] for p in node["fields"]["held_px"]["populations"])
        if kept:
            held[x] = kept
    transit = {d: 0 for d in build.DIRECTIONS}
    for packet in snap["spatial_transfers"]:
        for d in build.DIRECTIONS:
            transit[d] += sum(p[0] for p in packet["fields"][f"rad_{d}"])
    carrier = next(
        world.record_values(r)["momentum"]
        for n in world.nodes.values()
        for r in n.records
        if r is not None and doc["disturbance_types"][r.type_index]["name"] == "scatterer"
    )
    quanta = sum(sum(s.values()) for s in stock.values()) + sum(held.values()) + sum(transit.values())
    wave_px = (
        sum(sum(s.values()) * build.UNIT[d][0] for d, s in stock.items())
        + sum(held.values())
        + sum(v * build.UNIT[d][0] for d, v in transit.items())
    )
    return stock, held, carrier, quanta, wave_px


def run(charge, ticks=9):
    doc = build.configuration(charge, ticks=ticks)
    world = Simulation(parse_initial_state(doc))
    frames = [readout(world, doc)]
    for _ in range(ticks):
        world.step()
        frames.append(readout(world, doc))
    return frames


def test_charged_carrier_shadows_the_forward_stream_and_back_scatters_two_per_tick():
    frames = run(-1)
    stock, held, carrier, quanta, wave_px = frames[8]
    assert carrier == (24, 0, 0)
    assert all(v == 8 for x, v in stock["px"].items() if x > build.CARRIER_X)
    assert all(v == 2 for v in stock["mx"].values()) and len(stock["mx"]) == 6
    assert held == {}


def test_quanta_and_carrier_plus_wave_momentum_are_exact_until_the_boundary():
    for _stock, _held, carrier, quanta, wave_px in run(-1):
        assert quanta == 60
        assert wave_px + carrier[0] == 60


def test_neutral_carrier_leaves_the_stream_untouched():
    for stock, held, carrier, _quanta, _wave_px in run(0):
        assert carrier == (0, 0, 0) and held == {} and stock["mx"] == {}
        assert all(v == 10 for v in stock["px"].values())


@pytest.mark.parametrize("charge", [1, -1])
def test_scattering_is_even_in_the_sign_of_charge(charge):
    assert run(charge)[8][2] == (24, 0, 0)


def test_scattering_grows_with_charge_squared_up_to_the_available_stream():
    frames = run(2)
    stock, held, carrier, quanta, wave_px = frames[8]
    assert carrier == (96, 0, 0)
    assert all(v == 2 for x, v in stock["px"].items() if x > build.CARRIER_X)
    assert all(v == 8 for v in stock["mx"].values())


def test_back_scatter_appears_one_interval_after_the_hold():
    frames = run(-1, ticks=4)
    assert frames[2][1] == {build.CARRIER_X: 2} and frames[2][0]["mx"] == {}
    assert frames[3][0]["mx"] == {build.CARRIER_X: 2} and frames[3][2] == (4, 0, 0)
