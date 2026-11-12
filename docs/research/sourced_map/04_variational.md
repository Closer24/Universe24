# 4. Massive matter: exact structure and rejected variational alternatives

Baseline `f4f64e062f07b3ca119eccf655df746be206908b` (PR #56).
Reproduce: `python -m validation.sourced_map.variational`.
Evidence: `runs/sourced-map/variational.json`.

This lane independently derives the massive extension of the volume variables
and tests three numerical constructions. It does not duplicate the central
massless Engine experiment or supply a massive native implementation.

## The physical equations that a massive extension must implement

The actual homogeneous proper-time force in
`validation/completion/constraint_closure.py` is

\[
\dot B=Bk,\quad
\dot k=3k^2-\tfrac12(\mu\phi^2+d^2),\quad
\dot p=3kp-\mu\phi,\quad
\dot\phi=p,\quad
\dot d=\tfrac32kd,
\]

with `mu=mass_squared` and Einstein constraint
`C=6k²-p²-mu phi²-2d²=0`. On the physical domain `B>0`, define

\[
V=B^{-3},\quad U=-3kV,\quad P=pV,\quad D=d^2V.
\]

The script differentiates these expressions against the actual source vector
field and proves, without invoking C=0,

\[
\dot V=U,\quad
\dot U=\tfrac32(D+\mu\phi^2V),\quad
\dot P=-\mu\phi V,\quad
\dot\phi=P/V,\quad\dot D=0.
\]

The exact first integral is

\[
Q=U^2-\tfrac32P^2-\tfrac32\mu\phi^2V^2-3DV
=\tfrac32V^2C,\qquad \dot Q=0.
\]

For mu=0, P and D are constants and U has constant acceleration. For mu>0,
the comoving scalar momentum changes and the volume acceleration depends on
the evolving scalar potential. Consequently the massless affine volume map
cannot be reused with a mass term merely added to its decoder. The distinction
is physical, not just an integer encoding inconvenience.

## A useful quadratic formulation, with its physical clock made explicit

Let `X=phi V`. The invariant becomes the quadratic form

\[
Q=U^2-\tfrac32P^2-\tfrac32\mu X^2-3DV.
\]

In proper time, `Udot=3D/2+3mu X²/(2V)` and
`Xdot=P+XU/V`, so the force is rational. Choosing a new parameter s with
`d tau/ds=V` gives the polynomial system

\[
V_s=VU,\quad U_s=\tfrac32(DV+\mu X^2),\quad
P_s=-\mu XV,\quad X_s=PV+XU,\quad D_s=0,\quad\tau_s=V.
\]

Every right-hand side is degree at most two and Q remains exactly invariant.
This is a constructive massive-source specification for a future compiler,
not a solved update. It requires a positive-volume domain and an accumulated
proper-time variable if that time is used dynamically; s cannot silently be
reported as proper time. A fixed s endpoint is not a fixed physical endpoint.

## Kahan: reversible rational maps that fail the required constraint

For the actual quadratic force F, Kahan's map is

\[
z'=z+h(I-\tfrac h2F'(z))^{-1}F(z).
\]

It is linearly implicit and birational; its inverse is the negative-step map
where the required matrices are nonsingular. The literature proves particular
modified invariants for particular classes. That is not a theorem that this
Einstein zero set is preserved.

The audit derives exact symbolic failures, including at the constrained
massless sourced seed `(k,p,phi,d)=(-1,2,0,1)`:

\[
C(z')=
\frac{-144h^3(7h+4)}{(3h+2)^2(21h^2+30h+8)^2}\ne0.
\]

The massive seed `(-1,0,2,1)`, mu=1, also has a nonzero exact defect.
Both maps invert exactly at h=1/16. Applying Kahan to the quadratic lapse-time
system above likewise fails Q=0 at `(V,U,P,X,D)=(1,3,0,2,1)`. Full rational
defect expressions are retained in the evidence. These failures rule out these
specific unchanged Kahan maps; they are not general impossibility results.

## Implicit midpoint: an exact invariant, but not a rational native update

Because Q is quadratic, its midpoint identity is exact:

\[
Q(z')-Q(z)=\nabla Q((z+z')/2)\cdot(z'-z).
\]

Thus a solution of implicit midpoint for the lapse-time vector field preserves
Q exactly. It is symmetric on a consistently selected locally unique branch.
The audit checks the polynomial identity and its conservation premise.

The missing solve is substantive. At mu=1, the exact constrained seed
`(V,U,P,X,D)=(1,3,0,2,1)` and lapse step 1/16, eliminate the midpoint U,P,X
from the equations. The midpoint volume w must satisfy

\[
(1856w-2048-3w^2)(w^3+1024)^2-12582912w^3=0.
\]

The script verifies this elimination, proves the polynomial has degree eight
and is irreducible over the rationals, and counts exactly one root in
`1<w<9/8`. All cleared denominators are positive on that interval. A 65-digit
numerical cross-check verifies the corresponding invariant, but the exact
conservation proof is the midpoint identity above.

Every root is irrational, so this particular midpoint step cannot be represented
exactly by rational readouts of finite integer registers at that rational seed.
This is a scoped representation obstruction, not a no-go theorem for alternative
maps or algebraic readouts. A numerical root solver, discarded root choice, or
unrecorded projection cannot be inserted into the fixed tensor. An algebraic
encoding would require its own domain, branch and complete-state proof.

## Symmetric canonical splitting: good proper-time refinement, nonzero constraint

On C=0 the same physical solution follows the canonical Hamiltonian

\[
\mathcal H=-\tfrac34V\pi^2+\frac{P^2}{2V}
+\tfrac12\mu\phi^2V+D,\qquad
\pi=2k=-\frac{2U}{3V},\qquad Q=-3V\mathcal H.
\]

Off the constraint surface, its U equation differs from the original reduced
force by `Q/(2V)`. The audit therefore labels the canonical equivalence as
on-constraint; it does not exchange two distinct off-constraint equations.

The gravity, scalar-kinetic and mass-potential pieces each have explicit exact
rational subflows (mu=1 here):

| Piece | Nontrivial update over h |
| --- | --- |
| Gravity | `a=1-3h*pi/4`, `V'=V a²`, `pi'=pi/a` |
| Scalar kinetic | `pi'=pi+h P²/(2V²)`, `phi'=phi+hP/V` |
| Mass potential | `pi'=pi-h phi²/2`, `P'=P-h phi V` |

Compose them as `G(h/2) K(h/2) W(h) K(h/2) G(h/2)`. It is symmetric and
has an exact negative-step inverse on a chart with V>0 and nonzero gravity
factors. But symplectic subflows need not preserve the full Hamiltonian.
At the exact constrained strong massive seed `(V,pi,phi,P)=(1,-2,2,0)`, D=1,
the full composition has

\[
\mathcal H_{after}=-\tfrac34h^3+O(h^4)\ne0.
\]

The exact h=1/16 rational defect and inverse are saved. A separate 60-digit
proper-time comparison uses the independently written volume equations and
RK4 references with 2048/4096 steps. At fixed proper time 1/8:

| Split steps | Maximum field error | Absolute Hamiltonian defect |
| ---: | ---: | ---: |
| 2 | 5.73835052e-4 | 4.61462362e-4 |
| 4 | 1.43621578e-4 | 1.15164507e-4 |
| 8 | 3.59155806e-5 | 2.87786009e-5 |
| 16 | 8.97953193e-6 | 7.19386803e-6 |

Observed orders approach two. These are reference-map results, with no Engine
execution claimed. They show why useful convergence and exact inversion still
do not satisfy the requested exact constraint-preservation gate.

## Handoff to the selected construction

The central massless map has a special exact affine structure. This review
supports keeping that result narrow and concrete. For a massive successor,
the new quadratic lapse-time system and Q provide an explicit physical target.
Its compiler still needs a positive-volume/physical-time certificate, an
exact invariant-preserving finite map, and the complete Rule3 history embedding.
None of the tested Kahan or symmetric-split alternatives closes that gate;
midpoint supplies the invariant but not an allowed exact native update.

No massive law, runtime solver or new supported model is added here. Channel
count <=48 is not claimed for an unimplemented encoding, and these reference
calculations never feed the central integer evolution.

## Personally inspected primary sources

- Celledoni, McLaren, Owren and Quispel,
  [*Geometric and integrability properties of Kahan's method: The preservation of certain quadratic integrals*](https://arxiv.org/pdf/1805.08382),
  section 1 and Theorem 1: linearly implicit birational update and the precise
  scope of modified-integral results. The Einstein defects above were computed
  from this repository's force, not asserted by that paper.
- McLachlan, Quispel and Robidoux,
  [*A unified approach to Hamiltonian systems, Poisson systems, gradient systems, and systems with Lyapunov functions and/or first integrals*](https://arxiv.org/pdf/math-ph/9805021),
  section III, definition 1 and theorem 2: exact discrete-gradient identity and
  implicit invariant-preserving map. Its general existence framework supplies
  no bounded-channel explicit Rule3 compiler.

The coordinate changes, canonical splitting formulas, degree-eight midpoint
obstruction and executed Einstein counterexamples are this review's independent
derivations and evidence.
