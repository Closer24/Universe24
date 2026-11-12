# Constraint repair: exact defect and a sourced transport control

This follow-up does **not** close the general Einstein gate for the 44-channel
charged-scalar/frame proposal. It separates a diagnosed spatial truncation
error from a new exact restricted Einstein solution with positive moving
matter. Neither test changes the production Engine, the frame equations, the
acceptance tolerances or the retained-state contract.

Run:

```bash
python -m validation.geometry.team48.constraint_repair_spatial
python -m validation.geometry.team48.constraint_repair_ppwave
```

Fresh reports are written under `runs/team48/constraint_repair/` and contain
source hashes. The working-tree code belongs to the P3 proposal under #40.

## 1. The existing momentum-constraint defect is identified exactly

On the original periodic constrained slice, write

`B=I, Gamma=0, K=diag(0,k,k), Pi_phi=2, q=D(phi), k=phi+10`.

The independent directional derivative of every constraint agrees with the
following exact expression at all 125 nodes:

`M0_dot = -3 [D(k²)-2k Dk] - 1/2 [D(q²)-2q Dq]`.

It gives `(-21,-3,0,3,21)` on the five x positions. The initial derivatives of
H, the other momentum components, all torsion/gradient/curl constraints and
antisymmetric Ricci defects are zero. This identifies the failure as two
centered-difference product defects; it is not evidence that the continuum
stress tensor has the wrong sign or omits energy.

A fixed-domain test uses the same periodic C3 physical profile
`phi(x)=256 x^4(1-x)^4`, `Pi=2`, `k=phi+10`, `q=D_h(phi)` and
`rho_dust=k²-(4+q²)/2`. All arithmetic is exact Fraction validation.
Initial discrete H/M/gradient constraints vanish and dust is positive.

| L | max abs M0_dot | ratio from previous L |
|---:|---:|---:|
| 8 | 12.99147177 | — |
| 16 | 5.62184902 | 2.31089 |
| 32 | 1.83645420 | 3.06125 |
| 64 | 0.47481714 | 3.86771 |
| 128 | 0.11970438 | 3.96658 |
| 256 | 0.02998949 | 3.99154 |

Thus this tangent error has second-order spatial decay on a fixed physical
problem. The former fixed-dx result cannot alone establish nonconvergence.
This is **not** a fixed-time Engine trajectory or a proof of nonlinear
stability. Integer time refinement and all later constraint errors remain
separate obligations. Cancelling the displayed term by editing one equation
would need to preserve the gradient, torsion and conservation identities too;
no such unproved repair is inserted.

## 2. Five channels give an exact moving positive-energy Einstein control

Use units `8*pi*G=c=1` and the one metric

`g = diag(-1,1,1,1) + H (dt-dz)^2`,

`H = -rho(u)(x²+y²)/2 + p(u)(x²-y²) + 2 c(u)xy`, `u=t-z`.

The retained profiles `rho,p,c` carry null matter density and the two free
pp-wave polarizations. The other two retained fields are transverse coordinate
numerators X,Y. The source is positive null dust:

`T_mu_nu = rho * ell_mu * ell_nu`, `ell=(1,0,0,-1)`.

The Engine samples profiles F(z-t); in the displayed arbitrary-function
notation this is rho(u)=F(-u), and likewise for p,c. This reflection is fixed
and has no physical or arithmetic effect.

An independent symbolic metric/Christoffel/Ricci calculation, without calling
the existing frame RHS, verifies all 16 components `G_mu_nu=T_mu_nu`, all four
components of `nabla_mu T^(mu,nu)=0`, and a covariantly constant null flow
`k=(1,0,0,1)`. Consequently the four Einstein constraint and six evolution
projections vanish for this continuum family. Its determinant is exactly -1.
`R_txtx=rho/2-p` and `C_txtx=-p`, so the construction includes nonzero Ricci
and Weyl curvature. The geometry is not a vacuum chart with external labels.
The lapse and longitudinal shift are nontrivial when H is nonzero.

### Exact retained-state transport

For each profile the fixed tensor is simply

`u_profile = 3*(b_profile[z+1]+b_profile[z-1])`.

Prepare its previous slice as `a[z]=b[z+1]`. With unchanged Rule3,
`b_next[z]=b[z-1]` exactly: substitution gives
`ell=b[z+1]+b[z-1]`, with every remainder unchanged. This invariant proves the
right-moving branch for every number of steps and arbitrary initial profile,
without storing future samples or consulting an observer. The two coordinate
fields use `u=6b` with equal initial slices, so they stay fixed. All eight
monomials are linear and each uses one face neighbor at most. There are **five
channels / fifteen retained integers per node**, including coordinate fields;
no clock, history bank or discarded remainder is omitted.

The same tensor runs L=4,8,16,32 with `dt=dz=1/L` to physical time 1/4.
At every intermediate sample the profiles are exact samples of the same
translated physical profiles. Metric samples match their independent analytic
expressions exactly. On transverse interior points the literal nearest-face
Laplacian of the reconstructed H returns `-2 rho` exactly. Source density is
at least 1 and spatial `gzz` at least `22609/32768` in all tests. Complete-state
serialization/replay and rewind pass, including all remainder classes.
Retained bit maxima are 21,29,37,45; the channel count does not hide bit growth.
A separate fixed-L seed-quantization sweep bounds profile error by `1/Q` at
physical time 1/4. Quantization occurs only during preparation.

The wrong temporal-branch control (`a=b` for the transported profiles) remains
fully reversible and fails the exact parallel-null translation invariant.
This guards against inferring physical correctness from replay alone. An
additional transverse-localized density perturbation preserves the Engine
transport and rewind but breaks the literal transverse Einstein residual;
non-plane source data cannot silently inherit the ansatz theorem.

### Limits and integration boundary

- This is an exact **prepared pp-wave/null-dust family**, not general Einstein
  geometry, massive dust, charged scalar matter or arbitrary initial data.
- The metric is a proved passive cubic algebraic readout of these retained
  profiles and coordinates, with fixed preparation calibration. It does not
  repair the nonlinear 44-channel frame integrator.
- Matter is transported by real neighbor interactions. Its special parallel
  null direction is geodesic for this same metric, which explains why its
  reduced transport law does not acquire a generic feedback term.
- Transport is periodic in z. The x/y coordinate seams are not a global
  periodic geometry; only the declared interior transverse coordinate patch
  is tested as a spacetime. Seam nodes are not silently treated as valid.
- Spatial/time refinement is joint at `dt=dz`; independently changing these
  two scales is untested. Seed quantization is refined separately.
- No material clock, click-only apparatus, detector, Born/Bell result or
  generic causal metric-cone claim is added. This is a validation control,
  not another supported runtime or a reason to close #40.

## Literature checked and applicability

David L. Meier, *Constrained Transport Algorithms for Numerical Relativity. I.
Development of a Finite Difference Scheme* (2003),
<https://arxiv.org/abs/astro-ph/0312052>, motivates compatible derivatives from
Bianchi propagation, but explicitly leaves cubic-connection truncation errors
in general coordinates and requests stability/convergence experiments. It does
not prove the current nonlinear centered-difference scheme constraint exact.

C. Di Bartolo, R. Gambini, J. Pullin, *Consistent and mimetic discretizations in
general relativity* (2005), <https://arxiv.org/abs/gr-qc/0404052>, establishes a
linearized mimetic result. Its nonlinear consistency approach is not already a
fixed cubic integer tensor. The new pp-wave result above is instead verified
directly by its own complete symbolic Einstein calculation and Engine algebra;
it does not borrow a numerical convergence theorem from either paper.
