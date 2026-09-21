"""Series Q, a cluster of crowds read by one detector, at rest and moving as
one (`examples/events/cluster_clock/`, docs/designs/cluster_clock/DESIGN.md).
The expected values of docs/TEST_EXPECTATIONS.md ("A cluster of crowds"),
written down first:

(a) the shipped worlds equal `make_worlds.worlds()` document for document,
    parse under the law and run ten intervals with the books balanced; the
    detector is number 1 at x = 3, the five lamps (`s_px1`) are numbers 2,
    3, 6, 9, 12 at x = 40, 60, 80, 100, 120 with two `mass` sources each
    but the first, at F = 0, 1638, 4915, 9830, 16384 (k = 4 F / 2^16 = 0,
    0.1, 0.3, 0.6, 1); at rest every body is fixed; moving, every lamp's
    momentum is that of 0.2 c and each member's sources' that of
    0.2 c / (1 + k) by the drive's rule, within 1e-6; `expectations.json`
    declares the format, the window [250, 500], the members' numbers and
    the pinned readings;
(b) after twelve intervals of `cluster_rest` the presence at every lamp of a
    crowd is 4 F (6552, 19660, 39320, 65536) and the bare lamp's is at most
    8 (the other lamps' light passing);
(c) the algebra, no world's numbers: for a crowd slowed alike the reading is
    1 + k + v / c ((1 + k)(1 + (v / (1 + k)) / c) exactly), for a lamp
    behind an unslowed crowd (1 + k)(1 + v / c); the two differ by
    k v / c, 0.2 at k = 1 and v = 0.2 c; the dispersion of the five k is
    0.363 and their mean 0.4.
"""

from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

from event_universe.events import NatureBeamSimulation
from event_universe.world_loading import load_world

ROOT = Path(__file__).resolve().parents[1]
WORLDS = ROOT / "examples" / "events" / "cluster_clock"
LAMPS = {"m0": 2, "m01": 3, "m03": 6, "m06": 9, "m1": 12}
FLUX = {"m0": 0, "m01": 1638, "m03": 4915, "m06": 9830, "m1": 16384}


def load_generator():
    path = WORLDS / "make_worlds.py"
    spec = importlib.util.spec_from_file_location("cluster_clock_make_worlds", path)
    module = importlib.util.module_from_spec(spec)
    sys.modules["cluster_clock_make_worlds"] = module
    spec.loader.exec_module(module)
    return module


def simulation(name: str) -> NatureBeamSimulation:
    path = WORLDS / f"{name}.json"
    loaded = load_world(path.read_bytes(), base_dir=path.parent, root=WORLDS.parent)
    return NatureBeamSimulation(loaded.world)


def test_the_shipped_worlds_are_the_generators_and_run_balanced():
    """(a)."""
    generator = load_generator()
    generated = generator.worlds()
    assert set(generated) == {"cluster_rest", "cluster_moving"}
    c = generator.C
    numbers = generator.numbers()
    assert {name: m["lamp"] for name, m in numbers.items()} == LAMPS
    assert {name: m["flux"] for name, m in numbers.items()} == FLUX
    for name, document in generated.items():
        path = WORLDS / f"{name}.json"
        assert json.loads(path.read_text(encoding="utf-8")) == document, name
        moving = name == "cluster_moving"
        measured = document["measured"]
        assert measured[0]["position"] == [3, 4, 4] and measured[0]["fixed"]
        for member, m in numbers.items():
            lamp = measured[m["lamp"] - 1]
            assert lamp["family"] == "s_px1" and lamp["position"][0] == m["x"]
            sources = [measured[n - 1] for n in m["sources"]]
            assert len(sources) == (2 if m["flux"] else 0)
            if moving:
                assert abs(generator.P.speed(lamp["momentum"][0], lamp["amount"]) - 0.2 * c) < 1e-6
                for source in sources:
                    v = generator.P.speed(source["momentum"][0], source["amount"])
                    assert abs(v - 0.2 * c / (1 + m["k"])) < 1e-6, (member, v)
            else:
                assert lamp["fixed"] and all(s["fixed"] for s in sources)
        sim = simulation(name)
        for _ in range(10):
            sim.step()
        assert sim.books()["balanced"], name
    expected = json.loads((WORLDS / "expectations.json").read_text(encoding="utf-8"))
    assert expected["format"] == generator.EXPECTATIONS_FORMAT
    assert expected["window"] == [250, 500]
    assert {name: m["lamp"] for name, m in expected["members"].items()} == LAMPS
    rest = expected["cluster_rest"]["members"]
    assert [round(rest[n]["one_plus_z"], 3) for n in LAMPS] == [1.0, 1.1, 1.3, 1.6, 2.0]
    moving = expected["cluster_moving"]["members"]
    assert [round(moving[n]["one_plus_z_additive"], 3) for n in LAMPS] == [1.2, 1.3, 1.5, 1.8, 2.2]
    assert [round(moving[n]["one_plus_z_product"], 3) for n in LAMPS] == [1.2, 1.32, 1.56, 1.92, 2.4]


def test_the_presence_at_every_lamp_is_four_times_its_crowds_flux():
    """(b)."""
    sim = simulation("cluster_rest")
    for _ in range(12):
        sim.step()
    for name, number in LAMPS.items():
        presence = sim.measured[number].presence
        if FLUX[name]:
            assert presence == 4 * FLUX[name], (name, presence)
        else:
            assert presence <= 8, presence


def test_the_algebra_of_the_sum_against_the_product():
    """(c)."""
    generator = load_generator()
    v = 0.2
    for k in (0.0, 0.1, 0.3, 0.6, 1.0):
        alike = (1 + k) * (1 + v / (1 + k))
        assert abs(alike - (1 + k + v)) < 1e-12
        assert abs((1 + k) * (1 + v) - alike - k * v) < 1e-12
    assert abs((1 + 1.0) * (1 + v) - (1 + 1.0 + v) - 0.2) < 1e-12
    expected = generator.expectations()["cluster_rest"]
    assert abs(expected["z_mean"] - 0.4) < 1e-12
    assert abs(expected["z_dispersion"] - 0.363) < 5e-4
