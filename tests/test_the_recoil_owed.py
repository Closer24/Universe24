"""The click's books of the piece's momentum (ALGEBRA.md, The click's algebra beyond the law; the owner's rule, at the Nodes Rule3 only): at a click the write moves the count by one and writes nothing for the piece's momentum; p_a and the record's P_a are read and booked on the credit line with the piece's source drawn and named and the recoil it owes, -p_a as integers, and the recoil of a body held at declared Nodes is the declaration's. Two statements of the books on the shipped worlds: on the chain world every take books the piece lost to the taker and the recoil owed by the lay or by the source body, its write the taker's re-lay at its own Nodes alone, and every close of a body's window keeps the body's own P within D4's bound (`act.parted`, `take.recoiled`, `take.relaid`; Part H, MUST 1 as a statement of the books); on the packet world the directed packet's emission books the recoil owed at the lay and names it on the taker's later line (`act.written`, `BOOKED_AT_EMISSION`)."""

import math
from dataclasses import replace

import numpy as np

from event_universe import act, readings, take, world_files
from event_universe.emission import Emitter
from event_universe.lattice import Lattice
from event_universe.reports import (
    BOOKED_AT_EMISSION,
    LOST_TO_LAY,
    LOST_TO_SOURCE,
    LOST_TO_TAKER,
    NO_DRAW,
    THE_LAY,
)
from event_universe.world_files import load_world
from tests import laws
from tests.laws import EVENTS, d4_bound, family
from tests.laws_content import TWO_ATOMS, content_copy
from tests.laws_read import load_shipped


def own_p(board: Lattice, books) -> int:  # type: ignore[no-untyped-def]
    """A body's own P_x in T's unit: its record's momentum terms over its Nodes (`readings.momentum_of`, `take.scaled`)."""
    weight, at = board.families[books.index].pair[0], board.mask(books.nodes)
    read = readings.momentum_of(weight, board.lines_of(books.index, books.record), board.wrap, at)
    return take.scaled(read, weight)[0]


def test_the_chains_clicks_book_the_piece_and_the_recoil_owed_and_every_close_keeps_the_bodys_p(
    tmp_path, monkeypatch
):
    """The shipped chain world chain_x_minus over its 400 intervals (the clicks pinned 2026-10-20 under the twist's deletion: the takes at 74, 142 and 307 and the emissions at the windows' closes 122, 190 and 355, the third pair moved from (303, 351) by the fold's quarter turn on the second body's part, which had entered the born light's phase at 190): at every take the credit line books the piece p_a in T's unit, the fan equal to the light's P over the board at the click's interval, `recoil` = -p_a per axis and the source drawn and named, the piece taken at 74 the file's lay's and no body's (`THE_LAY`), its line [P lost to the taker, recoil lost to the lay], the pieces taken at 142 and 307 the source bodies' (body 0, body 1), their lines [P lost to the taker, recoil lost to the source]; every emission falls at its window's close with no draw, no piece and no recoil; the write at a take is the taker's re-lay alone, every lay line of the atom at the click at the taker's Nodes and none at the other body's; across every close of a body's window, the null re-lays at 217 and 355 among the eight, the body's own P_x moves within D4's bound, and the emitters' book ends with the lay spent, body 0 owed one quantum and body 1 none."""
    path = content_copy(tmp_path, EVENTS / "chain" / "chain_x_minus.json", TWO_ATOMS)
    board = Lattice(
        load_world(path), (lines := []).append
    )  # the content copy: the shipped world's run is refused by name at the body 0 of 'atom' at the interval 122 (the law's third refusal of the click's read, ALGEBRA.md The digits' budget: the room 2^45.8 of the digits read, the photon's five at three values each on the universe two_atoms.json, which declares no content, and the atom's three at the lay's origin, below the absorption draw's total 2^51.5; the former course took at 74 by the same number read, the rest weight's booking centred on 2026-10-23 moving the residue to the cell none takes), so the claim is read on the content copy (tests/laws_content.content_world, the born universe's holders prepended), which carries every draw
    atom, light = family(board, "atom"), family(board, "photon")
    marks = []
    for _ in range(board.world.intervals):
        board.step()
        marks.append(
            (
                board.interval,
                [own_p(board, b) for b in board.credit.bodies],
                [b.windows for b in board.credit.bodies],
                take.fan_momentum(board, light)[0],
            )
        )
    by_interval = {t: (ps, windows, p_light) for t, ps, windows, p_light in marks}
    credits = [c for c in lines if c["event"] == "credit" and c["label"] == "NODEDETECTOR"]
    takes = [c for c in credits if c["absorbed"]]
    emissions = [c for c in credits if c["emitted"]]
    assert (
        takes and emissions
    )  # the pair: a take and the emission that gives the quantum back (the shipped course's takes at 74, 142 and 307 and emissions at 122, 190 and 355 the former numbers; the copy's takes at 143 and 311, its emission at 195)
    sources, giver = (
        {},
        (THE_LAY, LOST_TO_LAY),
    )  # each take's source: the lay first, then the body that emitted last
    for click in credits:
        if click["absorbed"]:
            sources[click["interval"]] = giver
        elif click["emitted"]:
            giver = (click["node_detector"], LOST_TO_SOURCE)
    bounds = [d4_bound(board, atom, b.nodes)[0] for b in board.credit.bodies]
    for click in credits:
        t, body = click["interval"], int(click["node_detector"].split()[1])
        if not click["absorbed"]:
            assert click["momentum"] is None and click["recoil"] is None  # no piece without a take
            assert not click["lost"] or click["lost"] == [
                NO_DRAW
            ]  # a close drawn none, or the dark fall
            continue
        assert click["momentum"][1:] == [0, 0] and click["momentum"][0] != 0
        assert click["recoil"] == [-p for p in click["momentum"]]
        assert (click["source"], click["lost"]) == (sources[t][0], [LOST_TO_TAKER, sources[t][1]])
        assert click["fan"] == [by_interval[t][2], 0, 0]  # the light's P over the board at the click
        taker = {tuple(n) for n in board.credit.bodies[body].nodes}
        laid = [x for x in lines if x["event"] == "lay" and x["interval"] == t and x["family"] == "atom"]
        assert laid and all(tuple(x["node"]["at"]) in taker for x in laid)
        assert abs(by_interval[t][0][body] - by_interval[t - 1][0][body]) <= bounds[body]
    closes = [
        (t, body, ps[body] - marks[k - 1][1][body])
        for k, (t, ps, windows, _p) in enumerate(marks)
        if k
        for body in range(2)
        if windows[body] != marks[k - 1][2][body]
    ]
    assert {(c["interval"], int(c["node_detector"].split()[1])) for c in takes} <= {
        (t, body) for t, body, _moved in closes
    }  # every take at a close of its body's window (an emission is the hazard's own draw, any interval)
    assert all(abs(moved) <= bounds[body] for _t, body, moved in closes)
    assert board.credit.emitters[light][0] == Emitter(None, 0, False) and [
        e.body for e in board.credit.emitters[light][1:]
    ] == [int(c["node_detector"].split()[1]) for c in emissions]  # the lay, then each emitter in order
    print(
        f"the chain's takes {[(c['interval'], c['momentum'][0], c['source'], c['recoil'][0]) for c in credits if c['absorbed']]}, "
        f"the fans {[c['fan'][0] for c in credits if c['absorbed']]}; the bodies' own P across the closes "
        f"{[(t, body, moved) for t, body, moved in closes]} within D4 {bounds}"
    )


def test_the_directed_packets_recoil_is_booked_at_the_lay_and_named_at_the_take(tmp_path, monkeypatch):
    """The shipped packet world (examples/events/packet_emission: width 4, lifetime 48, [2, 3]) given one directed packet by the write step: the packet's lattice momentum at birth, read from the lay's own terms (`emission.laid_packet`, `readings.momentum_of`, no sine), within a tenth of the hands' 2 T sin k_z, cos k_z = 3 (den_l / num_l) cos Omega - 2 cos(pi / (w + 1)); the giver's books take its negative in T's unit as the recoil owed with the readings [recoil booked at the emission, recoil lost to the source], and the giver's record stands bit for bit, the lay the light's alone; the emitter registered with the recoil booked (`Emitter.booked`), and the piece's source drawn at a later take names body 0 with -P owed and the reading `BOOKED_AT_EMISSION`, its outstanding count down to 0."""
    packet = EVENTS / "packet_emission" / "packet_emission.json"
    board = Lattice(load_world(laws.world_beside(tmp_path, packet, lambda w: None)), [].append)
    light, atom = family(board, "pulse"), family(board, "atom")
    giver, action = board.credit.bodies[0], board.world.quantum_action
    rate = giver.declared.rates[0]
    assert rate.width == 4 and rate.resonance == (2, 3) and (0, 1) in rate.directions
    item = take.Item(
        light, None, None, 1, (giver.nodes[0],), None, rate.resonance, rate.lifetime, emitter=0
    )
    stood = [
        (r.now.copy(), r.before.copy(), r.remainder.copy()) for r in board.lines_of(atom, giver.record)
    ]
    act.written(board, [replace(item, width=rate.width, direction=(0, 1))])
    born = take.fan_momentum(board, light)
    cosine = 3 * (2 / 3) - 2 * math.cos(math.pi / (rate.width + 1))
    hands = 2 * action * math.sqrt(1 - cosine * cosine)
    assert born[1:] == (0, 0) and abs(born[0] - hands) < 0.1 * hands
    assert giver.recoil == [-p for p in born]  # the recoil owed, in T's unit as the fan is read
    assert giver.lost == [BOOKED_AT_EMISSION, LOST_TO_SOURCE]
    assert all(
        np.array_equal(a, b)
        for r, kept in zip(board.lines_of(atom, giver.record), stood, strict=True)
        for a, b in zip((r.now, r.before, r.remainder), kept, strict=True)
    )
    assert board.credit.emitters[light] == [Emitter(0, 1, True)]
    source, owed, reading = take.recoiled(board, light, (born[0], 0, 0), lambda weights: 0)
    assert (source, owed, reading) == ("body 0", [-born[0], 0, 0], BOOKED_AT_EMISSION)
    assert board.credit.emitters[light][0].outstanding == 0
    print(
        f"the packet's P_x at birth {born[0]} against the hands' 2 T sin k_z = {hands:.0f}; the giver's recoil "
        f"{giver.recoil} with {giver.lost}, its record standing; the take names {source} owing {owed}, {reading}"
    )
