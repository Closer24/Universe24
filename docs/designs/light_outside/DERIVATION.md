# Light Outside from the board: every equation of light Inside, carried Outside by its own transformation to a named detector at a named place (the owner's order, 2026-09-22, about 05:55Z, as the Boss relayed it)

The Light Mathematician, 2026-09-22, on the Boss's order; a derivation
on paper in the shape of the click frame's sections 0 and 8 (the click
frame at e26c1f43, PR #769, not yet merged, cited by its line numbers
at that head and not edited); no code, no world file, no run; every number a closed
form or a registered reading labelled by its kind, DETECTOR or GAMEBOARD;
a number whose kind is not named is not a result. Every symbol is named
in English at its first use and its kind is shown by its type: a scalar
plain, a vector in bold lowercase (**p** the momentum vector, **D** the
direction vector), a matrix in bold uppercase (**G** the click's Gram
matrix, **E** the evaluation matrix). Every result is stated as matching
nature, never as being nature (Highlights 5.4, record 762). Sources on
`main` are cited by file and line at `main` 46cf692b (2026-09-22).

**The owner's order, as the Boss relayed it.** "Now we have equations
beneath the board and equations above the board. One can derive
equations of light. We also have an equation for how one passes from
above the board, with a click, to beneath the board; then one must use
the equations of light beneath the board; and when the light is
measured on the other side, one must put the equations in there. Let
the mathematician try to derive equations, existing or not, on light,
and see that it agrees with experiments, simply. Instead of running
experiments in code and seeing what happens, put them into formulas. We
are going to run new Inside formulas and take them Outside, but note: a
transformation for each formula, because one passes from inside the
board to above the board. And one thing to keep: consistency. If one
wants to measure in another place, the detector has to move to that
other place. The emitter and the click are a transformation formula
between place and place."

**The owner's later words, as the Boss relayed them, which shape this
file.** (i) The three formulas: "W = E'^2 + 3 p.p is the formula of ONE
STEP beneath the board. One needs the formula of one step ABOVE the
board (which Einstein and Newton already wrote), the formula of one step
beneath the board, and the conversion between them. That is all the
formulas we need: the step above, the step beneath, and the map between
them; then one can compute anything, light and every Inside phenomenon,
without code." (ii) The pattern of every phenomenon: Outside (the
measurement) down to Inside (the rows, the phases, the merge, the
evaluation) and back Outside (the click's counts against the reading),
because every measurement is Outside but the computation must enter
Inside; and interference, one slit, two slits and Mach-Zehnder shown by
formulas alone, what passes and what does not. (iii) Locality Outside:
"velocity in the real world is passing a click with information to the
neighbouring Node and receiving that packet at the neighbouring Node,
having in effect moved there; the passage is always Outside to Inside,
moving, and coming out again; in the real world the packet passes from
place to place, it cannot jump: a kind of locality also Outside." And
his rule for every derivation: modern algebra and limits first, a run
only after, if needed; a run Outside is a run of clicks under declared
conditions. Section 0 states the three formulas, section I adds (A3),
and every row of section II is written Outside first.

**THE CONSISTENCY RULE, stated at the head and obeyed in every row
below.** Every Outside formula carries its own transformation: it is
written as the map from the emitter's clicks at its place to the
detector's clicks at its place, and nothing else. A reading at another
place is a detector at that place: a formula that needs a number no
detector there reads (the tick, a row's position between clicks, a
Node's crowd where no body counts, the amount or the phase of one
record between its birth and its click) is not an Outside formula and is
labelled GAMEBOARD wherever it appears. The emitter and the click are
one transformation between place and place, and its place-to-place
form is the k-calculus of the click frame's section 0 (lines 94 to 165
there): the ratio of two detectors' counts between two clicks.

## 0. The three formulas (the Inside step, the Outside step, the conversion), and the frame

**THE THREE FORMULAS.** Everything below is three formulas and nothing
else: the step beneath the board, the step above it as physics wrote it,
and the map between them. Every Outside formula of section II is (2)
obtained from (1) by (3), checked against the register's reading by
kind.

**(1) THE INSIDE STEP: the one-interval update of a photon's row, in
closed form from the six verbs, with the engine's lines on `main`.** A
row's record is (its Node, its direction **D**, its age tau, its phase
phi on the circle of N steps, its amount a, its content, its label);
per interval, in this order:

- *The hop by the schedule* (the translation T of the position
  accumulator and the Euclidean division D): `acc <- acc + 2 S_1 Q`, and
  if `acc >= 2 T_D` the row crosses the Link `line_D[m mod S_1]` and `acc
  <- acc - 2 T_D`, m the Links made before it (`Flight.walk_step`,
  `src/event_universe/events/nature_beam.py` lines 1009 to 1021, on the
  one verb `by_drive_rows`); in closed form the Links made by the age tau
  are `m(tau) = floor((2 tau S_1 Q + T_D) / (2 T_D))` and the row is at
  the m(tau)-th point of the Bresenham line of **D** (BEAM_LAW lines 359
  to 402): at most one Link per interval, `T_D = isqrt(3 |D|_2^2 Q^2)`.
- *The age*: `tau <- tau + 1`, whole on the record.
- *The phase per age* (T on the circle): `phi <- phi + floor((tau + 1) n
  / d) - floor(tau n / d)` steps of N (`by_clock_rows`; nature_beam.py
  lines 3472 to 3476; BEAM_LAW lines 3733 to 3750), or `phase_per_link`
  per Link crossed in the integer form; at the click the phase is read at
  the exact time of the last Link, `phi = phase - floor(terms n / d) +
  floor(n made T_D / (d S_1 Q))` (`exact_phase`, nature_beam.py lines 621
  to 660; BEAM_LAW line 3743).
- *The spreading at a Node*: a re-emitter (an opening, a splitter, a
  mirror) re-emits the arrival on its declared fan or table, one row per
  direction with the declared weights and turns (the split, the declared
  matrix, and the permutation P; BEAM_LAW section 5, `rerelease`); the
  merge (the addition G in the group ring `Z[Z_N]`) of rows of one record
  at one Node and phase, with the cancel of antipodal pairs, `x^(N/2) =
  -1` (nature_beam.py lines 1446 to 1458; DERIVATIONS_BEAM 6.5).
- *The click as the event* (the evaluation E and the bilinear form B):
  when every row of the record has ended, each cell's weight is `f^T G
  f` on the record's phase-count vector **f** (`Layer.gram_form`,
  `src/event_universe/events/amplitude.py` line 788, `gram_entry` `G_jk =
  C_j C_k + S_j S_k`), the rungs `b_k = (2 W C_k + T) // (2 T)` (`rungs`,
  line 241; W the wheel, `C_k` the cumulative weight, T the total), the
  cell of the birth phase u by the comparison `2 T u + T <= 2 W C_k`
  (`cell_of`, line 275), one click, the offers deleted.
- *What W is here.* For a row of no content `E'_0 = 0` and `W = 3` **p**
  `.` **p** is constant along the flight (the label **p** is a rate of the
  translation, never changed by the walk): W is the step's invariant, not
  the step; its whole root `E' = isqrt(W)` is `sqrt 3 |p|`, the row's
  energy in whole units, consistent with the pace `p / E' = 1 / sqrt 3 =
  c` (17.6 M3; the click frame section 7 row 1, line 898, the unit chain
  `E^2 = E_0^2 + c^2 p^2`, `E' = E / c^2`, the 3 being `1 / c^2`).

**(2) THE OUTSIDE STEP: the equation of light above the board as
physics writes it, each named where it is.** Einstein's light postulate
(1905), one pace c for every source and every direction; Planck's `E = h
f` (1900) with Einstein's light quantum (1905) and de Broglie's `lambda =
h / p` (1924); Kepler's inverse square of the intensity (1604); Doppler's
shift (1842) and Einstein's one form for source and receiver, `sqrt((1 +
v) / (1 - v))`; Bradley's aberration (1729); Huygens' construction and
Young's fringes (1801) with Fraunhofer's single-opening envelope;
Grangier, Roger and Aspect's one click (1986) in Mach and Zehnder's
device (1891); Einstein's gravitational redshift (1911) and Hubble's law
(1929); Malus's `cos^2` (1809); Bell's inequality and the CHSH sum (1964,
1969). Each row's part (a) names its own; none is an input (section
III).

**(3) THE CONVERSION: one transformation per formula, the emitter-to-
click map** `Outside_A -> Inside -> the flight -> Inside -> Outside_B`
stated below in this section, whose place-to-place form is Bondi's
`k_AB`. The owner's pattern of reading, obeyed in every row of section
II: the Outside quantity first with its detector and its place, then the
Inside step that computes it, then the conversion back to the click's
counts and the register's reading.

**The frame.**

**The two words** (docs/TERMINOLOGY.md lines 344 to 357, the owner's
record 768; docs/HIGHLIGHTS.md line 402). Inside is inside the
GameBoard: the Nodes, the integer rows on them, the tick (the interval's
count), where no one measures; a number Inside is a GameBoard reading.
Outside is the game above the board: the detectors and their clicks
only, which is not reality but is claimed to represent it, the match
shown result by result; a click Outside is a detector reading. Only a
detector's reading is a measurement (Highlights line 360; AGENTS.md,
the measurement rule); an emitter is also a detector at its own Node
(Highlights line 381, record 569), so the lamp at the place A is the
first detector of every row below, and its births are its clicks.

**A detector's clock and a velocity Outside** (the click frame lines 17
to 40; Highlights lines 399 and 402). A detector D at a Node has its own
count `n_D`: its count of intervals stretched by what arrives at it, the
age wall's member at coefficient 1 (record 709; `core.integer.age_wall`),
so that at an empty Node `n_D` advances one per interval and in a crowd
`a_tau` (the age moment, the sum over the rays at the Node of amount
times age) it advances at the rate `1 / (1 + a_tau n / d)`, `[n, d]` the
world's suspension pair; the detector never reads the tick, only `n_D`.
A click is the event of receiving a packet, stamped with `n_D`: the
triple (the Node, `n_D` at the arrival, what arrived), and what arrived
is the row's own record (its content, its momentum label, its phase, its
age since birth). A detector's clock Outside is a pulse and its return
(record 768): what it emits and receives back, counted on its own record.
A velocity Outside is Nodes apart over counts apart between two clicks of
neighbouring detectors (record 723: a moving detector is a passage of
clicks between Nodes; there is no velocity Outside but a series of clicks
with information), so a velocity is a ratio of two integers.

**The one map of every row.** Emitter at the place A (a lamp, a
detector at its own Node), detector at the place B. Each row of section
II is the composition

    Outside_A  ->  Inside  ->  the flight  ->  Inside  ->  Outside_B,

with these five arrows, each one of the law's operations:

1. `Outside_A -> Inside`, the birth: at A's own self-creation the lamp
   pays `h_q s` of content per unit born (`h_q` the family's quantum, s
   the lamp's turn in phase steps per self-creation), stamps its phase on
   the row and sends one row per direction of its fan (docs/BEAM_LAW.md
   lines 359 to 402 and 797 to 830; docs/DERIVATIONS_BEAM.md 6.4, lines
   1499 to 1555). What passes Inside is the row's record: an amount, a
   phase, a direction, an age 0. What stays Outside is A's count `n_A`
   at the birth.
2. `Inside`, the record: the six verbs act on it and nothing reads it.
3. `The flight`: the translation of the row's position accumulator by
   the direction's constant rate against the direction's wall (BEAM_LAW
   lines 359 to 402), and the translation of its phase accumulator by the
   family's declared rate per interval of age (BEAM_LAW lines 3733 to
   3750); the flight reads nothing of the crowd (P9, DERIVATIONS_BEAM
   24.1 row 7 at line 6988 and section 27 at line 7948).
4. `Inside -> Outside_B`, the click: the detector at B reads the
   arrival's record through its declared reading (BEAM_LAW lines 774 to
   830: the threshold, the `wave` pointer, the record `X^2 + Y^2`), and
   under the one click of a record (BEAM_LAW note 37 (x), line 2849; the
   ladder) one cell of one detector clicks once per record, its weight
   the click's bilinear form (DERIVATIONS_BEAM 6.7, line 1813), the
   probability of the cell within `1 / (2 N)` of Born's (23.2, line
   6762). What passes Outside is the click's triple; what never passes
   singly is the amount and the phase of one record (the click frame lines
   908 to 923, its second fact).
5. `Outside_B`, the reading: a ratio or a difference of counts at clicks,
   B's `n_B` against A's `n_A` carried on the record (the lamp's ordinal
   and wheel value and the row's age since; record 709), never the tick.

**The place-to-place form.** Between A and B the whole map is one
number per pair of clicks, Bondi's factor of the click frame's section 0
(lines 94 to 165) and section 2: `k_AB`, the count B reads between two
arrivals over the count A read between the two births. Under the law
as it stands, with `r_A` and `r_B` the two detectors' own rates against
the tick (1 at an empty Node, `1 / (1 + a_tau n / d)` in a crowd) and v
the velocity of A away from B as a fraction of the direction's pace c
(Nodes apart over counts apart),

    k_AB = (r_B / r_A) x (1 + v)      (A moving away, B at rest in the lattice's frame: the source's Doppler, DERIVATIONS_BEAM 2.5),
    k_AB = (r_B / r_A) / (1 - v)      (B moving away, A at rest: the receiver's count under the crossing rule, DERIVATIONS_BEAM 2.2 and 9.3),

and the round trip `k_AB k_BA = (1 + v) / (1 - v)` is free of every r
(the click frame lines 94 to 165: the boost is r-free, the dilation
carries r alone). Every row below is one instance of `k_AB` or of a
count at B alone; the rows differ in which operation of the flight the
count reads. Where nature's form has a root (`gamma`, the Lorentz
factor) the law's rows have `r = 1`, and the difference is the click
theorem's (A2), which the law's rows do not meet (the click frame lines
54 to 93 and 185 to 202): stated in each row as FAIL where the register
has read it, never hidden.

## I. The assumptions, each in the law's own words with its source line on `main`

Nine lines of the law and the two assumptions of the click frame; every
one is on `main` at 46cf692b except (A1) and (A2), which are the click
frame's (PR #769) and are used only where a row says so. Nothing of
Maxwell and nothing of optics is among them (section III).

- **(L1) The flight blind, P9.** "for a direction **v** = (a, b, c) with
  S_1 = |a| + |b| + |c| (its Manhattan length) and Q = 64 (the label's
  scale), `T_d = isqrt(3 (a^2 + b^2 + c^2) Q^2)` (the direction's
  resolution); the Manhattan steps made by age tau are `m(tau) = (2 tau
  S_1 Q + T_d) // (2 T_d)` and the ray at age tau is at the m(tau)-th
  point of the Bresenham line of **v**"; "at most one Link per interval
  in every direction, Euclidean speed exactly 1 / sqrt 3 for every
  direction" (BEAM_LAW lines 359 to 402). "A ray's rate never changes
  over its flight" (the same lines): the flight reads nothing of the
  crowd and nothing of the row's phase. Its status: a postulate chosen
  among few, not a theorem of the six verbs (DERIVATIONS_BEAM section 27,
  lines 7948 to 8200, REFUTED as a theorem; 24.1 row 7, line 6985).
- **(L2) `T_D` per direction and c on the body diagonal.** `T_D =
  isqrt(3 |D|^2 Q^2)` with `S_1 Q <= T_D` by Cauchy-Schwarz, equality on
  the body diagonals where three Manhattan steps make one Euclidean
  `sqrt 3`: `c = 1 / sqrt 3` Links per interval is the operator norm of
  the flight, the largest isotropic pace at which no direction crosses
  two Links in one interval (DERIVATIONS_BEAM 13.2 (a), lines 3588 to
  3625; 24.1 rows 9 and 10, lines 6990 to 6991;
  docs/designs/light_speed/FORM.md section 1, lines 15 to 37). The
  heading's rational is `Q / T_h = 64 / 110 = 32 / 55` (DERIVATIONS_BEAM
  2.1, lines 634 to 654).
- **(L3) The phase per age.** "the pair form of `phase_per_link`, n / d
  steps per interval of age, turns by floor(age x n / d), the phase of the
  whole intervals", and the exact phase at the click "phi = phase -
  floor(terms n / d) + floor(n made T_d / (d S_1 Q)) (mod N)" (BEAM_LAW
  lines 3733 to 3750): the row's phase is a second accumulator, a
  translation at the constant rate `n / d` on the circle of N steps, read
  at the click at the exact time of the last Link. And: "the phase per
  age of a row ... is never a member, since a stretched phase per age
  would redshift light" (BEAM_LAW lines 608 to 609): the age wall does
  not touch a row's phase in flight.
- **(L4) The Planck map with the circle's N.** "A lamp of quantum h whose
  clock turns s phase steps per self-creation ... pays `h s` per unit
  born ... Its frequency is `f = s / N` cycles per self-creation, so the
  content of one unit of light is `E = h s = (h N) f`" (DERIVATIONS_BEAM
  6.4, lines 1499 to 1512); the dictionary `h_A = h_q N`, `h = h_q N =
  h_A`, `hbar = h / (2 pi)`, `E = h f`, `lambda = h / p`, `k = 2 pi p / h`
  (6.4 lines 1521 to 1555; 24.1 row 25, line 7006: a calibration, the
  value of h an input). "No rule makes the content of a row follow its
  frequency in flight" (6.4, lines 1523 to 1524).
- **(L5) The spreading over the six Ports.** "On a beam the flow per Node
  is `amount x u_d`, the same at every Node of the digital line: the
  field along a beam is `1 / r^0`, and off every beam it is 0 ... The
  inverse square is the density of beams over a shell": the shell mean `q
  Q / N(r) -> q Q / (4 pi r^2)` in space with the ripple of `N(r)`, the
  lattice's count of Nodes on a shell (DERIVATIONS_BEAM 3.2, lines 874 to
  937; 5.1, lines 1168 to 1211: the presence `q dwell / (4 pi r^2)`, the
  age moment `q dwell / (4 pi c r)`). This is the arithmetic of six
  Ports and a fan of K directions, not a law (the click frame line 978,
  its (M)).
- **(L6) Born at the click, the conversion's line.** The `wave` reading:
  "the coherent pointer over the whole set `(X, Y) = (sum A_u C[phase_u],
  sum A_u S[phase_u])` ... and the record `X^2 + Y^2`"; "it is the one
  imported law of physics in the engine, intensity = the square of the
  summed amplitudes" (BEAM_LAW lines 797 to 830). Its form: the click's
  weight is the one bilinear form `f^T G f` on the record's integer
  phase-count vector **f**, **G** = **E**^T **E** the Gram matrix of the
  tables C and S at the scale 256 (DERIVATIONS_BEAM 6.7, lines 1813 to
  1860; 6.5, the lattice Gleason, line 1556: rotation invariance,
  conservation at the balanced splitter and non-negativity force a
  positive quadratic form, Born's member `c_1 = 1` the one imported
  member, 24.1 row 12, line 6993); Born's `|psi|^2` "holds AT THE CLICK
  as the cell's probability to within `1 / (2 N)`, and nowhere between
  clicks" (23.2, lines 6791 to 6797). One record, one click: the ladder
  chooses one cell by the birth phase u and deletes the record's offers
  in the same interval (BEAM_LAW note 37 (x), line 2849; EXPERIMENTS E15,
  line 9836). In the click frame's table this is the row "the click's
  bilinear form" (line 903): the conversion's (A2) at the click.
- **(L7) The crossing rule.** "a row and a body meet ONCE, at the crossing
  of their world lines" (BEAM_LAW note 48, lines 530 to 532;
  DERIVATIONS_BEAM 2.2, lines 655 to 706, and 9.3, lines 2221 to 2241;
  24.1 row 22, line 7003: DERIVED given the flight and the drive). Its
  count on an axis: `1 + v / c` toward the lamp, `1 - v / c` away, 1
  transverse, exact over whole Links and within one row otherwise
  (`tests/test_crossing.py`, the pinned counts).
- **(L8) The age wall at coefficient 1 on every count.** "a count at the
  rate `rate` against the wall `wall` becomes the count at `rate x d`
  against `wall x (d + a_tau n)`" (`core.integer.age_wall`; the click
  frame's (N2), lines 953 to 960): a body's self-creations, a lamp's
  births and a detector's own count are all stretched by the crowd at
  their Node at coefficient 1 (record 709, Highlights line 399); the
  row's flight and phase are not (L1, L3). The clock's word is the age
  moment (record 394).
- **(L9) The two-state label and its rotation.** "linear polarisation is
  the two-label record with a relative phase, the polariser its `rotate`
  and the label click" (BEAM_LAW lines 3088 to 3089; the hand, the
  pseudoscalar of the 48): a row carries a label bit, a declared setting
  rotates it (the permutation and the declared matrix, two of the six
  verbs), and the which-path `read` at a `sum` set clicks it
  (docs/designs/malus/NOTE.md, its verdict line: built from the entries
  in force).
- **(A1), (A2), the click frame's, used where a row says so.** "(A1) A
  click is the passage of information from Node to Node, at most one Node
  per interval: c is the unit, the same in every family, and nothing
  passes faster. (A2) A click's content is an amplitude with a phase that
  splits each interval between staying and hopping, the mass the staying
  share: the packet that passes is converted by its amplitudes" (the
  click frame lines 41 to 53). Every row below needs (A1) at the click
  (one Node per interval, the count's ratio the velocity); (A2) enters
  only through Born at the click (L6), which is (A2)'s form at the one
  place a record is read, and through no row's dynamics: the law's rows
  hop whole (the click frame lines 185 to 202), a fact stated and not
  hidden.
- **(A3) Locality Outside (the owner's word, as the Boss relayed it).**
  (A1) read from above: every Outside passage of light is a chain of
  clicks between neighbouring places, each click the receipt at one
  place of a packet that went Inside at the neighbouring place ("the
  passage is always Outside to Inside, moving, and coming out again; the
  packet passes from place to place, it cannot jump"), so the Outside
  inherits the Inside's locality (LOCALITY-1) through the conversion. It
  forbids three things: a velocity Outside above one Node per interval
  (c the bound of every ratio of counts), a jump (a click at a place with
  no click at a neighbouring place before it), and a reading at a place
  no chain of clicks reaches. Every row below obeys it and says so where
  it matters: the arrival count (II.1), the aberration (II.5), the
  fringes' paths (II.6). And the owner's rule for every derivation:
  modern algebra and limits first, a run only after, if needed; a run
  Outside is a run of clicks under declared conditions.

## II. The theorems: each formula of light Inside, its transformation, its Outside form, its order, its inverse, its reading

Every row has four parts in the owner's order, Outside, Inside, Outside:
(a) the Outside quantity, the measurement as physics writes it (the
Outside step, named) with its NAMED detector at its NAMED place; (b) the
Inside step that computes it, a GameBoard quantity from the six verbs
with its source; (c) the conversion back to the click's counts: the map
of section 0 written for the emitter at A and the detector at B with the
k-calculus factor where one applies, the Outside formula it gives (a
ratio or difference of counts at clicks), its order (rung 1 exact on the
GameBoard within the accumulator's remainder, rung 2 a limit: the shell
mean, the fan of every direction, `Q -> infinity`, `v << c`; "within the
tables' rounding" where the click's scale 256 enters) and its inverse
where one exists; (d) the registered reading on the Outside side, by
kind, a pin met written MET and a pin missed written FAIL. The verdict
of each row is one of SHOWN (it comes out algebraically under section
I's lines at the rung named), MEASURED ONLY (no closed form Outside; a
run rises Outside), NEITHER (no closed form and no reading), FAIL (a
registered pin missed, or nature's form missed where the register has
read it); the table of section IV collects them.

### II.1 The speed of light Outside: the arrival count over the Euclidean distance

**(a) Outside, the measurement and its detector.** The speed of light as physics writes it: Einstein's light postulate
(1905), one pace c for every source and every direction, read as the
distance between two places over the time a pulse takes between them,
in practice by a round trip (Fizeau's, Michelson's). Here: the lamp A at
the Node `x_A` and the detector B at the Node `x_B = x_A + j` **D**, both
at rest at empty Nodes, `L = j |D|_2` Links apart (Nodes apart, an
Outside number); the quantity read is `c_D = L` over the count between
A's birth and B's click (one way, the row's age on the record) or over
half of A's own count between its pulse and its return (two way, record
768). By (A3) the pulse is a chain of clicks Node to Node, at most one
per interval, so no reading of c above one Node per count exists: `c_D
<= 1` by the count, and `1 / sqrt 3` is what the chain's Euclidean
progress per count reads.

**(b) Inside, the step that computes it.** On the direction **D** (an integer vector with the
Manhattan length `S_1 = |D|_1` and the Euclidean length `|D|_2`) the row's
Links made by the age tau are `m_D(tau) = floor((2 tau S_1 Q + T_D) / (2
T_D))`, `T_D = isqrt(3 |D|_2^2 Q^2)`, so its k-th Link falls at the age
`tau_k = ceil((2 k - 1) T_D / (2 S_1 Q))` (L1, L2; DERIVATIONS_BEAM 11.1,
line 2495; EXPERIMENTS series Q, line 4547). After `j` periods of the
line (`j S_1` Links) the row's Euclidean displacement is `j |D|_2` Links
at the age `tau(j S_1) = ceil((2 j S_1 - 1) T_D / (2 S_1 Q))`, which is
`j T_D / Q` within one interval. The Manhattan pace is `S_1 Q / T_D` Links
per interval, the Euclidean pace `Q |D|_2 / T_D`.

**(c) The conversion, back to the click's counts.** The lamp A at the Node `x_A`, at rest at an
empty Node (`r_A = 1`). The detector B at the Node `x_B = x_A + j` **D**,
at rest at an empty Node (`r_B = 1`), on A's digital line, `L = j |D|_2`
Links from A: Nodes apart, an Outside number (the click frame line 33).
Two readings, both Outside:

- *The one-way count.* A births one row on **D** at its count `n_A`
  (Outside_A -> Inside: the row at age 0 carries A's ordinal on its
  record); the flight (L1); the click at B reads what arrived, and the
  row's age since birth is on its record (the click's triple; record
  709: a far clock is read only by what it sent, the lamp's ordinal and
  the row's age since). So B reads `tau(j S_1)` on the click without
  reading the tick and without any synchronisation of `n_A` and `n_B`:
  the row is the pulse and carries its own clock.
- *The pulse and its return* (record 768, the strict form). B is
  declared a re-emitter (`rerelease`; BEAM_LAW section 5; the isometry
  re-emits the arrival at age 0 on `-`**D** by the tables, DERIVATIONS_BEAM
  27 (R3), lines 8015 to 8030): the row returns to A on `-`**D**, whose
  `T_D` is the same (`T_D` depends on `|D|_2^2` alone), and A clicks its
  own row back at its count `n_A + 2 tau(j S_1)` within two intervals
  (each leg's ceiling). Nothing but A's own count enters: A emits and
  receives, the round trip's count is its clock.

*The Outside formula.* The speed of light on **D** read at B, or by A's round
trip, in Links per count:

    c_D(Outside) = L / tau(j S_1) = j |D|_2 / ceil((2 j S_1 - 1) T_D / (2 S_1 Q))  ->  Q |D|_2 / T_D   as j grows,
    and by the round trip  c_D = 2 L / (n_A(return) - n_A(birth)),   the same number within one interval per leg.

Its values at Q = 64 (the register's grain), a formula's value, GAMEBOARD
by kind until a detector reads them:

| **D** | `T_D` | `c_D = Q |D|_2 / T_D` Links per interval | `1 / c_D^2 = (T_D / (Q |D|_2))^2` |
| --- | --- | --- | --- |
| the heading (1, 0, 0) | 110 | 64 / 110 = 32 / 55 = 0.5818 | 2.954 |
| the face diagonal (1, 1, 0) | 156 | 64 sqrt 2 / 156 = 0.5802 | 2.971 |
| the body diagonal (1, 1, 1) | 192 | 64 sqrt 3 / 192 = 1 / sqrt 3 = 0.5774 | 3.000 |

The anisotropy is the isqrt's rounding of `T_D` above `sqrt 3 |D|_2 Q`:
`(c_D - 1 / sqrt 3) / (1 / sqrt 3) = 7.6 x 10^-3` at most (the heading)
and 0 on the body diagonal, bounded by `1 / (sqrt 3 Q - 1)` (NATURE row
5a and its note, lines 102 and 284 to 312); the isotropic limit is `Q ->
infinity`, `c_D -> 1 / sqrt 3` on every direction, the factor 3 of Eq.
14 being that limit's `1 / c^2` (the click frame section 7, lines 777 to
806: the 3 is `(|D|_1 / |D|_2)^2` on the body diagonal, 9 / 3). The
isotropy is (L2)'s second axiom and the equality at the supremum its
third statement (13.2 (a)): SHOWN as a consequence of the flight table,
which is declared; not derived from the six verbs alone (section 27).

*The order.* Rung 1 in the count: exact within one interval on the
one-way reading and within two on the round trip (the ceiling per leg);
the pace exact in the mean over a period of the line. Rung 2 in the
isotropy: `Q -> infinity`.

*The inverse.* L from the count and the pace, within one Link: `L =
c_D x tau` on a direction the detector's face names (the click's
momentum label gives **D**).

**(d) The register, Outside.** Series Q, c measured behind a detector
(EXPERIMENTS lines 4547 to 4613; DETECTOR): one lamp of 290 rows on the
fan of the 290 primitive directions within `|a| + |b| + |c| <= 6` in an
open cube of half-width 32, every row leaving through an open face (a
face is a detector, an escape a click): 290 clicks of 290 at the derived
tick, Node and face, none differing; the six axes at the age 56 (33
Links, the pace 33 / 56 = 0.5893), the twelve face diagonals at 79 (65
Manhattan Links, 0.5819), the eight body diagonals at 97 (97 Manhattan
Links, 0.5774); over the fan the pace min 0.5718, max 0.5893, mean
0.5810 against the asymptotic 0.5774 to 0.5818: MET on every class, the
one-way form of (c) with the row's age on the record. Series T
(EXPERIMENTS lines 6737 to 6835; DETECTOR): the lamp's light read at x =
110 from x = 10 on the heading, "the age read 172 in every world (the
flight of 100 Links)": `172 / 100 = 1.72` counts per Link against `T_h /
Q = 110 / 64 = 1.719`, within `1 / 172`: MET (and the same 172 at
series X, line 6946). The round trip of (b) is not registered as a
run: the pulse-and-return world of record 768 (`examples/events/reader_clock`, the clock audit's strict form) reads a
clock at rest, not a length; the two-way c after a detector is NOT MADE,
its integer pinned here from (c): on the heading over `L = 32` Links,
`2 tau(32) = 2 x ceil(63 x 110 / 128) = 2 x 55 = 110` counts, `c = 64 /
110` (GAMEBOARD until run). Against nature: the anisotropy `7.6 x 10^-3`
at Q = 64 against the bound `10^-17` (NATURE 5a; DERIVATIONS_BEAM 24.3
row 5, line 7067): FAIL at the register's grain, a bound on the grain, `Q
>= 5.8 x 10^16`; the isotropic limit's form (one c on every direction)
matches nature's. And the one-way pace relative to a moving detector is
`c -+ v`, Galilean (DERIVATIONS_BEAM 4.2, lines 1061 to 1082): the
lattice's frame is preferred by a one-way count, which nature's row 5b
(the two arms of a moving laboratory) reads as FAIL at `beta^2 / 2` on
`main` (NATURE line 103; 24.3 row 6), the same finding as II.4's
second order.

**Verdict.** SHOWN, rung 1 in the count and rung 2 in the isotropy; MET
on Q (290 of 290) and T (172); FAIL against nature's isotropy bound at
the register's grain, a bound on Q.

### II.2 The photon's energy and wavelength at a click: `E = h f`, `lambda = h / p`

**(a) Outside, the measurement and its detector.** Planck's `E = h f` (1900) with Einstein's light quantum (1905): the
energy a detector takes per click is Planck's constant times the
frequency; de Broglie's `lambda = h / p` (1924). Here: the lamp A at rest
at an empty Node; the detector B at rest at an empty Node, L Links from
A on the row's line, declared `measure`; B reads two numbers, the content
of one click and the frequency, `1 + z` as the inverse slope of the birth
ordinal against its own count.

**(b) Inside, the step that computes it.** The lamp's turn s phase steps per self-creation and its
cost `h_q s` per unit born (L4); the row's phase per interval of age `n /
d` steps of the circle of N (L3), so the row's frequency in the lattice's
frame is `f = n / (d N)` cycles per interval and its energy `E = h_q n /
d = (h_q N) f`; its wavelength, the Links the row makes in one turn of
its phase, `lambda = c_D N d / n` Links (`N d / n` intervals at `c_D`
Links per interval; DERIVATIONS_BEAM 7.1, line 1955); and the dictionary
`lambda = h_A / p`, `p = E / c` for a row of no content, which equals `c
N d / n` if and only if `h_A = h_q N` (6.4, lines 1526 to 1555).

**(c) The conversion, back to the click's counts.** The lamp A at rest at an empty Node
(Outside_A -> Inside: the birth pays `h_q s` and stamps the phase; the
lamp's own births are its clicks, DETECTOR at A, its stall when the
content falls below the cost being the register's reading of the cost
per unit). The flight: the phase accumulator translates at `n / d` per
interval of age and the content is a translation (L3, L4: nothing of the
content follows the frequency in flight). The detector B at rest at an
empty Node, L Links from A on the row's line, declared `measure`
(Inside -> Outside_B: the click's content line and the click's phase).
Two counts at B: the content per click, and the arrivals' rate against
`n_B`, `1 + z = ` the inverse slope of the birth ordinal against the
click's own count (series T's method), which for A and B at rest with
`r_A = r_B = 1` is exactly 1 (`k_AB = 1`).

*The Outside formula.*

    E_B = the content of one click = h_q s = h f_A     (exact, an identity of the release carried whole by the flight),
    f_B = f_A x k_AB                                     (the frequency B counts: the lamp's turn per B's count, k_AB = 1 at rest),
    lambda_B = c_D N d / n = h / p                        (read Outside only as a fringe spacing, II.6, or as the arrival's phase against the ordinal).

So `E = h f` Outside is `E_B = h f_B / k_AB`: at rest the click's content
is Planck's constant times the frequency B counts, with `h = h_q N`; in
motion or in a crowd the content stays the birth's while the counted
frequency moves by `k_AB` (II.4, II.8): the law carries no rule by which
a click's content follows the frequency read (L4's last line), a fact
for the far lamp (NATURE 11a, II.3 (d)).

*The order.* Rung 1: the content exact at every click (the books'
identity, GAMEBOARD as a check of the record; the click's content
DETECTOR); the frequency within the count's grain (one row over the
window); the wavelength exact in the mean of the flight's accumulator
(the staircase one Link, 7.1's list item 3).

*The inverse.* `f_A` from the content per click and h; `n / d` from the
frequency counted and N; p from `lambda` and h (the massive row's pin,
23.3, line 6831).

**(d) The register, Outside.** The cost per unit at the emitter (DETECTOR,
the lamp's own births): the Bell lamps of content `K + 2` "paying 2 per
birth, stalls once, at tick 4: 159 births in 160" (the bell README;
DERIVATIONS_BEAM 6.4, lines 1513 to 1517); the L1 lamp of content `2^20`
at `K = 2^20` turning 1 per self-creation and paying 1 per unit, its
clock stalling once at tick 2 (EXPERIMENTS line 3929, issue #533): MET
as `E = h s` at the birth. The content per click at B: every face click
of series Q carries its birth's content (290 of 290, the escaped
momentum `(0, 0, 0)`, the books balanced; DETECTOR the clicks, GAMEBOARD
the books) and the far lamp's content per click is pinned at 5, the
birth's, at every distance (NATURE 11a, `far_lamp_map.out`, not run). The
wavelength Outside: L2's `lambda = 8 x 32 / 55 = 4.654` Links read as the
fringe spacing (II.6, MET within the pixel); the frequency Outside: series
T's controls `1 + z = 1.0000` exactly at rest (DETECTOR, MET), series X's
three controls 1.0000 (line 6941). The identity `lambda = h / p` on a
row that carries a momentum: the pin `256 / 55 = 4.6545` Links of 23.3
(line 6831) for the massive row's fringes, NOT RUN (the massive row's
two-slit world not built).

**Verdict.** SHOWN, rung 1 (an identity of the release and of the
calibration `h_A = h_q N`); MET at the emitter (the stall) and at B (the
content per click, the frequency 1.0000 at rest, the wavelength through
II.6); `lambda = h / p` on a massive row NOT RUN. What matches nature:
the form `E = h f`, `lambda = h / p`; the value of h is an input (24.1
row 18).

### II.3 The intensity of a source: `1 / r^2` in the shell mean, `1 / r^0` on a beam

**(a) Outside, the measurement and its detector.** The inverse square of a source's intensity, Kepler's photometric law
(1604): the flux through a detector of area `A_det` at the distance r is
`L_source A_det / (4 pi r^2)`. Here: the lamp A at rest at an empty Node;
a shell of detectors `B_r`, one detector of one Node at every Node of
the shell at the distance r (a reading at another place is a detector at
that place), each counting its clicks per its own count; the quantity
read is the click rate per detector and its sum over the shell.

**(b) Inside, the step that computes it.** A lamp releasing q rows per self-creation on a fan of K
directions; on each digital line the row arrives at every Node of the
line, so the flow along a beam is `1 / r^0` and off every beam 0; the
shell mean over the `N(r)` Nodes of the shell at the distance r is `q K
/ N(r)` arrivals per interval per Node, `N(r) -> 4 pi r^2` in space,
`2 pi r` on the plane, with the ripple of Gauss's circle problem (L5;
DERIVATIONS_BEAM 3.2, lines 874 to 937).

**(c) The conversion, back to the click's counts.** The lamp A at rest at an empty Node, its
release q per self-creation (`r_A = 1`). The detectors: a shell of
detectors `B_r`, one detector of one Node at every Node of the shell at
the distance r (a reading at another place is a detector at that place:
the intensity at r is read by the detectors AT r and by nothing else),
each declared `measure` and counting its clicks per its own count (`r_B
= 1`). Outside_A -> Inside: the split of the birth over the fan (the
declared matrix, one row per direction, the multiplicity K). The flight
(L1). Inside -> Outside_B: each click carries the birth's content (II.2).

*The Outside formula.* Per detector on a beam, the click rate is q per count
(the beam does not dilute); per detector off every beam, 0; and over the
shell of detectors,

    sum over the shell of the click rates = q K per count, exactly (every row leaves the shell once: the count is conserved),
    the mean click rate per detector of the shell = q K / N(r)  ->  q K / (4 pi r^2),
    the intensity (content per count per detector) = h_q s x q K / (4 pi r^2)   (with II.2's content per click).

A detector of `A_det` Nodes (a face of the shell) reads `A_det q K / (4
pi r^2)` clicks per count in the limit of every direction (K to infinity
at fixed r with the angle weights: Huygens' fan, DERIVATIONS_BEAM 3.2,
its last paragraph), the inverse square; and at any finite K a single
Node reads a beam or nothing (rung 3 on a fan).

*The order.* The conservation of the count over a closed shell: rung 1,
exact. The `1 / r^2`: rung 2, the shell mean, with the finite-r ripple
of `N(r)` (no closed form, MEASURED ONLY where read). The `1 / r^0` on a
beam: rung 1, exact.

*The inverse.* r from the mean click rate over the shell, in the limit;
none per Node.

**(d) The register, Outside.** The conservation over a closed surface:
series Q's 290 clicks of 290 at the faces of the cube, none elsewhere
(DETECTOR, MET, rung 1). The beam's `1 / r^0` after a detector: series
T's presence word, a lamp's clock at 3 and at 6 Links on the two headings
of two crowds reading `1 + z = 1.3000` at both distances (DETECTOR,
lines 6737 to 6835; NATURE 12's presence word: "the clock reads the
flux, flat along the beam"): MET as the law's `1 / r^0` on a beam, which
is FAIL against nature's `1 / r` potential for a clock (NATURE row 12,
the presence word 1.000 against 2.00) and no reading of light's
intensity. The presence's rise toward a shell of sources: series X's
presence word inside, `k(2) / k(4) = 0.8390` against the pin 0.839989
(DETECTOR, MET, "NOT flat, the FAIL the design expected" for a
potential; the flux's form for the intensity, lines 6835 to 6970). The
`1 / r^2` at two radii after a detector of light: NOT MADE (the far
lamp's brightness pinned and not run, NATURE 11a, line 112; the click
frame's section 8 says the same of the fall's inverse square, line 1101);
series C's `count x r / q` and series E's `k_s r^2 = 41.5` are GAMEBOARD
(the probes' view) and are not compared. The luminosity against z of
G2's stars, `1 / (1 + z)` within 5 percent, 648 of 648 (DETECTOR, MET,
line 2508), reads the count's stretch of II.8 at one distance, not the
inverse square.

**Verdict.** SHOWN, rung 2 (the shell mean; rung 1 on a beam and for the
conservation); MET on Q (the conservation) and T (the beam); the decisive
Outside reading at two radii NOT MADE; the finite-r ripple MEASURED ONLY.

### II.4 The Doppler shift of a moving detector and of a moving lamp

**(a) Outside, the measurement and its detector.** Doppler's shift (1842) and Einstein's one form for source and receiver
(1905), `1 + z = sqrt((1 + v) / (1 - v))`: the frequency read at a
detector against the emitter's own, as a function of their relative
velocity. Here, two named cases: (i) the lamp A at rest on the x axis
and the detector B a passage of clicks along the axis at `v = 1 / k`
(record 723; by (A3) a chain of detectors `B_1, B_2, ...` at consecutive
Nodes, each at rest, the click's information passing one Node every k
counts, its velocity Nodes apart over counts apart); (ii) the lamp A
carried by a body thrown at v and the detector B at rest. The quantity
read: `1 + z = k_AB`, B's count between two arrivals over A's count
between the two births.

**(b) Inside, the step that computes it.** The crossing rule's count on an axis: a body stepping one
Link per k intervals toward a lamp at rest meets `k + T_h / Q = k + 55 /
32` rows per k intervals, `k - 55 / 32` away, exactly over whole Links
and within one row otherwise (L7; DERIVATIONS_BEAM 2.2, lines 655 to
706); a lamp thrown at v releases one row per self-creation and its rows
stand `c - v` Links apart ahead and `c + v` behind (2.5, lines 787 to
811); the transverse count exactly 1 (2.3); on a fan direction the
Manhattan flux `1 + v T_d / (Q S_1)` (2.4, lines 722 to 786).

**(c) The conversion, back to the click's counts.** Two named cases.

- *The moving detector, a passage of clicks* (record 723). The lamp A at
  rest at an empty Node on the x axis (`r_A = 1`). The detector B is a
  chain of detectors `B_1, B_2, ...` at consecutive Nodes on the axis,
  each at rest at an empty Node; "B moves at `v = 1 / k`" means the
  click's information passes from `B_i` to `B_(i+1)` every k counts (a
  body of content M carrying the record, stepping by the drive, is the
  law's realisation: `v = |p| / (Q S M + |p|)`, 2.1 line 650); the
  velocity Outside is the Nodes apart over the counts apart between the
  clicks of `B_i` and `B_(i+1)`. What the chain counts is the crossing
  count (L7), and B's own count `n_B` advances one per interval (`r_B =
  1`, the law: no rule slows a body's count by its speed, 4.3, line
  1083). Outside_A -> Inside the births at A's count; the flight; Inside
  -> Outside_B the crossings.
- *The moving lamp.* The lamp A carried by a body thrown at v (its births
  at its own self-creations, one per interval under the law, `r_A = 1`);
  the detector B at rest at an empty Node (`r_B = 1`); the rows' spacing
  at B is the source's Doppler (2.5).

*The Outside formula.* With `1 + z = k_AB`, the count B reads between two
arrivals over the count A read between the two births, v as a fraction of
the axis's pace `c = Q / T_h`:

    the moving detector:   1 + z = 1 / (1 -+ v)     (receding -, approaching +: the rows per B's count are 1 -+ v, the receiver's count),
    the moving lamp:       1 + z = 1 +- v           (receding +, approaching -: the source's spacing),
    the transverse:        1 + z = 1                (exactly),
    the round trip:        k_AB k_BA = (1 + v) / (1 - v)   (r-free: Lorentz's, the click frame lines 94 to 165).

The two one-way forms differ at second order, `(1 + v) / (1 / (1 - v)) =
1 - v^2`, and nature has one form for both, `sqrt((1 + v) / (1 - v)) =
gamma (1 + v)` (gamma the Lorentz factor): the law's forms agree with
nature's at first order in v and differ at `v^2 / 2` (DERIVATIONS_BEAM
2.6, lines 812 to 826; the click theorem: the missing (A2) is the r of
the moving record, `r = 1` on the law against `sqrt(1 - v^2)`). Under
covariant-readings-v1, an identity beside the law with its own name (not
the law), the moving lamp's `r = E'_0 / E'` gives `gamma (1 + beta)` (the
click frame section 7, line 900).

*The order.* Rung 1 within one row over a window (exact over whole
Links) for the counts; the forms exact in the limit of many intervals;
the first order in v matching nature, the second order the law's own.

*The inverse.* `v = z` for the moving lamp; `v = z / (1 + z)` for the
moving detector; from the round trip `v = (k^2 - 1) / (k^2 + 1)`, `k =
sqrt(k_AB k_BA)`.

**(d) The register, Outside.** The moving detector: the crossing rule's
counts on the experimenter's streams, the reader's own record (DETECTOR,
the body's count of what it meets): 45 rows in 32 intervals toward at k =
4 (the formula's 45.75, the boundary row), 58 in 48 at k = 8 (58.31), 19
in 32 and 38 in 48 away (18.25, 37.69), 183 = 128 + 55 and 311 = 256 + 55
over 32 Links toward (exact), 48 in 48 at rest (DERIVATIONS_BEAM 2.2's
table; `tests/test_crossing.py`; BEAM_LAW note 48): MET, `1 +- v / c`
with `c = 32 / 55`. The moving lamp: G2's `coasting_none`, the stars
thrown from one point with gravity off, the detector at the centre
reading each star's `1 + z = 1 + v / c`: `s_my1` declared `v / c = 0.1146`
reads z = 0.1146, `s_pz2` 0.2483 reads 0.2478, `s_mz2` 0.2674 reads
0.2636, `s_px1` 0.0573 reads 0.0611, every star within 0.004 of `v / c`
(DETECTOR, EXPERIMENTS lines 2361 to 2548; DERIVATIONS_BEAM 2.5): MET on
the law's form. Against nature (NATURE row 4b, line 101, and its note,
lines 268 to 283): `s_mz2` at beta 0.2674 reads z = 0.2636 against
nature's `gamma (1 + beta) - 1 = 0.315`, 0.051 below, seventeen grains
of 0.003: FAIL on `main` at second order, the clock's factor gamma =
1.0378 absent. Beside it, not the law: series S under
covariant-readings-v1, z = 0.3674 at the identity's beta 0.3040 against
the pin `0.369 +- 0.003`, gamma 1.04967 (DETECTOR, MET in its domain;
EXPERIMENTS lines 6652 to 6735). The transverse 1 against nature's gamma
(2.3): FAIL in form at second order, not registered as a run. The moving
detector as a chain of face detectors, and the ratio of the two one-way
factors `k_BA / k_AB` that decides between `1 - v^2` (the law), `1` (the
relativity principle) and the loop's `(1 + v) / (1 - v)`: NOT MADE (the
click frame section 4's missing direction, lines 332 to 388; record
762's moving detector).

**Verdict.** SHOWN, rung 1, at first order matching nature; FAIL at
second order (NATURE 4b, 0.2636 against 0.315) on the law, the same
finding as the muon's clock (row 4a); the decisive one-way ratio NOT
MADE.

### II.5 The aberration of a moving detector

**(a) Outside, the measurement and its detector.** Bradley's aberration (1729): a source is displaced toward the
observer's motion by `tan alpha = v / c` (Einstein's form `v / (c sqrt(1
- v^2 / c^2))`). Here: the lamp A at rest on the x axis; the detector B a
passage of clicks moving on y at `v = 1 / k` across the stream (by (A3)
the chain of neighbouring places is the only frame the passage has); the
quantity read is the direction of the arrivals at B, by the click's face
or by the chain's own Nodes apart over counts apart.

**(b) Inside, the step that computes it.** A row's direction is its label **D**, constant over its
flight (L1); a moving body's release direction on `main` is the fan's,
unchanged by its motion (DERIVATIONS_BEAM 12.2, lines 2886 to 2960: the
aberrated vector `w = Q W D + T_D N_v` is "the missing vector operation",
a proposal, not on `main`); a body's steps are the drive's on its own
momentum.

**(c) The conversion, back to the click's counts.** The lamp A at rest at an empty Node on the
x axis, its rows on **D** = (1, 0, 0). The detector B a passage of clicks
(II.4) moving on y at `v = 1 / k` Links per count, across the stream.
Two Outside readings of the direction of the arrivals at B:

- *By the click's face.* The click's triple carries the row's momentum
  label, which names the Port the row entered (series Q reads the faces
  so): the label is **D** at every `B_i`, whatever k. The direction read
  by the face is the lattice's, unchanged by B's motion: no aberration,
  rung 1, exact.
- *By the passage itself* (the telescope's form: the direction a chain of
  detectors reads from Nodes apart over counts apart). Every Outside
  velocity is Nodes apart over counts apart, and the stream's velocity in
  the chain's own frame is the composition of the two: the rows advance
  `c_D` Nodes per count along **e**_x while the chain's clicks pass `v`
  Nodes per count along **e**_y, so between two clicks of the chain the
  stream's displacement counted along the chain is `c_D` **e**_x `- v`
  **e**_y per count (the law's Galilean composition `c -+ v` of 4.2, line
  1061, taken transverse), and the chain reads the stream from the
  direction

    tan alpha = v / c_D,     alpha the angle by which the source is displaced toward the chain's motion,

  the Galilean aberration, `alpha = v / c` at first order.

*The Outside formula.* `tan alpha = v / c` by the passage, `alpha = 0` by the
face. Nature's is `tan alpha = v / (c sqrt(1 - v^2 / c^2))`: the same at
first order (Bradley's 20.5 arcseconds at `v / c = 10^-4`), the law's
short by gamma at second order, the same absent root as II.4.

*The order.* Rung 1 for the face (exact); rung 1 in the count for the
passage, its second order the law's own.

*The inverse.* v from `alpha` and c, at first order.

**(d) The register, Outside.** None: no registered world reads an arrival
direction from a moving chain; series Q reads the faces at rest (the
labels, 290 of 290). The emitter's aberration (12.2) is pinned in 12.4
(lines 3004 to 3041) and NOT RUN, and it is not on `main`.

**Verdict.** SHOWN at first order (the Galilean composition of Nodes
apart over counts apart; the face reading exact and aberration-free);
NOT READ; the second order the law's `r = 1`, one finding with II.4's
FAIL.

### II.6 Interference: the two-slit fringes, the fringe spacing from the phase per age and the two paths' age difference

**(a) Outside, the measurement and its detector.** Young's fringes (1801) by Huygens' construction: bright where the two
paths differ by a whole wavelength, the spacing `lambda D / s` at small
angles; and Fraunhofer's single-opening envelope. Here: the lamp A at
rest at an empty Node, the openings at `y = +- s / 2` (re-emitters, the
apparatus), the screen at the distance D a set of detectors `B_y`, one
detector at each pixel y, each reading `sum` and counting its clicks per
its own count over W births; the quantity read is the count per pixel,
and from it the fringe spacing (the Outside number) and the visibility.
By (A3) each of the two paths is a chain of Nodes, and the fringe is the
difference of the two chains' counts read at ONE place.

**(b) Inside, the step that computes it.** One record born at the lamp with the birth phase u on the
wheel; at each opening the re-emission on a fan of K directions (the
split with equal weights); two rows of the record reach the screen's
Node at the height y by the paths `L_1` and `L_2` (Euclidean, the cone
Euclidean: 4.1, line 1038), at the ages `tau_i = L_i / c` (L1), with the
path phases `(n / d) tau_i` steps (L3, the exact phase at the click);
the merge where two rows of one record meet; the click's weight at the
cell `|e^(i phi_1) + e^(i phi_2)|^2 = 2 + 2 cos(2 pi (n / (d N)) (L_1 -
L_2) / c)` (L6; DERIVATIONS_BEAM 7.1, lines 1933 to 2002), the cell's
probability the weight over the record's total within `1 / (2 N)` (23.2),
one click per record by u on the ladder.

**(c) The conversion, back to the click's counts.** The lamp A at rest at an empty Node, the
openings at `y = +- s / 2` (re-emitters, the apparatus: input 23 of 24.1),
the screen at the distance D: a set of detectors `B_y`, one detector at
each pixel y (each place its detector), every one reading `sum` and
counting its clicks per its own count over W births. Outside_A ->
Inside: the birth at u; the flight and the two re-emissions Inside; the
merge Inside; Inside -> Outside_B: at the record's completion the ladder
puts one click at one pixel; over W births the pixels' counts.

*The Outside formula.* The count at the pixel y over W births,

    C(y) / W = (2 + 2 cos(2 pi (L_1(y) - L_2(y)) / lambda)) / Z + O(1 / (2 N)) + O(1 / W),   lambda = c N d / n Links,   Z the record's total,

bright where `L_1 - L_2 = +- j lambda`, that is where `sqrt(D^2 + (y +
s / 2)^2) - sqrt(D^2 + (y - s / 2)^2) = j lambda`; the fringe spacing
from the two paths' age difference, `delta tau = (L_1 - L_2) / c = N d
/ n` intervals per fringe: one turn of the phase per age; and only in the
paraxial limit `s, y << D` is the spacing Young's `delta_y = lambda D /
s`. Every number is a count at a detector at its pixel; the phase per
age enters only through the age difference of two rows read at ONE
place.

*The order.* The exact two-path law in the limit of every direction
(rung 2: the fan's grain, K), the click's Born within `1 / (2 N)`, the
wheel's resolution `1 / W`, the arrival at a whole interval (an eighth
of the wavelength at `lambda = 8` intervals; 7.1's list). Young's
paraxial form rung 2 in `s / D`.

*The inverse.* `lambda` from the fringes' positions within a pixel;
hence `n / d` from `lambda`, c and N; hence the frequency of the lamp
from the fringes alone, read at the screen.

**(d) The register, Outside** (DETECTOR, the screen's cells). L2b
`slits_huygens` (NATURE row 2a, line 96, and its note, lines 149 to 185;
EXPERIMENTS series L, line 3870): 4096 births under the exact phase at
the click, `lambda = 8 x 32 / 55 = 4.654` Links, `s = 10`, `D = 44`: the
bright bands at the pixels 35 to 38, 59 to 61 and 82 to 85, their centres
36.5, 60 and 83.5, 23.5 apart, the exact law's 23.3 (the first bright
fringe at `|y| = 23.3`, the pixels 36.7 and 83.3): MET within the pixel;
the paraxial 20.5 is three pixels off and is not the check. The dark
cells 0 to 3 as pinned: MET. The visibility of the clicks 0.966 against
Grangier's 0.98 (nature's, a lower bound on the ideal 1): FAIL by 0.014,
the cause the fan's grain, registered. The counts' Pearson with the
two-source cosine 0.891 against the pin 0.96: FAIL (the pin derived for
the screen's fan, not this world's Farey fan; the miss registered). L1's
unequal arms, the two-path rule integer by integer: arm 2 longer by two
intervals at the pair form 0, [8, 1] and [16, 1] reads D1 / D2 = 64 / 0,
32 / 32, 0 / 64, the phase difference 0, 16, 32 steps of 64 (DETECTOR,
MET exactly; lines 3900 to 3950). The massive rows' fringes, series W
(record 754; EXPERIMENTS line 4414): the bands 37.06 / 59.99 / 83.02,
Pearson 0.88, visibility 0.964 (DETECTOR, PASS), the same two-path law
with `lambda = h / p` (II.2 (c), the inverse) under the every-family wall (PR #743 at
95e43ab9: the phase per age of every family under one table,
docs/designs/one_wall/EVERY_FAMILY.md).

**The writer's chain, verified against the engine's lines and the
register, and where it differs** (paper/general_formula/PLAN.md section
8c on the branch claude/paper-owner-review-five at fdc91cb8, read, not
copied; the paper is not touched). In the three-formula shape the
writer's two slits are: the Outside step, Young's fringes read as the
count per pixel; the Inside step, two rows of one record (m = 2), their
phases at the pixel, the merge in `Z[Z_N]` with the cancel at `Delta = N
/ 2`, the click's square `R(x) = 512 ((C[p_1] + C[p_2])^2 + (S[p_1] +
S[p_2])^2)` proportional to `1 + cos Delta(x)`; the conversion, the
rungs `b_x` and the count `b_x - b_(x-1)` over the births, the dark
pixel a rung of width 0. Checked line by line:

1. *Two rows, m = 2.* The pixel's pair of the limit of every direction
   (7.1). The registered worlds carry the fan (K rows per opening, 91 in
   `slits_low`, the Farey fan of width 48 in `slits_huygens`) and the
   wheel; at K = 91 only 27 of 75 pixels see both openings (7.1's list
   item 2), so the pair is exact per pixel only in the fan's limit. The
   same.
2. *The phase "one turn per Link (F)".* The integer form per Link is the
   paper's F; the registered two-slit worlds run the pair form, `n / d`
   steps per interval of AGE (`slits_huygens.json`: `phase_per_link`
   `[8591334592, 2^30]`, 8.00 steps per interval; BEAM_LAW line 3733),
   read at the exact time of the last Link (note 45; `exact_phase`). On a
   straight line at the constant pace the two agree up to the arrival's
   rounding, which the exact phase removes (Pearson 0.904 to 0.963, 7.1's
   list item 3). Differ in the form named; the same fringes.
3. *`R(x) = 512 (...)`.* The proportionality to `1 + cos Delta` is the
   engine's: `(C_1 + C_2)^2 + (S_1 + S_2)^2 = 2 (65536 + C_1 C_2 + S_1 S_2)`
   within the tables' rounding (`C^2 + S^2` within 361 of 65536), and
   `C_1 C_2 + S_1 S_2 = 65536 cos Delta` within 237 (6.7). The constant
   512 is the writer's; the engine's cell weight for two rows of amount 1
   is `(32 x 256^2)^2 = 2^42` times the bracket (`amplitude.py` `UNIT`,
   `gram_form`) and a detector set's `wave` record is `32^2` times it
   (BEAM_LAW line 797); the constant cancels in the rungs. Differ in the
   constant; the same shape.
4. *The rungs and the count.* `b_x = (2 W C_x + T) // (2 T)` with W the
   wheel (N under `[1, N]`; 4096 under L2b's `[2531, 4096]`) is
   `amplitude.py`'s `rungs` (line 241) and `cell_of` (line 275) exactly,
   and over W births with u uniform the count at x is `b_x - b_(x-1)`,
   Born to `1 / (2 N)` per cell (23.2). The same; the writer's "over N
   births" reads W.
5. *The dark pixel, "a rung of width 0, no click can land there".* Exact
   where the offer is exactly 0, the cancel of equal amounts at `Delta =
   N / 2` on the GameBoard (`mz_balanced`'s dark port); an offer below `T
   / (2 W)` also gets an empty cell (`rungs`' docstring), and a small
   offer above it gets a click now and then: L2b's dark cells read 0 to 3
   (the mean 0.68, NATURE 2a), not 0, since the fan's two rows at a dark
   pixel are not exactly antipodal and the arrival is rounded. Differ:
   "does not pass" is exact at the cancel and approximate elsewhere.
6. *"The bright pixels 19 to 51".* These are the bright pixels' COUNTS
   over 4096 births (EXPERIMENTS line 4339: "bright 19 to 51 (the mean
   39.3)"); the bright pixels' positions are 35 to 38, 59 to 61 and 82 to
   85. Say counts.
7. *"Young's spacing, recovered in the fan's limit".* The register's
   check is the exact two-path law (23.3 pixels at `y / D = 0.5`), not
   Young's paraxial `lambda D / s = 20.5`, three pixels off (7.1); name
   the exact form and its paraxial limit.
8. *One slit.* Right for a POINT opening: one row per pixel reached, no
   pair, `R = 2^42 (C^2 + S^2)` at every pixel within the tables' rounding
   (a part in 276), so the count per pixel is the fan's density of
   directions per pixel with the angle weights, flat only within that
   grain. A WIDE opening of w Nodes releasing rows of one record at the
   phases `p + j delta` (j = 0 .. w - 1, delta the neighbours' path
   difference times the turn) merges to `|sum_j e^(i j delta)|^2 = sin^2(w
   delta / 2) / sin^2(delta / 2)`, Fraunhofer's envelope with the dark
   pixels at `w sin theta = j lambda`: the Outside step of NATURE row 10
   (the single-opening spread, A10's 1.08 against 0.886, NOT YET under
   the one click). Say "a point opening".
9. *Mach-Zehnder.* The offers 1681 / 1682 and 1 / 1682 are NOT the
   tables' rounding: they are the declared (20, 21) split's own
   imbalance, exact, `(20 + 21)^2 = 1681` at the bright port and `(21 -
   20)^2 = 1` at the dark, the sum 1682 (NATURE 2b's note, lines 186 to
   199); the balanced (1, 1) split gives 1 and 0 with the dark port's
   rows cancelled on the GameBoard (`mz_balanced`). The registered
   device: the lamp births the record on two arms, the mirrors at (3, 0)
   and (0, 3), ONE splitter at (3, 3) whose table turns the reflected row
   by the quarter turn (`turns [[16, 0], [0, 16]]` at N = 64), not "the
   mirrors turn by N / 4". And the offers' visibility 0.9988 is a number
   of the apparatus layer, a diagnostic, never the ground of the PASS
   (records 562 and 564); the reading is the clicks 64 / 0. Differ: the
   source of the `1 / 1682` and the device's description; the same
   three lines otherwise.

In the three-formula shape, then: the Inside step is (1) of section 0
(the hop, the age, the phase per age, the merge with the cancel, the
click's `f^T G f` and the rungs); the Outside step is Young's and
Fraunhofer's for the openings and Mach and Zehnder's for the device
(II.7); the conversion is the record's births at A and the clicks at
the pixels or the ports, the count per place `b_x - b_(x-1)` over the
wheel. The fringe spacing Outside: `delta tau = N d / n` intervals of age
between bright pixels, that is `lambda = c_D N d / n` Links of path
difference, 4.654 Links on the registered world, read as 23.5 pixels
between band centres at `D = 44`, `s = 10`, the exact law's 23.3
(rung 2 in the fan, the click within `1 / (2 N)`, the pixel's grain).

**Verdict.** SHOWN, rung 2 (the fan) with Born at rung 1 within `1 / (2
N)`; MET on the fringe spacing (23.5 for 23.3), on the unequal arms
(exact) and on the dark cells; FAIL on the visibility (0.966 against
0.98) and on the correlation pin (0.891 against 0.96), both registered
with their cause.

### II.7 The click's indivisibility: Born at one click, never two (Grangier's anticorrelation, NATURE row 2b)

**(a) Outside, the measurement and its detector.** Grangier, Roger and Aspect's anticorrelation (1986): one photon at a
splitter clicks one detector and never both, `alpha = P(both) / (P(D1)
P(D2)) < 1` (0.18 +- 0.06 read, 0 the ideal), and in the recombined
device of Mach and Zehnder (1891) the visibility 0.98 (NATURE row 2b).
Here: the lamp A at (0, 0) on the plane; the detector D1 at (4, 3) and
the detector D2 at (3, 4), and in the Elitzur-Vaidman worlds the absorber
at (0, 3), each at its place reading `sum`; the quantity read is the
clicks per detector per record, and their coincidence.

**(b) Inside, the step that computes it.** One record, one click: at the record's completion the
ladder over the cells of every detector the record reached chooses the
cell of its birth phase u and deletes the record's offers in the same
interval (L6; BEAM_LAW note 37 (x), line 2849; EXPERIMENTS E15, line
9836: "the deletion of its 126 offers in the same interval, no row of it
left on the GameBoard"); the cell's weight `f^T G f`; the cancel: rows
of one record in antiphase with equal amounts read exactly zero (6.7,
**G** kills every antipodal pair).

**(c) The conversion, back to the click's counts.** The lamp A at (0, 0) on the plane, one
record per self-creation on two arms; the mirrors at (3, 0) and (0, 3)
and the splitter at (3, 3), declared tables (the apparatus); the detector
D1 at (4, 3) and the detector D2 at (3, 4), each at its place, each
reading `sum`; in the Elitzur-Vaidman worlds an absorber at (0, 3), a
third detector at a third place. Outside_A -> Inside the birth;
Inside the split, the mirrors' permutation, the merge at the splitter
with the quarter turn on the reflected row; Inside -> Outside the one
click of the record at ONE of the detectors.

*The Outside formula.* Per record, exactly one click among the detectors, at
D1 with the probability `w_1 / (w_1 + w_2)`, at D2 with `w_2 / (w_1 +
w_2)`, `w_i` the Gram weights (Born within `1 / (2 N)`), and never at
both:

    P(D1 and D2 in one record) = 0   exactly;   the anticorrelation parameter  alpha = P(both) / (P(D1) P(D2)) = 0,

and with equal arms and the balanced split the dark port's weight is the
cancel's 0 exactly: D2 reads 0 of W. Nature's Grangier, Roger and Aspect
1986 read `alpha = 0.18 +- 0.06 < 1` (EXPERIMENTS A4, line 4669; the
ideal single photon 0) and a visibility 0.98 in the recombined device
(NATURE row 2b, line 97).

*The order.* Rung 1, exact, for the one click (the ladder's
definition); Born within `1 / (2 N)` for the fractions; the dark port
exact by the cancel (a declared pair `(1, 1)`) or `1 / 1682` by the
declared Pythagorean pair (20, 21).

*The inverse.* None: the amount and the phase of one record never pass
Outside singly; the weights pass only as fractions over many records
(the click frame's second fact, lines 908 to 923).

**(d) The register, Outside** (DETECTOR, the gathers over 64 births;
EXPERIMENTS lines 3900 to 3950; NATURE 2b's note, lines 186 to 199).
`mz_equal` D1 64, D2 0: the visibility in the clicks 1.000 above the
measured 0.98, PASS (NATURE 2b), MET; `mz_balanced` 64 / 0 with D2's rows
cancelled on the GameBoard; `mz_345` 63 / 1, and at N = 32 and 128 the
same split 31 / 1 and 125 / 3, every pin met exactly; `ev_29` (the
absorber at (0, 3)): absorber 32, D1 17, D2 15, 64 clicks for 64
records, one per record and never two (MET: the anticorrelation read at
three places, `alpha = 0`, matching nature's below-one and its ideal 0);
`ev_169` 32, 16, 16. The offers' visibility `(1681 - 1) / 1682 = 0.9988`
is a number of the apparatus layer (the record's ledger), a diagnostic,
never the ground of the PASS (records 562 and 564). The pair's two clicks
from one cell at two places (E16, line 9852) are one record's ONE cell,
read at two detectors: not two clicks of one row.

**Verdict.** SHOWN, rung 1 (exact); MET on `mz_equal` (64 / 0, NATURE 2b
PASS), on `mz_345` at three N (exact), and on `ev_29` (one click per
record among three places).

### II.8 The redshift of light through a crowd: `1 + z_d = r (1 + z)`, the age wall at coefficient 1 (series G and G2)

**(a) Outside, the measurement and its detector.** Einstein's gravitational redshift (1911; Pound and Rebka 1960), `1 +
z = 1 + (Phi_B - Phi_A) / c^2` at first order, and Hubble's law (1929)
with the Doppler of the throw: the frequency read at a detector in one
crowd against a lamp's own in another. Here: the lamp A in its crowd at
the place A, thrown at v or at rest; the detector B in its crowd at the
place B, at rest, reading `measure` with `reads: age` on the click
record, counting in its own count; the quantity read is `1 + z_d`, B's
count between two clicks over A's count between the two births.

**(b) Inside, the step that computes it.** The age wall on every count (L8): a lamp in the crowd
`a_tau,A` at its Node self-creates at the rate `1 / (1 + k_A)`, `k_A =
a_tau,A n / d`, births included (one row per self-creation); a detector
in the crowd `a_tau,B` counts at `r_B = 1 / (1 + k_B)` per interval; the
row's phase per age and its flight are not members (L1, L3: "a
stretched phase per age would redshift light", BEAM_LAW line 609, so
the law redshifts light by the clocks and never in flight); the throw's
Doppler by II.4.

**(c) The conversion, back to the click's counts.** The lamp A in its crowd at the place A (its
births its clicks, at its own count), thrown at v or at rest; the
detector B in its crowd at the place B, at rest, reading `measure` with
`reads: age` on the click record (the age word), its own count `n_B`
stretched by its own crowd at coefficient 1 (record 709; the Clock
Reader's primitive, record 754: `r = delta age / delta t`, the detector's
self-creations per interval off its own state). Outside_A -> Inside the
births, one per A's count, at the tick spacing `1 + k_A`; the flight
blind; Inside -> Outside_B the clicks, one per row, at B's count.

*The Outside formula.* `1 + z_d`, the count B reads between two clicks over the
count A read between the two births (one), is the product of three
factors, each a count:

    1 + z_d = k_AB = (1 + k_A) x (1 + v / c) x r_B = r_B (1 + z),     1 + z = (1 + k_A)(1 + v / c) the lattice-frame form (series G's formula),   r_B = 1 / (1 + k_B),

the record 754 primitive derived: the lamp's stretch, the throw's
spacing, the detector's own rate. At `v = 0` the gravitational redshift
between two clocks in two crowds is

    1 + z_d = (1 + k_A) / (1 + k_B) = 1 + k_A - k_B + O(k^2),

and with the crowd's form about a point source (L5, the age moment `q
dwell / (4 pi c r)`, the `1 / r` potential: the click frame section 8
(b), lines 1009 to 1028) the first order is Pound and Rebka's `Phi_B -
Phi_A` form, the potential's, with the world's constant `[n, d]` and the
residence factor in place of `1 / c^2` (section 8 (e), line 1061). At
second order the law reads `1 - k + k^2` where nature reads `1 - k -
k^2 / 2` (DERIVATIONS_BEAM 5.2, lines 1212 to 1235: a different law in
the strong field, no horizon), below reach at the Earth (24.3 row 12).
The consistency rule is the row's content: `k_B` is read by B's own
count and by nothing else; a lamp and a detector in equal crowds read `z_d
= 0` at rest; the well of the detector's own crowd is `z_d(0) = r_B - 1
< 0`, a blueshift of every lamp at rest outside it (record 754). The
Hubble form: a coasting throw reads `H_d = r_B H` and the far lamp under
the growing wall (expansion-v1, a declared assumption, not built)
`1 + z = e^(H d / c_0)` with the stream's stretch exactly `1 + z` and one
factor `1 / (1 + z)` on the flux (docs/designs/far_lamp/BRIGHTNESS.md;
DERIVATIONS_BEAM 15.3, lines 4049 to 4065; NATURE rows 11a to 11c).

*The order.* Rung 1 within the count's grain (the owed count's whole
part per self-creation, the crossing's one row) for `1 + z_d = r_B (1 +
k_A)(1 + v / c)`; rung 2 (the shell mean) for the `1 / r` form of k; the
second order in k the law's own; the second order in v II.4's.

*The inverse.* `k_A - k_B` from `z_d` at `v = 0` at first order; `v / c`
from `z_d` at `k = 0`; `r_B` from a control lamp at rest in no crowd
(series T's and X's controls), `k = (1 + z) / (1 + z_0) - 1` against it
(the click frame's table, line 901).

**(d) The register, Outside** (DETECTOR unless said). Series G
(EXPERIMENTS lines 2125 to 2360): `(1 + z) / ((1 + k)(1 + v / c))` from
0.995 to 1.005 over 24 sources, 288 of 288 inside 2 percent over three
windows, the coasting worlds `z = v / c` to 0.003 and `H t_0 = 1.029` at
`t_0 = 350` (MET); under the detector's own clock (record 754, tier (b),
branch clock-rereads, PR #777 not merged at this writing: cited from the
record on `main`, line 1711) `r_w = 0.7500, 1.0000, 0.3400, 0.9600` in
the late windows, the formula 288 of 288, 304 inside and 32 outside, and
the crowd's well `z_d(0) = r - 1` blue for 15 and 20 of 24 sources in the
scalar worlds. Series G2 (lines 2361 to 2548): the formula 648 of 648,
the luminosity `1 / (1 + z)` 648 of 648 within 5 percent (MET), `r = 1`
in the `none` worlds and 0.4825 / 0.3725 in the scalar worlds (record
754); `coasting_none`'s stars `z = v / c` within 0.004 (MET on the law's
form; FAIL against nature's gamma, II.4). Series T (lines 6737 to 6835;
NATURE row 12, line 116): the age word `1 + z = 2.6517` at 3 Links (`k
= 22 F / 2^16 = 1.650`, the pin 2.650 +- 0.05) and 4.1500 at 6 Links (`k
= 3.150`, the pin 4.150 +- 0.05), the ratio of the two k `3.1503 / 1.6516
= 1.907` against the pin `1.909 +- 0.05` (MET; the continuum's 2.000
outside by the lattice's dwelling ages), the presence word 1.3000 at
both distances (MET as pinned, FAIL against nature's potential form,
1.000 against 2.00); the controls 1.0000 exactly (MET: `r_B = 1` at an
empty Node). Series X (lines 6835 to 6970): every one of nine worlds MET,
inside a shell of sources flat within 0.02 under the age word (`k(2) /
k(4) = 1.0029` for 1.003917) and outside `k(12) / k(4) = 0.6285` for
0.618270 (the continuum's `1 / r` 0.5 outside by the grain), the detector
in the shell's on-axis rows read at `k_D = 0.0945` to 0.1357 by the map
with the reading's denominator the host tick (the strict form's ratios
0.9994 and 0.5134 stated, GAMEBOARD arithmetic; the convention the
owner's). The far lamp under the growing wall (NATURE 11a to 11c; pinned,
not run): the stretch `1 + z` exactly, `b = 1` within `0.97 +- 0.10`
(11b, PASS pinned); the brightness `q_eff = +1` against `-0.53` (11a,
FAIL pinned) and Tolman's `n = 1` against 4 (11c, FAIL pinned): the law
carries one factor of `1 + z` where nature has two, because a click's
content never follows its frequency (II.2 (c), the Outside formula).

**Verdict.** SHOWN, rung 1 (the three factors are three counts; the
potential's `1 / r` rung 2); MET on G (288 of 288), G2 (648 of 648), T
(1.907 for 1.909) and X (nine of nine); FAIL on the presence word's form
(NATURE 12, the law's default word, 1.000 against 2.00; the age word the
owner's word) and, pinned not run, on the far lamp's brightness (11a)
and Tolman (11c); the second order in k below reach.

### II.9 Polarisation: Malus's law from the two-state label (NATURE row 9)

**(a) Outside, the measurement and its detector.** Malus's law (1809): the fraction a polariser at the angle theta passes
is `cos^2 theta`. Here: the lamp A at rest on the bar, the polarisers at
their places (declared `rotate` and `read` entries), the detector B a
`sum` set behind the last polariser at its place; the quantity read is
the fraction of the records clicking in the pass cell.

**(b) Inside, the step that computes it.** The row's label bit; the polariser the rotation of the
label by the declared setting (`rotate` on the GameBoard, or the `sum`
set's window) and the which-path `read` at a `sum` set (L9; the click's
Gram form on the rotated label, the half-angle tables at the scale 256:
docs/designs/malus/NOTE.md sections 1 to 3).

**(c) The conversion, back to the click's counts.** The lamp A at rest on a bar of 7, every row
born on the label 0, on the wheel [159, 256]; the polarisers at their
places (a `rotate` by the setting, then a `read`: the apparatus's
declared entries, input 23); the detector B behind the last polariser, a
`sum` set reading the label cell, at its place, counting its clicks per
record over the 256 records. Outside_A -> Inside the birth on the label;
Inside the rotation (the declared matrix) at each polariser's place;
Inside -> Outside_B the click in the pass cell or the stop cell.

*The Outside formula.* The fraction of the records clicking in the pass cell
behind a polariser at the angle theta to the label,

    P(pass) = cos^2 theta   within the tables' rounding at the scale 256   (exact where the table entry is exact: 45 and 90 degrees),

and through a chain the product of the cos^2 of the successive
differences, `1 / 4` for the third at 45 degrees between two crossed.

*The order.* Rung 1 within the tables' rounding (`+0.0019` at 22.5
degrees, DERIVATIONS_BEAM 24.3 row 4, line 7066); exact at 0, 45 and 90
degrees.

*The inverse.* theta from the pass fraction, within the rounding.

**(d) The register, Outside** (DETECTOR, the cells over the records 1 to
256; NATURE row 9, line 110; EXPERIMENTS A12 under the click, line 6256):
`malus_a` 0+ 128 / 0- 128 (1 / 2 at 45 degrees, exact), `malus_b` 0 of
256 crossed, `malus_c` 64 of 256 with the third polariser at 45 degrees
between (1 / 4 of the births, 1 / 2 of the 128 the first passed): every
pin met exactly, PASS (NATURE 9), MET; at 22.5 degrees 219 / 256 =
0.85547 against `cos^2 = 0.85355`, the chain 187 / 256 = 0.73047 against
`cos^4 = 0.72855`, `+0.0019` both, every pin met exactly (MET on the
pins; OPEN against a Malus test at `10^-3`, the tables' scale by the
owner's word, record 328).

**Verdict.** SHOWN, rung 1 within the tables' rounding; MET (exact at 45
and 90 degrees; `+0.0019` at 22.5 degrees, OPEN at `10^-3`).

### II.10 The pair's correlation at two places: the Bell pair of the amplitude family (NATURE row 1a)

**(a) Outside, the measurement and its detector.** Bell's inequality (1964) and the CHSH sum (1969): `S <= 2` for every
local assignment and at most `2 sqrt 2` in quantum theory (Cirel'son
1980), read as coincidence counts at two places under two settings each.
Here: the lamp A at the centre; Alice's counters at the places `A_+`,
`A_-` with the setting a and Bob's at `B_+`, `B_-` with the setting b,
each a detector at its place reading `sum`; the quantity read is the four
coincidence counts per pair of settings and their correlation.

**(b) Inside, the step that computes it.** One record born as one record with two arms, its rows
ending at Alice's counters and at Bob's; the one Gram form over both arms
at the record's completion, quadratic in the record vector **f** with
cross terms between its cells; the one click of the record puts its ONE
cell, a pair of outcomes, at the two detectors (L6; DERIVATIONS_BEAM
22.3, lines 6653 to 6680; 6.2's `S(N, Q)`).

**(c) The conversion, back to the click's counts.** The lamp A at the centre; Alice's two
counters at the place `A_+`, `A_-` with the setting a, Bob's at the place
`B_+`, `B_-` with the setting b, each a detector at its place reading
`sum`. Outside_A -> Inside the birth of the two-arm record; Inside the
two flights and the settings' rotations (the declared matrix at each
counter's place); Inside -> Outside the one cell at the two places, two
clicks of one record.

*The Outside formula.* The coincidence counts at the four cells over W births,
`E(a, b) = (N_++ + N_-- - N_+- - N_-+) / W` the correlation at one pair of
settings, `S = E(a, b) - E(a, b') + E(a', b) + E(a', b')` the CHSH sum;
the marginals `N_+ / W = 1 / 2` at each place whatever the other's
setting (no signalling: a click at Bob's place reads nothing of Alice's
setting, the consistency rule's sharpest case); and

    S(N) = the register's exact rational of the tables and the rungs,   S -> 2 sqrt 2   as N -> infinity within  8 / N + 16 arcsin(sqrt 2 / (2 Q)).

*The order.* Rung 1 exact at every N (the tables and the rungs);
Tsirelson's bound reached as a limit, the plateau `181 / 64` from N = 512
to 8192 (24.3 rows 1 to 3, lines 7063 to 7065).

*The inverse.* None singly (II.7 (c), the inverse).

**(d) The register, Outside** (DETECTOR, the cells over 64 births; NATURE
row 1a, line 94, and its note, lines 120 to 148; E16, line 9852): the
four cells 27 / 5 / 5 / 27 of 64 at the labels (0, 8), (0, 24), (16, 8),
(16, 24), `E x 64 = 44, -44, 44, 44`, `S = 176 / 64 = 2.75`, every marginal
32 / 64 exact: against Hensen 2015's `2.42 +- 0.20`, 1.65 standard
errors, PASS (MET); at N = 1024 and 4096 `S = 2.828125`, 0.0003 below the
bound (`pair_n`). Against Poh et al. 2015's `2.82759 +- 0.00051`: at N =
256 the law's 2.8125 is REFUTED by thirty standard errors, at the plateau
`2.828125` within 1.1 standard errors of the measured deficit (24.3 rows 1
and 2): FAIL at N = 64 and 256 against the precision test, OPEN on the
plateau.

**Verdict.** SHOWN, rung 1 (exact at every N); MET against Hensen (2.75
for `2.42 +- 0.20`); FAIL against the precision test at the registered N
= 64 and 256, OPEN on the plateau.

### II.11 Reflection and refraction: NEITHER, said plainly

The law has no law of reflection: a row meets no surface, reads nothing
of the crowd in flight (L1, P9) and is neither turned nor stopped by a
body; a mirror is a declared re-emission table of the apparatus (input
23: L1's mirrors at (3, 0) and (0, 3), the splitter's "transmitted 20,
reflected 21 with the quarter turn", EXPERIMENTS line 3901), whose angle
is the declared direction and not a formula of the law. The law has no
refraction: no crowd slows or bends a row on `main` (DERIVATIONS_BEAM
5.4, lines 1251 to 1292: "a row is neither bent nor delayed beside a
mass, exactly"; series K's 0.000), the flight table is one speed in
every crowd, and no medium exists in the law but the crowd, which the
flight does not read; optical-v1 and every family under one wall (PR
#743 at 95e43ab9), where a row's wall reads the crowd, are a hypothesis
under its own identity, not the law, and derive no Snell's law there
either (a wall's stretch, not a turn at a surface). Verdict for both:
NEITHER (no closed form Outside and no reading), plainly; the mirrors of
the register are the apparatus and rest on no law of reflection.

### II.12 The boundary: light's bending and delay by a mass

Belong to the Einstein Mathematician and are not derived here. Named:
on `main` the rows are blind (5.4; series K's deflection 0.000 pixel,
DETECTOR; DERIVATIONS_BEAM 24.3 row 14, REFUTED on `main`); under
optical-v1 and every family under one wall (PR #743 at 95e43ab9) the
beam's centroid shift `-1.993 / -3.989` pixels at gamma 0 / 1 in the mass
world, the ratio 2.00 within the pinned 0.25, the Bresenham far worlds
at b = 8 `-3.403 / +4.33` inside their pins `-3.37 +- 0.5` and `4.29 +-
1`, the delays' ratio 1.67 outside `2.00 +- 0.25` by 0.08 (DETECTOR,
EXPERIMENTS lines 6972 to 7165; NATURE row 13, line 115: NOT COMPARED,
gamma an input of kind 2). Nothing of it enters any row above; the
consistency rule holds there too: the shift is read at the screen's
pixels, the delay at the screen's count.

## III. The certification of the inputs

**Nothing of Maxwell and nothing of optics is assumed.** No wave
equation, no field **E** or **B**, no Huygens principle, no Fresnel
coefficient, no Snell's law, no Malus's law, no Planck spectrum and no
Doppler formula is an input of any row. What each row uses: the flight
table (L1, L2), the phase per age and the exact phase at the click (L3),
the release's cost and the dictionary of h (L4), the count of Nodes on a
shell (L5, arithmetic), the click's bilinear form and the one click (L6),
the crossing rule (L7), the age wall at coefficient 1 (L8) and the label
bit with its rotation (L9), every one a line of `main` at 46cf692b with
its line number in section I. The wave equation, its Lorentz symmetry
for the free rows, the inverse square, the fringes, the cos^2 and the
gravitational redshift come OUT of those lines at the rungs named; where
a row says "the paraxial limit", "the shell mean", "the fan of every
direction" or "within the tables' rounding" it names the limit taken and
its error term, and where the lattice departs from the limit at finite
grain it says MEASURED ONLY.

**What is assumed of the world, said once.** (A1) a click is the passage
of information from Node to Node, at most one Node per interval; (A2) a
click's content is an amplitude with a phase that splits between staying
and hopping (the click frame lines 41 to 53); (A3) locality Outside, (A1)
read from above: every passage of light Outside is a chain of clicks
between neighbouring places, no jump, no velocity above one Node per
interval, no reading where no chain reaches (the owner's word, section
I). Every row uses (A1) at the
click, as the one Node per interval of the count's ratio; (A2) is used
only at the click through Born's form (L6, the one imported member `c_1 =
1` of 24.1 row 12), and in no row's dynamics: the law's rows hop whole
(the click frame lines 185 to 202), so every `r` above is the law's `r =
1` at an empty Node and `1 / (1 + k)` in a crowd, and nature's root
(gamma) is absent at second order in v wherever a row reads a moving
record (II.4, II.5), which is stated as FAIL where the register has read
it and never softened. The frame's own assumption, that the board is
read only through detectors and emitters (Highlights line 401, record
762), is the consistency rule's ground and is assumed, not shown.

**What is not in the law, said under its own identity, outside the law.**
Nothing new is proposed inside the law here. Three things named above
stand outside it and are cited as such: covariant-readings-v1 (the
identity with `r = E'_0 / E'`, II.4 (d)), the emitter's aberration
operation of DERIVATIONS_BEAM 12.2 (II.5, a proposal, not on `main`) and
optical-v1 with every family under one wall (II.11, II.12, a hypothesis
under its own identity). No seventh verb is used in any row. Every
number in section II is a formula's value (GAMEBOARD until a detector
reads it, named so) or a registered detector reading named so; none is
pinned here from a run, and no run is named.

**The three tests, for the record** (skills/workflow.md, "The three
tests"): this document adds no rule, so there is nothing to admit; every
operation it reads is on `main` and already admitted. The verdicts:
generic, one flight, one phase, one click for every family (the same
rows serve `light`, `matter` and the Bell pair); vector, every row a
translation, a declared matrix, a bilinear form or a comparison, no root
at run time (the roots in section II are the derivation's, taken on
paper in the limit, never a step of the law; `isqrt` at load is the
declared rounding); local, every count a detector's own record and the
six neighbours, nothing kept at a Node (the consistency rule is LOCALITY-1
read Outside: a reading at another place is a detector at that place).

## IV. The verdict table

SHOWN: it comes out algebraically under section I's lines at the rung
named. MEASURED ONLY: no closed form Outside; the register's run rises
Outside. NEITHER: no closed form and no reading. FAIL: a registered pin
missed, or nature's form missed where the register has read it (a pin
met is MET, a pin missed is FAIL, in the same font). The register's
readings by kind; every number DETECTOR unless labelled.

| The formula Outside | Verdict | The one line that decides | The register (DETECTOR unless labelled) |
| --- | --- | --- | --- |
| the speed of light, `c_D = Q |D|_2 / T_D` by the row's age or by the pulse and its return; the anisotropy `1 / c_D^2 = 2.954 / 2.971 / 3.000` on the heading, the face diagonal and the body diagonal; the isotropic limit `1 / sqrt 3` | SHOWN, rung 1 in the count, rung 2 in the isotropy; FAIL against nature's isotropy at the grain | the flight table's `tau_k = ceil((2 k - 1) T_D / (2 S_1 Q))` (L1, L2), the age on the record read at B, the round trip A's own count | series Q: 290 of 290 at the derived tick, Node and face, the pace 0.5718 to 0.5893, mean 0.5810 (MET); series T: 172 counts for 100 Links, `1.72 = 110 / 64` (MET); NATURE 5a: `7.6 x 10^-3` against `10^-17` (FAIL at Q = 64, a bound `Q >= 5.8 x 10^16`); the two-way c after a detector NOT MADE (pinned here: 110 counts over 32 Links there and back, GAMEBOARD) |
| `E = h f` at a click, `lambda = h / p` | SHOWN, rung 1 (an identity of the release and the calibration `h_A = h_q N`) | the content per click is the birth's `h_q s` and follows nothing in flight (L4); the frequency B counts is the lamp's turn per `k_AB` | the paid lamps' stalls (159 births in 160 at 2 per birth; L1's at tick 2) (MET at the emitter); Q's clicks carry their birth content (MET); T's and X's controls `1 + z = 1.0000` (MET); `lambda` through L2's fringes (MET); the massive row's `256 / 55` (23.3) NOT RUN |
| the intensity of a source: `q K / (4 pi r^2)` per detector in the shell mean, `1 / r^0` on a beam, the count over a closed surface conserved | SHOWN, rung 2 (the shell mean); rung 1 on a beam and for the conservation; the finite-r ripple MEASURED ONLY | K beams over `N(r)` Nodes (L5); every row leaves the shell once | Q: 290 of 290 at the faces (MET, the conservation); T's presence word 1.3000 at 3 and at 6 Links (MET as `1 / r^0` on a beam; FAIL against nature's `1 / r` for a clock, NATURE 12); X's presence word inside 0.8390 for 0.839989 (MET, the flux rises toward the shell); the `1 / r^2` at two radii after a detector of light NOT MADE (NATURE 11a pinned, not run); series C and E GAMEBOARD, not compared |
| the Doppler of a moving detector `1 / (1 -+ v)`, of a moving lamp `1 +- v`, the transverse 1, the round trip `(1 + v) / (1 - v)` | SHOWN, rung 1; matches nature at first order; FAIL at second order on the law | the crossing count `1 +- v / c` (L7) and the rows' spacing `c -+ v` (2.5); `r = 1` on the law where nature has `sqrt(1 - v^2)` | the crossing counts 45 / 58 / 19 / 38 in 32 and 48 intervals, 183 and 311 over 32 Links (MET, `tests/test_crossing.py`); G2 `coasting_none` z = v / c within 0.004 per star (MET on the law's form); NATURE 4b: 0.2636 against 0.315 at beta 0.2674 (FAIL, gamma absent); series S under covariant-readings-v1 0.3674 for `0.369 +- 0.003` (MET in its domain, beside the law); the one-way ratio `k_BA / k_AB` NOT MADE |
| the aberration of a moving detector: `tan alpha = v / c` by the passage of clicks, 0 by the click's face | SHOWN at first order; NOT READ; the second order the law's `r = 1` | Nodes apart over counts apart compose as `c -+ v` (4.2); the label is the row's own | none registered; 12.2's emitter aberration pinned in 12.4, NOT RUN, not on `main` |
| the two-slit fringes: bright where `L_1 - L_2 = j lambda`, `lambda = c N d / n`, one turn of the phase per age per fringe; Young's `lambda D / s` paraxial | SHOWN, rung 2 (the fan), Born rung 1 within `1 / (2 N)` | the two rows' age difference at ONE detector, `(n / d)(L_1 - L_2) / c` steps, squared at the click (L3, L6) | L2b: the bands' centres 23.5 apart for the exact law's 23.3 (MET within the pixel), the dark cells 0 to 3 (MET); the visibility 0.966 against 0.98 (FAIL by 0.014, the fan's grain); Pearson 0.891 against the pin 0.96 (FAIL, the pin the screen's fan's); L1's unequal arms 64 / 0, 32 / 32, 0 / 64 at 0, 16, 32 steps (MET exactly); W's massive bands 37.06 / 59.99 / 83.02 (PASS) |
| the click's indivisibility: one click per record, never two; `alpha = 0`; the dark port 0 | SHOWN, rung 1 (exact) | the ladder chooses one cell and deletes the offers (L6, note 37 (x)); the cancel exact | `mz_equal` 64 / 0 (NATURE 2b PASS, MET); `mz_345` 63 / 1, 31 / 1, 125 / 3 at N = 64, 32, 128 (MET exactly); `ev_29` 32 / 17 / 15, 64 clicks for 64 records at three places (MET) |
| the redshift through a crowd `1 + z_d = r_B (1 + k_A)(1 + v / c) = r (1 + z)`; at rest `(1 + k_A) / (1 + k_B)`, the potential's `1 / r` at first order | SHOWN, rung 1 (three counts), the `1 / r` rung 2; the second order in k the law's own (below reach) | the age wall at coefficient 1 on the lamp's births and on the detector's own count, the row's phase never stretched (L8, L3, BEAM_LAW 609) | G: 288 of 288 within 2 percent, `H t_0 = 1.029` (MET); tier (b)'s `r_w` 0.7500 to 1.0000 and the crowd's well blue for 15 and 20 of 24 (record 754, PR #777 pending); G2: 648 of 648 and the luminosity 648 of 648 (MET); T: 2.6517 and 4.1500, the ratio 1.907 for `1.909 +- 0.05` (MET); NATURE 12's presence word 1.000 against 2.00 (FAIL, the default word); X: nine of nine, inside 1.0029, outside 0.6285 (MET); the far lamp 11b `b = 1` (PASS pinned), 11a `q_eff = +1` against `-0.53` and 11c `n = 1` against 4 (FAIL pinned, not run) |
| Malus: `P(pass) = cos^2 theta` within the tables' rounding | SHOWN, rung 1 within `+0.0019` | the rotated label's Gram form (L9, L6) | A12 under the click: 128 / 0 / 64 of 256 (NATURE 9 PASS, MET exactly); 219 / 256 and 187 / 256 at 22.5 degrees (MET on the pins; OPEN at `10^-3`) |
| the Bell pair's `E(a, b)` and `S(N)` at two places, the marginals `1 / 2` exact | SHOWN, rung 1 (exact at every N) | one Gram form over two arms, one cell at two places (L6) | 27 / 5 / 5 / 27, `S = 2.75` for Hensen's `2.42 +- 0.20` (NATURE 1a PASS, MET); against Poh's `2.82759 +- 0.00051` REFUTED at N = 64 and 256 (FAIL), OPEN on the plateau 2.828125 |
| reflection | NEITHER | a row meets no surface; a mirror is the apparatus's declared table (input 23) | the register's mirrors are declarations (L1), no law read |
| refraction | NEITHER | no crowd slows or bends a row on `main` (5.4, P9); optical-v1 a hypothesis outside the law, no Snell there either | series K's 0.000 (the rows blind) |
| the bending and the delay by a mass | the Einstein Mathematician's; named, not derived | `main` blind; the every-family wall a hypothesis under its own identity | K 0.000; the optical pin worlds `-1.993 / -3.989`, the far worlds `-3.403 / +4.33` inside their pins, the delays' ratio 1.67 outside `2.00 +- 0.25` (NATURE 13 NOT COMPARED, gamma an input) |

**The verdict line: LIGHT OUTSIDE FROM THE BOARD: PARTLY.** Every SHOWN
row is the Outside step (2) obtained from the Inside step (1) by the
conversion (3) of section 0, and nothing else. SHOWN under the nine lines
of the law, (A1) at the click and (A3) on every passage: the speed of light
Outside by a row's age and by a pulse and its return with its anisotropy
and its isotropic limit, `E = h f` and `lambda = h / p` as identities of
the release, the intensity's inverse square in the shell mean and its
`1 / r^0` on a beam, the two Doppler forms and the r-free round trip,
the aberration at first order, the two-slit law with its spacing from
the phase per age, the one click per record, the redshift through a
crowd as the product of three counts, Malus's cos^2 and the pair's
correlation; and MEASURED where the register reads them: Q (290 of
290), T (172; 1.907), G (288 of 288), G2 (648 of 648), X (nine of nine),
L1 and L2b (the spacing 23.5 for 23.3), `mz_equal` (64 / 0), A12 (128 /
0 / 64), the pair (2.75). FAIL, in the same font, where the law's `r =
1` meets nature's root: the Doppler at second order (4b, 0.2636 against
0.315) and with it the transverse and the aberration's second order; the
anisotropy of c at the register's grain (5a); the two-slit visibility
(0.966 against 0.98) and its correlation pin; the presence word's form
(12); the far lamp's brightness and Tolman's test (11a, 11c, pinned not
run); the precision Bell test at the registered N. MEASURED ONLY: the
lattice's ripple at finite r. NOT MADE: the two-way c after a detector,
the inverse square of light at two radii, the moving detector's one-way
ratio, the massive row's `h / p`. NEITHER: reflection and refraction.
The one line: every Outside formula of light is a ratio or a difference
of counts at clicks, the emitter's and the detector's, joined by the
flight's two accumulators, and where nature's formula has a root the
law's count has none, which the register reads and this document does
not hide.

## V. Three sentences for the paper (marked as such; the paper coordinator's to take or leave)

(i) Every equation of light the model reaches Outside is the same map
written for a named emitter and a named detector: the emitter's births
at its place pass Inside as a row with a content, a phase, a direction
and an age; the flight translates two accumulators at declared constant
rates and reads nothing; the click at the detector's place reads the
row's record and Born's form at one cell, and the Outside formula is a
ratio or a difference of the two detectors' own counts, so that the
speed of light, Planck's `E = h f`, the inverse square, the Doppler
forms, Young's fringes, the one click per quantum, the gravitational
redshift and Malus's law are shown, not assumed, at the rungs stated.
(ii) These come out with the lattice's own grain named at each: the
speed of light `Q |D| / T_D` per direction with `1 / c^2` from 2.954 on a
heading to 3.000 on the body diagonal and `1 / sqrt 3` in the limit, the
fringes to a pixel, the redshift through a crowd as the product of three
counts, and they match the register's detectors where it reads them
(290 of 290 face clicks at the derived tick, the fringe spacing 23.5 for
23.3, `1 + z` 2.6517 and 4.1500 for 2.650 and 4.150, one click per
record in 64 of 64). (iii) What the model does not have it states in the
same font: no root enters any count, so the Doppler, the transverse
shift and the aberration match nature at first order in `v / c` and miss
it at second (the registered 0.2636 against 0.315); light is neither
reflected nor refracted by any law of the model, only by declared
tables; and a reading at another place is always a detector at that
place, which is why every number above is a click and none is the tick.

## VI. Links

[The click frame at e26c1f43 (PR #769, not yet merged)](https://github.com/Closer24/Universe24/blob/e26c1f4300f62648a348d56ea82058606d82f55a/docs/designs/click_frame/DERIVATION.md):
section 0 (lines 8 to 202), section 7 (lines 688 to 923), section 8
(lines 924 to 1161), section 9, the conversion as a map (lines 1162 to
1319), section 10, Bell by the algebra (lines 1320 to 1507); [DERIVATIONS_BEAM](../../DERIVATIONS_BEAM.md)
sections 2, 3.2, 4.1, 4.2, 5.1, 5.2, 5.4, 6.4, 6.5, 6.7, 7.1, 9.3, 12.2,
13.2, 15.3, 23.2, 23.3, 24.1, 24.3, 27; [BEAM_LAW](../../BEAM_LAW.md)
sections 3 and 5 and its notes 37, 45 and 48;
[the statement of c](../light_speed/FORM.md); [the far lamp's
brightness](../far_lamp/BRIGHTNESS.md); [Malus](../malus/NOTE.md);
[every family under one wall](../one_wall/EVERY_FAMILY.md);
[NATURE](../../NATURE.md) rows 1a, 2a, 2b, 4b, 5a, 5b, 9, 11a to 11c, 12
and 13; [EXPERIMENTS](../../EXPERIMENTS.md) series Q, S, T, G, G2, X, L,
W, A12, the optical pin worlds, E15 and E16;
[TERMINOLOGY](../../TERMINOLOGY.md), the readings;
[HIGHLIGHTS 5.4](../../HIGHLIGHTS.md#54-the-detector), lines 360, 381,
395 to 403; the log's records 158, 394, 569, 709, 723, 754, 762, 768, 772
and 777 ([LOG_2026-09-20](../../LOG_2026-09-20.md)).
