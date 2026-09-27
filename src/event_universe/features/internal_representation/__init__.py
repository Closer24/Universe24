"""THE INTERNAL REPRESENTATION (ALGEBRA.md #what-is-open, #the-transport, #the-primitives): n pairs at a Node, the generators exact triples, the transport across a Link the product of the Port's rotation with the generator's table; order 2 on the arrivals, the receive 1. ALGEBRA.md #the-primitives: the step from the rule, the transport beyond (S).

One folder, one primitive (record 2221 (3)); the register finds it by this folder and reads
DECLARATION, the row of ALGEBRA.md #the-primitives for this name (a row of the ledger not built yet:
no bind and no apply; a term naming it is refused at load).
"""

from __future__ import annotations

from event_universe.core.register import Declaration

DECLARATION = Declaration(
    "the internal representation",
    "(i)",
    ("n pairs", "the generators' tables", "the Ports' accumulators"),
    ("the arrivals",),
    None,
    "ALGEBRA.md #what-is-open, #the-transport, #the-primitives",
    word="the right side",
)
