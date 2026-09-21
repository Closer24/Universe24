"""Write the worlds of series N, "the binding that costs content"
(`binding-v1`; the model owner's records 115 and 137 of 2026-09-20, the
physicist's design docs/designs/binding_v1/DESIGN.md sections 1 to 6, BEAM_LAW
note 40): the nucleons of series I carrying a paid family `bond` (quantum 1,
lifetime 3, no column, no phase circle) held 2 per nucleon, the free totals
kept at 1837 (p = 1834 `p` + 1 `nuclear` + 2 `bond`) and 1840 (n = 1837 `n`
+ 1 `nuclear` + 2 `bond`). At a contact under `measure` the refused body
gives its held `bond` to the flight on the heading opposite to the refused
step (`engine._give`): the border `lifetime` clicks the row two Links away
with its content, the released binding energy, measurable as clicks.

The base is series I's (`../nucleus/make_worlds.py`, loaded from its file:
the fan of 290 directions, K 2^20, N 64, `release` [1, 1], `suspension` 0,
`width` 2^28, an open 21^3 cube, 3000 intervals, the families `p`, `n` and
`nuclear` with the strong column 10000 and the lifetime 3). The worlds
(DESIGN section 4; README.md here has the pins):

| world | what |
| --- | --- |
| `deuteron_bond` (B1) | series I's `deuteron_1` with `bond` 2 per nucleon |
| `proton_bond_lamp` (B2) | the control: one proton alone at (10, 10, 10) with the I7 lamp (`light` 2^23, rate [1, 1], +y, a `sum` set four Links up, `amplitude` true) |
| `alpha_square_bond` (B3) | series I's `alpha_square` with `bond` 2 per nucleon |

    python examples/events/binding/make_worlds.py [--out DIR]
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / "src"))

from event_universe.world_loading import families_by_definition  # noqa: E402

FAMILY_DEFINITIONS = "../entities/families.json"
DEFINITIONS_SOURCE = (HERE.parent / "entities" / "families.json").read_bytes()
Json = dict[str, object]


def _nucleus_generator():
    """Series I's generator, loaded from its file (one canonical base)."""
    path = HERE.parent / "nucleus" / "make_worlds.py"
    spec = importlib.util.spec_from_file_location("nucleus_make_worlds", path)
    module = importlib.util.module_from_spec(spec)
    sys.modules["nucleus_make_worlds"] = module
    spec.loader.exec_module(module)
    return module


NUCLEUS = _nucleus_generator()

# The paid family a nucleon carries: the quantum h = 1 (one unit of content
# per unit), the lifetime 3 (the row clicks on the border two Links from its
# birth), no column and no phase circle, as `nuclear`.
BOND = {"name": "bond", "quantum": 1, "lifetime": NUCLEUS.LIFETIME, "phase": False}
BOND_HELD = 2
# The I7 lamp beside the proton (docs/LOG_2026-09-20.md record 123): `light`
# of content 8 x K (s = 8 per self-creation, the click's content 8), fixed,
# one row per self-creation on +y, one Link from the proton; its `sum` set
# of one `counter` Node four Links up the line.
LAMP_CONTENT = 8 * NUCLEUS.K
LAMP_OFFSET = (0, 1, 0)
SET_OFFSET = (0, 5, 0)


def bonded(body: Json) -> Json:
    """A nucleon of series I carrying `bond` 2: its own family's amount
    lowered by 2 so that its content (the sum of what it holds) is the
    register's 1837 or 1840."""
    held = dict(body["held"])
    held["bond"] = BOND_HELD
    return {**body, "amount": int(body["amount"]) - BOND_HELD, "held": held}


def world(name: str, bodies: list[Json]) -> Json:
    document = NUCLEUS.world(name, bodies)
    document["model_id"] = f"beam-binding-{name}-space-v1"
    document["families"] = [*document["families"], dict(BOND)]
    return document


def worlds() -> dict[str, Json]:
    c = NUCLEUS.SIDE // 2
    proton = (c, c, c)
    lamp = tuple(a + b for a, b in zip(proton, LAMP_OFFSET, strict=True))
    counter = tuple(a + b for a, b in zip(proton, SET_OFFSET, strict=True))
    control = world("proton_bond_lamp", [bonded(NUCLEUS.nucleon("p", proton))])
    control["families"] = [
        *control["families"],
        {"name": "light", "quantum": 1},
        {"name": "counter", "quantum": 1},
    ]
    control["measured"] = [
        *control["measured"],
        {
            "position": list(lamp),
            "family": "light",
            "amount": LAMP_CONTENT,
            "phase": 0,
            "fixed": True,
            "lamp": {"rate": [1, 1], "wheel": [1, 64], "directions": [list(LAMP_OFFSET)]},
        },
        {"position": list(counter), "family": "counter", "amount": 1, "fixed": True},
    ]
    # The lamp's rows are records (the one click of stage (vii): every lamp
    # births records, the world key `amplitude` deleted, MIGRATION (vii-4)).
    control["detectors"] = [
        {"name": "bound_set", "positions": [list(counter)], "threshold": 1, "reading": "sum"}
    ]
    return {
        "deuteron_bond": world(
            "deuteron_bond",
            [bonded(NUCLEUS.nucleon("p", proton)), bonded(NUCLEUS.nucleon("n", (c + 1, c, c)))],
        ),
        "proton_bond_lamp": control,
        "alpha_square_bond": world(
            "alpha_square_bond",
            [
                bonded(NUCLEUS.nucleon("p", (c, c, c))),
                bonded(NUCLEUS.nucleon("n", (c + 1, c, c))),
                bonded(NUCLEUS.nucleon("n", (c, c + 1, c))),
                bonded(NUCLEUS.nucleon("p", (c + 1, c + 1, c))),
            ],
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("--out", type=Path, default=HERE)
    args = parser.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)
    for name, document in worlds().items():
        path = args.out / f"{name}.json"
        document = families_by_definition(document, FAMILY_DEFINITIONS, DEFINITIONS_SOURCE)
        path.write_text(json.dumps(document, separators=(",", ":")) + "\n", encoding="utf-8")
        print(path)


if __name__ == "__main__":
    main()
