# The read of every src file under the owner's five rules, at 97e5b3fd6

The owner's order of 2026-10-28, 04:3x UTC: "Read all the code, make sure there is no number and only operations on integers, without cosine, sine or circularity that makes phenomena happen. When you find violations, update the Boss that there is a violation, and me; we do not change postulates or laws without my approval." A subagent read each of the 36 modules of src/event_universe whole (6,918 lines, the engine head 97e5b3fd6, nothing edited, no test run), and the Scribe verified its counts against the tree with tools/derivations/open_items/scribe_scan.py and an AST pass; what the Scribe verified is marked **checked**, what rests on the subagent's reading alone **read**. The head has since moved to 42d5448b7 (the one mirror, one new module phase.py): the gate's counts at it stand in SCRIBE-GATE-1.md.

## The five rules and the counts, checked

| the rule | the count at 97e5b3fd6 | |
| --- | --- | --- |
| no number in the code | 24 literals beyond 0 and 1, in 7 files: core/spokes.py 1 (the lattice's 3), gates.py 2, great_clock.py 1, reckoner.py 14, rim.py 2, run.py 3, swings.py 1; the engine proper holds the one | **checked** |
| whole numbers only | 0 float or complex literals, 0 `/`, 0 `float(`, 0 `round(`; the one `pow(a, d, n)` at rim.py:28 (modular, on integers); no import of math, cmath, statistics, random, fractions, decimal or scipy; no numpy trigonometric, exponential, logarithm, root or mean; the word float stands in code only as the string "floats used": 0 (gates.py:368) | **checked** |
| the operators | `**` with a name as the exponent: 10 in the engine, 5 in the readers; `//`: 1 in the engine (core/acts.py:23, Rule3's carry), 28 in the readers; `%`: 2 in the engine (core/spokes.py), 15 in the readers; `.astype`: 2, both in core/rates.py; 349 `int(` calls | **checked** |
| no circularity | the integer circle by name and by search: 25 call sites of the integer roots (largest_below and sine_rim), 75 circular names (sine_rim 22, sine 18, cosine 15, standard_angle 6 ...), a typed quarter-turn table (assembly/cycle.py), the six unit vectors typed in great_clock.py:266 | **checked** |
| no state beyond the Node-clock | the module-level containers features/standard SHORTEST_HANDS and features/stretch LOADS; 6 module-level caches (core/rates.py sides and certified, draw.py kept_pitch, features/stretch rate_zero, hands.py spoke_places and, since 42d5448b7, draw.py kept_mid); 19 id() keys (tick.py 11, draw.py 1, great_clock.py 4, reckoner.py 3); reads of the great clock's log by acts (striking.py, tick.py) | **checked** |
| the run is not reproducible by its clock | run.py:315 and :335 write the wall clock (time.monotonic_ns) into the chart's rows | **checked** |

## What the readers hard-code, read

The readers read a finished chart and produce nothing, yet several verdicts cannot fail or are typed:

- run.py:68 logs `senses=[-1, 1]` in every birth line and reckoner.py:166-173 computes the charge as `senses[k] * (key // 2)` from that constant, not from the state; rows 17, 65, 70, the conservations row and the Bell row's E = -1 follow from it (**checked** at run.py:68).
- gates.py:368 asserts `"floats used": 0` (**checked**): asserted, not measured.
- predicates.py:296-309, row 56, takes nature's band 4 < S^2 <= 8 as the criterion for SHOWN (**checked**).
- symmetries.py rows 71, 72 and 73, strikes.py and predicates.py rows 15 and 47 test identities that hold by the algebra of the books' slack (`taken + remainder_was - remainder == booked`), so they cannot fail; the CPT row holds identically (read).
- gates.py row 25: entropy as a sum of bit lengths, never falls (read); great_clock.py row 5 compares two coded sums, a lift and the load pull 2 sqrt(X / Gamma) (read); predicates.py confinement tests against a typed third of the charge (read).

## Where a phenomenon is made by a formula that holds it (read, the Scribe re-read E1, E3, E5, E8 and E19)

| | where | what |
| --- | --- | --- |
| E1 | bobs.py:100-126 | Born's rule and the collapse as a formula: the up twin is picked iff `drawn[0] * sum(sweeps) < drawn[1] * sweeps[0]`, the picked twin renormalised by a root |
| E2 | draw.py:20-46, striking.py:44-48 | a pseudo-random number from the fine teeth of a clock and its six neighbours picks the twin and the species |
| E3 | features/standard/__init__.py (whole), readings.py:36-54, meshes.py:47-61, 91-132 | a (cos, sin) circle by a Chebyshev recurrence applied as a rotation across every Mesh |
| E4 | assembly/cycle.py:21-45 | the quarter table, a quarter turn a tick typed |
| E5 | assembly/setting.py:101-184 | raised_cosine, rim_point (cos k = (rim^2 - 2 h^2) / rim, sin k by a root), angle_of, running_rotation: the dispersion relation as a closed form |
| E6 | hands.py:128-143, regulation.py:28-32 | cosine_count: the count K with cos omega_0 = pinion / rim, by search |
| E7 | meshes.py:111-132 | a rotation by the tangent-half-angle triple |
| E8 | core/rates.py:41-48, features/stretch/__init__.py:37-96 | the rate p0(c) = Gamma (1 - 1 / Gamma)^c as an exact exponential table and its inverse by search ("no logarithm") |
| E9 | core/rule3.py:57-61 | the mesh factor (Gamma - t)^2 / Gamma^2, a closed form |
| E10, E11 | core/rule3.py:96-110, tick.py:246-257, regulation.py:15-25 | the regulator's drive and the stress tensor as the source |
| E12, E13 | tick.py:183-244 | Pauli's sigma coupled to the curl, the source kicks |
| E14, E15 | core/rule3.py:113-115, clock.py:59, 94-95 | the winding as 3 T sin omega; the light's drift as a floor root of the key |
| E16, E17 | striking.py:127-157, unspring.py:40, assembly/setting.py:93-98 | the exclusion principle as refusals; the pair always born at senses -1 and +1, the + child's end set by the twist's sign |
| E18 | unspring.py:192-282, unwind.py:65-82 | the books balanced by a plug (`slack = slack_was + fall - tallied`, a recoil written `-p * rate * rate`) |
| E19 | clock.py:57-58, core/rates.py:25-27 | every hand a point on den's circle, sine_rim a floor root of rim^2 - pinion^2 |

## The reads beyond one Mesh, and the step's other acts, read

`hands.wind` over a window reaches two Meshes at 7 call sites (unspring.py:62, 68, 116, 137, 296; striking.py:288; bobs.py:170); train_twists reaches two (striking.py:65, 75); lay_window and lay_wind reach up to three (striking.py:266-290); whole-lattice scans stand at unspring.py:133-134, tick.py:131-135 and :311, striking.py:79, bobs.py:47 and clock.py:165. The tick's step holds 26 acts beyond Rule3's one carry (the loads, the readings and their clamps, the mesh factors, the Pauli drive, the sources, the regulator's clamp, the unwinds, the turnover, the striking), listed in the subagent's table of tick.py's lines 97 to 326.

## For the Boss and the owner

The departures are the gate's baseline (scribe_scan_baseline.json, 209 hits at 42d5448b7) and the register's R5; the Scribe's recommendation stands (ledger row 294): the pair's three integers and the setting's weights and angle digits as data in the universe and setting files, so that the engine computes no sine and no root; the formulas that hold a phenomenon (E1, E3, E5, E8, E19 above all) are the owner's to weigh against the law **No circularity that makes a phenomenon happen**; no postulate or law is changed by this read.

## Not read

Data files (the pieces and universes), the tests, the tools and the documents; no runtime value or verdict was run; the numbers made at run time (by len or by bool arithmetic) were found by reading and by an AST pass over the module-level names, not by a full flow analysis.
