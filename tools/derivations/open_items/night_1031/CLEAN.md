# CLEAN: the hostile clean-code audit of the new engine, 2026-10-31 ~06:45 UTC

Read only. Nothing in /home/user/Universe24 or S/nodeall was checked out, edited or run. Trees were extracted
with `git archive` into S/audit_clean/<name>/ (all, live, onelaw, edge, third).

What was audited:
- node-all exists (local branch in S/nodeall, 3aa4467bd), but holds only node-live 1794d474b + node-half 0893f2f28.
  node-onelaw 08c66fd40, node-edge 88b4d281c and node-third d9ad5f6aa are not yet merged; they are audited as
  deltas over node-live, and as the union the writer will fold.
- Docs read on origin/scribe-5 5c65e7ab9: docs/ARCHITECTURE.md (417 lines), docs/ALGEBRA.md, and the plan
  tools/derivations/open_items/TENSOR24_PLAN.md. There is no ENGINE.md on scribe-5: it left the tree at 20d14ea45
  (2026-10-30, the owner's "there is the architecture file, there is the algebra file"); only origin/scribe keeps an
  old ENGINE.md (812dddb73, the old engine). Read "ENGINE.md" as ARCHITECTURE.md + ALGEBRA.md below.
- Line numbers are node-all's unless a head is named (edge:, onelaw:, third:). "S" = the scratchpad.

## VERDICT

The engine proper is clean: on every head, engine/ and algebra/ hold no loop, branch, comparison or mask; no
literal beyond 0 and 1 (and no 2 as a sum or a chained slice) stands in src or tools/tensor24_*.py; `//` and `%`
stand only in algebra/carry.py; no INDICATOR quotient stands in any act (step.py, mesh.py, contract.py: 0 notes
on every head, by scribe-5's own gate); src, tests and tools are ASCII with no model names.

The old code and the old tests are around it, not in it:

- OLD CODE, about 25 items: the old engine's nine record types in record/schema.py (Whole, Split, Rate, Books,
  Holding, Taking, Child, Reading, Ledger: 119 of its 229 lines) and their reader in decoder/records.py (four old line
  kinds, six old checks in off(), the winding rule, the books guard, a ledger guard on the old Ledger shape) and in
  tools/tensor24_decode.py; 3 definitions with no caller in src (files.WHOLE; onelaw's contract.read; onelaw's
  load.scaled, test-only); 1 empty package (src/tensor24/readings/); 1 refusal kept for a retired key (RETIRED
  couplings); 5 record fields read by nothing (engine, runner, order, operands, undone) and the train card's
  "winding" under its old name (edge adds 4 more fields read by nothing); the test frame's "out" path no engine
  reaches; about 12 comments describing code that is not there; about 35 history-marked lines in src.
- OLD TESTS, about 55 cases: about 45 decoder cases built on line kinds no run writes (whole, rate, books) or on the
  old ledger line with "wind" (about 450 test lines: test_the_tensor24_decoder.py 22-304, all of
  test_the_tensor24_decoder_cases.py, meetings 26-29 and 172-174), about 30 of which test the old engine's fields
  and guards themselves; 2 asserts that test nothing current; 5 files-test cases that duplicate the unknown-key rule
  with old field names, and the `light` helper; 3 asserts that pin the constants of readings that read nothing;
  copied fixtures across two decoder files.
- MERGE DEFECTS, 6, found while auditing the union: the most serious is that third's 1.4 sides guard refuses edge's
  1.4 records wherever a Mesh edge carries (the mesh world), so node-all with both merged fails its own worlds test.

## THE LIST, ranked by weight

Each item: where; what; why it is old or unclear; the action.

### A. Merge defects in the union (fix while folding; each breaks node-all or misreads its records)

A1. third:src/tensor24/decoder/sides.py:44 and :30, against edge:src/tensor24/runner/run.py:clicked (the 1.4 line).
    What: third's guard requires a line's q to equal the sum of its "sides" and refuses a line with no sides. Edge's
    1.4 line (88b4d281c, after third was written against 50af24bde) sets q = SUM(sides) + SUM(across) and writes a
    line with sides [] for a clock whose only edges are Mesh edges (the board's wave). Why: edge's own README says the
    mesh world writes 21589 click lines from round 20, 14547 with Mesh sides that carried, and edge's worlds test pins
    the mesh world at 20 rounds with 8 click lines past its first Mesh click; with `paired` in GUARDS the merged
    reader refuses that record ("sides sum to .., not its q .." or "no sides"), and
    tests/test_the_tensor24_worlds.py's `cause == ""` fails for tensor24-mesh. Action: in sided(), sum sides and
    across against q, accept sides [] where across is present, and give `across` its own form and mirror check (edge's
    worlds test already holds the rule: q = SUM over sides + across, each side's mirror at the partner's place);
    add an across case to test_the_tensor24_decoder_sides.py. DERIVED from the code, certain: the wave has no
    own-Node-clock edge in the mesh world (no value-leg monomial joins it to another train), so edge's joined() gives
    it no partner and every wave line is {"sides": [], "across": [...]}, which sided() refuses at its first rule.
A2. edge:src/tensor24/engine/step.py:86 (passing reads `first, second, third, factor, target = plan`) and
    edge:src/tensor24/runner/plans.py:78 (crossing reads `first, _, _, factor, target = mesh`), against onelaw's
    Plan(legs, factor, target) (onelaw:src/tensor24/engine/state.py:22-31, contract.py:13-31).
    What: edge's two new readers of J's plan read the three-leg form onelaw replaced. Action: port both to `legs`
    (passing: the product over `legs` with the factor first, as onelaw's contract does; crossing: `legs[0]`), and
    Loaded.push/mesh's comments (edge load.py:156-172) to the k-leg form.
A3. third:src/tensor24/decoder/records.py:291 lacks edge's `and "sides" not in e` (edge:records.py:290).
    What: on third, a 1.4 line of q 0 (which edge writes for every clock joined to a carrying edge) is refused as
    "a tooth that carried no key". Action: take edge's version of clicked().
A4. src/tensor24/decoder/shadow.py:56-58 (met), :117-152 (clock_lines), decoder/clicks.py:1-4, and
    tools/tensor24_decode.py:2 and :37.
    What: the click world's readings and the tool assume 1.3, one line per train whose own tooth carried. Edge's 1.4
    writes a line for every clock of a joined set, q 0 included, so a place where one edge carries holds three lines
    in the click world (held, giver, taker) and met() ([-1, 1] sorted) reads it as no meeting; the tool prints
    "tooth None" for every 1.4 line and shows neither sides nor across. Action: read 1.4 meetings by the edge sides
    (a meeting is an edge side and its mirror), drop q-0 lines from the meeting count, print sides and across in the
    tool; rename the readings' 1.3 constants (shadow.py:15-18 "1.3 writes none", "every 1.3 clock"). DERIVED from
    the code, certain: in the click world the tie joins the held hand to the giver and to the taker and the hands'
    tie joins those two, so edge's meeting() puts the three in one set and all three write a line wherever one of
    their sides carries; met() then never reads SHOWN on a 1.4 click-world record.
A5. tools/tests_shape.py:62-77 (ROOM), against the union's line counts.
    What: the budgets (ROOM + SLACK 40) are exceeded once onelaw and edge both land: tests/test_the_tensor24_engine.py
    300 -> about 365 (onelaw +37, edge +28; budget 340); tests/test_the_tensor24_load.py 155 -> about 211 (budget
    195); tests/frame.py 237 -> about 278 (budget 277); edge's run test already sits at 335 = its budget. Action:
    make room by the cuts of section C below (the old decoder tests alone free about 450 lines), not by raising ROOM;
    the ROOM reasons quote line counts that drift ("300 lines", "155 lines", "237 lines").
A6. tests/tensor24_prefixes.jsonl (all 4 lines) and tests/test_the_tensor24_half.py:219-223, 238-242.
    What: the prefixes pin each head's own record bytes (node-all: the click world 27 lines at round 1; edge: 81 lines,
    the mesh world 8 lines at round 20); half's test reads `held.click` as (one, two, entry, train, key), the pair
    form edge replaces with (weight, train, key, across, onto). Action: rewrite the prefixes on node-all by
    derive/boss/prefixes/write.py after the merge, never by hand; cut half's "pairs by the dot" check, or move it to
    the tie, the one place pairs_of still lays.

### B. Old code (no caller, vestiges of the old engine, superseded forms, fields read by nothing)

B1. src/tensor24/record/schema.py:89-195 and :218-229 (Holding, Taking, Child, Reading, Whole, Split, Rate, Books;
    Ledger), with schema.py:9-13 and :14.
    What: the old engine's records: whole clicks with books, ends, children and windings, the split click with its
    draw and detector, the asynchronous runner's rate line and beat counts, books lines, and the old ledger line
    (wind, sweep, push, moment, windings). No run writes any of them since 1.2/1.3; they are reached only through
    records.schema_shapes()'s vars(schema). The comment at :9-13 still says "the ledger's own file holds Ledger and
    Count lines" (the run writes Count lines alone) and :14 says "the decoder upcasts an older major" (no upcast
    exists: records.py:225-230 refuses every major but 1). Action: retire the nine records with the decoder rules and
    tests that read them (B2, C1) in one cut; since the reader then refuses kinds it knew, make it schema 2.0, or say
    in the schema that 1.0-1.2 records are no longer read; drop the upcast sentence.
B2. src/tensor24/decoder/records.py:39 (KINDS' "whole", "split", "rate", "books"), :41 (BOOKED), :42 (AT's
    "clicks": the run writes only "step"), :137-159 (off(): ends, children, Spokes, the count "before the first beat",
    a whole click's q below 1, a holding's windings), :175-184 (carded(): "a winding counts its train's notches, and
    the books read each train's windings at it"), :302-307 (booked()), :345-348 (fitted()), and the comment block
    :3-29; tools/tensor24_decode.py:65 (`or record.of("whole")`) and :10-11 ("no whole click").
    What: the reader of the old records. fitted() is also wrong now: it checks every ledger line against the old
    Ledger record, so the Count lines the run writes have their "site" and "count" checked only as leaves (a Count
    line with "count": "x" passes). Action: retire with B1; check ledger lines against schema.Count; AT = ("step",).
B3. src/tensor24/runner/files.py:53 `WHOLE = Rule(whole, "a whole number")`.
    What: used by no rule of the format, by no tool and by no test (the meetings test's WHOLE is its own fixture),
    on every head. Action: delete.
B4. onelaw:src/tensor24/engine/contract.py:35-40 `read()`.
    What: after onelaw (the clocks' read became a Plan through contract()), nothing calls read(): step.py imports
    contract alone, mesh.gripped does its own gather on the stretch's Read. tools/tests_shape.py's rule (d) does not
    see it (see B12). Action: delete; keep state.Read only for the stretch, or move the stretch to a one-leg Plan too
    and retire Read, frame.unread() and frame.dense()'s isinstance branch (onelaw tests/frame.py:227-245).
B5. onelaw:src/tensor24/runner/load.py:267-290 `scaled()` (Sofer's finding), with onelaw
    tests/test_the_tensor24_load.py:159-183 (the test
    test_the_whole_action_times_one_factor_moves_every_count_and_click_bit_for_bit_and_runs_back).
    What: called only by its test; its own docstring says "OPEN, so no run scales and no file names a unit". Its
    1,269-character docstring also carries the open flat and units. Action: delete with its test (git keeps them),
    or keep it in a probe under derive/; main.typed (onelaw main.py:28) stays, as main.layout uses it.
B6. src/tensor24/readings/__init__.py (the whole package).
    What: one docstring line, "The readings' formulas, read by the runner and the decoder alike"; no module, no
    import, named by no part (ARCHITECTURE.md:308 says so) yet kept in the import table (ARCHITECTURE.md section 5).
    Action: delete the package and its rows in section 5 and in the gate's walls.
B7. src/tensor24/runner/files.py:35-38 (RETIRED), :172 (its use), and tests/test_the_tensor24_files.py:224-228.
    What: a refusal kept to name a key the format dropped ("couplings"); the generic "the key .. is not in the format"
    already refuses it. Action: delete RETIRED and the case.
B8. src/tensor24/runner/run.py:156 "engine", :157 "runner", :160 "order" (ORDER, :23), :179 "operands"
    (files.OPERANDS, files.py:25-31), :224 "undone"; schema.py:67-74 and :203.
    What: header and end fields no reader reads (decoder and tool: 0 reads each); "runner": "synchronous" names the
    asynchronous runner's absence, "undone" always equals "rounds". ARCHITECTURE.md:203 says 1.3 retires the runner's
    name and the operands; the code still writes both. Edge adds four more read by nothing: the header's "dial" (equal
    to every train card's "key", edge run.py:240 and :249), "birth" (:250), and the end's "teeth" and "across"
    (:304-305; DECODE3's fields for a reader not yet built). Action: retire engine, runner, order, operands and
    undone in the next minor; keep one of card "key" / header "dial".
B9. src/tensor24/runner/run.py:148 and :171 ("winding": the drive's dial T_d at the train's first row), schema.py:55,
    records.py:175-184.
    What: the old engine's "winding" (a whole click's notches) reused for T_d, guarded with the old meaning; on edge
    the header also has "dial" for the edge key, so "winding" (the drive) and "dial" (the key) are two names for two
    dials. Action: rename the card field to the drive's dial, or retire it (no reader needs it).
B10. tests/frame.py:22-29 (Engine.unstep(nb, s', out)), :134-143 (bijective's `bool(o1)`), :191-206.
    What: the property harness keeps the old engine's step "out"; the one engine adapter returns () always
    (test_the_tensor24_engine.py:117-123), so the out branch is a path no engine reaches. Action: drop "out".
B11. Superseded forms and copies kept beside their replacements.
    - whole() three times: runner/files.py:41, decoder/records.py:64, third:decoder/sides.py:17; Line three times
      (decoder/clicks.py:11, records.py:46, third:sides.py:11), Lines twice (records.py:47, third:sides.py:12): sides.py
      copies them because records.py imports it. Action: put the guard in records.py, or the helpers in record/.
    - the product of the sides twice: files.py:222-227 (sites_of) and records.py:167-169.
    - schema.Click.tooth (edge schema.py) beside sides, and records.clicked's 1.3 tooth checks beside third's 1.4
      sides guard: two guards for one line kind. Action: decide whether 1.3 records are still read (C7); if not,
      retire the tooth and its checks.
    - after the union: plans.selves's half-speed kept forms and load.kept_forms (load.py:214-219) feed only
      holding()'s tie, where every half-speed train is untied (factor 0): a path no world reaches once edge's edging
      replaces half's pair passing. Action: keep them only if the tie of a half-speed train is planned; else cut.
B12. tools/tests_shape.py:193-204 (uncalled()).
    What: the rule "a public function of src/ that nothing in src/, tools/ or examples/ names is refused" counts the
    name as a word anywhere, docstrings and comments included, so it passes onelaw's contract.read ("read" is
    everywhere) and load.scaled (its own docstring says "the scaled act's"). A check that cannot fail on the two dead
    functions it exists for. Action: count AST name and attribute loads, not words.
B13. Comments and docstrings that describe code no longer there:
    - src/tensor24/algebra/carry.py:4 "a click will be such a quotient where a winding is whole (G5)" (built: the
      click tooth's quotient at the key).
    - src/tensor24/decoder/clicks.py:1 and :4 "the clicks are not closed, so no reading stands on them yet ... until
      the clicks are closed" (shadow.py reads seven readings on them).
    - tools/tensor24_run.py:1 "(stage 10)" (the plan's build stage).
    - tests/test_the_tensor24_run.py:207 "no rate line".
    - onelaw:src/tensor24/engine/step.py:3 "(the widened step: ONELAW3 3.4's seven gears for det(gt) L^4, ten with the
      cross terms, against today's one 00 row)" and onelaw step.py:96 (weight) "the 3+1 split's dial det(gt) L^4 among
      them ... OPEN": they describe a dial no loader lays.
    - src/tensor24/engine/state.py:43 "every train's key, CHOSEN in the universe file" and load.py:2-3, :184 (true
      today; they go with the key, D1).
    Action: cut to what the code does.
B14. About 35 lines of src carry review history (reader IDs, rulings, hashes, NOT_CLOSED and FRAMES numbers, issue
    comment ids): e.g. runner/files.py:66 and :73 ("the first hostile code reader's M6 and the second's 3"),
    runner/plans.py:50 (M1), record/schema.py:2 (M11), runner/load.py:232 ("#2187 6488192915"), :264-265.
    Action: move the history to git and the ledger; a docstring says what the code does. The tests carry the same
    (tests/frame.py:52, :141; test_the_tensor24_engine.py:202, :213, :299; test_the_tensor24_load.py:46, :65, :86;
    test_the_tensor24_kinds.py:62, :79), which tests_shape's HISTORY pattern does not count.
B15. Not old, but no world reaches it, by design: the half-speed machinery (engine/kinds.py:24-40 and :121-223,
    runner/files.py:279-331 Spun, spun and halved_departures, runner/load.py:104-121 and :214-219) runs only in tests,
    since every file run refuses a half-speed train by name ("no family couples a half-speed train in this build",
    files.py:330). Keep it (the owner's "build everything generically"); name it so in ARCHITECTURE (F1).

### C. Old tests

C1. tests/test_the_tensor24_decoder.py:22-53, :66-146 (BROKEN), :172-202, :205-256, :271-305;
    tests/test_the_tensor24_decoder_cases.py (all 168 lines); tests/test_the_tensor24_decoder_meetings.py:26-29 and
    :172-174.
    What: about 45 cases on whole clicks, rate lines, books lines and the old ledger line ("wind" after "step" and
    after "clicks"). About 30 test the old engine's fields or guards (a whole click's books twice, its ends' sites
    and Spokes, children, the count before the first beat, windings and winding, a whole click's q, the ledger's wind
    as a whole number); the rest use old lines only as carriers of generic reader rules (the order, the board, ASCII
    names, digits, unnamed fields). The headers sit at minor 1. No Count line, the ledger line the run writes, is fed
    to the ledger guards. Action: cut with B1-B2; rewrite the generic rules once on click lines and Count lines,
    in one file.
C2. tests/test_the_tensor24_decoder.py:200-202 (the "turnover" kind).
    What: the same rule as BROKEN's "an unknown kind" (chime), on a kind retired at 1.2. Action: delete.
C3. tests/test_the_tensor24_run.py:180
    `assert not {"Ruler", "LAID"} & set(dir(state)) and not {"ruled", "reading", "at"} & set(dir(step))`.
    What: asserts that old names stay gone; it tests no behaviour of the code. Action: delete.
C4. tests/test_the_tensor24_run.py:271-296 (the pair world "kept as NOT_CLOSED 37's record").
    What: by its own comment it holds "whichever way it falls" (no departure, or the width's own); 1260 rounds that
    pin nothing of the engine. Action: delete, or move to a probe under derive/.
C5. tests/test_the_tensor24_files.py:20 (`light`, used at :191, :196, :201, :206, :211, :270) and :204-223.
    What: the helper keeps the old name of the first train (now "wave"); "a sine", "a weight", "a trace" and "a key,
    read by no act" repeat the unknown-key rule already held by the five "colour" cases (:119-143), with old field
    names. Action: rename the helper (`first_train`), delete the four cases.
C6. tests/test_the_tensor24_decoder.py:379 (`d6 == shadow.NO_COUNT and d7 == shadow.AT_NODE`) and
    tests/test_the_tensor24_decoder_meetings.py:71 (`shadow.echo(yes) == {"kind": "NOT READ", "cause": ECHO}`).
    What: shadow.duration/twins/echo (shadow.py:162-174) return a fixed NOT READ on every record with a click line;
    the asserts compare the module's constants with themselves. Action: drop the three stub readings and their asserts
    until each reads something (the owner: build it, no reading on paper), or keep one line naming them owed.
C7. tests/test_the_tensor24_decoder.py:309 (THIRTEEN) and :333-390 (three tests named and docstringed "schema 1.3").
    What: once edge lands the run writes 1.4; these then test a line no run writes, under minor 4 (schema.MINOR).
    Action: decide (Boss) whether the decoder still reads 1.3; if not, move the three to 1.4 lines; if so, name it.
C8. Duplicates.
    - tests/test_the_tensor24_decoder.py:16-53 and tests/test_the_tensor24_decoder_cases.py:12-61: the same TRAINS,
      H, B, E, holding/hold, click, end_of, rate, without and TAKE/ENDED/PAIR, copied (tests_shape's 8-line rule
      misses short copies). Action: goes with C1.
    - tests/tensor24_prefixes.jsonl on node-all: live, mesh and well have "no": 4 = "rounds": 4, so the test runs the
      same 4 rounds twice and "own" pins the same digest as "digest". Action: "no" one round short of "rounds".
    - one state turned by a group element in four forms: test_the_tensor24_engine.py:159 (twisted),
      test_the_tensor24_run.py:117 (turned; edge moves it to frame.turned_by), test_the_tensor24_half.py:175 (turned)
      and :245 (boarded). Action: one helper in tests/frame.py.
    - edge: test_the_tensor24_engine.py:233 and test_the_tensor24_run.py:286 both check an edge's two sides summing
      to 0 with teeth to key - 1 and the run back. Action: keep the check once.
C9. Names that no longer say what the test tests, and tests without a docstring.
    - test_the_tensor24_run.py:174 test_our_bang_is_laid_by_one_formula_... also holds the schema's leaves
      (:232-237), the departures and the even key (:238-258), the tool (:259-266) and the pair world; no docstring.
    - test_the_tensor24_engine.py:238 test_the_metric_is_pushed_... ("metric", D2).
    - test_the_tensor24_decoder_meetings.py:145 test_the_books_read_in_row_15_order_... holds the whole-click case.
    - test_the_tensor24_half.py:196 ..._and_pairs_by_the_dot and test_the_tensor24_load.py:98
      ..._the_passings_pairs_... test the pair passing edge removes (edge renames the load test; half's stays).
    - edge test_the_tensor24_engine.py:233 test_the_click_tooth_carries_the_pairs_passing_... now tests edge sides.
    - no docstring: test_the_tensor24_decoder.py:244 and :271, test_the_tensor24_run.py:174.
C10. Train labels with physics words in tests: test_the_tensor24_load.py:22 ("spin axial stress potential field"),
    test_the_tensor24_half.py:44 and :202 ("spin"). Action: clock labels.

### D. Leftovers named in the night's reports

D1. universe.json's chosen.key (KEY2): STILL THERE on every head. src/tensor24/runner/files.py:109 ("key": ODD),
    :65-71; src/tensor24/runner/load.py:191-192 (one key for the board, the birth (key - 1) div senses); edge
    load.py:184 (edging(..., chosen["key"], ...)) and :280-282 (laid_out reads chosen.key again to recover kappa / two
    by a carry); all five examples' universe.json. KEY2 (S/onelaw/KEY2.md) is DRAFTED and read by no hostile reader;
    it recommends laying the click teeth's birth k0 in the setting (K = senses k0 + 1, unlaid 0 = key 1) and retiring
    chosen.key, and measures the click world's lines and end digest unchanged. Per the Boss's ruling of 05:3x ("no key
    moves until the owner rules"), it stays until the owner's word. When it goes: files.py ODD and its tests
    (test_the_tensor24_files.py:41, :86-87), load.py:191-192, edge load.py:184 and :280-282 go with it.
D2. The "metric" train name: STILL THERE.
    - examples/tensor24, tensor24-click, tensor24-live and tensor24-well universe.json name a train "metric";
      examples/README.md 10 times.
    - src prose, 29 lines: runner/files.py (4; the user-visible messages at :76 "the metric's push off or on" and
      :363 "one metric family"), runner/load.py (7), engine/step.py (7), engine/state.py (6), runner/plans.py (2),
      engine/kinds.py (2), engine/mesh.py:35 ("the metric's push reads (term 5)").
    - tests: test_the_tensor24_load.py:26 (METRIC), :82; test_the_tensor24_half.py:34; test name at
      test_the_tensor24_engine.py:238; tools/tests_shape.py:55.
    - ARCHITECTURE.md 30 times ("The metric family" part).
    Action: the clock's name for the square's train (for instance "the clock train", its 00 slot "the clock's
    count"), in files, messages, prose, tests and docs; the label is a file's, so the examples change with it.
    Related board words: "gravity" at runner/plans.py:146 ("(gravity on)") and engine/step.py:4; "spin" as variable
    names in engine/kinds.py:206-217.
D3. Copy (a)'s "light" card: GONE from the files (the click world's card was renamed "wave" at 1794d474b; S/vary2's
    report). Remnants: the test helper `light` (C5); ARCHITECTURE.md:40 and ALGEBRA.md:35 (twice) still say "the
    wave of the train the files name light": no file names it so now. Action: "the board's wave of the A1 train".
D4. The 12 INDICATOR notes: STILL THERE on node-edge 88b4d281c. Read with scribe-5's gate (its indicator() on each
    function), runner/plans.py holds 25 notes on edge against 13 on node-live; the 12 added are edging's 9
    (f71c19390; edge plans.py:49-66) and crossing's 3 (88b4d281c; :89-91). meshing's own notes are 6 at three places
    (the `1 - lit(...)` masks at edge plans.py:223, :228, :233), the same as on node-live. node-all's own copy of the
    gate (older, without the "agreement" rule) sees 2 in plans.py. All are in the loader; no act holds one. One is a
    mask on a chosen number's value: edging's `lit(factor)` (edge plans.py:61-66) decides which monomials are edges,
    and kappa, the edge key's factor, from whether a CHOSEN strength is 0. Action: none for the act rule; name the
    whethers of the initialization in the docstring as the ledger reads them, and put edging's strength mask to the
    readers.

### E. Order (layout, names, schema versions, folders)

E1. Schema versions. node-all: 1.3 (MINOR = len(ADDED) = 3). Edge: 1.4, which retires the click line's "tooth" (a
    field readers read: records.py clicked()) at MAJOR 1, though the schema's own rule (schema.py:15) admits for a
    minor only an added field or line, or a line no run writes retired. Third: names "a 1.4 click line" (schema.py:78-80
    SIDE; sides.py) at MINOR 3. Stale "1.3" after the union: decoder/records.py:1, decoder/shadow.py:3-4 and :15-18,
    tools/tensor24_decode.py:2, tests named 1_3; edge schema.py:2 says "schema 1.4 ... with 1.3: not yet read". The
    header's "minor" is read by no reader, and the decoder reads every line kind in every minor. Action: either 2.0
    for the union (the tooth gone, the old kinds gone, B1) or keep the tooth; one version word in every docstring.
E2. Names used for two things: board (runner/board.py:23, decoder/records.py:162, tests/frame.py:32); placed
    (engine/kinds.py:106, decoder/records.py:247, decoder/shadow.py:48); read (runner/files.py:131,
    decoder/records.py:387, onelaw contract.py:35); passing and crossing (engine/step.py vs runner/plans.py, the act
    vs the loader; edge); clicked (runner/run.py:114 writes lines, decoder/records.py:280 guards them); Click
    (engine/state.py:42 vs record/schema.py:79); Train (runner/load.py:20 vs record/schema.py:48); Engine
    (runner/run.py:27 vs tests/frame.py:22); and the line kind "whole" is the old engine's whole click while term 11's
    whole click is written as kind "click". tests/test_the_tensor24_decoder_measure.py:5 imports frame "as board".
    Action: one name, one thing.
E3. Layout against the architecture's parts. The Loader part is spread over runner/files.py (the star, :58),
    engine/kinds.py (the kinds and lifts), runner/load.py (the 24's tables, :68), runner/plans.py and main.py (made);
    runner/ holds both the Loader and the Runner; star is imported through load (tools/tensor24_files.py:49,
    tests/test_the_tensor24_kinds.py:11, test_the_tensor24_run.py uses loading.star). The decoder's guards sit in
    records.py and in third's sides.py. Action: a folder per part, or ARCHITECTURE saying where each piece is.
E4. Files in another folder: tests/tensor24_prefixes.jsonl is written by tools/derivations/open_items/derive/boss/
    prefixes/write.py, a test-data generator inside a derivation folder; the example worlds' generators
    (derive/boss/click_lay, mesh_lay, live_lay, well_lay) likewise. Action: move write.py and the generators beside
    the tests or under tools/.
E5. examples/tensor24-click/setting.json ticks 5000: the shipped run names a count past the width at round 3752 and
    writes no record (examples/README.md, KEY2 4); the decoder has nothing to read on the shipped click world.
    Action: ticks within what runs (3751), or relay the world; an example should run.
E6. Small ones: engine/state.py:59 Gearing.parity's default 1 is used only by test_the_tensor24_engine.py:112;
    runner/load.py:194 `chosen, _, rest = universe["chosen"], *teeth(...)` (obscure, and teeth() is called again in
    geared()); runner/files.py:80-87 axial() counts the axes by catching board()'s unpacking error; tools use
    `Path / "src"` where probes are asked for joinpath.

### F. The documentation

F1. ARCHITECTURE.md (scribe-5) does not name parts and tests that exist (its own rule at :308 refuses them):
    decoder/sides.py and test_the_tensor24_decoder_sides.py (third); plans.edging and plans.crossing, and
    test_the_tensor24_edges.py (edge); kinds.lifts, files.Spun, load.kept_forms, plans.selves, and
    test_the_tensor24_half.py and test_the_tensor24_lifts.py (half; on node-all now); load.scaled (onelaw, B5). The
    Loader's Home (:189) lists rows_of, holding, tying, joined and meshing only.
F2. ARCHITECTURE.md statements the code contradicts:
    - :110 "BUILT at schema 1.3" against :205 "BUILT at schema 1.2"; after the union 1.4.
    - :203 "three fields no reader reads, the runner's name, the couplings (empty) and the operands, until schema 1.3
      retires them": runner and operands are still written (B8).
    - :126 "On main the plan is empty, so J = 0, and the tables are made but no plan reads them": the plans lay the
      notch, the hold, the tie and the mesh from the tables in four worlds.
    - :128 "A whole click will be the carry of a train's swept area by its own tooth": built (term 11).
    - :117 and :213 one click tooth per train, schema 1.3: after edge, edge sides and 1.4.
    - :40 "the train the files name light" (D3).
    - :304 "the decoder's four modules are owed" the four layers: clicks.py and shadow.py hold them; records.py and
      measure.py still lack them (and third's sides.py has them).
    - :308 the readings package "stands named by no part": still in the tree (B6).
    - :213 the click world's 282,663 lines in 5,000 rounds: no shipped run produces them (E5).
F3. ALGEBRA.md (scribe-5): its body cites about 114 files of the old engine as where its lines are held or gated
    (src/event_universe/share.py at :856, :878, :921; tests/test_the_node.py at :500, :878, :931; tests/test_the_board.py
    at :618; core/acts.py; ...), none in the tree since 2026-10-30; 18 lines name the assistant's brand (branch
    names of the form <brand>/click-one-act at :360-364, :819, :915, :948, :1619, :1628 and others, and "<brand> Code's
    check" at :102), against "no model names"; :35 "the train the files name light", twice. Action: point each law
    line at the new engine's part or say "no part yet"; drop the branch names.
F4. The plan, tools/derivations/open_items/TENSOR24_PLAN.md (scribe-5), section 11-13 (:405-506) describes parts that
    do not exist: engine/click.py with click_whole and click_split (:411), carry.py's nonneg, choose and home (:480),
    the Gaussian integers in algebra/ (:413, :484), readings/ (:413), a state of eight arrays a, b, r, rd, go, ph, tn,
    c (:415; the state is a, b, r, rd, k), an undo log read by rewind.py (:418, :490; rewind reads none), and the
    asynchronous runner (:426). Action: head it "superseded by ARCHITECTURE.md", or update section 11 to the five
    modules as built.
F5. Docstrings.
    - no docstring: decoder/records.py's 16 guards (:205 jsoned, :214, :218, :225, :233, :238, :242, :247, :253, :263,
      :302, :310, :331, :336, :345, :351), tools/tests_shape.py:122, :126, :266, and the tests of C9.
    - no four layers: decoder/records.py:1 and decoder/measure.py:1.
    - too long to be plain: runner/plans.py:146 pushing (2,488 chars), edge plans.py:36 edging (2,045), edge :77
      crossing (1,430), plans.py:178 meshing (1,348), onelaw load.py:270 scaled (1,269); engine/step.py:1-5 (3,679
      chars of module docstring). Unclear phrases: step.py:109 dials "the promise's measure, read from outside",
      :116 grips "the window's measure", files.py:81 axial.
    - decoder/shadow.py:1 "the board's physics read in its shadow": physics is only the click world's (the owner's
      word); say "the click world, read from the record".
    - tools/tests_shape.py:45-58: the ROOM reasons are about 5 KB of history; the owner asked the bureaucracy out.
F6. examples/README.md: "metric" ten times (D2); the click world's paragraph carries an earlier lay's numbers
    (282663 click lines in 5000 rounds; the books at 123066 of 123795 places) and, on edge, readings "measured before
    term 11 was laid on the edges ... wait for the re-lay": numbers no shipped world produces.

## Method, and what was run

- Read every file of the scope on node-all and every scope diff of onelaw, edge and third over node-live.
- AST scripts in S/audit_clean/scripts/ (read only): census.py and callgraph.py (callers), numbers.py (literals,
  1 + 1, chained slices, divisions), engine_rules.py (loops, branches, comparisons, masks in engine/), docs.py
  (docstrings and the four layers), tests_list.py (test names), indicators.py (the gate's own indicator() from
  scribe-5's and node-all's scribe_scan.py, applied per function).
- No test and no engine run was made. A probe to confirm A1 and A4 by execution was queued
  (S/audit_clean/scripts/probe.sh: edge's run tool on the mesh world at 20 rounds and on the click world at 1 round,
  each record read by edge's and by third's decoder) behind the rule's gate, the 1-minute load below 4; the load stayed
  between 5 and 8 from 06:1x to 06:40 UTC, so it was stopped unrun. A1 and A4 stand DERIVED from the code; the script
  is ready for the writer to run on node-all after the merge (python -I, one process at a time).
