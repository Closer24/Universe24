# MIN2, read by the hostile mathematician (2026-10-31)

(Written by the Boss from the reader's hand-back at 08:2x UTC, the reader's harness refusing the write; the text below
is the reader's, word for word.)

My harness refuses report files from me, as it did for S/min1_math/REPORT.md, so I did not write S/min2_math/REPORT.md; the whole report is below.

**The text and how I checked it.**
- The text is S/min2_frozen/MIN2.md (562 lines, sha256 4c0286f4e9240f94...). All 1,229 sums in FROZEN.sha256 check.
- I reran from a copy at S/min2_math/copy. Whole numbers, python -I, nice -n 19, one process at a time. Every run was gated on load below 8 (S/min2_math/chain.log), except one lapse noted at the end.

## VERDICT on MIN2: PASSED

There is no BLOCKING item.
- My B1 is met: one standing, split by cause exactly as the Boss's 07:5x MIN1 bullet rules.
- Each of my MINORs 1 to 10 is met, and on MINOR 9 MIN2 corrects me.
- The physicist's m1 to m8 are met, as MIN2's section 1 maps them.
- Its figures, forms, 24 and phases reproduce.

The weakest part is the build list's tests (MINOR 1). Fixing it is a condition before items 3 and 4 are built.

## MINOR

**1. The build list's tests cannot keep (c) waiting for its Mesh part.** Places: section 8, item 3's test (ii) and item 4's tests; mutants.py laid. This is the mutant that parts only on the strengths-1 world.
- Item 4 (the teeth) has no unit-strength test. A build that holds only the as-laid live teeth passes every test item 4 lists. Such a build drops the (c) teeth before their ruling. MIN2's own ABC form is exactly that build, byte for byte on every shipped world (section 4; my reruns).
- A run at the unit strengths would not catch it on click either.
  - MEASURED (teeth1.py: click, every chosen strength but the key at 1, the world's own lay, 20 rounds): the 24 (c) Mesh sides per Node-clock never leave their birth, 0 of 648 entries.
  - DERIVED reason: the click lay is the same at all 27 sites (setting.json: 54 gears, 1 distinct per-site set). The act is covariant under the board's translations, so the state stays alike at every site. Every stretch and gradient then stays 0, and so does every Mesh passing and gradient-vertex push, at any mesh strength.
  - Overturned by my own measurement: I expected this run to catch the teeth.
- So item 3's test (ii) sees only the push and notch part of (c).
  - The as-laid mutant parts through those, at round 3. In an alike state the push's kinetic part and the notch still act.
  - A mutant that drops only the Mesh's (c) passes test (ii) for good. That part is the 24 sides, 12 Mesh-plan terms and 24 coupling entries per Node-clock.
- The run is also short. I reran mutants.py laid for 5 rounds: the structural pruning never parts; the mutant parts at round 3, not 1 or 2; as laid it never parts. So a 2-round test (ii) would pass the mutant.
- Fix: give items 3 and 4 a static test, which cannot miss:
  - every plan's kept terms, and the coupling entries, equal those whose factor is not 0 at the unit strengths, term by term;
  - the held sides equal the sides live there, side by side;
  - keep the runs beside it, adding one on a lay that is not alike across sites;
  - mutant: the as-laid live set (MIN2's ABC), which must fail.

**2. S1 before (b): the scope of the derivation.** Places: section 2 ("so a factor 0 with every strength at 1 is 0 at every strength"); build items 1 then 3; cause.py:99-100 and 105-110, where (b) is read on the combined plan lay1c.
- After the combine, a factor is a sum over like monomials. If a group drew parts a and -a from two strengths, it would read dead at 1 while being live at other strengths, and (b) would drop it.
- MEASURED (hazard.py, all five worlds):
  - every J monomial's factor is linear in exactly one strength: 2,416 of 2,416, 360 of 360, 488 of 488 (bang), 488 of 488 (live), 563 of 563;
  - 0 like groups mix strengths, 0 cancel at 1, and 0 live groups read dead at 1.
  - So there is no instance today.
- Fix: name the hypothesis in 7.2 beside kappa's. Or read (b) per strength before the combine: one load per strength at 1 with the others 0, and a combined term is (b) when every strength's part is 0.

**3. Build item 2 names engine/contract.py (pushes) alone.** plans.edging lays Click.weight and Click.train in pushes' term order. The same rows must be dropped there, as item 3 says and as cause.py, mutants.py (cut_j) and my prune.py all do. Otherwise the passing misreads.

**4. The (b) passing work of live one-train terms rides with J's terms in every form** (section 3.4 against section 8). On click that is the spring's 4 terms and the notch's 14 after S1, 162 products. So AB removes 976 per mille (3,455 of 144,884 kept), not the 977 classed. Name it, or give the passing its own plan of edged terms.

**5. mutants.py:93 is dead code,** overwritten by line 94.

## SOUND

**Item by item against my report:**
- B1 is met (section 2).
- MINOR 1 is met (cause (a), item 2).
- MINOR 2 is met (5.2). probe24_math.py is byte-identical to my probe24.py, and so is its output (24 of 24; 72 and 72).
- MINOR 3 is met (7.2, item 1).
- MINOR 4 is met (5.1, with KEY3).
- MINOR 5 is met (7.3).
- MINOR 6 is met (3.4, 7.4).
- MINOR 7 is met (6).
- MINOR 8 is met (5, 9).
- MINOR 9: met, and MIN2's 7.5 overturns my second half; I withdraw "the runner builds the full k per round". run.clicked reads teeth only at partners[train] and at Mesh sides whose q is not 0, and teeth_of reads the partners and the crossed edges. A dead side's q is 0, so each round needs only the live sides, and the full k is needed only for the end digest.
- MINOR 10 is met (7.6).

**The base.** The engine, runner, algebra and main.py are byte-identical between the 48cd7fcf6 and 9d75a4904 extracts (diff). Only the decoder and record/schema.py differ, as MIN2 says.

**Section 2's factorization, checked against the code:**
- notching is square x notch;
- holding is spring x held, and hold x f x entry x tied x held;
- tying is tie x channel x flags;
- meshing is mesh x channel x flags;
- pushing is push x square x path;
- the clocks' and grips' reads carry no strength.
- Measured per monomial (MINOR 2).

**The figures, by arithmetic and against the probe's own counts:**
- State: click 78 + 4 + 30 = 112, then 88, then 85; mesh 36, 36, 33; bang and live 40; well 43.
- Products: 144,884 = 28,992 + 86,976 + 12,168 + 2,730 + 650 + 30 + 12,168 + 1,170.
  - (a) is 18,048 = 1,504 x 12.
  - (c) is 702 = 60 + 36 + 534 + 72.
  - Live is 1,439 = 336 + 972 + 125 + 6.
  - So 977, 949, 962 and 967 per mille.
- Section 3.2's table matches the probe's counts on click and mesh, term for term.
- The combine alone takes click to 86,324 products (cause.py's own "S1 PRODUCTS").

**The reruns:**
- cause.py on click, 100 rounds, and on mesh at file key 7, 60 rounds: identical to the frozen outputs, line for line.
- In both, AB, ABC and ABC+D1 are 0 off in a, b, r, rd, k, clicks and lines in every round. That is 4,050 and 6,824 click entries not 0, and 5,508 and 4,204 lines.
- The end teeth and the digest read back are equal, and each form runs back exactly from its own reduced end.

**Mode 11.** phase.py gives [[19, 60], [6, 19]] at the round's edge and [[19, 6], [60, 19]] between carries. That gives p+ = -27 n - 14 p and 27 n - 14 p, 60 of 60 each, and the mirror swaps n and p, 60 of 60. This matches my whole-number check.

**Section 5.1.** kappa div senses is 1 or 3 on the shipped worlds, and D must be odd by structure or refused, with KEY3.

**The other mutants are sound** (s1, unit, side, flip). The 'laid' design is right in kind: (c) is exact at the file's strengths, so only the unit strengths can tell (b) from (c). MINOR 1 widens it.

## DERIVED / MEASURED / OVERCLAIMED

- **DERIVED, sound:**
  - the one standing;
  - (a) and (b) exact, per monomial;
  - the pair law and its odd-key hypothesis;
  - the 24's move with the train swap;
  - locality;
  - S1's identity;
  - a, b and r by the lay;
  - D3 by the dial's range;
  - the runner reading the live sides alone;
  - the work counts.
- **MEASURED, reproduced by me:** cause.py (click, mesh at key 7); probe24; the 'laid' mutant (round 3).
- **MEASURED by me, new:**
  - hazard.py: no like group mixes strengths, on five worlds;
  - teeth1.py: the click lay hides the Mesh (c) from any run;
  - the click lay is alike across its sites.
- **OVERCLAIMED:**
  - "a factor 0 with every strength at 1 is 0 at every strength", applied to combined factors. It is true on the shipped plans as measured, not in general (MINOR 2).
  - "So test (ii) is required" leaves out that it is not sufficient (MINOR 1).

## Questions for the Boss

1. Do items 3 and 4 take MINOR 1's static test as a condition of building, so that (c) waits in the code as in the ruling?
2. S1 and (b): should (b) be read per strength before the combine, or should the hypothesis be named with hazard.py's measurement?

## Solution24

MIN2 gives Solution24 a lawful, exact build list for now: (a), (b), D3, S1 and the unit-row terms. That is 977 per mille of the click world's work and 279 -> 112 in state. (c) and D1 wait on the ruling and on the owner. With MINOR 1's static test, nothing unruled can slip in.

## Conduct and files

- One lapse: at 08:15 a cause.py run started at load 8.91. I stopped it after 17 s, and its rerun ran gated, starting at 7.78.
- Every other run started between 7.78 and 7.98 (chain.log).
- Nothing was written outside S/min2_math. The frozen folder and every worktree are untouched, and nothing was posted.

Files are in S/min2_math:
- hazard.py and hazard_all.txt
- teeth1.py and teeth1_click20.txt
- click_gears.txt
- cause_click100.txt and cause_mesh7_60.txt
- mutant_laid5.txt
- chain.sh and chain.log
- copy/
