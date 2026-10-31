# The hostile auditor of main b1a50bb33: no fake, no hidden number (2026-10-31)

(Written by the Boss from the auditor's hand-back, the auditor's harness having refused the write; the text is the
auditor's, shortened only in its layout. Its evidence is in this folder: gate_summary.txt, gate_all.txt,
indep_scan.py, indep_hits.txt, perm_check.py, perm_test/. Nothing in the repository was edited, committed or pushed.)

VERDICT on main b1a50bb33: NOT CLEAN. No FAKE, eight FORBIDDEN, seven NAMED-OPEN, the rest LAWFUL.

The core code is clean: src/tensor24 and tools/tensor24_*.py hold no float, no number beyond 0 and 1, no true
division, no circular or root call, no // or % outside algebra/carry.py; the Node-clock (engine/step.py, contract.py,
mesh.py) holds no if, loop, mask, clip, min, max or bound. What makes the tree unclean: the approved world files carry
a cosine and a root by construction (F4, F5); probes hold two roots by bisection, one by a linear search and sine
values typed as references (F1 to F3); two probes declare trains in code (F6); the decoder hides a count behind a
label tuple's length (F7); the CI tools still hold floats an earlier audit found (F8). The gate passes F3 to F6 and
most of F2, because it reads names and shapes.

## 1. How it was checked

- The gate over the whole tree (--base origin/engine-5.0-test): 2 refusals and 15 notes, as the Boss's run. Its --all
  mode: 70 hits (INDICATOR 12, DOCLAYER 4, LENGTH 6, KEYS 41, DECLARE 5, PIN 2); every hit read. (--all does not run the
  probe rules PROBE, DIVIDE, SEARCH, SINEWORD on unchanged probes.)
- An independent AST scan of all 120 .py files (3,623 hits): literals beyond 0 and 1, floats, /, //, %, divmod, **,
  shifts; forbidden imports; calls of roots, circular functions, round, float, pow, mean; float dtypes; Enums; len() of
  displays and constants; circular and root words in names, strings and comments.
- Reading beyond the gate: all 27 modules of src/tensor24, all of tools and the tests; the five worlds' 15 files value by
  value and the lays that made them; a sweep of all 73 probes for recurrences, Pell or Pythagorean seeds, searches, typed
  tables, typed decimals and trains in code.
- The four past audits on scribe-5, and NOT_CLOSED.md, FRAMES.md and PLAN.md's owner's list.
- Two readings per finding (the code read plus a computation or a run): the live world's 144 before-counts recomputed and
  49^2 - 6 x 20^2 = 1 checked; the typed decimals recomputed from the sine formula; the shipped world run as shipped and
  with its metric's kinds reordered (both reach 540e503cad44, the run back exact); git blame dating each probe line
  against decision 41 (2026-10-30, 02:1x UTC) and the owner's word (17:20 UTC).

## 2. FAKE

None found: one test assert compares against a number beyond 0 and 1 (test_the_tensor24_load.py:76) and restates the
law's form; no golden file; the decoder's verdicts and run.py's exact are computed; no probe prints a verdict it did not
compute; the live world's speed is the act's (the lay sets only the pulse's direction).

## 3. FORBIDDEN

- F1. A root found by bisection: tools/derivations/open_items/derive/david_open/node/g3_strengths.py, reach() lines 194
  to 212 (the gate's :200) and edge_swing() lines 420 to 437 (:427): `hi *= 2`, then `mid = carry(lo + hi, 2, 0)[0]`.
  Added at 1ae9a6c29 (08:45 UTC), after decision 41 and before the 17:20 word. Law: decision 41; "Sine is forbidden".
  Fix: delete the probe, or remove both searches with the readings that need a root.
- F2. Sine-formula values typed as the reference: g3_strengths.py:498 ("4 sin^2 (omega / 2) = spring / W gives 4,000
  omega / pi = 63.7 and 319.2"), :291, :332 and :393 ("the mass 63.7"); derive/david_open/node/g3_kinds_and_parts.py:88
  ("spring g n gives 63.7, 3 g n 110.3"): decimals worked off the code from an arcsine (recomputed: 1/400 gives 63.7,
  3/400 gives 110.3, about 1/16 gives 319.2). Law: line 102, line 100, "Sine is forbidden". The gate shows only :498 (a
  SINEWORD note). Fix: print the measured counts alone, or delete both probes.
- F3. A root by a linear search, and typed tables, in a dead probe: derive/david_open/tables/tb_tables.py:174 (`g =
  next(g for g in itertools.count(1) if 2*g*g*(2*gamma-1) > wall)`, an integer square root by search, printed as "the
  least square"); lines 37 and 38 type G = [[2,-1],[-1,2]] and 3 G^-1 = [[2,1],[1,2]]. It calls kinds.projector, which
  main lacks. Added at a6312ed1f (06:06 UTC). Law: decision 41; no table. Not seen by the gate. Fix: delete it.
- F4. A cosine by construction laid into an approved world (the well): derive/boss/well_lay/lay.py:49 to 59 (mode) and
  examples/tensor24-well/setting.json (light's first part). The "ring's whole standing mode" starts from values = [2, 1]
  and runs values.append(values[-1] - values[-2]): the Chebyshev recurrence at 2 cos(theta) = 1, giving 2, 1, -1, -2,
  -1, 1, exactly 2 cos(60 x degrees); chosen "as the longest" of the ring's whole modes, the angles where the cosine is
  whole, so picked for its angle; the setting lays 2000 (c(x) + c(y) + c(z)), crest 12000; the lump stands because it
  sits on this cosine eigenmode. Entered at 3bda0613d, 17:36 UTC, sixteen minutes after the owner's word. Law: line 102
  (the lay of a state holds no circular function, by any construction that finds one); "Sine is forbidden". It has come
  back: SCRIBE-AUDIT-97E5B3F-1 item E3 found the same device in the old engine. FRAMES.md 11 claims the well's lay holds
  "no root and no sine". Not seen by the gate, on no list. Fix: lay the lump with no mode (for example the polynomial
  bump the pulse already uses, at rest) and regenerate setting.json, or put it to the owner beside NOT_CLOSED 5.
- F5. A root by a Pell pair in three approved worlds, the before slot at 20/49 Meshes a round: well_lay/lay.py:42 and
  :164, mesh_lay/lay.py:38 and :76 (`NUM, DEN = 20, 49`, before = ((DEN - NUM) now + NUM next) div DEN); the pulses in
  tensor24-well/setting.json and tensor24-mesh/setting.json; tensor24-live/setting.json (all 144 before-counts equal
  ((49 - 20) now + 20 next) div 49). 20/49 lands on the lattice's light speed 1/sqrt 6: (49, 20) solves
  49^2 - 6 x 20^2 = 1, the Pell solution after (5, 2); the live world's commit (77fd6f606) compares its pulse with
  "1 / sqrt 6 = 0.4082"; the same device as tonight's PELL pair for cos 30 degrees. The live world's lay script is not
  in the tree. Law: decision 41 (no root, not outside the logic either); a number computed to land on a wanted value.
  Not seen by the gate. Fix: lay each pulse at rest (before = now) so it runs both ways at the act's own speed, or let
  the act make the before slot; commit the live lay and regenerate the three settings.
- F6. Trains declared in a probe's code: derive/boss/hand_per_quantum/probe.py:70 and 71 (19:31 UTC; hands laid as
  {"name", "kinds": ["T1"], "part": 1} with no pinion, the metric found by len(t["kinds"]) > 1, a role read by shape);
  derive/david_open/ladder/l2_ladder_on_the_act.py:22 to 34 (2026-10-29; three trains and two coupling rows declared,
  an API main no longer has; the gate's DECLARE at :37 and :38). Law: no train declared in code; decision 35; law line
  1704. Fix: read worlds from files and roles from the loader's flags; delete l2_ladder.
- F7. The star's two senses behind a label tuple's length (decoder): src/tensor24/decoder/records.py:41 and :171, WAYS =
  ("+", "-") used only in len(sides) * len(WAYS) to count the board's Spokes. Law: no number behind a name; counts from
  the structure (the owner's question on enums). A LENGTH note. Fix: the runner writes the Spokes into the header from
  the star and the decoder reads them, or drop the check (only Whole records need it, and no run writes them).
- F8. Floats in the tools, found before and never removed: tools/check.py:27 (5.0), :30 (30.0), :55 and :121 (float(),
  round()), CI timings in seconds; tools/documents_gates.py:143 and 144 (round(float(v), digits)), a dead path. Law:
  line 100 ("No float anywhere in the system ... the tools"). SCRIBE-LAW-AUDIT-2 section D found these. Fix: integer
  milliseconds and integer bounds; delete the dead path.

## 4. NAMED-OPEN

- N1. record/schema.py:25, MINOR = len(ADDED) = 3 (the owner's list, M11).
- N2. runner/load.py:216 and :231 to 238, plans.py:130 and :141: k0 = Spokes x senses = 12; load.py:231 gives the outcome
  as its reason ("GR's gamma = 1 for light needs it"; k0 = 1 read 144). NOT_CLOSED 26; until the owner confirms k0 as the
  star's unit, a value chosen for its result.
- N3. Frame 6, the held hand: plans.py:59 to 80 sets the own spring to rest (K = 2 W), f = rest div Gamma (CHOSEN); the
  lays put the held hand at (1, 0) with before (0, -1): the spring picked so the hand turns exactly a quarter a round,
  the quarter turn per tick the past audit's E4 found typed as a table, now made by a spring tuned to 90 degrees. FRAMES
  6 records both G3 readers NOT PASSED; NOT_CLOSED 22 and 29. By Big Pic's own test for NOT_CLOSED 5 ("only if picked to
  land at an angle"), it needs the owner's word under line 102.
- N4. tests/test_the_tensor24_run.py:271 to 295 builds a pair world tuned to stay inside the room where the books close
  (Gamma 1000, tie 9600, key 614401, 1260 rounds); NOT_CLOSED 29 says the books open past the room; the test checks the
  closing side only.
- N5. decoder bangs.py, books.py, measure.py and records.py lack the four documentation layers (DOCLAYER), allowed by
  scribe_scan_allowed.json row 399.
- N6. From SCRIBE-LAW-AUDIT-2 F, still standing: board.py:30 to 38 spells the six neighbours a second time beside
  load.star; pyproject.toml:14 lists scipy, which nothing imports; papers/spacetime_events/build.sh calls scripts that
  left the tree; check.py has typed shard numbers; the schema holds records no run writes.
- N7. The two showcases (the click world's hold 1, tie 96000 and key 50811429; the mesh world's hold 1 and mesh 200000).

## 5. LAWFUL (with the reason)

- INDICATOR notes (load.py:64, 78, 80, 89, 93, 94, 107, 110, 112; plans.py:92, 96; carry.py:26 lit): zero and sign tests
  at the load selecting an entry, a character, a pair or a part; none caps a value; lit is used only by the loader.
- LENGTH notes that are format arities (records.py:214, :306; tools/tensor24_files.py:39); files.py:84 len(AXES), the
  board's axes defined once; SENSES = len(star(1)) and the act's halves() derive from the star.
- PIN notes (load test :73, :76): both restate the law's forms.
- The 2's spelt as senses: derived from the star, never typed (ALGEBRA.md line 1911); for the owner: where the 2
  belongs to the scheme (the half-teeth, the energy's half, the notch's 2h), calling it senses is a reading, not a count
  of the star.
- KEYS (41 notes on the format's keys; the CHOSEN block named in the files); DECLARE hits and floats in the tests are
  inputs laid there to be refused; frame.py is the tests' own model; the runner's promise and window (run.py:39 to 68)
  are read from outside the act; the square's slots follow its own basis (tested: the metric's kinds reordered read the
  same rows and give the same digest).
- den = 15162856759112389 (worlds tensor24 and tensor24-live) factors as 617 x 196613 x 124992409, every prime 1 mod 4:
  a rim picked for lattice points on a circle, the old engine's den circle (E19); in Tensor24 it only scales the teeth;
  swap in den 1, as the other three worlds use, if the relic should go.
- The live pulse's now slot (a polynomial bump, 2^28 (64 - d^2)^2); in the probes: integer LCG streams, the gate's DIVIDE
  notes, spring.py:110's first round, term11_act's tangential lay, measure.py's integer mean; the scribe_* gate files and
  the patches.

## 6. Past audits

- Came back: E3, a cosine by Chebyshev recurrence, in the well lay (F4).
- Back in another form: E4, the quarter turn per tick (N3); E19, the den circle.
- Never left: F8 (the tools' floats); N6; g3_strengths' bisections, which SCRIBE-GATE-1 left "to be removed by David's
  mend".
- Gone (checked): in src, literals, floats, integer roots, circular names, typed tables, caches, id() keys, the wall
  clock, a draw or books in the act; t5_trace.py's fractions and random imports; g5_draw's Pell pair (on toys-5, not in
  main); NOT_CLOSED 5's Pythagorean lay (not in main).

## 7. Counts per area

| area | FAKE | FORBIDDEN | NAMED-OPEN | LAWFUL (groups) |
|---|---|---|---|---|
| engine (engine/, algebra/, main.py) | 0 | 0 | 0 | 3 |
| runner | 0 | 0 | 3 (N2, N3, board.py in N6) | 6 |
| record | 0 | 0 | 2 (N1, records no run writes) | 0 |
| decoder | 0 | 1 (F7) | 1 (N5) | 2 |
| tools | 0 | 1 (F8) | 1 (shard numbers) | 2 |
| tests | 0 | 0 | 1 (N4) | 5 |
| examples | 0 | 2 (F4; F5 in live, well, mesh) | 1 (N7) | 2 |
| probes (73 .py, 4 .sh, 5 .patch) | 0 | 6 (F1 to F6; F4 and F5 also counted in examples) | 1 (N3 in the lays) | 6 |
| papers | 0 | 0 | 1 (build.sh) | 0 |

## 8. How far it got

Code (src, tools, tests, examples) in full; all 73 probes scanned and swept, read whole or in part where flagged (g3_
strengths, g3_kinds_and_parts, tb_tables, l2_ladder, the well, mesh and click lays, hand_per_quantum's head); the other
60 or so read through their hits. Papers counted, not read: the TeX holds 805 circular and 185 root symbols and 50 data
files hold decimals; no code runs from them; their results come from the old engine, whose phenomena the past audit
found made by circular formulas; the owner should decide whether to mark or withdraw them. Not run: the full check and
the tests; only the shipped world, twice.
