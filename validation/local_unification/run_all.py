"""Collect reproducible, scoped evidence from one saved source-bearing run.

Supporting experiments retain their own laws and seeds. Only readers of the
same twelve-channel history enter the main identity join. Neither arithmetic
replay nor an exact finite null-source chart grants general physical acceptance.
"""
from __future__ import annotations

import argparse
import gzip
import hashlib
from fractions import Fraction
from itertools import product
from pathlib import Path
import platform

from universe24.core import State, exact_json
from universe24.system.bundle import canonical_bytes, load_bundle, state_from_data
from validation.local_unification import (
    acceptance, balance, contracts, geometry, geometry_review, limits,
    native, organization, records,
)

ROOT = Path(__file__).resolve().parents[2]
CORE_SOURCES = (
    "validation/selection/complexity.py",
    "universe24/algebra/group_2o.py",
    "universe24/core/engine.py", "universe24/core/tensor.py",
    "universe24/core/lattice.py", "universe24/core/exact_json.py",
    "universe24/system/bundle.py", "universe24/system/decoder.py",
    "universe24/system/runtime.py",
)


def _sha(path):
    digest = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def _write(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(canonical_bytes(value) + b"\n")


def source_snapshot():
    paths = sorted(set(CORE_SOURCES) | {
        str(path.relative_to(ROOT))
        for package in ("validation/local_unification", "universe24")
        for path in (ROOT / package).rglob("*.py")
    })
    if any((ROOT / path).is_symlink() for path in paths):
        raise ValueError("source files must not be symlinks")
    return {path: _sha(ROOT / path) for path in paths}


def _case_key(value):
    keys = ("side", "direction", "seed", "memory", "variant", "steps")
    if any(key not in value for key in keys):
        raise ValueError("incomplete trial identity")
    if (type(value["side"]) is not int or type(value["seed"]) is not int
            or type(value["steps"]) is not int
            or type(value["direction"]) is not list
            or any(type(v) is not int for v in value["direction"])):
        raise ValueError("trial identity must use exact integers")
    return (value["side"], tuple(value["direction"]), value["seed"],
            value["memory"], value["variant"], value["steps"])


def _panel_digest(value):
    # Organization's independently retained archive format includes default
    # JSON spacing. Do not substitute the bundle's compact canonical encoding.
    return hashlib.sha256(exact_json.dumps(value, sort_keys=True).encode()).hexdigest()


def validate_panel(report, *, full_panel=True):
    """Reject missing, duplicate, mixed-law or unbound panel trials."""
    protocol = organization.PROTOCOL
    if report.get("protocol") != protocol or report.get("full_panel") is not full_panel:
        raise ValueError("panel protocol or coverage declaration changed")
    sides = protocol["sides"] if full_panel else protocol["sides"][:1]
    seeds = protocol["seeds"] if full_panel else protocol["seeds"][:1]
    directions = protocol["directions"] if full_panel else protocol["directions"][:1]
    expected = {
        (side, tuple(direction), seed, memory, variant, protocol["steps"])
        for side, direction, seed, memory, variant in product(
            sides, directions, seeds, protocol["memory_preparations"], protocol["variants"])
    }
    cases = report.get("cases")
    if type(cases) is not list:
        raise ValueError("complete case summaries required")
    indexed = {}
    for row in cases:
        key = _case_key(row)
        if key in indexed:
            raise ValueError("duplicate panel trial")
        indexed[key] = row
    if set(indexed) != expected:
        raise ValueError("missing or unexpected panel trials")
    if report.get("case_count") != len(expected):
        raise ValueError("case count differs from full Cartesian coverage")
    shared = sum(key[4] == "shared" for key in expected)
    if report.get("shared_case_count") != shared:
        raise ValueError("shared-case denominator changed")
    sources = {
        "source_sha256": ROOT / "validation/local_unification/organization.py",
        "native_source_sha256": ROOT / "validation/local_unification/native.py",
        "inherited_metric_source_sha256": ROOT / "validation/selection/complexity.py",
    }
    if any(report.get(key) != _sha(path) for key, path in sources.items()):
        raise ValueError("panel reports stale implementation sources")
    archive = Path(report["complete_panel_archive"])
    if _sha(archive) != report["complete_panel_archive_sha256"]:
        raise ValueError("complete panel archive checksum mismatch")
    seen, laws, state_count = set(), {}, 0
    with gzip.open(archive, "rt", encoding="utf-8") as stream:
        for line in stream:
            raw = exact_json.loads(line)
            if type(raw) is not dict or set(raw) != {"spec", "tensor_hash", "states"}:
                raise ValueError("unsupported complete trial record")
            key = _case_key(raw["spec"])
            if key not in indexed or key in seen:
                raise ValueError("missing, duplicate or unrelated archived trial")
            seen.add(key)
            summary = indexed[key]
            side, direction, _, _, variant, steps = key
            law_key = (direction, variant)
            if law_key not in laws:
                laws[law_key] = native.build_tensor(
                    direction, coupled=variant != "collision_off",
                    stream_records=variant != "record_transport_off").fingerprint
            if raw["tensor_hash"] != laws[law_key] or summary["tensor_hash"] != laws[law_key]:
                raise ValueError("trial has a different declared law")
            states = raw["states"]
            if type(states) is not list or len(states) != steps + 1:
                raise ValueError("trial lacks its complete declared horizon")
            if (summary["seed_hash"] != _panel_digest(states[0])
                    or summary["complete_trace_hash"] != _panel_digest(states)):
                raise ValueError("trial seed/history identity mismatch")
            for data in states:
                state = state_from_data(data)
                if state.L != side or state.G != 8:
                    raise ValueError("trial retained allocation changed")
                if bool((state.r < 0).any()) or bool((state.r >= 6).any()):
                    raise ValueError("illegal retained carry in panel")
            if summary["complete_rewind"] is not True:
                raise ValueError("panel includes an unsuccessful complete rewind")
            state_count += len(states)
    if seen != expected:
        raise ValueError("archive omitted declared negative-control trials")
    task = report.get("repeated_task", {})
    task_rows = task.get("cases", [])
    task_variants = ("shared", "record_transport_off", "collision_off", "late_supply_removed")
    task_expected = {(side, tuple(direction), variant)
                     for side, direction, variant in product((7, 9), protocol["directions"], task_variants)}
    task_seen = set()
    expected_corrections = {"shared": [1, 2, 5, 6], "record_transport_off": [1],
                            "collision_off": [], "late_supply_removed": [1, 2]}
    for row in task_rows:
        key = (row["side"], tuple(row["direction"]), row["variant"])
        if key not in task_expected or key in task_seen:
            raise ValueError("duplicate or unrelated designed repeat-use control")
        task_seen.add(key)
        variant = row["variant"]
        law = native.build_tensor(
            tuple(row["direction"]), coupled=variant != "collision_off",
            stream_records=variant != "record_transport_off")
        if (row["tensor_hash"] != law.fingerprint or row["complete_rewind"] is not True
                or row["specification"]["steps"] != 6
                or row["correction_microsteps"] != expected_corrections[variant]
                or len(row["phases"]) != 2):
            raise ValueError("designed repeat-use control disagrees with its declared fixture")
    if (task_seen != task_expected or task.get("case_count") != len(task_expected)
            or task.get("same_law_late_supply_control") is not True):
        raise ValueError("missing designed repeat-use negative controls")
    controls = report.get("negative_controls", {}).get("controls", {})
    if set(controls) != {"fresh_random", "frozen_random", "periodic"}:
        raise ValueError("organization metric negative controls omitted")
    for control in controls.values():
        if (control.get("this_is_an_Engine_trajectory") is not False
                or len(control["scores"]) != protocol["steps"] + 1):
            raise ValueError("negative-control scope or horizon changed")
    return {"cases": len(expected), "shared_cases": shared,
            "designed_repeat_use_cases": len(task_expected),
            "complete_state_snapshots": state_count,
            "all_declared_trials_retained": True,
            "archive_sha256": report["complete_panel_archive_sha256"],
            "coverage": "full_registered_panel" if full_panel else "explicit_quick_subset"}


def _saved_states(run_dir):
    bundle = load_bundle(Path(run_dir) / "bundle")
    states = [bundle.seed]
    with gzip.open(Path(run_dir) / "full_trace.jsonl.gz", "rt", encoding="utf-8") as stream:
        for step, line in enumerate(stream, 1):
            row = exact_json.loads(line)
            before, after = (state_from_data(row[key]) for key in ("before", "after"))
            if row["step"] != step or not before.same_as(states[-1]):
                raise ValueError("disconnected complete trace")
            states.append(after)
    return bundle, states


def _bound_report(report, identity, keys):
    for report_key, identity_key in keys.items():
        if report.get(report_key) != identity[identity_key]:
            raise ValueError("independent report belongs to a different saved run")


def inspect_joint_run(run_dir, protocol, *, source_paths=None, out=None):
    """Independently inspect every main claim on the same complete history."""
    run_dir = Path(run_dir)
    paths = sorted(source_snapshot() if source_paths is None else source_paths)
    identity = contracts.run_identity(run_dir, source_paths=paths)
    bundle, states = _saved_states(run_dir)
    direction = tuple(protocol["direction"])
    if (identity["channels"] != 12
            or bundle.tensor.fingerprint != geometry.build_tensor(direction).fingerprint
            or protocol["L"] != bundle.seed.L
            or protocol["microsteps"] != identity["steps"]
            or len(states) != identity["steps"] + 1):
        raise ValueError("joint evidence requires one declared source-bearing geometry run")
    expected_tensor, expected_seed, expected_protocol = geometry.prepare_fixture(
        L=bundle.seed.L, steps=identity["steps"], direction=direction)
    if (expected_tensor.fingerprint != bundle.tensor.fingerprint
            or not expected_seed.same_as(bundle.seed)
            or canonical_bytes(protocol) != canonical_bytes(expected_protocol)):
        raise ValueError("chart protocol and complete seed differ from the declared prepared fixture")
    axis = next(i for i, value in enumerate(direction) if value)
    coordinate = protocol["receiver_coordinate"]
    xyz = [0, 0, 0]
    xyz[axis] = coordinate if direction[axis] > 0 else bundle.seed.L - 1 - coordinate
    receiver = bundle.seed.lattice.index(*xyz)
    oracle = acceptance.audit_saved_run(
        run_dir, protocol=protocol, out=None if out is None else Path(out) / "acceptance.json")
    _bound_report(oracle, identity, {
        "tensor_hash": "tensor_hash", "bundle_id": "bundle_id",
        "run_id": "run_id", "seed_hash": "seed_hash", "steps": "steps",
        "channels_per_node": "channels", "nodes": "nodes"})
    record_report = records.inspect_saved_run(
        run_dir, direction=direction, detector=receiver, allow_native_prefix=True)
    _bound_report(record_report, identity, {
        "tensor_hash": "tensor_hash", "bundle_id": "bundle_id", "run_id": "run_id"})
    local_checks, recoil_sites = 0, 0
    for before, after in zip(states, states[1:]):
        ledger = balance.source_transition_ledgers(before, after, bundle.tensor, direction=direction)
        for residual in ledger["residuals"].values():
            if bool((residual != 0).any()):
                raise ValueError("a local balance residual is nonzero")
            local_checks += residual.size
        recoil_sites += int((ledger["collision_delta"] != 0).sum())
    packet_states = [State(state.L, state.a[:8].copy(), state.b[:8].copy(), state.r[:8].copy())
                     for state in states]
    functional = [organization.functional_trace(
        packet_states, receiver=receiver, collision_phase=phase) for phase in (0, 1)]
    review = geometry_review.audit(
        None if out is None else Path(out) / "geometry-review.json",
        run_dir=run_dir, protocol=protocol)
    _bound_report(review["saved_chart"], identity, {
        "tensor_hash": "tensor_hash", "bundle_id": "bundle_id",
        "run_id": "run_id", "microsteps": "steps"})
    readouts = []
    for tick, state in enumerate(states):
        if tick % 2:
            continue
        value = geometry.readout(state, tick, protocol)
        fp, fm, plus, minus = geometry_review._profiles(
            geometry_review._plane_rows(state, direction))
        x = Fraction(protocol["interior_coordinate"])
        radius = (geometry_review._reconstruct(fp, x, geometry_review.cubic)
                  + geometry_review._reconstruct(fm, x, geometry_review.cubic))
        nplus = geometry_review._reconstruct(plus, x, geometry_review.hat)
        nminus = geometry_review._reconstruct(minus, x, geometry_review.hat)
        expected = {"macro_time": Fraction(tick, 2), "coordinate": x,
                    "R": radius, "n_plus": nplus, "n_minus": nminus,
                    "G_uu": nplus/radius, "G_vv": nminus/radius,
                    "other_Einstein_components": 0, "scalar_curvature": 0,
                    "energy_numerator": nplus+nminus, "momentum_numerator": nplus-nminus,
                    "dominant_energy_numerator": nplus+nminus-abs(nplus-nminus),
                    "source_curvature_residual": (Fraction(0), Fraction(0))}
        if value != expected:
            raise ValueError("candidate chart readout differs from independent reconstruction")
        readouts.append(geometry._json(value))
    claims = [
        ("independent_full_scalar_replay", "passed", oracle),
        ("retained_record_transport", "passed", record_report),
        ("positive_packet_balance", "passed", {
            "local_balance_residuals_checked": int(local_checks),
            "nonzero_species_recoil_sites": recoil_sites,
            "energy_assignment": "Boolean packet prefix only; no energy assigned to profile offsets"}),
        ("finite_repeat_use", "passed" if all(row["receiver_repeat_gate"] for row in functional)
         else "failed", {"collision_cohorts": functional, "finite_prepared_supply": True}),
        ("finite_null_source_chart", "passed", {
            "candidate_readouts": readouts, "independent_review": review,
            "scope": "restricted positive finite causal chart; even-tick macro correspondence"}),
        ("global_periodic_positive_source_chart", "failed", {
            "reason": "sum of a periodic second difference is zero; nonzero nonnegative source is impossible"}),
        ("massive_bound_body", "not_tested", {"reason": "no retained timelike bound-body construction"}),
        ("operational_proper_clock", "not_tested", {"reason": "no retained clock calibration"}),
        ("sustained_complexity_growth", "not_tested", {
            "reason": "finite prepared repeat-use is not sustained or universal complexity growth"}),
    ]
    evidence = [contracts.make_evidence(identity, claim, status, details)
                for claim, status, details in claims]
    joined = contracts.join_evidence(
        run_dir, evidence, required_claims=[claim for claim, _, _ in claims],
        source_paths=paths)
    result = {"schema": "universe24/local-unification/joint-evidence/1",
              "identity": identity, "evidence": evidence, "join": joined,
              "statuses": {claim: status for claim, status, _ in claims},
              "counts": {
                  "scalar_forward_inverse_register_comparisons": oracle["scalar_forward_inverse_register_comparisons"],
                  "independent_canonical_clicks": oracle["independent_canonical_clicks"],
                  "independent_source_constraints": oracle["ledger"]["interior_source_checks"],
                  "expanded_twelve_channel_comparisons": review["saved_chart"]["full_retained_scalar_comparisons"],
                  "local_balance_residuals_checked": int(local_checks),
                  "independent_rational_chart_readouts": review["saved_chart"]["independent_rational_metric_source_readouts"]},
              "created_inversion_record_steps": record_report["created_inversion_record_steps"],
              "physical_acceptance": "not_granted"}
    if out is not None:
        _write(Path(out) / "joint.json", result)
    return result


def collect(out, *, quick=False):
    """Execute all lanes and archive their evidence without combining counts."""
    directory = Path(out)
    if directory.exists() and (not directory.is_dir() or any(directory.iterdir())):
        raise ValueError("collection output must be a new or empty directory")
    directory.mkdir(parents=True, exist_ok=True)
    initial_sources = source_snapshot()
    _write(directory / "attempt.json", {
        "schema": "universe24/local-unification/attempt/1",
        "sources": initial_sources, "python": platform.python_version(),
        "quick": quick, "status": "running"})
    try:
        native_report = native.audit(directory / "native.json")
        balance_report = balance.audit(directory / "balance.json")
        records_report = records.audit(directory / "records")
        organization_report = organization.audit(directory / "organization", full_panel=not quick)
        panel = validate_panel(organization_report, full_panel=not quick)
        contracts_report = contracts.audit(directory / "contracts")
        geometry_report = geometry.audit(directory / "geometry")
        limits_report = limits.audit(directory / "limits.json")
        joint = inspect_joint_run(
            directory / "geometry/runtime", geometry_report["protocol"],
            source_paths=initial_sources, out=directory / "joint")
        if source_snapshot() != initial_sources:
            raise ValueError("implementation sources changed during collection")
        # Separate support reports are intentionally not assigned the main
        # run's law/seed identity. Overlapping comparison counts are not added.
        support = {
            "native": {"path": "native.json", "schema": native_report.get("schema")},
            "balance": {"path": "balance.json", "schema": balance_report.get("schema")},
            "records": {"path": "records/records.json", "schema": records_report.get("schema")},
            "organization": {"path": "organization/organization.json",
                             "coverage": panel,
                             "shared_receiver_repeat_passes": organization_report["shared_receiver_repeat_passes"],
                             "shared_bank_growth_outcomes": organization_report["shared_bank_growth_outcomes"]},
            "contracts": {"path": "contracts/contracts.json", "schema": contracts_report.get("schema")},
            "limits": {"path": "limits.json", "schema": limits_report.get("schema")},
        }
        _write(directory / "attempt.json", {
            "schema": "universe24/local-unification/attempt/1",
            "sources": initial_sources, "python": platform.python_version(),
            "quick": quick, "status": "completed"})
        artifacts = {str(path.relative_to(directory)): _sha(path)
                     for path in sorted(directory.rglob("*")) if path.is_file()}
        report = {
            "schema": "universe24/local-unification/collection/1",
            "sources": initial_sources, "python": platform.python_version(),
            "quick": quick, "main_identity": joint["identity"],
            "main_statuses": joint["statuses"],
            "main_counts": joint["counts"],
            "created_inversion_record_steps": joint["created_inversion_record_steps"],
            "supporting_reports": support, "artifacts": artifacts,
            "classification": {
                "proved": ["Boolean collision involution and exact packet balances",
                           "restricted null metric/source identities and spline reconstruction",
                           "positive periodic-source obstruction"],
                "finite_evidence": ["one saved twelve-channel history with retained records and source profile",
                                    "registered organization panel, including failures and blocked outcomes"],
                "failed": ["global nonzero positive periodic source in this metric chart"],
                "unproved": ["generic Einstein limit", "massive bound body", "operational proper clock",
                             "sustained complexity growth", "Born/Bell detector model"],
            },
            "physical_acceptance": "not_granted",
            "generic_runtime_acceptance_gates": "unchanged",
            "comparison_counts": "kept by report; overlapping checks are not added",
        }
        _write(directory / "collection.json", report)
        return report
    except Exception as exc:
        _write(directory / "failure.json", {
            "schema": "universe24/local-unification/collection-failure/1",
            "exception": type(exc).__name__, "reason": str(exc),
            "initial_sources": initial_sources, "physical_acceptance": "not_granted"})
        raise


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, default=Path("runs/local-unification"))
    parser.add_argument("--quick", action="store_true",
                        help="use the explicitly labelled nine-case organization subset")
    args = parser.parse_args(argv)
    report = collect(args.out, quick=args.quick)
    print(exact_json.dumps({
        "collection": str(args.out / "collection.json"),
        "run_id": report["main_identity"]["run_id"],
        "tensor_hash": report["main_identity"]["tensor_hash"],
        "bundle_id": report["main_identity"]["bundle_id"],
        "seed_hash": report["main_identity"]["seed_hash"],
        "source_manifest_hash": hashlib.sha256(canonical_bytes(report["sources"])).hexdigest(),
        "channels": report["main_identity"]["channels"],
        "steps": report["main_identity"]["steps"],
        "statuses": report["main_statuses"],
        "claim_status_counts": {
            status: list(report["main_statuses"].values()).count(status)
            for status in sorted(set(report["main_statuses"].values()))},
        "main_counts": report["main_counts"],
        "created_inversion_record_steps": report["created_inversion_record_steps"],
        "organization": report["supporting_reports"]["organization"],
        "physical_acceptance": report["physical_acceptance"]}, sort_keys=True))


if __name__ == "__main__":
    main()
