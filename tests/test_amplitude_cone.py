"""The cone worlds of series L7 (`examples/events/amplitude/make_worlds.py`,
`expectations.json` under `cone`; the register's L7 entry): which length a
row's phase counts. Two lamps of one world, one on the heading +x to a
counter 17 Links away, one on the plane diagonal (1, 1, 0) to a counter
24 Links along the staircase at the same Euclidean distance to one
percent; `cone_links` declares the integer form of `phase_per_link` (3 per
Link stepped), `cone_intervals` the pair form [3, 1] (3 per interval of
age). The expected integers of docs/TEST_EXPECTATIONS.md ("The amplitude
law: the cone"), written down before the run:

(a) the flight: every record's row clicks at its counter at the age 29 in
    both worlds (the flight table's m(29) = 17 on +x and 24 on the
    diagonal, BEAM_LAW section 3), 29 intervals after its birth;
(b) the path phase phase - u at the click: 51 at the axis and 8 at the
    diagonal under the integer form (3 x 17 and 3 x 24 mod 64), 23 at
    both under the pair form (3 x 29 mod 64);
(c) one gather per record, one cell each, as many at each counter; the
    expectation file's pins equal the flight formula's;
(d) the exact phase at the click (2026-09-21, BEAM_LAW note 45): under the
    pair form the click line's `exact` less u is the whole part of
    3 x made x T_d over S_1 Q modulo N with its `remainder` over S_1 Q,
    3 x 17 x 110 = 5610 = 87 x 64 + 42 at the axis (23, [42, 64]) and
    3 x 24 x 156 = 11232 = 87 x 128 + 96 at the diagonal (23, [96, 128]):
    the same whole part as the walk's 3 x 29 = 87 (the design's 41.75 and
    42.00 are the rate 8's, `tests/test_exact_phase.py`); under the integer
    form no `exact` is written, the phase being exact per Link.
"""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pytest

from event_universe.events import NatureBeamSimulation, parse_nature_beam_world
from event_universe.events.nature_beam import nature_beam_tables
from event_universe.events.world import LABEL_SCALE

ROOT = Path(__file__).resolve().parents[1]
WORLDS = ROOT / "examples" / "events" / "amplitude"
N = 64


def observed(name: str) -> list[dict[str, object]]:
    world = json.loads((WORLDS / f"{name}.json").read_text(encoding="utf-8"))
    lines: list[dict[str, object]] = []
    simulation = NatureBeamSimulation(parse_nature_beam_world(world), observer=lines.append)
    for _ in range(int(world["ticks"])):  # type: ignore[call-overload]
        simulation.step()
    return lines


@pytest.fixture(scope="module")
def expectation() -> dict[str, object]:
    found: dict[str, object] = json.loads((WORLDS / "expectations.json").read_text(encoding="utf-8"))[
        "cone"
    ]
    return found


@pytest.mark.parametrize("name", ["cone_links", "cone_intervals"])
def test_the_age_and_the_path_phase_at_the_click(name: str, expectation: dict) -> None:
    lines = observed(name)
    births = {line["record"]: line for line in lines if line["event"] == "birth"}
    clicks = [line for line in lines if line["event"] == "click"]
    gathers = [line for line in lines if line["event"] == "gather"]
    assert len(clicks) == len(gathers) > 0
    seen = {"axis": 0, "diagonal": 0}
    for click in clicks:
        birth = births[click["record"]]
        detector = click["detector"]
        assert click["age"] == expectation["age_at_click"][detector]  # (a)
        assert click["tick"] - birth["tick"] == expectation["age_at_click"][detector]
        assert (click["phase"] - birth["u"]) % N == expectation[name]["path_phase"][detector]  # (b)
        exact = expectation["exact"][name]
        if name == "cone_intervals":  # (d)
            assert (click["exact"] - birth["u"]) % N == exact["path_phase"][detector]
            assert click["remainder"] == exact["remainder"][detector]
        else:
            assert "exact" not in click and "remainder" not in click
        seen[detector] += 1
    assert seen["axis"] == seen["diagonal"] > 0  # (c)
    assert all(len(gather["chosen"]) == 1 for gather in gathers)


def test_the_pins_are_the_flight_formula(expectation: dict) -> None:
    """The register's numbers derived from the worlds and the flight table
    (since 2026-09-21 no literal of a world's number here): per detector
    the Manhattan Links from its lamp, the first age at which the lamp's
    direction has walked them (the flight table), one age for both; the
    path phase (phase per Link x Links) mod N under the integer form and
    (phase per interval x age) mod N under the pair form."""
    worlds = {
        name: json.loads((WORLDS / f"{name}.json").read_text(encoding="utf-8"))
        for name in ("cone_links", "cone_intervals")
    }
    parsed = parse_nature_beam_world(worlds["cone_links"])
    flight = nature_beam_tables(parsed).flight
    world = worlds["cone_links"]
    lamps = [event for event in world["measured"] if "lamp" in event]
    detectors = {detector["name"]: detector["positions"][0] for detector in world["detectors"]}
    links: dict[str, int] = {}
    ages: dict[str, int] = {}
    headings: dict[str, int] = {}
    for name, position in detectors.items():
        # The lamp whose one direction's line reaches the detector: the
        # offset is a positive multiple of the direction.
        for lamp in lamps:
            direction = lamp["lamp"]["directions"][0]
            offset = [position[axis] - lamp["position"][axis] for axis in range(3)]
            axis = next(a for a in range(3) if direction[a])
            multiple = offset[axis] // direction[axis]
            if multiple >= 1 and offset == [multiple * c for c in direction]:
                break
        else:
            raise AssertionError(name)
        links[name] = sum(abs(c) for c in offset)
        heading = parsed.directions.index(tuple(direction))
        headings[name] = heading
        candidates = np.arange(1, 200, dtype=np.int64)
        walked = flight.manhattan_steps(np.full(candidates.shape, heading, dtype=np.int64), candidates)
        ages[name] = int(candidates[walked >= links[name]][0])
    assert expectation["links"] == links
    assert expectation["age_at_click"] == ages
    assert expectation["same_age"] is (len(set(ages.values())) == 1)
    per_link = worlds["cone_links"]["families"][0]["phase_per_link"]
    assert expectation["cone_links"]["path_phase"] == {
        name: (per_link * links[name]) % N for name in detectors
    }
    numerator, denominator = worlds["cone_intervals"]["families"][0]["phase_per_link"]
    assert expectation["cone_intervals"]["path_phase"] == {
        name: (ages[name] * numerator // denominator) % N for name in detectors
    }
    # (d) The exact phase at the click (BEAM_LAW note 46): under the pair
    # form the whole part and the remainder of n x Links x T_d over
    # d x S_1 x Q (the flight table's resolution and Manhattan length, the
    # label scale Q), the whole part mod N; the integer form's `exact` the
    # path phase itself with the remainder 0 over 1.
    exact = expectation["exact"]
    assert exact["cone_links"]["path_phase"] == expectation["cone_links"]["path_phase"]
    assert exact["cone_links"]["remainder"] == {name: [0, 1] for name in detectors}
    for name in detectors:
        heading = headings[name]
        s1 = int(flight.manhattan[heading])
        resolution = int(flight.resolution[heading])
        whole, rest = divmod(numerator * links[name] * resolution, denominator * s1 * LABEL_SCALE)
        assert exact["cone_intervals"]["path_phase"][name] == whole % N
        assert exact["cone_intervals"]["remainder"][name] == [rest, s1 * LABEL_SCALE]
