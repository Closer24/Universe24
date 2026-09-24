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
they live in that folder). Every light wall is the mirror line of section 15
L-1 (the fourth commit): blocks of light's kind of side 1 per Node with the
pair [1, 2], two Nodes deep, the openings left free; the matter wall a barrier
line of matter-kind blocks with the raised pair [1, 2], two deep.

A world whose declared lines the engine on main does not carry yet is written
into `docs/designs/detector_law/held_worlds/`, outside the shipped set under
`examples/events` that the gate loads (the Boss's rule of 2026-09-24: nothing
shipped that the gate loads and refuses); it moves back to its folder when its
line lands.

| Group | Files | Written from | The loader on main (2026-09-24, after section 15) |
| --- | --- | --- | --- |
| L | `pace_fan_{12,16,24}.json`; held: `two_slits.json` | section 15 L-1 to L-3 and L-6 (row 2a: the lamp at [20, 64, 0], the stock 1024 at one per 16, the train 32 periods, the mirror line at x = 40 two deep, the screen at x = 104, the open faces the sponges, 17300 intervals; row 5a: one record on the four headings, the probes and ring sets at eight Nodes, 800 intervals; the clocks [77, 25], [30, 13], [77, 50]) | the fan worlds load; two_slits loads but is held until the engine's path for a block of light's kind lands (L-1); rows 2c, 10 (a), 10 (b) are not in the GO (L-4, L-5) and have no file |
| T | `bell_{a0b0,a0b1,a1b0,a1b1}.json`; `malus_{45,11.25,28.125,33.75}.json` | sections 1, 2, 5, 6 with section 14 item 1 and section 15 T-1 (the clocks [2464, 25] on N = 2048 and [308, 25] on N = 256 on the light family, [1, 1] on the counter family, the wheel [1, N]) | the eight files load; row 2b is not in the GO (T-2) and has no file |
| M1 | held (for `../massive_record/`): `redshift_{k3,control}.json`; `sagnac_{k3,rest}.json`; `light_clock_60.json`; `matter_waves_{12,16}.json`; `matter_front_12.json` | sections 4, 13, 10, 12 with section 15 M1-1 to M1-10 on main at 96fdfd7a (G = [1, 50], g = [1, 1000], the seed 50 x 2^20; no held content; light [1, 1]; the receivers detector sets bound to their body by `block` with their own wheel 64; `own_grace` 70 on the light clock's A and R2's blocks, 16700 on the matter lamp; `amplitude_bound` 2^32; R2's faces open for both kinds; the light clock's faces closed for light; the matter family's `phase_per_link` [1089, 320] or [11, 4], the lamp with the wheel [1, 64], the stock 2048 at one per 8, the train 8 periods; the wall a barrier line of the raised pair [1, 2] two deep; the take lines absorbing blocks of the matter kind with the take's pair [-19, 86] or [-5, 27]) | refused on main's loader, the builder's keys: `amplitude_bound` (the first unknown key named), then `own_grace`, the sets' `block` and `wheel`, the face value "closed", the matter family's `phase_per_link` with its lamp, the raised pair and the take's pair on a block; section 4 declares no `own_grace` for 4b's emitter |

The deep well worlds of group M2 are the massive record series' own
(`../massive_record/make_worlds.py`).

Regenerate from the repository root:

    PYTHONPATH=src python examples/events/detector_law/make_worlds.py

The dry check of every file, no run and no reading:

    PYTHONPATH=src python -m event_universe.configuration_validation examples/events/detector_law/<world>.json
