"""A bound body (ALGEBRA.md #the-generator, #what-a-body-is, #the-count-is-the-records-share): the generator lays a body, the GameBoard admits its declared count within the rounding of its family's share in quanta at its Nodes and refuses one beyond it by name, the count is the record's share and stays its family's within Rule3's rounding, the body's Nodes derived from where its share stands. The rotation round (ALGEBRA.md #the-hypotheses-under-their-own-names, The sign holder rotates the two-part record; #the-rows-against-nature (b2) and (f); HIGHLIGHTS.md, There is no sense): the turn is three exact shears, undone bit for bit and within two units of the real rotation; the angle is the holder's level over Gamma and the record of positive Wronskian rotates faster by it; the Wronskian read with the angle is the conserved one, and a record's Wronskian keeps its sign under Rule3; the odd line on the Link shifts the wave number by its angle with the Port's sign, is sourced by the momentum density, odd under the time reversal, and written at the wall den T; the act is the file's declaration, refused by name where it is not one of the two or asked of a holder of the content; a one-part reader and the two gates' worlds are untouched; the like-or-unlike look's blind on the committed worlds with the back-in-time gate MATCH, and the plain control's two senses source the holder oppositely and read it plainly."""

import json
import math
from itertools import product

import numpy as np

import event_universe.world_files as world_files
from event_universe import node
from event_universe.core.ports import Wrap
from event_universe.core.rule3 import coefficients
from event_universe.features import rotation
from event_universe.game_board import GameBoard
from event_universe.loader.derived import amplitude_bound, count_wall, held_write, turns
from event_universe.loader.world import parse_world, universe_of
from event_universe.world_files import input_digest, load_world
from tests.laws import BACK, CHAIN, CHARGED, EVENTS, QUANTA, TOOL, chain_body_world, load_file, refused

DRIFT = load_file("body_drift", EVENTS.parents[1] / "tools" / "body_drift.py")
BUILD = load_file("like_build", EVENTS / "like_or_unlike" / "build_world.py")
LOOK = EVENTS / "like_or_unlike"
GAMMA, T, PAIR, RING = 6000, 32768, (4000, 6000), Wrap(True, True, True)
ONE, LEVEL, SHAPE = (1, 1, 1), 100_000, (24, 1, 1)
OMEGA = math.acos(PAIR[0] / PAIR[1])  # the matter pair's rest rotation in the vacuum
RULE, ZERO = coefficients(*PAIR, GAMMA, 0), np.zeros(SHAPE, dtype=np.int64)
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
    u = np.unwrap(phases)
    return (u[-1] - u[0]) / (steps - 1), max(booked) - min(booked), max(plain) - min(plain)


def test_the_laid_body_is_admitted_its_count_kept_and_a_far_count_refused(tmp_path, monkeypatch):
    """The count is the record's share in quanta over the wall 3 den T, read at the start within the law's tolerance of the declared count, every Node of the body carrying a quantum; over a hundred intervals the share's total moves only by Rule3's own rounding (the books' drift, under a quantum per Node of the chain) and no quantum changes family, the quanta at the declared Nodes stay above 0 and the body's Nodes derived for a report are where its share stands; a declared count off the share beyond the rounding refuses the world by name. (a) Random pairs within a million turned at random tangent half-angles within 1 and turned back return bit for bit, the turned pair within two units of the real rotation by 2 arctan(n / w); a turned level is not within twice A (the audit's witness, #1583 B10: (-1, -1) at the tangent half-angle -1 / 4 turns to (-3, -1) at A = 1) but within 2 A + 3, exhaustively over small pairs and walls, and the turning universe's amplitude bound reads a turned record's rooms at A + 2 (the six arrivals and the level before it is stepped against both turned); (b) at one Node of the matter pair in the vacuum, every Port folded, a record of positive Wronskian (z_before = z_now e^(i omega), clockwise) under the time level L rotates at omega + L / Gamma within the half-angle's third order for L = 600 and -600 and at omega for 0, and the Wronskian read from the booking, the step's levels before the turn, stands over 400 intervals within the rounding while the plain one swings by the angle; (c) on a ring of 24 a plane wave at k = pi / 6 under the uniform odd level L_x rotates at the band's omega(k + theta_x) with tan(theta_x / 2) = L_x / (2 Gamma), the read through +x turned by the Link's angle and through -x by its opposite, and under -L_x at omega(k - theta_x); (d) the Wronskian's sign is the record's: the wave of either sense has W of that sign at every Node and keeps it over 100 plain intervals of Rule3 on both lines with one rule, and a real line has none; (e) a plane moving toward +x (z = A e^(i (k x - omega t)), positive Wronskian) has its momentum density P_x = (F_+x - F_-x) / num below 0 (the inflow through -x the larger, the share flowing toward +x) and P_y = P_z = 0, the record with now and before swapped gives -P_x exactly (the flip with the current) and a standing record 0; the holder of the sign under the rotation takes w x P_a of each plane reader into its odd line a by the one write with one remainder over the wall E_s den T (node.write_sources with the momenta as the axis bookings, node.held_write), a real reader sourcing none of it, its time line W over E_s T, and the write back undoes it bit for bit. The act key of a held row: `rotation` on the holder of the sign gives it 1 + 3 lines, its record the time line, its odd lines' walls E_s den T against the tensions' E_s x 3 den T, the plane turned by it (derived.turns) and matter, one part, reading it not at all; `pace` or no key keeps one line and the plain read; an act by another word, and the rotation asked of a holder of the content, are refused by name; the two gates' universe files declare no act, and Bell's world run on its universe with the rotation declared on the holder gives the same lines and books bit for bit as on the file (light and the pair family, real lines, read nothing of the holder, whose odd lines nobody sources). The committed worlds of examples/events/like_or_unlike (the blind expectation the builder's byte for byte, written from the design before any run; the mode files the generator's, the digest binding each to its world): the like, the unlike, the uncharged pair and the four single-body worlds read by tools/body_drift.py over their run: the like pair ends further apart than the unlike pair, the mutual effect's sign ((a - b) / 2 above 0, which no background enters), asserted; the blind's three lines against the background (the uncharged pair's change plus the image force read on the single bodies), like apart, unlike together and the same size to a third of the half-difference, read and printed yes or no beside the plain controls' changes (ENGINE.md, section 6, the looks' numbers: the bodies' response to their own angle is not additive between a pair and a lone body, so the three lines are not met by that background); the back-in-time gate MATCH on the three pairs over their run. The plain control of unlike senses (the dimension's table, ALGEBRA.md #a-familys-declaration): after one interval the two bodies carry the Wronskian of their senses at their Nodes, the holder's record (its one line, light's) stands at or above 0 at the first's Nodes and at or below 0 at the second's, not 0 in all; the plane reads the holder plainly, a level of 100 entering its content as 100 at every Node of both bodies, while matter, real parts of the same pair, reads nothing of it and light does not read its own row."""
    monkeypatch.setattr(world_files, "REPOSITORY_ROOT", tmp_path)
    world = chain_body_world(tmp_path, TOOL)
    board = GameBoard(load_world(world))
    index = [family.name for family in board.families].index("matter")
    declared, quanta = board.mask(board.world.bodies[0].nodes), board.quanta(index)[0]
    laid, wall = int(quanta[declared].sum()), count_wall(board.families[index], 32768)
    assert abs(laid - QUANTA) <= 2 * int(QUANTA**0.5) + 1 and int(quanta[declared].min()) >= 1
    kept, drifts = [], []
    for _ in range(100):
        board.step()
        quanta, standing = board.quanta(index)[0], board.body_nodes(0)
        kept.append(int(quanta[standing].sum()))
        assert (quanta[standing] != 0).all() and (standing & declared).any()
        books = board.books()["matter"]
        drifts.append(books["drift"])
        assert abs(books["quanta"] - laid) <= CHAIN  # Rule3's rounding, under a quantum per Node
    print(f"GAMEBOARD body {laid}: quanta {min(kept)}-{max(kept)}, drift {min(drifts)}-{max(drifts)}")
    assert abs(max(drifts, key=abs)) < CHAIN * wall and board.books()["matter"]["pace"] > 0
    document = json.loads(world.read_text(encoding="utf-8"))
    document["measured"][0]["nodes"] = [{**n, "count": 1} for n in document["measured"][0]["nodes"]]
    world.write_text(json.dumps(document), encoding="utf-8")
    mode_path = world.with_suffix(".mode.json")
    mode = {**json.loads(mode_path.read_text(encoding="utf-8")), "world_digest": input_digest(document)}
    mode_path.write_text(json.dumps(mode), encoding="utf-8")
    refused("a declared count is within the rounding of the share", lambda: GameBoard(load_world(world)))

    draw, shape = np.random.default_rng(1), (4, 3, 2)
    x, y = (draw.integers(-(10**6), 10**6, shape) for _ in range(2))
    numerator, wall = draw.integers(-2 * GAMMA, 2 * GAMMA, shape), 2 * GAMMA
    turned = rotation.turned(x, y, numerator, wall)
    back = rotation.turned(*turned, numerator, wall, -1)
    assert np.array_equal(back[0], x) and np.array_equal(back[1], y)
    angle = 2 * np.arctan(numerator / wall)
    real = (x * np.cos(angle) - y * np.sin(angle), x * np.sin(angle) + y * np.cos(angle))
    assert max(np.abs(turned[0] - real[0]).max(), np.abs(turned[1] - real[1]).max()) < 2
    bound = amplitude_bound(TURNING, GAMMA, T, 63)
    assert rotation.turned(-1, -1, -1, 4) == (-3, -1) and bound > 0  # the witness, beyond twice A = 1
    for x, y, n, w in product(range(-3, 4), range(-3, 4), range(-6, 7), range(1, 7)):
        assert abs(n) > w or max(map(abs, rotation.turned(x, y, n, w))) <= 2 * max(abs(x), abs(y)) + 3
    rules = (coefficients(*PAIR, GAMMA, level) for level in (0, GAMMA // 2, GAMMA - 1))
    assert all((sum(r) + w) * 2 * (bound + 2) + abs(s) * bound + w < 2**63 for r, s, w in rules)
    zero = np.zeros(ONE, dtype=np.int64)
    for level in (0, 600, -600):
        re = node.Record(np.full(ONE, LEVEL), np.full(ONE, round(LEVEL * math.cos(OMEGA))), zero)
        im = node.Record(zero, np.full(ONE, round(LEVEL * math.sin(OMEGA))), zero)
        start = int(node.wronskian([re, im], True)[0, 0, 0])  # the positive record, clockwise
        found, booked, plain = rate(re, im, (np.full(ONE, level), (zero, zero, zero)), 400)
        assert start > 0 and abs(found + OMEGA + level / GAMMA) < 3e-4, (level, found)
        assert booked * 1000 < start and (level == 0 or plain > 10 * booked), (booked, plain)
    k = math.pi / 6
    for level in (600, -600):
        odd = np.full(SHAPE, level, dtype=np.int64)
        found = rate(*wave(k, band(k)), (ZERO, (odd, ZERO, ZERO)), 60)[0]
        assert abs(found + band(k + 2 * math.atan(level / (2 * GAMMA)))) < 1e-3, (level, found)
    for sense in (1, -1):
        lines = wave(k, band(k), sense)
        for _ in range(100):
            assert (np.sign(node.wronskian(lines, True)) == sense).all()
            lines = [node.step(line, RULE, RING) for line in lines]
    assert node.wronskian(lines[:1], False) == 0
    names = [family.name for family in TURNING]
    charge, charged = names.index("charge"), names.index("charged")
    moving = wave(math.pi / 4, OMEGA)
    forward = node.momentum_of(moving, RING)
    assert (forward[0] < 0).all() and not forward[1].any() and not forward[2].any()
    reversed_ = [node.Record(line.before, line.now, ZERO) for line in moving]
    assert np.array_equal(node.momentum_of(reversed_, RING)[0], -forward[0])
    standing = [node.Record(line.now, line.now, ZERO) for line in moving]
    assert not any(part.any() for part in node.momentum_of(standing, RING))
    write = held_write(TURNING, charge, T)
    bookings = {charged: node.wronskian(moving, True)}
    numerators = node.write_sources(charge, TURNING, bookings, {charged: forward}, write)
    assert np.array_equal(numerators[1], forward[0]) and not numerators[2].any()
    assert np.array_equal(numerators[0], bookings[charged])
    held = node.empty_state(TURNING[charge], SHAPE, write.walls, np.int64)
    lines, remainders = node.held_write(held.lines, numerators, write.walls, held.write_remainders)
    expected = (forward[0] + 100 * PAIR[1] * T // 2) // (100 * PAIR[1] * T)
    assert np.array_equal(lines[1].now, expected) and not lines[2].now.any()
    back_lines, before = node.held_write(lines, numerators, write.walls, remainders, -1)
    assert all(np.array_equal(a.now, b.now) for a, b in zip(back_lines, held.lines, strict=True))
    assert all(np.array_equal(a, b) for a, b in zip(before, held.write_remainders, strict=True))
    universe = json.loads((LOOK / "turning.json").read_text(encoding="utf-8"))
    rows = {row["name"]: row for row in universe["families"]}
    names = [family.name for family in TURNING]
    charge, charged, matter, gravity = map(names.index, ("charge", "charged", "matter", "gravity"))
    assert (TURNING[charge].lines, TURNING[charge].record, TURNING[charge].rotation) == (4, 1, True)
    assert turns(TURNING, charged) and not turns(TURNING, matter)
    assert charge not in [read.family for read in TURNING[matter].reads]
    assert held_write(TURNING, charge, T).walls == (100 * T,) + (100 * PAIR[1] * T,) * 3
    assert held_write(TURNING, gravity, T).walls[1] == 1000 * 3 * PAIR[1] * T
    rows["charge"]["held"]["act"] = "pace"
    paced = universe_of(universe)[1][charge]
    assert (paced.lines, paced.rotation) == (1, False)
    rows["charge"]["held"]["act"] = "sideways"
    refused("act is one of", universe_of, universe)
    del rows["charge"]["held"]["act"]
    rows["gravity"]["held"]["act"] = "rotation"
    refused("a holder of the content, sourced by the form", universe_of, universe)
    for name in ("light", "pair"):
        gate = json.loads((EVENTS / f"{name}.json").read_text(encoding="utf-8"))["families"]
        assert not any("act" in row.get("held", {}) for row in gate)
    monkeypatch.setattr(world_files, "REPOSITORY_ROOT", EVENTS.parents[1])
    bell = EVENTS / "bell" / "bell_a_b.json"
    document = json.loads(bell.read_text(encoding="utf-8"))
    files = world_files.world_files(document)
    files[bell.with_suffix(".mode.json").name] = json.loads(bell.with_suffix(".mode.json").read_text())
    runs = []
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
    readings = {name: DRIFT.drift(LOOK / f"{name}.json", None) for name in expected["worlds"]}
    against = DRIFT.compared(expected, readings)
    changes = {name: DRIFT.change_of(reading) for name, reading in readings.items()}
    a, b = against["a_like_less_background"], against["b_unlike_less_background"]
    blind = {key: against[key] for key in ("like_apart", "unlike_together", "same_size")}
    print(f"GAMEBOARD the look: changes {changes}, a {a}, b {b}, blind {blind}")
    assert against["like_further_than_unlike"] and against["half_difference"][0] > 0, against
    for name in ("like", "unlike", "uncharged_pair"):
        board = GameBoard(load_world(LOOK / f"{name}.json"))
        verdict = BACK.verdict(board, board.world.ticks)
        assert (verdict["verdict"], verdict["intervals"]) == ("MATCH", board.world.ticks), name
    board = GameBoard(load_world(LOOK / "unlike_plain.json"))
    names = [family.name for family in board.families]
    charged, charge, matter = map(names.index, (CHARGED["name"], "charge", "matter"))
    plane, light = board.states[charged], board.states[charge]
    board.step()
    first, second = board.body_nodes(0), board.body_nodes(1)
    turn, level = np.sign(node.wronskian(plane.lines, True)), light.lines[0].now
    assert (turn[first] == 1).all() and (turn[second] == -1).all() and len(light.lines) == 1
    assert int(level[first].min()) >= 0 < int(level[first].sum()) and int(level[second].max()) <= 0
    assert int(level[second].sum()) < 0
    hill = np.full(board.shape, 100, dtype=np.int64)
    light.lines[0] = node.Record(hill, level, light.lines[0].remainder)
    held = [s for f, s in zip(board.families, board.states, strict=True) if f.held and not f.wronskian]
    plain = sum(state.lines[0].now for state in held)  # every holder of the content, as it stands
    content = node.read(charged, board.families, board.states, 1, board.wrap)[0]
    assert ((content - plain) == 100)[first | second].all()  # the plane reads the holder plainly
    for reader in (matter, charge):  # dimension one, and the holder's own record
        assert charge not in [read.family for read in board.families[reader].reads]
        assert np.array_equal(node.read(reader, board.families, board.states, 1, board.wrap)[0], plain)
