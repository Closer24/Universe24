"""Run real transactions and write a machine-readable conservation report."""

import argparse
import json
from pathlib import Path

from .algebra import ONE, ZERO, literal, rational
from .runtime import Complex, Lab, QuantumState, RandomStream

ROOT = Path(__file__).parent


def encode(quantity):
    return {
        "values": [
            str(x.numerator) if x.denominator == 1 else f"{x.numerator}/{x.denominator}"
            for x in quantity.components
        ],
        **quantity.json(),
    }


def ledger(lab):
    return {key: encode(value) for key, value in lab.totals().items()}


def massive(kind, mass=1, E=1, p=None, q=0):
    return kind, {"mass": mass, "E": E, "p": p or [0, 0, 0], "q": q}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=Path("artifacts/generic-vector-lab"))
    output = parser.parse_args().output
    output.mkdir(parents=True, exist_ok=True)
    definitions = json.loads((ROOT / "definitions.json").read_text(encoding="utf-8"))
    scenarios = [
        ("annihilate", [massive("electron", q=-1), massive("positron", q=1)], None),
        (
            "pair_creation",
            [("pulse", {"E": 1, "p": [1, 0, 0]}), ("pulse", {"E": 1, "p": [-1, 0, 0]})],
            None,
        ),
        ("capture", [massive("constituent"), massive("constituent")], None),
        (
            "absorb",
            [massive("ground", 2, 2), ("pulse", {"E": 3, "p": [3, 0, 0]})],
            None,
        ),
        ("emit", [massive("excited", 4, 5, [3, 0, 0])], None),
        (
            "elastic",
            [
                ("classical", {"mass": 1, "p": [1, 0, 0], "q": 0}),
                ("classical", {"mass": 1, "p": [0, 0, 0], "q": 0}),
            ],
            {"normal": literal([1, 1, 1])},
        ),
        (
            "mix_fields",
            [
                ("field_A", {"amplitude": [5, 0, 0]}),
                ("field_B", {"amplitude": [0, 0, 0]}),
            ],
            None,
        ),
    ]
    report = {"scope": definitions["description"], "scenarios": []}
    for name, inputs, parameters in scenarios:
        lab = Lab(definitions)
        ids = [lab.insert(0, lab.record(kind, fields)) for kind, fields in inputs]
        before = ledger(lab)
        products = lab.react(0, name, ids, parameters)
        after = ledger(lab)
        assert before == after
        report["scenarios"].append(
            {
                "name": name,
                "input_count": len(ids),
                "output_count": len(products),
                "before": before,
                "after": after,
                "exact_conservation": before == after,
                "products": [
                    {
                        "type": record.kind,
                        "quantities": {key: encode(q) for key, q in lab.context(record).items()},
                    }
                    for _, record in lab.nodes[0]
                ],
            }
        )
    lab = Lab(definitions)
    parent = lab.insert(0, lab.record(*massive("unstable", 2, 2)))
    stream = RandomStream(definitions["example_seed"])
    for tick in range(100):
        stream, products = lab.scheduled(0, "decay", [parent], stream)
        if products:
            report["scheduled_decay"] = {
                "zero_based_tick": tick,
                "products": len(products),
                "final_seed": stream.seed,
            }
            break
    else:
        raise AssertionError("Demo seed failed to decay within its bounded horizon")
    matrix = tuple(tuple(Complex(rational(x)) for x in row) for row in definitions["quantum_rotation"])
    quantum = QuantumState((Complex(ONE), Complex(ZERO))).evolve(matrix)
    lab = Lab(definitions)
    parent = lab.insert(0, lab.record(*massive("unstable", 2, 2)))
    before = ledger(lab)
    collapsed, products = quantum.measure_into(lab, 0, ["decay_x", "decay_y"], [parent], 24)
    assert ledger(lab) == before
    report["quantum_coupling"] = {
        "born_weights": quantum.weights(),
        "ticket": 24,
        "collapsed_weights": collapsed.weights(),
        "products": len(products),
        "exact_conservation": ledger(lab) == before,
    }
    (output / "report.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(f"{len(scenarios)} reaction scenarios: exact energy, momentum and charge balance passed.")
    print(f"Seeded decay fired at tick {tick}; quantum measurement created {len(products)} products.")
    print(f"Report: {output / 'report.json'}")


if __name__ == "__main__":
    main()
