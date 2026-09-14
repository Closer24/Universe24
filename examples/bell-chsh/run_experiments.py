"""Bell's test on the ray: a CHSH measurement of two phased rays from one source.

Two records at one Node each emit one quantum, one toward Alice along -x and
one toward Bob along +x, with a shared hidden phase: Alice's ray carries
lambda, Bob's lambda plus a half turn. Each side has a "plus" detector where a
reference lamp lands one quantum per tick at the detector's setting phase, so
the coherence of the arriving ray with the reference is cos^2 of half their
phase difference and the lottery capture takes the ray with that probability
(Malus's law on the Kerengonen coherence); a ray not taken walks on to a
"minus" detector that takes it surely. Every capture opens a claim, so the
surviving root of each train says where that quantum landed. Over every
hidden phase and many capture seeds, for the four CHSH setting pairs, the
correlations E(a, b) and S = |E(a,b) - E(a,b') + E(a',b) + E(a',b')| are
measured against the local bound 2 and the quantum value 2 sqrt 2. Every
number is a read-only world/event audit at host lattice coordinates; no
angle unit or constant is identified: a setting is a phase step.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path

from event_universe import Simulation
from event_universe.initialization import parse_initial_state
from event_universe.runner import source_fingerprint

WIDTH = 13
CENTER = WIDTH // 2
DISTANCE = 3  # links from the source to each plus detector; the minus detector is one further
PHASE_STEPS = 64
HALF_TURN = PHASE_STEPS // 2
# CHSH settings as phase steps: Alice 0 and a quarter turn, Bob an eighth and three eighths.
SETTINGS = {"a": 0, "a2": 16, "b": 8, "b2": 24}
PAIRS = (("a", "b"), ("a", "b2"), ("a2", "b"), ("a2", "b2"))
SEEDS = 16
TICKS = DISTANCE + 6
COSTS = {
    name: 1
    for name in ("receive", "read", "evaluate", "update", "couple", "route", "split", "send", "commit")
}


def document(hidden_phase: int, alice: int, bob: int, seed: int, ticks: int = TICKS) -> dict:
    """One pair at hidden phase lambda, detector settings for Alice and Bob, one capture seed."""
    body = {
        "fields": ["quanta", "momentum"],
        "defaults": {"quanta": 0, "momentum": [0, 0, 0]},
        "transport": {"mode": "hold"},
    }
    plus_alice, plus_bob = CENTER - DISTANCE, CENTER + DISTANCE
    return {
        "schema_version": 1,
        "model_id": "bell-chsh-ray-probe-v1",
        "shape": [WIDTH, 3, 3],
        "boundary": "open",
        "slots_per_node": 2,
        "link_ticks": 1,
        "normal_budget": 100000,
        "ticks": ticks,
        "operation_costs": COSTS,
        "fields": [
            {
                "name": "quanta",
                "components": 1,
                "units": "quantum",
                "signed": False,
                "conserved": True,
                "extensive": True,
            },
            {
                "name": "momentum",
                "components": 3,
                "units": "quantum times heading",
                "signed": True,
                "conserved": True,
                "extensive": True,
            },
            {
                "name": "train",
                "components": 1,
                "units": "label",
                "signed": False,
                "conserved": False,
                "extensive": False,
            },
        ],
        "disturbance_types": [
            {
                "name": "source_alice",
                "fields": ["quanta", "momentum", "train"],
                "defaults": {"quanta": 1, "momentum": [0, 0, 0], "train": 1},
                "transport": {"mode": "hold"},
            },
            {
                "name": "source_bob",
                "fields": ["quanta", "momentum", "train"],
                "defaults": {"quanta": 1, "momentum": [0, 0, 0], "train": 2},
                "transport": {"mode": "hold"},
            },
            {
                "name": "reference_alice",
                "fields": ["quanta", "momentum"],
                "defaults": {"quanta": ticks, "momentum": [0, 0, 0]},
                "transport": {"mode": "hold"},
            },
            {
                "name": "reference_bob",
                "fields": ["quanta", "momentum"],
                "defaults": {"quanta": ticks, "momentum": [0, 0, 0]},
                "transport": {"mode": "hold"},
            },
            {"name": "plus_alice", **body},
            {"name": "minus_alice", **body},
            {"name": "plus_bob", **body},
            {"name": "minus_bob", **body},
        ],
        "spatial_fields": [
            {
                "field": "quanta",
                "baseline": 0,
                "transport": "ray",
                "headings": [[-1, 0, 0], [1, 0, 0], [0, -1, 0]],
                "rays_per_tick": 1,
                "ray_slots": 8,
                "kerengonen": {
                    "phase_steps": PHASE_STEPS,
                    "phase_advance": 0,
                    "capture": "lottery",
                    "capture_seed": seed,
                },
                "claim": {"ticks": 4 * ticks, "slots": 4},
            }
        ],
        "emissions": [
            {
                "type": "source_alice",
                "field": "quanta",
                "amount": 1,
                "denominator": 1,
                "source": False,
                "recoil_field": "momentum",
                "kerengonen_phase": hidden_phase % PHASE_STEPS,
                "train_field": "train",
                "heading": [-1, 0, 0],
            },
            {
                "type": "source_bob",
                "field": "quanta",
                "amount": 1,
                "denominator": 1,
                "source": False,
                "recoil_field": "momentum",
                "kerengonen_phase": (hidden_phase + HALF_TURN) % PHASE_STEPS,
                "train_field": "train",
                "heading": [1, 0, 0],
            },
            {
                "type": "reference_alice",
                "field": "quanta",
                "amount": 1,
                "denominator": 1,
                "source": False,
                "recoil_field": "momentum",
                "kerengonen_phase": alice % PHASE_STEPS,
                "heading": [0, -1, 0],
            },
            {
                "type": "reference_bob",
                "field": "quanta",
                "amount": 1,
                "denominator": 1,
                "source": False,
                "recoil_field": "momentum",
                "kerengonen_phase": bob % PHASE_STEPS,
                "heading": [0, -1, 0],
            },
        ],
        "spatial_couplings": [
            {
                "name": f"{name}_absorbs",
                "field": "quanta",
                "mode": "absorb",
                "momentum_field": "momentum",
                "claim": True,
                # Each detector draws its own ticket sequence: two devices, two dice.
                "capture_salt": salt,
                "type": name,
            }
            for name, salt in (
                ("plus_alice", 0),
                ("minus_alice", 1),
                ("plus_bob", 2),
                ("minus_bob", 3),
            )
        ],
        "seeds": [
            {"position": [CENTER, 1, 1], "type": "source_alice"},
            {"position": [CENTER, 1, 1], "type": "source_bob"},
            {"position": [plus_alice, 1, 1], "type": "plus_alice"},
            {"position": [plus_alice - 1, 1, 1], "type": "minus_alice"},
            {"position": [plus_alice, 2, 1], "type": "reference_alice"},
            {"position": [plus_bob, 1, 1], "type": "plus_bob"},
            {"position": [plus_bob + 1, 1, 1], "type": "minus_bob"},
            {"position": [plus_bob, 2, 1], "type": "reference_bob"},
        ],
    }


def outcomes(raw: dict) -> dict:
    """Where each train landed: +1 at a plus detector, -1 at a minus detector."""
    world = Simulation(parse_initial_state(raw))
    initial = world.totals()["quanta"][0]
    for _ in range(raw["ticks"]):
        world.step()
    names = [kind["name"] for kind in raw["disturbance_types"]]
    detectors = {
        node.position: names[record.type_index]
        for node in world.inventory_view().nodes
        for record in node.records
        if record is not None and names[record.type_index].split("_")[0] in ("plus", "minus")
    }
    landed: dict[int, int] = {}
    for node in world.inventory_view().nodes:
        for claim in node.claims[0] if node.claims else ():
            if claim.parent < 0:
                landed[claim.train] = 1 if str(detectors.get(claim.origin)).startswith("plus") else -1
    escaped = world.escaped_totals()["quanta"][0]
    return {
        "alice": landed.get(1),
        "bob": landed.get(2),
        "closed": world.totals()["quanta"][0] + escaped == initial,
    }


def correlation(alice: int, bob: int, seeds: int = SEEDS) -> dict:
    """E(a, b) over every hidden phase and the given number of capture seeds."""
    total = count = 0
    plus_alice = plus_bob = 0
    missing = 0
    closed = True
    for hidden in range(PHASE_STEPS):
        for seed in range(1, seeds + 1):
            result = outcomes(document(hidden, alice, bob, seed))
            closed = closed and result["closed"]
            if result["alice"] is None or result["bob"] is None:
                missing += 1
                continue
            total += result["alice"] * result["bob"]
            count += 1
            plus_alice += result["alice"] > 0
            plus_bob += result["bob"] > 0
    predicted = -0.5 * math.cos(2 * math.pi * (alice - bob) / PHASE_STEPS)
    return {
        "alice": alice,
        "bob": bob,
        "pairs": count,
        "missing": missing,
        "E": round(total / count, 4) if count else None,
        "predicted_E": round(predicted, 4),
        "quantum_E": round(-math.cos(2 * math.pi * (alice - bob) / PHASE_STEPS), 4),
        "alice_plus_rate": round(plus_alice / count, 4) if count else None,
        "bob_plus_rate": round(plus_bob / count, 4) if count else None,
        "closed": closed,
    }


def chsh(seeds: int = SEEDS) -> dict:
    results = {
        f"{left},{right}": correlation(SETTINGS[left], SETTINGS[right], seeds) for left, right in PAIRS
    }
    e = {key: value["E"] for key, value in results.items()}
    s = abs(e["a,b"] - e["a,b2"] + e["a2,b"] + e["a2,b2"])
    predicted = abs(
        results["a,b"]["predicted_E"]
        - results["a,b2"]["predicted_E"]
        + results["a2,b"]["predicted_E"]
        + results["a2,b2"]["predicted_E"]
    )
    quantum = abs(
        results["a,b"]["quantum_E"]
        - results["a,b2"]["quantum_E"]
        + results["a2,b"]["quantum_E"]
        + results["a2,b2"]["quantum_E"]
    )
    return {
        "settings": SETTINGS,
        "seeds": seeds,
        "correlations": results,
        "S": round(s, 4),
        "predicted_S": round(predicted, 4),
        "local_bound": 2,
        "quantum_S": round(quantum, 4),
        "same_setting_E": correlation(0, 0, seeds)["E"],
        "closed": all(value["closed"] for value in results.values()),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--seeds", type=int, default=SEEDS)
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    result = chsh(args.seeds)
    report = {
        "source_sha256": source_fingerprint(),
        "probe_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "measurement_scope": "read-only world/event audit",
        "phase_steps": PHASE_STEPS,
        **result,
    }
    (args.output / "summary.json").write_text(json.dumps(report, indent=2) + "\n")
    for key, value in result["correlations"].items():
        print(
            key,
            "E",
            value["E"],
            "predicted",
            value["predicted_E"],
            "quantum",
            value["quantum_E"],
            "plus rates",
            value["alice_plus_rate"],
            value["bob_plus_rate"],
            "missing",
            value["missing"],
            "closed",
            value["closed"],
        )
    print(
        "S",
        result["S"],
        "predicted",
        result["predicted_S"],
        "local bound",
        result["local_bound"],
        "quantum",
        result["quantum_S"],
        "same setting E",
        result["same_setting_E"],
    )
    print("Wrote report: " + str(args.output / "summary.json"))


if __name__ == "__main__":
    main()
