# Reciprocal sources and exact geometric constraints

A reciprocal matter response can be a legal Rule3 tensor without being an
Einstein source. The missing condition is an invariant, sourced constraint
sector. Three exact obstructions below locate the gap: the direct probe source
does not preserve generic TT constraints; an ordinary pointwise scalar stress
is not conserved under central lattice derivatives; and positive total matter
energy cannot source a periodic linearized Einstein metric about Minkowski.
None is a no-go theorem for every encoded Rule3 model of gravity.

The passive integer audit is reproducible from the repository root:

```sh
python experiments/geometry/exact_constraint_audit.py
```

It writes `runs/constraint-geometry/exact_constraint_audit.json`. The script
uses Python integers in object arrays, with no floating arithmetic or state
update. It checks the algebra below; it does not execute a gravity model.
The underlying identities are proved here rather than inferred from those
finite checks. No default law or engine changes are made.

In every Rule3 recurrence below, `D` denotes the fixed constant six.

## 1. What a discrete Bianchi identity requires

Let `d_mu` be mutually commuting differences, let
`eta=diag(-1,1,1,1)`, and use eta to raise indices. Define

```
2 R_mu_nu = d_sigma d_mu h^sigma_nu
          + d_sigma d_nu h^sigma_mu
          - box h_mu_nu - d_mu d_nu h,
G_mu_nu = R_mu_nu - (1/2) eta_mu_nu R.
```

Commuting the differences and collecting terms gives, identically,

```
d^mu G_mu_nu = 0.
```

This linear identity needs no product rule. Consequently an exact equation
`G_mu_nu = kappa T_mu_nu`, with nonzero constant kappa, requires
`d^mu T_mu_nu = 0` for the same differences. A symmetric Hessian of a
potential is a reciprocity identity in field space, not this spacetime
divergence identity.

The audit uses unnormalised central differences
`d_mu=S_plus_mu-S_minus_mu`. It evaluates integer numerators `R2=2R` and
`G4=4G` on a generic symmetric periodic metric. All four Bianchi residuals
are exactly zero. Restoring the common factor of two in every derivative
does not change any zero/nonzero conclusion.

Harmonic gauge does not eliminate the requirement. If
`C_nu=d^mu hbar_mu_nu`, the reduced equations
`box hbar_mu_nu=-2 kappa T_mu_nu` imply
`box C_nu=-2 kappa d^mu T_mu_nu`. A nonconserved source drives a gauge
constraint even when its initial value and appropriate time data vanish.

## 2. The reciprocal phase-probe source has a specific TT obstruction

Consider the legal rank-four node/edge potential

```
Phi_int = kappa sum_(undirected x/y edges xy)
                 sigma_axis (F_x+F_y) (chi_y-chi_x)^2,
F = c (E00-E11) + s (B01+B10),
sigma_x=1, sigma_y=-1.
```

Every expanded monomial lies on a single physical edge, and its derivatives
have input degree three. Define

```
H_x = sum_(y=x+-ei, i=x/y) sigma_i (chi_y-chi_x)^2.
```

The metric and phase sources are

```
u_E00 =  kappa c H,     u_E11 = -kappa c H,
u_B01 =  kappa s H,     u_B10 =  kappa s H,
u_c   =  kappa (E00-E11) H,
u_s   =  kappa (B01+B10) H.
```

These sources are tracefree/symmetric before division, but generic `cH` and
`sH` have transverse gradients. For example at `c=1,s=0`, the electric source
is `diag(H,-H,0)` and its divergence is
`(d_x H,-d_y H,0)`. A scalar pulse at one node of an L=5 periodic board gives
exact nonzero maximum residuals `(1,1,0)`. It leaves the vacuum TT sector on
the first nonzero quotient. This failure persists in a choice where every
quotient is exact, so it is not merely a rounding problem.

For general coefficients, the signed algebraic relations also require an
arithmetic proof. Independent floor divisions need not preserve `E11=-E00`
or `B10=B01`. Complementary/equal remainder preparations can help with
specific signed maps. A simpler exact case is to choose every input as
`u=(D/2)K` with an integer polynomial K: each quotient is then K and every
remainder stays fixed.

There is a nonempty restricted repair of raw TT preservation. On an even
periodic board prepare

```
chi(x,y,z)=(-1)^x psi(z),
E,B,c,s depending on z alone, with E and B planar TT tensors.
```

Then `H=8 psi(z)^2`. Scalar nearest-neighbour inputs with z-dependent
coefficients retain the checkerboard factor, while the displayed metric and
phase sources remain planar TT. The curl block also preserves that shape.
If all inputs are in the exact-quotient class, the complete second-order
map and its inverse preserve this algebraic sector whenever both retained
arrays are prepared in it. This follows directly from closure under the
polynomial inputs and the inverse `a_old=K(a_new)-b_new`.

An alternative retains nonconstant remainders. If
`divmod(2u+r,D)=(ell,r_next)`, then exactly

```
divmod(-2u+D-1-r,D)=(-ell,D-1-r_next).
```

Thus negative field pairs retain their signs when their remainders are
complementary, and equal field pairs do so with equal remainders. Applying
this to the planar metric pairs and the two transverse checkerboard signs
extends the invariant-sector proof to the matching carrying preparation.
The separate [reciprocal candidate runner](../experiments/geometry/reciprocal_metric_candidate.py)
checks this at divisor six, kappa=1 for five Engine updates, including the independent
polynomial-input oracle, exact divmod ledger, one-step inverse and full
rewind. Its raw TT residuals stay zero, while the free phase/metric-shift
identities fail at update one and counters exceed 300 bits by update five.
Those finite observations illustrate the invariant algebra and its lack of
a demonstrated amplitude bound; they are not an all-time growth theorem.

This repair supplies genuine nonzero reciprocal forces and invariant raw
TT constraints; it supplies no bound or invariant metric signature. The
phase sources change the free phase oscillators and invalidate the previous
identity `F_t=S^t H_0`. In addition, a purely TT spacetime perturbation has
`G00=G0i=0`, whereas an ordinary excited scalar has positive energy density.
Such a restricted source is therefore not a complete physical scalar stress
or a sourced Einstein solution. Preparing chi to depend on z alone instead
makes the original transverse link interaction vanish entirely.

## 3. Why the continuum scalar stress cannot simply be copied

For central differences let
`A_mu=(S_plus_mu+S_minus_mu)/2`. The exact product identity is

```
d_mu(f g) = (d_mu f)(A_mu g) + (A_mu f)(d_mu g),
```

not the ordinary Leibniz rule. Replacing each continuum derivative in

```
T_mu_nu = (d_mu chi)(d_nu chi)
        - (1/2) eta_mu_nu [(d chi)^2 + m^2 chi^2]
```

therefore does not reproduce the continuum on-shell conservation proof.
This is an actual failure, rather than only a missing proof. On L=5 set

```
chi(t,x,y,z)=f(t+x)+g(t+y),
f=(0,1,-2,3,-1), g=(2,-1,0,1,-2),
```

with profile arguments modulo five. Each term is lattice-null, hence
`box chi=0` exactly. For the displayed massless stress the integer numerator
`T2=2T` nevertheless has divergence peaks `(40,40,40,0)`. Its nonnegative
`T2_00` sums to 1800 on every time slice. Global energy constancy does not
imply the required local four-divergence identity.

There is also a short algebraic obstruction to repairing this merely by
choosing a better derivative while retaining the ordinary product. On a
finite board let e_x be the pointwise idempotent at node x. Any derivation L
would obey

```
L(e_x) = L(e_x^2) = 2 e_x L(e_x).
```

At x this forces `L(e_x)=0`; away from x it forces the same. The e_x form a
basis, so L=0. Thus no nonzero linear finite-lattice derivative can obey
ordinary Leibniz on every pointwise field. This statement does not prohibit
staggered bond currents, shifted products, discrete differential complexes,
or specially restricted fields. Any such repair must define its actual
stress, divergence and conservation law, including the reciprocal coupling
and carry terms. Naming local flux registers does not prove their derivative
or constitutive relations are invariant.

## 4. Periodicity excludes positive mean sources in the flat linear target

For the same linearized Einstein operator,

```
2 G00 = sum_ij d_i d_j h_ij - sum_i d_i d_i sum_j h_jj.
```

Every periodic spatial difference has zero spatial sum. Therefore

```
sum_space G00 = 0
```

at each time for every h, independently of gauge and of the temporal
differences. Thus exact periodic `G00=kappa rho` requires `sum rho=0`.
When `rho>=0` pointwise, it follows that `rho=0` pointwise. A nontrivial
positive-energy scalar cannot be the total source of this target. The
crossing-wave audit provides one explicit positive-energy example, but the
obstruction is universal within the stated flat linear periodic target.

This does not forbid positive-energy matter on a nonlinear cosmological
torus. In the continuum Hamiltonian constraint, homogeneous extrinsic
curvature `Kij=-H gammaij` contributes
`K^2-Kij K^ij=6H^2`. For a spatially flat homogeneous background with
Lambda=0, `6H^2=16 pi G rho` can balance the mean density. A dynamic
homogeneous background is therefore a legitimate target change, still
requiring its own integer invariant encoding. Nonperiodic boundary flux is
another target change. Replacing rho by `rho-mean(rho)` would describe a
density contrast after a background has been specified; it is not a proof
that total positive matter gravitates. A runtime mean subtraction would
also violate the stated local fixed-law requirements.

## 5. What the fixed scalar arithmetic permits

For an allowed integer polynomial K, choose `u=3K`. With the fixed divisor
six, every legal remainder obeys

```
divmod(2u+r,6)=(K,r),
a'=b, b'=K-a.
```

Thus exact polynomial sectors with fixed remainders, including the curl and
retiming examples, need no adjustable normalization parameter. A desired
fractional direct coefficient is not automatically an admissible tensor entry.
For example, the ordinary scalar stencil with long-wave speed one half
would require `w=6/8=3/4`; that one-register stencil is unavailable with integer
coefficients. An alternative multi-register encoding needs its own proof.

The fixed divisor does not solve the Bianchi identity, the torus mean-source
condition, stability or constraint propagation. Generic inputs still produce
carries through `ell=floor((2u+r)/6)`. They may be omitted from an analysis
only where divisibility or an exact retained-ledger identity justifies it.

## 6. Precise next construction required

An admissible sourced target must specify a reversible geometric map and
its physical matter source together. It must propagate the actual sourced
constraints, account for the periodic mean/background, and preserve the
chosen metric-signature sector. It then needs a fixed local degree-three
Rule3 realization, possibly over a declared finite macrostep, with the
arithmetic registers included in the encoding. Neither a runtime projection
nor the formal first-order involution embedding supplies a missing
constraint-preserving target map.

The result here is a precise obstruction/minimal-repair analysis, with an
exact nonzero raw-TT reciprocal subsector. A universal reciprocal Einstein
matter-metric sector remains unconstructed.

## Primary sources and scope of their use

- S. Deser, *Self-Interaction and Gauge Invariance*, Gen. Rel. Grav. 1
  (1970), [author's paper](https://arxiv.org/abs/gr-qc/0411023). This establishes
  the continuum consistency role of conserved sources and nonlinear
  self-interaction; it is not a lattice compilation theorem.
- M. Kato, M. Sakamoto and H. So, *Taming the Leibniz Rule on the Lattice*,
  JHEP 05 (2008) 057, [paper](https://arxiv.org/abs/0803.3121). Its locality,
  translation and product-rule analysis is relevant context. The finite
  pointwise-algebra proof above is self-contained and uses narrower premises.
- B. Bahr and B. Dittrich, *Breaking and restoring of diffeomorphism symmetry
  in discrete gravity*, [paper](https://arxiv.org/abs/0909.5688). This explains
  why discretization need not preserve continuum gauge structure; it does
  not rule out all possible discrete constructions.
- Y. Guo, J. Hu and T. Lin, *Discretizing linearized Einstein-Bianchi system
  by symmetric and traceless tensors*, [paper](https://arxiv.org/abs/2508.04560).
  Its conformal-Hessian-complex construction illustrates that compatible
  tensor constraints require their own discretization. It is a real-valued
  finite-element vacuum construction, not a ready-made Rule3 matter law.
