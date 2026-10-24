"""The click's books of the piece's momentum (ALGEBRA.md, The click's algebra beyond the law; the owner's rule, at the Nodes Rule3 only): at a click the write moves the count by one and writes nothing for the piece's momentum; p_a and the record's P_a are read and booked on the credit line with the piece's source drawn and named and the recoil it owes, -p_a as integers, and the recoil of a body held at declared Nodes is the declaration's. Two statements of the books on the shipped worlds: on the chain world every take books the piece lost to the taker and the recoil owed by the lay or by the source body, its write the taker's re-lay at its own Nodes alone, and every close of a body's window keeps the body's own P within D4's bound (`act.parted`, `take.recoiled`, `take.relaid`; Part H, MUST 1 as a statement of the books); on the packet world the directed packet's emission books the recoil owed at the lay and names it on the taker's later line (`act.written`, `BOOKED_AT_EMISSION`)."""

import math
from dataclasses import replace

import numpy as np

from event_universe import act, take
from event_universe.emission import Emitter
from event_universe.lattice import Lattice
from event_universe.reports import (
    BOOKED_AT_EMISSION,
    LOST_TO_SOURCE,
)
from event_universe.world_files import load_world
from tests import laws
from tests.laws import EVENTS, family


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
