"""Same-law allocation, orientation and evidence checks for local unification.

These checks certify a declared mechanical interface.  They neither infer a
physical source from a channel name nor turn a passed audit into Einstein
acceptance.  Dependency paths are necessary structural conditions; finite
interventions and physical identities remain independent obligations.
"""
from __future__ import annotations

import argparse
import hashlib
import itertools
from pathlib import Path, PurePosixPath

import numpy as np

from universe24.core import Engine, State, Tensor
from universe24.core import exact_json
from universe24.system.bundle import canonical_bytes, load_bundle
from universe24.system.runtime import verify_run


IDENTITY_SCHEMA = "universe24/local-unification/run-identity/1"
EVIDENCE_SCHEMA = "universe24/local-unification/scoped-evidence/1"
_IDENTITY_KEYS = {"schema", "run_id", "bundle_id", "tensor_hash", "seed_hash",
                  "steps", "nodes", "channels", "trace_hash", "click_hash", "sources"}
_STATUSES = {"passed", "failed", "not_tested", "blocked"}
ROOT = Path(__file__).resolve().parents[2]


def _text(value, name):
    if type(value) is not str or not value.strip():
        raise ValueError(f"{name} must be a nonempty string")
    return value


def _integer(value, name, minimum=0):
    if type(value) is not int or value < minimum:
        raise ValueError(f"{name} must be an exact integer >= {minimum}")
    return value


def _hash(value):
    return hashlib.sha256(canonical_bytes(value)).hexdigest()


def _sha(value, name):
    if (type(value) is not str or len(value) != 64
            or any(c not in "0123456789abcdef" for c in value)):
        raise ValueError(f"{name} must be a lowercase SHA256 digest")
    return value


def allocation(tensor, roles, required_paths=()):
    """Check exclusive ownership and required directed coefficient dependencies.

    ``roles`` maps each exclusive owner role to its complete channel indices.
    A path reports possible algebraic influence only.  A constant preparation
    can make such influence inactive, so this never substitutes for a causal
    intervention.  A disconnected direct sum fails any cross-block claim.
    """
    if not isinstance(tensor, Tensor):
        raise ValueError("expected a Tensor")
    checked = Tensor.from_dict(tensor.to_dict(), strict_support=True)
    if not 1 <= checked.G <= 48:
        raise ValueError("at most48 total retained channels are allowed")
    if type(roles) is not dict or not roles:
        raise ValueError("provide an exhaustive ownership mapping")
    owners = {}
    for role, channels in roles.items():
        _text(role, "role")
        if type(channels) not in (list, tuple) or not channels:
            raise ValueError("every role must own at least one complete channel")
        for channel in channels:
            _integer(channel, "channel")
            if channel >= checked.G or channel in owners:
                raise ValueError("channel ownership must be unique and in range")
            owners[channel] = role
    if set(owners) != set(range(checked.G)):
        raise ValueError("every retained channel needs exactly one owner")
    graph = {channel: set() for channel in range(checked.G)}
    for term in checked.monomials:
        for factor in term.factors:
            graph[factor.gear].add(term.target)
    if type(required_paths) not in (list, tuple):
        raise ValueError("required_paths must be a list or tuple")
    paths = []
    seen = set()
    for pair in required_paths:
        if (type(pair) not in (tuple, list) or len(pair) != 2
                or any(type(role) is not str or role not in roles for role in pair)):
            raise ValueError("each required path must name two owned roles")
        source, target = pair
        if source == target or (source, target) in seen:
            raise ValueError("required role paths must be distinct nontrivial pairs")
        seen.add((source, target))
        reached = {channel: [channel] for channel in roles[source]}
        pending = list(reached)
        while pending:
            channel = pending.pop(0)
            for neighbour in sorted(graph[channel]):
                if neighbour not in reached:
                    reached[neighbour] = reached[channel] + [neighbour]
                    pending.append(neighbour)
        destinations = sorted(set(roles[target]) & set(reached))
        if not destinations:
            raise ValueError(f"disconnected claimed dependency {source}->{target}")
        paths.append({"source": source, "target": target,
                      "channel_path": reached[destinations[0]]})
    return {"tensor_hash": checked.fingerprint, "channels": checked.G,
            "retained_integers_per_node": 3 * checked.G,
            "degree": checked.rank - 1,
            "strict_support_violations": len(checked.support_violations()),
            "inverse_stages": [list(stage) for stage in checked.stages],
            "roles": {role: list(channels) for role, channels in roles.items()},
            "required_paths": paths,
            "path_scope": "possible coefficient influence; not an active-state or physical proof"}


def signed_permutations():
    """The48 exact signed permutation matrices, including24 reflections."""
    result = []
    for permutation in itertools.permutations(range(3)):
        for signs in itertools.product((-1, 1), repeat=3):
            result.append(tuple(tuple(signs[row] if column == permutation[row] else 0
                                      for column in range(3)) for row in range(3)))
    return tuple(result)


def _matrix(matrix):
    if (type(matrix) not in (tuple, list) or len(matrix) != 3
            or any(type(row) not in (tuple, list) or len(row) != 3 for row in matrix)
            or any(type(value) is not int or value not in (-1, 0, 1)
                   for row in matrix for value in row)):
        raise ValueError("expected an exact signed permutation matrix")
    matrix = tuple(tuple(row) for row in matrix)
    if (any(sum(abs(value) for value in row) != 1 for row in matrix)
            or any(sum(abs(matrix[row][column]) for row in range(3)) != 1
                   for column in range(3))):
        raise ValueError("expected an exact signed permutation matrix")
    return matrix


def transform_direction(direction, matrix):
    matrix = _matrix(matrix)
    if (type(direction) not in (tuple, list) or len(direction) != 3
            or any(type(value) is not int for value in direction)):
        raise ValueError("direction must contain three exact integers")
    return tuple(sum(matrix[row][column] * direction[column] for column in range(3))
                 for row in range(3))


def transform_tensor(tensor, matrix):
    """Transform spatial offsets of node-valued channels with trivial role action.

    Link metadata and intrinsic vector/spinor channel representations are not
    silently treated as scalars.  The native record/carrier plus/minus labels
    are roles relative to transformed direction parameters, not lab components.
    """
    matrix = _matrix(matrix)
    if not isinstance(tensor, Tensor) or any(gear.link is not None for gear in tensor.gears):
        raise ValueError("this action is defined only for node-valued channel roles")
    if tensor.designations:
        raise ValueError("this source-only transform does not transform designation metadata")
    terms = [(term.target, term.coeff,
              [(factor.gear, transform_direction(factor.offset, matrix), factor.field)
               for factor in term.factors]) for term in tensor.monomials]
    return Tensor(tensor.gears, terms, strict_support=True)


def transform_state(state, matrix):
    """Move every retained a,b,r entry by x->R*x on the periodic cube."""
    matrix = _matrix(matrix)
    if not isinstance(state, State):
        raise ValueError("expected a complete State")
    # Revalidate mutable arrays before indexing or serialising them.
    state = State(state.L, state.a, state.b, state.r)
    destinations = [state.lattice.index(*transform_direction(state.lattice.coords(node), matrix))
                    for node in range(state.N)]
    arrays = []
    for field in (state.a, state.b, state.r):
        transformed = np.empty_like(field)
        transformed[:, destinations] = field
        arrays.append(transformed)
    return State(state.L, *arrays)


def covariance(tensor, state, matrix):
    """Check one exact forward/inverse coordinate-covariance instance."""
    moved_tensor = transform_tensor(tensor, matrix)
    moved_state = transform_state(state, matrix)
    actual = Engine(moved_tensor).step(moved_state)
    expected = transform_state(Engine(tensor).step(state), matrix)
    if not actual.same_as(expected):
        raise ValueError("forward coordinate covariance failed")
    if not Engine(moved_tensor).inverse_step(actual).same_as(moved_state):
        raise ValueError("inverse covariance failed")
    return moved_tensor


def _sources(source_paths, source_root):
    if type(source_paths) not in (list, tuple) or not source_paths:
        raise ValueError("declare the nonempty exact implementation source set")
    source_root = ROOT if source_root is None else Path(source_root).resolve()
    result = {}
    for relative in source_paths:
        _text(relative, "source path")
        rel = PurePosixPath(relative)
        if rel.is_absolute() or ".." in rel.parts or str(rel) != relative or relative in result:
            raise ValueError("source names must be distinct canonical relative paths")
        path = source_root.joinpath(*rel.parts)
        if path.is_symlink() or not path.is_file() or not path.resolve().is_relative_to(source_root):
            raise ValueError("source must be an existing file inside the declared source root")
        result[relative] = hashlib.sha256(path.read_bytes()).hexdigest()
    return result


def run_identity(run_dir, *, source_paths, source_root=None):
    """Reexecute saved inputs and bind a scope to the exact current sources."""
    report = verify_run(run_dir)
    bundle = load_bundle(Path(run_dir) / "bundle")
    return {"schema": IDENTITY_SCHEMA, "run_id": report["run_id"],
            "bundle_id": bundle.bundle_id, "tensor_hash": bundle.tensor.fingerprint,
            "seed_hash": _hash(bundle.seed.to_dict()), "steps": report["steps"],
            "nodes": bundle.seed.N, "channels": bundle.tensor.G,
            "trace_hash": report["files"]["full_trace.jsonl.gz"],
            "click_hash": report["files"]["clicks.jsonl.gz"],
            "sources": _sources(source_paths, source_root)}


def _identity(identity):
    if type(identity) is not dict or set(identity) != _IDENTITY_KEYS:
        raise ValueError("complete run identity is required")
    if identity["schema"] != IDENTITY_SCHEMA:
        raise ValueError("unsupported run identity schema")
    for name in ("run_id", "bundle_id", "tensor_hash", "seed_hash", "trace_hash", "click_hash"):
        _sha(identity[name], name)
    for name in ("steps", "nodes", "channels"):
        _integer(identity[name], name, 0 if name == "steps" else 1)
    if identity["channels"] > 48:
        raise ValueError("identity exceeds total channel budget")
    if type(identity["sources"]) is not dict or not identity["sources"]:
        raise ValueError("identity needs implementation source hashes")
    for path, digest in identity["sources"].items():
        _text(path, "source path")
        _sha(digest, "source digest")
    canonical_bytes(identity)
    return identity


def make_evidence(identity, claim, status, details):
    """Attach a scoped claim; this does not verify its scientific content."""
    _identity(identity)
    _text(claim, "claim")
    if type(status) is not str or status not in _STATUSES:
        raise ValueError("use passed, failed, not_tested or blocked explicitly")
    if type(details) is not dict:
        raise ValueError("details must be explicit exact JSON data")
    result = {"schema": EVIDENCE_SCHEMA, "identity": identity, "claim": claim,
              "status": status, "details": details}
    # Round-trip both verifies exact JSON and removes aliases to mutable inputs.
    return exact_json.loads(canonical_bytes(result))


def join_evidence(run_dir, records, *, required_claims, source_paths, source_root=None):
    """Reject mixed tensor/seed/run/horizon/source reports; retain failed gates.

    Matching identities is necessary for a combined experiment, not sufficient
    evidence that any claim is true.  The returned object deliberately grants
    no physical acceptance; independent oracles must evaluate each detail.
    """
    expected = run_identity(run_dir, source_paths=source_paths, source_root=source_root)
    if type(required_claims) not in (tuple, list) or not required_claims:
        raise ValueError("name every required claim before collecting evidence")
    for claim in required_claims:
        _text(claim, "required claim")
    if len(set(required_claims)) != len(required_claims):
        raise ValueError("required claims must be unique")
    if type(records) not in (tuple, list):
        raise ValueError("records must be a complete list")
    joined = {}
    for record in records:
        if (type(record) is not dict
                or set(record) != {"schema", "identity", "claim", "status", "details"}
                or record["schema"] != EVIDENCE_SCHEMA):
            raise ValueError("malformed scoped evidence record")
        validated = make_evidence(record["identity"], record["claim"], record["status"], record["details"])
        if canonical_bytes(validated["identity"]) != canonical_bytes(expected):
            raise ValueError("cross-law, cross-seed, horizon, trace or stale-source evidence join")
        claim = validated["claim"]
        if claim in joined or claim not in required_claims:
            raise ValueError("duplicate or undeclared claim")
        joined[claim] = validated
    if set(joined) != set(required_claims):
        raise ValueError("required evidence is missing")
    return {"identity": expected, "claims": [joined[claim] for claim in required_claims],
            "identity_join": "passed", "physical_acceptance": "not_granted"}


def audit(out):
    """Run the final native law's orientation and allocation controls."""
    from validation.local_unification import native
    out = Path(out)
    out.mkdir(parents=True, exist_ok=True)
    law = native.build_tensor()
    roles = {"record": [0, 1, 4, 5], "carrier": [2, 3, 6, 7]}
    owned = allocation(law, roles, [("record", "carrier"), ("carrier", "record")])
    rng = np.random.default_rng(6306)
    current = rng.integers(0, 2, size=(8, 27)).astype(object)
    carries = np.array([[(g + n) % 6 for n in range(27)] for g in range(8)], dtype=object)
    seed = native.prepare_state(current, 3, remainders=carries)
    transforms = 0
    fixed = 0
    for matrix in signed_permutations():
        moved = covariance(law, seed, matrix)
        carrier_direction = transform_direction((1, 0, 0), matrix)
        declared = native.build_tensor(direction=carrier_direction)
        if moved.fingerprint != declared.fingerprint:
            raise ValueError("direction-indexed native family is not covariant")
        transforms += 1
        fixed += moved.fingerprint == law.fingerprint
    if fixed == transforms:
        raise ValueError("the declared directed control unexpectedly lost its orientation")
    # A standalone extra block cannot stand in for a geometry interaction.
    from universe24.core import GearType
    disconnected = Tensor(list(law.gears) + [GearType("disconnected.geometry", "audit")],
                          [(m.target, m.coeff, [(f.gear, f.offset, f.field) for f in m.factors])
                           for m in law.monomials] + [(8, 6, [(8, (0, 0, 0), "b")])],
                          strict_support=True)
    try:
        allocation(disconnected, {**roles, "geometry": [8]}, [("record", "geometry")])
    except ValueError as exc:
        disconnected_rejected = "disconnected claimed dependency" in str(exc)
    else:
        disconnected_rejected = False
    if not disconnected_rejected:
        raise ValueError("disconnected physical concatenation was not rejected")
    report = {"schema": "universe24/local-unification/contracts/1",
              "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              "allocation": owned, "signed_coordinate_transformations": transforms,
              "same_fixed_tensor_transformations": fixed,
              "forward_complete_register_comparisons": transforms * 3 * 8 * 27,
              "direction_family_covariance": "passed",
              "full_cube_invariance_of_fixed_directed_tensor": "failed",
              "disconnected_geometry_claim_rejected": disconnected_rejected,
              "physical_acceptance": "not_granted"}
    (out / "contracts.json").write_bytes(canonical_bytes(report) + b"\n")
    return report


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, default=Path("runs/local-unification/contracts"))
    args = parser.parse_args(argv)
    print(exact_json.dumps(audit(args.out), sort_keys=True))


if __name__ == "__main__":
    main()
