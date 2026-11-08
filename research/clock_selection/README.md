# Clock-mediated conditional response

This research asks whether an incoming signal can change a local clock state so
that the same later probe produces a different recorded response. A longer-term
target is repeated internal trials and a uniquely recorded preferred route.
These are separate acceptance claims. A prearranged late pulse alone is not
evidence that the apparatus computed approval.

Baseline: Universe24 main commit
`ff89e2ff661c8b60af84aff738f9040ad7f15bcc`.

Start with the [reviewed recording collection](evidence/presentation_collection_v3/index.html)
and [decision ledger](decision_ledger.md). The collection links complete
experiment selectors, explanations and independent certificates. The
[writer/probe comparison](evidence/animations_v1/review/README.md) shows the
clock memory before the probe at state40 and its outlet response at61. These
are renders of saved states; the clock hold is finite and the later probe can
change the stored phase.

The complete [terminal-clock pause/resume clip](evidence/animations_carrier_memory/carrier-pauses-restarts-clock.gif)
shows all121 native states with exact clock panels. The stopped states74–75 and
restart76 arise from the incoming carrier's two lobes. Its terminal record
still aliases null/probe-only; this is not computed approval. See its
[frame provenance and display-selection scope](evidence/animations_carrier_memory/FRAME_SOURCES.md).

The [public building-block guide](../../docs/CLOCK_SELECTION.md) gives the
available preparation APIs, supported environments and first run commands.

## Fixed model and research boundaries

Every run has one board, 48 channels per node, six spatial neighbors, and one
tensor fixed before the first update. Only synchronous Rule3 with `num=den=1`
evolves the counters and retained remainders. All components are initial data.
No observer, complexity metric, score, software timeout, inverse operation or
Presenter action controls a running state. Full reversible information is kept.

Research stages freeze their preparations, controls, readouts, resource budgets
and success criteria before execution. Exploratory discovery is separated from
later validation. A failed target and a resource-limited search remain visible;
neither is converted into success by changing the observer afterward.

## Generic recording and viewing

Record an ordinary native experiment or study specification using the existing
engine and runner:

```bash
python -m research.clock_selection.run record \
  --spec path/to/frozen-spec.json --output runs/clock-selection-recording
```

Package already saved complete recordings in the unchanged generic Presenter:

```bash
python -m research.clock_selection.run present \
  --input path/to/record.json.gz \
  --input path/to/another-record.json.gz \
  --output runs/clock-selection-presenter
python -m http.server 8000 --directory runs/clock-selection-presenter
```

Open `http://localhost:8000/index.html` in a JavaScript-enabled browser. The
inventory links complete experiments across bounded pages. The Presenter keeps
all saved states, all 48 channels, all remainders and raw C0/C1/C2 classes; it
does not select a route or evolve the board. A clock-hand rotation is not by
itself a click. Attachment previews may not execute JavaScript.

## Evidence indexing and independent review

Restore the pinned native evidence in a fresh checkout with
`python -m research.experiments.materialize_evidence`, then
`python -m research.clock_selection.archive materialize`.
The [publication guide](publication.md) explains checksums, lossless certificate
storage and clean-checkout validation. The [final identity index](evidence/index_final/index.json)
retains every completed control; its [verification and correction map](evidence/index_final/verification.json)
keeps24 partial duplicate captures and superseded observers separate from the890
completed study records.

The engine retains an empty core dependency list. The coherent-wave numerical
preparation and its critical observer regression use the pinned optional
research dependency:

```sh
python -m pip install -r research/clock_selection/requirements.txt
```

The existing symbolic-synthesis tests additionally use
`requirements-solver.txt`; they are separate from native Rule3 and may otherwise
report explicit optional skips. Reliability CI installs both pinned research dependencies,
restores and hash-checks the historical and clock-selection evidence archives,
then executes the existing test/reproducibility job. It does not repeat every
large research search. A configured workflow is not a claim that remote CI has
already run successfully.

Each submitted study directory must preserve `protocol.json`, `result.json`
and every complete recording under `records/`. Indexing keeps unsuccessful
cases too. A solver or incomplete search may have no forward recordings;
interpret its saved outcome separately.

```bash
python -m research.clock_selection.run index \
  --study pilot=path/to/completed-study --output runs/clock-selection-index
python -m research.clock_selection.run verify-index \
  --index runs/clock-selection-index/index.json
```

These commands verify file identities only. They do not certify physical
meaning, behavioral success or complete exploration. The independent audit
uses its own explicit study input and checks the actual full-state evolution,
controls and frozen predicates. Use a fresh output location for each command;
existing evidence is not overwritten.

## Completed evidence and its limits

The initial [WRITE–PROBE protocol](protocol_v1.json) retained
[all68 complete controls](evidence/write_probe_v1_run01/result.json). Its
[independent audit](evidence/independent_audit/write_probe_v1_verified.json)
replayed5220 complete states and5152 transitions. None of16 registered gates
passed. Removing writer counters alone left a remainder defect that damaged
the probe-only input. A joint outgoing packet did not repair that control.
The original failed initialization is retained separately under
`evidence/write_probe_v1/`; it is not a completed scientific run.

The [finite recurrence protocol](recurrence_protocol.json) retained
[all20 complete controls](evidence/recurrence_v1/result.json). The
[independent replay](evidence/independent_audit/recurrence_v1.json) checked2860
complete states and2840 transitions. Six continuous returns met the frozen
carrier predicate across sides48,50,52,54. Zero strict clock-conditioned gates
passed because the packet-only comparator did not supply a valid return.
This demonstrates bounded recirculation of an initially prepared carrier,
without reinjection, on an intentionally periodic guide.

The subsequent [read-only full-board period check](evidence/recurrence_period_diagnostic/result.json)
found exact initial-state closure at50 updates for the L50 joint case and54
updates for L54, with every retained shifted overlap equal. Exact full-state
closure under the fixed deterministic update implies continued repetition;
those two examples cannot accumulate a new full-board trial history. No repeat
was found for the L48/L52 joint cases within their original finite horizons.
That non-repeat does not exclude a longer period.

The [audited long follow-up](recurrence_results.md) extends L48/L52 through32
return opportunities. Neither joint preparation regenerates the fixed complete
carrier after loss, and every later scheduled output is absent. The first
return remains identifiable; no strict approval gate is established. All eight
long trajectories are available across bounded Presenter pages.

| Existing complete Presenter package | What it contains |
| --- | --- |
| [WRITE–PROBE V1](evidence/presenter_v1/index.html) | Eight prospectively selected controls,648 frames; failed target retained |
| [Finite recurrence](evidence/presenter_recurrence_v1/index.html) | All four masks at L50/L54,1160 frames; the full returning carrier and clock state |
| [WRITE–PROBE V2](evidence/presenter_v2/index.html) | Eight prospectively selected complete controls,712 frames; see its separate frozen protocol and audit before interpreting a gate |
| [Clock-region mediation](evidence/presenter_mediation/index.html) | Eight complete cross-preparation controls,392 frames; altered regions are prepared before startup |
| [Paired-clock response](evidence/presenter_structure/index.html) | Twelve complete examples,588 frames; original selections plus four labeled postanalysis display controls |
| [Long recurrence](evidence/presenter_recurrence_long/index.html) | All eight complete controls,13,128 frames on four pages |
| [Parallel division](evidence/presenter_parallel_division/index.html) | Eight selected native arithmetic examples,104 frames |
| [Quiet prepared clocks](evidence/presenter_quiet_clock/index.html) | Six complete amplitude/parity examples,54 frames; initial-only factory with all-sign support |
| [Separate-clock formation](evidence/presenter_formation/index.html) | Six complete controls,582 frames; bridge activation without accepted binding |
| [Internal comparison branch](evidence/presenter_internal_gap/index.html) | Five complete native examples,45 frames; no mass identification |
| [Dense coherent waves](evidence/presenter_coherent_waves/index.html) | Four complete full-cube examples,52 frames on four pages; mathematical checks pass, CPU budget fails |
| [Orthogonal two-outlet controls](evidence/presenter_two_outlet/index.html) | Sixteen complete examples,1424 frames across six pages; no unique redirection |
| [Routes and clock memory](evidence/presenter_route_clock/index.html) | Eight complete source/phase/rest controls,648 frames; first activation followed by failed quiet retention |
| [Initially resting clock sites](evidence/presenter_activation/index.html) | Eighteen complete matched controls,1458 frames across two pages; transient activation without an accepted late quiet clock |
| [Conditional carrier and terminal clock](evidence/presenter_carrier_memory_combined/index.html) | Eight complete controls,968 frames; four prespecified phase2 negatives and four labeled postanalysis phase0 pause/resume illustrations |

The second WRITE–PROBE study uses complete initial packet removal and has its
own [protocol](protocol_v2.json) and [records](evidence/write_probe_v2/result.json).
It does not replace V1 or convert a source-counter ablation into a complete
absence control. The [audited result and mediation report](write_probe_results.md)
records four accepted conditional-output groups on two cube sizes. Its separate
16-run mediation study passes all four crossed-region groups and all eight
unchanged native-suffix comparisons. The altered region/exterior combinations
are new initial preparations, not interventions in a running board. These
results do not establish two-route selection or internally generated approval.

The [structural study](structure_results.md) establishes finite signal-driven
phase reconfiguration of a prepared period-five paired clock in two of eight
geometries. It finds zero pairs of the registered isolated-clock products.
Its corrected passive assessment is authoritative; the withdrawn observer
positives and exact native records remain available. This is not a force or
physical-binding demonstration.

The [claim register](claim_register.md) assigns proof/result/hypothesis/future
status with exact evidence references. The [decision ledger](decision_ledger.md) maps each current hypothesis to its
candidate, fixed observations, available evidence and next decisive test. It
also keeps the unimplemented fixed-ratio candidate separate from the baseline.

The [parallel division report](parallel_division_report.md) independently checks
90 small-board native runs. Source fanout and all three arithmetic C classes
do not imply exclusive route choice. The [coherent-wave derivation](coherent_wave_algebra.md)
is an exact baseline-sector reduction and finite-time comparison theorem.
[All16 native comparisons](coherent_wave_results.md) independently pass their
mathematical criteria, while their **300-second CPU ceiling fails by28.943
seconds**. The [internal-gap demonstration](internal_gap_results.md) independently
checks20 finite native runs under unchanged Rule3. Neither result establishes
physical light or mass. Other per-channel ratios remain a mathematical candidate.

The [separate-clock formation study](structure_formation_results.md) verifies48
runs and finds zero registered formed composites. Equal-phase nearby clocks
activate a bridge and influence each other, but the late region fails recurrence
and isolation. This negative result is retained alongside the useful local
activation mechanism.

The [orthogonal two-outlet study](two_outlet_results.md) independently verifies128
runs and six history-conditioned carrier gates, but no exclusive or redirected
choice. Raw arithmetic clicks can occur without the declared complete carrier.
Its interrupted attempt, exact repeated overlaps and incomplete whole-workflow
CPU accounting remain documented; a phase-only timing receipt is not a complete
resource pass.

The reusable [QuietClock factory](quiet_clock_results.md) returns a complete
immutable center/halo Patch. Its exact isolated period-four construction covers
all eight existing sign tensors and all48 channels;48 native preparations pass
independent full-state replay. This is an initially prepared oscillator.
Incoming activation and subsequent quiet retention require a separate test.
The result explicitly leaves whole-session CPU certification unavailable
because preflight-process startup was not included in its timing receipt.

The [route-to-clock composition](route_clock_results.md) independently checks64
complete runs. The bare route and all28 driven incoming comparisons pass, yet
none of24 active-clock comparisons or four resting-apparatus comparisons leaves
the registered quiet phase memory. Resting winners activate with a native C1 at
update15; nominal losers activate at59. This distinguishes a real causal input
from permanent exclusive recording. No existing criterion was shortened to
hide the later influence.

The [direct activation study](activation_results.md) independently verifies36
native runs. All18 input comparisons are eligible and every source-off board
stays stationary. Six source-on cases produce real native C2 activation at
update16, but zero of18 comparisons leaves a quiet unit, axis-two or diagonal
clock during states64–80. This bounded negative result does not exclude every
possible resting preparation. Its complete whole-process resource receipt
passes all registered limits.

The [two-stage carrier/memory composition](carrier_memory_results.md) independently
verifies32 runs. All terminal regions are quiet at96–112, but zero of eight
geometries retains a joint result distinct from all three controls. In phase0,
the joint receiver differs from writer alone while equaling null/probe-only.
Its native late encounter stops the center through C2 at74 and restarts it
through C1 at76; no approval instruction exists. The four original phase2
display controls remain intact alongside explicitly labeled postanalysis
phase0 controls. The whole-process budget passes.

The [independent review addendum](independent_review_addendum.md) covers all15
studies:890 complete native recordings,76,322 complete states and75,432 forward
transitions, each independently inverted, with890 complete rewinds. Partial
duplicate attempts and passive rereads are retained separately and not counted
again. All scientific failures and resource qualifications remain in that total.

## Research organization

`run.py` is passive orchestration. The search producer, algebra note, physical
criteria and independent auditor have separate ownership. Preparation and
recording reuse the existing component APIs; the engine and Presenter sources
remain unchanged. Specific results and their finite domains are added only
after registered runs and independent review.

The [algebra note](algebra.md) distinguishes the proposed mechanisms and their
exact requirements. The [operational criteria](physics.md) define trials,
approval, clicks and preferred routes. Its source-cooperation proxy is proposed
passive analysis, not an established complexity law or a runtime selection rule.
The [composition and recurrence note](dynamics.md) explains why matching a local
clock interface does not remove the writer's external wake, and why recirculating
a carrier is a separately testable mechanism.

The [five physical-target notes](physics_targets/README.md) describe the missing
operational tests for electromagnetism, electronic binding, the strong and weak
interactions, and gravity. They are sourced prospective requirements. The
[arithmetic click and body-boundary note](click_algebra.md) distinguishes core
events from outer-halo remainders; [structure algebra](forces_algebra.md)
separates recurrent clusters from attraction, formation and dissociation.
