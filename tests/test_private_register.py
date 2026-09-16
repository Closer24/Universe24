"""Independent private-channel, ownership and dense-admission contracts."""

from dataclasses import FrozenInstanceError
from itertools import permutations, product

import pytest

from event_universe.core.disturbance_state import MAX_VALUE, encode, pack
from event_universe.core.private_reference import DenseSelector
from event_universe.core.private_register import (
    PRIVATE_PORT_PAIRS,
    IdentityLaw,
    PrivateKey,
    PrivateNode,
    PrivateResult,
    PrivateState,
    PrivateUnit,
    RegisterDatum,
    private_transition,
)


def test_identity_preserves_received_properties_and_own_memory_exactly():
    # These numbers are opaque encoded components, not an asserted energy law.
    datum = RegisterDatum(pack((1, -1, 2, 1, 0, 0, 3)))
    state = PrivateState(pack((5, -2)))
    result = private_transition(state, datum, IdentityLaw())
    assert result.state is state
    assert result.output is datum
    assert result.output.codes == (3, 2, 5, 3, 1, 1, 7)
    with pytest.raises(FrozenInstanceError):
        datum.codes = pack((99,))


def test_numerical_zero_is_present_and_only_absence_is_a_noop():
    unit = PrivateUnit()
    zero = RegisterDatum((1,))
    before = unit.state
    assert unit.advance(zero) is zero
    assert unit.advance(None) is None
    assert unit.state is before


def test_private_units_have_independent_state_and_no_peer_or_host_references():
    node = PrivateNode()
    selected = node.unit(0, 2)
    selected.state = PrivateState(pack((7,)))
    datum = RegisterDatum(pack((11,)))
    expected = private_transition(selected.state, datum, selected.law)
    for unit in node.units:
        if unit is not selected:
            unit.state = PrivateState(pack((-99,)))
    assert private_transition(selected.state, datum, selected.law) == expected
    assert len({id(unit) for unit in node.units}) == 24
    assert PrivateUnit.__slots__ == ("state", "law")
    assert selected.state.codes == pack((7,))


@pytest.mark.parametrize("invalid", [(), (0,), (True,), (2 * MAX_VALUE + 2,), (1,) * 33, [1]])
def test_received_datum_rejects_invalid_or_unbounded_storage(invalid):
    with pytest.raises(ValueError):
        RegisterDatum(invalid)


def test_single_input_contract_rejects_hidden_batches_without_changing_own_state():
    unit = PrivateUnit(state=PrivateState((encode(4),)))
    before = unit.state
    with pytest.raises(ValueError, match="one received datum"):
        unit.advance((RegisterDatum((1,)), RegisterDatum((3,))))
    assert unit.state is before
    with pytest.raises(ValueError, match="identity law"):
        IdentityLaw("mix")
    with pytest.raises(ValueError, match="one output datum"):
        PrivateResult(before, (RegisterDatum((1,)), RegisterDatum((3,))))


def test_twenty_four_directed_pairs_have_all_cube_symmetries():
    pairs = frozenset(PRIVATE_PORT_PAIRS)
    assert len(pairs) == 24
    for port in range(6):
        assert sum(source == port for source, _ in pairs) == 4
        assert sum(target == port for _, target in pairs) == 4
    for axes in permutations(range(3)):
        for flips in product((0, 1), repeat=3):
            relabel = {p: 2 * axes[p // 2] + ((p % 2) ^ flips[p // 2]) for p in range(6)}
            assert {(relabel[p], relabel[q]) for p, q in pairs} == pairs
    for source in range(6):
        for target in (source, source ^ 1):
            with pytest.raises(ValueError, match="orthogonal"):
                PrivateKey((0, 0, 0), source, target)


def test_dense_reference_visits_all_units_but_selects_only_actual_due_inputs():
    first = PrivateKey((0, 0, 0), 0, 2)
    last = PrivateKey((1, 0, 0), 5, 3)
    dense = DenseSelector(((1, 0, 0), (0, 0, 0)))
    assert dense.select((last, first)) == (first, last)
    assert dense.checks == 48
    assert dense.select(()) == ()
    assert dense.checks == 96
    with pytest.raises(ValueError, match="at most one"):
        dense.select((first, first))
    with pytest.raises(ValueError, match="undeclared"):
        dense.select((PrivateKey((2, 0, 0), 0, 2),))
    assert dense.checks == 96


def test_dense_reference_covers_all_5184_units_on_the_periodic_six_cube():
    dense = DenseSelector(product(range(6), repeat=3))
    assert len(dense.keys) == 5184
    assert len(set(dense.keys)) == 5184
    assert dense.select(()) == ()
    assert dense.checks == 5184
