"""Read every recorded run back tick by tick, with the per-ray detail the frames lack.

The canonical runner's recording (run.html frames, state.json, run.json) carries,
per Node and tick, the field value, octant populations and the ray count, but not
each ray's heading, amount and phase. This script replays the identical
initialization.json in-process (the engine is deterministic) and reads the
inventory view every tick. It then checks
that replay against the recorded frames Node by Node: every record's type and
values, and every spatial Node's complete field readout (value, directions,
populations, ray_count) and the escaped totals must match at every tick. Any
mismatch is reported, never hidden. The result is one JSON per panel with what
the renderer draws; nothing is interpolated.

Run:  PYTHONPATH=src python examples/research/ray-gallery/record_ticks.py --output DIR
      (DIR/runs/<panel>/ must hold the five recorded runs; see the README)
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import worlds

from event_universe import Simulation
from event_universe.core.disturbance_state import unpack
from event_universe.initialization import parse_initial_state
from event_universe.runner import source_fingerprint

HERE = Path(__file__).resolve().parent
CONFIGS = HERE / "configs"

OCTANT_SIGNS = [
    (1, 1),
    (1, 1),
    (1, -1),
    (1, -1),
    (-1, 1),
    (-1, 1),
    (-1, -1),
    (-1, -1),
]  # (sx, sy) per octant


def _json(value):
    if isinstance(value, tuple):
        return [_json(v) for v in value]
    if isinstance(value, list):
        return [_json(v) for v in value]
    if isinstance(value, dict):
        return {k: _json(v) for k, v in value.items()}
    return value


def recorded_frames(run_dir: Path) -> list[dict]:
    document = (run_dir / "run.html").read_text(encoding="utf-8")
    start = document.find('{"frames"')
    if start < 0:
        raise ValueError(f"{run_dir}: run.html carries no recorded frames")
    recording, _ = json.JSONDecoder().raw_decode(document[start:])
    return recording["frames"]


def replay(panel: dict, out: Path, configs: Path) -> dict:
    key = panel["key"]
    run_dir = out / "runs" / key
    raw = json.loads((run_dir / "initialization.json").read_text(encoding="utf-8"))
    report = json.loads((run_dir / "run.json").read_text(encoding="utf-8"))
    frames = recorded_frames(run_dir)
    field = panel["field"]
    names = [t["name"] for t in raw["disturbance_types"]]
    spatial = raw["spatial_fields"]
    field_index = next(i for i, f in enumerate(spatial) if f["field"] == field)
    definition = spatial[field_index]
    headings = definition.get("headings")
    phase_steps = definition.get("kerengonen", {}).get("phase_steps")
    octant_fields = [f["field"] for f in spatial if f.get("transport", "outward") == "outward"]
    computation = raw.get("computation_field")
    world = Simulation(parse_initial_state(raw))
    initial_total = world.totals()[field][0]
    mismatches: list[dict] = []
    ticks_out: list[dict] = []

    def compare(tick: int) -> None:
        frame = frames[tick]
        if frame["tick"] != tick:
            mismatches.append({"tick": tick, "what": "frame tick", "recorded": frame["tick"]})
            return
        recorded_records = {}
        for node in frame["nodes"]:
            for d in node["disturbances"]:
                recorded_records.setdefault(tuple(node["position"]), []).append(
                    (d["type"], _json(d["values"]))
                )
        replay_records = {}
        for pos, node in world.nodes.items():
            for r in node.records:
                if r is not None:
                    replay_records.setdefault(tuple(pos), []).append(
                        (names[r.type_index], _json(world.record_values(r)))
                    )
        for pos in recorded_records.keys() | replay_records.keys():
            a = sorted(json.dumps(x) for x in recorded_records.get(pos, []))
            b = sorted(json.dumps(x) for x in replay_records.get(pos, []))
            if a != b:
                mismatches.append(
                    {"tick": tick, "what": "records", "position": list(pos), "recorded": a, "replay": b}
                )
        recorded_spatial = {tuple(n["position"]): _json(n["fields"]) for n in frame["spatial_fields"]}
        for pos, fields in recorded_spatial.items():
            mine = _json(world._spatial.values(pos))
            if mine != fields:
                mismatches.append(
                    {
                        "tick": tick,
                        "what": "spatial",
                        "position": list(pos),
                        "recorded": fields,
                        "replay": mine,
                    }
                )
        for pos in world._spatial.nodes.keys() - recorded_spatial.keys():
            mine = _json(world._spatial.values(pos))
            blank = all(v == 0 for f in mine.values() for v in f["value"]) and all(
                f.get("ray_count", 0) == 0 for f in mine.values()
            )
            if not blank:
                mismatches.append(
                    {
                        "tick": tick,
                        "what": "spatial node missing from recording",
                        "position": list(pos),
                        "replay": mine,
                    }
                )
        if _json(world.escaped_totals()) != _json(frame["escaped_totals"]):
            mismatches.append(
                {
                    "tick": tick,
                    "what": "escaped",
                    "recorded": frame["escaped_totals"],
                    "replay": _json(world.escaped_totals()),
                }
            )

    def capture(tick: int) -> dict:
        view = world.inventory_view()
        rays, records, waits, cells = [], [], [], []
        ray_total = 0
        record_total = 0
        for node in view.nodes:
            x, y, z = node.position
            for r in node.rays[field_index] if node.rays else ():
                hx, hy, hz = headings[r.heading]
                ray_total += r.amount
                rays.append([x, y, hx, hy, r.amount, r.phase if phase_steps else None, r.wait])
            if node.position in world._spatial.nodes:
                sp = world._spatial.nodes[node.position]
                if sp.ray_wait:
                    waits.append([x, y, sp.ray_wait])
                for i, f in enumerate(spatial):
                    if f["field"] in octant_fields:
                        pops = [unpack(p)[0] for p in sp.states[i].populations]
                        total = sum(pops)
                        if total:
                            dx = sum(p * s[0] for p, s in zip(pops, OCTANT_SIGNS, strict=False))
                            dy = sum(p * s[1] for p, s in zip(pops, OCTANT_SIGNS, strict=False))
                            cells.append([x, y, f["field"], total, dx, dy])
            for r in node.records:
                if r is None:
                    continue
                values = _json(world.record_values(r))
                extra = {}
                if r.absorbed_phases:
                    extra["absorbed_phase"] = unpack(r.absorbed_phases[0])[0]
                if field in values:
                    record_total += values[field][0]
                records.append([x, y, names[r.type_index], values, extra])
        totals = world.totals()
        escaped = world.escaped_totals()
        sources = world.source_totals()
        accounting = world.spatial_accounting()
        return {
            "tick": tick,
            "rays": rays,
            "records": records,
            "waits": waits,
            "cells": cells,
            "totals": {
                "in_world": totals[field][0],
                "rays": ray_total,
                "records": record_total,
                "escaped": escaped[field][0],
                "injected": sources[field][0],
                "initial": initial_total,
            },
            "balanced": bool(accounting[field]["balanced"]),
        }

    compare(0)
    ticks_out.append(capture(0))
    for tick in range(1, raw["ticks"] + 1):
        world.step()
        compare(tick)
        ticks_out.append(capture(tick))
    derived = derive(panel, raw, ticks_out)
    return {
        "key": key,
        "title": panel["title"],
        "contract": panel["contract"],
        "kind": panel["kind"],
        "field": field,
        "config": str(configs / f"{key}.json"),
        "run_dir": str(run_dir),
        "shape": raw["shape"],
        "ticks": raw["ticks"],
        "headings": headings,
        "phase_steps": phase_steps,
        "computation_field": computation,
        "run": {
            k: report.get(k)
            for k in (
                "status",
                "error",
                "completed_ticks",
                "requested_ticks",
                "accounting_balanced_at_every_completed_tick",
                "conserved_at_every_completed_tick",
                "spatial_policy",
                "spatial_transport",
                "spatial_metric",
                "spatial_allocation",
                "ray_delay",
                "ray_phase",
                "local_delay",
                "computation_field",
                "initial_totals",
                "final_totals",
                "escaped_totals",
                "source_totals",
                "source_sha256",
                "initialization_sha256",
                "model",
            )
        },
        "verify": {
            "frames_recorded": len(frames),
            "frames_compared": raw["ticks"] + 1,
            "mismatches": len(mismatches),
            "first_mismatches": mismatches[:5],
            "checked": [
                "record types and values per Node",
                "field value, directions, populations, ray_count per Node",
                "escaped totals",
            ],
        },
        "derived": derived,
        "frames": ticks_out,
    }


def derive(panel: dict, raw: dict, frames: list[dict]) -> dict:
    """Panel-specific counters read from the replayed frames (never from a model)."""
    key = panel["key"]
    if key == "7-ray-delay":
        first = next(
            (
                f["tick"]
                for f in frames
                if any(r[2] == "screen" and r[3]["quanta"][0] for r in f["records"])
            ),
            None,
        )
        max_wait: dict[str, int] = {}
        for f in frames:
            for x, _y, k in f["waits"]:
                max_wait[str(x)] = max(max_wait.get(str(x), 0), k)
        return {
            "first_click_tick": first,
            "unloaded_first_click_tick": 11,
            "unloaded_first_click_source": "same document with emission 0, run in-process while tuning (not a recorded panel)",
            "max_wait_by_x": dict(sorted(max_wait.items(), key=lambda kv: int(kv[0]))),
        }
    if key == "6-mirror-cavity":
        holds = [
            (f["tick"], r[0])
            for f in frames
            for r in f["records"]
            if r[2] == "mirror" and r[3]["quanta"][0]
        ]
        return {"mirror_hold_ticks": holds}
    if key == "3-double-slit":
        final = frames[-1]["records"]
        return {"screen_profile_by_y": {str(r[1]): r[3]["quanta"][0] for r in final if r[2] == "screen"}}
    return {}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument(
        "--configs", type=Path, default=CONFIGS, help="directory of the five panel configurations"
    )
    args = parser.parse_args()
    ticks_dir = args.output / "ticks"
    ticks_dir.mkdir(parents=True, exist_ok=True)
    fingerprint = source_fingerprint()
    index = []
    for panel in worlds.PANELS:
        result = replay(panel, args.output, args.configs)
        result["replay_source_sha256"] = fingerprint
        (ticks_dir / f"{panel['key']}.json").write_text(json.dumps(result) + "\n", encoding="utf-8")
        v = result["verify"]
        print(
            f"{panel['key']:20s} ticks={result['ticks']:3d} frames={v['frames_recorded']:3d} mismatches={v['mismatches']} "
            f"run={result['run']['status']} balanced={result['run']['accounting_balanced_at_every_completed_tick']} "
            f"policy={result['run']['spatial_policy']}"
        )
        if v["mismatches"]:
            print("   FIRST MISMATCH:", json.dumps(v["first_mismatches"][0])[:400])
        index.append({"key": panel["key"], "ticks": result["ticks"], "mismatches": v["mismatches"]})
    (ticks_dir / "index.json").write_text(
        json.dumps({"source_sha256": fingerprint, "python": sys.version, "panels": index}, indent=1)
        + "\n"
    )


if __name__ == "__main__":
    main()
