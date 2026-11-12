# Researcher 3: variational gravity and local clocks

Date: 2026-11-11. Inspected local base `613ea1b`; research target is PR #47,
published head `621fc1f55800e50e1db5f6a30ce24bb83716a49a`. This report changes
no runtime, model, metric authority or acceptance gate. Issue #40 and the
repository `AGENTS.md` remain the contract.

## Result

The literature gives a useful design criterion: derive a **discrete constraint
identity and its compatible matter current from one action**, before choosing
the arithmetic encoding. It does not give a ready-made local 48-channel,
cubic-integer update for nonlinear Einstein gravity. In particular, solving
for lapse and shift is generally an implicit equation-solving method, and
introducing material clocks does not make this cost disappear.

The most economical next route is a restricted, action-first, sourced sector
whose constraint propagation is an algebraic identity. Compile that identity
into the existing fixed-six Engine only after proving it; then enlarge its
spatial and nonlinear domain. Retain #47 as the reference for continuum error
and never replace its failed constraints with a renamed mixed-time quantity.

## Primary papers actually inspected

The PDF sections below were opened and their formulas/method descriptions read.
The citations motivate the audit; the integer controls below are independent
calculations for this project, not results claimed by these papers.

| Source | Inspected result | Consequence for Universe24 |
| --- | --- | --- |
| Di Bartolo, Gambini and Pullin, [Consistent and mimetic discretizations in general relativity](https://arxiv.org/pdf/gr-qc/0404052), §II, equations (3)–(10), and §III | A discrete first-order action gives equations involving new canonical momenta and multipliers. Generic nonlinear cases determine the multipliers implicitly. The exact mimetic result is linearized gravity about Minkowski; mixed-time pseudo-constraints must be distinguished from same-time constraints. | Use its linearized identities as an audit target. Importing its general algorithm would introduce a forbidden runtime solve. |
| Gambini, Ponce and Pullin, [Consistent discretizations: the Gowdy spacetimes](https://arxiv.org/pdf/gr-qc/0505043), §II.B, equation (14) | Their reduced nonlinear evolution solves coupled algebraic systems. Their particular partitioned solution method additionally adjusts a lapse component with Newton–Raphson using a conserved spatial sum; the paper explains that a full coupled solve avoids that partitioning pathology. | Neither the global correction nor the full nonlinear solve is our fixed local tensor. This is concrete evidence for a research method, not a drop-in algorithm. |
| Bahr and Dittrich, [Improved and Perfect Actions in Discrete Gravity](https://arxiv.org/pdf/0907.4323), §2.1, equations (2.11)–(2.12), theorem; §5 | The exact mechanical action is the Hamilton–Jacobi action evaluated on a continuum boundary-value solution. Their explicit gravity results cover 3D with cosmological constant and restricted 4D constant-curvature/simplex settings. They state that an explicit improved action with propagating gravitational degrees of freedom was not obtained and expect nonlocality there. | An exact action already contains a solved evolution problem. Its existence does not establish a cubic, face-local implementation. The nonlocality statement is the authors' expectation, not a general impossibility theorem. |
| Frauendiener, [On the applicability of constrained symplectic integrators in general relativity](https://arxiv.org/pdf/0805.4465), §§4–5, equation (22) | A naive SHAKE/RATTLE correction requires inversion of the constraint Poisson-bracket matrix. First-class GR constraints make it singular on the constraint surface; breaking that property can produce deteriorating conditioning toward the continuum. | Reversibility or symplecticity is insufficient. Gauge fixing can alter the rank problem, but is an additional construction whose locality, solve, workspace and inverse need proof. |
| Brown and Kuchař, [Dust as a Standard of Space and Time in Canonical Quantum Gravity](https://arxiv.org/pdf/gr-qc/9409001), §§III.A, IV.B, equations (3.16), (4.6)–(4.11), and §VII | Dust proper time and three comoving coordinates are physical reference fields. In a specified positive branch, constraints can be written with separated dust momenta and Abelianized. The gravitational Hamiltonian involves a square root and inverse coordinate Jacobian. Special nonrotating/frame-orthogonal restrictions simplify the time sector. | This supports a matter-based clock interpretation, but neither removes its stress-energy nor gives a polynomial discretization. Coordinate time, dust proper time and independently recorded detector ticks remain different claims. |

## Why four extra clock variables do not close the existing system

For a representative first-order action

\[
L_n=p_n(q_{n+1}-q_n)-N_n C(q_n,p_n),
\]

the canonical equations are

\[
P_n=p_n+N_n C_q(q_n,p_n),\qquad
q_{n+1}=q_n+N_n C_p(q_n,p_n),\qquad C(q_n,p_n)=0.
\]

Thus the new canonical momentum is `P[n+1]=p[n]`; evaluating the constraint
at `(q[n],P[n+1])` does not evaluate it at `(q[n+1],P[n+1])`.

Take `C=(p²+q²)/2-E`, and the exact rational values
`q=1, p=2, N=1/4, E=5/2`. Then `P_in=9/4`, `q_out=3/2`.
The mixed-time residual is exactly zero, while the same-time residual after
the update is `5/8`. This is not a GR counterexample; it isolates the logical
mistake of identifying the two constraint statements.

Starting instead on the ordinary constraint with `q=1, P_in=2, E=5/2`, this
particular discretization permits `p_out=2, N=0` or `p_out=-2, N=4`.
The first branch stalls; the second gives `q_out=-7` and same-time residual
`24`. Rational canonical data `q=1, P_in=1, E=3/2` require `p_out²=2`.
There is no rational numerator/denominator representation of that exact root.
An algebraic-number encoding is conceivable, so this is an obstruction to
this direct rational import, **not** a no-go theorem for all integer encodings.
Such an alternative must explicitly count its coefficients, branch information
and extension arithmetic and prove an invariant representation.

The present protected law has 44 channels. Adding one lapse and three shift
numerators gives 48 before any solver state, scheduler or detector record.
Multiplying a present cubic monomial by a new lapse generally produces degree
four. New auxiliary variables or microsteps might factor it, but their state
and causal schedule are not free. The unprotected 41-channel law leaves more
room, with no transfer of the protected metric theorem to that different
allocation.

Brown–Kuchař dust gives another algebraic possibility:

\[
C_{\rm dust}=P_T+h,\qquad
h=-\sqrt{C_{\rm grav}^{\,2}-g^{ij}C_i C_j}.
\]

The continuum domain and branch matter. Replacing the existing single dust
amplitude by the direct eight-field canonical allocation
`T, Z¹,Z²,Z³, P_T,P_1,P_2,P_3` would give `44-1+8=51` channels in the present
one-numerator-per-field scheme. This is an accounting example, not a universal
lower bound: a proved pair encoding or a reduced sector could change it.
Neither the square root nor the inverse Jacobian is supplied by that count.

## An exact small control that does fit the arithmetic

The audit constructs three channels `q,T,P_T`, all with `u=6b`. Consequently
the existing Rule3 gives `b_next=2b-a` and preserves every remainder. With
`a_T=b_T-1`, `a_P=b_P`, and even prepared velocity `v=b_q-a_q`, choose
`P_T=-v²/2`. The following identities hold at every step:

\[
v_{n+1}=v_n,\qquad T_{n+1}-T_n=1,\qquad
P_{T,n+1}=P_{T,n},\qquad 2P_T+v^2=0.
\]

This is a restricted parametrized free mechanical sector, not a spacetime
model, shared-metric apparatus or gravitational source. It demonstrates what
an acceptable algebraic claim looks like: compatible preparation, invariant,
independent oracle, exact inverse and an explicit domain. The coordinate
counter is not promoted to an operational proper clock.

`python validation/research_eight/03_variational_clock_audit.py` ran the actual
Engine on 27 nodes for 128 steps in each of all six remainder classes. Every
state matches the closed-form oracle, all per-step inverses and full rewinds
pass, the largest retained value needs 10 bits, and the constraint residual is
zero. An incompatible seed with `P_T` increased by one retains residual `2`:
the clock does not repair the constraint. The same script reproduces all
nonlinear rational negative controls above. Source hashes and results are in
`runs/research_eight/03_variational_clock_audit.json`.

## Concrete next construction and rejection tests

1. Choose a **single spatially varying sourced sector** and a discrete action,
   with preparation, metric, matter stress and discrete constraints stated
   before measurement. A plane-symmetric scalar/dust sector would reuse the
   current independent oracles. A linearized Minkowski sector is a preliminary
   identity check, not acceptance of nonlinear matter gravity.
2. Seek a finite polynomial map `F` and a discrete constraint vector `C_d`
   with an exact factorization `C_d(F(z))=A(z) C_d(z)`. This is our proposed
   algebraic acceptance target, not a theorem from the papers. The constraint
   can be staggered, but its continuum limit and its difference from the
   independently sampled Einstein constraints must be measured separately.
3. Derive energy/momentum flux and geometric work from the same action.
   On a small periodic lattice, first use exact rational/symbolic calculations
   outside production. Reject a candidate if it needs more than one face edge
   in a monomial or a future-state solve. Gauge identities must be tested on
   nontrivial sources, not only a flat/vacuum seed.
4. Only then map the finite polynomial update into fixed-six channels. Count
   all phase/workspace registers, prove their invariant sectors and complete
   inverse, and report integer-bit growth. A physical time counter is not a
   replacement for independent moving/stationary clock tests.
5. Hold out one smooth inhomogeneous matter profile, one constraint-violating
   preparation and one nontrivial coordinate/gauge case. Predeclare separate
   time, space and integer-quantization refinement at fixed physical endpoint.
   Report both the exact discrete identity and literal Einstein defects;
   neither may replace the other.

This path is smaller than compiling a general nonlinear lapse solver and
more directly addresses the present failure. It remains a proposal. General
nonlinear Einstein closure, efficient long runs, an in-budget material clock
and operational detector behavior are still **not established**.
