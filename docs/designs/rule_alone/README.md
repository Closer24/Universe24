# The rule alone: the hard question's runs

Can the engine be built from the rule 9.57 (1) alone (ALGEBRA.md 9.98)? The owner's hard
question (the Boss's records 2134 to 2137 of 2026-09-26): Nature24 answers each item from his
own runs of the rule, in integers with the remainders kept and no motion rule of any kind, with
one verdict, WORKS, FAILS (with what fails) or NEEDS (the one missing thing); the algebra's
number beside the run's, the run written before the algebra's number is looked at (record 2137).
Every number is HOST (the runner's own computation) or GAMEBOARD (a reading of the runner's
board). Nothing here is engine code: the runner is checking code (record 2135).

## 1. The runner

1. `rule_alone.py`: one integer rule, transcribed from ALGEBRA.md 9.91 (2) and 9.57 (1):
   w a_next + r' = SUM R a_neighbour + S a_now - w a_before + r, 0 <= r' < w, with p = Gamma -
   c, R = 2 p^2 num, S = 12 den Gamma^2 - 6 (p^2 + Gamma^2)(den - num) - 12 num p^2, w = 6 den
   Gamma^2; the six neighbours, a level 0 beyond an open face. Its one step is equal to the
   engine's `one_rule` on random arrays (a check of the transcription, not of a number).
2. `bodies.py`: a body is its record on a well (the lowered pair [800, 801] on a cube of side
   5, the kind [800, 850] elsewhere: the species that binds in three dimensions, 9.98 (9)
   (a)); its record starts as the well's bound mode by the shipped generator's own operator
   (HOST, a start value); the moving record is the mode times the character of K at the
   group pace v, both levels split about the standing start with the later sample as now
   (9.98 (9) (b)); the content is s on the well's Nodes and the static level around it; the one
   seam in two forms: the well to the Node nearest the envelope's centroid over its support,
   or the well moved one Node when the record's own current has carried one Link.
3. The envelope of the pair (now, before) at a Node: A^2 = (now^2 + before^2 - 2 now before
   cos omega) / sin^2 omega, omega the pair's own rotation at the Node (HOST floats, a reading).

## 2. The verdicts

| Item | Verdict | The run (HOST) | The algebra | Side by side |
| --- | --- | --- | --- | --- |
| 1. A matter record falls in a content gradient in 3D, on the envelope | WORKS | `item1_fall.py`: a free Gaussian packet of width 20 Links at 2^19 on [400, 64, 64] (periodic across, open along x, the packet at the middle), c = 1000 + g (x - 200), 2100 intervals. g = 1: the centroid 200.00 to 227.83; the acceleration in windows of 300: 1.257e-5, 1.299e-5, 1.221e-5, 1.249e-5, 1.327e-5, 1.148e-5 Links per interval^2 (mean 1.25e-5). g = 0: the centroid at 200.000 throughout, the acceleration below 2e-8 | 9.98 (7) with 9.102 (2)'s factor: 2 (1 - 2U)^3 / (1 + (1 - 2U)^2) x (num / den) g / (6 Gamma) = 0.8055 x 1.5686e-5 = 1.264e-5 at U = 0.05 | 1.25e-5 against 1.264e-5; the windows 0.91 to 1.05 of it. They meet |
| 2. Two bodies attract and move, each by the content alone, the well hopping with the centroid | FAILS | `item2_pair.py`: two bodies of s = 2000 on wells of side 5, 20 Links apart on [80, 32, 32]; the content the two static levels moving with the wells. Seam (i), the centroid over the support: no hop in 3000 intervals, the centroids 30.00 +- 0.2 and 50.00 +- 0.2, the separation 20.0 +- 0.3. Seam (ii), the current: no hop for 375 intervals, then the wells run apart (the separation 27 at t = 400, 76 at 450, 96 at 500) | `item2_algebra.py`: Newton's fall by 9.98 (7) on the static content's own gradient (the lone body's level 2000 on its Nodes, 1394 at r = 4, 695 at 10, 354 at 20), from rest: the separation 19.46 at t = 50, 15.13 at 150, 11.05 at 200; the meeting at t = 249 | The algebra meets at 249; the run never (i) or moves the wrong way (ii). What fails: the seam. The well pins the record (the polarization a fifth of a Link, below half); a seam that reads the record's current feeds its own displacement |
| 3. A bound record put in motion keeps its shape and speed; its clock slows | FAILS | `item3_moving.py`: the body on [240, 32, 32] periodic, its record the mode times the character at v = 0.1 (K = 0.1068, HOST). Seam (i): 2 hops then none in 1500 intervals, the centroid 60.00 +- 0.1, the width along x breathing 2.5 to 40; the pair's phase rate at the centre 0.3007 per interval at v = 0.1 and 0.3007 at v = 0. Seam (ii): the well at 3.5 v, the record dispersed to the board in 300 intervals; at v = 0 no hop (the pace read -2e-5). The free control (no well): the packet moves 60.0 to 71.2 in 200 intervals (0.06 to 0.09 per interval) and disperses | the speed v = 0.1; the clock's ratio omega_K - K v over omega_rest = 0.984 (the dispersion, 9.94 (6)); 1 / gamma = 0.985 at c_l^2 = 1 / 3 | the run's speed 0 and ratio 1.000 against 0.1 and 0.984. What fails: the seam; the rule carries the momentum in the record's phase (the free control moves), the declared well stops it |
| 4. The vector part: the dragging; the Lorentz force | not run yet | needs the phase pair and the transport in the runner (9.81 (2), 9.101 item 2) | | |
| 5. A wound record keeps its winding and precesses | not run yet | the winding m theta on both levels (9.98 (9) (c)) | | |
| 6. The recoil as a rotation of the pair at a click, a phase gradient near 1e-8 per Link | not run yet | see section 4 for the arithmetic of the write | | |
| 7. A local source from the record's current and stress | WORKS as a reading | `item7_local_source.py`: on the moving mode at v = 0.05, 0.1, 0.2 the pace the local source implies at each Node, v_i = (num / den) J_a(i) / (3 F_i): the median on the well's 125 Nodes 0.0506, 0.1037, 0.2295 (min to max 0.036 to 0.064, 0.073 to 0.132, 0.157 to 0.284); on the support (about 15000 Nodes) the median 0.0497, 0.1019, 0.2173 with the quartiles a tenth either way; the local source's total over the support 4 s x 0.0504, 0.1028, 0.2189; at rest the current 0 at every Node exactly | 9.98 (4) as redesigned in 9.102 (3): 4 s J_a(i) div F_i at the Node alone, zero at rest; its sum 9.91 (3)'s 4 s v | the total within 1, 3 and 9 percent of 4 s v; the per-Node pace within a third of v. A source with the Node and its six neighbours alone exists |

## 3. What is needed beyond the rule and the click

1. **A body that can move.** A record bound in a declared pair-well is not moved by the rule
   alone through a seam that reads the record: the centroid seam pins it, the current seam is
   unstable. The rule moves a free record (item 1) and carries the momentum in the record's
   phase (the free control of item 3); the declared well stops it. Either the well is the
   record's own (matter's self-binding, P_2 not 0: 9.98 (8)'s big decision for three) or the
   body keeps a store of its motion beside the rule (the accumulator that 9.98 (5) (a) deletes).
   The mathematician has the question.
2. **The bound mode's start.** The generator's bound mode is not stationary under the rule at
   rest in three dimensions: with the well fixed, the record's peak swings between 2e4 and
   1.6e5 and its width along x between 4 and 17 Links over 1500 intervals (GAMEBOARD of the
   runner, `item3_moving_v0.0.json`). The loader's residual bound admits a profile that sloshes.
   This is the mode, not the rule; it does not change the verdicts.

## 4. The runs not read, kept in the folder

1. Item 1's first run: a packet of width 8 on [200, 24, 24] spread to the board in 500
   intervals and its control drifted by the near face's reflection (the runner's open face
   reflects; the engine's absorbs). Fixed by the wider packet at the board's middle.
2. Item 2's first run: the centroid over the whole board, which the mode's tail pulls; the
   displaced wells pumped the record and the wells met at t = 287. Withdrawn: not evidence.
3. Item 3's first run: the gravity time part stepped by the rule on a fully periodic board
   floods it (no face to sink it), the pace falls and the record blows up at t = 1050. Fixed by
   the content as the hold alone.
4. Item 2's gravity time part stepped by the rule with the hold on this runner's reflecting
   faces rang by 15 percent for 1500 intervals (the midpoint content 1193 to 1557) and never
   settled; the static level moving with the wells replaced it.

## 5. The commands

    PYTHONPATH=src python docs/designs/rule_alone/item1_fall.py 1 2100
    PYTHONPATH=src python docs/designs/rule_alone/item1_fall.py 0 2100
    PYTHONPATH=src python docs/designs/rule_alone/item2_pair.py 3000 [current]
    PYTHONPATH=src python docs/designs/rule_alone/item2_algebra.py
    PYTHONPATH=src python docs/designs/rule_alone/item3_moving.py 0.1 1500 [free] [current]
    PYTHONPATH=src python docs/designs/rule_alone/item7_local_source.py

The readings are written beside the scripts as JSON (the runs of 2026-09-26).
