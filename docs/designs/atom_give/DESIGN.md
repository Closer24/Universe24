# atom-give-v1: the give of content at the return, read off the body's action rows against their value at the last return, under its own identity, off by default

The Atom Give Designer, 2026-09-22, on the model owner's decision in the
Atom Algebraist's session ("Go with what you proposed. Is it valid only
for the electron?", record 881 of [docs/LOG_2026-09-20.md](../../LOG_2026-09-20.md),
on the Boss's branch of PR #831; the decision line for Highlights 5.4 is
the Boss's). A design only: no engine line, no world file, no run, no pin
moved. Base commit `origin/main` 305ef9266dee0dac5a3ba5ad03a85ec0a87aa53f
(PR #829 merged); the algebra it corrects is
[ALGEBRA.md](../atom_algebra/ALGEBRA.md) at 643b7ae7d4aeac2062518146aeb6e8b6f2998148
(PR #823, merged to `main` at 67cee0930fffbdc48a5d84b32d2ae180f10933a5; sections 1, 3 (c), 6 and 7), read with records 826 (I), 844,
858, 863, 864, 874, 876 and 881. The rule sits OUTSIDE the law under its
own identity, `atom-give-v1`, until it passes the gate (the three tests,
the physics-rule reviewer, the owner's go on the build); nothing here is
written into the law. Every number below is a HOST computation from the
law's integers as the atoms series declares them (GAMEBOARD by formula
until a detector clicks) or an EXPECTED detector reading derived before
any run; Bohr's, Balmer's and de Broglie's forms appear only on the
comparison side (record 817).

**The verdict in one line.** ADMISSIBLE under the three tests (generic,
vector, local: section 3), the flaw of ALGEBRA.md section 6 fixed (a
closed loop gives exactly nothing, section 1 (d)), bit-exact with the key
off; and the limit's algebra says, before any run, that the give of
content does not carry an open loop to a closing radius: under charge
per unit of content and inertia per unit of content the loop's closure
sum is invariant to first order in the content given, so the rule as
ordered is a slow evaporation of an open loop, not its return to a
closure (section 4 (b)). Both facts go to the owner; the run of section
5 reads the second on the lattice.

**The six lines (the report's head; every number DETECTOR or GAMEBOARD).**

1. *The information.* A body whose family declares a phase circle and
   whose record turns by momentum carries, beside its three action rows
   (one per axis, each with its remainder below h), three more
   accumulators, the action gained on each axis since the last return,
   kept modulo N h. At a return (the body's own momentum crossing the
   declared axis in the declared sense, once per loop, read off its own
   record) the body reads r, the remainder of the sum of the three
   modulo N h, gives one row per declared direction of content
   `h_q x floor(r n_g / (N h d_g))` from its own content with the row's
   label as its recoil, and zeroes the three. Nothing kept at a Node;
   the row crosses one Link per interval and clicks at a detector with
   its content and phase (DETECTOR); the tick is lost (GAMEBOARD).
2. *The generic solution.* One primitive for every family alike: two
   accumulators per axis on the record (the counts table's rows), one
   threshold on the momentum for the return, one Euclidean division
   with the remainder kept for r, one declared pair and one declared
   quantum for the content, and the law's existing paid release for the
   row; no family name, no kind; a family without a phase circle or
   without `phase_by_momentum` gives nothing, a value and not a branch.
3. *Why it works, and what refutes it.* A closed loop gains exactly
   `j N h` on the sum over a return, so `r = 0` and it gives nothing and
   stays, for every start (section 1 (d)); an open loop with the
   fraction f of a circle beyond the whole gives `floor(16 f)` quanta
   per row at the declared pair [16, 1]. The reading that shows it: the
   given rows' clicks at the detectors (the six faces today; a passive
   detector at every Node, record 721, when it lands) with their content
   between two returns, 0 per return at r = 12 and 2 per row at r = 8
   (EXPECTED DETECTOR, from the formula's f = 0.0010 and 0.1416). The
   reading that refutes the form: a give at r = 12 while the electron's
   rows' phase per return is whole within 1/16 of a circle. The reading
   that refutes the limit's algebra of section 4 (b): an open loop whose
   fraction f falls into the band 1/16 before the body has given a tenth
   of its content.
4. *Why do this at all.* It is the one stability rule of the atom the
   owner chose (record 881), and its design says, from the six verbs and
   the limit, what it does and does not do before an engine line is
   written: a closed loop is a fixed point of it, and the give of
   content moves the closure sum by `2 (j + f) G^2 / M^2` circles per
   return, upward, second order (section 4 (b)); not doing it leaves the
   owner's picture (the loop's frequency entering the circumference a
   whole number of times, record 874 (b)) without the arithmetic that
   decides whether a give of content can enforce it.
5. *The Highlights.* Kept: the click as the one operation (P6), the
   label as the one momentum (note 18), charge per unit of content (note
   28), the three tests, only a detector's reading a measurement (record
   281), reality is the detectors (record 721), the comparison side only
   (record 817), the closure generic and in the law (record 864). One
   line asked, the Boss's: the decision of record 881 with this design
   as its file, the identity off by default.
6. *The implementation.* When the owner says go: `events/world.py` (the
   world key `give_at_return`, the body key `give`, the family key
   `frequency_by_content`, refused without the world key),
   `events/measured.py` (three `Count("give", ...)` rows and one sign on
   the record), `events/engine.py` (the return's threshold, the division,
   the release through the existing paid-birth path), `nature_beam.py`
   (the row's pair from its content under the family key), one test
   module per rule on a minimal GameBoard, the gate set byte-identical
   with the key absent, two worlds of the atoms series (r = 12 and its
   named variant at r = 8). Host estimate: the build and its tests about
   two hours, each world about 60 s and a few hundred megabytes (series
   H's cost), the reviews beside. Dangerous: nothing with the key off
   (every world reads as it did, byte for byte); with it on, a give at
   every return of a closed loop, which section 1 (d) forbids and the r
   = 12 world guards.

**Notation** (skills/workflow.md, "Notation"). Q = 64 the label's scale;
S the width of the push (45120 in the atoms series); M the body's
content (the electron's 1836, in units); N = 64 the steps of the phase
circle; h the world's `action` (the atoms series under form B: 5 536 242
544); `h_q` a family's quantum (the content of one unit per phase step
of its emitter's turn; 1 on the `light` family); **p** the momentum
vector of the body in label units, `p_a` its component on the axis a;
**u**_d the unit vector of the direction d at the scale Q; `A_a` the
action row of the axis a (the exact sum of `abs(p_a) N` over the Links
counted on that axis since the body's birth, record 155); `A_ret_a` its
value at the last return; `D_a = A_a - A_ret_a` the action gained on the
axis since the last return; r the remainder of `D_x + D_y + D_z` modulo
N h; f = r / (N h) the fraction of a circle beyond the whole circles (0
<= f < 1); j the whole circles the phase turns per return; `[n_g, d_g]`
the give's declared pair; g the quanta given per row; G the content
given per return over all the rows; c the content per unit of a row; w
a row's amount; T the count between two returns (the period); v the
body's pace in Links per interval; a the semi-major axis of a loop in
the limit; `kappa` the push's constant and `m_i = Q S M` the inertial
constant of the drive's limit (ALGEBRA.md section 2 (a)); `floor(x)`
the whole part; `sqrt(x)` the limit's root, never the GameBoard's;
`theta` (the angle between a given row's direction and the momentum,
the limit's); pi the circle's ratio; lambda (a scale factor of the
content, the limit's).

The kinds of a number (record 189): kind 1 the grain (N, Q, the fan, K,
the roundings at load); kind 2 the family table and the width (h, `h_q`,
S, the charges, the pairs); kind 3 the state and the apparatus (the
positions, the momenta, the detectors, the ticks). Each pinned number
names its kind and DETECTOR or GAMEBOARD.

## 1. The rule, in the law's integers

**(a) The two accumulators per axis.** The engine keeps one action row
per axis for a body under `phase_by_momentum` with the world's `action`
h: `Count("action", "momentum", axis, axis, N, h)` (`measured.py:439`),
advanced by `abs(p_a) N` at every Link the step rule counts on the axis
a (`engine.py:892-898` under form B, `:911-921` on the per-axis drive),
the whole part over h delivered to the phase at a Link crossed, the
remainder below h kept in the row's accumulator (`core.integer.by_drive`).
So `A_a` exists on the record as its remainder and its delivered whole
parts, exactly (record 155's accumulator form). Under `atom-give-v1` the
record carries a SECOND row per axis,

    Count("give", "momentum", axis, axis, N, N h)        (three rows, the same rate abs(p_a) N at the same Links, the denominator N h, no cap, never age-walled),

whose accumulator holds `D_a mod (N h)`, the action gained on the axis
since the last return modulo N h (its whole parts, the circles per axis
since the last return, are a GameBoard diagnostic and act on nothing).
The order's form `A_ret_a` (the action at the last return, set at each
return) and this row are one arithmetic: `D_a = A_a - A_ret_a`, and the
row's accumulator is `D_a mod (N h)` because it is zeroed at the return
(section 1 (c)) and gains exactly what the action row gains between
returns. Two integers per axis on the record, nothing else (section 7).

**(b) The return.** A return is a fact of the body's own record: the
body's momentum on the declared axis crossing zero in the declared
sense, `sign(p_a)` passing from the declared sign to its opposite
between one interval and the next (the record's one extra integer: the
sign of `p_a` at the last interval, 0 at birth). On any loop that
circles a centre once per turn the declared component of **p** changes
sign twice per turn, once in each sense, so the declared sense fires
exactly once per loop; on a straight flight it never fires, and a free
body gives nothing (record 874 (b): "an electron would also know to go
straight"). The push translates `p_a` by the crowd's flow every interval
(the bilinear form, W2) and the threshold 0 is read on the translated
accumulator: the first verb, a translation with a threshold, the drive's
own shape. The declaration: `give.return = [axis, sign]`, the axis index
and the sign `p_a` crosses TO (section 2). The first return after the
birth reads the action since the birth; a world that wants the first
return to read one whole loop starts the body on the return's axis
crossing with `p_a = 0` there (the atoms series does: the electron
starts on the +x axis with **p** along y, section 5).

Why the return is not the returned row's click (ALGEBRA.md section 6 and
record 863 named the click of the body's own row, returned through the
proton under `rerelease`): that row's round trip is 2 r intervals (24 at
r = 12, one Link per interval each way), not the loop's period T (1490
at r = 12 under form B, the atoms pins): the give would then zero the
accumulators about sixty times per loop and read the action of one
sixtieth of a loop, `f = 4 x 24 / 1490 = 0.064` per window at r = 12,
one quantum per window on the CLOSED loop at the pair [16, 1]; the
returned row reads the pulse-and-return of a clock (ALGEBRA.md section 1
(b)), not the atom's return. The re-emitter is therefore NOT among what
this rule needs (a deviation from record 881's list, stated here for the
reviewer). The one reading set is untouched: the body never reads its
own rows; the return reads the body's own momentum, which is its own
record and not a row.

**(c) The give.** At a return, in this order and in one interval:

    r = (D_x + D_y + D_z) mod (N h)                (the sum of the three give rows' accumulators, each below N h, so the sum is below 3 N h and one Euclidean division gives r; the quotient is discarded);
    g = floor(r n_g / (N h d_g))                    (one Euclidean division on bounded integers: r n_g < N h d_g x (n_g / d_g), so g < n_g / d_g);
    if g > 0: for each declared direction d of the body, one row is born at the body's Node
        of the declared paid family F, amount w = 1, content per unit c = h_q g, age 0,
        the body's phase and number, no record, label c u_d = h_q g u_d;
    the body's content M := M - (the rows' content), its momentum p := p - (the sum of the rows' labels)   (the paid release's own recoil, born_recoil);
    D_x := D_y := D_z := 0                          (the three give rows' accumulators zeroed: A_ret_a := A_a on each axis).

The row's birth is the law's paid release as `engine._give` makes it
under `binding-v1` (BEAM_LAW note 40; "one row, age 0, the body's phase
and number, no record, at the body's Node on the heading, the body takes
the recoil, minus the row's label, Q x content per unit along the
heading, the one label of the law"), with the content per unit `h_q g`
in place of `held // h` units of `h_q`: a paid birth's content per unit
is `c = h_q s` with s the emitter's turn (DERIVATIONS_BEAM 6.4), and the
give is that birth with s read off the return's remainder instead of the
clock's turn. The row then has the law's fates: it clicks at a detector
with its content and phase, or a body on its line takes it under the
tables' `measure` (the label moved onto that body's momentum, the one
click of the law, `nature_beam.py:4986-4989`, a paid row's). The
directions are the body's own `directions` (the ones it releases on):
no new list; a symmetric list (the electron's four in-plane headings)
sums the recoil to zero exactly and the give is a pure loss of content.

**(d) The flaw of ALGEBRA.md section 6, fixed, with the arithmetic.**
Section 6 as written gives `w c = h_q x floor(sum_a (A_a - A_ret_a) /
(N h))`, the WHOLE part of the difference over N h. Over one return of a
closed loop with j circles per return the difference is exactly `j N h`
(section 1 (a) of ALGEBRA.md: `Delta A_a = 0 mod h` on each axis and the
quotients sum to `j N`), so the whole part is j and that form gives `h_q
j` at EVERY return of a closed loop: the closed loop would give at every
loop and decay, which is not a stability rule (records 874, 876, 881).
The corrected form reads the NON-WHOLE part, r:

    a closed loop:   D_x + D_y + D_z = j N h,   r = j N h mod N h = 0,   g = 0:   nothing given, nothing zeroed but zeros, the loop stays, for every starting state of the accumulators (the give rows start at 0 at the birth and at every return, so D_a is the gain itself and no start enters);
    an open loop:    D_x + D_y + D_z = (j + f) N h with 0 < f < 1,   r = f N h,   g = floor(f n_g / d_g):   a give unless f < d_g / n_g (the band: a loop closed to within one part in n_g / d_g of a circle gives nothing, the declared grain of the rule).

The identity checked in integers: the sum of the three per-axis
remainders modulo N h equals the total's remainder, since each `D_a mod
(N h)` differs from `D_a` by a multiple of N h; and on a closed loop the
phase's turn over the return is exactly `j N` steps for every start of
the action rows' remainders (the floor's telescoping at a multiple of
h), which is what makes r = 0 and the closure one fact. Where a return's
sum is a multiple of N h while one axis's gain is off a multiple of h
(the reviewer's per-axis line, record 863 (1)): r = 0 and the rule gives
nothing, though the phase's turn over that return may be one step off
`j N` either way depending on the start; the rule reads the sum, as the
owner's decision names it, and the per-axis residues stay a GameBoard
diagnostic of the give rows. A per-axis form of the give (three
remainders each below h read separately) is a variant not chosen.

**(e) Bit-exactness with the key off.** Without the world key no give
row exists on any record, no threshold is read and no row is born: the
counts table is as it is, and every registered world replays byte for
byte (the gate set, `examples/events/gate_set.json`, the assertion of
every key admitted since 2026-09-20).

## 2. The two declarations the world file carries, and what a family needs

| The declaration | Where | Kind | What it says | Default |
| --- | --- | --- | --- | --- |
| `give_at_return: true` | the world | the identity `atom-give-v1` (record 881), admitted per world | the body key `give` and the family key `frequency_by_content` are accepted; the record carries the identity under `hypotheses` | absent: refused if either key appears |
| `give: {"family": F, "pair": [n_g, d_g], "return": [axis, sign]}` | a measured event (a body) | kind 2 (the pair, the family) and kind 3 (the axis and sign of the apparatus's reading) | F a paid family of the world (`quantum` > 0: a free row moves no label and carries no content, ALGEBRA.md section 3 (a)); `[n_g, d_g]` positive integers, `n_g / d_g` the quanta given per row per whole circle of excess, `d_g / n_g` the band; `[axis, sign]` the return: the axis index 0, 1 or 2 and the sign -1 or +1 that `p_axis` crosses TO | absent: the body gives nothing |
| `frequency_by_content: true` | a paid family | the second declaration of record 826 (4) and 881 | every row of the family is born with its phase-per-age pair `[c, h_q]` steps per interval (c its content per unit): its frequency follows its content in flight, `f = c / (h_q N)` circles per interval, Planck's constant of the release `h_q N` (DERIVATIONS_BEAM 6.4: `E = h_q s = (h_q N) f`); a re-emission keeps the content and so the pair | false: the family's declared pair, as every family today |

What each family needs, and what it does not:

- The body's family declares a phase circle (`phase: true`) and the
  body declares `phase_by_momentum` under the world's `action` h (the
  three action rows exist; without them there is no closure to read):
  the electron `e` of the register does; the proton `p` and the neutron
  `n` declare `phase: false` and give nothing, a value and not a branch
  (record 881 (a)).
- A paid family F for the given rows (`quantum` > 0): the register's
  `light` (quantum 1) serves; the body pays the rows' content from its
  own content M as the click adds any paid row's content to M (ALGEBRA.md
  section 3 (a), `M' = M + w c` for a paid row of any family).
- The body's `directions`: the give's rows go on them; a body with the
  six headings by default gives six rows.
- NOT needed: `rerelease` at a re-emitter (section 1 (b)); a `hold`; any
  detector (the rule acts without one; the READING needs detectors:
  section 4 (c)); any word of the body's table (the give is a release,
  not a click).
- The engine branches on no name: `phase`, `phase_by_momentum`,
  `quantum` and the keys above are values of the tables.

The pair `[c, h_q]` is chosen over the wavelength's dictionary `[c Q N,
h]` (the row's own label over the world's action, ALGEBRA.md section 6's
"its content over `h_q N`" being the release's) because the give IS a
release and the two agree under the calibration `h = h_q N` of 6.4; in
the atoms series `h = 5 536 242 544` is not `h_q N = 64` (the
calibration is not made there), and the wavelength's form would turn a
row of content 2 by `2 x 64 x 64 / 5 536 242 544` steps per interval,
nothing readable in a 53^3 world. The choice is a declaration, kind 2;
the other is named and not chosen.

## 3. The three tests of every rule (skills/workflow.md, record 202)

| The test | The rule's answer | Verdict |
| --- | --- | --- |
| Generic | one primitive: two accumulators per axis (the counts table's rows), one threshold on a momentum component, one Euclidean division with the remainder kept, one declared pair and one declared quantum, the law's paid release; the same for the electron, a muon, a planet; a family without a phase circle or `phase_by_momentum` gives nothing as a value; the engine branches on no name | PASS |
| Vector | verb 1 (the translation of the give rows by `abs(p_a) N` at the counted Links, the momentum's threshold at 0 for the return), verb 6 (the Euclidean division: `r` modulo N h, `g = floor(r n_g / (N h d_g))`), the paid release's translation of the content and momentum by the rows' labels (the recoil, the law's); the rate `abs(p_a) N` linear in the state; no root, no float, no rounding beyond the declared pair | PASS |
| Local | the body's own record (the action rows, the give rows, the momentum, the sign) and nothing else; the rows born cross one Link per interval; nothing kept at a Node; fixed work and storage for fixed K (section 7); every host reading labelled | PASS |

All three pass; the rule is admissible to the gate. It enters the law
only on the reviewer's verdict and the owner's go, and stays outside it
under its identity meanwhile.

## 4. Why it works, and what refutes it

**(a) A closed loop gives nothing and stays.** Exact, section 1 (d):
`r = 0` at every return of a loop whose action gain is `j N h`, for every
start; nothing is born, the content and the momentum are untouched, the
loop is a fixed point of the rule. The closed loop's ladder of ALGEBRA.md
section 2, `a_j / a_i = (j / i)^2` in the shell mean with `T_j / T_i =
(j / i)^3`, is untouched by the rule: the rule acts on no closed loop.

**(b) An open loop gives, and which way it moves, with the sign.** Let
the open loop have `j + f` circles per return. At the return it gives G
= `(the number of directions) x h_q g` of content with the recoil `-
sum_d h_q g u_d` (zero on a symmetric list). Where does the next return's
closure sum stand? In the inverse-square limit of ALGEBRA.md section 2
(a), with both the push and the drive's wall proportional to the body's
content (W2; note 28: `kappa = M k_0`, `m_i = Q S M`), the closure sum of
a loop of semi-major axis a is `J = 2 pi sqrt(kappa m_i a) = 2 pi M
sqrt(k_0 Q S a)` and a circle at radius r has `p^2 = M^2 k_0 Q S / r`.
Scale the content by lambda at fixed **p** and fixed position (a pure
give of content, the recoil aside): the loop's constant is `E(lambda) =
T_k / lambda - 2 T_k lambda` with `T_k = p^2 / (2 m_i)` the circle's
kinetic term (`E(1) = -T_k`), the new semi-major axis is `a' = lambda M
k_0 / (2 abs(E)) = r lambda^2 / (2 lambda^2 - 1)`, and the new closure
sum is

    J' = J x lambda^2 / sqrt(2 lambda^2 - 1) = J x (1 + 2 epsilon^2 + O(epsilon^3))   at lambda = 1 - epsilon, epsilon = G / M:

the first-order term is ZERO (the derivative of `lambda^2 (2 lambda^2 -
1)^(-1/2)` at 1 is `2 - 2 = 0`; checked numerically: `epsilon = 10^-2`
gives `J' / J - 1 = 2.06 x 10^-4`). So a give of content G leaves the
closure sum unchanged at first order and raises it at second order by
`2 G^2 / M^2`: the fraction moves by

    Delta f = + 2 (j + f) G^2 / M^2   per return,   UPWARD, toward the closure j + 1 and away from the closure j below,

while the loop widens at first order, `a' = a (1 + 2 G / M)`, and the
whole ladder of closing radii moves outward with it, `a_j ~ 1 / M^2`
(ALGEBRA.md section 2 (b) with `kappa m_i ~ M^2`). The recoil, when the
directions do not cancel, adds the first-order term `-(j + f) x (G /
(S M v)) cos theta` (a row released along the motion lowers J, against
it raises it), with the coefficient `1 / (S v)`: the label per unit of
content of a row is Q, the body's momentum per unit of content is `Q S
v` (the drive's `p = Q S M v`), so the recoil is `1 / (S v)` of the
content's effect on the momentum and negligible where `S v >> 1` (2369
at r = 12, 2764 at r = 8 in the atoms series, GAMEBOARD by formula). The
reason in one sentence: with charge and inertia both per unit of
content, content is a scale of Kepler's problem and not an energy, and a
scale cannot select a radius.

At the atoms series' numbers (section 5): the open loop at r = 8 has `j
+ f = 3.1416` (GAMEBOARD by formula), gives `G = 4 x 2 = 8` units per
return, and moves by `Delta f = 2 x 3.14 x 64 / 1836^2 = 1.2 x 10^-4`
per return; to reach the band below the closure j + 1 = 4 (f = 0.9375)
it would need `1 / M_end = 1 / M_0 + 0.796 / (2 j G)`, that is 222
returns and a content of 61 out of 1836, by which time its semi-major
axis is `8 x (1836 / 61)^2 = 7250` Links: it leaves the 53^3 GameBoard
after about 102 returns (a = 26 at M = 1018). So on the register's
integers the give of content does not close an open loop; it evaporates
it, slowly, outward. This is the algebra's verdict on the mechanism,
stated before any run under the owner's rule that whatever can be
computed algebraically is computed algebraically (record 762); the run
of section 5 reads whether the lattice (the fan's grain, the two-valued
gaps) does what the limit does.

What would make the give first order, named and NOT chosen: a given row
carrying the body's momentum per unit of content, the label `G p / M`
in place of `G Q` (then `p' = p (1 - G / M)`, the same loop at the same
a with `J' = J (1 - G / M)`, downward toward the closure j by `(j + f) G
/ M` per return, 0.0137 per return at r = 8 with G = 8, the band reached
in 11 returns at a cost of 88 units), which is a change of the label
rule (note 18: the one label of the law is Q per unit of content) and
therefore a different rule, the owner's to name if he wants it.

**(c) The reach theorem bounds every give.** Each given row is one
impulse of the law's label; by ALGEBRA.md section 3 (c) one impulse
from a loop of semi-major axis a reaches only loops with `a' >= a / 2`,
and the content's loss only widens (section 3 (d), `dE / dM < 0`): no
give, at any pair, takes a body from the loop j to a loop with `2 i^2 <
j^2`, so no give is Balmer's or Lyman's line either; the rule cannot be
refuted by such a line's absence and does not claim one.

**(d) The refutations and the readings that decide.** The reading is a
click at a detector Node (records 721, 839), the detector's own count
stamped (record 754), the host's tick a labelled diagnostic:

1. The given rows' clicks with their content between two returns: the
   six faces of the atoms world are `wave` detectors of what leaves
   (series H's, the register's escaped lines carrying the content and
   the phase), and a passive detector at every Node (record 721) reads
   the same rows one Link from the body when it lands; DETECTOR. On the
   closed loop (r = 12) the expected number of given rows per return is
   0; on the open loop (r = 8) 4 rows of content 2 each per return.
2. The given rows' frequency: two faces on one line at different
   distances from the body read one row each with the phase at arrival
   and the detector's own count; `(phase_2 - phase_1) / (count_2 -
   count_1)` in steps per interval is the row's frequency, 2 at r = 8
   under `[c, h_q]`, a ratio of two detector differences; DETECTOR.
3. The closing radii's ladder `(j / i)^2` in the shell mean: read as the
   square of two circle counts (ALGEBRA.md section 2 (c) reading 1) on
   two closed loops, unchanged by the rule.
4. The electron's own rows' phase per return (reading 1 of ALGEBRA.md
   section 2 (c)): the fraction f on the lattice, the deciding reading
   at r = 12 still not taken (records 858, 863).

What refutes the form: a give at r = 12 (any face click of a `light` row
between two returns) while reading 4 is whole within 1/16 of a circle.
What refutes the atoms pin instead: a give at r = 12 with reading 4 off
by more than 1/16 (then r = 12 is not closed on the lattice, ALGEBRA.md
section 2 (d)'s fan table, and the pin `j = 4.001` falls, not the form).
What refutes section 4 (b)'s algebra: an open loop at r = 8 whose
fraction f (reading 4) falls into the band within the run's returns, or
whose gives stop while the body has given less than a tenth of its
content. What confirms it: 9 returns at r = 8 each giving 4 rows of
content 2, f constant to `10^-3`, the body's content 1836 to 1764.

## 5. The pins, declared before any run (GAMEBOARD by formula until a detector clicks)

The world: the atoms series' `hydrogen_r12` as written
([atoms/PINS.md](../atoms/PINS.md): the proton of series H fixed at the
centre of 53^3, the electron `e` of content 1836 at (38, 26, 26) with
**p** = (0, 293 783 192, 0), `phase_by_momentum` under `action` 5 536
242 544, `release` [1, 18360], `width` 45120, `suspension` 0, K 2^30, N
64, the four in-plane headings, `at_proton` a `wave` detector, `ticks`
7500), with the declarations of section 2 added and nothing else; and
its NAMED VARIANT `hydrogen_r8`, the same generator at RADIUS 8, whose
momentum is `h / 16 = 346 015 159` exactly (the generator's own rule `h
= 16 p(8)`), the electron at (34, 26, 26) with **p** = (0, 346 015 159,
0). Neither world file is written here; the build writes them.

The declarations for the read: `give_at_return: true`; on the electron
`give: {"family": "light", "pair": [16, 1], "return": [0, -1]}` (the x
axis, `p_x` crossing from + to -, the +x axis crossing of a loop that
turns from +x toward +y: the start's own crossing, so the first return
reads one whole loop); on `light` `frequency_by_content: true`; `light`
in the world's families (quantum 1, kind 2). The pair [16, 1] gives one
quantum per sixteenth of a circle of excess and a band of 1/16, chosen
so that the give is a whole number readable on a face (2 per row at r =
8, 0 at r = 12), below N / 2 in steps per interval (the phase unwraps on
one branch), and so that the pinned closure `j = 4.001` sits sixty times
inside the band.

| The pin | `hydrogen_r12` (closed) | `hydrogen_r8` (open) | Kind | How it is read |
| --- | --- | --- | --- | --- |
| the circles per return, `j + f = 2 pi p r / h` | 4.0010, f = 0.0010 | 3.1416, f = 0.1416 (the fraction pi - 3, the generator's `h = 16 p(8)`) | GAMEBOARD by formula (ALGEBRA.md 2 (c) reading 1 is the DETECTOR form) | the electron's rows' phase increments unwrapped over one return, on the faces |
| the period T | 1490 (the atoms pins, form B) | 811 (`1490 x (8 / 12)^(3 / 2)`, Kepler's ratio of ALGEBRA.md section 2 (b), used as a formula of the limit and compared, not put in) | GAMEBOARD by formula | the count between two `at_proton` clicks from the same axis |
| the returns in 7500 ticks | 5 (at 1490, 2980, 4470, 5960, 7450) | 9 (the first at 811) | GAMEBOARD by formula | the count of give events; the faces' `light` clicks grouped per return |
| the give per return | 0 on every return (`floor(16 x 0.0010) = 0`) | 2 quanta per row, 4 rows, G = 8 units of content | EXPECTED DETECTOR (the faces' clicks of `light` rows, content 2 each, 4 per return) | the faces' escaped lines: family `light`, content per row |
| the given rows' frequency | none | 2 steps per interval | EXPECTED DETECTOR | two faces' phases and counts on one line (section 4 (d) 2) |
| the body's content at the end | 1836 | `1836 - 9 x 8 = 1764` | GAMEBOARD (the record); DETECTOR through the faces' summed content 72 | the sum of the `light` rows' content on the faces |
| the fraction's drift per return | 0 | `+ 1.2 x 10^-4` (section 4 (b)), 1.1 x 10^-3 over the run, below the band's resolution | GAMEBOARD by formula | reading 4 at the last return against the first |
| the loop's widening | none | `a' = a (1 + 2 G / M)`: 0.87 percent per return, 8 to 8.6 Links over 9 returns | GAMEBOARD by formula (the arrival Nodes of the electron's rows, DETECTOR with a detector at every Node) | not read by the faces |
| the tolerance | the give exactly 0 (an integer) | the give exactly 2 per row; f within 1/16 of 0.1416; T within the atoms pins' spread (1454 to 1658 registered at r = 12, `+- 7 percent`) | | a give of 1 or 3 per row at r = 8 is a lattice reading of f outside `[0.125, 0.1875)`, the pin missed and f read, not the form refuted |

The refuting reading of the form is any `light` click in `hydrogen_r12`
with reading 4 whole within 1/16 (section 4 (d)); the refuting reading of
section 4 (b) is f at r = 8 falling into the band within the run. Bohr's
condition, Balmer's lines and de Broglie's whole number appear here only
as the thing the closure is compared with afterwards (ALGEBRA.md section
4); the given rows' frequency, 2 steps per interval, is NOT COMPARED
with any line (section 4 (c): the give is not a transition between two
closures). Host cost: series H's r12, about 60 s and a few hundred
megabytes per world; the per-Node detector array, when it lands, `53^3`
integers per interval (record 721), a host cost like the presence.

## 6. What it is not

- No change to the six verbs: the rule composes verbs 1 and 6 and the
  law's paid release; no seventh verb, no root, no float.
- No change to the one reading set: the body reads its own momentum (its
  record) and never its own rows; the give's rows are read by others as
  any rows.
- No change to the click's weight: the click stays the bilinear form
  `f^T G f` on the record's phase-count vector; the body's own phase
  enters no click.
- The alternative not chosen: the click-weight form, the owner's picture
  of record 874 (the loop interfering with itself, the body's phase as a
  component of the record's vector read against the returning row's
  phase at the click), stays named in ALGEBRA.md section 6 (ii) and is
  not designed here (record 881 chose the give).
- The planets' correspondence limit (record 881 (b)), a consequence,
  GAMEBOARD by formula: any body circling a fixed body under any column
  closes with the world's one h, so a planet of content 2^24 has j
  enormous and f a fraction at every return; it gives at most `n_g / d_g
  - 1` quanta per row, 15 at [16, 1], G <= 60 per return over six
  headings, a relative loss of at most `3.6 x 10^-6` per return and a
  widening of at most `7.2 x 10^-6` per return (`2 G / M`), the give per
  loop bounded by the declared quantum and not by j: the rule's effect
  on a body vanishes as `h_q n_g / (d_g M)`, Bohr's correspondence limit
  in the law's own words, compared with and not put in.

## 7. Cost

| Where | Storage | Work per interval | Kind |
| --- | --- | --- | --- |
| a Node | nothing (LOCALITY-1; the row born is an event at the Node, as every release) | nothing beyond the law's | the law's |
| a body's record | two integers per axis (the action row's remainder, below h; the give row's accumulator, below N h) and one sign integer: four beyond the three action rows already there, fixed for fixed K | one addition per counted Link on the stepped axis (beside the action row's), one sign comparison, and at a return one sum, two Euclidean divisions and one paid release of at most (the directions' count) rows | the law's, fixed |
| the host | the identity under `hypotheses` in the record; the per-Node detector array if declared (`53^3` integers per interval, record 721) | the world's run, series H's cost (about 60 s and a few hundred megabytes per world) | host, separate |

## 8. The row proposed for docs/HYPOTHESES.md (not written into it), and the Highlights line

For the list of section 27 of [HYPOTHESES.md](../../HYPOTHESES.md) (the
declared hypotheses outside the law), proposed here and written there
only by its owner on the owner's word:

| Derivation | Where it lived | The condition | What would close it | What would refute it | Held by |
| --- | --- | --- | --- | --- | --- |
| The atom's stability as a give of content at the return (the open loop gives, the closed loop stays) | designs/atom_give/DESIGN.md; ALGEBRA.md section 6; records 858, 874, 881 | `atom-give-v1`: the give rows on the record, the return's threshold, the pair `[n_g, d_g]`, the family key `frequency_by_content`; the limit's algebra says the give of content moves the closure sum at second order only (section 4 (b)) | nothing closes it into the law by derivation: it is a hypothesis by construction; the run of section 5 against its pins, then the reviewer's and the owner's admission | a `light` click at r = 12 with the closure whole within 1/16; or the open loop closing within the run against section 4 (b) | this entry |

The Highlights line is the Boss's (record 881): the decision, with this
file as the design and the identity off by default; every line of 5.4
named in the six lines' item 5 is kept.

## Links

[ALGEBRA.md](../atom_algebra/ALGEBRA.md) (sections 1, 2, 3, 6 and 7 at
643b7ae7); [the atoms pins](../atoms/PINS.md) and [their generator](../../../examples/events/atoms/make_worlds.py);
[BEAM_LAW note 40 and note 41](../../BEAM_LAW.md); [DERIVATIONS_BEAM 6.4
and 19.1](../../DERIVATIONS_BEAM.md); [the local integer operation contract](../../ARCHITECTURE.md#local-integer-operation-contract);
[LOCALITY-1](../../../SIMULATOR_DEFINITIONS.md); [the three tests](../../../skills/workflow.md);
[HIGHLIGHTS 5.4](../../HIGHLIGHTS.md#54-the-detector) (records 281, 721,
754, 762, 817, 844, 864); [HYPOTHESES section 27](../../HYPOTHESES.md).
