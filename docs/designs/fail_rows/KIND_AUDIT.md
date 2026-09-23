# The kind audit of the confrontation register: what number each row compares, of what kind, from which click line (the chief physicist, 2026-09-23)

The order (the Boss, 2026-09-23, on the model owner's words of the same
day as the Boss recorded them, records 1166, 1173 and 1175: "some
experiments ran not on the clicks but read the board directly"; "for some
rows we do not have nature's measurements, or the instrument in the
model"): one row per row of `docs/NATURE.md` and per line of the paper's
Table 3 (`paper/general_formula/main.tex`, `tab:nature`), with the number
compared, its kind, the detector's click line and the tool it comes from,
the verdict as written, the verdict the kind allows, and the kind of what
is missing where something is. Docs only, no run, no number moved: this
file is a proposal the physics-rule reviewer reads and the Register
Architect folds into `NATURE.md`'s tally block (one writer per shared
interface; nothing here edits `NATURE.md`, the paper or `CRITERIA.md`).
Base commit `863cf5fd` (`origin/main`, "Merge pull request #970").

**The kinds** (HIGHLIGHTS 5.4 item 9; RUN_8BC.md's head): DETECTOR, "a
click, a record's moments, a body's own record, an external thing's
reading, as declared in the world file, the only kind reality has and the
only kind compared with nature or pinned"; GAMEBOARD, the host's view (a
tick, a state column, a body's position on the board, the flight table's
arrivals, the lattice's clock), a diagnostic, never compared with nature;
COMPUTATION, arithmetic on readings or a number the algebra gives in
closed form with no run; CONVERSION, an Outside number from a detector's
counts by a named reading; HOST, a cost of the machine. Beside the kind
this audit names the FORM of a DETECTOR number, since the owner's word
"under the one click" turns on it: RECORD, the one click (the amplitude
law: one `gather` per record, its `chosen` cell the click); CROWD, a
declared detector's record line over many rays (the `record` of a `wave`
or `beam` set, the pointer's square, or a counter's `click` lines on rows
of no record); BORDER, the border's `click` lines (a `lifetime`, a face);
BODY, a body's own record lines (`become`, `contact`, `read`).

**The rule applied** (the Boss's order, with one addition of mine marked
R3 for the reviewer):

- R1. A DETECTOR number keeps its verdict as written.
- R2. A GAMEBOARD number (the host's view of a run) makes the verdict NOT
  YET until a click reads it; the old verdict is labelled a board reading
  kept as history.
- R3 (mine, for the reviewer). A COMPUTATION in closed form from the law
  with no run (a pin, a derivation's number) is the law's own number,
  which the new form of the table (record 1166) prints in every row; it is
  not a measurement, so its row's status word is "the law's number, no
  run" with the disagreement or agreement stated by the algebra, and the
  run that would make it a DETECTOR reading named in the missing column.
  Without R3 the pinned rows (4a, 5b, 11a, 11b, 11c) would fall under R2
  by default, which mislabels an algebra as a board reading.

**The three kinds of missing** (record 1173, the owner's word): (i)
INSTRUMENT, the model lacks the detector or the key that would read the
quantity; (ii) MEASUREMENT, nature's number is a bound or a fitted
parameter, not one measurement, or its source is not verified; (iii)
CLICK DEFINITION, the quantity has no click reading defined yet. A row may
carry two. A fourth case appears below and is none of the three: the
number compared is a declared INPUT of the world (7a, 8c, 13's gamma),
which the new form's third status names as "not predicted by the law as
built" with the missing rule as the missing piece.

## 1. The audit, row by row

The columns: the number compared (the model's side); its kind and form;
the click line and the tool; the verdict as written in `NATURE.md` / in
the paper's Table 3 (a dash where the row is absent there); the verdict
the kind allows under R1 to R3; the missing kind.

| Row | The number compared | Kind (form) | The click line; the tool | As written: NATURE / the paper | The verdict the kind allows | Missing |
| --- | --- | --- | --- | --- | --- | --- |
| 1a | S = 176 / 64 = 2.75 (the cells 27, 5, 5, 27 per setting) | DETECTOR (RECORD) | the `gather` lines' `chosen` (oA, oB) per record over 64 births per world; `tools/amplitude_path.py --check`; `tests/test_amplitude_pair.py` replays at head | PASS / PASS | keeps PASS (R1) | none (Hensen 2015 a measurement) |
| 1b | S = 2 exactly | DETECTOR (CROWD: the counters' `click` lines under each party's phase window, rows of no record) | the counters' clicks; `tools/bell_chsh.py` | FAIL / FAIL | keeps FAIL (R1); the row is the crowd form's window with the record form's 1a beside it; whether it stays a row or a history line is the owner's word | none |
| 1c (the paper only) | the serial correlation 15 / 16 under a constant setting and -1 / 16 under the period-3 cycle over 192 births; the marginals 96 / 96 | DETECTOR (RECORD: the gathers' order) | the gathers' sequence; the order-channel run of 2026-09-22 as the paper cites it | - / FAIL | keeps FAIL (R1); the cycle N / 2, 0, 0 at -5 / 16 is COMPUTATION, labelled so in the paper | none |
| 2a | the clicks' visibility 0.966 over the named bright and dark pixels; Pearson 0.891 | DETECTOR (RECORD: the gathers per pixel over the records 1 to 4096) | the `gather` lines' `chosen` per `screen_y`; `tools/amplitude_path.py --check`; the pin `slits_huygens_pin.py` met bit for bit | FAIL / FAIL | keeps FAIL (R1); the fan's grain share of the 0.014 is a COMPUTATION, section 2 of this file | (ii) the nature side: the paper itself notes the register's 0.98 is a Mach-Zehnder reading (Grangier 1986) and names a two-slit source (Jacques 2005, 0.94) "to be verified" |
| 2b | the clicks 64 / 0, the visibility 1.000 | DETECTOR (RECORD) | the gathers' chosen port; `tools/amplitude_path.py --check`; the tests replay | PASS / PASS | keeps PASS (R1); the offers 1681 / 1682 are GAMEBOARD, labelled so already | none |
| 2c | the power's window [1.917, 2.012) | COMPUTATION on DETECTOR (RECORD: the click cells read back) | the gathers of `mz_345` and the pair; `tools/amplitude_path.py --check` | NOT COMPARED / NOT COMPARED | keeps NOT COMPARED (an implementation gate, as both say) | (iii) no click reading of kappa: a three-opening world is not registered |
| 3 | q = -0.108 (coasting), the second-order coefficient of z(tau) with H free over the window [300, 400) | DETECTOR (CROWD: the centre `wave` set's `record` lines with `reads: "age"`, the pointer's turn, the click ages) for z; the time axis tau the host's tick, which the paper labels GAMEBOARD (record 768 as the paper cites it) with "the detector's own pulse-and-return clock NOT READ"; q a fit (COMPUTATION) on them | `tools/hubble_stars_readings.py`; `record/expectations.json` | FAIL / FAIL | NOT YET for the reading (R2: the time axis is the host's tick by the paper's own label; CRITERIA.md's "DETECTOR (the record lines and the click ages)" and the paper's label disagree, the reviewer's to settle); the FAIL kept as a board-clocked reading, history. The disagreement itself stands by the algebra with no run (DERIVATIONS_BEAM 15.4: q = 0 Milne, q > 0 with gravity, no term with q < 0), the law's own number (R3) | (i) the detector's own clock (the clock audit's form: a ratio of two click counts at the detector); (ii) nature's q_0 = -0.53 +- 0.01 is a fitted parameter of the Hubble diagram and the CMB, compared here with a fit |
| 4a | the lifetime ratio 1 (pinned, no run); the re-read under `covariant-readings-v1`: the electron products' face clicks at 369 and 345 (DETECTOR), the muon's 64th self-creation at 70 and 124 (`become` lines) | COMPUTATION (the pin) / DETECTOR (BORDER: the +x face's clicks) and the `become` lines (BODY by 5.4's letter, "a body's own record"; GAMEBOARD as NATURE labels them) | `tools/covariant_readings.py`; series S's `expectations.json` | FAIL (pinned; the run not made); PASS under the key within its domain / - | the pinned FAIL is the law's number, no run (R3); under the key the face clicks are DETECTOR and keep their PASS within the domain (R1); the `become` tick is the host's, the body's `counted` at it the body's own | (i) a moving body's clock read at a detector at the muon's speeds (the cart with a click, in build); nature's 29.33 a measurement |
| 4b | z = 0.2636 at beta = 0.2674 (the star's pointer over the late window); under the key z = 0.3674 against the pin 0.369 (not against nature) | DETECTOR (CROWD: the centre's pointer) with the time axis the host's tick (GAMEBOARD by the paper's label, as row 3) | `tools/hubble_stars_readings.py`; `tools/covariant_readings.py` | FAIL / FAIL | as row 3: NOT YET for the reading until the detector's own clock (R2), the FAIL a board-clocked reading kept as history; the disagreement stands by the algebra (DERIVATIONS_BEAM 4.3: the rate one at every speed, the classical z), the law's number (R3) | (i) the moving detector or clock (the cart); nature's z (Botermann 2014) a measurement |
| 5a | the pace 0.5774 to 0.5818 over the primitive directions within 64 | COMPUTATION (the flight table); behind it series Q's 290 of 290 face clicks at the derived tick (DETECTOR, BORDER) | `tools/c_measured_readings.py`; the paper's `checks/light_speed.txt` | BOUND / BOUND | keeps BOUND (a bound on Q from a computation; the detector reading confirms the table) | (ii) nature's number is a BOUND (Nagel 2015, Herrmann 2009, "to verify against the source") |
| 5b | the arms' round trips 1.375 along and 1.140 across at beta = 0.4297 | COMPUTATION (a host script on the flight table, no run) | none (DERIVATIONS_BEAM 12.3) | FAIL (pinned; the pair in motion not run) / - | the law's number, no run (R3): the disagreement (no contraction) by the algebra; no detector reading exists | (i) the pair in motion (12.4) not built; (ii) nature's number a BOUND (Michelson-Morley's modern form) |
| 6 | no line registered; the paper: the loop opens at 3407 intervals (series H, DETECTOR), the levels by algebra (COMPUTATION), the lines NOT COMPUTABLE | none for the ratio; DETECTOR (BORDER: the escape face click) for the loop's opening; COMPUTATION for the ladder | `tools/bohr_readings.py` | NOT YET / FAIL the law's (the loop opens), the lines NEED A NEW RULE | keeps NOT YET for the ratio; the loop's opening is a DETECTOR FAIL of another claim (the atom's stability) and keeps (R1) | (iii) no click definition of a line's ratio (a transition's click); the missing rule named by the paper |
| 7a | the escaped content 4 of 3677, 0.109 percent; the mass read 3673 | DETECTOR (BORDER: the bond's `lifetime` click lines; the books' `escaped` GAMEBOARD, a check) | no shipped tool: the README reads `events.jsonl`, `run.json`, `state.json` | BOUND / BOUND on a declared input | keeps BOUND (R1) | the fourth case: the binding per nucleon is an INPUT (record 106; the law derives no binding); the missing piece a rule, none of (i) to (iii); nature's 0.1185 percent a measurement (AME 2020) |
| 7b | the ratio 2.0 (four border clicks against two) | DETECTOR (BORDER) | the same | FAIL / FAIL | keeps FAIL (R1); also the law's number by the algebra (the give once per body, linear) | none |
| 8a | NATURE: the width over the median 0.036; the paper: a step of width 0 (the 64 clicks of content 3, DETECTOR), the 0.036 to 0.13 "GAMEBOARD, the lattice's clock, counted in no criterion" | the step and the line: DETECTOR (CROWD: the shell's `beam` set's 64 beta clicks; BODY: each neutron's `become` at its key); the width 0.036: GAMEBOARD (the click ticks in the lattice's clock, the reviewer's correction on PR #777 as CRITERIA.md records it) | `tools/weak_readings.py` | FAIL: 0.036 against 3.17 / FAIL: a step, width 0 | NATURE's number 0.036 is GAMEBOARD: NOT YET for that number (R2), the factor 88 a board reading kept as history; the paper's form keeps FAIL (R1: the step and the line are DETECTOR). Record 1166 places "8a's width" under disagrees; by R2 the width waits on the reading behind it, the reviewer's to settle | (i) and (iii) the detector reading of the width (a lamp at the shell counted between the clicks) NOT MADE; the registered J1 run predates the one flight wall (the paper), the redeclaration after the paper |
| 8b | 16 of 1024 at the first reader, 0 behind; the far detector 699 of 711; RUN_8BC's re-read under `massive_rows`: 0 of 1023, the whole beam at x = 14, the far detector 0 | DETECTOR (CROWD: each reader's own `click` and `pass` lines on rows of no record; under `massive_rows` the readers' lines on record rows) | `tools/weak_readings.py`, `weak/expectations.json`; `run_8bc_readings.py` | FAIL / FAIL | keeps FAIL (R1), in both forms | (ii) nature's "about 1" is a statement of the neutrino's penetration, no measurement cited for the ratio of two detectors in line; the row needs one named source |
| 8c | the `nu` content 0, an input | none (nothing measured) | - | FAIL (refuted) / a declared input refuted | the fourth case: an INPUT; the new form's third status "not predicted", the missing piece a content above 0 and an oscillation sector | (ii) nature's number a BOUND (the heaviest state at least 9.8 x 10^-8 of the electron's, PDG 2024, KATRIN 2022) |
| 9 | 128 of 256 at 45 degrees; 219 of 256 at 22.5; the chain 187 / 32 / 5 / 32 | DETECTOR (RECORD: the gathers' pass cells) | `tools/amplitude_path.py --check`; `tests/test_amplitude_malus.py` replays | PASS / PASS | keeps PASS (R1) | none |
| 10 | 1.08 (4.99 / 4.619): the width of the screen's cumulative `record` in sin theta, smoothed by a moving mean over five pixels, times w over lambda | DETECTOR (CROWD: the 161 `wave` pixels' cumulative `record`, the pointer's square over rays; not the one click) with COMPUTATION on it (the smoothing, the width, the product); NATURE keeps it as history | `tools/heisenberg_readings.py` | NOT YET under the one click / - | keeps NOT YET; the number 1.08 a crowd-form reading kept as history, as the row says; the pins under the one click are written before the run (RUN_10.md, PR #984: 0.925 at w = 27, 0.879 at w = 9, COMPUTATION) | (iii) was the missing kind; the click definition now exists (the `gather` per pixel over the records 1 to 4096); the run pending |
| 11a | q_eff = +1 (a derivation's pin) | COMPUTATION (`far_lamp_map.out`; no run; the key `expansion-v1` not built) | none | FAIL (pinned; the run not made) / - | the law's number, no run (R3) | (i) the key `expansion-v1` not built; (ii) nature's q_0 a fitted parameter |
| 11b | b = 1 (the stretch equals 1 + z) | COMPUTATION | none | PASS (pinned; the run not made) / - | the law's number, no run (R3): a "PASS" before a run is the algebra's agreement, not a measurement's; record 1166 calls it a pin | (i) the same key; nature's 0.97 +- 0.10 a measurement |
| 11c | n = 1 (the surface brightness (1 + z)^-1) | COMPUTATION | none | FAIL (pinned; the run not made) / - | the law's number, no run (R3) | (i) the same key; (ii) nature's exponent is itself fitted from surface-brightness data (the row's source column) |
| 12 | the ratio of the two clock rates 1.907 (the age word) and 1.000 (the presence word) at 3 and 6 Links | DETECTOR (CROWD: the lamp's light read at the detector's `record`, 1 + z from the pointer's turn in two windows) with the time axis the host's tick (GAMEBOARD by the paper's label, "the detector's own pulse-and-return clock NOT READ") | `examples/events/clock_word/read_runs.py`, `readings.json`, replicated | PASS under the age word, FAIL under the presence word / HISTORY, PENDING the weak-field re-read | HISTORY, as the paper says (the law before the generic entry of 2026-09-22); the time axis the host's tick: NOT YET for the reading until the detector's own clock (R2); the form 1.907 against 2.00 with no uncertainty stated meets the paper's PASS criterion nowhere, as the paper says | (i) the detector's own clock; the redeclaration in the weak field (series T alone, the chief physicist's parked task) |
| 13 | the ratio 2.00 of the centroid shifts at gamma 0 / 1 (series K's optical pins); the paper: the deflection 0.000 pixel by the law as built (series K), the ring's constant 3.655 .. 3.918 against 4 (flow-link-v1) | DETECTOR (CROWD: the screen's `wave` pixels' centroid; the ring's mean radial shifts) for the shifts; the constants COMPUTATION; `tools/optical_readings.py` is a GAMEBOARD diagnostic by its own docstring, never a reading | `tools/lensing_readings.py`; `tools/flow_link_readings.py` | NOT COMPARED (gamma an input) / FAIL the law's (0 against 1.75 arcseconds), the constant does not close, gamma an input | keeps NOT COMPARED for the ratio (it reads the declared input back); the paper's FAIL of the law as built (0 deflection) is DETECTOR and keeps (R1) | the fourth case: gamma an INPUT of kind 2; the missing piece a derivation of the space part from the law |
| 14 (the paper only) | T(24) / T(12) = 1.677 from the means of the recurrences of x of two unclosed loops; the controls' clicks at x = c_x + r; the escapes through the faces at 1208 and 2452 | DETECTOR (BORDER: the face clicks; the controls' clicks at the detector line) for the clicks; the "periods" COMPUTATION from two means of unclosed loops' spacings; the mean radii CONVERSION, as the paper labels them | `tools/orbit_lamp_readings.py`; series D3's `expectations.json` | - / FAIL as read under the one constant; the ratio not compared with nature; the inverse square in space NOT MADE | keeps as the paper states: not compared with nature (no loop closed); for the claim NOT YET | (iii) no click definition of a period yet (a closed loop's recurrence at a detector, the clock audit's form); the inverse square in space NOT MADE |

**The readings the paper names NOT MADE** (CRITERIA.md's closing table),
each without a number and so without a kind: the two-way c after a
detector; the inverse square's decisive reading (a closed orbit's period at
two radii, form B); the moving detector's one-way ratio and the velocity's
quantum (the cart with a click, in build); the detector reading behind
row 8a's width (a lamp at the shell counted between the clicks); and the
far lamp's three rows (11a, 11b, 11c: an engine key not built). All are
(i) INSTRUMENT or (iii) CLICK DEFINITION; none is a verdict.

## 2. What the audit says, in five lines

1. **The rows whose number is a click of the one record (RECORD form) keep
   their verdicts untouched**: 1a, 1c, 2a, 2b, 9 (and 2c's window as a
   read-back). Their tool is one, `tools/amplitude_path.py --check`, and
   the tests replay them at head.
2. **The rows whose number is a detector's line in the crowd form keep
   their verdicts by 5.4's letter** (1b, 7a, 7b, 8b, 13's shifts, and the
   BORDER and BODY lines of 4a, 6, 14), with the form named beside them;
   the owner's "under the one click" is a separate word, which only row 10
   carries today and rows 1b and 8b could carry beside their crowd rows.
3. **Three rows rest on the host's tick for their time axis, by the paper's
   own label** (3, 4b, 12: "that tick the host's interval, GAMEBOARD; the
   detector's own pulse-and-return clock NOT READ"): under R2 their
   readings are NOT YET until the detector's own clock reads them, the old
   verdicts board-clocked readings kept as history. Their disagreements
   with nature do not rest on those readings: for 3 and 4b the algebra
   gives the law's number with no run (q >= 0; the classical z), which the
   new form prints; for 12 the paper already says HISTORY. One more number
   is GAMEBOARD by CRITERIA.md's own record, 8a's width 0.036 (the
   lattice's clock), and waits on the reading behind it; the paper's form
   of 8a (a step, width 0, DETECTOR) keeps its FAIL.
4. **Five rows have no detector reading at all and are the law's own
   numbers by pins** (4a as pinned, 5b, 11a, 11b, 11c): under R3 their
   status is "the law's number, no run", the missing instrument named (the
   cart's clock; the pair in motion; the key `expansion-v1`). 5a is a
   BOUND from a computation with a detector reading behind it.
5. **Three rows compare an input, not a prediction** (7a's binding, 8c's
   content, 13's gamma): the new form's third status, the missing piece a
   rule; and three rows compare with a nature number that is a bound or a
   fit (5a, 8c, 3 and 11a's q_0, 11c's exponent) or with a source the paper
   itself marks to verify (2a's two-slit source, 5a's bounds), kind (ii).

Nothing here moves a cell. The reviewer decides R3 and the two labels
where the register's own documents disagree (3 and 4b: CRITERIA.md's
DETECTOR against the paper's GAMEBOARD tick; 8a's width: record 1166's
"disagrees" against CRITERIA.md's GAMEBOARD); the Architect folds the
outcome into the tally block; the writer into Part 7.

## 3. Row 2a's fan-grain share (COMPUTATION, no run)

The register's row 2a names its cause as "the fan's grain" (the width-48
fan, whose smallest angle off the axis is 1.22 degrees, the pixel at L =
44 Links 1.30 degrees). `row_2a_fan_grain.py` beside this file (its
output `row_2a_fan_grain.out`) runs the pin machinery of
`slits_huygens_pin.py` (the same integers as the click's; it reproduced
the registered run bit for bit, checked again here: wall 882, screen
1711, faces 1503, the visibility 0.9659) on the registered world with the
openings' fan alone replaced, and reads the clicks of the records 1 to
4096 for each fan:

| the fan | directions | the clicks' visibility | the weights' visibility | Pearson |
| --- | --- | --- | --- | --- |
| registered: width 48, weighted by angle | 1327 | 0.9659 | 0.9663 | 0.891 |
| weighted by angle, width 110 | 6907 | 0.9647 | 0.9685 | 0.914 |
| weighted by angle, width 220 | 27351 | 0.9680 | 0.9693 | 0.920 |
| selected one per 0.25 deg, width 48, unweighted | 641 | 0.9567 | 0.9519 | 0.859 |
| selected one per 0.25 deg, width 330, unweighted | 686 | 0.9701 | 0.9650 | 0.917 |
| selected one per 0.15 deg, width 330, unweighted | 1142 | 0.9654 | 0.9678 | 0.914 |

Every number is a COMPUTATION on the declared world (nature's 0.98 and
the ideal 1 are the things compared with; the only DETECTOR reading is
the registered run's, unchanged). What it says: the fans without a hole
give 0.965 to 0.970, so the fan's grain accounts for at most 0.004 of the
shortfall 0.034 to the ideal, 12 percent of it, and for at most a third of
the 0.014 to nature's 0.98; no fan tried reaches 0.98. What it would
change: the row's cause line ("the cause named: the fan's grain") is not
supported beyond 12 percent of the shortfall and should name the grain as
a minor share; the Pearson with the two-source cosine rises with the
finer fans (0.891 to 0.920), so the correlation pin 0.96 that the row
records as missed is closer but not met. What it would not change: the
verdict, FAIL against 0.98, under every fan tried. What it points at: the
first record's exact weights already carry the floor (the weights'
visibility 0.966 equals the clicks' 0.966 on the registered fan), so the
residual weight at the cosine's dark pixels is in the record's phases at
the click, not in the ladder's rounding or the fan; the next cause to
test by the same script, before any run, is the phase grain N = 64 and
the pixel's width against the path differences at the dark pixels (the
world at N = 128 or the screen farther, each a declared world validated
at load). Not started; the Boss's to order or drop.

## 4. Links

- [NATURE.md](../../NATURE.md): the rows as written; its tally.
- [CRITERIA.md](../paper_criteria/CRITERIA.md): per row "what is measured
  (the click line and its tool)", the base of the third column.
- The paper's Table 3 (`paper/general_formula/main.tex`, `tab:nature`):
  the kinds already printed in its cells (DETECTOR, GAMEBOARD, COMPUTATION,
  CONVERSION), which this audit reads back row by row.
- [The clock audit of 2026-09-22](../clock_audit/AUDIT_2026-09-22.md): the
  form of a time reading, a ratio of two click counts at a detector; the
  rows whose time axis is the host's tick.
- [RUN_8BC.md](RUN_8BC.md), and `RUN_10.md` beside it once PR #984
  (branch `row-10-opening`) merges: rows 8b and 10 by the algebra, the
  kinds of every number in their pins.
- HIGHLIGHTS 5.4 item 9, the three kinds of a number; the owner's words of
  records 281, 1139, 1166, 1173 and 1175 as the Boss recorded them.
