"""The moving detector, a cart with a click (docs/designs/moving_detector/
DESIGN.md; examples/events/moving_detector/): the shipped worlds equal
their generator's and run balanced with the cart's pace exact, the pins of
`expectations.json` are the design's closed forms, and the world key
`clock_stamp` writes the measured event's own count of self-creations on
every line it writes, nothing without the key, the count falling behind the
tick by the owed count in a crowd.

(a) The six worlds equal the generator's; each loads with `clock_stamp`
    true and the amplitude identity alone; c = 32 / 55; the cart's momentum
    gives the pace exactly (1 / k, or 3 / 7); ten intervals balanced; the
    pins are the closed forms (k_AB = 1 / (1 - beta), k_BA = 1 + beta, the
    ratio 1 - beta^2, the round trip, the radar velocity -v, the hop gaps).
(b) The capability world in-process (120 intervals): every line a measured
    event writes carries `clock`; on the moving cart in no crowd the count
    equals the interval; the ordinals of the lamp's rows it clicks advance
    one per row; its Node changes by at most one per count and by 0 or 1
    between consecutive clicks; the step lines come every five intervals.
(c) The key off: no line carries `clock`, and the record equals the keyed
    record with the field removed (byte identical otherwise); the key must
    be a boolean.
(d) The edge: the same world at the suspension pair [1, 16384] (a crowd of
    the lamp's rows at the cart): the cart's count falls behind the tick by
    what it owes, never exceeds it, and its last click's count is its `age`.
    (Written at [1, 64] before the generic entry of the bending, 2026-09-22;
    under the law as it stands the crowd's push at d = 64 turns every light
    row off the three-Node bar before it reaches the cart, no click and no
    crowd at the cart's Node, so the edge is read at the weak-field pair.)
(e) The birth stamp (the light clock's gate 1, 2026-09-23): under the key
    every `birth` line carries `clock`, the emitting measured event's own
    count at that interval (its `age`, the same field as on its clicks; in
    no crowd the interval), so N(j) = clock(return) - clock(birth) of one
    ordinal is read off the record; the edge is a body's first birth, the
    count 1 (the lamp births at its first self-creation, after the count).
    Without the key no birth line carries it and the record at 60 intervals
    is byte identical to the record before the field (its sha256 pinned).
"""

from __future__ import annotations

import copy
import hashlib
import importlib.util
import json
import sys
from fractions import Fraction
from pathlib import Path

import pytest

from event_universe.events import NatureBeamSimulation
from event_universe.events.run import execute_nature_beam_run
from event_universe.world_loading import load_world

ROOT = Path(__file__).resolve().parents[1]
WORLDS = ROOT / "examples" / "events" / "moving_detector"
ORDINAL_MASK = (1 << 32) - 1
# The sha256 of `events.jsonl` the capability world without `clock_stamp`
# wrote at 60 intervals through `execute_nature_beam_run` on origin/main
# 5783325353789c2167398486e2c7428f4f5fb62b, before the birth line's stamp.
UNKEYED_EVENTS_SHA256 = "1d6c3008871e4555fc298236668d208d51e7062d9a19b6fc6d4abcca616419e5"


def load_generator():
    path = WORLDS / "make_worlds.py"
    spec = importlib.util.spec_from_file_location("moving_detector_make_worlds", path)
    module = importlib.util.module_from_spec(spec)
    sys.modules["moving_detector_make_worlds"] = module
    spec.loader.exec_module(module)
    return module


def run_lines(document: dict, ticks: int) -> tuple[list[dict], NatureBeamSimulation]:
    world = load_world(json.dumps(document).encode("utf-8"), base_dir=WORLDS, root=WORLDS.parent).world
    lines: list[dict] = []
    simulation = NatureBeamSimulation(world, observer=lines.append, keep_row_clicks=True)
    for _ in range(ticks):
        simulation.step()
    assert simulation.books()["balanced"]
    return lines, simulation


def test_the_shipped_worlds_are_the_generators_and_the_pins_are_the_closed_forms():
    """(a)."""
    generator = load_generator()
    assert generator.C == Fraction(32, 55)
    generated = generator.worlds()
    assert set(generated) == {
        "cart_k3",
        "cart_k5",
        "cart_k9",
        "cart_k17",
        "cart_quantum",
        "capability_k5",
    }
    expectations = json.loads((WORLDS / "expectations.json").read_text(encoding="utf-8"))
    assert expectations["format"] == generator.EXPECTATIONS_FORMAT
    # the run blocks the reading tool writes under `runs` stand beside the pins
    assert {k: v for k, v in expectations.items() if k != "runs"} == generator.expectations()
    for name, document in generated.items():
        path = WORLDS / f"{name}.json"
        assert json.loads(path.read_text(encoding="utf-8")) == document, name
        loaded = load_world(path.read_bytes(), base_dir=path.parent, root=WORLDS.parent)
        world = loaded.world
        assert world.clock_stamp is True
        assert world.hypotheses == ["amplitude-v1"]
        carts = [entry for entry in world.measured if not entry.fixed]
        assert len(carts) == 1
        v = generator.WORLDS[name][0]
        assert generator.pace(carts[0].momentum[0]) == v
        simulation = NatureBeamSimulation(world)
        for tick in range(1, 11):
            simulation.step()
            assert simulation.books()["balanced"], (name, tick)
        pins = expectations["worlds"][name]
        beta = v / generator.C
        assert Fraction(pins["beta"]["fraction"]) == beta
        assert Fraction(pins["k_AB"]["fraction"]) == 1 / (1 - beta)
        gaps = pins["least_step"]["counts_between_hops"]["values"]
        assert gaps == ([2, 3] if name == "cart_quantum" else [int(1 / v)])
        if name == "capability_k5":
            assert "k_BA" not in pins
            continue
        assert Fraction(pins["k_BA"]["fraction"]) == 1 + beta
        assert Fraction(pins["ratio_k_BA_over_k_AB"]["fraction"]) == 1 - beta * beta
        assert Fraction(pins["round_trip"]["fraction"]) == (1 + beta) / (1 - beta)
        assert Fraction(pins["radar_velocity"]["fraction"]) == -v
    assert expectations["worlds"]["cart_k5"]["k_AB"]["fraction"] == "32/21"
    assert expectations["worlds"]["cart_k5"]["ratio_k_BA_over_k_AB"]["fraction"] == "903/1024"
    assert expectations["worlds"]["cart_k3"]["windows"]["round_trip_and_radar"]["from_count"] == 153
    assert expectations["worlds"]["cart_quantum"]["windows"]["round_trip_and_radar"]["from_count"] == 248


def test_the_clock_stamp_on_the_moving_cart_in_no_crowd():
    """(b)."""
    document = json.loads((WORLDS / "capability_k5.json").read_text(encoding="utf-8"))
    lines, simulation = run_lines(document, 120)
    # The lines a measured event writes at its table, its face and its lamp
    # (the birth line since the light clock's gate 1, (e)).
    stamped = [
        line
        for line in lines
        if line.get("measured") is not None
        and line["event"] in ("click", "read", "rerelease", "become", "birth")
    ]
    assert stamped and all("clock" in line for line in stamped)
    assert all("clock" not in line for line in lines if line.get("measured") is None)
    assert all("clock" not in line for line in lines if line["event"] in ("record", "split"))
    cart = next(number for number, entry in simulation.measured.items() if not entry.fixed)
    clicks = [line for line in lines if line["event"] == "click" and line.get("measured") == cart]
    assert len(clicks) > 40
    assert all(line["clock"] == line["tick"] for line in clicks)
    ordinals = [line["record"] & ORDINAL_MASK for line in clicks]
    assert ordinals == list(range(ordinals[0], ordinals[0] + len(ordinals)))
    for before, after in zip(clicks, clicks[1:], strict=False):
        delta_node = after["node"][0] - before["node"][0]
        delta_count = after["clock"] - before["clock"]
        assert delta_node in (0, 1) and abs(delta_node) <= delta_count
    steps = [line["tick"] for line in lines if line["event"] == "step"]
    assert steps == list(range(5, 121, 5))
    assert simulation.measured[cart].age == 120


def test_the_key_off_writes_nothing_and_must_be_a_boolean():
    """(c)."""
    document = json.loads((WORLDS / "capability_k5.json").read_text(encoding="utf-8"))
    keyed, _ = run_lines(document, 60)
    off = copy.deepcopy(document)
    off["clock_stamp"] = False
    unkeyed, _ = run_lines(off, 60)
    assert all("clock" not in line for line in unkeyed)
    stripped = [{key: value for key, value in line.items() if key != "clock"} for line in keyed]
    assert json.dumps(stripped) == json.dumps(unkeyed)
    absent = copy.deepcopy(document)
    del absent["clock_stamp"]
    default, _ = run_lines(absent, 60)
    assert json.dumps(default) == json.dumps(unkeyed)
    wrong = copy.deepcopy(document)
    wrong["clock_stamp"] = 1
    with pytest.raises(ValueError, match="clock_stamp"):
        load_world(json.dumps(wrong).encode("utf-8"), base_dir=WORLDS, root=WORLDS.parent)


def test_the_count_falls_behind_the_tick_by_the_owed_count_in_a_crowd():
    """(d)."""
    document = json.loads((WORLDS / "capability_k5.json").read_text(encoding="utf-8"))
    # The pair [1, 16384]: at [1, 64] the generic entry's push turns the
    # lamp's rows off the bar before the cart (no click; the module docstring).
    document["suspension"] = [1, 16384]
    lines, simulation = run_lines(document, 120)
    cart = next(number for number, entry in simulation.measured.items() if not entry.fixed)
    clicks = [line for line in lines if line["event"] == "click" and line.get("measured") == cart]
    assert clicks
    assert all(line["clock"] <= line["tick"] for line in clicks)
    counts = [line["clock"] for line in clicks]
    assert counts == sorted(counts)
    last = clicks[-1]
    assert last["clock"] < last["tick"]
    entry = simulation.measured[cart]
    assert entry.owed > 0 and entry.age < 120
    assert last["clock"] <= entry.age


def test_the_birth_line_carries_the_emitters_count_and_without_the_key_the_record_stands(tmp_path):
    """(e)."""
    document = json.loads((WORLDS / "capability_k5.json").read_text(encoding="utf-8"))
    lines, simulation = run_lines(document, 120)
    births = [line for line in lines if line["event"] == "birth"]
    assert births and all("clock" in line for line in births)
    # The field is the emitter's own count at that interval: on a fixed lamp
    # and on the moving cart in no crowd, the interval; the emitter's `age`
    # at the end equals the last count it stamped.
    assert all(line["clock"] == line["tick"] for line in births)
    emitters = {line["measured"] for line in births}
    assert len(emitters) == 2
    for number in emitters:
        own = [line for line in births if line["measured"] == number]
        assert own[-1]["clock"] == simulation.measured[number].age == 120
        # The edge: the first birth of a body carries the count 1, the lamp
        # birthing at its first self-creation, after the count (never 0).
        assert own[0]["clock"] == 1 and own[0]["tick"] == 1
        assert own[0]["record"] & ORDINAL_MASK == 1
        assert min(line["clock"] for line in own) == 1
    # The light clock's observable off the record: N(j) = clock(return) -
    # clock(birth) of one ordinal, the return click naming the record born.
    born_at = {line["record"]: line["clock"] for line in births}
    cart = next(number for number, entry in simulation.measured.items() if not entry.fixed)
    clicks = [line for line in lines if line["event"] == "click" and line.get("measured") == cart]
    flights = [line["clock"] - born_at[line["record"]] for line in clicks if line["record"] in born_at]
    assert flights and all(flight > 0 for flight in flights)
    # The key off: no birth line carries the field, and the run's record at
    # 60 intervals is byte for byte the record before the field.
    unkeyed = {key: value for key, value in document.items() if key != "clock_stamp"}
    source = json.dumps(unkeyed).encode("utf-8")
    loaded = load_world(source, base_dir=WORLDS, root=WORLDS.parent)
    assert loaded.world.clock_stamp is False
    out = tmp_path / "unkeyed"
    out.mkdir()
    execute_nature_beam_run(loaded.world, source, out, "test", 60, keep_row_clicks=True)
    written = (out / "events.jsonl").read_bytes()
    assert all("clock" not in json.loads(line) for line in written.splitlines())
    assert hashlib.sha256(written).hexdigest() == UNKEYED_EVENTS_SHA256
