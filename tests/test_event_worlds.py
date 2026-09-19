"""The worlds of the law of events on minimal boards (Highlights 5.4, the
model owner, 2026-09-19; 5.5, "The engine of the law of events: what the
tests show"): the books close at every interval, a measured content stays
constant, the flux through every closed surface is the emission, the far
field falls as the derivation says, two measured events push each other
equally and oppositely, the two-slit detector reads a minimum and a maximum,
the world file refuses by name and the runner records a run. The integers
are pinned in docs/TEST_EXPECTATIONS.md ("The worlds of the law of events")
from the engine's first readings on 2026-09-19, as a check that it does what
the law says and not as a result.

The free family `m` of (a) to (c) declares no phase circle since
2026-09-19 (`"phase": false`, the field of matter without phase: each
Port's arrival scatters on its own, four ninths back), the suspension
reads presence and a free family's push reads the net flow; (a) to (c)
were re-pinned that day from the new engine's readings, the old ones
in docs/TEST_EXPECTATIONS.md. The field is diffusive and 300 intervals
on 29^3 is not its steady state: the pins are a check, not a result.

(a) one measured event (29^3, 300 intervals): the books close every tick,
    the content is 2^24 at every tick (what comes home is created again),
    the momentum of the measured events zero; the flux through the cube of
    half-width 4 over ticks 101 to 200 is 0.74 of the emission (within
    0.04) and, over ticks 201 to 300, through the cubes of half-width 4, 8
    and 12 it is 0.86, 0.46 and 0.17 (each within 0.05), falling with the
    half-width as the field fills; the escape per interval 0.13 of the
    emission (within 0.03);
(b) the shell means over ticks 201 to 300 at r = 4, 6, 8, 10, 12: the count
    times r^2 / q reads 2.00, 1.93, 1.63, 1.11, 0.70 (each within 10 %),
    the radial flow times 4 pi r^2 / q reads 2.78, 2.38, 2.00, 1.43, 0.99
    (each within 10 %; the shell's mean radial arrival is not Gauss's flux
    where the field turns back on itself, `cube_flux` is), the size times
    r / sqrt q reads 3.44, 3.38, 3.10, 2.56, 2.03 (each within 10 %); the
    log-log slopes -2.90 +- 0.15, -2.90 +- 0.15, -1.46 +- 0.15;
(c) two measured events (21^3, d = 8, 200 intervals, no suspension): pushed
    toward each other by the net flow of each other's field, the axial
    pushes equal within 0.5 % (0.02 % measured: the flow of a diffusive
    field is symmetric where the labels were not), the transverse below
    0.1 % of the axial, the axial against M_B rho M_A / (4 pi d^2) between
    1.3 and 1.6 (1.45 measured); the pair doubled with K doubled pushed
    four times as much within 2 % (3.999 measured);
(d) the two-slit detector (23 x 41 x 9, 200 intervals): the screen's clicks
    by y are symmetric about the axis, with a minimum within 2 to 5 of the
    axis and a maximum beyond it within 6 to 11 at least 1.1 times the
    minimum; the one-slit control has no such rise. Since 2026-09-19 a
    release costs the emitter by its phase rate and a click measures that
    content: the lamp of 2^36 at K 2^34 turns 4 steps per self-creation at
    the start and fewer as it spends (its content over K falls toward 3 and
    below during the run), so the screen's content grows by more than 3 and
    at most 4 times its clicks, while the click counts are unchanged (a
    click is one unit whatever it carries);
(e) the refusals by name: the earlier engines' keys, `phase_turn`, a closed
    board, the law's value, an unknown key, a content at K x N / 2, a lamp
    on a free family, two measured events at one Node, an unknown table
    rule, N not a power of two, a detector on a Node without a measured
    event, a Node in two detectors, a quantum on a free family; and the
    runner's record: `run.json` with the law, the books per tick, the
    measured events and the detectors; `state.json`; `events.jsonl`.
"""

from __future__ import annotations

import json
import math
from pathlib import Path

import numpy as np
import pytest

from event_universe.events import EVENTS_LAW, EventSimulation, parse_event_world
from event_universe.runner import run_initialization

CONTENT = 1 << 24
# The emission of a content of 2^24 at release [1, 128]: 2^17 per Port, six Ports.
Q = 6 * (CONTENT // 128)
SIZE_COEFFICIENT = 3 * 0.2143


def one_content(shape: int, ticks: int, *, suspension: int = 1) -> dict[str, object]:
    """One measured event of 2^24, held in place at the centre of an open cube:
    N 64, K 2^22 (four phase steps per self-creation), release [1, 128]."""
    centre = shape // 2
    return {
        "law": "events",
        "model_id": "events-test-one",
        "shape": [shape, shape, shape],
        "boundary": "open",
        "ticks": ticks,
        "K": 1 << 22,
        "N": 64,
        "release": [1, 128],
        "suspension": suspension,
        "families": [{"name": "m", "kind": "free", "charge": 0, "phase": False}],
        "measured": [
            {"position": [centre, centre, centre], "family": "m", "amount": CONTENT, "fixed": True}
        ],
    }


def pair(shape: int, distance: int, amount: int, clock: int, ticks: int) -> dict[str, object]:
    centre = shape // 2
    world = one_content(shape, ticks, suspension=0)
    world["model_id"] = "events-test-pair"
    world["K"] = clock
    world["measured"] = [
        {
            "position": [centre - distance // 2, centre, centre],
            "family": "m",
            "amount": amount,
            "fixed": True,
        },
        {
            "position": [centre + distance // 2, centre, centre],
            "family": "m",
            "amount": amount,
            "fixed": True,
        },
    ]
    return world


def slits(openings: int, ticks: int) -> dict[str, object]:
    """A lamp of light at x = 2 (2^36 units, 2^22 per self-creation on every
    heading), a wall at x = 8 of measured events of the paid family `wall`
    with one or two openings of 3 x 3 Nodes 14 apart, a screen at x = 17
    declared as the detector `screen`; 23 x 41 x 9, no suspension."""
    extent_x, extent_y, extent_z = 23, 41, 9
    lamp_x, wall_x, screen_x = 2, 8, 17
    cy, cz = extent_y // 2, extent_z // 2
    centres = ((cy - 7, cz), (cy + 7, cz)) if openings == 2 else ((cy, cz),)
    slit_nodes = {(y + dy, z + dz) for y, z in centres for dy in (-1, 0, 1) for dz in (-1, 0, 1)}
    measured: list[dict[str, object]] = [
        {
            "position": [lamp_x, cy, cz],
            "family": "light",
            "amount": 1 << 36,
            "fixed": True,
            "lamp": {"rate": [1 << 22, 1]},
        }
    ]
    for y in range(extent_y):
        for z in range(extent_z):
            if (y, z) not in slit_nodes:
                measured.append(
                    {"position": [wall_x, y, z], "family": "wall", "amount": 1, "fixed": True}
                )
    screen = []
    for y in range(extent_y):
        for z in range(extent_z):
            measured.append({"position": [screen_x, y, z], "family": "wall", "amount": 1, "fixed": True})
            screen.append([screen_x, y, z])
    return {
        "law": "events",
        "model_id": f"events-test-slits-{openings}",
        "shape": [extent_x, extent_y, extent_z],
        "boundary": "open",
        "ticks": ticks,
        "K": 1 << 34,
        "N": 64,
        "release": [1, 128],
        "suspension": 0,
        "families": [{"name": "light", "kind": "paid"}, {"name": "wall", "kind": "paid"}],
        "measured": measured,
        "detectors": [{"name": "screen", "positions": screen}],
    }


def slope(radii, values) -> float:
    x = np.log(np.array(radii, dtype=float))
    y = np.log(np.array(values, dtype=float))
    return float(np.polyfit(x, y, 1)[0])


def test_one_measured_event_keeps_its_content_reaches_its_fixed_point_and_the_shell_laws_hold():
    """(a) and (b)."""
    shape, ticks, window = 29, 300, 100
    centre = (shape // 2,) * 3
    simulation = EventSimulation(parse_event_world(one_content(shape, ticks)))
    radii = (4, 6, 8, 10, 12)
    halves = (4, 8, 12)
    flux = np.zeros(len(halves))
    early = 0.0
    count = np.zeros(len(radii))
    push = np.zeros(len(radii))
    size = np.zeros(len(radii))
    escaped_before = 0
    escape = 0.0
    for tick in range(1, ticks + 1):
        simulation.step()
        books = simulation.books()
        assert books["balanced"], (tick, books)
        measured = books["families"]["m"]["measured"]
        assert measured["current"] == measured["initial"] == CONTENT
        assert measured["measured"] == measured["spent"] == measured["escaped"] == 0
        assert books["momentum"]["measured"] == [0, 0, 0]
        transit = books["families"]["m"]["transit"]
        assert transit["initial"] == 0
        assert transit["released"] == transit["current"] + transit["escaped"] + transit["absorbed"]
        if 100 < tick <= 200:
            early += simulation.cube_flux(0, centre, 4) / Q
        if tick > ticks - window:
            flux += np.array([simulation.cube_flux(0, centre, h) for h in halves]) / Q
            escape += (transit["escaped"] - escaped_before) / Q
            readings = [simulation.shell_readings(0, centre, r) for r in radii]
            count += np.array(
                [entry["count"] * r * r / Q for entry, r in zip(readings, radii, strict=True)]
            )
            push += np.array(
                [
                    entry["flow"] * 4 * math.pi * r * r / Q
                    for entry, r in zip(readings, radii, strict=True)
                ]
            )
            size += np.array(
                [entry["size"] * r / math.sqrt(Q) for entry, r in zip(readings, radii, strict=True)]
            )
        escaped_before = transit["escaped"]
    assert abs(early / 100 - 0.74) < 0.04, early / 100
    flux, count, push, size = flux / window, count / window, push / window, size / window
    assert all(
        abs(value - pinned) < 0.05 for value, pinned in zip(flux, (0.86, 0.46, 0.17), strict=True)
    ), flux
    assert flux[0] > flux[1] > flux[2]
    assert abs(escape / window - 0.13) < 0.03, escape / window
    assert all(
        abs(value / pinned - 1) < 0.10
        for value, pinned in zip(count, (2.00, 1.93, 1.63, 1.11, 0.70), strict=True)
    ), count
    assert all(
        abs(value / pinned - 1) < 0.10
        for value, pinned in zip(push, (2.78, 2.38, 2.00, 1.43, 0.99), strict=True)
    ), push
    assert all(
        abs(value / pinned - 1) < 0.10
        for value, pinned in zip(size, (3.44, 3.38, 3.10, 2.56, 2.03), strict=True)
    ), size
    assert abs(slope(radii, count / np.array(radii) ** 2) + 2.90) < 0.15
    assert abs(slope(radii, push / np.array(radii) ** 2) + 2.90) < 0.15
    assert abs(slope(radii, size / np.array(radii)) + 1.46) < 0.15


def pushes(world: dict[str, object], ticks: int, window: int) -> tuple[list[int], list[int]]:
    simulation = EventSimulation(parse_event_world(world))
    before: dict[int, list[int]] = {}
    for tick in range(1, ticks + 1):
        simulation.step()
        books = simulation.books()
        assert books["balanced"], (tick, books)
        assert books["momentum"]["measured"] == [
            sum(entry.pushed[axis] for entry in simulation.measured.values()) for axis in range(3)
        ]
        if tick == ticks - window:
            before = {number: list(entry.pushed) for number, entry in simulation.measured.items()}
    first, second = simulation.measured[1], simulation.measured[2]
    return (
        [a - b for a, b in zip(first.pushed, before[1], strict=True)],
        [a - b for a, b in zip(second.pushed, before[2], strict=True)],
    )


def test_two_measured_events_push_each_other_equally_and_the_product_law_holds():
    """(c)."""
    shape, distance, ticks, window = 21, 8, 200, 100
    first, second = pushes(pair(shape, distance, CONTENT, 1 << 22, ticks), ticks, window)
    assert first[0] > 0 > second[0]
    assert abs(first[0] + second[0]) < 0.005 * first[0], (first, second)
    for push in (first, second):
        assert abs(push[1]) < 0.001 * abs(push[0]) and abs(push[2]) < 0.001 * abs(push[0]), push
    law = CONTENT * CONTENT * (6 / 128) / (4 * math.pi * distance * distance) * window
    assert 1.3 < first[0] / law < 1.6, first[0] / law
    doubled, _ = pushes(pair(shape, distance, 2 * CONTENT, 1 << 23, ticks), ticks, window)
    assert abs(doubled[0] / first[0] - 4) < 0.02 * 4, doubled[0] / first[0]


def screen_profile(world: dict[str, object], ticks: int) -> list[float]:
    """The detector's clicks by y, summed over z, smoothed over three."""
    simulation = EventSimulation(parse_event_world(world))
    for tick in range(1, ticks + 1):
        simulation.step()
        assert simulation.books()["balanced"], tick
    extent_y = world["shape"][1]  # type: ignore[index]
    assert isinstance(extent_y, int)
    counts = [0] * extent_y
    content = 0
    for entry in simulation.measured.values():
        if entry.detector == 0:
            counts[entry.position[1]] += entry.events[0]
            content += entry.held[0]
    report = simulation.detectors()[0]
    assert report["name"] == "screen" and report["families"]["light"]["clicks"] == sum(counts) > 0
    # Each click measured the lamp's cost of its unit, quantum x s: the turn
    # s is 4 at the start and falls as the lamp spends.
    assert 3 * sum(counts) < content <= 4 * sum(counts), (content, sum(counts))
    return [
        (counts[max(y - 1, 0)] + counts[y] + counts[min(y + 1, extent_y - 1)]) / 3
        for y in range(extent_y)
    ]


def extrema(profile: list[float], centre: int, near: tuple[int, int], far: tuple[int, int]):
    low = min(profile[centre + d] for d in range(near[0], near[1] + 1))
    high = max(profile[centre + d] for d in range(far[0], far[1] + 1))
    return low, high


def test_the_two_slit_detector_reads_a_minimum_and_a_maximum_away_from_the_axis():
    """(d)."""
    ticks = 200
    two = screen_profile(slits(2, ticks), ticks)
    one = screen_profile(slits(1, ticks), ticks)
    centre = 20
    for profile in (two, one):
        for d in range(1, 13):
            assert abs(profile[centre + d] - profile[centre - d]) <= 0.05 * profile[centre] + 1, d
    low, high = extrema(two, centre, (2, 5), (6, 11))
    assert high > 1.1 * low, (low, high, two)
    low_one, high_one = extrema(one, centre, (2, 5), (6, 11))
    assert high_one < 1.1 * low_one, (low_one, high_one, one)


def test_the_world_refuses_by_name_and_the_runner_records_a_run(tmp_path):
    """(e)."""
    world = one_content(11, 4)
    with pytest.raises(ValueError, match=f"{EVENTS_LAW}.*earlier engines' keys"):
        parse_event_world({**world, "contents": []})
    for key in ("initial_shadows", "wait_per_quantum", "schema_version", "dense_field"):
        with pytest.raises(ValueError, match=f"{EVENTS_LAW}.*{key}"):
            parse_event_world({**world, key: 1})
    with pytest.raises(ValueError, match="unknown keys: phase_turn"):
        parse_event_world({**world, "families": [{"name": "m", "kind": "free", "phase_turn": "none"}]})
    with pytest.raises(ValueError, match="closed board is refused"):
        parse_event_world({**world, "boundary": "periodic"})
    with pytest.raises(ValueError, match='"law": "events"'):
        parse_event_world({key: value for key, value in world.items() if key != "law"})
    with pytest.raises(ValueError, match="unknown keys: prefill"):
        parse_event_world({**world, "prefill": 3})
    phased = {**world, "families": [{"name": "m", "kind": "free", "charge": 0}]}
    with pytest.raises(ValueError, match="below K x N"):
        parse_event_world(
            {**phased, "measured": [{"position": [1, 1, 1], "family": "m", "amount": 1 << 28}]}
        )
    # K does not apply to a family without a phase circle.
    parse_event_world({**world, "measured": [{"position": [1, 1, 1], "family": "m", "amount": 1 << 28}]})
    with pytest.raises(ValueError, match="a lamp is a measured event of a paid family"):
        parse_event_world(
            {
                **world,
                "measured": [{"position": [1, 1, 1], "family": "m", "amount": 4, "lamp": {"rate": 1}}],
            }
        )
    with pytest.raises(ValueError, match="two measured events at one Node"):
        parse_event_world(
            {
                **world,
                "measured": [
                    {"position": [1, 1, 1], "family": "m", "amount": 4},
                    {"position": [1, 1, 1], "family": "m", "amount": 4},
                ],
            }
        )
    with pytest.raises(ValueError, match="must be one of"):
        parse_event_world(
            {
                **world,
                "measured": [
                    {"position": [1, 1, 1], "family": "m", "amount": 4, "table": {"m": "keep"}}
                ],
            }
        )
    with pytest.raises(ValueError, match="power of two"):
        parse_event_world({**world, "N": 48})
    with pytest.raises(ValueError, match="without a measured event"):
        parse_event_world({**world, "detectors": [{"name": "d", "positions": [[0, 0, 0]]}]})
    with pytest.raises(ValueError, match="a Node in two detectors"):
        parse_event_world(
            {
                **world,
                "detectors": [
                    {"name": "d", "positions": [[5, 5, 5]]},
                    {"name": "e", "positions": [[5, 5, 5]]},
                ],
            }
        )
    with pytest.raises(ValueError, match="unit is the unit of content"):
        parse_event_world({**world, "families": [{"name": "m", "kind": "free", "quantum": 2}]})
    parsed = parse_event_world(
        {**world, "detectors": [{"name": "d", "positions": [[5, 5, 5]], "threshold": 3}]}
    )
    assert parsed.owners(0) == (1,) and parsed.suspension == (1, 1) and parsed.release == (1, 128)
    assert parse_event_world({**world, "suspension": [1, 4]}).suspension == (1, 4)
    assert parse_event_world({**world, "suspension": [0, 4]}).suspension == (0, 1)
    with pytest.raises(ValueError, match="suspension denominator"):
        parse_event_world({**world, "suspension": [1, 0]})
    with pytest.raises(ValueError, match=r"families\[0\].phase must be true or false"):
        parse_event_world({**world, "families": [{"name": "m", "kind": "free", "phase": 0}]})
    with pytest.raises(ValueError, match="refused for a family without a phase circle"):
        parse_event_world(
            {
                **world,
                "measured": [
                    {
                        "position": [1, 1, 1],
                        "family": "m",
                        "amount": 4,
                        "table": {"m": {"rule": "read", "phase_window": 3}},
                    }
                ],
            }
        )
    with pytest.raises(ValueError, match=r"measured\[0\].phase must be an integer from 0 through 0"):
        parse_event_world(
            {**world, "measured": [{"position": [1, 1, 1], "family": "m", "amount": 4, "phase": 5}]}
        )
    with pytest.raises(ValueError, match="refused on a lamp of a family without a phase circle"):
        parse_event_world(
            {
                **world,
                "families": [{"name": "light", "kind": "paid", "phase": False}],
                "measured": [
                    {
                        "position": [1, 1, 1],
                        "family": "light",
                        "amount": 4,
                        "lamp": {"rate": 1, "phase_window": 3},
                    }
                ],
            }
        )
    assert parsed.detector_of((5, 5, 5)) == 0 and parsed.detectors[0].threshold == 3
    path = tmp_path / "world.json"
    path.write_text(json.dumps(world), encoding="utf-8")
    record = json.loads(run_initialization(path, tmp_path / "run").read_text(encoding="utf-8"))
    assert record["law"] == EVENTS_LAW and record["status"] == "completed"
    assert record["completed_ticks"] == 4 and record["conserved_at_every_completed_tick"] is True
    assert len(record["audit"]) == 4 and record["measured"][0]["content"] == CONTENT
    assert record["detectors"] == [] and record["suspension"] == [1, 1]
    assert record["families"][0]["phase"] is False
    assert (tmp_path / "run" / "state.json").exists() and (tmp_path / "run" / "events.jsonl").exists()
    state = json.loads((tmp_path / "run" / "state.json").read_text(encoding="utf-8"))
    assert state["law"] == EVENTS_LAW and state["tick"] == 4 and state["nodes"] and "measured" in state
    with pytest.raises(ValueError, match="ticks must be nonnegative"):
        run_initialization(path, tmp_path / "negative", ticks=-1)
    with pytest.raises(ValueError, match="empty output directory"):
        run_initialization(path, tmp_path / "run")
    assert Path(tmp_path / "run" / "initialization.json").read_bytes() == path.read_bytes()
