"""Source-only mechanical smoke fixture; not an accepted physical universe."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from universe24.core import Engine, State, compose, reference_block
from universe24.system.bundle import create_bundle, save_bundle, canonical_bytes
from universe24.system.decoder import default_protocol
from universe24.system.runtime import run_bundle, verify_run


def fixture():
    tensor = compose(reference_block((1, -1, 1)))
    seed = State(3, [[n - 13 for n in range(27)]] * 48,
                 [[(n % 7) - 3 for n in range(27)]] * 48,
                 [[n % 6 for n in range(27)]] * 48)
    seed.b[0, 0] = -(1 << 30)
    return create_bundle(tensor, seed,
                         channels=[{"index": i, "name": g.name, "label": g.label,
                                    "owner": "mechanical-fixture", "purpose": "test state; no physical claim"}
                                   for i, g in enumerate(tensor.gears)],
                         protocol=default_protocol(),
                         model={"id": "mechanical-fixture", "version": "1",
                                "domain": "software contract tests only"})


def scalar_step(tensor, state):
    """Independent scalar oracle: no Engine.step or compiled input evaluator."""
    a = [[0] * state.N for _ in range(tensor.G)]
    b = [[0] * state.N for _ in range(tensor.G)]
    r = [[0] * state.N for _ in range(tensor.G)]
    L = state.L
    for node in range(state.N):
        xyz = (node // (L * L), (node // L) % L, node % L)
        values = [0] * tensor.G
        for term in tensor.monomials:
            value = term.coeff
            for factor in term.factors:
                x, y, z = [(xyz[k] + factor.offset[k]) % L for k in range(3)]
                value *= int(getattr(state, factor.field)[factor.gear, (x * L + y) * L + z])
            values[term.target] += value
        for gear, value in enumerate(values):
            quotient, remainder = divmod(2 * value + int(state.r[gear, node]), 6)
            a[gear][node] = int(state.b[gear, node])
            b[gear][node] = quotient - int(state.a[gear, node])
            r[gear][node] = remainder
    return State(L, a, b, r)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args(argv)
    bundle = fixture()
    save_bundle(bundle, args.out / "input")
    report = run_bundle(args.out / "input", args.out / "run", 6)
    current = expected = bundle.seed
    engine = Engine(bundle.tensor)
    for _ in range(6):
        current = engine.step(current)
        expected = scalar_step(bundle.tensor, expected)
        if not current.same_as(expected):
            raise AssertionError("independent scalar oracle mismatch")
    if report != verify_run(args.out / "run"):
        raise AssertionError("saved-run replay mismatch")
    evidence = {"role": "mechanical fixture only", "scalar_oracle": "passed",
                "bundle_id": bundle.bundle_id, "run_id": report["run_id"],
                "channels": bundle.tensor.G, "full_physics_acceptance": "not_tested"}
    (args.out / "smoke.json").write_bytes(canonical_bytes(evidence))
    print(json.dumps(evidence, indent=2))


if __name__ == "__main__":
    main()
