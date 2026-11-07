# Independent message-mechanism review

Candidate base: `0d4c4805be67b0efc42e084416ff2204529a1e07`. Review date: 7 November 2026.

The new finite studies do not establish an autonomous pending/approval/cancellation component. Their negative results are useful interface failures, with exact recorded counterexamples. The translating prepared packet remains a demonstrated carrier in its guide. Nothing in this review identifies it with physical light.

## Independence and prospective scope

The reviewer read the baseline, converter and opposing-packet protocols before their trajectories. The baseline received an explicit complete-state requirement before freezing: the other 46 receiver remainders must remain unchanged, not merely the observed pair. The independently replayed converter sample was declared before the discovery data: lexicographically first 16 failed candidate IDs, plus every retained complete recording and all positives. No candidate passed, so no positive-validation holdout was triggered.

The oracle uses `research.reference.algebra` to construct the coupling from exact 4×4 matrices, independently of the production quaternion operations, routing tables and scalar updater. The source halo is reconstructed through the unique matrix-derived receiving channel. Initial patches are reconstructed independently, including the complete complementary time-reversed packet used in the interaction study. Overlapping initial assignments must agree. Every checked forward transition uses the whole previous state. Inverse transitions and a separate complete backward traversal are checked.

All runs use the same fixed `+++` member of the available tensor family, one complete board, 48 channels and all six neighbor ports. These data provide no claim of robustness across the other seven tensor choices. No runtime callback, source injection, approval gate or branch-deletion operation is added. The new code is research, audit and presentation material; the model engine is unchanged.

## Audit coverage and results

| Study | Independent check | Result |
|---|---|---|
| Packet/receiver baseline | All 18 full recordings; 450 complete states; 432 forward and 432 inverse transitions; 18 full reverse traversals; every receiver channel and all six signed input terms | 0/9 active preparations satisfy the frozen pending predicate. All 9 source-absent controls are stationary. The unmodified-guide control translates exactly. |
| Opposing packets | All 62 full recordings; 1,998 complete states; 1,936 forward and 1,936 inverse transitions; 62 full reverse traversals; all 48 channels at five probes and actual pair input terms | Both carrier directions translate exactly. 0/15 groups have the registered quiet record; 0/15 pass strict local cancellation. Counter nonlinearity occurs in 13/15 groups. |
| Converter discovery | All 891 saved receiver trajectories and recorded input sums are checked against scalar arithmetic and the unchanged observer. All 12 retained full recordings are independently replayed: 492 states and 480 forward/inverse transitions. | 0/891 accepted candidates; the best quiet target interval in each family is only 2 saved states, whereas acceptance requires 9 consecutive states. |
| Predeclared converter dynamics sample | 16 complete matrix-oracle re-evolutions from independent initial preparations, 640 updates; every receiver state/input and the full final-state digest match; exact reverse traversal | All pass. The sample is `row3-000` through `row3-015`; `row3-000` also has a retained recording. |
| External inverse preparation | All 54 endpoints reconstructed independently; 1,728 inverse steps and corresponding forward checks; all 33 hashes per inverse history and every complete prepared initial state checked. Four retained forward recordings add 164 complete states and 160 forward/inverse transitions. | 0/54 initial preparations are admissible. Every receiver already contains the target `(2,4)`, rather than the required ready pair `(4,2)`, and every preparation has 4–16 active channels outside the fixed source box. |

The converter audit does **not** assert an independent full-dynamics replay of all 891 candidates. Complete intermediate production states were not retained for the unsampled preparations. Recomputing the frozen scalar readout on every saved receiver ledger is broader observation coverage, not equivalent to reconstructing every intermediate whole-board state. The evidence and audit record preserve this distinction.

The source controls change only the designated source counters. Packet remainders, halo, receiver and guide are retained. All baseline and interaction source controls were checked directly; converter controls reconstruct the same declared geometry and preserve the stationary source-off preparation. No nonzero counter touches a periodic boundary in the baseline or interaction recordings. The full periodic guide is nevertheless part of their prepared environment.

## Specific failures and interpretation

At the baseline `(2,2)` receiver, the first packet lobe changes the remainder pair without an arithmetic C event. The target is lost at state 15. Thus absence of C is not sufficient evidence of lasting pending memory. The `(4,2)` receiver develops an unwanted channel-0 C at state 15. The independent audit checks counters, remainders and actual inputs together rather than treating a remainder pair as a complete record.

The interaction study has **zero control-eligible strict-cancellation groups**. In its fixed outlet window the opposite singleton also produces outlet C events, violating the required quiet control. Therefore the 15 groups are tested preparations, not 15 eligible instances of a cancellation test. Separately, every joint preparation has C activity at both outlets in the same fixed window, so even the weaker condition of a quiet joint outlet fails. No detector window was changed after observing these results.

All four initial source-control configurations retain distinct complete final states in every interaction group. `audit.json` records explicit final channel addresses and different counter/remainder triples witnessing the distinction between each singleton and the joint preparation. Local disappearance, if observed in a future experiment, would not erase this complete-state information. Present nonlinear interactions alone are not approval, selection or quantum collapse.

The separately frozen inverse-preparation search has a different evidential burden. Applying the inverse to a chosen endpoint and then returning to it by forward evolution is a construction identity. It does not demonstrate that an arriving source writes a new record. The independent audit therefore checks the predeclared ready receiver and source box before examining forward behavior. None of the 54 preparations passes either combined eligibility requirement. All begin with the target pair already installed; all have active counter contamination outside the permitted source box. The matched source-box-off controls preserve every outside counter and every remainder. Some such controls retain the target or become locally quiet, but they cannot count as clean source-absent preparations or successful writes. All inverse operations occur in external initial preparation, never in the recorded forward runtime.

A zero-counter receiver that has no guarded C throughout an interval must have zero quotient throughout it. This follows inductively: a nonzero quotient starting from zero counters produces a changed counter triple, hence C. Consequently each channel satisfies `r(t)-r(0)=2*sum(u)` through such an interval. A balanced actual input cannot leave a changed quiet remainder. This is a conditional algebraic obstruction; it does not prohibit a different initial converter from producing an unbalanced receiver waveform.

One fixed complete initial board determines one trajectory. Simulating a family externally is a search over initial preparations. It is not evidence that a board internally enumerates all alternatives or computes a maximum of complexity. A preloaded second signal would test an arrival interface; it would still need a causal construction showing where a comparison inside the board generated that signal. No such closed decision mechanism, entanglement, Born probabilities or physical time direction is established here.

## Integrity checks and reproduction

The review checks frozen protocol hashes, source manifests, every retained record hash, decoded state hashes and exact initial preparations. Interaction probe and assembly hashes are checked on their canonical decoded contents so lossless compression cannot conceal semantic changes. All stored failures remain represented; no result is hidden by filtering to detected trials.

Three deliberate corruption tests verify that the audit rejects a rehashed altered source halo, a rehashed incorrect later transition, and forged six-neighbor contributions whose signed sum remains unchanged. Run:

```bash
python -m unittest tests.test_message_mechanism_audit -v
python -m research.message_mechanism.audit \
  --baseline research/message_mechanism/evidence/baseline_v1 \
  --discovery research/message_mechanism/evidence/discovery_v1 \
  --interactions research/message_mechanism/interaction_evidence \
  --reverse research/message_mechanism/evidence/reverse_v1 \
  --output research/message_mechanism/audit.json
```

The next decisive question is whether a separately frozen initial preparation can write the same complete quiet receiver target for eight subsequent updates. Any discovery hit needs independent replay and fresh geometry plus declared amplitude/sign perturbations before a reusable component claim. Approval and cancellation should be tested only after a working pending interface exists, with isolated-source and stale-message controls. A failure may motivate a new initial-preparation family; it does not authorize a runtime gate or a change to Rule3.
