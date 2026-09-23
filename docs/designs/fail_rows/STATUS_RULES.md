# The status rules of the confrontation register: the decision procedure for every row (the physics-rule reviewer, 2026-09-23)

The order (the Boss, 2026-09-23, 03:17Z, on the model owner's word of the
same day, record 1223: "these rules on what is predicted, what is not
predicted, what is right, what is wrong: on this the paper will stand or
fall, so we must be very, very precise"): one page, the decision procedure
for every row of [`docs/NATURE.md`](../../NATURE.md) and of the paper's
Table 3 (`paper/general_formula/main.tex`, `tab:nature`), numbered in the
order it is applied, each step with the record that set it and the code
line that makes it checkable; then the procedure applied to every row in
one table, so that the chief physicist's rule (record 1215) and the
reviewer's (record 1196) are decided row by row by the same steps and not
by a judgment. Docs only, no run, no number moved, no cell edited: this
page is a proposal. The chief physicist verifies it, the model owner reads
it, and only then the writer and the Register Architect apply it
identically to the paper and to the register (one writer per shared
interface; nothing here edits `NATURE.md`, the paper or `CRITERIA.md`).
Base commit `688a93d3` (`origin/main`, "Merge pull request #996").
Records 1215, 1216 and 1223 are cited as the Boss reported them on
2026-09-23; their log entries were pending at this base. Code lines are
those of `src/event_universe/events/` at the base commit. Amended on
2026-09-23 after the chief physicist's verification (PR #1013) and the
reviewer's answer of 04:42Z: rows 3 and 5a conceded to the physicist, step
(2)'s last sentences, step (5)'s tolerance, two citations, and the carries
for rows 4a, 4b, 8a and 13; nothing else moved.

Notation: gamma is the Lorentz factor, beta the speed as a fraction of c,
Q the grain (the flight's denominator), sigma a cross-section, epsilon a
small fraction; every number below carries its kind.

## The procedure, in the order it is applied

**(0) The row.** One observable, dimensionless; one published number with
its uncertainty and its source; the mark "verified" or "to verify against
the source" as `NATURE.md`'s section "Values marked to verify" has it. A
reading with no published dimensionless figure is not a row (it waits in
`NATURE.md`'s section of readings with a counterpart in quantum theory but
no figure). Where nature's number is a bound or a fitted parameter (the
model owner's kind (2), record 1173), that is said here, beside the
number; it sets the direction of the comparison (a bound) or its tolerance
(a fit) and never the row's status. The referee counts independent
predictions (record 1159): two rows of one observable are one row.

**(1) The kind of the law's number, read off the code line that produced
it.** The kinds are HIGHLIGHTS 5.4 item 9's and record 281's; the line
that wrote the number decides, not the tool that summed it.

- DETECTOR: a line the engine writes at a measured event or at a face:
  `"event": "click"` (`nature_beam.py` 5536, the measured event's click
  line of the `measure` branch; 4333, the face line carrying `record`,
  `branch`, `multiplicity` and `u` at 4340 to 4352; `engine.py` 986 for a
  body at a face); `"event": "gather"` with its `chosen` cell
  (`amplitude.py` 964 and 971: the record's one click, the RECORD form);
  `"event": "record"` (`nature_beam.py` 5612: a declared detector's record
  line over many rays, the CROWD form); `"event": "read"` (5375),
  `"event": "pass"` (5262), `"event": "become"` (6311, the products
  thrown); a body's own record's count, a `become`'s `counted` or a stamp,
  is DETECTOR by HIGHLIGHTS 5.4 item 9, and only its Node by a `step` line
  is GAMEBOARD. The line's time is DETECTOR only under the world key
  `clock_stamp` (`world.py` 1309 to 1312), which stamps `"clock":
  entry.age`, the event's own count of self-creations under the age wall
  (`nature_beam.py` 6322; `engine.py` 1000); without the stamp the line's
  time is the host's tick, GAMEBOARD (records 768 and 1196 on rows 3 and
  4b: the re-run at head read the same count in the detector's own clock,
  `count_owed`, `engine.py` 157, returning (0, accumulator) at a zero
  `suspension` numerator: no count owed, the age one per interval).
- GAMEBOARD: the host's view: the tick, a state column, a store, a
  presence, a body's Node by its `step` line (`engine.py` 1023), a `home`
  line (`nature_beam.py` 5246, no clock and no record), the flight table's
  arrivals. A diagnostic, printed beside a DETECTOR number and in no
  verdict (record 281).
- COMPUTATION: a pin in closed form with no run (R3, record 1196). It is
  the law's own number when the pin is of the law as built (the flight
  table's resolution T_h = isqrt(3 Q^2), `world.py` 475; `count_owed`,
  `engine.py` 157; the click algebra of `docs/ALGEBRA.md`). It is a
  hypothesis's number when the pin is under a key that is false or absent
  by default (`covariant_readings`, `flow_link`, `centred_step`, `drive_b`:
  the key list `WORLD_KEYS`, `world.py` 396 to 430; `covariant_frame`,
  `engine.py` 218) or under a hypothesis with no key at all (the growing
  wall, `expansion-v1`: no such key in `WORLD_KEYS`). The key `optical` is
  not such a key: gamma = 0, absent or declared 0, is the law's own
  coupling for every world (`_optical`, `world.py` 3930 to 3956, the
  generic entry, record 847), and only gamma > 0 is a declared input.
- CONVERSION: arithmetic on click lines by a named reading (a fraction of
  cells, a ratio of two of one detector's counts, a visibility).
- INPUT: a number declared in the world file and read back by a click: a
  content of the family table, a give, a fan width, a gamma above 0, the
  width S (the inputs table of record 817, kind 2 there; the grain Q = 64 is
  a constant of the law, not an input).

The rule of this step: a DETECTOR number, a CONVERSION of one, and a
COMPUTATION of the law as built go on to (2); a GAMEBOARD number waits
outside the count with its run named (the reviewer's rule, PR #979); an
INPUT read back, and a COMPUTATION of a hypothesis, go to (3) as a named
missing piece.

**(2) The owner's principle (record 1216).** "What nature measured was not
measured on the board; very special things must be done to convert a
measurement at a detector into a measurement on the board." Applied as
two questions, answered before any number is looked at: which detector of
nature read the observable, and what did it read; which detector of the
law, in the law's version of that arrangement, reads it, and what does it
read (a click, a record's moments, an external thing's reading, or the
pin of that click in closed form). The observable is the parameter both
arrangements read, not the distance or time variable one of them uses (row
3: q_0 is a property of a(t) alone, and z against the light's age reads it
at second order as the luminosity distance does). If the law's detector
reads the observable in that arrangement, or its pin in closed form is of
that click, the row goes to (3). If the law as built has no click of the
observable at all, the row is not predicted by (3)(b), inside the count as
P, the missing click named (6, 11a, 11c). If the law has a reading but
nature's side is unverified, or the two sides are not yet the same
observable and no conversion is written (the dictionary of HIGHLIGHTS 5.7),
the row is NOT COMPARED, outside the count, until the source is verified or
the conversion written (2a, 2c). A number of another observable, however
definite, is not a number for this one.

**(3) The structure before the outcome (records 1166 and 1173).** A row
that passed (2) is "not predicted" only for a named missing piece, printed
in the row's bracket, of one of these forms: (a) a declared input read
back (INPUT of step (1)): the give of 7a, the content of 8c, the
gamma_PPN behind 13's ratio (a constant of the law, such as the grain Q =
64 of `world.py` 348, is not an input: row 5a); (b) no click definition of
the observable in the law as built, the law's number being another
observable's or none (a line, a brightness, an angular size); (c) a key or a hypothesis not built, the pin its number and not
the law's (the growing wall of 11a to 11c). A missing RULE is not a
missing piece of this kind: where the law's detector reads the observable
and reads it wrong, the row is predicted and the missing rule is named in
its disagrees line, as 8a's line names the bath and 1c's the wheel (rows
4a, 4b and 5b: no verb makes a count depend on the momentum and nothing
contracts, `count_owed` at `engine.py` 157 advancing one per interval at
every momentum). Nature's number being a bound or a fit (kind (2)) was
said in (0) and decides nothing here.

**(4) The referee's test (record 1159).** The row sits in the same class
had its number matched nature. Asked of every row: had the law's number
equalled nature's, would this register have written "agrees"? If yes, the
row is predicted and goes to (5). If the same words would still stand ("a
declaration read back", "another diagram", "a hypothesis's number"), the
row is not predicted, and (3)'s bracket is right.

**(5) Agrees or disagrees.** Only against a pin declared before the run
and never moved (record 1129); the tolerance is two standard errors of the
source's stated uncertainty, or the source's own stated confidence
interval (1a at 1.65 standard errors agrees), else the tables' grain (1 /
256 for row 9) or the register's stated bracket; a bound met is marked "a
bound met" (after this procedure no row carries it); the law's number is
printed either way with its kind, and a disagrees line names the missing
rule. A disagrees with no number is not a disagrees (record 1166, "with
the number").

**(6) The other words, all outside the count.** NOT COMPARED: step (2)
failed, or nature's number is not yet verified (2a until its two-slit
source is verified, the owner's placement of record 1204; 2c, kappa not
computed from the cells). NOT YET: the run is defined and not completed,
or the reading is not yet a click (10; 14, a period not yet a click,
RUN_14). HISTORY: a verdict superseded by the owner's word and kept (12,
the presence word, record 394). A control (1b, a theorem of every local
read-out). A consistency check (1d, a theorem of the click's form,
`docs/ALGEBRA.md` 4.9). A FORM row (4c, no nature source with a number
named). R2 and R4, pins of rows not yet run, a line beside their family
(4a, 4b, 5b) and never evidence on them (record 1190). Each keeps its word
until its own condition changes.

**(7) The count sentence.** Formed from (2) to (6) alone, every row of the
table in exactly one place: "of the N observables the law as built
predicts (N + 1 once row 14 is read), A agree within tolerance (...), D
disagree (...), and P are not predicted by construction (...); 2a NOT
COMPARED until its source is verified; K rows keep their words (...); 1b a
control, 1d a consistency check and 4c a FORM row, outside the count",
with N = A + D. The model owner decides the count; the procedure yields
it.

## The procedure applied to every row

The columns: the row; the law's number with its kind and the line that
wrote it (step 1); compared or not, by the two detectors (step 2); the
class and the missing piece (steps 3 and 4); the status (steps 5 and 6);
the one reason. Nature's numbers and sources are `NATURE.md`'s rows table
and are not repeated.

| Row | The law's number, its kind, the line (1) | Compared? The two detectors (2) | Class, the missing piece (3, 4) | Status (5, 6) | The one reason |
| --- | --- | --- | --- | --- | --- |
| 1a | S = 2.75 (DETECTOR: one `gather` per record over 64 births, the cells 27, 5, 5, 27; `amplitude.py` 964) | yes: nature's coincidence counters at two stations; the law's gather cells at two parties; the same S | predicted | agrees | within 1.65 standard errors of 2.42 +- 0.20 |
| 1b | S = 2 exactly (DETECTOR: the counters' clicks of the window form) | yes | a theorem of every local read-out | a control | outside the count; the law's row is 1a |
| 1c | 15 / 16 under a = 0 (DETECTOR, the second party's serial correlation at lag 1, met 16 of 16) | yes: one detector's successive clicks, their correlation | predicted; the missing rule: the wheel is a counter, the order deterministic (no draw at a Node) | disagrees | 15 / 16 against 0 |
| 1d | 0 exactly (DETECTOR, replayed at head; the difference COMPUTATION from the cells) | yes | a theorem of the click's form (`docs/ALGEBRA.md` 4.9) | a consistency check | outside the count |
| 2a | the visibility 0.966 (DETECTOR, `slits_huygens`; the pin 0.9659 COMPUTATION, met) | not yet: nature's two-slit figure unverified (0.98 is a Mach-Zehnder's) | a prediction under every fan (KIND_AUDIT.md section 3) | NOT COMPARED | until the source is verified (record 1204) |
| 2b | the visibility 1.000 (DETECTOR, 64 / 0 over 64 births) | yes: one detector's bright and dark counts | predicted | agrees | above 0.98 |
| 2c | the power window [1.917, 2.012) (COMPUTATION from the click cells) | no: kappa not computed from the cells | none | NOT COMPARED | keeps its word |
| 3 | the law's own crowd q = +0.35 to +0.92 (the flux weight and the source rule) and the coasting control q = -0.108, the Milne form q = 0 within the grain (DETECTOR: the pointer's z against the row's age at the click, in the detector's own clock at head) | yes: nature's q_0 is a property of a(t) alone; the luminosity distance reads it, and z against the light's age reads it at second order, z = H tau + (1 + q_0 / 2)(H tau)^2, no brightness and no conversion needed (the register's own note: the same diagram in another distance) | predicted; the missing rule: nothing in the law accelerates the throw, the crowd decelerates as general relativity without a cosmological constant; had the law read -0.53 the register would have written agrees | disagrees | q >= 0 against -0.53 +- 0.01 (a fitted parameter of the diagram, said beside); the missing click of a brightness is 11a's piece, not this row's |
| 4a | the ratio 1: the products' face clicks at 64 plus the flight at every speed (COMPUTATION, the pin of the law as built, R3; the run J4 the click); the body's own count 64 (DETECTOR by 5.4 item 9, the body's own clock; the laboratory's reading the products' face clicks, the same 1 at r = 1); under `covariant_readings` 369 and 345 (DETECTOR, a hypothesis's) | yes: nature counts the decay products at detectors round the ring against the laboratory's clock; the law's face clicks against the detector's own clock; a ratio of one detector's counts, no conversion | predicted; the missing rule: no verb makes a count depend on the momentum (`count_owed`, `engine.py` 157); had the clicks come 29.33 times later the register would have written agrees | disagrees | 1 against 29.33 |
| 4b | z = 0.2647 at head (the re-run, the pin met) and 0.2636 registered, at beta = 0.2674 (DETECTOR: G2's detector at the centre, in its own clock at head; `nature_beam.py` 4333 with the stamp) | yes: a moving emitter's light at a detector at rest against its rest rate, as Ives-Stilwell and Botermann read it | predicted; the same missing rule (the factor gamma = 1.0378 absent) | disagrees | 0.2647 against 0.315 (the classical Doppler 0.2674) |
| 4c | 3.708 and 2.054 for 151 / 41 and 43 / 21 (DETECTOR, RUN_4AB.md 6.3) | in form only | no nature source with a number named | FORM row | outside the count |
| 5a | 7.6 x 10^-3 at the law's grain Q = 64, the anisotropy 1 / (sqrt 3 Q - 1) (COMPUTATION, the flight table, `world.py` 475; Q a constant of the law, `world.py` 348); series Q's 290 of 290 clicks within it (DETECTOR) | yes: a two-way pace by direction at one detector, the observable the resonators read | predicted; Q is a constant of the law as built and no world file's input, so (3)(a) does not apply; had the pace by direction differed by less than 10^-18 the register would have written agrees | disagrees | 7.6 x 10^-3 at the registered grain against below 10^-18, fifteen orders; what would agree: Q >= 2^59, within the 64-bit word only at a fan of the six headings |
| 5b | gamma^2 along and gamma across, beta^2 / 2 (COMPUTATION, R3, the law as built: nothing contracts, the bond a whole Link; the pair in motion the click) | yes: the fringe at one detector, the ratio of two round trips; the laboratory's orbital speed changes by 60 km/s over the year, so beta = 10^-4 for part of it | predicted; the same missing rule as 4a (a contraction by 1 / gamma) | disagrees | at least 5 x 10^-9 for part of the year against below 10^-17 |
| 6 | no line read; the algebra's 27 / 20 a conjecture in the shell mean's limit (COMPUTATION, not a click of the law) | no: the law's detector reads no line | (3)(b): no click of a line, no rule of the six quantises a loop or moves the electron between two closed loops | not predicted | [kind (3)] |
| 6b (the atom's stability; the owner's word on entering it) | the electron escapes at 3407 intervals (DETECTOR, series H's world); under `centred_step`, a declared start, no escape in 7500 intervals (DETECTOR) beside | yes: a free electron at the border, where nature's detector behind hydrogen reads none | predicted; the cause the half-Link lag (WHAT_IS_MISSING.md 1.6) | disagrees | a finite escape against no escape (nature's a bound) |
| 7a | 4 of 3677 = 0.109 percent (DETECTOR, the border's `bond` clicks) | the observable the same, but the give is a declared INPUT read back | (3)(a) (record 1204) | not predicted | [the missing piece a rule deriving the binding; 4 of 3677 brackets nature's 4.35] |
| 7b | the ratio 2.0 (DETECTOR: four border clicks against two) | yes: two bindings read as clicks | predicted; the missing rule: a give growing with the bonds a body makes | disagrees | 2.0 against 12.72 |
| 8a | the laboratory-clock reading, the shell detector's own count under `clock_stamp`, NOT MADE, the Row 8a Runner pinning it (PINS_8A_CLOCK.md: at most 2.93 before the run); the width 0 in each neutron's own clock (DETECTOR by 5.4 item 9, a body's own record, the 64 `become` lines) beside; 0.036 in the host's tick GAMEBOARD | yes once made: nature reads the decays at a detector at rest in the laboratory's clock; the law's shell bodies read the betas in their own counts; the neutrons' own clocks are not that reading | predicted; the missing rule: a decay fired by a declared bath | disagrees | a step, at most 2.93 by the pin, against 3.17; the number the run's |
| 8b | 16 of 1024 and 0 behind (DETECTOR, series J2) | yes: two identical detectors in line | predicted; the missing piece: an attenuation by depth (a cross-section) where the law has a filter by residue | disagrees | 0 behind against 1 - epsilon, epsilon = n sigma L below 10^-12 for any detector under a kilometre of ordinary matter (n about 3 x 10^23 per cm^3, sigma about 10^-43 cm^2; a bound computed, kind (2)) |
| 8c | the `nu` content 0 (DETECTOR reading an INPUT: the family table's content) | the content a declared input read back | (3)(a) | not predicted | [a declared content; the oscillation not modelled]; nature's number a bound, said beside |
| 9 | 128 / 256, 0 / 256, 64 / 256; 219 / 256 at 22.5 degrees (DETECTOR) | yes: the pass fraction at one detector behind the polarisers | predicted | agrees | exact at 45 and 90 degrees; +0.0019 at 22.5, the tables' grain 1 / 256; R3's 246, 199, 177 of 256 a re-reading beside |
| 10 | the crowd form's 1.08 (history); the record form's run not completed | not yet | none | NOT YET | keeps its word |
| 11a | q_eff = +1 (COMPUTATION, the growing wall's pin; no key in `WORLD_KEYS`) | no: no click of a brightness; the pin a hypothesis's | (3)(b) and (c) | not predicted | [the wall's growth a hypothesis not built; no click of a brightness] |
| 11b | b = 1 (COMPUTATION, the growing wall's pin) | the observable a click rate, but the pin a hypothesis's and not the law's | (3)(c) | not predicted | [the hypothesis's b = 1 within 0.97 +- 0.10, printed as the hypothesis's, for its run when built] |
| 11c | n = 1 (COMPUTATION, the growing wall's pin) | no: no click of an angular size; the pin a hypothesis's | (3)(b) and (c) | not predicted | [the wall's growth a hypothesis not built; no click of an angular size] |
| 12 | 1.907 under the age word, 1.000 under the presence word (DETECTOR: the ratio of two records' rates, the tick cancelling) | yes | the presence word superseded (record 394) | HISTORY | keeps its word |
| 13 | the centroid shift -1.993 pixel at gamma_PPN = 0 on a coupled world at head (DETECTOR, optical/mass_g0 against control_g0, the pin -1.93 +- 0.5 met; the world declares `optical: 0`, the default, the law's own coupling by `_optical`, `world.py` 3930 to 3956, record 847), half of the gamma_PPN = 1 world's -3.989; series K's 0.000 pixel the suspension-0 worlds' reading, history; under the declared gamma_PPN = 1 the ring's shift 0.731 and the ratio 2.00 (DETECTOR readings of an INPUT) | yes: the star's shift on the plate; the centroid's shift on the far detector's face | predicted for the law as built; the missing rule: gamma from light's own step (the time part alone read); the declared part (3)(a), beside and not counted | disagrees | a factor 2: the time part alone against nature's 1 + gamma = 2, 1.75 arcsec |
| 14 | 1.677 and 1.512 (COMPUTATION from two means of unclosed loops on the host's tick) | not yet: a period is not yet a click; the moving detector's arrival click missing (RUN_14) | none yet | NOT YET READ | keeps its word until read |
| R2, R4 | pins (COMPUTATION); R2's first arrangement not read (RUNS.md section 4) | when run: ratios of one detector's own counts | none | a line beside 4a, 4b, 5b | outside the count (record 1190) |

## Where the two rules of 2026-09-23 differed, and how the procedure decides

- **Rows 4a, 4b, 5b.** The reviewer's placement (record 1196): not
  predicted, kind (1), the instrument missing. The physicist's (record
  1215): a definite number, 1 or the classical form, is a prediction and
  disagrees. Step (2) finds the law's detector reading the observable in
  nature's arrangement; step (3) finds a missing rule and not a missing
  click; step (4) finds the register would have written agrees had the
  number matched. Disagrees, the physicist's; the reviewer's placement
  withdrawn.
- **Row 3.** The reviewer's page as first written: not predicted, kind
  (3), the law's number another diagram's. The physicist's: disagrees.
  Conceded to the physicist: q_0 is kinematic, a property of a(t) alone,
  and the second-order coefficient of z against the light's age is 1 + q_0
  / 2, the same q_0 the luminosity distance reads; step (2) passes, step
  (3) finds a missing term and not a missing click, step (4) passes.
  Disagrees.
- **Row 5a.** "Agrees (a bound met)" as written; the reviewer's page as
  first written: not predicted, the grain read back. The physicist's: Q =
  64 is a constant of the law (`world.py` 348), not a world file's input,
  so 7.6 x 10^-3 is the flight table's own number at the registered grain;
  step (4) decides. Conceded: predicted, disagrees at the registered grain,
  the bracket naming what would agree (Q >= 2^59).
- **Row 6.** "Disagrees" as written, on the loop's opening. Step (2)
  finds no line read, and step (5) allows no disagrees without the number.
  Not predicted; the loop's opening is another observable, 6b, which
  passes (2) and disagrees. The physicist's.
- **Rows 11a to 11c.** Three words as written (not predicted, PASS by a
  pin, not predicted). Step (1) finds the three pins a hypothesis's with no
  key in `WORLD_KEYS`. One status, not predicted; the hypothesis's numbers
  printed as such. The physicist's.

## The count the procedure yields

Of the thirteen observables the law as built predicts (fourteen once row 14
is read; fourteen now if the atom's stability, 6b, is entered), three agree
within tolerance (1a, 2b, 9), ten disagree (1c, 3, 4a, 4b, 5a, 5b, 7b, 8a,
8b, 13; 6b an eleventh), and six are not predicted by construction (6, 7a,
8c, 11a, 11b, 11c); 2a NOT COMPARED until its source is verified; five rows
keep their words (2a, 2c, 10, 12, 14); 1b a control, 1d a consistency check
and 4c a FORM row, outside the count. The rows: 3 + 10 + 6 + 5 + 3 = 27, and
28 with 6b. Rows 4a, 4b and 5b are one finding read thrice (a body's count
at rate 1 at every momentum); they are three observables in the count and
one missing rule. This count is the chief physicist's and the reviewer's
together, after the reviewer conceded rows 3 and 5a (PR #1013); the model
owner decides.

## What this page does not do

No cell of `NATURE.md`, the paper or `CRITERIA.md` moves on it; the model
owner decides the count and the entry of 6b; the writer and the Register
Architect apply the procedure on his word, identically, with the cells of
this table (rows 3, 4a, 4b, 5a, 5b, 6, 6b, 8a, 11b and 13 as they stand
here) and the structure lines before the table rewritten to steps (2) and
(3): the first (the law's clock at rate 1) as it is, the second (the
crowd's history) for 11a and 11c alone with the click named, the third
(declared inputs) without the grain.
The code lines are for checking the kinds, not rules of the law; nothing
of the engine changes, no key, no default. "Matches nature" appears
nowhere else on this page: a row agrees within a tolerance or disagrees by
a number.
