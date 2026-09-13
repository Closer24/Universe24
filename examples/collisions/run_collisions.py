"""Build, run and summarize configured collision experiments.

Each experiment is a schema 1 initialization with named mass/momentum fields
and an atomic pair interaction supplied in JSON. Nothing here is an engine law.
The scenarios follow Highlights 3.5.2 (local collisions) and 3.5.4 (shared
checks): equal and unequal masses, opposing velocities, a target at rest, an
unrepresentable integer outcome, a declared inelastic energy exchange and
two- and three-particle contact.

Usage, from the repository root with the project interpreter:

    python examples/collisions/run_collisions.py [--output artifacts/collisions]
"""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]

SHAPE = [21, 7, 7]
Y, Z = 3, 3


def reflect(axis: int) -> list[list[int]]:
    return [[-1 if i == j == axis else int(i == j) for j in range(3)] for i in range(3)]


def field(name: str, side: str) -> dict:
    return {"field": name, "side": side}


def op(name: str, *args: object, **extra: object) -> dict:
    node: dict = {"op": name, "args": list(args)}
    node.update(extra)
    return node


def mass(side: str) -> dict:
    return field("mass", side)


def momentum(side: str) -> dict:
    return field("momentum", side)


def total_mass() -> dict:
    return op("add", mass("left"), mass("right"))


def total_momentum() -> dict:
    return op("add", momentum("left"), momentum("right"))


def relative_momentum() -> dict:
    # D = mR * pL - mL * pR; a positive component along the contact axis means approach.
    return op(
        "sub",
        op("mul", mass("right"), momentum("left")),
        op("mul", mass("left"), momentum("right")),
    )


def approaching(axis: int = 0) -> dict:
    return op("gt", op("component", relative_momentum(), index=axis), 0)


def elastic_assignments(axis: int = 0) -> list[dict]:
    reflected = op("transform", relative_momentum(), matrix=reflect(axis))
    return [
        {
            "side": "left",
            "field": "momentum",
            "expression": op(
                "exact_div",
                op("add", op("mul", mass("left"), total_momentum()), reflected),
                total_mass(),
            ),
        },
        {
            "side": "right",
            "field": "momentum",
            "expression": op(
                "exact_div",
                op("sub", op("mul", mass("right"), total_momentum()), reflected),
                total_mass(),
            ),
        },
    ]


def elastic_invariants() -> list[dict]:
    return [
        {"name": "left_mass", "expression": mass("left")},
        {"name": "right_mass", "expression": mass("right")},
        {"name": "total_momentum", "expression": total_momentum()},
        {
            "name": "kinetic_energy_scaled",
            "expression": op(
                "add",
                op("mul", mass("right"), op("dot", momentum("left"), momentum("left"))),
                op("mul", mass("left"), op("dot", momentum("right"), momentum("right"))),
            ),
        },
    ]


def elastic_rule(name: str, left: str, right: str, axis: int = 0) -> dict:
    return {
        "name": name,
        "left_type": left,
        "right_type": right,
        "when": approaching(axis),
        "assignments": elastic_assignments(axis),
        "invariants": elastic_invariants(),
    }


def twice_kinetic(side: str) -> dict:
    return op("exact_div", op("dot", momentum(side), momentum(side)), mass(side))


def inelastic_rule(name: str, left: str, right: str) -> dict:
    shared = op("exact_div", op("dot", total_momentum(), total_momentum()), total_mass())
    loss = op("sub", op("add", twice_kinetic("left"), twice_kinetic("right")), shared)
    half_loss = op("exact_div", loss, 2)
    return {
        "name": name,
        "left_type": left,
        "right_type": right,
        "when": approaching(),
        "assignments": [
            {
                "side": "left",
                "field": "momentum",
                "expression": op("exact_div", op("mul", mass("left"), total_momentum()), total_mass()),
            },
            {
                "side": "right",
                "field": "momentum",
                "expression": op("exact_div", op("mul", mass("right"), total_momentum()), total_mass()),
            },
            {"side": "left", "field": "heat", "expression": op("add", field("heat", "left"), half_loss)},
            {
                "side": "right",
                "field": "heat",
                "expression": op("add", field("heat", "right"), half_loss),
            },
        ],
        "invariants": [
            {"name": "left_mass", "expression": mass("left")},
            {"name": "right_mass", "expression": mass("right")},
            {"name": "total_momentum", "expression": total_momentum()},
            {
                "name": "total_energy_twice",
                "expression": op(
                    "add",
                    op("add", field("heat", "left"), field("heat", "right")),
                    op("add", twice_kinetic("left"), twice_kinetic("right")),
                ),
            },
        ],
    }


MASS_FIELD = {"name": "mass", "components": 1, "units": "mass unit", "signed": False, "conserved": True}
MOMENTUM_FIELD = {
    "name": "momentum",
    "components": 3,
    "units": "mass unit times c / 120",
    "signed": True,
    "conserved": True,
    "scale": 120,
}
HEAT_FIELD = {
    "name": "heat",
    "components": 1,
    "units": "momentum squared per mass unit (twice kinetic energy)",
    "signed": False,
    "conserved": False,
    "extensive": False,
}

MOVE_BY_MOMENTUM = {
    "mode": "move",
    "direction_field": "momentum",
    "rate": op("exact_div", op("sum", op("abs", {"field": "momentum"})), {"field": "mass"}),
    "rate_denominator": 120,
}


def body(name: str, m: int, p: int | list[int], *extra_fields: str, **extra_defaults: object) -> dict:
    defaults: dict = {"mass": m, "momentum": [p, 0, 0] if isinstance(p, int) else list(p)}
    defaults.update(extra_defaults)
    return {
        "name": name,
        "fields": ["mass", "momentum", *extra_fields],
        "defaults": defaults,
        "transport": MOVE_BY_MOMENTUM,
    }


def seed(name: str, x: int, y: int = Y, z: int = Z) -> dict:
    return {"position": [x, y, z], "type": name}


def configuration(
    model_id: str, ticks: int, fields: list, types: list, rules: list, seeds: list
) -> dict:
    return {
        "schema_version": 1,
        "model_id": model_id,
        "shape": SHAPE,
        "slots_per_node": 4,
        "link_ticks": 1,
        "normal_budget": 10000,
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
        "fields": fields,
        "disturbance_types": types,
        "couplings": [],
        "interactions": rules,
        "seeds": seeds,
    }


EXPERIMENTS: dict[str, tuple[str, dict]] = {
    "01-equal-mass-head-on": (
        "Equal masses, opposing velocities. Elastic outcome: momenta swap.",
        configuration(
            "collision-equal-mass-elastic-head-on-v1",
            240,
            [MASS_FIELD, MOMENTUM_FIELD],
            [body("Body A", 1, 4), body("Body B", 1, -4)],
            [elastic_rule("elastic_contact", "Body A", "Body B")],
            [seed("Body A", 3), seed("Body B", 11)],
        ),
    ),
    "02-light-into-heavy-at-rest": (
        "Light body (m=1, p=6) strikes a heavy body (m=3) at rest. Elastic: (-3, 9).",
        configuration(
            "collision-light-into-heavy-rest-elastic-v1",
            240,
            [MASS_FIELD, MOMENTUM_FIELD],
            [body("Light body", 1, 6), body("Heavy target", 3, 0)],
            [elastic_rule("elastic_contact", "Light body", "Heavy target")],
            [seed("Light body", 2), seed("Heavy target", 7)],
        ),
    ),
    "03-nonintegral-outcome-rejected": (
        "Masses (2,3), momenta (4,-3). Elastic result -16/5 is not an integer; exact_div must fault.",
        configuration(
            "collision-nonintegral-elastic-outcome-v1",
            360,
            [MASS_FIELD, MOMENTUM_FIELD],
            [body("Body A", 2, 4), body("Body B", 3, -3)],
            [elastic_rule("elastic_contact", "Body A", "Body B")],
            [seed("Body A", 2), seed("Body B", 8)],
        ),
    ),
    "04-perfectly-inelastic": (
        "Equal masses (4, -2) stick: shared momentum 1 each, lost kinetic energy declared as heat 9 each.",
        configuration(
            "collision-perfectly-inelastic-declared-heat-v1",
            360,
            [MASS_FIELD, MOMENTUM_FIELD, HEAT_FIELD],
            [body("Body A", 1, 4, "heat", heat=0), body("Body B", 1, -2, "heat", heat=0)],
            [inelastic_rule("sticking_contact", "Body A", "Body B")],
            [seed("Body A", 3), seed("Body B", 9)],
        ),
    ),
    "05-three-body-simultaneous": (
        "Outer bodies (+4, -4) reach a resting middle body in the same tick; three pairwise elastic rules.",
        configuration(
            "collision-three-body-simultaneous-elastic-v1",
            300,
            [MASS_FIELD, MOMENTUM_FIELD],
            [body("Left body", 1, 4), body("Middle body", 1, 0), body("Right body", 1, -4)],
            [
                elastic_rule("left_middle", "Left body", "Middle body"),
                elastic_rule("middle_right", "Middle body", "Right body"),
                elastic_rule("left_right", "Left body", "Right body"),
            ],
            [seed("Left body", 6), seed("Middle body", 10), seed("Right body", 14)],
        ),
    ),
    "06-newton-cradle-chain": (
        "One moving body passes momentum through two resting equal masses in sequence.",
        configuration(
            "collision-sequential-chain-elastic-v1",
            360,
            [MASS_FIELD, MOMENTUM_FIELD],
            [body("Striker", 1, 4), body("First rest", 1, 0), body("Second rest", 1, 0)],
            [
                elastic_rule("striker_first", "Striker", "First rest"),
                elastic_rule("first_second", "First rest", "Second rest"),
                elastic_rule("striker_second", "Striker", "Second rest"),
            ],
            [seed("Striker", 2), seed("First rest", 6), seed("Second rest", 9)],
        ),
    ),
    "07-oblique-contact-along-x": (
        "Momenta (4,2,0) and (-4,2,0): the x contact component reflects, the shared y drift is retained.",
        configuration(
            "collision-oblique-x-normal-elastic-v1",
            240,
            [MASS_FIELD, MOMENTUM_FIELD],
            [body("Body A", 1, [4, 2, 0]), body("Body B", 1, [-4, 2, 0])],
            [elastic_rule("elastic_contact", "Body A", "Body B", axis=0)],
            [seed("Body A", 3, 1, 3), seed("Body B", 11, 1, 3)],
        ),
    ),
    "08-head-on-along-z": (
        "Experiment 01 rotated onto the z axis: momenta (0,0,4) and (0,0,-4) with a z reflection.",
        configuration(
            "collision-equal-mass-elastic-head-on-z-v1",
            240,
            [MASS_FIELD, MOMENTUM_FIELD],
            [body("Body A", 1, [0, 0, 4]), body("Body B", 1, [0, 0, -4])],
            [elastic_rule("elastic_contact", "Body A", "Body B", axis=2)],
            [seed("Body A", 10, 3, 1), seed("Body B", 10, 3, 5)],
        ),
    ),
    "09-three-axis-oblique": (
        "Momenta (4,1,1) and (-4,1,1): only the x contact component reflects; y and z components ride through.",
        configuration(
            "collision-oblique-three-axis-elastic-v1",
            240,
            [MASS_FIELD, MOMENTUM_FIELD],
            [body("Body A", 1, [4, 1, 1]), body("Body B", 1, [-4, 1, 1])],
            [elastic_rule("elastic_contact", "Body A", "Body B", axis=0)],
            [seed("Body A", 3, 2, 2), seed("Body B", 11, 2, 2)],
        ),
    ),
}


def write_inputs() -> None:
    for name, (_, config) in EXPERIMENTS.items():
        (HERE / f"{name}.json").write_text(json.dumps(config, indent=2) + "\n", encoding="utf-8")


def run(name: str, output: Path) -> tuple[int, str]:
    shutil.rmtree(output, ignore_errors=True)
    completed = subprocess.run(
        [
            sys.executable,
            "-m",
            "event_universe",
            "--init",
            str(HERE / f"{name}.json"),
            "--output",
            str(output),
        ],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    return completed.returncode, (completed.stdout + completed.stderr).strip()


def vec(values: dict) -> str:
    return "(" + ",".join(str(v) for v in values["momentum"]) + ")"


def pos(position: list[int]) -> str:
    return "(" + ",".join(str(v) for v in position) + ")"


def summarize(name: str, output: Path, returncode: int, console: str) -> None:
    description, config = EXPERIMENTS[name]
    print(f"\n=== {name} ===")
    print(description)
    run_path = output / "run.json"
    if not run_path.exists():
        print(f"exit code {returncode}; no run.json written")
        print(console[-1200:])
        return
    result = json.loads(run_path.read_text(encoding="utf-8"))
    print(f"status: {result['status']}  ticks: {result['completed_ticks']}/{result['requested_ticks']}")
    if result["error"]:
        print(f"error: {result['error']}")
    print(f"totals: initial {result['initial_totals']}  final {result['final_totals']}")
    print(
        f"conserved every tick: {result['conserved_at_every_completed_tick']}  "
        f"accounting balanced: {result['accounting_balanced_at_every_completed_tick']}"
    )

    defaults = {kind["name"]: kind["defaults"] for kind in config["disturbance_types"]}
    last: dict[str, dict] = {}
    where: dict[str, list[int]] = {}
    for entry in config["seeds"]:
        last[entry["type"]] = {"momentum": defaults[entry["type"]]["momentum"]}
        where[entry["type"]] = entry["position"]
        print(
            f"  {entry['type']:<14} starts at {pos(entry['position']):<10} momentum {vec(last[entry['type']])}"
        )

    events_path = output / "events.jsonl"
    if events_path.exists():
        for line in events_path.read_text(encoding="utf-8").splitlines():
            event = json.loads(line)
            kind = event.get("event")
            if kind not in {"sent", "received"}:
                continue
            body_name = event["disturbance"]
            if kind == "received":
                where[body_name] = event["position"]
            if event["values"]["momentum"] != last[body_name]["momentum"]:
                print(
                    f"  tick {event['tick']:>4}: {body_name:<14} at {pos(event['position']):<10} "
                    f"momentum {vec(last[body_name])} -> {vec(event['values'])}"
                )
                last[body_name] = event["values"]

    state_path = output / "state.json"
    if state_path.exists():
        state = json.loads(state_path.read_text(encoding="utf-8"))
        for node in state["nodes"]:
            for record in node["disturbances"]:
                values = record["values"]
                extra = f"  heat {values['heat'][0]}" if "heat" in values else ""
                print(
                    f"  final: {record['type']:<14} at {pos(node['position']):<10} "
                    f"mass {values['mass'][0]} momentum {vec(values)}{extra}"
                )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--output", default="artifacts/collisions")
    args = parser.parse_args()
    base = (ROOT / args.output).resolve()
    write_inputs()
    for name in EXPERIMENTS:
        output = base / name
        code, console = run(name, output)
        summarize(name, output, code, console)


if __name__ == "__main__":
    main()
