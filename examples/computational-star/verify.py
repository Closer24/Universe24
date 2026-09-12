"""Verify completed delay experiments and distinguish scheduled from elapsed waiting."""

import argparse
import hashlib
import json
from pathlib import Path

from event_universe.retention import ArtifactLease


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    results = {r["case"]: r for r in json.loads((args.input / "results.json").read_text())}
    expected = {"active", "no_field", "small_mass", "reverse_vector", "high_budget"}
    assert set(results) == expected
    frames = {
        name: [
            json.loads(line) for line in (args.input / name / "frames.jsonl").read_text().splitlines()
        ]
        for name in expected
    }
    active = results["active"]
    for name, result in results.items():
        assert result["ticks"] == 128 and result["fault"] is None
        assert all(v == 0 for v in result["max_inventory_error"].values())
        assert len(frames[name]) == 129
        assert result["momentum_unchanged"]
        for probe, events in result["departures"].items():
            assert [e["port"] for e in events] == [0] * len(events)
            if name in ("small_mass", "reverse_vector"):
                assert events == active["departures"][probe]
                assert result["cycles"][probe] == active["cycles"][probe]
    assert frames["small_mass"] == frames["active"]
    for a, b in zip(frames["active"], frames["reverse_vector"], strict=True):
        assert a["probes"] == b["probes"] and a["source_work_max"] == b["source_work_max"]
        assert len(a["field_slice"]) == len(b["field_slice"])
        for x, y in zip(a["field_slice"], b["field_slice"], strict=True):
            assert x[:3] == y[:3] and x[3:] == [-v for v in y[3:]]
    summary = []
    for name, result in sorted(results.items()):
        for probe, cycles in result["cycles"].items():
            summary.append(
                {
                    "case": name,
                    "probe": probe,
                    "hops": len(result["departures"][probe]),
                    "scheduled_extra_wait": sum(c["extra"] for c in cycles),
                    "elapsed_extra_wait": sum(
                        max(0, min(c["tick"] + c["extra"], result["ticks"]) - c["tick"]) for c in cycles
                    ),
                    "max_cycle_cost": max(c["cost"] for c in cycles),
                }
            )
    args.output.mkdir(parents=True, exist_ok=False)
    with ArtifactLease(args.output.parent, [args.output]):
        report = {
            "checks": "passed",
            "summary": summary,
            "controls": {
                "small_mass_exact_trajectory_and_timing": True,
                "reverse_vector_exact_timing_and_negated_field": True,
            },
            "evidence_sha256": {
                str(p.relative_to(args.input)): hashlib.sha256(p.read_bytes()).hexdigest()
                for p in args.input.rglob("*")
                if p.is_file()
            },
        }
        (args.output / "verification.json").write_text(json.dumps(report, indent=2))
        print(json.dumps(summary))


if __name__ == "__main__":
    main()
