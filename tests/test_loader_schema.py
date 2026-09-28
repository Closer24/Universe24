"""The schema reading: core/schema.py's kinds of a value and one check that refuses by name, each folder's card carrying its schema, loader/cards.py collecting the cards, and the shipped universe file checked against them."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from event_universe.core.register import Declaration, Register, discover
from event_universe.core.schema import (
    FILE_PLACES,
    Context,
    Either,
    Flag,
    Integer,
    IntegerName,
    ListOf,
    Name,
    ObjectOf,
    OneOf,
    Schema,
    check,
    check_keys,
)
from event_universe.loader import cards, derived
from tests.worlds import SOURCED

ROOT = Path(__file__).resolve().parents[1]
UNIVERSE = ROOT / "examples" / "events" / "universe.json"
# one sourced entry (the word `sourced`, a card's key), as the retired source folder wrote it
FAMILY = "a family's entry"
CONTEXT = Context(("alpha", "beta"), {"Lambda": 7, "amplitude_bound": 1 << 20})


def refused(value, kind, message, context=CONTEXT):
    with pytest.raises(ValueError, match=message):
        check(value, kind, "the.label", context)


def test_every_kind_accepts_its_values_and_refuses_the_rest_by_name():
    """An integer with its bounds, as written or by the universe's integer's name; a flag; one of the listed values exactly (1 is not true); a family's name; an integer's name read as the integer; a list of one kind with or without a length; an object with its keys; the first of either kind; the checked value returned, a list as a tuple."""
    assert check(5, Integer(least=1, most=5), "the.label", CONTEXT) == 5
    refused(0, Integer(least=1), "the.label is 0, below its least 1")
    refused(6, Integer(least=1, most=5), "the.label is 6, above its most 5")
    refused(8, Integer(most="Lambda"), "the.label is 8, above its most 'Lambda'")
    refused(8, Integer(most="Gamma"), "bounded by 'Gamma', which names no integer of the universe")
    refused(True, Integer(), "the.label must be an integer, not True")
    refused("5", Integer(), "the.label must be an integer, not '5'")
    assert check(True, Flag(), "the.label", CONTEXT) is True
    refused(1, Flag(), "the.label must be true or false, not 1")
    assert check("q", OneOf((1, "q")), "the.label", CONTEXT) == "q"
    refused(True, OneOf((1, "q")), r"the.label must be one of \[1, 'q'\], not True")
    refused(2, OneOf((1, "q")), r"the.label must be one of \[1, 'q'\], not 2")
    assert check("beta", Name(), "the.label", CONTEXT) == "beta"
    refused(
        "gamma",
        Name(),
        r"the.label names 'gamma', no family of the universe \(the families: \['alpha', 'beta'\]\)",
    )
    assert check("Lambda", IntegerName(), "the.label", CONTEXT) == 7
    refused("Gamma", IntegerName(), "the.label names 'Gamma', no integer of the universe")
    assert check([1, 2], ListOf(Integer(), length=2), "the.label", CONTEXT) == (1, 2)
    refused([1], ListOf(Integer(), length=2), "the.label must be a list of 2, not of 1")
    refused([1, "a"], ListOf(Integer()), r"the.label\[1\] must be an integer, not 'a'")
    refused(3, ListOf(Integer()), "the.label must be a list, not 3")
    shape = ObjectOf({"of": Name(), "weight": Integer(), "cap": Integer(least=1)}, frozenset({"cap"}))
    assert check({"of": "alpha", "weight": -1}, shape, "the.label", CONTEXT) == {
        "of": "alpha",
        "weight": -1,
    }
    refused(
        {"of": "alpha", "weight": 1, "scale": 3},
        shape,
        r"the.label has unknown keys: scale \(the keys: cap, of, weight\)",
    )
    refused({"of": "alpha"}, shape, r"the.label lacks keys: weight")
    refused([], shape, r"the.label must be an object with the keys \['cap', 'of', 'weight'\]")
    either = Either((ListOf(Integer(least=1), length=2), OneOf(("body",))))
    assert check([1, 3], either, "the.label", CONTEXT) == (1, 3)
    assert check("body", either, "the.label", CONTEXT) == "body"
    refused(
        "well",
        either,
        r"the.label must be a list, not 'well'; or the.label must be one of \['body'\], not 'well'",
    )
    with pytest.raises(TypeError, match="is no kind of this module"):
        check(1, "integer", "the.label", CONTEXT)  # type: ignore[arg-type]


def test_a_schema_lives_at_the_places_of_the_files_and_gives_its_keys():
    """A schema names places of the files alone and optional keys it holds; iterated, it gives every key at every place."""
    schema = Schema(
        {
            FAMILY: ObjectOf({"pair": Integer()}, frozenset()),
            "a body": ObjectOf({"pair": Integer(), "fixed": Flag()}, frozenset({"fixed"})),
        }
    )
    assert sorted(schema) == ["fixed", "pair", "pair"] and set(schema) == {"fixed", "pair"}
    with pytest.raises(ValueError, match=r"a schema at \['the well'\]: the places of the files are"):
        Schema({"the well": ObjectOf({"depth": Integer()})})
    with pytest.raises(
        ValueError, match=r"a schema at 'a body' names optional keys it lacks: \['seed'\]"
    ):
        Schema({"a body": ObjectOf({"pair": Integer()}, frozenset({"seed"}))})
    assert Declaration("the well", "(iv)", (), ()).schema is None
    assert set(FILE_PLACES) == {"the integers", FAMILY, "a body", "the world", "the start"}


def declaration(name: str, places: dict) -> Declaration:
    return Declaration(name, "(iv)", (), (), None, "9.117", schema=Schema(places))


def test_the_cards_are_collected_by_place_and_two_folders_claiming_one_key_are_refused():
    """The owners at every place, a folder without a schema skipped; the merged kind at a place with the optional keys united; a key two folders declare at one place refused by name, the same key at two places two keys."""
    register = Register()
    register.add(declaration("the hold", {FAMILY: ObjectOf({"held": Integer()}, frozenset({"held"}))}))
    register.add(
        declaration(
            "the pair", {FAMILY: ObjectOf({"pair": Integer()}), "a body": ObjectOf({"pair": Integer()})}
        )
    )
    register.add(Declaration("the wait", "(i)", (), ()))
    owners = cards.owners(register)
    assert owners[FAMILY] == {"held": "the hold", "pair": "the pair"}
    assert owners["a body"] == {"pair": "the pair"} and owners["the world"] == {}
    merged = cards.at(register, FAMILY)
    assert merged == ObjectOf({"held": Integer(), "pair": Integer()}, frozenset({"held"}))
    assert cards.at(register, "the start") == ObjectOf({}, frozenset())
    with pytest.raises(ValueError, match="no place 'the well' in the files"):
        cards.at(register, "the well")
    register.add(declaration("the source", {FAMILY: ObjectOf({"held": Integer()})}))
    with pytest.raises(
        ValueError,
        match="the key 'held' at a family's entry is declared by both 'the hold' and 'the source'",
    ):
        cards.owners(register)


def shipped_entries() -> list[dict]:
    universe = json.loads(UNIVERSE.read_text(encoding="utf-8"))
    return universe["families"] + [dict(SOURCED)]


def context_of(entries: list[dict]) -> Context:
    universe = json.loads(UNIVERSE.read_text(encoding="utf-8"))
    integers = {key: value for key, value in universe["integers"].items() if type(value) is int}
    return Context(tuple(entry["name"] for entry in entries), integers)


def test_the_shipped_universe_and_a_sourced_entry_pass_the_folders_schemas():
    """Every key of every shipped family entry beyond the frame's own (name, clock, spins_step) is one folder's, the folder named by its card; every entry passes the merged check with the integer's name read as the integer; an unknown attribute is refused by name."""
    register = discover()
    owners = cards.owners(register)[FAMILY]
    entries = shipped_entries()
    frame_keys = {"name", "quantum", "clock", "spins_step"}  # loader/frame.py, entry_kind
    words = {key for entry in entries for key in entry} - frame_keys
    assert words <= set(owners), sorted(words - set(owners))
    assert owners["sourced"] == "the source" and owners["reads"] == "the signed read"
    merged = cards.at(register, FAMILY)
    context = context_of(entries)
    for entry in entries:  # THE FAMILIES FROM THE RULE: the rows filled by the rule pass the cards
        body = {k: v for k, v in derived.filled(entry, entries).items() if k not in frame_keys}
        checked = check_keys(body, merged.keys, merged.optional, entry["name"], context)
        for read in checked["reads"]:
            assert type(read["weight"]) is int and read["weight"] >= 1
    with pytest.raises(ValueError, match=r"matter has unknown keys: nonsense_attribute"):
        check_keys(
            {k: v for k, v in derived.filled(entries[2], entries).items() if k not in frame_keys}
            | {"nonsense_attribute": 1},
            merged.keys,
            merged.optional,
            "matter",
            context,
        )
