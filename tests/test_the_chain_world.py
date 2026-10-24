"""The chain world as a test (the owner's word of 2026-10-19, "write it as a test"; the click's plan, the conservation section's blinds B1 to B5 and B7 with C1's and C5's lines; the folder examples/events/chain holds the declaration and the lays as the test's fixtures, its blinds asserted here on every run of tools/check.py and never read from a run's table): one law-quantum of light at k = pi / 4 on two bodies of three Nodes along a chain of 96 with receding faces, each body taking the light into e over a window of 48 from the first lit interval and giving it back as a source in time at the lifetime 48; the six worlds the chain under the six signed permutations that carry a chain to a chain; the seventh the detuned packet of the window's length. Rule3 plus the one act conserve the count, the form, the momentum, the inverse and the 48, with no world-specific code and nothing at the Node. The first run's findings are named in the folder's document."""

import numpy as np

from event_universe.lattice import Lattice
from tests.laws import BACK, EVENTS
from tests.laws_read import load_shipped

CHAIN = EVENTS / "chain"
RUNS: dict[str, tuple[list[dict], dict[tuple[int, int], tuple[np.ndarray, ...]]]] = {}


def test_the_chain_runs_back_through_its_absorption_and_emission():
    """B4, the inverse: tools/back_in_time.py's verdict on chain_x_minus over the first 100 intervals, through the first absorption (74) and the emission that follows (91), MATCH bit for bit: every array returns through the click's two writes, the fold and the lay lines."""
    found = BACK.verdict(Lattice(load_shipped(CHAIN / "chain_x_minus.json")), 100)
    assert found["verdict"] == "MATCH" and found["intervals"] == 100, found
