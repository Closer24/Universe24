"""Gathered gravity probe: a claim gathers a train's pull whole, closed, on a small world."""

import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "gathered_gravity_probe", ROOT / "examples/gathered-gravity/run_experiments.py"
)
PROBE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(PROBE)


def test_a_claim_multiplies_the_pull_of_the_crossing_rays_and_the_world_closes():
    plain = PROBE.pull(PROBE.document(3, False, ticks=16, headings=128, size=13))
    claimed = PROBE.pull(PROBE.document(3, True, ticks=16, headings=128, size=13))
    assert plain["quanta_closed"] and claimed["quanta_closed"]
    # The plain body pays only for the rays that cross its Node; the claiming body
    # gathers the rest of each train the flood still reaches, pays for all of it,
    # and is pulled far harder than its own line's share.
    assert 0 < plain["paid"] < claimed["paid"]
    assert claimed["pull_per_tick"] > 4 * plain["pull_per_tick"] > 0
    assert all(gain > 0 for gain in claimed["last_gains"])
