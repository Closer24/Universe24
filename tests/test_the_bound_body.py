"""A bound body (ALGEBRA.md #the-generator, #what-a-body-is, #the-count-is-the-records-share): the generator lays a body, the GameBoard admits its declared count within the rounding of its family's share in quanta at its Nodes and refuses one beyond it by name, the count is the record's share and stays its family's within Rule3's rounding, the body's Nodes derived from where its share stands. The rotation round (ALGEBRA.md #the-hypotheses-under-their-own-names, The sign holder rotates the two-part record; #the-rows-against-nature (b2) and (f); HIGHLIGHTS.md, There is no sense): the turn is three exact shears, undone bit for bit and within two units of the real rotation; the angle is the holder's level over Gamma and the record of positive Wronskian rotates faster by it; the Wronskian read with the angle is the conserved one, and a record's Wronskian keeps its sign under Rule3; the odd line on the Link shifts the wave number by its angle with the Port's sign, is sourced by the sign's current, the mean of the Node's two a-Links' Wronskian currents, odd under the sense, and written over the time line's wall E_s T, the same wall as the time level's W, so that the odd level over the time level is the law's 3 den v / num; the act is the file's declaration, refused by name where it is not one of the two or asked of a holder of the content; a one-part reader and the two gates' worlds are untouched; the like-or-unlike look's six charged worlds (like, unlike, the two plain controls and the two charged single bodies), which had no lay under the energy line's integers and were refused at load by name, left the repository on 2026-10-03 at the owner's word, and its three uncharged worlds run the window whole with the back-in-time gate MATCH; the charged looks' drift and back-in-time and the plain control's reading of the two senses (the holder sourced oppositely and read plainly) wait for the re-design with the small charge (N_q at most about 400 on a neutral content), the engine round's open item."""

import json
import math
import shutil
from itertools import product

import numpy as np
from scipy.sparse import diags, kronsum
from scipy.sparse.linalg import spsolve

import event_universe.world_files as world_files
from event_universe import node
from event_universe.bookings import booked_of
from event_universe.core import paces
from event_universe.core.ports import Wrap
from event_universe.core.rule3 import coefficients, division_forward
from event_universe.features import rotation
from event_universe.features.start import scaled_source, unit_of
from event_universe.game_board import GameBoard
from event_universe.loader.derived import (
    amplitude_bound,
    count_wall,
    held_write_of,
    row_sources,
    turns,
    weight_of,
)
from event_universe.loader.lay import least_action
from event_universe.loader.universe import universe_of
from event_universe.world_files import input_digest, load_world
from tests.laws import BACK, CHAIN, EVENTS, PACKET, QUANTA, TOOL, chain_body_world, load_file, refused

DRIFT = load_file("body_drift", EVENTS.parents[1] / "tools" / "body_drift.py")  # the looks' drift tool
GATED = (  # the smallest shipped world of each builder whose load is seconds; the long loads are the runner's gate
    ("anticoincidence", "one_photon"),
    ("bell", "bell_a_prime_b_prime"),
    ("ghz", "ghz_y_x_y"),
    ("neutron_conversion", "neutron_conversion"),
    ("nuclide", "free_nuclide"),
    ("packet_giving", "packet_giving"),
    ("resonance", "detuned"),
    ("shelved_ion", "shelved_ion"),
    ("two_slits", "two_slits"),
    ("which_way", "one_gap"),
    ("zeno", "zeno_1"),
    ("zeno_pulsed", "zeno_pulsed_1"),
)
LOOK, GAMMA, PAIR, RING = EVENTS / "like_or_unlike", 6000, (4000, 6000), Wrap(True, True, True)
INTEGERS, TURNING = universe_of(json.loads((LOOK / "turning.json").read_text(encoding="utf-8")))
T, NAMES = INTEGERS["quantum_action"], [family.name for family in TURNING]  # the rule's rows, the plane
CHARGE, CHARGED, MATTER, BINDING = map(NAMES.index, ("charge", "charged", "matter", "binding"))
LEVEL, SHAPE, VACUUM, KEYS = 100_000, (24, 1, 1), (GAMMA, (GAMMA,) * 3), ("now", "before", "remainder")
OMEGA = math.acos(PAIR[0] / PAIR[1])  # the matter pair's rest rotation in the vacuum
RULE, ZERO, SIZE = coefficients(*PAIR, GAMMA, GAMMA, GAMMA), np.zeros(SHAPE, dtype=np.int64), 5_000


def band(k: float) -> float:
    """The matter pair's rotation rate at the wave number k along x on a ring (y and z folded)."""
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
    """The count is the record's share in quanta over the wall 3 den T, read at the start within the law's tolerance of the declared count, every Node of the body carrying a quantum; the start sources the binding holder by the form the hold writes, so the hold's first write returns the start's rest within Rule3's rounding, two units at most at any Node; over a hundred intervals the share's total moves only by Rule3's own rounding (the books' drift, under a quantum per Node of the chain) and no quantum changes family, the quanta at the declared Nodes stay above 0 and the body's Nodes derived for a report are where its share stands; a declared count off the share beyond the rounding refuses the world by name. (a) Random pairs within a million turned at random tangent half-angles within 1 and turned back return bit for bit, the turned pair within two units of the real rotation by 2 arctan(n / w); a turned level is not within twice A (the audit's witness, #1583 B10: (-1, -1) at the tangent half-angle -1 / 4 turns to (-3, -1) at A = 1) but within 2 A + 3, exhaustively over small pairs and walls, and the turning universe's amplitude bound reads a turned record's rooms at A + 2 (the six arrivals and the level before it is stepped against both turned); (b) at one Node of the matter pair in the vacuum, every Port folded, a record of positive Wronskian (z_before = z_now e^(i omega), clockwise) under the time level L rotates at omega + L / Gamma within the half-angle's third order for L = 600 and -600 and at omega for 0, and the Wronskian read from the booking, the step's levels before the turn, stands over 400 intervals within the rounding while the plain one swings by the angle; (c) on a ring of 24 a plane wave at k = pi / 6 under the uniform odd level L_x rotates at the band's omega(k + theta_x) with tan(theta_x / 2) = L_x / (2 Gamma), the read through +x turned by the Link's angle and through -x by its opposite, and under -L_x at omega(k - theta_x); (d) the Wronskian's sign is the record's: the wave of either sense has W of that sign at every Node and keeps it over 100 plain intervals of Rule3 on both lines with one rule, and a real line has none; (e) a plane moving toward +x (z = A e^(i (k x - omega t)), positive Wronskian) has as its sign current the mean of its two x-Links' Wronskian currents, J_x / 2 with J_x = Im(conj(z_i) (z_(+x) - z_(-x))) = 2 A^2 sin k, above 0 at every Node and within the lay's rounding of A^2 sin k, and J_y = J_z = 0, its conjugate, the opposite sense moving alike, the opposite within the read's rounding unit (where the momentum density gave the two the same current; the owner's word of 2026-10-01, 17:17, on the two hands), and a real record, two equal real lines, 0; the holder of the sign under the rotation takes its write weight k_w times w x that mean of each plane reader into its odd line a by the one write with one remainder over the time line's wall E_s T, the same wall as its time line's k_w x w x W (node.write_sources with the sign currents as the axis booked, node.held_write; k_w 400 in turning.json; ALGEBRA.md row (b2)'s arithmetic, the mathematician's 122 D, #1572 comment 5946560198, and the advisor's #1563 comment 5946186214, two hands): the plane wave at k = pi / 4 and the amplitude 5,000, the files' scale, writes its odd level over its time level at the law's 3 den v / num within the integers' rounding, v the band's group velocity at k (J_a = (6 den / num) W v exactly on a plane record), where over den T the odd level rounded to 0 at every Node and the engine's magnetic sector was absent; a real reader sources none of it, and the write back undoes it bit for bit. The act key of a held row: `rotation` on the holder of the sign gives it 1 + 3 lines, its record the time line, its four walls one E_s T against the tensions' E_s x 3 den T, the plane turned by it (derived.turns) and matter, one part, reading it not at all; `pace` or no key keeps one line and the plain read; an act by another word, and the rotation asked of a holder of the content, are refused by name; the two gates' universe files declare no act (light and the pair family, real lines, name no holder of the sign in their reads, and a real line naming one under the rotation is refused by name, tests/test_the_features.py). The plain control of unlike senses (the dimension's table, ALGEBRA.md #a-familys-declaration): after one interval the two bodies carry the Wronskian of their senses at their Nodes, the holder's record (its one line, light's) stands at or above 0 at the first's Nodes and at or below 0 at the second's, not 0 in all; the plane reads the holder plainly, a level of 100 entering its content as 100 at every Node of both bodies, while matter, real parts of the same pair, names no holder of the sign and reads nothing of it. A laid message on a sourced holder is kept (ENGINE.md section 3, the start): on the chain with a rotating body of the charged family, whose Wronskian sources the holder of the sign, and a packet of light laid on the holder's row, the holder's record at tick 0 is the laid message plus a rest static under it, the same in the level now and the level before (the message kept bit for bit), the rest the start lays with the message's own form among the sources (light's form sources the rows of the content, so the rest the start lays on an empty line differs from it, the binding row's by a hump under the packet), that empty line's rest static and positive at the body's Nodes and the remainder the start's."""
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
    document["bodies"][0]["nodes"] = [{**n, "count": 5} for n in document["bodies"][0]["nodes"]]
    world.write_text(json.dumps(document), encoding="utf-8")
    mode = {**json.loads(mode_path.read_text(encoding="utf-8")), "world_digest": input_digest(document)}
    mode_path.write_text(json.dumps(mode), encoding="utf-8")
    refused("a declared count is within the rounding of the share", lambda: GameBoard(load_world(world)))
    world = chain_body_world(tmp_path, TOOL, senses=(1,), mode=False)  # the body sources the holder
    packet = {**PACKET, "amplitude": 400, "top": dict(x=[5, 5], y=[0, 0], z=[0, 0])}
    document = {**json.loads(world.read_text(encoding="utf-8")), "messages": [packet]}
    world.write_text(json.dumps(document), encoding="utf-8")
    TOOL.main(["--input", str(world), "--sense", "1", "--pixel", "0"])  # the one-Node record
    board = GameBoard(load_world(world))
    message, light = board.world.messages[0], board.states[CHARGE].lines[0]
    now, before = board.board_array(message.now), board.board_array(message.before)
    for index in board.held:  # the start again on empty time lines: every held row's rest alone
        board.states[index].lines[0] = node.empty_record(board.shape, board.kind)
    board.start()
    rest = board.states[CHARGE].lines[0]
    assert now.any() and not np.array_equal(now, before) and (rest.remainder == light.remainder).all()
    assert np.array_equal(light.now - now, light.before - before)  # the message kept, its rest static
    assert not rest.now.any() and board.record(CHARGE)[0].now[board.body_nodes(0)].min() > 0  # the rows
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
    own, write = (CHARGED, 0), held_write_of(TURNING, CHARGE, T)  # the plane's one record owns the row 1
    sign = {own: node.wronskian(plane, True)}
    sources = node.write_sources(CHARGE, TURNING, sign, {own: flux}, write, {own: VACUUM}, GAMMA)
    assert np.array_equal(sources[4], TURNING[CHARGE].write * sign[own]) and not sources[6].any()
    assert np.array_equal(sources[5], TURNING[CHARGE].write * flux[0])  # k_w x w x J_x / 2 at w = 1
    held = node.empty_state(TURNING[CHARGE], SHAPE, write.walls, np.int64)
    lines, remainders = node.held_write(held.lines, sources, write.walls, held.write_remainders)
    assert write.walls == (100 * T,) * 8 and not any(map(np.any, sources[:4] + sources[6:]))  # E_s T
    assert np.array_equal(lines[5].now, (sources[5] + 50 * T) // (100 * T))  # (k_w J / 2 + r) div wall
    speed = (band(k + 1e-6) - band(k - 1e-6)) / 2e-6  # the band's group velocity at k, the law's v
    assert abs(int(lines[5].now.sum()) / int(lines[4].now.sum()) - 3 * PAIR[1] * speed / PAIR[0]) < 1e-3
    back_lines, before = node.held_write(lines, sources, write.walls, remainders, -1)
    assert all(np.array_equal(a.now, b.now) for a, b in zip(back_lines, held.lines, strict=True))
    assert all(np.array_equal(a, b) for a, b in zip(before, held.write_remainders, strict=True))
    universe = json.loads((LOOK / "turning.json").read_text(encoding="utf-8"))
    rows = {row["name"]: row for row in universe["families"]}
    assert (TURNING[CHARGE].lines, TURNING[CHARGE].record, TURNING[CHARGE].rotation) == (8, 1, True)
    assert turns(TURNING, CHARGED) and not turns(TURNING, MATTER)
    assert CHARGE not in [read.family for read in TURNING[MATTER].reads]
    assert held_write_of(TURNING, NAMES.index("gravity"), T).walls[1] == 1000 * 3 * PAIR[1] * T
    rows["charge"]["held"]["act"] = "pace"
    assert ((paced := universe_of(universe)[1][CHARGE]).lines, paced.rotation) == (2, False)
    rows["charge"]["held"]["act"] = "sideways"
    refused("act is one of", universe_of, universe)
    rows["gravity"]["held"]["act"], rows["charge"]["held"]["act"] = "rotation", "pace"
    refused("a holder of the content, sourced by the form", universe_of, universe)
    for gate in (json.loads((EVENTS / f"{n}.json").read_bytes()) for n in ("light", "pair")):
        assert all(row["held"]["act"] == "pace" for row in gate["families"] if "held" in row)  # stated


def test_the_committed_worlds_load_and_every_blind_is_its_builders_byte_for_byte(tmp_path):
    """The committed worlds of examples/events/like_or_unlike (the blind expectation the builder's byte for byte, written from the design before any run; the mode files the generator's, the digest binding each to its world) and every blind of examples/events: each blind is its builder's byte for byte; the three uncharged worlds load, their run the blind's window, and no other world stands in the folder (the six charged worlds and the universe file plain.json, refused at load, left the repository on 2026-10-03 at the owner's word, "what does not load, delete; we will manage without them"). No world runs here: the looks' drift over the window, the back-in-time MATCH on the pairs over their 400 and the standing world's 48 images through its 1000 intervals (examples/events/standing_body, 166's theorem under the write's factor booked as one rounding) are readings of tools/body_drift.py, tools/back_in_time.py and tools/body_standing.py by name (ENGINE.md, section 6), the gate and the 48 asserted as units on small worlds in test_the_node.py and test_the_meeting.py (a test runs under 30 seconds, the owner's word of 2026-10-03: a committed 128-chain's held rests alone take longer at the load). The drift's tool runs over four intervals of the anticoincidence world, its reading two bodies. The count gate (GameBoard's start) runs on the smallest world of every builder whose load is seconds (GATED, the loader's mode file applied to the laid Nodes, the defect of #1788 caught here); the folders whose smallest world is a long load (light_and_charge, like_or_unlike, matter_alone, matter_and_gravity, standing_body) keep the runner's gate at every run, by name."""
    for folder in (LOOK, *(p.parent for p in sorted(EVENTS.glob("*/blind_and_reading.md")))):
        build, out = load_file(f"{folder.name}_build", folder / "build_world.py"), tmp_path / folder.name
        build.main(["--folder", str(shutil.copytree(folder, out))])  # every look's blind its builder's
        assert (out / "expectation.json").read_bytes() == (folder / "expectation.json").read_bytes()
    expected = json.loads((LOOK / "expectation.json").read_text(encoding="utf-8"))
    lawful = list(expected["worlds"])  # the three uncharged worlds; the charged left on 2026-10-03
    assert len(lawful) == 3 and all("uncharged" in name for name in lawful)
    kept = ["design.json", "expectation.json", "turning.json", "uncharged.json"]  # no charged world
    files = [f"{n}{e}" for n in lawful for e in (".json", ".mode.json")] + kept
    assert sorted(p.name for p in LOOK.glob("*.json")) == sorted(files)
    assert all(load_world(LOOK / f"{n}.json").ticks == expected["window"][1] for n in lawful)  # loaded
    read = DRIFT.drift(GameBoard(load_world(EVENTS / "anticoincidence" / "one_photon.json")), 4)
    assert read["intervals"] == 4 and len(read["bodies"]) == 2  # the drift's tool on a small world
    for folder, name in GATED:  # the gate on the smallest world of every builder whose load is seconds
        world = GameBoard(load_world(EVENTS / folder / f"{name}.json")).world
        assert world.bodies or world.messages, (folder, name)


def test_two_charged_records_of_count_one_write_their_own_sign_rows_and_a_count_above_one_is_refused(
    tmp_path, monkeypatch
):
    """The count-1 gate and the lay of each quantum of charge as its own record (ALGEBRA.md, No record reads its own write of the sign; what is open, item 43 (1)): a universe of a holder of the content at a level weight so large that its rest is 0 at every Node (the paces Gamma, the write's factor 1 and the turn's numerator the level itself), the holder of the sign under the rotation at E_s = 1 and k_w by the energy line (k_w Gamma den = E_s T num, 4 at T = 36,000) and the charged plane of matter's pair; a chain of ten Nodes (x open) with two bodies of the charged family of count 1 in the senses +1 and -1, each laid by the generator as the one-Node record of its quantum (`--pixel`: one unit of the invariant 2 A^2 sin omega = T, A = isqrt(T den div (2 sine)) with sine = isqrt(den^2 - num^2), its Wronskian A x (A sine div den) at its Node and 0 elsewhere, sense x T / 2 within 2 A of the rounding) and admitted by the gate at the start: each body its own record, the holder three rows of four lines (the free row 0 and one per record), each row sourced by its own record alone (`row_sources`), the free row 0 at every Node (nothing sources it, no light laid) and each record's row at the start of the sign of its own sense; over three intervals, for each record, the turn's time numerator is bit for bit the other record's row's time line and its odd angles the other row's odd lines, the same bit for bit with the record's own row zeroed (the self-read 0 to the bit), and the row's time line after the step is Rule3's plain step of the row (the massless pair at the vacuum's paces) plus (k_w x W + r) div (E_s T) with W the record's own Wronskian booking and r the write's remainder before, the other record's Wronskian entering nowhere; a body of count 2, and a body of two Nodes of count 1, of the charged family are refused by name as one quantum of its family."""
    monkeypatch.setattr(world_files, "REPOSITORY_ROOT", tmp_path)
    k_w = T * PAIR[0] // (GAMMA * PAIR[1])  # the energy line at E_s = 1: k_w Gamma den = E_s T num
    content = {
        "sources": ["form"],
        "level_weight": 10**12,
        "write_weight": 1,
        "act": "pace",
    }  # a rest of 0
    sign = {"sources": ["wronskian"], "level_weight": 1, "write_weight": k_w, "act": "rotation"}
    rows = [
        {"name": "binding", "pair": [2400, 2401], "reads": {"binding": 1}, "held": content},
        {"name": "charge", "pair": [6000, 6000], "reads": {"binding": 1}, "held": sign},
        {"name": "charged", "pair": list(PAIR), "reads": {"binding": 1, "charge": 1}, "dimension": 2},
    ]
    (tmp_path / "u.json").write_text(json.dumps({"integers": INTEGERS, "families": rows}), "utf-8")
    (tmp_path / "e.json").write_bytes((EVENTS / "engine_start.json").read_bytes())
    world = dict(shape=[10, 1, 1], boundary=dict(x="open", y="periodic", z="periodic"), face_depth=1)
    quanta = [{"family": "charged", "nodes": [{"node": [x, 0, 0], "count": 1}]} for x in (3, 6)]
    world.update(ticks=3, universe="u.json", engine="e.json", node_readers=[], bodies=quanta)
    (path := tmp_path / "quanta.json").write_text(json.dumps(world), encoding="utf-8")
    TOOL.main(["--input", str(path), "--sense", "1", "-1", "--pixel", "0", "1"])  # each its own record
    board = GameBoard(load_world(path))
    families, charge, charged = board.families, 1, 2
    sources = [row_sources(families, charge, row) for row in range(3)]  # the free row, one per record
    assert sources == [[], [(charged, 0)], [(charged, 1)]] and families[charge].lines == 4 * 3
    assert [r for r, _ in board.laid_rows()] == [0, 1]  # each body of the charged family its own record
    sine = math.isqrt(PAIR[1] ** 2 - PAIR[0] ** 2)  # the lay by the invariant 2 A^2 sin omega = T
    amplitude = math.isqrt(T * PAIR[1] // (2 * sine))
    quantum = amplitude * (amplitude * sine // PAIR[1])  # the one-Node record's Wronskian, T / 2
    assert abs(quantum - T // 2) <= 2 * amplitude
    time_lines = [board.states[charge].lines[4 * row].now for row in range(3)]  # the rows at the start
    for record, (x, sense) in enumerate(((3, 1), (6, -1))):
        wronskian = node.wronskian(board.lines_of(charged, record), True)
        assert int(wronskian[x, 0, 0]) == sense * quantum and int(np.count_nonzero(wronskian)) == 1
        own = sense * time_lines[record + 1]  # the row's rest at the start, of its own record's sense
        assert (own >= 0).all() and own[x, 0, 0] > 0
    assert not time_lines[0].any()  # the free row: nothing sources it and no light is laid
    rule = coefficients(6000, 6000, GAMMA, GAMMA, GAMMA, None, board.unit)  # the vacuum's rule
    empty = node.empty_record(board.shape, board.kind)
    for _ in range(3):
        states, lines = board.states, list(board.states[charge].lines)
        remainders = [r.copy() for r in states[charge].write_remainders]
        bookings = board.stepped(charged, 1)[1]  # the bookings about the step, as the step books them
        for record in (0, 1):
            other = 4 * (2 - record)  # the other record's row: its time line and its three odd lines
            turn = node.turning(charged, families, states, 1, GAMMA, record)
            assert np.array_equal(turn[0], lines[other].now) and lines[4 * (record + 1)].now.any()
            assert all(np.array_equal(a, lines[other + 1 + axis].now) for axis, a in enumerate(turn[1]))
            blank = [*states[:charge], node.NodeState(list(lines), remainders), *states[charge + 1 :]]
            blank[charge].lines[4 * (record + 1) : 4 * (record + 2)] = [empty] * 4  # the own row zeroed
            zeroed = node.turning(charged, families, blank, 1, GAMMA, record)
            assert np.array_equal(zeroed[0], turn[0])  # the self-read 0 to the bit
            assert all(np.array_equal(a, b) for a, b in zip(zeroed[1], turn[1], strict=True))
        board.step()
        for record in (0, 1):
            line, own = 4 * (record + 1), node.wronskian(bookings[record][1], True)
            expected = node.step(lines[line], rule, board.wrap).now + (k_w * own + remainders[line]) // T
            assert np.array_equal(board.states[charge].lines[line].now, expected), (board.tick, record)
    document, mode_path = json.loads(path.read_text(encoding="utf-8")), path.with_suffix(".mode.json")
    for nodes in ([{"node": [3, 0, 0], "count": 2}], [{"node": [x, 0, 0], "count": 1} for x in (3, 4)]):
        document["bodies"][0]["nodes"] = nodes
        path.write_text(json.dumps(document), encoding="utf-8")
        mode = {**json.loads(mode_path.read_text("utf-8")), "world_digest": input_digest(document)}
        mode_path.write_text(json.dumps(mode), encoding="utf-8")
        refused("one quantum of its family", load_world, path)


HOLDER = {"name": "nuclear", "pair": [50, 51], "reads": {"gravity": 1, "binding": 1, "nuclear": 1}}
HOLDER["held"] = {"sources": ["form"], "level_weight": 1, "write_weight": 300, "act": "pace"}  # E_n, W_1
NUCLEON = {"name": "nucleon", "pair": list(PAIR), "dimension": ["plane"] * 3, "reads": HOLDER["reads"]}
COMPACT = {"kind": "fixed_point", "stop": 2, "passes": 30, "seed": "compact", "profile": [1, 4]}
K2 = (32, 1)  # the budget's confidence multiple squared, the shipped lays' key
NUCLEUS, CUBE = 25, 9  # the design's count, a few quanta, and the open cube's side


def test_the_nucleons_fixed_point_in_its_own_nuclear_holders_well_stands_and_the_twin_without_it_spreads(
    tmp_path, monkeypatch
):
    """The nucleon's fixed point in its own nuclear holder's well (ALGEBRA.md, The nucleon is a compact body of its family and The nuclear holder, a hypothesis by name with four declared integers, the file's and not the law's: the holder's pair [50, 51], its level weight E_n = 1, its write weight W_1 = 300 and the read weight 1, printed beside the numbers; the mathematician's 275 (b) with the advisor's second, #1572 comments 5969267087 and 5969197876): the rule's universe with a held row `nuclear` sourced by the form, reading the content holders and itself at 1 as every shipped holder does, and a `nucleon` family of three planes at matter's pair reading gravity 1, binding 1 and `nuclear` 1; one body of 25 quanta at the centre of an open 9-cube laid by `lay.kind` `fixed_point` with the compact seed at the profile [1, 4] (one part at the centre and four at each of the six Ports' Nodes), the stop 2 and 30 passes, the tolerance [1, den] at the largest den whose least T is the universe's 32,768 (the budget's line, loader/lay.py); no draw and no node_reader: the body is read by its share and its standing. (i) The fixed point returns: the generator's passes end with the content and the record repeating within the stop at every Node under the passes (ten passes on the first run, the last within one unit); the engine's start then holds the rest: the hold's first write returns it within one unit at every Node (the mathematician's 293: the integer rest satisfies its line within one rounding, the residual at most half a wall under the half-wall origin, so the first write moves a level by at most 1; the floor origin admitted two), and the nuclear row's deviation from the row's exact line at its own composed paces (the source the laid record's form as the hold books it, scaled per proper volume and per proper interval over the wall E_n T, solved sparse in the test as tests/test_the_features.py solves the massless and binding rows) is printed beside the line as a GAMEBOARD reading and pinned below 0.6 at this seed, a reading of the neighbours' roundings' alignment and no bound: the derived bound is the residual through the inverse operator, 0.5 x 306 / 6 = 25.5 levels. (ii) The count is the record's share: the world's declared counts (the generator's reading, 43 over 33 Nodes from the design's 25, the three planes' per-plane rounding scaling the record above the design's count) against the share read at those Nodes within the gate ((|c - read| - 1) div 2)^2 <= c, every plane's lines alike and the sense lines 0. (iii) The body stands: P = 2 pi / omega_b rounded, cos omega_b the level before over the level now at the centre of the laid record (8 intervals from the pair (227, 158)), and the form D_i = now^2 - next x before summed over the record's lines returns to itself within one quantum of form, |D_i(1 + P) - D_i(1)| < T, at every Node of the region whose form is above T div 100 (2,547 at most against 32,768 on the first run); the twin without the holder (the nucleon's read of `nuclear` dropped, the same lay under the same mode file) spreads: after P intervals its share over the body's Nodes is below the bound body's by more than the gate's rounding at the body's count (20.6 against 43.7 quanta on the first run, the numbers pinned in the assertion's comment) and its centre's share below the body's. (iv) The guard admits the start (the content below the Link's zero at every Node, the laid levels within the amplitude bound as main derives it with the hill's factor; C.14's tension room is not on main), the back-in-time gate MATCH over 2 P intervals, every write remainder at half its wall and every sourced held row's time line at its rest's half wall, the record's lines born at the half wall of the rule they step by, the lay's origin (#1743). Found and not asserted: deeper wells toward the compact branch (W_1 from 325 at this count, from 450 at 13 quanta seeded [1, 2]) are refused in the engine's own start, the lay and the rest of the holders returning to an earlier state three to five units apart at the centre, beyond the rounding tie's two, so the nucleon laid here stands on the wide branch, the content 1,217 = 0.20 Gamma at the centre and 2 cos omega_b = 1.392 above the band's top 1.333."""
    monkeypatch.setattr(world_files, "REPOSITORY_ROOT", tmp_path)
    rule = json.loads((EVENTS / "rule.json").read_text(encoding="utf-8"))
    action, rows = rule["integers"]["quantum_action"], rule["families"]
    rows = [r for r in rows if r["name"] != "matter"]
    unread = {name: w for name, w in NUCLEON["reads"].items() if name != HOLDER["name"]}
    for name, reads in (("u", NUCLEON["reads"]), ("t", unread)):  # the universe and the twin's
        universe = {**rule, "families": [*rows, HOLDER, {**NUCLEON, "reads": reads}]}
        (tmp_path / f"{name}.json").write_text(json.dumps(universe), encoding="utf-8")
    (tmp_path / "e.json").write_bytes((EVENTS / "engine_start.json").read_bytes())
    centre = (CUBE // 2,) * 3
    world = dict(shape=[CUBE] * 3, boundary=dict(x="open", y="open", z="open"), face_depth=1, ticks=40)
    world.update(universe="u.json", engine="e.json", node_readers=[], lay=COMPACT)
    world["bodies"] = [{"family": "nucleon", "nodes": [{"node": list(centre), "count": NUCLEUS}]}]
    (path := tmp_path / "w.json").write_text(json.dumps(world), encoding="utf-8")
    TOOL.main(["--input", str(path)])
    mode = json.loads(path.with_suffix(".mode.json").read_text(encoding="utf-8"))
    world = json.loads(path.read_text(encoding="utf-8"))  # the Nodes and counts the generator read
    passes = mode["bodies"][0]["lay"][
        "trajectory"
    ]  # per pass the content's change, the record's, the count
    assert len(passes) <= COMPACT["passes"] and max(passes[-1][1:3]) <= COMPACT["stop"]
    nodes, ticks = world["bodies"][0]["nodes"], world["ticks"]
    declared, per_node = sum(n["count"] for n in nodes), max(n["count"] for n in nodes)
    den = max(d for d in range(1, 1000) if least_action(PAIR, ticks, per_node, (1, d), K2) <= action)
    assert (
        least_action(PAIR, ticks, per_node, (1, den), K2) == action
    )  # T the least power of two admitted
    assert least_action(PAIR, ticks, per_node, (1, den + 1), K2) > action
    world["lay"] = {**COMPACT, "tolerance": [1, den], "confidence": list(K2)}
    for name, document in (("w", world), ("tw", {**world, "universe": "t.json"})):  # the twin's lay
        (tmp_path / f"{name}.json").write_text(json.dumps(document), encoding="utf-8")
        laid = {**mode, "world_digest": input_digest(document)}
        (tmp_path / f"{name}.mode.json").write_text(json.dumps(laid), encoding="utf-8")
    board, twin = (GameBoard(load_world(tmp_path / f"{n}.json")) for n in ("w", "tw"))  # the guard
    names, families, gamma = [f.name for f in board.families], board.families, GAMMA
    nucleon, nuclear = names.index("nucleon"), names.index("nuclear")
    lines = board.states[nucleon].lines
    mask = board.mask(tuple(tuple(n["node"]) for n in nodes))
    off = abs(declared - int(board.quanta(nucleon)[0][mask].sum()))
    assert off <= 1 or ((off - 1) // 2) ** 2 <= declared  # the gate, the count the record's share
    assert all(np.array_equal(getattr(lines[0], k), getattr(lines[p], k)) for p in (2, 4) for k in KEYS)
    assert not any(lines[p].now.any() or lines[p].before.any() for p in (1, 3, 5))  # no sense laid
    assert int(board.read(nucleon)[0].max()) < paces.frozen_content(gamma)  # below the Link's zero
    assert max(int(np.abs(line.now).max()) for line in lines) <= board.world.amplitude_bound
    assert all((x.remainder == board.half_wall(nucleon)).all() for x in lines)  # born at the half wall
    for index in (names.index(n) for n in ("gravity", "binding", "nuclear")):  # the sourced held rows
        state, walls = board.states[index], board.walls(index)
        assert all((r == w // 2).all() for r, w in zip(state.write_remainders, walls, strict=True))
        half = (coefficients(*families[index].pair, gamma, gamma, gamma, None, board.unit)[2] - 1) // 2
        assert board.origins[index] == half and (state.lines[0].remainder == half).all()  # the rest's
    num, den_h = families[nuclear].pair  # the nuclear row's exact line at its own composed paces
    levels = [board.states[r.family].lines[0].now.astype(object) for r in families[nuclear].reads]
    content = sum(r.weight * level for r, level in zip(families[nuclear].reads, levels, strict=True))
    form = np.asarray(booked_of(families, nucleon, board.stepped(nucleon, 1)[1])[0][(nucleon, 0)])
    source = families[nuclear].write * weight_of(nuclear, families[nucleon]) * form.astype(object)
    wall, (clock, pace) = board.walls(nuclear)[0], paces.node_paces(gamma, content)
    unit = unit_of(source, (num, den_h), wall, board.world.width, gamma, board.wrap)
    fine = division_forward(3 * den_h * unit * source, wall, 0)[0] * gamma * gamma  # the booked source
    scaled = np.asarray(scaled_source(fine, clock, pace, gamma, 2), dtype=float).ravel() / unit
    paths = [diags([1.0, 1.0], [-1, 1], shape=(n, n)) for n in board.shape]
    links = kronsum(kronsum(paths[0], paths[1]), paths[2])  # the six Ports, zeros beyond the faces
    line = np.asarray(6 * (den_h - num) * clock * clock + 6 * num * pace * pace, dtype=float).ravel()
    operator = (diags(line) - diags(np.asarray(num * pace * pace, dtype=float).ravel()) @ links).tocsr()
    exact = spsolve(operator, scaled).reshape(board.shape)
    off_line = float(np.abs(board.states[nuclear].lines[0].now - exact)[mask].max())
    # a reading of the neighbours' roundings' alignment at this seed (the mathematician's 293), not a bound; the
    # derived bound is 25.5 levels
    assert off_line < 0.6
    now, before = (int(getattr(lines[0], k)[centre]) for k in KEYS[:2])
    period = round(2 * math.pi / math.acos(before / now))  # the record's own rotation at the centre
    kept, hold_before = [[x.now.astype(object) for x in lines]], board.states[nuclear].lines[0].now
    hold_before = hold_before.copy()
    for tick in range(1, 2 * period + 3):
        board.step()
        kept.append([x.now.astype(object) for x in board.states[nucleon].lines])
        if tick == 1:  # the hold's first write returns the start's rest within one unit
            moved = int(np.abs(board.states[nuclear].lines[0].now - hold_before).max())
            assert moved <= 1
        if tick == period:
            share = board.share_of(nucleon)[0]
            standing, at_centre = int(share[mask].sum(dtype=object)), int(share[centre])

    def form_at(t: int):  # type: ignore[no-untyped-def]
        return sum(kept[t][k] * kept[t][k] - kept[t + 1][k] * kept[t - 1][k] for k in range(len(lines)))

    first, later = form_at(1), form_at(1 + period)
    region = first > action // 100  # the body's region, the Nodes above a hundredth of a quantum of form
    assert region[centre] and mask[region].any() and int(np.abs(later - first)[region].max()) < action
    for _ in range(period):
        twin.step()
    spread, wall_c = twin.share_of(nucleon)[0], count_wall(families[nucleon], action)
    deficit = (standing - int(spread[mask].sum(dtype=object))) // wall_c  # 43.7 against 20.6 quanta
    assert ((deficit - 1) // 2) ** 2 > declared and int(spread[centre]) < at_centre
    print(
        f"GAMEBOARD the nuclear holder's declared integers: the pair {HOLDER['pair']}, E_n "
        f"{HOLDER['held']['level_weight']}, W_1 {HOLDER['held']['write_weight']}, the read weight "
        f"{NUCLEON['reads']['nuclear']}; the lay {declared} quanta over {len(nodes)} Nodes in {len(passes)} "
        f"passes, the period {period}, the body's share {standing / wall_c:.1f} and the twin's "
        f"{int(spread[mask].sum(dtype=object)) / wall_c:.1f} over the body's Nodes after the period; the nuclear "
        f"rest off its exact line by {off_line:.4f} level at most over the body (a reading), the first write moving it {moved}"
    )
    assert BACK.verdict(GameBoard(load_world(tmp_path / "w.json")), 2 * period)["verdict"] == "MATCH"
