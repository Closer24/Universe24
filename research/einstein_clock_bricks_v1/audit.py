"""Reproducible finite Universe24 gravity-preconditions audit.

It does NOT derive a GR metric, stress-energy tensor, equivalence principle, or
Einstein's equation. It only constructs initial states, runs the unmodified
reference Engine, and reads complete trajectories. Python standard library.
Run from the repository: python research/einstein_clock_bricks_v1/audit.py
"""
from __future__ import annotations

import hashlib
import itertools
import json
import random
import sys
from collections import deque
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO))
from universe24 import Channel, Coupling, Cube, Engine, State
from universe24.core.group_2o import DIRECTIONS, group

EXPECTED_CORE_BLOBS = {
    "universe24/core/__init__.py": "30a11a21f915417029d2aa28c829eca325211fc0",
    "universe24/core/coupling.py": "16d959466bd31bbcf292b6c0e1e3f4f78f748900",
    "universe24/core/engine.py": "2493378dd0b692491bca78c0250433189c96258d",
    "universe24/core/group_2o.py": "16c4ae73de6b8208696196bf68517de2bd8548c8",
    "universe24/core/rule3.py": "dd2a7cdd34200aeb73aba64d02f6cccbfb32afe5",
    "universe24/core/state.py": "3d706224eef1ec158f78623efa453bc39b0afe30",
}


def verify_pinned_source():
    for name, expected in EXPECTED_CORE_BLOBS.items():
        raw = (REPO / name).read_bytes()
        got = hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\0" + raw).hexdigest()
        assert got == expected, f"Source drift: {name}: {got}; audit pinned to c5a23743"


def q(v):
    return 6 * (v.b - v.a) + v.r - 2


def J(v):
    return Channel(-v.a, -v.b, 4 - v.r + 2 * (v.r % 2))


def center_map():
    G = group()
    C = [G.multiplication[G.central][g] for g in range(48)]
    assert G.central == 14
    assert all(C[C[g]] == g and C[g] != g for g in range(48))
    return C


def flip_center_and_J(s, C):
    return State(s.cube, s.background, {
        (*address[:3], C[address[3]]): J(v) for address, v in s.cells.items()
    })


def balanced_vacuum(L, C):
    rs = [None] * 48
    for g in range(48):
        if rs[g] is None:
            rs[g], rs[C[g]] = 0, 4
    return State(Cube(L), cells={
        (x, y, z, g): Channel(0, 0, rs[g])
        for x, y, z in itertools.product(range(L), repeat=3)
        for g in range(48)
    }), rs


def period(trace):
    return next((d for d in range(1, len(trace) // 2 + 1)
                 if all(trace[t] == trace[t - d] for t in range(d, len(trace)))), None)


def native_two_clock_classes():
    L, T, F, N = 7, (2, 2, 2), (5, 5, 5), 40
    E = Engine(Coupling((1, 1, 1)))
    source = (-1, -1, 0)
    probes = ((-1, -1, 0), (0, -1, 4))
    counts = 0
    for d, k, present in itertools.product(range(6), range(2), (False, True)):
        src = tuple((T[i] + DIRECTIONS[d][i]) % L for i in range(3))
        cells = {(*site, g): Channel(*probes[k]) for site in (T, F) for g in range(48)}
        if present:
            cells.update({(*src, g): Channel(*source) for g in range(48)})
        S = State(Cube(L), cells=cells)
        initial = S
        near, far, src_history, returns = [], [], [], []
        for t in range(N + 1):
            near.append(S.node(T))
            far.append(S.node(F))
            src_history.append(S.node(src))
            if S == initial:
                returns.append(t)
            if t < N:
                next_s = E.advance(S)
                assert E.rewind(next_s) == S
                S = next_s
                counts += 1
        assert period(near) == (5 if present else 4)
        assert period(far) == 4
        if present:
            assert period(src_history) == 5
            assert returns == [0, 20, 40]
        else:
            assert returns == list(range(0, N + 1, 4))
    return {"native_cases": 24, "all_48_channels": True, "directions": 6,
            "probe_seeds": [list(p) for p in probes], "source_seed": list(source),
            "baseline_period": 4, "sourced_period": 5,
            "reference_period": 4, "observed_period_ratio": "4/5",
            "full_state_step_and_inverse_checks": counts,
            "not_universal_for_all_clocks": True}


def check_local_continuity(old, new, c):
    L = old.cube.side
    def flux(x, axis):
        d = 2 * axis
        y = tuple((x[i] + DIRECTIONS[d][i]) % L for i in range(3))
        return sum(2 * (old.at((*x, g)).b - old.at((*y, c.ports[d][g])).b)
                   for g in range(48))
    for x in itertools.product(range(L), repeat=3):
        qq = sum(q(new.at((*x, g))) - q(old.at((*x, g))) for g in range(48))
        outward = sum(flux(x, i) for i in range(3))
        inward = sum(flux(tuple((x[j] - int(i == j)) % L for j in range(3)), i)
                     for i in range(3))
        assert qq + outward - inward == 0
    return L ** 3


def local_continuity_random():
    rng = random.Random(20261108)
    E = Engine(Coupling((1, 1, 1)))
    site_checks = 0
    for L in (3, 4):
        for trial in range(4):
            cells = {(x, y, z, g): Channel(rng.randint(-2, 2), rng.randint(-2, 2), rng.randrange(6))
                     for x, y, z in itertools.product(range(L), repeat=3) for g in range(48)}
            S = State(Cube(L), cells=cells)
            T = E.advance(S)
            assert E.rewind(T) == S
            site_checks += check_local_continuity(S, T, E.coupling)
    return {"exact_site_continuity_checks": site_checks, "signed_scope": "+++ only",
            "physical_energy_identified": False}


def symmetry_all_signs():
    G, C = group(), center_map()
    N = 0
    tests = 0
    for signs in itertools.product((1, -1), repeat=3):
        c = Coupling(signs)
        for d, g in itertools.product(range(6), range(48)):
            assert c.ports[d][C[g]] == C[c.ports[d][g]]
            assert c.weights[d][C[g]] == c.weights[d][g]
            tests += 1
        E = Engine(c)
        B, rs = balanced_vacuum(3, C)
        assert E.advance(B) == B
        assert flip_center_and_J(B, C) == B
        plus = dict(B.cells)
        plus.update({(1, 1, 1, g): Channel(0, 1, rs[g]) for g in range(48)})
        X = State(Cube(3), cells=plus)
        Y = flip_center_and_J(X, C)
        for step in range(7):
            assert flip_center_and_J(X, C) == Y
            if step < 6:
                Xn, Yn = E.advance(X), E.advance(Y)
                assert E.rewind(Xn) == X and E.rewind(Yn) == Y
                X, Y = Xn, Yn
                N += 2
    return {"sign_choices": 8, "center_index": G.central,
            "port_covariance_checks": tests, "complete_trajectory_symmetry_checks": N,
            "fixed_balanced_remainder_vacuum": True}


def propagation_test():
    L, T, C = 7, (3, 3, 3), center_map()
    E = Engine(Coupling((1, 1, 1)))
    results = {}
    for name in ("standard", "balanced"):
        if name == "standard":
            B, rs = State(Cube(L)), [2] * 48
        else:
            B, rs = balanced_vacuum(L, C)
        cells = dict(B.cells)
        cells.update({(*T, g): Channel(0, 1, rs[g]) for g in range(48)})
        X = State(Cube(L), cells=cells)
        Y = flip_center_and_J(X, C)
        traces = []
        for t in range(4):
            assert flip_center_and_J(X, C) == Y
            vals = {}
            for axis, sgn in itertools.product(range(3), (-1, 1)):
                nbr = tuple((T[i] + int(axis == i) * sgn) % L for i in range(3))
                vals[f"{axis}{sgn:+d}"] = sum(abs(X.at((*nbr, g)).b - B.at((*nbr, g)).b)
                                               for g in range(48))
            traces.append(vals)
            if t < 3:
                Xn, Yn = E.advance(X), E.advance(Y)
                assert E.rewind(Xn) == X and E.rewind(Yn) == Y
                X, Y = Xn, Yn
        results[name] = traces
    assert list(results["standard"][1].values()) == [0] * 6
    assert list(results["balanced"][1].values()) == [24] * 6
    assert len(set(results["balanced"][3].values())) > 1
    # Compute exact directional second moment for each 24-element central sheet.
    G = group()
    n0 = (1, 1, 2)
    B, rs = balanced_vacuum(3, C)
    for phase in (0, 2):
        raw = [[sum((rs[g] // 2 == phase) *
                    sum(G.rotations[g][i][k] * n0[k] for k in range(3)) *
                    sum(G.rotations[g][j][k] * n0[k] for k in range(3))
                    for g in range(48)) for j in range(3)] for i in range(3)]
        assert raw == [[48 if i == j else 0 for j in range(3)] for i in range(3)]
    return {"all48_positive_negative_full_state_partner": True,
            "plus_and_minus_tooth_tensors": "Xi+ = Xi- = I/2",
            "standard_vacuum_nearest_step1": results["standard"][1],
            "balanced_vacuum_nearest_step1": results["balanced"][1],
            "balanced_vacuum_nearest_step3": results["balanced"][3],
            "isotropic_beyond_first_step": False}


def signed_kernel_classification():
    classes = {}
    fixed = 0
    for L in (3, 4, 5, 6):
        balanced = []
        for signs in itertools.product((1, -1), repeat=3):
            c = Coupling(signs)
            root = (0, 0, 0, 0)
            gauge = {root: 1}
            queue = deque([root])
            contradictions = 0
            while queue:
                x, y, z, g = queue.popleft()
                for d, delta in enumerate(DIRECTIONS):
                    nbr = ((x + delta[0]) % L, (y + delta[1]) % L,
                           (z + delta[2]) % L, c.ports[d][g])
                    val = gauge[(x, y, z, g)] * c.weights[d][g]
                    if nbr not in gauge:
                        gauge[nbr] = val
                        queue.append(nbr)
                    elif gauge[nbr] != val:
                        contradictions += 1
            assert len(gauge) == 48 * L ** 3
            if contradictions == 0:
                balanced.append("".join("+" if x == 1 else "-" for x in signs))
                for scale in (1, -2):
                    S = State(Cube(L), cells={loc: Channel(scale * val, scale * val, 2)
                                             for loc, val in gauge.items()})
                    assert Engine(c).advance(S) == S
                    fixed += 1
        classes[str(L)] = balanced
    assert classes["3"] == ["+++", "+--"]
    assert classes["4"] == ["+++", "+--", "-++", "---"]
    assert classes["5"] == classes["3"]
    assert classes["6"] == classes["4"]
    return {"kernel_classes_finite": classes, "tested_L": [3, 4, 5, 6],
            "signed_nonzero_fixed_state_replays": fixed,
            "full_infinite_L_classification_claimed": False}


def periodic_mean_check():
    E, L = Engine(Coupling((1, 1, 1))), 7
    cases = []
    seeds = [[(1, 1, 1, (-1, -1, 0))],
             [(1, 1, 1, (-1, -1, 0)), (2, 1, 1, (-1, -1, 0))],
             [(1, 1, 1, (1, 1, 4))]]
    for case in seeds:
        cells = {(x, y, z, g): Channel(*seed) for x, y, z, seed in case for g in range(48)}
        S = State(Cube(L), cells=cells)
        initial = S
        trajectory = [S]
        for t in range(1, 33):
            Sn = E.advance(S)
            assert E.rewind(Sn) == S
            if Sn == initial:
                length = t
                break
            trajectory.append(Sn)
            S = Sn
        else:
            raise AssertionError("Expected a complete bounded periodic orbit")
        totals = {}
        for step_state in trajectory:
            for address, v in step_state.cells.items():
                totals[address] = totals.get(address, 0) + v.b
        assert all(v == 0 for v in totals.values())
        cases.append({"number_of_prepared_sites": len(case), "period": length,
                      "time_average_b_exactly_zero_all_addresses": True})
    assert [c["period"] for c in cases] == [4, 5, 4]
    return {"cases": cases, "proof": "p(t+1)-p(t)=-L_sigma b(t); sum a full return period"}


def main():
    verify_pinned_source()
    result = {
        "reference_core_commit": "c5a23743d96936190210dd510105ed470d4a0b23",
        "science_claim": "Exact restricted clock-rate coincidence and mathematical preconditions, NOT Einstein gravity",
        "two_clock_classes": native_two_clock_classes(),
        "local_current": local_continuity_random(),
        "central_and_J_symmetry": symmetry_all_signs(),
        "phase_balanced_response": propagation_test(),
        "signed_graph_kernel": signed_kernel_classification(),
        "periodic_mean": periodic_mean_check(),
        "gravity_derived": False,
        "physical_energy_stress_identified": False,
        "universal_equivalence_principle_verified": False,
    }
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
