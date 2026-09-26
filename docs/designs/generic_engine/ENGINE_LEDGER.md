# The engine's ledger: what is implemented, what is to do

The model owner's word of 2026-09-26 (11:35Z, in Nature24's session): one place that says
what the engine implements and what is still to do; the engine is closed when everything has
moved to "implemented" and the "to do" column is empty. One row per generic support and per
family attribute; each row names where the support lives and the test that proves it. A row
without a green test stays "to do". The Boss owns the ledger; Nature24 is the second party who
checks each row; The 3 moves a row by landing its build and its test. Read from emitter-click
01109b05 and stroke-side 2ec28033; the attributes' detail is in FAMILY_ATTRIBUTES.md.
The ledger stays here until the documents' merge (item 22), then becomes a section of
docs/ENGINE.md; the table of primitives of record 2179 is its section 3, one file, not two
(the Boss's record 2180).

## 1. Implemented

| Support | Where | The test that proves it |
| --- | --- | --- |
| the rule, one step at every Node (9.57 (1), 9.91 (2)) | `events/rule.py` | the one step equal to the rule's transcription bit for bit on random arrays (`docs/designs/rule_alone/rule_alone.py`); the resting worlds bit for bit at every commit |
| the representation as parts, 1, 1 + 3, 1 + 3 + 6 (9.86) | the loader's `parts`, the stepping of every component | the leak test per part (commit 2) |
| the four paces from the reads (9.91 (2)) | commit 3 | bit for bit with the tensor zero |
| the held source of a body: the count, its factors, its dipole (9.91 (3)) | the loader's `held` | the holds' tests of commit 2 |
| the reads with a positive weight and a twist | the loader's `reads` | the digests of the shipped worlds |
| the wall W = 3 Q M | commit 4 | its test |
| the charge's four components with light as its wave, the transport (9.86, 9.81 (2)) | commit 4 | its tests; the twist table provisional |
| the point emitter as the law's one giving (9.69 (2), 9.85 (5)) | commit 7 | the point emitter's tests |
| the four-vector click without the recoil | commit 5 in part (01109b05) | its tests |
| the spin's step and the self-source slot | commit 6 in part, provisional | its tests |
| the click journal and the backward run | record 2070's build | the property test |
| the families file and the leak test (record 2075) | `universe.json`, the runner | a family with no source exactly zero at every interval |
| the cancel of the ray law, nothing deleted | stroke-side, merged | `tests/test_cancelled_paths.py` |
| the check-mode worlds' generator | stroke-side, merged | `tests/test_check_mode_worlds.py` |
| the engine start file, every default out of the code (record 2089) | `examples/events/engine_start.json` | its test |

## 2. To do

| Support | What is missing | The test that will prove it |
| --- | --- | --- |
| a signed read weight, a hill (9.108 (8)) | the loader bounds the weight from 1 | a family with a hill on gravity behaves as a hill against the algebra's number, no code touched |
| the source verb of a record (9.98 (11) (b), 9.108 (10) (a)) | no record adds its count into a family's level; only the body's hold and the field's self source | a sourced family's level equals the static response to a held record, in integers |
| the guard on both sides of the pace, at run time | the load's guard alone, from below | a world whose content reaches Gamma or 0 at run time stops with the guard's line |
| the click that keeps the momentum (9.109 (2)) | the recoil's store in the Ports' accumulators | one body keeps its speed across clicks; the ninth question's rerun in the engine |
| a free body moving by the rule (record 2168 (3)) | the pair well and the hop still there | the falling body of item 1 as a world file, no `fixed` |
| the internal representation as a family attribute (9.88 (7) (i)) | the primitives are a draft with no attribute and no hook | a family of n pairs transported around a loop returns to itself |
| the twist table's precision (9.96 (2) (c)) | the fine table all identities | the mathematician's line and its test |
| the attribute set as generic terms (9.88 (7) (ii)) | the loader admits a fixed set of keys | an attribute declared only in the file gives its effect with no code change |
| universe.json and the words of record 2128 | the words in part | the loader reads `universe`, `q`, `stocks` and refuses the old words |
| the residue lines and the eight failing tests | listed in docs/CANCELLED_WORLDS.md section 9 | the gate green |
| commit 10, the convergence test | not run | the check-mode table blind with everything on, the rule of three per row |
| no flag, family name or number in the code (records 2172 to 2174) | the review after the merge | a grep of `src/event_universe`, empty |

## 3. The one table of primitives (the ledger's section of supports)

The Boss's records 2179 and 2180 of 2026-09-26, on the model owner's question "what is the
generic implementation in the engine for families?": a PRIMITIVE is a kind of attribute the
engine can apply, written once in the code and applied to any family by its kind, never by
its name; an ATTRIBUTE is a family's declared value of a primitive, written in the run's
files, never in the code (HIGHLIGHTS 5.6; ALGEBRA.md 9.110 items 1 and 3). The engine
implements the rule, the click and this closed set of primitives; The 3 supports exactly this
table after the merge; the tests at the end check it. Any experiment is then a change of the
files and a check-mode run; a kind this table lacks is proposed as a new row, never written
into a step. The keys are the loader's of emitter-click 01109b05 where a row is implemented
and 9.110 item 3's word where it is to do.

| Primitive | Key (universe.json family row unless said) | Allowed values | ALGEBRA.md | The test (green today, or to do) |
| --- | --- | --- | --- | --- |
| the pair: the range and the rest rotation of the six-neighbour term | `pair`; a body's or an emitter's `pair` in the world file when the row says "body" | [num, den], two integers from 1 with den >= num (den = num massless, den > num a range), or the word "body" | 9.57 (1), 9.85 (3), 9.91 (7), 9.110 item 3 | green: `tests/test_families_file.py` (the file and the inline list bit for bit; the body's kind where the row says "body"); `tests/test_engine_acceptance.py` test (f) (three pairs bit for bit against the rule's transcription) |
| the degree: the representation as parts | `parts` | [1], [1, 3] or [1, 3, 6] (degree 0, 1, 2: scalar, vector, tensor; 9.86) | 9.86, 9.88 (7) (the term's degree), 9.91 (2), 9.110 item 3 | green: `tests/test_vector_holds.py` (the parts written and inverted; every other part silent at rest); the leak test per part of commit 2 |
| the phase: one level or a pair | `phase` | 1 or 2 | 9.91 (2), 9.110 item 3 | green: `tests/test_families_file.py` |
| the signed read with a twist: a coupling into the pace | `reads`, a list of {`family`, `weight`, `twist`, `by`} | `family` a row's name; `weight` today an integer from 1 or the word "Lambda", after the merge any nonzero integer (positive a hollow, negative a hill); `twist` "own", "Lambda_v" or an integer; `by` "plain" (1) or "sign" ("q") | 9.91 (2), 9.108 (8), 9.110 items 2 and 3 | green for the positive weight: the shipped worlds' digests, `tests/test_engine_acceptance.py` test (a) (the same digests under random names); TO DO for the sign: `tests/test_engine_acceptance.py` test (d), a hill on gravity against the algebra's number (xfail strict today) |
| the hold: a body's count and dipole written at its Nodes | `held`, {`count`, `factors`, `dipole`, `dipole_div`} | `count` "content" or "sign"; `factors` one integer per part; `dipole` "spin" or "moment"; `dipole_div` an integer from 1 | 9.91 (3), 9.85 (7), 9.110 items 2 and 3 | green: `tests/test_vector_holds.py` (a moving body's vector and tensor parts with the remainders carried; the dipoles written and inverted exactly) |
| the source: a record's count added into a family's level | TO DO: `sourced`, {the records' family, the weight, the scale} on the sourced row; the scale E_s (or the table's cap) an integer of universe.json | the weight a nonzero integer; E_s an integer from 1; the saturating form s_i = s_cap F div (s_cap E_s + F) as the primitive's own table | 9.98 (11) (b), 9.108 (8), (10) (a), 9.110 items 2 and 5 | TO DO: a sourced family's level equals the static response to a held record, in integers (the transcription is `docs/designs/rule_alone/binding_family.py`, source=level and source=table) |
| the clicks: the ladder, the giving, the taking, the recoil | `clicks`, {`gives`, `takes`, `quantum`}; the recoil has no key: it is the click step's own | `gives` and `takes` true or false; `quantum` an integer from 1 | 9.25 (2), (3), 9.91 (4), 9.109 (2), 9.110 item 2 | green: `tests/test_emitter.py` (M excitations give M givings, the quanta conserved), `tests/test_amplitude_click.py` (the offers and the ladder); TO DO for the recoil into the Ports' accumulators: one body keeps its speed across clicks, the ninth question's rerun in the engine (`docs/designs/rule_alone/item9_clicks.py` is the transcription of the bath) |
| the lifetime: the border a family's records click on at an age | `lifetime` | an integer from 1 through the world's `age_bound`; today admitted on the inline list's family only, not on a universe.json row (the ray law's form) | 9.88 (3) (a lowered pair is the short range; the lifetime a border, not a force), the border's rule in docs/ENGINE.md | green: `tests/test_lifetime.py` (the escape booked as a face does; the reach on the flight table; the refusals); TO DO: the key admitted on a universe.json row, or the row says the border is retired for the lowered pair |
| the internal representation: n pairs with exact rotation tables and the transport | TO DO: `internal`, {n, the generators' tables} | n an integer from 1; every generator an exact triple or quadruple of the twist table | 9.88 (7) (i), (1), 9.81 (2), 9.96 (2) | draft green: `tests/test_primitives.py` (the identities and the exact product; the transport composes and inverts per Node; the loader's hook refuses the rest); TO DO: the attribute on a row and the hook in the loader, then a family of n pairs transported around a loop returns to itself |
| the clicks list: several products of one click and the momenta's share | TO DO: `clicks` takes a list of givings, each {`family`, `count`, `sign`}, beside `gives`, `takes`, `quantum` | every product a row's name with an integer count from 1; the conserved integers of the products sum to the taken quantum's or the loader refuses; the share by the record's residue on its own wheel scaled to the wall | 9.88 (4), (7) (iii), 9.99 (6) | draft green: `tests/test_primitives.py` (the list balances the conserved integers or refuses; the momenta shared whole with the sum exact); TO DO: the attribute on a row, then a body giving into two families at its period gives the counts in the declared ratio |
| the hand: the helicity sign a click takes or gives | TO DO: `hand` on a giving of the clicks list, or on a body's click | -1, 0 (none) or 1; the sign of the body's spin dotted with its momentum, an integer; a wave has none | 9.88 (5), (7) (iv) | draft green: `tests/test_primitives.py` (the helicity's sign and its admission); TO DO: the attribute on a row, then a click with a declared hand refused on a body of the other hand |
| the self-source as an integer polynomial with a structure table | `self_source` {`unit`} today; TO DO the structure table on the same object | `unit` an integer from 0 (0 off); the table the family's constants, integers, degree two and three | 9.78 (3), 9.88 (2), (7) (ii), 9.91 (5) | green for the unit: the shipped worlds' digests; TO DO for the table: waits for the mathematician's line, then two colour sources under a self-coupled family at a large unit and the field's energy between them read against the algebra's number |

Not a row but a rule of the engine: THE REMAINDERS. Every division of every primitive keeps
its remainder on the dividing family's record at the Node (the hold's, the read's, the
source's, the recoil's, the transport's), carried between intervals and inverted with the
step; nothing else is kept at a Node; every intermediate a bounded integer (9.91 (2), (3),
9.109 (2) (b); the local integer operation contract of docs/ARCHITECTURE.md). The model owner's
word of 2026-09-26 (12:00Z, in Nature24's session): "behaviour with remainders where needed;
everything only in whole numbers".

Not a row but a rule of the engine: THE PACE'S GUARD ON BOTH SIDES. Every pace stays in
0 < p <= Gamma at run time, for every family and every axis, whatever the reads and the
sources declare (9.110 item 2; 9.108 items 11 and 12; docs/designs/rule_alone/README.md
section 10: above about 1.25 Gamma the step is unstable). Today the guard is the load's alone,
from below (`reach >= node_clock` refused); the run-time guard on both sides is the to-do row
of section 2 and stops the run with the guard's line, never a flag.

Not rows either: the integers of the universe (`node_clock`, `amplitude_bound`, `Lambda`,
`momentum_unit`, the twist table's unit and triples, and E_s with the source) are
declarations of the universe, one copy (9.110 item 5); a body's keys are declarations of a
body (9.110 item 4); the self-source's unit (`self_source` {`unit`}) is a declared integer
polynomial whose structure table waits for the mathematician (9.88 (7) (ii)), listed in
section 1 as provisional.

THE NUCLEAR FORCES AS DECLARATIONS, checked against the table (the model owner's word of
2026-09-26, 12:00Z: "make sure the options for the additional families, the nuclear force,
exist, so that everything closes as it should"; 9.88 (7): "with these four the strong and the
weak forces are declarations"). The strong force as the well: two sourced families with the
pairs [1000, 1019] and [1000, 1181], one read positive and one negative, the source's table
(rows 4 and 6; 9.108). The strong force as colour: a family with the internal representation
n = 3 or 8 and a structure table on its self-source, the clicks list refusing a coloured
product alone (rows 9, 10, 12). The weak force: a massive vector family (parts [1, 3], a
lowered pair) with a clicks list of several products and a hand (rows 1, 2, 10, 11). A decay:
a body giving into several families at its period (row 10). No row names a force; a force
that needs a thirteenth kind is a new row, proposed before it is written.

THE EXPERIMENT'S TOOLS ARE DECLARATIONS TOO, and each is tested alone (the model owner's word
of 2026-09-26, 12:00Z: "the engine does not know what you built in the experiment; you compose
it generically; the crystal can be tested alone, a detector alone, everything alone, not all
together at large"). A crystal, a polariser, a detector, a screen, a counter, an emitter and
a receiver are bodies of the world file with their keys (9.110 item 4; the detectors' rule of
9.92); a tool's test is one world with the tool alone and its one reading; the shipped
experiment is the composition, run in check mode, and owes no test of its own beyond the
composition's digest. The engine's own tests are the rows above, one small test per row.

## 4. The closing condition

The engine is closed when section 2 is empty, every row of section 1 has its green test on
main, and every row of section 3 reads "green" with no "TO DO" left in it. From then on a force, a coupling or a well is a line in the files, and a run in check
mode is how it is tried.

Every row of this ledger is tried from run files alone: the world file, the universe file and
the start file, run by the one command (`tools/run_inputs.py`), with the engine never rebuilt
for it (the model owner's word of 2026-09-26, 11:45Z). The test of the closing: if trying a
thing needs a line of code, the engine is not closed.
