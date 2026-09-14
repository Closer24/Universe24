"""Two-wing CHSH acceptance for the native register program on the canonical runner."""

import importlib.util
import json
from fractions import Fraction
from pathlib import Path

from event_universe.configuration_validation import validate_configuration

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "bell_chsh_experiment", ROOT / "examples/quantum/bell_chsh.py"
)
EXPERIMENT = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(EXPERIMENT)


def test_analytic_settings_give_chsh_14_over_5_and_a_dephased_control_below_two():
    bell = EXPERIMENT.analytic("bell")
    assert bell["correlations"] == {"a0b0": "3/5", "a0b1": "3/5", "a1b0": "4/5", "a1b1": "-4/5"}
    assert bell["chsh"] == "14/5" and bell["violates_local_bound"]
    assert bell["joint_probabilities"]["a1b1"] == {
        "00": "1/20",
        "01": "9/20",
        "10": "9/20",
        "11": "1/20",
    }
    control = EXPERIMENT.analytic("dephased")
    assert control["correlations"] == {"a0b0": "3/5", "a0b1": "3/5", "a1b0": "0", "a1b1": "0"}
    assert control["chsh"] == "6/5" and not control["violates_local_bound"]
    # Every setting is a valid two-outcome instrument: (sI + O)^2 + (sI - O)^2 = 4 s^2 I.
    for observable, scale in (*EXPERIMENT.ALICE_SETTINGS.values(), *EXPERIMENT.BOB_SETTINGS.values()):
        plus, minus = EXPERIMENT.instrument(observable, scale)
        total = [
            [
                sum(plus[k][i] * plus[k][j] + minus[k][i] * minus[k][j] for k in range(2))
                for j in range(2)
            ]
            for i in range(2)
        ]
        assert total == [[4 * scale * scale, 0], [0, 4 * scale * scale]]


def test_generated_inputs_are_valid_and_keep_the_wings_nine_links_apart():
    template = json.loads(EXPERIMENT.TEMPLATE.read_text(encoding="utf-8"))
    assert validate_configuration(json.dumps(template).encode()).valid
    assert EXPERIMENT.wing_link_distance(template) == 9
    for a, b in EXPERIMENT.SETTINGS:
        for environment in ("bell", "dephased"):
            raw = EXPERIMENT.configuration(a, b, tickets=[0, 0], environment=environment)
            assert raw["event_program"]["model"] == "local-quantum-events-v2"
            ticks = [layer["tick"] for layer in raw["event_program"]["layers"]]
            assert ticks == sorted(ticks) and ticks[-1] < EXPERIMENT.MEASUREMENT_TICK < raw["ticks"]
            assert ("channel" in json.dumps(raw)) == (environment == "dephased")
            assert validate_configuration(json.dumps(raw).encode()).valid


def test_two_wing_runs_reproduce_the_exact_chsh_value_and_write_classical_outcomes(tmp_path):
    result = EXPERIMENT.run_experiment(tmp_path / "experiment", trials=5)
    exact = result["exact"]
    assert exact["chsh"] == "14/5" and exact["violates_local_bound"]
    assert exact["correlations"] == result["analytic"]["correlations"]
    assert exact["alice_weights_for_every_bob_setting"] == [[4, 4]]
    assert exact["bob_marginal_for_every_alice_setting"] == ["1/2", "1/2"]
    assert exact["settings"]["a1b0"]["bob_weights_given_alice"] == [[360, 40], [40, 360]]
    assert exact["settings"]["a1b1"]["bob_weights_given_alice"] == [[40, 360], [360, 40]]
    control = result["exact_control"]
    assert control["chsh"] == "6/5" and not control["violates_local_bound"]
    assert control["settings"]["a1b0"]["bob_weights_given_alice"] == [[200, 200], [200, 200]]
    for table in (exact, control):
        for row in table["settings"].values():
            for case in row["cases"]:
                assert case["alice"]["tick"] == case["bob"]["tick"] == EXPERIMENT.MEASUREMENT_TICK
                assert case["random_draws"] == 2 and case["model"] == "local-quantum-events-v2"
                assert case["classical_outcome_codes"] == {
                    "Detector A": case["alice"]["outcome"] + 1,
                    "Detector B": case["bob"]["outcome"] + 1,
                }
    sampled = result["sampled"]
    assert sampled["trials_per_setting"] == 5
    for row in sampled["settings"].values():
        assert sum(row["counts"].values()) == 5 and len(row["outcomes"]) == 5
    assert abs(Fraction(sampled["chsh"])) <= 4
    assert result["wing_link_distance"] == 9 and result["measurement_tick"] == 8
    assert not list((tmp_path / "experiment").rglob("*.html"))
