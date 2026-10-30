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

`examples/tensor24-live/` is a fourth folder of the same three files, a world that shows something: the light train's
first component laid as a pulse along z, its peak at 2^40 counts (far above one notch), its before slot one round back
by the lattice's own speed (c^2 = grip / W = 1 / 6 per axis at the loader's rest, c about 20 / 49 Meshes a round), so
the pulse travels toward +z and crosses the board of 3 by 3 by 40 in its 100 rounds; the metric family stands at 0, a
standing clock, so the act is exact and the run back returns the start bit for bit. Run it as the one bang:
`python -I tools/tensor24_run.py examples/tensor24-live/universe.json examples/tensor24-live/piece.json
examples/tensor24-live/setting.json <record .jsonl>`; the ledger beside the record holds the light's counts at every
Node-clock and round, the pulse's peak moving along z. The clocks' wells, the grips' lengthening and the clicks are
owed to the terms still drafted (5, 9 and 11); the window of the wave, 0 <= SUM grip / W <= 1, is read by the runner.
