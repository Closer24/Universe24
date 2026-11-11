"""Independent mechanical audit of a supplied clock-link research bundle.

This module never calls Engine.step to compute an expected state, nor imports
the proposal's polynomial evaluator. Scalar coordinate arithmetic and the
serialized monomials provide the oracle. Physical gates remain separate.
"""
from __future__ import annotations

import argparse
import gzip
import hashlib
from pathlib import Path

import numpy as np

from universe24.core.engine import Engine, State
from universe24.core.tensor import Tensor
from universe24.core import exact_json
from universe24.system.bundle import load_bundle, validate_bundle
from universe24.system.decoder import decode_transition, make_transition
from universe24.system.runtime import run_bundle, verify_run


def _position(node, size):
    return node // (size * size), (node // size) % size, node % size


def _index(position, size):
    x, y, z = (v % size for v in position)
    return (x * size + y) * size + z


def scalar_step(tensor, state):
    """Literal independent fixed-six update of every retained integer."""
    size, count = state.L, state.G
    old = {key: getattr(state, key) for key in ("a", "b", "r")}
    next_a = np.asarray(state.b, dtype=object).copy()
    next_b = np.empty(next_a.shape, dtype=object)
    next_r = np.empty(next_a.shape, dtype=object)
    for node in range(size ** 3):
        position = _position(node, size)
        inputs = [0] * count
        for term in tensor.monomials:
            product = int(term.coeff)
            for factor in term.factors:
                other = _index(tuple(position[k] + factor.offset[k] for k in range(3)), size)
                product *= int(old[factor.field][factor.gear, other])
            inputs[term.target] += product
        for channel, value in enumerate(inputs):
            quotient, remainder = divmod(2 * value + int(old["r"][channel, node]), 6)
            next_b[channel, node] = quotient - int(old["a"][channel, node])
            next_r[channel, node] = remainder
    return State(size, next_a, next_b, next_r)


def structural_certificate(tensor):
    """Recompute support/degree/old-a acyclicity without Tensor's checkers."""
    if not 1 <= tensor.G <= 48:
        raise AssertionError("retained channel budget exceeded")
    dependencies = {channel: set() for channel in range(tensor.G)}
    degrees = [0, 0, 0, 0]
    for term in tensor.monomials:
        if type(term.coeff) is not int or len(term.factors) > 3:
            raise AssertionError("noninteger coefficient or excessive polynomial degree")
        degrees[len(term.factors)] += 1
        support = set()
        for channel, offset in [(term.target, (0, 0, 0))] + [
                (factor.gear, factor.offset) for factor in term.factors]:
            support.add(tuple(offset))
            axis = tensor.gears[channel].link
            if axis is not None:
                end = list(offset)
                end[axis] += 1
                support.add(tuple(end))
        if len(support) > 2:
            raise AssertionError("term touches more than one physical face")
        if len(support) == 2:
            first, second = tuple(support)
            if sum(abs(a - b) for a, b in zip(first, second)) != 1:
                raise AssertionError("non-face physical support")
        for factor in term.factors:
            if factor.field == "a":
                dependencies[term.target].add(factor.gear)
    completed, stages = set(), []
    while len(completed) < tensor.G:
        ready = sorted(channel for channel, inputs in dependencies.items()
                       if channel not in completed and inputs <= completed)
        if not ready:
            raise AssertionError("cyclic old-a dependencies")
        completed.update(ready)
        stages.append(ready)
    return {"channels": tensor.G, "retained_integers_per_node": 3 * tensor.G,
            "terms": len(tensor.monomials), "degree_counts": degrees,
            "strict_physical_support": "passed", "independent_inverse_stages": stages}


def _bits(state):
    return max(abs(int(value)).bit_length()
               for field in (state.a, state.b, state.r) for value in field.flat)


def synthetic_seed(channels, *, size=3, carry=0, huge=False):
    """Disclosed mechanical stress seed; no assertion of physical admissibility."""
    shape = (channels, size ** 3)
    a = np.array([((7 * g + 3 * n) % 7) - 3
                  for g in range(channels) for n in range(size ** 3)], dtype=object).reshape(shape)
    b = np.array([((11 * g + 5 * n) % 9) - 4
                  for g in range(channels) for n in range(size ** 3)], dtype=object).reshape(shape)
    r = np.full(shape, carry, dtype=object)
    if huge:
        a[0, 0], b[1 % channels, 1] = -(1 << 100), 1 << 109
    return State(size, a, b, r)


def compare_trajectory(tensor, seed, steps):
    engine = Engine(tensor)
    actual = expected = seed
    comparisons, bit_sizes = 0, [_bits(seed)]
    for step in range(1, steps + 1):
        prior = actual.copy()
        actual, expected = engine.step(actual), scalar_step(tensor, expected)
        if not actual.same_as(expected):
            raise AssertionError(f"independent full-state oracle mismatch at {step}")
        if not engine.inverse_step(actual).same_as(prior):
            raise AssertionError(f"step inverse mismatch at {step}")
        comparisons += 3 * seed.G * seed.N
        bit_sizes.append(_bits(actual))
    if not engine.rewind(actual, steps).same_as(seed):
        raise AssertionError("complete rewind mismatch")
    return {"steps": steps, "retained_integer_comparisons": comparisons,
            "maximum_integer_bits_by_step": bit_sizes,
            "independent_scalar_oracle": "passed", "complete_rewind": "passed"}


def causal_audit(tensor, *, size=3, steps=2):
    """Perturb every channel in each retained bank; check complete-state cones."""
    seed = synthetic_seed(tensor.G, size=size, carry=3)
    engine = Engine(tensor)
    reference = [seed]
    for _ in range(steps):
        reference.append(engine.step(reference[-1]))
    origins = [(0, 0, 0)]
    for axis in range(3):
        for direction in (1, -1):
            point = [0, 0, 0]
            point[axis] = direction % size
            origins.append(tuple(point))
    observations, checks = [], 0
    for origin in origins:
        source = _index(origin, size)
        for field in ("a", "b", "r"):
            changed = seed.copy()
            array = getattr(changed, field)
            for channel in range(tensor.G):
                array[channel, source] = ((int(array[channel, source]) + 1) % 6
                                          if field == "r" else int(array[channel, source]) + 1)
            for step in range(1, steps + 1):
                changed = engine.step(changed)
                affected = set()
                for node in range(seed.N):
                    position = _position(node, size)
                    distance = sum(min((position[k] - origin[k]) % size,
                                       (origin[k] - position[k]) % size) for k in range(3))
                    for bank in ("a", "b", "r"):
                        actual, expected = getattr(changed, bank)[:, node], getattr(reference[step], bank)[:, node]
                        if not np.array_equal(actual, expected):
                            affected.add(node)
                        if distance > step:
                            checks += tensor.G
                            if not np.array_equal(actual, expected):
                                raise AssertionError("complete retained state escaped its face causal cone")
                observations.append({"origin": list(origin), "bank": field, "step": step,
                                     "affected_nodes": len(affected)})
    return {"perturbations": 3 * len(origins), "steps_per_perturbation": steps,
            "retained_integer_outside_cone_checks": checks,
            "six_face_directions_and_periodic_seams": "passed",
            "complete_state_causal_bound": "passed", "observations": observations,
            "scope": "computational face-edge cone; not a physical metric light cone"}


def passive_audit(tensor, seed):
    engine = Engine(tensor)
    before, after = seed.copy(), engine.step(seed)
    first, second = before.copy(), after.copy()
    data_before = tensor.to_dict()
    record = make_transition(tensor, before, after, run_id="independent-clock-link-audit", step=1)
    events = decode_transition(record, tensor)
    # Independently compute event membership and coarse arithmetic attributes.
    expected = []
    for node in range(seed.N):
        for channel in range(seed.G):
            old = tuple(int(getattr(before, f)[channel, node]) for f in ("a", "b", "r"))
            new = tuple(int(getattr(after, f)[channel, node]) for f in ("a", "b", "r"))
            quotient = new[1] + old[0]
            if quotient == 0 or old == new:
                continue
            delta = (new[2] - old[2]) % 6
            kind = ("C0" if delta in (0, 3) else "C1" if delta in (1, 2) else "C2")
            expected.append((node, channel, quotient, kind))
    observed = [(event["node"], event["channel"], event["quotient"], event["kind"]) for event in events]
    if observed != expected:
        raise AssertionError("independent click membership/weight/class mismatch")
    if not before.same_as(first) or not after.same_as(second) or tensor.to_dict() != data_before:
        raise AssertionError("observer mutated retained state or law")
    return {"events": len(events), "independent_arithmetic_event_match": "passed",
            "state_and_tensor_passivity": "passed", "physical_measurement": "not_tested"}


def base_independence(bundle, steps=3):
    """Verify the original law and record the absence of complexity feedback."""
    count = bundle.model.get("base_channels")
    if type(count) is not int or not 1 <= count < bundle.tensor.G:
        return {"status": "not_tested", "reason": "no declared base/apparatus split"}
    terms = [term for term in bundle.tensor.monomials if term.target < count]
    if any(factor.gear >= count for term in terms for factor in term.factors):
        raise AssertionError("claimed one-way apparatus feeds back into original channels")
    designations = [(target, factors, why)
                    for (target, factors), why in bundle.tensor.designations.items() if target < count]
    source = Tensor(bundle.tensor.gears[:count], terms,
                    designated_one_way=designations, strict_support=True)
    if source.fingerprint != bundle.model.get("base_tensor_hash"):
        raise AssertionError("original base law changed in the extension")
    def project(state):
        return State(state.L, *(getattr(state, field)[:count].copy() for field in ("a", "b", "r")))
    seed = bundle.seed
    changed = seed.copy()
    for field in ("a", "b", "r"):
        array = getattr(changed, field)
        for channel in range(count, changed.G):
            for node in range(changed.N):
                value = int(array[channel, node]) + 17 + channel + node
                array[channel, node] = value % 6 if field == "r" else value
    original, altered, expected = seed, changed, project(seed)
    engine = Engine(bundle.tensor)
    for _ in range(steps):
        original, altered = engine.step(original), engine.step(altered)
        expected = scalar_step(source, expected)
        if not project(original).same_as(expected) or not project(altered).same_as(expected):
            raise AssertionError("base states changed under apparatus preparation")
    return {"status": "passed", "base_channels": count, "steps": steps,
            "original_tensor_hash_verified": source.fingerprint,
            "retained_source_integer_comparisons": steps * 3 * count * seed.N * 2,
            "arbitrary_apparatus_history_cannot_change_source": True,
            "complexity_selection": "blocked: no apparatus-to-carrier dependency in this tensor",
            "apparatus_backreaction": "absent by construction"}


def audit(bundle, out, *, steps=3):
    bundle = load_bundle(bundle) if isinstance(bundle, (str, Path)) else validate_bundle(bundle)
    out = Path(out)
    if out.exists() and any(out.iterdir()):
        raise ValueError("audit output must be new or empty")
    out.mkdir(parents=True, exist_ok=True)
    certificate = structural_certificate(bundle.tensor)
    trajectories = {"supplied_seed": compare_trajectory(bundle.tensor, bundle.seed, steps)}
    for carry in range(6):
        trajectories[f"mechanical_carry_{carry}"] = compare_trajectory(
            bundle.tensor, synthetic_seed(bundle.tensor.G, carry=carry, huge=carry == 5), 2)
    cones = causal_audit(bundle.tensor)
    passive = passive_audit(bundle.tensor, bundle.seed)
    independence = base_independence(bundle, steps)
    run = run_bundle(bundle, out / "run", steps)
    if verify_run(out / "run") != run:
        raise AssertionError("saved replay changed its report")
    count = 0
    with gzip.open(out / "run" / "full_trace.jsonl.gz", "rt", encoding="utf-8") as stream:
        for line in stream:
            transition = exact_json.loads(line)
            before, after = (State.from_dict(transition[key]) for key in ("before", "after"))
            if not scalar_step(bundle.tensor, before).same_as(after):
                raise AssertionError("saved trace fails independent scalar oracle")
            count += 1
    if count != steps:
        raise AssertionError("saved trace step count mismatch")
    report = {"schema": "universe24/clock-links/independent-acceptance/1",
              "bundle_id": bundle.bundle_id, "tensor_hash": bundle.tensor.fingerprint,
              "certificate": certificate, "trajectories": trajectories,
              "causality": cones, "observation": passive,
              "source_independence": independence,
              "saved_run": {"run_id": run["run_id"], "steps": steps,
                            "saved_scalar_oracle": "passed", "complete_replay": "passed",
                            "canonical_clicks": run["click_count"]},
              "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              "physical_gates": {
                  "einstein_constraints": "not_tested",
                  "metric_calibrated_material_clocks": "not_tested",
                  "apparatus_backreaction": "absent_by_construction" if independence.get("status") == "passed" else "not_tested",
                  "complexity_selected_growth": "blocked_no_apparatus_feedback" if independence.get("status") == "passed" else "not_tested",
                  "derived_born_probability": "not_tested",
                  "complete_trial_bell_violation": "not_tested"},
              "interpretation": "Mechanical acceptance of the supplied finite run; synthetic stresses are not physically constrained seeds."}
    (out / "acceptance.json").write_text(exact_json.dumps(report, sort_keys=True) + "\n", encoding="utf-8")
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--bundle", required=True, type=Path)
    parser.add_argument("--out", default=Path("runs/clock_links/acceptance"), type=Path)
    parser.add_argument("--steps", default=3, type=int)
    args = parser.parse_args()
    result = audit(args.bundle, args.out, steps=args.steps)
    print(exact_json.dumps({"bundle_id": result["bundle_id"], "certificate": result["certificate"],
                            "saved_run": result["saved_run"], "physical_gates": result["physical_gates"]}))


if __name__ == "__main__":
    main()
