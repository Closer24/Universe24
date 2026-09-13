"""Repeat a declared contact experiment without changing the simulator's laws."""

import argparse
import hashlib
import json
import time
from collections import Counter
from copy import deepcopy
from pathlib import Path

from event_universe import Simulation
from event_universe.configuration_validation import prepare_initialization
from event_universe.retention import ArtifactLease, validate_output_path
from event_universe.runner import run_initialization, source_fingerprint


def geometry(document):
    program = document["event_program"]
    addresses = program["addresses"]
    return [
        {
            "name": domain["name"],
            "source": addresses[domain["source"]["register_index"]],
            "hub": addresses[domain["register_indices"][1]],
            "targets": {
                letter: addresses[index]
                for letter, index in zip("ABC", domain["capture"]["register_indices"], strict=True)
            },
        }
        for domain in program["domains"]
    ]


def one_trial(document, seed, *, record=False):
    raw = deepcopy(document)
    raw["event_program"]["seed"] = seed
    prepared = prepare_initialization(raw)
    layout = geometry(raw)
    targets = {
        (domain["name"], tuple(address)): letter
        for domain in layout
        for letter, address in domain["targets"].items()
    }
    started = time.perf_counter()
    frames = []
    with Simulation(prepared.initial) as world:
        initial = world.totals()

        def snapshot():
            report = world.computation_report()["resolver"]
            return {
                **world.snapshot(),
                "source_envelopes": report["source_envelopes"],
                "contact_transfers": deepcopy(report["contact_transfers"]),
            }

        if record:
            frames.append(snapshot())
        for _ in range(raw["ticks"]):
            world.step()
            stock = world.totals()
            sources, losses, escaped = (
                world.source_totals(),
                world.dissipation_totals(),
                world.escaped_totals(),
            )
            for name, before in initial.items():
                assert tuple(a + b for a, b in zip(before, sources[name], strict=True)) == tuple(
                    a + b + c for a, b, c in zip(stock[name], losses[name], escaped[name], strict=True)
                ), (seed, world.tick, name)
            assert stock["charge"] == (-6,) and stock["mass"] == (24,), (seed, world.tick)
            assert all(item["balanced"] for item in world.spatial_accounting().values())
            if record:
                frames.append(snapshot())
        report = world.computation_report()["resolver"]
        captures = [
            {**event, "outcome": targets[event["domain"], tuple(event["address"])]}
            for event in report["contact_transfers"]
            if event["direction"] == "to_localized"
        ]
        assert Counter(event["domain"] for event in captures) == Counter(d["name"] for d in layout)
        assert all(event["tick"] == {"A": 3, "B": 5, "C": 7}[event["outcome"]] for event in captures)
        assert all(node["retired"] for node in report["source_envelopes"])
        assert report["quantum_inventory"]["charge"] == (0,)
        result = {
            "seed": seed,
            "ticks": world.tick,
            "elapsed_seconds": time.perf_counter() - started,
            "captures": captures,
            "charge": stock["charge"],
            "mass": stock["mass"],
            "source_totals": sources,
            "final_totals": stock,
            "dissipation_totals": losses,
            "escaped_totals": escaped,
            "accounting_balanced": True,
            "all_envelopes_retired": True,
            "random_draws": report["random_draws"],
            "causal_events": len(world.event_space.events),
        }
    return result, frames


def run_experiment(initialization, output, *, trials=200, visualize=False):
    if type(trials) is not int or not 1 <= trials <= 1000:
        raise ValueError("choose one through one thousand independent repetitions")
    source = initialization.read_bytes()
    document = json.loads(source)
    prepare_initialization(document)
    validate_output_path(output)
    if output.exists() and any(output.iterdir()):
        raise ValueError("use a new or empty experiment output directory")
    output.mkdir(parents=True, exist_ok=True)
    fingerprint = source_fingerprint()
    seed_start = document["event_program"]["seed"]
    started = time.perf_counter()
    representative = output / "representative"
    run_initialization(initialization, representative, visualize=visualize)
    trial_path, summary_path = output / "trials.jsonl", output / "summary.json"
    trial_path.touch()
    summary_path.touch()
    # Share the runner's registry after its writer closes, rather than owning
    # a parent directory around a nested active runner lease.
    with ArtifactLease(output, [representative.resolve(), trial_path.resolve(), summary_path.resolve()]):
        results = []
        with (output / "trials.jsonl").open("w", encoding="utf-8") as stream:
            for index in range(trials):
                raw = deepcopy(document)
                # The representative continues longer to check that capture
                # remains one-shot. Every repetition runs through cancellation.
                if index:
                    raw["ticks"] = 12
                result, frames = one_trial(raw, seed_start + index, record=visualize and index == 0)
                results.append(result)
                stream.write(json.dumps(result) + "\n")
                stream.flush()
                if frames:
                    (representative / "frames.json").write_text(json.dumps(frames), encoding="utf-8")
                if (index + 1) % 25 == 0:
                    print(f"Completed {index + 1}/{trials} independent trials", flush=True)
        primary = json.loads((representative / "run.json").read_text(encoding="utf-8"))
        primary_captures = [
            event
            for event in primary["computation"]["resolver"]["contact_transfers"]
            if event["direction"] == "to_localized"
        ]
        observed = [{k: v for k, v in e.items() if k != "outcome"} for e in results[0]["captures"]]
        assert primary_captures == json.loads(json.dumps(observed))
        assert primary["final_totals"] == json.loads(json.dumps(results[0]["final_totals"]))
        counts = Counter(event["outcome"] for result in results for event in result["captures"])
        summary = {
            "model": document["model_id"],
            "source_sha256": fingerprint,
            "initialization_sha256": hashlib.sha256(source).hexdigest(),
            "trial_count": trials,
            "total_captures": sum(counts.values()),
            "seed_start": seed_start,
            "expected_probabilities": {"A": 16 / 25, "B": 144 / 625, "C": 81 / 625},
            "counts": {letter: counts[letter] for letter in "ABC"},
            "domains": geometry(document),
            "trials": results,
            "elapsed_seconds": time.perf_counter() - started,
            "independent_domains": True,
            "repeated_hops_observed": False,
            "simultaneous_quantum_particles": 6,
            "target_particles": 18,
            "preparation_partners": 6,
        }
        assert source_fingerprint() == fingerprint
        (output / "summary.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    return summary


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--init", type=Path, default=Path(__file__).with_suffix(".json"))
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--trials", type=int, default=200)
    parser.add_argument("--visualize", action="store_true")
    args = parser.parse_args()
    result = run_experiment(args.init, args.output, trials=args.trials, visualize=args.visualize)
    print(
        json.dumps(
            {key: result[key] for key in ("trial_count", "total_captures", "counts", "elapsed_seconds")}
        )
    )
