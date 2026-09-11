"""Canonical positive-register encoding for signed field magnitudes.

Only encoded pairs belong in new field records and packets. Decoded signed
integers are transient arithmetic inputs, not the stored representation. This
module does not migrate legacy particle, clock or momentum-ledger records.
"""

from event_universe.core.state import checked

EncodedMagnitude = tuple[int, int]
ZERO_CODE = 1
POSITIVE_CODE = 2
NEGATIVE_CODE = 3
ENCODED_ZERO: EncodedMagnitude = (1, ZERO_CODE)


def encode_signed(value: int) -> EncodedMagnitude:
    """Encode one signed physical-register value using only positive integers."""
    checked(value)
    if value == 0:
        return ENCODED_ZERO
    return abs(value), POSITIVE_CODE if value > 0 else NEGATIVE_CODE


def decode_signed(encoded: EncodedMagnitude) -> int:
    """Validate canonical positive storage before returning a signed value."""
    if not isinstance(encoded, tuple) or len(encoded) != 2:
        raise ValueError("an encoded magnitude requires a fixed two-integer tuple")
    magnitude, code = encoded
    checked(magnitude)
    checked(code)
    if magnitude < 1 or code not in (ZERO_CODE, POSITIVE_CODE, NEGATIVE_CODE):
        raise ValueError("positive magnitude and a defined sign code are required")
    if code == ZERO_CODE:
        if magnitude != 1:
            raise ValueError("encoded zero must use canonical magnitude one")
        return 0
    return magnitude if code == POSITIVE_CODE else -magnitude


def encode_values(values: tuple[int, ...]) -> tuple[int, ...]:
    """Flatten a fixed tuple of signed values into positive magnitude-code pairs."""
    return tuple(part for value in values for part in encode_signed(value))


def decode_values(encoded: tuple[int, ...]) -> tuple[int, ...]:
    """Validate and decode a schema-sized tuple of magnitude-code pairs.

    The definition owns its fixed width. This helper only validates the encoding;
    accepting a tuple here does not authorize a variable-sized physical record.
    """
    if not isinstance(encoded, tuple) or len(encoded) % 2:
        raise ValueError("encoded values require complete magnitude-code pairs")
    return tuple(decode_signed((encoded[i], encoded[i + 1])) for i in range(0, len(encoded), 2))
