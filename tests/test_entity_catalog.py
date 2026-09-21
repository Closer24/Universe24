"""The worlds of the entity catalog (docs/ENTITY_CATALOG.md; the model
owner's decision of 2026-09-20, Highlights 5.4: every entity physics knows
as one row of the law's keys, and the external things placed on the
GameBoard "so that they can be placed and things tested"). The catalog's
worlds under `examples/events/catalog/` are placements, not experiments,
so this module pins no number of any world (the model owner's rule of
2026-09-17); it checks that each world is what the catalog says it is
(docs/TEST_EXPECTATIONS.md, "The entity catalog"):

(a) every catalog world is the one its generator writes (the shipped file
    equals `make_worlds.worlds()` document for document), parses through
    the canonical loader as a world of the law (its `law` the value
    `world.py` names, its `model_id` naming the catalog), declares
    `quantum` on every family and `reading` on every declared detector,
    and runs 20 to 50 intervals;
(b) each runs its declared intervals headless with the books balanced at
    every interval; since the directional drive of 2026-09-21 (BEAM_LAW
    note 49) `neutron_star` runs six and is refused at the seventh: its
    eight neutrons of content 2^26 take the gravity column's push of 3 x
    2^50 label units per interval (the placement's "the largest a short
    run allows" was set by the per-axis rule's bound on a component), so
    by tick 6 a neutron's |p|_1 is 5 x 2^51 on the direction (3, 2, 5),
    whose resolution T_D = 683 puts the drive's wall Q S M S_1 Q + |p|_1
    T_D beyond 2^62 - 1, the rule's bound (the FORM's "larger momenta are
    refused"; the world's re-placement at a smaller content is the
    catalog's, not this rule's); the refusal is the `OverflowError` naming
    the wall, the books balanced through tick 6;
(c) the readings the catalog names exist: every declared detector appears
    in the run's detector report with an integer `record` per family, at
    least one declared detector of a world that declares detectors wrote a
    `record` line, and every probe (a measured event whose table passes a
    family, the clock the catalog reads) ends with its clock's identity,
    age + waited = the intervals run, its owed count an integer.
"""

from __future__ import annotations

import importlib.util
import json
import re
import sys
from pathlib import Path

import pytest

from event_universe.core.game_board import PORT_HEADINGS
from event_universe.events import NatureBeamSimulation
from event_universe.events import world as schema
from event_universe.events.world import LAW_VALUE
from event_universe.world_loading import load_world

ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "examples" / "events" / "catalog"
WORLDS = ("sun_planet", "neutron_star", "lamp_mirror_screen", "clock_near_mass")
# The interval at which a world's run is refused by the drive's bound (the
# directional drive of 2026-09-21, BEAM_LAW note 49): the neutron star's
# momenta pass 2^62 / T_D at tick 7 (docstring (b)).
REFUSED_AT = {"neutron_star": 7}


def load_generator():
    path = CATALOG / "make_worlds.py"
    spec = importlib.util.spec_from_file_location("catalog_make_worlds", path)
    module = importlib.util.module_from_spec(spec)
    sys.modules["catalog_make_worlds"] = module
    spec.loader.exec_module(module)
    return module


def shipped(name: str) -> dict[str, object]:
    return json.loads((CATALOG / f"{name}.json").read_text(encoding="utf-8"))


def test_the_shipped_worlds_are_the_generators():
    """(a): the files and the generator agree, world by world."""
    generated = load_generator().worlds()
    assert set(generated) == set(WORLDS)
    for name in WORLDS:
        assert shipped(name) == generated[name], name


@pytest.mark.parametrize("name", WORLDS)
def test_every_catalog_world_declares_its_keys_and_parses(name):
    """(a)."""
    document = shipped(name)
    # The law's value as `world.py` names it (`beam` since the Beam Law
    # rename of 2026-09-20), never a literal.
    assert document["law"] == LAW_VALUE and "catalog" in document["model_id"]
    assert 20 <= document["ticks"] <= 50
    assert all("reading" in detector for detector in document.get("detectors", []))
    # Its families inline or, since 2026-09-20, from the definitions it
    # references (a climb to `entities/`, confined to `examples/events`).
    loaded = load_world((CATALOG / f"{name}.json").read_bytes(), base_dir=CATALOG, root=CATALOG.parent)
    expanded = json.loads(loaded.expanded_source)
    assert all("quantum" in family for family in expanded["families"])
    assert loaded.world.model_id == document["model_id"]
    assert len(loaded.world.measured) == len(document["measured"])


@pytest.mark.parametrize("name", WORLDS)
def test_every_catalog_world_runs_with_the_books_balanced_and_its_readings_exist(name):
    """(b) and (c)."""
    document = shipped(name)
    world = load_world(json.dumps(document).encode("utf-8"), base_dir=CATALOG, root=CATALOG.parent).world
    lines: list[dict[str, object]] = []
    simulation = NatureBeamSimulation(world, lines.append)
    ticks = int(document["ticks"])
    refused_at = REFUSED_AT.get(name)
    for tick in range(1, ticks + 1):
        if tick == refused_at:
            with pytest.raises(OverflowError, match="the drive's wall"):
                simulation.step()
            break
        simulation.step()
        assert simulation.books()["balanced"], (name, tick)
    assert simulation.tick == (ticks if refused_at is None else refused_at)
    # The declared detectors: one record per family each, exact integers.
    reports = {str(entry["name"]): entry for entry in simulation.detectors()}
    declared = [str(detector["name"]) for detector in document.get("detectors", [])]
    for detector_name in declared:
        report = reports[detector_name]
        assert report["reading"] == "wave"
        for family in world.families:
            assert isinstance(report["families"][family.name]["record"], int)
    recorded = {str(line.get("detector")) for line in lines if line["event"] == "record"}
    if declared:
        assert recorded & set(declared), (name, recorded)
    # The probes: a measured event whose table passes a family reads its
    # clock; every interval is a self-creation or a wait.
    probes = [
        entry
        for entry in simulation.measured.values()
        if "pass" in world.measured[entry.number - 1].table
    ]
    if name in ("neutron_star", "clock_near_mass"):
        assert probes, name
    for probe in probes:
        state = probe.state()
        assert state["age"] + state["waited"] == simulation.tick, (name, probe.number)
        assert isinstance(state["owed"], int) and state["owed"] >= 0


# -- the catalog against the parser and the register (2026-09-20) -----------------
#
# (d) every key the catalog names in an "Its keys today" cell is a key the
#     world parser knows (its key sets in `world.py`, the nested keys of
#     `rotate` and `gate`, the rules, the components, the readings, the
#     faces and the border), or a family or column name a registered world
#     declares (the keys of a table object are family names); (e) every
#     family a registered world declares is named in the catalog, in a row
#     or in the family-name table. The catalog cannot drift silently again.


CATALOG_DOCUMENT = ROOT / "docs" / "ENTITY_CATALOG.md"
EXAMPLES = ROOT / "examples" / "events"
KEYS_COLUMN = "Its keys today"
ROTATE_KEYS = {"setting", "bit", "turn"}
GATE_KEYS = {"kind", "hold", "parties", "control"}
VALUES = {"true", "false"}


def register_worlds() -> list[dict[str, object]]:
    """Every world under `examples/events` (a document declaring `law`, never
    `format`), as the loader expands it: its families inline or, since
    2026-09-20, from the definitions it references."""
    found = []
    for path in sorted(EXAMPLES.rglob("*.json")):
        document = json.loads(path.read_text(encoding="utf-8"))
        if isinstance(document, dict) and "format" not in document:
            loaded = load_world(path.read_bytes(), base_dir=path.parent, root=EXAMPLES)
            found.append(json.loads(loaded.expanded_source))
    return found


def register_names() -> tuple[set[str], set[str]]:
    """The family names and the column names the registered worlds declare."""
    families: set[str] = set()
    columns: set[str] = set()
    for document in register_worlds():
        for family in document["families"]:
            families.add(str(family["name"]))
            columns.update(family.get("columns", {}))
    return families, columns


def parser_keys() -> set[str]:
    """Every key and value word of the world file as `world.py` names it."""
    found = set()
    for group in (
        schema.WORLD_KEYS,
        schema.FAMILY_KEYS,
        schema.MEASURED_KEYS,
        schema.LAMP_KEYS,
        schema.TABLE_ENTRY_KEYS,
        schema.TRANSIT_KEYS,
        schema.DETECTOR_KEYS,
        schema.COLUMN_KEYS,
        schema.BECOME_KEYS,
        schema.WINDOW_READING_KEYS,
        ROTATE_KEYS,
        GATE_KEYS,
        schema.TABLES,
        schema.READS,
        schema.DETECTOR_READINGS,
        (schema.SUM_READING, schema.LIFETIME_NAME),
        schema.FACE_NAMES,
        schema.BOUNDARIES,
        schema.GATE_KINDS,
    ):
        found.update(group)
    return found


def key_cells() -> list[tuple[str, str]]:
    """The (entity, cell) pairs of every table column named `Its keys today`."""
    cells = []
    column = None
    for line in CATALOG_DOCUMENT.read_text(encoding="utf-8").splitlines():
        if not line.startswith("| "):
            column = None
            continue
        parts = [part.strip() for part in line.strip().strip("|").split(" | ")]
        if KEYS_COLUMN in parts:
            column = parts.index(KEYS_COLUMN)
            continue
        if column is None or set(parts[0]) <= {"-"}:
            continue
        if column < len(parts):
            cells.append((parts[0], parts[column]))
    return cells


def named_keys(cell: str) -> set[str]:
    """The key words a cell names: a backticked identifier, the identifier
    before a colon, and the string keys of a backticked JSON object."""
    found = set()
    for span in re.findall(r"`([^`]*)`", cell):
        if re.fullmatch(r"[a-z_][a-z0-9_:+-]*", span):
            found.add(span)
        elif re.match(r"[a-z_]+\s*:", span):
            found.add(span.split(":")[0].strip())
        found.update(re.findall(r'"([a-z_][a-z0-9_]*)"\s*:', span))
    return found


def test_the_nested_key_sets_are_the_parsers():
    """The nested keys the test spells (`rotate`, `gate`) are the parser's:
    the parser accepts exactly them and refuses one more."""
    assert schema._rotation({"rotate": {"setting": 1, "bit": 0, "turn": 0}}, "t", "rerelease", 64)
    table = ((0, 0, 0), (0, 0, 0), *PORT_HEADINGS)
    gate = {"kind": "cnot", "hold": True, "parties": 2, "control": [0, 1, 0]}
    assert schema._gate({"gate": gate}, "t", "rerelease", table)
    with pytest.raises(ValueError):
        schema._rotation({"rotate": {"setting": 1, "extra": 0}}, "t", "rerelease", 64)
    with pytest.raises(ValueError):
        schema._gate({"gate": {**gate, "extra": 0}}, "t", "rerelease", table)


def test_every_key_the_catalog_names_is_a_key_the_parser_knows():
    """(d)."""
    families, columns = register_names()
    known = parser_keys() | families | columns | VALUES
    cells = key_cells()
    assert len(cells) >= 30
    unknown = {(entity, key) for entity, cell in cells for key in named_keys(cell) if key not in known}
    assert not unknown, sorted(unknown)


def test_every_family_of_the_register_has_a_catalog_row():
    """(e)."""
    text = CATALOG_DOCUMENT.read_text(encoding="utf-8")
    families, _ = register_names()
    assert len(families) >= 20
    missing = sorted(name for name in families if f"`{name}`" not in text)
    assert not missing, missing


def test_every_shipped_definition_is_named_by_a_catalog_row():
    """(f): the rows reference the definitions of `examples/events/entities/`
    (the worlds' migration of 2026-09-20), each by its name."""
    text = CATALOG_DOCUMENT.read_text(encoding="utf-8")
    names = []
    for file in ("families.json", "apparatus.json"):
        document = json.loads((EXAMPLES / "entities" / file).read_text(encoding="utf-8"))
        names.extend(str(entity["name"]) for entity in document["entities"])
    assert len(names) >= 30
    missing = sorted(name for name in names if f"`{name}`" not in text)
    assert not missing, missing
