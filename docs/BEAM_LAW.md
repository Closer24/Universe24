# The Beam Law (`beam-v1`)

The beam is the record of an event in transit, `NatureBeam` in the code; on
the GameBoard there are only events; until 2026-09-20 this law was called the
law of the ray, and "ray" stays its informal name in prose (the model owner,
2026-09-20, [Highlights 5.4](HIGHLIGHTS.md#54-the-detector); the identity
`beam-v1` is `rays-v1`, the same law, [migration](MIGRATION.md#the-names-naturebeam-and-gameboard-and-the-glossarys-single-names-on-2026-09-20)).

The published design and implementation contract of the Beam Law, the
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

- **Model identity** `beam-v1`. A world selects it with `"law": "beam"`; the
  record (`run.json`) carries `"law": "beam-v1"`. `configuration_validation`
  reports the kind `beam`.
- **`events-v1` is deleted** (the owner's rule, one engine). `"law": "events"`
  is refused naming the Beam Law and pointing to MIGRATION. The engine
  package `src/event_universe/events/` keeps its name (the GameBoard's things are
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

`NatureBeam` (one record; the GameBoard's state is a multiset of them; identical
records at one Node are one record with the amounts and contents added, which
is a bijection since identical units are interchangeable):

| Field | Meaning | Bound |
| --- | --- | --- |
| `node` | the Node (three integers, in `shape`) | 0 .. 4095 per axis |
| `direction` | index into the world's direction table `D`; entries 0 and 1 are the two rest vectors (0, 0, 0) ("here a", "here b"), 2 .. 7 the six headings in Port order, 8 .. the declared further directions, each a primitive integer vector with every component in -P .. P | 0 .. len(D) - 1 |
| `age` | the count of intervals since the measured event that created the ray, a birth or a re-emission (a collision keeps it), kept **whole** on the record since 2026-09-20 (note 25; until then reduced modulo the direction's period `L_d`): the flight reads it modulo `L_d`, its place on the digital line (section 3), and a measured event, the external thing, reads it whole as the age moment of the one reading (step 2); `age` 0 at birth | 0 .. `age_bound` |
| `phase` | a step of the circle of N, stamped by the emitter's clock at birth, turned by the family's `phase_per_link` steps at every Link crossed and, since 2026-09-20 under the world key `meeting` (note 35), advanced by the crowd a paid unit meets at every free-space Node in whole units of Q (the phase carries the crowd met modulo N, one grain step of the direction per wrap of the circle) | 0 .. N - 1 |
| `number` | the last emitter (a measured event's number) | as today |
| `amount` | whole units | 1 .. 2^62 - 1 (`AMOUNT_BOUND`) |
| `content` | the content one unit carries (`quantum` x s at birth for a paid family, 0 for a free one) | 0 .. 2^62 - 1 |
| `family` | the family index (one store per family, so implicit in the store) | |

Nothing else is on the record: since 2026-09-20 (the model owner, Highlights
5.4: charge is per unit of content of a family; section 10, note 28) the
factor of the electric push is the family's `charge`, the charge per unit
of content rho declared as an integer or a pair `[n, d]`, and the two
columns `charge` and `mass` of note 20 (the emitter's charge and content at
birth) are deleted from `NatureBeam`, the store and `state.json`.

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
(the label flow, section 3 step 4), what a click moves onto the
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
(`momentum_labels`, `label_overflow_rows`; since 2026-09-20, note 26: a
merged row can outgrow the parser's bound, and until then the born
labels' product was checked after it was formed, so a wrap inside the
bound passed silently); the refusal names the Node and the amount.

World-file keys added: `"law": "beam"`; per family `charge`, since
2026-09-20 the charge per unit of content rho, an integer c (the pair
`[c, 1]`) or a pair `[n, d]` with d from 1 (a measured event's charge is
rho times its content, a report; on a paid family since 2026-09-20 the
whole charge per unit of amount, an integer, read on the charge line of the
books alone, D-1, note 36 (ii); refused with a denominator of 0 or a part
that is not an integer, and on a paid family with a denominator other than
1); the
key `charge` on a measured event is refused naming MIGRATION; since
2026-09-20 (note 31; the model owner, "one mechanism for all the laws on
the GameBoard") per family `columns`, an object of column name to
`{"value": n or [n, d], "sign": 1 or -1}`, the further columns of the one
coupling per unit of content: `gravity` is the built-in first column of
every family (the value [1, 1], the sign minus; a declared `gravity` is
refused), `charge` the built-in second (the sign plus; the family key
`charge` is its value's shorthand, and `columns.charge` may replace it
but not join it), a declared name's sign is the column's (one per name
across the world, two signs refused), a family that does not name a
column carries [0, 1] there, a paid family's values must be 0, at most
`COLUMN_LIMIT` = 8 columns in all, and the world's column order is
gravity, charge, then the names in the order of their first declaration;
the record carries `columns-v1` under `hypotheses` when a column beyond
`charge` is declared; since 2026-09-20 (note 31 (vii); the model owner,
"the strong force's range is a lifetime, L") per family `lifetime`, an
integer L from 1, one scalar (a list refused; absent, the family lives
forever): a ray of the family whose age reaches L at the end of its walk
makes no next event but a click on the border `lifetime`, booked exactly
as an open face books an escape (step 6; section 5), refused beyond the
world's `age_bound`, a declared ray of the family at or beyond it
refused, and the name `lifetime` refused for a detector as a face's name
is; the record carries `columns-v1` also when a lifetime is declared;
since 2026-09-20 (note 31 (viii); the physicist's D-1) per measured
event `held`, an object of family name to content (an integer from 1),
the content the event holds of families other than its own beside its
`amount`: its content is the sum over what it holds, its charge in every
column the exact rational sum over the families held of their value
times their content, every free family it holds is released at the
world's rate beside its own, and a held paid family is content it
carries (only a lamp releases paid content, and a lamp is of the event's
own family); the own family and an unknown family are refused;
`directions` (optional, at the world:
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
step rule of section 3 step 5). Added on 2026-09-20 (note 25): `age_bound`
(an integer from 1: the largest age a ray may carry, the bound of the
store; on a GameBoard with an open axis twice the flight bound by default, the
age at which every straight ray has left a GameBoard of that diameter,
`world.flight_bound`; required on a GameBoard periodic on every axis, which no
ray leaves; a declared ray's `age` is refused beyond it and a run in which
a ray on the GameBoard carries an age beyond it is refused), and the value
`age` of a table entry's `reads` (the age moment; the clock of that entry
counts it in place of the presence). Added on 2026-09-20 (note 30): per
measured event `span` (three odd integers from 1, `[1, 1, 1]` by default:
the measured event is a body on the set of span_x x span_y x span_z Nodes
centred on its `position`, one record on all of them; the model owner's
principle of the detector as a set applied to the electron, "the electron
of width 3"); at the world `action` (h, an integer from 1, in label units
times Links, absent by default: the quantum of action of the turn by
momentum) and per measured event `phase_by_momentum` (true: the body
turns its phase by its momentum label at every Link it steps, over h;
false by default; the model owner's decision on Bohr, "put it as
parameters outside the GameBoard like the age"; the record carries the
identity `bohr-v1` under `hypotheses` when `action` is declared). Added on
2026-09-20 (note 35; the model owner, "DECIDED: the meeting, M-R"): at the
world `meeting` (true or false, false by default: every paid unit in
transit reads the free crowd of the other numbers at every free-space
Node after the collision and turns toward it by its phase register,
section 3 step 3; refused with a paid family without a phase circle,
which has no register; the record carries `meeting` as declared and the
identity `meeting-v1` under `hypotheses` when it is true; absent, no world
changes by a byte).
Unchanged: `shape`, `boundary`, `ticks`, `K`, `N`, `release`,
`suspension`, `families`, `measured` (`table` with `read`, `measure`,
`rerelease`, `pass` and `phase_window`, since 2026-09-20 with its width
`phase_width`, note 36 (i)), `in_transit` (gains `direction`,
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
only what differs (`tools/migrate_nature_beam_worlds.py` rewrote them; the Bell and
coupling generators emit the trimmed form).

```json
{"law": "beam", "model_id": "two-slits-rays", "shape": [60, 121, 1],
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
nature_beam(store: NatureBeamStore, world: NatureBeamWorld, tables: NatureBeamTables, measured: dict,
           tick: int, record: Record, inverse: bool = False) -> Books
```

and nothing else with law in it. `NatureBeamTables` holds the two pure tables,
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
one Node are bounded by `len(D) x age_bound x N x numbers x contents`, a
constant of the world (until 2026-09-20 `sum_d L_d x N x numbers x
contents`, the age reduced modulo the period; since then the age is whole,
rows of different ages are distinct rows and the bound is the world's
`age_bound`, note 25: the host cost of the whole age); a crowd of
identical units is one row. Fixed
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
components up to 6; `scratchpad architect/nature_beam_tables.py`). Why 1 / sqrt 3 and
not 1 / sqrt 2 on the plane: the flight table is a Beam Law, not of the
GameBoard; 1 / sqrt 3 is the largest speed at which no integer direction in
space ever crosses two Links in one interval ((1, 1, 1) is the bound), and a
plane world (extent 1 on z) uses the same table, so a wavelength is `period x
c` on every GameBoard. The step of the interval is `step_d(tau) = line_d[m(tau)
mod S_1]` if `m(tau + 1) > m(tau)`, else no move; the inverse is `tau - 1`
then the same step subtracted: bit-exact. The flight reads the age modulo
`L_d`, the least period of the pair `(tau mod T_d / gcd(S_1 Q, T_d), m(tau)
mod S_1)`, so the step of an age is a function of `age mod L_d` (the
heading (1, 0, 0): T 110, L 55; (1, 1, 0): T 156, L 39; (1, 1, 1): T 192,
L 3; (3, 1, 0): T 350, L 175). Since 2026-09-20 the age itself is kept
whole on the record (`(direction, age) -> (direction, age + 1)` is
injective, a bijection onto its image; the store's bound is the world's
`age_bound`, note 25); until then it was reduced modulo `L_d`. A rest
direction has S_1 = 0 and never moves.

**The interval**, in this order, each step a bijection on the GameBoard's state
except where marked as the border; the inverse runs the steps in reverse
order with each step's inverse:

1. **Departures become arrivals (the walk).** Every ray with `m(age + 1) >
   m(age)` is created at the neighbour along `step_d(age)` (the wrap on a
   periodic axis, `adjacent_node`), its age advanced (mod L_d) and its phase
   turned by `phase_per_link`; a ray that does not step this interval stays
   at its Node (its age still advances: the age is the flight phase, not a
   self-creation). A ray whose step leaves through an open face reaches the
   face detector (step 4); a ray whose age reaches its family's `lifetime`
   in this advance is read where it arrived (step 4) and then booked on
   the border (step 6). Inverse: age back one, the same step subtracted,
   the phase turned back (a ray at age 0 is at its birth, which has no
   inverse: refused). Rest rays (direction 0, 1) stay. The age is advanced
   whole; the flight table is read at `age mod L_d`.
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
   |D| is not normalised); and, since 2026-09-20 (note 25), the **age
   moment**, `sum amount x age` over the set, split outside and here the
   same way: a first moment in the age, the reading aid of the measured
   event, the external thing, which alone reads the age whole (the GameBoard's
   rules, the flight and the collision, never read it whole; the component
   changes nothing on the GameBoard). Every coupling selects its component by
   the key `reads` (the threshold the scalar, the push the vector, a
   detector may declare the tensor; the clock's count the scalar, or on a
   table entry that reads `age` the age moment, `measured.count_component`);
   the detector's record is the
   every `u_d` has the length Q within 1.35 %, so a fan's flow reads Q per
   unit of amount direction-blind, and on the six headings the moments
   are Q times, Q^2 times, what they were on D; note 23). Every coupling
   selects its component by the key
   `reads` (the clock's count and the threshold the scalar, the push the
   vector, a detector may declare the tensor); the detector's record is the
   square of the first moment of the same reading over the clicked rays,
   taken on the circle's unit vectors (C[phase], S[phase], 0) with their
   amplitudes as weights (the pointer; note 33, the four unifications).
   On the six headings the moments are the slot
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
   class is invariant). **Then the meeting** (since 2026-09-20, under the
   world key `meeting`; the model owner, "DECIDED: the meeting, M-R: an
   event in transit reads the crowd as a body does, a report, not a
   balance"; note 35; `events/meeting.py`): at every Node of free space,
   after the table, every PAID unit present (a row of a family with
   `quantum` h >= 1) reads the free units of every number but its own at
   the Node by the one reading set of step 2 (rest and moving alike), the
   vector moment with the labels as weights, `V_B = sum amount x u_d` over
   the free rows of the family B, and the column sum of its family
   against theirs, `kappa_AB = sum_c epsilon_c c_A c_B` (gravity the
   universal column, so a paid family without other columns reads
   `kappa = -1`: the gravity of the crowd); the target is `t = sum_B
   kappa_AB V_B` (for gravity `-V`, against the flow, toward the source,
   exactly the direction of the push a body takes), and the unit's
   direction is turned by k steps of the arc permutation `pi_t` of the
   direction table toward t, k read off the register the unit already
   carries, its phase: `adv = (|t| + Q // 2) // Q` (the crowd met in whole
   units of Q, the nearest), `total = phase + adv`, `k = total // N`,
   `phase' = total % N`, `|t| = isqrt(t . t)` the exact integer norm; so
   N crowd units met turn the unit by one grain step whatever the spacing
   of the meetings and the phase carries the crowd met modulo N. `pi_t`
   partitions the moving directions into sectors about t (the sign
   pattern of the part perpendicular to t in the frame `e1 = t x a`, a the
   axis of the smallest |t| component, `e2 = t x e1`: the signs of
   `u . e1`, `u . e2` and their difference of magnitudes; the directions
   on the line of t a sector of their own), orders each sector by the
   exact angle to t (the signed cos^2 as a fraction of integers, ties by
   index) and shifts it cyclically by one step toward t, the closest
   wrapping to the farthest; the rest directions are fixed. The free
   units are untouched; two or more paid units at one Node read the same
   V and never each other; content, amount, age and number are untouched;
   the transit momentum line moves by `weight x (u_d' - u_d)` at every
   turn, booked as the `turned` line per family, a report as the free
   push on a body is. Inverse: the same reading of the untouched crowd,
   `k = (adv - phase' + N - 1) // N`, `phase = phase' + k N - adv` and
   `pi_t^-k`, before the inverse table (a bijection of (direction, phase)
   for every fixed crowd). Without the key nothing reads and every world
   is byte-identical.
4. **The measured events' tables and the detectors.** A measured event meets
   the rays that arrived this interval at its Node, per family and number
   other than its own, as today (since 2026-09-20, rule (a) of the
   suspension, the model owner's record 128: only in an interval in which
   its clock owes nothing; a measured event that waits neither releases
   nor reads, its table reading `pass` for every family that interval, the
   arrivals going on as at a Node without a measured event, note 17): the
   threshold on the arrivals (section 5),
   then the `phase_window` on each ray's own phase (no coherent sum: the
   window reads the record; a bundle is now the rays of one number arriving
   in one interval; since 2026-09-20 the window has a width, `phase_width`,
   the w consecutive steps centred on the setting, N / 2 by default, note
   36 (i)), then the rule: `read` (the push taken; the rays go
   on), `measure` (the click: the amount, its content and its label join;
   the border), `rerelease` (the re-emission, section 5), `pass`. **The
   push is ONE signed inner product over the columns** (since 2026-09-20,
   the model owner's "one mechanism for all the laws on the GameBoard"
   and the mathematician's verified form; note 31; `nature_beam.push_form`):
   for a group of a free family B's rays with the label flow `V_B`, per
   axis, `push_A = sum over the columns c of epsilon_c x sign(V E_c n_c) x
   by_clock(age_A, |V x E_c x n_c|, D_c x d_c)`, with `age_A` the
   reader's clock age, the age before the interval's self-creation, at
   which every rate of the law is read (since 2026-09-20, the four
   unifications (4), note 33; until then the age after the frame's
   advance, note 20), `(E_c, D_c)` the
   reader's charge in the column c as the frame read it (the exact
   rational sum over the families it holds of their value per unit of
   content times their content, `Measured.charges`), `(n_c, d_c)` the
   arriving family's value in the column, `epsilon_c` the column's sign,
   every column floored on its own off the reader's clock and never summed
   before the floor; the first column of every family is `gravity` (the
   value 1, the sign minus: its term is `-M_A V_B` exactly), the second
   `charge` (rho, the sign plus: its term is the electric part below), and
   a declared column (the strong force, the sign minus) is a third term of
   the same sum, not a term of the code. On the two built-in columns this
   is the form landed the same day, integer by integer (the mathematician:
   11 945 pushes of the registered worlds, 0 unequal): **ONE bilinear
   form** over the arriving rays (the model owner's proposal 2, admissible
   with the reviewer's two corrections; section 10, note 20): `push_A =
   sum over the rays of kappa(A, B) . V_B`, with `V_B`
   the label flow of the rays, the vector moment of `read_arrivals` with
   the labels as weights (`amount x u_d` for a free family, `content x
   amount x u_d` for a paid one, the unit vectors of section 2), and
   `kappa(A, B)` =
   `M_A x (rho_A rho_B - 1)` for a free family's rays, ONE product per
   arriving free ray (the model owner's decision of 2026-09-20: charge is
   per unit of content of a family, note 28; `nature_beam.push_form`):
   M_A the reader's content as the frame read it at the start of the
   interval (`frame_content`, the same for every family's rays whatever
   the family order: a click of the interval joins the content the next
   frame reads; the orchestrator's D1 on the architect's B3, 2026-09-20,
   note 27), rho_A and rho_B the reader's and the arriving family's
   charges per unit of content, the pairs (n_A, d_A) and (n_B, d_B) as
   declared; formed in integers as the gravity `-M_A V_B` plus the
   electric part taken as the whole part off the reader's clock by the
   declared pairs, `sign(V n_A n_B) x by_clock(age_A, |V x n_A n_B x
   M_A|, d_A d_B)` per axis, which equals the earlier `sign x
   by_clock(age_A, |V q_A q_B|, M_B)` integer by integer wherever q_A =
   rho_A M_A and q_B = rho_B M_B were integers (the same rational floored
   at the same clock; no divisor can be 0); and `+ 1` for a paid ray (its
   label already carries h s). Every input is the reader's or the
   arriving family's key; nothing is on the record but the ray's number
   and nothing is looked up by number. A detector Node's record (section 5) is written from the
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
   the owed count read off the clock from what the clock counted over
   every ray of another number at its Node, `by_clock(age_A, k n, d)`: k
   the presence, or on a table entry that reads `age` the age moment
   `sum amount x age` of that family (note 25: the clock beside a mass
   then reads M / r in space, the push keeping M / r^2). Every new ray:
   `age` 0, the emitter's phase, its number. A measured event on a set of
   Nodes (`span`, note 30) releases at every Node of its set with whole
   units only: each row born is apportioned whole over the set in its
   fixed order, the leftover to the Nodes counted from `age mod w`, so
   the total released is the content's whatever the width. The step of a measured event by its momentum: as the
   other change leaves it (no merge; refused onto an occupied Node, and
   since 2026-09-20 the refused step is a contact read through the
   occupant's table, note 31 (ix): the occupant's entry for the body's
   family, `measure` by the keys, hands the body's momentum component on
   that axis to the occupant, `rerelease` returns it, `read` and `pass`
   leave the labels as they were; a
   body on a set steps as one, note 30; a body that declares
   `phase_by_momentum` in a world with `action` turns its phase at the
   Link it steps by the difference of two floors of k x |p| x N / h, k the
   count of Links the step rule gives at its age, note 30 (ii)), with
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
   by_clock(age, n, k)`. Since 2026-09-20 (note 17 as amended, the step
   drive) the count is the whole part of the SIGNED distance the momentum
   has driven, kept on the body's record as `drive` per axis (`drive +=
   p` at every self-creation in which it may step, one Link on the + side
   and `drive -= Q x S x M + |p|` at or beyond +D, one Link on the - side
   and `drive += Q x S x M + |p|` at or beyond -D; signed since record
   126 of the same day, the first form's `|p|` being history), the same
   integers at a momentum of one sign as the whole part off the clock
   (implementation notes 15 and 17; `tests/test_push_width.py`,
   `tests/test_step_drive.py`).
6. **The border `lifetime`; then merge identical rows and sort by Node.**
   Since 2026-09-20 (note 31 (vii)) every row of a family with a
   `lifetime` whose whole age is at or beyond it after this interval's
   walk (read in step 4 where it arrived at a measured event; unread in
   free space) clicks on the border `lifetime`: its amount, content and
   label booked as an open face books an escape (the ledger's lifetime
   lines, summed into the escaped lines beside the faces), one `click`
   record per row naming the border, the border's record the square of
   the coherent pointer of what clicked, per family; then the rows leave
   the store. Local (the row's own age against its family's key), fixed
   work (one comparison per row), no draw and no register: the one-way
   border of the interval beside the click, so a GameBoard with a family
   of a lifetime has no inverse interval (refused naming the family and
   its lifetime). The merge is a bijection (a permutation of rows and a
   sum of interchangeable units).

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
returning on a periodic GameBoard, head-on beams) and there they are the only
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
at load from this rule (`nature_beam_tables.py` is the reference; the implementation
ports `collision_table()` and `class_key()` into `NatureBeamTables`).

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
uncertainty, and the reading, not the GameBoard, is what is uncertain).
Per interval and per family, a detector's set (its declared `positions`;
a measured event outside every declared detector is a detector of one
Node with the default reading) reads the arrivals of every number but
each Node's own at all its Nodes as one set: the **threshold**, under
`beam` on the amount summed over the whole set and under `wave`, since
2026-09-20 (note 32; issue #359 step A), on the square of the coherent
pointer of the set's arrivals in units of one ray, the nearest integer to
(X^2 + Y^2) / 2^26 (`nature_beam.pointer_units`, 2^26 the square of one
unit's pointer at phase 0: one unit at any phase reads 1, a rays in phase
a^2, rays that cancel 0, so a pair in antiphase passes whether or not a
window is declared; no memory between intervals; the pointer gate is the
click's, the entries that absorb, and a `read` entry keeps the amount gate
under both readings, note 32), a set below it passing
at every Node of it with a `pass` record naming `threshold`; then the
**reading** the detector declares (`reading`: `wave` by default since 2026-09-20, the
model owner's decision, "on the GameBoard a ray, in the world a wave"; or
`beam`, declared; section 10, notes 24 and 29):

- `wave`: with the rays the set clicks this interval (after the threshold
  and the window; `measure` only), `A_u = 32 x amount_u` (note 3) and the
  1/256 tables `C`, `S` of `core/phase.py`, the coherent pointer over the
  whole set `(X, Y) = (sum A_u C[phase_u], sum A_u S[phase_u])`, since
  2026-09-20 the first moment of the one reading taken on the circle's
  unit vectors `(C[phase], S[phase], 0)` with the amplitudes as the
  weights (`nature_beam.coherent_pointer` through `read_groups`; note 33),
  and the record `X^2 + Y^2`, an integer added to the detector's one
  `record` (per detector, cumulative, never per Node). The set's phase is the
  pointer's nearest step (`nature_beam.pointer_phases`: the step of the
  circle whose table entry is nearest in direction, the least
  `|X S[k] - Y C[k]|` among the k with `X C[k] + Y S[k] > 0`, exact
  integers; a zero pointer has no phase). The **window** of a Node's
  entry reads the set's phase (the pointer of the arrivals the threshold
  admitted), not each ray's own: the set is admitted or passes as one.
  After a click the set's phase is **returned to the GameBoard** (the model
  owner: "the detector must also return to the GameBoard the information it
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
  never fringes; rays, section 3). It is the default: a detector that
  declares no `reading`, and a measured event outside every declared
  detector, reads `wave`.
- `beam` (declared; the model owner's "only events"; the default from
  2026-09-19 to 2026-09-20): a rule on whole
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
`32 x 257 x (the amount clicked)`: the pointer was summed in the int64
register while the amount a detector Node (or a face) clicks of one
family in one interval was within `(2^62 - 1) // (32 x 257)` =
560759486676481 (`POINTER_AMOUNT_BOUND`, 2^48 inside, 2^49 beyond; the
constant is deleted since note 33) and, since the four unifications
(2026-09-20, note 33), it is the first moment of the one reading over
the circle, taken in the register where the reading's own bound holds
for its table (`reading_fits`: 32 x amount x 256^2 x the rows of the
group within 2^62 - 1, the second moment's bound, which the pointer
does not read but the one table forms) and in Python integers beyond
it (`coherent_pointer`, `moment_table(exact=True)`: the same table); the
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
whose step leaves the GameBoard clicks there, its amount, label and content
booked as escaped, its phase on the click record; the face's record is the
same square; the momentum that left is booked per family since 2026-09-20
(note 32; issue #360: until then one vector per face and the world's
total written into every family's escaped line of `run.json`). A periodic
axis has no face.

**The border `lifetime`** (since 2026-09-20, note 31 (vii)). A family that
declares a `lifetime` L makes the GameBoard a detector without Nodes named
`lifetime`, listed after the faces (`face_detectors()`, `detectors()`,
the run's record): a ray of the family whose age reaches L at the end of
its walk clicks there at step 6, booked as a face books an escape (the
amount, the content, the label, the square of the pointer per family),
and the books' escaped lines sum the faces and the border. The border
is where the click is, not a place: the click record names the Node the
ray was on.

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
`test_nature_beam_clock.py`), `test_phaseless_family.py` (the diagonal weights; the
free push by the flow moves to `test_nature_beam_readings.py`),
`test_reversible_detector.py`, `test_reversible_detector_world.py`, the
mixing refusals of `test_integer_bounds_of_measured_and_emission.py`.
Examples: `examples/events/*.json` rewritten as NatureBeam worlds (`one_content`
and `two_contents` release on the six headings; `two_slits` and `one_slit`
as section 2; the `bell/` and `coupling/` generators re-emit `"law": "beam"`).

Documents: ENGINE.md is replaced by this document (the per-axis topology and
the record sections move here, shortened; the wave's paragraphs go to
MIGRATION); TERMINOLOGY gains ray, direction, rest slot, collision, record,
and marks event in transit as "a ray"; EXPERIMENTS re-registers series C and
Bell A2 under `beam-v1` (section 8) and keeps the `events-v1` readings as
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
| `test_nature_beam_flight.py` | the lone unit, every heading, every declared direction of the example, 150 intervals | straight on its digital line, direction and phase unchanged (`phase_per_link` 0), one Link at most per interval |
| | flight isotropy: 1000 intervals on (1,0,0), (1,1,0), (1,1,1), (3,1,0), (5,2,1) | Euclidean distance^2 within 2 % of 1000^2 / 3 for every direction; equal flight time to equal Euclidean distance within one interval |
| | the flight table | `T_d >= S_1 Q`; `m(tau + 1) - m(tau)` in {0, 1}; `L_d` periods as listed in section 3 |
| `test_nature_beam_collision.py` | the table | 6561 states; `INV[FWD[s]] = s`; the class invariant; the 20 orbits with the sizes of section 4; a crowd slot never changes |
| | conservation | for every moving state the amount and the heading sum are equal before and after |
| `test_nature_beam_bijection.py` | periodic 8 x 8 x 4, 300 records incl. head-on pairs and rest units, 50 forward then 50 inverse intervals, no measured event | the sorted store bit-exact; the state differs at the turning point |
| `test_nature_beam_detector.py` | two rays of amount 1 in phase, then in antiphase, arriving in one interval at a detector of threshold 1 | record 4 x 32^2 x 256^2, then 0; the amount 2 and two clicks both times |
| | the threshold under the one reading set | a bundle of 1 at threshold 2 passes with a `pass` record; rest units count |
| `test_nature_beam_reemission.py` | one ray of amount 3 into a `rerelease` Node with three directions | three rays of amount 1, the arriving phase, age 0, the re-emitter's number; recoil = label in - labels out; books closed |
| | the face click | a ray stepping off an open face: one click on the face detector, escaped amount 1, the record its square |
| `test_nature_beam_clock.py` | a lamp of turn s on two directions | cost and label `quantum x s` per unit along each direction; the owed count off the clock unchanged (reference) |
| `test_nature_beam_worlds.py` | the two slits of section 2 on 60 x 121 x 1, 500 intervals | the interference term V(y) of the screen's record correlates with the two-source Euclidean cosine at lambda = c x period above 0.9 (rays measured 0.969); the plain count additive to the unit |
| | Bell | the ten A2 worlds under `"law": "beam"`: S = 2 exactly, no-signalling exact |
| `test_nature_beam_world_parsing.py` | refusals | `"law": "events"`, `dynamics`, `headings`, a non-primitive direction, a component beyond P, a label beyond 2^62 - 1, `phase_per_link` outside 0 .. N - 1, each named |

## 8. Independent expectations for the re-registered readings

Pinned before implementation, from the prototypes (rays and rays2 measured on
the plane) and the argument that every ray present at a Node is leaving it
(presence = |flow|):

| Reading | Under `events-v1` (registered) | Under `beam-v1` (expected) |
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
3. `events/nature_beam.py` (new; engine owner): `NatureBeam`, `NatureBeamStore`,
   `NatureBeamTables` (`flight_table(directions)`, `collision_table()`, both pure,
   generated and checked at load), `nature_beam(...)` with `inverse`.
4. `events/world.py` (schema owner): `"law": "beam"`, `directions`,
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
loop in rays2), so a GameBoard with one ray per Node breaks even and a dense
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
   n^2 times that (the pointer of n equal amplitudes).
4. **Home keeps the arriving phase and content.** What comes home is
   created again with the phase and the content per unit it arrived with
   (as the re-emission does), not re-stamped by the clock; the books'
   absorbed and released lines carry it exactly.
5. **A ray below the threshold or outside the window passes with a
   `pass` record** naming `threshold` or `window`; a set at the threshold
   clicks row by row (one `click` record per row, the amount on it) and the
   window reads each row's own phase, no coherent phase of the set (the
   record is the pointer's square; the window is a gate on the record).
6. **The inverse interval exists only without a measured event**: with one
   on the GameBoard `inverse_step` refuses (the click, the release and the home
   are the one-way border and no inverse of them is defined); the
   bijection test runs on a GameBoard of rays alone.
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
12. **A ray may be declared on a GameBoard without a measured event** (the
    in_transit `number` bound is max(1, the number of measured events)),
    so the bijection and the collision tests run on rays alone.
13. **Every ray steps at its first interval**: the flight table's first
    walk is at tau = 1 for every direction (T_d >= S_1 Q), so a declared
    ray at age 0 crosses its first Link in the first interval and a ray
    released at tick t first walks at t + 1.
14. **The registered readings** (section 8) are marked measured against
    expected in EXPERIMENTS.md; the far-field ring means of a six-heading
    source follow the GameBoard ring's Node count (the rings at r = 16 and
    r = 20 both hold 112 Nodes) and fall outside the ±10 % expectation,
    registered and not moved; the fan the expectation was pinned on is the
    owner's decision to run.
15. **The table from the keys; the kind from the quantum** (the model
    owner, the night of 2026-09-19, "I approve 1 and 3", Highlights 5.4;
    `tests/test_default_table.py`). `world.default_table(families)` is the
    one function that gives every measured event its table (section 2);
    `FamilyDefinition.free` is `quantum == 0`; the constraints the parser
    kept are expressed through the quantum and not widened: a charge is
    refused on a paid family (h >= 1; lifted on 2026-09-20 by D-1, note 36
    (ii): a paid family's whole charge per unit of amount on the charge
    line), a lamp on a free one, a free unit
    carries no content and its label is `amount x D` (the mathematician's
    note that "paid => q = 0 and free => h = 1 are decisions, not
    necessities" is recorded; the first was acted on by D-1). `quantum` is required: a
    default would be an implicit kind. The record (`run.json`) carries
    `quantum` per family and no `kind`. Every example world parses to the
    same `NatureBeamWorld` as before the change (checked structure by structure
    over the 39 worlds), and the Bell and coupling runs are unchanged
    record by record (VALIDATION.md).
16. **The moments replace the slots** (the same decision; `tests/
    test_nature_beam_readings.py` (a)). `read_arrivals(vectors, amounts, keys,
    size)` takes the moments of section 3, step 2, exact integers, with
    the normalisation `tensor = 3 x M2 - tr(M2) I` for the second moment
    `M2 = sum amount x D D^T` (the trace removed times the number of
    dimensions, so no division); the `Moments` holds the six entries of
    `M2` and forms the tensor on demand. On the six headings the moments
    equal the slot decomposition exactly (the old `(p_x + p_y - 2 p_z,
    p_x - p_y)` being `-T_zz` and `(T_xx - T_yy) / 3`); under the 48
    signed axis permutations the scalars are fixed, the vector rotates and
    the tensor is conjugated. What this changes on the GameBoard: only the
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
    that uses it is series D in EXPERIMENTS.md). **Amended on 2026-09-20,
    the step drive (superseded for the moving body only: record 107, the
    findings, and record 108, the model owner's decision, "yes; let him
    give a generic solution if he can"; the owner on series G2's finding,
    "1 and 2 are very important for a solution and a new run"; change 2,
    the push at the relative speed, not built as proposed, record 110;
    the physicist's design RULES.md section 1 (docs/designs/hubble_stars/ on branch `claude/series-g2-stars`); `tests/test_step_drive.py`).**
    Read at the current momentum, the whole part `floor(age |p| / D)`
    stalled a body for tens of intervals under a falling momentum and then
    stepped it at every interval (series G2: a star at 0.019 Links per
    interval stepping five Links in six intervals, faster than the ray;
    the Links made equal to age x v_now). The count is now the whole part
    of the distance the momentum has driven: the body's own record
    carries per axis one bounded integer `drive_a` (0 at the start, as
    its age is on its record and nothing at a Node), and at every
    self-creation in which it may step `drive_a += p_a`, the SIGNED
    component; when `drive_a >= Q S M + |p_a|` it steps one Link on the
    axis's + side and subtracts that, when `drive_a <= -(Q S M + |p_a|)`
    one Link on the - side and adds it (record 126 of 2026-09-20, the
    signed drive: the first form accumulated |p_a| and took the direction
    from the sign at the fire, so a deuteron's neutron, charged by
    fourteen intervals toward the proton, stepped away after the contact
    handed it the proton's component; "the distance the momentum has
    driven" is the signed sum, and the |p| form equals it only while the
    momentum keeps one sign). With a momentum of one sign the step fires
    exactly when `floor(n |p| / D)` increments (the drive is the signed
    remainder of that division): every world whose bodies take no push
    replays byte-identical, and every world whose momenta keep their sign
    on every axis steps as under the first form; under a push the motion
    follows the momentum's signed history at every self-creation, a
    reversal first cancelling what was driven the other way, and never two
    Links fall in one interval (one D is subtracted per self-creation; a
    residual earned at a larger momentum fires at the following
    self-creations, one Link each, the distance the momentum had driven).
    The drive of every axis advances at every such self-creation, and the
    frame's order stands as before, x before y before z: a later axis
    whose drive reaches its D in the interval of an earlier axis's step
    (made, refused or an escape) loses that Link, its D subtracted,
    nothing carried, so a body with momentum on two axes at a constant
    momentum steps exactly where it did. The turn by momentum (note 30
    (ii)) reads its k0 off the record's count of the rule's fires on the
    axis, `axis_steps` (a lost or refused step counted, as the whole part
    off the clock counted it), the same number at a constant momentum.
    The count primitive is `core.integer.by_drive(drive, rate, D)`, the
    whole part of an accumulated signed rate on the reader's own record,
    the count -1, 0 or +1 (the model owner's record 108, "a generic
    solution if he can": one primitive every count against a rate could
    use, equal to `by_clock` wherever the rate is constant and of one
    sign); the step reads it now, and the
    clock's turn, the owed count, the release and the lamp keep `by_clock`
    with their docstrings saying they are the same count where the rate
    is constant, so nothing registered outside the pushed-body worlds
    moves. `run.json`, `state.json` and the `step` line carry `drive`; a
    declared `drive` is refused as an unknown key. Re-registered under it, the old
    integers kept as history in TEST_EXPECTATIONS.md: the bodies pushed or
    handed a momentum in `tests/test_contact.py` (a), (d), (e),
    `tests/test_nature_beam_clock.py` (d), `tests/test_paid_charge.py` (d)
    and `tests/test_nucleus_readings.py`, each one self-creation later
    than the count off the clock stepped it (a body that receives a
    momentum begins its drive at 0 instead of stepping off its age). "No
    remainder is kept" above stands for the clock, the release, the lamp
    and the owed count, which read a rate against an age no push changes.
    **Rule (a) of the suspension (2026-09-20, the model owner's decision
    on the third-law gap of record 126, record 128: "a measured event
    whose clock owes an interval in that interval neither releases nor
    reads: a message enters a body only at its self-creation; to wait is
    not to communicate in either direction").** Until this rule a waiting
    body released nothing and read everything: it took the push of every
    row arriving at its Node while its partner, receiving none of its rows,
    took none, so a bound pair gained one push net per wait. Under the
    rule the table of a body that owes this interval reads `pass` for every
    family (`nature_beam`, the rule matrix of step 4 read off the frame's
    `creating`): no push, no click, no re-emission and no transformation
    by a click; the rows that arrive at its Node are not consumed and go on
    as at a Node without a measured event, so the books stay exact and the
    walk a bijection; a deferral of the click to the next self-creation
    would need a register at the Node and is not this law. Its clock still
    counts the presence at its Node, a reading of what is there and not a
    consumption: a body that measures (`measure`) and waits therefore
    counts, at the self-creation after its wait, the rows it did not
    consume while they dwell at its Node beside the new arrivals
    (`tests/test_nature_beam_clock.py` (e): the probe of k = 8 counts 16
    after a wait and owes 4 where it owed 2), the consequence of not
    consuming them, registered as read. Under `suspension` 0 nothing waits
    and every world is byte-identical; the worlds with a suspension (the
    clock worlds of series E, G and J, the catalog's clock and neutron
    star, the coupling's item 6) are re-read with dated lines. On the
    third law: a wait now removes one read and one release, and the pair's
    momentum sum is unchanged by an isolated wait (the waiter misses one
    push, the partner misses the waiter's release one flight later) but
    not when the partner waits at the interval the missing release would
    have arrived (`tests/test_step_drive.py` (g): the register's deuteron
    under a suspension, the proton waiting twice and the neutron once, the
    sum -P at the end); the gap is narrowed to that coincidence, not
    closed, and is recorded for the owner.
18. **The one label; no collision at a measured event's Node** (the
    physics-rule reviewer's F1, blocking, and the model owner's decision on
    its case (c), the night of 2026-09-19; `tests/test_nature_beam_push.py` (h),
    `tests/test_nature_beam_collision.py` (d)). Until this note the push read the
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
    Nodes; `tests/test_nature_beam_bijection.py` passes as before) and the
    registered runs are unchanged record by record (no collision acts in
    them and their arrivals are their directions; VALIDATION.md).
19. **The record exact, never refused** (the reviewer's F2, corrected
    twice; `tests/test_nature_beam_detector.py` (e), `tests/test_nature_beam_worlds.py`
    (e)). The finding: the record's amplitude products were unchecked
    int64 (an amount of 2^52 recorded 0 silently) and the design's bound
    `256 x 32 x isqrt(sum amount)` was stale (the amplitude is linear,
    note 3). The night's correction refused the run when a detector Node
    or a face clicked more than the affordable amount
    `RECORD_AMOUNT_BOUND` = isqrt(2^62 - 1) // (32 x 257) = 261123 of one
    family in one interval; the same night `examples/events/two_contents.json`
    (two fixed contents of 2^24 at `release` [1, 128] on an open 21^3
    GameBoard), which had run 200 intervals before the bound, was refused at
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
    verdict "admissible with two corrections"; `tests/test_nature_beam_push.py` (a)
    to (g)). (The two columns of this note are deleted since 2026-09-20,
    the factor being the family's charge per unit of content: note 28.) `push_form` computes `push_A = sum kappa(A, B) . V_B` (step
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
    the frame's advance, frozen while it is owed (until 2026-09-20: since
    the four unifications (4), note 33, the columns are floored at the
    clock age like every other rate). The reviewer's F7 is
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
    collision the Nodes the same way. (ii) The dense readings of the GameBoard
    (`count`, `flow`, `presence`, `per_port`) are diagnostics, decomposed
    on request from the rows the walk left (`GameBoardDiagnostics`, `ArrivalRows`)
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
    released less what left; `NatureBeamSimulation.recount()` counts the three
    lines from the rows on request and `tests/test_nature_beam_books.py` asserts
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
    |D| <= 8, about 10 x at |D| <= 16); `tests/test_nature_beam_label.py`). The
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
    (`GameBoardDiagnostics`, the reading at a measured event, step 2), so a fan's
    flow reads Q x q direction-blind; the zeroth moment is unchanged.
    What else changes: the label flow's bulk bound is the first
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
    coefficient no longer alternates (`test_nature_beam_push` (e): 96 per tick
    where 2, 1 alternated), the floor resolving 1 / Q per unit. Every
    pinned test's momentum integer is x 64 (the fan fixtures on u_d;
    TEST_EXPECTATIONS lists the re-pins; MIGRATION the units).
24. **The detector's set, its two readings and the phase returned** (the
    model owner, 2026-09-19, three decisions of the same day: the
    detector a set with one record, "the detector must also return to
    the GameBoard the information it received", and the key `reading` with
    `beam` the default and `wave` the imported law; section 5;
    `tests/test_nature_beam_detector.py` (f), (g), (h)). The decisions the
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

25. **The age whole, read by the measured event; the clock beside a mass**
    (the model owner, 2026-09-19, Highlights 5.4, "the clock beside a mass
    ... Go for it", implemented 2026-09-20; `tests/test_nature_beam_age.py` (a) to
    (e); the placement by the owner's instruction: "the age reading must
    live in an external place in the code, outside the GameBoard's law"). The
    accepted price of section 8 (the clock's count reads the presence, M /
    r^2 in space, not Einstein's M / r) is paid by a reading, not by a rule
    of the GameBoard: the ray's age, the count of intervals since the measured
    event that created it (a birth or a re-emission; a collision is a
    permutation and cannot reset it), is on the record and travels with
    it, so a clock reading the amount-weighted age of its arrivals reads
    (M / r^2) x r = M / r while the push keeps reading the flow, M / r^2:
    Einstein's pair from two readings of the same rays, no estimator,
    fixed work, additive over sources. What changed: (i) the store keeps
    the age WHOLE (`NatureBeamStore.age`, the walk advances it by one; a rest ray
    keeps it; a re-emission and a birth start at 0); the flight reads it
    modulo the direction's period, `flight.steps[direction, age mod L_d]`,
    and the collision never reads it, so the GameBoard's step is unchanged by
    the whole age (test (e): the same run with the ages reduced from
    outside the law after every interval gives the same Nodes, directions,
    phases, amounts and contents at every interval; the bijection echo of
    `test_nature_beam_bijection` passes as before, its all-periodic world
    declaring `age_bound`). The host cost: rows of different ages no
    longer merge, so the store's bound is `len(D) x age_bound x N x
    numbers x contents` in place of `sum_d L_d x ...` (section 3); on the
    registered worlds the row counts are unchanged in practice (a beam
    holds at most two rays per Node, of different ages either way) and
    `state.json` now records the whole age. (ii) The one reading
    `read_arrivals` gains the age moment (`Moments.age_outside`,
    `age_here`, `age`; the `ages` argument, zero without it; the bound
    check covers `amount x age`), the value `age` of `reads`, and the
    record of a `read`, `click` or `rerelease` on such an entry carries
    it. The age is read whole only by a measured event, the external
    thing; this component is a reading aid of the detector and changes
    nothing on the GameBoard. (iii) What the clock counts is selected on the
    measured-event side, `measured.count_component(reads)`: the age moment
    on an entry that reads `age`, the presence on every other entry (the
    default: every world without the key reads the same, integer by
    integer); step 4 reads both over every ray of another number at the
    Node (rest and moving alike, as the presence) into `Measured.presence`
    and `Measured.counted`, and the frame's `_suspend` owes
    `by_clock(age_A, counted x n, d)`. (iv) The bound of the age, the
    world key `age_bound`, and the rule at the bound. Three rules were
    weighed: saturation (many-to-one, not a bijection: rejected); a click
    at the bound (a one-way gate like the face click: admissible, but a
    detector without a Node and a new escaped line of the books, in the
    detector's area being changed concurrently); and the refusal, chosen:
    a row whose age passes `age_bound` refuses the run at the end of the
    interval with `OverflowError` naming the key, as every other bound of
    the law does, nothing on the GameBoard changed, so the bijection holds
    exactly up to the refusal and the world must be small enough or
    declare its bound. The default on a GameBoard with an open axis is twice
    the flight bound, `world.flight_bound(shape, D)` = the largest over the
    moving directions of `ceil(ceil(D_M / S_1) x T_d / Q)` with `D_M = X +
    Y + Z - 2` the longest Manhattan flight on the GameBoard (inside and out;
    the least tau with m(tau) >= M is at most ceil(M T_d / (S_1 Q))): the
    age at which every straight ray has left the GameBoard, doubled as the
    slack of one collision or one wrap of a periodic axis (a head-on pair
    parked at rest keeps its age and flies again; a ray along a periodic
    axis never leaves). On a GameBoard periodic on every axis no ray leaves,
    so the key is required and refused if absent (the bijection, flight,
    collision and push tests' periodic cubes declare it). The parser
    refuses a declared `age` beyond the bound; `run.json` records the key.
    (v) The clock's count with the age moment on a bar (test (c)): a
    reader three Links from a source whose rays dwell two intervals at its
    Node counts 5 + 6 = 11 over a presence of 2 and owes `by_clock(age,
    11, 4)` in place of `by_clock(age, 2, 4)`. The registered readings of
    section 8 are unchanged (the scalar is the default); the experiment
    that reads the pair in space is series E in EXPERIMENTS.md (the
    redshift of two clocks under the age reading). Recorded as an idea of
    the owner, not implemented: a ray sent back toward its source could
    count its age down and be measured where it reaches zero.
26. **The label's product checked before it is formed** (the architect's
    B1, blocking, 2026-09-20; `tests/test_nature_beam_label.py` (c), (d)). Until
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
27. **M_A is the content the frame read** (the architect's B3, blocking;
    the orchestrator's D1, 2026-09-20; `tests/test_nature_beam_push.py` (j)).
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
28. **Charge per unit of content; the push one product; the record's two
    columns deleted** (the model owner's decision of 2026-09-20,
    Highlights 5.4; it resolves the architect's B2 by dissolving its
    divisor; `tests/test_nature_beam_push.py` (a) to (e), (i), (k), (l),
    `tests/test_nature_beam_world_parsing.py`). The family key `charge` is the
    charge per unit of content, rho, declared as an integer or a pair
    `[n, d]` as `suspension` is (an integer c is `[c, 1]`; d = 0 and a
    part that is not an integer are refused; a paid family's rho must be
    0); a measured event's charge is rho x its content, a report
    (`Measured.charge`, the reduced pair; `state.json` and the books'
    `charge` line carry the pair), and the per-event key `charge` is
    refused naming MIGRATION. The ray's record loses `charge` and `mass`:
    the family suffices, so `NatureBeam`, the store (seven columns and
    `arrival`), the merge's identity (six fields) and `state.json` carry
    nothing of the emitter but the number. The push is ONE product per
    arriving free ray (`push_form`): `push_A = M_A x (rho_A rho_B - 1) x
    V_B`, the gravity -M_A V_B plus the electric part off the reader's
    clock by the declared pairs, `sign x by_clock(age_A, |V n_A n_B M_A|,
    d_A d_B)` per axis; on every series 7 world it equals the earlier
    `q_A q_B / M_B` form integer by integer (the same rational floored at
    the same clock; the six worlds' 181 or 185 `read` records, `pushed`
    and momenta equal, VALIDATION). The six series 7 worlds now declare
    two free families with their pairs (`q` the source, `p` the probe:
    2^23 on 2^24 is [1, 2], 2 on 1 is [2, 1], 2 on 4 is [1, 2];
    `examples/events/coupling/make_worlds.py`), since one charge per unit
    of content is one family; `tools/migrate_nature_beam_worlds.py` moves a
    per-event charge to its family as the reduced pair and refuses a
    family whose events imply two. A re-emitted free ray is its family's
    ray (the orchestrator's D2: it takes the re-emitter's number and
    keeps its family, so it pushes by its family's rho; the re-emitter
    of another family gives it nothing, and B2's zero divisor cannot
    arise: (k)). The electric push is proportional to the reader's
    content as the gravity is, the equivalence principle for the electric
    push, pinned in (l).
29. **`wave` is the default reading** (the model owner's decision of
    2026-09-20, Highlights 5.4, "on the GameBoard a ray, in the world a
    wave"; `world.DETECTOR_READINGS` = ("wave", "beam")). A detector that
    declares no `reading`, and a measured event outside every declared
    detector (a detector of one Node), reads `wave`: the coherent pointer
    over the set, its square the record, its nearest step the phase the
    window reads and the phase returned; `beam` is a declared option
    (note 24 (v) and (vi) describe it as the default of 2026-09-19).
    What moves: a windowed detector met by rays of different phases in
    one interval reads the pointer's phase, not each ray's own
    (`tests/test_nature_beam_readings.py` (d): 2 units at phase 0 and 1 at phase
    32 point to 0, outside the window 32, and all pass, where `beam`
    clicked the one at 32; `tests/test_nature_beam_collision.py` (d) declares
    `beam` on its windowed taker to keep the case of note 18, a zero
    pointer having no phase); the wall of the two-slit worlds records the
    square of what it absorbs (its record is read by nothing). Unchanged:
    the Bell worlds (one ray per interval per counter: the pointer of one
    ray at phase p reads p, every click and pass identical, S = 2 exactly,
    `tools/bell_chsh.py` 326 criteria passed), the two-slit screens and
    the Heisenberg worlds (declared), series C and D (no detector).
30. **A body on a set of Nodes with one record, and the turn by momentum:
    Bohr as parameters outside the GameBoard** (the model owner, 2026-09-20,
    Highlights 5.4: the physicist's report on hydrogen, the seven
    proposals, and "DECIDED (the owner): On Bohr, go, and put it as
    parameters outside the GameBoard like the age"; the placement rule: the
    turn is a declared parameter of the measured event, the external
    thing, read by it from its own record with no memory at a Node; the
    rays' flight and collision are untouched; a world without the keys
    reads the same integer by integer; `tests/test_nature_beam_body.py` (a) to
    (f)). Two features on the measured-event side, nothing on the GameBoard.
    **(i) The body on a set** (proposal 1, "the electron of width 3"; the
    physicist measured 0 to 8 rays per shell around a mean of 4 at one
    Node of a 2616-direction fan, the grain that broke the orbit). A
    measured event declares `span`, three odd integers from 1 (`[1, 1,
    1]` by default): it is a body on the block of span_x x span_y x
    span_z Nodes centred on its `position` (`world.body_nodes`, the
    offsets ascending x, then y, then z: the fixed order of the set), ONE
    record on all of them (age, phase, momentum, content, amount, owed
    count) exactly as a detector is a set with one record (note 24). The
    form chosen: a centre with a span, not a list of positions, so that
    `position` keeps its meaning (the reported place, what a detector
    names, what the step moves) and the set is one key of three
    integers; a list would have needed a second reference Node and would
    have allowed shapes no orbit needs. What the set does: every Node of
    the body maps to it (`node_event` in step 4), so the rows at any of
    its Nodes are its arrivals and the one reading set of BEAM_LAW is
    summed over its Nodes, per Node ("everything at the Node but the
    reader's own number, including here"): the threshold reads the
    amount arriving over the whole set, the clock's count the presence
    (or the age moment) over the set, the push the label flow over the
    set (a ray crossing w Nodes of the body along its line is read w
    times, once at each Node it enters: the body's reading is the sum of
    its Nodes' readings, so its push is about w times one Node's at the
    same content, a declared width like the detector's, which the orbit
    derivation of series H takes into account); the click's content and
    momentum join the one record; the `click`, `read`, `pass` and
    `record` lines name the body's `position` as their `node` ("here, in
    one of these"); no collision acts at any Node of the set (note 18
    applies to every Node); own-number rays arriving at any Node of the
    set are home. The release: each row born at a self-creation (a free
    release, a lamp's, what came home or is re-released) is apportioned
    whole over the body's Nodes in their fixed order with equal weights,
    the leftover units to the Nodes counted from `age mod w`
    (`apportion_whole`, the tie rule of the re-emission over the
    directions): the total released is the content's release whatever
    the width (the flux of a body of content M is M's, the equivalence
    kept), no Node is favoured over w self-creations, and the books
    balance (the shares sum to the amount, every share keeps the row's
    content per unit and phase, the labels' sum is the same recoil); the
    rule chosen over "the full amount at every Node", which would have
    made a body of w Nodes emit w times its content's flux. The step
    (`_move`): the centre steps one Link by the step rule and the set
    moves with it, refused when any Node of the moved set holds another
    measured event (the body's own Nodes overlap the moved set and do
    not refuse it), the whole body clicking on the face detector when
    any of its Nodes would leave the GameBoard through an open face, every
    Node wrapping on a periodic axis; the inverse interval is refused
    with a measured event on the GameBoard as before (note 6). Parsing: a
    span must be odd (a centred body), at most its axis's extent, the
    body inside the GameBoard on an open axis at the start, two measured
    events never share a Node, and a detector names a body by its
    `position` (a Node of the body that is not its centre is refused by
    name). A set of one Node is bit-identical to the measured event of
    2026-09-19: the same rows, records and books on the world of test (a)
    with the key absent and with `[1, 1, 1]` declared. `run.json` carries
    `span` per measured event under `numbers` and in the measured
    events' states, `state.json` the same key.
    **(ii) The turn by momentum** (proposal 5, the owner's placement
    rule; the physicist's "Bohr's radii would need the body's phase to
    turn by its momentum label per Link stepped"; the orchestrator's
    answer, flagged: a measured event's phase turns only by its own
    clock, content over K per self-creation, by time alone, so its rays
    carry to the detector how long and not how far; what is missing is
    the tie between a body's momentum and its phase that E = h f gives a
    released ray). The world key `action`, h (an integer from 1, in the
    units of the momentum label times Links; absent by default), and the
    measured-event key `phase_by_momentum` (true; false by default;
    refused without `action`, on a `fixed` measured event, which never
    steps, and on a family without a phase circle). With them, in
    `_move` where the step already happens, at the Link a body steps on
    an axis whose momentum component is p its phase turns by

        floor(k1 x |p| x N / h) - floor(k0 x |p| x N / h),

    with k0 = floor((age - 1) x |p| / (Q S M + |p|)) the count of Links
    the step rule gives on that axis at the age before the self-creation
    and k1 = k0 + 1 the count after it, that is `by_clock(k0, |p| x N,
    h)`: the count is derived from the age by the step rule exactly as
    the owed count is read off the clock, so nothing is kept at a Node
    and no remainder register exists; with a constant momentum k1 is the
    Links stepped on the axis and after k Links the phase has turned
    floor(k x |p| x N / h) mod N in all (test (d): 1 and 16 steps per
    Link, and 20480 k / 7 with a remainder each step, the floors 2925,
    5851, 8777, 11702, 14628). The axes compose: the steps are x before
    y before z, the phase's turn is the sum of the three components'
    turns at the Links stepped on each, and a step lost to an earlier
    axis's step in the same interval turns nothing (no Link was crossed;
    the count of the lost axis, derived from the age, still advances,
    as the step rule's count does). Where the momentum changes along
    the path (a push between two steps) the count k0 is the rule's
    count at the current age and momentum, not a history: the
    placement rule reads the record, not the past. Placed, as the owner
    said, outside the GameBoard like the age: a rule of the measured event,
    the external thing, read from its own record (its momentum label,
    its age); it changes nothing of the rays' flight or collision (test
    (e): the rays' rows identical with and without the two keys on a
    colliding crowd, the body's phase alone differing); the rays the
    body releases carry its phase as before (the clock's turn by content
    over K at the self-creation, this turn at the step after it, the
    release of the interval carrying the phase before both); without
    `action` there is no turn and every world reads as before. The bound
    derived: a body steps at most one Link per interval, so within the
    run k <= `ticks` on an axis and the parser refuses a turning body
    whose `ticks x |p| x N` exceeds 2^62 - 1 for its declared momentum
    (`age_bound`, the bound of a ray's age, does not bound a body's
    Links: a body lives the whole run); at run time the product
    (k0 + 1) x |p| x N is bounded before it is formed (`bounded`,
    `OverflowError` naming the body and "turn by momentum"), which covers
    a momentum grown by the pushes and a run longer than declared. The
    identity: the turn is a new physical hypothesis beside the law, not
    a rule of the GameBoard, so the law keeps `beam-v1` and `run.json`
    carries `action` and, when it is declared, `"hypotheses":
    ["bohr-v1"]` (`world.BOHR_RULE`); the `step` line of `events.jsonl`
    gains the body's `phase` after the step (the readings tool of series
    H reads it). What the closure means in the law's terms: the turn per
    orbit is (N / h) x the sum over the Links stepped of |p_axis|, which
    for a circle of radius r stepped on the GameBoard is 4 p r (the
    Manhattan weighting of the path: 4 r against the circle's 2 pi r),
    so the phase closes when 4 p r = j h, j whole, and with p
    proportional to 1 / sqrt(r) under a 1 / r^2 push the closing radii
    are proportional to j^2, Bohr's ladder in the GameBoard's metric
    (series H, EXPERIMENTS.md).

31. **The columns: the one coupling as a signed inner product** (the model
    owner, 2026-09-20, Highlights 5.4, "one mechanism for all the laws on
    the GameBoard", after the physicist's design of the strong force
    (scratchpad/strong/DESIGN.md) and the mathematician's verification of
    the form (scratchpad/columns/COLUMNS.md, "correct and working": the
    generic two-column form is the landed `push_form` integer by integer,
    411 600 + 200 000 cases, and reproduces every push of the registered
    worlds, 11 945 of 11 945); `tests/test_columns.py` (a) to (e)). The
    push a measured event takes from a group of a free family's rays is,
    per axis, `sum over the columns c of epsilon_c x sign(V E_c n_c) x
    by_clock(age_A, |V E_c n_c|, D_c d_c)` (step 4): every column is a
    value per unit of content declared per family with one sign per
    column, `gravity` the built-in first column of every family (the
    value [1, 1], the sign minus: `by_clock(age, |V M_A|, 1) = |V M_A|`,
    the law's -M_A V_B, not a term written in the code), `charge` the
    built-in second (rho, the sign plus: the electric part as landed,
    the same rational floored at the same clock), and a declared column
    (`"columns": {"<name>": {"value": n or [n, d], "sign": 1 or -1}}` on
    the family, the world-file form the mathematician's, which parsed
    all 66 example worlds unchanged) a further term of the same sum; the
    strong force is the column `strong` with the sign minus and a
    lifetime on its family, no code of its own. What the implementation
    decided where the design was silent: (i) the reader's side is its
    charge in every column read at the frame from what it holds
    (`Measured.charges`, `frame_charges`: the exact rational sum over the
    families held of their value times their content, the reduced pair,
    the physicist's D-1; for a one-family event rho x M, the report it
    was; gravity's the content), the arriving side the family's aligned
    values (`FamilyDefinition.values`), so the products `n_A n_B` and
    `d_A d_B` of the mathematician's form are formed per group at the
    push from the reader's charge and the family's value (one product
    and one `by_clock` per column per axis, fixed work) rather than once
    per family pair at load, because a reader's charge is a property of
    what it holds and not of one family; (ii) every column is floored on
    its own and never summed before the floor (the mathematician's
    section 4: the counterexample V = 64, rho_A = [1, 3], rho_B = [1, 1]
    reads -43, -43, -42, -43 at the ages 0 to 3 per column and -42, -43,
    -43, -42 summed then floored; the per-column form is the landed
    integer); (iii) the bounds: each column's product |V| x |E n| is
    tested by division before it is formed and refused naming the
    measured event and the column, the partial sum bounded after every
    column (`bounded`, the mathematician's R1 and R2), and at load the
    parser's static budget (`world._column_budget`, the mathematician's
    P3 in the form the physicist's design states): for every declared
    reader, every free family and every column, |E n| times the largest
    label flow one self-creation's release of the family can put at
    the reader (Q x the reader's Nodes x the largest release over the
    other events' directions) within 2^62 - 1, and the sum over the
    columns of the whole parts within it; a declared ray in transit, a
    merged or re-emitted row and a content grown by clicks are beyond
    the static rule and are refused at the push they would overflow
    (the mathematician's "what it does not reach the run-time rule
    refuses"); (iv) a reader's charge in a column beyond 2^62 - 1 (rho x
    M itself, which the landed form never formed alone) is refused at
    the frame naming the event and the column; the charge column's
    product is tested on the reduced pair, so a run the landed form
    refused at |V n_A n_B M_A| may be accepted where the reduced |V E n|
    is within the bound, the same integers where both accept; (v) the
    identity: the two built-in columns are the law as it was, so a world
    without a declared column carries no new identity, and a world that
    declares a column beyond `charge` carries `columns-v1` under
    `hypotheses` in `run.json` (as `bohr-v1` for `action`), the identity
    of the one mechanism; (vi) the record: `run.json` carries `columns`
    (the world's, name and sign, in order) and per family `columns`
    (name, value, sign, aligned), `state.json` and the measured events'
    states carry `charges` (the charge in every column by name). Checked
    on the 66 example worlds: `events.jsonl` byte-identical before and
    after, `state.json` equal but for the added `charges`, `run.json`
    equal but for the added keys (VALIDATION.md). (vii) The lifetime (the
    model owner, 2026-09-20, "DECIDED: the strong force's range is a
    lifetime, L: the event whose age reaches L makes no next event but an
    escape click in the ledger, as at an open face"; the physicist's
    design, scratchpad/strong/DESIGN.md; `tests/test_lifetime.py` (b) to
    (d)): the family key `lifetime`, an integer L from 1, one scalar
    (`FamilyDefinition.lifetime`, `NatureBeamWorld.lifetimes`); at step 6,
    after the reads of step 4 and the self-creations of step 5 and before
    the merge, every row of the family whose whole age is at or beyond L
    clicks on the border `lifetime` (`LIFETIME_NAME`): its amount,
    content and label booked in the ledger's `lifetime_amount`,
    `lifetime_content` and `lifetime_momentum` and the square of its
    coherent pointer in `lifetime_record`, summed into `escaped_amount`,
    `escaped_content` and `escaped_momentum` beside the faces, the transit
    momentum line lowered by what left, one `click` record per row naming
    the border (`measured` None, the Node the row was on, its family,
    number, amount, phase, label and content); then the rows leave the
    store. The reach of a lifetime is the flight table's: L = 1 reaches
    the six neighbours alone (every direction's first step is one Link
    along a heading), L = 2 the twelve face diagonals too, L = 3 the eight
    cube diagonals and the second Link of a heading (test (c)); a ray read
    at the age L is read and then booked, the reading of step 4 before the
    border. The parser refuses a lifetime beyond `age_bound` (a row would
    carry an age beyond the store's bound before the border took it), a
    declared ray in transit at or beyond its family's lifetime, and the
    name `lifetime` on a detector; the inverse interval is refused on a
    GameBoard with a family of a lifetime (the border has no inverse, as a
    face has none). The record: `run.json`'s `detectors` carry the border
    after the faces (`name` "lifetime", `nodes` 0, `threshold` 1, per
    family `measured`, `clicks`, `content`, `record` and `measured_content`
    0, and `momentum`), the `escaped` lines sum it, every family carries
    its `lifetime` (None without one), and `hypotheses` carries
    `columns-v1` when a lifetime is declared: a lifetime is the range of
    a column, the other half of the one mechanism, so it shares the
    identity and there is no third one. (viii) The held content (the
    physicist's D-1; test (e)): the measured-event key `held`, an object
    of family name to content, the content of every other family the
    event holds beside its `amount` under its own (`MeasuredDefinition.held`,
    aligned with the families; `Measured.held`, which the clicks of paid
    content joined already): the content the frame reads is the sum, the
    charges per column the rational sums of (i), every free family held is
    released at the world's rate at every self-creation (rows of the held
    amount per direction, as the own family's; the release of a held free
    family was the engine's rule before, reached by no declared world),
    the labels' bound and the phase-turn bound read the sum, and `owners`
    counts the event under every family it holds. Refused naming the key:
    the own family, an unknown family, a content that is not an integer
    from 1, `held` that is not an object. The register's proton is 1836 of
    `p` (charge 4) holding one unit of `nuclear` (strong 10000, lifetime
    3): the charges (1837, 1), (7344, 1), (10000, 1). No existing world
    declares a lifetime or `held`: every registered run is unchanged.
    (ix) The contact through the table (the model owner, 2026-09-20, on
    the physicist's design, section 4.4, "the contact of two bound
    bodies": with the step refused and the labels left as they were, a
    bound pair's labels grew under every push without bound, 10^10 to 3 x
    10^11 per interval, until the integer bound refused the run, and no
    book of the momentum on the measured events could close;
    `tests/test_contact.py` (a) to (d)): a body whose step on an axis is
    refused because the destination holds another measured event has
    arrived at that occupant, and the occupant's table entry for the
    body's family decides as it decides for a ray (`engine._contact`,
    `Measured.contact`): `measure` hands the body's momentum component on
    that axis to the occupant (the body's 0, the occupant's raised by it:
    what a click takes, kappa = 1, the body's momentum its own label),
    `rerelease` returns it (the body's component reversed, the occupant's
    raised by twice it: what a mirror does), `read` and `pass` leave the
    step refused and the labels as they are (the rule as it was: a world
    that wants it declares the rule). Where the entry is the keys' own
    rule for the body's family, declared or not, the contact is `measure`
    (`world.CONTACT_DEFAULT`, `MeasuredDefinition.contact` per family:
    the entry's rule where it differs from `default_rule`, `rerelease`,
    `pass`, `measure` on a free family or `read` on a paid one, and
    `measure` otherwise, so that an entry equal to the default changes
    nothing, the table-from-keys decision kept): a body arriving at a
    body is a paid arrival, its momentum its own label, and the keys' rule
    for a paid arrival is `measure`; so a free family's `read`, the keys'
    own, is the hand-over for its bodies as it is the push for its rays
    (`read` accumulates only where it is declared against the keys, on a
    paid family), and a declared `measure` on a free family absorbs its
    rays and its bodies alike, as for any arrival. The sum of the momenta on the measured
    events is unchanged by a hand-over (a transfer from one line to
    another; the books' measured momentum line is their sum), each label
    bounded by what one push accumulates between attempts. A body on a set
    of Nodes whose destination set holds several occupants hands the
    component apportioned whole over them by their contents
    (`apportion_whole`, the units left to the largest remainders, ties from
    the body's age modulo their count, in number order); an occupant of
    content 0 takes nothing. One `contact` record per occupant that took a
    hand-over (the tick, the body's number, its Node and the destination,
    the `occupant`, the body's `family`, the `rule`, the `axis` and the
    signed `component` the occupant gained, the body's `momentum` after);
    no record under `read` or `pass`; the occupant's state counts the
    hand-overs per family (`contacts`). Local (the destination Node is
    read by the step already; the transfer crosses one Link in one
    interval, as a ray's step does), fixed work (one entry per occupant of
    the destination set), the steps the frame's, outside the walk and the
    collision; no key and no third identity: the contact is a rule of the
    frame, as the no-merge decision was, and a world that declares no
    column reads it too. The design's integers hold on the engine: the
    pair of the six headings (Q 12, G 11, M 5, +128 per interval) reads
    128, 0, 0, 128, 256, 384, 512 over ticks 2 .. 8 and hands 256, 128,
    640, 512, 128, 256, 256 at ticks 3, 4, 9, 13, 14, 16, 18, the sum of
    the two labels 0 after every tick; the register's proton and neutron
    at one Link on the 290 fan read 310 967 280 640 per interval and hand
    it 999 times over 1000 intervals, the labels (0, 0, 0) at the end
    (under `pass` declared on each for the other's family, 39 times the
    `nuclear` rows' push alone after 40). Of the 66
    example worlds 60 are byte-identical in `events.jsonl` (no body of
    theirs ever stepped onto another) and six change from the first
    refused step of a body on: the coupling `1b_m1`, `1b_m4`, `1b_m16`
    (the free probe beside its source from tick 31, 169 hand-overs), Bohr
    `r2` and `r4` (the electron beside the proton) and the orbit `s8_r12`
    (one hand-over at tick 174), registered old against new in
    VALIDATION.md. A TIE OF THE FRAME, declared (the closing gate's
    genericity probe, 2026-09-20, finding G1; `tests/test_contact.py`
    (e)): the frame moves the bodies one after another in number order,
    so when two bodies step in one interval and one's destination is the
    other's Node, the lower number steps first: it makes the contact if
    the other has not yet moved, and the other, moving after, finds the
    Node it vacated free or hands over to it in turn; the sum of the
    momenta is the same either way, the holder and the positions are not.
    The declaration order is therefore a tie of the same kind as the axis
    order and `age mod n` (the mathematician's list), stated here and in
    ENGINE "The frame"; a simultaneous step of one interval would be a
    change of the law and is the owner's to decide.
32. **The `wave` threshold on the pointer's square; the escaped momentum
    per family** (the model owner, 2026-09-20; issue #359 step A and
    issues #360 and #361 item 1; `tests/test_nature_beam_detector.py`
    (i), `tests/test_nature_beam_books.py`). (i) Under `wave` a detector
    set's threshold reads the square of the coherent pointer of the set's
    arrivals this interval in units of one ray: with `(X, Y) = (sum 32 x
    amount_u C[phase_u], sum 32 x amount_u S[phase_u])` over the arrivals
    of every number but each Node's own (the pointer the window already
    read), one unit at phase 0 has `X^2 + Y^2 = (32 x 256)^2 = 2^26`
    (`POINTER_UNIT`), and the reading is the nearest integer,
    `pointer_units(X, Y) = (X^2 + Y^2 + 2^25) // 2^26`, a Python integer,
    exact and never refused; the set clicks when it is at least the
    threshold, and passes otherwise with `pass` records naming
    `threshold` as before, the window and the rule following unchanged.
    The pointer gate is the click's: it applies to the entries that absorb
    (`measure`, and `rerelease`, whose re-emission is a click), and a
    `read` entry, the push of a body, keeps the amount gate under both
    readings, since the push reads the flow and not the pointer (section
    3 step 4, note 25: the gravity of two rays does not depend on their
    relative phase at the reader; the closing gate's finding F1 of
    2026-09-20, `tests/test_nature_beam_detector.py` (k)).
    Why the nearest integer: the tables' `C^2 + S^2` is 65536 within 361
    for every N through 4096 (within 237 at N = 64), so one unit at any
    phase reads 1 exactly, a rays in phase read a^2 within a^2 x
    361 / 65536 (exactly through a = 11 at N = 64), two opposite rays 0,
    two a quarter turn apart 2, three a third of a turn apart 0 (their
    square 200704, 0.003 of a unit); a truncation would read 0 for one
    unit at 45 degrees (1024 x 65522 < 2^26). Under `beam` the threshold
    stays the amount summed over the set (the count is what a beam
    detector reads). No memory between intervals: the pointer is this
    interval's arrivals, and a pair that passed goes on as any passing
    ray does. What changes in the registered worlds (the 66 example
    worlds re-run and compared, VALIDATION): 65 are byte-identical in
    `events.jsonl`, `two_slits`, `one_slit`, the Bell ten (S = 2 exactly)
    and the three narrower A10 screens among them: no set of theirs ever
    read a pointer below its threshold with an amount at it. `w27_wave`
    alone changes: 2312 rays that met a screen pixel in antiphase pass
    where they clicked with the pointer 0, and, going on, click at other
    pixels and on the faces, so 38 of its 161 pixels' records differ (the
    sum of the screen's records 0.16 % higher), the screen's clicks
    150 187 -> 148 131, the count's FWHM 0.761 -> 0.758 and its rms 0.325
    -> 0.321, the record's FWHM 0.185 and the product 4.99 unchanged,
    the escaped 25 666 -> 27 634; re-registered old against new in
    EXPERIMENTS A10. The threshold
    keys of the tests that read the amount are re-pinned with the new
    integers written first (the detector's (a) to (d), the readings' (d),
    the body's (b): a smaller set is one ray, 1 < 3, where two in phase
    read 4). (ii) The momentum that leaves the GameBoard is booked per
    family: `Ledger.face_momentum[port][family]` and
    `lifetime_momentum[family]` (until then one vector per face and one
    for the border), `escaped_momentum(family)` the family's own and
    `escaped_momentum()` the world's total, `face_momentum_total(port)`
    and `lifetime_momentum_total()` the faces' and the border's sums; a
    body's escape books its momentum under its own family. `run.json`'s
    `escaped` line per family carries the family's own momentum (until
    then the world's total was written into every line, issue #361 item
    1); the face and border reports carry `momentum` per family beside
    their total; the books' escaped line is the total, unchanged. No
    registered integer changes except the per-family `escaped` lines of
    `run.json` in worlds of several families.
33. **The four unifications of the formulas: every logic once, to the
    letter** (the model owner, 2026-09-20, Highlights 5.4, "DECIDED: the
    four unifications of the formulas, after the strong force lands", on
    the mathematician's report of the same day, `ONE_FORMULA.md`: the law
    is two formulas and one table composed, every reading a moment
    `M_k = sum w u^(x)k` of the records at a set and every rate the whole
    part off an age, `by_clock(a, n, d) = floor((a + 1) n / d) - floor(a n
    / d)`; the four places where the code spelled one of the two
    primitives twice are spelled once, each an identity, the full suite
    and the replay of the register the proof that the law is the same).
    **(1) The pointer is the first moment of the one reading over the
    circle** (`tests/test_nature_beam_detector.py` (j)). The coherent
    pointer `(X, Y)` of a detector set (the window's, the threshold's,
    the record's and the phase returned: notes 24 and 32), of a face and
    of the border `lifetime` is `M_1` of the same moment table that reads
    space (`moment_table`, `read_groups`), taken on the circle's unit
    vectors `(C[phase], S[phase], 0)` in 256ths (`circle_vectors`) with
    the amplitudes `32 x amount` as the weights: `X = sum 32 amount
    C[phase]`, `Y = sum 32 amount S[phase]` integer by integer (the
    mathematician's moment_checks 1: bit-exact at N = 8, 64, 4096 on 900
    random sets), the record `|M_1|^2`, the set's phase its nearest step
    (`pointer_phases`), the `wave` threshold's `pointer_units` the same
    `M_1`. One call site of the one reading (`coherent_pointer` through
    `read_groups`); the separate pointer sum (`amplitude x C[phase]`
    reduced per group) is deleted. The record is never refused: the
    reading's own bound decides the register (`reading_fits`, the one
    test `read_arrivals` refuses by and `first_reading_overflow` looks
    per group by: 32 x amount x 256^2 x the rows of the group within
    2^62 - 1, the second moment's bound, which the pointer does not read
    but the one table forms, so one row of an amount below 2^41 fits
    where the former `POINTER_AMOUNT_BOUND` = (2^62 - 1) // (32 x 257)
    let 2^48 in), and beyond it the same table is taken in Python
    integers (`moment_table(exact=True)`, the dtype `object`), exact: a
    row of 2^42 that `read_arrivals` refuses reads its pointer, a row of
    2^49 reads (2^62, 0), a row of 2^60 (2^73, 0). `POINTER_AMOUNT_BOUND`
    is deleted (MIGRATION). Every world of the register replays
    byte-identical in `events.jsonl` and `state.json` (VALIDATION).
    **(2) Every age against a key is the one `by_clock`; the turn is the
    release at the rate [1, K]** (`tests/test_nature_beam_clock.py` (f)).
    The mathematician found that the turn `s = by_clock(a, M, K)` is the
    free release `by_clock(a, H n_r, d_r)` at the rate [1, K] (clock_checks
    8: the phase circle's turn is a release rate of phase per unit of
    content, E = h f as a rate), and that the lifetime's click, `become
    at` and the age bound are the same primitive read on an age against
    a key: `by_clock(a, 1, key) = 1` exactly at the self-creation that
    takes the age from key - 1 to key (clock_checks 4: first at the age
    L, then every L). So: the world key `K` is the clock's rate, a pair
    `[n, d]` of phase steps per unit of content per self-creation like
    `release`, the integer K read as `[1, K]` (every world file valid and
    bit-identical; the key keeps the name the owner uses; the record
    carries it as declared), the turn `by_clock(age, content x n, d)`
    (`NatureBeamWorld.turn`, `nature_beam.by_clock_rows` over the phased
    events in one array where the products fit the register), the
    refusal `2 s >= N` kept and the parser's static bound read at the
    rate (`2 x content x n < d x N`); the lifetime's click and the
    world's age bound are `nature_beam.ages_at_key(age, key)`,
    `by_clock(age - 1, 1, key) = 1` on the age after the walk (the walk
    that brought the age to the key; a row at age 0 has not walked and
    is never at the key; a rest row keeps its age and, by the parser's
    refusal of a declared age at or beyond L and the click at L, never
    stands at a key), the bound the key `age_bound + 1`: `store.age >=
    lifetime` and `store.age.max() > age_bound` are deleted, identities on
    every reachable state. `become at` is not in the code (in flight,
    WEAK.md) and will read the same call. No registered integer moves:
    every world of the register replays byte-identical.
    **(3) One moment table over one set object shared by a body and a
    detector, the data only** (`tests/test_nature_beam_body.py` (g)). The
    data: a body on a set of Nodes (note 30) and a detector set (note 24)
    are one object, `DetectorSet`: its Nodes mapped to the measured event
    at each (`DetectorSet.nodes`, a body one event, a declared detector
    several), one record and one phase per family, the one reading summed
    over the set in both; `Measured.nodes` reads a body's Nodes from its
    set's map (in the fixed order x, then y, then z, the engine inserting
    them so as a body steps or leaves, `NatureBeamSimulation._place`), and
    the engine's index `NatureBeamSimulation.at` maps every occupied Node
    to its set (`occupant` to the event's number; the reading's
    `node_event` is built from the sets). A detector stays a detector
    and a body a body: the rule unification (a detector as one measured
    event, its content, momentum and re-emission joining one record) is
    NOT taken, by the owner's decision, since it would re-register A10's
    openings and the two-slit walls. The table: step 4 takes ONE moment
    table per family over the rows at the set (`moment_table` on the
    arrivals' unit vectors, a row that did not step on the zero vector,
    the amounts as the weights and the ages among them) with the two
    masks the mathematician named, present and admitted: the present
    rows are every row of another number at the set, rest and moving,
    and the presence (what the clock counts) is their zeroth moment per
    measured event and the age moment their age moment (the two
    `np.add.at` sums of `family_plan` are deleted); the admitted rows are
    the rows the threshold, the window and the rule admit, and the
    record's component and the push's flow are their moments per
    (measured event, number), the flow with the label's weight (the
    table's own flow for a free family, the flow times the content per
    unit for a paid one; the separate `labels = u x weight` product is
    deleted). The one case where the two masks are not nested: `beam`'s
    pairing (note 24 (v)) splits a row into the units that go on and the
    units that click; the table takes the units that go on as a row of
    their own, present and not admitted, and the units that click as the
    admitted row, so the presence counts the whole row (5 for the rows of
    3 and 2 that pair 2 in test (g)) as it did and the push and the record
    read the clicked units as they did. Bit-exact: every world of the
    register replays byte-identical in `events.jsonl` and `state.json`.
    **(4) The columns floored at the clock age like every other rate**
    (`tests/test_nature_beam_push.py` (m); `tests/test_columns.py` (b), (e)
    and `tests/test_nature_beam_push.py` (k) re-pinned). The one exception
    of note 20: the columns' `by_clock` was read at `a_A`, the reader's
    age after the frame's advance, while the turn, the release, the lamp,
    the owed count and the step are read at the clock age `a_A - 1`, the
    age before the interval's self-creation (the mathematician's row 8).
    Now `push_form` takes `Measured.clock_age`: every rate of the law is
    read at the clock age. What moves: nothing where the product `V x E_c
    x n_c` is a multiple of `D_c x d_c` (`by_clock(a, n, d)` is then `n /
    d` at every age: series 7's product 3 x 2^22 x [1, 2] is even, 0 of
    200 ticks differ, the mathematician's clock_checks 3; `test_nature_beam_push`
    (e)'s 1920 / 20 = 96 exactly); where it is not, the extra unit of
    the floor lands on other ticks and the sum over the ticks is the same
    (the floors telescope): with an odd flow on a fan direction, V =
    u_(2, 1, 0) = (57, 29, 0), every tick moves by exactly one unit per
    axis and the sum over 22 reads by none (test (m), the fractional pin
    the owner accepted); the pins of `test_columns` (b) and (e) and of
    `test_nature_beam_push` (k) are re-pinned with the new integers
    written first (MIGRATION). The register: every world of the 85
    replays byte-identical in `events.jsonl` and `state.json`, so no
    registered series moves (C, 7, D, E, G, H, I, K, Bell, A10, the
    catalog: every charged product of theirs is a multiple of its
    denominators, or their reads never met a fractional floor).
34. **A table entry's window read from a reading** (issue #363, the model
    owner's go of 2026-09-20: "Alice and Bob are part of the GameBoard,
    no?"; a measurement, not a change of law; `tests/test_nature_beam_window_reads.py`
    (a) to (c); [ENGINE, the world](ENGINE.md#the-beam-law-beam-v1)). One
    additive key: on a measured event's table entry, `phase_window` may be
    the object `{"reads": "<family>", "offset": s}` in place of the number.
    The centre of the window is then the phase of the coherent pointer of
    the named family's rows present at the set in the interval, every row
    at the set but the reader's own number, rest and moving alike, as the
    presence counts them (the same first moment over the circle as the
    detector's record, `coherent_pointer`, its nearest step
    `pointer_phases`; `nature_beam.setting_steps`, read once per named
    family from the rows after the walk and the collision, before any table
    acts, so the order of the families changes nothing), plus the offset s
    in phase steps (0 by default); the width stays the law's half circle
    (`phase_width`, once it exists, applies to it as to a number). With no
    row of the named family at the set, or a zero pointer (an antiphase
    pair), the entry has no centre and passes, the `pass` record naming
    `window` None and `reads`; every `click` of such an entry carries the
    `window` used, so a reader bins by the setting off the record. What the
    implementation decided: (i) the setting is read over the SET (the
    detector set the reader belongs to), as the threshold and the window
    are, so a counter of one Node reads the rows at its Node and a declared
    set reads the rows at all of its Nodes; (ii) the rows read are the rows
    present (the presence), not the arrivals alone: a stream of one row per
    interval at a heading dwells one or two intervals at a Node (the flight
    table's 32 Links per 55 intervals), and the window must exist at every
    interval the stream is there; (iii) the setting rows meet the reader's
    table by their own entry (`pass` in the Bell worlds: no push, no
    record, the rays go on), the reading of their pointer being a reading
    aid of the measured event and no rule of the GameBoard; (iv) refused
    naming the key: an unknown family, a family without a phase circle (no
    phase to read), the entry's own family (the window gates those rows),
    the form on `pass` (as any window on `pass`) and on a lamp (a lamp's
    window is a number); the `offset` outside 0 .. N - 1 and an object with
    other keys or without `reads`. Every world without the key is the same
    integer by integer: 21 example worlds (the Bell ten, `one_content`,
    `two_contents`, `two_slits`, `one_slit`, the four of the catalog,
    `w1_wave` and two detector worlds) replayed byte-identical in
    `events.jsonl`, `state.json` and `run.json` before and after
    ([validation](VALIDATION.md)). The run that uses it is
    [A2 with the choosers on the GameBoard](EXPERIMENTS.md#a2-with-the-choosers-on-the-gameboard-2026-09-20):
    the settings of a Bell run decided by GameBoard events, S = 2 exactly
    with every E on the triangle, the law found not to correlate what
    never met.
35. **The meeting, M-R: an event in transit reads the crowd as a body
    does, a report** (the model owner, 2026-09-20, Highlights 5.4,
    "DECIDED: the meeting, M-R", "go for it if it seems generic and smart
    to you"; the physicist's and the mathematician's joint design of the
    same day, `scratchpad/meeting/MEETING.md`, sections 1.2 M-R, 1.3, 2.1,
    2.3, 3.1, 3.3 and 6, its scripts `turn_permutation.py` and
    `k_deflection.py`; the identity `meeting-v1`; `events/meeting.py`;
    `tests/test_meeting.py` (a) to (e); series K re-registered under the
    key in EXPERIMENTS.md and VALIDATION.md). The rule is section 3 step 3
    as written. What the implementation decided where the design was
    silent, and what it found: (i) **The module and the two call sites.**
    The arc permutation (built once per direction table from the flight
    table's unit vectors and cached per target, forward and inverse), the
    reading, the turn and the inverse live in `meeting.py`; `nature_beam`
    calls `meet` once after the collision in step 3 and once before the
    inverse collision, so the law's own function gains two lines and the
    tables one field (`NatureBeamTables.arcs`). (ii) **The target as
    read, not reduced.** The sector boundary `|u . e1| = |u . e2|` lies at
    the angle 1 / |t| off the e1 axis (`e2 = t x e1` grows with |t|), so
    `pi_t` depends on the magnitude of t and not on its direction alone:
    the target is `t = kappa V` whole (the crowd's flow of one unit gives
    (0, -64, 0), not (0, -1, 0)), which is how the design's offline flight
    was flown and what its registered expectation assumes; the two give
    the same chain from (1, 0, 0) on K's table. (iii) **kappa as a
    rational, the target over the common denominator.** `kappa_AB` is the
    reduced pair of the signed sum of the two families' values per unit
    of content over the columns (`meeting.column_sum`, `rational_sum`),
    and `t = sum_B n_AB (D / d_AB) V_B` over the least common denominator
    D with `|t| = isqrt(t . t) // D`; in every world of the register a paid
    family's values beyond gravity are 0 (the parser refuses others), so
    `kappa = (-1, 1)` and `t = -V` exactly; D-1's whole charge on a paid
    family would enter here without a change of code. (iv) **The bounds.**
    Every product is tested by division before it is formed and refused
    naming the Node or the target: the crowd's flow at a Node (the largest
    label times the rows at the fullest Node within 2^62 - 1, as the
    reading's bound), `n_AB x |V_B|` per family, a target component
    beyond 2^30 (`t . t` must fit the work register for the exact root: a
    crowd of 2^24 units on one heading), a target's component beyond 2^20
    before its frame is formed, and the angle keys' products
    `(u . t)^2 x |u|^2` beyond 2^62 - 1 (the design's bound, the products
    within `(Q^2 |t|)^2`: a crowd of about 2^13 units at one Node met by a
    paid unit; no registered world comes within a hundredth of it). (v)
    **The rest and the phase.** A paid unit at rest reads the crowd and
    advances its phase like any other (the coordinate map of the design's
    section 2.1 applies to every paid unit), and the permutation fixes its
    direction: it stays the table's. A paid family without a phase circle
    is refused under the key at parsing, naming the register. (vi) **The
    `turned` line.** `Ledger.turned_momentum` per family, the change of
    the transit momentum line by the turns, is added to the books
    (`families[<name>].turned` and `momentum.turned` in every audit line
    of `run.json`, zero without the key; `tests/test_lifetime.py` (b) and
    `tests/test_nature_beam_flight.py` re-pinned with the new line written
    first) and the running transit
    line is moved by the same delta, so `books(recount=True)` equals
    `books()` under the key and the inverse returns both lines. (vii)
    **The cost.** One segmented reading of the crowd per interval (two
    `np.unique` passes over the free rows at free-space Nodes) and one
    exact sector sort of at most `len(D)` directions per new target of a
    turning row. Measured on series K's `mass` world on an idle machine
    (400 intervals in-process, the host's wall time): 19.9 ms per interval
    without the key and 24.5 ms with it, the meeting 4.6 ms per interval
    (1.8 s over the run) for 13618 crowd rows and 447 rows of the beam;
    67 permutations built in the whole run (the targets a beam meets
    repeat) at 0.58 ms each on the 296-direction table, 0.04 s in all; the
    rest of the cost is the two segmented readings of the crowd. Under the
    load of the register's replay the same run took 36.5 s against the
    control's 17.6 s (EXPERIMENTS.md, K under the meeting), which is not a
    measurement. (viii) **What the register replays.** Every one of the
    85 example worlds is byte-identical in `events.jsonl` and `state.json`
    with the module present and the key absent, and the ten registered
    worlds named by the design (the six of series 7, `2`, `s8_r12`, `r4`,
    `coasting_age`) are byte-identical with the key declared (no paid row
    in transit meets a free row in any of them); `run.json` gains the key
    and the `turned` lines in every world (VALIDATION.md). (ix) **What the
    offline flight left out.** The design flew the beam beside the replayed
    crowd and skipped the turn at occupied Nodes, but let a ray pass
    through the mass's Node; on the engine the mass is a measured event
    whose table measures a paid arrival, so the rays turned into it click
    there (122 of the beam in `mass`, 169 in `near`, 1 in `heavy`), and the
    centroid at b = 6, M = 2^12 reads -1.8 pixels where the flight said
    -3.0 (EXPERIMENTS.md, K under the meeting).
36. **The weak force in the world's terms: (i) the window's width** (the
    model owner, 2026-09-20, Highlights 5.4, "DECIDED: go on everything;
    just make sure again that it is good and generic", item (1): the weak
    force in the recommended order, the neutrino first with the table-entry
    key `phase_width` and no change of law; the physicist's design,
    scratchpad/weak/WEAK.md 1.2, with its check `weak_integers.py` 1.1 and
    1.2 and the engine's baseline `window_engine.py`, 320 of 640 arrivals
    clicking under the half circle; `tests/test_window_width.py` (a) to
    (e)). A window is its setting s and its width w: the w consecutive
    steps of the circle [s - floor(w / 2), s - floor(w / 2) + w), a phase
    at the distance d = (phase - s) mod N inside when (d + floor(w / 2))
    mod N < w, the one floor of the window and its width
    (`nature_beam.window_admits`; the mathematician's ONE_FORMULA row 11),
    read as before under `beam` on each ray's own phase, under `wave` on
    the set's pointer and on a lamp on its clock's phase. The key
    `phase_width` on a table entry (any rule but `pass`) and on a lamp, an
    integer from 1 through N, N / 2 by default (`world.default_width`): the
    half circle as it was, d < N / 4 or d >= 3 N / 4, identical on every
    (phase, setting) pair of every N from 2 through 4096 (test (a)), so
    every registered world is bit-identical; the window table of
    `NatureBeamTables` is deleted, the one floor its only spelling, and
    `beam`'s pairing arc is the entry's width (test (c)). The admitted
    fraction of a source's rays whose clock turns s steps per
    self-creation (the stride s over the circle) is exactly w / N when
    gcd(s, N) = 1 and g x (the residues of the coset inside the arc) / N
    when gcd(s, N) = g (test (b): 10, 20, 40 and 320 of 640 arrivals at
    w = 1, 2, 4, 32; the stride 2 at w = 1 centred on 0 admits 20, centred
    on 1 none). Refused naming the key: a width outside 1 .. N, on `pass`,
    on a family without a phase circle, and without its window's setting
    (what the implementation decided where the design was silent: a width
    is the width of a window, and never centres itself on 0 by default);
    a lamp's width the same. The record: the measured events' states and
    `state.json` carry `widths` (per family, None where none is declared)
    beside `windows`; nothing else changes. Checked on the 85 example
    worlds: `events.jsonl` byte-identical before and after, `state.json`
    and `run.json` equal but for the added `widths` (VALIDATION.md). What
    the detector's world sees (series J2, EXPERIMENTS): a cross-section
    where the GameBoard has a stride, w / N per arrival, deterministic, no
    draw, flat in the emitter's rate (the window reads the phase alone and
    a free ray carries no content: PREDICTIONS entry 7, the law's own
    limit against nature's rise with the neutrino's energy, stated and not
    tuned), and a filter rather than an attenuation (entry 8: a beam that
    survived one reader survives every identical reader behind it). No
    identity: no law changed; the neutrino is a free family with a phase
    circle, no charge and no content, gated by a reader's window.
    **(ii) A paid family's charge per unit of amount, D-1** (the model
    owner, 2026-09-20, "go on everything", item (2): "a paid family may
    declare a whole charge per unit of amount, read on the charge line
    only, the push untouched"; the physicist's design, WEAK.md 1.5, the
    mathematician's note that "paid => q = 0" was a decision and not a
    necessity; `tests/test_paid_charge.py` (a) to (e)). The wording of the
    law: the charge of a measured event is rho times its content for a
    free family and the declared whole charge times the amount for a paid
    family. The family key `charge` on a paid family is an integer c (a
    pair with a denominator other than 1 is refused: a charge per whole
    unit is whole), the whole charge of one unit of amount, and it is read
    in one place, the charge line of the books: per measured event the
    free families' rho x content held (as before) plus the paid families'
    c x the units it holds (`Measured.units`: the units it clicked and the
    units waiting to be created again, at home, re-released or a product;
    `Measured.charges` and the report `Measured.charge`), plus per paid
    family c x the rows in transit (the transit line's running current) and
    c x the units escaped (the rows through the faces and the border with
    the units that stepped off with a body, `Ledger.units_escaped`): the
    line is conserved exactly through the flight of a charged paid row,
    its click, its home and re-creation, its escape and the escape of the
    body that holds it (tests (a) to (d)), and it will be through a
    transformation ((iii)). Nothing of the push changes: the paid family's
    `charge` column value stays (0, 1) (`FamilyDefinition.column_charge`),
    so the frame's `frame_charges` (`Measured.charges(for_push=True)`, the
    reader's side of the push) leave the paid units out, a paid ray's push
    stays its label, and a charged free reader reading a charged paid row
    takes the label alone (test (a): (64, 0, 0) with the beta charge -1
    and 0 alike). Refused naming the key: a fractional charge on a paid
    family; a lamp on a measured event of a charged paid family (what the
    implementation decided where the design was silent: a lamp's releases
    would create charge from nothing, the lamp's own content being content
    and not units; a charged paid family is born by a transformation or
    declared in transit). The record: `run.json` carries the family's
    `charge` as declared ([c, 1]) and its `charge` column value [0, 1];
    the books' `charge` pair is the extended sum, the same pair as before
    in every world without a charged paid family. No identity: a report of
    the books. Checked on the 85 example worlds: byte-identical in
    `events.jsonl`, `state.json` and `run.json` (VALIDATION.md; no
    registered world declares a charge on a paid family).
    **(iii) The transformation `become`, the identity `weak-v1`** (the
    model owner, 2026-09-20, "go on everything", item (1): "the
    transformation `become` with the identity `weak-v1`", in the
    recommended order after the neutrino; the physicist's design, WEAK.md
    sections 2 and 4.3 with its integers in `weak_integers.out` 2 to 6;
    `tests/test_become.py` (a) to (f)). One table rule on the one-way side
    of the border, beside `read`, `measure`, `rerelease` and `pass`: a
    measured event becomes an event of another family and releases the
    rest as products. Two triggers, one function (`nature_beam.transform`).
    The clock trigger is the measured-event key `become`, `{"at": a,
    "into": family, "products": [[family, amount, content per unit], ...],
    "crowd": c}`, fired in step 5 at the self-creation whose clock reaches
    `at` (the event's own age against the key by the one `by_clock`,
    `ages_at_key`, the lifetime's form: first at `at`, then at every
    multiple of it) while the gate is open: `crowd`, optional, an integer
    from 0, lets the transformation fire only at a self-creation at which
    the count the clock read is below it (the law's form of the condition
    that keeps a bound neutron stable; absent, no gate). The click trigger
    is a table entry whose rule is `become`, `{"rule": "become",
    "phase_window": s, "phase_width": w, "into": ..., "products": [...]}`:
    an arrival that passes the threshold and the window is clicked in
    step 4 exactly as `measure` clicks it (a free arrival's push on the
    reader, a paid arrival's label and units) and then the same
    transformation fires, its products born at the reader's next
    self-creation; no `at` and no `crowd` on it (the window is the gate).
    What fires: the products are paid from what the event holds of its own
    family, R = the sum of amount x content per unit, at most its declared
    `amount` (refused at load) and refused at run time naming the event if
    it holds less at the trigger (a declared transformation that cannot be
    paid is a defect of the world, loud, never silent); the family line
    moves, held[into] += held[from] - R and held[from] = 0, the event's
    family is `into` and its rho the new family's; everything else of the
    event (its number, Node, set, momentum, age, clock, phase, owed count,
    detector set and every other family held) is untouched: it is the same
    measured event with another family's content, and its rays come home
    as before. The products are born at that self-creation as every
    re-release is (`PendingRow`: product k apportioned whole over the
    event's directions with the leftover counted from (clock age + k) mod
    n, so that two products of amount 1 leave on different directions; the
    parent's phase at the trigger; the age 0), the recoil over all of them,
    free and paid (a free product is a thing thrown, not the field; the
    design's "the nu label joins" a free ray's click is not this: on a
    click a free ray takes the columns' push and its label never joins),
    and the event's `become` key and every `become` entry of its table are
    consumed (the entries reset to the keys' own rule for their family
    with no window, the contact under them the default; the other entries
    stay as declared): the transformation is the event's one change of
    family. Charge exact: the parser refuses a transformation whose
    charges do not balance (rho_into x (amount - R) plus the paid
    products' whole charges per unit of amount, D-1, against rho_from x
    amount), so the books' charge line is the same pair before and after
    (test (a): [0, 1] at every tick, +1 on `p`'s content 5 against -1 on
    the beta unit in transit, clicked or escaped; test (e) through the
    click of the product). One-way (a change of a measured event's
    record, as a click and a release are; the walk and the collision read
    nothing of it), local (the event's own record, the arrival at its
    Node), fixed work (one comparison per self-creation at the clock
    trigger, one apportioning per product at the birth), fixed storage
    (the declaration), no draw, no register, no formula in a payload. The
    parser's refusals, naming the key: `become` without `into` or
    `products`, `into` an unknown family or the event's own, a product
    naming an unknown family, an amount below 1, a free product's content
    other than 0, a paid product's content below 1, a label beyond the
    bound, `at` below 1 or absent, `at` or `crowd` on a table entry,
    `crowd` negative or fractional, `into` or `products` on another rule,
    the products' content above the `amount`, the charges unbalanced,
    `become` on a family (test (f)). What the implementation decided where
    the design was silent: the crowd gate is read at every pulse of the
    key (the clock trigger is `ages_at_key`, so a gated event whose count
    falls below the gate fires at the next age that is a multiple of `at`,
    never between; the bound neutron's stability is a gate on a pulse, not
    a reset of its clock: test (c), the gate 64 holding a count of 128
    over 40 intervals, the gate 129 letting tick 4 fire); the entries are
    consumed at the transformation and the contact under a `become` entry
    is the keys' `measure` (a body arriving at a `become` reader is a paid
    arrival); the record's `become` line is written at the products'
    birth, when their directions and the recoil are known; the count the
    clock reads slows the trigger (test (c): a crowd of 128 at the
    suspension [1, 128] fires tick 4 against tick 3), no special case for
    a bound event. The record: `hypotheses` carries `weak-v1` when a
    measured event declares `become` or a table entry's rule is `become`
    (after `bohr-v1` and `columns-v1`); `run.json`'s `numbers` per
    measured event carry `become` (the declaration by names, None
    without); the measured events' states carry `became` (the
    transformations fired) and their `family` after; the books' measured
    line per family gains `became` (negative out of the family left,
    positive into the family become, the sum over the families minus the
    products' content: initial + measured + became = current + spent +
    escaped); `events.jsonl` gains one `become` line per transformation
    at the products' birth (`tick`, `node`, `measured`, `trigger` "clock"
    or "click", `triggered` the tick of the trigger, `from`, `into`,
    `products` as [family, amount, content, direction] with the direction
    each was born on, `recoil`, `counted` the count the clock read at the
    trigger); the tally of a `become` entry's clicks under `measure`.
    Checked on the 85 example worlds: byte-identical in `events.jsonl`;
    `state.json` and `run.json` equal but for the added `became` and
    `become` (VALIDATION.md; no registered world declares a
    transformation). What the detector's world sees (series J1 and J3,
    EXPERIMENTS): a population of 64 neutrons decays in a step (the
    shell's clicks within 23 intervals, a width of 0.036 of the median
    against nature's 3.17 for a memoryless decay), every beta carries the
    one declared content (a line), a neutron beside a proton decays later
    than a free one (577 against 512) or, under `crowd`, not within the
    run: PREDICTIONS entries 10 and 18, the law's own limits against
    nature's exponential survival, continuous spectrum and stable bound
    neutron, stated and not tuned; the trigger ticks are the engine's
    clock slowed by its count as every clock is, and the three readings
    outside their pins are the estimator's (one tick's count for a whole
    history), reported and not moved.
    **(iv) The W world: the exchange form at one Link, no key added** (the
    model owner, 2026-09-20, "go on everything", item (3): the W world
    after the transformation; the physicist's design, WEAK.md 1.1 and
    4.5; `tests/test_w_world.py` (a) to (d)). The W is a paid family
    (`quantum` 1) with a whole charge per unit of amount (D-1, (ii)) and
    the family key `lifetime` 1 (note 31 (vii)), no column: a row born at
    a self-creation makes its one step at the age 1 (m(1) = 1 on every
    direction), is read by the table of the measured event it arrives at
    (a paid arrival is measured by the keys' rule: its units clicked, its
    label the push) and is booked on the border `lifetime` at the end of
    that interval where no table took it; it exists on the neighbours of
    its emitter and nowhere else. Nothing is added to the law: the W
    world composes `become` ((iii)), D-1 and the lifetime. L = 0 is no
    family at all (the parser refuses a lifetime of 0): the contact form
    of the weak force is the `become` entry itself, its products released
    by the measured event with no carrier on the GameBoard (Fermi's form;
    series J1 and J3 are the contact form). No Z family: a neutral
    current is the neutrino's own row met by a `rerelease` within a
    window. The exchange: a neutron (1839 of `n`) with `become` at its
    key into `p` and the one product `[["w", 1, 3]]` (the charges: 4 x
    1836 on the proton left against -7344 on the W unit, 0 the neutron's)
    throws the W on +x; one interval later the proton one Link away
    measures it and holds it: its content 1836 + 3 = 1839 and its charge
    7344 - 7344 = 0, a neutron's content and a neutron's charge in the
    detector's terms, with no `become` entry on the proton at all (test
    (a): the click at tick 4 for the key 3, the push (192, 0, 0), the
    recoil (-192, 0, 0), the charge line [7344, 1] at every tick, the
    store empty, the border 0). What the implementation decided where the
    design was silent: the design's sketch of the proton's entry, `w:
    {rule become, into n, products [["beta", ...]]}`, does not balance
    under the law (the W unit clicked stays held with its own -7344, the
    proton's line loses +7344 to `n`'s 0 and the beta carries another
    -7344), so the parser refuses it (test (c)); a `become` entry on the
    proton balances only with a positive paid product (a positron of
    +7344: p + W -> n + e+, the W unit held), which the test pins and the
    register does not use: the exchange is complete at the click, and the
    family name `p` on the proton holding the W is the GameBoard's label,
    not the detector's reading. The record: nothing new (`hypotheses`
    carries `columns-v1` for the lifetime and `weak-v1` for the
    transformation). Checked on the 85 example worlds: the source is
    byte-identical to (iii)'s (the same fingerprint), so every replay is
    (iii)'s (VALIDATION.md). What the detector's world sees (the
    register's `w_exchange`, EXPERIMENTS): the W born at the key and
    taken one Link and one interval later, the proton's charge 0 and
    content 1839 after, nothing on the border, the momentum exchanged
    (+192 and -192): 5 readings inside, 0 outside. What nature's W has and
    this does not (the physicist's 5.3, registered as limits): the
    electroweak scale and its broken symmetry, the W and Z masses fixing
    the scale, the propagator's rise and V-A; the law's W is a carrier of
    charge and momentum over one Link and nothing else.
    **(v) The moving body's clock, unchanged** (the physicist's finding,
    WEAK.md 2.4; the model owner, 2026-09-20: the engine stands). The
    clock of a measured event ticks at every interval in which it owes
    nothing, whether or not its body steps in that interval (`_frame_all`
    before `_move`), so a body in flight fires its `become` at the same
    tick as one at rest and its range is v x at, linear in v; TERMINOLOGY's
    sentence on the self-creation ("a transfer is not one"), which read as
    if a step skipped a tick, is corrected, and nature's gamma is recorded
    as a limit of the law in HYPOTHESES.md entry 21 (series J4 the reading
    to make), not tuned in. Nothing of the engine changes.

37. **The amplitude law, `amplitude-v1`: the record on the row, the
    normal form, the split, the layer and the world's clicks read from
    the GameBoard's paths** (the model owner, 2026-09-20, Highlights 5.4,
    "DECIDED: `amplitude-v1` is built, with the four recommendations and
    the four unifications"; the physicist's and the mathematician's
    design, `docs/designs/amplitude-v1/DESIGN.md`, its check scripts the
    integers; the branch `amplitude-impl` from `7f986124`, the commits (i)
    `ca2e5fad`, (ii) `9ca0600c`, (iii) `578742e3`, (iv) `f3d4ad54`, (v)
    `62369cb8` and this note's; the physics-rule reviews of (i)/(ii) and
    of (iii) applied; MIGRATION (i) to (vi), ENGINE, TERMINOLOGY,
    TEST_EXPECTATIONS, VALIDATION and the register's series L). Under the
    world key `amplitude` and nowhere else, the GameBoard computes every
    path of a record locally and exactly, and the world's list of clicks
    is read from those paths by the birth phase u on a ladder of the
    record's offers; without the key every world reads as it did, byte for
    byte (the gate set, (viii)). The law in the world's terms:
    **(i) The record on the row and the normal form** (the design's 1 and
    2.3; commit (i)). Every row of the store carries three columns beyond
    the ray's: `record` (the identity of the birth that made it, the
    lamp's number x 2^32 + the birth's ordinal, `amplitude.record_identity`;
    0 on a row of no record, which every row is without the key), `branch`
    (the arm and the label packed, arm x 2^32 + label, bit k of the label
    the arm k's; 0 without the key) and `multiplicity` (m, the product of
    the splits' norms along the path, 1 without the key). The merge is the
    normal form of the design's module |p + N/2> = -|p>: two rows of one
    record, one branch and one multiplicity at one Node and direction whose
    phases are opposite cancel, the signed sum by magnitude on every group
    (the books' `cancelled` lines; N3 of the review: (i) alone kept a guard
    that (ii) removed, so (i) is not runnable on a record alone,
    MIGRATION). The flight, the collision and the push never read the
    three columns (N10): a branched row pushes matter by its amount as
    every row does, the owner's (c), the sum over the branches; the K
    finding of (ix) is the next item on that.
    **(ii) The split and the birth** (the design's 2.1, 2.3 and 3.1;
    commit (ii); the owner's unification (2)). A `rerelease` entry under
    the key declares `weights` (one integer per declared direction),
    `turns` and `inputs` (a row of weights and turns per arrival
    direction, N6: the beam splitter's matrix [[b i, a], [a, b i]] / c,
    unitary, its conjugate transpose the inverse through the merge); a row
    (w, m, p) arriving is re-emitted as (w a_i, m x A, p + t_i) with A the
    sum of the squares; the split is the re-emission with a vector, one
    rule, and a split is not a click (B1 of the review of (i)/(ii)): no
    pointer gate and no window at a `rerelease` under the key, the amount
    gate alone; the units a split creates, sum (a_i - 1) w per row, enter
    `released` as every re-creation does (N5: the design's `split` line is
    not a line of the books, the identity closes without it). A lamp
    births one record per self-creation, k rows of one unit on its k
    directions with the multiplicity k (the rate [1, 1] alone under the
    key: r units per direction would be r identical paths with one birth,
    refused; `branches` and `arms` give the joint labels of a pair or a
    GHZ triple, one row per label per direction, m = paths x norm, a lamp
    short of the quanta refused, S4). A row of a record taken home is
    re-created with its columns and its m kept, apportioned whole as a row
    of no record is (N8: no acceptance world sends a record's row home).
    **(iii) The pair form of `phase_per_link`** (the design's frequency;
    the owner's unification (1); N1, N2). Under the key a family may
    declare [n, d], the phase per interval of age: a row turns
    `by_clock(age, n, d)` at every walk that advances its age, the row's
    own floor per segment from its age 0 at its birth or re-emission,
    sum_j floor(A_j n / d) over a path's segments, equal to the design's
    one floor at the click when d = 1 (every L1 world) and within one step
    per segment otherwise; the integer form turns per Link crossed as it
    did and the two are not the same number on the flight table (a heading
    crosses 32 Links in 55 intervals). The default is the integer 0, not
    the lamp's own turn: a family that turns in transit declares it.
    **(iv) The layer, the reading `sum` and the ladder** (the design's 3,
    5 and 7; commit (iii); the owner's unification (4)). The layer
    (`events/amplitude.py`) is a host register beside the GameBoard, not a
    Node's: it holds, per live record, its offers per Node (the pointers,
    the residual units, the content and the momentum the rows carried
    there), fed by the engine's `birth`, `split`, `cancel`, `rotate`,
    `join` and `end`, and it completes a record when its live units are 0:
    the cells (a set's weight the sum over its Nodes of the square of the
    coherent sum over the labels of the products of the arms' residuals,
    the decision of the review of (iii) on the owner's point 5: coherent
    within one Node, incoherent across a set's Nodes), the rungs b_k =
    (2 N C_k + Total) // (2 Total) at the nearest integer, u the birth's
    phase choosing the cell, the Node within the cell chosen by the same
    rungs over the Nodes (c_j = (2 W D_j + T) // (2 T)), the `gather` line
    with the chosen set, arm and channel, the Node, the content and the
    momentum, the weight, the total and the cells. `sum` is the one
    pointer's reading at the record's scope (`DetectorSet.scope`: crowd,
    record or none; unification (4) done as a scope, not as a fourth
    reading): a `sum` set ends the units it takes with an offer and clicks
    nothing itself; the crowd's readings `wave` and `beam` are untouched,
    and a free family's rows keep the unkeyed apportioning and gates at
    every entry (B2). One birth per rebirth: a record that chose a `sum`
    re-emitter is born again there once, its rows by the split (B1 of the
    review of (iii)). A `phase_window` on a `rerelease` whose Node reads no
    `sum` set is refused at load (S3); the layer's set names are reserved
    under the prefix `measured:` (S5); the multiplicity through every
    re-emitter of the world is bounded at load within 2^62 - 1 (S6). The
    reading tool `tools/amplitude_path.py` replays a run's register
    through the layer and equals `run.json`'s `world` on every keyed run.
    **(v) The pair, the rotation at the window and the label click** (the
    design's 4; commit (iv)). A `sum` set whose window has the setting s
    reads the rotation U_s = [[C'[s], S'[s] v(t)], [-S'[s], C'[s] v(t)]]
    on the half-angle tables of 2N into its channels + and -, t the table
    entry's `turn` on the label-1 column (0 by default), the setting
    declared or read from a reading (at N = 4096 the tables of 2N do not
    exist: an even setting reads the 4096 table at s / 2, an odd one is
    refused); the click of a pair is one cell of the joint labels'
    products over the arms, so the marginals are exact and the outcome of
    the pair is the one u of the one record.
    **(vi) The gate and the label rotation** (the design's 10 and its
    `gate.py`; commit (v)). A `rerelease` entry declares `rotate`
    (`world.Rotation`: one label bit turned on the GameBoard, two rows per
    row on the bit cleared and set with the amounts w C' and w S' of the
    half-angle tables and the matrix's signs, m x 65536) and `gate`
    (`world.Gate`, the CNOT between the records of distinct lamps pending
    at the entry, one record per emitter, the earliest born, exactly
    `parties`; the control the record whose rows arrive on the entry's
    declared `control` direction, required for two parties or more, so
    that the circuit does not change with the order of the `measured`
    list (the review of (v), S1); with `hold` the entry holds the rows
    pending until rows of `parties` distinct emitters are pending at it,
    read from the rows alone, the design's local hold, the layer's live
    count left to the completion (B3); the layer's `join`: the joint
    labels the product of the label sets permuted from the control's bit
    0, every row replicated over the other records' labels, the units the
    copies add booked on the live count as a split books its rows (B1:
    until this fix every gathered record of the CNOT worlds ended at live
    -1), the identities aliased; a record that reaches a gate with units
    elsewhere or with an offer already made is refused by the layer,
    since its rows and offers elsewhere would keep their pre-join labels
    and drop out of the joint cells (B2; the design's lazy relabelling is
    not built); a gate of one party relabels the rows present and joins
    nothing); the `gate` and `rotate` lines. The register's ceiling: three label rotations on a path (m =
    2^48) fit, four (2^64) are refused at load naming the Node, Grover's
    six (2^96) are not a world of the GameBoard, as the design states.
    **(vii) What the worlds gave** (series L, EXPERIMENTS; every integer
    the design's check scripts' unless named). L1: the Mach-Zehnder at
    one port (D1/D2 over 64 births: 64/0, 0/64, 32/32, 64/0 with D2's rows
    cancelled on the GameBoard, 63/1 on (3, 4), the unequal arms 64/0,
    32/32 and 0/64 at the pair 0, [8, 1] and [16, 1]), Elitzur-Vaidman
    32/17/15 and 32/16/16, the same list on a second run. L2: the two
    slits at a low rate, wall 34, screen 15, faces 15 of 64 under the
    per-Node rule (re-pinned from 31/14/19 by the decision of the review
    of (iii); the design's "3/5, 2/5" is not this geometry's reading,
    every set the reading's). L3: the pair at the CHSH labels S = 176/64
    (E x 64 = 44, -44, 44, 44), the registered quadruple 156/64, every
    marginal 32/64, the which-path world 88/64, Bob's counters 116 Links
    farther E = 44 (0 with the read): no maintenance. L4: GHZ's four
    allowed triples per basis, the products -1 (XXX) and +1 (XYY, YXY,
    YYX). L5: the CNOT pair 176/64, CNOT twice the identity, GHZ by one
    gate of three parties the same triples. L6: S = 2896/1024 (E x 1024 =
    724, -724, 724, 724) and S = 11584/4096 = 2.828125 (E x 4096 = 2900,
    -2900, 2892, 2892), below 2 sqrt 2 = 2.828427 at every N; the design's
    bound |E - cos| <= 1/N holds at N = 1024 and not at 64 (0.0196 against
    0.0156) or 4096 (the tables' 1/256 entries round E by 0.0009 against
    0.00024, the test pinned marked failing), and S = 2 sqrt 2 - epsilon
    with epsilon at most 4/N holds at 1024 and 4096 and not at 64 (0.078
    against 0.0625). Departures from the design, stated and not moved:
    the record's total over u takes eight values from 65448/65536 to
    65773/65536 on the (20, 21) splitter, the tables' own formula
    (1681 q[u + 16] + q[u + 32]) / (1682 x 65536) pinned, the design's
    0.0019 holding at u = 0 alone; the gate joins one record per lamp,
    the earliest born, and holds a record whose rows are elsewhere (two
    sequential gates on an entangled record are one gate of three parties
    or one gate per arm, the design's lazy relabelling not built).
    **(viii) The key's existence and the one click not landed.** From (i)
    to (v) the key gates everything: the gate set of seventeen worlds (one
    per table rule, key and family kind, the owner's change to the
    design's test 7) replays byte-identical in `events.jsonl` and
    `state.json` without it, `run.json` gaining the key false alone
    (VALIDATION, the digests). The design's section 6, the record form
    the default and the crowd's threshold path deleted, was tried at stage
    (vi) as the owner's half-hour version (the key forced true, the `wave`
    pointer gate off) on the gate set: three lamps are refused at load
    (`two_slits` at the rate [64, 1], `catalog/lamp_mirror_screen` [4, 1],
    `heisenberg/w3_beam` [47, 1]: the record form births one record per
    self-creation), `catalog/sun_planet` fails in the run (a record's rows
    reach the set `screen` with the multiplicities 9 and 36, one
    multiplicity per offer), `bell/read`, `bell/a0_b8` and
    `lensing/mass_meeting` change their clicks (their lamps at [1, 1]
    birth records read by the ladder) and every world without a lamp
    changes byte-wise by the columns written on its click lines and in
    `state.json` with no value differing (`coupling/7_pp`, `one_content`,
    `redshift/age`, `hubble/coasting_age`, `weak/j2_filter`,
    `weak/w_exchange`, `detector/periodic_z_node`; `nucleus/deuteron_1`,
    `weak/j3_neutron_free` and `bohr/r2` by their digests, their lines
    not kept). Worlds outside the crowd-threshold series change, so by the
    owner's rule stage (vi) stopped there and the key stays: the one
    click needs the lamp's rate under the record form, a set's offer of
    several multiplicities of one record, the columns written only where
    a record is, and the design's test 7 restated as identity on the
    worlds without a lamp; none is a half hour, none is done here.
    **(ix) What is not done, and next.** Unification (3), one permutation
    component for the collision, the meeting and the gate, is refused with
    the reason: the collision permutes directions by the six-heading table,
    the meeting turns phases, the gate permutes the labels of the rows of
    different records, three different columns under three keys, and a
    shared wrapper would add no logic and hide the three. The K finding
    under the record's click (the coordinator's record of 2026-09-20, the
    lensing worlds of `mass_meeting` under the key): the record's click
    beside a mass moved to smaller y against the control's in every world,
    -2.115, -5.208 and -4.432 pixels at the three (M, b) against the
    crowd's -2.021, -4.345 and -2.465, and the 464 records that reached
    the mass were absorbed whole by it; two changes are the next item, not
    landed here (more than an hour together): u as the record's own field
    on the row beside the running phase (u = the lamp's clock count mod N,
    the GameBoard's rules reading the path phase, phase - u, the click
    reading u; the test: the K record world's click centroid equals its
    offers' expectation under uniform u within one rung) and a record's
    row pushing matter with its share amount^2 / (m x norm) of the label,
    the remainder booked on a ledger line (the test: the mass's momentum
    per record equals the label times the sum of the shares). Also open:
    the full register replay and the coverage-measured gate set (the
    trimming pull request), the design's Grover (a world beyond the
    register's ceiling), the design's `split` line of the books, and the
    design's bounds at N = 64 and 4096 as stated above.
