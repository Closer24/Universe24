"""Independent arrival times for the canonical runnable node relay."""

from pathlib import Path

from event_universe.configuration_validation import validate_configuration
from event_universe.diagnostics.node_probe import NodeProbe
from event_universe.initialization import load_initial_state

EXAMPLE = Path(__file__).resolve().parents[1] / "examples/node-clock/three_nodes.json"


def test_three_node_example_preserves_inventory_and_requires_each_link_interval():
    report = validate_configuration(EXAMPLE.read_bytes())
    assert report.valid, report.issues
    initial = load_initial_state(EXAMPLE)
    assert initial.slots_per_node == 1
    assert initial.topology.degree == 6 and initial.ticks == 9
    positions = ((0, 0, 0), (1, 0, 0), (2, 0, 0))
    observed = []
    with NodeProbe(initial, positions) as probe:
        for tick in range(1, initial.ticks + 1):
            transition = probe.step()
            observed.extend(transition.events)
            assert probe.world.totals() == {"inventory": (7,)}
            assert [sample.clock for sample in transition.after] == [
                int(tick >= 1),
                int(tick >= 4),
                int(tick >= 7),
            ]
            assert all(sample.spatial_cycles == 0 for sample in transition.after)
            if tick < 6:
                second = probe.world.node_view((2, 0, 0)).carrier
                assert second is None or all(record is None for record in second.records)
        inputs = [event for event in observed if event.direction == "input"]
        outputs = [event for event in observed if event.direction == "output"]
        assert [(event.position, event.audit_tick) for event in inputs] == [
            ((1, 0, 0), 3),
            ((2, 0, 0), 6),
        ]
        assert [(event.position, event.audit_tick, event.arrival_tick) for event in outputs] == [
            ((0, 0, 0), 0, 3),
            ((1, 0, 0), 3, 6),
            ((2, 0, 0), 6, 9),
        ]
        assert all(event.travel_port == 0 and event.receiver_port == 1 for event in observed)
        assert all(dict(event.values) == {"inventory": (7,)} for event in observed)
        final = probe.world.node_view((3, 0, 0)).carrier
        assert final is not None
        assert [probe.world.record_values(record) for record in final.records if record is not None] == [
            {"inventory": (7,)}
        ]
