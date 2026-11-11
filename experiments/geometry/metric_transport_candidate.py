"""Optional integer, reciprocal node-flux transport; not Einstein dynamics.

The ordinary scalar Rule3 executes one fixed tensor at divisor six. Local auxiliary
fluxes permit H_xy*j_x*j_y without a three-site gradient product. The same
flat four-field transport block is repeated for matter and metric components.
All construction coefficients and initial data are integers. Fourier formulae
in the report are passive linearization statements, not a second update.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import sys

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from universe24.core import Engine, State, Tensor
from universe24.core.lattice import lattice
from universe24.core.reciprocity import check_reciprocity
from universe24.core.tensor import GearType, LocalityError

ZERO = (0, 0, 0)
AXES = tuple(tuple(int(i == k) for i in range(3)) for k in range(3))
PAIRS = tuple((i, j) for i in range(3) for j in range(i, 3))
METRIC = tuple(f"H{i}{j}" for i, j in PAIRS)
MATTER = ("matter.A", "matter.B")
SPECIES = METRIC + MATTER
SLOTS = ("f", "j0", "j1", "j2")


def negate(x):
    return tuple(-v for v in x)


def differentiate_integer_potential(potential, signs):
    """Construction-time exact integer derivatives, translated to target zero."""
    terms = []
    for coefficient, variables in potential:
        assert type(coefficient) is int
        for position, (target, origin) in enumerate(variables):
            factors = tuple((name, tuple(a-b for a, b in zip(offset, origin)), "b")
                            for k, (name, offset) in enumerate(variables) if k != position)
            terms.append((target, signs[target] * coefficient, factors))
    return terms


def build(g=1, coupling=1):
    """u_f=D*f+g*div(j); u_j=-D*j+g*grad(f), plus local Hjj."""
    assert all(type(v) is int for v in (g, coupling))
    D = 6
    gears, signs, potential = [], {}, []
    for species in SPECIES:
        for slot in SLOTS:
            name = f"{species}.{slot}"
            sign = 1 if slot == "f" else -1
            signs[name] = sign
            why = "Auxiliary flux signature: u_j=-dPhi/dj; the negative sign is explicit in the fixed tensor, not an engine branch."
            gears.append(GearType(name, sign=sign, sign_why=why if sign < 0 else ""))
            potential.append((D // 2, ((name, ZERO), (name, ZERO))))
        for i, edge in enumerate(AXES):
            for coefficient, offset in ((g, edge), (-g, negate(edge))):
                potential.append((coefficient, ((f"{species}.f", ZERO),
                                                (f"{species}.j{i}", offset))))
    for matter in MATTER:
        for i, j in PAIRS:
            coefficient = coupling * (1 if i == j else 2)
            potential.append((coefficient, ((f"H{i}{j}.f", ZERO),
                                            (f"{matter}.j{i}", ZERO),
                                            (f"{matter}.j{j}", ZERO))))
    return Tensor(gears, differentiate_integer_potential(potential, signs),
                  strict_support=True)


def blank(tensor, L=5, remainder=2):
    zeros = np.zeros((tensor.G, L**3), dtype=object)
    return State(L, zeros, zeros.copy(), np.full_like(zeros, remainder))


def replace_seed(tensor, entries, L=5):
    state = blank(tensor, L)
    for name, values in entries.items():
        index = tensor.gear_index(name)
        state.a[index] = values
        state.b[index] = values
    return state


def coordinates(L):
    lat = lattice(L)
    return np.asarray([lat.coords(n) for n in range(lat.N)], dtype=object)


def delta(values, axis, lat):
    return values[..., lat.shift_index(AXES[axis])] - values[..., lat.shift_index(negate(AXES[axis]))]


def peak(values):
    return max((abs(int(v)) for v in np.asarray(values).flat), default=0)


def integer_list(values):
    return [int(v) for v in np.asarray(values).flat]


def trace_digest(states):
    digest = hashlib.sha256()
    for state in states:
        digest.update(json.dumps(state.to_dict(), separators=(",", ":")).encode())
    return digest.hexdigest()


def law_audit(tensor):
    report = check_reciprocity(tensor)
    assert report.ok and not report.designated and not report.skipped_two_time
    assert not tensor.support_violations() and tensor.b_only
    assert tensor.rank == 3
    # The forbidden direct gradient product remains rejected by the validator.
    rejected = False
    try:
        Tensor(("H", "chi"), [("H", 1, (("chi", AXES[0], "b"),
                                           ("chi", AXES[1], "b")))], strict_support=True)
    except LocalityError:
        rejected = True
    assert rejected
    # Extract the degree-one block in relative slot indices; every species must
    # have precisely the same linear operator, not merely the same small-k speed.
    blocks = []
    for species in SPECIES:
        ids = [tensor.gear_index(f"{species}.{slot}") for slot in SLOTS]
        block = []
        for m in tensor.monomials:
            if m.target in ids and m.degree == 1:
                factor = m.factors[0]
                assert factor.gear in ids
                block.append((ids.index(m.target), m.coeff, ids.index(factor.gear), factor.offset))
        blocks.append(sorted(block))
    assert all(block == blocks[0] for block in blocks)
    return dict(D=6, gears=tensor.G, monomials=len(tensor.monomials),
                rank=tensor.rank, max_input_degree=tensor.rank-1, fingerprint=tensor.fingerprint,
                strict_physical_support=True, support_violations=0, reciprocal=True,
                one_way_designations=0, negative_auxiliary_signs=len(report.negative_sign_gears),
                sign_exception="Node flux fields have s=-1. This is signed reciprocity, not an all-positive force potential.",
                old_a_reads=0, identical_complete_flat_linear_blocks=True,
                illegal_direct_cross_gradient_rejected=rejected)


def exact_input_and_backreaction(tensor):
    L = 5
    xyz = coordinates(L)
    impulse = np.asarray([int(all(v == 0 for v in row)) for row in xyz], dtype=object)
    seed = replace_seed(tensor, {"matter.A.j0": 3*impulse, "matter.A.j1": 6*impulse})
    engine = Engine(tensor)
    base = blank(tensor, L)
    initial_u = engine.inputs(seed)
    gi = tensor.gear_index
    assert np.array_equal(initial_u[gi("H00.f")], 9*impulse)
    assert np.array_equal(initial_u[gi("H01.f")], 36*impulse)
    assert np.array_equal(initial_u[gi("H11.f")], 36*impulse)
    after = engine.step(seed)
    empty_after = engine.step(base)
    assert np.array_equal(after.b[gi("H00.f")], 3*impulse)
    assert np.array_equal(after.b[gi("H01.f")], 12*impulse)
    assert np.array_equal(after.b[gi("H11.f")], 12*impulse)
    assert np.any(after.b[:24] != empty_after.b[:24])
    # Same tensor and same matter seed; vary only the initial off-diagonal field.
    hseed = seed.copy()
    hseed.a[gi("H01.f")] = hseed.b[gi("H01.f")] = 1
    hinput = engine.inputs(hseed)
    assert np.array_equal(hinput[gi("matter.A.j0")]-initial_u[gi("matter.A.j0")], -12*impulse)
    assert np.array_equal(hinput[gi("matter.A.j1")]-initial_u[gi("matter.A.j1")], -6*impulse)
    hafter = engine.step(hseed)
    j0_difference = hafter.b[gi("matter.A.j0")]-after.b[gi("matter.A.j0")]
    j1_difference = hafter.b[gi("matter.A.j1")]-after.b[gi("matter.A.j1")]
    assert np.array_equal(j0_difference, -4*impulse)
    assert np.array_equal(j1_difference, -2*impulse)
    assert engine.inverse_step(after).same_as(seed)
    assert engine.inverse_step(hafter).same_as(hseed)
    source_matrix = np.zeros((3, 3, L**3), dtype=object)
    for i, j in PAIRS:
        source_matrix[i, j] = source_matrix[j, i] = initial_u[gi(f"H{i}{j}.f")]
    trace = sum(source_matrix[i, i] for i in range(3))
    divergence = sum(delta(source_matrix[i], i, seed.lattice) for i in range(3))
    assert peak(trace) and peak(divergence)
    return dict(matter_flux_seed_at_origin=[3, 6, 0], metric_inputs_at_origin=dict(H00=9,H01=36,H11=36),
                actual_metric_b_after_one_update=dict(H00=3,H01=12,H11=12),
                H01_background_change=1, actual_matter_flux_b_changes_at_origin=[-4,-2,0],
                exact_inverse=True, source_trace_peak=peak(trace), source_divergence_peak=peak(divergence),
                source_limit="The reciprocal H source is neither TT nor a demonstrated conserved Einstein stress source.")


def independent_integer_oracle(tensor):
    """Audit the compiled potential against explicit input and scalar divmod."""
    results = []
    for amplitude in (1, 2**70):
        shape = (tensor.G, 3**3)
        indices = np.arange(tensor.G*3**3, dtype=np.int64).astype(object).reshape(shape)
        state = State(3, amplitude*((indices*3+1)%11-5),
                      amplitude*((indices*7+2)%13-6), (indices*5+1)%6)
        expected = np.zeros(shape, dtype=object)
        gi = tensor.gear_index
        for species in SPECIES:
            f = gi(f"{species}.f")
            js = [gi(f"{species}.j{i}") for i in range(3)]
            expected[f] = 6*state.b[f]+sum(delta(state.b[j],i,state.lattice) for i,j in enumerate(js))
            for i,j in enumerate(js):
                expected[j] = -6*state.b[j]+delta(state.b[f],i,state.lattice)
        for matter in MATTER:
            js = [gi(f"{matter}.j{i}") for i in range(3)]
            for i,j in PAIRS:
                h = gi(f"H{i}{j}.f")
                expected[h] += (1 if i==j else 2)*state.b[js[i]]*state.b[js[j]]
            for i in range(3):
                for j in range(3):
                    h = gi(f"H{min(i,j)}{max(i,j)}.f")
                    expected[js[i]] -= 2*state.b[h]*state.b[js[j]]
        engine = Engine(tensor)
        assert np.array_equal(engine.inputs(state),expected)
        result = engine.step(state)
        for gear in range(state.G):
            for node in range(state.N):
                quotient,remainder = divmod(2*int(expected[gear,node])+int(state.r[gear,node]),6)
                assert int(result.a[gear,node]) == int(state.b[gear,node])
                assert int(result.b[gear,node]) == quotient-int(state.a[gear,node])
                assert int(result.r[gear,node]) == remainder
        assert engine.inverse_step(result).same_as(state)
        results.append(dict(initial_amplitude=amplitude, exact_inputs=True, exact_scalar_divmod=True,
                            exact_inverse=True, engine_stats=engine.stats))
    return results


def scenario_seed(tensor, mode, background, L=5, amplitude=6):
    xyz = coordinates(L)
    entries = {}
    if mode == "axes":
        phases = (xyz[:, 0], xyz[:, 1])
    elif mode == "angles":
        phases = (xyz[:, 0]+xyz[:, 1], xyz[:, 0]-xyz[:, 1])
    else:
        raise ValueError(mode)
    for matter, phase in zip(MATTER, phases):
        entries[f"{matter}.f"] = np.asarray([amplitude if int(v) % L == 0 else 0 for v in phase], dtype=object)
    entries.update({f"{name}.f": value for name, value in background.items()})
    return replace_seed(tensor, entries, L)


def history_case(tensor, mode, background, steps):
    seed = scenario_seed(tensor, mode, background)
    engine = Engine(tensor)
    state = seed
    history = [state]
    gi = tensor.gear_index
    detectors = ((2,0,0), (0,2,0)) if mode == "axes" else ((1,1,0),(1,4,0))
    indices = [next(n for n in range(state.N) if state.lattice.coords(n) == coord) for coord in detectors]
    records, kinds, series = 0, set(), [[], []]
    remainders_changed = False
    metric_history = []
    for tick in range(1, steps+1):
        previous = state
        state = engine.step(previous)
        history.append(state)
        log = engine.clicks(previous, state, tick).select("official")
        records += len(log)
        kinds.update(int(v) for v in log.kind)
        remainders_changed |= not np.array_equal(state.r, seed.r)
        for k, (matter, node) in enumerate(zip(MATTER, indices)):
            gear = gi(f"{matter}.f")
            matches = log.quotient[(log.gear == gear)&(log.node == node)]
            assert len(matches) <= 1
            series[k].append(int(matches[0]) if len(matches) else 0)
        metric_history.append(max(peak(state.b[gi(f"{name}.f")]) for name in METRIC))
    assert engine.rewind(state, steps).same_as(seed)
    return dict(mode=mode, background=background, steps=steps, detectors=detectors,
                signed_official_scalar_detector_quotients=series, official_records=records,
                observed_kinds=sorted(kinds), remainder_changed=remainders_changed,
                peak_counter=max(state.max_abs() for state in history),
                peak_metric_by_step=metric_history, exact_rewind=True,
                seed_sha256=trace_digest([seed]), final_sha256=trace_digest([state]),
                complete_trace_sha256=trace_digest(history)), history


def response_histories(tensor, steps=8):
    specifications = (("axis_flat","axes",{}), ("axis_plus","axes",{"H00":1,"H11":-1}),
                      ("angle_flat","angles",{}), ("angle_cross","angles",{"H01":1}))
    cases, histories = {}, {}
    for name, mode, background in specifications:
        cases[name], histories[name] = history_case(tensor, mode, background, steps)
    gi = tensor.gear_index
    comparisons = {}
    for mode, reference, changed in (("diagonal_metric","axis_flat","axis_plus"),
                                     ("offdiagonal_metric","angle_flat","angle_cross")):
        per_species = []
        for matter in MATTER:
            f = gi(f"{matter}.f")
            differing = [tick for tick in range(1,steps+1)
                         if not np.array_equal(histories[reference][tick].b[f],histories[changed][tick].b[f])]
            assert differing
            a = cases[reference]["signed_official_scalar_detector_quotients"][MATTER.index(matter)]
            b = cases[changed]["signed_official_scalar_detector_quotients"][MATTER.index(matter)]
            detector_changes = [t+1 for t,(u,v) in enumerate(zip(a,b)) if u!=v]
            assert detector_changes
            per_species.append(dict(species=matter, first_scalar_field_change=differing[0],
                                    detector_changed_updates=detector_changes))
        comparisons[mode] = per_species
    return dict(cases=cases, same_tensor_comparisons=comparisons,
                interpretation="Actual dynamic source runs: background fields backreact and are not held fixed. Quotient changes demonstrate response, not calibrated geodesics or packet speeds.")


def locality_prefix(tensor, steps=3):
    L = 9
    zero = blank(tensor,L)
    perturbed = zero.copy()
    perturbed.b[tensor.gear_index("matter.A.f"), 0] = 9
    e = Engine(tensor)
    left, right = zero, perturbed
    distances = [sum(min(v,L-v) for v in left.lattice.coords(n)) for n in range(left.N)]
    records = []
    for tick in range(1,steps+1):
        left,right = e.step(left),e.step(right)
        changed = np.any((left.a!=right.a)|(left.b!=right.b)|(left.r!=right.r),axis=0)
        furthest = max((distances[n] for n in np.flatnonzero(changed)),default=0)
        assert furthest <= tick
        records.append(dict(step=tick,furthest_changed_face_distance=furthest))
    assert e.rewind(left,steps).same_as(zero) and e.rewind(right,steps).same_as(perturbed)
    return dict(prefix=records, exact_rewinds=True)


def jordan_control(tensor, steps=12):
    seed = blank(tensor,L=3)
    # Metric auxiliary transverse uniform mode has no matter source and u=-D*j.
    gear = tensor.gear_index("H22.j0")
    seed.a[gear] = 1
    engine = Engine(tensor)
    state = seed
    for t in range(1,steps+1):
        state = engine.step(state)
        assert np.all(state.b[gear] == (-1)**t*t)
        assert np.array_equal(state.r,seed.r)
    assert engine.rewind(state,steps).same_as(seed)
    return dict(steps=steps,formula="b_t=(-1)^t*t in uniform H22.j0",peak=state.max_abs(),
                exact_rewind=True,proved_unbounded_off_preparation=True,
                interpretation="Unit-modulus formal eigenvalues include a Jordan endpoint; the complete integer theory is not bounded for arbitrary data.")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out",type=Path,default=ROOT/"runs/metric-transport/candidate.json")
    parser.add_argument("--steps",type=int,default=8)
    args = parser.parse_args()
    if not 4 <= args.steps <= 8:
        parser.error("--steps must be in 4..8: this intentionally unstable candidate is a finite response audit")
    tensor = build()
    report = dict(scope="Optional signed-reciprocal local-flux transport candidate; no Einstein or boundedness claim",
                  source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                  engine_sha256=hashlib.sha256((ROOT/"universe24/core/engine.py").read_bytes()).hexdigest(),
                  law=law_audit(tensor), reciprocal_response=exact_input_and_backreaction(tensor),
                  independent_integer_oracle=independent_integer_oracle(tensor),
                  response_histories=response_histories(tensor,args.steps),
                  locality=locality_prefix(tensor),off_preparation_control=jordan_control(tensor),
                  algebra=dict(
                    integer_potential="Phi0=sum_s [D/2*(f_s^2+sum_i j_si^2)+g*f_s*sum_i delta_i j_si]; Phi_int=kappa*sum_matter [sum_i Hii*ji^2+2*sum_i<j Hij*ji*jj]",
                    constants=dict(D=6,g=1,kappa=1),
                    fixed_input="u_f=D*f+g*div(j)+metric_source; u_ji=-D*ji+g*delta_i(f)-2*kappa*sum_j Hij*jj for matter",
                    update="ell,r_next=divmod(2*u+r,D); a_next=b; b_next=ell-a",
                    passive_flat_symbol="longitudinal lambda^2=D^2-4*g^2*sum_i sin(k_i)^2; cos(omega)=lambda/D; transverse lambda=-D",
                    passive_flat_low_frequency_speed="2*g/D=1/3 coarse sites per scalar update, common to every repeated block",
                    passive_frozen_metric_relation="cos(omega)-1=-(g^2/D)*v^T*[D*(cos(omega)+1)*I+2*kappa*H]^-1*v, v_i=2*sin(k_i)",
                    passive_low_frequency_contravariant_spatial_coefficient="inverse(I+(kappa/D)*H), relative to c0^2=(2*g/D)^2",
                    passive_low_frequency_covariant_spatial_candidate="I+(kappa/D)*H, conditional on unit lapse, zero shift and a separate physical time calibration; no measured spacetime metric is established",
                    passive_frozen_background_instability="For a spatially uniform matter flux along a positive eigenvalue h of fixed H, lambda=-D-2*kappa*h<-D when kappa*h>0. The carry-suppressed linear recurrence has a root outside the unit circle; at divisor six,kappa=h=1, z+z^-1=-8/3. This is a passive frozen-coefficient instability, not an extra runtime with frozen fields.",
                    auxiliary_warning="The j_i are independent node fields. No instantaneous gradient/constitutive graph or its exact preservation is asserted.",
                    fourier_warning="These symbols linearize the polynomial input and suppress carries. Fixed-six Engine runs include remainder changes; equal flat blocks alone do not prove measured universal propagation."),
                  limitations=[
                    "Flux signs are negative in signed reciprocity; an all-positive-potential realization is not supplied.",
                    "Equality of the complete linear transport blocks holds only at H=0. Hjj modifies matter fluxes only, so geometric components do not share the matter frozen-H characteristics on nonzero metric backgrounds.",
                    "Positive H eigenvalues already destabilize a spatially uniform flux mode in the passive frozen-background linearization; the finite actual Engine runs also exhibit very rapid growth.",
                    "The reciprocal metric source violates TT trace and divergence constraints for the demonstrated seed.",
                    "A conserved Einstein stress tensor, lapse/shift constraints and nonlinear Einstein equations are not established.",
                    "Finite reciprocal-response runs do not establish stability; a uniform auxiliary mode is rigorously unbounded.",
                    "All fields, coefficients and seeds are integers. Fractions occur only in passive symbol/continuum interpretation strings.",
                    "Node fluxes are node vectors, not Yee links. Assigning link metadata would alter physical support and needs a new audit."])
    args.out.parent.mkdir(parents=True,exist_ok=True)
    args.out.write_text(json.dumps(report,indent=2)+"\n")
    print(json.dumps(dict(output=str(args.out),law=report["law"],
                          response=report["response_histories"]["same_tensor_comparisons"],
                          all_exact_rewinds=True)))


if __name__ == "__main__":
    main()
