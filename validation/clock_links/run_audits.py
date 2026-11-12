"""Reproduce the six clock-link checks on one declared 44-channel bundle.

All physics failures are retained in the combined report. A successful command
means the stated experiments and negative controls reproduced, not that a
physical clock, Born measurement or complexity-selection law was obtained.
"""
from __future__ import annotations

import argparse
import hashlib
from pathlib import Path
import subprocess
import sys

from universe24.core import exact_json
from universe24.system.bundle import read_json


REPORTS = {
    "algebra": "algebra/algebra.json",
    "phase": "phase/phase.json",
    "observer": "observer/audit.json",
    "complexity": "complexity/complexity.json",
    "born_bell": "born/report.json",
    "acceptance": "acceptance/acceptance.json",
}


def collect(out):
    out = Path(out)
    reports = {name: read_json(out / relative) for name, relative in REPORTS.items()}
    phase, observer = reports["phase"], reports["observer"]
    born, acceptance = reports["born_bell"], reports["acceptance"]
    if not (phase["tensor_hash"] == observer["tensor_hash"] == born["tensor_hash"]
            == acceptance["tensor_hash"]):
        raise ValueError("reports do not concern the same apparatus tensor")
    if not (phase["bundle_id"] == observer["bundle_id"] == acceptance["bundle_id"]):
        raise ValueError("reports mix different seeds, metadata or apparatus protocols")
    if (phase["base_bundle_id"] != born["base_bundle_id"]
            or phase["base_tensor_hash"] != born["base_tensor_hash"]):
        raise ValueError("Born calibrations use a different source bundle")
    board_runs = reports["complexity"]["board_runs"]
    if len(board_runs) != 1 or board_runs[0]["bundle_id"] != phase["bundle_id"]:
        raise ValueError("complexity results concern a different board")
    if observer["run_id"] != acceptance["saved_run"]["run_id"] or observer["run_id"] != board_runs[0]["run_id"]:
        raise ValueError("observation, structural and scalar audits concern different trajectories")
    runtime = read_json(out / "phase/run/validation.json")
    if (runtime["run_id"] != observer["run_id"]
            or phase["steps"] != acceptance["saved_run"]["steps"]):
        raise ValueError("saved runtime identity or horizon mismatch")
    replay = born["saved_replay"]
    if replay["saved_transitions_verified"] != 258 or not all(
        replay[key] for key in ("independent_scalar_oracle", "all_complete_rewinds",
                               "canonical_stream_parity", "unique_complete_declared_trials")
    ):
        raise ValueError("Born control trajectories were not completely verified")
    if phase["channels_per_node"] != 48 or not phase["base_projection_unchanged"]:
        raise ValueError("the joint allocation or source projection changed")
    if born["Born_binary_frequencies"] != "failed" or born["one_outcome_per_trial"] != "failed":
        raise ValueError("known detector counterexamples were lost")
    if not (observer["online_offline_parity"] and observer["saved_run_unchanged"]):
        raise ValueError("observer parity/passivity failed")
    root = Path(__file__).resolve().parents[2]
    for name, evidence in reports.items():
        hashes = evidence["source_sha256"]
        if isinstance(hashes, str):
            hashes = {f"validation/clock_links/{name}_audit.py": hashes}
        elif name == "observer":
            hashes = {"validation/clock_links/" + key: value for key, value in hashes.items()}
        for relative, expected in hashes.items():
            if hashlib.sha256((root / relative).read_bytes()).hexdigest() != expected:
                raise ValueError(f"{name} report is stale for source {relative}")
    source_paths = sorted((root / "validation/clock_links").glob("*.py"))
    source_paths += sorted((root / "universe24/tests").glob("test_clock_link*.py"))
    source_paths += [root / name for name in (
        "validation/team48_contract.py", "universe24/core/engine.py",
        "universe24/core/tensor.py", "universe24/core/lattice.py",
        "universe24/core/exact_json.py", "universe24/system/bundle.py",
        "universe24/system/decoder.py", "universe24/system/runtime.py")]
    report = {
        "schema": "universe24/validation/clock-links-synthesis/1",
        "upstream_main": "4c494c1188f70eb8a677bf59765cc6e8571c6b88",
        "reference_law_source": "49b896c795203914a939e465d6d39e5b99343259",
        "tensor_hash": phase["tensor_hash"], "bundle_id": phase["bundle_id"],
        "channels_per_node": 48, "retained_integers_per_node": 144,
        "gates": {
            "same_board_exact_phase_records": "passed",
            "complete_state_scalar_oracle_replay": "passed",
            "records_only_passive_observer": "passed",
            "one_outcome_per_measurement": "failed",
            "binary_born_frequencies": "failed",
            "recurrent_structural_growth": "blocked",
            "local_complexity_selection": "not_implemented",
            "local_gauge_covariant_clock_links": "failed",
            "metric_calibrated_proper_clock": "not_tested",
            "apparatus_stress_backreaction": "not_supplied",
            "engine_bell_violation": "not_tested",
        },
        "reports": reports,
        "report_sha256": {name: hashlib.sha256((out / relative).read_bytes()).hexdigest()
                          for name, relative in REPORTS.items()},
        "source_sha256": {str(path.relative_to(root)): hashlib.sha256(path.read_bytes()).hexdigest()
                          for path in source_paths},
        "interpretation": "Finite one-way research apparatus on the same coupled carrier; no physical model promotion. Binary events, observed quotient weights and hidden intensities are distinct.",
    }
    (out / "summary.json").write_text(exact_json.dumps(report, sort_keys=True) + "\n", encoding="utf-8")
    return report


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base-bundle", type=Path)
    parser.add_argument("--out", type=Path, default=Path("runs/clock-links"))
    parser.add_argument("--collect", action="store_true", help="collect already completed audits")
    args = parser.parse_args(argv)
    if not args.collect:
        if args.base_bundle is None:
            parser.error("--base-bundle is required when running audits")
        if args.out.exists() and any(args.out.iterdir()):
            parser.error("fresh output directory required")
        args.out.mkdir(parents=True, exist_ok=True)
        phase = args.out / "phase"
        commands = [
            ("algebra_audit", ["--out", args.out / "algebra"]),
            ("phase_audit", ["--base-bundle", args.base_bundle, "--out", phase]),
            ("observer_audit", ["--run", phase / "run", "--out", args.out / "observer"]),
            ("complexity_audit", ["--run", phase / "run", "--out", args.out / "complexity"]),
            ("born_bell_audit", ["--base-bundle", args.base_bundle, "--out", args.out / "born"]),
            ("acceptance_audit", ["--bundle", phase / "run/bundle", "--out", args.out / "acceptance"]),
        ]
        for module, arguments in commands:
            subprocess.run([sys.executable, "-m", "validation.clock_links." + module,
                            *map(str, arguments)], check=True)
    report = collect(args.out)
    print(exact_json.dumps({"tensor_hash": report["tensor_hash"], "gates": report["gates"]}, sort_keys=True))


if __name__ == "__main__":
    main()
