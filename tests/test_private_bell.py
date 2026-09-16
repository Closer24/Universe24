"""Private36 terminal capture, causal detector activation and one-number ownership."""

import importlib.util
import json
import runpy
import sys
from copy import deepcopy
from dataclasses import replace
from pathlib import Path

import pytest

from event_universe.core.disturbance_state import MAX_VALUE, pack, unpack
from event_universe.core.private_register import PrivateKey, PrivateState, RegisterDatum
from event_universe.diagnostics.private_render import frame
from event_universe.integration.private_contacts import (
    DetectorDefinition,
    PairRequest,
    PrivateContacts,
    PrivatePairOwner,
    captured_result,
    prepare_capture,
)

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "private_bell_prepare", ROOT / "examples/private_bell/prepare.py"
)
PREPARE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(PREPARE)


def document():
    return json.loads((ROOT / "examples/private_bell/input.json").read_text())


def contacts(world):
    assert isinstance(world.contacts, PrivateContacts)
    return world.contacts


def owned_tokens(world):
    held = sum(bool(unit.state.codes) for node in world.nodes.values() for unit in node.units)
    return len(world.transport.inputs) + len(world.transport.channels) + held


def test_local_request_and_terminal_result_keep_the_original_token_without_output():
    state = PrivateState()
    datum = RegisterDatum(pack((17, 2)))
    request = prepare_capture(state, datum, DetectorDefinition(2, 8))
    assert request == PairRequest(17, 2, 8)
    result = captured_result(request, -1)
    assert result.output is None and unpack(result.state.codes) == (17, 2, -1)
    assert not state.codes and unpack(datum.codes) == (17, 2)
    with pytest.raises(ValueError, match="already owns"):
        prepare_capture(result.state, datum, DetectorDefinition(2, 8))


@pytest.mark.parametrize("end,setting", [(True, 0), (0, 0), (3, 0), (1, True), (1, 64), (1, -1)])
def test_detector_definition_rejects_invalid_values(end, setting):
    with pytest.raises(ValueError):
        DetectorDefinition(end, setting)


def test_completed_pair_replay_never_draws_a_second_number_or_changes_settings():
    owner = PrivatePairOwner((17,), 7)
    a = owner.answer(PairRequest(17, 1, 0))
    b = owner.answer(PairRequest(17, 2, 0))
    assert a == -b
    assert owner.registry.numbers == owner.registry.released == 1
    assert owner.registry.questions == 2 and not owner.registry.open
    before = owner.canonical_state()
    for _ in range(3):
        assert owner.answer(PairRequest(17, 1, 0)) == a
        assert owner.answer(PairRequest(17, 2, 0)) == b
    assert owner.canonical_state() == before
    with pytest.raises(ValueError, match="change"):
        owner.answer(PairRequest(17, 1, 8))
    with pytest.raises(ValueError, match="undeclared"):
        owner.answer(PairRequest(18, 1, 0))
    assert owner.canonical_state() == before


def test_direct_owner_exhaustion_preserves_quantum_counters():
    owner = PrivatePairOwner((1, 2), 7, (0,))
    owner.answer(PairRequest(1, 1, 0))
    before = owner.canonical_state()
    with pytest.raises(OverflowError, match="exhausted"):
        owner.answer(PairRequest(2, 1, 0))
    assert owner.canonical_state() == before


@pytest.mark.parametrize("first_end", [1, 2])
@pytest.mark.parametrize("strategy", ["dense", "sparse"])
def test_actual_unequal_arrival_times_keep_one_open_pair_until_the_second_capture(first_end, strategy):
    raw = document()
    raw["detectors"][first_end - 1]["node"][0] = 4 if first_end == 1 else 8
    for detector in raw["detectors"]:
        detector["setting"] = 0
    world, _ = PREPARE.prepare(raw, strategy=strategy)
    for _ in range(3):
        world.step()
    owner = contacts(world)
    assert [(record.end, record.tick) for record in owner.records] == [(first_end, 2)]
    assert owner.report()["numbers"] == owner.report()["open_pairs"] == 1
    assert owned_tokens(world) == 2 and len(world.transport.channels) == 1
    world.step()
    assert [(record.end, record.tick) for record in owner.records] == [
        (first_end, 2),
        (3 - first_end, 3),
    ]
    assert owner.records[0].outcome == -owner.records[1].outcome
    assert owner.report()["numbers"] == 1 and owner.report()["open_pairs"] == 0
    assert owned_tokens(world) == 2 and not world.transport.channels


@pytest.mark.parametrize("strategy", ["dense", "sparse"])
def test_exhausted_second_staged_pair_rolls_back_the_complete_due_cohort(strategy):
    raw = document()
    raw["pair_ids"].append(2)
    raw["number_stream"] = [0]
    for seed in deepcopy(raw["seeds"]):
        seed["node"][1] = 2
        seed["codes"][0] = pack((2,))[0]
        raw["seeds"].append(seed)
    for detector in deepcopy(raw["detectors"]):
        detector["node"][1] = 2
        raw["detectors"].append(detector)
    world, _ = PREPARE.prepare(raw, strategy=strategy)
    for _ in range(3):
        world.step()
    before, work = world.canonical_state(), world.work_report()
    with pytest.raises(OverflowError, match="exhausted"):
        world.step()
    assert world.canonical_state() == before and world.work_report() == work
    assert contacts(world).report()["numbers"] == 0 and owned_tokens(world) == 4


def test_local_control_uses_actual_private_captures_without_a_quantum_owner(monkeypatch):
    monkeypatch.setitem(sys.modules, "prepare", PREPARE)
    harness = runpy.run_path(str(ROOT / "examples/private_bell/run.py"))
    cells = []
    for left, right in ((0, 8), (0, 24), (16, 8), (16, 24)):
        raw = document()
        raw["detectors"][0]["setting"], raw["detectors"][1]["setting"] = left, right
        world, ticks = PREPARE.prepare(raw)
        owner = harness["FixedLocalContacts"](contacts(world).bindings)
        world.contacts = owner
        for _ in range(ticks):
            world.step()
        cells.append([tuple(record.outcome for record in owner.records)])
        assert [record.tick for record in owner.records] == [3, 3]
        assert owned_tokens(world) == 2 and owner.report()["oracle_calls"] == 0
        projected = frame(world, owner.bindings)
        assert not projected["transfers"]
        assert sum(row["disturbances"][0]["type"] == "retained_token" for row in projected["nodes"]) == 2
    assert harness["chsh"](cells)["S"] == "2"


@pytest.mark.parametrize("mirror", [False, True])
def test_both_arrival_orders_preserve_one_number_and_same_setting_anticorrelation(mirror):
    raw = document()
    for detector in raw["detectors"]:
        detector["setting"] = 0
        if mirror:
            detector["end"] = 3 - detector["end"]
    if mirror:
        for seed in raw["seeds"]:
            seed["codes"][1] = 8 - seed["codes"][1]
    world, ticks = PREPARE.prepare(raw)
    for _ in range(ticks):
        world.step()
    owner = contacts(world)
    assert [row.end for row in owner.records] == ([2, 1] if mirror else [1, 2])
    assert owner.records[0].outcome == -owner.records[1].outcome
    assert owner.report()["numbers"] == 1


def test_dense_and_sparse_match_every_tick_including_capture_and_quantum_state():
    dense, ticks = PREPARE.prepare(document(), strategy="dense")
    sparse, _ = PREPARE.prepare(document(), strategy="sparse")
    assert len(dense.nodes) == 117 and all(len(node.units) == 36 for node in dense.nodes.values())
    for index in range(ticks):
        assert dense.canonical_state() == sparse.canonical_state()
        assert owned_tokens(dense) == owned_tokens(sparse) == 2
        assert not contacts(dense).records
        dense.step()
        sparse.step()
        if index < 3:
            assert contacts(dense).report()["numbers"] == 0
    assert dense.canonical_state() == sparse.canonical_state()
    assert owned_tokens(dense) == owned_tokens(sparse) == 2
    assert not dense.transport.inputs and not dense.transport.channels
    records = contacts(dense).records
    assert [r.tick for r in records] == [3, 3]
    assert {r.key.node for r in records} == {(3, 1, 1), (9, 1, 1)}
    assert contacts(dense).report() == {
        "oracle_calls": 2,
        "model_oracle_operations": 2,
        "additional_model_ticks": 0,
        "numbers": 1,
        "answered_endpoints": 2,
        "completed_pairs": 1,
        "open_pairs": 0,
        "declared_pair_slots": 1,
    }
    before = contacts(dense).canonical_state()
    for _ in range(6):
        dense.step()
    assert contacts(dense).canonical_state() == before and owned_tokens(dense) == 2


@pytest.mark.parametrize("strategy", ["dense", "sparse"])
def test_invalid_second_arrival_rolls_back_first_quantum_answer_and_all_owners(strategy):
    world, _ = PREPARE.prepare(document(), strategy=strategy)
    for _ in range(3):
        world.step()
    source = next(key for key, packet in world.transport.channels.items() if packet.target.node[0] == 9)
    packet = world.transport.channels[source]
    world.transport.channels[source] = replace(packet, datum=RegisterDatum(pack((999, 2))))
    before, work = world.canonical_state(), world.work_report()
    with pytest.raises(ValueError, match="undeclared"):
        world.step()
    assert world.canonical_state() == before and world.work_report() == work
    assert contacts(world).quantum.registry.numbers == 0


def test_terminal_detector_reentry_is_not_a_second_inventory_owner():
    world, ticks = PREPARE.prepare(document())
    for _ in range(ticks):
        world.step()
    key = PrivateKey((3, 1, 1), 0, 1)
    world.transport.admit(key, RegisterDatum(pack((1, 1))))
    before = world.canonical_state()
    with pytest.raises(ValueError, match="already owns"):
        world.step()
    assert world.canonical_state() == before and contacts(world).report()["numbers"] == 1


@pytest.mark.parametrize("strategy", ["dense", "sparse"])
def test_clock_overflow_preserves_unmeasured_pair_and_inflight_tokens(strategy):
    world, _ = PREPARE.prepare(document(), strategy=strategy)
    world.tick = MAX_VALUE - 1
    world.step()
    before, work = world.canonical_state(), world.work_report()
    with pytest.raises(ValueError, match="integer bound"):
        world.step()
    assert world.canonical_state() == before and world.work_report() == work


@pytest.mark.parametrize(
    "defect", ["duplicate_end", "duplicate_detector", "small_shape", "unknown_pair", "different_source"]
)
def test_initializer_rejects_ambiguous_ownership_and_topology(defect):
    raw = deepcopy(document())
    if defect == "duplicate_end":
        raw["seeds"][1]["codes"] = raw["seeds"][0]["codes"]
    elif defect == "duplicate_detector":
        raw["detectors"].append(raw["detectors"][0])
    elif defect == "small_shape":
        raw["shape"][1] = 2
    elif defect == "unknown_pair":
        raw["seeds"][1]["codes"][0] = 99
    else:
        raw["seeds"][1]["node"][0] += 1
    with pytest.raises(ValueError):
        PREPARE.prepare(raw)
