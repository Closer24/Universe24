# Source-driven component composition — U24-COMPONENTS-v1

A single prepared front starts two local clock projections and writes two finite
records in the same unchanged Rule3 lattice. Both readouts work together on two
new guide lengths. The registered perturbation family is fragile, and none of
the 24 control-source preparations meets the registered clutch requirement.
These are finite computational results for a prepared medium, not evidence for
physical light, spontaneous component assembly, permanent memory or a reusable
clutch.

The [frozen protocol](../research/building_blocks/component_protocol.json),
[runner](../research/building_blocks/component_study.py) and
[complete results](../research/building_blocks/component_results.json) record
successes and failures. The protocol was saved before execution in this session;
this is not independent timestamped preregistration. The code uses engine
baseline `ed1556e202eb0f3cc60342c75d44012c2eeb71c3`, positive body signs `(1,1,1)`
and coupling fingerprint
`44b672d96111e71a145a2a74cc93c83d41d917140e979186c308a5ecd52c6f77`.

## Preparation and fixed interface

All unspecified channels have `(a,b,r)=(0,0,2)`. Set
`origin=(L//2-N//2,L//2,L//2)`. At the origin, source channels 0 and 14 hold
`(0,1,2)` and `(0,-1,2)`. For each guide position `origin+(j,0,0)`,
`j=1,...,N`, those channels hold `(0,0,4)` and `(0,0,0)`.

Every subsequent update is `Engine.advance`; there is no insertion, removal,
switch or coupling change during a run. The source is part of the initial state.
The other prepared counters start at zero. The prepared remainders are part of
the apparatus, not a new dynamical rule.

| Component | Preparation and environment | Input and output | Response and declared scope |
|---|---|---|---|
| Candidate signal | Source pair plus finite straight guide | Counter activity entering the prepared next receiver | First activity arrives at receiver j at update j in the successful cases |
| Local clock | Receiver's channel-0 and channel-14 counters | Arrival starts channel-0 cycle `(0,1),(1,0),(0,-1),(-1,0)`; channel 14 is its negative | Projected period four during the first record window, not a period of the whole board |
| Memory | Receiver remainder pair | `M=1` exactly when `(r0,r14)=(0,4)` | First window `j <= t < 2(N+1)-j`; temporary record |
| Recorded click | Passive rising-edge readout of that internal bit | `M(t-1)=0` and `M(t)=1` | Zero added state change; distinct from the engine's existing arithmetic C0/C1/C2 classification |
| Composed receivers | Two readouts along the same prepared guide | One source successively activates both | New N=24 and N=28 preparations; no separate detector rule |
| Clutch candidate | One guide pair replaced by vacuum; transverse preloaded control pair | Tested whether the control source allows data to reach a downstream record | No preparation meets the four-sample retention and single-source-null criteria |

**A mathematical source-absence condition:** any state with every counter
`a=b=0` is fixed, even when the valid remainders vary spatially. Every neighbor
sum is zero, so `divmod(r,6)=(0,r)` and the update returns the same triple. Thus
this prepared apparatus cannot start itself when both sources are removed.
This is a property of the specified initialization, not a claim that every
allowed Universe24 preparation requires an external source or physical light.

## Composed runs

The readout and four-phase expectation were held fixed throughout all runs.
The window duration counts sampled states; `[6,44)` contains 38 samples.

| N | L | Receiver j | First click | First record window | Samples retained | Later clicks observed |
|---|---|---|---|---|---|---|
| 24 | 161 | 6 | 6 | `[6,44)` | 38 | 56, through update 64 |
| 24 | 161 | 12 | 12 | `[12,38)` | 26 | 62, through update 64 |
| 28 | 181 | 8 | 8 | `[8,50)` | 42 | 66, through update 72 |
| 28 | 181 | 16 | 16 | `[16,42)` | 26 | None through update 72 |

Both simultaneous receivers satisfy their exact first-window memory and clock
criteria. Each corresponding source-absent run stays equal to its complete
initial state at every sampled update and produces no click. Composition here
means two functioning readouts in one connected preparation. It does not yet
establish interchangeable modules, branching networks or arbitrary attachments.

Later clicks are explicitly retained. Neither temporary reset nor a zero
readout establishes information erasure; every final state reconstructs its
complete initial state by the exact inverse.

## Perturbations and failures

The registered Cartesian family combines five source counter phases/amplitudes
with six target remainder-pair choices at both N=24 receivers. Only the original
`source (a,b)=(0,1)`, target remainders `(4,0)` preparation passes all original
arrival, phase and first-window criteria: **1 of 30 cases**.

This is a strict interface test. A phase-shifted signal may still transmit
influence while failing the original time/phase requirement; those failures are
not assertions that no useful behavior exists. Likewise, changing an initially
armed readout to one with M already equal to one is not a source-triggered
record under this protocol.

For the source `(0,1)` and target remainders `(5,0)`, arrival and the counter
cycle still satisfy the original timing, but no M click occurs. The channel-0
remainder stays odd, while M requires it to be zero. This exposes a readout
limitation directly. Even-parity changes also fail this strict interface: for
example `(2,2)` gives delayed activity and multiple short records. The runner
keeps all traces, including these failures.

## Control-source search and the near miss

For N=14 and L=101, replace the pair at guide index k with vacuum `(0,0,2)` in
both channels. Place the control source one site in the +y direction from that
gate. The fixed coupling selects its channels 2 and 24. Their initial triples
are `(A*a,A*b,2)` and `(-A*a,-A*b,2)`, for four quarter-cycle `(a,b)` choices and
amplitudes `A=1,2`. Gate positions `k=3,4,5` give 24 preparations. Every
preparation is tested with neither source, data alone, control alone and both.
The target is j=k+3 and all four cases run through update 24.

Acceptance requires only the two-source case to produce a target click by
`k+8`, at least four consecutive samples of its first record, and no
single-source target click through update 24. For the stronger stored-control
criterion, the control-only gate must additionally be at rest, armed with
remainders `(4,0)`, and have zero input at `t=k-1`, immediately before data
would arrive. **No candidate passes even the first criterion.** The conditional
held-out tests were consequently not triggered; zero executed holdouts cannot
be interpreted as validation.

A useful near miss occurs at k=3 with `(a,b)=(-1,0)` and `A=1`:

| Sources present | Gate at t=2 | Input to gate at t=2 | Target j=6 clicks through t=24 | First record |
|---|---|---|---|---|
| Neither | Vacuum `(r0,r14)=(2,2)` | `(0,0)` | None | None |
| Control only | At rest, armed `(4,0)` | `(0,0)` | None | None |
| Data only | Vacuum `(2,2)` | `(1,-1)` | None | None |
| Both | At rest, armed `(4,0)` | `(1,-1)` | 6 and 20 | `[6,7)`: one sample |

The control source really changes the gate's stored state before data arrives;
the successful early target response is not explained by control input at that
same update. However, its first record lasts only one sample, so the registered
four-sample criterion fails. It is a reproducible short conditional response,
**not an accepted persistent clutch**. The later response at t=20 also rules out
an assumed one-shot interpretation.

Another limitation is that a vacuum gap is not a universal blocker. With k=4,
data alone produces downstream target j=7 clicks at t=15 and t=21. A different
gap location or a shorter observation horizon would conceal this delayed
transmission. This is why the control horizon is part of the interface.

## Verification, budget and reproduction

The study completes 130 runs and 4,136 forward updates. Every update has an
exact full-state one-step inverse check; every final state is additionally
rewound through its entire trajectory. All pass. Complete normalized-state
trace hashes, exact deterministic preparation parameters, target counter and
remainder traces, source hashes and the coupling fingerprint are retained.

All observed nonbackground support remains away from the periodic boundary.
The N=24/N=28 runs additionally have initial boundary margins greater than their
respective 64/72-update horizons, excluding wrap influence by the one-link per
update causal bound. This does not certify arbitrary longer runs.

The frozen budget is 120 CPU seconds, 300 wall seconds and 20,000 explicitly
stored channels. The recorded execution took approximately four CPU seconds.
Budget exhaustion is recorded as inconclusive, not as failed physics. Failed
scientific component criteria remain present even when execution and inverse
checks succeed.

From the repository root:

```bash
python -m research.building_blocks.component_study --output runs/component-rerun.json
```

Create the output parent directory first if needed. Existing output files are
never overwritten. Compare scientific fields while excluding the recorded
runtime durations and interpreter metadata when appropriate.

The next decisive experiment should register a new control-source preparation
that separates the priming pulse from its later counter-phase reversal, and
validate it on new gate locations, source phases and retention horizons. The
current one-sample near miss supplies a concrete target; it does not justify
weakening the four-sample criterion after seeing the result. No core or tensor
change is required to state that test, and none was made here.
