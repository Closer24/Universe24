"""Mirror probe: the standing wave's period follows the advance and the world closes."""

import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "kerengonen_mirror_probe", ROOT / "examples/kerengonen-mirror/run_experiments.py"
)
PROBE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(PROBE)


def test_the_standing_wave_period_is_half_the_wavelength_and_the_world_closes():
    for advance in (4, 8):
        standing = PROBE.run(PROBE.document(advance, ticks=72))
        assert standing["quanta_closed"]
        assert PROBE.period(standing["readings"]) == PROBE.PHASE_STEPS // (2 * advance)
        assert standing["mirror_momentum"][0] > 0
    free = PROBE.run(PROBE.document(4, ticks=40, mirror=False))
    assert (
        free["quanta_closed"]
        and PROBE.period(free["readings"]) in (None, 1)
        or all(value == 8 for value in free["readings"].values())
    )
