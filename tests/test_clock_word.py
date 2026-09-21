"""Series S, the clock's word: the presence or the age moment
(`examples/events/clock_word/`, docs/designs/clock_age/NOTE.md section 6).
The expected values of docs/TEST_EXPECTATIONS.md ("The clock's word"),
written down first, from the physicist's pin and the map's section B:

(a) the shipped worlds equal `make_worlds.worlds()` document for document,
    parse under the law and run ten intervals with the books balanced; the
    detector is number 1 at x = 110 reading `age`, the lamp number 2 at
    x = 10 fixed with a lamp on +x, its `mass` entry `pass` (the presence
    word) or `{"rule": "pass", "reads": "age"}` (the age word), the two
    `mass` sources numbers 3 and 4 at 3 or 6 Links on +y and +z with
    F = 4915 per interval (the amount F x 2^16) on the fan of nine toward
    the lamp's line; the bar 121 x 9 x 9 at 3 Links and 121 x 15 x 15 at
    6; `expectations.json` declares the format, the two windows and the
    four worlds with the pinned k = 0.300, 0.300, 1.650, 3.150 and
    1 + z = 1.300, 1.300, 2.650, 4.150;
(b) the count the lamp's clock owes per self-creation once the crowd's rows
    dwell at its Node (after twelve intervals): the presence 4 F = 19660 at
    both distances under both words; the age moment 22 F = 108130 at 3
    Links and 42 F = 206430 at 6 under the age word; the first interval at
    which the lamp's count is not zero is tick 6 at 3 Links and tick 11 at
    6 (the first row's age 5 and 10 at that Link on the heading), and at
    that interval the count is the first row's alone (2 F under the
    presence word, 2 F x 5 or 2 F x 10 under the age word);
(c) the algebra of the pin, no world's numbers: k = (count per F) x F / 2^16,
    the ratio of the two k at the same F is 1 under the presence word and
    42 / 22 = 1.909 under the age word, against the continuum's potential
    2.000 at the same push.
"""

from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

from event_universe.events import NatureBeamSimulation
from event_universe.world_loading import load_world

ROOT = Path(__file__).resolve().parents[1]
WORLDS = ROOT / "examples" / "events" / "clock_word"
NAMES = ("presence_3", "presence_6", "age_3", "age_6")
LAMP = 2
F = 4915


def load_generator():
    path = WORLDS / "make_worlds.py"
    spec = importlib.util.spec_from_file_location("clock_word_make_worlds", path)
    module = importlib.util.module_from_spec(spec)
    sys.modules["clock_word_make_worlds"] = module
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
    for name, document in generated.items():
        path = WORLDS / f"{name}.json"
        assert json.loads(path.read_text(encoding="utf-8")) == document, name
        word, distance, side = generator.WORLDS[name]
        centre = side // 2
        detector, lamp, *sources = document["measured"]
        assert document["shape"] == [121, side, side]
        assert detector["position"] == [110, centre, centre]
        assert detector["table"]["s_px1"] == {"rule": "measure", "reads": "age"}
        assert lamp["position"] == [10, centre, centre] and lamp["fixed"]
        assert lamp["lamp"]["directions"] == [[1, 0, 0]]
        expected_entry = {"rule": "pass"} if word == "presence" else {"rule": "pass", "reads": "age"}
        assert lamp["table"]["mass"] == expected_entry
        assert [s["position"] for s in sources] == [
            [10, centre + distance, centre],
            [10, centre, centre + distance],
        ]
        for source in sources:
            assert source["amount"] == F * 65536 and source["fixed"]
            assert len(source["directions"]) == 9
        sim = simulation(name)
        for _ in range(10):
            sim.step()
        assert sim.books()["balanced"], name
    expected = json.loads((WORLDS / "expectations.json").read_text(encoding="utf-8"))
    assert expected["format"] == generator.EXPECTATIONS_FORMAT
    assert expected["windows"] == [[200, 350], [350, 500]]
    assert expected["flux"] == F
    assert [round(expected["worlds"][n]["k"], 3) for n in NAMES] == [0.3, 0.3, 1.65, 3.15]
    assert [round(expected["worlds"][n]["one_plus_z"], 3) for n in NAMES] == [1.3, 1.3, 2.65, 4.15]
    assert "replicated" not in expected


def test_the_lamps_count_under_each_word_at_each_distance():
    """(b)."""
    expected_count = {"presence_3": 4 * F, "presence_6": 4 * F, "age_3": 22 * F, "age_6": 42 * F}
    first_tick = {"presence_3": 6, "presence_6": 11, "age_3": 6, "age_6": 11}
    first_count = {"presence_3": 2 * F, "presence_6": 2 * F, "age_3": 2 * F * 5, "age_6": 2 * F * 10}
    for name in NAMES:
        sim = simulation(name)
        first = None
        for tick in range(1, 13):
            sim.step()
            counted = sim.measured[LAMP].counted
            if first is None and counted:
                first = (tick, counted)
        assert sim.measured[LAMP].presence == 4 * F, name
        assert sim.measured[LAMP].counted == expected_count[name], name
        assert first == (first_tick[name], first_count[name]), (name, first)


def test_the_algebra_of_the_pin():
    """(c)."""
    generator = load_generator()
    assert abs(generator.pinned_k("presence", 3) - 4 * F / 65536) < 1e-12
    assert abs(generator.pinned_k("age", 6) - 42 * F / 65536) < 1e-12
    ratios = generator.expectations()["ratios"]
    assert ratios["presence"]["k_6_over_k_3"] == 1.0
    assert abs(ratios["age"]["k_6_over_k_3"] - 42 / 22) < 1e-12
    assert round(ratios["age"]["k_6_over_k_3"], 3) == 1.909
    assert ratios["age"]["continuum"] == 2.0
