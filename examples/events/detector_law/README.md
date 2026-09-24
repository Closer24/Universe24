# The worlds of the launch list under the local detector law

The world files of the rows that
[docs/designs/detector_law/RUN_LIST.md](../../../docs/designs/detector_law/RUN_LIST.md)
marks "to write: the builder", each written by `make_worlds.py` beside them
from its declaration alone
([DECLARATIONS.md](../../../docs/designs/detector_law/declarations/DECLARATIONS.md),
[DESIGN.md](../../../docs/designs/detector_law/DESIGN.md) sections 6.0 to 6.2,
[PINS.md](../../../docs/designs/detector_law/PINS.md) rows 2a, 2c, 5a and 10,
and the launch list's own lines). The rule of the writing (the Boss's order of
2026-09-24): every number in a file is the declaration's; a line the file needs
and the declaration lacks is left ABSENT, so that the loader's refusal names
it, and is reported to the Boss, never filled by the writer. No pin is written
here: the pins script writes `expectations.json` before each run.

The form is the first build's ray-law world
(`tests/test_detector_law.py::chain_world`: `clock_stamp` and `detector_law`
true, a lamp with `rate`, `wheel`, `train` and `directions`, a receiver a
fixed body of the light family with one detector set on its Node) and, for the
massive rows, the massive record series' form (`../massive_record/make_worlds.py`,
whose `world` helper writes them; they live in that folder). A mirror line is
the engine's (M) wall, a block of light's kind of side 1 per Node with the
pair [21, 22] (the launch list's row 10 (a), BUILD.md section 5 (iv-b)).

| Group | Files here | Written from | The loader on main (2026-09-24) |
| --- | --- | --- | --- |
| L | `two_slits.json`; `three_openings_{abc,ab,ac,bc,a,b,c}.json`; `pace_fan_{12,16,24}.json`; `one_opening_near.json`; `one_opening_far.json` | DESIGN.md 6.2, 6.1, 6.0 A; PINS.md 2a, 2c, 5a, 10; the list's lines | refused: `ticks` (not declared); the lamp's Node (not declared); the third opening's place (not declared, the mirror line unbroken); the 24-Link clock pair (not declared); the far opening's board (not declared) |
| T | `bell_{a0b0,a0b1,a1b0,a1b1}.json`; `malus_{45,11.25,28.125,33.75}.json`; `mach_zehnder.json` | DECLARATIONS.md sections 1, 2, 5, 6, 3 | refused: light's clock pair under `detector_law` (the registered K and lamp content give one step per interval; no pair is declared); the Mach-Zehnder lamp's rate, the mirrors' Nodes and the ports (not declared); the splitter's table (refused as a fan under the rule until the splitter component lands) |
| M1, M2 | in `../massive_record/`: `redshift_{k3,control}.json`; `sagnac_{k3,rest}.json`; `matter_waves_{12,16}.json`; `deep_well_{k3,rest}_40.json`; `light_clock_60.json` | DECLARATIONS.md sections 4, 13, 12, 10; the list's step 3 line with `massive_layer_pins.py` | the deep well worlds load; refused: the declared coupling g = [1, 50000] (the load bound of the rows' int64, BUILD.md section 3); `held` light content for `emits` (not declared); light's clock pair (sections 10 and 13); the matter lamp's wheel and omega and the zero line (section 12; the lamp on the massive kind is the component the list names as waiting) |

Regenerate from the repository root:

    PYTHONPATH=src python examples/events/detector_law/make_worlds.py

The dry check of every file, no run and no reading:

    PYTHONPATH=src python -m event_universe.configuration_validation examples/events/detector_law/<world>.json
