# The algebra visualizer: one page in three layers, the geometry that is the algebra, how it produces the physics, and the clicks, every panel read from a run's record alone (the design before the build; the Algebra Visualizer, 2026-09-23)

The model owner's word of 2026-09-23, 15:33Z, as the Boss gave it (record
1435 of docs/LOG_2026-09-20.md on the Boss's checkout; the log on `main`
at `05e9f103` ends at record 1395, so the number is the Boss's and the
words are quoted from his order): "the visualizer should bring the
algebraic forms and also how it looks in our world: how the clicks look in
our world and how they are born on the board. Show the genericity, then
the physics, then the clicks. One beautiful system where everything is
seen by eye: the geometry, which is the algebra; then how it produces the
physics; then the clicks." Visualization is requested by the owner for
this task, so a page is in scope (the display contract of
[SIMULATOR_DEFINITIONS.md](../../../SIMULATOR_DEFINITIONS.md), "Default run
display": runs are headless unless visualization is explicitly requested).

This file is step 1, docs only: no tool, no engine line, no run. Step 2,
the tool and the page for the two runs named in section 5, published for
the owner as a private Artifact page, starts only on the Boss's word after
his read of this file.

**The rules the page obeys.** (1) It reads recorded state alone: a run's
events (`events.jsonl`), its metadata (`run.json`) and its snapshot
(`state.json`), the world file beside them and, where one exists, the
series' register (`expectations.json`); it never changes a run and it
never runs one. (2) It computes no physics: no rule of the law is
evaluated, no engine table is loaded, no record is stepped again; the only
arithmetic on a recorded number is a difference or a ratio of two recorded
integers, exact (`fractions.Fraction`), the same allowance the visual check
took ([docs/designs/visual_check/VISUAL.md](../visual_check/VISUAL.md):
"a click is counted, a tick is read, a Node is placed"); floats appear in
drawing coordinates alone. (3) Every number carries its kind, in the five
kinds of [ALGEBRA.md](../../ALGEBRA.md)'s head (DETECTOR, GAMEBOARD,
COMPUTATION, HOST, CONVERSION) and two more that the sources already use
(DECLARATION, an input of the world file, as
[ALGEBRA_MASSIVE_RECORD.md](../../ALGEBRA_MASSIVE_RECORD.md) labels it;
PIN, a number of the register written before the run, printed beside the
run's and never as a verdict). A number whose kind is not named is not a
result (the model owner, 2026-09-21, record 281). (4) Every click is a
DETECTOR reading; a board view is a GAMEBOARD diagnostic and is labelled so
(the readings by type in [ENGINE.md](../../ENGINE.md)). (5) Nothing is
pinned, compared with nature or given a verdict by the page beyond what
the run's own register says. (6) The names are
[TERMINOLOGY.md](../../TERMINOLOGY.md)'s: Node, NodeState, Link, Port,
Event, LocalRule, GameBoard, row, body, record, family, detector, click.

**The symbols, named once.** N the phase circle's grain (64 on both runs);
Z_N the integers modulo N; f a record's rows at a Node as one element of
the group ring Z[Z_N]; (X, Y) the click's pointer, the evaluation of f on
the tables C and S at the scale 256; u the birth wheel's value on a
record; Q the label's scale, 64; **D** a direction as a primitive integer
vector; S_1 = abs(**D**)_1 its Manhattan length; T_D its flight period; c
the pace of a light row, 1 / sqrt 3 Links per interval in the limit; tau
the age of a row in intervals; **p** a body's momentum in label units; M a
body's content; S_6 the sum of a record's amplitude at the six neighbours
of a Node; a_before, a_now, a_next a record's amplitude at a Node at the
interval before, the present one and the one to come; r and r' the row's
remainder before and after the division; [num, den] a record kind's pair
on the six-neighbour term ([1, 1] for light); **F** the interval's map on
the state vector **s** with its rate vector **r** and wall d per
component; the six verbs (T) the translation, (B) the bilinear form, (G)
the group-ring addition, (P) the permutation, (E) the evaluation, (D) the
division with the remainder kept and the comparison (ALGEBRA.md chapter
2).

---

## 0. What the design stands on, and the one finding

Read first, in this order, as the Boss ordered: AGENTS.md and
CONTRIBUTING.md; ALGEBRA.md chapters 1 to 4 (the torus, 1.6; the Node and
its six Ports, 1.1 and 7 (i); the state vector and the six verbs, 2 and
2.11; the record, 1.5 and 2.3; the clock, 3.1 and 3.3; the click as an
action, the one deletion, 3.1 and 4.7); HIGHLIGHTS.md section 5.4 (the
lines of records 1139 and 1327 on `main`: a click is an action of the law
on the state, the record ends at the detector and the detector's own
count advances; a detector and an emitter are one generic receiver-inserter
declared Outside, its clock the return to the same point; the lines the
Boss numbers 1423 and 1425 are not on `main` at `05e9f103`, so they are
taken as the Boss states them and not quoted); the display contracts;
ENGINE.md, "The detector's readings by type" (the record's three files and
every field by kind); TERMINOLOGY.md; the reading and rendering tools of
the tree (section 7.1); examples/events/README.md.

**The one finding, stated first because it shapes Layer 1.** The light
rule the Boss names, `3 a_next + r' = S_6 - 3 a_before + r`, is the rule of
`docs/designs/detector_law/DESIGN.md` section 2 on the
branch `detector-law-design` (at `b6131c64`; not on `main`), written in ALGEBRA.md's
verbs by [ALGEBRA_MASSIVE_RECORD.md](../../ALGEBRA_MASSIVE_RECORD.md)
section 0.1 on `main`, and generalized to the pair form
`3 den a_next + r' = num S_6 - 3 den a_before + r` by MASSIVE_RECORD.md
section 1 on the same branch. It is not in the engine on `main`: `main`
runs the Beam Law (`beam-v1`, rows on digital lines by the flight table,
with the record form `amplitude-v1` of every lamp), and no registered run
on `main` records `a_now`, `a_before` or `r` at a Node (no identifier of
that name exists under `src/`). So the light rule's picture in Layer 1
(section 2.5) cannot be read from a run on `main`. This design draws it
from one worked example with declared integers, labelled COMPUTATION and
"not from a run", checked once by the tool's test against the formula,
and it names the day the same panel reads a run: when the rule enters the
engine on `main` and a run records the row (`a_now`, `a_before`, `r`) at a
Node with its six neighbours, the panel reads those lines and the example
goes. This is the one question to the Boss (section 13).

---

## 1. The page in one look

One static HTML file, one column, three layers top to bottom, each layer
one horizontal band with its title, its one-sentence claim from the
algebra, its panels, and under every panel the file and the lines it was
read from. The head of the page names the two runs it renders (section
5), each with its world file's sha256, its model identity, its run's
`source_sha256` (the engine's fingerprint, from `run.json`), its
`initialization_sha256` and its tick count, and carries the legend of the
kinds (section 8). The page is one file: inline SVG, inline CSS, one short
inline script for the two sliders (Layer 2's faces filling by tick, Layer
3's one record followed from birth to click); no external resource, no
image file, no font.

| Layer | Its title on the page | What is seen by eye | The run it reads |
| --- | --- | --- | --- |
| 1 | The geometry that is the algebra | the torus, a Node with its six Ports, a record's state vector, each verb on one Node with its integers, the light rule as one picture; everything generic, no physical name | both (one recorded instance of each verb where a run carries one); the light rule from the worked example (section 0) |
| 2 | How it produces the physics | the same verbs over many Nodes and intervals: a record propagating and read at the faces, the pace c, a foreign object as a declared block with its own pair, a detector-emitter as a declared object, a GameBoard view labelled a diagnostic | run 1 (the light fan at the faces); run 2 (the declared objects, the books, the store) |
| 3 | The clicks | how a click is born on the board beside how it looks in our world: one record's birth, offers, gather, deletion; the screen as the experimenter sees it, the counts against the detector's clock, the interval between clicks | run 2 |

---

## 2. Layer 1: the geometry that is the algebra

Everything in this layer is generic: no family name, no physical word
(no "light", no "mass"); the panels say "a row", "a body", "a record",
"a detector". Each panel has two parts: the algebra's line, quoted from
ALGEBRA.md with its section, and one recorded instance from the runs,
with the integers on the recorded lines.

### 2.1 The GameBoard as the torus

The picture: three axes, each drawn as a circle when the world declares
the axis periodic and as a segment with its two faces when open, the
faces named as the face detectors `face:+x` .. `face:-z` (an open face is
a detector; a periodic axis has no faces: TERMINOLOGY.md, "Face, face
detector"). The line: the translation group Z_X x Z_Y x Z_Z acting on the
Nodes (ALGEBRA.md 1.6). Read from `run.json`: `shape` and `boundary`
(DECLARATION). Run 1 draws an open cube of 65 per axis; run 2 draws
60 x 121 x 1 with z periodic, so one axis is a circle of one Node and the
other two are segments.

### 2.2 A Node and its six Ports

The picture: one Node at the centre, its six Ports +x, -x, +y, -y, +z,
-z in Port order, each Port a Link to a neighbouring Node, the seven
Nodes of the causal front (ALGEBRA.md 7 (i)); beside it, the sentence
that the 48 maps of the six Ports that send opposite Ports to opposite
Ports are the symmetry, the 24 of hand +1 the rotations (the group of
order 24) and the 24 of hand -1 the reflections (ALGEBRA.md 1.1, 1.4,
4.5). No number of a run is here: the Port order is TERMINOLOGY.md's
constant and the page carries it as text; the tool imports no engine
table for it (section 7.3).

### 2.3 A record's state vector

The picture: the state vector of one row, as ALGEBRA.md 2.11 lists it,
(x, **D**, **p**, tau, f, acc_drive, acc_push, acc_owed), each component
a bounded integer or a vector of them, and beside it the recorded
instance: one row's line of `state.json` under `nodes` (its Node
`position`, its family, its direction, its age, its phase, its amount,
its content, its number) and one body's entry under `measured` (its
`position`, `momentum`, `phase`, `age`, `held`, `owed`, `steps`, its
accumulators `acc.*` where written). Both are the store's view, GAMEBOARD
(ENGINE.md, "a replay's or a store's reading"). Run 2's snapshot at its
last interval carries rows still on Nodes and the screen's 121 bodies;
run 1's carries the lamp's body alone, every row having escaped (its
`escaped` line says so, GAMEBOARD).

### 2.4 The six verbs, each on one Node, with the integers before and after

One panel per verb. Each panel quotes the verb's line from ALGEBRA.md
chapter 2 and shows one recorded instance: the integers before and after,
the pair (the rate over the wall, or the pair of the ring's element), and
the remainder where the verb keeps one. Where neither run records the
verb acting, the panel says "not recorded by these two runs" and names
the line that would show it, instead of drawing invented integers.

| Verb | The line (ALGEBRA.md) | The recorded instance and its lines | Kind |
| --- | --- | --- | --- |
| (T) the translation of an accumulator by its rate | 2.1: x -> x + r; a row's age tau gains 1 per interval, its phase turns by its family's pair per Link | run 1: one row from its `birth` line (tick 1, the lamp's Node, `u`) to its face `click` line (`tick`, `node`, `phase`, `momentum` the label): the age at the click is the tick difference, the Links crossed the Manhattan difference of the two Nodes plus the face's one step, both exact differences of recorded integers | DETECTOR (the birth and the click), the differences CONVERSION |
| (B) the bilinear form with a declared matrix | 2.2: the click's weight f^T **G** f = X^2 + Y^2 on the record's element; the push **r** = **C** **a** | run 2: one `record` line of a screen set under the reading `sum`: `pointer` [X, Y] and `record` = X^2 + Y^2 both recorded (the page draws the pointer as an arrow on the phase plane and prints the recorded square; it squares nothing). The push: no body is pushed in either run; the line that would show it is a `step` line's `momentum` beside the body's `pushed` | DETECTOR |
| (G) the group-ring addition: the merge and the cancel | 2.3: f <- f + g on Z[Z_N], the cancel [p + N/2] = -[p] | run 2: the `record` lines of one record (`of` its identity) at one set: several offers, each with its `arm`, `label`, `pointer` and `multiplicity`; the `gather` line's `weight` and `total` are the sum the layer made, recorded. The page lists the offers and the recorded sum; it adds nothing | DETECTOR |
| (P) the permutation of the joint state | 2.4: the collision's shift on the slot states; the split's table selected by the arrival | run 2: one `split` line at an opening (the row in, the rows out with their weights and turns, `u` carried); the collision writes no line in either run (a store operation between rows of one number; the panel says so) | DETECTOR (the split line is a record's row's) |
| (E) the evaluation at the roots of unity: the click's pointer | 2.5: ev: Z[Z_N] -> Z[zeta_N]; the pointer (X, Y) = **E** f on the tables at the scale 256 | run 2: one `gather` line: `u` the wheel's value, `cells` the rungs, `chosen` the cell, `weight`, `total`, `T`; the pointer per label on the set's last `record` line before it | DETECTOR |
| (D) the division with the remainder kept, and the comparison | 2.6: the count is the whole part the accumulator holds in units of the wall, the remainder stays; the comparison the ladder's cell `2 T u + T <= 2 N C_k` | run 1: a face `click` line's `exact` and `remainder` (the exact phase at the click and the remainder of the turn's division, written when the family declares a phase per age); run 2: the `gather` line's `cells` against `u`, the comparison that chose the cell, recorded | DETECTOR |

The rate over the wall is printed as a pair where the record carries
both (the flight's 2 S_1 Q over 2 T_D is the engine's table and is NOT
loaded; the panel names it as the flight's pair in words and prints only
the recorded ages and Links).

### 2.5 The light rule as one picture

The picture: one Node in the middle with its six neighbours around it,
each neighbour carrying its amplitude a_E, a_W, a_N, a_S, a_U, a_D at the
present interval; below the Node its amplitude the interval before,
a_before; above it the amplitude to come, a_next; on the row the
remainder r before and r' after; and the one line

    3 a_next + r' = S_6 - 3 a_before + r,   0 <= r' < 3,   S_6 = a_E + a_W + a_N + a_S + a_U + a_D

with the verbs named on the picture as its sources name them: S_6 the
group-ring addition (G) over the six Ports, the division by 3 with the
remainder kept the verb (D), the accumulator carrying r the translation
(T) (ALGEBRA_MASSIVE_RECORD.md 0.1); MASSIVE_RECORD.md section 1 on the
branch names the six-neighbour term one entry of verb (B)'s declared
matrix and the pair form beside it:

    3 den a_next + r' = num S_6 - 3 den a_before + r,   0 <= r' < 3 den

with [num, den] = [1, 1] the light rule bit for bit and den > num a
massive record kind (Layer 2, section 3.3, shows the pair on a block).

The integers on the picture are one worked example, declared here and
carried by the tool as constants (COMPUTATION; not from a run; the finding
of section 0): the neighbours (a_E, a_W, a_N, a_S, a_U, a_D) = (7, 5, 4,
2, 3, 1), so S_6 = 22; a_before = 4; r = 1; then 3 a_next + r' = 22 - 12
+ 1 = 11, so a_next = 3 and r' = 2. The same neighbours under the pair
[2, 3]: 9 a_next + r' = 44 - 36 + 1 = 9, so a_next = 1 and r' = 0. The
tool's test checks these eight integers against the two lines before
anything is drawn (section 9); the page prints them with the label "a
worked example, COMPUTATION; the rule of docs/designs/detector_law on
`detector-law-design`, not in the engine on main; no run records a_now".
When a run does, the panel reads the record's row at a Node and at its six
neighbours at two consecutive intervals and the constants go.

---

## 3. Layer 2: how it produces the physics

The same verbs over many Nodes and many intervals. Here the family names
appear, as the world files declare them (DECLARATION), and every number
is one of the runs'.

### 3.1 A record propagating, read where it is read: at the faces (run 1)

Run 1 is one birth of one record of 290 rows on the fan of every
primitive direction with Manhattan length at most 6, at the centre
(32, 32, 32) of an open cube of 65 per axis, at tick 1; every row leaves
through a face, and an open face is a detector, so the run's record is
290 face `click` lines (the register's Q: 290 of 290 at the derived tick,
Node and face). The runner writes the snapshot once, at the end, so the
board's interior per interval is not recorded and the page does not draw
it as if it were; the record is seen where it is read. The picture: the
six faces unfolded as the net of the cube, every click a mark at its
`node` on its `detector` face, its `tick` the mark's shade; a slider by
tick fills the faces in the order the clicks came, so the eye sees the
front reach the axes' faces first, the face diagonals next and the body
diagonals last (the classes' ticks are on the click lines; the register's
`classes.*.ages` 56, 79 and 97 are printed beside as PIN). Beside the net,
the straight line from the birth Node to each click's Node drawn faint
and labelled as the reader's inference after the click (Highlights 5.4,
the line of record 1336: the line from the emitter to the detector is the
reader's inference), not a recorded path. Kind: DETECTOR for every click
(its tick, its Node, its face, its `momentum` the label of its direction,
its `phase`, its `exact` and `remainder`); the lines CONVERSION.

### 3.2 The pace c from the three inputs

The text, first: c is not declared but forced, and the page states the
three inputs in one sentence each, quoted from their sources: (1) locality
with the 48, the six neighbours entering with one weight (MASSIVE_RECORD.md
1.1 on the branch, "derived, not declared"; ALGEBRA.md 4.2, the flight
operator's norm 1 / sqrt 3 from locality and straightness); (2) the zero
mode, a uniform record a solution; (3) the absent self term, which picks
the pace 1 / sqrt 3 in that family; and beside them the negative result
of ALGEBRA.md 4.14 (the constancy of c is the declared postulate P9 on the
engine as built, not a theorem of the six verbs). Then the run: for every
click of run 1, the Euclidean distance from the birth Node to the click's
Node plus the face's unit step, against the tick difference, drawn as
points on two axes (Links against intervals), so the pace is the slope by
eye, the axes' clicks, the face diagonals' and the body diagonals' told
apart by marker; the ratio per click and per class printed as an exact
fraction of two recorded integers (CONVERSION), the register's `pace` and
`asymptotic_pace` per class printed beside as PIN, and c = 1 / sqrt 3 as
the line the algebra names, COMPUTATION. No verdict is printed.

### 3.3 A foreign object as a declared block with its own pair

Not built and not on `main` (MASSIVE_RECORD.md on `detector-law-design`,
sections 0 to 5, the vocabulary only). The picture: a medium of pair
[num, den] drawn as a field of Nodes each carrying the pair; a block R of
side s (a cube; on a one-layer world a square) whose cells carry the
lowered pair [num', den'] with num' / den' > num / den, a well of the pair;
the object's record the bound mode in the well, its clock the mode (a
character at k = 0), its extent the mode's and not a declaration; its
momentum **P** one integer per axis for the whole block with its
remainder; its click the evaluation (E) across R. The integers on the
picture are DECLARATION only, taken from that file's own tables (its
section 2's rows, [num, den] = [2, 3] with the rest period 7.5 intervals,
and [128, 129] with 50.4), labelled with the branch and the SHA; no run,
no number of a run, no pin. Beside it, the rule of section 2.5 with the
pair on the six-neighbour term, so the eye sees that the block differs
from the light rule by the pair alone.

### 3.4 A detector-emitter as a declared object (run 2)

Run 2's world file declares, on a plane of 60 x 121 Nodes: one lamp of
`light` at (2, 60, 0) (an emitter: its `birth` lines, one record per
self-creation, the wheel `u`), a wall of bodies of `wall` at x = 8 with
two openings that `rerelease` on the fan of 90 directions (the `split`
lines), and a screen at x = 52 of 121 one-Node detector sets `screen_0` ..
`screen_120` reading `sum` (the `record` and `gather` lines). The picture:
the plane as the world declares it, each object at its Nodes, labelled by
its declared role (DECLARATION), and beside each object what it wrote to
the record in this run: the lamp its 64 births, the openings their splits,
the screen its gathers (counts of lines, DETECTOR). One sentence from
Highlights 5.4 under the picture: every external entity is one generic
detector-emitter, a receiver-inserter declared Outside (record 1327); a
detector's clock is its own count (record 709).

### 3.5 The GameBoard view, labelled a diagnostic (run 2)

Two pictures, both GAMEBOARD and titled so: (a) the store at the last
interval, `state.json`'s `nodes`: every Node that still holds rows, with
the rows' amounts, on the plane; (b) the books, `run.json`'s `audit` at
the last completed tick: per family the released, in transit, absorbed
and escaped amounts and contents and `balanced` (ALGEBRA.md 4.3, the
books as an identity of the ledger). Nothing here is compared with
anything; the panel's caption says what the owner's rule says: a reading
of the board itself is a diagnostic (record 281).

---

## 4. Layer 3: the clicks

Two columns side by side, the same record on both: on the left how the
click is born on the board, on the right how it looks in our world.

### 4.1 Left: how a click is born on the board (run 2, one record)

One record of run 2 followed from its `birth` line to its `gather` line,
chosen as the first record whose gather is at a screen set (the page
names its identity and its `u`; E15 of EXPERIMENTS.md followed the record
born at tick 43 with u = 41 through an in-process replay; this page
follows one from the record alone, no replay). The slider steps through
the record's lines in tick order:

1. the `birth` line: the tick, the lamp's Node, `u`, `labels`, `units`,
   `multiplicity`;
2. its `split` lines at the openings: the rows out with their weights;
3. its `record` lines at the sets it reached: per set the offer's
   `pointer` and `record` (the square) and `multiplicity`, drawn as a
   growing list of arrows on the phase plane per set (the detector's own
   record filling, verbs (G) and (E));
4. its `gather` line: the completion, `tick`, `arrived`, `chosen` (the
   set and the cell), `node`, `u`, `cells` (the rungs), `weight` and
   `total`: the evaluation (E) of the detector's own record and the
   comparison (D) that chose the cell, in the detector's own clock (the
   owner's word of record 1139: the click is an action; the record ends
   at the detector, its content enters the detector's own record);
5. the deletion: the count of the record's offers before the gather and
   after it (no `record` line of that identity follows the gather; the
   rows of the record are gone from the store: the one deletion, ALGEBRA.md
   4.7, Theorem 3);
6. the stamp with the detector's own count: run 2 does not declare
   `clock_stamp`, so no line of it carries `clock`; the page prints the
   chosen set's body from `state.json` (`age`, `owed`, `waited`) and says
   that in this run, with `owed` 0, the body's own count advanced at every
   interval, so its count at the click is the tick (the tick GAMEBOARD, the
   body's `age` and `owed` the store's view, GAMEBOARD); the DETECTOR stamp
   proper is the `clock` field a world under `clock_stamp` writes, which
   the third run of section 5 carries.

### 4.2 Right: how it looks in our world (run 2, all records)

1. **The pattern on the screen as the experimenter sees it.** One bar per
   pixel `screen_0` .. `screen_120`, the count of `gather` lines whose
   `chosen` set is that pixel, over the 64 births; the wall's and the
   faces' gathers as two bars beside (the register's L2 reading, 34 / 15 /
   15 over 64 births, printed beside as PIN, no verdict). DETECTOR.
2. **The detector's counts against its own clock.** For the screen as one
   detector and for one pixel chosen by the reader (a selector over the
   121), the gathers in the order of their ticks: the count of clicks
   against the tick on the horizontal axis, a staircase; the axis labelled
   "the tick (GAMEBOARD); equal to the pixel's own count in this run, its
   `owed` 0 (state.json)". Under `clock_stamp` the same panel reads
   `clock` and the axis is DETECTOR (the third run).
3. **The interval between clicks.** The differences of consecutive
   gather ticks at the screen, as a histogram of exact integers, and the
   list of the first differences; the `u` of every gather printed in the
   list, so the eye sees the wheel turn once per birth (every u once, the
   register's replication line).
4. **One line under the column**: only a detector's reading is a
   measurement; a click, a count between clicks on the detector's own
   record and a ratio of such counts are what is compared with nature; a
   reading of the board itself is a diagnostic (ALGEBRA.md 3.2, the
   reading rule); this page compares nothing.

---

## 5. The two runs the page renders first

| | Run 1, a light world | Run 2, a world with a detector and clicks |
| --- | --- | --- |
| world file | `examples/events/c_measured/c_measured.json` (series Q, c measured behind a detector) | `examples/events/amplitude/slits_low.json` (series L2, the two slits at a low rate) |
| model identity | `beam-c-measured-v1` | `beam-amplitude-slits_low-v1` |
| the world file's sha256 (the run's `initialization_sha256`) | `a3baa930a92e93f879670952b52dd38bb034539e38ec16a4c8ce408d5fc920fe` | `5df876c6ceb80675ebfb26c92e5a1185c5b7f67949c0949fd112fe76bd7b4bc6` |
| the registered run | 2026-09-21, the source fingerprint `acf789fe0811`, 0.39 s, completed and conserved (EXPERIMENTS.md, Q) | 2026-09-20, the fingerprint `ff5c382d672f`, 230 intervals, 2.4 s; replicated 2026-09-21 at `5fbd0c7`, 4.34 s wall, bit-exact (REPLICATIONS.md, `two_slits`, L2) |
| re-run since | the visual check of 2026-09-22 at `20d3a45a`, fingerprint `d537d4435b92` | the same, 230 intervals in 4.0 s (HOST) |
| the GameBoard and the length | 65^3 open, 100 intervals | 60 x 121 x 1, z periodic, 230 intervals |
| what the record holds | 1 `birth` line (290 rows on the fan at tick 1), 290 face `click` lines with `exact` and `remainder`, the lamp's body in `state.json`, the books | 64 `birth` lines, the `split` lines at the openings, the `record` lines of the 121 screen sets under `sum`, the `gather` lines (the register's 34 wall, 15 screen on 14 pixels, 15 faces over 64 births), the store's rows and the screen's 121 bodies in `state.json`, the books |
| what it is for on the page | Layer 1's (T) and (D) instances; Layer 2's propagation at the faces and the pace c | Layer 1's (B), (G), (P), (E) instances; Layer 2's declared objects and the GameBoard view; the whole of Layer 3 |

The runs are made by the register's own runner, outside the tree
(CONTRIBUTING.md: generated outputs are never committed), through
`tools/run_series.py` into one runs directory, each world in its folder
`<name>/run` (or the runner directly, `python -m event_universe --init
<world> --output <folder>`); the page names the folder it read and the
fingerprint `source_sha256` of `run.json`, so a page made at another
commit says so on its head. The page is made at the head the Boss names
for step 2, and its SHA is written on the page and in the log's record of
the run.

**A third run, later, on the Boss's word and not in step 2's first
page**: `examples/events/moving_detector/cart_k5.json`
(`beam-moving-detector-cart-k5-v1`, the world file's sha256
`ce6f113c785af44e34fc05d8b3ec788419cc7235e12319b0afcb2143cffcc3b9`, 600
intervals; the capability run of its sibling `capability_k5` at the source
`9a189f6b8f53`), the one registered world family whose every line carries
`clock`, the detector's own count, under `clock_stamp`: Layer 3's panels
2 and 3 then read the count and not the tick, DETECTOR proper, and the
cart's `step` lines give Layer 1's (T) on a body's drive (`drive` the
accumulator per axis, the wall the declared Q S M + abs(p_a)). It is
named here so that the panels are designed to take it without change.

---

## 6. What each panel reads, and from which file

| Panel | File | Lines or fields | Kind on the page |
| --- | --- | --- | --- |
| head: the runs | `run.json` | `model_id`, `source_sha256`, `initialization_sha256`, `ticks`, `completed`, `omit_row_clicks` | HOST (the fingerprints), DECLARATION |
| 2.1 the torus | `run.json` | `shape`, `boundary` | DECLARATION |
| 2.2 the Node and its Ports | none (text) | the Port order of TERMINOLOGY.md | none |
| 2.3 the state vector | `state.json` | one entry of `nodes` (a row), one of `measured` (a body) | GAMEBOARD |
| 2.4 (T) | run 1 `events.jsonl` | one `birth` line and one face `click` line of the same row (`tick`, `node`, `detector`, `phase`, `momentum`, `exact`, `remainder`) | DETECTOR; the differences CONVERSION |
| 2.4 (B), (G), (E) | run 2 `events.jsonl` | the `record` lines of one identity (`of`, `arm`, `label`, `pointer`, `record`, `multiplicity`) and its `gather` line (`u`, `cells`, `chosen`, `weight`, `total`, `T`) | DETECTOR |
| 2.4 (P) | run 2 `events.jsonl` | one `split` line | DETECTOR |
| 2.4 (D) | run 1 and run 2 `events.jsonl` | a face click's `exact` and `remainder`; a gather's `cells` against `u` | DETECTOR |
| 2.5 the light rule | the tool's constants (section 2.5) | the worked example | COMPUTATION, "not from a run" |
| 3.1 the fan at the faces | run 1 `events.jsonl`, `run.json` | every face `click` line; the lamp's `birth` line; `shape` | DETECTOR; the inferred lines CONVERSION |
| 3.2 the pace | run 1 `events.jsonl`; `examples/events/c_measured/expectations.json` | the clicks' `tick` and `node` against the birth's; the register's `classes`, `pace`, `asymptotic_pace`, `c` | DETECTOR; the ratios CONVERSION; the register PIN; c COMPUTATION |
| 3.3 the block | the tool's constants, from MASSIVE_RECORD.md's tables on `detector-law-design` at `b6131c64` | [num, den] and the rest periods of its section 2 | DECLARATION, "not built" |
| 3.4 the declared objects | `slits_low.json` (the world file beside the run's `initialization.json`); run 2 `events.jsonl` | `measured` (the lamp, the wall), `detectors` (the screen), the openings' `rerelease`; the counts of `birth`, `split` and `gather` lines | DECLARATION; the counts DETECTOR |
| 3.5 the GameBoard view | run 2 `state.json`, `run.json` | `nodes` (the rows left), `audit` (the books) | GAMEBOARD |
| 4.1 one record's life | run 2 `events.jsonl`, `state.json` | the `birth`, `split`, `record` and `gather` lines of one identity; the chosen set's body (`age`, `owed`, `waited`) | DETECTOR; the body's counts GAMEBOARD |
| 4.2 the screen, the counts, the intervals | run 2 `events.jsonl`; `examples/events/amplitude/expectations.json` | every `gather` line (`tick`, `chosen`, `u`); the register's `two_slits` block | DETECTOR; the register PIN |

No panel reads a per-row `click` line of a measured event, so the runs
are made under the runner's default (`omit_row_clicks` true) and the page
says so on its head; the page refuses nothing on that account.

---

## 7. The technology

### 7.1 What exists, and what is reused

- `docs/designs/visual_check/` (the Visual Checker, 2026-09-22): eleven
  figures from re-runs of registered worlds, read from `run.json` and
  `events.jsonl` alone, drawn with matplotlib, published as one private
  Artifact page. Its rule ("a click is counted, a tick is read, a Node is
  placed"; exact arithmetic only on a physical number; every figure names
  its kind) is this design's rule and is followed, not restated. Its
  `common.py` readers are bound to matplotlib at import and are not
  imported here (section 7.3); its reading of what a picture may be is.
- `examples/events/amplitude/pages/build_pages.py` (2026-09-21, E15 and
  E16): `click.html` and `bell.html`, a frame player and a GIF inside one
  HTML file, made by stepping the engine again in-process for the frames
  (numpy and Pillow). It is the record of what a moving picture of one
  record looked like; this page does not step the engine and does not
  import it, so nothing of it is reused but its one-file form (everything
  inline) and its rule that every number on the page names its source.
- `tools/click_readings/` (2026-09-22, the readings of every series): each
  module reads a run's record and prints the readings by kind; the
  certificate table of its README names what every tool reads and what it
  derives. This page's readers follow the same boundary (read and print;
  write nothing back; no rule of the law); the pace panel of 3.2 prints
  the register's numbers, it does not re-derive `c_measured.py`'s verdict.
- `pytest --visualize-runs` (tests/conftest.py): presentation tests are
  marked `visualization` and skipped without the flag; this design's
  page-writing test is marked so (section 9).

### 7.2 The tool

A folder `tools/algebra_visualizer/` with a README and four modules,
following `tools/click_readings/`'s form (a script with its usage line in
its docstring, loaded by its path in its test):

- `record.py`: the readers, standard library only: `run.json`
  (`json.load`), `events.jsonl` line by line filtered by `event`,
  `state.json`, the world file beside `initialization.json`, a series'
  `expectations.json`; every value returned as the record's integer or
  `fractions.Fraction`.
- `panels.py`: the panel models: one small dataclass per panel (its title,
  its algebra line with its ALGEBRA.md section, its numbers each as a
  `(value, kind, source line)` triple, its picture's data); the constants
  of 2.5 and 3.3 live here, labelled.
- `svg.py`: the pictures as inline SVG strings (the net of the cube, the
  Node with its Ports, the phase plane with pointer arrows, the bars, the
  staircase, the histogram, the light rule's seven Nodes); floats in
  coordinates only.
- `render.py`: the entry point. `PYTHONPATH=src python
  tools/algebra_visualizer/render.py RUNS_DIR [--render OUT.html]`:
  without `--render` it is headless, reads the two runs, builds the
  panels and prints every panel's numbers with their kinds and sources as
  text (the same table the test checks) and writes no file; with
  `--render` it writes the one HTML file and nothing else (the page is
  never written by a test or a check without the flag). A missing run
  folder is refused plainly with the `tools/run_series.py` line that makes
  it; the tool never runs the engine.

Dependencies: the standard library alone (`json`, `fractions`, `html`,
`pathlib`, `argparse`, `dataclasses`, `collections`); no numpy, no
matplotlib, no Pillow, no playwright, no library from a network; nothing
is added to `pyproject.toml`'s `render` extra or to the runner path. The
inline script on the page is a few lines of plain JavaScript for the two
sliders and the pixel selector, and the page reads without it (every
frame's data is in the page as text; the script only shows and hides).

### 7.3 No engine import beyond the readers

`record.py` imports nothing of `event_universe`; the tool reads the
record's fields as ENGINE.md names them. The two constants the tool needs
of the engine are read from the record, not imported: the Port order is
text of TERMINOLOGY.md; a click's direction is its recorded `momentum`
(the label, the unit vector of the direction at the scale Q), so the
flight and label tables (`nature_beam_tables`) are not loaded, unlike
`c_measured.py`, which needs them for its verdict. The test of section 9
asserts this with the module's import list. The engine's own reader of
the trimmed record (`event_universe.trimmed_record`, standard library) is
not needed either, since no panel reads a per-row click line; `run.json`'s
`omit_row_clicks` is printed on the head as the record says it.

---

## 8. How the page labels every number

Every number on the page sits in one HTML element carrying a `data-kind`
attribute with one of the seven kinds (DETECTOR, GAMEBOARD, COMPUTATION,
HOST, CONVERSION, DECLARATION, PIN) and a `data-source` attribute naming
the file and the line kind or field it was read from (`events.jsonl:
gather.chosen`, `run.json: audit`, `expectations.json: classes.axes.ages`,
`constant: section 2.5`). The kind is shown beside the number as a short
badge, one colour per kind, DETECTOR the darkest, GAMEBOARD a plain grey
box titled "a diagnostic", PIN in a dashed box titled "the register's
pin, written before the run", COMPUTATION and DECLARATION in outline. The
legend of the seven kinds is on the head of the page and repeats at the
head of every layer. A number with no `data-kind` is a defect the test
catches (section 9): the test parses the page and finds every run of
digits in text; each must be inside an element with `data-kind` or inside
a `data-source` or a section number. A picture's caption names its kind
in words as well, as the visual check's captions do, so a reader who
prints the page in black and white still reads the kind.

---

## 9. The tests

`tests/test_algebra_visualizer.py`, loading `render.py` by its path as the
click readings' tests do. A fixture run is made once per session by the
runner's API (`event_universe.runner.run_initialization`) into a temporary
directory from two registered worlds cheap enough for a test: run 1's own
world (`c_measured.json`, 100 intervals, 0.39 s registered) and
`examples/events/amplitude/mz_equal.json` (80 intervals, 0.3 s: births,
splits, records, gathers at two one-Node sets), the second standing in for
run 2 so that the suite never runs the 4 s world; the page for the owner
is made from run 2 itself. No test pins a number of a world (CONTRIBUTING,
the owner's rule of 2026-09-17): every assertion is the tool's contract
against the record it read.

1. **The headless run writes nothing.** `render.py RUNS_DIR` without
   `--render` prints the panel table and leaves the temporary directory
   without a new file.
2. **Every panel is present and every number is labelled.** The panel
   models of both fixture runs: the fourteen panels of sections 2 to 4
   exist; every `(value, kind, source)` triple has a kind among the seven
   and a non-empty source; the panels that a run cannot fill say "not
   recorded by these two runs" and carry no number.
3. **The readings equal the record's own totals.** The count of gather
   lines the screen panel shows equals the number of `gather` lines in
   the fixture's `events.jsonl` whose `chosen` is a set of the world; the
   count of face clicks on the net equals the number of face `click`
   lines; the books panel's numbers equal `run.json`'s `audit` values as
   read. Each is the tool against the file it read, never a pin.
4. **The light rule's worked example.** The eight integers of section 2.5
   satisfy `3 a_next + r' = S_6 - 3 a_before + r` with `0 <= r' < 3` and the
   pair form at [2, 3] with `0 <= r' < 9`, the integers written here
   before the tool exists; the check is the test's arithmetic, not the
   tool's.
5. **No engine import beyond the readers.** The four modules' import
   lists (by `ast`) contain no `event_universe` name and no `numpy`,
   `matplotlib`, `PIL` or `playwright`; the test also asserts that
   importing `render.py` imports none of them (`sys.modules`).
6. **The page (under `--visualize-runs` only, marked `visualization`).**
   `render.py RUNS_DIR --render OUT.html` writes one file; the file parses
   (`html.parser`); it contains the three layers' titles, the legend, both
   runs' `source_sha256` and `initialization_sha256`, the light rule's
   line and its "not from a run" label, the GAMEBOARD panels' "a
   diagnostic" title, and no run of digits outside a `data-kind` element
   (section 8); the file's size is below 4 MB.
7. **The refusals.** A runs directory without one of the two folders is
   refused with the `tools/run_series.py` line in the message; a record
   without `gather` lines fills Layer 3 with "not recorded" and does not
   fail.

`python tools/check.py` selects the test through the tool's path and the
documentation gates for this file and the index row; ruff formats and
checks the four modules; mypy covers `src/` alone and is not extended.

---

## 10. What the page will NOT do

- No physics computed: no rule of the law evaluated, no accumulator
  stepped, no pointer summed, no table of the engine loaded, no replay of
  a record for frames (the E15 page's way), no fit; the only arithmetic is
  an exact difference or ratio of two recorded integers, labelled
  CONVERSION.
- No pin moved and no verdict: a register's number is printed beside the
  run's as PIN and nothing is called PASS, FAIL, SEEN or matched; nothing
  is compared with nature.
- No live run: the tool never starts the engine; the page renders a runs
  directory made beforehand by the register's runner, and a missing run is
  a plain refusal.
- No render dependency in the runner path and none new anywhere: standard
  library only; no frame capture, no GIF, no image file.
- No new world and no new key: the two runs are registered worlds as they
  stand; the third is named, not run.
- No wording of its own on the physics: every sentence of the algebra on
  the page is quoted from ALGEBRA.md, Highlights 5.4, ENGINE.md,
  TERMINOLOGY.md or, for the block, MASSIVE_RECORD.md on its branch, with
  its section; the page is a reader of the tree, not a second statement.
- No light rule from a run on `main` until the rule is on `main` (section
  0); the worked example is labelled as such and goes on that day.

---

## 11. The cost

| Item | Host time | Kind |
| --- | --- | --- |
| the two runs, once, through `tools/run_series.py` at the head named for step 2 | run 1 about 0.4 s; run 2 about 4 s (the registered and re-run timings above) | HOST |
| the render, one pass over each `events.jsonl` and `state.json` (run 2's snapshot is the larger, the plane's rows) | under 2 s | HOST |
| the page's size | a few hundred kilobytes (290 marks, 121 bars, one record's offers as text, the SVGs), well under the Artifact's 16 MB | HOST |
| the test's fixture runs in the suite | about 1 s in all, once per session | HOST |
| the third run, later | `cart_k5`, 600 intervals on a bar of 240 x 3 x 3, a few seconds | HOST |

---

## 12. The build's steps for step 2, in order, with their sizes

Only on the Boss's word after his read of this file. Sizes are host
estimates of one agent's time and of lines of Python.

1. **The readers** (`record.py`, about 120 lines, 30 minutes): the five
   files, the filters by `event` and by identity, every value an integer
   or a Fraction; test 5's import gate written first.
2. **Layer 1's models** (`panels.py`, about 250 lines, 60 minutes): the
   torus, the Node, the state vector from one row and one body, the six
   verbs' instances by the table of 2.4 with their "not recorded" fallbacks,
   the light rule's example with test 4 written before it.
3. **Layer 2's models** (about 150 lines, 45 minutes): the faces' net by
   tick, the pace points and the exact ratios per class with the
   register's pins beside, the block's declared table, the declared
   objects of run 2 with their line counts, the store and the books.
4. **Layer 3's models** (about 150 lines, 45 minutes): one record's life
   from its lines, the deletion's before-and-after count, the screen's
   bars, the staircase, the intervals; the `clock` branch for the third
   run left in place and exercised by a test on a `clock_stamp` line built
   by hand.
5. **The pictures and the page** (`svg.py` and `render.py`, about 400
   lines, 90 minutes): the seven SVGs, the kind badges, the legend, the
   head, the two sliders' script, the headless printout; tests 1, 2, 3, 6
   and 7.
6. **The checks** (30 minutes): `ruff format`, `ruff check`, `python
   tools/check.py`, then `pytest tests/test_algebra_visualizer.py
   --visualize-runs` once for the page test, headless otherwise.
7. **The runs, the page and the record** (45 minutes): the two runs
   through `tools/run_series.py` at the head, the render, the page read by
   eye against sections 2 to 4, the private Artifact page published for
   the owner (the Boss's word names who shares it), the tool's README
   row in `tools/click_readings/README.md`'s style, the row of docs/README.md
   updated with the page's link, one record in the day's log with the
   head's SHA and the two runs' fingerprints; open no PR, report to the
   Boss.

About six hours end to end; nothing of it touches the engine, a world, a
pin or a key, so nothing of it is dangerous; the one thing it can break is
the documentation index gate, which check.py runs.

---

## 13. The one question to the Boss

The light rule `3 a_next + r' = S_6 - 3 a_before + r` is not in the engine
on `main` and no run on `main` records a_now, a_before or r (section 0).
Does the Boss want Layer 1's light-rule panel drawn from the worked example
of section 2.5, labelled COMPUTATION and "not from a run", for the first
page, with the panel reading a run the day the rule is on `main`; or does
he want the first page to wait for that day? The design carries the first;
nothing else in it depends on the answer.
