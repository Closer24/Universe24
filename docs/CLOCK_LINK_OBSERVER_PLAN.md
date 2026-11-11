# From the whole board to local clock links and observer records

The first construction is implemented: the existing coupled 44-channel
carrier drives four reversible local phase-intensity records in **one
48-channel bundle**, through the unchanged Engine, saved trace and decoder.
The apparatus history changes whether an arithmetic event is present.
It does not yet select a physical outcome or drive increasing structure.

Coordination: [#45](https://github.com/Closer24/Universe24/issues/45), with
the allocation contract in [#40](https://github.com/Closer24/Universe24/issues/40)
and material-clock requirements in [#41](https://github.com/Closer24/Universe24/issues/41).
Main source is `4c494c1188f70eb8a677bf59765cc6e8571c6b88`; the existing
compatibility adapter imports the explicitly pinned 44-channel law
`49b896c795203914a939e465d6d39e5b99343259`. The projective law in #47 has a
different normalization/readout and is not silently substituted here.

## The staged plan and what was checked

| Stage | Concrete construction or test | Result in this patch |
| --- | --- | --- |
| 1. Board and clocks | Treat the board as one autonomous retained state; use its existing two-component carrier for local phase relations. Keep update count outside the tensor. | Implemented relational ports; no proper-time calibration claimed. |
| 2. Clock connections | Preserve signs in adjacent carrier dot/cross correlations and coherent sums. | Exact signed identities and three-axis interference pass in the prepared fixed gauge. Independent local gauge covariance fails. |
| 3. Observer inside the board | Add four complete `(a,b,r)` response channels; all outputs read the same old snapshot. | 48 channels, strict face support, exact complete inverse and unchanged source44 projection. |
| 4. Clicks as observations | Read canonical records with a declared complete-window protocol, keeping missing/single/multiple records and quotient weights separate. | Records-only incremental/offline parity and passivity pass. Positive intensity can be invisible to this observation. |
| 5. Complexity and measurement | Apply the preregistered structural controls and full two-detector calibration trials. | No qualifying burst growth; one-way apparatus cannot select carrier structure. Binary Born frequencies and exclusive outcome gates fail. |
| 6. Independent acceptance | Scalar oracle, all carries, signed/big integers, causal cones, raw saved controls and complete replay. | Mechanical checks pass; physical gates keep their individual failures and blockers. |

The six work packages were algebra, phase-link integration, observer protocol,
complexity, Born/Bell, and independent review. Their reports and peer corrections
are linked below and posted in #45. Reproduction is a single command after the
existing pinned-source import; no installed runtime selector was introduced.

## Exact connection to the board

Let the existing charged carrier be `z_v = phi_v + i chi_v`. For a face neighbor w,

\[
C_{vw}=\phi_v\phi_w+\chi_v\chi_w,\qquad
S_{vw}=\phi_v\chi_w-\chi_v\phi_w,
\]
\[
C_{vw}^2+S_{vw}^2=|z_v|^2|z_w|^2,\qquad
|z_v+z_w|^2=|z_v|^2+|z_w|^2+2C_{vw}.
\]

The four apparatus inputs are `F0=|z_v|²` and
`Fk=|z_v+z_(v+e_k)|²` for x/y/z. Each uses `u=3F`. The unchanged fixed-six law
then gives exactly

\[
(a,b,r)\mapsto(b,F-a,r),\qquad \ell=F.
\]

The 44 source channels remain untouched. The four new channels retain 12
additional integers per node, so all state totals **144 integers per node**.
Every new monomial is quadratic and supported on one face edge or its target.
The combined tensor has degree at most three because its original source law
does. The base supplies the only declared geometric authority; the recorders
are one-way test apparatus with no supplied stress or backreaction.

The stored value `b` is not an instantaneous intensity. Its quotient readout
uses a transition, `ell=after.b+before.a`. All source and apparatus histories
remain recoverable. Bare adjacent charged phases are compared in a declared
fixed gauge: a physical comparison still needs gauge-covariant transport and
material-clock calibration to the same metric.

## Measured results and decisive failures

The integrated run covers 27 nodes and three updates. Its tensor fingerprint is
`094bb4edbe243e4f7654073e64688ebc7b56d951724a21a0f3af1526153df611`;
the complete final bundle is
`f15c3c342d4a9ee807640fcd6357996a1c878cb43e448f8371e3a6b6b662fad9`.

- **324 exact intensity/quotient comparisons** and 18 phase/axis/seam controls
  pass. Twenty saved control trajectories are independently reloaded, evolved
  and rewound. The complete source44 projection remains identical.
- **314 apparatus records** are observed. All are C0, since these four inputs
  preserve the remainder. Peak complete-state bit lengths are 3 at the seed,
  then 6, 12 and 25. Arbitrary-integer stress tests are separate preparations.
- Matched detector histories yield event-presence sequences `[1,1,1]` and
  `[0,0,1]` for the same input quotients `[2,2,530]`. A stationary triple can
  suppress a positive-intensity event. This is retained-state dependence of
  observation, not stochastic outcome selection.
- The records-only protocol covers 81 complete node/update bins. All contain
  multiple apparatus ports. Those bins are not physical emissions; the
  independent two-detector calibration below tests exclusivity separately.
- In 36 complete calibration trials with intensities 9:1, both detectors
  register in every trial: binary counts are 36:36, while quotient sums are
  324:36. Squared-amplitude **weights** work; a one-winner Born law does not.
  Seven preparations give 252 full trials. All 258 saved transitions, including
  four phase and two indistinguishability controls, pass independent scalar,
  inverse and canonical-stream replay.
- Two allowed preparations with intensity ratios 10:2 and 2:10 produce the
  same empty four-receiver stream over the declared one-update window. A
  decoder receiving only that stream and the same static protocol cannot
  infer which ratio occurred. This scoped impossibility can be escaped only
  by changing the preparation domain, data available, window or dynamics.
- The preregistered persistent phase-motif score is `[0,0,0,0]`; record counts
  are `[100,107,107]`, with no strict interior peak. The four-episode growth
  gate is blocked. Periodic controls correctly fail growth. Frozen random
  fields can score above an organized stripe, so this proxy is not a universal
  measure of meaningful complexity; that failure was retained.

The independent acceptance audit checks 58,320 retained integer comparisons,
84,672 outside-cone comparisons and 21 complete-bank perturbations. It checks
all remainder classes and stress values reaching 313 bits, as well as full
saved-run replay. These counts are scoped mechanical evidence, not proofs of
Einstein convergence, clock universality or a physical probability measure.

## Why the next change must affect dynamics

There are **zero apparatus-to-source terms**. For two complete seeds with the
same original44 state, induction on updates proves that their original44
trajectories remain identical regardless of apparatus history. Therefore this
particular recorder cannot favor a future carrier structure. A more elaborate
passive observer or a global complexity score cannot repair that missing
causal interaction.

The next proposed patch must replace or reuse the four apparatus slots,
not append more state. Its acceptance sequence is explicit:

1. **Material phase reference and pointer.** Declare retained oscillator and
   pointer variables and their reciprocal local interaction, with all previous
   values and carries counted. Specify the valid preparation sector and source
   stress/charge accounting before integration. The algebra report sketches
   a four-slot port; it is an unimplemented proposal, not a proven physical law.
2. **Causal history effect on structure.** Hold the complete current source
   fixed and change only retained apparatus history. Require a later change
   in carrier phase structure inside its causal cone; a disconnected-law
   control must remove it. Preserve all existing source/constraint failures.
3. **One recorded alternative per declared trial.** Build a retained pointer
   with an operational ready/recorded protocol. Losing alternatives cannot be
   discarded from the full state. Nondetection and double outcomes remain in
   the denominator. Prove any bounded sector used for a local comparison.
4. **Derive the probability measure.** State the distribution of complete
   preparations and explain why it is stable/physical. Check held-out phase,
   intensity and scale cases against `I_i/sum(I)`. A normalized weighted
   decoder, hidden ticket or appended sampler is not this derivation.
5. **Reconnect to geometry and structural recurrence.** Compare independently
   generated ticks with the same metric at fixed physical endpoints, include
   backreaction or a controlled approximation, then test finite-window burst
   growth with the preregistered controls. More bits or more elapsed updates
   do not count as structure. The current motif score is bounded, so it cannot
   establish indefinite growth on a fixed finite lattice.
6. **Bell is a separate protocol.** Supply source preparation, two analyzer
   settings, complete trials and stated independence/locality assumptions.
   A shared past clock and local stochastic response do not by themselves
   evade the factorization bound. The exact local control checks 6,561 response
   grids with maximum CHSH 2; it is not an Engine Bell experiment.

The first compiler feasibility check already finds a concrete obstacle in the
four-slot reference/pointer sketch. Its reciprocal force ports can compile
within 48 under compatible staggered phases, but the double-well pointer
potential contributes a fourth-degree energy term to the Einstein source.
The existing degree-three compiler rejects it. A complete coupled successor
therefore needs a proved degree-lowering encoding with spare capacity, a
different apparatus potential, or an explicitly limited test approximation.
The symbolic Hamiltonian is not a ready integrated model. The detailed
phase-assignment and degree check is in the algebra report.

Complexity can influence the evolution that produces amplitudes before
measurement. Weighting already determined positive intensities by unequal
outcome-dependent complexity factors changes the Born ratio: 9:1 weighted
by 2:1 becomes 18:1. A proposal must establish which role complexity plays,
then test it, rather than treating the two operations as equivalent.

## Reproduction and evidence

```bash
python -m validation.team48_contract --source /path/to/clean/pinned49b896c --out runs/team48-contract
python -m validation.clock_links.run_audits --base-bundle runs/team48-contract/run/bundle --out runs/clock-links
python -m unittest discover -s universe24/tests -t . -v
python -m validation.system_smoke --out runs/system-smoke
python -m universe24 verify --run runs/system-smoke/run
```

The combined collector rejects mixed tensor/bundle/run identities and stale
source hashes. It records the individual reports, their hashes and separate
physical statuses. CI uploads complete tensors, seeds, traces, calibration
trials and protocols. The checked summary is
[`evidence/clock_link_observer.json`](evidence/clock_link_observer.json).

Local validation on the final code: **305 repository tests passed**, all six
audits completed, 21 recorded code hashes matched, and the generic CLI
forward/replay smoke passed. Scientific failure statuses above are unchanged.

Detailed reports:
[algebra](research/clock_links/01-algebra.md),
[links](research/clock_links/02-links.md),
[observer](research/clock_links/03-observer.md),
[complexity](research/clock_links/04-complexity.md),
[Born/Bell](research/clock_links/05-born-bell.md),
[independent review](research/clock_links/06-acceptance.md).
