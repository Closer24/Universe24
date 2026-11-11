"""Exact passive linearized-curvature identities for the prepared TT metric."""
from pathlib import Path
import json
import numpy as np

def run():
    L=7;M=7;P=4096;R=M*P
    hp=np.array([120,-96,24,-24,-16,48,-56],dtype=object)
    hq=np.array([80,-32,24,-32,-32,24,-32],dtype=object)
    p=np.array([3,-2,-1,0,0,0,0],dtype=object)
    q=np.array([2,0,0,-1,-1,0,0],dtype=object)
    coords=np.indices((L,L,L,L));phase=(coords[0]+coords[3])%L
    h=np.zeros((4,4,L,L,L,L),dtype=object)
    h[1,1]=hp[phase];h[2,2]=-hp[phase];h[1,2]=hq[phase];h[2,1]=hq[phase]
    eta=[-1,1,1,1]
    def d(f,mu):return np.roll(f,-1,axis=mu)-np.roll(f,1,axis=mu)
    def dd(f,mu,nu):return d(d(f,nu),mu)
    def box(f):return sum(eta[mu]*dd(f,mu,mu) for mu in range(4))
    trace=sum(eta[mu]*h[mu,mu] for mu in range(4))
    assert np.all(trace==0)
    ricci=[]
    for mu in range(4):
     for nu in range(4):
      value=sum(eta[sigma]*(dd(h[sigma,mu],sigma,nu)+dd(h[sigma,nu],sigma,mu)) for sigma in range(4))-dd(trace,mu,nu)-box(h[mu,nu])
      assert np.all(value==0);ricci.append(0)
    # R_0i0j=-1/2 partial_t^2 h_ij. Unnormalised central d=2 partial;
    # the integer numerator below is 8 R times the linearized Riemann entry.
    assert np.array_equal(-dd(h[1,1],0,0),8*M*p[phase])
    assert np.array_equal(-dd(h[1,2],0,0),8*M*q[phase])
    # Linear Hamiltonian and momentum constraints with flat raising.
    spatial_trace=sum(h[i,i] for i in range(1,4))
    hamiltonian=sum(dd(h[i,j],i,j) for i in range(1,4) for j in range(1,4))-sum(dd(spatial_trace,i,i) for i in range(1,4))
    assert np.all(hamiltonian==0)
    for j in range(1,4):assert np.all(sum(dd(h[i,j],i,0) for i in range(1,4))-dd(spatial_trace,j,0)==0)
    result={'scope':'Passive exact linearized Einstein operator on the reconstructed axis TT metric, using stated central differences; not nonlinear GR or the probe-inferred metric',
     'L':L,'metric_denominator':R,'integer_hplus':list(map(int,hp)),'integer_hcross':list(map(int,hq)),
     'microtime_profile':'h(t,z)=H[(t+z) mod7]/(M P)',
     'derivative_convention':'D_mu=(shift_plus_mu-shift_minus_mu)/2 in unit lattice spacing; curvature uses D_mu D_nu, a two-cell second-derivative stencil',
     'all_16_linearized_Ricci_components_zero':True,'linear_Hamiltonian_constraint_zero':True,'all_linear_momentum_constraints_zero':True,
     'electric_Riemann_matches_original_curvature_profiles':True,'trace_and_transversality_exact':True,
     'maximum_squared_integer_polarisation_amplitude':int(max(hp*hp+hq*hq)),
     'spatial_signature_positive':bool(max(hp*hp+hq*hq)<R*R),
     'limitations':['Geometry is reconstructed from a prepared profile and internal phase registers, not inferred from official events alone.','The exact statements refer to the declared linearized difference operator; the nonlinear Einstein residual is not zero.','Nearest-neighbor and central-derivative-squared curvature stencils are different at finite lattice spacing.','The separately tested scalar probe has a different flat characteristic speed, so this does not produce one universal metric.']}
    return result

if __name__ == "__main__":
    import argparse
    import hashlib
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out",type=Path,default=Path("runs/geometry/linear_metric_reconstruction.json"))
    args=parser.parse_args()
    result=run()
    result["implementation_sha256"]=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    args.out.parent.mkdir(parents=True,exist_ok=True)
    args.out.write_text(json.dumps(result,indent=2)+"\n")
    print(json.dumps(result,indent=2))
