# Matter, shared face exchange and geometric work

Researcher 4 of the eight-researcher review, 11 November 2026.
Inspected local source: `613ea1b`; PR47 evidence is pinned at
`621fc1f55800e50e1db5f6a30ce24bb83716a49a`. This report changes no installed
runtime or accepted physical model. Coordination: issue #40; operational
clocks, when derived, belong in #41.

## Recommendation

Derive the matter current and the reciprocal geometric source from the same
discrete edge action. Use the two retained time slices to form the action's
actual discrete charge, stress and energy balances. In a changing geometry,
the matter-energy balance includes geometric work; requiring constant matter
energy would test the wrong equation. These are concrete construction rules,
not a proof that the present 44-channel law satisfies them.

The new executable control below proves an exact local flux/work identity
inside the unchanged Engine. It does not close Einstein constraints or supply
an operational clock.

## Primary papers read, and what they actually establish

1. Squire, Qin and Tang, *Geometric integration of the Vlasov–Maxwell system
   with a variational particle-in-cell scheme*, Physics of Plasmas 19,
   084501 (2012), [author manuscript](https://arxiv.org/pdf/1401.6723).
   Read the action and field equations (4)–(9), and particle equations
   (10)–(13), pp. 5–7. The same gauge-invariant discrete action determines
   the field update and charge deposition, giving compatible Gauss
   propagation. The field Hodge star is part of that action. Their particle
   update is generally implicit when crossing cells. Consequently this is
   a useful design source, not an allowed drop-in integer implementation.

2. Glasser and Qin, *The geometric theory of charge conservation in
   particle-in-cell simulations*, Journal of Plasma Physics 86 (2020),
   [author manuscript](https://arxiv.org/pdf/1910.12395).
   Read §5, especially theorem (5.3), and §6, equations (6.12)–(6.18)
   and initialization discussion around (6.30). Their sufficient condition
   for exact momentum-map conservation is that **each split Hamiltonian**
   has the same gauge symmetry and its flow is integrated exactly. The
   momentum map also defines the correct initial Gauss constraint. Arbitrary
   splitting, integer rounding, or labeling an old current “Noether” does
   not inherit the theorem. Their continuous Lie-group action has not been
   constructed on our full integer/remainder state.

3. Xiao, Qin, Liu and Zhang, *Local Energy Conservation Law for
   Spatially-Discretized Hamiltonian Vlasov–Maxwell System*, Physics of
   Plasmas 24, 062112 (2017), [author manuscript](https://arxiv.org/pdf/1612.04186).
   Read the discrete operators (8)–(10), energy balance (39), the paragraph
   immediately following it, and Appendix A. Their conservation result is
   spatially discrete and continuous in time. The authors explicitly say
   temporal discretization generally removes exact energy conservation;
   symplectic stepping instead controls energy error under its assumptions.
   Appendix A's local-divergence representation also does not promise our
   stronger target-plus-one-face polynomial stencil or a 48-register bound.

The conclusions above concern the papers' stated domains. The following
identities and Engine audit were derived and checked here independently.

## Exact local balance with changing coefficients

For one real scalar, let `p` be canonical momentum and `q` its spatial
gradient. The one-dimensional Hamiltonian density is

`H_m = (A p² + B q²)/2`.

For a zero-shift scalar on a metric, the corresponding coefficients are
`A=N/sqrt(gamma)` and `B=N*sqrt(gamma)*gamma^xx`. This identifies the
continuum target only: the audit's A and B are autonomous affine coefficient
fields, not an Einstein metric, and no reciprocal stress feeds them.

Set `Delta f_x = f_(x+1)-f_(x-1)`. At unit time/space steps, the control is

```text
phi_next = phi_previous + 2 A p
p_next   = p_previous   + Delta(B q)
q_next   = q_previous   + Delta(A p)
A_next   = A_previous   + 2
B_next   = B_previous   + 4.
```

All coefficients are retained before evolution. There is no runtime
callback, external background injection, or future-state lookup. The
gradient constraint propagates as
`q_next-D phi_next = q_previous-D phi_previous`, with `D=Delta/2`.
Both initial slices are prepared on that constraint.

Define the doubled polarized matter energy of the current retained pair:

`E2 = A_previous p_previous p + B_previous q_previous q`.

For the face from x to y=x+1, define

`J_xy = (A p)_x (B q)_y + (B q)_x (A p)_y`.

Define the local coefficient-work term

`W = (A-A_previous) p_previous p + (B-B_previous) q_previous q`.

Direct substitution gives the exact identity

`E2_next-E2 = J_(x,x+1)-J_(x-1,x) + W`.

Proof: expanding the left side first separates W; the remaining terms are
`(A p)_x Delta(B q)_x + (B q)_x Delta(A p)_x`. Expanding the two face
fluxes gives precisely those terms. No continuum product rule, truncation
estimate, or constraint projection is used. The conventional outward
physical flux is `-J` with this sign convention. On periodic boundaries,
the total change equals the sum of W because the face flux telescopes.

This does **not** make E2 positive on arbitrary pairs. It neither controls
the leapfrog computational mode nor proves stability. High-amplitude audit
growth is retained and reported.

### Actual Engine evidence

Run:

```bash
python -m validation.research_eight.04_metric_work
```

Source: `validation/research_eight/04_metric_work.py`.
Fresh result: `runs/research_eight/04_metric_work.json`.

| Check | Compatible face update | Coefficient-outside-derivative control |
|---|---:|---:|
| Retained channels / integers per node | 6 / 18 | 6 / 18 |
| Tensor monomials / maximum input degree | 7 / 3 | 7 / 3 |
| Lattice / updates | 5³ / 8 | 5³ / 8 |
| Exact local energy/flux/work residual | 0 | 3,903,444,548,646,001,833,993 |
| Twice scalar-gradient constraint peak | 0 | 171,594,253,132 |
| Largest retained integer | 39 bits | 40 bits |
| Independent direct recurrence | Passed | Passed |
| All six remainders; exact inverse/rewind | Passed | Passed |

The compatible law's tensor SHA256 is
`a2461acb92f1989f160bb2902369dd1b814d77626cb7c200633908573f40d0f5`.
The wrong control replaces `Delta(B q)` with `B Delta(q)` and likewise for
A. It still satisfies the mechanical/inverse contract but violates the
proposed physical identities. Omitting W from the compatible law gives a
peak nonzero residual of `2444576114709428018`, exactly the omitted work.
These are raw integer diagnostics, not continuum error estimates.

The face flux is quartic as a passive diagnostic. The evolution tensor is
cubic because every physical quadratic update receives one sign factor.
No flux registers are hidden in the state. This standalone six-channel
control is **not** appended to the 44-channel candidate.

## A route to reciprocal matter–geometry exchange

An elementary candidate edge contribution is

`V_xy = C_xy (phi_y-phi_x)²/2`.

Its canonical forces are

```text
F_phi_x =  C_xy (phi_y-phi_x)
F_phi_y = -C_xy (phi_y-phi_x)
F_C     = -(phi_y-phi_x)²/2.
```

The same term supplies both the neighbor exchange and the response to the
geometric coefficient C. These forces are quadratic, depend on one face,
and use no divide-by-state operation. Fixed rational factors can be cleared
statically in the already supported exact compiler. But this is not a full
proposal: a retained C needs its geometric conjugate/encoding, a complete
gravitational action, the gauge constraints, and a demonstrated symplectic
or discrete-variational evolution. Explicitly advancing the displayed
forces does not automatically conserve the cubic V exactly.

Using a discrete-gradient formula that contains future C or phi would give
an implicit equation. That is disallowed as a hidden runtime solve, even if
it would conserve an energy mathematically. The native kick–drift route
being reviewed by researcher 1 is a possible alternative, but its integer
floor/remainder step must itself be shown to preserve the desired symmetry.

For charged complex matter, a genuinely gauge-invariant edge action compares
`phi_y` with a transported `U_xy phi_x`. This brings extra transport state,
degree and exact-norm arithmetic. Simply multiplying the old additive
potential by a phase is not a proof. The existing rational pure-gauge
negative control in `matter_repair_flux.py` remains applicable. A metric
weighted cubic physical current cannot be put through the quadratic sign
compiler unchanged: the sign factors can exceed the input-degree bound.
Stored products or retiming would have to be declared and counted.

## What must be tested for Einstein and for clocks

The covariant continuum identity is

`partial_mu(sqrt(-g) T^mu_nu) = sqrt(-g) T^(alpha beta) partial_nu(g_alpha beta)/2`.

It follows directly from `nabla_mu T^mu_nu=0`, symmetry of T, and the
Levi-Civita connection. It explains why the desired matter-energy/momentum
test contains geometry-dependent work/force terms. Generic curved
spacetimes have no required globally conserved matter energy; a Killing
field, when available, yields an associated conserved current. There is
also no generic tensorial local gravitational-energy density to cancel
matter energy by simple addition.

The practical next gate is a small **reciprocal** sourced patch whose current,
stress, geometric work and geometric update come from one discrete action.
Test complete local balances, Gauss, H/M/torsion, pure gauge, source reversal,
all remainders, and convergence against an independent metric oracle. A
clock based on a charged/complex matter phase must use this same coupling;
the computational sign channel is not proper time. Proper-clock readiness
therefore remains open in #41.

| Claim | Status |
|---|---|
| Variable-coefficient wave has exact polarized local flux/work identity | Proved and actual Engine checked |
| Compatible stencil preserves its scalar-gradient constraint | Proved and checked |
| Existing flat complex-scalar/Gauss controls remain useful | Established restricted controls, no promotion |
| Shared discrete edge action can supply reciprocal force formulas | Algebraic candidate; no GR completion |
| General charged Einstein model, exact H/M propagation, operational clocks within 48 | Open |
| Long-time stable/positive energy and bounded-bit evolution | Not established by this control |
