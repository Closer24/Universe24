# The fourteenth hostile review: the merged engine tests, the files' one checker, the room by file (cb7a54943, c98cf9154, a49138552, 1de239790, 1a4d1fdfe)

Verdict: approve with changes (a fresh reader, 05:2x UTC 2026-10-29). Four changes are asked: one in the tests' room
rule, one in the checker's tests, one in how the checker's format is spelt for Sofer's gate, and two of text in the
plan. Each claim stands on a probe the reader ran. The probes stay in the reader's scratch (decision 26), named below.

## Sofer's question: the merged file against the four it replaced

- 356 source mutants over engine/step.py (209), mesh.py (19), contract.py (9), runner/board.py (111), rounds.py (5)
  and rewind.py (3): operator flips, dropped terms and negations, 0 and 1 swapped, arguments and tuple elements
  swapped, a call replaced by its argument, a call deleted (mutate.py, mutants_summary.out).
- The merged file kills 349, 16 of them by the timeout (over 90 s, nine times the clean run). It lets 7 through, and
  the four old files let 6 of those through too: five are equivalent (moveaxis on two axes; three swaps among r, go,
  rd and ph in untick's State that sources() never reads; uncarry's arguments), and one, the board's Meshes as a list
  of six arrays, behaves the same in the engine.
- One mutant only the old files kill: the board's neighbours as a list, which the old board file caught through its
  own mutant's `nb[:, ...]`. In the suite, test_the_tensor24_load.py and test_the_tensor24_light.py fail 6 tests on
  it, so the loss is harmless (board_list.out). The laws that reach kinds.py stand alike in both files
  (kinds_laws_diff.out).

## Required, and where each went

1. **The room counted twice** (tools/tests_shape.py): `lines_in(base, "tests/") + room_of(head)` added every ROOM
   entry on top of a base that already held its lines, so at 67b765312 a new test of 100 lines with no budget went
   unseen (room_probe.out, room_split.out). The rule is now the head's budgets less the base's, `+ room_of(head) -
   room_of(base)`, and tests/test_the_tensor24_room.py (its own budget, 50) refuses a test with no budget beside a
   budget the base already holds; it fails on the old rule.
2. **The checker's tests missed the rewrite's promises** (checker_mutants.out, checker_slip.out): making version,
   integers, trains, shape or ticks optional, naming every departure twice, and reading a null as absence each passed.
   tests/test_the_tensor24_files.py now has an absence edit for every key the format requires, a null edit for each
   key a file may leave out (couplings, gears, weight), and a file of two departures whose each is named once. Each
   of the reviewer's mutants fails it; the file's budget is 400.
3. **Keys hidden from the note KEYS** (keys_blind.out): `dict.fromkeys` is read by no rule of the gate, so a key added
   through it went unseen in 4 of 6 ways. The integers and the train's pair are now dict literals in
   runner/files.py, every key a constant the gate reads; the five integers' keys are new paths for Sofer to list.
4. **Two of text in 1de239790:**
   - the hour of 6487250651: the plan and TENSOR24.md now say "relayed by David at 03:40 UTC", the comment's own time;
   - Postulate 6's enforcement: the plan now names that the law's text (ALGEBRA.md line 35) still has the engine
     build the time gear's coupling with itself, which the count does not hold, and asks Sofer which text goes.

## Follow-ups, not blocking

- **Vacuous laws** (vacuity.out): tests/frame.py's `forth = bool(o1) or ...` is always true for an Out, so "a step
  undoes its run back" is never asked; the clock file's "both ways" law (gear of ungear at teeth to 2**80) was not
  carried over; in alike(), T_k is never read (q is 0 there); law() sends "formula" to the file's own law, so the
  frame's formula property and "kinds" are not run; no divisor above 19 and no full rate but 9 is drawn; model()'s
  `np.array_equal` takes a list for an array. Each is the merged file's to strengthen, with a cheap assertion test
  first, so that the mutants that now hang fail in seconds (Sofer's parity run, 6488350975, item 5).
- **OPTIONAL by key name** in every form (files.py), where the form's own entry could carry it; the walker's "a list
  of one train or more" is the trains' words in a generic walker.
- **Old behaviour kept** (checker_echo.out, checker_nulls.out): a part that is not whole also names the sine, a den of
  0 or below also names the pinion and the sine, and `"sine": null` on a train of one gear passes (load never reads
  it). c98cf9154's "names every departure" holds within a file's forms; the cross-references and the setting are
  read once the forms hold.
- **The gate's copies:** scribe_scan_keys.json and SCRIBE-GATE-1.md lag scribe-5 (0aae017f8); adopting them makes a
  run without origin/scribe-5 read as the gate does.

## What holds

- The checker, old against new, on 6,494 hostile copies: neither raises, the new never passes what the old refused,
  no old message is lost, no departure is named twice, and load() never raises on a file the new checker passes;
  nesting to JSON's limit, 5,000-digit integers and sides to 2**997 raise nothing (checker_fuzz.out,
  checker_edges.out).
- The room: a file one line over its budget is refused by name, and the twelve budgets are each file's lines
  rounded up to 50.
- The code's laws: no `//` or `%` outside carry.py, no number beyond 0 and 1, no float, and no if, comparison or loop
  in engine/ (laws_scan.out). The gate: refusals 0, notes 2; 1a4d1fdfe's four files blob for blob scribe-5 bcc070bb9
  (gate.out, blobs_verdict.out).
- The fast checks all pass; the Tensor24 tests 346 passed; the merged file runs in 10.8 s against the four's 17.1 s
  (fast_checks.out, pytest_tensor24.out).
- Decision 25 as Sofer entered it, and decision 26 as done, with the caveats above.
