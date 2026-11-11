"""Exact prepared linear TT sector of the existing optional Einstein tensor.

This is a board/audit invariant-sector check, not an official-click gravitational
wave detector or a nonlinear Einstein-constraint proof. No tensor is edited.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from universe24.core import Engine, compose
from universe24.layers.einstein import SIGNS, einstein_system
from universe24.layers.one import one_system
from universe24.observe.einstein import stored_to_h, stored_to_hbar
from universe24.observe.gravity import div_spatial


def run(steps: int = 256) -> dict:
    if steps < 1:
        raise ValueError("steps must be positive")
    system = einstein_system(one_system(), on=True)
    tensor = compose(*system.blocks)
    engine = Engine(tensor, system.Q)
    Q, D, L = system.Q, engine.D, 4
    active = [tensor.gear_index("metric.a1"), tensor.gear_index("metric.hxy")]
    active_set = set(active)
    inactive = [i for i in range(tensor.G) if i not in active_set]

    # Structural certificate: restricting all other a,b to zero leaves exactly
    # the seven free, self-reading stencil monomials for each active gear.
    survivors = [m for m in tensor.monomials
                 if all(f.gear in active_set for f in m.factors)]
    assert len(survivors) == 14
    assert {m.target for m in survivors} == active_set
    zero = (0, 0, 0)
    faces = {(1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0),
             (0, 0, 1), (0, 0, -1)}
    for g in active:
        rows = [m for m in survivors if m.target == g]
        assert all(len(m.factors) == 1 and m.factors[0].gear == g
                   and m.factors[0].field == "b" for m in rows)
        coefficients = {m.factors[0].offset: m.coeff for m in rows}
        assert coefficients == {zero: 6, **{f: Q - 1 for f in faces}}

    initial = engine.vacuum(L, [D // 2 - 1] * tensor.G)
    preparation = {
        "metric.a1": {"a": [2, -3, 5, 0], "b": [3, 0, -3, 1],
                      "r": [0, D // 7, D - 1, D // 2]},
        "metric.hxy": {"a": [-1, 4, 0, -2], "b": [0, 2, 0, -2],
                       "r": [D // 3, 1, 3 * D // 4, D - 2]},
    }
    for name, fields in preparation.items():
        g = tensor.gear_index(name)
        for field, values in fields.items():
            getattr(initial, field)[g] = np.tile(values, L * L)

    def metric(state, field):
        values = {name: getattr(state, field)[tensor.gear_index("metric." + name)]
                  .astype(object).reshape(L, L, L) for name in SIGNS}
        return stored_to_h(values), stored_to_hbar(values)

    def assert_constraints(state):
        for field in ("a", "b"):
            assert np.all(getattr(state, field)[inactive] == 0)
            h, hb = metric(state, field)
            assert np.all(-h["00"] + h["xx"] + h["yy"] + h["zz"] == 0)
            assert np.all(h["xx"] == -h["yy"])
            assert all(np.all(h[p] == 0) for p in ("00", "0x", "0y", "0z", "zz", "xz", "yz"))
            for nu in range(4):
                fields = {}
                for i in range(1, 4):
                    key = "".join(sorted("0xyz"[i] + "0xyz"[nu], key="0xyz".index))
                    fields[i, nu] = hb[key]
                assert np.all(div_spatial(fields, nu) == 0)
        assert np.array_equal(state.r[inactive], initial.r[inactive])
        for field in ("a", "b", "r"):
            for g in active:
                arr = getattr(state, field)[g].reshape(L, L, L)
                assert np.all(arr == arr[0, 0, :])

    state = initial
    official_count = audit_count = raw_count = 0
    kinds = {"C0": 0, "C1": 0, "C2": 0}
    maximum_abs_wave_residual = peak_counter = changed_steps = 0
    assert_constraints(state)
    for step in range(1, steps + 1):
        after = engine.step(state)
        assert_constraints(after)
        changed_steps += int(not after.same_as(state))
        for g in active:
            b = state.b[g].astype(object).reshape(L, L, L)
            lap = np.roll(b, -1, axis=2) + np.roll(b, 1, axis=2) - 2 * b
            residual = D * (after.b[g].astype(object).reshape(L, L, L)
                            - 2 * b + state.a[g].astype(object).reshape(L, L, L)) - 2 * (Q - 1) * lap
            ledger = (state.r[g].astype(object) - after.r[g].astype(object)).reshape(L, L, L)
            assert np.array_equal(residual, ledger)
            maximum_abs_wave_residual = max(maximum_abs_wave_residual, max(abs(int(v)) for v in residual.flat))
        log = engine.clicks(state, after, step)
        official_count += len(log.select("official"))
        audit_count += len(log.select("audit"))
        raw_count += len(engine.clicks(state, after, step, stream="raw"))
        for kind, count in zip(*np.unique(log.kind, return_counts=True)):
            kinds["C" + str(int(kind))] += int(count)
        peak_counter = max(peak_counter, max(abs(int(v)) for v in after.b[active].flat))
        state = after
    assert maximum_abs_wave_residual < D
    assert engine.rewind(state, steps).same_as(initial)
    assert official_count == 0 and audit_count > 0 and changed_steps > 0
    return {
        "scope": "Exact prepared planar linear transverse-traceless board sector; not nonlinear ADM constraints or an official detector response",
        "tensor_fingerprint": tensor.fingerprint,
        "dynamics_fingerprint": tensor.dynamics_fingerprint,
        "Q": Q, "D": D, "P": system.info["P"], "L": L, "steps": steps,
        "active_gears": [tensor.names[g] for g in active],
        "preparation": preparation,
        "other_preparation": "a=b=0; r=D/2-1 for every inactive gear; active values depend only on z",
        "structural_certificate": {"surviving_monomials": len(survivors),
                                   "only_two_independent_free_stencils": True,
                                   "inactive_sector_has_no_surviving_forcing": True},
        "exact_checks_every_step": {"trace_zero": True, "linear_harmonic_divergence_zero": True,
                                    "planarity_of_a_b_r": True, "inactive_vacuum_unchanged": True,
                                    "wave_equation_includes_exact_carry_ledger": True},
        "changed_updates": changed_steps, "peak_absolute_counter": peak_counter,
        "maximum_abs_wave_residual": maximum_abs_wave_residual,
        "wave_residual_bound": D - 1,
        "clicks": {"official_label_records": official_count,
                   "audit_label_records_with_official_arithmetic_criterion": audit_count,
                   "all_raw_arithmetic_records": raw_count, "audit_kinds": kinds},
        "exact_rewind": True,
        "limitations": ["The invariant sector is selected in the preparation, not attracted from generic data.",
                        "The metric gears are audit-labelled; no official gravitational-wave click detector is obtained.",
                        "The linear TT constraints are not the full nonlinear ADM constraints.",
                        "The wave equation has its exact bounded carry residual, not an assumed zero residual.",
                        "No all-time amplitude bound is inferred from this finite numerical run."]}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--steps", type=int, default=256)
    parser.add_argument("--out", type=Path, default=Path("runs/geometry/planar_tt_sector.json"))
    args = parser.parse_args()
    result = run(args.steps)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))
