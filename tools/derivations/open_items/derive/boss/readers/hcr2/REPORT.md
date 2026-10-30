# The second hostile code reader on f72067cdf..87f88322d (node-live), 2026-10-30

Filed by the Boss from the reader's hand-back.

HOSTILE CODE READING 2: f72067cdf..87f88322d (node-live), and the tree at 87f88322d

Summary: no BLOCKING finding, seven MINOR findings. The first reader's B1 is folded. Hypothesis (d) holds by the structure of the loader's plan, and it held on every lay I could reach, including one with every plan on at once. M1 to M7 and M10 to M12 are folded. M8 is still open, waiting on the owner's word. M9 is half folded.

WHAT I RAN
- The gate (gate5, --base origin/main --summary): 0 refusals and 6 notes, each read.
  - INDICATOR load.py:110 and :112: the held and kept flags, exact character tests.
  - INDICATOR plans.py:92 and :96, both in tying: a sign test that takes each unordered pair once, and a one-part test.
  - PIN load test :73 (the 0i rows' range) and :76 (the notch's factors and the square's ten rows).
  - None of the six is a bound inside the Node-clock. The PIN count fell from 3 to 2.
- The full check (CHECK_BASE=origin/main): exit 0, 27 passed.
- scribe_law_check --arch: 1 departure, runner/plans.py. This check is not among tools/check.py's ratchets.
- The five worlds, run by the run tool on this tree. Each wrote its record with exact 1:

| World | Rounds back | Digest | Time | Click lines |
|---|---|---|---|---|
| tensor24 | 10 of 10 | 540e503cad44 | 1 s | 0 |
| live | 100 of 100 | cfef203d5dd5 | 54 s | 0 |
| well | 128 of 128 | 05586b5db17f | 142 s | 0 |
| mesh | 125 of 125 | 00fd62494c9a | 27 s | 0 |
| click | 5000 of 5000 | f351582ede39 | 1026 s | 4212 |

  The click world's digest is the same as writer C's run at 9ccbc6481. The decode tool reads the click, mesh and well records, exit 0, nothing on stderr.
- Probes, whole numbers only, in /tmp/claude-0/-home-user-Universe24/e136d210-1915-523c-8c8e-0abbdf97855b/scratchpad/hcr2/probes/. The numbers are in /tmp/claude-0/-home-user-Universe24/e136d210-1915-523c-8c8e-0abbdf97855b/scratchpad/hcr2/NOTES.md, and the runs are in /tmp/claude-0/-home-user-Universe24/e136d210-1915-523c-8c8e-0abbdf97855b/scratchpad/hcr2/runs/.
  - P1: every plan on at once.
  - P3: the gradient vertex as one potential.
  - P4: test mutants.
  - P5: the key.
  - P6: the click world's books.
  - P7: the mesh world's ledger.
  - P9: locality.
  - P10: the plan's first integers.
  - P11: the well world under the plan's letter.
  - P12: the decoder on malformed lines.
- The worktree is removed.

=== BLOCKING ===
None.

=== MINOR (ranked) ===

1. The gradient vertex's test does not hold "the two pushes of one potential". Writer B.
   - Where: tests/test_the_tensor24_load.py:148-155. Line 150 unpacks the plan as (one, _, _, factor, target).
   - Claim broken: FRAMES.md 7 names this load test as the test of "the two pushes of one potential". The test checks each term's first reading, factor and target. It never checks the second or third reading, and no test runs the loader's mesh plan through the act.
   - Evidence (P4):
     - I set meshing's second reading to the target row's value. The vertex becomes cubic and is no longer one potential's gradient. The load test still passes, and so does the whole suite (27 passed, via the plugin hcr2/plug/meshmut.py).
     - I set the third reading to the first. It also passes.
     - Only a change of the factor fails the test.
     - The code itself is right (P3, below).
   - Fix: assert that both remaining readings are the unit. Or check J of the loader's mesh plan against -grad V by the five-point stencil, as the engine test's conserved() does for J. P3 is that check: 8 of 8, and its no is 0 of 8.

2. The format accepts any whole "push" of at least 0, although term 5 claims no strength. Writer B.
   - Where: src/tensor24/runner/files.py:90, "push": NONE_BELOW.
   - Claim broken:
     - FRAMES.md 3 says: "No strength: the factor is 1; the universe's "push" is 1 (gravity) or 0 (none)".
     - The plans.py:1 docstring says: "no strength: push 1 or 0".
   - Evidence: the well universe with push 2, 7 or 1000 loads with no departure. pushing multiplies J5 by that number, and the books open by that factor. Only pushing's docstring and the README say so; nothing is said at load. An even key, which also opens the books, is refused by name (M6). A push other than 0 or 1 is not.
   - Fix: a rule that refuses by name any push other than 0 or 1, as ODD does for the key. Or FRAMES 3 names "push" as the strength it is in the file.

3. The odd key's stated reason belongs to the old flip mirror. Writer B.
   - Where: files.py:65-66 (the comment), files.py:69 (the departure's message), load.py:176 (the birth's comment).
     - The comment says the tooth born at (key - 1) div senses "is the one the mirror leaves in place only then".
     - The message says "the one the mirror keeps".
     - The birth's comment says "the one tooth the mirror leaves in place".
   - Claim broken: since A1, step.mirror returns k for every key, so it leaves every tooth in place. "Only then" is false.
   - The true reason, which NOT_CLOSED 11 states: two teeth born at (key - 1) div 2 sum to key - 1 only for an odd key. That sum, with S_L + S_M = 0, forces q_L + q_M = 0.
   - Evidence (P5): on the run test's pair world, key 614400 opens the books at 23 of 1260 rounds. The two teeth sum to key - 2, then to 2 key - 2. Key 614401 opens them at 0 rounds.
   - Fix: the comment and the message name the pair's teeth summing to key - 1. The tests match only the message's prefix "an odd whole number", so they stand.

4. The gradient vertex pairs L and M by part index, and the consequence is not named as a price. Writer B.
   - Where: plans.py:175 (same) and plans.py:177.
   - What happens: light has part 2, but only its first part couples. Its second part takes no gradient vertex in any world (P3: the plan lands on light's row 0 alone). The part index is a place, so this is a role read by place.
   - What is said today:
     - FRAMES 7 has "M_j every row of one part of a tied train".
     - The README has "light's first part L".
     - The load test's docstring has "light's second part in none".
     - No price says that any part of L beyond the tied train's parts passes matter untouched. The mesh world lays its pulse on the coupled part.
   - Fix: name it as a price in FRAMES 7 (and in NOT_CLOSED 4), or lay the vertex for every part of L against every part of M.

5. The two momentum planes are counted by the name senses. Writer B.
   - Where: plans.py:131, `unit = (n + senses) * rows`.
   - Law broken: a count behind a name. The momenta in and out are not the two senses of an axis. The line also ties the loader to the plane layout inside step.stress.
   - Fix: lay the unit as -1, the readings' last row, as contract.pushes, holding, tying and notching already do. Then only the momenta's own planes are named, n rows + r and (n + 1) rows + r, and no 2 is needed. meshing's `(force + 1) * rows` at :173 can take -1 too.

6. Docstrings that say what the code no longer does.
   - Writer A:
     - state.py:23: Plan says "none until the coupling family's one plan (G3)". The plan has held the notch, the held spring and both ties since B2.
     - state.py:75: Layout.mesh says "(none until the gradient vertex)". The loader has laid it since B5.
   - Writer B:
     - files.py:3: "nothing else is laid: no coupling, strength, particle or mass". The chosen block reads six CHOSEN strengths. ARCHITECTURE's World line (decision 35) says the same and is the writer's mend.
     - examples/README.md:3: "the one world the engine runs". The examples now hold five worlds.
   - Fix: one line each.

7. The documents beside the candidate hold stale numbers. These are the Boss's and the architect's files, not a code writer's.
   - PLAN.md, the road to main: the owner's list for M8 gives load 147 and run 291. The tree holds load 155 (B5) and run 295 (B's fold).
   - NOT_CLOSED.md item 11 says the strengths are "0 on the three shipped worlds". The well world ships push 1 and notch 120000. Five worlds ship, two of them with frame strengths above 0, as PLAN B3 and B5 planned and as FRAMES 6, 7 and 11 name them:
     - the click world: hold 1, tie 96000;
     - the mesh world: hold 1, mesh 200000.
     The night's definition of a frame says its strengths are 0 in the shipped worlds. Confirm these two exceptions on the owner's list.
   - Fix: give the numbers as they stand.

=== THE FIRST READER'S ITEMS ===
- B1 (the run back under the push): FOLDED.
  - The fix taken: hypothesis (d). In the loader's plan (plans.py:136-143), J5 lands on the square's 00 and ii rows only, and it reads the momenta only of rows it does not land on. On those rows K1 = K, so M_out is the round's own momentum.
  - B2b's loader route plus A's docstrings (step.py:2, :52, :170) and A's engine test (:284-286). That test's yes is pushed(path=True) at T_d 7, with J1 on the read rows and the clock moving; its no reads the ii rows' momenta.
  - P1: with push, notch, hold, tie and mesh all on at once and an odd key, drawn states at three spans (3, 1000 and 2^20) run back exactly over one round and over six.
  - P11: on the shipped well world, the plan as built runs back at 3 of 3 rounds; the plan's letter (the ii rows read) runs back at 0 of 3.
  - The well world runs back 128 of 128. The README's "the run back returns the lay bit for bit" is now true.
  - The two-plan road is named as the alternative, and its price is NOT_CLOSED 30.
- The known window (writer B, B2b): FOLDED. The well world runs 128 rounds and comes back exact.
- M1: FOLDED. plans.py:38 gives the square the factor 0 by its flag. The load test's wanted pairs are built with 1 - square. The change is named in FRAMES 4.
- M2: FOLDED. The flipped tooth's no is back at engine test :231-232. The test docstring corrects the false identity.
- M3: FOLDED. The run test's pair world now stays inside the room for 1260 rounds. P5 measured it: hold (|x_g|^2 + |x_t|^2) at most 196 of 250, |k|^2 1, books 0, the held train never clicks, the run back exact. The comment states the bound but the test does not assert it; it holds indirectly, since the held train's lines would show if the room were left.
- M4: FOLDED in B's files (the run test's pins spelt as sums are gone) and in C's (decoder test :545 and :560-565).
- M5: FOLDED. B5 lays the Mesh plan at the CHOSEN mesh. A world with no light and tied pair still lays it at the factor 0, as every strength does.
- M6: FOLDED. An even key is refused by name (files.py:67-70), the run test's no is at :241 and :248, and P5 confirms an even key opens the books. Its stated reason is stale (finding 3).
- M7: FOLDED, all six parts: step.py:4, step.py:52, state.py:3 and :74, plans.py:127, the README's window ([0, senses W]), and run.promises/window naming the teeth below 1.
- M8: NOT FOLDED; it waits on the owner's word. The rooms against main stand at frame 237 (230), engine 300 (202), load 155 (113) and run 295 (285); the decoder is lowered to 572 (600). This range raised the engine by 1, run by 4 and load by 15, all within the Boss's ceilings.
- M9: HALF. The frame.turned wording is corrected in PLAN A2 and NOT_CLOSED 25. runner/plans.py is still named by no Home or Test line (scribe_law_check --arch: 1 departure). That line is the writer's mend to ARCHITECTURE on the road to main.
- M10: FOLDED. records.clicked (records.py:279) refuses five causes by name:
  - a train with no card;
  - q 0;
  - a tooth below 0;
  - a tooth not below its card's key;
  - a doubled (round, site, train).
  The test lists each of these in REFUSED (decoder test :527). In P12 the decoder raised nothing on twelve malformed click lines and three malformed train cards. Every one was refused by an earlier shape guard, except a line with no tooth or no train, which reads by the decoder's own rule for absent fields.
- M11: FOLDED AS NAMED. schema.py:2 names MINOR = len(ADDED) as open for the owner.
- M12: FOLDED. step.passing's docstring, step.py's Board line, FRAMES 5 and NOT_CLOSED 31 all say J5 enters no train's X.

=== SOUND ===
- Law scans (on the syntax tree):
  - No literal beyond 0 and 1, and no 1 + 1, in src or in tools/tensor24_*.py.
  - No //, %, divmod, power, shift or true division outside carry.py.
  - No if, loop, comprehension, comparison, boolean operator, where, clip, min, max or abs in engine/.
  - ASCII only.
  - The imports stay within section 5.
  - docs/, .github, uv.lock and the gate's files are untouched.
  - Every probe in the range is whole numbers (no float, no true division, no root).
- The books' form and the run back:
  - A's two docstring commits change no code.
  - The Algebra line now states the half once.
  - k0 = Spokes x senses is one number for both the clock's read and the 00 push.
  - The dial is senses exactly on the rows the push lands on (geared and pushing compute the same set).
- The 24 under the twisted action (P1): 24 of 24 turns commute with the act, clicks included, at every span. This holds with every plan on, with the mesh alone, and with push and notch alone.
- The gradient vertex:
  - It is one potential's gradient: J = -grad V for V = SUM_x mesh C M_j D_i L, at 8 of 8 on 3^3, 5x4x3 and 7x1x1 (P3). Its no (the push onto L dropped or sign-flipped) is 0 of 8.
  - It is local: 14 of 14 perturbations, every plan on, moved nothing past a site's six Meshes (P9).
  - The drive alone reads it; the passing never does.
  - The held hand takes none, and T2 rows take none.
- The mesh world, from its own ledger (P7):
  - The tied hand moves at 106 sites.
  - hold |x|^2 is at most 900.
  - The held hand's |k|^2 stays 1.
  - Light ends at 944 permille of its start.
  - Its key is 1, the strictest detector, and it writes no click line.
  - At the plan's first integers (P10, the README's claim, which no committed file records): mesh 1000 never moves the tied hand. Mesh 2000 leaves the room at round 57 and mesh 3000 at round 28; both then run away with the held hand.
- The click world's books, from my own run's record and ledger (P6):
  - The q sum to 0 at all 2106 places.
  - The two lines at each place have teeth summing to key - 1, before and after.
  - Every tooth is within [0, key).
  - The held train writes no line, and its |k|^2 is 1 at every site and round.
  - The room is at most 1600 of 2500.
  - The largest count is 40.
  - Light and the metric stay at 0.
  - The lines are alike at all 27 sites.
  - The giver totals -108 and the taker 108.
  - The README's run times and ledger sizes match my runs.
- C4: the five new causes, the room folded with no change of behaviour, and records.py at 399 lines.
- A3: whole numbers, measured on the act, its claims within its stated spreads.
- B2b's probe and lays: they run on the act and the built loader.
