# Independent review of the clock-selection study

Date: 2026-11-08. Baseline commit:
`ff89e2ff661c8b60af84aff738f9040ad7f15bcc`.

The independent auditor reconstructed preparations and coupling routes with the
existing exact-matrix reference, then compared every recorded complete state
against both forward and inverse evolution. Every channel and remainder was
retained. Full backward traversal recovered every initial preparation. These
are finite computational checks, separate from the mathematical inverse proof.
No engine or Presenter source was changed by this reviewer.

## Verified captures

| Study | Complete recordings | Full states | Forward/inverse transitions | Independently supported conclusion |
| --- | ---: | ---: | ---: | --- |
| WRITE→PROBE V1 | 68 | 5,220 | 5,152 | No accepted gate; retained inactive-writer remainder footprint invalidates the probe-only input control. |
| WRITE→PROBE V2 | 260 | 22,820 | 22,560 | Four registered carrier-and-C discriminators: phase0, gaps36/38, sides337/353. |
| Local-region mediation | 16 | 784 | 768 | Four complete groups pass; the output follows the selected 336-triple local region across both selected exterior histories. |
| Short periodic return | 20 | 2,860 | 2,840 | Six continuous one-lap returns; zero strict clock-conditioned gates. |
| Long periodic return | 8 | 13,128 | 13,120 | No later joint-template reappearance or accepted gate through 32 registered return opportunities. |
| Signal–cluster structure | 36 | 1,764 | 1,728 | Two finite region reconfigurations; zero registered separated-product outcomes after observer correction. |
| Parallel integer division | 90 | 1,170 | 1,080 | All first-step predictions, 13 cross-size comparisons, full Q balances and causal bounds verified. |
| Total captured records audited | 498 | 47,746 | 47,248 | Counts are recordings, not independent statistical samples or distinct scientific mechanisms. |

The following certificates contain exact protocol/source identities, per-record
checks and assessments:

- [V1](evidence/independent_audit/write_probe_v1_verified.json)
- [V2](evidence/independent_audit/write_probe_v2.json)
- [Mediation](evidence/independent_audit/clock_region_mediation.json)
- [Short recurrence](evidence/independent_audit/recurrence_v1.json)
- [Long recurrence](evidence/independent_audit/recurrence_long_v1.json)
- [Structure](evidence/independent_audit/structure_v1.json)
- [Division](evidence/independent_audit/parallel_division_v1.json)

The separate 64-case orthogonal preparation preflight involved no evolution.
Its complete initial states and source masks also matched independent
reconstruction; see [its certificate](evidence/independent_audit/orthogonal_preflight_v1.json).

## What the positive gate result establishes

V2 repairs the V1 source-control defect by removing an absent source's entire
declared footprint and restoring the predefined guide/background there. The
change belongs to a new frozen protocol; it does not retrospectively rescue V1.
The V2 input, hold, carrier and raw-C windows remain fixed across every control.

The mediation study makes new initial boards from complete state40 anchors.
It independently crosses the seven-node/all48-channel region with either
exterior history. All eight diagonal preparations reproduce all49 parent suffix
states exactly. Both off-diagonal crosses preserve the registered incoming
tests and initial four-step isolated hold. Exact carrier and raw-C outcomes
follow the region selection in every registered case.

This establishes finite causal mediation by the retained local region across
these two exteriors and two gap values. The near-input predicate intentionally
excludes the fixed region nodes, and the intervention is an offline initial
preparation. The result is not proof of arbitrary-context component robustness,
an autonomously created probe, repeated trial generation, preference for
complexity, a photon, quantum collapse or a unique physical time direction.

## Defects, negative outcomes and corrections retained

The structural observer reused the name `pairs` for two different lists. Its
class-coexistence rows overwrote the actual separated-product pairs, creating
false product classifications when a parent template disappeared. Independent
reconstruction found no registered isolated products. The original source,
native captures and erroneous assessment remain available. A separate passive
correction changes only the two faulty observation fields and their downstream
assessment; all other observations and every native record match the original.
See the [correction check](evidence/structure_v1_analysis/independent_correction_check.json)
and [preserved-source check](evidence/independent_audit/structure_source_check.json).
The genuine structural positive is phase2/delay7 region reconfiguration on both
sizes, with complete isolated periodic-region checks. This is not mechanical
binding or dissociation.

The initial V1 producer attempt stopped before trajectories because a source
snapshot named a nonexistent file. The initial long-recurrence capture also
stopped before trajectories because its inherited frame limit was too small.
The structural capture-limit correction retained 20 earlier records and checked
980 overlapping full states for exact equality. These execution corrections
did not alter scientific acceptance definitions.

The first V1 auditor attempt incorrectly hashed numeric counters instead of the
native format's decimal strings. Its zero-record failure and executed source
were preserved; the successful auditor corrects only that encoding. A
large-integer regression test covers this distinction.

The short L50/L54 joint preparations are complete closed orbits with periods
dividing50/54, so a longer run cannot discover a new state on those same orbits.
The [independent period check](evidence/recurrence_period_diagnostic/independent_check.json)
uses direct full-state equality on all20 records. In the long L48/L52 studies,
packet-only controls close at periods1200/1404; joint cases do not repeat within
their recorded horizons1576/1704. A finite absence of repeats does not exclude
a later repeat. No later joint +X template reappears within the registered
all-frame/all-X scan.

## Mathematical and physical claim review

The following derivations were checked independently: exact guarded
`Ck = u mod3`; remainder change alone is not a C event; the four-step global
zero-quotient recurrence obstruction; local/global algebraic account balances;
parity spectator sectors; complete pair period5 and isolated period4 templates;
and the accumulated quotient/input bound from retained remainders.

The b3 counterexample is now also a full native finite demonstration: one
initial donor emits six simultaneous C0 events at six distinct recipients.
Therefore C0 alone does not select one route. Event class is also nonmonotonic
in the number of unit donors. These results constrain a proposed approval
mechanism without prohibiting a separately demonstrated state-dependent gate.

The fixed-rational-coefficient document is a separate, unimplemented candidate.
Its declared inverse, gcd spectator sectors, weighted-account condition and
gain bound check algebraically. Its coefficients are attached to lattice
addresses; they do not define transported mass. None of its state-domain or
rule changes was used in the audited baseline studies.

The electronic-binding, charge/EM, strong, weak, gravity and mass-family notes
separate established physical targets from proposed board gates. In particular,
chemical binding is electromagnetic, charge is a property, raw Q is not already
physical charge or energy, a clock phase shift is not a frequency shift, and a
frequency gap is not calibrated mass. Representative primary-source abstract
checks confirmed the limited descriptions of MICROSCOPE, MuLan, QCD string
breaking, the XENONnT charge-nonconservation analysis and hydrogen QED. This is
a claim-scope review and source spot-check, not a derivation of those physical
phenomena from Rule3.

## Regression verification and next decision

Eight reviewer-owned tests passed, including hidden-channel remainder rejection,
invalid input controls despite favorable joint outputs, arbitrary-size native
hashes, exact complete pair period5, and six-way C0 fanout:

```sh
python -m unittest tests.test_clock_selection_audit tests.test_clock_selection_oracle -v
```

The next scientifically discriminating question is whether an admissible
autonomous assembly can produce a later probe/trial and a durable internally
readable record without an externally preloaded schedule being mistaken for
computed approval. Its acceptance must additionally test repeated operation
and interactions with new component contexts. The present verified gate is a
useful constituent; the claimed preferred-complexity selection mechanism is
still unestablished. Presenter visual behavior is tested separately by the
implementation team, not certified by the numerical audits above.
