# Light Outside from the board: every equation of light Inside, carried Outside by its own transformation to a named detector at a named place (the owner's order, 2026-09-22, about 05:55Z, as the Boss relayed it)

The Light Mathematician, 2026-09-22, on the Boss's order; a derivation
on paper in the shape of the click frame's sections 0 and 8 (the click
frame at 3268e7d5, PR #769, not yet merged, cited by its line numbers
and not edited); no code, no world file, no run; every number a closed
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

## 0. The frame: Inside, Outside, and the one map of every row

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
   24.1 row 7 at line 6985 and section 27 at line 7948).
4. `Inside -> Outside_B`, the click: the detector at B reads the
   arrival's record through its declared reading (BEAM_LAW lines 774 to
   830: the threshold, the `wave` pointer, the record `X^2 + Y^2`), and
   under the one click of a record (BEAM_LAW note 37 (x), line 2849; the
   ladder) one cell of one detector clicks once per record, its weight
   the click's bilinear form (DERIVATIONS_BEAM 6.7, line 1813), the
   probability of the cell within `1 / (2 N)` of Born's (23.2, line
   6762). What passes Outside is the click's triple; what never passes
   singly is the amount and the phase of one record (the click frame line
   897 to 912, its second fact).
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
  3625; 24.1 rows 9 and 10, lines 6987 to 6988;
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
  (6.4 lines 1521 to 1555; 24.1 row 25, line 7011: a calibration, the
  value of h an input). "No rule makes the content of a row follow its
  frequency in flight" (6.4, line 1519).
- **(L5) The spreading over the six Ports.** "On a beam the flow per Node
  is `amount x u_d`, the same at every Node of the digital line: the
  field along a beam is `1 / r^0`, and off every beam it is 0 ... The
  inverse square is the density of beams over a shell": the shell mean `q
  Q / N(r) -> q Q / (4 pi r^2)` in space with the ripple of `N(r)`, the
  lattice's count of Nodes on a shell (DERIVATIONS_BEAM 3.2, lines 874 to
  937; 5.1, lines 1168 to 1211: the presence `q dwell / (4 pi r^2)`, the
  age moment `q dwell / (4 pi c r)`). This is the arithmetic of six
  Ports and a fan of K directions, not a law (the click frame line 967,
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
  member, 24.1 row 12, line 6990); Born's `|psi|^2` "holds AT THE CLICK
  as the cell's probability to within `1 / (2 N)`, and nowhere between
  clicks" (23.2, lines 6800 to 6810). One record, one click: the ladder
  chooses one cell by the birth phase u and deletes the record's offers
  in the same interval (BEAM_LAW note 37 (x), line 2849; EXPERIMENTS E15,
  line 9836). In the click frame's table this is the row "the click's
  bilinear form" (line 892): the conversion's (A2) at the click.
- **(L7) The crossing rule.** "a row and a body meet ONCE, at the crossing
  of their world lines" (BEAM_LAW note 48, lines 530 to 532;
  DERIVATIONS_BEAM 2.2, lines 655 to 706, and 9.3, lines 2221 to 2241;
  24.1 row 22, line 7008: DERIVED given the flight and the drive). Its
  count on an axis: `1 + v / c` toward the lamp, `1 - v / c` away, 1
  transverse, exact over whole Links and within one row otherwise
  (`tests/test_crossing.py`, the pinned counts).
- **(L8) The age wall at coefficient 1 on every count.** "a count at the
  rate `rate` against the wall `wall` becomes the count at `rate x d`
  against `wall x (d + a_tau n)`" (`core.integer.age_wall`; the click
  frame's (N2), lines 940 to 948): a body's self-creations, a lamp's
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
