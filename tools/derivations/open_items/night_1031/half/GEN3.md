# GEN3: Big Pic's three generations on the board

This is the Boss's deriver of the half-speed gear, writing at 2026-10-31, 02:5x UTC, for a pair of hostile readers.
I worked from the Boss's summary of Big Pic's #2187 comment 6537793603, items 5 to 8. I did not fetch the comment
itself in the 20 minutes.

The probe is probe_gen3.py. Its outputs are probe_gen3.txt and probe_gen3_run2.txt, and the two are byte-identical.
It runs with scratchpad/live/.venv/bin/python -I and reuses probe_half2, which carries HALF2's units, trains and
step.gear.

The rules the probe keeps:
- whole numbers only;
- Rule3's carry as the one division;
- Z[w] held as exact pairs p + q w, with w^2 = -1 - w, compared for equality only: no order and no root, as HALF2
  ruling 4 says for Z[r2] (Sofer and Big Pic to confirm for Z[w] too);
- no sign test and no INDICATOR in any act. The probe's membership tests are the prober's own, not the act's.

Every MEASURED below is a clock fact on the board. The masses, Koide's Q and the generations as physics are owed to
the click world.

## 1. On the board: the three doublets as the act's modes (MEASURED, twice)

**The units (part 1).**
- The 24 whole units are Q8, w Q8 and w^2 Q8, with w = (-1 + i + j + k) / 2.
- The three cosets are disjoint and cover the 24, w^3 = 1, and Q8 is normal.
- w's turn on the axes is i -> k, k -> j, j -> i, as Big Pic said.

**The kinds of the 24 (part 2).** The seven kinds come from the units alone, as Z[w] pairs:
- 1, 1' and 1'': the coset's phase 1, w or w^2;
- 3: the turn's trace;
- 2: 2 Re g;
- 2': 2 Re g times w^k;
- 2'': 2 Re g times w^2k, where k is the coset's index.

Their degrees are 1, 1, 1, 3, 2, 2, 2, and the squares sum to 24. The characters are orthonormal exactly: every
quotient, remainder and w part was checked.

**By characters, restricted to the 24 (part 3).**

| hand | its doublets under the 24 |
| --- | --- |
| E1/2 | 2 |
| E1/2 x T1, the half-speed hand on the three axes | 2 + 2' + 2'', each once (Big Pic's (b)) |
| HALF2's 8-gear train (2 G3/2) | 2 2' + 2 2'' |
| HALF2's 24-gear train | 4 2 + 4 2' + 4 2'' |
| the 8-gear train laid on each of the three axis rows (24 gears, L(g) x pi(g), signed permutations 48 of 48) | 4 2 + 4 2' + 4 2'' |

The last two rows have equal characters on all 48 (part 6). So **the half-speed hand on the three axes is HALF2's
24-gear train**, which is already on writer A's list as kinds ["E1/2", "E5/2", "G3/2", "G3/2"] at part 2. No new
train is needed. By HALF2's classification, a 24-gear signed-permutation train with this character is one orbit, so
the two forms differ only by a signed permutation of the gears. Reading 2 below needs the 8 x 3 labelling, whose gears
are named by axis row.

**The whole projectors and w's charge (part 4; the same on both 24-gear forms).**
- Pi_2 = SUM chi_2(g^-1) L(g), and Pi_c = SUM (chi_2' + chi_2'')(g^-1) L(g). Both are whole, because
  chi_2' + chi_2'' is whole.
- They satisfy Pi_2 + Pi_c = 12 I, Pi_2 Pi_2 = 12 Pi_2, Pi_c Pi_c = 12 Pi_c and Pi_2 Pi_c = 0. By traces their
  ranks are 8 and 16.
- **The charge** is Q = SUM over w's class of L(g) less SUM over w^2's class of L(g), each class 4 units, the two
  apart. Q is whole, antisymmetric and central in the 24, with Q Pi_2 = 0 and Q Q = -Pi_c.
  - On 2, Q is 0.
  - On 2' and 2'', Q is the complex structure that tells them apart.
  - Q is kept by the 24 whole units.
  - Each of the 24 lifts with r2 (the quarter turns' and the edge turns') sends Q to -Q, so those turns swap 2' and
    2''. Big Pic's "the quarter turns pair 2' with 2'' into G3/2" holds in whole numbers.

**Each doublet's share on each axis row (part 6).** The projector's trace per axis row is:
- 2: 32, 32 and 32 of 96;
- 2' + 2'': 64, 64 and 64 of 192.

Both are 1/3 exactly, with remainder 0. w's turn cycles the axis rows and keeps every irreducible subspace, so the
share of every doublet on every axis row is 1/3 (DERIVED). This is the board side of Big Pic's "each landing on each
axis with share 1/3".

**By the act's own steps (part 5).**

The setup is the 24-gear train of the 8-gear on the three axes, with step.gear, and a real symmetric coupling C kept
by the 24. C is not kept by all 48; a board coupling must be (see "What a real spring can part" below).

Results:
- **Where W divides every push** (W = 5, push W C - 2 W, 12 rounds), the tooth never moved. A hand laid in 2 keeps
  0 in 2' + 2'' at every round, and a hand laid in 2' + 2'' keeps 0 in 2. The act's modes split exactly by the
  characters.
- **Where the carry rounds** (W = 10^6 and 6 x 10^5, 400 rounds), the tooth moved at every gear in every round. The
  largest entry of the other part (x12) stays at 800 to 1,000, against the hand's own part of 107,712 to 149,158 (x12).
  The split holds to the carry's rounding: a board reading, at below one per cent here.

**What a real spring can part (DERIVED).**
- C commutes with Q (measured: Q is central).
- So every real eigenspace of C carries Q's complex structure, and its complexification holds 2' and 2'' equally.
- Hence **a real spring gives 2' and 2'' the same rates**. A real spring kept by the 24 can still give 2 a rate apart
  from 2' + 2''.
- A coupling kept by all 48, which the board's 24 turns require (line 94), meets the r2 lifts that swap 2' and 2''.
  So any such coupling, symmetric or not, gives them equal rates.
- So on the act as built: at most two rates, never three.

## 2. The parting coupling

**What it must be (DERIVED from part 4).**
- A term that parts 2' from 2'' must be odd in Q, so it is antisymmetric on the gears.
- As a push on the now slot it would be a curl force: complex rates, not a clock.
- As a conservative term it must act on the rates: Q (a - b), a gyroscopic hop.
- Q (a - b) flips under the r2 lifts (Q -> -Q) and under the run back ((a - b) -> -(a - b)). Times a charge that flips
  under both, it is kept by every symmetry of the board.
- The held hand's sigma = a_A1 a_A2' - a_A2 a_A1' is such a charge: A2 flips under the quarter turns, and the rates
  flip under the run back.
- So sigma Q (a - b) is the shape. Big Pic's "the held hand's charge on the axes' antisymmetric hop on the rates" is,
  in whole numbers, sigma times the central antisymmetric class difference Q on the train's rates.

**Can it be written lawfully?**
- **No sign test and no INDICATOR: yes.** sigma is a polynomial in the held hand's slots, Q is a whole matrix laid at
  load from the two class sums, and the term is products and sums.
- **No typed number: almost.**
  - Q's entries come from the structure.
  - Which class is w's and which is w^2's is an orientation, a choice that is the same as the sign of the term's
    strength.
  - The strength would be CHOSEN in the universe file, as hold, tie and mesh are.
  - Q is the half x half -> A2 antisymmetric channel of the 48: it is kept by the 24 and flips under the r2 lifts.
- **From the families' law: NO, so it is OPEN.** Three causes:
  - (i) The act's push reads the now slot alone. That is the mirror theorem's hypothesis (d): with a push P(a), the
    mirrored tick returns (b, a, -1 - s) exactly. A rate leg (a - b) breaks that. A reversible gyroscopic step needs
    the midpoint rate (a+ - b), which is implicit: a matrix division, not Rule3's carry.
  - (ii) sigma is a product of the held hand's now and before slots, a time-odd A2 quantity. The families' tables lay
    value legs only (the value, the gradient, the pull, the unit), so no table of the law yields it.
  - (iii) The owner's line 102: it must come from the families' law, never be typed, and no family's coupling gives
    it tonight.

## 3. The road to Big Pic's five click readings (each to be read twice in the click world)

**Common to all five:**
- HALF2's 24-gear train laid (writer A, items 1 and 2 now; in-memory test worlds only, HALF2 item 5);
- a click channel, which needs a half-speed table from the families (HALF2's gate: the passing is 0 on an untied
  train);
- a clock's own clicks (the critical path).

| reading | needs beyond the common | status |
| --- | --- | --- |
| 1. three species' own clocks at rest, three rates | the parting coupling (section 2) for the third rate; two rates at most without it | OPEN |
| 2. each species' quanta landing on each axis row with share 1/3 | a click that names the row (the third click failed its law tonight) | OPEN; its board side MEASURED (part 6) |
| 3. a heavier species' line ending in lighter ones | three rates (reading 1) and a channel between the doublets (a half-speed table with a whole-speed leg) | OPEN |
| 4. Koide's Q from the three rates, within the calibre | reading 1, and the calibre condition (the clock's cure) | OPEN |
| 5. the Michelson reading with the held hand turning | the held hand inside its window (the tie), sigma on the board (section 2), and a two-arm world in the click world | OPEN |

**The first that could be read: reading 2.**
- It needs no parting: every doublet's share is 1/3 whether parted or not (part 6).
- It does need the common three, plus a click that names the row.
- It can be read on species 2 against 2' + 2'', which a real spring already separates.

## 4. Tonight: what can be built, and what cannot

**Can be built tonight**, as in-memory tests on writer A's items 1 and 2:
- the 24-gear train as the half-speed hand on the three axes;
- the 24 whole units as three cosets, with the coset index read by the product;
- the seven characters of the 24 as Z[w] pairs, or only their whole sums (chi_2 and chi_2' + chi_2'' are whole);
- the whole projectors Pi_2 and Pi_c, and Q, as load-time readings with their identities:
  Pi_2 + Pi_c = 12 I, Q Pi_2 = 0, Q Q = -Pi_c, and Q -> -Q under the r2 lifts;
- the modes kept exactly where W divides every push, and to the carry's rounding elsewhere.

Each of these has its no, already in the probe:
- a non-lift breaks equivariance (HALF2);
- a hand laid in 2 has 0 in Pi_c only while nothing rounds.

**Cannot be built tonight:**
- the parting coupling (section 2: no rate leg in the act, no sigma from the families' law);
- a third rate;
- any click of the half-speed train (no half-speed table);
- the click that names the row;
- a clock's own clicks;
- all five click readings;
- the generations, masses and Koide's Q as physics, which stay owed to the click world.

The board shows three doublets, two rates at most, and a charge Q that would part the third, which no lawful term
carries yet.
