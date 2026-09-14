"""Quantum-to-classical probes: where the finite quantum rules meet the classical ones.

Three host-side measurements on existing laws only; no engine rule is added and
no physical constant is identified.

1. A one-excitation walk on the finite event network. Coherent hopping spreads
   ballistically (width proportional to time). Discarding the position record
   after every step turns the same walk into the classical random walk, whose
   width grows as the square root of time and whose distribution equals the
   classical Markov chain exactly. Rarer discards interpolate between the two.
2. Single quanta on the straight-ray field. One quantum leaves per tick in a
   scrambled direction; a detector Node sees only whole clicks, and the click
   rate over a full sweep is the classical inverse-square flux.
3. Repeated capture attempts at one detector. A delocalized charge meets a 3:4
   mixer once per pass; over many independent worlds the capture tick follows
   the geometric decay law with survival 9/25 per pass, and charge and mass stay
   exact through every quantum episode.

Every number is a read-only world/event audit at host coordinates; no
operational observer is modeled and no ticket comes from a physical device.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
from collections import Counter
from copy import deepcopy
from fractions import Fraction
from pathlib import Path

from event_universe import Simulation
from event_universe.initialization import parse_initial_state
from event_universe.quantum import Amplitude, DeferredQuantum, EventNetworkConfig, LocalUnitary
from event_universe.quantum.operations import dephasing
from event_universe.runner import prepare_initialization, source_fingerprint

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]

WALK_NODES = 25
WALK_STEPS = 14
DISCARD_EVERY = (0, 4, 2, 1)  # 0 never discards the position record

COUNT_SIZE = 21
COUNT_CENTER = COUNT_SIZE // 2
COUNT_HEADINGS = 4096
HEADING_SCALE = 24
GOLDEN_STRIDE = 2531  # round(4096 / golden ratio), odd: a permutation of the sweep
DETECTOR_RADII = (2, 3, 4, 6, 8)
WINDOWS = (64, 256, 1024)

CAPTURE_TRIALS = 2000
CAPTURE_TICKS = 16
PASS_PERIOD = 4  # the charge meets the detector's mixer every four ticks


# --- 1. Quantum walk ----------------------------------------------------------


def hop() -> LocalUnitary:
    """Number-preserving neighbor mixer with equal weights: (|10> +- |01>) / sqrt 2."""
    z, o, n, v = Amplitude(0, 0), Amplitude(1, 0), Amplitude(-1, 0), Amplitude(1, 1)
    return LocalUnitary(((v, z, z, z), (z, o, o, z), (z, o, n, z), (z, z, z, v)))


def walk(steps: int, discard_every: int, nodes: int = WALK_NODES) -> list[dict]:
    """Alternate even and odd bonds; optionally discard every position record."""
    network = DeferredQuantum().bind_event_network(
        EventNetworkConfig(tuple((x, 0, 0) for x in range(nodes)), (nodes // 2,))
    )
    mixer = hop()
    rows = []
    for step in range(steps):
        network.step(tuple((mixer, (i, i + 1)) for i in range(step % 2, nodes - 1, 2)))
        if discard_every and (step + 1) % discard_every == 0:
            network.step(tuple((dephasing(2), (i,)) for i in range(nodes)))
        occupation = []
        for i in range(nodes):
            weights = network.query(i).weights
            occupation.append(Fraction(weights[1], sum(weights)))
        mean = sum(i * p for i, p in enumerate(occupation))
        variance = sum((i - mean) ** 2 * p for i, p in enumerate(occupation))
        rows.append(
            {
                "step": step + 1,
                "total": str(sum(occupation)),
                "mean_offset": str(mean - nodes // 2),
                "variance": str(variance),
                "width": round(math.sqrt(variance), 4),
                "occupation": [str(p) for p in occupation],
            }
        )
    return rows


def classical_walk(steps: int, nodes: int = WALK_NODES) -> list[dict]:
    """The Markov chain a fully dephased walk must equal: cross the active bond with 1/2."""
    p = [Fraction(0)] * nodes
    p[nodes // 2] = Fraction(1)
    rows = []
    for step in range(steps):
        q = [Fraction(0)] * nodes
        for i in range(nodes):
            if not p[i]:
                continue
            j = i + 1 if (i - step) % 2 == 0 else i - 1
            if 0 <= j < nodes:
                q[i] += p[i] / 2
                q[j] += p[i] / 2
            else:
                q[i] += p[i]
        p = q
        mean = sum(i * v for i, v in enumerate(p))
        variance = sum((i - mean) ** 2 * v for i, v in enumerate(p))
        rows.append({"step": step + 1, "variance": str(variance), "occupation": [str(v) for v in p]})
    return rows


def fit_exponent(points: list[tuple[float, float]]) -> float | None:
    usable = [(math.log(x), math.log(y)) for x, y in points if x > 0 and y > 0]
    if len(usable) < 2:
        return None
    n = len(usable)
    mx = sum(x for x, _ in usable) / n
    my = sum(y for _, y in usable) / n
    sxx = sum((x - mx) ** 2 for x, _ in usable)
    sxy = sum((x - mx) * (y - my) for x, y in usable)
    return sxy / sxx if sxx else None


def walk_probe() -> dict:
    result: dict = {"nodes": WALK_NODES, "steps": WALK_STEPS, "runs": {}}
    classical = classical_walk(WALK_STEPS)
    for every in DISCARD_EVERY:
        rows = walk(WALK_STEPS, every)
        late = [(row["step"], row["width"]) for row in rows if row["step"] >= 4]
        result["runs"][f"discard_every_{every}"] = {
            "rows": rows,
            "width_exponent_from_step_4": fit_exponent(late),
            "equals_classical_chain": [r["occupation"] for r in rows]
            == [c["occupation"] for c in classical],
        }
    result["classical_chain"] = classical
    return result


# --- 2. Single-quantum counting -------------------------------------------------


def golden_headings(count: int, scale: int) -> list[list[int]]:
    ratio = (1 + 5**0.5) / 2
    result = []
    for i in range(count):
        z = 1 - 2 * (i + 0.5) / count
        radius = math.sqrt(1 - z * z)
        angle = 2 * math.pi * i / ratio
        heading = [
            round(scale * radius * math.cos(angle)),
            round(scale * radius * math.sin(angle)),
            round(scale * z),
        ]
        result.append(heading if any(heading) else [scale, 0, 0])
    return result


def scrambled_headings(count: int, scale: int) -> list[list[int]]:
    """Golden-spiral headings in golden-stride order: consecutive quanta are unrelated."""
    ordered = golden_headings(count, scale)
    return [ordered[(k * GOLDEN_STRIDE) % count] for k in range(count)]


def counting_document(ticks: int, headings: list[list[int]]) -> dict:
    return {
        "schema_version": 1,
        "model_id": "single-quantum-counting-probe-v1",
        "shape": [COUNT_SIZE] * 3,
        "boundary": "open",
        "slots_per_node": 2,
        "link_ticks": 1,
        "normal_budget": 100000,
        "ticks": ticks,
        "operation_costs": {
            name: 1
            for name in (
                "receive",
                "read",
                "evaluate",
                "update",
                "couple",
                "route",
                "split",
                "send",
                "commit",
            )
        },
        "fields": [
            {
                "name": "quanta",
                "components": 1,
                "units": "quantum",
                "signed": False,
                "conserved": True,
                "extensive": True,
            }
        ],
        "disturbance_types": [
            {
                "name": "source",
                "fields": ["quanta"],
                "defaults": {"quanta": 1},
                "transport": {"mode": "hold"},
            }
        ],
        "spatial_fields": [
            {
                "field": "quanta",
                "baseline": 0,
                "transport": "ray",
                "headings": headings,
                "rays_per_tick": 1,
                "ray_slots": 64,
            }
        ],
        "emissions": [
            {"type": "source", "field": "quanta", "amount": 1, "denominator": 1, "source": True}
        ],
        "seeds": [{"position": [COUNT_CENTER] * 3, "type": "source"}],
    }


def counting_probe(ticks: int = COUNT_HEADINGS, radii: tuple[int, ...] = DETECTOR_RADII) -> dict:
    raw = counting_document(ticks, scrambled_headings(COUNT_HEADINGS, HEADING_SCALE))
    world = Simulation(parse_initial_state(raw))
    # Six detector Nodes per radius, one on each axis; a click is a quantum at any of them.
    detectors = {
        r: [
            tuple(COUNT_CENTER + r * sign * int(axis == k) for k in range(3))
            for axis in range(3)
            for sign in (1, -1)
        ]
        for r in radii
    }
    clicks: dict[int, list[int]] = {r: [] for r in radii}
    click_values: dict[int, set[int]] = {r: set() for r in radii}
    for _ in range(ticks):
        world.step()
        for r, positions in detectors.items():
            values = [world.spatial_values(p)["quanta"]["value"][0] for p in positions]
            click_values[r].update(values)
            clicks[r].append(sum(values))
    rows = []
    for r, series in clicks.items():
        total = sum(series)
        windows = {}
        for width in WINDOWS:
            counts = [sum(series[i : i + width]) for i in range(0, ticks, width)]
            mean = sum(counts) / len(counts)
            variance = sum((c - mean) ** 2 for c in counts) / len(counts)
            windows[str(width)] = {
                "counts": counts if len(counts) <= 16 else counts[:16],
                "mean": round(mean, 4),
                "variance": round(variance, 4),
                "relative_spread": round(math.sqrt(variance) / mean, 4) if mean else None,
            }
        rows.append(
            {
                "host_r": r,
                "detectors": 6,
                "click_values": sorted(click_values[r]),
                "clicks_per_sweep": total,
                "rate_per_detector": round(total / ticks / 6, 6),
                "rate_times_r2": round(total / ticks / 6 * r * r, 4),
                "windows": windows,
            }
        )
    return {
        "ticks": ticks,
        "headings": COUNT_HEADINGS,
        "rows": rows,
        "rate_exponent": fit_exponent([(row["host_r"], row["rate_per_detector"]) for row in rows]),
        "totals": {name: list(values) for name, values in world.totals().items()},
        "escaped": {name: list(values) for name, values in world.escaped_totals().items()},
    }


# --- 3. Repeated capture attempts -----------------------------------------------


def capture_document(ticks: int) -> dict:
    raw = json.loads((ROOT / "examples/quantum/causal_charge.json").read_text())
    raw["ticks"] = ticks
    raw["event_program"].pop("tickets", None)
    return raw


def capture_trial(document: dict, seed: int) -> dict:
    raw = deepcopy(document)
    raw["event_program"]["seed"] = seed
    prepared = prepare_initialization(raw)
    with Simulation(prepared.initial) as world:
        for _ in range(raw["ticks"]):
            world.step()
            stock = world.totals()
            if stock["charge"] != (-1,) or stock["mass"] != (1,):
                raise AssertionError(f"charge or mass changed at tick {world.tick} of seed {seed}")
        report = world.computation_report()["resolver"]
        captures = [e for e in report["contact_transfers"] if e["direction"] == "to_localized"]
    if len(captures) > 1:
        raise AssertionError(f"more than one capture in seed {seed}")
    return {"seed": seed, "capture_tick": captures[0]["tick"] if captures else None}


def capture_probe(trials: int = CAPTURE_TRIALS, ticks: int = CAPTURE_TICKS) -> dict:
    document = capture_document(ticks)
    outcomes = [capture_trial(document, seed) for seed in range(1, trials + 1)]
    counts = Counter(o["capture_tick"] for o in outcomes)
    passes = list(range(ticks // PASS_PERIOD))
    click, survive = Fraction(16, 25), Fraction(9, 25)
    rows = []
    for k in passes:
        tick = 3 + PASS_PERIOD * k
        expected = click * survive**k
        rows.append(
            {
                "pass": k + 1,
                "capture_tick": tick,
                "observed": counts.get(tick, 0),
                "observed_fraction": round(counts.get(tick, 0) / trials, 4),
                "geometric_law": str(expected),
                "geometric_fraction": round(float(expected), 4),
            }
        )
    uncaptured_expected = survive ** len(passes)
    captured = [o["capture_tick"] for o in outcomes if o["capture_tick"] is not None]
    mean_pass = sum((t - 3) // PASS_PERIOD + 1 for t in captured) / len(captured) if captured else None
    return {
        "trials": trials,
        "ticks": ticks,
        "rows": rows,
        "uncaptured": {
            "observed": counts.get(None, 0),
            "observed_fraction": round(counts.get(None, 0) / trials, 4),
            "geometric_law": str(uncaptured_expected),
            "geometric_fraction": round(float(uncaptured_expected), 4),
        },
        "mean_pass_of_captured": None if mean_pass is None else round(mean_pass, 4),
        "mean_pass_geometric": str(1 / (1 - survive)),
        "conserved_every_tick": {"charge": -1, "mass": 1},
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    result = {
        "source_sha256": source_fingerprint(),
        "probe_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "measurement_scope": "read-only world/event audit",
        "walk": walk_probe(),
        "counting": counting_probe(),
        "capture": capture_probe(),
    }
    (args.output / "summary.json").write_text(json.dumps(result, indent=2) + "\n")
    for name, run in result["walk"]["runs"].items():  # type: ignore[union-attr]
        print(
            name,
            "width exponent",
            round(run["width_exponent_from_step_4"], 3),
            "widths",
            [row["width"] for row in run["rows"]][::2],
            "classical",
            run["equals_classical_chain"],
        )
    for row in result["counting"]["rows"]:  # type: ignore[index]
        print("r", row["host_r"], "clicks", row["clicks_per_sweep"], "rate x r^2", row["rate_times_r2"])
    print("rate exponent", result["counting"]["rate_exponent"])  # type: ignore[index]
    for row in result["capture"]["rows"]:  # type: ignore[index]
        print(
            "pass",
            row["pass"],
            "observed",
            row["observed_fraction"],
            "geometric",
            row["geometric_fraction"],
        )
    print("uncaptured", result["capture"]["uncaptured"])  # type: ignore[index]
    print("Wrote report: " + str(args.output / "summary.json"))


if __name__ == "__main__":
    main()
