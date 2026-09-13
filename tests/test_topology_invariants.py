"""Independent integrated conservation and causality checks for configured ports."""

from copy import deepcopy
from itertools import product

import pytest

from event_universe import Simulation
from event_universe.core.topology import neighbor_address, site_allowed
from event_universe.diagnostics.cell_contract import cell_state_violations
from event_universe.initialization import parse_initial_state

from .test_disturbance_engine import document as carrier_document
from .test_disturbance_engine import field as carrier_field
from .test_disturbance_engine import kind, resident_values
from .test_local_field_rules import ORIGIN, document, field, invariant, local, operation, seed, value
from .test_spatial_interactions import carrier, exchange


def topology(name):
    candidates = tuple(v for v in product((-1, 0, 1), repeat=3) if any(v))
    degree = {"bcc": 3, "fcc": 2}.get(name)
    offsets = [list(v) for v in candidates if degree is None or sum(abs(x) for x in v) == degree]
    result = {"model_id": "configured-ports-v1", "offsets": offsets}
    if name == "bcc":
        result.update(site_modulus=2, site_residues=[[0, 0, 0], [1, 1, 1]])
    elif name == "fcc":
        result.update(site_modulus=2, site_residues=[[0, 0, 0], [0, 1, 1], [1, 0, 1], [1, 1, 0]])
    return result


def configure(raw, name):
    raw["topology"] = topology(name)
    raw["shape"] = [8, 8, 8]
    raw["normal_budget"] = 100000
    return raw


def sum_tree(expressions):
    """Balance the syntax tree so degree 26 stays within the fixed depth limit."""
    if len(expressions) == 1:
        return expressions[0]
    midpoint = len(expressions) // 2
    return operation("add", sum_tree(expressions[:midpoint]), sum_tree(expressions[midpoint:]))


def owner_expressions(name, count):
    return [local(name)] + [{"outgoing": name, "port": port} for port in range(count)]


@pytest.mark.parametrize(("name", "expected"), [("bcc", 128), ("fcc", 256), ("cubic", 512)])
def test_json_public_api_connectivity_uses_exact_site_subset(name, expected):
    initial = parse_initial_state(configure(document([field("stock")]), name))
    reached, pending = {ORIGIN}, [ORIGIN]
    while pending:
        position = pending.pop()
        for port in range(initial.topology.degree):
            target = neighbor_address(position, port, initial.shape, initial.boundary, initial.topology)
            if target not in reached:
                reached.add(target)
                pending.append(target)
    allowed = {v for v in product(range(8), repeat=3) if site_allowed(v, initial.topology)}
    assert reached == allowed
    assert len(reached) == expected


@pytest.mark.parametrize("name", ["bcc", "fcc", "cubic"])
def test_all_ports_partition_signed_scalar_and_vector_with_exact_owner_ledger(name):
    count = len(topology(name)["offsets"])
    raw = configure(
        document(
            [field("stock", conserved=True), field("vector", 3, conserved=True)],
            [seed("stock", -2 * (count + 1)), seed("vector", [2 * (count + 1), -3 * (count + 1), 0])],
        ),
        name,
    )
    raw["link_ticks"] = 2
    raw["field_rules"] = []
    for item in raw["fields"]:
        quantity = item["name"]
        portion = operation("exact_div", local(quantity), count + 1)
        assignments = [{"field": quantity, "expression": portion}]
        assignments.extend({"field": quantity, "port": p, "expression": portion} for p in range(count))
        raw["field_rules"].append(
            {
                "name": "partition_" + quantity,
                "assignments": assignments,
                "invariants": [invariant(quantity, sum_tree(owner_expressions(quantity, count)))],
            }
        )
    events = []
    world = Simulation(parse_initial_state(raw), observer=events.append)
    expected = {"stock": (-2 * (count + 1),), "vector": (2 * (count + 1), -3 * (count + 1), 0)}
    world.step()
    assert value(world, "stock") == (-2,)
    assert value(world, "vector") == (2, -3, 0)
    assert world.totals() == expected
    assert all(
        value(world, "stock", tuple(2 + x for x in offset)) == (0,)
        for offset in raw["topology"]["offsets"]
    )
    world.step()
    for port, offset in enumerate(raw["topology"]["offsets"]):
        position = tuple(2 + x for x in offset)
        assert value(world, "stock", position) == (-2,)
        state = world.spatial_values(position)["vector"]
        assert state["value"] == (2, -3, 0)
        assert len(state["directions"]) == count
        assert state["directions"][port] == (2, -3, 0)
    assert world.totals() == expected
    assert all(v["balanced"] for v in world.spatial_accounting().values())
    assert not cell_state_violations(tuple(world._spatial.cells.values()))
    assert not cell_state_violations(tuple(world._spatial.links.values()))
    sent = [event for event in events if event["event"] == "spatial_sent"]
    assert {event["port"] for event in sent} == set(range(count))
    assert all(event["arrival_tick"] - event["tick"] == 2 for event in sent)


def field_norm_case(*, reject=False):
    raw = configure(document([field("a", 3, conserved=True)], [seed("a", [3, -4, 0])]), "cubic")
    raw["link_ticks"] = 2
    owners = owner_expressions("a", 26)
    expression = sum_tree([operation("dot", owner, owner) for owner in owners])
    assignments = [
        {"field": "a", "expression": [0, 0, 0]},
        {"field": "a", "port": 25, "expression": local("a")},
    ]
    if reject:
        # Component sums remain exact, but separate owners have norm 15 instead of 25.
        assignments[1]["expression"] = [2, -3, 0]
        assignments.append({"field": "a", "port": 24, "expression": [1, -1, 0]})
    raw["field_rules"] = [
        {
            "name": "declared_energy",
            "assignments": assignments,
            "invariants": [invariant("mode_energy", expression)],
        }
    ]
    return raw


def test_26_port_norm_guard_counts_every_outgoing_owner_and_retained_value():
    raw = field_norm_case()
    world = Simulation(parse_initial_state(raw))
    world.step()
    assert value(world, "a") == (0, 0, 0)
    assert world.totals()["a"] == (3, -4, 0)
    assert value(world, "a", (3, 3, 3)) == (0, 0, 0)
    world.step()
    assert value(world, "a", (3, 3, 3)) == (3, -4, 0)
    assert sum(x * x for x in value(world, "a", (3, 3, 3))) == 25


def test_26_port_nonlinear_energy_failure_preserves_failing_node_and_all_links():
    world = Simulation(parse_initial_state(field_norm_case(reject=True)))
    before = deepcopy(world.snapshot())
    with pytest.raises(ValueError, match="invariant"):
        world.step()
    after = world.snapshot()
    assert after["spatial_fields"] == before["spatial_fields"]
    assert after["spatial_transfers"] == before["spatial_transfers"]
    assert world.totals()["a"] == (3, -4, 0)


def pair_case(name, *, reject=False):
    raw = configure(
        carrier_document(
            [kind("first", values={"p": [3, 4, 0]}), kind("second", values={"p": [-1, 2, 0]})],
            [(ORIGIN, "first"), (ORIGIN, "second")],
            fields=[carrier_field("p", 3)],
        ),
        name,
    )
    left, right = {"field": "p"}, {"field": "p", "side": "right"}
    raw["interactions"] = [
        {
            "name": "equal_unit_mass_contact",
            "left_type": "first",
            "right_type": "second",
            "assignments": [
                {"side": "left", "field": "p", "expression": [1, 3, 0] if reject else right},
                {"side": "right", "field": "p", "expression": [1, 3, 0] if reject else left},
            ],
            "invariants": [
                invariant("total_p", operation("add", left, right)),
                invariant(
                    "twice_unit_mass_kinetic",
                    operation("add", operation("dot", left, left), operation("dot", right, right)),
                ),
            ],
        }
    ]
    return raw


@pytest.mark.parametrize("name", ["bcc", "fcc", "cubic"])
def test_colocated_momentum_exchange_conserves_independent_unit_mass_energy(name):
    world = Simulation(parse_initial_state(pair_case(name)))
    initial = resident_values(world, ORIGIN)
    for tick in range(1, 5):
        world.step()
        values = resident_values(world, ORIGIN)
        assert values == (initial[::-1] if tick % 2 else initial)
        assert tuple(sum(v["p"][i] for v in values) for i in range(3)) == (2, 6, 0)
        assert sum(x * x for v in values for x in v["p"]) == 30
        assert world.totals()["p"] == (2, 6, 0)


@pytest.mark.parametrize("name", ["bcc", "fcc", "cubic"])
def test_pair_energy_rejects_even_when_momentum_is_preserved(name):
    world = Simulation(parse_initial_state(pair_case(name, reject=True)))
    before = deepcopy(resident_values(world, ORIGIN))
    with pytest.raises(ValueError, match="invariant"):
        world.step()
    assert resident_values(world, ORIGIN) == before
    assert world.totals()["p"] == (2, 6, 0)
    assert not world.snapshot()["transfers"]


@pytest.mark.parametrize("name", ["bcc", "fcc", "cubic"])
def test_joint_carrier_field_swap_keeps_configured_sum_and_squared_norm(name):
    world = Simulation(parse_initial_state(configure(exchange(), name)))
    world.step()
    assert carrier(world) == (2,)
    assert value(world, "quantity") == (5,)
    assert carrier(world)[0] ** 2 + value(world, "quantity")[0] ** 2 == 29
    assert world.totals()["quantity"] == (7,)
    assert world.spatial_accounting()["quantity"]["balanced"]


def test_positive_dot_affinity_actual_covering_displacement_is_not_arbitrary_velocity():
    raw = carrier_document([kind("walker", mode="move", values={"inventory": 1})], [(ORIGIN, "walker")])
    configure(raw, "bcc")
    raw["disturbance_types"][0]["transport"].update(
        direction=[3, 4, 0], direction_policy="positive-dot", routing="balanced"
    )
    events = []
    world = Simulation(parse_initial_state(raw), observer=events.append)
    for _ in range(16):
        world.step()
        assert world.totals() == {"inventory": (1,)}
    sent = [event for event in events if event["event"] == "sent"]
    assert len(sent) == 16
    offsets = raw["topology"]["offsets"]
    displacement = tuple(sum(offsets[event["port"]][i] for event in sent) for i in range(3))
    assert displacement == (12, 16, 0)


def test_translated_periodic_carrier_preserves_full_route_and_fractional_credit_state():
    raw = configure(
        carrier_document(
            [kind("walker", mode="move", values={"inventory": 1})],
            [(ORIGIN, "walker")],
            travel=2,
        ),
        "bcc",
    )
    raw["disturbance_types"][0]["transport"].update(
        direction=[3, 4, 0],
        direction_policy="positive-dot",
        routing="balanced",
        rate=3,
        rate_divisor=5,
    )
    shifted = deepcopy(raw)
    shifted["seeds"][0]["position"] = [0, 0, 0]
    worlds = [Simulation(parse_initial_state(case)) for case in (raw, shifted)]

    def owner(world, shift):
        def position(value):
            return tuple((x - shift) % 8 for x in value)

        values = [
            ("resident", position(p), record)
            for p, cell in world.cells.items()
            for record in cell.records
            if record is not None
        ]
        values += [
            ("transit", position(packet.origin), packet.port, packet.arrival_tick, packet.record)
            for links in world.links.values()
            for packet in links
            if packet is not None
        ]
        assert len(values) == 1
        assert not cell_state_violations(values[0][-1])
        return values[0]

    for _ in range(80):
        for world in worlds:
            world.step()
            assert world.totals() == {"inventory": (1,)}
        assert owner(worlds[0], 0) == owner(worlds[1], 6)


@pytest.mark.parametrize("name", ["bcc", "fcc", "cubic"])
def test_delayed_joint_energy_guard_revalidates_diagonal_arrival(name):
    raw = configure(exchange(delayed=True, incoming=True), name)
    raw["normal_budget"] = 10
    offset = raw["topology"]["offsets"][-1]
    raw["spatial_seeds"][-1]["position"] = [2 - x for x in offset]
    port = len(raw["topology"]["offsets"]) - 1
    raw["field_rules"][0]["assignments"][1]["port"] = port
    raw["field_rules"][0]["invariants"][0]["expression"]["args"][1]["port"] = port
    world = Simulation(parse_initial_state(raw))
    world.step()
    pending = world.cells[ORIGIN].pending
    assert pending is not None and pending.ready_tick > 1
    assert value(world, "quantity") == (3,)
    while world.tick < pending.ready_tick - 1:
        world.step()
    with pytest.raises(ValueError, match="invariant"):
        world.step()
    assert carrier(world) == (5,)
    assert value(world, "quantity") == (3,)
    assert world.totals()["quantity"] == (8,)
    assert world.spatial_accounting()["quantity"]["reactions"] == (0,)
