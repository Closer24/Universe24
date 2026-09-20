"""The phase window under the law of the ray (docs/RAY_LAW.md, section 3,
step 4; the model owner, 2026-09-19: "Approve the phase window as a declared
width of a detector, and of the emitter too"): one generic key,
`phase_window`, a setting s on the circle of N steps and the half circle
centred on it (d = (phase - s) mod N, d < N / 4 or d >= 3 N / 4). On a table
entry the response is made to each ray whose own phase falls in the window
(no coherent sum: the window reads the record), a ray outside it passing
with a `pass` record; on a lamp, a release only at the self-creations whose
clock phase falls in it, the clock and the phase turning either way.
Re-pinned from `test_phase_window` under the flight table (a ray released
at tick t first walks at t + 1; 10 Links take 17 walks, 11 Links 19). The
expected integers of docs/TEST_EXPECTATIONS.md ("The phase window under the
ray law"), written down first. Bars of 1 x 1 in y and z, N 64, `suspension`
0, `release` [0, 1], the families `light` (paid) and `counter` (paid), every
measured event `fixed`:

(a) the boundary of the window at N = 64: a counter at x = 6 of a 7 x 1 x 1
    bar measuring `light` through the window 20; four rays of number 1 on
    +X at x = 5 with phase 35 (d = 15), x = 4 with 36 (d = 16), x = 3 with 3
    (d = 47) and x = 2 with 4 (d = 48), reaching x = 6 in intervals 1, 3, 5
    and 7 (the flight table's first arrivals at 1, 2, 3 and 4 Links). d = 15
    and d = 48 click (`click` records at ticks 1 and 7 with `phase` 35 and
    4, the push (64, 0, 0), `content` 1; since 2026-09-19 the label of a
    unit along a heading is Q e_d, Q = 64, RAY_LAW section 2 and note 23);
    d = 16 and d = 47 pass (`pass` records at ticks 3 and 5 with the phase
    and `window` 20), go on and click on `face:+x` at their next step
    (ticks 5 and 7). After 7 intervals `events` [2, 0], `held` [2, 1], the
    momentum (128, 0, 0), 2 escaped, nothing in the store, the books
    balanced; `in_window` at
    N = 64 admits d in [0, 16) and [48, 64), at N = 2 the step 0, at N = 4
    the steps 0 and 3 (the window table);
(b) the complement covers the circle exactly: a bar of 12 x 1 x 1, K 2^14,
    a lamp of `light` (content K + 2, phase 0, rate [1, 1] on +X only) at
    x = 0, whose release of age a carries the phase a mod 64; a counter at
    x = 10 measuring through the window 40 and its complement at x = 11
    through the window 8. The release of age a (tick a + 1) reaches x = 10
    at tick a + 18 and x = 11 at tick a + 20: after 83 intervals (the age
    63 at x = 11) the two counters clicked 32 times each, x = 10 the phases
    24..55, x = 11 the phases 0..23 and 56..63, every one of the first 64
    releases exactly once; 34 `pass` records at x = 10 (the 32 outside its
    window and the ages 64 and 65, phases 0 and 1, still on their way to
    x = 11) and none at x = 11, nothing escaped; the lamp at age 83, phase
    19, content K + 2 - 83, momentum (-5312, 0, 0) (83 labels of 64);
(c) a lamp with a window: the lamp of (b) with `phase_window` 8 and a plain
    counter at x = 10: at each of the first 64 intervals t its age is t, its
    phase t mod 64, and it released one ray at phase t - 1 when t - 1 is in
    the window (the ages 0..23 and 56..63) and none otherwise: after 64
    intervals 32 released, content K + 2 - 32, momentum (-2048, 0, 0), phase
    0; after 81 (the age 63 at x = 10) the counter clicked 32 times, once at
    each of those phases, and the lamp released 17 more (the ages 64..80,
    the phases 0..16, all in the window), 49 in all. The
    refusals, naming the key: a window of 64 at N = 64, a window on `pass`,
    an object entry with an unknown key, a lamp window of -1, a `reads` key
    outside the reading's components; an object entry without `rule` takes
    the family's default rule (a window alone on a paid family measures in
    the window 8).
"""

from __future__ import annotations

import pytest

from event_universe.events import NatureBeamSimulation, parse_nature_beam_world
from event_universe.events.nature_beam import nature_beam_tables

LIGHT, COUNTER = 0, 1
FAMILIES = [{"name": "light", "quantum": 1}, {"name": "counter", "quantum": 1}]
NO_RESPONSE = {"home": 0, "read": 0, "measure": 0, "rerelease": 0}
K_B = 1 << 14
IN_WINDOW_8 = [*range(0, 24), *range(56, 64)]
OUT_OF_WINDOW_8 = list(range(24, 56))
# A ray released at tick t first walks at t + 1: 10 Links take 17 walks.
TEN, ELEVEN = 17, 19


def world(
    shape: list[int],
    measured: list[dict[str, object]],
    clock: int,
    in_transit: list[dict[str, object]] | None = None,
) -> dict[str, object]:
    return {
        "law": "rays",
        "model_id": "ray-window-test",
        "shape": shape,
        "boundary": "open",
        "ticks": 90,
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
    return {
        "position": [0, 0, 0],
        "family": "light",
        "amount": K_B + 2,
        "phase": 0,
        "fixed": True,
        "lamp": {"rate": [1, 1], "directions": [[1, 0, 0]], **keys},
    }


def beam(x: int, phase: int) -> dict[str, object]:
    return {
        "position": [x, 0, 0],
        "family": "light",
        "number": 1,
        "direction": [1, 0, 0],
        "amount": 1,
        "phase": phase,
    }


def test_the_window_is_the_centred_half_circle_and_a_ray_outside_it_passes():
    """(a)."""
    for modulus, admitted in ((64, [*range(16), *range(48, 64)]), (2, [0]), (4, [0, 3])):
        tables = nature_beam_tables(
            parse_nature_beam_world(
                world([7, 1, 1], [counter(6, {"light": "measure"})], 1 << 20) | {"N": modulus}
            )
        )
        assert [d for d in range(modulus) if tables.window[d]] == admitted
    source = {"position": [0, 0, 0], "family": "light", "amount": 8, "fixed": True}
    gate = counter(6, {"light": {"rule": "measure", "phase_window": 20}})
    beams = [beam(5, 35), beam(4, 36), beam(3, 3), beam(2, 4)]
    parsed = parse_nature_beam_world(world([7, 1, 1], [source, gate], 1 << 20, beams))
    assert parsed.measured[1].table == ("measure", "measure") and parsed.measured[1].windows == (
        20,
        None,
    )
    records: list[dict[str, object]] = []
    simulation = NatureBeamSimulation(parsed, records.append)
    entry = simulation.measured[2]
    for _ in range(7):
        simulation.step()
        assert simulation.books()["balanced"], simulation.tick
    assert entry.clicks == [2, 0] and entry.held == [2, 1]
    assert entry.momentum == [128, 0, 0] and entry.pushed == [128, 0, 0]
    assert entry.taken[LIGHT] == {**NO_RESPONSE, "measure": 2}
    assert simulation.stores[LIGHT].size == 0 and simulation.ledger.escaped_amount(LIGHT) == 2
    kinds = [
        (r["event"], r["tick"], r.get("detector"), r["phase"]) for r in records if r["event"] != "record"
    ]
    assert kinds == [
        ("click", 1, None, 35),
        ("pass", 3, None, 36),
        ("click", 5, "face:+x", 36),
        ("pass", 5, None, 3),
        ("click", 7, "face:+x", 3),
        ("click", 7, None, 4),
    ]
    clicks = [r for r in records if r["event"] == "click" and r["detector"] is None]
    assert all(r["push"] == [64, 0, 0] and r["content"] == 1 and r["amount"] == 1 for r in clicks)
    passes = [r for r in records if r["event"] == "pass"]
    assert all(r["window"] == 20 and r["node"] == [6, 0, 0] for r in passes)


def test_a_window_and_its_complement_cover_the_circle_exactly():
    """(b)."""
    gate = counter(10, {"light": {"rule": "measure", "phase_window": 8 + 32}})
    complement = counter(11, {"light": {"rule": "measure", "phase_window": 8}})
    records: list[dict[str, object]] = []
    simulation = NatureBeamSimulation(
        parse_nature_beam_world(world([12, 1, 1], [lamp(), gate, complement], K_B)), records.append
    )
    source, near, far = simulation.measured[1], simulation.measured[2], simulation.measured[3]
    for _ in range(83):
        simulation.step()
        assert simulation.books()["balanced"], simulation.tick
    assert near.clicks == [32, 0] and far.clicks == [32, 0]
    assert near.held == [32, 1] and far.held == [32, 1] and simulation.ledger.escaped_amount(LIGHT) == 0
    assert source.age == 83 and source.phase == 19 and source.turned == 83
    assert source.held == [K_B + 2 - 83, 0] and source.momentum == [-5312, 0, 0]
    clicks = [r for r in records if r["event"] == "click"]
    passes = [r for r in records if r["event"] == "pass"]
    assert len(clicks) == 64
    assert sorted(r["phase"] for r in clicks) == list(range(64))
    assert sorted(r["phase"] for r in clicks if r["node"] == [10, 0, 0]) == OUT_OF_WINDOW_8
    assert sorted(r["phase"] for r in clicks if r["node"] == [11, 0, 0]) == IN_WINDOW_8
    assert all(r["amount"] == 1 and r["push"] == [64, 0, 0] and r["content"] == 1 for r in clicks)
    assert sorted(r["phase"] for r in passes) == sorted([*IN_WINDOW_8, 0, 1])
    assert all(r["node"] == [10, 0, 0] and r["window"] == 40 for r in passes)
    for record in clicks:
        offset = TEN + 1 if record["node"] == [10, 0, 0] else ELEVEN + 1
        assert record["tick"] == record["phase"] + offset, record


def test_a_lamp_with_a_window_releases_in_it_and_its_clock_turns_regardless():
    """(c)."""
    parsed = parse_nature_beam_world(
        world([12, 1, 1], [lamp(phase_window=8), counter(10, {"light": "measure"})], K_B)
    )
    assert parsed.measured[0].lamp is not None and parsed.measured[0].lamp.window == 8
    records: list[dict[str, object]] = []
    simulation = NatureBeamSimulation(parsed, records.append)
    source, gate, light = simulation.measured[1], simulation.measured[2], simulation.stores[LIGHT]
    assert source.lamp_window == 8
    for tick in range(1, 65):
        simulation.step()
        assert simulation.books()["balanced"], tick
        assert source.age == tick and source.phase == tick % 64 and source.turned == tick, tick
        fresh = light.age == 0
        released = (tick - 1) in IN_WINDOW_8
        assert int(fresh.sum()) == int(released), tick
        if released:
            assert int(light.phase[fresh][0]) == tick - 1 and int(light.direction[fresh][0]) == 2
    assert simulation.ledger.transit_released[LIGHT] == 32 and simulation.ledger.held_spent[LIGHT] == 32
    assert source.held == [K_B + 2 - 32, 0] and source.momentum == [-2048, 0, 0] and source.phase == 0
    for _ in range(17):
        simulation.step()
        assert simulation.books()["balanced"], simulation.tick
    assert (
        gate.clicks == [32, 0] and gate.held == [32, 1] and simulation.ledger.escaped_amount(LIGHT) == 0
    )
    clicks = [record for record in records if record["event"] == "click"]
    assert len(clicks) == 32 and sorted(record["phase"] for record in clicks) == IN_WINDOW_8
    assert simulation.ledger.transit_released[LIGHT] == 49 and source.held == [K_B + 2 - 49, 0]
    assert source.age == 81 and source.phase == 17

    base = world([12, 1, 1], [lamp(), counter(10, {"light": "measure"})], K_B)
    with pytest.raises(
        ValueError, match=r"table\['light'\]\.phase_window must be an integer from 0 through 63"
    ):
        parse_nature_beam_world(
            {
                **base,
                "measured": [lamp(), counter(10, {"light": {"rule": "measure", "phase_window": 64}})],
            }
        )
    with pytest.raises(ValueError, match=r"table\['light'\]\.phase_window is refused on pass"):
        parse_nature_beam_world(
            {**base, "measured": [lamp(), counter(10, {"light": {"rule": "pass", "phase_window": 8}})]}
        )
    # A window alone is a lawful entry: the rule is the family's default
    # (`measure` for a paid family; the table generated from the keys).
    windowed = parse_nature_beam_world(
        {**base, "measured": [lamp(), counter(10, {"light": {"phase_window": 8}})]}
    )
    assert windowed.measured[1].table[0] == "measure" and windowed.measured[1].windows[0] == 8
    with pytest.raises(ValueError, match=r"table\['light'\] has unknown keys: width"):
        parse_nature_beam_world(
            {**base, "measured": [lamp(), counter(10, {"light": {"rule": "measure", "width": 8}})]}
        )
    with pytest.raises(ValueError, match=r"lamp\.phase_window must be an integer from 0 through 63"):
        parse_nature_beam_world(
            {**base, "measured": [lamp(phase_window=-1), counter(10, {"light": "measure"})]}
        )
    with pytest.raises(ValueError, match=r"table\['light'\]\.reads must be one of"):
        parse_nature_beam_world(
            {**base, "measured": [lamp(), counter(10, {"light": {"rule": "measure", "reads": "wave"}})]}
        )
