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
true, an emitter body of a massive kind with its `emitter` on a wheel and its
stock, seeded on its mode (BUILD.md section 26; the lamp is refused under the
detector law), a receiver a fixed body of the family with one detector set on
its Node, a screen one set per Node of its row) and, for the massive rows, the massive record series'
form (`../massive_record/make_worlds.py`, whose `world` helper writes them;
they live in that folder). Every light wall is the mirror line of section 15
L-1 (the fourth commit): blocks of light's kind of side 1 per Node with the
pair [1, 2], two Nodes deep, the openings left free; the matter wall a barrier
line of matter-kind blocks with the raised pair [1, 2], two deep.

A world whose declared lines the engine on main does not carry yet is written
into `docs/designs/detector_law/held_worlds/`, outside the shipped set under
`examples/events` that the gate loads (the Boss's rule of 2026-09-24: nothing
shipped that the gate loads and refuses); it moves back to its folder when its
line lands. Since PR 1118's merge (main 1454030f: the margin rule skips a
silent block, seed 0 with no record of its own, so an absorbing take line of
the matter kind at the kind's own pair is no longer refused as a mode that is
not bound) every world loads and constructs at its RUN_LIST path, the pre-GO
preflight tool (`tools/preflight_worlds.py`) and the runner sharing that
construction. Since the emitter as a clicking body (BUILD.md section 26) the
four Bell worlds are held there until the crystal (the pair lamp's arms have
no emitter form yet); the emitter's own take of its record, its grace and its
exemption are retired (its cells are cells like every other), so no emitter
carries a timing key.

| Group | Files | Written from | The loader (main 1454030f, 2026-09-24) |
| --- | --- | --- | --- |
| The light rows: the two slits and the pace fans (L) | `two_slits.json`; `pace_fan_{12,16,24}.json` | section 15 L-1 to L-3 and L-6 (row 2a, L-3's second draft: the 160 x 256 layer with x and y open, the four faces the sponges; the lamp at [20, 128, 0] with NO HEADING (regenerated 2026-09-24 on Reviewer 3's second reading, 16:25Z, under the owner's standard: a heading should arise; the loader's default the six headings, an isotropic emitter, the beam's shape the mask's and the split's work; the map that gives the pin drives one Node with no heading, so the pin does not move; the collimated form with `directions` [[1, 0, 0]] HISTORY), the stock 1024 at one per 4 on the wheel [1, 1024], the train 32 periods, the lamp's `receiver` the 201 screen sets (its records' ladder, the faces and the mirror line sinks); the mirror line at x = 40 two deep with two openings of width 3 centred at y = 115 and 141; the screen at x = 153 over y in [28, 228], each set with the rung wheel 2^20; 5500 intervals; row 5a: one record with no heading (the loader's six headings, an isotropic emitter; 16:25Z: the four declared headings HISTORY); the physicist's lines of 2026-09-24 09:02Z and 10:15Z: two probes per ray at 36 and 40 Links on free Nodes, NO ring sets (the drift seen at the probes is a ring's back-scatter, not the front; the fan files carry the lamp and the probes and no detector set), the ticks 1000, 1400 and 1900 per clock, the reader the probes' phase per ray two periods after the front with the spread printed; the clocks [77, 25], [30, 13], [77, 50]) | every file loads; rows 2c, 10 (a), 10 (b) are not in the GO (L-4, L-5) and have no file |
| The tables' rows: Bell's four settings and Malus's four (T) | `bell_{a0b0,a0b1,a1b0,a1b1}.json`; `malus_{45,11.25,28.125,33.75}.json` | sections 1, 2, 5, 6 with section 14 item 1 and section 15 T-1 (the clocks [2464, 25] on N = 2048 and [308, 25] on N = 256 on the light family, [1, 1] on the counter family, the wheel [1, N]); the Bell lamp's stock `amount` 2048 (exactly W births, section 2 item 8), its `residue_order` "seed" with one `residue_seed` per world (section 2 item 8: a 64-bit draw from the host's entropy, drawn once and kept over regenerations) and `ticks` 5500 (2048 births, the completion 3204 intervals after the last birth on the engine's train of 3200, the far arm's transit 13, the margin 235); the Malus lamp's train 32 periods, its stock `amount` 256 (the count of 256 births) and `ticks` 1200 (section 5 item 2); the Malus bar 8 x 1 x 1 with the polariser's set alone on its entry Node at x = 6 (the exit cell at x = 7 on the board; the registered which-path read body at x = 4 and its set `first` dropped, section 5 item 1, 12:15Z) | every file loads (the builder's line 8 under the declared names); row 2b is not in the GO (T-2) and has no file |
| The massive rows: the moving lamp's redshift, the Sagnac ratio, the light clock, the energy of a moving mass, de Broglie's fringes (M1) | in `../massive_record/`: `redshift_{k3,control}.json`; `sagnac_{k3,rest}.json`; `light_clock_60.json`; `matter_front_12.json`; `matter_waves_{12,16}.json` | sections 4, 13, 10, 12 with section 15 M1-1 to M1-10 (G = [1, 50], g = [1, 1000], the seed 50 x 2^20; no held content; light [1, 1]; 4b on the loader's 4096 chain: A at 2994, the receiver's set at 4094 with wheel 64, `own_grace` 3000 and the world key `wheel` 64, 9600 intervals (the physicist's 10:15Z: 10000 runs A off the board at 9732); R2's sets bound to the blocks by `block` with wheel 256 and `own_grace` 3000; the light clock's set `block` 0 with the one position [612, 0, 0] and wheel 64, `own_grace` 70, the faces closed for light, 2600 intervals (the physicist's 09:18Z); `amplitude_bound` 2^32; the world key `wheel`, the ladder's W, on the worlds with a set and no lamp: 256 on R2's two files (the physicist's 07:37Z, one integer with the sets' rung), 64 on 4b's two and on the light clock; R2 on the chain of 3000 with 6400 (k3) and 8450 (rest) intervals (the physicist's 08:06Z on Reviewer 3's arithmetic: every hold record completes); the matter family's `phase_per_link` [1089, 320] or [11, 4] and its `take` [-19, 86] or [-5, 27]; the sized form of section 12 and SIZING.md: the lamp with the wheel [1, 2048], the stock 2048 at one per 2, the train 8 periods, `own_grace` 4700 (the hold) and its `receiver` the screen's 121 sets (the ladder; the take lines sinks outside it), the sets with the rung wheel 65536, 4700 intervals; the wall a barrier line of the raised pair [1, 2] two deep; the take lines absorbing blocks of the matter kind with the kind's own pair and the take's pair [-19, 86] or [-5, 27] under the builder's key `take`) | every file loads and constructs (the take lines' blocks are silent, seed 0, so the margin rule skips them since PR 1118) |

The deep well worlds of group M2 are the massive record series' own
(`../massive_record/make_worlds.py`).

Regenerate from the repository root:

    PYTHONPATH=src python examples/events/detector_law/make_worlds.py

The dry check of every file, no run and no reading:

    PYTHONPATH=src python -m event_universe.configuration_validation examples/events/detector_law/<world>.json
