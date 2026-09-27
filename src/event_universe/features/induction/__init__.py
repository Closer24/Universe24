"""THE INDUCTION (ALGEBRA.md 9.117 item 2; 9.78 (4); 9.91 (8) (v)): n_a -= the change of (n_b V_b) div W over the interval.

One folder, one primitive (record 2221 (3)); the register finds it by this folder and reads
DECLARATION, the row of ALGEBRA.md 9.117 for this name (a row of the ledger not built yet:
no bind and no apply; a term naming it is refused at load).
"""

from __future__ import annotations

from event_universe.core.register import Declaration

DECLARATION = Declaration(
    "the induction",
    "(v)",
    ("the momentum part of the contraction at the body's Node this interval and the last",),
    ("a body's momentum n", "a body's remainders"),
    None,
    "9.117 item 2; 9.78 (4); 9.91 (8) (v)",
    word="after the step",
)
