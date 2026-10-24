"""Every Link's phase pair stands on the one orbit from the seed (features/phase `Orbit`, node.phase_carried; the architect's round of 2026-10-24): the pair at a count is the checkpoint at or below it, or the Link's own pair where that is nearer, carried by the rest, the same integers as the acts one by one from the seed; the folded Universe24 over 32 intervals writes its shipped eras, nodes and clicks lines bit for bit, and 30 intervals of it with the pairs carried act by act hold the same phase lines (the born pairs sourcing the holder from 30)."""

import json
from pathlib import Path
from typing import Any

import numpy as np
import pytest

from event_universe import node
from event_universe.features import phase
from event_universe.lattice import Lattice
from event_universe.world_files import load_world
from tests.laws_universe import ERAS, FOLDER, LOG, WORLD

INTERVALS, COMPARED, GAMMA, WIDTH = 32, 30, 1000, 63
COUNTS = (0, 1, 2, 255, 256, 257, 511, 512, 1000, 3000)


def lines_of(path: Path, limit: int | None = None) -> list[dict[str, Any]]:
    """The log's lines without the clock (`seconds`), the lines up to the interval `limit` where one is given."""
    found = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()]
    for line in found:
        line.pop("seconds", None)
    return [line for line in found if limit is None or line.get("interval", 0) <= limit]


def lines_over(pairs: list[Any]) -> Any:
    """Pairs given per count laid as the pair of lines over the counts, one array per integer."""
    return tuple(
        tuple(np.array([p[line][part] for p in pairs], dtype=object) for part in range(3))
        for line in range(2)
    )


def test_the_orbits_pair_at_a_count_is_the_acts_from_the_seed() -> None:
    unit, amplitude = phase.unit(GAMMA), phase.amplitude(phase.unit(GAMMA), WIDTH)
    orbit, seed = phase.Orbit(unit, amplitude), phase.seed(amplitude, unit)
    counts, zeros = np.array(COUNTS, dtype=object), np.zeros(len(COUNTS), dtype=object)
    from_checkpoints = orbit.pairs_at(counts, zeros, lines_over([seed] * len(COUNTS)), object)
    below = [phase.iterate(seed, max(count - 1, 0), unit) for count in COUNTS]  # the pairs one act below
    from_near = orbit.pairs_at(counts, np.maximum(counts - 1, 0), lines_over(below), object)
    for k, count in enumerate(COUNTS):
        pair = phase.iterate(seed, count, unit)
        for found in (from_checkpoints, from_near):
            assert [int(a[k]) for line in found for a in line] == [int(a) for line in pair for a in line]
    assert orbit.reached == max(COUNTS)
    assert (
        sorted(orbit.checkpoints) == list(range(0, max(COUNTS) + 1, phase.SPACING))
        and phase.SPACING == 128
    )


def test_the_folded_universe_writes_its_shipped_logs_over_32_intervals(tmp_path: Path) -> None:
    ERAS.run(WORLD, tmp_path / "e.jsonl", 10**6, INTERVALS, tmp_path / "c.jsonl", tmp_path / "n.jsonl")
    assert lines_of(tmp_path / "e.jsonl")[1:] == lines_of(LOG)[1 : INTERVALS + 1]
    assert lines_of(tmp_path / "n.jsonl") == lines_of(FOLDER / "universe24.nodes.jsonl")[:INTERVALS]
    assert lines_of(tmp_path / "c.jsonl") == lines_of(FOLDER / "universe24.clicks.jsonl", INTERVALS)


def phases_of(board: Lattice) -> list[list[list[int]]]:
    """Every holder's phase lines as Python's integers."""
    return [
        [
            [
                int(x)
                for a in (line.now, line.before, line.remainder)
                for x in np.asarray(a, dtype=object).reshape(-1)
            ]
            for line in row
        ]
        for state in board.states
        for row in state.phases
    ]


def test_the_pairs_on_the_orbit_are_the_pairs_carried_act_by_act(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    act_by_act = Lattice(load_world(WORLD), output=lambda line: None)
    on_orbit = Lattice(load_world(WORLD), output=lambda line: None)
    real = phase.orbit_of
    monkeypatch.setattr(  # the former path for act_by_act's states alone, through the loop
        node.phase,
        "orbit_of",
        lambda state: None if any(state is s for s in act_by_act.states) else real(state),
    )
    rotating = [s for s, f in zip(on_orbit.states, on_orbit.families, strict=True) if f.rotation]
    assert rotating and all(real(s) is not None for s in rotating)  # on_orbit's holders on the orbit
    for _ in range(COMPARED):
        on_orbit.step()
        act_by_act.step()
        assert phases_of(on_orbit) == phases_of(act_by_act)
    assert any(any(x for line in row for x in line) for row in phases_of(on_orbit))
