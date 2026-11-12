"""Execute proposal-composition rejection and causal-interface controls."""
from __future__ import annotations

import argparse
from fractions import Fraction
import hashlib
import json
from pathlib import Path
import tempfile

import numpy as np

from universe24.core import Engine, GearType, State, Tensor
from universe24.system.bundle import BundleError, create_bundle
from universe24.system.decoder import default_protocol
from universe24.system.runtime import run_bundle, verify_run
from validation.geometry.team48 import refinement_integer_projective as projective
from validation.geometry.team48 import temporal_repair_projective as temporal
from validation.synthesis.complexity_selection import tensor as comparison_tensor

BASE = "621fc1f55800e50e1db5f6a30ce24bb83716a49a"
ROOT = Path(__file__).resolve().parents[2]
ZERO = (0, 0, 0)


def terms(law):
    return [(law.names[m.target], m.coeff,
             [(law.names[f.gear], f.offset, f.field) for f in m.factors])
            for m in law.monomials]


def extend_seed(seed, additional):
    a = np.zeros((additional, seed.N), dtype=object)
    r = np.array([[n % 6 for n in range(seed.N)] for _ in range(additional)], dtype=object)
    return State(seed.L, np.vstack((seed.a, a)), np.vstack((seed.b, a)),
                 np.vstack((seed.r, r)))


def bundle(law, seed):
    channels = [{"index": i, "name": g.name, "label": g.label,
                 "owner": "integration-control", "purpose": "Scoped interface verification"}
                for i, g in enumerate(law.gears)]
    # Even deliberately grand metadata cannot certify physics.
    return create_bundle(law, seed, channels=channels, protocol=default_protocol(),
                         model={"id": "Einstein-and-Born", "version": "test-only",
                                "domain": "Off-constraint interface control; no physical claim"})


def audit():
    program = projective.compile_projective(temporal.NAMES, temporal.BUILDER,
                                            dt=Fraction(1, 8), dx=1, degree=3)
    seed = temporal.prepared(program, 64)
    phi = 1 + program.fields.index("phi")
    chi = 1 + program.fields.index("chi")
    receiver = GearType("audit.interface_intensity", label="audit")
    receiver_terms = [(receiver.name, 3, [(program.tensor.names[i], ZERO, "b")] * 2)
                      for i in (phi, chi)]
    law = Tensor([*program.tensor.gears, receiver],
                 terms(program.tensor) + receiver_terms, strict_support=True)
    initial = extend_seed(seed, 1)
    changed = initial.copy()
    changed.a[44] = np.array([n - 13 for n in range(27)], dtype=object)
    changed.b[44] = np.array([2*n + 1 for n in range(27)], dtype=object)
    changed.r[44] = np.array([(n + 1) % 6 for n in range(27)], dtype=object)
    feedback_terms = sum(m.target < 44 and any(f.gear >= 44 for f in m.factors)
                         for m in law.monomials)
    assert feedback_terms == 0
    engine = Engine(law)
    left, right = initial, changed
    for _ in range(3):
        left, right = engine.step(left), engine.step(right)
        assert State(3, left.a[:44], left.b[:44], left.r[:44]).same_as(
            State(3, right.a[:44], right.b[:44], right.r[:44]))
    assert engine.rewind(left, 3).same_as(initial)
    assert engine.rewind(right, 3).same_as(changed)

    # A legal feedback edge is detected and actually changes the source.
    # This is a mechanical positive control, not a physical force proposal.
    reciprocal_test = Tensor(law.gears, terms(law) + [
        (program.tensor.names[phi], 3, [(receiver.name, ZERO, "b")])],
        strict_support=True)
    feedback_engine = Engine(reciprocal_test)
    p, q = feedback_engine.step(initial), feedback_engine.step(changed)
    assert not np.array_equal(p.b[phi], q.b[phi])
    assert feedback_engine.inverse_step(p).same_as(initial)
    assert feedback_engine.inverse_step(q).same_as(changed)

    # The real independent comparison and receiver do not share a state bank.
    comparison = comparison_tensor()
    excess = Tensor([*law.gears, *comparison.gears], terms(law) + terms(comparison),
                    strict_support=True)
    rejected = ""
    try:
        bundle(excess, extend_seed(seed, 5))
    except BundleError as exc:
        rejected = str(exc)
    assert excess.G == 49 and "got 49" in rejected

    valid = bundle(law, initial)
    with tempfile.TemporaryDirectory(prefix="interface-control-", dir=ROOT / "runs") as folder:
        run_path = Path(folder) / "run"
        report = run_bundle(valid, run_path, 1)
        assert all(report["acceptance_gates"][gate]["status"] == "not_tested"
                   for gate in "CDEF")
        verified = verify_run(run_path)
        report_file = run_path / "validation.json"
        original = report_file.read_bytes()
        report["acceptance_gates"]["C"]["status"] = "passed"
        report_file.write_text(json.dumps(report))
        forged_rejected = ""
        try:
            verify_run(run_path)
        except ValueError as exc:
            forged_rejected = str(exc)
        finally:
            report_file.write_bytes(original)
        assert "disagrees" in forged_rejected
        assert verify_run(run_path) == verified

    paths = [Path(__file__), Path(projective.__file__), Path(temporal.__file__),
             ROOT / "validation/synthesis/complexity_selection.py",
             ROOT / "universe24/core/engine.py", ROOT / "universe24/core/tensor.py",
             ROOT / "universe24/system/bundle.py", ROOT / "universe24/system/runtime.py"]
    return {
        "status": "interface_controls_passed", "scope": "Actual tensor/bundle/runtime rejection and causal controls",
        "base_revision": BASE,
        "source_sha256": {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest() for p in paths},
        "command": "python -m validation.synthesis.interface_contract --out runs/synthesis/interface_contract.json",
        "source_channels": 44, "one_way_channels": law.G,
        "source_feedback_monomials": feedback_terms,
        "apparatus_history_intervention_source_equal_steps": 3,
        "positive_feedback_changes_source": True,
        "comparison_plus_receiver_channels": excess.G,
        "budget_rejection": rejected,
        "metadata_cannot_promote_physics": True,
        "forged_physics_report_rejection": forged_rejected,
        "tensor_sha256": law.fingerprint,
        "physical_acceptance": "not_established",
        "limits": ["No physical feedback/stress model is supplied by the positive mechanical control",
                   "Full saved-state denominator readouts are not click-only operational observations",
                   "Independent controls are not combined into an accepted physical tensor"],
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, default=Path("runs/synthesis/interface_contract.json"))
    args = parser.parse_args()
    (ROOT / "runs").mkdir(exist_ok=True)
    result = audit()
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
