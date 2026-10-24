"""The one meeting, the click that writes at the record's birth (the owner's words of 2026-10-19 and 2026-10-20; ALGEBRA.md, The click is the meeting of the future with the past: at the root it writes; The meeting's reading; The meeting's identity, the Gram theorem; the design verdicts of 2026-10-20): a record of several parts read by N sides is credited by N draws in the order of the sides' closes, equal closes in the declared order, each side alone at its own place with its own state on its own region's read (the Gram read: the quadratic form of its coefficients on its own second moments with the Gram of the sides after it), its realised port's integer coefficients written into the record's parts at the record's birth inside the run back along the record's light cone, the board run forward from the rewritten birth by Rule3 at one Link per interval, the next side reading the realised term where it stands; every click writes, the last side's read coherent. The tests: (a) the sides' weights equal the chain rule from the parts lines exactly at the four Bell settings in both pattern forms, E and S the law's numbers, the credit lines with their order and the record's scale; (b) the statistics over 48 seeds, the anticorrelation exact; (c) the books, the hole, the fronts and the observers' five passes; (d) a world without a record of several parts byte for byte; (e) the refusals by name; (f) the inverse's exactness in use and the back-in-time gate; (g) the one reach, the record's light cone, with the write at the birth seen in the frames; (h) the shipped GHZ world's three sides under the cone. The worlds the tests' own (tests/laws_spin.py), no world or family name in the engine."""

import json
from dataclasses import replace
from fractions import Fraction

import numpy as np
import pytest

from event_universe import meeting_back, world_files
from event_universe.features.front import ball
from event_universe.lattice import Lattice
from event_universe.loader.draw import ports_of
from event_universe.world_files import load_world
from tests.laws import BACK as GATE
from tests.laws import EVENTS, family, world_beside
from tests.laws import ROOT as TREE
from tests.laws_spin import (
    BELL,
    IDENTITY,
    PORT,
    SINGLET,
    correlation,
    spin_world,
)

ANTISYMMETRIC = "antisymmetric"  # the family's sign under exchange, the identity pattern on both sides
SETTINGS = [(a, b) for a in BELL[:2] for b in BELL[2:]]  # the four Bell settings, a b, a b', a' b, a' b'


def test_the_sides_draws_give_the_joint_distribution_exactly_through_the_write_on_the_record():
    """(a) The identity through the write on the singlet at the four Bell settings, for the crossed pattern under no sign and for the identity pattern on both sides under the family's antisymmetric sign (the sixteen declared worlds ran 88 s on the suite's clock): the gate's E at (a, b) is `correlation`'s exact fraction, -119 / 169, 119 / 169, -120 / 169, -120 / 169 in the CHSH order with |S| = 478 / 169; the shipped record examples/events/bell_singlet declares the sign's form (`exchange` antisymmetric, the identity patterns) and names the crossed pattern [[0, 1], [-1, 0]] as the form it equals term by term, its blind the same fractions; the crossed pattern's ports are the determinant's signs on the parts (`ports_of`, no run)."""
    a, a2, b, b2 = BELL
    found = {(x, y): correlation(x, y) for x, y in SETTINGS}
    assert [found[a, b], found[a, b2], found[a2, b], found[a2, b2]] == [
        Fraction(-119, 169),
        Fraction(119, 169),
        Fraction(-120, 169),
        Fraction(-120, 169),
    ]
    assert abs(found[a, b] - found[a, b2] + found[a2, b] + found[a2, b2]) == Fraction(478, 169)
    record = json.loads((EVENTS / "bell_singlet" / "expectation.json").read_text(encoding="utf-8"))
    assert record["exchange"] == ANTISYMMETRIC and record["superseded_pattern"] == SINGLET
    assert (
        record["patterns"] == {"a": IDENTITY, "b": IDENTITY}
        and record["settings_declared_as"] == "basis"
    )
    settings = {k: tuple(v) for k, v in record["settings"].items()}
    assert settings == {"a": a, "a_prime": a2, "b": b, "b_prime": b2}
    for name, e in record["blind"]["correlation"].items():
        x, y = (settings[part] for part in name.split())
        assert Fraction(*e) == found[x, y], name
    assert all(
        Fraction(*m) == Fraction(1, 2) for w in record["blind"]["marginals"].values() for m in w.values()
    )
    for y in BELL[2:]:  # the crossed pattern's ports are the determinant's signs on the parts
        crossed = ports_of(y, tuple(tuple(p) for p in SINGLET))
        plain = ports_of(y, tuple(tuple(p) for p in IDENTITY))
        for port in range(2):
            assert tuple(crossed[port]) == (plain[port][1], (-plain[port][0][0], -plain[port][0][1]))


def test_the_books_balance_and_the_observers_see_the_five_passes(tmp_path, monkeypatch):
    """(c) The books: the (a, b) singlet world over 60 intervals: the two credit lines at the derived window's close (30; the former declared window closed at 40) with the orders 1 and 2, the count 1 and nothing left, the record's scale on each; the counts and the deficits at the close, the hole's faces at 41 and 42 for every line of the record at one Node per side, the two fronts begun at the close after the last side's draw and erasing the count-0 wave shell by shell to 60, the share fallen; the observers: pass 1 to the close with the boundary frame at the close before the first step back, pass 2 the run back to the birth, pass 3 the run forward to the close, pass 4 the second side's run back, pass 5 its run forward and the run on; the tick a forward clock standing at the close through the passes 2 to 5 (observers_api_D.md)."""
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
    credits = [c for c in lines if c["event"] == "credit"]
    close = credits[0][
        "interval"
    ]  # the derived window's close (30 under the derived window, 2026-10-23; the former declared 40)
    assert board.tick == 60 and all(k == t for k, t, p in ticks if p == 1)
    assert all(k == close for k, _t, p in ticks if 1 < p < 5) and all(
        k >= close for k, _t, p in ticks if p == 5
    )  # the board's tick stands at the close through the run back and forward
    assert [(c["node_detector"], c["order"], c["count"], c["left"], c["interval"]) for c in credits] == [
        ("left", 1, 1, 0, close),
        ("right", 2, 1, 0, close),
    ]
    assert all(c["scale"] >= 1 for c in credits) and credits[1]["scale"] % credits[0]["scale"] == 0
    faces = [f for f in lines if f["event"] == "face"]
    holes = [f for f in faces if f["interval"] == close + 1]
    assert (
        len(holes) == 2 * board.families[spin].lines and min(f["interval"] for f in faces) == close + 1
    )
    nodes = {tuple(f["node"]["at"]) for f in holes}
    assert len(nodes) == 2 and {at[0] < 4 for at in nodes} == {True, False}  # one Node per side
    shells = {e["interval"] for e in lines if e["event"] == "erasure"}
    assert shells == set(range(close + 1, 61)) and len(board.credit.fronts) == 2
    assert board.credit.counts[spin] == 0 and board.total_share(spin)[0] < books["spin"]["share"]
    expected = [
        (t, 1, 1) for t in range(1, close + 1)
    ]  # the loop to the close less one and the first run back's boundary frame
    for passes in (2, 4):
        expected += [(t, -1, passes) for t in range(close - 1, -1, -1)]
        expected += [(t, 1, passes + 1) for t in range(1, close + 1)]
        expected += [
            (close, 1, passes + 1)
        ]  # the second run back's boundary frame; the step's end at the close
    expected += [(t, 1, 5) for t in range(close + 1, 61)]
    assert frames == expected
    print(
        f"the books at the close: {books['spin']}; the credit lines {[(c['realised'], c['scale']) for c in credits]}"
    )


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
    close = board.world.draw.window  # the derived window's close (30; the former declared 40)
    gate = Lattice(load_world(path))
    assert (
        GATE.verdict(gate, close - 2)["verdict"] == "MATCH" and gate.credit.lays == {}
    )  # to the interval before the close, no write crossed
    gate = Lattice(load_world(path))
    for _ in range(close + 1):  # through the close: the two writes at the birth, the hole and the fronts
        gate.step()
    assert GATE.verdict(gate, close)["verdict"] == "MATCH"
    print(
        "the inverse in the act: 20 intervals back and forward exact; the gate MATCH before and after the close"
    )


def test_the_cone_is_the_one_reach_and_the_write_stands_at_the_birth(tmp_path, monkeypatch):
    """(g) The run back's one reach, the record's light cone (the owner's word of 2026-10-19 and the law of one Node of 2026-10-23: the region the click runs back is derived from the record's birth by the causal bound, one Link per interval, and no key names it): the (a, b) singlet world run once; two credit lines, the reach written on no line; the five passes; the radius t + 1 at the frame's interval, the volume |G(t)| per interval the test's own count by the front's ball and never decreasing, and at every frame of the runs back and forward the arrays outside the ball equal to frame 0 over the board as laid (the locality on the engine, the write inside the cone); at the birth of pass 2 the board the lay bit for bit, at the birth of pass 4 the lay with every part's lines multiplied by the first side's realised coefficient (the write exact in the integers); the tick stands at the close through the act."""
    sides = {"left": (BELL[0], IDENTITY), "right": (BELL[2], SINGLET)}
    path = spin_world(tmp_path, monkeypatch, sides, both=True, amplitude=64)
    lines, frames, volumes, births = [], [], {}, {}
    board = Lattice(load_world(path), lines.append)
    spin, zero = family(board, "spin"), meeting_back.snapshot(board)

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
        if passes == 1:
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
    close = (
        board.world.draw.window
    )  # the derived window's close (30; the former declared 40), the run to it
    for _ in range(close):
        board.step()
    assert volumes and volumes == {t: board.credit.cone[t] for t in volumes}
    assert meeting_back.first_difference(zero, births[2]) is None  # the lay, unwritten
    clicks = [c for c in lines if c["event"] == "credit"]
    first = meeting_back.coefficients_of(board.families[spin], board.credit.sides[0][1], True)
    coefficients = first[PORT[clicks[0]["realised"]]]
    width = board.families[spin].width
    for number, (label, laid) in enumerate(zero[spin][: 3 * board.families[spin].lines]):
        written = births[4][spin][number][1]
        c = coefficients[(number // 3) // width]
        assert c[1] == 0  # a real-port world: the integers with 0 behind them
        expected = laid if label.endswith("remainder") else laid * c[0]
        assert (written == expected).all(), (label, c)  # the write at the birth, bit for bit
    assert (
        len(clicks) == 2
        and [c["proper"] for c in clicks] == [close - 1] * 2
        and "reach" not in clicks[0]
    )
    assert board.tick == close and sorted({f[3] for f in frames}) == [1, 2, 3, 4, 5]
    cone = board.credit.cone
    counted = [cone[t] for t in range(close + 1)]
    assert all(x <= y for x, y in zip(counted, counted[1:], strict=False))
    assert counted[0] == len(board.credit.support) + 2  # S_0 within one Link on the chain
    radii = [(f[1], f[4]) for f in frames if f[3] == 2]
    assert radii == [(t, t + 1) for t in range(close - 1, -1, -1)]
    assert [f[4] for f in frames if f[3] == 3][:close] == list(range(2, close + 2))
    assert all(f[0] == close for f in frames if f[3] > 1)
    print(
        f"the one reach: the lines {[(c['realised'], c['scale']) for c in clicks]}; the cone's volumes {counted}"
    )


def test_the_born_pairs_cone_grows_from_its_birth(tmp_path, monkeypatch):
    """(g) The born pair under the cone (the shipped born_a_b world, its `meeting` key dropped): the cone's volume |G(t)| counted from the birth at 24 by the test's own ball equals the engine's at every pass, 2 r + 1 on the chain from the birth, cut to the grown board at the run's end; the volumes printed. The world's atom gives the pair in the exact dark, its read finding every digit at the lay's origin, so the emission falls at its window's close, 24, without a draw (`meeting.emission_drawn`), and the two sides' runs back reach the birth from 62 and 124."""
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
        if (
            1 < passes < 5
        ):  # the meeting's own passes, the run back and forward (the run goes on past the close under the derived window, 2026-10-23)
            at = [tuple(n + o for n, o in zip(node, b.offset, strict=True)) for node in b.credit.support]
            counted[interval] = int(
                ball(b.shape, at, interval - b.credit.birth + 1, b.world.periodic).sum()
            )

    born.observers.append(cone_of)
    for _ in range(born.world.intervals):
        born.step()
    assert counted and counted == {t: born.credit.cone[t] for t in counted}  # |G(t)| from the birth
    assert born.credit.birth == born.world.bodies[0].detector.draw.window == 24  # the window's close
    assert [born.credit.cone[t] for t in (24, 25, 26)] == [3, 5, 7]  # 2 r + 1 from the birth at 24
    close = max(born.credit.cone)  # the meeting's close, the last interval the cone was counted at
    assert born.credit.cone[close] == int(np.prod(born.shape)) < 2 * (close - 24) + 3  # the grown board
    print(f"the born pair's cone volumes: {[born.credit.cone.get(t) for t in range(24, close + 1)]}")


def test_the_three_sides_read_one_joint_under_the_cone_on_the_ghz_worlds_record():
    """(h) N sides as the general case, read from the record (the shipped GHZ world (x, y, y) under the cone ran 352 s on the suite's clock): examples/events/ghz/expectation.json declares three sides, a left, b right and c top, light's four parts with the patterns A, B, C, and its rule names the three ports drawn one after another by the sides on their own reads with the write at the birth, the realised triple the gate's; the (x, y, y) world's blind reads E_3 = -1 from its joint table over the eight port triples, every marginal 1 / 2, and the reading's page carries the row; the world file stands in the folder."""
    folder = EVENTS / "ghz"
    record = json.loads((folder / "expectation.json").read_text(encoding="utf-8"))
    assert record["sides"] == {"a": "left", "b": "right", "c": "top"} and len(record["patterns"]) == 3
    assert all(len(pattern) == 4 for pattern in record["patterns"].values())
    assert (
        "three ports drawn one after another" in record["rule"] and "realised triple" in record["rule"]
    )
    joint = {k: Fraction(*v) for k, v in record["blind"]["joint"]["x y y"].items()}
    assert len(joint) == 8 and all(len(k.split()) == 3 for k in joint)
    e_3 = sum(j * (-1) ** k.split().count("minus") for k, j in joint.items()) / sum(joint.values())
    assert e_3 == -1 and record["blind"]["correlation"]["x y y"] == [-1, 1]
    assert all(Fraction(*m) == Fraction(1, 2) for m in record["blind"]["marginals"]["x y y"].values())
    assert "| x y y | -1 |" in (folder / "blind_and_reading.md").read_text(encoding="utf-8")
    assert (folder / f"{record['runs']['x y y']}.json").is_file()
