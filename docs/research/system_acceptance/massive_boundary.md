# Massive homogeneous source: verified boundary and remaining implementation

The six-channel spinor construction is substantive progress for the declared
homogeneous, isotropic, expanding Einstein system with a neutral scalar of mass
squared one and comoving dust. Its quadratic physical decoder satisfies the
Hamiltonian constraint identically, while its cubic coordinate force pushes
forward to the intended five physical evolution equations. This is a different
physical interpretation from the earlier linear physical-numerator map; that
map's cross-history constraint failure does not disprove this construction.

The reviewed source is PR60 commit
`6b82369830bf763cbaddcc37bd972c555faea782`. Focused checks executed exact source
blobs loaded into memory against the consolidated repository dependencies.
They did not replace the production Engine, alter Rule3, or modify the source
under review. These checks are separate from the integration owner's full
suite and remote CI.

## What was verified

The coordinate decoder in
`validation/unified_law/constrained_coordinates.py` gives

`C = 6*k^2 - p^2 - phi^2 - 2*dust^2 = 0`

for every real spinor coordinate value. Symbolic expansion reproduced this
identity, all five source pushforward equations, continuum source continuity,
and the phase-equivariance identities. The existing full44 source comparison
passed all 33 homogeneous constraints and confirmed zero velocities for the
omitted fields. All 625 signed rational coordinate cases passed. The
wrong-dynamics control still rejects an altered force even though the decoder
continues to produce zero constraint.

The actual six-channel Engine map passed its complete retained-history
recurrence, scalar oracle, immediate inverses and full rewind. The default
tensor and seed fingerprints reproduced the published values:

- Tensor: `8d5f0fad5d094908afd4e78d05e60710b96c95943bb7aa791e5b753ff33e9df9`.
- Seed: `61b79e0831d775508ab04086aa4f4009d89bb6df95e2357e4ee7e5ff2777097f`.
- Allocation: six complete channels, 18 retained integers per node; 27 nodes.

Independent physical-coordinate RK4 refinement at 60 decimal digits reproduced
the following fixed proper-time comparison, with `T=1/8`:

| Engine steps | Step size | Maximum physical-field error | Peak retained bits |
|---:|---:|---:|---:|
| 3 | 1/24 | 0.003424288038394702 | 207 |
| 4 | 1/32 | 0.0025445298932897514 | 649 |
| 6 | 1/48 | 0.0016808919563542362 | 6101 |

Observed field orders were 1.03220774377 and 1.02258203717. The independent
1024/2048-step reference discrepancy was `2.4600852042871587e-18`.
These are separately fingerprinted timestep tensors, not one tensor whose
coefficients change during execution.

The analytic argument in `docs/research/unified_law/04_invariant_map.md` was
reviewed separately from those samples. Its positive denominator recurrence,
history bound `epsilon <= h^3/63`, weighted-norm bootstrap, beta bound and
Gronwall estimate are coherent on the stated seed domain
`h=1/m<=1/16`, `D0>=2`, `n*h<=1/8`. They establish finite-time first-order
convergence for this actual retained-history map, not efficient refinement.
Additional boundary executions used `h=1/16`, two ticks, and initial
denominators 2, 3 and 5. Each retained zero physical constraint, the stated
curvature/beta bounds and full rewind; peak bit sequences were respectively
`[3,15,54]`, `[3,16,59]` and `[3,19,66]`.

## Clock and source limits remain distinct

The same-law clock audit was rerun. At 3, 4 and 6 ticks its scalar phase errors
were approximately `0.00330197076`, `0.00245408886`, and `0.00162143849`.
Dust-mass errors were approximately `0.00005669673`, `0.00004150934`, and
`0.00002702010`. Exact rational exponential bounds certify a positive,
nonzero finite-step dust-mass drift. Thus zero Hamiltonian constraint does not
mean exact discrete dust conservation.

The scalar phase is monotone in the declared continuum domain, but its rate
depends on the evolving source. The exact rational witness and the independent
continuum reference reject identifying phase divided by mass with universal
elapsed proper time. No autonomous clock counter, transported packet,
detector, record stress, or quantum probability measure is supplied by this
construction.

This candidate fixes mass squared to one. A mass-parameter family and a
verified massless limit have not been implemented here. In particular, the
massless sector's conserved scalar momentum cannot be carried over as a
constant when the massive scalar force is present. Source recovery must be
checked explicitly before either candidate is represented as the other's
parameter limit.

## The efficient temporal path that remains open

The remaining temporal obstruction for this candidate is the cost of the
cubic projective denominator, whose bit length grows exponentially with the
number of ticks. It is no longer the old decoded Hamiltonian-constraint defect.

The existing native 21-channel quadratic scheduler is not an efficient
implementation of the selected spinor law. It executes a different quadratic
system, retains an exact-constraint failure, and certifies division depths only
one and two. Directly multiplying the cubic spinor force by its stored pulse
would produce degree four and violate the tensor contract. Passing mechanical
checks for that scheduler cannot transfer the spinor convergence result to it.

A concrete next design is to preserve the selected quadratic physical decoder
and factor the same cubic coordinate force through three quadratic temporary
quantities: `k`, `phi`, and `dust`. The force then uses linear terms and products
of a spinor coordinate with one of these quantities. A separate retained stage
could compute the quadratic quantities with a pulse-gated cubic polynomial;
a later stage could use pulse-gated bilinear force terms, also of degree at
most three. This observation identifies an algebraic route around the direct
degree-four gate. It is not a compiled temporal solution.

Acceptance requires all of the following on one immutable tensor:

1. An explicit compute/use/uncompute schedule preserving the correct data
   histories, with every auxiliary, pulse, scheduler, rounding remainder and
   persistent arithmetic record included in the total of at most 48 channels.
2. Independent scalar arithmetic and macro-map oracles, every-step inverse,
   complete rewind, and proven restoration or explicit continued retention
   of workspace. Reusing a register name is not a restoration proof.
3. A precision/refinement family for the same cubic coordinate ODE. For cubic
   coordinates scaled by amplitude `A`, the force scales as `A^3`; increasingly
   fine fixed-point precision and decreasing physical step size require a
   corresponding division mechanism. The present fixed depths one and two
   do not establish that family. Any reused deeper divider must retain its
   information and include its schedule and bit cost in the proof.
4. Finite-time convergence, a positive metric domain, exact decoded constraint,
   source/phase/dust controls and measured bit growth on the actual Engine
   trajectory. The current first-order theorem cannot simply be assigned to
   a different native update.

No such counted, reversible cubic native construction is implemented or proved
by this review. Rule3 need not be changed to investigate it, but feasibility
within the complete budget remains an open implementation and proof obligation.
The verified six-channel construction therefore remains a constrained
homogeneous research result with expensive temporal encoding, rather than an
accepted general Einstein or quantum system.
