# The three clicks, Big Pic's toys (#2187 6538736766, 6538805478)

Whole numbers on the board's own primitives: Rule3's carry with its tooth kept, and shears read about the tooth's birth (D - 1) div 2, the 2 the Spokes along one axis (the loader's birth of the click tooth). A stand-in lay (Python's random) seeds the teeth only. Every division is a carry.

| toy | what it shows | its record |
|---|---|---|
| threeclicks.py | the owner's three clicks in one code path, with no condition: one taker is the first click (no turn, no draw); two or three takers split over triangles, and the triangle's turn is the third click | threeclicks.txt |
| turnteeth.py | the turned tooth at a giver with two takers (the triangle's three edge teeth): run back, mirror, no downward crossing, empty taker, shares, lives, memory | turnteeth_world_dial.txt |
| samepast.py | the law's own reading for one clock: two lays alike in every click before, apart by one hidden unit | samepast.txt |
| turnteeth2.py | the same with two edge teeth only (memory after two clicks in a row) | - |
| nedges.py, order4.py | memory against the number of teeth turned together | nedges.txt |
| pairbell.py | the pair's one hand drawn by the turned tooth, with the push-back to the first outcome: CHSH from the click counts, no signal, run back (its angle cos = 12/13 is a toy's pick, which the board must not make) | pairbell.txt |

Run: `python3 -I threeclicks.py`; `python3 -I turnteeth.py 50811429 600000 1 1250` (dial, rounds, turned 1 or 0, the passing's divisor); `python3 -I samepast.py`; `python3 -I nedges.py 4`; `python3 -I order4.py turnteeth.py`; `python3 -I pairbell.py 400000`.

## Stage 1 and the third click on the real act (node-live 1794d474b)

`edgeclick.py` steps the shipped worlds by step.act unchanged (the click pushes nothing into the gears) and books, at every Node-clock and round, David's split as one flow per edge (david_split.py, copied whole from toys-5 4b15b8b5b), each edge carried with its own tooth at the dial 3 key, born at its middle, the far end clicking the opposite quotient; a train's click is the sum of its edges. Where three trains are pairwise joined, the triangle's three teeth turn between carries (the third click); a lone edge carries as the first click. No line asks how many trains meet.

| record | world, rounds | what it reads |
|---|---|---|
| edge_click_first.txt | click, 200 | the first click: 4,212 click places, the books open at 0; the click teeth run back to the lay |
| edge_click_third.txt | click, 200 | the third click: 4,158 click places, the books open at 0; run back |
| edge_mesh_first.txt, edge_mesh_third.txt | mesh, 125 | one edge, no triangle: the two records byte for byte alike, 4,442 places, books open at 0 |
| cmp_click_200.txt | click, 200 | the law's own reading: one hidden unit in one edge tooth at Node-clock 0 changes 298 click lines from round 18, all at that Node-clock, in the third click, and none in the first |
| check24_click.txt, check24_mesh.txt | click 40, mesh 40 | the 24: every turn that is a symmetry of the board gives the same clicks at the turned Node-clocks, in both clicks |
| readings_click_1000.txt | click, 1,000 | booked less swept per edge, its running sum and lag-1 correlation; the record run twice |

Run: `python3 -I edgeclick.py <src> tensor24-click 200 1`; `python3 -I cmp.py <src> tensor24-click 200`; `python3 -I check24.py <src> 40 [world]`; `python3 -I readings.py <src> tensor24-click 1000`.

## Stage 2: the third click's turn (node-live 1794d474b, step.act unchanged)

`edgeclick.py <src> <world> <rounds> <mode> [laid]`; every turn is whole shears about the birth, read by the carry.

| mode | the turn | the board's run back (the same act on the mirrored state) | the label rule (P L = L P) | every edge of the triangle turned | memory in the toy (toymem.py) |
|---|---|---|---|---|---|
| 0 | none: the first click | by the carry's own inverse | yes | none | never two clicks in a row: a fixed order |
| 1 | the triangle M | by M's inverse only | no | yes | - |
| 2 | the 3+3 palindrome (THIRD deriver, carried around three) | yes | no | yes | - |
| 3 | SPLIT3 at the apex (the SPLIT deriver) | yes | yes | no: the alike pair's edge stays unturned, det(L - I) = 0 | - |
| **4** | **C C^T off its diagonal: the triangle's edges coupled by their boundary signs, no edge to itself** | **yes** | **yes** | **yes, traces 18, 6, 6** | **none over 1,000,000 rounds** |
| 5 | road 3 (THIRD deriver, withdrawn), C C^T's diagonal: each triangle edge with its own twin | yes | yes | yes, trace 6 each | remembers: after two in a row on ab a third 1,798 against 2,764 |

C is each edge's sign on the boundary of every triangle it lies on (the boundary of [i, j, k] is [j, k] - [i, k] + [i, j]). Modes 4 and 5 are the two parts of C C^T, each a palindrome of two blocks (each twin gains K of the edge teeth, then each edge tooth K of the twins; the carries; the blocks again in reverse), so the round's turn is L = [[I + 2 K^2, 2 K], [2 K + 2 K^3, I + 2 K^2]], a pair of trace 2 + 4 kappa^2 per eigenvalue kappa of K. A lone edge lies on no triangle, so K gives it nothing and it carries as the first click, with no condition: the structure chooses between the first click and the third. C C^T itself has the roots 3, 0, 0, so its palindrome would keep two directions unturned. Every edge tooth is kept by the mirror and every twin flipped about the birth, which an odd dial makes its own complement: the click lay makes every key odd.

| 9, 10 | modes 7 and 8 (the flow teeth gain only along the circulation) with each flow-tooth shear's quotient booked on its edge | yes | yes | one turned pair | each clock's books hold, but each clock's clicks remember (the wraps booked edge by edge) |
| **11** | **the triangle's own tooth (circ.py): each edge carries 3 x - C C^T x at the dial 3D, unturned; the triangle's tooth carries y = c . x and lands each quantum as one whole circulation, +1, +1, -1, in one round** | **yes** | **yes** | **the circulation alone** | **the circulation's quanta carry no memory over 1,000,000 rounds; each clock's books hold by construction** |

**Mode 11 is the form this stage ends on** (the owner's word of 05:3x UTC: the third click is never seen alone): each clock's line is made by its own edges' carries of their shares alone, since B c = 0, so the circulation's quantum never shows in any clock's line; it rides on a passing as its path, read in the sides; an idle triangle lands none. The earlier proposal, mode 4, keeps the mirror, the swap and no memory but breaks each clock's books (drift.py).

**Mode 4, the earlier proposal:** it keeps the label rule draw by draw, runs back by the board's own law, turns every edge of the triangle, shows no memory in the Boss's toy over 1,000,000 rounds, and needs no rule to pick it from a family.

| record | what it reads |
|---|---|
| kturn_click.txt | the laws on the structure alone, in whole numbers: the mirror R L R L = I, the label rule P L = L P, det(L - I) and det(L + I), and K's spectrum by its characteristic polynomial's whole roots |
| toymem_200000.txt, toymem_1000000_m4.txt, toymem_1000000_m6.txt | the Boss's toy (one triangle, steady passings 9m, 9m, 12m): after one click the next and after two in a row a third against independent draws, the lives against the geometric law, the swap and the mirror's run back |
| swap_click_200.txt | the label rule draw by draw on the click world, every mode: 0 of 200 rounds differ for modes 0, 3, 4 and 5, 65 for M, 75 for the 3+3 palindrome |
| cmp_click_200_34.txt, cmp_click_200_5.txt | R2 for each edge's hidden unit at Node-clock 0: mode 4 moves 280, 292 and 282 lines, all at that Node-clock |
| check24_click_34.txt, check24_click_5.txt | the 24: 24 of 24 for modes 3, 4 and 5 |
| readings_click_1000_034.txt, readings_click_1000_5.txt | 1,000 rounds: R1, the books, the run back; booked less swept within one dial for the first click (lag-1 -406, -527, -135 per mille), wandering for the third (mode 4: lag-1 -7, 24, -45) |
| cross_click_1000.txt | the board's lives per edge and the edges' gap correlations: the turn adds no correlation between edges (at most 4 per mille) against the flows' shared 508 |
| laws_click_150.txt, laws_mesh_125.txt | `laws.py`: every law in one run, exit status 0 when all hold; on the mesh world, its one edge on no triangle carries in modes 4 and 5 exactly as in the first click |

The earlier `varied` option set each Node-clock's teeth by turning the birth, which the turn leaves at the birth: it changed nothing and is removed (fullpicture_k1600.txt, rerun without it, reads the same digests).

## The full-picture worlds and the key

Every coupling at its table's entry 1; copy a world into `examples/` to run.

- `worlds/click-k1`, key 1: every passing is whole dials (the split's two-leg flows carry KAPPA / 2 = 3, the dial at key 1), so no tooth moves and no turn shows a choice: every gap 0 and R2 0 lines at every edge in every mode (readings_k1_laid_1000.txt, cmp_k1_laid_1000.txt).
- `worlds/click-k1600`, key 40^2: an even dial, whose birth is one short of its complement, so a swap of the alike pair shifts their edge's tooth and the label rule fails in a mixing turn (swap_k1600_laid_200.txt: mode 4 at 1 of 200 rounds).
- `worlds/click-k1601-laid`, key 1601, the whole lay's norm (the held hand's 1 and the giver's 1,600), odd: the label rule, R2 and the readings in the k1601 records. Its setting.json is VARY1's stand-in written by `laywrite.py` into the world's own file (the taker at the bare unit 1 and each hand's count one up per a board coordinate), and its record is byte for byte the run that lays it in memory (`laid`).

## Stage 3 and 4

- **Stage 3, the record for the decoder** (`record14.py`): the three clicks in schema 1.4's sides shape, both ends of every edge, k_before the tooth the carry reads and k_after the tooth it leaves, read back on the record alone (partner, quotients summing to 0, teeth summing to the dial less one, q the sum of its sides) with each side's weight by the carry's own law, x = dial q + k_after - k_before. The twins are written nowhere. Records: record14_click_road3_100.txt, record14_k1_tri_100.txt, every refusal at 0.
- **Stage 4, the pair in whole numbers** (`pairwhole.py`, gate clean): the triangle's own settings (sides 0 and 60 degrees, heights 30 and 90), every weight the triangle's own squares (the height's 3 and the half side's 1 over the side's 4); CHSH from the click counts 2,501 per mille against the hand's own 2,499 and the triangle's 5/2, no signal, the run back, and the first click with no draw beside it (2,499 too: Bell reads the pair's hand), with the order of the landings (lag-1 -1 per mille in the third click, -1,000 in the first).
- **Stage 4b, the pair world's two ends, road (C)** (`twoends.py`, gate clean; PICTURE.md section 11): the free end, each wing's end laid apart and kept where the two copies run back to one birth, reads at most 2 (the sign rule 1,981 to 2,021 per mille over eight births against the exact 2,000, every hand value giving +2; the member's landing read back from its end tooth 818 to 879 against 849, the run back exact at 50,000 of 50,000); (B) forward reads the same; the timelike case 2,490 to 2,517 against 2,499; no signal (at most 9 per mille between a wing's two far-setting shares); the order at lags 1 and 2 within -9 to 10 per mille. Two seeds' laws that pick nothing: the end at the middle reads the sign rule at 388 of 388; one birth with one death keeps one hand value per setting pair and reads 2 with a signal (A's share 917 against 752). Records: twoends_200000.txt, twoends_200000_runs8.txt.
- **Stage 4c, Bell from the end** (`bellend.py`, bellend.txt; the owner's words of 09:33 and 10:10 UTC, David's
  meeting's weight). The probe counts every seed, so every reading is an exact fraction: no draw and no stand-in
  stream.
  - **In (C)'s form** (the HALF pair: NOT PASSED; the Boss's rulings, 6542866096 item 2): the hand and the fixing end
    are fixed in advance, and the far click chooses by its own seeds.
  - **The hand's dependence on the fixing end's setting is a laid measure.** As first stated, the end click wrote the
    board's hand, against the law of the path (the physicist's B1). Read lawfully, the dependence is laid by statement,
    and its start twin writes the same joint law.
  - **Under the owner's laws of 11:47 and 11:52 UTC** (the Boss's 6542967796 and 6543015767): "A click is forbidden to
    write on the board", and "The connection between two places comes, for certain, from the start and from the end."
    - The laid measure's source is the law itself: the start and the end, fixed together in advance. Each click only
      chooses its place's reading.
    - Its form, road (C)'s seeds' law, stays OPEN and mine. It must come from the structure, never from the target: a
      seed rule chosen so that S comes out above 2 is a pick (the 08:4x rule).
    - OPEN beside it: the weight between the start and the end (the owner's 10:10 question), and a mark in the clicks
      that tells a law of both ends from a law of the start alone.
  - The law has three parts, and the pair's one hand runs from the birth to both wings:
  - (i) one wing's click fixes the hand: clicking +1 it leaves the hand along its setting, clicking -1 across it;
  - (ii) the board runs that end back to the birth;
  - (iii) the other wing's click takes the hand's share along its own setting, the square of their overlap, which is one
    of the triangle's own squares.
  - **Read exactly:**
    - the pair's curve E = cos 2 theta at every multiple of 30 degrees;
    - CHSH 5/2 at the triangle's settings, at every weight between the ends read (1:0, 0:1, 1:1, 1:2);
    - 2,828 per mille on the plane's own lattice at the turn of z = 13 + 5 w, which is Tsirelson's 2 r2;
    - each wing's +1 share 500 per mille under every far setting: no signal.
  - **The free-lay control** reads half of each: CHSH 1,250 and 1,414 per mille.
  - **The ruled control, a local act at the bound:** the hand born free over the same lines, and each wing's click fixed
    by the hand alone (+1 where its share along the setting is more than half). It reads CHSH 2,000 per mille exactly,
    at the triangle's settings and at z's, with no share of exactly half.
  - **No signal rests on the fixing end's equal split,** one count each way. On the key's odd dial a signal of
    (5 D - 1) / (4 D^2) remains, so the board form is OPEN.
  - The mathematician PASSED it as a counted law. Tsirelson's 2 r2 is its supremum, and z = 13 + 5 w is a lattice
    point 41 millionths below it, a test's lay.
  - **OPEN:** the law on the board's own act, that is, the end click leaving the hand along its setting, the run back
    to the birth on the pair world, and the far click's share by its own seeds. Also open: the order reading both ways,
    and the pair's reading.

## The uncertainty from the share rule alone (spread.py, spread.txt)

- **The share rule** is bellend.py's part (iii): a click along a setting s takes the hand h's share
  p = (h . s)^2 / ((h . h)(s . s)), the square of their overlap, by its own seed.
- **Per click:**
  - the reading is E = 2 p - 1;
  - its spread is 1 - E^2 = 4 p (1 - p).
- **The relation (DERIVED from the share rule, by algebra on the plane):** for every hand and any two settings whose
  own share is c, the two spreads sum to at least 1 - |2 c - 1|.
  - At 30 or 60 degrees apart the bound is 1/2. Along or across each other it is 0.
  - So no hand gives two sharp readings on settings that are neither along nor across each other.
- **MEASURED** (exactly, whole numbers and Rule3's carry), with the hands the 288 Eisenstein integers m + n w with |m|
  and |n| at most 8, and the settings the six lattice lines and five powers of z = 13 + 5 w (55 pairs):
  - the relation holds in 15,840 of 15,840 hand-pair readings;
  - the bound is met exactly in 7 of the 55 pairs, where its best hand lies on the lattice;
  - every hand sharp on both settings (80 of them) sits on a pair along or across each other.
- **What it rests on:**
  - The share rule alone: no end law, no pair, no draw beyond the click's own seed.
  - The share rule's place on the board is a CANDIDATE, OPEN. Every click lands energy on its edge: the edge's passing
    is the energy flowing through it, (kappa / 2) f times the pair's wedge, which is how the books close. A hand's
    energy along a setting is the square of its overlap.
  - So a click that lands one quantum, split between an outlet along the setting and one across it by their
    passings, takes the share rule. That is not run.
- **With the share rule, Bell also needs the end law's laid measure** (parts i and ii above, in (C)'s form, its source
  OPEN). The free lay and the local act stay at or below 2.

Usage: python3 -I spread.py <src> [RANGE]

## The form of the 11:52 law, a first reading: one cell joins the two ends (onecell.py, onecell.txt)

- **The owner's law of 11:52 UTC:** "The connection between two places comes, for certain, from the start and from the
  end." Its form is first on the order of work (the Boss's 6543120369 item 4).
- **Read under the square form with David's cell rule** (a held hand carries one cell, h times the sum of what it ties):
  - the pair's source ties the two ends, so it carries one cell: the sum over its two states e_k of the plane of
    (a . e_k)(e_k . b), with a and b the two ends' readings (each its setting, along or across);
  - the joint weight is that cell's square, over the source's equal split.
- **The cell holds no hand** (DERIVED, checked exactly): the sum over the source's two states, each over (e_k . e_k), is
  a . b, the plane's own unit form between the two ends. It holds in 13,824 of 13,824 lattice cases. So the connection
  is the start's split and the two ends' readings, and nothing else.
- **It is the end law exactly,** as the algebra says:
  - the joint counts are alike as fractions in 8 of 8 setting pairs, at the triangle's settings and at z's;
  - CHSH is 2,500 and 2,828 per mille;
  - each wing's +1 share is exactly half in 8 of 8.
- **One cell per state is the local act.** Squaring each state's cell apart means the hand is born along e_k or across
  it, and each end takes its own share. It reads at most 1,750 and 1,420 per mille over the six bases.
- **So the 11:52 law's form, as a candidate:** the pair's two clicks weigh as the square of one cell joining the two
  ends through the start.
  - It is David's cell rule again: one cell over what a source ties. Its cross term is the band at the held hand, and
    the correlation here.
  - A cell per part gives no band there, and the local bound here.
  - CANDIDATE.
- **OPEN:**
  - why one cell (shared with the cell rule);
  - the board form: how the board carries the joining cell, with no click writing on it;
  - the weight between the start and the end, idle here, since the form is symmetric in the two ends.

Usage: python3 -I onecell.py <src>
