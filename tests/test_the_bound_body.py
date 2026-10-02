"""A bound body (ALGEBRA.md #the-generator, #what-a-body-is, #the-count-is-the-records-share): the generator lays a body, the GameBoard admits its declared count within the rounding of its family's share in quanta at its Nodes and refuses one beyond it by name, the count is the record's share and stays its family's within Rule3's rounding, the body's Nodes derived from where its share stands. The rotation round (ALGEBRA.md #the-hypotheses-under-their-own-names, The sign holder rotates the two-part record; #the-rows-against-nature (b2) and (f); HIGHLIGHTS.md, There is no sense): the turn is three exact shears, undone bit for bit and within two units of the real rotation; the angle is the holder's level over Gamma and the record of positive Wronskian rotates faster by it; the Wronskian read with the angle is the conserved one, and a record's Wronskian keeps its sign under Rule3; the odd line on the Link shifts the wave number by its angle with the Port's sign, is sourced by the sign's current, the mean of the Node's two a-Links' Wronskian currents, odd under the sense, and written over the time line's wall E_s T, the same wall as the time level's W, so that the odd level over the time level is the law's 3 den v / num; the act is the file's declaration, refused by name where it is not one of the two or asked of a holder of the content; a one-part reader and the two gates' worlds are untouched; the like-or-unlike look's six charged worlds (like, unlike, the two plain controls and the two charged single bodies), which have no lay under the energy line's integers, are refused at load by name with the start's refusals recorded in the blind, and its three uncharged worlds run the window whole with the back-in-time gate MATCH; the charged looks' drift and back-in-time and the plain control's reading of the two senses (the holder sourced oppositely and read plainly) wait for the re-design with the small charge (N_q at most about 400 on a neutral content), the engine round's open item."""

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
from event_universe.loader.world import universe_of
from event_universe.world_files import input_digest, load_world
from tests.laws import BACK, CHAIN, EVENTS, PACKET, QUANTA, TOOL, chain_body_world, load_file, refused

DRIFT = load_file("body_drift", EVENTS.parents[1] / "tools" / "body_drift.py")
BUILD = load_file("like_build", EVENTS / "like_or_unlike" / "build_world.py")
LOOK, GAMMA, PAIR, RING = EVENTS / "like_or_unlike", 6000, (4000, 6000), Wrap(True, True, True)
INTEGERS, TURNING = universe_of(json.loads((LOOK / "turning.json").read_text(encoding="utf-8")))
T, NAMES = INTEGERS["quantum_action"], [family.name for family in TURNING]  # the rule's rows, the plane
CHARGE, CHARGED, MATTER, BINDING = map(NAMES.index, ("charge", "charged", "matter", "binding"))
LEVEL, SHAPE, VACUUM, KEYS = 100_000, (24, 1, 1), (GAMMA, (GAMMA,) * 3), ("now", "before", "remainder")
OMEGA = math.acos(PAIR[0] / PAIR[1])  # the matter pair's rest rotation in the vacuum
RULE, ZERO, SIZE = coefficients(*PAIR, GAMMA, GAMMA, GAMMA), np.zeros(SHAPE, dtype=np.int64), 5_000


def band(
    k: float,
) -> float:  # the matter pair's rotation rate at the wave number k along x on a ring (y and z folded)
    return math.acos(PAIR[0] / (3 * PAIR[1]) * (math.cos(k) + 2))


def wave(k: float, omega: float, sense: int = 1, size: int = LEVEL) -> list[node.Record]:
    at = k * np.arange(SHAPE[0]).reshape(SHAPE)
    re, im = (np.rint(size * f(at)).astype(np.int64) for f in (np.cos, np.sin))
    re_before, im_before = (np.rint(size * f(at + omega)).astype(np.int64) for f in (np.cos, np.sin))
    return [node.Record(re, re_before, ZERO), node.Record(sense * im, sense * im_before, ZERO)]


START = int(node.wronskian(wave(0, OMEGA), True).sum(dtype=object))  # the uniform record's W on the ring


def turned_run(lines, ramp, links, steps):  # type: ignore[no-untyped-def]
    """A plane of the charged family on the ring stepped `steps` intervals in the turning universe at the vacuum's rule, the holder of the sign at the time level ramp[t + 1] with ramp[t] the previous interval's at the interval t (its two levels as the hold leaves them, so the turn of the level before is by the previous interval's angle, node.turned_before) and its odd lines `links`; then the same intervals back in the inverse's two stages, the holder's levels stepped back by hand between them, every level and remainder returning bit for bit, asserted; returns the rotation rate at the Node 0 (the phase unwrapped) and the swings of the Wronskian read from the booking and of the plain one."""
    states = [node.empty_state(f, SHAPE, (), np.int64) for f in TURNING]
    odd = [node.Record(level, level, ZERO) for level in links]  # the holder's odd lines, static
    time = [node.Record(ramp[t + 1] + ZERO, ramp[t] + ZERO, ZERO) for t in range(steps + 1)]
    phases, swings, kept = [], [], []
    for t in range(steps):
        states[CHARGE].lines, states[CHARGED].lines = [time[t], *odd], lines
        kept.append(np.array([getattr(r, k) for r in lines for k in KEYS]))
        lines, (_first, second) = node.step_family(CHARGED, TURNING, states, RULE, RING, GAMMA)
        phases.append(math.atan2(int(lines[1].now[0, 0, 0]), int(lines[0].now[0, 0, 0])))
        swings.append([int(node.wronskian(w, True).sum(dtype=object)) for w in (second, lines)])
    for t in reversed(range(steps)):  # the inverse's two stages around the holder's own step back
        states[CHARGE].lines, states[CHARGED].lines = [time[t + 1], *odd], lines
        states[CHARGED].lines = node.step_family(CHARGED, TURNING, states, RULE, RING, GAMMA, -1)[0]
        states[CHARGE].lines = [time[t], *odd]
        lines = node.turned_before(CHARGED, TURNING, states, GAMMA, -1)
        assert np.array_equal(kept[t], [getattr(r, k) for r in lines for k in KEYS]), t
    return np.diff(np.unwrap(phases)).mean(), *(max(s) - min(s) for s in zip(*swings, strict=True))


def test_the_laid_body_is_admitted_its_count_kept_and_a_far_count_refused(tmp_path, monkeypatch):
    """The count is the record's share in quanta over the wall 3 den T, read at the start within the law's tolerance of the declared count, every Node of the body carrying a quantum; the start sources the binding holder by the form the hold writes, so the hold's first write returns the start's rest within Rule3's rounding, two units at most at any Node; over a hundred intervals the share's total moves only by Rule3's own rounding (the books' drift, under a quantum per Node of the chain) and no quantum changes family, the quanta at the declared Nodes stay above 0 and the body's Nodes derived for a report are where its share stands; a declared count off the share beyond the rounding refuses the world by name. (a) Random pairs within a million turned at random tangent half-angles within 1 and turned back return bit for bit, the turned pair within two units of the real rotation by 2 arctan(n / w); a turned level is not within twice A (the audit's witness, #1583 B10: (-1, -1) at the tangent half-angle -1 / 4 turns to (-3, -1) at A = 1) but within 2 A + 3, exhaustively over small pairs and walls, and the turning universe's amplitude bound reads a turned record's rooms at A + 2 (the six arrivals and the level before it is stepped against both turned); (b) at one Node of the matter pair in the vacuum, every Port folded, a record of positive Wronskian (z_before = z_now e^(i omega), clockwise) under the time level L rotates at omega + L / Gamma within the half-angle's third order for L = 600 and -600 and at omega for 0, and the Wronskian read from the booking, the step's levels before the turn, stands over 400 intervals within the rounding while the plain one swings by the angle; (c) on a ring of 24 a plane wave at k = pi / 6 under the uniform odd level L_x rotates at the band's omega(k + theta_x) with tan(theta_x / 2) = L_x / (2 Gamma), the read through +x turned by the Link's angle and through -x by its opposite, and under -L_x at omega(k - theta_x); (d) the Wronskian's sign is the record's: the wave of either sense has W of that sign at every Node and keeps it over 100 plain intervals of Rule3 on both lines with one rule, and a real line has none; (e) a plane moving toward +x (z = A e^(i (k x - omega t)), positive Wronskian) has as its sign current the mean of its two x-Links' Wronskian currents, J_x / 2 with J_x = Im(conj(z_i) (z_(+x) - z_(-x))) = 2 A^2 sin k, above 0 at every Node and within the lay's rounding of A^2 sin k, and J_y = J_z = 0, its conjugate, the opposite sense moving alike, the opposite within the read's rounding unit (where the momentum density gave the two the same current; the owner's word of 2026-10-01, 17:17, on the two hands), and a real record, two equal real lines, 0; the holder of the sign under the rotation takes its write weight k_w times w x that mean of each plane reader into its odd line a by the one write with one remainder over the time line's wall E_s T, the same wall as its time line's k_w x w x W (node.write_sources with the sign currents as the axis booked, node.held_write; k_w 400 in turning.json; ALGEBRA.md row (b2)'s arithmetic, the mathematician's 122 D, #1572 comment 5946560198, and the advisor's #1563 comment 5946186214, two hands): the plane wave at k = pi / 4 and the amplitude 5,000, the files' scale, writes its odd level over its time level at the law's 3 den v / num within the integers' rounding, v the band's group velocity at k (J_a = (6 den / num) W v exactly on a plane record), where over den T the odd level rounded to 0 at every Node and the engine's magnetic sector was absent; a real reader sources none of it, and the write back undoes it bit for bit. The act key of a held row: `rotation` on the holder of the sign gives it 1 + 3 lines, its record the time line, its four walls one E_s T against the tensions' E_s x 3 den T, the plane turned by it (derived.turns) and matter, one part, reading it not at all; `pace` or no key keeps one line and the plain read; an act by another word, and the rotation asked of a holder of the content, are refused by name; the two gates' universe files declare no act (light and the pair family, real lines, name no holder of the sign in their reads, and a real line naming one under the rotation is refused by name, tests/test_the_features.py). The committed worlds of examples/events/like_or_unlike (the blind expectation the builder's byte for byte, written from the design before any run; the mode files the generator's, the digest binding each to its world): the like, the unlike, the uncharged pair and the four single-body worlds read by tools/body_drift.py over their run: the like pair ends further apart than the unlike pair, the mutual effect's sign ((a - b) / 2 above 0, which no background enters), asserted; the blind's three lines against the background (the uncharged pair's change plus the image force read on the single bodies), like apart, unlike together and the same size to a third of the half-difference, read and printed yes or no beside the plain controls' changes (ENGINE.md, section 6, the looks' numbers: the bodies' response to their own angle is not additive between a pair and a lone body, so the three lines are not met by that background); the back-in-time gate MATCH on the three pairs over their run. The plain control of unlike senses (the dimension's table, ALGEBRA.md #a-familys-declaration): after one interval the two bodies carry the Wronskian of their senses at their Nodes, the holder's record (its one line, light's) stands at or above 0 at the first's Nodes and at or below 0 at the second's, not 0 in all; the plane reads the holder plainly, a level of 100 entering its content as 100 at every Node of both bodies, while matter, real parts of the same pair, names no holder of the sign and reads nothing of it. A laid message on a sourced holder is kept (ENGINE.md section 3, the start): on the chain with a rotating body of the charged family, whose Wronskian sources the holder of the sign, and a packet of light laid on the holder's row, the holder's record at tick 0 is the laid message plus a rest static under it, the same in the level now and the level before (the message kept bit for bit), the rest the start lays with the message's own form among the sources (light's form sources the rows of the content, so the rest the start lays on an empty line differs from it, the binding row's by a hump under the packet), that empty line's rest static and positive at the body's Nodes and the remainder the start's."""
    monkeypatch.setattr(world_files, "REPOSITORY_ROOT", tmp_path)
    board = GameBoard(load_world(world := chain_body_world(tmp_path, TOOL)))
    declared, quanta = board.mask(board.world.bodies[0].nodes), board.quanta(MATTER)[0]
    laid, wall = int(quanta[declared].sum()), count_wall(board.families[MATTER], 32768)
    assert abs(laid - QUANTA) <= 2 * int(QUANTA**0.5) + 1 and int(quanta[declared].min()) >= 1
    kept, drifts, source = [], [], board.states[BINDING].lines[0].now.copy()  # the start's rest
    for _ in range(100):
        board.step()
        assert kept or int(np.abs(board.states[BINDING].lines[0].now - source).max()) <= 2
        quanta, standing = board.quanta(MATTER)[0], board.body_nodes(0)
        kept.append(int(quanta[standing].sum()))
        assert (quanta[standing] != 0).all() and (standing & declared).any()
        drifts.append((books := board.books()["matter"])["drift"])
        assert abs(books["quanta"] - laid) <= CHAIN  # Rule3's rounding, under a quantum per Node
    assert abs(max(drifts, key=abs)) < CHAIN * wall and board.books()["matter"]["pace"] > 0 and kept
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
    message, light = board.world.messages[0], board.states[CHARGE].lines[0]
    now, before = board.board_array(message.now), board.board_array(message.before)
    for index in board.held:  # the start again on empty time lines: every held row's rest alone
        board.states[index].lines[0] = node.empty_record(board.shape, board.kind)
    board.start()
    rest = board.states[CHARGE].lines[0]
    assert now.any() and not np.array_equal(now, before) and np.array_equal(rest.now, rest.before)
    assert np.array_equal(light.now - now, light.before - before)  # the message kept, its rest static
    assert np.array_equal(light.remainder, rest.remainder) and rest.now[board.body_nodes(0)].min() > 0
    draw, shape = np.random.default_rng(1), (4, 3, 2)
    x, y, numerator = (draw.integers(-size, size, shape) for size in (10**6, 10**6, 2 * GAMMA))
    turned, angle = rotation.turned(x, y, numerator, wall := 2 * GAMMA), 2 * np.arctan(numerator / wall)
    assert np.array_equal(rotation.turned(*turned, numerator, wall, -1), (x, y))
    real = (x * np.cos(angle) - y * np.sin(angle), x * np.sin(angle) + y * np.cos(angle))
    assert max(np.abs(turned[0] - real[0]).max(), np.abs(turned[1] - real[1]).max()) < 2
    bound, k = amplitude_bound(TURNING, GAMMA, T, 63), math.pi / 6
    assert rotation.turned(-1, -1, -1, 4) == (-3, -1) and bound > 0  # the witness, beyond twice A = 1
    for x, y, n, w in product(range(-3, 4), range(-3, 4), range(-6, 7), range(1, 7)):
        assert abs(n) > w or max(map(abs, rotation.turned(x, y, n, w))) <= 2 * max(abs(x), abs(y)) + 3
    rules = (coefficients(*PAIR, GAMMA, *paces.node_paces(GAMMA, c)) for c in (0, GAMMA // 2, GAMMA - 1))
    assert all((sum(r) + w) * 2 * (bound + 2) + abs(s) * bound + w < 2**63 for r, s, w in rules)
    k, ramp = math.pi / 6, np.linspace(0, 2 * GAMMA * math.tan(0.11), 1202).round().astype(int)
    for levels in ([0] * 402, [600] * 402, [-600] * 402, ramp):  # three static levels, then the ramp
        found, booked, plain = turned_run(wave(0, OMEGA), levels, (ZERO,) * 3, len(levels) - 2)
        assert START > 0 and abs(found + OMEGA + np.mean(levels[1:-1]) / GAMMA) < 3e-4, found
        assert booked * 1000 < START and (not any(levels) or plain > 10 * booked), (booked, plain)
    for level in (600, -600):
        found = turned_run(wave(k, band(k)), [0] * 62, (np.full_like(ZERO, level), ZERO, ZERO), 60)[0]
        assert abs(found + band(k + 2 * math.atan(level / (2 * GAMMA)))) < 1e-3, (level, found)
    for sense in (1, -1):
        lines = wave(k, band(k), sense)
        for _ in range(100):
            lines = [node.step(line, RULE, RING) for line in lines]
            assert (np.sign(node.wronskian(lines, True)) == sense).all()
    assert node.wronskian(lines[:1], False) == 0
    flux = node.sense_current_of(plane := wave(k := math.pi / 4, band(k), size=SIZE), RING)
    assert np.abs(flux[0] - SIZE * SIZE * math.sin(k)).max() < 2 * SIZE
    assert (flux[0] > 0).all() and not flux[1].any() and not flux[2].any()
    assert np.isin(node.sense_current_of(wave(k, band(k), -1, SIZE), RING)[0] + flux[0], (0, 1)).all()
    assert not any(part.any() for part in node.sense_current_of([plane[0], plane[0]], RING))
    write, sign = held_write(TURNING, CHARGE, T), {CHARGED: node.wronskian(plane, True)}
    sources = node.write_sources(CHARGE, TURNING, sign, {CHARGED: flux}, write, {CHARGED: VACUUM}, GAMMA)
    assert np.array_equal(sources[0], TURNING[CHARGE].write * sign[CHARGED]) and not sources[2].any()
    assert np.array_equal(sources[1], TURNING[CHARGE].write * flux[0])  # k_w x w x J_x / 2 at w = 1
    held = node.empty_state(TURNING[CHARGE], SHAPE, write.walls, np.int64)
    lines, remainders = node.held_write(held.lines, sources, write.walls, held.write_remainders)
    assert write.walls == (100 * T,) * 4 and not lines[2].now.any()  # E_s T on every line, E_s = 100
    assert np.array_equal(lines[1].now, (sources[1] + 50 * T) // (100 * T))  # (k_w J / 2 + r) div wall
    speed = (band(k + 1e-6) - band(k - 1e-6)) / 2e-6  # the band's group velocity at k, the law's v
    assert abs(int(lines[1].now.sum()) / int(lines[0].now.sum()) - 3 * PAIR[1] * speed / PAIR[0]) < 1e-3
    back_lines, before = node.held_write(lines, sources, write.walls, remainders, -1)
    assert all(np.array_equal(a.now, b.now) for a, b in zip(back_lines, held.lines, strict=True))
    assert all(np.array_equal(a, b) for a, b in zip(before, held.write_remainders, strict=True))
    universe = json.loads((LOOK / "turning.json").read_text(encoding="utf-8"))
    rows = {row["name"]: row for row in universe["families"]}
    assert (TURNING[CHARGE].lines, TURNING[CHARGE].record, TURNING[CHARGE].rotation) == (4, 1, True)
    assert turns(TURNING, CHARGED) and not turns(TURNING, MATTER)
    assert held_write(TURNING, NAMES.index("gravity"), T).walls[1] == 1000 * 3 * PAIR[1] * T
    rows["charge"]["held"]["act"] = "pace"
    assert ((paced := universe_of(universe)[1][CHARGE]).lines, paced.rotation) == (1, False)
    rows["charge"]["held"]["act"] = "sideways"
    refused("act is one of", universe_of, universe)
    rows["gravity"]["held"]["act"], rows["charge"]["held"]["act"] = "rotation", "pace"
    refused("a holder of the content, sourced by the form", universe_of, universe)
    for gate in (json.loads((EVENTS / f"{n}.json").read_bytes()) for n in ("light", "pair")):
        assert not any("act" in row.get("held", {}) for row in gate["families"])
    monkeypatch.setattr(world_files, "REPOSITORY_ROOT", EVENTS.parents[1])  # the repository's worlds
    BUILD.main(["--folder", str(tmp_path)])
    assert (tmp_path / "expectation.json").read_bytes() == (LOOK / "expectation.json").read_bytes()
    expected = json.loads((LOOK / "expectation.json").read_text(encoding="utf-8"))
    charged = [
        name for name in expected["worlds"] if "uncharged" not in name
    ]  # six, no lay under the line
    for name in charged:  # declared without a mode file, refused at load by name
        refused("mode file beside the world must be an object", load_world, LOOK / f"{name}.json")
    for words in (
        "length 8, 12699 and -8253 at the Node [33, 0, 0]",
        "length 4, 531 and 539 at the Node [87, 0, 0]",
        "declares the count 54 and its family's share reads 431 quanta",
        "length 4, -5053 and 10375 at the Node [33, 0, 0]",
        "length 2, -4548 and 9907 at the Node [95, 0, 0]",
    ):
        assert words in expected["comment"], words  # the start's refusals recorded in the blind by name
    lawful = [name for name in expected["worlds"] if "uncharged" in name]
    assert (len(charged), len(lawful)) == (6, 3)
    readings = {name: DRIFT.drift(LOOK / f"{name}.json", None) for name in lawful}
    assert {reading["intervals"] for reading in readings.values()} == {expected["window"][1]}
    print(f"GAMEBOARD the look, the changes: {[(n, DRIFT.change_of(r)) for n, r in readings.items()]}")
    for name in lawful:
        verdict = BACK.verdict(board := GameBoard(load_world(LOOK / f"{name}.json")), board.world.ticks)
        assert (verdict["verdict"], verdict["intervals"]) == ("MATCH", board.world.ticks), name
