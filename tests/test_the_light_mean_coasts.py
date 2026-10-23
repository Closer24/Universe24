"""The light mean's coasting (ALGEBRA.md, the light family's declaration under A family's declaration, the clause of 2026-10-23, the light hand's derivation at the Node): for the massless pair S_i + SUM_j R_ij = 2 w at every Node whatever its paces, so at a level uniform over a Node and its six neighbours Rule3's numerator is w (2 L - a_before) + r, the step a_next = 2 L - a_before exact with the remainder carried unchanged, the double root at k = 0; the velocity v is a first integral and the level L_0 + v t a straight line in the interval count, bounded by nothing in the law. The clauses: (1) on the 3-cube torus the uniform light level drifts at exactly v at every Node at every interval, bit for bit, the remainder standing at the half wall; (2) the level is a gauge read by nothing: the same world laid at the seed's level with the same velocity has the same share, quanta and remainders at every Node (the click's hazard reads the share and the draw the remainders), the share 3 den v^2 per Node, the velocity's form and not the level's, and the time line stands; (3) the run back 40 of 40 exact; (4) on the gapped torus where every Node turns at one interval the light row's levels after the fire retrace the rise, the T-image bit for bit (the level now at t* + k the level before at t* - 1 - k, the velocity -v), and the run back through the fire is exact; (5) the massless board fires nowhere."""

import json
from pathlib import Path
from typing import Any

import numpy as np
import pytest

from event_universe import records, world_files
from event_universe.core import paces
from event_universe.core.rule3 import wall_of
from event_universe.lattice import Lattice
from event_universe.world_files import input_digest, load_world
from tests.laws import board_state, same_state

GAMMA, ACTION, CUBE, LEVEL, SPEED = 1000, 36000, 3, 500, 7
HELD = {"sources": ["form", "tensions"], "level_weight": 1, "write_weight": 1}


def light_world(folder: Path, gap: int, dust: int, amplitude: int) -> Path:
    """The 3-cube torus with gravity's pair [gap, Gamma], light [Gamma, Gamma] reading it as the big bang declares it, and, where `dust` is given, dust [0, Gamma] laid uniform at the band's rest rotation (the swap test's lay at a smaller amplitude)."""
    families: list[dict[str, Any]] = [
        {"name": "gravity", "pair": [gap, GAMMA], "reads": {"gravity": 1}, "held": HELD},
        {"name": "light", "pair": [GAMMA, GAMMA], "reads": {"gravity": 1}, "dimension": 1},
    ]
    if dust:
        families.append({"name": "dust", "pair": [0, GAMMA], "reads": {"gravity": 1}, "dimension": 1})
    universe: dict[str, Any] = {
        "integers": {"node_clock": GAMMA, "quantum_action": ACTION, "width": 92, "link_unit": 16}
    }
    universe["families"] = families
    (folder / "u.json").write_text(json.dumps(universe), encoding="utf-8")
    nodes = [[x, y, z] for x in range(CUBE) for y in range(CUBE) for z in range(CUBE)]
    world: dict[str, Any] = {
        "shape": [CUBE] * 3,
        "boundary": {"x": "periodic", "y": "periodic", "z": "periodic"},
    }
    world.update(intervals=400, universe="u.json", node_detectors=[], bodies=[])
    mode: dict[str, Any] = {"bodies": [], "packets": []}
    if dust:
        world["bodies"] = [{"family": "dust", "nodes": [{"node": at, "count": dust} for at in nodes]}]
        clock = paces.clock(GAMMA, 0)
        before = (2 * (GAMMA**3 - GAMMA * clock * clock) * amplitude + GAMMA**3) // (2 * GAMMA**3)
        moving = {"now": [amplitude] * len(nodes), "before": [before] * len(nodes)}
        mode["bodies"] = [{"family": "dust", "pair": [0, GAMMA], "moving": moving}]
    path = folder / "light.json"
    path.write_text(json.dumps(world), encoding="utf-8")
    mode["world_digest"] = input_digest(world)
    path.with_suffix(".mode.json").write_text(json.dumps(mode), encoding="utf-8")
    return path


def coasting(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, gap: int, dust: int, amplitude: int, level: int
) -> tuple[Lattice, int]:
    """The board with light's record uniform at `level` now and `level` - v before, the remainder the half wall (the state a coasting mean reaches, which no lay door writes: No write from outside Rule3 wakes either double root of the massless row), with the light family's index."""
    tmp_path.mkdir(exist_ok=True)
    monkeypatch.setattr(world_files, "REPOSITORY_ROOT", tmp_path)
    monkeypatch.setattr(Lattice, "gate", lambda board: None)
    board = Lattice(load_world(light_world(tmp_path, gap, dust, amplitude)))
    board.output = lambda line: None
    index = [i for i, family in enumerate(board.families) if family.name == "light"][0]
    line = board.states[index].lines[0]
    now = np.full(board.shape, level, dtype=line.now.dtype)
    before = np.full(board.shape, level - SPEED, dtype=line.before.dtype)
    remainder = np.full(board.shape, board.half_wall(index), dtype=line.remainder.dtype)
    board.states[index].lines = [records.Record(now, before, remainder)]
    return board, index


def flat(array: Any) -> list[int]:
    return [int(x) for x in np.asarray(array, dtype=object).reshape(-1)]


def readings(board: Lattice, index: int) -> tuple[list[int], list[int], list[int], list[int]]:
    """What the click reads of the light row: the share and the quanta at every Node (the hazard's weights) and the remainders (the draw's digits), with the time line's levels."""
    line, time = board.states[index].lines[0], board.states[board.held[0]].lines[0]
    return (
        flat(board.share_of(index)[0]),
        flat(board.quanta(index)[0]),
        flat(line.remainder),
        flat(time.now),
    )


def test_the_uniform_light_level_drifts_at_its_velocity_and_is_read_by_nothing(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    board, index = coasting(tmp_path, monkeypatch, GAMMA, 0, 0, LEVEL)
    seed, same_index = coasting(tmp_path / "seed", monkeypatch, GAMMA, 0, 0, 0)
    assert same_index == index
    wall = wall_of(GAMMA, GAMMA, board.unit)
    states = {0: board_state(board)}
    for t in range(1, 41):
        board.step()
        seed.step()
        states[t] = board_state(board)
        line = board.states[index].lines[0]
        assert flat(line.now) == [LEVEL + SPEED * t] * CUBE**3, t  # (1) the drift exactly v
        assert flat(line.before) == [LEVEL + SPEED * (t - 1)] * CUBE**3, t
        assert flat(line.remainder) == [wall // 2] * CUBE**3, t  # the remainder carried unchanged
        assert flat(seed.states[index].lines[0].now) == [SPEED * t] * CUBE**3
        if t in (1, 2, 20, 40):
            share, quanta, remainders, time = readings(board, index)
            assert share == [3 * GAMMA * SPEED * SPEED] * CUBE**3 and quanta == [0] * CUBE**3  # (2)
            assert time == [GAMMA] * CUBE**3  # the time line stands
            assert (share, quanta, remainders, time) == readings(seed, index)  # the level unread
    assert board.swaps == [] and seed.swaps == []  # (5) the massless board fires nowhere
    back = 0  # (3) the run back
    for k in range(40):
        board.step_inverse()
        back += same_state(board_state(board), states[39 - k])
    assert back == 40


def test_the_turned_board_runs_the_light_mean_back(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    board, index = coasting(tmp_path, monkeypatch, GAMMA - 1, 21, 160, LEVEL)
    wall = wall_of(GAMMA, GAMMA, board.unit)
    levels, states = {0: flat(board.states[index].lines[0].now)}, {0: board_state(board)}
    t = 0
    while t < 160 and (not board.swaps or t < board.swaps[0][0] + 12):
        t += 1
        board.step()
        levels[t], states[t] = flat(board.states[index].lines[0].now), board_state(board)
    fires = [(s[0], s[2]) for s in board.swaps if s[1] == 1]
    assert len(fires) == 1 and fires[0][1] == CUBE**3 and 20 < fires[0][0] <= 130, fires
    star = fires[0][0]
    for k in range(12):  # (4) the T-image: the level now at t* + k the level before of t* - 1 - k
        line = states[star + k][index][0][0]
        assert flat(line[0]) == levels[star - 2 - k] == [LEVEL + SPEED * (star - 2 - k)] * CUBE**3, k
        assert flat(line[1]) == levels[star - 1 - k], k
        assert flat(line[2]) == [wall - 1 - wall // 2] * CUBE**3, k
    back = 0
    for k in range(20):
        board.step_inverse()
        back += same_state(board_state(board), states[t - 1 - k])
    assert back == 20 and [(s[0], s[2]) for s in board.swaps if s[1] == -1] == [(star, CUBE**3)]
