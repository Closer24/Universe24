# What the observer can recover from clicks

The installed `universe24/observer.py` provides passive observations whose input
is the canonical `clicks.jsonl.gz` stream. Its observer functions do not read
the seed, complete trace, latent field, spatial metric or Engine history.
The source-only `validation/click_observer_audit.py` harness separately prepares/runs complete bundles and compares the
results with independent complete-state replay. Neither observer feeds the
Engine.

The installed arithmetic record already contains `quotient`, `kind`, `sign`,
channel, node/xyz addresses and provenance. This audit retains those semantics.
Addresses identify locations in the computation; they are not measured physical
distances. A step index is not a material clock's proper-time reading. The
record's `run_id` and `event_id` are provenance, not extra detector measurements.

## Click-only retained memory on an explicitly calibrated domain

The new installed detector law in `universe24/detection.py` supplies a retained
light-to-memory exchange. Its existing `detect` audit uses complete states to
validate exchanges. The added click-only reconstruction needs the following
**public calibration**:

- The declared detector tensor and the memory-channel address.
- The set of node addresses and the complete observation horizon.
- Zero initial memory in both retained histories.
- The declared nonnegative-amplitude exchange sector and constant carries.

No light amplitude, incoming field, arming state, coordinate metric or hidden
memory history is provided to the observer. Its own inferred histories are
passive analysis results, not extra retained universe channels.

For a memory click on update `t`, the recorded quotient is
`Q_t=M_t+M_(t-2)`. Known previous histories therefore give
`M_t=Q_t-M_(t-2)`. On a quiet update there are two possibilities in the
canonical protocol: the complete triple stayed fixed, or the quotient was
zero. Nonnegativity and the known two previous histories distinguish these
possibilities. If the two old histories agree, memory stays fixed; otherwise
the zero-quotient possibility requires `M_t=-M_(t-2)>=0`.

This inference includes releases as well as captures. A retained memory cell
is not counted anew during every quiet tick. A capture ordinarily generates
two arithmetic transition clicks, one for each settling history, rather than
two capture events. An inference based on a quiet tick is explicitly marked.
The observer does not infer hidden arming opportunities or classify quiet
memory as an arming opportunity with no transfer.

All recovered memory changes and quadratic memory accounts are compared
against the installed detector's complete-state observer. This independent
comparison is validation evidence, not an input to click-only reconstruction.
It establishes the stated calibration, not inversion of arbitrary latent
states and not photon-number calibration.

## Completed controls

Fresh evidence: `runs/click-observer-20261113-v2/results.json`.
Ten complete bundles ran through the existing runtime for 64 updates total.
All passed saved forward replay, exact inverses/rewind and canonical click
parity. The distinct tensor families remain separate experiments.

| Control | Observation |
| --- | --- |
| Two different stationary positive seeds | Exactly identical empty click files; clicks alone do not identify the latent state |
| Same light amplitudes, different retained constant carries | 1,470 clicks each; all observational fields, including quotients, agree; provenance IDs differ |
| Matched-phase clock alone | 7,776 arithmetic clicks |
| Same phase clock plus light | 7,812 arithmetic clicks; first-click time at every node remains identical to the clock-only control |
| Armed detector, unit amplitude | 650 arithmetic clicks; click-only memory recovery matches complete-state exchanges |
| Armed detector, no light | 400 arithmetic arming clicks, zero captures |
| Unarmed detector, light present | 400 arithmetic light clicks, zero captures |
| Armed detector, doubled amplitude | Same 650 arithmetic clicks and occupied-cell transfer counts, with four times the quadratic memory account |

The detector preparations use a `5^3` periodic lattice, light at address
coordinate 0 and arming at 3, with eight updates. The armed preparations
capture 25 memory cells on update 2 and release them on update 7. Their 100
memory arithmetic clicks correspond to 50 memory changes, not 100 photons.
The unit-amplitude peak memory account is 25; the doubled-amplitude account
is 100. Neither account is calibrated in joules or `hbar*omega`.

The first-recorded-click map is deliberately named that way. Clock/background
activity can already produce a click at every node before a putative optical
arrival. Matched light/no-light controls show that the complete click payload
can distinguish the two preparations, while the first-click map cannot. This
does not identify a physical photon from an uncalibrated single record.

For nonempty cross-run equality, only `run_id` and `event_id` are excluded,
and that exclusion is reported. Full canonical records of different runs
are not claimed byte-identical. Quotients are never dropped: adding a uniform
amplitude bias generally changes them even when click support/classes agree.

## Reproduction and limits

```bash
python -m validation.click_observer_audit --out runs/new-click-observer
python -m validation.click_observer_audit --clicks runs/new-click-observer/detector-armed/clicks.jsonl.gz
```

`reconstruct_memory_from_clicks(path, memory_channel=..., node_count=..., steps=...)`
in `universe24.observer` is the reusable calibrated observer. Per-detector `click-only-memory.json`
files contain the inferred changes, preserved arithmetic event IDs, account
history and explicit assumptions.

Record syntax checks cannot discover every omitted valid event. The complete
saved-run replay is what establishes click-stream completeness and the
observation horizon. An empty file alone does not tell the observer how long
the system ran or whether the experiment was silent.

The installed reader rejects malformed or duplicate JSON fields, invalid event
IDs/signs, mixed run/tensor provenance, duplicate events and noncanonical
ordering. Reconstruction also rejects calibration bounds, an uncalibrated
tensor and histories incompatible with nonnegative memory. Eight active I/O
contract tests cover these checks, pure click-file operation, explicit
provenance projection and arbitrary-size integer observations. They do not
introduce another physical model or research acceptance suite. The original
collection directory is preserved; v2 uses this installed observer and the
stronger input checks.

The results do not identify dark matter, a shared metric, geodesics, proper
clocks, Born probabilities or photon number. In particular, a component dark
to an electromagnetic readout need not be dark to arithmetic clicks, and
absence of clicks is not a dark-matter detection. Those physical questions
remain separate from the demonstrated click-only memory inference.
