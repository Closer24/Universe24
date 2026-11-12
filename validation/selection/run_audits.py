"""Reproduce eight research lanes and validate their actual shared inputs.

Success means positive results AND physical counterexamples reproduced. The
native three-channel selector, sourced47 and raw-feedback48 are explicitly
different constructions; none is promoted to an accepted physical universe.
"""
from __future__ import annotations

import argparse
import hashlib
from pathlib import Path

from universe24.core import exact_json
from universe24.system.bundle import load_bundle, read_json


REPORTS = {
    "clocks": "clocks/clocks.json",
    "complexity": "complexity/complexity.json",
    "pointer": "pointer/pointer.json",
    "qca": "qca/qca.json",
    "measurement": "measurement/measurement.json",
    "coupled": "coupled/coupled.json",
    "pointer48": "pointer48/appended.json",
    "pointer48_texture": "pointer48-texture/appended.json",
    "physical_phase": "physical-phase-response/physical-phase-response.json",
    "pointer_phase": "pointer-phase-response/pointer-phase-response.json",
    "pointer_texture_phase": "pointer-texture-phase-response/pointer-phase-response.json",
    "born": "born/born.json",
    "acceptance": "acceptance/acceptance.json",
}
SOURCE_MODULE = {
    "physical_phase": "complexity", "pointer_phase": "complexity",
    "pointer_texture_phase": "complexity",
}


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def require(condition, message):
    if not condition:
        raise ValueError(message)


def write_report(path, report):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(exact_json.dumps(report, sort_keys=True) + "\n", encoding="utf-8")


def collect(out):
    """Reject stale code, mismatched apparatus seeds and unreviewed run links."""
    from validation.selection.coupled import REFERENCE_COMMIT
    out = Path(out)
    root = Path(__file__).resolve().parents[2]
    reports = {name: read_json(out / path) for name, path in REPORTS.items()}
    for name, report in reports.items():
        hashes = report.get("source_sha256", {})
        if isinstance(hashes, str):
            hashes = {"validation/selection/" + SOURCE_MODULE.get(name, name) + ".py": hashes}
        if name == "coupled":
            hashes = {"validation/selection/coupled.py": report["current_source_sha256"]}
        for path, expected in hashes.items():
            require(digest(root / path) == expected, f"stale {name} report for {path}")

    clocks, complexity = reports["clocks"], reports["complexity"]
    table = clocks["gate_table"]
    require(table == [row["output"] for row in complexity["collision_table"]],
            "clock embedding and complexity experiments use different gates")
    require(table == reports["qca"]["native_selector_quantum_lift"]["collision_table_mxy"],
            "quantum comparator uses a different collision")
    require(table == [row["after"] for row in reports["acceptance"]["native"]["explicit_collision_table"]],
            "independent reviewer uses a different collision")
    require(complexity["bridge_source_sha256"] == clocks["source_sha256"],
            "complexity embedding is stale")
    native_bundle = load_bundle(out / "complexity/representative-run/bundle")
    require(reports["born"]["gate"]["tensor_hash"] == native_bundle.tensor.fingerprint,
            "Born audit uses a different native law")
    require(any(row["tensor_hash"] == native_bundle.tensor.fingerprint
                for row in clocks["compiled_tensors"]), "native runtime law absent from clock proof")
    require(complexity["growth_passes"] == 0 and complexity["growth_failures"] == 30
            and complexity["growth_blocked"] == 6, "declared growth counterexamples changed")
    require(reports["born"]["gate"]["Born_measure_derived"] is False,
            "native routing was incorrectly promoted to a Born derivation")
    born = reports["born"]
    for name, expected in born["artifact_sha256"].items():
        require(digest(out / "born" / name) == expected, "Born raw evidence hash mismatch")
    require(born["saved_replay"]["transitions"] == 4080,
            "complete declared Born control population missing")
    replay = born["saved_replay"]
    require(all(replay[key] for key in ("complete_contiguous_trial_chains", "independent_scalar_replay",
                                       "complete_inverse", "canonical_records_equal")),
            "Born trial continuity or independent replay failed")
    require(replay["by_family"] == {"gate": 3072, "pointer": 1008},
            "Born trial families do not match the declared population")

    pointer_trials = out / "pointer/instrument_trials.json"
    require(reports["measurement"]["native_pointer_observation"]["source_sha256"] == digest(pointer_trials),
            "measurement report uses different pointer trials")
    require(reports["pointer"]["failed"]["exclusive_choice"], "double-record control missing")
    coupled = reports["coupled"]
    require(coupled["reference_commit"] == REFERENCE_COMMIT,
            "wrong corrected-frame source revision")
    require(len(coupled["verified_reference_python_blobs"]) > 0,
            "pinned reference Python bytes were not verified")
    require(coupled["current_main_full_state_comparisons"] == 40
            and coupled["current_main_runtime_and_replay"], "incomplete sourced47 comparison")
    raw = out / "coupled/reference/raw-reference.json.gz"
    require(digest(raw) == coupled["raw_reference_sha256"] == reports["physical_phase"]["raw_source_sha256"],
            "phase audit uses different sourced47 histories")
    primary = load_bundle(out / "coupled/connected-homogeneous-+1/bundle")
    require(coupled["primary_bundle_id"] == primary.bundle_id, "primary sourced47 bundle mismatch")

    for variant, phase, subdir, source_case in (
        ("pointer48", "pointer_phase", "pointer48", "connected-homogeneous-+1"),
        ("pointer48_texture", "pointer_texture_phase", "pointer48-texture", "connected-texture-+1"),
    ):
        source = load_bundle(out / "coupled" / source_case / "bundle")
        appended = reports[variant]
        require(source.tensor.G == 47 and appended["channels"] == 48,
                "joint apparatus allocation changed")
        require(source.bundle_id == appended["base_bundle_id"]
                and source.tensor.fingerprint == appended["base_tensor_hash"],
                "pointer was appended to a different source seed or law")
        response = reports[phase]
        for index, name in enumerate(("raw_record_feedback", "matched_old_memory")):
            saved = read_json(out / subdir / name / "validation.json")
            require(saved["run_id"] == response["run_ids"][index] == appended["runs"][name]["run_id"],
                    "pointer phase and acquisition reports concern different runs")
            require(saved["bundle_id"] == response["bundle_ids"][index] == appended["runs"][name]["bundle_id"],
                    "pointer history seed mismatch")
            require(saved["tensor_hash"] == response["tensor_hash"], "pointer law mismatch")
        require(appended["steps"] == 5 and response["predeclared_steps"] == 4,
                "exploratory fifth update was lost or relabeled")
    require(all(row["exact_phase_link_direction_differences"] == 0
                for row in reports["pointer_phase"]["steps"]), "homogeneous negative control changed")
    require([row["exact_phase_link_direction_differences"]
             for row in reports["pointer_texture_phase"]["steps"]] == [0, 0, 0, 0, 12, 12],
            "declared textured pointer response changed")

    reviewed = {row["run_id"]: row for row in reports["acceptance"]["saved_runs"]}
    runtime_paths = sorted(out.rglob("validation.json"))
    require(len(runtime_paths) == 19, "missing or extra declared runtime evidence")
    require(len(reviewed) == len(runtime_paths), "independent review population mismatch")
    for path in runtime_paths:
        saved = read_json(path)
        require(saved["run_id"] in reviewed, "runtime missing from independent replay")
        review = reviewed[saved["run_id"]]
        require(review["bundle_id"] == saved["bundle_id"] and review["tensor_hash"] == saved["tensor_hash"]
                and review["steps"] == saved["steps"] and review["complete_saved_scalar_replay"],
                "independent replay does not match saved runtime")

    source_paths = sorted((root / "validation/selection").glob("*.py"))
    source_paths += sorted((root / "universe24/tests").glob("test_selection*.py"))
    source_paths += [root / p for p in (
        "universe24/core/engine.py", "universe24/core/tensor.py", "universe24/core/lattice.py",
        "universe24/core/exact_json.py", "universe24/system/bundle.py",
        "universe24/system/decoder.py", "universe24/system/runtime.py",
        "universe24/tests/test_migration.py", "validation/clock_links/acceptance_audit.py")]
    summary = {
        "schema": "universe24/validation/retained-selection/1",
        "upstream_main": "4c494c1188f70eb8a677bf59765cc6e8571c6b88",
        "base_pr49": "a3013a9d91ae5ff74ed8b4f511e03ac221425b98",
        "reference_pr50": REFERENCE_COMMIT,
        "research_lanes": 8,
        "constructions": {"native_selector": 3, "native_pulse_pointer": 3,
                          "reciprocal_homogeneous_source": 47, "raw_record_feedback": 48},
        "gates": {
            "native_prepared_clock_and_reversible_preference": "passed",
            "native_retained_history_changes_later_carrier": "passed",
            "finite_pulse_record_and_feedback": "passed",
            "homogeneous_reciprocal_source_identity": "passed",
            "same_48_memory_changes_textured_phase": "passed_as_mechanical_control",
            "complete_saved_scalar_replay": "passed",
            "sustained_burst_complexity_growth": "failed_30_blocked_6",
            "unconditional_exclusive_pointer": "failed",
            "unique_Born_preparation_measure": "not_derived",
            "physical_Bell_instrument": "not_supplied",
            "globally_bounded_interaction_energy": "failed",
            "inhomogeneous_apparatus_momentum_and_record_stress": "not_supplied",
            "shared_metric_material_clock": "not_tested",
            "general_Einstein_constraints_and_convergence": "not_established",
        },
        "saved_runtime_count": len(runtime_paths),
        "independent_integer_comparisons": sum(row["retained_integer_comparisons"] for row in reviewed.values()),
        "independent_canonical_records": sum(row["canonical_records_compared"] for row in reviewed.values()),
        "reports": reports,
        "report_sha256": {name: digest(out / relative) for name, relative in REPORTS.items()},
        "source_sha256": {str(path.relative_to(root)): digest(path) for path in source_paths},
        "interpretation": "Eight synchronized research lanes, not eight physical models. Mechanical preference is internal retained state; clicks remain passive. Separate constructions and negative controls cannot be pooled into a physics certificate.",
    }
    write_report(out / "summary.json", summary)
    return summary


def run(reference, out):
    from validation.selection import acceptance, born, clocks, complexity, coupled, measurement, pointer, qca
    out = Path(out)
    if out.exists() and any(out.iterdir()):
        raise ValueError("fresh combined audit directory required")
    out.mkdir(parents=True, exist_ok=True)
    def stage(name):
        print("selection audit: " + name, flush=True)
    stage("clocks and native selection")
    write_report(out / REPORTS["clocks"], clocks.audit(complexity.SORT_GATE))
    complexity.audit(out / "complexity")
    stage("retained pulse pointer and quantum reference contracts")
    pointer.audit(out / "pointer")
    write_report(out / REPORTS["qca"], qca._json(qca.audit()))
    write_report(out / REPORTS["measurement"], measurement.audit(out / "pointer/instrument_trials.json"))
    stage("pinned corrected-frame source and reciprocal47")
    coupled.audit(reference=reference, out=out / "coupled", steps=4)
    stage("same-source48 memory interventions, including exploratory fifth update")
    for subdir, source_case, response in (
        ("pointer48", "connected-homogeneous-+1", "pointer-phase-response"),
        ("pointer48-texture", "connected-texture-+1", "pointer-texture-phase-response"),
    ):
        pointer.audit_appended(out / "coupled" / source_case / "bundle", out / subdir, steps=5)
        complexity.audit_pointer_response(out / subdir / "raw_record_feedback",
                                         out / subdir / "matched_old_memory", out / response)
    complexity.audit_physical_response(out / "coupled/reference/raw-reference.json.gz",
                                       out / "physical-phase-response")
    stage("complete preparation-measure controls")
    born.audit(out / "born")
    stage("independent saved-state and source review")
    saved_runs = sorted(path.parent for path in out.rglob("validation.json"))
    acceptance.audit(out / "acceptance", saved_runs)
    return collect(out)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--reference", type=Path)
    parser.add_argument("--out", type=Path, default=Path("runs/retained-selection"))
    parser.add_argument("--collect", action="store_true")
    args = parser.parse_args(argv)
    if not args.collect and args.reference is None:
        parser.error("--reference requires a checkout of the exact pinned PR50 revision")
    result = collect(args.out) if args.collect else run(args.reference, args.out)
    print(exact_json.dumps({"gates": result["gates"], "saved_runtime_count": result["saved_runtime_count"]}, sort_keys=True))


if __name__ == "__main__":
    main()
