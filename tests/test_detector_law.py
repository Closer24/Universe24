"""The local detector law (`detector-law-v1`, docs/designs/detector_law/DESIGN.md),
the build's first gate: the loader's key and refusals, the rule's step against
the design's integers, and one chain world run headless (a lamp at one end,
a receiver at the other, the open face behind the lamp): one click per
record, the books balanced at every tick, the click's time at the front's
first rung about L / c after the birth, the click line with the stamp."""

from __future__ import annotations

import numpy as np
import pytest

from event_universe.events.detector_law import UNIT, DetectorLawSimulation
from event_universe.events.world import DETECTOR_LAW_RULE, parse_nature_beam_world


def chain_world(train: int = 4, clock_stamp: bool = True) -> dict:
    """A chain of 80 Nodes (y and z periodic, one layer each; x open): the
    lamp's body at x = 2, a receiver body at x = 70 read as the set
    `screen`; the light family's clock the pair [77, 25] on N = 64 (3.08
    steps per interval, the period 20.78 intervals, lambda = 12 Links)."""
    return {
        "law": "beam",
        "model_id": "beam-detector-law-chain-v1",
        "shape": [80, 1, 1],
        "boundary": {"x": "open", "y": "periodic", "z": "periodic"},
        "ticks": 400,
        "K": 1073741824,
        "N": 64,
        "release": [1, 128],
        "suspension": 0,
        "clock_stamp": clock_stamp,
        "detector_law": True,
        "directions": [],
        "families": [{"name": "light", "quantum": 1, "phase_per_link": [77, 25]}],
        "measured": [
            {
                "position": [2, 0, 0],
                "family": "light",
                "amount": 6,
                "phase": 0,
                "momentum": [0, 0, 0],
                "fixed": True,
                "directions": [[1, 0, 0]],
                "lamp": {
                    "rate": [1, 40],
                    "wheel": [2531, 4096],
                    "directions": [[1, 0, 0]],
                    "train": train,
                },
            },
            {
                "position": [70, 0, 0],
                "family": "light",
                "amount": 1,
                "phase": 0,
                "momentum": [0, 0, 0],
                "fixed": True,
                "directions": [[-1, 0, 0]],
            },
        ],
        "detectors": [{"name": "screen", "positions": [[70, 0, 0]], "threshold": 1}],
    }


def test_the_loader_admits_the_key_and_refuses_the_ray_laws_instruments():
    world = parse_nature_beam_world(chain_world())
    assert world.detector_law
    assert DETECTOR_LAW_RULE in world.hypotheses
    assert world.measured[0].lamp is not None and world.measured[0].lamp.train == 4
    with_turns = chain_world()
    with_turns["measured"][0]["lamp"]["turns"] = [3]
    with pytest.raises(ValueError, match="turns is refused under detector-law-v1"):
        parse_nature_beam_world(with_turns)
    integer_clock = chain_world()
    integer_clock["families"][0]["phase_per_link"] = 3
    with pytest.raises(ValueError, match="pair form of phase_per_link"):
        parse_nature_beam_world(integer_clock)


def test_the_rule_is_the_designs_integers_on_a_chain():
    """One step of the engine's rule equals the design's line
    3 a_next + r' = a_E + a_W + 4 a - 3 a_before + r on a one-layer chain
    (the y and z neighbours the row itself), with the remainder kept."""
    world = parse_nature_beam_world(chain_world())
    simulation = DetectorLawSimulation(world)
    rng = np.random.default_rng(7)
    now = rng.integers(-UNIT, UNIT, size=(80, 1, 1), dtype=np.int64)
    before = rng.integers(-UNIT, UNIT, size=(80, 1, 1), dtype=np.int64)
    remainder = rng.integers(0, 3, size=(80, 1, 1), dtype=np.int64)
    total = simulation._neighbours(now) - 3 * before + remainder
    expected = np.zeros_like(now)
    for x in range(80):
        left = now[x - 1, 0, 0] if x > 0 else 0
        right = now[x + 1, 0, 0] if x < 79 else 0
        expected[x, 0, 0] = left + right + 4 * now[x, 0, 0] - 3 * before[x, 0, 0] + remainder[x, 0, 0]
    assert np.array_equal(total, expected)
    nxt = np.floor_divide(total, 3)
    assert np.array_equal(total - 3 * nxt, np.mod(total, 3))


def test_a_chain_world_clicks_once_per_record_with_the_books_balanced():
    world = parse_nature_beam_world(chain_world())
    lines: list[dict] = []
    simulation = DetectorLawSimulation(world, observer=lines.append)
    for _ in range(600):
        simulation.step()
        assert simulation.books()["balanced"], simulation.tick
    births = [line for line in lines if line["event"] == "birth"]
    gathers = [line for line in lines if line["event"] == "gather"]
    # the lamp's stock of 6 units, one record per 40 intervals; a record that
    # clicks back at the lamp (a detector at rest) returns its unit to the stock
    assert 6 <= len(births) <= 9
    assert len(gathers) + len(simulation.records) == len(births)
    assert len(gathers) >= 4
    assert all("clock" in g and "birth" in g and "click" in g for g in gathers)
    for gather in gathers:
        assert gather["chosen"] is None or gather["chosen"][0][0] in {"screen", "face:-x", "measured:1"}
        if gather["chosen"] is not None and gather["chosen"][0][0] == "screen":
            flight = gather["click"] - gather["birth"]
            # the front's first rung about L / c = 68 / 0.577 = 118 intervals after the birth
            assert 104 <= flight <= 132, flight
    books = simulation.books()["families"]["light"]
    assert books["measured"]["measured"] + books["transit"]["escaped"] == len(gathers)
