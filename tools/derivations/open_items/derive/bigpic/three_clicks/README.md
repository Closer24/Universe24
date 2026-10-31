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
| readings_click_1500.txt | click, 1,500 | booked less swept per edge, its running sum and lag-1 correlation; the record run twice |

Run: `python3 -I edgeclick.py <src> tensor24-click 200 1`; `python3 -I cmp.py <src> tensor24-click 200`; `python3 -I check24.py <src> 40 [world]`; `python3 -I readings.py <src> tensor24-click 1500`.
