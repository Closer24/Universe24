"""The worlds of record (examples/events/experiments, the universe of record): every Bell world loads with the mode file beside it under the three held rows of the file, gravity and the free charge as the sum at their divisor and the bound charge `polarisation` at the pair [1, 2] and the divisor 1, each with a record of its own; the bound charge's level at the load is the start folder's rest, a GameBoard diagnostic read here and labelled so: above 0 at every body's Node and nowhere above the largest count (the rest's line 12 a = S_6(a) + 6 sigma at [1, 2] bounds a by the largest source), and 0 beyond the reach of every body (the sum of the sources times the pair's decay per Link below one unit; ALGEBRA.md "The well": kappa^2 = 6 den / num - 6, the decay per Link the root of lambda + 1 / lambda = 2 + kappa^2)."""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pytest
from scipy.ndimage import distance_transform_cdt

from event_universe.events.detector_law import DetectorLawSimulation
from event_universe.world_files import load_world

BELL = Path(__file__).resolve().parents[1] / "examples" / "events" / "experiments" / "bell"


@pytest.mark.parametrize("name", sorted(p.stem for p in BELL.glob("*.json") if "." not in p.stem))
def test_a_bell_world_of_record_loads_with_the_three_held_records(name: str):
    document = json.loads((BELL / f"{name}.json").read_text(encoding="utf-8"))
    simulation = DetectorLawSimulation(load_world(BELL / f"{name}.json"))
    held = {simulation.families[f].name: simulation.held_records[f] for f in simulation.held_families}
    universe = json.loads((BELL.parents[0] / "universe.json").read_text(encoding="utf-8"))
    rows = {row["name"]: row for row in universe["families"] if row.get("held")}
    assert set(held) == set(rows) and len({id(record) for record in held.values()}) == len(rows)
    num, den = rows["polarisation"]["pair"]
    edge = 2 + 6 * den / num - 6  # 2 + kappa^2: the decay per Link is the root of x + 1 / x = edge
    decay, level = (edge - (edge**2 - 4) ** 0.5) / 2, held["polarisation"].now
    nodes = [node for entry in document["measured"] for node in entry["nodes"]]
    occupied, total, largest = np.zeros(level.shape, dtype=bool), 0, max(node["count"] for node in nodes)
    for node in nodes:
        occupied[tuple(node["node"])], total = True, total + node["count"]
        assert 0 < level[tuple(node["node"])] <= largest  # the wells of the bodies' counts, GameBoard
    distances = distance_transform_cdt(~occupied, metric="taxicab")
    farthest = np.unravel_index(np.argmax(distances), level.shape)
    assert total * decay ** int(distances[farthest]) < 1 and abs(int(level[farthest])) <= 1
