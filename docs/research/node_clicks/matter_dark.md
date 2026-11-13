# Matter and dark-sector controls in the current phase law

`validation/matter_dark_audit.py` runs six complete preparations through one
unchanged 384-term phase tensor. Every bundle has 48 node channels, 144
retained integers per node, degree at most three, one-face support, exact
2O covariance, and the normal saved-run/replay interface. No ordinary-matter
or dark-matter species is assigned by a channel name.

The saved click observer accepts only canonical click records. Full-state
optical, contrast and localization diagnostics are separately identified as
latent audits. They never modify evolution or enter the click-only observer.
An arithmetic click is an available observation, not a particle identity.

## A structural obstruction in the phase tensor

For central partners `g,-g`, define the diagnostic pair sum and difference

\[
p=b_g+b_{-g},\qquad q=b_g-b_{-g}.
\]

The current phase law is

\[
u_g=3[b_{-g}+b_{g,+}+q^2(b_{g,-}-b_{g,+})].
\]

All coefficients are divisible by three, so every legal remainder is retained
and Rule3 gives the exact difference equation

\[
q_{t+1}=-q_t+q_{t,+}+q_t^2(q_{t,-}-q_{t,+})-q_{t-1}.
\]

It contains no pair sum `p`. Optical amplitudes cannot source the contrast
in this tensor, even though contrast can change their propagation. This is
an algebraic one-way-coupling result, not merely an untested possibility.
The audit checks matched light/no-light preparations with identical complete
contrast histories.

Every target polynomial also reads only its own central partner pair and
its own propagation axis. There are 24 independent partner-pair blocks and
no cross-pair or transverse interaction terms. The audit checks this directly
on all polynomial factors. Exact 2O covariance is compatible with this
factorization; symmetry alone does not provide binding, collisions, a
stress-energy source or gravitational response.

## Registered preparations and physical meanings

All six cases use `L=5` and the same tensor and observer protocol.

| Case | Preparation and purpose |
| --- | --- |
| `vacuum` | Constant positive `a=b=32`, remainder 1: fixed-state, no-click control |
| `clock` | Homogeneous central four-cycle and uniform pair-sum drift, no optical profile |
| `clock-light` | Same clock plus a transverse plane profile; compare optical evolution with contrast history |
| `local-contrast` | Clock background plus `+1,-1` in one partner pair at one node, preserving its initial pair sum |
| `local-contrast-light` | Exactly the same local contrast perturbation plus the same plane profile |
| `local-pulse` | A point profile added equally to both channels and both histories of one pair |

The homogeneous clock and localized contrast controls have zero decoded
`E,B`, yet their evolving integer state can emit arithmetic clicks. This
establishes electromagnetic darkness **of this readout** and internal
activity. It does not establish invisible gravitating matter.

The local common pulse translates by `ceil(t/2)` nodes rather than staying
at rest. A point profile also gives nonzero centered divergence of its
electric readout. Thus a localized amplitude is not automatically either
an ordinary rest particle or a source-free Maxwell photon. The installed
plane-wave sector avoids that particular divergence issue by its declared
transverse preparation.

The local contrast is a negative stability control. Its optical cancellation
does not prevent rapid contrast growth and eventual negative retained
integers. Larger positive background offsets can postpone some positivity
failures but do not derive a mass, a conserved physical energy or stable
localized dynamics.

## What the installed memory component changes

Current main also contains `universe24/detection.py` and the documented
`light-memory48` preparation. Its 624-term tensor can exchange a transported
amplitude with stationary retained memory, with a conserved dimensionless
quadratic account. It uses a different tensor from the phase law above.

The memory is not already a massive material body: its source documentation
leaves energy-frequency calibration, material clocks, recoil stress and
Einstein backreaction open. A record that persists until an internal arming
pulse revisits it is useful detector machinery; that alone does not establish
ordinary-matter or dark-matter dynamics. Successes from these two distinct
tensors cannot be added together as a single-law physical acceptance result.

Earlier six/eight-channel homogeneous sourced models and massive spinor
constructions are separately pinned historical research. They are not the
current regular-48 phase tensor and cannot supply missing mass/source claims
through naming, padding or reinterpretation of their old evidence.

## Required coupling and observation gates

1. A proposed matter sector needs a declared positive rest-energy or
   dispersion relation, a stable localized or otherwise justified matter
   state, and measured response/recoil under interactions. One tested moving
   point pulse fails the declared stationary-rest control; it is not a
   no-go theorem for all future constructions.
2. A dark-sector candidate needs gravitational stress/source and clustering
   evidence in the same law and metric, in addition to suppressed direct
   electromagnetic response. For a cold-dark-matter interpretation, low
   velocity/pressure at the relevant scale must also be derived.
3. The phase tensor needs interactions beyond its current independent axial
   blocks if it is to supply general scattering and reciprocal geometry.
   A fixed polynomial can have state-dependent effective couplings, but the
   current `q` equation proves that its optical source channel is absent.
4. A click-only classifier must be calibrated against a retained apparatus
   and controls. Zero `E,B` is available to the latent audit; it is not an
   extra observable secretly handed to the observer. The same arithmetic
   click class may be produced by a clock, a traveling profile or an unstable
   contrast, so C0/C1/C2 labels alone do not identify species.

The [Particle Data Group dark-matter review (2026, revised August 2025)](https://pdg.lbl.gov/2026/reviews/rpp2026-rev-dark-matter.pdf)
grounds the distinction: dark-matter evidence includes gravitational mass
tracers and structure formation, while the cold interpretation concerns a
nonrelativistic, approximately pressureless component. Optical cancellation
in a chosen channel readout supplies neither of those checks.

## Reproduction

```bash
python -m validation.matter_dark_audit --out runs/new-matter-dark-audit
```

The registered horizon is eight steps for vacuum, homogeneous clock,
clock-plus-light and local common pulse, and four steps for each localized
contrast case: **six runs and forty forward updates**. Every saved step is
compared to the independent pair-force oracle; the first two steps of each
case also use the scalar monomial oracle. Saved replay, every inverse step
and full rewind are checked, including negative-control states.

Source hashes cover all actual evolution and observation dependencies and
must remain unchanged during collection. Fresh evidence is written to
`runs/matter-dark-audit-20261113/results.json`. Each result separates the
click-only `observer` from `latent_audit`, reports bit growth and the first
nonpositive retained value, and retains failed/not-tested/blocked gates.

The completed collection passes full replay, inverse, rewind, every force
oracle comparison and the first-two-step scalar comparisons for all six
cases. Its common tensor hash is
`0d9a9a329b36cd43d388364d041fa6e32b6f963ed12e38698218883a6bb15116`.

| Case | Canonical clicks | Maximum retained bits | First nonpositive value |
| --- | ---: | ---: | --- |
| Vacuum | 0 | 6 | None |
| Clock without light | 36,000 | 6 | None |
| Clock with light | 36,200 | 6 | None |
| Local contrast without light | 18,007 | 27 | Tick 3: `-325` |
| Local contrast with light | 18,103 | 31 | Tick 3: `-69` |
| Local common pulse | 36,004 | 6 | None |

All emitted events are C0: the tensor retains all remainders. The local
contrast reaches maximum absolute value `206210319` after four updates,
identically with and without the optical pulse. Without the optical pulse
its `E,B` remain exactly zero; with the pulse it changes optical evolution.
The point common pulse has two nonzero centered-divergence nodes in each of
its electric and magnetic readouts throughout its exact move/hold motion.

These results pass internal optical-darkness and activity checks, fail the
tested localized natural-domain and stationary-rest controls, and leave
ordinary-matter and dark-matter physical acceptance **blocked**. Positive
rest mass, coldness, gravitational sourcing and clustering are **not tested**,
not declared to have failed an experiment that was never performed.
