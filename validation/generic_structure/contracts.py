"""Research observation joins over the existing verified SystemBundle runtime.

This is not a replacement bundle validator or a physical-proof checker. It binds
*interpretations and observation windows* to a replay-verified run. A matching
receipt permits comparison; it cannot promote an Einstein or clock claim.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass, replace
from enum import Enum
from fractions import Fraction
import hashlib
import json
from pathlib import Path
import tempfile

from universe24.system.bundle import canonical_bytes, load_bundle
from universe24.system.runtime import run_bundle, verify_run


class InputKind(str, Enum):
    FULL_STATE = "full_state_diagnostic"
    ARITHMETIC_CLICKS = "canonical_arithmetic_records"


@dataclass(frozen=True)
class Interpretation:
    """A declared semantic contract, NOT a theorem that these semantics hold."""
    representation: str
    metric_rule: str
    metric_channels: tuple[str, ...]
    denominator_channel: str
    physical_time_per_microtick: Fraction
    spatial_step: Fraction
    coordinate_convention: str
    domain: str

    def payload(self):
        if not all(type(x) is str and x for x in
                   (self.representation, self.metric_rule, self.denominator_channel,
                    self.coordinate_convention, self.domain)):
            raise ValueError("Interpretation needs explicit representation, metric, gauge and domain")
        if (type(self.physical_time_per_microtick) is not Fraction
                or type(self.spatial_step) is not Fraction
                or self.physical_time_per_microtick <= 0 or self.spatial_step <= 0):
            raise ValueError("Physical scales must be positive exact Fractions")
        if (type(self.metric_channels) is not tuple or len(self.metric_channels) != 9
                or len(set(self.metric_channels)) != 9
                or any(type(x) is not str or not x for x in self.metric_channels)):
            raise ValueError("The full-frame interpretation requires nine distinct retained frame names")
        data = asdict(self)
        data["physical_time_per_microtick"] = str(self.physical_time_per_microtick)
        data["spatial_step"] = str(self.spatial_step)
        return data


@dataclass(frozen=True)
class Observation:
    """Typed input provenance. A diagnostic never becomes click-only by relabeling."""
    quantity: str
    input_kind: InputKind
    retained_dependencies: tuple[str, ...]
    start_step: int
    stop_step: int


@dataclass(frozen=True)
class Receipt:
    run_id: str
    bundle_id: str
    tensor_sha256: str
    seed_sha256: str
    full_trace_sha256: str
    click_trace_sha256: str
    interpretation_sha256: str
    start_step: int
    stop_step: int
    quantity: str
    input_kind: str
    dependencies: tuple[str, ...]


def digest(data):
    return hashlib.sha256(canonical_bytes(data)).hexdigest()


def bind_observation(run_path, interpretation: Interpretation,
                     observation: Observation) -> Receipt:
    """Re-use actual runtime replay; do not accept a caller's 'verified' boolean.

    Source-code identity/authorship and the mathematical validity of the
    interpretation require separate evidence. No arbitrary reader is executed.
    """
    path = Path(run_path)
    report = verify_run(path)
    bundle = load_bundle(path / "bundle")
    description = interpretation.payload()
    if any(name not in bundle.tensor.names for name in
           interpretation.metric_channels + (interpretation.denominator_channel,)):
        raise ValueError("Interpretation references a field outside the actual allocation")
    if (type(observation.start_step) is not int or type(observation.stop_step) is not int
            or not 0 <= observation.start_step < observation.stop_step <= report["steps"]):
        raise ValueError("Observation must identify a nonempty interval within the verified run")
    if type(observation.quantity) is not str or not observation.quantity:
        raise ValueError("Observation quantity must be explicit")
    if type(observation.input_kind) is not InputKind:
        raise ValueError("Observation input authority must be a typed InputKind")
    dependencies = observation.retained_dependencies
    if (type(dependencies) is not tuple or len(set(dependencies)) != len(dependencies)
            or any(name not in bundle.tensor.names for name in dependencies)):
        raise ValueError("Observation reads an unknown or duplicated retained dependency")
    if observation.input_kind is InputKind.ARITHMETIC_CLICKS and dependencies:
        raise ValueError("A records-only observation cannot read hidden retained state")
    if observation.input_kind is InputKind.FULL_STATE and not dependencies:
        raise ValueError("A state diagnostic must list its retained input fields")
    return Receipt(report["run_id"], bundle.bundle_id, bundle.tensor.fingerprint,
        digest(bundle.seed.to_dict()), report["files"]["full_trace.jsonl.gz"],
        report["files"]["clicks.jsonl.gz"], digest(description),
        observation.start_step, observation.stop_step, observation.quantity,
        observation.input_kind.value, dependencies)


def join_observations(left: Receipt, right: Receipt):
    """Require exact same-run/window/interpretation provenance for comparison.

    Different quantities can be compared (e.g. phase and metric). Different
    interpretations require a separately executed equivalence adapter, not an
    ignored mismatch. No theorem or physical acceptance is returned here.
    """
    keys = ("tensor_sha256", "seed_sha256", "bundle_id", "run_id",
            "full_trace_sha256", "click_trace_sha256", "interpretation_sha256",
            "start_step", "stop_step")
    mismatches = [key for key in keys if getattr(left, key) != getattr(right, key)]
    if mismatches:
        raise ValueError("Incompatible observation join: " + ", ".join(mismatches))
    return {"compatibility": "same_verified_run_window_and_declared_interpretation",
            "quantities": [left.quantity, right.quantity],
            "input_kinds": [left.input_kind, right.input_kind],
            "physical_acceptance": "not_established"}


def allocation_delta(base_names, additional_names):
    """An append ledger, not a compiler, alias proof or allocation reservation."""
    base, extra = tuple(base_names), tuple(additional_names)
    if (not all(type(x) is str and x for x in base + extra)
            or len(set(base)) != len(base) or len(set(extra)) != len(extra)):
        raise ValueError("Retained owners must have unique nonempty names")
    if set(base) & set(extra):
        raise ValueError("Reusing a name is not a proved reversible shared encoding")
    total = len(base) + len(extra)
    if total > 48:
        raise ValueError(f"Joint append allocation has {total} retained triples, above 48")
    return {"channels": total, "retained_integers_per_node": 3 * total,
            "append_budget_only": True, "coupled_tensor_exists": "not_established"}


def audit(out):
    """Actual common45 observation join plus meaningful incompatible controls."""
    from validation.completion import common45
    from universe24.system.bundle import create_bundle
    program = common45.build45()
    seed = common45.weak_seed(program)
    bundle = common45.make_bundle(program, seed)
    root = Path(out)
    root.mkdir(parents=True, exist_ok=True)
    directory = Path(tempfile.mkdtemp(prefix="contracts-", dir=root))
    path = directory / "common45"
    run_bundle(bundle, path, 2)
    meaning = Interpretation("current_projective_ratios", "gamma_inverse=B.T*B",
        tuple("projective.B" + str(a) + str(i) for a in range(3) for i in range(3)),
        "projective.D", program.dt, program.dx, "synchronous lapse=1 shift=0",
        "homogeneous weak constrained initial slice; later constraints are not asserted")
    # The actual denominator name is authoritative, not a guessed naming convention.
    meaning = replace(meaning, denominator_channel=program.tensor.names[0])
    metric_spec = Observation("inverse_spatial_metric", InputKind.FULL_STATE,
                             meaning.metric_channels + (meaning.denominator_channel,), 0, 2)
    clock_spec = Observation("scalar_I_S", InputKind.FULL_STATE,
        tuple("projective." + x for x in ("phi", "chi", "Pi_phi", "Pi_chi"))
        + (meaning.denominator_channel,), 0, 2)
    metric = bind_observation(path, meaning, metric_spec)
    clock = bind_observation(path, meaning, clock_spec)
    result = join_observations(metric, clock)
    rejected = []

    def reject(name, function):
        try:
            function()
        except ValueError:
            rejected.append(name)
        else:
            raise AssertionError(name + " unexpectedly accepted")

    for name, altered in (
        ("different_physical_tick_scale", replace(meaning, physical_time_per_microtick=2*program.dt)),
        ("scheduler_relabelled_as_metric_clock", replace(meaning, representation="scheduler_as_proper_clock")),
        ("different_frame_order", replace(meaning, metric_channels=meaning.metric_channels[::-1])),
        ("different_invariant_domain", replace(meaning, domain="all retained histories")),
    ):
        other = bind_observation(path, altered, clock_spec)
        reject(name, lambda other=other: join_observations(metric, other))
    shorter = bind_observation(path, meaning, replace(clock_spec, stop_step=1))
    reject("different_comparison_window", lambda: join_observations(metric, shorter))
    reject("hidden_state_under_records_only_label", lambda: bind_observation(path, meaning,
           replace(clock_spec, input_kind=InputKind.ARITHMETIC_CLICKS)))
    massless = common45.build45(mass_squared=0)
    massless_bundle = create_bundle(massless.tensor, common45.weak_seed(massless),
        channels=common45.channel_manifest(massless), protocol=bundle.protocol,
        model={"id": "contract-negative-control", "version": "1", "domain": "massless control"})
    other_path = directory / "massless"
    run_bundle(massless_bundle, other_path, 2)
    other = bind_observation(other_path, meaning, clock_spec)
    reject("actual_massless_tensor_join", lambda: join_observations(metric, other))
    changed_seed = seed.copy()
    changed_seed.r[0, 0] = (int(changed_seed.r[0, 0]) + 1) % 6
    changed_bundle = create_bundle(program.tensor, changed_seed,
        channels=common45.channel_manifest(program), protocol=bundle.protocol, model=bundle.model)
    changed_path = directory / "different-carry"
    run_bundle(changed_bundle, changed_path, 2)
    changed = bind_observation(changed_path, meaning, clock_spec)
    reject("actual_different_complete_preparation", lambda: join_observations(metric, changed))
    reject("45_plus_4", lambda: allocation_delta(program.tensor.names, ("q", "p", "record", "clock")))
    reject("duplicate_slot_claim", lambda: allocation_delta(program.tensor.names, (program.tensor.names[1],)))
    budget = allocation_delta(program.tensor.names, ("q", "p", "record"))
    output = {"status": "passed_compatibility_controls_only", "same_run_join": result,
        "metric_receipt": asdict(metric), "clock_receipt": asdict(clock),
        "rejected_controls": rejected, "hypothetical_45_plus_3": budget,
        "verified_runs": [str(path), str(other_path), str(changed_path)],
        "limitations": ["Declared semantics are not independently proved by a hash.",
                        "No physical gate or invariant-domain theorem is certified.",
                        "Equal provenance permits comparison; it does not imply equal observables."]}
    (root / "06_contracts.json").write_text(json.dumps(output, indent=2) + "\n")
    return output


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", default="runs/generic_structure/contracts")
    answer = audit(parser.parse_args().out)
    print(json.dumps({"status": answer["status"],
                      "rejected_controls": answer["rejected_controls"]}, indent=2))
