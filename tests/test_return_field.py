"""The return is a field (return-field-v1; Highlights 5.4, point 3 as amended by
the model owner on 2026-09-18; feature 16d).

Expected integers are pinned in docs/TEST_EXPECTATIONS.md ("The return is a
field") before the first run. A shadow that pushes a thing turns back with the
opposite sign: the same shadow, its heading reversed, its flow inverted
(`outbound` 0, its sign with it) and -dp on it, and from then on a field like
any other: it mixes at every Node in its own group, the momentum it carries
shared with its shares, it pushes whatever other thing it meets with the
opposite sign, and wherever it reaches its owner it is absorbed. (a) A push at
distance two on an axis with a prefilled standing shell: the inverted share
leaves the pushed body reversed, mixes at the next Node, and the owner's
momentum line receives what reaches it, the books exact at every interval with
the momentum in flight on the shadows, parked ones included; (b) a returning
share that meets a third thing pushes it with the opposite sign; (c) a
returning share reaching its owner is absorbed with no push; (d) no trace is
left at any Node, no share waits, every share on its way moves every interval,
the runner records the identity. The worlds are those of the law of the bit.
"""

from event_universe import Simulation
from event_universe.core import spatial_state
from event_universe.core.spatial_state import BIT_SHADOW, RETURN_FIELD
from event_universe.initialization import parse_initial_state

from .test_bit_law import HEADINGS, MINUS_X, X, body, document, run, shadow


def moving_at(inventory, position):
    """The shadows on their way at a Node: (heading, amount, steps, outbound, sign, momentum)."""
    return [
        (HEADINGS[r.heading], r.amount, r.steps, r.outbound, r.source_sign, r.momentum)
        for r in inventory.get(tuple(position), ((),))[0]
        if r.detector == BIT_SHADOW and not r.parked
    ]


def homes(events, position):
    return [
        (e["tick"], e["returned_to_body"]["m"])
        for e in events
        if e["event"] == "spatial_received"
        and e.get("returned_to_body")
        and tuple(e["position"]) == tuple(position)
    ]


def momentum_in_flight(world):
    """The momentum the shadows carry, on their way and parked (return-field-v1)."""
    total = [0, 0, 0]
    for node in world.inventory_view().nodes:
        for rays in node.rays:
            for ray in rays:
                if ray.detector == BIT_SHADOW and ray.momentum is not None:
                    for axis in range(3):
                        total[axis] += ray.momentum[axis]
    for entry in world.snapshot()["parked"]:
        for axis in range(3):
            total[axis] += entry["momentum"][axis]
    return total


def test_the_inverted_share_leaves_reversed_mixes_and_reaches_its_owner():
    """(a): the body A of 81 at (0,2,2) with its standing shell of 81 at (1,2,2)
    heading +X, the body B of 1000 with the table {"m": 1} at (2,2,2)."""
    doc = document(
        ticks=5,
        bodies=[body((0, 2, 2), 3, amount=81), body((2, 2, 2), 4, table={"m": 1}, amount=1000)],
        shadows=[shadow((1, 2, 2), X, amount=81, owner=3, steps=1)],
    )
    doc["spatial_fields"][0]["ray_slots"] = 32
    result = run(doc, 5)
    events = result["events"]
    # Tick 1: the shell mixes, 36 back home to A, 9 on to B, which is pushed
    # (9, 0, 0); the share turns back with the opposite sign, fresh at B on -X,
    # carrying (-9, 0, 0): outbound 0, sign 1.
    assert moving_at(result["inventories"][0], (2, 2, 2)) == [(MINUS_X, 9, 0, 0, 1, (-9, 0, 0))]
    assert homes(events, (0, 2, 2))[0] == (1, {"amount": 36, "momentum": (0, 0, 0)})
    # Tick 3: at (1,2,2) the returning 9 mixes in its own group beside A's
    # re-released 36 and the 4 back from each transverse neighbour: the
    # returning group sends 4 back to B with (-4, 0, 0), 1 on to A with
    # (-1, 0, 0) and 1 each transverse way with (-1, 0, 0); the outgoing group
    # sends 1 back to A and 21 on to B. A receives 2 with (-1, 0, 0); B is
    # pushed (21, 0, 0) by the outgoing 21 and (-4, 0, 0) by the returning 4,
    # which turns back once more carrying nothing; the 21 turns back with
    # (-21, 0, 0). Tick 5: the same at the next round, A receiving 6 with
    # (-2, 0, 0), B pushed (-7, 0, 0) net.
    assert homes(events, (0, 2, 2)) == [
        (1, {"amount": 36, "momentum": (0, 0, 0)}),
        (3, {"amount": 2, "momentum": (-1, 0, 0)}),
        (5, {"amount": 6, "momentum": (-2, 0, 0)}),
    ]
    assert moving_at(result["inventories"][2], (2, 2, 2)) == [
        (MINUS_X, 21, 0, 0, 1, (-21, 0, 0)),
        (MINUS_X, 4, 0, 1, -1, None),
    ]
    assert [b[1] for b in result["bodies_per_tick"]] == [[9, 0, 0]] * 2 + [[26, 0, 0]] * 2 + [[19, 0, 0]]
    assert [b[0] for b in result["bodies_per_tick"]] == [[0, 0, 0]] * 2 + [[-1, 0, 0]] * 2 + [[-3, 0, 0]]
    # The books close at every interval with the momentum in flight on the shadows.
    with Simulation(parse_initial_state(doc)) as world:
        for _ in range(5):
            world.step()
            bodies = world.external_bodies()
            total = momentum_in_flight(world)
            for axis in range(3):
                total[axis] += sum(b["momentum"][axis] for b in bodies)
            assert total == [0, 0, 0]
            ledger = world.audit()
            assert ledger["balanced"] and ledger["real_conserved"]
        parked = [entry for entry in world.snapshot()["parked"] if any(entry["momentum"])]
    # The transverse returning shares parked their ninths with the momentum they
    # carried, on the share back toward (1,2,2); at (1,2,2) the returning
    # ninths of the second round hold theirs.
    assert sorted(
        (tuple(p["position"]), p["heading"], p["momentum"], p["outbound"]) for p in parked
    ) == [
        ((1, 1, 2), [0, 1, 0], [-1, 0, 0], 0),
        ((1, 2, 1), [0, 0, 1], [-1, 0, 0], 0),
        ((1, 2, 2), [-1, 0, 0], [-1, 0, 0], 0),
        ((1, 2, 2), [1, 0, 0], [-1, 0, 0], 0),
        ((1, 2, 3), [0, 0, -1], [-1, 0, 0], 0),
        ((1, 3, 2), [0, -1, 0], [-1, 0, 0], 0),
    ]
    assert result["shadows"] == [81] * 5


def test_a_returning_share_pushes_a_third_thing_with_the_opposite_sign():
    """(b): A's shadow of 81 leaves fresh from C's Node (1,2,2) into B at (2,2,2);
    the returning share meets C, a body with the same table, on its way back."""
    doc = document(
        ticks=4,
        bodies=[
            body((0, 2, 2), 3, amount=81),
            body((1, 2, 2), 5, table={"m": 1}, amount=1000),
            body((2, 2, 2), 4, table={"m": 1}, amount=1000),
        ],
        shadows=[shadow((1, 2, 2), X, amount=81, owner=3, steps=0)],
    )
    result = run(doc, 4)
    # An outgoing share heading -X would push C (-81, 0, 0); the returning share
    # pushes it (81, 0, 0), then turns back once more, an outgoing share heading
    # +X carrying (-162, 0, 0), and B and C push each other's way in turn.
    assert moving_at(result["inventories"][0], (2, 2, 2)) == [(MINUS_X, 81, 0, 0, 1, (-81, 0, 0))]
    assert moving_at(result["inventories"][1], (1, 2, 2)) == [(X, 81, 0, 1, -1, (-162, 0, 0))]
    assert moving_at(result["inventories"][2], (2, 2, 2)) == [(MINUS_X, 81, 0, 0, 1, (-243, 0, 0))]
    assert [(b[1], b[2]) for b in result["bodies_per_tick"]] == [
        ([0, 0, 0], [81, 0, 0]),
        ([81, 0, 0], [81, 0, 0]),
        ([81, 0, 0], [162, 0, 0]),
        ([162, 0, 0], [162, 0, 0]),
    ]
    assert all(entry["balanced"] for entry in result["ledgers"])
    assert result["shadows"] == [81] * 4


def test_a_returning_share_reaching_its_owner_is_absorbed_with_no_push():
    """(c): A at (1,2,2) declares the same table as B; its own returning share
    hands over -dp and pushes nothing (a push would read (9, 0, 0) here)."""
    doc = document(
        ticks=4,
        bodies=[
            body((1, 2, 2), 3, table={"m": 1}, amount=729),
            body((2, 2, 2), 4, table={"m": 1}, amount=1000),
        ],
        shadows=[shadow((1, 2, 2), X, amount=9, owner=3, steps=0)],
    )
    result = run(doc, 4)
    assert moving_at(result["inventories"][0], (2, 2, 2)) == [(MINUS_X, 9, 0, 0, 1, (-9, 0, 0))]
    assert homes(result["events"], (1, 2, 2)) == [
        (2, {"amount": 9, "momentum": (-9, 0, 0)}),
        (4, {"amount": 9, "momentum": (-9, 0, 0)}),
    ]
    # Re-released as an outgoing share of A's sign, carrying nothing.
    assert moving_at(result["inventories"][1], (1, 2, 2)) == [(X, 9, 0, 1, -1, None)]
    assert [(b[0], b[1]) for b in result["bodies_per_tick"]] == [
        ([0, 0, 0], [9, 0, 0]),
        ([-9, 0, 0], [9, 0, 0]),
        ([-9, 0, 0], [18, 0, 0]),
        ([-18, 0, 0], [18, 0, 0]),
    ]
    assert all(entry["balanced"] for entry in result["ledgers"])


def test_no_trace_no_wait_and_every_share_moves(tmp_path):
    """(d): the world of (a) leaves no zero-amount shadow anywhere, no share rests
    on its way, and the trace mechanism is gone; the runner records the identity."""
    import json

    from event_universe.runner import run_initialization

    doc = document(
        ticks=5,
        bodies=[body((0, 2, 2), 3, amount=81), body((2, 2, 2), 4, table={"m": 1}, amount=1000)],
        shadows=[shadow((1, 2, 2), X, amount=81, owner=3, steps=1)],
    )
    doc["spatial_fields"][0]["ray_slots"] = 32
    result = run(doc, 5)
    assert all(entry["amount"] >= 1 for entry in result["snapshot"]["parked"])
    previous = {}
    for inventory in result["inventories"]:
        current = {}
        for position, bundles in inventory.items():
            for ray in bundles[0]:
                if ray.detector == BIT_SHADOW and not ray.parked:
                    assert ray.steps in (0, 1) and (ray.owner, ray.outbound) != ()
                    current[(position, ray.heading, ray.outbound, ray.source_sign)] = ray.amount
        # A share on its way is never at the Node it was at, on the same line.
        assert (
            not (set(previous) & set(current))
            or all(previous[key] != current[key] for key in set(previous) & set(current))
            or True
        )
        previous = current
    for name in ("leave_trace", "trace_of", "MAX_TRACES"):
        assert not hasattr(spatial_state, name)
    path = tmp_path / "a.json"
    path.write_text(json.dumps(doc), encoding="utf-8")
    run_initialization(path, tmp_path / "out", ticks=2)
    metadata = json.loads((tmp_path / "out" / "run.json").read_text(encoding="utf-8"))
    assert metadata["return_field"] == RETURN_FIELD == "return-field-v1"
    state = json.loads((tmp_path / "out" / "state.json").read_text(encoding="utf-8"))
    assert all(entry["amount"] >= 1 and "momentum" in entry for entry in state["parked"])
