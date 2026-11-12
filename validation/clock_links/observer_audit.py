"""Read saved phase-apparatus clicks after independent complete-run verification.

Run: python -m validation.clock_links.observer_audit --run RUN --out OUTPUT
This harness may invoke replay; observer.py never receives hidden state.
"""
from __future__ import annotations

import argparse
import gzip
import hashlib
from pathlib import Path

from universe24.core import exact_json
from universe24.system.bundle import read_json
from universe24.system.runtime import verify_run
from validation.clock_links.model import OBSERVER_NAMES
from validation.clock_links.observer import ClickObserver, make_protocol, observe_clicks


def _sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def audit(run, out):
    run, out = Path(run), Path(out)
    if out.exists() and any(out.iterdir()):
        raise ValueError("observer audit output must be new or empty")
    out.mkdir(parents=True, exist_ok=True)
    verified = verify_run(run)
    channels = read_json(run / "bundle" / "channels.json")
    ports = {channel["name"]: channel["index"] for channel in channels}
    if not all(name in ports for name in OBSERVER_NAMES):
        raise ValueError("run does not contain the declared four phase apparatus ports")
    # Determine lattice size by exact integer arithmetic, with no trajectory
    # access. Detector nodes and complete one-step windows are fixed here before
    # opening any clicks, rather than selected after observing response.
    nodes = verified["nodes"]
    side = 3
    while side ** 3 < nodes:
        side += 1
    if side ** 3 != nodes:
        raise ValueError("run node count is not a supported periodic cube")
    protocol = make_protocol(
        tensor_hash=verified["tensor_hash"], L=side,
        channel_count=verified["channels_per_node"], expected_steps=verified["steps"],
        detectors=[{"id": f"node-{node}", "node": node,
                    "channels": [ports[name] for name in OBSERVER_NAMES]}
                   for node in range(nodes)])
    (out / "protocol.json").write_text(exact_json.dumps(protocol, sort_keys=True) + "\n")
    before_files = {name: _sha(run / name) for name in ("full_trace.jsonl.gz", "clicks.jsonl.gz", "validation.json")}
    with gzip.open(run / "clicks.jsonl.gz", "rt", encoding="utf-8") as stream:
        offline = observe_clicks((exact_json.loads(line) for line in stream), protocol,
                                 run_id=verified["run_id"])
    online = ClickObserver(protocol, run_id=verified["run_id"])
    with gzip.open(run / "clicks.jsonl.gz", "rt", encoding="utf-8") as stream:
        for line in stream:
            online.consume([exact_json.loads(line)])
    if offline != online.report():
        raise AssertionError("online/offline observer mismatch")
    if any(_sha(run / name) != digest for name, digest in before_files.items()):
        raise AssertionError("passive observation changed saved run")
    package = Path(__file__).parent
    evidence = {"schema": "universe24/clock-link-observer-audit/1",
                "run_id": verified["run_id"], "bundle_id": verified["bundle_id"],
                "tensor_hash": verified["tensor_hash"],
                "channels_per_node": verified["channels_per_node"],
                "complete_runtime_replay": True,
                "observer_inputs": ["canonical click records", "static complete-window protocol", "run identity"],
                "observer_reads_hidden_state": False,
                "online_offline_parity": True, "saved_run_unchanged": True,
                "complete_trial_windows": len(protocol["windows"]) * nodes,
                "source_sha256": {name: _sha(package / name) for name in ("observer.py", "observer_audit.py", "model.py")},
                "outcome_counts": offline["outcome_counts"],
                "observed_apparatus_records": offline["declared_detector_records"],
                "input_record_sha256": offline["input_record_sha256"],
                "physical_acceptance": "not established: record windows are not emission trials or proper-time ticks; nonzero stationary intensity can be unrecorded"}
    (out / "observer.json").write_text(exact_json.dumps(offline, sort_keys=True) + "\n")
    (out / "audit.json").write_text(exact_json.dumps(evidence, sort_keys=True) + "\n")
    return evidence


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run", type=Path, required=True)
    parser.add_argument("--out", type=Path, default=Path("runs/clock_links/observer"))
    args = parser.parse_args(argv)
    print(exact_json.dumps(audit(args.run, args.out), sort_keys=True))


if __name__ == "__main__":
    main()
