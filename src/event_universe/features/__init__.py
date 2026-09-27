"""THE FEATURES: every primitive of the engine in its own folder (the model owner's
decision of 2026-09-26, the Boss's records 2221 and 2224; ALGEBRA.md #the-primitives; issue #1154).

A folder under this package is one primitive: it declares its own name, its place in
the interval (the five of ALGEBRA.md #the-interval), its word (ALGEBRA.md #the-primitives), what it reads,
what it writes (the values named once in ALGEBRA.md #the-primitives) and its order among the writers
of one value at one place (`DECLARATION`, a `Declaration` of the register), and it holds
the one function the loop calls, `apply(term, start, own) -> writes`: `term` the family's
or the body's declaration read from the run's files, `start` the values of the interval's
start the primitive reads, `own` the record the primitive keeps its remainders on, and
the writes the values it hands back, entered by the loop at the primitive's place
(event_universe.core.primitive). Until a folder's body of code moves in, `bind(loop)`
gives the loop's method that implements it today; a folder with neither is a row of the
ledger not built, and a term naming it is refused at load. The folder's name is the
primitive's name without the article, the apostrophe dropped, a space or a hyphen an
underscore ("the spin's step" is spins_step, "the self-source" self_source). The register
(event_universe.core.register.discover) finds the folders and refuses a folder without a
declaration, a folder whose name is not its own, and a name declared twice; adding a
primitive adds a folder and touches no other file. A folder's declaration is the row of
ALGEBRA.md #the-primitives for its name, and a folder whose declaration differs from its row is not
approved until one moves; a folder's docstring carries the word of ALGEBRA.md #the-primitives for its
row, FROM THE RULE or BEYOND THE RULE, where the algebra gives one. Integers only: no
float, no family's name, no number of the universe.
"""
