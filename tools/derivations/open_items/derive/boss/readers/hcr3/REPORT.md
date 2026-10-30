# The third hostile code reader on 87f88322d..996df846f (node-live), 2026-10-30

(Written by the Boss from the reader's hand-back, the reader's harness having refused the write; the text is the
reader's. The reader's evidence is in this folder: gate.txt, check.txt, plug/, probes/ (with q1.out and q2.out) and
push/. The reader's worktree hcr3/tree was removed; to rerun a probe, re-add a worktree at 996df846f.)

VERDICT on 87f88322d..996df846f: PASSED

No BLOCKING finding and three MINOR ones, all in writer B's new test lines and wording. No law is broken. The second
reader's minors 1, 2, 3, 5 and 6 are met, and no shipped world changes.

WHAT I RAN (my own detached worktree of 996df846f under hcr3/, removed when done)
- The gate (gate5, --base origin/main --summary): 0 refusals and 6 notes, the same six as before. They are INDICATOR
  load.py:110 and :112 and plans.py:92 and :96, and PIN load test :73 and :76.
- The full check (CHECK_BASE=origin/main): exit 0, 27 passed.
- A syntax-tree scan of src and tools/tensor24_*.py:
  - no literal beyond 0 and 1, and no 1 + 1;
  - no //, % or divmod outside carry.py;
  - no if, loop, comparison, mask or bound in engine/;
  - the only hits are six pathlib joins in the tools, which the range does not touch;
  - the range's eight files are ASCII.
- Mutants as pytest plugins (hcr3/plug/). Probes in whole numbers, using an integer LCG through carry (hcr3/probes/).

=== BLOCKING ===
None.

=== MINOR ===

1. The load test still lets one push of the vertex be laid twice. So it does not hold "one potential's two pushes",
   although it now says it does. Writer B.
   - Where: tests/test_the_tensor24_load.py:151, where terms is a dict keyed by (first, target), and :155.
   - The claim: the docstring (:100) and tools/tests_shape.py TENSOR24_LOAD ("one potential's two pushes and never a
     cubic vertex").
   - Evidence:
     - plug/mut4.py lays meshing's onto-M block (or its onto-L block) a second time.
     - The mutant's J is then no potential's gradient. J(d1).d2 = J(d2).d1 holds at 0 of 6 drawn pairs, against 6 of
       6 for the true plan, on three worlds (probes/q1_one_potential.py).
     - The load test passes and so do all 27, for each of the two. The duplicate term collapses in the dict.
     - Laying every term twice (the strength doubled) also passes the load test.
   - Fix: count the terms with a factor against wanted, as the passing's check does with len(got) == len(one). Or
     assert J(d1).d2 = J(d2).d1 on the loader's plan, which needs no V. The test has no slack at 155.

2. The files test holds files.SWITCH on one side only. Writer B.
   - Where: tests/test_the_tensor24_files.py:79, "a push of 2".
   - Evidence:
     - SWITCH written as v <= 1 passes all 27, although a push of -1 then loads, the books' form turned the other way
       (plug/sw.py).
     - SWITCH written as v != 2 also passes all 27.
     - The true rule refuses 2, -1, true and 1000 by name, and 0 and 1 load (the files tool on copies of the well
       world, hcr3/push/).
     - ODD's floor has the same gap, inherited from outside this range: ODD without v >= 1 also passes all 27
       (plug/oddm.py).
   - Fix: hold a push below 0 beside the push of 2. No single value catches both v >= 0 and v <= 1. The test has no
     slack at 310.

3. files.py's new text names the push two ways. Writer B.
   - Where:
     - files.py:3 counts the push among "the free strengths", but SWITCH's message (:75) and plans.py:1 say term 5
       claims no strength.
     - files.py:72 says the books' form is laid "at the factor 1 or not at all". At push 0 the loader lays every term
       at the factor 0 (168 terms on the tensor24 world).
   - Fix: one line each, for example "the key, the push's switch and the four strengths", and "or at the factor 0".

=== THE BRIEF'S QUESTIONS ===
- files.SWITCH is a lawful rule of the format, not a number in disguise:
  - it spells no number beyond 0 and 1;
  - v * v == v admits exactly 0 and 1, the two literals the law allows, as v in (0, 1) would;
  - files.vocabulary already uses the same test of being its own square (:255, :257);
  - the files' check reads it outside the Node-clock, as it reads ODD and NONE_BELOW.
  The loader does not guard the push itself, so a probe that calls load directly (drive_mirror) keeps its own
  strength.
- The unit as -1 is the same row as before on every world. probes/q2_unit_row.py compares 996df846f's plans with
  87f88322d's plans.py on the five shipped worlds:
  - every other field of the push and Mesh terms is identical;
  - the old units are the readings' last rows: (Spokes + 2) rows in stress and (axes + 2) rows in readings;
  - J5 and the Mesh J are the same on a drawn state. J5 is not 0 at 2592 entries on the well world, and the Mesh J
    is not 0 at 360 on the mesh world.
  Only engine.contract reads the unit legs, and frozen_edge's probe reads only the push's first two readings.
- No shipped world changes. The Boss's runs at 996df846f, each exact 1:

  | World | Digest | Rounds back |
  |---|---|---|
  | tensor24 | 540e503cad44 | 10 of 10 |
  | live | cfef203d5dd5 | 100 of 100 |
  | well | 05586b5db17f | 128 of 128 |
  | mesh | 00fd62494c9a | 125 of 125 |
  | click | f351582ede39 | 5000 of 5000 |

  - The click world (the rerun after the restart): 4212 lines at 2106 places, the books open at 0 places, giver
    -108, taker 108, and the decoder exits 0.
  - Every world's ledger is byte-identical to the second reader's run at 87f88322d.
  - Every record is identical after its header line, which names the record's own file.

=== THE SECOND READER'S MINORS ===
- 1: MET. The true code passes the load test. The second-reading mutant and the third-reading mutant each fail it at
  :155, the unit's assert, and nothing else fails (26 of 27 pass). At 87f88322d both passed it (hcr2 P4).
- 2: MET. files.SWITCH refuses by name every push but 0 or 1: 2, -1, true and 1000 are named, and 0 and 1 load. All
  five worlds stand at 0 or 1.
- 3: MET. files.py:65-67, ODD's message (:70) and load.py:176 now give the pair's two teeth summing to key - 1 as the
  reason, and no mirror reason is left. The arithmetic holds: two teeth at (key - 1) div 2 sum to key - 1 only for an
  odd key, and with S_L + S_M = 0 and both remainders in [0, key), q_L + q_M = 0 and the sum is kept.
- 5: MET. pushing's (n + senses) rows and meshing's (force + 1) rows are gone. The unit is -1, as in
  contract.pushes, holding, tying and notching. It is the same row (q2), and the digests are unchanged.
- 6: MET. These lines now say what the code does: state.py:3, :23, :51 and :75 (writer A), and files.py:3 and
  README:3 (writer B), apart from the word for the push in finding 3. ARCHITECTURE.md:126 (in docs/, outside the
  range) still reads "no coupling, strength, particle or mass".

Note: before the gate I ran one `git fetch` by mistake. It moved no ref: origin/main was last updated at 18:21 and
origin/node-live at 23:19, both by push. I committed and pushed nothing.
