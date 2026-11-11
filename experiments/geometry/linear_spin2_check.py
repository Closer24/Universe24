"""Exact constrained integer curl waves, with a separate 3D instability control.

This isolated experiment uses the unchanged Rule3 engine. It is not a nonlinear
Einstein model or a calibrated detector. Output defaults to ignored runs/.
"""
from __future__ import annotations

import argparse
import itertools
import json
from pathlib import Path
import sys

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from universe24.core import Engine, State, Tensor
from universe24.core.lattice import lattice
from universe24.core.reciprocity import check_reciprocity

EPS = np.zeros((3, 3, 3), dtype=int)
for i, j, k in ((0, 1, 2), (1, 2, 0), (2, 0, 1)):
    EPS[i, j, k] = 1
    EPS[i, k, j] = -1


def build(doubled=False):
    """A column curl, or the original full-nine symmetric extension C."""
    D = 6
    names = [f"{side}{i}{j}" for side in "EB" for i in range(3) for j in range(3)]
    terms = []
    for side, other in (("E", "B"), ("B", "E")):
        for i, j, k, l in itertools.product(range(3), repeat=4):
            sources = [(int(EPS[i, k, l]), l, j)]
            if doubled:
                sources.append((int(EPS[j, k, l]), i, l))
            for coefficient, row, col in sources:
                if coefficient:
                    for sign in (-1, 1):
                        offset = tuple(sign if axis == k else 0 for axis in range(3))
                        terms.append((f"{side}{i}{j}", D // 2 * coefficient * sign,
                                      ((f"{other}{row}{col}", offset, "b"),)))
    return Tensor(names, terms, strict_support=True)


def delta(values, axis, lat):
    offset = tuple(1 if i == axis else 0 for i in range(3))
    back = tuple(-v for v in offset)
    return values[..., lat.shift_index(offset)] - values[..., lat.shift_index(back)]


def vector_curl(v, lat):
    # Independent component oracle, not the production epsilon-term loop.
    return np.array([delta(v[2], 1, lat) - delta(v[1], 2, lat),
                     delta(v[0], 2, lat) - delta(v[2], 0, lat),
                     delta(v[1], 0, lat) - delta(v[0], 1, lat)], dtype=object)


def curl(T, lat, doubled=False):
    result = np.zeros_like(T, dtype=object)
    for j in range(3):
        result[:, j] = vector_curl(T[:, j], lat)
    if doubled:
        for i in range(3):
            result[i] += vector_curl(T[i], lat)
    return result


def maxabs(values):
    return max((abs(int(v)) for v in values.flat), default=0)


def constraints(T, lat):
    divergence = sum(delta(T[i], i, lat) for i in range(3))
    return dict(symmetry=maxabs(T - T.swapaxes(0, 1)),
                trace=maxabs(sum(T[i, i] for i in range(3))),
                divergence=maxabs(divergence))


def dot(a, b):
    return sum(int(x) * int(y) for x, y in zip(a.flat, b.flat))


def phase_seed(E, B, L, doubled=False):
    lat = lattice(L)
    a = np.concatenate((E.reshape(9, -1), (-B + curl(E, lat, doubled)).reshape(9, -1)))
    b = np.concatenate((E.reshape(9, -1), B.reshape(9, -1)))
    r = np.arange(18 * lat.N, dtype=np.int64).astype(object).reshape(18, lat.N) % 6
    return State(L, a, b, r)


def travelling_seed(axes=(2,), L=7):
    lat = lattice(L)
    coords = np.array([lat.coords(n) for n in range(lat.N)])
    E = np.zeros((3, 3, lat.N), dtype=object)
    B = E.copy()
    f = np.array([3, -2, -1, 0, 0, 0, 0], dtype=object)
    g = np.array([2, 0, 0, -1, -1, 0, 0], dtype=object)
    for axis in axes:
        i, j = (axis + 1) % 3, (axis + 2) % 3
        z = coords[:, axis]
        p, q = f[z], g[z]
        sp, sq = f[(z + 1) % L], g[(z + 1) % L]
        E[i, i] += p; E[j, j] -= p
        E[i, j] += q; E[j, i] += q
        B[i, i] -= sq; B[j, j] += sq
        B[i, j] += sp; B[j, i] += sp
    return phase_seed(E, B, L)


def run_travelling(axes):
    tensor = build();engine = Engine(tensor)
    seed = travelling_seed(axes);state = seed
    period = None;records = 0;peak = 0
    lat = seed.lattice
    for tick in range(1, 57):
        previous = state;state = engine.step(state)
        for field in (state.a, state.b):
            for start in (0, 9):
                assert not any(constraints(field[start:start+9].reshape(3, 3, -1), lat).values())
        assert np.array_equal(state.r, seed.r)
        if tick % 2 == 0:
            # Lattice.shift_index accepts face offsets only; this explicit
            # repeated array shift is an independent global translation oracle.
            expected = seed.b.reshape(18, 7, 7, 7)
            for axis in axes:
                expected = np.roll(expected, -tick, axis=axis + 1)
            expected = (-1) ** (tick // 2) * expected.reshape(18, -1)
            assert np.array_equal(state.b, expected)
        log = engine.clicks(previous, state, tick, "official")
        records += len(log)
        assert np.all(log.kind == 0)
        peak = max(peak, state.max_abs())
        if period is None and state.same_as(seed):period = tick
    assert period == 28
    assert engine.rewind(state, 56).same_as(seed)
    return dict(D=6, L=7, axes=list(axes), polarisations=2,
                zero_mean_profiles=True, steps=56, exact_full_state_period=period,
                exact_translation_every_two_updates=True, macro_carrier=-1,
                macro_shift_per_axis=2, peak_counter=peak, official_records=records,
                all_official_kinds_C0=True, all_TT_residuals_zero=True,
                remainders_constant=True, exact_rewind=True,
                rank=tensor.rank, strict_support=True,
                reciprocity=check_reciprocity(tensor).ok,
                tensor_fingerprint=tensor.fingerprint)


def oblique_seed(doubled=False):
    L=5;lat=lattice(L)
    coords=np.array([lat.coords(n) for n in range(lat.N)])
    f=np.array([3,-2,-1,0,0],dtype=object)
    xy=(coords[:,0]+coords[:,1])%L
    xyz=coords.sum(axis=1)%L
    Txy=np.array([[-1,1,0],[1,-1,0],[0,0,2]],dtype=object)
    Txyz=np.array([[2,-4,2],[-4,2,2],[2,2,-4]],dtype=object)
    cross=np.array([[0,0,1],[0,0,-1],[1,-1,0]],dtype=object)
    E=Txy[:,:,None]*f[xy]+Txyz[:,:,None]*f[xyz]
    B=cross[:,:,None]*f[(xy+1)%L]+Txyz[:,:,None]*f[(xyz+2)%L]
    return phase_seed(E,B,L,doubled)


def run_instability(doubled=False):
    tensor=build(doubled);engine=Engine(tensor)
    seed=oblique_seed(doubled);state=seed;lat=seed.lattice
    E,B=seed.b[:9].reshape(3,3,-1),seed.b[9:].reshape(3,3,-1)
    invariant=dot(E,E)+dot(B,B)-dot(E,curl(B,lat,doubled))
    samples=[]
    for tick in range(1,65):
        state=engine.step(state)
        for field in (state.a,state.b):
            for start in (0,9):
                assert not any(constraints(field[start:start+9].reshape(3,3,-1),lat).values())
        assert np.array_equal(state.r,seed.r)
        if tick%2==0:
            E,B=state.b[:9].reshape(3,3,-1),state.b[9:].reshape(3,3,-1)
            assert dot(E,E)+dot(B,B)-dot(E,curl(B,lat,doubled))==invariant
        if tick in (1,2,4,8,16,32,64):
            samples.append(dict(tick=tick,peak_counter=state.max_abs(),bits=state.max_abs().bit_length()))
    assert state.max_abs()>10**12
    assert engine.rewind(state,64).same_as(seed)
    return dict(operator="doubled symmetric extension C" if doubled else "single-index curl A",
                D=6,L=5,steps=64,all_TT_residuals_zero=True,
                remainders_constant=True,exact_rewind=True,
                conserved_macro_quadratic=invariant,quadratic_positive_definite=False,
                growth=samples,scope="Oblique 3D high-wave-number instability despite exact constraints.")


def algebra_audit():
    lat=lattice(3);rng=np.random.default_rng(41)
    X=rng.integers(-3,4,size=(3,3,lat.N)).astype(object)
    Y=rng.integers(-3,4,size=(3,3,lat.N)).astype(object)
    results=[]
    for doubled in (False,True):
        tensor=build(doubled);engine=Engine(tensor)
        b=np.concatenate((X.reshape(9,-1),Y.reshape(9,-1)))
        seed=State(3,b.copy(),b.copy(),np.arange(b.size).reshape(b.shape)%6)
        actual=engine.inputs(seed)
        expected=np.concatenate((curl(Y,lat,doubled).reshape(9,-1),curl(X,lat,doubled).reshape(9,-1)))*3
        assert np.array_equal(actual,expected)
        assert dot(X,curl(Y,lat,doubled))==dot(curl(X,lat,doubled),Y)
        assert check_reciprocity(tensor).ok and not tensor.support_violations()
        results.append(dict(doubled=doubled,independent_input_oracle=True,
                            full_nine_component_self_adjointness=True,
                            reciprocity=True,strict_support=True,monomials=len(tensor.monomials)))
    return results


def rotate_state(state, permutation, signs):
    lat=state.lattice;R=np.zeros((3,3),dtype=np.int64)
    for i,p in enumerate(permutation):R[i,p]=signs[i]
    coords=np.array([lat.coords(n) for n in range(lat.N)],dtype=np.int64).T
    old=(R.T@coords)%state.L
    indices=old[0]*state.L**2+old[1]*state.L+old[2]
    a=np.zeros_like(state.a,dtype=object);b=a.copy();r=a.copy()
    for offset in (0,9):
        for i,j in itertools.product(range(3),repeat=2):
            target=offset+3*i+j;source=offset+3*permutation[i]+permutation[j]
            sign=signs[i]*signs[j]
            a[target]=sign*state.a[source,indices]
            b[target]=sign*state.b[source,indices]
            old_r=state.r[source,indices]
            r[target]=old_r if sign==1 else 5-old_r
    return State(state.L,a,b,r)


def rotation_and_locality_audit():
    tensor=build();engine=Engine(tensor);L=5
    rng=np.random.default_rng(82)
    seed=State(L,rng.integers(-2,3,size=(18,L**3)),
               rng.integers(-2,3,size=(18,L**3)),
               rng.integers(0,6,size=(18,L**3)))
    following=engine.step(seed);rotations=0
    for permutation in itertools.permutations(range(3)):
        parity=(-1)**sum(permutation[i]>permutation[j] for i in range(3) for j in range(i+1,3))
        for signs in itertools.product((-1,1),repeat=3):
            if parity*signs[0]*signs[1]*signs[2]!=1:continue
            rotated=rotate_state(seed,permutation,signs)
            assert engine.step(rotated).same_as(rotate_state(following,permutation,signs))
            rotations+=1
    assert rotations==24
    L=7;zero=np.zeros((18,L**3),dtype=np.int64)
    base=State(L,zero.copy(),zero.copy(),np.full_like(zero,5))
    perturbed=base.copy();perturbed.b[0,0]=1
    lat=base.lattice
    distances=np.array([sum(min(c,L-c) for c in lat.coords(n)) for n in range(lat.N)])
    for tick in range(1,4):
        base,perturbed=engine.step(base),engine.step(perturbed)
        outside=distances>tick
        for field in ('a','b','r'):
            assert np.array_equal(getattr(base,field)[:,outside],getattr(perturbed,field)[:,outside])
    return dict(proper_cube_rotations=rotations,full_state_equivariance=True,
                generic_off_sector_state=True,local_prefix_steps=3,
                no_influence_outside_face_distance=True)


def integer_precision_audit():
    """Amplitude scaling exercises Python integers without changing the divisor."""
    factor = 1 << 70
    left = Engine(build());right = Engine(build())
    a = travelling_seed();b = State(a.L, factor*a.a.astype(object),
                                  factor*a.b.astype(object), a.r.copy())
    seed_left, seed_right = a.copy(), b.copy()
    for tick in range(1,29):
        n,m=left.step(a),right.step(b)
        assert np.array_equal(factor*n.a.astype(object),m.a)
        assert np.array_equal(factor*n.b.astype(object),m.b)
        assert np.array_equal(n.r,m.r)
        a,b=n,m
    assert left.rewind(a,28).same_as(seed_left)
    assert right.rewind(b,28).same_as(seed_right)
    return dict(amplitude_factor=factor,divisor=6,steps=28,
                exact_scaled_counter_histories=True,exact_rewind=True,
                arbitrary_precision_exercised=right.stats["pyint_steps"]>0)


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out',type=Path,default=ROOT/'runs/geometry/linear_spin2.json')
    args=parser.parse_args()
    result=dict(scope="Exact prepared linear TT curl sector; no nonlinear Einstein metric, common matter coupling, or calibrated physical detector.",
                algebra_audit=algebra_audit(),
                rotation_and_locality=rotation_and_locality_audit(),
                integer_precision=integer_precision_audit(),
                travelling=[run_travelling(axes) for axes in ((2,),(0,1,2))],
                instability_controls=[run_instability(False),run_instability(True)])
    args.out.parent.mkdir(parents=True,exist_ok=True)
    args.out.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))


if __name__=='__main__':main()
