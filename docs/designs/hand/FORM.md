# hand-v1, the hand on the message: the integer form and bounds (read-only, the mathematician, 2026-09-20)

On the Boss's assignment under the owner's decision of the day ([record 119](../../LOG_2026-09-20.md),
"go on everything, in parallel, as generic as possible, on the information
problems": item 4, hand-v1, a hand on the message, an axial record and a
right-hand rule in `become`, the weak transformation acting on one hand
only, the parity test the cube reflection). The physicist's design is
written in parallel; this file gives the integer representation, its
bounds, the action of the 48 symmetries and the rules the design must
obey to be generic. Every integer is from `hand_map.py` beside this file
(`hand_map.out`: the 48 signed axis permutations, their action on the six
headings as polar and as axial vectors, the hand's sign, and the
right-hand rule's sign under each, checked exhaustively). Nothing is
built; no run.

## 1. The representation: one hand bit on the message, one axial record on the body

Two objects, because the message and the body are different things:

| Object | Where | Representation | Bound | Under the 48 symmetries |
| --- | --- | --- | --- | --- |
| the **hand** of a message (a row) | a column of the store, `hand`, one int8 per row | h in {-1, 0, +1}: 0 no hand (every family today), +-1 the two hands; a pseudoscalar (the helicity: the sign of the spin's projection on the flight, a bit RELATIVE to the row's direction, which is why it needs no axis on the row) | 3 values; no arithmetic on it but a sign product | h -> det(g) h: kept by the 24 proper rotations, negated by the 24 improper (the reflections and the inversion) |
| the **axial record** of a measured event | the measured-event key `axis`, one of the six headings in Port order with its sign carried by the heading (0 .. 5), or absent | a signed heading: an axial vector, the body's spin axis for the right-hand rule (the nucleus's polarisation in the Wu experiment) | 6 values or none; a world constant of the body, untouched by pushes and steps (a body does not turn) | a -> det(g) g a: the same signed heading under a proper rotation as a polar vector would take, its opposite under an improper one (`hand_map.out`, the "axial image" column) |

Why not an axis on the row: an axial vector on every row is 6 more values
per row and must be transported through every re-creation with a rule of
its own at each (a mirror re-emits on other directions: what happens to a
row's axis?), while the helicity bit is carried unchanged and means the
same thing on every direction; the 48 act on it by det(g) alone, one sign,
exactly as they must (a pseudoscalar). The representation the 48 act on
cleanly is therefore: **the bit on the message, the axis on the body.**

Carried through every re-creation unchanged: a `rerelease` (mirror,
opening, splitter), a split (every output row takes the input's hand), a
label rotation and a gate (they act on labels, not on the hand), the
meeting (a turn of direction; the helicity is direction-relative, so it
stays), a home. A `become` product is born with the hand its product
declares (section 3). The merge's normal form takes the hand as an
identity field: two rows of opposite hands never merge and never cancel
(opposite helicities are orthogonal; a left row and a right row in
antiphase are two rows, not nothing). A collision permutes directions of
singles and leaves the hand on the row as the phase is left.

## 2. The action of the 48 symmetries, as a table

`hand_map.out` lists every g = (a permutation of the axes, three signs),
det(g) = sign(permutation) x the product of the signs; 24 with det +1, 24
with det -1; the group closes and det is multiplicative on all 48 x 48
products (checked), so the hand's representation h -> det(g) h is a group
action. For each g the table gives the image of each of the six headings
as a polar vector (what the genericity probe applies to positions,
directions, momenta and every vector of a world today) and as an axial
vector (det(g) g e: the same image under the 24 proper rotations, the
opposite heading under the 24 improper). The first rows (the identity, the
reflection z -> -z, the reflection y -> -y):

| g | det | polar image of (+x -x +y -y +z -z) | axial image | h |
| --- | --- | --- | --- | --- |
| identity | +1 | 0 1 2 3 4 5 | 0 1 2 3 4 5 | h |
| z -> -z | -1 | 0 1 2 3 5 4 | 1 0 3 2 4 5 | -h |
| y -> -y | -1 | 0 1 3 2 4 5 | 1 0 2 3 5 4 | -h |

**What the genericity probe's T2 must do.** The probe transforms a world
by g: every position, direction, momentum and declared vector as a polar
vector (as today), and, with the hand, every `axis` key as an AXIAL vector
(det(g) g a) and every declared hand (on an `in_transit` row, on a `become`
product, on a table entry's admitted hand) by det(g). With that
transformation a world with hands is byte-identical under all 48 (the
probe's "parity-symmetric world stays identical"): the law is covariant.
The parity TEST is the other transformation: g applied as a polar
transformation only (the hands and the axes left as declared): a world
without hands is identical under all 48 as today, and a weak world with a
hand reads differently under the 24 improper ones (section 3: the products
leave in the other hemisphere), identical under the 24 proper ones. That
is Wu's experiment as a reading: the mirror image of the apparatus with
the same left-handed rule gives different counts.

## 3. The right-hand rule for `become`'s products, in integers

The `become` key's products gain a fourth field, the hand: `[family,
amount, content, hand]` with hand in {-1, 0, +1} (0 by default: no hand,
the rule as it is today, bit-identical). A product with a hand is born on
the parent's `directions` restricted to a hemisphere of the parent's axis:

    admitted(d) := sign(a . d) = -hand, or a . d = 0

with `a` the parent's `axis` (a signed heading), `d` the product's
direction vector from the world's table, `a . d` an integer (one component
of d, since a is a heading: |a . d| <= P = 64), `sign` in {-1, 0, +1}. The
apportioning over the admitted directions is the whole apportioning of
today (`apportion_whole` with the leftover counted from the clock age) over
the admitted subset in the declared order; a product with a hand on a
parent without an `axis` is refused at load (a hand needs an axis to be
read against), and a parent whose admitted subset is empty for a declared
hand is refused at load (a fan with directions on both sides of every
heading is never empty). The recoil is the labels of the rows born, as
today. So the weak `become` acting on the left hand only is: its charged
product declared with hand -1 (the beta, left-handed) and its neutral
product with hand +1 (the antineutrino, right-handed), born in opposite
hemispheres of the parent's axis; a product with hand 0 is unchanged.

The integers of the rule: `a . d` is a lookup of one component with a
sign, no product; nothing is floored, nothing is bounded beyond P; the
work per product is one comparison per direction of the parent
(`len(directions)` <= 4096). Under every g the sign transforms exactly:
`hand_map.out` checks on all 48 x 6 x 124 vectors that
sign((det(g) g a) . (g d)) = det(g) sign(a . d): kept under the 24 proper
rotations, negated under the 24 improper. So with the axis transformed as
an axial vector the rule is covariant, and with the axis transformed as a
polar vector (the parity test) the hemisphere flips under every improper
g: the reading differs, exactly and only in the weak worlds.

## 4. A filter admitting one hand, and the record click

A table entry may declare `hand: +1` or `-1` (on `measure`, `read`,
`rerelease`, `become`; refused on `pass` and on a family whose rows
carry no hand): a row whose hand is not the admitted one passes the entry
as a row outside a window passes (a `pass` record naming `hand`). Under
the record click this is a which-path factor on the hand exactly as the
`read` entry is on the label (the design's 4.4): the hand is an identity
field of the row, never summed coherently with the other hand, so a filter
removes the rows of the other hand from the record's offers at that set
and the ladder is taken over what remains, with no pointer, no rounding
beyond the ladder's own rungs: **exact**, in the same sense and by the same
code path as the label's which-path factor (the rows of a hand are the
rows of a channel). What it does to the counts: at a set that admits one
hand, a record born with one hand offers everything or nothing there (a
Stern-Gerlach on the hand), and a record born as a superposition of hands
offers its two hands' rows to two sets (section 5).

## 5. Can the hand be the qubit's label bit of a Bell pair, with the design's integers unchanged?

Yes, if it is declared as a LABEL and not as a row field. The design's
label is a bit of the joint label of the record with the rows' amounts as
amplitudes, rotated at a window by `U_s` on the half-angle tables and read
by the label click; a hand declared on a `branches` birth as the label bit
of each arm (`[[label, weight], ...]` with the label's bit k the hand of
arm k, the Bell pair `[[0, 1], [3, 1]]` reading "both left or both right")
gives exactly the design's integers, since nothing in the layer reads
what a label bit MEANS: S = 176/64 at N = 64, the marginals 32/64 for all
4096 setting pairs, 2896/1024 and 11584/4096 (record 105), unchanged. Two
consequences the design must state: (i) the window's rotation `U_s` on the
hand bit is the analyser at the half angle in the basis of the two hands;
a physical polariser reads the linear basis, which is the hand basis
turned by the Hadamard (`rotate {setting: N/4}`) with a phase between the
hands: the design's settings are then the analyser angles in that basis,
and the counts are the same integers under the change of basis (a
rotation composed with a rotation on the tables, one lookup at the click
by the angle-index form of the companion design, `label_rotation/FORM.md`);
(ii) under an improper symmetry the label bit is negated as a pseudoscalar
(0 <-> 1 on that bit): the Bell state `|00> - |11>` maps to `|11> - |00>`,
the same state up to a global sign, so the pair's counts are
parity-symmetric and the probe's cube reflection stays equal on the Bell
worlds, as it should. The one thing that changes nothing and must be
chosen: a row then carries its hand in its label (a record's channel), not
in the `hand` column; a family may have one or the other, never both
(refused at load), so that the merge's identity fields and the offers per
channel are defined once.

## 6. Bounds, locality, identity, tests

- **Bounds.** One int8 per row (`hand`), one int8 per measured event
  (`axis`, -1 for none); `a . d` within P; the apportioning as today; the
  store's row bound gains a factor 3 on the distinct records at one Node
  (rows of different hands are different rows), which the world's
  `age_bound` product already accommodates for a factor of that size (the
  distinct rows at one Node are bounded by `len(D) x age_bound x N x
  numbers x contents`, times 3).
- **Locality.** The hand is on the row and read where the row is; the axis
  is the body's own key; the hemisphere rule reads the parent's record and
  the world's direction table; nothing of another Node, no history.
- **Identity.** `hand-v1` under `hypotheses` when any row, product or entry
  declares a hand or a body an `axis`; absent, no column is written and
  every registered world is byte-identical (the default hand 0 is the
  today's row; the probe's T2 with det on nothing changes nothing).
- **Tests the implementation must add.** (a) the 48-table of
  `hand_map.out` reproduced by the engine's own transformation of a world
  (the probe's T2 with the axial rule): a hand world byte-identical under
  all 48; (b) the parity test: the same world under the polar
  transformation alone, identical under the 24 proper and different under
  the 24 improper, and only where a `become` product carries a hand;
  (c) a product with hand -1 born only on directions with a . d < 0 or 0,
  pinned on a parent with the six headings (three admitted) and with a
  fan (the count admitted); (d) the merge never merges opposite hands and
  never cancels them; (e) the filter as a which-path factor: the ladder
  over the admitted hand's rows equals the label's `read` case integer by
  integer on the path worlds; (f) the Bell pair with the hand as the label
  bit: S = 176/64 unchanged.

## 7. The verdict in one line

Admissible and generic in this form: a pseudoscalar bit on the message
and an axial heading on the body, the 48 acting by det(g) and det(g) g,
one hemisphere rule with an integer sign for `become`, a filter that is
the label's which-path factor on another field; nothing else in the law
reads it, every world without it is byte-identical, and the parity
violation is the reflected world with the unreflected rule, read as counts.
