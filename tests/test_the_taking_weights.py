"""The taking's weights at one denominator (ALGEBRA.md, The taking, the draw (a) and (b): where the shares of the bodies closing one drive's interval sum above the unit the rest is 0 and the drive's one quantum goes to one of them in the proportion of their shares; each body's weight is its own transfer share, its entered label squared over its own norm, the weights of bodies of different counts brought to one denominator, the norms' least common multiple, bodies of one count read as before; the mathematician's line, #1793 comment 5981866600 K4, the advisor's second 5981976271 (3), two hands; `meeting.took`, `credit.Books.untaken_in`)."""

import json
import math

from event_universe import meeting
from event_universe.features.click import drawn
from event_universe.game_board import GameBoard
from event_universe.world_files import load_world
from tests.laws import EVENTS, ROOT, TOOL, load_file


def test_bodies_of_different_counts_take_by_their_own_transfer_shares(tmp_path, monkeypatch):
    """Two atoms reading one photon, A of count 1 and B of count 2 (the anticoincidence world's two atoms, B's ground part declared at the count 2; B's norm the engine's own, read from the books and not assumed), closing one drive's interval together over 1,200 trials, each trial the first closing body's generator at the trials tool's hashed state of the trial's number, the write step reduced to the books (the drive's count moved, nothing laid) so that the draw alone is read: (i) both bodies fully turned, each body's entered label squared its own norm, each takes at 1/2 within three standard errors and more than three from the 1/5 and 4/5 the smaller body's label squared against the larger body's norm would give (the engine before this line); (ii) A half turned, its entered label squared half its norm, and B untouched, A takes at 1/2 within three standard errors and more than three from 1/8, and B never; (iii) A alone, half turned, at the count 1, the picks bit for bit those of the click's draw over the weights [s_A, N_A - s_A] from the same states, the form before this line, so that nothing of one body per drive moves; the realised frequencies printed."""
    world = json.loads((EVENTS / "anticoincidence" / "one_photon.json").read_text(encoding="utf-8"))
    world["bodies"][1]["parts"][0]["count"] = 2  # the second atom's ground part at the count 2
    (path := tmp_path / "two_counts.json").write_text(json.dumps(world), encoding="utf-8")
    TOOL.main(["--input", str(path)])
    hashed_state = load_file("meeting_trials", ROOT / "tools" / "meeting_trials.py").hashed_state
    board = GameBoard(load_world(path))
    a, b = board.credit.bodies
    drive, width, trials = a.declared.transitions[0].drive, board.world.width, 1200
    n_a, n_b = (sum(label * label for label in books.labels) for books in (a, b))
    assert a.counts == [1, 0] and b.counts == [2, 0] and 0 < n_a < n_b  # the engine's own norms

    def booked(board, items):  # the write step reduced to the books: the drive's count moved, no lay
        board.credit.counts[items[0].family] += items[0].delta

    monkeypatch.setattr(meeting, "written", booked)
    monkeypatch.setattr(meeting, "reported", lambda *args: None)

    def frequencies(closing, shares):
        taken, picks = {books.number: 0 for books in closing}, []
        for seed in range(trials):
            board.credit.counts[drive], closing[0].state = 1, hashed_state(seed, width)
            board.credit.account_ended(drive)
            for books, share in zip(closing, shares, strict=True):
                books.shares = {books.declared.transitions[0]: share}
            done = meeting.took(board, closing)
            picks.append(min(done) if done else len(closing))
            for number in done:
                taken[number] += 1
        return [taken[books.number] / trials for books in closing], picks

    error = 3 * math.sqrt(0.25 / trials)  # three standard errors of a frequency about 1/2
    (full_a, full_b), _picks = frequencies([a, b], [n_a, n_b])
    (half_a, none_b), _picks = frequencies([a, b], [n_a // 2, 0])
    (alone_a,), picks = frequencies([a], [n_a // 2])
    generator, modulus = a.declared.draw, width + 1
    before = [
        drawn(
            hashed_state(seed, width),
            generator.multiplier,
            generator.increment,
            modulus,
            [n_a // 2, n_a // 2],
        )[0]
        for seed in range(trials)
    ]
    print(
        f"norms {n_a} and {n_b}; both turned A {full_a:.4f} B {full_b:.4f}; A half turned, B untouched"
        f" A {half_a:.4f} B {none_b:.4f}; A alone {alone_a:.4f}; three standard errors {error:.4f}"
    )
    assert abs(full_a - 1 / 2) < error < abs(full_a - 1 / 5) and abs(full_b - 1 / 2) < error
    assert error < abs(full_b - 4 / 5) and full_a + full_b == 1  # one quantum, one taker per trial
    assert abs(half_a - 1 / 2) < error < abs(half_a - 1 / 8) and none_b == 0
    assert picks == before and abs(alone_a - 1 / 2) < error
