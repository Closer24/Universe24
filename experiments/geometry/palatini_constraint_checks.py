"""Exact counterexamples to two naive Palatini-to-Rule3 constructions.

Run from any directory. Outputs go to ignored runs/ by default. This isolated
experiment changes no production layer, default tensor, or update primitive.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from universe24.core import Engine, GearType, State, Tensor
from universe24.core.reciprocity import check_reciprocity
from universe24.core.tensor import LocalityError

ZERO = (0, 0, 0)


def factor(name):
    return name, ZERO, "b"


def multiplier_counterexample():
    """A regular dynamical multiplier does not impose its algebraic constraint."""
    Q, D, kappa = 2, 12, 3
    # Phi = D/2*(q^2 + lambda^2) - kappa*lambda*(q^2 - 1).
    tensor = Tensor(
        ["q", "lambda"],
        [
            ("q", D, (factor("q"),)),
            ("q", -2 * kappa, (factor("lambda"), factor("q"))),
            ("lambda", D, (factor("lambda"),)),
            ("lambda", -kappa, (factor("q"), factor("q"))),
            ("lambda", kappa, ()),
        ],
        Q=Q,
        strict_support=True,
    )
    engine = Engine(tensor, Q)
    b = np.ones((2, 27), dtype=np.int64)
    seed = State(3, b.copy(), b.copy(), np.zeros_like(b))
    following = engine.step(seed)
    initial_constraint = int(seed.b[0, 0]) ** 2 - 1
    next_constraint = int(following.b[0, 0]) ** 2 - 1
    rewind = engine.inverse_step(following).same_as(seed)
    reciprocal = check_reciprocity(tensor).ok
    assert initial_constraint == 0 and next_constraint == -1
    assert rewind and reciprocal and not tensor.support_violations()
    return {
        "Q": Q,
        "D": D,
        "kappa": kappa,
        "rank": tensor.rank,
        "tensor_fingerprint": tensor.fingerprint,
        "seed_scope": "Every one of the 27 nodes has the stated initial triple.",
        "initial_a": [1, 1],
        "initial_b": [1, 1],
        "initial_r": [0, 0],
        "next_a": list(map(int, following.a[:, 0])),
        "next_b": list(map(int, following.b[:, 0])),
        "next_r": list(map(int, following.r[:, 0])),
        "initial_constraint": initial_constraint,
        "next_constraint": next_constraint,
        "exact_rewind": rewind,
        "reciprocity": reciprocal,
        "strict_support": True,
        "interpretation": (
            "Giving lambda regular Rule3 inertia turns lambda*(q^2-1) into a "
            "force, not exact enforcement of q^2=1. If used as a coframe "
            "diag(q,1,1,1), this initial nondegenerate coframe becomes degenerate."
        ),
    }


def physical_link_counterexample():
    """Low polynomial degree does not guarantee one-physical-edge support."""
    gears = [
        GearType("e"),
        GearType("omega_x", link=0),
        GearType("omega_y", link=1),
    ]
    term = ("e", 1, (factor("e"), factor("omega_x"), factor("omega_y")))
    tensor = Tensor(gears, [term], Q=1)
    try:
        Tensor(gears, [term], Q=1, strict_support=True)
    except LocalityError as exc:
        rejection = str(exc)
    else:
        raise AssertionError("cross-axis physical support was not rejected")
    return {
        "rank": tensor.rank,
        "violations": len(tensor.support_violations()),
        "rejection": rejection,
        "interpretation": (
            "A low-degree term using honest x-link and y-link connections "
            "touches three physical vertices and violates the one-edge "
            "monomial condition. This tests a term, not a complete gravity law."
        ),
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--out", type=Path,
        default=ROOT / "runs/geometry/palatini_constraint_checks.json",
    )
    args = parser.parse_args()
    result = {
        "multiplier_counterexample": multiplier_counterexample(),
        "strict_link_support": physical_link_counterexample(),
        "scope": (
            "Counterexamples to naive constructions, not no-go theorems for "
            "prepared invariant sectors, auxiliary encodings, or other "
            "discrete gravity actions."
        ),
    }
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
