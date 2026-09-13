# Disturbance routing and restricted coarse-graining

This research package addresses [task #82](https://github.com/Closer24/Universe24/issues/82)
using the existing `Simulation`. It supplies ordinary initialization data,
explicit property aggregation metadata, reproducible comparisons and a restricted
autonomous macro readout. Production source and defaults are unchanged.

## Run and inspect

From the repository root with the project Python environment and `src` on
`PYTHONPATH`:

```sh
python -m examples.coarse-graining.run_experiments --output artifacts/disturbance-study
```

Use a fresh output name. `artifacts/disturbance-study/report.json` records results,
source fingerprints, microscopic/macro comparisons, counterexamples and Python
allocation measurements. Its `inputs/` contains eight ordinary simulation JSON
files. Canonical run directories are siblings named
`artifacts/disturbance-study-<case>`; each has initialization, final state, events
and run metadata. They share one retention registry and the existing 24-hour
output policy. No renderer or GIF is requested.

Edit a saved input and use the existing validator and runner; no simulator
compilation is involved:

```sh
python -m event_universe.configuration_validation artifacts/disturbance-study/inputs/local-transfer.json
python -m event_universe --init artifacts/disturbance-study/inputs/local-transfer.json --output artifacts/changed-transfer
```

The macro comparison admits its exact restricted configuration only. An edited
input can be valid microscopically without being admitted for compression.

## Results and supported scope

| Requirement | Evidence |
| --- | --- |
| Momentum routing | Existing `direction_field` and `routing: balanced` give `(5,-2,0)` the period `+X,-Y,+X,+X,+X,-Y,+X`. Four periods give 20 X hops and eight negative Y hops with unchanged momentum. |
| Rest and timing | Zero momentum does not drift. Each hop uses one cardinal Link. Configured rate, carried credit and priced computation determine time; routing registers remain frozen until commit. |
| Local field coupling | A property-selected rule changes carrier `(E,P,internal)` from `(3,(1,0,0),0)` to `(4,(0,1,0),1)`. The local field changes by `(-1,(1,-1,0))`; the next route is +Y. |
| Generic eligibility | `requires` selects owned properties. Zero/opposite coupling, renamed labels and reordered field declarations retain expected behavior. |
| Parallel blocks | For 4, 16 and 64 Nodes, one same-direction owner per Node becomes 2, 4 and 8 exit bins. Every boundary arrival tick, outgoing E/P and still-owned E/P match the real engine, including link times one and two. |
| Timing information | Equal summed quantities with different delays remain distinguishable. Terminal-Link stock remains owned until actual escape; no early release. |
| Finite closure search | All 325 zero/one/two-owner configurations on 2x2x1 produce 650 measured transitions. Totals have 286 conflicting transitions; direction totals have 266; direction plus phase has zero. This is minimal only among these three candidate summaries in this finite free domain. |
| Interaction limitation | Equal initial E/P and free direction/phase summaries hide an encounter versus parallel lanes. The configured encounter exits along Y; the parallel case exits along X. |
| Derived mass readout | Two opposite individually massless candidates with energy three each have total E=6, P=0 and normalized system mass squared 36. No mass register, square root or elementary-particle mass derivation is added. |

Energy and momentum are explicitly owned additive candidate inventories. The
transfer is a supplied elementary integer law, not a Lorentz, Maxwell or QED
derivation. No dispersion relation or Euclidean isotropy is established. A lattice
route is a staircase. Guards and the passive event audit validate complete
transfers; they never choose a response or repair a residual.

Open-block runs reduce in-domain inventory as stock escapes. Consequently the
runner's `conserved_at_every_completed_tick` can be false;
`accounting_balanced_at_every_completed_tick` and the local E/P audit include
escape and pass. Raw in-domain equality is not the closed-plus-escaped balance.

## Aggregation metadata is not a closure proof

[properties.py](properties.py) requires one explicit `PropertySpec` per property.
`sum` and `vector_sum` add quantities; `keep_equal`, `phase_bins` and
`interaction_state` partition by exact values; `nonmergeable` keeps separate
contributors. Every bin also preserves law, channel, direction, remaining delay
and supplied state keys. Unknown modes, missing properties, duplicate identities,
mutable inputs, booleans and out-of-range values reject.

This research readout does not authorize replacing engine records. Two independent
amplitudes two and three can own energies four and nine, totaling 13. Squaring
their summed amplitude gives 25, a different state. Never reconstruct additive
energy from summed amplitude without an equivalent selected law. Tests preserve
this distinction.

Actual records also own routing counters/previous weights, rate credit and its
denominator, interaction residuals, emission phases and finite allowances. Node
slot order, pending proposals, receiving capacity and Link timing affect futures.
Identical momentum with different routing counters selects +X versus -Y; equal
rate one half with different credit waits versus moves. A supplied `state_key`
does not automatically discover these dependencies.

## Precisely admitted macro state

[closure.py](closure.py) admits an initialized isolated open block with only
constant-rate cardinal free carriers, the exact configured high budget, no later
inputs and no interactions. Capacity safety requires at most two owners globally
or one common travel direction. Three converging arrivals into two slots are
rejected before compression; the real engine counterexample retains stock and
reports exhaustion.

Initialization reads microscopic owners once and counts remaining Links to the
boundary. Evolving `FreeMacro` retains bounded exit bins with direction, channel,
delay and additive E/P. Each tick decrements delays; zero-delay bins leave. It
holds no microscopic records, member identities, world map or callbacks. Under
the admitted law nothing changes those exit times or quantities, establishing
this restricted countdown transition.

This predicts the initialized block's direction/time boundary observable. It
discards transverse exit coordinates, so it is **not a composable replacement
for a network of blocks**. Arbitrary arrivals, interactions, overload, oblique
routing, future field responses and a minimal interacting macro state remain
open. Additional total quantities alone do not close these gaps.

## Architecture, memory and integration proposal

Keep this package outside the physical engine. `configuration.py` owns common
input assembly; `routing.py` and `coupling.py` run actual engine laws;
`properties.py` validates readout bins; `closure.py` owns restricted comparisons;
`run_experiments.py` saves evidence. The existing source remains the sole engine.
The broader Node-owner and field-delay PR stacks are not prerequisites.

Generic metadata caps contributors at 2,048, properties at 16, component shapes
at one or three, identity length at four and state keys at 128 integers. Its
diagnostic member lists are bounded by block capacity. The restricted macro
admits at most 128 bins and 64 delay ticks, retains no member list and drops
released bins. Fixed-schema storage is bounded; world maps, histories,
enumeration and reports are separate host costs.

Measured Python allocations on Python 3.14.7:

| Microscopic owners | Macro bins | Retained traced bytes | Peak traced bytes |
| --- | --- | --- | --- |
| 4 | 2 | 424 | 14,832 |
| 16 | 4 | 756 | 35,552 |
| 64 | 8 | 1,364 | 115,392 |

Tracing starts after input construction and includes parsing/compression. These
finite Python measurements are not RSS or a whole-engine speedup. Production
Node layouts and memory ownership are unchanged. Existing architecture,
integer/locality and NodeState checks remain the production gates.

Propose integrating this research package and tests only. General physical
merging needs a separate sufficient-state and boundary-interface contract plus
interaction and capacity proofs. Boss, architecture, field, physics-review and
test Skills were reviewed; their existing generic-law, ownership and independent
validation requirements cover this work, so no duplicate Skill procedure is added.

Related research illustrates why exactness must name its observable:
[Lu and Vanden-Eijnden](https://arxiv.org/abs/1404.4729) preserve specified
statistical visitation and first-passage properties. That result does not establish
the deterministic pathwise or interacting closure required here.
