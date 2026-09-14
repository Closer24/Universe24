"""Opt-in causal null notices: local factor, Link transport, delayed commit, no defaults changed."""

import json
from fractions import Fraction

import pytest

from event_universe.core.disturbance_state import OPERATIONS, CostMeter, OperationCosts
from event_universe.core.event_space import CausalEventSpace
from event_universe.core.node_services import NodeEvents
from event_universe.core.source_envelope_node import (
    NOTICE_BANK,
    OUTPUT_SLOTS,
    EnvelopePacket,
    SourceEnvelopeNode,
)
from event_universe.core.source_envelope_state import EnvelopeAmplitude, EnvelopeScale
from event_universe.diagnostics.node_contract import node_state_violations
from event_universe.fields.source_envelope import local_output, null_factor, scaled_weight
from event_universe.initialization import parse_initial_state

from .test_causal_contact_fields import (
    DETECTOR,
    MIDDLE,
    SOURCE,
    causal_configuration,
    scalar_sources,
    source_trace,
)
from .test_localized_quantum_contact import step, world_for

COSTS = OperationCosts((1,) * len(OPERATIONS))


def meter():
    return CostMeter(COSTS)


def notice_configuration(*, arm_detector=False, tickets=(0, 0, 0)):
    raw = causal_configuration()
    raw["event_program"]["null_notices"] = True
    raw["event_program"]["tickets"] = list(tickets)
    raw["ticks"] = 14
    domain = raw["event_program"]["domains"][0]
    inverse = [[5, 0, 0, 0], [0, 3, 4, 0], [0, -4, 3, 0], [0, 0, 0, 5]]
    swap = [[1, 0, 0, 0], [0, 0, 1, 0], [0, 1, 0, 0], [0, 0, 0, 1]]
    domain["phases"] = [
        [{"register_indices": [0, 1], "matrix": domain["phases"][0][0]["matrix"]}],
        [{"register_indices": [1], "matrix": [[1, 0], [0, [0, 1]]]}],
        [{"register_indices": [0, 1], "matrix": inverse}],
        [{"register_indices": [1, 2], "matrix": swap}],
        *([[]] * 12),
    ]
    if arm_detector:
        domain["capture"]["register_indices"] = [1, 2]
        raw["seeds"].append({"position": list(MIDDLE), "type": "contact_probe"})
    return raw


def test_scale_and_factor_arithmetic_are_exact_and_clip_at_one():
    assert EnvelopeScale() == EnvelopeScale(1, 1)
    with pytest.raises(ValueError):
        EnvelopeScale(3, 4)
    with pytest.raises(ValueError):
        EnvelopeScale(1, 0)
    amplitude = EnvelopeAmplitude(4, 0, 5)
    assert null_factor(amplitude, EnvelopeScale(), meter()) == (25, 9)
    assert null_factor(EnvelopeAmplitude(3, 0, 5), EnvelopeScale(25, 9), meter()) is None
    assert null_factor(EnvelopeAmplitude(1), EnvelopeScale(), meter()) is None
    assert scaled_weight(EnvelopeAmplitude(3, 0, 5), EnvelopeScale(25, 9), meter()) == (1, 1)
    assert scaled_weight(EnvelopeAmplitude(3, 0, 5), EnvelopeScale(25, 16), meter()) == (9, 16)
    assert scaled_weight(EnvelopeAmplitude(4, 0, 5), EnvelopeScale(25, 9), meter()) == (1, 1)


def test_notice_packets_require_a_factor_of_at_least_one_and_a_positive_identity():
    with pytest.raises(ValueError):
        EnvelopePacket(1, SOURCE, 0, 7, None, scale=(3, 4), notice_id=1)
    with pytest.raises(ValueError):
        EnvelopePacket(1, SOURCE, 0, 7, None, scale=(4, 3))
    with pytest.raises(ValueError):
        EnvelopePacket(1, SOURCE, 0, 7, None, notice_id=3)
    packet = EnvelopePacket(1, SOURCE, 0, 7, None, scale=(4, 3), notice_id=3)
    assert packet.is_notice and not EnvelopePacket(1, SOURCE, 0, 7, None).is_notice


def test_null_without_a_factor_keeps_the_original_local_only_behavior():
    node = SourceEnvelopeNode(SOURCE, source_id=7, amplitude=EnvelopeAmplitude(4, 0, 5))
    node.null(1, None)
    assert node.amplitude == EnvelopeAmplitude() and node.scale == EnvelopeScale()
    assert all(packet is None for packet in node.output)


def test_null_with_a_factor_scales_itself_and_sends_one_notice_per_port():
    space = CausalEventSpace(40)
    events = NodeEvents(space, None)
    node = SourceEnvelopeNode(MIDDLE, source_id=7, amplitude=EnvelopeAmplitude(4, 0, 5))
    node.null(
        1,
        None,
        null_factor=null_factor,
        neighbor_ports=(0, 1),
        send_delay=0,
        link_ticks=1,
        costs=COSTS,
        events=events,
    )
    assert node.amplitude == EnvelopeAmplitude() and node.scale == EnvelopeScale(25, 9)
    notices = [packet for packet in node.output if packet is not None]
    assert [packet.port for packet in notices] == [0, 1]
    assert all(packet.scale == (25, 9) and packet.arrival_tick == 2 for packet in notices)
    assert notices[0].notice_id == notices[1].notice_id == node.cause_id >= 0
    assert node.applied_notices[-1] == notices[0].notice_id
    assert space.events[-1].kind == "source-null-notice"
    assert len(node.output) == OUTPUT_SLOTS and node.output[12] is notices[0]


def test_vacuum_or_certain_null_sends_no_notice():
    space = CausalEventSpace(40)
    events = NodeEvents(space, None)
    vacuum = SourceEnvelopeNode(DETECTOR)
    vacuum.null(1, None, null_factor=null_factor, neighbor_ports=(1,), costs=COSTS, events=events)
    assert all(packet is None for packet in vacuum.output) and vacuum.scale == EnvelopeScale()
    empty = SourceEnvelopeNode(DETECTOR, source_id=7)
    empty.null(1, None, null_factor=null_factor, neighbor_ports=(1,), costs=COSTS, events=events)
    assert all(packet is None for packet in empty.output) and empty.scale == EnvelopeScale()
    assert not space.events


def test_received_notice_waits_the_control_delay_then_forwards_away_from_its_arrival_port():
    space = CausalEventSpace(60)
    events = NodeEvents(space, None)
    node = SourceEnvelopeNode(MIDDLE, source_id=7, amplitude=EnvelopeAmplitude(3, 0, 5))
    # Sent by the Node on the +x side through its -x Port (1); it enters here through Port 0.
    packet = EnvelopePacket(3, DETECTOR, 1, 7, None, scale=(25, 9), notice_id=11)
    node.receive(packet, 3, 1, 2, events, costs=COSTS)
    assert space.events[-1].kind == "source-notice-received"
    assert node.pending_scales[0] is not None and node.pending_scales[0].ready_tick == 5
    assert node.scale == EnvelopeScale()
    assert not node.complete(4, local_output, (), COSTS, (0, 1), 0, 1, events)
    assert node.complete(5, local_output, (), COSTS, (0, 1), 0, 1, events)
    assert node.scale == EnvelopeScale(25, 9)
    assert node.applied_notices[-1] == 11 and node.pending_scales[0] is None
    forwarded = [(slot, p) for slot, p in enumerate(node.output) if p is not None]
    assert [slot for slot, _ in forwarded] == [12 + 1]
    assert forwarded[0][1].scale == (25, 9) and forwarded[0][1].notice_id == 11
    assert space.events[-1].kind == "source-scale-committed"
    duplicate = EnvelopePacket(6, SOURCE, 0, 7, None, scale=(25, 9), notice_id=11)
    node.receive(duplicate, 6, 1, 0, events, costs=COSTS)
    assert space.events[-1].kind == "source-notice-ignored"
    assert node.scale == EnvelopeScale(25, 9) and node.pending_scales[1] is None
    assert not node_state_violations(node)


def test_applied_notice_bank_is_fixed_and_a_retired_node_ignores_notices():
    space = CausalEventSpace(80)
    events = NodeEvents(space, None)
    node = SourceEnvelopeNode(MIDDLE, source_id=7, amplitude=EnvelopeAmplitude(1, 0, 2))
    for identity in range(0, NOTICE_BANK + 1):
        node.receive(
            EnvelopePacket(identity, DETECTOR, 1, 7, None, scale=(4, 3), notice_id=identity),
            identity,
            1,
            0,
            events,
            costs=COSTS,
        )
        node.complete(identity, local_output, (), COSTS, (0,), 0, 1, events)
    assert len(node.applied_notices) == NOTICE_BANK and 0 not in node.applied_notices
    retired = SourceEnvelopeNode(MIDDLE, source_id=7, retired=7)
    retired.receive(
        EnvelopePacket(9, DETECTOR, 1, 7, None, scale=(4, 3), notice_id=99), 9, 1, 0, events, costs=COSTS
    )
    assert space.events[-1].kind == "source-notice-ignored"
    assert retired.scale == EnvelopeScale() and all(p is None for p in retired.pending_scales)


def test_option_requires_the_causal_model_and_a_boolean():
    raw = causal_configuration()
    raw["event_program"]["null_notices"] = True
    raw["event_program"]["model"] = "localized-contact-quantum-v1"
    with pytest.raises(ValueError, match="causal contact field model"):
        parse_initial_state(raw)
    raw = causal_configuration()
    raw["event_program"]["null_notices"] = 1
    with pytest.raises(ValueError, match="true or false"):
        parse_initial_state(raw)


def test_default_profile_report_and_emission_are_unchanged_without_the_option(monkeypatch):
    raw = notice_configuration(arm_detector=True)
    del raw["event_program"]["null_notices"]
    world, resolver = world_for(raw)
    trace = source_trace(world, monkeypatch)
    assert resolver.report()["null_notices"] is False
    step(world, 5)
    assert [amount for tick, amount in scalar_sources(trace, SOURCE) if tick in (2, 3, 4)] == [-9] * 3
    assert all(node.scale == EnvelopeScale() for node in resolver.source_nodes().values())
    assert all(p is None for node in resolver.source_nodes().values() for p in node.output)


def test_arm_null_restores_the_source_to_the_conditional_weight_after_one_link(monkeypatch):
    raw = notice_configuration(arm_detector=True)
    world, resolver = world_for(raw)
    trace = source_trace(world, monkeypatch)
    assert resolver.report()["null_notices"] is True
    step(world, 2)
    # Tick 1: M decided [9, 16] and drew a null; its notice reached S at tick 2.
    assert scalar_sources(trace, SOURCE) == [(1, -9)]
    nodes = resolver.source_nodes()
    assert [nodes[a].scale for a in (SOURCE, MIDDLE, DETECTOR)] == [EnvelopeScale(25, 9)] * 3
    step(world, 4)
    assert [amount for tick, amount in scalar_sources(trace, SOURCE) if tick in (2, 3, 4)] == [-25] * 3
    # The next gate acts on the scaled envelopes: 9/25 and 16/25 are the exact
    # conditional Born weights of the state after the null.
    assert scalar_sources(trace, SOURCE)[-1] == (5, -9)
    assert scalar_sources(trace, MIDDLE)[-1] == (5, -16)
    # The second null at M (tick 5) sent a second factor; the world clock is
    # now at tick 6 and both neighbors applied it at the start of that tick.
    scales = [nodes[a].scale for a in (SOURCE, MIDDLE, DETECTOR)]
    assert all(Fraction(x.numerator, x.denominator) == Fraction(625, 81) for x in scales)
    step(world, 2)
    assert scalar_sources(trace, SOURCE)[-1][1] == -25
    assert all(not node_state_violations(node) for node in resolver.source_nodes().values())
    assert all(value["balanced"] for value in world.spatial_accounting().values())


def test_output_null_notice_crosses_two_links_before_the_source_recovers(monkeypatch):
    raw = notice_configuration()
    world, resolver = world_for(raw)
    trace = source_trace(world, monkeypatch)
    step(world, 8)
    # Tick 7: D decided [337, 288] and drew a null. Its notice reaches M at 8 and S at 9.
    assert resolver.space.records[-1].decision.weights == (337, 288)
    assert resolver.source_nodes()[DETECTOR].scale == EnvelopeScale(625, 337)
    assert resolver.source_nodes()[SOURCE].scale == EnvelopeScale()
    step(world, 1)
    assert resolver.source_nodes()[MIDDLE].scale == EnvelopeScale(625, 337)
    assert scalar_sources(trace, SOURCE)[-1] == (8, -13)
    step(world, 1)
    assert resolver.source_nodes()[SOURCE].scale == EnvelopeScale(625, 337)
    assert scalar_sources(trace, SOURCE)[-1] == (9, -25)
    report = resolver.report()
    assert [tuple(e["weight_scale"]) for e in report["source_envelopes"]] == [(625, 337)] * 3


def test_headless_run_records_scales_and_keeps_balanced_accounting(tmp_path):
    initial = tmp_path / "notices.json"
    initial.write_text(json.dumps(notice_configuration(arm_detector=True)), encoding="utf-8")
    from event_universe.runner import run_initialization

    run_initialization(initial, tmp_path / "run")
    report = json.loads((tmp_path / "run/run.json").read_text(encoding="utf-8"))
    resolver = report["computation"]["resolver"]
    assert resolver["null_notices"] is True
    assert report["accounting_balanced_at_every_completed_tick"]
    assert report["final_totals"]["charge"] == [-1]
    assert all(e["weight_scale"] == [625, 81] for e in resolver["source_envelopes"])


# Crossing nulls: a null decided before an earlier-ordered notice arrives is corrected.


def test_null_correction_is_the_exact_quotient_and_telescopes():
    from event_universe.core.source_envelope_state import NullRecord
    from event_universe.fields.source_envelope import null_correction

    record = NullRecord(4, 256, 625)
    result = null_correction(record, (625, 481), meter())
    assert result is not None
    (numerator, denominator), assumed = result
    assert Fraction(numerator, denominator) == Fraction(177489, 140625) and assumed == (625, 481)
    assert Fraction(625, 481) * Fraction(625, 369) * Fraction(numerator, denominator) == Fraction(25, 9)
    # Two corrections in sequence equal one correction by the product of the factors.
    first = null_correction(record, (5, 4), meter())
    assert first is not None
    second = null_correction(NullRecord(4, 256, 625, *first[1]), (6, 5), meter())
    once = null_correction(record, (30, 20), meter())
    assert second is not None and once is not None
    assert Fraction(*first[0]) * Fraction(*second[0]) == Fraction(*once[0]) and second[1] == once[1]
    # A weight that would reach one under the delivered scale admits no correction.
    assert null_correction(NullRecord(0, 1, 2), (2, 1), meter()) is None
    with pytest.raises(ValueError, match="at least one"):
        null_correction(record, (1, 2), meter())
    with pytest.raises(ValueError, match="probability"):
        NullRecord(0, 3, 2)


def test_notice_packets_carry_an_optional_ordering_key():
    packet = EnvelopePacket(
        3, (1, 1, 1), 0, 7, None, scale=(25, 9), notice_id=4, null_tick=2, null_origin=(2, 1, 1)
    )
    assert packet.order_key == (2, (2, 1, 1))
    assert EnvelopePacket(3, (1, 1, 1), 0, 7, None, scale=(25, 9), notice_id=4).order_key is None
    with pytest.raises(ValueError, match="ordering key requires the deciding"):
        EnvelopePacket(3, (1, 1, 1), 0, 7, None, scale=(25, 9), notice_id=4, null_tick=2)
    with pytest.raises(ValueError, match="belongs to a notice"):
        EnvelopePacket(3, (1, 1, 1), 0, 7, None, null_origin=(2, 1, 1))


def crossing_configuration(offset):
    import importlib.util
    from pathlib import Path

    path = Path(__file__).resolve().parents[1] / "examples/quantum/crossing_nulls.py"
    spec = importlib.util.spec_from_file_location("crossing_nulls", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module, module.configuration(offset)


def source_scales(resolver):
    return {
        tuple(e["position"]): (Fraction(*e["weight_scale"]), e["corrections"])
        for e in resolver.report()["source_envelopes"]
    }


def test_crossing_nulls_are_corrected_to_the_conditional_scale_by_the_later_null():
    probe, raw = crossing_configuration(0)
    world, resolver = world_for(raw)
    step(world, 5)
    # Both probes decide at tick 4: M with the exact conditional weights, D given M's null.
    decisions = [
        (r.decision.tick, r.decision.register_index, tuple(r.decision.weights))
        for r in resolver.space.records
    ]
    assert decisions[:2] == [(4, 1, (481, 144)), (4, 2, (225, 256))]
    scales = source_scales(resolver)
    # M sent 625/481 from its exact scale and D sent 625/369 from the stale one; one Link
    # later M's notice reached D, and D, the later null by (tick, position), corrected itself
    # to the conditional 25/9 and queued the correction. D's stale notice reached M, and S
    # so far holds M's factor only.
    assert scales[DETECTOR] == (Fraction(25, 9), 1)
    assert scales[MIDDLE] == (Fraction(390625, 177489), 0)
    assert scales[SOURCE] == (Fraction(625, 481), 0)
    step(world, 1)
    scales = source_scales(resolver)
    assert scales[MIDDLE] == (Fraction(25, 9), 0) and scales[SOURCE] == (Fraction(390625, 177489), 0)
    step(world, 1)
    scales = source_scales(resolver)
    assert scales == {
        SOURCE: (Fraction(25, 9), 0),
        MIDDLE: (Fraction(25, 9), 0),
        DETECTOR: (Fraction(25, 9), 1),
    }
    assert resolver.report()["null_corrections"] == 1
    assert all(value["balanced"] for value in world.spatial_accounting().values())
    # The probe's own analytic targets agree.
    targets = probe.analytic()
    assert targets["exact_source_scale"] == Fraction(25, 9)
    assert targets["stale_product"] == Fraction(390625, 177489)


@pytest.mark.parametrize("offset", [1, 2])
def test_sequential_nulls_need_no_correction(offset):
    _, raw = crossing_configuration(offset)
    world, resolver = world_for(raw)
    step(world, 8)
    scales = source_scales(resolver)
    assert scales[SOURCE] == (Fraction(25, 9), 0) and resolver.report()["null_corrections"] == 0


def test_corrections_leave_through_their_own_bank_and_are_bounded():
    from event_universe.core.source_envelope_node import CORRECTION_QUEUE
    from event_universe.core.source_envelope_state import NullRecord
    from event_universe.fields.source_envelope import null_correction, squared_weight

    events = NodeEvents(CausalEventSpace(400), None)
    node = SourceEnvelopeNode((2, 1, 1), source_id=7, amplitude=EnvelopeAmplitude(4, 0, 5))
    node.null(
        4,
        None,
        null_factor=null_factor,
        neighbor_ports=(0, 1),
        costs=COSTS,
        events=events,
        null_weight=squared_weight,
    )
    assert node.null_record == NullRecord(4, 16, 25, 1, 1)
    assert node.output[12].null_tick == 4 and node.output[12].null_origin == (2, 1, 1)
    # A notice from a null ordered earlier (tick 3) arrives; the Node corrects itself.
    node.receive(
        EnvelopePacket(
            5, (1, 1, 1), 0, 7, None, scale=(5, 4), notice_id=90, null_tick=3, null_origin=(1, 1, 1)
        ),
        5,
        1,
        0,
        events,
        costs=COSTS,
    )
    node.clear_output(12, node.output[12])
    node.clear_output(13, node.output[13])
    node.complete(5, lambda *a: EnvelopeAmplitude(), (), COSTS, (0, 1), 0, 1, events, null_correction)
    expected = null_correction(NullRecord(4, 16, 25, 1, 1), (5, 4), meter())
    assert expected is not None and node.corrections == 1
    assert node.null_record is not None and (
        node.null_record.scale_numerator,
        node.null_record.scale_denominator,
    ) == (5, 4)
    sent = [node.output[18 + port] for port in (0, 1)]
    assert all(
        p is not None and (p.scale, p.null_tick, p.null_origin) == (expected[0], 4, (2, 1, 1))
        for p in sent
    )
    assert node.pending_corrections == ()
    assert not node_state_violations(node)
    # A notice ordered later than the Node's own null is applied and forwarded, never corrected.
    node.receive(
        EnvelopePacket(
            6, (3, 1, 1), 1, 7, None, scale=(7, 6), notice_id=91, null_tick=4, null_origin=(3, 1, 1)
        ),
        6,
        1,
        0,
        events,
        costs=COSTS,
    )
    for slot in (12, 13, 18, 19):
        if node.output[slot] is not None:
            node.clear_output(slot, node.output[slot])
    node.complete(6, lambda *a: EnvelopeAmplitude(), (), COSTS, (0, 1), 0, 1, events, null_correction)
    assert node.corrections == 1 and node.output[18] is None
    # Without a weight law there is no record and no correction; the queue is bounded.
    plain = SourceEnvelopeNode((2, 1, 1), source_id=7, amplitude=EnvelopeAmplitude(4, 0, 5))
    plain.null(4, None, null_factor=null_factor, neighbor_ports=(0,), costs=COSTS, events=events)
    assert plain.null_record is None and plain.output[12].order_key is None
    with pytest.raises(ValueError, match="at most six pending corrections"):
        SourceEnvelopeNode((2, 1, 1), pending_corrections=(None,) * (CORRECTION_QUEUE + 1))
