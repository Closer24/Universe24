"""THE HOP (ALGEBRA.md 9.117 item 2; 9.52; 9.104 item 6): the position's accumulator += n each interval; at W the body's Nodes move one Link along the axis and the accumulator keeps the rest; a body with fixed does not hop.

One folder, one primitive (record 2221 (3)); the register finds it by this folder and reads
DECLARATION, the row of ALGEBRA.md 9.117 for this name (the count's line, bound at (ii), moves a body's Nodes by its record's current; this card
is not built: its line would be the position's accumulator, which the law no longer keeps).
"""

from __future__ import annotations

from event_universe.core.register import Declaration

DECLARATION = Declaration(
    "the hop",
    "(v)",
    ("n", "W", "the hop's remainder", "fixed"),
    ("a body's position", "a body's remainders"),
    None,
    "9.117 item 2; 9.52; 9.104 item 6",
    word="after the step",
)
