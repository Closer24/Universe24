"""A bound body (ALGEBRA.md #the-generator, #what-a-body-is, #the-count-is-the-records-share): the generator lays a body, the GameBoard admits its declared count within the rounding of its family's share in quanta at its Nodes and refuses one beyond it by name, the count is the record's share and stays its family's within Rule3's rounding, the body's Nodes derived from where its share stands. The rotation round (ALGEBRA.md #the-hypotheses-under-their-own-names, The sign holder rotates the two-part record; #the-rows-against-nature (b2) and (f); HIGHLIGHTS.md, There is no sense): the turn is three exact shears, undone bit for bit and within two units of the real rotation; the angle is the holder's level over Gamma and the record of positive Wronskian rotates faster by it; the Wronskian read with the angle is the conserved one, and a record's Wronskian keeps its sign under Rule3; the odd line on the Link shifts the wave number by its angle with the Port's sign, is sourced by the sign's current, the mean of the Node's two a-Links' Wronskian currents, odd under the sense, and written at the wall den T; the act is the file's declaration, refused by name where it is not one of the two or asked of a holder of the content; a one-part reader and the two gates' worlds are untouched; the like-or-unlike look's blind on the committed worlds with the back-in-time gate MATCH, and the plain control's two senses source the holder oppositely and read it plainly."""

import json
import math
from itertools import product

import numpy as np

import event_universe.world_files as world_files
from event_universe import node
from event_universe.core import paces
from event_universe.core.ports import Wrap
from event_universe.core.rule3 import coefficients
from event_universe.features import rotation
from event_universe.game_board import GameBoard
from event_universe.loader.derived import amplitude_bound, count_wall, held_write, turns
from event_universe.loader.world import parse_world, universe_of
from event_universe.world_files import input_digest, load_world
from tests.laws import BACK, CHAIN, EVENTS, PACKET, QUANTA, TOOL, chain_body_world, load_file, refused

DRIFT = load_file("body_drift", EVENTS.parents[1] / "tools" / "body_drift.py")
BUILD = load_file("like_build", EVENTS / "like_or_unlike" / "build_world.py")
LOOK, GAMMA, T, PAIR, RING = EVENTS / "like_or_unlike", 6000, 32768, (4000, 6000), Wrap(True, True, True)
ONE, LEVEL, SHAPE, VACUUM = (1, 1, 1), 100_000, (24, 1, 1), (GAMMA, (GAMMA,) * 3)  # the rulers at rest
OMEGA = math.acos(PAIR[0] / PAIR[1])  # the matter pair's rest rotation in the vacuum
RULE, ZERO = coefficients(*PAIR, GAMMA, GAMMA, GAMMA), np.zeros(SHAPE, dtype=np.int64)
TURNING = universe_of(json.loads((LOOK / "turning.json").read_text(encoding="utf-8")))[1]


def band(k: float) -> float:
    """The matter pair's rotation rate at the wave number k along x on a ring (y and z folded)."""
    return math.acos(PAIR[0] / (3 * PAIR[1]) * (math.cos(k) + 2))


def wave(k: float, omega: float, sense: int = 1) -> list[node.Record]:
    """A plane's two lines on the ring, z = A e^(i (k x - omega t)) for the sense +1 (clockwise, the positive Wronskian) and its conjugate for -1, the level before one interval earlier."""
    at = k * np.arange(SHAPE[0]).reshape(SHAPE)
    re, im = (np.rint(LEVEL * f(at)).astype(np.int64) for f in (np.cos, np.sin))
    re_before, im_before = (np.rint(LEVEL * f(at + omega)).astype(np.int64) for f in (np.cos, np.sin))
    return [node.Record(re, re_before, ZERO), node.Record(sense * im, sense * im_before, ZERO)]


def rate(re: node.Record, im: node.Record, angles, steps: int):  # type: ignore[no-untyped-def]
    """A plane's rotation rate at the Node 0 over `steps` turned intervals, the phase unwrapped, with the swings of the Wronskian read from the booking and of the plain one over the run."""
    phases, booked, plain = [], [], []
    for _ in range(steps):
        (re, im), (_first, second) = node.step_plane(re, im, RULE, RING, angles, GAMMA)
        phases.append(math.atan2(int(im.now[0, 0, 0]), int(re.now[0, 0, 0])))
        booked.append(int(node.wronskian(second, True).sum(dtype=object)))
        plain.append(int(node.wronskian([re, im], True).sum(dtype=object)))
    return np.diff(np.unwrap(phases)).mean(), max(booked) - min(booked), max(plain) - min(plain)


def test_the_laid_body_is_admitted_its_count_kept_and_a_far_count_refused(tmp_path, monkeypatch):
    """The count is the record's share in quanta over the wall 3 den T, read at the start within the law's tolerance of the declared count, every Node of the body carrying a quantum; the start sources the binding holder by the form the hold writes, so the hold's first write returns the start's rest within Rule3's rounding, two units at most at any Node; over a hundred intervals the share's total moves only by Rule3's own rounding (the books' drift, under a quantum per Node of the chain) and no quantum changes family, the quanta at the declared Nodes stay above 0 and the body's Nodes derived for a report are where its share stands; a declared count off the share beyond the rounding refuses the world by name. (a) Random pairs within a million turned at random tangent half-angles within 1 and turned back return bit for bit, the turned pair within two units of the real rotation by 2 arctan(n / w); a turned level is not within twice A (the audit's witness, #1583 B10: (-1, -1) at the tangent half-angle -1 / 4 turns to (-3, -1) at A = 1) but within 2 A + 3, exhaustively over small pairs and walls, and the turning universe's amplitude bound reads a turned record's rooms at A + 2 (the six arrivals and the level before it is stepped against both turned); (b) at one Node of the matter pair in the vacuum, every Port folded, a record of positive Wronskian (z_before = z_now e^(i omega), clockwise) under the time level L rotates at omega + L / Gamma within the half-angle's third order for L = 600 and -600 and at omega for 0, and the Wronskian read from the booking, the step's levels before the turn, stands over 400 intervals within the rounding while the plain one swings by the angle; (c) on a ring of 24 a plane wave at k = pi / 6 under the uniform odd level L_x rotates at the band's omega(k + theta_x) with tan(theta_x / 2) = L_x / (2 Gamma), the read through +x turned by the Link's angle and through -x by its opposite, and under -L_x at omega(k - theta_x); (d) the Wronskian's sign is the record's: the wave of either sense has W of that sign at every Node and keeps it over 100 plain intervals of Rule3 on both lines with one rule, and a real line has none; (e) a plane moving toward +x (z = A e^(i (k x - omega t)), positive Wronskian) has as its sign current the mean of its two x-Links' Wronskian currents, J_x / 2 with J_x = Im(conj(z_i) (z_(+x) - z_(-x))) = 2 A^2 sin k, above 0 at every Node and within the lay's rounding of A^2 sin k, and J_y = J_z = 0, its conjugate, the opposite sense moving alike, the opposite within the read's rounding unit (where the momentum density gave the two the same current; the owner's word of 2026-10-01, 17:17, on the two hands), and a real record, two equal real lines, 0; the holder of the sign under the rotation takes w x that mean of each plane reader into its odd line a by the one write with one remainder over the wall E_s den T (node.write_sources with the sign currents as the axis booked, node.held_write), a real reader sourcing none of it, its time line W over E_s T, and the write back undoes it bit for bit. The act key of a held row: `rotation` on the holder of the sign gives it 1 + 3 lines, its record the time line, its odd lines' walls E_s den T against the tensions' E_s x 3 den T, the plane turned by it (derived.turns) and matter, one part, reading it not at all; `pace` or no key keeps one line and the plain read; an act by another word, and the rotation asked of a holder of the content, are refused by name; the two gates' universe files declare no act, and Bell's world run on its universe with the rotation declared on the holder gives the same lines and books bit for bit as on the file (light and the pair family, real lines, read nothing of the holder, whose odd lines nobody sources). The committed worlds of examples/events/like_or_unlike (the blind expectation the builder's byte for byte, written from the design before any run; the mode files the generator's, the digest binding each to its world): the like, the unlike, the uncharged pair and the four single-body worlds read by tools/body_drift.py over their run: the like pair ends further apart than the unlike pair, the mutual effect's sign ((a - b) / 2 above 0, which no background enters), asserted; the blind's three lines against the background (the uncharged pair's change plus the image force read on the single bodies), like apart, unlike together and the same size to a third of the half-difference, read and printed yes or no beside the plain controls' changes (ENGINE.md, section 6, the looks' numbers: the bodies' response to their own angle is not additive between a pair and a lone body, so the three lines are not met by that background); the back-in-time gate MATCH on the three pairs over their run, each on its own fresh load, and one inverse step more returns its board to the loaded state bit for bit, the state the drift then reads (one load of each pair instead of two: the reading is the fresh load's by that check). The plain control of unlike senses (the dimension's table, ALGEBRA.md #a-familys-declaration): after one interval the two bodies carry the Wronskian of their senses at their Nodes, the holder's record (its one line, light's) stands at or above 0 at the first's Nodes and at or below 0 at the second's, not 0 in all; the plane reads the holder plainly, a level of 100 entering its content as 100 at every Node of both bodies, while matter, real parts of the same pair, reads nothing of it and light does not read its own row. A laid message on a sourced holder is kept (ENGINE.md section 3, the start): on the chain with a rotating body of the charged family, whose Wronskian sources the holder of the sign, and a packet of light laid on the holder's row, the holder's record at tick 0 is the laid message plus a rest static under it, the same in the level now and the level before (the message kept bit for bit), the rest the start lays with the message's own form among the sources (light's form sources the rows of the content, so the rest the start lays on an empty line differs from it, the binding row's by a hump under the packet), that empty line's rest static and positive at the body's Nodes and the remainder the start's."""
    monkeypatch.setattr(world_files, "REPOSITORY_ROOT", tmp_path)
    board = GameBoard(load_world(world := chain_body_world(tmp_path, TOOL)))
    index, binding = ([f.name for f in board.families].index(n) for n in ("matter", "binding"))
    declared, quanta = board.mask(board.world.bodies[0].nodes), board.quanta(index)[0]
    laid, wall = int(quanta[declared].sum()), count_wall(board.families[index], 32768)
    assert abs(laid - QUANTA) <= 2 * int(QUANTA**0.5) + 1 and int(quanta[declared].min()) >= 1
    kept, drifts, source = [], [], board.states[binding].lines[0].now.copy()  # the start's rest
    for _ in range(100):
        board.step()
        assert kept or int(np.abs(board.states[binding].lines[0].now - source).max()) <= 2
        quanta, standing = board.quanta(index)[0], board.body_nodes(0)
        kept.append(int(quanta[standing].sum()))
        assert (quanta[standing] != 0).all() and (standing & declared).any()
        drifts.append((books := board.books()["matter"])["drift"])
        assert abs(books["quanta"] - laid) <= CHAIN  # Rule3's rounding, under a quantum per Node
    print(f"GAMEBOARD body {laid}: quanta {min(kept)}-{max(kept)}, drift {min(drifts)}-{max(drifts)}")
    assert abs(max(drifts, key=abs)) < CHAIN * wall and board.books()["matter"]["pace"] > 0
    mode_path, document = world.with_suffix(".mode.json"), json.loads(world.read_text(encoding="utf-8"))
    document["measured"][0]["nodes"] = [{**n, "count": 1} for n in document["measured"][0]["nodes"]]
    world.write_text(json.dumps(document), encoding="utf-8")
    mode = {**json.loads(mode_path.read_text(encoding="utf-8")), "world_digest": input_digest(document)}
    mode_path.write_text(json.dumps(mode), encoding="utf-8")
    refused("a declared count is within the rounding of the share", lambda: GameBoard(load_world(world)))
    world = chain_body_world(tmp_path, TOOL, senses=(1,), mode=False)  # the body sources the holder
    packet = {**PACKET, "amplitude": 400, "top": dict(x=[5, 5], y=[0, 0], z=[0, 0])}
    document = {**json.loads(world.read_text(encoding="utf-8")), "messages": [packet]}
    world.write_text(json.dumps(document), encoding="utf-8")
    TOOL.main(["--input", str(world), "--sense", "1"])
    board = GameBoard(load_world(world))
    charge = [family.name for family in board.families].index("charge")
    message, light = board.world.messages[0], board.states[charge].lines[0]
    now, before = board.board_array(message.now), board.board_array(message.before)
    for index in board.held:  # the start again on empty time lines: every held row's rest alone
        board.states[index].lines[0] = node.empty_record(board.shape, board.kind)
    board.start()
    rest = board.states[charge].lines[0]
    assert now.any() and not np.array_equal(now, before) and (rest.remainder == light.remainder).all()
    assert np.array_equal(light.now - now, light.before - before)  # the message kept, its rest static
    assert not rest.now.any() and board.record(charge)[0].now[board.body_nodes(0)].min() > 0  # the rows
    draw, shape = np.random.default_rng(1), (4, 3, 2)
    x, y, numerator = (draw.integers(-size, size, shape) for size in (10**6, 10**6, 2 * GAMMA))
    turned, angle = rotation.turned(x, y, numerator, wall := 2 * GAMMA), 2 * np.arctan(numerator / wall)
    assert np.array_equal(rotation.turned(*turned, numerator, wall, -1), (x, y))
    real = (x * np.cos(angle) - y * np.sin(angle), x * np.sin(angle) + y * np.cos(angle))
    assert max(np.abs(turned[0] - real[0]).max(), np.abs(turned[1] - real[1]).max()) < 2
    k, bound = math.pi / 6, amplitude_bound(TURNING, GAMMA, T, 63)
    assert rotation.turned(-1, -1, -1, 4) == (-3, -1) and bound > 0  # the witness, beyond twice A = 1
    for x, y, n, w in product(range(-3, 4), range(-3, 4), range(-6, 7), range(1, 7)):
        assert abs(n) > w or max(map(abs, rotation.turned(x, y, n, w))) <= 2 * max(abs(x), abs(y)) + 3
    rules = (coefficients(*PAIR, GAMMA, *paces.node_paces(GAMMA, c)) for c in (0, GAMMA // 2, GAMMA - 1))
    assert all((sum(r) + w) * 2 * (bound + 2) + abs(s) * bound + w < 2**63 for r, s, w in rules)
    for level in (0, 600, -600):
        re = node.Record(np.full(ONE, LEVEL), np.full(ONE, round(LEVEL * math.cos(OMEGA))), ZERO[:1])
        im = node.Record(ZERO[:1], np.full(ONE, round(LEVEL * math.sin(OMEGA))), ZERO[:1])
        start = int(node.wronskian([re, im], True)[0, 0, 0])  # the positive record, clockwise
        found, booked, plain = rate(re, im, (np.full(ONE, level), (ZERO[:1], ZERO[:1], ZERO[:1])), 400)
        assert start > 0 and abs(found + OMEGA + level / GAMMA) < 3e-4, (level, found)
        assert booked * 1000 < start and (level == 0 or plain > 10 * booked), (booked, plain)
    for level in (600, -600):
        found = rate(*wave(k, band(k)), (ZERO, (np.full_like(ZERO, level), ZERO, ZERO)), 60)[0]
        assert abs(found + band(k + 2 * math.atan(level / (2 * GAMMA)))) < 1e-3, (level, found)
    for sense in (1, -1):
        lines = wave(k, band(k), sense)
        for _ in range(100):
            assert (np.sign(node.wronskian(lines, True)) == sense).all()
            lines = [node.step(line, RULE, RING) for line in lines]
    assert node.wronskian(lines[:1], False) == 0
    names = [f.name for f in TURNING]
    charge, charged, matter, gravity = map(names.index, "charge charged matter gravity".split())
    flux = node.sense_current_of(moving := wave(math.pi / 4, OMEGA), RING)
    assert np.abs(flux[0] - LEVEL * LEVEL * math.sin(math.pi / 4)).max() < 2 * LEVEL
    assert (flux[0] > 0).all() and not flux[1].any() and not flux[2].any()
    assert np.isin(node.sense_current_of(wave(math.pi / 4, OMEGA, -1), RING)[0] + flux[0], (0, 1)).all()
    assert not any(part.any() for part in node.sense_current_of([moving[0], moving[0]], RING))
    own, write = (charged, 0), held_write(TURNING, charge, T)  # the plane's one record owns the row 1
    sign = {own: node.wronskian(moving, True)}
    sources = node.write_sources(charge, TURNING, sign, {own: flux}, write, {own: VACUUM}, GAMMA)
    assert np.array_equal(sources[4], sign[own]) and np.array_equal(sources[5], flux[0])
    held = node.empty_state(TURNING[charge], SHAPE, write.walls, np.int64)
    lines, remainders = node.held_write(held.lines, sources, write.walls, held.write_remainders)
    expected = (flux[0] + 100 * PAIR[1] * T // 2) // (100 * PAIR[1] * T)
    assert np.array_equal(lines[5].now, expected) and not any(map(np.any, sources[:4] + sources[6:]))
    back_lines, before = node.held_write(lines, sources, write.walls, remainders, -1)
    assert all(np.array_equal(a.now, b.now) for a, b in zip(back_lines, held.lines, strict=True))
    assert all(np.array_equal(a, b) for a, b in zip(before, held.write_remainders, strict=True))
    universe = json.loads((LOOK / "turning.json").read_text(encoding="utf-8"))
    rows = {row["name"]: row for row in universe["families"]}
    assert (TURNING[charge].lines, TURNING[charge].record, TURNING[charge].rotation) == (8, 1, True)
    assert turns(TURNING, charged) and not turns(TURNING, matter)
    assert charge not in [read.family for read in TURNING[matter].reads]
    assert write.walls == ((100 * T,) + (100 * PAIR[1] * T,) * 3) * 2  # the walls per row, two rows
    assert held_write(TURNING, gravity, T).walls[1] == 1000 * 3 * PAIR[1] * T
    rows["charge"]["held"]["act"] = "pace"
    assert ((paced := universe_of(universe)[1][charge]).lines, paced.rotation) == (2, False)
    rows["charge"]["held"]["act"] = "sideways"
    refused("act is one of", universe_of, universe)
    rows["gravity"]["held"]["act"], rows["charge"]["held"]["act"] = "rotation", "pace"
    refused("a holder of the content, sourced by the form", universe_of, universe)
    for gate in (json.loads((EVENTS / f"{n}.json").read_bytes()) for n in ("light", "pair")):
        assert not any("act" in row.get("held", {}) for row in gate["families"])
    monkeypatch.setattr(world_files, "REPOSITORY_ROOT", EVENTS.parents[1])
    document = json.loads((bell := EVENTS / "bell" / "bell_a_b.json").read_text(encoding="utf-8"))
    files, runs = world_files.world_files(document), []
    files[bell.with_suffix(".mode.json").name] = json.loads(bell.with_suffix(".mode.json").read_text())
    for act in ({}, {"act": "rotation"}):
        pair = json.loads(json.dumps(files[document["universe"]]))
        next(row for row in pair["families"] if row["name"] == "charge")["held"].update(act)
        world = parse_world(document, {**files, document["universe"]: pair}, input_digest(document))
        board = GameBoard(world, (lines := []).append)
        for _ in range(world.ticks):
            board.step()
        holder = board.states[[f.name for f in board.families].index("charge")]
        runs.append((lines, board.books(), len(holder.lines)))
    assert runs[0][:2] == runs[1][:2] and runs[0][0] and (runs[0][2], runs[1][2]) == (1, 4)
    BUILD.main(["--folder", str(tmp_path)])
    assert (tmp_path / "expectation.json").read_bytes() == (LOOK / "expectation.json").read_bytes()
    expected = json.loads((LOOK / "expectation.json").read_text(encoding="utf-8"))
    gated = {n: GameBoard(load_world(LOOK / f"{n}.json")) for n in ("like", "unlike", "uncharged_pair")}
    for n, board in gated.items():  # the gate on a fresh load; a step back more: the drift's start
        loaded, v, t = BACK.snapshot(board), BACK.verdict(board, board.world.ticks), board.world.ticks
        assert (v["verdict"], v["intervals"], board.step_inverse()) == ("MATCH", t, None), n
        assert BACK.first_difference(loaded, BACK.snapshot(board)) is None and board.tick == 0, n
    readings = {n: DRIFT.drift(gated.get(n, LOOK / f"{n}.json"), None) for n in expected["worlds"]}
    against = DRIFT.compared(expected, readings)
    changes = {name: DRIFT.change_of(reading) for name, reading in readings.items()}
    a, b = against["a_like_less_background"], against["b_unlike_less_background"]
    blind = {key: against[key] for key in ("like_apart", "unlike_together", "same_size")}
    print(f"GAMEBOARD the look: changes {changes}, a {a}, b {b}, blind {blind}")
    assert against["like_further_than_unlike"] and against["half_difference"][0] > 0, against
    board, names = (b := GameBoard(load_world(LOOK / "unlike_plain.json"))), [f.name for f in b.families]
    charged, charge, matter = map(names.index, ("charged", "charge", "matter"))
    plane, light = board.states[charged], board.states[charge]
    board.step()
    first, second = board.body_nodes(0), board.body_nodes(1)
    plain = sum(board.states[i].lines[0].now for i in board.held if i != charge)  # the content holders
    rows, level = [line.now for line in light.lines], board.record(charge)[0].now  # the rows; light
    turn = np.sign(node.wronskian(plane.lines, True))
    assert (turn[first] == 1).all() and (turn[second] == -1).all() and level[second].sum() < 0
    assert level[first].min() >= 0 < level[first].sum() and level[second].max() <= 0
    assert np.array_equal(level, sum(rows)) and not rows[0].any() and len(rows) == 3  # light: the sum
    assert rows[1][first].min() > 0 and rows[2][second].max() < 0  # each record's own row, its write
    assert all((board.read(charged, 1, k)[0] - plain == rows[0] + rows[2 - k]).all() for k in (0, 1))
    assert all(charge not in [x.family for x in board.families[r].reads] for r in (matter, charge))
    assert all(np.array_equal(board.read(r)[0], plain) for r in (matter, charge))  # the holder: content
