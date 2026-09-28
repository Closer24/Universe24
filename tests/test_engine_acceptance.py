"""The engine's acceptance tests: attributes read by kind, never by name; the adversarial universe, the cap of twenty families, the null family, an added attribute, the closed engine (no family name, universe integer, default, flag or version in the code) and the rule as one function; a support not built yet is xfail strict and loses its mark when it lands."""

from __future__ import annotations

import ast
import json
import random
import re
import string
from pathlib import Path

import numpy as np
import pytest

from event_universe.events.detector_law import DetectorLawSimulation
from event_universe.world_files import input_stamp, parse_nature_beam_world
from tests.worlds import emitter_world, family_entry

ROOT = Path(__file__).resolve().parents[1]
ENGINE = ROOT / "src" / "event_universe"
# the universe file (record 2128's word) or, until it lands, the families file it replaces
UNIVERSE = next(
    path
    for path in (
        ROOT / "examples" / "events" / "universe.json",
        ROOT / "examples" / "events" / "families.json",
    )
    if path.exists()
)
STEPS = 200


def random_names(names: list[str], seed: int) -> dict[str, str]:
    rng = random.Random(seed)
    fresh = {}
    for name in names:
        fresh[name] = "".join(rng.choice(string.ascii_lowercase) for _ in range(9))
    return fresh


def renamed(document: dict, mapping: dict[str, str]) -> dict:
    """Every family name in the document replaced: the entries' `name`, every `family` value, and the keys of a body's `held` or `stocks` (its stocks by family); no other string."""

    def walk(node: object, key: str | None) -> object:
        if isinstance(node, dict):
            out = {}
            for k, v in node.items():
                new_key = mapping.get(k, k) if key in ("held", "stocks") else k
                out[new_key] = walk(v, k)
            return out
        if isinstance(node, list):
            return [walk(item, key) for item in node]
        if isinstance(node, str) and key in ("name", "family") and node in mapping:
            return mapping[node]
        return node

    result = walk(document, None)
    assert isinstance(result, dict)
    return stamped(result)


def stepped(document: dict, steps: int) -> tuple[DetectorLawSimulation, list[dict]]:
    lines: list[dict] = []
    simulation = DetectorLawSimulation(parse_nature_beam_world(document), observer=lines.append)
    for _ in range(steps):
        simulation.step()
        assert simulation.books()["balanced"], simulation.tick
    return simulation, lines


def stamped(document: dict) -> dict:
    """The world's stamp rewritten after an edit: under `stamp` (the digest alone, ALGEBRA.md #the-primitives, the engine branch) or under `input` (the word before it)."""
    key = "stamp" if "stamp" in document else "input"
    document[key] = input_stamp(document)
    return document


def families_of(document: dict) -> list[dict]:
    """The world's inline family list: under `universe` (record 2128's word, the engine branch) or under `families` (the word before it)."""
    entries = (
        document["universe"] if isinstance(document.get("universe"), list) else document["families"]
    )
    assert isinstance(entries, list)
    return entries


def extra_family(name: str) -> dict:
    """A paid family declaring the light kind and nothing that sources it."""
    return family_entry(name, [1, 1], clock=[512, 1])


def test_a_the_adversarial_universe_runs_bit_for_bit_under_random_family_names():
    """(a) The shipped families renamed at random: the same records, remainders, held levels and lines (the lines' family words renamed), and no leak. The engine reads a family by its attributes and never by its name (records 2066, 2172 to 2174)."""
    document = emitter_world(stock=2, ticks=STEPS)
    names = [family["name"] for family in families_of(document)]
    mapping = random_names(names, seed=11)
    assert len(set(mapping.values())) == len(names) and not set(mapping.values()) & set(names)
    a, lines_a = stepped(document, STEPS)
    b, lines_b = stepped(renamed(document, mapping), STEPS)
    assert len(lines_a) > 0
    expected = [
        {**line, "family": mapping.get(line["family"], line["family"])} if "family" in line else line
        for line in lines_a
    ]
    assert expected == lines_b and set(a.records) == set(b.records)
    for identity, live in a.records.items():
        other = b.records[identity]
        assert np.array_equal(live.now, other.now) and np.array_equal(live.remainder, other.remainder)
    for source in ("content", "sign"):
        assert np.array_equal(a.level_of(source), b.level_of(source))
    assert [family.name for family in b.families] == [mapping[name] for name in names]
    assert a.leaks() == [] and b.leaks() == []


def test_b_twenty_families_run_and_the_twenty_first_is_refused_by_the_loaders_own_line():
    """(b) The universe's `most_families`: families up to it load and run; one more is refused by the loader naming it."""
    document = emitter_world(stock=1, ticks=20)
    MOST_FAMILIES = document["most_families"] = 20  # the universe's key, inline as its integers are
    base = len(families_of(document))
    families_of(document).extend(
        extra_family(f"extra{index:02d}") for index in range(MOST_FAMILIES - base)
    )
    assert len(families_of(document)) == MOST_FAMILIES
    stamped(document)
    simulation, _ = stepped(document, 20)
    assert len(simulation.families) == MOST_FAMILIES and simulation.leaks() == []
    families_of(document).append(extra_family("onetoomany"))
    stamped(document)
    with pytest.raises(ValueError, match=f"at most {MOST_FAMILIES} families"):
        parse_nature_beam_world(document)


def test_c_a_family_with_no_source_stays_exactly_zero_and_silent():
    """(c) The null family (record 2075 (3)): declared with nothing that sources it, it carries no record at any interval and the engine's leak reading stays empty."""
    document = emitter_world(stock=2, ticks=STEPS)
    families_of(document).append(extra_family("nullfamily"))
    stamped(document)
    lines: list[dict] = []
    simulation = DetectorLawSimulation(parse_nature_beam_world(document), observer=lines.append)
    null = [family.name for family in simulation.families].index("nullfamily")
    for _ in range(STEPS):
        simulation.step()
        assert simulation.leaks() == [], simulation.tick
        assert all(live.family != null for live in simulation.records.values()), simulation.tick
    assert all(line.get("family") != "nullfamily" for line in lines)


@pytest.mark.xfail(
    strict=True,
    reason="the ledger's item 'a signed read weight' (ALGEBRA.md #the-paces): the loader bounds "
    "the weight from 1; when the support lands this passes and the mark comes off",
)
def test_d_an_attribute_added_in_the_file_alone_gives_its_effect_a_hill_on_gravity():
    """(d) The added attribute: a matter family reading a held family with the weight -1 is a hill (the pace raised where the level is), declared in the file with no code touched. The check is the primitive's: the effective content under the weight -1 is the negative of the content under +1 on the same board."""
    document = emitter_world(stock=1, ticks=20)
    matter = next(family for family in families_of(document) if family["name"] == "matter")
    assert matter["reads"], "the test world's matter family reads a held family"
    hollow = json.loads(json.dumps(document))
    hill = json.loads(json.dumps(document))
    for read in next(f for f in families_of(hill) if f["name"] == "matter")["reads"]:
        read["weight"] = -int(read["weight"])
    stamped(hill)
    a = DetectorLawSimulation(parse_nature_beam_world(hollow))
    b = DetectorLawSimulation(parse_nature_beam_world(hill))
    index = [family.name for family in a.families].index("matter")
    for _ in range(5):
        a.step()
        b.step()
    assert np.array_equal(b._effective_content(index), -a._effective_content(index))


def python_files() -> list[Path]:
    return sorted(path for path in ENGINE.rglob("*.py") if "__pycache__" not in path.parts)


def constants(tree: ast.AST) -> list[tuple[int, object]]:
    """Every literal constant with its line, docstrings left out."""
    docstrings: set[int] = set()
    for node in ast.walk(tree):
        if isinstance(node, (ast.Module, ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            body = node.body
            if body and isinstance(body[0], ast.Expr) and isinstance(body[0].value, ast.Constant):
                docstrings.add(id(body[0].value))
    found = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Constant) and id(node) not in docstrings:
            found.append((node.lineno, node.value))
    return found


# green since the loader's cuts 3 and 4: the columns' 'gravity' left world.py with the ray law's parse
def test_e1_no_family_name_of_the_universe_is_a_constant_of_the_engine():
    """(e) The closed engine (records 2172 to 2174): a family's name from universe.json appears nowhere in the engine's code as a string constant (docstrings and comments aside; a name that is also an attribute key, such as `charge`, is the key's word and is left out)."""
    universe = json.loads(UNIVERSE.read_text(encoding="utf-8"))
    names = {family["name"] for family in universe["families"]}
    attribute_keys = {"charge", "clicks"}
    checked = names - attribute_keys
    assert checked
    offending = []
    for path in python_files():
        for line, value in constants(ast.parse(path.read_text(encoding="utf-8"))):
            if isinstance(value, str) and value in checked:
                offending.append(f"{path.relative_to(ROOT)}:{line} {value!r}")
    assert offending == [], offending


def test_e2_no_integer_of_the_universe_is_a_literal_of_the_engine():
    """(e) The universe's integers (the Node clock, the quantum's action where the file declares it, the twist table's unit) come from the file alone; none is a numeric literal of the engine's code."""
    universe = json.loads(UNIVERSE.read_text(encoding="utf-8"))
    integers = universe["integers"]
    values = {int(integers[key]) for key in ("node_clock", "quantum_action") if key in integers}
    twist = integers.get("twist_table", {})
    if isinstance(twist, dict) and "unit" in twist:
        values.add(int(twist["unit"]))
    offending = []
    for path in python_files():
        for line, value in constants(ast.parse(path.read_text(encoding="utf-8"))):
            if type(value) is int and value in values:
                offending.append(f"{path.relative_to(ROOT)}:{line} {value}")
    assert offending == [], offending


def world_key_defaults() -> list[str]:
    """Every `<obj>.get("<key>", <default>)` of the loader with a default that is not None: a key of the files with a default written in the code."""
    loader = ENGINE / "events" / "world.py"
    tree = ast.parse(loader.read_text(encoding="utf-8"))
    found = []
    for node in ast.walk(tree):
        if (
            isinstance(node, ast.Call)
            and isinstance(node.func, ast.Attribute)
            and node.func.attr == "get"
            and len(node.args) == 2
            and isinstance(node.args[0], ast.Constant)
            and isinstance(node.args[0].value, str)
            and not (isinstance(node.args[1], ast.Constant) and node.args[1].value is None)
        ):
            found.append(f"world.py:{node.lineno} {node.args[0].value!r}")
    return found


@pytest.mark.xfail(
    strict=True,
    reason="the ledger's item 'no flag, family name or number in the code' (records 2172 to 2174): "
    "the loader still writes defaults for keys of the files; the review after the merge",
)
def test_e3_no_key_of_the_files_has_a_default_written_in_the_engine():
    """(e) A flag or a default is a line of the files (the start file, the universe file, the world file), never of the code (record 2089, records 2172 to 2174)."""
    defaults = world_key_defaults()
    assert defaults == [], defaults


VERSION_STRING = re.compile(r"-v[0-9]+$")
FLAG_WORDS = {"flag", "flags", "version", "schema_version"}


def test_e4_no_flag_and_no_version_is_a_constant_of_the_engine():
    """(e) The engine has no flag and no version (the Boss's record 2182, the model owner: "in the code there will be no flags; they are in the run file only; there is no version in the engine"; HIGHLIGHTS 5.6): no string constant of the engine's code names a version (`<name>-v<digits>`) and none is the word of a flag or a version key."""
    offending = []
    for path in python_files():
        for line, value in constants(ast.parse(path.read_text(encoding="utf-8"))):
            if isinstance(value, str) and (VERSION_STRING.search(value) or value in FLAG_WORDS):
                offending.append(f"{path.relative_to(ROOT)}:{line} {value!r}")
    assert offending == [], offending
