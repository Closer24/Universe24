"""Source-only controls separating host workload from retained physical dynamics.

Run from the repository root:
    python -m validation.einstein_node_audit.load_invariance

The extra host arithmetic never enters a tensor, state, seed or decoder. The
object backend subclass changes only exact array representation in this audit;
it does not modify the production Engine or establish a new physical model.
"""
from __future__ import annotations

import hashlib
import json
from fractions import Fraction
from pathlib import Path

import numpy as np

from universe24.core import Engine, State, Tensor
from universe24.core.engine import OBJ


ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / "runs/einstein-node/load_invariance.json"
STEPS = 128
WORK_PER_STEP = 500


class ExactObjectEngine(Engine):
    """Choose the existing Python-integer evaluator even for small inputs."""

    def _dtype(self, plan, a, b, extra):
        return OBJ


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def digest(value):
    data = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(data).hexdigest()


def scalar_step(state):
    """Independent scalar oracle for this exact two-face linear tensor."""
    old_a, old_b, old_r = state["a"][0], state["b"][0], state["r"][0]
    side = state["L"]
    new_b, new_r = [], []
    for node in range(side ** 3):
        x, yz = divmod(node, side * side)
        plus = ((x + 1) % side) * side * side + yz
        minus = ((x - 1) % side) * side * side + yz
        u = 3 * (old_b[plus] + old_b[minus])
        quotient, remainder = divmod(2 * u + old_r[node], 6)
        new_b.append(quotient - old_a[node])
        new_r.append(remainder)
    return {"L": side, "a": [old_b.copy()], "b": [new_b], "r": [new_r]}


def tensor():
    return Tensor(
        ["g"],
        [("g", 3, (("g", (1, 0, 0), "b"),)),
         ("g", 3, (("g", (-1, 0, 0), "b"),))],
        strict_support=True,
    )


def cycle_control(law):
    """A full-state period-three orbit refutes generic monotone equalization."""
    q = [[1 if node // 9 == 0 else 0 for node in range(27)]]
    seed = State(3, q, q, [[node % 6 for node in range(27)]])
    engine = Engine(law)
    state = seed.copy()
    trace = [state.to_dict()]
    variances = []
    for step in range(4):
        values = [int(v) for v in state.b.flat]
        mean = Fraction(sum(values), len(values))
        variance = sum((Fraction(v) - mean) ** 2 for v in values) / len(values)
        variances.append(str(variance))
        if step < 3:
            state = engine.step(state)
            trace.append(state.to_dict())
    require(state.same_as(seed), "period-three complete-state return failed")
    require(variances == ["2/9", "8/9", "2/9", "2/9"], "cycle variance changed")
    require(engine.rewind(state, 3).same_as(seed), "cycle rewind failed")
    return {
        "status": "passed",
        "full_state_period": 3,
        "spatial_b_variance_by_step": variances,
        "full_state_trace": trace,
        "conclusion": "Local reversible Rule3 does not force monotone amplitude equalization.",
        "scope": "This variance is an illustrative load proxy, not calibrated energy or complexity.",
    }


def audit():
    law = tensor()
    seed = State(
        3,
        [[(n * 7) % 13 - 6 for n in range(27)]],
        [[(n * 11) % 17 - 8 for n in range(27)]],
        [[n % 6 for n in range(27)]],
    )
    engines = [Engine(law), ExactObjectEngine(law), Engine(law)]
    modes = ["default_int64", "forced_exact_python_object", "extra_discarded_host_work"]
    states = [seed.copy() for _ in engines]
    scalar = seed.to_dict()
    full_trace = [scalar]
    state_hashes = [[digest(scalar)] for _ in engines]
    click_hashes = [[] for _ in engines]
    complete_clicks = []
    comparisons = oracle_comparisons = click_comparisons = extra_work = 0
    for step in range(1, STEPS + 1):
        before = [state.copy() for state in states]
        for mode in range(len(modes)):
            if mode == 2:
                for k in range(WORK_PER_STEP):
                    # Intentionally discarded host work, outside all physics.
                    _discarded = (1234567890123456789012345678901234567890 + k) ** 2
                    extra_work += 1
            states[mode] = engines[mode].step(states[mode])
        scalar = scalar_step(scalar)
        require(states[0].to_dict() == scalar, f"scalar oracle differs at {step}")
        oracle_comparisons += 81
        full_trace.append(scalar)
        rows = [list(engine.clicks(old, new, step).rows())
                for engine, old, new in zip(engines, before, states)]
        complete_clicks.append(rows[0])
        for mode in (1, 2):
            require(states[0].same_as(states[mode]), f"retained state differs at {step}/{mode}")
            require(rows[0] == rows[mode], f"clicks differ at {step}/{mode}")
            comparisons += 81
            click_comparisons += 1
        for mode in range(len(modes)):
            state_hashes[mode].append(digest(states[mode].to_dict()))
            click_hashes[mode].append(digest(rows[mode]))
    require(engines[0].stats["int64_steps"] == STEPS, "default int64 path unused")
    require(engines[1].stats["pyint_steps"] == STEPS, "Python-object path unused")
    require(states[1].b.dtype == np.dtype(object), "object output representation absent")
    for mode, (engine, state) in enumerate(zip(engines, states)):
        require(engine.rewind(state, STEPS).same_as(seed), f"rewind failed for mode {mode}")
    source_paths = [
        "universe24/core/engine.py", "universe24/core/tensor.py", "universe24/core/lattice.py",
        "validation/einstein_node_audit/load_invariance.py",
    ]
    report = {
        "schema": "universe24-einstein-node-load-invariance-v1",
        "inspected_main": "4c494c1188f70eb8a677bf59765cc6e8571c6b88",
        "status": "passed",
        "scope": "Host workload/backend invariance and nonmonotone-load countercontrol only.",
        "not_established": ["intrinsic workload theory", "physical clock calibration", "energy identification",
                            "Einstein dynamics", "general covariance", "emergent Lorentz invariance"],
        "steps": STEPS,
        "channels": law.G,
        "nodes": seed.N,
        "tensor": law.to_dict(),
        "seed": seed.to_dict(),
        "tensor_fingerprint": law.fingerprint,
        "modes": modes,
        "complete_retained_integer_backend_comparisons": comparisons,
        "independent_scalar_integer_comparisons": oracle_comparisons,
        "complete_click_transition_comparisons": click_comparisons,
        "extra_host_multiplications_in_third_mode_only": extra_work,
        "exact_rewinds": len(modes),
        "engine_stats": [engine.stats for engine in engines],
        "final_dtypes": [str(state.b.dtype) for state in states],
        "maximum_retained_bits": max(abs(value).bit_length() for snap in full_trace
                                     for field in ("a", "b", "r") for row in snap[field] for value in row),
        "full_baseline_trace": full_trace,
        "full_baseline_click_rows_by_transition": complete_clicks,
        "state_hashes_by_mode": state_hashes,
        "click_hashes_by_mode": click_hashes,
        "nonmonotone_load_countercontrol": cycle_control(law),
        "source_sha256": {path: hashlib.sha256((ROOT / path).read_bytes()).hexdigest()
                          for path in source_paths},
    }
    return report


def main():
    report = audit()
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    # Keep the complete trace while avoiding tens of thousands of padding lines.
    OUTPUT.write_text(json.dumps(report, sort_keys=True, separators=(",", ":")) + "\n")
    keys = ("status", "steps", "channels", "nodes", "complete_retained_integer_backend_comparisons",
            "independent_scalar_integer_comparisons", "complete_click_transition_comparisons",
            "extra_host_multiplications_in_third_mode_only", "exact_rewinds", "maximum_retained_bits")
    print(json.dumps({key: report[key] for key in keys}, sort_keys=True))


if __name__ == "__main__":
    main()
