# The eighth hostile review: stage 6 (83a0b214a, 3fbbd1cd0, 91226e796)

Verdict: approve with changes, at 91226e796 (a fresh reader, 23:1x UTC 2026-10-28). The one defect of the code it
found, the load raising on a universe without couplings or a setting without gears, was already mended in 91226e796
on Sofer's own fuzz. The changes it asks are of the tests: 11 of 48 source mutants survived every test and the tool
(source_mutants.py, its output source_mutants_at_91226e796.out). Each claim stands on a probe the reader ran.

## Required, and where each went

1. **The joint untested:** the tests built the kinds and tables with their own transpose and never called main.made
   or kinds.inverse, so main.made passing the turns as their own inverses, and kinds.inverse returning the turn,
   survived; under them 33 of the 43 tables change and none of those is kept by the 24. Now the kinds' test builds
   through kinds.inverse and pins main.made's kinds and tables equal to its own, and the load's test takes its kinds
   and tables from main.made.
2. **T1 the turn itself, unpinned:** T1 and T2 conjugated by a third turn of the axes keep every character, stay a
   representation and leave the dot, the cross and A2 x T1 -> T2 as they are, while the load reads the gradient's
   component j as the axis j and the frame's stored(m) takes T1(g) = g. Now the law forms pins, on the 24, A1 = 1,
   T1 = the turn, A2 = the sign of its axes' permutation and T2 = A2 T1, with that mutant.
3. **The lay on a later train:** the lay dropping a train's first row survived, since the test laid on train 0
   alone. Now a gear is laid on the last train, whose first row is the earlier trains' rows, and every going, dial,
   count and time is checked at 0.
4. **The gradient's coverage:** the gradient read at part 0 and the A1 rule read on the first side alone survived.
   Now the plan's naive sum holds the gradient of a hand's second part, and an edit puts the gradient of a T1 train
   on the second side.
5. **The rate promise's edge:** at the dial 0 a rate of Gamma + 1 still runs back, so a bound one past survived. Now
   the test runs at the dial's top, Gamma - 1, where the full rate runs back (k = 1) and one past does not (k = 2),
   and the promise names a rate of Gamma + 1; every rate at -1 does not run back (k = -1).

The mutants again on the head that carries these: 3 of 48 survive (source_mutants_after.out), the three the reader
named harmless or equivalent: E's basis in its other equivalent order (no train holds E at stage 6); the last seed
not 0 in place of the first (equivalent, the sign being fixed by the first entry); the greatest common divisor
without its absolute value (primitive() fixes the sign).

## Follow-ups, and where each went

- kinds(matrix, unit) held E right for the identity's unit alone: the parameter is gone, the unit is the board's
  axes, made inside.
- The State's rate comment and the schema's k comment said the load holds the rates, where load() calls promises()
  only from stage 7: both say so now.
- The frame's kinds' images had no positive control: a mixing the 24 keep (each T1 row fed the A1 row's difference
  across its own axis) now passes them at three seeds.
- Not changed: a board that fits the index range but not the machine's memory may be killed by the system before
  the lay names it; tools/tensor24_files.py stands outside check.py, and the example holds no coupling.

## What holds

- Every fast check and Sofer's gate (refusals 0, notes 2) at all three commits; 240, 242 and 243 of Tensor24's tests.
- With the board's axes the five kinds are representations with Sofer's characters, element by element against his
  kinds_ref.py; kinds.inverse gives rho(g^-1); every array is of whole numbers.
- The tables solved exactly with fractions: 43 channels of dimension 1 and 82 of 0; every C on its equivariant
  line, primitive, 0 exactly on the forbidden channels, equal to a naive group sum; at 3fbbd1cd0 all 43 start
  positive.
- contract against a naive loop on 300 random plans: 0 differences, Python integers to 902 bits.
- 37 of the 48 mutants were killed at 91226e796, all 17 of the checker's among them.
- Sofer's gate refuses each planted break (an if, a 2, a float and a floor division in main.py; the runner importing
  the engine and the engine the runner; len in the engine).
- ENGINE.md's room numbers equal tests_shape.py's ROOM; the plan's changed lines match the code.

The mutant script runs as `python3 -I source_mutants.py <a worktree>`; its outputs stand beside it.
