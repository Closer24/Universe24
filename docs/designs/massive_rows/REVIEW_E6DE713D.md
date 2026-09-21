# Physics-rule review of `massive-rows-fast` at e6de713d: the massive rows beside the covariant readings, with the speed-up, before the merge to main

The open-problems physicist acting as the physics-rule reviewer,
2026-09-21, on the Boss's bounded order of 17:15Z (record 462: the
Architect's head `e6de713dea569f4d3afd64244b7cef6ab81b0cf0`, one merge
commit over N check's 70df6514 bringing the builder's WIP 4ca770a2 and
origin/main 93f46617). Read-only: nothing edited on the branch, no world
file changed, no registered number moved. Read: the diff of the head
against main `9ca2d276` (30 files, 3701 insertions: `world.py`,
`nature_beam.py`, `amplitude.py`, `engine.py`, `measured.py`, `run.py`,
`tests/test_massive_rows.py`, the docs and the worlds of
`examples/events/massive_rows/`), the design
[DESIGN.md](DESIGN.md) with its three review rounds (8, 8b), HYPOTHESES
entry 26 and the register entry "S, the massive rows" on the head,
BEAM_LAW section 2 and ENGINE.md as amended there, the covariant readings
as merged (PR #582). Every number below is a GAMEBOARD reading (a
digest, a count, a table entry) unless marked DETECTOR; the host checks
I ran are named as host checks. The Boss's five questions are the five
sections.

Notation, once (record 369): **p** the momentum vector in label units and
p its magnitude; **p**_D the label of a massive row on the direction D at
the scale p; Q = 64 the label's scale, S the width, M a row's content;
E'_0 = Q S M the rest energy and E'_D = isqrt(E'_0^2 + 3 **p**_D . **p**_D)
the wall of the flight on D, both in mass units; T_D = isqrt(3 |D|^2 Q^2)
the flight's resolution; h the world's `action`, N the phase circle; f_F
and q_F a family's placed fraction and completion quantum, (1, 0) for
every family without the flag and (0, M) with it; `by_drive_rows` the
count primitive on the rows' accumulators.

## VERDICT: ADMISSIBLE

The head may merge to main. (1) With both keys off the speed-up changes
no integer of the law: the slab merge, the packed words, the threaded
gathers and walk chunks and the bulk recoil are each proved equal to the
one-shot code by construction and shown equal on the host (the merge on
220 000 random rows in three regimes, the registered two-slit world for
60 intervals on main and on the head, the pin world for 200 intervals on
the head with four threads and with one: every digest equal). (2) The
new code paths keep LOCALITY-1: no state at a Node between intervals, no
Node-keyed cache, no rule reads the books; the one global is a thread
pool that holds no data. (3) The two identities are independent in
`world.py` (two keys, two parsers, no branch on a kind) and cannot even
coexist in one world today (a massive family needs `action`, the
covariant key is refused with it). (4) HYPOTHESES 26's declarations and
pins are what the code does, integer for integer where I could recompute
them. (5) The three tests pass for every rule built. Two should-fixes,
both documents, neither blocking: the register's series letter S is used
twice on the head (the massive rows and the covariant readings), and the
design's sentence "the photon's table is Flight's by value" should carry
the one number on which the two identities would meet (the 3 of E'_D is
Flight's constant, the covariant key's d is declared) for the day both
keys are wanted in one world.

## 1. Bit-exactness with both keys off

**By construction, each new path.**

- *The merge per Node slab* (`NatureBeamStore.merge`, `_merge_rows`). The
  old merge took one stable sort of the whole store on the packed key (or
  the lexsort of the eleven identity columns), summed amounts and shares
  per group of identical rows by `reduceat` in the sorted order, kept
  every other field from the group's first row in that order, then
  cancelled under the amplitude key. The new merge cuts the store into
  slabs of whole Nodes and merges each slab by the same body
  (`_merge_rows` is the old body transcribed: the same `identity_columns`
  logic inline, the same reductions, the same cancel). It is the same
  total order because the Node is the order's first field: the store at
  the merge is the walk's Node-sorted rows (`store.sort()` at the walk,
  nature_beam.py:3345) followed by the interval's releases appended in no
  order; the slabs are cut at Node values of the sorted prefix
  (`searchsorted` on `node[:prefix]`, the thresholds `node[at]`), and
  every appended row joins the slab of its Node value after the prefix's
  rows (`searchsorted(thresholds, node[prefix:], side="right")`, the same
  half-open ranges as the cuts), so each slab holds every row of its Node
  range in the store's own order; a stable sort within a slab is then the
  global stable sort restricted to that range, groups never straddle slabs
  (a group is one Node), and the slabs concatenated in Node order are the
  global sorted store. The cancel dict is merged in slab order, which is
  the old Node order, so the `cancel` lines of `events.jsonl` come in the
  same sequence. Rows of different Nodes never merge, as the law says.
- *The packed words* (`merge_words`, `_pack_words`). The old `merge_key`
  packed the identity fields into one 62-bit word or fell back to the
  lexsort of the fields; the new one packs into as many words as the
  widths need, no field split across two words, each field offset to its
  least value, the first word the most significant, and sorts by the one
  word or by the lexsort of the words. Lexicographic order on the words
  equals lexicographic order on the fields (each word is a fixed-width
  concatenation of non-negative fields in field order), and equal words
  are identical rows; `argsort(kind="stable")` and `lexsort` are both
  stable, so ties keep the store order as before. The old one-word case
  is the new one-word case, byte for byte.
- *The threaded gathers and joins* (`take`, `append`, `_gather`, `_pool`).
  A gather per field is one field's alone; `Executor.map` returns the
  results in submission order; the fields are reassigned in `FIELDS`
  order. No integer is formed on a thread that depends on another
  thread's result.
- *The walk in chunks* (`_walk_rows`). The per-row arithmetic of the walk
  (the family's `walk_step`, the coordinates, the wrap, the escape) is
  applied to row ranges and concatenated in order: a pure function of each
  row's own fields, so the chunking is a no-op on the numbers.
- *The bulk recoil* (`born_recoil`). The vectorised form computes
  `abs(label x amount) // multiplicity` with the sign restored, which is
  `share_of(label, amount, multiplicity)[0]` at accumulator 0
  (nature_beam.py:1460-1463, the truncation toward zero), summed exactly
  by `exact_column_sums`; when the product could leave the working
  register it falls back to the row loop. The same integers.
- *The tables by value* (`FamilyFlight`, `family_flight`). A family
  without the flag carries Flight's triple (2 S_1 Q, 2 T_D, T_D), Flight's
  labels u_D, the turn `phase_per_link` over 1 (the count per Link as it
  was, the remainder 0 at every step, so `acc_turn` stays 0 on every row
  and takes 0 bits in the packed key) and the pair (1, 0), so `kept = 0`
  at every end and `_place_completion` returns before touching the books;
  the `waiting`, `massive` and `acc_turn` lines are written under the key
  alone (`engine.py`, `run.py`, `record_line`).

**On the host (my checks, this session, the project's venv, Python
3.14.0rc2, numpy 2.5.3).** The merge alone: a deterministic random store
of 220 000 rows (a Node-sorted prefix of 180 000 and 40 000 appended in
no order; records on both halves of the circle) merged with modulus 0 and
64 on main's engine and on the head with `_GATHER_THREADS` 4 (slabs on
the pool) and 1 (one slab, no pool), in three regimes: sparse duplicates
(219 989 rows kept, 1 cancel), dense duplicates (120 616 kept, 6 cancels)
and wide fields forcing the fallback (two packed words on the head, the
eleven-column lexsort on main; 145 780 kept, 8 cancels). The sha256 of
every field and of the cancel dict was equal in all nine runs. The
branch's own tests: `tests/test_massive_rows.py` and the gate and
byte-identity tests of `tests/test_amplitude_click.py`, 45 passed on the
head in a scratch worktree. The whole-run digests (the runner, the same
world file, `state.json`, the books and `events.jsonl`):

| World | Tree | Threads | Intervals | State | Books | Events | Equal |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `amplitude/slits_huygens` (both keys off, the registered two-slit world, 1332-direction fans) | main 9ca2d276 | the old code | 150 | 4454e07f... | 88479142... | 922cc53a... | |
| the same | e6de713d | 4 | 150 | 4454e07f... | 88479142... | 922cc53a... | EQUAL to main |
| `massive_rows/slits_matter_1024` (the pin world, `massive_rows` on) | e6de713d | 4 | 400 | 05878d84... | 45319a42... | 47ab5d25... | |
| the same | e6de713d | 1 | 400 | 05878d84... | 45319a42... | 47ab5d25... | EQUAL to four threads |

(The digests are the first 20 hex digits of the sha256 of `state.json`,
of the books (the audit of `run.json`, JSON-encoded) and of
`events.jsonl`; the books balanced at every tick in all four runs; the
pin world at 400 intervals took 44 s on four threads and 56 s on one; the
rows in flight at the end were 258 486 in the two-slit world and 690 585
in the pin world, above the 65 536-row threshold at which the slabs, the
threaded gathers and the walk chunks engage, so the new paths were
exercised; the shorter runs of 60 and 200 intervals gave the same
equalities.)

The Boss's gates, reported and not re-run by me: `tools/check.py` exit 0
(1154 passed, 1 xfailed), the gate set at its caps SAME on the nine
registered digests, the pin world's 300 intervals identical to the
builder's WIP 4ca770a2 (54086740..., 55a1bbff..., 294aa734...).

## 2. LOCALITY-1 in the new code paths

- The slab merge reads the store's fields of the interval and writes the
  merged fields; the slabs are views and copies of the interval's arrays;
  nothing survives the call but the store itself, as before.
- The thread pool `_gather_pool` is the one new module global: a
  `ThreadPoolExecutor` of four workers, created on first use, holding no
  data between calls; the thread count is a host constant (not read from
  the machine) and the numbers do not depend on it (section 1). It is
  host machinery in the class of numpy's own threads.
- `_walk_rows` chunks rows by index; each chunk reads its rows' own
  fields and the world's constants (the periodic axes, the extents) and
  writes nothing shared.
- `born_recoil` sums the labels of the rows born at one release at one
  Node: the emitter's own record.
- No new code path reads the books (`Ledger`) to decide a rule; the books
  are written (the `waiting` lines) and read only by the reports. No
  Node-keyed cache exists; `FamilyFlight` is a table over directions
  formed at load, not per Node.
- The identity's own non-local step is the record's completion through
  the apparatus's layer (`gather_records`, `_place_completion`), named by
  the design (section 3, item 4) and admitted by the owner's record 332:
  the one operation at the one-way border, now moving one quantum and
  one label to the chosen set and the rest to the cancelled lines. It is
  the layer's operation as before, not a new reading at a distance during
  the flight.

## 3. The two identities' independence in `world.py`

- Two keys, two shapes: `massive_rows` a boolean of the world with the
  family flag `massive` and the lamp key `momentum_magnitude` under it;
  `covariant_readings` one object (`c2`, `grain`, `books`) with the
  measured-event key `E` under it. Two parsers: `_massive` and
  `_massive_families` (the flag's refusals, the magnitude resolved from
  the family's lamps, the ceilings at load) against `_covariant` (the
  pair, the grain, the domain, the declared `E`, the identity's
  diagnostic); `parse_nature_beam_world` calls each once and
  `NatureBeamWorld` carries `massive_rows: bool` and `covariant:
  CovariantDeclaration | None` as two fields; `hypotheses` appends
  `massive-rows-v1` after `amplitude-v1` and `covariant-readings-v1`
  after `hand-v1`, each on its own key.
- No branch on a kind: the run-time reads are values (`table.placed`,
  `table.quantum`, `table.content`, the triple, the turn table) formed at
  load by `family_flight`, which branches on the flag once at load, as
  the design's value form requires; the covariant frame reads the
  declaration's grain and factor. The one run-time branch on a family
  key, `_massive`'s refusal of a free family, is at load.
- They cannot coexist today: a massive family needs the world's `action`
  (the turn's h), and `covariant_readings` is refused with `action`
  (17.6 S4). So no world can declare both, no shared field is touched by
  both (`acc_turn` on rows, `CovariantReadings` on bodies; a massive row
  is never a body until its completion places its quantum), and the OFF
  path of each is the other's ON path's baseline. Independence holds by
  construction; the day both are wanted in one world (a massive record
  completing into a body that then carries E') is a design, not this
  merge's concern (should-fix S2).

## 4. The declarations and the pins against the code

HYPOTHESES 26 and the register entry, checked line by line against
`world.py`, `nature_beam.py` and the shipped worlds:

| Declared | In the code | Recomputed by me (host) |
| --- | --- | --- |
| the label p_D, the integer vector nearest p D / abs(D) by `unit_label`'s rule at the scale p | `scaled_label` (world.py), `family_flight` | at Q it is `unit_label` (the test (b)); on (1, 1, 0) at p = 220 the label (156, 156, 0) |
| the flight at the rate 2 abs(p_D)_1 against the wall 2 E'_D from the start E'_D, E'_D = isqrt(E'_0^2 + 3 p_D . p_D) at load | `flight_triple`, `FamilyFlight.walk_step` (the same `by_drive_rows`) | E'_0 = 4096 (S = 1, M = 64); on the heading E'_D = isqrt(4096^2 + 3 x 220^2) = 4113; on the diagonal isqrt(4096^2 + 3 x 2 x 156^2) = 4113 (the entry (624, 8226, 4113), the test (g)); 4113 on every direction since 3 p_D . p_D spans 144 270 to 146 130 within [4113^2, 4114^2) |
| the photon its E'_0 = 0 case, one primitive | `flight_triple(Q D, 0)` = (2 S_1 Q, 2 T_D, T_D) | the test (b): 1332 of 1332 directions of the pin's table with the flight vector Q D |
| de Broglie's turn abs(p_a) N / h at every axis Link on one accumulator | `FamilyFlight.turned`, `by_drive_rows(acc_turn, turn[direction, axis], h)` at the walk; `acc_turn` an identity field of the merge | 220 x 64 / 1024 = 55 / 4 steps per axis Link; the wavelength h / p = 1024 / 220 = 4.6545 Links; the test (e) reads the plane wave to one remainder |
| the pace p / E' | the triple | 220 / 4113 = 0.05349 Links per interval = 0.0926 c |
| the completion hands ONE quantum M and the one label of the chosen row's direction to the chosen set; the rest cancelled; the pair (1, 0) for every other family | `Layer.end(placed, direction)`, `Offer.waiting_*`, `_place_completion`, `node_choice` on the waiting units per direction (the ladder's rungs, no draw); `Ledger.wait` and the `waiting` lines | the test (c) at the open faces, (e) at a screen; the books' identities (e) |
| every family carries the same tables by value, no flag read at run time | `family_flight` at load; the walk, the labels, the turn and the placement read `frame.family_flights[family]` | the gate test (a): (1, 0) on every family of every gate world, `acc_turn` absent from `state.json` |
| the pin `slits_matter`: the lamp leg 139 (the photon's 13) | the accumulator rule on the engine's lines (the test (g)) | age_of(11 Links) on (1, 1, 0): ceil((11 x 8226 - 4113) / 624) = 139; the photon's ceil((11 x 312 - 156) / 256) = 13 |
| the first `click` line at `screen_60` about 955 within 5, at `screen_37` and `screen_83` about 1016; the bands at 36.5, 60, 83.5; Pearson 0.89 +- 0.03; the visibility 0.95 +- 0.03; the dark pixels 0 to 3 (DETECTOR) | `expectations.json` under `slits_matter` and `slits_matter_1024`, read by `read_run.py` | not recomputed here (the round-2 map's and the test (g)'s numbers stand); the 1024-birth run's PASS is the Boss's report (record 460), N check re-reading it on this head |
| the refusals (the flag without the key, with `phase_per_link`, on a free family, without a phase circle, without `action`; the magnitude absent, elsewhere, below 1, two values; no lamp; `age_bound` absent; the ceilings; the turn 2 at a birth; the inverse interval) | `_massive`, `_lamp`, `_massive_families`, `_release_family`, `_inverse_interval` | the test (d), every message matched |

The register's entry S names the design "ADMISSIBLE in the physics-rule
review's three rounds", which DESIGN.md sections 8 and 8b carry (round 3
at b1248102, no blocking finding). Nothing declared is absent from the
code and nothing in the code is undeclared, with one remark: the design
says the completion's rule is stated in the value form so that "no flag
is read at run time", and the build honours it (`placed`, `quantum`,
`content` are table values), while `_release_family` refuses a massive
birth at a turn other than 1 by `table.content and cost != table.content`,
a value check, as the design's M3 asks.

## 5. The three tests

1. **The flight of a massive row** (the triple per direction, one
   `by_drive_rows`): generic PASS (one primitive, the family's declared
   integers M, p, S, no name read at run time); vector PASS (the
   translation on the digital line with a wall, E'_D one integer root per
   direction at load in T_D's class, p_D one rounding per direction in
   u_D's class, both declared); local PASS (the row's own record and its
   family's table).
2. **The turn** (`by_drive_rows` on `acc_turn` at every axis Link):
   generic PASS (`phase_per_link` over 1 for every other family, the same
   verb); vector PASS (the Euclidean division with the remainder kept on
   one accumulator, no root, no float, `acc_turn` below h); local PASS
   (its own record).
3. **The label** `content x p_D` (`momentum_labels` on the family's
   table): generic, vector (bilinear at load), local: PASS.
4. **The completion** (the pair (f_F, q_F), the waiting in the record's
   offers, the placement by the ladder's rungs): generic PASS (two
   declared integers per family by value); vector PASS (additions of
   content and momentum, the rungs' Euclidean division, no draw); local
   PASS with the price named (the layer's one operation at the one-way
   border, record 332).
5. **The speed-up** (the slabs, the words, the threads, the bulk recoil):
   not a rule but an implementation of the merge, the walk and the recoil
   as they were; it passes by section 1 (no integer changed) and section
   2 (no state, no cache, no reading of the books).

## 6. Should-fixes (documents, not blocking)

- **S1, the series letter.** On the head `docs/EXPERIMENTS.md` carries two
  entries headed "S": "S, the massive rows (2026-09-21)" (line 4219) and
  "S, the covariant readings (2026-09-21)" (line 6449, merged from main
  after the branch chose its letter). One of them takes the next free
  letter, and HYPOTHESES 26, the series README and TEST_EXPECTATIONS
  follow; the Boss's call which.
- **S2, the two identities in one world.** The design's sentence "the
  photon's table is Flight's by value" and HYPOTHESES 26 should state
  once that the 3 in E'_D = isqrt(E'_0^2 + 3 p_D . p_D) is Flight's
  constant (T_D = isqrt(3 |D|^2 Q^2), the identity at E'_0 = 0 needs it),
  where the covariant key declares its d; a world that one day carries a
  massive record completing into a body under `covariant_readings` must
  declare d = 3, and the composition with `action` (17.6 S4) is that
  design's first sentence. Nothing to build now.

## 7. What stands, in one paragraph for the Boss

The head e6de713d carries `massive-rows-v1` as designed and reviewed
three times, beside `covariant-readings-v1` as merged, both keys off by
default, with the Architect's speed-up: the merge per Node slab on packed
words, the gathers, joins and walk chunks on four threads, the born rows'
recoil in bulk. Each of these is the old computation in a different
order of evaluation whose result cannot depend on the order, and the host
shows it: the same digests on main and on the head for the registered
two-slit world, the same digests on the head with four threads and with
one for the pin world, the same merge of 220 000 random rows in three
regimes on both engines. LOCALITY-1 holds in every new path, the two
identities are independent and cannot meet in one world today, the
declarations and pins are the code's, the three tests pass. Verdict:
ADMISSIBLE; the merge to main may proceed, the two should-fixes as a docs
follow-up.
