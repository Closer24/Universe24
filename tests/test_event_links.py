"""Direct event identities and fixed local banks share one spacetime ledger."""

from concurrent.futures import ThreadPoolExecutor
from dataclasses import FrozenInstanceError
from threading import Barrier, Event

import pytest

from event_universe.core.event_links import EventCursor, EventReferences
from event_universe.core.event_space import CausalEventSpace

A, B = (0, 0, 0), (1, 0, 0)


def test_current_heads_and_immutable_events_need_no_separate_local_history():
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
    assert (a.head, b.head) == (joined.id, joined.id)
    assert joined.parents == (left.id, right.id)
    assert space.ancestors(joined.id) == (source.id, left.id, right.id, joined.id)
    assert space.event(source.id) is source
    assert space.event(left.id).parents == (source.id,)
    assert space.event(right.id).parents == (source.id,)
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
    assert (a.head, b.head) == (checkpoint.id, checkpoint.id)
    assert space.event(source.id) is source
    assert space.events == (source, left, right, joined, checkpoint)
    assert not hasattr(space, "history")
    assert not hasattr(joined, "predecessors")
    assert (a.physical_tick, b.physical_tick) == (2, 2)
    with pytest.raises(FrozenInstanceError):
        source.tick = checkpoint.tick
    with pytest.raises(AttributeError):
        a.head = source.id
    with pytest.raises(AttributeError):
        a.physical_tick = checkpoint.tick


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
    resolutions = tuple(space.resolution(event.id) for event in space.events)
    with pytest.raises((ValueError, OverflowError)):
        space.append(**args)
    assert before == (space.events, space.model_cost, a.head, b.head, a.physical_tick, b.physical_tick)
    assert tuple(space.resolution(event.id) for event in space.events) == resolutions


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


def test_origin_banks_are_shared_per_node_and_independent_of_register_count():
    space = CausalEventSpace(shape=(3, 1, 1))
    cursors = space.bind_streams("state", (A,) * 30)
    a, b = space.bind_references((A, B))
    assert space.bind_references((B, A)) == (b, a)
    assert space.references_at(A) is a
    assert space.references_at(B) is b
    assert space.references_at((2, 0, 0)) is None
    a.replace(tuple(range(6)), 10)
    assert len(a.origins) == 6
    assert space.cursors_at(A) == cursors
    assert len(cursors) == 30
    assert space.stream_addresses == (A, B)
    before = space.stream_addresses
    with pytest.raises(ValueError):
        space.bind_references(((2, 0, 0), (3, 0, 0)))
    with pytest.raises(ValueError, match="distinct reference addresses"):
        space.bind_references(((2, 0, 0), (2, 0, 0)))
    assert space.stream_addresses == before
    assert space.references_at((2, 0, 0)) is None
    space.seal_streams()
    with pytest.raises(ValueError, match="fixed after Node assembly"):
        space.bind_references(((2, 0, 0),))


def test_reference_bank_capacity_rejection_preserves_existing_banks():
    space = CausalEventSpace(capacity=1)
    (a,) = space.bind_references((A,))
    with pytest.raises(OverflowError, match="event reference capacity"):
        space.bind_references((B,))
    assert space.references_at(A) is a
    assert space.references_at(B) is None
    assert space.stream_addresses == (A,)


@pytest.mark.parametrize(
    ("origins", "event_id"),
    [
        (tuple(range(7)), 10),
        ((1, 1), 10),
        ((-1,), 10),
        ((True,), 10),
        ((1 << 30,), 10),
        ([1], 10),
        ((1,), -1),
        ((1,), True),
        ((1,), 1 << 30),
    ],
)
def test_invalid_origin_replacement_preserves_all_local_metadata(origins, event_id):
    references = EventReferences()
    references.replace((1, 2), 3)
    references.consume()
    before = references.origins, references.event_id, references.consumed_id
    with pytest.raises(ValueError):
        references.replace(origins, event_id)
    assert (references.origins, references.event_id, references.consumed_id) == before


def test_local_reference_consumption_preserves_the_next_activation():
    references = EventReferences()
    assert (references.origins, references.event_id, references.consumed_id) == ((), None, None)
    references.replace((1,), 2)
    assert references.consumed_id is None
    references.consume()
    references.replace((1, 3), 4)
    assert (references.origins, references.event_id, references.consumed_id) == ((1, 3), 4, 2)
    references.consume()
    assert references.consumed_id == 4
    references.replace((), None)
    assert (references.origins, references.event_id, references.consumed_id) == ((), None, 4)
    with pytest.raises(AttributeError):
        references.origins = (5,)
    with pytest.raises(AttributeError):
        references.event_id = 5
    with pytest.raises(AttributeError):
        references.consumed_id = 5


def test_owner_transaction_is_reentrant_and_excludes_competing_append():
    space = CausalEventSpace()
    attempted, published = Event(), Event()

    def append_competing_event():
        attempted.set()
        result = space.append(tick=0, addresses=(B,), owner="other", kind="record")
        published.set()
        return result

    with ThreadPoolExecutor(max_workers=1) as pool:
        with space.transaction():
            future = pool.submit(append_competing_event)
            assert attempted.wait(5)
            assert not published.wait(0.05)
            first = space.append(tick=0, addresses=(A,), owner="state", kind="source")
            with space.transaction():
                second = space.append(
                    tick=0, addresses=(A,), owner="state", kind="record", parents=(first.id,)
                )
            assert space.events == (first, second)
        competing = future.result(timeout=5)
    assert space.events == (first, second, competing)
    assert tuple(event.id for event in space.events) == (0, 1, 2)


def test_failed_append_releases_transaction_for_another_writer():
    space = CausalEventSpace()
    with pytest.raises(ValueError):
        space.append(tick=-1, addresses=(A,), owner="state", kind="source")
    with ThreadPoolExecutor(max_workers=1) as pool:
        event = pool.submit(
            space.append, tick=0, addresses=(A,), owner="state", kind="source", model_cost=1
        ).result(timeout=5)
    assert (event.id, space.model_cost) == (0, 1)


def test_resolution_updates_six_statuses_without_rewriting_past_or_local_banks():
    space = CausalEventSpace()
    a, b = space.bind_references((A, B))
    sources = tuple(space.append(tick=0, addresses=(A,), owner="state", kind="source") for _ in range(6))
    origins = tuple(source.id for source in sources)
    for references in (a, b):
        references.replace(origins, sources[-1].id)
    decision = space.append(tick=1, addresses=(B,), owner="state", kind="record", parents=origins)
    before = space.events, space.model_cost
    assert all(space.resolution(origin) is None for origin in origins)
    space.resolve(origins, decision.id)
    assert tuple(space.resolution(origin) for origin in origins) == (decision.id,) * 6
    assert space.resolution(decision.id) is None
    assert (space.events, space.model_cost) == before
    assert all(space.event(source.id) is source for source in sources)
    assert a.origins is origins and b.origins is origins
    assert (a.event_id, b.event_id) == (sources[-1].id,) * 2
    space.resolve(origins, decision.id)
    assert tuple(space.resolution(origin) for origin in origins) == (decision.id,) * 6


@pytest.mark.parametrize(
    "error",
    [
        "empty",
        "mutable",
        "duplicate",
        "seventh",
        "unknown_origin",
        "negative_origin",
        "boolean_origin",
        "overflow_origin",
        "unknown_decision",
        "negative_decision",
        "boolean_decision",
        "overflow_decision",
        "owner",
        "time",
        "self",
        "later_identity",
        "resolved",
    ],
)
def test_invalid_resolution_leaves_every_origin_unchanged(error):
    space = CausalEventSpace()
    first = space.append(tick=0, addresses=(A,), owner="state", kind="source")
    second = space.append(tick=0, addresses=(B,), owner="state", kind="source")
    foreign = space.append(tick=0, addresses=(B,), owner="other", kind="source")
    future = space.append(tick=2, addresses=(A,), owner="state", kind="source")
    prior = space.append(tick=1, addresses=(B,), owner="state", kind="record")
    decision = space.append(tick=1, addresses=(A,), owner="state", kind="record")
    later = space.append(tick=0, addresses=(A,), owner="state", kind="source")
    origins, event_id = (first.id, second.id), decision.id
    if error == "empty":
        origins = ()
    elif error == "mutable":
        origins = [first.id]
    elif error == "duplicate":
        origins = (first.id, first.id)
    elif error == "seventh":
        origins = tuple(event.id for event in space.events)
    elif error == "unknown_origin":
        origins = (first.id, space.next_id)
    elif error == "negative_origin":
        origins = (first.id, -1)
    elif error == "boolean_origin":
        origins = (first.id, True)
    elif error == "overflow_origin":
        origins = (first.id, 1 << 30)
    elif error == "unknown_decision":
        event_id = space.next_id
    elif error == "negative_decision":
        event_id = -1
    elif error == "boolean_decision":
        event_id = True
    elif error == "overflow_decision":
        event_id = 1 << 30
    elif error == "owner":
        origins = (first.id, foreign.id)
    elif error == "time":
        origins = (first.id, future.id)
    elif error == "self":
        origins = (first.id, decision.id)
    elif error == "later_identity":
        origins = (first.id, later.id)
    else:
        space.resolve((second.id,), prior.id)
    before = space.events, tuple(space.resolution(event.id) for event in space.events)
    with pytest.raises(ValueError):
        space.resolve(origins, event_id)
    assert (space.events, tuple(space.resolution(event.id) for event in space.events)) == before
    assert space.resolution(first.id) is None


@pytest.mark.parametrize("origin", [-1, True, 1 << 30, 1])
def test_resolution_rejects_invalid_identity(origin):
    space = CausalEventSpace()
    space.append(tick=0, addresses=(A,), owner="state", kind="source")
    with pytest.raises(ValueError):
        space.resolution(origin)


def test_competing_decisions_publish_exactly_one_resolution():
    space = CausalEventSpace()
    origin = space.append(tick=0, addresses=(A,), owner="state", kind="source")
    decisions = tuple(
        space.append(tick=1, addresses=(B,), owner="state", kind="record") for _ in range(8)
    )
    ready = Barrier(len(decisions))

    def resolve(event):
        ready.wait(timeout=5)
        try:
            space.resolve((origin.id,), event.id)
        except ValueError:
            return None
        return event.id

    with ThreadPoolExecutor(max_workers=len(decisions)) as pool:
        results = tuple(pool.map(resolve, decisions))
    winners = tuple(result for result in results if result is not None)
    assert len(winners) == 1
    assert space.resolution(origin.id) == winners[0]
    assert space.event(origin.id) is origin


def test_overlapping_origin_resolutions_do_not_partially_commit_the_loser():
    space = CausalEventSpace()
    origins = tuple(
        space.append(tick=0, addresses=(A,), owner="state", kind="source").id for _ in range(3)
    )
    decisions = tuple(
        space.append(tick=1, addresses=(B,), owner="state", kind="record").id for _ in range(2)
    )
    ready = Barrier(2)

    def resolve(index):
        ready.wait(timeout=5)
        try:
            space.resolve(origins[index : index + 2], decisions[index])
        except ValueError:
            return False
        return True

    with ThreadPoolExecutor(max_workers=2) as pool:
        left_won, right_won = tuple(pool.map(resolve, (0, 1)))
    assert left_won != right_won
    statuses = tuple(space.resolution(origin) for origin in origins)
    assert statuses == (
        (decisions[0], decisions[0], None) if left_won else (None, decisions[1], decisions[1])
    )


def test_dependency_is_not_a_physical_link_and_capacity_is_atomic():
    events = CausalEventSpace(3)
    a = events.append(tick=0, addresses=((0, 0, 0),), owner="a", kind="source")
    with pytest.raises(ValueError, match="link"):
        events.append(
            tick=0, addresses=((9, 0, 0),), owner="b", kind="receive", physical_parents=(a.id,)
        )
    assert events.next_id == 1
    b = events.append(tick=0, addresses=((9, 0, 0),), owner="b", kind="calculation", parents=(a.id,))
    events.append(tick=0, addresses=((9, 0, 0),), owner="b", kind="result", parents=(b.id,))
    with pytest.raises(OverflowError):
        events.append(tick=0, addresses=((9, 0, 0),), owner="b", kind="overflow")
    assert events.next_id == 3
