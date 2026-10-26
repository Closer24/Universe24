# Report: a horizon on the returning board (H-Horizon-On-The-Returning-Board-2, sb2, 2026-10-26, the engine head 89b47631e)

**The verdict line: WORKS, with no sentence changing an act. One seed of the law both returns exactly and freezes a Node** - the fourth lay form, the uniform sea of a plane with a gap at a count at every Node, the count carrying its rise past the frozen content (4 Gamma^3 to one content; the count 7,550 at the top, crossed in the rise by 50,000 at Gamma 1,000). Measured on w9 (the side 4, the count 50,000, 1,200 intervals): 64 of 64 Nodes frozen AT ONCE at the interval 43 at the content 3,837 with 192 Links held at the wall, released at 44 by FR-S1's turn (64 Nodes turned at once, the content 3,792), the board back to Gamma at every Node at 87 and again at 1,162, three bangs (1, 88, 1163). The engine's own readers on that one record: gate 34 (the horizon and the stopped clock) SHOWN, gate 1 (the board returns to Gamma) SHOWN with two exact returns, gate 46 (the recurring bang) SHOWN with two tops turning at once and three bangs, gate 61 (the horizon radiates) NOT SHOWN (every Node is the horizon, so no credit can stand two Links from every frozen Node), gate 14 NOT REACHED **by a defect of its own predicate** (it reads the content's max from the reader's rows, one at every twelfth interval, and misses the single frozen interval the Node lines hold: board.py:262-284, the bug below). The laws checked: the kit's conservation check 12 of 12 in full on w9 (the re-run's log 237,121 of 237,121 events, the current's antisymmetry 1,200 of 1,200, the Links' momentum 0 on three axes 1,200 of 1,200, floats 0); the run back 20 of 20 on each of six records; 117 bits at the mark; 90 arrays per Node; no file of src or tests touched. The one law unmet on the candidate: the 48 on the clicks, which has no reading on it (0 births, 0 clicks: the checker has nothing to carry), and gate 61's predicate, which the board frozen at every Node cannot meet as written.

The derivation, the algebra page, the per-world predictions and the ledger row: DERIVATION.md and PREDICTIONS.md beside this file. The worlds under worlds/; the outputs under out/.

## The commands (every run nice -n 19, one at a time, the load 0.01 to 0.63 at the starts; P the venv's python, W this worktree, F this folder)

- `PYTHONPATH=$W/src $P $F/algebra.py` (the frozen mark from the law's own tables)
- `PYTHONPATH=$W/src $P -m event_universe.run $F/worlds/<world>.json /dev/shm/tmp/sb2/<id>.json back 20` for w0, w1, w4 (refused), w6, w7, w8, w9
- `$P $F/read_record.py /dev/shm/tmp/sb2/<id>.json` (the Node lines: the alike intervals, the freeze, the release, the return)
- `PYTHONPATH=$W/src $P $F/gates_read.py /dev/shm/tmp/sb2/w9.json` (the engine's own readers: board.horizon, board.stopped_clock, clicks.horizon_radiates, board.returns, board.recurring_bang; out/w9_gates.txt)
- `PYTHONPATH=$W/src $P <kit>/conservation_check.py /dev/shm/tmp/sb2/w9.json out /dev/shm/tmp/sb2/w9_cons.json` (out/w9_cons.txt: 12 of 12)

## The numbers, world by world

| world | lay, count | alike / intervals | content max (interval) | volume max | frozen | release | returns | births / clicks | bits (state / transient) | run back |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| w0 | cycle, 5 | 220 of 240 | 775 (109 to 120) | 22,253 | none | - | the volume 999 at 220 | 144 / 348 | 115 / 99 | 20 of 20 |
| w1 | cycle, 500 | 15 of 400 | 1,906 (300) | above 1,483,625 | none | - | none | 26 / 3,336 | 115 / 106 | 20 of 20 |
| w4 | cycle, side 5 | refused by the lay (wave.py:49: the cycle pattern is 4 by 4) | | | | | | | | |
| w6 | sea, 5 | 400 of 400 | 863 (382) | 31,577 | none | - | 253 and 256 | 0 / 0 | 115 / 100 | 20 of 20 |
| w7 | sea, 5,000 | 800 of 800 | 3,521 (800) | 1,265,091,507 | none | - | none in 800 | 0 / 0 | 115 / 115 | 20 of 20 |
| w8 | sea, 5,000 | 3,600 of 3,600 | 3,628 (1,788) | 2,114,115,686 | none (165 short of 3,793) | - | 3,575, the bang at 3,576 | 0 / 0 | 115 / 116 | 20 of 20 |
| w9 | sea, 50,000 | 1,200 of 1,200 | 3,837 (43) | 4,427,299,591 | 64 of 64 at the interval 43, 192 Links at the wall | 44, 64 turned at once | 87 and 1,162 at Gamma, three bangs | 0 / 0 | 117 / 117 | 20 of 20 |

## The algebra in one paragraph

The frozen content is c_f = (Gamma div 2) ln(2 Gamma) to the integer, 3,793 at Gamma 1,000 (the clock 22); the level's clause makes the content (Gamma div 4) ln(X div Gamma), so the mark in volumes is 4 Gamma^3 to one content (measured 4,268,834,097, and the level of 4,000,000,000 is 3,792). The cycle lay leaves the carrier alike at every Node, so BG-S1's spread e is 0, the Links' lift vanishes and the pull alone ends the rise: the one-Node line is the same at every side, **the cube's side is no lever at all** (and the cycle lay is refused off the multiples of 4 in any case), the one lever being the lay's count, whose top content was measured to rise by 401 per e-fold (858 at the count 5, 3,628 at 5,000). FR-S1 releases a frozen Node at its own frozen interval by the swap's trigger, so the release is one interval and is in time for any period; and since the frozen content kills every arrival (next = 2 now - before, no Link term), it is the swap's own ceiling: a board alike at every Node cannot pass it, freezes at every Node at once, turns at every Node at once, and by CS6-S1 retraces its rise with no click in it. What bars the cycle lay from the pair is not its symmetry but its births at a subset of the Nodes at a raised count (w1: 20 births of 64 at the interval 6, the board parted by 16), after which BG-S1's lift leaves no top.

## The sentences

**HR-S1 (the unification, the one threshold where two stand):** the frozen content is the swap's own ceiling and not a second threshold: where the Link pace rounds to 0 every arrival vanishes and the Node's line is a free linear rise, which the turn at the weak maximum ends; so the horizon is a reading of the content alone, and OS-S1's clause 3 ("the horizon needs a Node unlike its neighbours") is too strong by the breadth of one gate: gates 14 and 34 name no neighbour, gate 61 alone does.

**HR-S2 (the item):** one seed of the law both returns exactly and freezes a Node - the uniform sea of a plane with a gap at a count at every Node whose rise passes 4 Gamma^3 (the count above 2 Gamma div C, 7,550 at Gamma 1,000 on ga2's gapped row): the board being alike at every Node it freezes at every Node at once, FR-S1's turn releases it at the next interval and CS6-S1's retrace carries it back to Gamma, so the horizon (gate 34) and the recurring bang (gates 1 and 46) stand on ONE record at the intervals 43 and 87 and 1,162.

## Bugs, by file and line

1. **src/event_universe/board.py:262-284 (gate 14, the horizon).** The predicate takes the content's max from `record.rows` (the reader's rows, one at every twelfth interval and two early marks) while the freeze itself is read from the Node lines (`record.first_frozen()`): on w9 it printed "max content in the rows 3,748" against the frozen content 3,793 and the verdict NOT REACHED while 64 Nodes stood frozen at the interval 43 and gate 34 read SHOWN on the same record. A horizon shorter than a twelfth of the run is invisible to gate 14. The fix within the reader: take the max over the Node lines' `content` (the same lines gate 34 walks), or read the frozen lines first and the rows second.
2. **src/event_universe/clicks.py:359-388 (gate 61, the horizon radiates).** The predicate asks a credit two or more Links from EVERY frozen Node, which no board frozen at every Node can hold, so the one seed that returns with a horizon can never show the radiation: the row owes a reading for the board whose every Node is the horizon (a candidate for the Reader, named not proposed).
3. **src/event_universe/run.py:87 (the reader's row "links at the wall").** It counts every Link factor 0, the tension at or past Gamma among them, so it read 64 at the interval 33 of w1 with no frozen Node on the board; the horizon's own count of held Links is the Node lines' `held` (192 at w9's interval 43). The row's name reads as BH-S1's wall and is not it.
4. The kit's README rule 2 (`$P -m event_universe.decoder <out.json>`) does not run on this head: decoder.py has no main and prints nothing with exit 0. The readers are board.py, clicks.py and predicates.py through decoder.Record (gates_read.py here).

## What was cut short, by name

w2 (the cycle lay at the count 50,000), w3 (the cycle lay on the side 8) and w5 (the cycle lay beside the hole) are written under worlds/ and were not run; the chiral seed's period search to 8,000 was not run; the kit's reach.py on w9 was not run; the 48 on the clicks has no reading on w9 (no click). No chain is still running (the one background run, w8, finished; nothing is left on the box).
