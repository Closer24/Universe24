"""Local history links are immutable provenance, not extra causal dependencies."""

from dataclasses import FrozenInstanceError

import pytest

from event_universe.core.event_links import EventCursor
from event_universe.core.event_space import CausalEventSpace

A, B = (0, 0, 0), (1, 0, 0)


def test_split_join_keeps_each_predecessor_without_inventing_a_causal_edge():
    space = CausalEventSpace()
    a, b = space.bind_streams("state", (A, B))
    source = space.append(tick=0, addresses=(A, B), owner="state", kind="source", cursors=(a, b))
    left = space.append(
        tick=1, addresses=(A,), owner="state", kind="local", parents=(source.id,), cursors=(a,)
    )
    right = space.append(
        tick=1, addresses=(B,), owner="state", kind="local", parents=(source.id,), cursors=(b,)
    )
    joined = space.append(
        tick=2,
        addresses=(A, B),
        owner="state",
        kind="join",
        parents=(left.id, right.id),
        cursors=(a, b),
    )
    saved = joined.predecessors
    assert tuple((p.stream_id, p.event_id) for p in saved) == (
        (a.stream_id, left.id),
        (b.stream_id, right.id),
    )
    assert space.history(a) == (joined.id, left.id, source.id)
    assert space.history(b) == (joined.id, right.id, source.id)
    checkpoint = space.append(
        tick=3,
        addresses=(A, B),
        owner="state",
        kind="checkpoint",
        cursors=(a, b),
        advance_stream_time=False,
    )
    assert checkpoint.parents == ()
    assert space.ancestors(checkpoint.id) == (checkpoint.id,)
    assert space.history(a) == (checkpoint.id, joined.id, left.id, source.id)
    assert space.history(a, joined.id) == (joined.id, left.id, source.id)
    assert joined.predecessors is saved
    assert (a.physical_tick, b.physical_tick) == (2, 2)
    with pytest.raises(FrozenInstanceError):
        saved[0].event_id = checkpoint.id
    with pytest.raises(AttributeError):
        a.head = source.id
    with pytest.raises(ValueError, match="does not belong"):
        space.history(a, right.id)


@pytest.mark.parametrize(
    "error",
    ["foreign", "forged", "duplicate", "owner", "address", "future", "parent", "capacity", "cost"],
)
def test_failed_append_leaves_event_ledger_and_all_heads_unchanged(error):
    space = CausalEventSpace(capacity=2)
    a, b = space.bind_streams("state", (A, B))
    space.append(tick=1, addresses=(A, B), owner="state", kind="source", cursors=(a, b))
    args = dict(tick=2, addresses=(A, B), owner="state", kind="change", cursors=(a, b))
    if error == "foreign":
        args["cursors"] = CausalEventSpace().bind_streams("state", (A,))
    elif error == "forged":
        args["cursors"] = (EventCursor(a.stream_id),)
    elif error == "duplicate":
        args["cursors"] = (a, a)
    elif error == "owner":
        args["owner"] = "other"
    elif error == "address":
        args["addresses"] = (A,)
    elif error == "future":
        args["tick"] = 0
    elif error == "parent":
        args["parents"] = (100,)
    elif error == "cost":
        args["model_cost"] = -1
    else:
        space.append(tick=1, addresses=(B,), owner="other", kind="audit")
    before = space.events, space.model_cost, a.head, b.head, a.physical_tick, b.physical_tick
    with pytest.raises((ValueError, OverflowError)):
        space.append(**args)
    assert before == (space.events, space.model_cost, a.head, b.head, a.physical_tick, b.physical_tick)


def test_colocated_streams_are_distinct_and_local_storage_is_bounded():
    space = CausalEventSpace(shape=(2, 1, 1))
    cursors = space.bind_streams("state", (A,) * 30)
    assert len(space.cursors_at(A)) == 30
    assert space.cursors_at(B) == ()
    with pytest.raises(ValueError, match="local event stream capacity"):
        space.bind_streams("extra", (A,))
    assert space.cursors_at(A) == cursors
    with pytest.raises(ValueError):
        space.bind_streams("outside", ((2, 0, 0),))
    with pytest.raises(ValueError):
        space.bind_streams("state", (B,))
    assert space.stream_addresses == (A,)
    space.seal_streams()
    with pytest.raises(ValueError, match="fixed after Node assembly"):
        space.bind_streams("late", (B,))
