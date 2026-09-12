"""Reproducible finite quantum and native classical-control experiments.

This is an experiment harness, not another evolution engine. All measured
predictions come from the active quantum owner or the canonical native runner.
Analytic targets remain independent of the update code. Use --visualize to
retain the existing recorded HTML players. No GIF or physical repair is used.
"""

import argparse
import html
import json
import platform
from dataclasses import asdict
from fractions import Fraction
from pathlib import Path

from event_universe.entities import compile_entities
from event_universe.quantum import (
    DeferredQuantum,
    EventNetworkConfig,
    LocalInstrument,
    LocalUnitary,
)
from event_universe.quantum.operations import dephasing, integer_matrix, permutation
from event_universe.retention import ArtifactLease, validate_output_path
from event_universe.runner import run_initialization, source_fingerprint

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
H = LocalUnitary(integer_matrix(((1, 1), (1, -1))))
CX = permutation((0, 3, 2, 1))


def new_pair():
    return DeferredQuantum().bind_event_network(EventNetworkConfig(((0, 0, 0), (1, 0, 0))))


def probability(weights):
    return [str(Fraction(w, sum(weights))) for w in weights]


def bell_experiment():
    correlations = []
    distributions = []
    for observable_a in (((1, 0), (0, -1)), ((0, 1), (1, 0))):
        for observable_b in (((3, 4), (4, -3)), ((3, -4), (-4, -3))):
            joint = {}
            for outcome in (0, 1):
                g = new_pair()
                g.step(((H, (0,)),))
                g.step(((CX, (0, 1)),))

                def instrument(rows, scale):
                    return LocalInstrument(
                        tuple(
                            integer_matrix(
                                tuple(
                                    tuple(scale * int(i == j) + sign * v for j, v in enumerate(row))
                                    for i, row in enumerate(rows)
                                )
                            )
                            for sign in (1, -1)
                        )
                    )

                d = g.prepare(1, 0, instrument(observable_a, 1))
                pa = Fraction(d.weights[outcome], sum(d.weights))
                g.commit(d, sum(d.weights[:outcome]))
                b = g.prepare(2, 1, instrument(observable_b, 5))
                for j, w in enumerate(b.weights):
                    joint[outcome, j] = pa * Fraction(w, sum(b.weights))
            assert sum(joint.values()) == 1
            assert all(sum(joint[a, b] for b in (0, 1)) == Fraction(1, 2) for a in (0, 1))
            assert all(sum(joint[a, b] for a in (0, 1)) == Fraction(1, 2) for b in (0, 1))
            correlations.append(sum((1 if a == b else -1) * w for (a, b), w in joint.items()))
            distributions.append({f"{a}{b}": str(w) for (a, b), w in joint.items()})
    s = correlations[0] + correlations[1] + correlations[2] - correlations[3]
    assert s == Fraction(14, 5)
    return {
        "correlations": list(map(str, correlations)),
        "chsh": str(s),
        "unconditional_marginals": "1/2 in all settings",
        "joint_probabilities": distributions,
        "interpretation": "Exact simulated statistics; not a laboratory Bell test.",
    }


def markov_experiment():
    g = DeferredQuantum().bind_event_network(EventNetworkConfig(((0, 0, 0),)))
    rotation = LocalUnitary(integer_matrix(((3, -4), (4, 3))))
    p = (Fraction(1), Fraction(0))
    steps = []
    for step in range(1, 6):
        g.step(((rotation, (0,)),))
        g.step(((dephasing(2), (0,)),))
        a, b = p
        p = ((9 * a + 16 * b) / 25, (16 * a + 9 * b) / 25)
        measured = probability(g.query(0).weights)
        assert measured == list(map(str, p)) and not g.records
        steps.append(
            {"cycle": step, "quantum_probabilities": measured, "classical_markov": list(map(str, p))}
        )
    return {
        "steps": steps,
        "records": 0,
        "world_ticks": g.tick,
        "events": [asdict(e) for e in g.events],
        "interpretation": "Classical probability dynamics after each basis record is discarded; not Newtonian emergence.",
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--visualize", action="store_true")
    args = parser.parse_args()
    out = args.output.resolve()
    validate_output_path(out)
    if out.exists() and any(out.iterdir()):
        raise ValueError("use a new or empty output directory")
    out.mkdir(parents=True, exist_ok=True)
    owned = [out / "summary.json", out / "entity-preparation.json"]
    if args.visualize:
        owned.append(out / "report.html")
    for path in owned:
        path.touch()
    with ArtifactLease(out, owned):
        cases = []
        for name, expected in [
            ("interference", ["1", "0"]),
            ("phase_reversal", ["0", "1"]),
            ("dephasing", ["1/2", "1/2"]),
            ("partial_dephasing", ["17/25", "8/25"]),
            ("native_classical", ["1", "0"]),
            ("native_cost_delay", ["1", "0"]),
        ]:
            run_initialization(HERE / (name + ".json"), out / name, visualize=args.visualize)
            meta = json.loads((out / name / "run.json").read_text())
            c = meta["computation"]
            q = c["resolver"]
            record = q["records"][0]
            probs = probability(record["decision"]["weights"])
            assert probs == expected
            assert meta["status"] == "completed" and meta["accounting_balanced_at_every_completed_tick"]
            assert c["model_operations_cost"] == c["event_ledger_cost"] > 0
            assert q["oracle_calls"] == 1 and q["oracle_direct_world_ticks"] == 0
            cases.append(
                {
                    "name": name,
                    "probabilities": probs,
                    "outcome": record["outcome"],
                    "random_draws": q["random_draws"],
                    "cost": c["model_operations_cost"],
                    "ticks": meta["completed_ticks"],
                    "contact_tick": record["decision"]["tick"],
                    "html": name + "/run.html" if args.visualize else None,
                }
            )
        catalog = json.loads((ROOT / "examples/known-entities/catalog.json").read_text())
        profile = compile_entities(
            catalog, ["electron", "positron", "electromagnetic_field"], representation="quantum"
        )
        init = out / "entity-preparation.json"
        init.write_text(json.dumps(profile, indent=2))
        run_initialization(init, out / "entity-preparation", visualize=args.visualize)
        result = {
            "status": "pass",
            "python": platform.python_version(),
            "source_sha256": source_fingerprint(),
            "native": cases,
            "bell": bell_experiment(),
            "classical_probabilities": markov_experiment(),
            "catalog": {
                "profiles": len(catalog["field_entities"]) + len(catalog["particle_entities"]),
                "joint_entity_preparation": ["electron", "positron", "electromagnetic_field"],
                "dimensions": profile["event_program"]["dimensions"],
            },
            "limits": [
                "Finite integer representation; no arbitrary real amplitudes or unlimited memory.",
                "No derived species Hamiltonians, quantum gravity, Maxwell law, full QFT or universal collapse rule.",
                "Classical paths and their positive operation costs are supplied by the configured native law.",
                "A discarded environment cannot later be coherently reversed without retaining it explicitly.",
            ],
        }
        (out / "summary.json").write_text(json.dumps(result, indent=2) + "\n")
        if args.visualize:
            rows = "".join(
                "<tr>"
                + "".join(
                    "<td>" + html.escape(str(row[k])) + "</td>"
                    for k in ("name", "probabilities", "outcome", "random_draws", "cost")
                )
                + "</tr>"
                for row in cases
            )
            players = "".join(
                "<details><summary>"
                + html.escape(row["name"])
                + '</summary><iframe title="'
                + html.escape(row["name"])
                + '" src="'
                + row["html"]
                + '"></iframe></details>'
                for row in cases
            )
            page = (
                """<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Universe24 quantum and classical checks</title><style>body{font:16px system-ui;margin:24px;max-width:1150px}table{border-collapse:collapse;width:100%}td,th{padding:10px;text-align:left;border-bottom:1px solid}section{overflow-x:auto}iframe{width:100%;height:660px;border:0}summary{padding:16px;cursor:pointer}pre{white-space:pre-wrap;overflow-wrap:anywhere}</style><h1>Quantum entities and classical outputs</h1><p>Native engine recordings and exact finite quantum checks. Supplied model laws, not a derivation of all physics.</p><section><table><tr><th>Experiment</th><th>Probabilities</th><th>Selected outcome</th><th>Draws</th><th>Path cost</th></tr>"""
                + rows
                + """</table></section><h2>CHSH = 14/5 = 2.8</h2><p>Exact joint correlations; local unconditional probabilities remain 1/2.</p>"""
                + players
                + "<details><summary>Full recorded evidence</summary><pre>"
                + html.escape(json.dumps(result, indent=2))
                + "</pre></details></html>"
            )
            (out / "report.html").write_text(page)
        print(
            json.dumps(
                {
                    "status": "pass",
                    "output": str(out),
                    "native_runs": len(cases),
                    "chsh": result["bell"]["chsh"],
                    "source_sha256": result["source_sha256"],
                }
            )
        )


if __name__ == "__main__":
    main()
