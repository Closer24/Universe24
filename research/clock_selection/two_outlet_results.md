# Orthogonal inputs and two registered outlets

Status: all 128 registered preparations were captured in the documented retry
and independently replayed. The frozen question separates simultaneous
two-outlet competition from sequential writer-conditioned continuation.
Rule3, the fixed +++ tensor and the engine are unchanged. These are two prepared
inputs; this experiment does not split one input into two possible routes.

## Registered apparatus and controls

A +X writer on channels 0/14 and a later or simultaneous +Y probe on channels
15/39 meet one channel-2 clock region. Each input has its own complete guide.
The shared clock has a jointly prepared halo; every overlapping initial triple
is checked before the one board is finalized. Absent inputs restore their
complete 24-address source footprints, including remainders. Clock-counter-off
and wholly absent clock-interface controls are kept separate.

The primary side-369 family tests phases 0–3, input spacings 0/34/36 and all
four input masks with and without clock counters. The prospective side-385
holdout uses phase 3. Sixteen bare crossed-guide controls traverse the complete
junction and output windows. Four isolated-axis controls test whole-state
translation. Encounter horizons are 88 updates; isolated controls use 12.

The clock-on apparatus already oscillates without a signal. In the saved
writer-only counter-off controls, the center is `(0,0,0)` throughout states
32–40 for every tested phase label. This family demonstrates phase control of
a prepared clock, not persistent clock creation from zero counters.

Both early and near incoming templates compare every channel in the complete
carrier box. The near boxes avoid the interface and perpendicular guide, so
there are no excluded channels or clock nodes. Every clock-on group passes
these incoming checks. Eight of twelve clock-counter-off groups pass; the
other four are input-ineligible comparisons.

At each outlet, an exact candidate must match four consecutive complete carrier
states. Both natural arrival times and the prospectively fixed latency range
−4 through +8 are checked. Candidates are identified by `(outlet,start)`, so
coincident epochs do not create duplicate candidates. The separate raw-C test
requires C2 with quotient −1 at `T-3` and C1 with quotient +1 at `T+1`, with no
other primary-channel C in `T-3..T+4`. All other events remain recorded.

## Six conditional continuation results

All fifteen clock-on groups pass the complete incoming checks and the fixed
336-triple quiet-orbit check. Of the ten sequential clock-on comparisons, six
pass the registered carrier-and-C history discriminator:

| Cube side | Initial phase | Input spacing | Exact late Y carrier without writer | Exact late Y carrier after writer | Registered result |
|---|---|---|---|---|---|
| 369 | 0 | 34 | No | Yes, at T=61 | Enabled |
| 369 | 2 | 34 | No | Yes, at T=61 | Enabled |
| 369 | 3 | 34 | No | Yes, at T=61 | Enabled |
| 369 | 3 | 36 | Yes, at T=63 | No | Suppressed |
| 385 | 3 | 34 | No | Yes, at T=61 | Enabled |
| 385 | 3 | 36 | Yes, at T=63 | No | Suppressed |

The phase-1 clock already has the retained phase reached after writing, so its
comparison does not demonstrate changed memory. The other negative sequential
cases remain in the evidence. No exact late X redirected-output candidate
satisfies the registered target.

These results control an exact outgoing carrier and its C timing pattern.
They do **not** switch all raw clicks on or off. For example, at side 369,
phase 0 and spacing 34, the Y outlet has the following complete raw-C list
through update 88:

| Input mask | Y-outlet raw C events, listed as `(step,kind,quotient)` |
|---|---|
| Neither input | None |
| Writer only | None |
| Probe only | `(59,2,-1)`, `(60,1,+1)`, `(61,2,-1)`, `(62,1,+1)` |
| Writer and probe | `(58,2,-1)`, `(62,1,+1)` |

The probe-only case therefore still produces arithmetic events even though it
fails the exact carrier/signature test. The joint preparation changes the
waveform and timing. It has not implemented a single approved click, erased
an unapproved history or produced a persistent detector record.

## Simultaneous exclusivity did not occur

At spacing zero, phases 0, 1 and 2 yield no exact registered joint outlet
carrier. Phase 3 yields **two**, one at X and one at Y, both with the clean C
signature. The two-output phase-3 result repeats on side 385. None of the five
clock-on simultaneous comparisons yields exactly one candidate.

The bare simultaneous crossing also delivers both exact carriers, but has an
additional C2 event at update 30 at each outlet, after the expected events at
24 and 28. The frozen producer requires a clean C signature in its bare-route
calibration, so that calibration fails. The sequential bare crossings at
spacings 34 and 36 pass. This stricter calibration condition must not be
relaxed after seeing the extra event. Even without that calibration issue,
the observed zero-or-two joint carrier counts do not meet the one-output
criterion.

## Interruption, reproducibility and limits

The first attempt retained only four complete isolated-control recordings
before its execution session became unavailable. Its terminal error and CPU
usage are unknown. It is preserved as an interrupted attempt, not counted as
a complete 128-case study. The retry uses the same protocol and scientific
predicates, with a reviewed runner change that saves each complete record,
progress and explicit failures immediately. All four overlapping preparations,
complete frame sequences and assessments match exactly.

The retry completed all 128 records, all full-state inverse checks and all
four isolated translation tests. Exact source-archive and live-source checks
passed. The independent audit verified 11,088 complete states and 10,960
transitions, every inverse and all four exact overlaps with the interrupted
attempt. It confirmed all six history results and both zero-result counts.
Recorded size was 112,632,937 bytes. The measured capture, observation
and record-serialization phase used 574.25 CPU seconds and 575.87 wall seconds.
That timer excludes preparation preflight and final Presenter JSON export.
Total-process CPU is unknown; therefore a whole-workflow 600-second CPU-cap
success is **not** certified. The explicit timing-scope note preserves this
limitation alongside the original receipt.

This study improves the separation of clean writer and probe inputs. Its
conditional continuation results have a specified finite domain. It supplies
neither autonomous trial generation nor measured complexity preference, and
it supplies no exclusive route winner in the registered simultaneous family.
The separately studied OR/NO prepared route block remains distinct: this
negative result does not erase that earlier block's finite route preference.

- Frozen protocol: [protocol_two_outlet.json](protocol_two_outlet.json)
- Complete retry: [two_outlet_v1_retry01/result.json](evidence/two_outlet_v1_retry01/result.json)
- Independent replay: [two_outlet_v1.json](evidence/independent_audit/two_outlet_v1.json)
- Original interruption: [interruption_receipt.json](evidence/two_outlet_v1/interruption_receipt.json)
- Exact replay overlap: [retry_overlap.json](evidence/two_outlet_v1_retry01/retry_overlap.json)
- Timing scope: [timing_scope.json](evidence/two_outlet_v1_retry01/timing_scope.json)
- Independent timing qualification: [two_outlet_timing_scope_review.json](evidence/independent_audit/two_outlet_timing_scope_review.json)
- Presenter selections: [presenter_selection.json](evidence/two_outlet_v1_retry01/presenter_selection.json)
