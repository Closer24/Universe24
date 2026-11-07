# Prepared signals across the fixed tensor family

## Question, protocol and evidence

Can the same initial guide transfer a signal through the eight existing signed
tensors, and do simple unprepared seeds give an exactly translating compact state?
This study varies **only initial triples and the tensor selected before a run**.
It uses the unchanged `Engine.advance`; observation never changes the state.

The [frozen protocol](../research/building_blocks/signal_protocol.json),
[executable study](../research/building_blocks/signal_study.py) and
[complete case results](../research/building_blocks/signal_results.json) belong
to `U24-SIGNAL-FAMILY-v1`. The protocol was written before computation in this
session; this is not an externally timestamped registration. The pinned engine is
`ed1556e202eb0f3cc60342c75d44012c2eeb71c3`. The result records protocol, runner and
all engine-file SHA-256 digests, each tensor fingerprint and each deterministic
initial-state generator. No random generator is used.

All **160 registered cases** completed: 96 guide preparations, 24 controls and
40 unprepared compact motifs. The 4,992 forward steps each passed exact one-step
inversion, and every final state rewound through the complete trajectory to its
initial state. The run took approximately 4.3 CPU seconds locally, below the
120-second ceiling; no 20,000-channel support ceiling was reached. Timing is an
environment-dependent execution metric, not a physical result.

## Component interface and readouts

The environment is a cube of side 151, background `(0,0,2)`, source position
`(60,75,75)`, and receivers at `(60+j,75,75)` for `j=1,...,N`, with `N=24` or 28.
The source uses channels 0 and 14, respectively `(a,b,2)` and `(-a,-b,2)`.
The guide receivers initially use `(0,0,4)` and `(0,0,0)` on the same two channels.
All other channels remain at the background. Each preparation runs for `N+12`
updates. The causal radius is smaller than its margin to every periodic boundary,
so a boundary crossing cannot affect these runs.

| Interface | Fixed definition |
|---|---|
| Input | Source phase/amplitude `(a,b)` in `(0,1),(1,0),(0,-1),(-1,0),(0,2),(0,-2)` |
| Signal arrival | First sampled time with nonzero channel-0 `b` at receiver `j` |
| Registered speed success | All arrivals equal `j+d` for one delay `d` in `{0,1}` |
| Local memory | `M_j=1` exactly when the remainder pair `(r0,r14)=(0,4)` |
| Click | A sampled rising edge of that same local memory bit |
| Outputs | Complete arrival vector and memory/click traces at `j=6,12` |
| Applicable range | Exactly the specified lengths, source alphabet, eight fixed tensors and run horizons |

These readouts were fixed in the protocol. The memory is a function of internal
retained states; the resulting log is external and passive. A signal here is an
activation front in a **prepared medium**. It is not yet physical light, a free
wave in an unprepared medium, or a compact object moving without leaving a record.

## Observed outcomes

Exactly **24 of the 96 guide cases** satisfy the registered unit-speed criterion.
For both guide lengths, these are the four choices with body-axis sign `s_x=+1`
and each of the following source states:

| Source `(a,b)` | First arrival at every receiver | Target click behavior in the measured horizon |
|---|---|---|
| `(0,1)` | `t=j` | One click at `j=6` and one at `j=12`; the bits remain set through the run end |
| `(-1,0)` | `t=j+1` | One click at `t=7` and one at `t=13`; a one-update source delay |
| `(0,2)` | `t=j` | Repeated target clicks at `j,j+6,j+12,...` within the horizon |

The other 72 guide cases fail this particular complete-guide unit-speed
criterion. Failure does not mean that every form of influence vanishes.
For example, for `s_x=-1` and source `(0,-1)`, reached receiver prefixes have
observed arrivals `1,4,7,10,...`; `(1,0)` shifts this to `2,5,8,11,...`.
Farther receivers are not reached within the registered horizon. This partial
slower pattern is an observation, not a separately confirmed all-length speed law.
A later study must freeze an appropriate longer horizon before promoting it.

The measured guide arrival and target-memory readouts agree across the four
choices of transverse signs at a fixed `s_x` and source state. This does **not**
assert equality of the complete microscopic states for different tensors, or
isotropy under arbitrary spatial orientations.

All 24 controls have no target click: eight tensors each with (1) no source,
(2) no prepared guide, or (3) the prepared pair at `j=3` omitted. In the positive
`s_x` gap cases, receivers 1 and 2 activate, but receivers beyond the gap do not
activate during the horizon. The missing receiver was fixed in the initial
condition; this is not an external runtime switch. For the no-source preparation,
all counters are zero. The exact Rule3 equation then leaves every remainder and
counter unchanged, so the apparatus is a fixed point until a nonzero input is
present in its initial causal environment.

These controls demonstrate source dependence of this restricted device. They do
not prove that all possible clocks must be driven by a signal: nonzero initial
counter preparations can already contain an autonomous oscillation. Nor is source
dependence an established energy-transfer law.

## Compact translating-pattern search: negative result

The registered compact search used side 61, source center `(30,30,30)`, background
`(0,0,2)`, all eight tensors, and five motifs: channel-0 amplitudes 1 or 2, opposite
channel-0/14 amplitudes 1 or 2, and the prepared clock pair
`(-1,-1,0)/(1,1,4)`. At each of updates 1 through 12, the **entire retained state**
was compared with the initial state translated along a coordinate axis by one or
two sites in either direction. Remainders, absent background entries and support
size were included. This defines 5,760 time/shift comparisons across 40 runs.

There were **no nonzero-shift certificates** in that finite domain. Instead,
all amplitude-1 and clock-pair motifs returned exactly at updates 4,8,12, and
all amplitude-2 motifs at 6,12. This is evidence of recurrence in these seeds,
not a general impossibility proof for moving patterns. The test excludes a
projection-only traveling appearance from being counted as a full-state packet.

## Limitations and next decisive test

This study establishes finite transfer and source-dependent local recording in
prepared guides. It also demonstrates that changing source amplitude from 1 to 2
changes the number of clicks while preserving the first-front speed. Thus the
same device does not have amplitude-independent one-shot recording on this input
alphabet. Source phase and the longitudinal sign matter; a universal all-tensor
unit-speed claim fails. These limitations remain visible in the full result data.

Neither broad spontaneous emergence, free physical light, arbitrary-axis
isotropy, an energy or momentum law, permanent detector storage, nor a reusable
autonomously switching clutch follows from these runs. The guide and readout are
engineered initial preparations, not an ensemble of naturally emerging devices.

The next decisive propagation test is a new registered family with (a) a longer
horizon for the observed slow-front prefix, (b) the channel/spatial transformation
needed to orient the same guide along different axes, and (c) source amplitudes
held out from discovery. It must keep arrival and memory definitions fixed and
separate first-arrival speed from sustained pulse shape and record persistence.

Reproduce without overwriting the retained result:

```bash
python -m research.building_blocks.signal_study --output runs/signal-family-repeat.json
```

Compare the resulting JSON with the retained result after excluding only
`runtime_cpu_seconds` and, when intentionally comparing Python versions, the
`python` environment field. Source identities, generators, scientific outcomes,
state digests and inverse results must agree exactly.
