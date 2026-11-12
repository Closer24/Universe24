"""Reciprocal face-coupling control, not the coupled Einstein/apparatus law.

Run: python -m validation.synthesis.matter_backreaction --out runs/synthesis/matter_backreaction.json
"""
from __future__ import annotations

import argparse
from fractions import Fraction
import hashlib
from itertools import product
import json
from pathlib import Path
import subprocess

import numpy as np
import sympy as sp

from universe24.core import Engine, GearType, State, Tensor, check_reciprocity
from validation.system_smoke import scalar_step

NAMES = ('carrier.real', 'carrier.imag', 'receiver.real', 'receiver.imag')
ROOT = Path(__file__).resolve().parents[2]


def tensor(*, nonlinear=0, one_way=False):
    """Each z(x) exchanges with w(x+e1); every monomial is one-face local."""
    terms = []
    symbols = sp.symbols('x y X Y')
    x, y, xx, yy = symbols
    radius2 = (x-xx)**2 + (y-yy)**2
    for target in range(4):
        component = target % 2
        source = target < 2
        own = (0, 1) if source else (2, 3)
        other = (2, 3) if source else (0, 1)
        offset = (1, 0, 0) if source else (-1, 0, 0)
        variable = symbols[component]
        force = 0 if one_way and source else -(1+nonlinear*radius2)*(variable-symbols[component+2])
        polynomial = sp.Poly(sp.expand(3*(2*variable+force)), *symbols)
        ports = [(own[0], (0,0,0)), (own[1], (0,0,0)), (other[0], offset), (other[1], offset)]
        for powers, coefficient in polynomial.terms():
            factors = [(NAMES[g], off, 'b') for (g, off), power in zip(ports, powers) for _ in range(power)]
            terms.append((NAMES[target], int(coefficient), factors))
    return Tensor([GearType(n, label='audit') for n in NAMES], terms, strict_support=True)


def invariants(state, nonlinear=0):
    a, b = state.a.astype(object), state.b.astype(object)
    shift = state.lattice.shift_index((1,0,0))
    da, db = a[:2]-a[2:,shift], b[:2]-b[2:,shift]
    kinetic2 = sum(int(v)**2 for v in (b-a).flat)
    polarized = kinetic2 + sum(int(x)*int(y) for x,y in zip(da.flat, db.flat))
    radii = [sum(int(db[i,n])**2 for i in range(2)) for n in range(state.N)]
    point_energy = Fraction(kinetic2,2) + sum(Fraction(r,2)+Fraction(nonlinear*r*r,4) for r in radii)
    charge = sum(int(a[g,n])*int(b[g+1,n])-int(a[g+1,n])*int(b[g,n])
                 for g in (0,2) for n in range(state.N))
    momentum = [sum(int(b[g,n])-int(a[g,n]) for g in (i,i+2) for n in range(state.N)) for i in (0,1)]
    return {'charge': charge, 'internal_translation_momentum': momentum,
            'linear_polarized_invariant': polarized, 'naive_point_energy': point_energy}


def explicit_pair(old, now, nonlinear, one_way=False):
    d = [now[i]-now[i+2] for i in range(2)]
    factor = 1+nonlinear*sum(v*v for v in d)
    forces = [0 if one_way else -factor*d[0], 0 if one_way else -factor*d[1], factor*d[0], factor*d[1]]
    return tuple(2*b-a+f for a,b,f in zip(old, now, forces))


def pair_invariants(old, now, nonlinear=0):
    kinetic2=sum((b-a)**2 for a,b in zip(old,now))
    da=[old[i]-old[i+2] for i in (0,1)]
    db=[now[i]-now[i+2] for i in (0,1)]
    radius=sum(v*v for v in db)
    return {'charge':sum(old[g]*now[g+1]-old[g+1]*now[g] for g in (0,2)),
            'internal_translation_momentum':[sum(now[g]-old[g] for g in (i,i+2)) for i in (0,1)],
            'linear_polarized_invariant':kinetic2+sum(a*b for a,b in zip(da,db)),
            'naive_point_energy':Fraction(kinetic2+radius,2)+Fraction(nonlinear*radius*radius,4)}


def run():
    # Exhaustive scalar identity controls independent of Tensor/Engine evaluation.
    scalar_cases = 0
    for old in product((-1,0,1), repeat=4):
        for now in product((-1,0,1), repeat=4):
            inv = pair_invariants(old, now)
            for nonlinear in (0,1):
                nxt = explicit_pair(old, now, nonlinear)
                after = pair_invariants(now, nxt, nonlinear)
                assert inv['charge'] == after['charge']
                assert inv['internal_translation_momentum'] == after['internal_translation_momentum']
                if not nonlinear:
                    assert inv['linear_polarized_invariant'] == after['linear_polarized_invariant']
                for carry in range(6):
                    for a,b,c in zip(old, now, nxt):
                        u = 3*(c+a)
                        ell, remainder = divmod(2*u+carry,6)
                        assert (ell-a,remainder) == (c,carry)
                        assert ell-c == a
                    scalar_cases += 1

    rng = np.random.default_rng(604413)
    rows = []
    for nonlinear, one_way in ((0,False),(1,False),(0,True),(1,True)):
        law = tensor(nonlinear=nonlinear, one_way=one_way)
        reciprocity = check_reciprocity(law)
        assert reciprocity.ok == (not one_way)
        engine = Engine(law)
        charge_defect = momentum_defect = polarized_defect = 0
        point_defect = Fraction(0)
        max_bits = 0
        transitions = 0
        for carry in range(6):
            a = rng.integers(-2,3,(4,27)).astype(object)
            b = rng.integers(-2,3,(4,27)).astype(object)
            if carry == 5:
                a[0,0] = 2**120+3
                b[3,-1] = -(2**121+7)
            state = State(3,a,b,np.full((4,27),carry,dtype=int))
            seed = state.copy()
            for _ in range(3):
                before = invariants(state, nonlinear)
                nxt = engine.step(state)
                assert nxt.same_as(scalar_step(law,state))
                assert engine.inverse_step(nxt).same_as(state)
                assert np.array_equal(nxt.r,state.r)
                after = invariants(nxt, nonlinear)
                charge_defect = max(charge_defect,abs(after['charge']-before['charge']))
                momentum_defect = max(momentum_defect,max(abs(x-y) for x,y in zip(after['internal_translation_momentum'],before['internal_translation_momentum'])))
                polarized_defect = max(polarized_defect,abs(after['linear_polarized_invariant']-before['linear_polarized_invariant']))
                point_defect = max(point_defect,abs(after['naive_point_energy']-before['naive_point_energy']))
                max_bits = max(max_bits,max(abs(int(v)).bit_length() for v in nxt.a.flat),max(abs(int(v)).bit_length() for v in nxt.b.flat))
                state=nxt
                transitions += 1
            for _ in range(3):
                state=engine.inverse_step(state)
            assert state.same_as(seed)
        if not one_way:
            assert charge_defect == momentum_defect == 0
            if not nonlinear:
                assert polarized_defect == 0
        else:
            assert charge_defect > 0 and momentum_defect > 0
        assert point_defect > 0
        rows.append({'nonlinear':nonlinear,'one_way':one_way,'channels':law.G,
                     'degree':law.rank-1,'monomials':len(law.monomials),'reciprocity':reciprocity.ok,
                     'engine_transitions':transitions,'complete_oracle_and_inverse':'passed',
                     'charge_max_defect':str(charge_defect),'internal_translation_momentum_max_defect':str(momentum_defect),
                     'linear_polarized_max_defect':str(polarized_defect),
                     'naive_point_energy_max_defect':str(point_defect),'max_integer_bits':max_bits})
    # Minimal counterexamples easy to inspect, independent of random controls.
    counterexamples = []
    for old,now in (((1,0,0,1),(1,0,0,1)), ((0,0,0,0),(1,0,0,0))):
        for nonlinear,one_way in ((0,False),(1,False),(0,True)):
            nxt=explicit_pair(old,now,nonlinear,one_way)
            before=pair_invariants(old,now,nonlinear)
            after=pair_invariants(now,nxt,nonlinear)
            counterexamples.append({'old':old,'now':now,'next':nxt,'nonlinear':nonlinear,'one_way':one_way,
                                    'charge_before':before['charge'],'charge_after':after['charge'],
                                    'point_energy_before':str(before['naive_point_energy']),
                                    'point_energy_after':str(after['naive_point_energy']),
                                    'polarized_before':before['linear_polarized_invariant'],
                                    'polarized_after':after['linear_polarized_invariant']})
    files = [Path(__file__),ROOT/'universe24/core/engine.py',ROOT/'universe24/core/tensor.py',ROOT/'validation/system_smoke.py']
    return {'schema':'universe24/synthesis/backreaction/1','status':'passed_scoped_algebra_controls',
            'scope':'Isolated four-channel reciprocal face-pair control; not appended to 44-channel Einstein model',
            'source_commit':subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),
            'source_hashes':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in files},
            'command':'python -m validation.synthesis.matter_backreaction --out runs/synthesis/matter_backreaction.json',
            'exhaustive_signed_scalar_carry_cases':scalar_cases,'rows':rows,'small_counterexamples':counterexamples,
            'proposed_ledger':'Reuse two carrier components plus two receiver components: 44+2=46 slots, but projective denominator compatibility and coupled stress have NOT been compiled.',
            'limits':['Internal translation momentum is a configuration-space symmetry invariant, not established spacetime momentum.',
                      'Linear time-polarized invariant is not a calibrated Einstein energy density.',
                      'Cubic reciprocal forces preserve the tested global charge, not exact naive energy.',
                      'Only globally shared phase symmetry is proved; no local gauge transporter.',
                      'Fixed face pairing is not a full three-direction apparatus or metric-coupled detector.',
                      'Cubic control integer growth is measured, not solved.'],
            'primary_sources':['https://lagrange.mechse.illinois.edu/pubs/MaWe2001/MaWe2001.pdf',
                               'https://lagrange.mechse.illinois.edu/var_int/']}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out',type=Path,required=True)
    args=parser.parse_args()
    evidence=run()
    args.out.parent.mkdir(parents=True,exist_ok=True)
    args.out.write_text(json.dumps(evidence,indent=2)+'\n')
    print(json.dumps({'out':str(args.out),'status':evidence['status'],
                      'scalar_cases':evidence['exhaustive_signed_scalar_carry_cases'],
                      'engine_transitions':sum(r['engine_transitions'] for r in evidence['rows'])}))


if __name__=='__main__':
    main()
