"""The one meeting, the click that writes at the record's birth (the owner's words of 2026-10-19 and 2026-10-20; ALGEBRA.md, The click is the meeting of the future with the past: at the root it writes; The meeting's reading; The meeting's identity, the Gram theorem; the design verdicts of 2026-10-20): a record of several parts read by N sides is credited by N draws in the order of the sides' closes, equal closes in the declared order, each side alone at its own place with its own state on its own region's read (the Gram read: the quadratic form of its coefficients on its own second moments with the Gram of the sides after it), its realised port's integer coefficients written into the record's parts at the record's birth inside the run back along the record's light cone, the board run forward from the rewritten birth by Rule3 at one Link per interval, the next side reading the realised term where it stands; every click writes, the last side's read coherent. The tests: (a) the sides' weights equal the chain rule from the parts lines exactly at the four Bell settings in both pattern forms, E and S the law's numbers, the credit lines with their order and the record's scale; (b) the statistics over 48 seeds, the anticorrelation exact; (c) the books, the hole, the fronts and the observers' five passes; (d) a world without a record of several parts byte for byte; (e) the refusals by name; (f) the inverse's exactness in use and the back-in-time gate; (g) the two reaches one meeting with the write at the birth seen in the frames; (h) the shipped GHZ world's three sides under the cone. The worlds the tests' own (tests/laws_spin.py), no world or family name in the engine."""

import json
from dataclasses import replace
from fractions import Fraction

import numpy as np
import pytest

from event_universe import meeting_back, world_files
from event_universe.features.front import ball
from event_universe.lattice import Lattice
from event_universe.loader.draw import BOARD, CONE, body_draw_of, draw_of, windowless_of
from event_universe.world_files import input_digest, load_world
from tests.laws import BACK as GATE
from tests.laws import EVENTS, family, refused, world_beside
from tests.laws import ROOT as TREE
from tests.laws_spin import (
    BELL,
    IDENTITY,
    PORT,
    SINGLET,
    correlation,
    joint_shares,
    marginal_of,
    reduced_write,
    sided,
    spin_world,
    trial,
)

ANTISYMMETRIC = "antisymmetric"  # the family's sign under exchange, the identity pattern on both sides
FORMS = {"crossed": (SINGLET, None), "sign": (IDENTITY, ANTISYMMETRIC)}  # the two pattern forms
SETTINGS = [(a, b) for a in BELL[:2] for b in BELL[2:]]  # the four Bell settings, a b, a b', a' b, a' b'


def squares(coefficients) -> int:  # type: ignore[no-untyped-def]
    return sum(c * c for c in coefficients)


def test_the_sides_draws_give_the_joint_distribution_exactly_through_the_write(tmp_path, monkeypatch):
    """(a) The identity through the write on the singlet at the four Bell settings, for the crossed pattern under no sign and for the identity pattern on both sides under the family's antisymmetric sign: the engine's weights at each side's draw (`credit.Books.weights`, the Gram read of the side's own moments) equal the chain rule from the `parts` lines exactly (`laws_spin.sided`: the first side's marginal, the second side's conditional at the realised port, the record rewritten at its birth by the first side's integer coefficients, one magnitude on the surviving parts at these settings); the realised ports the sides' reads of the board at the close; the two credit lines with the orders 1 and 2, the count 1, nothing left and the record's scale after each write (the norm's square of the coefficients, the second the product); E(a, b) = -cos(theta_a - theta_b), -119 / 169, 119 / 169, -120 / 169, -120 / 169 in both forms, |S| = 478 / 169; every side's marginal 1 / 2 whatever the other side's axis (no signalling)."""
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
            )
            board, lines = trial(path, 40)
            spin = family(board, "spin")
            clicks = [c for c in lines if c["event"] == "credit"]
            realised = [PORT[c["realised"]] for c in clicks]
            shares = joint_shares(lines, sides, sign)
            total = sum(shares.values())
            sided(board, spin, shares, realised)
            books = board.credit
            first = meeting_back.coefficients_of(board.families[spin], books.sides[0][1], True)
            scale = squares(first[realised[0]])
            assert [(c["node_detector"], c["order"], c["count"], c["left"]) for c in clicks] == [
                ("left", 1, 1, 0),
                ("right", 2, 1, 0),
            ]
            written = reduced_write(
                [1] * len(first[0]), list(first[realised[0]])
            )  # after the first write
            assert [c["scale"] for c in clicks] == [
                scale,
                squares(reduced_write(written, list(books.sides[1][1][realised[1]]))),
            ]
            same, different = shares[0, 0] + shares[1, 1], shares[0, 1] + shares[1, 0]
            found[form, a, b] = Fraction(same - different, total)
            assert found[form, a, b] == correlation(a, b)
            marginals[form, "left", a, b] = Fraction(marginal_of(shares, 0)[0], total)
            marginals[form, "right", a, b] = Fraction(marginal_of(shares, 1)[0], total)
            print(
                f"the one meeting, {form}: the axes {a} and {b} read E = {found[form, a, b]}, the realised pair "
                f"{realised}, the weights {[books.weights[(spin, n)] for n, _p in books.sides]}"
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


def test_the_books_balance_and_the_observers_see_the_five_passes(tmp_path, monkeypatch):
    """(c) The books: the (a, b) singlet world over 60 intervals: the two credit lines at the close 40 with the orders 1 and 2, the count 1 and nothing left, the record's scale on each; the counts and the deficits at the close, the hole's faces at 41 and 42 for every line of the record at one Node per side, the two fronts begun at the close after the last side's draw and erasing the count-0 wave shell by shell to 60, the share fallen; the observers: pass 1 to the close with the boundary frame at the close before the first step back, pass 2 the run back to the birth, pass 3 the run forward to the close, pass 4 the second side's run back, pass 5 its run forward and the run on; the tick a forward clock standing at the close through the passes 2 to 5 (observers_api_D.md)."""
    sides = {"left": (BELL[0], IDENTITY), "right": (BELL[2], SINGLET)}
    path = spin_world(tmp_path, monkeypatch, sides, both=True, amplitude=64)
    frames, lines, ticks = [], [], []
    board = Lattice(load_world(path), lines.append)
    board.observers.append(lambda t, direction, passes: frames.append((t, direction, passes)))
    board.observers.append(lambda t, d, p, b=board: ticks.append((b.tick, t, p)))
    for _ in range(40):
        board.step()
    books = board.books()
    for _ in range(20):
        board.step()
    spin = family(board, "spin")
    assert board.tick == 60 and all(k == t for k, t, p in ticks if p == 1)
    assert all(k == 40 for k, _t, p in ticks if 1 < p < 5) and all(
        k >= 40 for k, _t, p in ticks if p == 5
    )
    credits = [c for c in lines if c["event"] == "credit"]
    assert [(c["node_detector"], c["order"], c["count"], c["left"], c["interval"]) for c in credits] == [
        ("left", 1, 1, 0, 40),
        ("right", 2, 1, 0, 40),
    ]
    assert all(c["scale"] >= 1 for c in credits) and credits[1]["scale"] % credits[0]["scale"] == 0
    faces = [f for f in lines if f["event"] == "face"]
    holes = [f for f in faces if f["interval"] == 41]
    assert len(holes) == 2 * board.families[spin].lines and min(f["interval"] for f in faces) == 41
    nodes = {tuple(f["node"]["at"]) for f in holes}
    assert len(nodes) == 2 and {at[0] < 4 for at in nodes} == {True, False}  # one Node per side
    shells = {e["interval"] for e in lines if e["event"] == "erasure"}
    assert shells == set(range(41, 61)) and len(board.credit.fronts) == 2
    assert board.credit.counts[spin] == 0 and board.total_share(spin)[0] < books["spin"]["share"]
    expected = [
        (t, 1, 1) for t in range(1, 41)
    ]  # the loop to 39 and the first run back's boundary frame
    for passes in (2, 4):
        expected += [(t, -1, passes) for t in range(39, -1, -1)]
        expected += [(t, 1, passes + 1) for t in range(1, 41)]
        expected += [
            (40, 1, passes + 1)
        ]  # the second run back's boundary frame; the step's end at the close
    expected += [(t, 1, 5) for t in range(41, 61)]
    assert frames == expected
    print(
        f"the books at the close: {books['spin']}; the credit lines {[(c['realised'], c['scale']) for c in credits]}"
    )


def test_the_meetings_refusals_by_name(tmp_path, monkeypatch):
    """(e) The refusals: the key `meeting` declared with any value (there is one meeting; the key is refused by name); `reach` with `books` (a click that writes runs) or any other word; `reach` on a body's node_detector; `reach` admitted alone with `cone` or `board` and None where absent (the engine reads the cone); the loader's own law of the patterns in tests/test_the_exchange_sign.py."""
    draw = {"window": 40}
    for word in ("root", "back", "elsewhere"):
        refused("there is one meeting", draw_of, {**draw, "meeting": word}, "draw", True)
    refused(
        "the click that runs back writes at the birth and runs",
        draw_of,
        {**draw, "reach": "books"},
        "draw",
        True,
    )
    refused("is 'cone' or 'board'", draw_of, {**draw, "reach": "far"}, "draw", True)
    refused("unknown key 'reach'", draw_of, {**draw, "reach": CONE}, "bodies[0].node_detector")
    refused(
        "unknown key 'meeting'", body_draw_of, {**draw, "meeting": "back"}, "bodies[0].node_detector"
    )
    refused("unknown key 'meeting'", windowless_of, {"meeting": "back"}, "bodies[0].node_detector")
    for word in (BOARD, CONE):
        assert draw_of({**draw, "reach": word}, "draw", True).reach == word
    assert draw_of(draw, "draw", True).reach is None and draw_of(draw, "draw").reach is None
    sides = {"left": (BELL[0], IDENTITY), "right": (BELL[2], SINGLET)}
    path = spin_world(tmp_path, monkeypatch, sides, both=True, amplitude=64)
    world = json.loads(path.read_text(encoding="utf-8"))
    world["draw"]["meeting"] = "back"
    (keyed := tmp_path / "keyed.json").write_text(json.dumps(world), encoding="utf-8")
    mode = json.loads((tmp_path / "spin.mode.json").read_text(encoding="utf-8"))
    mode["world_digest"] = input_digest(world)
    (tmp_path / "keyed.mode.json").write_text(json.dumps(mode), encoding="utf-8")
    refused("there is one meeting", load_world, keyed)
    assert load_world(path).draw.reach is None


def test_the_run_back_and_forward_is_exact_in_the_act_and_the_gate_crosses_the_write(
    tmp_path, monkeypatch
):
    """(f) The inverse's exactness in use: on the singlet world stepped 20 intervals, `meeting_back.run_back` to the record's birth, the lay's interval 0, fires the boundary frame and returns the copy, `run_forward` to 20 returns every array bit for bit with no write standing (the record unwritten, the moments taken on the way), and a level moved outside the record's cone at the birth is refused by name at the return; the back-in-time gate (tools/back_in_time.py, its crossing imported from the engine) reads MATCH up to the interval 39, before the close, and MATCH over 40 intervals after it, across the hole's faces and the fronts' erasure; the frames the loop recorded before the close stand as the possibilities' run by the law (the inverse from after the click returns the realised past), so the gate is pinned on the two sides of the close and the engine's own exactness across the write inside the act (the birth the coefficients times the unwritten parts, the close outside the cone the kept close, asserted at every click)."""
    sides = {"left": (BELL[0], IDENTITY), "right": (BELL[2], SINGLET)}
    path = spin_world(tmp_path, monkeypatch, sides, both=True, amplitude=64)
    frames = []
    board = Lattice(load_world(path))
    board.observers.append(lambda t, direction, passes: frames.append((t, direction, passes)))
    for _ in range(20):
        board.step()
    spin = family(board, "spin")
    kept = meeting_back.run_back(board, spin)
    assert board.interval == 0 and frames[20] == (20, 1, 1)
    assert frames[21:] == [(t, -1, 2) for t in range(19, -1, -1)]
    meeting_back.run_forward(board, spin, 20, kept)
    assert (
        meeting_back.first_difference(
            meeting_back.snapshot(board, kept[0]), meeting_back.snapshot(board)
        )
        is None
        and board.interval == 20
    )
    assert frames[41:] == [(t, 1, 3) for t in range(1, 21)] and board.passes == 3
    kept = meeting_back.run_back(board, spin)
    line = board.states[spin].lines[0]
    now = np.array(line.now, copy=True)
    now[30 + board.offset[0], 0, 0] += 1  # outside the record's cone at the birth
    board.states[spin].lines[0] = replace(line, now=now)
    with pytest.raises(RuntimeError, match="the record's cone"):  # the moved rest, at the cone's edge
        meeting_back.run_forward(board, spin, 20, kept)
    gate = Lattice(load_world(path))
    assert (
        GATE.verdict(gate, 38)["verdict"] == "MATCH" and gate.credit.lays == {}
    )  # to 39, before the close
    gate = Lattice(load_world(path))
    for _ in range(41):  # through the close: the two writes at the birth, the hole and the fronts
        gate.step()
    assert GATE.verdict(gate, 40)["verdict"] == "MATCH"
    print(
        "the inverse in the act: 20 intervals back and forward exact; the gate MATCH before and after the close"
    )


def test_the_two_reaches_read_one_meeting_and_the_write_stands_at_the_birth(tmp_path, monkeypatch):
    """(g) The run back's reach (the owner's word of 2026-10-19): the (a, b) singlet world three times, the reach absent (the engine's cone), `board` and `cone`; the credit lines equal word for word in the three, the books at the close equal, the reach written on no line; the five passes; in the cone's reach the radius t + 1 at the frame's interval, the volume |G(t)| per interval the test's own count by the front's ball and never decreasing, and at every frame of the runs back and forward the arrays outside the ball equal to frame 0 over the board as laid (the locality on the engine, the write inside the cone); at the birth of pass 2 the board the lay bit for bit, at the birth of pass 4 the lay with every part's lines multiplied by the first side's realised coefficient (the write exact in the integers); the tick stands at the close through the act."""
    sides = {"left": (BELL[0], IDENTITY), "right": (BELL[2], SINGLET)}
    runs = {}
    for reach in (None, BOARD, CONE):
        path = spin_world(
            tmp_path / str(reach), monkeypatch, sides, both=True, amplitude=64, reach=reach
        )
        lines, frames, volumes, births = [], [], {}, {}
        board = Lattice(load_world(path), lines.append)
        spin, zero = family(board, "spin"), meeting_back.snapshot(board)
        assert board.credit.reach == (reach or CONE)

        def seen(
            interval,
            direction,
            passes,
            b=board,
            zero=zero,
            frames=frames,
            spin=spin,
            volumes=volumes,
            births=births,
        ):
            frames.append((b.tick, interval, direction, passes, meeting_back.radius(b)))
            if interval == 0:
                births[passes] = meeting_back.snapshot(b)
            if passes == 1 or b.credit.reach != CONE:
                return
            at = [tuple(n + o for n, o in zip(node, b.offset, strict=True)) for node in b.credit.support]
            inside = ball(b.shape, at, interval + 1, b.world.periodic)
            volumes[interval] = int(inside.sum())
            box = tuple(slice(o, o + e) for o, e in zip(b.offset, zero[0][0][1].shape, strict=True))
            outside = ~inside[box]
            for family_zero, state in zip(zero, b.states, strict=True):
                arrays = [a for r in state.lines for a in (r.now, r.before, r.remainder)]
                arrays += list(state.write_remainders)
                for (label, was), now in zip(family_zero, arrays, strict=True):
                    assert not ((np.asarray(now)[box] != was) & outside).any(), (interval, label)

        board.observers.append(seen)
        for _ in range(40):
            board.step()
        assert volumes == {} or volumes == {t: board.credit.cone[t] for t in volumes}
        assert meeting_back.first_difference(zero, births[2]) is None  # the lay, unwritten
        clicks = [c for c in lines if c["event"] == "credit"]
        first = meeting_back.coefficients_of(board.families[spin], board.credit.sides[0][1], True)
        coefficients = first[PORT[clicks[0]["realised"]]]
        width = board.families[spin].width
        for number, (label, laid) in enumerate(zero[spin][: 3 * board.families[spin].lines]):
            written = births[4][spin][number][1]
            c = coefficients[(number // 3) // width]
            expected = laid if label.endswith("remainder") else laid * c
            assert (written == expected).all(), (label, c)  # the write at the birth, bit for bit
        runs[reach] = (board, lines, frames)
    credits = {r: [c for c in lines if c["event"] == "credit"] for r, (_b, lines, _f) in runs.items()}
    assert all(credits[r] == credits[None] for r in credits) and len(credits[None]) == 2
    assert [c["proper"] for c in credits[None]] == [39, 39] and "reach" not in credits[None][0]
    assert all(b.tick == 40 and b.books() == runs[None][0].books() for b, _l, _f in runs.values())
    passes = {r: sorted({f[3] for f in frames}) for r, (_b, _l, frames) in runs.items()}
    assert passes == {None: [1, 2, 3, 4, 5], BOARD: [1, 2, 3, 4, 5], CONE: [1, 2, 3, 4, 5]}
    assert runs[BOARD][0].credit.cone == {}
    cone = runs[CONE][0].credit.cone
    volumes = [cone[t] for t in range(41)]
    assert all(x <= y for x, y in zip(volumes, volumes[1:], strict=False))
    assert volumes[0] == len(runs[CONE][0].credit.support) + 2  # S_0 within one Link on the chain
    radii = [(f[1], f[4]) for f in runs[CONE][2] if f[3] == 2]
    assert radii == [(t, t + 1) for t in range(39, -1, -1)]
    assert [f[4] for f in runs[CONE][2] if f[3] == 3][:40] == list(range(2, 42))
    assert all(f[0] == 40 for f in runs[CONE][2] if f[3] > 1)
    print(
        f"the two reaches: the lines {[(c['realised'], c['scale']) for c in credits[None]]}; the cone's volumes {volumes}"
    )


def test_the_born_pairs_cone_grows_from_its_birth(tmp_path, monkeypatch):
    """(g) The born pair under the cone (the shipped born_a_b world, its `meeting` key dropped): the cone's volume |G(t)| counted from the birth at 17 by the test's own ball equals the engine's at every pass, 2 r + 1 on the chain from the birth, cut to the grown board at the run's end; the volumes printed. The world's atom gives the pair in the dark, so its emission draw is the body's read of its own record alone."""
    monkeypatch.setattr(world_files, "REPOSITORY_ROOT", TREE)
    source = (
        EVENTS / "bell_singlet" / "born_a_b.json"
    )  # the born pair under the cone: the radius from the birth
    born = Lattice(
        load_world(
            world_beside(tmp_path / "born_cone", source, lambda w: w["draw"].pop("meeting", None))
        )
    )
    counted = {}

    def cone_of(interval, _direction, passes, b=born, counted=counted):  # type: ignore[no-untyped-def]
        if passes > 1:
            at = [tuple(n + o for n, o in zip(node, b.offset, strict=True)) for node in b.credit.support]
            counted[interval] = int(
                ball(b.shape, at, interval - b.credit.birth + 1, b.world.periodic).sum()
            )

    born.observers.append(cone_of)
    for _ in range(born.world.intervals):
        born.step()
    assert counted and counted == {
        t: born.credit.cone[t] for t in counted
    }  # |G(t)| from the birth at 17
    assert [born.credit.cone[t] for t in (17, 18, 19)] == [3, 5, 7]  # 2 r + 1 from the birth at 17
    assert (
        born.credit.cone[124] == int(np.prod(born.shape)) < 2 * (124 - 17) + 3
    )  # cut to the grown board
    print(f"the born pair's cone volumes: {[born.credit.cone.get(t) for t in range(17, 125)]}")


def test_the_three_sides_read_one_joint_under_the_cone_on_the_ghz_world(tmp_path, monkeypatch):
    """(h) N sides as the general case: the shipped GHZ world (x, y, y) under the one meeting (the cone), three regions reading light's four parts; the three credit lines in the declared order with the orders 1, 2, 3, the count 1 each and the record's many quanta less one left (one credited per window, no front), the engine's weights at every side's draw equal to the chain rule from the parts lines exactly (every coefficient written 0 or 1 in magnitude: the write exact, the Gram read the chain's), the realised triple the three draws on the states hashed from the declared seed, E_3 = -1 exactly as the blind, every marginal 1 / 2 (no signalling), the observers' seven passes with the tick at the close through the three runs back and forward, and the cone asserted by the engine at every step with no refusal."""
    source = EVENTS / "ghz" / "ghz_x_y_y.json"
    path = world_beside(tmp_path, source, lambda world: world["draw"].pop("meeting", None))
    lines, frames = [], []
    board = Lattice(load_world(path), lines.append)
    light, draw = family(board, "light_ghz"), board.world.draw
    assert draw is not None and board.credit.reach == CONE and len(board.credit.sides) == 3
    board.observers.append(lambda t, d, p, b=board: frames.append((b.tick, t, d, p)))
    for _ in range(board.world.intervals):
        board.step()
    clicks = [c for c in lines if c["event"] == "credit"]
    names = [name for name, _ports in board.credit.sides]
    left = board.credit.counts[light]
    assert [(c["node_detector"], c["order"], c["count"], c["left"]) for c in clicks] == [
        (name, order, 1, left) for order, name in enumerate(names, 1)
    ]
    realised = [PORT[c["realised"]] for c in clicks]
    sides = {r.name: (r.basis, [list(p) for p in r.pattern]) for r in board.world.node_detectors}
    joint = joint_shares(lines, sides, 0, board.families[light].width)
    total = sum(joint.values())
    sided(board, light, joint, realised)
    signs = sum(v * (-1) ** sum(k) for k, v in joint.items())
    assert Fraction(signs, total) == Fraction(-1) and joint[tuple(realised)] > 0  # E_3 the blind's
    for side in range(3):
        assert Fraction(marginal_of(joint, side)[0], total) == Fraction(1, 2)
    assert (
        sorted({f[3] for f in frames}) == [1, 2, 3, 4, 5, 6, 7] and board.tick == board.world.intervals
    )
    assert all(f[0] == 60 for f in frames if f[3] > 1) and left > 0 and not board.credit.fronts
    print(
        f"the GHZ under the cone: the realised triple {realised}, the volumes {[board.credit.cone[t] for t in (0, 10, 30, 60)]}"
    )
