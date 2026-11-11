"""Validate the pinned 44-channel proposal through the one supported runtime.

This is an import adapter and compatibility audit, not a second runtime model
selector. The proposal is loaded only in an isolated Python subprocess. Its
published first staggered-audit seed is reproduced without claiming that it
satisfies Einstein constraints. No proposal code is imported into production.

Run: python -m validation.team48_contract --source /path/to/pinned/checkout
"""
from __future__ import annotations

import argparse
import gzip
import hashlib
from pathlib import Path
import subprocess
import sys

from universe24.core import exact_json
from universe24.system.bundle import create_bundle, read_json, state_from_data, tensor_from_data
from universe24.system.decoder import default_protocol
from universe24.system.runtime import run_bundle, verify_run

SOURCE_COMMIT = "49b896c795203914a939e465d6d39e5b99343259"
SOURCE_PR = "https://github.com/Closer24/Universe24/pull/42"
SEED_RECIPE = "experiments/geometry/team48/integer_staggered_audit.py:check_candidate first phase (1,1)"

# Runs under `python -I`, using only the pinned checkout. This repeats the
# exact first-sector seed recipe in check_candidate, including RNG draw order.
_EXPORT = r'''
import hashlib, json, pathlib, sys
root, output = map(pathlib.Path, sys.argv[1:3])
sys.path.insert(0, str(root))
import numpy as np
from universe24.core import Engine
from universe24.tests.test_migration import scalar_step
from experiments.geometry.team48.candidate import build
from experiments.geometry.team48.integer_staggered_audit import candidate, pair_diagnostics
from experiments.geometry.team48 import integer_staggered as staggered

program, builder = candidate()
declared = build('charged_positive', mass_squared=1)
assert declared.program.tensor.fingerprint == program.tensor.fingerprint
assert program.tensor.G == 44
rng = np.random.default_rng(4439)
previous, current = [rng.integers(-1, 2, size=(43, 27)).astype(object) for _ in range(2)]
for axis in range(3):
    p, q = (program.fields.index(f'diag_{label}{axis}') for label in ('p', 'q'))
    previous[p], previous[q], current[p], current[q] = 1, 1, 1, 0
carry = rng.integers(0, 6, size=(44, 27)).astype(object)
initial = staggered.prepare(program, previous, current, L=3, phase=(1, 1), remainders=carry)
engine = Engine(program.tensor)
state = oracle = initial
states = [initial.to_dict()]
areas, _, _ = pair_diagnostics(program, previous, current)
assert np.all(areas == 1)
for _ in range(3):
    state, oracle = engine.step(state), scalar_step(program.tensor, oracle)
    assert state.same_as(oracle)
    assert np.array_equal(state.r, carry)
    states.append(state.to_dict())
assert engine.rewind(state, 3).same_as(initial)
owners = {0: 'computational_phase'}
for name, fields in declared.blocks:
    for field in fields:
        owners[program.tensor.gear_index('field.' + field)] = name
assert set(owners) == set(range(44))
channels = [dict(index=i, name=gear.name, label=gear.label,
                 owner=owners[i], purpose='Pinned proposal ' + owners[i] + '; no physical promotion')
            for i, gear in enumerate(program.tensor.gears)]
paths = sorted((root / 'experiments/geometry/team48').glob('*.py'))
paths += [root/'universe24/core/engine.py', root/'universe24/core/tensor.py',
          root/'universe24/core/lattice.py', root/'universe24/tests/test_migration.py']
hashes = {str(path.relative_to(root)): hashlib.sha256(path.read_bytes()).hexdigest() for path in paths}
reference = dict(states=states, source_sha256=hashes, manifest=declared.manifest(),
                 seed_rng=4439, phase=[1, 1], steps=3,
                 all_remainder_classes=sorted(set(int(v) for v in carry.flat)),
                 proposal_scalar_oracle_agreement=True, proposal_complete_rewind=True,
                 seed_is_continuum_einstein_solution_pair=False)
output.mkdir(parents=True)
for name, data in [('tensor.json', program.tensor.to_dict()), ('seed.json', initial.to_dict()),
                   ('channels.json', channels), ('reference.json', reference)]:
    (output/name).write_text(json.dumps(data, sort_keys=True, separators=(',', ':'))+'\n')
print(json.dumps({'channels': program.tensor.G, 'monomials': len(program.tensor.monomials),
                  'complete_state_snapshots': len(states)}))
'''


def _git(source, *args):
    return subprocess.run(["git", "-C", str(source), *args], text=True, check=True,
                          stdout=subprocess.PIPE, stderr=subprocess.PIPE).stdout.strip()


def audit(source: str | Path, out: str | Path) -> dict:
    source, out = Path(source).resolve(), Path(out).resolve()
    if _git(source, "rev-parse", "HEAD") != SOURCE_COMMIT:
        raise ValueError("proposal checkout is not the explicitly pinned commit")
    if _git(source, "status", "--porcelain", "--untracked-files=no"):
        raise ValueError("proposal checkout has tracked modifications")
    if out.exists() and (not out.is_dir() or any(out.iterdir())):
        raise ValueError("audit output must be new or empty")
    out.mkdir(parents=True, exist_ok=True)
    raw = out / "proposal-inputs"
    subprocess.run([sys.executable, "-I", "-c", _EXPORT, str(source), str(raw)],
                   cwd=source, text=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    tensor = tensor_from_data(read_json(raw / "tensor.json"))
    seed = state_from_data(read_json(raw / "seed.json"))
    reference = read_json(raw / "reference.json")
    if tensor.G != 44 or len(reference["states"]) != 4:
        raise ValueError("pinned audit has unexpected allocation or reference length")
    bundle = create_bundle(tensor, seed, channels=read_json(raw / "channels.json"),
                           protocol=default_protocol(),
                           model={"id": "proposal-team48-pinned-compatibility", "version": SOURCE_COMMIT,
                                  "domain": "Mechanical import of published charged_positive first-sector audit; not an accepted Einstein model"})
    run = out / "run"
    runtime_report = run_bundle(bundle, run, steps=3)
    if exact_json.dumps(seed.to_dict(), sort_keys=True) != exact_json.dumps(reference["states"][0], sort_keys=True):
        raise ValueError("imported complete seed disagrees with pinned proposal")
    seen = 0
    with gzip.open(run / "full_trace.jsonl.gz", "rt", encoding="utf-8") as stream:
        for index, line in enumerate(stream, start=1):
            record = exact_json.loads(line)
            if (exact_json.dumps(record["before"], sort_keys=True) != exact_json.dumps(reference["states"][index-1], sort_keys=True)
                    or exact_json.dumps(record["after"], sort_keys=True) != exact_json.dumps(reference["states"][index], sort_keys=True)):
                raise ValueError(f"proposal/generic runtime complete-state mismatch at step {index}")
            seen = index
    if seen != 3:
        raise ValueError("missing proposal comparison step")
    clicks_by_label = {"official": 0, "audit": 0}
    with gzip.open(run / "clicks.jsonl.gz", "rt", encoding="utf-8") as stream:
        for line in stream:
            clicks_by_label[exact_json.loads(line)["label"]] += 1
    verify_run(run)
    report = {
        "schema": "universe24/validation/team48-contract/1",
        "source_pr": SOURCE_PR, "source_commit": SOURCE_COMMIT, "seed_recipe": SEED_RECIPE,
        "adapter_source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "proposal_source_sha256": reference["source_sha256"],
        "bundle_id": runtime_report["bundle_id"], "run_id": runtime_report["run_id"],
        "tensor_hash": tensor.fingerprint, "channels_per_node": tensor.G,
        "parameters": {"dt": 1, "dx": 1, "mass_squared": 1, "coupling": 1, "cosmological": 0},
        "protocol": default_protocol(),
        "retained_integer_entries_per_node": 3 * tensor.G, "nodes": seed.N, "steps": 3,
        "monomials": len(tensor.monomials), "strict_physical_support_violations": len(tensor.support_violations()),
        "all_retained_states_and_remainders_match_proposal": True,
        "proposal_scalar_oracle_agreement": reference["proposal_scalar_oracle_agreement"],
        "remainder_classes": reference["all_remainder_classes"],
        "exact_rewind": True, "generic_runtime_and_decoder_used": True,
        "production_model_selected_or_promoted": False,
        "arithmetic_click_count": runtime_report["click_count"],
        "arithmetic_clicks_by_label": clicks_by_label,
        "seed_is_continuum_einstein_solution_pair": False,
        "physical_acceptance_gates": {
            key: {"status": "not_tested", "reason": reason}
            for key, reason in {
                "C": "This compatibility run does not evaluate Einstein constraints or independent curvature; its published audit seed is unconstrained.",
                "D": "No space, time or quantization refinement study is performed here. General convergence remains unestablished.",
                "E": "The computational sign phase is not proper-clock apparatus. Shared-metric clock/detector behavior remains unestablished.",
                "F": "All exported clicks are audit-labelled arithmetic events. Born/Bell or operational detector physics remains unestablished.",
            }.items()
        },
        "reported_proposal_limitations": {
            "nonlinear_constraint_counterexamples": {
                "status": "reported_failure", "rerun_in_this_adapter": False,
                "source": "experiments/geometry/team48/constraints_findings.md",
                "reason": "Pinned research reports constraint counterexamples in investigated nonlinear frame-leapfrog routes; this is not a fresh constraint evaluation of the imported 44-channel seed.",
            },
            "fractional_coefficient_refinement": {
                "status": "reported_failure", "rerun_in_this_adapter": False,
                "source": "experiments/geometry/team48/integer_RESEARCH.md",
                "reason": "The published compiler rejects increments with noninteger coefficients. A general controlled integer refinement family has not been established.",
            },
        },
        "interpretation": "All 44 audit-labelled channels import and replay through one runtime. A zero official click stream is not a physical nondetection result. Positive paired geometry uses a computational second mode and does not close the Einstein gates.",
    }
    (out / "integration.json").write_text(exact_json.dumps(report, sort_keys=True) + "\n", encoding="utf-8")
    return report


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", required=True, type=Path)
    parser.add_argument("--out", type=Path, default=Path("runs/team48-contract"))
    args = parser.parse_args(argv)
    report = audit(args.source, args.out)
    print(exact_json.dumps({key: report[key] for key in (
        "source_commit", "channels_per_node", "steps", "all_retained_states_and_remainders_match_proposal",
        "exact_rewind", "production_model_selected_or_promoted")}))


if __name__ == "__main__":
    main()
