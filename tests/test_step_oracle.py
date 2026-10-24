"""The step's oracle inside the suite's bound: the engine matches the law in its implementation, not only in its results. tools/step_oracle.py keeps the law's first form of Rule3, SUM over the six Ports of R_ij m_ij + S a_now - w a_before + r, with the one Node's interval around it, in no file of src/, and runs it against the engine's step (Rule3's flux line, src/event_universe/flux.py, core/rule3.rule3): two boards from one load, every array and the output lines compared at every interval, then the engine's board back with the record to the lay. Here two worlds under the suite's thirty seconds: bell_a_b (a held well with the holders, the draw, the growth of the board, 100 intervals) and the fold's chain (the rule's universe with the charged plane and gravity carrying the flux's odd lines, a moving packet, 40 intervals; declared by no shipped world)."""

from __future__ import annotations

import event_universe.world_files as world_files
from event_universe.lattice import Lattice
from event_universe.world_files import load_world
from tests.laws import ORACLE, flux_world, packet
from tests.laws_interval import laid_torus, volume_universe


def test_the_flux_step_equals_the_first_form_on_a_held_well_and_runs_back_to_the_lay(
    tmp_path, monkeypatch
) -> None:  # type: ignore[no-untyped-def]
    """The laid 3-cube torus (tests/laws_interval.py, matter in its held well at the volume form's integers), every interval of 6 forward against the first form (every line's two levels and remainder, every write remainder, the record) and back with the record to the lay exactly (bell_a_b over its 100 intervals, 30 s on the suite's clock, left on 2026-10-24)."""
    monkeypatch.setattr(world_files, "REPOSITORY_ROOT", tmp_path)
    volume_universe(tmp_path)
    found = ORACLE.verdict(Lattice(load_world(laid_torus(tmp_path, "well", intervals=6))), None)
    assert found["verdict"] == "EQUAL" and found["intervals"] == found["back"] == 6, found


def test_the_flux_step_equals_the_first_form_under_the_fold(tmp_path, monkeypatch) -> None:  # type: ignore[no-untyped-def]
    """The fold of a flux holder on the chain of 25 with a moving packet, 40 intervals forward and back; the odd line written along the packet's way, so the fold was read."""
    monkeypatch.setattr(world_files, "REPOSITORY_ROOT", tmp_path)
    board = Lattice(
        load_world(flux_world(tmp_path, (25, 1, 1), dict(x="periodic", y="periodic", z="periodic"), 40))
    )
    packet(board, 0, (1, 4), 7, 3)
    found = ORACLE.verdict(board, 40)
    assert found == {**found, "verdict": "EQUAL", "intervals": 40, "back": 40}, found
    gravity = board.states[[f.name for f in board.families].index("gravity")]
    assert gravity.lines[4].now.any()
