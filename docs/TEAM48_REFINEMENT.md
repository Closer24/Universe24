# Integer refinement and constraint evidence within 44 channels

This follow-up replaces the old sign-leapfrog **research integrator** with a
projective integer construction. It removes the fractional-coefficient
obstruction, gives a compatible positive-frame preparation, and demonstrates
decreasing physical errors in two sourced test families. It does not establish
a general Einstein solver or operational apparatus. Coordination and all
negative findings are recorded in [issue 40](https://github.com/Closer24/Universe24/issues/40).

The baseline proposal is pinned at
`49b896c795203914a939e465d6d39e5b99343259` (PR42). The supported execution
architecture is main `c2d6b05a7b8e32cfad40162df0377335c8dc4577` (PR44).
The new implementation belongs in source-only validation. It supplies data to
the existing bundle/Engine/decoder interface; it does not add a runtime selector.

## The concrete change

For a degree-d polynomial spatial discretization `dy/dt=f(y)`, retain integer
numerators P and one uniform denominator D. Homogenize to
`F(P,D)=D^d*f(P/D)`. The fixed-six cubic-or-lower tensor implements

```
D_next = C*D^d - D_old
P_next = C*(D^(d-1)*P + h*F(P,D)) - P_old.
```

C is a static integer coefficient clearing the rational coefficients of
hF, never a new Engine divisor. All u values are multiples of three, so
every legal remainder remains unchanged. Denominator uniformity follows
from identical local preparation and identical onsite updates; no global
communication is introduced. Initial D>=2, D_old=0 gives a positive growing
denominator. All retained arrays invert exactly.

The decoded update is exactly Euler plus a retained-history term:
`y_next=E+(D_old/D_next)*(E-y_old)`, where `E=y+h*f(y)`.
Zero old numerators make the first step exactly Euler. The finite-time
consistency argument applies to a fixed spatial grid and a regular locally
Lipschitz ODE solution. It is not a continuum Einstein stability theorem.

The charged scalar/Maxwell/squared-dust/triangular-frame law has 40 physical
numerators and one denominator: **41 total channels**. Replacing three
diagonal frame entries by six amplitude numerators gives **44 channels**,
629 monomials for the tested massless law and 132 retained integers per node.
It has one metric, strict single-face support, degree at most three, and no
old-a input dependencies. The denominator replaces the sign channel.

For the positive frame, `B_aa=(p_a^2+q_a^2)/D^2`. Each pair has the same
linear coefficient in its numerator update; therefore its two-slice
Wronskian is exactly constant. Preparing each old q numerator as 1, all
other old numerators and old D as 0, gives nonzero W and prevents a vanishing
diagonal. The old slice is explicitly arithmetic memory, not a prior metric.
Its first physical perturbation is `-1/(C*D0^3)`; with the tested D0=S^2,
h=1/S it vanishes as O(h^7). This addresses the old incompatibility between
metric protection and a controlled temporal limit.

## Independent actual Engine evidence

The homogeneous test has initially B=I, K=-I, scalar momentum 2 and dust
amplitude 1: energy density 3 and all Einstein constraints initially zero.
It is compared with the independent mixed scalar/dust FLRW solution
`a(t)^3=1+3t+3t^2/4` at fixed proper time T=1/4.

| Updates | Maximum Hamiltonian residual | Maximum field error | Largest retained integer |
| ---: | ---: | ---: | ---: |
| 2 | 0.046875 | 0.192254 | 70 bits |
| 4 | 0.0146592 | 0.0795939 | 849 bits |
| 8 | 0.00629406 | 0.0370768 | 85,291 bits |

Independent integer updates, all six remainder classes, per-step inversion
and complete rewind agree. A heterogeneous charged/source test separately
checks all 81 nodewise Wronskians and positive diagonals; it is off-constraint
and is not evidence of physical convergence.

The inhomogeneous test uses the 41-channel law and a smooth periodic scalar
and positive dust profile, with nonzero momentum, fixed domain [0,1) and
final proper time 1/16. The oracle reconstructs curvature from the metric
independently of the retained frame connection. A disclosed additional
joint-refinement series gives:

| Spatial nodes per direction / updates | Hamiltonian | Momentum | Scalar-gradient | Connection/metric |
| --- | ---: | ---: | ---: | ---: |
| 8 / 4 | 0.088176 | 0.005126 | 0.0000102866 | 0.00084997 |
| 12 / 6 | 0.067857 | 0.003273 | 0.0000102096 | 0.00062557 |
| 16 / 8 | 0.053374 | 0.002309 | 0.0000090045 | 0.00048861 |

These are unscaled residuals, not errors divided by a growing normalization.
The separate temporal series also improves all four. **The original joint
series, fixed-time-step spatial series, and first better-resolved joint
series fail the all-four strict-decrease test.** They remain in the evidence.
The additional series was selected after inspecting those failures and is
explicitly exploratory; it is not a held-out acceptance test. Three short
refinement levels do not certify general stability or exact constraints.
The seed-quantization sweep reduces initial H from 0.3125 to approximately
3.08e-7; finite-time errors eventually reach the discretization floor.

## What the negative findings now mean

The old momentum-constraint tangent of magnitude 21 is independently
identified as a spatial product-rule defect. For the original fixture it is
exactly `-3*(D(k^2)-2*k*Dk)-(D(q^2)-2*q*Dq)/2`. On an exact rational,
fixed-domain smooth family it decreases approximately quadratically under
spatial refinement. It does not imply that time refinement alone repairs
the discrete constraint surface, or that all spatial constraint problems
are solved.

Independent restricted controls provide additional targets, not extra
components appended to the 44-channel allocation:

- A five-channel transported pp-wave/null-dust family has positive energy,
  nonzero momentum and Weyl curvature, exact sampled transport, and an
  independent symbolic four-dimensional Einstein/stress-conservation check.
  Its numerical residual checks only the transverse reduced equation inside
  the chart; periodic transverse seams are excluded.
- A four-channel inhomogeneous plane-dust analytic family verifies all
  Einstein components, stress conservation and a proper-time readout with
  separate temporal/spatial/quantization controls. Its dynamics have no
  neighbor exchange; transverse generalization fails an explicit control.
- Seven-channel flat scalar dynamics preserve time-polarized local charge,
  energy and momentum balances exactly. An eight-channel face-current control
  preserves Gauss while a same-node-current variant fails. The latter lacks
  reciprocal electromagnetic force/energy coupling and is not full MKG.

## Remaining gates and cost

| Requirement | Current evidence |
| --- | --- |
| Fixed-six, integer, <=48, degree<=3, one face, full inverse | Passed for the reported constructions and tests |
| Fractional physical time/space steps | Constructively encoded with a proved passive ratio identity |
| Positive metric for protected44 | Exact nodewise invariant on the declared preparation |
| Temporal convergence with nonzero protecting memory | Measured for sourced FLRW; generic semidiscrete consistency argument |
| General nonlinear Einstein constraints and continuum convergence | Open; mixed positive/negative spatial evidence |
| Efficient long-duration evolution | Open; bit length grows roughly d^n |
| Autonomous proper-clock/detector/Born/Bell behavior | Not established; spare slots are not apparatus |

The bit-growth cost is substantial, despite the fixed channel count. It
cannot be removed by dividing or resetting live numerators without a new
reversible encoding proof. All observation ratios are passive; no observer
feeds evolution. No physical gate is closed by a software test or a restricted
analytic family.

Detailed derivations, primary-source ledgers and reproduction programs are
beside the code in `validation/geometry/team48/`. The literature motivates
methods; the projective map and its invariants are checked directly here.
The aggregate evidence records source hashes, command results, failures,
runtime-interface checks and the exact scope of each claim.

Reproduce from the source checkout:

```bash
python -m unittest universe24.tests.test_team48_refinement -v
python -m validation.geometry.team48.refinement_run_audits
python -m validation.system_smoke --out runs/projective-system-smoke
```

The runner writes `runs/team48/refinement/report.json` and preserves every
comparison group. Its runtime handoff runs in an isolated Python process and
checks all 13 imported package/core/system files against the pinned main Git
blob hashes before execution. Each output retains the complete channel
ownership, tensor/seed, arithmetic trace and decoder results.
