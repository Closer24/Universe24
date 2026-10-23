"""The swap at the top on a world with a holder of the sign under the rotation (ALGEBRA.md, The swap at the top, the phase clause; The turn per proper interval, the centred count; the phase hand's derivation M23 on the owner's decision of 2026-10-23): the Node's phase row Phi a Rule3 record whose write is the clocked potential, the Link's count K_ij = K_i - K_j the two ends' difference of K = Phi_next - Phi_before (twice the trapezoid sum to the triple's centre), the pair at the half angle. At a turned Node the swap exchanges the phase row's two levels and conjugates the plane record, and the centred count reads -K: the fall's pairs are the rise's conjugates and the run back of the planes is exact. The universe is declared inside the test: a gapped 3-cube torus (Gamma 1,000, gravity's pair [990, 1000] so that the top comes within 50 intervals, dust at 21 quanta per Node laid as test_the_swap_at_the_top lays it) with the charge holder under the rotation (level weight 100) read by a charged plane [600, 1000] of two records at two Nodes laid at a third of the one quantum's profile (the gate off; so that the counts stay in the tens and the fires' carry of the pairs at the Links between a turned and an unturned Node, about 2 |K| acts each, stays cheap, node.phase_counts), which carry no dust (the loader admits one body per Node): a structured board, whose void Nodes turn at their pinned rest first and whose board turns at the top. Clauses: (1) the forward run through the top fires at the board's Nodes with no refusal; (2) at every Link whose both ends turned at the top, the count after the fall's first act is the negative of the count the undone step read and the pair's lines are that step's bit for bit (the conjugate under the read); (3) the run back from the run's end to interval 0 is exact at every interval through the split top's two fire intervals (44 and 45) and the void's at 1, the whole state's digest equal, phase lines, pairs and frames included, the inverse firing where the forward run fired (the Link reads its two ends in one frame, the frame the phase row's remainder at the wall 2: the bijection hand's derivation M25, ALGEBRA.md, The swap at the top, the frame clause; the former reading of a mixed Link, -K_i - K_j with the neighbour's value read in its own frame, was inexact at the unturned neighbours of a split top); (4) a flat charged world ([Gamma, Gamma]) never fires, its phase course is live (counts move) and is the same under a second run bit for bit; (5) a deliberately split charged board, the dust's amplitude 869 on the layer x = 0 and 400 on the two others, tops over four intervals (34 to 37, 1, 8, 9 and 9 Nodes, the void's rest at 1 and 2), and its run back to interval 0 is exact at every interval, every fire mirrored. The former reading (to 2026-10-23, the left-sum count moved at the step's start) had no image under the act and a top on such a world was refused by name; the test's numbers are the centred reading's."""

import json
import math

import numpy as np

from event_universe import world_files
from event_universe.core import paces
from event_universe.core.ports import AXES
from event_universe.lattice import Lattice
from event_universe.world_files import input_digest, load_world

GAMMA, ACTION, CUBE, NUM = 1000, 36000, 3, 600
GAP, LAY = (
    GAMMA - 10,
    3,
)  # gravity's pair [990, 1000], the top within 50 intervals; the charged lay over 3, the counts in the tens
SINE = math.isqrt(GAMMA * GAMMA - NUM * NUM)  # 800: the charged pair's sine times den
CENTRES = [(0, 0, 0), (1, 1, 1)]


def charged_world(folder, gap, count, amplitude, intervals=400, weight=100, divisor=1, layers=None):  # type: ignore[no-untyped-def]
    """The gapped 3-cube torus with two one-quantum charged records (the count-1 gate's lay, tests/laws.sign_world), the dust everywhere else; `layers`, the dust's amplitude per layer x in place of `amplitude` (the deliberately split board of clause (5))."""
    universe = {
        "integers": {"node_clock": GAMMA, "quantum_action": ACTION, "width": 92, "link_unit": 16},
        "families": [
            {
                "name": "gravity",
                "pair": [gap, GAMMA],
                "reads": {"gravity": 1},
                "held": {"sources": ["form", "tensions"], "level_weight": 1, "write_weight": 1},
            },
            {"name": "dust", "pair": [0, GAMMA], "reads": {"gravity": 1}, "dimension": 1},
            {
                "name": "charge",
                "pair": [GAMMA, GAMMA],
                "reads": {"gravity": 1},
                "held": {"sources": ["wronskian"], "level_weight": weight},
            },
            {
                "name": "charged",
                "pair": [NUM, GAMMA],
                "reads": {"gravity": 1, "charge": 1},
                "dimension": 2,
            },
        ],
    }
    (folder / "u.json").write_text(json.dumps(universe), encoding="utf-8")
    shape = (CUBE,) * 3
    nodes = [
        [x, y, z]
        for x in range(CUBE)
        for y in range(CUBE)
        for z in range(CUBE)
        if (x, y, z) not in CENTRES
    ]
    world = {"shape": [CUBE] * 3, "boundary": {"x": "periodic", "y": "periodic", "z": "periodic"}}
    world.update(intervals=intervals, universe="u.json", node_detectors=[])
    bodies = [{"family": "dust", "nodes": [{"node": at, "count": count} for at in nodes]}]
    clock = paces.clock(GAMMA, 0)
    amplitudes = [
        (amplitude if layers is None else layers[x]) if (x, y, z) not in CENTRES else 0
        for x in range(CUBE)
        for y in range(CUBE)
        for z in range(CUBE)
    ]
    modes = [
        {
            "family": "dust",
            "pair": [0, GAMMA],
            "moving": {
                "now": amplitudes,
                "before": [
                    (2 * (GAMMA**3 - GAMMA * clock * clock) * a + GAMMA**3) // (2 * GAMMA**3) if a else 0
                    for a in amplitudes
                ],
            },
        }
    ]
    for centre in CENTRES:
        d = np.abs(np.indices(shape) - np.asarray(centre).reshape(3, 1, 1, 1)).sum(axis=0)
        profile = np.select([d == 0, d == 1], [1200, 600], 0)
        values = [int(v) for v in profile.ravel()]
        scale = math.isqrt(ACTION * GAMMA * 1000 * 1000 // (2 * SINE * sum(v * v for v in values)))
        levels = [v * scale // (1000 * divisor) for v in values]  # the one quantum's lay over `divisor`
        moving = dict(now=levels, before=[v * NUM // GAMMA for v in levels])
        moving.update(im_now=[0] * len(levels), im_before=[v * SINE // GAMMA for v in levels])
        bodies.append({"family": "charged", "nodes": [{"node": list(centre), "count": 1}]})
        modes.append({"family": "charged", "pair": [NUM, GAMMA], "moving": moving})
    world["bodies"] = bodies
    path = folder / "charged_swap.json"
    path.write_text(json.dumps(world), encoding="utf-8")
    path.with_suffix(".mode.json").write_text(
        json.dumps({"world_digest": input_digest(world), "bodies": modes, "packets": []}),
        encoding="utf-8",
    )
    return path


def digest(board):  # type: ignore[no-untyped-def]
    """The whole state as bytes: every line, every write remainder and every phase line."""
    parts = []
    for state in board.states:
        for line in state.lines:
            parts += [line.now, line.before, line.remainder]
        parts += list(state.write_remainders)
        for row in state.phases:
            for line in row:
                parts += [line.now, line.before, line.remainder]
    return [np.asarray(a, dtype=object).tolist() for a in parts]


def phase_state(board, holder):  # type: ignore[no-untyped-def]
    rows = [r for r in range(len(board.states[holder].phases)) if board.states[holder].phases[r]]
    return {
        (r, a): tuple(
            np.asarray(getattr(board.states[holder].phases[r][k], f), dtype=object).copy()
            for k in (2 * a, 2 * a + 1, 2 * AXES + a)
            for f in ("now", "before")
        )
        for r in rows
        for a in range(AXES)
    }


def test_the_swap_fires_on_the_charged_torus_and_the_phase_retraces_as_the_conjugate(
    tmp_path, monkeypatch
):  # type: ignore[no-untyped-def]
    from event_universe import swap

    monkeypatch.setattr(world_files, "REPOSITORY_ROOT", tmp_path)
    monkeypatch.setattr(Lattice, "gate", lambda board: None)
    masks = []
    swapped = swap.swapped
    monkeypatch.setattr(
        swap,
        "swapped",
        lambda board, held, mask: (
            masks.append((board.interval, mask.copy())),
            swapped(board, held, mask),
        ),
    )
    board = Lattice(load_world(charged_world(tmp_path, GAP, 21, 869, divisor=LAY)))
    board.output = lambda line: None
    holder = [i for i, f in enumerate(board.families) if f.name == "charge"][0]
    assert board.families[holder].rotation
    digests, phases, tops = {0: digest(board)}, {0: phase_state(board, holder)}, []
    for t in range(1, 400):
        board.step()  # (1) no refusal
        digests[t], phases[t] = digest(board), phase_state(board, holder)
        tops = [
            s[0] for s in board.swaps if s[1] == 1 and s[0] > 5
        ]  # the board's top (at 44 and 45), not the void's pinned rest at 1
        if tops and t >= tops[-1] + 3 and sum(s[2] for s in board.swaps if s[1] == 1 and s[0] > 5) >= 20:
            break
    assert tops and sum(s[2] for s in board.swaps if s[1] == 1 and s[0] > 5) >= 20, board.swaps  # (1)
    star = tops[0]
    first = {}
    for interval, mask in masks:
        for idx in zip(*np.nonzero(mask), strict=True):
            first.setdefault(tuple(int(i) for i in idx), interval)
    both = 0
    for (r, a), rows in phases[
        0
    ].items():  # (2) the fall's first act against the step it undoes, per Link turned at one interval at both ends
        for idx in np.ndindex(rows[0].shape):
            nb = list(idx)
            nb[a] = (nb[a] + 1) % CUBE
            s = first.get(idx)
            if s is not None and s > 5 and first.get(tuple(nb)) == s:
                both += 1
                after, rise = phases[s + 1][(r, a)], phases[s - 1][(r, a)]
                assert after[4][idx] == -rise[4][idx], (r, a, idx)  # the count the negative
                assert after[0][idx] == rise[0][idx] and after[2][idx] == rise[2][idx], (r, a, idx)
                assert after[1][idx] == rise[1][idx] and after[3][idx] == rise[3][idx], (r, a, idx)
    assert both >= 10 and any(int(np.abs(p[4]).max()) > 0 for p in phases[star - 1].values()), both
    back, end = 0, max(digests)  # (3) the run back to interval 0 through every fire, the whole state
    for k in range(end):
        board.step_inverse()
        back += digest(board) == digests[end - k - 1]
    fired = [(s[0], s[2]) for s in board.swaps if s[1] == 1]
    assert back == end and [(s[0], s[2]) for s in board.swaps if s[1] == -1] == fired[::-1], back
    assert [s[0] for s in fired] == [1, 44, 45], fired


def test_a_deliberately_split_charged_board_runs_back_exactly_through_its_four_fire_intervals(
    tmp_path, monkeypatch
):  # type: ignore[no-untyped-def]
    monkeypatch.setattr(world_files, "REPOSITORY_ROOT", tmp_path)
    monkeypatch.setattr(Lattice, "gate", lambda board: None)
    board = Lattice(load_world(charged_world(tmp_path, GAP, 21, 0, divisor=LAY, layers=(869, 400, 400))))
    board.output = lambda line: None
    digests = {0: digest(board)}
    for t in range(1, 120):  # (5) the tops over four intervals, Node by Node
        board.step()
        digests[t] = digest(board)
        tops = [s for s in board.swaps if s[1] == 1 and s[0] > 5]
        if tops and sum(s[2] for s in tops) >= CUBE**3 and t >= tops[-1][0] + 2:
            break
    fired = [(s[0], s[2]) for s in board.swaps if s[1] == 1]
    assert [s[0] for s in fired if s[0] > 5] == [34, 35, 36, 37], fired
    back, end = 0, max(digests)
    for k in range(end):
        board.step_inverse()
        back += digest(board) == digests[end - k - 1]
    assert back == end and [(s[0], s[2]) for s in board.swaps if s[1] == -1] == fired[::-1], back


def test_a_flat_charged_world_never_fires_and_its_phase_course_stands(tmp_path, monkeypatch):  # type: ignore[no-untyped-def]
    monkeypatch.setattr(world_files, "REPOSITORY_ROOT", tmp_path)
    monkeypatch.setattr(Lattice, "gate", lambda board: None)
    courses = []
    for _ in range(2):  # (4) the same course under a second run
        board = Lattice(load_world(charged_world(tmp_path, GAMMA, 21, 869, 40)))
        board.output = lambda line: None
        holder = [i for i, f in enumerate(board.families) if f.name == "charge"][0]
        course = []
        for _ in range(15):
            board.step()
            course.append(digest(board))
        assert board.swaps == []
        counts = [
            np.asarray(line.now, dtype=object)
            for r in board.states[holder].phases
            for line in r[2 * AXES : 3 * AXES]
        ]
        assert any(int(np.abs(c).max()) > 0 for c in counts)
        courses.append(course)
    assert courses[0] == courses[1]
