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
PASS (the comparison is the detector's own on its own record; the
exhaustion is the record's own count of its counted futures, a HOST
bookkeeping of the record labelled so, as the layer's live count is
today). Pins: the pair world's cells 27, 5, 5, 27 and S = 2.75, Malus
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
owner's word of about 05:52Z ("confirm to him that I agree with you,
what you think today is right; I agree with you on everything") makes
it his decision: the trigger is S2; S1 is what the code forbids and
stays listed so that its pins are on record. Two more of his decisions
by the same word: a sensitivity per (detector, family) is a declared
input of kind 2 (the cross-section; row 8b's condition in section 3);
and the crowd's flow turning a row of no content (row 13's second half)
is NOT decided as a law by it: the chief physicist has no verified form
for it and names it a hypothesis for its own identity after the split's
runs (M9).

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

### M5. The meeting: the paid unit's reading of the free crowd

The owner (record 1272): it enters generically as the default. The code:
it is the default since 2026-09-22 in the momentum form (`optical_turn`,
`nature_beam.py` 3733 to 3770, verbs 2 and 3 of the generic entry: the
time part in the flight wall for every row, the space part the turn of
the momentum accumulator **W** by the crowd's flow with the weight
content x w, on every row of every family in free space, no key);
meeting-v1 under the key `meeting` is the earlier phase-register form,
off by default, the five lensing worlds' history. Not a mistake of the
code; a mistake of the law's text, corrected in BEAM_LAW note 35 (branch
`beam-law-note-35`, 15db1a62). One consequence for row 13 is in section
3: the space part's weight content x w is 0 on a row of no content, so
light is not turned by the space part at head (series K's 0.000), and
under the split the time part alone bends the wave.

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

### M9. The space part of the bending on a row of no content: a hypothesis, not a correction

Series K reads 0.000 pixel for light beside a mass because the space
part of the generic entry (`optical_turn`, the momentum accumulator
translated by the crowd's flow with the weight content x w) is 0 on a
row of no content (M5). Under the split the time part alone bends the
wave (section 3, row 13, the first 1 of 1 + gamma). The second 1 would
need the flow to act on a row of no content by its energy (its phase
rate, E = h f) rather than by its content, a rule the chief physicist
has not verified and does not put in the law by this design: it is a
hypothesis under its own identity, with its three tests and its pin,
after the split's runs; the owner's word of 05:52Z ("I agree with you on
everything") is read here as agreeing to that order, not as entering
the rule.

### M8. A row of no content does not split at head, and a body is a quantum: what the design leaves for the massive form

The owner's rule has one exception, the quantum. This design splits rows
of no content (light, and any family declared with content 0, the
neutrino's `nu` at head) and leaves every row of content and every body
as it is: a body is the quantum that does not split, its record, its
push, its contact and its `become` untouched (DESIGN.md section 8). Not
a mistake found; the boundary of this design, named so that the massive
form (the next design) says how a massive row splits, which rows 6, 8a
and 14 need (section 3).

## 2. THE VERIFICATION PLAN, per solution, before any row is read

Nothing registered moves before its re-pin; every old reading is
history in the log, labelled the old law's. The order: the build of M1
and M2 with their tests, the gate set re-pinned, then the rows of the
record form re-run BESIDE and compared with the pins, then M3's
readings, then the bodies' rows after the massive form.

**M1, the split.** (a) Pins by the algebra before the run: DESIGN.md
section 7 (the pair world 27, 5, 5, 27 and S = 2.75; Malus 1 / 2; the
single opening's far field 0.887 and 0.891, the band 0.92 +- 0.03 and
0.886 +- 0.03); to be added by a script beside the build, `split_pins.py`:
the two slits' visibility as the Fourier sum of the double aperture at
the pixel grain of `slits_huygens` (the fan's pin 0.9659 is history), and
row 13's deflection (below). (b) The engine change: one function in the
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
Q as S2 with the detectors the only sets. (c) Falsifiers: a record with
two clicks or none; a fringe absent (the S1 form); a gather with one arm.

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
with the time part's 1 of 1 + gamma; the space part's 1 (gamma = 1) is
not the split's (M5).

## 3. THE TABLE'S CONVERGENCE, row by row, declared before any run

The rows are the rules page's (`STATUS_RULES.md` on branch status-rules,
PR #1013; the count on both voices as the Boss gave it: thirteen
predicted, three agree, ten disagree, six not predicted) and NATURE.md's
status column at d2982954. "The corrected law" is the law as built plus
M1 (the split, default on, rows of no content), M2 (the trigger in the
S2 or Q form), M3 (the readings on the detector's own count), M4 and M7;
the bodies untouched (M8). Expected: PASS (agrees, or a NOT YET row
expected to agree), STAY (the status as it is, with the reason), MOVE
(the number moves, to what).

| Row | Status today | Under the corrected law | Reason, one line |
| --- | --- | --- | --- |
| 1a CHSH | agrees, S = 2.75 | PASS, unchanged | The cells' ratios are the labels' rotation; the arm's phase a common factor; the gather reads both arms (M2's S2 or Q); no time is read |
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
| 5a c by direction | agrees (a bound met), 0.5774 to 0.5818 | PASS under pace (A); MOVE under pace (B) to the L1 front, the bound failed at the front | The flight table is the law's pace; the light clock world (M3 item 5) reads it as the detector's count, the return count from the flight table |
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
| 13 the bending of light | disagrees, 0.000 pixel | MOVE to the time part's deflection, 1 of 1 + gamma, by the split alone (the pin of section 2); the second 1 stays a missing rule unless gamma is declared (an input read back) or the crowd's flow turns a row of no content (an item for the owner) | At head a ray on a digital line cannot turn, only its age changes; under the split the front tilts by the gradient of the delay (Fermat), the wave's own bending; the space part's weight content x w is 0 on light (M5) |
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
half (the space part on light), 3 and 11 (a brightness click and the
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
