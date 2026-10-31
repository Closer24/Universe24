# The examples

Tensor24's worlds, each a folder of the same three files: the click world (`examples/tensor24-click/`) and the mesh
world (`examples/tensor24-mesh/`) below. The three worlds that wrote no click line by their structure, our bang, the
live world and the well world, left the tree on the owner's word of 2026-10-31, about 09:30 UTC ("out"), and the old
engine's worlds, records and pages left it with that engine on his word of 2026-10-30, 09:3x UTC; git's history keeps
them.

| File | What it holds |
| --- | --- |
| `universe.json` | The universe's integers (`den`, `full_rate`, `width`) and its trains, each with its kinds among the 24's five, its part and its pinion. |
| `piece.json` | The board's shape, the Node-clocks along each axis. |
| `setting.json` | The run's ticks and the gears laid at the start. |

Check and load them: `python -I tools/tensor24_files.py` (the click world by default). Run a world to a record and
its ledger: `python -I tools/tensor24_run.py <universe .json> <piece .json> <setting .json> <record .jsonl>`, each
world's own line below. Read the record: `python -I tools/tensor24_decode.py <record .jsonl> [<ledger .jsonl>]`.

## The strengths, each OPEN

The owner's law: choosing a strength is forbidden, and no strength, dial or factor is picked for an outcome (03:5x UTC).
Every strength below stands in a shipped file as it was laid, each OPEN with how it came, for the owner's batch (AUDIT2
A1, Sofer's form 4 list; the Boss's ruling of 07:5x UTC); until he rules none moves, and none is the act's choice:
- the mesh world's mesh, 250000: searched in a window for an outcome (at 200000 and 240000 the tied hand never moves in
  125 rounds, at 350000 it moves at 128 Node-clocks, so 250000 was taken), a value found by search, Forbidden by the
  law and OPEN;
- the click world's key, 50811429: set from a run (the code-clean auditor's C7), its window an odd whole up to the
  giver's swing over its first beat read at the key 1, about 13 keys in that beat, OPEN;
- the click world's tie, 96000: the rule first tried (it runs away, the run's stop at round 3752 below), OPEN;
- the springs of the click and the mesh worlds, 10^8: the file's den Gamma^2 by a stated rule (the grip at rest, the
  Mesh's own strength), a frame and no search, OPEN as the frame is.

## The click world

`examples/tensor24-click/` is a folder of the same three files, a world whose clicks fall: term 6's coupling
family in its frame (the held train found by its character and Mesh-less, the tied trains found by theirs) and term
11's whole click, on a cube of 3 at den 1 and full_rate 10000 (the rest teeth 6 10^8, f = rest div Gamma = 60000).
Its setting is laid by `tools/derivations/open_items/derive/boss/click_lay/lay.py` from the universe and the piece, in
whole numbers by the act itself (its account in `lay.txt` beside it). Five trains: the A1 train (part 2, the board's wave) and the square train
at 0, push 0 and notch 0; the held hand (A1, A2) laid at rest at (1, 0) at every Node-clock, its before its now, no
angle aimed (the sixth code reader's minor 1, the audit's N3), every edge tooth at the dial's middle, s = 0, the
format's default, and its own spring at 10^8 (OPEN, above) by the rule: the grip at rest, den Gamma^2, the Mesh's own
strength, which the held hand does not hold (its stiffness 2 spring = 2 10^8, a third of W = 6 10^8, inside the held
hand's window 0 < 2 spring < 4 W and on no exact turn, W, 2 W or 3 W; the world's tie, 96000, the rule first tried,
runs away, its counts past 4300 digits by round 1734); and two tied hands (T1, T2), tied to the held hand's square at
hold 1 (the tied spring 2 hold f = 120000; the giver alone beats in 428 rounds on this lay) and to each other by the
hands' tie at 96000: the giver laid as a line hand at its turning point, a = b = (40, 0, 0) on its T1 rows at every
Node-clock, and the taker at 0. Every Node-clock is laid alike, so the Meshes pull nothing between like sites and each
runs as the one Node-clock the generator reads. The key stands in the universe file, 50811429 (OPEN, above), and the lay computes
none (the audit's C7): its window is an odd whole from 1 to the largest swing of the giver's course of S (its passing,
the two-round energy change) over its first beat, read off the act at the key 1, where the click is S itself, on this
lay a swing of 687744000, so that about 13 keys pass in that beat (a chosen unit of wind below the quantum; Planck's
key is NOT_CLOSED 3).

What the act does with this lay, as it falls (`lay.txt`, on one Node-clock, every site of the cube alike; no tick count
and no strength picked to avoid it): the first click falls at round 1, the held train clicking (596 of its clicks
before the run stops); the giver's and the taker's q do not sum to 0 at 2490 rounds, so the books are open; the held
hand's |k|^2, read every 250 rounds, is 1, 1, 1, 1, 1, 1, 0, 9, 9, 1, 4, 1, 1 and 4 to round 3500 and a number of 69 digits at round 3750, and the tied hands'
squares summed at the held hand, hold (|x_giver|^2 + |x_taker|^2), leave the room, Gamma div 4 = 2500, within the first
beat (their most 6829 there); then the counts climb, and after round 3751 a count takes 339 bits against the universe's
width of 128, which the run tool's promise "wide" names at round 3752, the round that reads it, and the run writes no
record, so the decoder has nothing to
read on this lay. Its cause, in Big Pic's words (#2187 6538018966 item 4): a held hand laid at rest beats as a standing
wave, so its square, and the giver's spring 2 hold f |k|^2 with it, swings, a parametric drive. The road is OPEN
(NOT_CLOSED 37): a finer notch first, then the held pair laid above it with the hat's own spring. The lay's no, the
hands' tie at a tenth of the tied spring (12000) at the key 1: no count of the taker moves in 5000 rounds, its push in
its tooth, at most 1128528000 of the dial's half 1200000000, while the held train's 5187 clicks fall, and no count
passes the width. These click readings, and the key's window read at the key 1, are the per-train passing's, measured
before term 11 was laid on the edges; on the edges (`runner/plans.py`'s `edging`, the edge key 3 times the key) every
edge's books are 0 at every place by the carry's law, the counts are the board's as before (the click pushes no gear),
and the lay's click readings wait for the re-lay.

Run it as the one bang: `python -I tools/tensor24_run.py examples/tensor24-click/universe.json
examples/tensor24-click/piece.json examples/tensor24-click/setting.json <record .jsonl>`: on this lay the run names the
count past the width at round 3752, every Node-clock alike, and writes no record (307 s on the run tool). That is the
run's stop, kept and named, not hidden by fewer ticks: the shipped setting's 5000 ticks stand, and the run stops at
round 3752, where its promise "wide" reads a count past the universe's width, the held hand's parametric drive running
away (NOT_CLOSED 37, its road OPEN; KEY3's 6.4); the worlds test and the pages read its first rounds, short of the
stop. The numbers of the lay before this one, the held hand laid at
a quarter turn ((1, 0) now and (0, -1) before, aimed at 90 degrees a round, the audit's N3) at the same spring, were
writer D's run (36fbfbbde and a66674061): 5000 rounds out and back exact, 282663 click lines, the books NOT SHOWN at
123066 of 123795 places, the meetings NOT SHOWN, the held hand's |k|^2 climbing to 5, 100, 404 and 680 by rounds 250,
2500, 4250 and 5000; and the account of `click_lay/measure.py` in `measure.txt` (4212 click lines, the books 0 at 2106
of 2106 places, the held train's lines none and its |k|^2 1) is the lay of the exact quarter turn, before the spring key,
not rerun. The frame's prices (FRAMES.md 6): the held train holds no Mesh, so the vacuum does not propagate; its |k|^2
is laid by the seed and picked by no law (no vacuum minimum); one beat per tied train; the room was the exact quarter
turn, and with none laid the held train clicks and the books open (NOT_CLOSED 29); a Mesh leg's wind is counted by
the Mesh's edges (`runner/plans.py`'s `crossing`), at the mesh 0 of this world by none.

## The mesh world

`examples/tensor24-mesh/` is a second folder of the same three files, a world where the board's wave reaches a tied hand through
the Mesh: the gradient vertex (FRAMES.md 7), laid by `runner/plans.py`'s `meshing` at the mesh (OPEN, above), V = mesh x SUM_i
M_i D_i L between the first part L of the board's wave and a tied hand's T1 rows M_i, as one potential's two pushes (each M_i's row
pushed by -mesh D_i L and the wave's row by +mesh D_i M_i; A1 x T1 has no A1 channel at the value legs, so the board's
wave reaches a vector hand through the Mesh alone, and the held hand, Mesh-less, takes none). Its setting is laid by
`tools/derivations/open_items/derive/boss/mesh_lay/lay.py` from the universe and the piece (its account in `lay.txt`
beside it): a ring of 180 Node-clocks along x, one across y and z, at den 1 and full_rate 10000 (the rest teeth 6 10^8,
the grip 10^8, f = 60000); three trains: the A1 train (part 2, the board's wave), its first part a pulse (95, 281, 439, 500,
439, 281, 95 about x = 20), laid at rest, its before its now, so that the act alone sets how it moves; the held hand
(A1, A2) at rest at (1, 0), its before its now (no angle aimed; the sixth code reader's minor 1, the audit's N3), every
edge tooth at the dial's middle, its own spring at 10^8 (OPEN, above) by the click world's rule, the grip at rest (the world's
tie is 0, outside the window); and a tied hand (T1, T2) at rest
at every Node-clock, tied to the held hand's square at hold 1 (the tied spring 120000); push 0, notch 0, tie 0, mesh
250000 (its ground state needs mesh^2 below grip x 2 hold f / 2 = 6 10^12, and it is 625 10^8), 125 ticks.

The pulse laid at rest splits into two halves that run apart along the ring, each about half its peak (254 of 500 at
round 25, 232 at round 125), about 10 Meshes in 25 rounds: at rounds 25, 50, 75, 100 and 125 at x = 30, 40, 50, 60 and
70 ahead and at x = 10, 0, 170, 160 and 150 behind (read off the run's ledger; a board reading, no claim of physics).
The strengths were picked, as the click world's were, and stand OPEN (above): so that the world stays inside the room, hold
|x_tied|^2 below Gamma div 4 = 2500, for its whole run, and so that the tied hand moves at all: the edge moves a count
only where a momentum reaches half a count a round, and at mesh 200000 and at 240000 the tied hand never moves in the
125 rounds, while at 350000 it moves at 128 Node-clocks inside the room (at most 900; `lay.txt`, the window about the
file's mesh), so mesh is 250000. The tied hand is gripped as the board's wave is, so its waves ride with each half and it
grows by resonance along their paths, linearly in its count (hold |x|^2 4, 81, 196, 361 and 576 at rounds 25 to 125);
it stays at most 576 over the 125 rounds and the same mesh leaves the room at round 226 (`lay.txt`, the window).
Measured on the act at the chosen spring (`lay.txt`, and the run's ledger and `tools/tensor24_decode.py`): the tied
hand moves at 122 Node-clocks, where the halves pass, up to 24 counts; the held hand's |k|^2 swings between 0 and 1, as
its own spring turns it by no quarter turn; the squares of the board's wave summed within 62 permille of the same files
at mesh 0 (the wave's own dispersion on the ring apart: the vertex takes that much into the tied hand); on term 11's
edges (the shared tooth for every pair of clocks, NC29b; `runner/plans.py`'s `edging`) and the Mesh's edges (term 6's
gradient vertex split by the Spoke it reads across, `crossing`), at the edge key 3, the key 1 times kappa / two, 21589
click lines from round 20, 14547 of them with Mesh sides that carried (27308 Mesh sides, the wave and the tied hand
across the Meshes along the ring, a two-clock meeting each), every edge's books 0 at every place by the carry's law, at
the held and tied hands' own Node-clock and across every Mesh; the run back exact. Run it as the one bang: `python -I
tools/tensor24_run.py examples/tensor24-mesh/universe.json examples/tensor24-mesh/piece.json
examples/tensor24-mesh/setting.json <record .jsonl>` (125 rounds out and back in under a minute; the ledger is about 5
MB, three lines a Node-clock a round; 21589 click lines; the run back returns the lay bit for bit).
