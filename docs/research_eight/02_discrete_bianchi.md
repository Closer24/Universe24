# Researcher 2: shift-aware algebra before nonlinear Einstein constraints

Research date: 2026-11-11. Inspected local baseline `613ea1b`; current proposal
PR #47 is published at `621fc1f55800e50e1db5f6a30ce24bb83716a49a`.
This is source-only research. It does not change the Engine, the accepted
model status, the mathematical contract or an installed runtime.

## Finding and recommendation

The immediate algebraic target is a **compatible face-flux product and discrete
constraint identity**, rather than a more accurate derivative inserted into
the existing continuum-expanded equations. The existing spatial counterexample
already isolates an exact product-rule mismatch. Shift-aware products can
remove that mismatch without extra registers. They do not by themselves prove
that a revised Einstein/matter law propagates its constraints.

Three different claims must be checked separately:

1. A kinematic identity of discrete transport/curvature.
2. A dynamical identity linking a discretized action, gravity equations and
   matter conservation.
3. A constraint-preserving **explicit integer implementation** of those
   equations in the fixed-six Engine within 48 channels.

The papers below provide useful results for the first two levels in specified
domains. None supplies all three under the Universe24 contract.

## Primary papers actually inspected

The original full-text sections and equations were opened, not only abstracts.

| Primary source | What was read and established | Boundary for this project |
| --- | --- | --- |
| Di Bartolo, Gambini, Pullin, *Consistent and mimetic discretizations in general relativity*, [gr-qc/0404052](https://arxiv.org/pdf/gr-qc/0404052), JMP 46, 032501 (2005) | Sec. III, equations (33)–(36), and Sec. V: exact discrete propagation of linearized Minkowski constraints follows from compatible commuting differences and summation by parts. | Nonlinear consistent discretization generally determines lapse/shift. The displayed metric stencil includes diagonal and distance-two samples; it is not directly a single-face tensor. Explicitness is singled out as a property of the linearized case. |
| Kur and Glasser, *Discrete Gravity with Local Lorentz Invariance*, [2202.02486](https://arxiv.org/html/2202.02486v2), PRD 106, 064001 (2022) | Secs. III–V, especially (17)–(25), (27)–(29): edge Poincare holonomies, a lattice Palatini action, vacuum equations, local Lorentz invariance and multisymplectic structure. | The cubical curvature in (23) is a four-edge product containing a diagonal vertex. Local Lorentz symmetry and multisymplecticity do not by themselves establish the desired nonlinear Hamiltonian/momentum propagation or coupled matter law. |
| Hamber and Kagel, *Exact Bianchi Identity in Regge Gravity*, [gr-qc/0107031](https://arxiv.org/pdf/gr-qc/0107031), CQG 21, 5915–5948 (2004) | Secs. III–V, equations (3.7), (4.4)–(4.13): correctly ordered transported rotation products obey exact nonlinear identities. Their small-curvature expansions differ from the full identities. | A nonlinear holonomy identity is not the same equation as the literal sampled ADM constraint. Matrix ordering and transport cannot be discarded when replacing it by a sum of curvatures. |
| Kato, Sakamoto, So, *No-Go Theorem of Leibniz Rule and Supersymmetry on the Lattice*, [0810.2360](https://arxiv.org/pdf/0810.2360) | Sec. II, equations (2.1)–(2.7): translation-invariant local lattice product/difference operators cannot satisfy the ordinary Leibniz identity nontrivially under the stated infinite-lattice assumptions. | This rules out one naive repair strategy, not all lattice gravity. Shifted products, restricted sectors, approximate identities and different discrete constraints are different hypotheses. Researcher 6 treats the finite pointwise version separately. |

## Exact shift-aware algebra

Let `T` move a scalar to one face neighbor and let `delta=T-I` (the physical
spacing factor can be restored as a static rational calibration). Then

```text
delta(f g) = (T f) delta(g) + g delta(f)
delta(f g h) = (T f)(T g) delta(h)
             + (T f) h delta(g) + g h delta(f).
```

Both identities follow by expansion and cancellation. Every expanded monomial
uses only the target and that one neighbor, with degree at most three. These
are exact shift identities; they are not the ordinary same-point Leibniz rule.
They work at integer amplitudes of any size and require no stored derivative.

For the centered difference `D=(T-T^-1)/(2 dx)` and average
`A=(T+T^-1)/2`, the exact identity is

```text
D(f g) = A(f) D(g) + A(g) D(f).
```

An implementation must first expand and cancel this expression: individual
uncancelled products can contain both neighbors, violating one-face support.
For cubic products use the forward shifted identity or explicit conservative
flux, rather than multiplying three centered averages and derivatives.

The existing constrained scalar/dust fixture has

```text
M0_dot = -3 [D(k^2)-2 k D(k)] - [D(q^2)-2 q D(q)]/2,
k = (10,14,18,14,10), q = (2,4,0,-4,-2), dx = 1.
```

The literal expression has peak 21. Replacing each scalar product identity by
`D(s^2)=2 A(s)D(s)` yields exactly zero. **This only verifies the algebraic
defect cancellation.** It is not a revised Einstein RHS, a new constraint
tangent calculation, or evidence that the existing trajectory was repaired.
Changing an observer's residual would not repair the dynamics.

## Actual Engine audit and matched failure

Reproduce from the repository root:

```bash
python -m validation.research_eight.02_shift_flux_audit
```

Files: `validation/research_eight/02_shift_flux_audit.py` and generated
`runs/research_eight/02_shift_flux.json`. The JSON includes the script hash,
both tensor hashes, all runs, all sums and integer bit lengths.

The audit uses one channel at each of 125 periodic nodes. Its cubic tensor is

```text
u_i = 6 b_i + 3(b_(i+ex)^3 - b_(i-ex)^3).
```

Thus every legal remainder is unchanged and the exact recurrence is

```text
b_i' = 2 b_i - a_i + b_(i+ex)^3 - b_(i-ex)^3,  a_i'=b_i.
```

The periodic sum obeys `S_(n+1)=2S_n-S_(n-1)`. Constant `S` requires the
declared initial condition `sum(a)=sum(b)`; otherwise the sum evolves affinely.
This is a mathematical scalar balance, **not a claimed physical energy**.

| Control | Retained channels | Degree | Strict support | Measured result |
| --- | ---: | ---: | --- | --- |
| Conservative cubic flux | 1 (three integers/node) | 3 | Pass | Sum remains 125 for all four updates. |
| Same-point chain-rule substitution `u=6b+9b^2(b_+-b_-)` | 1 | 3 | Pass | Sum changes 125 to -775 on the first update. |
| Direct diagonal plaquette factor | No execution | 1 | Rejected | Tensor construction raises `LocalityError`. |

Each law was run with all six uniform remainder classes **and** a spatially
mixed `r_i=i mod 6` preparation. An independent scalar update agrees with each
Engine transition; every step inverts and four-step full rewind reproduces all
`a,b,r`. The shifted pair and triple identities were checked on 10,000 seeded
integer tuples in addition to their algebraic expansion.

The conservative control's peak bit lengths are `2,5,15,46,136`; the negative
control's are `2,6,17,50,147`. These deliberately coarse nonlinear controls
show that exact conservation and reversibility do not solve growth or
stability. They do not constitute a convergent transport solver.

## Allocation and why a direct Palatini import fails

| Proposed operation | Retained cost and obstruction |
| --- | --- |
| Algebraic shift/face-flux rewrite of an existing polynomial RHS | No additional registers when the fully expanded expression remains degree <=3 and one-face. The current 41/44 allocation could remain unchanged; a complete compatible gravity law has **not** been derived. |
| The demonstrated scalar flux control | Exactly one total channel; no phase, workspace, link state or extra bank. It is a validation primitive, not an appended physical subsystem. |
| Cubical Palatini with explicit 4x4 spatial Lorentz matrices | Three positive spatial link matrices require 48 scalar entries before coframes, sources or workspace in this straightforward representation. This is a representation cost, not a universal lower bound. Intrinsic six-parameter coordinates introduce separate group/encoding questions. |
| Cubical Palatini curvature treated as a free symbol | Conceals four link factors and a diagonal vertex. The action `e e Omega` is degree six in primitive link/coframe entries on a cubical face, not cubic. Retaining `Omega` demands storage and exact compatibility; it cannot be treated as free scratch. |
| Sequential loop transport over microticks | Can propagate influence by face steps, but must account for retained partial products, clock, undo information and changing links. No <=48 allocation/invariant is supplied here. Multiplying a cubic force by a scheduling phase also raises its degree to four unless separately factored. |

The Lorentz inverse can be written as `eta Lambda^T eta` on the exact group
sector, so it is not the matrix inverse alone that blocks the direct import.
The support, representation, group invariant, action degree and explicit
update all need proofs. A four-vector carried around a loop can be an
operational experiment; it does not automatically compute the instantaneous
full curvature while the geometry evolves.

## Concrete next construction and falsifying gates

First retain the same linearized frame variables and build compatible
commuting differences/face fluxes with **a derived discrete constraint
propagation identity**, checked independently on the actual Engine. A free
gravitational-wave check alone is insufficient: include nonzero constraint
perturbations to verify the propagation operator, then conserved external
linearized sources with their approximation explicitly stated.

For nonlinear matter, derive gravity and stress from the same discrete action
or compatible balance identity. Researcher 4's polarized matter/work identity
is an appropriate coupling target. Do not replace energy density in the old
gravity equations and assume that its new conservation law follows.

Before an integration claim require, in order:

1. Symbolically establish `C(next)=A(state) C(state)` for the declared discrete
   constraints, or establish a stated defect bound. If this cannot be shown,
   report failure rather than rename a monitored residual.
2. Map every product to degree <=3, one-face terms and audited retained slots.
   Clock factorization and any transport accumulator count in the cap.
3. Demonstrate complete fixed-six rewind on arbitrary legal carries and actual
   source perturbations; quantify integer growth.
4. Separately test convergence of those discrete constraints to continuum
   Hamiltonian/momentum constraints, using the independent reconstructed metric,
   fixed-time joint refinement and held-out spatial profiles from #47.
5. Keep a naive same-point product law as a matched negative control.

Current conclusion: the shift-aware face-flux algebra is feasible under the
micro-law and removes a demonstrated class of algebraic errors. Full nonlinear
Einstein closure, efficient bit growth, coupled operational clocks and a
complete accepted <=48 tensor remain open.
