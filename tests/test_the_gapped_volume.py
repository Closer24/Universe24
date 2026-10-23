"""The gapped time line in the volume form (ALGEBRA.md, The carried momentum, the clause of 2026-10-23 on the return hand's derivation read cold by the reader, the old clause kept by name; The closed lattice has no rest; The sign side of the exponent; loader/interval.volume_rows, Lattice.start): a tiny torus declared inside the test with gravity's pair gapped, [999, 1000] at Gamma 1,000, dust laid uniform at the band's rest rotation at the law's amplitude for 21 quanta per Node, and the shipped world of the test of the law's course held bit for bit against its own log."""

import hashlib
import json

import numpy as np

from event_universe import lists, node, world_files
from event_universe.core import paces
from event_universe.emission import amplitude
from event_universe.lattice import Lattice
from event_universe.world_files import input_digest, load_world
from tests.laws import BACK, EVENTS, ROOT, load_file

ERAS = load_file("eras_tool", ROOT / "tools" / "eras.py")
DIGEST = "00573f6ccdc48b4d"  # the matter world's twenty intervals of readings on the one Node, recorded 2026-10-23

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
    """(i) The loader moves the gapped gravity row to the volume form by its tension lines (loader/interval.volume_rows, `FamilyRule.axes`) and the start lays it at the vacuum's volume Gamma at every Node; (ii) over 50 intervals the step's mass term at the fixed wall, X_next - 2 X_now + X_before less the write's increment, equals -2 (1 - nu) (p_0 / Gamma)^2 X_now within one level at every interval (the return hand's energy identity E1, met within 0.99 of a level on the 5-torus), the write's increment never negative and the tension lines 0 (a uniform lay); (iii) the run back MATCH over 50 intervals (the reversibility hand's Theorem 1 at the wall that never moves). The write's increment is read from the held write's call that carries the time line itself, so the reading stands whether a row's lines are written in one call or the time line and the tension lines in two (the shear's momentum, the tension lines written after the time line's step and write)."""
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
    """(iv) The clause on the tensions changes no shipped run: in the universes of examples/ and tests/ every held row of the content is sourced by the tensions iff its pair is [Gamma, Gamma] (the binding holder [2400, 2401] sourced by the form alone keeps the level form), so the clause selects the same rows on every shipped universe; and the shipped matter world (examples/events/big_bang/big_bang_matter.json) stepped by the one Node through the eras tool's own run (tools/eras.py) reads over its first twenty intervals the stored digest of its integer readings (gravity's level and its remainder, the level before and its remainder, the volume and the volume before, the seed's and the far Node's volumes, the well, every writer's write, and every family of quanta's largest level, count and frozen Nodes; the level 4,066 at the twentieth), recorded on the one Node (2026-10-23) in place of the shipped eras log, which the branch interval-no-observable recorded and the one Node's write leaves from the sixth interval (the matter's write and the tension means); no other clause run anywhere."""
    rows = []
    for folder in ("examples", "tests"):
        for path in sorted((ROOT / folder).rglob("*.json")):
            try:
                families = json.loads(path.read_text(encoding="utf-8")).get("families")
            except ValueError, AttributeError:
                continue
            rows += [f for f in families or [] if isinstance(f, dict) and "held" in f]
    content = [f for f in rows if "wronskian" not in f["held"]["sources"]]
    assert content and all(
        ("tensions" in f["held"]["sources"]) == (f["pair"][0] == f["pair"][1]) for f in content
    )
    assert any(f["pair"] == [2400, 2401] for f in content)
    world = EVENTS / "big_bang" / "big_bang_matter.json"
    lines = ERAS.run(world, tmp_path / "matter.eras.jsonl", 1, 20)
    assert [line["interval"] for line in lines] == list(range(1, 21))
    integers = ("level", "level_remainder", "before", "before_remainder", "volume", "volume_before")
    integers += ("at_seed", "at_far", "well", "nodes")
    found = hashlib.sha256()
    for line in lines:
        row = line["rows"]["gravity"]
        kept = {
            "interval": line["interval"],
            **{key: row[key] for key in integers},
            "writes": row["writes"],
        }
        kept["quanta"] = {n: [q["largest"], q["quanta"], q["frozen"]] for n, q in line["quanta"].items()}
        found.update(json.dumps(kept, sort_keys=True).encode())
    assert (found.hexdigest()[:16], lines[-1]["rows"]["gravity"]["level"]) == (DIGEST, 4066)
