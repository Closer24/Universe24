"""The start's stop rule reads the levels' values, not their identities (features/start `state_key`, `returned`, `settled`; the builder's finding of 2026-10-23 on the start that never settled under the gravity row, where the start's level arrays are of kind object, Python's integers past the width under the volume form, and an object array's tobytes() is its elements' identities): two level lists equal element for element, of kind object, give one key and the second is seen as returned, the fixed point's tie within the acts or the cycle refused by name; for the lattice's integers the key is the array's bytes, the former key bit for bit. No law in it: the one rule of a repeat as it always read, now reading values."""

import numpy as np
import pytest

from event_universe.features import start


def levels(kind: type, big: int = 10**20) -> list[np.ndarray]:
    """Two level arrays of the kind, their values made anew from text so that no two calls share an integer object (the small integers are one object each in the interpreter, and the test's point is the identities)."""
    rows = [[[big + 1, big + 3], [big - 7, big]], [[big + 11, big + 12], [big + 13, big + 14]]]
    return [np.array([[int(str(v)) for v in row] for row in level], dtype=kind) for level in rows]


def test_two_equal_object_states_give_one_key_and_the_second_is_seen_as_returned():  # type: ignore[no-untyped-def]
    a, b = levels(object), levels(object)
    assert all(x is not y for x, y in zip(a, b, strict=True)) and start.state_key(a) == start.state_key(
        b
    )
    assert b"".join(x.tobytes() for x in a) != b"".join(
        x.tobytes() for x in b
    )  # the former key, identities
    far = [x + 5 for x in a]  # the levels re-read far from the state they were read at: no tie
    seen: dict[start.StateKey, int] = {}
    assert not start.returned(a, far, seen, "the rest") and len(seen) == 1
    with pytest.raises(ValueError, match="finds no fixed point.*a cycle of length 1"):
        start.returned(b, far, seen, "the rest")
    near = [x + 1 for x in b]  # within one act: the rounding tie, returned
    assert start.returned(b, near, {start.state_key(a): 0}, "the rest")


def test_the_lattice_integers_key_is_the_former_bytes_key():  # type: ignore[no-untyped-def]
    a = levels(np.int64, 1000)
    assert start.state_key(a) == tuple(x.tobytes() for x in a)
    assert (
        start.state_key(a)
        == start.state_key(levels(np.int64, 1000))
        != start.state_key(levels(object, 1000))
    )
