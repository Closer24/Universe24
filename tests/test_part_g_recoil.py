"""Part G, the source as partner, the click with two receivers (both hands' lines of 2026-10-10, the mathematician's 6091663984 and the advisor's 6091670073, the Boss's merged line 6091735946): at a click the write conserves the lattice momentum with two receivers, the taker's part folded by +p_a and the piece's source's part by -p_a, at the click's tick by one twist (`twist.recoiled`, `twist.folded_source`); the erasure removes only the fan's own P_a, zero to the floor for a lay at one Node; the source is drawn among the emitters by the quanta each still holds in the record (`credit.Books.emitters`), one source no draw; where no body emitted, the recoil is booked lost to the lay. The emit-and-take world: a periodic chain of 48 of the resonance world's universe, body 0 an excited atom on six Nodes along x at count 1 emitting at [2, 3] over the lifetime 48 (its window longer than the run, so no null window re-lays it: a null window's re-lay discards a body's twist, Part F's taker's too, a finding reported and not hidden), body 1 a ground atom of the same reach twelve Links on. The brief's four Nodes at count 1 carry 48,432 of the 52,566 a four-Node region reads at [2, 3] on this guide (the hands' 46,341 is the pi / 4 piece of one_photon's packets); six Nodes read 44,566 and carry it whole on both sides. Every integer printed for the Boss."""

import json
import time
from dataclasses import replace
from pathlib import Path

import numpy as np

from event_universe import emission, meeting, node, twist, world_files
from event_universe.lattice import Lattice
from event_universe.reports import (
    LOST_TO_LAY,
    LOST_TO_SOURCE,
    LOST_TO_TAKER,
    PAID_AT_EMISSION,
    THE_LAY,
)
from event_universe.world_files import load_world
from tests import laws
from tests.laws import EMIT_RUN as RUN
from tests.laws import EVENTS, emit_and_take_world, levels_floor, one_photon_board

T = 32768
ORACLE = Path(__file__).resolve().parent / "oracle" / "one_photon_before_g.output.json"
STRIPPED = {"momentum", "fan", "twist", "lost", "source", "recoil"}  # the Boss's check strips these


def drift_bound(board: Lattice, index: int) -> int:
    """The hands' bound on the integers' drift of P_x per step in T's unit, 2 SUM_i |now_(i+1) - now_(i-1)| (Part F, test (a))."""
    chain = board.shape[0]
    found = 0
    for r in laws.own_lines(board, index):
        now = r.now.reshape(-1).astype(object)
        found += int(sum(abs(now[(i + 1) % chain] - now[(i - 1) % chain]) for i in range(chain)))
    return 2 * found


def test_a_body_emits_and_another_takes_and_the_source_is_folded_by_the_recoil(tmp_path, monkeypatch):
    """Task 5 (a) to (d). (a) At the emission's intervals (the source in time's 48 lays from 61) the light's P_x over the board stays within the accumulated drift bound (it reads 0: the one-Node lay is even about its Node). (b) At body 1's click (144) the credit line names `source` body 0, `recoil` = -`momentum` per axis and `lost` None: the six-Node taker carries +p and the six-Node source carries -p. (c) P over the board and the two bodies before the emission equals P after the front has passed, to the floor of the two folds' roundings, read after the front and before the taker's next window closes (192, whose null window re-lays the body); the three integers and the floor printed. (d) The reversal with the books through the emission, the click, the two folds and the front is bit for bit (tools/back_in_time: MATCH)."""
    monkeypatch.setattr(world_files, "REPOSITORY_ROOT", tmp_path)
    path = emit_and_take_world(tmp_path, list(range(6)), list(range(12, 18)))
    board = Lattice(load_world(path), (lines := []).append)
    atom = next(i for i, f in enumerate(board.families) if f.name == "atom")
    light = next(i for i, f in enumerate(board.families) if f.name == "pulse")
    before_emission = None
    light_during, bound = [], 0
    after, floor = None, None
    for _ in range(RUN):
        if not any(c["event"] == "credit" for c in lines):  # before the emission's click
            before_emission = twist.fan_momentum(board, light)[0] + twist.fan_momentum(board, atom)[0]
        if board.credit.sources:
            bound += drift_bound(board, light)
        board.step()
        if board.credit.sources:  # the emission's intervals: the light's P over the board
            light_during.append(twist.fan_momentum(board, light)[0])
        taken = [c for c in lines if c["event"] == "credit" and c["absorbed"] == "pulse"]
        if taken and after is None and not board.credit.fronts and board.credit.counts[light] == 0:
            after = (
                board.interval,
                twist.fan_momentum(board, light)[0],
                twist.fan_momentum(board, atom)[0],
            )
            at = np.zeros(board.shape, dtype=bool)
            for books in board.credit.bodies:
                at |= board.mask(books.nodes)
            floor = levels_floor(board, atom, at) + 2  # the two readings' own roundings
    credits = [c for c in lines if c["event"] == "credit" and c["label"] == "NODEDETECTOR"]
    given = [c for c in credits if c["emitted"] == "pulse"]
    taken = [c for c in credits if c["absorbed"] == "pulse"]
    assert len(given) == 1 and given[0]["node_detector"] == "body 0" and given[0]["recoil"] is None
    assert len(taken) == 1 and taken[0]["node_detector"] == "body 1"
    click = taken[0]
    # (a) the one-Node lay carries no P
    assert light_during and max(abs(p) for p in light_during) <= bound
    # (b) the two receivers
    assert click["source"] == "body 0" and click["lost"] is None
    assert click["recoil"] == [-p for p in click["momentum"]] and click["momentum"][0] < 0
    assert board.credit.emitters[light][0].outstanding == 0
    # (c) P conserved over the board and the two bodies to the floor
    assert before_emission == 0 and after is not None and floor is not None
    total_after = after[1] + after[2]
    assert abs(total_after - before_emission) <= floor, (before_emission, after, floor)
    print(
        f"Part G (5a-c): the light's P_x over the emission's {len(light_during)} intervals at most "
        f"{max(abs(p) for p in light_during)} (the bound {bound}); the click at {click['interval']}: p = {click['momentum']}, "
        f"source {click['source']}, recoil {click['recoil']}, twist {click['twist']}, lost {click['lost']}; P before the "
        f"emission {before_emission}, after the front passed (interval {after[0]}) the light's {after[1]} and the two bodies' "
        f"{after[2]}, the total {total_after}, the floor {floor}"
    )


def test_the_emit_and_take_world_runs_back_through_the_emission_the_click_and_the_two_folds(
    tmp_path, monkeypatch
):
    """Task 5 (d): the reversal with the books on the same world (the emitter's window 240), RUN intervals forward and back through the emission, the click and the two folds, MATCH; its own test so that each half of Task 5 runs under the suite's bound."""
    monkeypatch.setattr(world_files, "REPOSITORY_ROOT", tmp_path)
    started = time.perf_counter()
    path = emit_and_take_world(tmp_path, list(range(6)), list(range(12, 18)))
    verdict = laws.BACK.verdict(Lattice(load_world(path)), RUN)
    assert verdict["verdict"] == "MATCH", verdict
    print(
        f"Part G (5d): {RUN} forward and back through the emission, the click and the two folds: MATCH; {time.perf_counter() - started:.1f} s"
    )


def test_the_lays_case_on_one_photon_books_the_recoil_lost_to_the_lay(tmp_path, monkeypatch):
    """Task 5 (e): one_photon's first click (48): no body emitted the packets, so `source` is the lay, `recoil` the negative of `momentum` with "recoil lost to the lay" after the taker's own loss, and the board unchanged against the Part F2 run recorded at 04caccce2 (the oracle's lines to 48, the six keys stripped as the Boss's check strips them)."""
    monkeypatch.setattr(world_files, "REPOSITORY_ROOT", tmp_path)
    board, lines = one_photon_board(tmp_path)
    for _ in range(48):
        board.step()
    credits = [c for c in lines if c["event"] == "credit"]
    assert len(credits) == 1 and credits[0]["interval"] == 48
    click = credits[0]
    assert click["source"] == THE_LAY and click["recoil"] == [-p for p in click["momentum"]]
    assert click["lost"] == [LOST_TO_TAKER, LOST_TO_LAY]
    oracle = json.loads(ORACLE.read_text(encoding="utf-8"))
    kinds = {"click", "density", "parts", "credit", "erasure", "lay", "face", "conversion"}

    def cleaned(found):  # type: ignore[no-untyped-def]
        return [
            {k: v for k, v in line.items() if k not in STRIPPED}
            for line in found
            if line["event"] in kinds and int(str(line["interval"])) <= 48
        ]

    assert cleaned(lines) == cleaned(oracle["lines"])
    print(
        f"Part G (5e): one_photon at 48: source {click['source']}, recoil {click['recoil']}, lost {click['lost']}; the board the Part F2 run's"
    )


def test_the_two_node_source_books_the_recoil_lost_to_the_source(tmp_path, monkeypatch):
    """Task 5 (f): the shipped two-Node atom as the emitter (count 1 on two Nodes along x, the hands' reach 32,400 against the piece) with the six-Node taker: the click books "recoil lost to the source", `recoil` the quarter turn's reading and the remainder |p| less it printed beside the hands' 46,341 - 32,400."""
    monkeypatch.setattr(world_files, "REPOSITORY_ROOT", tmp_path)
    path = emit_and_take_world(tmp_path, [0, 1], list(range(12, 18)))
    board = Lattice(load_world(path), (lines := []).append)
    for _ in range(RUN):
        board.step()
    taken = [c for c in lines if c["event"] == "credit" and c["absorbed"] == "pulse"]
    assert len(taken) == 1 and taken[0]["source"] == "body 0" and taken[0]["lost"] == [LOST_TO_SOURCE]
    click = taken[0]
    remainder = -click["momentum"][0] - click["recoil"][0]
    assert click["momentum"][0] < 0 < click["recoil"][0] < -click["momentum"][0]
    print(
        f"Part G (5f): the two-Node source: p = {click['momentum']}, recoil {click['recoil']} ({click['lost']}), "
        f"the remainder {remainder} against the hands' 46,341 - 32,400 = {46341 - 32400}"
    )


def test_resonant_runs_green_and_names_atom_0_as_the_source_at_the_taking_click():
    """Task 5 (g): examples/events/resonance/resonant.json runs its 96 intervals green (atom 0 gives at 61, its line's `recoil` None: the source in time pays none at the lay); stepped on to the third close of atom 1's window (288; within the file's 96 intervals atom 1 takes nothing, a finding reported) atom 1 takes with `source` body 0; its recoil and lost printed (the two-Node atoms carry this piece: the wave's p at the two-Node region after its circulation reads below their reach)."""
    world_files.REPOSITORY_ROOT = EVENTS.parents[1]
    board = Lattice(load_world(EVENTS / "resonance" / "resonant.json"), (lines := []).append)
    for _ in range(board.world.intervals):
        board.step()
    credits = [c for c in lines if c["event"] == "credit" and c["label"] == "NODEDETECTOR"]
    assert [c["emitted"] for c in credits] == ["pulse"] and credits[0]["recoil"] is None
    assert not [c for c in credits if c["absorbed"]]
    while board.interval < 288:
        board.step()
    taken = [c for c in lines if c["event"] == "credit" and c["absorbed"] == "pulse"]
    assert len(taken) == 1 and taken[0]["node_detector"] == "body 1" and taken[0]["source"] == "body 0"
    print(
        f"Part G (5g): resonant.json green over 96; stepped on, atom 1 takes at {taken[0]['interval']}: "
        f"p = {taken[0]['momentum']}, source {taken[0]['source']}, recoil {taken[0]['recoil']}, lost {taken[0]['lost']}"
    )


def test_the_directed_packets_recoil_is_paid_at_the_lay(tmp_path, monkeypatch):
    """Task 3: the shipped packet world (examples/events/packet_emission, width 4, lifetime 48, [2, 3]): the packet's lattice momentum at birth read from the lay's own terms (`emission.laid_packet`, `node.momentum_of`, no sine) against 2 T sin k_z, cos k_z = 3 (den_l / num_l) cos Omega - 2 cos(pi / (w + 1)) (the hands' 1.85 T); the write step folds the two-Node giver by its negative at the lay (`meeting.written`, `twist.folded_source`): the giver's books take `recoil` (its reach, the two-Node atom falling short) and `lost` ["recoil paid at the emission", "recoil lost to the source"], the emitter registered with the recoil paid, and a later click of this light would fold nothing more (`twist.recoiled`). The lay is written on the loaded board at its first interval, no stepping."""
    world_files.REPOSITORY_ROOT = EVENTS.parents[1]
    board = Lattice(load_world(EVENTS / "packet_emission" / "packet_emission.json"), [].append)
    light = next(i for i, f in enumerate(board.families) if f.name == "pulse")
    atom = next(i for i, f in enumerate(board.families) if f.name == "atom")
    giver = board.credit.bodies[0]
    rate = giver.declared.rates[0]
    assert rate.width == 4 and rate.resonance == (2, 3) and (0, 1) in rate.directions
    item = twist.Item(
        light, None, None, 1, (giver.nodes[0],), None, rate.resonance, rate.lifetime, emitter=0
    )
    item = replace(item, width=rate.width, direction=(0, 1))
    standing = node.momentum_of(
        board.families[atom].pair[0], board.lines_of(atom, giver.record), board.wrap
    )
    meeting.written(board, [item])
    num = board.families[light].pair[0]
    born = twist.fan_momentum(board, light)
    recoil, lost = giver.recoil, giver.lost
    assert recoil is not None and lost is not None and lost[0] == PAID_AT_EMISSION
    assert born[0] > 0 and born[1:] == (0, 0) and recoil[0] < 0 and recoil[1:] == [0, 0]
    folded = node.momentum_of(
        board.families[atom].pair[0], board.lines_of(atom, giver.record), board.wrap
    )
    assert folded[0] < standing[0]  # the giver recoils against the packet
    emitters = board.credit.emitters[light]
    assert (
        len(emitters) == 1
        and emitters[0].body == 0
        and emitters[0].paid
        and emitters[0].outstanding == 1
    )
    source, owed, reading = twist.recoiled(board, light, (born[0], 0, 0), lambda weights: 0)
    assert source == "body 0" and owed == [-born[0], 0, 0] and reading == PAID_AT_EMISSION
    assert emitters[0].outstanding == 0
    import math  # the test prints against the hands' sine; the engine reads no sine

    cosine = 3 * (2 / 3) - 2 * math.cos(math.pi / (rate.width + 1))
    hands = 2 * T * math.sqrt(1 - cosine * cosine)
    print(
        f"Part G (3): the packet's P_x at birth {born[0]} (num {num}) against 2 T sin k_z = {hands:.0f} "
        f"({born[0] / T:.3f} T, the hands' 1.85 T); the giver folded by -P: recoil {recoil}, lost {lost}, "
        f"the giver's P_x {standing[0]} -> {folded[0]}; the emitter registered paid"
    )
    assert abs(born[0] - hands) < 0.1 * hands
    assert emission.Emitter(0, 1, True) == emission.Emitter(0, 1, True)
