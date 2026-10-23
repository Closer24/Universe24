"""The swap at the top (P-M19-5 as M20 derives it; the fifth act of the interval, swap.py, always on, no key): at a Node whose time line shows a weak maximum over one interval, X0 <= X1 >= X2 and not all equal (X0 the level before at the interval's start, X1 the level now at the start, X2 the level now at the end after the step and the write), the Node ends the interval at its pre-state swapped and complemented, every line (now, before, r) -> (before, now, wall - 1 - r), the step's output discarded; by the T-image theorem (F T F = T on the engine's lines) the forward run from it is the run back of the rise, and the inverse is the same reading on the undone interval. The clauses: (1) on the gapped torus the trigger fires at exactly one interval of the first rise, at every Node at once, at the first weak maximum of X, and never before it (never at the start at rest); (2) from the fire on, the state at t* + k is the T-image of the state at t* - 1 - k bit for bit, every remainder complemented at its wall; (3) the run back through the fire is exact and the inverse fires at the same interval; (4) a massless time line [Gamma, Gamma] never fires (X' never passes 0 downward on the uniform torus)."""

import json

import numpy as np

from event_universe import shear, world_files
from event_universe.core import paces
from event_universe.core.rule3 import wall_of
from event_universe.lattice import Lattice
from event_universe.world_files import input_digest, load_world
from tests.laws import state_of

GAMMA, ACTION, CUBE = 1000, 36000, 3
HELD = {"sources": ["form", "tensions"], "level_weight": 1, "write_weight": 1}


def gapped_world(folder, gap, count, amplitude):  # type: ignore[no-untyped-def]
    """The 3-cube torus with gravity's pair [gap, Gamma] and dust [0, Gamma] laid uniform at the band's rest rotation (test_the_gapped_volume's world, the count the gate's own reading)."""
    universe = {
        "integers": {"node_clock": GAMMA, "quantum_action": ACTION, "width": 92, "link_unit": 16},
        "families": [
            {"name": "gravity", "pair": [gap, GAMMA], "reads": {"gravity": 1}, "held": HELD},
            {"name": "dust", "pair": [0, GAMMA], "reads": {"gravity": 1}, "dimension": 1},
        ],
    }
    (folder / "u.json").write_text(json.dumps(universe), encoding="utf-8")
    nodes = [[x, y, z] for x in range(CUBE) for y in range(CUBE) for z in range(CUBE)]
    world = {"shape": [CUBE] * 3, "boundary": {"x": "periodic", "y": "periodic", "z": "periodic"}}
    world.update(intervals=400, universe="u.json", node_detectors=[])
    world["bodies"] = [{"family": "dust", "nodes": [{"node": at, "count": count} for at in nodes]}]
    clock = paces.clock(GAMMA, 0)
    before = (2 * (GAMMA**3 - GAMMA * clock * clock) * amplitude + GAMMA**3) // (2 * GAMMA**3)
    entry = {
        "family": "dust",
        "pair": [0, GAMMA],
        "moving": {"now": [amplitude] * len(nodes), "before": [before] * len(nodes)},
    }
    path = folder / "swap.json"
    path.write_text(json.dumps(world), encoding="utf-8")
    path.with_suffix(".mode.json").write_text(
        json.dumps({"world_digest": input_digest(world), "bodies": [entry], "packets": []}),
        encoding="utf-8",
    )
    return path


def same(a, b):  # type: ignore[no-untyped-def]
    return all(
        all(np.array_equal(u, v) for x, y in zip(la, lb, strict=True) for u, v in zip(x, y, strict=True))
        and all(np.array_equal(u, v) for u, v in zip(ra, rb, strict=True))
        for (la, ra), (lb, rb) in zip(a, b, strict=True)
    )


def t_image(board, s):  # type: ignore[no-untyped-def]
    """Every line swapped and its remainder complemented at its wall: w on a plain line, 3 w (X_now + X_before) on a tension line carried as the shear's momentum, the write's wall on a write remainder."""
    out = []
    for index, (lines, rems) in enumerate(s):
        family = board.families[index]
        w = wall_of(family.pair[1], GAMMA, board.unit)
        at = set(shear.shear_lines(family)) if shear.carried(family) else set()
        new = []
        for n, (now, before, rem) in enumerate(lines):
            first = (n // family.width) * family.width
            lw = 3 * w * (lines[first][0] + lines[first][1]) if n in at else w
            new.append((before, now, np.asarray(lw, dtype=object) - 1 - rem))
        walls = board.write_walls.get(index, [])
        out.append(
            (new, [np.asarray(wl, dtype=object) - 1 - r for wl, r in zip(walls, rems, strict=True)])
        )
    return out


def test_the_swap_fires_once_at_the_first_weak_top_and_the_fall_is_the_rise_run_back(
    tmp_path, monkeypatch
):  # type: ignore[no-untyped-def]
    monkeypatch.setattr(world_files, "REPOSITORY_ROOT", tmp_path)
    monkeypatch.setattr(Lattice, "gate", lambda board: None)
    board = Lattice(load_world(gapped_world(tmp_path, GAMMA - 1, 21, 869)))
    board.output = lambda line: None
    g = [i for i in board.held if board.families[i].motion_volume][0]
    X = lambda: int(np.asarray(board.states[g].lines[0].now, dtype=object).reshape(-1)[0])  # noqa: E731
    xs, states = [X()], {0: state_of(board)}
    for t in range(1, 340):
        board.step()
        xs.append(X())
        states[t] = state_of(board)
    fires = [(s[0], s[2]) for s in board.swaps if s[1] == 1]
    tops = [
        t
        for t in range(1, 330)
        if xs[t - 1] <= xs[t] >= xs[t + 1] and (xs[t - 1] < xs[t] or xs[t + 1] < xs[t])
    ]
    assert len(fires) == 1 and fires[0][1] == CUBE**3, fires  # (1) once, every Node
    star = fires[0][0]
    assert tops[0] == star - 1 and star > 200, (
        tops,
        star,
    )  # at the first weak maximum, not at the start
    for k in range(0, 40):  # (2) the fall is the rise's T-image bit for bit
        assert same(states[star + k], t_image(board, states[star - 1 - k])), k
    assert xs[star + 40] == xs[star - 42]
    back = 0  # (3) the run back through the fire
    for k in range(80):
        board.step_inverse()
        back += same(state_of(board), states[339 - k - 1])
    assert back == 80 and [(s[0], s[2]) for s in board.swaps if s[1] == -1] == [(star, CUBE**3)]


def test_a_massless_time_line_never_fires(tmp_path, monkeypatch):  # type: ignore[no-untyped-def]
    monkeypatch.setattr(world_files, "REPOSITORY_ROOT", tmp_path)
    monkeypatch.setattr(Lattice, "gate", lambda board: None)
    board = Lattice(load_world(gapped_world(tmp_path, GAMMA, 21, 869)))  # [Gamma, Gamma]
    board.output = lambda line: None
    g = [i for i in board.held if board.families[i].motion_volume][0]
    xs = []
    for _ in range(60):
        board.step()
        xs.append(int(np.asarray(board.states[g].lines[0].now, dtype=object).reshape(-1)[0]))
    assert board.swaps == [] and all(a < b for a, b in zip(xs, xs[1:], strict=False))  # (4)


def test_the_shipped_matter_world_fires_at_the_bodys_six_neighbours_at_interval_2_and_nowhere_after(
    tmp_path, monkeypatch
):  # type: ignore[no-untyped-def]
    """(5) The shipped big bang's matter world (Gamma 6,000, gravity [6000, 6000], the seed at one Node: a structured massless board) under the law with both acts, read 2026-10-23 (the structured-cycle branch): the fifth act fires at the body's six Link neighbours at interval 2 and nowhere after over 50 intervals, board.swaps == [(2, 1, 6)]. The cause: under The stress is the Links' the body's pressure is read at its six neighbours one Link out and enters their time line's write as the trace at the weight -1 before the form's write reaches them by the step at interval 3, so their volume's step output dips below the rest they stand at (6,247), a weak maximum, and the act keeps the rest; the former stress reading put the pressure at the body's own Node, where the form's write outweighs it, and the world fired nowhere (the former clause). The course stands after the fires: X at the body 6,247, 16,785, 34,986 at 1, 2, 3, every Node rising from 3 on, U 1.283 at 100, 1.530 at 200 and 1.675 at 300 (the fine mean over the Nodes) against the shipped eras log's level reading under the former stress reading, 1.283, 1.535, 1.684, no further fire and no refusal (examples/events/big_bang/big_bang_matter.course.jsonl)."""
    from tests.laws import EVENTS

    board = Lattice(load_world(EVENTS / "big_bang" / "big_bang_matter.json"))
    board.output = lambda line: None
    for _ in range(50):
        board.step()
    assert board.swaps == [(2, 1, 6)]


def run_back_exact(world, intervals):  # type: ignore[no-untyped-def]
    """A world stepped `intervals` forward and back, the snapshot at every interval compared bit for bit on the way back, the counts and the swaps' mirror read: the steps matched, the counts' equality."""
    from event_universe.meeting_back import first_difference, snapshot

    board = Lattice(load_world(world))
    board.output = lambda line: None
    counts, snaps = list(board.credit.counts), [snapshot(board)]
    for _ in range(intervals):
        board.step()
        snaps.append(snapshot(board))
    matched = 0
    for k in range(intervals):
        board.step_inverse()
        matched += first_difference(snaps[intervals - k - 1], snapshot(board)) is None
    return matched, list(board.credit.counts) == counts, board.swaps


def test_the_matter_worlds_run_back_reaches_interval_0_exactly_through_the_fires_and_the_declared_lay():  # type: ignore[no-untyped-def]
    """The shipped matter world under both acts run 60 intervals forward and back, every snapshot on the way back bit for bit, interval 0 included, the counts back (the lay's inverse, 2026-10-23). The former mismatch at the last step, named: the file's packets (`interval: 1`) are laid by the lay act from outside the Node after the held writes of interval 1, so the first interval writes nothing; before the lay's inverse the run back undid the books' log's lays alone (the clicks', where the world reads sides), the laid records stayed and the held write's inverse took off a write never added (the body's time line `before` 16,786 against 6,247, the same letter on the landing head before both acts, 16,208), and the swap's inverse fired at the six neighbours on the spurious dip; now every lay at an interval above 0 is logged and crossed back at its interval before the interval's inverse, the laid packets' counts with their levels (`lay.written`, `meeting_back.logged`), so the inverse finds the bookings of the first interval's start empty as the forward found them, and the six fires of interval 2 are mirrored by their inverse alone."""
    from tests.laws import EVENTS

    matched, counts_back, swaps = run_back_exact(EVENTS / "big_bang" / "big_bang_matter.json", 60)
    assert matched == 60 and counts_back
    assert swaps == [(2, 1, 6), (2, -1, 6)]


def test_the_big_bang_worlds_run_back_reaches_interval_0_exactly_through_its_lays_and_fires():  # type: ignore[no-untyped-def]
    """The shipped big bang world with light (three plane waves laid whole at interval 1 beside the matter) run 40 intervals forward and back under both acts: every snapshot on the way back bit for bit, interval 0 included, the counts back, every fire mirrored by its inverse (the lay's inverse, 2026-10-23)."""
    from tests.laws import EVENTS

    matched, counts_back, swaps = run_back_exact(EVENTS / "big_bang" / "big_bang.json", 40)
    assert matched == 40 and counts_back
    forward = [s for s in swaps if s[1] == 1]
    assert [(t, -1, n) for t, _d, n in reversed(forward)] == [s for s in swaps if s[1] == -1]
