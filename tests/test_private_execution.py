"""Independent causal and ownership controls for dense and sparse private units."""

import importlib.util
import json
from pathlib import Path

import pytest

from event_universe.core.disturbance_state import MAX_VALUE
from event_universe.core.private_register import PrivateKey, RegisterDatum
from event_universe.core.private_worklist import PrivateSimulation

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "private_transport_prepare", ROOT / "examples/private_transport/prepare.py"
)
assert SPEC and SPEC.loader
PREPARE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(PREPARE)


def document():
    return json.loads((ROOT / "examples/private_transport/input.json").read_text())


def world(strategy, raw=None):
    wiring, seeds, _ = PREPARE.prepare(document() if raw is None else raw)
    return PrivateSimulation(wiring, seeds, strategy=strategy)


def test_exact_four_hop_loop_and_every_tick_private_parity():
    dense, sparse = world("dense"), world("sparse")
    expected = (
        PrivateKey((0, 0, 0), 0, 2),
        PrivateKey((0, 1, 0), 3, 0),
        PrivateKey((1, 1, 0), 1, 3),
        PrivateKey((1, 0, 0), 2, 1),
    )
    assert dense.canonical_state() == sparse.canonical_state()
    for tick in range(12):
        dense.step()
        sparse.step()
        assert dense.canonical_state() == sparse.canonical_state()
        for simulation in (dense, sparse):
            assert simulation.tick == tick + 1
            assert not simulation.transport.inputs
            assert len(simulation.transport.channels) == 1
            source, packet = next(iter(simulation.transport.channels.items()))
            assert source == expected[tick % 4]
            assert packet.target == expected[(tick + 1) % 4]
            assert packet.due_tick == tick + 1
            assert packet.datum.codes == (1,)  # Present encoded numerical zero.
            sends = [event for event in simulation.events if event.kind == "send"]
            assert len(sends) == tick + 1
            assert simulation.transitions == tick + 1
    assert dense.work_report()["register_checks"] == 12 * 5184
    assert sparse.work_report()["register_checks"] == 12
    assert sparse.work_report()["arrival_handles"] == 1
    assert sparse.work_report()["arrival_epochs"] == 1


def test_empty_world_only_sparse_scheduler_has_no_work():
    raw = document()
    raw["seeds"] = []
    dense, sparse = world("dense", raw), world("sparse", raw)
    for _ in range(3):
        dense.step()
        sparse.step()
        assert dense.canonical_state() == sparse.canonical_state()
    assert dense.work_report()["register_checks"] == 3 * 5184
    assert sparse.work_report()["register_checks"] == 0
    assert not dense.events and not sparse.events


def test_wiring_bijection_inverse_and_fourth_power_on_all_registers():
    wiring, _, _ = PREPARE.prepare(document())
    assert len(wiring.nodes) == 216 and len(wiring.channels) == 5184
    inverse = {channel.target: source for source, channel in wiring.channels.items()}
    assert len(inverse) == 5184
    directions = ((1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1))
    for key in wiring.channels:
        prior_node = tuple((key.node[axis] + directions[key.from_port][axis]) % 6 for axis in range(3))
        assert inverse[key] == PrivateKey(prior_node, key.to_port, key.from_port ^ 1)
        cursor = key
        for _ in range(4):
            cursor = wiring.channels[cursor].target
        assert cursor == key


def test_capacity_rejection_preserves_existing_owner_and_tick():
    simulation = world("sparse")
    before = simulation.canonical_state()
    seed = PrivateKey((0, 0, 0), 0, 2)
    with pytest.raises(ValueError, match="capacity one"):
        simulation.transport.admit(seed, RegisterDatum((3,)))
    assert simulation.canonical_state() == before
    simulation.step()
    destination = next(iter(simulation.transport.channels.values())).target
    simulation.transport.admit(destination, RegisterDatum((5,)))
    before_collision = simulation.canonical_state()
    with pytest.raises(ValueError, match="capacity one"):
        simulation.step()
    assert simulation.canonical_state() == before_collision


@pytest.mark.parametrize("strategy", ["dense", "sparse"])
def test_clock_overflow_rejects_before_due_receipt_or_owner_mutation(strategy):
    simulation = world(strategy)
    simulation.tick = MAX_VALUE - 1
    simulation.step()
    assert simulation.tick == MAX_VALUE
    assert not simulation.transport.inputs
    packet = next(iter(simulation.transport.channels.values()))
    assert packet.due_tick == MAX_VALUE and packet.datum.codes == (1,)
    simulation.transport.admit(PrivateKey((3, 3, 3), 0, 2), RegisterDatum((3,)))
    before = simulation.canonical_state()
    with pytest.raises(ValueError, match="integer bound"):
        simulation.step()
    assert simulation.canonical_state() == before


@pytest.mark.parametrize("defect", ["duplicate", "noncausal", "diagonal", "unknown", "wait"])
def test_invalid_wiring_or_rule_rejects_before_running(defect):
    raw = document()
    if defect == "duplicate":
        raw["wiring"][1] = raw["wiring"][0]
    elif defect == "noncausal":
        raw["wiring"][0]["transit_ticks"] = 0
    elif defect == "diagonal":
        raw["wiring"][0]["offset"] = [1, 1, 0]
    elif defect == "unknown":
        raw["global_peer_snapshot"] = []
    else:
        raw["local_rule"]["wait_ticks"] = 1
    with pytest.raises(ValueError):
        PREPARE.prepare(raw)
