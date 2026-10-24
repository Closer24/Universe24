"""The step's oracle inside the suite's bound (the owner's word of 2026-10-16: the engine matches the law in its implementation and not only in its results): tools/step_oracle.py keeps the law's first form of Rule3, SUM over the six Ports of R_ij m_ij + S a_now - w a_before + r, with the one Node's interval around it, in no file of src/, and runs it against the engine's step (Rule3's flux line, src/event_universe/flux.py, core/rule3.rule3): two boards from one load, every array and the output lines compared at every interval, then the engine's board back to the seed. On the bare 3-cube torus of the one universe file over the 28 intervals before the births."""

from __future__ import annotations

from pathlib import Path

import pytest

import event_universe.world_files as world_files
from event_universe import seed
from event_universe.lattice import Lattice
from event_universe.world_files import load_world
from tests.laws import ORACLE
from tests.laws_universe import CUBE, bare_torus, uniform_sea

INTERVALS = 23  # the intervals before the uniform sea's births at 24 on the tests' small universe (the sea laid by name, 2026-10-24: the oracle's first form is the step's and not the close's births, as on main, whose 28 intervals ended before the births at 30; the hole seed's draw births from its first intervals)


def test_the_engines_step_is_the_laws_first_form_on_the_bare_torus(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """EQUAL over 23 intervals forward and 23 back: the oracle's arrays and output lines the engine's at every interval, the seed recovered."""
    monkeypatch.setattr(world_files, "REPOSITORY_ROOT", tmp_path)
    monkeypatch.setattr(
        seed, "uniform_seed", uniform_sea
    )  # the uniform sea, the law's seed to 2026-10-24, by name
    board = Lattice(load_world(bare_torus(tmp_path, CUBE, INTERVALS)))
    found = ORACLE.verdict(board, INTERVALS)
    assert found == {**found, "verdict": "EQUAL", "intervals": INTERVALS, "back": INTERVALS}
