# Directional local delay

`directional-local-wait-v1` extends the existing cost delay with six nonnegative
integer coefficients. Their order is **+X, -X, +Y, -Y, +Z, -Z**. These are six
port values, not a spatial three-vector or an established spacetime metric.
The extension changes scheduling, not any physical field-name interpretation.

## Configuration and exact default

Omitting `directional_delay` is equivalent to:

```json
"directional_delay": {
  "weights": [1, 1, 1, 1, 1, 1],
  "denominator": 1,
  "spatial_mode": "fixed"
}
```

An integer `weights: 1` broadcasts to all six directions. Six ones with no
field controls preserve the original carrier timing, events and snapshots.
The original independent spatial clock remains selected by `fixed`.
Equal coefficients `q` with `denominator: q` have the same effect. Other equal
ratios change the size of the extra wait uniformly. Weights are **multipliers,
not absolute tick counts**; zero removes extra waiting but never the link transit.

For example, `[1,3,1,1,1,1]` triples the extra wait for -X. Select
`spatial_mode: "cost"` to apply the same delay calculation to spatial outputs.
This is an explicit new field-clock policy, not a silent change to old worlds.

Optional `positive_field` and `negative_field` name unsigned spatial
three-vector fields. Their X/Y/Z components are added to the +X/+Y/+Z and
-X/-Y/-Z coefficients respectively, before division by `denominator`. The same
field may be used for both signs, giving reciprocal axis-dependent delays.
Missing fields, signed or scalar controls, malformed weights, booleans, floats,
negative coefficients and a nonpositive denominator are rejected.

Controls are ordinary configured state, never Python callbacks or inferred
properties of a field named `mass` or `computation`. Read only the node's retained
state and already completed arrivals. Reads in a field-forwarding phase use the
pre-forwarding sample; subsequent arrivals cannot rewrite a frozen schedule.
A field rule producing a control takes effect on later timing reads, not
retroactively on the transaction that produced it. Each distinct control read is
priced once per timing consumer using the configured `read` operation cost.
The six-value cached view is not extra inventory and contains no formula.

## Timing, commits and ownership

Let `C` be the already combined, priced cost, `B` the normal budget, and `tau`
the unchanged link time. Define the original extra wait and port waits:

```text
D = (max(1, ceil(C / B)) - 1) * tau
W[p] = ceil(D * effective_weight[p] / denominator)
release[p] = cycle_start + W[p]
arrival[p] = release[p] + tau
```

All operations use bounded integers. Upward rounding is a declared discrete
clock rule, not rounding of conserved inventory. Products, final waits and
absolute timestamps are validated before committing the affected transaction.
With unit coefficients the old `D` and total interval `D + tau` are exact.

A carrier batch freezes its proposal at cycle start. Its common atomic commit
occurs at the shortest **participating output** wait. A no-output transaction
uses the minimum of the six waits. A single outgoing record is therefore not
committed early merely because an unused direction is fast. Multiple outputs
commit together once; slower outputs remain in fixed **cell-owned dispatch
slots** until their individual release. A new carrier batch starts only after
this batch's last output completes its link (or the ordinary no-output interval).
This is not a claim of six indefinitely concurrent processors per node.

Before the common commit, originals own all stock. After it, replacements and
prepared outputs own it exactly once. Only actual dispatch emits `sent` or
`spatial_sent`; a future release is not an arrival or an in-flight signal.
Stored output capacity is still six times the configured carrier slot count
and six spatial bundles per node. There is no growing physical queue.
Sources in waiting dispatch slots continue emitting from their actual origin
until dispatch. They are included in a bounded local emission-owner view, never
read from a neighboring cell or an in-flight packet. Emission bookkeeping cannot
change their frozen route, payload values or release time.

In spatial `cost` mode, the local field transformation and source-bookkeeping
commit happen when the batch is prepared; **the outgoing bundles wait**, then
cross the unchanged links. Retained field updates are not deferred carrier-style
proposals. The next spatial batch is eligible after the last output arrival,
without requiring alignment to a global multiple of `tau`. Source emission is
once per eligible spatial batch, rather than once per fixed global field phase.
This distinction is explicit and is not a claim of a universal proper-time law.

Completed arrivals accumulate in retained field state and the six received
channels while that node waits. The next batch consumes those channels once.
Reception observers report only each newly completed receipt, not the whole
accumulated buffer. Decay and open-boundary escape occur only on completed links,
never during local waiting. A coupled reaction in this mode deposits into live
retained state; it cannot edit previously prepared or dispatched bundles.
Carrier cycles are charged only for newly executed spatial work, not a stale
field-cost report repeated throughout a wait.

## Owners and output consumers

`core/timing.py` owns the shared scalar and directional arithmetic.
`initialization.py` resolves strict configuration; `DirectionalDelayDefinition`
in `core/disturbance_state.py` is shared immutable data, outside dynamic cells.
The record/spatial engines own bounded timestamps, atomic commits and releases.
Wave mixing remains an ordinary field rule, not a scheduler feature.

Snapshots mark waiting bundles with `owner: "cell"` and `departure_tick`.
Accounting counts these and link-owned bundles once. The existing HTML player
keeps waiting output at its node and labels it as waiting; it interpolates only
a dispatched link. Run metadata preserves the selected policy, coefficients,
control names and port order. The workspace can edit this object and updates
its field references when a control is renamed. Diagnostics never feed a schedule.

## Regression and research boundary

[Timing tests](../tests/test_directional_delay.py) cover independent releases,
source persistence while waiting, signed stock, reaction/decay/escape accounting,
fixed transit, overflow, exact uniform compatibility and playback ownership.
[Control tests](../tests/test_directional_delay_controls.py) check causal local
reads, priced controls, frozen schedules, reciprocal axes and renamed labels.
[Experiment tests](../tests/test_curvature_delay_experiment.py) distinguish
actual mode mixing from a fixed-direction launcher and validate probe placement.

The [revised computation-field experiment](../examples/computational-curvature/README.md)
uses one existing local six-mode mixing law in all its mixing comparisons. Its
configured control rule derives three axis coefficients from completed source
receipts. That is an explicit candidate, not a gravitational law derived by the
engine. Equal weights alone do not create or forbid curvature. Transverse
spreading is not evidence of gravitational bending, and a fixed link time is
not a local light-speed measurement without an operational clock and ruler.

Existing wave-energy claims were tested under their stated synchronous laws.
Delays can change which amplitudes merge. Keep the separate squared-amplitude
readout and do not infer universal energy conservation from linear stock
accounting or one finite successful run. No new metric, geodesic, scattering
law, Lorentz invariance or general-relativistic acceptance is claimed here.
