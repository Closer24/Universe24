# The examples

Tensor24's three files under `examples/tensor24/`, the one world the engine runs. The old engine's worlds, records and
pages left the tree with it on the owner's word of 2026-10-30, 09:3x UTC; git's history keeps them.

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

`examples/tensor24-live/` is a second folder of the same three files, a world that shows something: the light train's
first component laid as a pulse along z, its peak at 2^40 counts (far above one notch), its before slot one round back
by the lattice's own speed (c^2 = grip / W = 1 / 6 per axis at the loader's rest, c about 20 / 49 Meshes a round), so
the pulse travels toward +z and crosses the board of 3 by 3 by 40 in its 100 rounds; the metric family stands at 0, a
standing clock, so the act is exact and the run back returns the start bit for bit. Run it as the one bang:
`python -I tools/tensor24_run.py examples/tensor24-live/universe.json examples/tensor24-live/piece.json
examples/tensor24-live/setting.json <record .jsonl>`; the ledger beside the record holds the light's counts at every
Node-clock and round, the pulse's peak moving along z. The clocks' wells and the grips' slackening are the well world's
below (terms 5 and 9, drafted); the clicks are owed to term 11 (drafted, no vertex laid in these worlds; the click world
below lays one); the window of the wave, the six Spokes' grips summed within [0, senses W] (2 W, the senses of an axis
counted from the star), is read by the runner.

## The well world

`examples/tensor24-well/` is a third folder of the same three files, a world with a held lump. Its setting is laid by
`tools/derivations/open_items/derive/boss/well_lay/lay.py` from the universe and the piece, in whole numbers by the
lattice's own modes and the act itself, Rule3's carry the one division (its account stands in `lay.txt` beside it):
the board 18 by 6 by 6 at small teeth (den 1, full_rate 1000: the grip 10^6, the rest teeth 6 10^6, so that the well
is a visible part of W), three trains. The light's first part is laid at rest (now = before, the tooth 0) at 2000 f on
the board's whole standing mode f = c(x) + c(y) + c(z), c the ring's whole mode 2, 1, -1, -2, -1, 1: the sequence
whose second difference is minus itself, c(x + 1) = c(x) - c(x - 1) from (2, 1), closing on a side that is a multiple
of 6 (a ring's only whole modes are this one, the one whose second difference is minus twice itself, 1, 0, -1, 0, the
constant and the alternating one; this one is chosen as the longest, and summed over the three axes alike so that it
is an eigenvector of the board's pull and stands, with no net drive on the E part). The second part is the act's own
state a quarter beat later, 4 rounds, the count at which the crest's count has crossed 0 (12000, 10000, 6333,
1611, -3379): its counts a and b and its edge tooth (the format lays a tooth within the edge's dial, the run's
promise): the parts' squares, momenta squared and gradients squared, summed, then stand nearly still in time, (most -
least) / (most + least) of the parts' squares summed at a crest within 72 and 74 permille by windows of 16 rounds (one
standing part alone beats at twice its frequency and twice its wavevector and rings the metric; the pair does not;
the period-4 mode's quarter beat, 1.5 rounds, is no count of rounds). The metric family is pushed by term 5 in the
books' form at push 1, the books closed (push 0 is no gravity, and any other value opens the books by that factor):
each slot read by a gear is pushed by minus the act's own energy's derivative by it, taken at fixed momentum, the
momentum being what a clock keeps as its teeth move (dH / dW = -v^2 / 2 there, so the 00 slot is pushed by + k0 v^2 /
2, a deeper and slower clock where the matter moves; at fixed velocity the derivative would read + v^2 / 2 and push
the wrong way). The 00 slot is pushed by k0 = Spokes x senses = 12, the factor the clock reads it at, times the
momenta in and out of every row the push does not land on, and each ii slot by minus its axis's two Meshes'
stretches squared, both halved by the drive's dial 2 on the 00 and ii rows with the remainder kept in the fine
tooth; the 0i and jk slots are read by nothing and pushed by nothing. The push reads the momenta in whole turns of
the rest dial, a count a round at the rest teeth by the centred split, so a row gliding below half a count a round
pushes the 00 slot by nothing: here the light's strides reach 5010 counts a round, the pulse's 97 and the metric's
own 21 (`measure.py` and `measure.txt` beside `lay.py`). The form's price as built: the 00 push leaves out the
square's own 00 and ii rows, whose momentum out the act reads before the push's own kick (a pushed row's stride, which
no plan may read for the mirror to swap every stride it reads), so the metric's own kinetic share of the books, its
self-stress (OPEN in G2), is not paid into the 00 slot: over the run the ii rows' momenta in and out sum to 350206
against the matter's 317317525959, 1 part per million (`lay.txt`). The metric is held by term 9's notch at the
CHOSEN h 120000, twice the 60000 it was at the dial 1, as the notch's monomials on the 00 and ii rows ride the same
dial (the board's mean swings about its rest with a beat of about 31 rounds); its 00, xx, yy and zz slots are laid
at the mean (Rule3's carry) of a first run from 0 over its rounds 65 to 128 by the same generator, so that the well
stands rather than swinging between 0 and twice its depth (the Node-clock has no damping). The third train, `pulse`,
is a small pulse along x, alike at every y and z, 500 (16 - u^2)^2 div 256 at the distance u from its centre (95,
281, 439, 500, 439, 281, 95), its before slot one round back at about 20 / 49 Meshes a round, (29 now + 20 next)
div 49, so that it travels toward +x across the lump's rows and the void's. Run it as the one bang:
`python -I tools/tensor24_run.py examples/tensor24-well/universe.json examples/tensor24-well/piece.json
examples/tensor24-well/setting.json <record .jsonl>` (128 rounds out and back in about two minutes and a quarter;
the ledger is about 20 MB, three lines a Node-clock a round; the run back returns the lay bit for bit). In the
ledger, train 0's two counts are the lump's parts; train 1's first count is the 00 slot (W = rest + 12 c00: in
time's mean over rounds 65 to 128, 143 at the mode's crests, x, y and z all multiples of 6 or all 3 more, and 85
where the mode is absent, f = 0, the board's mean 95, so N^2 = rest / W is 999714 parts per million at the crests
and 999830 in the void, 10^6 at the loader's rest: the clock deepens where the matter moves; along x through (y, z)
= (0, 0) the mean runs 143, 126, 99, 88, 99, 126 and again, the mode's period of 6; from 0 the 00 slot rises first
at the crests, 22 there against 0 in the void after one round and 141 against 29 after five, before its own waves
spread it, `derive/boss/term5_books/probe.txt`), its fifth to seventh the xx, yy and zz slots (below 0 over the
whole board and a shade deeper in the void than at the crests, as the ii push reads the lump's stretches, which
stand between its crests, and not its momenta: yy and zz -18 at the crests and -20 in the void in time's mean, xx -31
and -32, the pulse's own stretches along x drawing xx down, as the E part has no restoring force on the torus, so the
x Meshes' grips g + c_xx + c_xx' through (0, 0) are 999923 to 999946 of 10^6 at the last round); and train 2's one
count is the pulse, slowed by the well by less than a tenth of a Mesh: over the 127 rounds from the first its
centroid along x (weighted by its counts squared) moves 50.79 Meshes against 50.88 for the same files at push 0 (the
metric standing at 0), a lag of 0.09 Mesh, and the bend between the rows through the crests and the rows of the void
is 0.01 Mesh, below the lattice's resolution (the well is 3 parts in 10^4 of W at its deepest). OPEN here, by name
(the edge text's section 4, derive/boss/edge/EDGE2.md on the Boss's derivation branch): the 00 row's own law. The 00
row's teeth stand at rest, the acyclic cut, so its own waves run on the rest cone while light and every other slot
run on the well's, c^2 = grip / W: at the last round every other row's dial reads 6000852 to 6001812 where the 00
row's reads 6000000, a second cone 1000142 to 1000302 parts per million of the first.

## The click world

`examples/tensor24-click/` is a fourth folder of the same three files, a world whose clicks fall: term 6's coupling
family in its frame (the held train found by its character and Mesh-less, the tied trains found by theirs) and term
11's whole click, on a cube of 3 at den 1 and full_rate 10000 (the rest teeth 6 10^8, f = rest div Gamma = 60000).
Its setting and its key are laid by `tools/derivations/open_items/derive/boss/click_lay/lay.py` from the universe and
the piece, in whole numbers by the act itself (its account in `lay.txt` beside it). Five trains: light (A1, part 2)
and the metric at 0, push 0 and notch 0 (the held turn is exact only for -rest / 4 <= c00 < rest / 2); the held hand
(A1, A2) at (1, 0) at every Node-clock, its before (0, -1) a quarter turn back, every edge tooth at the dial's middle,
s = 0, the format's default (the room exists only for a held tooth born there), so that its quarter turn is exact at
every Node-clock; and two tied hands (T1, T2), tied to the held hand's square at hold 1 (the tied spring 2 hold f =
120000, a lone tied hand's beat 410 rounds on the act) and to each other by the hands' tie at 96000: the giver laid as
a line hand at its turning point, a = b = (40, 0, 0) on its T1 rows at every Node-clock, and the taker at 0. Every
Node-clock is laid alike, so the Meshes pull nothing between like sites and each runs as the one Node-clock the
generator reads.

The room, with its numbers: the passing's books hold only while the held hand's quarter turn is exact (the tie is a
monomial of four value legs, NOT_CLOSED 29), which holds while the tied hands' squares summed at the held hand, hold
(|x_giver|^2 + |x_taker|^2), stay below Gamma div 4 = 2500. The lay starts at hold A^2 = 1600, and the act keeps the
sum at most 1600 over all 5000 rounds with the energy moving between the giver and the taker (the pair beats on its two
normal modes, so each beat's most falls from 1600 to about 1000 over the run and does not stand constant). The tie is
800 permille of the tied spring, not a tenth of it, because the edge moves a count only where a gear's momentum reaches
half a count a round, and a tied hand inside the room moves at most about 0.7 of a count a round: at a tenth (12000)
the taker's push stays in its tooth, at most 158400000 of the dial's half 1200000000, no count moves and no click falls
in 5000 rounds (`lay.txt`, its no). The key is CHOSEN as the nearest odd whole to the seventh of the largest swing of
the giver's course of S (its passing, the two-round energy change) over its first beat, read off the act at the key
1, where the click is S itself: a swing of 355680000, so the key 50811429 and about seven keys a beat (a chosen unit of
wind below the quantum; Planck's key is NOT_CLOSED 3).

Run it as the one bang: `python -I tools/tensor24_run.py examples/tensor24-click/universe.json
examples/tensor24-click/piece.json examples/tensor24-click/setting.json <record .jsonl>` (5000 rounds out and back in
about 17 minutes; the ledger is about 54 MB, five lines a Node-clock a round). Measured from outside on its record and
ledger by `click_lay/measure.py` (`measure.txt`): 4212 click lines, the giver's and the taker's alone; the pair's books,
the q of the lines summed over the trains, 0 at every one of the 2106 rounds and Node-clocks where a line stands; the
held train's lines none, and its |k|^2 1 at every Node-clock and round; the room at most 1600 at every Node-clock; the
largest count 40, no runaway; the taker's course in keys swinging between 1 and 7 from round 91 on, its lines alike at
every Node-clock, the giver's and the taker's q summing to -4 and 4 at each over the run; the run back exact; the 24,
the lay turned under the twisted action (a negated row's counts negated and its tooth flipped to -1 - s) with its sites
moved, run on the cube against the run turned, alike in the state and in every click at 24 of 24 turns over its first
100 rounds. The frame's prices (FRAMES.md 6): the held train holds no Mesh, so the vacuum does not propagate; its |k|^2
is laid by the seed and picked by no law (no vacuum minimum); one beat per tied train; the room is half a quantum, and
past it the held train clicks alone and the books open (NOT_CLOSED 29); a Mesh leg's wind is booked by no click
(NOT_CLOSED 4).
