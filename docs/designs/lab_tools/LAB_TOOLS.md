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

THE SYMBOLS USED IN SEVERAL SECTIONS. N = 2048 the phase circle's steps
and W = 2048 the birth wheel; omega (the angular frequency per interval,
an Outside reading) of a clock pair [p, q] is 2 pi p / (q N); the light
family's clock [2464, 25] (omega_0 = 0.302378, a period of 20.779
intervals, about 12 Links per period) and the halved clock [1232, 25]
(omega_1 = omega_0 / 2, about 24 Links); the Outside reading of the
split, 3 cos omega = cos k_x + cos k_y + cos k_z (ALGEBRA.md 8.1 at [1,
1]), with **k** the wave vector (bold lowercase, a vector); c = 1 / sqrt
3 Links per interval; a label is an integer whose bit j is the value on
arm j (0 for H, 1 for V); the branches [[label, weight], ...] a record's
joint labels with integer weights from 1; C'[s] and S'[s] the half-angle
tables at 1 / 256 at the setting s, **U**_s = [[C'[s], S'[s]], [-S'[s],
C'[s]]] (bold uppercase, a matrix); R a cell's weight; E(a, b) a
correlation and S the CHSH sum.

---

## 1. The crystal (it folds in the blind page docs/designs/detector_law/CRYSTAL_ALGEBRA.md, branch crystal-algebra at 238c7281, Reviewer 3's read CONFIRMED WITH LINES, record 1829)

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

THE DESIGN THIS SECTION SPECIFIES: TWO CROSSED CRYSTALS OF TYPE I, the
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

## 2. The polariser (its corrected form: it reads the record's label state; Reviewer 3's finding of record 1819)

**2.1 What it is.** A sheet that passes the polarisation's component
along its axis; in the laboratory a polarising beam splitter sends the
two components to two detectors. Its existing designs: [the Malus
note](../malus/NOTE.md) and DECLARATIONS.md section 14 (the table form).

**2.2 Its body, its kind, its orientation.**

- THE BODY: a cube of side 1 declared by its vertex (its ENTRY cell),
  and its EXIT cell the next Node along its own THROUGH-LINE; the two
  cells one body of two cells (the table body).
- THE KIND: light's kind, a MATERIAL, NO BOUND MODE; its cells are take
  Nodes (a receiver's form: the amplitude held at 0 there). The algebra
  requires one condition of it, true of the tables: **U**_s^T **U**_s =
  n_s **I** exactly (ALGEBRA.md 3.6), so the two weights of a record
  whose weights are w_l sum to n_s times the sum of w_l^2 and the split
  loses nothing beyond the kept remainder.
- THE ORIENTATION, declared by the polariser itself: its TRANSMISSION
  AXIS, the setting s (the axis at pi s / N on the half-angle tables of
  2N), and its THROUGH-LINE, an integer vector of the body's own. On
  main the exit is "the next Node beyond it on the arm's line", taken
  from the emitter's arm direction; with the double emitter cancelled the
  exit is taken from the polariser's own through-line (the Boss's line
  of 18:20Z).

**2.3 Its action (PROVED HERE).** A record whose label state is SUM over
l of w_l (l) reaching the body is split by the weights R(+) = (SUM over
l of w_l U_s[+][bit of l on the body's arm])^2 and R(-) likewise: the
offer booked at the entry cell's Ports moves R(+) / (R(+) + R(-)) of
itself to the exit cell (the + cell), one division per interval with
the remainder kept, and the click's cell is chosen by the birth wheel's
u on the ladder of the two weights. For a record of rank 2 the body's
two cells are one side of the joint gather (ALGEBRA.md 3.6), unchanged.
Nature24's fix on his branch polariser-fix reads this form (his point
5); on main the split reads [C'[s]^2, S'[s]^2], label H's weights alone.

**2.4 Timing (PROVED HERE, the crystal page 3.4).** The first rung of
both cells is the first interval at which the whole offer times W
reaches the record's norm; the split moves the offer between the cells
after the booking and the amplitudes never read the setting: the click's
interval is the same at every setting.

**2.5 The engine lines.** (1) The split's weights from the record's
labels (2.3): generic (the body's table and the record's own label
weights); vector (B, the rotation on the label vector; D, the division
with the remainder kept); local (the entry cell's own Ports). (2) The
exit cell from the body's own through-line (a loader line). Cost: one
pair of weights per record at the body, formed once.

**2.6 The unit tests (COMPUTATION; the + and - counts over one wheel of
births):**

| The record, W = 2048 | s = 0 | s = 256 | s = 512 | s = 768 | s = 1024 |
| --- | --- | --- | --- | --- | --- |
| label H, [[0, 1]] | 2048, 0 | 1749, 299 | 1024, 1024 | 299, 1749 | 0, 2048 |
| label V, [[1, 1]] | 0, 2048 | 299, 1749 | 1024, 1024 | 1749, 299 | 2048, 0 |
| 45 degrees, H + V, [[0, 1], [1, 1]] | 1024, 1024 | 1747, 301 | 2048, 0 | 1747, 301 | 1024, 1024 |

The weights: H at s = 256 (56169, 9604) = (237^2, 98^2); H + V at 256
(112225, 19321) = ((237 + 98)^2, (237 - 98)^2), at 512 (131044, 0) =
(362^2, 0). At W = 64 the + counts at s = 0, N / 4 and N / 2 are 64,
32, 0 for H, 0, 32, 64 for V and 32, 64, 32 for H + V (Nature24's test,
agreeing). Malus's four worlds (records of label H) keep their declared
counts (RUN_LIST.md row 9). The timing test: the click's interval equal
at every setting. The through-line test: a polariser whose through-line
is (0, 1, 0) on a layer takes its exit cell at its vertex plus (0, 1, 0)
with no emitter arm declared.

---

## 3. The material mirror (a gap block of light's kind; the reflection arises)

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
depth 2 with the face open behind it and a sink beyond: the offer booked
beyond it over the booked total 5.561 x 10^-4 (the steady value; the
train's spread of clocks MEASURED ONLY beside); depth 1: 3.000 x 10^-2;
the reflected train's first rung at the emitter's receiver later than a
closed face's by the delay difference (K form above, MEASURED ONLY).

---

## 4. The well body (the massive record's block)

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

---

## 5. The receiver

A body declared by its vertex and edge (the smallest of side 1), of
light's kind, A MATERIAL, NO BOUND MODE, whose cells are take Nodes with
a wheel: it books the record's offer at its Ports and clicks at the
first rung (pointer times W at or above the record's norm). Specified in
DESIGN.md section 5 (the counting form and the books),
SIMULATOR_DEFINITIONS.md "The four building blocks" (the receiver, the
ladder by name, the sinks) and TEST_RUNS.md sections 1 and 4 (its
tests). Its orientation: none (it takes from every Port). Its action on
every label: it books the whole offer and reads no label (a polariser
does). Its timing: the first rung. Its cost: one pointer per record per
cell. No new engine line. The unit test added: a record of branches
[[0, 1], [1, 1]] booked as one record of the same norm, the first rung
at the same interval as a record of one label.

---

## 6. The emitter with no heading

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

## 7. The splitter (a thin layer; its outputs from its orientation: A DESIGN LINE FOR THE OWNER)

**7.1 What it is.** A half-silvered layer: the transmitted and the
reflected light arise from its plane; nothing declares where they go.
On main the splitter of the table form declares its outputs
(DECLARATIONS.md section 14 item 4; record 1830 puts it to the owner).

**7.2 The proposal.** A layer ONE Node thick: a line of cubes of side 1
(a line of bodies, as the mirror line is), each of light's kind with a
gap pair [num, den], A MATERIAL, NO BOUND MODE; its orientation its
plane; the reflected share arises by the split. COMPUTATION (the chain's
exact harmonic solution): the one-Node pairs nearest a half-and-half
split are [91, 107] (abs(r)^2 = 0.49987) and [108, 127] (0.50016) at
[2464, 25], and [183, 199] (0.49987) at [1232, 25]: the share depends on
the clock, as a real coating's does, and is not exactly 1 / 2 at any
pair of this search (denominators below 200). At 45 degrees on a layer
the reflected light leaves at the mirror angle (the tangential wave
vector kept, an Outside reading, 3.3), so a Mach-Zehnder geometry arises. THE OWNER'S WORD:
whether the splitter becomes this material layer (its share a computed
number, not a declared 1 / 2) or keeps the table form with declared
outputs.

**7.3 The unit tests (if adopted).** A chain, the layer [91, 107], an
emitter of [2464, 25]: the offer booked beyond over the total 0.50013,
before it 0.49987 (the steady values; the train's spread of clocks
MEASURED ONLY beside).

---

## 8. What is agreed, and what goes to the owner

Nothing in this file is agreed yet: each section is checked by the
physicist and agreed or sent to the Boss. The points for the owner from
this draft: (1) the crystal in the type I form of two crossed crystals
(1.2): record 1830's rule and record 1831's word leave type II with
mirror arms impossible with an index per label; (2) the crystal's index
table per label AND per clock (its dispersion, 1.3), which keeps one
amplitude per Node per record everywhere; (3) the splitter as a material
layer (7.2).
