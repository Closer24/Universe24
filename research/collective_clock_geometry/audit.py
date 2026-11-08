"""Fresh exact audit of the activity/balance bridge; no evolution-law changes.

The independent matrix gather oracle supplies all six donors and complete-state
forward/inverse comparisons. All preparations occur before the first update.
Run: python -m research.collective_clock_geometry.audit --output runs/activity-check
"""
from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from pathlib import Path
import random
import time

from research.component_families.oracle import input_at, routing, step
from research.reference.algebra import DIRECTIONS
from universe24 import Channel, Coupling, Cube, Engine, State
from universe24.core.rule3 import forward

ROOT = Path(__file__).resolve().parents[2]
BACKGROUND = (0, 0, 2)
BASELINE = "37fe77be8f489ba722ac687ff544b3956352e62f"
SEED = 2026110802
SOURCE_FILES = (
    "universe24/core/rule3.py", "universe24/core/engine.py",
    "universe24/core/coupling.py", "universe24/core/state.py",
    "universe24/core/group_2o.py", "research/reference/algebra.py",
    "research/component_families/oracle.py",
    "research/collective_clock_geometry/audit.py",
)


def phase_balance(triple):
    a, b, r = triple
    return 3 * (b - a) + r // 2 - 1


def reconstruct(b, p, epsilon):
    """Inverse coordinates, not a new evolution operation."""
    if epsilon not in (0, 1):
        raise ValueError("Remainder parity must be 0 or 1")
    theta = (p + 1) % 3
    return b - (p + 1) // 3, b, 2 * theta + epsilon


def cells_of(state):
    return {address: tuple(value) for address, value in state.cells.items()}


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def state_hash(cells, side):
    payload = {"side": side, "background": BACKGROUND,
               "cells": [[*address, *value] for address, value in sorted(cells.items())]}
    return hashlib.sha256(canonical(payload).encode()).hexdigest()


def addresses(side):
    return itertools.product(range(side), range(side), range(side), range(48))


def activity_four(cells, side, signs=(1, 1, 1)):
    """Return exact integer 4*S_xx,4*S_yy,4*S_zz at each spatial site.

    Off-diagonal entries vanish for this six-axis diagnostic. This function
    reads counter b only; it does not modify the state or compute a metric.
    """
    graph, _ = routing(tuple(signs))
    out = {}
    for x, y, z in itertools.product(range(side), repeat=3):
        diag = [0, 0, 0]
        for g in range(48):
            b = cells.get((x, y, z, g), BACKGROUND)[1]
            for d, delta in enumerate(DIRECTIONS):
                other = ((x + delta[0]) % side, (y + delta[1]) % side,
                         (z + delta[2]) % side, graph.ports[d][g])
                mismatch = b - graph.weights[d][g] * cells.get(other, BACKGROUND)[1]
                diag[d // 2] += mismatch * mismatch
        out[(x, y, z)] = tuple(diag)
    return out


def scalar_checks():
    values = tuple(range(-3, 4)) + (-10**40, 10**40)
    count = 0
    for a, b, u, r in itertools.product(values, values, values, range(6)):
        old = Channel(a, b, r)
        new = forward(old, u)
        p, pn = phase_balance(old), phase_balance(new)
        assert reconstruct(b, p, r % 2) == tuple(old)
        assert pn == p + u - 6 * b
        assert new.b == b + (pn + 1) // 3
        assert new.r % 2 == r % 2
        count += 1
    return {"cases": count, "integer_values": list(values), "remainders": list(range(6))}


def board_checks():
    rng = random.Random(SEED)
    records = []
    channel_checks = 0
    for side, signs in itertools.product((3, 4), itertools.product((-1, 1), repeat=3)):
        signs = tuple(signs)
        graph, _ = routing(signs)
        for d, g in itertools.product(range(6), range(48)):
            h = graph.ports[d][g]
            assert graph.ports[d ^ 1][h] == g
            assert graph.weights[d ^ 1][h] == graph.weights[d][g]
        old = {address: (rng.randrange(-2, 3), rng.randrange(-2, 3), rng.randrange(6))
               for address in addresses(side)}
        native = State(Cube(side), cells=old)
        old = cells_of(native)
        engine = Engine(Coupling(signs))
        native_next = engine.advance(native)
        new = cells_of(native_next)
        assert step(old, side, signs=signs) == new
        assert step(new, side, signs=signs, reverse=True) == old
        assert engine.rewind(native_next) == native
        s4 = activity_four(old, side, signs)
        dot = 0
        squared_changes = {pos: 0 for pos in s4}
        for address in addresses(side):
            before = old.get(address, BACKGROUND)
            after = new.get(address, BACKGROUND)
            b = before[1]
            u = input_at(old, address, side, signs)
            delta = phase_balance(after) - phase_balance(before)
            assert delta == u - 6 * b
            assert after[1] == b + (phase_balance(after) + 1) // 3
            assert after[2] % 2 == before[2] % 2
            dot += b * (6 * b - u)
            squared_changes[address[:3]] += delta * delta
            channel_checks += 1
        total4 = sum(sum(v) for v in s4.values())
        assert total4 == 2 * dot
        for pos, diag in s4.items():
            assert squared_changes[pos] <= 6 * sum(diag)
        # Central finite difference of the quadratic activity, derived separately
        # from the matrix donor sum, equals twice its real gradient.
        chosen = (0, 0, 0, 0)
        plus, minus = dict(old), dict(old)
        a, b, r = old.get(chosen, BACKGROUND)
        plus[chosen], minus[chosen] = (a, b + 1, r), (a, b - 1, r)
        total_plus = sum(sum(v) for v in activity_four(plus, side, signs).values())
        total_minus = sum(sum(v) for v in activity_four(minus, side, signs).values())
        assert total_plus - total_minus == 8 * (6 * b - input_at(old, chosen, side, signs))
        records.append({"side": side, "signs": signs, "seed": SEED,
                        "initial_sha256": state_hash(old, side),
                        "next_sha256": state_hash(new, side),
                        "four_times_activity": total4})
    return {"complete_boards": len(records), "channel_identity_checks": channel_checks,
            "records": records}


def counterexamples():
    side, center = 3, (1, 1, 1, 0)
    engine = Engine(Coupling((1, 1, 1)))
    plus = State(Cube(side), cells={center: (1, 1, 2)})
    minus = State(Cube(side), cells={center: (-1, -1, 2)})
    assert activity_four(cells_of(plus), side) == activity_four(cells_of(minus), side)
    assert all(phase_balance(plus.at(a)) == phase_balance(minus.at(a)) == 0
               for a in addresses(side))
    pn, mn = engine.advance(plus), engine.advance(minus)
    assert phase_balance(pn.at(center)) == -6
    assert phase_balance(mn.at(center)) == 6
    assert step(cells_of(plus), side) == cells_of(pn)
    assert step(cells_of(minus), side) == cells_of(mn)
    impulse = State(Cube(side), cells={center: (0, 1, 2)})
    later = engine.advance(impulse)
    before4 = sum(sum(v) for v in activity_four(cells_of(impulse), side).values())
    after4 = sum(sum(v) for v in activity_four(cells_of(later), side).values())
    assert (before4, after4) == (12, 0)
    assert engine.rewind(later) == impulse
    # This exact homogeneous solution changes forever with p=3 and S=0.
    drift = State(Cube(side), cells={address: (0, 1, 2) for address in addresses(side)})
    for t in range(5):
        assert all(tuple(drift.at(a)) == (t, t + 1, 2) for a in addresses(side))
        assert all(phase_balance(drift.at(a)) == 3 for a in addresses(side))
        assert not any(sum(v) for v in activity_four(cells_of(drift), side).values())
        if t < 4:
            drift = engine.advance(drift)
    return {"same_activity_and_initial_p": {
                "side": side, "background": BACKGROUND, "address": center,
                "positive_initial": [1, 1, 2], "negative_initial": [-1, -1, 2],
                "p_initial_everywhere": 0, "next_center_p": [-6, 6]},
            "activity_not_conserved": {"initial": [0, 1, 2], "V_before": 3, "V_after": 0},
            "p_not_a_clock_phase": {"uniform_initial": [0, 1, 2], "checked_states": 5,
                                     "exact_state_at_t": ["t", "t+1", 2], "p": 3, "S": 0}}


def finite_period(history):
    return next((p for p in range(1, len(history) // 2 + 1)
                 if all(history[t] == history[t - p] for t in range(p, len(history)))), None)


def clock_replay():
    """Independent full-state replay of the 24 current-main clock preparations.

    These are fresh records, not recovered historical local experiment files.
    """
    side, target, reference, horizon = 7, (2, 2, 2), (5, 5, 5), 40
    source_seed = (-1, -1, 0)
    probe_seeds = ((-1, -1, 0), (0, -1, 4))
    engine = Engine(Coupling((1, 1, 1)))
    records = []
    for direction, probe_seed, source_present in itertools.product(range(6), probe_seeds, (False, True)):
        delta = DIRECTIONS[direction]
        source = tuple((target[i] + delta[i]) % side for i in range(3))
        cells = {(*pos, g): probe_seed for pos in (target, reference) for g in range(48)}
        if source_present:
            cells.update({(*source, g): source_seed for g in range(48)})
        native = State(Cube(side), cells=cells)
        old = cells_of(native)
        initial = dict(old)
        near, far, returns, hashes = [], [], [], []
        for t in range(horizon + 1):
            assert cells_of(native) == old
            hashes.append(state_hash(old, side))
            near.append(tuple(old.get((*target, g), BACKGROUND) for g in range(48)))
            far.append(tuple(old.get((*reference, g), BACKGROUND) for g in range(48)))
            if old == initial:
                returns.append(t)
            if t < horizon:
                new = step(old, side)
                next_native = engine.advance(native)
                assert new == cells_of(next_native)
                assert step(new, side, reverse=True) == old
                assert engine.rewind(next_native) == native
                old, native = new, next_native
        assert finite_period(near) == (5 if source_present else 4)
        assert finite_period(far) == 4
        assert returns == ([0, 20, 40] if source_present else list(range(0, 41, 4)))
        backward = old
        for t in range(horizon - 1, -1, -1):
            backward = step(backward, side, reverse=True)
            assert state_hash(backward, side) == hashes[t]
        assert backward == initial
        records.append({"direction": direction, "source_position": source,
                        "source_present": source_present, "probe_seed": probe_seed,
                        "near_period": finite_period(near), "reference_period": finite_period(far),
                        "complete_board_returns": returns, "complete_state_sha256": hashes})
    return {"coupling": [1, 1, 1], "side": side, "target": target,
            "reference": reference, "source_seed": source_seed, "background": BACKGROUND,
            "all_48_channels_at_prepared_sites": True, "seed": None, "horizon": horizon,
            "cases": len(records), "stored_state_hashes": len(records) * (horizon + 1),
            "independent_forward_transitions": len(records) * horizon,
            "independent_one_step_inverse_transitions": len(records) * horizon,
            "independent_full_rewind_transitions": len(records) * horizon,
            "native_forward_and_inverse_comparisons": len(records) * horizon,
            "recurrence_rate_ratio": "4/5", "universal_clock_slowing_claimed": False,
            "records": records}


def source_hashes():
    return {name: hashlib.sha256((ROOT / name).read_bytes()).hexdigest() for name in SOURCE_FILES}


def run_audit(output):
    output = Path(output)
    output.mkdir(parents=True, exist_ok=False)
    pins = source_hashes()
    protocol = {"format": "universe24-collective-clock-geometry-v1", "baseline_commit": BASELINE,
                "provenance": "Fresh reconstruction and replay after prior scratch artifacts became unavailable.",
                "fixed_rule": "divmod(2*u+r,6); a'=b; b'=ell-a", "source_sha256": pins,
                "scalar_values": [*range(-3, 4), -10**40, 10**40], "remainders": list(range(6)),
                "dense_board_sides": [3, 4], "all_eight_sign_triples": True,
                "random_seed": SEED, "clock_cases": 24, "clock_horizon": 40,
                "acceptance": "Every declared exact equality, inverse, whole-state hash and recurrence must pass.",
                "scope": "Activity/balance identities and restricted recurrence-rate coincidence, not gravity."}
    (output / "protocol.json").write_text(json.dumps(protocol, indent=2) + "\n")
    start = time.process_time()
    result = {"status": "PASS", "baseline_commit": BASELINE,
              "scalar": scalar_checks(), "dense_boards": board_checks(),
              "counterexamples": counterexamples(), "clock_replay": clock_replay(),
              "source_sha256": pins, "gravity_derived": False,
              "clock_rate_from_activity_tensor_derived": False}
    assert source_hashes() == pins
    result["cpu_seconds_after_imports"] = time.process_time() - start
    (output / "results.json").write_text(json.dumps(result, indent=2) + "\n")
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", required=True, help="A new directory; existing evidence is never overwritten")
    args = parser.parse_args()
    result = run_audit(args.output)
    print(json.dumps({"status": result["status"], "scalar_cases": result["scalar"]["cases"],
                      "boards": result["dense_boards"]["complete_boards"],
                      "clock_cases": result["clock_replay"]["cases"],
                      "independent_clock_forward_transitions": result["clock_replay"]["independent_forward_transitions"],
                      "cpu_seconds_after_imports": result["cpu_seconds_after_imports"]}))
