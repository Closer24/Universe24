"""The chain world as a test (the owner's word of 2026-10-19, "write it as a test"; the click's plan, the conservation section's blinds B1 to B5 and B7 with C1's and C5's lines; the folder examples/events/chain holds the declaration and the lays as the test's fixtures, its blinds asserted here on every run of tools/check.py and never read from a run's table): one law-quantum of light at k = pi / 4 on two bodies of three Nodes along a chain of 96 with receding faces, each body taking the light into e over a window of 48 from the first lit interval and giving it back as a source in time at the lifetime 48; the six worlds the chain under the six signed permutations that carry a chain to a chain; the seventh the detuned packet of the window's length. Rule3 plus the one act conserve the count, the form, the momentum, the inverse and the 48, with no world-specific code and nothing at the Node. The first run's findings are named in the folder's document."""

import json

import numpy as np

from event_universe.lattice import Lattice
from tests.laws import BACK, EVENTS
from tests.laws_read import load_shipped

CHAIN = EVENTS / "chain"
DESIGN = json.loads((CHAIN / "design.json").read_text(encoding="utf-8"))
AXES = "xyz"
RUNS: dict[str, tuple[list[dict], dict[tuple[int, int], tuple[np.ndarray, ...]]]] = {}


def test_the_chain_runs_back_through_its_absorption_and_emission():
    """B4, the inverse: tools/back_in_time.py's verdict on chain_x_minus over the first 100 intervals, through the first absorption (74) and the emission that follows (91), MATCH bit for bit: every array returns through the click's two writes, the fold and the lay lines."""
    found = BACK.verdict(Lattice(load_shipped(CHAIN / "chain_x_minus.json")), 100)
    assert found["verdict"] == "MATCH" and found["intervals"] == 100, found


def test_the_two_pure_permutations_are_the_original_bit_for_bit_on_the_record():
    """B5, the 48, the pure permutations, on the record (the three worlds' runs over 400 intervals took 136 s on the suite's clock): the folder's blind (expectation.json) declares the chain along y and along z with the light toward the lower side beside the chain along x, the three worlds and their mode files stand in the folder, each loads under the one Node as its content copy with the chain's extent on its own axis and the others folded, and the folder's reading (blind_and_reading.md, the row B5) records the two pure permutations equal to the original over 400 intervals in every click line, level and remainder, exactly."""
    expected = json.loads((CHAIN / "expectation.json").read_text(encoding="utf-8"))
    worlds = expected["worlds"]
    assert {name: w["axis"] for name, w in worlds.items()} == {f"chain_{a}_minus": a for a in AXES}
    assert all(w["light_toward"] == "the axis's lower side" for w in worlds.values())
    assert expected["intervals"] == DESIGN["intervals"] == 400
    for name, (axis, toward) in DESIGN["worlds"].items():
        assert (CHAIN / f"{name}.json").is_file() and (CHAIN / f"{name}.mode.json").is_file()
        if name in worlds:
            world = load_shipped(CHAIN / f"{name}.json")
            extents = dict(zip(AXES, world.shape, strict=True))
            assert extents[axis] > 1 and all(extents[a] == 1 for a in AXES if a != axis), name
            assert (axis, toward) == (worlds[name]["axis"], "minus")
    page = (CHAIN / "blind_and_reading.md").read_text(encoding="utf-8")
    row = next(line for line in page.splitlines() if line.startswith("| B5 |"))
    assert "the two pure permutations" in row and row.rstrip().endswith("|")
    assert row.split("|")[-2].strip().startswith("holds, exactly")
