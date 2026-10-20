"""The meeting that runs back at N sides and with the erasure's taper (the reader's verdict of 2026-10-19, points 11 and 13; ALGEBRA.md, The meeting's reading, root or back; The meeting's identity), beside tests/test_the_meeting_back.py: (i) the reader's case, a two-part record with the identity pattern on every side read at three sides at the settings (3, 4), (1, 1), (1, 0), where the middle side's weights by the chain rule from the booked joint (1 / 2, 1 / 2) differ from the re-weighted one-side share (49 / 50, 1 / 50) by the cross terms of the third side's read, so the engine draws every side after the first on the chain and the law's two-sided words are the last side's alone, tested equal there; no signalling at N sides, every side's marginal its own; (j) the erasure's taper in the back mode, the fronts the act's as built, the erasure lines and the end state equal bit for bit to the root mode's at any seed on regions whose inflow enters at one Node; and the cone stepped alone (the owner's word of 2026-10-20, only the cone moves and the whole board steps as ever): (k) the shipped fifth world and the shipped GHZ world read under the cone and under the whole board with every line, the close and the lay equal and fewer Node-steps in the cone, (l) its three refusals by name. The worlds the tests' own (tests/laws_spin.py), no world or family name in the engine."""

import hashlib
from dataclasses import replace
from fractions import Fraction

import numpy as np
import pytest

from event_universe import credit, meeting_back, reports, world_files
from event_universe.features.click import drawn, hashed
from event_universe.features.front import distances
from event_universe.lattice import Lattice
from event_universe.loader.draw import BACK, BOARD, CONE
from event_universe.records import Record
from event_universe.world_files import load_world
from tests.laws import BACK as GATE
from tests.laws import EVENTS, world_beside
from tests.laws import ROOT as TREE
from tests.laws_spin import (
    BELL,
    IDENTITY,
    PORT,
    SINGLET,
    TRIALS,
    joint_shares,
    rebooked,
    spin_world,
    trial,
)

READER = [9, 16, 9, 16, 16, 9, 16, 9]  # the reader's J over the triples 000 .. 111


def family(board: Lattice, name: str = "spin") -> int:
    return [f.name for f in board.families].index(name)


def digest(board: Lattice) -> str:
    """One hash of every array of the board at a frame (`meeting_back.snapshot`, the arrays' bytes in the families' and the lines' order, the levels' list where the kind is Python's integers): the state of one frame, compared frame by frame between two reaches."""
    found = hashlib.sha256()
    for arrays in meeting_back.snapshot(board):
        for _label, array in arrays:
            a = np.asarray(array)
            found.update(a.tobytes() if a.dtype != object else repr(a.ravel().tolist()).encode())
    return found.hexdigest()


def test_a_middle_side_draws_on_the_chain_from_the_joint_and_the_last_on_the_laws_words(
    tmp_path, monkeypatch
):
    """(i) N sides, the reader's case (the verdict's point 11 of 2026-10-19): the two-part record with the identity pattern on every side read at three sides at the settings (3, 4), (1, 1) and (1, 0), the third region four Nodes inside the left one with one Node between; the three credit lines in the declared order with the count 1 and nothing left, five passes; the engine's booked J equal to the reader's arithmetic over the three sides' `parts` lines and, the parts laid alike, 9, 16, 9, 16, 16, 9, 16, 9 hundredths over the triples 000 .. 111 exactly; at the first side's port p the second side's weights from J by the chain rule (`credit.conditional_of`) 1 / 2 and 1 / 2 against 49 / 50 and 1 / 50 from the re-weighted one-side share at lambda (3, 4) (the mirror at p = 1), the cross terms of the third side's read: the middle side draws on the chain and never on the share; for the last side the chain's weights and the law's words (`conditioned`, `reweighted_share`) proportional at every (p, q), and P(p) P(q | p) P(r | p, q) = J(p, q, r) / SUM J exactly; the realised triple the three draws on the chain's weights at the states hashed from the seed, the names and the window; no signalling at N sides: every side's marginal 1 / 2 here and at other settings of the other sides."""
    reader = {"left": ((3, 4), IDENTITY), "near": ((1, 1), IDENTITY), "right": ((1, 0), IDENTITY)}
    other = {"left": ((3, 4), IDENTITY), "near": ((5, 12), IDENTITY), "right": ((1, 1), IDENTITY)}
    marginals, worlds = {}, {}
    for label, sides in (("reader", reader), ("other", other)):
        path = spin_world(
            tmp_path / label,
            monkeypatch,
            sides,
            both=True,
            amplitude=64,
            meeting=BACK,
            regions={"near": [5, 6, 7, 8]},
        )
        board, lines = trial(path, 1, 40)
        draw, modulus = board.world.draw, board.world.width + 1
        clicks = [c for c in lines if c["event"] == "credit"]
        assert [(c["node_detector"], c["order"], c["count"], c["left"]) for c in clicks] == [
            (name, order, 1, 0) for order, name in enumerate(sides, 1)
        ]
        joint, fixed = rebooked(board, lines), {}
        total = sum(joint.values())
        assert joint == joint_shares(lines, sides, 0) and total > 0 and board.passes == 5
        for side, (name, click) in enumerate(zip(sides, clicks, strict=True)):
            weights = credit.conditional_of(joint, fixed, side)
            marginals[label, side] = Fraction(credit.conditional_of(joint, {}, side)[0], total)
            state = hashed(draw.seed, name, 1, modulus)
            fixed[side] = drawn(state, draw.multiplier, draw.increment, modulus, weights)[0]
            assert fixed[side] == PORT[click["realised"]]  # the draw on the chain's weights
        worlds[label] = (board, joint, total, fixed)
    assert set(marginals.values()) == {Fraction(1, 2)}  # no signalling: each side's marginal its own
    board, joint, total, realised = worlds["reader"]
    spin = family(board)
    assert [Fraction(joint[k], total) for k in sorted(joint)] == [Fraction(n, 100) for n in READER]
    for p in range(2):
        chain = credit.conditional_of(joint, {0: p}, 1)
        lambdas = credit.conditioned(board, spin, {0: p}, 1)
        share = credit.reweighted_share(board, spin, 1, lambdas)
        assert [Fraction(w, sum(chain)) for w in chain] == [Fraction(1, 2)] * 2
        assert lambdas == [[3, 4], [-4, 3]][p]
        assert [Fraction(w, sum(share)) for w in share] == [
            Fraction(49 - 48 * p, 50),
            Fraction(1 + 48 * p, 50),
        ]
        for q in range(2):
            last = credit.conditional_of(joint, {0: p, 1: q}, 2)
            words = credit.reweighted_share(
                board, spin, 2, credit.conditioned(board, spin, {0: p, 1: q}, 2)
            )
            assert [Fraction(w, sum(last)) for w in last] == [Fraction(w, sum(words)) for w in words]
            for r in range(2):
                sequential = Fraction(credit.conditional_of(joint, {}, 0)[p], total)
                sequential *= Fraction(chain[q], sum(chain)) * Fraction(last[r], sum(last))
                assert sequential == Fraction(joint[p, q, r], total), (p, q, r)
    print(
        f"the reader's case at three sides: J {[joint[k] for k in sorted(joint)]}, the realised triple "
        f"{list(realised.values())}, the other settings' triple {list(worlds['other'][3].values())}"
    )


def test_the_tapered_front_erases_alike_in_the_two_modes_inside_the_clicks_light_cone(
    tmp_path, monkeypatch
):
    """(j) The erasure's taper in the back mode (the verdict's point 13 of 2026-10-19): the singlet world with regions of two Nodes at the chain's ends, whose inflow enters at the inner Node alone, and `erasure` 3, run 126 intervals in the root mode and in the back mode at two seeds; the click's write and the front are the act's as built, so the hole's Node is the inner Node whatever the port realised or the generators' states, and the erasure lines (the shell's distance, its Nodes, the share standing), the faces and the end state are equal bit for bit in the two modes at either seed; the two fronts begin at the close, one shell per interval at the Link distance of the intervals since the click (inside the click's light cone), two Nodes at most on the chain, the shells beyond the grown board the taper's last lines, and end at the close plus the farthest Node's distance, one and the taper, the record's count 0 and its share erased; the back-in-time gate reads MATCH over 60 intervals across the tapered shells."""
    sides = {"left": (BELL[0], IDENTITY), "right": (BELL[2], SINGLET)}
    runs, ends = {}, {"left": [0, 1], "right": [31, 32]}
    for mode in (None, BACK):
        path = spin_world(
            tmp_path / str(mode),
            monkeypatch,
            sides,
            both=True,
            amplitude=64,
            meeting=mode,
            regions=ends,
            erasure=3,
        )
        for seed in (1, 5):
            lines = []
            board = Lattice(load_world(path), lines.append)
            board.credit.declaration = replace(board.world.draw, seed=seed)
            board.credit.state = TRIALS.hashed_state(seed, board.world.width)
            for _ in range(126):
                board.step()
            runs[mode, seed] = (board, lines)
    spin = family(board)
    for seed in (1, 5):
        boards = [runs[mode, seed][0] for mode in (None, BACK)]
        kinds = {
            k: [[e for e in runs[mode, seed][1] if e["event"] == k] for mode in (None, BACK)]
            for k in ("erasure", "face", "credit")
        }
        assert kinds["erasure"][0] == kinds["erasure"][1] and kinds["face"][0] == kinds["face"][1]
        assert meeting_back.first_difference(*(meeting_back.snapshot(b) for b in boards)) is None
        for b in boards:
            assert not b.credit.fronts and b.credit.counts[spin] == 0 and b.total_share(spin)[0] == 0
        close, erasures = kinds["credit"][1][0]["interval"], kinds["erasure"][1]
        assert [(c["node_detector"], c["order"]) for c in kinds["credit"][1]] == [
            ("left", 1),
            ("right", 2),
        ]
        for origin in ((1, 0, 0), (31, 0, 0)):  # the regions' inner Nodes, where the inflow enters
            shells = [e for e in erasures if tuple(e["origin"]) == origin]
            at = tuple(o + f for o, f in zip(origin, board.offset, strict=True))
            farthest = int(distances(board.shape, at, board.world.periodic).max())
            taper = board.world.erasure
            assert [e["interval"] for e in shells] == list(
                range(close + 1, close + farthest + taper + 2)
            )
            assert all(e["distance"] == e["interval"] - close and e["nodes"] <= 2 for e in shells)
            beyond = [e["interval"] for e in shells if e["nodes"] == 0]
            assert beyond == list(range(close + farthest + 1, close + farthest + taper + 2))
        assert len(erasures) == 2 * len(shells) and taper == 3 and close == 40
    assert GATE.verdict(Lattice(load_world(path)), 60)["verdict"] == "MATCH"
    print(
        f"the taper in the two modes: {len(erasures)} erasure lines equal at the seeds 1 and 5, the shells "
        f"to {max(e['interval'] for e in erasures)} on the board of {board.shape[0]}, the realised ports "
        f"{[(m, s, [c['realised'] for c in runs[m, s][1] if c['event'] == 'credit']) for m, s in runs]}"
    )


def test_the_cone_stepped_alone_returns_the_board_runs_close_at_fewer_node_steps(tmp_path, monkeypatch):
    """(k) The cone stepped alone (the owner's word of 2026-10-20; ALGEBRA.md, The meeting's reading, root or back; The interval's dependency radius is one Link): the shipped fifth world (singlet_back_a_b, the cone by default) and the shipped GHZ world (x, y, y) with `meeting: back`, each run whole under the cone and under `reach: board` beside it; the two runs' every output line equal (the credit lines with the realised ports, the parts, the faces), the two boards equal bit for bit at the end, the books equal; the frames' sequence of tick, interval, direction and pass equal and, at every frame of both runs, the hash of every array of the board equal in order (`digest` over `meeting_back.snapshot`: the cone-alone trajectory is the board's at every step and not at the ends alone, the assertion naming the first frame that differs), and at the birth the board equal to the lay bit for bit (frame 0 inside S_0 and outside it alike, the growths all popped); the Node-steps of the reading (`credit.stepped`, in the cone the box with its ring per step, on the board its volume) counted at the same intervals, the cone's fewer at every interval and in all (the saving modest on the shipped boards, which the cone fills early); the growths of the receding faces popped on the way back and replayed on the way forward, the board's growth log and shape at the end the board run's and the record's history stack empty; no refusal."""
    runs = {}
    for folder, name, edit in (
        ("bell_singlet", "singlet_back_a_b.json", {}),
        ("ghz", "ghz_x_y_y.json", {"meeting": BACK}),
    ):
        source = EVENTS / folder / name
        for reach in (None, BOARD):
            edits = {**edit, **({"reach": reach} if reach else {})}
            if edits:
                path = world_beside(
                    tmp_path / f"{folder}_{reach}", source, lambda w, e=edits: w["draw"].update(e)
                )
            else:
                monkeypatch.setattr(world_files, "REPOSITORY_ROOT", TREE)
                path = source
            lines, frames, digests = [], [], []
            board = Lattice(load_world(path), lines.append)
            zero = meeting_back.snapshot(board)

            def seen(t, d, p, b=board, frames=frames, digests=digests, zero=zero):
                frames.append((b.tick, t, d, p))
                digests.append(digest(b))  # the frame's state, every array
                if p > 1 and t == 0:  # the birth: the lay bit for bit, the growths popped
                    assert meeting_back.first_difference(zero, meeting_back.snapshot(b)) is None

            board.observers.append(seen)
            for _ in range(board.world.intervals):
                board.step()
            runs[name, reach] = (board, lines, frames, digests)
        cone, whole = runs[name, None], runs[name, BOARD]
        assert cone[0].credit.reach == CONE and whole[0].credit.reach == BOARD
        assert cone[1] == whole[1] and cone[2] == whole[2] and len(cone[1]) > 100
        first = next((f for f, a, b in zip(cone[2], cone[3], whole[3], strict=True) if a != b), None)
        assert first is None, (
            f"the cone-alone trajectory first differs from the board's at the frame (tick, interval, direction, pass) {first}"
        )
        assert (
            meeting_back.first_difference(
                meeting_back.snapshot(whole[0]), meeting_back.snapshot(cone[0])
            )
            is None
        )
        assert cone[0].books() == whole[0].books() and cone[0].shape == whole[0].shape
        assert cone[0].growths == whole[0].growths and cone[0].credit.popped == [] and cone[0].growths
        stepped = {reach: runs[name, reach][0].credit.stepped for reach in (None, BOARD)}
        assert sorted(stepped[None]) == sorted(stepped[BOARD]) and len(stepped[None]) > 1
        assert all(stepped[None][t] <= stepped[BOARD][t] for t in stepped[None])
        assert sum(stepped[None].values()) < sum(stepped[BOARD].values())
        print(
            f"the cone stepped alone on {name}: Node-steps {sum(stepped[None].values())} against the board's "
            f"{sum(stepped[BOARD].values())}, {len(cone[0].growths)} growths popped and replayed, the lines "
            f"{[c['realised'] for c in cone[1] if c['event'] == 'credit']} in both"
        )


def test_the_cone_stepped_alone_refuses_a_moved_rest_a_broken_cone_and_an_act_outside_by_name(
    tmp_path, monkeypatch
):
    """(l) The three refusals of the cone stepped alone by name (the reader's verdict of 2026-10-20), on the singlet world laid on a chain of 120 Nodes with the regions about the centre where the chain of 33 has them (no growth in 40 intervals, the chain's ends outside the record's cone at the close): a level moved by hand at the interval 39 at 42 Links from the lay, the first step back's ring, refused at that step as the rest moved at the cone's edge (read from the board's own arrays); a level moved inside the cone at 34 Links, far from the record, refused as the cone not holding when the shrinking cone's shell reaches the past the inverse computes for a level with no past; a lay of the books' log at a Node outside the cone at its interval refused as an act outside the record's cone before the step re-presents it; the same world untouched read under the cone and under the board with the two closes equal bit for bit and |G(0)| the lay's 13 Nodes within one Link."""
    sides = {"left": (BELL[0], IDENTITY), "right": (BELL[2], SINGLET)}
    regions = {"left": [44, 45, 46, 47], "right": [73, 74, 75, 76]}

    def world(label, reach=None):
        return spin_world(
            tmp_path / label,
            monkeypatch,
            sides,
            both=True,
            amplitude=64,
            length=120,
            meeting=BACK,
            reach=reach,
            regions=regions,
        )

    def moved(board, x):  # a level moved by hand at the chain's Node x, a new array beside the old
        spin, line = family(board), board.states[family(board)].lines[0]
        now = np.array(line.now, copy=True)
        now[x + board.offset[0], 0, 0] += 1
        board.states[spin].lines[0] = Record(now, line.before, line.remainder)

    for label, x, text in (
        ("edge", 12, "the rest at the record's cone's edge moved at the interval 40"),
        ("inside", 100, "the record's cone did not hold at the interval"),
    ):
        board = Lattice(load_world(world(label)))
        for _ in range(39):
            board.step()
        moved(board, x)
        with pytest.raises(RuntimeError, match=text):
            board.step()
    board = Lattice(load_world(world("act")))
    for _ in range(39):
        board.step()
    board.credit.lays[20] = [reports.lay(20, "spin", 0, [10, 0, 0], [0, 0, 0], [0, 0, 0])]
    with pytest.raises(
        RuntimeError, match=r"an act of the interval 20 stands at the Node \[10, 0, 0\] outside"
    ):
        board.step()
    boards = [Lattice(load_world(world(str(reach), reach))) for reach in (None, BOARD)]
    for board in boards:
        for _ in range(40):
            board.step()
    assert meeting_back.first_difference(*(meeting_back.snapshot(b) for b in boards)) is None
    assert boards[0].credit.cone[0] == 15 and boards[0].credit.reach == CONE
    print(
        f"the three refusals by name; the untouched chain of 120 read alike in the two reaches, |G(0)| {boards[0].credit.cone[0]}"
    )
