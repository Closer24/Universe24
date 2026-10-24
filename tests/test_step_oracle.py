"""The step's oracle inside the suite's bound: the engine matches the law in its implementation, not only in its results. tools/step_oracle.py keeps the law's first form of Rule3, SUM over the six Ports of R_ij m_ij + S a_now - w a_before + r, with the one Node's interval around it, in no file of src/, and runs it against the engine's step (Rule3's flux line, src/event_universe/flux.py, core/rule3.rule3): two boards from one load, every array and the output lines compared at every interval, then the engine's board back with the record to the lay. Here two worlds under the suite's thirty seconds: bell_a_b (a held well with the holders, the draw, the growth of the board, 100 intervals) and the fold's chain (the rule's universe with the charged plane and gravity carrying the flux's odd lines, a moving packet, 40 intervals; declared by no shipped world)."""

from __future__ import annotations

from pathlib import Path

import event_universe.world_files as world_files
from event_universe.lattice import Lattice
from tests.laws import ORACLE, flux_world, packet

ROOT = Path(__file__).resolve().parents[1]


def test_the_flux_step_equals_the_first_form_under_the_fold(tmp_path, monkeypatch) -> None:  # type: ignore[no-untyped-def]
    """The fold of a flux holder on the chain of 25 with a moving packet, 16 intervals forward and back, the engine's step and the first form equal at every interval and the run back to the lay; the odd line written along the packet's way, so the fold was read. The intervals: at 17 the seed's light meets itself at the Node 8 and the board births a pair there (the light's level 0 where the first form, which knows no click, keeps 3258), so the comparison stops at 16 (2026-10-24, the holders derived: the tests' universe without the binding holder and without gravity's rest 60). On the former tests' universe the sign holder's levels under the universal charge passed the content bound of this chain at the interval 35 (the level 6267 against A = 6178) and the run of 40 was refused by the law's own sentence, the refusal the assertion of the morning of 2026-10-24, kept by name."""
    monkeypatch.setattr(world_files, "REPOSITORY_ROOT", tmp_path)
    board = Lattice(flux_world(tmp_path, (25, 1, 1), 16))
    packet(board, 0, (1, 4), 7, 3)
    found = ORACLE.verdict(board, 16)
    assert found == {**found, "verdict": "EQUAL", "intervals": 16, "back": 16}, found
    gravity = board.states[[f.name for f in board.families].index("gravity")]
    assert gravity.lines[4].now.any()  # the x odd line written along the packet's way
