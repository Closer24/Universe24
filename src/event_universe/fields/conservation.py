"""Exact local integer-ratio emission with an explicitly retained remainder."""

from event_universe.core.state import checked, checked_work


def split_ratio(
    amount: int, weights: tuple[int, ...], remainder: int = 0
) -> tuple[tuple[int, ...], int]:
    """Emit only whole weighted bundles; never distribute leftover units.

    The caller supplies a fixed schema-sized weight tuple. With A equal to new
    amount plus old remainder and W equal to sum(weights), outputs are
    floor(A/W)*weights and new remainder A%W. Thus every nonzero emitted bundle
    has the exact declared ratios and its missing amount stays local.
    """
    checked_work(amount)
    checked(remainder)
    if amount < 0 or remainder < 0 or not isinstance(weights, tuple) or not weights:
        raise ValueError("non-negative amounts and a fixed nonempty weight tuple are required")
    width = 0
    for weight in weights:
        checked(weight)
        if weight < 0:
            raise ValueError("directional weights must be non-negative")
        width = checked_work(width + weight)
    if width == 0 or remainder >= width:
        raise ValueError("positive total weight and a remainder below it are required")
    available = checked_work(amount + remainder)
    bundles, retained = divmod(available, width)
    portions = tuple(checked(checked_work(bundles * weight)) for weight in weights)
    return portions, checked(retained)
