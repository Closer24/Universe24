"""THE HAND (ALGEBRA.md #what-is-open): the sign of S . n, an integer -1, 0, 1; a click declaring a hand is refused on a body of the other hand (a check, no value written). ALGEBRA.md #the-primitives: beyond (L, S).

One folder, one primitive (record 2221 (3)); the register finds it by this folder and reads
DECLARATION, the row of ALGEBRA.md #the-primitives for this name (a row of the ledger not built yet:
no bind and no apply; a term naming it is refused at load).
"""

from __future__ import annotations

from event_universe.core.register import Declaration

DECLARATION = Declaration(
    "the hand",
    "(ii)",
    ("a body's spin S", "a body's momentum n"),
    (),
    None,
    "ALGEBRA.md #what-is-open",
    word="after the step",
)
