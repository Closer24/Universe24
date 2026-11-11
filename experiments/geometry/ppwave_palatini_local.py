"""Local-chart pp-wave sector embedded in unchanged integer Rule3.

This embeds a chosen exact continuum vacuum family, not a discrete Palatini
action or general gravitational dynamics. Pointwise centered Cartan residuals
vanish in the transverse interior; periodic seams and operational-clock
controls are explicit failures. All construction/evolution/audits use integers.
"""
from __future__ import annotations

import argparse
import hashlib
from itertools import permutations
import json
from pathlib import Path
import sys

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from universe24.core import Engine, State, Tensor
from universe24.core.lattice import lattice
from universe24.core.reciprocity import check_reciprocity

ZERO, PLUS_Z, MINUS_Z = (0, 0, 0), (0, 0, 1), (0, 0, -1)
ETA = (-1, 1, 1, 1)
NULL = (1, 0, 0, -1)
PAIRS = tuple((a, b) for a in range(4) for b in range(a+1, 4))
COMPONENTS = tuple(f"E{a}{mu}" for a in range(4) for mu in range(4)) + tuple(f"W{a}{b}" for a, b in PAIRS)
TRIPLES = ((0, 1, 2), (0, 1, 3), (0, 2, 3), (1, 2, 3))


def peak(array):
    return max((abs(int(x)) for x in np.asarray(array).flat), default=0)


def parity(values):
    return (-1)**sum(values[i] > values[j] for i in range(len(values)) for j in range(i+1, len(values)))


def digest(state):
    return hashlib.sha256(json.dumps(state.to_dict(), separators=(",", ":")).encode()).hexdigest()


def build():
    """44 geometric gears, two signal banks and two uncoupled clock controls."""
    names = [f"{bank}.{component}" for bank in ("X", "Y") for component in COMPONENTS]
    names += ["signal.X", "signal.Y", "clock.period4", "clock.period6"]
    terms = []
    def f(name, offset=ZERO):
        return (name, offset, "b")
    for left, right in [(f"X.{c}", f"Y.{c}") for c in COMPONENTS] + [("signal.X", "signal.Y")]:
        # R(X,Y)=(Y,S_minus X), R^-1(X,Y)=(S_plus Y,X).
        terms += [(left, 3, (f(right),)), (left, 3, (f(right, PLUS_Z),)),
                  (right, 3, (f(left),)), (right, 3, (f(left, MINUS_Z),))]
    terms.append(("clock.period6", 3, (f("clock.period6"),)))
    return Tensor(names, terms, strict_support=True)


def prepare(tensor, L=7, P=256, mode="vacuum", wrong_connection=False):
    """Complete integer seed. P is fixed coframe calibration, with the fixed engine divisor six."""
    if type(L) is not int or L < 5 or L % 2 != 1:
        raise ValueError("This centered local chart uses odd L>=5")
    if type(P) is not int or P < 1 or mode not in ("vacuum", "flat", "nonharmonic"):
        raise ValueError("Positive integer P and a declared preparation required")
    lat = lattice(L)
    xyz = lat.all_coords()
    x, y, z = xyz[:, 0]-L//2, xyz[:, 1]-L//2, xyz[:, 2]
    A = np.array([i % 5-2 for i in range(L)], dtype=object)
    B = np.array([(2*i+1) % 3-1 for i in range(L)], dtype=object)
    if mode == "flat":
        A[:] = B[:] = 0
    az, bz = A[z], B[z]
    cz = az if mode == "nonharmonic" else -az
    F = az*x*x + 2*bz*x*y + cz*y*y
    Fx, Fy = 2*az*x+2*bz*y, 2*bz*x+2*cz*y
    if 2*peak(F) >= P:
        raise ValueError("Choose P>2 max|F| for the declared timelike coordinate clocks")
    fields = {}
    for a in range(4):
        for mu in range(4):
            fields[f"E{a}{mu}"] = P*int(a == mu) + ETA[a]*NULL[a]*NULL[mu]*F
    for a, b in PAIRS:
        value = Fx if (a, b) in ((0, 1), (1, 3)) else Fy if (a, b) in ((0, 2), (2, 3)) else np.zeros(lat.N, dtype=object)
        fields[f"W{a}{b}"] = np.zeros(lat.N, dtype=object) if wrong_connection else value
    # Fill object arrays before State chooses int64 versus arbitrary precision.
    # Constructing a zero State first would narrow its storage before big seeds.
    a_values = np.zeros((tensor.G, lat.N), dtype=object)
    b_values = a_values.copy()
    r_values = a_values.copy()
    gi = tensor.gear_index
    for component, values in fields.items():
        X, Y = gi(f"X.{component}"), gi(f"Y.{component}")
        b_values[X] = b_values[Y] = values
        a_values[X] = b_values[Y, lat.shift_index(PLUS_Z)]
        a_values[Y] = b_values[X]
    pulse = np.zeros(lat.N, dtype=object)
    origin = lat.index(L//2+1, L//2, 0)
    pulse[origin] = 1
    X, Y = gi("signal.X"), gi("signal.Y")
    b_values[X] = b_values[Y] = pulse
    a_values[X] = pulse[lat.shift_index(PLUS_Z)]
    a_values[Y] = pulse
    for name in ("clock.period4", "clock.period6"):
        b_values[gi(name)] = 1
    state = State(L, a_values, b_values, r_values)
    return state, dict(L=L, P=P, profile_A=list(map(int, A)), profile_B=list(map(int, B)),
                      mode=mode, wrong_connection=wrong_connection, signal_origin=list(lat.coords(origin)),
                      all_initial_remainders=0, coordinate_rule="x=index_x-L//2,y=index_y-L//2,z=index_z")


def unpack(state, bank="X"):
    """Read stored E and the six coefficients of W_ab=W_ab_scalar*(dt-dz)."""
    offset = 0 if bank == "X" else 22
    E = state.b[offset:offset+16].astype(object).T.reshape(state.N, 4, 4)
    W = np.zeros((state.N, 4, 4, 4), dtype=object)
    for i, (a, b) in enumerate(PAIRS):
        value = state.b[offset+16+i].astype(object)
        for mu in (0, 3):
            W[:, a, b, mu] = ETA[a]*value*NULL[mu]
            W[:, b, a, mu] = -ETA[b]*value*NULL[mu]
    return E, W


def cartan(previous, current, following, P):
    """Integer numerators with centered differences and pointwise wedge.

    T2=2P*physical_torsion_of_E; R2=2P^2*physical_connection_curvature.
    These are declared diagnostics, not an inferred discrete action.
    """
    E, W = unpack(current)
    Ep, Wp = unpack(previous)
    En, Wn = unpack(following)
    dE, dW = [En-Ep], [Wn-Wp]
    for axis in range(3):
        direction = tuple(int(i == axis) for i in range(3))
        plus = current.lattice.shift_index(direction)
        minus = current.lattice.shift_index(tuple(-v for v in direction))
        dE.append(E[plus]-E[minus])
        dW.append(W[plus]-W[minus])
    T2 = np.zeros((current.N, 4, 4, 4), dtype=object)
    R2 = np.zeros((current.N, 4, 4, 4, 4), dtype=object)
    for mu in range(4):
        for nu in range(4):
            T2[:, :, mu, nu] = P*(dE[mu][:, :, nu]-dE[nu][:, :, mu]) + 2*(
                (W[:, :, :, mu]@E[:, :, nu, None])[:, :, 0] -
                (W[:, :, :, nu]@E[:, :, mu, None])[:, :, 0])
            R2[:, :, :, mu, nu] = P*(dW[mu][:, :, :, nu]-dW[nu][:, :, :, mu]) + 2*(
                W[:, :, :, mu]@W[:, :, :, nu]-W[:, :, :, nu]@W[:, :, :, mu])
    palatini = np.zeros((current.N, 4, 4), dtype=object)
    for a in range(4):
        for b, c, d in permutations([i for i in range(4) if i != a]):
            coefficient = parity((a, b, c, d))*ETA[d]
            for ti, (i, j, k) in enumerate(TRIPLES):
                palatini[:, a, ti] += coefficient*(E[:, b, i]*R2[:, c, d, j, k]
                    - E[:, b, j]*R2[:, c, d, i, k] + E[:, b, k]*R2[:, c, d, i, j])
    return E, T2, R2, palatini


def exact_inverse_metric_and_ricci(E, R2, P):
    """Polynomial inverse certificate and Ricci numerator, no divisions."""
    identity = np.eye(4, dtype=object)
    J = 2*P*identity-E
    assert np.array_equal(E@J, np.broadcast_to(P*P*identity, E.shape))
    assert np.array_equal(J@E, np.broadcast_to(P*P*identity, E.shape))
    eta = np.diag(np.array(ETA, dtype=object))
    G = E.transpose(0, 2, 1)@eta@E
    # Ricci numerator has constant denominator 2P^4.
    ricci = np.zeros_like(E)
    for rho in range(4):
        for nu in range(4):
            converted = J@R2[:, :, :, rho, nu]@E
            ricci[:, :, nu] += converted[:, rho, :]
    F = E[:, 0, 3]
    G_inverse_numerator = P*eta-2*F[:, None, None]*np.outer(np.array(ETA)*NULL, np.array(ETA)*NULL)
    trace_numerator = np.sum(G_inverse_numerator*ricci, axis=(1, 2))
    einstein = 2*P**3*ricci-G*trace_numerator[:, None, None]
    # Normal proportional to (P+2F,0,0,2F), spacelike t-slices if P+2F>0.
    n0, n3 = P+2*F, 2*F
    hamiltonian = n0*n0*einstein[:, 0, 0]+n0*n3*(einstein[:, 0, 3]+einstein[:, 3, 0])+n3*n3*einstein[:, 3, 3]
    momentum = n0[:, None]*einstein[:, 0, 1:]+n3[:, None]*einstein[:, 3, 1:]
    k = np.array([1, 0, 0, 1], dtype=object)
    assert np.all(np.sum((G@k)*k, axis=1) == 0)
    return G, ricci, hamiltonian, momentum


def execute(tensor, seed, steps):
    engine = Engine(tensor)
    history, logs, trace = [seed], [], hashlib.sha256()
    for tick in range(1, steps+1):
        before = history[-1]
        after = engine.step(before)
        # Independent first-order map on the prepared transported-bank graph.
        # It is checked after Engine.step and never supplies the next state.
        expected = np.empty_like(after.b, dtype=object)
        expected[:22] = before.b[22:44]
        expected[22:44] = before.b[:22, before.lattice.shift_index(MINUS_Z)]
        expected[44] = before.b[45]
        expected[45] = before.b[44, before.lattice.shift_index(MINUS_Z)]
        expected[46] = -before.a[46]
        expected[47] = before.b[47]-before.a[47]
        on_graph = (np.array_equal(before.a[:22], before.b[22:44, before.lattice.shift_index(PLUS_Z)])
                    and np.array_equal(before.a[22:44], before.b[:22])
                    and np.array_equal(before.a[44], before.b[45, before.lattice.shift_index(PLUS_Z)])
                    and np.array_equal(before.a[45], before.b[44]))
        if on_graph:
            assert np.array_equal(after.b, expected)
        ell = after.b.astype(object)+before.a.astype(object)
        assert np.array_equal(2*engine.inputs(before).astype(object)+before.r, 6*ell+after.r)
        assert np.array_equal(after.r, seed.r)
        assert engine.inverse_step(after).same_as(before)
        log = engine.clicks(before, after, tick).select("official")
        logs.append(log)
        history.append(after)
        trace.update(bytes.fromhex(digest(after)))
    assert engine.rewind(history[-1], steps).same_as(seed)
    return history, logs, dict(seed_sha256=digest(seed), final_sha256=digest(history[-1]),
                              trace_sha256=trace.hexdigest(), steps=steps, exact_rewind=True,
                              trace_convention="SHA256 of concatenated 32-byte state digests after each update")


def shifted_wedge_counterexample():
    """A different, shifted differential product must not inherit our zeros."""
    profile = (1, 2, 3, 4, 5)
    t, z, x = 0, 2, 1
    connection_x = 2*profile[(z-t) % 5]*x
    shifted_z = 2*profile[(z+1-t) % 5]*x
    shifted_t = 2*profile[(z-t-1) % 5]*x
    coefficient = connection_x*(shifted_z-shifted_t)
    assert coefficient == 24
    return dict(profile_A=list(profile), event=dict(t=t,z=z,x=x,y=0),
                connection_x=connection_x, shifted_z=shifted_z, shifted_t=shifted_t,
                shifted_null_connection_wedge_square_coefficient=coefficient,
                interpretation="For dx_mu*f=(S_mu f)dx_mu, the shifted wedge yields a nonzero null-basis omega^-_+ square term. This is a separate calculus control, not an Engine result.")


def run(L=7, P=256):
    tensor = build()
    reciprocal = check_reciprocity(tensor)
    assert reciprocal.ok and not reciprocal.designated
    assert tensor.G == 48 and not tensor.support_violations() and tensor.b_only
    seed, preparation = prepare(tensor, L, P)
    steps = 12*L
    history, logs, provenance = execute(tensor, seed, steps)
    lat, gi = seed.lattice, tensor.gear_index
    interior = np.array([0 < x < L-1 and 0 < y < L-1 for x, y, z in lat.all_coords()])
    geometry = slice(0, 44)
    for n in range(steps//2+1):
        translated = seed.b[geometry][:, lat.shift_index((0, 0, -n))]
        assert np.array_equal(history[2*n].b[geometry], translated)
        assert np.array_equal(history[2*n].a[geometry], seed.a[geometry][:, lat.shift_index((0, 0, -n))])
        expected_node = lat.index(L//2+1, L//2, n)
        assert np.flatnonzero(history[2*n].b[gi("signal.X")]).tolist() == [expected_node]
    assert history[2*L].b[:46].tolist() == seed.b[:46].tolist()
    assert history[steps].same_as(seed)
    # A full longitudinal cycle suffices; subsequent cycles repeat exactly.
    samples = []
    max_curvature, seam_torsion, seam_einstein = 0, 0, 0
    clock_min, clock_max, minimum_slice = None, None, None
    for n in range(1, L+1):
        E, T2, R2, palatini = cartan(history[2*n-2], history[2*n], history[2*n+2], P)
        G, ricci, hamiltonian, momentum = exact_inverse_metric_and_ricci(E, R2, P)
        assert peak(T2[interior]) == peak(palatini[interior]) == peak(ricci[interior]) == 0
        assert peak(hamiltonian[interior]) == peak(momentum[interior]) == 0
        max_curvature = max(max_curvature, peak(R2[interior]))
        seam_torsion += int(np.count_nonzero(np.any(T2[~interior] != 0, axis=(1, 2, 3))))
        seam_einstein += int(np.count_nonzero(np.any(palatini[~interior] != 0, axis=(1, 2))))
        lo, hi = min(map(int, -G[:, 0, 0])), max(map(int, -G[:, 0, 0]))
        sl = min(map(int, P+2*E[:, 0, 3]))
        clock_min = lo if clock_min is None else min(clock_min, lo)
        clock_max = hi if clock_max is None else max(clock_max, hi)
        minimum_slice = sl if minimum_slice is None else min(minimum_slice, sl)
        samples.append(dict(macrostep=n, bulk_torsion=0, bulk_palatini=0, bulk_ricci=0,
                            bulk_ADM_normal_and_momentum_projections=0, peak_bulk_R2=peak(R2[interior])))
    assert max_curvature and seam_torsion and seam_einstein and clock_min > 0 and minimum_slice > 0
    # Same tensor, different initial geometry. Uncoupled clock records must fail
    # the desired metric response; do not disguise that absence as universality.
    flat, _ = prepare(tensor, L, P, "flat")
    flat_history, flat_logs, flat_provenance = execute(tensor, flat, steps)
    clock_ids = [gi("clock.period4"), gi("clock.period6")]
    def records(selected_logs, ids):
        return [[(int(g), int(n), int(q)) for g, n, q in zip(log.gear, log.node, log.quotient) if int(g) in ids] for log in selected_logs]
    assert records(logs, clock_ids) == records(flat_logs, clock_ids)
    signal_ids = [gi("signal.X"), gi("signal.Y")]
    assert records(logs, signal_ids) == records(flat_logs, signal_ids)
    bad_results = {}
    for label, mode, wrong in (("nonharmonic", "nonharmonic", False), ("wrong_connection", "vacuum", True)):
        bad, _ = prepare(tensor, L, P, mode, wrong)
        bad_history, _, bad_provenance = execute(tensor, bad, 4)
        _, T2, R2, palatini = cartan(bad_history[0], bad_history[2], bad_history[4], P)
        if wrong:
            assert peak(T2[interior]) > 0
        else:
            assert peak(T2[interior]) == 0 and peak(palatini[interior]) > 0
        bad_results[label] = dict(bulk_T2_peak=peak(T2[interior]), bulk_palatini_peak=peak(palatini[interior]), **bad_provenance)
    # No universal boundedness: uniform off-graph history drifts exactly.
    drift = Engine(tensor).vacuum(3, [0]*tensor.G)
    drift.a[gi("X.E11")] = drift.a[gi("Y.E11")] = 1
    drift_history, _, drift_provenance = execute(tensor, drift, 8)
    for t, s in enumerate(drift_history):
        assert np.all(s.b[gi("X.E11")] == -t) and np.all(s.b[gi("Y.E11")] == -t)
    detector = lat.index(L//2+1, L//2, 2)
    series = []
    for log in logs:
        found = [int(q) for g, n, q in zip(log.gear, log.node, log.quotient) if int(g) == gi("signal.X") and int(n) == detector]
        series.append(found[0] if found else 0)
    assert any(series)
    return dict(scope="Prepared nonflat pp-wave local-chart embedding, not a global discrete Einstein model",
        tensor=dict(D=6,gears=tensor.G,monomials=len(tensor.monomials),rank=tensor.rank,
                    fingerprint=tensor.fingerprint,strict_single_edge=True,reciprocal=True,
                    components="44 geometric bank registers; 2 signal banks; 2 uncoupled clock controls",
                    not_binary_octahedral_representation=True),
        preparation=preparation, wave=provenance, flat=flat_provenance,
        exact_macro_shift=True, macro_period= L, geometry_micro_period=2*L,
        complete_state_return_at=steps, max_counter=max(s.max_abs() for s in history),
        bulk_events_checked=int(np.count_nonzero(interior))*L, bulk_samples=samples,
        maximum_bulk_curvature_numerator=max_curvature,
        seam_events_with_torsion=seam_torsion, seam_events_with_palatini_failure=seam_einstein,
        metric=dict(coframe_determinant=P**4,metric_determinant=-(P**8),
                    inverse_certificate="E*(2P I-E)=(2P I-E)*E=P^2 I",
                    minimum_timelike_coordinate_clock_norm_squared=clock_min,
                    maximum_timelike_coordinate_clock_norm_squared=clock_max,
                    minimum_spacelike_slice_factor=minimum_slice,
                    varying_clock_norm_is_only_a_metric_prediction=True),
        official=dict(total_records=sum(map(len,logs)),signal_detector=list(lat.coords(detector)),
                      signal_detector_quotients=series,signal_first_detector_event=next(i+1 for i,q in enumerate(series) if q),
                      signal_along_covariantly_constant_null_direction=True,
                      clocks_and_signal_identical_in_flat_and_wave_controls=True,
                      proper_clock_response_pass=False,full_null_cone_response_pass=False),
        negative_controls=bad_results, shifted_product_control=shifted_wedge_counterexample(),
        off_preparation_drift=dict(formula="b_t=-t uniformly in E11 banks",**drift_provenance),
        limitations=["The tensor encodes a known restricted solution family; it is not obtained by varying a discrete Palatini action.",
          "The transverse polynomial is not periodic. Bulk checks pass and periodic seam equations fail.",
          "Centered differences with pointwise wedge are declared diagnostics; shifted exterior-product and gauge covariance are unproved.",
          "P is a fixed integer calibration; stored E,W,inputs and states are integers. No fractional update or seed arithmetic is used.",
          "The 48 registers have explicit bank roles and are not a derived 2O representation.",
          "The co-propagating signal follows one special null geodesic family; it does not test the other null directions or gravitational bending.",
          "Uncoupled clock controls fail proper-clock response. There is no universal operational metric or matter backreaction.",
          "Prepared-sector boundedness does not extend to arbitrary retained histories."])


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--L", type=int, default=7)
    parser.add_argument("--P", type=int, default=256)
    parser.add_argument("--out", type=Path, default=ROOT/"runs/palatini-local/report.json")
    args = parser.parse_args()
    report = run(args.L, args.P)
    report["source_sha256"] = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(report, indent=2)+"\n")
    print(json.dumps({k:report[k] for k in ("scope","tensor","bulk_events_checked","maximum_bulk_curvature_numerator",
                                          "seam_events_with_torsion","seam_events_with_palatini_failure")},indent=2))
