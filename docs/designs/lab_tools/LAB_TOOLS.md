# The lab tools: one specification per tool, each with its body, its algebra, its timing, its cost, its engine lines and its unit tests' expected values (the mathematician, 2026-09-24; checked by the physicist; docs only)

THE OWNER'S WORDS (2026-09-24, records 1825, 1830, 1831 and 1832 of
docs/LOG_2026-09-20.md, on the Boss's log branch until it merges; the
Boss's orders of 17:25Z to 18:20Z): there are three levels, the building
blocks, the lab tools and the experiments; every tool gets its algebra
and is checked by its own tests before it enters an experiment; "all of
the above is defined in one specification file of the lab tools; the
mathematician can write the design of everything; Nature just checks all
of it and talks with him"; "every instrument has a specification with
its direction and the rest, and tests". A tool declares its own
orientation and never the directions of what leaves it (record 1830).
The split and the carrying of amplitude are the board's own (record
1831).

THE WORDS OF THIS FILE (docs/TERMINOLOGY.md: "the Node holds no wave").
On the GameBoard a record holds one integer amplitude per Node at two
levels (now and before, with the remainder), and the one local rule at
each Node is THE SPLIT: the six neighbours' amplitudes summed with the
kind's pair, the Node's previous amplitude subtracted, one integer
division with the remainder kept (DESIGN.md section 2; ALGEBRA.md 8.1).
A "wave", its "wavelength", its "wave vector" **k** and "phase matching"
are the OUTSIDE READING of that rule (the characters of the torus that
the rule maps to themselves, ALGEBRA.md 1.6 and 8.1); every sentence
below that uses them says what the rule does to the amplitudes, and the
reading is named as such.

NO TABLE ANYWHERE (the owner's word of 2026-09-24, 18:55Z, through the
Boss: "make sure we have no such thing at all as Nodes with a table; it
should not exist at all"). A Node carries only its NodeState and the one
rule acts; every tool is a BODY OF MATERIAL whose Nodes carry only
material integers. THE MATERIAL, one form for every tool (HISTORY in its angle and its
take, superseded by part A: the angle is the integer axis (a, b) of
ALGEBRA.md 9.14 (b), ADOPTED, and the take is removed, 9.12): per LABEL,
the label matrix **M**_u = [[a, b], [-b, a]] of the body's axis on the
record's label rows (ALGEBRA.md 9.16 (2); never a Node's table), and per
FAMILY where two families meet (the crystal), an INDEX PAIR (the
coefficient [num, den] = 1 / n^2 of DESIGN.md 4.1); the rotation is a 2
x 2 over the labels (verb B). THE ONE ENABLING ENGINE LINE for all of it:
ONE AMPLITUDE PER LABEL VALUE on every record (two fields, H and V,
each stepped by the split with its own pair), which the crystal needs
anyway; a record of rank 2 keeps its joint label state for the gather,
and each arm's amplitudes per label carry its timing and its books. WHAT
RETIRES on main: the table body of two cells (`TableBody`, the split by
declared weights), the splitter of the table form (`Splitter`, declared
inputs, weights and outputs, with the linear form it reads), and the
rules by family name (the old transponder's `rerelease`); the setting's
key `phase_window` becomes the body's `axis`.

THE FORM OF EVERY SECTION: what the tool is and what nature gives it; ITS
BODY (declared by its cube's lower vertex and its edge, as every body:
a cube on a board, a square on a layer, a segment on a chain, the
smallest of side 1; SIMULATOR_DEFINITIONS.md "The body"), its kind, and
whether it is a WELL (a lowered pair trapping a bound mode, the foreign
body of ALGEBRA.md chapter 8, with its load-time conditions) or a
MATERIAL (a pair or a table and no bound mode); its orientation,
declared by itself; its action on every kind of input (every label, a
superposition, every Port); its timing; its cost; the engine lines it
needs, each with the three tests (generic, vector, local;
[skills/workflow.md](../../../skills/workflow.md)); its unit tests' exact
expected values. Each statement carries its kind: PROVED HERE,
COMPUTATION (exact integers from main's own functions, or the Outside
reading's closed form in floating point, labelled so), MEASURED ONLY (a
board quantity no closed form reaches; a run may read it and never pin
it), or DECLARATION. Existing design files are cited, never copied.
Nothing here is code; the physicist writes the code, the worlds and the
test-run lines, each tool's code after its section is agreed.

THE SYMBOLS USED IN SEVERAL SECTIONS (HISTORY where marked; part A
holds). N = 2048 the phase circle's steps (W = 2048 the birth wheel:
HISTORY, no wheel is declared, ALGEBRA.md 9.19 (4)); a clock pair [p, q]
is the born character's PHASE PER LINK, k = 2 pi p / (q N) (ALGEBRA.md
9.17 (4)), and its frequency omega (per interval, an Outside reading)
follows from the band along a lattice axis, 3 cos omega = cos k + 2:
the light family's clock [2464, 25] has k = 0.302378 per Link, omega =
0.17413, a period of 36.08 intervals and a wavelength of 20.78 Links
(the earlier reading of [p, q] as omega, "a period of 20.779 intervals",
is HISTORY: 20.78 is the wavelength in Links); the halved clock [1232,
25] has k = 0.151189, omega = 0.08723, a period of 72.03 intervals and
a wavelength of 41.56 Links; the Outside reading of the split, 3 cos
omega = cos k_x + cos k_y + cos k_z (ALGEBRA.md 8.1 at [1, 1]), with
**k** the wave vector (bold lowercase, a vector); c = 1 / sqrt 3 Links
per interval; a label is an integer whose bit j is the value on arm j
(0 for H, 1 for V); the branches [[label, weight], ...] a record's joint
labels with integer weights from 1; C'[s], S'[s] and **U**_s = [[C'[s],
S'[s]], [-S'[s], C'[s]]] (the half-angle tables at the setting s, bold
uppercase a matrix): HISTORY, the axis (a, b) and **M**_u replace them
(ALGEBRA.md 9.14 (b)); R a cell's weight; E(a, b) a correlation and S
the CHSH sum.

---

## A. THE SPECIFICATION: every tool from ALGEBRA.md chapter 9 alone (the Boss's order of 2026-09-24, 22:10Z: "LAB_TOOLS.md becomes the one complete file")

THIS PART HOLDS. Sections 0 to 12 below are the derivations and the
settlements with the physicist that led here; where they differ from this
part, they are history. Every line cites the section of
[ALGEBRA.md](../../ALGEBRA.md) chapter 9 it comes from.

**A.0 The generic primitives: the law's components, with no family name
and no tool name.** Every tool is built from these alone.
- **R**, THE RULE: the split at every Node, with that Node's pair per
  family (8.1). A tool's material is its pair per family on its cells.
- **E** then **D**, THE CLICK: the evaluation of a record's offer at the
  cells its ladder names, then the rung 2 T u + T <= 2 W C_k (2.5, 3.1,
  8.6). Only a record that names the cells is read (9.7).
- **X**, THE CLICK'S ACTION: the record ends, all its rows, at its click
  (9.12; the close of the first reading is superseded by 9.19 (3) (a):
  the ladder is read at every interval and the face receiver is last on
  it). There is no take.
- **E**^T, THE BIRTH: a record written at the cells by its own clock
  (9.13).
- **B**_u, THE LABEL MATRIX: verb B with the integers of an axis on a
  record's label rows (9.16 (2); section 12.2).
- THE LOADER'S CHECKS: integer checks at load, never the law's (9.5).
- THE FACES: the segment's border, the row beyond read as 0, with the
  receiver `face` at the border of an open axis, last on every ladder
  (1.6; 9.19 (3) (a), Highlights' record 15 kept; "a closed face that
  reflects" is HISTORY).
- THE BOARD AT INTERVAL 0: the occupied bound bodies' own records, each
  the composed operator's mode at its amplitude, the emitter bodies'
  first excitations among them; nothing else (9.9, 9.22 (3)).

**A.1 The emitter.**
- Its group element: **E**^T. The orbit sum of a Port, the projector onto
  G_48's trivial representation (9.4, 9.13).
- A direction: NONE. A beam is a line of emitter cubes born in phase, a
  placement (9.6).
- Its primitive: its own record's click (**E**, **D**, **X**), then
  **E**^T, which writes the born record's two levels once on its cells
  (ALGEBRA.md 9.17). There is no drive: `_drive`, the block's source
  term and the lamp's rate accumulator retire. The body holds M excited
  records IN TURN, each clicking at its own rung, each click birthing the
  photon and the next excitation (9.17 (4)). A narrow train is a line of emitter cells n
  wavelengths long.
- Its material integers: its body's (a block of a massive kind with its
  own record, 8.3); the born family and its clock [p, q]; the amplitude
  A; the line's length in wavelengths; the label state (branches). No
  wheel and no residue order: u is the law's remainder at the centre cell
  (ALGEBRA.md 9.19 (4)), so the body's well pair is rich, 3 x denominator
  / gcd(numerator, 3) >= 500 ([800, 801], never [800, 800] or [8, 7]).
- On the board at interval 0: its first excited record, the body's
  composed mode (9.17 (4), 9.22 (3)); the births come later.
- Its load check: every birth has a clicking record behind it (9.17);
  `arms` is refused; a declared wheel or residue is refused; the centre
  cell's pair is rich (9.19 (4a)).
- Its unit tests: the excited record's norm per period and the born
  pair's check (9.17 (5)); the six tests of 9.20 (B) on the planted
  board; nothing reaches Manhattan distance m before age m. HISTORY (the
  drive's era, COMPUTATION on main's `_births` and `_phase`): at [2464,
  25] and 128 periods the train lasted 3200 intervals; at one Node, N =
  2048, the norm was 9517232; the share of its own record's norm that
  its own cells book (9.10 item 1) is RETIRED with the take (9.12), the
  emitter's own record clicking at its own rung by the flux (9.19 (3)).

**A.2 The receiver.**
- Its group element: **E** then the rung: a scalar, the trivial
  representation (9.4, 9.12).
- A direction: NONE.
- Its primitive: **E**, **D**, **X**.
- Its material integers: its name in the ladders of the records it reads
  (the ladder by name). No take pair (9.12) and no wheel: the rung's wheel
  is the record's own (ALGEBRA.md 9.19 (4)).
- On the board at interval 0: nothing.
- Its load check: every ladder names only declared receivers; the
  generator's timing condition that each record's click or close comes
  before the first face reflection reaches its receivers (9.12 item 2;
  the per-row margins are in B).
- Its unit tests:
  - A record of branches [[0, 1], [1, 1]] clicks at the same interval as
    a one-label record of the same norm.
  - A record clicks once. From the next interval its rows are 0
    everywhere.
  - The Inside's content is conserved exactly until the click (8.8).

**A.3 The mirror.**
- Its group element: the reflection, -I times the half-turn of V_4 about
  the normal of the face met, realised by a gap (9.2, 9.4).
- A direction: none of its own on a cube; a slab's unoriented normal.
- Its primitive: **R**, with the gap pair on its cells.
- Its material integers: the gap pair [num, den] for light; the side
  (its depth).
- On the board at interval 0: nothing.
- Its load check: every clock that reaches it lies below its gap; the
  transmitted share at its depth is below the declared bound.
- Its unit tests (COMPUTATION, the chain's exact harmonic solution; an
  emitter of [2464, 25], the gap [1, 2]):
  - The transmitted share is 3.000 x 10^-2 at depth 1 and 5.561 x 10^-4
    at depth 2. The interval over the train at depth 2 is [5.314 x 10^-4,
    5.816 x 10^-4].
  - The reflection's delay is 4.085 intervals, against 3.547 for the
    closed face: a difference of +0.538.

**A.4 The splitter.**
- Its group element: the mirror's reflection weighted by r and the
  identity weighted by t (9.2).
- A direction: its plane's normal (a layer of cubes of side 1).
- Its primitive: **R**, with the layer's pair.
- Its material integers: the pair [91, 107] at [2464, 25], or [183, 199]
  at [1232, 25].
- On the board at interval 0: nothing.
- Its load check: the share computed from the pair at the declared
  clock, printed at load (GAMEBOARD).
- Its unit tests: 0.49987 reflected and 0.50013 transmitted; the
  interval over the train is [0.4901, 0.5098].

**A.5 The polariser.**
- Its group element: the rational projector **P**_u = **u** **u**^T /
  abs(**u**)^2, in the image M_2(Q) of Q[G_48] and NOT in G_48 (9.14
  (b), ADOPTED).
- A direction: NO SPATIAL DIRECTION. It is chiral: a reflection sends the
  axis (a, b) to (a, -b).
- Its primitive: **B**_u, **M**_u = [[a, b], [-b, a]] on the label rows;
  the click's weights R = J^2 through `joint_weights` with (a, b).
- Its material integers: the axis [a, b], with a^2 + b^2 > 0 and gcd(a,
  b) = 1 (one form per axis), and its two receivers (+ along the axis, -
  across it).
- On the board at interval 0: nothing.
- Its load check: the axis's conditions; the two receivers named.
- Its unit tests:
  - Malus at 256 records, H arriving: the expected values 128.0, 246.2,
    199.3 and 177.2 at (1, 1), (5, 1), (15, 8) and (3, 2) with their
    binomial bands (ALGEBRA.md 9.19 (4b); the wheel [159, 256] is
    HISTORY).
  - The norm identity: 77^2 + 36^2 = 289 x 25.
  - HV + VH books a^2 + b^2 on each of + and - (section 12.2).

**A.6 The crystal.**
- Its group element: **E**, then m^T, then **E**^T (9.13). It is
  equivariant under all 48 on a cube.
- A direction: NONE of its own. The headings are the placement's (9.3,
  9.16 (6)).
- Its primitive: **E**, **D**, **X** on the arriving record (the crystal
  is its named receiver), then **E**^T: the pair record born on its cells
  by its own clocks, carrying the arriving record's residue u (9.7 (b)).
- Its material integers: the born clocks p_1 + p_2 = p (one split, or the
  window of section 12.1); the branches [[1, 1], [2, 1]], which are a =
  b = 0 and c = 1 (9.16 (5)); `label_hands`; the born amplitude.
- On the board at interval 0: nothing (no seed, 9.7).
- Its load check: p_1 + p_2 = p exactly; the crystal is the arriving
  record's named receiver; the branches lie in a maximally entangled
  family (b = -a, or c = 0 and a = b).
- Its unit tests:
  - W arriving records give W pairs (one quantum, one click).
  - The Bell pins of B.
  - A mirror-symmetric placement gives both arms the same first rung
    (the mirror theorem).

**A.7 The well.**
- Its group element: the bound mode of a lowered pair on a G_48-set, a
  character of the time translation at **k** = 0 (8.3).
- A direction: NONE at rest; in motion, its declared momentum.
- Its primitive: **R**, with the lowered pair; **E**, **D** on its own
  record at its own block (8.6).
- Its material integers: the pair, the side, the momentum with its ramp,
  the coupling, a stock where it births (9.17 (4)); the seed is the
  generator's, not a declaration (9.22 (3)); no wheel and no `emits`
  (9.19 (4), 9.17).
- On the board at interval 0: its record, carrying its seed, the mode of
  the COMPOSED world (9.9).
- Its load check: the body check (8.7), extended by 9.9: the bodies'
  cells disjoint; the seed recomputed on the composed operator, bit for
  bit; the hybrids' share within the band.
- Its unit tests: section 4.1 and the rest worlds' pins (B).

**A.8 The transponder.**
- Its group element: a well that also carries light's gap: the mirror's
  reflection in the moving body's frame (section 8).
- A direction: its declared momentum.
- Its primitive: **R**, with two families' pairs on the same cells.
- Its material integers: the well's, plus the gap [1, 2] for light.
- On the board at interval 0: the well's seed.
- Its load check: the well's and the mirror's.
- Its unit tests: at rest, the reflected clock equals the sent one
  exactly. At k = 3 the sent over the received clock is 3.7733 at [2464,
  25] and 3.7420 at [1232, 25] (blind).

**A.9 The faces.**
- Its group element: the segment's border (1.6): the row beyond read as
  0.
- A direction: the axis's normal.
- Its primitive: **R**.
- Its material integers: none. Each axis is periodic, or open with the
  face receiver `face` at its border on every ladder's end (Highlights'
  record 15, kept: what leaves clicks there; ALGEBRA.md 9.19 (3) (a)).
- On the board at interval 0: nothing.
- Its load check: a periodic axis or a face receiver on every axis (a
  closed board is refused); the timing condition of A.2.
- Its unit test: the closed face's reflection delay on the chain at
  [2464, 25] is 3.547 intervals.

**A.10 THE ONE TABLE (the owner's word of 22:30Z: every tool, click or
no click, the rotation of its shape, its primitive, its material).**
Every tool is the law's advance on its material plus at most a click
(ALGEBRA.md 9.17). Every tool is a BOUND body of the HOLDER family carrying
its light material (ADOPTED, record 1875, 2026-09-25 on the Israel
clock), so that its own record's vector carries the push and
momentum is conserved on the board (9.15). Its mass is written so that
it drifts less than one Link over the run.

| Tool | Click? | Its group element: the rotation of its shape | A direction? | Its generic primitive | Its material integers |
| --- | --- | --- | --- | --- | --- |
| Emitter | YES: its own record clicks, and the birth is the click's other side | **E**^T, the projector onto G_48's trivial representation (the orbit sum of a Port) | none on a cube; a line of cells gives a line's (a placement) | its own record's **E**, **D**, **X**, then **E**^T once | the block's pair, side and seed; the born clock [p, q]; A; the line's length; the branches; a stock M (no wheel, 9.19 (4)) |
| Receiver | YES | **E** then the rung: a scalar, the trivial representation | none | **E**, **D**, **X** | its name in the ladders (no wheel) |
| Mirror | no | the reflection -I x (the half-turn of V_4 about the face's normal), arising from the gap | none on a cube; a slab's unoriented normal | **R** with the gap | the gap [num, den], the side |
| Splitter | no | the reflection weighted by r, the identity by t | the layer's normal | **R** with the layer's pair | [91, 107] at [2464, 25] |
| Polariser | no of its own; its two receivers click | the rational projector **P**_u in Q[G_48]'s image M_2(Q), not in G_48; chiral: (a, b) -> (a, -b) | no spatial direction | **B**_u on the label rows | the axis [a, b], gcd 1; its two receivers |
| Crystal | YES: the arriving record clicks at it, and the pair is born | **E**, then m^T, then **E**^T; all 48 on a cube | none; the headings are the placement's | **E**, **D**, **X** on the arriving record, then **E**^T | the born clocks p_1 + p_2 = p; the branches [[1, 1], [2, 1]]; `label_hands` (no wheel, 9.19 (4)) |
| Well | YES: its own record's clicks (its clock) | the bound mode, a character of the time translation at **k** = 0 | none at rest; its momentum in motion | **R** with the lowered pair; its own **E**, **D** | the pair, the side, the momentum and ramp, the coupling (no wheel; the seed is the generator's) |
| Transponder | its own record's clicks; the reflection itself does not click | the well's, plus the mirror's reflection in its moving frame | its momentum | **R** with two families' pairs | the well's, plus the gap [1, 2] for light |
| Faces | no | the segment's border, the row beyond read as 0 | the axis's normal | **R** | none (per axis periodic, or open with the receiver `face`; A.9) |

**A.11 The crystal's keys for its world file (the physicist's two
questions of 18:50Z).**
- (1) THERE IS NO TAKE PAIR: the take is removed (ALGEBRA.md 9.12). The
  crystal's cells are the arriving record's NAMED RECEIVER, and its
  material is its light pair (the vacuum's [1, 1] unless an index is
  declared) and its massive body's pair.
- (2) THERE IS NO WHEEL KEY (ALGEBRA.md 9.19 (4), ADOPTED): the pair's
  residue u is the arriving record's remainder at the crystal's centre
  cell at its click, and its wheel is 3 x denominator / gcd(numerator, 3)
  of the crystal's LIGHT pair there; so the crystal declares on its cells
  a light pair rich enough, an index such as [800, 801] (2403 values),
  never the vacuum's [1, 1] (3 values).
- (3) No residue order and no seed anywhere: the loader refuses them.
- (4) THE SHELL OF RECEIVER CUBES RETIRES with the take. An open face is
  the receiver `face` at the border (A.9; ALGEBRA.md 9.19 (3) (a)), so
  the two slits' layer gains no bodies; its regeneration follows B's
  margin.

**A.12 THE UNIFICATION, ADOPTED (ALGEBRA.md 9.18; the model owner,
record 1875, 2026-09-25 on the Israel clock).** The nine tools of A.10 are ONE OBJECT: a body, a cube of
a massive family whose cells carry optional integers. The emitter, the
receiver and the clock of the definitions' four building blocks become
options and readings of that one body.

| The body carries | It is |
| --- | --- |
| nothing more | the well |
| a light pair | the mirror, the splitter, an index slab |
| an axis (a, b) | the polariser |
| a coupling (g, G) | the index rows' medium |
| a birth triggered by its own excited record, and a stock M | the emitter |
| a birth triggered by a named arriving record | the crystal |
| its name in ladders | the receiver |
| a light pair and a momentum | the transponder |

- A body is BOUND: its own record, of the holder family, its momentum by
  the push and its seed the composed mode (ADOPTED, record 1875); the
  silent body (no record, momentum leaving the board at it) is HISTORY.
- The faces are not a body.
- THE FAMILIES OF A WORLD: light [1, 1]; the experiment's matter, where
  it has matter; and, with bound tools, ONE HOLDER FAMILY for the tools'
  bodies. The holder must differ from every family a tool acts on or
  reads, because a Node carries one pair per family (ALGEBRA.md 9.18 (2)).
  At most three families, with no duplicate.
- THE GENERIC PRIMITIVES: the rule, the coupling, the label matrix, the
  click, the click's action, the birth, the push, a count on a record's
  own age, and the loader's checks (ALGEBRA.md 9.18 (4)).
- THE LAW USES NO TABLE, NO ROOT AND NO FLOAT once the retirements of
  9.18 (5) are made. The tables stay only in the readers and in the
  generator.

## B. THE FIFTEEN EXPERIMENTS AS PLACED TOOLS (cubes on a torus; RUN_LIST.md's rows; the pins blind, written before any run)

THE TIMING'S FORM, in every row: nothing reaches a receiver at Manhattan
distance m before age m (the causal bound). The front's K form is
distance / v_g. For light at the born clocks [2464, 25] (N = 2048), [77,
25] (N = 64) and [308, 25] (N = 256), the same k = 0.3024 per Link, so v_g = 0.5729 Links per interval and the period is
36.08 intervals. For the chains' light at [1, 1] on N = 64, v_g = 0.5769
and the period is 110.9. For the index clocks, v_g = 0.5773 (COMPUTATION
on the band 3 cos omega = cos k + 2).

THE FACE MARGIN: M is the distance from a reading's receiver to the
nearest face behind it. The first reflection reaches the receiver 2 M /
v_g after the front. A reading must end before that, or it must be one
where a shift common to every record cancels.

| Row | The board and its faces | The placed tools (vertex, side, material) | The pin (kind) | When the clicks come |
| --- | --- | --- | --- | --- |
| Bell, four settings (1a to 1d) | a layer [30, 33, 1], periodic (11.3); its shell of receiver cubes retires with the take (9.12) | an emitter at (2, 16); the crystal, side 3, at vertex (13, 15), clocks p_1 + p_2 = p, branches [[1, 1], [2, 1]]; Alice's polariser at (26, 28) with its receivers at (27, 29), axes (1, 0) or (1, 1); Bob's polariser at (26, 4) with (27, 3), axes (1, 2) or (3, 1); no wheel: the residues are the law's remainders (ALGEBRA.md 9.19 (4), ADOPTED; the exact W = 20 pin HISTORY) | n = 100 pair records per setting: the expected counts 40/10/10/40, 5/45/45/5, 45/5/5/45, 40/10/10/40 with the standard deviations 4.9, 3.0, 3.0, 4.9 and 2.2, 5.0, 5.0, 2.2; S = 2.80, standard deviation 0.141, the pin S in [2.38, 3.22], the falsifier S <= 2 (K, DETECTOR; ALGEBRA.md 9.19 (4b)) | birth at t_e + 11 or later; each arm's first rung at the birth + 22 or later; the two arms equal exactly (11.3); the first rung is the direct front's, before any wrapped field returns (ALGEBRA.md 9.12), and the counts are computed weights |
| Malus, four settings (9) | the bar of 8 (a chain) with the face receivers | an emitter body at x = 0 (H, a stock of 256; the wheel and the train are HISTORY, 9.22 (2)); the polariser at x = 6 with the axis (1, 1), (5, 1), (15, 8) or (3, 2), its + receiver at x = 7 | at 256 records on the + cell: 128 +- 24, 246 +- 9, 199 +- 20, 177 +- 22 (3 standard deviations; the expected 128.0, 246.2, 199.3, 177.2) (K, DETECTOR; ALGEBRA.md 9.19 (4b)) | the front at 6 / 0.5729 = 10.5 intervals from each birth; the reading is the computed weights, which a face does not move (9.12) |
| The two slits (2a) | 160 x 256 layer with the face receivers and the margin | an emitter at (20, 128) (no heading, on regeneration); a wall of mirror cubes, side 1, gap [1, 2], at x = 40 with two openings of width 3 at d = 26; the screen of 201 receivers at x = 153, y 28 to 228 (the wheel 2^20 is HISTORY) | visibility 0.96 +- 0.02 (K, `two_slits_1024.py`) | the front at the screen 133 / 0.5729 = 232 intervals after a birth. FACE MARGIN 6 Links (x) and 27 (y): the reflection comes 21 intervals after the front, while the train (32 periods, 1155 intervals, 661 Links) needs a margin of at least 331 Links. THE BOARD MUST GROW to x >= 485 with the y faces 331 Links beyond every path, or the train must shorten. The generator's map re-derives the pin on the grown board (OWED, blind) |
| The pace fans (5a) | 128 x 128 layer with the face receivers and the margin | an emitter at (64, 64); probes at 40 and 36 Links on each ray | the axis's k above the diagonal's by k^2 / 48 (K; GAMEBOARD by declaration) | the front at 40 / 0.5729 = 70 intervals; FACE MARGIN 23 Links, a reflection 80 intervals after the front, so the settled reading must end before it or the board grows (OWED on regeneration) |
| The muon's form (4a) | 200 x 200 layer, periodic | one well, side 14, pair [3200, 3227], at (93, 93), at rest and at k = 3 (ramp 12000) | f / f_0 = 0.8116, band 0.3 percent (K) | its own record's clicks over the hold after the ramp; no face |
| The redshift (4b) | chain 4096 with the face receivers | a moving well, side 12, pair [314, 315], at 2994, emits light; a receiver at 4094 | 1 + z = 1.9889, band 0.3 percent (K) | FACE MARGIN 1 Link: a shift of about 3.5 intervals common to every record, which cancels in the ratio of intervals |
| The round trip (4c) | a chain with the face receivers | an emitter with its receiver at rest; a transponder (A.8) at k = 3 | (1 + beta) / (1 - beta) = 3.7733 on the board's band at [2464, 25] (blind, A.8); 3.732 the continuum form beside | the round trip 2 D / (c (1 - beta)); the file `cart_k3.json` is the table form and is REBUILT as A.8 |
| Sagnac (R2) | chain 3000 with the face receivers | two wells, side 12, pair [800, 801] (ALGEBRA.md 9.19 (4a); [800, 800] HISTORY), at 700 and 772, co-moving at k = 3 or at rest; receivers by name (at_a, at_b) | 108 (rest), 247 and 72 (k = 3), each +- 2, and the ratio 0.5774 +- 0.01 (K): OWED, re-derived blind on the flux form and [800, 801] before any run | the first rung from each birth; the two wells hybridise by 3.2 x 10^-6 over the run at [800, 801] (ALGEBRA.md 9.9), and the seeds are regenerated on the composed world |
| de Broglie's fringes (M1) | 128 x 128 layer, x with the face receivers and the margin, y periodic | a matter emitter at (20, 64); the take lines' 256 cubes of the vacuum pair [800, 809] (they RETIRE with the take); a wall of 252 gap cubes [1, 2] with its openings; 121 receivers at x = 104 (the wheel 65536 is HISTORY) | the side lobe's centroid at y = 64 + 27.4, band one Node (K) | the matter front's pace per the band; FACE MARGIN 23 Links behind the screen, so the close must come before the reflection (the generator's check, OWED) |
| The moving mass's energy (M2) | chain 200 with the face receivers | a matter emitter body at 20 with a stock (the train is HISTORY); a receiver at 104 | 169 +- 2 (K): OWED, re-derived blind on the flux form before any run | the first rung from the birth; FACE MARGIN 95 Links, so a reflection returns long after the first rung |
| The bound clock's second term (ii-a, ii-b) | cubes 64^3 and 48^3, periodic | one well, side 20 or 28, pair [800, 801] ([800, 800] HISTORY), at rest or at k = 3 | 0.7814 and 0.8032, band 0.3 percent (P) | its own clicks over the hold; no face |
| The deep well (control) | 128 x 128 layer, periodic | one well, side 40, pair [800, 801] ([800, 800] HISTORY), at (44, 44) | 0.7531, band 0.3 percent (CONTROL) | its own clicks over the hold; no face |
| The light clock | chain 674 with the face receivers | a well A, side 12, pair [800, 801], at 600, with a stock (`emits` HISTORY), receiver at_a at 612; the mirror body, gap [1, 2], at [672, 674) | 214 +- 1 (K; OWED, re-derived blind on the flux form and [800, 801] before any run; the physicist's blind map with the material mirror [1, 2] at [672, 674) on the chain of 674; 213 on the closed face HISTORY) | the first cycle's first rung at 612 from its birth, after one reflection |
| The receding index at k = 3 (v-m) | chain 4000 with the face receivers and the margin | an emitter at 800 (the clock [3565, 10000]); a moving well, side 24, pair [314, 315], at 1500; the rest and reference worlds beside | the lab phase +1.0144 rad +- 0.04; the drift 1.2 x 10^-3 rad per interval +- 10 percent (P; GAMEBOARD by declaration) | the probe's window [3800, 5400]; FACE MARGIN checked by the generator against the window (OWED) |
| The receding index at k = 4 | as at k = 3 | as at k = 3, at k = 4 | +0.6103 rad +- 0.04; drift 4.3 x 10^-4 rad per interval +- 10 percent (P) | as at k = 3 |

THE CONSEQUENCE OF THE FACES (the face receivers of ALGEBRA.md 9.19 (3)
(a) in place of the closed faces of 9.12 item 3; the zero row beyond the
border still reflects until the face's click deletes the record, and
that click comes when the record's offer at the border reaches its
rung, up to the whole packet's length after its front arrives, so the
margin stands), stated once:
- The rows whose reading is a steady field at a receiver near a face
  (the two slits, the pace fans, M1 and the index rows' probe windows)
  need a margin of half the train's length behind every receiver, or a
  shorter train.
- The rows whose reading is a first rung (M2, Sagnac, the light clock)
  or a ratio of intervals (the redshift) are unmoved.
- The clock rows are on periodic boards and have no face.
- Bell and Malus read computed weights and are unmoved.
The World Generator applies the margin at regeneration; each regrown
world's pin is re-derived blind on its own map before any run.

---

## 0. (HISTORY) Each tool from the algebra: the operation, the body that carries it, what is written on the board, the load-time check (the owner's words of 2026-09-24, 19:10Z and 19:25Z, through the Boss)

THE DERIVATION NOW LIVES IN [ALGEBRA.md chapter 9](../../ALGEBRA.md) ("The
tools as operations of the group", the owner's word of 19:35Z): a tool is a
body at rest whose action is the equivariant map its stabiliser allows;
polar or not polar by its action on the hands; and what follows there,
not chosen: the crystal's mixed channels HV + VH with equal weights and
phase 0 (a theorem of the crystal's mirror), the hands' indices equal (no
birefringence: the cone from the families' dispersion), the Bell
experiment needing a crystal of one cell, the splitter a material layer.
This section is the summary table beside it; where they differ, chapter 9
holds. In particular chapter 9.7 replaces the crystal's start "at the
first rising zero after the Node's first rung" (1.1a item 2), a read of a
cell to decide, by THE CLICK, THEN A BIRTH (the bilinear coupling with a
seed weighed and rejected there): the crystal a receiver for the arriving
record and, on its click, an emitter of the pair, no cone (section 11); and 9.8 makes the
faces shells of receiver cubes, an experiment only cubes on a torus.

THE OWNER'S WORDS (translated): "all of it must follow from the algebra.
Do not assume from physics ... We have a receiver, an emitter, a
crystal, nothing else ... check whether it is a group or a subgroup,
like the body, or perhaps an action of the group"; "we reached the body
too through the algebra, how it must be written on the board ... the
algebra already derives what must be put there for the polariser, the
mirror, all these things; you can take them out". This section derives
every tool from [ALGEBRA.md](../../ALGEBRA.md) alone, in the body's own
form (8.3 and 8.7: a G_48-set of Nodes, the integers on it computed from
the algebra and checked at load). Each line is marked IN THE ALGEBRA
(with its section), DERIVED HERE (with the derivation) or MISSING (what
the algebra lacks). No physical assumption enters.

**0.1 The two conservation laws are the group law (DERIVED HERE from 1.1,
1.5, 1.6, 1.7 and 8.1).** A record is two samples of the real part of
one character of Z_N x (the time translation) x (the torus's
translations) (1.7; 8.1's plane waves): its CLOCK is the character of
the time translation (the energy, E = h s of 4.11) and its WAVE VECTOR
the character of the translations (the momentum, the label of 1.2's
dictionary). The characters of an abelian group form a group under the
pointwise product, chi_omega chi_omega' = chi_(omega + omega') and
chi_k chi_k' = chi_(k + k'): ENERGY ADDING AND MOMENTUM ADDING ARE THE
GROUP LAW OF THE DUAL GROUP, and on the phase circle the product of the
group ring, [p] [q] = [p + q] (1.1, 1.5), is the same law on Z_N. So a
map that sends one character to pairs of characters conserves energy
and momentum exactly when it lands on pairs whose product is the
arriving character; nothing physical is assumed.

**0.2 The one operation behind the crystal: the transpose of the ring's
product (DERIVED HERE).** The product m: Z[Z_N] (x) Z[Z_N] -> Z[Z_N],
[a] (x) [b] -> [a + b] (1.1), has the transpose m^T([p]) = SUM over a + b
= p of [a] (x) [b] for the inner product in which the [p] are
orthonormal. m^T is linear with a 0 / 1 integer matrix, the group's own
table read backwards (verb B, its matrix not declared but the group's),
and its image lies exactly on the pairs whose product is [p]: energy
conservation is m^T's support, not a check. The same transpose on the
translations' characters gives momentum. The consequences:
- m^T of one arriving clock is the sum of ALL its splits (a, p - a),
  equally weighted. A record on main carries ONE clock per family, so
  the born record takes one split: the born family's clock is the
  crystal's material, a declaration (MISSING: a record carrying the whole
  sum of splits; nature's broad spectrum of the pair is that sum).
- The degenerate split [p / 2] (x) [p / 2] exists on Z_N only for p even;
  on the circle of 2N it exists for every p (the doubling Z_N -> Z_2N, p
  -> 2 p; the half-angle tables of 2N, 3.6): EXACT (IN THE ALGEBRA, 3.6's
  tables).
- On the translations the transpose is realised by the drive: the born
  amplitudes at every crystal Node carry the arriving character's own
  phase there, halved (1.1a item 2), so the sum over the crystal's Nodes
  is m^T's momentum part; the arms' headings follow with nothing
  declared, given the born family's pace (1.1a item 3; DERIVED there).
- The pace per family is IN THE ALGEBRA: the index form for light, the
  pair on light's record at the cells with D_i >= 1 (8.3, "light cannot
  be a body"), D = n^2; the crystal carries no bound mode (PROVED in 8.3:
  the norm bound).
- The halving's start at each Node is an event of that Node's cell (the
  first rising zero after its first rung), no count kept: DERIVED HERE
  from 1.7's pair (the zero of a_now with a_before below it is a
  comparison, verb D).

**0.3 The table of the tools.**

| Tool | (1) The operation | (2) The body that carries it | (3) What is written on the board | (4) The load-time check |
| --- | --- | --- | --- | --- |
| The body | a G_48-set of Nodes with a lowered pair, its clock the bound mode (IN, 8.3) | a cube by its vertices, its stabiliser the cube's (IN, 8.3) | the pair and the seed, the bound mode's integer profile computed by the generator (IN, 8.7) | the body check: whole on the board, the profile bit for bit, the ramp at ten relaxation times (IN, 8.7; record 1817) |
| The emitter | a birth whose headings are the G_48-orbit of one Port: the 48 act transitively on the six Ports (1.1), so the orbit is all six and the source is isotropic; a direction can only come from the body's shape, a set of cells with a smaller stabiliser driven in phase (DERIVED HERE) | a cube by its vertices (isotropic); a beam is a line of cells, its stabiliser the line's | the clock pair (the time character), the amplitude, the train, the label state (IN, 1.7 and 4.11) | the train ends at the clock's zero (the quarter rule), exact; `arms` refused |
| The receiver | the evaluation of the record on its cells (E), the norm (B), the rung (D): the click (IN, 2.5 and 8.6); the TAKE is a declaration of the world, not an operation of the law (IN as a declaration, 8.6) | a cube by its vertices, no orientation | the take pair and the wheel W | W >= 1; the take pair [n, d] with 0 <= n <= d |
| The crystal | the transpose m^T of the ring's product on the clocks and on the translations (DERIVED, 0.2); in the blocks, a receiver and an emitter at the same Nodes (1.1a) | a cube (a square on a layer) by its vertices; its stabiliser about the arriving axis fixes the cone's symmetry | the born family's clock (one split of m^T), the born family's index pair D = [a^2 + 2 b^2] / [a^2 + b^2] for the cone's heading (a, b, 0) (DERIVED, 1.1a item 3), the coupling pair (the share taken), a Pythagorean pair | the born clocks' product equal to the arriving clock (the group law, an integer identity); the index's D - 1 equal to b^2 / (a^2 + b^2) exactly; the coupling pair Pythagorean |
| The mirror | a reflection of the det = -1 coset of G_48 (IN, 1.1) acting on the characters, k_perp -> -k_perp; REALISED by a gap: the band cos omega = (num / den) cos omega_l(k) (IN, 8.1) carries no clock with cos omega > num / den, so below the gap the amplitude decays inside and the reflection arises with the tangential character kept (DERIVED, 3.3) | a slab of cubes whose plane is the reflection's fixed set; its stabiliser the plane's | the gap pair [num, den], the depth D | every family clock that reaches it below its gap, C[k] > 256 num / den on the tables (an integer comparison); the depth such that the transmitted share is below the declared bound (computed, 3.3) |
| The splitter | the mirror's operation at a finite depth: the reflection sigma weighted by the layer's r and the identity by t; NOT a separate operation (DERIVED HERE: the same band, a thinner layer) | a one-Node layer of cubes; its plane | the gap pair of the share (computed, 7.2) | the share computed from the pair at the declared clock (7.2), printed at load as GAMEBOARD |
| The polariser | the rotation U_s on the label module Z^2 (IN, 3.6), then the receiver's take on one component: a receiver acting in the rotated label basis, NOT a separate operation (DERIVED HERE); U_s at a general s lies outside G_48 (the 48 give only quarter turns of the label plane about an axis) but inside the wheel's group: the relative translation x^s of the two hands, rows (x^0, x^(-s)) and (x^0, x^(N/2 - s)), no table (ALGEBRA.md 9.14) | a cube or a slab of cubes; the label plane is not a spatial direction, so the body's shape is free (its through-line the arriving path's) | the angle s and the take pairs, [1, 1] across the axis and [0, 1] along it | each row's norm 2 at every s, exactly (ALGEBRA.md 9.14) |

**0.4 What the owner's three blocks cover (DERIVED HERE).** The owner
names a receiver, an emitter and a crystal. With the body (8.3) as the
carrier of every material: the MIRROR and the SPLITTER are bodies whose
pair makes a gap (no new operation: the reflection arises); the
POLARISER is a receiver acting in the rotated label basis; the CRYSTAL is
a receiver and an emitter at the same Nodes joined by m^T; the
TRANSPONDER is a body carrying a mirror's gap on a moving body. So every
tool is a body carrying integers on which the law's four groups act (the
48, the phase circle, the translations, the time translation) through
the six verbs; NONE IS A NEW GROUP, a subgroup appears only as a body's
stabiliser (its shape), and the tools' operations are: the group law of
the dual group (the crystal), an element of the det = -1 coset (the
mirror, realised by a gap), the orbit of a Port (the emitter), the
evaluation (the receiver) and a declared rotation of the label module
(the polariser's angle, the one tool quantity outside the cells'
group).

**0.5 What is MISSING in the algebra, for the owner.** (1) A record
carrying the whole sum m^T([p]) (all the splits; one clock per family on
main). (2) The label module per amplitude: 3.6 carries the labels as
weights on the record, not as one amplitude per label value (the head's
enabling line). (3) The take is a declaration of the world, not an
operation (8.6 says so); the receiver's loss is therefore the one input
of the tools that the algebra does not produce. (4) The polariser's angle
at a general s is a declared rotation, not an element of the cells'
group.

---

## 1. (HISTORY) The crystal (it folds in the blind page docs/designs/detector_law/CRYSTAL_ALGEBRA.md, branch crystal-algebra at 238c7281, Reviewer 3's read CONFIRMED WITH LINES, record 1829)

**1.1 What it is and what nature gives it.** In the laboratory a
nonlinear crystal converts a small fraction of an arriving photon's
amplitude into a pair whose energies and momenta sum to the arriving
one's; the pair's directions arise from the conversion itself, never
pushed afterwards; the crystal's pace depends on the polarisation and
on the frequency (birefringence and dispersion), which is what lets the
directions lie off the arriving axis. For Bell's experiment the
laboratory uses one crystal of type II (the pair HV or VH) or two thin
crystals of type I with their axes crossed (the pair HH from one, VV
from the other; Kwiat and others, 1999). The owner's decisions: the
crystal and Bell are one experiment (record 1817); the double emitter is
cancelled (1818); the entanglement arises from two indistinguishable
conversion channels whose amplitudes add in one record of rank 2 (1821);
the crystal is birefringent (1829); the split is the board's own (1831).

**1.1a THE FORM THIS FILE NOW RECOMMENDS: THE RECEIVER-EMITTER CRYSTAL
(the owner's "think of a beautiful solution for the crystal that
works", through the Boss, 18:30Z; the Boss's proposal computed and
broken where it breaks). Sections 1.2 to 1.10 below are the alternative
(B), two crossed crystals, kept as computed.**

1. THE BODY AND ITS KIND. One body of light's kind declared by its
   vertex and edge, a square of side L on a layer (a cube on a board),
   each of its Nodes its own cell; A MATERIAL, NO BOUND MODE; `seed` 0.
   Its ORIENTATION: none beyond its cells; its dispersion is its one
   declared property about pace: ONE COEFFICIENT PAIR PER FAMILY at its
   cells, [1, 1] for the arriving record's family and [num, den] = 1 /
   n_b^2 for the born pair's family (on main the pace is already held per
   family per Node, `kind_num` and `kind_den`; a body writes only its own
   family's arrays today, so the extension is a body carrying a pair for
   each of two families). Two families of light's kind: the emitter's,
   at [2464, 25], and the pair's, at [1232, 25], summing to it; the
   polarisers and the receivers read the pair's family.
2. ITS ACTION (the receiver's form, then the emitter's, at the same
   Node; the fraction is the body's COUPLING PAIR between the arriving
   family and the born family, a material integer, no table). At each of its Nodes it TAKES the declared fraction of the
   arriving record's amplitude (booked on no pointer: the taken part is
   the pair's, one quantum, one click) and with it DRIVES the pair's
   record at that Node, with no heading. THE PHASE HALVED: the pair's
   drive at a Node starts at the first rising zero of the arriving
   amplitude after the Node's first rung, on the pair's own clock, so its
   phase is half the arriving phase there without a sign ambiguity (the
   start is an event of that Node's cell; the halving is exact on the
   circle of 2N steps). BOTH CHANNELS (H on the first arm and V on the
   second; V on the first and H on the second) are driven at the same
   Nodes, with the same phase and the same index: the record is born
   with the branches [[1, 1], [2, 1]] directly (verb G at the birth), its
   relative phase 0 EXACTLY (PROVED HERE: the two channels' drives are one
   drive), and ONE FIELD of amplitudes per label serves both arms (the
   head's one amplitude per label on every record) (the arms differ
   only by the body each is gathered at, as on main).
3. WHAT ARISES (PROVED HERE in the continuum; COMPUTATION on the board's
   own dispersion). The drive's phase along the crystal is the arriving
   record's own, halved, so the born amplitudes of all the crystal's
   Nodes add in phase only where the pair's wave vector (Outside
   reading) has the component k_p / 2 along the axis: inside cos
   theta_in = n_a / n_b, outside sin theta_out = sqrt(n_b^2 - n_a^2) with
   n_a = 1 (the cone, an Outside reading). No gradient is declared. For an
   integer heading (a, b, 0) the exact continuum pair is [num, den] = [a^2
   + b^2, a^2 + 2 b^2]: [2, 3] for (1, 1, 0), [5, 6] for (2, 1, 0), [5, 9]
   for (1, 2, 0). On the board at [2464, 25] with [2, 3]: the cone at
   44.321 degrees; the collinear heading leaves the main lobe from L =
   109 and the neighbouring integer headings from L = 178; the half-power
   band 32.2 to 55.1 degrees at L = 109, 37.2 to 51.0 at L = 178, 0.1 to
   88.9 (no cone) at L = 12 and 24; the lobe read in the far field, 2 A^2
   / (23.95 Links) with A = sqrt 2 L: about 1984 Links at L = 109 and
   5292 at L = 178. At the doubled clock ([4928, 25], the pair at about
   12 Links) the cone sits at 41.94 degrees (the board's own anisotropy),
   the collinear heading leaves from L = 58 and the neighbours from L =
   103, the far field about 1130 and 3565 Links. THE PRICE: a formed cone
   needs a crystal of about 60 to 180 Nodes and a board of a few thousand
   Links on a side; the Bell pin does not need it (item 6).
4. THE ENTANGLEMENT AND THE ANALOGY. Both channels see the SAME born index,
   so their cones coincide everywhere and the channels' amplitudes add on
   the whole cone: HV + VH on every direction of it, with no amplitude per
   label needed for the entanglement itself (the head's amplitudes per label
   serve the polarisers) (the Boss's point 5 CONFIRMED). BIREFRINGENCE AMONG THE BORN
   LABELS WOULD BREAK IT (PROVED HERE): with n_H different from n_V the H
   arms' cone and the V arms' cone on a layer are two different pairs of
   headings (+-theta_H, +-theta_V) with no heading in common, so no
   direction carries both channels and the state is a mixture of products
   (abs(S) <= 2). The pace difference that makes the cone is the
   dispersion between the arriving family and the born one, not a
   birefringence. THE ANALOGY: the geometry is that of the source of Kwiat
   and others, 1999 (two cones made to coincide, entangled everywhere on
   them); the labels HV + VH are those of the type II source of 1995,
   where the two cones differ and the entanglement lives only at their
   two crossings. So the analogy holds for the geometry, not for the
   crystal's physics: in nature the coincidence of the two cones is bought
   by two crystals of type I (HH + VV), which this body gives by one
   variant, the conversion entries V to HH and H to VV at the same born
   index with the arriving record polarised at 45 degrees (the state HH +
   VV, the cancelled worlds' pin with the old roles).
5. THE ARMS AND THE GATHER (PROVED HERE). One field serves both arms, so
   each arm reaches each receiver with the same offer. (i) The state HV +
   VH is symmetric under exchanging the arms (the labels 1 and 2 swap and
   carry equal weights), so the joint weights R = J^2 do not depend on
   which arm is gathered at which body; the same holds for every state,
   since exchanging the arms changes J by at most a sign. CONFIRMED. (ii)
   On main the joint gather binds one table body to each arm and gathers
   once over the product of the two bodies' channels: every gathered pair
   is a coincidence at the two different bodies. (iii) If instead the
   gather chose each arm's receiver by its offer, freely, then with two
   receivers of equal offers the two clicks would land at two different
   receivers with the chance 1 / 2 and at the same receiver with 1 / 2 (2
   p_A p_B / (p_A + p_B)^2 = 1 / 2 at p_A = p_B); the correlation
   conditioned on two different receivers is the state's, the same weights
   R, so S is unchanged.
6. WHAT IT DOES NOT CARRY (the Boss's point 7). The pair's opposite
   transverse directions: each arm alone forms the whole cone (on a layer,
   both headings +theta and -theta); the two arms are not tied to opposite
   sides. The cost: under a free gather half the pairs land at one
   receiver (the coincidence share 1 / 2 on a layer, less in three
   dimensions, the share of the cone a receiver subtends); it does not
   change S (5 (iii)). The pairing as a law of the click (optional, for
   the owner): main's joint gather already binds each arm to one body,
   which IS the pairing; stated as a law, "the two clicks of a pair are
   at two cells mirror images through the crystal's axis" is a
   permutation of cells by the body's own mirror (verb P) inside the
   gather: generic (the crystal's own symmetry, no name), vector (P, then
   the ladder's D), and not local, as the gather is not: it adds nothing
   to the law's one declared non-local step (POSTULATES.md section 10).
7. THE NUMBERS FOR THE BELL WORLD (the cone not formed, item 3). The
   pair family at [1232, 25], the crystal a square of side 4 with the
   coefficient [2, 3] for the pair's family (the cone's pair, harmless on a
   short crystal), the per-Node fraction a Pythagorean pair of size about
   1 / 4 ([7, 25], the passing numerator 24), the bodies at 45 degrees
   (their placement the experimenter's), the smallest layer about 32 x 33
   (the page of the branch crystal-algebra, 3.6, with the crystal's side
   added). THE TIMING: the arriving train 3200 intervals; the first birth
   at the crystal's first Node t_e + L0 / c plus at most one arriving
   period (20.8 intervals) for the rising zero after the first rung
   (bound t_e + L0); each arm's first rung at its body t_birth + d / c (K
   form; bound the Manhattan distance); THE MIRROR THEOREM HOLDS: one
   field, a symmetric crystal, board and bodies, so the two bodies' first
   rungs and completions are equal EXACTLY at every setting (the crystal
   page 3.4); the gather at the common completion, after the train and
   the flight. THE PIN, declared blind: the state HV + VH, so at the
   cancelled worlds' settings a in {0, 512}, b in {256, 768} the counts are
   the cancelled counts with Bob's two settings exchanged ((0, 256): 150,
   874, 874, 150; the other three 874, 150, 150, 874), S = E(0, 768) - E(0,
   256) + E(512, 768) + E(512, 256) = 181 / 64 EXACTLY under the crystal's
   own count as the pair's wheel (the crystal page 4.5), and 0 in the
   cancelled roles. The variant HH + VV (item 4) keeps the old roles.
8. THE ENGINE LINES: (i) a body carrying a coefficient pair for each of
   two families (generic: the pair chosen by the record's family, as
   today; vector: T and D as today; local); (ii) the take-and-drive at
   each crystal Node, fired at the rising zero after the Node's first
   rung (generic: a declared conversion entry; vector: B the linear form,
   D the division with the remainder kept, E the clock's table; local:
   the Node's own amplitudes and the arriving record's own pair; no birth
   fires on an arrival on main); (iii) a record of rank 2 with ONE field
   for both arms (the gather's offers at the two bodies read on the same
   field); (iv) the pair's residue from the crystal's own count. Cost:
   one field per pair, one linear form per crystal Node per interval.
9. THE UNIT TESTS: (a) one channel only (the branches [[2, 1]]): at (0,
   0) 0, 2048, 0, 0; at (512, 512) 512 in each cell; (b) both channels:
   at (0, 0) 0, 1024, 1024, 0; at (512, 512) 1024, 0, 0, 1024 (the
   entanglement test against (a)'s 512 each); (c) the born family's pace
   in the crystal c / n_b (a slab test as 1.9 test 1, the family in place
   of the label); (d) the same counts with the two bodies' arms exchanged
   (5 (i)); (e) the refusals: the pair's clocks not summing to the
   arriving clock, a non-Pythagorean fraction, a pair num > den; (f) the
   cone (a large board, L = 109, GAMEBOARD by declaration): the peak at
   44.3 degrees, the half-power band 32.2 to 55.1 degrees.

10. THE COUPLING WITHOUT A DECLARED HALVING (for the owner and the
   physicist; not this file's recommendation). The engine's coupling
   between records at a body's cells (the massive coupling, ALGEBRA.md
   8.5) is linear in the arriving amplitude, and a linear coupling
   invariant in time keeps the clock (the crystal page 3.2): it cannot
   make [1232, 25] from [2464, 25]. The coupling that makes the halved
   clock ARISE is BILINEAR, the born family's source g a_arriving
   a_born at each crystal Node (verb B, a rate bilinear in the state,
   within the vector test): the product's difference frequency is
   resonant at half the arriving clock, the parametric resonance of
   nature's down-conversion. Its conditions, PROVED HERE: (i) from a born
   amplitude of 0 it makes nothing (the product is 0), so the born family
   needs a SEED on the crystal's cells (the body's `seed`, the stand-in
   of nature's vacuum); (ii) the born amplitude then grows as sinh(g A t),
   A the arriving amplitude, so the converted share is set by g, the seed
   and the length, not by a declared fraction; (iii) the arriving record
   must lose what the born one gains (a back-coupling -g a_born^2 on it),
   and the conserved form of the coupled scheme with that cubic term is
   still to be written. Item 2's take-and-drive (the start at the rising
   zero) is its first-order form with the seed and the gain folded into
   the one coupling pair.

**1.2 The answer to the owner's question of record 1831 ("the medium
alone causes this ... confirm whether I am right") (PROVED HERE).**

- RIGHT for the pace and the spreading: every record's amplitudes spread
  from Node to Node by the split, and a medium sets the pace per Node by
  its coefficient (DESIGN.md 4.1); a crystal of one index needs nothing
  new.
- RIGHT for the directions in the TYPE I form. Let the pair be born at
  every crystal Node with each arm's clock started so that its phase is
  HALF the arriving record's phase there (the arms' clocks summing to the
  arriving clock and nothing else declared). The arms' amplitudes born
  along the arriving axis then carry the phase step k_p / 2 per Link, and
  the split adds them constructively only in the headings where each
  arm's own wave vector (Outside reading) has the component k_p / 2 along
  the axis. For two arms of one label, at the index n_s in a crystal
  where the arriving record sees n_p < n_s, those headings are cos
  theta_in = n_p / n_s inside, at +theta and -theta, mirror images: the
  cone (Outside reading) arises from the medium alone.
- NOT for the TYPE II form with mirror arms and an index per label only:
  the H arm's heading would be sin theta_out = sqrt(n_H^2 - n_p^2) and
  the V arm's sqrt(n_V^2 - n_p^2) outside (continuum form, exit face
  normal to the arriving axis); the arriving record carries H or V, so
  n_p is n_H or n_V and that label's arm is collinear; mirror arms would
  need n_H = n_V, which is no birefringence. The page on the branch
  crystal-algebra reached type II only by DECLARING each arm's source
  phase across the crystal's cells (its section 8.2), which record 1830
  forbids.

THE ALTERNATIVE (B), superseded by 1.1a as this file's recommendation (its
sentences on one amplitude per record predate the head's no-table rule, which
puts one amplitude per label on every record): TWO CROSSED CRYSTALS OF TYPE I, the
laboratory's second form. It differs from record 1821's channels (H on
the first arm and V on the second, and the swap), which are type II: A
POINT FOR THE OWNER through the Boss. What the two forms share is the
owner's principle: two indistinguishable conversion channels whose
amplitudes add in one record. Here the channels are V to HH (the first
crystal) and H to VV (the second); their sum is HH + VV, EXACTLY the
state the cancelled emitter declared, so the Bell pin of the cancelled
worlds stands with its roles unchanged (1.6).

**1.3 Its body, its kind, its orientation.**

- THE BODY: each crystal a square of side L on a layer (a cube of side L
  on a board), declared by its lower vertex and its edge; the two
  crystals adjacent along the arriving axis, the first at [x_1, x_1 +
  L), the second at [x_1 + L, x_1 + 2 L).
- THE KIND: light's kind, `seed` 0 (no record of its own), no coupling:
  A MATERIAL, NO BOUND MODE. The algebra's condition on it: every index
  pair has num <= den (no label faster than the vacuum), so its
  coefficient form is stable on the board (DESIGN.md 4.1; the conserved
  form carries the index squared on the motion term).
- THE ORIENTATION, the one thing a crystal declares about direction: its
  INDEX TABLE, one coefficient pair [num, den] = 1 / n^2 per LABEL VALUE
  AND PER CLOCK (the index squared, so an irrational index is an exact
  pair). The first crystal: at the halved clock [1232, 25], H [2, 3]
  (n^2 = 3 / 2) and V [1, 1]; at the arriving clock [2464, 25], H and V
  both [1, 1]. The second crystal is the first rotated by 90 degrees: at
  [1232, 25], V [2, 3] and H [1, 1]; at [2464, 25] both [1, 1]. Nothing
  declares a heading. The table per clock is the crystal's dispersion,
  a property nature gives it; it is what lets the arriving record, of
  label state H + V, cross both crystals at one pace (1.7, Nature24's
  point (a)).
- ITS CONVERSION ENTRY: the arriving label that converts (V in the first
  crystal, H in the second), the pair's joint label (0 = HH from the
  first, 3 = VV from the second), the arms' clocks ([1232, 25] each,
  summing to [2464, 25], refused at load otherwise), and the per-Node
  fraction [n, d] of the arriving amplitude with the passing amplitude m
  / d, n^2 + m^2 = d^2 (a Pythagorean triple, checked at load as the
  splitter's isometry is).

**1.4 Its action on every input (the continuum statements PROVED HERE;
the lattice numbers COMPUTATION on the Outside reading).**

- The arriving record (label state H + V, clock [2464, 25]) crosses both
  crystals at the vacuum's pace ([1, 1] at its clock for both labels):
  one amplitude per Node, as on main.
- In the first crystal, at every Node the arriving record reaches, the
  converting label's share (V) is converted: the pair's record of the
  channel V to HH is born there with the fraction n / d of the local
  amplitude and each arm's clock started at the arriving amplitude's
  rising zero at that Node (so the half phase is taken without a sign
  ambiguity); the arriving record keeps m / d there. The H share passes
  unconverted. In the second crystal likewise for H to VV.
- Each channel's record is born with ONE label per arm (H, H or V, V),
  so it moves at one pace in every crystal Node it crosses (the HH
  record at [2, 3] in the first crystal and [1, 1] in the second; the VV
  record at [2, 3] in the second): one amplitude per Node per record.
- THE ADDITION (verb G): the two channels' records are born of ONE
  arriving quantum (one birth stamp, one residue); at the second
  crystal's exit face, where the medium is label-blind again, they are
  added into ONE record of rank 2 with the branches [[0, 1], [3, 1]] and
  its arms' amplitudes the sums of the two channels' amplitudes per Node
  (Nature24's point (a): no record inside a crystal ever holds two
  paces).
- THE HEADINGS (Outside reading): each channel's arms leave where k_x =
  k_p / 2; inside cos theta_in = n_p / n_s, outside sin theta_out =
  sqrt(n_s^2 - n_p^2); at n_p = 1 and n_s^2 = 3 / 2 the continuum gives
  45 degrees outside EXACTLY (35.26 degrees inside). On the board's own
  dispersion (the arms at [1232, 25], a layer) the match is at 44.321
  degrees outside, 35.226 inside. The second crystal's VV arms match at
  the same angle by the swap of its table (PROVED HERE: the same equation
  with the labels exchanged): HH and VV leave on the same two headings.
- THE LOBE (COMPUTATION, one arm, the sum of L Nodes' contributions): the
  mismatch per Link -0.0579 at the collinear heading, -0.0354 at (2, 1,
  0), +0.0016 at (1, 1, 0) and +0.0445 at (1, 2, 0). The collinear
  heading leaves the main lobe from L = 109 (2 pi / 0.0579); (2, 1, 0)
  and (1, 2, 0) too from L = 178; 45 degrees stays in it up to L = 2021.
  The half-power band: 0.1 to 88.9 degrees at L = 24 (no selection), 0.1
  to 70.0 at L = 48, 30.4 to 56.6 at L = 96. The width scales as the
  arms' period in Links over L; the lobe is read in the far field, at
  about 2 A^2 / (24 Links) with A = (L + W) / sqrt 2 (about 5300 Links
  at L = W = 178), a HOST cost.
- THE PIN DOES NOT NEED THE SELECTION: the counts come from the joint
  gather's weights (1.6); a short crystal adds the Nodes' contributions
  broadly, its lobe still peaked at 44.3 degrees. The Bell world may take
  L = 24; the lobe's width is the crystal's own unit test on a large
  board (1.9, test 5).
- THE SIDE FACES (PROVED HERE in the continuum; 0.26237 per Link both on
  the board at 45 degrees): at the match an arm's k along the axis
  inside equals the vacuum's whole k (n_s^2 - sin^2 theta_out = n_p^2 =
  1), so an arm's amplitude that reaches a face parallel to the axis
  leaves it grazing: a loss to the sinks, never a wrong heading.
- THE NORM: the Nodes' contributions add coherently in the lobe, so the
  per-Node fraction is at most about 1 / L on it; the Pythagorean pairs
  of that size are (2 j + 1, 2 j (j + 1), 2 j (j + 1) + 1), n / d about 1
  / j (at L = 24: [49, 1201], the passing numerator 1200).
- Every Port of a crystal Node reads the split as every Node does; the
  crystal takes nothing (it is no receiver) and books nothing but the
  births.

**1.5 One quantum, one click, one residue (PROVED HERE).** The arriving
record's quantum ends in one click: the pair and the passing part are
outcomes of ONE record's quantum with one residue u and one gather;
separate quanta would click twice. The pair's residue: the crystal's own
count of its conversions on its own wheel of W (the crystal's count, a
clock block), which makes the counts exact for every fraction (the
crystal page's 4.5). The residue order: "seed" (Nature24's point 6: the
counts depend on the multiset of residues alone, and the seeded order
closes the order channel, ORDER_CHANNEL_ATTACKS.md), declared at the
crystal.

**1.6 The state and the pin (COMPUTATION on main's tables and rung;
exact integers).** The pair's branches [[0, 1], [3, 1]], HH + VV with
equal weights, the relative phase set by the geometry and NOT READ by
the joint gather, which reads the integer label weights (a stated
departure from nature, where a relative phase other than 0 lowers S).
The counts at the cancelled worlds' four settings pairs, W = 2048, one
gathered pair per residue of the crystal's wheel:

| (a, b) | ++, +-, -+, -- | E |
| --- | --- | --- |
| (0, 256) | 874, 150, 150, 874 | +181 / 256 |
| (0, 768) | 150, 874, 874, 150 | -181 / 256 |
| (512, 256) | 874, 150, 150, 874 | +181 / 256 |
| (512, 768) | 874, 150, 150, 874 | +181 / 256 |

S = E(0, 256) - E(0, 768) + E(512, 256) + E(512, 768) = 181 / 64 =
2.828125 EXACTLY, the cancelled worlds' pin with their roles unchanged;
the marginals 1024 of 2048. THE PIN'S FORM, DECLARED HERE BEFORE ANY RUN
(Reviewer 3's line): the four worlds a in {0, 512}, b in {256, 768}; S
as written; the pair's residue the crystal's own count; any count other
than the table's an engine defect to name.

**1.7 The engine lines (each new; the physicist writes them after this
section is agreed).**

1. THE INDEX PER LABEL AND PER CLOCK. Inside a crystal's cells a
   record's amplitudes step by the coefficient form of DESIGN.md 4.1
   with the pair its table gives for the record's clock and label:
   3 den a_next + r' = num S_6 + 6 (den - num) a_now - 3 den a_before + r,
   0 <= r' < 3 den. A record whose labels have different pairs at a
   crystal Node is REFUSED there (the design never sends one: 1.4), so
   one amplitude per Node per record stays the engine's form. Generic
   (the pair chosen from the body's declared table by the record's clock
   and label bit, no family name); vector (T with the pair, D by the wall
   3 den); local (the record's own six reads).
2. THE CONVERSION AT EVERY NODE, FIRED BY ARRIVAL. At a crystal Node,
   from the first interval the arriving record's amplitude there rises
   through zero after its first rung at that Node, the Node drives the
   channel record's two arms with the fraction n / d of the arriving
   amplitude (the linear form of DECLARATIONS.md section 14 reading the
   arriving pair (a_before, a_now)) on the arms' clock started at that
   interval, and the arriving record keeps m / d there. No birth fires on
   an arrival on main (Nature24's point 4): this is new, with its test.
   Generic (a declared conversion entry, no family name); vector (B the
   linear form, D the division by d with the remainder kept, E the
   clock's table); local (the Node's own amplitudes and the arriving
   record's own pair).
3. THE ADDITION AT THE EXIT FACE. Two records of one birth whose arms
   carry different labels are summed into one record of rank 2 once both
   have left the crystals' cells: the branches' union with their weights
   (verb G) and the arms' amplitudes added per Node. Generic (by the
   birth stamp and the arms, no name); vector (G); local (per Node, the
   two records' own amplitudes). Until the addition the two records
   share the residue and the one gather (as the arms of a pair do on
   main, `_click_pair`).
4. THE PAIR'S RESIDUE: the crystal's own count of its conversions, one
   per converted quantum, on a wheel of W, the residue order declared at
   the crystal.

**1.8 The timing (the formulas; the absolute first-rung intervals
MEASURED ONLY).** An emitter at L0 Links before the first crystal along
the axis; the bodies' entry Nodes at L1 steps along (1, +-1, 0) beyond
the second crystal.

- The arriving train is 3200 intervals (the declared 128 periods become
  154 by the quarter-zero rule; 3200 is also 77 periods of the halved
  clock, a common zero; the crystal page 3.1).
- The first crystal converts from t_e + L0 / c (bound t_e + L0), each
  Node at depth x at t_e + (L0 + x) / c; the second from t_e + (L0 + L) /
  c (the arriving record at the vacuum's pace in both).
- THE TWO CHANNELS' LAG (Nature24's point (b); PROVED HERE in the
  continuum, where the pace in a medium is the same for the phase and the
  envelope): within one crystal the matched headings make every Node's
  contribution reach a far line across the heading at one time; the
  channels differ by the second crystal's offset along the axis seen
  along the heading, so the VV record reaches the far line L (1 - cos
  theta_out) / c after the HH record: 12.2 intervals at L = 24, 6.1 at L
  = 12, 24.4 at L = 48. THE CONDITION OF THE ADDITION: this lag well below
  the train's length (3200 intervals), where the two alternatives are
  indistinguishable in time; nature's crystals need a compensating plate
  when their lag exceeds the coherence time; here L up to a few hundred
  Nodes keeps the lag below 5 percent of the train.
- Each arm's first rung at its body: after t_e + L0 / c + (the path to
  the body) / c (K form), the bound the Manhattan distance; the group
  pace outside c (1 + k^2 (1 - 3 A) / 24) with A the sum of the heading's
  components to the fourth power (the crystal page 3.3).
- THE MIRROR THEOREM HOLDS (PROVED HERE, the crystal page's 3.4 per
  channel record): the crystals, the board and the bodies symmetric about
  the arriving axis, each channel's two arms of one label and one clock,
  so at every interval arm 1's amplitudes are the mirror image of arm
  0's; the two arms' first rungs and completions are equal EXACTLY at
  every setting; the gather's stamp is that common interval.

**1.9 The unit tests, each on a small world that is none of the
fifteen, with their exact expected values.**

1. THE INDEX PER LABEL AND CLOCK (a chain; a slab of side 60 whose table
   gives H at [1232, 25] the pair [2, 3]): an emitter of label H at
   [1232, 25] crosses it in 60 sqrt(3 / 2) / v_g intervals against 60 /
   v_g for label V or for H at [2464, 25] (the K form's difference 60
   (sqrt(3 / 2) - 1) / c = 23.4 intervals; the first rungs beyond the
   slab MEASURED ONLY); a record of labels with different pairs refused.
2. ONE CRYSTAL, ARRIVING V (the first crystal alone): the branches [[0,
   1]] (HH), a product; the joint counts at (0, 0): 2048, 0, 0, 0; at
   (512, 512): 512, 512, 512, 512; at (0, 512): 1024, 1024, 0, 0; at (0,
   256): 1749, 299, 0, 0.
3. ONE CRYSTAL, ARRIVING H (the first crystal): nothing converted; the
   record passes whole at the vacuum's pace; no pair, no gather.
4. TWO CROSSED CRYSTALS, ARRIVING H + V: the branches [[0, 1], [3, 1]]
   after the exit face; at (0, 0): 1024, 0, 0, 1024; at (512, 512): 1024,
   0, 0, 1024 (the entanglement test: the product of test 2 gives 512 in
   each cell there); at (0, 512): 512, 512, 512, 512; the Bell table of
   1.6.
5. THE LOBE (a large layer, L = 96, receivers on a ring in the far field,
   GAMEBOARD by declaration): the arms' offer peaked at 44.3 degrees, the
   half-power band 30.4 to 56.6 degrees.
6. THE REFUSALS at load: arms' clocks not summing to the arriving clock;
   a conversion fraction that is not a Pythagorean pair; an index pair
   with num > den.
7. THE MIRROR THEOREM (a symmetric placement, two settings pairs): the
   two arms' first-rung intervals equal, and equal across the settings.
8. THE LAG: the VV record's first rung at a far receiver across the
   heading later than the HH record's by L (1 - cos theta_out) / c in the
   K form (12.2 at L = 24; MEASURED ONLY within the rung's grain).

**1.10 Cost.** Per crystal Node per interval, one linear form and one
division per converting record; two channel records per converted
quantum until the exit face (twice the rows there); the far-field lobe
test's board (5300 Links at L = 178) the one large HOST cost; the Bell
world itself stays small (L = 24).

---

## 2. (HISTORY) The polariser (a material: it takes one label along its own axis; the counts arise from the record's label state projected on that axis)

**2.1 What it is.** In the laboratory an absorbing polariser (a sheet)
takes the polarisation across its axis and passes the one along it; a
polarising beam splitter reflects the one and passes the other to two
detectors. The former table form (a body of two cells splitting a booked
offer by declared weights; [the Malus note](../malus/NOTE.md),
DECLARATIONS.md section 14) RETIRES.

**2.2 Its body, its kind, its orientation.** A body declared by its
vertex and edge (the smallest of side 1; a line of such cubes across a
beam), of light's kind, A MATERIAL, NO BOUND MODE. Its ORIENTATION,
declared by itself: its AXIS, the angle pi s / N on the half-angle tables
of 2N (the setting s, the key `axis` in place of `phase_window`). Its
MATERIAL, in its own rotated label basis (the component along the axis
a_par = (C'[s] a_H + S'[s] a_V) / 256 and the one across it a_perp =
(-S'[s] a_H + C'[s] a_V) / 256, each division with its remainder kept):
- THE ABSORBING FORM: along the axis the index pair [1, 1] and the take
  pair [0, 1] (it passes); across it the take pair [1, 1] (it takes and
  books); a plain receiver beyond it books what passes. The two cells of
  the click are the polariser's own (the - cell) and the receiver beyond
  (the + cell): no exit cell is declared from any arm.
- THE SPLITTING FORM (a polarising splitter layer, one Node thick):
  across the axis a gap pair (the mirror's [1, 2], section 3), along it
  [1, 1]: the across part is reflected and the along part passes, each to
  its own receiver; the two counts arise at the two receivers.
The algebra's one condition, true of the tables: **U**_s^T **U**_s = n_s
**I** exactly, so the rotation keeps the record's norm up to the factor n_s
/ 65536 on both parts alike (ALGEBRA.md 3.6).

**2.2a The axis as an element of the wheel's group (ALGEBRA.md 9.14,
replacing the half-angle form above).** In the hands basis, with
`label_hands` declared, the axis s is the relative translation x^s of the
two hands. Along the axis a_pass = a_+ + x^(-s) a_-, and across it a_block
= a_+ + x^(N/2 - s) a_-: a translation and a sum on the ring, with no
division and no remainder. Both rows have the norm 2, and the common
factor drops out of the ladder. The weights are real elements of
Z[zeta_N], and the rung compares them exactly by the sign recursion of ALGEBRA.md
9.14. The pins do not move (Bell 874/150/150/874 with S = 181 / 64;
Malus 128, 246, 199, 177). In 2.3 below read C' and S' as these rows.

**2.3 Its action (PROVED HERE).** A record of one arm whose label state
is SUM over l of w_l (l) has the amplitudes per label a_l = w_l a (one
field a, born by the emitter, times the label's weight), so along the
axis a_par = (C' w_H + S' w_V) a / 256 and across it a_perp = (-S' w_H +
C' w_V) a / 256: the two parts' booked motions stand in the ratio R(+) :
R(-) = (C' w_H + S' w_V)^2 : (-S' w_H + C' w_V)^2, THE PROJECTION OF THE
RECORD'S LABEL STATE ON THE MATERIAL'S AXIS, exactly the weights of the
joint gather's primitive with one body. The click's weights are these
(computed from the record's label state and the body's axis, as the
gather computes them), and the board's books must agree with them within
the rung's margin (2.6): a consistency test of the material, not a
second source of the counts. For a record of rank 2 each arm's
polariser rotates that arm's amplitudes per label (the timing and the
books) and the joint gather computes R = J^2 from the record's joint
label state and the two bodies' axes (ALGEBRA.md 3.6), unchanged.

**2.4 Timing (PROVED HERE).** The first rung of the click is the first
interval at which the record's offer booked at the two cells together
times W reaches the norm; the rotation redistributes the offer between
the two parts, the parts' amplitudes step by the same pair [1, 1] up to
the polariser, and the receiver beyond sits one Link further: in the
absorbing form the + cell's first rung lags the - cell's by the one Link
(a K form of 1 / c = 1.73 intervals, MEASURED ONLY); the joint click's
stamp is the later arm's first rung at its body's two cells, the same at
every setting.

**2.5 The engine lines.** (1) One amplitude per label on every record
(the head); (2) the rotation of a record's label amplitudes by a body's
axis at its cells and the per-part pairs (verb B, the 2 x 2; generic:
the body's declared angle and pairs, no name; vector: B, then T and D
per part; local: the Node's own amplitudes); (3) the click's weights
from the record's label state and the body's axis (the gather's
primitive with one body, as on Nature24's branch polariser-fix, point 5
of his notes). RETIRES: `TableBody` and its split of a booked offer.

**2.6 The unit tests (COMPUTATION on main's tables and rung).**

| The record, W = 2048 | s = 0 | s = 256 | s = 512 | s = 768 | s = 1024 |
| --- | --- | --- | --- | --- | --- |
| label H, [[0, 1]] | 2048, 0 | 1749, 299 | 1024, 1024 | 299, 1749 | 0, 2048 |
| label V, [[1, 1]] | 0, 2048 | 299, 1749 | 1024, 1024 | 1749, 299 | 2048, 0 |
| 45 degrees, H + V, [[0, 1], [1, 1]] | 1024, 1024 | 1747, 301 | 2048, 0 | 1747, 301 | 1024, 1024 |

(+, - counts over one wheel of births). MALUS'S FOUR WORLDS under the
material form (label H, N = 256, W = 256): 128, 246, 199, 177 at s = 64,
16, 40, 48, UNCHANGED (the weights (32761, 32761), (63001, 2500), (51076,
14641), (45369, 20164)); their rung margins 0.500, 0.271, 0.466 and 0.269
of a count, so the material's books must agree with the projection to
about 1 part in 1000 of the norm for the board's own offers to give the
same counts. BELL'S FOUR SETTINGS: 874, 150, 150, 874 per settings pair,
UNCHANGED (the gather's weights); the margins 0.0218 of a count at (0,
256) and (0, 768), 0.0986 at the other two: a book-based count would
need agreement to about 1 part in 100000. The pins are re-derived before
any run on the owner's word; under this form none moves. The books test:
the - cell's booked motion over the + cell's equal to R(-) / R(+) within
the margins above (MEASURED ONLY). The axis test: the counts at the same
setting with the body's line turned by 90 degrees on the layer
unchanged (no exit cell from any arm).

---

## 3. (HISTORY) The material mirror (a gap block of light's kind; the reflection arises)

**3.1 What it is.** A mirror reflects because the light cannot proceed
inside it; nothing tells it the outgoing direction. Here: a body of
light's kind whose pair [num, den] on the six-neighbour term opens a gap
(cos omega_0 = num / den, ALGEBRA.md 8.1): below omega_0 the split
carries no amplitude through it, and the reflection arises by the rule.
The mirror line is this (DECLARATIONS.md section 15 item L-1, the pair
[1, 2], omega_0 = pi / 3 = 1.047 per interval). It replaces the board's
closed face in the light clock (record 1822) and the one-Node mirror
that re-emitted in a declared direction (record 1830).

**3.2 Its body, its kind, its orientation.** A cube of side D (its depth)
by its vertex, or a line of such cubes; light's kind with the pair [1,
2]; a MATERIAL, NO BOUND MODE (a gap lowers the pair, and for light's
kind below the gap the Node's amplitudes decay inside, PROVED on the
band's Outside reading, ALGEBRA.md 8.1); not `absorbing`; the face
behind it open. Its orientation: its cells' own plane; nothing else.

**3.3 Its action (COMPUTATION: the exact harmonic solution of the split
on a chain, in complex floating point; no rule stepped).** Off the pair
[1, 2], the reflected energy share abs(r)^2 and the transmitted
abs(t)^2 (their sum 1 to the printed digits):

| Depth D | [2464, 25]: abs(r)^2; abs(t)^2 | [1232, 25]: abs(r)^2; abs(t)^2 |
| --- | --- | --- |
| 1 | 0.969997; 3.000 x 10^-2 | 0.992410; 7.590 x 10^-3 |
| 2 | 0.999444; 5.561 x 10^-4 | 0.999876; 1.237 x 10^-4 |
| 3 | 0.999990; 1.038 x 10^-5 | 0.999998; 2.067 x 10^-6 |
| 4 | 1 - 2 x 10^-7; 1.938 x 10^-7 | 1 - 3 x 10^-8; 3.456 x 10^-8 |

The decay per Node inside is cosh(kappa) = 6 cos omega - 2 on the chain
(kappa = 1.985 per Link at [2464, 25]). At oblique incidence the split
is invariant under translations along the mirror's plane, so the
tangential wave vector (Outside reading) is kept: the angle of
reflection equals the angle of incidence, the direction arises (PROVED
HERE).

**3.4 Timing (COMPUTATION).** The reflection's phase at the last free
Node before the body is -1.9302 rad at [2464, 25] (D >= 3) and its group
delay (the derivative of the phase by omega) +4.085 intervals, the round
trip from that Node included; at [1232, 25] -2.5402 rad and +3.996
intervals. For the light clock's pin (record 1822, re-derived blind by
the physicist) this is the mirror's contribution per reflection, referred
to the last free Node.

**3.5 The engine lines: none.** A body with a pair is on main (ENGINE.md,
the measured event with `side`, `pair`).

**3.6 The unit tests.** A chain, an emitter of [2464, 25], the mirror of
depth 2 with the face open behind it and a sink beyond: THE SHARE ON THE
TRAIN'S STEADY WINDOW (the booking gained beyond the mirror over the
window, over the same gain without the mirror), 5.561 x 10^-4; depth 1:
3.000 x 10^-2. The ratio of the whole bookings at the records' close is
NOT the share (1.4 x 10^-2 at depth 1 on the physicist's board: the
front is broadband and the records close at different intervals). The
physicist's reading on material-mirror 27226b9d: 3.02 to 3.07 x 10^-2 and
5.6 to 6.0 x 10^-4 window by window, inside the intervals;
the reflected train's first rung at the emitter's receiver later than a
closed face's by the delay difference (K form above, MEASURED ONLY).

---

## 4. (HISTORY) The well body (the massive record's block)

A body declared by its vertex and edge (a cube; a square on a layer; a
segment on a chain), of a massive kind: A WELL, its pair lowered on its
cells trapping a BOUND MODE, the foreign body of the algebra, with the
load-time conditions of the physicist's body check (whole on the board;
the bound mode's integer profile compared bit for bit; the ramp at ten
relaxation times or more; record 1817). Its orientation: none (a cube
is symmetric under the 48). Everything else is specified in
[MASSIVE_RECORD.md](../detector_law/MASSIVE_RECORD.md) and ALGEBRA.md
chapter 8 (8.1 the rule and the band, 8.3 the block, 8.5 the coupling,
8.6 the click, 8.7 the seed), with the build in
[BUILD.md](../detector_law/BUILD.md) and the readings in
[BUILD_READINGS.md](../detector_law/BUILD_READINGS.md). Its declared
properties: `position` and `side`, `pair`, `seed` or the profile with
`margin`, `coupling`, `momentum` with `ramp` and `start`, `wheel`,
`emits`. Its rest period N_0 = 2 pi / omega_0 with cos omega_0 = num /
den (ALGEBRA.md 8.1). Its unit tests are the body check's and the rest
worlds' pins (RUN_LIST.md, the muon's form at rest). This section is an
index.

**4.1 The well among the other tools (ALGEBRA.md 9.9, the well and the
other tools).**
- Only a body with a pair of the well's own family enters its record's
  operator; light's tools are the vacuum for it.
- No click but its own reads its record (by name).
- Its seed is the mode of the COMPOSED world. Where two wells of one
  family are nearly degenerate, the seed is the hybrid localised on the
  well, and the world is refused if sin^2(delta omega T / 2) exceeds the
  reading's band.
- No two bodies share a Node.

The expected values of the load check:
- `sagnac_rest.json`: delta omega = 1.96 x 10^-7 per interval and
  sin^2(delta omega T / 2) = 6.9 x 10^-7, so it is accepted on the band.
  Its seeds, computed alone, differ from the composed ones by up to 244
  units at 72 Nodes (amplitude 52428800), so they are refused until they
  are regenerated.
- A light mirror added off the deep well: the seed is unchanged,
  accepted.
- A receiver of side 2 at (80, 80, 0) inside the deep well: refused; at
  (84, 44, 0): accepted.

The engine line: the margin module's `bound_mode` forms the operator
from every block of the family, not only its own.

---

## 5. (HISTORY) The receiver (an absorbing material with its click's named set)

A body declared by its vertex and edge (the smallest of side 1), of
light's kind, A MATERIAL, NO BOUND MODE, whose Nodes carry the TAKE PAIR
[1, 1] (a complete take: the arriving amplitude booked at its Ports and
held at 0, the counting form of DESIGN.md section 5) for every label
alike, and a wheel: it clicks at the first rung (pointer times W at or
above the record's norm). Its click's NAMED SET is the ladder by name
(SIMULATOR_DEFINITIONS.md, the receiver, the ladder by name, the sinks;
TEST_RUNS.md sections 1 and 4). Its orientation: none (it takes from
every Port). Its action on every label: it books the sum of the record's
label amplitudes' motions and reads no label (a polariser does). A take
pair below [1, 1] is a partial absorber (a grey filter), the untaken
share passing on by the split. Its timing: the first rung. Its cost: one
pointer per record per cell. The engine line: the take pair as a
material integer (today a receiver's take is complete by construction;
[1, 1] keeps every registered world unchanged). The unit tests added: a
record of branches [[0, 1], [1, 1]] booked as one record of the same norm,
its first rung at the same interval as a record of one label; a take
pair [1, 2] books half the offer at its first Node (MEASURED ONLY beside
the K form).

---

## 6. (HISTORY) The emitter with no heading

**6.1 What it is.** A source whose Nodes insert its family's train by
its clock, one record per birth: its amplitude at its own Nodes driven
by the clock, the split carrying it outward to every neighbour
(SIMULATOR_DEFINITIONS.md, the emitter). A beam is several emitter
Nodes driven in phase (DESIGN.md section 2, "The source"), never a
declared heading. The two-arm emitter is cancelled (record 1818): `arms`
refused at load.

**6.2 Its body, its kind, its orientation.** A cube declared by its
vertex and edge (the smallest of side 1, one Node); light's kind (or a
massive kind's matter emitter); A MATERIAL, NO BOUND MODE; its
orientation: none (isotropic). Its declarations: its family and clock,
its train in periods, its rate, its wheel, its residue order, its label
state (the branches of one arm, [[0, 1], [1, 1]] for a source polarised
at 45 degrees, a property nature gives a polarised laser), `own_grace`,
`receiver`.

**6.3 Its action and timing (COMPUTATION on `_births` and `_phase`).**
The train begins at the clock's zero (the phase 3 N / 4) and ends at the
first interval at or after the declared periods whose phase is exactly N
/ 4 or 3 N / 4: at [2464, 25] and 128 periods, 3200 intervals (154
periods). The record's norm is the motion its train inserts, the Nodes
times the sum over the train of the squared steps of the driven
amplitude: at one Node, 128 periods at [2464, 25], N = 2048, the norm is
9517232 (the cosine table's integers). Nothing reaches a Node at
Manhattan distance m before age m (the causal bound); the first rung at
a distance along an axis within a few intervals of the distance over c
(DESIGN.md 6.4: 206 against 2 L / c = 207.85 on the chain), MEASURED
ONLY.

**6.4 The engine line: none** beyond the refusal of `arms`. The unit
tests: the train's 3200 intervals; the norm 9517232 at one Node; a
record of branches [[0, 1], [1, 1]] carried with one amplitude per Node.

---

## 7. (HISTORY) The splitter (a thin layer of material; its outputs arise from its plane)

**7.1 What it is.** A half-silvered layer: the transmitted and the
reflected light arise from its plane; nothing declares where they go.
The splitter of the table form (`Splitter`, declared inputs, weights and
outputs, DECLARATIONS.md section 14 item 4) RETIRES under the owner's
word of 18:55Z.

**7.2 Its body, its kind, its orientation, its material.** A layer ONE
Node thick, a line of cubes of side 1 (a line of bodies, as the mirror
line is), of light's kind, A MATERIAL, NO BOUND MODE, each Node with a
gap pair [num, den] for every label alike; its orientation its plane.
COMPUTATION (the chain's exact harmonic solution of the split): the
one-Node pairs nearest a half-and-half split are [91, 107] (abs(r)^2 =
0.49987) and [108, 127] (0.50016) at [2464, 25], and [183, 199]
(0.49987) at [1232, 25]; the share depends on the clock, as a real
coating's does, and is not exactly 1 / 2 at any pair with a denominator
below 200. At 45 degrees on a layer the reflected light leaves at the
mirror angle (the tangential wave vector kept, an Outside reading,
3.3), so a Mach-Zehnder geometry arises. The POLARISING splitter is the
polariser's splitting form (2.2): the gap for one label only, in the
body's rotated label basis.

**7.3 The engine lines: none** beyond the head's (a body with a pair is
on main). RETIRES: `Splitter` and the linear form it reads.

**7.4 The unit tests.** A chain, the layer [91, 107], an emitter of
[2464, 25]: the offer booked beyond over the total 0.50013, before it
0.49987 (the steady values; the train's spread of clocks MEASURED ONLY
beside).

---

## 8. (HISTORY) The transponder (a moving mirror: a mirror material carried by the massive body)

**8.1 What it is.** A reflector receding from a lamp at rest: the
reflected light returns red-shifted by (1 - beta) / (1 + beta), beta the
reflector's pace over c; the round trip's sent period over the received
one (1 + beta) / (1 - beta) (RUN_LIST.md row 4c, the round trip off a
receding transponder). Reviewer 3's audit (record 1819) found main's
world a SHORTCUT (the old table form, a lamp carrying an imposed
momentum label and a `rerelease` by family name): it RETIRES.

**8.2 Its body, its kind, its orientation.** The massive body of
section 4 (a WELL, its bound mode and its body check), carried at k = 3
(one Link per three intervals), whose cells carry ALSO the mirror
material for light's family: the gap pair [1, 2] (section 3). This is the
crystal's extension (1.1a item 1): a body carrying a pair for each of
two families. Its orientation: its cells' plane. A lamp with its own
receiver at rest (sections 5 and 6) sends and receives.

**8.3 Its action (PROVED HERE on the band; COMPUTATION for the
numbers).** The reflection arises as at a resting mirror (section 3); on
the mirror's line x = v t the incident and the reflected amplitudes keep
one phase, so omega_r = omega_i - v (k_i + k_r), both on the vacuum
band 3 cos omega = 2 + cos k (a chain), v = 1 / 3. The continuum gives
omega_i / omega_r = (1 + beta) / (1 - beta) with beta = v / c = sqrt 3 /
3: 3.7321. ON THE BOARD'S OWN DISPERSION (the pin's number, blind): the
sent over the received clock 3.7733 at [2464, 25] (about 12 Links per
period), 3.7420 at [1232, 25] (about 24 Links): the band's dispersion
adds 1.1 and 0.3 percent to the continuum form. The mirror moves by
hops, one Link every three intervals, so the reflected train carries
sidebands at the hop's clock beside the mean (MEASURED ONLY); the
pin's reading is the mean.

**8.4 Timing.** The round trip from the lamp's birth to the first rung
at its own receiver: 2 D / (c (1 - beta)) in the continuum for a mirror
at the distance D at the birth, receding; the reflection's own delay
(section 3.4, 4.09 intervals at rest) stretched by the motion (MEASURED
ONLY).

**8.5 The engine lines.** A body carrying a pair for each of two
families (shared with the crystal); none else. RETIRES: `rerelease` by
family name and the table body that re-emitted.

**8.6 The unit tests.** At rest (k = 0) the reflected clock equals the
sent one exactly; at k = 3 the ratio of the sent to the received clock
3.7733 at [2464, 25] within the reading's grain (the pin, blind, the
owner's word before any run).

---

## 9. (HISTORY) What each tool needs and what retires, in one table

| Tool | Its body and kind | The engine lines it needs | What retires on main |
| --- | --- | --- | --- |
| The crystal | a square of light's kind, material | one amplitude per label; a body with a pair for each of two families; the take-and-drive at the rising zero (the coupling pair); the pair's residue from the crystal's own count | the two-arm emitter (`arms`), already cancelled |
| The polariser | a cube or a line of cubes of light's kind, material | one amplitude per label; the rotation by the body's axis with the per-part pairs; the click's weights from the label state and the axis | `TableBody`; the key `phase_window` (becomes `axis`) |
| The material mirror | a cube or a line of cubes of light's kind, gap [1, 2], material | none | the one-Node mirror with a declared direction; the closed face as a mirror |
| The well body | a cube of a massive kind, a well | none (the body check) | none |
| The receiver | a cube of light's kind, take [1, 1], material | the take pair as a material integer | none |
| The emitter | a cube, isotropic, material | one amplitude per label | `arms` and declared headings |
| The splitter | a line of cubes, gap [91, 107], material | none | `Splitter` and the linear form |
| The transponder | the massive body carrying the mirror's pair | a body with a pair for each of two families | `rerelease` by family name |

---

## 10. (HISTORY) What is agreed, and what goes to the owner

HISTORY (part A holds): at this section's writing nothing in this file
was agreed yet; each section is checked by the
physicist and agreed or sent to the Boss. The points for the owner from
this draft: (1) no table anywhere: every tool a body of material, the
one enabling line one amplitude per label on every record (the head);
(2) the crystal in the receiver-emitter form of 1.1a with his channels
HV and VH (the pin with Bob's settings exchanged), or its variant HH + VV
(the old roles), or the alternative (B); the bilinear coupling of 1.1a
item 10 named, with its seed and its unwritten conserved form, as the
form in which the halving itself arises; (3) the cone from the dispersion
between the families, birefringence among the born labels removing the
entanglement on a layer; (4) a formed cone's cost; (5) Malus's and Bell's
counts unchanged under the material polariser (the click's weights the
projection of the label state on the material's axis), the books a
consistency test within the rung's margin; (6) the transponder's pin,
blind: 3.7733 at [2464, 25] on the board against the continuum's 3.7321.

---

## 11. (HISTORY) The settlements with the physicist (his checks of 17:10Z and 17:40Z on 08890a34 and 570bc2cf)

AGREED by the physicist and marked so: section 4 (the well body, his body
check on body-check 6c6386ce); section 6 (the emitter with no heading, his
no-heading 98eefac9); section 3's numbers and its engine line "none";
section 5's form; section 0's table; the key `axis` in place of
`phase_window` with `TableBody`'s retirement; the transponder's blind pin
3.7733 (8.3), its sidebands MEASURED ONLY; the retirements table (9). His
recomputation on main's `joint_weights`, `half_angle` and `cell_of`
confirmed every count of 2.6, 1.6 and 1.1a items 7 and 9 exactly.

**11.1 The amplitude per label: withdrawn as the head's enabling line
(his point 1, AGREED).** A one-arm record's label amplitudes are w_l times
ONE field, so the ABSORBING polariser is performed on one field by the
projection: at its cell the passing amplitude J(+) a / 256 with the
record's label state set to the along label, and J(-) a / 256 taken and
booked at the - cell (for an arm of a record of rank 2 the weights are the
partial trace of ALGEBRA.md 9.11 (d), not the coherent sum). One amplitude
per label is needed ONLY by the polariser's SPLITTING form (the two parts
leave in different directions) and by a birefringent crystal (rejected,
1.1a item 4 and ALGEBRA.md 9.3); it is built with the splitting form, if
a world of the list ever needs it, and not for all records. The head's
paragraph "THE ONE ENABLING ENGINE LINE" is superseded by this item.

**11.2 One quantum, one click, settled (his point 2, in his form of 18:05Z).**
ALGEBRA.md 9.7 (b): the crystal is the arriving record's NAMED receiver;
the arriving record clicks at its first rung at the crystal and ends
there (its remaining field energy to the sinks, content 0); at that
interval the crystal births the pair by its own clocks, the pair carrying
the arriving record's residue u. Every arriving record that reaches the
crystal's rung gives one pair, so the emitter's W births over its wheel
(its residue order "seed") give W pairs, and the pairs' joint counts are
exact: at (0, 256), (0, 768), (512, 256), (512, 768), 150, 874, 874, 150
and 874, 150, 150, 874 thrice (HV + VH), S = 181 / 64 with Bob's settings
exchanged. The "fraction converted" is the share of the arriving norm the
crystal's cells book, which must reach the rung (at least 1 / W; about 3
cells over 2 pi 11 Links on the layer, some 4 percent, COMPUTATION of the
order); the crystal's own wheel is not needed.

**11.3 The Bell world's placement and its timing as integers (his points 3
and 6).** The layer [30, 33, 1], periodic on both axes with a shell of
receiver cubes of side 1 (take [1, 1]) on x = 0, x = 29, y = 0 and y = 32
(ALGEBRA.md 9.8); the mirror line y = 16. The emitter: a cube of side 1 at
(2, 16, 0). The crystal: a cube of side 3 at the vertex (13, 15, 0) (cells
x 13 to 15, y 15 to 17, centred on the mirror line). Alice's polariser: a
cube of side 1 at (26, 28, 0), its + receiver a cube of side 1 at (27, 29,
0); Bob's: (26, 4, 0) and (27, 3, 0) (mirror images through y = 16). THE
INTEGERS THE UNIT TEST ASSERTS AS BOUNDS: the crystal's click, the arriving record's first rung there (the pair's
birth) at t_e + 11 or later (the Manhattan distance from (2, 16) to (13,
16)); each arm's first rung at its polariser at the birth + 22 or later
(the Manhattan distance from (15, 17) to (26, 28), and from (15, 15) to
(26, 4)); THE TWO ARMS' FIRST RUNGS EQUAL EXACTLY (the mirror theorem, one
field, a mirror-symmetric placement); the gather's stamp that common
interval. The K forms beside, never asserted: the birth near t_e + 11 / c
= t_e + 19.05, each arm's first rung near the birth + 12 sqrt 2 / c = +
29.39 (from the crystal's centre (14, 16)). The pair's train: 77 periods
of [1232, 25], 3200 intervals, the common zero with the arriving train.

**11.4 The crystal's cells (his point 4).** Under 11.2 the crystal is ONE
receiver set (its cells), the arriving record's receiver by name, NOT a
sink; its first rung is taken over the arriving record's norm with the
set's wheel (the world's W unless declared); no per-Node cells. The open
faces stay faces (ALGEBRA.md 9.8: the face's cell admitted as the shell's
shorthand), so the Bell world's layer is [30, 33, 1] with open faces in
place of the shell of 11.3, the Nodes unchanged.

**11.5 The mirror's and the splitter's test intervals and the closed
face's delay (his point 5; COMPUTATION, the chain's exact harmonic
solution over the train's clocks, the angular frequency within 3 x 2 pi /
3200 of [2464, 25]).** The transmitted share of the booked total: depth 1
between 2.886 x 10^-2 and 3.116 x 10^-2; depth 2 between 5.314 x 10^-4 and
5.816 x 10^-4. The splitter [91, 107]: the reflected share between 0.4901
and 0.5098. THE CLOSED FACE (the Node beyond the last free Node held at 0):
r = -e^(2ik), its phase -2.0859 rad and its delay 2 / v_g = +3.547
intervals referred to the last free Node; the gap mirror's +4.085, so the
material mirror adds +0.538 intervals per reflection over the closed face.
The light clock's first rung comes after ONE reflection (A's record
leaves A, reflects once and returns to A's set), so it moves by +0.538
once, not twice (the physicist's correction). His blind map gives 214 at
W = 64 (211 at 256, 209 at 1024), against 213 on the closed face: the
pin is 214 +- 1 at W = 64, on the chain of 674 with the mirror body at
[672, 674).

**11.6 The label bits as hands (his point (h)).** ALGEBRA.md 9.3's
derivation of HV + VH reads the label bit as the hand (1.2's dictionary).
On main the joint gather reads `labels`, and a bit is a hand only where
the lamp declares `label_hands`: the crystal's world declares it (bit 0
the hand +1, bit 1 the hand -1), so that the derivation's premise is the
world's declaration.

**11.7 The initial state's wording (his point (k)).** Adopted in ALGEBRA.md
9.9: no record but the bodies' own at interval 0, each a well's mode
profile over the whole board; his check to assert that the set of records
at interval 0 is exactly the bodies' own.


## 12. (HISTORY) The two engine forms that close ALGEBRA.md 9.16 (1) and (2), with their unit tests (for the physicist to build)

**12.1 The split sum on one record (ALGEBRA.md 9.16 (1)).**

The form:
- A record's clock is a list of components [[a, n_a], ...]: arm 0 at the
  clock a, arm 1 at p - a, with the integer weight n_a >= 1.
- A crystal's birth writes the components of its declared window [a_lo,
  a_hi] (the material key `window`), with weight 1 each.
- Each component is propagated by the one rule at its own clock. The
  record's offer at a cell is the sum of the components' offers.
- The joint gather's weights are unchanged, because they read the label
  state only.
- Default: one component, which is main's record byte for byte.

The generic primitive is the rule (verbs S and T) applied per component,
with no family name.

The unit tests (inputs, expected values, edge cases):
1. m m^T = N on Z[Z_8]: m^T([3]) has the 8 terms [a] (x) [3 - a], and
   the product of each pair is [3], so m(m^T([3])) = 8 [3].
2. A window [1, 3] at p = 3 gives the 3 components (1, 2), (2, 1) and
   (3, 0), and m of their sum is 3 [3].
3. The degenerate split (a = p - a on Z_N) exists exactly when p is even,
   with two solutions: at N = 8 and p = 4, a = 2 and a = 6; at p = 3,
   none.
4. The default: a world with one component replays main's record byte for
   byte (the gate set's three digests).
5. The counts do not depend on the components: Bell at the axes of 9.16
   (4) with 1 component and with 3 gives the same counts, 1024, 256, 256,
   1024 at W = 2560 for (1, 0) with (1, 2).

**12.2 One amplitude per label on every record (ALGEBRA.md 9.16 (2)).**

The form:
- A record carries two rows per arm, one per label value (bit 0 and bit
  1).
- The one rule acts on each row alike.
- A polar body's cells apply **M**_u = [[a, b], [-b, a]] to the arriving
  pair of rows (verb B). The + row (along the axis) and the - row (across
  it) continue to the body's two receivers.
- The record's norm scale is multiplied by abs(**u**)^2. There is no
  division and no remainder.
- Default: a record with one label value carries one row, which is main's
  record byte for byte.

The generic primitive is verb B with the body's written integers (a, b).
There is no family name and no branch on a label.

The unit tests:
1. The norm identity: at **u** = (15, 8), with rows x = 3 and y = 4, the +
   row is 77 and the - row is 36. So 77^2 + 36^2 = 7225 = 289 x 25 =
   abs(**u**)^2 (x^2 + y^2).
2. H arriving (1, 0) at **u** = (5, 1): the rows are 5 and -1, so the
   books stand 25 : 1. At **u** = (1, 1) they stand 1 : 1, which is 128 of
   256 at the rung.
3. The partial trace (the defect (d) of ALGEBRA.md 9.11): HV + VH at any
   **u** books equal weights on + and -, a^2 + b^2 each. That is 2 and 2 at
   (1, 1) and 289 and 289 at (15, 8). The code on polariser-fix booked all
   of it on + at s = 512; the per-label rows remove that case.
4. Label blindness: a record with the rows (x, 0) and one with (0, x),
   from the same emitter, book the same offer at every cell at every
   interval until a polar body.
5. The default: a world with one label replays main's record byte for
   byte.
