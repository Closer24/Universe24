# Independent synthesis: one runtime and the missing physical coupling

## Decision

The integrated code supports one execution system. It does not yet supply one
physical law joining general spatial gravity, material clocks, repeated
cosmological bursts and sustained structural growth. The README and research
agenda correctly retain that distinction. Closing PRs and issues is a change
to work organization, not evidence that the physical construction is complete.

The central locality postulate is represented correctly: each node updates
retained integers from the old local snapshot and immediate face neighbors.
The tensor's individual monomials obey the stricter target-plus-one-edge
support rule. Quantum and geometric interpretations remain outcomes to derive,
not consequences established merely by choosing integer arithmetic.

## What can be joined now

The twelve-channel local carrier/record construction is the strongest existing
same-history join in this review. It contains actual repeated scattering,
retained records, exact directional packet balances and source-dependent
geometry profiles. Its independent spline reconstruction gives a positive
two-null-stream Einstein chart within a declared finite causal interior.

That result cannot be extended by metadata alone. The packet equations do not
read the geometry profiles. Their total directional sources freely stream,
even though species routes change in collisions. The periodic positive-source
chart is impossible for this ansatz because the sum of a periodic second
difference vanishes. A finite interior with explicitly retained seam defects
is the proved domain, not an entire periodic Einstein universe.

The homogeneous massless and anisotropic laws have different state meanings
and invariants. Their exact source clocks are passive diagnostics. The massive
spinor law has its own finite-time proof and expensive integer growth. The
static gauge wave is unstable; the dynamic sign-link law has a prepared period
dividing three and lacks successive-edge signal transport. No documented
conjugacy or common source action identifies these laws as one physical tensor.

Putting distinct blocks on the same board is feasible as a software operation,
subject to the full channel budget, but leaves them dynamically disconnected.
Adding arbitrary cross-terms changes their domains and invalidates the old
physical proofs. Neither operation supplies the requested unification.

## Executed final coupling countercontrol

This review tested the simplest geometry-to-packet addition against the actual
twelve-channel source fixture. On the L=11, two-microtick prepared chart, add
the onsite term `u_packet0 += 3*b_geometry8` to the existing immutable tensor.
This is a test-only tensor constructed in memory; production code was not
changed. Its channel count remains 12, degree remains three, and strict
physical support has zero violations. Exact inverse still recovers the seed.

Nevertheless, after one actual Engine step, all 1,331 values of that packet
rail leave the Boolean domain: the modified values range from 954 to 968.
The reason is exact: adding `3*g` to u adds `g` to the quotient and therefore
to the next packet value while keeping the carry unchanged. The existing
Boolean collision/source interpretation is lost. This is a concrete rejected
coupling attempt, not a no-go theorem for other reciprocal constructions.

Reproduction uses `geometry.prepare_fixture(L=11, steps=2)`, copies its tensor
monomials, adds `(0, 3, [(8, (0, 0, 0), 'b')])`, constructs a strict-support
`Tensor`, and compares one `Engine.step` and `inverse_step`. No solver,
projection, reset or hidden callback participates.

## Bursts and complexity

Nine focused tests passed using:

```sh
python -m unittest universe24.tests.test_local_unification_limits universe24.tests.test_system_burst_growth -v
```

These preserve the free-streaming and packet-clock obstructions, exact
recurrence, complete-history guards and failed structural-growth result.
The complete ring preparation scan has recurring activity but zero growth
passes. A periodic activity peak is not an identified cosmological bang.

There is an additional readout limit. `selection.complexity.structure_trace`
counts distinct nonuniform length-three motifs of two Boolean carrier rails,
with each counted motif repeated at least twice. There are four possible
carrier labels and at most `4^3 - 4 = 60` nonuniform motifs. Its score is
therefore bounded by `min(60, floor(N/2))`. Enlarging the board alone cannot
make this particular score grow without bound. Keep its historical verdict
unchanged, and use a separately preregistered scalable or multiscale measure
for a future sustained-growth claim.

The finite-state recurrence argument applies to the prepared Boolean packet
projection. It does not show that the full twelve-channel state is finite:
its geometry integers can grow. Nor does it exclude growing organization
under every possible unbounded-integer Rule3 law.

## Next decisive same-law experiment

Start from the twelve-channel source/record history and define one new
reciprocal interaction with an explicit invariant domain before compiling it.
The first milestone is a retained geometry-sensitive clock or material
interaction with complete source accounts. A passive counter or added decoder
does not meet it. All workspace, link data and clock histories must count
inside the same 48-channel allocation.

The existing constant-profile intervention gives a sharp acceptance test.
Shift both histories of each of the four geometry profile channels by C,
keeping the complete packet state equal. The current law leaves all packet
records equal while the safe-chart radius becomes R+4C and the fixed-position
proper-time rate changes from `sqrt(2)*R^(-1/4)` accordingly. A proposed
geometry-sensitive apparatus must predict its changed operational response,
with its retained size, calibration and energy/source effects declared. It
must also pass a disconnected-interaction control and full inverse replay.

Only after that interaction has a source/constraint proof should the same
tensor be tested for repeated encounters, finite resource reuse and
longer-lived structure. Predeclare preparations, burst meaning, scalable
structure and functional-persistence measures, fixed physical horizons and
all failure/insufficient-history outcomes. Compare several resolutions and
include changed-carry, wrong-source, exhausted-supply and rotated/off-axis
controls. No current result passes this full experiment; it remains research
in the single central agenda.
