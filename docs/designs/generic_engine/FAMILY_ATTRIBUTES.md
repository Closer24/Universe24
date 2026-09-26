# The family attributes: what the files hold and what the engine still lacks

The model owner's ask of 2026-09-26 (11:20Z, in Nature24's session): every force, coupling
and well is either an attribute of a family or a family; once the engine is closed and locked
they are added by name in the files and played with; the engine must run many attributes;
whatever is missing is either in the definitions file (good) or a support the engine must
still implement. This is the inventory, read from the loader and the universe file of
emitter-click at 01109b05 (the one stroke, commit 5 in part) by Nature24, the second party;
checking notes, not engine code (record 2135).

## 1. In the files today

The universe file `examples/events/universe.json` holds the integers (the Node clock, the
amplitude bound, Lambda, the momentum unit, the twist table) and the families; the loader
reads each family by its attributes and never by its name (records 2066, 2075; item 53).

| Attribute | Key in the family's entry | Form the loader admits | The engine reads it as |
| --- | --- | --- | --- |
| the name | `name` | any string, distinct, at most 20 families | a label only |
| the representation | `parts` | [1], [1, 3] or [1, 3, 6] (ALGEBRA.md 9.86) | the components the rule steps |
| the phase | `phase` | 1 or 2 | the record's phase kind |
| the pair (the mass and the range) | `pair` | [num, den] with den >= num, or "body" (every body declares its own) | the six-neighbour term's coefficients |
| the held source | `held` | {count: content or sign, factors, dipole: spin or moment, dipole_div} | the body's write at its Nodes (9.91 (3)) |
| the reads | `reads` | [{family, weight, twist, by}], weight an integer FROM 1 or "Lambda", by plain or sign, twist own, Lambda_v or an integer | the pace Gamma - SUM weight x by x level (9.91 (2)) |
| the self source | `self_source` | {unit} | the field's own energy as its source (9.97 (3)) |
| the clicks | `clicks` | {gives, takes, quantum} | the ladder and the giving |
| the lifetime | `lifetime` | an integer | the border every row of the family clicks on |

A family declaring none of the sources stays exactly zero at every interval (the leak test of
record 2075 (3)); the shipped families renamed at random give the same digests (item 53).

## 2. Missing in the engine: supports the algebra asks and the loader or the engine lacks

| Support | What the algebra asks | What the engine has | The gap |
| --- | --- | --- | --- |
| a signed read weight (a hill) | every read a hollow or a hill, the weight positive or negative (9.108 (8)) | the weight bounded from 1 (`_integer(read["weight"], ..., 1, AMOUNT_BOUND)`); `by: sign` gives - q x weight x level for a charge sign only | a negative weight, or a `by` word for the hill |
| the source verb of a record | every record adds its local count s_i = F_i div E_s into a family's level at its Nodes each interval (9.98 (11) (b), 9.108 (10) (a)); E_s a universe integer | the body's hold (the level written at a body's Nodes) and the field's self source; no record-driven source | the verb, and E_s (or the table's s_cap) in the universe file |
| the guard's second side | the pace stays below Gamma as well as above 0: above about 1.25 Gamma the step is unstable (docs/designs/rule_alone/README.md section 10) | the load's guard alone, on the static reach of the held content (`reach >= node_clock` refused); nothing at run time, nothing above | a run-time guard on both sides, needed the moment a read can be negative or a source can move |
| the click that keeps the momentum | the taking keeps the record's phase; the recoil into the Ports' angle accumulators; a record re-created whole carries K in the six Ports of its Node (9.109 (2)) | the four-vector click without the recoil (commit 5 in part) | the recoil's store |
| a free body moving by the rule | a body without `fixed` moves as its record does; the declared pair well and the hop retire (record 2168 (3), (d)) | the pair well on the body's Nodes and the hop | the retirement, once the well is a family |
| the internal representation | a family of n pairs with the exact rotation tables and the transport (9.88 (7) (i)) | a draft module (the primitives, stroke-side 725f79dc) with no family attribute and no loader hook | the attribute and the hook |
| the twist table's precision | 9.96 (2) (c) | the fine table all identities (the finding of 2026-09-26) | the mathematician's line |

## 3. The attribute set itself

The loader admits a fixed set of keys (`FAMILY_ENTRY_KEYS`) and refuses any other. That is
right for safety and wrong for the owner's second ask: a new attribute today is a new key,
and a new key is code. For an attribute to be added when the engine is closed and locked,
every attribute must be one generic term of one primitive, [degree, weight, table] (9.88 (7)
(ii)), and the engine must apply a term by its form: a read is a term into the pace, a source
a term into a level, a hold a term of a body, a click a term of the ladder. Then a family's
entry is a list of terms, and the twenty-first family or the attribute that did not exist
yesterday is a line in the file. Whether the term form covers every attribute of section 1
is the mathematician's line; whether the loader reads terms is The 3's build.

## 4. The tests at the end (checking code, Nature24's, once the merged engine is on main)

1. The adversarial universe: the shipped families renamed at random; every digest unchanged.
2. The cap: twenty families run; the twenty-first is refused by the loader's own line.
3. The null family: declared with no source, exactly zero at every interval of every shipped
   world.
4. The added attribute: a family with a hill on gravity (a negative weight) behaves as a hill
   against the algebra's number, with no code touched.
5. The closed engine: no family name, no flag, no default of a world key and no literal number
   of the universe anywhere under `src/event_universe` (records 2172 to 2174).
6. The rule as one function: one step of the engine equal to the rule's transcription bit for
   bit on random arrays (`docs/designs/rule_alone/rule_alone.py` does this today).
