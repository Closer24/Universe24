"""THE INTERNAL REPRESENTATION (ALGEBRA.md 9.88 (7) (i); 9.101; 9.117 item 3): n pairs at a Node, the generators exact triples, the transport across a Link the product of the Port's rotation with the generator's table; order 2 on the arrivals, the receive 1. 9.113 item 2: the step from the rule, the transport beyond (S).

One folder, one primitive (record 2221 (3)); the register finds it by this folder and reads
DECLARATION, the row of ALGEBRA.md 9.117 for this name (a row of the ledger not built yet:
no bind and no apply; a term naming it is refused at load).
"""

from __future__ import annotations

from event_universe.core.register import Declaration

DECLARATION = Declaration(
    "the internal representation",
    "(i)",
    ("n pairs", "the generators' tables", "the Ports' accumulators"),
    ("the arrivals",),
    2,
    None,
    "9.88 (7) (i); 9.101; 9.117 item 3",
    word="the right side",
)
