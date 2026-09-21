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
reads (the flight rule, the collision table). Since 2026-09-21 (the model
owner's order, "optimization and simplify") `nature_beam` reads as the six
steps it names, each step a function of the same module called by
`nature_beam` alone, over the frame `Interval` that `interval_frame` reads
once per interval: `_walk`, `_collide`, `_measure` (with `_measured_arrays`,
`_family_plan`, `_apply_plans` and `_apply_plan`), `_release` (with
`_release_family`), `_border`, `_merge` and `_inverse_interval`; the law is
still the one function, its text moved and not changed (bit-exact;
[MIGRATION](MIGRATION.md#the-interval-in-named-steps-on-2026-09-21-host-only-bit-exact)).
The repository's rule that a
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
one, with `u_d` the **unit vector of the direction at the flight's
scale**: the integer vector nearest `Q D[direction] / |D[direction]|`,
Q = 64, one world constant per direction computed once in the direction
table (`nature_beam.unit_label`, the flight's `labels`) by the exact
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
changes by a byte). Added on 2026-09-21 (the model owner's record 270 of
the log of 2026-09-20; a hypothesis beside the law, not a rule of it): the
world key `covariant_readings`, one object `{"c2": [1, d], "grain": g,
"books": false}` (absent by default; refused with `action`), the identity
`covariant-readings-v1` of [DERIVATIONS_BEAM section 17 as amended in
17.6](DERIVATIONS_BEAM.md#176-amended-per-the-physics-rule-review-of-covariant-readings-v1-record-297-the-nine-must-fixes-the-integer-forms-the-should-fixes):
under it every body that is not `fixed` carries its energy readings (the
exact square W = E'_0^2 + d **p** . **p** with E'_0 = Q S M, E' the largest
integer with E'^2 <= W by comparisons, the load-time root once; a measured
event may declare `E`), its self-creations are gated by a second owed count
`by_drive(acc_tau, E' - E'_0, E'_0)`, the drive's wall loses its cap term
(`step_divisor` with `cap` false: Q S M alone, so the pace per lattice
interval is p / E' in the mean), the crowd's count is charged with the sum
of the readings since the last self-creation, and the free release runs
per lattice interval at the rate held x E' over E'_0 x d; the domain |p|_1
<= Q S M and the push ceiling of one grain per interval are refused; the
record carries the `energy` lines and the key's block
([ENGINE.md, the readings by type](ENGINE.md#the-detectors-readings-by-type));
absent, nothing of it is computed and no world changes by a byte (series
S, [examples/events/covariant/README.md](../examples/events/covariant/README.md)).
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

and nothing else with law in it; since 2026-09-21 its six steps are the
named functions of the module listed in section 1 ("The owner's name"),
called by `nature_beam` alone, over the frame `Interval` (the world's
constants, the measured events in number order and the crossing marks of
note 48, read once by `interval_frame`) and, in step 4, `MeasuredArrays`
(the measured events' tables in array form, read once by
`_measured_arrays`). `NatureBeamTables` holds the two pure tables,
computed once at load from the world's direction set and N: the flight rule
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

**The flight rule** (one world constant, the owner's 1 / sqrt 3, "the phase
velocity the wave on the mesh had"): for a direction **v** = (a, b, c) (the
direction vector) with S_1 = |a| + |b| + |c| (its Manhattan length) and Q = 64
(the label's scale), `T_d = isqrt(3 (a^2 + b^2 + c^2) Q^2)` (the direction's
resolution); the Manhattan steps made by age tau (the age) are `m(tau) = (2
tau S_1 Q + T_d) // (2 T_d)` and the ray at age tau is at the m(tau)-th point
of the Bresenham line of **v**
(`line_d`, the S_1 unit steps of one period of the direction's line, the
axis furthest behind first: a world constant per direction like u_d),
`position(tau) = (m // S_1) v + line_d[0 .. m mod S_1]`. m(tau) is the whole
count of the position's accumulator on the row (the model owner's record
155 of 2026-09-20, "no tables"; note 41 (viii)): the accumulator starts at
T_d, gains r = 2 S_1 Q at every interval over d = 2 T_d, and the interval's
Manhattan step is e = [acc + r >= d] (`Flight.walk_step`, the one count
rule `by_drive` written out); a ray's rate never changes over its flight,
so the accumulator at the age is `(tau r + T_d) mod d` and the count made
is m(tau), both off the age, and the row carries no field for them. Since
`3 |v|^2 >= S_1^2` (Cauchy-Schwarz), `T_d >= S_1 Q` and `m(tau + 1) - m(tau)`
is 0 or 1: **at most one Link per interval in every direction, Euclidean
speed exactly 1 / sqrt 3 for every direction** (600 intervals put a ray at
distance^2 within 1.5 % of 600^2 / 3 for all 1730 primitive directions with
components up to 6; `scratchpad architect/nature_beam_tables.py`). Why 1 / sqrt 3 and
not 1 / sqrt 2 on the plane: the flight rule is a Beam Law, not of the
GameBoard; 1 / sqrt 3 is the largest speed at which no integer direction in
space ever crosses two Links in one interval ((1, 1, 1) is the bound), and a
plane world (extent 1 on z) uses the same table, so a wavelength is `period x
c` on every GameBoard. The step of the interval is `step_d(tau) = line_d[m(tau)
mod S_1]` if `m(tau + 1) > m(tau)`, else no move; the inverse is `tau - 1`
then the same step subtracted: bit-exact. The step of an age is periodic
in `L_d`, the least period of the pair `(tau mod T_d / gcd(S_1 Q, T_d),
m(tau) mod S_1)` (the heading (1, 0, 0): T 110, L 55; (1, 1, 0): T 156, L
39; (1, 1, 1): T 192, L 3; (3, 1, 0): T 350, L 175), a fact about the rate
the readers use for the speed c = m(L_d) / L_d; until record 155 the
engine read a step table per direction over that period, built from the
same rule at load, and the age modulo L_d. Since 2026-09-20 the age
itself is kept whole on the record (`(direction, age) -> (direction, age +
1)` is injective, a bijection onto its image; the store's bound is the
world's `age_bound`, note 25); until then it was reduced modulo `L_d`. A
rest direction has S_1 = 0 and never moves.

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
   whole; the flight rule reads it (the position's accumulator off the age).
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
   other than its own, as today: the threshold on the arrivals (section 5),
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
   the same sum, not a term of the code. Since the crossing rule
   (2026-09-21, note 48; the model owner's record 158 of 2026-09-20) the
   rows a reader meets are the crossings of its world line: its arrivals
   and, in the interval of a step, the rows on its Link against it and
   the rows at the Node it entered moving against it, never a row that
   came over its Link behind it; a moving reader's Doppler is the count
   of the rows it crosses (the world key `doppler` of 2026-09-20, the
   flux weight at the grain G, note 38 as it was, is deleted with it).
   On the two built-in columns this
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
symmetric outputs is broken by the sorted order, that is by Port order, one
of the law's two declared ties (the other is the digital line's, note 39),
averaged out over the six orientations of a crowd.
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
| | the flight rule | `T_d >= S_1 Q`; `m(tau + 1) - m(tau)` in {0, 1}; `L_d` periods as listed in section 3 |
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
   `NatureBeamTables` (`direction_flight(directions)`, `collision_table()`, both pure,
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
(d) The tie by Port order in the collision is a declared tie (the digital
line's tie by axis order is the second, note 39); a test asserts the
six-orientation average of a head-on pair's exits is isotropic. (e) The re-registered readings are expectations, not results:
series C item 6's slowing changes power (the accepted price), and the
register must say so.

## 10. Implementation notes (2026-09-19, the implementation)

The decisions the implementation took where the design was silent,
impossible as written or ambiguous, each decided by the design's principles
(one generic function, every piece of logic once, a bijection but the click,
the flight's speed, integers only) and recorded here as the
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
   flight rule, but the age of a ray parked by the collision is kept (the
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
9. **The Bell worlds run 160 intervals**: the flight's pace puts the
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
13. **Every ray steps at its first interval**: the flight's first
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
    event's drive advances at every self-creation, before the interval's
    owed count is paid (the crossing rule, note 48, 2026-09-21; until then
    a step waited for the interval that paid the count: `test_push_width`
    (c) 18, 36, 54 became 17, 35, 53); the momentum is untouched by the
    step; `run.json` records
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
    momentum begins its drive at 0 instead of stepping off its age). The
    exemption that stood here until the fraction-free law of 2026-09-20
    ("'No remainder is kept' above stands for the clock, the release, the
    lamp and the owed count, which read a rate against an age no push
    changes") held only at a constant rate: a paid lamp's rate falls at
    every birth and the crowd a clock reads on a fan changes at every
    interval, so on the register the remainder of those counts was
    discarded undeclared (the physics-rule reviewer, record 148). Since
    note 41 below every count keeps its remainder on the body's
    record, and `by_clock` off the age is the constant-rate identity of
    that count, not a count of its own.
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
    the direction at the flight's scale Q = 64 (the same table as
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
    Unchanged: the flight rule T_d, the collision table, the clock, the
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
    placement rule reads the record, not the past (until the model owner's
    record 155 of 2026-09-20, note 41 (i): the count is the `action` row
    of the body's table of counts, the exact sum of |p| N over the Links
    counted on the axis, so a push between two steps is counted where it
    happened). Placed, as the owner
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
    store. The reach of a lifetime is the flight's: L = 1 reaches
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
    did and the two are not the same number on the flight rule (a heading
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
    worlds without a lamp; none is a half hour, none was done at (vi).
    Stage (vii), step 1 (MIGRATION (vii-1); `tests/test_amplitude_click.py`)
    builds the four under the key: a lamp's rate births as many records
    as it says units per direction, each with its own ordinal and the
    birth phase advanced by the clock's stride; two multiplicities of one
    record at one offer add at the common denominator where their ratio
    is a square (the held pointers rescaled by its root) and are refused
    otherwise (the integer form has no cross term over the square root of
    their product: a limit of the law, recorded); the columns and the
    `cancelled` lines are written only where a record is; the gate set's
    lamp-free worlds read the same with the key and without it.
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
    the mass were absorbed whole by it; two changes: u as the record's
    own field on the row beside the running phase (u = the lamp's count of
    births mod N, the GameBoard's rules reading the path phase, phase - u,
    the click reading u; built at stage (vii) step 2, MIGRATION (vii-2):
    the K record world's clicks per set within one rung of its offers'
    expectation under uniform u and the click centroid within 0.25 pixels
    of it, `tests/test_amplitude_click.py` (f)) and a record's row pushing
    matter with its share amount^2 / m of the quantum's label (the
    record's norm in m), the integer form label x amount // m, the
    remainder booked on the books' `remainder` line (built at stage (vii)
    step 3, MIGRATION (vii-3): the mass's momentum is the sum of the
    shares of the rows it absorbed, `tests/test_amplitude_click.py` (g);
    N10's "matter feels every branch" is closed: matter feels each branch
    by its share). Also open:
    the full register replay and the coverage-measured gate set (the
    trimming pull request), the design's Grover (a world beyond the
    register's ceiling), the design's `split` line of the books, and the
    design's bounds at N = 64 and 4096 as stated above.
    **(x) The one click, landed** (stage (vii) step 4, MIGRATION (vii-4);
    the design's section 6). The record form is the law: the world key
    `amplitude` is deleted (a world that declares it is refused), every
    lamp births records, the crowd's `wave` threshold on the pointer's
    square is deleted (the amount summed over the set under both
    readings; the pointer gives the set's phase and its record), the
    layer is on every world and the identity `amplitude-v1` is under
    `hypotheses` when a lamp is declared. A world without a lamp reads as
    it did before the law (the gate set's lamp-free worlds pinned by their
    digests); every world with a lamp is re-read: its rows are records,
    read by the ladder, and its clicks are the records' (the register's
    re-run worlds, EXPERIMENTS, marked "re-run under the one click; the
    verdict to be re-read", the old numbers kept as dated history).
    **(xi) The click's weight as the inner product** (2026-09-21, the model
    owner's order "not a square in the code but a vector operation", record
    173 of the log of 2026-09-20; the branch `click`). The click's weight is
    the inner product of the pointer with itself, through the coupling's
    primitive: `core.integer.signed_inner((X, Y), (X, Y), (1, 1))` in
    `amplitude.cells`, a vector, a declared diagonal matrix of +1 and -1, a
    vector, the same class of operation as the coupling's signed inner
    product over the columns and as the reading's order-2 moment; nothing is
    squared as a step of its own; the layer passes no bound, its weights
    being the host's reports (2^116 on a pair, 2^174 on a GHZ triple, beyond
    the register), and the ladder's rungs stay a comparison. The coupling's
    own sum, `nature_beam.push_form`, is left untouched and does not call
    the primitive, for a precise reason: its term per column is the whole
    part off the reader's clock, `by_clock(age, |V E_c n_c|, D_c d_c)`, a
    floor taken between the product and the sum, so the push is the signed
    sum over the columns of the columns' whole parts and equals the inner
    product of E and n under the declared signs, times V, only where every
    denominator D_c d_c is 1; written through the primitive it would be the
    inner product of the whole parts with a vector of ones, a sum disguised
    as a product, and its refusals name the measured event and the column
    before each product is formed and after each column's sum (pinned in
    `test_columns`), which a shared call would not. Bit-identical: the gate
    set's sixteen worlds and the full check unchanged (VALIDATION).
    **(xii) The click without amplitudes: one bilinear form with a declared
    Gram matrix** (2026-09-21, the model owner's decision, record 188 of the
    log of 2026-09-20, "yes, if it cleans a non-vector operation off the
    GameBoard"; the derivation mathematician's proof, DERIVATIONS_BEAM.md
    section 6.7 with `click_gram.py`; the branch `click`). The record's rows
    at an end Node and label are the phase-count vector **f** in Z^N, f_p
    the amount at the phase p at the amplitude scale 32 (the record's
    group-ring element written as a vector), and the layer keeps that
    vector and no pointer (`amplitude.Offer.counts` and `residuals`; the
    `Counts` type). The click's weight is ONE bilinear form with a declared
    matrix, **f**^T **G** **f**, **G** = **E**^T **E** the Gram matrix of the
    tables, **E** the 2 x N matrix whose rows are the tables C and S and
    G_jk = C_j C_k + S_j S_k over those rounded entries themselves, never
    the cosine of j - k, built once per N at load (`core.phase.phase_gram`,
    stored through N = 512, an entry formed from the tables beyond it):
    symmetric, of rank 2, not circulant (its diagonal takes the eight
    values 65448 .. 65773 that were the eight totals over the births of
    series L; 3696 of its 4096 entries at N = 64 differ from their
    diagonal neighbour). For one arm the form is evaluated explicitly
    through the primitive (`Layer.gram_form`: G's rows on the support of f
    against f, then f against that image) and the complex pair (X, Y) is
    never formed; for several arms (the pair, GHZ) the weight is the same
    bilinear form on the tensor product of the arms' vectors, whose matrix
    G^(k) = E^(k)^T E^(k), E^(k) the 2 x N^k matrix of the products of the
    tables' entries, is not materialised (N^6 for a triple) but evaluated
    through its rank-2 factorisation, the product in Z[i] of the arms'
    pointers **E f** (`Layer.evaluate`, `cmul`) summed over the labels and
    taken with itself (`signed_inner`, (xi)): the same integer by the
    associativity of integer arithmetic. The rotation's entries act on the
    counts as scalars (C' x 256 and S' x 256 in 1/256^2) and the entry's
    turn v(t) as the shift of the phases by t (`Layer.rotation`), the
    group ring's multiplication by e_t; a read's factor is the multiple
    256^2 of the ring's identity e_0, and an arm's factors multiply in
    Z[Z_N] (`ring_product`). The convolution form ACROSS arms is the exact
    law's statement and not the built click's: the rounded evaluation E is
    not a ring homomorphism (E(e_1)^2 = (64400, 12750) against 256 E(e_2) =
    (64256, 12800) at N = 64), so the built click multiplies the arms'
    pointers, as the tensor form says, and convolves nothing across arms.
    Bit-identical on every registered cell (`tests/test_amplitude_gram.py`
    and the click tests unchanged): mz_equal's 1681 / 1682 at all 64 u and
    its 64 / 0, slits_low's 64 clicks (wall 11, 12, 11, the screen's 15 on
    fourteen pixels, the faces 8, 7), the pair's 27, 5, 5, 27 and S = 176 /
    64, GHZ, the cone; the `record` line of a `sum` set adds the same form
    of the record's counts (`gather_records`) and reports the pointer.
    Two precise statements for the reviewer: (1) the turn's shift equals
    the former product (C_t, S_t)(C_p, S_p) exactly where the tables turn
    exactly, at t a multiple of N / 4 (every registered turn is 0 or 16 at
    N = 64), and differs at any other turn by the tables' rounding (at t =
    3, the entry 181, the phase 1 and the weight 7: (76811875, 31668665)
    formerly, (76871424, 31786496) now, one rounding in place of two; no
    registered world declares such a turn); (2) the amplitude scale 32 on
    the amounts and the identity 256^2 of a plain set stay as scalars on
    the counts, the unit 2^58 of a weight unchanged.

38. **The reading's weight at the relative speed, `doppler-v1`** (the model
    owner, 2026-09-20, record 119; the world key `doppler`, the flux of a
    row's stream through a moving body at its speed quantised to the grain
    G = 2^12, off the reader's clock before the columns, `weighted_flow`):
    deleted on 2026-09-21 with the crossing rule (note 48; the model
    owner's record 158, "in both cases the key leaves the code": a moving
    reader's Doppler is the count of the rows it crosses, no weight, no
    grain). The note's text, the key, the grain, `quantised_speed`,
    `flux_pair`, `weighted_flow`, the nine worlds `hubble_stars/doppler/`
    and `tests/test_doppler.py` are in the repository's history before the
    branch `crossing` (MIGRATION, "The crossing rule, on 2026-09-21"); the
    third run of series G2 under the key stays as a dated record in
    EXPERIMENTS, VALIDATION and the series README.
39. **The hand, `hand-v1`** (the model owner, 2026-09-20, record 128 of
    [the log](LOG_2026-09-20.md), "the hand's three choices confirmed";
    the physicist's design hand/DESIGN.md, record 122, read against the
    mathematician's integer form FORM.md, record 120; `tests/test_hand.py`
    (a) to (g); the worlds of series P, `examples/events/hand/`). The one
    thing the record did not carry: its sense of turning about its own
    direction. **The row** gains one column `hand` in {-1, 0, +1}: +1 a
    right-handed screw along u_d, -1 a left-handed one, 0 none (every row
    of every world without a declaration), the helicity, `sign(S . p)`,
    which on the GameBoard, where every row moves at the one speed of the
    flight rule, is the chirality the weak force reads. A pseudoscalar:
    under a signed axis permutation g of the cube a hand goes to det(g) h,
    kept by the 24 proper rotations and negated by the 24 improper ones
    (a reflection composed with a rotation), with no arithmetic; a bit
    relative to the direction, so every rule that changes a row's
    direction leaves it untouched, and a column of constant 0 has a width
    of 0 bits in the packed merge key (`merge_key`), so every world
    without a hand keeps the same key, the same order and the same bytes.
    It is an identity field of the merge (`IDENTITY_FIELDS`): two rows
    equal in every field but the hand are two rows and never merge, and
    under the amplitude key two rows of one record in antiphase with
    opposite hands never cancel (opposite helicities are orthogonal).
    Carried unchanged through every re-creation: the walk (a column of the
    row), the collision (the permutation moves the direction, the columns
    go with it; the class key (number, content) is untouched, so the
    table, the twenty orbits and the bijection are what they were), the
    meeting (a slow turn conserves helicity), a re-release at a mirror, a
    wall or a re-emitter (`PendingRow.hand`), a split by `weights` (every
    output row), a `rotate` (the label turns, the hand does not), a `cnot`
    gate (`_replace` keeps it), a home and the inverse interval ((direction,
    age, hand) to (direction, age + 1, hand) is injective). **The measured
    event** gains the axial record `axis`: one of the six headings in
    Port order declared as its vector, `[1, 0, 0]` .. `[0, 0, -1]`
    (refused otherwise), or none; an axial vector, a -> det(g) g a under
    the 48; a declaration fixed like `fixed` (no angular-momentum ledger:
    a click on the event does not turn it, the products' spins are not
    subtracted from it). Wu's polarised nucleus is an axis; a neutrino in
    flight is a bit. **GIVING.** The family key `hand` (-1 or +1; the
    catalog's definition, as `charge` is: the neutrino is left-handed
    once, not per world): every row born of the family (a lamp's, a free
    release's, a product's, a home's, a declared transit row's) carries
    it. The lamp key `hand`: a circularly polarised lamp of a family
    without a hand (light of one hand); a lamp of a chiral family may
    repeat the family's value only. The transit key `hand`: a row of a
    family without one; a chiral family's row takes the family's. **The
    right-hand rule** at the birth of a `become` product (step 5, the
    apportioning of the pending row over the parent's directions): at a
    parent with the axis A, a product of a family with the hand h is born
    only on the parent's declared directions d with `sign(A . u_d) = h`,
    one integer sign per direction (`world.axis_sign`: A is a heading, so
    A . u_d is one component with a sign, in {-64, 0, 64}), the whole
    apportioning of today (`apportion_whole` with the leftover counted
    from (clock age + k) mod n) over the admitted subset in declared
    order; a product of a family without a hand is born on every declared
    direction stamped `h = sign(A . u_d)`, +1 along the axis, -1 against
    it, 0 on the equator; at a parent without an axis every product on
    every declared direction as today, its family's hand carried (an
    unpolarised parent is lawful and the general case: nature's free
    neutron emits handed antineutrinos isotropically; J1's neutrons and
    J3's deuteron declare no axis). The three choices, taken by the model
    owner as physics over convention against FORM.md's (record 128): (i)
    a left-handed product leaves AGAINST the axis (`sign(A . u_d) = h`,
    not -h: in Wu's experiment the electrons leave opposite to the
    nuclear spin, and the left-handed beta's spin then points along the
    parent's axis, the product carrying the parent's sense; both forms are
    covariant and give the same parity difference, the sign decides which
    reading is Wu's and `hand/wu.json` pins Wu's side); (ii) the strict
    hemisphere only, the equator not admitted (a heading perpendicular to
    the axis has no sign against it; on the six headings one direction is
    admitted, not five); (iii) the hand's home on the family, not on the
    product (a hand cannot then be declared inconsistently between two
    worlds or two products), with a lamp's and a transit row's hand for
    families without one. An empty admitted set is refused at load naming
    the rule, the product and the axis (`world._handed_products`; a
    declared transformation that cannot leave is a defect of the world,
    loud). Nothing else gives a hand; the engine branches on no name (an
    integer of the event, an integer of the family, the direction table).
    **TAKING.** The table-entry key `hand` (-1 or +1; refused on `pass`),
    the parity filter: the entry's rule (`read`, `measure`, `rerelease`,
    `become`) applies to arrivals of that hand only; an arrival of the
    other hand or of hand 0 is passed exactly as an arrival outside the
    entry's window is (a `pass` line naming its `hand`; J2's form: the
    rows a reader does not take go on to the reader behind it). Admitted
    = the threshold AND the window AND the hand, three comparisons of an
    integer the row carries at the Node with a declaration of the reader,
    applied after the window (and after the amplitude law's exemptions of
    a `sum` set and a split from the window: a filter at a `sum` set
    passes the other hand). The weak force on one hand is then the
    `become` entry's `hand` -1 and nothing else: a right-handed W arriving
    at it is passed, dies on the border `lifetime` one interval later and
    transforms nothing (test (c)); the same key on a `measure` entry is
    Goldhaber's helicity filter and on a `rerelease` a hand-selective
    mirror. **A hand is not a column**: no push, no moment, no pointer and
    no clock reads it (the one-reading-set principle holds; the meeting's
    target and every moment are blind to it). **PASSING.** The meeting,
    the collision, a `pass` entry and every re-creation keep it, no
    arithmetic; a `read` entry with a hand filter reads the push of one
    hand and passes the other. **The record.** Only in a world that
    declares a hand or an axis anywhere (`NatureBeamWorld.handed`): the
    `click`, `pass`, `read` and `rerelease` lines carry `hand` (a click
    per row; a group line the one hand of its rows, None where they
    differ), the face and border `click` lines carry it, the `become`
    line's products gain a fifth entry, the product's hand; the books'
    measured line per family gains `left` and `right`, the units clicked
    of each hand as the row's column carries it (a report,
    `Ledger.taken_left`, `taken_right`); `run.json`
    carries each family's `hand` and each number's `axis` as declared and
    `hand-v1` under `hypotheses` (after `amplitude-v1`); `state.json`
    writes the row's `hand`. Without a declaration no line, no key and no
    byte changes: the gate set replayed identical ([VALIDATION](VALIDATION.md)).
    **The hand as a label bit named** (FORM.md section 5, the design's
    section 4): on a branched family of the amplitude law the hand is the
    meaning of a label bit and NOT the row column (a rotation makes two
    rows on the bit cleared and set, and a hand carried as a column would
    then disagree with the label on one of them): a lamp's `branches` may
    carry a third entry per branch, the hand of the label, every branch or
    none, the bit k of a label the hand of the row on arm k, the two
    values of a bit the two hands (`LampDefinition.label_hands`); the
    click line then carries the hand the row's label bit means on its arm
    (`nature_beam.row_hand`), the row column stays 0, and a family
    declares one or the other, never both (refused at load); the parity
    filter reads the same hand of such a row, the label's meaning on its
    arm (`nature_beam.read_hands`, the physics-rule review's finding 1.1:
    the filter on a branched family is then the which-path click on the
    label, FORM.md section 4, and not a filter that admits nothing): on
    the pair with the rotations removed and `hand` +1 on the two plus
    counters, 32 of the 64 records gather at the plus counters and 32 at
    the minus ones, none mixed, and with the rotations kept the label is
    read after the rotation and every marginal stays 32/64 (test (g)). The
    books' `left` and `right` lines count the row's COLUMN alone (on such
    a family they stay 0 while the click lines name the label's hand: a
    report of two readings, stated). With it the
    pair's integers are unchanged: S = 176/64 at the CHSH labels, every
    marginal 32/64 (test (g)); an improper symmetry negates the bit, which
    sends |00> - |11> to itself up to a global sign, so the Bell worlds
    stay mirror-equal. Malus's law is the label's, not the hand's: a
    linear polarisation is the two-label record with a relative phase, the
    polariser its `rotate` and the label click; a hand filter alone on
    circular light is 1 or 0, no angle. **The parity test** (the design's
    1.3 and 3.2, test (d)): under a signed axis permutation g of the cube
    every polar thing goes by g (positions, directions, momenta, the
    detectors), the `axis` as an axial vector, det(g) g A, and every
    `hand` is copied VERBATIM (the law's data: the catalog's families and
    the readers' filters, as Wu mirrored her apparatus and not the
    neutrino), the readings mapped back by the Node map. Under the mirror
    in x, the genericity probe's T2 as coded, an axis along the mirror's
    normal is its own mirror image, det(M) M e_x = e_x, so on the worlds
    of series P the axial transform and a verbatim copy of the axis
    coincide (under a y- or z-mirror they do not: an axis in the mirror's
    plane goes to its opposite heading, and a verbatim copy would be a
    different apparatus); the pins under that mirror: every registered world equal (no hand);
    `w_hand` DIFFERENT by exactly the click moving from the proton at x =
    3 to the proton at x = 1, the product's direction, the recoil and the
    push with the other sign, everything else equal; the control
    `w_two_sides` (no axis, no hand) equal; `wu` different, the beta's
    click at x = 16 against x = 0 and the antineutrino's face -x against
    +x; `nu_hand` equal (a hand without an axis is a datum a mirror cannot
    see; Goldhaber's reading needs the axis, as nature needed the
    polarised Eu-152). Over all 48 signed axis permutations (test (d); the
    physics-rule review's own probe read the same): the parity image
    differs under exactly the 24 improper elements and under none of the
    24 proper ones on `w_hand` and `wu`, and under none of the 48 on
    `w_two_sides` and `nu_hand`; and the full transform (every hand by
    det(g) too, every axis by det(g) g A) is equal under all 48 on every
    world: the law is covariant under the 48 when its data transform as a
    pseudoscalar and an axial vector, on the headings and on every
    direction whose digital line has no tie; on a fan the line's tie (an
    equal deficit on two axes at a step, broken by the axis index, x
    before y before z, `_bresenham`) breaks the 40 axis permutations for
    a tied direction: the Nodes crossed and the exit face move, the label
    **u**_d, the momentum and the hand do not (the auditor's round 2 on a
    fan world of the five directions (1, 1, 0), (2, 1, 0), (3, 1, 2),
    (1, -2, 0), (0, 1, -3): the record mapped back through g^-1 equals
    the base under exactly the 8 elements with the identity axis
    permutation; the six headings and (2, 1, 0), (1, -2, 0) never tie,
    (1, 1, 0), (3, 1, 2), (0, 1, -3) do, which is why test (d) on series
    P, the headings +x and -x alone, reads equal under all 48). This tie
    and the collision's Port-order tie (section 4) are the law's two
    declared ties; a tie broken by a datum of the row instead of the axis
    index is the owner's call. Parity violation on the
    GameBoard is one statement, the catalog's one-handed families (no
    `nubar` of hand -1 and no `nu` of hand +1 is declared anywhere; a
    right-handed neutrino declared in a transit row would be passed by
    every `hand` -1 entry and clicked by none: a sterile row, the law's
    own prediction). **Cost and locality.** One int8 per row (two bits in
    the merge key where it varies, none where it does not), one index per
    event, one sign per product per direction at a birth (at most the
    declared directions), one comparison per arrival group at a filter;
    no product, no division, no remainder, no draw; the birth reads the
    parent's own axis and directions at its Node, the filter the arriving
    row's hand at the reader's Node and the reader's declaration, every
    re-creation copies a field of the row it holds (LOCALITY-1); the
    store's row bound gains a factor 3 at most and only where a hand is
    declared. **What the implementation decided where the design was
    silent:** a `pass` rule writes no line, as it never did, so the
    antineutrino's passage at Wu's far reader shows in the face click one
    interval later and not in a `pass` line (the design's 3.4 expected
    one; the record form of `pass` entries, not the rule); the label hand
    on a click line is read from the lamp of the row's record (a report of
    the host by the record's identity, nothing of the law); a group line
    of mixed hands names None. **Limits, stated and not built:** no
    angular-momentum ledger and no spin dynamics (one bit for every
    family; no precession, no spin-1/2 against spin-1); nature's helicity
    reversal of circular light at a metallic mirror at normal incidence
    (the axis-keeping form h' = sign(h u_in . u_out), one more inner
    product, recorded in the design's section 6: the owner's frame says a
    re-creation keeps what the message carries); V-A's energy dependence;
    CP (with a hand and the columns' signs the law has a mirror and a
    charge conjugate but no phase that distinguishes them). The identity
    `hand-v1` is a hypothesis of its own, HYPOTHESES entry 23.
40. **The binding that costs content, `binding-v1`: the give at the
    contact** (the model owner's records 115 and 137 of 2026-09-20; the
    physicist's read-only design `docs/designs/binding_v1/DESIGN.md`,
    sections 1 to 6, candidate A, record 132; `engine._give`, `engine._contact`,
    `world.BINDING_RULE`, `NatureBeamWorld.binding`;
    `tests/test_binding.py` (a) to (d); series N,
    `examples/events/binding/`). A hypothesis beside the law with its own
    identity and no new key. **The rule, one condition on the verb GIVE:**
    at a contact under `measure` (the momentum hand-over of note 31 (ix),
    the first hand-over of a contact) the refused body GIVES to the flight
    the paid content it carries: for every paid family other than its own
    that it holds (`held`; a lamp's own paid content is not carried and
    never given) with the quantum h, `held // h` units of content h as one
    row (age 0, the body's phase and number, no record) at the body's Node
    on the heading opposite to the refused step, away from the occupant
    (the step's sign, the Link the drive fired on the axis, not the
    momentum's: under the signed drive of record 126 the two differ at a
    reversal, as the register's neutron shows at its first contact, its
    momentum +270 720 after the proton's hand-over and its step -x);
    `held mod h` stays held; the body takes the recoil, minus the row's
    label (Q x content per unit along the heading, the one label of note
    23, checked before it is formed), toward the occupant. A body that
    carries nothing gives nothing: the contact is the hand-over alone, bit
    for bit. Why the give is at the contact: it is the one moment the law
    already treats a body as a paid arrival at another body (note 31 (ix));
    what a click of a paid arrival takes is the amount, its content and its
    label (step 4), and the contact takes the label's component alone,
    since taking the content would merge the bodies; binding-v1 lets the
    content the body carries LEAVE at that moment, a TAKE turned into a
    GIVE so that two bodies stay two. Why away from the occupant: a row
    given toward it is taken by its entry for the family (`measure` by the
    keys), a swap with no defect; given away, the content leaves the pair
    whole and the picture is nature's, n + p -> d + gamma, the gamma
    leaving, the pair recoiling inward. **The fates**, all existing rules:
    on a heading a row makes its first Link at age 1 and its second at age
    3 (the flight rule, T = 110), so with the family's `lifetime` L = 3 it
    clicks on the border `lifetime` two Links from its birth with its
    content, the released binding energy, measurable as clicks (note 31
    (vii)); a body on its line reads it by its entry, `measure` (the keys'
    rule for a paid arrival) TAKES it (the content joins the body's held,
    booked `measured`), `rerelease` re-creates it on that body's fan, `pass`
    and `read` let it go on to the border. After the give the body carries
    nothing and every later contact is the hand-over alone: the pair is
    stable for ever; the closed loop of record 115 (re-created by the
    partner for ever) is not reachable without a second rule (a re-creation
    on the reversed arriving direction, a retro-mirror on PASS) and is not
    built. **The books:** the family's measured line, initial + measured =
    current + spent + escaped, with the give on `spent` as a lamp's release
    books it; the row on the transit and content lines (`released`) until
    the border books it on `lifetime` (summed into `escaped`) or a body
    absorbs it; the momentum: the recoil on the giver's label, the row's
    label on the transit line, the border's `lifetime_momentum` at the
    click; no remainder (`held mod h` stays held, nothing is rounded). The
    `contact` record gains `given` beside `component` (the content given at
    that hand-over, summed over the paid families the body carried, 0 on
    a later one; the books keep the split per family, and a world that
    holds two paid families would want it per family: none does), written
    from the moment the run holds the fact; `run.json` carries `binding-v1`
    under `hypotheses` from the same fact. **The fact of the run** (the
    physics-rule review's should-fix, 2026-09-20): the parser knows what is
    held at load (`NatureBeamWorld.binding`: a measured event holds a paid
    family other than its own), but the rule fires on the run-time `held`:
    a body of a free family that TAKES a paid row under the keys' `measure`
    (fate (c)) carries it from then on and gives it at its next contact. So
    the engine holds the fact (`NatureBeamSimulation.binding`), true at
    load when a body holds a paid family and raised at the first give
    otherwise; from then on every `contact` record carries `given` and the
    run's record the identity (`NatureBeamSimulation.hypotheses`, what
    `run.json` writes); `tests/test_binding.py` (f): a declared `bond` row
    taken at tick 1 by a body that held none, given at its contact at tick
    3, the record with `given` 2, the border click at tick 6, `binding-v1`
    in `run.json`. Two more readings of the design, stated: a body on a set
    of Nodes gives its row at its centre Node, whole, on the one heading
    (not apportioned over its Nodes as a lamp's release is; the momentum
    share rule over several occupants untouched); an occupant whose share
    of the component is 0 takes no hand-over and triggers no give. **The
    identity:** every world without a body that holds a paid family at
    load or takes one during the run reads as it did, byte for byte (no
    registered world does either: the gate set replays identical,
    VALIDATION); `beam-v1` is unchanged without such a body. **Locality
    and integers:** the contact reads the destination Node's occupant as
    the step already does (one Link); the give reads the giver's own held
    content and the heading of its own refused step; the row crosses one
    Link per interval; no partner content, no memory of partners, no host
    total; fixed work, one row per paid family carried per contact; the
    division by h exact with its remainder held; the label's product and
    the recoil bounded before they are assigned. **What it gives** (the
    design's section 2, series N): the register's deuteron with `bond`
    (h 1, L 3) held 2 per nucleon gives 2 units per body at its first
    contact, two border clicks of amount 2 and content 2 at (8, 10, 10)
    and (13, 10, 10), the escaped content 4 = 0.109 % of 3677 (nature
    4.353 m_e, 0.1185 %; the register's grain is 1 m_e), the mass a
    detector reads 3673, the push on p 310 956 229 248 before and
    310 945 171 840 after (the reader's gravity charge 1835); the size is
    one declared width (record 106: every content is an input). The give
    is per body, so the alpha gives 8 units, the ratio 2.0 in energy to
    the deuteron where nature has 12.72: no form of the rule with one
    declared value gives nature's alpha, stated so that it fails, and not
    tuned. What it does not give: the deuteron/alpha ratio without a
    second value; "every family paid" (the design's section 7) does not
    give the defect and costs two rules, recorded as a direction. The
    register's pp threshold G = 7111 becomes 7112 once both protons have
    given (a prediction, marginal and exact; not run in series N, unread).
    **One design pin read outside** (series N, the review's finding): the
    design's "momentum: measured + transit + escaped = 0" (DESIGN section
    2) reads +270 720 on x in B1 from tick 16 on, and nonzero in B3 from
    tick 16. The cause is not the give: before it, p reads n's 1838 free
    units with its gravity charge 1837 while n reads p's 1835 with 1840, a
    gap of 6 x 3008 = 18 048 per interval over the 15 pushes of ticks 2 to
    16 = 270 720 exactly, the third-law gap of record 126 made visible by a
    held paid family that counts in M_A (note 31 (viii)) but is never
    released; after both gave the two pushes are equal (310 945 171 840)
    and the gap stops. A property of held paid content that predates the
    give; the give removes it. Not checked on the engine before the run:
    the exact tick of the first contact (about 16 from the drive's
    arithmetic, met exactly), the alpha line's inner gives.

41. **The fraction-free law: every count an
    accumulator on the reader's record** (the model owner's records 147
    and 148 of 2026-09-20; the mathematician's read-only
    `docs/designs/fraction_free/FORM.md` (its section 1's claim corrected
    by record 148: on the register no lamp and no crowd on a fan runs at
    a constant rate); the physics-rule reviewer's read-only
    `docs/designs/fraction_free/REVIEW_COUNTS.md`; `core.integer.by_drive`,
    `engine.count_owed`, `engine._frame_all`, `engine._suspend`,
    `nature_beam.push_form`, `nature_beam.weighted_flow` (deleted by note
    48, 2026-09-21), the lamp and the release in `nature_beam`,
    `amplitude.cell_of`; `Measured.acc_*`;
    `tests/test_fraction_free.py` (a) to (f); the register re-registered
    in one batch, MIGRATION "The fraction-free law"). No new identity: an
    integer form of the same counts under `beam-v1`.
    (i) **The one primitive.** Every count of a body is `by_drive` on one
    bounded integer of the body's own record: the accumulator gains the
    count's rate at the self-creation, the count is the whole part it
    then holds in units of the count's denominator, that much is
    subtracted, and the remainder stays below the denominator, its one
    owner (the local integer operation contract's "declare the remainder
    owner"), nothing at a Node. The residue is the phase of the count
    within its cycle, what the clock has already made toward its next
    whole count (the model owner's reading, record 150 of
    docs/LOG_2026-09-20.md), which is why the record carries it ((vi):
    a run resumed without it is another run). The counts and their records: the owed
    count `acc_owed` (the rate `counted x n` at `suspension` [n, d],
    below d; `count_owed`), the free release `acc_release` per family
    (the rate `held x n` at `release` [n, d], below d), a lamp's rate
    `acc_lamp` (below d of `rate`), the turn `acc_turn` (the rate
    `content x n` at K = [n, d], below d; the phase is the turn's count
    mod N as before), the push per column and axis `acc_push` (below
    Lambda_c^2, (iv)) and the step's `drive` as note 17 built it (the
    doppler weight's rows per direction and axis, `acc_flow`, left with
    the key on 2026-09-21, note 48). `by_clock(age, n, d)` is the constant-rate identity: from
    an empty accumulator at age 0 and a rate of one sign the two give the
    same integers at every self-creation and the accumulator holds `(age
    n) mod d` (FORM.md section 1, proved; test (a) on every count over
    10^4 self-creations). The counts are one table on the body's record
    (the model owner's direction, "where is the table?", record 150 of
    docs/LOG_2026-09-20.md: `Measured.counts`, a `CountTable` of `Count` rows built by
    `measured.counts_table` from the world's rates: the name, the source of
    the numerator, the index and axis, the rate's factor, the denominator,
    the cap `at_most` and the accumulator), and one loop,
    `CountTable.advance`, runs every row of a count through `by_drive` and
    hands the whole parts to the count's consumer at the stage of the
    interval where its numerator exists (the frame for the turn, step 5
    for the release and the lamp, `_suspend` for the owed count, `_move`
    for the drive, the reading for the push): a future count is a new
    row, not new code. What remains read off an age is a key (`ages_at_key`:
    the lifetime, the age bound, the clock trigger; a comparison, no
    rate) and the rows' phase per interval of age (`by_clock_rows`: a
    ray's rate is its family's `phase_per_link`, a constant over its
    flight, so the identity's case, with no record to hold an
    accumulator). The turn by momentum under `action` (note 30 (ii)) was
    left as built by the first form of this note, the one count whose
    rate a push changes that was not an accumulator; by the model owner's
    record 155 of 2026-09-20 ("no registers at Nodes, no tables": one
    rule, no exception) it is the `action` row of the table per axis: the
    row gains |p_a| x N at every Link the step rule counts on the axis
    (crossed, lost to an earlier axis's step, or refused at a contact) and
    the whole part over h turns the phase at the Link crossed, the count
    of a Link not crossed discarded as the count off the Links stepped
    skipped it; the same integers as `by_clock(k0, |p| N, h)` at a
    constant momentum (test (d) of `test_nature_beam_body` and (e) of
    `test_step_drive` unchanged), the exact sum of |p| N over the Links
    where the momentum changes along the path (series H, the register's
    dated line: the count off the Links re-priced every earlier Link at
    the present momentum). The product formed at run time is |p| N alone
    (the parser's bound on ticks x |p| x N stays as declared).
    (ii) **Why the count of a changing rate is the accumulator's** (the
    physics-rule reviewer's reading, record 148). Under E = h f the turn
    is the lamp's frequency, `content x n / d` per self-creation, and the
    number of turns a clock has made is the whole part of the integral of
    its frequency over its history, which the accumulator holds and
    nothing else; `by_clock` at the current rate re-prices the whole age
    at today's rate, a history that never happened, and its drift has no
    bound (on the Bell lamp of content K + 2, paying 2 per birth: +1 turn
    in 160 births, +9 in 20 000, +1089 in 200 000). Every registered lamp
    pays at every birth (its frequency falls) and every clock on a fan
    reads a crowd that changes at every interval (the deuteron's rows
    dwell 1 or 2 intervals: 128 800 and 104 880 at the proton), so the
    "constant rate" that made the two forms bit-identical held on no
    registered lamp and no crowd; the owed count is then the integral of
    the potential along the clock's history (note 25), not `age x k_now /
    d`: on `weak/j3_deuteron` 69 intervals waited of 700 in place of 80,
    the same on both nucleons, the verdict BOUND unchanged, the neutron
    firing at 568 (577) and its beta clicking the shell at 581 (590) with
    the same content at the same Node.
    (iii) **The one discarded count.** A lamp's accumulator advances at
    every self-creation of the lamp; a self-creation whose turn is 0 (a
    stall: the clock's accumulator short of one turn) or whose phase
    falls outside the lamp's window births nothing, and the count the
    lamp's accumulator gained there is taken out and lost, as the count
    off the clock was unread at such a self-creation; not banked for a
    later self-creation (a window is a gate on the clock's phase, not a
    queue; a declared choice, `nature_beam` at the lamp's count).
    (iv) **The push.** Per column c the rate `V x
    E_c n_c / (D_c d_c)` is lifted to the column's one denominator
    Lambda_c^2, Lambda_c the least common multiple of the families'
    value denominators in the column (`world.column_scales`: every
    reader's charge denominator D_c and every arriving value's d_c divide
    it), and counted on `acc_push[c][axis]`, signed as the drive is (a
    reversed flow first cancels what it had accumulated), below
    Lambda_c^2 in magnitude; Lambda is 1 on gravity and on charge wherever
    the charges are whole (every registered world but the series 7 pair),
    where the push was exact already and does not move. The lifted
    product is tested by division before it is formed and refused naming
    the column (`test_columns` (a): a refusal of its own where |V E n|
    Lambda^2 / (D d) does not fit the register with coprime denominators
    of 30 bits, never elsewhere); Lambda_c^2 itself is tested by division
    where Lambda_c is formed, and a column whose square leaves the
    register (Lambda_c above 2^31 - 1) is refused at load naming the
    column and the bound, not at its first push (`world.column_scales`;
    test (g); the physics-rule review of the branch,
    `docs/designs/fraction_free/REVIEW.md` section 4). Per interval the
    count differs from the floor off the clock by at most one label unit
    per column, axis and interval, and the sum over any period is the
    whole part of the sum of the numerators exactly (FORM.md section 2;
    tests (b), (e); the weighted flow's rows under `doppler`, `acc_flow`
    at the denominator G Q |v_d|^2, one per direction, and their tests on
    the doppler bar, 396672 for 396673 off the clock, left with the key on
    2026-09-21, note 48).
    (v) **The ladder at the click.** The cell of a record's u is the first
    k with `2 T u + T <= 2 N C_k`, the comparison of two products
    (`amplitude.cell_of`), which is `u < b_k` with the rung `b_k = (2 N
    C_k + T) // (2 T)` at the nearest integer: no division, the same
    integers, the rungs a report on the gather line (test (f) on every
    gather of the keyed worlds and on random ladders); the click's
    rounding is the nearest-integer rung, declared, once per record.
    (vi) **The record.** `state.json` and `run.json` carry the
    accumulators per measured event under `acc` by name (`owed`,
    `release`, `lamp`, `turn`, `push` per column, `flow` under the key),
    beside `drive`; a run resumed from a state is the unbroken run in
    every record (test (c)); a declared `acc` in a world file is refused.
    (vii) **The alignment of a lamp's births with the ticks.** A paid lamp
    paying c per birth keeps one birth per interval over T intervals from
    the least content K + c (T - 1) / 2 rounded up, K + T - 1 at c = 2
    (K + 159 for the Bell lamps' 160 births): the frame reads the content
    before the birth pays, so the k-th self-creation adds M0 - c (k - 1)
    to the turn's accumulator, which after T of them holds T M0 - c T
    (T - 1) / 2 less the K of each turn (the physics-rule review of the
    branch, `docs/designs/fraction_free/REVIEW.md` section 5, and its
    replay: K + 159 gives 160 births of 160, K + 2 the stall at tick 4);
    K + c (T - 1), the bound stated first (REVIEW_COUNTS section 2 (b),
    MIGRATION), is sufficient and not the least; below the least content
    its exact clock stalls where its content has
    fallen below K (the Bell lamps of content K + 2, paying 2 per birth,
    once at tick 4; the L worlds' lamps of 2^20 at tick 2 and its pair
    lamps at tick 3), so the tick of a birth is
    not the age of the lamp's clock, and a pair is read by its record
    (the birth ordinal, `record` and `u` on every click and pass line),
    never by a tick window or a tick offset. S = 176/64 on the CHSH
    labels, the cells, the choosers' fifteen E and S = 156/64, the
    Mach-Zehnder ports and the GHZ triples do not depend on the
    alignment: a click is a function of the record's u and the settings
    alone, the same integers read by ordinal on both counts (the
    reviewer's `pair_by_ordinal.py`; `tools/bell_chsh.py`,
    `tools/bell_choosers.py`, `tests/test_amplitude_pair.py`).
    (viii) **No tables, no remainder discarded, and the law's remaining
    divisions** (the model owner's record 155 of 2026-09-20; the
    derivation mathematician's inventory, `docs/DERIVATIONS_BEAM.md`
    section 1.3, whose items 1 to 6 this note and the branch `no-tables`
    replace and whose items 7 to 14 are listed below as found). The
    symbols, named once for this note: **v** = (a, b, c) the direction
    vector of a ray's flight, S_1 = |a| + |b| + |c| its Manhattan length,
    Q = 64 the label's scale, T_d = isqrt(3 |**v**|^2 Q^2) the direction's
    resolution, tau the age of a row, m(tau) the count of Manhattan steps
    made by the age, r = 2 S_1 Q the position accumulator's rate and d = 2
    T_d its wall, e the Manhattan step of one interval (0 or 1), p_a the
    momentum's component on an axis, N the steps of the phase circle and
    h the world's `action`. The flight: the Link a ray crosses at an age
    is `Flight.walk_step`, one Manhattan accumulator started at T_d,
    gaining r per interval over d, the interval's step e = [acc + r >=
    d], and the step is the m-th unit step of the direction's line, whose
    axis is the Bresenham choice (at Manhattan step j the axis maximising
    |v_i| (j + 1) - S_1 |pos_i|, v_i the vector's and pos_i the position's
    component on the axis, the lowest axis on a tie: the deficits' argmax
    carry, periodic in S_1, computed once from the vectors at load,
    `lines`); the pair (m(tau), the residue (tau r + T_d) mod d) is formed
    in one place, `Flight.accumulator(direction, age)`, which `walk_step`
    reads for the step (since 2026-09-21, the model owner's word on the
    flight's accumulator, record 299, through `nature_beam.by_drive_rows`,
    the array form of the one count primitive `core.integer.by_drive`,
    equal to it row by row: the residue gains r over d and the count
    gained is the step, the accumulator after the next age's residue;
    the pair off the age is the verb's constant-rate identity applied
    tau times from T_d, as `by_clock` is of `by_drive`, so the row
    carries no field) and the click's exact phase reads for the residue
    at an arrival (TWO_SLITS.md section 2; test (f) of the flight); a
    ray's rate never changes over its flight, so both counts are read off
    the whole age and the row carries no field (the inventory's 1.4:
    "keeps the age and computes the step from it"; a per-axis position
    accumulator is NOT this form, two Links in one interval on (1, 1, 0)
    and 22 for 24 at age 29, and was not built). A row's phase is a point
    of Z_N on the record, and of Z_{N d} only through the age (nothing
    discarded). The push by a record row's share: `share_of` keeps the
    remainder on the row (`share_x`, `share_y`, `share_z`: the part of
    the row's push on a body not yet delivered, below the record's
    multiplicity, summed at a merge, carried from reader to reader so
    that a row read at every
    interval of a passage pushes the exact sum; it leaves with the row
    when the row is absorbed, to the books' `remainder` line with the
    rest of the label, or escapes: the `remainder` line then reads what
    left with absorbed rows and nothing of a row that lives; test (h)).
    A set's release over its Nodes: `place_over_nodes`, the `place` rows
    of the body's table, one per Node, the Node's fractional claim on
    the body's releases carried from row to row and self-creation to
    self-creation, every Node within one unit of its equal share of all
    the body has released (until then the leftover units went to the
    Nodes counted from `age mod w`, a tie reset at every row; test (i);
    series H, the catalog's `clock_near_mass` and `sun_planet` re-read).
    **The law's remaining divisions**, every `//` of `core/integer.py`
    and `events/` at run time, so that the claim "no division at run
    time discards a remainder" is checkable; every one is of a class
    below or is `by_drive`:
    (1) the primitive: `by_drive` (`core.integer`, `abs(drive) //
    denominator`); its constant-rate identity `by_clock` (`core.integer`;
    `by_clock_rows` in `nature_beam`: a ray's phase per interval of age
    at its family's `phase_per_link`, a constant over the flight; the
    age against a key); the flight's counts off the age
    (`Flight.manhattan_steps` and `Flight.accumulator`: `held //
    denominator` and `held % denominator`; `Flight.walk_step`: `(residue
    + rate) // denominator`); `share_of` (`abs(total) // multiplicity`,
    the remainder on the row); `place_over_nodes` (`divmod(amount,
    ways)`, the leftover to the claims).
    (2) an exact division by a common divisor, no remainder: `reduced`
    and every `// common`, `// gcd`, `// bounded_gcd` (`core.integer`;
    `amplitude.lcm`, `common_denominator`, `rungs`, `complete`;
    `meeting.meet`; `world.column_scales`; the periods in
    `nature_beam.direction_flight`); the lifts by a least common multiple
    (`amplitude.rungs` and `cell_of`, `denominator // m`; `meeting.meet`,
    `denominator // d`; `nature_beam.push_form`, `scale // denominator`);
    the columns' Lambda lift; the arms' partition of the directions
    (`ways // arms`, `way // paths` at the lamp's births in
    `nature_beam`, exact by the parser's refusal); the whole quanta a
    lamp or a give can pay (`held // cost` at the lamp's births, `held //
    quantum` in `engine._give`: the remainder stays held as content);
    the half-angle tables' step (`amplitude.half_angle`: `2 * steps //
    size`, `index //= factor`, exact by the refusal of an odd setting); a
    record's multiplicity over a split's norm (the layer's `cells` in
    `amplitude`, exact by construction).
    (3) a declared rounding computed once from the keys or once per
    record: T_d by `integer_root` and u_d by `unit_label` (at load);
    the ladder's rungs at the nearest integer (`amplitude.rungs`,
    `node_choice`: the cell is the comparison of products, the rung a
    report); the half circle `modulus // 2` and a window's half width
    `width // 2` (constants of N and the width); the speed at the grain G
    (`quantised_speed`, `G |p| // D`, the remainder below 1 / G by
    declaration, note 38 as it was) left with the crossing rule on
    2026-09-21 (note 48).
    (4) a guard or an addressing: every `MOMENTUM_BOUND // x` and
    `AMOUNT_BOUND // x` (a bound tested by division before a product is
    formed: `measured.column_charges`, `engine._frame_all`,
    `world.column_scales`, `_families`, `_column_budget`,
    `meeting.arc_shift` and `meet`, `nature_beam.label_overflow_rows`,
    `label_weights`, `coherent_pointer` and its `POINTER_STEP_BOUND`,
    `apply_gate`, `push_form` and the lamp's births), the parser's
    ceilings (`flight_bound`, `_lamp`, `_measured`, `_column_budget`: the largest
    values a run can form), a body's span half (`world.body_nodes`) and
    the store's strides (`NatureBeamStore.coordinates`). The `//` of
    `core/phase.py` (the cosine and sine tables of the circle, a declared
    rounding at load) are outside this list's scope on purpose: a table
    of the circle's constants, not a count of the law. The functions are
    cited, not the lines, so that a merge does not move the citations.
    (5) an exact apportioning within one event (`apportion_whole`,
    `integer.py` 124): the whole is distributed, the units left going to
    the largest remainders with the ties by a rotation; nothing of the
    event is discarded, the rotation is a declared tie rule: the
    re-release of a row over the admitted directions and the contact's
    hand-over over the occupants.
    (6) **a remainder discarded at the meeting**, to become an
    accumulator on the row under the meeting verbs (record 155 step 5;
    not changed on `no-tables`): `adv = (|t| + Q // 2) // Q`
    (`meeting.register` and `register_inverse`: the crowd met rounded to
    the nearest whole unit of Q every interval, the rest dropped; the
    inventory's item 9) and `norm //= denominator` after the
    `integer_root` per interval (`meeting.meet`; item 10: the one root
    evaluated on the lattice per interval on a varying t, whose discards
    do not telescope; a change of the meeting's law, for the owner);
    `total // modulus` (`meeting.register`) is the torus reduction with
    the remainder kept as the phase, lawful, and `(advance - after +
    modulus - 1) // modulus` (`register_inverse`) the whole turns of the
    same advance.
    **Found by the inventory and left as built** (to be pinned before
    any change): (7) a coincident drive fire on a later axis in one
    self-creation pays its D and crosses no Link (`engine._move`: one
    Link per interval, the later axis's Link dropped; the torus form
    would not advance that axis past its wall, so it fires at the next
    self-creation; only bodies with two nonzero momentum components and
    coincident fires move, series D, H, the diagonal stars of G2, the
    kicked deuteron); (8) a refused step under a `read` or `pass`
    contact loses its drive's D with nothing handed (`engine._move`,
    `_contact`; the torus form adds D back; no registered world declares
    such a contact on the gate set); (9) the `action` row's whole part at
    a Link not crossed (a Link lost to an earlier axis's step in the same
    self-creation, or refused at a contact) is discarded at run time: the
    row gains |p_a| N on every axis whose drive fired and the whole part
    over h is delivered only on the axis whose Link was crossed
    (`engine._move`), the residue kept, so no remainder is lost but a
    whole count is, as the retired rule's `k0` skipped it (the wording of
    note 30 (ii) as amended above: a step lost or refused adds nothing to
    the phase; the inventory's item 6, "a second discard inside the
    first"); the torus form of item 7 would remove the lost Link's
    discard; pinned before any change by `tests/test_step_drive.py` (e):
    the coincidence body of (a) (content 1, the momentum (64, 64, 0), D =
    128 on both axes) under `action` 7 at N = 64 holds, after 10
    intervals, `acc.action` [5, 5, 0] (the residue of five counts of 4096
    = 7 x 585 + 1 on each axis) and the phase 45 = 5 x 585 mod 64 from
    the x row alone, the y row's five whole parts, 2925, never delivered
    (the phase would read 26 with them; the physics-rule review of
    2026-09-21, item 2).

    **The tables the engine carries at run time** (2026-09-21; the paper's
    referee under the owner's direction, record 316, that a formula's
    derivation must not depend on the formula itself: the paper states the
    caveat, the tree states the fact). Every table below is computed once
    at load from the declared integers of the world and read by the rules
    as a constant, so the three tests of record 202 read the rule (the
    walk, the click, the collision, the meeting) and never the load; a
    rounding taken at load is a declared rounding of the world (record
    156, "C and S computed from N as a declared rounding"), not a formula
    inside a rule.
    - The flight's constants per direction (`nature_beam.direction_flight`,
      the `Flight` of the world's direction set): from the declared
      vectors **v** and Q = 64, S_1 = |a| + |b| + |c| a sum, T_d =
      isqrt(3 |**v**|^2 Q^2) an integer root at load (a declared rounding),
      the period L_d by two gcds, the line by the deficits' argmax (the
      Bresenham comparison), and the unit label **u**_d (`unit_label`), an
      integer root per component (a declared rounding). The walk reads r =
      2 S_1 Q and d = 2 T_d as the direction's integers, never the root.
      Pinned: `tests/test_nature_beam_label.py` (a) (**u**_d),
      `tests/test_nature_beam_flight.py` (a) and (g) (T_d, the periods, the
      lines).
    - The phase circle (`core.phase.phase_circle`, `phase_cosines`,
      `phase_sines`, cached per N): from the declared N, cos(2 pi d / N)
      and sin at the scale 256 by fixed-point series in integers, rounded
      to the nearest integer: the declared resolution of the click's Gram
      form (the click's notes 45 and 46) at 1 / 256; the pointer and the
      click read the entries as declared integers. Pinned:
      `tests/test_group_structure.py` (b) (equal phases 65536, opposite
      phases exactly the negative, C^2 + S^2 within 361 of 65536) and the
      amplitude gate's xfail at N = 4096 (`tests/test_amplitude_gate.py`,
      the rounding named: E at 2900 / 4096 against the cosine's 2896.3 /
      4096).
    - The collision table (`nature_beam.collision_table`, cached once):
      from the eight slots and the class rule of section 4, the shift as
      a permutation of the 3^8 slot states, generated; no closed form, no
      rounding. Pinned: `tests/test_nature_beam_collision.py` (b),
      `tests/test_group_structure.py` (c).
    - The arc table of the meeting (`meeting.arc_table` on the unit labels,
      the permutation per target on demand, cached): from **u**_d their
      norms as sums of squares, and per target an integer root of the
      target's norm (a declared rounding at the meeting's read), the
      permutation by integer comparisons. Pinned: `tests/test_meeting.py`.
    - The cube's group (`core.game_board.cube_symmetries`, cached): the 48
      signed axis permutations, generated; read by no rule at run time,
      the tests' constant.
    Not tables: the window (the one floor `window_admits`), the ladder's
    rungs (per record at its completion, from its offers), the counts table
    of a body (its state, not a constant) and the flight's accumulator (off
    the age). On the cosine table: the exact form of the phase is the
    record's phase-count vector **f** in Z[Z_N] (note 45) and the click's
    comparison is of the norms |**f**(zeta_N)|^2, algebraic integers of
    Z[zeta_N]; with no table at all that comparison is a sign test of an
    algebraic number on its cyclotomic representative, a verb outside the
    six, so the table at 1 / 256 is the declared rounding that keeps the
    comparison on rational integers; without it every `wave` record's
    square and every rung of the ladder would move by the rounding, the
    gate's E at N = 4096 first (the xfail). The owner's word is given: the
    table stays and is a declared input of the law beside Q, S and N, the
    circle's rounding (the model owner, record 328 of [the log](LOG_2026-09-20.md),
    the fixed-point transforms its precedent). A statement, not a change.
42. **The group structure named** (2026-09-21; the vector program, record
    191; the architect's item 3; names and types only, no rule changed and
    every registered integer the same): the collision table is the action
    of the cyclic group on the slot states by the shift, its orbits the
    classes of section 4 (`CollisionTable.act`, `orbit`, `period`); the
    world's circle of N steps is the cyclic group of the phase with its
    unit vectors (`core.phase.PhaseCircle`, carried by the tables as
    `circle`; the two scalar turns of the engine and the layer's tables
    read it); the 48 signed axis permutations are the cube's group with
    its hand as the pseudoscalar (`core.game_board.cube_symmetries`,
    `symmetry_hand`), the same 48 maps the collision test enumerated. The
    tests state the properties (closure, inverse, the orbit-stabilizer and
    Burnside counts, one cycle per class) in place of the counted orbits
    (`tests/test_group_structure.py`; `test_nature_beam_collision.py` (b)).
43. **The mass of a bound set is its total content** (2026-09-21; the
    owner's direction, record 273, "about the masses and the quarks, what
    you found: put it into the generic law, on the group";
    [DERIVATIONS_BEAM 19.1](DERIVATIONS_BEAM.md#191-the-generic-statement-the-mass-of-a-bound-set-is-its-total-content),
    binding-v1's read mass of record 115 with section 17's energy carried
    as the state; no rule changed, no run moved): the mass a detector
    reads of any bound set is the set's total content, M = H + F - E, with
    H the content its bodies hold (the `held` and `content` of their
    records), F the content of its rows in flight between them (the sum of
    amount x content per unit over the set's rows in transit) and E the
    content escaped (the escape click at the lifetime L: the released
    binding). It is a reading of the state vector, an addition over the
    record and its rows, and it passes the three tests of record 202 in
    one sentence each: generic, one sum with declared integers over any
    family, every family paid and the strong column read per unit with
    one sign (19.1: the bond's content in flight is blind to the charge
    and to the held content, the same F for `u u d` and `u d d`); vector,
    the group-ring addition on the record's held content and its rows'
    content, no root, no float; local, the record and its rows at the six
    neighbours, nothing kept at a Node, the sum over the set a host reading
    of the books labelled so. The part in force today is the held content,
    binding-v1's read mass (note 40; the deuteron of series B1 with the
    `bond` family: the held sum 3673 of the 3677 declared, the 4 escaped
    the binding energy, `examples/events/binding/README.md`, "What was
    measured"); the in-flight part enters with covariant-readings-v1
    (record 270). The register: the binding series has no
    `expectations.json`, the B1 row of its README carries the read mass
    ("the state `held` and the mass read") and no test derives it
    (`tests/test_binding.py` tests the give on its own worlds), so the
    derive-and-compare test is missing: a `read_mass` entry beside the
    world (the held sum off the record's `measured`, the in-flight content
    off the books' transit line, the escaped off `escaped`, M = H + F - E
    at the cap) and the test that derives it from the run and compares,
    for the Boss to order.
44. **The parity, the group's two classes** (2026-09-21; record 273;
    [DERIVATIONS_BEAM 19.3](DERIVATIONS_BEAM.md#193-how-the-quarks-bind-generically-the-chain-on-the-bipartite-lattice)
    and 18.3, the give per contact Link): the GameBoard's translation
    group has two cosets under the six steps, the Nodes of even and of odd
    x + y + z (the lattice is bipartite: a step on any Port changes the
    parity of the coordinate sum; on a periodic axis of odd extent the seam
    joins the two classes and the statement holds on the open GameBoards
    and on the even periods, which every registered world has), so a Link
    always joins the two classes and no three Nodes are pairwise adjacent:
    three bodies at adjacent Nodes bind as a chain, a line or an L, the
    centre of one class and the two ends of the other, never as a
    triangle; four bind at most as a square (the lattice's 4-cycle), the
    form series I's alpha took and lost (the line held, the square
    dispersed). The parity is the law's only colour: a contact is always
    between the two classes, a set of three has two of one class and one
    of the other, and a third class does not exist on the six Ports (a
    design that needs three colours is a hypothesis outside the law, record
    251). It passes the three tests in one sentence each: generic, a
    statement on the group with no family name; vector, the comparison of
    x + y + z modulo 2, a Euclidean division with the remainder kept, the
    same verb the flight's accumulator uses; local, a Node's class is its
    own and its six neighbours' is the other. The formula in its three
    places (record 248): this note; DERIVATIONS_BEAM 19.3 with the sign it
    gives (the neutron's negative mean square charge radius from the chain
    `d u d`); in the code the six headings of `core/game_board.py`, each
    one unit on one axis, so that the parity check is a property of the
    Ports and its test (every heading flips the parity; no three headings
    sum to zero) is missing, for the Boss to order.
45. **The exact phase at the click: the phase at the exact time of the
    row's last Link** (the model owner's decision of 2026-09-21, record 163
    (2) of the log of 2026-09-20, "YES, the exact phase at the click from
    the row's two accumulators"; the mathematician's design,
    [TWO_SLITS.md section 2](designs/fraction_free/TWO_SLITS.md) with
    `two_slits_map.py`; the branch `click`). A row of a family with the
    pair form of `phase_per_link`, n / d steps per interval of age, turns by
    `by_clock_rows` at every walk that moves it, so its phase column holds
    floor(age x n / d), the phase of the whole intervals; the flight table
    moves it by whole Links at whole intervals, m(tau) = (2 tau S_1 Q + T_d)
    // (2 T_d) Links by the age tau, so the row arrives at its click at a
    whole age while the exact time of its last Link is made x T_d / (S_1 Q)
    intervals, a rational, `made` the Links the table counts on the row's
    direction. The click reads the phase at that time from the row's two
    counts, the phase per interval and the Links made (`nature_beam.exact_phase`):

        phi = phase - floor(terms n / d) + floor(n made T_d / (d S_1 Q))   (mod N),

    `terms` the intervals the phase holds. Three Euclidean divisions are
    taken here and no other, each named with its class (the standard of
    record 155 (b) for note 41 (viii)): (1) made = (2 made_at S_1 Q + T_d)
    // (2 T_d), the flight's own count of Links m(tau) re-read off the age
    (its remainder is the flight's, derivable from the age and the world's
    constants, never held on the row); (2) floor(terms n / d), the walk's
    whole part re-read to peel it off the phase column (its remainder the
    walk's own, derivable the same way; nothing kept on the row is lost);
    (3) the one division of the click, the numerator n made T_d by the
    denominator d S_1 Q, the numerator within the working register (refused
    beyond it naming the place; on every registered world below 2^53), a
    `divmod` whose remainder is kept and reported. So no division at run
    time discards a remainder the row held: the click line of every row of
    such a family carries
    `exact`, phi, and `remainder`, [the remainder, d S_1 Q]; the row's
    `phase` stays the walk's, the GameBoard's own, and a re-emission carries
    it as before (the phase finer than N across a re-emission is the one
    need beyond this, record 165, not built). Where it is read: a click at a
    measured event and a `sum` re-emitter's end (`terms` = `made_at` = the
    age after the walk, `plan.t_exact`), an open face (the row read before
    that walk's turn: `terms` its age, its last Link the step at that age,
    m(age + 1)) and the border `lifetime` (after the walk). The layer's
    pointer of every end is at the exact phase (`Layer.end`); the crowd's
    readings, the windows, the meeting and the faces' ledger records read
    the path phase as before. A family without the pair form, or a row on
    a rest slot, reads its phase as it is; a row whose direction a
    collision changed reads its age on its present line, as the table does
    for its next step. What moved, re-registered once
    ([MIGRATION](MIGRATION.md#the-exact-phase-at-the-click-on-2026-09-21-the-phase-read-at-the-exact-time-of-the-rows-last-link)):
    `slits_low`'s 64 clicks stay wall 34 (11, 12, 11), screen 15 and faces
    15 (8, 7) but land on other pixels (y = 11, 29, 36, 40, 50, 56, 59, 60
    twice, 61, 70, 77, 84, 90, 107; the reading's total 4834019/4259840 in
    place of 847181/745472, its Pearson with the two-source cosine 0.382 in
    place of 0.368), the reading of one birth agreeing with the run on every
    one of the 80 sets; the design's map expected wall 34, screen 16, faces
    14 because it carried the lamp leg's exact fraction across the
    re-emission and evaluated on a 4096-entry table of floats, where the
    engine floors once on the tables of N = 64 with the re-emission's whole
    phase, as this note says. The Mach-Zehnder worlds with unequal arms keep
    their clicks (64 / 0, 32 / 32, 0 / 64) with their weights and totals
    moved; the equal arms, Bell, GHZ and the gate are bit-identical (equal
    paths have equal overshoots; the label click reads u and the label); the
    cone worlds keep their pins (the pair form at the rate 3: the exact
    whole parts 87 at the axis and the diagonal, the remainders 42 / 64 and
    96 / 128, `expectations.json` under `cone.exact`), the design's 41.75
    and 42.00 being the rate 8's, pinned in `tests/test_exact_phase.py`
    (the axis u + 41 with the remainder 48 / 64, the diagonal u + 42 with
    the remainder 0, a face u + 4 where the walk read u + 56, the bound).

46. **The birth wheel at a declared rate: u one row of the lamp's counts
    table** (the model owner's decision of 2026-09-21, record 180 of the
    log of 2026-09-20, "the wheel was also turned into a generic vector,
    wasn't it?", the decision on record 163 (3); the mathematician's design,
    [TWO_SLITS.md section 8](designs/fraction_free/TWO_SLITS.md) with
    `wheel_map.py`; the branch `click`). A lamp declares `wheel` [r, W], a
    rate like every rate of the world, no default: one `Count` row of its
    counts table (`measured.counts_table`, the name `wheel`, the source the
    lamp's own rate, no cap), advanced by r over W at every birth of a
    record as every count is (`by_drive`); the accumulator before the
    advance is the record's coordinate u on the ladder, u = ordinal x r mod
    W (the ordinal from 0), written on the record and its rows at birth
    (`nature_beam.birth_coordinate`; the `birth` column, the `birth`, `click`
    and `gather` lines' `u`), the rows' birth phase u mod N, and its
    remainder carried in `state.json` under `acc` as `wheel`. The click's
    rungs are on W, b_k = (2 W C_k + T) // (2 T), b_K = W, the cell the
    first k with u < b_k (`amplitude.Layer.complete`, `LiveRecord.wheel`,
    `rungs`, `cell_of`); N stays the phase circle (the tables, the merge's
    cancel) and W is the click's own grain. [1, N] is the count of births
    mod N as built: every registered lamp declares it (a mechanical edit of
    the world files through their generators, the entity definitions and
    the tests' lamps; `tools/amplitude_path.py` reads the wheel from the
    world's lamp), and every such world is bit-identical in its events,
    its `state.json` gaining the row's accumulator; a rebirth at a
    re-emitter that is no lamp keeps u = its count of births less one mod N
    and the rungs on N (the built rule, no key of its own; a re-emitter
    that is a lamp reads its wheel). The golden rate [2531, 4096], the
    nearest odd integer to 0.618 x 4096 over W = 4096 (the Weyl sequence,
    every prefix equidistributed by the three-distance theorem), is the
    generic wheel the map chose against the bit-reversed ordinal (section
    8: the same clicks within one at 4096 births, the same cells filled by
    1024): `slits_huygens` (L2b) declares it and is re-registered as the run
    that shows the wheel (its entry in the register). Pinned before the run
    from the map's section 8 at 4096 births: the bright pixels about 28 to
    29 clicks, the dark 0 to 3, the Pearson of the counts with the
    two-source cosine about 0.96 (the map's 0.963 with the exact phase on
    a table of 4096; the engine's on the tables of 64). The run (the L2b
    entry of the register): the dark pixels 0 to 3 as pinned; the bright
    19 to 51, the mean 39, since the map's 28 to 29 was the screen's fan of
    121 directions (the screen share 0.35) where this world's Farey fan
    puts 0.418 of the total on the screen with its peak at 0.012; the
    counts' Pearson with the cosine 0.891, the weights' own 0.895; and the
    wheel's own statement exact, every cell's count over the 4096 births
    within 2 of 4096 x its weight over the total (within 2 and not one: the rungs are per record, the tables' eight totals at u mod 64, a part in 276, note 37 (xii), so the counts are compared with the first record's rungs), the histogram's Pearson
    with the first record's rungs 1.000 over the 126 cells: the wheel
    turns the weights into counts. Refused: a lamp
    without the key, a bare integer, a rate of 0 and a wheel of 0
    (`tests/test_birth_wheel.py`); the first ten u under the golden rate 0,
    2531, 966, 3497, 1932, 367, 2898, 1333, 3864, 2299 with the phases 0,
    35, 6, 41, 12, 47, 18, 53, 24, 59, and the cell read on the wheel
    (two equal cells, the rungs [2048, 4096]: a, b, a, b, a, a, b, a, b, b,
    where [1, 64] sends the first 32 to a and the next 32 to b).

47. **The crowd audit: what every rule in force reads of its own record
    and of the crowd** (2026-09-21; the owner's question, record 276, "are
    you checking the crowd everywhere?"; the architect's audit of `main`
    at 86b59ba1; a table, no rule changed, no run moved; the numbers 45
    and 46 are the click branch's). The crowd of a reader is the one
    reading set of section 3 step 2: everything at its Node but its own
    number, and the six neighbouring Nodes (LOCALITY-1), read by
    `read_arrivals` as the moments of the arrivals. One row per rule, the
    citation the function and line of `src/event_universe/events/` on
    `main`.

    | The rule | Reads of its own record | Reads of the crowd | The code |
    | --- | --- | --- | --- |
    | the walk (the flight) | the row's direction, age and position accumulator (rate 2 S_1 Q, wall 2 T_D) | nothing | `Flight.walk_step`, nature_beam.py:598; step 1 at 2556 |
    | the escape at a face | the row's position against the open boundary; the face click | nothing | nature_beam.py:2569 to 2574 |
    | the merge | the row's identity fields (Node, direction, age, phase, number, content, record, branch, multiplicity, hand) | the rows at its Node identical in every field but the amount (a phase difference of N / 2 under the amplitude key) | `NatureBeamStore.merge`, nature_beam.py:1260; called at 2553 and 4288 |
    | the readings (the one reading set) | the reader's number (excluded from the set) | the arrivals at the Node: the amounts on their direction vectors, the moments of order 0, 1 and 2 and the age moment | `read_arrivals`, nature_beam.py:450; step 2 at 2679 |
    | the collision | the row's slot (its direction) and its (number, content) class | the single units of the same number and content in the eight slots of a free Node: its own crowd only, never another number's | `collide`, nature_beam.py:2460; step 3 at 2685 |
    | the meeting (`meeting-v1`, the world key `meeting`) | the paid row's label and number | the free crowd's labels at its Node less its own number (`crowd_flow`), the arc permutation toward the target | `meet`, meeting.py:282; `crowd_flow`, meeting.py:244; called at 2693 |
    | the coupling (the push over the columns) | the reader's content and charges as the frame read them (`frame_content`, `frame_charges`), its push accumulators | the label flow V_B of the group of arriving rays, per column | `push_form`, nature_beam.py:2295; called at 3429; the frame `_frame_all`, engine.py:445 |
    | the reading's weight under `doppler` (note 38; deleted by note 48 on 2026-09-21, the row kept as the audit's record) | the reader's momentum as the frame read it (`frame_momentum`), its flow accumulators | the arriving rows' directions and labels per direction | `weighted_flow`, nature_beam.py:2219; called at 3421 |
    | the click's admission (the threshold, the window) | the set's threshold and its window's setting and width (declared), the set's phase | the arriving rows: the amount summed over the set against the threshold, each row's phase against the window | nature_beam.py:2905 to 2977 |
    | the click's choice at a `sum` set (the one click) | the record's own cells' weights and its u: the cell as a comparison of two products | nothing: the ladder is the record's own | `Layer.complete`, amplitude.py:684; `cell_of`, amplitude.py:208, called at 706 |
    | the re-emission (`rerelease`, the split) | the entry's declared weights and turns; the one arriving row re-emitted (its direction, record, branch, multiplicity) | the one row it re-emits, never the set | nature_beam.py:3502 |
    | the gate (`amplitude-v1`) | the entry's declared gate | the pending rows of every record present at the entry: the other records' labels (a crowd of records) | `apply_gate`, nature_beam.py:1898; called at 3791 |
    | the rotation | the row's own label bit and phase; the set's declared setting | nothing | `rotate_rows`, nature_beam.py:1977; called at 3800 |
    | the transformation `become`, the clock trigger | the body's own age at the key `at` (`ages_at_key`) | the count its clock read this interval (`counted`) as the gate `crowd` only: open below the gate, never a rate | nature_beam.py:3720 to 3729; `transform`, nature_beam.py:1538 |
    | the transformation `become`, the click trigger | the entry's window | one arriving row of the entry's family admitted by the window | nature_beam.py:3651 |
    | the clock's count (`counted`) | the body's number (excluded) and the component its entry `reads` | the presence, or the age moment, of every number but its own at its Node | nature_beam.py:3252 to 3255; `measured.count_component` |
    | the owed count | the body's owed accumulator and the world's suspension pair | the count above, times n / d, as the whole part the accumulator gains | `count_owed`, engine.py:131; `_suspend`, engine.py:499 |
    | the turn | the body's content and its turn accumulator at the rate n / d; under `action` its momentum and the Links stepped | nothing | `_frame_all`, engine.py:445 (the turn at 488); the turn by momentum in `_move`, engine.py:512 |
    | the birth (the lamp) | the lamp's rate on its own accumulator, its held content, its birth ordinal | nothing | nature_beam.py:3730 to 3737 (`advance("lamp")`), the births at 3823 and 4008 |
    | the release (a free family's emission) | the body's held content times its rate on its release accumulators | nothing | nature_beam.py:3740 (`advance("release")`) |
    | the drive (the step) | the body's momentum, content and drive accumulators, the world's width | the occupant of the destination Node, one neighbour, when the step is refused | `step_axis`, engine.py:95; `_move`, engine.py:512; `occupant` at 668 |
    | the contact and the give (`binding-v1`) | the body's momentum component and its held paid content | the one occupant's table entry for the body's family | `_contact`, engine.py:696; `_give`, engine.py:803 |
    | the border `lifetime` (the escape click at L) | the row's own age against its family's lifetime | nothing | nature_beam.py:4212 (`ages_at_key`); the age bound at 4325 |

    Of the 23 rows, 13 read the crowd (the merge, the readings, the
    collision within its own class, the meeting, the coupling, the doppler
    weight, the click's admission, the gate, the two triggers of `become`
    (the clock's as a gate only), the clock's count, the owed count
    through it, the drive's contact with the give) and 10 read nothing but
    their own record: the walk, the escape at a face, the click's choice,
    the re-emission (one row, never the set), the rotation, the turn, the
    birth, the release, the border `lifetime`, and the decay's timing (the
    clock trigger's age at `at`, the crowd entering only as the gate). For
    those, the hypothesis under which the crowd would enter, where one is
    stated: the decay, `decay-by-crowd-v1` (DERIVATIONS_BEAM 18.2 (ii)):
    the `become` trigger as the click of the body's u against the crowd's
    cumulative rung, memoryless where the crowd mixes, named and not
    built; the turn, `covariant-readings-v1` (DERIVATIONS_BEAM section 17,
    record 270): the clock's rate E_0 / E with E the energy accumulator the
    pushes feed, so the crowd would enter the turn through the push, named
    and not built; the flight, the meeting already in force under the key
    `meeting` (a row in transit reads the crowd's flow, the one place the
    crowd enters the walk). For the birth, the release, the escape at a
    face, the border `lifetime`, the rotation, the re-emission and the
    click's choice no derivation names a crowd: they stay "no crowd", for
    the owner to decide, nothing invented.
48. **The crossing rule: a row and a body meet once, at the crossing of
    their world lines** (the model owner's record 158 of 2026-09-20, "the
    step reads the crossed Link"; the physicist's design
    `docs/designs/crossing/DESIGN.md` on the experimenter's finding of
    record 151, that a reader read k rows per k intervals toward and away
    alike, because step 4 counted the rows that stepped into its Node and
    the step came after the reading; built on 2026-09-21 on the branch
    `crossing`). The symbols, named once: **e** the heading of the Link a
    body crossed this interval (the zero vector without a step) and
    **e'** the heading of the Link it crossed the interval before;
    **s_1** the step a row made this interval and **s_2** the one before,
    off the flight rule at the row's age (`Flight.walk_step`; nothing kept
    on the row); **u** the unit vector of the row's direction at the scale
    Q (`unit_label`); X a Node of the body's set after its step and O the
    origin of that Node, O = X - **e**. **The order of the interval** (the
    engine's `step`): the frame, then every measured event's step
    (`_move`, in number order), then the law, then the clocks' turn and
    the count owed: a body's departure becomes its arrival as a row's
    does in the walk, so the reading of an interval finds the body at its
    destination and reads there what it met by the step itself; until
    then the step was the interval's last act and the destination was
    read one interval later. The step at a self-creation uses the
    momentum after the previous interval's push (the drive advances by
    it): at a constant momentum the same Links at the same
    self-creations; under a push a fire can fall one interval later than
    it did (the pinned pairs of `test_contact`, `test_binding` and
    `test_paid_charge` moved so; the design's "an adjacent pair that only
    contacts keeps its integers" holds at a constant momentum only). **A
    timing changed with the order**: under a suspension the step no
    longer waits for the interval that pays the count owed; `_move` runs
    at every self-creation (`creating` its only guard) before this
    interval's owed count, so the drive advances at the self-creation
    itself, where until then a self-creation whose count was owed
    stepped in the interval that paid it (`test_push_width` (c): the
    steps 18, 36, 54 became 17, 35, 53, `steps` the whole part of age x
    16 / 144 after every interval for (age - 1) x 16 / 144 after a
    self-creation; note 17's sentence amended, MIGRATION). A
    contact, a give and an escape happen inside the step, before the law:
    a row given at a contact makes its first Link in the interval of the
    give, the rows a body releases in the interval of a step are born at
    its destination with the phase turned at the Link (`action`), a body
    reads its own rows home at its destination in that interval, and a
    body that escapes in the interval of its self-creation carries the
    phase before that interval's clock turn. **The marks**:
    `Measured.step_port` and `last_step_port`, the Ports of the body's
    own two last Links (-1 without a step: no fire, a refused step, an
    escape), set by `_move` at its entry for every measured event and
    read by step 4 as **e** and **e'**; in `state.json` beside `drive`
    and on the `step` line. The same kind of one-interval fact as a row's
    `arrival`; no memory of any row at any Node. **The rule** (step 4,
    `nature_beam`, the one `met`), per row of another number at a table
    entry that is not `pass`:

        C1   (the swap)             e != 0, the row at O, s_1 = -e             -> met
        C2   (the entered)          e != 0, the row at X, s_1 = 0, u . e < 0   -> met
        C2'  (with the step)        e != 0, the row at X, s_1 = 0, u . e >= 0  -> not met
        C3   (the arrival)          the row at X, s_1 != 0                     -> met, unless
        C3'  (over the body's Link) e != 0, s_1 = e                            -> not met
        C3'' (the leapfrog)         e = 0, e' != 0, s_1 = e', s_2 = 0          -> not met

    C3 with **e** = 0 and no C3'' is the reading as built: a body at rest
    and a fixed body read their arrivals as before, to the byte. A rest
    row (**u** = 0) is met by nobody's step. A row younger than two
    intervals made no step before, so C3'' never excludes it. A body on a
    set applies the rule per Node of its moved set with **e** the set's
    step: C1 on the trailing face only (an origin Node not in the new
    set, of free space: a row at a Node held by another body is that
    body's arrival), C2 on the entered Nodes only (a Node whose neighbour
    along **e** is not in the set), C3' and C3'' at every Node of the set.
    The swap rows join the group of the event (gathered with the rows at
    the set; the reading's bound `first_reading_overflow` over the larger
    group, at most the rows at one more Node per Node of the set: fixed
    work). A met row is read on its own direction: an arrival's the
    direction it arrived on (at a body's Node its direction, no collision
    acting there; a swap row's the direction it crossed the Link on), a
    resident row met by the step its own direction (its label along its
    motion); a resident row not met keeps the zero vector (`here`). The
    presence, what the clock counts, stays the rows at the set (rest and
    moving alike) plus the swap rows; the threshold, the window, the click
    and the push read the same `met`. Own-number rows (home), the
    collision, the walk and the meeting are untouched; the reading was
    the one-way border before and is after. **Locality**: the body's own
    two last Links and the rows' own last two steps off the flight rule,
    the Link's traffic this interval (what crossed it, the walk's own
    fact) and the entered Node's residents: nothing kept at a Node, fixed
    work per row. **What it gives** (`tests/test_crossing.py`; the
    experimenter's streams of record 151, a heading stream of one row per
    interval and a reader stepping one Link per k intervals): toward, k +
    55 / 32 rows per k intervals as a COUNT (45 in 32 at k = 4, the
    windows 5, 6, 6, 5, 6, 6, 6, 5; 58 in 48 at k = 8), away k - 55 / 32
    (19 in 32; 38 in 48), at rest k (48 in 48), no row twice and none
    missed; over a period of 32 Links 183 = 128 + 55 and 311 = 256 + 55
    exactly, 74 and 202 away (the one extra the row co-located with the
    reader at the first interval, a boundary of the window): the rate 1 +
    v / c toward and 1 - v / c away with c = 32 / 55, the Doppler of a
    moving reader as the count of the rows it crosses, no weight, no
    grain; a transverse heading stream at exactly the rest rate (32 in
    32); a face-diagonal stream moving with the step at 24 in 32 and
    against it at 36 in 32 on a plane of lines (the lattice's own
    encounter count on a fan direction, not the continuum flux: the
    design's "at exactly the rest rate" and "2 or 3 residents at every
    step" for the diagonals were the physicist's estimate; the pinned
    integers are the rule's, transcribed on the lines' geometry in
    `docs/designs/crossing/crossing_2d.py` before the run). **Deleted with
    it** (record 151, "in both cases the key leaves the code"; MIGRATION):
    the world key `doppler` and `doppler-v1` (note 38 as it was; a world
    that declares the key is refused as an unknown key), the grain G =
    2^12 (`SPEED_GRAIN`), `quantised_speed`, `flux_pair`, `weighted_flow`
    and its bounds, `weighted_flow_factor` and the budget's factor,
    `frame_momentum`, the `flow` rows of the table of counts and
    `acc_flow`, `run.json`'s `doppler`, the nine worlds
    `hubble_stars/doppler/` with their flux expectations, and
    `tests/test_doppler.py`. **Not proved, stated**: a body faster than
    one Link per two intervals (|p_a| > Q S M, possible under pushes) can
    step twice in a row, and the one-interval mark cannot tell a leapfrog
    of lag two from a first arrival: the rule stays local and generic
    there, the one-per-crossing count is not proved (the design's section
    2), and the engine reports the count of such Links once per run,
    `fast_steps` in `run.json` (`tests/test_crossing.py` (f)), no refusal;
    a row whose direction a collision changed at the origin while it
    rested there reads **s_2** off its new direction (the flight rule's
    lookup, the design's choice, nothing kept). The registered worlds
    with a completed step or a fire under a push re-pin (VALIDATION, the
    dated table): series G2 (the run under the rule is the G2 session's),
    the hubble worlds, D, H, the catalog's `sun_planet`, the nucleus,
    binding and weak pairs; every world whose measured events are all
    fixed reads the same records.
