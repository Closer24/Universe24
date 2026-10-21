"""Part G, the source as partner, the click with two receivers (both hands' lines of 2026-10-10, the mathematician's 6091663984 and the advisor's 6091670073, the Boss's merged line 6091735946): at a click the write books the piece's momentum on the credit line with the source drawn and named and the recoil it owes, -p_a, and writes nothing for it (`take.recoiled`; ALGEBRA.md, The click's algebra beyond the law); the erasure removes only the fan's own P_a, zero to the floor for a lay at one Node; the source is drawn among the emitters by the quanta each still holds in the record (`credit.Books.emitters`), one source no draw; where no body emitted, the recoil is booked lost to the lay. The emit-and-take world: a periodic chain of 48 of the resonance world's universe, body 0 an excited atom on six Nodes along x at count 1 emitting at [2, 3] over the lifetime 48 (its window 61: in the exact dark its emission falls at the window's close, `meeting.emission_fell`; a null window's re-lay keeps each Node's own direction, Part H), body 1 a ground atom of the same reach twelve Links on. The brief's four Nodes at count 1 carry 48,432 of the 52,566 a four-Node region reads at [2, 3] on this guide (the hands' 46,341 is the pi / 4 piece of one_photon's packets); six Nodes read 44,566 and carry it whole on both sides. Every integer printed for the Boss."""

import time

import pytest

from event_universe import world_files
from event_universe.lattice import Lattice
from event_universe.world_files import load_world
from tests import laws
from tests.laws import EMIT_RUN as RUN
from tests.laws import EVENTS
from tests.laws_content import RESONANT, ZENO_ATOM, content_world, opened
from tests.laws_read import load_shipped

T = 32768
STRIPPED = {"momentum", "fan", "lost", "source", "recoil"}  # the Boss's check strips these


def test_the_emit_and_take_world_runs_back_through_the_emission_the_click_and_the_two_folds(monkeypatch):
    """Task 5 (d): the reversal with the books through the emission, the click and the two folds, MATCH; its own test so that each half of Task 5 runs under the suite's bound. Re-read 2026-10-20 under the click's read of the board (the reader's ruling): on the content-declared emit-and-take world the emitter's quantum leaves by the faces before any take, so a sentence of a take reads where its matter is, the shipped chain world chain_x_minus (examples/events/chain), which takes at 74 and 142 and emits at 122 and 190 within 200 intervals: 200 forward and back with the books through two takes with their folds and two emissions, MATCH (the emit-and-take ring over 240 before)."""
    monkeypatch.setattr(world_files, "REPOSITORY_ROOT", EVENTS.parents[1])
    started = time.perf_counter()
    verdict = laws.BACK.verdict(Lattice(load_shipped(EVENTS / "chain" / "chain_x_minus.json")), RUN)
    assert verdict["verdict"] == "MATCH", verdict
    print(
        f"Part G (5d): chain_x_minus {RUN} forward and back through two takes, their folds and two emissions: MATCH; {time.perf_counter() - started:.1f} s"
    )


def test_resonant_runs_green_and_names_atom_0_as_the_source_at_the_taking_click(tmp_path, monkeypatch):
    """Task 5 (g): examples/events/resonance/resonant.json runs its 162 intervals green (the pair over three Nodes since 2026-10-21, the reader's ruling; 96 intervals over two Nodes before: atom 0 gives at 48, the close of its window, the emission in the exact dark falling at the window's close; its line's `recoil` None: the source in time pays none at the lay; within the file's intervals atom 1 takes nothing, its close at 161 a count of 0, a finding reported; stepped on, the giver's third window closes at the exact vacuum and is refused at 191, as the two-Node pair's second was at 143). Re-read 2026-10-20 under the click's read of the board: the 96 intervals run as they stand (the shipped world whole), and stepped on, the read of the board at atom 0's close 143 is refused by name, the digits read there below the draw's total (light at the exact paces three values a digit); atom 1's take beyond 96, read before on the stepped-on world (288), is not read: on the content-declared copy (the universe with the holders of the content, the box opened along x as the content's sink, the windows derived 48 for both) stepped to 400, atom 0's first close at 48 reads no emission and the emission is drawn at 83, its window closes null at 96, and atom 1's six closes, 146 to 386, take nothing, the quantum leaving by the faces (the reader's and G's measurement)."""
    monkeypatch.setattr(world_files, "REPOSITORY_ROOT", EVENTS.parents[1])
    board = Lattice(load_shipped(EVENTS / "resonance" / "resonant.json"), (lines := []).append)
    for _ in range(board.world.intervals):
        board.step()
    credits = [c for c in lines if c["event"] == "credit" and c["label"] == "NODEDETECTOR"]
    assert [(c["interval"], c["emitted"], c["recoil"]) for c in credits] == [(48, "pulse", None)]
    assert not [c for c in credits if c["absorbed"]]
    with pytest.raises(
        RuntimeError, match="do not carry the draw"
    ) as refusal:  # stepped on: atom 0's close
        for _ in range(board.world.intervals, 400):
            board.step()
    assert board.interval == 191 and "the body 0 of 'atom' at the interval 191" in str(refusal.value)

    def long_run(world):  # type: ignore[no-untyped-def]
        opened(world)
        world["intervals"] = 400

    monkeypatch.setattr(world_files, "REPOSITORY_ROOT", tmp_path)
    copy = Lattice(
        load_world(content_world(tmp_path, "resonant", RESONANT, ZENO_ATOM, long_run)),
        (copied := []).append,
    )
    for _ in range(400):
        copy.step()
    found = [(c["interval"], c["node_detector"], c["emitted"]) for c in copied if c["event"] == "credit"]
    nulls = [
        (t, "body 1", None) for t in (75, 123, 171, 219, 267)
    ]  # the taker's closes every 48 from its window's opening at 28
    assert found == [
        (10, "body 0", "pulse"),
        (48, "body 0", None),
        *nulls,
        (315, "body 0", None),
        (315, "body 1", None),
    ]
    taken = [
        c for c in copied if c["event"] == "credit" and c["absorbed"]
    ]  # the taking click, the source named (the pair over three Nodes, 2026-10-21; over two Nodes the copy's emission fell at 83 and nothing took to 400)
    assert [
        (c["interval"], c["node_detector"], c["absorbed"], c["source"], c["recoil"]) for c in taken
    ] == [(267, "body 1", "pulse", "body 0", [51680, 0, 0])]
    print(
        f"Part G (5g): resonant.json green over {board.world.intervals}, atom 0 gives at {credits[0]['interval']}; the read at 191 refused by name; the content copy's emission at 10, the take at 267 with atom 0 named as the source"
    )
