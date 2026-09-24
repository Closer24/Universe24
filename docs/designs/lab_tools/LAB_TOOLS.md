# The lab tools: one specification per tool, each with its algebra, its timing, its cost, its engine lines and its unit tests' expected values (the mathematician, 2026-09-24; checked by the physicist; docs only)

THE OWNER'S WORDS (2026-09-24, records 1825, 1830, 1831 and 1832 of
docs/LOG_2026-09-20.md, on the Boss's log branch until it merges; the
Boss's orders of 17:25Z to 17:45Z): there are three levels, the building
blocks, the lab tools and the experiments; every tool gets its algebra
and is checked by its own tests before it enters an experiment; "all of
the above is defined in one specification file of the lab tools; the
mathematician can write the design of everything; Nature just checks all
of it and talks with him". A tool declares its own orientation and never
the directions of what leaves it (record 1830). The split and the
carrying of amplitude are the board's own (record 1831).

THE FORM OF EVERY SECTION: what the tool is and what nature gives it; its
declared properties and its orientation; its action on every kind of
input (every label, a superposition, every Port); its timing; its cost;
the engine lines it needs, each with the three tests (generic, vector,
local; [skills/workflow.md](../../../skills/workflow.md)); its unit
tests' exact expected values. Each statement carries its kind: PROVED
HERE, COMPUTATION (exact integers from main's own functions, or the
band's closed form in floating point, labelled so), MEASURED ONLY (a
board quantity no closed form reaches; a run may read it and never pin
it), or DECLARATION. Existing design files are cited, never copied.
Nothing here is code; the physicist writes the code, the worlds and the
test-run lines, each tool's code after its section is agreed.

THE BUILDING BLOCKS AND THE RULE: SIMULATOR_DEFINITIONS.md "The four
building blocks"; the rule of [DESIGN.md](../detector_law/DESIGN.md)
section 2 and its band, 3 cos omega = cos k_x + cos k_y + cos k_z
(ALGEBRA.md 8.1 at [1, 1]); the medium's coefficient form, DESIGN.md
section 4.1; the click, the ladder and the joint gather, ALGEBRA.md 3.6,
4.9 and 4.10.

THE SYMBOLS USED IN SEVERAL SECTIONS. N = 2048 the phase circle's steps
and W = 2048 the birth wheel; omega (the angular frequency per interval)
of a clock pair [p, q] is 2 pi p / (q N); the light family's clock [2464,
25] (omega_0 = 0.302378, a period of 20.779 intervals, lambda about 12
Links) and the halved clock [1232, 25] (omega_1 = omega_0 / 2, about 24
Links); **k** the wave vector (bold lowercase, a vector), k its length;
c = 1 / sqrt 3 Links per interval; v_g the group pace; a label is an
integer whose bit j is the value on arm j (0 for H, 1 for V); the
branches [[label, weight], ...] a record's joint labels with integer
weights from 1; C'[s] and S'[s] the half-angle tables at 1 / 256 at the
setting s, **U**_s = [[C'[s], S'[s]], [-S'[s], C'[s]]] (bold uppercase,
a matrix); R a cell's weight; E(a, b) a correlation and S the CHSH sum.

---

## 1. The crystal (it folds in the blind page docs/designs/detector_law/CRYSTAL_ALGEBRA.md, branch crystal-algebra at 238c7281, Reviewer 3's read CONFIRMED WITH LINES, record 1829)

**1.1 What it is and what nature gives it.** In the laboratory, a
nonlinear crystal converts a small fraction of an arriving photon's
amplitude into a pair whose energies and momenta sum to the arriving
one's; the pair's directions arise from the conversion itself (phase
matching), never pushed afterwards; the crystal is birefringent (its
pace depends on the polarisation), which is what lets the directions be
off the arriving axis. For Bell's experiment the laboratory uses either
one crystal of type II (the pair HV or VH) or two thin crystals of type I
with their optic axes crossed (the pair HH from one, VV from the other;
Kwiat and others, 1999). The owner's decisions: the crystal and Bell are
one experiment (record 1817); the double emitter is cancelled (1818);
the entanglement arises from two indistinguishable conversion channels
whose amplitudes add in one record of rank 2 (1821); the crystal is
birefringent (1829); the split and the carrying of amplitude are the
board's own (1831).

**1.2 The answer to the owner's question of record 1831 ("the medium
alone causes this ... confirm whether I am right") (PROVED HERE).**

- RIGHT for the pace and the spreading: every record's wave spreads from
  Node to Node by the rule, and a medium sets the pace per Node by its
  coefficient (DESIGN.md 4.1); a crystal of one index needs nothing new.
- RIGHT for the directions, in the TYPE I form: if the pair is born at
  every crystal Node with each arm's phase HALF the arriving phase there
  (the arms' clocks summing to the arriving clock and nothing else
  declared), each arm's source has the phase gradient k_p / 2 along the
  arriving axis, so each arm radiates where its own wave vector's
  component along that axis equals k_p / 2. For two arms of the same
  label at index n_s in a crystal where the arriving label has index n_p
  < n_s, this is the heading cos(theta_in) = n_p / n_s inside, both arms
  at +theta and -theta, mirror images: the cone arises from the medium
  alone.
- NOT for the type II form with mirror arms: with the half-phase birth,
  the H arm radiates at sin(theta_out) = sqrt(n_H^2 - n_p^2) and the V
  arm at sqrt(n_V^2 - n_p^2) outside (continuum form, exit face normal
  to the arriving axis); the arriving record carries H or V, so n_p is
  n_H or n_V and that label's arm is collinear (theta = 0); and mirror
  arms need n_H = n_V, which is no birefringence. The page on the branch
  crystal-algebra reached type II only by DECLARING each arm's source
  phase across the crystal's cells (its section 8.2), which record 1830
  now forbids (a tool never declares the directions of what leaves it).
  Type II with mirror arms would need an index per CLOCK as well as per
  label (the arriving record's clock seeing a lower index than both
  arms'): a dispersion table, not a birefringence.

THE DESIGN THIS SECTION SPECIFIES, therefore: TWO CROSSED CRYSTALS OF
TYPE I, the laboratory's second form. This differs from record 1821's
channels (H on the first arm and V on the second, and the swap), which
is type II: A POINT FOR THE OWNER through the Boss. What the two forms
share is the owner's principle: two indistinguishable conversion
channels whose amplitudes add in one record; here the channels are V to
HH (the first crystal) and H to VV (the second), and their sum is HH +
VV, which is EXACTLY the state the cancelled emitter declared, so the
Bell pin of the cancelled worlds stands with its roles unchanged (1.6).

**1.3 Declared properties and orientation.**

- Its cells: a rectangle of Nodes on the layer, L along the arriving
  axis and W across (a line of blocks of side 1, as the mirror line is
  built; the body form on main is a square, SIMULATOR_DEFINITIONS.md
  "The body").
- Its ORIENTATION, the one thing a crystal declares about direction: its
  index table per label, one coefficient pair per label value, [num,
  den] = 1 / n^2 (the index squared, so an irrational index is an exact
  pair). The first crystal: V [1, 1] (the vacuum's pace) and H [2, 3]
  (n_H^2 = 3 / 2); the second crystal, rotated by 90 degrees: H [1, 1]
  and V [2, 3]. Nothing declares a heading.
- Its conversion entry: the arriving label that converts (V in the
  first crystal, H in the second), the pair's joint label (0 = HH from
  the first, 3 = VV from the second), the arms' clocks ([1232, 25] each,
  summing to [2464, 25], refused at load otherwise), and the per-Node
  fraction [n, d] of the arriving amplitude, the passing amplitude m / d
  with n^2 + m^2 = d^2 (a Pythagorean triple, checked at load as the
  splitter's isometry is; section 4.2 of the crystal page).
- `seed` 0 (silent: no record of its own); no coupling.

**1.4 Its action on every input (the continuum statements PROVED HERE;
the lattice numbers COMPUTATION on the band).**

- The arriving record's label parts cross each crystal at their own
  paces (the index table); a record whose label state holds both H and V
  therefore needs ONE WAVE PER LABEL VALUE while it is inside the crystal
  (1.7, the engine line).
- An arriving part of the converting label (V in the first crystal) is
  converted at every Node it reaches: the pair's two arms are born there
  with the fraction [n, d] of the local level and each arm's phase half
  the arriving phase (the arms' clock started at the arriving level's
  rising zero at that Node, so the half is taken without sign ambiguity:
  1.7); the rest passes at m / d.
- The part of the other label (H in the first crystal) passes
  unconverted at its own pace.
- The arms (both H from the first crystal) radiate where k_x = k_p / 2:
  inside cos(theta_in) = n_p / n_s, outside sin(theta_out) = sqrt(n_s^2
  - n_p^2); at n_p = 1 and n_s^2 = 3 / 2 the continuum gives 45 degrees
  outside EXACTLY (35.26 degrees inside). On the band (the arms at
  [1232, 25], a layer): the match at 44.321 degrees outside, 35.226
  inside. The second crystal's arms (both V) match at the same angle by
  the swap of its index table (PROVED HERE: the same equation with the
  labels exchanged). So HH and VV leave on the same two headings, the
  channels coincide exactly, and each arm's record carries both label
  columns: THE ENTANGLEMENT ARISES (HH + VV on every mirror pair) and is
  never declared.
- The mismatch per Link and the lobe (COMPUTATION on the band, one arm,
  the Dirichlet factor of L Nodes): delta k = -0.0579 at the collinear
  heading, -0.0354 at (2, 1, 0), +0.0016 at (1, 1, 0) and +0.0445 at (1,
  2, 0). The collinear heading leaves the main lobe from L = 109 (2 pi /
  0.0579); (2, 1, 0) and (1, 2, 0) as well from L = 178; 45 degrees
  stays in the lobe up to L = 2021. The half-power band of the lobe: 0.1
  to 88.9 degrees at L = 24 (no selection), 0.1 to 70.0 at L = 48, 30.4
  to 56.6 at L = 96. The width scales as lambda_1 / L, and the far field
  where the lobe is read as 2 A^2 / lambda_1 (A the crystal's aperture
  seen from 45 degrees, (L + W) / sqrt 2): about 5300 Links at L = W =
  178, a HOST cost to weigh.
- THE PIN DOES NOT NEED THE SELECTION: the counts come from the joint
  gather's weights (1.6), and a short crystal radiates broadly, its lobe
  still peaked at 44.3 degrees. So the Bell world may take a short
  crystal (L = 24), and the lobe's width is the crystal's own unit test
  on a large board (1.9, test 5).
- The side faces (PROVED HERE on the band): the arms' k along the axis
  inside equals the vacuum's whole k at the match (exactly in the
  continuum, n_s^2 - sin^2(theta_out) = n_p^2 = 1; 0.26237 per Link both
  on the band at 45 degrees), so an arm row that meets a face along the axis leaves it at
  grazing; the crystal is taken wider than long (W >= 2 L) so the rows
  that matter leave through the far face.
- The norm: the Nodes' amplitudes add coherently in the lobe, so the
  per-Node fraction is at most about 1 / L on it; the Pythagorean pairs
  of that size are (2 j + 1, 2 j (j + 1), 2 j (j + 1) + 1), n / d about 1
  / j (at L = 24: [49, 1201], the passing numerator 1200).
- Every Port of the crystal reads the rule as every Node does; the
  crystal takes nothing (it is no receiver) and books nothing but the
  births.

**1.5 One quantum, one click, one residue (PROVED HERE; the crystal
page's section 2.6 and 4.2).** The arriving record's quantum ends in one
click: the pair and the passing part are outcomes of ONE record with one
residue u and one gather; separate records would click twice for one
quantum. The pair's residue: the crystal's own count of its conversions
on its own wheel of W (the crystal a body whose own record counts, the
clock block), which makes the counts exact for every fraction (the
crystal page's 4.5); the order test of the hidden residue
(DECLARATIONS.md section 2 item 8) then moves to the crystal.

**1.6 The state and the pin (COMPUTATION on main's tables and rung;
exact integers).** The two crossed crystals with an arriving record of
label state H + V (the emitter's branches [[0, 1], [1, 1]], weights 1
and 1) give the pair's branches [[0, 1], [3, 1]]: HH + VV with equal
weights, the relative phase set by the geometry and NOT READ by the
joint gather, which reads the integer label weights (a stated departure
from nature, where a relative phase other than 0 lowers S). The counts
at the cancelled worlds' four settings pairs, W = 2048, one gathered
pair per residue of the crystal's wheel:

| (a, b) | ++, +-, -+, -- | E |
| --- | --- | --- |
| (0, 256) | 874, 150, 150, 874 | +181 / 256 |
| (0, 768) | 150, 874, 874, 150 | -181 / 256 |
| (512, 256) | 874, 150, 150, 874 | +181 / 256 |
| (512, 768) | 874, 150, 150, 874 | +181 / 256 |

S = E(0, 256) - E(0, 768) + E(512, 256) + E(512, 768) = 181 / 64 =
2.828125 EXACTLY, the cancelled worlds' pin with their roles UNCHANGED
(no exchange of Bob's settings, unlike the type II page); the marginals
1024 of 2048. THE PIN'S FORM, DECLARED HERE BEFORE ANY RUN (Reviewer 3's
line): the four worlds a in {0, 512}, b in {256, 768}; S as written;
the pair's residue the crystal's own count; any count other than the
table's an engine defect to name.

**1.7 The engine lines (each new; the physicist writes them after this
section is agreed).**

1. THE WAVE PER LABEL. A record's state holds one wave (a_now, a_before,
   the remainder) per label value, H and V, at every Node where the
   record has rows; outside every crystal both waves step by the same
   rule, so a record born with one label keeps one wave in effect. Today
   a LiveRecord (`detector_law.py`) holds one wave and one label state
   (record 1831's open point): this is the change. Generic (one wave per
   label bit, no family name); vector (the rule per wave, no root);
   local (each wave's own six reads). Cost: twice the storage and work
   for a record of two labels.
2. THE INDEX PER LABEL. Inside a crystal's cells a wave of label value l
   steps by the coefficient form of DESIGN.md 4.1 with the label's pair
   [num_l, den_l] = 1 / n_l^2: 3 den_l a_next + r' = num_l S_6 + 6 (den_l -
   num_l) a_now - 3 den_l a_before + r, 0 <= r' < 3 den_l. Generic (the
   pair chosen by the label bit from the body's declared table); vector
   (T with the pair, D by the wall 3 den_l); local (its own wave's six
   reads).
3. THE CONVERSION AT EVERY NODE, FIRED BY ARRIVAL. At a crystal Node,
   from the first interval the arriving record's wave of the converting
   label rises through zero after its first rung at that Node, the Node
   drives the pair's two arms' waves of the pair's label with the
   fraction n / d of the arriving level's amplitude (the linear form of
   DECLARATIONS.md section 14 reading the arriving pair (a_before,
   a_now)) on the arms' clock started at that interval, and the arriving
   wave keeps m / d there. Generic (a declared conversion entry, no
   family name); vector (B the linear form, D the division by d with the
   remainder kept, E the clock's table); local (the Node's own rows and
   the arriving wave's own pair). No block on main births on a rung
   (Reviewer 3's line): this is new, with its test.
4. THE PAIR'S RESIDUE: the crystal's own count of its conversions, one
   per converted quantum, on a wheel of W (the clock block's count),
   the residue order declared at the crystal.

**1.8 The timing (the formulas; the absolute first-rung intervals
MEASURED ONLY).** An emitter at L0 Links before the first crystal along
the axis, the two crystals of length L each, back to back; the bodies'
entry Nodes at L1 steps along (1, +-1, 0) from the crystals' far face.

- The arriving train is 3200 intervals (the declared 128 periods become
  154 by the quarter-zero rule; 3200 is also 77 periods of the halved
  clock, a common zero; the crystal page 3.1).
- The first crystal converts from t_e + L0 / c (the arriving's V part at
  the vacuum's pace; bound t_e + L0), each Node x at t_e + (L0 + x) / c.
- The second crystal converts the H part after it has crossed the first
  crystal at n_H: from t_e + (L0 + L sqrt(3 / 2)) / c. The VV pair
  therefore lags the HH pair by L (sqrt(3 / 2) - 1) / c = 9.3 intervals
  at L = 24 (COMPUTATION, continuum), against a train of 3200: not read
  by any count (the gather reads weights, not times within a record).
- Each arm's first rung at its body: after t_e + L0 / c + (the path to
  the body) / c (K form), the bound the Manhattan distance; the group
  pace of each column on its heading c (1 + k^2 (1 - 3 A) / 24) outside
  (A the sum of the heading's components to the fourth power; the
  crystal page 3.3).
- THE MIRROR THEOREM HOLDS (PROVED HERE, the crystal page's 3.4 per
  label column): the crystals, the board and the bodies symmetric about
  the arriving axis, each crystal's two arms of one label and one clock,
  so at every interval arm 1's column of each label is the mirror image
  of arm 0's column of the same label; the two arms' first rungs and
  completions are equal EXACTLY at every setting; the gather's stamp is
  that common interval.

**1.9 The unit tests, each on a small world that is none of the
fifteen, with their exact expected values.**

1. THE INDEX PER LABEL (a chain; a slab of the coefficient [2, 3] and
   length 60; one emitter of label H, then one of label V): the H train's
   envelope crosses the slab in 60 sqrt(3 / 2) / v_g intervals against
   60 / v_g for V (the continuum ratio sqrt(3 / 2) = 1.2247 exactly in
   the K form; the first rungs at a receiver beyond the slab MEASURED
   ONLY, their difference within the chain's grain of the K form's 23.4
   intervals, 60 (sqrt(3 / 2) - 1) / c). An emitter of H + V: two columns, each at its
   own pace; outside the slab one wave each, unchanged.
2. ONE CRYSTAL, ARRIVING V (type I, the first crystal alone): the
   pair's branches [[0, 1]] (HH), product; the joint counts at (0, 0):
   2048, 0, 0, 0; at (512, 512): 512, 512, 512, 512; at (0, 512): 1024,
   1024, 0, 0; at (0, 256): 1749, 299, 0, 0.
3. ONE CRYSTAL, ARRIVING H (the first crystal): nothing converted, the
   record passes whole at n_H's pace; no pair, no gather.
4. TWO CROSSED CRYSTALS, ARRIVING H + V: the branches [[0, 1], [3, 1]];
   at (0, 0): 1024, 0, 0, 1024; at (512, 512): 1024, 0, 0, 1024 (the
   entanglement test: the product of test 2 gives 512 in each cell
   there); at (0, 512): 512, 512, 512, 512; the Bell table of 1.6.
5. THE LOBE (a large layer, L = 96, receivers on a ring in the far
   field, GAMEBOARD by declaration): the arms' offer peaked at 44.3
   degrees, the half-power band 30.4 to 56.6 degrees; no arm offer at the
   collinear heading above the lobe's side level.
6. THE REFUSALS at load: arms' clocks not summing to the arriving clock;
   a conversion fraction that is not a Pythagorean pair; an index pair
   with num > den (a label faster than the vacuum).
7. THE MIRROR THEOREM (a symmetric placement, two settings pairs): the
   two arms' first-rung intervals equal, and equal across the settings.

**1.10 Cost.** Per record of two labels, twice the rows and the six reads
per Node per interval (the wave per label); per crystal Node per
interval, one linear form and one division per converting record; the
far-field selection test's board (5300 Links at L = 178) is the one large
HOST cost; the Bell world itself stays small (a short crystal, 1.4).

---

## 2. The polariser (its corrected form: it reads the record's label state; Reviewer 3's finding of record 1819)

**2.1 What it is.** A sheet that passes the component of the polarisation
along its axis and absorbs or deflects the rest; in the laboratory a
polarising beam splitter sends the two components to two detectors. Its
existing designs: [the Malus note](../malus/NOTE.md) and DECLARATIONS.md
section 14 (the table form); the table body of two cells,
SIMULATOR_DEFINITIONS.md "The body".

**2.2 Declared properties and orientation.** Its Node (the entry cell)
and the next Node beyond it on the line the record arrives on (the exit
cell); its setting s, an integer on the half-angle tables of 2N (its
orientation: the axis at pi s / N). Nothing declares a heading.

**2.3 Its action (PROVED HERE).** A record whose label state is SUM over
l of w_l (l) reaching the body is split by the weights R(+) = (SUM over l
of w_l U_s[+][l])^2 and R(-) = (SUM over l of w_l U_s[-][l])^2, the
joint gather's primitive with one body: the offer booked at the entry
cell's Ports moves R(+) / (R(+) + R(-)) of itself to the exit cell (the
+ cell), one division per interval with the remainder kept, and the
click's cell is chosen by the birth wheel's u on the ladder of the two
weights. For a record of rank 2 the body's two cells are one side of the
joint gather (ALGEBRA.md 3.6), unchanged. On main the split reads [C'[s]^2,
S'[s]^2], the weights of the label H alone, for every record: the bug.

**2.4 Timing (PROVED HERE, the crystal page 3.4).** The first rung of
both cells is the first interval at which the whole offer (the two cells'
sum) times W reaches the record's norm; the split moves the offer
between the two cells after the booking, and the levels never read the
setting: the click's interval is the same at every setting.

**2.5 The engine line.** The split's weights from the record's labels
(the formula of 2.3). Generic (the table of the body and the record's
own label weights, no family name); vector (B, the rotation on the label
vector; D, the division with the remainder kept); local (the entry
cell's own Ports). Cost: one pair of weights per record at the body,
formed once.

**2.6 The unit tests (COMPUTATION, W = 2048; the + and - counts over one
wheel of births):**

| The record | s = 0 | s = 256 | s = 512 | s = 768 | s = 1024 |
| --- | --- | --- | --- | --- | --- |
| label H, [[0, 1]] | 2048, 0 | 1749, 299 | 1024, 1024 | 299, 1749 | 0, 2048 |
| label V, [[1, 1]] | 0, 2048 | 299, 1749 | 1024, 1024 | 1749, 299 | 2048, 0 |
| 45 degrees, H + V, [[0, 1], [1, 1]] | 1024, 1024 | 1747, 301 | 2048, 0 | 1747, 301 | 1024, 1024 |

The weights: H at s = 256 (56169, 9604) = (237^2, 98^2); H + V at 256
(112225, 19321) = ((237 + 98)^2, (237 - 98)^2), at 512 (131044, 0) =
(362^2, 0). The V and 45-degree rows tell the corrected form from main's.
Malus's four worlds (records of label H) keep their declared counts
(RUN_LIST.md row 9). The timing test: the click's interval equal at s =
0, 256, 512 and 768.

---

## 3. The material mirror (a gap block of light's kind; the reflection arises)

**3.1 What it is.** A metal or dielectric mirror reflects because the
wave cannot propagate inside it; nothing tells it the outgoing direction.
Here: a block of light's kind whose pair [num, den] on the six-neighbour
term opens a gap (cos omega_0 = num / den, ALGEBRA.md 8.1): every clock
below omega_0 is evanescent inside, and the reflection arises by the
rule. The mirror line is this (DECLARATIONS.md section 15 item L-1, the
pair [1, 2], omega_0 = pi / 3 = 1.047 per interval). It replaces the
board's closed face in the light clock (record 1822) and the one-Node
mirror that re-emitted in a declared direction (record 1830).

**3.2 Declared properties and orientation.** Its cells (a line or a
slab, its depth D in Nodes), its pair; its orientation is its cells'
plane; the face behind it open. Not `absorbing`.

**3.3 Its action (COMPUTATION: the exact harmonic scattering of the
rule on a chain, in complex floating point; no rule stepped).** At the
light clock [2464, 25], off the pair [1, 2], the reflected energy share
|r|^2 and the transmitted |t|^2 (|r|^2 + |t|^2 = 1 to the printed
digits):

| Depth D | [2464, 25]: abs(r)^2; abs(t)^2 | [1232, 25]: abs(r)^2; abs(t)^2 |
| --- | --- | --- |
| 1 | 0.969997; 3.000 x 10^-2 | 0.992410; 7.590 x 10^-3 |
| 2 | 0.999444; 5.561 x 10^-4 | 0.999876; 1.237 x 10^-4 |
| 3 | 0.999990; 1.038 x 10^-5 | 0.999998; 2.067 x 10^-6 |
| 4 | 1 - 2 x 10^-7; 1.938 x 10^-7 | 1 - 3 x 10^-8; 3.456 x 10^-8 |

The evanescent decay per Node inside is cosh(kappa) = 6 cos(omega) - 2
on the chain (kappa = 1.985 per Link at [2464, 25]). At oblique
incidence the reflection keeps the tangential wave vector (the rule is
invariant under translations along the mirror's plane), so the angle of
reflection equals the angle of incidence: the direction arises.

**3.4 Timing (COMPUTATION).** The reflection's phase at the last free
Node before the block is -1.9302 rad at [2464, 25] (D >= 3) and its
group delay (the derivative of the phase by the clock) +4.085 intervals,
round trip from that Node included; at [1232, 25] -2.5402 rad and +3.996
intervals. For the light clock's pin (record 1822, re-derived blind by
the physicist) this is the mirror's contribution per reflection referred
to the last free Node.

**3.5 The engine line: none.** A block with a pair is on main (ENGINE.md,
the measured event with `side`, `pair`). Its three tests are the rule's.

**3.6 The unit tests.** A chain, an emitter of [2464, 25], the mirror of
depth 2 with the face open behind it and a sink beyond: the offer booked
beyond the mirror over the booked total 5.561 x 10^-4 within the train's
spectral spread (MEASURED ONLY beyond the steady-state value); the
reflected train's first rung at the emitter's own receiver later than the
closed face's by the delay difference (MEASURED ONLY; the K form above).
Depth 1: 3.000 x 10^-2 beyond.

---

## 4. The well body (the massive record's block)

A block with the massive kind's pair, its own record seeded on its
cells, its bound mode and its clock: specified in
[MASSIVE_RECORD.md](../detector_law/MASSIVE_RECORD.md) and ALGEBRA.md
chapter 8 (8.1 the rule and the band, 8.3 the block, 8.5 the coupling,
8.6 the click, 8.7 the seed), with the build in
[BUILD.md](../detector_law/BUILD.md) and the readings in
[BUILD_READINGS.md](../detector_law/BUILD_READINGS.md); the body's
conditions (whole on the board, the bound mode's profile compared bit for
bit, the ramp at ten relaxation times or more) in the physicist's body
check (record 1817). Its declared properties: `position` and `side` (the
cube's lower vertex and edge), `pair`, `seed` or the profile with
`margin`, `coupling`, `momentum` with `ramp` and `start`, `wheel`,
`emits`. Its orientation: none (a cube is symmetric under the 48). Its
rest period N_0 = 2 pi / omega_0 with cos omega_0 = num / den (ALGEBRA.md
8.1). Its unit tests are the body check's and the rest worlds' pins
(RUN_LIST.md, the muon's form at rest): nothing new here; the section is
an index.

---

## 5. The receiver

A set of cells with a wheel that books the record's offer at its Ports
and clicks at the first rung (pointer x W at or above the record's norm):
specified in DESIGN.md section 5 (the counting form and the books),
SIMULATOR_DEFINITIONS.md "The four building blocks" (the receiver, the
ladder by name, the sinks) and TEST_RUNS.md sections 1 and 4 (its
tests). Its orientation: none (it takes from every Port). Its action on
every label: it books the whole offer, the sum over the label columns
(1.7); a receiver never reads a label (a polariser does). Its timing:
the first rung; its cost: one pointer per record per cell. The new line
for the wave per label: the booked offer is the sum of the columns'
motions. The unit test added: a record of two label columns booked as
the sum of the two, the first rung the same as a one-label record of the
same norm.

---

## 6. The emitter with no heading

**6.1 What it is.** A source at a Node that inserts its family's train
by its clock, one record per birth, isotropic (a lamp with no `directions`
on main radiates to all six neighbours; SIMULATOR_DEFINITIONS.md, the
emitter). A beam is a line of emitter Nodes driven in phase (DESIGN.md
section 2, "The source"), never a declared heading. The two-arm emitter
is cancelled (record 1818): `arms` refused at load.

**6.2 Declared properties.** Its Node or Nodes, its family and clock, its
train in periods, its rate, its wheel, its residue order, its label state
(the branches of one arm, e.g. [[0, 1], [1, 1]] for a source polarised at
45 degrees: a property nature gives a polarised laser), `own_grace`,
`receiver`.

**6.3 Its action and timing (COMPUTATION on `_births` and `_phase`).**
The train begins at the clock's zero (the phase 3 N / 4) and ends at the
first interval at or after the declared periods whose phase is exactly N
/ 4 or 3 N / 4: at [2464, 25] and 128 periods, 3200 intervals (154
periods). The record's norm is the motion its train inserts, the Nodes
times the sum over the train of the squared steps of the driven level: at
one Node, 128 periods at [2464, 25], N = 2048, the norm is 9517232 (the
cosine table's integers). Nothing reaches a Node at Manhattan distance m
before age m (the causal bound); the first rung at a distance along an
axis within a few intervals of the distance over c (DESIGN.md 6.4:
206 against 2 L / c = 207.85 on the chain), MEASURED ONLY.

**6.4 The engine line: none** beyond the refusal of `arms`. The unit
tests: the train's 3200 intervals; the norm 9517232 at one Node; a record
of branches [[0, 1], [1, 1]] carried as two label columns of equal
waves.

---

## 7. The splitter (a thin layer; its outputs from its orientation: A DESIGN LINE FOR THE OWNER)

**7.1 What it is.** A half-silvered layer: the transmitted and the
reflected waves arise from its plane; nothing declares where they go.
On main the splitter of the table form declares its outputs
(DECLARATIONS.md section 14 item 4; record 1830 puts it to the owner).

**7.2 The proposal.** A layer of ONE Node thickness of a gap pair [num,
den] of light's kind (as the mirror, thinner): its orientation is its
plane; the reflected share arises by the rule. COMPUTATION (the chain's
exact scattering): the one-Node pairs nearest a half-and-half split are
[91, 107] (|r|^2 = 0.49987) and [108, 127] (0.50016) at [2464, 25], and
[183, 199] (0.49987) at [1232, 25]: the share depends on the clock, as a
real coating's does, and is never exactly 1 / 2 at a rational pair in
this search. At 45 degrees on a layer the reflected wave leaves at the
mirror angle (the tangential wave vector kept), so the Mach-Zehnder
geometry arises. THE OWNER'S WORD: whether the splitter becomes this
material layer (its share a computed number, not a declared 1 / 2) or
keeps the table form with declared outputs.

**7.3 The unit tests (if adopted).** A chain, the layer [91, 107], an
emitter of [2464, 25]: the offer booked beyond over the total 0.50013,
before it 0.49987 (the steady-state values; the train's spectrum
MEASURED ONLY beside).

---

## 8. What is agreed, and what goes to the owner

Nothing in this file is agreed yet: each section is checked by the
physicist and agreed or sent to the Boss. The points for the owner, from
this draft: (1) the crystal in the type I form of two crossed crystals
(1.2), since record 1830's rule and record 1831's word leave type II
with mirror arms impossible with an index per label alone; (2) the
splitter as a material layer (7.2).
