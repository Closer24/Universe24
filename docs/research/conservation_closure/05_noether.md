# Carry-aware conservation and the missing spatial condition

This package proves one exact continuity identity for the unchanged Engine,
executes it on a genuine face-interaction tensor, and tests an inhomogeneous
negative on the **same eight-channel Bianchi-I tensor** selected by this round.
The face-interaction tensor is a separate arithmetic construction; its success
does not transfer to the sourced Bianchi tensor.

## 1. The conserved covector must include the remainder

For one retained triple define

\[
\pi=6(b-a)+r.
\]

From the actual fixed-six primitive,

\[
6(b_++a)=2u+r-r_+,\qquad a_+=b,
\]

so the exact identity is

\[
\boxed{\pi_+-\pi=2(u-6b).}
\]

No approximation, zero-remainder assumption, quotient callback, or extra
channel is used. Both histories and the carry have a definite algebraic role.
The audit checks the symbolic identity and 4,050 signed integer inputs covering
every legal remainder.

Let an integer polynomial interaction produce
`u_g=6*b_g+s_g*partial(Phi)/partial(b_g)`, with `s_g` equal to ±1. If a constant
shift vector `c` is an infinitesimal symmetry of the global potential, then

\[
\sum_{x,g}c_g\,\partial_{b_g(x)}\Phi=0
\quad\Longrightarrow\quad
\mathcal Q_c=\sum_{x,g}c_gs_g\pi_g(x)
\quad\text{is exactly conserved.}
\]

This is a direct complete-state algebraic proof. The `s_g*pi_g` are the
quantities paired with the symmetry generator, as a covector pairs with a
vector. This statement does not assert arbitrary coordinate covariance of
the integer quotient map, or identify these quantities with physical
gravitational energy-momentum.

On the **same primary eight-channel sourced trace**, the identity gives
`pi_volume=6*J-18*D+r_volume` and `Delta pi_volume=36*D`; every other arithmetic
charge has zero increment. All 648 channel/node/transition comparisons pass.
Thus the general identity also explains the retained volume-history balance,
while the physical constants `P,D,S` and quadratic source constraint are
separately identified invariants. Volume momentum is sourced, not conserved.

## 2. Actual local transport on the board

The separate two-channel law uses current node fields `phi,g` and the
translation-invariant interaction over positive face edges in all three axes:

\[
\Phi=-\sum_{e=(i,j)}(g_i+g_j)(\phi_j-\phi_i)^2.
\]

Here `g` is an algebraic stiffness variable, **not** the accepted spacetime
metric. Differentiating the same interaction supplies both responses:

\[
F_i^\phi=2\sum_{j\sim i}(g_i+g_j)(\phi_j-\phi_i),\qquad
F_i^g=-\sum_{j\sim i}(\phi_j-\phi_i)^2.
\]

The existing potential compiler generates `u=6b+F`. It is quadratic,
strictly one-face local, and uses **two channels / six retained integers per
node**, with no scheduler or workspace. Every response reads the same old
snapshot.

Let `B1` be the oriented node-edge incidence matrix, −1 at the tail and +1 at
the head. Define the algebraic oriented edge current

\[
J_e=4(g_i+g_j)(\phi_j-\phi_i).
\]

The independently evaluated actual transition satisfies

\[
\boxed{\pi^\phi_+-\pi^\phi=-B_1J.}
\]

Internal faces cancel in a region sum. Periodic boundaries therefore give
exact global conservation. Four actual Engine ticks on 27 nodes / 81 face
edges pass an independent scalar polynomial oracle, an independent edge
derivative, every microstep inverse and complete rewind. Node charges change
and edge currents are nonzero; this is actual spatial exchange, not a frozen
charge control. All six carry classes are present and carries change.

The complete global charge is **69 at every tick**. Omitting the carries gives
the initial value **6**, then **0, 6, 6, 0**. The actual maximum retained bits
are **7, 15, 32, 65** after those ticks. Thus exact conservation alone is not
a stability or efficient long-time theorem. Arithmetic clicks are counted in
the evidence, with no claim that those clicks measure proper time.

The same node values satisfy `B2.T*B1.T*phi=0`, because the exactly constructed
cubical incidence matrices obey `B1*B2=0`: the boundary of a boundary vanishes.
This explains why incidence operators are useful for exact structural
constraints. It does not supply the metric-dependent constitutive law or
Einstein's curvature/source equations. All incidence arrays and currents
are passive validation values, not hidden retained channels.

Deleting the response on `g` gives a legal reversible tensor which still
conserves the `phi` charge. The reciprocity check and the independently
predicted `g` response then fail. A conserved charge therefore does not
uniquely determine, or physically validate, the interaction.

## 3. Pointwise source constraints do not become spatial Einstein constraints

The selected native Bianchi source has

\[
Q=U^2-3DV-\tfrac32(P^2+S_1^2+S_2^2+S_3^2)=0,
\quad H_i=\frac{U}{3V}+\frac{S_i}{V},\quad \sum_iS_i=0.
\]

Consider initial data with spatially constant metric, `V=7/3,U=4,D=1,P=2`,
zero scalar gradient, comoving dust, and the smooth tracefree shear family

\[
(S_1,S_2,S_3)=
\frac{(x^2-1,\;-x(x+2),\;2x+1)}{x^2+x+1}.
\]

The denominator is everywhere positive. The shear norm is identically 2,
so **the Hamiltonian constraint is zero at every spatial point**. Initial
spatial curvature and matter momentum are zero. With `K^i_j=-H_i delta^i_j`,
the independent momentum constraint is

\[
\mathcal M_i=D_jK^j{}_i-D_iK-j_i
=\partial_i\left(\frac{2U}{3V}-\frac{S_i}{V}\right).
\]

At `x=0` the exact smooth residual is

\[
\boxed{\mathcal M_x=-3/7\ne0.}
\]

For an actual board control, prepare the shared eight-channel tensor with
shears `(-1,0,1)`, `(0,-1,1)`, `(1,-1,0)` on its three x-planes. These all have
norm 2. The unchanged Engine executes three ticks; **108 site/sample
Hamiltonian-invariant checks remain exactly zero**, scalar oracles and full
rewind pass, but the initial centered unit-grid momentum residual takes the
nonzero values **3/14 and −3/7**. The latter is explicitly a chosen diagnostic
stencil, not an accepted discrete ADM discretization. The smooth initial-data
counterexample above does not depend on that stencil.

The primary physical reader correctly rejects this nonhomogeneous seed.
No accepted Bianchi preparation has been silently enlarged. This negative
locates the missing work: a shared face-coupled source/geometry operator must
implement the spatial curvature and momentum constraints and preserve or
convergently control them on its actual complete state. Independently
conserved onsite charges cannot establish that result.

## 4. What the literature supplies

- Marsden, Patrick and Shkoller, *Multisymplectic Geometry, Variational
  Integrators, and Nonlinear PDEs*, §5, equation (5.7),
  [primary paper](https://arxiv.org/pdf/math/9807080): an invariant discrete
  action yields discrete momentum/boundary identities. Our carry identity is
  derived directly above; we do not assume their variational, symplectic or
  energy conclusions for the fixed-six map.
- Hirani, *Discrete Exterior Calculus* (2003), §3.6, definitions 3.6.1–3.6.5,
  [primary thesis](https://thesis.caltech.edu/1885/03/thesis_hirani.pdf):
  incidence/coboundary identities explain exact `d*d=0`. They do not specify
  the required metric or prove a continuum limit for this project.
- Gourgoulhon, *3+1 Formalism and Bases of Numerical Relativity* (2007),
  equations (10.5) and (10.7),
  [author's lecture notes](https://people-lux.obspm.fr/gourgoulhon/pdf/form3p1.pdf):
  the Hamiltonian residual is a scalar and the momentum residual is a
  separate one-form. They give the convention used in the spatial negative.

The cited sections were read. The executable project-specific identities,
counterexamples and Engine checks are derived in this package.

```sh
python -m validation.conservation_closure.noether_spatial
```

Fresh evidence: `runs/conservation_closure/noether_spatial.json`. Primary and
negative seed identities, both tensor identities, source hashes, the complete
carry-aware theorem and all test statuses are recorded there.
