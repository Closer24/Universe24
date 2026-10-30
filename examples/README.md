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
below (terms 5 and 9, drafted); the clicks are owed to term 11 (drafted, no vertex laid in these worlds); the window of
the wave, 0 <= SUM grip / W <= 1, is read by the runner.

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
counts a and b a quarter beat later, 4 rounds, the count at which the crest's count has crossed 0 (12000, 10000,
6333, 1611, -3379), its tooth left at 0 (the state's teeth are below one count, and the files lay a tooth from 0 up):
the parts' squares, momenta squared and gradients squared, summed, then stand nearly still in time, (most - least) /
(most + least) of the parts' squares summed at a crest within 71 and 84 permille by windows of 16 rounds (one
standing part alone beats at twice its frequency and twice its wavevector and rings the metric; the pair does not;
the period-4 mode's quarter beat, 1.5 rounds, is no count of rounds). The metric family is pushed by term 5 at the
CHOSEN push 30 and held by term 9's notch at the CHOSEN h 60000 (the board's mean swings about its rest with a beat of
about 31 rounds); its 00, xx, yy and zz slots are laid at the mean (Rule3's carry) of a first run from 0 over its
rounds 65 to 128 by the same generator, so that the well stands rather than swinging between 0 and twice its depth
(the Node-clock has no damping). The third train, `pulse`, is a small pulse along x, alike at every y and z, 500 (16 -
u^2)^2 div 256 at the distance u from its centre (95, 281, 439, 500, 439, 281, 95), its before slot one round back at
about 20 / 49 Meshes a round, (29 now + 20 next) div 49, so that it travels toward +x across the lump's rows and the
void's. Run it as the one bang:
`python -I tools/tensor24_run.py examples/tensor24-well/universe.json examples/tensor24-well/piece.json
examples/tensor24-well/setting.json <record .jsonl>` (128 rounds out and back in about a minute and a half; the
ledger is about 22 MB, three lines a Node-clock a round; the run back returns the lay bit for bit). In the ledger,
train 0's two counts are the lump's parts; train 1's first count is the 00 slot (W = rest + c00: in time's mean over
rounds 65 to 128, 350882 at the mode's crests, x, y and z all multiples of 6 or all 3 more, and 258128 where the mode
is absent, f = 0, the board's mean 275624, so N^2 = rest / W is 944 permille at the crests and 958 in the void, 1000 at
the loader's rest; along x through (y, z) = (0, 0) the mean runs 350923, 324760, 277416, 255979, 277392, 324718 and
again, the mode's period of 6), its fifth to seventh the xx, yy and zz slots (below 0 where the lump is: yy and zz
-10969 at the crests and -2733 in the void in time's mean, xx -18981 and -10763, the pulse's own stress along x
drawing xx down through the run, as the E part has no restoring force on the torus, so the x Meshes' grips g + c_xx +
c_xx' through (0, 0) are 952459 to 965609 of 10^6 at the last round); and train 2's one count is the pulse, slowed by
the well: over the 127 rounds from the first its centroid along x moves 49.20 Meshes against 50.79 for the same files
at push 0 (the metric standing at 0), a lag of 1.59 Meshes, and the bend between the rows through the crests and the
rows of the void is 0.011 Mesh, below the lattice's resolution (the well's period, 6 Meshes, is near the pulse's own
width, and a bend needs a well wider than the wavelength). OPEN here, by name (the edge text's section 4,
derive/boss/edge/EDGE2.md on the Boss's derivation branch): the 00 row's own law. The 00 row's teeth stand at rest, the
acyclic cut, so its own waves run on the rest cone while light and every other slot run on the well's, c^2 = grip / W:
at this lay every other row's dial reads 6237473 to 6334120 where the 00 row's reads 6000000, a second cone 1039 to
1055 permille of the first.
