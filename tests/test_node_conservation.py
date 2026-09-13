"""Independent exact checks of complete local owners before physical mutation."""

from dataclasses import replace

import pytest

from event_universe.core.disturbance_state import (
    MAX_VALUE,
    OPERATIONS,
    DisturbanceRecord,
    Expression,
    FieldDefinition,
    OperationCosts,
    pack,
)
from event_universe.core.node_conservation import (
    CarrierReadout,
    ConservedReadout,
    LocalInventory,
    NodeConservationDefinition,
)
from event_universe.core.spatial_state import SpatialFieldDefinition
from event_universe.fields.node_conservation import LocalBalanceGuard


def field(index=0):
    return Expression("field", field=index)


def op(name, *args):
    return Expression(name, arguments=args)


def record(amount, direction=(0, 0, 0)):
    return DisturbanceRecord(0, (pack((amount,)), pack(direction)), ((1,), (1, 1, 1)))


def guard(expression=None, *, spatial=False):
    fields = (
        FieldDefinition("amount", 1, "unit", True, False),
        FieldDefinition("direction", 3, "vector unit", True, False),
    )
    expression = field() if expression is None else expression
    readouts = (
        ConservedReadout(
            "first", 1, "unit", (CarrierReadout((0,), expression),), expression if spatial else None
        ),
        ConservedReadout(
            "second", 3, "vector unit", (CarrierReadout((0,), field(1)),), field(1) if spatial else None
        ),
    )
    spatial_fields = (
        tuple(
            SpatialFieldDefinition(index, pack((0,) * item.components))
            for index, item in enumerate(fields)
        )
        if spatial
        else ()
    )
    return LocalBalanceGuard(
        fields,
        spatial_fields,
        OperationCosts((1,) * len(OPERATIONS)),
        NodeConservationDefinition("local test", readouts),
    )


def bundle(amount, direction=(0, 0, 0)):
    return ((pack((amount,)),) + (pack((0,)),) * 7, (pack(direction),) + (pack((0, 0, 0)),) * 7)


def test_complete_transfer_preserves_owner_once():
    original = record(7, (2, -1, 0))
    policy = guard()
    before = LocalInventory(records=(original,))
    transit = LocalInventory(carrier_packets=(original,))
    after = LocalInventory(records=(original,))
    policy.check(before, transit, "dispatch")
    policy.check(transit, after, "receive")
    assert policy.measure(after) == ((7,), (2, -1, 0))
    with pytest.raises(ValueError, match="first"):
        policy.check(
            before, LocalInventory(records=(original,), carrier_packets=(original,)), "duplicate"
        )


def test_nonlinear_merge_is_rejected_with_unchanged_inputs():
    policy = guard(op("mul", field(), field()))
    first, second = record(2), record(3)
    before = LocalInventory(records=(first,), carrier_packets=(second,))
    candidate = LocalInventory(records=(record(5),))
    assert policy.measure(before)[0] == (13,)
    assert policy.measure(candidate)[0] == (25,)
    with pytest.raises(ValueError, match="first"):
        policy.check(before, candidate, "merge")
    assert before.records == (first,) and before.carrier_packets == (second,)


def test_field_and_carrier_reaction_balance_together():
    policy = guard(spatial=True)
    policy.validate_empty()
    before = LocalInventory(records=(record(3, (1, 0, 0)),), spatial=bundle(4, (-1, 1, 0)))
    after = LocalInventory(records=(record(4, (0, 1, 0)),), spatial=bundle(3))
    policy.check(before, after, "joint reaction")
    assert policy.measure(before) == policy.measure(after) == ((7,), (0, 1, 0))


def test_independent_spatial_packets_are_measured_before_combining():
    policy = guard(op("mul", field(), field()), spatial=True)
    before = LocalInventory(spatial_packets=(bundle(2), bundle(3)))
    after = LocalInventory(spatial=bundle(5))
    with pytest.raises(ValueError, match="first"):
        policy.check(before, after, "field receipt")


def test_momentum_failure_is_not_hidden_by_energy_balance():
    with pytest.raises(ValueError, match="second"):
        guard().check(
            LocalInventory(records=(record(3, (1, 0, 0)),)),
            LocalInventory(records=(record(3, (0, 1, 0)),)),
            "turn",
        )


def test_missing_layout_is_rejected():
    with pytest.raises(ValueError, match="exactly once"):
        guard().measure(LocalInventory(records=(replace(record(2), type_index=1),)))


def test_empty_field_cannot_supply_a_constant_conserved_readout():
    with pytest.raises(ValueError, match="empty spatial"):
        guard(Expression("literal", literal=(1,)), spatial=True).validate_empty()


def test_overflow_before_later_cancellation_is_rejected():
    # Each square fits a working register, but nine positive contributions do not.
    policy = guard(op("mul", field(), field()))
    owners = tuple(record(MAX_VALUE) for _ in range(9))
    with pytest.raises(OverflowError, match="64-bit"):
        policy.measure(LocalInventory(records=owners))


def test_guard_does_not_charge_model_work_or_depend_on_tariffs():
    policy = guard()
    other = replace(policy, costs=OperationCosts((99,) * len(OPERATIONS)))
    state = LocalInventory(records=(record(2, (1, 2, 3)),))
    assert policy.measure(state) == other.measure(state)
    policy.check(state, state, "identity")


def test_local_capacity_is_bounded():
    with pytest.raises(ValueError, match="capacity"):
        guard().measure(LocalInventory(records=(record(1),) * 33))
