"""Configuration-only experiments against the existing simulator; no build."""

import json
from collections import Counter
from datetime import datetime
from fractions import Fraction
from pathlib import Path

from event_universe.retention import ArtifactLease
from event_universe.runner import run_initialization, source_fingerprint

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent

# Logical experiment names select one canonical configuration, never a copied law.
REFERENCE_CONFIGURATIONS = {
    "collision": HERE.parent / "04-unequal-mass-collision.json",
    "three-masses": HERE / "three-masses.json",
    "three-masses-low-budget": HERE / "three-masses-low-budget.json",
    "boundary-periodic": HERE / "boundary-periodic.json",
    "boundary-open": HERE / "boundary-open.json",
}


def main():
    if not __debug__:
        raise RuntimeError("Run without -O so numerical acceptance checks remain enabled")
    output = ROOT / "artifacts" / ("known-entities-" + datetime.now().strftime("%Y%m%d-%H%M%S-%f"))
    before = source_fingerprint()
    results = []
    for name, config in REFERENCE_CONFIGURATIONS.items():
        raw = json.loads(config.read_text())
        folder = output / name
        print("Running " + name, flush=True)
        meta = json.loads(run_initialization(config, folder).read_text())
        state = json.loads((folder / "state.json").read_text())
        counts = Counter()
        delayed = 0
        reactions = 0
        first_receives = {}
        for line in (folder / "events.jsonl").open(encoding="utf-8"):
            event = json.loads(line)
            kind = event["event"]
            counts[kind] += 1
            if kind in ["sent", "spatial_sent"]:
                assert event["arrival_tick"] == event["tick"] + raw["link_ticks"]
            if kind == "cycle_started":
                cost = event["cost"]
                assert cost >= 0
                cycles = max(1, (cost + raw["normal_budget"] - 1) // raw["normal_budget"])
                assert event["ready_tick"] == event["tick"] + (cycles - 1) * raw["link_ticks"]
                delayed += event["ready_tick"] > event["tick"]
            if kind == "spatial_coupled" and event.get("reaction"):
                reactions += 1
            if kind == "received":
                first_receives.setdefault(event["disturbance"], event)
        assert meta["status"] == "completed"
        assert meta["completed_ticks"] == raw["ticks"]
        assert meta["accounting_balanced_at_every_completed_tick"]
        assert meta["display"] == "none"
        assert (folder / "initialization.json").read_bytes() == config.read_bytes()
        assert not list(folder.glob("*.html"))
        records = [
            (cell["position"], record) for cell in state["cells"] for record in cell["disturbances"]
        ]
        if name == "collision":
            bodies = {r["type"]: (p, r["values"]) for p, r in records}
            assert len(bodies) == 2 and not state["transfers"]
            assert bodies["Light body"] == ([3, 7, 7], {"mass": [2], "momentum": [-4, 0, 0]})
            assert bodies["Heavy body"] == ([13, 7, 7], {"mass": [3], "momentum": [9, 0, 0]})
            assert sum(
                Fraction(sum(x * x for x in v["momentum"]), 2 * v["mass"][0]) for p, v in bodies.values()
            ) == Fraction(35, 2)
            assert meta["conserved_at_every_completed_tick"]
        if name.startswith("three-masses"):
            assert len(records) + len(state["transfers"]) == 3
            assert meta["final_totals"]["mass"] == [10]
            assert counts["spatial_sent"] > 0
            if name == "three-masses":
                assert reactions > 0
            if name.endswith("low-budget"):
                assert delayed > 0
        if name == "boundary-periodic":
            by_name = {r["type"]: p for p, r in records}
            assert len(by_name) == 6 and not state["transfers"]
            for seed, definition in zip(raw["seeds"], raw["disturbance_types"], strict=True):
                direction = definition["defaults"]["momentum"]
                for tick, actual in [
                    (1, first_receives[seed["type"]]["position"]),
                    (raw["ticks"], by_name[seed["type"]]),
                ]:
                    assert actual == [
                        (p + tick * d) % n
                        for p, d, n in zip(seed["position"], direction, raw["shape"], strict=True)
                    ]
            assert counts["escaped"] == 0
        if name == "boundary-open":
            assert not records and not state["transfers"]
            assert counts["escaped"] == 6
            assert meta["escaped_totals"] == {"mass": [6], "momentum": [0, 0, 0]}
        row = dict(
            name=name,
            ticks=meta["completed_ticks"],
            seconds=meta["elapsed_seconds"],
            checked=True,
            delayed_cycles=delayed,
            nonzero_field_reactions=reactions,
            events=dict(counts),
            final_totals=meta["final_totals"],
            dissipation=meta["dissipation_totals"],
            escaped=meta["escaped_totals"],
            spatial_accounting=meta.get("spatial_accounting"),
        )
        results.append(row)
        print(json.dumps(row), flush=True)
    assert source_fingerprint() == before
    summary = output / "summary.json"
    summary.write_text(
        json.dumps(dict(source_sha256=before, simulator_unchanged=True, results=results), indent=2)
        + "\n"
    )
    with ArtifactLease(output, [summary.resolve()]):
        pass
    print("PASS: " + str(summary), flush=True)


if __name__ == "__main__":
    main()
