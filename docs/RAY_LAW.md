# The law of the ray (`rays-v1`)

The published design and implementation contract of the law of the ray, the
model owner's decision of 2026-09-19 ([Highlights 5.4](HIGHLIGHTS.md#54-the-detector),
"DECIDED: the law of the ray"): the Node holds no wave. No coherent sum, no
shares, no placement, no tie order, no scatter. A unit is a ray with a record
and moves along the digital line of its momentum at one speed for every
direction, a bijection; rays that meet at a Node are permuted by the seven-slot
collision table, a bijection; the wave is a reading of a crowd of rays at a
detector and lives nowhere else; the click is the only one-way border. The
design is published here before the engine changes (the
[published-design requirement](../skills/workflow.md#implement-from-a-published-design));
the implementation cites this file and its commit. Inputs: the three
prototypes (`rays`, `rays2`, `reversible`) and the mathematician's review
(the 2 + 3 + 2 decomposition, the 20 orbits, theorems T1 to T4), all of
2026-09-19, recorded in Highlights 5.4. This document assumes the two changes
landing on the same base and does not re-specify them: one reading set for
every coupling (presence, push and threshold read everything at the Node but
the reader's own number, "here" included; `tests/test_one_reading_set.py`),
and no merge on a step, an open face as a detector, the owed count read off
the clock ([the engine](ENGINE.md)).

**The owner's name.** The ray's law is ONE generic function. The record is the
dataclass `NatureBeam`; the law is the single function `nature_beam(...)`, which
performs a Node's whole interval for the rays present. No other function holds
a piece of the ray's law; helpers exist only as pure tables that `nature_beam`
reads (the flight table, the collision table). The repository's rule that a
name states a component's responsibility (AGENTS.md) yields to the owner's
explicit name for this one component; this exception is recorded here and in
Highlights 5.4, and applies to nothing else.

## 1. Identity

- **Model identity** `rays-v1`. A world selects it with `"law": "rays"`; the
  record (`run.json`) carries `"law": "rays-v1"`. `configuration_validation`
  reports the kind `rays`.
- **`events-v1` is deleted** (the owner's rule, one engine). `"law": "events"`
  is refused naming the law of the ray and pointing to MIGRATION. The engine
  package `src/event_universe/events/` keeps its name (the board's things are
  still events: a ray is an event in transit); `mixing.py` and `reversible.py`
  go, `transit.py` is replaced, `engine.py` and `world.py` are rewritten in
  place. Tests and examples that go: section 6.
- **`reversible-detector-v1` (#344) is absorbed and deleted** as a separate
  `dynamics`: its pointer is the detector's record of section 5 (the coherent
  vector per interval is the pointer, its square the record); its `transduce`
  and `port_map` are the re-emission on declared directions (`rerelease` with
  `directions`), a bijection on (direction, phase) as `transduce` was on
  (Port, pointer); its refusal of an open face becomes "an open face is a
  detector". The `dynamics` key, `_validate_reversible_world`,
  `_reversible_*` in `engine.py`, `reversible.py`, `tests/test_reversible_detector*.py`
  and the contract section of DETECTOR_REQUIREMENTS.md are deleted, the
  requirements section kept.

## 2. The record of a ray and the world file

`NatureBeam` (one record; the board's state is a multiset of them; identical
records at one Node are one record with the amounts and contents added, which
is a bijection since identical units are interchangeable):

| Field | Meaning | Bound |
| --- | --- | --- |
| `node` | the Node (three integers, in `shape`) | 0 .. 4095 per axis |
| `direction` | index into the world's direction table `D`; entries 0 and 1 are the two rest vectors (0, 0, 0) ("here a", "here b"), 2 .. 7 the six headings in Port order, 8 .. the declared further directions, each a primitive integer vector with every component in -P .. P | 0 .. len(D) - 1 |
| `age` | the flight phase, the remainder's owner of the digital line, reduced modulo the direction's period `L_d` (section 3); `age` 0 at birth | 0 .. L_d - 1 |
| `phase` | a step of the circle of N, stamped by the emitter's clock at birth, turned by the family's `phase_per_link` steps at every Link crossed | 0 .. N - 1 |
| `number` | the last emitter (a measured event's number) | as today |
| `amount` | whole units | 1 .. 2^62 - 1 (`AMOUNT_BOUND`) |
| `content` | the content one unit carries (`quantum` x s at birth for a paid family, 0 for a free one) | 0 .. 2^62 - 1 |
| `charge` | on a free family's ray, the charge q_B of its emitter at birth: the emitter's factor of the electric push, carried on the record from birth (section 10, note 20); 0 on a paid family's ray | a charge |
| `mass` | on a free family's ray, the content M_B of its emitter at birth: the held content of the family that the release rate read at that self-creation (equal to the declared amount on every registered world, whose free measured events hold what they declared); 0 on a paid family's ray, whose factor is its `content` | 0 .. 2^62 - 1 |
| `family` | the family index (one store per family, so implicit in the store) | |

The momentum vector of a ray is not stored: it is its **label**,
`content x u_d` per unit for a paid family and `amount x u_d` for a free
one, with `u_d` the **unit vector of the direction at the flight table's
scale**: the integer vector nearest `Q D[direction] / |D[direction]|`,
Q = 64, one world constant per direction computed once in the direction
table (`nature_beam.unit_label`, the flight table's `labels`) by the exact
integer rule `k(|a|) = (isqrt((2 Q |a|)^2 // |D|^2) + 1) // 2` per
component with the sign restored (the model owner's decision of
2026-09-19 on the physics-rule reviewer's verdict, "go for it"; section
10, note 23). On a heading `u_d = Q e_d` exactly; on any direction
`|u_d| = Q` within `sqrt 3 / (2 Q)` = 1.35 % and `u_d` is parallel to D
within 0.78 degrees; `u_{-D} = -u_D` exactly and `u_{gD} = g u_D` for the
48 signed axis permutations; no exact tie exists for a direction bound
below 147. So every unit of a ray carries one momentum of length Q per
unit of its weight, direction-blind, and every momentum of the record (a
declared `momentum`, a push, a recoil, the books' lines) is in these
label units, Q per unit of amount along a heading. (A free unit carries
no content and its label is the unit along `u_d`; until the night of
2026-09-19 the free family's `quantum` was forced to 1 and multiplied
here, section 10, note 15; until 2026-09-19 the label was along the
integer direction D itself and its magnitude grew with |D|, note 21.)
Since the night of 2026-09-19 the label is the ONE momentum of the law
(`nature_beam.momentum_labels`; section 10, note 18): what the push reads
(the label moment, section 3 step 4), what a click moves onto the
detector, what a face click books, what a re-emitter or a home takes in
and gives back, what the transit line of the books sums; no momentum is
read off a Port anywhere.
The bound check `MOMENTUM_BOUND` (2^62 - 1) applies to every component, so
`Q x content x amount` must fit (content x amount below 2^56 per row); the
parser refuses a world whose declared `in_transit`, lamp rate or free
release could exceed it, naming the numbers (risk, section 9), and every
label the law forms (a birth, a re-emission, a home, a face click, the
recount) is checked per row BEFORE the product is formed, the weight times
the largest component of the row's `u_d` within the bound
(`momentum_labels`, `label_overflow_rows`; since 2026-09-20, note 25: a
merged row can outgrow the parser's bound, and until then the born
labels' product was checked after it was formed, so a wrap inside the
bound passed silently); the refusal names the Node and the amount.

World-file keys added: `"law": "rays"`; `directions` (optional, at the world:
a list of integer vectors beyond the six headings that any lamp or re-emitter
may name; the table `D` is the two rest vectors, the six headings and these,
in that order; each primitive with components in -P .. P, P = `direction_bound`,
64 by default, at most 4096 entries); per family `phase_per_link` (an integer
0 .. N - 1, 0 by default: the phase steps a ray turns per Link crossed);
per measured event `directions` (a list of indices or vectors from the
world's table, replacing the lamp's `headings`: the directions a lamp releases
on and a `rerelease` entry re-emits on; the six headings by default);
`detectors[].record` is always written (no key). Keys removed and refused:
`headings` on a lamp, `dynamics`, `port_map`, `output`, `capacity`, the
`phase` false branch's mixing semantics (`"phase": false` stays as "never
turns, phase 0, no window"), and, since the night of 2026-09-19 (the model
owner: "the tables are generated from the keys and a world declares only
what differs, `kind` derived from `quantum`"; section 10, note 15), `kind`
on a family: a family declares its `quantum` (required), h = 0 a free
family, h >= 1 a paid one, and the refusal names the derivation and
MIGRATION. Added on 2026-09-19 after the implementation: `width` (S, an integer from 1, 1 by default: the width of the push, the
step rule of section 3 step 5). Unchanged: `shape`, `boundary`, `ticks`, `K`, `N`, `release`,
`suspension`, `families`, `measured` (`table` with `read`, `measure`,
`rerelease`, `pass` and `phase_window`), `in_transit` (gains `direction`,
a vector, in place of `heading`; the six headings accepted as vectors),
`detectors` (`threshold`).

**The table generated from the keys** (the same decision). The table of a
measured event is one generic function of the families' keys,
`world.default_table(families)`: per family the rule the arrival's key
gives, `read` for a free family (h = 0: the push taken, the rays go on, the
record carrying the flow) and `measure` for a paid one (h >= 1: the click,
the record carrying the presence), no window. A world declares only the
entries that differ: a `phase_window`, a rule off the default (`rerelease`
for an opening or a mirror, `pass` for transparency, `read` on a paid
family, `measure` on a free one), a `reads` component; the object form of
an entry may omit `rule`, which is then the family's default, so a window
alone (`{"light": {"phase_window": 32}}`) is a lawful entry. An entry equal
to the default is accepted and changes nothing (the mathematician measured
that in every world of the repository no declared rule differed from the
key's; the forty declared entries were windows). The shipped worlds declare
only what differs (`tools/migrate_ray_worlds.py` rewrote them; the Bell and
coupling generators emit the trimmed form).

```json
{"law": "rays", "model_id": "two-slits-rays", "shape": [60, 121, 1],
 "boundary": {"z": "periodic"}, "ticks": 500, "K": 1024, "N": 64,
 "release": [1, 128], "suspension": 0,
 "directions": [[1, 1, 0], [1, -1, 0], [2, 1, 0], [2, -1, 0], [3, 1, 0], [3, -1, 0]],
 "families": [{"name": "light", "quantum": 1, "phase_per_link": 0}],
 "measured": [
  {"position": [2, 60, 0], "family": "light", "amount": 1000000, "fixed": true,
   "lamp": {"rate": [16, 1], "directions": [[1, 0, 0], [1, 1, 0], [1, -1, 0], [2, 1, 0], [2, -1, 0]]}},
  {"position": [8, 55, 0], "family": "light", "amount": 1, "fixed": true,
   "table": {"light": "rerelease"}, "directions": [[1, 0, 0], [2, 1, 0], [2, -1, 0], [3, 1, 0], [3, -1, 0]]},
  {"position": [8, 65, 0], "family": "light", "amount": 1, "fixed": true,
   "table": {"light": "rerelease"}, "directions": [[1, 0, 0], [2, 1, 0], [2, -1, 0], [3, 1, 0], [3, -1, 0]]}
 ],
 "detectors": [{"name": "screen", "positions": "x=52", "threshold": 1}]}
```

(The wall's Nodes are measured events with `measure`, the screen's a
detector as today; `"positions": "x=52"` stands for the list.)

## 3. The Node's interval: `nature_beam`

Module `src/event_universe/events/nature_beam.py`: the dataclass `NatureBeam`,
the one function

```
nature_beam(store: RayStore, world: RayWorld, tables: RayTables, measured: dict,
           tick: int, record: Record, inverse: bool = False) -> Books
```

and nothing else with law in it. `RayTables` holds the two pure tables,
computed once at load from the world's direction set and N: the flight table
and the collision table (section 4). `engine.py` keeps the interval's frame
(the tick, the books, the record, the measured events' clocks by `by_clock`,
the snapshot) and calls `nature_beam` once per interval; `transit.py`'s
per-Port arrays are replaced by the store.

**The store** (per family): a structure of arrays, one row per record,
`node` (int64, the flat index), `direction` (int16), `age` (int32), `phase`
(int16), `number` (int16), `amount` (int64), `content` (int64); rows sorted by
`node` at the start of every interval (`argsort`, stable), so a Node's rays
are one contiguous slice and every per-Node step is a segmented reduction
(`np.add.reduceat`, `bincount` on the segment ids). Identical rows (equal in
every field but `amount`, `content`) are merged after every interval by a
lexsort and a segmented sum. **Fixed local storage**: the distinct records at
one Node are bounded by `sum_d L_d x N x numbers x contents`, a constant of
the world (for the six headings with `phase_per_link` 0 and one content per
number: 6 x 55 x N x numbers); a crowd of identical units is one row. Fixed
local work: every per-Node step below is a bounded loop over that Node's
rows. The host cost is the total rows times about 0.1 to 1 us (section 9).

**The flight table** (one world constant, the owner's 1 / sqrt 3, "the phase
velocity the wave on the mesh had"): for a direction v = (a, b, c) with
S_1 = |a| + |b| + |c| and Q = 64, `T_d = isqrt(3 (a^2 + b^2 + c^2) Q^2)`; the
Manhattan steps made by age tau are `m(tau) = (2 tau S_1 Q + T_d) // (2 T_d)`
and the ray at age tau is at the m(tau)-th point of the Bresenham line of v
(`line_d`, S_1 unit steps per period, the axis furthest behind first, a fixed
integer table), `position(tau) = (m // S_1) v + line_d[0 .. m mod S_1]`. Since
`3 |v|^2 >= S_1^2` (Cauchy-Schwarz), `T_d >= S_1 Q` and `m(tau + 1) - m(tau)`
is 0 or 1: **at most one Link per interval in every direction, Euclidean
speed exactly 1 / sqrt 3 for every direction** (600 intervals put a ray at
distance^2 within 1.5 % of 600^2 / 3 for all 1730 primitive directions with
components up to 6; `scratchpad architect/ray_tables.py`). Why 1 / sqrt 3 and
not 1 / sqrt 2 on the plane: the flight table is a law of the ray, not of the
board; 1 / sqrt 3 is the largest speed at which no integer direction in
space ever crosses two Links in one interval ((1, 1, 1) is the bound), and a
plane world (extent 1 on z) uses the same table, so a wavelength is `period x
c` on every board. The step of the interval is `step_d(tau) = line_d[m(tau)
mod S_1]` if `m(tau + 1) > m(tau)`, else no move; the inverse is `tau - 1`
then the same step subtracted: bit-exact. The age is reduced modulo `L_d`,
the least period of the pair `(tau mod T_d / gcd(S_1 Q, T_d), m(tau) mod
S_1)`, so `(direction, age) -> (direction, age + 1 mod L_d)` is a bijection
and the store's bound above is finite (the heading (1, 0, 0): T 110, L 55;
(1, 1, 0): T 156, L 39; (1, 1, 1): T 192, L 3; (3, 1, 0): T 350, L 175). A
rest direction has S_1 = 0 and never moves.

**The interval**, in this order, each step a bijection on the board's state
except where marked as the border; the inverse runs the steps in reverse
order with each step's inverse:

1. **Departures become arrivals (the walk).** Every ray with `m(age + 1) >
   m(age)` is created at the neighbour along `step_d(age)` (the wrap on a
   periodic axis, `adjacent_node`), its age advanced (mod L_d) and its phase
   turned by `phase_per_link`; a ray that does not step this interval stays
   at its Node (its age still advances: the age is the flight phase, not a
   self-creation). A ray whose step leaves through an open face reaches the
   face detector (step 4). Inverse: age back one, the same step subtracted,
   the phase turned back. Rest rays (direction 0, 1) stay.
2. **The readings** (one reading set): presence per number per Node = the
   amount of every ray at the Node, rest and moving alike, and the measured
   content; flow per number = `sum amount x u_d` (since 2026-09-19 on the
   unit vectors of section 2, note 23; until then on D); both read as the
   other change specifies. Read-only; no bijection needed. Since the night
   of 2026-09-19 (the model owner: "the one reading function is the
   amount-weighted moments of order 0, 1 and 2 of the direction vectors,
   valid for fans as for the six headings, here entering the zeroth moment
   alone"; section 10, note 16) the one function `read_arrivals` takes,
   over the arrivals of the reading set, the moments of their direction
   vectors weighted by their amounts: order 0 the count, split outside (a
   ray that arrived this interval, its vector `u_d` of the direction it
   arrived on, before the collision) and here (a ray that did not step,
   its vector (0, 0, 0), so it enters the zeroth moment alone); order 1
   the net flow `sum amount x u_d`; order 2 the traceless tensor `3 x sum
   amount x u (x) u - tr(sum amount x u (x) u) I`, exact integers (the raw
   second moment with its trace removed, times the number of dimensions;
   every `u_d` has the length Q within 1.35 %, so a fan's flow reads Q per
   unit of amount direction-blind, and on the six headings the moments
   are Q times, Q^2 times, what they were on D; note 23). Every coupling
   selects its component by the key
   `reads` (the clock's count and the threshold the scalar, the push the
   vector, a detector may declare the tensor); the detector's record is the
   same moments over the clicked rays with their amplitudes as weights, the
   scalar squared. On the six headings the moments are the slot
   decomposition of the first implementation exactly; on a fan they are
   the moments of the fan's vectors, no projection onto the Ports.
3. **The collision.** At every Node of free space, a Node that holds no
   measured event, the collision table permutes the directions of the
   single units in the seven slots (section 4). Since the night of
   2026-09-19 (the model owner's decision on the physics-rule reviewer's
   F1(c); section 10, note 18) there is **no collision at a Node that holds
   a measured event**: rays meet the table there, not each other; the
   collision is a rule of free space, and a measured event's Node never
   parks a ray at rest or turns an arrival before the table reads it.
   Inverse: the inverse table on the output pattern at the same Nodes (the
   class is invariant).
4. **The measured events' tables and the detectors.** A measured event meets
   the rays that arrived this interval at its Node, per family and number
   other than its own, as today: the threshold on the arrivals (section 5),
   then the `phase_window` on each ray's own phase (no coherent sum: the
   window reads the record; a bundle is now the rays of one number arriving
   in one interval), then the rule: `read` (the push taken; the rays go
   on), `measure` (the click: the amount, its content and its label join;
   the border), `rerelease` (the re-emission, section 5), `pass`. **The
   push is ONE bilinear form** over the arriving rays (the model owner's
   proposal 2, admissible with the reviewer's two corrections; section 10,
   note 20): `push_A = sum over the rays of kappa(A, B) . V_B`, with `V_B`
   the label moment of the rays, the vector moment of `read_arrivals` with
   the labels as weights (`amount x u_d` for a free family, `content x
   amount x u_d` for a paid one, the unit vectors of section 2), and
   `kappa(A, B)` =
   `-M_A` for a free family's ray (gravity, M_A the reader's content as
   the frame read it at the start of the interval, `frame_content`, the
   same for every family's rays whatever the family order: a click of
   the interval joins the content the next frame reads; the
   orchestrator's D1 on the architect's B3, 2026-09-20, note 26), `+
   q_A x q_B / M_B` for a charged free family's ray (electricity, taken as
   the whole part off the reader's clock, `sign x by_clock(age_A, |V q_A
   q_B|, M_B)`, per emitter factor (q_B, M_B) carried on the rows), `+ 1`
   for a paid ray (its label already carries h s). Every input is on the
   reader's record or on the arriving rows; nothing is looked up by
   number. A detector Node's record (section 5) is written from the
   clicked rays. Own-number rays are home: taken to be created again on
   the measured event's `directions` at its next self-creation (as today),
   which is bijective given the record of what came home; a paid family's
   home labels join the momentum at the home and leave it at the
   re-creation (note 18). An open face is a detector whose click books
   the escape (the other change). The click is the only one-way step of
   the interval.
5. **The self-creations** (unchanged in form): `by_clock` for the turn, the
   release (a free family: `content x release` per declared direction, phase
   the clock's; a lamp: `rate` per direction when s > 0, cost and label
   `quantum x s` per unit along `u_d`, the recoil `-label`), what
   came home or is re-released apportioned whole over the `directions`
   (`apportion_whole`, ties in table order from `age mod len(directions)`),
   the owed count read off the clock. Every new ray: `age` 0, the emitter's
   phase, its number. The step of a measured event by its momentum: as the
   other change leaves it (no merge; refused onto an occupied Node), with
   the width of the push since 2026-09-19 (the model owner's D1) and
   the label's scale since the same day (note 23): on an axis whose
   momentum component is p (in label units), a free measured event of
   content M steps one Link per (Q x S x M + p) / p self-creations,
   `by_clock(age, |p|, Q x S x M + |p|)`, S the world key `width` (an
   integer from 1; 1 by default), Q = 64 the label's scale (the width in
   units of one free unit's label, Q x M; the physics-rule reviewer's
   correction 2). One unit of net flow gives any body p = Q M, so the
   speed it gives is 1 / (S + 1) for every content: the push stays
   proportional to the content (the equivalence principle) and the world
   chooses how slow its slowest motion is; every step registered before
   the label's scale is the same step, `by_clock(age, Q n, Q k) =
   by_clock(age, n, k)`. No remainder is kept; the count is the whole
   part off the clock (implementation note 15; `tests/test_push_width.py`).
6. **Merge identical rows; sort by Node.** A bijection (a permutation of rows
   and a sum of interchangeable units).

The prototype's rule holds: only arrivals are measured (a ray created at the
Node this interval is its own release and is not met until it arrives
somewhere), so a re-emitter never re-measures its fresh copies.

## 4. The collision table

**Slots.** Eight single-occupancy slots per Node: the six headings in Port
order and the two rest slots "here a", "here b" (rays2 measured that one rest
slot holding two units is not injective: (A at +x, B at -x) and (B, A) merge).
A ray occupies the slot of its direction when that direction is a heading or
a rest vector. **The alphabet answer:** a ray on any other declared direction
is a spectator; it passes the Node untouched. The table is not applied to a
projection onto the six headings, because a projection is not injective and
would break the bijection, and not to the full direction set, because a table
over `len(D)` directions has no fixed size and the owner specified seven
slots. What this implies: an outgoing crowd of a lamp or an opening on fan
directions never collides (rays2: 0 collisions in 500 intervals), so fringes
and the far field of a source are ballistic and exact; collisions act on the
six-heading gas (a free family's release on the six headings, matter's field
returning on a periodic board, head-on beams) and there they are the only
spreading (the mathematician's T3).

**Slot state.** Each slot is empty (0), single (exactly one unit: one row of
amount 1) or a crowd (2: a row of amount above 1, or several rows). The table
permutes the single units only; a crowd is a wall the pattern never enters
or leaves. **Class** of a slot state `(crowd mask, n = number of singles, S =
the vector sum of the singles' headings, rest = 0)`. Inside a class the
members are sorted (lexicographically as 8-tuples) and the **forward map is
the cyclic shift by +1, the inverse the shift by -1**; a class of one is
fixed. A moved unit takes its new slot's direction (rest vector for a rest
slot); age, phase, number, amount and content are unchanged. Amount and
momentum (the slot headings' sum, hence the labels' sum for units of equal
content; the generic law applies to units, and units of different content at
one Node are different rows, so the table acts per (number, content) class in
a fixed order: number, then content ascending) are conserved by construction;
the class is recomputable from the output, so `INV[FWD[s]] = s` for all 3^8 =
6561 slot states (checked: 5440 classes, 2132 moving states; on the 256
binary states 202 move, as rays2 found). The table is generated and checked
at load from this rule (`ray_tables.py` is the reference; the implementation
ports `collision_table()` and `class_key()` into `RayTables`).

**The 20 orbits.** The six-heading occupation patterns with a "here" flag fall
into 20 orbits under the 48 signed axis permutations (10 x 2; no handedness:
the group includes reflections). The table respects them: two states in one
orbit have classes of equal size and equal (n, S) up to the symmetry. The
table itself is not O_h-equivariant (no deterministic equivariant choice
among symmetric outputs exists; the mathematician, 2.4): the tie among
symmetric outputs is broken by the sorted order, that is by Port order, the
one undeclared breaking, averaged out over the six orientations of a crowd.
The 20 orbit representatives (here = the first rest slot occupied; the row is
the forward image of the representative; hb the second rest slot):

| Pattern | here | orbit | n | S | class | -> forward |
| --- | --- | --- | --- | --- | --- | --- |
| empty | 0 | 1 | 0 | 0 | 1 | fixed |
| +x | 0 | 6 | 1 | (1,0,0) | 1 | fixed: a lone unit is straight |
| +x -x | 0 | 3 | 2 | 0 | 4 | ha hb (the head-on pair parks; +y-y -> +x-x, ha hb -> +z-z, +z-z -> +y-y) |
| +x +y | 0 | 12 | 2 | (1,1,0) | 1 | fixed |
| +x -x +y | 0 | 12 | 3 | (0,1,0) | 3 | +y ha hb |
| +x -x +y -y | 0 | 3 | 4 | 0 | 6 | +z -z ha hb |
| +x +y +z | 0 | 8 | 3 | (1,1,1) | 1 | fixed |
| +x -x +y +z | 0 | 12 | 4 | (0,1,1) | 2 | +y +z ha hb |
| +x -x +y -y +z | 0 | 6 | 5 | (0,0,1) | 3 | +y -y +z ha hb |
| all six | 0 | 1 | 6 | 0 | 4 | +y -y +z -z ha hb |
| empty | 1 | 1 | 1 | 0 | 2 | hb (a lone rest unit alternates a <-> b) |
| +x | 1 | 6 | 2 | (1,0,0) | 2 | +x hb |
| +x -x | 1 | 3 | 3 | 0 | 6 | +z -z hb |
| +x +y | 1 | 12 | 3 | (1,1,0) | 2 | +x +y hb |
| +x -x +y | 1 | 12 | 4 | (0,1,0) | 4 | +y +z -z hb |
| +x -x +y -y | 1 | 3 | 5 | 0 | 6 | +y -y +z -z hb |
| +x +y +z | 1 | 8 | 4 | (1,1,1) | 2 | +x +y +z hb |
| +x -x +y +z | 1 | 12 | 5 | (0,1,1) | 2 | +x -x +y +z hb |
| +x -x +y -y +z | 1 | 6 | 6 | (0,0,1) | 2 | +x -x +y -y +z hb |
| all six | 1 | 1 | 7 | 0 | 2 | all six, hb |

Every pattern that sends a unit into rest holds a head-on pair (S = 0 on two
slots): a rest unit carries no momentum to trade. The known defects of the
six-heading gas (spurious per-line invariants, the anisotropic fourth-order
tensor) are partly remedied by the rest pair and are not a concern of a
static field (its second-order tensor is isotropic; the mathematician, 3.5).

## 5. The detector's record, the re-emission, the face detectors

**The detector is a set of Nodes with ONE record** (the model owner,
2026-09-19, Highlights 5.4: "a detector measuring three Nodes sees one
electron that can be on any of the three"; a click says "here, in one of
these" and not which; the declared width of the set is the position's
uncertainty, and the reading, not the board, is what is uncertain).
Per interval and per family, a detector's set (its declared `positions`;
a measured event outside every declared detector is a detector of one
Node with the default reading) reads the arrivals of every number but
each Node's own at all its Nodes as one set: the **threshold** on the
amount summed over the whole set (a smaller set passes at every Node of
it with a `pass` record naming `threshold`), then the **reading** the
detector declares (`reading`: `beam` by default, or `wave`; section 10,
note 23):

- `wave`: with the rays the set clicks this interval (after the threshold
  and the window; `measure` only), `A_u = 32 x amount_u` (note 3) and the
  1/256 tables `C`, `S` of `core/phase.py`, the coherent pointer over the
  whole set `(X, Y) = (sum A_u C[phase_u], sum A_u S[phase_u])` and the
  record `X^2 + Y^2`, an integer added to the detector's one `record`
  (per detector, cumulative, never per Node). The set's phase is the
  pointer's nearest step (`nature_beam.pointer_phases`: the step of the
  circle whose table entry is nearest in direction, the least
  `|X S[k] - Y C[k]|` among the k with `X C[k] + Y S[k] > 0`, exact
  integers; a zero pointer has no phase). The **window** of a Node's
  entry reads the set's phase (the pointer of the arrivals the threshold
  admitted), not each ray's own: the set is admitted or passes as one.
  After a click the set's phase is **returned to the board** (the model
  owner: "the detector must also return to the board the information it
  received"): every measured event of the set takes it as its own phase,
  so what it emits afterwards, a lamp's release or a re-emission, carries
  the phase it received, as the content and the momentum already return
  by joining the event and pushing it; the frame's turn by content over K
  is added after it as always (E = h f untouched); a pass or a read
  leaves the phase alone. This reading is the reversible detector's idea
  absorbed (the pointer is the detector's phase) and it is **the one
  imported law of physics in the engine**, intensity = the square of the
  summed amplitudes, kept as an option a world declares. Two rays of
  equal amount in phase record 4 A^2 x 256^2, in antiphase 0, each alone
  A^2 x 256^2: the wave is this reading and nothing else (the plain count
  never fringes; rays, section 3).
- `beam` (the default; the model owner's "only events"): a rule on whole
  rays with no amplitude and no square. Over the set, in one interval,
  the rays that would click (after the threshold and the window, which
  here reads each ray's own phase) are paired by opposite phase, greedily
  in the fixed order of the rows (measured event, number, row): a row
  pairs its units with the first later rows of the set whose phase is
  opposite to its own, exactly (a difference of N / 2) when the row's
  Node declares no window and within the half circle centred on the
  opposite phase (the window's own width, the pairing arc) when it does;
  a paired couple does not click and is not absorbed, both parts pass on
  whole with their records (`pass` lines naming `cancelled`), and the
  rest of a row clicks as `measure` does (the content and the momentum
  join, one click record per row naming the detector). The record is the
  plain count of the units clicked; the set's phase returned to the
  events is the phase of the last clicked row of the interval (chosen
  over the mean step: no division, one integer of the record). The books
  close, a cancelled ray going on. Expectation registered: two coherent
  beams of n1 and n2 units meeting at a beam detector click n1 + n2 at
  phase difference 0 and |n1 - n2| at N / 2; between them the pairing
  as implemented gives, for two rows of fixed phases, a step of the arc
  (paired or not), and the law two spread beams read (the model owner
  expects a triangle where `wave` reads a cosine) is the reading A10
  registers on the two-slit screen under both readings, not a pin.

**What stays per Node.** Everything the law does with an arrival's
physics: `measure` joins the content and the label of the ray to the
measured event at the Node the ray actually reached (its held content,
its momentum, the push), the recoil, the momentum labels, the books, the
re-emission (each Node of an opening of declared width re-emits what it
took), the `click` line (its `node`, its `measured` and the ray's own
`phase`); only the reading is over the set. The `record` line is one per
detector per family per interval, after the set's last measured event of
the interval, with its `node` and `measured` None for a set of several
Nodes, the `pointer` under `wave`, the `record` (the square, or the
count) and the set's `phase`; the run's detector report carries per
detector its `reading`, its one `record` and its `phase` at the last
click; a measured event's state carries no record of its own. A face
detector keeps the square of what left through it (no set to pair over).
**The record is exact and never refused**
(section 10, note 19; the physics-rule reviewer's F2, corrected twice).
The record is a reading the host reports, not the law's local work: the
law's bound 2^62 - 1 governs what a Node holds and moves (the amounts,
the contents, the labels, the pushes), and a report of the host has no
bound. The amplitude of a row is `32 x amount` (note 3) and every entry
(C, S) of the 1/256 tables is shorter than 257 for every N (the largest
C^2 + S^2 is 65897), so each component of the pointer is within
`32 x 257 x (the amount clicked)`: the pointer is summed in the int64
register while the amount a detector Node (or a face) clicks of one
family in one interval is within `(2^62 - 1) // (32 x 257)` =
**560759486676481** (`POINTER_AMOUNT_BOUND`, 2^48 inside, 2^49 beyond)
and in Python integers beyond it (`coherent_pointer`: one comparison of
the exact clicked amount per group, a few groups per interval); the
square `X^2 + Y^2` and the record that accumulates it are Python
integers always, per detector per family (`DetectorSet.record`) and
per face per family (`Ledger.face_record`), held beside the arrays and
updated only for the sets clicked. The record of `events.jsonl`,
`run.json` and `state.json` is this exact integer: it can exceed 2^63
(`two_contents` holds 181 x 2^62 on `face:+y` after 200 intervals) and a
reader parses it as an arbitrary-precision integer (JSON has no bound;
Python's `json` reads it exactly). Every sum the law forms (the amounts
and the contents of a set, the labels of the transit line, the merged
amounts) is exact (`exact_sum`), never a wrapped register. The threshold reads the
**arrivals** of every number but the Node's own (the rays that stepped
into the Node this interval; the reviewer's F3, settled by the decision of
note 18: a ray that dwells at the Node on its digital line, or rests
there, is not met again; it is the clock's presence, not the threshold's
set, and no collision at a measured event's Node can put a ray at rest
there); a set below the threshold passes as today.

**The re-emission** (`rerelease`; the absorbed `transduce`): each arriving
record met by the rule is re-emitted at the measured event's next
self-creation on its declared `directions`, its amount apportioned whole over
them (`apportion_whole`, the leftover to the direction `age mod len`), each
part keeping the arriving phase and content per unit, stamped with the
re-emitter's number, age 0; the re-emitter of a paid family's rays takes
the recoil `-(label out) + (label in)`, the one label of section 2 (in at
the meeting as the push of step 4, kappa = 1; out at the re-creation as
the labels of the rows born); a free family's rays met by the rule give
the push of the form (gravity and electricity) and their re-emission takes
no recoil, as a free release costs nothing. What comes home is the same
in and out (note 18). An opening of declared width is a row of such Nodes.
A lamp releases on its `directions` with its clock phase, the recoil the
labels of the rows born. The books close for a paid family over the click,
the re-emission and the home (measured + transit + escaped constant; a
`read` of a paid ray is a report of its label, the ray going on); units
are moved, not copied (the prototype's copying was a lamp of unbounded
content and is not the law).

**The face detectors.** An open face is a detector (the other change): a ray
whose step leaves the board clicks there, its amount, label and content
booked as escaped, its phase on the click record; the face's record is the
same square. A periodic axis has no face.

## 6. What is deleted and which documents change

Deleted: `events/mixing.py` entirely (`coherent_weights`,
`diagonal_weights`, `mix_arrivals`, `place_departures`, `apportion_carried`,
`tie_order`, `integer_root` moves to `core/integer.py` as `integer_root`);
`events/reversible.py`; in `transit.py` the per-Port arrays, `receive`,
`suspend`, `cycle`, `sizes`, `phase_at`, `nearest_step`, `step_window`,
`frozen`, `take`, `place` (the suspension of transit bundles is deleted: the
wait is not a Node's exit any more; the seventh exit is the rest slot of the
collision, and a measured event's delay is the owed count off its clock);
in `engine.py` the `_reversible_*` path, `_pointer`, `detector_readouts`,
the coherent phase read in `_meet`, `EMISSION_CELL_BOUND` and
`EMISSION_MARGIN` (no cell); the merge on a step (the other change).
Tests deleted with them: `test_node_mixing.py`, `test_node_mixing_numbers.py`,
`test_event_transit.py` (replaced), `test_event_suspension.py` (the transit
suspension parts; the measured event's clock parts move to
`test_ray_clock.py`), `test_phaseless_family.py` (the diagonal weights; the
free push by the flow moves to `test_ray_readings.py`),
`test_reversible_detector.py`, `test_reversible_detector_world.py`, the
mixing refusals of `test_integer_bounds_of_measured_and_emission.py`.
Examples: `examples/events/*.json` rewritten as ray worlds (`one_content`
and `two_contents` release on the six headings; `two_slits` and `one_slit`
as section 2; the `bell/` and `coupling/` generators re-emit `"law": "rays"`).

Documents: ENGINE.md is replaced by this document (the per-axis topology and
the record sections move here, shortened; the wave's paragraphs go to
MIGRATION); TERMINOLOGY gains ray, direction, rest slot, collision, record,
and marks event in transit as "a ray"; EXPERIMENTS re-registers series C and
Bell A2 under `rays-v1` (section 8) and keeps the `events-v1` readings as
history; TEST_EXPECTATIONS lists the new modules (section 7);
HIGHLIGHTS_IMPLEMENTATION rewrites the 5.4 rows; MIGRATION gains "The law of
the ray, on 2026-09-19 (`rays-v1`)" naming every deletion; CHANGELOG one
entry; README's project map lists `nature_beam.py` and drops `mixing.py`,
`reversible.py`; DETECTOR_REQUIREMENTS drops its implementation contract;
docs/README.md indexes this document (done with this commit).

## 7. Tests the implementation must add

Isolated, short, fixed arrays, headless; the expected integers written before
the first run (TEST_EXPECTATIONS owns them).

| Module | Case | Expected |
| --- | --- | --- |
| `test_ray_flight.py` | the lone unit, every heading, every declared direction of the example, 150 intervals | straight on its digital line, direction and phase unchanged (`phase_per_link` 0), one Link at most per interval |
| | flight isotropy: 1000 intervals on (1,0,0), (1,1,0), (1,1,1), (3,1,0), (5,2,1) | Euclidean distance^2 within 2 % of 1000^2 / 3 for every direction; equal flight time to equal Euclidean distance within one interval |
| | the flight table | `T_d >= S_1 Q`; `m(tau + 1) - m(tau)` in {0, 1}; `L_d` periods as listed in section 3 |
| `test_ray_collision.py` | the table | 6561 states; `INV[FWD[s]] = s`; the class invariant; the 20 orbits with the sizes of section 4; a crowd slot never changes |
| | conservation | for every moving state the amount and the heading sum are equal before and after |
| `test_ray_bijection.py` | periodic 8 x 8 x 4, 300 records incl. head-on pairs and rest units, 50 forward then 50 inverse intervals, no measured event | the sorted store bit-exact; the state differs at the turning point |
| `test_ray_detector.py` | two rays of amount 1 in phase, then in antiphase, arriving in one interval at a detector of threshold 1 | record 4 x 32^2 x 256^2, then 0; the amount 2 and two clicks both times |
| | the threshold under the one reading set | a bundle of 1 at threshold 2 passes with a `pass` record; rest units count |
| `test_ray_reemission.py` | one ray of amount 3 into a `rerelease` Node with three directions | three rays of amount 1, the arriving phase, age 0, the re-emitter's number; recoil = label in - labels out; books closed |
| | the face click | a ray stepping off an open face: one click on the face detector, escaped amount 1, the record its square |
| `test_ray_clock.py` | a lamp of turn s on two directions | cost and label `quantum x s` per unit along each direction; the owed count off the clock unchanged (reference) |
| `test_ray_worlds.py` | the two slits of section 2 on 60 x 121 x 1, 500 intervals | the interference term V(y) of the screen's record correlates with the two-source Euclidean cosine at lambda = c x period above 0.9 (rays measured 0.969); the plain count additive to the unit |
| | Bell | the ten A2 worlds under `"law": "rays"`: S = 2 exactly, no-signalling exact |
| `test_ray_world_parsing.py` | refusals | `"law": "events"`, `dynamics`, `headings`, a non-primitive direction, a component beyond P, a label beyond 2^62 - 1, `phase_per_link` outside 0 .. N - 1, each named |

## 8. Independent expectations for the re-registered readings

Pinned before implementation, from the prototypes (rays and rays2 measured on
the plane) and the argument that every ray present at a Node is leaving it
(presence = |flow|):

| Reading | Under `events-v1` (registered) | Under `rays-v1` (expected) |
| --- | --- | --- |
| Series C item 5, plane: count x r / q | 0.33 constant (coherent) | constant within 10 % for r >= 8 (rays: 0.31 to 0.33 on a fan; on the six headings a ring mean over mostly empty Nodes, 0.15 to 0.19) |
| flow x 2 pi r / q | about 1 | 1.00 +- 0.10 (Gauss exact for a ballistic stream); `cube_flux` within 2 % of q |
| size x sqrt r | constant | deleted (no size); the detector record of a probe reads presence^2 x 32^2 x 256^2 for one ray |
| Item 6, the clock's count at r (`suspension` 1) | k ~ presence, the log on the plane | k = presence // d ~ 1 / r on the plane, ~ 1 / r^2 in space (the accepted price: M / r^2, not M / r); granular: a Node reads one ray or none |
| Items 1 and 3 (equivalence, superposition) | identities of the phase-less field | identities: rays of different numbers never interact (no collision between spectators; head-on collisions permute directions but not numbers' flows in the mean), so `push_m = m x push_1` and the sum of the two sources' pushes hold exactly record by record |
| Item 4, retardation | the lone-arrival chain 131072, 14563, ... | the first `read` at r on +x at tick `r x ceil(sqrt 3) ...`: at speed 1 / sqrt 3 the front reaches r after `m^-1(r)` = the least tau with m(tau) = r on (1, 0, 0), amount 2^17 whole (no chain: a ray does not spread) |
| Item 2, the third law 4 : 1 | 1.21 to 1.28 | 1.00 exactly where both streams are lone rays on the axis (no rounding) |
| Bell A2 | S = 2, no-signalling exact | unchanged: S = 2 exactly, E(a, b) the triangle 1 - 4 k / N (rays 6, rays2 6) |
| Two slits (A1 as a world test) | fringes in the count | the record fringes at lambda = period / sqrt 3, corr > 0.9; the count does not |

## 9. Implementation plan (one PR, one agent) and risks

1. `docs/`: this document is the contract; MIGRATION, CHANGELOG entries first
   (architecture owner).
2. `core/integer.py`: `integer_root` moved from mixing (core owner).
3. `events/nature_beam.py` (new; engine owner): `NatureBeam`, `RayStore`,
   `RayTables` (`flight_table(directions)`, `collision_table()`, both pure,
   generated and checked at load), `nature_beam(...)` with `inverse`.
4. `events/world.py` (schema owner): `"law": "rays"`, `directions`,
   `phase_per_link`, the measured event's `directions`, the direction and
   label bounds, the refusals; `dynamics` and the reversible validation
   deleted.
5. `events/engine.py` (engine owner): `EventSimulation.step` becomes the
   frame around `nature_beam`; `_meet`, `_release`, `_move` reduced to the
   measured event's clock and tables; the books gain `record` per detector;
   the reversible path deleted. `transit.py` reduced to the periodic
   `adjacent_node` use or deleted if nothing remains.
6. `events/run.py`, `snapshot_writer.py`: the store in `state.json` (rows per
   Node), `record` in `run.json` and `events.jsonl` (`click` gains no field;
   the detector's per-tick `record` is a new line).
7. Delete `mixing.py`, `reversible.py`, the tests and examples of section 6;
   add the tests of section 7; rewrite the examples and the two generators.
8. Documents of section 6; `tools/coupling_readings.py` and
   `tools/bell_chsh.py` read the new record; re-register series C and Bell
   with the expectations of section 8 and the runs' fingerprints.
9. `python tools/check.py --full`; the physics-rule reviewer on the tables
   and the readings; the regression evidence in VALIDATION.md.

Risks. (a) **The momentum bound**: the label `content x amount x u_d` has
a component up to Q = 64 on every direction (since 2026-09-19, note 23;
until then `content x amount x D`, growing with P), so a content 2^36
exceeds 2^62 at amount 2^20 on any direction; the parser refuses at
load, naming the numbers, and dense lamps must lower the content or the
rate.
(b) **The direction set size**: a fan of every primitive vector with
components up to 24 is 720 on the plane and about 10^5 in space; `len(D)`
is capped at 4096, `L_d` grows as about 222 |v| S_1, so the store's bound
is large though fixed; worlds should declare only the directions they use.
(c) **Performance**: today 3.6 us per Node per interval on dense arrays; the
store costs per row (0.1 us in flight, about 1 us with a Python collision
loop in rays2), so a board with one ray per Node breaks even and a dense
gas of the six headings with `sum L_d x N` rows per Node is slower; the
collision must be vectorized (segment ids, a `bincount` per Node, one table
read on the 3^8 code, `np.put` of the new directions) to reach the budget.
Resolved by the implementation and its optimizations (section 10, notes 8
and 22: 0.11 us per Node on the plane, 0.69 us per row on the two slits).
(d) The tie by Port order in the collision is the one undeclared breaking;
a test asserts the six-orientation average of a head-on pair's exits is
isotropic. (e) The re-registered readings are expectations, not results:
series C item 6's slowing changes power (the accepted price), and the
register must say so.

## 10. Implementation notes (2026-09-19, the implementation)

The decisions the implementation took where the design was silent,
impossible as written or ambiguous, each decided by the design's principles
(one generic function, every piece of logic once, a bijection but the click,
the flight table's speed, integers only) and recorded here as the
implementation's part of the contract. The design above is unchanged.

1. **The reading is of the arrivals.** (Amended by note 16.) Until the
   night of 2026-09-19 the seven slots of `read_arrivals` were the amounts
   that arrived through the six Ports (the Port a ray's last step entered
   by) and here (the rays that did not step this interval, the rest rays
   among them), a ray on a declared direction counting in the Port of its
   last Link. What stays: the reading is of what arrived this interval
   (the row's `arrival`, the direction the ray arrived on, kept through
   the collision) and of what stayed; what changed: a fan ray now enters
   with its own vector `D[direction]`, not the unit Link of its last step.
2. **Rest rays keep their age.** A rest direction has period 1 in the
   flight table, but the age of a ray parked by the collision is kept (the
   walk and its inverse leave a rest ray's age untouched); otherwise the
   inverse walk could not restore the age a ray had when it parked and the
   interval would not be a bijection. The seeding of a declared ray at rest
   reduces its `age` modulo the heading period.
3. **The amplitude is linear in the amount.** The design's isqrt(1024 x
   amount) is not invariant under the merge of identical records (two rows
   of amount 1 and one row of amount 2 would record differently), so the
   amplitude of a row is 32 x amount, exact and merge-invariant; one unit
   records 32^2 x 256^2 as the design says, a row of n identical rays
   n^2 times that (the coherent sum of n equal amplitudes).
4. **Home keeps the arriving phase and content.** What comes home is
   created again with the phase and the content per unit it arrived with
   (as the re-emission does), not re-stamped by the clock; the books'
   absorbed and released lines carry it exactly.
5. **A ray below the threshold or outside the window passes with a
   `pass` record** naming `threshold` or `window`; a set at the threshold
   clicks row by row (one `click` record per row, the amount on it) and the
   window reads each row's own phase, no coherent phase of the set (the
   record is the coherent reading; the window is a gate on the record).
6. **The inverse interval exists only without a measured event**: with one
   on the board `inverse_step` refuses (the click, the release and the home
   are the one-way border and no inverse of them is defined); the
   bijection test runs on a board of rays alone.
7. **The two-slit example uses a dense fan.** A fan of five directions
   gives ballistic spots on the screen, not fringes; the example and the
   world test re-emit at the openings on the 91 primitive directions
   (a, b, 0) with a >= 1 and a + |b| <= 12 (P = 12), the lamp of turn 8
   (K 2^30) on five directions toward the wall, 500 intervals; the
   correlation pinned at 0.85 for this fan (measured 0.893; the design's
   0.9 was for a fan of 203).
8. **The step table is `int8`** (D x L_max x 3, the step of each age per
   direction), the collision table `int16` codes over 3^8, the store's
   columns `int64`; every physical value is an integer and every bound
   check is against 2^62 - 1.
9. **The Bell worlds run 160 intervals**: the flight table's pace puts the
   plus click of age a at tick a + 14 and the minus click at a + 16, so 128
   pairs need 144 ticks; 160 leaves the margin. `tools/bell_chsh.py` admits
   the `record` line among the record kinds and checks the minus offset
   above the plus.
10. **`reads` names the component**, one of `scalar` (outside + here, the
    default: the presence, the threshold), `outside`, `here`, `vector` (the
    flow) and `tensor` (the traceless second moment, since the night of 2026-09-19 a 3 x 3 matrix, note 16); the push always
    reads the flow and the clock's count always the scalar; a detector
    entry may declare `tensor` and the world test of the detector
    definitions does.
11. **The section 2 example is illustrative**: its K 1024 with a content of
    10^6 would give a turn of 976 steps beyond N; the shipped
    `two_slits.json` uses K 2^30 and a content of 8 K + 1 400 000 (a turn
    of 8, the phases stamped a mod 64). The parser refuses a content at or
    past K x N / 2 as before.
12. **A ray may be declared on a board without a measured event** (the
    in_transit `number` bound is max(1, the number of measured events)),
    so the bijection and the collision tests run on rays alone.
13. **Every ray steps at its first interval**: the flight table's first
    walk is at tau = 1 for every direction (T_d >= S_1 Q), so a declared
    ray at age 0 crosses its first Link in the first interval and a ray
    released at tick t first walks at t + 1.
14. **The registered readings** (section 8) are marked measured against
    expected in EXPERIMENTS.md; the far-field ring means of a six-heading
    source follow the lattice ring's Node count (the rings at r = 16 and
    r = 20 both hold 112 Nodes) and fall outside the ±10 % expectation,
    registered and not moved; the fan the expectation was pinned on is the
    owner's decision to run.
15. **The table from the keys; the kind from the quantum** (the model
    owner, the night of 2026-09-19, "I approve 1 and 3", Highlights 5.4;
    `tests/test_default_table.py`). `world.default_table(families)` is the
    one function that gives every measured event its table (section 2);
    `FamilyDefinition.free` is `quantum == 0`; the constraints the parser
    kept are expressed through the quantum and not widened: a charge is
    refused on a paid family (h >= 1), a lamp on a free one, a free unit
    carries no content and its label is `amount x D` (the mathematician's
    note that "paid => q = 0 and free => h = 1 are decisions, not
    necessities" is recorded, not acted on). `quantum` is required: a
    default would be an implicit kind. The record (`run.json`) carries
    `quantum` per family and no `kind`. Every example world parses to the
    same `RayWorld` as before the change (checked structure by structure
    over the 39 worlds), and the Bell and coupling runs are unchanged
    record by record (VALIDATION.md).
16. **The moments replace the slots** (the same decision; `tests/
    test_ray_readings.py` (a)). `read_arrivals(vectors, amounts, keys,
    size)` takes the moments of section 3, step 2, exact integers, with
    the normalisation `tensor = 3 x M2 - tr(M2) I` for the second moment
    `M2 = sum amount x D D^T` (the trace removed times the number of
    dimensions, so no division); the `Reading` holds the six entries of
    `M2` and forms the tensor on demand. On the six headings the moments
    equal the slot decomposition exactly (the old `(p_x + p_y - 2 p_z,
    p_x - p_y)` being `-T_zz` and `(T_xx - T_yy) / 3`); under the 48
    signed axis permutations the scalars are fixed, the vector rotates and
    the tensor is conjugated. What this changes on the board: only the
    reading of a fan ray at a measured event, whose push is now its label
    `content x amount x D` (the recoil its emitter took) and not the unit
    Link of its last step, so the momentum a wall takes from a fan closes
    with the lamp's recoil; the six-heading worlds (Bell, series C, one
    and two contents) read exactly as before. The reading is bounded
    before any product is formed (`amount x P^2 x rows` against 2^62 - 1,
    `OverflowError` beyond it); the Links crossed per Port (`per_port`,
    for Gauss's flux) remain a diagnostic of the walk, not of the reading.
17. **The width of the push** (the model owner's D1, 2026-09-19, Highlights
    5.4, "try D1"). The step rule of step 5 reads the world key `width`
    (S, an integer from 1, 1 by default): `_move` steps on an axis when
    `by_clock(age, |p|, S x M + |p|)` is 1, in place of `M + |p|`. With
    S = 1 nothing changes for any existing world (the coupling series' 1b
    identities hold as registered); with S = 8 a body with p = M steps once
    per 9 self-creations. Kept as they were: at most one Link per interval,
    x before y before z (an axis whose step coincides with an earlier
    axis's step in one interval loses it, nothing carried); a measured
    event steps only in an interval where it owes nothing, so the step of
    a self-creation whose count is owed lands on the interval that pays
    the count; the momentum is untouched by the step; `run.json` records
    `width`. The parser refuses 0, a negative width, a string and a
    fraction naming the key (`tests/test_push_width.py`; the experiment
    that uses it is series D in EXPERIMENTS.md).
18. **The one label; no collision at a measured event's Node** (the
    physics-rule reviewer's F1, blocking, and the model owner's decision on
    its case (c), the night of 2026-09-19; `tests/test_ray_push.py` (h),
    `tests/test_ray_collision.py` (d)). Until this note the push read the
    rows' arrival (the moments change) while the click's momentum, the
    recoil and the transit line read the rows' direction, which the
    collision could have turned at the detector's Node, and a head-on pair
    of one number collided at a windowed detector left one ray stranded at
    rest. Now every momentum the law reads or moves is the one label of
    the rows, `momentum_labels` (section 2): the push's moment (step 4),
    the click's momentum on its record and on the detector, the face
    click's, the recoil of a release and of a re-emission (the labels of
    the rows born) and the transit line; and the collision (step 3) does
    not act at a Node that holds a measured event (rays meet the table
    there, not each other), forward and inverse alike, so at such a Node
    the arrival is the direction and the reviewer's three cases read
    consistently: a (2, 1, 0) ray of content c and amount a clicking gives
    the detector (2, 1, 0) x c x a; a re-emitter passing a ray straight
    through on its own direction ends with the momentum it had; the
    head-on pair at the windowed detector clicks one ray with its label
    and passes the other on its way, nothing at rest. With it, what comes
    home of a paid family joins the momentum at the home (`push` on the
    `home` record, its labels' sum) and leaves at the re-creation, so the
    momentum book of a paid family closes over the click, the re-emission
    and the home (until this note a home leaked the label out). The
    reviewer's F3 dissolves: the threshold reads the arrivals (section 5).
    The bijection of the interval is unchanged (the inverse skips the same
    Nodes; `tests/test_ray_bijection.py` passes as before) and the
    registered runs are unchanged record by record (no collision acts in
    them and their arrivals are their directions; VALIDATION.md).
19. **The record exact, never refused** (the reviewer's F2, corrected
    twice; `tests/test_ray_detector.py` (e), `tests/test_ray_worlds.py`
    (e)). The finding: the record's amplitude products were unchecked
    int64 (an amount of 2^52 recorded 0 silently) and the design's bound
    `256 x 32 x isqrt(sum amount)` was stale (the amplitude is linear,
    note 3). The night's correction refused the run when a detector Node
    or a face clicked more than the affordable amount
    `RECORD_AMOUNT_BOUND` = isqrt(2^62 - 1) // (32 x 257) = 261123 of one
    family in one interval; the same night `examples/events/two_contents.json`
    (two fixed contents of 2^24 at `release` [1, 128] on an open 21^3
    board), which had run 200 intervals before the bound, was refused at
    its 20th interval when the two +y beams of 2^17 left through
    `face:+y` together (262144). A refusal was the wrong correction for a
    report: the record is a host reading, not the law's local work, so
    it must be exact and can be neither refused nor wrapped. The
    correction now (2026-09-19, after the batching): the pointer (X, Y)
    is summed in the int64 register while the clicked amount is within
    `POINTER_AMOUNT_BOUND` = (2^62 - 1) // (32 x 257) = 560759486676481
    (each component within 32 x 257 x the amount, inside 2^62 - 1) and
    in Python integers beyond it (`coherent_pointer`); the square and the
    cumulative record are Python integers always (`Measured.record`,
    `Ledger.face_record`); `RECORD_AMOUNT_BOUND`, `check_record_amount`,
    `record_amount` and the refusal are deleted. The record written to
    `events.jsonl`, `run.json` and `state.json` can exceed 2^63 and is
    parsed as an arbitrary-precision integer. Every reduction of the law
    stays exact (`exact_sum`, `exact_column_sums`, the merge's sums, the
    label weights checked before their product). The 44 other example
    worlds are byte-identical before and after; `two_contents` completes
    its 200 intervals with the books closed (VALIDATION.md).
20. **The push as one bilinear form; the emitter's factor on the record**
    (the model owner's proposal 2, "2 with the physicist"; the reviewer's
    verdict "admissible with two corrections"; `tests/test_ray_push.py` (a)
    to (g)). `push_form` computes `push_A = sum kappa(A, B) . V_B` (step
    4) in one place; the three-branch `push_of` and the lookup of the
    emitter by number (`world.measured[number - 1]`, the one LOCALITY-1
    deviation, with the lcm denominator `content_lcm`) are deleted. The
    emitter's factor of a free family's ray is carried on its record from
    birth as TWO integer columns, `charge` (q_B) and `mass` (M_B), never a
    floored ratio (a floored 3/4 would destroy the coupling); M_B is the
    content the release rate read at birth, the emitter's held content of
    the family at that self-creation, equal to the declared amount on
    every registered world; a declared ray in transit of a free family
    takes the charge and the declared amount of the measured event its
    number names (0 and 0 without one); a paid family's rows carry 0 and
    0, their factor being their content. The electric part is `sign x
    by_clock(age_A, |V q_A q_B|, M_B)` per (q_B, M_B) class among the
    rows, which equals the earlier computation integer by integer
    including the floor (the reviewer: since M_B divides the lcm D,
    floor(n k / (k M_B)) = floor(n / M_B); 20160 cases, 0 mismatches), and
    the registered series C and Bell runs read unchanged record by record
    (VALIDATION.md; the series 7 worlds, kappa 0 in `7_pp` and `7_mm`,
    -2^25 and -2 in `7_mp` and `7_pm`, -12582912 and -3 in `7_pp_m4`,
    -2^24 and -1 in `7_00`, row by row). The rounding subtlety of today
    survives unchanged and is stated: `age_A` is the reader's age after
    the frame's advance, frozen while it is owed. The reviewer's F7 is
    closed: fixed local work (one product and one `by_clock` per axis per
    factor class met), fixed local storage (two more integers per row,
    functions of the number today, so the store's bound does not grow;
    the merge compares them), no lookup beyond the Node.
21. **Open: the magnitude of a fan ray's label** (a finding for the model
    owner from the re-registration of series D, the night of 2026-09-19;
    not changed here). The label of a ray is `content x amount x D` with
    D the integer direction (section 2, the law as designed), so its
    magnitude grows with the integer length |D| of the direction: equal
    amounts released on (1, 0, 0) and on (7, 5, 0) carry the momenta 1 and
    sqrt 74, and the push a fan source gives is the fan's mean |D| times
    what six headings give (the orbit series' 120 directions: 5.19). The
    open question is whether the label should be along the unit vector of
    the direction at the flight table's scale Q = 64 (the same table as
    the flight, one table: every direction's momentum per unit of the same
    length), which this implementation recommends the owner rule on; the
    recoil, the click and the push would then read the same magnitude for
    every direction. Registered in PROJECT_STATUS ("What is open") and in
    the orbit register (EXPERIMENTS.md, D); nothing was changed in the
    law. **Decided on 2026-09-19: the label is along `u_d` (note 23).**
22. **The host's batching** (the optimizations of 2026-09-19; the model
    owner: "make sure there is optimization in everything"). Five changes
    to how the host runs the law and none to the law: the same integers
    in the same order of reduction, every example world's `events.jsonl`
    and `state.json` byte-identical before and after (VALIDATION.md), the
    bijection and every pinned test unchanged. (i) Step 4 is taken in
    bulk across the measured events: the rows at measured events found by
    one gather per family, grouped by (measured event, number) with one
    segmented sum per moment, the threshold and the window as masks,
    every bound of the per-set rule checked per group (the same
    condition, the same refusal at the same point of the interval), the
    records and the side effects then applied per group in the order of
    the records (`FamilyPlan`); the walk already batched the rays and the
    collision the Nodes the same way. (ii) The dense readings of the board
    (`count`, `flow`, `presence`, `per_port`) are diagnostics, decomposed
    on request from the rows the walk left (`Readings`, `ArrivalRows`)
    over the active Nodes only; the law reads its own local sets at the
    measured events; the keyed reading's bound is checked when the
    diagnostics are read. (iii) The merge orders the rows by one packed
    key of the identity fields when their ranges fit 62 bits (checked at
    every merge from the columns' extremes, `merge_key`) and by the
    lexsort of the fields otherwise, the same total order; the second
    sort by Node is gone, the Node being the first field. (iv) The books
    are running ledger lines: the transit momentum is kept by the law as
    rows are born and leave (`Ledger.transit_momentum`; the collision
    conserves it, its class fixing the vector sum of the singles, and the
    merge conserves it), the transit and content `current` are what was
    released less what left; `RaySimulation.recount()` counts the three
    lines from the rows on request and `tests/test_ray_books.py` asserts
    the running lines equal the recount at every interval; the per-tick
    `balanced` of `run.json` now checks the ledger's own consistency, the
    recount the store. The collision table is generated once per process
    and shared read-only. (v) The clocks' frame is taken for every
    measured event at once (`_frame_all`), the self-creations visit only
    the measured events that can release, `np.r_` and the per-family
    property reads are gone from the interval, `events.jsonl` is written
    through a megabyte buffer. Not done: a process pool (the audit's
    condition: it pays only above about 10^6 rows per interval; the
    per-world parallelism of `tools/run_series.py` uses the cores) and
    narrower dtypes (the store's columns stay int64 for the bound checks,
    the step table int8; no measurable cost at these sizes). Measured
    (headless, the record and the books every tick, the best of three
    runs): the plane source of series C 2.97 -> 1.61 ms per interval
    (0.20 -> 0.11 us per Node, 0.75 -> 0.40 us per row), two slits 12.4
    -> 3.5 ms (1.71 -> 0.48 us per Node, 2.43 -> 0.69 us per row), Bell
    0.53 -> 0.47 ms, one content 0.77 -> 0.58 ms, the orbit s32_r12 1.47
    -> 0.77 ms; the suite 16.8 -> 5.5 s. Risk (c) of section 9 is
    resolved: the collision is vectorized (segment ids, one table read
    per Node) and the interval's cost is a function of the rows in flight
    and the measured events met, not of the Nodes, the store's promise of
    section 3 (the plane's 14641 Nodes cost 0.11 us each, the two slits'
    5100 rows 0.69 us each).
23. **The label along the unit vector of the direction at the flight
    table's scale** (the model owner's decision of 2026-09-19, Highlights
    5.4, "go for it", on the physics-rule reviewer's verdict on note 21:
    the D-label was "the right direction and the wrong magnitude", |p|
    discontinuous in the direction ((4, 3, 0) and (7, 5, 0), 1.4 degrees
    apart, carrying 5 and 8.60 at equal amounts) and a fan's push
    diverging with the grain of its declaration (5.19 x the headings at
    |D| <= 8, about 10 x at |D| <= 16); `tests/test_ray_label.py`). The
    label of a unit is `u_d`, the integer vector nearest `Q D / |D|`,
    Q = 64 (section 2), by the reviewer's exact integer rule `k(|a|) =
    (isqrt((2 Q |a|)^2 // |D|^2) + 1) // 2` with the sign restored: it
    equals the float rounding on all 1780418 primitive directions with
    components in -64 .. 64 (0 mismatches), has no tie for a direction
    bound below 147 (a half-integer needs |D| a multiple of 256), gives
    exactly `Q e_d` on the six headings, `u_{-D} = -u_D` and `u_{gD} =
    g u_D` under the 48 signed axis permutations, and every component
    within Q. Pinned: (1, 1, 0) -> (45, 45, 0); (1, 1, 1) -> (37, 37,
    37); (2, 1, 0) -> (57, 29, 0); (3, 1, 0) -> (61, 20, 0); (7, 5, 0) ->
    (52, 37, 0); (11, 1, 0) -> (64, 6, 0); (1, 2, 3) -> (17, 34, 51);
    (63, 46, 46) -> (45, 33, 33). Exact under it: every conservation of
    note 18 (push = label sum, click = label, recoil = -(labels born), the
    re-emission -(out) + (in), home, face escape, the transit line), the
    collision (it acts on the eight slot directions only, so the label
    sum it conserves is Q x content x S, S the heading sum), the bijection
    of the interval, the books. Approximate, the law's grain: |u_d| = Q
    within sqrt 3 / (2 Q) = 1.35 % (the worst (63, 46, 46) -> 1.30 %; the
    orbit fan 0.994 .. 1.009, mean 1.0000) and u_d parallel to D within
    0.78 degrees, comparable to the flight's own 0.77 % speed anisotropy,
    both governed by the one Q (a larger Q shrinks both at 1 bit of bound
    per doubling; the owner's knob, not required). The four corrections
    of the verdict, all binding and implemented: (1) the rounding rule
    above, in integers only (`integer_root`); (2) the step rule
    `by_clock(age, |p|, Q x S x M + |p|)` in `_move` (section 3 step 5:
    the width in units of one free unit's label, so one unit of net flow
    gives 1 / (S + 1) and every registered step is bit-identical,
    `by_clock(age, Q n, Q k) = by_clock(age, n, k)`); (3) the parser's
    label bound and `label_weights` at `Q x content x amount <= 2^62 - 1`
    per row, refused loudly with the number (`world.LABEL_SCALE`; the
    parser's bound on the default P = 64 is the same number as before,
    on the six headings it tightens from 2^62 to 2^56 per row; the
    bound-edge tests are re-pinned at 1/64 of their amounts); (4) the
    reading's vector and tensor moments on `u_d` in place of D
    (`Readings`, the reading at a measured event, step 2), so a fan's
    flow reads Q x q direction-blind; the zeroth moment is unchanged.
    What else changes: the label moment's bulk bound is the first
    moment's (weight x |u| x rows, `first_moment_overflow`), and the
    reading's second-moment bound, amount x Q^2 x rows, now refuses a row
    above 2^50 at a measured event's Node (the detector test's row of
    2^52 re-pinned at 2^49, still beyond the pointer's register bound).
    Unchanged: the flight table T_d, the collision table, the clock, the
    threshold, Gauss's flux off the Port crossings (`per_port`,
    `cube_flux`, the tool's `square_flux`), the record. Every momentum in
    a world file (`momentum`) and in `run.json` and `state.json` is in
    label units, x 64 for a heading; the registered runs: series C reads
    every push, momentum and book line x 64 exactly (the electric part
    too, `q_A q_B / M_B` being an integer on every series 7 world and
    `by_clock(age, 64 n, k) = 64 by_clock(age, n, k)` when k divides n),
    the tool `tools/coupling_readings.py` dividing the labels by Q where
    it compares with q or an amount, so every criterion and reading is
    the same; Bell is unchanged (S = 2, 326 criteria); series D is
    re-derived with L = 1 in label units under the Q S M rule and re-run
    (EXPERIMENTS.md, D; `examples/events/orbit/`). A fractional electric
    coefficient no longer alternates (`test_ray_push` (e): 96 per tick
    where 2, 1 alternated), the floor resolving 1 / Q per unit. Every
    pinned test's momentum integer is x 64 (the fan fixtures on u_d;
    TEST_EXPECTATIONS lists the re-pins; MIGRATION the units).
24. **The detector's set, its two readings and the phase returned** (the
    model owner, 2026-09-19, three decisions of the same day: the
    detector a set with one record, "the detector must also return to
    the board the information it received", and the key `reading` with
    `beam` the default and `wave` the imported law; section 5;
    `tests/test_ray_detector.py` (f), (g), (h)). The decisions the
    implementation took: (i) the set's phase is `pointer_phases`, the
    step whose table entry is nearest in direction to the pointer, exact
    integers (in the int64 register while every component is within
    `POINTER_STEP_BOUND` = (2^62 - 1) // 257, Python integers beyond);
    a pointer of one ray at phase p reads p wherever the 1/256 tables
    tell the steps apart (every N through 64; at N = 4096 adjacent
    entries coincide and the reading is to the tables' resolution, as
    the record itself is); a zero pointer (an antiphase pair) has no
    phase: the window treats it as outside and the events keep their
    phase. (ii) Under `wave` the window reads the phase of the pointer of
    the arrivals the threshold admitted over the set; the record's
    pointer is of the rows that clicked (equal when every Node of the
    set measures under one window, the declared case). (iii) The
    `record` line and the phase returned follow the set's last measured
    event that had anything this interval, per family in family order
    (when two families click one set in one interval the later family's
    phase is the one the events keep). (iv) The `click` line keeps the
    ray's own phase (the ray's record, what `tools/bell_chsh.py` reads
    as the age mod N); the set's phase is on the `record` line and in the
    report. (v) Under `beam` the pairing walks the rows of the set in
    the order (measured event, number, row) and splits a row: the paired
    units stay in the store as the row's amount (the row is not
    absorbed), the rest clicks; the reading's moments, the push and the
    labels are of the clicked units; the `record` line under `beam`
    carries the count and the phase and no pointer. (vi) A measured event
    outside every declared detector is a detector of one Node with the
    default reading `beam`: the wall of the two-slit worlds now counts
    what it absorbs; the face detectors keep the square (a face has no
    set to pair over and is not declared). (vii) The screen of
    `two_slits.json`, `one_slit.json` and the world test is declared as
    121 one-Node `wave` detectors `screen_<y>` (the screen's pixels):
    declared as one detector of 121 Nodes it would read one record with
    no resolution in y (the declared width is the uncertainty), and a
    pixel one Node wide reads what the Node read before, so its record
    and the pinned correlation are unchanged. (viii) The Bell worlds
    read exactly as before under the default `beam`: one ray per
    interval per detector, nothing to pair, every `click` and `pass`
    line identical; their `record` lines now carry the count 1 and the
    phase, `run.json` carries no `measured[].record` and its counters'
    `phase` is the last click's (VALIDATION.md). `Measured.record` and
    the per-Node threshold are gone (`DetectorSet`, MIGRATION.md).
25. **The label's product checked before it is formed** (the architect's
    B1, blocking, 2026-09-20; `tests/test_ray_label.py` (c), (d)). Until
    this note `momentum_labels` bounded the weight at `Q x weight` and
    the births' labels were checked after the int64 product; the
    architect's probe (a heading row of amount 2^58 re-emitted on
    (64, 1, 0), before the label along `u_d`) read a label of 0 where the
    exact is 2^64, the books balanced at the wrong integer. Now the one
    pre-check `label_overflow_rows` (the weight times the largest
    component of the row's unit vector within 2^62 - 1, both products
    tested by division, nothing formed) runs per row inside
    `momentum_labels` and, in bulk with the same rule, before the home
    and the taken rows' labels of step 4 (`first_label_overflow`); the
    post-check at the births is deleted; the refusal names the Node, the
    amount, the content, the unit vector and the product. The check is
    exact per direction: a row of weight 2^56 on (1, 1, 0) (u = (45, 45,
    0)) is accepted where the heading's 64 x 2^56 = 2^62 is refused. The
    parser's bound (Q x content x amount on a declared ray, a lamp's or
    a free release) is unchanged and conservative; what it does not
    reach, a merged row, is refused at the next label formed of it.
26. **M_A is the content the frame read** (the architect's B3, blocking;
    the orchestrator's D1, 2026-09-20; `tests/test_ray_push.py` (j)).
    Until this note the push read `Measured.content` inside the
    per-family loop of step 4, after the clicks of the families before
    it in family order had joined `held`, so the world file's family
    order changed the integers (the architect's probe: `[A, B]` pushed
    (-356544, 0, 0) against `[B, A]` (-378432, 0, 0), the first read
    -960 against -1536). Now the frame reads every measured event's
    content once into `frame_content` before the law runs (`_frame_all`,
    beside `clock_age` and `turn`; the turn is read off the same
    content) and the push, gravity and electricity alike, reads that:
    order-independent, and the click of an interval pushes from the next
    interval on. No registered run has a paid click and a free read at
    one reader in one interval, so every pin and every registered
    reading is unchanged; the step rule (`_move`) reads the live content
    after the interval as before.
