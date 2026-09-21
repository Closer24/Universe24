"""Series S, a reader inside a crowd (`examples/events/reader_clock/`,
docs/designs/reader_clock/DESIGN.md). The expected values of
docs/TEST_EXPECTATIONS.md ("A reader inside a crowd"), written down first:

(a) the shipped worlds equal `make_worlds.worlds()` document for document,
    parse under the law and run ten intervals with the books balanced; the
    reader is number 1 at x = 10 (fixed, a lamp on -x, measuring `s_px1`
    with `reads: "age"`), the source number 2 at x = 70 (a lamp on -x,
    passing `s_px1`); the crowds' fluxes are F = k 2^16 / 4 (0, 16384,
    32768 / 2 = 8192 for k = 0, 1, 0.5); in `alike_receding` the source's
    momentum is that of 0.2 c and its sources' that of 0.1 c by the drive's
    rule within 1e-6; `expectations.json` declares the format, the window
    [250, 500] and the pinned readings in the two clocks;
(b) after twelve intervals of `alike` the presence at the reader and at the
    source is 4 x 16384 each, and of `reader_half` 4 x 8192 at the reader
    and 4 x 16384 at the source;
(c) the algebra: (1 + k_s)(1 + v / c) / (1 + k_r) is 0.5 for k_r = 1 and
    k_s = 0 at rest, 1 for k_r = k_s, 4 / 3 for k_r = 0.5 and k_s = 1, and
    (1 + k_s + v / c) / (1 + k_r) is 1.1 for k_r = k_s = 1 at 0.2 c; the
    clicks per reader birth are (1 + k_r) / (1 + k_s)(1 + v / c).
"""

from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

from event_universe.events import NatureBeamSimulation
from event_universe.world_loading import load_world

ROOT = Path(__file__).resolve().parents[1]
WORLDS = ROOT / "examples" / "events" / "reader_clock"
NAMES = ("control", "reader_dense", "alike", "reader_half", "alike_receding")


def load_generator():
    path = WORLDS / "make_worlds.py"
    spec = importlib.util.spec_from_file_location("reader_clock_make_worlds", path)
    module = importlib.util.module_from_spec(spec)
    sys.modules["reader_clock_make_worlds"] = module
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
    assert set(generated) == set(NAMES)
    c = generator.C
    for name, document in generated.items():
        path = WORLDS / f"{name}.json"
        assert json.loads(path.read_text(encoding="utf-8")) == document, name
        reader, source = document["measured"][0], document["measured"][1]
        assert reader["position"] == [10, 4, 4] and reader["fixed"]
        assert reader["table"]["s_px1"] == {"rule": "measure", "reads": "age"}
        assert reader["lamp"]["directions"] == [[-1, 0, 0]]
        assert source["position"] == [70, 4, 4] and source["table"]["s_px1"] == {"rule": "pass"}
        k_r, k_s, moving = generator.WORLDS[name]
        crowds = document["measured"][2:]
        assert len(crowds) == 2 * ((k_r > 0) + (k_s > 0))
        for body in crowds:
            assert body["amount"] == generator.flux(k_r if body["position"][0] == 10 else k_s) * 65536
        if moving:
            assert abs(generator.P.speed(source["momentum"][0], source["amount"]) - 0.2 * c) < 1e-6
            for body in crowds:
                if body["position"][0] == 70:
                    v = generator.P.speed(body["momentum"][0], body["amount"])
                    assert abs(v - 0.1 * c) < 1e-6
        else:
            assert source["fixed"]
        sim = simulation(name)
        for _ in range(10):
            sim.step()
        assert sim.books()["balanced"], name
    assert generator.flux(1.0) == 16384 and generator.flux(0.5) == 8192 and generator.flux(0.0) == 0
    expected = json.loads((WORLDS / "expectations.json").read_text(encoding="utf-8"))
    assert expected["format"] == generator.EXPECTATIONS_FORMAT
    assert expected["window"] == [250, 500]
    readers = {n: round(expected["worlds"][n]["one_plus_z_readers_clock"], 3) for n in NAMES}
    assert readers == {
        "control": 2.0,
        "reader_dense": 0.5,
        "alike": 1.0,
        "reader_half": 1.333,
        "alike_receding": 1.1,
    }
    lattice = {n: round(expected["worlds"][n]["one_plus_z_lattice"], 3) for n in NAMES}
    assert lattice == {
        "control": 2.0,
        "reader_dense": 1.0,
        "alike": 2.0,
        "reader_half": 2.0,
        "alike_receding": 2.2,
    }


def test_the_presence_at_the_reader_and_the_source():
    """(b)."""
    sim = simulation("alike")
    for _ in range(12):
        sim.step()
    assert sim.measured[1].presence == 4 * 16384
    assert sim.measured[2].presence == 4 * 16384
    sim = simulation("reader_half")
    for _ in range(12):
        sim.step()
    assert sim.measured[1].presence == 4 * 8192
    assert sim.measured[2].presence == 4 * 16384


def test_the_algebra_of_the_ratio():
    """(c)."""

    def ratio(k_r, k_s, v=0.0, alike=False):
        top = (1 + k_s + v) if alike else (1 + k_s) * (1 + v)
        return top / (1 + k_r)

    assert ratio(1.0, 0.0) == 0.5
    assert ratio(1.0, 1.0) == 1.0
    assert abs(ratio(0.5, 1.0) - 4 / 3) < 1e-12
    assert abs(ratio(1.0, 1.0, 0.2, alike=True) - 1.1) < 1e-12
    assert abs((1 + 1.0) / ((1 + 0.0) * 1.0) - 2.0) < 1e-12
