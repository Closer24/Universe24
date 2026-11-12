"""Independent fixed-domain validation of the new projective Engine encoding.

No runtime correction, clipping, constraint projection, or floating state.
The independent continuum/finite-difference planar RHS is used only as an
oracle, never to evolve the actual integer Engine.
"""
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path
import time
import numpy as np

from universe24.core import Engine
from universe24.core.lattice import lattice
from .refinement_integer_projective import build_charged, prepare
from .validation_repair_seed import smooth_integer_seed, diagnostic_fields, literal_metric_constraints

ROOT=Path(__file__).resolve().parents[3]


def planar_rhs(f, dx):
    """Independent diagonal-plane Einstein/massless-scalar/square-dust RHS.

    From ds3²=b^-2 dx²+c^-2(dy²+dz²), orthonormal K=(k,l,l),
    g=<nabla_e1 e1,e0>=<nabla_e2 e2,e0>, and Pi=n(phi).
    Uses only these reduced coordinate formulas, no production equations.
    """
    def D(a):return (np.roll(a,-1)-np.roll(a,1))/(2*dx)
    b,c,k,l,g,pi,psi,d=(f[n] for n in ('B00','B11','K00','K11','G011','Pi_phi','Xi_phi0','dust_amplitude'))
    tr=k+2*l
    R0=2*b*D(g)-2*g*g
    R1=b*D(g)-2*g*g
    result={n:np.zeros_like(v) for n,v in f.items()}
    result.update(B00=k*b, B11=l*c, B22=l*c,
                  K00=R0+tr*k-psi*psi-d*d/2,
                  K11=R1+tr*l-d*d/2, K22=R1+tr*l-d*d/2,
                  G011=b*D(l)+k*g, G022=b*D(l)+k*g,
                  phi=pi, Pi_phi=b*D(psi)-2*g*psi+tr*pi,
                  Xi_phi0=b*D(pi)+k*psi, dust_amplitude=tr*d/2)
    return result


def binary_state_hash(state):
    h=hashlib.sha256()
    h.update(f'{state.L},{state.G}'.encode())
    for block in (state.a,state.b,state.r):
        for v in block.flat:
            v=int(v); data=abs(v).to_bytes(max(1,(abs(v).bit_length()+7)//8),'big')
            h.update(bytes([int(v<0)]));h.update(len(data).to_bytes(8,'big'));h.update(data)
    return h.hexdigest()


def run_case(n, dt, *, final_time=F(1,16), resolution=2**24):
    started=time.monotonic()
    dt=F(dt); steps=final_time/dt
    if steps.denominator!=1:raise ValueError('Fixed final time must contain integral updates')
    steps=int(steps)
    program=build_charged(dt=dt,dx=F(1,n))
    numerators,seed_report=smooth_integer_seed(program.fields,n,resolution)
    lat=lattice(n);x=lat.all_coords()[:,0]
    current=np.asarray([[F(int(v),resolution) for v in row[x]] for row in numerators],dtype=object)
    remainders=np.asarray([[int((i+j)%6) for j in range(lat.N)] for i in range(program.tensor.G)],dtype=object)
    state=seed=prepare(program,current,L=n,denominator=resolution,remainders=remainders)
    engine=Engine(program.tensor)
    line=np.asarray([lat.index(j,0,0) for j in range(n)])
    initial=diagnostic_fields(program.fields,state.b[1:,line],state.b[0,line])
    initial_diagnostic=literal_metric_constraints(initial,F(1,n))
    first_expected={name:value+float(dt)*planar_rhs(initial,1/n)[name] for name,value in initial.items()}
    max_bits=[];first_error=None
    for tick in range(steps):
        previous=state
        state=engine.step(state)
        assert np.array_equal(state.r,seed.r)
        assert np.all(state.b[0]==state.b[0,0]) and int(state.b[0,0])>0
        if tick==0:
            first=diagnostic_fields(program.fields,state.b[1:,line],state.b[0,line])
            first_error=max(float(np.max(np.abs(first[n]-v))) for n,v in first_expected.items())
            assert first_error<1e-12,first_error
        max_bits.append(max(abs(int(v)).bit_length() for v in state.b[:,line].flat))
    final=diagnostic_fields(program.fields,state.b[1:,line],state.b[0,line])
    result=literal_metric_constraints(final,F(1,n))
    # An independently coded planar reference is not fundamental arithmetic.
    # Keep it outside the Engine and report that boundary explicitly.
    reference={name:value.copy() for name,value in initial.items()}
    for _ in range(steps):
        rhs=planar_rhs(reference,1/n)
        reference={name:value+float(dt)*rhs[name] for name,value in reference.items()}
    euler_difference=max(float(np.max(np.abs(final[name]-v))) for name,v in reference.items())
    final_hash=binary_state_hash(state)
    assert engine.rewind(state,steps).same_as(seed)
    return {'n':n,'dt':str(dt),'dx':str(F(1,n)),'final_time':str(final_time),
            'updates':steps,'channels':program.tensor.G,'degree':program.degree,
            'monomials':len(program.tensor.monomials),'static_multiplier':program.multiplier,
            'seed':seed_report,'initial_literal_metric':initial_diagnostic,
            'final_literal_metric':result,'independent_first_step_Euler_max_error':first_error,
            'independent_finite_time_Euler_max_error':euler_difference,
            'diagnostic_final_fields':{name:values.tolist() for name,values in final.items()},
            'max_retained_bit_length_per_update':max_bits,
            'nonzero_carries_unchanged':True,'complete_exact_rewind':True,
            'strict_face_support':not bool(program.tensor.support_violations()),
            'tensor_sha256':hashlib.sha256(json.dumps(program.tensor.to_dict(),sort_keys=True).encode()).hexdigest(),
            'seed_state_binary_sha256':binary_state_hash(seed),
            'final_state_binary_sha256':final_hash,
            'seconds':time.monotonic()-started}


def smooth_reference(n=384, steps=1024, final_time=F(1,16)):
    """Independent floating RK4 reference, never a fundamental Engine state."""
    names=build_charged().fields
    x=np.arange(n)/n
    f={name:np.zeros(n) for name in names}
    for axis in range(3):f[f'B{axis}{axis}'][:]=1
    f['phi']=np.sin(2*np.pi*x)/16
    f['Pi_phi'][:]=2
    f['Xi_phi0']=(2*np.pi/16)*np.cos(2*np.pi*x)
    f['K11']=2+f['phi'];f['K22']=f['K11'].copy()
    f['dust_amplitude']=np.sqrt(f['K11']**2-2-f['Xi_phi0']**2/2)
    h=float(final_time)/steps
    for _ in range(steps):
        k1=planar_rhs(f,1/n)
        k2=planar_rhs({name:v+h*k1[name]/2 for name,v in f.items()},1/n)
        k3=planar_rhs({name:v+h*k2[name]/2 for name,v in f.items()},1/n)
        k4=planar_rhs({name:v+h*k3[name] for name,v in f.items()},1/n)
        f={name:v+h*(k1[name]+2*k2[name]+2*k3[name]+k4[name])/6 for name,v in f.items()}
    return f


def run(out):
    out=Path(out);out.mkdir(parents=True,exist_ok=True)
    cases=[]
    # Separate temporal, spatial, and joint rows reuse the same physical
    # profile/domain, fixed final time, units, and independent diagnostics.
    parameters=[(4,F(1,32)),(8,F(1,64)),(16,F(1,128)),
                (8,F(1,32)),(8,F(1,128)),(4,F(1,128)),(12,F(1,64)),(12,F(1,96))]
    for n,dt in parameters:
        row=run_case(n,dt)
        cases.append(row)
        print(json.dumps({k:row[k] for k in ('n','dt','updates','final_literal_metric','max_retained_bit_length_per_update','seconds')}),flush=True)
        (out/'projective_progress.json').write_text(json.dumps(cases,indent=2)+'\n')
    quantization=[]
    for q in (2**4,2**8,2**12,2**24):
        row=run_case(8,F(1,64),resolution=q)
        quantization.append(row)
    by_case={(r['n'],r['dt']):r for r in cases}
    groups={'time':[(8,'1/32'),(8,'1/64'),(8,'1/128')],
            'space':[(4,'1/128'),(8,'1/128'),(16,'1/128')],
            'joint_original':[(4,'1/32'),(8,'1/64'),(16,'1/128')],
            'joint_better_resolved':[(8,'1/32'),(12,'1/64'),(16,'1/128')],
            'joint_additional_four_six_eight_steps':[(8,'1/64'),(12,'1/96'),(16,'1/128')]}
    required=('H_linf','M0_linf','gradient_linf','connection_metric_linf')
    gates={}
    for group,keys in groups.items():
        selected=[by_case[k]['final_literal_metric'] for k in keys]
        components={name:all(selected[i+1][name]<selected[i][name] for i in range(len(selected)-1)) for name in required}
        gates[group]={'strict_decrease':components,'all_four_decrease':all(components.values())}
    fine=smooth_reference(384,1024);medium=smooth_reference(192,512)
    reference_difference=max(float(np.max(np.abs(fine[name][::2]-v))) for name,v in medium.items())
    for row in cases:
        stride=384//row['n']
        row['independent_RK4_field_error_linf']=max(float(np.max(np.abs(np.asarray(v)-fine[name][::stride])))
                                                 for name,v in row['diagnostic_final_fields'].items())
    report={'scope':'Actual projective integer Engine, smooth periodic sourced plane-symmetric finite-time refinement. Not a general-GR or physical-apparatus validation.',
            'precision':'Exact integer fundamental state; independent float diagnostic and reference only',
            'case_definitions':{'time':'n8; h1/32,1/64,1/128','space':'h1/128; n4,8,16',
                                'joint_original':'(n4,h1/32),(n8,h1/64),(n16,h1/128)',
                                'joint_better_resolved':'(n8,h1/32),(n12,h1/64),(n16,h1/128)',
                                'joint_additional_four_six_eight_steps':'(n8,h1/64),(n12,h1/96),(n16,h1/128)',
                                'seed_quantization':'n8,h1/64; Q16,256,4096,16777216'},
            'acceptance_protocol':'For each named refinement group require strict decrease of every unscaled final H/M/gradient/connection-metric residual; report failure without discarding the run.',
            'protocol_extension_disclosure':'After the original and better-resolved groups failed, one additional n12,h1/96 row tested four/six/eight updates. All earlier rows and failed gates remain. A monotonic sequence is comparative evidence, not an asymptotic convergence proof.',
            'gates':gates,'cases':cases,'quantization_cases':quantization,
            'independent_reference':{'method':'separate planar coordinate RHS, floating RK4, analytic smooth initial data',
                                     'fine_grid':384,'fine_updates':1024,'medium_grid':192,'medium_updates':512,
                                     'nested_field_difference_linf':reference_difference},
            'limitations':['Short fixed physical time1/16','Plane symmetry, neutral real scalar subset; charged/Maxwell fields zero',
                           'No nondegeneracy theorem for arbitrary projective seeds',
                           'Exponentially growing denominator bits; no bounded-memory claim',
                           'Finite-grid metric and frame curvature observers have different truncation errors'],
            'source_sha256':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest()
                             for p in [Path(__file__),Path(__file__).with_name('validation_repair_seed.py'),Path(__file__).with_name('refinement_integer_projective.py')]}}
    (out/'projective_validation.json').write_text(json.dumps(report,indent=2)+'\n')
    return report


if __name__=='__main__':
    run(ROOT/'runs/team48/validation_repair')
