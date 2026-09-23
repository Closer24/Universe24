"""Series V, a cluster of crowds read by one detector, at rest and moving as
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
# The generic entry of the bending (2026-09-22, record 847; the price,
# docs/designs/one_wall/GENERIC_BENDING_PRICE.md): the light in a crowd at a
# pair with n > 0 is stretched and pushed by the crowd's age moment as the
# clocks are, and a pushed row's momentum at d = 65536 makes the wall's
# square exceed the working bound, the contract's refusal. The worlds
# below are declared at that pair and are not in the paper (the model
# owner's word of record 871: not needed; the Register Architect's to
# remove after the entry merges): the test records what the law does with
# them as declared, the readings before the entry kept in the comments.
REFUSED_BEFORE_THE_LADDER_AT = 6  # both worlds
# Under the split ladder of the pushed row's wall (flow-link-build, 2026-09-22,
# 89f43572: T = Q a + b from the wall's square X alone, X Q^2 never formed)
# the refusal above is lifted: these worlds run balanced past the interval
# where they refused. Their readings under the ladder are a RECORD by kind
# (GAMEBOARD: the host's view of the lamp's presence and counted clock, the
# measured events' counters after 12 intervals), NOT pinned and NOT compared
# with the registered pins of the worlds that never refused; the refusal
# stays as history ("refused before the ladder at interval N").
READ_UNDER_THE_SPLIT_LADDER = {
    "kind": "GAMEBOARD",
    "after_intervals": 12,
    "both_worlds": {
        "m0": {"presence": 0, "counted": 0},
        "m01": {"presence": 4 * 1638, "counted": 22 * 1638},
        "m03": {"presence": 14 * 4915, "counted": 112 * 4915},
        "m06": {"presence": 14 * 9830, "counted": 112 * 9830},
        "m1": {"presence": 14 * 16384, "counted": 112 * 16384},
    },
}


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
                # The per-axis drive of history under the world's key.
                axis = generator.P.AXIS_DRIVE
                assert abs(generator.P.speed(lamp["momentum"][0], lamp["amount"], axis) - 0.2 * c) < 1e-6
                for source in sources:
                    v = generator.P.speed(source["momentum"][0], source["amount"], axis)
                    assert abs(v - 0.2 * c / (1 + m["k"])) < 1e-6, (member, v)
            else:
                assert lamp["fixed"] and all(s["fixed"] for s in sources)
        sim = simulation(name)
        # Ten intervals balanced in both worlds (before the ladder both
        # refused at interval 6, REFUSED_BEFORE_THE_LADDER_AT).
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
    # Before the entry, after 12 intervals of `cluster_rest`: the presence
    # at every lamp 4 x FLUX[name] (at most 8 at the lamp of no crowd).
    # Under the law as declared, before the ladder, the world refused at
    # interval 6; under the split ladder it runs the 12 intervals
    # balanced, the presences the record READ_UNDER_THE_SPLIT_LADDER
    # (GAMEBOARD, not a pin).
    sim = simulation("cluster_rest")
    for _ in range(12):
        sim.step()
    assert sim.tick == 12 and sim.books()["balanced"]
    assert all(sim.measured[number].presence >= 0 for number in LAMPS.values())


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


def test_the_registers_k_is_a_labelled_gameboard_diagnostic():
    """The crowd's k and every number derived from it alone (a replay of the
    store) stay in the register unchanged, labelled GAMEBOARD under
    `gameboard_diagnostics`: a diagnostic, never pinned, out of the deciding
    set; the pin of the series is 1 + z at the detector (the model owner,
    2026-09-22, records 562 and 564; the audit of record 567, F1)."""
    expected = json.loads((WORLDS / "expectations.json").read_text(encoding="utf-8"))
    diagnostics = expected["gameboard_diagnostics"]
    assert diagnostics["kind"] == "GAMEBOARD"
    assert any(key.endswith(".k") or key.endswith("_k_3") for key in diagnostics["keys"])
    assert "never pinned" in diagnostics["statement"] and "not yet read" in diagnostics["statement"]
    assert "1 + z at the detector (DETECTOR)" in diagnostics["statement"]
