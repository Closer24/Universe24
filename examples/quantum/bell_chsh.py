"""Bell test in CHSH form with two spatially separated wings on the lattice.

This is an experiment harness, not another evolution engine. Every measured
number comes from the canonical runner under ``local-quantum-events-v2``: the
decision weights and outcomes recorded by the quantum owner, and the classical
outcome codes written into the detector records at the two wings. Analytic
targets are computed here with exact rational arithmetic on the configured
matrices, independently of the update code, before the runs are read.

Layout: ten registers on one line, x = 8 ... 17. A Hadamard on x = 12 and a
controlled-NOT on (12, 13) prepare the Bell pair. Configured SWAP gates then
carry one member to x = 8 and the other to x = 17, one Link per tick. Two
detector bodies travel inward from the boundaries and reach the wings at the
same tick, nine Links apart, so no Link signal connects the two decisions.
Each wing measures with its own configured instrument; the classical outcome
code is written into the detector record that triggered it.

Settings: Alice measures Z or X. Bob measures (3Z + 4X)/5 or (3Z - 4X)/5, the
closest 3-4-5 rational stand-ins for the optimal (Z +/- X)/sqrt(2). The exact
CHSH value of these settings is 14/5 = 2.8, above the local bound 2 and below
the Tsirelson bound 2 sqrt(2), which no rational setting can reach.
"""

import argparse
import json
import platform
import shutil
from fractions import Fraction
from itertools import product
from pathlib import Path

from event_universe.retention import ArtifactLease, validate_output_path
from event_universe.runner import run_initialization, source_fingerprint

HERE = Path(__file__).resolve().parent
TEMPLATE = HERE / "bell_chsh.json"
ALICE_WING, BOB_WING = 8, 17
ALICE_REGISTER, BOB_REGISTER = 0, 9
MEASUREMENT_TICK = 8
ENVIRONMENT_TICK = 3
# Observables as integer matrices with a positive integer scale: O / scale has eigenvalues +1 and -1.
ALICE_SETTINGS = {"a0": ([[1, 0], [0, -1]], 1), "a1": ([[0, 1], [1, 0]], 1)}
BOB_SETTINGS = {"b0": ([[3, 4], [4, -3]], 5), "b1": ([[3, -4], [-4, -3]], 5)}
SETTINGS = list(product(ALICE_SETTINGS, BOB_SETTINGS))
# CHSH combination: E(a0 b0) + E(a0 b1) + E(a1 b0) - E(a1 b1).
CHSH_SIGNS = {("a0", "b0"): 1, ("a0", "b1"): 1, ("a1", "b0"): 1, ("a1", "b1"): -1}
LOCAL_BOUND = Fraction(2)
DEPHASING = [[[1, 0], [0, 0]], [[0, 0], [0, 1]]]
OUTCOME_CODES = [1, 2]


def instrument(observable, scale):
    """Kraus pair (scale I + O, scale I - O): projectors onto the +1 and -1 eigenspaces, times 2 scale."""
    return [
        [[scale * int(i == j) + sign * observable[i][j] for j in range(2)] for i in range(2)]
        for sign in (1, -1)
    ]


def projectors(observable, scale):
    """Exact rational projectors (I +/- O / scale) / 2 for outcomes 0 (+1) and 1 (-1)."""
    return [
        [
            [(Fraction(int(i == j)) + sign * Fraction(observable[i][j], scale)) / 2 for j in range(2)]
            for i in range(2)
        ]
        for sign in (1, -1)
    ]


def density(environment):
    """Two-register density matrix of (|00> + |11>) / sqrt(2), optionally dephased on the first register."""
    rho = {
        (0, 0): Fraction(1, 2),
        (0, 3): Fraction(1, 2),
        (3, 0): Fraction(1, 2),
        (3, 3): Fraction(1, 2),
    }
    if environment == "dephased":
        # A discarded basis record on one member removes the coherence between |00> and |11>.
        rho = {key: value for key, value in rho.items() if key[0] == key[1]}
    return rho


def joint_probability(rho, alice, bob):
    """Tr(rho (P_a x P_b)) with little-endian basis keys: key = alice_level + 2 * bob_level."""
    total = Fraction(0)
    for (row, column), value in rho.items():
        a_row, b_row = row % 2, row // 2
        a_col, b_col = column % 2, column // 2
        total += value * alice[a_col][a_row] * bob[b_col][b_row]
    return total


def analytic(environment="bell"):
    """Exact joint distributions, correlations and CHSH value for the configured settings."""
    rho = density(environment)
    correlations = {}
    joints = {}
    for a, b in SETTINGS:
        alice = projectors(*ALICE_SETTINGS[a])
        bob = projectors(*BOB_SETTINGS[b])
        joint = {(i, j): joint_probability(rho, alice[i], bob[j]) for i in (0, 1) for j in (0, 1)}
        assert sum(joint.values()) == 1
        joints[a + b] = {f"{i}{j}": str(p) for (i, j), p in joint.items()}
        correlations[a + b] = sum((1 if i == j else -1) * p for (i, j), p in joint.items())
    chsh = sum(CHSH_SIGNS[a, b] * correlations[a + b] for a, b in SETTINGS)
    return {
        "environment": environment,
        "joint_probabilities": joints,
        "correlations": {key: str(value) for key, value in correlations.items()},
        "chsh": str(chsh),
        "violates_local_bound": chsh > LOCAL_BOUND,
    }


def configuration(a, b, *, tickets=None, seed=0, environment="bell"):
    raw = json.loads(TEMPLATE.read_text(encoding="utf-8"))
    program = raw["event_program"]
    for binding, (name, table) in zip(
        program["bindings"], ((a, ALICE_SETTINGS), (b, BOB_SETTINGS)), strict=True
    ):
        binding["instrument"] = instrument(*table[name])
    program.pop("tickets", None)
    if tickets is not None:
        program["tickets"] = list(tickets)
    program["seed"] = seed
    if environment == "dephased":
        layers = program["layers"]
        source = [op["register_indices"][0] for op in layers[0]["operations"]]
        layers.insert(
            2,
            {
                "tick": ENVIRONMENT_TICK,
                "operations": [{"register_indices": source, "channel": DEPHASING}],
            },
        )
        assert [layer["tick"] for layer in layers] == sorted(layer["tick"] for layer in layers)
    return raw


def wing_link_distance(raw):
    addresses = raw["event_program"]["addresses"]
    return sum(
        abs(p - q) for p, q in zip(addresses[ALICE_REGISTER], addresses[BOB_REGISTER], strict=True)
    )


def run_case(name, raw, output):
    case_dir = output / name
    if case_dir.exists():
        shutil.rmtree(case_dir)
    output.mkdir(parents=True, exist_ok=True)
    initialization = output / (name + ".json")
    initialization.write_text(json.dumps(raw, indent=1) + "\n", encoding="utf-8")
    run_initialization(initialization, case_dir)
    report = json.loads((case_dir / "run.json").read_text(encoding="utf-8"))
    assert report["status"] == "completed", report["error"]
    assert report["conserved_at_every_completed_tick"]
    assert report["final_totals"]["mass"] == [2] and report["final_totals"]["momentum"] == [0, 0, 0]
    resolver = report["computation"]["resolver"]
    decisions = {}
    for record in resolver["records"]:
        register = record["decision"]["register_index"]
        assert register not in decisions, "one decision per wing"
        decisions[register] = {
            "tick": record["decision"]["tick"],
            "weights": record["decision"]["weights"],
            "outcome": record["outcome"],
            "event_id": record["event_id"],
        }
    assert set(decisions) == {ALICE_REGISTER, BOB_REGISTER}, decisions
    assert all(d["tick"] == MEASUREMENT_TICK for d in decisions.values()), decisions
    state = json.loads((case_dir / "state.json").read_text(encoding="utf-8"))
    codes = {}
    for node in state["nodes"]:
        for record in node["disturbances"]:
            codes[record["type"]] = record["values"]["outcome"][0]
    # The classical outcome code at each wing is the recorded quantum outcome.
    assert codes == {
        "Detector A": OUTCOME_CODES[decisions[ALICE_REGISTER]["outcome"]],
        "Detector B": OUTCOME_CODES[decisions[BOB_REGISTER]["outcome"]],
    }, codes
    return {
        "name": name,
        "alice": decisions[ALICE_REGISTER],
        "bob": decisions[BOB_REGISTER],
        "classical_outcome_codes": codes,
        "random_draws": resolver["random_draws"],
        "model": resolver["model"],
    }


def exact_table(output, environment):
    """Joint distributions from recorded weights: Alice's marginal and Bob's conditional weights."""
    rows = {}
    correlations = {}
    alice_weights = set()
    bob_marginals = set()
    for a, b in SETTINGS:
        prefix = f"{environment}_{a}{b}"
        first = run_case(
            prefix + "_alice0", configuration(a, b, tickets=[0, 0], environment=environment), output
        )
        marginal = first["alice"]["weights"]
        assert first["alice"]["outcome"] == 0
        # The ticket equal to the first weight selects Alice's second outcome.
        second = run_case(
            prefix + "_alice1",
            configuration(a, b, tickets=[marginal[0], 0], environment=environment),
            output,
        )
        assert second["alice"]["weights"] == marginal and second["alice"]["outcome"] == 1
        alice_weights.add(tuple(marginal))
        joint = {}
        for i, case in enumerate((first, second)):
            conditional = case["bob"]["weights"]
            for j in (0, 1):
                joint[i, j] = Fraction(marginal[i], sum(marginal)) * Fraction(
                    conditional[j], sum(conditional)
                )
        assert sum(joint.values()) == 1
        bob_marginals.add(tuple(sum(joint[i, j] for i in (0, 1)) for j in (0, 1)))
        correlations[a + b] = sum((1 if i == j else -1) * p for (i, j), p in joint.items())
        rows[a + b] = {
            "alice_weights": marginal,
            "bob_weights_given_alice": [first["bob"]["weights"], second["bob"]["weights"]],
            "joint_probabilities": {f"{i}{j}": str(p) for (i, j), p in joint.items()},
            "correlation": str(correlations[a + b]),
            "cases": [first, second],
        }
    chsh = sum(CHSH_SIGNS[a, b] * correlations[a + b] for a, b in SETTINGS)
    # No signalling: Alice's weights do not depend on Bob's setting and Bob's
    # marginal, summed over Alice's outcomes, does not depend on Alice's setting.
    assert len(alice_weights) == 1 and len(bob_marginals) == 1, (alice_weights, bob_marginals)
    return {
        "environment": environment,
        "settings": rows,
        "correlations": {key: str(value) for key, value in correlations.items()},
        "chsh": str(chsh),
        "violates_local_bound": chsh > LOCAL_BOUND,
        "alice_weights_for_every_bob_setting": sorted(map(list, alice_weights)),
        "bob_marginal_for_every_alice_setting": [str(p) for p in next(iter(bob_marginals))],
    }


def sampled_trials(output, trials, environment="bell"):
    """Coincidence counts from seeded runs, one run per trial, as in a counting experiment."""
    rows = {}
    estimates = {}
    for index, (a, b) in enumerate(SETTINGS):
        counts = {"00": 0, "01": 0, "10": 0, "11": 0}
        outcomes = []
        for trial in range(trials):
            seed = 1 + index * trials + trial
            case = run_case(
                f"{environment}_{a}{b}_trial_{trial:03d}",
                configuration(a, b, seed=seed, environment=environment),
                output,
            )
            key = f"{case['alice']['outcome']}{case['bob']['outcome']}"
            counts[key] += 1
            outcomes.append(key)
        same = counts["00"] + counts["11"]
        estimates[a + b] = Fraction(same - (trials - same), trials)
        rows[a + b] = {"counts": counts, "correlation": str(estimates[a + b]), "outcomes": outcomes}
    chsh = sum(CHSH_SIGNS[a, b] * estimates[a + b] for a, b in SETTINGS)
    return {
        "environment": environment,
        "trials_per_setting": trials,
        "settings": rows,
        "correlations": {key: str(value) for key, value in estimates.items()},
        "chsh": str(chsh),
        "chsh_decimal": float(chsh),
    }


def run_experiment(output, trials=100):
    template = json.loads(TEMPLATE.read_text(encoding="utf-8"))
    predicted = analytic("bell")
    predicted_control = analytic("dephased")
    exact = exact_table(output, "bell")
    control = exact_table(output, "dephased")
    assert exact["correlations"] == predicted["correlations"], (exact, predicted)
    assert control["correlations"] == predicted_control["correlations"], (control, predicted_control)
    assert exact["chsh"] == "14/5" and control["chsh"] == "6/5"
    sampled = sampled_trials(output, trials)
    return {
        "status": "pass",
        "python": platform.python_version(),
        "source_sha256": source_fingerprint(),
        "model": template["event_program"]["model"],
        "template": TEMPLATE.name,
        "ticks": template["ticks"],
        "measurement_tick": MEASUREMENT_TICK,
        "wing_link_distance": wing_link_distance(template),
        "settings": {
            "alice": {k: {"matrix": m, "scale": s} for k, (m, s) in ALICE_SETTINGS.items()},
            "bob": {k: {"matrix": m, "scale": s} for k, (m, s) in BOB_SETTINGS.items()},
        },
        "analytic": predicted,
        "analytic_control": predicted_control,
        "exact": exact,
        "exact_control": control,
        "sampled": sampled,
        "local_bound": str(LOCAL_BOUND),
        "limits": [
            "Settings are 3-4-5 rational stand-ins; the Tsirelson value 2 sqrt(2) is not representable.",
            "Both wings decide at the same tick nine Links apart; the run is finite and ends before any Link signal could cross.",
            "The simulated RNG supplies tickets; this is an exact model calculation, not a laboratory Bell test.",
            "Detector arrival at a wing is the only trigger; there is no free-will or detection-efficiency loophole analysis.",
        ],
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--trials", type=int, default=100, help="seeded runs per setting pair")
    args = parser.parse_args()
    out = args.output.resolve()
    validate_output_path(out)
    if out.exists() and any(out.iterdir()):
        raise ValueError("use a new or empty output directory")
    out.mkdir(parents=True, exist_ok=True)
    summary = out / "summary.json"
    summary.touch()
    with ArtifactLease(out, [summary]):
        result = run_experiment(out, args.trials)
        summary.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(
        json.dumps(
            {
                "status": result["status"],
                "output": str(out),
                "exact_chsh": result["exact"]["chsh"],
                "control_chsh": result["exact_control"]["chsh"],
                "sampled_chsh": result["sampled"]["chsh"],
                "source_sha256": result["source_sha256"],
            }
        )
    )


if __name__ == "__main__":
    main()
