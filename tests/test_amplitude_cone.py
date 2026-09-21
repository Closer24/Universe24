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
(d) the exact phase at the click (2026-09-21, BEAM_LAW note 42): under the
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

import pytest

from event_universe.events import NatureBeamSimulation, parse_nature_beam_world

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
    assert expectation["same_age"] is True
    assert expectation["age_at_click"] == {"axis": 29, "diagonal": 29}
    assert expectation["links"] == {"axis": 17, "diagonal": 24}
    assert expectation["cone_links"]["path_phase"] == {"axis": 51, "diagonal": 8}
    assert expectation["cone_intervals"]["path_phase"] == {"axis": 23, "diagonal": 23}
    assert expectation["exact"]["cone_intervals"] == {  # (d)
        "path_phase": {"axis": 23, "diagonal": 23},
        "remainder": {"axis": [42, 64], "diagonal": [96, 128]},
    }
    assert expectation["exact"]["cone_links"]["path_phase"] == {"axis": 51, "diagonal": 8}
