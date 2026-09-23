# The engine's run audit: how one interval schedules its work, what it costs at head, and what a split of every row would cost (2026-09-23)

The model owner's order of 2026-09-23, 05:40Z, through the Boss: check
that the system runs orderly with the new laws, that the active Nodes are a
queue and not a sweep, so that there are no long runs when many
experiments are re-run. The Register Architect is the one writer. Every
physics run is held (record 1276); the measurements below are HOST
measurements of the engine's run and nothing else: no reading is taken,
compared or registered, the physics is not read. Every claim of section 1
carries a code line of main at 412b81f1; every number of section 2 is
labelled HOST; section 3 is a COMPUTATION from the event-split design's
own formulas; section 4 recommends and builds nothing. A scheduling change
never changes the law's order of operations within an interval: the chief
physicist owns that order, and what would touch it is named as a question
for him, not as a recommendation.

## 1. The scheduling as built (main 412b81f1)

**In one sentence.** One interval visits the live rows (a queue: the
stores' arrays, sorted by Node, gathered and re-sorted per phase at
O(R log R)) and the measured events (a Python loop over E); it sweeps the
whole GameBoard once per interval, not per event, in one dense per-Node
array (`node_event`, `occupied`), and it pays Python loops per row in
three places (the age wall on every live row in the walk, the clicks'
record lines, the layer's calls per ending row).

**The interval.** `engine.py:577-633`, `NatureBeamSimulation.step`: the
tick (590), the clocks' frame `_frame_all` (591), the measured events'
steps `_move` in a Python loop over `sorted(self.measured)` (592-594), one
call of `nature_beam` over all stores (595-604), the clocks' turn in a
second loop over E (605-633; an `energy` record line per event under the
covariant key only, 616-633). `nature_beam` (`nature_beam.py:3403-3461`)
runs the phases in the law's order: `interval_frame` (3423), `_walk`
(3427), `GameBoardDiagnostics` (3432, references only), `_collide` per
family (3435-3436), `meet` under the key `meeting` or `optical_turn`
(3441-3448), `_measure` (3451), `_release` (3454), `_border` (3457),
`_merge` (3458), `gather_records` with a layer (3459-3460).

**What is visited.** The state is one `NatureBeamStore` per family
(`nature_beam.py:1984-2277`): a structure of numpy arrays, 26 int64
columns per row (`FIELDS`, 1567-1600; 208 bytes per row), kept sorted by
Node after each interval (1991); the Node is the flat index of the address
(1996). There is no per-Node array of the law's state: nothing is kept at
a Node beyond the rows there (LOCALITY-1 as written). The measured events
are a dict of Python objects (`Measured`, `measured.py:501-928`), their
counts a `CountTable` of Python rows, their pending rows Python lists;
the detector sets keep one dict entry per Node of the set
(`DetectorSet.nodes`, `measured.py:187`), sized by the set and not by the
GameBoard.

| Phase | Structure visited | Cost class (R live rows, E events, N_nodes the GameBoard's Nodes, K occupied Nodes, M rows at events) | numpy or Python | Lines (nature_beam.py unless named) |
| --- | --- | --- | --- | --- |
| the frame: `node_event`, `occupied` | one dense array of N_nodes, filled at the events' Nodes, and its boolean | O(N_nodes) per interval, once (not per event) | `np.full(nodes, -1)`, `>= 0`; Python loops over the bodies' Nodes only | 3303, 3318, 3324, 3321-3323, 3342-3362 |
| the frame: the crowd, first build | all live rows to the K occupied Nodes and the (Node, number) pairs | O(R log R) | `np.unique` twice, `np.add.at`, `bincount` | `CrowdMoments` 3184-3229, built at 3399 |
| the walk: the flight | the live rows per family | O(R) numpy plus O(R) Python | `by_drive_rows` (602-634); the Python loop `for k in range(rate.shape[0])` calling `age_wall` per row | 3841-3924; the loop 3833-3837 |
| the walk: the crowd's query | the sparse crowd keys | O(R log K) | `searchsorted` | 3231-3247, 3877 |
| the walk: the escapes | the escaped rows | O(escaped) Python: `exact_phase`, `layer.end`, one `click` line per row | dict and list comprehensions, a loop | 4298-4355 |
| the walk: the sort | the live rows, 26 columns | O(R log R) plus a gather of 26 columns | `argsort(kind="stable")`, `store.take` | 4396-4399, 2075-2082 |
| the readings (`GameBoardDiagnostics`) | dense arrays of N_nodes per family, only when a property is read (the engine's diagnostics, `diagnostics/shell_readings.py`); the law never reads it | O(N_nodes + R log R) when read; O(1) on the interval | `np.zeros(nodes)`, `np.unique`, `np.add.at` | 2321-2400 (2349-2370, 2388-2400), 538-579 |
| the collision | the eligible live rows; `occupied` gathered at the rows' indices | O(R log R) | `lexsort((content, number, node))`, `cumsum`, `np.add.at`, the table `forward[code]` (3^8 entries, built once) | 3464-3507; the table 1247-1325 |
| the turn (`optical_turn`) | the rows in free space; the crowd built a second time from the arrivals | O(R log R) numpy plus Python O(pushed rows x fan) | `np.unique`, `searchsorted`, `np.isin`; the Python loops `momentum_pair` (3729-3766) and the Bresenham choice `for k in held.tolist()` | 3953-4186; the crowd 4025; the loops 4076-4102, 4123-4148 |
| the measure: the plan | `node_event[store.node]`, one gather; the M rows at events sorted by event | O(R) plus O(M log M) plus Python O(M); the beam pairing O(k^2) per set | `argsort`, `lexsort`, `isin`, `searchsorted`, `reduceat`, `np.add.at`; Python loops over the taken rows | `_family_plan` 4543-5146 (4598, 4623, 4887-4913, 5021-5108) |
| the measure: the apply | the plans per event, family, group and row | O(E x families + M), all Python; one `click` line per clicking row, `layer.end` per row | Python | `_apply_plans` 5627-5674, `_apply_plan` 5160-5624 (5533-5572, 5516-5531) |
| the measure: the keep | the live rows, 26 columns | O(R) | `flatnonzero`, `take` | 5697-5707 |
| the release | the entries, the pending and born rows; one `concatenate` per column | O(E + B) Python plus O(R + B) | Python loops; `store.extend` | 6214-6328, 5748-6211, 2049-2069 |
| the border | the live rows; the gone rows | O(R) plus O(gone) Python (a `click` line per row) | comparison, `take`; a loop | 6331-6465 |
| the merge | the live rows, 20 identity columns packed into 1 to 3 int64 words, then sorted | O(R log R) plus O(R x 26) | `_pack_words`, `argsort` or `lexsort`, `reduceat`, `take`; stores of 65536 rows and more cut into Node-aligned slabs on 4 threads | 6468-6534, 2139-2222, 1455-1564 (1496-1500), 1389-1390 |
| the gather of records | the layer's completed records and their offers | O(completions x cells) Python | Python | 6537-6708; `amplitude.py:901-1003`, `cells` 817-899 |
| the record | one dict and one `json.dumps` per line, a 1 MiB buffer | O(lines) Python | Python | `run.py:57-61` |
| the books | E x families x pending, per interval, from the runner | O(E x F x P) Python, no rows | Python | `engine.py:1433-1594`; `run.py:67` |

**Where the work is proportional to the live rows (the queue).** The walk,
the collision, the turn, the measure's gather, the border and the merge
visit the stores' arrays and nothing else: O(R) or O(R log R) in numpy
(the sorts at 4396, 3476, 1498-1500; the `np.unique` of the crowd at
3213 and 3225). Rows are grouped for the merge by a sort on a composite
packed key and not by a dict (1455-1470, 1496-1506), and summed by
`np.add.reduceat` (1513); the collision's lookup is one fancy index into
a table of 6561 slot states per (Node, number, content) group (3490).
The queue the owner asks for is what the stores are.

**Where the work is proportional to the GameBoard's size.** One place on
the interval's path: `interval_frame` allocates and scans `node_event`
and `occupied`, N_nodes entries each, every interval (3303, 3318, 3324);
the collision (3470), the turn (4030) and the measure (4598, 1962) read
them at the rows' indices only. Nothing sweeps every Node per measured
event: no O(E x N_nodes) path was found, and no O(E x R) path. The
diagnostics' dense arrays (2349-2370) are paid only by a host that reads
them, not by the law.

**Where the work is proportional to the record's length.** Only the
layer, per completed record: `Layer.complete` iterates the records whose
live count reached zero (`amplitude.py:910`), never every record;
`cells` takes the product over the arms and rescans `present` per cell
(848-859), and `gram_form` is O(S^2) in the phase support (788-799); the
`gathers` list, `gathered` and `aliases` grow for the whole run
(472-475, 998, 1001, 634) and are dumped into run.json at the end
(`run.py:243-248`).

**Where the work is Python per row (the slow paths).**

| Lines | What | How often |
| --- | --- | --- |
| 3833-3837 | `optical_rate_and_wall`: `for k in range(rate.shape[0])` calling `age_wall` | every live row, every interval |
| 3729-3766 | `momentum_pair` per pushed row (called from 3803, 4076, 4090) | the pushed rows |
| 4097-4102, 4123-4148 | the turn's residue rescale and Bresenham choice | the pushed rows x the fan |
| 4887-4913 | the beam pairing, nested loops | O(k^2) per set, k the paired rows |
| 4332-4355, 6438-6462, 5533-5572, 5259-5289 | the `click` and `pass` record lines, one dict and one `json.dumps` per row | every escaping, expiring, clicking or passed row |
| 4314-4329, 5361-5372, 5516-5531, 6420-6435 | `layer.end` per ending row | every ending row of a recorded family |
| 5021-5108 | `_family_plan`'s record shares, `exact_phase` and `optical_last_link` per taken row | every clicking row |

**Rows squared.** None over the store. The one quadratic loop is the beam
pairing at one set (4887-4913), quadratic in the rows paired at that set.

**Dead code.** `_walk_rows` (1402-1444) is defined and called nowhere in
`src/` or `tests/`.

## 2. The measurement, HOST only (main 412b81f1, 300 intervals per world)

The tool is `tools/profile_run.py`, a HOST tool: it steps a world in
process with the runner's record callback replaced by a counter (the
bytes `json.dumps(event) + "\n"` would write, counted and not written),
under cProfile, and prints per world the seconds per interval, the live
rows per interval (the sum of the stores' sizes after the interval), the
Nodes the live rows occupy (`np.unique` of the stores' `node` columns),
the record bytes and lines per interval, and the top functions by
cumulative time. The three worlds: the two slits under the one click
(`amplitude/slits_huygens.json`, 60 x 121 x 1, the paper's row 2a), the
clock's word (`clock_word/age_3.json`, 121 x 9 x 9, a lamp inside two
crowds, series T), light beside a mass (`lensing/mass.json`, 57 x 41 x 41,
1683 measured events, series K). The outputs stay under the scratchpad;
nothing is committed as a run; no reading is taken.

| World (HOST, 300 intervals under cProfile) | Seconds per interval (mean; the last 50) | Live rows per interval (mean; max) | Nodes occupied by the live rows (mean; max; of the GameBoard's Nodes) | Record per interval (bytes; lines; the kinds) | The top functions by cumulative time (of the run's total under cProfile) |
| --- | --- | --- | --- | --- | --- |
| the two slits, `amplitude/slits_huygens.json` | 0.707 s; 0.957 s (growing with the rows) | 203531; 258496 | 3826; 5115; of 7260 (53 percent) | 625103 bytes; 1740 lines; `click` 501471 of 522152 lines over the 300 intervals (96 percent), `record` 19021, `rerelease` and `split` 572 each, `birth` 299 | 211.9 s total: `_walk` 111.6 s (53 percent), of it `optical_walk_step` 85.8 s and `optical_rate_and_wall` 74.4 s (35 percent of the run; 62.8 s in the loop's own frame, 3833-3837); the gather threads' `result_iterator` 41.0 s (the merge's and the walk's slab threads on a store above 65536 rows); `optical_turn` 32.0 s; `CrowdMoments.__init__` 31.8 s over 600 calls (two builds per interval, 15 percent); `_measure` 30.6 s |
| the orbit, `orbit/s8_r12.json` (series D, 121 x 121 x 1, two bodies) | 0.0062 s; 0.0069 s | 1115; 1472 | 865; 1168; of 14641 | 1430 bytes; 7.7 lines; `click` 2129, `step` 147, `read` 19 | 1.86 s total: `_walk` 0.96 s (51 percent), `optical_walk_step` 0.56 s, `optical_rate_and_wall` 0.45 s (24 percent), `CrowdMoments.__init__` 0.29 s (15 percent), `optical_turn` 0.28 s, `_merge` 0.21 s |
| light beside a mass, `lensing/mass.json` (series K, 57 x 41 x 41, 1683 measured events, 1681 screen sets) | 0.098 s; 0.101 s | 12924; 14065 | 8386; 9257; of 95817 (9 percent) | 48229 bytes; 253 lines; `click` 74435 of 75998 lines (98 percent), `record` 1053, `birth` 300, `gather` 210 | 29.4 s total: `nature_beam` 24.5 s (83 percent), `_walk` 8.8 s (30 percent), `_measure` 7.1 s (24 percent), `optical_walk_step` 5.6 s, `_measured_arrays` 5.1 s (17 percent, 3.5 s in its own Python frame: the E-sized arrays built by list comprehensions over 1683 events, 4452-4487), `optical_rate_and_wall` 4.8 s (16 percent), `engine._frame_all` 3.6 s (12 percent: the Python loop over 1683 events, `engine.py:666-722`), `interval_frame` 2.6 s (9 percent: the dense per-Node arrays over 95817 Nodes and the first crowd build) |
| the clock's word, `clock_word/age_3.json` (series T, 121 x 9 x 9, a lamp inside two crowds) | 0.0067 s over 38 intervals | 312; 529 | 66; 86; of 9801 | 898 bytes; 4.6 lines; `click` 172, `birth` 9 | the run stopped at interval 39 with the law's refusal of the world at head (an OverflowError of the wall's square in `momentum_pair`, 3754: a physics event of this world under the generic entry, recorded here as HOST information only and not read; the orbit world stands in as the bodies' world) |

**What the profile says, HOST.** The interval's cost tracks the live rows
and not the GameBoard: 6 ms at 1.1 x 10^3 rows on 14641 Nodes, 98 ms at
1.3 x 10^4 rows on 95817 Nodes, 707 ms at 2.0 x 10^5 rows on 7260 Nodes,
about 3 to 8 microseconds per live row per interval; the two-slit world's
interval grows with its rows through the run (0.96 s over the last 50).
On every world the largest single function is the walk, and inside it the
Python loop `optical_rate_and_wall` (24 to 35 percent of the run); the
crowd's two builds per interval are 15 percent on the light worlds; the
per-event Python of the lensing world (`_measured_arrays`, `_frame_all`)
is 29 percent with 1683 events; the dense per-Node arrays are within
`interval_frame`'s 9 percent on the 95817-Node board and not visible on
the smaller ones. The record is per-row `click` lines: 96 to 98 percent
of the lines on the two light worlds (0.63 MB per interval on the two
slits, 2.7 GB for its registered 4300 intervals at this rate, HOST). The
dedicated CI runner of the register's runs is slower than this host by a
factor the register's own timings give (the mass world's 400 intervals
took 23.5 s of the runner on 2026-09-23, `DISAGREES.md` section 9, against
29.4 s here for 300 under cProfile's own overhead).

## 3. Under the corrected law (the event split), a COMPUTATION

The design: `docs/designs/event_split/DESIGN.md` sections 3, 5, 9 and 10
and `CORRECTIONS.md` sections 1 and 2 on the branch `event-split` at
e6f6b343 (the physicist's, not merged; nothing of it read as a rule
here). Build (ii), the record form: a recorded row of no content at
every Node it enters becomes K rows on the Node's outputs (K = 6 Ports
under pace (B), or the fan around its heading under pace (A); the
weights equal, the amount copied whole, the multiplicity times A), the
merge at the next Node sums the identical rows (the owner's word, record
1282, form G as the code has it: the same Node, direction, age, phase
modulo N / 2, record, branch, multiplicity), the grain deletes a branch
whose share falls below 1 / W at the Node where it falls (nothing kept at
the Node), and the click's trigger is the detector's sensitivity in the
counting form. The design's own bounds (section 3.2, section 4): the rows
of one record after k splits number K^k before the merge; after it, at
most (the Nodes within tau Links) x K x N / 2; a stray path falls below
the grain after log_K(W) intervals (4.6 for the six Ports at W = 4096,
1.8 for 91 outputs, 1.3 for 601); the whole-count multiplicity K^tau stays
under 2^63 for tau <= 24 at K = 6, 9 at 91, 6 at 601.

| World | Today (HOST, section 2) | Under the split, per live record, before the merge | After the merge (the bound), after the grain (the estimate) | The record per run |
| --- | --- | --- | --- | --- |
| the two slits (7260 Nodes, N = 64, the lamp's wheel W = 4096, the openings' fans of 1327 directions today) | 2.0 x 10^5 live rows, 0.7 s per interval, 96 percent of the record's lines per-row clicks | K^tau: 6^tau under pace (B) (46656 at tau = 6, 6^24 = 4.7 x 10^18 at tau = 24); 91^tau under pace (A) on the fan of 91 | at most 7260 x 6 x 32 = 1.39 x 10^6 rows per record (the design's bound); with the birth's 2^30 units over the front's 2 tau^2 + 2 tau + 1 Nodes the wave stays above the grain across the board (1.29 x 10^5 units per Node at tau = 64), so the estimate is the bound's order for the coherent front, of the order 10^5 to 10^6 rows per record; with a record born every interval and a flight of 60 to 180 intervals across the board, 10^7 to 10^8 live rows | the per-row `click` lines at 355 bytes each: the rows per set grow with the paths, so the record grows as the rows do; the runner's option to write the per-row click lines only on request (the Record Trimmer's, session 012fSQJ4kLi3L8iRafMAfWuJ, not touched here) is a condition of the run |
| the clock's word (9801 Nodes; the lamp `s_px1` of one direction, 2^20 units on the wheel [1, 64]; the two `mass` sources release rows of no phase circle, not recorded, which do not split) | 3 x 10^2 live rows (the crowd's), 7 ms per interval over the 38 intervals before the law's refusal at head | the lamp's records only: 6^tau per record before the merge | at most 9801 x 6 x 32 = 1.88 x 10^6 rows per record; the bar is 121 Links long, so a record fills the bar in about 110 intervals; the crowd's rows unchanged | the `click` lines of the lamp's records at the detector and the faces, growing with the rows; the crowd's rows write nothing |
| light beside a mass (95817 Nodes; the lamp `light` of 5 directions, 8.6 x 10^9 units on [1, 4096]; the mass `m` releases 290 directions of rows of no phase circle, not recorded) | 1.3 x 10^4 live rows (the crowd's bulk), 98 ms per interval, 98 percent of the record's lines per-row clicks | the beam's records only: 6^tau per record before the merge | at most 95817 x 6 x 32 = 1.84 x 10^7 rows per record; the flight to the screen is 57 Links, the front's Nodes in three dimensions grow as tau^3 (about 4 / 3 pi tau^3 / 6 within the box), so a record's rows reach the order 10^5 to 10^6 by the screen; the crowd's rows (today's bulk) unchanged | the screen's 1681 `wave` sets write one `record` line per set per interval as today and the per-row `click` lines grow with the rows |

**Where the present structures would make such a run long.** Under the
split the live rows grow by two to four orders on the light worlds, and
the interval's cost follows the table of section 1:

1. **The Python loops per row.** `optical_rate_and_wall` (3833-3837)
   runs `age_wall` once per live row per interval in Python: at 10^6 rows
   that is of the order of a second per interval before any numpy work.
   The per-row `click` lines (4332-4355, 5533-5572, 6438-6462), one dict
   and one `json.dumps` each, and `layer.end` per ending row (4314-4329,
   5516-5531, 6420-6435) scale the same way at the screens.
2. **The sorts and the gathers of 26 columns.** Three full-store
   re-orderings per interval (the walk's `argsort` and `take` 4396-4399,
   the measure's `keep` 5705-5707, the merge's `lexsort` and `take`
   1496-1540): O(R log R) each, on 208 bytes per row; at 10^7 rows about
   2 GB of store and several seconds per interval of memory traffic.
3. **The crowd built twice per interval** (3399 and 4025), two
   `np.unique` over all rows each time.
4. **The split itself** is a release per row: today the born rows come
   from Python loops over the pending rows and their directions
   (`_release_family` 5838-6083), K rows per live row per interval would
   be a Python loop over R x K unless written as one numpy `repeat` over
   the store (the build's, not this audit's).
5. **The grain** as designed deletes at the Node where a row falls below
   1 / W by the row's own accumulator against the wheel: a mask over the
   store, O(R), if written as one; a Python loop otherwise.
6. **Not a cost.** The dense per-Node array of the frame (3318) is
   O(N_nodes) and does not grow with the rows; the collision's table is
   fixed; nothing scans the whole GameBoard per event.

## 4. The findings and the recommendations, ranked by gain

The gain is a HOST estimate from section 2's profile; the test that
proves a fix changes no physics is the same for every row: the gate set's
digests (`examples/events/gate_set.json`, `tests/test_amplitude_click.py`
part (d)) byte identical; a short run's `events.jsonl` byte identical
before and after on the three worlds of section 2; `tests/test_integer_
algebra.py` green (no float, no root outside the list); the interval's
order of phases untouched (`nature_beam.py:3423-3460`).

| Rank | Finding | Lines | Cost class | The fix (a scheduling change, the law's order kept) | Gain (HOST estimate) | Proof |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | `age_wall` called per live row in a Python loop in the walk | 3833-3837 (`optical_rate_and_wall`), `core/integer.py` `age_wall` | O(R) Python every interval, on every world since the generic entry of the bending | the same integer arithmetic over the store's columns at once (the wall's stretch per row is an integer expression of rate, wall, coefficient and age moment: a numpy expression over int64, the bound checked as today); the function `age_wall` kept for the scalar callers | the walk's Python share of the interval on every world; on the lensing world of section 2 the largest single function under the walk; at 10^6 rows the difference between seconds and milliseconds | the gate set's digests; the events file byte identical; the gate test |
| 2 | the dense per-Node arrays rebuilt every interval | 3303, 3318, 3324 | O(N_nodes) per interval | keep `node_event` across intervals and update the Nodes of the bodies that moved and the sets that changed (the frame already lists them, 3342-3362); the boolean `occupied` derived once per change | small on boards below 10^5 Nodes (a fraction of a millisecond); on the 301^3 hubble_stars board (2.7 x 10^7 Nodes) of the order of 30 to 100 ms per interval, of the same order as the whole interval today | the same; no order changes |
| 3 | the per-row record lines: one dict and one `json.dumps` per clicking, escaping, expiring or passed row | 4332-4355, 5259-5289, 5533-5572, 6438-6462; `run.py:59-61` | O(rows ending) Python per interval; 97 to 98 percent of the record's bytes | the Record Trimmer's option (the runner's, not this audit's): the per-row click lines written on request; beside it, the lines of one interval and one set batched into one array-built string instead of a dict per row | on a world whose record is per-row clicks, most of the record's time and bytes (the 6 GB record of row 10 was 98 percent click lines); the batching a further constant factor | the events file byte identical when the lines are written; the digests |
| 4 | three full re-orderings of the store per interval (the walk's sort, the measure's keep, the merge's sort), each a gather of 26 columns | 4396-4399, 5705-5707, 1496-1540 | O(R log R) x 3, 208 bytes per row moved three times | one re-ordering per interval: the walk's `argsort` by Node kept (the collision and the measure read the store sorted by Node), the measure's `keep` and the merge's sort fused into the merge's one `lexsort` (the merge's key begins with the Node, 1455-1470, so its order is the walk's order refined) | a third of the interval's memory traffic on a large store; at 10^6 rows of the order of 100 ms per interval | the same; a question for the chief physicist only if the store's order between the measure and the merge is read by a rule (it is read by the border's `ages_at_key` as a mask, order-free, 6363) |
| 5 | the crowd built twice per interval | 3399, 4025 | O(R log R) x 2 | the first build's `np.unique` of the Nodes reused by the second where the walk's sort already gives the Node order (`searchsorted` on a sorted column instead of `np.unique`) | of the order of 10 to 20 percent of the interval on the crowd world | the same; the two builds read different rows (before and after the walk) by the law, so the two moments stay; only their construction changes |
| 6 | `momentum_pair` and the turn's Bresenham choice per pushed row in Python | 3729-3766, 4076-4102, 4123-4148 | O(pushed x fan) Python | the ladder `split_ladder` over the pushed rows as one vectorised comparison ladder (its squares are int64 by construction), the Bresenham choice as one argmin over the fan per row | on worlds with many pushed rows (the crowd worlds under the generic entry); small elsewhere | the same |
| 7 | the beam pairing, nested Python loops per set | 4887-4913 | O(k^2) per set | a sort of the paired rows by the pairing key per set | negligible today (k small); a guard for wide sets | the same |
| 8 | the layer's `cells` rescans `present` per cell and `gram_form` is O(S^2) per Node tuple | `amplitude.py:848-859, 788-799` | O(cells x keys) per completion | `present` computed once per completion; the Gram form over the support by one table lookup per pair as today, or the N x N table when stored (464-466) | per completion only; matters on records with many arms | the click's replay (`tools/amplitude_path.py`), the gate set |
| 9 | the run's audit keeps the books of every tick and run.json is one `json.dumps(indent=2)` at the end | `run.py:67-77, 224-227, 252` | O(T x F) objects held; one large dump | the runner's, not the engine's: stream the audit | the end-of-run pause on long runs; no interval cost | the run record byte identical |
| 10 | `_walk_rows` is dead code | 1402-1444 | none | delete on the physicist's word (the file is his) | none; clarity | the tests |

**What needs the chief physicist's word.** (a) Any change of the order in
which the phases run or the rows are visited within a phase where a rule
reads the order: the fused re-ordering of rank 4 if any rule reads the
store between the measure and the merge in a Node order; (b) the split's
build itself (section 3), a release per row at every Node, its pace and
weights (DESIGN.md section 5), its grain and trigger (section 4): the
owner's open choices, not a scheduling matter; (c) the deletion of
`_walk_rows`.

**What needs the owner's word.** (a) The split's pace ((A) the fan, (B)
the six Ports) and weights (equal or by angle): the pace multiplies the
rows per interval by K and sets the grain's reach; (b) the merge on the
GameBoard (form G, the code's) or only at the click (form K):
CORRECTIONS.md M6; under form K the rows are never summed on the board and
the live rows grow as K^tau to the grain, the HOST cost the design names;
(c) whether the per-row click lines are the run's record by default or on
request (the Record Trimmer's option), since under the split they are the
record's bulk.

**What this audit does not do.** It reads no physics, moves no number,
builds no fix and touches no engine line; the branches `event-split`,
`register-paper-sources` and `highlights-one-version` are untouched. The
build of any fix follows the Boss's GO after the physicist's read.

## 5. The machine for the full re-run (item (7) of the order; the owner's word of 05:55Z, record 1288)

Every experiment is re-run under the corrected engine after the split's
build, on strong machines if needed. This section counts the worlds from
the register, states the engine's process model from the code, measures
what can be measured (HOST) and estimates the rest (COMPUTATION from the
design's multiplicity, section 3), and from these names the machine.

**The worlds to re-run (the list's source: the register's world files).**
Under `examples/events/` at main 412b81f1 there are 341 world files (a
JSON object with `shape` and `measured`; the registers, readings and
generators excluded), 465924 registered intervals in all; 230 carry a
lamp (recorded rows, the split's subject) and 111 carry none (the
bodies' and the crowds' worlds, which do not split). PR #860 (the paper's
sources, `docs/designs/register_paper_sources/PLAN.md`) deletes 48 of
them (two_stars 3, masses 2, buildup 3, gallery 5, hand 4, catalog 4,
crowd_clock 8, cluster_clock 2, reader_clock 5, hubble_stars' gravity and
double worlds with their record copies 12), leaving 293. Beside them the
fail_rows worlds (`docs/designs/fail_rows/worlds/`, 11: the cart at k = 3
and 5 under the law and the key, the six J4 muon worlds,
`coasting_none_covariant_stamp` on the 27.3 M Node board) and the new_rows
worlds (`docs/designs/new_rows/worlds/`, 11: Malus at s = 16, 40, 48; the
Sagnac worlds at k = 3, 5, 9, 17 in two arrangements): 315 worlds after
PR #860, 363 before it. The gate set (`examples/events/gate_set.json`)
lists 18 at main (15 after PR #860). By series (the count, the largest
board, the registered intervals; the recorded ones marked): amplitude 73
(7260 Nodes, 141012 intervals; 72 recorded, the bell worlds on 21 Nodes
among them), optical 33 (95817; 18 recorded), coupling 21 (bodies),
bell 19 (21 Nodes), hubble_stars 18 (27270901; recorded), orbit_lamp 13
(14641; recorded), flow_link 13 (95817; recorded), weak 11 (68921;
bodies), lensing 9 (176505; recorded), shell_clock 9 (27450; recorded),
heisenberg 8 (19320; recorded), nucleus 8, orbit 8, quarks 7, bohr 7
(226981; bodies), atoms 6 (166375), drive_b 6, moving_detector 6
(recorded), covariant 4 (27270901), hubble 4 (27270901), clock_word 4
(recorded), newton_side 3 (95817; recorded), massive_rows 3 (recorded),
binding 3, redshift 2, lamp_shell 2 (recorded), c_measured 1
(274625; recorded), and the single worlds at the top of the folder.

**The engine's process model (the code).** One Python process per world:
`tools/run_series.py` starts each world as a child (`subprocess.Popen`,
line 151), at most `--jobs` at once (the machine's cores by default),
with `--wall-seconds` (a run killed past the wall clock and reported not
completed), `--memory-mb` (each run's address space bounded by RLIMIT_AS
and a stopped run reported), `--list examples/events/gate_set.json`
(the listed worlds at their listed ticks), `--fast`, and `--compare` (an
earlier summary against this one, exit 1 on a changed digest). Within
one run the interval is one thread of numpy integer arithmetic (numpy's
integer kernels take no BLAS threads), plus the engine's pool of 4 gather
threads on a store of 65536 rows and more (`_GATHER_THREADS`,
`_GATHER_ROWS`, `nature_beam.py:1389-1390`; the merge's Node-aligned
slabs 2182-2215): a light world above that size uses up to four cores
in its gathers and merges (the two slits' profile shows the pool's
`result_iterator` at 41 s of 212, HOST), a small world one core. Memory:
the stores at 208 bytes per row (26 int64 columns) plus the temporaries
of a re-ordering (an int64 `argsort` and a copy of the 26 columns, about
three times the store while a sort runs), the crowd's keys and moments
(a few ints per occupied Node), the layer's live records (Python dicts
per (Node, label, phase) key of each open record), the record stream's
1 MiB buffer, the books of every tick in the audit (`run.py:67-68`), and
the state snapshot streamed at the end. Measured peak RSS (HOST, one
process per world, 300 intervals): the orbit 55 MB (1.1 x 10^3 rows),
light beside a mass 78 MB (1.3 x 10^4 rows), the two slits 369 MB
(2.6 x 10^5 rows at most; the store itself 54 MB, the rest the sort's
temporaries, the layer's live records and the interpreter): about 1.4 KB
of peak memory per live row on the light world, seven times the store's
208 bytes, the ratio the estimates below use.

**Today's wall time (HOST rates x the registered intervals; cProfile's
overhead is in the rates, 20 to 30 percent).** The two slits: 4300
intervals at 0.7 to 1.0 s, 50 to 70 minutes; light beside a mass: 400 at
0.1 s, 40 s (the register's own time for `mass_g0` without cProfile
23.5 s, `DISAGREES.md` section 9); the orbit: 4000 at 6 ms, 25 s; the
largest boards (27.3 M Nodes): the register's 43 s for 400 intervals of
`coasting_none_covariant_stamp` (`RUN_4AB.md` section 2), of which the
dense per-Node array of the frame (finding 2) is the bulk at about 0.1 s
per interval. The whole register serially is of the order of hours of one
core today; the two heaviest worlds are the two slits above and row 10's
`w27_beam` (whose record reached 6.8 GB at interval 3664 without
completing, `DESIGN.md` section 9).

**Under the split (COMPUTATION, section 3; the split's own release step
not yet built, its cost not measured).** The 230 recorded worlds grow:
a light world's live rows reach 10^6 to 10^8 (the two slits: at most
1.39 x 10^6 per record after the merge, a record born per interval, a
flight of 60 to 180 intervals). At today's 3 to 8 microseconds per live
row per interval (the profile's rate) a store of 10^7 rows costs 30 to
80 s per interval, 36 to 96 hours for the two slits' 4300 intervals in
the present structures; with the top fixes of section 4 (the Python
loops vectorised, one re-ordering per interval, the crowd built once)
the rate falls toward 1 microsecond per row, 10 s per interval, about 12
hours per such world; the bodies' and crowds' worlds (111) are unchanged.
Peak memory at the measured 1.4 KB per live row: 10^6 rows 1.4 GB,
10^7 rows 14 GB, 10^8 rows 140 GB (beyond one process on a common host:
the grain and the merge decide where between 10^6 and 10^8 a world lands,
section 3; the store alone is 208 bytes per row, and the ratio falls if
the layer's dicts and the sort's temporaries are trimmed). The record on disk: the per-row `click` lines
at about 355 bytes per ending row per interval are the record's bulk
today (96 to 98 percent of the lines, 0.63 MB per interval on the two
slits, 2.7 GB per registered run at today's rows) and grow with the
rows under the split (10^5 rows ending per interval would be 35 MB per
interval, 150 GB per world), so the per-row lines written on request
(the Record Trimmer's option) is a condition of the re-run, not a
saving; without them a world's record is its set `record` lines, its
births and gathers, of the order of 10 to 100 MB, plus the state
snapshot at 208 bytes per live row at the end (2 GB at 10^7 rows).

**The machine for one day (an estimate; the assumptions named).** With
(a) the three top fixes of section 4 built and proved, (b) the per-row
click lines off by default, (c) the light worlds landing at 10^6 to 10^7
live rows: about 100 heavy worlds (the recorded worlds on boards of 7260
Nodes and more: the screen worlds of amplitude, heisenberg,
massive_rows, optical, lensing, flow_link, newton_side, lamp_shell,
shell_clock, orbit_lamp, hubble_stars) at 4 to 12 hours each, and the
other 215 in minutes each. One world per process, N at once: 100 worlds
x 8 hours / 24 hours is 33 processes busy through the day, so 48 to 64
cores (each heavy world also takes up to 4 threads in its gathers), 16 GB
per heavy process at 10^7 live rows (1.4 KB per row measured, section 2)
bounded by `--memory-mb` (a run past the bound is reported, not lost),
1 TB of memory for 64 at once (512 GB for 32 at once and two days), and
2 TB of disk for the records and the snapshots (the record grows to tens
of GB per world if the per-row lines stay on). A world that lands at
10^8 rows needs 140 GB by itself and is a run on its own machine or a
run that waits on the grain's word. Without the fixes the same machine takes about a week, or the day
needs of the order of 300 cores and the memory to match; a second
machine halves either. The runner's form, the existing one (HOST):

    PYTHONPATH=src python tools/run_series.py --jobs 48 --out runs/rerun \
        --wall-seconds 86400 --memory-mb 12000 <the world files>

with the world list taken from the register (the 315 files above; the
gate set by `--list examples/events/gate_set.json`), every world in its
own process, `summary.json` per batch and `--compare` against the base
run for the digests; the batch of the small worlds first, the heavy ones
after, so that the cores stay full. The numbers measured here are the
HOST profiles of section 2 and the peak RSS above; the rows under the
split, the seconds per interval at those rows, and the disk under the
split are estimates from the design's multiplicity and the measured
rates, to be measured at the build's first run on one world before the
machine is ordered.

## 6. The record's writing against the compute: in memory or on disk (the owner's order of 06:44Z, record 1303)

The model owner's assumption: the experiments would run faster kept in
memory and written to disk at the end, if wanted. Measured here, HOST,
on the three worlds of section 2, 300 intervals each, the runner's own
loop replicated by `tools/profile_run.py --writer` (a record line per
event into `events.jsonl` through the runner's 1 MiB buffer, the books
of every interval kept for the audit as `run.py:66-68` keeps them,
`state.json` streamed and `run.json` dumped at the end), each world in
its own process, three modes: ON (every line, today's default on main),
OFF (the measure rule's per-row `click` lines dropped by the same guard
as the runner's `--omit-row-clicks` of PR #1026: the lines carrying a
`reading`), MEMORY (every line held as a string and written once at the
end). No reading is taken; the files are deleted after the measurement.

| World, mode (HOST) | Wall, 300 intervals | The compute (the interval) | The books per interval (the audit) | `json.dumps` | the `write` calls | the end flush | `state.json` | `run.json` | The writing, all | `events.jsonl` | Held in memory | Peak RSS |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| the orbit, ON | 1.4 s | 1.2 s | 0.02 s | 0.02 s (1.2 percent) | 0.00 s (0.2 percent) | 0 | 0.08 s | 0.00 s | 0.10 s, 7.6 percent | 0.43 MB (1430 bytes per interval), 2295 lines | 0 | 46 MB |
| the orbit, OFF | 1.3 s | 1.2 s | 0.02 s | 0.02 s | 0.00 s | 0 | 0.08 s | 0.00 s | 0.10 s, 7.4 percent | the same (no per-row click line in this world) | 0 | 46 MB |
| the orbit, MEMORY | 1.4 s | 1.3 s | 0.02 s | 0.02 s | 0 | 0.00 s | 0.08 s | 0.00 s | 0.10 s, 7.2 percent | the same | 0.43 MB | 46 MB |
| light beside a mass, ON | 27.1 s | 21.3 s | 4.46 s (16 percent) | 0.35 s (1.3 percent) | 0.06 s (0.2 percent) | 0 | 0.87 s | 0.01 s | 1.29 s, 4.8 percent | 14.5 MB (48229 per interval), 75998 lines | 0 | 91 MB |
| light beside a mass, OFF | 26.4 s | 20.8 s | 4.33 s | 0.34 s | 0.06 s | 0 | 0.82 s | 0.01 s | 1.23 s, 4.7 percent | 14.1 MB (47158 per interval), 74945 lines, 1053 dropped | 0 | 91 MB |
| light beside a mass, MEMORY | 27.8 s | 22.0 s | 4.49 s | 0.36 s | 0 | 0.10 s | 0.85 s | 0.01 s | 1.32 s, 4.8 percent | 14.5 MB | 14.5 MB | 126 MB |
| the two slits, ON | 165.0 s | 156.8 s | 0.74 s | 3.14 s (1.9 percent) | 0.46 s (0.3 percent) | 0 | 3.83 s (2.3 percent) | 0.04 s | 7.47 s, 4.5 percent | 187.5 MB (625103 per interval), 522085 lines | 0 | 373 MB |
| the two slits, OFF | 163.2 s | 157.3 s | 0.73 s | 1.10 s (0.7 percent) | 0.17 s (0.1 percent) | 0 | 3.92 s | 0.04 s | 5.23 s, 3.2 percent | 63.7 MB (212380 per interval), 194556 lines, 327529 dropped (63 percent of the lines) | 0 | 367 MB |
| the two slits, MEMORY | 167.5 s | 158.1 s | 0.76 s | 3.42 s | 0 | 1.25 s | 3.92 s | 0.05 s | 8.64 s, 5.2 percent | 187.5 MB | 187.5 MB | 928 MB |

**What the numbers say (HOST).** The record's writing is 4.5 to 7.6
percent of the wall time with every line on, and of that the `write`
calls themselves are 0.2 to 0.3 percent: the runner's stream is buffered
by the megabyte (`run.py:57`), so the disk is touched once per MiB and
the operating system's page cache takes the rest. The larger parts of
the writing are the serialisation (`json.dumps`, 1.2 to 1.9 percent, one
call per line) and the state snapshot at the end (`state.json`, 2.3
percent on the two slits, 0.1 GB written once). Holding the record in
memory and writing it once at the end saved nothing on any world (the
wall time within the run-to-run noise: 165.0 s ON against 167.5 s
MEMORY on the two slits, 27.1 against 27.8 on the lensing, 1.4 against
1.4 on the orbit): the serialisation is paid either way, the end flush
(1.25 s for 187 MB) replaces the buffered writes (0.46 s), and the record
held costs memory equal to its size plus the interpreter's per-string
overhead, 555 MB more on the two slits (928 against 373 MB at peak) for
187 MB of lines, 35 MB more on the lensing. The per-row click lines off
(the Trimmer's default in flight) is the real saving of the writer: on
the two slits 63 percent of the lines, two thirds of the record's bytes,
2.0 s of 7.5 s of writing; on the bodies' and crowds' worlds nothing,
since their records are not per-row click lines. Larger than the writer
on the crowd world is the runner's books per interval (`run.py:67`,
`engine.books`, 4.5 s of 27.1, 16 percent: the Python loop over 1683
measured events and their families, `engine.py:1465-1469`, the charge's
`units` tuple built per event per interval, `measured.py:742-747`), a
HOST cost of the conservation check that a cache of the unchanged events'
charges would remove; it is not the record.

**The answer to the assumption.** The record is already written from
memory: a run does not wait on the disk per interval. An in-memory record
with one write at the end would save, per world, of the order of 0.2 to
0.3 percent of the wall time (the `write` calls) and would cost the whole
record's size in memory for the length of the run: the two slits'
registered 4300 intervals at 0.63 MB per interval are 2.7 GB held (8 GB
with the interpreter's overhead at the measured ratio of three) for a
saving of about 7 s in an hour; with the per-row lines off, 0.9 GB held
for about 2 s. For the split's case of section 3 (10^7 live rows, the
per-row lines off as the condition), the record per interval is the set
`record` lines, the births and the gathers, of the order of 1 to 10 MB
per interval by the rows ending at the sets, 4 to 40 GB per run held in
memory against a saving of the same 0.2 to 0.3 percent, while the store
itself is 14 GB at that size (section 5): an in-memory record would
double or triple the run's memory to save a fraction of a percent, and a
run killed at the wall clock would lose the record entirely. The present
form is the faster one in every case measured.

**The smallest form, if the owner still wants the option (nothing
built).** A HOST option of the runner, `--record-in-memory`, off by
default, that keeps the lines in a list and writes them in the `finally`
of the run; the streaming write stays the default because a killed run
(`--wall-seconds`, `--memory-mb`, a crash) keeps its partial record and
the audit up to the last interval, which the readers and the reviewers
use to name the interval of a refusal. What a killed run loses under each
form:

| The form | `events.jsonl` up to the kill | `state.json` | `run.json` (the audit, the books per interval) | The interval of a refusal |
| --- | --- | --- | --- | --- |
| streaming, buffered by 1 MiB (today) | kept to the last flushed MiB (at most the last MiB lost on a hard kill; nothing on a refusal, which the runner records and then flushes) | written by the runner on a refusal; lost on a hard kill | written by the runner on a refusal; lost on a hard kill | named by the runner on a refusal |
| in memory, one write at the end | lost entirely on a hard kill; written in the `finally` on a refusal | the same as today | the same as today | the same on a refusal; nothing on a hard kill |

The recommendation is not to build it: the measured gain is below the
noise of a run, the memory cost is the record's size, and the loss on a
kill is the whole record. What does pay, on the record's side, is the
Trimmer's default (the per-row click lines off), and on the runner's
side the cached charges of the books per interval on worlds with many
measured events; both are HOST changes that leave every kept line byte
identical, proved by the events file of a run with the lines on compared
before and after.

## 7. Links

- `tools/profile_run.py`: the HOST profiler of section 2 and the record
  writer's measurement of section 6 (`--writer on|off|memory`).
- `docs/designs/event_split/DESIGN.md` and `CORRECTIONS.md` (the branch
  `event-split` at e6f6b343): the design section 3 estimates against.
- `docs/ENGINE.md`: the engine's readings by type.
- `docs/designs/register_paper_sources/NODE_ALGEBRA.md`: the six verbs at a
  Node, the audit this one follows in form.
