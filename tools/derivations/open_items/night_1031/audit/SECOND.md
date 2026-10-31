# Second reading of Sofer's items on main b1a50bb33

**Source.** Sofer's report is origin/scribe-5:tools/derivations/open_items/SCRIBE-AUDIT-B1A50BB33-1.md. Its text is
identical at 831499980 and at the branch's head, 2a28157ae.

**How it was read.** I read each item's line on main b1a50bb33, in the read-only tree scratchpad/scanY. Each verdict
below was checked twice; the two checks are named under each item. Nothing was edited, committed or pushed.

## Summary

| item | Sofer | mine | |
| --- | --- | --- | --- |
| B2 records.py:214 | FAKE | FAKE | AGREE; my LAWFUL withdrawn |
| B3 records.py:40, :306 | FAKE | FAKE | AGREE; my LAWFUL withdrawn |
| B4 tools/tensor24_files.py:39 | FAKE | FAKE | AGREE; my LAWFUL withdrawn |
| B5 files.py:32, :84 | NAMED-OPEN | NAMED-OPEN (a fake by his words unless he rules) | AGREE; my LAWFUL withdrawn |
| (B1 records.py:41, :171, not asked) | FAKE | FAKE (my F7, relabelled from FORBIDDEN) | AGREE |
| C5 the lays' typed inputs | NAMED-OPEN | split: the seed's inputs LAWFUL; SLOTS FORBIDDEN (minor); NUM/DEN and PERIOD FORBIDDEN (my F5, F4) | partly DISAGREE |
| C6 copies of the files' numbers | NAMED-OPEN | NAMED-OPEN | AGREE |
| C7 the click key by a typed seventh | NAMED-OPEN | NAMED-OPEN | AGREE |
| C8 g0_lane.py:18, :24 | NAMED-OPEN | FORBIDDEN (line 100's letter; harmless in effect) | DISAGREE on the label |
| C9 CAP = 10**60 | NAMED-OPEN | LAWFUL in kind; moot (the file leaves) | DISAGREE on the label |
| C10 the Eisenstein shell | NAMED-OPEN (M7's class) | NAMED-OPEN (M7's class) | AGREE |
| C13 the keeper's // and % | NAMED-OPEN (frozen) | NAMED-OPEN (frozen) | AGREE |
| E1 the keeper's tools | LAWFUL | LAWFUL, with limits | AGREE (confirmed) |

## B2 to B5: the counts behind label tuples

**Why I changed my verdict.** I first rated B2 to B5 LAWFUL as "format arities". That was not the owner's test. His
words of 2026-10-30, 09:0x and 11:0x UTC are: "There are no numbers hidden behind enums and such, right, because that
is a fake." The law says the same in scribe-5's docs/ARCHITECTURE.md line 361: "the law refuses a number behind a
length (lines 96 and 100)". Neither makes an exception for the format's own counts.

A tuple of labels written in the code is an enum by another name, and its length is a constant number. I now apply
this line:

- **Lawful:** a count read from the structure. That is the star, the Spokes, or a file's own data. files.py:64,
  SENSES = len(star(1)), therefore stays lawful.
- **A number behind a name:** a count read off a tuple of labels typed in the code.

The code writer's held fixes show that each number can go: 9a461bcdf and 834a4ffb7 (2026-10-30 13:17 UTC). I read
their diffs.

### B2: src/tensor24/decoder/records.py:214

The line is `len(lines) < len(("header", "end"))`.

- **AGREE: FAKE.** The literal tuple exists only to make a 2. Its members are used nowhere through it; headed() and
  ended() test the strings "header" and "end" themselves.
- **Check 1:** read on main.
- **Check 2:** 9a461bcdf deletes this line, and ARCHITECTURE:361 names "the frame's display" among the counts hidden
  in label tuples.
- **Fix:** read the frame from the structure. `lines[1:]` must be non-empty and its last line the end; no number is
  needed.

### B3: records.py:40 and :306

The lines are `ENDS = ("near", "far")` and `len(ends) != len(ENDS)`.

- **AGREE: FAKE.** grep shows ENDS used only at :306, for its length: a 2 behind labels.
- **Check 1:** grep over src and tools.
- **Check 2:** 9a461bcdf deletes ENDS and its use, and ARCHITECTURE:361 lists len(ENDS).
- **Fix:** take the two ends from the schema's own form, or drop the check, which only Whole records need (no run
  writes them).

### B4: tools/tensor24_files.py:39

The line is `len(given) not in (0, len(NAMES))`.

- **AGREE: FAKE.** NAMES = ("universe", "piece", "setting") is used for its names too: files.py:242, and
  tensor24_files.py:36 and :41. That is why I first read it as a table's count.
- But :39 compares len(given) with the constant 3 that the tuple stands for. The same check needs no number.
- **Check 1:** read on main, with every use of NAMES.
- **Check 2:** 9a461bcdf replaces :39 with `zip(NAMES, given, strict=True)`, and ARCHITECTURE:361 lists len(NAMES).
- **Fix:** that zip.

### B5: src/tensor24/runner/files.py:32 and :84

The lines are `AXES = ("x", "y", "z")` and `len(v) == len(AXES)`.

- **AGREE: NAMED-OPEN.** By his words its nature is a fake, the same as B2 and B3. AXES's labels are used nowhere
  in src except for their count, at files.py:84; the tests use len(AXES) too.
- It sets nothing in the run: run.py:181 takes the dimension from the piece, `star(len(shape))`. It only pins that
  a piece names three sides.
- It stands open because the document names it for his ruling. ARCHITECTURE:361 says: "len(AXES), the engine's
  dimension, stay as notes of the gate until their reasons are written and the owner has them".
- **Check 1:** grep over src, tools and tests.
- **Check 2:** run.py:181 read, and ARCHITECTURE:361.
- **Fix:** his ruling. Either the format may name the cube's axes, or the dimension comes from the piece alone and
  any refusal is read from the engine's own structure.

### B1: records.py:41 and :171 (WAYS)

Not asked, but for consistency: my F7 is relabelled **FAKE** by the same words. 834a4ffb7 deletes WAYS.

## C5: the lays type their own inputs

**PARTLY DISAGREE.** I would not send all of these to the owner as one question. Lay by lay:

- **The seed's inputs: LAWFUL.**
  - well_lay/lay.py:39 to 44: AMPLITUDE 2000, PULSE 500, HALF 4, CENTRE 9, TICKS 128, WINDOW 64.
  - mesh_lay/lay.py:37 and :40: PULSE 500, HALF 4, CENTRE 20, TICKS 125.
  - click_lay/lay.py:43, 44 and 47: A 40, TICKS 5000, SEARCH 1000.

  The seed is free: decision 38 (law line 35), and line 8, where "declared is a scale or a seed alone". These choose
  the laid state and its run, and their products stand in the approved setting files. None is a number of the
  universe or a role. The owner may still prefer the lays to read them from a file; that is a way of keeping the
  record, not a breach.

- **SLOTS = (0, 4, 5, 6), well_lay/lay.py:45: FORBIDDEN (minor).** It types the square's roles (00, xx, yy, zz) by
  place, while the same lay derives the ii places as `base + 1 + len(shape) + i` at :209. SLOTS decides which
  components land in the approved file.
  - **Check 1:** read :45, :175 to 186 and :209.
  - **Check 2:** examples/tensor24-well/setting.json lays the square train at components exactly [0, 4, 5, 6].
  - **Law:** a table typed by hand where the structure gives it (decision 41: "not outside the logic either";
    counts from the structure).
  - **Fix:** `SLOTS = (0, *(1 + len(shape) + i for i in range(len(shape))))`.

- **NUM, DEN = 20, 49 (well :42, mesh :38): FORBIDDEN, my F5.** (49, 20) solves 49^2 - 6 x 20^2 = 1: it is the Pell
  pair of sqrt 6, the lattice's light speed 1/sqrt 6. Sofer lists NUM and DEN only as typed inputs. His report scanned
  for Pell shapes but does not name this one.

- **PERIOD = 6 (well :46): part of my F4.** It is the period of the cosine mode, Sofer's A5.

- **SEVENTH 7** is C7, and **SCAN's 200000** is C6.

## C6: second copies of the approved files' numbers

**AGREE: NAMED-OPEN.**

- **Where:**
  - g5_draw.py:40: `GRIP = 15162856759112389 * 1000 * 1000`, with :41 `W = 6 * GRIP`.
  - c1_quantum_per_mode.py:19 and c2_held_by_the_clock.py:16: `W = 6 * 15162856759112389 * 1000 * 1000`; the same
    at g3_strengths.py:103 and g3_kinds_and_parts.py:32.
  - mesh_lay/lay.py:39: `SCAN = ((200000, 250), (250000, 125))`.
- **What:** each is a second copy of an approved file's number. In the first three it is also a copy of the loader's
  formula, 6 den Gamma^2 (load.teeth), with its 6 typed.
- **Check 1:** read on main.
- **Check 2:** they equal the files today: den 15162856759112389 and full_rate 1000 in
  examples/tensor24/universe.json, and mesh 200000 in examples/tensor24-mesh/universe.json.
- Against the owner's "numbers exist only in the files we approved" they are out of place. They are not hidden and
  not a fake today. Their author has named them (David 6536738713, item 1), with the mend.
- **Fix:** read den, full_rate and mesh from the file, and the teeth from the loader.

## C7: the click world's key chosen by a typed seventh

**AGREE: NAMED-OPEN.**

- **Where:** click_lay/lay.py:45, `SEVENTH = 7`, and :141 to 143: the key is the nearest odd whole to the seventh of
  the giver's largest swing at key 1, "so that about seven keys pass in a beat". It is written into the universe file
  at :149.
- **Check 1:** read on main.
- **Check 2:** lay.txt records the swing as 355,680,000, which gives the key 50811429 (7 x 50811429 = 355680003). The
  universe file holds 50811429.
- **Why it is open, not hidden:** it is a number chosen to land on a wanted click rate, and it is stated openly. The
  key is the universe's CHOSEN integer (files.py chosen.key, ODD). It is named open as Planck's key (NOT_CLOSED 3,
  which the owner's list holds as "the key at depth (3)"). It is also among the click world's showcase constants on
  the owner's list.
- It is not passed off as derived, and no clause of the law says how a chosen constant is picked. For the owner,
  beside C5.

## C8: derive/G/g0_lane.py:18 and :24

**DISAGREE on the label: FORBIDDEN.**

- **Where:** `t0 = time.time()`, then `f'{time.time() - t0:.0f}s'`: a float wall clock and a float format, in a job
  driver under tools/derivations.
- **Law:** line 100 names the derivation probes under tools/derivations ("No float anywhere in the system"). No word
  of the owner excepts timing yet. Sofer proposes to ask him; until he grants it, the letter forbids it.
- **In effect:** harmless. It is one log line of a job queue, and no engine, record or verdict reads it.
- It also builds its paths by string concatenation and f-strings, not by joinpath (the probes' rule).
- **New to my report:** my parser and the gate both miss `time.time()`.
- **Check 1:** read on main.
- **Check 2:** gate5's scribe_scan.py has no `time` in its PROBE list.
- **Fix:** use `time.monotonic_ns()` with Rule3's carry by 10^9, or drop the timing. Build the paths with joinpath,
  or delete the old driver.
- My F8 (check.py, documents_gates.py) is the same class, and I keep it FORBIDDEN on the same reason.

## C9: g3_strengths.py:190, CAP = 10**60

**DISAGREE on the label: LAWFUL in kind, and moot.**

- **Where:** CAP is used at :225, :257, :310 and :450, and in g3_kinds_and_parts.py at :37, :83 and :121.
- **What:** each use is `if abs(...) > CAP:` followed by a return. The probe stops a run it reads as run away.
- **Why lawful:** the law forbids a bound in the Node-clock, and src holds no CAP, if or clip in the act. A probe's
  stop is a reading device: ANIMATE-SPRING/spring.py:28 says of the same CAP, "the probe stops it there, the step
  never does".
- **Check 1:** every use read.
- **Check 2:** grep: no CAP in src.
- It is moot because both files leave main with F1 and F2, on David's word. Leaving is the file's fate, not the cap's
  nature.

## C10: g3_kinds_and_parts.py:247 to 252

**AGREE: NAMED-OPEN, in M7's class.**

- **What:**
  - `size = 3 * 231 * 231`.
  - `shell` is every (p, q) in [-480, 480]^2 with p^2 - pq + q^2 = size: the whole points of one hexagonal-norm
    circle, found by an exhaustive grid.
  - Then the least of f_act over the shell, printed with whether it falls on a symmetry line.
- A circle's whole points are used as the domain of a reading. That is M7's class: a rational point of the circle,
  NOT_CLOSED 5 on the owner's list, waiting on his ruling on "any construction that finds one".
- **Check 1:** read on main.
- **Check 2:** the shell feeds only the print at :251 and :252, and the file ends at :252, so it feeds no lay.
- By Big Pic's own test ("picked to land at an angle") the whole shell is taken, not one angle, so it may fall short
  of the bar. The owner's ruling on M7 decides. Moot here too, since the file leaves main.

## C13: the keeper's floor divisions and remainders

**AGREE: NAMED-OPEN (frozen).**

- **Where:**
  - SOFER-ODD-TEETH-1_PROBE.py: 13 floor divisions and 21 remainders, 34 in all, by my AST count.
  - scribe_law_check.py:113 and :119: `block.count("**") % 2` and `block.count('"') % 2`, the parity of the marks in
    one of the law's clauses.
- **Check 1:** my AST count on main.
- **Check 2:** they stand at exactly their frozen counts in scribe_scan_probes.json on scribe-5 (DIVIDE: floor
  division 13 and remainder 21 for SOFER-ODD-TEETH; remainder 2 for scribe_law_check), under the owner's "Yes."
  (DIVIDE is a note).
- The law's letter ("a division only with Rule3") reaches them. The remainders in scribe_law_check count marks in
  text, not the world.

## E1: the keeper's tools

**AGREE: LAWFUL (confirmed)** for the code of scribe_scan.py (2,651 lines at main), scribe_scan_selftest.py (3,453),
scribe_code_census.py (125) and scribe_law_check.py (710).

**Check 1, my own parser over all four.** It found none of these:

- a float literal, float() or round();
- a true division, other than scribe_law_check.py:398 and :411, which are path joins;
- a power;
- a banned import; they import only the standard library (argparse, ast, json, re, subprocess, pathlib and their
  kin);
- a circular or root call;
- a bisection, a series or a linear search.

**Check 2, every flagged line and every import, read by eye.**

- The circular words are the patterns they refuse: scribe_scan.py:137, 141, 157, 283, 298, 301 and 473;
  scribe_code_census.py:13; and the self-test's inputs, which must be refused.
- The names flagged as roots are just names: root_of, ROOTS, ROOT_MODULES, NEW_ROOT.
- len(DOCS) and len(CASES) count lists for a printed report.
- EXPECTED_LINES = 1960 is the keeper's tamper check on the law's length.
- The two `%` are C13's frozen two.

**Limits for the owner (none is a fake):**

- **(a)** The gate exempts its own files (OWN) from its probe rules. Only an outside reading checks them; this one
  did.
- **(b)** Main's copy of the gate (2,651 lines) is older than the keeper's working one (gate5, 2,751 lines).
- **(c)** The gate tiers LENGTH and SINEWORD as notes. That is why the counts the owner calls fakes (B1 to B4) and
  the typed sine values (Sofer's A3 and A4, my F2) reached main without a refusal.
- **(d)** The gate reads names and shapes, so these pass it: F3 (a linear search), F4 (a recurrence), F5 (a Pell
  pair), hand_per_quantum's trains with no pinion, and C5 to C8.

## What changes in my report

- **B1 to B4: FAKE**, as Sofer has them. My LAWFUL for records.py:214, :306 and tensor24_files.py:39 is withdrawn,
  and my F7 (WAYS) is relabelled FAKE.
  - So FAKE is now **4** items. All four are named in the document, with fixes held on the code writer's branch
    (9a461bcdf, 834a4ffb7).
- **B5: NAMED-OPEN.** My LAWFUL for files.py:84 is withdrawn.
- **F6 is corrected.** l2_ladder_on_the_act.py's coupling rows are on the owner's allowed list, scribe_scan_allowed.json
  row 399: "frozen until he redoes them on the generic form (the owner's word of 12:5x: no trains, no exceptions in
  code)". They become NAMED-OPEN.
  - hand_per_quantum/probe.py:70 and 71 stays FORBIDDEN: it was written at 19:31 UTC, after that word.
- **Added as FORBIDDEN:**
  - C8's g0_lane.py:18 and :24, beside F8;
  - C5's SLOTS (minor).
- **The verdict stays: NOT CLEAN.**

## Where the two readings still part (for the Boss to send on)

1. **F5, the 20/49 Pell pair of sqrt 6** in the live, well and mesh settings. Sofer does not name it; I hold it
   FORBIDDEN (decision 41). In the live world every one of the 144 before-counts equals ((49 - 20) now + 20 next)
   div 49, and that world's lay script is not in the tree.
2. **F3, tb_tables.py:174**, an integer root by a linear search added at 06:06 UTC (after decision 41), and its typed
   G and 3 G^-1 (:37, :38). Sofer has neither; I hold both FORBIDDEN.
3. **F6, hand_per_quantum/probe.py:70 and 71**: trains declared in code, and the metric found by
   `len(t["kinds"]) > 1`. Sofer does not name it; I hold it FORBIDDEN.
4. **C8 and F8, floats in tools:** FORBIDDEN by line 100 until the owner excepts them. Sofer: NAMED-OPEN.
5. **C9:** LAWFUL in kind against NAMED-OPEN. This is a label only.
6. **N2 (k0 = 12, "GR's gamma = 1 for light needs it", NOT_CLOSED 26) and N3 (frame 6, the held hand's spring tuned
   to an exact quarter turn a round, FRAMES 6):** Sofer does not list them. I hold both NAMED-OPEN for the owner.
