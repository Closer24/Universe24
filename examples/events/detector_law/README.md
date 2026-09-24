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
line lands. Since 2026-09-24 06:10Z every emitter of every world carries
`remnant_take` (DECLARATIONS.md section 10 item 10: the intervals after its
train from which its own cells take its own record's remnant, ceil(extent /
v_g) + 2 on the band's group pace at the declared wavelength; 4 for a one-Node
lamp of light, 24 for an emitting block of side 12, 4 and 5 for the matter
lamps at 12 and 16 Links), a key the loader on main does not carry, so every
world is held until the builder's line lands; the files are then load-checked
on his SHA and moved back.

| Group | Files (all held) | Written from | The loader (2026-09-24, the builder's head 299b6bb2) |
| --- | --- | --- | --- |
| L | `two_slits.json`; `pace_fan_{12,16,24}.json` | section 15 L-1 to L-3 and L-6 (row 2a: the lamp at [20, 64, 0], the stock 1024 at one per 16, the train 32 periods, the mirror line at x = 40 two deep, the screen at x = 104, the open faces the sponges, 17300 intervals; row 5a: one record on the four headings, the probes and ring sets at eight Nodes, 800 intervals; the clocks [77, 25], [30, 13], [77, 50]); the lamps' `remnant_take` 4 | every line loads but `remnant_take`; rows 2c, 10 (a), 10 (b) are not in the GO (L-4, L-5) and have no file |
| T | `bell_{a0b0,a0b1,a1b0,a1b1}.json`; `malus_{45,11.25,28.125,33.75}.json` | sections 1, 2, 5, 6 with section 14 item 1 and section 15 T-1 (the clocks [2464, 25] on N = 2048 and [308, 25] on N = 256 on the light family, [1, 1] on the counter family, the wheel [1, N]); the Bell lamp's `residue_order` "seed" with one `residue_seed` per world (section 2 item 8: a 64-bit draw from the host's entropy, drawn once and kept over regenerations) and `ticks` 5000 (2048 births, the train's 2660 intervals, the far arm's transit 13, the completion's allowance); the Malus lamp's train 32 periods, its stock `amount` 256 (the count of 256 births) and `ticks` 1200 (section 5 item 2); the lamps' `remnant_take` 4 | every line loads but `remnant_take` and, on the Bell lamp, `residue_order` and `residue_seed` (the builder's line 8 on 299b6bb2 spells the world key `order_seed` instead; the declaration's spelling is written); row 2b is not in the GO (T-2) and has no file |
| M1 | for `../massive_record/`: `redshift_{k3,control}.json`; `sagnac_{k3,rest}.json`; `light_clock_60.json`; `matter_waves_{12,16}.json`; `matter_front_12.json` | sections 4, 13, 10, 12 with section 15 M1-1 to M1-10 (G = [1, 50], g = [1, 1000], the seed 50 x 2^20; no held content; light [1, 1]; 4b on the loader's 4096 chain: A at 2994, the receiver's set at 4094 with wheel 64, `own_grace` 8000, 14686 intervals; R2's sets bound to the blocks by `block` with wheel 256 and `own_grace` 3000; the light clock's set `block` 0 with the one position [612, 0, 0] and wheel 64, `own_grace` 70, the faces closed for light; `amplitude_bound` 2^32; the emitting blocks' `remnant_take` 24; the matter family's `phase_per_link` [1089, 320] or [11, 4], the lamp with the wheel [1, 64], the stock 2048 at one per 8, the train 8 periods, `own_grace` 16700 and `remnant_take` 4 or 5; the wall a barrier line of the raised pair [1, 2] two deep; the take lines absorbing blocks of the matter kind with the kind's own pair and the take's pair [-19, 86] or [-5, 27] under the builder's key `take`) | every line loads but `remnant_take` (on main: `amplitude_bound` the first unknown key named, then the rest of the builder's keys) |

The deep well worlds of group M2 are the massive record series' own
(`../massive_record/make_worlds.py`).

Regenerate from the repository root:

    PYTHONPATH=src python examples/events/detector_law/make_worlds.py

The dry check of every file, no run and no reading:

    PYTHONPATH=src python -m event_universe.configuration_validation docs/designs/detector_law/held_worlds/<world>.json
