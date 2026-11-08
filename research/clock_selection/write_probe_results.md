# Sequential writer–probe experiments

These are finite computational results, independently checked against the
saved full states. They do not establish preferred-route selection, autonomous
search, a physical photon or quantum collapse. The engine, scalar Rule3,
48-channel node, six spatial neighbors and fixed +++ coupling are unchanged.
All packets and the clock interface are prepared before each run.

## V1: counter-only source removal fails the input control

The frozen V1 study contains 68 complete runs: 64 encounters and four pristine
translation controls. On a side-321 cube, phases 0–3 and writer–probe spacings
32–35 were tested for 80 updates. Removing only a writer's counters left its
packet remainders in place. That retained footprint disturbed every probe-only
control. The exact later carrier in phase 1, spacing 34 therefore does **not**
qualify as an accepted conditional gate. The registered result is **0/16**.

All 68 full-state inverse checks passed, and the independent audit reproduced
5,220 states and 5,152 transitions. This negative control result remains part
of the evidence; the V1 protocol and records were not rewritten.

- Protocol: [protocol_v1.json](protocol_v1.json)
- Evidence: [write_probe_v1_run01/result.json](evidence/write_probe_v1_run01/result.json)
- Audit: [write_probe_v1_verified.json](evidence/independent_audit/write_probe_v1_verified.json)

## V2: complete absent-source controls yield four accepted gates

V2 is a new protocol. An absent input restores its complete 24-address packet
footprint, including transverse remainder halo, to the pristine guide and
background. Every triple outside that declared input footprint is unchanged.
The separate clock-off comparison removes only the center clock counters.
These are initial preparation differences; no runtime source is injected or
removed.

The registered domain is +++, sides 337 and 353, center remainder 0, phases
0–3, writer delay 2, spacings 36–39, four writer/probe masks and clock on/off.
The study records 256 encounters for 88 updates and four pristine controls.
It completed in 367.47 CPU seconds, with 26,357,171 recorded bytes and no
registered resource overrun. All 260 full inverse checks and four pristine
translation checks passed. The independent audit reproduced 22,820 states and
22,560 transitions and confirmed the registered assessments.

Only phase 0 has valid incoming-probe comparisons in all four masks: eight
clock-on groups across the two sizes and four spacings. Four of those groups
pass the complete carrier and raw-C discrimination criteria. The other
24 clock-on groups are input-ineligible. Every clock-off group has an invalid
joint incoming probe, so its apparent output differences do not establish
clock necessity.

| Writer present | Probe present | Phase 0, spacing 36 | Phase 0, spacing 38 |
|---|---|---|---|
| No | No | No exact outlet carrier/signature | No exact outlet carrier/signature |
| Yes | No | No exact outlet carrier/signature | No exact outlet carrier/signature |
| No | Yes | Exact outlet carrier and C signature | No exact outlet carrier/signature |
| Yes | Yes | No exact outlet carrier/signature | Exact outlet carrier and C signature |

This same table holds on both registered cube sizes. It describes suppression
at spacing 36 and enabling at spacing 38. It does not say that every signal or
all microscopic information disappears in the other cases.

Between the encounters, all 336 triples on the clock node and its six face
neighbors repeat after four updates throughout states 32–40. The center has
unit counter norm, the other counter pairs are zero, and every separate
external contribution into that region is zero during the hold. At state 40,
the probe-only center is `(a,b,r)=(0,1,0)` and the writer-conditioned center is
`(0,-1,0)`. The retained information in this example is **clock phase**, not a
changed center remainder or an established persistent click record.

The outlet carrier is compared against an exact 6×3×3 spatial template with
all 48 channels at four consecutive states. Its fixed outlet C window is
`T-3` through `T+4`, where `T=26+spacing`. The accepted signature consists of
C2 with quotient −1 at `T-3`, followed by C1 with quotient +1 at `T+1`, with
no other outlet C in that window. All other raw C events remain in the saved
records. These arithmetic events are not a calibrated photon detector.

- Protocol: [protocol_v2.json](protocol_v2.json)
- Complete evidence: [write_probe_v2/result.json](evidence/write_probe_v2/result.json)
- Initial-source checks: [preparation_equivalence.json](evidence/write_probe_v2/preparation_equivalence.json)
- Audit: [write_probe_v2.json](evidence/independent_audit/write_probe_v2.json)
- Presenter selections: [presenter_selection.json](evidence/write_probe_v2/presenter_selection.json)

## Independent local-state mediation test

The V2 result demonstrates a history-dependent conditional probe output. The
incoming check close to the controller excludes the seven prepared clock
nodes, and the exterior contains the departing writer history. The result
alone does not prove that only the retained clock state mediates the output.

The separately registered [clock-region mediation protocol](protocol_mediation.json)
crossed the complete state of those 336 triples and the entire exterior from
the two native histories at state 40. Each cross was a new initial preparation
run for 48 updates. The two unchanged crosses in each geometry replayed every
complete native suffix state. This is a causal test of the existing mechanism,
not a new board operation or a runtime intervention.

All 16 registered preparations passed their incoming, quiet-orbit and boundary
checks. At both cube sizes and both spacings, the exact carrier and raw-C
signature followed the retained clock-region source independently of which of
the two exteriors was used. All four geometry groups passed. The independent
audit reproduced 784 states, 768 transitions, all full inverse checks and all
eight complete native suffix comparisons. Capture used 18.30 CPU seconds and
8,804,565 recorded bytes, with no registered resource overrun.

| Retained region source | Exterior source | Spacing 36 | Spacing 38 |
|---|---|---|---|
| Probe-only history | Probe-only history | Exact carrier and C | Neither registered exact result |
| Probe-only history | Writer-and-probe history | Exact carrier and C | Neither registered exact result |
| Writer-and-probe history | Probe-only history | Neither registered exact result | Exact carrier and C |
| Writer-and-probe history | Writer-and-probe history | Neither registered exact result | Exact carrier and C |

This establishes finite causal control by the complete retained region in these
two chosen exterior states. It does not yet establish that the center counters
alone suffice, that arbitrary exteriors are irrelevant, or that the mechanism
creates its own probes or selects a globally preferred route. The original V2
writer changes the region through uninterrupted Rule3; the additional crossed
preparations test that region's causal role.

- Evidence: [clock_region_mediation/result.json](evidence/clock_region_mediation/result.json)
- Audit: [clock_region_mediation.json](evidence/independent_audit/clock_region_mediation.json)
- Presenter selections: [presenter_selection.json](evidence/clock_region_mediation/presenter_selection.json)

## Next unresolved mechanism

The next question is whether internally recurring or competing attempts can
reach this controller with valid inputs and leave a persistent internal
record. A preloaded sequence alone does not create an autonomous trial
generator. Rejected signals may disturb later probes on a shared guide, so
that effect must be measured rather than discarded or repaired during a run.
A complexity preference would additionally require a fixed independent metric
and alternatives with controlled differences; no such preference was tested
in the studies above.
