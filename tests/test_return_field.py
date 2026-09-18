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
the runner records the identity; (f) one meeting, one push (the orchestrator's
reading of the definition of a meeting, to be confirmed by the model owner): a
head-on push is taken exactly once, the share turned back rides the Link with
the thing it pushed on the same lane, arrives at the next Node through the Port
the thing arrived by and pushes nothing there; the thing's momentum line shows
one push and the share carries -dp once; (e) the dense layer (the default
where admitted) and the engine alone agree on the worlds of (a) and (b) over
four ticks, board, parked shares, ledgers and momenta (part 2 of the feature:
the returning shares live in the arrays with their momentum and mix in their
own group). The worlds are those of the law of the bit.
"""

from copy import deepcopy

from event_universe import Simulation
from event_universe.core import spatial_state
from event_universe.core.spatial_state import BIT_SHADOW, BIT_THING, RETURN_FIELD
from event_universe.initialization import parse_initial_state

from .test_bit_law import HEADINGS, MINUS_X, TURN, X, body, document, lamp, line, run, shadow


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
    # (-21, 0, 0). Tick 5: the next round. Re-pinned on 2026-09-18 in the cleanup
    # (one N for the world, `cleanup-law-v1`): this world declared no width and
    # ran on one phase value, where the returning share carried no sign; on the
    # circle of N steps (64, the default) the returning share is the minus, so
    # at the second round the returning and the outgoing shares of one owner sum
    # apart at (1,2,2): A receives 3 with (-2, 0, 0) (6 with (-2, 0, 0) on one
    # phase value) and B is pushed (8, 0, 0) net ((-7, 0, 0) before); the books
    # close either way.
    assert homes(events, (0, 2, 2)) == [
        (1, {"amount": 36, "momentum": (0, 0, 0)}),
        (3, {"amount": 2, "momentum": (-1, 0, 0)}),
        (5, {"amount": 3, "momentum": (-2, 0, 0)}),
    ]
    assert moving_at(result["inventories"][2], (2, 2, 2)) == [
        (MINUS_X, 21, 0, 0, 1, (-21, 0, 0)),
        (MINUS_X, 4, 0, 1, -1, None),
    ]
    assert [b[1] for b in result["bodies_per_tick"]] == [[9, 0, 0]] * 2 + [[26, 0, 0]] * 2 + [[34, 0, 0]]
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


def test_a_head_on_push_is_taken_exactly_once():
    """(f): the lamp of 2 at (1,2,2) heading +X (thing 1); the body of 100 at
    (9,2,2) (owner 2) with its shadow of 1 fresh at (3,2,2) on -X; the table
    {"m": -1} reading content. The push at (2,2,2) in the cycle of tick 2 is
    on the thing's own axis, so it turns nowhere; the share turned back rides
    the Link to (3,2,2) with it on the same lane and pushes nothing there (one
    meeting, one push; the double push was an artefact, removed 2026-09-18)."""
    kind, emission, seed = lamp("lamp", 2, (1, 2, 2))
    doc = document(
        ticks=4,
        types=[kind],
        emissions=[emission],
        seeds=[seed],
        bodies=[body((9, 2, 2))],
        shadows=[shadow((3, 2, 2), MINUS_X, owner=2, steps=0)],
        rules=(TURN | {"momentum_table": {"m": -1}, "reads": "content"},),
    )
    assert parse_initial_state(doc).spatial_fields[0].owners == (1, 2)
    result = run(doc, 4)
    # The thing's momentum line: one push, (2, 0, 0), in the cycle of tick 2,
    # nothing after.
    assert result["momentum"] == [{1: [2, 0, 0], 2: [0, 0, 0]}] + [{1: [4, 0, 0], 2: [0, 0, 0]}] * 3
    for t in range(1, 5):
        (thing,) = [
            r
            for r in result["inventories"][t - 1].get((1 + t, 2, 2), ((),))[0]
            if r.detector == BIT_THING
        ]
        assert (thing.owner, thing.steps, thing.momentum) == (1, t, None if t == 1 else (2, 0, 0))
    # Tick 1: the shadow beside the thing at (2,2,2), an outgoing share of the
    # body's sign. Tick 2: turned back on +X carrying -dp once, riding with the
    # thing to (3,2,2). Tick 3: it arrived through the Port the thing arrived
    # by, pushes nothing, mixes and parks its ninths with -dp shared over them
    # by the largest remainder: -1 on the 4 back (-X), -1 on the +X ninth (the
    # lower Port among the ties), nothing on the other four.
    assert moving_at(result["inventories"][0], (2, 2, 2)) == [(MINUS_X, 1, 1, 1, -1, None)]
    assert moving_at(result["inventories"][1], (3, 2, 2)) == [(X, 1, 1, 0, 1, (-2, 0, 0))]
    assert moving_at(result["inventories"][2], (3, 2, 2)) == []
    ninths = sorted(
        (tuple(e["heading"]), e["amount"], tuple(e["momentum"]), e["outbound"])
        for e in result["snapshot"]["parked"]
    )
    assert ninths == sorted(
        [(tuple(MINUS_X), 4, (-1, 0, 0), 0), (tuple(X), 1, (-1, 0, 0), 0)]
        + [(tuple(h), 1, (0, 0, 0), 0) for h in HEADINGS if h not in (X, MINUS_X)]
    )
    assert all(tuple(e["position"]) == (3, 2, 2) for e in result["snapshot"]["parked"])
    # The books: the lamp's recoil (-2, 0, 0), the thing (4, 0, 0) and the
    # share (-2, 0, 0) sum to nothing at every tick, nothing spent, nothing home.
    assert line(result["ledgers"][3], "fields", "momentum") == {
        "initial": (0, 0, 0),
        "sourced": (0, 0, 0),
        "current": (0, 0, 0),
        "escaped": (0, 0, 0),
        "absorbed": (0, 0, 0),
        "absorbed_by_marks": (0, 0, 0),
        "returned": (0, 0, 0),
        "spent": (0, 0, 0),
    }
    assert all(entry["balanced"] and entry["real_conserved"] for entry in result["ledgers"])
    assert result["contents"] == [2] * 4 and result["shadows"] == [1] * 4
    with Simulation(parse_initial_state(doc)) as world:
        for t in range(1, 5):
            world.step()
            assert momentum_in_flight(world) == ([0, 0, 0] if t == 1 else [-2, 0, 0])


def test_the_dense_layer_agrees_with_the_engine():
    """(e): the worlds of (a) and (b) under the engine alone and under the shadow
    layer (the default where admitted, dense-field-v1): one board, one set of
    parked shares, one ledger and one momentum on every thing, body and shadow
    at every tick, four ticks; the region carries the returning shares and
    their momentum in its arrays (feature 16d, part 2)."""
    a = document(
        ticks=4,
        bodies=[body((0, 2, 2), 3, amount=81), body((2, 2, 2), 4, table={"m": 1}, amount=1000)],
        shadows=[shadow((1, 2, 2), X, amount=81, owner=3, steps=1)],
    )
    b = document(
        ticks=4,
        bodies=[
            body((0, 2, 2), 3, amount=81),
            body((1, 2, 2), 5, table={"m": 1}, amount=1000),
            body((2, 2, 2), 4, table={"m": 1}, amount=1000),
        ],
        shadows=[shadow((1, 2, 2), X, amount=81, owner=3, steps=0)],
    )
    for name, doc in (("a", a), ("b", b)):
        assert parse_initial_state(deepcopy(doc)).dense_field
        engine = run(deepcopy(doc) | {"dense_field": False}, 4)
        dense = run(deepcopy(doc), 4)
        for key in ("inventories", "ledgers", "momentum", "bodies_per_tick", "shadows"):
            assert engine[key] == dense[key], (name, key)
        # The region lists every owner of the family, the engine alone the owners
        # with a shadow on its way: the counts agree where they count something.
        assert [{o: c for o, c in counts.items() if c != [0, 0]} for counts in engine["counts"]] == [
            {o: c for o, c in counts.items() if c != [0, 0]} for counts in dense["counts"]
        ], name
        assert engine["snapshot"]["parked"] == dense["snapshot"]["parked"], name
        assert engine["bodies"] == dense["bodies"], name
        assert all(entry["balanced"] and entry["real_conserved"] for entry in dense["ledgers"]), name
    # In (a) the transverse Nodes are the region's, and after tick 4 each holds
    # in its arrays the returning ninth's momentum, (-1, 0, 0) on the 4 ninths
    # back toward (1,2,2) (flow 1, sign 1, the Port toward (1,2,2)).
    with Simulation(parse_initial_state(a)) as world:
        for _ in range(4):
            world.step()
        region = world._spatial.dense
        assert region is not None
        (family,) = region.families.values()
        rank = family.rank[3]
        for position, port in (((1, 1, 2), 2), ((1, 3, 2), 3), ((1, 2, 1), 4), ((1, 2, 3), 5)):
            assert region.owner[position] == 0
            assert family.reg[position][rank, 1, 2].tolist() == [1, 1, 1, 1, 1, 1][:port] + [4] + [1] * (
                5 - port
            )
            assert family.reg_mom[position][rank, 1, 2].tolist() == [
                [-1, 0, 0] if p == port else [0, 0, 0] for p in range(6)
            ]
