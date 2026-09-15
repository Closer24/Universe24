"""Bell's test on the ray: Malus's law at each detector, S below the local bound, closed."""

import importlib.util
from pathlib import Path

import pytest

from event_universe.initialization import parse_initial_state

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "bell_chsh_probe", ROOT / "examples/bell-chsh/run_experiments.py"
)
PROBE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(PROBE)


def test_aligned_phases_land_deterministically_and_the_world_closes():
    for seed in (1, 2, 3):
        aligned = PROBE.outcomes(PROBE.document(0, 0, 0, seed))
        opposite = PROBE.outcomes(PROBE.document(PROBE.HALF_TURN, 0, 0, seed))
        # Alice's ray at the reference phase is taken surely at her plus detector; Bob's
        # ray, a half turn away from his, walks on to his minus detector; and the reverse.
        assert (aligned["alice"], aligned["bob"]) == (1, -1) and aligned["closed"]
        assert (opposite["alice"], opposite["bob"]) == (-1, 1) and opposite["closed"]


def test_one_seed_over_every_hidden_phase_stays_below_the_local_bound():
    result = PROBE.chsh(seeds=1)
    assert result["closed"]
    assert result["quantum_S"] == 2.8284 and result["predicted_S"] == 1.4144
    # One capture seed over the 64 hidden phases: 256 pairs, every one landed.
    assert all(
        value["missing"] == 0 and value["pairs"] == 64 for value in result["correlations"].values()
    )
    assert result["S"] == 1.5001 and result["same_setting_E"] == -0.5312
    assert result["S"] < result["local_bound"] < result["quantum_S"]


def test_capture_salt_is_validated():
    raw = PROBE.document(0, 0, 0, 1)
    raw["spatial_couplings"][0]["capture_salt"] = PROBE.PHASE_STEPS * 0 + 1073741789
    with pytest.raises(ValueError, match="ticket modulus"):
        parse_initial_state(raw)
    raw = PROBE.document(0, 0, 0, 1)
    raw["spatial_fields"][0]["kerengonen"] = {"phase_steps": PROBE.PHASE_STEPS, "phase_advance": 0}
    with pytest.raises(ValueError, match="requires the lottery"):
        parse_initial_state(raw)


def test_deterministic_hidden_variables_reach_the_bound_and_stop_there():
    result = PROBE.chsh(seeds=1, capture="threshold")
    assert result["closed"] and result["capture"] == "threshold"
    assert [value["E"] for value in result["correlations"].values()] == [-0.5, 0.5, -0.5, -0.5]
    assert [value["predicted_E"] for value in result["correlations"].values()] == [-0.5, 0.5, -0.5, -0.5]
    assert result["S"] == 2.0 == result["local_bound"] < result["quantum_S"]
    assert result["same_setting_E"] == -0.9375


def test_bonded_pairs_break_the_local_bound_with_the_singlet_law():
    for seed in (1, 2, 3):
        same = PROBE.outcomes(PROBE.document(0, 0, 0, seed, capture="bond"))
        opposite = PROBE.outcomes(PROBE.document(0, 0, PROBE.HALF_TURN, seed, capture="bond"))
        # Equal settings never agree, settings a half turn apart always do; both closed.
        assert same["alice"] == -same["bob"] and same["closed"]
        assert opposite["alice"] == opposite["bob"] and opposite["closed"]
    result = PROBE.chsh(seeds=1, capture="bond")
    assert result["closed"] and result["predicted_S"] == 2.8284
    assert all(value["missing"] == 0 for value in result["correlations"].values())
    # One number per bonded pair, fixed by the registry seed and the pair's birth code;
    # the second end reads the first end's number.
    assert [value["E"] for value in result["correlations"].values()] == [
        -0.6562,
        0.8125,
        -0.6562,
        -0.6562,
    ]
    assert result["S"] == 2.7811 and result["same_setting_E"] == -1.0
    assert result["S"] > result["local_bound"]


def test_both_rays_carry_the_code_of_their_birth_node_and_tick():
    from event_universe import Simulation
    from event_universe.core.spatial_state import origin_bond

    raw = PROBE.document(0, 0, 0, 1, capture="bond")
    initial = parse_initial_state(raw)
    assert initial.emissions[0].bond_origin and initial.emissions[1].bond_origin
    world = Simulation(initial)
    world.step()
    bonds = {
        ray.bond for node in world.inventory_view().nodes for ray in (node.rays[0] if node.rays else ())
    }
    # One pair, one code: the source Node and the tick of the emission.
    assert bonds == {origin_bond((PROBE.CENTER, 1, 1), (PROBE.WIDTH, 3, 3), 0)}
    assert origin_bond((0, 0, 0), (13, 3, 3), 0) == 1
    assert origin_bond((0, 0, 0), (13, 3, 3), 5) == 6
    assert origin_bond((1, 0, 0), (13, 3, 3), 0) != origin_bond((0, 1, 0), (13, 3, 3), 0)


def test_bonds_are_validated():
    raw = PROBE.document(0, 0, 0, 1, capture="bond")
    raw["spatial_fields"][0]["bond"]["seed"] = 1073741789
    with pytest.raises(ValueError, match="ticket modulus"):
        parse_initial_state(raw)
    raw = PROBE.document(0, 0, 0, 1, capture="bond")
    del raw["spatial_fields"][0]["bond"]
    with pytest.raises(ValueError, match="bond_field requires"):
        parse_initial_state(raw)
    raw = PROBE.document(0, 0, 0, 1, capture="bond")
    del raw["spatial_fields"][0]["bond"]
    for rule in raw["emissions"]:
        rule.pop("bond_field", None)
    with pytest.raises(ValueError, match="bond_setting requires"):
        parse_initial_state(raw)
    raw = PROBE.document(0, 0, 0, 1, capture="bond")
    del raw["spatial_fields"][0]["kerengonen"]
    with pytest.raises(ValueError, match="requires a kerengonen"):
        parse_initial_state(raw)
    raw = PROBE.document(0, 0, 0, 1, capture="bond")
    raw["emissions"][0]["bond_field"] = "momentum"
    with pytest.raises(ValueError, match="scalar owned"):
        parse_initial_state(raw)


def test_an_external_number_source_is_invisible_when_uniform_and_a_signal_when_biased():
    # One seed per slot. A uniform outside source gives the same physics: S near the
    # quantum value and plus rates that do not move with the other end's setting.
    uniform = PROBE.chsh(seeds=1, capture="bond", source="uniform")
    assert uniform["closed"] and uniform["S"] == 2.625 and uniform["same_setting_E"] == -1.0
    assert uniform["alice_rate_shift"] == 0.0 and uniform["bob_rate_shift"] < 0.1
    # A biased source keeps S but moves Bob's plus rate with Alice's setting: a signal.
    biased = PROBE.chsh(seeds=1, capture="bond", source="biased")
    assert biased["closed"] and biased["S"] == 2.625 and biased["same_setting_E"] == -1.0
    assert all(value["alice_plus_rate"] == 1.0 for value in biased["correlations"].values())
    assert biased["correlations"]["a,b2"]["bob_plus_rate"] == 0.875
    assert biased["correlations"]["a2,b2"]["bob_plus_rate"] == 0.1875
    assert biased["alice_rate_shift"] == 0.0 and biased["bob_rate_shift"] == 0.6875
    assert PROBE.external_number(1, "sequence") is None
    assert PROBE.external_number(1, "biased") < PROBE.TICKET_MODULUS // 2


def test_the_bond_stream_is_validated():
    raw = PROBE.document(0, 0, 0, 1, capture="bond", stream=5)
    parse_initial_state(raw)
    raw["spatial_fields"][0]["bond"]["stream"] = []
    with pytest.raises(ValueError, match="non-empty list"):
        parse_initial_state(raw)
    raw["spatial_fields"][0]["bond"]["stream"] = [PROBE.TICKET_MODULUS]
    with pytest.raises(ValueError, match="below the ticket modulus"):
        parse_initial_state(raw)
    raw["spatial_fields"][0]["bond"]["stream"] = [1] * 4097
    with pytest.raises(ValueError, match="at most 4096"):
        parse_initial_state(raw)


def test_the_bonded_value_is_the_registry_law_pair_by_pair_with_its_standard_error():
    from fractions import Fraction

    # The registry's exact expectation on the 64-step table: 4 x 181 / 256.
    assert PROBE.EXPECTED_BOND_S == Fraction(181, 64)
    seeds = {
        PROBE.sweep_seed(pairs, replica, setting, index)
        for pairs in (16, 64)
        for replica in range(2)
        for setting in range(4)
        for index in range(pairs)
    }
    assert len(seeds) == 2 * 4 * (16 + 64) and all(0 < seed < PROBE.TICKET_MODULUS for seed in seeds)
    lattice = PROBE.bonded_statistics(16, 0, lattice=True)
    registry = PROBE.bonded_statistics(16, 0, lattice=False)
    # Every one of the 64 lattice outcomes is the registry's answer from the same seed.
    assert lattice["closed"] and lattice["identical_to_registry"] == 64
    assert lattice["S"] == registry["S"] and lattice["sigma_S"] == registry["sigma_S"]
    assert all(
        lattice["correlations"][key]["E"] == registry["correlations"][key]["E"]
        and lattice["correlations"][key]["missing"] == 0
        for key in lattice["correlations"]
    )
    # A hundred thousand registry pairs per correlation: within three standard errors
    # of the law's expectation, and the error itself below one part in two hundred.
    big = PROBE.bonded_statistics(100000, 0, lattice=False)
    assert big["sigma_S"] < 0.005 and abs(big["S"] - 2.828125) < 3 * big["sigma_S"]
    assert big["expected_S"] == 2.828125 and big["quantum_S"] == 2.82843


def test_only_the_bonded_candidate_moves_an_outcome_with_the_other_ends_setting():
    # At fixed hidden variable, a local candidate's outcome at one end never moves
    # with the other end's setting: parameter independence, measured as a rate.
    lottery = PROBE.causal_factors("lottery", seeds=1)
    assert lottery["closed"] and lottery["hidden_variables"] == 64
    assert lottery["parameter_independent"]
    assert lottery["alice_moves_with_bob_setting"] == {"a": 0.0, "a2": 0.0}
    assert lottery["bob_moves_with_alice_setting"] == {"b": 0.0, "b2": 0.0}
    # The registry: Alice's coin never moves with Bob's setting; Bob's answer at b'
    # moves with Alice's setting for 47 of 64 hidden variables (the law says 362/512).
    bond = PROBE.causal_factors("bond", seeds=1)
    assert bond["closed"] and bond["hidden_variables"] == 64
    assert not bond["parameter_independent"]
    assert bond["alice_moves_with_bob_setting"] == {"a": 0.0, "a2": 0.0}
    assert bond["bob_moves_with_alice_setting"] == {"b": 0.0, "b2": 0.7344}


def test_a_source_biased_in_the_agreement_half_is_a_box_above_the_quantum_value_without_a_signal():
    # The coin stays even and only the lower half of the number is fixed: the ends
    # disagree at three setting pairs and agree at the fourth, S = 4, the
    # Popescu-Rohrlich box, while neither end's plus rate moves with the other's setting.
    box = PROBE.chsh(seeds=1, capture="bond", source="agreement")
    assert box["closed"] and box["S"] == 4.0 and box["same_setting_E"] == -1.0
    assert [value["E"] for value in box["correlations"].values()] == [-1.0, 1.0, -1.0, -1.0]
    assert box["alice_rate_shift"] == 0.0 and box["bob_rate_shift"] == 0.0312
    assert all(0.45 < value["alice_plus_rate"] < 0.55 for value in box["correlations"].values())
    number = PROBE.external_number(1, "agreement")
    assert number in (PROBE.TICKET_MODULUS // 4, PROBE.TICKET_MODULUS // 4 + PROBE.TICKET_MODULUS // 2)
