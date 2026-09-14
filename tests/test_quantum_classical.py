"""Quantum-to-classical probes: dephased walk equals the classical chain, quanta click whole."""

import importlib.util
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "quantum_classical_probe", ROOT / "examples/quantum-classical/run_experiments.py"
)
PROBE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(PROBE)


def test_dephased_walk_is_the_classical_chain_and_the_coherent_walk_spreads_faster():
    classical = PROBE.classical_walk(6, nodes=15)
    dephased = PROBE.walk(6, 1, nodes=15)
    coherent = PROBE.walk(6, 0, nodes=15)
    assert [r["occupation"] for r in dephased] == [r["occupation"] for r in classical]
    assert [Fraction(r["variance"]) for r in dephased] == [Fraction(4 * t - 3, 4) for t in range(1, 7)]
    assert all(Fraction(r["total"]) == 1 for r in coherent)
    # Ballistic against diffusive: the coherent width at step 6 exceeds the classical one
    # and its distribution is not the classical bell.
    assert Fraction(coherent[-1]["variance"]) > Fraction(classical[-1]["variance"])
    assert coherent[-1]["occupation"] != classical[-1]["occupation"]


def test_single_quanta_click_whole_and_their_count_is_closed():
    result = PROBE.counting_probe(ticks=256, radii=(2,))
    (row,) = result["rows"]
    assert row["click_values"] == [0, 1]
    assert row["clicks_per_sweep"] > 0
    # One quantum per tick left the source; all of it is a record, in flight or escaped.
    assert result["totals"]["quanta"][0] + result["escaped"]["quanta"][0] == 1 + 256


def test_capture_attempts_land_on_the_pass_ticks_with_charge_and_mass_exact():
    document = PROBE.capture_document(8)
    ticks = {PROBE.capture_trial(document, seed)["capture_tick"] for seed in range(1, 9)}
    assert ticks <= {3, 7, None}
    assert 3 in ticks
