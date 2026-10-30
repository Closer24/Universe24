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

`examples/tensor24-well/` is a third folder of the same three files, a world with a held lump: a board of 16 by 8 by 8
at small teeth (den 1, full_rate 1000: the grip 10^6, the rest teeth 6 10^6, so that the well is a visible part of W)
and three trains. The light train's two parts are laid in quadrature on one isotropic standing mode, f = cos(pi x / 4)
cos(pi y / 4) cos(pi z / 4) at the amplitude 10^4: the first part at its turning point (a = A f, b = A f cos w) and the
second a quarter beat behind (a = 0, b = -A f sin w), w the mode's beat on the lattice at rest (cos w = 1 - 3 (1 -
cos(pi / 4)) / 6), so that the parts' squares, their momenta squared and their gradients squared, summed, stand still in
time: a steady source (one standing wave's stress beats at twice its frequency and twice its wavevector, on the
lattice's own light cone, and rings the metric; the pair in quadrature does not). The metric family is pushed by term 5
at the CHOSEN push 30 and held by term 9's notch at the CHOSEN h 60000 (the board's mean swings about its rest with a
beat of about 2 pi / sqrt(4 h / W) = 31 rounds); its 00, xx, yy and zz slots are laid at the time's mean of a first
run from 0 over its last 64 rounds, so that the well stands rather than swinging between 0 and twice its depth (the
Node-clock has no damping). The third train, `pulse`, is a small pulse (peak 500, half-width 4) travelling toward +x,
alike at every y and z, that crosses the lump's rows and the void's. Run it as the one bang:
`python -I tools/tensor24_run.py examples/tensor24-well/universe.json examples/tensor24-well/piece.json
examples/tensor24-well/setting.json <record .jsonl>` (128 rounds out and back in about two minutes; the ledger is about
34 MB, three lines a Node-clock a round; the run back returns the lay bit for bit). In the ledger, train 0's two counts
are the lump's parts (their squares summed at a crest stay within 99763732 and 108639725 over the 128 rounds); train 1's
first count is the 00 slot (W = rest + c00: in time's mean over the last 64 rounds 333701 at the lump's crests, x, y and
z all multiples of 4, and 239474 in the void, one of them 2 more than a multiple of 4, so N^2 = rest / W is 947 permille
at the crests and 961 in the void, 1000 at the loader's rest), its fifth to seventh the xx, yy and zz slots (below 0
where the lump is: xx -13714 at the crests and -6605 in the void in time's mean, yy and zz -10788 and -3665, so the
Meshes' grips g + c_ii + c_ii' are slacker at the crests, the x Meshes' 973415 to 976344 of 10^6 at the last round); and
train 2's one count is the pulse, slowed by the well: over the 127 rounds from the first its centroid along x moves
49.33 Meshes against 50.97 for the same pulse in a metric standing at 0 (the same files at push 0), a lag of 1.63
Meshes, and the bend between the crests' rows and the void's is 0.003 Mesh, below the lattice's resolution (the well's
period, 4 Meshes, is the pulse's own width, and a bend needs a well wider than the wavelength). OPEN here, by name
(the edge text's section 4, derive/boss/edge/EDGE2.md on the Boss's derivation branch): the 00 row's own law. The 00
row's teeth stand at rest, the acyclic cut, so its own waves run on the rest cone while light and every other slot run
on the well's, c^2 = grip / W: at this lay every other row's dial reads 6198532 to 6317650 where the 00 row's reads
6000000, a second cone 1033 to 1052 permille of the first.
