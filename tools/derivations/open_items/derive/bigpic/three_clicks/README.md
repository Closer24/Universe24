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

| mode | the turn | the board's run back (the same act on the mirrored state) | the label rule (P L = L P) | every edge of the triangle turned |
|---|---|---|---|---|
| 0 | none: the first click | by the carry's own inverse | yes | none |
| 1 | the triangle M | by M's inverse only | no | yes |
| 2 | the 3+3 palindrome (THIRD deriver, carried around three) | yes | no | yes |
| 3 | SPLIT3 at the apex (the SPLIT deriver) | yes | yes | no: the alike pair's edge stays unturned, det(L - I) = 0 |
| 4 | C C^T off its diagonal: the triangle's edges coupled by their boundary signs | yes | yes | yes, traces 18, 6, 6 |
| 5 | road 3 (THIRD deriver), C C^T's diagonal: each triangle edge with its own twin | yes | yes | yes, trace 6 each |

C is each edge's sign on the boundary of every triangle it lies on (the boundary of [i, j, k] is [j, k] - [i, k] + [i, j]). Modes 4 and 5 are the two parts of C C^T, each a palindrome of two blocks (each twin gains K of the edge teeth, then each edge tooth K of the twins; the carries; the blocks again in reverse), so the round's turn is L = [[I + 2 K^2, 2 K], [2 K + 2 K^3, I + 2 K^2]], a pair of trace 2 + 4 kappa^2 per eigenvalue kappa of K. A lone edge lies on no triangle, so K gives it nothing and it carries as the first click, with no condition; C C^T itself has the roots 3, 0, 0, so its palindrome would keep two directions unturned. Every edge tooth is kept by the mirror and every twin flipped about the birth, which an odd dial makes its own complement: the click lay makes every key odd, and so the full-picture world takes key 1.

| record | what it reads |
|---|---|
| kturn_click.txt | the laws on the structure alone, in whole numbers: the mirror R L R L = I, the label rule P L = L P, det(L - I) and det(L + I), and K's spectrum by its characteristic polynomial's whole roots |
| swap_click_200.txt | the label rule draw by draw on the click world, every mode |
| cmp_click_200_34.txt, cmp_click_200_5.txt | R2 for each edge's hidden unit at Node-clock 0 |

The earlier `varied` option set each Node-clock's teeth by turning the birth, which the turn leaves at the birth: it changed nothing and is removed.

## Stage 3 and 4

- **The full-picture worlds:** `worlds/click-k1` (every coupling at its table's entry 1, the key 1) and `worlds/click-k1600` (the key 40^2, an even dial, whose birth is one short of its complement); copy one into `examples/` to run, with `laid` (VARY1's stand-in, labelled so: the taker at the bare unit 1 and each hand's count set apart by the board's own coordinates).
- **Stage 3, the record for the decoder** (`record14.py`): the three clicks in schema 1.4's sides shape, both ends of every edge, k_before the tooth the carry reads and k_after the tooth it leaves, read back on the record alone (partner, quotients summing to 0, teeth summing to the dial less one, q the sum of its sides) with each side's weight by the carry's own law, x = dial q + k_after - k_before. The twins are written nowhere.
- **Stage 4, the pair in whole numbers** (`pairwhole.py`, gate clean): the triangle's own settings (sides 0 and 60 degrees, heights 30 and 90), every weight the triangle's own squares (the height's 3 and the half side's 1 over the side's 4); CHSH from the click counts, no signal, the run back, and the first click with no draw beside it, with the order of the landings.
