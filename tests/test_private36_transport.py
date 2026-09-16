"""Cubic private transport, terminal ownership and atomic scheduler contracts."""

from dataclasses import dataclass, field, replace

import pytest

from event_universe.core.disturbance_state import MAX_VALUE
from event_universe.core.private_reference import DenseSelector
from event_universe.core.private_register import (
    CUBIC_PORT_PAIRS,
    PrivateKey,
    PrivateResult,
    PrivateState,
    RegisterDatum,
)
from event_universe.core.private_transport import CausalTransport, PeriodicWiring, RouteTemplate
from event_universe.core.private_worklist import PrivateSimulation, SparseSelector

DIRECTIONS = ((1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1))


def cubic_templates():
    templates = []
    for source, output in CUBIC_PORT_PAIRS:
        target_output = source
        if source == output ^ 1:
            target_output = output
        elif source == output:
            target_output = output ^ 1
        templates.append(
            RouteTemplate((source, output), DIRECTIONS[output], (output ^ 1, target_output))
        )
    return tuple(templates)


def wiring():
    return PeriodicWiring((3, 3, 3), cubic_templates(), pairs=CUBIC_PORT_PAIRS)


def snapshot(simulation):
    return (
        simulation.canonical_state(),
        simulation.work_report(),
        tuple((tick, frozenset(keys)) for tick, keys in sorted(simulation.transport._due.items())),
    )


def test_all_cubic_routes_have_six_neighbors_and_explicit_straight_and_return_paths():
    links = wiring()
    assert len(links.channels) == 27 * 36
    assert {channel.target for channel in links.channels.values()} == set(links.channels)
    for node in links.nodes:
        neighbors = {channel.target.node for key, channel in links.channels.items() if key.node == node}
        assert len(neighbors) == 6 and node not in neighbors
        for output, direction in enumerate(DIRECTIONS):
            neighbor = tuple((node[axis] + direction[axis]) % 3 for axis in range(3))
            straight = PrivateKey(node, output ^ 1, output)
            returned = PrivateKey(node, output, output)
            assert links.channels[straight].target == PrivateKey(neighbor, output ^ 1, output)
            assert links.channels[returned].target == PrivateKey(neighbor, output ^ 1, output ^ 1)
            assert links.channels[links.channels[returned].target].target == returned


@pytest.mark.parametrize("defect", ["offset", "entrance", "missing", "outside_profile"])
def test_invalid_explicit_cubic_wiring_rejects_before_execution(defect):
    templates = list(cubic_templates())
    pairs = CUBIC_PORT_PAIRS
    if defect == "offset":
        templates[0] = replace(templates[0], offset=(0, 1, 0))
    elif defect == "entrance":
        templates[0] = replace(templates[0], target=(0, 0))
    elif defect == "missing":
        templates.pop()
    else:
        templates = [RouteTemplate((0, 2), (0, 1, 0), (3, 0))]
        pairs = ((0, 2),)
    with pytest.raises(ValueError):
        PeriodicWiring((3, 3, 3), tuple(templates), pairs=pairs)


def test_all_thirty_six_simultaneous_inputs_preserve_objects_and_dense_sparse_parity():
    links = wiring()
    seeds = tuple(
        (PrivateKey((1, 1, 1), *pair), RegisterDatum((index + 1,)))
        for index, pair in enumerate(CUBIC_PORT_PAIRS)
    )
    dense = PrivateSimulation(links, seeds, strategy="dense")
    sparse = PrivateSimulation(links, seeds)
    owners = {id(datum) for _, datum in seeds}
    for _ in range(5):
        dense.step()
        sparse.step()
        assert dense.canonical_state() == sparse.canonical_state()
        assert len(sparse.transport.channels) == 36
        assert {id(packet.datum) for packet in sparse.transport.channels.values()} == owners
        assert not sparse.transport.inputs
    assert sparse.work_report()["register_checks"] == 5 * 36
    assert dense.work_report()["register_checks"] == 5 * 27 * 36


@dataclass
class PreparedCapture:
    owner: object
    results: dict = field(default_factory=dict)

    def commit(self):
        self.owner.commits += 1


class TerminalContacts:
    """Configured capture test double; no quantum probability law is implemented."""

    def __init__(self, targets, defect=None):
        self.targets = frozenset(targets)
        self.defect = defect
        self.commits = 0

    def prepare(self, tick, inputs):
        results = {}
        for item in inputs:
            if item.key not in self.targets:
                continue
            state = PrivateState((*item.datum.codes, 3))
            results[item.key] = PrivateResult(state, None)
            if self.defect == "copied_output":
                results[item.key] = PrivateResult(item.state, RegisterDatum(item.datum.codes))
            elif self.defect == "lost_input":
                results[item.key] = PrivateResult(PrivateState((1,)), None)
            elif self.defect == "foreign":
                results[PrivateKey((2, 2, 2), 5, 5)] = results[item.key]
            elif self.defect == "mutable":
                results[item.key] = {"state": state, "output": None}
            elif self.defect == "prepare_failure":
                raise ValueError("contact preparation failed")
        return PreparedCapture(self, results)

    def canonical_state(self):
        return (self.commits,)


def capture_world(strategy="sparse", defect=None):
    links = wiring()
    seeds = (
        (PrivateKey((1, 1, 1), 1, 0), RegisterDatum((3, 3))),
        (PrivateKey((1, 1, 1), 0, 1), RegisterDatum((3, 5))),
    )
    targets = tuple(links.channels[key].target for key, _ in seeds)
    contacts = TerminalContacts(targets, defect)
    return PrivateSimulation(links, seeds, strategy=strategy, contacts=contacts), targets


def test_contacts_are_due_only_and_terminal_retention_has_one_physical_owner():
    dense, targets = capture_world("dense")
    sparse, _ = capture_world()
    for step in range(4):
        dense.step()
        sparse.step()
        assert dense.canonical_state() == sparse.canonical_state()
        captures = [event for event in sparse.events if event.kind == "capture"]
        if step == 0:
            assert not captures and len(sparse.transport.channels) == 2
        else:
            assert len(captures) == 2
            assert {event.tick for event in captures} == {1}
            assert not sparse.transport.inputs and not sparse.transport.channels
            assert {
                sparse.nodes[key.node].unit(key.from_port, key.to_port).state.codes for key in targets
            } == {(3, 3, 3), (3, 5, 3)}
    assert len([event for event in sparse.events if event.kind == "send"]) == 2
    assert sparse.transitions == 4
    before = sparse.canonical_state()
    sparse.contacts.commits += 1
    assert sparse.canonical_state() != before


@pytest.mark.parametrize("strategy", ["dense", "sparse"])
@pytest.mark.parametrize(
    "defect", ["copied_output", "lost_input", "foreign", "mutable", "prepare_failure", "occupied"]
)
def test_invalid_contact_stage_preserves_all_owners_events_and_work_counters(strategy, defect):
    simulation, targets = capture_world(strategy, defect)
    simulation.step()
    if defect == "occupied":
        simulation.nodes[targets[0].node].unit(
            targets[0].from_port, targets[0].to_port
        ).state = PrivateState((1,))
    before = snapshot(simulation)
    with pytest.raises(ValueError):
        simulation.step()
    assert snapshot(simulation) == before


@pytest.mark.parametrize("strategy", ["dense", "sparse"])
@pytest.mark.parametrize("defect", ["input_capacity", "output_capacity", "clock"])
def test_transport_preflight_failures_do_not_commit_contacts_or_scheduler_work(strategy, defect):
    simulation, targets = capture_world(strategy)
    if defect == "clock":
        simulation.tick = MAX_VALUE - 1
    simulation.step()
    if defect == "input_capacity":
        simulation.transport.admit(targets[0], RegisterDatum((5, 3)))
    elif defect == "output_capacity":
        source = next(iter(simulation.transport.channels))
        simulation.transport.admit(source, RegisterDatum((5, 3)))
        simulation.tick = 0
    before = snapshot(simulation)
    with pytest.raises(ValueError):
        simulation.step()
    assert snapshot(simulation) == before


def test_preview_and_retention_require_the_actual_input_object():
    key = PrivateKey((1, 1, 1), 1, 0)
    datum = RegisterDatum((3, 3))
    transport = CausalTransport(wiring(), ((key, datum),))
    preview = transport.preview_inputs(0)
    assert preview[key] is datum and transport.inputs[key] is datum
    with pytest.raises(ValueError, match="actual received datum owner"):
        transport.retain(key, RegisterDatum(datum.codes))
    assert transport.inputs[key] is datum
    transport.retain(key, datum)
    assert not transport.inputs and not transport.channels
    for invalid in (None, RegisterDatum((3, 3))):
        with pytest.raises(ValueError, match="actual received datum owner"):
            transport.emit(key, invalid, 0)
        with pytest.raises(ValueError, match="actual received datum owner"):
            transport.retain(key, invalid)
        assert not transport.inputs and not transport.channels and not transport._due


def test_selectors_enforce_the_configured_profile_and_rejected_dispatch_preserves_checks():
    key = PrivateKey((0, 0, 0), 0, 0)
    for selector in (DenseSelector(((0, 0, 0),)), SparseSelector()):
        with pytest.raises(ValueError, match="undeclared"):
            selector.select(frozenset((key,)))
        assert selector.checks == 0

    class InvalidSelector:
        checks = 7

        def select(self, due):
            self.checks += 100
            return ()

    simulation, _ = capture_world()
    simulation.selector = InvalidSelector()
    before = snapshot(simulation)
    with pytest.raises(ValueError, match="exactly the actual due"):
        simulation.step()
    assert snapshot(simulation) == before
