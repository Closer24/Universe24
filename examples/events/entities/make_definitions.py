"""Write the canonical entity definitions of the register: `families.json`,
one definition per family the registered worlds declare (the model owner's
decision of 2026-09-20, record 113 of docs/LOG_2026-09-20.md: one canonical
definition per family, referenced by the worlds; the rows of
docs/ENTITY_CATALOG.md), and `apparatus.json`, the external things and the
sources of `amplitude-v1` as measured events and detector sets with the
material family each is made of. Both in the format `event-entities-v2`
(docs/ENTITY_DEFINITIONS.md): a definition may carry `families`, merged into
the world that places it by name. A family named by two series with
different keys (the proton's charge per series, the coupling's test
charges, the amplitude series' `phase_per_link` as a pair, the quark
worlds' `d` against the detector material `d`, the dressed quark world's
`glue` at a pair) is written here in the catalog's canonical form; a world
whose family differs keeps it inline. The amounts of the sources are for a
world of `K` 4096 (a turn of 1 per self-creation on a content of 4096); a
world with another `K` writes its own source.

    python examples/events/entities/make_definitions.py
"""

from __future__ import annotations

import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
FORMAT = "event-entities-v2"
SOURCE_CONTENT = 4096
QUARTER_TURN = 16  # N / 4 at N = 64, the reflection's turn
LEFT, RIGHT, UP = [-1, 0, 0], [1, 0, 0], [0, 1, 0]


def family_definition(name: str, families: list[dict[str, object]]) -> dict[str, object]:
    return {"name": name, "families": families, "measured": [], "detectors": []}


def families() -> dict[str, object]:
    """One definition per family of the register, its keys the catalog's row."""
    free_mass = {"quantum": 0, "charge": 0, "phase": False}
    inert = {"quantum": 1}
    entities = [
        family_definition("photon", [{"name": "light", **inert}]),
        family_definition("electron", [{"name": "e", "quantum": 0, "charge": -15, "phase": True}]),
        family_definition("electron_born_by_become", [{"name": "beta", "quantum": 1, "charge": -7344}]),
        family_definition("proton", [{"name": "p", "quantum": 0, "charge": [1, 1], "phase": False}]),
        family_definition("neutron", [{"name": "n", "quantum": 0, "phase": False}]),
        family_definition(
            "strong_family",
            [
                {
                    "name": "nuclear",
                    "quantum": 0,
                    "columns": {"strong": {"value": 10000, "sign": -1}},
                    "lifetime": 3,
                    "phase": False,
                }
            ],
        ),
        # The paid content a nucleon carries and gives at its first contact
        # (`binding-v1`, series N; BEAM_LAW note 40): no column, no phase
        # circle, the lifetime 3 as the strong family's.
        family_definition(
            "bond_family", [{"name": "bond", "quantum": 1, "lifetime": 3, "phase": False}]
        ),
        # The quarks of series R (docs/designs/quarks/QUARKS.md; the worlds
        # of `quarks/`): the up quark `u`, and `glue`, the strong family a
        # quark body holds one unit of (the keys of `nuclear` under another
        # name). The down quark `d` of the same worlds shares its name with
        # the detector material `d` below and keeps its row inline; so does
        # the dressed world's `glue` at the pair [10000, 606].
        family_definition("up_quark", [{"name": "u", "quantum": 0, "charge": 1224, "phase": False}]),
        family_definition(
            "glue_family",
            [
                {
                    "name": "glue",
                    "quantum": 0,
                    "columns": {"strong": {"value": 10000, "sign": -1}},
                    "lifetime": 3,
                    "phase": False,
                }
            ],
        ),
        family_definition("neutrino", [{"name": "nu", "quantum": 0}]),
        # The antineutrino of series P (`hand-v1`): a free family whose every
        # row is right-handed, born along a polarised parent's axis.
        family_definition("antineutrino", [{"name": "nubar", "quantum": 0, "hand": 1}]),
        family_definition(
            "w_boson", [{"name": "w", "quantum": 1, "charge": -7344, "lifetime": 1, "phase": False}]
        ),
        family_definition("wall_material", [{"name": "wall", **inert}]),
        family_definition("screen_material", [{"name": "screen", **inert}]),
        family_definition("counter_material", [{"name": "counter", **inert}]),
        family_definition("apparatus_material", [{"name": "apparatus", **inert}]),
        family_definition("carrier_material", [{"name": "carrier", **inert}]),
        family_definition("detector_material", [{"name": "detector", **inert}]),
        family_definition("detector_material_d", [{"name": "d", "quantum": 1, "phase": False}]),
        family_definition("mass_m", [{"name": "m", **free_mass}]),
        family_definition("mass", [{"name": "mass", **free_mass}]),
        family_definition("neutron_star_material", [{"name": "neutron", **free_mass}]),
        family_definition("probe_material", [{"name": "probe", **free_mass}]),
        family_definition("source_material", [{"name": "s", "quantum": 0, "phase": False}]),
        family_definition("test_charge", [{"name": "q", "quantum": 0, "charge": [0, 1]}]),
        family_definition("choosers", [{"name": "sa", "quantum": 0}, {"name": "sb", "quantum": 0}]),
        family_definition(
            "thrown_sources",
            # In the order the Hubble worlds declare them (one instance of
            # this definition is the tail of their `families`): per axis,
            # the four thrown toward +axis, then the four toward -axis.
            [
                {"name": f"{kind}{axis}{index}", "quantum": 0}
                for axis in ("x", "y", "z")
                for kind in ("p", "m")
                for index in (1, 2, 3, 4)
            ],
        ),
        family_definition(
            "hubble_stars",
            # In the order the series G2 worlds declare them (one instance of
            # this definition is the tail of their `families`): the stars
            # dealt round-robin over the six axes in Port order, rank by
            # rank; each a paid light family of its own (quantum 1).
            [
                {"name": f"s_{axis}{rank}", "quantum": 1}
                for rank in (1, 2, 3, 4)
                for axis in ("px", "mx", "py", "my", "pz", "mz")
            ],
        ),
        # The massive quantum (`massive-rows-v1`, 2026-09-21): a paid family
        # declared `massive` with its phase circle spelled, placed with its
        # lamp (the pin's keys: M 64, p 220, the wheel of `slits_matter`),
        # since the family's tables are formed from its lamp's
        # `momentum_magnitude`; a world that places it declares
        # `massive_rows`, `action` and `age_bound`. The pin worlds spell the
        # family by the design's row (no `phase` key) and carry their own
        # lamp, so they keep it inline and place no second lamp.
        {
            "name": "massive_quantum",
            "families": [{"name": "matter", "quantum": 64, "phase": True, "massive": True}],
            "measured": [
                measured(
                    "matter",
                    [0, 0, 0],
                    amount=SOURCE_CONTENT,
                    lamp={
                        "rate": [1, 1],
                        "wheel": [2531, 4096],
                        "directions": [RIGHT],
                        "momentum_magnitude": 220,
                    },
                )
            ],
            "detectors": [],
        },
    ]
    return {"format": FORMAT, "entities": entities}


def measured(family: str, position: list[int], **keys: object) -> dict[str, object]:
    return {"position": position, "family": family, "amount": 1, "fixed": True, **keys}


def light() -> list[dict[str, object]]:
    return [{"name": "light", "quantum": 1}]


def material(name: str) -> list[dict[str, object]]:
    return [{"name": name, "quantum": 1}]


def apparatus() -> dict[str, object]:
    """The external things and the sources of `amplitude-v1`, each with the
    family it is made of; a table entry names `light`, the world's or a
    source's."""
    origin = [0, 0, 0]
    counter_window = {"light": {"phase_window": 0}}
    entities = [
        {
            "name": "lamp",
            "families": light(),
            "measured": [
                measured(
                    "light",
                    origin,
                    amount=SOURCE_CONTENT,
                    lamp={"rate": [1, 1], "wheel": [1, 64], "directions": [RIGHT]},
                )
            ],
            "detectors": [],
        },
        {
            "name": "laser",
            "families": light(),
            "measured": [
                measured(
                    "light",
                    origin,
                    amount=SOURCE_CONTENT,
                    lamp={"rate": [1, 1], "wheel": [1, 64], "directions": [RIGHT], "phase_window": 16},
                )
            ],
            "detectors": [],
        },
        {
            "name": "mirror",
            "families": material("apparatus"),
            "measured": [measured("apparatus", origin, directions=[UP], table={"light": "rerelease"})],
            "detectors": [],
        },
        {
            "name": "wall",
            "families": material("wall"),
            "measured": [measured("wall", [x, 0, 0]) for x in range(3)],
            "detectors": [],
        },
        {
            "name": "slit",
            "families": material("wall"),
            "measured": [
                measured("wall", [0, 0, 0]),
                measured("wall", [1, 0, 0], directions=[UP, LEFT, RIGHT], table={"light": "rerelease"}),
                measured("wall", [2, 0, 0]),
            ],
            "detectors": [],
        },
        {
            "name": "screen",
            "families": material("screen"),
            "measured": [measured("screen", [x, 0, 0]) for x in range(3)],
            "detectors": [
                {
                    "name": "screen",
                    "positions": [[x, 0, 0] for x in range(3)],
                    "threshold": 1,
                    "reading": "wave",
                }
            ],
        },
        {
            "name": "pixel",
            "families": material("screen"),
            "measured": [measured("screen", origin)],
            "detectors": [{"name": "pixel", "positions": [origin], "threshold": 1, "reading": "wave"}],
        },
        {
            "name": "probe",
            "families": [{"name": "probe", "quantum": 0, "charge": 0, "phase": False}],
            "measured": [measured("probe", origin)],
            "detectors": [],
        },
        {
            "name": "clock",
            "families": [{"name": "probe", "quantum": 0, "charge": 0, "phase": False}],
            "measured": [measured("probe", origin, span=[3, 3, 3])],
            "detectors": [],
        },
        {
            "name": "pair_source",
            "families": light(),
            "measured": [
                measured(
                    "light",
                    origin,
                    amount=SOURCE_CONTENT,
                    lamp={
                        "rate": [1, 1],
                        "wheel": [1, 64],
                        "directions": [LEFT, RIGHT],
                        "arms": 2,
                        "branches": [[0, 1], [3, 1]],
                    },
                )
            ],
            "detectors": [],
        },
        {
            "name": "ghz_source",
            "families": light(),
            "measured": [
                measured(
                    "light",
                    origin,
                    amount=SOURCE_CONTENT,
                    lamp={
                        "rate": [1, 1],
                        "wheel": [1, 64],
                        "directions": [LEFT, RIGHT, UP],
                        "arms": 3,
                        "branches": [[0, 1], [7, 1]],
                    },
                )
            ],
            "detectors": [],
        },
        {
            "name": "splitter",
            "families": material("apparatus"),
            "measured": [
                measured(
                    "apparatus",
                    origin,
                    directions=[RIGHT, UP],
                    table={
                        "light": {
                            "rule": "rerelease",
                            "inputs": [UP, RIGHT],
                            "weights": [[1, 1], [1, 1]],
                            "turns": [[QUARTER_TURN, 0], [0, QUARTER_TURN]],
                        }
                    },
                )
            ],
            "detectors": [],
        },
        {
            "name": "label_rotation",
            "families": material("apparatus"),
            "measured": [
                measured(
                    "apparatus",
                    origin,
                    directions=[UP],
                    table={"light": {"rule": "rerelease", "rotate": {"setting": QUARTER_TURN}}},
                )
            ],
            "detectors": [],
        },
        {
            "name": "cnot_gate",
            "families": material("apparatus"),
            "measured": [
                measured(
                    "apparatus",
                    origin,
                    directions=[UP, RIGHT],
                    table={
                        "light": {
                            "rule": "rerelease",
                            "inputs": [UP, RIGHT],
                            "weights": [[1, 0], [0, 1]],
                            "gate": {"kind": "cnot", "hold": True, "parties": 2, "control": UP},
                        }
                    },
                )
            ],
            "detectors": [],
        },
        {
            "name": "counter_pair",
            "families": material("counter"),
            "measured": [
                measured("counter", [0, 0, 0], table=counter_window),
                measured("counter", [0, 1, 0], table=counter_window),
            ],
            "detectors": [
                {"name": "plus", "positions": [[0, 0, 0]], "reading": "sum"},
                {"name": "minus", "positions": [[0, 1, 0]], "reading": "sum"},
            ],
        },
        {
            "name": "chooser",
            "families": [{"name": "sa", "quantum": 0}, *material("counter")],
            "measured": [
                measured("sa", [0, 0, 0]),
                measured(
                    "counter",
                    [0, 2, 0],
                    table={"light": {"phase_window": {"reads": "sa", "offset": 0}}, "sa": "pass"},
                ),
            ],
            "detectors": [{"name": "reading", "positions": [[0, 2, 0]], "reading": "sum"}],
        },
    ]
    return {"format": FORMAT, "entities": entities}


def write() -> None:
    for name, document in (("families.json", families()), ("apparatus.json", apparatus())):
        (HERE / name).write_text(json.dumps(document, indent=1) + "\n", encoding="utf-8")


if __name__ == "__main__":
    write()
