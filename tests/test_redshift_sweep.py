"""Redshift from delay growth on a closed row: the law on the eye's own clock, and the fits."""

import importlib.util
import math
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
PROBES = ROOT / "examples/relativity-probes"


def load(name: str):
    spec = importlib.util.spec_from_file_location(name, PROBES / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


SWEEP = load("redshift_sweep")
HUBBLE = load("redshift_hubble")


def test_a_growing_load_stretches_the_train_on_the_eyes_own_clock():
    run = SWEEP.measure("quick", 16, 32, 1000, 7000, 400)
    assert run["distance"] == 9.5 and run["hop_time_at_launch"] == 8
    assert run["absorbed"] == 12 and run["closure"]["light_conserved"]
    assert run["closure"]["linear_in_age"]
    # The eye counts its own cycles: one per tick, with rays waiting at it and a load on it.
    assert run["eye_clock_equals_ticks"] and run["gaps_on_the_eye_clock"] == run["gaps_in_ticks"]
    assert run["gaps_on_the_eye_clock"] == [8, 9, 9, 9, 9, 10, 10, 10, 11, 11, 11]
    assert run["z"] == 0.2159 and run["duration_ratio"] == 1.2159
    # The stretch is the ratio of the hop time in force at reception to the hop time at launch.
    assert abs(run["predicted_1_plus_z"] - (1 + run["z"])) < 0.1
    assert abs(run["alpha_measured"] - math.log(1.2159) / 9.5) < 1e-5
    assert 0.025 < run["alpha_from_schedule"] < 0.035
    # The gaps between absorptions repeat the rays' last hops into the eye within a tick.
    last = run["last_hops_into_the_eye"]
    assert len(last) == 12 and abs(sum(last) / 12 - sum(run["gaps_on_the_eye_clock"]) / 11) < 1


def test_without_emission_nothing_stretches():
    run = SWEEP.measure("control", 16, 0, 1000, 7000, 200)
    assert run["hop_time_at_launch"] == 7 and run["absorbed"] == 12
    assert run["z"] == 0.0 and run["duration_ratio"] == 1.0 and run["predicted_1_plus_z"] == 1.0
    assert run["gaps_on_the_eye_clock"] == [7] * 11 and run["eye_clock_equals_ticks"]
    assert run["alpha_measured"] is None and run["alpha_from_schedule"] is None


def test_the_row_must_be_longer_than_the_train():
    with pytest.raises(ValueError, match="longer than the train"):
        SWEEP.document(12, 32, 1000, 7000, 10)


def test_the_hop_time_is_a_scale_factor_with_the_stated_deceleration():
    assert HUBBLE.lattice_distance(1.0, 1) == math.log(2)
    assert abs(HUBBLE.lattice_distance(1.0, 2) - 2 * (math.sqrt(2) - 1)) < 1e-12
    assert abs(HUBBLE.deceleration_numeric(HUBBLE.shape(1, "A")) - 1.0) < 0.01
    assert abs(HUBBLE.deceleration_numeric(HUBBLE.shape(1, "B"))) < 0.01
    assert abs(HUBBLE.deceleration_numeric(HUBBLE.shape(2, "B")) + 0.5) < 0.01
    assert abs(HUBBLE.deceleration_numeric(HUBBLE.SHAPES["flat LambdaCDM, Omega_m 0.334"]) + 0.5) < 0.01
    assert abs(HUBBLE.deceleration_numeric(HUBBLE.SHAPES["Einstein-de Sitter"]) - 0.5) < 0.01


def test_the_fit_recovers_its_own_shape_and_separates_the_others(tmp_path):
    lcdm = HUBBLE.SHAPES["flat LambdaCDM, Omega_m 0.334"]
    sample = [(z, 5 * math.log10(lcdm(z)) + 20.0, 0.1) for z in (0.02 + 0.04 * i for i in range(40))]
    own = HUBBLE.fit(lcdm, sample)
    assert own["chi2"] < 1e-9 and own["offset"] == 20.0 and own["count"] == 40
    coasting = HUBBLE.fit(HUBBLE.shape(1, "B"), sample)
    assert coasting["chi2"] > 5
    # The coasting shape is too bright at high redshift relative to its low-redshift fit:
    # the residual falls from the first bin to the last.
    bins = coasting["binned_residuals_model_minus_data"]
    assert bins[0]["mean_residual_mag"] > 0 > bins[-1]["mean_residual_mag"]
    table = tmp_path / "sne.dat"
    table.write_text(
        "CID zHD m_b_corr m_b_corr_err_DIAG IS_CALIBRATOR\n"
        "a 0.005 10.0 0.1 0\n"
        "b 0.5 22.0 0.1 1\n"
        "c 0.5 22.0 0.1 0\n",
        encoding="utf-8",
    )
    assert HUBBLE.read_pantheon(table) == [(0.5, 22.0, 0.1)]


def test_the_waves_frequency_redshifts_with_the_rate_when_its_phase_advances_per_link():
    # Phase per link: the whole frequency follows the stretch, 1 / (1 + z) in expectation.
    link = SWEEP.measure("wave", 16, 32, 1000, 7000, 400, "link")
    assert link["wave"] == "link" and link["absorbed"] == 12 and link["z"] == 0.2159
    assert link["frequency_at_the_source"] == -1.697 and link["frequency_at_the_eye"] == -1.5575
    assert link["frequency_ratio"] == 0.9178 and link["frequency_ratio_predicted"] == 0.8224
    # Phase per interval as well: only the excess over the advance rate follows the stretch.
    interval = SWEEP.measure("wave", 16, 32, 1000, 7000, 400, "interval")
    assert interval["frequency_ratio"] == 0.8164 and interval["frequency_ratio_predicted"] == 0.6032
    assert interval["frequency_ratio"] < link["frequency_ratio"] < 1
    # Without emission nothing shifts.
    still = SWEEP.measure("wave", 16, 0, 1000, 7000, 200, "link")
    assert still["frequency_ratio"] == 1.0 and still["z"] == 0.0


def test_one_source_emitting_on_its_own_clock_reads_the_same_law():
    # Twelve lamps on one Node, each emitting once, 24 ticks apart on that Node's clock
    # (three launch hops at k_e = 8); every ray crosses the same 15 links.
    run = SWEEP.measure("single", 16, 32, 1000, 7000, 600, None, True)
    assert run["single_source"] and run["distance"] == 15 and run["hop_time_at_launch"] == 8
    assert run["absorbed"] == 12 and run["eye_clock_equals_ticks"] and run["closure"]["light_conserved"]
    # The gaps at the eye against the 24-tick interval at the source.
    assert run["gaps_on_the_eye_clock"] == [36, 38, 36, 39, 37, 38, 37, 39, 34, 39, 37]
    assert run["z"] == 0.553 and run["duration_ratio"] == 1.553
    # Read ray by ray, each ray's last hop over the hop time in force when it left.
    assert run["predicted_1_plus_z"] == 1.5051
    # The two readings agree to about a tick in a gap of 24 (1.15 ticks here).
    assert abs(run["predicted_1_plus_z"] - (1 + run["z"])) * 24 < 1.2
