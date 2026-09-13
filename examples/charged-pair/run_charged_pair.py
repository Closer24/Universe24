"""Two charged bodies under a configured sign-dependent field response.

Each body emits a signed scalar spatial field proportional to its charge and
exchanges momentum with the delivered flux of that field, multiplied by its own
charge. The sign rule (like charges pushed apart, unlike charges pulled together)
is supplied here in JSON through the generic spatial coupling contract; the
engine recognizes neither charge nor Coulomb's law. See docs/SPATIAL_COUPLINGS.md
and examples/small-space/source-notes.md for the flux sign convention.

Usage, from the repository root with the project interpreter:

    python examples/charged-pair/run_charged_pair.py [--output artifacts/charged-pair]
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]

SHAPE = [21, 7, 7]
CENTER = 3
LEFT_X, RIGHT_X = 9, 12
EMISSION_PER_CHARGE = 540
RESPONSE_DENOMINATOR = 10


def op(name: str, *args: object) -> dict:
    return {"op": name, "args": list(args)}


FIELDS = [
    {"name": "mass", "components": 1, "units": "mass unit", "signed": False, "conserved": True},
    {"name": "charge", "components": 1, "units": "charge unit", "signed": True, "conserved": True},
    {
        "name": "momentum",
        "components": 3,
        "units": "mass unit times c / 120",
        "signed": True,
        "conserved": True,
        "extensive": True,
        "scale": 120,
    },
    {
        "name": "potential",
        "components": 1,
        "units": "emitted charge-field unit",
        "signed": True,
        "conserved": True,
        "extensive": True,
    },
]

CHARGED_BODY = {
    "name": "charged body",
    "fields": ["mass", "charge", "momentum"],
    "defaults": {"mass": 1, "charge": 1, "momentum": [0, 0, 0]},
    "transport": {
        "mode": "move",
        "direction_field": "momentum",
        "rate": op("min", 120, op("exact_div", op("sum", op("abs", {"field": "momentum"})), {"field": "mass"})),
        "rate_denominator": 120,
    },
}


def configuration(model_id: str, left_charge: int, right_charge: int, ticks: int) -> dict:
    return {
        "schema_version": 1,
        "model_id": model_id,
        "boundary": "open",
        "shape": SHAPE,
        "slots_per_cell": 4,
        "link_ticks": 1,
        "normal_budget": 1_000_000,
        "ticks": ticks,
        "operation_costs": {
            name: 1
            for name in ("receive", "read", "evaluate", "update", "couple", "route", "split", "send", "commit")
        },
        "fields": FIELDS,
        "disturbance_types": [CHARGED_BODY],
        "spatial_fields": [
            {"field": "potential", "baseline": 0, "transport": "outward"},
            {"field": "momentum", "baseline": [0, 0, 0], "transport": "outward"},
        ],
        "emissions": [
            {
                "type": "charged body",
                "field": "potential",
                "amount": op("mul", {"field": "charge"}, EMISSION_PER_CHARGE),
                "denominator": 1,
                "source": True,
            }
        ],
        "spatial_couplings": [
            {
                "name": "charge_times_delivered_flux",
                "type": "charged body",
                "field": "momentum",
                "mode": "exchange",
                "amount": op("neg", op("mul", {"field": "charge"}, {"flux": "potential"})),
                "denominator": RESPONSE_DENOMINATOR,
            }
        ],
        "seeds": [
            {"position": [LEFT_X, CENTER, CENTER], "type": "charged body", "values": {"charge": left_charge}},
            {"position": [RIGHT_X, CENTER, CENTER], "type": "charged body", "values": {"charge": right_charge}},
        ],
    }


EXPERIMENTS = {
    "like-charges": ("Charges (+1, +1): expected to move apart.", configuration("charged-pair-like-v1", 1, 1, 120)),
    "opposite-charges": (
        "Charges (+1, -1): expected to move toward each other.",
        configuration("charged-pair-opposite-v1", 1, -1, 120),
    ),
    "neutral-control": (
        "Charges (0, 0): no emission and no response; expected to stay put.",
        configuration("charged-pair-neutral-control-v1", 0, 0, 120),
    ),
}


def run(name: str, output: Path) -> tuple[int, str]:
    completed = subprocess.run(
        [sys.executable, "-m", "event_universe", "--init", str(HERE / f"{name}.json"), "--output", str(output)],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    return completed.returncode, (completed.stdout + completed.stderr).strip()


def summarize(name: str, output: Path, returncode: int, console: str) -> None:
    description, config = EXPERIMENTS[name]
    print(f"\n=== {name} ===")
    print(description)
    run_path = output / "run.json"
    if not run_path.exists():
        print(f"exit code {returncode}; no run.json written\n{console[-1500:]}")
        return
    result = json.loads(run_path.read_text(encoding="utf-8"))
    print(f"status: {result['status']}  ticks: {result['completed_ticks']}/{result['requested_ticks']}")
    if result["error"]:
        print(f"error: {result['error']}")
    print(f"momentum totals (carriers + field, all in-transit): initial {result['initial_totals']['momentum']}  final {result['final_totals']['momentum']}")
    print(f"charge totals: initial {result['initial_totals']['charge']}  final {result['final_totals']['charge']}")
    print(f"accounting balanced every tick: {result['accounting_balanced_at_every_completed_tick']}")

    # Track each body by its seed x order: "L" started at LEFT_X, "R" at RIGHT_X.
    position = {"L": [LEFT_X, CENTER, CENTER], "R": [RIGHT_X, CENTER, CENTER]}
    momentum = {"L": [0, 0, 0], "R": [0, 0, 0]}
    history: list[tuple[int, int, int, list[int], list[int]]] = [(0, LEFT_X, RIGHT_X, [0, 0, 0], [0, 0, 0])]
    coupled_samples: list[dict] = []
    for line in (output / "events.jsonl").read_text(encoding="utf-8").splitlines():
        event = json.loads(line)
        kind = event.get("event")
        if kind == "spatial_coupled" and len(coupled_samples) < 2:
            coupled_samples.append(event)
        if kind not in {"sent", "received"}:
            continue
        # Identify which body: the one whose last known position matches the event cell.
        who = next((k for k, p in position.items() if p == event["position"]), None)
        if kind == "sent":
            if who is None:
                continue
            momentum[who] = event["values"]["momentum"]
            position[who] = None  # in transit
        else:
            who = next((k for k, p in position.items() if p is None), None)
            if who is None:
                continue
            position[who] = event["position"]
            momentum[who] = event["values"]["momentum"]
        history.append((event["tick"], (position["L"] or [None])[0], (position["R"] or [None])[0], momentum["L"], momentum["R"]))

    print("  tick   xL   xR  distance   pL           pR")
    shown = set()
    for tick, xl, xr, pl, pr in history:
        if xl is None or xr is None or tick in shown:
            continue
        shown.add(tick)
        print(f"  {tick:>4}  {xl:>3}  {xr:>3}  {abs(xr - xl):>5}     {str(pl):<12} {str(pr)}")

    state = json.loads((output / "state.json").read_text(encoding="utf-8"))
    for cell in state["cells"]:
        for record in cell["disturbances"]:
            v = record["values"]
            print(f"  final: charge {v['charge'][0]:+d} at {cell['position']} momentum {v['momentum']}")
    if coupled_samples:
        print(f"  first spatial_coupled event: {json.dumps(coupled_samples[0])[:300]}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--output", default="artifacts/charged-pair")
    args = parser.parse_args()
    base = (ROOT / args.output).resolve()
    for name, (_, config) in EXPERIMENTS.items():
        (HERE / f"{name}.json").write_text(json.dumps(config, indent=2) + "\n", encoding="utf-8")
    for name in EXPERIMENTS:
        output = base / name
        code, console = run(name, output)
        summarize(name, output, code, console)


if __name__ == "__main__":
    main()
