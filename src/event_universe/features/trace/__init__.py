"""THE TRACE (ALGEBRA.md 9.112 item 5; 9.117 item 2): one line per traced word per Node per interval with the integers read, written and the remainder; declared in the start file; read by no word. 9.113 item 2: neither: a diagnostic.

One folder, one primitive (record 2221 (3)); the register finds it by this folder and reads
DECLARATION, the row of ALGEBRA.md 9.117 for this name (a row of the ledger not built yet:
no bind and no apply; a term naming it is refused at load).
"""

from __future__ import annotations

from event_universe.core.register import Declaration

DECLARATION = Declaration(
    "the trace", "any", ("every word's integers",), (), None, "9.112 item 5; 9.117 item 2", word="any"
)
