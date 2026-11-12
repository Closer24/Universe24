# Independent review of the generic construction

Reviewer 8 of the requested eight-agent continuation. Baseline:
`8c53e69f4b466dcbd2da7dab7e3c365bd9731766`. This review reads the actual new
programs and runs additional independent controls. It changes no production
Engine, runtime, model or physical acceptance gate.

Reproduce the additional checks with:

```bash
python -m validation.generic_structure.independent_review
```

Evidence is `runs/generic-structure/independent_review.json`. The report hashes
the research source files and records the exact counterexamples below.

## The interaction and temporal compiler really connect

The existing joined example passes one face potential through the interaction
compiler, a pure-force adapter, the low-rank scheduler and the actual unchanged
Engine. It has six retained channels and restores complete workspace triples.
This is a genuine composition of the construction interfaces, not the sum of
unrelated passing fixtures. Its field shift charge is an algebraic invariant,
not a demonstrated Einstein momentum or energy.

An additional reviewer case uses a different potential,

```text
Phi = sum_i [-3*x_i^2/2 + 2*x_i*y_(i+ey)^2],
field signs = (+1,-1), A=(2,-1), B=(1,-2)^T.
```

The independently derived force is
`F_x(i)=-3*x_i+2*y_(i+ey)^2`,
`F_y(i)=-4*x_(i-ey)*y_i`.
Three nine-tick periods on 27 nodes match the independently constructed complete
macro state, including all six carries, signed matrix entries and y-face
periodic seams. Every macro inverse and full rewind agree. This is another
six-channel arithmetic construction; its signed gradient is not assigned a
physical Hamiltonian interpretation.

Review found two constructor-boundary defects and requested fixes:

- A caller could override the scheduler's 48-channel limit by passing a larger
  `budget`. The compiler now requires an exact integer budget in `1..48`;
  the independent review rechecks rejection of `budget=91`.
- The symmetry extractor accepted an out-of-range reduced carry before the
  Engine eventually rejected it. It now validates every carry as an exact
  integer in `0..5`; independent controls recheck `-1` and `6` rejection.

Review also found that the force adapter initially trusted a mutable
certificate string. It now reconstructs the pure-gradient tensor from the actual
declared potential and gear metadata and compares the actual coefficient table's
fingerprint. An independent negative control relabels a genuine inertial-plus-force
tensor as pure gradient while preserving its matching tensor hash; the adapter
rejects it. A hash or declaration alone does not establish that the table excludes
the inertial `6b` baseline. The reconstruction closes that semantic boundary.

## Rank and floor are separate obligations

The `n+r+3` count includes all retained work and scheduler registers. Within
this specific layout, substituting `a=3e_j` into the quotient drift proves
`BA=I` is necessary for independent componentwise quotients, hence `r>=n`.
The conclusion that 44 independent drifts require 91 channels is therefore
correct for this layout. A rank-one 48-channel instance is not an equivalent
full-rank 44-field kinetic map. No universal lower bound for all possible
reversible compilers follows.

The new review supplies a stronger concrete negative control:

```text
A = [[1,1],[0,1]], B = [[1,-1],[0,1]], BA=I,
a=(1,2), workspace carries=(0,0).
```

The actual seven-channel nine-tick Engine gives a drift `(1,0)`, while the
independent componentwise `floor(a/3)` gives `(0,0)`. Complete rewind still
passes. Thus an invertible matrix factorization does not commute with the
integer floor; `BA=I` is necessary and is not sufficient. The certificate
correctly keeps those statements separate.

## Complete-history constraints and the restricted sector

Both exact positive constraint maps have explicit inverses and polynomial
quadratic-invariant identities. The Groebner calculations reduce the full
prepared-history residuals, rather than just checking current fields.
The `3(Phi+Phi^-1)` construction is a sufficient embedding under its stated
degree, integer, locality, allocation and complete-preparation conditions.
It is not a generic compiler for arbitrary rational Einstein maps.

The independent cubic-null counterexample starts from
`a=b=(1,0,0)`. Each separate slice obeys `2xz+y^2=0`, but the next actual
Rule3 slice is `(1,0,-4)` and its quadratic form is `-8`. Inversion still
works. The missing history relation is substantive even when both individual
slices are null. The source's reduced Einstein tick-two failure is therefore
not repaired by the unrelated positive quadratic-form examples.

The full45-to-six extractor compares every substituted target polynomial and
checks omitted targets vanish. Carry transparency follows from coefficients
divisible by three; homogeneous `a,b` histories can coexist with arbitrary legal
node-dependent carries. The review separately verifies forward and backward
commutation on mixed signed nonzero histories and complete projection/embedding
equality. It also reproduces the physical defect `H_after=-7/4096`.

This is an exact invariant symmetry image with a valid inverse on that image.
It discards no incoming arbitrary45 state: states outside the image are refused.
It removes spatial, anisotropic and charged modes by restriction and preserves
the original temporal/constraint/bit-growth problems. The remaining channels
in this restricted lab cannot be counted as spare channels in the full model.

## Packet, frame and observation scope

The three-channel packet has an independent discrete spectral oracle. The
review verifies its group-velocity expression against a numerical derivative
of the independently written scalar dispersion relation. It then runs a new
24-node-side, z-direction, 24-tick packet preparation and checks the existing
deterministic field-error bound, spectral phase, centroid comparison and exact
rewind. Localization is along one axis; the transverse directions are planar.

The finite lattice dispersion, integer mass coefficient and complementary
temporal branch matter. This is not a common45 packet and does not have
fixed-physical-mass continuum refinement in the stated integer stencil.
FFT phase and decoded zero crossings are passive diagnostics; they do not
establish retained operational apparatus. The high-frequency zero-group-speed
negative is a spectral mode, not an executed localized stationary packet.

The 11-channel frame map has a correct exact determinant and complete-history
identity. The reviewer reruns its symbolic proof, three actual Engine steps
and its unprepared-history/conditioning negatives. These are onsite shears
with frozen parameters. They change the spatial metric, preserve volume and
can become exponentially ill-conditioned. They are neither Lorentz gauge
transformations nor sourced gravitational dynamics.

The observation contracts were inspected at the source boundary. `bind_observation`
calls the existing full-run verifier and computes provenance from the actual
bundle and saved trace. Its declared interpretation and dependencies remain
assumptions to audit separately. `join_observations` checks compatibility of
the resulting in-memory receipts; those receipts are not authenticated proof
objects for arbitrary imported data. No equality of physical observables or
validity of a semantic claim follows from matching hashes. The separate
contract audit executes the positive and negative saved-run cases.

## Conclusion

The new modules provide a concrete generic interaction-to-Engine path, exact
restricted embeddings and useful complete-state proof obligations. Their
mathematical scopes are compatible when stated this narrowly. They do not
compose automatically into a single Einstein model, and this review found no
basis to promote general gravitational constraints, stable shared-metric
packets or independent material clocks. The unresolved task remains an exact
physical map with a compatible complete integer history and counted allocation.
