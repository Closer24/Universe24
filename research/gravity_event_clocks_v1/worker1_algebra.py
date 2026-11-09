#!/usr/bin/env python3
"""Worker 1: exact discrete event-wave identity, bounded-time no-go, action extension tangent."""
from __future__ import annotations
import itertools,json,random,math
from pathlib import Path
from collections import deque,defaultdict
from universe24.core.state import Cube,State,Channel
from universe24.core.engine import Engine
from universe24.core.coupling import Coupling
from universe24.core.group_2o import DIRECTIONS

ROOT=Path(__file__).resolve().parent
OUT=ROOT/'results'; OUT.mkdir(exist_ok=True)

def p(v): return 3*(v.b-v.a)+(v.r//2)-1

def exact_update_checks():
    rng=random.Random(20261109)
    summary=[];channel_tests=0; parity_tests=0; anti=0
    for signs in itertools.product((-1,1),repeat=3):
        eng=Engine(Coupling(tuple(signs)))
        for L in (3,4):
            cube=Cube(L)
            cells={(x,y,z,g):Channel(rng.randint(-6,6),rng.randint(-6,6),rng.randrange(6))
                   for x in range(L) for y in range(L) for z in range(L) for g in range(48)}
            old=State(cube,cells=cells)
            nxt=eng.advance(old)
            assert eng.rewind(nxt)==old
            sums=eng.input_sums(old)
            for address in cells:
                prev=old.at(address); after=nxt.at(address)
                u=sums.get(address,0); lap=6*prev.b-u
                # exact integer wave equation, no approximations/limits:
                residual=6*(after.b-2*prev.b+prev.a)+2*lap+(after.r-prev.r)
                assert residual==0,(signs,L,address,residual)
                assert p(after)-p(prev)==-lap
                assert after.r%2==prev.r%2
                # signed arithmetic current identity is local even if global Q not conserved
                assert 6*(after.b-after.a)+after.r-(6*(prev.b-prev.a)+prev.r)==-2*lap
                channel_tests+=1; parity_tests+=1
            summary.append({'signs':signs,'L':L,'all_channel_addresses_checked':48*L**3,
                            'forward_reverse_equal':True,'exact_integer_event_wave_residual_max':0})
    return {'signed_full_board_cases':len(summary),'full_address_update_checks':channel_tests,
            'exact_integer_wave_eq':'6*(b[n+1]-2*b[n]+b[n-1])+2*(L_sigma b[n])+(r[n+1]-r[n])=0',
            'exact_phase_eq':'p[n+1]-p[n]=-(L_sigma b[n])',
            'all_signed_choices':summary}

def connectivity(L):
    c=Coupling();start=(0,0,0,0); seen={start};q=deque([start])
    while q:
        x,y,z,g=q.popleft()
        for d,(dx,dy,dz) in enumerate(DIRECTIONS):
            nxt=((x+dx)%L,(y+dy)%L,(z+dz)%L,c.ports[d][g])
            if nxt not in seen:seen.add(nxt);q.append(nxt)
    return {'L':L,'reachable':len(seen),'total':48*L**3,'connected':len(seen)==48*L**3}

def periodic_constraint():
    e=Engine();L=7;src=(3,3,3);probe=(4,3,3);A=Channel(-1,-1,0)
    init=State(Cube(L),cells={**{(*src,g):A for g in range(48)},**{(*probe,g):A for g in range(48)}})
    s=init;lap_sum=defaultdict(int); p0=defaultdict(int);pt=defaultdict(int)
    for t in range(20):
        u=e.input_sums(s)
        for address in s.cells.keys()|u.keys():
            v=s.at(address); lap_sum[address]+=6*v.b-u.get(address,0)
        s=e.advance(s)
    assert s==init
    assert all(t==0 for t in lap_sum.values()),len([x for x in lap_sum.values() if x])
    return {'complete_period':20,'full_state_return':True,'exact_laplacian_time_sum_all_addresses_zero':True,
            'finite_cover_connectivity':[connectivity(n) for n in (3,4,5,6)],
            'theorem':'for every bounded trajectory, abs(L mean_T b)_nu=abs(p_T-p_0)_nu/T ->0; for a complete period it equals zero exactly',
            'scope':'mean b only; does not rule out phase-correlation or nonperiodic gravity'}

def parity_superselection_check():
    """Arbitrary per-address r parity choices are entirely invisible to (a,b,theta) evolution."""
    rng=random.Random(991108);checks=0;cases=[]
    for signs in itertools.product((-1,1),repeat=3):
        e=Engine(Coupling(tuple(signs)));L=3;addresses=[(x,y,z,g) for x in range(L) for y in range(L) for z in range(L) for g in range(48)]
        cells={a:Channel(rng.randint(-2,2),rng.randint(-2,2),2*rng.randrange(3)+rng.randrange(2)) for a in addresses}
        mask={a:rng.getrandbits(1) for a in addresses}
        twin={a:Channel(v.a,v.b,v.r^mask[a]) for a,v in cells.items()}
        s=State(Cube(L),cells=cells);t=State(Cube(L),cells=twin)
        for time in range(7):
            for addr in addresses:
                x=s.at(addr);y=t.at(addr)
                assert (x.a,x.b,x.r//2)==(y.a,y.b,y.r//2)
                assert (x.r^y.r)==mask[addr]
                checks+=1
            if time<6:
                s=e.advance(s);t=e.advance(t)
        cases.append({'signs':signs,'addresses':len(addresses),'times':7,'all_counter_theta_same':True,'arbitrary_parity_mask_retained':True})
    return {'exact_decoupling_identity':'divmod(2u+2theta+epsilon,6)=(floor((u+theta)/3),2*((u+theta) mod 3)+epsilon)',
            'parity_bit_is_completely_inert_for_a_b_theta':True,
            'all48_per_site_still_retained_exactly':True,
            'arbitrary_local_parity_experiment_full_states':checks,'cases':cases}

def tooth_D(z):
    k=math.floor(z/3);t=z-3*k
    if t<=1:return k
    if t<=2:return k+3*(t-1)**2-2*(t-1)**3
    return k+1

def smooth_tangent_obstruction():
    # Value interpolation in current repo has zero first derivative at EVERY integer.
    sample_values=[]
    h=1e-5
    for m in range(-60,61):
        assert tooth_D(float(m))==(m+1)//3
        approx=(tooth_D(m+h)-tooth_D(m-h))/(2*h)
        assert abs(approx)<1e-3
        sample_values.append(abs(approx))
    return {'integer_samples':len(sample_values),'max_approx_derivative_h1e-5':max(sample_values),
            'exact_piecewise_derivative_at_all_integers':'0 (flat plateau and cubic smoothstep has zero endpoint slope)',
            'auxiliary_symplectic_tangent_map_at_integer':'delta_b_next=delta_b; delta_p_next=delta_p-L_sigma delta_b',
            'T_step_jacobian':'[[I,0],[-T*L_sigma,I]] when all iterates are integer',
            'relevance':'arbitrary real interpolation is not calibrated photon or gravitational spin-2 propagation; finite integer pulses can still change b'}

def run():
    report={'worker':'A_exact_event_algebra','status':'PASS',
            'wave':exact_update_checks(),
            'bounded_source':periodic_constraint(),
            'smooth_tangent':smooth_tangent_obstruction(),
            'parity_decoupling':parity_superselection_check()}
    path=OUT/'worker1_algebra.json';path.write_text(json.dumps(report,indent=2,ensure_ascii=False)+'\n')
    print(json.dumps({'worker':report['worker'],'status':report['status'],'channel_checks':report['wave']['full_address_update_checks'],'path':str(path)}),flush=True)
    return report

if __name__=='__main__':run()
