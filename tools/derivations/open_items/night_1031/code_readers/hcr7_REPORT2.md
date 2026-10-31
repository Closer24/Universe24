# The seventh hostile code reader, second read: 86ec0e348..5ecb100f5 (writer D's minors a66674061, writer B's re-lay 5ecb100f5), 2026-10-31

(Written by the Boss from the reader's hand-back; the text is the reader's, shortened in layout. Evidence in hcr7/:
mut2.py with mut2_5ecb.out and mut2_86ec.out, fullcheck2.log, gate2.log, runs2/ (click.out, the mesh decode),
lay2_click.out, lay2_mesh.time, hpq_now.out. The worktree removed; nothing edited or pushed.)

VERDICT on 86ec0e348..5ecb100f5: NOT PASSED (three BLOCKING items, each a small fix)

## BLOCKING

1. a66674061 drops the only test that read a real run's click lines, with no reason and nothing in its place: at
   86ec0e348 the run test's pair world read its record with records.read (cause ""), asserted every click line's q
   and tooth whole and the held train's lines; now the pair world writes nothing (tests/test_the_tensor24_run.py:
   292-293), and the lean test only counts click lines (tests/test_the_tensor24_worlds.py:28, :41). Mutant CL2
   (run.clicked, src/tensor24/runner/run.py:123, writes each line's train one past) is caught at 86ec0e348 (KeyError
   0) and survives at 5ecb100f5 (run and worlds tests, 5 passed); CL1 (q negated) and CL3 (the tooth pair swapped)
   survive at both (an older gap). Fix: write.py writes, beside "clicks", a digest of the record's click lines as the
   run wrote them (no digest typed); the lean test compares it and reads each record with records.read, asserting
   cause "": kills CL1, CL2 and CL3.
2. The click lay prints a check it never makes: tools/derivations/open_items/derive/boss/click_lay/lay.py:138 prints
   "so the key's window, an odd whole from 1 to that swing, holds it" whatever the key and the swing (lay.txt step
   3). Fix: compute it (the key odd by Rule3's carry, key <= swing[0]); regenerate lay.txt by the lay.
3. The pair world pins NOT_CLOSED 37's open state and does not guard the promise: tests/test_the_tensor24_run.py:292
   requires the at-rest pair to run away within 1260 rounds (checking only the "round " prefix, not round 766); if
   NOT_CLOSED 37 closes, the test fails with the promise sound (Sofer's point). It guards only that some count past
   the width is named and nothing written (W2, wide dropped, and W4, ledger kept, caught); the promise's edge is
   unguarded (W1, the bound doubled, and W5, one bit loose, survive). Smallest lawful form: (a) a direct edge test of
   run.wide: counts of +-((1 << w) - 1) give []; a count of 1 << w or -(1 << w) in either slot is named "row 0, site
   0: the count ... takes more bits than the width, 128" (checked in a probe); (b) for the unlink path, a world that
   crosses the width by inertia alone (one free gear laid at now (1 << w) - 1, before (1 << w) - 2, no strength),
   named at round 2 with nothing written (not tried); (c) drop the pair world, or keep it as NOT_CLOSED 37's record
   with no assert that it runs away.

## MINOR

1. The click lay's docstring contradicts its own account: lines 14-15 say "no count moves and no click falls" while
   step 5 shows 5187 clicks, the held train's; line 22 says the q sum to 0 and "the held train clicks nowhere" while
   step 4 shows the books open at 2490 rounds and 596 held clicks. Restate it from lay.txt.
2. SEARCH = 1000 (click_lay/lay.py:47) is lawful (a fixed run reading the beat off the sign changes; none of the gate's
   SEARCH shapes) but misnamed beside its "no search" comment: rename it, e.g. BEAT_RUN. REACH = 200 in
   prefixes/write.py:31 is lawful too.
3. The mesh lay misstates whose clicks they are: mesh_lay/lay.py:144 prints "7592 clicks (the Mesh leg's wind is
   counted by no click)", its docstring line 16 still "Clicks: n/a": say the held train's 4302 and the tied hand's
   3290.
4. The click world's yes digest now pins 1 round where it pinned 4 (every gear at rest, momentum-only terms 0 at round
   1; the no case pins no digest of its own). Optional: write.py also writes the 4-round digest, and the test compares
   it.
5. wide does not read the end state (run.py:215, `if at < ticks`): a count past the width in the last round is written
   to the ledger unnamed, against the commit's "writes nothing past it". Say so in run.py's docstring, or read the end
   state too.
6. Light and matter: no new board-side uses (the added "light" lines a re-wrapped README line, the train's file name,
   and a lay.txt line regenerated from the old f-string).

## Checked and found sound

- wide: read from outside before every round beside the dial's and the window's promises, on both slots;
  int(n).bit_length() > width, the width from the universe file; no literal; engine, load and plans untouched; src
  number tokens unchanged.
- D's other minors: hand_per_quantum's probe exits 0, probe.txt byte for byte; g3_frame marked the K = 2 W record; the
  files test's "universe.chosen.{k}" back; the README's |k|^2 lines restated.
- The click world falls as shipped, untuned: its universe file untouched (ticks 5000, spring 10^8, key 50811429, tie
  96000); the lay reproduces lay.txt and setting.json byte for byte (48.8 s); the run tool exits 1 at round 3752,
  naming rows 12, 14 and 20 at all 27 sites past 128 bits, writing no record and no ledger (7m26s under load); the
  README gives Big Pic's cause and NOT_CLOSED 37.
- The mesh world: the lay byte for byte (2m6s); the run 125 of 125 back exact, digest 254bb57990b454b2; 7592 click
  lines (held 4302, tied 3290); the books NOT SHOWN at 5942 of 6018 places from round 20.
- The well: only measure.txt's keys move; the len() is of the shape. The 498: Rule3's carry of 548654125767 x 1000 /
  2^40. The prefixes regenerated byte for byte (1m9s). The lean test can fail: 6 of 6 (LT1 the giver's count +1, LT2
  spring +1, LT3 the next odd key, LT4 K = 2 W restored, LT5 a mesh setting count +1, LT6 an unwritten example folder);
  CL4 (no click line) caught (0 == 27).
- The gate: no refusal and no note; no gate file touched. The full check exit 0, 28 passed in 30.73 s at load 3.6 to
  6.1. No non-ASCII added.

## The Boss's rulings (03:3x UTC)

- BLOCKING 1 and 2, MINOR 1 to 4: writer B, one commit on 5ecb100f5.
- BLOCKING 3: (a) the direct edge test of run.wide, and (c) the pair world kept as NOT_CLOSED 37's record with no
  runaway assert, its run back to the runaway round's eve kept only if it is lawful without a typed round; (b) only if
  cheap. MINOR 5: read the end state too. Writer B, in the same commit.
