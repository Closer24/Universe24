# Bell's one nonlocal gather: is there a local mechanism, or is the honest statement the end (the open-problems physicist, read-only, 2026-09-21)

Problem (4) of the seven (record 393 of the log of 2026-09-20, on the
Boss's branch at the time of writing): "Bell's one action at a distance:
the joint gather at the far completion is nonlocal by design; the honest
statement (local transport plus one nonlocal measurement operation) is
the only solution the Boss sees; it is not a mechanism". The order: is
there any local mechanism, or is the statement the end. Read against
`main` at be194aca: the one click of amplitude-v1 (BEAM_LAW note 37 (x)
to (xii); the amplitude design's sections 3 and 4), the register's Bell
entries (A2 under the Beam Law, S = 2 exactly with local windows; the
pair under the one click, 27, 5, 5, 27 and S = 176 / 64; the choosers on
the GameBoard), DERIVATIONS 6.2, 6.5, 6.7, 22.3 and 24.3 rows 1 to 3, and
the two papers' causal sections. Every number is from
[bell_map.py](bell_map.py) beside this note (the click's own forms on
the exact half-angle cosines, the rungs at the nearest integer; the
built click's tables round them at 1 / 256 and give the same cells) and
its output [bell_map.out](bell_map.out); no run, nothing registered,
nothing decided. Notation as the workflow's rule: u the record's birth
phase (the wheel's value), a and b the two settings, o_A and o_B the
outcomes, **f** the record's phase-count vector, S the CHSH sum.

## 0. The verdicts, stated at the top

| Candidate | What it is | Verdict |
| --- | --- | --- |
| (i) a local mechanism within the six verbs: each arm's rows read at their own Node against their own setting, whatever the rule does with u | LOCALITY-1 as written for a click: the record's rows at this Node and this setting | **NOT ADMISSIBLE, PROVED** (section 2): every such outcome is a function of (u, its own setting), and for every such pair `S <= 2` (Fine 1982; the map's brute force: the largest CHSH sum over the 16 assignments per u is 2); the law's registered instance is A2 under the Beam Law, `S = 2` exactly with the triangle `1 - 4 k / N`; the register's 2.75 at N = 64 and 2.828 on the plateau are unreachable by it |
| (ii) superdeterminism: the wheel u correlated with the settings | the settings read at the birth | **NOT THE LAW**: u is drawn at the birth before any setting exists and no rule that sets a setting reads it (the choosers' world: the settings are streams of coprime periods with no meeting; measurement independence measured, not assumed) |
| (iii) the one gather as built: one record read once at its completion from both settings | amplitude-v1's click: the square of the SUM over the labels of the products of the two arms' rotation entries, the cells by the rungs, no signalling exact | **ADMISSIBLE** (the reviews of amplitude-v1; the law): the minimal nonlocal step, one operation per record, parameter-dependent at the second party and no-signalling in the counts (32 / 64 in all 4096 setting pairs, reproduced); Tsirelson reached as a limit; the class Bell's theorem requires of any deterministic model above 2 |
| (iv) the record as one object: the local test read on the record and not on the Node | "its own record" in the three tests | **the honest statement, and the end**: the gather reads its own record, which passes the local test as written; the record has rows at two Nodes, and that extension is the nonlocality; no mechanism on Links reproduces it (i), and none is needed for what nature measures (no signal, Tsirelson's bound) |

So: the statement is the end, as a mechanism; what this note adds is
where exactly the nonlocality sits on the GameBoard (one cross term, a
product of one entry of A's rotation with one of B's, formed nowhere but
at the gather: section 3), the proof that nothing on Links reaches it,
the measured exclusion of the two loopholes the law could have hidden in
(superdeterminism, signalling), and the honest reading of the local
test.

## 1. The pins, before any number

- **Nature.** CHSH `S <= 2` for every local model (Bell 1964, Clauser,
  Horne, Shimony and Holt 1969); the quantum `2 sqrt 2` (Tsirelson 1980);
  the loophole-free 2.42 +- 0.20 (Hensen et al. 2015) and `2.82759 +-
  0.00051` (Poh et al. 2015), as NATURE 1a and 24.3 rows 1 to 3 cite them.
- **The register.** A2 under the Beam Law: `S = 2` exactly, every E on
  the triangle, no-signalling exact, 326 criteria; the pair under the one
  click: 27, 5, 5, 27 at every CHSH pair, `E = 44 / 64`, `S = 176 / 64 =
  2.75` (N = 64), 2.8125 (256), `181 / 64 = 2.828125` on the plateau 512
  to 8192, the marginals 32 / 64 in all 4096 setting pairs; the choosers'
  world: the settings from two streams with no causal meeting. The
  identity amplitude-v1 admitted by its reviews and the owner's decision
  (record 135, 145).
- **What must not move.** Any of those integers; the one click as the law.

## 2. Theorem: no click that reads one Node's rows against one setting reaches the register's S

**On the GameBoard.** A Bell pair is one record born at a lamp with the
branches `[[0, 1], [1, 1]]`: two rows per arm on the labels 0 and 1, the
same birth phase u on every row of the record, flying on two arms to two
detectors 16 and 16 Links away (the A2 geometry). Each detector's entry
is a rotation `U_s` by its own setting s on the label pair and a click.
What a detector holds when the rows arrive is: the rows of THIS arm
(their labels, phases, amounts), its own setting s, and, through the
layer, the record's identity (u) and the state of the record's offers
elsewhere. LOCALITY-1 for a Node reads its own record and its six
neighbours; the six verbs act on those.

**The proof.** Let the click of arm A be any function of the six verbs
on what arm A holds without the layer's word from arm B: its rows, its
setting a, and u. Its outcome is then `A(u, a)`, and B's is `B(u, b)`,
deterministic given u (the law is deterministic; a tie is a declared
order). For every u the four products `A(u, a) B(u, b)` over the two
settings each are one of 16 assignments, and the largest of `|A B - A B'
+ A' B + A' B'|` over them is 2 (the map's section C); the mean over u
of a quantity that is at most 2 for every u is at most 2. So `S <= 2`
for every local click, whatever the rule is and whatever u carries
(Fine's theorem: a joint distribution over the four outcomes exists
exactly when CHSH holds). The law's own instance is the window gate of
A2 under the Beam Law: `A(u, a) = +` iff `(u - a) mod N < N / 2`, the
correlation the triangle `1 - 4 k / N`, `S = 2.0000` exactly at the CHSH
settings (the map's section B, the register's 326 criteria). No verb
added on the arms, no rate, no table, changes the bound: it is the
bound of every function of (u, a) and (u, b).

**What the theorem does not forbid.** A click whose outcome at B is a
function of (u, a, b): parameter dependence at B, the largest S then 4
(the map). That is what the gather does, and it reaches 2.75 and 2.828,
below Tsirelson's bound by the tables' rounding (the paper's theorem on
the finite-N Bell value), never above it on the plateau.

## 3. Where the nonlocality sits: one cross term, formed only at the gather

**On the GameBoard** (the amplitude design's 4.1 to 4.3, note 37 (xii)).
The record's rows at each arm are rotated by that arm's entry `U_s`; the
layer keeps the two arms' residuals; at the record's completion (the
live count 0, every row ended at a set) the click forms, per outcome pair
`(o_A, o_B)`, the SUM over the two labels of the products of the two arms'
entries and squares it:

    W(o_A, o_B) = (U_a[o_A][0] U_b[o_B][0] + U_a[o_A][1] U_b[o_B][1])^2,

then the rungs at the nearest integer choose the cell by u. The square
of a sum has a cross term the sum of the squares has not: at the
settings (16, 8) and the outcome (+, +) the two products are 0.6533 and
0.2706, their squares sum to 0.5000, their sum squares to 0.8536, the
cross term `2 U_a[+][0] U_a[+][1] U_b[+][0] U_b[+][1] = 0.3536` (the map's
section D). That cross term is a product of one entry of A's rotation
with one of B's: it is a number that needs both settings, and nothing on
the GameBoard holds both settings at one Node. The local click of
section 2 forms the sum of the squares (each arm's own square, one per
pair) and reads the triangle; the gather forms the square of the sum and
reads the cosine. Between the two lies exactly `S = 2` and `S = 2.75`.

**Why it is one operation and not a signal.** The gather is one read of
one record, once, at its completion, in the layer (the apparatus's list,
not a Node: principle 5, "the apparatus's one non-local operation"). Its
first party's channel is chosen by u alone (`+` for `u < N / 2` at every
setting), so A's marginal is 1 / 2 for every (a, b); B's is 1 / 2 by the
mirror symmetry of the weights and the rungs at the nearest integer (the
map: 32 / 64 in all 4096 pairs). Neither party can read the other's
setting from its own counts: no signalling, exact in the counts. The
dependence of B's outcome on a is the resource, as it is in quantum
mechanics (the joint conditional state); the law spends it in one
deterministic step where quantum mechanics spends it in the Born rule
applied to an entangled state. The law is exactly as nonlocal as quantum
mechanics and no more: it reaches Tsirelson from below (2.75, 2.8125,
2.828125), never the algebraic 4.

## 4. The two loopholes the law could have hidden in, and why it does not

- **Superdeterminism.** In a deterministic world file the settings could
  be numbers correlated with u through the initial state, and then S
  says nothing. The register measured it: the choosers' world (issue
  #363) reads each setting from a stream of a third and a fourth source
  with coprime periods and no causal meeting with the pair lamp; under
  the window gate `S = 2` with the triangle, under the one click the
  settings enter only at the gather and the marginals stay 1 / 2. The
  wheel is drawn at the birth, before the settings, and read by nothing
  that sets a setting: measurement independence holds by the world's
  structure, checked, not by fiat.
- **Signalling.** A parameter-dependent model can signal unless its
  marginals are setting-independent; the rungs at the nearest integer
  were chosen for exactly this (the design's 3.3: the strict crossing
  signalled 1 / 64 in 3944 of 4096 pairs; the nearest rung 0 in 4096).
  The paper proves the marginals for the equal-weight pair and leaves
  the unequal pair open; the map confirms 4096 of 4096 at N = 64.

## 5. Is the statement the end? Yes, and here is its exact form

The three tests, read on the gather: generic (one bilinear form with the
declared Gram matrix, no family name), vector (the evaluation, the
product in the ring, one comparison of two products at the rung), local
(it reads its OWN RECORD; a record is the object the local test names).
The local test as written does not forbid the gather, which is why the
reviews admitted amplitude-v1; what the record is, physically, is one
object with rows at two far Nodes, and that is the nonlocality, stated.
A mechanism on Links cannot replace it (section 2). A second object of
the same kind is not needed for anything nature measures (no signal,
Tsirelson from below). So the honest statement, "local transport plus one
nonlocal read of one record", is the end of the mechanism question, with
one sharpening the owner may want in the paper: the nonlocality is not
"an action at a distance" (nothing acts on the far Node: its rows are
untouched, its marginal unchanged) but "one record, one read": the law's
records are extended objects, and the click is local to the record.

**What would change the verdict.** A run in which a local click (section
2's form, the window gate) reads S above 2 on a Bell pair would refute
Fine's theorem on the lattice, which is impossible; a run in which the
gather's marginals move with the far setting would make the law a
signalling model and refute the design's 3.3, which the map excludes at
N = 64 and the paper proves for the equal-weight pair. Neither is a
research run; both are pinned as theorems.

## 6. The owner's question on the conditional derivations, for this problem

Nothing here is conditional: Tsirelson's bound is reached as a limit
(6.2, derived), the finite-N values are exact rationals of the tables
(the paper's theorem), no-signalling is a theorem for the equal-weight
pair and a check for the rest, and the impossibility of a local
mechanism is Bell's and Fine's theorem restated on the lattice (section
2). The paper stands as it is; the open-problems item (4) can say "the
statement is the end: a theorem, not a gap".

## 7. Proposed lines for the documents I do not write

- **The paper** (the coordinator): the open problems' item (4) restated:
  "no local mechanism exists for the pair, by Fine's theorem on the
  lattice (every click reading one Node's rows against one setting gives
  `S <= 2`; the law's A2 with local windows reads 2 exactly); the one
  gather is where the cross term `2 U_a U_a' U_b U_b'` is formed, the one
  number that needs both settings; the law is exactly as nonlocal as the
  Born rule on an entangled state and no more".
- **DERIVATIONS_BEAM 22.3** (the mathematician): after "the registered
  `176 / 64 = 2.75` has no such distribution": "and no click of the six
  verbs on one Node's rows against one setting reaches it: the largest
  CHSH sum over the 16 deterministic assignments per u is 2, the law's
  window gate reads exactly 2 (the open-problems note on Bell, section
  2)".
- **NATURE.md row 1a** (the physicist): a clause "the local reading of
  the same rows (A2 under the Beam Law) reads 2 exactly: the register
  holds both sides of Bell's bound on one world".
- **HIGHLIGHTS 5.4**: nothing.

## 8. Questions, through the Boss

1. **For the owner (substantive)**: none. One wording for the paper is
   offered in section 5 ("one record, one read" in place of "action at a
   distance"); the physics does not decide words.
2. **For the Boss**: none; no run is proposed (the two pins of section 5
   are theorems).

## 9. Links

[BEAM_LAW note 37](../../../BEAM_LAW.md#10-implementation-notes-2026-09-19-the-implementation) (x) to (xii);
[the amplitude design](../../amplitude-v1/DESIGN.md) sections 3 and 4;
[DERIVATIONS_BEAM 6.5](../../../DERIVATIONS_BEAM.md#65-the-uniqueness-of-the-clicks-square-a-lattice-gleason),
[6.7](../../../DERIVATIONS_BEAM.md#67-the-click-without-amplitudes-one-bilinear-form-on-the-records-integer-vector),
[22.3](../../../DERIVATIONS_BEAM.md#223-bell-beside-it),
[24.3](../../../DERIVATIONS_BEAM.md#243-the-delta-p-table-every-computable-difference-from-quantum-mechanics-or-relativity-as-the-law-is-declared) rows 1 to 3;
[EXPERIMENTS A2 under the Beam Law](../../../EXPERIMENTS.md#a2-under-the-beam-law-2026-09-19) and
[A2 with the choosers](../../../EXPERIMENTS.md#a2-with-the-choosers-on-the-gameboard-2026-09-20);
[NATURE](../../../NATURE.md) row 1a;
[the three tests](../../../../skills/workflow.md#the-three-tests-of-every-rule-generic-vector-local-the-model-owner-2026-09-21-record-202).
