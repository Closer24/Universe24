"""The gapped time line in the volume form (ALGEBRA.md, The carried momentum, the clause of 2026-10-23 on the return hand's derivation read cold by the reader, the old clause kept by name; The closed lattice has no rest; The sign side of the exponent; loader/interval.volume_rows, Lattice.start): a tiny torus declared inside the test with gravity's pair gapped, [999, 1000] at Gamma 1,000, dust laid uniform at the band's rest rotation, and the shipped world of the test of the law's course held bit for bit against its own log."""

import json
import re

import numpy as np

from event_universe import board_readings, node, world_files
from event_universe.core import paces
from event_universe.core.rule3 import division_forward, largest_below
from event_universe.lattice import Lattice
from event_universe.world_files import input_digest, load_world
from tests.laws import BACK, EVENTS, ROOT

GAMMA, ACTION, CUBE, GAP = 1000, 36000, 3, 999  # the gapped torus: Gamma 1,000, gravity [999, 1000]
HELD = {"sources": ["form", "tensions"], "level_weight": 1, "write_weight": 1}


def gapped_world(folder, count, amplitude):  # type: ignore[no-untyped-def]
    """The 3-cube torus (every board's interval no observable under the one Node) with gravity's pair [999, 1000] and dust [0, 1000] laid uniform as one body at the band's rest rotation in the vacuum (now A, before A cos omega_b), the return hand's world at the gap 1 / 1,000 on the smallest odd torus."""
    universe = {
        "integers": {"node_clock": GAMMA, "quantum_action": ACTION, "width": 92, "link_unit": 16},
        "families": [
            {"name": "gravity", "pair": [GAP, GAMMA], "reads": {"gravity": 1}, "held": HELD},
            {"name": "dust", "pair": [0, GAMMA], "reads": {"gravity": 1}, "dimension": 1},
        ],
    }
    (folder / "u.json").write_text(json.dumps(universe), encoding="utf-8")
    nodes = [[x, y, z] for x in range(CUBE) for y in range(CUBE) for z in range(CUBE)]
    body = [{"node": at, "count": count} for at in nodes]
    world = {"shape": [CUBE] * 3, "boundary": {"x": "periodic", "y": "periodic", "z": "periodic"}}
    world.update(
        intervals=60, universe="u.json", node_detectors=[]
    )  # every board's interval unobservable
    world["bodies"] = [{"family": "dust", "nodes": body}]
    clock = paces.clock(GAMMA, 0)
    before = (2 * (GAMMA**3 - GAMMA * clock * clock) * amplitude + GAMMA**3) // (2 * GAMMA**3)
    entry = {
        "family": "dust",
        "pair": [0, GAMMA],
        "moving": {"now": [amplitude] * len(nodes), "before": [before] * len(nodes)},
    }
    path = folder / "gapped.json"
    path.write_text(json.dumps(world), encoding="utf-8")
    mode = {"world_digest": input_digest(world), "bodies": [entry], "packets": []}
    path.with_suffix(".mode.json").write_text(json.dumps(mode), encoding="utf-8")
    return path


def laid_gapped(folder, count=21):  # type: ignore[no-untyped-def]
    """The gapped world laid uniform at `count` quanta per Node (the return hand's 21), the dust's amplitude found from the share the gate reads: the band's rest amplitude for the count as the first guess, the share read from the gate's refusal (it grows as the amplitude squared), the amplitude rescaled once and raised by one until the declared count is within the share's rounding (ALGEBRA.md #the-count-is-the-records-share)."""
    nodes = CUBE**3
    amplitude = largest_below(
        int(division_forward(count * ACTION * GAMMA, 2 * paces.sine_den(0, GAMMA), 0)[0])
    )
    for attempt in range(12):
        path = gapped_world(folder, count, amplitude)
        try:
            Lattice(load_world(path))
            return path
        except ValueError as refusal:
            read = int(re.search(r"share reads (\d+) quanta", str(refusal)).group(1))
            amplitude = (
                round(amplitude * (count * nodes / read) ** 0.5) if attempt == 0 else amplitude + 1
            )
    raise AssertionError(amplitude)


def test_the_gapped_row_carries_the_volume_and_its_step_is_rule3s_own_mass_at_the_fixed_wall(
    tmp_path, monkeypatch
):
    """(i) The loader moves the gapped gravity row to the volume form by its tension lines (loader/interval.volume_rows, `FamilyRule.axes`) and the start lays it at the vacuum's volume Gamma at every Node; (ii) over 50 intervals the step's mass term at the fixed wall, X_next - 2 X_now + X_before less the write's increment, equals -2 (1 - nu) (p_0 / Gamma)^2 X_now within one level at every interval (the return hand's energy identity E1, met within 0.99 of a level on the 5-torus), the write's increment never negative and the tension lines 0 (a uniform lay); (iii) the run back MATCH over 50 intervals (the reversibility hand's Theorem 1 at the wall that never moves)."""
    monkeypatch.setattr(world_files, "REPOSITORY_ROOT", tmp_path)
    path = laid_gapped(tmp_path)
    board = Lattice(load_world(path))
    g = [family.name for family in board.families].index("gravity")
    assert board.families[g].pair == (GAP, GAMMA) and board.families[g].motion_volume
    assert not board.families[g + 1].motion_volume  # dust, a family of quanta
    line = board.states[g].lines[0]
    assert set(np.asarray(line.now, dtype=object).reshape(-1)) == {GAMMA}  # the vacuum's volume
    assert set(np.asarray(line.before, dtype=object).reshape(-1)) == {GAMMA}  # at rest
    increment = {}
    original = node.held_write_at

    def wrapped(lines, numerators, walls, remainders, direction=1):  # type: ignore[no-untyped-def]
        found, after = original(lines, numerators, walls, remainders, direction)
        increment["write"] = int(found[0].now.reshape(-1)[0]) - int(lines[0].now.reshape(-1)[0])
        return found, after

    monkeypatch.setattr(node, "held_write_at", wrapped)
    nu, misses = GAP / GAMMA, []
    for _ in range(50):
        line = board.states[g].lines[0]
        now = np.asarray(line.now, dtype=object).reshape(-1)
        assert now.min() == now.max()  # the uniform lay stays uniform to the bit
        assert all(not axis.now.any() for axis in board.states[g].lines[1:])  # the tensions 0
        content = node.read(g, board.families, board.states, 1, board.wrap, GAMMA, board.unit, 0)[0]
        clock = int(np.asarray(paces.node_paces(GAMMA, content)[0]).reshape(-1)[0])
        x_now, x_before = int(now[0]), int(np.asarray(line.before, dtype=object).reshape(-1)[0])
        board.step()
        x_next = int(np.asarray(board.states[g].lines[0].now, dtype=object).reshape(-1)[0])
        assert increment["write"] >= 0  # the pull is the step's mass term and not the write
        mass_term = x_next - 2 * x_now + x_before - increment["write"]
        misses.append(abs(mass_term + 2 * (1 - nu) * (clock / GAMMA) ** 2 * x_now))
    assert max(misses) <= 1.0, misses
    assert x_next > GAMMA  # the free fall's rise from the seed
    monkeypatch.setattr(node, "held_write_at", original)
    verdict = BACK.verdict(Lattice(load_world(path)), 50)
    assert verdict == {"verdict": "MATCH", "intervals": 50, "interval": 1, "ended": None}


def test_every_shipped_gravity_pair_is_massless_and_the_matter_world_runs_as_its_log_says():  # type: ignore[no-untyped-def]
    """(iv) The clause on the tensions changes no shipped run: every held row sourced by the tensions in the universes of examples/ and tests/ has the pair [Gamma, Gamma] (the one gapped held row shipped, the atom's binding holder [2400, 2401], has no tension lines and stays in the level form), and the shipped matter world of the test of the law's course (examples/events/big_bang/big_bang_matter.json) reproduces its own eras' log bit for bit over 100 intervals, the level now and before of gravity's uniform mode with their remainders (`board_readings.uniform_mode`, the log's columns)."""
    tensions, form_alone = [], []
    for folder in ("examples", "tests"):
        for path in sorted((ROOT / folder).rglob("*.json")):
            try:
                families = json.loads(path.read_text(encoding="utf-8")).get("families")
            except ValueError, AttributeError:
                continue
            for family in families or []:
                if isinstance(family, dict) and "held" in family:
                    (tensions if "tensions" in family["held"]["sources"] else form_alone).append(family)
    assert tensions and all(family["pair"][0] == family["pair"][1] for family in tensions)
    assert any(family["pair"] == [2400, 2401] for family in form_alone)
    world = EVENTS / "big_bang" / "big_bang_matter.json"
    with (world.parent / "big_bang_matter.eras.jsonl").open(encoding="utf-8") as log:
        next(log)
        rows = [json.loads(next(log))["rows"]["gravity"] for _ in range(100)]
    board = Lattice(load_world(world))
    g = [family.name for family in board.families].index("gravity")
    for row in rows:
        board.step()
        mode = board_readings.uniform_mode(board, g)
        read = (mode.level, mode.level_remainder, mode.before, mode.before_remainder)
        assert read == (row["level"], row["level_remainder"], row["before"], row["before_remainder"]), (
            row["interval"]
        )
