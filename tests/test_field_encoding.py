"""Independent signed values represented by canonical positive register pairs."""

import pytest

from event_universe.core.state import MAX_CORE_INT
from event_universe.fields.encoding import decode_signed, encode_signed


@pytest.mark.parametrize(
    "value,encoded",
    [
        (0, (1, 1)),
        (1, (1, 2)),
        (-1, (1, 3)),
        (MAX_CORE_INT, (MAX_CORE_INT, 2)),
        (-MAX_CORE_INT, (MAX_CORE_INT, 3)),
    ],
)
def test_signed_codec_has_exact_positive_canonical_representations(value, encoded):
    assert encode_signed(value) == encoded
    assert decode_signed(encoded) == value


@pytest.mark.parametrize("value", [True, 1.0, MAX_CORE_INT + 1, -MAX_CORE_INT - 1])
def test_encoding_rejects_invalid_decoded_registers(value):
    with pytest.raises((TypeError, OverflowError)):
        encode_signed(value)


@pytest.mark.parametrize(
    "encoded",
    [
        (0, 1),
        (-1, 2),
        (2, 1),
        (1, 0),
        (1, 4),
        (True, 2),
        (1, 2.0),
        (MAX_CORE_INT + 1, 2),
        (1,),
        (1, 2, 3),
        [1, 2],
    ],
)
def test_decoding_rejects_noncanonical_or_invalid_positive_records(encoded):
    with pytest.raises((TypeError, ValueError, OverflowError)):
        decode_signed(encoded)
