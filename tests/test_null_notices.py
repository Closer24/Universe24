"""Source-envelope null notices: local factor, Link transport, delayed commit and corrections.

A null that sends notices needs a ledger event identity; that case and the crossing-null
Node case went with the causal event ledger on 2026-09-17 (issue #164, bucket B.4).
"""

from fractions import Fraction

import pytest

from event_universe.core.disturbance_state import OPERATIONS, CostMeter, OperationCosts
from event_universe.core.node_services import NodeEvents
from event_universe.core.source_envelope_node import (
    CORRECTION_QUEUE,
    NOTICE_BANK,
    EnvelopePacket,
    SourceEnvelopeNode,
)
from event_universe.core.source_envelope_state import EnvelopeAmplitude, EnvelopeScale, NullRecord
from event_universe.diagnostics.node_contract import node_state_violations
from event_universe.fields.source_envelope import (
    local_output,
    null_correction,
    null_factor,
    scaled_weight,
    squared_weight,
)

SOURCE = (1, 1, 1)
MIDDLE = (2, 1, 1)
DETECTOR = (3, 1, 1)
COSTS = OperationCosts((1,) * len(OPERATIONS))


def meter():
    return CostMeter(COSTS)


def observed() -> tuple[NodeEvents, list[dict[str, object]]]:
    published: list[dict[str, object]] = []
    return NodeEvents(published.append), published


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


def test_vacuum_or_certain_null_sends_no_notice():
    events, published = observed()
    vacuum = SourceEnvelopeNode(DETECTOR)
    vacuum.null(1, None, null_factor=null_factor, neighbor_ports=(1,), costs=COSTS, events=events)
    assert all(packet is None for packet in vacuum.output) and vacuum.scale == EnvelopeScale()
    empty = SourceEnvelopeNode(DETECTOR, source_id=7)
    empty.null(1, None, null_factor=null_factor, neighbor_ports=(1,), costs=COSTS, events=events)
    assert all(packet is None for packet in empty.output) and empty.scale == EnvelopeScale()
    assert not published


def test_received_notice_waits_the_control_delay_then_forwards_away_from_its_arrival_port():
    events, published = observed()
    node = SourceEnvelopeNode(MIDDLE, source_id=7, amplitude=EnvelopeAmplitude(3, 0, 5))
    # Sent by the Node on the +x side through its -x Port (1); it enters here through Port 0.
    packet = EnvelopePacket(3, DETECTOR, 1, 7, None, scale=(25, 9), notice_id=11)
    node.receive(packet, 3, 1, 2, events, costs=COSTS)
    assert published[-1]["event"] == "source-notice-received"
    assert node.pending_scales[0] is not None and node.pending_scales[0].ready_tick == 5
    assert node.scale == EnvelopeScale()
    assert not node.complete(4, local_output, (), COSTS, (0, 1), 0, 1, events)
    assert node.complete(5, local_output, (), COSTS, (0, 1), 0, 1, events)
    assert node.scale == EnvelopeScale(25, 9)
    assert node.applied_notices[-1] == 11 and node.pending_scales[0] is None
    forwarded = [(slot, p) for slot, p in enumerate(node.output) if p is not None]
    assert [slot for slot, _ in forwarded] == [12 + 1]
    assert forwarded[0][1].scale == (25, 9) and forwarded[0][1].notice_id == 11
    assert published[-1]["event"] == "source-scale-committed"
    duplicate = EnvelopePacket(6, SOURCE, 0, 7, None, scale=(25, 9), notice_id=11)
    node.receive(duplicate, 6, 1, 0, events, costs=COSTS)
    assert published[-1]["event"] == "source-notice-ignored"
    assert node.scale == EnvelopeScale(25, 9) and node.pending_scales[1] is None
    assert not node_state_violations(node)


def test_applied_notice_bank_is_fixed_and_a_retired_node_ignores_notices():
    events, published = observed()
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
    assert published[-1]["event"] == "source-notice-ignored"
    assert retired.scale == EnvelopeScale() and all(p is None for p in retired.pending_scales)


# Crossing nulls: a null decided before an earlier-ordered notice arrives is corrected.


def test_null_correction_is_the_exact_quotient_and_telescopes():
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


def test_a_notice_sending_null_needs_an_event_identity_and_the_correction_queue_is_bounded():
    events, published = observed()
    node = SourceEnvelopeNode(MIDDLE, source_id=7, amplitude=EnvelopeAmplitude(4, 0, 5))
    with pytest.raises(ValueError, match="recording event owner"):
        node.null(
            4,
            None,
            null_factor=null_factor,
            neighbor_ports=(0, 1),
            costs=COSTS,
            events=events,
            null_weight=squared_weight,
        )
    assert not published
    with pytest.raises(ValueError, match="at most six pending corrections"):
        SourceEnvelopeNode(MIDDLE, pending_corrections=(None,) * (CORRECTION_QUEUE + 1))
