"""The bond registry: an even first coin, the singlet's conditional second, and its validation."""

import pytest

from event_universe.core.spatial_state import TICKET_MODULUS
from event_universe.fields.bonds import BondRegistry


def test_the_first_answer_is_even_and_the_second_follows_the_singlet():
    registry = BondRegistry(7, 64)
    firsts = [registry.draw(bond, 0, bond * 13) for bond in range(1, 401)]
    assert 150 < sum(1 for outcome in firsts if outcome > 0) < 250
    # Equal settings: the other end always disagrees; a half turn apart: always agrees.
    assert all(registry.draw(bond, 0, 5) == -first for bond, first in enumerate(firsts, 1))
    registry = BondRegistry(7, 64)
    firsts = [registry.draw(bond, 0, bond * 13) for bond in range(1, 401)]
    assert all(registry.draw(bond, 32, 5) == first for bond, first in enumerate(firsts, 1))
    # A quarter turn apart: agreement about half the time.
    registry = BondRegistry(7, 64)
    firsts = [registry.draw(bond, 0, bond * 13) for bond in range(1, 401)]
    agreements = sum(registry.draw(bond, 16, 5) == first for bond, first in enumerate(firsts, 1))
    assert 150 < agreements < 250
    assert registry.questions == 800


def test_the_registry_is_validated():
    with pytest.raises(ValueError, match="ticket modulus"):
        BondRegistry(TICKET_MODULUS, 64)
    with pytest.raises(ValueError, match="positive"):
        BondRegistry(1, 64).draw(0, 0, 0)
