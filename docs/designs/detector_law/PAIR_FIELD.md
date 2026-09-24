# The pair as a field: the one missing algebraic step, stated as a hypothesis under its own identity `pair-field-v1`, outside the law (the chief physicist, 2026-09-23; docs and one printed computation, no build, no run)

The model owner's word of 2026-09-23, about 20:40Z (Hebrew, in substance):
"So we lack only one algebraic step to stitch it completely, then a few
more experiments. Go for it; update the Boss; he is to close exactly which
experiments we must approve before the pins; when everything is approved
we close all the pins; he should have a clear plan."

This page is that step, written as the three tests require: a hypothesis
with its own identity, beside the law and not in it. Nothing of the law
changes; no pin of `SCHEDULE.md` moves; the engine gets no line from this
page until the Boss orders a build and Reviewer 3 has read it. Every number
is a COMPUTATION from the algebra before any run, printed by
`pair_field_pins.py` beside this page (its record `pair_field_pins.out`,
HOST 117 s), or a DECLARATION, a PREDICTION or a NATURE value, each named.

## 1. The step in plain words

The massive record kind (`MASSIVE_RECORD.md`) carries its pair (den, num)
as a declared constant: the pitch cos omega_0 = num / den is the same at
every Node. That is why rows 3, 11, 12, 13 and 14 of the schedule read NOT
PREDICTED: nothing in the law tells one block about another block's
content at a distance, so there is no clock in a crowd's field, no bending
at a crowd, no 1 / r between blocks, no far lamp under a growing wall.

The step: the pair itself is carried by a record. A third record kind,
massless (its own pair [1, 1], light's), obeys the same six-neighbour rule
as every kind. Every block's content M is its source at the block's cells,
by the static source verb the engine already has for a block. Every Node
reads this record as the deviation of its own pair: where the field is
deep the massive pitch is lower. Nothing else is added. The field spreads
at the pace c of the rule, so it is retarded by construction; its steady
shape around a source at rest is the lattice Green's function of the
six-neighbour Laplacian, which tends to 1 / (4 pi r) (section 4, (a)).

## 2. The objects (DECLARATION)

| The object | What it is | Where it lives |
| --- | --- | --- |
| The pair field | a record kind `pair` with the pair [1, 1]: a_next = S_6 / 3 - a_before + (the remainder's line of the rule), one scalar per Node | the world file's `kinds`, beside `light` and `massive` |
| Its source | every block's content M, added at the block's cells each interval by the existing static source verb (the block's declared strength kappa in place of the well's depth) | the block's declaration |
| Its reading by the massive kind | the Node's pitch: omega_0(r) = max(omega_0 - delta(r), 0), delta(r) = 4 pi kappa phi(r) with phi the field's steady value at the Node; in integers, the Node's pair (den, num) is replaced by (den, num + d) with d the field's integer at the Node, floored at num + d <= den (the pair cannot pass light: cos <= 1) | the massive rule's one division, the wall unchanged |
| Its reading by light | through the medium's declared coupling only (G g at declared cells, MASSIVE_RECORD.md section 6): the medium's pitch omega_0 shifts with the field, so its index n_m shifts; free light reads nothing | the index block's declaration |
| Its identity | `pair-field-v1`, off by default | the world file's `hypothesis` key |

The static source verb exists (the block's well); the third kind is one
more entry of `kinds`; the reading is the only new verb: the massive
division reads its num from the pair record at the Node. What the engine
lacks is section 8.

## 3. The three tests

- Generic: one primitive, the six-neighbour rule with a pair per kind; the
  source verb and the reading verb name no family and no kind by physical
  name (a kind reads the record named in its declaration). Held.
- Vector: the source is an add (no root, no float, the remainder's line
  kept). The reading is NOT an add in the rule: the massive step
  multiplies num by S_6, so with num + d read from the field record the
  step becomes (num + d) x S_6, a product of two records' integers at the
  Node, bilinear in the state. Verb (B) is the bilinear form with a
  DECLARED matrix (ALGEBRA.md 2.2), and no verb of the six multiplies two
  records. NOT HELD as the law's vector test stands: that product is
  exactly what the hypothesis asks for, and the honest reason this page
  is a hypothesis and not the law (Reviewer 3's read of 5ab165ce, 21:12Z).
- Local: the field at a Node is that Node's own record and its six
  neighbours; a block sources its own cells; a Node reads its own record.
  No global estimator, no self-field subtraction. Held.
- What the hypothesis changes, said plainly: under the law the pair is a
  declared constant of a kind and every step is linear in the state; under
  `pair-field-v1` the pair is read from a record at the Node and the step
  multiplies two records' integers. That is a change of what a pair IS and
  of the rule's linearity, so it is a hypothesis under its own identity and
  not the law, until the owner decides otherwise (Highlights 5.4 by his
  word only).
- The self-shift, named: a block reads its own field at its own cells
  (local, lawful, no subtraction), so every block's rest pitch is lowered
  by its own source, delta_self = 4 pi kappa (M phi(0) + the neighbours'
  values at its cells) with phi(0) = 0.2527: the rest pitch that the pins
  of MASSIVE_RECORD.md section 8 use is moved by kappa on the hypothesis's
  worlds only; every pin of such a world is computed with the self-shift
  in, and kappa is named beside it.

## 4. The four computations (COMPUTATION, `pair_field_pins.py`, 120^3 and 64^3, HOST 117 s)

(a) THE FIELD'S SHAPE. The lattice Green's function on a periodic 120^3
board (FFT, the background subtracted), gauged to the infinite lattice by
Watson's constant phi(0) = 0.252731 (the identity 6 phi(0) - 6 phi(1) = 1
returns 1.00000). r phi(r) along an axis: 0.0861 (r = 1), 0.0812 (4),
0.0802 (6), 0.0800 (8), 0.0799 (12), 0.0801 (16); along a diagonal at
|r| = 6.9 to 20.8: 0.0793, 0.0798, 0.0804. The limit 1 / (4 pi) = 0.0796.
Isotropy under the 48 within 0.3 percent from r = 6; the periodic images'
error O(r^2 / n^3) is 0.5 percent at r = 12 and grows beyond. The field IS
1 / r beyond a few Links: the law's rule, sourced at a point, gives
Newton's shape without a new constant.

(b) THE CLOCK IN THE FIELD (row 12's form). The pitch's shift delta(r) is
proportional to phi(r); the ratio of the shifts at r and 2 r: 2.114 (r =
2), 2.030 (4), 1.997 (8), 1.972 (12). A 1 / r field gives 2.000. Row 12's
form (a clock at two distances from a crowd reads the crowd's 1 / r) is
reached at the form level; its NUMBER needs the field's strength kappa
tied to a declared block, and the massive kind's own gamma in the field
(section 6), before it is a pin.

(c) THE BENDING AGAINST THE CLOCK (row 13). Light reads the field only
through a medium (section 2). The medium's index n_m^2 = 1 + G g /
(omega_0^2 - omega^2) (MASSIVE_RECORD.md section 6) shifts when its
omega_0 shifts with the field; in the long-wave limit the bending against
the clock's shift is 1 + gamma_eff = (n_m^2 - 1) / n_m: 0.833 (n_m = 1.5),
1.500 (2), 2.000 (n_m = 1 + sqrt 2 = 2.414), 2.667 (3). Nature's 2
(Shapiro, VLBI; row 13) is reached at ONE declared input, the medium's
coupling, n_m = 1 + sqrt 2. Honesty: one row fixes that input; row 13
then predicts nothing by itself. It is the OTHER rows that predict: with
that one input fixed, rows 3, 11 and 12 have no free number left (section
6). Free light reads no field under this hypothesis; if nature's bending
of light in vacuum must come out with no medium, `pair-field-v1` is
falsified on that row (section 7).

(d) THE 1 / r WELL'S LADDER (row 6). A point source of strength kappa
gives the Bohr radius a_B = c^2 cot omega_0 / kappa Links; the massive
kind's reduced Compton length is lambda_C = c / omega_0 = 3.87 Links at mu
= 0.15, so alpha_eff = lambda_C / a_B. On 120^3 at a_B = 8 (alpha_eff =
0.483, the pitch floored at 0 within two Links of the source; eigsh 107 s)
the six lowest levels E_n = omega_n - omega_0 are -0.01300, -0.00557,
-0.00420, -0.00302, -0.00172, -0.00093; the continuum's E_1 = -kappa /
(2 a_B) = -0.01731 (the GameBoard's ground level at 0.75 of it: the strong
coupling and the two floored Links). NOT A LADDER YET: the periodic
images floor the well at delta(60) = 0.0046 below omega_0, so every level
above -0.0046 sits at the box's floor, the four levels of hydrogen's n = 2
rung are not degenerate (spread 1.06) and E_1 / E_2 = 3.58 is a
box-limited number, not read against 4. The weak limit (alpha_eff -> 0) is
the Schroedinger ladder 1 / n^2, a theorem; what the board must show is
its approach to that theorem at a declared alpha_eff. HOST: a 256^3 board
with closed faces and a_B = 8 (about one hour) before any ladder number is
read; the schedule's scale condition for hydrogen itself (a_B = 527 Links
at mu = 0.15, alpha_eff = 1 / 137) stands as written.

(e) TWO AND FOUR SOURCES AT CONTACT (rows 7a, 7b). On 64^3 at a_B = 8 per
source and the contact d = 4: one source binds -0.01483, two (on an axis)
-0.03383, four (the origin and its three axes) -0.06332; per source
against one, two 0.0190, four 0.0485, the ratio four / two = 2.55 (nature's
alpha / deuteron per nucleon 6.4). The same floor applies (the images'
delta at the half-box 32 is 0.0087 per source, of E_1's size), so 2.55 is
box-limited and NOT a pin; the form is what this shows: under the
hypothesis a contact of sources binds, and the alpha-to-deuteron ratio is
a PREDICTION of the declared contact once the board is large enough. What
a nucleus IS under the hypothesis (a block of declared cells, or several
at contact) is a declaration this page does not make.

## 5. The rows reached now, and after the second step

| Row | Under the law today (`SCHEDULE.md`) | Under `pair-field-v1` | Kind |
| --- | --- | --- | --- |
| 12, the clock at two distances | NOT PREDICTED | the field's 1 / r at the form level, (b); the number after the strength is tied to a block | (K) form; the number a PREDICTION |
| 13, the bending 1 + gamma_PPN | NOT PREDICTED | (n_m^2 - 1) / n_m, one declared input; nature's 2 at n_m = 1 + sqrt 2, (c) | the one row that FIXES the input |
| 6, the atom's ladder | NOT COMPARED (the scale) | the 1 / r well of the field, (d); box-limited tonight | (P) after the 256^3 board |
| 7a, 7b, the bindings | NOT PREDICTED | a contact of sources binds, (e); box-limited tonight | (P) after the board and a declared nucleus |
| 3, 11a to 11c, the far lamp | NOT PREDICTED | need the crowd's field on light's clock along the ray: the field is here; the ray's reading needs the SECOND STEP | after the second step |
| 14, the 1 / r period ratio | NOT PREDICTED | needs the field's PUSH on a block: the second step | after the second step |

THE SECOND STEP (open, not derived here): the field's gradient at a
block's cells as the block's push, in the same verb as the wall's push
(MASSIVE_RECORD.md section 5, lines (a) to (e)). Its form follows from J
(section 7 there) by the same two-point Lagrangian with the pair's num
read from the field; the derivation is the algebra chapter's next part,
not this page's. Until it is written, rows 3, 11 and 14 stay NOT
PREDICTED in the schedule and this page claims nothing on them.

## 6. Honesty: what is fixed by declaration and what is predicted

- The medium's coupling G g is a DECLARATION; through it 1 + gamma_eff.
  One nature row fixes it (13); the hypothesis is tested on the rows that
  share that input and have none of their own.
- The field's strength kappa per block is a DECLARATION (the block's
  content M times one declared constant, the same for every block). One
  row fixes it (12 at one distance); the same row at the second distance,
  and rows 6, 7a, 7b, are then PREDICTIONS.
- The clock in the field: the massive kind's own gamma at its own exact
  cone c_eff (MASSIVE_RECORD.md section 8) stands; in the field the pitch
  omega_0(r) is lower, so c_eff(r) is lower too; the moving clock in a
  field is the one formula with omega_0(r): a PREDICTION with no free
  number once kappa is fixed.
- The field's own energy is not in the invariant J; a static field adds
  a constant per configuration; a moving source's radiation of the field
  is not derived. Said, not hidden.
- The numbers of (d) and (e) are box-limited (the images' floor); they
  show the form and are not pins. The numbers of (a), (b), (c) are clean
  within the stated 0.3 to 0.5 percent.
- The strong coupling: at a_B = 8 the two Links nearest the source are
  floored at pitch 0 (the pair at light's); the hydrogen regime is a_B
  much larger than lambda_C, where nothing is floored.

## 7. The falsifiers, said before any run

- (a) if the field read on a board of the engine is not 1 / r beyond a
  few Links (the ratio of (b) outside 2.00 by more than the images'
  error), the third kind is not the field claimed: the hypothesis fails.
- (c) if row 13's 2 must come out with free light and no medium, the
  hypothesis fails on that row as written (free light reads no field).
- (d) if, on the 256^3 board at a declared alpha_eff, the ladder does not
  approach 1 / n^2 as alpha_eff is lowered, the reading verb is wrong.
- rows 12, 6, 7: with kappa fixed by one reading, a second reading off
  its prediction by more than the reader's grain falsifies.

## 8. What the engine needs (three lines, for the Boss's plan; no build ordered)

1. A third entry of `kinds` in the world file, the pair [1, 1] under the
   name declared there (`pair`), the same rule (nothing new in the rule).
2. The block's static source verb writing its content M times the declared
   kappa into that kind at its cells (the verb exists for the well).
3. The reading verb: the massive division at a Node reads num + d, d the
   pair kind's integer at the Node, floored at den; light's medium reads
   its omega_0 from the same; under the key `hypothesis: pair-field-v1`
   only, off by default. The world (a) of section 4 is the first
   exploratory run (a block at rest on 64^3, the field read on an axis
   and a diagonal, GAMEBOARD, against (a)).

## 9. Reproducibility

`PYTHONPATH=src python docs/designs/detector_law/pair_field_pins.py`, the
record `pair_field_pins.out` beside it; numpy and scipy (eigsh on a
LinearOperator), no engine import, HOST 117 s on this container.
