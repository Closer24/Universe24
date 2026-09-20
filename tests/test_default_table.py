"""The table generated from the keys (docs/RAY_LAW.md, section 2; the model
owner, 2026-09-19, Highlights 5.4, "I approve 1 and 3": the tables are
generated from the keys and a world declares only what differs, `kind`
derived from `quantum`): `world.default_table` gives every measured event
its table from the families' quanta, a free family (h = 0) read and a paid
one (h >= 1) measured, no window, the rule's component; a declared entry
overrides only what it names, and an entry equal to the default is accepted
and changes nothing. The expected results of docs/TEST_EXPECTATIONS.md ("The
table generated from the keys"), written down first:

(a) the default: for the families m (quantum 0) and light (quantum 3) the
    generated table is (("read", None, "vector"), ("measure", None,
    "scalar")); a measured event without `table` parses to exactly that,
    and so does one that writes the default out, as strings, as objects
    with `reads`, or as empty objects: the four `RayWorld`s are equal field
    by field;
(b) what differs is kept: a window alone ({"phase_window": 8}) keeps the
    default rule `measure` with the window 8 and the component `scalar`; a
    rule off the default (`pass`, `rerelease`, `read` on a paid family,
    `measure` on a free one) is kept with its component (`vector` on
    `read`, `scalar` otherwise); `reads` `tensor` is kept; an entry that
    names only `reads` keeps the default rule;
(c) the derived kind: quantum 0 is free, 1 and 2^30 paid
    (`FamilyDefinition.free`); the unit label is 1 for a free family and
    the quantum for a paid one; `kind` is refused naming the removal and
    MIGRATION whatever its value; a family without `quantum` is refused
    naming the key; a negative quantum is refused; a charge on a paid family
    is refused naming its quantum; a charge on a free family and a lamp on
    a paid family are accepted, and a lamp on a free family refused;
(d) the example worlds: every world of `examples/events/` (the Bell and
    coupling worlds, the four top-level worlds, the four detector worlds
    through the entity loader) parses equal, field by field, to the same
    document with the generated default written back into every measured
    event's table as explicit entries: the shipped worlds declare only what
    differs and lose nothing by it.
"""

from __future__ import annotations

import copy
import json
from pathlib import Path

import pytest

from event_universe.events.world import (
    FamilyDefinition,
    default_reads,
    default_rule,
    default_table,
    parse_ray_world,
)
from event_universe.world_loading import load_world

ROOT = Path(__file__).resolve().parents[1]
FAMILIES = [{"name": "m", "quantum": 0}, {"name": "light", "quantum": 3}]
DEFAULT = (("read", None, "vector"), ("measure", None, "scalar"))


def world(families: list[dict[str, object]], table: object = None, **keys: object) -> dict[str, object]:
    measured: dict[str, object] = {"position": [1, 1, 1], "family": "m", "amount": 4, "fixed": True}
    if table is not None:
        measured["table"] = table
    document: dict[str, object] = {
        "law": "rays",
        "model_id": "default-table-test",
        "shape": [3, 3, 3],
        "boundary": "open",
        "ticks": 1,
        "K": 1 << 20,
        "N": 64,
        "release": [0, 1],
        "suspension": 0,
        "families": families,
        "measured": [measured],
    }
    document.update(keys)
    return document


def entry(
    document: dict[str, object],
) -> tuple[tuple[str, ...], tuple[int | None, ...], tuple[str, ...]]:
    parsed = parse_ray_world(document).measured[0]
    return parsed.table, parsed.windows, parsed.reads


def test_the_default_table_is_generated_from_the_keys_and_explicit_defaults_change_nothing():
    """(a)."""
    families = tuple(FamilyDefinition(str(f["name"]), int(str(f["quantum"]))) for f in FAMILIES)
    assert default_table(families) == DEFAULT
    assert default_rule(families[0]) == "read" and default_rule(families[1]) == "measure"
    assert default_reads("read") == "vector"
    assert default_reads("measure") == default_reads("rerelease") == default_reads("pass") == "scalar"
    omitted = parse_ray_world(world(FAMILIES))
    assert omitted.measured[0].table == ("read", "measure")
    assert omitted.measured[0].windows == (None, None) and omitted.measured[0].reads == (
        "vector",
        "scalar",
    )
    for table in (
        {"m": "read", "light": "measure"},
        {"m": {"rule": "read", "reads": "vector"}, "light": {"rule": "measure", "reads": "scalar"}},
        {"m": {}, "light": {}},
        {"light": "measure"},
    ):
        assert parse_ray_world(world(FAMILIES, table)) == omitted, table


def test_what_differs_from_the_default_is_kept():
    """(b)."""
    assert entry(world(FAMILIES, {"light": {"phase_window": 8}})) == (
        ("read", "measure"),
        (None, 8),
        ("vector", "scalar"),
    )
    assert entry(world(FAMILIES, {"light": "pass", "m": "rerelease"})) == (
        ("rerelease", "pass"),
        (None, None),
        ("scalar", "scalar"),
    )
    assert entry(world(FAMILIES, {"light": "read", "m": "measure"})) == (
        ("measure", "read"),
        (None, None),
        ("scalar", "vector"),
    )
    assert entry(world(FAMILIES, {"light": {"reads": "tensor"}, "m": {"reads": "here"}})) == (
        ("read", "measure"),
        (None, None),
        ("here", "tensor"),
    )
    assert entry(
        world(FAMILIES, {"light": {"rule": "read", "phase_window": 3, "reads": "outside"}})
    ) == (
        ("read", "read"),
        (None, 3),
        ("vector", "outside"),
    )


def refused(document: dict[str, object], text: str) -> None:
    with pytest.raises(ValueError, match=text):
        parse_ray_world(document)


def test_the_kind_is_derived_from_the_quantum_and_never_declared():
    """(c)."""
    assert FamilyDefinition("m", 0).free and FamilyDefinition("m", 0).unit_label == 1
    assert not FamilyDefinition("light", 1).free and FamilyDefinition("light", 1).unit_label == 1
    paid = FamilyDefinition("light", 1 << 30)
    assert not paid.free and paid.unit_label == 1 << 30
    parsed = parse_ray_world(world(FAMILIES))
    assert [family.free for family in parsed.families] == [True, False]
    for kind in ("free", "paid", "other"):
        refused(
            world([{"name": "m", "kind": kind, "quantum": 0}]),
            "families\\[0\\] declares kind, a key removed on 2026-09-19.*docs/MIGRATION.md",
        )
    refused(world([{"name": "m"}]), "families\\[0\\] lacks keys: quantum")
    refused(world([{"name": "m", "quantum": -1}]), "families\\[0\\].quantum must be an integer from 0")
    refused(
        world([{"name": "m", "quantum": 2, "charge": 1}]),
        "a paid family \\(quantum 2\\) carries no charge \\(m\\)",
    )
    charged = parse_ray_world(world([{"name": "m", "quantum": 0, "charge": -3}]))
    assert charged.families[0].charge == (-3, 1) and not hasattr(charged.measured[0], "charge")
    halves = parse_ray_world(world([{"name": "m", "quantum": 0, "charge": [1, 2]}]))
    assert halves.families[0].charge == (1, 2)
    lamp = {"position": [1, 1, 1], "family": "m", "amount": 4, "fixed": True, "lamp": {"rate": 1}}
    lit = parse_ray_world({**world([{"name": "m", "quantum": 2}]), "measured": [lamp]})
    assert lit.measured[0].lamp is not None and not lit.families[0].free
    refused(
        {**world([{"name": "m", "quantum": 0}]), "measured": [lamp]},
        "a lamp is a measured event of a paid family",
    )


def example_worlds() -> list[Path]:
    return sorted(
        path
        for path in (ROOT / "examples" / "events").rglob("*.json")
        if json.loads(path.read_text(encoding="utf-8")).get("format") != "event-entities-v1"
    )


@pytest.mark.parametrize("path", example_worlds(), ids=lambda path: str(path.relative_to(ROOT)))
def test_the_example_worlds_declare_only_what_differs(path: Path):
    """(d)."""
    source = path.read_bytes()
    shipped = load_world(source, base_dir=path.parent)
    document = json.loads(source)
    rules = {
        str(family["name"]): default_rule(FamilyDefinition(str(family["name"]), int(family["quantum"])))
        for family in document["families"]
    }
    explicit = copy.deepcopy(document)
    for measured in explicit.get("measured", []):
        table = dict(measured.get("table", {}))
        for name, rule in rules.items():
            if name not in table:
                table[name] = {"rule": rule, "reads": default_reads(rule)}
            elif isinstance(table[name], dict) and "rule" not in table[name]:
                table[name] = {"rule": rule, **table[name]}
        measured["table"] = table
    written_back = load_world(json.dumps(explicit).encode("utf-8"), base_dir=path.parent)
    assert written_back.world == shipped.world
    for measured in document.get("measured", []):
        for name, value in measured.get("table", {}).items():
            rule = rules[name]
            if isinstance(value, dict):
                default = value.get("rule", rule) == rule and set(value) <= {"rule", "reads"}
                default = default and value.get("reads", default_reads(rule)) == default_reads(rule)
            else:
                default = value == rule
            assert not default, f"{measured['position']} writes the default entry for {name} out"
