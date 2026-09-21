# The bending of light under the age word: what the rows' turn reaches, what the clock's word changes, and where the 2 is declared (the G2 experimenter, read-only, 2026-09-21)

Problem (1) of the seven (record 394 of the log of 2026-09-20, on the
Boss's branch at the time of writing; the Boss's order of about 14:42Z on
the model owner's word "give it to Far"): the bending and the delay of
light beside a mass under the clock's new word (the age moment, the
owner's decision of 14:01Z), with the owner's hypothesis relayed by the
Boss, "maybe the coupling is attached only to light and not to the clock".
The order: the three candidates of that hypothesis (the age word for the
rows only, for the clock only, for both), series K re-read by the map, the
deflection per Link summed against `4 G M / (b c^2)` and Newton's half,
the three tests, the GameBoard first, the pins before the numbers, one
verdict of three per candidate, and the owner's question ("conditional,
not derived: derive or enough?") answered for this problem. Read against
`main` at b7ddf93 (optical-v1 designed and reviewed, not built; form B not
on `main`; clock-age-v1 in build on the branch `clock-age-v1`, not on
`main`). Every number is from [light_bending_map.py](light_bending_map.py)
beside this note (the engine's own flight lines, `direction_flight`, the
one import; no run, no fit) and its output
[light_bending_map.out](light_bending_map.out); nothing here is
registered, built or decided. Notation: k the crowd's count at a Node in
units of the clock's pair, `k_s` under the presence word (`M / r^2` in the
shell mean), `k_a` under the age word (`M / r`), P and A the presence and
the age moment per unit of the pair, f the declared factor of optical-v1,
b the impact distance in Links.

## 0. The verdicts, stated at the top

| Candidate | What it is | Verdict |
| --- | --- | --- |
| (A) the age word for the rows only: optical-v1's verbs read A and the flow, the clock keeps the presence | light coupled to the potential's field, the clock to the `M / r^2` field | **REACHABLE IN FORM for light, NOT ADMISSIBLE as a whole** (section 4): the row turns by `2 f k_a(b)` toward the mass and is delayed as the logarithm, the FORM of the pins; but a clock beside it runs at `1 / (1 + k_s)`, the `M / r^2` form that nature's clocks refute at two heights (record 365, NATURE row 12 FAIL under the presence); two fields from one stream for two readers, no one metric; this is `main` today plus the build of optical-v1 without clock-age-v1 |
| (B) the age word for the clock only: the law as decided (record 394), the flight blind to the crowd | the clock reads the potential, nothing reads the crowd for a row's step | **NOT REACHED** (section 4): the row turns 0 and is not delayed; series K's registered 0.000 stands under the new word (its worlds declare `suspension` 0, so no clock there counts the crowd and the word cannot move a reading of K); the physicist's entry 2 ("light is neither bent nor delayed") stands as the law's prediction and the disagreement with nature stands |
| (C) the age word for both: clock-age-v1 and optical-v1 with the declared f | one field, A, read by the clock (`1 + k_a`) and by the rows (`n = 1 + f k_a`) | **REACHABLE IN FORM, the 2 declared** (sections 4 and 6): the row turns by `2 f k_a(b)` (`f = 2` Einstein's `4 G M / (b c^2)`, `f = 1` Newton's half), is delayed by `(f k_a(b) b / c) ln(4 r1 r2 / b^2)`, and the clock beside it runs at `1 / (1 + k_a)`: the time part of the metric is the clock's word and the space part is the second unit of f; the factor 2 over Newton is a declared integer of the world, not derived from the six verbs; the pins are the physicist's design's (section 4 there), unchanged by the clock's word |

The answer to the order's question in one sentence: the clock's word
decides nothing about light by itself (candidate B: the flight reads
nothing of the crowd, bending is not reached and K's 0.000 stands); the
bending needs the rows' own rule (optical-v1) and reaches nature's form
with one declared factor under either word for the clock; the age word
for the clock is what makes the two readers, the clock and the row, read
one field (candidate C), where the owner's hypothesis (A) leaves the clock
on a field nature's clocks refute. What the map adds beyond the design is
section 3: on series K's fan of 290 directions the Node-by-Node transverse
difference of A is the fan's grain, an order of magnitude above the
continuum's `2 f k_a(b)` in the sum and of the wrong sign at `b = 3`, so a
run of optical-v1 on K's mass as registered would read the grain and not
the pin; the pin world needs a crowd whose lines cover the beam's Nodes
(section 3, what the build must declare).

## 1. The pins, before any number

Nature's numbers (the map's section A):

| Pin | Nature | Source |
| --- | --- | --- |
| The deflection at the Sun's limb | `4 G M / (b c^2) = 4 k = 1.752` arcsec with `k = G M / (r c^2) = 2.123 x 10^-6`; Newton's (Soldner's) half `2 k = 0.876` arcsec | Dyson, Eddington and Davidson 1920: `1.98 +- 0.16` (Sobral), `1.61 +- 0.40` (Principe); VLBI `gamma = 0.99992 +- 0.00012` |
| The factor 2 over Newton | one unit from the time part of the weak isotropic metric (`g_00`, the clock's potential) and one from the space part (`g_rr`) | Cassini 2003 fixes it to `2 x 10^-5` (`gamma - 1 = (2.1 +- 2.3) x 10^-5`) |
| The delay | `(2 G M / c^3) (1 + gamma) ln(4 r1 r2 / b^2)`, about 250 microseconds Earth-Saturn at conjunction | Shapiro 1964; Cassini 2003 |

The model's pins (the physicist's design, [gr_rows/DESIGN.md](../../gr_rows/DESIGN.md)
section 4, on the pair `[1, 4096]` with series K's mass sixteen times the
registered): `k_a(b) = 0.0445` (`mass`, `b = 6`) and `0.0887` (`heavy`,
`b = 6`; `near`, `b = 3`); the deflection `2 f k_a(b) = 0.178` and
`0.355` rad at `f = 2`; the centroid's shift on the screen `-4.63` and
`-9.22` pixels; the count ratio of a clock at the beam's Node `0.9901` and
`0.9805`. A world without the key `optical` is byte identical in
`events.jsonl` and `state.json`. This note does not move a pin; it asks
what each candidate reads against them.

## 2. The GameBoard first: series K's mass on the lattice

The map's section B, from the engine's flight lines and nothing else:
series K's open box `57 x 41 x 41`, the mass at `(28, 20, 20)` releasing
one row per direction per interval (`M = 2^12`) or two (`2^13`) on the
fan of 290 primitive directions with `|a| + |b| + |c| <= 6`, the beam
along +x at `y = 20 + b`, `z = 20`, the lamp at `x = 2`, the screen at
`x = 54`. Each row's dwell ages along its digital line (about 2 per Link
of dwell at the flight's ages); the stationary presence P and age moment
A at a Node are the sums over the lines through it. Read on the beam's
line and its two neighbours in y, every fourth Node:

| World | b | On the beam's line at the mass's plane (`x = 28`): P, A | The shell mean at b (the README's estimate): P, A | The beam's nine Nodes at the plane, mean P, mean A |
| --- | --- | --- | --- | --- |
| `mass` (`2^12`) | 6 | 2, 21 | 1.10, 11.4 | 2.33, 22.7 |
| `heavy` (`2^13`) | 6 | 4, 42 | 2.20, 22.8 | 4.67, 45.3 |
| `near` (`2^12`) | 3 | 6, 29 | 4.40, 22.8 | 5.44, 26.3 |

The fan's grain: a Node on one of the 290 lines reads that line's rows;
a Node off every line reads 0 (on the beam's line at `b = 6` A is 0 at
`x = 14` and `42`, and on the neighbour `y + 1` at `x = 10, 22, 34, 46`);
the shell mean is the continuum's `M / r^2` and `M / r` (series E,
`k_s r^2 = 41.5`, `k_a r = 36.1`). The beam's own Node at the plane reads
about twice the shell mean in both P and A because it lies on a line of
the fan; the mean over the nine Nodes of the beam's cross-section is
twice the shell mean as well, at `b = 6`. The design's `k_a(b)` is the
shell mean; a rule at a Node reads the Node.

## 3. The deflection per Link, summed along the path, against the continuum

The design's verb 2 turns a row by the crowd's transverse flow **V** at
the row's own Node; the map reads the transverse difference of A across
the beam's line. In the continuum these are one reading: for the
stationary stream of a point source `grad A = -V` per unit dwell
([DERIVATIONS_BEAM 5.1](../../../DERIVATIONS_BEAM.md#51-the-two-fields-of-one-stream-and-the-equation-they-obey)),
so Fermat's law on the index `n = 1 + f k_a` gives the turn per Link
`d theta = f (n_s / d_s) (A(y + 1) - A(y - 1)) / 2` and the sum along the
path `2 f k_a(b)`. On the lattice both **V** and the difference of A are
the lines' (the map's section C):

| World | f | The lattice's sum over `x = 2..54`, per unit pair | The continuum `2 f A(b)`, per unit pair | At the pin pair `[1, 4096]`, the mass x 16: lattice / continuum (rad) | Links with a nonzero difference | The extremes per Link |
| --- | --- | --- | --- | --- | --- | --- |
| `mass`, b = 6 | 2 | `-663.0` | `48.1` | `-2.590` / `0.188` (the design's 0.178) | 49 of 53 | `+13` at `x = 15`, `-42` at `x = 4` |
| `mass`, b = 6 | 1 | `-331.5` | `24.1` | `-1.295` / `0.094` | 49 of 53 | |
| `heavy`, b = 6 | 2 | `-1326.0` | `96.3` | `-5.180` / `0.376` (the design's 0.355) | 49 of 53 | `+26` at `x = 15`, `-85` at `x = 4` |
| `near`, b = 3 | 2 | `+840.0` | `96.3` | `+3.281` / `0.376` | 47 of 53 | `+64` at `x = 10`, `-26` at `x = 18` |

The sign: A grows toward the mass (y decreasing), so a negative sum is a
turn toward the mass. What the table says, in three lines:

- **The form is reached and the sign is right where the shell mean is
  read.** The continuum column is the design's pin to the rounding of the
  shell mean (`0.188` against `0.178`: the map's `k_a(b)` is `36.1 / b`
  per unit pair, the design's is the register's `11.4 / 4096 x 16`).
- **The lattice's sum is the grain, not the pin.** On K's fan the beam's
  line crosses the fan's lines at a few Nodes, where the transverse
  difference is tens per Link, and reads small or 0 between them; the sum
  is fourteen times the continuum at `b = 6` and of the wrong sign at
  `b = 3` (the beam's line at `y = 23` lies just above a dense set of the
  fan's lines through `y - 1`, and above them A falls to 0). A run of
  optical-v1 on series K's mass as registered would read this, whole
  steps of `THETA_G` per Link (the design's dither over records, section
  4 there), and not `2 f k_a(b)`.
- **What the pin world must declare.** The design's pins assume the shell
  mean at every Node of the beam's line and its neighbours. That holds
  when the crowd's lines cover them: a fan bound larger than 6 (the count
  of primitive directions grows as the bound cubed; 290 at bound 6, 2,114
  at 12, 9,506 at 20) or a mass extended over many Nodes (a crowd
  of sources, series V's form) whose lines fill the beam's Nodes, at a
  release the pair `[1, 4096]` still reads. This is a declaration of the
  pin world, not of the rule, and it is the build's; the register's K
  worlds are not that world.

The map's lattice sum is a host reading of the stationary fields, not the
engine's turn (which needs the wheel, the records and the dither); it says
what the engine would read, not what it would register.

## 4. The three candidates of the owner's hypothesis

The map's section D, at the beam's Node on the mass's plane in `mass`
(`b = 6`): per unit pair `k_s = 2.000`, `k_a = 21.000` (the shell mean's
`k_a(b) = 12.03`); at the pin pair `[1, 4096]` with the mass x 16,
`k_s = 0.0078`, `k_a = 0.0820` (shell mean `0.0470`).

**(A) The age word for the rows only** (optical-v1 built, the clock on the
presence as `main` has it today). The row turns by `2 f k_a(b) = 0.188`
rad at `f = 2` toward the mass and is delayed as the potential's
logarithm: the FORM of the two pins for light. A clock at the same Node
runs at `1 / (1 + k_s) = 0.9922`, the `M / r^2` form; nature's clocks at
two heights (GPS, Galileo's eccentric pair, Pound and Rebka) follow the
potential and refute that form (record 365; NATURE row 12 FAIL under the
presence word, 1.000 against 2.00). One stream, two fields, two readers
that disagree on which they read; there is no metric whose time part is
`M / r^2` and whose space part is `M / r`. Verdict: reachable in form for
light, not admissible as the law's whole. The owner's hypothesis, read
literally, is this candidate; what it saves (the clock unchanged) is what
nature refutes.

**(B) The age word for the clock only** (the law as decided, record 394;
no rule of the rows reads the crowd). The row turns 0 and is not delayed;
series K's registered `0.000` pixel stands (K's worlds declare
`suspension` 0: no clock in them counts the crowd, so the clock's word
moves nothing in K; the map re-reads K's fields P and A, section 2, and
finds no reading of K to move). The clock runs at `1 / (1 + k_a) =
0.9551`, the potential's form (NATURE row 12 PASS under the age word,
1.907 against 2.00). Verdict: the bending of light is not reached; the
physicist's entry 2 stands as the law's own prediction and the plain
disagreement with nature stands. The clock's word is not a rule for
light.

**(C) The age word for both** (clock-age-v1 as decided and optical-v1
with the declared f). One field A: the clock's `1 + k_a` and the rows'
`n = 1 + f k_a`. The row turns by `2 f k_a(b)` (`0.188` rad at `f = 2`,
`0.094` at `f = 1`, Newton's) and is delayed by
`(f k_a(b) b / c) ln(4 r1 r2 / b^2)`; the clock beside it runs at
`1 / (1 + k_a) = 0.9551`. The weak isotropic metric's two parts are read
by two readers of one field: the time part is the clock's word, the
space part is the second unit of f. Verdict: reachable in form, with the
2 declared. This is the design as reviewed (ADMISSIBLE WITH MUST-FIXES,
the eight closed in round 2, BUILDABLE after form B lands) under the
clock's new word; the clock's word changes no pin of the design (the
design's count ratios `0.9901` and `0.9805` are already the age word's,
its section 4 reading the age moment for the clock at the pair).

## 5. The three tests, one line each, for the candidate that adds a rule

Candidate (B) adds nothing to the rows and passes as clock-age-v1 passed
([the clock's word note](../../clock_age/NOTE.md), section 3). Candidates
(A) and (C) add optical-v1 to the rows; the tests are the design's and
the reviewer's, restated:

- **Generic:** two moments of the one reading set (the age moment A, a
  sum of amount x age; the flow **V**, a sum of amount x unit vector at
  the scale Q), the factor f a declared integer of the world, no family
  name, no branch on a kind (the emitter's number compared as
  `crowd_flow` compares it). Pass.
- **Vector:** verb 1 adds `f n_s A` to the wall (linear in the state,
  the rate `by_drive`); verb 2 turns the direction by the transverse
  component of **V** in whole steps of `THETA_G` (bilinear, the wheel's
  dither, no root, no float). Pass, as reviewed.
- **Local:** both read the rows present at the row's own Node this
  interval, nothing kept at the Node, fixed work per row for fixed K
  (five of the moment table's thirteen columns, recomputed by the host's
  segmented pass). Pass.

What the tests do not decide: the factor 2 (a declared integer passes
the generic test as a world input and is not derived, section 6), and
the grain of section 3 (the tests admit the rule; the pin world decides
what it reads).

## 6. The owner's question on the conditional derivations, for this problem

The owner asked (14:03Z to 14:46Z through the Visualiser and this
session): the wave limit and Lorentz, the field equation beyond the
static case, `1 / r^2` are "conditional, not derived: derive them, or is
this enough?" For the bending of light, the map's section E sorts what
is which:

**Derived on the GameBoard from the rows** (no assumption beyond the six
verbs and the fan):

- the presence falls as `M / r^2` and the age moment as `M / r` from the
  same stationary stream (series E, the fan's dilution as the shell;
  `k_s r^2 = 41.5`, `k_a r = 36.1`);
- the push is minus the gradient of A and the clock runs at
  `1 / (1 + k_a)` at first order (5.1, 5.2);
- A obeys the retarded scalar wave equation of its stream, so the field
  equation beyond the static case IS derived for this field: a moving
  or changing mass changes A at the rows' pace, not at once (5.1);
- the FORM of the bending, `M / b`, and its sign toward the mass, from
  any turn that reads a transverse gradient of A or the flow (the
  meeting's grain, optical-v1's index); the delay's logarithm from any
  pace that reads A along the path (verb 1).

**Conditional** (a declaration, not a derivation):

- **the factor 2 of Einstein over Newton.** optical-v1 declares it as f.
  A derivation would need the space part of the metric from the verbs: a
  row's Link that shortens beside a mass, or a pace that falls twice as
  fast for a row as a clock does for a body. No verb of the six gives it:
  the flight table is one pace for every row and the Links are the
  lattice's. The one unit that IS derived is the clock's (the time part,
  `1 + k_a`); light follows the time part alone at `f = 1`, Newton's
  half, and needs the declaration for the second. This is the honest
  state: `f = 2` is read from Eddington and Cassini into the world file,
  as S (the push's width) and the clock's pair are read from nature.
- **the identification `k_a = G M / (r c^2)`.** The suspension pair sets
  the scale on the GameBoard; nature fixes it by one clock (NATURE row 12
  is the form, not the scale; the scale is one number read in).
- **Einstein's equation.** A's equation is the linear retarded scalar
  wave equation of a stream; it is not Einstein's nonlinear tensor
  equation (5.5). What is derived is the weak static limit's two pieces,
  one from the clock and one declared; the perihelion's `3 G M / (a c^2)`
  per orbit, the nonlinear term, is neither derived nor declared here
  (the second-order term of the design's section 5 is on the clock, not
  on the orbit).

Enough, or derive? For the bending: the form and the sign are derived and
the run would read them; the 2 is a declaration and stays one under every
candidate, and I know no route within the six verbs to it. If the owner
wants it derived, the question is a new one, "what shortens a row's Link
beside a mass", and it needs its own design, not this note.

## 7. Proposed lines for the documents I do not write

- **The register, series K:** no reading moves under the age word (the
  worlds declare `suspension` 0); one line under the verdict: "re-read by
  the light-bending map of 2026-09-21: the beam's Node at the mass's
  plane lies on a line of the fan and reads twice the shell mean (P 2, A
  21 against 1.10, 11.4); the fan's grain, section 3 of the note".
- **gr_rows/DESIGN.md, section 4 (a should-fix for the build, through the
  Boss):** the pin world's crowd must cover the beam's Nodes, or the
  registered K mass x 16 reads the grain (`-2.59` rad summed against the
  pin's `0.178`, of the wrong sign at `b = 3`); a fan bound above 6 or an
  extended mass, declared before the run.
- **NATURE:** no row today for the bending or the delay; a row can be
  added only when a detector reading exists (the build's), with nature's
  `1.752` arcsec, Cassini's `gamma`, and the model's `2 f k_a(b)` at the
  declared f; until then the disagreement is the physicist's entry 2 in
  Highlights 5.4.
- **The clock's word note, section 1** (the mathematician's): "the age
  moment is already the field of the rows' rule" is candidate (C) of this
  note; one link.

## 8. Questions, through the Boss

1. The owner's hypothesis as relayed reads as candidate (A). Is it (A)
   (the clock stays on the presence, which record 394 has already
   replaced), or is it the question whether the rows need f at all under
   the age word (candidate B against C)? This note answers both; the
   owner's word decides which is asked.
2. For the build of optical-v1 (after form B, the owner's go of record
   303): does the pin world get a wider fan or an extended mass (section
   3)? The design's numbers hold for the shell mean and the register's
   K mass does not give it at a Node.
3. Is the factor 2 to stay a world input (as S and the pair), or is
   "what shortens a row's Link beside a mass" a problem to add to the
   seven?

## 9. Links

[Series K](../../../EXPERIMENTS.md#k-light-beside-a-mass-2026-09-20) and
[its README](../../../../examples/events/lensing/README.md#the-derivation-before-the-runs);
[optical-v1](../../gr_rows/DESIGN.md), [its review](../../gr_rows/REVIEW.md)
and [round 2](../../gr_rows/REVIEW_ROUND2.md);
[the clock's word](../../clock_age/NOTE.md);
[DERIVATIONS_BEAM section 5](../../../DERIVATIONS_BEAM.md#5-general-relativity-the-equation-of-the-delay-field);
[BEAM_LAW section 3](../../../BEAM_LAW.md#3-the-nodes-interval-nature_beam)
(step 5, note 25); [NATURE](../../../NATURE.md) row 12;
[the three tests](../../../../skills/workflow.md#the-three-tests-of-every-rule-generic-vector-local-the-model-owner-2026-09-21-record-202);
[problem (2), special relativity from the six verbs](../lorentz/NOTE.md).
