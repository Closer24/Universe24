"""THE HAND (ALGEBRA.md 9.88 (5)): the sign of S . n, an integer -1, 0, 1; a click declaring a hand is refused on a body of the other hand.

One folder, one primitive (record 2221 (3)); the register finds it by this folder and reads
DECLARATION; bind gives its function for the loop (a row of the ledger not built yet:
no bind, a term naming it is refused at load).
"""

from __future__ import annotations

DECLARATION = {
    "name": "the hand",
    "place": "(ii)",
    "word": "after the step",
    "reads": ("the body's spin S", "the body's momentum n"),
    "writes": ("the click's admission",),
    "section": "9.88 (5)",
}
