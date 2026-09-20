# `amplitude-v1`: the design (read-only, the physicist and the mathematician, 2026-09-20)

Base: `a9c12384` (main, the merge of #366) read at the start; the owner's
additions read from the branch at `d88539c8` and after (Highlights 5.4:
the click generators, the corrected sentence and the wave, the click
defined by what it does, the two forms of the click, the ten points of one
quantum, the decision for form A at `a3d87cef`, the gate between records).
Nothing in the repository was edited. Check scripts and their outputs
beside this file: `tables.py/.txt`, `mz.py/.txt`, `bell.py/.txt`,
`gate.py/.txt`, `slits_world.py`, `slits_read.py/slits.txt` (two engine
runs in `one_birth_run/` and `crowd_run/`, the engine as it is). The
prototype the other session names, `scratchpad/amp/proto.py`, is absent
from this session's scratchpad (`scratchpad/impl/patch_amplitude.py` is an
older amplitude-scale patch, not it); the prototype's numbers are taken
from issue #365 comment 2 as reported there.

Every integer below is from the scripts unless marked "stated". N = 64
unless said; the 1/256 tables `C`, `S` of `core/phase.py` at N and the
half-angle tables `C'`, `S'` at 2N = 128 (the same function, `phase_cosines(128)`);
`v(p) = (C[p], S[p])`; the pointer unit `2^26 = (32 x 256)^2`.

Facts of the tables the design leans on (`tables.txt`): the quarter turn
and the half turn are exact on the tables at every N (`C[p + N/4] = -S[p]`,
`S[p + N/4] = C[p]`, `C[p + N/2] = -C[p]`); `C^2 + S^2` is 65536 +- 237 at
N = 64 (0.36 %), +- 315 at N >= 1024; `C[N/8] = S[N/8] = 181`;
`C_64[8] = 181`, `C_64[24] = -181`.

---

## 0. The corrected sentence, the wave, and what this design changes (the owner's standing form)

"The world is the list of clicks. The GameBoard computes every possible
future between click and click, and the next click chooses and adds a row
to the list." Under the key `amplitude`:

- The GameBoard: unchanged. The flight table, the collision table, the
  meeting, the clocks, the push, the books over every row. Two int64
  columns are added to the store (`record`, `branch`) and one more
  (`multiplicity`, section 1) that the flight and the collision never read.
- The click's reading is a THIRD form under the key, named `sum` (the
  detector key `reading: "sum"`, refused without the key): the set reads
  the sum of the rows OF ONE RECORD AND ONE LABEL that arrived at its Nodes,
  squared, accumulated over the record's lifetime; the choice by u follows
  that sum. `beam` (the count) and `wave` (the crowd's pointer per interval)
  stay as they are for every world without the key, byte for byte. The
  amount reading stays for matter. (The owner: "a detector that reads
  amount does not see a wave because it does not read a sum".)
- The world's list: one row per click: `(tick, node, detector, family,
  record, u, channel, weight, total, combinations before, combinations
  after)`; section 5.
- The sum is never over the crowd (rows of different records): that
  reading is `wave`, it gave the pilot no single-click fringe (T4) and
  #363's amount reading gave S = 2. The rows of a record arrive at a set
  over several intervals; the accumulation waits for the record's
  completion (section 3.2), which the layer knows because every end of a
  row is a Port event of the apparatus.

---

## 1. THE ROW AND THE RECORD

### 1.1 The amplitude on the row: (amount, phase, multiplicity), not (X, Y)

Chosen: the row keeps today's `amount` and `phase` and gains
`multiplicity` m (int64, 1 by default and when the key is off). The
amplitude of the row is

    z = amount / sqrt(m) x v(phase) / 256,   |z|^2 = amount^2 (C^2 + S^2) / (m 65536)

so the norm of a row is the exact rational `amount^2 / m` (times the
tables' 65536 +- 237, section 2.4). An `(X, Y)` pair on the row was
weighed and rejected for three reasons of exactness:

1. The flight turns the phase by `phase_per_link` steps per Link and the
   meeting by the crowd's register (note 35): on the circle of N that is an
   integer addition, exact and bit-identical to today. On a Cartesian pair
   it is a rotation by 2 pi / N, only through the rounded tables, a loss
   of `+- 237 / 65536` of the norm at EVERY Link: not admissible under the
   integer contract ("do not round"), and not byte-identical.
2. The split (section 2) multiplies the amount by an integer and the
   multiplicity by an integer: exact without any divisibility condition.
3. The record's `(X, Y)` the owner names is the pointer the click reads,
   `(X, Y) = sum_rows 32 amount v(phase)` over the rows of one record and
   one label at the set, the same first moment `coherent_pointer` forms
   today (note 33), an integer pair computed at the read and never stored.

The row under the key (the store's columns, all int64; the identity of the
merge gains the three):

| Column | Meaning | Bound | Key off |
| --- | --- | --- | --- |
| `record` | the birth's identity: the emitter's number x 2^32 + its self-creation count (local to the emitter; a re-emitter that births from a gathered record uses its own count) | < 2^62 | 0, not written |
| `branch` | the joint label of the row within its record (section 4): 0 .. L - 1 with L the record's label count, 2^n after n gates | < 2^62 (n <= 62) | 0, not written |
| `multiplicity` | m: the product of the norms of the splits the row's path passed (an equal k-way split x k, a rotation (a_i) x sum a_i^2, a label rotation x 65536) | <= 2^62 - 1, refused at the split that would exceed it, naming the Node | 1, not written |
| `amount` | the amplitude's magnitude in units of one ray; under the key a birth is amount 1 per row, a rotation multiplies it by its entry | as today (2^62 - 1, the label bound) | as today |
| `phase` | as today, the circle of N; a reflection adds N/4, a sign N/2 (exact on the tables) | 0 .. N - 1 | as today |
| `content` | as today, per unit: `h s` of the birth; a split's new rows carry it (the GameBoard's ledger over every branch, section 3.5) | as today | as today |
| `number` | as today (the last emitter) | as today | as today |

`u`, the birth phase, is the row's `phase` at birth (the lamp's clock), as
today; no fourth column: the layer reads u from the record's birth line
(section 5), never from a row. The state under the key is the free
Z-module on the basis `(node, direction, age, phase mod N/2, number,
content, record, branch, m)` with the identification `|p + N/2> = -|p>`:
the row multiset is its normal form (section 2.3).

### 1.2 The record (the layer's table per live record, host state)

| Field | Meaning | Where |
| --- | --- | --- |
| `u` | the birth phase, 0 .. N - 1 | the layer (from the birth line) |
| `T` | the birth norm: a report, 1 (one quantum) in units of 2^26 x 65536 | the layer; not used by the ladder (section 3.2) |
| `C` | the offers so far, per (set, label): the accumulated pointer `(X, Y)` per (record, label, set), Python integers, and the weight `|X, Y|^2 / m` as a pair (numerator, denominator) | the layer |
| `live` | the count of the record's rows on the GameBoard: + (k - 1) at a k-way split, - 1 at every end (a click, a face, the border) | the layer, from the apparatus's Port events |
| `labels` | the joint labels present and, after the first click of a many-arm record, the residual amplitude per remaining label (integer pairs) | the layer |
| `gathered` | None, or (set, channel, tick) | the layer |

Storage per Node: three more int64 per hosted row, fixed. The rows per
Node: today's bound `len(D) x age_bound x N x numbers x contents` times
`L x R`, L the largest label set of the world (2^n after n gates) and R
the live records per number (at most `ticks` births of one lamp; a row
dies within `age_bound` of its last re-emission), a constant of the world
and the run. The layer's table is the host's: live records x (sets that
received rows) x labels integers, reported as host cost.

---

## 2. SPLIT AND MERGE AS INVERSES

### 2.1 The split as a table rule

A table entry `split` (a measured event's entry for a paid family under
the key, refused without it):

    "split": {"outputs": [{"direction": d_i, "weight": a_i, "turn": t_i}, ...]}

The arriving row `(w, m, p, record, branch)` is absorbed as a `rerelease`
absorbs (the GameBoard's click line, one-way for the row) and re-emitted
at the next self-creation as the rows `(w a_i, m x A, p + t_i, record,
branch)` on the directions `d_i`, `A = sum a_i^2`, age 0, the re-emitter's
number, the record and branch kept. Norm: `sum (w a_i)^2 / (m A) = w^2 / m`,
exact for ANY integer weights: an equal k-way split is `a_i = 1`, `A = k`;
a rotation by a Pythagorean pair is `(a, b)` with `A = c^2`; the balanced
splitter that no triple gives exactly is `(1, 1)` with `A = 2`. The
existing `rerelease` on k `directions` becomes, under the key, the equal
k-way split with the same rows born (amount 1 per direction, `apportion_whole`
unchanged) and `m x k`; a lamp's release on k directions under the key is
the birth of one record with k rows of amount 1, m = k, u the clock's
phase, `T = 1`; `rate` other than [1, 1] is refused under the key in this
version (r records with one u would make r identical paths; extension:
r records with u advanced by the clock's stride).

The two-input mixing of a beam splitter is NOT performed at the splitter:
each arriving row is split on its own and the rows on one output direction
stay separate rows (the same Node, direction, age and record; different
phases), summed where they are read (the click's pointer) or merged where
they become identical (2.3). This keeps every row an integer and is the
same physics: the offer at D1 of the rows `a z1` and `b z2` is `|a z1 + b
z2|^2` exactly as the mixed amplitude's square would be.

The reflection's quarter turn (`turn` N/4) is exact on the tables; the
quarter turn needs `4 | N`: the key is refused for N < 4.

### 2.2 The rotation of labels (a single-label gate, section 10)

A table entry `rotate: {"setting": s, "turn": t}` on a set: the rows of
the record at the set, per label pair (0, 1) of one qubit position, become
`(w C'[s], m 65536, p)` on label 0 and `(w S'[s], m 65536, p + t)` on
label 1 from label 0, `(w S'[s], m 65536, p + N/2)` and `(w C'[s], m 65536,
p + t)` from label 1: the matrix `U_s = [[C', S'], [-S', C']]` of the 2N
tables (`U_s^T U_s = (C'^2 + S'^2) I` exactly: the off-diagonal `C'S' - S'C'`
is 0 in integers). Not a click (invertible, `U_{-s}` on the same tables
after dividing the common 65536 in the normal form when the amounts allow;
the rows kept). The Bell counter's window under the key is this rotation
followed by the label click (section 4).

### 2.3 The merge and the normal form

Two rows equal in every identity field (`node, direction, age, phase,
number, content, record, branch, multiplicity`) merge by the sum of the
amounts: the interference in phase, a bijection as today. Under the key
only, two rows of ONE record and label equal in every field but a phase
difference of exactly N/2 cancel: the amounts subtract, the difference
stays at the larger's phase, an equal pair leaves nothing (the row
disappears there: the owner's point 4, "in a dark fringe the sum is zero").
Two rows with any other phase difference stay two rows: on the circle of N
their sum is not a row; the click's pointer sums them (the interference
read). Rows of different m are never merged (a common m is required at a
read: 2.5). Without the key no row carries `record > 0`, so nothing
cancels and every registered world is byte-identical (acceptance test 7).

### 2.4 The proof that split and merge are inverses (checked)

The transposed table on each output row, then the normal form, returns the
inputs. Two inputs `(1 at 5)` along +y and `(1 at 37)` along +x at a
splitter (20, 21, 29): forward 4 rows, backward 8 rows, the normal form
merges two pairs in phase and cancels two pairs in antiphase and returns
`(841, 1414562, 5)` on in1 and `(841, 1414562, 37)` on in2, the amplitude
`841 / sqrt(2 x 841^2) = 1 / sqrt 2` of the inputs, the phases exact; the
same for (3, 4, 5) and (119, 120, 169) and for `(3 at 0, 2 at 16)`
(`mz.txt`, "inverse ... True"). So the split is an isometry of the record's
module whose inverse is its transpose, and the interval with a split is a
bijection onto its image. The engine's `inverse_step` is refused with any
measured event on the GameBoard already (note 6); the proof is the
mathematical one the principle asks for, not a new engine path.

The collision table acts on rows as today: a row of amount 1 is a single
in its slot, a row of amount above 1 or two rows in a slot a crowd (a wall
the pattern never enters). A moved row takes its new direction with its
record, branch and multiplicity unchanged: a permutation of the rows'
directions, unitary on the record's amplitude vector when the record's
rows are alone in their (number, content) class, a bijection of the joint
state always; the free crowd of other records is untouched (a free family
never carries a record). In no acceptance world does a collision act (the
splitters and counters are measured events, where no collision acts, note 18;
the fans are spectators).

### 2.5 Where the total norm is not conserved on the lattice, and the rule

Three sources, all measured:

1. The tables: `sum of the offers` of the Mach-Zehnder is 1.000000,
   1.001808 or 0.999893 depending on the arm's phase (`mz.txt`), the
   +- 237 / 65536 of the tables per row.
2. Paths of one record that meet again at a set NOT through a unitary
   recombination: the shipped two-slit world sends 88 of the 182 rows
   re-emitted at the openings into the wall Nodes beside the openings
   (the Bresenham line of a steep direction steps in y first), many at
   one Node in one interval and in phase, whose coherent sum is `k^2 / 455`
   where the paths' norm was `k / 455`: the record offers 5.10 where its
   norm is 1 (`slits.txt`). A split into k directions that re-meet is not
   unitary on the lattice; QM has the same non-unitarity when paths are
   forced to one point.
3. Rows of one record meeting at one set at different intervals: no merge
   on the lattice, two arrivals in the set's accumulated sum (3.2), which
   is the coherent reading and needs no normalisation.

The rule chosen: **the ladder is normalised at the record's completion by
the sum of the record's offers, `Total = sum over (set, label) of
|X, Y|^2 / m`, not by T fixed at birth.** Then exactly one click per
completed record (the last rung is N by construction, 3.3), no loss, no
double click, and Born on the lattice's own weights. T at birth was
checked as the alternative: on the Mach-Zehnder it gives the same counts
at every arm phase (0 of 64 phases differ, `mz.txt`) because the
deviation is under 1/N; on the two-slit world it would leave 80 % of the
births without a click or with the cell of the first over-weighted offer,
and at N >= 256 a one-row record at a phase where the tables read 65242
would fail to click for the top u. T stays on the record as a report; the
`gather` line carries `total` and `T` so the deviation is read per record.

---

## 3. THE CLICK

### 3.1 The offer: the sum of one record's rows at the set, accumulated

At a set with `reading: "sum"`, the rows of a record and a label that the
threshold and the rule admit are absorbed as today (the GameBoard's click:
the amount, the content and the label join the measured event at the Node
the row reached; the `click` line per row; the crowd's `wave` threshold
over all numbers stays the set's gate). Then, under the key, the layer adds
the rows' pointer to the record's accumulated pointer at that set and
label:

    X += sum 32 w C[(p + f(age, tick)) mod N],  Y += sum 32 w S[...]

with `f(age, tick) = floor(tick n / d) - floor((tick - age) n / d)` the
family's `frequency` [n, d] (a new family key under the key: the phase
steps per interval of age the external thing adds at the read, the lamp's
own turn `[content, K]` by default) read whole by the measured event as the
age is (note 25). Rows of one record arriving at one Node at different
intervals therefore interfere with the phase difference `f x (difference
of flight times)`: the Euclidean path difference through the flight table,
which is the registered A1 correlation (0.969 with the Euclidean cosine
for the crowd). The pilot's reading (T4) summed per interval, where rows
of different path lengths never coincide; this is the owner's note (i).
The weight of the (set, label) is `(X^2 + Y^2) / m`, exact; the rows at a
set must share m, refused otherwise naming the record and the set (no
acceptance world violates it: every path of the two-slit record has
m = 5 x 91 = 455, of the Mach-Zehnder 2 x 841).

`pointer_units` per record: the same function on the record's `(X, Y)`;
the crowd's `pointer_units` over all numbers is untouched.

### 3.2 When the record is read: at its completion

The layer's `live` count reaches 0 when every row of the record has ended
(a click at a set, an open face, the border `lifetime`; a split reports
`+ (k - 1)`; the birth `+ k`). Every one of these is an event of the
apparatus (a measured event, a face, the border, a lamp) and reaches the
layer through the apparatus's Link Port (principle 5): no row on the
GameBoard is read at a distance, and the lattice's law never reads the
layer. A record with rows parked at rest by a collision or on a periodic
axis without a lifetime never completes; the run's end reports it `open`
with its offers, and `age_bound` bounds the wait on an open GameBoard.

### 3.3 The ladder: the rungs at the nearest integer

The record's offers in the layer's order (the sets in declaration order:
the measured events by number, then the declared detectors, then the faces
in Port order and the border; within a set the labels ascending; the order
is a declared tie, section 6 of BEAM_LAW's kind) with the cumulative
weights `C_1 <= ... <= C_K = Total`. The rungs

    b_k = (2 N C_k + Total) // (2 Total)      (b_0 = 0, b_K = N)

and the click is the k with `b_{k-1} <= u < b_k`. Every u falls in exactly
one cell; an offer below `Total / 2N` may get an empty cell (never chosen).
This is Born with the count per cell the nearest integer to `N x weight /
Total`. Why the nearest and not the strict crossing (`N C_k > u Total`):
with the strict rule the second party's marginal of a pair reads 33/64 in
3944 of the 4096 setting pairs (`bell.py` before the change), a signalling
of 1/64 made by the rounding; with the rungs at the nearest integer both
marginals are 32/64 in all 4096 pairs (`bell.txt`), by the mirror symmetry
of the pair's weights (`W(o_A, o_B) = W(-o_A, -o_B)`) and the identity
`floor(N/2 - x + 1/2) = N/2 - floor(x + 1/2)` off a tie. The gather: the
world's row is written for the chosen (set, label): the record's one
quantum (`h s`) is the world's content at that set; the tick of the row is
the completion tick, with the last arrival's tick beside it.

### 3.4 The Mach-Zehnder of the issue, in integers (`mz.txt`)

The 5 x 5 world: the source at (0, 0) births one record of two rows of
amount 1, m = 2 (norm 1, the issue's "(+x, 5), (+y, 5), norm 50" scaled to
one quantum), the +y row with the reflection's quarter turn; mirrors at
(3, 0) and (0, 3) (`rerelease` on one direction, no change of amplitude);
the splitter at (3, 3) a `split` entry with the pair (20, 21) (`A = 841`,
the shares 400/841 = 0.4756 and 441/841: no triple is balanced; (119, 120,
169) is within 0.4 % and costs `m x 28561`); D1 at (4, 3), D2 at (3, 4),
one set each, `reading: "sum"`.

| Case | Offer D1 | Offer D2 | Total | Clicks over 64 births (u = 0 .. 63) |
| --- | --- | --- | --- | --- |
| equal arms | 1681/1682 | 1/1682 | 1 | D1 64, D2 0 |
| half turn on arm 2 | 1/1682 | 1681/1682 | 1 | D1 0, D2 64 |
| quarter turn | 1/2 | 1/2 | 1 | D1 32, D2 32 |
| arm 2 longer by two intervals, `frequency` 0 | 1681/1682 | 1/1682 | 1 | D1 64 (the rows accumulate in phase) |
| the same at `frequency` 8 steps per interval | 1/2 | 1/2 | 1 | D1 32, D2 32 |
| the same at `frequency` 16 | 1/1682 | 1681/1682 | 1 | D2 64 |
| the same read per interval, no accumulation (the prototype's reading) | 441/1682, 400/1682 at t; 400/1682, 441/1682 at t + 2 | | 1 | D1 17 + 15, D2 15 + 17, one click per birth at two ticks |
| with (3, 4, 5) instead: equal arms | 49/50 | 1/50 | 1 | D1 63, D2 1 |
| Elitzur-Vaidman, arm 2 absorbed (20, 21, 29) | 441/1682 | 400/1682 | 1 with the absorber's 1/2 | absorber 32, D1 17, D2 15 (D2 the dark port of the unblocked device: 15/64 against the ideal 16) |
| the same with (119, 120, 169) | 7200/28561 | 14161/57122 | 1 | absorber 32, D1 16, D2 16 |

The prototype's unequal-arm table (32 / 32 at ticks 6 and 8) is the
per-interval reading; under the accumulation the unequal arms read the
wavelength, as an interferometer does (a delay of two intervals at 8 steps
per interval is a quarter turn: 32 / 32 by coincidence of the numbers).
The issue's "5 + 5 = 10 toward D1, 5 - 5 = 0 toward D2" is a Hadamard
without its 1 / sqrt 2 (norm 50 to 100) and is replaced by the exact pair.

### 3.5 The books

Two ledgers. The GameBoard's over every row, as today, with two report
lines under the key: `split` per family (the amount and content the
splits created, `sum (a_i - 1) w` per split; zero without the key) and
`cancelled` (what the normal form removed), so `released + split =
current + escaped + absorbed + cancelled` holds at every interval; the
momentum lines as today over the rows' labels (a split's rows carry
`w a_i x h s x u_d`, the splitter's recoil the difference: a report as the
free push is). The world's over the path: per record one quantum in, one
gather out (content `h s`, the momentum a report: the share-weighted mean
`h s Q sum_r w_r^2 u_{d_r} / sum_r w_r^2` over the gathered set's rows);
`in = gathered + open` at the end of the run.

---

## 4. THE PAIR (form A, the owner's decision; form B in section 11 for the record)

### 4.1 One mechanism: the pair is the single quantum with labels

A lamp under the key declares `branches`: the joint labels of a birth,
`[[label, weight], ...]` with weights integers (the Bell pair
`[[0, 1], [1, 1]]`: two combinations of two labels, amplitude 1 each, the
norm 2; the norm is the rows' `m`: each arm's rows are `(1, 2, u)` on
labels 0 and 1) and `arms`: the count of directions that are separate
quanta (2 for a pair, 3 for GHZ; 1 by default: k directions are k paths of
one quantum). The A2 worlds carry no `branches`, so under the key they are
one quantum on two arms (a which-way world); the Bell acceptance world is
the A2 file plus `amplitude: true`, `arms: 2`, `branches` and
`reading: "sum"` on the counters; without the key the same file reads the
window gate, byte-identical.

The counter's `phase_window: s` under the key is the rotation `U_s`
(2.2) followed by the label click: the rows of label 0 and 1 at the set
become the residual amplitudes per channel, `+`: `(C'[s], S'[s])` on
(label 0, label 1), `-`: `(-S'[s], C'[s])`; the record's other rows (on
the other arm) are not summed with these: rows of different labels are
never summed coherently while their partners are open (the label is a
combination, not a path). The `phase_window: {reads, offset}` form (#363)
gives `s` from the chooser's pointer as today; both forms read the window
gate without the key.

### 4.2 The first click's marginal is 1/2 exactly, for every setting

The layer's joint weight of the outcomes `(o_A, o_B)` is `J^2` with
`J = sum_label U_a[o_A][label] U_b[o_B][label]`, an integer in 1/256^2.
Because `U_b^T U_b = n_b I` exactly on the tables, `sum_{o_B} J(o_A, o_B)^2
= n_a n_b` for both `o_A`: the cumulative of A's half is exactly
`Total / 2` and the rung `b = (2 N (Total/2) + Total) // (2 Total) = N/2`
for every (a, b): A's outcome is `+` for `u < 32` and `-` for `u >= 32`
(`bell.txt`, "for every (a, b): True"). B's marginal is 32/64 in all 4096
pairs by the mirror symmetry (3.3). No-signalling exact in the counts, for
every setting, at N = 64.

The first click (in the layer's order) chooses its channel by u on the
coarse rungs; the other arm's rows keep flying; at their set the second
click reads the record (the layer: A's channel), sums coherently what
remains, `J(o_A, o_B)` for the two `o_B`, and chooses on the fine rungs
within A's cell with the same u. A which-path click on an arm (a `measure`
or `read` entry on a branched record: the labels are its channels, the
rows of each label its offer, weights 1/2 and 1/2 here) removes the other
labels' combinations; the counters then read a product (4.4).

### 4.3 The joint counts at N = 64, 256, 1024, and Tsirelson (`bell.txt`)

The CHSH settings of A2, (0, 8), (0, 24), (16, 8), (16, 24), are on the
grid: the counts per cell over the 64 birth phases, the weights in 1/256^4:

| (a, b) | W(++) | W(+-) | counts ++ +- -+ -- | E | C_64[a - b] / 256 |
| --- | --- | --- | --- | --- | --- |
| (0, 8) | 15810167966860836864 | 2703285676329140224 | 27 5 5 27 | 44/64 = +0.6875 | +0.7070 |
| (0, 24) | 2703285676329140224 | 15810167966860836864 | 5 27 27 5 | -44/64 | -0.7070 |
| (16, 8) | 15790890611743129600 | 2718608131071410176 | 27 5 5 27 | +44/64 | +0.7070 |
| (16, 24) | 15790890611743129600 | 2718608131071410176 | 27 5 5 27 | +44/64 | +0.7070 |

    S(N = 64) = 176/64 = 2.75000;  S(256) = 720/256 = 2.81250;  S(1024) = 2896/1024 = 2.82812;  2 sqrt 2 = 2.82843.

At or below Tsirelson at every N with the rungs at the nearest integer.
The other session's 2.875 is the strict crossing's rounding (every E at
46/64, computed here too before the change: `S = 184/64`), which also
broke the marginals; it is neither a prediction nor a defect of the tables
(the exact cosine's cells give the same 184/64 and 176/64: the cells, not
the tables, round). What the discreteness predicts: `|E - cos| <= 1/N`
per E (measured at most 0.0352 at N = 64 over all 4096 pairs), so `S = 2
sqrt 2 - epsilon(N)` with epsilon at most 4/N, converging from below with
the nearest rungs; the tables' own rounding moves E by at most 2 x 237 /
65536 = 0.007. The choosers' settings (0, 12, 25, 38, 51 / 8, 29, 51):
E x 64 = 44, -60, 20, 60, -8, -48, -8, 60, -52, -64, 40, 20, -28, -36, 64;
on the registered quadruple (0, 25) x (8, 29): `156/64 = 2.4375` (was 2
under the window gate); the largest S over the ordered quadruples
`172/64 = 2.6875` on (12, 0) x (8, 51).

Why S = 2 today and 2.83 under the key, in one paragraph: the window gate
reads each ray's own phase against the setting and clicks or passes, so
each outcome is `f(u, a)` and `g(u, b)` and the record sums the SQUARES
of the two arms' readings, one per pair: Bell's bound, the triangle `1 -
4k/N` (#363, S = 2 exactly). Under the key the click reads the SUM over
the labels of the products of the two arms' rotation entries and squares
it: the cross term `2 C'_a S'_a C'_b S'_b` between the labels is what the
square of a sum has and the sum of the squares has not; on the grid the
CHSH labels 0, 8, 16, 24 give `C_64[8] = 181` and the integer S of the
moment table's cells is 176/64. No cosine is computed at run time: the
entries are table reads, the products and sums integers.

### 4.4 The which-path world

A `measure` (label channels) on arm A before Alice's counter: the joint
is a product; at the CHSH settings `E x 64 = 44, -44, 0, 0`, `S = 88/64 =
1.375` (`bell.txt`); the largest S over all settings of a product is 2.
"S falls to 2" means Bell's bound; at these settings the value is 1.375.

### 4.5 GHZ

Three arms, labels 000 and 111 (weights 1, 1), settings X = (s N/4, turn
0) and Y = (s N/4, turn N/4) at each counter: the joint weights over the
8 outcome triples are exactly 0 on four and equal (39588699237876835586664300544
in 1/256^12) on four (`bell.txt`); the product of the outcomes is +1 on
every allowed triple of XXX and -1 on every allowed triple of XYY, YXY,
YYX: the deterministic contradiction with any local assignment (which
would need the product of the three products, +1, to equal the XXX
product... the four constraints multiply to -1 = +1). YYY has all eight
outcomes allowed. The zeros are exact because the same table entries
enter with opposite signs (181 x 181 x 181 both ways).

---

## 5. THE LAYER

The layer is the apparatus's: one object of the frame (`engine.py`, a
module `events/amplitude.py` owning nothing of the lattice), built once
from the world's `detectors`, the measured events outside them, the faces,
the border and the lamps and splitters (the apparatus), each with a Link
Port to it: `ports` in `run.json` lists them. It holds the table per live
record of section 1.2 and nothing per Node. Its operations, each at an
apparatus event of the interval, after `nature_beam` has run the GameBoard's
step 4 (the lattice never waits for the layer):

| Event | The layer |
| --- | --- |
| birth (a lamp's self-creation) | a new record: u, T, live = k, labels |
| split | live += k - 1 |
| click of rows at a set (per record, label) | if `gathered`: drop (the rows were absorbed on the GameBoard as every branch is; the world ignores them: lazy deletion, no message); else accumulate `(X, Y)`; live -= rows |
| face, border | as a set: an offer; live -= rows |
| live = 0 | the ladder (3.3): the world's row; for a many-arm record the coarse and fine rungs in the arms' order; `gathered` set |
| gate (section 10) | the union of two records' tables under the surviving number |

The `gather` line of `events.jsonl` and `run.json`'s `world` list: `(tick,
arrived, node or the set, detector, family, record, u, channel, weight,
total, T, before, after)` with `before`/`after` the count of combinations
(labels x offers) before and after: the click's size (the owner's
operational definition: a click is the operation that removes combinations
and adds one row to the list; the birth adds combinations; flight,
collision, meeting, split, merge and rotation are invertible and remove
none). By this definition a `read` entry that distinguishes labels is a
click without absorption, a window that passes is not, one that absorbs is.

Cost: per click one segmented sum per (record, label) more than today
(the rows are already grouped by (event, number); the group by record is
one more key of the same sort), Python integers for the accumulation
(exact, a report never refused); per completion `K` rung divisions. The
click generators' table of section 8 makes the pair's completion a lookup.

The offline reading: `tools/amplitude_path.py` rebuilds the world's list
from `events.jsonl` (the birth lines, the `click` lines per record and
label with their phases and ages, the faces) by the same accumulation and
the same rungs (the functions imported from `events/amplitude.py` by path,
as `bell_choosers.py` does), and asserts equality with the run's `world`
list: proven equal because both read the same lines in the same declared
order with the same integers. The reading form of comment 6 is this tool.

---

## 6. WHAT STAYS BYTE-IDENTICAL

- Free families never branch: no `split`, `branches` or `sum` is accepted
  on a free family (refused naming the key); gravity, electric, strong
  fields, every body, clock, orbit, nucleus, lens and Hubble reading are
  untouched with the key on or off.
- Without the key: `record = 0` on every row, the three columns not
  written, no cancel, no accumulation, no layer; the 85 registered worlds
  byte-identical in `events.jsonl`, `state.json` and `run.json` (`run.json`
  gains `amplitude: false` only, as `meeting` did): acceptance test 7.
- With the key, a one-row record reproduces today's law (proof): its
  birth is one row (amount 1, m = 1); its split is the `rerelease` it was
  (k rows of amount 1, m = k: the same rows, the multiplicity unread by
  the flight); its click at its first set is the only offer, `Total` = that
  offer, `b_1 = (2 N Total + Total) // (2 Total) = N`: every u clicks there,
  u unused; the GameBoard's click line is today's. The tables' rounding
  cannot move it (the normalisation by the total).
- A moving body struck by a branched paid row: the GameBoard's push reads
  the rows as today (`amount x content x u_d` per row, every branch: the
  GameBoard's ledger over every branch); the mean the owner names,
  `h s Q u_d x w^2 / (m Total)` per row, is a report of the reading tool.
  Stated as the limit: matter on the GameBoard feels every branch until
  the owner decides the push of a branch (section 9).
- The lineage at a re-release: a re-emitter that took the rows of a
  GATHERED record (the chosen set's rows: a re-emitter is a set that can
  be chosen) births a new record (a new u from its own clock, its own
  number and count, `live` from its rows) at its next self-creation; a
  re-emitter that took rows not chosen (the record gathered elsewhere, or
  not yet complete: the re-emission is a split, not a click) keeps the
  record and splits, and if the record is later gathered elsewhere its
  rows are dropped lazily at their next set. A re-emission never removes a
  combination: it is not a click.

---

## 7. THE ACCEPTANCE TESTS (written before any run; the integers above)

| Test | World | Expected, exact |
| --- | --- | --- |
| 1 Mach-Zehnder | 5 x 5, `split` (20, 21) at (3, 3), D1, D2 `sum` | equal arms D1 64 / D2 0; half turn 0 / 64; quarter turn 32 / 32; unequal arms at `frequency` 8: 32 / 32 and at 0: 64 / 0; one gather per birth; Total 1 within +- 0.0019 |
| 2 Two slits at a low rate | the shipped 60 x 121 world with `in_transit` one birth (or a lamp at rate 1 with 64 births), `frequency` [8591334592, 2^30], the pixels `sum` | the single record's weights per pixel correlate 0.992 with the crowd's registered record (A10's form: "A10's record is already the offers' weights"), 0.753 with the incoherent sum, 0.38 with the Euclidean cosine (the sparse fan's spots); 61 pixels receive rows, 27 receive two paths; the 64-birth histogram over the screen alone correlates 0.963 with the weights; in the shipped geometry 61 of 64 births click the wall (88 fan rows step into the wall beside the openings, in phase, offering 4.85) and 3 the screen (pixels 40, 60, 81): the acceptance world must free the openings' neighbours (a world-file change; then the wall's share is 3/5 of the births and the screen's 2/5) |
| 3 Elitzur-Vaidman | test 1 with an absorber at (0, 3) | absorber 32, D1 17, D2 15 ((119, 120, 169): 32, 16, 16) |
| 4 A2 with the choosers | `read.json` plus the key, `arms: 2`, `branches [[0,1],[1,1]]`, `sum` | S = 156/64 on (0, 25) x (8, 29); every marginal 32/64; E per bin as listed in 4.3; the four written worlds at the CHSH labels S = 176/64 |
| 5 GHZ | three arms, X/Y settings | the four allowed triples per basis, products +1 (XXX) and -1 (XYY, YXY, YYX), every forbidden triple weight 0 |
| 6 Which-path | test 4 with `measure` on arm A before the counter | S = 88/64 at the CHSH labels; marginals 32/64; the single-quantum two-slit world with a `measure` at one opening: no fringe (the weights the incoherent sum) |
| 7 Byte-identity | the 85 registered worlds without the key | `events.jsonl`, `state.json` identical; `run.json` gains the key false |
| 8 Determinism | test 1 and test 2 twice with the same u | the same gather; a moved detector (D1 one Node farther) moves the rungs, the same u falls elsewhere where the weights changed |
| 9 No maintenance | test 4 with 200 idle intervals before the counters | S unchanged; with a `read` on one arm at any tick before the counter, S = 88/64 |
| 10 The register's replay | the reading tool on tests 1 to 6 | the tool's list equals `run.json`'s `world` |

---

## 8. THE DETECTORS AS CLICK GENERATORS (the owner's addition)

Tested and settled. (1) The pair's correlation is fixed at placement: the
rows' labels at each counter are the lattice's computation (the flight
table brings the record's rows at phase u to each set; the rotation's
entries are the table at the setting); nothing of it depends on the run
beyond u. (2) The layer records, once per detector pair at construction,
the integer table `W[a][b][o_A o_B] = J(a, b, o_A, o_B)^2` over the N x N
settings: `64 x 64 x 4 = 16384` integers, the largest below 2^65 (Python
integers; in 1/256^4), built through the moment table's entries (the
engine's only cosine) in `N^2 x (4 products + 2 sums + 4 squares)` integer
operations, 10^5 at N = 64, a host cost reported in `run.json`'s `layer`
beside the lattice's; it lives in the layer and the run's metadata, never
at a Node. The rows' arrival labels can be BUILT by running the lattice
from the birth to the counters headless, as the owner prefers, and the
result is the same table because the counters read the same `admit()`.
(3) The click is a lookup: the first click reads its window (the #363
form: the chooser's pointer gives `a`) and takes A's marginal rung, which
is N/2 for every entry of the table (4.2: Born, the pointer's square,
1/2); the second reads the same record, the row `W[a][b][o_A, .]` of the
table, and the fine rung within A's cell; u enters as the rung's position,
the same u for both, the normalisation the table's row sum: cos^2 and
no-signalling as in 4.3, the same integers as the run-time formula by
construction (it is the formula, tabulated). (4) The paragraph of 4.3.
(5) The one exception, as the owner asked: the table's placement, the
apparatus's, computed by the system's time at construction; everything
else within the system's laws. (6) Tests: 4, the marginals, 9, the
single-detector fringes (test 2) unchanged by the table's presence, 7.

---

## 9. THE DEAD ROW (the owner's third point)

After the first click of an entangled record, a row whose combinations
were all removed keeps flying. (1) Lazy deletion is the only local form:
at its next set it is absorbed as every branch is on the GameBoard, the
layer reads `gathered`, offers nothing, and the world ignores it; an
escape through a face or the border ends it the same way. Eager deletion
at a far Node would be a write at a distance and is out. (2) Meanwhile it
turns its phase, is counted in the crowd (a paid row is not a free crowd:
a body's push reads free rows; a `read` entry on the paid family reads its
label as the push, kappa = 1), meets the free crowd (meeting-v1 turns the
paid unit toward the crowd; the free units are untouched, note 35: the
mass's event is not turned by the meeting, it is pushed only by the rows
that reach its Node), and pushes or is absorbed where it reaches a body.
This is not new: today for a single photon beside a mass every row of the
birth turns and, reaching the mass, is absorbed there (122 of the beam in
`mass`, note 35 (ix)), and under the key only one row is the world's;
conservation is the GameBoard's books over every row, not the list. The
difference under entanglement is the lifetime of the dead row, bounded by
`age_bound` after its last re-emission. (3) The size of the dead action
per row: at a `read` entry the push `content x amount x Q u_d` per read
(Q = 64 per unit of weight along the row's direction), at a `measure` its
content and label once; per meeting 0 on the crowd and one grain step of
its own direction per N crowd units met (the `turned` line, a report).
Registered as the limit: the GameBoard's matter feels the sum over the
branches (a mean field). The alternative for the owner: a branched row in
flight reads (turns) but gives no push and joins no content until its
record's gather, its momentum given at the click alone; it would make the
push of a paid family on a body depend on the layer (a read at a distance
at the body: out by the owner's rule) or defer every paid push to the
gather (series K's 122 absorbed rays would push nothing; the meeting's
turned line unchanged). Recommended: (1) + (2) with the limit stated.

---

## 10. THE GATE BETWEEN TWO RECORDS (CNOT), AND THE CIRCUIT'S NAMES

A table entry on a measured event (or a Node's `meeting` key) under the
key:

    "gate": {"kind": "cnot", "control": "<family or record label rule>", "target": ..., "hold": true}

The meeting of the rows of two records at the entry's Node permutes their
joint labels: the rows of both records present together are relabelled by
`(l_c, l_t) -> (l_c, l_t xor l_c)`; the record with the lower `record`
survives, the other's rows at the Node take its number and the layer maps
the other's id to it (`joined` in the record's table) so that its rows
elsewhere are read as the same record lazily; the joint label set becomes
the product of the two label sets (each record's rows now carry a joint
label, the target's one row of label 0 becoming two rows (0, 0) and
(1, 1) for a control in `|+>`). `hold: true`: the entry holds the first
record's rows as a re-emitter holds what came home (`pending`, the owed
count), acts when the other's arrive, re-emits both on their `directions`;
`false`: acts only on rows present together, the rest pass. The gate is
invertible (CNOT is its own inverse; the joint state a permutation) and
removes no combination: not a click. Rows whose combination reaches zero
weight by a merge that cancels are deleted on the lattice by the normal
form (2.3); a row of amount 0 never exists.

The single-label gates the engine has, named for a circuit: `split` with
`(1, 1)` and the turn N/4 on the second output is the Hadamard on a PATH
qubit (the two directions the labels); `rotate {setting: N/4}` is the
Hadamard on a LABEL qubit (up to the sign convention: H|0> = (|0> - |1>)/sqrt 2
here); `turn {label: l, steps: t}` the phase on one label; the flight's
`phase_per_link` and a path length the phase on a path.

Checked (`gate.txt`): CNOT on `H|0> x |0>` gives `{(0,0): +, (1,1): -}`,
the pair `|00> - |11>` (Bob reads at -b: S = 176/64 at the CHSH labels, the
same as 4.3); CNOT twice is the identity (every row back); GHZ by two
CNOTs from `H|0>|0>|0>` gives `{000, 111}` and the XXX / XYY / YXY / YYX
products -1 / +1 / +1 / +1 (the sign of this convention's H; the
contradiction the same); Grover on two labels (H H, the oracle a half
turn on the marked label, H H, a half turn on 00, H H): the marked
label's weight is the whole total and the click is the marked row for
every u, for each of the four marks. Rows born: `n x 2^n` per record
after n gates (n = 20: 20971520 rows) times the paths per record: the
ceiling of principle 9 as a store bound.

The register's ceiling, measured: the multiplicity grows per pass on one
path by k (an equal k-way split), `c^2` (a rotation pair), 65536 (a label
rotation); within 2^62 a path takes 9 passes of the 91-fan, 13 of (3, 4,
5), 6 of (20, 21, 29), 4 of (119, 120, 169), 3 label rotations, 62
balanced (1, 1) splits. Grover's six rotations exceed the register on the
lattice (m = 2^192): exact on the host's integers, not on a Node. This is
the concrete form of the two sentences of principle 9: the GameBoard as a
finite host predicts a ceiling (a circuit deeper than the register's exact
depth cannot run on the lattice exactly; wider than the store's bound
cannot be held); the GameBoard as a description does not (Python integers
carry Grover's 10^77).

---

## 11. FORM B, kept short (not built; the all-local alternative)

The click as a row: a counter's click births 2L click rows of a free
family `click` (phase circle, no columns, `pass` everywhere) toward the
coincidence unit, each carrying the record's number, `branch` = (outcome,
label, sign) packed, `amount = |U_s[o][label]|`, `phase = u`; the unit
(a measured event with the rule `compare`, holding by number as a body
holds, a declared capacity) resolves when `count` parties' rows of one
number are held: the tuple weights `|sum_label prod_parties amount x
sign|^2`, the same integers as form A on 21 x 13 setting pairs
(`bell.txt`), the choice by the rows' phase u on the rungs of 3.3, the
world's row written there. The coordinator's sketch is corrected on one
point: the labels cannot be encoded as phase offsets of the rows (`u +
sigma l N/2L`) with the moments multiplied at the unit, because a product
of single-row phases is a product state (S <= 2; the sum over labels of
`cos(u - a) cos(u - b)` depends on u); the click rows must carry the
rotation's entries per (outcome, label), 2L rows per click. Its cost:
one free family, one unit per pair, the click rows' flight; the same
integers; its limit: a label rule on the rows only (a general 2^n record
stays the host's, as recorded).

---

## 12. THE COST AND THE CEILING (principle 9)

Per row: three int64 columns. Per Node: today's rows times L x R. Per
click: one more grouping key and Python-integer sums. Per record: the
layer's table, `(sets received) x L` integer pairs, live until completion;
per detector pair the click-generators' table, 16384 integers at N = 64.
The lattice stays O(1) per Node for fixed L; the host pays L = 2^n and the
register bounds the exact depth (section 10). The two sentences: a finite
host predicts a ceiling for a quantum computer (the store's bound on rows,
the register's bound on exact multiplicity: named numbers above); a
description does not.

---

## 13. DEPARTURES FROM THE TEN PRINCIPLES, NAMED

1. Principle 2's "(X, Y) on the row": the row carries (amount, phase, m);
   (X, Y) is the record's pointer at the read. Reason: exactness of the
   flight (1.1).
2. Principle 3's "a meeting of identical rows sums them; that is the
   interference": rows identical in phase merge; rows in antiphase cancel
   (an addition under the key); rows of other phases interfere at the
   click's accumulated sum. Reason: a sum of two phases is not a row.
3. Principle 4's "the accumulation is crossed" in real time: the ladder is
   read at the record's completion, normalised by the sum of its offers.
   Reason: the accumulated `|Sigma|^2` at a Node falls when an antiphase
   row arrives later, so a crossing could be undone; and the lattice's sum
   of offers is not the birth norm (2.5). The click's tick is the
   completion's; a delay of the view, not of the physics (comment 6).
4. Principle 5 as read by the coordinator's sketch of the layer's lazy
   deletion: unchanged; the layer additionally counts live rows through
   the apparatus's Ports (the splitters and lamps are apparatus too).
5. The rungs at the nearest integer (3.3) in place of the strict crossing:
   required for exact marginals; it moves the Mach-Zehnder's (3, 4, 5)
   counts by nothing and the pair's S from 2.875 to 2.75 at N = 64.

---

## 14. THE VERDICT IN FIVE LINES

1. Admissible under the law and the integer contract: every operation on
   the lattice is an integer table on the row's own fields, bounded before
   it is formed (m refused at the split), local, a bijection up to the
   click; the non-local read is the apparatus's layer, at the one-way
   place, never a Node's; the sum the click reads is over one record.
2. Blocking issues before code: none in the law; two in the worlds: the
   shipped two-slit geometry's fans step into the wall (test 2's world
   must change), and no Pythagorean pair is balanced (the Mach-Zehnder
   uses (20, 21) with 64 / 0 at N = 64, or the `(1, 1)` split with `m x 2`,
   exact and balanced, which the design admits: prefer it for the
   acceptance world and keep the pairs for declared unequal splitters).
3. The order of implementation: (i) the three columns, the key's refusals
   and the byte-identity of the 85 worlds (one commit, no behaviour); (ii)
   `split`, the normal form's cancel and `frequency` with tests 1, 3, 8;
   (iii) the layer, `reading: "sum"`, the ladder, the `gather` line and
   the reading tool with tests 2, 7, 10; (iv) `branches`, `arms`, the
   rotation at the window and the label click with tests 4, 5, 6, 9; (v)
   the gate with section 10's tests; the click generators' table with
   (iv) as its lookup form.
4. What the owner must decide before code: (a) the ladder at completion
   with the total's normalisation (departure 3) or the strict real-time
   crossing against the birth norm with its stated losses; (b) the
   frequency key as the family's (recommended) or the lamp's turn read
   from the record; (c) the branched row's push on matter, the mean or
   the sum over branches (recommended: the sum, the limit stated,
   section 9); (d) the `(1, 1)` balanced split beside the Pythagorean
   pairs (recommended: both).
5. The claim this design lets the model make: under the key the
   registered lattice is unchanged and the world's list of clicks reads
   Born, cos^2(a - b) with exact marginals, GHZ and Grover from the
   engine's own tables, with S below Tsirelson at every N and the
   register's exact depth as the ceiling; the sentence "on the GameBoard
   every path, in the world one" holds with the stated departures.
