"""The law of the shadow, the field-only engine (field-only-v1; Highlights 5.4,
"The law of the shadow: only shadows and events", the model owner's decision of
2026-09-18, the evening; feature 20): only shadows and events, matter a content
held at Nodes that releases its field every interval, absorbs the whole quanta
that reach it by its table and releases them again; the push an absorption
read by the holder's content (gravity) and charge (electricity); the wait the
size of the field read by every quantum, held or in flight; the books per
family and the momentum exact at every interval.

Expected numbers are pinned in docs/TEST_EXPECTATIONS.md ("The law of the
shadow") before the first run, from DERIVATIONS.md round 7 (sections 46 to
50): (a) a held content at rest on an open board releases at its rate, the
books close every tick, the content stays constant, and the field reaches its
fixed point within the transit (Gauss's flux through every cube the emission);
(b) the shell means fall as 1/r^2 in the count and the push and as 1/r in the
size, with the derivation's coefficients; (c) two held contents at rest push
each other equally and oppositely (the free field read at each and passed
on, round 8 section 54 (ii)) and the product law holds for a pair scaled
together; (d) a lamp, two slits and a screen of marks: the marks' counts have
a minimum and a maximum away from the axis where the one-slit control falls
away from the axis without them (a reading); (e) a held content near a mass
waits, the fraction of intervals waited falling as 1/r (the slope nearer -1
than -2); (f) the mode's refusals; (g) the nearest phase step of the layer
equals the engine's argmax rule; (h) a held content given a momentum steps
by its accumulators, at most once in two intervals, its momentum untouched
and its own field pushing nothing (round 8 sections 53 and 54).
"""

from __future__ import annotations

import json
import math
from pathlib import Path

import numpy as np
import pytest

from event_universe.core.spatial_state import phase_cosines, phase_sines
from event_universe.initialization import parse_initial_state
from event_universe.runner import run_initialization
from event_universe.shadow import SHADOW_LAW, ShadowSimulation, parse_shadow_world
from event_universe.shadow.layer import nearest_step, step_window

ROOT = Path(__file__).resolve().parents[1]
# The emission of a content of 2^24 at release [1, 128]: 2^17 per Port, six Ports.
CONTENT = 1 << 24
Q = 6 * (CONTENT // 128)
# The derivation's coefficients (round 7, section 46 (iii)): the count 0.147 q/r^2
# (0.1378 plus the edge's excess), the push q/(4 pi r^2), the amplitude
# 0.2143 sqrt(q)/r, which the engine's size reads as 3|u|.
COUNT_COEFFICIENT = 0.147
SIZE_COEFFICIENT = 3 * 0.2143


def one_content(shape: int, ticks: int, *, wait: object = 1) -> dict[str, object]:
    """One content of 2^24 at rest, held in place, at the centre of an open
    cube: N 64, K 2^22 (four phase steps per interval, the period 16),
    release [1, 128]."""
    centre = shape // 2
    return {
        "law": "shadow",
        "model_id": "field-only-test-one",
        "shape": [shape, shape, shape],
        "boundary": "open",
        "ticks": ticks,
        "K": 1 << 22,
        "N": 64,
        "release": [1, 128],
        "wait_per_quantum": wait,
        "families": [{"name": "m", "kind": "free", "charge": 0}],
        "contents": [
            {"position": [centre, centre, centre], "family": "m", "amount": CONTENT, "fixed": True}
        ],
    }


def pair(shape: int, distance: int, amount: int, clock: int, ticks: int) -> dict[str, object]:
    """Two contents of one amount at rest, held in place, on the x axis
    symmetric about the centre, no wait."""
    centre = shape // 2
    world = one_content(shape, ticks, wait=0)
    world["model_id"] = "field-only-test-pair"
    world["K"] = clock
    world["contents"] = [
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
    """A lamp of light at x = 2 (a paid family, 2^36 quanta, 2^22 per interval
    on every heading, four phase steps per interval), a wall at x = 8 of held
    contents of the paid family `wall` (content 1, holding light) with one or
    two slits, openings of 3 x 3 Nodes in the wall, 14 apart (a re-emitting
    slit would stamp its own number on the light, and two numbers never
    interfere), a screen of marks at x = 17; 23 x 41 x 9, no wait."""
    extent_x, extent_y, extent_z = 23, 41, 9
    lamp_x, wall_x, screen_x = 2, 8, 17
    cy, cz = extent_y // 2, extent_z // 2
    centres = ((cy - 7, cz), (cy + 7, cz)) if openings == 2 else ((cy, cz),)
    slit_nodes = {(y + dy, z + dz) for y, z in centres for dy in (-1, 0, 1) for dz in (-1, 0, 1)}
    contents: list[dict[str, object]] = [
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
                contents.append(
                    {"position": [wall_x, y, z], "family": "wall", "amount": 1, "fixed": True}
                )
    for y in range(extent_y):
        for z in range(extent_z):
            contents.append({"position": [screen_x, y, z], "family": "wall", "amount": 1, "fixed": True})
    return {
        "law": "shadow",
        "model_id": f"field-only-test-slits-{openings}",
        "shape": [extent_x, extent_y, extent_z],
        "boundary": "open",
        "ticks": ticks,
        "K": 1 << 34,
        "N": 64,
        "release": [1, 128],
        "wait_per_quantum": 0,
        "families": [{"name": "light", "kind": "paid"}, {"name": "wall", "kind": "paid"}],
        "contents": contents,
    }


# E11's nine probe Nodes about the source: three on an axis, three on (110),
# three on (111).
PROBES = (
    (4, 0, 0),
    (8, 0, 0),
    (12, 0, 0),
    (3, 3, 0),
    (6, 6, 0),
    (9, 9, 0),
    (2, 2, 2),
    (5, 5, 5),
    (7, 7, 7),
)


def probes(shape: int, ticks: int) -> dict[str, object]:
    """The content of `one_content` with nine probes of a paid family (content
    1, passing the mass's quanta, held in place) at E11's Nodes, the wait one
    interval per 512 whole units of size read."""
    centre = shape // 2
    world = one_content(shape, ticks, wait=[1, 512])
    world["model_id"] = "field-only-test-wait"
    world["families"] = [{"name": "m", "kind": "free", "charge": 0}, {"name": "probe", "kind": "paid"}]
    contents = world["contents"]
    assert isinstance(contents, list)
    for x, y, z in PROBES:
        contents.append(
            {
                "position": [centre + x, centre + y, centre + z],
                "family": "probe",
                "amount": 1,
                "fixed": True,
                "table": {"m": "pass"},
            }
        )
    return world


def run(world: dict[str, object], ticks: int, *, window: int = 0):
    """Step a world, the books asserted at every tick; returns the simulation
    and the per-tick books of the last `window` ticks."""
    simulation = ShadowSimulation(parse_shadow_world(world))
    books = []
    for tick in range(1, ticks + 1):
        simulation.step()
        entry = simulation.books()
        assert entry["balanced"], (tick, entry)
        if tick > ticks - window:
            books.append(entry)
    return simulation, books


def slope(radii, values) -> float:
    """The log-log slope of values against radii, least squares."""
    x = np.log(np.array(radii, dtype=float))
    y = np.log(np.array(values, dtype=float))
    return float(np.polyfit(x, y, 1)[0])


def test_one_content_releases_reaches_its_fixed_point_and_the_shell_laws_hold():
    """(a) and (b): 29^3, 300 ticks, the window ticks 201 to 300."""
    shape, ticks, window = 29, 300, 100
    centre = (shape // 2,) * 3
    world = one_content(shape, ticks)
    simulation = ShadowSimulation(parse_shadow_world(world))
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
        # (a) the books close every tick, the content is constant, nothing of
        # the momentum exists (a content at rest carries none, its field none).
        assert books["balanced"], (tick, books)
        held = books["families"]["m"]["held"]
        assert held["current"] == held["initial"] == CONTENT
        assert held["absorbed"] == held["spent"] == held["escaped"] == 0
        assert books["momentum"]["held"] == [0, 0, 0]
        shadows = books["families"]["m"]["shadows"]
        assert shadows["initial"] == 0
        assert shadows["released"] == shadows["current"] + shadows["escaped"] + shadows["absorbed"]
        if 100 < tick <= 200:
            early += simulation.cube_flux(0, centre, 4) / Q
        if tick > ticks - window:
            flux += np.array([simulation.cube_flux(0, centre, h) for h in halves]) / Q
            escape += (shadows["escaped"] - escaped_before) / Q
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
        escaped_before = shadows["escaped"]
    # (a) the fixed point within the transit: the flux through the cube of
    # half-width 4 is the emission within 2 % over ticks 101 to 200 (2 sqrt 3 H
    # = 48), and in the window through every cube; the escape the emission
    # within 3 % (the rest shed into standing content at N = 64).
    assert abs(early / 100 - 1) < 0.02, early / 100
    flux, count, push, size = flux / window, count / window, push / window, size / window
    assert all(abs(value - 1) < 0.02 for value in flux), flux
    assert abs(escape / window - 1) < 0.03, escape / window
    # (b) the shell means: the count 0.147 q/r^2 with the standing excess, the
    # push q/(4 pi r^2) within the edge's ripple, the size 3 x 0.2143 sqrt(q)/r.
    assert all(0.14 <= value <= 0.20 for value in count), count
    assert all(abs(value - 1) < 0.20 for value in push), push
    assert all(abs(value / SIZE_COEFFICIENT - 1) < 0.05 for value in size), size
    assert abs(slope(radii, count / np.array(radii) ** 2) + 2) < 0.10
    assert abs(slope(radii, push / np.array(radii) ** 2) + 2) < 0.15
    assert abs(slope(radii, size / np.array(radii)) + 1) < 0.10


def pushes(world: dict[str, object], ticks: int, window: int) -> tuple[list[int], list[int]]:
    """The push each content took over the last `window` ticks, the books
    asserted at every tick; the held momentum is the sum of the pushes."""
    simulation = ShadowSimulation(parse_shadow_world(world))
    before: dict[int, list[int]] = {}
    for tick in range(1, ticks + 1):
        simulation.step()
        books = simulation.books()
        assert books["balanced"], (tick, books)
        assert books["momentum"]["held"] == [
            sum(holder.pushed[axis] for holder in simulation.holders.values()) for axis in range(3)
        ]
        if tick == ticks - window:
            before = {number: list(holder.pushed) for number, holder in simulation.holders.items()}
    first, second = simulation.holders[1], simulation.holders[2]
    return (
        [a - b for a, b in zip(first.pushed, before[1], strict=True)],
        [a - b for a, b in zip(second.pushed, before[2], strict=True)],
    )


def test_two_contents_push_each_other_equally_and_the_product_law_holds():
    """(c): 21^3, d = 8, 200 ticks, the window ticks 101 to 200."""
    shape, distance, ticks, window = 21, 8, 200, 100
    first, second = pushes(pair(shape, distance, CONTENT, 1 << 22, ticks), ticks, window)
    # The third law by symmetry: equal and opposite along the line, toward each
    # other (the first content, at the lower x, pushed toward +x) within 5 %
    # (the mean field's 0.3 to 1.9 %, round 8 section 55 (ii), and the
    # rounding of whole units per window at N = 64, round 7 section 47 (ii)),
    # the transverse parts below 3 % of the axial.
    assert first[0] > 0 > second[0]
    assert abs(first[0] + second[0]) < 0.05 * first[0], (first, second)
    for push in (first, second):
        assert abs(push[1]) < 0.03 * abs(push[0]) and abs(push[2]) < 0.03 * abs(push[0]), push
    # The magnitude against M_B rho M_A/(4 pi d^2): the free field read at a
    # holder on the axis at d = 8 is 1.08 of the law in the mean field with a
    # sponge edge (round 8 section 55 (i)); on this open board the edge's
    # mirror ripples the per-Node push by +-2 R r / (2 H - r), +-36 % at r = 8
    # on 21^3, with the anisotropy on top (round 7 section 46 (iii)): between
    # 0.4 and 1.6 of the law; the law is read in the shell mean of (b).
    law = CONTENT * CONTENT * (6 / 128) / (4 * math.pi * distance * distance) * window
    assert 0.4 < first[0] / law < 1.6, first[0] / law
    # The product law: both contents doubled with the clock doubled (the same
    # period), the push four times within 5 %.
    doubled, _ = pushes(pair(shape, distance, 2 * CONTENT, 1 << 23, ticks), ticks, window)
    assert abs(doubled[0] / first[0] - 4) < 0.05 * 4, doubled[0] / first[0]


def screen_profile(world: dict[str, object], ticks: int) -> list[float]:
    """The marks' light counts by y, summed over z, smoothed by a running mean
    over three marks."""
    simulation, _ = run(world, ticks)
    extent_y = world["shape"][1]  # type: ignore[index]
    assert isinstance(extent_y, int)
    counts = [0] * extent_y
    for holder in simulation.holders.values():
        if holder.position[0] == 17:
            counts[holder.position[1]] += holder.absorbed[0]["keep"]
    assert sum(counts) > 0
    return [
        (counts[max(y - 1, 0)] + counts[y] + counts[min(y + 1, extent_y - 1)]) / 3
        for y in range(extent_y)
    ]


def extrema(
    profile: list[float], centre: int, near: tuple[int, int], far: tuple[int, int]
) -> tuple[float, float]:
    """The lowest value at a distance from the centre within `near` and the
    highest within `far`, on the side of larger y."""
    low = min(profile[centre + d] for d in range(near[0], near[1] + 1))
    high = max(profile[centre + d] for d in range(far[0], far[1] + 1))
    return low, high


def test_two_slits_give_a_minimum_and_a_maximum_away_from_the_axis():
    """(d): the reading of the marks over 200 intervals against the one-slit
    control; the pattern is symmetric about the axis."""
    ticks = 200
    two = screen_profile(slits(2, ticks), ticks)
    one = screen_profile(slits(1, ticks), ticks)
    centre = 20
    for profile in (two, one):
        for d in range(1, 13):
            assert abs(profile[centre + d] - profile[centre - d]) <= 0.05 * profile[centre] + 1, d
    # Two slits 14 apart, the screen 9 behind them, the wavelength 16/sqrt 3
    # Links: the first minimum near 4 from the axis and the first maximum
    # beyond it near 8.5, the maximum at least 1.1 times the minimum; the
    # one-slit control falls from the axis outward without such a rise.
    low, high = extrema(two, centre, (2, 5), (6, 11))
    assert high > 1.1 * low, (low, high, two)
    low_one, high_one = extrema(one, centre, (2, 5), (6, 11))
    assert high_one < 1.1 * low_one, (low_one, high_one, one)


def test_a_content_near_a_mass_waits_and_the_slowdown_falls_as_one_over_r():
    """(e): 29^3, nine probes, 300 ticks, the fraction of intervals waited over
    ticks 101 to 300."""
    shape, ticks, window = 29, 300, 200
    simulation = ShadowSimulation(parse_shadow_world(probes(shape, ticks)))
    before: dict[int, int] = {}
    for tick in range(1, ticks + 1):
        simulation.step()
        assert simulation.books()["balanced"], tick
        if tick == ticks - window:
            before = {number: holder.waited for number, holder in simulation.holders.items()}
    # The mass reads only its own field, which it does not read: no wait, its
    # clock four steps per interval; a probe's clock does not turn (1 / K).
    mass = simulation.holders[1]
    assert mass.waited == 0 and mass.phase_steps == 4 * ticks
    fractions = []
    radii = []
    for index, (x, y, z) in enumerate(PROBES):
        probe = simulation.holders[index + 2]
        assert probe.phase_steps == 0 and probe.absorbed[0]["rerelease"] == 0
        fractions.append((probe.waited - before[index + 2]) / window)
        radii.append(math.sqrt(x * x + y * y + z * z))
    # The size 3 x 0.2143 sqrt(q)/r in 32nds at 1 / 512 per unit: 0.28 at r = 4,
    # 0.14 at 8, 0.09 at 12, rippled per Node; every fraction between 0.03 and
    # 0.5, the log-log slope over the nine probes nearer -1 than -2.
    assert all(0.03 < value < 0.5 for value in fractions), fractions
    fitted = slope(radii, fractions)
    assert -1.5 < fitted < -0.5, (fitted, fractions)


def bar(momentum: int, ticks: int) -> dict[str, object]:
    """A content of 2^24 at x = 4 on a 41 x 9 x 9 bar, given a momentum along
    +x, free to step, no wait."""
    world = one_content(41, ticks, wait=0)
    world["model_id"] = "field-only-test-step"
    world["shape"] = [41, 9, 9]
    world["contents"] = [
        {"position": [4, 4, 4], "family": "m", "amount": CONTENT, "momentum": [momentum, 0, 0]}
    ]
    return world


def test_a_content_with_momentum_steps_by_its_accumulators_and_its_own_field_pushes_nothing():
    """(h): 60 intervals on the bar, p = M/16 and p = M."""
    ticks = 60
    for momentum, expected_steps, expected_ticks in (
        (CONTENT // 16, 3, [16, 33, 50]),
        (CONTENT, 30, [1, 3, 5, 7, 9, 11]),
    ):
        simulation = ShadowSimulation(parse_shadow_world(bar(momentum, ticks)))
        stepped = []
        for tick in range(1, ticks + 1):
            simulation.step()
            assert simulation.books()["balanced"], tick
            if simulation.holders[1].position[0] != 4 + len(stepped):
                stepped.append(tick)
        holder = simulation.holders[1]
        # The accumulator gives back the content at every step and the momentum
        # stays what it was given: the own field pushes nothing (section 54 (i)).
        assert holder.steps == expected_steps and holder.position == (4 + expected_steps, 4, 4)
        assert holder.momentum == [momentum, 0, 0] and holder.pushed == [0, 0, 0]
        # T2: a step every 17 intervals at p = M/16 (the sixteenth interval
        # fills the accumulator, the interval after a step is the event's), and
        # every second interval at p = M, the cap of a half Link per interval.
        assert stepped[: len(expected_ticks)] == expected_ticks, stepped
        assert holder.held == [CONTENT] and holder.absorbed[0]["read"] == 0


def test_the_mode_refuses_the_old_keys_and_the_old_engine_refuses_the_law(tmp_path):
    """(f): the refusals, both ways, and the runner's switches."""
    world = one_content(11, 4)
    with pytest.raises(ValueError, match="unknown keys.*law"):
        parse_initial_state(world)
    ring = json.loads((ROOT / "examples/nature/ring.json").read_text(encoding="utf-8"))
    with pytest.raises(ValueError, match=f"{SHADOW_LAW}.*old engine's keys"):
        parse_shadow_world(ring)
    for key in ("schema_version", "dense_field", "initial_field", "wait_reads", "shadow_wait"):
        with pytest.raises(ValueError, match=f"{SHADOW_LAW}.*{key}"):
            parse_shadow_world({**world, key: 1})
    with pytest.raises(ValueError, match="closed board is refused"):
        parse_shadow_world({**world, "boundary": "periodic"})
    with pytest.raises(ValueError, match='"law": "shadow"'):
        parse_shadow_world({key: value for key, value in world.items() if key != "law"})
    with pytest.raises(ValueError, match="unknown keys: prefill"):
        parse_shadow_world({**world, "prefill": 3})
    with pytest.raises(ValueError, match="below K x N"):
        parse_shadow_world(
            {**world, "contents": [{"position": [1, 1, 1], "family": "m", "amount": 1 << 28}]}
        )
    with pytest.raises(ValueError, match="a lamp is a held content of a paid family"):
        parse_shadow_world(
            {
                **world,
                "contents": [{"position": [1, 1, 1], "family": "m", "amount": 4, "lamp": {"rate": 1}}],
            }
        )
    with pytest.raises(ValueError, match="two contents at one Node"):
        parse_shadow_world(
            {
                **world,
                "contents": [
                    {"position": [1, 1, 1], "family": "m", "amount": 4},
                    {"position": [1, 1, 1], "family": "m", "amount": 4},
                ],
            }
        )
    with pytest.raises(ValueError, match="must be one of"):
        parse_shadow_world(
            {
                **world,
                "contents": [
                    {"position": [1, 1, 1], "family": "m", "amount": 4, "table": {"m": "return"}}
                ],
            }
        )
    with pytest.raises(ValueError, match="power of two"):
        parse_shadow_world({**world, "N": 48})
    parsed = parse_shadow_world(world)
    assert parsed.owners(0) == (1,) and parsed.wait == (1, 1) and parsed.release == (1, 128)
    # The runner: the record of a run, and its refusal of the old switches.
    path = tmp_path / "world.json"
    path.write_text(json.dumps(world), encoding="utf-8")
    record = json.loads(run_initialization(path, tmp_path / "run").read_text(encoding="utf-8"))
    assert record["law"] == SHADOW_LAW and record["status"] == "completed"
    assert record["completed_ticks"] == 4 and record["conserved_at_every_completed_tick"] is True
    assert len(record["audit"]) == 4 and record["contents"][0]["content"] == CONTENT
    assert (tmp_path / "run" / "state.json").exists() and (tmp_path / "run" / "events.jsonl").exists()
    state = json.loads((tmp_path / "run" / "state.json").read_text(encoding="utf-8"))
    assert state["law"] == SHADOW_LAW and state["tick"] == 4 and state["nodes"]
    with pytest.raises(ValueError, match="headless and alone"):
        run_initialization(path, tmp_path / "dense", dense_field=True)


@pytest.mark.parametrize("modulus", [2, 8, 64, 256, 4096])
def test_the_nearest_step_of_the_layer_is_the_engines_argmax(modulus):
    """(g): the windowed nearest step equals the argmax over the whole circle,
    the first on a tie, on random sums and on directions exactly on and
    between the steps; the window is 1 up to N = 64, 4 at 256, 69 at 4096."""
    assert step_window(64) == 1 and step_window(256) == 4 and step_window(4096) == 69
    cosines = np.array(phase_cosines(modulus), dtype=np.int64)
    sines = np.array(phase_sines(modulus), dtype=np.int64)
    generator = np.random.default_rng(modulus)
    steps = np.arange(modulus)
    for scale in (1, 100, 10**9):
        x = generator.integers(-scale, scale + 1, size=4000)
        y = generator.integers(-scale, scale + 1, size=4000)
        between = (steps + 0.5) * 2 * np.pi / modulus
        on = steps * 2 * np.pi / modulus
        x = np.concatenate(
            [x, np.rint(scale * np.cos(between)), np.rint(scale * np.cos(on)), [0]]
        ).astype(np.int64)
        y = np.concatenate(
            [y, np.rint(scale * np.sin(between)), np.rint(scale * np.sin(on)), [0]]
        ).astype(np.int64)
        expected = np.argmax(x[:, None] * cosines + y[:, None] * sines, axis=-1)
        assert np.array_equal(nearest_step(cosines, sines, x, y), expected)
