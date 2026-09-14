"""Kerengonen Bell test: the CHSH form on a local phased-ray field, against the quantum owner.

Configuration only on the `kerengonen-ray-field-v1` candidate. A funded source at
the centre fires one ray toward each wing every tick; both rays carry the same
hidden phase. On each wing a reference lamp fires across the ray at the analyzer
Node with the wing's setting as its phase, and the analyzer absorbs the coherent
share of what meets there. The absorbed part of the source ray is the outcome +1,
the part that passes is -1. Correlations are averaged over the hidden phase, and
the CHSH combination is compared with the value 14/5 the finite quantum owner
records at the same settings in `examples/quantum` (Bell CHSH experiment). Every
number is a read-only world audit at host lattice coordinates; no physical
constant, wavelength or species is identified.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from fractions import Fraction
from pathlib import Path

from event_universe import Simulation
from event_universe.core.spatial_state import PHASE_COSINE_SCALE, phase_cosines
from event_universe.initialization import parse_initial_state
from event_universe.runner import source_fingerprint

SIZE_X = 15
CENTER_X = SIZE_X // 2
SIZE_Y = 7
CENTER_Y = SIZE_Y // 2
DISTANCE = 3  # source to analyzer, lamp to analyzer: equal links, equal phase advance
PHASE_STEPS = 360
PER_RAY = 1024  # a multiple of 256: every coherent share is an exact integer
TICKS = 24
ARRIVAL = DISTANCE  # ticks before the first rays reach the analyzers
LOTTERY_TICKS = 96
HEADINGS = [[1, 0, 0], [-1, 0, 0], [0, 1, 0], [0, -1, 0]]
# The quantum owner's settings, Alice Z or X and Bob (3Z +- 4X)/5, as phases on a
# 360-step circle: 0, 90, +53 and -53 degrees (arctan(4/3) = 53.13 degrees).
ALICE = {"a0": 0, "a1": 90}
BOB = {"b0": 53, "b1": 307}
PAIRS = (("a0", "b0"), ("a0", "b1"), ("a1", "b0"), ("a1", "b1"))
SIGNS = {("a0", "b0"): 1, ("a0", "b1"): 1, ("a1", "b0"): 1, ("a1", "b1"): -1}
QUANTUM_OWNER = {
    ("a0", "b0"): Fraction(3, 5),
    ("a0", "b1"): Fraction(3, 5),
    ("a1", "b0"): Fraction(4, 5),
    ("a1", "b1"): Fraction(-4, 5),
}
SHARE_GRID = 5  # hidden phase every five steps: 72 worlds per setting pair
LOTTERY_GRID = 15  # 24 worlds per setting pair, single quanta
LOTTERY_SEED = 11
COSTS = {
    name: 1
    for name in ("receive", "read", "evaluate", "update", "couple", "route", "split", "send", "commit")
}
TYPES = ("source", "lamp_a", "lamp_b", "analyzer_a", "analyzer_b")


def document(
    hidden_phase: int,
    setting_a: int,
    setting_b: int,
    *,
    per_ray: int = PER_RAY,
    ticks: int = TICKS,
    phase_steps: int = PHASE_STEPS,
    capture_seed: int | None = None,
    audit: bool = False,
) -> dict:
    """One world: a source with a hidden phase between two analyzers lit by setting lamps."""
    stock = len(HEADINGS) * per_ray * ticks
    field: dict = {
        "field": "quanta",
        "baseline": 0,
        "transport": "ray",
        "headings": HEADINGS,
        "rays_per_tick": len(HEADINGS),
        "ray_slots": 8,
    }
    if phase_steps:
        field["kerengonen"] = {"phase_steps": phase_steps, "phase_advance": 1}
        if capture_seed is not None:
            field["kerengonen"].update({"capture": "lottery", "capture_seed": capture_seed})

    def kind(name: str, quanta: int) -> dict:
        return {
            "name": name,
            "fields": ["quanta", "momentum"],
            "defaults": {"quanta": quanta, "momentum": [0, 0, 0]},
            "transport": {"mode": "hold"},
        }

    def emission(name: str, phase: int) -> dict:
        rule: dict = {
            "type": name,
            "field": "quanta",
            "amount": len(HEADINGS) * per_ray,
            "denominator": 1,
            "source": False,
            "recoil_field": "momentum",
        }
        if phase_steps:
            rule["kerengonen_phase"] = phase % phase_steps
        return rule

    raw: dict = {
        "schema_version": 1,
        "model_id": "kerengonen-bell-probe-v1",
        "shape": [SIZE_X, SIZE_Y, 3],
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
        ],
        "disturbance_types": [
            kind(name, stock if name in ("source", "lamp_a", "lamp_b") else 0) for name in TYPES
        ],
        "spatial_fields": [field],
        "emissions": [
            emission("source", hidden_phase),
            emission("lamp_a", setting_a),
            emission("lamp_b", setting_b),
        ],
        "spatial_couplings": [
            {
                "name": f"{name}_absorbs",
                "type": name,
                "field": "quanta",
                "mode": "absorb",
                "momentum_field": "momentum",
            }
            for name in ("analyzer_a", "analyzer_b")
        ],
        "seeds": [
            {"position": [CENTER_X, CENTER_Y, 1], "type": "source"},
            {"position": [CENTER_X - DISTANCE, CENTER_Y - DISTANCE, 1], "type": "lamp_a"},
            {"position": [CENTER_X + DISTANCE, CENTER_Y - DISTANCE, 1], "type": "lamp_b"},
            {"position": [CENTER_X - DISTANCE, CENTER_Y, 1], "type": "analyzer_a"},
            {"position": [CENTER_X + DISTANCE, CENTER_Y, 1], "type": "analyzer_b"},
        ],
    }
    if audit:
        raw["conservation"] = {
            "name": "quanta",
            "energy_units": "quantum",
            "momentum_units": "quantum times heading",
            "carriers": [
                {
                    "requires": ["quanta", "momentum"],
                    "energy": {"field": "quanta"},
                    "momentum": {"field": "momentum"},
                }
            ],
            "spatial": {
                "energy": {"field": "quanta", "side": "right"},
                "momentum": {"op": "vector", "args": [0, 0, 0]},
            },
        }
    return raw


def analyzers(world: Simulation) -> dict[str, tuple[int, int, int]]:
    """Quanta and momentum absorbed so far by each analyzer.

    The source ray reaches analyzer A heading -x and analyzer B heading +x; each
    lamp ray heads +y. The x momentum therefore counts the absorbed source quanta
    and the y momentum the absorbed lamp quanta, separately.
    """
    out = {}
    for node in world.nodes.values():
        for record in node.records:
            if record is not None and TYPES[record.type_index].startswith("analyzer"):
                values = world.record_values(record)
                out[TYPES[record.type_index]] = (
                    values["quanta"][0],
                    values["momentum"][0],
                    values["momentum"][1],
                )
    return out


def source_absorbed(state: dict[str, tuple[int, int, int]]) -> tuple[int, int]:
    """Absorbed source quanta at A and B from the x momentum."""
    return (-state["analyzer_a"][1], state["analyzer_b"][1])


def run_share(raw: dict) -> dict:
    """Run one world and return each wing's absorbed source share as an exact fraction."""
    world = Simulation(parse_initial_state(raw))
    initial = world.totals()["quanta"][0]
    for _ in range(raw["ticks"]):
        world.step()
    state = analyzers(world)
    sent = raw["emissions"][0]["amount"] // len(HEADINGS) * (raw["ticks"] - ARRIVAL)
    absorbed = source_absorbed(state)
    totals, escaped = world.totals(), world.escaped_totals()
    return {
        "absorbed_source": list(absorbed),
        "absorbed_lamp": [state["analyzer_a"][2], state["analyzer_b"][2]],
        "sent_per_wing": sent,
        "share": [Fraction(value, sent) for value in absorbed],
        "quanta_closed": totals["quanta"][0] + escaped["quanta"][0] == initial,
        **({"audit": world.conservation_report()["status"]} if "conservation" in raw else {}),
    }


def run_lottery(raw: dict) -> dict:
    """Run one single-quantum world tick by tick and record the click at each wing."""
    world = Simulation(parse_initial_state(raw))
    initial = world.totals()["quanta"][0]
    previous = (0, 0)
    clicks: list[tuple[int, int]] = []
    for tick in range(raw["ticks"]):
        world.step()
        current = source_absorbed(analyzers(world))
        if tick >= ARRIVAL:
            clicks.append((current[0] - previous[0], current[1] - previous[1]))
        previous = current
    totals, escaped = world.totals(), world.escaped_totals()
    assert all(a in (0, 1) and b in (0, 1) for a, b in clicks)
    return {
        "clicks": clicks,
        "coincidence_sum": sum((2 * a - 1) * (2 * b - 1) for a, b in clicks),
        "pairs": len(clicks),
        "quanta_closed": totals["quanta"][0] + escaped["quanta"][0] == initial,
    }


def model_outcome(difference: int, phase_steps: int = PHASE_STEPS) -> Fraction:
    """The expected outcome, 2 x coherent share - 1, of one wing at a phase difference.

    Two equal rays at phase difference d have coherence (1 + cos d) / 2 on the
    field's fixed-point table, so the outcome expectation is the table cosine.
    """
    return Fraction(phase_cosines(phase_steps)[difference % phase_steps], PHASE_COSINE_SCALE)


def model_correlation(
    setting_a: int, setting_b: int, grid: int, phase_steps: int = PHASE_STEPS
) -> Fraction:
    """The local model's correlation: the hidden phase averaged over the grid."""
    phases = range(0, phase_steps, grid)
    return sum(
        (
            model_outcome(phase - setting_a, phase_steps) * model_outcome(phase - setting_b, phase_steps)
            for phase in phases
        ),
        Fraction(0),
    ) / len(phases)


def chsh(correlations: dict[tuple[str, str], Fraction]) -> Fraction:
    return sum((SIGNS[pair] * correlations[pair] for pair in PAIRS), Fraction(0))


def share_correlations(
    grid: int = SHARE_GRID, *, phase_steps: int = PHASE_STEPS, ticks: int = TICKS
) -> dict:
    """Exact correlations from the share rule: one world per hidden phase and setting pair."""
    result: dict = {"correlations": {}, "closed": True, "worlds": 0}
    for pair in PAIRS:
        a, b = ALICE[pair[0]], BOB[pair[1]]
        products = []
        for hidden in range(0, phase_steps, grid):
            run = run_share(document(hidden, a, b, phase_steps=phase_steps, ticks=ticks))
            result["closed"] = result["closed"] and run["quanta_closed"]
            result["worlds"] += 1
            outcome_a, outcome_b = (2 * share - 1 for share in run["share"])
            products.append(outcome_a * outcome_b)
        result["correlations"][pair] = sum(products, Fraction(0)) / len(products)
    result["S"] = chsh(result["correlations"])
    return result


def lottery_correlations(
    grid: int = LOTTERY_GRID, *, ticks: int = LOTTERY_TICKS, seed: int = LOTTERY_SEED
) -> dict:
    """Click coincidences from the lottery rule: whole single quanta, one pair per tick."""
    result: dict = {"correlations": {}, "closed": True, "worlds": 0, "pairs_per_setting": 0}
    for pair in PAIRS:
        a, b = ALICE[pair[0]], BOB[pair[1]]
        total, count = 0, 0
        for hidden in range(0, PHASE_STEPS, grid):
            run = run_lottery(document(hidden, a, b, per_ray=1, ticks=ticks, capture_seed=seed))
            result["closed"] = result["closed"] and run["quanta_closed"]
            result["worlds"] += 1
            total += run["coincidence_sum"]
            count += run["pairs"]
        result["correlations"][pair] = Fraction(total, count)
        result["pairs_per_setting"] = count
    result["S"] = chsh(result["correlations"])
    return result


def plain_correlations(*, ticks: int = TICKS) -> dict:
    """The same worlds without the key: every ray is absorbed whole, the outcome is always +1."""
    result: dict = {"correlations": {}, "closed": True}
    for pair in PAIRS:
        run = run_share(document(0, ALICE[pair[0]], BOB[pair[1]], phase_steps=0, ticks=ticks))
        result["closed"] = result["closed"] and run["quanta_closed"]
        outcome_a, outcome_b = (2 * share - 1 for share in run["share"])
        result["correlations"][pair] = outcome_a * outcome_b
    result["S"] = chsh(result["correlations"])
    return result


def serial(value: object) -> object:
    if isinstance(value, Fraction):
        return {"numerator": value.numerator, "denominator": value.denominator, "value": float(value)}
    if isinstance(value, dict):
        return {"/".join(k) if isinstance(k, tuple) else str(k): serial(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [serial(v) for v in value]
    return value


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--share-grid", type=int, default=SHARE_GRID)
    parser.add_argument("--lottery-grid", type=int, default=LOTTERY_GRID)
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    model = {pair: model_correlation(ALICE[pair[0]], BOB[pair[1]], args.share_grid) for pair in PAIRS}
    exact_model = {pair: model_correlation(ALICE[pair[0]], BOB[pair[1]], 1) for pair in PAIRS}
    share = share_correlations(args.share_grid)
    lottery = lottery_correlations(args.lottery_grid)
    plain = plain_correlations()
    audited = run_share(document(0, 0, 0, audit=True))
    result = {
        "source_sha256": source_fingerprint(),
        "probe_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "measurement_scope": "read-only world audit",
        "phase_steps": PHASE_STEPS,
        "settings": {"alice": ALICE, "bob": BOB, "signs": SIGNS},
        "per_ray": PER_RAY,
        "ticks": TICKS,
        "share_grid": args.share_grid,
        "lottery_grid": args.lottery_grid,
        "lottery_ticks": LOTTERY_TICKS,
        "lottery_seed": LOTTERY_SEED,
        "model": {"correlations": model, "S": chsh(model)},
        "model_full_circle": {"correlations": exact_model, "S": chsh(exact_model)},
        "share": share,
        "lottery": lottery,
        "plain": plain,
        "quantum_owner": {"correlations": QUANTUM_OWNER, "S": chsh(QUANTUM_OWNER)},
        "local_bound": 2,
        "audited": audited,
    }
    (args.output / "summary.json").write_text(json.dumps(serial(result), indent=2) + "\n")
    for pair in PAIRS:
        print(
            pair,
            "model",
            model[pair],
            "share",
            share["correlations"][pair],
            "lottery",
            lottery["correlations"][pair],
            "plain",
            plain["correlations"][pair],
            "quantum",
            QUANTUM_OWNER[pair],
        )
    print("S model", chsh(model), float(chsh(model)), "full circle", float(chsh(exact_model)))
    print("S share", share["S"], float(share["S"]), "worlds", share["worlds"], "closed", share["closed"])
    print(
        "S lottery",
        lottery["S"],
        float(lottery["S"]),
        "pairs",
        lottery["pairs_per_setting"],
        "closed",
        lottery["closed"],
    )
    print("S plain", plain["S"], "quantum owner", chsh(QUANTUM_OWNER), "bound", 2)
    print("audited", audited)
    print("Wrote report: " + str(args.output / "summary.json"))


if __name__ == "__main__":
    main()
