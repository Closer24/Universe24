# Message mechanism research

This research asks whether an unchanged Rule3 board can supply the actual input waveforms needed for a quiet pending memory, later approval or cancellation, and eventually an internal comparison between finitely represented alternative routes.

**Base:** `0d4c4805be67b0efc42e084416ff2204529a1e07`. All new preparations use the existing fixed `+++` tensor. The engine, coupling construction, released component library, generic Presenter and frozen model specification remain unchanged. Source schedules are encoded in the initial board only.

Four bounded studies are complete: an 18-run baseline, a 62-run interaction family, an 891-preparation stationary converter search, and 54 reverse-designed preparations. **No new quiet-pending, approval or cancellation component qualifies.** The exact opposite-moving packet preparation is a constructive algebraic result. No autonomous complexity-based chooser or quantum interpretation is established.

The baseline has 0/9 accepted source-present quiet pending records; its nine source-absent controls remain stationary. The unmodified guide translates the complete prepared packet exactly through the 24-step horizon. The matrix oracle checked all 450 complete states and 432 forward plus 432 inverse baseline transitions, and all 1,998 states and 1,936 forward plus 1,936 inverse interaction transitions.

The opposed-packet study has 0/15 strict outlet-cancellation successes and 0/15 changed quiet records. It also reveals a failed control premise: isolated-source reflections leave no group eligible under the strict outlet-isolation predicate. Both joint outlets remain active. Thirteen groups exhibit nonlinear counter interaction, which is a diagnostic rather than an accepted message component.

The converter search has 0/891 accepted quiet pending records. It varies three on-row initial remainder pairs or one on-row and one transverse pair, retaining the source and fixed tensor. Every candidate completes its 40-step horizon and per-step engine inverse checks. The best quiet target in each family lasts two states, below the required nine. No discovery candidate is promoted and no positive holdout is claimed.

The independent converter audit checks all 891 stored local scalar traces and predicates. Its matrix oracle checks 12 retained full recordings and 16 failed preparations selected before discovery. Other unstored intermediate whole-board states are not claimed independently audited. See [`audit.json`](audit.json) for the exact scope.

The reverse search has 0/54 admissible initial preparations. Every proposed initial receiver already equals its desired pending target, and every preparation has active counters outside its fixed source box. Endpoint recovery after externally prepared inverse evolution is a construction identity, not a successful write. All 54 complete initial states and four full forward examples, including contaminated source-box-off controls, are retained.

The independent matrix audit checks all 54 initial preparations, their complete 33-hash inverse histories and 1,728 inverse/forward step checks. It also checks the four retained forward controls across 164 states and 160 transitions in each direction. These are validity checks of rejected preparations, not accepted building blocks.

## Contents and status

| File or directory | Purpose |
|---|---|
| [`../../docs/MESSAGE_MECHANISM.md`](../../docs/MESSAGE_MECHANISM.md) | Synthesis, exact claim boundaries and research decisions |
| [`protocol_baseline.json`](protocol_baseline.json) | Prospectively fixed 18-run packet/receiver interface and all acceptance predicates |
| [`compute_baseline.py`](compute_baseline.py) | Complete preparation, reference-engine execution, passive readouts and Presenter export |
| [`evidence/baseline_v1/`](evidence/baseline_v1/) | Registration, result, 18 compressed native recordings, full input traces and four-example Presenter |
| [`algebra.md`](algebra.md) | Conditional message identities, waveform constraints, full-board time reversal and information accounting |
| [`protocol_design.md`](protocol_design.md) | Bounded internal alternative/approval/cancellation protocol and missing components |
| [`protocol_discovery.json`](protocol_discovery.json), [`compute_discovery.py`](compute_discovery.py) | Separate 891-preparation remainder-converter discovery study; not a validated component |
| [`protocol_reverse.json`](protocol_reverse.json), [`compute_reverse.py`](compute_reverse.py), [`evidence/reverse_v1/result.json`](evidence/reverse_v1/result.json) | Fifty-four externally reverse-designed initial states; no admissible clean source or newly written memory |
| [`interaction_protocol.json`](interaction_protocol.json), [`interaction_evidence/summary.json`](interaction_evidence/summary.json) | Opposed-packet discovery and predeclared delay partition with all four source controls |
| [`audit.json`](audit.json), [`independent_review.md`](independent_review.md), [`audit.py`](audit.py) | Separate matrix oracle, complete-record and acceptance checks, with exact sampling scope |
| [`../../tests/test_message_mechanism_audit.py`](../../tests/test_message_mechanism_audit.py) | Three deliberate corruption regressions, including forged hashes and balanced false input terms |
| [`evidence/publication_v1/validation.json`](evidence/publication_v1/validation.json) | Fresh Git checkout: all 132 tests, standard impulse audits, identical combined scientific audit, scoped Presenter checks and browser limitation |

The baseline registration records protocol and source SHA-256 digests before execution. Its protocol digest is `9a397bfee30dcca86ff15c41085fa8182804b79ddf82cd9f959c9e93fa4c391f`. There is no random seed because every one of the nine even receiver pairs is enumerated with and without its source. Every unsuccessful trial remains in the evidence.

## Run the baseline

From the repository root, with Python 3.11 or later:

```bash
python -m research.message_mechanism.compute_baseline --output runs/message-baseline-reproduction
python -m research.message_mechanism.compute_discovery --output runs/message-converter-reproduction
python -m research.message_mechanism.compute_reverse --output runs/message-reverse-reproduction
python -m research.message_mechanism.interaction_search --output runs/message-interaction-reproduction
python -m research.message_mechanism.audit --baseline runs/message-baseline-reproduction --discovery runs/message-converter-reproduction --reverse runs/message-reverse-reproduction --interactions runs/message-interaction-reproduction --output runs/message-audit.json
python -m unittest tests.test_message_mechanism_audit -v
```

The output directory must not already exist. The generator saves all 18 full trajectories and actual receiver inputs. It builds the unchanged generic Presenter with four predefined examples, retaining the entire cube and all 48 channels rather than an invented two-channel simulation.

Open [`evidence/baseline_v1/The_Presenter.html`](evidence/baseline_v1/The_Presenter.html) in a browser with JavaScript enabled. Select an experiment, play or step through it, drag to rotate, and use Reset view to recover the full cube. A static attachment preview that does not execute JavaScript cannot play the experiments.

For a local browser, run `python -m http.server 8000 --bind 127.0.0.1` in the repository root, then visit [the baseline](http://127.0.0.1:8000/research/message_mechanism/evidence/baseline_v1/The_Presenter.html), [converter](http://127.0.0.1:8000/research/message_mechanism/evidence/discovery_v1/The_Presenter.html), [reverse preparation](http://127.0.0.1:8000/research/message_mechanism/evidence/reverse_v1/The_Presenter.html), or [interaction](http://127.0.0.1:8000/research/message_mechanism/interaction_evidence/interaction_presenter.html) page on the same computer. These links require the local server to be running; they are not hosted public demos. The interaction Presenter contains a four-control negative illustration selected after analysis.

Actual Chromium startup is blocked in this environment by `SIGTRAP` before a page loads. JavaScript/native-Canvas smoke checks have a narrower stated scope; neither those checks nor a static preview establish Safari/iPad layout compatibility.

The smoke checks pass all 18 bundled experiments: populated DOM experiment selectors, all saved steps/hashes and 48 channels, stepping/play/pause, synthetic drag, cube reset, all eight projected corners and unchanged recorded data, with no application JavaScript errors. Results are in [`evidence/presenter_smoke_v1/report.json`](evidence/presenter_smoke_v1/report.json) and [`evidence/presenter_smoke_reverse_v1/report.json`](evidence/presenter_smoke_reverse_v1/report.json). The reusable harness is [`presenter_smoke.cjs`](presenter_smoke.cjs); it requires Node.js, `jsdom` and `@napi-rs/canvas` and accepts a new output directory followed by any number of Presenter HTML paths. It emulates geometry explicitly and does not validate browser CSS or real pointer hit testing.

The recorded optional smoke environment uses Node.js `24.22.1`, `jsdom 26.1.0` and `@napi-rs/canvas 0.1.80`. With those packages available to Node:

```bash
node research/message_mechanism/presenter_smoke.cjs runs/message-presenter-smoke \
  research/message_mechanism/evidence/baseline_v1/The_Presenter.html \
  research/message_mechanism/evidence/discovery_v1/The_Presenter.html \
  research/message_mechanism/evidence/reverse_v1/The_Presenter.html \
  research/message_mechanism/interaction_evidence/interaction_presenter.html
```

The scientific Python generators and audits do not require these JavaScript testing dependencies.

| Presenter example | What it tests |
|---|---|
| `packet-r04-on` | Translation through the unmodified guide |
| `packet-r42-on` | A receiver defect that does not satisfy quiet pending retention |
| `packet-r22-on` | A counter-quiet receiver whose changed remainder is not retained |
| `packet-r42-off` | The same receiver preparation without the source |

These examples show the tested interfaces, including failures; they are not four accepted building blocks. A self-contained Presenter is a passive copy of native recordings. It is not evidence that a receiver emitted a decision, that the board ran every possible history, or that a detector outcome selected a physical world.

## Evidence rules

1. Freeze state predicates, time windows, case families and controls before scientific validation.
2. Keep every trial denominator and distinguish designed discovery from prospective fresh holdouts.
3. Save complete states, actual signed inputs, source/tensor/protocol hashes and inverse checks.
4. Check all 48 receiver channels, not only a favorable remainder pair.
5. An ordinary packet supplied at a fixed initial offset can test a message interface; an autonomous decision requires a message generated by the internal comparison apparatus.
6. A quiet outlet or restored receiver is local behavior. Full-state information must remain recoverable.
7. Promote a new block only after its preparation, ports, environment, response/retention horizon, controls and composition domain are explicit and validated.

The preceding study and its different probes remain in [`../light_approval/`](../light_approval/README.md). This study does not overwrite those protocols or reinterpret their failed pending/confirmation criteria as successes.

The next proposed stage is a separately registered initially active transverse converter, with a clean ready receiver and matched apparatus/source controls. Neither apparatus alone nor source alone may write the declared pending record or produce a receiver click record; a preexisting oscillation alone is not signal-activated memory. The confined-row translating phase-front family has a proved narrow obstruction; lengthening that pulse is not a solution under the same assumptions. These results motivate a new preparation family within the unchanged model, not a new evolution law.
