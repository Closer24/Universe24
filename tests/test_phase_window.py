"""The phase window under the law of events (Highlights 5.4, the model
owner, 2026-09-19: "Approve the phase window as a declared width of a
detector, and of the emitter too"): one generic key, `phase_window`, a
setting s on the circle of N steps, and the half circle centred on it (with
d = (phase - s) mod N, d < N / 4 or d >= 3 N / 4: exactly N / 2 steps). On a
table entry the response is made only to a bundle whose phase at the Node
falls in the window, a bundle outside it passing (no push, the units mixing
on, a `pass` record); on a lamp, a release only at the self-creations whose
clock phase falls in it, the clock and the phase turning either way; every
measurement record carries the phase read. `suspension` 0, `release` [0, 1],
the families `light` (paid) and `counter` (paid) in that order, every
measured event `fixed`. The expected integers of docs/TEST_EXPECTATIONS.md
("The phase window"), written down first:

(a) the boundary of the window at N = 64, K 2^20: a bar of 7 x 1 x 1, a
    source of `light` (content 8, number 1) at x = 0, a counter (content 1,
    number 2) at x = 6 measuring `light` through the window 20; four units
    of light of number 1 in transit on +X, at x = 5 with phase 35 (d = 15),
    x = 4 with 36 (d = 16), x = 3 with 3 (d = 47) and x = 2 with 4 (d = 48),
    each reaching x = 6 alone, in intervals 2, 3, 4 and 5. The units at
    d = 15 and d = 48 click (a `click` record each, with `"phase"` 35 and 4
    and the push (1, 0, 0)); the units at d = 16 and d = 47 pass (a `pass`
    record each, with the phase and `"window"` 20, no push), go on to the
    edge and escape in the walk of the next interval. After 5 intervals:
    `events` [2, 0], `held` [2, 1], the momentum (2, 0, 0), 2 escaped,
    nothing in transit, exactly those four records, the books balanced at
    every interval.
(b) the complement covers the circle exactly: a bar of 12 x 1 x 1, K 2^14,
    a lamp of `light` (content K + 2, phase 0, rate [1, 1] on +X only) at
    x = 0; with content K + 2 the release of age a carries phase a mod 64
    exactly while 2 a (a + 1) < K, so the first 64 releases carry the phases
    0, 1, ..., 63. A counter at x = 10 measuring `light` through the window
    8 and its complement at x = 11 through the window 40 (8 + 32). The
    release of age a (interval a + 1) reaches x = 10 in interval a + 11 and
    x = 11 in interval a + 12, so after 64 + 10 intervals the two counters
    clicked 32 times each: x = 10 the phases with d = (phase - 8) mod 64 in
    [0, 16) or [48, 64), that is 0..23 and 56..63, x = 11 the phases 24..55,
    every one of the first 64 releases exactly once, the 64 click records'
    phases 0..63 each once, 32 `pass` records at x = 10 (the phases 24..55,
    window 8) and none at x = 11, nothing escaped; the lamp at age 74, phase
    10, 74 phase steps, content K + 2 - 74, momentum (-74, 0, 0). In the
    75th interval the release of age 64 (phase 0 again) clicks at x = 10.
(c) a lamp with a window: the lamp of (b) with `phase_window` 8 and a plain
    counter (`measure`, no window) at x = 10. At each of the first 64
    intervals t its age is t, its phase t mod 64 and its phase steps t, and
    its departure on +X is one unit stamped with phase t - 1 when t - 1 is
    in the window (the ages 0..23 and 56..63) and nothing otherwise: after
    64 intervals 32 released, content K + 2 - 32, momentum (-32, 0, 0),
    phase 64 mod 64 = 0. After 64 + 10 intervals the counter clicked 32
    times, once at each of those phases, and the lamp, cycling on, released
    10 more at the ages 64..73 (phases 0..9), 42 in all. The refusals,
    naming the key: a window of 64 at N = 64, a window on `pass`, an object
    entry without `rule`, an object entry with an unknown key, a lamp window
    of -1.
"""

from __future__ import annotations

import pytest

from event_universe.events import EventSimulation, parse_event_world
from event_universe.events.engine import in_window

PLUS_X = 0
LIGHT, COUNTER = 0, 1
FAMILIES = [{"name": "light", "kind": "paid"}, {"name": "counter", "kind": "paid"}]
NO_RESPONSE = {"home": 0, "read": 0, "measure": 0, "rerelease": 0}
K_B = 1 << 14
# The phases in the window 8 at N = 64: d = (phase - 8) mod 64 in [0, 16) or [48, 64).
IN_WINDOW_8 = [*range(0, 24), *range(56, 64)]
OUT_OF_WINDOW_8 = list(range(24, 56))


def world(
    shape: list[int],
    measured: list[dict[str, object]],
    clock: int,
    in_transit: list[dict[str, object]] | None = None,
) -> dict[str, object]:
    return {
        "law": "events",
        "model_id": "phase-window-test",
        "shape": shape,
        "boundary": "open",
        "ticks": 75,
        "K": clock,
        "N": 64,
        "release": [0, 1],
        "suspension": 0,
        "families": FAMILIES,
        "measured": measured,
        "in_transit": in_transit or [],
    }


def counter(x: int, table: dict[str, object]) -> dict[str, object]:
    return {"position": [x, 0, 0], "family": "counter", "amount": 1, "fixed": True, "table": table}


def lamp(**keys: object) -> dict[str, object]:
    """The lamp of (b): content K + 2, phase 0, one unit per self-creation on +X."""
    return {
        "position": [0, 0, 0],
        "family": "light",
        "amount": K_B + 2,
        "phase": 0,
        "fixed": True,
        "lamp": {"rate": [1, 1], "headings": [[1, 0, 0]], **keys},
    }


def unit(x: int, phase: int) -> dict[str, object]:
    return {
        "position": [x, 0, 0],
        "family": "light",
        "number": 1,
        "heading": [1, 0, 0],
        "amount": 1,
        "phase": phase,
    }


def test_the_window_is_the_centred_half_circle_and_a_bundle_outside_it_passes():
    """(a)."""
    assert [d for d in range(64) if in_window((20 + d) % 64, 20, 64)] == [*range(16), *range(48, 64)]
    assert [d for d in range(2) if in_window(d, 0, 2)] == [0]
    assert [d for d in range(4) if in_window(d, 0, 4)] == [0, 3]
    source = {"position": [0, 0, 0], "family": "light", "amount": 8, "fixed": True}
    gate = counter(6, {"light": {"rule": "measure", "phase_window": 20}})
    units = [unit(5, 35), unit(4, 36), unit(3, 3), unit(2, 4)]
    parsed = parse_event_world(world([7, 1, 1], [source, gate], 1 << 20, units))
    assert parsed.measured[1].table == ("measure", "measure")
    assert parsed.measured[1].windows == (20, None) and parsed.measured[0].windows == (None, None)
    records: list[dict[str, object]] = []
    simulation = EventSimulation(parsed, records.append)
    entry, light = simulation.measured[2], simulation.transits[LIGHT]
    assert entry.windows == [20, None] and entry.state()["windows"] == [20, None]
    for _ in range(5):
        simulation.step()
        assert simulation.books()["balanced"], simulation.tick
    assert entry.events == [2, 0] and entry.held == [2, 1]
    assert entry.momentum == [2, 0, 0] and entry.pushed == [2, 0, 0]
    assert entry.measured[LIGHT] == {**NO_RESPONSE, "measure": 2}
    assert light.escaped == 2 and int(light.arr_amt.sum()) == 0 and int(light.fly_amt.sum()) == 0
    assert simulation.transit_absorbed[LIGHT] == 2 and simulation.held_measured[LIGHT] == 2
    common = {"node": [6, 0, 0], "measured": 2, "detector": None, "family": "light", "number": 1}
    assert records == [
        {"event": "click", "tick": 2, **common, "amount": 1, "push": [1, 0, 0], "phase": 35},
        {"event": "pass", "tick": 3, **common, "amount": 1, "phase": 36, "window": 20},
        {"event": "pass", "tick": 4, **common, "amount": 1, "phase": 3, "window": 20},
        {"event": "click", "tick": 5, **common, "amount": 1, "push": [1, 0, 0], "phase": 4},
    ]


def test_a_window_and_its_complement_cover_the_circle_exactly():
    """(b)."""
    gate = counter(10, {"light": {"rule": "measure", "phase_window": 8}})
    complement = counter(11, {"light": {"rule": "measure", "phase_window": 8 + 32}})
    records: list[dict[str, object]] = []
    simulation = EventSimulation(
        parse_event_world(world([12, 1, 1], [lamp(), gate, complement], K_B)), records.append
    )
    source, near, far = simulation.measured[1], simulation.measured[2], simulation.measured[3]
    light = simulation.transits[LIGHT]
    for _ in range(64 + 10):
        simulation.step()
        assert simulation.books()["balanced"], simulation.tick
    assert near.events == [32, 0] and far.events == [32, 0]
    assert near.held == [32, 1] and far.held == [32, 1] and light.escaped == 0
    assert simulation.held_measured[LIGHT] == 64 and simulation.transit_absorbed[LIGHT] == 64
    assert source.age == 74 and source.phase == 10 and source.phase_steps == 74
    assert source.held == [K_B + 2 - 74, 0] and source.momentum == [-74, 0, 0]
    assert simulation.held_spent[LIGHT] == 74 and simulation.transit_released[LIGHT] == 74
    clicks = [record for record in records if record["event"] == "click"]
    passes = [record for record in records if record["event"] == "pass"]
    assert len(clicks) == 64 and len(records) == len(clicks) + len(passes)
    assert sorted(record["phase"] for record in clicks) == list(range(64))
    assert sorted(record["phase"] for record in clicks if record["node"] == [10, 0, 0]) == IN_WINDOW_8
    assert (
        sorted(record["phase"] for record in clicks if record["node"] == [11, 0, 0]) == OUT_OF_WINDOW_8
    )
    assert all(record["amount"] == 1 and record["push"] == [1, 0, 0] for record in clicks)
    assert sorted(record["phase"] for record in passes) == OUT_OF_WINDOW_8
    assert all(record["node"] == [10, 0, 0] and record["window"] == 8 for record in passes)
    # The release of age a reaches x = 10 in interval a + 11: the click's tick
    # is its phase plus 11, and a passer clicks at x = 11 one interval later.
    for record in clicks:
        assert record["tick"] == record["phase"] + 11 + (record["node"] == [11, 0, 0]), record
    simulation.step()
    assert simulation.books()["balanced"]
    assert near.events == [33, 0] and far.events == [32, 0]
    assert records[-1]["event"] == "click" and records[-1]["phase"] == 0 and records[-1]["tick"] == 75


def test_a_lamp_with_a_window_releases_in_it_and_its_clock_turns_regardless():
    """(c)."""
    parsed = parse_event_world(
        world([12, 1, 1], [lamp(phase_window=8), counter(10, {"light": "measure"})], K_B)
    )
    assert parsed.measured[0].lamp is not None and parsed.measured[0].lamp.window == 8
    assert parsed.measured[1].windows == (None, None)
    records: list[dict[str, object]] = []
    simulation = EventSimulation(parsed, records.append)
    source, gate, light = simulation.measured[1], simulation.measured[2], simulation.transits[LIGHT]
    assert source.lamp_window == 8
    own = (0, 0, 0, light.rank[1], PLUS_X)
    for tick in range(1, 65):
        simulation.step()
        assert simulation.books()["balanced"], tick
        assert source.age == tick and source.phase == tick % 64 and source.phase_steps == tick, tick
        released = (tick - 1) in IN_WINDOW_8
        assert int(light.fly_amt[own]) == int(released), tick
        if released:
            assert int(light.fly_ph[own]) == tick - 1 and light.fly_mom[own].tolist() == [1, 0, 0], tick
    assert simulation.transit_released[LIGHT] == 32 and simulation.held_spent[LIGHT] == 32
    assert source.held == [K_B + 2 - 32, 0] and source.momentum == [-32, 0, 0] and source.phase == 0
    for _ in range(10):
        simulation.step()
        assert simulation.books()["balanced"], simulation.tick
    assert gate.events == [32, 0] and gate.held == [32, 1] and light.escaped == 0
    clicks = [record for record in records if record["event"] == "click"]
    assert len(clicks) == len(records) == 32
    assert sorted(record["phase"] for record in clicks) == IN_WINDOW_8
    assert simulation.transit_released[LIGHT] == 42 and source.held == [K_B + 2 - 42, 0]
    assert source.age == 74 and source.phase == 10

    base = world([12, 1, 1], [lamp(), counter(10, {"light": "measure"})], K_B)
    with pytest.raises(
        ValueError, match=r"table\['light'\]\.phase_window must be an integer from 0 through 63"
    ):
        parse_event_world(
            {
                **base,
                "measured": [lamp(), counter(10, {"light": {"rule": "measure", "phase_window": 64}})],
            }
        )
    with pytest.raises(ValueError, match=r"table\['light'\]\.phase_window is refused on pass"):
        parse_event_world(
            {**base, "measured": [lamp(), counter(10, {"light": {"rule": "pass", "phase_window": 8}})]}
        )
    with pytest.raises(ValueError, match=r"table\['light'\] lacks keys: rule"):
        parse_event_world({**base, "measured": [lamp(), counter(10, {"light": {"phase_window": 8}})]})
    with pytest.raises(ValueError, match=r"table\['light'\] has unknown keys: width"):
        parse_event_world(
            {**base, "measured": [lamp(), counter(10, {"light": {"rule": "measure", "width": 8}})]}
        )
    with pytest.raises(ValueError, match=r"lamp\.phase_window must be an integer from 0 through 63"):
        parse_event_world(
            {**base, "measured": [lamp(phase_window=-1), counter(10, {"light": "measure"})]}
        )
