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
| `clicks_plate.json` | An open plane of 31 x 11, a lamp of `light` at (1, 5) (content 2^25 at K = 2^22) releasing one unit per self-creation on five directions within 5 degrees of +x (the heading and (24, +-1, 0), (12, +-1, 0), series K's narrow beam), a plate at x = 29 of eleven measured events of the paid family `apparatus` declared as the one-Node `wave` detectors `plate_<y>`; 110 intervals | [The clicks](../../../docs/pages/gallery/clicks.html): every record's five rows ending on the plate, its one click landing on one pixel by the ladder's rungs and its wheel value u, the click list growing one line per record |
| `collision.json` | An open cube of 9 x 9 x 9 with no measured event and six declared rows of `light` of one number and content: a head-on pair on the x axis meeting at (4, 4, 4), a triple +x, -x, +y meeting at (4, 4, 1), and a lone unit on a diagonal; 30 intervals | [The collision](../../../docs/pages/gallery/collision.html): the collision table's permutation at a Node of free space, the head-on pair parking on the rest slots, turning to another axis and leaving, the triple's odd unit going on, the diagonal unit a spectator |
| `proton_electron.json` | Series R's registered `q1_proton_line` as it is (the quark bodies u d u at (9..11, 10, 10), each holding one unit of `glue`; the families, the fan of 290 directions and the width 2^37 unchanged) with one more free family `e` (one unit of content, the charge -7344 per unit, minus the register's proton; no strong column) and one body of it at (3, 10, 10) thrown +x with the momentum 2 x 10^13 label units; 600 intervals | [The quarks](../../../docs/pages/gallery/quarks.html): the electron reaching the line, handing its momentum to the first quark through the contact, the momentum passing down the line, the far quark walking off through the face +x and the rest following: the law binds and does not confine |
| `clock_6.json` | Series P's registered `crowd_clock/still_3` (the lamp `s_px1` at rest at (10, 4, 4) shining +x to the detector at x = 110, two `mass` sources releasing F = 4915 units per interval each on the fan of nine, the suspension [1, 2^16]) with the two sources moved from three Links to six, (10, 10, 4) and (10, 4, 10), on a bar of 121 x 15 x 15; 30 intervals | [The clock's word](../../../docs/pages/gallery/clock.html): the presence at the lamp's Node 4 F at six Links as at three, the age moment 42 F against 22 F: the presence clock cannot tell the distances apart, the age clock can (the physicist's two-crowd pin, `docs/designs/clock_age/NOTE.md`) |

Write them again and make the pages:

```bash
python examples/events/gallery/make_worlds.py
PYTHONPATH=src python tools/gallery_pages.py --page all --runs artifacts/gallery_runs
```
