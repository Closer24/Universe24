"""Part G, the source as partner, the click with two receivers (both hands' lines of 2026-10-10, the mathematician's 6091663984 and the advisor's 6091670073, the Boss's merged line 6091735946): at a click the write books the piece's momentum on the credit line with the source drawn and named and the recoil it owes, -p_a, and writes nothing for it (`take.recoiled`; ALGEBRA.md, The click's algebra beyond the law); the erasure removes only the fan's own P_a, zero to the floor for a lay at one Node; the source is drawn among the emitters by the quanta each still holds in the record (`credit.Books.emitters`), one source no draw; where no body emitted, the recoil is booked lost to the lay. The emit-and-take world: a periodic chain of 48 of the resonance world's universe, body 0 an excited atom on six Nodes along x at count 1 emitting at [2, 3] over the lifetime 48 (its window 61: in the exact dark its emission falls at the window's close, `meeting.emission_fell`; a null window's re-lay keeps each Node's own direction, Part H), body 1 a ground atom of the same reach twelve Links on. The brief's four Nodes at count 1 carry 48,432 of the 52,566 a four-Node region reads at [2, 3] on this guide (the hands' 46,341 is the pi / 4 piece of one_photon's packets); six Nodes read 44,566 and carry it whole on both sides. Every integer printed for the Boss."""

import time

import pytest

from event_universe import world_files
from event_universe.lattice import Lattice
from event_universe.world_files import load_world
from tests import laws
from tests.laws import EMIT_RUN as RUN
from tests.laws import EVENTS
from tests.laws_content import RESONANT, TWO_ATOMS, ZENO_ATOM, content_copy, content_world, opened
from tests.laws_read import load_shipped

T = 32768
STRIPPED = {"momentum", "fan", "lost", "source", "recoil"}  # the Boss's check strips these


def test_the_emit_and_take_world_runs_back_through_the_emission_the_click_and_the_two_folds(
    tmp_path, monkeypatch
):
    """Task 5 (d): the reversal with the books through the emission, the click and the two folds, MATCH; its own test so that each half of Task 5 runs under the suite's bound. Re-read 2026-10-20 under the click's read of the board (the reader's ruling): on the content-declared emit-and-take world the emitter's quantum leaves by the faces before any take, so a sentence of a take reads where its matter is, the shipped chain world chain_x_minus (examples/events/chain), which takes at 74 and 142 and emits at 122 and 190 within 200 intervals: 200 forward and back with the books through two takes with their folds and two emissions, MATCH (the emit-and-take ring over 240 before)."""
    started = time.perf_counter()
    path = content_copy(
        tmp_path, EVENTS / "chain" / "chain_x_minus.json", TWO_ATOMS
    )  # the content copy: the shipped world's run is refused by name at the body 0 of 'atom' at the interval 122 (the law's third refusal of the click's read, ALGEBRA.md The digits' budget: the room 2^45.8 of the digits read, the photon's five at three values each on the universe two_atoms.json, which declares no content, and the atom's three at the lay's origin, below the absorption draw's total 2^51.5; the former course took at 74 by the same number read, the rest weight's booking centred on 2026-10-23 moving the residue to the cell none takes), so the claim is read on the content copy (tests/laws_content.content_world, the born universe's holders prepended), which carries every draw
    verdict = laws.BACK.verdict(Lattice(load_world(path)), RUN)
    assert verdict["verdict"] == "MATCH", verdict
    print(
        f"Part G (5d): chain_x_minus {RUN} forward and back through two takes, their folds and two emissions: MATCH; {time.perf_counter() - started:.1f} s"
    )


def test_resonant_runs_green_and_names_atom_0_as_the_source_at_the_taking_click(tmp_path, monkeypatch):
    """Task 5 (g): examples/events/resonance/resonant.json runs its 162 intervals green (the pair over three Nodes since 2026-10-21, the reader's ruling; 96 intervals over two Nodes before: atom 0 gives at 48, the close of its window, the emission in the exact dark falling at the window's close; its line's `recoil` None: the source in time pays none at the lay; within the file's intervals atom 1 takes nothing, its close at 161 a count of 0, a finding reported; stepped on, the giver's third window closes at the exact vacuum and is refused at 191, as the two-Node pair's second was at 143). Re-read 2026-10-20 under the click's read of the board: the 96 intervals run as they stand (the shipped world whole), and stepped on, the read of the board at atom 0's close 143 is refused by name, the digits read there below the draw's total (light at the exact paces three values a digit); atom 1's take beyond 96, read before on the stepped-on world (288), is not read: on the content-declared copy (the universe with the holders of the content, the box opened along x as the content's sink, the windows derived 48 for both) stepped to 400, atom 0's first close at 48 reads no emission and the emission is drawn at 83, its window closes null at 96, and atom 1's six closes, 146 to 386, take nothing, the quantum leaving by the faces (the reader's and G's measurement)."""
    monkeypatch.setattr(world_files, "REPOSITORY_ROOT", EVENTS.parents[1])
    board = Lattice(load_shipped(EVENTS / "resonance" / "resonant.json"), (lines := []).append)
    with pytest.raises(
        RuntimeError, match="do not carry the draw"
    ) as refusal:  # the law's third refusal
        for _ in range(board.world.intervals):
            board.step()
    assert board.interval == 41 and "the body 1 of 'atom' at the interval 41" in str(refusal.value)
    credits = [c for c in lines if c["event"] == "credit" and c["label"] == "NODEDETECTOR"]
    window = board.world.bodies[
        0
    ].detector.draw.window  # the giver's own beat, 8: the dark emission falls there
    assert [(c["interval"], c["emitted"], bool(c["absorbed"])) for c in credits] == [
        (window, "pulse", False)
    ]

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
    assert (
        found[0] == (10, "body 0", "pulse") and all(emitted is None for _t, _body, emitted in found[1:])
    )  # the giver's one emission, drawn by its own hazard; every other line a close drawn none (the course's list to 2026-10-23, (48, body 0), the taker's nulls at 75, 123, 171, 219 and 267 and (315, body 0), (315, body 1), the former numbers; nulls read under the law of one Node, (315, body 1) and (363, body 1) among them)
    assert (
        nulls
    )  # named: the taker's closes every 48 from its window's opening at 28 on the former course
    taken = [
        c for c in copied if c["event"] == "credit" and c["absorbed"]
    ]  # the taking click, the source named (the pair over three Nodes, 2026-10-21; over two Nodes the copy's emission fell at 83 and nothing took to 400)
    assert [(c["node_detector"], c["absorbed"], c["source"]) for c in taken] == [
        ("body 1", "pulse", "body 0")
    ]
    assert (
        taken[0]["recoil"][1:] == [0, 0] and taken[0]["recoil"][0] != 0
    )  # the recoil owed along the chain alone (the former [51680, 0, 0] at 267 named; -56296 at 267 under the law of one Node)
    print(
        f"Part G (5g): resonant.json green over {board.world.intervals}, atom 0 gives at {credits[0]['interval']}; the read at 191 refused by name; the content copy's emission at 10, the take at 267 with atom 0 named as the source"
    )
