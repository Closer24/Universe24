"""The meeting that runs back (the owner's word of 2026-10-19; ALGEBRA.md, The click is the meeting of the future with the past: backward, to the past, the click is a reading and never a write, the credit's reading through the root; the cold design verdict of the day): the world's `draw` gains `meeting`, `root` (the one draw through the root, the default where absent, every shipped world bit for bit) or `back` (`src/event_universe/meeting_back.py`, `lists.readings`): the first side draws at its own place with its own state on its marginal, the result runs back along the record to its birth by Rule3's inverse and forward again by the step at the Nodes alone, bit for bit, nothing written at the birth, the credit re-weights the partner's parts by what the first port read of them and the partner draws at its own place on its re-weighted one-side share. The six tests: (a) the identity P(A) P(B | A) = P(A, B) exact in Fractions from the `parts` lines and in the engine's books' integers, on the singlet at the four Bell settings under both pattern forms; (b) the statistics over 48 seeds per setting, the anticorrelation exact at equal axes; (c) the books balanced as in the root mode; (d) the default bit for bit on the shipped Bell world against the record of origin/main; (e) the refusals by name; (f) the inverse's exactness asserted inside the act, the observers' frames of the three passes and the back-in-time gate across the two readings; and the run back's reach (the owner's word of the same day): (g) the three reaches one meeting with the cone's volumes and the arrays outside the cone at frame 0; (h) the shipped GHZ world's three sides under the cone; the N sides and the taper in tests/test_the_meeting_sides.py. The worlds the tests' own (tests/laws_spin.py), no world or family name in the engine."""

import hashlib
import json
from dataclasses import replace
from fractions import Fraction

import numpy as np
import pytest

from event_universe import credit, meeting_back, world_files
from event_universe.features.click import drawn, hashed
from event_universe.features.front import ball
from event_universe.lattice import Lattice
from event_universe.loader.draw import (
    BACK,
    BOARD,
    BOOKS,
    CONE,
    ROOT,
    body_draw_of,
    draw_of,
    generator_of,
    meeting_of_the_law,
)
from event_universe.node_detector import credit_draw
from event_universe.world_files import input_digest, load_world
from tests.laws import BACK as GATE
from tests.laws import EVENTS, RUN, refused, world_beside
from tests.laws import ROOT as TREE
from tests.laws_spin import (
    BELL,
    IDENTITY,
    PORT,
    SINGLET,
    TRIALS,
    conditional_shares,
    correlation,
    joint_shares,
    rebooked,
    spin_world,
    trial,
)

ANTISYMMETRIC = "antisymmetric"  # the family's sign under exchange, the identity pattern on both sides
FORMS = {"crossed": (SINGLET, None), "sign": (IDENTITY, ANTISYMMETRIC)}  # the two pattern forms
SETTINGS = [(a, b) for a in BELL[:2] for b in BELL[2:]]  # the four Bell settings, a b, a b', a' b, a' b'
SEEDS = 48
MAIN_DIGEST = "4505021d0a017ff8"  # the shipped (a, b) world's 100 intervals of output lines at origin/main fe6010be1


def family(board: Lattice, name: str = "spin") -> int:
    return [f.name for f in board.families].index(name)


def test_the_two_readings_give_the_one_joint_distribution_exactly(tmp_path, monkeypatch):
    """(a) The identity on the singlet in the back mode at the four Bell settings, for the crossed pattern under no sign and for the identity pattern on both sides under the family's antisymmetric sign: the reader's own arithmetic from the `parts` lines (`conditional_shares`: the first side's marginal, the re-weighting lambda at its realised port, the partner's re-weighted share) equals the engine's books' integers (`credit.marginal_of`, `credit.conditioned`, `credit.reweighted_share` over the engine's own accumulation run again, `rebooked`), and P(p) P(q | p) from the sequential shares equals J(p, q) over SUM J exactly in Fractions for every p and q; the two credit lines carry `meeting: back` and the orders 1 and 2 with the count 1 and nothing left, the first side's realised port the draw on the marginal at the state hashed from the declared seed, the side's name and the window, and the partner's the draw on the conditional at its own; E(a, b) = -cos(theta_a - theta_b), -119 / 169, 119 / 169, -120 / 169, -120 / 169, |S| = 478 / 169 in both forms, the joint shares the root mode's (the board the same bit for bit)."""
    found, marginals = {}, {}
    for form, (right, exchange) in FORMS.items():
        for a, b in SETTINGS:
            sides, sign = {"left": (a, IDENTITY), "right": (b, right)}, -1 if exchange else 0
            path = spin_world(
                tmp_path / f"{form}_{a[0]}_{a[1]}_{b[0]}_{b[1]}",
                monkeypatch,
                sides,
                both=True,
                amplitude=64,
                exchange=exchange,
                meeting=BACK,
            )
            board, lines = trial(path, 1, 40)
            spin, draw, modulus = family(board), board.world.draw, board.world.width + 1
            assert draw is not None and draw.meeting == BACK and board.credit.runs_back
            clicks = [c for c in lines if c["event"] == "credit"]
            assert [
                (c["node_detector"], c["meeting"], c["order"], c["count"], c["left"]) for c in clicks
            ] == [
                ("left", BACK, 1, 1, 0),
                ("right", BACK, 2, 1, 0),
            ]
            realised = [PORT[c["realised"]] for c in clicks]
            shares = joint_shares(lines, sides, sign)
            assert rebooked(board, lines) == shares  # the joints and the window's sums per interval anew
            total = sum(shares.values())
            for p in range(2):
                marginal, lambdas, conditional = conditional_shares(lines, sides, sign, 0, p)
                joint = board.credit.joints[spin]
                assert marginal == credit.conditional_of(joint, {}, 0)
                assert lambdas == credit.conditioned(board, spin, {0: p}, 1)  # the law's words
                assert conditional == credit.reweighted_share(board, spin, 1, lambdas)
                chain = credit.conditional_of(joint, {0: p}, 1)  # the one arithmetic the draw reads
                assert sum(conditional) > 0 and (sum(marginal) == total)
                for q in range(2):
                    sequential = Fraction(marginal[p], total) * Fraction(
                        conditional[q], sum(conditional)
                    )
                    assert sequential == Fraction(shares[p, q], total), (form, a, b, p, q, shares)
                    assert Fraction(chain[q], sum(chain)) == Fraction(conditional[q], sum(conditional))
                marginals[form, "left", a, b] = Fraction(marginal[0], total)
                marginals[form, "right", a, b] = Fraction(credit.conditional_of(joint, {}, 1)[0], total)
                states = [hashed(draw.seed, name, 1, modulus) for name in ("left", "right")]
                first = drawn(states[0], draw.multiplier, draw.increment, modulus, marginal)[0]
                assert first == realised[0]  # the first side's realised port, the draw on the marginal
                if p == realised[0]:  # the partner's realised port, the draw on the conditional at p
                    second = drawn(states[1], draw.multiplier, draw.increment, modulus, conditional)[0]
                    assert second == realised[1] and shares[tuple(realised)] > 0
            same, different = shares[0, 0] + shares[1, 1], shares[0, 1] + shares[1, 0]
            found[form, a, b] = Fraction(same - different, total)
            assert found[form, a, b] == correlation(a, b)
            print(
                f"the meeting that runs back, {form}: the axes {a} and {b} read E = {found[form, a, b]}, "
                f"the realised pair {realised}, the first side's marginal {marginal}, the conditional at "
                f"{realised[0]} {conditional_shares(lines, sides, sign, 0, realised[0])[2]}"
            )
    a, a2, b, b2 = BELL
    for form in FORMS:
        assert [found[form, a, b], found[form, a, b2], found[form, a2, b], found[form, a2, b2]] == [
            Fraction(-119, 169),
            Fraction(119, 169),
            Fraction(-120, 169),
            Fraction(-120, 169),
        ]
        assert abs(
            found[form, a, b] - found[form, a, b2] + found[form, a2, b] + found[form, a2, b2]
        ) == (Fraction(478, 169))
        for x in (a, a2):  # no signalling: a side's marginal the same whatever the other side's axis
            assert marginals[form, "left", x, b] == marginals[form, "left", x, b2] == Fraction(1, 2)
        for y in (b, b2):
            assert marginals[form, "right", a, y] == marginals[form, "right", a2, y] == Fraction(1, 2)


def test_the_realised_pairs_over_48_seeds_read_the_correlation_and_the_anticorrelation_is_exact(
    tmp_path, monkeypatch
):
    """(b) The statistics in the back mode: the board's run to the close does not depend on the seed (the draws enter at the close alone), so the realised pair of a seed is the engine's two draws at the close on the engine's own weights, the first side's state and the partner's hashed from the seed, the side's name and the window as the run hashes them (`credit_draw` with the side, `credit.Books.states`); over 48 seeds per setting the realised pairs' E lies within three binomial scatters of the share's E (-119 / 169, 119 / 169, -120 / 169, -120 / 169), and at equal axes the partner's weight at the first side's port is 0 exactly, the second draw with one outcome, every pair opposite; at each setting one more seed is run whole through the act, its credit lines' realised pair the emulated draws' (the run back and forward inside, bit for bit)."""
    for a, b in [*SETTINGS, ((3, 1), (3, 1))]:
        sides = {"left": (a, IDENTITY), "right": (b, SINGLET)}
        path = spin_world(
            tmp_path / f"{a[0]}_{a[1]}_{b[0]}_{b[1]}",
            monkeypatch,
            sides,
            both=True,
            amplitude=64,
            meeting=BACK,
        )
        board, lines = trial(path, 1, 40)
        spin, shares = family(board), rebooked(board, lines)
        marginal = credit.conditional_of(board.credit.joints[spin], {}, 0)
        conditional = {p: credit.conditional_of(board.credit.joints[spin], {0: p}, 1) for p in range(2)}
        pairs = []
        for seed in range(SEEDS):
            board.credit.declaration, board.credit.states = replace(board.world.draw, seed=seed), {}
            p = credit_draw(board, marginal, "left")
            pairs.append((p, credit_draw(board, conditional[p], "right")))
        same, expected = (
            sum(p == q for p, q in pairs),
            Fraction(shares[0, 0] + shares[1, 1], sum(shares.values())),
        )
        scatter = (SEEDS * expected * (1 - expected)) ** 0.5
        assert abs(same - SEEDS * expected) <= 3 * scatter, (a, b, same, expected)
        read = Fraction(2 * same - SEEDS, SEEDS)
        if a == b:  # the anticorrelation exact: the second draw has one outcome
            assert same == 0 and all(conditional[p][p] == 0 < conditional[p][1 - p] for p in range(2))
        seed, lines = 2, []
        other = Lattice(load_world(path), lines.append)
        other.credit.declaration = replace(other.world.draw, seed=seed)
        for _ in range(40):
            other.step()
        clicks = [c for c in lines if c["event"] == "credit"]
        assert (
            tuple(PORT[c["realised"]] for c in clicks) == pairs[seed] and other.credit.counts[spin] == 0
        )
        print(
            f"the meeting that runs back at {a}, {b}: {same} of {SEEDS} pairs alike, E read {read} against "
            f"{correlation(a, b)} (the scatter {scatter:.2f} pairs); the seed {seed} run whole realised {pairs[seed]}"
        )


def test_the_books_balance_as_the_roots_and_the_observers_see_the_three_passes(tmp_path, monkeypatch):
    """(c) The books balanced: the (a, b) singlet world in the root mode and in the back mode over 60 intervals, the same seed; two credit lines each at the close with the count 1 and nothing left, equal line by line but for the port realised, the parts kept and the back mode's two words; the counts, the deficits and the books' line equal at the close; the hole's faces at 41 and 42 for every line of the record at one Node per side, the two fronts begun at 40 and erasing the count-0 wave shell by shell to 60 in both modes; the root mode's lines without the two words. The observers: the root run fires (t, +1, 1) once per step; the back run fires pass 1 to the close with the boundary frame at the close before the first step back, pass 2 the run back to 0, pass 3 the run forward to the close, the close again after the acts and the run on (observers_api_D.md)."""
    sides = {"left": (BELL[0], IDENTITY), "right": (BELL[2], SINGLET)}
    runs = {}
    for mode in (None, BACK):
        path = spin_world(
            tmp_path / str(mode), monkeypatch, sides, both=True, amplitude=64, meeting=mode
        )
        frames, lines, ticks = [], [], []
        board = Lattice(load_world(path), lines.append)
        board.observers.append(
            lambda t, direction, passes, frames=frames: frames.append((t, direction, passes))
        )
        board.observers.append(lambda t, d, p, b=board, ticks=ticks: ticks.append((b.tick, t, p)))
        board.credit.state = TRIALS.hashed_state(1, board.world.width)
        for _ in range(40):
            board.step()
        books = board.books()
        for _ in range(20):
            board.step()
        runs[mode] = (board, lines, frames, books, ticks)
        assert board.tick == 60 and all(
            k == t for k, t, p in ticks if p == 1
        )  # the tick a forward clock
        assert all(k == 40 for k, _t, p in ticks if p == 2) and all(
            k >= 40 for k, _t, p in ticks if p == 3
        )
    spin = family(runs[None][0])
    credits = {m: [c for c in r[1] if c["event"] == "credit"] for m, r in runs.items()}
    stripped = [
        [{k: v for k, v in c.items() if k not in ("realised", "kept", "meeting", "order")} for c in cs]
        for cs in credits.values()
    ]
    assert stripped[0] == stripped[1] and [c["count"] for c in credits[BACK]] == [1, 1]
    assert [c["left"] for c in credits[BACK]] == [0, 0] and [c["interval"] for c in credits[BACK]] == [
        40,
        40,
    ]
    assert [(c["meeting"], c["order"]) for c in credits[BACK]] == [(BACK, 1), (BACK, 2)]
    assert all("meeting" not in c and "order" not in c for c in credits[None])
    assert runs[None][3] == runs[BACK][3] and runs[None][0].credit.counts == runs[BACK][0].credit.counts
    faces = {m: [f for f in r[1] if f["event"] == "face"] for m, r in runs.items()}
    lines_of_the_record = runs[None][0].families[spin].lines
    for found in faces.values():  # the hole's faces at 41, the first front shell's from 42 on
        holes = [f for f in found if f["interval"] == 41]
        assert len(holes) == 2 * lines_of_the_record and min(f["interval"] for f in found) == 41
        nodes = {tuple(f["node"]["at"]) for f in holes}
        assert len(nodes) == 2 and {at[0] < 4 for at in nodes} == {True, False}  # one Node per side
    for mode, (
        board,
        lines,
        _frames,
        books,
        _ticks,
    ) in runs.items():  # the fronts erasing the count-0 wave
        shells = {e["interval"] for e in lines if e["event"] == "erasure"}
        assert shells == set(range(41, 61)) and len(board.credit.fronts) == 2, mode
        assert board.credit.counts[spin] == 0 and board.total_share(spin)[0] < books["spin"]["share"]
    run = [(t, 1, 1) for t in range(1, 61)]
    assert runs[None][2] == run
    back = [(t, 1, 1) for t in range(1, 41)] + [(t, -1, 2) for t in range(39, -1, -1)]
    back += [(t, 1, 3) for t in range(1, 41)] + [(t, 1, 3) for t in range(40, 61)]
    assert runs[BACK][2] == back
    print(
        f"the books at the close in both modes: {runs[BACK][3]['spin']}; the realised pairs root "
        f"{[c['realised'] for c in credits[None]]} and back {[c['realised'] for c in credits[BACK]]}"
    )


def test_the_default_is_the_one_draw_bit_for_bit_on_the_shipped_bell_world(monkeypatch):
    """(d) The default bit for bit: the shipped (a, b) Bell world declares no `meeting`, loads with `root`, and its 100 intervals of output lines (the kinds tools/run_inputs.py writes) have the digest of origin/main's record, written by tools/run_inputs.py at fe6010be1 (MAIN_DIGEST); no line carries the two words and the books' back run's own entries stay empty (the lays' log, the sides' states, the sums per interval)."""
    monkeypatch.setattr(world_files, "REPOSITORY_ROOT", TREE)
    world = load_world(EVENTS / "bell" / "bell_a_b.json")
    assert world.draw is not None and world.draw.meeting == ROOT
    lines = []
    board = Lattice(world, lines.append)
    assert not board.credit.runs_back
    for _ in range(world.intervals):
        board.step()
    kept = [line for line in lines if line["event"] in RUN.LINES]
    canonical = json.dumps(kept, sort_keys=True, separators=(",", ":"))
    assert hashlib.sha256(canonical.encode()).hexdigest()[:16] == MAIN_DIGEST, len(kept)
    assert not any("meeting" in line or "order" in line for line in kept)
    assert board.credit.lays == {} and board.credit.states == {} and board.credit.levels == {}
    assert board.credit.conditioning == {} and board.passes == 1 and board.heading == 1


def test_the_meetings_refusals_by_name(tmp_path, monkeypatch):
    """(e) The refusals: a value of `meeting` other than `root` or `back`; `meeting` on a body's node_detector, with its window or the probe's generator alone (the world's draw's word); `back` on one side, on a one-part record and on a record given a quantum during the run (standing in one part at its birth), each by hand on the loader's own function, three sides admitted, N the general case; and at load, the singlet world with one side under `back`; `root` and the absent key admitted alike."""
    draw = {
        "window": 40,
        "seed": 24,
        "multiplier": 6364136223846793005,
        "increment": 1442695040888963407,
    }
    refused("is 'root' or 'back'", draw_of, {**draw, "meeting": "elsewhere"}, "draw", True)
    refused("word of the back mode", draw_of, {**draw, "reach": CONE}, "draw", True)  # no meeting
    refused("word of the back mode", draw_of, {**draw, "meeting": ROOT, "reach": BOARD}, "draw", True)
    refused(
        "is 'board', 'cone' or 'books'", draw_of, {**draw, "meeting": BACK, "reach": "far"}, "draw", True
    )
    refused("unknown key 'reach'", draw_of, {**draw, "reach": CONE}, "bodies[0].node_detector")
    for word in (BOARD, CONE, BOOKS):
        assert draw_of({**draw, "meeting": BACK, "reach": word}, "draw", True).reach == word
    assert draw_of({**draw, "meeting": BACK}, "draw", True).reach is None  # the engine reads the cone
    assert (
        draw_of(draw, "draw", True).meeting
        == ROOT
        == draw_of({**draw, "meeting": ROOT}, "draw", True).meeting
    )
    assert (
        draw_of({**draw, "meeting": BACK}, "draw", True).meeting == BACK
        and draw_of(draw, "draw").meeting == ROOT
    )
    refused("unknown key 'meeting'", draw_of, {**draw, "meeting": BACK}, "bodies[0].node_detector")
    refused("unknown key 'meeting'", body_draw_of, {**draw, "meeting": BACK}, "bodies[0].node_detector")
    generator = {k: v for k, v in draw.items() if k != "window"}
    refused(
        "unknown key 'meeting'", generator_of, {**generator, "meeting": BACK}, "bodies[0].node_detector"
    )
    sides = {"left": (BELL[0], IDENTITY), "right": (BELL[2], SINGLET)}
    path = spin_world(tmp_path, monkeypatch, sides, both=True, amplitude=64)
    families = load_world(path).families
    spin, charge = ([f.name for f in families].index(name) for name in ("spin", "charge"))
    back, pattern = draw_of({**draw, "meeting": BACK}, "draw", True), ((1, 0), (0, 1))
    meeting_of_the_law(back, [pattern, pattern], [spin], [], families)  # admitted: two sides, two parts
    meeting_of_the_law(
        draw_of(draw, "draw", True), [pattern], [charge], [], families
    )  # the root asks nothing
    meeting_of_the_law(None, [pattern] * 3, [charge], [spin], families)
    refused("two or more sides", meeting_of_the_law, back, [pattern], [spin], [], families)
    refused("two or more sides", meeting_of_the_law, back, [pattern, pattern], [charge], [], families)
    refused("stands in one part", meeting_of_the_law, back, [pattern, pattern], [spin], [spin], families)
    meeting_of_the_law(
        back, [pattern] * 3, [spin], [], families
    )  # three sides admitted, N the general case
    alike = (1,) * families[spin].parts  # the laid lines weighted alike, so the parts
    meeting_of_the_law(back, [pattern, pattern], [spin], [], families, [alike])
    differ = alike[:-1] + (2,)  # one line weighted 2: the parts not laid alike, refused by name
    refused(
        "weights that differ",
        meeting_of_the_law,
        back,
        [pattern, pattern],
        [spin],
        [],
        families,
        [differ],
    )
    world = json.loads(path.read_text(encoding="utf-8"))
    world["draw"]["meeting"], world["node_detectors"] = BACK, world["node_detectors"][:1]
    (one := tmp_path / "one.json").write_text(json.dumps(world), encoding="utf-8")
    mode = json.loads((tmp_path / "spin.mode.json").read_text(encoding="utf-8"))
    mode["world_digest"] = input_digest(world)
    (tmp_path / "one.mode.json").write_text(json.dumps(mode), encoding="utf-8")
    refused("two or more sides", load_world, one)
    world["node_detectors"] = json.loads(path.read_text(encoding="utf-8"))["node_detectors"]
    (two := tmp_path / "two.json").write_text(json.dumps(world), encoding="utf-8")
    mode["world_digest"] = input_digest(world)
    (tmp_path / "two.mode.json").write_text(json.dumps(mode), encoding="utf-8")
    assert load_world(two).draw.meeting == BACK  # the same world with its two sides loads


def test_the_run_back_and_forward_is_exact_in_the_act_and_the_gate_crosses_the_two_readings(
    tmp_path, monkeypatch
):
    """(f) The inverse's exactness in use: on the singlet world in the root mode stepped 20 intervals, `meeting_back.run_back` to the lay's interval 0 fires the boundary frame and returns the copy, `run_forward` to 20 returns every array bit for bit (the same with a conditioning written in the books, which touches no array), and a level moved between the two is refused by name at the return; the back-in-time gate (tools/back_in_time.py, its crossing imported from the engine) reads MATCH on the back-mode world over 45 intervals, across the two readings' close at 40 and the hole's faces, the engine's own log of the lays crossed beside the tool's lines; the lays' log on the back-mode world of the singlet is empty (no act lays a level before the close)."""
    sides = {"left": (BELL[0], IDENTITY), "right": (BELL[2], SINGLET)}
    path = spin_world(tmp_path / "root", monkeypatch, sides, both=True, amplitude=64)
    frames = []
    board = Lattice(load_world(path))
    board.observers.append(lambda t, direction, passes: frames.append((t, direction, passes)))
    for _ in range(20):
        board.step()
    spin, kept = family(board), meeting_back.run_back(board, 0)
    assert (
        board.interval == 0
        and frames[20] == (20, 1, 1)
        and frames[21:] == [(t, -1, 2) for t in range(19, -1, -1)]
    )
    board.credit.conditioning[spin] = [1, -1]  # a conditioning in the books touches no array
    meeting_back.run_forward(board, 20, kept)
    assert (
        meeting_back.first_difference(kept, meeting_back.snapshot(board)) is None
        and board.interval == 20
    )
    assert frames[41:] == [(t, 1, 3) for t in range(1, 21)] and board.passes == 3
    kept = meeting_back.run_back(board, 0)
    board.states[spin].lines[0].now[
        tuple(n + o for n, o in zip((16, 0, 0), board.offset, strict=True))
    ] += 1
    with pytest.raises(RuntimeError, match="the run back and forward of the meeting returned"):
        meeting_back.run_forward(board, 20, kept)
    back = spin_world(tmp_path / "back", monkeypatch, sides, both=True, amplitude=64, meeting=BACK)
    gate = Lattice(load_world(back))
    assert GATE.verdict(gate, 45)["verdict"] == "MATCH" and gate.credit.lays == {}
    print(
        f"the inverse in the act: {board.interval} intervals back and forward exact; the gate MATCH over 45"
    )


def test_the_three_reaches_read_one_meeting_and_the_cone_holds_the_record(tmp_path, monkeypatch):
    """The run back's reach (the owner's word of 2026-10-19; ALGEBRA.md, The meeting's reading, root or back): the (a, b) singlet world four times, the reach absent (the engine's cone), `board`, `cone` and `books`; the credit lines equal word for word in the four (the realised ports, the parts kept, the count, the proper clocks of the regions), the joint integers, E and the books at the close equal, the reach written on no line; the books' reach runs nothing (one pass, no frame of the run back, the cone's volumes empty), the board's and the cone's the three passes; in the cone's reach the radius is t + 1 at the frame's interval, decreasing by one per step back to the lay's Nodes (the state at the birth the lay, bit for bit) and growing by one per step forward, the volume |G(t)| per interval the test's own count by the front's ball and never decreasing in t, and at every frame of the run back and forward the arrays outside the ball equal to frame 0 over the board as laid (the record's levels 0 there, the holders at their rest), the locality on the engine; the tick stands at the close through the act."""
    sides = {"left": (BELL[0], IDENTITY), "right": (BELL[2], SINGLET)}
    runs = {}
    for reach in (None, BOARD, CONE, BOOKS):
        path = spin_world(
            tmp_path / str(reach), monkeypatch, sides, both=True, amplitude=64, meeting=BACK, reach=reach
        )
        lines, frames, volumes = [], [], {}
        board = Lattice(load_world(path), lines.append)
        spin, zero = family(board), meeting_back.snapshot(board)  # frame 0, the test's own copy
        assert board.credit.reach == (reach or CONE) and board.world.draw is not None

        def seen(
            interval, direction, passes, b=board, zero=zero, frames=frames, spin=spin, volumes=volumes
        ):
            frames.append((b.tick, interval, direction, passes, meeting_back.radius(b)))
            if passes == 1 or not b.credit.support:
                return
            at = [tuple(n + o for n, o in zip(node, b.offset, strict=True)) for node in b.credit.support]
            inside = ball(b.shape, at, interval + 1, b.world.periodic)
            volumes[interval] = int(inside.sum())  # the test's own count of |G(t)|, the engine's after
            box = tuple(slice(o, o + e) for o, e in zip(b.offset, zero[0][0][1].shape, strict=True))
            outside = ~inside[box]  # the board as laid, outside the cone
            for family_zero, state in zip(zero, b.states, strict=True):
                arrays = [a for r in state.lines for a in (r.now, r.before, r.remainder)]
                arrays += list(state.write_remainders)
                for (label, was), now in zip(family_zero, arrays, strict=True):
                    assert not ((np.asarray(now)[box] != was) & outside).any(), (interval, label)
            for line in b.states[spin].lines:
                assert not line.now[~inside].any() and not line.before[~inside].any()
            if interval == 0:
                assert meeting_back.first_difference(zero, meeting_back.snapshot(b)) is None  # the lay

        board.observers.append(seen)
        for _ in range(40):
            board.step()
        assert volumes == {} or volumes == {
            t: board.credit.cone[t] for t in volumes
        }  # the engine's |G(t)|
        runs[reach] = (board, lines, frames)
    credits = {r: [c for c in lines if c["event"] == "credit"] for r, (_b, lines, _f) in runs.items()}
    assert all(credits[r] == credits[None] for r in credits) and len(credits[None]) == 2
    assert [c["proper"] for c in credits[None]] == [39, 39] and "reach" not in credits[None][0]
    joints = {r: rebooked(b, lines) for r, (b, lines, _f) in runs.items()}
    assert all(joints[r] == joints[None] for r in joints)
    assert all(b.tick == 40 and b.books() == runs[None][0].books() for b, _l, _f in runs.values())
    passes = {r: sorted({f[3] for f in frames}) for r, (_b, _l, frames) in runs.items()}
    assert passes == {None: [1, 2, 3], BOARD: [1, 2, 3], CONE: [1, 2, 3], BOOKS: [1]}
    assert runs[BOOKS][0].credit.cone == {} and runs[BOARD][0].credit.cone == {}
    cone = runs[CONE][0].credit.cone
    volumes = [cone[t] for t in range(41)]
    assert all(x <= y for x, y in zip(volumes, volumes[1:], strict=False))
    assert volumes[0] == len(runs[CONE][0].credit.support) + 2  # S_0 within one Link on the chain
    radii = [(f[1], f[4]) for f in runs[CONE][2] if f[3] == 2]
    assert radii == [
        (t, t + 1) for t in range(39, -1, -1)
    ]  # the radius t + 1, down by one per step back
    assert [f[4] for f in runs[CONE][2] if f[3] == 3][:40] == list(range(2, 42))  # up by one forward
    assert all(f[0] == 40 for f in runs[CONE][2] if f[3] > 1)  # the tick stands at the close
    print(
        f"the three reaches: the lines {[(c['realised'], c['proper']) for c in credits[None]]}; the cone's volumes {volumes}"
    )


def test_the_three_sides_read_one_joint_under_the_cone_on_the_ghz_world(tmp_path, monkeypatch):
    """N sides as the general case (the owner's word of 2026-10-19): the shipped GHZ world (x, y, y) with `meeting: back` on its draw and nothing more (the cone), three regions reading light's four parts; the three credit lines in the declared order with the orders 1, 2, 3, the count 1 each and the record's many quanta less one left (one credited per window, no front), the chain of the engine's conditionals from the booked joint, P(p_1) P(p_2 | p_1) P(p_3 | p_1, p_2), equal to J / SUM J exactly for every triple (the test's own sums over the joint), the realised triple the three draws on the states hashed from the declared seed, E_3 = -1 exactly as the root's blind, every marginal 1 / 2 (no signalling), the observers' five passes with the tick at the close through the two runs back and forward, and the cone asserted by the engine at every step with no refusal."""
    source = EVENTS / "ghz" / "ghz_x_y_y.json"
    monkeypatch.setattr(
        world_files, "REPOSITORY_ROOT", tmp_path
    )  # restored after the test; world_beside moves the root
    path = world_beside(tmp_path, source, lambda world: world["draw"].update(meeting=BACK))
    lines, frames = [], []
    board = Lattice(load_world(path), lines.append)
    light, draw, modulus = family(board, "light_ghz"), board.world.draw, board.world.width + 1
    assert draw is not None and board.credit.reach == CONE and len(board.credit.sides) == 3
    board.observers.append(lambda t, d, p, b=board: frames.append((b.tick, t, d, p)))
    for _ in range(board.world.intervals):
        board.step()
    clicks = [c for c in lines if c["event"] == "credit"]
    names = [name for name, _ports in board.credit.sides]
    left = board.credit.counts[
        light
    ]  # the record of many quanta: one credited per window, the rest standing
    assert [(c["node_detector"], c["order"], c["count"], c["left"]) for c in clicks] == [
        (name, order, 1, left) for order, name in enumerate(names, 1)
    ]
    realised = [PORT[c["realised"]] for c in clicks]
    joint = rebooked(board, lines, "light_ghz")
    total = sum(joint.values())
    for triple in joint:
        chain, fixed = Fraction(1), {}
        for side, port in enumerate(triple):
            weights = credit.conditional_of(joint, fixed, side)
            own = [
                sum(
                    v
                    for k, v in joint.items()
                    if k[side] == q and all(k[s] == f for s, f in fixed.items())
                )
                for q in range(2)
            ]
            assert weights == own and sum(weights) > 0
            chain *= Fraction(weights[port], sum(weights))
            fixed[side] = port
        assert chain == Fraction(joint[triple], total), triple
    fixed = {}
    for side, (name, port) in enumerate(zip(names, realised, strict=True)):
        state = hashed(draw.seed, name, 1, modulus)
        weights = credit.conditional_of(joint, fixed, side)
        assert drawn(state, draw.multiplier, draw.increment, modulus, weights)[0] == port
        fixed[side] = port
    signs = sum(v * (-1) ** sum(k) for k, v in joint.items())
    assert Fraction(signs, total) == Fraction(-1) and joint[tuple(realised)] > 0  # E_3 the blind's
    for side in range(3):
        assert Fraction(credit.conditional_of(joint, {}, side)[0], total) == Fraction(1, 2)
    assert sorted({f[3] for f in frames}) == [1, 2, 3, 4, 5] and board.tick == board.world.intervals
    assert all(f[0] == 60 for f in frames if f[3] > 1) and left > 0 and not board.credit.fronts
    print(
        f"the GHZ under the cone: the realised triple {realised}, the volumes {[board.credit.cone[t] for t in (0, 10, 30, 60)]}"
    )
