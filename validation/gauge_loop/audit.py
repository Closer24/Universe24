"""Save and independently replay the finite-gauge loop controls.

Run ``python -m validation.gauge_loop.audit --out runs/gauge-loop``.
Separate tensors retain separate claims; their results are never pooled into
one physical construction. All state changes use the existing Engine.
"""
from __future__ import annotations

import argparse
import gzip
import hashlib
import json
from pathlib import Path

from universe24.core import Engine, State
from universe24.system.bundle import canonical_bytes, create_bundle
from universe24.system.decoder import default_protocol
from universe24.system.runtime import run_bundle, verify_run
from validation.system_smoke import scalar_step
from . import model


BASE_COMMIT = "b8a064a9b0cccb1218445578d8765642572b40a7"


def make_bundle(tensor, seed, *, identifier, domain):
    """Exhaustively count every link, history and reader in the public bundle."""
    return create_bundle(
        tensor, seed,
        channels=[{"index": i, "name": gear.name, "label": gear.label,
                   "owner": identifier,
                   "purpose": "retained finite-gauge research register; not a physical detector"}
                  for i, gear in enumerate(tensor.gears)],
        protocol=default_protocol(),
        model={"id": identifier, "version": "1", "domain": domain,
               "base_commit": BASE_COMMIT, "physical_acceptance": "not_established"})


def saved_states(directory):
    """Read actual saved transitions, after the production verifier succeeds."""
    verify_run(directory)
    states = []
    with gzip.open(Path(directory) / "full_trace.jsonl.gz", "rt", encoding="utf-8") as stream:
        for line in stream:
            record = json.loads(line)
            if not states:
                states.append(State.from_dict(record["before"]))
            states.append(State.from_dict(record["after"]))
    return states


def _require(condition, message):
    if not condition:
        raise AssertionError(message)


def _scalar_replay(tensor, states):
    comparisons = 0
    for before, after in zip(states, states[1:]):
        _require(scalar_step(tensor, before).same_as(after), "independent scalar replay failed")
        comparisons += 3 * before.G * before.N
    return comparisons


def static_runs(out):
    """Same static law, two real flux sectors and their complete gauge copies."""
    tensor = model.build_tensor()
    cases, histories = {}, {}
    compared = 0
    # Deterministic nonuniform phases exercise all four local rotations.
    phases = tuple((n * n + 3 * n + n // 3 + 1) % 4 for n in range(125))
    target = (1 * 5 + 1) * 5
    for flux in (1, -1):
        original = model.prepare_two_path(flux=flux)
        for transformed in (False, True):
            name = ("positive" if flux == 1 else "negative") + ("_gauge" if transformed else "")
            seed = model.gauge_transform(original, phases) if transformed else original
            bundle = make_bundle(tensor, seed, identifier="static-z4-loop",
                                 domain="Gaussian-unit stationary links; arbitrary integer matter; planar background control")
            directory = out / name
            execution = run_bundle(bundle, directory, 4)
            states = saved_states(directory)
            compared += _scalar_replay(tensor, states)
            for state in states:
                model.validate_static_domain(state)
                _require(model.plaquette(state) == (flux, 0), "static flux changed")
            expected = 4 if flux == 1 else 0
            _require(model.intensity(states[2], target) == expected, "two-path intensity failed")
            _require(model.receiver_quotient(states[2], states[3], target) == expected,
                     "retained receiver failed")
            _require(all(model.receiver_quotient(a, b, n) == model.intensity(a, n)
                         for a, b in zip(states, states[1:]) for n in range(a.N)),
                     "neutral receiver disagrees with independent intensity")
            cases[name] = {"bundle_id": bundle.bundle_id, "run_id": execution["run_id"],
                           "tensor_hash": tensor.fingerprint,
                           "flux": list(model.plaquette(seed)),
                           "target_intensity_at_step_2": expected,
                           "target_receiver_quotient_at_step_3": expected,
                           "maximum_integer_bits": max(execution["maximum_integer_bits_by_step"]),
                           "files": execution["files"], "complete_replay": "passed"}
            histories[name] = states
        plain = "positive" if flux == 1 else "negative"
        for left, right in zip(histories[plain], histories[plain + "_gauge"]):
            _require(model.gauge_transform(left, phases).same_as(right), "full-history gauge covariance failed")
            _require(all(model.intensity(left, n) == model.intensity(right, n)
                         for n in range(left.N)), "local intensity changed under gauge")
    # This unnormalized four-port recurrence is not a stable wave solver.
    # Its homogeneous mode q_next=4*q-q_previous grows from q_-1=q_0=1.
    uniform = model.prepare_two_path()
    uniform.a[model.PHI, :] = 1
    uniform.b[model.PHI, :] = 1
    growth = [1]
    for _ in range(3):
        uniform = Engine(tensor).step(uniform)
        growth.append(int(uniform.b[model.PHI, 0]))
    _require(growth == [1, 3, 11, 41], "homogeneous instability countercontrol changed")
    return {"status": "passed", "channels": tensor.G,
            "degree": max(term.degree for term in tensor.monomials),
            "strict_support_violations": len(tensor.support_violations()),
            "scalar_register_comparisons": compared, "saved_histories": cases,
            "gauge_group": "Z4, time-independent residual local transformations",
            "link_dynamics": "stationary prepared background",
            "homogeneous_matter_growth_control": growth,
            "stable_wave_dynamics": "failed: uniform mode has a root 2+sqrt(3)>1",
            "reader": "neutral one-way intensity register; not a Born detector",
            "probability_norm_conservation": "not_claimed"}


def source_hashes():
    """Bind the complete repository-owned Python dependency closure conservatively."""
    root = Path(__file__).resolve().parents[2]
    paths = sorted(path for prefix in ("universe24", "validation")
                   for path in (root / prefix).rglob("*.py")
                   if "tests" not in path.relative_to(root).parts)
    return {str(path.relative_to(root)): hashlib.sha256(path.read_bytes()).hexdigest() for path in paths}


def run(out):
    out = Path(out)
    if out.exists():
        raise FileExistsError("audit output must be a fresh directory")
    out.mkdir(parents=True)
    report = {"schema": "universe24/gauge-loop-audit/1", "base_commit": BASE_COMMIT,
              "scope": "separate finite-gauge constructions and falsification controls",
              "static_loop": static_runs(out / "static")}
    from .obstructions import obstruction_audit
    report["existing_law_countercontrols"] = obstruction_audit()
    # The dynamic law is separately named, hashed and executed below. Its
    # finite Z2 orbit does not supply the static Z4 wave's missing dynamics.
    from . import dynamic
    report["dynamic_connection"] = dynamic.dynamic_audit()
    dynamic_tensor = dynamic.build_tensor()
    dynamic_seed = dynamic.prepare_fixture()
    dynamic_bundle = make_bundle(dynamic_tensor, dynamic_seed, identifier="dynamic-z2-cycle",
                                 domain="prepared complete-history sign sector; periodic local matter-link cycle")
    execution = run_bundle(dynamic_bundle, out / "dynamic", 6)
    states = saved_states(out / "dynamic")
    comparisons = _scalar_replay(dynamic_tensor, states)
    for state in states:
        dynamic.validate_prepared_domain(state)
    _require(states[3].same_as(states[0]) and states[6].same_as(states[0]),
             "saved dynamic history lost its proved period")
    _require(any(dynamic.wilson_plaquettes(state) != dynamic.wilson_plaquettes(states[0])
                 for state in states[1:3]), "saved dynamic fixture has no changing loop")
    report["dynamic_saved_run"] = {"tensor_hash": dynamic_tensor.fingerprint,
                                   "bundle_id": dynamic_bundle.bundle_id,
                                   "run_id": execution["run_id"], "files": execution["files"],
                                   "steps": 6, "scalar_register_comparisons": comparisons,
                                   "maximum_integer_bits": max(execution["maximum_integer_bits_by_step"]),
                                   "complete_replay": "passed"}
    report["physical_gates"] = {
        "one_combined_wave_and_dynamic_link_law": "not_established",
        "continuous_u1_or_controlled_emergent_limit": "not_established",
        "electric_gauss_law_and_maxwell_propagation": "not_established",
        "shared_einstein_source_and_operational_clock": "not_established",
        "born_detector_or_complexity_growth": "not_established"}
    report["source_hashes"] = source_hashes()
    (out / "report.json").write_bytes(canonical_bytes(report) + b"\n")
    return report


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args(argv)
    report = run(args.out)
    print(json.dumps({key: value for key, value in report.items() if key != "source_hashes"}, indent=2))


if __name__ == "__main__":
    main()
