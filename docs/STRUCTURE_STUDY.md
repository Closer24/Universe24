# Prepared oscillator clusters and limits of binding claims

This study changes only initial states and one of the existing eight fixed
coupling sign triples. Every transition uses the unchanged reference engine.
The results concern prepared integer-state structures; physical matter, spatial
binding and autonomous assembly are not established.

## Registered questions and evidence

The [v1 protocol](../research/building_blocks/structure_protocol.json) was frozen
before its runs. It tested isolated clocks, adjacent and separated copies,
and two incoming-signal interfaces. Its [23 complete cases](../research/building_blocks/structure_results.json)
each ran 40 updates with all one-step inverses and a complete rewind passing.

V1 revealed that the retained remainders around a clock are part of its state.
The [v2 protocol](../research/building_blocks/structure_protocol_v2.json) was then
registered before new runs on L=31 and L=37. It tested a predeclared radius-one
halo rather than deleting that state from the definition. Its [128 cases](../research/building_blocks/structure_results_v2.json)
each ran 42 updates; all full-state inverses passed. V1 is retained unchanged.
These are within-session registrations, not independently timestamped studies.

Each result includes the complete initial and final checkpoint, tensor
fingerprint, source hashes, protocol, full-state trace hashes, fixed readouts
and runtime. A script can regenerate every intermediate state from the initial
checkpoint. The recorded checkouts were dirty during parallel development;
source hashes identify the actual executed files. An acceptance run from a
clean publication commit should be retained separately.

## The prepared interface

All unspecified channels begin at `(a,b,r)=(0,0,2)`. The canonical oscillator
at a site uses channel 0 `(-1,-1,0)` and channel 14 `(1,1,4)`. A two-site
motif places an identical pair one x-step away. These counters are nonzero at
t=0: this preparation is preloaded and is not source-activated.

| Component | Input and output | Response and tested range |
|---|---|---|
| Isolated clock plus halo | Preloaded counter pair; full-state recurrence | Period 4 for the canonical seed, all eight sign triples |
| Adjacent recurrent cluster | Two preloaded pairs one x-step apart; interacting recurrence | Period 5 when the fixed x sign is +1; period 7 when it is -1 |
| Separated copies | Same pair at separation 3 or 6, positive signs | Period 4 and no target-triple difference from separate isolated copies through t=40 |
| Separation-2 interaction | Same pair two x-steps apart, positive signs | Difference from separate clocks at t=2; no full return in the registered t=1..12 search; maximum sparse support 550 through t=40 |
| Signal into preloaded pair | Prepared guide into an already moving pair | Source changes the target by t=16; source-absent target is already active |
| Signal into quiescent receivers | Same guide, target counters initially zero | Activation at target positions j=9 and j=10; source-absent targets stay inactive through t=40 |

The initial tensor is fixed for each run. Its signs change between experiments,
never during a trajectory. These period differences do not derive an effective
`num/den` law or a physical gear ratio from a family of dynamical equivalences.

## Complete-state halo and phase sensitivity

A clock diagram showing only the two local counter triples omits retained
state. In v1, an isolated canonical clock visits up to 14 nonbackground
channels; its adjacent counterpart visits up to 24. Both fail the registered
strict two-site support criterion. This failure is visible even though the
entire states recur exactly. It does not show that no finite oscillator cluster
exists.

V2 includes every retained remainder in its support. The registered radius is
the minimum toroidal Manhattan distance to an initially prepared motif site.
Four channel-0 counter pairs were specified in advance, with remainder 0;
channel 14 has negated counters and remainder 4. The surrounding halo always
starts at the uniform background. Each row below occurs for both cube sizes
and all four choices of the y/z signs (eight cases per x-sign entry).

| Channel-0 counters | Isolated: period / radius | Adjacent, x sign +1: period / radius | Adjacent, x sign -1: period / radius |
|---|---|---|---|
| `(-1,-1)` | 4 / 1 | 5 / 1 | 7 / 1 |
| `(-1,1)` | 6 / 2 | 6 / 2 | 3 / 1 |
| `(1,1)` | 4 / 1 | 5 / 1 | 7 / 1 |
| `(1,-1)` | 6 / 2 | 7 / 2 | 6 / 2 |

Thus **72 of 128 preparations pass the registered radius-one criterion**;
56 fail it. All 128 have a full first return within seven updates and exact
repeated-state equality through t=42. Radius two is a reported observation for
the failed cases, not a replacement for their registered radius-one criterion.
The minimum active boundary distance is 12, so no active value needs a wrapped
port during these runs.

Changing only local counter values while resetting the halo is not a phase
shift of the complete clock state. A composable phase interface must preserve
or deliberately prepare that halo. The canonical adjacent cluster has a
bounded complete-state period-5 or period-7 recurrence and interacts already
at t=1; this is a sound finite computational primitive. Calling it a pair of
particles that bound together would add a claim not tested here.

Exact recurrence also gives a conditional mathematical implication: for a
deterministic map F, verified equality F^p(S)=S implies F^(t+p)(S)=F^t(S) for
all t by applying F^t to both sides. A finite engine calculation supplies the
recurrence certificate for these seeds; it is not a proof that every seed has
such a recurrence or that the implementation is universally correct.

## Signal control, failed criteria and an unsuitable criterion

The signal trials use a source at `(50,60,60)`, prepared guide receivers at
x offsets 1 through 8, and two target sites at offsets 9 and 10. The source
pair is `(0,1,2)` and `(0,-1,2)`; an inert guide/receiver pair is `(0,0,4)` and
`(0,0,0)`. All preparations are fixed before t=0. The local record is
`M=1 iff (r0,r14)=(0,4)` and a click is its rising edge.

With initially quiescent targets, source-absent counters stay zero, while the
source-present case activates them at t=9 and t=10. Their record rising edges
are `[9,31]` and `[10,32]` through t=40. The registered target-period-five test
fails: target triples are not equal at every `(t,t+5)` pair for t=16,...,30.
With preloaded targets the period-five test also fails, and the no-source
control is already active. These are finite findings about the specified
interfaces, not a prohibition on all source-created clocks.

**V1's `created_source_driven_localized_period5_structure` conjunction is an
unsuitable acceptance criterion for the signal cases.** It reuses a bound
requiring every nonbackground value to stay on the target sites from t=0,
but the initial source and prepared guide already lie outside them. Its false
value is therefore a protocol-design failure and is **inconclusive** about
source-created structures. The source-response, inactive-control and local
period-five fields remain separately interpretable. V2 repairs only the
bare-motif halo question; it does not retroactively repair that signal criterion.

No run demonstrates two identifiable moving motifs joining and subsequently
separating. Neither recurrence, a changed period, nor disruption by an incoming
front is by itself attachment or breakup. No physical light or matter claim
follows from these observations.

## Reproduction and next decision

Use new output filenames; neither script overwrites existing evidence:

```bash
python -m research.building_blocks.structure_study --output runs/structures-v1.json
python -m research.building_blocks.structure_confirm --output runs/structures-v2.json
```

Compare the deterministic case data; runtime, checkout metadata and development
working-tree state are reported separately. Budgets are 120 CPU seconds and
20,000 explicitly stored channels per run family. Exhaustion is inconclusive.
The completed families took approximately 0.4 and 1.7 CPU seconds respectively
on the recorded interpreter; this timing is not a physical observable.

The next decisive source-driven test needs a fresh protocol: include a
predeclared full-state halo and the guide's wake, require an inert source-absent
control, then test whether an arriving signal creates a recurrent cluster with
a stable interface on held-out seeds. An attachment/breakup claim additionally
requires operationally identifiable motion before and after contact. The
present result justifies visualizing and composing prepared recurrent clusters,
while retaining their source-independent preparation and phase limitations.
