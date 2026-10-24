"""A bound body (ALGEBRA.md #the-generator, #what-a-body-is, #the-count-is-the-records-share): the generator lays a body, the lattice admits its declared count within the rounding of its family's share in quanta at its Nodes and refuses one beyond it by name, the count is the record's share and stays its family's within Rule3's rounding, the body's Nodes derived from where its share stands. The rotation round (ALGEBRA.md #the-hypotheses-under-their-own-names, The sign holder rotates the two-part record; #the-rows-against-nature (b2) and (f); HIGHLIGHTS.md, There is no sense): the time turn is three exact shears, undone bit for bit and within two units of the real rotation; the angle is the holder's level over Gamma and the record of positive Wronskian rotates faster by it; the Wronskian read with the angle is the conserved one, and a record's Wronskian keeps its sign under Rule3; the odd line on the Link shifts the wave number by its angle with the Port's sign (the Link's turn in the fold form since the two hands' lines of 2026-10-09, plane.sign_pairs), is sourced by the sign's current, the Node's two a-Links' Wronskian currents summed unhalved, odd under the sense, and written over the doubled wall 2 E_s T, so that the odd level over the time level is the law's 3 den v / num; the act is the file's declaration, refused by name where it is not one of the two or asked of a holder of the content; a one-part reader and the two gates' worlds are untouched; the universe turning.json stands at examples/events/ for these tests."""

import json
import math

import numpy as np

import event_universe.world_files as world_files
from event_universe import node, readings, records, share
from event_universe.core import paces
from event_universe.core.ports import Wrap
from event_universe.core.rule3 import coefficients, rule_integers
from event_universe.features import phase
from event_universe.flux import step_family as flux_step_family
from event_universe.flux import step_line as flux_step_line
from event_universe.lattice import Lattice
from event_universe.loader.derived import (
    amplitude_bound,
    held_write_of,
    row_sources,
    turns,
)
from event_universe.loader.universe import universe_of
from event_universe.plane import link_levels, link_pairs, turned_room
from event_universe.world_files import input_digest, load_world
from tests.laws import EVENTS, TOOL, design_beside, refused
from tests.laws_universe import COUNT, small_world

GAMMA, PAIR, RING = (
    6000,
    (3600, 6000),
    Wrap(True, True, True),
)  # the charged plane's pair, Pythagorean since 2026-10-24 ((4000, 6000) until then, refused under the sign)
INTEGERS, TURNING = universe_of(json.loads((EVENTS / "turning.json").read_text(encoding="utf-8")))
T, NAMES = INTEGERS["quantum_action"], [family.name for family in TURNING]  # the rule's rows, the plane
CHARGE, CHARGED, MATTER, BINDING = map(NAMES.index, ("charge", "charged", "matter", "binding"))
LEVEL, SHAPE, VACUUM, KEYS = 100_000, (24, 1, 1), (GAMMA, (GAMMA,) * 3), ("now", "before", "remainder")
OMEGA = math.acos(PAIR[0] / PAIR[1])  # the matter pair's rest rotation in the vacuum
RULE = rule_integers(*PAIR, GAMMA, GAMMA, GAMMA)  # the reaches, S, w, the mass D
ZERO, SIZE = np.zeros(SHAPE, dtype=np.int64), 5_000


def band(k: float) -> float:
    """The matter pair's rotation rate at the wave number k along x on a ring (y and z folded)."""
    return math.acos(PAIR[0] / (3 * PAIR[1]) * (math.cos(k) + 2))


def wave(k: float, omega: float, sense: int = 1, size: int = LEVEL) -> list[records.Record]:
    at = k * np.arange(SHAPE[0]).reshape(SHAPE)
    re, im = (np.rint(size * f(at)).astype(np.int64) for f in (np.cos, np.sin))
    re_before, im_before = (np.rint(size * f(at + omega)).astype(np.int64) for f in (np.cos, np.sin))
    return [records.Record(re, re_before, ZERO), records.Record(sense * im, sense * im_before, ZERO)]


START = int(
    records.wronskian(wave(0, OMEGA), True).sum(dtype=object)
)  # the uniform record's W on the ring


def turned_run(lines, ramp, links, steps):  # type: ignore[no-untyped-def]
    """A plane of the charged family on the ring stepped `steps` intervals in the turning universe at the vacuum's rule, the holder of the sign at the time level ramp[t + 1] with ramp[t] the previous interval's at the interval t (its two levels as the held write leaves them; under the temporal gauge the time level turns nothing at the Node, features/phase, the Link's phase pair standing at its seed here, no phase lines given) and its odd lines `links`, each Link's pair in the fold form from them (plane.link_pairs, the caller's as flux.step_records computes it); then the same intervals back, the holder's levels stepped back by hand, every level and remainder returning bit for bit, asserted; returns the rotation rate at the Node 0 (the phase unwrapped) and the swings of the Wronskian read from the booking and of the plain one (the same numbers now, the bookings from the plain pair)."""
    states = [records.empty_state(f, SHAPE, (), np.int64) for f in TURNING]
    odd = [records.Record(level, level, ZERO) for level in links]  # the holder's odd lines, static
    time = [records.Record(ramp[t + 1] + ZERO, ramp[t] + ZERO, ZERO) for t in range(steps + 1)]
    phases, swings, kept = [], [], []
    states[CHARGE].lines = [time[0], *odd]
    angles = node.turning(CHARGED, TURNING, states, 1)  # the sign's odd levels, static
    assert angles is not None
    pairs = link_pairs(
        PAIR, GAMMA, 0, (1,) * 6, None, link_levels(angles[1], RING, (-1, -1))
    )  # the Links' pairs
    for t in range(steps):
        states[CHARGE].lines, states[CHARGED].lines = [time[t], *odd], lines
        kept.append(np.array([getattr(r, k) for r in lines for k in KEYS]))
        lines, (_first, second) = flux_step_family(
            CHARGED, TURNING, states, RULE, RING, GAMMA, pairs=pairs
        )
        phases.append(math.atan2(int(lines[1].now[0, 0, 0]), int(lines[0].now[0, 0, 0])))
        swings.append([int(records.wronskian(w, True).sum(dtype=object)) for w in (second, lines)])
    for t in reversed(range(steps)):  # the inverse, the holder's own step back by hand beside it
        states[CHARGE].lines, states[CHARGED].lines = [time[t + 1], *odd], lines
        lines = flux_step_family(CHARGED, TURNING, states, RULE, RING, GAMMA, -1, pairs=pairs)[0]
        states[CHARGE].lines = [time[t], *odd]
        assert np.array_equal(kept[t], [getattr(r, k) for r in lines for k in KEYS]), t
    return np.diff(np.unwrap(phases)).mean(), *(max(s) - min(s) for s in zip(*swings, strict=True))


def test_the_laid_body_is_admitted_its_count_kept_and_a_far_count_refused(tmp_path, monkeypatch):
    """The count is the record's share in quanta over the wall 3 den T, read at the start within the law's tolerance of the declared count by the lay's own support (share.plain_quanta, the plain term at the Nodes the lay wrote; ALGEBRA.md, The booking is the frame's, the last clause), on the one clump of the small torus with the universe file (tests/laws_universe.small_world, posed here on 2026-10-24; the clicks chain of 24 with a body of 50 quanta to then, every world but Universe24 cancelled): the support reads the declared count at the declared Node and nowhere else, the frame's share stands below it there with the rest at the six neighbours, the Links' halves, and nowhere further, the board's total the declared count within the floors per Node; over 40 intervals the quanta at the body's standing Nodes stay above 0, the declared Node among them, and the books' total follows the clump's well (read and printed: from the lay's 429 upward as X falls at the clump, where the chain's static paces kept it within a quantum per Node over a hundred intervals, the former clause); a declared count off the share beyond the rounding refuses the world by name. (a) Random pairs within a million turned at random tangent half-angles within 1 and turned back return bit for bit, the turned pair within two units of the real rotation by 2 arctan(n / w); a turned level is not within twice A (the audit's witness, #1583 B10: (-1, -1) at the tangent half-angle -1 / 4 turns to (-3, -1) at A = 1) but within 2 A + 3, exhaustively over small pairs and walls, and the turning universe's amplitude bound reads a turned record's rooms at the six arrivals under the sign's pair with the phase at its own extreme, X sqrt 2 to the rounding (`derived.turned_room`, features/phase: 7,591 on turning.json, the mathematician's number of 2026-10-09); (b) at one Node of the matter pair in the vacuum, every Port folded, a record of positive Wronskian (z_before = z_now e^(i omega), clockwise) under a uniform time level L rotates at omega for L = 600, -600 and 0 alike (the temporal gauge: a uniform level does nothing, as a uniform potential does, the mathematician's item 6; the phase lives on the Link, test_part_c_phase_line), and the Wronskian read from the booking, the plain pair's, stands over 400 intervals within the rounding; (c) on a ring of 24 a plane wave at k = pi / 6 under the uniform odd level L_x rotates at the band's omega(k + theta_x) with tan(theta_x / 2) = L_x / (2 Gamma), the read through +x turned by the Link's angle and through -x by its opposite, and under -L_x at omega(k - theta_x); (d) the Wronskian's sign is the record's: the wave of either sense has W of that sign at every Node and keeps it over 100 plain intervals of Rule3 on both lines with one rule, and a real line has none; (e) a plane moving toward +x (z = A e^(i (k x - omega t)), positive Wronskian) has as its sign current its two x-Links' Wronskian currents summed unhalved, J_x = Im(conj(z_i) (z_(+x) - z_(-x))) = 2 A^2 sin k, above 0 at every Node and within the lay's rounding of 2 A^2 sin k, and J_y = J_z = 0, its conjugate, the opposite sense moving alike, the opposite exactly (the mean taken by the doubled wall, the two hands' lines of 2026-10-09; the owner's word of 2026-10-01, 17:17, on the two hands), and a real record, two equal real lines, 0; the holder of the sign under the rotation takes its write weight k_w times w x that sum of each plane reader into its odd line a by the one write with one remainder over the doubled wall 2 E_s T, its time line's k_w x w x W over E_s T (records.write_sources with the sign currents as the axis booked, node.held_write_at; k_w 400 in turning.json; ALGEBRA.md row (b2)'s arithmetic, the mathematician's 122 D, #1572 comment 5946560198, and the advisor's #1563 comment 5946186214, two hands): the plane wave at k = pi / 4 and the amplitude 5,000, the files' scale, writes its odd level over its time level at the law's 3 den v / num within the integers' rounding, v the band's group velocity at k (J_a = (6 den / num) W v exactly on a plane record), where over den T the odd level rounded to 0 at every Node and the engine's magnetic sector was absent; a real reader sources none of it, and the write back undoes it bit for bit. The act key of a held row: `rotation` on the holder of the sign gives it 1 + 3 lines, its record the time line, its four walls E_s T on the time line and 2 E_s T on the odd lines against the tensions' E_s x 3 den T, the plane turned by it (derived.turns) and matter, one part, reading it not at all; `pace` or no key keeps one line and the plain read; an act by another word, and the rotation asked of a holder of the content, are refused by name; the two gates' universe files declare no act (light and the pair family, real lines, name no holder of the sign in their reads, and a real line naming one under the rotation is refused by name, tests/test_the_features.py). The plain control of unlike senses (the dimension's table, ALGEBRA.md #a-familys-declaration): after one interval the two bodies carry the Wronskian of their senses at their Nodes, the holder's record (its one line, light's) stands at or above 0 at the first's Nodes and at or below 0 at the second's, not 0 in all; the plane reads the holder plainly, a level of 100 entering its content as 100 at every Node of both bodies, while matter, real parts of the same pair, names no holder of the sign and reads nothing of it. The laid packet on a sourced holder (ENGINE.md section 3, the start: the holder's record at interval 0 the laid packet plus a rest static under it) was the chain's clause with a rotating body and a light packet on the holder's row, left with the chain on 2026-10-24."""
    monkeypatch.setattr(world_files, "REPOSITORY_ROOT", tmp_path)
    board = Lattice(
        load_world(world := small_world(tmp_path, detector=False))
    )  # the one clump on the small torus
    board.output = lambda line: None
    matter_at = [f.name for f in board.families].index("matter")
    declared, quanta = board.mask(board.world.bodies[0].nodes), board.quanta(matter_at)[0]
    support, laid = share.plain_quanta(board, matter_at)[0], int(quanta[declared].sum())
    assert (
        int(support[declared].sum()) == int(support.sum()) == COUNT
    )  # the lay's own support, the gate's read
    beside = np.logical_or.reduce(
        [a != 0 for a in readings.ports(declared.astype(np.int64), board.wrap)]
    )
    assert 0 < laid < COUNT and int(quanta[beside].sum()) > 0 and not quanta[~(declared | beside)].any()
    assert abs(int(quanta.sum()) - COUNT) <= int(declared.sum() + beside.sum())  # the floors per Node
    kept = []
    for _ in range(40):
        board.step()
        quanta, standing = board.quanta(matter_at)[0], board.body_nodes(0)
        kept.append(int(quanta[standing].sum()))
        assert (quanta[standing] != 0).all() and (standing & declared).any()
        books = board.books()["matter"]
        assert books["quanta"] > 0 and books["pace"] > 0 and books["drift"] is not None
    print(f"the clump's quanta at its standing Nodes over 40 intervals {kept[::8]} (the lay {COUNT})")
    mode_path, document = world.with_suffix(".mode.json"), json.loads(world.read_text(encoding="utf-8"))
    document["bodies"][0]["nodes"] = [{**n, "count": 5000} for n in document["bodies"][0]["nodes"]]
    world.write_text(json.dumps(document), encoding="utf-8")
    mode = {**json.loads(mode_path.read_text(encoding="utf-8")), "world_digest": input_digest(document)}
    mode_path.write_text(json.dumps(mode), encoding="utf-8")
    refused("a declared count is within the rounding of the share", lambda: Lattice(load_world(world)))
    seed, unit = (
        phase.seed(amplitude := phase.amplitude(GAMMA, 63), GAMMA),
        amplitude,
    )  # the phase line's pair
    for count in (-6000, -777, 0, 1, 9408):  # the turn of a plane is the fold of the phase pair (Part C)
        pair = phase.iterate(seed, count, GAMMA)
        assert phase.iterate(pair, count, GAMMA, -1) == seed  # the reversal bit for bit
        cosine, sine = (int(a) for a in phase.read(pair))
        assert (
            abs(cosine - unit * math.cos(count / GAMMA))
            < 2 * GAMMA
            > abs(sine - unit * math.sin(count / GAMMA))
        )
    bound, k = amplitude_bound(TURNING, GAMMA, T, 63), math.pi / 6
    assert bound > 0
    for content in (
        0,
        GAMMA // 2,
        GAMMA - 1,
    ):  # the turned record's room: the pair's extreme on the arrivals
        clock, pace = paces.node_paces(GAMMA, content)
        reads, s, w = coefficients(*PAIR, GAMMA, clock, pace)
        arrivals = 6 * pace * pace * turned_room(PAIR, GAMMA, 1)  # X sqrt 2 to the rounding per arrival
        assert sum(reads) < arrivals < 2 * sum(reads)  # above the plain reads, under the fold's twice
        assert arrivals * bound + w * bound + abs(s) * bound + w < 2**63
    k, ramp = math.pi / 6, np.linspace(0, 2 * GAMMA * math.tan(0.11), 1202).round().astype(int)
    for levels in ([0] * 402, [600] * 402, [-600] * 402, ramp):  # three static levels, then the ramp
        found, booked, plain = turned_run(wave(0, OMEGA), levels, (ZERO,) * 3, len(levels) - 2)
        assert START > 0 and abs(found + OMEGA) < 3e-4, found  # a uniform level turns nothing
        assert booked * 1000 < START and plain == booked, (booked, plain)
    for level in (
        600,
        -600,
    ):  # a static odd level turns the band to omega(k + theta), the Link's angle theta = -2 atan(level / (2 Gamma)) at the read (-1, -1) (since 2026-10-21, the sign opposite to the time line's, the law's row (b2); k + 2 atan under the read (1, 1) until then)
        found = turned_run(wave(k, band(k)), [0] * 62, (np.full_like(ZERO, level), ZERO, ZERO), 60)[0]
        assert abs(found + band(k - 2 * math.atan(level / (2 * GAMMA)))) < 1e-3, (level, found)
    for sense in (1, -1):
        lines = wave(k, band(k), sense)
        for _ in range(100):
            lines = [flux_step_line(line, RULE, RING) for line in lines]
            assert (np.sign(records.wronskian(lines, True)) == sense).all()
    assert records.wronskian(lines[:1], False) == 0
    flux = readings.sense_current_of(plane := wave(k := math.pi / 4, band(k), size=SIZE), RING)
    assert np.abs(flux[0] - 2 * SIZE * SIZE * math.sin(k)).max() < 4 * SIZE  # J_x unhalved, 2 A^2 sin k
    assert (flux[0] > 0).all() and not flux[1].any() and not flux[2].any()
    assert not (
        readings.sense_current_of(wave(k, band(k), -1, SIZE), RING)[0] + flux[0]
    ).any()  # odd exactly
    assert not any(part.any() for part in readings.sense_current_of([plane[0], plane[0]], RING))
    own, write = (CHARGED, 0), held_write_of(TURNING, CHARGE, T)  # the plane's one record owns the row 1
    sign = {
        own: 2 * records.wronskian(plane, True)
    }  # the Wronskian booked centred on the triple, the two edges' sum over the doubled wall (the centred count, 2026-10-23): on a plane wave the two edges are equal, so twice the one (the former booking took the one edge over E_s T)
    sources, walls, _weight = records.write_sources(
        CHARGE, TURNING, sign, {own: flux}, write, {own: VACUUM}, GAMMA
    )
    carried = [
        int(np.asarray(w, dtype=object).reshape(-1)[0]) for w in walls
    ]  # the carried factor's walls at the vacuum's rulers, one number each
    scales = [
        c // w for c, w in zip(carried, write.walls, strict=True)
    ]  # the factor's wall per Node over the interval's wall
    whole = [
        np.asarray(a, dtype=object) for a in (sign[own], flux[0])
    ]  # Python's integers: the carried wall passes 63 bits
    factor = write.factors[
        CHARGED
    ]  # the one charged reader's charge factor, 3 T den over its count unit brought to the holder's wall (The constants, 2026-10-24)
    assert np.array_equal(sources[4], TURNING[CHARGE].write * factor * whole[0] * scales[4])
    assert not sources[6].any()
    assert np.array_equal(
        sources[5], TURNING[CHARGE].write * factor * whole[1] * scales[5]
    )  # k_w x w x the charge factor x J_x at w = 1, unhalved, at the carried wall
    held = records.empty_state(TURNING[CHARGE], SHAPE, carried, object)
    lines, remainders = node.held_write_at(held.lines, sources, carried, held.write_remainders)
    assert (
        write.walls[0] % (200 * T) == 0 and len(set(write.walls)) == 1 and len(write.walls) == 8
    )  # 2 E_s T times the charge multiple on every line, the time line too (The constants, 2026-10-24), the Wronskian booked centred on the triple (the centred count, 2026-10-23; the former E_s T on the time line, 2 E_s T on the odd lines)
    assert not any(map(np.any, sources[:4] + sources[6:]))
    assert np.array_equal(
        lines[5].now, (sources[5] + carried[5] // 2) // carried[5]
    )  # (k_w J + r) div the wall
    speed = (band(k + 1e-6) - band(k - 1e-6)) / 2e-6  # the band's group velocity at k, the law's v
    assert abs(int(lines[5].now.sum()) / int(lines[4].now.sum()) - 3 * PAIR[1] * speed / PAIR[0]) < 1e-3
    back_lines, before = node.held_write_at(lines, sources, carried, remainders, -1)
    assert all(np.array_equal(a.now, b.now) for a, b in zip(back_lines, held.lines, strict=True))
    assert all(np.array_equal(a, b) for a, b in zip(before, held.write_remainders, strict=True))
    universe = json.loads((EVENTS / "turning.json").read_text(encoding="utf-8"))
    rows = {row["name"]: row for row in universe["families"]}
    assert (TURNING[CHARGE].lines, TURNING[CHARGE].record, TURNING[CHARGE].rotation) == (8, 1, True)
    assert turns(TURNING, CHARGED) and not turns(TURNING, MATTER)
    assert CHARGE not in [read.family for read in TURNING[MATTER].reads]
    assert (
        held_write_of(TURNING, NAMES.index("gravity"), T).walls[1] == 2 * 1000 * 3 * PAIR[1] * T
    )  # the tension line's doubled wall 2 E_s W_c (The stress is the Links', 2026-10-23; the former E_s W_c)
    rows["charge"]["held"]["act"] = (
        "pace"  # the former act key: the one Node refuses it as any unknown key
    )
    refused("unknown key 'act'", universe_of, universe)
    for gate in (json.loads((EVENTS / f"{n}.json").read_bytes()) for n in ("light", "pair")):
        assert all(
            "act" not in row["held"] for row in gate["families"] if "held" in row
        )  # content alone


def test_two_charged_records_of_count_one_write_their_own_sign_rows_and_a_count_above_one_is_refused(
    tmp_path, monkeypatch
):
    """The count-1 gate and the lay of each quantum of charge as its own record (ALGEBRA.md, No record reads its own write of the sign; what is open, item 43 (1)): a universe of a holder of the content at a level weight so large that its rest is 0 at every Node (the paces Gamma, the write's factor 1 and the turn's numerator the level itself), the holder of the sign under the rotation at E_s = 1 and k_w by the energy line (k_w Gamma den = E_s T num, 4 at T = 36,000) and the charged plane of matter's pair; a chain of ten Nodes (x open) with two bodies of the charged family of count 1 in the senses +1 and -1, each laid by the generator as the one-Node record of its quantum (the design's `pixels`: one unit of the invariant 2 A^2 sin omega = T, A = isqrt(T den div (2 sine)) with sine = isqrt(den^2 - num^2), its Wronskian A x (A sine div den) at its Node and 0 elsewhere, sense x T / 2 within 2 A of the rounding) and admitted by the gate at the start: each body its own record, the holder three rows of four lines (the free row 0 and one per record), each row sourced by its own record alone (`row_sources`), the free row 0 at every Node (nothing sources it, no light laid) and each record's row at the start of the sign of its own sense; over three intervals, for each record, the turn's time numerator is bit for bit the other record's row's time line and its odd angles the other row's odd lines, the same bit for bit with the record's own row zeroed (the self-read 0 to the bit), and the row's time line after the step is Rule3's plain step of the row (the massless pair at the vacuum's paces) plus (k_w x W + r) div (E_s T) with W the record's own Wronskian booking and r the write's remainder before, the other record's Wronskian entering nowhere; a body of count 2, and a body of two Nodes of count 1, of the charged family are refused by name as one quantum of its family."""
    monkeypatch.setattr(world_files, "REPOSITORY_ROOT", tmp_path)
    content = {
        "sources": ["form"],
        "level_weight": 10**12,
        "write_weight": 1,
    }  # a rest of 0
    sign = {"sources": ["wronskian"], "level_weight": 1}  # alpha E_s T num / (Gamma den), derived
    rows = [
        {"name": "binding", "pair": [2400, 2401], "reads": {"binding": 1}, "held": content},
        {"name": "charge", "pair": [6000, 6000], "reads": {"binding": 1}, "held": sign},
        {"name": "charged", "pair": list(PAIR), "reads": {"binding": 1, "charge": 1}, "dimension": 2},
    ]
    (tmp_path / "u.json").write_text(json.dumps({"integers": INTEGERS, "families": rows}), "utf-8")
    world = dict(shape=[10, 1, 1], boundary=dict(x="open", y="periodic", z="periodic"), face_depth=1)
    quanta = [{"family": "charged", "nodes": [{"node": [x, 0, 0], "count": 1}]} for x in (3, 6)]
    world.update(intervals=3, universe="u.json", node_detectors=[], bodies=quanta)
    (path := tmp_path / "quanta.json").write_text(json.dumps(world), encoding="utf-8")
    design_beside(tmp_path, "quanta", senses=[1, -1], pixels=[0, 1])  # the design's keys beside
    TOOL.main(["--input", str(path)])  # each its own record
    board = Lattice(load_world(path))
    families, charge, charged = board.families, 1, 2
    write = held_write_of(families, charge, T)
    factor, multiple = (
        write.factors[charged],
        write.walls[0] // (2 * T * families[charge].write_wall),
    )  # the reader's charge factor and the walls' charge multiple (The constants, 2026-10-24)
    k_w = families[
        charge
    ].write_weight  # the law's alpha E_s T / Gamma at E_s 1, carried inside the write, no pair in it (2026-10-24; E_s T num / (Gamma den) until then)
    assert (k_w, families[charge].write_wall) == (T // GAMMA, 1)
    sources = [row_sources(families, charge, row) for row in range(3)]  # the free row, one per record
    assert sources == [[], [(charged, 0)], [(charged, 1)]] and families[charge].lines == 4 * 3
    assert [r for r, _ in board.laid_rows()] == [0, 1]  # each body of the charged family its own record
    sine = math.isqrt(PAIR[1] ** 2 - PAIR[0] ** 2)  # the lay by the invariant 2 A^2 sin omega = T
    amplitude = math.isqrt(T * PAIR[1] // (2 * sine))
    quantum = amplitude * (amplitude * sine // PAIR[1])  # the one-Node record's Wronskian, T / 2
    assert abs(quantum - T // 2) <= 2 * amplitude
    time_lines = [board.states[charge].lines[4 * row].now for row in range(3)]  # the rows at the start
    for record, (x, sense) in enumerate(((3, 1), (6, -1))):
        wronskian = records.wronskian(board.lines_of(charged, record), True)
        assert int(wronskian[x, 0, 0]) == sense * quantum and int(np.count_nonzero(wronskian)) == 1
        own = sense * time_lines[record + 1]  # the row's rest at the start, of its own record's sense
        assert (own >= 0).all() and own[x, 0, 0] > 0
    assert not time_lines[0].any()  # the free row: nothing sources it and no light is laid
    rule = rule_integers(
        6000, 6000, GAMMA, GAMMA, GAMMA, None, board.unit
    )  # the vacuum's rule, the mass 0
    empty = records.empty_record(board.shape, board.kind)
    for _ in range(3):
        states, lines = board.states, list(board.states[charge].lines)
        remainders = [r.copy() for r in states[charge].write_remainders]
        bookings = board.stepped(charged, 1)[1]  # the bookings about the step, as the step books them
        for record in (0, 1):
            other = 4 * (2 - record)  # the other record's row: its time line and its three odd lines
            turn = node.turning(charged, families, states, 1, record)
            assert np.array_equal(turn[0], lines[other].now) and lines[4 * (record + 1)].now.any()
            assert all(np.array_equal(a, lines[other + 1 + axis].now) for axis, a in enumerate(turn[1]))
            blank = [*states[:charge], records.NodeState(list(lines), remainders), *states[charge + 1 :]]
            blank[charge].lines[4 * (record + 1) : 4 * (record + 2)] = [empty] * 4  # the own row zeroed
            zeroed = node.turning(charged, families, blank, 1, record)
            assert np.array_equal(zeroed[0], turn[0])  # the self-read 0 to the bit
            assert all(np.array_equal(a, b) for a, b in zip(zeroed[1], turn[1], strict=True))
        board.step()
        for record in (0, 1):
            line, own = 4 * (record + 1), records.wronskian(bookings[record][1], True)
            fixed = np.asarray(board.fixed_walls[charge][line], dtype=object)  # the wall fixed per Node
            expected = (
                flux_step_line(lines[line], rule, board.wrap).now
                + (
                    k_w
                    * families[charge].write_wall
                    * factor
                    * own
                    * (fixed // (T * families[charge].write_wall * multiple))
                    + remainders[line]
                )
                // fixed
            )  # the carried factor at the vacuum's rulers: the write's wall T times the charge multiple scaled to the fixed wall, the Wronskian times the reader's charge factor (The constants, 2026-10-24)
            assert (
                int(
                    np.abs(
                        np.asarray(board.states[charge].lines[line].now, dtype=object) - expected
                    ).max()
                )
                <= 1
            ), (  # within one unit: the charge multiple's scaling of the fixed wall rounds once (2026-10-24; the equality to the bit until then)
                board.interval,
                record,
            )
    document, mode_path = json.loads(path.read_text(encoding="utf-8")), path.with_suffix(".mode.json")
    for nodes in ([{"node": [3, 0, 0], "count": 2}], [{"node": [x, 0, 0], "count": 1} for x in (3, 4)]):
        document["bodies"][0]["nodes"] = nodes
        path.write_text(json.dumps(document), encoding="utf-8")
        mode = {**json.loads(mode_path.read_text("utf-8")), "world_digest": input_digest(document)}
        mode_path.write_text(json.dumps(mode), encoding="utf-8")
        refused("one quantum of its family", load_world, path)


HOLDER = {"name": "nuclear", "pair": [50, 51], "reads": {"gravity": 1, "binding": 1, "nuclear": 1}}
HOLDER["held"] = {"sources": ["form"], "level_weight": 1, "write_weight": 300}  # E_n, W_1
NUCLEON = {"name": "nucleon", "pair": list(PAIR), "dimension": ["plane"] * 3, "reads": HOLDER["reads"]}
COMPACT = {"kind": "fixed_point", "stop": 2, "passes": 30, "seed": "compact", "profile": [1, 4]}
K2 = (32, 1)  # the budget's confidence multiple squared, the shipped lays' key
NUCLEUS, CUBE = (
    32,
    9,
)  # the design's count (25 under the bolometer's unit; 32 the least that binds in the family's quantum, 31 and 35 clouds) and the open cube's side
