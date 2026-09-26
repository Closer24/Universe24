"""THE TRACE (ALGEBRA.md 9.112 item 5): one line per traced word per Node per interval with the integers read, written and the remainder; declared in the start file; read by no word.

One folder, one primitive (record 2221 (3)); the register finds it by this folder and reads
DECLARATION; bind gives its function for the loop (a row of the ledger not built yet:
no bind, a term naming it is refused at load).
"""

from __future__ import annotations

DECLARATION = {
    "name": "the trace",
    "place": "any",
    "word": "any",
    "reads": ("every word's integers",),
    "writes": (),
    "section": "9.112 item 5",
}
