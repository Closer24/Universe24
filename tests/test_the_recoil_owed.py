"""The click's books of the piece's momentum (ALGEBRA.md, The click's algebra beyond the law; the owner's rule, at the Nodes Rule3 only): at a click the write moves the count by one and writes nothing for the piece's momentum; p_a and the record's P_a are read and booked on the credit line with the piece's source drawn and named and the recoil it owes, -p_a as integers, and the recoil of a body held at declared Nodes is the declaration's. Three statements of the books on the surviving worlds: a body's click books the piece lost to the taker and the source's recoil lost to the source, its write the taker's re-lay alone (`act.parted`, `twist.recoiled`); the directed packet's emission books the recoil owed at the lay and names it on the taker's later line (`act.written`, `PAID_AT_EMISSION`); the null window's re-lay keeps each body's own P within D4's bound and the board's P is the fan's alone (Part H, MUST 1 as a statement of the books)."""

import math
from dataclasses import replace

import numpy as np

from event_universe import act, readings, records, twist, world_files
from event_universe.emission import Emitter
from event_universe.lattice import Lattice
from event_universe.reports import LOST_TO_SOURCE, LOST_TO_TAKER, NO_DRAW, PAID_AT_EMISSION
from event_universe.world_files import load_world
from tests import laws
from tests.laws import EMIT_RUN, EVENTS, d4_bound, drift_bound, emit_and_take_world, family, levels_floor


def own_p(board: Lattice, books) -> int:  # type: ignore[no-untyped-def]
    """A body's own P_x in T's unit: its record's momentum terms over its Nodes (`readings.momentum_of`, `twist.scaled`)."""
    weight, at = board.families[books.index].pair[0], board.mask(books.nodes)
    read = readings.momentum_of(weight, board.lines_of(books.index, books.record), board.wrap, at)
    return twist.scaled(read, weight)[0]


def emit_and_take(tmp_path, window: int, intervals: int):  # type: ignore[no-untyped-def]
    """The emit-and-take world run `intervals` intervals with the bodies' own P_x per interval, the board's P before the emission, the light's P over the source's span with the drift bound, and the board's P once the front has passed."""
    path = emit_and_take_world(tmp_path, list(range(6)), list(range(12, 18)), window=window)
    board = Lattice(load_world(path), (lines := []).append)
    atom, light = family(board, "atom"), family(board, "pulse")
    marks, before, during, bound, after, floor = [], None, [], 0, None, None
    for _ in range(intervals):
        if not any(c["event"] == "credit" for c in lines):
            before = twist.fan_momentum(board, light)[0] + twist.fan_momentum(board, atom)[0]
        if board.credit.sources:
            bound += drift_bound(board, light)
        board.step()
        marks.append(
            (
                board.interval,
                [own_p(board, b) for b in board.credit.bodies],
                [b.windows for b in board.credit.bodies],
            )
        )
        if board.credit.sources:
            during.append(twist.fan_momentum(board, light)[0])
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
    return board, lines, marks, (before, during, bound, after, floor)


def test_a_bodys_click_books_the_piece_lost_to_the_taker_and_the_recoil_lost_to_the_source(
    tmp_path, monkeypatch
):
    """The emit-and-take world (the emitter's window 61, the taker's 48, EMIT_RUN intervals; the read's intervals pinned 2026-10-20: the emission at 61 at the window's close with no draw, the take at 174): the taker's credit line books the piece p_a in T's unit, the fan 0 (the one-Node lay even about its Node), `source` body 0, `recoil` = -p_a per axis and `lost` [P lost to the taker, recoil lost to the source], the emitter's outstanding count down to 0; the write is the taker's re-lay alone, every `lay` line at the click on the taker's record's lines and none on the source's; the taker's own P_x stands within D4's bound across its click and the light's P over the source's span within the drift bound; once the front has passed, the board's P (the light's and the bodies') is within the floor of its value before the emission, 0: the piece is booked and nowhere written."""
    monkeypatch.setattr(world_files, "REPOSITORY_ROOT", tmp_path)
    board, lines, marks, (before, during, bound, after, floor) = emit_and_take(tmp_path, 61, EMIT_RUN)
    atom, light = family(board, "atom"), family(board, "pulse")
    credits = [c for c in lines if c["event"] == "credit" and c["label"] == "NODEDETECTOR"]
    given, taken = (
        [c for c in credits if c["emitted"] == "pulse"],
        [c for c in credits if c["absorbed"] == "pulse"],
    )
    assert [(c["interval"], c["node_detector"]) for c in given] == [(61, "body 0")]
    assert given[0]["lost"] == [NO_DRAW] and given[0]["recoil"] is None and given[0]["momentum"] is None
    assert [(c["interval"], c["node_detector"]) for c in taken] == [(174, "body 1")]
    click = taken[0]
    assert click["momentum"][0] < 0 and click["momentum"][1:] == [0, 0] and click["fan"] == [0, 0, 0]
    assert click["source"] == "body 0" and click["recoil"] == [-p for p in click["momentum"]]
    assert click["lost"] == [LOST_TO_TAKER, LOST_TO_SOURCE]
    assert board.credit.emitters[light] == [Emitter(0, 0, False)]
    taker = board.credit.bodies[1]
    own = records.record_slice(board.families[atom], taker.record)
    laid = [x for x in lines if x["event"] == "lay" and x["interval"] == 174]
    assert laid and all(x["family"] == "atom" and own.start <= x["line"] < own.stop for x in laid)
    by_interval = {t: ps for t, ps, _w in marks}
    moved = by_interval[174][1] - by_interval[173][1]
    assert abs(moved) <= d4_bound(board, atom, taker.nodes)[0]
    assert before == 0 and during and max(abs(p) for p in during) <= bound
    assert after is not None and floor is not None and abs(after[1] + after[2] - before) <= floor
    print(
        f"the click at 174: p = {click['momentum']}, source {click['source']}, recoil {click['recoil']}, lost {click['lost']}; "
        f"{len(laid)} lay lines at the click, the taker's record's alone; the taker's own P_x {by_interval[173][1]} to "
        f"{by_interval[174][1]} (D4 {d4_bound(board, atom, taker.nodes)[0]}); the light's P over the span at most "
        f"{max(abs(p) for p in during)} (the bound {bound}); after the front passed ({after[0]}) the light's {after[1]} and "
        f"the bodies' {after[2]} against {before} before the emission, the floor {floor}"
    )


def test_the_directed_packets_recoil_is_booked_at_the_lay_and_named_at_the_take(tmp_path, monkeypatch):
    """The shipped packet world (examples/events/packet_emission: width 4, lifetime 48, [2, 3]) given one directed packet by the write step: the packet's lattice momentum at birth, read from the lay's own terms (`emission.laid_packet`, `readings.momentum_of`, no sine), within a tenth of the hands' 2 T sin k_z, cos k_z = 3 (den_l / num_l) cos Omega - 2 cos(pi / (w + 1)); the giver's books take its negative in T's unit as the recoil owed with the readings [recoil paid at the emission, recoil lost to the source], and the giver's record stands bit for bit, the lay the light's alone; the emitter registered with the recoil booked (`Emitter.paid`), and the piece's source drawn at a later take names body 0 with -P owed and the reading `PAID_AT_EMISSION`, its outstanding count down to 0."""
    packet = EVENTS / "packet_emission" / "packet_emission.json"
    board = Lattice(load_world(laws.world_beside(tmp_path, packet, lambda w: None)), [].append)
    light, atom = family(board, "pulse"), family(board, "atom")
    giver, action = board.credit.bodies[0], board.world.quantum_action
    rate = giver.declared.rates[0]
    assert rate.width == 4 and rate.resonance == (2, 3) and (0, 1) in rate.directions
    item = twist.Item(
        light, None, None, 1, (giver.nodes[0],), None, rate.resonance, rate.lifetime, emitter=0
    )
    stood = [
        (r.now.copy(), r.before.copy(), r.remainder.copy()) for r in board.lines_of(atom, giver.record)
    ]
    act.written(board, [replace(item, width=rate.width, direction=(0, 1))])
    born = twist.fan_momentum(board, light)
    cosine = 3 * (2 / 3) - 2 * math.cos(math.pi / (rate.width + 1))
    hands = 2 * action * math.sqrt(1 - cosine * cosine)
    assert born[1:] == (0, 0) and abs(born[0] - hands) < 0.1 * hands
    assert giver.recoil == [-p for p in born]  # the recoil owed, in T's unit as the fan is read
    assert giver.lost == [PAID_AT_EMISSION, LOST_TO_SOURCE]
    assert all(
        np.array_equal(a, b)
        for r, kept in zip(board.lines_of(atom, giver.record), stood, strict=True)
        for a, b in zip((r.now, r.before, r.remainder), kept, strict=True)
    )
    assert board.credit.emitters[light] == [Emitter(0, 1, True)]
    source, owed, reading = twist.recoiled(board, light, (born[0], 0, 0), lambda weights: 0)
    assert (source, owed, reading) == ("body 0", [-born[0], 0, 0], PAID_AT_EMISSION)
    assert board.credit.emitters[light][0].outstanding == 0
    print(
        f"the packet's P_x at birth {born[0]} against the hands' 2 T sin k_z = {hands:.0f}; the giver's recoil "
        f"{giver.recoil} with {giver.lost}, its record standing; the take names {source} owing {owed}, {reading}"
    )


def test_the_null_windows_re_lay_keeps_each_bodys_own_p_and_the_boards_p_is_the_fans(
    tmp_path, monkeypatch
):
    """Part H, MUST 1 as a statement of the books (the emitter's window 48, shorter than the run, 400 intervals; the read's intervals pinned 2026-10-20: the emission at 48, the take at 353, the bodies' windows closed 7 and 6 times): across every close of a body's window, the null windows' re-lays among them, the body's own P_x moves within D4's bound (each Node laid again in its own direction, `twist.relaid`), the taker's across its click too; the one-Node source's light carries no P over its span beyond the drift bound (the fan 0 on the taker's line), so the board's P once the front has passed is within the floor of its value before the emission: the board's P falls by the fan and the books carry the piece and the recoil owed."""
    monkeypatch.setattr(world_files, "REPOSITORY_ROOT", tmp_path)
    board, lines, marks, (before, during, bound, after, floor) = emit_and_take(tmp_path, 48, 400)
    atom = family(board, "atom")
    credits = [c for c in lines if c["event"] == "credit" and c["label"] == "NODEDETECTOR"]
    assert [(c["interval"], c["node_detector"], c["absorbed"], c["emitted"]) for c in credits] == [
        (48, "body 0", None, "pulse"),
        (353, "body 1", "pulse", None),
    ]
    click = credits[1]
    assert click["fan"] == [0, 0, 0] and click["recoil"] == [-p for p in click["momentum"]]
    assert click["lost"] == [LOST_TO_TAKER, LOST_TO_SOURCE] and [
        b.windows for b in board.credit.bodies
    ] == [7, 6]
    bounds = [d4_bound(board, atom, b.nodes)[0] for b in board.credit.bodies]
    closes = [
        (t, body, ps[body] - marks[k - 1][1][body])
        for k, (t, ps, windows) in enumerate(marks)
        if k
        for body in range(2)
        if windows[body] != marks[k - 1][2][body]
    ]
    assert len(closes) == 13 and all(abs(moved) <= bounds[body] for _t, body, moved in closes)
    assert before == 0 and during and max(abs(p) for p in during) <= bound
    assert after is not None and floor is not None and abs(after[1] + after[2] - before) <= floor
    print(
        f"the closes {[(t, body, moved) for t, body, moved in closes]} within D4 {bounds}; the click at 353: "
        f"p = {click['momentum']}, recoil {click['recoil']}, {click['lost']}; after the front passed ({after[0]}) the "
        f"light's {after[1]} and the bodies' {after[2]} against {before}, the floor {floor}"
    )
