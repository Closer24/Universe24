"""The bond registry: one number per pair, a bounded idempotent bank, the singlet's second answer."""

import pytest

from event_universe.core.spatial_state import TICKET_MODULUS
from event_universe.fields.bonds import MAX_OPEN_BONDS, BondRegistry


def test_the_first_answer_is_even_and_the_second_follows_the_singlet():
    registry = BondRegistry(7, 64)
    firsts = [registry.draw(bond, 0, bond * 13) for bond in range(1, 401)]
    assert 150 < sum(1 for outcome in firsts if outcome > 0) < 250
    assert len(registry.open) == 400 and registry.numbers == 400
    # Equal settings: the other end always disagrees; a half turn apart: always agrees.
    assert all(registry.draw(bond, 0, 5) == -first for bond, first in enumerate(firsts, 1))
    assert registry.open == {} and registry.released == 400
    registry = BondRegistry(7, 64)
    firsts = [registry.draw(bond, 0, bond * 13) for bond in range(1, 401)]
    assert all(registry.draw(bond, 32, 5) == first for bond, first in enumerate(firsts, 1))
    # A quarter turn apart: agreement about half the time.
    registry = BondRegistry(7, 64)
    firsts = [registry.draw(bond, 0, bond * 13) for bond in range(1, 401)]
    agreements = sum(registry.draw(bond, 16, 5) == first for bond, first in enumerate(firsts, 1))
    assert 150 < agreements < 250
    # Two questions per bond, one number per bond, and the number is fixed by seed and bond.
    assert registry.questions == 800 and registry.numbers == 400
    assert registry.number(5) == BondRegistry(7, 64).number(5) != BondRegistry(8, 64).number(5)


def test_the_same_end_asking_again_gets_the_same_answer_and_the_bank_is_bounded():
    registry = BondRegistry(3, 64)
    first = registry.draw(9, 4, 100)
    assert registry.draw(9, 4, 100) == first and registry.numbers == 1 and len(registry.open) == 1
    # The other end, at the same setting, always disagrees and releases the pair.
    assert registry.draw(9, 4, 101) == -first and registry.open == {}
    full = BondRegistry(3, 64)
    for bond in range(1, MAX_OPEN_BONDS + 1):
        full.draw(bond, 0, bond)
    with pytest.raises(OverflowError, match="at most 4096 open pairs"):
        full.draw(MAX_OPEN_BONDS + 1, 0, 1)
    assert full.draw(1, 0, 1) in (1, -1)  # an open pair still answers its own end


def test_the_registry_is_validated():
    with pytest.raises(ValueError, match="ticket modulus"):
        BondRegistry(TICKET_MODULUS, 64)
    with pytest.raises(ValueError, match="positive"):
        BondRegistry(1, 64).draw(0, 0, 0)


def test_an_external_stream_supplies_one_number_per_pair_in_order():
    stream = (5, TICKET_MODULUS - 1, 123456789)
    registry = BondRegistry(7, 64, stream)
    # The first pair takes the first number: 5 is below one half, so +1.
    assert registry.draw(11, 0, 1) == 1 and registry.consumed == 1
    assert registry.draw(11, 0, 1) == 1 and registry.consumed == 1  # idempotent, no new number
    assert registry.open[11][3] == 5
    # The second pair takes the second number: just below the modulus, so -1.
    assert registry.draw(12, 0, 1) == -1 and registry.open[12][3] == TICKET_MODULUS - 1
    assert registry.draw(13, 0, 1) in (1, -1) and registry.consumed == 3
    with pytest.raises(OverflowError, match="stream is exhausted"):
        registry.draw(14, 0, 1)
    # The other end of a streamed pair answers from the same number.
    assert registry.draw(11, 0, 2) == -1 and registry.open.get(11) is None
    with pytest.raises(ValueError, match="below the ticket modulus"):
        BondRegistry(7, 64, (TICKET_MODULUS,))
