# Reciprocal carrier and apparatus in the corrected massive model

The previous four-record construction was one-way: apparatus history could
change event presence but could not change future carrier structure. This
proposal adds an actual reciprocal interaction to the corrected full-frame
equations from PR #50. It explicitly sets carrier mass squared to one; the old
`build45()` default was massless, and the protected triangular 44-channel clock
test used another tensor. Neither result is silently imported.

The constructive result is a **47-channel homogeneous-source proposal**, leaving
one slot for a separately labelled mechanical record. The two new apparatus
fields exchange energy with the existing charged scalar and source the same
geometry. A retained apparatus momentum intervention changes subsequent carrier
positions; the matched disconnected control removes this effect. Generic
inhomogeneous apparatus stress and momentum accounting remain incomplete.

## Equations and channel ledger

Use the existing synchronous normal frame, its unit lapse, spatial frame and
extrinsic curvature, with `K=K00+K11+K22`. Put

\[
I=\phi^2+\chi^2,\qquad
W(q,I)=\tfrac12\omega^2q^2+gqI.
\]

The sole new matter equations and changes to the old carrier equations are

\[
\dot q=p,\quad \dot p=Kp-\omega^2q-gI,
\qquad\Delta\dot\Pi_\phi=-2gq\phi,\quad
\Delta\dot\Pi_\chi=-2gq\chi.
\]

The apparatus is neutral. Its homogeneous source is

\[
\rho_a=\tfrac12p^2+W,\quad
S^a_{ij}=(\tfrac12p^2-W)\delta_{ij},\quad j^a_i=0.
\]

In the existing source convention this adds `-W` to every diagonal `Kdot` and
`-2 rho_a` to the Hamiltonian constraint. The tensor is compiled from these
equations, including the cubic interaction energy in the geometry source.
There is no external force callback, reset, clipping or imposed source history.
The two new fields use the same retained denominator as all existing fields.

| Retained component | Channels | Meaning |
| --- | ---: | --- |
| Corrected full-frame geometry, massive charged scalar, dust, Maxwell and projective denominator | 45 | Exact #50 equations with explicit mass parameter |
| `projective.apparatus_q`, `projective.apparatus_p` | 2 | Neutral homogeneous receiver and momentum |
| Optional native audit record in the pointer experiment | 1 | Raw integer memory; no supplied physical stress |
| Total with that record | 48 | 144 retained integers per node |

The sourced 47-channel tensor has **909 terms**, maximum degree three and strict
face support. It has no old-`a` inputs and preserves all six legal remainders.
The ordinary fixed-six Engine and complete `(a,b,r)` inverse remain unchanged.
Current physical fields are read as `P_current/D_current`; `D_old=0` in preparation
is retained arithmetic boundary memory, not a physical earlier geometry. Any
native record driven by `Pq` records a numerator, not a normalized physical
amplitude. No use of an after-snapshot denominator is justified for a
before-snapshot writer.

## Source identities and the explicit limitations

The code independently expands the homogeneous identity

\[
\dot\rho_a=Kp^2+gq\dot I.
\]

The new carrier force contributes `-gq Idot`, so interaction power cancels in the
combined continuum energy equation. Likewise
`phi Delta(Pi_chi_dot)-chi Delta(Pi_phi_dot)=0`. No new electric charge or current
is inserted into Maxwell/Gauss: the neutral interaction is invariant under
rotation of the two charged carrier components. These are algebraic identities;
they do not assert exact finite-step energy conservation or lattice local-gauge
invariance of the entire existing discretization.

The receiver has no retained spatial gradients. Its source is physically
asserted only for homogeneous normal-frame data. Generic spatial momentum balance
fails already in a flat diagnostic: set the carrier and `q` to zero, `p=1`, and
`partial_x p=1`. The displayed apparatus pressure has gradient one, while its
momentum density and momentum evolution are both absent. A covariant real scalar
receiver in this first-order representation would require three gradients, making
50 channels before adding the record, or 51 with it. An alternative encoding
would need its own proof. The local intervention runs below are therefore
equation/locality probes with disclosed physical defects, not moving detectors.

The potential also lacks a global lower bound. Eliminating the receiver gives

\[
q_*=-gI/\omega^2,\qquad W(q_*,I)=-g^2 I^2/(2\omega^2).
\]

For `m²=omega²=1`, `g=1/4`, `phi=8`, `chi=0`, `q=-16`, even the combined carrier
and apparatus potential is `-96`. The sufficient nonnegative-potential domain
`m²/2+gq>=0` is checked on the reported trajectory; it is not proved invariant.
The massless control leaves this domain. The construction removes the previous
quartic Einstein-source compiler obstruction by choosing a quadratic receiver
and cubic interaction; it does not replace it with a stability theorem.

## Prepared tests and observed response

The default exact homogeneous initial data are `B=identity`, `G=0`, `phi=1/2`,
`chi=Pi=Xi=dust=E=M=A=q=0`, `p=+1/4` or `-1/4`, and
`Kdiag=(-4,-4,-3)/16`. Both signs have identical carrier/geometry data and identical
initial source stress. Their `rho=5/32`, `det B=1`, and all Hamiltonian, momentum
and Gauss constraints are exactly zero. This is a retained apparatus momentum
intervention; it does not pretend that the complete current apparatus states
are identical. Parameters are `dt=1/32`, `dx=1`, `m²=omega²=1`, `g=1/4`.

Four updates on 27 nodes give the following paired results:

| Pair | First carrier momentum difference | First carrier position difference | Disconnected `g=0` source difference |
| --- | --- | --- | --- |
| Homogeneous apparatus momentum signs | Update 2 | Update 3 | None in all four updates |
| One-site momentum flip on a declared phase texture | Update 2 | Update 3 | None in all four updates |

The second preparation has nonuniform carrier phase and supplied discrete scalar
gradients, but is not advertised as constrained Einstein data. It allows the
separate complexity audit to assess phase structure instead of treating growing
numbers as complexity. Reciprocal response alone is not a preference for greater
structure or growth between bursts.

Every state is compared to the independent scalar oracle, all six carries are
present, and all four updates rewind exactly. Maximum retained size is 806 bits.
The zero-source physical state stays flat and exactly constant in physical
ratios. A separate massless control has a distinct tensor and preserves its
negative effective-potential-domain result. No complete material-clock period,
redshift, off-axis moving apparatus, Born selection or Bell experiment is claimed.

The homogeneous Hamiltonian defect starts at zero but reaches approximately
`-0.00125866` and `-0.00111114` in the two connected histories. Their final frame
determinants are approximately `0.91787234` and `0.91788273`. This finite constraint
drift is retained as a failure, despite exact information recovery. The textured
run's sampled final H defects are about `0.04579`; those seeds never passed the
initial homogeneous physical gate. Decimal values here are presentation-only
approximations to saved exact rational diagnostics.

## Source isolation and reproduction

Reference equations are pinned to commit
`62202fdccdd9a40d5dbbec104de6f97d9587a999`. The exporter requires that exact Git
HEAD and a clean tracked checkout. It loads reference code only in an isolated
Python subprocess, saving immutable tensor, complete seed, ownership, protocol
and every expected state. The current main runtime then imports those ordinary
data and compares every complete transition to the reference. Reference code is
not imported into the current runtime and cannot provide callbacks to it.

```bash
python -m validation.selection.coupled \
  --reference /path/to/exact-pr50-checkout \
  --out runs/selection/coupled-final
```

The connected 47-channel tensor hash is
`53e16d2f6ec111b43c968d507be4f954decaf93d78a5ff73c6b6de7dabefe243`.
Saved controls include eight matched intervention trajectories plus zero-source
and massless cases. The ordinary bundle/trace replay path checks current-engine
agreement; the reports preserve source hashes, bit growth and failed physical
gates. The optional 48th pointer and any raw pointer-feedback perturbation have
their own hashes and scope in lane 3; neither inherits homogeneous source
accounting merely by being appended.

## Primary-paper review and what transfers

Lin and Hu, [gr-qc/0611062](https://arxiv.org/pdf/gr-qc/0611062), section II,
equation (6), formulate a harmonic oscillator and scalar field from a joint
action. Their nonperturbative analysis motivates retaining reciprocal dynamics
and checking the limits of detector interpretations. Their quantum state,
prescribed trajectory, linear coupling and renormalization are not our integer
system, so none of their detector-temperature or entanglement results is claimed
here.

Sachs, Mann and Martín-Martínez,
[arXiv:1704.08263](https://arxiv.org/pdf/1704.08263), section II equations (3)–(5),
study a detector coupled to a normal-ordered field square. This supports studying
an intensity-like interaction as a candidate, while their multi-detector
divergences show that writing a quadratic response does not itself establish a
well-defined quantum detector. Here `gqI` is a classical polynomial proposal;
normal ordering, vacuum correlations, quantum outcome probabilities and an
emergent Born law are absent.
