"""The absorption's weights at one denominator (ALGEBRA.md, The absorption, the draw (a) and (b): where the shares of the bodies closing one drive's interval sum above the unit the rest is 0 and the drive's one quantum goes to one of them in the proportion of their shares; each body's weight is its own transfer share, its entered label squared over its own norm, the weights of bodies of different counts brought to one denominator, the norms' least common multiple, bodies of one count read as before; the mathematician's line, #1793 comment 5981866600 K4, the advisor's second 5981976271 (3), two hands; `lists.absorption`, `credit.Books.unabsorbed_in`)."""

import json
import math
from fractions import Fraction

from event_universe import act, meeting
from event_universe.features.click import drawn
from event_universe.lattice import Lattice
from event_universe.resonance import unit_weight
from event_universe.twist import quarter_turn
from event_universe.world_files import load_world
from tests.laws import EVENTS, ROOT, TOOL, load_file


def test_bodies_of_different_counts_take_by_their_own_transfer_shares(tmp_path, monkeypatch):
    """Two atoms reading one photon, A of count 1 and B of count 2 (the anticoincidence world's two atoms, B's ground part declared at the count 2; B's norm the engine's own, read from the books and not assumed), closing one drive's interval together over 1,200 trials, each trial the first closing body's generator at the trials tool's hashed state of the trial's number, the write step reduced to the books (the drive's count moved, nothing laid) so that the draw alone is read: (i) both bodies fully turned, each body's entered label squared its own norm, each takes at 1/2 within three standard errors and more than three from the 1/5 and 4/5 the smaller body's label squared against the larger body's norm would give (the engine before this line); (ii) A half turned, its entered label squared half its norm, and B untouched, A takes at 1/2 within three standard errors and more than three from 1/8, and B never; (iii) A alone, half turned, at the count 1, the picks bit for bit those of the click's draw over the weights [s_A, N_A - s_A] from the same states, the form before this line, so that nothing of one body per drive moves; the realised frequencies printed."""
    world = json.loads((EVENTS / "anticoincidence" / "one_photon.json").read_text(encoding="utf-8"))
    world["bodies"][1]["parts"][0]["count"] = 2  # the second atom's ground part at the count 2
    (path := tmp_path / "two_counts.json").write_text(json.dumps(world), encoding="utf-8")
    TOOL.main(["--input", str(path)])
    hashed_state = load_file("meeting_trials", ROOT / "tools" / "meeting_trials.py").hashed_state
    board = Lattice(load_world(path))
    a, b = board.credit.bodies
    drive, width, trials = a.declared.transitions[0].drive, board.world.width, 1200
    n_a, n_b = (sum(label * label for label in books.labels) for books in (a, b))
    assert a.counts == [1, 0] and b.counts == [2, 0] and 0 < n_a < n_b  # the engine's own norms

    def booked(board, items):  # the write step reduced to the books: the drive's count moved, no lay
        if items:  # the outcome that none takes writes nothing
            board.credit.counts[items[0].family] += items[0].delta

    monkeypatch.setattr(act, "written", booked)
    monkeypatch.setattr(act, "reported", lambda *args: None)

    def frequencies(closing, shares):
        taken, picks = {books.number: 0 for books in closing}, []
        for seed in range(trials):
            board.credit.counts[drive], closing[0].state = 1, hashed_state(seed, width)
            board.credit.account_ended(drive)
            for books, share in zip(closing, shares, strict=True):
                books.shares = {books.declared.transitions[0]: share}
            done = meeting.absorptions_drawn(board, closing)
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


def test_the_weight_from_the_unit_is_checked_on_the_zeno_calibration():
    """C9 (a) of the click's plan, the transition's weight from the unit (`resonance.unit_weight`): the weight at which one quantum of the drive at resonance, spread over the window as it passes the Node, turns the quarter turn, the ratio of the phase line's quarter turn (9424 acts at Gamma 6000) over S_1 = sqrt(3 W T / (4 sin k)), the plane's size one quantum makes over the window; at W = 48 and T = 32768 S_1 reads 1086 at the Zeno transition [2, 3] (k = pi / 2) and 1291 at the atoms' [5414, 6000] (k = pi / 4), the ratios 8.68 and 7.30 where the files declare 1 and 6. The check on the Zeno calibration (the drive 392 at the weight 1, Itano's pi pulse): the drive carries A^2 W sin k / (3 T) = 75 + 1 / 32 quanta past the body per window, and the declared weight times the root of that count is the derived weight within one part in four hundred, the pi pulse being the derived weight's quarter turn at one quantum per window scaled by the root of the quanta, an identity of the model; so the replacement of the files' weights keeps Itano's column only with the drive re-declared at one quantum per window, 392 over the root, about 45, the owner's call, and the derivation stands beside the declared weight. None for a massive drive and for a resonance outside the massless band ([1, 3], the resonance folder's detuned taker, stands at cos k = -1). The cold reader's line of 2026-10-19 on this identity: A_1 cancels in it, so it tests neither S_1 nor the premise of one quantum turning the quarter; it says that 392 is the quarter-turn amplitude at the weight 1 over the window 48 (pi Gamma / W = 392.7) and that the derived weight is that amplitude over the one-quantum amplitude, the calibration identity by name; the unit's weight carries 1 / sqrt(W) of its window and is no coupling's constant (the check of the same day: the declared weight stands)."""
    board = Lattice(load_world(EVENTS / "zeno" / "zeno_1.json"))
    body, action, quarter = board.credit.bodies[0], board.world.quantum_action, quarter_turn(board)
    transition, window = body.declared.transitions[0], body.declared.draw.window
    light, amplitude = board.families[transition.drive].pair, board.world.packets[0].amplitude
    zeno = unit_weight(quarter, window, action, light, transition.resonance)
    atom = unit_weight(quarter, window, action, light, (5414, 6000))
    assert zeno == (9424, 1086) and atom == (9424, 1291) and (light, amplitude) == ((6000, 6000), 392)
    quanta = Fraction(amplitude**2 * window, 3 * action)  # A^2 W sin k / (3 T), sin k = 1 at pi / 2
    derived = Fraction(*zeno)
    assert quanta == Fraction(2401, 32) and transition.weight == 1
    assert abs(float(derived) / math.sqrt(quanta) - transition.weight) < 1 / 400
    assert unit_weight(quarter, window, action, (1, 1299), (2, 3)) is None  # a massive drive
    assert unit_weight(quarter, window, action, light, (1, 3)) is None  # cos k = -1, no travelling wave
    print(
        f"C9 (a): the weight from the unit {float(derived):.3f} at [2, 3] and {float(Fraction(*atom)):.3f} at "
        f"[5414, 6000] over the window {window}; the Zeno drive {amplitude} carries {float(quanta):.2f} quanta per "
        f"window, its one-quantum amplitude {amplitude / math.sqrt(quanta):.1f}"
    )
