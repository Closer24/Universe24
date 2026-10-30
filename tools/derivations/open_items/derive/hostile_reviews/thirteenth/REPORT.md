# The thirteenth hostile review: the engine since the tenth (fc8c810ff, 610fef782, d61cdb7bd, e0c52c053)

Verdict: approve with changes (a fresh reader, 02:5x UTC 2026-10-29). Two changes of text are asked; no defect of the
code of e0c52c053, fc8c810ff or 610fef782 was found, and d61cdb7bd is documents alone. Each claim stands on a probe the
reader ran. The probes stay in the reader's scratch (decision 26), named below.

## Required, and where each went

1. **The charge identity stated without its condition.** The reader derives, for a hand whose two rows share W, W+,
   s, D and the grip, over one synchronous round: Q*+ - Q* = SUM torques / (2 s) + SUM T_k Im(conj(a) q). The test ran
   with no plan, so q = 0. With J on the identity as stated fails in 8 of 8 rounds, and with the kick's term it holds
   in 8 of 8 (charge_identity.py, the derivation in its docstring).
   - The test's `kept()` now runs both: with J off, and with J on, where the kick's term is read from the drive's own
     carry, T_d q = J + r_d - r_d+, and J is asked to be nonzero in every round. A mutant that drops the kick's teeth
     passes with J off and fails with J on, so the test reads J's path. With J on the gears square each round, so
     that run takes four rounds on gears below 2**10.
   - The conditions (the hand's rows alike in W, W+, s, D, T_k and T_d) stand in the test's docstring, the room's
     reason and the eleventh report.
2. **Item (u) shown settled.** The plan's line 600 read "Past, as decision 25 derives it", where the owner's quoted
   word covers Postulate 6 alone. It now reads "Past, as decision 25's reading derives it, put to the owner", the
   item stays among the owner's open decisions, and the owner is asked.

## Follow-ups, and where each went

- **What the charge test cannot see** (mutants_charge.py, 36 mutants of step.py and mesh.py, every one failing the
  suite): the pull's sign, the spring and J's path but for the kick leave the charge where it was, as the derivation
  says; the formula law catches each.
- **The lay's arrays** were told apart by `id()` alone, and two views would pass (lay_alias.py): the test now asks no
  two arrays to share memory.
- **The run back's swaps** (run_back_swaps.py): a swap of T_k and T_d failed only by a raise at a T_k of 0. `varied()`
  draws T_k from 2 where the divisors are, and a mutant swapping them in the run back is in the list. The parted round
  ticked 6 to 9 of 60 clocks (back_parted_ticks.py): it now runs every due beat and asks a gear to tick.
- **contract() on an int64 factor** wraps silently, and no load makes one (contract_widths.py): the Plan's comment
  says the factor is Python integers.
- **Stage 7c** was named and not defined: the plan's tick line now says what 7c brings.
- **Decision 25's family** read "linear in (Gamma / N)^n, n = 0", which is linear in 1: its member n = 0 is now named
  the logarithm, the family's limit.

## What holds

- The fast checks, the gate (refusals 0, notes 2) and the 298 Tensor24 tests (fast_checks.out).
- The per-site lemma of the charge, 0 failures in 200 trials; with W parted on a hand's rows, 200 of 200 fail
  (charge_identity.py). The torques are about 2**313 a round, and the pull's term is nonzero at 60 of 60 sites and
  sums to 0 (charge_vacuity.py).
- W, W+ and T_d at least 2 in every layout `back()` draws; all 73 two-field swaps of the engine's records fail the pin
  test, and Plan's three adjacent swaps pass the rest of the suite without it (records_swap.py,
  records_swap_layout.py); the eleventh's survivors r4 and r5 die, d1 and s12 stand equivalent
  (mutants_s12_survivors_at_head.out).
- fc8c810ff: J of Python integers equal to the naive sum on int64, bool, float and uint8 gears, exact at strength
  2**300 and gears 2**400 (contract_widths.py).
- engine/ by its syntax tree: no branch, comparison, loop, list literal, len or number beyond 0 and 1, attribute
  access on arrays alone, no float, no floor division or modulo outside carry.py (laws_ast.py).
- 610fef782's three gate files blob for blob scribe-5 43cd5981d, the head's equal to 6199bb040's; the self-test 877
  cases at 610fef782 and 918 at the head, 0 parted; the ninth review's 11 spellings of a wrap caught
  (gate_selftest.out, gate_board_dodges_at_head.out).
- ENGINE.md's room numbers equal ROOM's sums, and the eleventh report's counts reproduce.
