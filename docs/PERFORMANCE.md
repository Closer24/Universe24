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
numpy mode for boards that fields fill is measured before adoption.

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
