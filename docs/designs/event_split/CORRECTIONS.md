# The mistakes and the solutions, the verification plan and the table's convergence under the corrected law (the chief physicist, 2026-09-23; docs only)

The model owner's order of 2026-09-23 (05:1xZ, by voice, through the
Boss, his rendering): "Now we need to reach an understanding of what the
mistakes were and what the solutions are, and the physicist makes sure
the solutions work; and then the laws should work for us: from the table
you made we should see that they begin to converge, and what is supposed
to pass will pass; because what we say passes must pass with the new
detectors, with the new readings: that now a moving detector reads; how
a detector measures a clock; that there is no external clock; it is a
detector, it has its own clock. All these things must enter, and the
physicist checks them." The Boss's order on it (05:15Z): one writer, the
chief physicist, alone; (1) every place the law as built departs from
what the owner has said is the law, with the code lines and each
solution's three tests; (2) how each solution is verified before any row
is read; (3) for every row of the rules page and of NATURE.md what the
corrected law with the new detectors and readings should make of it,
declared before any run; (4) the algebra under the split; (5) the host
cost and the dangers. (4) and (5) are [DESIGN.md](DESIGN.md) sections 1,
9 and 10 beside this file; this file is (1), (2) and (3). Every run is
held until (2) is done and the owner has read (1) and (3).

The ground this file is written on (the Boss's list of 04:58Z, the state
at head, closed as clicks, one mechanism): a detector is a measured
event, a body with a record (`measured.py` 154); a moving detector is the
same measured event with a drive (`engine.py` 122 to 154), carrying its
record, its held content and its Nodes; its clock is its own count of
self-creations under the age wall (`engine.py` 699 to 706; the crowd
slows the count, not the click's tick; r_D = d / (d + A n)), stamped on
its lines under `clock_stamp`; a measurement is the law's action, a
click: the record ends at the detector and the detector's own record
changes (record 1139; the deposit at `nature_beam.py` 5498); an emitter
is a detector at its Node (record 570); every external thing is a
measured event declared in the world file with its table and directions
(record 562: `measure`, `read`, `pass`, `rerelease` as a fan or a
re-emitter with its weights, a rotation, a window, a gate; the `sum`,
`wave` and `beam` sets), never something the GameBoard has by itself;
there is no mirror on the GameBoard, the far end of the light clock is a
receiver body under `rerelease` (record 1234); a click reads what
arrives with the record as it is; two co-moving bodies that exchange a
packet both measure; an open face has no clock, a one-Node wave pixel is
a body and has one; the detector's count is a member of the age wall's
set (record 812). Where a solution below needs a mechanism not in this
list, it is named as an item for the owner, not assumed. Every number
is labelled COMPUTATION, DETECTOR, GAMEBOARD or HOST; no run was made
for this file. Code lines are those of `src/event_universe/events/` at
origin/main d2982954.

## 1. THE MISTAKES AND THE SOLUTIONS

Each item: what the owner said is the law; what the code does; the
solution; the three tests (generic, vector, local) of the solution.

### M1. The ray does not split at every Node

The owner (records 1262, 1267): an event always splits unless it is a
quantum; the GameBoard is all the futures; the ray's not splitting is a
bug in the law as built. The code: a recorded row walks the digital line
of its direction (`_walk`, `nature_beam.py` 3966) and splits only where
an apparatus declares it, a lamp's fan at the birth and a `rerelease`
entry's directions (5413 to 5427, `PendingRow(..., split=True)`); at a
free Node it does not split. The solution: the split as the Node's rule
for every recorded row of no content, [DESIGN.md](DESIGN.md) sections 3
and 5 (the record form, the weights and the pace the owner's open
choices), default ON, no key. The three tests: DESIGN.md section 6,
build (ii): generic PASS, vector PASS, local PASS.

### M2. The record completes on the GameBoard, and the click is triggered by that completion

The owner (record 1263): no completion on the board; the record ends only
at a quantum's click; what ends is only the click. The code: the layer
holds a live count per record (`amplitude.Layer`, host state; amplitude-v1
section 3.2), decremented by every row's end (a set, a face, the border)
and incremented by every split, and the record is gathered and clicks
when the count reaches 0 (`nature_beam.gather_records`; the docstring
"the record completes when all rows ended"). Under the split the count
never reaches 0 by the walls alone, so the completion rule is the second
half of the same bug. The solution is the click's trigger, bounded by the
owner's word (record 1276 by the Boss's word of 05:14Z; his two options,
no third unless the code forces one), with what the code forces stated
first:

**What the code forces.** The ladder (`rungs`, `cell_of`) reads the
record's cells as ratios of the offers accumulated per set; the cells
give Born only over the record's whole front, because paths of one
record of different lengths reach a set at different intervals and the
square of the set's accumulated pointer rises and falls with each
arrival (amplitude-v1 section 13, departure 3; DESIGN.md section 4,
"Where the trigger comes from"). A trigger that reads the ladder while
counted futures are still in flight truncates the front. The grain
(record 1263, the owner's bookkeeping: a branch below one unit no longer
counted) is what makes the counted futures of one quantum finite; it is
not the trigger.

**Option S, the detector's sensitivity** (the owner: "the detector has a
kind of sensitivity"; record 04 of 2026-09-19: "a detector measuring
three Nodes sees one electron that can be on any of the three"). Each
detector declares a sensitivity s_D, a fraction of the quantum in units
of the wheel (the code's `threshold` today is a count of units of amount
summed over the set per interval, no memory between intervals,
`nature_beam.py` 4551 to 4558; under the record form the quantity that
reaches a set is its accumulated offer over the multiplicity, so the
sensitivity is on the share, not the amount: a change of what the
threshold compares). Two readings of S: (S1) as a first crossing, the
record clicks at the first interval a set's accumulated offer reaches
s_D, the ladder on the offers accumulated so far: the code forbids it
for the reason above (the pins: the two slits' fringe and the single
opening's spread truncated to the paths that arrived first, the spread
narrower than the Fourier width, a Heisenberg break; the pair world's
gather lost when one arm's set crosses first); (S2) as the counting
rule, a set whose accumulated offer is below s_D takes no rung (the
empty rung of `rungs`), a branch whose share is below s_D at any Node is
no longer counted (the grain, declared per detector rather than fixed at
1 / W), and the record clicks when no counted future is in flight; with
s_D = 1 / W for every detector this is the grain of DESIGN.md section 4
exactly. Three tests of S2: generic PASS (one declared integer per
detector, an input of kind 3, no family name; a sensitivity per family,
which row 8b would need, is an input of kind 2 and a design item for the
owner); vector PASS (a comparison, verb (D), of the set's accumulated
square over the multiplicity against s_D times the birth norm); local
PASS for the detector's comparison on its own record and for the grain
on the row's own; the exhaustion ("no counted future in flight")
decides WHEN the law acts on the whole record and is non-local, as the
completion it replaces and as the deletion at the click: it passes only
as the click's own non-local step, the one the law already has (ALGEBRA
3.1; the owner's "what ends is only the click"; Reviewer 3's A2). One
sentence for the owner: the sensitivity read as a first crossing is the
local trigger, and it is the one the ladder forbids (S1), so the click's
timing stays the record's. Pins: the pair world's cells 27, 5, 5, 27 and S = 2.75, Malus
1 / 2, the single opening inside its band (DESIGN.md section 7), each
conditional on s_D below the smallest offer that carries a cell (the
faces' 0.011 share in row 10's first record, COMPUTATION, `run_10_pins.out`
section 4).

**Option Q, the single-quantum reading** (the owner: "or it reads a
single quantum"). A detector clicks when one whole quantum's share is at
its set. Read literally, a set that receives the whole quantum exists
only where every counted future ends at one detector set (a screen
declared as one detector of many Nodes, the cell within the set chosen
by `node_choice`; not the two slits' 121 one-Node pixels, and never
where faces or walls take part of the front); read as the law can build
it, "the whole quantum is at the detectors" is the exhaustion of the
counted futures, the same condition as S2 with s_D = 1 / W and the
detectors the only sets. Three tests: as S2. Pins: as S2 where the
world's sets take the whole front; a world with open faces (row 10's
worlds, 0.011 of the front on the faces) needs the faces to be sets
that offer, else Q never fires there.

**Decided.** The chief physicist's recommendation was S2 with s_D = 1 / W
by default (the wheel's own grain) and declarable per detector: the
grain the owner accepted as bookkeeping, Born over the whole front, the
click mechanism and the ladder unchanged, Q its special case. The
owner's word of 05:55Z to the Boss (record 1288, Hebrew, by voice, the
Boss's rendering: "I think that all the experiments must be re-run with
the new engine after the fix. As the physicist's recommendations."),
after his word to the chief physicist of about 05:52Z ("I agree with you
on everything"), makes it his decision: the trigger is S2; S1 is what the code forbids and
stays listed so that its pins are on record. Two more of his decisions
by the same word: a sensitivity per (detector, family) is a declared
input of kind 2 (the cross-section; row 8b's condition in section 3);
and the crowd's flow turning a row of no content (row 13's second half)
is the second half of the bending, whose form the pins of M9 decide
before the build (his word of 06:12Z: add it, see how everything
behaves, go back if it does not).

### M3. Readings by the host's tick where the law has no external clock

The owner: there is no external clock; a detector has its own clock; a
moving detector reads as a resting one does; how a detector measures a
clock. The code: the detector's own count exists (`engine.py` 699 to 706,
the count of self-creations under the age wall, r_D = d / (d + A n)) and
is stamped on the record only under `clock_stamp`, declared by 20 worlds
at head (the Outside audit, `docs/designs/outside_audit/AUDIT.md`
section 1); the registered series declare it nowhere, so their tools
read times off the host's tick. The audit's sixteen changes, sorted:

- **Mistakes of the law's reading** (a DETECTOR number formed on the
  host's tick where the detector's own count is the only clock; PIN in
  kind): item 2 (G2 and G: z, the luminosity and t_0 against the host's
  tick; rows 3 and 4b), item 3 (S: the muon's lifetime in ticks, the
  electron's arrival at a tick; row 4a), item 4 (T and X: 1 + z as the
  ordinal against the host's tick; X's k(2) / k(4) move by the
  detector's own dwell in the shell), item 6 (D3 and the k17 pair: the
  period as a fraction of a tick; row 14), item 7 (the atom's levels R1
  and R3 on the host's tick; row 6), item 8 (J: the W's trigger and the
  far detector's expectation in ticks; rows 8a and 8b), and item 5 (Q: c
  measured as a face click at a tick; row 5a: the registered pace stays a
  COMPUTATION of the flight table, and the DETECTOR reading is the light
  clock world of records 1226 and 1227, a receiver body under
  `rerelease`, the return read as the detector's own count).
- **A gap of the record, not a wrong number**: item 1 (the stamp absent
  from the registered worlds; the re-run byte-identical in physics, the
  count added to the lines).
- **Labels of a tool or a test, no number of the law moved**: items 9
  (N, P, I, R: the books and host ticks out of the reading tables), 10
  (K: the phase rate per the lamp's ordinal), 11 (the drive's tools), 12
  (C: the fourteen board checks to diagnostics), 13 (the amplitude
  register's tick pins), 14 (Bell's crowd forms' tick offsets), 15 (one
  label each: the build-up, Heisenberg, the massive rows, the new rows,
  the crowd clocks, rows 8b and 8c), 16 (the rule tests that write into
  a running board: a sentence).

The solution: the mistakes of the reading re-read on the detector's own
count (the audit's items as written, the tools' lines named there), the
stamp declared by every registered world (item 1), the labels applied.
Three tests: generic PASS (one count per detector, the age wall's member,
for every family alike); vector PASS (the count is (T) and (D) on the
detector's accumulator, already the law's); local PASS (the detector
reads its own count; the tools read the record). No physical rule
changes; what changes is which number is called DETECTOR.

### M4. A mirror on the GameBoard

The owner (record 1234): no mirror on the board; a mirror from outside
enters and does something; the far end of the light clock is a receiver
body under `rerelease`. The code: there is no mirror object; a
`rerelease` entry with one output on every arrival is what the code's
comments call "a mirror" (`engine.py` 975: "what a mirror does", the
momentum returned; `measured.py` 84: "while units wait at a mirror";
`world.py` 2291: "a mirror, an opening's fan"), and the Mach-Zehnder's
mirrors are such entries. The mechanism is the owner's (a receiver body
that re-emits); the word is the mistake. The solution: the three comments
and the register's READMEs say "a receiver body under `rerelease`"; no
engine line, no number. Three tests: not applicable (a name).

### M5. The meeting: the paid unit's reading of the free crowd, and the two parts named against the code

The owner (record 1272): it enters generically as the default. The code:
it is the default since 2026-09-22 in the momentum form (`optical_turn`,
`nature_beam.py` 3733 to 3770, verbs 2 and 3 of the generic entry) on
every row of every family in free space, no key; meeting-v1 under the
key `meeting` is the earlier phase-register form, off by default, the
five lensing worlds' history. Not a mistake of the code; a mistake of
the law's text, corrected in BEAM_LAW note 35 (branch
`beam-law-note-35`, 15db1a62, merged), whose sentence then named the
parts wrongly and is corrected again on the branch `beam-law-note-35-fix`
(this pass; Reviewer 2's and Reviewer 3's reading of the code). **What
the turn and the wall each carry, against the code, on a light row of
the registered worlds** (the `light` family, quantum 1, content 1 per
unit): the wall of the row's flight is 2 T_D (d + f n A) with f = 1 +
gamma and A the crowd's age moment at the Node (`age_wall`,
`core/integer.py` 118; `optical_rate_and_wall`), the delay; the turn
translates the row's momentum accumulator **W** by the flow **V** at the
rate n x weight with the weight (1 + gamma) content x e_D per unit
(`unit_weights`, `nature_beam.py` 3564: (E'_D^2 + 3 gamma p_D . p_D) //
E'_D, e_D = isqrt(3 u_D . u_D) for the photon), the deflection. At gamma
= 0 the turn gives the time part's deflection (Newton's half: the optical
pin worlds' -1.93 pixels at M = 2^16, b = 6, the pair [1, 16384],
DETECTOR; -1.993 on Reviewer 2's re-run of mass_g0) and the wall the time
part's delay (2.68 intervals); at gamma = 1 each is doubled (-3.86,
5.36). So "the time part in the flight wall, the space part the turn
along the momentum's line" (note 35 at 15db1a62, the meeting line of
record 1272, the first form of this item and of row 13's reason) was
wrong as a naming: the turn is the deflection's mechanism and the wall
the delay's, each at 1 + gamma; the time part is the 1 of both and the
space part the gamma of both, absent at gamma 0. My earlier sentence
"the space part's weight content x w is 0 on light" was wrong too:
light's content per unit is 1 and the turn acts on it; a row of content
0 (a free family, `nu` at head) is the only row the turn never moves.
Series K's 0.000 (row 13's "the law as built") is a world at
`suspension` 0, where n = 0 and neither the wall nor the turn has a
rate, a declaration of that world. What M9 asks is then not a weight
but the wave's own tilt under the split, against the turn.

### M6. Amplitudes added on the GameBoard: decided, the code's merge is the law

The owner's word of 04:29Z (record 1262): "amplitudes are never added on
the board; two possibilities meeting in a Node keep their own phases;
interference exists only in the click's sum", which the chief physicist
confirmed to him then; the code: `_merge_rows` (`nature_beam.py` 1473;
the identity fields 1610) sums the amounts of rows identical in every
identity field with the phase read modulo N / 2 and cancels an antipodal
pair, a row of another phase untouched. The Boss put the two to him, and
his word of 05:24Z (record 1282) decides it: "I think the logic, in
order to keep all the laws, is that the amplitudes add at the Node,
right? What comes from the six neighbours, they add, and the event
propagates." So the merge (verb (G)) at the Node is the law and the
mistake was the chief physicist's sentence, not the code: the one form
is the sum at the Node, the split at the next Node, the pattern read at
the click from the summed amplitude. Three tests: (G) on the row's own
Node, generic, vector and local PASS as it is.

### M7. The openings' declared fans, redundant under the split

The world files of rows 2a and 10 (`amplitude/slits_huygens.json`;
`docs/designs/fail_rows/opening_w27.json`, `opening_w9.json`) give the
openings' Nodes a `rerelease` entry with a fan of 91 or 601 directions:
the apparatus's split standing in for the board's. Under the split the
opening's Nodes are free Nodes and the wall's Nodes measure; a declared
fan there would split the arriving row twice. The solution: the entries
removed from those worlds at the re-registration (a wall with a gap, no
entry on the gap); a lamp's fan stays (the owner: "a ray splits
according to the laws it has"; an emitter is an apparatus). Three tests:
the world file's, none of the law.

### M9. The second half of the bending: what the law as built has, what the split adds, and the one question the pins must answer before the build (corrected 06:40Z)

**The premise of this item's first form was wrong, and is corrected
here.** The registered light is the paid family `light` (`quantum` 1,
`examples/events/entities/families.json`), so it has content per unit
and the crowd's push (verb 2 of `optical_turn`) DOES act on it, at the
unit weight e_D = isqrt(3 u_D . u_D) at gamma = 0 (Newton's half) and
2 e_D at gamma = 1 (`unit_weights`, `nature_beam.py` 3564): the pin
worlds `examples/events/optical/` read the shift -1.93 pixels at gamma =
0 and -3.86 at gamma = 1 (DETECTOR, M = 2^16, b = 6, the pair [1,
16384]) and the delays 2.68 and 5.36 intervals. Series K's 0.000 (row
13's "the law as built") is a world with `suspension` 0, where n = 0
and neither the wall nor the push has a rate: a declaration of that
world, not the law's default. A family of content 0 (`nu` at head, a
crowd family `m`) is the only row the push never turns; the
energy-weight form of this item's first version (the equivalent content
M_eq = 3 h n / (Q S_w d) at load) applies to those alone and is kept as
a note for the massive form, not as this build's rule.

**What the split adds, and the question.** Under the split the wave's
own front tilts by the gradient of the wall's delay across the impact
parameter (Fermat's rule on the Huygens sum), which a ray on a digital
line cannot do. The derivation mathematician's check of 2026-09-21
(`docs/designs/one_wall/one_wall_check.py`, identity 2, no run): the
front's tilt is the derivative of the Shapiro delay across b and equals
the push's turn, 2 G M / (b c^2), Newton's half; "the wall's tilt and
the push's turn are one deflection read in two languages, never a sum".
So under the split, with the wall and the push both acting on a row of
light, the click's centroid would move by the tilt AND the push, two
times Newton's half at gamma = 0: numerically nature's 2, but by the same
potential counted twice through its two moments (A the age moment on the
wall, V the flow on the momentum), while the delay stays the wall's
alone, 1 of nature's 2 (Shapiro's (1 + gamma)). The three numbers the
pins script must produce on the pin world, on the lattice's own lines
and not by the continuum's identities, before any build: (i) the front's
tilt under the split from the wall alone (the phase-front's gradient
across the beam at the screen, COMPUTATION), (ii) the push's turn on the
same rows (the pin's -1.93), (iii) the delay; and whether (i) equals
(ii) on the lattice as the identity says.

**The forms the owner then chooses between, stated now so the pins are
read against them** (his word of 06:12Z: "add the second half and see
how everything behaves; go back if it does not"):
- Form W (the wall's language): a row that splits is not pushed by verb
  2 (its momentum turns only through the wave's own tilt), the wall
  carries the coefficient f = 1 + gamma for every row, and gamma = 1 is
  the law's default declaration (an input of kind 2, as today's `optical`
  gamma, its default moved from 0 to 1 on the owner's word): the
  deflection 2 (the time part 1 and the space part 1, both by the tilt)
  and the delay 2, both as nature reads them; row 13 "an input read
  back" as it is at gamma = 1 today, its number the split's own.
- Form P (both languages): the wall at f = 1 and the push at e_D both
  act on a splitting row, gamma = 0: the deflection 2 by the double
  count, the delay 1; a reading that disagrees with Shapiro's (1 +
  gamma) = 2 (Cassini, gamma to 2 x 10^-5), so this form is refuted by
  the delay unless the pins show (i) and (ii) are not equal on the
  lattice.
- A body (the quantum that does not split) keeps the push, Newton's, in
  either form; the massive form decides its wave.

The chief physicist's recommendation stands only after the pins:
if (i) = (ii) on the lattice, Form W (the second half as the wall's
gamma = 1 by default, the push off for a splitting row), and row 13
stays an input read back with the split's own number; the hope that
gamma is derived by the split is then not met, and this file says so.
Three tests of Form W: generic PASS (one coefficient on the one wall,
every family alike; the push's exemption a property of a row that
splits, not of a name); vector PASS ((T) and (D) on the flight
accumulator as today); local PASS (the age moment at the row's Node).
What Form W can move: every world with a crowd and a suspension pair
(the optical pin worlds, G2's Hubble light, the clock-word and shell
worlds); the crowd-free worlds bit-identical.


**The owner's sentence of 06:22Z (record 1297), stated as ordered, and
read against the code.** His words (the Boss's rendering): "the generic
weight is the row's energy in content units, the same for every family;
for a body it is the content as today, for light it is M_eq = 3 h n /
(Q S_w d) per unit from its phase rate, a rational number made at load,
no root and no division at run time; E = h f becomes one sentence for
both." Against the code: the push's weight per unit today is (1 + gamma)
content x e_D (`unit_weights`, `nature_beam.py` 3564 to 3582, the
weight (E'_D^2 + 3 gamma p_D . p_D) // E'_D; `optical_turn` 3733 to
3770), with E'_D the family's energy per unit on its own labels
(`unit_energies`: e_D = isqrt(3 u_D . u_D) for a family without the flag
`massive`, E'_0 = Q S_w M for a massive one, S_w the world's `width`, 1 by
default): the photon's energy in the code is read off its MOMENTUM
label, |p| = Q |u_D| at the label's scale, e_D = isqrt(3 Q^2) = 110 or
111 by direction (COMPUTATION), and the wall's stretch reads the age
moment alone, no weight. The owner's sentence reads the photon's energy
off its FREQUENCY through the load-time identity 3 h n = Q S_w d
(ALGEBRA 5.3): E'_eq = Q S_w M_eq = 3 h n / d. The numbers for the
registered light (the family `light`, quantum h = 1, phase rate n / d =
8591334592 / 1073741824 = 8.0013 steps per interval; the same family in
row 13's pin worlds, the two slits and Malus): E'_eq = 3 x 1 x 8.0013 =
24.004 against the code's e_D = 111, the ratio 4.62; M_eq = 24.004 / (Q
S_w) = 0.375 content units per unit of light at S_w = 1 (COMPUTATION;
S_w cancels in the ratio). So the sentence CHANGES light's push weight,
from the label's 111 to the clock's 24: what it says, plainly, is that
in the registered light E = p c does not hold (the momentum label at the
flight's grain Q against the clock's h f differ by 4.62; ALGEBRA 5.3's
"the content and the phase rate untied on main"), and that the push
reads the energy by the clock, not by the label. The three tests of the
sentence: generic PASS (one primitive, the family's h and n / d from the
table, the same for every family, no name); vector PASS (a rational pair
formed at load, a declared rounding at load if reduced, the same verb
(T) on **W** at run time, no root, no float); local PASS (nothing kept
at a Node; the crowd's flow at the row's Node as today). What it moves
(COMPUTATION, the push linear in the weight at small angles): row 13's
pin worlds' shifts -1.93 and -3.86 pixels to -0.42 and -0.84 (divided by
4.62), the delays 2.68 and 5.36 unchanged (the wall takes no weight);
light as a SOURCE of the push on others is unchanged (the crowd's
moments are amounts, ages and labels, not energies); nothing else in
the register has a crowd on light. The one-wall identity is untouched
by the weight in its form; in its number the push's constant drops by
4.62 against the wall's, so on the pin worlds (the pair [1, 16384], the
release [1, 4096], k_wall / k_push = 1 / 4 in the code, `one_wall_check.out`
section 3) the two constants come within 15 percent of each other
(4.62 / 4 = 1.15) under the sentence: a COMPUTATION worth the owner's
eye, not a derivation. My view for him, one sentence: the sentence is
right in principle (E = h f for light and E = m c^2 for a body as one
weight) and passes the three tests, and its cost is a moved pin (row
13's -1.93 to -0.42 at gamma 0) and the plain statement that the
registered photon's label momentum and clock energy disagree by 4.62,
which the design of the lamp's label (kind 1) must then reconcile.

**Both ties, for the owner's choice after the pilot (the Boss's order of
07:17Z, record 1313).** The sentence is made true in the code by tying
the family's two integers, and there are two ways, each moving
different things (COMPUTATION on the integers, no engine line in
either; both stated here so that the choice is his):

- The chief physicist's tie: the clock raised to the label. The family
  `light` declared with `quantum` h = 5 and the pair `phase_per_link`
  [22, 3] (3 h n / d = 110 = e_D on the axis headings, the label kept at
  |**u**| = Q = 64), so that lambda = c x period = (64 / 110) x (64 x 3 /
  22) = 5.078 Links in place of 4.654. What it moves: the push weight
  111 KEPT, so row 13's -1.93 and -3.86 pixels KEPT; the lamp spends 5
  units per phase step; rows 2a and 10 re-pinned by their own scripts at
  the new wavelength before any run: for the two slits (slits_huygens_pin.py
  at the tied world, 2026-09-23 07:35Z) the clicks' visibility over the
  pinned bright and dark pixels 0.9138 against 0.9659 untied (nature's
  0.98: the tie moves row 2a AWAY from nature by 0.05), Pearson with the
  two-source cosine 0.850 against 0.891, wall 919, screen 1853 on 103
  pixels, faces 1324; for the openings the lamp's declared turns in the
  world files are computed for the old rate (run_10_worlds.py), so the
  worlds must be regenerated at the tied rate before run_10_pins.py can
  print the exact sums at the new Fresnel numbers (1.329 at w = 27).
  Where the two integers live: in each world file's own `families`
  entry (opening_w27, opening_w9, slits_huygens, row 13's pin worlds);
  NOT in Malus, whose world takes the photon entity of
  `examples/events/entities/families.json` (quantum 1, no rate pair, its
  phase from the polariser's half-angle tables and the wheel at N = 256),
  shared by every world that names that entity, nor in the light clock's
  `clock` family (quantum 1, no rate pair): the tie by the pair does not
  touch them, and the quantum 5 would touch every world of the entity if
  the entity were tied; the owner chooses the four worlds' own entries or
  the entity.
- Reviewer 3's tie: the label lowered to the clock. The lamp's label
  |**u**| = 14 so that e_D = isqrt(3 x 14 x 14) = 24 exactly = 3 h n / d
  at h = 1 and the registered rate, the wavelength KEPT at 4.654 Links.
  What it moves: the push weight 111 to 24, row 13's -1.93 and -3.86
  pixels to -0.42 and -0.84 (as computed above); light's flow label
  scaled by 14 / 64 wherever light is a crowd's SOURCE; `family_flight`
  extended to a non-massive family with its own label scale (a
  declaration of kind 1, ALGEBRA 5.3); rows 2a and 10 unmoved.

A fact of the record that both ties must face (found 2026-09-23 07:45Z
in the loader, world.py about line 604, DERIVATIONS_BEAM 17.6 N5): the
engine already carries an E = h f identity of its own, `3 h n = Q S
d_K` (the exchange's accounting, the books' balance, WITHDRAWN until
derived; a diagnostic line at load naming each paid family off it and
its gap, a refusal only where the world declares `books`, which no
pilot world does), and it differs from the sentence's form on the
headings (3 h n / d = e_D = isqrt(3 u . u), 110.85 at |**u**| = Q) by
exactly sqrt 3: N5 wants h n / d = Q S / 3 = 21.33, the sentence wants
h n / d = 110 / 3 = 36.67. Neither is on the law today (ALGEBRA 5.3,
"the content and the phase rate untied on main"); the physicist's tie is
off N5 by sqrt 3 and the loader prints that gap as its diagnostic line;
Reviewer 3's tie is off it by the same factor in the other direction.
The sentence of record 1297 chooses the energy on the headings, the
push's weight; the sqrt 3 is stated so that the choice is the owner's.

The Boss recommends the physicist's tie to the owner, since it keeps the
measured deflection (row 13) and moves only a wavelength the scripts
re-pin; the chief physicist agrees, with the cost named: row 2a's
expected visibility falls to 0.914 at the tied family, further from
nature, and the openings' exact sums are re-derived only after their
worlds are regenerated. The owner's "bug" of record 1267 is, by the pins
of M11, not a bug in free space; the Highlights say so plainly in the
rewritten line (the Boss's).

**Form W or Form P: is it derived from the law? (the owner's question of
06:39Z, record 1301; the Boss's answer corrected where it is wrong).**
The Boss's answer: the law reads both moments on the same row and does
not say whether they are one thing written twice; the one-reading
principle decides; if the identity holds on the lattice Form W is the
law's form and gamma stays declared; if the lattice breaks it, the
difference is the lattice's space part and gamma may be derived. The
correction, on the computations that exist: (i) the one-wall identity
(the tilt equals the push) is a CONTINUUM identity (`one_wall_check.out`
sections 1 and 2, exact in the closed forms); (ii) on the lattice it is
NOT met by the crowd's own moments: the light-bending map
(`docs/designs/open_problems/light_bending/light_bending_map.out`, lines
35 and 52) reads the ratio of the flow to the gradient of the age moment
along the beam's line at -0.340 and -0.023 against the continuum's 1.000
("the ripple the digital lines'"), and the one-wall map (section C) reads
the delay's difference between neighbouring rows as no gradient at all
at the fan P = 6 (its sign flips from b = 6 to b = 3; "the front's tilt
is not readable by neighbouring rows at P = 6; it needs the dense fan or
a shell mean"): the lattice reads two combs, not one number; (iii) so
the law as built is not double-reading one thing: it reads two moments
(A on the wall, **V** on the momentum) that agree only in the shell mean
and the continuum; a ray takes the delay from the one and the bend from
the other, and the "one-reading principle" is not a principle the law
as built has: it reads twice by design (the generic entry's verbs 1 and
2). Therefore: under (b) of M11 (the ray law, Huygens at every
apparatus) the question does not arise: both readings stay, gamma is a
declared input (0 by default; 1 gives nature's 2 and Shapiro's 2, an
input read back), row 13 stays "an input read back", and nothing is
derived. Under (a) (a lattice wave), a wave tilts by the wall's delay
across its whole front (the shell mean the map says a wave needs), so the
wave WOULD read the delay's gradient as a bend and the push as a second
bend: there Form W (the push off for the row that splits) would follow
from a one-reading principle IF the owner writes that principle into
the law (it is not there today), and gamma stays declared; whether the
lattice's front tilt equals the continuum's is then the wave's own
computation with its dispersion (Reviewer 3's caution), not made, and
if it differs, the difference is the lattice's, not a derived gamma. So
Form W is not derived from the law as built: it needs his word as a new
rule ("a row reads the crowd once"), and only for a wave; for the ray
law there is nothing to choose. That is the answer to his question,
plainly: not derived; his signature, and only under (a).

### M8. The split's domain, the recorded row of a family without the flag `massive`; a body is a quantum: what the design leaves for the massive form

The owner's rule has one exception, the quantum. This design splits the
recorded rows (`record != NO_RECORD`, born by a lamp under the amplitude
law) of every family without the flag `massive`, light's rows of content
1 per unit included (Reviewer 3's D1), and leaves every massive family's
row and every body as it is: a body is the quantum that does not split, its record, its
push, its contact and its `become` untouched (DESIGN.md section 8). Not
a mistake found; the boundary of this design, named so that the massive
form (the next design) says how a massive row splits, which rows 6, 8a
and 14 need (section 3).

### M10. The copy rule at a free Node is a diffusion; the split as the Grover coin: REFUTED BY M11 (rows 2a and 10), kept as the record of the form tried

amplitude-v1's split (section 2.1, the `rerelease` entry's rule) sends
one arriving row to K outputs as K copies over sqrt K, an isometry of
one input. At a free Node under the split the inputs are K arrivals, and
the copy rule applied to each is the rank-one matrix (1 / sqrt K) J: it
forgets the direction of what arrived and the record's amplitude then
spreads as a diffusion with phases (in one dimension a_k(t + 1) =
sqrt 2 cos k a_k(t), an amplifying heat kernel, no front), not as a
wave; the shares of far and near cells are then set by the path counts,
not by the interference, and the pins of DESIGN.md section 7 are not its
readings. The correction (DESIGN.md section 3.2, on Reviewer 3's A1 that
the split is verb (B) with a declared matrix): the split at a free Node
is the multiplication of the Node's arrivals by Grover's coin (2 / K) J
- I over the world's fan, unitary, declared by K alone, the norm
conserved exactly, the single arrival's outputs 2 / K forward and (2 -
K) / K backward (Huygens' forward wave); the lamp's fan and a
`rerelease` entry keep the one-input rule. Three tests: generic PASS
(one matrix by K, no name), vector PASS ((B), declared integers over K,
the multiplicity times K^2), local PASS (the Node's own arrivals). What
it costs, the exact wave's digits: the amounts grow as K^tau (a
surviving row's amount at least K^tau / sqrt W), int64 to tau = 8 at K =
90; the build carries them as Python integers (HOST, ten to fifty times
int64); the one alternative, an amplitude grain declared at load with
the remainders dropped at a stride, is a rounding at run time and not
one of the six verbs: the owner's word decides between the exact form
(the HOST pays) and a declared rounding, and this file takes the exact
form until he speaks.

Reviewer 3's second read (record 1300) on this item, answered by M11's
refutation and by one line each: P1 (the walk's dispersion, cos omega' =
(1 / K) sum_j cos(k . d_j) on the propagating pair, the pace c / sqrt 2
at long wavelength on an in-plane fan, further branches on fans of 8 and
more, flat bands at +1 and -1 holding 2 / K of every arrival): agrees
with what split_pins.py measured (the front a bundle at 0.54 to 0.61
Links per interval, the trapped share never ending), and it is why the
reading is speckle; P2 (the grain's cap of W rows against the 10^5 to
10^6 cells a resolved wave needs): moot under M11's option (b), a design
question of its own under (a), where the grain acts on the merged offer
at the sets and not per row on the GameBoard, the rows then the wave's
cells and the HOST theirs; C1 (the coin's words: the direct ray continues
with -(K - 2) / K and decays as ((K - 2) / K)^(2 t), the wave what the
scattered 2 / K builds): right, and moot; the light clock under the coin
(one return per birth lost, the direct cell's share ((K - 2) / K)^(2 L))
moot under (b), where one return per birth stands and gate 1's five
pins are the law's.

### M11. The pins' verdict on the coin, before any build (split_pins.py, 07:40Z): the coin form is refuted by its own pins; the build is not ready

`split_pins.py` beside this file (its output `split_pins.out`, COMPUTATION
only, no engine run) walks one record offline on the registered worlds
under each candidate form and reads the screen as the law reads it (the
pointer per set over the arrivals, the phase the record's rate times the
exact flight time on the arriving line, BEAM_LAW note 45; the cells of
the wall, the faces and the pixels; the clicks of 4096 births by
`cell_of`). Its findings, in the order they bind:

1. **The reading machinery is NOT YET the proof** (section V; Reviewer
   3's read of ea9d12ee, record 1313, AGREED): the law as built, straight
   lines with the one-time split over the world's forward fan at the
   opening's Nodes, gives a smooth bell (the pixel-to-pixel roughness
   0.10) with w x FWHM / lambda = 1.055 at w = 27 against RUN_10's 0.916
   and 0.674 at w = 9 against 0.891. The residual is the script's own:
   it models the split at the opening as a TURNED row in reseed_flight's
   form (the fan's rows advance by the record's age on the flight table,
   `Line.made(tau)` with the record's tau, the old residue dropped), which
   rounds a re-emitted row's time by up to one Link's time, 1.7
   intervals, a fifth of a turn at lambda = 4.65 Links; the engine
   re-creates a re-emitted row at the age 0 with its phase carried
   (nature_beam.py, the rerelease lines about 5812; amplitude-v1 section
   2.1) and is exact. So V does not reproduce the exact sums, and "the
   reading machinery is right" does not stand until the script's
   apparatus split is brought to the engine's own re-emission rule (a
   new row at age 0, its line's residue its own, the phase carried) and
   RUN_10's 0.916 and 0.891 (and w = 9's) are reproduced; until then no
   number of split_pins.py is a pin, every one a COMPUTATION of the
   script. The same rounding is in every section that creates rows on
   the record's age: C (the openings and the slits under the coin), E
   (the slower clocks) and F (the turn scan), whose rows all advance by
   the record's tau on their lines; section G (the hop) uses exact times
   per hop and carries no such rounding. The coin's verdict below
   therefore rests on G (speckle at lambda = 16, 32 and 64 Links) and on
   the dispersion diagnosis, not on C, E and F alone.
2. **The copy rule is a diffusion** (section A): in one dimension its
   norm grows as 2^(t / 2) and its spread as 0.71 sqrt t; the coin's norm
   is conserved and its spread 0.54 t, a front (M10 confirmed).
3. **The coin on the fan with the digital lines** (sections B, C, E, F):
   unitary only when it acts on every row at a Node every interval (the
   arrivals and the dwellers together; acting on the arrivals alone and
   merging with the dwellers it does not conserve the norm), the front at
   0.54 to 0.61 Links per interval by direction (the isotropy 6 percent at
   K = 16, 4 percent at K = 48 at the age 64, not the 0.9 percent of the
   facets), the norm 1.000000000; BUT the screen's pattern read at the
   record's clock is speckle (the roughness 0.8 to 1.0, no envelope) at
   the registered wavelength and at every slower clock tried (lambda =
   4.65 to 74 Links), and for every turn of the coin's one parameter (the
   unitary coin symmetric in the outputs is exp(i eps P), eps = pi
   Grover's, eps -> 0 the straight rays: at small eps a spike, at large
   eps speckle, no eps a bell). The single opening's w x FWHM / lambda
   reads 0.02 to 0.09 against the pins 0.916 and 0.891: refuted, below the
   0.85 that refutes 22.2, by its own pins.
4. **The hop (pace B) with Grover's coin** (section G): speckle likewise
   at lambda = 16, 32 and 64 Links.
5. **A scalar lattice wave** (section H, the field form of build (i) with
   two time levels, psi(t + 1) = c^2 sum over the neighbours - psi(t - 1)
   + (2 - 4 c^2) psi(t), c^2 = 1 / 3, the source the aperture as a plane
   wave): a smooth bell (the roughness 0.008), but 1.244 against 0.916 at
   the registered clock and no diffraction pattern at the slower clocks
   (flat at lambda = 9.2, a dip at the centre at 18.5): the two-dimensional
   wave's wake and the pulse's time profile enter the reading, and the
   reference model itself is not yet right; not a verdict on the field
   form, a statement that its pins are not yet computed. Reviewer 3's
   line (record 1313), agreed: section H is NO REFERENCE YET. Its failure
   is the reference model's, not the field form's: the absorbing Nodes
   zeroed at every step are Dirichlet reflectors, not absorbers; the
   source is a one-step impulse, not the clock's frequency; the far edges
   are damped by a hand-set factor. The right reference is the lattice
   Helmholtz problem at the clock's frequency (a monochromatic source at
   the aperture, an outgoing condition at the edges) at a wavelength of
   ten Links or more, its pattern compared with the Fresnel sum at the
   same Fresnel number; until that is computed, section H says nothing
   for or against a lattice wave.
6. **The registered bars** (section D): 98 percent of the pair record's
   norm leaves through the open faces, alice_plus reads 0.020 and
   bob_plus 0.0008, alice_minus and bob_minus nothing: NOT READABLE
   (Reviewer 3's D3 confirmed by the numbers).

**The diagnosis.** The law as built is dispersion-free: every row moves
at c on an exact line, so one birth's pulse, read at the record's clock
over its arrivals, IS the monochromatic pattern (the Fresnel sum), exact
at any wavelength; that is why the registered pins are so precise. A
lattice walk (any coin, any pace) has its own dispersion: the record's
clock read on one birth's pulse selects the walk's modes at that
frequency, several branches at unrelated wavelengths (a coin's -1
eigenvalue folds the frequency by half a turn), so the walk's response
at the clock's frequency is not the Helmholtz kernel and the screen
reads speckle. A lattice wave with a clean long-wavelength limit (the
scalar two-level field) reads smoothly, but its pins are not yet
computed right and its wavelength must be many Links (the registered
4.65 is not), which scales every world's geometry with it.

**What this means for the design.** The split as the Grover coin (M10,
DESIGN.md 3.2) does not reproduce rows 2a and 10 in the record form's
reading and is refuted before any engine line; the build of M1 as
written is not ready and does not start. What stands: the split's
absence is the owner's finding and his decision; the copy rule is not a
wave; the diagnosis above. What is open, for the owner's word through
the Boss, one line each: (a) whether the split at every Node must be a
lattice wave equation (the field form, build (i), a two-level field per
record, "the sum from the six neighbours, the event propagates", whose
dispersion at the world's clock must first be shown to give the
diffraction pins, a computation to make right before any build, and
whose wavelength must be many Links, the worlds re-registered at a
slower clock and a larger geometry, HOST); or (b) whether "the ray
splits" is met by the law's Huygens at every apparatus (the split at
the lamp, the openings, the re-emitters, the law as built, exact at
every wavelength, passing the pins) with the split at a free Node shown
by these pins to be a diffusion or a speckle, so that the correction of
M1 is the world files' fans (M7) and not the engine; or (c) a third
form the physics-rule reviewer or the mathematician names, with its
pins first. The chief physicist's recommendation: (b) now, because it
is exact and passes; (a) as a design of its own with the mathematician,
its dispersion and its pins before any engine line; nothing built until
the owner chooses.

### M12. The Register Architect's fixes (RUN_AUDIT.md section 4 at 62e3aba9), the chief physicist's read

His measured rates (HOST): 3 to 8 microseconds per live row per interval,
1.4 KB of peak memory per live row; 315 registered worlds after PR #860,
465924 registered intervals; a week for the full re-run on the present
structures, a day with his top three fixes. On the law's order within an
interval: the fixes that touch no rule (rank 1 the age wall vectorised,
rank 2 the dense per-Node arrays kept across intervals, rank 3 the
per-row `click` lines written on request, rank 5 the crowd's `unique`
reused, ranks 6 to 9 the Python loops and the runner's dump) are the
host's and may be built on the Boss's GO, the gate set's digests their
proof; the fused re-ordering of rank 4 (one sort per interval in place
of the walk's, the measure's and the merge's three) is lawful only if no
rule reads the store's order between them: the collision reads the
(Node, number, content) groups on its own sort, the tables read the rows
per set in the plan's order of arrivals, the merge reads its identity
words on its own sort; a fused order must keep each reader's own order
or prove the readers order-blind; the gate set's bit-identity at every
cap is the proof, and a fused re-ordering that changes one digest is
refused. My word: build rank 4 last, after ranks 1 to 3, under that
proof; rank 10 (`_walk_rows` dead code): delete.

## 2. THE VERIFICATION PLAN, per solution, before any row is read

The owner's rule (record 1288, 05:55Z): every experiment is re-run
under the corrected engine after the build; every reading of the engine
without the split is history; no old reading stands as the law's. So:
nothing registered moves before its re-pin, and every old reading is
history in the log, labelled the old law's. The order: the pins of `split_pins.py` (M1, M10, M9's question, D3's
shares; their verdict M11: the coin form refuted, the build held until
the owner chooses the form); then the build of the chosen form with its
tests; the gate set re-pinned; the pilot of four worlds (below); the gate set re-pinned; then every
registered world re-run BESIDE its old reading (the rows of the record
form first, compared with the pins of this section; then the rest,
including the bodies' worlds, whose numbers are expected unchanged
until the massive form and whose re-run under the corrected engine is
the check of that expectation); then M3's readings on the detector's
own count; the old readings history.

**M1 and M10, the split as the coin.** (a) Pins by the algebra before
the run, written by `split_pins.py` beside this file (DESIGN.md section
7): the fan's isotropy and the coin's front (the pace by direction, the
norm to the digit); the single opening's sums at the pixel grain and the
Fresnel number 1.45 (0.916 at w = 27, 0.891 at w = 9, the far field
beside as the limit; Reviewer 3's D4); the two slits' visibility at the
pixel grain (the fan's 0.9659 history); the pair's cells 27, 5, 5, 27 and
Malus's 1 / 2 on the re-arranged bars (D3), with the closed form of the
shares on the registered bars as the record that those cannot be read;
row 13's tilt and turn (M9). (b) The engine change: one function in the
interval's order beside the `rerelease` split, the copies at the row's
Node with the multiplicity times K, the merge as it is; tests written
with the build: a one-row world (one birth, one row) shows K rows at the
next interval and the total share sum over i of (w a_i)^2 / (m A) equal
to the birth's w^2 / m, exactly; an un-split row's walk bit for bit on
the flight table (pace (A)); the merge of two copies that re-meet at one
Node sums them; the multiplicity by the age function equals the stored
product on every row to tau = 24 (six Ports); the gate set's digests
(`examples/events/gate_set.json`) move and are re-pinned as the
corrected law's, the old digests in the log. (c) Falsifiers: a pair cell
off by more than 1; the single opening below 0.85; Malus off 1 / 2 by
more than the tables' grain 1 / 256; the two slits' visibility below the
Fourier pin by more than the pixel grain.

**M2, the trigger.** (a) Pins: the same, each conditional on s_D below
the smallest cell-carrying offer. (b) Tests: one click per record
exactly (the last rung is W); no click while a counted future is in
flight; the pair's two arms in one gather; a branch below s_D deleted at
its Node and the record's total unchanged by more than s_D per branch;
Q as S2 with the detectors the only sets; the key `sensitivity` read,
its default 1, a value below 1 refused. (c) Falsifiers: a record with
two clicks or none; a fringe absent (the S1 form); a gather with one arm
(the expected outcome on the registered open bars, D6).

**The pilot before the full re-run (the owner's word of 06:06Z, record
1293: "first we must run a few worlds that we know are supposed to be
right, two, three, four, see that they converge, and then run
everything").** After the build's tests and the gate set's re-pin, four
worlds whose expectations are known run first, each against its pin
from `split_pins.py` and its falsifier; the full re-run of the register
(record 1288) only when all four converge; a miss sends the work back
to the design, not to more runs. HOST estimates from the Architect's
audit (3 to 8 microseconds per int64 row per interval; the
Python-integer amounts ten to fifty times that, unmeasured):

| Pilot | World | Pin (COMPUTATION, `split_pins.py`) | Falsifier | HOST |
| --- | --- | --- | --- | --- |
| (a) the single opening, w = 27 | `docs/designs/fail_rows/opening_w27.json` with the openings' fan entries removed, the fan K = 90, the lamp's rate lowered to one record per 32 intervals | the exact sum at the pixel grain and the Fresnel number 1.45, 0.916, inside 22.2's 0.92 +- 0.03; the coin walk's own sum beside it | below 0.85, or outside the band by more than the pixel's grain, or a norm not conserved | six live records x W rows x K: 2 x 10^6 row-operations per interval, seconds per interval, hours per world; about 150 records' clicks, the FWHM's bracket widened by their statistics |
| (b) the two slits | `examples/events/amplitude/slits_huygens.json` with the fan entries removed, K = 90, the rate lowered likewise | the double aperture's visibility at the pixel grain | the visibility below the pin by more than the pixel grain, or the fringe's period off lambda / d | as (a), 7260 Nodes, hours |
| (c) Malus | `malus_a.json` re-arranged: the bar 7 x 3 x 1 periodic in y and z, admitted and passed at one set | 1 / 2 exactly at 45 degrees (the rotation's) | off 1 / 2 by more than the tables' grain 1 / 256 | 21 Nodes, one record at a time, seconds |
| (d) the light clock at rest | `docs/designs/new_rows/worlds/light_clock_rest.json` (branch light-clock, LIGHT_CLOCK.md; gate 1 the birth stamp on branch birth-stamp) | the return count N_0 = 206 +- 2 in the detector's own clock (the arm 60 Links, c = 32 / 55, the closed form 206.25), the birth stamp to the return click's clock; under the split the chosen cell's arrival stamp, the direct path's, with a tail of later counts from the split's longer paths whose shares the script gives | a return count off 206 by more than 2 on the direct path's cell; a click stamped by the host's tick anywhere | a bar of 60 Links, one record at a time, minutes |

The click's time under the split, for (d) and for every time reading:
the click is stamped with the chosen row's arrival at its set (the
detector's own count at that arrival, `clock`), and the ladder's
decision at the record's exhaustion is the host's view of when the
choice was made, a delay of the view and not of the physics
(amplitude-v1 section 13, departure 3); a detector never reads the
tick.

**The external things under the corrected law (the owner's word of
06:06Z, record 1293: "the new method has all the detectors exactly as we
say: a detector and an emitter, mirrors, everything outside the board,
with its own clocks and everything we defined"; the checklist records
1139, 1217, 1226, 1227, 1234, 1277 and 1286).** Everything outside the
GameBoard's law is declared in the world file (record 562's list),
nothing the board has by itself:

| Kind | Declared (the key; the code) | Its clock | Its trigger under the decided form | The test before the engine changes |
| --- | --- | --- | --- | --- |
| a detector: a measured event with `measure` (a click), `read` (a non-absorbing read), `pass`, a `phase_window` (a setting), a `become` gate | `measured` entry, `table` per family (`world.default_table`, ENGINE.md's world-file section); `Measured`, `measured.py` 154; the click's deposit `nature_beam.py` 5498 | its own count of self-creations under the age wall (`engine.py` 699 to 706), stamped under `clock_stamp` on its `read`, `rerelease`, `click`, `become` lines; no host tick in any reading | `sensitivity` on its `detectors` entry, 1 by default (s_D = 1 / W); the record's exhaustion the click's non-local step | the stamp on every line of a registered world (audit item 1, byte-identical physics); one click per record; `tests/test_amplitude_click.py` extended for the key |
| an emitter, the lamp (a detector at its Node, record 570) | `lamp` `{rate, wheel, directions, turns}` on a measured event of a paid family | its own count; the birth line stamped under `clock_stamp` once branch birth-stamp merges (Reviewer 3's MUST 1 on the light clock) | none (it births records; the one-input split at the birth, the fan its declared outputs) | the birth's u = ordinal x r mod W unchanged (`tests/test_birth_wheel.py`); the birth stamp's test on its branch |
| a receiver body under `rerelease` (the thing the comments called a mirror; record 1234) | `rerelease` on a measured event with `directions`, `weights`, `turns`, `inputs` (`world.Split`); `nature_beam.py` 5413 to 5427 | its own count, stamped on its `rerelease` line | the one-input split rule with its declared outputs, unchanged; the row it re-emits continues under the coin from the next Node | `tests/test_amplitude_split.py` (the split and merge as inverses) unchanged; the comments' word replaced (M4) |
| the `sum`, `wave` and `beam` sets | `detectors` entry: `name`, `positions`, `threshold`, `reading` | the set's measured events' own counts | the sensitivity per set (the key above); the ladder over the record's offers per set | `tests/test_amplitude_layer.py`, the offers per set; byte-identical for a `wave` or `beam` set of a world with no lamp |
| a moving detector, the cart | the measured event's drive (`step_axis`, `engine.py` 122 to 154; the body carries its record, held content and Nodes, 1009 to 1011) | its own count under the age wall, the crowd slowing the count and not the click's tick; r_D = d / (d + A n) | as a detector; the click reads what arrives with the record as it is (POSTULATES 26.2) | `tests/test_moving_detector.py` (the cart's `clock` per ordinal); the two co-moving bodies both measuring (the reviewer's gate on PINS_R2) |
| an open face | the GameBoard's boundary (`boundary` open) | none (no clock) | a cell of the ladder (an escape offers); no stamp | `tests/test_face_click_summary.py` unchanged |
| a wall, a body of matter met in flight | a measured event of a paid family with `measure` (the contact rule, the push) | its own count | a click or a push, as built ("may not pass"); a body's own row does not split (M8) | the contact and push tests unchanged; the bodies' worlds re-run beside with their numbers expected unchanged |

Nothing in the table is a mechanism beyond the Boss's list of 04:58Z
except the `sensitivity` key (named in DESIGN.md section 4) and the
recorded row's exemption from the collision (M10, DESIGN.md 3.2), both
items of this design for the owner's reading.

**M3, the readings on the detector's count.** (a) Pins: each of the
audit's items 2 to 8 restated in counts before the re-run (the audit's
own lines); for the light clock (item 5) the return count from the
flight table: two legs of L Links at the pace S_1 Q / T_D in the
detector's own intervals, a COMPUTATION to be written with the world. (b)
Tests: the tools read `clock`, never `tick`, on every DETECTOR line
(`tests/test_repository_language.py`'s kind of gate on the tools'
readers); the count stamped by every registered world (item 1). (c)
Falsifiers: a restated number differing from the tick reading by more
than the detector's own dwell (the age wall's excess) where the detector
owes nothing; a moving detector's count differing from a resting one's at
the same crowd.

**M4, the mirror.** The word; no test.

**M5, the meeting.** Done (note 35); the test is the existing
`test_optical.py` on the default.

**M6, the merge.** Decided; the existing merge tests stand (`tests/test_amplitude_split.py`, the split and merge as inverses).

**M7, the fans.** The two worlds load without the openings' entries; the
opening's Nodes carry none.

**Row 13's pin (the time part's bending under the split), COMPUTATION
before the run:** the phase rate of a row of no content at a Node is
slowed by the crowd through the age wall's member of its flight (the
time part); a wave whose front crosses the crowd's gradient tilts by the
gradient of the delay across the front (Fermat's rule, the Huygens sum of
the split's paths); the deflection is the integral of the transverse
gradient of the delay along the path, evaluated on series K's crowd
(`examples/events/lensing/`) by the flight table's own stretched walls;
its number is written by `split_pins.py` before the run and compared
with the push's turn on the same lines (M9's question (i) against (ii)),
the delay beside; the form chosen on the answer, the ring's ratio 2.00
its pin.

## 3. THE TABLE'S CONVERGENCE, row by row, declared before any run

The rows are the rules page's (`STATUS_RULES.md` on branch status-rules,
PR #1013; the count on both voices as the Boss gave it: thirteen
predicted, three agree, ten disagree, six not predicted) and NATURE.md's
status column at d2982954. "The corrected law" is the law as built plus
M1 (the split, default on, rows of no content), M2 (the trigger, S2 as decided), M3 (the readings on the detector's own count), M4 and M7;
the bodies untouched (M8). Expected: PASS (agrees, or a NOT YET row
expected to agree), STAY (the status as it is, with the reason), MOVE
(the number moves, to what).

| Row | Status today | Under the corrected law | Reason, one line |
| --- | --- | --- | --- |
| 1a CHSH | agrees, S = 2.75 | PASS, unchanged | The cells' ratios are the labels' rotation; the arm's phase a common factor; the gather reads both arms (M2's S2, decided); no time is read |
| 1b the window form | a control | STAY | A theorem of every local read-out |
| 1c the order channel | disagrees, 15 / 16 against 0 | STAY disagrees | The serial correlation is the wheel's order on the birth count u, which the split does not touch; the understanding is not reached here: nature's 0 needs a click whose cell is not a function of the birth ordinal, which the law has not (no draw at a Node) |
| 1d no-signalling | agrees, a check | STAY | A theorem of the rotation |
| 2a the two slits | NOT COMPARED (0.966 on the fan) | MOVE in number to the Fourier visibility of the double aperture at the pixel grain (the pin of section 2 before the run); status NOT COMPARED until the source is verified | The fan's pin was pinned on the fan of 91 (KIND_AUDIT section 3: at most 0.004 by the grain); the split's paths replace it (M7) |
| 2b the Mach-Zehnder | agrees, 1.000 | PASS expected if the arms are enclosed; else MOVE (the danger paragraph) | The split fills the free Nodes between the splitters; the registered world's enclosure decides; the run says |
| 2c Born's power | NOT COMPARED | follows 2a and 2b | Read from their cells |
| 3 the deceleration q | not predicted, q = -0.108 | STAY not predicted | The reading against the detector's own count (M3 item 2) is a z against the light's age, not a brightness; the crowd is bodies', untouched |
| 4a the muon's lifetime | not predicted, the ratio 1 | STAY not predicted | The body is a quantum; its own count 64 at every speed; M3 item 3 restates it in `counted`; the understanding is not reached here: the dilation needs the body's count to slow with its speed, which no rule of the six gives (5b's theorem) |
| 4b the Doppler with gamma | not predicted, z = 0.2636 | STAY not predicted | The same missing factor gamma; the detector's own count already the reading at head |
| 4c the transponder | FORM row | STAY outside | No nature number |
| R2 Sagnac, R4 | beside 4a, 4b, 5b | STAY | The cart's count reads as a resting detector's at the same crowd (M3), no gamma |
| 5a c by direction | agrees (a bound met), 0.5774 to 0.5818 | PASS (the pace decided: the digital lines kept) | The flight table is the law's pace; the light clock world (M3 item 5) reads it as the detector's count, the return count from the flight table |
| 5b the two arms in motion | not predicted, beta^2 / 2 | STAY not predicted | Nothing contracts; a bodies' row |
| 6 Bohr's ratio | disagrees (the electron escapes) | STAY until the massive form | The atom is bodies; the electron's futures around the nucleus are what the massive form must give (M8) |
| 6b the atom's stability | predicted, the escape | STAY | The same |
| 7a the deuteron's binding | not predicted (an input) | STAY | The give is declared |
| 7b the alpha over the deuteron | disagrees, 2.0 | STAY disagrees | Bodies |
| 8a the decay curve | disagrees, the width 0 | STAY disagrees | The decay is the body's own count (`become` at 64), a quantum's, no futures; the massive form's question |
| 8b the neutrino's passage | disagrees, 0 behind | MOVE only if the sensitivity is per (detector, family), the cross-section as a declared input of kind 2 (an item for the owner); else STAY | The `nu` row has content 0 and splits under M1; a detector whose sensitivity to it is above the wave's offer takes no rung and the wave passes to the one behind (M2, S2); with one sensitivity for every family the first detector takes the whole front |
| 8c the neutrino's mass | not predicted (an input) | STAY | Declared |
| 9 Malus | agrees, 128 / 256 | PASS, unchanged | The rotation of the labels; the split copies them |
| R3 Malus at three settings | agrees, beside | STAY | The same |
| 10 the single opening | NOT YET (the fan's 0.925 and 0.879 the old law's, history) | PASS expected: inside 0.92 +- 0.03 and 0.886 +- 0.03; the number moves from the fan's | The Fourier width of the aperture under the split (DESIGN.md section 7); refuted below 0.85 |
| 11a, 11b, 11c the far lamp | not predicted; PASS by a pin; not predicted | STAY | The growing wall a hypothesis not built |
| 12 the clock's field | HISTORY | STAY | Superseded |
| 13 the bending of light | disagrees, 0.000 pixel (series K at `suspension` 0, the coupling declared off; the pin worlds at [1, 16384]: -1.93 at gamma 0, -3.86 at gamma 1, an input read back) | MOVE: under the split the wave's own tilt appears; the number depends on the pins' answer to M9's question (the tilt against the push on the lattice) and on the owner's choice of form; under Form W the deflection 2.00 and the delay 2 with gamma = 1 declared, "an input read back" with the split's own number | At head a ray on a digital line cannot turn, only its age changes; under the split the front tilts by the gradient of the delay (Fermat), the wave's own bending; the space part's weight content x w is 0 on light (M5) |
| 14 Newton after a detector | NOT YET READ | STAY until the arrival click (RUN_14) and the massive form | Bodies; M3 item 6 restates the period in counts |

**What we say passes must pass with the new detectors.** The rows that
pass or are expected to (1a, 1d, 2b, 5a, 9, R3, 10) read no time from
the host: the cells, the visibility, the pass fraction and the spread
are ratios of offers at the detectors' Nodes, and 5a's reading becomes
the light clock's return count. Under the detector's own count (M3)
none of them moves. The rows where the understanding is not yet
reached, said plainly: 1c (the click's order), 4a, 4b, 5b and R2 (the
factor gamma on a body's own count), 6, 8a and 14 (the massive form),
7b (the binding's growth), 8b (the sensitivity per family), 13's second
half (M9's question, the pins before the build), 3 and 11 (a brightness click and the
wall's growth). The split and the new readings move 10 into its band,
13 to its first half, 2a to the aperture's own pin, and 8b conditionally;
they leave the bodies' rows where they are, by design (M8).

## 4. Links

[DESIGN.md](DESIGN.md) (the split's design; section 1 the algebra under
the split, sections 9 and 10 the host cost and the dangers);
[the Outside audit](../outside_audit/AUDIT.md); [RUN_10.md](../fail_rows/RUN_10.md);
[KIND_AUDIT.md](../fail_rows/KIND_AUDIT.md); [NATURE.md](../../NATURE.md);
[ALGEBRA.md](../../ALGEBRA.md); [ENGINE.md](../../ENGINE.md), the
detectors' readings by type.
