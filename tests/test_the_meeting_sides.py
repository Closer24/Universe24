"""The meeting that runs back at N sides and with the erasure's taper (the reader's verdict of 2026-10-19, points 11 and 13; ALGEBRA.md, The meeting's reading, root or back; The meeting's identity), beside tests/test_the_meeting_back.py: (i) the reader's case, a two-part record with the identity pattern on every side read at three sides at the settings (3, 4), (1, 1), (1, 0), where the middle side's weights by the chain rule from the booked joint (1 / 2, 1 / 2) differ from the re-weighted one-side share (49 / 50, 1 / 50) by the cross terms of the third side's read, so the engine draws every side after the first on the chain and the law's two-sided words are the last side's alone, tested equal there; no signalling at N sides, every side's marginal its own; (j) the erasure's taper in the back mode, the fronts the act's as built, the erasure lines and the end state equal bit for bit to the root mode's at any seed on regions whose inflow enters at one Node. The worlds the tests' own (tests/laws_spin.py), no world or family name in the engine."""

from dataclasses import replace
from fractions import Fraction

from event_universe import credit, meeting_back
from event_universe.features.click import drawn, hashed
from event_universe.features.front import distances
from event_universe.lattice import Lattice
from event_universe.loader.draw import BACK
from event_universe.world_files import load_world
from tests.laws import BACK as GATE
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
