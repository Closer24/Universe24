"""De Broglie probe: the beam's advance follows its momentum and the worlds close."""

import importlib.util
from pathlib import Path

from event_universe.initialization import parse_initial_state

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "de_broglie_probe", ROOT / "examples/de-broglie/run_experiments.py"
)
PROBE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(PROBE)


def test_the_probe_composes_for_every_momentum_and_closes_on_a_short_run():
    headings = PROBE.cone_headings(32, PROBE.HEADING_SCALE)
    for momentum in PROBE.MOMENTA:
        initial = parse_initial_state(PROBE.document(momentum, headings, ticks=4))
        rule = initial.emissions[0]
        assert rule.advance is not None and rule.advance_denominator == PROBE.ADVANCE_DENOMINATOR
        assert initial.emissions[1].phase_carried
    assert parse_initial_state(PROBE.document(16, headings, ticks=4, phased=False))
    result = PROBE.run(PROBE.document(64, headings, ticks=8))
    assert result["matter_closed"]
