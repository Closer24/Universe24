# The demonstration worlds of the visual gallery

The pages of [the visual gallery](../../../docs/pages/gallery/index.html)
(the model owner's request of 2026-09-21: the situations of the law in
HTML pages, beams and clicks, nothing else) show a registered world
wherever one shows the story. Where none does, a page shows one of the
worlds here, written by `make_worlds.py`, under the one engine
([the Beam Law](../../../docs/BEAM_LAW.md), [the engine](../../../docs/ENGINE.md)).
They are demonstrations: not experiments of
[the register](../../../docs/EXPERIMENTS.md), no number read off them is
registered, no test pins one, and a page made from one says so. The pages
are written by `tools/gallery_pages.py`, which replays a world in process
and reads the engine's stores for the picture (a GameBoard reading) and
the runner's record for the readings (detector readings).

| World | What it declares | What the page shows |
| --- | --- | --- |
| `beam_fan.json` | An open plane of 41 x 41 (z periodic with an extent of 1), a lamp of the paid family `light` at the centre (content 2^25 at K = 2^22: the turn 8 phase steps of 64 per self-creation, every unit costing 8 content, E = h f) releasing one unit per self-creation on every primitive in-plane direction with abs(a) + abs(b) <= 6, 48 directions; 60 intervals | [The beam](../../../docs/pages/gallery/beam.html): the rows spreading on the digital lines of the fan at the pace of the flight table, the front round (the circle of c = 1 / sqrt 3 inside the L1 bound), the phase as colour (a record's birth phase u) |
| `collision.json` | An open cube of 9 x 9 x 9 with no measured event and six declared rows of `light` of one number and content: a head-on pair on the x axis meeting at (4, 4, 4), a triple +x, -x, +y meeting at (4, 4, 1), and a lone unit on a diagonal; 30 intervals | The collision (the page in preparation): the collision table's permutation at a Node of free space, the head-on pair parking on the rest slots, turning to another axis and leaving, the triple's odd unit going on, the diagonal unit a spectator |

Write them again and make the pages:

```bash
python examples/events/gallery/make_worlds.py
PYTHONPATH=src python tools/gallery_pages.py --page all --runs artifacts/gallery_runs
```
