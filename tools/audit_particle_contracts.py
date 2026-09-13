"""Run bounded particle candidates headlessly with independent exact diagnostics."""

import argparse
import hashlib
import json
import sys
import time
from collections import Counter
from copy import deepcopy
from fractions import Fraction
from pathlib import Path

from event_universe import Simulation
from event_universe.core.disturbance_state import MAX_VALUE
from event_universe.initialization import parse_initial_state
from event_universe.runner import source_fingerprint

ROOT = Path(__file__).resolve().parents[1]
EXAMPLES = ROOT / "examples/particle-contracts"


def load(name):
    return json.loads((EXAMPLES / (name + ".json")).read_text(encoding="utf-8"))


def inventory(world, raw):
    snapshot = world.snapshot()
    records = [r["values"] for c in snapshot["nodes"] for r in c["disturbances"]]
    records.extend(r["values"] for r in snapshot["transfers"])
    momentum = [Fraction(0)] * 3
    energy = Fraction(0)
    for values in records:
        p = [
            Fraction(w) + Fraction(r, values["denominator"][0])
            for w, r in zip(values["whole"], values["remainder"], strict=True)
        ]
        momentum = [a + b for a, b in zip(momentum, p, strict=True)]
        energy += (
            Fraction(values["energy"][0])
            if "energy" in values
            else sum(x * x for x in p) / (2 * values["mass"][0])
        )
    for seed in raw.get("spatial_seeds", []):
        node = world.spatial_values(tuple(seed["position"]))
        # These are names in the audited candidate, not generic engine branches.
        if seed["field"] == "reservoir":
            energy += node["reservoir"]["value"][0]
            momentum = [a + b for a, b in zip(momentum, node["reaction"]["value"], strict=True)]
    return (
        tuple(momentum),
        energy,
        sum(v["mass"][0] for v in records),
        sum(v["charge"][0] for v in records),
    )


def run(name, raw):
    events = Counter()
    displacement = [0] * 3
    trace = hashlib.sha256()
    max_cost = 0
    delayed = 0

    def observe(event):
        nonlocal max_cost, delayed
        events[event["event"]] += 1
        if event["event"] == "sent":
            port = event["port"]
            displacement[port // 2] += 1 if port % 2 == 0 else -1
            assert event["arrival_tick"] - event["tick"] == raw["link_ticks"]
        if event["event"] == "cycle_started":
            cost = event["cost"]
            max_cost = max(max_cost, cost)
            cycles = max(1, (cost + raw["normal_budget"] - 1) // raw["normal_budget"])
            assert event["ready_tick"] - event["tick"] == (cycles - 1) * raw["link_ticks"]
            delayed += int(cycles > 1)
        trace.update(json.dumps(event, sort_keys=True).encode("utf-8"))

    started = time.perf_counter()
    world = Simulation(parse_initial_state(raw), observer=observe)
    initial = inventory(world, raw)
    max_momentum_error = Fraction(0)
    max_energy_error = Fraction(0)
    for _ in range(raw["ticks"]):
        world.step()
        current = inventory(world, raw)
        max_momentum_error = max(
            max_momentum_error, *(abs(a - b) for a, b in zip(current[0], initial[0], strict=True))
        )
        max_energy_error = max(max_energy_error, abs(current[1] - initial[1]))
        assert current == initial, (name, world.tick, initial, current)
    return {
        "case": name,
        "model_id": raw["model_id"],
        "ticks": world.tick,
        "seconds": round(time.perf_counter() - started, 4),
        "events": dict(events),
        "trace_sha256": trace.hexdigest(),
        "sent_displacement": displacement,
        "max_cost": max_cost,
        "delayed_cycles": delayed,
        "max_decoded_momentum_error": str(max_momentum_error),
        "max_total_energy_error": str(max_energy_error),
        "mass_and_charge_conserved": True,
    }


def configurations():
    result = {}
    for name in [
        "electron-positron",
        "electron-proton",
        "proton-neutron",
        "massless-axis",
        "massless-oblique",
        "energy-reservoir",
    ]:
        for link_ticks in [1, 2]:
            raw = load(name)
            raw["link_ticks"] = link_ticks
            if "reservoir" not in name:
                raw["ticks"] = 720 if "massless" not in name else 100
            result[f"{name}-transit-{link_ticks}"] = raw
    entities = load("entities")["entities"]
    for name, properties in entities.items():
        raw = load("electron-proton")
        raw["model_id"] = "bounded-rational-free-" + name + "-v1"
        raw["ticks"] = 240
        raw.pop("interactions")
        kind = deepcopy(raw["disturbance_types"][0])
        kind["name"] = name
        kind["defaults"].update(properties, whole=[properties["mass"], 0, 0])
        raw["disturbance_types"] = [kind]
        raw["seeds"] = [{"position": [8, 8, 8], "type": name}]
        result["free-" + name] = raw
    for scale in [1, 1000, MAX_VALUE]:
        raw = load("massless-axis")
        raw["model_id"] = "balanced-routing-scale-probe-v1"
        raw["ticks"] = 60
        raw["disturbance_types"][0]["transport"] = {
            "mode": "move",
            "routing": "balanced",
            "weights": [scale, 0, scale, 0, 0, 0],
        }
        result["direction-scale-" + str(scale)] = raw
    raw = deepcopy(result["free-electron"])
    raw["normal_budget"] = 100000
    result["free-electron-delayed"] = raw
    raw = load("electron-proton")
    raw["model_id"] = "bounded-rational-coarse-mass-contact-v1"
    raw["ticks"] = 720
    for kind, mass, sign in zip(raw["disturbance_types"], [1, 1836], [1, -1], strict=True):
        kind["defaults"].update(mass=mass, whole=[sign * mass, 0, 0])
    result["coarse-electron-proton"] = raw
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, help="Optional diagnostic JSON; no frames or event files")
    args = parser.parse_args()
    fingerprint = source_fingerprint()
    configs = configurations()
    results = [run(name, raw) for name, raw in configs.items()]
    assert source_fingerprint() == fingerprint
    assert not any(
        name in sys.modules for name in ["PIL", "matplotlib", "event_universe.diagnostics.render"]
    )
    report = {
        "source_sha256": fingerprint,
        "python": sys.version,
        "no_visualization": True,
        "no_frame_recording": True,
        "configurations": configs,
        "results": results,
    }
    if args.output:
        args.output.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(
        json.dumps(
            {
                "cases": len(results),
                "ticks": sum(r["ticks"] for r in results),
                "seconds": round(sum(r["seconds"] for r in results), 4),
                "max_energy_error": max(
                    Fraction(r["max_total_energy_error"]) for r in results
                ).__str__(),
                "max_momentum_error": max(
                    Fraction(r["max_decoded_momentum_error"]) for r in results
                ).__str__(),
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
