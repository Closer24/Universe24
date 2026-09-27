"""THE WAIT (ALGEBRA.md #the-interval): one interval, for every Port, always: a value sent at the start of t is combined in t.

One folder, one primitive (record 2221 (3)); the register finds it by this folder and reads
DECLARATION, the row of ALGEBRA.md #the-primitives for this name, and its function `wait`.
"""

from __future__ import annotations

from event_universe.core.register import Declaration


def wait() -> int:
    """WAIT is one interval, always (ALGEBRA.md #the-interval): a value sent at the start of t is combined in t."""
    return 1


DECLARATION = Declaration("the wait", "(i)", (), (), wait, "ALGEBRA.md #the-interval", word="the step")
