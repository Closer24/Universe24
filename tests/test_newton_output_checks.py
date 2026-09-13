"""Synthetic measurement fixtures test the external checker, not physical emergence."""

import ast
import hashlib
import json
import subprocess
import sys
from fractions import Fraction
from pathlib import Path

import pytest

from tools import newton_output_checks as check


def history(ticks=120, rest=False):
    return [
        {
            "tick": t,
            "position": (Fraction(t // 20), Fraction(0), Fraction(0)),
            "x": (Fraction(0 if rest else t // 20), Fraction(0), Fraction(0)),
            "mass": Fraction(1),
            "p": (Fraction(0 if rest else 1, 20), Fraction(0), Fraction(0)),
        }
        for t in range(ticks + 1)
    ]


def saved_run(folder, rows=None, shape=201):
    rows = history() if rows is None else rows
    initial = {
        "model_id": "synthetic-output-fixture",
        "shape": [shape] * 3,
        "boundary": "periodic",
        "link_ticks": 1,
        "fields": [{"name": "mass"}, {"name": "momentum", "scale": 20}],
    }
    frames = [
        {
            "tick": row["tick"],
            "cells": [
                {
                    "position": [int(v) % shape for v in row["x"]],
                    "disturbances": [
                        {
                            "type": "body",
                            "values": {"mass": [1], "momentum": [int(v * 20) for v in row["p"]]},
                        }
                    ],
                }
            ],
            "transfers": [],
        }
        for row in rows
    ]
    folder.mkdir(exist_ok=True)
    (folder / "initialization.json").write_text(json.dumps(initial))
    meta = {
        "model": initial["model_id"],
        "status": "completed",
        "error": None,
        "completed_ticks": len(rows) - 1,
        "requested_ticks": len(rows) - 1,
        "source_sha256": "synthetic-source",
        "initialization_sha256": hashlib.sha256(
            (folder / "initialization.json").read_bytes()
        ).hexdigest(),
    }
    rewrite(folder, meta, frames)
    return meta, frames


def rewrite(folder, meta, frames):
    (folder / "run.json").write_text(json.dumps(meta))
    (folder / "state.json").write_text(json.dumps(frames[-1]))
    (folder / "run.html").write_text(
        '<script id="recording" type="application/json">'
        + json.dumps({"metadata": meta, "frames": frames})
        + "</script>"
    )


def test_inertia_uses_positions_and_held_out_time_windows():
    result = check.inertia(history(), 20)
    assert result["status"] == "pass"
    assert result["measured_velocity"] == ["1/20", "0", "0"]
    assert result["max_absolute_error"] == "19/20"
    assert result["held_out_ticks"] == 100


def test_rest_is_exact_not_a_one_cell_drift_allowance():
    rows = history(rest=True)
    assert check.inertia(rows, 20)["status"] == "pass"
    rows[-1]["x"] = (Fraction(1), Fraction(0), Fraction(0))
    assert check.inertia(rows, 20)["status"] == "fail"


@pytest.mark.parametrize("corruption", ["momentum", "trajectory"])
def test_inertia_rejects_measured_drift(corruption):
    rows = history()
    if corruption == "momentum":
        rows[-1]["p"] = (Fraction(1), Fraction(0), Fraction(0))
    else:
        rows[-1]["x"] = (Fraction(9), Fraction(0), Fraction(0))
    assert check.inertia(rows, 20)["status"] == "fail"


def test_low_speed_without_resolved_displacement_is_not_a_pass():
    rows = history(rest=True)
    rows[0]["p"] = (Fraction(1, 1000), Fraction(0), Fraction(0))
    with pytest.raises(check.NotTestable, match="unresolved"):
        check.inertia(rows, 20)


def test_insufficient_duration_and_excess_speed_are_not_accepted():
    with pytest.raises(check.NotTestable):
        check.inertia(history(20), 20)
    rows = history()
    for row in rows:
        row["x"] = (Fraction(row["tick"]), Fraction(0), Fraction(0))
    with pytest.raises(check.NotTestable, match="speeds"):
        check.inertia(rows, 20)


def test_momentum_velocity_is_independently_measured_from_position():
    rows = history()
    assert check.momentum_velocity({"body": rows}, 20)["status"] == "pass"
    for row in rows:
        row["p"] = (Fraction(1), Fraction(0), Fraction(0))
    assert check.momentum_velocity({"body": rows}, 20)["status"] == "fail"


def pair():
    left, right = history(4, rest=True), history(4, rest=True)
    for index, (a, b) in enumerate(zip(left, right, strict=True)):
        a["mass"], b["mass"] = Fraction(2), Fraction(3)
        a["p"] = (Fraction(8 if index < 2 else -4, 120), Fraction(0), Fraction(0))
        b["p"] = (Fraction(-3 if index < 2 else 9, 120), Fraction(0), Fraction(0))
    return {"A": left, "B": right}


def test_contact_recomputes_impulses_and_energy_not_saved_success_flags():
    result = check.contact(pair())
    assert all(row["status"] == "pass" for row in result.values())
    assert result["newton_third"]["impulses"][0]["left"] == ["-1/10", "0", "0"]
    assert result["elastic_energy"]["initial_energy"] == "7/5760"


@pytest.mark.parametrize("corruption", ["unbalanced", "delayed", "nonlocal", "no_contact"])
def test_third_law_requires_real_same_time_local_opposite_impulses(corruption):
    rows = pair()
    if corruption == "unbalanced":
        rows["B"][-1]["p"] = (Fraction(1), Fraction(0), Fraction(0))
    elif corruption == "delayed":
        rows["B"][2]["p"] = rows["B"][1]["p"]
    elif corruption == "nonlocal":
        rows["B"][1]["position"] = (Fraction(2), Fraction(0), Fraction(0))
    else:
        for h in rows.values():
            for row in h:
                row["p"] = h[0]["p"]
    status = check.contact(rows)["newton_third"]["status"]
    assert status == ("not_testable" if corruption == "no_contact" else "fail")


def independent(kind):
    return {
        "measurement_kind": kind,
        "source_sha256": "synthetic-source",
        "provenance": {
            "derived_from_target_kinematics": False,
            "method": "Synthetic checker fixture, not a physical measurement",
            "calibration": "Exact synthetic rational units",
        },
    }


def accelerated():
    rows = history(800, rest=True)
    for row in rows:
        t = row["tick"]
        row["x"] = (Fraction(t * t // 16000), Fraction(0), Fraction(0))
    measurement = independent("independent_net_force")
    measurement["samples"] = [{"tick": row["tick"], "force": ["1/8000", 0, 0]} for row in rows]
    return rows, measurement


def test_second_law_compares_force_to_position_acceleration_not_momentum():
    rows, measurement = accelerated()
    # Momentum is deliberately uninformative: it defines neither force nor acceleration.
    result = check.second_law(rows, measurement, "synthetic-source", 200)
    assert result["status"] == "pass"
    for row in measurement["samples"]:
        row["force"] = ["3/8000", 0, 0]
    assert check.second_law(rows, measurement, "synthetic-source", 200)["status"] == "fail"


@pytest.mark.parametrize("problem", ["circular", "zero", "short", "changing", "source"])
def test_second_law_rejects_missing_independence_or_inadequate_measurements(problem):
    rows, measurement = accelerated()
    if problem == "circular":
        measurement["provenance"]["derived_from_target_kinematics"] = True
    elif problem == "source":
        measurement["source_sha256"] = "other"
    elif problem == "zero":
        for sample in measurement["samples"]:
            sample["force"] = [0, 0, 0]
    elif problem == "short":
        measurement["samples"].pop()
    else:
        measurement["samples"][-1]["force"] = [0, 0, 0]
    with pytest.raises(ValueError):
        check.second_law(rows, measurement, "synthetic-source", 200)


def gravitational_sweep(power=2):
    measurement = independent("gravitational_force_sweep")
    measurement["samples"] = [
        {
            "separation": [r, 0, 0],
            "force": [str(Fraction(-1, r**power)), 0, 0],
            "source_mass": 1,
            "test_mass": 1,
        }
        for r in (2, 4, 6)
    ]
    return measurement


def test_gravity_uses_one_calibration_and_held_out_distances():
    result = check.gravity(gravitational_sweep(), "synthetic-source")
    assert result["status"] == "pass"
    assert result["calibration_g_squared"] == "1"
    assert result["held_out_samples"] == 2
    assert result["mass_scaling_tested"] is False
    assert check.gravity(gravitational_sweep(1), "synthetic-source")["status"] == "fail"


@pytest.mark.parametrize("force", [[0, 0, 0], [1, 0, 0], [-1, 1, 0]])
def test_gravity_rejects_zero_repulsive_and_nonradial_force(force):
    measurement = gravitational_sweep()
    measurement["samples"][1]["force"] = force
    assert check.gravity(measurement, "synthetic-source")["status"] == "fail"


def test_gravity_does_not_pass_without_multiple_separations():
    measurement = gravitational_sweep()
    measurement["samples"] = [measurement["samples"][0]] * 3
    with pytest.raises(check.NotTestable):
        check.gravity(measurement, "synthetic-source")


def test_saved_output_is_read_only_and_missing_force_stays_partial(tmp_path):
    saved_run(tmp_path)
    before = {p.name: p.read_bytes() for p in tmp_path.iterdir()}
    result = check.audit(tmp_path, "inertia", 20)
    assert result["status"] == "partial"
    assert result["checks"]["newton_first"]["status"] == "pass"
    assert result["checks"]["newton_second"]["status"] == "not_testable"
    assert result["checks"]["newton_gravity"]["status"] == "not_testable"
    assert before == {p.name: p.read_bytes() for p in tmp_path.iterdir()}


@pytest.mark.parametrize(
    "problem",
    [
        "failed",
        "short",
        "hash",
        "missing_frame",
        "false_tick",
        "duplicate_identity",
        "transit",
        "jump",
        "lost_mass",
    ],
)
def test_corrupted_or_inapplicable_recordings_cannot_pass(tmp_path, problem):
    meta, frames = saved_run(tmp_path)
    if problem == "failed":
        meta["status"] = "failed"
    elif problem == "short":
        meta["requested_ticks"] += 1
    elif problem == "hash":
        meta["initialization_sha256"] = "wrong"
    elif problem == "missing_frame":
        frames.pop(10)
    elif problem == "false_tick":
        frames[0]["tick"] = False
    elif problem == "duplicate_identity":
        frames[10]["cells"][0]["disturbances"] *= 2
    elif problem == "transit":
        frames[10]["transfers"] = [{"type": "body"}]
    elif problem == "jump":
        frames[10]["cells"][0]["position"][0] = 5
    else:
        del frames[10]["cells"][0]["disturbances"][0]["values"]["mass"]
    rewrite(tmp_path, meta, frames)
    with pytest.raises(ValueError):
        check.audit(tmp_path, "inertia", 20)


def test_final_state_and_recording_must_agree(tmp_path):
    saved_run(tmp_path)
    (tmp_path / "state.json").write_text('{"cells":[],"transfers":[]}')
    with pytest.raises(ValueError, match="disagree"):
        check.audit(tmp_path, "inertia", 20)


def test_periodic_coordinates_unwrap_without_inventing_acceleration(tmp_path):
    saved_run(tmp_path, shape=5)
    assert check.audit(tmp_path, "inertia", 20)["checks"]["newton_first"]["status"] == "pass"


def test_duplicate_keys_and_boolean_measurements_are_rejected():
    with pytest.raises(ValueError, match="Duplicate"):
        check.decode('{"tick":1,"tick":2}')
    with pytest.raises(ValueError):
        check.rational(True)


def test_checker_has_no_simulator_or_third_party_imports():
    tree = ast.parse(Path(check.__file__).read_text())
    allowed = {"__future__", "argparse", "hashlib", "json", "fractions", "html", "pathlib", "typing"}
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            assert all(alias.name.split(".")[0] in allowed for alias in node.names)
        elif isinstance(node, ast.ImportFrom):
            assert node.module.split(".")[0] in allowed


def test_detached_cli_reports_missing_measurements_without_a_green_exit(tmp_path):
    saved_run(tmp_path / "run")
    script = tmp_path / "checker.py"
    script.write_text(Path(check.__file__).read_text())
    process = subprocess.run(
        [
            sys.executable,
            "-I",
            str(script),
            str(tmp_path / "run"),
            "--case",
            "inertia",
            "--window",
            "20",
        ],
        cwd=tmp_path,
        capture_output=True,
        text=True,
        check=False,
    )
    assert process.returncode == 3, process.stderr
    assert json.loads(process.stdout)["status"] == "partial"


def test_capture_controls_do_not_modify_the_reference_law():
    from tools import capture_newton_outputs as capture

    original = json.loads(capture.REFERENCE.read_text())
    before = json.dumps(original, sort_keys=True)
    generated = capture.controls(original)
    assert json.dumps(original, sort_keys=True) == before
    for document in generated.values():
        assert document["interactions"] == []
        assert (
            document["disturbance_types"][0]["transport"]["rate"]
            == original["disturbance_types"][0]["transport"]["rate"]
        )
    assert capture.WINDOWS == {"collision-reference": 120, "free": 60, "rest": 30, "slow": 1000}
