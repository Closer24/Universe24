"""The revised internal graph has 24 symmetric directed one-to-one units."""

from itertools import permutations, product

import pytest

from event_universe.core.register_contracts import (
    INTERNAL_PORT_PAIRS,
    InternalRegisterKey,
    InternalRegisterState,
    RegisterInput,
    RegisterOutput,
)


def test_exactly_four_internal_targets_per_external_port():
    assert len(INTERNAL_PORT_PAIRS) == len(set(INTERNAL_PORT_PAIRS)) == 24
    units = tuple(InternalRegisterState(source, target) for source, target in INTERNAL_PORT_PAIRS)
    assert len(units) == 24
    for port in range(6):
        targets = {target for source, target in INTERNAL_PORT_PAIRS if source == port}
        assert targets == {candidate for candidate in range(6) if candidate // 2 != port // 2}
        assert sum(target == port for _, target in INTERNAL_PORT_PAIRS) == 4
    assert {(target, source) for source, target in INTERNAL_PORT_PAIRS} == set(INTERNAL_PORT_PAIRS)


def test_internal_graph_preserves_every_signed_axis_permutation():
    pairs = set(INTERNAL_PORT_PAIRS)
    # All 48 cubic axis permutations/reflections act on the same generic graph.
    for axes in permutations(range(3)):
        for reversed_axes in product((0, 1), repeat=3):
            remap = {
                port: 2 * axes[port // 2] + ((port % 2) ^ reversed_axes[port // 2]) for port in range(6)
            }
            assert {(remap[source], remap[target]) for source, target in pairs} == pairs


@pytest.mark.parametrize("target", [0, 1])
def test_same_axis_is_not_silently_added_to_internal_graph(target):
    with pytest.raises(ValueError, match="orthogonal"):
        InternalRegisterKey((1, 2, 3), 0, target)


def test_each_unit_has_only_one_input_and_one_output_reference():
    unit = InternalRegisterState(0, 2, RegisterInput(0), RegisterOutput(1))
    assert unit.input.slot == 0
    assert unit.output.slot == 1
    with pytest.raises(ValueError, match="exactly one input"):
        InternalRegisterState(0, 2, (RegisterInput(0), RegisterInput(1)), RegisterOutput(2))
    with pytest.raises(ValueError, match="exactly one output"):
        InternalRegisterState(0, 2, RegisterInput(0), (RegisterOutput(1), RegisterOutput(2)))
    # These are channel/reference contracts, not a hidden split/merge operation.
    assert not hasattr(unit, "payloads")


@pytest.mark.parametrize("slot", [-1, 32, True, [0, 1]])
def test_single_channel_reference_is_bounded_and_scalar(slot):
    with pytest.raises(ValueError, match="one bounded"):
        RegisterInput(slot)
    with pytest.raises(ValueError, match="one bounded"):
        RegisterOutput(slot)
