# The Gleason bound: what the tables' rounding does to hypothesis (a), and the weight of a mixture the register cannot exclude (the Gleason Bound Mathematician, docs only, 2026-09-22)

The order: the Boss's brief of 2026-09-22 on the owner's second referee
read, verified by the paper writer at 10:05Z (record 916 (b) of the log
of 2026-09-20): the rounding of the tables breaks hypothesis (a) of the
lattice Gleason theorem on the referee's example `f = 256 x^8 - 181 (1 +
x^16)` at N = 64, and the paper's sentence "excludes every mixture"
(Section 6, the paragraph "Against the registered integers",
`paper/general_formula/main.tex` line 1004 on `main`) is too strong
without a bound. The writer narrowed the sentence on the owner's direct
word (record 921; the paper branch `claude/paper-owner-review-five` at
65674bcb, `main.tex` line 805, and at e6117ef6 after the cut, line 794,
the sentence unchanged): "exclude every mixture the readings resolve; a
mixture of a weight below the readings' rounding cell is not excluded,
and the bound on that weight is not computed", and the norm range said
to bound "one phasor's error ... and not the relative error of a sum
that nearly cancels, for which no theorem is given". This note computes
that weight and gives that theorem. Read against `main` at 30c84db7
(PR #843): the theorem and its hypotheses (`main.tex` lines 912 to 975), the tables'
definition and norm range (Appendix, the technical details, lines 1457 to
1470), the rounding rule ([DERIVATIONS_BEAM 6.2](../../DERIVATIONS_BEAM.md),
the three roundings declared once: the rung, the tables at the scale 256,
the wheel), the tables as integers (`core/phase.py`; the listing
[tables.txt](../amplitude-v1/tables.txt)), the Malus map
([malus_map.out](../malus/malus_map.out) sections 2 and 4), the Born note
([NOTE.md](../open_problems/born/NOTE.md) sections 2 and 4), records 817
and 894 of the log of 2026-09-20. Every number here is from
[bound_map.py](bound_map.py) beside this note, run on the engine's own
tables (`event_universe.core.phase`, host arithmetic, no run) with its
output [bound_map.out](bound_map.out); a number read from the register is
labelled DETECTOR with its line, a number computed from the tables is
labelled GAMEBOARD by formula. Gleason's theorem, Born's rule and quantum
mechanics' forms appear only as the thing compared with, never as an input
(record 817); no physical law changes; no rule is proposed, so the three
tests (generic, vector, local) have nothing to admit here.

Notation. N (the phase circle, 64), T (the tables' scale, 256), x (the
generator of one phase step), `zeta` (the primitive N-th root of unity),
`f = sum_p f_p x^p` (a record's element of the group ring, `f_p` the
integer amount at the phase p; the record's phase-count vector **f**),
`ev(f)` (the pointer, `sum_p f_p zeta^p`), C[p] and S[p] (the tables,
`round(T cos(2 pi p / N))` and `round(T sin(2 pi p / N))`), (X, Y) (the
built pointer, `X = sum_p f_p C[p]`, `Y = sum_p f_p S[p]`; the engine forms
it with the amplitudes 32 x amount, `nature_beam.coherent_pointer`, a
common factor that changes no ratio and is dropped here), (X*, Y*) (the
exact pointer, `T ev(f)`), R (the built weight, `X^2 + Y^2`, the click's
Gram form **f**^T **G** **f** with **G** = **E**^T **E** the Gram matrix of
the tables), R* (the exact weight, `X*^2 + Y*^2 = T^2 |ev(f)|^2`), A (the
record's total amount, `sum_p |f_p|`), `sigma_j` (the j-th Galois
evaluation, `sum_p f_p exp(2 pi i j p / N)`, `sigma_1 = ev`), `c_j` (the
click's harmonic constants), w (the weight of a mixture: the part of
`sum_j c_j = 1` that lies off the class of the fundamental), W (the birth
wheel, 256 in the Malus worlds), a cell (the resolution of a reading: one
count of W at the polariser, one click at a pixel of the two slits).

## 0. The verdicts, stated at the top

| Question | Verdict |
| --- | --- |
| Does the tables' rounding break hypothesis (a), `R(x f) = R(f)`, on the built click? | **YES, and by more than the referee's numbers**: on `f = 256 x^8 - 181 (1 + x^16)` the built click reads R = 0 as written, R = 196 rotated by 8 steps and R = 25028 rotated by 1 step, where the exact weight is R* = 49.005 at every rotation (0, 0.00299 and 0.38190 against 0.000748 in the unit of the tables' scale); section 1 (GAMEBOARD by formula) |
| Is the paper's "a part in 276" the bound? | **NO, it is the one-row case**: for a record of total amount A the built pointer is within A / 2 of the exact one per component (lemma 2), the built weight within `A sqrt(2 R*) + A^2 / 2` of the exact (lemma 3), a part in 181 at full scale and **no relative bound at a cancellation**; section 2 |
| What weight of a mixture does the register exclude? | Malus at 22.5 degrees (219 of 256, DETECTOR) excludes every mixture of weight above **w* = 0.00066 = 1 / 1516** on the harmonics `j = +-3 mod 8` (the count falls to 218 above it; the margin-free bound, one whole cell, is 1 / 181 = 0.0055); Malus bounds **nothing** on `j = +-1 mod 8` (j = 7, 9, 15, 17, 23, 25, 31 read exactly as j = 1 at 22.5, 45 and 90 degrees); the two-slit bands exclude a weight above about **0.019** on that class (one click at the peak of 51, DETECTOR); section 3 (GAMEBOARD by formula) |
| Does the bound reach the readings' cell? | At the polariser **yes, below it**: the cell is 1 / 256 = 0.0039 and w* = 0.00066, because a unit of weight moves the reading by 181 cells; at the two slits **no**: the bound is the bands' own cell (one click in 51) and rests on the pixels' margins, not read here |
| The sentence for the paper | Section 4, in two forms |
| The table click's zeros (the Boss's added item) | At N = 8192 **two rows of amount 1** at the phases 0 and 4097 read (0, 0) on the tables where the ideal `|ev(f)|^2 = 5.9 x 10^-7` (1952 distinct table pairs among 8192 phases; 64368 two-row zeros with amounts 1 to 4); at N = 64 **NONE FOUND** up to three rows at distinct phases with amounts 1 to 4; the converse (an ideal zero reading nonzero on the tables) **cannot exist**, by the tables' exact antisymmetry; section 5 (COMPUTATION) |
| Not proved | Section 6, one line |

## 1. Hypothesis (a) as the theorem has it, and its failure on the referee's example

The paper's hypothesis (a) (`main.tex` line 912), verbatim: "(a) The
phase rotation, `R(xf) = R(f)`: a rotation of the record's phase by one
step changes no weight (the rungs take no u; u only selects among them),
an operation of Section 2." The theorem (line 934) is about the ideal
reading `R` on the lattice `Z[zeta_N]`; the paper then says (line 1004)
that the built click is this form "to the tables' rounding", names the
one-row violation (`C[1]^2 + S[1]^2 = 65650`, the extreme a part in 276)
and the norm range of the appendix as "the error bound between the two".

The tables at N = 64 as integers (the engine's `phase_cosines(64)` and
`phase_sines(64)`; equal to `round(256 cos(2 pi p / 64))` and
`round(256 sin(2 pi p / 64))` entry by entry, checked for every power of
two N from 4 to 65536, no entry differing; bound_map.out section 1):

```
C[0..63] = 256 255 251 245 237 226 213 198 181 162 142 121 98 74 50 25 0 -25 -50 -74 -98 -121 -142 -162 -181 -198 -213 -226 -237 -245 -251 -255 -256 -255 -251 -245 -237 -226 -213 -198 -181 -162 -142 -121 -98 -74 -50 -25 0 25 50 74 98 121 142 162 181 198 213 226 237 245 251 255
S[0..63] = 0 25 50 74 98 121 142 162 181 198 213 226 237 245 251 255 256 255 251 245 237 226 213 198 181 162 142 121 98 74 50 25 0 -25 -50 -74 -98 -121 -142 -162 -181 -198 -213 -226 -237 -245 -251 -255 -256 -255 -251 -245 -237 -226 -213 -198 -181 -162 -142 -121 -98 -74 -50 -25
```

The norms `C[p]^2 + S[p]^2` take the eight values 65448, 65501, 65522,
65533, 65536, 65650, 65717, 65773 (the paper's eight totals). The entry
that matters: `C[8] = S[8] = 181` where `256 / sqrt 2 = 181.01934`.

The referee's example. `f = 256 x^8 - 181 (1 + x^16)`; under the cancel
`x^32 = -1` the rows are the amounts 256 at the phase 8, 181 at 32 and
181 at 48, the total amount A = 618. Exactly, `ev(f) = 256 zeta^8 - 181 -
181 zeta^16 = (256 / sqrt 2 - 181) (1 + i)`, so `|ev(f)|^2 = 2 (256 /
sqrt 2 - 181)^2 = (256 - 181 sqrt 2)^2 = 0.000748`: the referee's 0.00075,
in the unit of the tables' scale; `R* = 65536 x 0.000748 = 49.005` in
the integer scale, and it is one number at every rotation. The built
readings (bound_map.out section 3):

| rotation | the rows (phase: amount) | the terms `amount x (C, S)` | (X, Y) | R | R / 65536 |
| --- | --- | --- | --- | --- | --- |
| as written | 8: 256, 32: 181, 48: 181 | `256 x (181, 181)`, `181 x (-256, 0)`, `181 x (0, -256)` | (0, 0) | 0 | 0 |
| by 8 steps, `x^8 f` | 16: 256, 40: 181, 56: 181 | `256 x (0, 256)`, `181 x (-181, -181)`, `181 x (181, -181)` | (0, 14) | 196 | 0.00299 |
| by 1 step, `x f` | 9: 256, 33: 181, 49: 181 | `256 x (162, 198)`, `181 x (-255, -25)`, `181 x (25, -255)` | (-158, 8) | 25028 | 0.38190 |

So `R(f) = 0`, `R(x^8 f) = 196` and `R(x f) = 25028` on the built click
against the one exact `R* = 49.005`: hypothesis (a) fails on the tables,
as the referee says, and the rotation by one step, the very rotation (a)
names, fails it five hundred times over the exact weight. The reason is
in the terms: `256 x 181 = 46336` cancels `181 x 256 = 46336` exactly
because the rounded `C[8] = 181` equals the coefficient 181, where the
exact `256 x 181.019 = 46341` does not; and after one step the three
terms carry three independent roundings (162 for 162.41, 255 for 254.98,
25 for 25.08) whose residues, multiplied by the amounts 256 and 181, no
longer cancel.

## 2. The bound on a sum under the tables' rounding

**Lemma 1 (the entry).** `|C[p] - T cos(2 pi p / N)| <= 1 / 2` and
`|S[p] - T sin(2 pi p / N)| <= 1 / 2` for every p. Proof: the tables are
the roundings to the nearest integer; the engine's fixed-point series
gives exactly those roundings at every power of two N from 4 to 65536
(bound_map.out section 1, 0 entries differing), so the lemma holds on
the engine's tables as verified integers, not only on the definition.

**Lemma 2 (the sum).** For a record of amounts `f_p` with total
`A = sum_p |f_p|`, `|X - X*| <= A / 2` and `|Y - Y*| <= A / 2`. For a sum
of k terms of magnitude at most M, `|X - X*| <= k M / 2`. Proof:
`X - X* = sum_p f_p (C[p] - T cos(2 pi p / N))`, the triangle inequality
and lemma 1. The bound is attained in the sign pattern, so no smaller
constant holds for every f.

**Lemma 3 (the weight).** `|R - R*| <= A sqrt(2 R*) + A^2 / 2`. Proof:
`X^2 - X*^2 = (X - X*) (2 X* + (X - X*))`, so `|X^2 - X*^2| <= (A / 2)
(2 |X*| + A / 2)`; the same for Y; adding, `|R - R*| <= A (|X*| + |Y*|) +
A^2 / 2 <= A sqrt(2 R*) + A^2 / 2` by `|X*| + |Y*| <= sqrt 2 sqrt(X*^2 +
Y*^2)`.

**Corollary (the relative error).** `|R - R*| / R* <= A sqrt(2 / R*) +
A^2 / (2 R*)`. At full scale (the aligned record, `R* = (T A)^2`) this is
`sqrt 2 / T + 1 / (2 T^2) = 0.00553`, a part in 181; it grows without
bound as `R*` falls, and for a sum that cancels to below `A / 2` per
component (`R* < A^2 / 2`) the tables bound the reading's absolute error
by `A / 2` per component and its relative error by nothing: the reading
may be 0 (the referee's f as written, `R* = 49`) or `A^2 / 2` (the same f
after one step reads 25028; the bound `A^2 / 2 = 190962`). The
violation of (a) is bounded the same way: `|R(x f) - R(f)| <= 2 (A
sqrt(2 R*) + A^2 / 2)`, both readings lying within lemma 3 of the one
`R*`; on the referee's f, 197080, which holds the observed 25028.

**The paper's sums, with their k and M** (bound_map.out section 4):

| the sum | k | M | the bound of lemmas 2 and 3 | the tables' actual |
| --- | --- | --- | --- | --- |
| one row, the record's total over the 64 birth phases (`main.tex` line 1004, the appendix line 1470) | 1 | 1 | `|R - 65536| <= 256 sqrt 2 + 1 / 2 = 362.5` | 237 (65773), the eight values from 65448 to 65773: the paper's "a part in 276" is this row alone |
| the Mach-Zehnder's dark port, two rows a half turn apart (the pins 0 / 64) | 2 | equal | the sum is exactly 0 | exactly 0, by `C[p + 32] = -C[p]`, `S[p + 32] = -S[p]` (the exact antisymmetry of the tables: the two roundings are the same rounding with opposite sign, so they cancel; not a case of lemma 2's worst pattern) |
| the quarter turn, two rows 16 steps apart (the pin 32 / 32) | 2 | equal | `|R - 131072 M^2| <= M^2 (2 sqrt 2 x 362 + 2) = 1026 M^2` | R over the 64 phases in `[130896, 131546] M^2`: within 474 of the exact |
| the aligned record of total amount A | any | any | a part in 181 | the one-row 237 / 65536 = a part in 276 is the observed extreme |
| the referee's f, three rows that cancel | 3 | 256 | `A / 2 = 309` per component; no relative bound | the errors 4.95, 7.00 and 162.4 per component; the relative errors 1, 3 and 510 |

The paper's sentence "the built click is this form to the tables'
rounding, ... the norm range of Appendix A is the error bound between
the two" is therefore true of one row and false of a record: the bound
between the ideal `R` and the built click is lemma 3's, `A sqrt(2 R*) +
A^2 / 2`, and it bounds no ratio where the record's rows cancel. The
paper's registered pins are not touched by this: the Mach-Zehnder's
0 / 64 cancels exactly by the antisymmetry, and the (3, 4) split, the far
pair, the two slits and Malus are read through the rung, whose cell (one
count of W) is what section 3 measures the rounding against.

## 3. The weight of a mixture the register cannot exclude

**The family and the classes.** The theorem's admissible readings are
`R = sum_j c_j |sigma_j(f)|^2` over the odd j below N / 2, sixteen
constants at N = 64; the fundamental is `c_1 = 1`. Under the tables the
member j is built from the same rounded tables at the relabelled phases
(`sigma_j` through the tables is `sum_p f_p (C[j p mod N], S[j p mod N])`,
`p -> j p` a permutation of the circle for odd j), so every member and
every mixture has a built click, and lemmas 1 to 3 hold for each member
alike. A mixture of weight w puts `1 - w` on the fundamental's class and
w off it, however spread.

**Malus at 22.5 degrees** (the Born note's section 4; the Malus map's
section 2). The polariser reads the half-angle tables of 2N = 512 at the
window 32 (22.5 degrees): the member j reads the pass weight
`C'[32 j]^2` against the absorbed weight `S'[32 j]^2` and the count of W
= 256 births by the rung `b = (2 W C + T) // (2 T)` on the cumulative
weight C over the total T (bound_map.out section 5):

| the class | the members j | C'[32 j], S'[32 j] | the pass weight | the absorbed weight | the pass x 256 / T | the count of 256 |
| --- | --- | --- | --- | --- | --- | --- |
| `+-1 mod 8` | 1, 7, 9, 15, 17, 23, 25, 31 | +-237, +-98 | 56169 | 9604 | 218.620 | 219 |
| `+-3 mod 8` | 3, 5, 11, 13, 19, 21, 27, 29 | +-98, +-237 | 9604 | 56169 | 37.380 | 37 |

The total T = 65773 is the same for every member. The register's
DETECTOR numbers, with their lines: the pass 219 of 256 at 22.5 degrees
and the chain's 187 of 256 (A12 extended at 22.5 degrees, record 395 of
the log of 2026-09-20; `main.tex` line 1208, the checks table, and line
1261, the nature table's row 9; [EXPERIMENTS.md](../../EXPERIMENTS.md)
line 6580; [DERIVATIONS_BEAM 24.3](../../DERIVATIONS_BEAM.md) row 4,
line 7066). The reading's cell is one count of 256, `1 / 256 = 0.0039`.
The built fundamental's number is `256 x 56169 / 65773 = 218.620`
(the exact `256 cos^2(22.5 degrees) = 218.510`), and the rung reads 219
as long as the cumulative pass weight is at least `28742801 / 512 =
56138.283`: a margin of 30.717 on the weight, 0.1196 of a cell.

**The bound.** A mixture of weight w on the class `+-3 mod 8` has the
pass weight `56169 - 46565 w` (the shift per unit weight 46565 on the
weight, 181.24 cells), so its count is 219 if and only if `46565 w <=
30.717`:

- **w* (the polariser) = 15727 / 23841280 = 0.000660 = 1 / 1516**
  (GAMEBOARD by formula): a mixture of weight above w* on the class
  `+-3 mod 8` reads 218 of 256 and is excluded by the registered 219; a
  mixture of weight below w* reads 219 and is not excluded.
- **w* (the chain) = 0.001089 = 1 / 919** (GAMEBOARD by formula, the
  Malus map's section 4: the cell 0+ of the chain has the fundamental's
  weight `56169^2` of `65773^2`, the class `+-3` the weight `9604^2`, the
  pinned 187 kept while the cumulative weight is at least
  `373 x 65773^2 / 512`): weaker than the polariser's.
- **The margin-free bound, 1 / 181.2 = 0.0055** (GAMEBOARD by formula):
  a mixture whose shift is one whole cell, `46565 w >= 65773 / 256`, is
  excluded whatever the margin of the built number inside its cell; w*
  below it rests on the margin 0.1196 of a cell that the tables of 512
  happen to give at the window 32, an exact integer fact of the tables
  and not a robust one (a table that rounded 218.620 to a margin of
  0.001 would bound w at 0.000006, one that rounded it to 218.49 would
  read 218 already).
- **The class `+-1 mod 8`**: the members 7, 9, 15, 17, 23, 25 and 31 read
  the pass weight 56169 at 22.5 degrees, 1 / 2 at 45 degrees and 0 at 90
  degrees exactly as the fundamental does (the Born note's line, "admits
  j = +-1 mod 8"); Malus bounds nothing on a mixture within this class,
  at any weight.

**The two-slit bands on the class `+-1 mod 8`** (bound_map.out section
6). The DETECTOR numbers: the bright pixels 19 to 51 clicks of 4096
births, the dark 0 to 3, the visibility 0.966, the rungs within one
(`main.tex` line 1204; series L2b). The member j reads `1 + cos(2 pi j
D / 64)` where the fundamental reads `1 + cos(2 pi D / 64)` at the phase
difference D of a pixel, so a weight w on `j != 1` moves a pixel's count
by at most `w |cos(j t) - cos t| x 51 / 1.966 <= 51.9 w` clicks. One click
is the cell: a change of one whole click needs `w >= 0.0193`
(GAMEBOARD by formula from the peak 51 and the visibility). Above about
0.02 a pixel's count must change; below it the bands exclude a mixture
only through the pixels' margins inside their rungs, which this note did
not read. The bands' cell, one click in 51, is thus the bound on the
class Malus is blind to; the fringe of period `23.5 / j` pixels that the
Born note names (3.4 pixels at j = 7) is what would be seen above it.

**The Mach-Zehnder and the pair** (the Born note's section 4) read the
phase differences 0, 16 and 32, where `cos(2 pi j D / 64)` is 1, 0 and
-1 for every odd j: blind to every mixture, at every weight.

## 4. The one sentence for the paper (Section 6, line 1004), in two forms

The sentence on `main` (line 1004): "... and Malus at 22.5 degrees
(219/256 and 187/256 exact) admits `j = +-1 mod 8` and excludes every
mixture: the register pins the fundamental, and the least-rank click
(P10) stores it." The sentence on the paper branch (65674bcb, line 805;
record 921): "... admit the harmonic `j = +-1 mod 8` and exclude every
mixture the readings resolve; a mixture of a weight below the readings'
rounding cell is not excluded, and the bound on that weight is not
computed: the register pins the fundamental to that resolution, and the
least-rank click (P10) stores it." The two forms below sharpen the
narrowed sentence into its number; the writer takes one of them on the
merge SHA and the owner's word.

**Form 1, with the weight:** "... and Malus at 22.5 degrees (219/256 and
187/256 exact) admits `j = +-1 mod 8` and excludes every mixture of weight
above `w = 0.00066` on `j = +-3 mod 8`, w the part of `sum c_j = 1` off the
fundamental's class, read as the count of 256 that falls from 219 to 218
(the margin of the built 218.620 above the rung's 218.5, over the shift of
181 counts per unit weight); the two-slit bands exclude a weight above
about 0.02 on `j = +-1 mod 8` (one click at the peak of 51): to these
weights the register pins the fundamental, and the least-rank click (P10)
stores it."

**Form 2, where the bound does not reach the cell:** "... below these
weights the register does not exclude a mixture: not below 0.00066 on
`j = +-3 mod 8` (the polariser's count of 256 does not move), and not
below the bands' cell, one click in 51, on `j = +-1 mod 8`, where Malus at
22.5, 45 and 90 degrees reads every member alike."

And for the sentence before it (on `main`, "the built click is this
form to the tables' rounding ... the norm range of Appendix A is the
error bound between the two"; on the paper branch, "the norm range of
Appendix B bounds one phasor's error between the ideal reading and the
tables and not the relative error of a sum that nearly cancels, for which
no theorem is given"), the bound as proved, lemma 3 being the theorem
the branch says is not given: "to the tables' rounding: within
`A sqrt(2 R*) + A^2 / 2` of the exact weight `R*` for a record of total
amount A (a part in 181 at full scale, the one-row extreme a part in
276), and with no relative bound where the record's rows cancel below
A / 2 per component, where hypothesis (a) fails on the built click
(`f = 256 x^8 - 181 (1 + x^16)` reads 0, 196 and 25028 at three
rotations against the exact 49)".

## 5. The table click's zeros (the Boss's added item, 11:50Z; kind: COMPUTATION)

The reader's point. The paper (Section 6, after the objects; the paper
branch at 65674bcb, `main.tex` lines 733 to 735) says "ev is the identity
on it: the GameBoard's cancel and the click's zero are one relation,
exactly", where the click is the ideal evaluation `ev` on `Z[zeta_N]`.
The reader says the TABLE click, `R(f) = X^2 + Y^2` with `(X, Y) = (sum_i
a_i C[p_i], sum_i a_i S[p_i])` on the declared integer tables (the engine
forms it with the amplitudes 32 x amount, `AMPLITUDE_SCALE` in
`events/amplitude.py`; a common scale, the Boss's 512 included, changes no
zero), has additional zeros: elements f nonzero in `Z[zeta_N]` whose table
reading is exactly (0, 0). Searched by computation
([zeros_map.py](zeros_map.py), its output [zeros_map.out](zeros_map.out)):
every f with at most three rows at distinct phases and amounts 1 to 4, at
every phase (the sign `p -> p + N/2` is exact on both sides and is used;
the phase rotation is no symmetry of the table reading, section 1, and is
not used to cut the search), at N = 64 and at N = 8192 (the Bell
plateau's tables, `main.tex` line 888). Nothing here is a measurement.

**The structure, before the search.** The table pointer is a Z-linear
map of the group ring `Z[Z_N]` (rank N) onto a lattice of rank 2 in
`Z^2`, so its kernel has rank N - 2; the cancel's kernel, the ideal `(1 +
x^(N/2))` of the antipodal pairs, has rank N/2. The first contains the
second (the converse below), so the table click's additional zeros are a
lattice of rank N/2 - 2 inside `Z[zeta_N]` (rank N/2): none at N = 4, rank
2 at N = 8, rank 30 of 32 at N = 64, rank 4094 of 4096 at N = 8192. Any
three rows at any three distinct phases have a table zero with some
integer amounts (three vectors of `Z^2` are Z-dependent; the referee's f
is one at N = 64 with the amounts 256, 181, 181), while in `Z[zeta_N]`
three rows at distinct phases are never dependent. What the search
measures is how small the amounts of a zero get.

**The search** (zeros_map.out):

| N | distinct (C, S) pairs among the N phases | one row | two rows | three rows (gcd of the amounts 1) | the smallest example |
| --- | --- | --- | --- | --- | --- |
| 64 | 64 of 64 | none (`C^2 + S^2 >= 65448`) | none | none | **NONE FOUND** up to three rows at distinct phases with amounts 1 to 4 |
| 8192 | 1952 of 8192 (6240 phases repeat an earlier pair) | none (`C^2 + S^2 >= 65192`) | 64368 unordered sets | 4971336 unordered sets; the smallest three rows of amount 1 at the phases 0, 2728 and 5460 (a third of the circle apart, 2730.67 steps), the ideal `|ev(f)|^2 = 3.136 x 10^-6` | two rows of amount 1 at the phases 0 and 4097 (or 0 and 4095): `f = 1 + x^4097 = 1 - x` in `Z[zeta]`, the ideal `|ev(f)|^2 = 4 sin^2(pi / 8192) = 5.883 x 10^-7` (the tables' scale as the unit), the table reading `(256, 0) + (-256, 0) = (0, 0)`, R = 0 |

At N = 8192 the sine's step near the axis is `256 x 2 pi / 8192 = 0.196`
per phase, so five consecutive phases round to the same table pair (`S[0]
= S[1] = S[2] = 0`, `C = 256`), and the pair at 4097 is exactly the
negative of the pair at 0: two rows a phase step past antipodal cancel
exactly on the tables and not in the ideal. At N = 64 every phase has its
own pair and its negative sits only at `p + 32`, so the smallest table
zero needs amounts beyond 4 (the referee's 256, 181, 181 is one; the
bound of the search is three rows and the amount 4, stated).

**The converse.** An ideal zero whose table reading is not (0, 0) cannot
exist: CONFIRMED. The kernel of `ev` on `Z[Z_N]`, N a power of two, is the
ideal `(1 + x^(N/2))`, the antipodal pairs of equal amounts, and the
tables are exactly antisymmetric, `C[p + N/2] = -C[p]`, `S[p + N/2] =
-S[p]` (checked at every power of two from 4 to 65536, zeros_map.out's
last line), so the Z-linear table reading kills every such pair; this
holds whether the merge cancels before the tables or the tables see the
pair, the two being one relation for ideal zeros, as the paper says. The
relation is one-way: every ideal zero is a table zero, not the converse.

**One line for the paper, in the paper's words** (after "one relation,
exactly"): "The built click on the tables keeps that relation one way:
every cancel reads (0, 0), and the tables read (0, 0) on more, the table
pointer being a Z-linear map of `Z[Z_Nphi]` onto a lattice of rank 2, its
kernel of rank `Nphi - 2` against the cancel's `Nphi / 2`; at `Nphi =
8192` only 1952 of the 8192 table pairs are distinct and two rows of amount
1 at the phases 0 and 4097 read (0, 0) where `|ev(f)|^2 = 4 sin^2(pi /
8192) = 5.9 x 10^-7`; at `Nphi = 64` no zero exists with at most three rows
of amounts up to 4 (a computation from the tables, not a run)."

## 6. What I did not prove

The two-slit threshold to better than one click at the peak (the
registered pixels' margins inside their rungs were not read, so 0.019 is
where exclusion is certain, not where it begins), and any bound tighter
than the margin-free 1 / 181 that does not rest on the tables' accident
at the window 32.

## 7. Links

- The theorem and its hypotheses: `paper/general_formula/main.tex` lines
  912 to 975; the sentence: line 1004 on `main` at 30c84db7, line 805 on
  `claude/paper-owner-review-five` at 65674bcb (line 794 at e6117ef6);
  the tables: lines 1457 to 1470.
- The referee's point and its folding: records 916 (b) and 921 of the
  log of 2026-09-20.
- The rounding rule: [DERIVATIONS_BEAM 6.2](../../DERIVATIONS_BEAM.md);
  the Gram matrix's eight diagonal values: 6.7 there.
- The tables: `src/event_universe/core/phase.py` (`phase_cosines`,
  `phase_sines`); [tables.txt](../amplitude-v1/tables.txt).
- The Malus numbers: [malus_map.py](../malus/malus_map.py) and
  [malus_map.out](../malus/malus_map.out); record 395.
- The classes of harmonics: [the Born note](../open_problems/born/NOTE.md)
  sections 2 and 4, [born_map.out](../open_problems/born/born_map.out).
- The arithmetic of this note: [bound_map.py](bound_map.py),
  [bound_map.out](bound_map.out); the zeros' search: [zeros_map.py](zeros_map.py),
  [zeros_map.out](zeros_map.out).
