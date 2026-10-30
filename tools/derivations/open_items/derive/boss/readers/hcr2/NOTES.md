# The second hostile code reader: notes (f72067cdf..87f88322d, node-live, tree at 87f88322d)

## Ran
- gate5 scribe_scan --base origin/main --summary: 0 refusals, 6 notes (INDICATOR load.py:110, :112; plans.py:92, :96
  in tying; PIN load test :73, :76). gate.txt.
- CHECK_BASE=origin/main tools/check.py --full: exit 0, 27 passed. check.txt.
- scribe_law_check --arch .: 1 departure, src/tensor24/runner/plans.py named by no Home or Test (M9 stands; the check
  is not among tools/check.py's ratchets).
- Worlds by tools/tensor24_run.py on this tree (runs/):
  tensor24 10 rounds exact 1 digest 540e503cad44 (1 s); live 100 exact 1 cfef203d5dd5 (54 s); well 128 exact 1
  05586b5db17f (142 s); mesh 125 exact 1 00fd62494c9a (27 s), no click line; click 5000 exact 1 f351582ede39
  (1026 s), 4212 click lines.
- decode tool on click, mesh, well: reads, raises nothing; click: not 0 at 0 of 2106 places.

## Probes (probes/, whole numbers)
- p1_all_plans: push 1, notch 120000, hold 1, tie 96000, mesh 200000, odd key, cube of 3, drawn states at spans 3,
  1000, 2^20: the 24 under the twisted action 24 of 24 (clicks included) at every span; untick(tick s) = s and six
  rounds out and back exact at every span; the same with mesh alone and push+notch alone.
- p3_one_potential: the loader's mesh plan's J = -grad V, V = SUM_x mesh C M_j D_i L, by the five-point stencil: 8 of
  8 on 3^3, 5x4x3, 7x1x1; the no (onto-L dropped or sign-flipped): 0 of 8. Lands on light's row 0 only (its second
  part never) and the T1 rows of each tied train.
- p4_load_test_mutants: the load test's plans test passes with meshing's second reading set to the target's value
  plane (a cubic vertex) and with the third reading set to the first; fails only for the onto-L factor doubled.
  The whole suite (27) passes under the cubic mutant (plug/meshmut.py).
- p5_key_and_pair: P8 the run test's pair world at key 614401: hold (|x_g|^2+|x_t|^2) <= 196, |k|^2 1, books 0,
  held clicks 0, run back exact, 162 lines. Even key 614400: books open at 23 of 1260 rounds, teeth sum key - 2 then
  2 key - 2. Even 614402 and 4096: books 0 here (teeth sum key - 2).
- p6_click_books (on my click run): books 0 at 2106 places; the two lines' teeth sum key - 1 before and after at
  every place; teeth in [0, key); held train no line; |k|^2 1; room <= 1600 of 2500; largest 40; light and metric 0;
  lines alike at all 27 sites; q by train giver -108, taker 108.
- p7_mesh_ledger: tied hand moved at 106 sites; hold |x|^2 <= 900; held |k|^2 1; light's first part 845384 ->
  798810 (944 permille); light's second part 0 throughout.
- p9_locality: every plan on, 5^3, 14 of 14 perturbations moved nothing past the six Meshes.
- p10: the plan's first integers (Gamma 1000, mesh 1000..3000, 400 rounds): see p10.out.

## Findings (draft)
- MINOR B plans.py:131 (unit = (n + senses) * rows): the two momentum planes counted by `senses`; -1 (the
  readings' last row, as pushes() and the other plans lay the unit) needs no count.
- MINOR B load test :148-155: mesh check reads only first/factor/target (p4).
- MINOR B files.py:65-69 and load.py:176: the odd key's reason stale (the mirror keeps every tooth).
- MINOR B meshing per part: light's second part coupled to nothing; not named as a price.
- MINOR A state.py:23 and :75: stale "none until" docstrings.
- MINOR (docs) PLAN road-to-main list stale (run 291 -> 295, load 147 -> 155); NOT_CLOSED 11 "0 on the three
  shipped worlds" while five ship.
