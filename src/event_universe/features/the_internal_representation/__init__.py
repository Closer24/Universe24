"""THE INTERNAL REPRESENTATION (ALGEBRA.md 9.88 (7) (i); 9.101): n pairs at a Node, the generators exact triples, the transport across a Link the product of the Port's rotation with the generator's table.

One folder, one primitive (record 2221 (3)); the register finds it by this folder and reads
DECLARATION; bind gives its function for the loop (a row of the ledger not built yet:
no bind, a term naming it is refused at load).
"""

from __future__ import annotations

DECLARATION = {
    "name": "the internal representation",
    "place": "(i)",
    "word": "the right side",
    "reads": ("n pairs", "the generators' tables", "the Ports' accumulators"),
    "writes": ("the arrivals",),
    "order": 2,
    "section": "9.88 (7) (i); 9.101",
}
