"""A reader's count, declared once (ALGEBRA.md, The NodeReader is one declaration kind for every experiment; the mathematician's hand with the advisor's second, two hands): a reader's Nodes carry the lay's weights, A_i^2 = A^2 w_i / SUM w, and the record's count is declared once, by its `parts` or by `count` for a record converted whole; a charged record's count is 1 (ALGEBRA.md, No record reads its own write of the sign)."""

from __future__ import annotations

from typing import Any

from event_universe.loader import derived
from event_universe.loader.derived import FamilyRule
from event_universe.loader.keys import integer


def reader_count(body: dict[str, Any], label: str, families: tuple[FamilyRule, ...], family: int) -> int:
    """The record's count of a reader with a record of its own: the sum of its parts' counts where it declares `parts` (`count` beside them refused by name), else its `count` (a record converted whole), else refused by name; above 1 refused for a family that reads a holder of the sign (`derived.charged`)."""
    declared = body.get("parts")
    if isinstance(declared, list) and all(isinstance(p, dict) for p in declared):
        if "count" in body:
            raise ValueError(f"{label} declares its count by its parts; `count` is a converted record's")
        count = sum(int(p["count"]) for p in declared if isinstance(p.get("count"), int))
    elif "count" in body:
        count = int(integer(body["count"], f"{label}.count", 1))
    else:
        raise ValueError(
            f"{label} declares no count: a record converted whole declares `count`, the record's count "
            "over its region declared once; a record with parts declares it in its parts"
        )
    if derived.charged(families, family) and count > 1:
        raise ValueError(
            f"{label} declares the count {count} of {body['family']!r}, a family that reads the holder of "
            "the sign: such a record is one quantum of its family, and many quanta are that many bodies "
            "of count 1, each its own record with its own row of the sign (ALGEBRA.md, No record reads "
            "its own write of the sign)"
        )
    return count
