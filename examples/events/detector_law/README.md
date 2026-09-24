# The worlds of the launch list under the local detector law

The world files of the rows that
[docs/designs/detector_law/RUN_LIST.md](../../../docs/designs/detector_law/RUN_LIST.md)
marks "to write: the builder", each written by `make_worlds.py` beside them
from its declaration alone
([DECLARATIONS.md](../../../docs/designs/detector_law/declarations/DECLARATIONS.md),
its section 15 the world lines row by row and section 14 the tables' clocks;
[DESIGN.md](../../../docs/designs/detector_law/DESIGN.md) sections 6.0 to 6.2;
[PINS.md](../../../docs/designs/detector_law/PINS.md); the launch list's own
lines). The rule of the writing (the Boss's order of 2026-09-24): every number
in a file is the declaration's; a line the file needs and the declaration
lacks is left ABSENT, so that the loader's refusal names it, and is reported
to the Boss, never filled by the writer. No pin is written here: the pins
script writes `expectations.json` before each run.

The form is the first build's ray-law world
(`tests/test_detector_law.py::chain_world`: `clock_stamp` and `detector_law`
true, a lamp with `rate`, `wheel`, `train` and `directions`, a receiver a
fixed body of the family with one detector set on its Node, a screen one set
per Node of its row) and, for the massive rows, the massive record series'
form (`../massive_record/make_worlds.py`, whose `world` helper writes them;
they live in that folder). Every wall is the absorbing form of section 15
L-1: a block of side 1 per Node with `absorbing` true (on light's kind the
pair [21, 22]), the openings left free.

| Group | Files | Written from | The loader on main (2026-09-24, after section 15) |
| --- | --- | --- | --- |
| L | `two_slits.json`; `pace_fan_{12,16,24}.json` | section 15 L-1 to L-3 and L-6 (row 2a: the lamp at [20, 64, 0], the stock 1024 at one per 16, the train 32 periods, the wall at x = 40, the screen at x = 104, the take lines, 17300 intervals; row 5a: one record on the four headings, the probes and ring sets at eight Nodes, 800 intervals; the clocks [77, 25], [30, 13], [77, 50]) | the four files load; rows 2c, 10 (a), 10 (b) are not in the GO (L-4, L-5) and have no file |
| T | `bell_{a0b0,a0b1,a1b0,a1b1}.json`; `malus_{45,11.25,28.125,33.75}.json` | sections 1, 2, 5, 6 with section 14 item 1 and section 15 T-1 (the clocks [2464, 25] on N = 2048 and [308, 25] on N = 256 on the light family, [1, 1] on the counter family, the wheel [1, N]) | the eight files load; row 2b is not in the GO (T-2) and has no file |
| M1 | in `../massive_record/`: `redshift_{k3,control}.json`; `sagnac_{k3,rest}.json`; `light_clock_60.json`; `matter_waves_{12,16}.json`; `matter_front_12.json` | sections 4, 13, 10, 12 with section 15 M1-1 to M1-6 (G = [1, 50], g = [1, 1000], the seed 50 x 2^20; no held content; light [1, 1]; the receivers detector sets at the receiving body's cells with their own wheel 64, M1-4; R2's faces open for both kinds, M1-7; the light clock's faces closed for light; the matter lamp's clock [1089, 320] or [11, 4], the wheel [1, 64], the stock 2048 at one per 8, the train 8 periods, the walls absorbing blocks of the matter kind) | refused, the builder's lines: `emits` without `held` (M1-2); a detector set's own `wheel` (M1-4, key (i)); the closed face for light (section 10); the lamp on the massive kind and its clock key (M1-6); the matter walls' block pair (not declared) |

The deep well worlds of group M2 are the massive record series' own
(`../massive_record/make_worlds.py`).

Regenerate from the repository root:

    PYTHONPATH=src python examples/events/detector_law/make_worlds.py

The dry check of every file, no run and no reading:

    PYTHONPATH=src python -m event_universe.configuration_validation examples/events/detector_law/<world>.json
