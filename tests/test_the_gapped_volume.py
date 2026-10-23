"""The gapped time line in the volume form (ALGEBRA.md, The carried momentum, the clause of 2026-10-23 on the return hand's derivation read cold by the reader; The closed lattice has no rest; The sign side of the exponent; loader/interval.volume_rows, Lattice.start): a tiny torus declared inside the test with gravity's pair gapped, [999, 1000] at Gamma 1,000, dust laid uniform at the band's rest rotation at the law's amplitude for 21 quanta per Node, and the shipped world of the test of the law's course held bit for bit against its own log."""

import json

import numpy as np

from event_universe import lists, node, world_files
from event_universe.core import paces
from event_universe.emission import amplitude
from event_universe.lattice import Lattice
from event_universe.world_files import input_digest, load_world
from tests.laws import BACK, EVENTS, ROOT, load_file

ERAS = load_file("eras_tool", ROOT / "tools" / "eras.py")

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


def laid_gapped(folder, monkeypatch, count=21):  # type: ignore[no-untyped-def]
    """The gapped world laid uniform at the law's amplitude for `count` quanta per Node (`emission.amplitude`, the lay across parts; the return hand's 21), its declared count the share the repository's own gate reads of that lay (`lists.gate_count`, the count a reading of the record and no input: ALGEBRA.md #the-count-is-the-records-share), read once with the gate held and declared for the load with the gate on."""
    size = amplitude(count, ACTION, (0, GAMMA), 1)
    with monkeypatch.context() as held:
        held.setattr(Lattice, "gate", lambda board: None)
        board = Lattice(load_world(gapped_world(folder, count, size)))
    read = lists.gate_count(board, board.world.bodies[0])
    assert read % CUBE**3 == 0, read  # a uniform lay reads alike at every Node
    return gapped_world(folder, read // CUBE**3, size)


def test_the_gapped_row_carries_the_volume_and_its_step_is_rule3s_own_mass_at_the_fixed_wall(
    tmp_path, monkeypatch
):
    """(i) The loader moves the gapped gravity row to the volume form by its tension lines (loader/interval.volume_rows, `FamilyRule.axes`) and the start lays it at the vacuum's volume Gamma at every Node; (ii) over 50 intervals the step's mass term at the fixed wall, X_next - 2 X_now + X_before less the write's increment, equals -2 (1 - nu) (p_0 / Gamma)^2 X_now within one level at every interval (the return hand's energy identity E1, met within 0.99 of a level on the 5-torus), the write's increment never negative and the tension lines 0 (a uniform lay); (iii) the run back MATCH over 50 intervals (the reversibility hand's Theorem 1 at the wall that never moves). The write's increment is read from the held write's call that carries the time line itself, so the reading stands whether a row's lines are written in one call or the time line and the tension lines in two (the shear's momentum, the tension lines written after the time line's step and write). Uniform by nature: this test's claim is the k = 0 line's, the one write's arithmetic on a level uniform over the board, so its board is uniform (the owner's rule of 2026-10-23: the tests of the law's course run on a structured board; the uniform board stands here as the null case of that one line)."""
    monkeypatch.setattr(world_files, "REPOSITORY_ROOT", tmp_path)
    path = laid_gapped(tmp_path, monkeypatch)
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
        for line, stepped in zip(lines, found, strict=True):
            if line is board.states[g].lines[0]:  # the time line's own write, whichever call carries it
                increment["write"] = int(stepped.now.reshape(-1)[0]) - int(line.now.reshape(-1)[0])
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


def test_every_shipped_gravity_pair_is_massless_and_the_matter_world_runs_as_its_shipped_log(tmp_path):  # type: ignore[no-untyped-def]
    """(iv) The clause on the tensions changes no shipped run: in the universes of examples/ and tests/ every held row sourced by the tensions is a row of the content, massless [Gamma, Gamma] or gapped (the cycle's and Universe24's gravity [999, 1000] carrying its volume), never the holder of the sign, and the binding holder [2400, 2401] sourced by the form alone keeps the level form; and the shipped matter world (examples/events/big_bang/big_bang_matter.json) stepped by the one Node through the eras tool's own run (tools/eras.py) over its first twenty intervals reads the law's course and not a stored one: one line per interval with gravity the one held row read (the sign's holder reads none), its level rising from the seed at every interval (the free fall's rise, the pull the step's mass term), each line's level before and its remainder the line before's level and remainder and its volume before the line before's volume (the reading's chain), the remainders of the carried division below the Nodes' count, the volume the sum of the volume form over the board growing with the level, the seed's well at or above 0 and open from the second interval (the seed's Node above the far one), every writer's write at or above 0 with light's 0 (no light laid on this world), no family frozen, no swap at the top (gravity massless, the swap reads the gapped time line alone) and no Link at the wall. The former pin, the digest 687901882f2c706c of the twenty lines' integers with the level 4,091 at the twentieth (recorded 2026-10-23 at the landing with the stress the Links' and the swap at the top; 00573f6ccdc48b4d with 4,066 before the Links' stress, the same day), was read on a course where the swap at the top fired at the interval 2 at the body's six neighbours on the massless gravity row, the reading struck the same day (the swap reads the gapped time line alone; the level reads 4,099 at the twentieth since), named here and not asserted (ENGINE.md section 9). Uniform by nature: this test's claim is the k = 0 line's, the one write's arithmetic on a level uniform over the board, so its board is uniform (the owner's rule of 2026-10-23: the tests of the law's course run on a structured board; the uniform board stands here as the null case of that one line)."""
    rows = []
    for folder in ("examples", "tests"):
        for path in sorted((ROOT / folder).rglob("*.json")):
            try:
                families = json.loads(path.read_text(encoding="utf-8")).get("families")
            except ValueError, AttributeError:
                continue
            rows += [f for f in families or [] if isinstance(f, dict) and "held" in f]
    content = [f for f in rows if "wronskian" not in f["held"]["sources"]]
    assert (
        content
        and all(
            ("wronskian" not in f["held"]["sources"]) if "tensions" in f["held"]["sources"] else True
            for f in content
        )
    )  # the tensions source the content's rows alone, massless or gapped (the cycle's gravity [999, 1000]), never the sign's holder
    assert any(f["pair"] == [2400, 2401] for f in content)
    world = EVENTS / "big_bang" / "big_bang_matter.json"
    lines = ERAS.run(world, tmp_path / "matter.eras.jsonl", 1, 20)
    assert [line["interval"] for line in lines] == list(range(1, 21))
    rows = [line["rows"]["gravity"] for line in lines]
    assert all(list(line["rows"]) == ["gravity"] for line in lines)  # the one held row read
    assert all(row["nodes"] == rows[0]["nodes"] > 0 for row in rows)
    assert all(later["level"] > earlier["level"] for earlier, later in zip(rows, rows[1:], strict=False))
    assert all(0 <= row["level_remainder"] < row["nodes"] for row in rows)
    assert all(
        (later["before"], later["before_remainder"], later["volume_before"])
        == (earlier["level"], earlier["level_remainder"], earlier["volume"])
        for earlier, later in zip(rows, rows[1:], strict=False)
    )  # the reading's chain
    assert all(
        later["volume"] > earlier["volume"] > 0 for earlier, later in zip(rows, rows[1:], strict=False)
    )
    assert (
        all(row["well"] == row["at_seed"] - row["at_far"] >= 0 for row in rows) and rows[1]["well"] > 0
    )
    assert all(min(row["writes"].values()) >= 0 and row["writes"]["light"] == 0 for row in rows)
    assert all(q["frozen"] == 0 for line in lines for q in line["quanta"].values())
    assert all(line["fires"] == 0 and line["horizon"] == 0 for line in lines)
