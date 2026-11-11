# Constraint physics audit for the 48-channel attempt

This isolated research result contains one positive exact sourced **linearized**
Einstein Engine sector and three limitations of the current nonlinear frame
leapfrog. It does not establish full nonlinear 48-channel Einstein evolution.
No production layer or default engine is changed.

Reproduce from the repository root:

```sh
python experiments/geometry/team48/constraints_audit.py
```

Evidence: `runs/team48/constraints/results.json`. The report hashes the Engine
and Frame48 source files against which it was generated. All calculations are
exact integer or symbolic operations. Positive and negative checks both pass.

## A small positive result with matter energy and momentum

Use a one-dimensional perturbation of Minkowski space, unit lapse, zero shift,
and Einstein coupling equal to one. Set

\[
h_{xx}=w,\quad h_{yy}=h_{zz}=v,\qquad
K_{xx}=l,\quad K_{yy}=K_{zz}=k,\qquad p=D_xv/2.
\]

Other metric and extrinsic-curvature perturbations vanish. A conserved null-beam
stress perturbation has

\[
j_x=S_{xx}=\rho,\qquad j_y=j_z=S_{yy}=S_{zz}=0,
\qquad \dot\rho=-D_x\rho.
\]

The first-order sourced linearized Einstein equations reduce to

\[
\begin{aligned}
\dot w&=-2l,&\dot v&=-2k,\\
\dot l&=-2D_xp-\rho,&\dot k&=-D_xp,\\
\dot p&=-D_xk,&\dot\rho&=-D_x\rho.
\end{aligned}
\]

The nontrivial constraints are

\[
H=-4D_xp-2\rho=0,\qquad
M_x=-2D_xk-\rho=0,\qquad p-D_xv/2=0.
\]

The integer mathematics agent's period-four sign lift places these six fields
in six gears, plus one shared clock. The clock obeys unchanged Rule3 with
`u=0` and has signs `1,1,-1,-1`. If its current `a=s_n`, `b=s_(n+1)`, encode a
linear field as `b_z=s_n*y_n` and use

\[
u_z=6\Delta t\,a_{clock}b_{clock} f(z).
\]

Its decoded update is exactly `y_next=y_previous+2*dt*f(y_current)`. Clock
factors are at the target node; every derivative factor is at one face
neighbor. All monomials have degree three, all old-`a` dependencies point from
the clock to the fields, and no runtime readout changes evolution.

At `dt=dx=1`, prepare a periodic profile `v=4*[0,1,0,-1,0]`, with
`p=k=D_x v/2`, `rho=-2*D_x p`, `l=w=0`. The preceding slice is the same profile
shifted one site forward. This selects the exact right-moving translation
branch of the centered leapfrog. Both initial slices satisfy every constraint.

Actual unchanged Engine results:

| Check | Result |
| --- | --- |
| Gears / monomials / maximum degree | 7 / 11 / 3 |
| Lattice | Periodic `5^3`, fields vary only in x |
| Steps checked | 20 |
| Hamiltonian, momentum, gradient residuals | Exactly zero at every step |
| Matter energy density perturbation | Integers from -3 to 3; total zero |
| Complete `(a,b,r)` rewind | Exact |
| Freeze density evolution, keep its metric source | After one step: `max|H|=12`, `max|M|=6` |

This is a useful regression: matter conservation and metric constraint
propagation are coupled and both matter. It is not positive matter on a flat
periodic universe. On a periodic linearized flat slice, the summed Hamiltonian
constraint forces the mean density perturbation to vanish. The signed profile
is stated explicitly. Small perturbative physical amplitudes require an
appropriately justified calibration; the raw integer fixture is an algebraic
linearized solution, not a nonlinear spacetime approximation claim.

## General sourced linearized constraint identity

Let `D_i` be any commuting discrete derivatives, including centered periodic
face differences. With linearized Ricci tensor

\[
R_{ij}^{L}=\tfrac12(D_kD_ih_{jk}+D_kD_jh_{ik}
                 -D_kD_kh_{ij}-D_iD_jh_{kk}),
\]

the evolution equations are

\[
\dot h_{ij}=-2K_{ij},\qquad
\dot K_{ij}=R^L_{ij}-S_{ij}+\tfrac12\delta_{ij}(S-\rho).
\]

The script proves symbolically, for arbitrary field symbols,

\[
H=R^L-2\rho,\quad M_i=D_jK_{ij}-D_iK_{jj}-j_i,
\qquad \dot H=-2D_iM_i,\quad \dot M_i=-\tfrac12D_iH,
\]

provided `rho_dot=-D_i*j_i` and `j_i_dot=-D_j*S_ij`. The discrete contracted
linear Bianchi identity is exact because the derivatives commute. Therefore
unrounded leapfrog preserves these *linear* constraints when both initial
slices satisfy them. Freezing density adds the nonzero defect `-2*D_i*j_i`.

A general first-order, fixed-direction null-beam version would use metric 6,
extrinsic curvature 6, half-gradient metric 18, density 1, shared clock 1:
**32 gears** before additional controls. This is a field budget, not a compiled
general stable model. Its derivative compatibility conditions and initial
constraints must also hold. Channel compression alone does not supply stable
multi-dimensional integer refinement.

This agrees with the scope distinction in Di Bartolo, Gambini and Pullin:
their mimetic Einstein result is linearized; their nonlinear consistency
strategy determines multipliers as part of the discrete solution [1].

## Why ordinary nonlinear continuum identities do not transfer directly

For centered `D`, already `f=g=x^2` gives

\[
D(fg)-fDg-gDf=4x\,dx^2.
\]

At `x=dx=1` the defect is exactly four. The script also verifies the exact
alternative

\[
D(fg)=\bar f Dg+\bar g Df,\qquad
\bar f=(f_++f_-)/2.
\]

There is a sharper finite-node statement: on the ordinary pointwise algebra
of a finite set, every derivation is zero. For each point idempotent `e`, a
Leibniz derivative must satisfy `D(e)=D(e^2)=2eD(e)`; every component is zero.
The point idempotents span the algebra. Thus a nonzero ordinary difference
cannot satisfy the continuum product rule for all fields.

This rules out borrowing the continuum nonlinear Bianchi cancellations
without a discrete derivation. It does **not** rule out a flux formulation,
shifted products, a discrete action, or modified discrete constraints.
Unexpanded flux differences can meet single-face support. Establishing all
the required metric, connection and matter identities remains the work.

## Four constraint variables are useful, but naive damping fails

The Z4 continuum extension introduces one four-vector. Einstein solutions are
the zero-Z sector, with compatible initial constraints. Suitable gauges give
hyperbolic formulations [2]. Constraint damping has a genuine continuum
derivation, including a limitation for constant modes [3].

Nevertheless, under the current leapfrog, even `z_dot=-kappa*z` becomes

\[
z_{n+1}=z_{n-1}-2h\kappa z_n,\qquad
r_\pm=-h\kappa\pm\sqrt{1+h^2\kappa^2}.
\]

For **every** positive `h*kappa`, one root has modulus greater than one.
Adding a continuum damping term without changing its temporal realization
therefore creates a growing computational mode. In the actual two-gear
Rule3 lift with `2*h*kappa=1`, unit initial fields reach magnitude 610 after
16 steps while complete rewind remains exact. Reversibility did not imply
physical damping.

The single-bank frame count would allow 24 geometric fields + four Z4 fields
+ one clock = 29 gears before matter. With eleven independently justified
matter fields that would be 40. This arithmetic is **not** a proof that the
nonlinear Z4 equations compile with the required degree, gauge, support,
reduction constraints, stable timestep or integer calibration. Four dynamic
multiplier names do not solve constraints; an implicit constraint solve is a
different operation from adding four unconstrained ordinary differential
equations. The variational team's audit of [1] confirms this distinction.

## Limited nonlinear integer refinement obstruction

Consider only a direct field encoding `K=s*k` with integer `k`, positive fixed
physical scale `s`, and the same leapfrog for `K_dot=K^2`. Its integer update is

\[
k_{n+1}=k_{n-1}+m k_n^2,\qquad m=2hs.
\]

If this nonzero coefficient must itself be an integer, then for nonzero `k`

\[
|hK|=|mk|/2\geq\tfrac12.
\]

Consequently field rescaling alone cannot produce `h*|K| -> 0` for nonzero
curvature in this direct representation. This is a narrow obstruction, not a
theorem against all 48-channel encodings. Extra divisibility arithmetic,
proved nonlinear readouts, retiming, prepared sectors or a different update
could evade its assumptions. They require an actual construction and retained
state accounting. Using smaller real timesteps in a floating reference does
not evade this integer encoding bound.

## Actionable result

Keep the seven-gear sourced linearized Engine sector as a positive control.
Require any proposed nonlinear constraint fix to pass its conservation
negative control, the existing nonlinear Frame48 initial-data checks, and a
refinement family in physical time. The freed channel budget is real; it
should be spent only after deriving a compatible constraint propagation law
and a stable, refinable temporal realization. A discrete action or compatible
flux calculus is a concrete next derivation; simply naming four Z4 gears or
adding damping is insufficient.

## Primary references

1. C. Di Bartolo, R. Gambini, J. Pullin, *Consistent and mimetic
   discretizations in general relativity*, J. Math. Phys. 46, 032501 (2005).
   https://arxiv.org/abs/gr-qc/0404052
2. C. Bona, T. Ledvinka, C. Palenzuela, M. Zacek, *General-covariant evolution
   formalism for Numerical Relativity*, Phys. Rev. D 67, 104005 (2003).
   https://arxiv.org/abs/gr-qc/0302083
3. C. Gundlach, J. M. Martin-Garcia, G. Calabrese, I. Hinder, *Constraint
   damping in the Z4 formulation and harmonic gauge*, Class. Quantum Grav.
   22, 3767–3774 (2005). https://arxiv.org/abs/gr-qc/0504114
