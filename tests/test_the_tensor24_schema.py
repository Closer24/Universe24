"""Tensor24's record schema: every field of every line a whole number of any width, a label, or a row of them."""

import dataclasses
import typing

from tensor24.record import schema


def leaves(hint):
    """The types a field's hint is built of, through rows, absences and the schema's own records."""
    if dataclasses.is_dataclass(hint):
        hints = typing.get_type_hints(hint)
        return set().union(*(leaves(hints[field.name]) for field in dataclasses.fields(hint)))
    inner = [arg for arg in typing.get_args(hint) if arg is not Ellipsis]
    return set().union(*map(leaves, inner)) if inner else {hint}


def test_every_line_holds_whole_numbers_and_labels_alone_and_a_float_is_seen():
    records = [record for record in vars(schema).values() if dataclasses.is_dataclass(record)]
    assert set().union(*map(leaves, records)) == {int, str, type(None)}
    assert float in leaves(dataclasses.make_dataclass("Broken", [("x", tuple[int, float])]))
    assert bool in leaves(dataclasses.make_dataclass("Broken", [("x", bool)]))
