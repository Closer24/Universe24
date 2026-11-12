# Same-state anisotropic metric and Einstein tensor

This audit independently derives the curvature of the **same eight-channel
native Bianchi-I candidate** defined in `common.py`. It extends a homogeneous
massless-scalar/dust subcase to nonzero diagonal shear. No spatial gradient,
new runtime, transported material detector or general Einstein solution is
claimed. The exact Bianchi solution is established physics; the new object
being checked here is its retained integer realization and common readout.

## Conventions and the conserved variables

Use signature (-,+,+,+), synchronous lapse one, zero shift, and
`c=8*pi*G=1`. Let

\[
 ds^2=-dt^2+\sum_{i=1}^3 a_i(t)^2(dx^i)^2,\qquad
 V=a_1a_2a_3,\quad U=\dot V.
\]

The scalar has no potential. Its conserved homogeneous momentum is
`P=V*phi_dot`; the comoving dust mass is `D=V*rho_dust`. Introduce two
independent trace-free shear charges, with `S3=-S1-S2`, and set

\[
 H_i={\dot a_i\over a_i}={U/3+S_i\over V},\qquad
 \dot U={3D\over2},\quad \dot P=\dot D=\dot S_i=0.
\]

These `S_i` are **not covector components**. They are the diagonal entries of
`V*sigma^i_j`. The mixed shear is `sigma^i_j=diag(S_i/V)`, whereas its lowered
form is `sigma_ij=diag(a_i^2*S_i/V)`. Consequently,

\[
 {d\sigma_{ii}\over dt}=(2H_i-U/V)\sigma_{ii},\qquad
 {d\sigma^i{}_i\over dt}=-(U/V)\sigma^i{}_i.
\]

Dropping the metric factors confuses a coordinate derivative with the
covariant derivative. Under a constant determinant-one coordinate change
`x'=L*x`, the spatial metric becomes `L^-T*g*L^-1` and the mixed shear becomes
`L*sigma*L^-1`. The executable audit checks both `tr(sigma^2)` and the separate
covector contraction `p^T*g^-1*p` under an explicit nonsingular shear of the
coordinate basis. For a general determinant-changing transformation, `V` is
a spatial volume density, so `V*sigma^i_j` is a mixed tensor density. The
constant-basis check does not add spatial degrees of freedom to this model.

## Metric from retained anchors

Put `K_flow=U^2-3*D*V`, which the native map conserves even off the physical
constraint, and let `q=sqrt(K_flow)`. The common reader uses the actually
retained reference velocity `Uref` and scalar offset `phi_ref`:

\[
 I={1\over q}\log\left({(U-q)(U_{\rm ref}+q)\over
                              (U+q)(U_{\rm ref}-q)}\right),\qquad
 a_i=V^{1/3}e^{S_i I},\qquad \phi=\phi_{\rm ref}+PI.
\]

The proof differentiates this expression and obtains `I_dot=1/V`, then
`a_i_dot/a_i=H_i` and `phi_dot=P/V`. Numerical evaluation uses stable
`log1p`, but no root, logarithm or exponential participates in Engine
evolution. Neither an external tick index nor a reference trajectory supplies
the metric. The retained proper-time channel is independent of this readout.

The source constraint is

\[
 Q=U^2-3DV-{3\over2}\left(P^2+\sum_iS_i^2\right)=0.
\]

On `Q=0`, `K_flow=3*(P^2+sum(S_i^2))/2`. Using `K_flow`, rather than silently
substituting this desired source value on an off-constraint input, is
essential: otherwise the decoder would change the field equations while
appearing to repair an invariant.

## Independent four-dimensional curvature calculation

`metric_curvature()` starts with symbolic `diag(-1,a1^2,a2^2,a3^2)` and its
inverse. It constructs all 64 Christoffel entries, all 256 Riemann entries,
all 16 Ricci entries, the scalar curvature and the Einstein tensor. Time
derivatives use independent symbols `H_i` and `Hdot_i`; all spatial
derivatives vanish by the declared symmetry. There are nine nonzero
Christoffel and 24 nonzero Riemann entries before imposing equations.

Only after this metric calculation does the audit substitute

\[
 \dot H_i={D\over2V}-{U(U/3+S_i)\over V^2},\quad
 \rho={P^2\over2V^2}+{D\over V},\quad
 p={P^2\over2V^2}.
\]

The resulting sixteen component identities are

\[
 \boxed{G_{\mu\nu}-T_{\mu\nu}
 ={Q\over3V^2}\,\operatorname{diag}(1,a_1^2,a_2^2,a_3^2).}
\]

Thus all off-diagonal equations vanish identically and all diagonal equations
vanish on the same retained constraint. Independent exact derivatives also
verify scalar wave evolution, dust continuity and
`rho_dot+(U/V)*(rho+p)=0`. This is stronger than checking only a Friedmann
scalar or simply declaring a stress tensor equal to the curvature.

The default seed is `V=7/3,U=4,D=1,P=2,S=(1,-1,0)`. The normalized electric
Weyl eigenvalues are `(9,-15,6)/49`; its magnetic part vanishes. Therefore

\[
 C_{abcd}C^{abcd}=8E_{ij}E^{ij}={2736\over2401}>0.
\]

This supplies a genuine anisotropic tidal-curvature witness, rather than a
constant rescaling of FLRW coordinates. Setting all shear charges to zero
recovers zero Weyl curvature and the isotropic Einstein equations.

## Future metric domain

For the declared branch `V0>0,D>0,K_flow>0,U0>sqrt(K_flow)`,

\[
 V(t)=V_0+U_0t+{3D\over4}t^2>0,\qquad U(t)=U_0+{3D\over2}t.
\]

For all future finite proper times,

\[
 0\le I(t)<{1\over\sqrt K}\log{U_0+\sqrt K\over U_0-\sqrt K}.
\]

Every `a_i` is positive and finite. Total volume expansion does not imply
that every axis expands for arbitrary allowed shear. For the default seed,
`U0/3+min(S_i)=1/3>0`, so all three directional rates are positive and remain
positive. The theorem follows from the exact polynomial flow sampled by the
native map; it is not a projection or an evolving domain veto.

## Actual Engine evidence and negative controls

The audit executes the shared law at `N=24,48,96`, reaching proper time
`1/8` in `3,6,12` ticks. Across **24 actual complete states**, it checks exact
rational curvature/source residuals and conserved `P,D,S`, metric positivity,
`a1*a2*a3=V` to high precision, every immediate inverse, and full rewind.
Each receipt includes its tensor and complete seed hash. The metric and
scalar diagnostics all come from these very states.

Three controls preserve the distinction between arithmetic validity,
constraint validity and physical validity:

1. Erase shear from the metric while leaving the correct `Q=0` source and
   retained charges: initially `G00-rho=9/49`, so Einstein fails.
2. Freeze the metric while keeping the same `Q=0` source: initially
   `G00-rho=-39/49`, again a failure.
3. Change the **actual retained scalar charge** from `P=2` to `P=1` without
   changing the geometry. Three actual native states retain `Q=9/2`;
   the initial `G00-rho=27/98`. The passive metric reader leaves this defect
   visible, and the erroneous physical run still rewinds exactly.

The first two are intentionally wrong metric interpretations, not new
accepted tensors. The third is an executed source intervention. Exact
conservation alone cannot select the correct metric, identify an operational
clock, or prove uniqueness of the underlying law.

```sh
python -m validation.conservation_closure.tensor_metric
```

Fresh evidence: `runs/conservation_closure/tensor_metric.json`. This package
does not modify Engine, the system decoder or the production acceptance gate.

## Primary readings inspected

- Cáceres, Castañeda and Tejeiro, *Shear Dynamics in Bianchi I Cosmology*,
  [arXiv:1003.3491](https://arxiv.org/pdf/1003.3491), section 2.1,
  equations (2.3)–(2.17): diagonal metric integration and the distinction
  between lowered shear components and covariant differentiation. Equations
  (2.19)–(2.21) discuss the dust volume/shear solution. These motivate the
  index checks; all component identities above are independently derived.
- Capozziello, Marmo, Rubano and Scudellaro, *Noether symmetries in Bianchi
  universes*, [arXiv:gr-qc/9606050](https://arxiv.org/pdf/gr-qc/9606050),
  section 4 equation (50) and the dust discussion in section 6: cyclic
  anisotropy/scalar variables supply conserved charges, while dust changes
  the energy constraint. This does not establish the discrete native
  embedding; that part is proved and executed in this project.
