# Two initially complete clocks: bridge activation without finite formation

All 48 registered runs completed, with 4,656 full states, 4,608 transitions and 48 complete rewinds. Independent replay agrees with every recorded observation and all twelve four-mask comparisons. **Zero of twelve geometries pass the registered stationary-composite formation criterion.** Equal-phase clocks separated by two sites activate an intermediate bridge and affect each other, but their late target region is neither recurrent nor isolated.

The [frozen protocol](structure_formation_protocol_v1.json) has SHA-256 `147a40c82d584990a822f4904c85f543e23f29fdf9ceba0b01870811a4383917`. The executed producer has SHA-256 `3efbaf25f1a53725ef12073f90bbecd9a90c30a9e3bde9b341b3bcae9e601ea5`; its exact source is preserved with the [results](evidence/structure_formation_v1/result.json). The [independent audit](evidence/independent_audit/structure_formation_v1.json) reconstructs the native dynamics and readouts independently. No engine, tensor, click semantics or runtime control changed.

## Outcomes under the original definitions

Two complete isolated channel-0/14 clocks start at distances 2, 3 or 4 along X. The first has central counter pair `(1,1)`; the second has either `(1,1)` or `(-1,-1)`, with their complete phase-dependent remainders. Immutable composition verifies both initial 336-triple templates. The four masks preserve the entire remainder field while enabling neither clock, either clock, or both. All twelve comparisons pass initial and singleton eligibility.

The following outcomes hold separately on both cube sides, 225 and 257. The late window is states 64 through 96; the registered periods are 1 through 16. The target includes all 48 channels in the radius-one expansion of the full connecting segment, including a prospective bridge's transverse halo.

| Distance | Second sign | New counter bridge | Both original cores differ from singleton controls | Late exact period | Individual-term isolation | Formation |
| ---: | ---: | --- | --- | --- | --- | --- |
| 2 | +1 | Yes, update 1 | Yes | None in 1..16 | No | No |
| 2 | -1 | No | No | 4 | Yes | No |
| 3 | +1 | No | No | 4 | Yes | No |
| 3 | -1 | No | No | 4 | Yes | No |
| 4 | +1 | No | No | 4 | Yes | No |
| 4 | -1 | No | No | 4 | Yes | No |

For distance two with equal signs, the middle channel-0 triples begin

`(0,0,2), (0,1,0), (1,-1,2), (-1,-2,4), (-2,2,2), (2,1,0)`.

The first middle activation is the predicted native quotient threshold: two unit inputs produce `divmod(2*2+2,6)=(1,0)`. Either singleton leaves the middle counters zero. This is a demonstrated cooperative activation mechanism in a planned preparation. It does not settle into the registered localized recurrent object. The run reaches 15,330 sparse non-background triples. External incoming terms first enter the fixed 17-node target at update 26 and remain nonzero in every update of the late isolation window; the 32 late updates contain 24,280 individual external terms.

The ten negative-control geometries match the analytic period-four predictions. Opposite phases at distance two cancel the shared middle inputs, keeping its counters and remainder fixed. The shared halo then differs from either standalone clock's phase-dependent halo at some times, even though the endpoint counter cycles remain independent. Complete constituent identities are therefore reported as lost at those phases; core-only identity would be misleading. At distances three and four the complete isolated halos remain disjoint.

All recorded states avoid an active boundary hit. [Direct centered-state comparison](evidence/structure_formation_v1/size_equivalence.json) checks all 2,328 cross-size state pairs, including every remainder, rather than comparing only output scores. This finite-size agreement does not establish robustness under arbitrary preparations or longer runs.

## A limited algebraic obstruction

Suppose a transverse recipient of the newly activated middle is required to keep zero counters, and receives no other nonzero input. For the unchanged first-four-step core path, it sees middle counter values `0,1,-1,-2`. Its zero-quotient remainder would have to follow

`r, r, r+2, r, r-4`.

Keeping all these remainders in `[0,5]` requires both `r<=3` and `r>=4`, which is impossible. With the actual initial remainder two, that recipient develops a counter at update four. The companion channel maps to a distinct recipient and does not remove this constraint. This argument was independently checked algebraically.

The obstruction excludes a passive, zero-counter transverse halo for that fixed early bridge path. It does **not** exclude a larger recurrent body, active feedback that changes the path, a different complete initial preparation, or recurrence beyond the registered period/window. A proposed next candidate must state which of those assumptions changes before it is tested.

## Click observations and physical scope

Every native C0/C1/C2 event, quotient and six signed inputs is retained. In the equal-phase distance-two L225 run, the bridge has 260 C0 events, the endpoint cores 588, the remaining target halo 3,112, and the exterior 24,684. This failed formation case produces many C0 events. C0 presence alone therefore cannot serve as the successful-organization criterion in this tested family.

The opposite-phase distance-two preparation has ongoing period-four counter motion and **zero native C events**. Its zero quotients illustrate why counter motion, clock period and native click records are different observations. This does not make the board static or make native time a measured physical time.

There is no attraction, repulsion, matter, chemical bond or dissociation result here. The initial cores are stationary; creating an active intermediate counter is not inward motion. No new formation result may be inferred from the length of a run, a dense activity plot, a larger period, or a class of clicks.

## Reproduction and decision

The capture used 69.42 CPU seconds and 69.96 wall seconds within the 300 CPU-second, 600 wall-second and 64 MiB limits. Independent replay used 42.38 CPU seconds. Three contract regressions check exclusion of prejoined adjacent cores, sensitivity to complete shared-halo identity, and rejection of an empty recurrent region as a bridge.

From the repository root, choose a new output directory:

```sh
python -m research.clock_selection.structure_formation --output /tmp/universe24-formation-new
python -m unittest tests.test_clock_selection_formation
```

The [Presenter bundle](evidence/structure_formation_v1/experiments.json) contains six complete recordings: all four equal-phase distance-two controls, the opposite-phase distance-two joint run, and a distance-three joint control. The same generic Presenter displays their native states.

The demonstrated reusable behavior is conditional bridge activation and reciprocal influence. The missing behavior is a closed recurrent stationary product. Further work should register a larger complete object or an explicit initial halo preparation with active feedback, retain all external information, and test the same formation conjunction with matched controls. Simply rerunning this family longer would not by itself establish binding.
