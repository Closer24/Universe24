"""Exact whole-state translation probe for a prepared guided packet."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import time

from universe24 import State
from universe24.core.group_2o import DIRECTIONS
from universe24.experiments.config import checkpoint_data
from universe24.observation.clicks import clicks
from research.components import BoardSpec, TensorSpec, GuideSegment, Patch, place, finalize, plain
from research.signal_clocks.run import write_json, canonical

ROOT = Path(__file__).resolve().parents[2]
PROTOCOL = Path(__file__).with_name("confirmation_packet_protocol.json")


def prepare_packet(side, present):
    board = BoardSpec(side=side, tensor=TensorSpec.from_signs((1, 1, 1)))
    origin = (0, side // 2, side // 2)
    guide = GuideSegment(start=0, stop=side - 1, sockets=(0, 1, 2, 3),
        remainder_pair=(0, 4), tensor=board.tensor)
    cells = {}
    for x in range(4):
        a = (1 if x == 0 else -1 if x == 2 else 0) if present else 0
        b = (1 if x == 1 else -1 if x == 3 else 0) if present else 0
        cells[(x, 0, 0, 0)] = (a, b, 4)
        cells[(x, 0, 0, 14)] = (-a, -b, 0)
    for x in (1, 2):
        for direction in range(2, 6):
            dx, dy, dz = DIRECTIONS[direction]
            for g, sign in ((0, 1), (14, -1)):
                h = board.tensor.ports[direction][g]
                weight = board.tensor.weights[direction][g]
                address = (x + dx, dy, dz, h)
                value = (0, 0, 2 - 2 * sign * weight)
                if address in cells and cells[address] != value:
                    raise ValueError("Packet halo assignments conflict")
                cells[address] = value
    source_addresses = tuple((x, 0, 0, g) for x in range(4) for g in (0, 14))
    packet = Patch("signal-source", cells, tensor=board.tensor,
        sources={"packet": source_addresses}, ports={"packet": source_addresses},
        evidence_domains=("Exact guided-translation candidate; not established physical light.",))
    return finalize(board, [place(guide, at=origin, name="guide"),
        place(packet, at=origin, name="packet")])


def translate_x(state):
    return State(state.cube, state.background,
        {((x + 1) % state.cube.side, y, z, g): value for (x, y, z, g), value in state.cells.items()})


def execute(output):
    output = Path(output)
    output.mkdir(parents=True, exist_ok=False)
    raw = PROTOCOL.read_bytes()
    protocol = json.loads(raw)
    if protocol["status"] != "frozen_before_checks":
        raise ValueError("Packet protocol is not frozen")
    (output / "protocol.frozen.json").write_bytes(raw)
    sources = [PROTOCOL, Path(__file__), ROOT / "research/signal_clocks/run.py",
        *sorted((ROOT / "research/components").glob("*.py")), *sorted((ROOT / "universe24").rglob("*.py"))]
    manifest = {}
    for path in sources:
        data = path.read_bytes()
        rel = path.relative_to(ROOT)
        manifest[str(rel)] = hashlib.sha256(data).hexdigest()
        target = output / "source" / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(data)
    write_json(output / "source_manifest.json", manifest)
    start, wall = time.process_time(), time.monotonic()
    results, presentation = [], []
    failure = None
    for side in protocol["preparation"]["sides"]:
        for present in protocol["preparation"]["source_presence"]:
            identifier = f"guided-packet-L{side}-s{int(present)}"
            folder = output / "cases" / identifier
            folder.mkdir(parents=True, exist_ok=False)
            prepared = prepare_packet(side, present)
            engine, initial = prepared.engine, prepared.initial
            write_json(folder / "assembly.json", plain(prepared.manifest))
            state = initial
            checkpoints = [checkpoint_data(state, engine, 0)]
            observations, event_records = [], []
            try:
                for step in range(1, side + 1):
                    if time.process_time() - start > protocol["budget"]["cpu_seconds"] or time.monotonic() - wall > protocol["budget"]["wall_seconds"]:
                        raise TimeoutError("Declared guided-packet budget exhausted")
                    after = engine.advance(state)
                    if len(after.cells) > protocol["budget"]["max_stored_channels"]:
                        raise MemoryError("Declared stored-channel budget exhausted")
                    observations.append({"step": step, "translation_equal": after == translate_x(state),
                        "stationary": after == initial, "inverse_equal": engine.rewind(after) == state})
                    event_records.extend({"step": e.step, "address": list(e.address), "kind": e.kind,
                        "quotient": e.quotient, "before": list(e.before), "after": list(e.after)}
                        for e in clicks(state, after, step))
                    state = after
                    checkpoints.append(checkpoint_data(state, engine, step))
            except (TimeoutError, MemoryError) as exc:
                failure = {"case": identifier, "type": type(exc).__name__, "message": str(exc)}
            with (folder / "states.jsonl").open("x", encoding="utf-8") as handle:
                for checkpoint in checkpoints:
                    handle.write(canonical(checkpoint) + "\n")
            write_json(folder / "initial.json", checkpoints[0])
            write_json(folder / "final.json", checkpoints[-1])
            write_json(folder / "events.json", event_records)
            rewound = state
            for _ in observations:
                rewound = engine.rewind(rewound)
            first_return = next((row["step"] for row in observations if row["stationary"]), None)
            passed = failure is None and all(row["inverse_equal"] for row in observations) and rewound == initial
            passed &= (all(row["translation_equal"] for row in observations) and first_return == side) if present else all(row["stationary"] for row in observations)
            result = {"id": identifier, "side": side, "present": present, "steps": len(observations),
                "passed": passed, "first_return": first_return, "full_rewind": rewound == initial,
                "observations": observations, "trace_sha256": hashlib.sha256((folder / "states.jsonl").read_bytes()).hexdigest(),
                "coupling_fingerprint": engine.coupling.fingerprint, "guarded_events": len(event_records)}
            write_json(folder / "result.json", result)
            results.append(result)
            presentation.append({"id": identifier, "title": f"Guided packet L={side}: {'moving' if present else 'no-source control'}",
                "description": protocol["scope"] + " " + protocol["boundary_scope"],
                "trace": str((folder / "states.jsonl").relative_to(output)), "trace_sha256": result["trace_sha256"],
                "view": {"position": [1, side // 2, side // 2], "channel": 0}, "readouts": []})
            print(json.dumps({k: result[k] for k in ("id", "passed", "first_return", "guarded_events")}), flush=True)
            if failure:
                break
        if failure:
            break
    summary = {"protocol_id": protocol["protocol_id"], "protocol_sha256": hashlib.sha256(raw).hexdigest(),
        "execution_status": "completed" if failure is None else "inconclusive", "failure": failure,
        "passed": failure is None and len(results) == 6 and all(r["passed"] for r in results),
        "runs": len(results), "forward_steps": sum(r["steps"] for r in results),
        "cpu_seconds": time.process_time() - start, "wall_seconds": time.monotonic() - wall,
        "source_manifest": manifest, "git_head": subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip(),
        "results": results, "scope": protocol["scope"], "boundary_scope": protocol["boundary_scope"]}
    write_json(output / "result.json", summary)
    write_json(output / "presentation.json", {"format": "universe24-signal-clock-presentation-v1",
        "title": "Guided compact packet: full-state translation checks", "protocol": {"path": "protocol.frozen.json", "sha256": hashlib.sha256(raw).hexdigest()},
        "cases": presentation})
    return summary


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    execute(parser.parse_args().output)
