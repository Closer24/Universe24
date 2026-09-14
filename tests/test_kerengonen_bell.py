"""Kerengonen Bell test: a local phased field stays inside the CHSH bound of 2."""

import importlib.util
from fractions import Fraction
from pathlib import Path

from event_universe.initialization import parse_initial_state


def load_probe():
    path = Path(__file__).resolve().parents[1] / "examples/kerengonen-bell/run_experiments.py"
    spec = importlib.util.spec_from_file_location("kerengonen_bell", path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_each_wing_absorbs_the_table_cosine_share_of_the_source_ray():
    probe = load_probe()
    for hidden, expected in (
        (0, Fraction(1)),
        (90, Fraction(1, 2)),
        (180, Fraction(0)),
        (53, Fraction(205, 256)),
    ):
        run = probe.run_share(probe.document(hidden, 0, 0, ticks=8))
        assert run["quanta_closed"]
        assert run["share"] == [expected, expected]
        # The lamp ray is taken at the same share: the analyzer reads both by momentum.
        assert run["absorbed_lamp"] == run["absorbed_source"]
    audited = probe.run_share(probe.document(0, 0, 0, ticks=8, audit=True))
    assert audited["audit"] == "passed" and audited["share"] == [1, 1]


def test_the_share_rule_reproduces_the_local_model_exactly():
    probe = load_probe()
    share = probe.share_correlations(90, ticks=8)
    assert share["closed"] and share["worlds"] == 16
    for pair in probe.PAIRS:
        expected = probe.model_correlation(probe.ALICE[pair[0]], probe.BOB[pair[1]], 90)
        assert share["correlations"][pair] == expected
    assert share["S"] == probe.chsh(
        {
            pair: probe.model_correlation(probe.ALICE[pair[0]], probe.BOB[pair[1]], 90)
            for pair in probe.PAIRS
        }
    )


def test_the_local_model_stays_inside_the_bound_and_the_quantum_owner_does_not():
    probe = load_probe()
    full = {
        pair: probe.model_correlation(probe.ALICE[pair[0]], probe.BOB[pair[1]], 1)
        for pair in probe.PAIRS
    }
    coarse = {
        pair: probe.model_correlation(probe.ALICE[pair[0]], probe.BOB[pair[1]], probe.SHARE_GRID)
        for pair in probe.PAIRS
    }
    assert abs(probe.chsh(full) - Fraction(7, 5)) < Fraction(1, 100)
    assert abs(probe.chsh(coarse) - Fraction(7, 5)) < Fraction(1, 100)
    assert probe.chsh(probe.QUANTUM_OWNER) == Fraction(14, 5) > 2
    plain = probe.plain_correlations(ticks=8)
    assert plain["closed"] and plain["S"] == 2
    assert all(value == 1 for value in plain["correlations"].values())


def test_lottery_clicks_are_whole_single_quanta_and_stay_inside_the_bound():
    probe = load_probe()
    lottery = probe.lottery_correlations(120, ticks=24)
    assert lottery["closed"] and lottery["worlds"] == 12 and lottery["pairs_per_setting"] == 63
    assert all(-1 <= value <= 1 for value in lottery["correlations"].values())
    assert lottery["S"] <= 2


def test_the_probe_document_is_valid_configuration():
    probe = load_probe()
    parse_initial_state(probe.document(53, 90, 307))
    parse_initial_state(probe.document(0, 0, 0, per_ray=1, capture_seed=3))
    parse_initial_state(probe.document(0, 0, 0, phase_steps=0))
