"""Bounded headless host-memory measurements; never a physical input or speed claim."""

from __future__ import annotations

import dataclasses
import gc
import hashlib
import json
import sys
import tracemalloc
from pathlib import Path
from time import perf_counter

import event_universe
from event_universe import Simulation
from event_universe.initialization import parse_initial_state
from event_universe.retention import ArtifactLease, validate_output_path
from event_universe.runner import source_fingerprint

ROOT = Path(sys.argv[1]).resolve()
OUTPUT = Path(sys.argv[2]).resolve()
POINTS = (0, 1, 2, 3, 16, 32, 64, 128, 256)


def sha_json(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def deep_size(value):
    """Measure unique reachable Python allocations for an explicit local-owner graph."""
    seen = set()

    def visit(item):
        if id(item) in seen:
            return 0
        seen.add(id(item))
        size = sys.getsizeof(item)
        if dataclasses.is_dataclass(item):
            size += sum(visit(getattr(item, field.name)) for field in dataclasses.fields(item))
        elif isinstance(item, (tuple, list)):
            size += sum(visit(child) for child in item)
        elif isinstance(item, dict):
            size += sum(visit(key) + visit(child) for key, child in item.items())
        return size

    return visit(value)


def configuration(kind, count, width, slots):
    source = (
        ROOT / "examples/node-vector" / ("six-records.json" if kind == "records" else "two-fields.json")
    )
    raw = json.loads(source.read_text(encoding="utf-8"))
    template_sha = sha_json(raw)
    raw["slots_per_node"] = slots
    raw["ticks"] = POINTS[-1]
    raw["shape"] = [5, 5, 5]
    for field in raw["fields"]:
        old_width = field["components"]
        if width < old_width:
            raise ValueError("benchmark does not truncate declared registers")
        field["components"] = width
    for definition in raw["disturbance_types"]:
        for key, values in definition.get("defaults", {}).items():
            if isinstance(values, list):
                definition["defaults"][key] = values + [0] * (width - len(values))
    for field in raw.get("spatial_fields", []):
        field["baseline"] += [0] * (width - len(field["baseline"]))
    for seed in raw["seeds"]:
        for key, values in seed.get("values", {}).items():
            if isinstance(values, list):
                seed["values"][key] = values + [0] * (width - len(values))
    for seed in raw.get("spatial_seeds", []):
        seed["populations"] = [values + [0] * (width - len(values)) for values in seed["populations"]]
    positions = [(i % 3, (i // 3) % 3, i // 9) for i in range(count)]
    for key in ("seeds", "spatial_seeds"):
        original = raw.get(key, [])
        if original:
            raw[key] = [
                dict(seed, position=list(position)) for position in positions for seed in original
            ]
    if kind == "fields":
        # Exercise repeated pending ownership, retaining the configured generic
        # swap. Removing its one-shot predicate is an explicit benchmark input.
        for rule in raw["spatial_interactions"]:
            rule.pop("when", None)
        reads = [{"field": item["name"], "side": "right"} for item in raw["fields"]]
        total = {"op": "add", "args": reads}
        raw["field_rules"] = [
            {
                "name": "benchmark retained field window",
                "k": 2,
                "assignments": [
                    {"field": item["name"], "expression": read}
                    for item, read in zip(raw["fields"], reads, strict=True)
                ],
                "invariants": [{"name": "retained registers", "expression": total}],
            }
        ]
    return raw, str(source), template_sha


def state_metrics(world):
    carriers = tuple(world._nodes.values())
    spatial = () if world._spatial is None else tuple(world._spatial.nodes.values())
    packets = tuple(p for bank in world.links.values() for p in bank if p is not None)
    spatial_packets = (
        ()
        if world._spatial is None
        else tuple(p for bank in world._spatial.links.values() for p in bank if p is not None)
    )
    return {
        "tick": world.tick,
        "carrier_nodes": len(carriers),
        "spatial_nodes": len(spatial),
        "carrier_pending": sum(node.pending is not None for node in carriers),
        "spatial_pending": sum(node.pending is not None for node in spatial),
        "resident_records": sum(record is not None for node in carriers for record in node.records),
        "carrier_packet_count": len(packets),
        "spatial_packet_count": len(spatial_packets),
        "carrier_slot_capacity": sum(len(node.records) for node in carriers),
        "carrier_output_capacity": sum(len(node.output.packets) for node in carriers),
        "spatial_output_capacity": sum(len(node.output.packets) for node in spatial),
        "physical_owner_graph_bytes": deep_size((carriers, spatial)),
        "carrier_host_index_bytes": sys.getsizeof(world._nodes) + sys.getsizeof(world._links._banks),
        "spatial_host_index_bytes": 0
        if world._spatial is None
        else sys.getsizeof(world._spatial.nodes)
        + sys.getsizeof(world._spatial.links._banks)
        + sys.getsizeof(world._spatial._active),
        "shared_initialization_graph_bytes": deep_size(world.initial),
        "event_history_enabled": world.event_space is not None,
        "model_cost": world.computation_report()["model_operations_cost"],
    }


def measure(kind, count, width, slots):
    baseline = source_fingerprint()
    raw, source, template_sha = configuration(kind, count, width, slots)
    initial = parse_initial_state(raw)
    plain = Simulation(initial)
    plain_start = perf_counter()
    for _ in range(POINTS[-1]):
        plain.step()
    plain_seconds = perf_counter() - plain_start
    del plain
    gc.collect()
    if source_fingerprint() != baseline:
        raise RuntimeError("source fingerprint changed during plain case")
    tracemalloc.start()
    world = Simulation(initial)
    samples = []
    step_seconds = 0.0
    for target in POINTS:
        started = perf_counter()
        while world.tick < target:
            world.step()
        step_seconds += perf_counter() - started
        gc.collect()
        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.reset_peak()
        state = state_metrics(world)
        state.update(traced_current_bytes=current, interval_peak_bytes=peak)
        samples.append(state)
        # Exclude this explicit graph traversal's temporary sets from the next
        # interval's stepping peak; its retained result dictionary is disclosed.
        tracemalloc.reset_peak()
    final = source_fingerprint()
    tracemalloc.stop()
    if final != baseline:
        raise RuntimeError("source fingerprint changed during instrumented case")
    result = {
        "kind": kind,
        "node_count": count,
        "vector_width": width,
        "slots_per_node": slots,
        "degree": 6,
        "ticks": POINTS[-1],
        "source_sha256": baseline,
        "template": source,
        "template_sha256": template_sha,
        "initialization_sha256": sha_json(raw),
        "uninstrumented_step_seconds": plain_seconds,
        "tracemalloc_step_seconds": step_seconds,
        "instrumentation_time_ratio": step_seconds / plain_seconds,
        "samples": samples,
    }
    print(
        json.dumps(
            {
                key: result[key]
                for key in (
                    "kind",
                    "node_count",
                    "vector_width",
                    "slots_per_node",
                    "uninstrumented_step_seconds",
                    "tracemalloc_step_seconds",
                )
            }
        ),
        flush=True,
    )
    return result


def measure_all():
    if ROOT / "src/event_universe/__init__.py" != Path(event_universe.__file__).resolve():
        raise RuntimeError("imported package differs from intended source checkout")
    report = {
        "interpreter": sys.executable,
        "python_version": sys.version,
        "imported_package": event_universe.__file__,
        "checkout": str(ROOT),
        "script": str(Path(__file__).resolve()),
        "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "source_sha256_before": source_fingerprint(),
        "method": "No observer, event graph, frame capture, renderer or saved history. Fixed six ports. GC before sampled host bytes. One plain pass and one tracemalloc pass per case; this is an instrumentation comparison, not a speedup claim.",
        "limits": "tracemalloc excludes native allocator/RSS and begins after parsed configuration allocation. Reachable graph totals use Python object identity and include shared payload reuse; not physical register counts or a complete process memory figure. Tiny retained measurement-list growth and interpreter caches contribute to traced current bytes. Samples at 16/32/64/128/256 compare the same repeated cycle phase.",
        "cases": [],
    }
    cases = [("records", n, 8, 8) for n in (1, 8, 27)]
    cases += [("records", 8, width, 8) for width in (16, 32)]
    cases += [("records", 8, 8, slots) for slots in (16, 32)]
    cases += [("fields", 1, 8, 8), ("fields", 8, 8, 8)]
    for case in cases:
        report["cases"].append(measure(*case))
        OUTPUT.write_text(json.dumps(report, indent=2), encoding="utf-8")
    report["source_sha256_after"] = source_fingerprint()
    report["one_source_tree"] = (
        report["source_sha256_before"] == report["source_sha256_after"]
        and len({case["source_sha256"] for case in report["cases"]}) == 1
    )
    OUTPUT.write_text(json.dumps(report, indent=2), encoding="utf-8")


if __name__ == "__main__":
    validate_output_path(OUTPUT)
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    if OUTPUT.exists():
        raise ValueError("memory report requires a new output file")
    OUTPUT.touch()
    with ArtifactLease(OUTPUT.parent, [OUTPUT]):
        measure_all()
