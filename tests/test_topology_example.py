"""Independent normalized invariants for the configured BCC vector encounter."""

from pathlib import Path

from event_universe import Simulation
from event_universe.core.disturbance_state import unpack
from event_universe.initialization import load_initial_state

EXAMPLE = Path(__file__).resolve().parents[1] / "examples/topology/bcc_vectors.json"


def mode_owners(world):
    spatial = world._spatial
    assert spatial is not None
    values = [[], []]
    for cell in spatial.cells.values():
        for index, state in enumerate(cell.states):
            values[index].extend(unpack(payload) for payload in state.populations)
    for row in spatial.links.values():
        for packet in row:
            if packet is not None:
                for index, populations in enumerate(packet.fields):
                    values[index].extend(unpack(payload) for payload in populations)
    return [[v for v in mode if any(v)] for mode in values]


def test_bcc_encounter_rotates_vectors_and_preserves_normalized_diagnostics():
    dispatches, meetings = [], []

    def observe(event):
        if event["event"] != "spatial_sent":
            return
        # Inspect dispatched ownership before the one-tick link completes.
        packet = next(
            packet
            for packet in world._spatial.links[event["position"]]
            if packet is not None and packet.port == event["port"]
        )
        modes = [
            index
            for index, populations in enumerate(packet.fields)
            if any(any(unpack(payload)) for payload in populations)
        ]
        assert modes == [packet.port] and packet.port in (0, 1)
        assert packet.arrival_tick == event["tick"] + 1
        dispatches.append(packet.port)

    world = Simulation(load_initial_state(EXAMPLE), observer=observe)
    expected = [((3, -3, 0), (0, 2, -2)), ((-3, 0, 3), (2, -2, 0)), ((0, 3, -3), (-2, 0, 2))]
    for tick in range(12):
        owners = mode_owners(world)
        assert [len(mode) for mode in owners] == [1, 1]
        norms = [sum(component * component for component in mode[0]) for mode in owners]
        assert norms == [18, 8]
        assert sum(norms) == 26
        assert tuple(norms[0] - norms[1] for _ in range(3)) == (10, 10, 10)
        assert all(sum(mode[0]) == 0 for mode in owners)
        stage = 0 if tick <= 2 or tick == 11 else 1 if tick <= 6 else 2
        assert tuple(mode[0] for mode in owners) == expected[stage]
        for position, cell in world._spatial.cells.items():
            if all(any(any(unpack(payload)) for payload in state.populations) for state in cell.states):
                meetings.append((tick, position))
        if tick < 11:
            world.step()
    assert meetings == [(2, (4, 4, 4)), (6, (0, 0, 0)), (10, (4, 4, 4))]
    assert [dispatches.count(port) for port in (0, 1)] == [11, 11]
