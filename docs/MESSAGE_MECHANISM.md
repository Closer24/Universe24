# Message mechanisms on one reversible board

**Research date:** 7 November 2026. **Candidate base:** `0d4c4805be67b0efc42e084416ff2204529a1e07`.

This study asks whether ordinary Rule3 signals can write a quiet pending record, approve or cancel it later, and eventually communicate a decision between alternative routes represented inside one board. The current model, coupling construction, component recipes and generic Presenter remain unchanged. Every new run uses one preselected `+++` tensor and an initial preparation; nothing injects, approves, cancels or selects a state during evolution.

The four bounded studies are complete. They supply an exact opposite-moving packet preparation and sharper constraints on a message interface, but **no new quiet-pending, approval or cancellation component passes its acceptance criteria**. The research package is reproducible; the requested autonomous decision mechanism remains unbuilt. No physical light, quantum entanglement, collapse or preference for more complex routes has been established.

## The exact local message interface

For each channel the only forward operation is

```text
ell, r_next = divmod(2*u + r, 6)
a_next = b
b_next = ell - a
```

Here `u` must be the actual signed sum from the six spatial neighbors in the same previous board state. The following calculation concerns channels `0` and `14`, initially with zero counters. It does not prescribe input sums to a running board.

| Initial receiver pair | Actual input pair | Resulting remainder pair | Resulting counters and interpretation |
|---|---|---|---|
| Ready `(2,4)` | `(1,-1)` | `(4,2)` | All zero: write a pending record |
| Pending `(4,2)` | `(0,0)` | `(4,2)` | All zero: wait without a local event |
| Pending `(4,2)` | `(-1,1)` | `(2,4)` | All zero: restore the ready receiver |
| Pending `(4,2)` | `(1,-1)` | `(0,0)` | Channel 0 has `(a,b)=(0,1)`: an arithmetic C event |

These are exact conditional identities, not yet autonomous building blocks. Other channels must also meet the declared complete-state interface. A source waveform can contain later lobes; receiver feedback can change its own future input. The complete preparation must supply every required input and preserve the stated behavior for the entire horizon.

The proposed messages are state dependent. Sending the nominal cancellation pair `(-1,1)` to the ready pair `(2,4)` instead produces a channel 14 arithmetic C event. Duplicate, stale and wrong-state messages therefore cannot be treated as harmless commands.

There is also an exact constraint on quiet writing. If a receiver begins with zero counters and has no guarded C event during an interval, its quotient stays zero, its counters stay zero, and each channel satisfies

```text
r(t) = r(0) + 2 * sum(actual_inputs_before_t)
```

through that interval. A balanced input waveform restores the original remainder. A converter must change the actual waveform reaching the receiver; changing a readout label does not solve this constraint. A quiet zero-counter pending receiver emits no counter disturbance by itself. Approval or cancellation generated inside the board therefore needs a further active pattern or a later interaction with the stored remainder.

See the [algebra note](../research/message_mechanism/algebra.md) for the formal assumptions and message constraints.

## What the first 18 runs show

The [baseline protocol](../research/message_mechanism/protocol_baseline.json) was recorded before these trajectories. Its SHA-256 is `9a397bfee30dcca86ff15c41085fa8182804b79ddf82cd9f959c9e93fa4c391f`; this is a research registration, not a third-party timestamp certificate.

The board has side `129`, background `(0,0,2)`, horizon `24`, and fixed `+++` coupling. A complete periodic guide with pair `(0,4)` runs along x at `y=z=64`. The compact source occupies x `32..35`, including its full transverse preparation; the receiver is at `(48,64,64)`. All nine ordered even receiver pairs in `{0,2,4}^2` are tested with and without the source. No random seed is used: the family is exhaustively enumerated.

The prospective pending target is the complete 48-channel state with zero counters, pair `((r0-2) mod 6, (r14+2) mod 6)`, and all other remainders unchanged at 2. It must hold at every saved state `13..21`, which includes eight subsequent quiet updates after first arrival. Every receiver counter must be zero through state 21, with no receiver C in updates `1..21`. A source-absent run must retain its whole initial board through step 24.

**None of the nine source-present preparations passes the pending-record criterion.** All nine attain the target remainder pattern at first arrival, but this does not establish a retained record. Eight lose the pattern at state 15; the unmodified-guide control loses it at state 17. The `(2,2)` receiver remains counter-quiet through state 21, but its changed remainder target is already lost at state 15. The other eight source-present cases develop receiver counters and C events by state 15.

All nine source-absent boards remain stationary. The source-present `(0,4)` control exhibits exact complete-state translation by one x site at every step. All 18 stored whole-board rewinds agree with their initial states. A separate matrix-oracle audit reproduced all 432 forward and 432 inverse transitions across 450 complete states. It checked every receiver channel, actual input and all six neighbor terms, and verified the source-absent remainders and halo. See the [result and failed predicates](../research/message_mechanism/evidence/baseline_v1/result.json) and [independent audit](../research/message_mechanism/audit.json).

The precise failure is the packet-to-quiet-memory interface. It does not refute every possible initial preparation and does not revoke the existing packet translation result. The next search changes only a finite initial converter patch and keeps the receiver definition fixed.

## The 891-preparation converter search

The separate [discovery protocol](../research/message_mechanism/protocol_discovery.json) fixes a receiver initially at `(4,2)`, target `(2,4)`, and horizon 40 on the same `L=129` guide geometry. It enumerates 729 combinations of three initial remainder pairs at x45, x46 and x47; 81 combinations of a row-x47 pair and a transverse pair at `(47,65,64)`; and 81 combinations with that transverse pair at `(46,65,64)`. Every pair is in `{0,2,4}^2`; the transverse channel addresses are derived from the fixed tensor. Counters outside the existing source remain initially zero. There is no random seed.

Acceptance requires a start state in `13..24` followed by eight further states with the exact full-node pending target, with zero receiver counters and no receiver C from the initial state through the end of that interval. This finite window is fixed in advance; it is not moved to a later favorable plateau. The result is **0/891 accepted preparations**. All candidates completed within the budget, and each family's best quiet target lasted only two consecutive saved states. See the [result](../research/message_mechanism/evidence/discovery_v1/result.json) and [complete compact trial ledger](../research/message_mechanism/evidence/discovery_v1/ledger.jsonl.gz).

All 35,640 screened reference-engine transitions passed their per-step inverse checks. The ledger retains each case's preparation parameters and specification digest, all 48 receiver states and actual input sums, final full-state digest and fixed assessment. The frozen generator and protocol reconstruct its complete specification. Full trajectories are retained for the prospectively required first and best cases in each family, with matched source-absent controls.

The [independent audit](../research/message_mechanism/audit.json) recomputes the local scalar evolution and acceptance predicates in all 891 stored receiver ledgers. Its separate matrix oracle checks all 12 retained full recordings (492 states, 480 forward and inverse transitions) and freshly re-evolves the 16 failed candidates selected by the rule fixed before discovery (640 updates in each direction, with complete final digests and all receiver inputs compared). This does not independently verify every intermediate whole-board state in all 891 candidates; those unstored, unsampled states remain outside its scope.

No candidate is promoted to a new component, and no successful-candidate holdout is claimed. The bounded result excludes these enumerated stationary remainder converters for this source, receiver, tensor and horizon. It does not exclude active converter seeds, different geometries or other initial preparations.

## The 54 reverse-designed preparations

A final [prospective preparation search](../research/message_mechanism/protocol_reverse.json) starts from 54 complete proposed endpoints: three outgoing packet locations, two compensation locations and nine even compensation pairs. The fixed receiver is at `(48,64,64)`, and its required initial ready pair is `(4,2)`; its target pending pair is `(2,4)`. Thirty-two inverse steps are used only by the external initial-condition search. Any actual experiment then advances solely with the existing forward Rule3 engine.

The acceptance test requires every initial active counter to lie in a source box `x=8..40`, `y,z=48..80`, separated from the receiver; the receiver must start exactly ready. A forward run must then write the changed full-node target, with no receiver C, and retain it at states `32..40`. Source-box-off controls remove only the declared source counters and retain all other initial data. The source box and receiver cannot be moved after seeing the preparation.

**All 54 preparations fail initial admissibility.** Every one already contains the target pending receiver at time zero, instead of the required ready receiver, and also has 4–16 active channels outside the allowed source box. Consequently there are zero admissible sources and zero successful memory writes. The [result](../research/message_mechanism/evidence/reverse_v1/result.json) and complete initial-state records retain every failure. The 1,728 inverse preparation steps were checked against reference forward steps.

Four full forward examples retain the first and best-ranked proposals plus their source-box-off controls. For the on cases, recovering the chosen endpoint at update 32 is a consequence of how the initial state was constructed; it is not evidence that a clean incoming signal wrote the receiver. A source-box-off example holds its target quietly because that target was present initially. Outside-box contamination remains in those controls rather than being deleted to manufacture a quiet null case. These examples must not be used as accepted pending memories.

The independent matrix audit verifies all 54 complete initial preparations and all 33 recorded hashes in each inverse preparation history: 1,728 inverse steps and their forward checks. It also reproduces all four full forward controls, with 164 complete states, 160 transitions in each direction and exact rewinds. No initial-admissibility or memory-write success is inferred from those consistency checks.

## A proved limit on a narrower construction

The [algebra note](../research/message_mechanism/algebra.md#a-confined-translating-front-cannot-leave-a-different-guide-phase) proves a confined-row obstruction. Consider a translating identity-channel X-row profile with finite counter support, stationary zero-counter far fields, no active transverse inputs, and a one-site advance after any finite internal period. Its far-field remainder jump satisfies `delta = 8*B`, where `B` is an integer sum over its counter phases. Since two valid remainders differ by at most five, `delta=0`.

Thus this particular moving front cannot leave a different quiet guide phase behind it, even if its pulse is lengthened or its one-site advance takes several updates. This is not a theorem against active transverse converters, general multichannel motion, multiple-site advance, extended tails or nontranslating scatterers. A single isolated interface also needs care on a periodic board, where another interface must occur. These assumptions determine the proof's useful boundary.

## The opposed-packet interaction study

The separately frozen [interaction protocol](../research/message_mechanism/interaction_protocol.json) uses a left guide with pair `(0,4)` and a right guide with pair `(4,0)`, meeting at x64 on an `L=129` cube. The right-moving compact packet and its complete halo are retained. The left-moving packet is obtained using the even-sector time-reversal transform `J(a,b,r)=(b,a,4-r)` on every prepared channel, rather than reversing a drawing or assuming a negative pulse travels backward.

Two carrier controls run for eight steps. The interaction family tests seam pairs `(0,4)`, `(2,2)` and `(4,0)` with relative delays `0,2,4` in discovery and `1,3` in a predeclared holdout partition. Each of these 15 groups has neither source, each isolated source, and both sources, through step 32. Thus the study retains 62 runs, 1,998 complete states and 1,936 transitions. Holdout here means new delays specified before this family ran; it is not validation of a successful discovered component.

The [recorded result](../research/message_mechanism/interaction_evidence/summary.json) has **0/15 strict outlet-cancellation successes, 0/15 changed quiet-memory successes, and 13/15 nonlinear counter interactions**. A nonlinear interaction means that the joint counters differ somewhere from the declared combination of the two isolated-source controls. It supplies no approval or durable-record guarantee.

The strict outlet cancellation predicate demands a functioning transmitted source, a quiet matched opposite-source control at that outlet, and a quiet joint output in the fixed window `20..32`. In this geometry, isolated-source reflections already violate the control-null condition: there are no eligible groups under that clause. Both joint outlets also remain active in every group. The result therefore identifies a failed outlet separation and conversion interface, not a general impossibility of local cancellation.

One illustration selected after analysis is seam `(0,4)`, delay 0. In the joint preparation the center stays inactive throughout the 32 steps, whereas isolated packets activate it. Nevertheless, each joint outlet has four pair-channel C events in the outgoing window, and all four complete final control states are distinct. The locally quiet center is neither a changed memory record nor a deleted trajectory. The independent matrix audit reproduces all 62 full recordings and their inverses, initial transformed halos, probes and fixed comparisons. It also records explicit complete-state channel differences between the joint and singleton preparations. See the [independent review](../research/message_mechanism/independent_review.md).

## Alternatives, approval and cancellation inside the board

One complete initial state and one fixed tensor determine one complete trajectory. Finite alternative routes can be represented simultaneously by distinct patterns in that trajectory. Running several simulations and comparing them afterward is an external search over preparations; it is not an internal representation of those alternatives.

A useful internal protocol must state which patterns encode candidate routes, what information is compared, where the comparison occurs, how an ordinary signal returns its result, and when a receiver can know that all declared competitors have been accounted for. The first target should be a bounded two-route apparatus with a known candidate set and response horizon. The [protocol design](../research/message_mechanism/protocol_design.md) specifies this target and its missing physical components.

The proposed next block is a pending memory with separate approval and cancellation input contracts. Its acceptance requires a source-dependent quiet write, a finite wait, and a later ordinary signal that produces the declared record or restores the ready state. Supplying a second preloaded packet can test this interface; it cannot establish that a competition inside the board generated the approval.

An absent signal at one outlet does not mean the complete state was erased. Reversibility requires distinct initial states to remain distinct complete states. A cancellation candidate must identify its remaining records, outgoing disturbances or other retained differences and pass a full-state inverse audit. A nonstationary whole board cannot enter a global fixed point after finitely many steps under an invertible update. A local region may nevertheless become quiet while information propagates elsewhere.

## Acceptance contract for a reusable component

| Item | Required evidence |
|---|---|
| Preparation | Exact counter/remainder patch, background, tensor identity, occupied support and compatible connection sockets |
| Environment | Guide and surrounding halo, boundary conditions, allowed neighboring preparations and no-wrap horizon |
| Input | Actual full 48-channel input traces and allowed incoming packet family; duplicates and invalid timing included in the contract |
| Output | Fixed state predicate and address before the run; both presence and absence controls |
| Timing | Arrival, response, quiet waiting and record-retention windows stated in board steps |
| Causality | Source-absent and each-source controls; approval production traced to the retained internal apparatus |
| Composition | A working pair or larger assembly under one compatible fixed tensor; no hidden runtime operation |
| Robustness | Fresh preparations, geometry or board-size holdouts and declared perturbation domain after discovery |
| Reversibility | Complete-state forward and inverse comparison with an independently constructed oracle |
| Claim boundary | Designed preparation distinguished from a broad family and physical interpretation distinguished from arithmetic behavior |

A numerical complexity score may be a passive observable or a discovery objective used before a run. It is not an internal selector. To claim that the board favors greater complexity, the chosen score, alternative predictions and controls must be frozen, and the apparatus must implement any comparison and signal generation through Rule3 alone. No such preference is established by the present baseline. The earlier [`C_pair` study](PATH_SELECTION_BLOCK.md#results) had ten eligible arrival-matched comparisons and ten counterexamples to its registered higher-score-only prediction. A replacement measure would define a new hypothesis, not repair that result retrospectively.

## Claim ledger and decisions

| Claim | Status | Evidence or unresolved test |
|---|---|---|
| The scalar write/wait/approve/cancel table is valid for its stated input sums | Exact conditional calculation | [Algebra](../research/message_mechanism/algebra.md) |
| A balanced quiet input cannot leave a changed remainder record | Mathematical consequence under zero-counter/no-C assumptions | [Algebra](../research/message_mechanism/algebra.md) |
| A complete translated packet can be converted into an opposite-moving preparation by time reversal of its entire state | Mathematical consequence of `F J F = J`; the paired guide and transverse halo must also be transformed | [Full-board symmetry proof](../research/message_mechanism/algebra.md#4-exact-full-board-phase-and-time-reversal-symmetries) |
| A confined finite-support row front advancing one site per period can leave a changed quiet far-field remainder | Ruled out under the explicitly stated row, stationary-far-field and zero-transverse-input assumptions | [Narrow proof](../research/message_mechanism/algebra.md#a-confined-translating-front-cannot-leave-a-different-guide-phase) |
| The existing compact packet translates in the unmodified guide | Computational control in this study; existing broader result has its own scope | [Baseline result](../research/message_mechanism/evidence/baseline_v1/result.json) |
| A single even receiver defect stores the required quiet pending record | Failed finite criterion: 0/9 source-present cases; 9 null controls | [Protocol](../research/message_mechanism/protocol_baseline.json), [result](../research/message_mechanism/evidence/baseline_v1/result.json) |
| Opposed packets produce a changed quiet record or a strictly canceled outlet | Failed finite criteria: 0/15 groups; strict outlet-control eligibility also fails in this geometry | [Interaction protocol](../research/message_mechanism/interaction_protocol.json), [result](../research/message_mechanism/interaction_evidence/summary.json) |
| Opposed packets interact nonlinearly | Finite diagnostic: 13/15 groups; not approval or memory acceptance | [Interaction result](../research/message_mechanism/interaction_evidence/summary.json) |
| The first stationary remainder-converter family repairs the packet-to-memory interface | Failed finite discovery criterion: 0/891; no component promoted | [Discovery protocol](../research/message_mechanism/protocol_discovery.json), [result](../research/message_mechanism/evidence/discovery_v1/result.json) |
| The reverse-designed family supplies a clean localized source that writes the receiver | Failed initial-admissibility criterion: 0/54; every receiver already has the target and every preparation has outside-box counters | [Reverse protocol](../research/message_mechanism/protocol_reverse.json), [result](../research/message_mechanism/evidence/reverse_v1/result.json) |
| A closed internal comparison produces unique approval and cancellation messages | Research target | [Bounded protocol design](../research/message_mechanism/protocol_design.md) |
| More complex routes are selected by the dynamics | Hypothesis requiring a fixed complexity measure and competing controls | No supporting result from this study |
| Clicks establish light, quantum entanglement, collapse or physical time | Not established | Requires an operational physical model and independent predictions |

| Next question | Deliverable | Budget | Pass | Fail and continuation |
|---|---|---|---|---|
| Can an initially active transverse converter supply an unbalanced receiver waveform and quiet pending record? | A new frozen finite-support initial patch family, clean ready receiver, actual inputs, all four source/apparatus controls and full positive records | Proposed maximum 256 candidates, horizon 64, 600 CPU seconds, 20 minutes wall time; one fixed tensor | Source-dependent changed full-node target, zero receiver counters and no C through nine retained target states; fresh geometry and declared perturbation holdouts then pass | Preserve the first input/retention violation; constrain the next family from its waveform rather than repeat the excluded confined-row ansatz |
| Can a delayed second packet approve or cancel an accepted pending record? | Four source controls for each branch, stale-message controls and a new frozen holdout | At most 64 preparations times four controls, horizon 48, 240 CPU seconds after pending acceptance | First source writes quietly; second produces exactly the branch-specific record; null/isolated controls and retention pass | Identify the first counterexample input or feedback; do not change event windows retrospectively |
| Can a two-route apparatus generate its own decision signal? | Declared candidates, comparison region, response bound and complete causal histories | At most 32 preparations times four controls, horizon 64, 240 CPU seconds after working message ports | Approval originates in the board's comparison state and only the declared record is committed | A preloaded schedule or external maximum is insufficient; first identify the missing comparison component |

The decision is to stop the completed stationary-converter and reverse-endpoint grids and avoid repeating the mathematically excluded confined-row phase-front construction. The next proposed experiment is an independently registered active transverse converter within the same fixed model. The finite negatives do not justify a structural model change. Any such change remains a separately named candidate requiring a separate research decision.

For that proposed active converter, both isolated controls matter: apparatus alone and source alone must not write the declared pending record or produce a receiver click record. Only their composed interaction may pass. An apparatus that records by its own preexisting oscillation does not establish signal-activated memory.

## Reproduction and viewing

The existing generic Presenter replays saved complete states; it never supplies an approval or changes the dynamics. The baseline Presenter contains four prospectively selected examples: unmodified-guide translation, two receiver defects, and a source-absent control. The full 18-record set remains available beside it.

```bash
python -m research.message_mechanism.compute_baseline --output runs/message-baseline-reproduction
python -m research.message_mechanism.compute_discovery --output runs/message-converter-reproduction
python -m research.message_mechanism.compute_reverse --output runs/message-reverse-reproduction
python -m research.message_mechanism.interaction_search --output runs/message-interaction-reproduction
python -m research.message_mechanism.audit --baseline runs/message-baseline-reproduction --discovery runs/message-converter-reproduction --reverse runs/message-reverse-reproduction --interactions runs/message-interaction-reproduction --output runs/message-audit.json
python -m unittest tests.test_message_mechanism_audit -v
```

The output directory must be new. Open `The_Presenter.html` in a browser that runs JavaScript. Use the experiment selector, drag to rotate, and Reset view to see the whole cube. Focus retained state enlarges the apparatus inside that cube. These are native recorded-state examples, not an animation that invents signals or successful components.

To view the checked-in examples from a local checkout, run this in the repository root:

```bash
python -m http.server 8000 --bind 127.0.0.1
```

Then open [the baseline Presenter](http://127.0.0.1:8000/research/message_mechanism/evidence/baseline_v1/The_Presenter.html), [the converter Presenter](http://127.0.0.1:8000/research/message_mechanism/evidence/discovery_v1/The_Presenter.html), [the reverse-preparation Presenter](http://127.0.0.1:8000/research/message_mechanism/evidence/reverse_v1/The_Presenter.html), or [the four-control interaction Presenter](http://127.0.0.1:8000/research/message_mechanism/interaction_evidence/interaction_presenter.html) on that computer. The interaction illustration was selected after analysis and is labeled as a negative example. The complete full-state records and fixed readouts remain authoritative.

A chat attachment or file preview may display static HTML while disabling its scripts. Such a preview cannot select or play these experiments. This study does not establish native Safari/iPad or host-preview compatibility. The current environment's Chromium process terminates with `SIGTRAP` before loading a page; separate JavaScript/native-Canvas checks are reported with that narrower scope.

The [three-bundle smoke report](../research/message_mechanism/evidence/presenter_smoke_v1/report.json) and [reverse-bundle report](../research/message_mechanism/evidence/presenter_smoke_reverse_v1/report.json) pass all 18 displayed experiments across four Presenters. They check populated DOM selectors, every saved frame and digest, all 48 channel entries, stepping/play/pause, synthetic drag rotation, whole-cube reset with all eight projected corners inside the canvas, and unchanged retained data. They record no application JavaScript errors. Their explicit geometry emulation is not browser CSS or native pointer-layout validation.

The publication candidate passes all 132 repository tests with no failures, errors or skips in a fresh Git checkout after the pinned historical evidence is materialized. The standard impulse audits pass, and a fresh combined audit of all four studies reproduces the recorded audit exactly apart from CPU timing. The [validation record](../research/message_mechanism/evidence/publication_v1/validation.json) identifies the tested tree and separates subsequent documentation/validation records from the unchanged tested code and scientific evidence. Engine and frozen model bytes match the originally audited commit.

See the [research entry point](../research/message_mechanism/README.md), [complete audit](../research/message_mechanism/audit.json) and [independent review](../research/message_mechanism/independent_review.md) for reproduction details and exact coverage.
