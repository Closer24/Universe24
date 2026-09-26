# The engine's ledger: what is implemented, what is to do

The model owner's word of 2026-09-26 (11:35Z, in Nature24's session): one place that says
what the engine implements and what is still to do; the engine is closed when everything has
moved to "implemented" and the "to do" column is empty. One item per generic support and per
family attribute; each item names where the support lives and the test that proves it. An item
without a green test stays "to do". The Boss owns the ledger; Nature24 is the second party who
checks each item; The 3 moves an item by landing its build and its test. Read from emitter-click
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
| commit 10, the convergence test | not run | the check-mode table blind with everything on, the rule of three per experiment |
| the hold by flat indices (record 2185) | the hold walks the body's Nodes one by one | the shipped worlds bit for bit, the host time beside |
| a click's held change written after all advances (record 2185) | a read now out of the order of reading (detector_law.py near 3837 and 2845) | the interval's order of 9.91 (8) asserted on a giving world; the digests that move named as GameBoard readings |
| the active box from the real support on every path, or active tiles (record 2185) | one path walks the whole GameBoard | the active path against the plain one bit for bit on the shipped worlds (Nature24's test) |
| records advanced in parallel, merged in identity order (record 2185) | one record after another | the parallel path against the plain one bit for bit on the shipped worlds (Nature24's test) |
| docs/ARCHITECTURE.md naming the running engine (record 2185) | the document names the ray law's modules | the documentation index test |
| a run-time overflow bound on every world (record 2185) | the bound checked at load alone | a world whose integers pass the load and overflow at run time stops with the bound's line |
| no flag, family name, number or version in the code (records 2172 to 2174, 2182) | the review after the merge; today nine identity strings of the form `<name>-v1` in the loader | `tests/test_engine_acceptance.py` tests (e1) to (e4), no mark left on them |

## 3. The one table of primitives (the ledger's section of supports)

The Boss's records 2179 and 2180 of 2026-09-26, on the model owner's question "what is the
generic implementation in the engine for families?": a PRIMITIVE is a kind of attribute the
engine can apply, written once in the code and applied to any family by its kind, never by
its name; an ATTRIBUTE is a family's declared value of a primitive, written in the run's
files, never in the code (HIGHLIGHTS 5.6; ALGEBRA.md 9.110 items 1 and 3). The engine
implements the rule, the click and this closed set of primitives; The 3 supports exactly this
table after the merge; the tests at the end check it. Any experiment is then a change of the
files and a check-mode run; a kind this table lacks is proposed as a new primitive, never written
into a step. The keys are the loader's of emitter-click 01109b05 where a primitive is implemented
and 9.110 item 3's word where it is to do. Every primitive has one place in the interval's
step and one algebraic expression (the Boss's record 2182, the model owner: "each one has a
specific place of use, and its algebraic expression"): the two columns beside the key, the
values and the test. The interval's order of 9.91 (8): (i) the families with clicks step, with
the transport, every component; (ii) the bookings at the Ports, the ladder, the takings and
the givings; (iii) the held families' step; (iv) the holds written, the clicks' changes
included; (v) the bodies on one Node, the feed, the induction, the spin's step, the recoil's
accumulator. The words are the glossary's (HIGHLIGHTS 5.6): a FAMILY is a kind of record
declared in the universe file; a FIELD is one family's levels over the Nodes, the wave, and
nothing else; an ATTRIBUTE is never called a field; a FLAG is a key of the run's files only,
and the engine has no flag and no version. An EXPERIMENT is one world of the check-mode
table with its blind expectation; the word "row" is not used for it, nor for a primitive of this
table or a family's entry (the model owner's word of 2026-09-26, 12:10Z: "rows are the
experiments; say experiment").

| Primitive | Key (a family's entry of universe.json unless said) | Allowed values | Its place in the interval's step (9.91 (8)) | Its algebraic expression, written out | ALGEBRA.md | The test (green today, or to do) |
| --- | --- | --- | --- | --- | --- | --- |
| the pair: the range and the rest rotation of the six-neighbour term | `pair`; a body's or an emitter's `pair` in the world file when the entry says "body" | [num, den], two integers from 1 with den >= num (den = num massless, den > num a range), or the word "body" | the rule's step, (i) for a family with clicks and (iii) for a held family, on every component, from the levels at the interval's start | w a_next + r' = SUM_a R_a (a_{+a} + a_{-a}) + S a_now - w a_before + r - w Sigma_self, 0 <= r' < w, with w = 6 den Gamma^2, R_a = 2 num p_a^2, S = 12 den Gamma^2 - 6 (p_0^2 + Gamma^2)(den - num) - 4 num (p_x^2 + p_y^2 + p_z^2); the inverse the same integers by the ceiling | 9.57 (1), 9.91 (2), (8), 9.85 (3) | green: `tests/test_families_file.py` (the file and the inline list bit for bit; the body's kind where the entry says "body"); `tests/test_engine_acceptance.py` test (f) (three pairs bit for bit against the rule's transcription) |
| the degree: the representation as parts | `parts` | [1], [1, 3] or [1, 3, 6] (degree 0, 1, 2: scalar, vector, tensor) | the rule's step, (i) and (iii): the same line on each component of each part; the hold (iv) with one factor per part | the components 1, 1 + 3, 1 + 3 + 6 in the fixed order t, x, y, z, xx, yy, zz, xy, yz, zx; every component steps by the pair's line; a part that is zero and unheld stays exactly zero (the leak test) | 9.86 (3), 9.88 (7), 9.91 (2) | green: `tests/test_vector_holds.py` (the parts written and inverted; every other part silent at rest); the leak test per part of commit 2 |
| the phase: one level or a pair | `phase` | 1 or 2 | the rule's step, (i): the line on each of the two levels, a_{+a} and a_{-a} the arrivals through the Ports after the transport | phase 1: one level a per component, the neighbours' levels the arrivals; phase 2: the pair (re, im) per component, each stepped by the same line, the arrivals the transported pair; with no twist the second level starting zero stays exactly zero | 9.91 (2), (6), 9.81 (2) | green: `tests/test_families_file.py` |
| the signed read with a twist: a coupling into the pace | `reads`, a list of {`family`, `weight`, `twist`, `by`} | `family` a family's name; `weight` today an integer from 1 or the word "Lambda", after the merge any nonzero integer (positive a hollow, negative a hill); `twist` "own", "Lambda_v" or an integer; `by` "plain" (1) or "sign" ("q") | the pace's read, at the head of (i) and (iii), from the read family's levels at the interval's start; the twist on the Port at the transport of (i) | p_0 = Gamma - SUM over reads of weight x by x (the read family's t level at the Node); p_a = p_0 - SUM over reads of weight x by x (the read family's aa level div 2), the remainder on the reading family's record; by = 1 or q; the guard 0 < p <= Gamma; the twist: k_port = sigma x q x w_V x (A_a here + A_a arrived) on the Port along a, the arrival rotated by k_port through the twist table | 9.91 (2), 9.81 (2) (a), 9.108 (8), 9.110 items 2 and 3 | green for the positive weight: the shipped worlds' digests, `tests/test_engine_acceptance.py` test (a) (the same digests under random names); TO DO for the sign: `tests/test_engine_acceptance.py` test (d), a hill on gravity against the algebra's number (xfail strict today) |
| the hold: a body's count and dipole written at its Nodes | `held`, {`count`, `factors`, `dipole`, `dipole_div`} | `count` "content" or "sign"; `factors` one integer per part; `dipole` "spin" or "moment"; `dipole_div` an integer from 1 | (iv), after the held families' step, at every Node of the body's support, both levels, remainder 0; the clicks' changes of M, Q and n of the same interval included | count s = SUM over the families k the body holds of (M_k x P_0) div P_k, one remainder per family on the body's record (9.111 item 3; P_0 = [1, 1000], M_own = 1000 s P_own, a stock's M its count of givings; at a giving M_k falls by one and s by P_0 / P_k, kept in that family's remainder), or Q for the sign; t: f_0 s; a: (f_1 s n_a) div W; ab: (f_2 s n_a n_b) div W^2 (f the factors, W the wall 3 Q M); the dipole on the six neighbours: component i at the Node + sigma e_j += (sigma x (D x e_j)_i) div dipole_div, D the spin or the moment; the divisions' remainders on the body's record | 9.91 (3), 9.78 (2), 9.85 (2), (7), 9.51 (8), 9.111 item 3 | green: `tests/test_vector_holds.py` (a moving body's vector and tensor parts with the remainders carried; the dipoles written and inverted exactly) |
| the source: a record's count added into a family's level | TO DO: `sourced`, {the records' family, the weight, the scale} on the sourced family's entry; the scale E_s (or the table's cap) an integer of universe.json | the weight a nonzero integer; E_s an integer from 1; s_cap an integer from 1 when the table form is declared | (iv), beside the hold, at the record's Nodes, from the record's count at the interval's start; the inverse subtracts the same integers | level_i += weight x s_i, s_i = F_i div E_s (F_i the record's local count at Node i), or, in the table form, s_i = s_cap F_i div (s_cap E_s + F_i); the remainder on the record; the sourced family then steps by its own pair's line | 9.98 (11) (b), 9.108 (8), (10) (a), 9.110 items 2 and 5 | TO DO: a sourced family's level equals the static response to a held record, in integers (the transcription is `docs/designs/rule_alone/binding_family.py`, source=level and source=table) |
| the clicks: the ladder, the giving, the taking, the recoil | `clicks`, {`gives`, `takes`, `quantum`}; the recoil's store is the click term's `target` (9.110 item 7): the held vector n of a held body, the Port angle accumulators of a sourced body | `gives` and `takes` true or false; `quantum` an integer from 1 | (ii), after the step: the bookings at the detectors' Ports, the ladder, the takings and the givings; the click's writes to M, Q and n enter at the hold (iv) of the same interval, the levels read them from t + 1 | C(t) = C(t - 1) + SUM over the ladder's detectors of the one-way inward flux num (now_i before_j - before_i now_j); theta = (2 u + 1) T div (2 W), u the record's residue; the click at the first t* with C(t*) >= theta, at the Node whose segment of that interval's increment holds theta - C(t* - 1); one quantum: M -= quantum at a giving, += at a taking; sigma_a = sign(the flux booked through the -a face minus through the +a face), the quantum's direction of travel (9.111 item 1); the recoil on a held body: n_a += sigma_a x (W x P_body) div (M x lambda_q); on a sourced body: the Port angle accumulators of its Nodes along a += sigma_a x (k_q div M) in units of theta_unit; the giver with the opposite sign in both; the two the same number (9.111 item 2); the remainders on the body's record | 9.25 (2), (3), 9.91 (4), 9.109 (2), 9.85 (2), 9.111 items 1 and 2 | green: `tests/test_emitter.py` (M excitations give M givings, the quanta conserved), `tests/test_amplitude_click.py` (the offers and the ladder); TO DO for the recoil into the Ports' accumulators: one body keeps its speed across clicks, the ninth question's rerun in the engine (`docs/designs/rule_alone/item9_clicks.py` is the transcription of the bath) |
| the lifetime: the border a family's records click on at an age | `lifetime` | an integer from 1 through the world's `age_bound`; today admitted on the inline list's family only, not on a universe.json entry (the ray law's form) | (ii), with the bookings: a record whose age reaches L at this interval clicks on the border instead of stepping on | age(record) = L implies a click on the border named `lifetime`, booked as a face's escape with the record's whole count; nothing else changes; a lowered pair [num, den] is the short range itself, the lifetime is a border and not a force | 9.88 (3); the border's rule in docs/ENGINE.md | green: `tests/test_lifetime.py` (the escape booked as a face does; the reach on the flight table; the refusals); TO DO: the key admitted on a universe.json entry, or the entry says the border is retired for the lowered pair |
| the internal representation: n pairs with exact rotation tables and the transport | TO DO: `internal`, {n, the generators' tables} | n an integer from 1; every generator an exact triple or quadruple of the twist table | (i), the transport: a neighbour's n pairs rotated on the Port as they arrive, before the step reads them; the inverse per Node from the arrival and the remainders | per pair and per generator on the Port, the plane rotation T d + rho' = c re - s im + rho with (c, s, d) the exact triple (c^2 + s^2 = d^2) and rho the running remainder, the quaternion rotation for a quadruple; the transport composes the generators along the Link; a loop of Links returns every pair to itself | 9.88 (7) (i), (1), 9.81 (2) (c), (d), 9.96 (2), 9.99 (6) | draft green: `tests/test_primitives.py` (the identities and the exact product; the transport composes and inverts per Node; the loader's hook refuses the rest); TO DO: the attribute on the entry and the hook in the loader, then a family of n pairs transported around a loop returns to itself |
| the clicks list: several products of one click and the momenta's share | TO DO: `clicks` takes a list of givings, each {`family`, `count`, `sign`}, beside `gives`, `takes`, `quantum` | every product a family's name with an integer count from 1; the conserved integers of the products sum to the taken quantum's or the loader refuses | (ii), at a giving: one click, several given records, each into its family's ladder; the shares booked before the hold (iv) | SUM over products of (count x sign, the charge, the internal numbers) = the taken quantum's, checked at load; the four-momentum shared whole: the shares are the record's residue on its own wheel scaled to W, sorted, each product's share a whole number and the sum exact, the leftover on the giver's record | 9.88 (4), (7) (iii), 9.99 (6) | draft green: `tests/test_primitives.py` (the list balances the conserved integers or refuses; the momenta shared whole with the sum exact); TO DO: the attribute on the entry, then a body giving into two families at its period gives the counts in the declared ratio |
| the hand: the helicity sign a click takes or gives | TO DO: `hand` on a giving of the clicks list, or on a body's click | -1, 0 (none) or 1 | (ii), at the click's admission on a body, before the ladder books it; a wave has no hand and the check does not run on it | h = sign(S . n), S the body's spin and n its momentum's whole part, an integer in {-1, 0, 1}; a click declaring h admits a body with that sign only, refused by name otherwise | 9.88 (5), (7) (iv) | draft green: `tests/test_primitives.py` (the helicity's sign and its admission); TO DO: the attribute on the entry, then a click with a declared hand refused on a body of the other hand |
| the self-source as an integer polynomial with a structure table | `self_source` {`unit`} today; TO DO the structure table on the same object, terms [degree, weight, table] | `unit` an integer from 0 (0 off); the table the family's constants, integers, degree two and three | (i) and (iii), off the step's right side of the pair's line, from the levels at the interval's start | Sigma_self = (SUM over the six Links of SUM over the components (a_j - a_i)^2) div P_2, P_2 the unit, 0 when P_2 = 0; with the table the terms of degree two (f_abc x a component x a difference) and three (f f a a a) added under the same div, the remainder on the family's record | 9.78 (3), 9.88 (2), (7) (ii), 9.91 (5) | green for the unit: the shipped worlds' digests; TO DO for the table: waits for the mathematician's line, then two colour sources under a self-coupled family at a large unit and the field's energy between them read against the algebra's number |

THE RUN'S DECLARATIONS, of the world file and the start file and not of a family (the
mathematician's 9.111 item 5: three lines the table lacked; what is today a line of Nature24's
checking code becomes a key of the run's files):

| Declaration | Key (world file unless said) | Allowed values | Where the run reads it | ALGEBRA.md | The test |
| --- | --- | --- | --- | --- | --- |
| the run's words: the start, the faces, the length, the seed | TO DO: `start` (the stationary state at the pace: the record's mode and the fields' static levels iterated together), `faces` (closed, periodic or absorbing), the run's length, `seed`; `mode` in the start file today | `start` "stationary" or "loaded"; `faces` one of the three words per axis; the length and the seed integers | at load, before the first interval | 9.108 item 12 (ii), (iii), 9.90 (6) | TO DO: a world started "stationary" rings below 5 percent at the peak over 300 intervals; a world with absorbing faces returns no transient |
| the readings a world file declares and the run writes, each labelled a GameBoard reading | TO DO: `readings`, a list of {kind, where, when}: a level's amplitude at a Node over intervals, a body's centre against a well's centre, the band-averaged speed of a body, the exact K reading as the neighbours' phase difference and the flux click half a Link ahead, the host cost beside | every reading one of the kinds above, by name, on declared Nodes and intervals | after the interval, read only, written to the run's output under its label | 9.108 item 12, 9.109 items 3 and 4, docs/ENGINE.md (the readings by type) | TO DO: every reading of docs/designs/rule_alone/ reproduced from a world file with no line of code |
| the residue keys of every run | the keys table of 9.90 (6): a key read and not in the table, or in the table and never read, fails | the shipped worlds' `law`, `model_id`, `engine`, `K`, `N`, `release`, `width`, `age_bound`, `clock_stamp` gone | at load | 9.90 (6), 9.107 item 6 (b) | TO DO: the walking test of the keys table; `tests/test_engine_acceptance.py` test (e3) |

THE OUTPUT IS A DECLARATION TOO (the model owner's word of 2026-09-26, 12:20Z: "how is the
experiment's output made fully generic: how the clicks are counted, at which Node, whatever each
one asks to be written in the output; the output is generic, the input is generic, and the
engine implements what is between them"). The run writes nothing of its own choosing: every
line of the output is a reading the world file declares (the `readings` declaration above: the
detector's clicks with their Node and interval, a body's centre, a level at a Node, a count on
a face), each labelled by its kind (DETECTOR, GAMEBOARD, HOST), in one format for every
experiment; the engine knows no experiment's name and no reading's purpose. The visualizer
renders the output file alone, never the engine's state: "what the visualizer does is make the
output runnable on a screen" (the owner, the same word); a new display is a reader of the
output, not a line of the engine.

THE TERM FORM behind the table (the mathematician's 9.110 item 7): a family is a shape and a
list of terms [kind, target, of, degree, weight, table], the kind one of four (READ, SOURCE,
HOLD, CLICK); the shape is `parts`, `phase`, `pair` and the internal representation
(primitives 1, 2, 3, 9); every other primitive is a term of one of the four kinds. What stays
code, said honestly: a fifth kind and a new shape; the closing test is that no experiment of
the check-mode table needs either.

Not a primitive but a rule of the engine: THE REMAINDERS. Every division of every primitive keeps
its remainder on the dividing family's record at the Node (the hold's, the read's, the
source's, the recoil's, the transport's), carried between intervals and inverted with the
step; nothing else is kept at a Node; every intermediate a bounded integer (9.91 (2), (3),
9.109 (2) (b); the local integer operation contract of docs/ARCHITECTURE.md). The model owner's
word of 2026-09-26 (12:00Z, in Nature24's session): "behaviour with remainders where needed;
everything only in whole numbers".

Not a primitive but a rule of the engine: THE PACE'S GUARD ON BOTH SIDES. Every pace stays in
0 < p <= Gamma at run time, for every family and every axis, whatever the reads and the
sources declare (9.110 item 2; 9.108 items 11 and 12; docs/designs/rule_alone/README.md
section 10: above about 1.25 Gamma the step is unstable). Today the guard is the load's alone,
from below (`reach >= node_clock` refused); the run-time guard on both sides is the to-do item
of section 2 and stops the run with the guard's line, never a flag.

Not primitives either: the integers of the universe (`node_clock`, `amplitude_bound`, `Lambda`,
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
(primitives 4 and 6; 9.108). The strong force as colour: a family with the internal representation
n = 3 or 8 and a structure table on its self-source, the clicks list refusing a coloured
product alone (primitives 9, 10, 12). The weak force: a massive vector family (parts [1, 3], a
lowered pair) with a clicks list of several products and a hand (primitives 1, 2, 10, 11). A decay:
a body giving into several families at its period (primitive 10). No primitive names a force; a force
that needs a thirteenth kind is a new primitive, proposed before it is written.

THE EXPERIMENT'S TOOLS ARE DECLARATIONS TOO, and each is tested alone (the model owner's word
of 2026-09-26, 12:00Z: "the engine does not know what you built in the experiment; you compose
it generically; the crystal can be tested alone, a detector alone, everything alone, not all
together at large"). A crystal, a polariser, a detector, a screen, a counter, an emitter and
a receiver are bodies of the world file with their keys (9.110 item 4; the detectors' rule of
9.92); a tool's test is one world with the tool alone and its one reading; the shipped
experiment is the composition, run in check mode, and owes no test of its own beyond the
composition's digest. The engine's own tests are the primitives above, one small test per primitive.

## 4. The closing condition

The engine is closed when section 2 is empty, every item of section 1 has its green test on
main, and every primitive of section 3 reads "green" with no "TO DO" left in it. From then on a force, a coupling or a well is a line in the files, and a run in check
mode is how it is tried.

Every item of this ledger is tried from run files alone: the world file, the universe file and
the start file, run by the one command (`tools/run_inputs.py`), with the engine never rebuilt
for it (the model owner's word of 2026-09-26, 11:45Z). The test of the closing: if trying a
thing needs a line of code, the engine is not closed.
