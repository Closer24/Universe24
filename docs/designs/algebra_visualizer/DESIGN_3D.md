# The algebra visualizer in 3-D: any registered run folder as one page in three layers, the algebra, the GameBoard as the Inside in 3-D, and the clicks as the Outside (the design before the build; the Algebra Visualizer 2, 2026-09-23)

The model owner's word of 2026-09-23, 17:02Z, as the Boss gave it (Hebrew,
in substance): "The visualizer is, when we make experiments, it can give
the experiment in 3-D: show our three layers, the algebra layer, the
GameBoard layer which is the Inside, and the layer we see outside, which
is the clicks." Visualization is requested by the owner for this task, so
a page is in scope (the display contract of
[SIMULATOR_DEFINITIONS.md](../../../SIMULATOR_DEFINITIONS.md), "Default run
display": runs are headless unless visualization is explicitly requested).

This file is STEP 1, docs only: no tool line, no engine line, no run.
STEP 2, the build in `tools/algebra_visualizer/` (extended, not forked),
its tests, the README and one page from an existing registered run
published for the owner as a private Artifact page, starts only on the
Boss's GO after his read of this file.

**What this design extends.** The first visualizer
([DESIGN.md](DESIGN.md), merged with PR #1051): a standard-library tool,
headless by default, one static page in three layers from two registered
runs, every number with its kind and its source, no physics computed. Its
rules, its readers (`record.py`), its panel model (`panels.py`: a
`Number` is a value, a kind and a source; a `Panel` is a title, its
algebra lines, its numbers, its picture's data and, where a run cannot
fill it, its `missing` sentence), its pictures (`svg.py`) and its entry
(`render.py`) stay and are extended. What is new: (1) the tool takes ANY
registered run folder, of the engine on `main` (the Beam Law, `beam-v1`
with `amplitude-v1`, "the old engine" below) or of the detector-law
engine on the branch `detector-law-build` (`detector-law-v1`, with
`massive-record-v1` under its key, "the new engine" below), told apart
from `run.json` alone; (2) the GameBoard layer is a 3-D view of the board
with a step control over the intervals; (3) the three layers are the
owner's three: the algebra, the Inside, the Outside.

**The rules the page obeys** are the first design's, unchanged ("The rules
the page obeys" of [DESIGN.md](DESIGN.md)): (1) it reads recorded state
alone and never runs or changes a run; (2) it computes no physics, the
only arithmetic a sum, a difference or a ratio of recorded integers,
exact (`fractions.Fraction`), floats in drawing coordinates alone; (3)
every number carries one of the seven kinds (DETECTOR, GAMEBOARD,
COMPUTATION, HOST, CONVERSION, DECLARATION, PIN) and its source file and
key; a number whose kind is not named is not a result (the model owner,
2026-09-21, record 281); (4) a click is a DETECTOR reading, a board view
is a GAMEBOARD diagnostic and is titled so, never pinned; (5) nothing is
pinned, compared with nature or given a verdict; (6) the names are
[TERMINOLOGY.md](../../TERMINOLOGY.md)'s. Two rules of this task are
added: (7) the tool computes nothing beyond sums and labels; (8) the page
opens a run folder of the new engine's first worlds (the massive record
kind, the layer worlds) without a code change beyond what `run.json`
declares: every key is read by name and an absent key is "not recorded",
never a crash.

**The symbols, named once.** N the phase circle's grain; Z_N the integers
modulo N; f a record's rows at a Node as one element of the group ring
Z[Z_N]; (X, Y) a click's pointer, the evaluation of f on the tables at the
scale 256; u the birth wheel's value on a record; n_D a detector's own
count (ALGEBRA.md 3.1); t the interval's count, the tick, GAMEBOARD and
never read by a detector; **D** a direction as a primitive integer
vector; **p** a body's momentum, **P** a block's momentum, one integer
per axis; M a body's content; s a block's side in Nodes; S_6 the sum of
a record's amplitude at the six neighbours of a Node; a_before, a_now,
a_next a record's amplitude at a Node at the interval before, the
present one and the one to come; r and r' the row's remainder before and
after the division; [num, den] a record kind's pair on the six-neighbour
term ([1, 1] for light; den > num a massive kind); [num', den'] a block's
own pair on its cells; I the conserved form of a massive record
(MASSIVE_RECORD.md section 3 on the branch, the key `form`); **F** the
interval's map on the state vector **s**; the six verbs (T) the
translation, (B) the bilinear form, (G) the group-ring addition, (P) the
permutation, (E) the evaluation, (D) the division with the remainder
kept and the comparison (ALGEBRA.md chapter 2).

---

## 0. What the design stands on, and the three findings

Read first, as the Boss ordered: AGENTS.md, skills/workflow.md,
TERMINOLOGY.md, ALGEBRA.md chapters 1 to 3 and 5, DESIGN.md and the tool
beside it, its README, ENGINE.md ("The detector's readings by type", the
record's files and every field by kind), and on the branch
`detector-law-build` at `2f44797c` (not on `main`; the files are named by
path and not linked, since the index gate follows links)
`docs/designs/detector_law/DESIGN.md`, `MASSIVE_RECORD.md` sections 1 to 3
and 11, `BUILD.md`, and the engine `src/event_universe/events/detector_law.py`
with `tests/test_detector_law.py` and `tests/test_massive_record.py`.
Beside the reading, five runs were made outside the tree to see what each
engine writes, and the tables of section 5 are read from those files and
not from the documents alone: on `main` at `52a5cd9e`, `c_measured`
(65^3 open, 100 intervals), `mz_equal` (5 x 5 x 1, 80 intervals) and
`cart_k5` (240 x 3 x 3 under `clock_stamp`, 600 intervals, the cart's
`step` lines); on the branch at `2f44797c`, the chain world of
`test_detector_law.py` (80 x 1 x 1, 200 intervals) and a block world of
`test_massive_record.py` (40 x 1 x 1, the kind [800, 809], one block of
side 3 with the well [800, 800] and **P** = (64, 0, 0), a lamp and a
screen, 60 intervals). HOST, all of it; no number of them is on this page
and none is pinned.

**Finding 1, which shapes the GameBoard layer.** Neither engine records
the board's state per Node per interval. The old engine writes the
store's Node view once, at the end (`state.json`, `nodes[].families[].rays[]`:
a row's direction, age, phase, amount, content, record), and per interval
only the events (`events.jsonl`: `birth`, `split`, `rerelease`, `cancel`,
`record`, `gather`, `click`, `step`, and the rest of ENGINE.md's list)
and the books' totals per family (`run.json`: `audit`, `measured_content`,
`transit_content`, `momentum`). The new engine writes no row at all per
interval: per interval it writes each block's line (`block`: its `corner`,
its `steps`, the `sum` of its own record over its cells, its `clock`),
each light probe's values where the world declares `probes` (`probe`:
`values`, light's summed amplitude at each probe Node), the births, the
blocks' self-clicks (`click`) and the records' clicks (`gather`); at the
end it writes each block's own record over the whole board (`state.json`
`blocks[].rows`, the one per-Node dump) and each live record's pointer per
cell (`records[].pointers`), never the light records' rows. So the 3-D
view shows the records' presence where the record shows it, at the Nodes
of the events at their intervals, the blocks where their lines put them,
the probes where they are declared, and the snapshot at the last
interval; it says on its face what the run keeps and does not draw a row
where none is recorded (section 3.2).

**Finding 2, which shapes the detection.** Both engines write `law:
"beam-v1"` in `run.json`. The new engine is told by its identity in
`hypotheses` (`"detector-law-v1"`; and `"massive-record-v1"` with the
top-level `massive_record: true` under the key); `state.json` of the new
engine writes `law: "detector-law-v1"` and its `layer` block in `run.json`
writes `law: "detector-law-v1"` on a recorded world. The tool reads
`hypotheses` and nothing else to choose its readers (section 5.1); it
never branches on a family name.

**Finding 3, which shapes the tests.** The new engine is not on `main`, so
the suite on `main` cannot make a run of it with the runner's API. Its
fixture is a record built by hand in the test, in a temporary directory,
from the keys of section 5.3 as the branch's engine writes them at
`2f44797c` (the way the first design exercised the `clock_stamp` branch
on a line built by hand, DESIGN.md section 12 item 4); the day the engine
is on `main` the fixture is made by the runner's API and the hand-built
record goes. The Boss's first real run folders (the massive record kind,
the layer worlds) are opened headless first; a key the engine renamed
since `2f44797c` shows as "not recorded" in the printout and is reported,
not patched around (section 7, test 7).

---

## 1. The page in one look

One static HTML file, one column, three layers top to bottom, each a band
with its title, its one-sentence claim from the algebra, its panels, and
under every panel the file and the key it was read from. The head names
the run folder it renders: the world file's sha256
(`initialization_sha256`), the model identity (`model`), the engine's
fingerprint (`source_sha256`), the engine the tool found (section 5.1),
the identities (`hypotheses`), the interval count (`completed_ticks` of
`requested_ticks`), `status` and `error`, `elapsed_seconds` (HOST), and
the legend of the seven kinds. One run per page; the first visualizer's
two-run page stays as it is (section 6.4).

| Layer | Its title on the page | What is seen by eye | Kind of every number |
| --- | --- | --- | --- |
| 1 | The algebra | the run's declared objects as objects of ALGEBRA.md: the families with their pairs, the blocks with their pairs and sides, the detectors and the emitters, the board's extents and faces, the verbs that act per interval, read from `run.json` and the world file beside it | DECLARATION (every integer); the fingerprints HOST |
| 2 | The GameBoard, the Inside (a diagnostic) | the board in 3-D: the Nodes' extents as a box, a layer or a chain; the records' presence over the intervals where the record shows it; the blocks as cubes at their positions moving by their recorded steps; the detectors as faces or cells; a step control over the intervals; the run's own statement of what it keeps per Node | GAMEBOARD, titled "GAMEBOARD, a diagnostic, never a measurement" |
| 3 | The Outside: the clicks | the clicks as the detectors' own records in their own counts: per detector its clicks, the count against the detector's own count where the run stamps it, the intervals between clicks, the pattern an experimenter sees | DETECTOR; the differences CONVERSION; a register's number PIN |

---

## 2. Layer 1: the algebra layer

Everything here is a declaration of the world, printed as the object of
ALGEBRA.md it is, with the section it comes from, and with the family
names as the world file gives them. Every integer is DECLARATION and
carries the file and the key it was read from. No number of the run's
result is on this layer.

### 2.1 The board: the translation group of the torus

The object: Z_X x Z_Y x Z_Z acting on the Nodes, each factor a circle (a
periodic axis) or a segment whose faces are the border, a click at the
face detector (ALGEBRA.md 1.6; TERMINOLOGY.md "GameBoard", "Face, face
detector"). The panel prints the three extents (`shape`) and the faces per
axis (`boundary`, "open" or per axis) and names the board's form in
words: a 3-D box when every extent exceeds 1, a layer when one extent is
1 (the layer worlds z = 1 of the new engine's schedule), a chain when two
are. On a massive world it prints beside light's faces each family's own
faces (`families[].faces`, periodic where absent, the kind's own border:
BUILD.md section 3 on the branch) so the eye sees that the light's faces
and a massive kind's faces are two declarations.

### 2.2 The families and their pairs

The object: a record kind's pair [num, den] on the six-neighbour term,
`3 den a_next + r' = num S_6 - 3 den a_before + r` with `0 <= r' < 3 den`,
[1, 1] the light rule bit for bit and den > num a massive kind whose gap
is cos omega_0 = num / den (MASSIVE_RECORD.md sections 1 and 2 on the
branch; the light rule as ALGEBRA_MASSIVE_RECORD.md section 0.1 writes it
in the verbs). One row per family of `run.json`'s `families`: its name,
its quantum h, its charge, its phase circle and its phase per Link (the
pair form `phase_per_link` [n, d], the family's clock: ALGEBRA.md 2.1),
its lifetime, and on the new engine under the key its `pair` and its
`faces`. On the old engine the row says "no pair declared: the engine on
`main` runs the Beam Law, whose record form is `amplitude-v1`; the
six-neighbour rule is not in it", and prints nothing invented. The
massive kind's row prints its pair and names it "a massive kind (den >
num), its clock its gap, no lamp" as BUILD.md's loader has it.

### 2.3 The blocks with their pairs and sides

The object: a foreign object as a declared cube of side s at a corner,
its cells carrying the lowered pair [num', den'] with num' / den' > num /
den, a well; its momentum **P** one integer per axis with the drive's
wall `3 Q S M` per axis; its click the evaluation (E) across its cells
(MASSIVE_RECORD.md sections 4 to 7 on the branch; BUILD.md section 3's
block keys). One card per block: on the new engine a measured event of
the world file that declares `side` (`initialization.json`, `measured[]`:
`position` the corner, `family`, `side`, `pair`, `amount` the content M,
`momentum`, and where declared `coupling` {G, g}, `wheel`, `seed`,
`absorbing`, `cavity`, `ramp`, `margin`, `emits`, `held`); `run.json`'s
`numbers` echoes its position and family and no block key, and the card
says so. On the old engine the card is the body's: `numbers[n]`'s
`position`, `family`, `span` (its extent, a box of Nodes centred on its
position), and from the world file `amount`, `momentum`, `fixed`, `held`,
its `table` (the rule per family: read, measure, rerelease, pass, become)
and its `lamp` where one is declared; the card names the body "a body of
the Beam Law, its extent `span`, not a cube of the massive kind" so the
two engines' objects are never confused. A run without blocks or bodies
says "none declared".

### 2.4 The detectors and the emitters

The object: a detector D at a Node with its own count n_D, which never
reads the tick (ALGEBRA.md 3.1; 5.6 (a)); a lamp a body's declared
source (TERMINOLOGY.md "Lamp"); both declarations of the world file, not
records that hop (ALGEBRA.md 3.4); every external entity one generic
detector-emitter, a receiver-inserter declared Outside (Highlights 5.4,
the line of record 1327, quoted as the first design quotes it). The
panel lists: every declared detector set (`initialization.json`
`detectors[]`: `name`, `positions`, `threshold`, `reading` where the old
engine declares it), the face detectors the board's open faces make
(named `face:+x` .. `face:-z` from `boundary`, no number), every emitter
(a measured event with `lamp`: its `rate`, its `wheel` [r, W], its
`directions`, and on the new engine its `train`; a block with `emits`
and its `held`), and on the old engine every measured event's rule table
as the receiver-inserter's declaration. On the new engine the panel adds
the sentence of the law: every declared set's Nodes and every measured
event's Nodes receive (BUILD.md section 3; `detector_law.py`'s cells).

### 2.5 The verbs that act per interval

The object: one interval of a record applies, in order, (T) on every
accumulator, (D) whose whole part is the event, (B) at the push and at
the click, (G) and (E) where rows are summed at one Node and where they
end, and (P) at a collision (ALGEBRA.md 2.11, quoted). The panel prints
the six verbs' names and lines (ALGEBRA.md 2.1 to 2.6) once, and beside
them per engine what the record shows acting, as text and not as a claim
of the tool: on the old engine the lines of 2.11 (the hop, the phase, the
push, the crowd, the split, the sum, the click and the age); on the new
engine the one line of the rule, (G) the sum over the six Ports, (D) the
division by `3 den` with the remainder kept, (T) the carry of r, the pair
one entry of (B)'s declared matrix, and (E) the click across the cells
(MASSIVE_RECORD.md section 1; ALGEBRA_MASSIVE_RECORD.md 0.1). The worked
example of the first design's section 2.5 is not repeated here: a run of
the new engine records no `a_now`, `a_before` or `r` either (Finding 1),
so the panel says "no run records the row's three integers; the rule's
instance is the first page's worked example, COMPUTATION" and links to it.

---

## 3. Layer 2: the GameBoard, the Inside, in 3-D

The band's title on the page: "GAMEBOARD, the Inside: a diagnostic,
never a measurement". Every number in the band is GAMEBOARD except a
declared extent or position (DECLARATION) and a click's mark, which is
drawn on the board at the detector's cell and keeps its DETECTOR badge.
The band's claim from the algebra, printed once: Inside is the GameBoard,
Nodes on the cubic lattice, integer rows on them, and the tick, which no
detector ever reads; a reading of the board itself is a diagnostic
(ALGEBRA.md 3.1 and 3.2; TERMINOLOGY.md "Inside and Outside", record 768).

### 3.1 The box, the layer, the chain

The picture: the GameBoard's extents as a wire box in an orthographic
projection, the three axes named, the origin Node (0, 0, 0) marked, a
periodic axis drawn with its two ends joined by a dashed return and an
open axis with its two faces drawn as translucent squares titled by
their face detector's name. A layer world (one extent 1) is drawn as one
plane inside a thin box, so that the eye sees the layer is the board and
not a slice of one; a chain as one line. The extents are DECLARATION
(`shape`); the faces DECLARATION (`boundary`; on a massive world each
family's `faces` drawn as a second, lighter set of faces with the
family's name).

### 3.2 The records' presence over the intervals, where the record shows it

The picture, over the box, at the interval t the step control selects:

- **The old engine.** Every event line of `events.jsonl` with a `node` and
  a `tick` is a mark on the board at its Node at its tick, one glyph per
  event kind (a `birth` at the lamp's Node; a `split` or a `rerelease` at
  an opening; a `record` at a detector's cell; a `gather` at its chosen
  set's Node; a face `click` on the face; a `step` from `node` to `to`;
  a `cancel` at its Node where one is written). At interval t the marks
  of ticks up to t are shown, the tick t's marks full and the earlier
  ones fading by age in a fixed number of shades (a drawing choice, no
  number), so the eye follows a record from its birth to its click
  across the events that are recorded of it. Under the board a strip
  prints the books at tick t from `run.json`'s `audit[t - 1]` (per family
  the released, in transit, absorbed, escaped, and `balanced`) and
  `transit_content[t - 1]` and `measured_content[t - 1]` per family, all
  GAMEBOARD, the books being the run's own per-interval totals and not a
  Node's state. At the last interval the snapshot's rows are drawn as
  well: every Node of `state.json`'s `nodes` with rows, a cell shaded by
  the sum of its rows' `amount` (a sum of recorded integers, allowed),
  the sum printed on hover and in the panel's table; and the bodies of
  `measured` at their `position`. The panel's caption states the finding:
  "this run keeps no per-Node state per interval; it keeps the events at
  their Nodes, the books per interval and the store's view at the last
  interval", with the counts of each (the number of event lines per kind
  from the reader's `counts`, GAMEBOARD).
- **The new engine.** The births at their Nodes at their ticks; each
  block's cube at its `corner` of its `block` line at tick t (section
  3.3); each `probe` line's `values` at tick t drawn as a shaded cell at
  each declared probe Node (`initialization.json` `probes`, DECLARATION;
  the value GAMEBOARD, the one per-interval per-Node reading of light the
  engine writes); each `gather`'s `node` at its `tick` as a click mark
  (DETECTOR) and each block's self-click (`click`) at its `node`; the
  books at tick t from `audit[t - 1]`, with the conserved form `form` per
  family under the key, printed as the GAMEBOARD diagnostic it is (BUILD.md
  section 3). At the last interval the snapshot: each block's own record
  over the board, `state.json` `blocks[].rows`, drawn as cells shaded by
  their integer (section 3.5 on the cap), and each live record's
  `pointers` per cell printed in the panel's table beside the cell's
  name. The caption states the finding for this engine: "this run keeps
  no row per Node per interval; it keeps the blocks' lines per interval,
  the probes where declared, the births and the clicks, and at the last
  interval each block's own record over the board and each live record's
  pointer per cell".

In both, a mark's tick is printed as "the tick t (GAMEBOARD, the record's
ordering, never read by a detector)" (ALGEBRA.md 3.3), and the click marks
keep their DETECTOR kind because they are the detector's clicks placed on
the board, not a reading of the board.

### 3.3 The blocks as cubes, moving by their recorded steps

The picture: each block a cube of side s (DECLARATION) at the corner its
line gives (GAMEBOARD): on the new engine the `block` line's `corner` at
tick t and its `steps` printed beside (the Links stepped so far), its
`sum` (its own record's total over its cells) and its `clock` (its count
as the host's copy on the line, GAMEBOARD; the count's DETECTOR reading is
the block's `click` line of the Outside layer); at the last interval
`state.json` `blocks[]`'s `corner`, `steps`, `drive` (the remainder per
axis), `momentum`, `responses` and `emitted`. On the old engine a body is
a box of `span` at its `position` and moves by its `step` lines: at tick
t the body stands at the `to` of its last `step` line with tick at most
t, else at its declared position; the line's `drive` (the accumulator per
axis) and `momentum` are printed beside as the store's view, and at the
last interval `state.json` `measured[]`'s `position`, `steps`,
`axis_steps`, `drive` and `momentum`. The cube's motion between two
lines is a jump of one Link at the line's tick, never interpolated: a
block is where its line puts it and nowhere between. The caption: "a
block's position is the host's view of the board, GAMEBOARD; only its
click is a measurement" (ALGEBRA.md 3.2: a body's own record enters no
comparison).

### 3.4 The detectors as faces or cells

The picture: each declared detector set's `positions` as cells on the
board (DECLARATION), named; each open face of the board as a translucent
face (its name from `boundary`); on the old engine every measured event
outside a set as a one-Node detector (TERMINOLOGY.md "Detector"); on the
new engine every measured event's Nodes as receiving cells (BUILD.md
section 3). Each cell prints, at interval t, the count of clicks it has
received up to t (the `gather` lines with that cell in `chosen` and tick
at most t on both engines; the face `click` lines per face on the old
engine), DETECTOR, so the eye sees the Outside layer's counts grow on
the Inside's cells as the slider moves.

### 3.5 The step control and the cap

One slider over the intervals 0 to `completed_ticks`, with a step of one
and buttons for one interval back and forward, and the interval's number
printed as "t = ... (GAMEBOARD)". The page's data is one JSON object in a
`<script type="application/json">` element written by the tool: the
extents, the faces, the cells, the blocks' lines by tick, the marks by
tick, the probe values by tick, the books by tick, the snapshot; every
integer in it is also printed once in the panel's table with its kind, so
that the test's rule (no digit outside a labelled element) holds for the
data as it holds for the text. The inline script (section 6.2) reads
that object, draws the board at t and rotates it; without the script the
page shows the tool's pre-rendered SVG of the board at the last interval
in the default view, with the same numbers in its table. The cap: the
tool writes at most 20,000 cells of a snapshot (`state.json` `nodes` on
the old engine, a block's `rows` on the new) into the page; a larger
snapshot is written as the sum per plane of the board's longest axis
(a sum of recorded integers), and the caption names the cap, the number
of cells the snapshot has and that the planes' sums stand in for them.

---

## 4. Layer 3: the Outside, the clicks

The band's claim, printed once: a click at a detector, a count between
clicks on the detector's own record, and a ratio of such counts are what
is compared with nature; nothing measured inside the board is compared
(ALGEBRA.md 3.2, the reading rule); a click is an action of the law, the
record ends at the detector and the detector's own count advances
(ALGEBRA.md 3.1; POSTULATES.md section 10, record 1139). Every number
DETECTOR; a difference of two clicks' counts CONVERSION; a register's
number PIN, printed beside and never as a verdict. The panels take the
detectors from the run's own tables, never from a family name.

### 4.1 The detectors' own records in their own counts

One card per detector: on the new engine `run.json` `detectors[]`'s
`name`, `positions` and `clicks` (the count of gathers whose chosen cell
is that set), and the face cells from the `gather` lines' `chosen`; on the
old engine `run.json` `detectors[]`'s `name`, `nodes`, `threshold`,
`reading` and per family `measured`, `clicks`, `record` (the detector's
own record: the square X^2 + Y^2 under `wave`, the count under `beam`,
the accumulated record under `sum`) and for a face its `content` and
`momentum`; beside the card the count of `gather` lines chosen at that
set, and on the old engine the count of face `click` lines on that face,
which the test holds equal to the record's own totals (section 7, test
3). The block's self-clicks on the new engine are a card too: its `click`
lines' `cycle` and `clock`, the count of the block's own cycles, the
click of a body (MASSIVE_RECORD.md section 1's table: "a measurement: a
click at a body").

### 4.2 The counts against the detector's own count

For one detector chosen by a selector over the run's sets (the screen's
sets as one detector where a run declares many, as the first design does
for `screen_0` .. `screen_120`): the clicks in order as a staircase, the
count on the vertical axis; the horizontal axis the detector's own count
where the run stamps it, the `clock` field of the `gather` line under
`clock_stamp` on either engine (on the new engine the block's count at
the first rung's crossing, else the rung's interval: `detector_law.py`'s
gather), labelled DETECTOR; where the run does not stamp it, the tick
(old engine) or the gather's `click` interval (new engine), labelled
"GAMEBOARD, the record's ordering; the detector's own count is not
stamped in this run" (the first design's rule of section 4.2 item 2,
kept). The block's own clock on the new engine is a second staircase, its
`click` lines' `cycle` against `clock`.

### 4.3 The intervals between clicks

The differences of consecutive clicks' counts at the chosen detector
(the `clock` where stamped, else the ordering of 4.2), as a histogram of
exact integers and as the list of the first differences with each
gather's `u` (so the eye sees the wheel turn), CONVERSION for the
differences, DETECTOR for the counts. On the new engine the `gather`
line's `birth` and `click` give a second list, the record's age at its
click in the record's ordering (CONVERSION of two GAMEBOARD integers,
labelled so).

### 4.4 The pattern an experimenter sees

One bar per detector set in the order of the world file, the count of
clicks (4.1), and beside the bars, where a register exists beside the
world (`expectations.json` by the run's name, as `render.py`'s `REGISTERS`
maps it today, extended by name and never by a family), the register's
numbers as PIN with no verdict. On a screen of many one-Node sets the bars
are the pattern; on a chain or a world of one detector the panel is one
bar and says so. Under the column the sentence of the first design's
section 4.2 item 4: this page compares nothing.

---

## 5. What is read from which file and key, per engine

### 5.1 The detection, from `run.json` alone

| Read | Key | Then |
| --- | --- | --- |
| the identities | `hypotheses` (a list) | `"detector-law-v1"` in it: the new engine's readers (5.3); else the old engine's (5.2) |
| the massive kind | `massive_record` (true under the key) and `"massive-record-v1"` in `hypotheses` | the family `pair` and `faces`, the block cards, the `form` in the books, `blocks` in the snapshot |
| the stamp | `clock_stamp` (true where declared) | the `clock` field is read on `birth`, `gather`, `rerelease` and, on the new engine, `block` and `click` lines |
| the record's trim | `omit_row_clicks` | printed on the head; no panel reads a per-row click of a measured event |
| the run's state | `status`, `error`, `completed_ticks`, `requested_ticks`, `tick`, `elapsed_seconds`, `conserved_at_every_completed_tick`, `package_version`, `source_sha256`, `initialization_sha256`, `model` | the head; HOST for the fingerprints and the time, DECLARATION for the model and the counts |

A folder without one of `run.json`, `events.jsonl`, `state.json`,
`initialization.json` is refused with the line that makes a run (the
runner, `python -m event_universe --init WORLD --output FOLDER`, and the
series' runner `tools/run_series.py`); a `run.json` without `hypotheses`
is refused naming the key; anything else absent is "not recorded" on its
panel.

### 5.2 The old engine (the Beam Law on `main`, `beam-v1` with `amplitude-v1`)

| Panel | File | Keys | Kind |
| --- | --- | --- | --- |
| 2.1 the board | `run.json` | `shape`, `boundary` | DECLARATION |
| 2.2 the families | `run.json` | `families[]`: `name`, `quantum`, `charge`, `columns`, `phase`, `phase_per_link`, `lifetime`, and `hand`, `massive`, `momentum_magnitude` where written | DECLARATION |
| 2.3 the bodies | `run.json`; `initialization.json` | `numbers[n]`: `position`, `family`, `span`, `become`; `measured[]`: `amount`, `momentum`, `fixed`, `held`, `table`, `lamp`, `directions` | DECLARATION |
| 2.4 the detectors and emitters | `initialization.json`; `run.json` | `detectors[]`: `name`, `positions`, `threshold`, `reading`; `boundary` for the faces; `measured[].lamp`: `rate`, `wheel`, `directions`; `measured[].table` | DECLARATION |
| 2.5 the verbs | none (text) | ALGEBRA.md 2.11 | none |
| 3.1 the box | `run.json` | `shape`, `boundary` | DECLARATION |
| 3.2 the marks by tick | `events.jsonl` | every line's `event`, `tick`, `node` (and `to` on a `step`, `detector` on a `click` or a `record`, `chosen` on a `gather`) | GAMEBOARD; a `gather` or face `click` mark DETECTOR |
| 3.2 the books by tick | `run.json` | `audit[t - 1]`: `families[name].measured.*`, `.transit.*`, `balanced`; `transit_content[t - 1]`, `measured_content[t - 1]` | GAMEBOARD |
| 3.2 the snapshot | `state.json` | `nodes[]`: `position`, `families[].rays[]`: `amount` (summed per Node), `direction`, `age`, `phase`, `content`, `record`; `measured[]`: `position` | GAMEBOARD |
| 3.3 the bodies moving | `events.jsonl`; `state.json` | `step` lines: `tick`, `number`, `node`, `to`, `momentum`, `drive`, `step_port`; `measured[]`: `position`, `steps`, `axis_steps`, `drive`, `momentum` | GAMEBOARD; `span` DECLARATION |
| 3.4 the detectors' cells | `initialization.json`; `events.jsonl` | `detectors[].positions`; the count of `gather` lines by `chosen` and of face `click` lines by `detector`, up to t | DECLARATION; the counts DETECTOR |
| 4.1 the detectors' records | `run.json`; `events.jsonl` | `detectors[]`: `name`, `nodes`, `threshold`, `reading`, `families[name]`: `measured`, `clicks`, `record`, `phase`, `content`, `momentum`; the counts of `gather` and face `click` lines | DETECTOR |
| 4.2 the staircase | `events.jsonl`; `run.json` | `gather` lines: `tick`, `chosen`, `clock` where `clock_stamp` | DETECTOR (`clock`); the tick GAMEBOARD |
| 4.3 the intervals | `events.jsonl` | consecutive `gather` lines' `clock` or `tick`, `u` | CONVERSION; DETECTOR |
| 4.4 the pattern | `events.jsonl`; `examples/events/<series>/expectations.json` | `gather` lines by `chosen`; the register's block by the run's name | DETECTOR; PIN |

### 5.3 The new engine (`detector-law-v1`, `massive-record-v1` under its key; the branch at `2f44797c`)

| Panel | File | Keys | Kind |
| --- | --- | --- | --- |
| 2.1 the board | `run.json` | `shape`, `boundary`; under the key `families[].faces` | DECLARATION |
| 2.2 the families | `run.json` | `families[]`: `name`, `quantum`, `charge`, `phase`, `phase_per_link` (the pair form), `lifetime`; under the key `pair`, `faces` | DECLARATION |
| 2.3 the blocks | `initialization.json`; `run.json` | `measured[]` with `side`: `position`, `family`, `side`, `pair`, `amount`, `momentum`, `held`, `coupling` {`G`, `g`}, `wheel`, `seed`, `absorbing`, `cavity`, `ramp`, `margin`, `emits`; `numbers[n]`: `position`, `family` | DECLARATION |
| 2.4 the detectors and emitters | `initialization.json`; `run.json` | `detectors[]`: `name`, `positions`; `measured[].lamp`: `rate`, `wheel`, `directions`, `train`; `measured[].emits`, `.held`; `probes`; `run.json` `detectors[]`: `name`, `positions` | DECLARATION |
| 2.5 the verbs | none (text) | MASSIVE_RECORD.md section 1 on the branch | none |
| 3.1 the box | `run.json` | `shape`, `boundary`, `families[].faces` | DECLARATION |
| 3.2 the marks by tick | `events.jsonl` | `birth`: `tick`, `node`, `record`, `u`, `train`, `clock`, `cycle` on a block's birth; `gather`: `tick`, `node`, `chosen`, `click`, `birth`; `click` (a block's self-click): `tick`, `node`, `cycle`, `clock`; `probe`: `tick`, `values` | GAMEBOARD; the `gather` and `click` marks DETECTOR |
| 3.2 the books by tick | `run.json` | `audit[t - 1]`: `families[name].measured.*`, `.transit.*`, `.form` under the key, `records`, `balanced`; `transit_content`, `measured_content` | GAMEBOARD |
| 3.2 the snapshot | `state.json` | `blocks[]`: `rows` (the block's own record over the board, in the board's order), `form`; `records[]`: `record`, `lamp`, `family`, `u`, `born`, `birth`, `age`, `train`, `norm`, `absorbed`, `pointers` {cell: pointer}, `form`; `measured[]`: `position`, `held` | GAMEBOARD |
| 3.3 the blocks moving | `events.jsonl`; `state.json` | `block` lines: `tick`, `measured`, `corner`, `steps`, `sum`, `clock`; `blocks[]`: `corner`, `side`, `steps`, `drive`, `momentum`, `responses`, `emitted`, `clock` | GAMEBOARD; `side` DECLARATION |
| 3.4 the detectors' cells | `run.json`; `events.jsonl` | `detectors[].positions`; the count of `gather` lines by `chosen` up to t | DECLARATION; the counts DETECTOR |
| 4.1 the detectors' records | `run.json`; `events.jsonl` | `detectors[]`: `name`, `positions`, `clicks`; the count of `gather` lines by `chosen`; the block's `click` lines: `cycle`, `clock` | DETECTOR |
| 4.2 the staircase | `events.jsonl` | `gather` lines: `clock` where `clock_stamp`, else `click`; the block's `click` lines' `cycle` against `clock` | DETECTOR (`clock`, `cycle`); `click` GAMEBOARD |
| 4.3 the intervals | `events.jsonl` | consecutive `gather` lines' `clock` or `click`; `birth` and `click` of each | CONVERSION; DETECTOR |
| 4.4 the pattern | `run.json`; the register beside the world where one exists | `detectors[].clicks`; `layer`: `born`, `gathered`, `open` | DETECTOR; PIN |

The keys of 5.3 are the branch's at `2f44797c`, read from the two runs of
section 0 and from `detector_law.py` (the `block` line written by
`_block_clock`, the `gather` at the layer's completion, the `probe` line
in `step`, the snapshot by `snapshot_stream`, the counts by `detectors`) and `run.py` on the branch (the `families[].pair` and
`.faces`, `massive_record`); BUILD.md section 3 promised the block line
"its cells' amplitudes" and `numbers` "per block its keys", and the
engine writes neither at this head, so the tool reads what is written
and the panels say "not recorded" for the rest. When the Boss's run
folders come, the tool is run headless on them first (section 7, test 7).

---

## 6. The technology

### 6.1 The choice: no external library; the 3-D as inline SVG with an inline script

The page stays one file with no external resource: inline CSS, inline
SVG, the board's data as one inline JSON element, and one inline script
of plain JavaScript (about 200 lines) for two things and nothing else:
the rotation of the board (an orthographic projection by two angles, yaw
and pitch, changed by dragging or by two sliders, the cubes and cells
drawn back to front by their projected depth) and the interval step
control of section 3.5. The script draws SVG elements from the JSON; it
computes no number of the record beyond placing a mark at its recorded
Node and shading a cell by its recorded integer, and it never writes a
number on the page that the tool's table does not already print with
its kind. Without the script the page shows the tool's pre-rendered SVG
(the board at the last interval, the default view) and every table, so a
reader with scripts off reads the whole record.

The alternative the task allows, an external library from
cdnjs.cloudflare.com or cdn.jsdelivr.net/npm named with its version
(three.js at `three@0.160.0` on jsdelivr, or the same at cdnjs), was
weighed and declined for four reasons: (1) the page must read offline
and as a file, as the first page does, and a library is a network
dependency the Artifact host allows but a saved file does not have; (2)
a WebGL canvas draws its numbers as pixels, so a number on it carries no
`data-kind` element and the labelling test (section 7, test 2) could not
see it; (3) the boards the schedule names (a 200^2 layer, a 48^3 box, a
1400 chain) hold a few thousand drawn cells at most under the cap of
section 3.5, well within what SVG draws; (4) the tool stays a reader
with no dependency to name and no version to keep. If a later world
needs more (a 191^3 box with a per-Node dump), the library's line is one
`<script src>` from the allowed hosts named with its version, added on
the Boss's word and not before.

### 6.2 The tool: extended, not forked

The folder `tools/algebra_visualizer/` keeps its four modules and gains
one:

- `record.py` (extended): `load_run(folder)` as today, plus `engine_of(meta)`
  (5.1), the readers of the new engine's lines (`block`, `probe`, the
  block's `click`, the `gather`'s `click` and `birth`), the readers of
  `state.json`'s `blocks` and `records`, and the old engine's `step`
  reader; the per-tick indexes (the lines by tick, a body's or a block's
  position by tick from its lines, a cell's click count by tick), each an
  exact index of recorded integers. Standard library only, no
  `event_universe` import (the first design's section 7.3 and its test 5).
- `panels.py` (extended): the algebra layer's five panels (section 2)
  built from one `RunRecord` for either engine; the Outside layer's four
  panels (section 4) taking the detectors from the run's tables; the
  first page's panels untouched.
- `board3d.py` (new): the GameBoard layer's model: the box, the cells,
  the marks by tick, the blocks by tick, the probes by tick, the books by
  tick, the snapshot under the cap; its output the JSON of section 3.5
  and the pre-rendered SVG's data. The projection lives here as the one
  place floats appear, in drawing coordinates.
- `svg.py` (extended): the wire box, the cubes, the faces and cells, the
  marks; the staircase, histogram and bars reused as they are.
- `render.py` (extended): `render.py RUN_FOLDER [--render OUT.html]` for
  one run folder of either engine (a folder holding `run.json`, or a
  series folder `<name>/run`); the first page's `render.py RUNS_DIR
  [--light NAME] [--detector NAME]` kept unchanged (a directory without
  `run.json` is the first page's runs directory). Headless by default: it
  prints every panel's numbers with their kinds and sources, the engine it
  found, and what the run keeps per Node, and writes nothing. `--render`
  writes the one HTML file and nothing else. It never runs the engine.

Dependencies: the standard library alone, as today; nothing added to
`pyproject.toml`; nothing in the runner path.

### 6.3 How the page labels every number

As the first design's section 8: every number in one element with
`data-kind` and `data-source` (the file and the key, `events.jsonl:
block.corner`, `run.json: families[].pair`, `state.json: blocks[].rows`,
`initialization.json: measured[].side`), a badge per kind, the legend on
the head and at the head of every layer, the GameBoard band titled "a
diagnostic". The JSON data element of section 3.5 is excluded from the
digit test's scan only because every integer in it is printed once more
in the panels' tables with its kind, which the test checks by parsing the
JSON and looking each integer up in the tables (section 7, test 2).

### 6.4 The first page

The two-run page of DESIGN.md (the light world beside the world with a
detector, published at the link in the README) is not changed by this
design; the same modules render it as before, and its tests stay.

---

## 7. The tests

`tests/test_algebra_visualizer.py` extended, or a sibling
`tests/test_algebra_visualizer_3d.py` loading the same modules by path,
as the Boss prefers (the design carries the sibling so the first page's
tests stay as they are). Fixtures, once per session: the old engine's
run made by the runner's API (`event_universe.runner.run_initialization`)
from `examples/events/amplitude/mz_equal.json` (80 intervals, cheap: two
one-Node sets, births, splits, records, gathers) into a temporary
directory, and one `step` line built by hand from `cart_k5`'s recorded
form (section 0) for the moving body; the new engine's run built by hand
in the test from the keys of section 5.3 (a chain of 40 Nodes, one lamp,
one block of side 3 with its `block` lines over 12 intervals stepping
once, two `gather` lines chosen at a screen with `clock`, one block
`click` line, `state.json` with `blocks[].rows` of 40 integers and one
`records[]` entry, `run.json` with `hypotheses` `["amplitude-v1",
"detector-law-v1", "massive-record-v1"]`, `massive_record` true, the
family `pair` and `faces`, the `detectors[].clicks` equal to the gathers,
the `audit` with `form`), written into a temporary directory. No test
pins a number of a world: every assertion is the tool's contract against
the record it read.

1. **Headless writes nothing.** `render.py FOLDER` without `--render`
   prints the table and leaves the directory without a new file, for
   each fixture.
2. **Every panel present and every number labelled.** For each fixture:
   the thirteen panels of sections 2 to 4 exist (3.5 is the control); every `Number` has a
   kind among the seven and a non-empty source; the JSON data of the
   board holds no integer that the panels' tables do not print with a
   kind; the GameBoard panels carry the title "a diagnostic"; a panel the
   run cannot fill says "not recorded" and carries no number.
3. **The readings equal the record's own totals.** The Outside's count
   per detector equals the count of `gather` lines chosen at it in the
   fixture's `events.jsonl`; on the new engine it also equals `run.json`'s
   `detectors[].clicks`; on the old engine the face counts equal the face
   `click` lines; the block's cube at the last interval stands at
   `state.json` `blocks[].corner` and the old body's box at `measured[].position`;
   the books' numbers at the last interval equal `audit[-1]` as read; the
   snapshot's cells equal `blocks[].rows` (or the summed `nodes`) as read;
   the intervals between clicks are the differences of the recorded
   counts. Each is the tool against the file it read.
4. **The refusals.** A folder without one of the four files names the
   runner's line; a `run.json` without `hypotheses` is refused naming the
   key; a run of either engine without `gather` lines fills the Outside
   with "not recorded" and does not fail; a run of the new engine without
   `blocks` in its snapshot (a world without the key) draws no cube and
   does not fail.
5. **No engine import beyond the readers.** The five modules' import
   lists (by `ast`) hold no `event_universe`, `numpy`, `matplotlib`,
   `PIL` or `playwright` name, and importing `render.py` loads none.
6. **The page (under `--visualize-runs` only, marked `visualization`).**
   `render.py FOLDER --render OUT.html` writes one file per fixture; it
   parses; it holds the three layers' titles, the legend, the
   fingerprints, the engine's name, the "GAMEBOARD, a diagnostic" title,
   the JSON data element whose interval count equals `completed_ticks`,
   no `<script src>` and no `<link href>` to any host, no run of digits
   outside a labelled element, and its size is below 8 MB.
7. **A fixture run of each engine, and the first real folders.** The
   old engine's fixture is the runner's; the new engine's is the
   hand-built record until the engine is on `main`, when a test makes it
   with the runner's API from the branch's chain world and the hand-built
   one goes. When the Boss sends the first run folders, `render.py
   FOLDER` headless on each is the first check; a key that shows "not
   recorded" where the folder has it under another name is reported to
   the Boss with the folder and the key, and the tool is changed only on
   his word.

`python tools/check.py --base origin/main` selects the tests through the
tool's path and the documentation gates for this file and its index row;
ruff formats and checks the five modules; mypy covers `src/` alone.

---

## 8. What the page will NOT do

- No physics computed: no rule evaluated, no row stepped, no pointer
  summed, no table of the engine loaded, no interpolation of a block
  between two recorded lines; the only arithmetic a sum of recorded
  integers (a Node's rows, a plane's cells under the cap), a difference
  (the intervals between clicks, a record's age) or a ratio, exact and
  labelled CONVERSION or GAMEBOARD as its inputs are.
- No replay of the law: the board at interval t is the record's lines at
  t and nothing the engine would compute from them; a Node the record
  does not write is drawn empty and the caption says the run keeps no
  per-Node state per interval (Finding 1).
- No pin moved, no verdict: a register's number is PIN beside the run's,
  nothing is called PASS, FAIL, SEEN or matched, nothing is compared with
  nature.
- No run made: the tool never starts the engine; a missing folder is a
  plain refusal with the runner's line.
- No render dependency and no network resource: standard library alone;
  no library from a host unless the Boss orders one (section 6.1); no
  frame capture, no GIF, no image file.
- No new world, no new key, no engine line: the two engines' records are
  read as they are written; a key the engine does not write is "not
  recorded".
- No wording of its own on the physics: every sentence of the algebra is
  quoted from ALGEBRA.md, Highlights 5.4, ENGINE.md, TERMINOLOGY.md or,
  for the new engine, the branch's design files with their sections.
- No change to the first page and its tests.

---

## 9. The cost

| Item | Host time | Kind |
| --- | --- | --- |
| STEP 1, this file | about 40 minutes of one agent | HOST |
| STEP 2, the build (section 10) | about 7 hours of one agent end to end | HOST |
| the render of one run: one pass over `events.jsonl`, `state.json` and `run.json`; the JSON and the SVG | under 3 s for a run of the size of `cart_k5` (600 intervals, 3,400 lines); under 10 s for a 200^2 layer world of the schedule with a snapshot under the cap | HOST |
| the page's size | a few hundred kilobytes for a small run; about 2 MB at the cap of 20,000 snapshot cells and a few thousand marks; under 8 MB by the test, well under the Artifact's 16 MB | HOST |
| the tests' fixtures | the `mz_equal` run about 0.3 s once per session; the hand-built record under 0.1 s | HOST |
| the page for the owner | one existing registered run made outside the tree at the head named for STEP 2 (`cart_k5`, the one registered world whose lines carry `clock` and whose body steps, 3.6 s; or the run the Boss names) | HOST |

Nothing of it touches the engine, a world, a pin or a key, so nothing of
it is dangerous; the one gate it can break is the documentation index,
which `check.py` runs.

---

## 10. The build's steps for STEP 2, in order, with their sizes

Only on the Boss's GO after his read of this file. Sizes are host
estimates of one agent's time and of lines of Python.

1. **The readers and the detection** (`record.py`, about 150 lines, 60
   minutes): `engine_of`, the new lines' readers, the per-tick indexes;
   test 5's import gate and test 4's refusals written first.
2. **The algebra layer** (`panels.py`, about 200 lines, 60 minutes): the
   five panels of section 2 for either engine, every integer DECLARATION
   with its key.
3. **The board in 3-D** (`board3d.py` and `svg.py`, about 400 lines, 120
   minutes): the model, the cap, the JSON, the projection, the
   pre-rendered SVG; test 3's positions and totals.
4. **The Outside layer** (`panels.py`, about 150 lines, 60 minutes): the
   four panels of section 4 from the run's own detector tables, the
   stamped count where present.
5. **The page and the script** (`render.py`, about 300 lines of Python
   and script, 90 minutes): the run-folder argument, the head with the
   engine, the bands, the step control, the rotation; tests 1, 2 and 6.
6. **The checks** (30 minutes): `ruff format`, `ruff check`, `python
   tools/check.py --base origin/main`, then `pytest --visualize-runs` once
   for the page test, headless otherwise.
7. **The run, the page and the record** (60 minutes): one existing
   registered run made outside the tree at the head, the render, the page
   read by eye against sections 2 to 4, the private Artifact page for the
   owner (the `artifact-design` skill loaded first), the README's row and
   the page's link, the index row of docs/README.md; open no PR, report
   to the Boss with the SHA.

---

## 11. The questions to the Boss, with the answer the design carries

1. The new engine is not on `main`. Does the Boss want STEP 2's page made
   from a run of the old engine (the design names `cart_k5`, the one
   registered world whose body steps and whose lines carry `clock`), with
   the new engine's readers tested on the hand-built record until his
   first run folders come; or does he want STEP 2 to wait for the branch
   to merge? The design carries the first.
2. The tests: extend `tests/test_algebra_visualizer.py` or add the
   sibling `tests/test_algebra_visualizer_3d.py`? The design carries the
   sibling, so the first page's tests stay as they are.
3. The 3-D: no external library, an inline script (section 6.1). If the
   Boss wants three.js from one of the two allowed hosts instead, the line
   is `three@0.160.0` and the labelling test loses the numbers drawn on
   the canvas; the design carries none.
