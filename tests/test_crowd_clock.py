"""Series P, a lamp inside a crowd, still and moving
(`examples/events/crowd_clock/`, docs/designs/crowd_clock/DESIGN.md). The
expected values of docs/TEST_EXPECTATIONS.md ("A lamp inside a crowd"),
written down first:

(a) the shipped worlds equal `make_worlds.worlds()` document for document,
    parse under the law and run ten intervals with the books balanced; the
    five still worlds hold the lamp (`s_px1`, number 2) at x = 10 and its
    two `mass` sources fixed three Links away on +y and +z, the three
    moving worlds throw the three together at 0.2 c along +x (the speed by
    the drive's rule within 1e-6); `expectations.json` declares the
    generator's format, the two window pairs and the eight worlds with
    their pinned k = 4 F / 2^16 (0.005, 0.08, 0.3, 1, 2 still; 0.08, 0.3, 1
    moving);
(b) the presence at the still lamp's Node once the crowd's rows arrive
    (after the twelfth interval of `still_005`) is 4 F = 328, and the
    lamp's clock owes accordingly: in `still_1` (k = 1) the lamp births
    once in two intervals between the twentieth and the hundredth (40
    births, within 2);
(c) the derivation's algebra, no world's numbers: 1 + z =
    (1 + k)(1 + v / c) reaches z = 1 only with a slowed clock for v < c
    (1 + v / c < 2 for every v below c), a still lamp at k = 1 reads z = 1
    and at k = 2 reads z = 2; the lag of a slowed lamp behind its unslowed
    crowd is k v t / (1 + k) and the exit from a fan of reach 4 comes at
    4 (1 + k) / (k v), 69 intervals for k = 1 at 0.2 c.
"""

from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

from event_universe.events import NatureBeamSimulation
from event_universe.world_loading import load_world

ROOT = Path(__file__).resolve().parents[1]
WORLDS = ROOT / "examples" / "events" / "crowd_clock"
STILL = ("still_005", "still_08", "still_3", "still_1", "still_2")
MOVING = ("moving_08", "moving_3", "moving_1")
LAMP = 2


def load_generator():
    path = WORLDS / "make_worlds.py"
    spec = importlib.util.spec_from_file_location("crowd_clock_make_worlds", path)
    module = importlib.util.module_from_spec(spec)
    sys.modules["crowd_clock_make_worlds"] = module
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
    assert set(generated) == set(STILL) | set(MOVING)
    c = generator.C
    for name, document in generated.items():
        path = WORLDS / f"{name}.json"
        assert json.loads(path.read_text(encoding="utf-8")) == document, name
        moving = name in MOVING
        lamp, sources = document["measured"][1], document["measured"][2:]
        assert lamp["family"] == "s_px1" and lamp["lamp"]["directions"] == [[-1 if moving else 1, 0, 0]]
        assert [s["position"] for s in sources] == [
            [lamp["position"][0], 7, 4],
            [lamp["position"][0], 4, 7],
        ]
        if moving:
            for body in (lamp, *sources):
                assert "fixed" not in body
                v = generator.speed(body["momentum"][0], body["amount"])
                assert abs(v - 0.2 * c) < 1e-6, (name, v)
        else:
            assert lamp["position"][0] == 10
            assert all(body["fixed"] for body in (lamp, *sources))
        sim = simulation(name)
        for _ in range(10):
            sim.step()
        assert sim.books()["balanced"], name
    expected = json.loads((WORLDS / "expectations.json").read_text(encoding="utf-8"))
    assert expected["format"] == generator.EXPECTATIONS_FORMAT
    assert expected["still_windows"] == [[200, 350], [350, 500]]
    assert expected["moving_windows"] == [[100, 250], [250, 400]]
    assert set(expected["worlds"]) == set(generated)
    pinned = {name: round(expected["worlds"][name]["k"], 4) for name in expected["worlds"]}
    assert pinned == {
        "still_005": 0.005,
        "still_08": 0.08,
        "still_3": 0.3,
        "still_1": 1.0,
        "still_2": 2.0,
        "moving_08": 0.08,
        "moving_3": 0.3,
        "moving_1": 1.0,
    }
    for name in STILL:
        assert expected["worlds"][name]["flux"] * 4 / 65536 == expected["worlds"][name]["k"]


def test_the_presence_at_the_lamp_is_four_times_the_flux_and_the_clock_owes_it():
    """(b)."""
    sim = simulation("still_005")
    for _ in range(12):
        sim.step()
    lamp = sim.measured[LAMP]
    assert lamp.presence == 4 * 82 == 328
    births: list[int] = []
    sim = NatureBeamSimulation(
        load_world(
            (WORLDS / "still_1.json").read_bytes(), base_dir=WORLDS, root=WORLDS.parent
        ).world,
        lambda e: births.append(e["tick"])
        if e["event"] == "birth" and e.get("measured") == LAMP
        else None,
    )
    for _ in range(100):
        sim.step()
    assert sim.measured[LAMP].presence == 4 * 16384
    inside = sum(1 for t in births if 20 <= t < 100)
    assert abs(inside - 40) <= 2, inside


def test_the_algebra_of_the_crowds_clock():
    """(c)."""
    generator = load_generator()
    c = generator.C
    for v_over_c in (0.2, 0.5, 0.9, 0.999):
        assert 1 + v_over_c < 2
    assert (1 + 1) * (1 + 0) == 2.0
    assert (1 + 2) * (1 + 0) == 3.0
    assert abs(generator.pinned_k(16384) - 1.0) < 1e-12
    assert abs(generator.pinned_k(32768) - 2.0) < 1e-12
    v = 0.2 * c
    assert abs(generator.lag(1.0, 100) - v * 100 / 2) < 1e-9
    assert abs(generator.exit_tick(1.0) - 8 / v) < 1e-9
    assert round(generator.exit_tick(1.0)) == 69
    assert generator.exit_tick(0.3) > generator.exit_tick(1.0)
