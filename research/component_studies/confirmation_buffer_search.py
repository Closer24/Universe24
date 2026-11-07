"""Initial matching-buffer search assembled through the generic component API."""
from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from pathlib import Path
import subprocess
import time

from research.components import BoardSpec, TensorSpec, GuideSegment, Receiver, SignalSource, place, finalize, plain
from research.signal_clocks.run import run_case, write_json
from .confirmation_search import evaluate, receiver_events

ROOT = Path(__file__).resolve().parents[2]
PROTOCOL = Path(__file__).with_name("confirmation_buffer_protocol.json")


def prepare_buffer(case, mask):
    board = BoardSpec(side=case["side"], tensor=TensorSpec.from_signs(case["body_signs"]))
    origin = (case["side"] // 2,) * 3
    first, second = case["source_offsets"]
    sockets = (first, -2, -1, 0, 1, 2, second)
    placements = [place(GuideSegment(start=first, stop=second, sockets=sockets,
        tensor=board.tensor), at=origin, name="guide")]
    placements.append(place(Receiver(remainders=case["target_remainders"], tensor=board.tensor),
        at=origin, name="receiver"))
    for distance, pair in enumerate(case["buffer_pairs"], 1):
        for direction in (-1, 1):
            point = (origin[0] + direction * distance, origin[1], origin[2])
            placements.append(place(Receiver(remainders=pair, tensor=board.tensor),
                at=point, name=f"buffer-{distance}-{direction}"))
    source_positions = []
    for index, (offset, counters, present) in enumerate(zip(case["source_offsets"], case["source_ab"], mask), 1):
        point = (origin[0] + offset, origin[1], origin[2])
        source_positions.append(point)
        placements.append(place(SignalSource(a=counters[0], b=counters[1], present=present,
            tensor=board.tensor), at=point, name=f"source-{index}"))
    prepared = finalize(board, placements)
    return prepared.engine, prepared.initial, {"origin": origin,
        "detector": prepared.ports["receiver.memory"], "sources": source_positions}


def candidate_cases(protocol):
    pairs = list(itertools.product(protocol["preparation"]["allowed_remainders"], repeat=2))
    for index, (inner, outer) in enumerate(itertools.product(pairs, pairs)):
        p = protocol["preparation"]
        yield {"id": f"confirmation-buffer-{index:03d}",
            **{k: p[k] for k in ("side", "steps", "extent", "guide_mode", "source_offsets", "source_ab", "target_remainders")},
            "body_signs": protocol["model"]["body_signs"], "buffer_pairs": [inner, outer],
            "arrival_windows": [[8, 9], [16, 19]]}


def execute(output):
    output = Path(output)
    output.mkdir(parents=True, exist_ok=False)
    raw = PROTOCOL.read_bytes()
    protocol = json.loads(raw)
    if protocol["status"] != "frozen_before_search":
        raise ValueError("Protocol must be frozen before searching")
    (output / "protocol.frozen.json").write_bytes(raw)
    candidates = list(candidate_cases(protocol))
    assert len(candidates) == protocol["cases"]
    write_json(output / "candidate_manifest.json", candidates)
    source_files = [PROTOCOL, Path(__file__), Path(__file__).with_name("confirmation_search.py"),
        ROOT / "research/signal_clocks/run.py", ROOT / "research/signal_clocks/preparation.py",
        *sorted((ROOT / "research/components").glob("*.py")), *sorted((ROOT / "universe24").rglob("*.py"))]
    manifest = {}
    for path in source_files:
        data = path.read_bytes()
        rel = path.relative_to(ROOT)
        manifest[str(rel)] = hashlib.sha256(data).hexdigest()
        target = output / "source" / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(data)
    write_json(output / "source_manifest.json", manifest)
    started = time.process_time()
    wall = time.monotonic()
    results, runs_completed = [], 0
    failure = None
    for case in candidates:
        group = {}
        try:
            for mask in protocol["source_masks"]:
                if time.monotonic() - wall > protocol["budget"]["wall_seconds"]:
                    raise TimeoutError("Matching-buffer wall budget exhausted")
                key = "".join(str(int(v)) for v in mask)
                folder = output / "cases" / (case["id"] + "-s" + key)
                result = run_case(case, tuple(mask), deadline_cpu=started + protocol["budget"]["cpu_seconds"],
                    max_cells=protocol["budget"]["max_stored_channels"], audit=True, output=folder,
                    prepare_function=prepare_buffer)
                result["receiver_all_channel_events"] = receiver_events(folder / "states.jsonl", result["locations"]["origin"])
                write_json(folder / "receiver_events.json", result["receiver_all_channel_events"])
                group[key] = result
                runs_completed += 1
            result = evaluate(case, group)
            times = group["11"]["record_event_times"]
            result["checks"]["11:four_complete_quiet_updates"] = len(times) == 2 and times[1] - times[0] - 1 >= 4
            result["passed"] = all(result["checks"].values())
            results.append(result)
            write_json(output / (case["id"] + ".json"), result)
            print(json.dumps({"case": case["id"], "passed": result["passed"], "R": result["R_times"],
                "C": result["receiver_C_times"], "cpu_seconds": round(time.process_time() - started, 3)}), flush=True)
        except (TimeoutError, MemoryError) as exc:
            failure = {"case": case["id"], "type": type(exc).__name__, "message": str(exc)}
            break
    summary = {"format": "universe24-confirmation-buffer-result-v1", "protocol_id": protocol["protocol_id"],
        "protocol_sha256": hashlib.sha256(raw).hexdigest(), "source_manifest": manifest,
        "git_head": subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip(),
        "execution_status": "completed" if failure is None else "inconclusive", "cases_completed": len(results),
        "runs_completed": runs_completed, "passing_cases": [r["id"] for r in results if r["passed"]],
        "failure": failure, "cpu_seconds": time.process_time() - started, "wall_seconds": time.monotonic() - wall,
        "results": results, "fresh_confirmation_performed": False, "generic_components_used": True,
        "scope": protocol["scope"]}
    write_json(output / "result.json", summary)
    return summary


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    execute(parser.parse_args().output)
