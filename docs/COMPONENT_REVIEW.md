# Independent component and research review

The generic preparation boundary passes the reviewed software checks. Its
assembly contracts do not establish arbitrary functional composition. The
strict waiting/confirmation and joined single-click retaining targets remain
unmet in their registered finite families.

The review uses the separate exact-matrix construction in
`research/reference/algebra.py`, an independent sparse gather updater and
inverse, and complete retained states. It does not use production routing
tables or the production scalar updater as its numerical oracle.

## Software boundary and preservation

The 20 independent tests in
[test_component_research_review.py](../tests/test_component_research_review.py)
cover explicit background assignments before sparsification, socket filling,
conflicting triples, duplicate independent sources, exact global tensor and
background requirements, immutable data, and rejection of runtime controls.
All 48 proper 2O lifts are checked on state, ports, source identities and
readouts; explicit wrapping and self-alias rejection are checked separately.

Generic-runner checks compare complete recordings with and without observers,
exercise exact large integers, and independently recompute C, R, input sums
and counter magnitude. C is never inferred from a remainder change alone.
The guided-packet recipe reproduces all six frozen packet trajectories.
The arm-length extension preserves the declared gate sites and moves the full
48-channel outlet metadata to the declared endpoint.

All 44 historical component experiments were reassembled through the new
library, preserving all 1,868 complete states. The historical traces were
also independently replayed for all 1,824 forward transitions and inverses.
The migration is a software equivalence result, not a new physical result.

The final repository suite contains 120 tests, including the 20 independent
review tests: 120 passed, with zero failures, errors or skips. The code writer
ran that complete suite; this reviewer inspected its explicit result and log.
The [final review report](../research/component_review/report.json) records
source hashes and checks all 61 previously pinned files: 13 core source files,
44 historical trajectory files, three delivered HTML files and the previous
scientific verification record. The core and those historical artifacts remain
unchanged. The original evidence was captured before publication; its exact
source snapshots identify those runs independently of later publication commits.

## Scientific audit scope

| Study | Independent observations | Independent full-state replay | Conclusion |
| --- | --- | --- | --- |
| Historical component corpus | Complete historical state equality | All 44 runs; 1,824 transitions | Existing results preserved |
| First waiting search | Four representative source controls | Four runs; 160 transitions | First input writes a transient record, followed by an unwanted C; reported family result is 0/64 cases |
| Matching-buffer search | Four representative source controls | Four runs; 160 transitions | Registered waiting behavior fails in the reviewed case; reported family result is 0/81 cases |
| Guided packet | All six runs and every guarded event | Six runs; 106 transitions | Exact full-state translation at L=5,17,31; separate proof covers the declared preparation at every L>=5 |
| Cooperation-score search | All 432 recordings, 18 scores and 243 comparisons | 20 selected runs; 725 transitions | All 10 eligible comparisons refute the fixed higher-score prediction |
| Fresh phase-conditioned competition | All 200 recordings, 10,600 native/portable states and 96 comparisons | 16 positive/control runs; 832 transitions | OR/NO competition confirms at the registered input and fresh lengths 8/10; no input-controlled winner reversal |
| Joined route and prepared receiver | All 16 recordings, all 48 receiver channels and every signed input term | All 16 runs; 768 transitions | Eight null controls pass; all six required source-present cases fail the single-click retaining criterion |

The two waiting searches contain 580 complete production runs in total. The
review does **not** claim an independent replay of all 580: its independently
replayed subset is eight runs, with source, protocol and reported-result checks
for the two studies.

The guided packet is compact relative to an entire prepared periodic guide.
Its transverse remainder halo is included. The local algebra and translation
induction are reviewed separately in
[packet_proof_review.md](../research/component_review/packet_proof_review.md).
This is a mathematical guided mobile pattern, not established physical light
or a waiting memory device.

The fresh competition result uses a separately frozen narrower protocol after
the original score prediction failed. The lower-score OR route wins the
registered OR/NO comparisons. The original prediction remains refuted and its
all-phase holdout gate remains closed. Neither the score nor the observer is
used to choose a state during evolution.

## Joined failure and source integrity

The joined trial contains one initially supplied central source and receivers
already prepared in their waiting state. It does not test an earlier signal
writing that state or an internally computed uniqueness approval.

In every required active case, the first receiver C occurs on time at step 12,
following actual old-step-11 input `(1,-1)`. There are then 19 C-bearing updates
at steps 12,14,...,48. The `(0,0)` remainder record first fails at step 14. In
both mixed spatial swaps, the NO receiver's entire 48-channel state stays equal
to its null baseline throughout steps 1..48. Full-state inversion preserves the
information elsewhere on the board.

The frozen field `event_in_declared_window` combines the timing condition with
the requirement of exactly one C-bearing update. Its false value therefore
does not mean that the first event was late. The independent report records
`first_C_in_window=true` explicitly. The failures are repeated events and lost
retention, not first-arrival timing.

Every run in the 200-run followup shares one exact frozen source version; all
22 archived source files match its manifest. The same check passes separately
for the 16-run joined batch. Different batches have separate snapshots; no
cross-batch identity is assumed. Specs match the manifests written before the
runs, and native checkpoint states equal the portable Presenter states.

## Presentation and limits

The code writer's final Presenter check reports 24 selected examples passing
in jsdom with native Canvas2D and explicit geometry. That is evidence for the
application's rendering logic. It does not establish browser CSS layout,
Safari/iPad playback, responsive layout, accessibility or actual pointer
interaction. A host that disables JavaScript cannot be made interactive by a
static experiment list. These UI limits are separate from the numerical audit.

No result establishes physical light, physical time, energy, quantum collapse,
an autonomous uniqueness approval, or a general preference for complexity.
The next scientific obstacle is a retained receiver response after a real
incoming signal; successful software assembly alone does not remove it.

## Evidence and reproduction

The [machine-readable review](../research/component_review/report.json) links
the preserved-source manifest and individual audits. Each audit module accepts
`--evidence` and a new `--output` path, except the final aggregation module.
For example, from the repository root:

```bash
python -m unittest discover -s tests -p test_component_research_review.py -v
python -m research.component_review.review_packet --evidence research/component_studies/confirmation_packet_evidence_v1 --output packet-review-new.json
python -m research.component_review.review_joined --evidence research/component_studies/selection_receiver_evidence_v1 --output joined-review-new.json
```

Individual reports:

- [Historical full-state oracle](../research/component_review/baseline_trace_audit.json)
- [Waiting search representative](../research/component_review/confirmation_discovery_review.json)
- [Matching-buffer representative](../research/component_review/buffer_review.json)
- [Guided packet](../research/component_review/packet_review.json)
- [Cooperation-score search](../research/component_review/selection_review.json)
- [Fresh competition](../research/component_review/selection_followup_review.json)
- [Joined receiver](../research/component_review/joined_receiver_review.json)
