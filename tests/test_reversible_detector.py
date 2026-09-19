"""Independent cases for the local reversible contact, design 418c5ac.

The exact integers are published in docs/DETECTOR_REQUIREMENTS.md before
implementation: q=2, quantum=3, +X -> +Y gives material (13,-10,2), phase 7;
the bounded nonwrapping domain contains 3,240 distinct complete states.
"""

from dataclasses import replace
from itertools import product

import pytest

from event_universe.events.reversible import (
    CarrierState,
    ContactState,
    clock_step,
    inverse_transduce,
    pointer_displacement,
    transduce,
)

SWAP_X_Y = (2, 1, 0, 3, 4, 5)
IDENTITY = (0, 1, 2, 3, 4, 5)
HEADINGS = ((1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1))
BOUND = (1 << 62) - 1


def test_contact_retains_carrier_and_previous_material_information_with_exact_recoil():
    carrier = CarrierState(0, 7, 2, 16, 0, (6, 0, 0))
    material = ContactState(5, (7, -4, 2))
    outgoing, changed = transduce(carrier, material, SWAP_X_Y, 32, 3)
    assert outgoing == CarrierState(0, 7, 2, 16, 2, (0, 6, 0))
    assert changed == ContactState(7, (13, -10, 2))
    assert tuple(a + b for a, b in zip(outgoing.momentum, changed.momentum, strict=True)) == (13, -4, 2)
    assert inverse_transduce(outgoing, changed, SWAP_X_Y, 32, 3) == (carrier, material)

    other_carrier, same_pointer = transduce(replace(carrier, phase=0), material, SWAP_X_Y, 32, 3)
    assert same_pointer == changed and other_carrier.phase == 0
    assert other_carrier != outgoing
    _, other_material = transduce(carrier, replace(material, phase=6), SWAP_X_Y, 32, 3)
    assert other_material.phase == 8 and other_material != changed


def test_complete_output_is_injective_and_invertible_on_3240_independent_inputs():
    outputs = set()
    for amount, phase, port, momentum in product(
        (1, 2), range(4), range(6), product((-1, 0, 1), repeat=3)
    ):
        carrier = CarrierState(0, 7, amount, phase, port, tuple(amount * h for h in HEADINGS[port]))
        for material_phase in range(4 - amount):
            material = ContactState(material_phase, momentum)
            result = transduce(carrier, material, SWAP_X_Y, 4, 1)
            assert result not in outputs
            outputs.add(result)
            assert inverse_transduce(*result, SWAP_X_Y, 4, 1) == (carrier, material)
    assert len(outputs) == 3240


def test_modular_contact_wrap_is_reversible_independently_of_readout_capacity():
    carrier = CarrierState(0, 1, 1, 9, 0, (1, 0, 0))
    material = ContactState(31, (0, 0, 0))
    result = transduce(carrier, material, IDENTITY, 32, 1)
    assert result == (carrier, ContactState(0, (0, 0, 0)))
    assert inverse_transduce(*result, IDENTITY, 32, 1) == (carrier, material)


def test_nonzero_clock_and_reverse_contact_order_restore_prior_material():
    first = CarrierState(0, 1, 1, 12, 0, (3, 0, 0))
    second = CarrierState(0, 2, 2, 16, 2, (0, 6, 0))
    initial = ContactState(5, (7, -4, 2))
    first_out, middle = transduce(first, initial, SWAP_X_Y, 32, 3)
    second_out, final = transduce(second, middle, SWAP_X_Y, 32, 3)
    age, phase = clock_step(2, 3, 4, 32, final.phase)
    assert (age, phase) == (3, 9)
    # The independently specified clock turn at age 2, content 3, K=4 is 1.
    restored_second, restored_middle = inverse_transduce(
        second_out, replace(final, phase=phase - 1), SWAP_X_Y, 32, 3
    )
    restored_first, restored_initial = inverse_transduce(first_out, restored_middle, SWAP_X_Y, 32, 3)
    assert (restored_first, restored_second, restored_initial) == (first, second, initial)


def test_pointer_uses_declared_reference_and_current_local_clock():
    assert pointer_displacement(9, 3, 3, 4, 4, 32) == 3
    assert clock_step(2, 3, 4, 32, 31) == (3, 0)


def test_pointer_clock_boundary_has_zero_displacement_after_a_valid_clock_step():
    age = BOUND - 15
    assert pointer_displacement(31, age, 2, 31, 1, 32) == 0
    next_age, next_phase = clock_step(age, 2, 1, 32, 31)
    assert (next_age, next_phase) == (age + 1, 1)
    assert pointer_displacement(next_phase, next_age, 2, 31, 1, 32) == 0


@pytest.mark.parametrize("change", [{"amount": True}, {"amount": 0}, {"momentum": (5, 0, 0)}])
def test_contact_rejects_noninteger_empty_and_noncanonical_inputs(change):
    carrier = replace(CarrierState(0, 7, 2, 16, 0, (6, 0, 0)), **change)
    with pytest.raises(ValueError):
        transduce(carrier, ContactState(5, (7, -4, 2)), SWAP_X_Y, 32, 3)


def test_contact_rejects_a_nonbijective_route():
    with pytest.raises(ValueError):
        transduce(CarrierState(0, 1, 1, 0, 0, (1, 0, 0)), ContactState(0, (0, 0, 0)), (0,) * 6, 32, 1)


def test_recoil_and_clock_intermediates_cannot_overflow_then_cancel():
    with pytest.raises(OverflowError):
        transduce(
            CarrierState(0, 1, BOUND, 0, 0, (BOUND, 0, 0)),
            ContactState(0, (BOUND, 0, 0)),
            (1, 0, 2, 3, 4, 5),
            32,
            1,
        )
    # The final clock difference would be only one, but age*content exceeds W.
    with pytest.raises(OverflowError):
        clock_step((1 << 61), 4, 4, 32, 0)
    with pytest.raises(OverflowError):
        pointer_displacement(0, (1 << 61), 4, 0, 4, 32)
