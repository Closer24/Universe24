"""Exact bounded two-bank retiming with a separate off-preparation control.

This optional fixed tensor uses the ordinary scalar Rule3. It matches a
candidate scalar probe's long-wave speed, not its finite-lattice dispersion.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path
import sys

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from universe24.core import Engine, State, Tensor
from universe24.core.lattice import lattice
from universe24.core.reciprocity import check_reciprocity

NAMES = ("p.X", "p.Y", "q.X", "q.Y")
PROFILES = ((3, -2, -1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
            (2, 0, 0, -1, -1, 0, 0, 0, 0, 0, 0, 0, 0, 0))


def build(Q, axis):
    D = 6 * Q
    zero = (0, 0, 0)
    plus = tuple(int(i == axis) for i in range(3))
    minus = tuple(-v for v in plus)
    terms = []
    for pol in ("p", "q"):
        for offset in (zero, minus):
            terms.append((f"{pol}.X", D // 2, ((f"{pol}.Y", offset, "b"),)))
        for offset in (zero, plus):
            terms.append((f"{pol}.Y", D // 2, ((f"{pol}.X", offset, "b"),)))
    return Tensor(NAMES, terms, Q=Q, strict_support=True)


def expected_counters(L, axis, tick):
    """Independent fine-ring oracle; never applies the compiled tensor."""
    lat = lattice(L)
    coordinate = np.array([lat.coords(n)[axis] for n in range(lat.N)])
    return np.array([np.array(profile, dtype=object)[(2 * coordinate + bank + tick) % (2 * L)]
                     for profile in PROFILES for bank in (0, 1)], dtype=object)


def seed_state(Q, axis, L=7):
    b = expected_counters(L, axis, 0)
    a = expected_counters(L, axis, -1)
    indices = np.arange(b.size, dtype=np.int64).astype(object).reshape(b.shape)
    # An explicit nonuniform phase preparation, independent of wave amplitude.
    r = (indices * 17 + 5) % (6 * Q)
    return State(L, a, b, r)


def delta(values, axis, lat):
    plus = tuple(int(i == axis) for i in range(3))
    minus = tuple(-v for v in plus)
    return values[..., lat.shift_index(plus)] - values[..., lat.shift_index(minus)]


def assert_TT(counters, axis, lat):
    i, j = (axis + 1) % 3, (axis + 2) % 3
    for bank in (0, 1):
        h = np.zeros((3, 3, lat.N), dtype=object)
        h[i, i] = counters[bank]
        h[j, j] = -counters[bank]
        h[i, j] = h[j, i] = counters[2 + bank]
        assert np.all(h == h.swapaxes(0, 1))
        assert np.all(sum(h[k, k] for k in range(3)) == 0)
        assert np.all(sum(delta(h[k], k, lat) for k in range(3)) == 0)


def run_case(Q, axis, steps=56):
    tensor = build(Q, axis)
    assert check_reciprocity(tensor).ok
    engine = Engine(tensor, Q)
    seed = seed_state(Q, axis)
    state = seed
    first_period = None
    peak = 0
    records = 0
    counter_hash = hashlib.sha256()
    event_hash = hashlib.sha256()
    for tick in range(1, steps + 1):
        previous = state
        state = engine.step(previous)
        assert np.array_equal(state.b, expected_counters(7, axis, tick))
        assert np.array_equal(state.a, expected_counters(7, axis, tick - 1))
        assert np.array_equal(state.r, seed.r)
        for retained in (state.a, state.b):
            assert_TT(retained, axis, state.lattice)
        official = engine.clicks(previous, state, tick).select("official")
        assert np.all(official.kind == 0)
        records += len(official)
        counter_hash.update(json.dumps([int(v) for v in state.b.flat]).encode())
        event_hash.update(json.dumps(official.rows()).encode())
        peak = max(peak, state.max_abs())
        if first_period is None and state.same_as(seed):
            first_period = tick
    assert first_period == 14
    assert peak == 3
    assert engine.rewind(state, steps).same_as(seed)
    return dict(Q=Q, D=6 * Q, L=7, axis=axis, steps=steps, gears=tensor.G,
                monomials=len(tensor.monomials), rank=tensor.rank,
                tensor_fingerprint=tensor.fingerprint, reciprocal=True,
                strict_single_edge_support=True, exact_fine_shift_every_update=True,
                exact_coarse_shift_every_two_updates=True, complete_state_period=first_period,
                peak_counter=peak, both_retained_bank_TT_constraints=True,
                remainders_constant=True, exact_rewind=True,
                official_records=records, all_official_events_C0=True,
                counter_history_sha256=counter_hash.hexdigest(),
                official_history_sha256=event_hash.hexdigest())


def unprepared_control():
    """Reversibility alone does not bound states off the prepared graph."""
    Q, L, steps = 4, 3, 16
    tensor = build(Q, 2)
    engine = Engine(tensor, Q)
    shape = (4, L ** 3)
    seed = State(L, np.ones(shape, dtype=object), np.zeros(shape, dtype=object),
                 np.full(shape, 7, dtype=object))
    state = seed
    for tick in range(1, steps + 1):
        state = engine.step(state)
        assert np.all(state.a == 1 - tick)
        assert np.all(state.b == -tick)
        assert np.array_equal(state.r, seed.r)
    assert engine.rewind(state, steps).same_as(seed)
    return dict(Q=Q, L=L, steps=steps, initial_a=1, initial_b=0, initial_r=7,
                exact_formula="a_t=1-t, b_t=-t in every gear and node",
                unbounded_by_formula=True, exact_rewind=True,
                meaning="The all-time bound requires a=R^-1 b; arbitrary seeds need not be bounded.")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, default=ROOT / "runs/geometry/retimed_tensor_wave.json")
    args = parser.parse_args()
    cases = [run_case(Q, axis) for Q in (4, 2 ** 72) for axis in range(3)]
    for axis in range(3):
        assert cases[axis]["counter_history_sha256"] == cases[axis + 3]["counter_history_sha256"]
        assert cases[axis]["official_history_sha256"] == cases[axis + 3]["official_history_sha256"]
    dispersion = []
    for k in (math.pi / 16, math.pi / 8, math.pi / 4, math.pi / 2):
        dispersion.append(dict(coarse_wave_number=k, retimed_frequency=k / 2,
                               candidate_scalar_frequency=2 * math.asin(0.5 * math.sin(k / 2))))
    result = dict(scope="Exact bounded prepared two-bank retiming; a candidate long-wave speed match only",
                  source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                  engine_sha256=hashlib.sha256((ROOT / "universe24/core/engine.py").read_bytes()).hexdigest(),
                  profiles=[list(profile) for profile in PROFILES],
                  seed="b_pX=f_p(2z), b_pY=f_p(2z+1), likewise q; a=R^-1 b; r=(17*flat_index+5) mod D",
                  retiming="R(X,Y)=(Y,SX), R^-1(X,Y)=(S^-1Y,X), u=(D/2)(R+R^-1)b",
                  exact_speed_in_coarse_sites_per_update="1/2",
                  cases=cases, common_divisor_counter_and_official_histories_equal=True,
                  off_preparation_control=unprepared_control(),
                  candidate_scalar_probe=dict(implemented_here=False, w="D/8 (requires Q divisible by 4)",
                      low_wave_number_speed="1/2", cosine_frequency_range=[-0.5, 1],
                      dispersion="cos(omega)=1-(1/2)*sum_i sin(k_i/2)^2",
                      axis_comparison=dispersion),
                  limitations=["One chosen axis per tensor; rotating that axis gives another tensor, not a proved isotropic three-dimensional dynamics.",
                      "The fine-ring interpretation interleaves two internal banks; it does not refine all three spatial coordinates or the scalar probe grid.",
                      "Matching the long-wave speed does not match the complete scalar dispersion or microscopic support cone.",
                      "No matter coupling, reciprocal gravitational backreaction or Einstein constraints are implemented in this experiment.",
                      "TT is the algebraic transformation/constraint type of the two planar polarization readouts, not a proof of measured curvature."])
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(dict(output=str(args.out), cases=len(cases), exact_period=14,
                         all_rewinds=True, peak_counter=3,
                         negative_control="unprepared uniform mode grows linearly")))


if __name__ == "__main__":
    main()
