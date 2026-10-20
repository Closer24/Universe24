"""Part G, the source as partner, the click with two receivers (both hands' lines of 2026-10-10, the mathematician's 6091663984 and the advisor's 6091670073, the Boss's merged line 6091735946): at a click the write conserves the lattice momentum with two receivers, the taker's part folded by +p_a and the piece's source's part by -p_a, at the click's tick by one twist (`twist.recoiled`, `twist.folded_source`); the erasure removes only the fan's own P_a, zero to the floor for a lay at one Node; the source is drawn among the emitters by the quanta each still holds in the record (`credit.Books.emitters`), one source no draw; where no body emitted, the recoil is booked lost to the lay. The emit-and-take world: a periodic chain of 48 of the resonance world's universe, body 0 an excited atom on six Nodes along x at count 1 emitting at [2, 3] over the lifetime 48 (its window 61: in the exact dark its emission falls at the window's close, `meeting.emission_fell`; a null window's re-lay keeps the fold, Part H), body 1 a ground atom of the same reach twelve Links on. The brief's four Nodes at count 1 carry 48,432 of the 52,566 a four-Node region reads at [2, 3] on this guide (the hands' 46,341 is the pi / 4 piece of one_photon's packets); six Nodes read 44,566 and carry it whole on both sides. Every integer printed for the Boss."""

import time


from event_universe import world_files
from event_universe.lattice import Lattice
from event_universe.world_files import load_world
from tests import laws
from tests.laws import EMIT_RUN as RUN
from tests.laws import EVENTS, emit_and_take_world
from tests.laws_read import load_shipped

T = 32768
STRIPPED = {"momentum", "fan", "twist", "lost", "source", "recoil"}  # the Boss's check strips these


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


def test_resonant_runs_green_and_names_atom_0_as_the_source_at_the_taking_click():
    """Task 5 (g): examples/events/resonance/resonant.json runs its 96 intervals green (atom 0 gives at 61, its line's `recoil` None: the source in time pays none at the lay); stepped on to the third close of atom 1's window (288; within the file's 96 intervals atom 1 takes nothing, a finding reported) atom 1 takes with `source` body 0; its recoil and lost printed (the two-Node atoms carry this piece: the wave's p at the two-Node region after its circulation reads below their reach)."""
    world_files.REPOSITORY_ROOT = EVENTS.parents[1]
    board = Lattice(load_shipped(EVENTS / "resonance" / "resonant.json"), (lines := []).append)
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
