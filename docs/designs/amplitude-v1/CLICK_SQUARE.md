<!-- The physicist's read-only design note of 2026-09-21 on the owner's question of the click's square (docs/LOG_2026-09-20.md record 170 the question, record 171 the answer); copied from the scratchpad unchanged. Verdict: the square stays in the apparatus's layer with Theorem 2 as the theorem; a return is refuted by the two experiments; a mirror without a return forms no square and loses Bell's 176/64. -->

# The click's square: where X^2 + Y^2 can live on the GameBoard (the physicist, read-only, 2026-09-21)

The owner's question through the paper session: the click's norm X^2 + Y^2 is
the one operation of the model beyond translate-and-threshold, multiply by a
declared integer matrix, and add; it is where the Born rule is put in. Three
ways were named: (1) keep the square in the apparatus's layer and prove it is
forced; (2) the square as a RETURN (the detector sends back what reached it
along the reversed paths, the inverse split, the ladder at the source, no
layer; the retired postulate 24); (3) leave the square in the apparatus with
(1) as a theorem. The Boss's candidate, checked first: the detector as a
phase-reversing mirror, so that the record meets its own mirror image in
flight near the detector and the merge forms the autocorrelation
|ev(f)|^2 = ev(f * f~) as real rows, with nothing returning to the source.

Read on main at `78d130d9`: AGENTS.md; BEAM_LAW.md note 37 and section 5;
TWO_SLITS.md sections 1 and 2; amplitude-v1 DESIGN.md sections 2.4, 2.5, 4
and 11; POSTULATES.md section 24; Highlights (the 2026-09-19 closure, "So we
do not want a return to the source"); LOG_2026-09-20 records 156, 158, 160,
164 and 167; `nature_beam.py` (the interval's six steps, `IDENTITY_FIELDS`,
`merge`, the rest ray at 2488 to 2500), `meeting.py`, `amplitude.py` (`end`,
`cells`, `complete`); `two_slits_map.py` as the model of the paths. No engine
run. The integers are in `check.py` and `check.out` beside this file
(`reconcile.py` for the span). Everything below is in the law's words.

## 0. The verdict in one paragraph

The physics allows way (3) and nothing else. The square is not an operation
any Node can perform on two rows: the law has no product between rows (the
merge adds signed amounts of identical rows; the collision permutes headings
and reads no phase and no amount; the meeting reads every number but the
row's own), and the only bilinear product on the GameBoard is at a measured
event (content x flow, the push). The Boss's mirror cannot form the cross
term of the norm: on `slits_low` the two rows of one record to a pixel are
two non-parallel world lines, the reflected first row and the arriving
second row never share a Node and an interval at 17 of the 27 two-path
pixels, and where they do (10, at a Node the two digital lines share just
before the pixel, by a coincidence of the arrival difference) the merge does
not act (the direction and the age are identity fields) and the collision
only permutes. For the pair, any form in which each detector reads its own
half alone, with u and the labels shared, is a local assignment A(u, a),
B(u, b): S <= 2 as an identity, and with the rotation reading E = +1 at every
setting; the registered 176/64 needs the product of an entry at A and an
entry at B for the same label, which no Node holds. The return, way (2), is
refuted by the two experiments as pins (3 L / c against L / c; the setting
2 L / c earlier against the final setting). What Theorem 2 does prove is
that the Born WEIGHT is local: the split conserves sum w^2 / m for every
declared vector and for no other power, so every row carries the record's
total in its multiplicity and each end Node could know W_k / m without a
ledger; what stays non-local is the EXCLUSIVITY (exactly one cell per
record over cells at different Nodes and sets, the ladder's cumulative
order) and the pair's cross-arm product. Those two are the ledger's whole
job, and it is the minimum owner of them. The decision of 2026-09-19 stands.

## 1. The Boss's candidate, checked

### (i) The merge, the crossing rule, and what a meeting of two rows is

The merge (`nature_beam.py`, `IDENTITY_FIELDS`, `merge`) adds the signed
amounts of rows equal in node, direction, age, phase (modulo N / 2 with the
sign, the cancel), number, content, record, branch, multiplicity and hand.
Two rows of one record merge only when co-directed and co-aged at one Node.
A reflected row (direction reversed, age larger by the walk) and an arriving
row of the same record are never one group: no addition, no cancel. The
merge has no product in it; the autocorrelation's coefficient
sum_p f_p f_{p+q} is a product of two amounts, an operation that exists
nowhere between rows.

Two rows crossing: at a Node, the collision table permutes the single units
of one (number, content) class in the eight slots, a cyclic shift that reads
neither phase nor amount (section 3 step 3); on a Link, nothing happens: a
row is at a Node at every interval, and two rows crossing on a Link swap
Nodes and are never at one Node in one interval. The crossing rule (record
158) is a rule of what a BODY reads: a body and a row meet once at the
crossing of their world lines. It says nothing of two rows, because rows do
not read rows of their own number (`meeting.py`: "paid units never read each
other"; the reading set is every number but the reader's own). So a head-on
meeting of a reflected row and an arriving row of one record is, under the
law as built and under the crossing rule, no event at all.

### (ii) The geometry on `slits_low`: does the reflected head meet the tail?

By the map (`check.py` section 2, `reconcile.py`): 75 pixels with rows, 27
with two or more rows (25 from both openings, 2 from one opening on adjacent
fan directions). The two rows' arrivals differ by 0 to 11 intervals (mean
5.3; 0 at 5 pixels), the leg's 13 intervals equal for both openings, so the
record's span at a pixel is 11 intervals on this world (the mathematician's
18 is the path difference at the heading pace; the flight table's pace makes
the arrival difference 11; either bounds the hold below).

A row reflected at the pixel with its direction exactly reversed retraces its
own world line: at the interval t1 + k it is where it was at t1 - k. The
record's other row walks its own line toward the pixel. They share a Node
and an interval only at a Node X the two digital lines have in common (2 to
11 shared Nodes when the openings differ, just before the pixel; 35 to 39 on
the two same-opening pixels) and only when the arrival difference equals the
sum of the two rows' step times from X to the pixel: a coincidence met at 10
of the 27 pixels and at none of the other 17. A row mirrored in x alone
(direction (-a, b)) leaves the screen column toward x > 52, where no path of
the record lies: 0 of 27. And at the 10 coincidences nothing forms: the
merge does not act (different direction and age), the collision permutes.
So the autocorrelation does not form in flight, neither completely nor
partially; the "amount the meeting leaves within the detector's reach" is
the rows' amounts unchanged. The reading that the mirror would leave to the
set is therefore the diagonal one, w1^2 + w2^2 per row read alone: its
Pearson with the Euclidean two-source cosine over the 75 pixels is 0.089
against the layer's 0.390 on the built phase (the cross term 2 w1 w2 cos is
1.36 of a row's norm on average against W_d's 2.31, from 0.50 to 3.41 of
W_d). Not an approximation of W_d: the fringe is the cross term and the
cross term is absent.

A second defect of the mirror: a reflected row that is not absorbed walks
back along its path to the opening and to the lamp, a return to the source,
which the decision of 2026-09-19 forbids. To keep the decision the reflected
rows must end within the detector's reach after the span, which is a hold,
not a reflection: section 4.

### (iii) The Bell pair

Today the joint cell is the ledger's: J(o_A, o_B) = sum over the labels l of
U_a[o_A][l] U_b[o_B][l], squared (DESIGN 4.2, `amplitude.cells`), giving
E x 64 = 44, -44, 44, 44 and S = 176/64. Under the reflection form each
detector reads its own half alone. The label is an identity field of the
merge, so the two labels' rows never add coherently on one arm: the
autocorrelation per channel is sum_l |U_a[o][l]|^2 = C'^2 + S'^2, equal on
the two channels at every setting (`check.out` section 3: 65536, 65773,
65522, 65773, 65536 at s = 0, 8, 16, 24, 32, the same on + and -). Each arm's
cell is + for u < 32 and - for u >= 32 whatever its setting; with the one u
shared, E(a, b) = +1 at all four CHSH settings, S = 2, and the controls
E(0, 32) = +1 against -1 and E(0, 16) = +1 against 0. More generally, any
form in which A's click is a function of (u, the labels, a) and B's of (u,
the labels, b) is a local deterministic assignment with the shared variable
u, and S <= 2 is an identity on it (the design's section 11 says the same of
its click rows: "a product of single-row phases is a product state, S <= 2").
The correlation is in the product of an entry at A and an entry at B for
the same label, and no Node of the GameBoard ever holds both. The reflection
form loses the registered 176/64 and reproduces nothing of L3.

## 2. The two experiments as pins for any form (iv)

(a) The click's time. Today the layer completes a record when its live
count reaches 0, at the last row's end (`Layer.end`, `complete`): the click
is at L / c plus the record's span at the set (11 intervals on `slits_low`),
never later. A form that returns to the source and clicks there puts the
click at 3 L / c (out, back, the message); at Hensen's 1.3 km that is
8.7 microseconds against the time-tagged L / c: refuted. The reflection and
the hold form of section 4 click at L / c plus the span: they pass.

(b) The setting. Today `Layer.end` applies the rotation U_s with the set's
setting at the tick of the row's arrival (the `rotation` argument of `end`
is the setting the window has when the row ends); the layer's completion
reads what the arrivals wrote, so a setting changed while the quantum is in
flight is the one read (Wheeler, Jacques 2007): passes. A standing return
from earlier records lets the source decide at a birth with the apparatus as
it was 2 L / c earlier: refuted. The hold form reads the setting when the
hold ends, at arrival plus at most the span: passes.

Way (2) fails both pins, and by section 1 (iii) it also could not give the
pair's correlation without the return: the amount returning to the source,
W_d, is real and needs only the three operations, but it is the wrong number
at the wrong time with the wrong setting.

## 3. Theorem 2, and what a lattice Gleason would and would not prove

Checked (`check.out` section 1): the split (w, m) -> (w a_i, m A) with
A = sum a_i^2 conserves sum_i (w a_i)^k / (m A)^{k/2} for every declared
integer vector only at k = 2 (for (20, 21), (3, 4), (119, 120), (1, 1),
(1, 2, 3): k = 1, 3, 4 fail, since sum a_i^k = A^{k/2} for every vector with
two nonzero entries only at k = 2, the power mean). So the exponent is forced
by three things the law already has: the split is a declared integer matrix,
its norm is the sum of the squares of its entries (the only power for which
the norm of an integer vector under every rotation of the splitter's matrix
is the same integer), and the total is conserved at every cut. The phase
rotation invariance is the merge's cancel [p + N / 2] = -[p] on the record's
element of Z[Z_N], and |ev(f)|^2 is invariant under [q] f for every q. The
non-negativity is the norm's.

What is proved: among power laws the square is forced; the split and the
merge are inverses (DESIGN 2.4, checked). What is not yet proved and should
be stated as the mathematician's theorem, not the physicist's: that
additivity over the cells under EVERY declared unitary split, non-negativity
and the rotation invariance force a positive quadratic form and not another
function of |ev(f)| (the Jordan-von Neumann route needs the parallelogram
law on the declared splits; the declared splits are a finite family per
world, so the theorem holds on the family the world declares and is stated
so). On the lattice the total is not exactly conserved where paths re-meet
not through a unitary recombination (DESIGN 2.5), and the ladder's
normalisation by the record's Total at completion is the rule; Theorem 2
holds row by row and the multiplicity carries the birth norm on every row.

The consequence that matters for the question: the Born WEIGHT of an end is
local. A row at an end Node carries (w, m) and its phase; the coherent sum
over the record's rows present at that Node and |sum|^2 / m is that Node's
share of a unit, and the sum of the shares over all ends is 1 (up to the
lattice's 2.5). No Node needs the ledger to know its weight, only to know
its PLACE in the order of the cells and whether the record's other rows,
elsewhere, clicked instead. That place is the exclusivity, and the
exclusivity is the ladder's cumulative C_k: a sum over cells at different
Nodes and sets, the atemporal step. For the pair the cross-arm product is a
second such step. The ledger is the owner of exactly these two.

## 4. (v) The group-ring form at the detector's set, and its classification

The other candidate: W = ev(f * f~) computed at the detector's set from the
rows present over the record's span. What it needs is that the rows of one
record that reach the set at different intervals be present at one Node at
one interval. The law already has the state that does this: a REST ray
keeps its age and does not turn (`nature_beam.py` 2488 to 2500: a resting
row's age and phase are frozen), and a parked unit is the table's. So the
form is: a row that reaches a detector's Node under this rule is not ended
at arrival; it rests there with its phase frozen (its own accumulators
untouched) and carries one more count, the hold, an accumulator on the row
(record 155: every count an accumulator on the record); when the hold
reaches the detector's declared depth D (in intervals; D >= the record's
span at the set, 11 on `slits_low`), the set reads ALL the rows of that
record present at the Node in that one interval, the coherent sum over them
and its square, the same X^2 + Y^2 as the layer's per-Node weight, and ends
them. The frozen phase is what makes the reading right: the arriving row's
phase advanced along its longer path, the resting row's did not, so their
difference is the path difference's phase, as the ledger reads it today;
had the resting row kept turning, the two would always agree and no fringe
could appear. On `slits_low` this gives the layer's 75 per-Node weights
exactly (the same rows, the same phases, the same sum), and it reads the
setting at the hold's end (the pin (b) passes) at L / c plus at most D (the
pin (a) passes).

The honest classification under "a Node keeps nothing, a record keeps its
own": a held row is the record's own (a row is a row; the Node holds the
rows present and nothing else; the hold is a count on the row, bounded by
D, and every row leaves at D); the cost per Node is the rows present, bounded
by the rate times D. It is not a register. What WOULD be a register is a
table at the detector's Nodes indexed by record identity holding (amount,
phase) of rows already ended, or the detector's own `record` used as a memory
of another record's rows: the detector's one record is its own (the
cumulative X^2 + Y^2 and the phase it takes as its own after a click,
section 5), not a ledger of live records; the layer relocated to the
detector's Node is the layer. The bounded window "of the detector's own
span" is lawful only in the first form, as rows resting on the GameBoard.

And what it cannot give, even so: the click. The set knows W_node / m (the
weight is local, section 3) but not the record's other ends, so it cannot
choose one cell of the record: either every end Node clicks by its own
weight against u (then the count of clicks per record is not one: the
expectation is right by Theorem 2 and the exclusivity is lost), or the
ladder's cumulative order is read, which is the ledger. For the pair the
held rows at A never hold B's entries. So the hold form moves the WEIGHT
onto the GameBoard, where it belongs, and leaves the ledger exactly its two
non-local jobs, the order and the pair's product. It does not remove the
layer; it makes its content smaller (per record, the ends' weights and
Nodes, no pointers per row), and is worth building only if the owner wants
that smaller ledger, with `slits_low`'s per-Node weights as the pin
(identical under D = 11) and L3's 176/64 unchanged.

## 5. The three ways, judged

- (1) The square in the apparatus's layer, proved forced: the exponent is
  forced (section 3, checked); the full quadratic-form theorem is the
  mathematician's to state on the declared splits. Admissible; the proof's
  local half (Theorem 2) is already the law's.
- (2) The return: not admissible. Refuted by the click's time (3 L / c) and
  by the delayed choice (the setting 2 L / c earlier), and it would reopen
  postulate 24 which the owner closed on 2026-09-19. The mirror without a
  return (the Boss's candidate) is not a return but also not a square: no
  product between rows exists in the law, the two paths' rows do not meet in
  flight at 17 of 27 pixels and form nothing at the other 10, the diagonal
  reading it leaves has Pearson 0.089 against 0.390, and the pair falls to
  S = 2 with E = +1 at every setting.
- (3) The square stays in the apparatus with (1) as a theorem: this is the
  physics. State the theorem in two halves: the weight is local on the
  GameBoard (Theorem 2, the multiplicity carrying the norm), the exclusivity
  and the pair's product are the ledger's, the one atemporal step, owned by
  the apparatus at the one-way border and by nothing else.

## 6. Recommendation for the owner, one sentence

Keep the square in the apparatus's layer (way 3) with Theorem 2 as the
theorem that the weight is local and the ledger owns only the order of the
cells and the pair's product; do not reopen the decision of 2026-09-19,
since a return puts the click at 3 L / c with a stale setting and a mirror
without a return forms no square and loses Bell's 176/64.

## 7. What was checked and what was not

Checked in integers (`check.py`, `check.out`, `reconcile.py`): the exponent
on five vectors; the two paths' arrival difference, shared Nodes and
meetings on all 27 two-path pixels of `slits_low` under both reflections;
the diagonal reading's Pearson against the layer's; the per-arm
autocorrelation at the five settings and the local form's E and S; the
layer's joint weights at the CHSH settings (E = 0.708, 0.706 before the
ladder's rounding, the registered 44/64 after it). Not done: any engine
run; the full quadratic-form theorem; the hold form as code (a design
sketch only, section 4, not ordered). The hold form is recorded here as the
one lawful shape of "a bounded window at the detector", for the owner to
take or leave; nothing in this document changes the law.
