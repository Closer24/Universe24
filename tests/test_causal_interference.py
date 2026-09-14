"""Two-arm interference and which-path acceptance for the causal source candidate."""

import importlib.util
from fractions import Fraction
from pathlib import Path

from event_universe.configuration_validation import validate_configuration

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "causal_interference_experiment", ROOT / "examples/quantum/causal_interference.py"
)
EXPERIMENT = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(EXPERIMENT)


def test_analytic_port_weights_follow_the_configured_mixer_and_phase():
    assert EXPERIMENT.analytic("0")["output_port_weights"] == [625, 0]
    assert EXPERIMENT.analytic("pi/2")["output_port_weights"] == [337, 288]
    assert EXPERIMENT.analytic("pi")["output_port_weights"] == [49, 576]
    assert EXPERIMENT.analytic("3pi/2")["output_port_weights"] == [337, 288]
    assert EXPERIMENT.analytic("pi")["capture_probability"] == "576/625"


def test_generated_inputs_are_valid_and_keep_the_profile():
    for phase in EXPERIMENT.PHASES:
        for which_path in (False, True):
            raw = EXPERIMENT.configuration(phase, which_path=which_path, tickets=[0])
            assert raw["event_program"]["model"] == "causal-contact-fields-v1"
            assert len(raw["event_program"]["domains"][0]["phases"]) == 16
            assert validate_configuration(__import__("json").dumps(raw).encode()).valid


def test_interference_is_visible_at_the_output_and_removed_by_an_arm_detector(tmp_path):
    result = EXPERIMENT.run_experiment(tmp_path / "experiment")
    measured = {row["phase"]: row["measured_output_weights"] for row in result["interference"]}
    assert measured == {"0": [1, 0], "pi/2": [337, 288], "pi": [49, 576], "3pi/2": [337, 288]}
    for row in result["interference"]:
        steady = Fraction(row["measured_source_emission_after_recombination"])
        predicted = Fraction(row["analytic"]["source_emission_after_recombination"])
        assert abs(steady - predicted) < Fraction(1, 6)
    assert result["localized_capture_at_output"]["captures"] == [{"tick": 7, "x": 3}]
    assert {row["arm_ticket"] for row in result["which_path"]} == {"null", "capture"}
    for row in result["which_path"]:
        assert row["arm_decision_weights"] == [9, 16]
        if row["arm_ticket"] == "null":
            assert row["source_emission_after_arm_null"] == 9
            assert row["captures"] == []
        else:
            assert row["captures"] == [{"tick": 1, "x": 2}]
    assert result["retarded_source_fraction_after_arm_null"] == "9/25"
    assert not list((tmp_path / "experiment").rglob("*.html"))
