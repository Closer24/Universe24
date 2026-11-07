# Independent review of clockwork building blocks

This review distinguishes implementation agreement, accepted finite behavior,
failed scientific criteria and unresolved physical interpretation. It reviewed
the unchanged engine baseline `ed1556e202eb0f3cc60342c75d44012c2eeb71c3`
with the new research preparations and replay tooling. It does not establish
that the activation front is physical light.

## Independent checks

[test_building_blocks_review.py](../tests/test_building_blocks_review.py) contains
nine executable regressions. Its comparison executor gathers each receiver's
inputs using the separate exact-matrix algebra in `research/reference/`; it
imports neither production routing tables nor the production scalar update.
Its guide generator is separate from the published preparation generator.

| Check | Domain and observed result |
|---|---|
| Quiescent apparatus | A nonuniform remainder preparation with all counters zero, all eight sign triples, L=3, four updates: every complete state stays fixed. |
| Independent complete evolution | N=8, L=61, 24 updates, complete guide, no source, gap at j=3 and odd remainder at j=2: all 96 complete updates equal the independent matrix-based gather; all engine step inverses and complete rewinds pass. |
| Finite record and clock | N=8, target j=2: first record is `[2,16)`, the declared four counter phases hold, and the memory rises again at t=20. |
| Triggering versus continuous drive | The same receiver has measured net input zero through eight postactivation transitions while its counter clock continues. |
| Parity and readout | An odd target remainder permits counter activity but never matches the exact even-parity memory predicate. A phase-only replacement readout is explicitly rejected. |
| Published preparation and passive readout | All seven assembly configurations equal separately constructed initial states. Reading pairs and memory leaves states and subsequent evolution unchanged. |
| Delayed gap leakage | N=24, gap j=10, target j=12: first activation t=32, record edges t=32,38,42,50 through t=56. The frozen no-transfer criterion fails. |
| Incomplete horizon rejection | An N=8 run stopped at t=8 cannot certify the target-j=2 retention endpoint at t=16, even though all receivers have already activated. |
| Bundle corruption controls | Fresh generated bundles verify successfully while retaining scientific rejection. Changing a displayed memory bit, displayed spatial position, retained remainder or required renderer source identity is rejected. |

The first replay bundle was also checked directly against its retained
`states.jsonl` files. All **400 forward updates across seven trajectories**
matched the independent gather, including every retained counter and remainder.
Every displayed pair, local memory bit, rising edge, support count and checkpoint
digest matched the full saved state. This audit is separate from inspecting an
attractive animation. The later renderer/provenance corrections do not change
these numerical trajectories; the final packaged bundle should be subjected to
the same command below.

The independent executor shares the declared mathematical specification and
channel-label convention with the engine. This reduces implementation coupling
but cannot rule out a conceptual error in the specification. Finite comparison
alone is not a proof for every integer preparation.

## Rerun of the bounded studies

The reviewer reran the signal, component and structure-v1 studies directly,
without overwriting their retained files. Their deterministic result fields
matched exactly; only runtime CPU/wall fields were excluded. The 128 structure-v2
cases were independently rerun through their declared case generator and matched
all returned deterministic fields as well.

| Study | Reviewed finite outcome |
|---|---|
| Signal family | 160 completed cases: 96 guide preparations, 24 controls and 40 compact motifs. Exactly 24 guide preparations satisfy the registered common unit-speed arrival criterion. No registered nonzero-shift full-state certificate was found. |
| Composition and control | 130 completed runs. Both two-receiver guide preparations and their stationary no-source controls pass. Only 1 of 30 phase/remainder perturbations satisfies the original exact interface. None of the 24 four-input control-source candidate groups passes the coincidence/stored-control criterion. |
| Structure v1 | Recurrent and interacting preloaded counter motifs exist, but the strict support-only-at-initial-sites test fails because remainder halos are retained. Signal-created binding is not established. |
| Structure v2 | The new radius-one criterion passes in 72 of 128 cases and fails in 56. Failed radius-one cases reach radius two while retaining a short full-state recurrence. These are deliberately prepared oscillator clusters, not source-created matter. |

The preparation families are finite engineered examples. Neither a large basin
of simple random seeds nor spontaneous self-assembly was tested.

## Problems found and treatment

**Frozen gap hypothesis failed.** The assembly protocol predicted no activation
or record at j=12 through t=56 after omitting the receiver at j=10. The actual
state leaks influence and records at t=32. The original protocol and its hash
remain unchanged; the complete assembly protocol is therefore **not accepted**.
Successful complete-guide composition remains a separate, narrower result. A
shorter no-transfer observation window must not be substituted after inspection.

**Structure-v1 source-localization criterion was unsuitable.** Its source-created
success conjunction required the full state's support to stay at the two target
sites from t=0, although the source and guide were explicitly outside those sites
at t=0. That conjunction was impossible by construction. Its failure is a
protocol-design limitation, not evidence of a no-go theorem for signal-created
structures. V1 is retained; v2 registers a finite-halo criterion on new sizes and
counter phases and still does not claim source-created attachment or breakup.

**A clipped retention check could overclaim an unobserved duration.** The initial
exporter evaluated its counter/record predicates only on available samples. A
run shorter than the required endpoint could therefore look successful. The
exporter now requires the complete declared observation horizon, and a dedicated
negative regression covers this case. The originally registered runs were long
enough, so their outcomes are unaffected.

**Renderer provenance was missing.** The original source map covered the engine,
protocol, preparation and runner but omitted the HTML template. The renderer was
added to the fingerprinted inputs so a published representation is identified
alongside the states it displays. This is a reproducibility correction, not a
change to Rule3 or to a scientific readout.

**Verifier metadata required stronger checks.** A nonempty source map alone did
not establish that every dependency was identified, and displayed site positions
were initially unchecked. The verifier now requires the exact source map and
pinned core identities, reconstructs displayed geometry, and checks the complete
arrival map and support counts. Four deliberate corruptions in the new integrity
regressions demonstrate rejection. Verification success means that the saved
run and negative finding reproduce; the original scientific protocol remains
rejected rather than being relabelled as passed.

## Meaning of a signal-driven device

For any complete state with every `a=b=0`, each input sum is zero and
`divmod(r,6)=(0,r)`. Thus the entire state is fixed, for any allowed remainder
preparation and fixed tensor. A quiescent remainder-encoded apparatus cannot
self-start. Source-present versus source-absent comparisons are consequently a
well-defined test of triggering in this device family.

After arrival, a channel with zero net input obeys `(a,b)->(b,-a)` and can keep
cycling. This makes the demonstrated devices **signal-started**; it does not
establish continued energy delivery from light. Conversely, a preloaded nonzero
counter motif can already oscillate with no separate incoming source. Such a
motif must be reported separately from the quiescent-apparatus requirement.

The replay correctly retains exact integers alongside clock angles and remainder
gears. It separates the internal-memory edge from the engine's arithmetic
`C0/C1/C2` classification. Playback and scrubbing select saved frames; they do
not inject a pulse, operate a clutch, or evolve the model by an additional law.
Off-guide remainders remain part of the complete state even when the main visual
focus is channels 0 and 14 on the guide.

## Reproduction and decision

Run the independent regressions from the repository root:

```bash
python -m unittest discover -s tests -p test_building_blocks_review.py -v
```

After generating a fresh clockwork bundle, audit its complete retained states
and displayed fields with the separate gather implementation:

```bash
PYTHONPATH=tests python -c "from test_building_blocks_review import audit_recorded_replay; print(audit_recorded_replay('runs/clockwork-first'))"
```

Replace the explicit bundle path when reviewing a different generated result.
The audit returns seven scenarios and 400 independent complete updates for the
registered assembly protocol. It does not overwrite evidence.

The evidence supports a reproducible prepared front that starts two counter
clocks and finite internal records. It also preserves failures of gap blocking,
phase/parity robustness, the tested autonomous control-source candidates and
compact translation in the declared search family. The next decisive component
test is a newly registered control-signal preparation with a fixed downstream
readout, enough time to detect delayed leakage, and all four source/control
combinations. No physical-light, reusable-clutch or matter claim should be
promoted before those separate requirements are met.
