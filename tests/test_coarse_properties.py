"""Independent bounded readout checks; these do not certify a closure law."""

import importlib.util
import sys
from dataclasses import FrozenInstanceError, replace
from pathlib import Path

import pytest

from event_universe.core.disturbance_state import MAX_VALUE
from event_universe.core.integer import MAX_WORK_INT

SPEC = importlib.util.spec_from_file_location(
    "coarse_properties", Path(__file__).parents[1] / "examples/coarse-graining/properties.py"
)
assert SPEC is not None and SPEC.loader is not None
MODULE = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = MODULE
SPEC.loader.exec_module(MODULE)
PropertySpec = MODULE.PropertySpec
Contribution = MODULE.Contribution
aggregate_properties = MODULE.aggregate_properties


def contribution(identity=0, **changes):
    return replace(Contribution((identity,), "cardinal-v1:tau=3", 0, 0, 3, ((2,), (2, 0, 0))), **changes)


def test_additive_readout_preserves_owned_energy_not_square_of_total_amplitude():
    schema = (
        PropertySpec("owned_energy", "sum"),
        PropertySpec("momentum", "vector_sum", 3),
        PropertySpec("amplitude", "sum"),
    )
    first = contribution(values=((4,), (2, 0, 0), (2,)))
    second = contribution(1, values=((9,), (3, 0, 0), (3,)))
    before = (first, second)
    result = aggregate_properties(schema, before, capacity=2)
    assert len(result) == 1
    assert result[0].values == ((13,), (5, 0, 0), (5,))
    assert result[0].values[0][0] != result[0].values[2][0] ** 2
    assert result[0].member_ids == ((0,), (1,)) and result[0].count == 2
    assert before == (first, second)
    with pytest.raises(FrozenInstanceError):
        result[0].remaining_delay = 0


@pytest.mark.parametrize(
    "changes",
    [
        {"law": "different-rule"},
        {"channel": 1},
        {"direction": 1},
        {"remaining_delay": 2},
        {"state_key": (1,)},
    ],
)
def test_each_explicit_compatibility_difference_preserves_separate_bins(changes):
    schema = (PropertySpec("energy", "sum"), PropertySpec("momentum", "vector_sum", 3))
    result = aggregate_properties(schema, (contribution(), contribution(1, **changes)), capacity=2)
    assert len(result) == 2
    assert tuple(item.member_ids for item in result) == (((0,),), ((1,),))
    assert all(item.values == ((2,), (2, 0, 0)) for item in result)


@pytest.mark.parametrize("mode", ["keep_equal", "phase_bins", "interaction_state"])
def test_exact_retained_property_distinguishes_futures_and_equal_values_can_group(mode):
    schema = (PropertySpec("quantity", "sum"), PropertySpec("retained", mode))
    items = (
        contribution(values=((2,), (0,))),
        contribution(1, values=((3,), (1,))),
        contribution(2, values=((5,), (0,))),
    )
    result = aggregate_properties(schema, items, capacity=3)
    assert tuple(item.values for item in result) == (((7,), (0,)), ((3,), (1,)))
    assert result[0].member_ids == ((0,), (2,))


def test_nonmergeable_equal_inputs_stay_separate_and_duplicates_are_rejected():
    schema = (PropertySpec("quantity", "sum"), PropertySpec("internal", "nonmergeable"))
    first = contribution(values=((2,), (7,)))
    second = contribution(1, values=((2,), (7,)))
    assert len(aggregate_properties(schema, (first, second), capacity=2)) == 2
    with pytest.raises(ValueError, match="duplicate"):
        aggregate_properties(schema, (first, first), capacity=2)


def test_full_block_bound_keeps_large_exact_sum_in_working_register():
    schema = (PropertySpec("quantity", "sum"),)
    items = tuple(contribution(i, values=((MAX_VALUE,),)) for i in range(2048))
    result = aggregate_properties(schema, items, capacity=2048)
    assert result[0].values == ((2_199_023_253_504,),)
    assert result[0].count == 2048
    with pytest.raises(ValueError, match="capacity"):
        aggregate_properties(schema, items, capacity=2047)
    with pytest.raises(ValueError, match="2048"):
        aggregate_properties(schema, (), capacity=2049)


@pytest.mark.parametrize("capacity", [True, 0, -1, 1.0])
def test_capacity_rejects_noninteger_or_nonpositive_limits(capacity):
    with pytest.raises(ValueError):
        aggregate_properties((PropertySpec("q", "sum"),), (), capacity=capacity)


@pytest.mark.parametrize(
    "changes",
    [
        {"identity": ()},
        {"identity": (0,) * 5},
        {"identity": (True,)},
        {"law": ""},
        {"law": "x" * 129},
        {"channel": True},
        {"channel": -1},
        {"direction": True},
        {"direction": 6},
        {"remaining_delay": -1},
        {"remaining_delay": MAX_WORK_INT + 1},
        {"state_key": (0,) * 129},
        {"state_key": (False,)},
        {"values": ((MAX_VALUE + 1,),)},
        {"values": ((True,),)},
        {"values": ((1, 2),)},
        {"values": ((0,),) * 17},
        {"values": [[1]]},
    ],
)
def test_contribution_rejects_unbounded_or_mutable_metadata(changes):
    with pytest.raises((ValueError, TypeError, OverflowError)):
        contribution(**changes)


@pytest.mark.parametrize(
    "arguments",
    [("q", "unknown"), ("q", "sum", 3), ("q", "vector_sum", 1), ("q", "sum", True)],
)
def test_schema_rejects_unsupported_operators_or_shapes(arguments):
    with pytest.raises(ValueError):
        PropertySpec(*arguments)


def test_complete_schema_and_tuple_boundary_are_checked_before_aggregation():
    one = (PropertySpec("quantity", "sum"),)
    with pytest.raises(ValueError, match="complete schema"):
        aggregate_properties(one, (contribution(),), capacity=1)
    with pytest.raises(ValueError, match="unique"):
        aggregate_properties(one * 2, (), capacity=1)
    with pytest.raises(ValueError, match="immutable"):
        aggregate_properties(one, iter(()), capacity=1)
    with pytest.raises(ValueError, match="sixteen"):
        aggregate_properties(tuple(PropertySpec(str(i), "sum") for i in range(17)), (), capacity=1)
    assert aggregate_properties(one, (), capacity=1) == ()


def test_renaming_properties_and_consistent_permutation_preserve_observed_sums():
    schema = (PropertySpec("a", "sum"), PropertySpec("b", "vector_sum", 3))
    items = (contribution(), contribution(1, values=((3,), (-1, 4, 0))))
    ordinary = aggregate_properties(schema, items, capacity=2)[0]
    renamed = (PropertySpec("impulse", "vector_sum", 3), PropertySpec("inventory", "sum"))
    permuted = tuple(replace(item, values=(item.values[1], item.values[0])) for item in items)
    changed = aggregate_properties(renamed, permuted, capacity=2)[0]
    assert ordinary.values == ((5,), (1, 4, 0))
    assert changed.values == ((1, 4, 0), (5,))
    assert changed.member_ids == ordinary.member_ids
