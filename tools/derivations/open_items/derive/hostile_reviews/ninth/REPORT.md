# The ninth hostile review: stage 6 after the eighth's changes (af564daac, 54b9e6a63, 83a0b214a to 927071a14)

Verdict: approve with changes, at 927071a14 (a fresh reader, 23:4x UTC 2026-10-28). The eighth review's five changes
work: every mutant behind them dies. But the load still raised on files the checker holds, and 5 of the reader's 29
new source mutants survived every test and the tool (new_mutants.py, its output new_mutants_at_927071a14.out). Each
claim stands on a probe the reader ran.

## Required, and where each went

1. **The load raised on files the checker holds (against 91226e796's claim).** The guard 91226e796 added covered the
   lay's first three arrays alone. The plan's scatter, a dense rows x terms matrix, stood outside it, and so did the
   lay's going and clocks. On a 440 KB universe the checker holds (one T1 train of 10,000 kinds on a hand and 10,000
   cross rows) the scatter asked 26.8 GiB and MemoryError escaped the load; under a cap that holds three of the lay's
   arrays, the going raised (load_raise.py, cases A and B, load_raise_at_927071a14.out). The mutant dropping
   MemoryError from the guard survived. Now contract is a scattered sum, np.add.at over the terms' landing rows into an
   array of the gears' shape, so the plan holds three index columns and the factors and no matrix at all; the lay
   builds its five arrays under the one guard; and a test refuses each of the five in turn and finds the board named.
   After the changes case A loads in half a second and the tool exits 0, and case B names the board
   (load_raise_after.out).
2. **Test gaps beside the eighth's changes 3 (the lay) and 4 (the gradient).**
   - N1, the lay dropping the fine tooth: every gear in the tests had tooth 0. Now a gear is laid with a tooth and r
     is read at its row and site.
   - N2, clocks of one site: the test read the clocks at 0 alone. Now the shapes of a, b, r, the going and the three
     clocks are pinned, and the laid entries counted.
   - N3, the gradient read at its train's first kind: every gradient was of an A1 at kind 0. Now the naive-sum
     universe holds a train [T1, A1] and a gradient of its A1, kind 1.
   - N4, the A1 rule reading the train's first kind: the refusal edits used the one-kind spin train. Now an edit
     refuses a gradient of the potential's T1 (kind 1), and another loads a gradient of the field's A1 (kind 1).
   gradient_kinds.py shows the code right on these files and each of N1, N3 and N4 wrong on one
   (gradient_kinds_at_927071a14.out); after the changes the code stays right on all three (gradient_kinds_after.out).

The reader's mutants again on the head that carries these: none of the 29 survives, the control aside
(new_mutants_after.out). The eighth's 48 rerun on the same head (its L17 and C1 re-aimed at the new lines of the lay
and of contract): the same three survive as at 927071a14, K8, L1 and L3, harmless or equivalent as the eighth reader
said (eighth_source_mutants_rerun.out).

## Follow-ups, and where each went

- The dense scatter was quadratic: one contraction took 0.03 s, 0.13 s, then 0.57 s as the rows and the terms
  doubled at 8 sites (load_raise.py, case C). The scattered sum of change 1 takes its place: 0.4 ms, 0.7 ms and
  1.4 ms at the same sizes (load_raise_after.out, case C).
- Sofer's fuzz_files.py (on scribe-5) crashed in its own harness at seeds 7 and 11 ("Circular reference detected"):
  its mutate() inserts the POOL's lists and dicts by reference and then changes them in place. With copy.deepcopy on
  the three inserts (fuzz_files_deepcopy.py), seeds 7, 11 and 23 ran 20,000 variants each with no raise in the
  checker, the load or the contraction (fuzz_files_deepcopy_seed{7,11,23}.out). Sofer mended his harness in
  scribe-5 505db14c6 (6483433943: 0 raises in 43,000 variants). Seed 7 again after the changes: the checker holds
  1,726, the load names 182 and loads 1,544, and nothing raises (fuzz_files_deepcopy_seed7_after.out).
- The adopted gate misses six spellings of a wrap in runner/board.py (gate_board_dodges.py, .out):
  np.unravel_index's second part, == as the whether, np.equal, np.digitize, getattr(np, "re" + "mainder") and
  vars(np)[...]. The adopted text never claims to catch them, so the adoption stands; they go to Sofer for his next
  round.
- tools/tensor24_files.py exits 1 both for a named departure and for an uncaught raise. Not changed: the number rule
  holds the tools to 0 and 1, a raise prints its traceback where a departure prints its name, and no file the checker
  holds is known to make the load raise after change 1.

## What holds

- At 927071a14 every fast check passes: ruff, ruff format, mypy (61 files), tests_shape, record_code_shape,
  engine_gates, documents_gates, Sofer's gate (refusals 0, notes 2), tensor24_files, and 247 of 247 Tensor24 tests.
- The eighth's source_mutants.py reruns at 927071a14 identical to its committed after-run: 3 of 48 survive, and every
  mutant behind the eighth's five changes dies. 24 of the reader's 29 die there too, all 15 of the checker's among
  them.
- The frame's kinds' images separate right from wrong: 6 mixings the 24 keep pass and 7 near misses fail.
- Sofer's original fuzz at 91226e796, seed 7, gives the Boss's numbers: 1,701 held, 166 named, 1,535 loaded, no raise.
- 54b9e6a63: the three gate files are byte for byte those of scribe-5's a0dd6b376; the self-test runs 861 cases with
  none parted, and the tree passes the gate.
- af564daac: the plan's width line matches the code. The decoder is unchanged since 823690afc, and the seventh
  review's decoder_readings and decoder_precedence probes rerun identical to their committed outputs.
- 3fbbd1cd0: 43 of the 125 tables are not 0, each primitive with its first entry positive, all Python integers.
- The rate promise is exact: a rate from -1 to Gamma + 1 runs back at every dial in [0, Gamma) exactly when it lies
  in [0, Gamma].

The probes run as `python3 -I <probe> <a worktree> [...]`, each docstring naming its arguments; load_raise.py,
gradient_kinds.py and fuzz_files_deepcopy.py pass the gears' shape to contract where it takes it, so each runs at
927071a14 and after the changes.
