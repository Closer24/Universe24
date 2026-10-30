# The tenth hostile review: the ninth review's changes to stage 6 (0ff2ae0dc)

Verdict: approve with changes, at 0ff2ae0dc (a fresh reader, 00:4x UTC 2026-10-29). The scattered sum gives the right
values and the lay's guard holds. But J took the dtype of the gears its caller passed, and 8 of the reader's 34 new
source mutants survived every test, the tool and Sofer's gate (mutants_s11.py, its output mutants_s11_at_0ff2ae0dc.out).
Each claim stands on a probe the reader ran.

## Required, and where each went

1. **J of the caller's dtype.** contract made its source as `0 * gears`, so int64, bool or uint8 gears gave a J of a
   fixed width (an OverflowError past 64 bits), object gears holding np.int64 gave np.int64 entries, and float gears gave
   a J that is silently inexact (contract_equiv.py, .out); the architect's ruling refuses every fixed width. Now the
   source is `np.zeros_like(gears, dtype=object)`: Python integers whatever the gears hold. Sofer's gate accepts the
   spelling (gate_alternatives.py, .out).
2. **Gaps in the load's tests beside the changed code**, each survivor with the check that now kills it:
   - S1 and S2, J added onto or written into the caller's gears (every test passed gears at 0): the naive-sum test
     passes gears of 80 bits and checks them unchanged after;
   - S3 in its new spelling, the source of the gears' own dtype: the same test passes int64 gears and finds a J of
     Python integers;
   - S10, the plan's factor as int64 (no strength passed 64 bits): the naive-sum test runs again with every strength
     shifted by 70 bits;
   - S18 to S20, the lay's arrays, the going or the clocks as int64 (the test pinned shapes alone): the gear test lays
     a, b and the tooth past 64 bits and asks dtype=object of every laid array;
   - S21, b written at every site of its row (b's entries were never counted): b's laid entries are counted;
   - S22, the lay's bound read on train 0 (every component laid was below the light's two rows): a gear is laid at the
     last train's last component.

   The reader's six checks (proposed_checks.py) all hold on the head that carries these (proposed_checks_after.out).
   Its 34 mutants again: 3 survive, the three it named equivalent (mutants_s11_after.out): S11, the plan's two reading
   columns swapped (the product commutes); S17, the strides' refusal falling through (the load discards a refused plan);
   S23, the three clocks one array (the lay returns one array three times already). S1 to S3 aim at the old line; their
   aims at the new one, `gears + 0`, `gears` and `np.zeros_like(gears)`, each fail the load's test.

## Follow-ups, and where each went

- The guard names what the allocator refuses. With memory overcommitted, four large object arrays may each be granted
  and the system may stop the load where it would have raised; the checker's parse and the plan's lists stay unguarded
  and grow with the file. Not changed: the reader reasoned it and did not run it on the shared machine, and no limit is
  the engine's to set (law 11).
- Sofer's fuzz_files.py at origin/scribe-5 a77a90e3b calls contract without the gears: told to Sofer at 00:1x UTC; his
  505db14c6 mends the harness's circular document.
- The record: ninth/load_raise_at_927071a14.out was made by an earlier text of the probe; it is rerun at 927071a14
  with the probe's text as committed, and its outcomes stand (both raises, the contraction 0.04 s, 0.16 s and 0.63 s).
  The eighth's source_mutants.py, its L17 and C1 re-aimed at the ninth's lines, runs at 0ff2ae0dc and after, its
  committed runs standing for the strings they were made with (the README says so). ENGINE.md's room sentence named
  the fine tooth on a later train's gear, where it is laid on the first train's: said right. tools/tests_shape.py's
  reason for the load's room names the newer tests.
- The lay's dial, count and time are one array returned three times: harmless while nothing writes a state array in
  place (the engine writes none).

## What holds

- At 0ff2ae0dc every fast check passes, and 250 of 250 Tensor24 tests.
- contract equals the old dense form and a naive loop on 600 random plans: 360 with repeated landings, 90 empty, 335
  with integers of 200 to 1,000 bits, 438 with negative factors. With object gears every entry is a Python integer, J
  does not depend on the gears' values, and the caller's gears stay untouched. It keeps the laws: + and * alone, the
  number 0 alone, no branch and no loop, each site's column read alone.
- np.zeros raises ValueError or MemoryError alone at every board size the reader tried, up to 2^1000 sites
  (zeros_raises.py, .out).
- 43,200 coupling rows over every kind, part, operand and target load with no raise, every refusal named; the 3,537
  rows taken (13,797 terms) contract to the naive sum with huge readings and strengths past 64 bits; boards of 2^31 to
  2^1000 sites are named; values of 2^1000 load exactly (load_edges.py, .out).
- The ninth's probes run at both commits and reproduce their outcomes; its fuzz copy gives 1,774, 182 and 1,592 at
  927071a14 and 1,726, 182 and 1,544 at the head, and a new seed 31 raises nowhere.
- The eighth's 48 mutants at the head leave K8, L1 and L3, and the ninth's 29 leave none.
- ROOM's 18 entries for the load's test equal its functions' lines and sum to ENGINE.md's figure; the ninth's report
  matches its probes' outputs; the README's rows match the folders.

The probes run as `python3 -I <probe> <a worktree> [...]`, each docstring naming its arguments; their outputs stand
beside them.
