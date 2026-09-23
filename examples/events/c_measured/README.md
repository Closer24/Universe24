# Series Q: c measured behind a detector

One world, written by `make_world.py` with its register (`expectations.json`,
`derived.csv`, written before the run); the register entry is
[Q, c measured behind a detector (2026-09-21)](../../../docs/EXPERIMENTS.md#q-c-measured-behind-a-detector-2026-09-21).
The question, in the model owner's words of 2026-09-21 ("go for it", record
236 of the day's log: verify c by a run behind a detector against the
formula), under his rule that a formula gives and a run proves
([the shared workflow](../../../skills/workflow.md), "The main course"):
does every row of a fan leave the GameBoard through an open face (an open
face is a detector, an escape is a click) at the tick the closed form of
the flight gives, on every direction, and what pace do the faces read
against c = 1 / sqrt 3 Links per interval? A research run, made once,
never a test; the expectation below was written before the run from the
formula; a reading outside its expectation is reported with its numbers,
never moved. Every number is one of two kinds
([the register](../../../docs/EXPERIMENTS.md), "Two kinds of readings"): a
DETECTOR reading (a face's click: its tick, its Node, its face; the
lamp's birth record) or a FORMULA number (the closed form's integer,
written before the run); no GameBoard reading is used. The six faces
are detectors at rest on the GameBoard: this run's claim is the pace a
detector at rest reads; what a detector in motion reads is another claim
([DERIVATIONS_BEAM 4.2 and 4.5](../../../docs/DERIVATIONS_BEAM.md#42-a-moving-body-what-it-reads):
a moving reader's one-way count is `c -+ v`, the two-way count null, the
two-way time not; NATURE.md rows 4a, 4b, 5b), not made here (record 304
of the day's log).

Notation (the owner's rule, record 184): every symbol is named at its
first use; a scalar is plain (c the pace of a row, Q the label's scale,
tau the age, k the Link count, S_1 the Manhattan length, T_D the
resolution), a vector is bold lowercase (**x** a position, **d** a
displacement), and the direction vector keeps its uppercase D as in
BEAM_LAW; inside code spans every symbol is plain.

## The world

`c_measured.json`, `"law": "beam"`, the model `beam-c-measured-v1`: an open
cube of 65^3 Nodes (the half-width 32), every axis open, so that its six
faces are the detectors `face:+x` .. `face:-z`; K 290, N 64, `release`
[0, 1], `suspension` 0, 100 intervals. One lamp of the paid family `light`
(quantum 1, from the shipped definitions) at the centre **x**_0 =
(32, 32, 32), `fixed`, with the content 290 and the rate [1, 1] on the fan
of 290 primitive directions (a, b, c) with 0 < |a| + |b| + |c| <= 6 (the
fan series E, I and K declare; 284 declared beyond the six headings). At
K 290 its clock turns once at its first self-creation (tick 1) and the
birth of one record of 290 rows of amount 1, one per direction, costs
exactly its 290 units (E = h f), so the lamp holds 0 after and turns no
more: one birth, one row per direction, nothing else on the GameBoard.
No collision (the six heading rows of one number never share a Node),
no merge (one row per direction), no field, no other body. Every row
flies its digital line at the flight table's pace and leaves through a
face; the face's click carries the tick, the Node the row was on and the
face. The click record carries no age and no direction as the engine
stands: the age is the click's tick less the birth's tick (the lamp's own
`birth` line), and the direction is read off the click's momentum, the
unit vector of the direction at the scale Q = 64 (the engine's label
table, injective on the fan; `tools/click_readings/c_measured.py`).

The vector read after the detector, named before the run: the click's
Node **x**, an integer 3-vector in Links, with its face and its tick (a
scalar, the interval); from them the observable, the escape's pace
|**x**_k - **x**_0|_2 / tau in Links per interval, **x**_k the click's Node
plus the face's unit step (the Link crossed out).

## The expectation, written before the run

The closed form of the flight
([DERIVATIONS_BEAM section 11.1](../../../docs/DERIVATIONS_BEAM.md#111-the-linear-block-the-lattice-as-the-translation-group-the-shift-operator-and-the-flights-closed-form)):
a row born at **x**_0 on the direction D (S_1 = |a| + |b| + |c| its
Manhattan length, T_D = isqrt(3 |D|^2 Q^2) its resolution) is at the age
tau at **x**(tau) = **x**_0 + line_D[m_D(tau)] with

    m_D(tau) = floor((2 tau S_1 Q + T_D) / (2 T_D)),

line_D the Bresenham line of D (at each step the axis whose progress is
furthest behind, the lowest axis first; the engine's `flight.lines`), so
that its k-th Link falls at the age

    tau_k = ceil((2 k - 1) T_D / (2 S_1 Q)).

The escape of a row is its first Link k whose Node is off the GameBoard
(a coordinate below 0 or above 64): its click is at the tick 1 + tau_k
(the birth at tick 1, the age 0 there), on the Node after k - 1 Links
(the last on the GameBoard), on the face of the k-th step. Its pace is
|**x**_k - **x**_0|_2 / tau_k. `make_world.py` computes every direction's
row (`derived.csv`: the direction, its class, S_1, T_D, k, tau_k, the
tick, the Node, the face, |**d**|^2 and the pace) and the register
(`expectations.json`); the asymptotic pace of a direction is Q |D| / T_D
([FORM.md section 1](../../../docs/designs/light_speed/FORM.md), `light_speed_map.out`
A: 0.5774 to 0.5818 over the directions within 64 at Q = 64; recomputed
over this fan below, the same range, its extremes the body diagonal
0.57735 and the heading 64 / 110 = 0.581818).

| class | directions | k (Links) | tau_k (age) | tick | pace min / max / mean | asymptotic Q \|D\| / T_D |
| --- | --- | --- | --- | --- | --- | --- |
| the axes | 6 | 33 | 56 | 57 | 0.589286 / 0.589286 / 0.589286 | 0.581818 |
| the face diagonals | 12 | 65 | 79 | 80 | 0.581866 / 0.581866 / 0.581866 | 0.580190 |
| the body diagonals | 8 | 97 | 97 | 98 | 0.577412 / 0.577412 / 0.577412 | 0.577350 |
| the rest | 264 | 39 to 81 | 57 to 84 | 58 to 85 | 0.571767 / 0.588439 / 0.580901 | 0.577415 to 0.579386 |
| the fan | 290 | | 56 to 97 | 57 to 98 | 0.571767 / 0.589286 / 0.581018 | 0.577350 / 0.581818 / 0.578375 |

against c = 1 / sqrt 3 = 0.577350. The pinned totals: one birth at tick
1 (290 units, the multiplicity 290), 290 clicks on the faces and none
elsewhere, the last at tick 98, the escaped momentum (0, 0, 0) (the fan
is symmetric), one gather (the record form's one click of the record,
among its 290 offers), the books balanced at every tick.

Two properties of the grain, read off the derivation before the run and
to be confirmed by the clicks: (i) the finite escape's pace spreads wider
(0.5718 to 0.5893) than the flight's asymptotic range (0.5774 to 0.5818):
every row makes its first Link at its first interval (tau_1 = 1 on every
direction, since S_1 Q > T_D / 2) and tau_k is a ceiling, so a heading
makes 33 Links in 56 intervals (0.5893 above 64 / 110) and the slowest
direction (1, 5, 0) 40 Links in 59; (ii) the line's tie (the lowest axis
first) is not covariant under the permutation of the axes: (5, 1, 0)
leaves through the x face at its Link 39 (age 57, the pace 0.5884) while
(1, 5, 0) leaves through the y face at its Link 40 (age 59, 0.5718), and
the faces read 57, 47 and 41 clicks per pair (x, y, z) from a fan that
is symmetric under the 48 signed permutations.

**The refutation condition.** Any click whose tick differs from the
derived tick of its direction (or whose Node or face differs), or any
escape's pace outside the derived range 0.571767 to 0.589286; a click
count other than 290, a birth at another tick than 1, or the books off.

## What was measured (2026-09-21)

The run: `python -m event_universe --init examples/events/c_measured/c_measured.json
--output <folder>` (headless, no frames), 100 intervals, the runner's
0.39 s (the wall 0.96 s), the source fingerprint
`acf789fe08118a7aecf601e0a5f241351320ba5f2b4956056c194d37376e4b32`, the
package 0.3.1, `completed`, the books balanced at every tick; the reading
by `tools/click_readings/c_measured.py <folder>`, whose verdict is inside.

DETECTOR: one birth at tick 1 (290 units, the multiplicity 290); 290 clicks
on the faces (`face:+x` 57, `face:-x` 57, `face:+y` 47, `face:-y` 47,
`face:+z` 41, `face:-z` 41; the escaped amount and content 290, the
escaped momentum (0, 0, 0)), none elsewhere; 290 of 290 at the derived
tick, Node and face, none differing; one gather at the end.

| class | clicks | ages read | ages derived | pace read min / max / mean | pace derived min / max / mean |
| --- | --- | --- | --- | --- | --- |
| the axes | 6 of 6 | 56 | 56 | 0.589286 / 0.589286 / 0.589286 | 0.589286 / 0.589286 / 0.589286 |
| the face diagonals | 12 of 12 | 79 | 79 | 0.581866 / 0.581866 / 0.581866 | 0.581866 / 0.581866 / 0.581866 |
| the body diagonals | 8 of 8 | 97 | 97 | 0.577412 / 0.577412 / 0.577412 | 0.577412 / 0.577412 / 0.577412 |
| the rest | 264 of 264 | 57, 58, 59, 60, 63, 68, 69, 71, 84 | the same | 0.571767 / 0.588439 / 0.580901 | 0.571767 / 0.588439 / 0.580901 |
| the fan | 290 of 290 | 56 to 97 | the same | 0.571767 / 0.589286 / 0.581018 | 0.571767 / 0.589286 / 0.581018 |

Every reading inside its pin, nothing moved; the two properties of the
grain confirmed by the clicks (the faces' 57 / 47 / 41 per pair, the
pair (5, 1, 0) at age 57 and (1, 5, 0) at 59). The verdict in plain
words: the engine's flight is its closed form, bit-exact, on every one of
the 290 directions, and a detector on the faces reads the pace 0.5810 on
the mean over the fan at this GameBoard (0.5718 to 0.5893 by the grain of
the finite escape), 0.5784 (0.5774 to 0.5818) in the limit of the long
flight, against c = 1 / sqrt 3 = 0.5774: c is confirmed as the engine's
constant behind a detector. Not claimed: that nature's c is this; the run
establishes what the law does, not a physical law.

The three tests of the rule (record 202): no rule was touched. The flight
rule read against them, one line each: generic, one accumulator per row
with the declared integers S_1 Q and T_D and no family name; vector, the
translation of the accumulator by its rate with the Euclidean division
(T_D's root at load, none at run time); local, the row's own record and
the Link to one of its six neighbours, nothing kept at a Node.

What the engine could not record: the click record carries no age and no
direction; the age was taken as the click's tick less the lamp's `birth`
tick (both records of things in the world) and the direction off the
click's momentum label through the engine's own table.

## How to re-run

    PYTHONPATH=src python examples/events/c_measured/make_world.py
    PYTHONPATH=src python -m event_universe --init examples/events/c_measured/c_measured.json --output artifacts/c_measured/run
    PYTHONPATH=src python tools/click_readings/c_measured.py artifacts/c_measured/run
    PYTHONPATH=src python -m pytest tests/test_c_measured.py -q
