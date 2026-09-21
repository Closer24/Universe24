"""A table entry's window read from a reading (docs/ENGINE.md, "The world";
docs/BEAM_LAW.md note 34; issue #363, 2026-09-20: the settings of a Bell run
decided by GameBoard events). The key `phase_window` on a measured event's
table entry accepts, beside the number, `{"reads": "<family>", "offset": s}`:
the centre of the window is the phase of the coherent pointer
(`nature_beam.coherent_pointer`, the first moment over the circle; its
nearest step `pointer_phases`) of the named family's rows present at the
set in the interval (every row at the set but the reader's own number, rest
and moving alike, as the presence counts them) plus the offset in phase
steps (0 by default); the width stays the law's half circle. With no row of
the named family at the set, or a zero pointer, the entry passes with a
`pass` record naming `window` None and `reads`; every `click` of such an
entry carries the `window` used. The expected integers of
docs/TEST_EXPECTATIONS.md ("A window read from a reading"), written down
first. A bar of 7 x 1 x 1, N 64, K 2^20, `suspension` 0, `release` [0, 1],
the families `light` (paid), `counter` (paid) and `s` (free, the setting),
every measured event `fixed`, a counter at x = 3 measuring `light` through
`{"reads": "s", "offset": 4}` and passing `s`, a measured event of `s` at
x = 6 (the number the setting rays carry) and one of `light` at x = 0 (the
number the pair rays carry):

(a) the centre is the setting ray's phase plus the offset: a ray of `s`
    (number 2, phase 20) and a ray of `light` (number 3, phase 30) both at
    x = 2 on +X reach x = 3 in the first interval (the flight table's first
    step); the centre is 24 and d = 6 is inside, so the light ray clicks at
    tick 1 with `window` 24 on the click record, `held` [1, 1, 0] and the
    push (64, 0, 0); a second light ray of phase 45 (d = 21, outside) at
    x = 2 with the age 1 (its next step at the age 2) arrives at tick 2
    with the same setting ray still present (its second interval at x = 3,
    no step at its age 1: the presence counts it) and passes with `window`
    24 and `reads` "s"; the setting ray passes the counter's table with no
    record (`pass` responds to nothing) and goes on; a numeric window 24 on
    the same world gives the same clicks and passes, without `window` on
    the click and without `reads`;
(b) the edge case, no setting ray present: a light ray of phase 24 alone
    at x = 2 passes at tick 1 with `window` None and `reads` "s", no
    `threshold` key, and goes on (past the `s` event, which passes light)
    to click on `face:+x` at tick 8 (five Links, m(8) = 5); two setting
    rays in antiphase (20 and 52) arriving with the light ray give a zero
    pointer, no centre, and the light ray passes the same way;
(c) the parsing: `windows` None on the `light` entry and `window_reads`
    (2, 4) on it (the family `s` at index 2, the offset 4), the
    offset 0 by default; refused naming the key: an unknown family, a
    family without a phase circle, the entry's own family, the form on
    `pass`, an offset of 64 at N = 64, an unknown key in the object, a
    missing `reads`, and the form on a lamp (a lamp's window is a number).
"""

from __future__ import annotations

import pytest

from event_universe.events import NatureBeamSimulation, parse_nature_beam_world

LIGHT, COUNTER, SETTING = 0, 1, 2
FAMILIES = [
    {"name": "light", "quantum": 1},
    {"name": "counter", "quantum": 1},
    {"name": "s", "quantum": 0},
]
READS = {"light": {"phase_window": {"reads": "s", "offset": 4}}, "s": "pass"}
NUMERIC = {"light": {"phase_window": 24}, "s": "pass"}


def world(table: dict[str, object], in_transit: list[dict[str, object]]) -> dict[str, object]:
    return {
        "law": "beam",
        "model_id": "window-reads-test",
        "shape": [7, 1, 1],
        "boundary": "open",
        "ticks": 10,
        "K": 1 << 20,
        "N": 64,
        "release": [0, 1],
        "suspension": 0,
        "families": FAMILIES,
        "measured": [
            {
                "position": [0, 0, 0],
                "family": "light",
                "amount": 8,
                "fixed": True,
                "table": {"s": "pass"},
            },
            {"position": [3, 0, 0], "family": "counter", "amount": 1, "fixed": True, "table": table},
            {
                "position": [6, 0, 0],
                "family": "s",
                "amount": 1,
                "fixed": True,
                "table": {"s": "pass", "light": "pass"},
            },
        ],
        "in_transit": in_transit,
    }


def ray(family: str, number: int, x: int, phase: int, age: int = 0) -> dict[str, object]:
    return {
        "position": [x, 0, 0],
        "family": family,
        "number": number,
        "direction": [1, 0, 0],
        "amount": 1,
        "phase": phase,
        "age": age,
    }


def run(
    document: dict[str, object], intervals: int
) -> tuple[NatureBeamSimulation, list[dict[str, object]]]:
    records: list[dict[str, object]] = []
    simulation = NatureBeamSimulation(parse_nature_beam_world(document), records.append)
    for _ in range(intervals):
        simulation.step()
        assert simulation.books()["balanced"], simulation.tick
    return simulation, records


def lines(records: list[dict[str, object]], kind: str) -> list[dict[str, object]]:
    return [r for r in records if r["event"] == kind and r["detector"] is None]


def test_the_centre_is_the_setting_rays_phase_plus_the_offset():
    """(a)."""
    rays = [ray("s", 3, 2, 20), ray("light", 1, 2, 30), ray("light", 1, 2, 45, age=1)]
    simulation, records = run(world(READS, rays), 3)
    counter = simulation.measured[2]
    clicks = lines(records, "click")
    passes = lines(records, "pass")
    assert [(r["tick"], r["phase"], r["window"]) for r in clicks] == [(1, 30, 24)]
    assert clicks[0]["push"] == [64, 0, 0] and clicks[0]["content"] == 1
    assert counter.held == [1, 1, 0] and counter.clicks == [1, 0, 0]
    assert [(r["tick"], r["phase"], r["window"], r["reads"]) for r in passes] == [(2, 45, 24, "s")]
    assert "threshold" not in passes[0]
    # The setting ray met `pass`: no record of it, and it went on.
    assert all(r["family"] == "light" for r in clicks + passes)
    assert simulation.stores[SETTING].size == 1 and counter.taken[SETTING]["measure"] == 0
    # The number written in the file gives the same clicks and passes, the
    # record without the reading's keys.
    numeric_simulation, numeric_records = run(world(NUMERIC, rays), 3)
    numeric_clicks = lines(numeric_records, "click")
    numeric_passes = lines(numeric_records, "pass")
    assert [(r["tick"], r["phase"]) for r in numeric_clicks] == [(1, 30)]
    assert "window" not in numeric_clicks[0] and "reads" not in numeric_passes[0]
    assert [(r["tick"], r["phase"], r["window"]) for r in numeric_passes] == [(2, 45, 24)]
    assert numeric_simulation.measured[2].held == counter.held


def test_without_a_setting_ray_the_entry_passes_naming_window():
    """(b)."""
    _, records = run(world(READS, [ray("light", 1, 2, 24)]), 9)
    passes = lines(records, "pass")
    assert [(r["tick"], r["phase"], r["window"], r["reads"]) for r in passes] == [(1, 24, None, "s")]
    assert "threshold" not in passes[0] and lines(records, "click") == []
    faces = [r for r in records if r["event"] == "click" and r["detector"] == "face:+x"]
    assert [(r["tick"], r["family"], r["phase"]) for r in faces] == [(8, "light", 24)]
    # Two setting rays in antiphase: a zero pointer, no centre.
    rays = [ray("s", 3, 2, 20), ray("s", 3, 2, 52), ray("light", 1, 2, 24)]
    _, records = run(world(READS, rays), 1)
    passes = lines(records, "pass")
    assert [(r["tick"], r["phase"], r["window"], r["reads"]) for r in passes] == [(1, 24, None, "s")]


def test_the_parsing_and_the_refusals():
    """(c)."""
    parsed = parse_nature_beam_world(world(READS, []))
    assert parsed.measured[1].windows == (None, None, None)
    assert parsed.measured[1].window_reads == ((SETTING, 4), None, None)
    assert parsed.measured[1].table == ("measure", "measure", "pass")
    by_default = parse_nature_beam_world(
        world({"light": {"phase_window": {"reads": "s"}}, "s": "pass"}, [])
    )
    assert by_default.measured[1].window_reads[LIGHT] == (SETTING, 0)
    numeric = parse_nature_beam_world(world(NUMERIC, []))
    assert numeric.measured[1].windows[LIGHT] == 24 and numeric.measured[1].window_reads[LIGHT] is None

    def refused(table: dict[str, object], message: str) -> None:
        with pytest.raises(ValueError, match=message):
            parse_nature_beam_world(world(table, []))

    refused({"light": {"phase_window": {"reads": "t"}}}, r"phase_window\.reads names an unknown family")
    refused({"light": {"phase_window": {"reads": "light"}}}, r"names the entry's own family 'light'")
    refused(
        {"light": {"phase_window": {"reads": "s"}, "rule": "pass"}}, r"phase_window is refused on pass"
    )
    refused(
        {"light": {"phase_window": {"reads": "s", "offset": 64}}},
        r"phase_window\.offset must be an integer",
    )
    refused(
        {"light": {"phase_window": {"reads": "s", "width": 1}}}, r"phase_window has unknown keys: width"
    )
    refused({"light": {"phase_window": {"offset": 1}}}, r"phase_window lacks keys: reads")
    phaseless = world(READS, [])
    phaseless["families"] = [*FAMILIES[:2], {"name": "s", "quantum": 0, "phase": False}]
    with pytest.raises(ValueError, match=r"names the family 's', which has no phase circle"):
        parse_nature_beam_world(phaseless)
    lamp = world({"s": "pass"}, [])
    lamp["measured"][0]["lamp"] = {
        "wheel": [1, 64],
        "rate": [1, 1],
        "directions": [[1, 0, 0]],
        "phase_window": {"reads": "s"},
    }
    with pytest.raises(ValueError, match=r"lamp\.phase_window must be an integer"):
        parse_nature_beam_world(lamp)
