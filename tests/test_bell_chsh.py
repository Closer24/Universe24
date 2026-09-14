"""Two-wing CHSH acceptance for the native register program on the canonical runner."""

import importlib.util
import json
from fractions import Fraction
from pathlib import Path

import pytest

from event_universe.configuration_validation import validate_configuration

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "bell_chsh_experiment", ROOT / "examples/quantum/bell_chsh.py"
)
EXPERIMENT = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(EXPERIMENT)
VIEW_SPEC = importlib.util.spec_from_file_location(
    "bell_chsh_view", ROOT / "examples/quantum/bell_chsh_view.py"
)
VIEW = importlib.util.module_from_spec(VIEW_SPEC)
VIEW_SPEC.loader.exec_module(VIEW)


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


def test_view_reads_recorded_gates_and_positions_without_advancing_a_world(tmp_path):
    raw = EXPERIMENT.configuration("a1", "b0", tickets=[0, 0])
    case = EXPERIMENT.run_case("bell_a1b0_alice0", raw, tmp_path)
    run = VIEW._load_run(tmp_path / "bell_a1b0_alice0")
    carriers = VIEW._carriers_by_tick(run)
    assert carriers[1][0] == {4} and carriers[2][0] == {4, 5}
    assert carriers[3][0] == {4, 5} and carriers[7][0] == {0, 9}
    assert "Controlled-NOT" in carriers[2][1] and "SWAP" in carriers[7][1]
    assert run["positions"][0] == {"Detector A": [0, 1, 1], "Detector B": [25, 1, 1]}
    assert run["positions"][8] == {"Detector A": [8, 1, 1], "Detector B": [17, 1, 1]}
    assert run["records"][0]["outcome"] == case["alice"]["outcome"]
    assert run["codes"] == case["classical_outcome_codes"]
    dephased = EXPERIMENT.configuration("a0", "b0", tickets=[0, 0], environment="dephased")
    EXPERIMENT.run_case("dephased_a0b0_alice0", dephased, tmp_path)
    control = VIEW._carriers_by_tick(VIEW._load_run(tmp_path / "dephased_a0b0_alice0"))
    assert "Dephasing" in control[3][1] and control[3][0] == {4, 5}


@pytest.mark.visualization
def test_view_renders_one_animation_and_four_stills(tmp_path):
    pytest.importorskip("matplotlib")
    pytest.importorskip("PIL")
    from PIL import Image

    output = tmp_path / "experiment"
    result = EXPERIMENT.run_experiment(output, trials=1)
    (output / "summary.json").write_text(json.dumps(result), encoding="utf-8")
    saved = VIEW.render_experiment(output, tmp_path / "view")
    assert [path.name for path in saved] == [
        "bell_chsh.gif",
        "bell_chsh_start.png",
        "bell_chsh_pair.png",
        "bell_chsh_measured.png",
        "bell_chsh_result.png",
    ]
    assert all(path.stat().st_size for path in saved)
    animation = Image.open(saved[0])
    assert animation.n_frames >= 4 * 10 // 2 and animation.size == (1200, 560)
