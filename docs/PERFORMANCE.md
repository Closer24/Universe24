# Run performance

## Ray-event engine: Local Focus measured (2026-09-17)

Measured on Linux with Python 3.14.0rc2 on 2026-09-17 at head `f64b3f7`,
source fingerprint
`ae363f86be9b57c2e8e3fc120368496c36eff9b5204be51bb74cd178f02dacd6`, one Node
worker, through `event_universe.runner.run_initialization`. Local Focus has
been the default since the 2026-09-15 change below; every input was run with
`"focus": false` and with `"focus": true` and nothing else changed. Three
inputs: the two-electron released-field world of the 2026-09-17 electron-field
recording (21 x 11 x 7, open boundary, two `hold` lamps emitting electron 8
toward each other on parallel lines, G released `[1, 4]`, `phase_steps` 8,
the `turn` interaction) for 24 and for 96 ticks, and the pair-lamp Detector
world of `tests/test_inverse_split.py` (15 x 15 x 15 periodic, arm A returned
at the mark three Links out, `return_mode` `siblings`) for 48 ticks. The
earlier measurement of the pre-prune engine is [PR #134](https://github.com/Closer24/Universe24/pull/134)
(2026-09-15, sparse carrier 57.95% shorter, straight-ray field 20.74%); it is
prior art for the method, not reused here.

| Input | Ticks | Wall, Focus off | Wall, Focus on | Spatial plan requests -> evaluations | Hit rate | Carrier plan hits | Records identical |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| Two electrons, released G | 24 | 0.487 s | 0.490 s | 754 -> 530 | 29.7% | 0 of 0 | yes |
| Two electrons, released G | 96 | 0.614 s | 0.601 s | 902 -> 678 | 24.8% | 0 of 0 | yes |
| Detector pair lamp, siblings | 48 | 0.200 s | 0.203 s | 150 -> 150 | 0.0% | 33 of 36 | yes |

Wall time is the median of five interleaved off/on runs of the whole runner
call, files included. Stepping alone through the `Simulation` API, the median
of fifteen interleaved runs, gives 0.404 s against 0.396 s, 0.457 s against
0.447 s and 0.178 s against 0.183 s. The 224 hits of the electron world all
fall in ticks 3 to 24, where the two mirror-image electrons and their parallel
G columns present equal planning inputs in the same tick; ticks 25 to 96 add
148 requests and no hit. The Detector world has one lamp and no symmetric
Node, so no spatial plan repeats; its 33 carrier hits are the lamp's unchanged
`hold` record, and `return_mode` `straight` and `annul` behave the same (no
spatial hit, identical records). Carrier phase visits are equal with and
without Focus (144, 576 and 144) because the only carrier Nodes in these
worlds are the lamps; ray Nodes belong to the spatial engine, whose active
index does not depend on Focus.

Records identical means equal SHA-256 digests of `events.jsonl` and
`state.json`, and of `run.json` after removing `elapsed_seconds`, `execution`
and `initialization_sha256` (the input file differs by the flag). Replayed on
`494acfd`, source fingerprint
`9515c6cddf9dbb8850f110161c032300bd8074e6b3869d2a91076dbed98c14e7`, every
`events.jsonl` and `state.json` digest matched `f64b3f7` exactly; those replay
timings are not used.

Counter caveat: with Focus off the engine hands the spatial planner to the
Nodes directly (`core/disturbance_engine.py`, constructor), so
`spatial_plan_reuse.requests` reads 0 in the off report. cProfile of the same
run shows 754 planner calls (`fields/spatial_plan.py`) off and 530 on, so the
requests column describes the same run either way.

Profile split (cProfile, two electrons, 24 ticks, Focus off, 1.90 s profiled):
the spatial planner takes 20% of the step time (754 calls),
`validate_spatial_plan` 22% and delivery through `spatial_node.receive` 23%.
Validation and delivery run on every request, hit or miss, so plan reuse can
touch only the planner's fifth; with Focus on the planner drops to 530 calls
and `plan_reuse.one` adds about 0.01 s of key hashing.

Cache size: after 24 ticks the spatial cache holds 530 entries of about
10.4 KB each as Python objects (3.5 KB key, 6.9 KB plan), 5.5 MB in all; at
the 4096-entry capacity about 43 MB per cache, two caches per simulation. The
spatial key carries the world tick (`core/spatial_node.py`), so a ray Node can
hit only against another Node of the same tick; ignoring the tick, 158 of the
530 entries repeat and the hit rate would be 382 of 754 (50.7%). The planner
in `fields/spatial_plan.py` reads the tick only in a bounds check; the
parameter serves `ray_delay` and per-tick phase.

Focus is already the default and stays so: the records are byte-identical,
the 2% saving on the symmetric world is inside the run-to-run noise of about
3%, the Detector world loses 3% to key construction without a hit, and no
change is made now.

Reproduction, without a committed script: copy the input JSON twice with
`"focus"` set each way; in one process call `run_initialization(path, output,
ticks=N)` five times per flag in alternating order into a fresh output
directory, timing each call with `time.perf_counter()` and taking the median;
read the counters from the `execution` object of `run.json`; hash the three
records as described. For stepping alone, build `parse_initial_state` from
the same documents and time `Simulation(initial).step()` over N ticks,
fifteen times per flag in alternating order. For the cache size, read
`_execution._field_reuse._entries` of a live `Simulation` before `close()`
and sum `sys.getsizeof` over dataclass fields and tuples. Wrap one runner
call in `cProfile` for the split.

## Plan: compiling the catalog into transition tables

The model owner's direction of 2026-09-17: because every quantity sits on a
ladder, the Node's law can be split into streaming and collision, like a
lattice gas. Streaming is one fixed permutation of the whole board, the
lattice wiring, the same for every Node; a body Node only excludes the body's
content from it (the flag). Collision is a lookup on a small key. The phase
enters a meeting only through the phase difference: the coherence table in
`core/spatial_state.py` is a cosine over differences computed once, and the
Born split is a catalog coupling indexed by the difference in sectors, so the
collision key of a two-ray meeting carries one phase dimension, the
difference, not one per ray. Rays of different layers never meet
(ray-layers-v1), so there is one table per layer, compiled from that layer's
families and couplings. Feasibility from the key the cache actually uses,
`SpatialPlanningInput(states, records, received, node_cost, rays, tick,
ray_hold)` with each `Ray` carrying heading, accumulators, amount, phase,
advance, wait, interaction delay, steps, outbound, event Ports, event shares
and Detector bit:

- Reduced key per ray, what the `turn` interaction reads: heading x amount x
  phase = 6 x 8 x 8 = 384 (eight phase steps, six Ports, amounts up to 8).
  Counting one phase per ray, two rays in one layer give 384^2 = 147,456
  entries, about 9.4 MB packed at 64 bytes per entry (1.5 GB at the measured
  10.4 KB per Python entry). On the difference key the same meeting is
  heading_a x amount_a x heading_b x amount_b x difference = 6 x 8 x 6 x 8 x 8
  = 18,432 rows per family pair and layer, about 1.2 MB packed (192 MB as
  Python entries).
- The full planner key is not precomputable: per ray it adds steps (up to the
  world diameter, unbounded on a periodic board), outbound, event shares
  (9^6 = 531,441 combinations, which fix the event Ports) and the Detector
  bit, about 4.7 x 10^7 per ray, so 147,456 x (4.7 x 10^7)^2, about 3 x 10^20
  entries, plus the unbounded tick and the records of lamp Nodes.
- Growth. With one phase per ray the count is 384^N in the ray count N, and
  6,144^N at 128 phase values (`phase_bits` 7; 6 x 8 x 128 per ray): two rays
  3.8 x 10^7 entries (2.4 GB packed), three rays at eight steps 5.7 x 10^7
  (3.6 GB packed), three rays at 128 values 2.3 x 10^11 (15 TB packed). On
  the difference key N rays carry N - 1 differences, 48^N x P^(N-1) rows for
  P phase values: two rays at 128 values 294,912 rows (19 MB packed), three
  rays at eight steps 7.1 x 10^6 (453 MB packed), three rays at 128 values
  1.8 x 10^9 (116 GB packed). A true 128-bit phase, feature 9's wide case,
  has 2^128 values and cannot be tabulated at all.

Where the apparatus sits in the compiled tables. The external body
(Highlights 3.19, external-body-v1 on `494acfd`; `body_release`,
`body_absorb` and `body_step` in `core/spatial_state.py`): its release is a
constant packet per body, amount x n/d on each heading with its declared
phase, computed once at load (seven variants: all six headings, or five when
it steps through a Port), so it never enters a key. Its couplings are
catalog entries, realised as a feature 6 meeting with the body as a
one-quantum token participant, so they are rows of the same collision table,
keyed by the arriving ray's reduced key (heading x amount x phase, the body's
declared phase being the constant the difference is taken against) and the
body's family; the sink default is the row that absorbs. Its momentum change
is a fixed linear map, the momentum table's sign x amount x heading summed
over arrivals, and its motion is the per-axis accumulator compared with the
amount: registers outside the key, like a ray's steps. Its amount is of any
width and is never a key dimension, which is why the "spreading not
enforced" flag costs nothing in the table. The Detector (detector-mark-v1):
the draw is outside any table, one unsalted draw per arrival; its two
outcomes, click on 1 and return on 0, are two rows.

Consequence: the tables are feasible only for the collision step on the
reduced key, with the ray-event bookkeeping (steps, event Ports, shares,
Detector bit) carried outside the key. That is a refactor of the planner's
key, scheduled as the step after feature 10 of issue #169, before any GPU
port. Two cheaper levers come first, each as its own PR with byte identity of
the run records as the acceptance test: drop the tick from the spatial key
where the planner ignores it (+21 points of hit rate on the electron world),
and skip `validate_spatial_plan` on a cache hit (22% of step time). A dense
numpy mode for boards that fields fill is measured before adoption, with
feature 12, field spreading (Highlights 3.5, 2026-09-17), under which the
field fills the board.

**Field spreading measured before adoption (2026-09-17, `field-spreading-v1`,
feature 12).** The electron world of `tests/test_released_field.py` (one lamp
at (2,5,3) emitting an electron of 5 along +X, `G` its field at `release:
[1, 4]`, G's 16 slots raised to 4096 so that no slot budget cuts the run) on
21 x 11 x 7 open, 48 ticks, single process on the recording host, with and
without `spread: [6, 1, 1, 1, 1, 1]` on G; `Simulation.step` wall time summed
over the 48 ticks, active Nodes and rays read from the engine after each
step. Without spread: 0.28 s; active Nodes 2, 7, 17, 27 at ticks 1 to 4, 43
at tick 8, 47 at 12, 51 at 16, 48 at 20, 18 at 24, 12 at 28, 1 from tick 40,
the peak 53; rays in the world 1, 6, 11, 16 at ticks 1 to 4, 22 at 8, 24 at
12, 26 at 16, 22 at 20, 8 at 24, 6 at 28, none from tick 40, the peak 27,
never more than one ray at a Node. With spread: 0.33 s; active Nodes 2, 7,
17, 27, then 33 at tick 8, 58 at 12, 56 at 16, 63 at 20, 29 at 24, 12 at 28,
1 from tick 40, the peak 67; rays 1, 6, 11, 16, then 22 at 8, 34 at 12, 37 at
16, 34 at 20, 17 at 24, 5 at 28, none from tick 40, the peak 39, at most 6
rays at a Node. The G total per tick and the 90 quanta escaped by tick 40
are the same in both runs: the release booking is unchanged, and every
released ray of this world is one quantum, which the table cannot split, so
the remainder rule sends each whole through the entry its phase selects
(phases 0 to 4 forward, 5 backward, 6 and 7 transverse) and the field
wanders on whole quanta instead of filling the board. On this world the
spread costs 18% of step time and 26% more active Nodes at the peak; a world
whose releases carry many quanta per ray (a body of amount 4096 at
`release: [1, 2048]` releases 2 per heading, still below the table's total
11) is where the split itself acts, and it is not measured here.

## The dense mode measured before adoption (2026-09-17)

The dense numpy mode the plan above schedules for boards that a field fills,
measured before adoption (`dense-field-v1`; [the dense
mode](SPATIAL_FIELDS.md#the-dense-mode-dense-field-v1)). The pure-field
Nodes of a board, those holding nothing but outbound content of spreading
families and their remainder registers, are cycled as one vectorized step
over integer arrays (`event_universe/dense_field.py`, numpy int64, outside
the core, behind the `DenseRegion` protocol of `core/spatial_engine.py`)
that applies the spread and remainder rule of `field-spreading-v1` and
`field-remainder-v1` to every such Node at once with the same integers: the
split per arriving heading into whole quanta and shares, the registers per
source sign and Port with their phases combined by the coherence rule in the
engine's order (Port by Port; tabulated over held, held phase, share and
share phase when the table fits, computed as the engine's `_phase_of_sum`
otherwise), the releases at one quantum, the departures walking one Link
with the family's rate, the open boundary's escapes per family and sign, the
Detector bit of the whole on every departure, and the plan cost the spatial
law would meter (received packets, resident rays, departures, sending
Ports, the registers). A Node holding anything else (a Detector mark, an
external body, a record, a ray of another family, a returning ray, an
event-carrying ray) is the engine's, and ownership is decided at every
delivery for the Nodes that receive something: a ray leaving a dense Node
toward an engine Node is handed over as an ordinary packet of merged rays,
a packet leaving an engine Node into the region is absorbed into the arrays,
and the registers move with the Node. The region's Nodes read back as Node
state for the totals, the snapshot and the inventory view; a dense Node
publishes no per-Node event, the record of a dense region being its totals
per tick, so the mode is not for records that need per-Node field events.
The acceptance test is byte identity of `state.json` and of the world ledger.

Measured on Linux with Python 3.14.0rc2 and numpy 2.5.3 on 2026-09-17, one
Node worker, Focus on (the default), single process, the engine alone on the
change with `dense_field` off (source fingerprint
`0fab8a444af6a15dbb6e7a2ca630a984c046f952ecc30b1c84bcc681a38ba02e`) and with
it on; the engine alone on `9d477f4` before the change (source fingerprint
`aec35d9ec38c9c3778a3e2ef3966d996d0ffcadfb547c4626defa526b754d705`) gives
the same `state.json` and ledger digests on every world below that was
replayed on it (the field-spreading worlds, the screen loop, pp_r16), so the
engine's path is unchanged by the hooks. The worlds: the boards of
`tests/test_field_spreading.py` (13^3 open, the lamps emitting `light` with
the table [6, 1, 1, 1, 1, 1], written without their `conservation` key,
which the mode rejects: `single` for 4 and 24 ticks, `superposition`,
`cancelled`, `stream`, `sign`, `returned`, `source` for 12 and 40 ticks,
`resident`), `examples/nature/screen_loop.json` for 48 ticks (E9: the ring's
four corners are records, the seven marks Detectors that return every
quantum), and `examples/nature/a5_static/pp_r8.json` for its 48 ticks and
`pp_r16.json` for 32 (two bodies at rest radiating 4096 quanta per heading
per interval, the field filling the board: every Node of the 19 x 11 x 11
and 27 x 11 x 11 boards cycles from tick 11 on).

| Input | Ticks | Node cycles | Step wall, engine | Step wall, dense | ms per Node cycle, engine | Dense | Records identical |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| Field spreading, single | 4 | 26 | 0.006 s | 0.037 s | 0.217 | 1.434 | yes |
| Field spreading, stream | 12 | 47 | 0.014 s | 0.084 s | 0.304 | 1.786 | yes |
| Field spreading, source | 12 | 205 | 0.071 s | 0.177 s | 0.347 | 0.865 | yes |
| Field spreading, resident | 4 | 52 | 0.021 s | 0.057 s | 0.408 | 1.088 | yes |
| Field spreading, source | 40 | 1847 | 0.414 s | 0.664 s | 0.224 | 0.360 | yes |
| Screen loop | 48 | 10900 | 4.391 s | 0.916 s | 0.403 | 0.084 | yes |
| A5s pp_r8 | 48 | 94355 | 219.7 s | 1.833 s | 2.328 | 0.0194 | yes |
| A5s pp_r16 | 32 | 77683 | 152.6 s | 1.631 s | 1.964 | 0.0210 | yes |

Node cycles is the sum over the ticks of the engine's active Nodes after
each step, the same count in both modes (a Node with content cycles once per
interval whoever cycles it); ms per Node cycle is the step wall over that
count. Step wall is `Simulation.step` summed over the ticks, the median of
three runs in one process per mode (one run for the engine on the two A5s
worlds, 220 and 153 seconds each), the three within 4% of each other. The
other field-spreading worlds are identical as well, at 0.003 s against
0.013 s (`superposition`, `cancelled`), 0.009 against 0.024 (`sign`), 0.004
against 0.029 (`returned`, where no Node is ever the region's: every Node
with content holds the lamp, the mark or the returned quantum) and 0.019
against 0.123 (`single`, 24 ticks). At the full board the engine spends 5.50
s per tick on pp_r8 (2299 Nodes, two spreading families) and 6.19 s on
pp_r16 (3267 Nodes) against 38.0 and 51.6 ms for the region, 145 and 120
times shorter per tick; the whole runner call, files included, takes 245.8
and 170.8 s against 3.06 and 3.10 s. On the small boards the mode is slower,
by two to seven times: its step costs a fixed 3 to 6 ms per tick over the
whole 13^3 board whether the field fills it or not (the arrays are the
board's, not the active Nodes'), against the engine's fraction of a
millisecond for a handful of active Nodes, which is why the mode is a
switch and not the default.

Records identical means equal SHA-256 digests of `state.json` (every Node's
rays, registers and phases, delivered amounts, arrival mask and cost) and of
the `audit` list of `run.json` (the world ledger of every completed tick),
equal `final_totals`, `source_totals`, `escaped_totals`,
`external_body_totals` and `external_bodies` (every body's momentum,
accumulators and sinks), and the same Detector and body events in the same
order: the 16 clicks and 4 passes of the screen loop, the 1022
`external_body_absorbed` records of pp_r8 and the 396 of pp_r16 (tick, body,
Port, family, amount, momentum), the 12 returns and 10 `field_returned` of
the 40-tick source world. `events.jsonl` differs by construction: with the
mode on, pp_r8 records 96 `spatial_cycle`, 94 `spatial_received` and 576
`spatial_sent` events (the two bodies' Nodes) against 92058, 94353 and
547940, and no `field_spread` or `spatial_escaped` of a dense Node (161738
and 40066 in the engine's record); the region's cycles are in the ledger's
current, sourced and escaped lines and nowhere else. `run.json` also differs
in `elapsed_seconds`, `execution` (the plan-reuse and bank counters) and
`source_sha256`. The isolated test (`tests/test_dense_field.py`) pins one
cycle against `spread_content`, the hand-over both ways on the source world
and the identity on the field-spreading worlds through the runner.

Projection for A5s's steady state. The step's cost is the board's, not
the active Nodes': 38.0 ms per tick over 2299 Nodes on pp_r8 and 51.6 over
3267 on pp_r16 (16.5 and 15.8 microseconds per Node and tick, two spreading
families), and, timed once on the same two bodies at r = 16 on larger boards
(the region alone cycling, the engine's two body Nodes beside it, 8 and 16
ticks, no runner), 2.23 s per tick over 59 x 43 x 43 = 109,091 Nodes (20.4
microseconds per Node and tick) and 8.86 s over 81 x 65 x 65 = 342,225
Nodes, the r = 16 board with the boundary 2r away of the mean-field entry
(25.9 microseconds; the larger boards' arrays no longer fit the caches, and
the second timing ran beside an engine run on another core). At the
measured 26 microseconds per Node and tick, the mean-field entry's steady
state ([EXPERIMENTS](EXPERIMENTS.md#a5s-coulombs-force-law-between-two-charges-at-rest):
342 k Nodes x 354 ticks at r = 16, 1.14 M x 866 at r = 24, at the engine's
2.3 ms per Node cycle 78 hours and 26 days) costs about 3,150 s, 52
minutes, at r = 16 and about 25,700 s, 7.1 hours, at r = 24, ninety times
shorter, the r = 24 figure a projection from the r = 16 board (the 1.14 M
board was not run; the prototype's int64 arrays hold about 4 KB per Node
and spreading family, 4.6 GB there before the step's temporaries, which
narrower storage would quarter). The step itself is one Python loop over
six Ports of whole-board numpy operations per family; a compaction to the
active Nodes, narrower storage or a compiled kernel would each shorten it
further and none is needed for the acceptance test.

Adoption: behind the world key `dense_field: true` or the runner's
`--dense-field`, default off, the run record carrying `dense_field:
"dense-field-v1"` when on; a world without the key runs and records byte
for byte as before. The prototype admits a world with a spreading family
whose spatial fields are all ray fields, without the local conservation
audit (`conservation`, which reads per-Node events), without polarization
(`ray-polarization-v1`; the region carries unpolarized content), without a
ray interaction two of whose participants can be spreading families (a
coupling on field rays inside the region), and one Node worker; the parser
names the reason. Every other Node kind (a mark, a body, a lamp, a ray of
another family, a returning quantum) is the engine's and crosses the region
by packets, so the screen loop and the electron worlds run under the mode
with the engine's Nodes where the physics needs them.

Reproduction, without a committed script: write the worlds (the
field-spreading builders with their `conservation` key removed; the two
A5s files as they are; `screen_loop.json` as it is), each once as it is and
once with `"dense_field": true`; in one process per mode call
`run_initialization(path, output, ticks=N)` and hash `state.json` and the
`audit` list of `run.json` as described, reading the events for the clicks
and the absorptions; then build `prepare_initialization(document).initial`
and time `Simulation(initial).step()` over N ticks three times per mode,
reading `len(world._spatial._active)` after each step, and once on the two
larger A5s boards.

## Ray-event engine: the tick leaves the spatial plan key (2026-09-17)

The first of the two levers scheduled above. Measured on Linux with Python
3.14.0rc2 on 2026-09-17, one Node worker, Focus on (the default), before on
`2af76d7` (source fingerprint
`57d6c941dede850cb952948ad739e1e4216bc0e788ae38c37fdc52a710a23de2`) and
after on the change (source fingerprint
`27061f2926566afa58fae56cb30f826a56fd06b11d2b19430fc967a5ba7586f3`). The
spatial law (`fields/spatial_plan.py`) read the tick only in a bounds check
and the Node checks its clock before it plans, so the tick left
`SpatialPlanningInput` and the law's signature: a Node whose local input
repeats hits the entry of an earlier tick, and a Node whose plan changes with
time carries that time in its records (a lamp's stock or allowance, its
emission cursor and wave phase). Five worlds: the one-lamp electron world of
the field-spreading measurement above (one lamp at (2,5,3) emitting an
electron of 5 along +X, `G` released `[1, 4]` with 4096 slots, 21 x 11 x 7
open, 48 ticks, no spread); a two-electron world after the Local Focus
recording (two `hold` lamps at (2,4,3) and (18,6,3) emitting electron 8 toward
each other on parallel lines, `G` released `[1, 4]`, `phase_steps` 8, the
`turn` interaction, 21 x 11 x 7 open, the builder of
`tests/test_released_field.py` with its default slots) for 24 and 96 ticks;
`examples/nature/screen_loop.json` for 48 ticks; `examples/nature/ring.json`
for its 16 ticks.

| Input | Ticks | Requests -> evaluations, before | After | Hit rate, before | After | Step wall, before | After | Records identical |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| One electron, released G | 48 | 543 -> 543 | 543 -> 290 | 0.0% | 46.6% | 0.289 s | 0.256 s | yes |
| Two electrons, released G | 24 | 723 -> 527 | 723 -> 383 | 27.1% | 47.0% | 0.394 s | 0.369 s | yes |
| Two electrons, released G | 96 | 869 -> 673 | 869 -> 385 | 22.6% | 55.7% | 0.446 s | 0.396 s | yes |
| Screen loop | 48 | 10477 -> 6858 | 10477 -> 4942 | 34.5% | 52.8% | 4.956 s | 4.758 s | yes |
| Ring | 16 | 64 -> 64 | 64 -> 24 | 0.0% | 62.5% | 0.061 s | 0.041 s | yes |

Requests, evaluations and hits are `spatial_plan_reuse` of the `execution`
object of `run.json`. Step wall is `Simulation.step` summed over the ticks,
the median of seven runs in one process per source; the seven runs of one
world and source lie within 4% of each other, and the two sources ran in
separate processes, not interleaved. The two-electron world gains 19.9
points at 24 ticks (the plan above projected 21 on the recording's world,
whose lamp positions are not committed) and 33.1 at 96, where the tail of
the run repeats the inputs of earlier ticks; the one-lamp world and the ring,
which had no symmetric Node and no hit, now reuse every steady Node's plan.
Step time falls by 4% to 11% on the electron worlds and the screen loop, and
by a third on the ring; validation and delivery still run on every request
(the second lever).

Records identical means equal SHA-256 digests of `events.jsonl`, of
`state.json` and of `run.json` after removing `elapsed_seconds`, `execution`
(the reuse counters are the lever) and `source_sha256` (the code differs);
`initialization_sha256` is kept, the inputs being the same files. All five
worlds are identical, and the isolated test of the key
(`tests/test_plan_reuse.py`) pins a Node in a steady field hitting from its
second arrival while a lamp whose stock counts down never hits.

Reproduction, without a committed script: write the five inputs (the two
electron worlds from the builder of `tests/test_released_field.py` with
`shape` `[21, 11, 7]`, `boundary` `open` and, for the one-lamp world, `G`'s
`ray_slots` 4096); in one process per source call
`run_initialization(path, output, ticks=N)` once per world and hash the three
records as described, reading the counters from `run.json`; then build
`prepare_initialization(document).initial` and time
`Simulation(initial).step()` over N ticks seven times per world, taking the
median.

## Ray-event engine: no validation on a plan-reuse hit (2026-09-17)

The second of the two levers scheduled above, measured like the first: the
same host, worlds, records and timing method, before on the first lever
(source fingerprint
`27061f2926566afa58fae56cb30f826a56fd06b11d2b19430fc967a5ba7586f3`) and
after on the change (source fingerprint
`ebb8abf38b06c07b50c275f922436f78309b32db06b4474b08a7a172d0b44da3`). The
Node boundary's `validate_spatial_plan` now runs once per evaluated plan, at
the execution (`NodeExecution`'s `spatial_validator`), before the plan is
returned or retained, so a hit is served a plan validated at its miss and the
Node checks only what it changes after planning: an external body's part,
whose registers are outside the key, is validated on every cycle, and the
completion of a pending cycle (`node_execution`) still validates the plan it
merges with the live states. The serial engine without reuse hands the Nodes
the law itself and they validate each plan as before; parallel execution
validates its batches, which serve every request.

| Input | Ticks | Requests -> evaluations | Hit rate | Step wall, before | After | Change | Records identical |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| One electron, released G | 48 | 543 -> 290 | 46.6% | 0.256 s | 0.234 s | 8.9% shorter | yes |
| Two electrons, released G | 24 | 723 -> 383 | 47.0% | 0.369 s | 0.331 s | 10.3% shorter | yes |
| Two electrons, released G | 96 | 869 -> 385 | 55.7% | 0.396 s | 0.346 s | 12.5% shorter | yes |
| Screen loop | 48 | 10477 -> 4942 | 52.8% | 4.758 s | 4.205 s | 11.6% shorter | yes |
| Ring | 16 | 64 -> 24 | 62.5% | 0.041 s | 0.039 s | 7.0% shorter | yes |

Requests, evaluations and hits are unchanged by construction (the key is the
first lever's). Step wall is the median of seven runs in one process per
source, the seven within 4% of each other except one run of the one-electron
world at +17%, outside the median. The saving is the validation of the hits,
22% of step time times the hit rate on the profile of the Local Focus
recording, less the hits' share of the cheaper plans. Against `2af76d7`,
before either lever, the two together shorten the step by 19.2%, 16.1%,
22.4%, 15.2% and 36.9% on the five worlds in the table's order, at the same
records.

Records identical means the same three digests as the first lever's, equal
on all five worlds, and the isolated test (`tests/test_plan_reuse.py`) counts
the validations: one per evaluation at the execution and none at the Node
with Focus on, one per request at the Node with Focus off, and the body's
Node validating after each of its cycles.

## Active engine: default Focus and exact plan reuse

Measured on Linux with Python 3.14.7 on 2026-09-15. Baseline:
`4796cb256cbdbd830aa29cc3038fea98087de58b`, with its original default Focus off.
The proposed default enables certified empty-carrier scheduling and pure plan
reuse; both transport engines additionally index occupied output banks.

| Input | Ticks | Baseline median | Optimized median | Elapsed time change |
| --- | ---: | ---: | ---: | ---: |
| One moving carrier leaving an empty trail | 240 | 0.2041 s | 0.0849 s | 58.4% shorter |
| 32 repeated moving carriers, periodic domain | 120 | 1.1858 s | 0.8199 s | 30.9% shorter |
| 16 repeated local two-field configurations | 48 | 6.7063 s | 4.5271 s | 32.5% shorter |
| Existing finite-field example | 16 | 0.1898 s | 0.1960 s | 3.3% longer |

Each value is the median of three fresh processes. Variant order alternates.
Timers include `step()` and the same ordered event serialization, while excluding
initialization, imports, per-tick comparison reads and HTML export. CPU time is
recorded separately. These are small input-specific benchmarks, not universal
speed guarantees. The low-repetition finite-field input showed no benefit;
cache lookup and index maintenance can outweigh savings in such a short world.

For repeated carriers, 3840 local planning requests required only two actual law
evaluations. The 16 repeated field configurations required 47 spatial evaluations
for 752 requests and one carrier evaluation for 736 requests. Every Node still
performed its own guarded commits, event publication and modeled cost accounting;
reducing planner work by more than 90% does not reduce whole-run time by 90%.

Across all 24 measured runs, the cumulative hashes of every completed tick's
snapshot, actual inventory and computation report matched within each input.
Full ordered event trace hashes and final accounting also matched. Every run
produced HTML using the existing `render_disturbances` generator. Browser visual
inspection was unavailable because the browser policy blocked local-file access;
HTML generation and embedded recording integrity were checked separately.

Baseline source fingerprint:
`c70c279be058f8730358a9110a9a51a1c201e91f5f0d884641cbfc3ef263fb14`.
Optimized source fingerprint:
`7c5375d1731082a27cb9f50fd2fe5e87c0bad761d8a67b6c679b469d2f83b346`.
The fingerprint covers active Python source, not generated outputs or this text.

A subsequent constructor correction preserves the original spatial planner object
for direct law inspection while passing the same reuse adapter to execution.
Its source fingerprint is
`4e0c9eeffd4a1ce1bb832c0687913c71a8c44dd4d79d100296c42e9238f50c36`.
All four inputs were replayed on this corrected source and matched the recorded
state, event, cost and accounting evidence exactly. The table remains the earlier
isolated timing measurement: constructor setup is outside its timer, the stepping
callback is unchanged, and timings from the extra acceptance replays are not used.

Reproduce with the same environment and `tools/benchmark_focus.py`, setting
`PYTHONPATH` to each chosen checkout's `src`. Select `--case trail`, `repeated`,
`fields` or `finite`, provide that checkout with `--source`, and use a fresh
`--output` directory. `--focus true` or `--focus false` provides an explicit
control. Run each comparison at least three times. Inputs, events, result JSON
and canonical HTML are written together; generated outputs stay outside commits.
See [Local Focus](LOCAL_FOCUS.md) for eligibility, bounds and supercell limits.

## Active engine: one validation per crossing and undecoded checks

Measured on Linux with Python 3.14.0rc2 on 2026-09-16 with the same
`tools/benchmark_focus.py` inputs. Baseline: `e5b5911` (merged Focus default).
Profiling that baseline showed `node_boundary.validate_record` at about half
of the repeated-carrier step time, with each delivered record validated by the
transport loop, by `DisturbanceNode.receive` and again by `validate_records`
over the received records. In the two-field input, `decode` and `unpack`
took more than half of the step time, reached from conservation readouts,
field guard validation and spatial-state validation.

Three host-only changes follow, each with identical physical outputs:

- A delivered record is validated once, by the receiving Node. `receive`
  passes its validated arrivals to `validate_records` as verified objects, so
  only new records such as merges are checked again; transport validates only
  records escaping through an open boundary. Malformed records raise the same
  errors at the same boundary.
- `FieldDefinition.validate` and `SpatialState.validate` inspect codes without
  decoding: a valid code is an integer in `1..2*MAX_VALUE+1` and an even code
  is exactly a negative value. Messages and their order are unchanged.
- `LocalBalanceGuard` keeps two bounded caches (4096 entries each, least
  recently used eviction) of successful readouts keyed by quantity index and
  the immutable record values or spatial bundle. Failures are never retained;
  the discarded validation meter charges nothing observable. The caches are
  bounded at 2 x 4096 entries, belong to one guard instance (a derived guard
  starts empty), assume the boundary validation that precedes every readout,
  and are deliberately absent from `execution_report()` so that execution
  reports stay identical to the baseline.

| Input | Ticks | Baseline median | Optimized median | Elapsed time change |
| --- | ---: | ---: | ---: | ---: |
| One moving carrier leaving an empty trail | 240 | 0.0478 s | 0.0362 s | 24.1% shorter |
| 32 repeated moving carriers, periodic domain | 120 | 0.4590 s | 0.3755 s | 18.2% shorter |
| 16 repeated local two-field configurations | 48 | 2.3308 s | 0.9181 s | 60.6% shorter |
| Existing finite-field example | 16 | 0.1028 s | 0.0977 s | 4.9% shorter |

Each value is the median of three fresh processes per stage; the same
timer as the earlier table is used. Intermediate stages measured 18.3%
(repeated) after the first change and 25.7% (two-field) after the second; the
readout cache contributes most of the two-field gain, while the small
carrier-only inputs vary by a few milliseconds between stages. These are
small input-specific measurements on a shared host, not speed guarantees.

Across all 48 measured runs (baseline plus three stages, four inputs, three
runs each), `state_sha256`, `events_sha256`, the computation report, final
totals, spatial accounting and the execution report matched the baseline
exactly within each input. Modeled operation cost and world time are
unchanged; only host work was removed. HTML export ran through the existing
generator without visual inspection.

Baseline source fingerprint:
`4e0c9eeffd4a1ce1bb832c0687913c71a8c44dd4d79d100296c42e9238f50c36`.
After the first change:
`1ebe5f5f00f8a87003e97d9d1bc8a3eb12f5a334b4ec24305d28f4a71b3e9bb5`;
after the second:
`fa966dd12f3527be137217fe5de0a55c9a9f0730bbd5706f83a1762653d005b2`;
optimized source fingerprint:
`39a611ddd1df3f549566a233417c3cb2c28cb953fc52cd388b96f5cbde04a516`.
The fingerprint covers active Python source, not generated outputs or this text.

`validate_field_guards` in `fields/local_field_rules.py` still decodes its
stock and outgoing payloads on every commit; reusing its result would need a
cache keyed by the complete spatial state and plan, threaded through the
spatial Node services, and was left for a separate change.

## Historical renderer measurements

These are dated measurements of the historical scalar/particle renderer, which
was deleted together with its runner and scenarios on 2026-09-17 (issue #164,
bucket A). They cannot be reproduced on the current tree and do not measure the
active initialization-defined disturbance engine. Current runs are headless
unless visualization is explicitly requested.

## Measured contact run

Measured on the same Windows host on 2026-09-11, using Python 3.14.7,
Matplotlib 3.11.1, Pillow 12.3.0 and NumPy 2.5.3 in one existing environment.
The baseline was commit `1168463ae7d211f86274200dd75c5e03c556c8f3`.
Each measurement used the historical contact scenario: 48 physical ticks, 49 saved
frames, stride 1, and enhanced 1500x1275 3D GIF and standalone HTML.

| Measured phase | Before | After |
| --- | ---: | ---: |
| Simulation, capture and metadata before rendering | 0.724 s | 0.697 s |
| Rendering and GIF/HTML export | 44.106 s | 20.349 s |
| Total run after imports | 44.831 s | 21.046 s |

This run completed **2.13 times faster**, with a **53.1% shorter elapsed time**.
These are single before/after wall-clock measurements, not a cross-platform
guarantee or a statistical benchmark. Setup, dependency installation and imports
are excluded. Larger fields or longer runs can have different bottlenecks.

The baseline source fingerprint is
`c7696ccccad62080363a35673f9e6be053c3f5461909160de8792abc8b621256`;
the optimized source fingerprint is
`49c8e8fe8401f038d463ab20ab331392ae8a41c723bd25309a9af571eb2be506`.
Fingerprints identify the active Python source, independently of documentation.

## Validation environment

The Windows validation environment enables UTF-8 mode (`$env:PYTHONUTF8 = '1'`
in PowerShell) before the unchanged gate. Some existing tests read UTF-8 source
and HTML through the platform default encoding; a legacy Windows code page
cannot decode those files. This setting does not change simulation arithmetic.

Generated GIFs, HTML, event traces and timing records belong in run outputs,
outside source commits. Their comparison and the executed gate results are
recorded in the implementation PR.
