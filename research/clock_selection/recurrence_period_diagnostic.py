"""Read-only full-board period diagnostic on existing recurrence recordings.

This is explicitly postanalysis: it adds no trajectory, changes no acceptance
predicate and distinguishes a proven repeated state from an unobserved period.
"""
from __future__ import annotations

import argparse
import gzip
import hashlib
import json
from pathlib import Path

from research.experiments.run import recorded_states
from research.presenter.export import state_sha256


def inspect_record(path):
    raw = path.read_bytes()
    row = json.loads(gzip.decompress(raw) if path.suffix == ".gz" else raw)
    states = recorded_states(row["experiment"])
    hashes = [state_sha256(state) for state in states]
    first, repeats, hash_collisions = {}, [], []
    for step, digest in enumerate(hashes):
        if digest in first:
            previous = first[digest]
            if states[previous] == states[step]:
                repeats.append([previous, step])
            else:
                hash_collisions.append([previous, step])
        else:
            first[digest] = step
    candidate = min((b-a for a,b in repeats), default=None)
    overlap = None if candidate is None else all(
        states[t] == states[t+candidate] for t in range(len(states)-candidate))
    initial_closed = candidate is not None and states[0] == states[candidate]
    return {"record":path.name,"record_file_sha256":hashlib.sha256(raw).hexdigest(),
        "case":row["case"],"frames":len(states),"first_repeat":repeats[0] if repeats else None,
        "repeat_pairs":repeats,"smallest_observed_period":candidate,
        "all_recorded_overlaps_equal":overlap,"initial_state_closes":initial_closed,
        "state_hash_collisions":hash_collisions,
        "full_board_period_certified_by_exact_equality":bool(initial_closed and overlap),
        "qualification":"Exact equality of complete sparse states including implicit background; deterministic fixed update extends a closed orbit. No finite non-repeat excludes a longer period."}


def main(argv=None):
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--study",type=Path,required=True)
    parser.add_argument("--output",type=Path,required=True)
    args=parser.parse_args(argv)
    paths=sorted((args.study/"records").glob("*.json.gz"))
    paths+=sorted((args.study/"records").glob("*.json"))
    if not paths:raise ValueError("No complete saved records")
    if args.output.exists():raise FileExistsError(args.output)
    rows=[inspect_record(path) for path in paths]
    result={"format":"universe24-recurrence-period-postanalysis-v1",
        "analysis_status":"postanalysis_of_existing_complete_records_only",
        "analysis_source_sha256":hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "input_protocol_sha256":hashlib.sha256((args.study/"protocol.json").read_bytes()).hexdigest(),
        "input_result_sha256":hashlib.sha256((args.study/"result.json").read_bytes()).hexdigest(),
        "records":rows,"new_transitions":0,
        "certified_closed_orbits":sum(r["full_board_period_certified_by_exact_equality"] for r in rows)}
    args.output.mkdir(parents=True,exist_ok=False)
    (args.output/"result.json").write_text(json.dumps(result,indent=2,sort_keys=True)+"\n")
    (args.output/"executed_diagnostic.py").write_bytes(Path(__file__).read_bytes())
    print(json.dumps({"records":len(rows),"closed_orbits":result["certified_closed_orbits"],
        "periods":[[r["record"],r["smallest_observed_period"],r["initial_state_closes"]] for r in rows]},indent=2))


if __name__=="__main__":main()
