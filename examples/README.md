# The examples

Tensor24's three files under `examples/tensor24/`, the first of the five worlds the engine runs; the live, the well,
the click and the mesh worlds below are four more folders of the same three files. The old engine's worlds, records
and pages left the tree with it on the owner's word of 2026-10-30, 09:3x UTC; git's history keeps them.

| File | What it holds |
| --- | --- |
| `universe.json` | The universe's integers (`den`, `full_rate`, `width`) and its trains, each with its kinds among the 24's five, its part and its pinion. |
| `piece.json` | The board's shape, the Node-clocks along each axis. |
| `setting.json` | The run's ticks and the gears laid at the start. |

Check and load them: `python -I tools/tensor24_files.py` (the examples by default). Run them to a record and its
ledger: `python -I tools/tensor24_run.py examples/tensor24/universe.json examples/tensor24/piece.json
examples/tensor24/setting.json <record .jsonl>`. Read the record: `python -I tools/tensor24_decode.py <record .jsonl>
[<ledger .jsonl>]`.

## The live world

`examples/tensor24-live/` is a second folder of the same three files, a world that shows something: the A1 train's
first component laid as a pulse along z by `tools/derivations/open_items/derive/boss/live_lay/lay.py` from the universe
and the piece (its account in `lay.txt` beside it), 2^28 (64 - d^2)^2 at the distance d below 8 from z = 10, its peak
at 2^40 counts (far above one notch), laid at rest, its before its now, so that the act alone sets how it moves: it
splits into two halves of about half its peak (498 permille each at round 20) that run apart along z on the board of 3
by 3 by 40, about 8 Meshes in 20 rounds, meet at its far side, z = 30, near round 50, and meet again at z = 10 at round
100, where the pair makes 967 permille of the laid peak (a board reading off the run's ledger, no claim of physics);
the square train stands at 0, a standing clock, so the act is exact and the run back returns the start bit for bit.
Run it as the one bang: `python -I tools/tensor24_run.py examples/tensor24-live/universe.json
examples/tensor24-live/piece.json examples/tensor24-live/setting.json <record .jsonl>`; the ledger beside the record
holds the counts of the board's wave at every Node-clock and round, the pulse's two halves running along z. The clocks' wells and the grips' slackening are the well world's
below (terms 5 and 9, drafted); the clicks are owed to term 11 (drafted, no vertex laid in these worlds; the click world
below lays one); the window of the wave, the six Spokes' grips summed within [0, senses W] (2 W, the senses of an axis
counted from the star), is read by the runner.

## The well world

`examples/tensor24-well/` is a third folder of the same three files, a world with a lump that spreads. Its setting is
laid by `tools/derivations/open_items/derive/boss/well_lay/lay.py` from the universe and the piece, in whole numbers by
a polynomial lump and the act itself, with no mode of the ring, no circular function and no construction that finds
one, no root, no search and no table, Rule3's carry the one division (its account stands in `lay.txt` beside it): the
board 18 by 6 by 6 at small teeth (den 1, full_rate 1000: the grip 10^6, the rest teeth 6 10^6, so that the well is a
visible part of W), three trains. The first part of the board's wave is laid at rest (now = before, the tooth 0) as one lump about
(0, 0, 0), the pulse's polynomial bump turned round its centre: 12000 (9 - r^2)^2 div 81 where r^2, the squared
distance from the centre summed over the three axes around their rings, is below 9 (12000, 9481, 7259, 5333, 3703,
2370, 1333 and 148 at r^2 = 0 to 6 and 8, at 93 Node-clocks); its second part is laid at 0. The lump is no mode of the
board's pull, so the act moves it as it will, and it spreads; read on the board (`lay.txt`, line 4): within 16 rounds
its centre's count falls from 12000 to 431 and 955 permille of its squares leave its laid support; its waves cross the
ring and partly come back, 286 permille of them within the support at round 80 (the centre at -5756) and 177 at round
128; its squares stand alike on its two sides along x at every window, so it spreads and does not move as a whole.
The square train is pushed by term 5 in the books' form at push 1, the books closed (push 0 is no gravity; any other
value would open the books by that factor, and the files' format refuses it by name): each slot read by a gear is
pushed by minus the act's own energy's derivative by it, taken at fixed momentum, the momentum being what a clock keeps
as its teeth move (dH / dW = -v^2 / 2 there, so the 00 slot is pushed by + k0 v^2 / 2, a deeper and slower clock where
the sourcing trains' rows move; at fixed velocity the derivative would read + v^2 / 2 and push the wrong way). The 00 slot is pushed
by k0 = Spokes x senses = 12, the factor the clock reads it at, times the momenta in and out of every row the push
does not land on, and each ii slot by minus its axis's two Meshes' stretches squared, both halved by the drive's dial 2
on the 00 and ii rows with the remainder kept in the fine tooth; the 0i and jk slots are read by nothing and pushed by
nothing. The push reads the momenta in whole turns of the rest dial, a count a round at the rest teeth by the centred
split, so a row gliding below half a count a round pushes the 00 slot by nothing: here the strides of the board's wave reach 5580
counts a round, the pulse's 96 and the square train's own 50 (`measure.py` and `measure.txt` beside `lay.py`). The form's
price as built: the 00 push leaves out the square's own 00 and ii rows, whose momentum out the act reads before the
push's own kick (a pushed row's stride, which no plan may read for the mirror to swap every stride it reads), so the
square train's own kinetic share of the books, its self-stress (OPEN in G2), is not paid into the 00 slot: over the run the
ii rows' momenta in and out sum to 446149 against the sourcing rows' 19388914470, 23 parts per million (`lay.txt`). The
square train is held by term 9's notch at the CHOSEN h 120000, twice the 60000 it was at the dial 1, as the notch's
monomials on the 00 and ii rows ride the same dial (the board's mean swings about its rest with a beat of about 31
rounds); its 00, xx, yy and zz slots, read from the piece's shape, are laid at the mean (Rule3's carry) of a first run
from 0 over its rounds 65 to 128 by the same generator, so that the square train starts near the mean the lump gives it and
not at 0 (the Node-clock has no damping). The third train, `pulse`, is a small pulse along x about x = 9, the ring's
far side from the lump, alike at every y and z, 500 (16 - u^2)^2 div 256 at the distance u from its centre (95, 281,
439, 500, 439, 281, 95), laid at rest, its before its now, so that the act alone sets how it moves: it splits into two
halves that run apart along x, about 7 Meshes in 16 rounds, meet in the lump at x = 0 and again at x = 9 (`lay.txt`,
line 5; a board reading, no claim of physics). Run it as the one bang: `python -I tools/tensor24_run.py
examples/tensor24-well/universe.json examples/tensor24-well/piece.json examples/tensor24-well/setting.json <record
.jsonl>` (128 rounds out and back in about two minutes and a half; the ledger is about 20 MB, three lines a Node-clock
a round; the run back returns the lay bit for bit). In the ledger, train 0's two counts are the lump's parts, train
1's first count the 00 slot (W = rest + 12 c00) and its fifth to seventh the xx, yy and zz slots, and train 2's one
count the pulse.

Its readings are a spreading lump's, read on the board (`measure.txt`), and none of them is a standing well's: term
5's sign, read from 0 with the square train's gears taken out, the 00 slot's mean over the lump's laid support against the
void's, 1 and 0 at round 2, 11 and 0 at round 4, 25 and 3 at round 8 and 17 and 11 at round 16: the clock deepens
first where the lump's rows move, before its waves spread it; the depth, in time's mean over rounds 65 to 128 of
the laid world, the 00 slot 7 at the lump's centre, 4 over its laid support and 5 over the void, 4 to 12 over the
board (along x through (y, z) = (0, 0): 7, 6, 5, 5, 6, 7, 8, 8, 7, 6, 7, 8, 8, 7, 6, 5, 5, 6), so N^2 = rest / W is
999986 parts per million at the centre and 999990 over the void, a well that is real but spread nearly flat over the
board by the lump's own waves, and the ii slots -3 to -2; and the pulse through it, its squares' mean distance from its
laid centre at push 1 and at push 0 (the square train standing at 0) apart by at most 6 hundredths of a Mesh over the run,
either way, below the lattice's resolution. OPEN here, by name: the 00 row's own law (the edge text's section 4,
derive/boss/edge/EDGE2.md on the Boss's derivation branch): the 00 row's teeth stand at rest, the acyclic cut, so its
own waves run on the rest cone while the board's wave and every other slot run on the well's, c^2 = grip / W: at the last round
every other row's dial reads 5999736 to 6000396 where the 00 row's reads 6000000, a second cone 999956 to 1000066
parts per million of the first. OPEN on this world: term 13's frozen clock (`derive/boss/frozen_edge`, the night's
PLAN A3), which reads a test clock's beat against a standing well; the lump spreads, so no well stands here to read it
against (its `probe.txt` reads the standing mode this world was laid on before), and frame 11's standing well waits on
a lawful steady source.

## The click world

`examples/tensor24-click/` is a fourth folder of the same three files, a world whose clicks fall: term 6's coupling
family in its frame (the held train found by its character and Mesh-less, the tied trains found by theirs) and term
11's whole click, on a cube of 3 at den 1 and full_rate 10000 (the rest teeth 6 10^8, f = rest div Gamma = 60000).
Its setting is laid by `tools/derivations/open_items/derive/boss/click_lay/lay.py` from the universe and the piece, in
whole numbers by the act itself (its account in `lay.txt` beside it). Five trains: the A1 train (part 2, the board's wave) and the square train
at 0, push 0 and notch 0; the held hand (A1, A2) laid at rest at (1, 0) at every Node-clock, its before its now, no
angle aimed (the sixth code reader's minor 1, the audit's N3), every edge tooth at the dial's middle, s = 0, the
format's default, and its own spring CHOSEN at 10^8 by the rule: the grip at rest, den Gamma^2, the Mesh's own
strength, which the held hand does not hold (its stiffness 2 spring = 2 10^8, a third of W = 6 10^8, inside the held
hand's window 0 < 2 spring < 4 W and on no exact turn, W, 2 W or 3 W; the world's tie, 96000, the rule first tried,
runs away, its counts past 4300 digits by round 1734); and two tied hands (T1, T2), tied to the held hand's square at
hold 1 (the tied spring 2 hold f = 120000; the giver alone beats in 428 rounds on this lay) and to each other by the
hands' tie at 96000: the giver laid as a line hand at its turning point, a = b = (40, 0, 0) on its T1 rows at every
Node-clock, and the taker at 0. Every Node-clock is laid alike, so the Meshes pull nothing between like sites and each
runs as the one Node-clock the generator reads. The key is CHOSEN in the universe file, 50811429, and the lay computes
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

`examples/tensor24-mesh/` is a fifth folder of the same three files, a world where the board's wave reaches a tied hand through
the Mesh: the gradient vertex (FRAMES.md 7), laid by `runner/plans.py`'s `meshing` at the CHOSEN mesh, V = mesh x SUM_i
M_i D_i L between the first part L of the board's wave and a tied hand's T1 rows M_i, as one potential's two pushes (each M_i's row
pushed by -mesh D_i L and the wave's row by +mesh D_i M_i; A1 x T1 has no A1 channel at the value legs, so the board's
wave reaches a vector hand through the Mesh alone, and the held hand, Mesh-less, takes none). Its setting is laid by
`tools/derivations/open_items/derive/boss/mesh_lay/lay.py` from the universe and the piece (its account in `lay.txt`
beside it): a ring of 180 Node-clocks along x, one across y and z, at den 1 and full_rate 10000 (the rest teeth 6 10^8,
the grip 10^8, f = 60000); three trains: the A1 train (part 2, the board's wave), its first part the well world's pulse (95, 281, 439, 500,
439, 281, 95 about x = 20), laid at rest, its before its now, so that the act alone sets how it moves; the held hand
(A1, A2) at rest at (1, 0), its before its now (no angle aimed; the sixth code reader's minor 1, the audit's N3), every
edge tooth at the dial's middle, its own spring CHOSEN at 10^8 by the click world's rule, the grip at rest (the world's
tie is 0, outside the window); and a tied hand (T1, T2) at rest
at every Node-clock, tied to the held hand's square at hold 1 (the tied spring 120000); push 0, notch 0, tie 0, mesh
250000 (its ground state needs mesh^2 below grip x 2 hold f / 2 = 6 10^12, and it is 625 10^8), 125 ticks.

The pulse laid at rest splits into two halves that run apart along the ring, each about half its peak (254 of 500 at
round 25, 232 at round 125), about 10 Meshes in 25 rounds: at rounds 25, 50, 75, 100 and 125 at x = 30, 40, 50, 60 and
70 ahead and at x = 10, 0, 170, 160 and 150 behind (read off the run's ledger; a board reading, no claim of physics).
The strengths are chosen by the act, as the click world's are, so that the world stays inside the room, hold
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
