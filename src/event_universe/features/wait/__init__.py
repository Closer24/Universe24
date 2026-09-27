"""THE WAIT (ALGEBRA.md 9.112 item 1): one interval, for every Port, always: a value sent at the start of t is combined in t.

One folder, one primitive (record 2221 (3)); the register finds it by this folder and reads
DECLARATION, the row of ALGEBRA.md 9.117 for this name, and its function `wait`.
"""

from __future__ import annotations

from event_universe.core.register import Declaration


def wait() -> int:
    """WAIT is one interval, always (ALGEBRA.md 9.112 item 1): a value sent at the start of t is combined in t."""
    return 1


DECLARATION = Declaration("the wait", "(i)", (), (), wait, "9.112 item 1", word="the step")
