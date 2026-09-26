# The engine's ledger: what is implemented, what is to do

The model owner's word of 2026-09-26 (11:35Z, in Nature24's session): one place that says
what the engine implements and what is still to do; the engine is closed when everything has
moved to "implemented" and the "to do" column is empty. One item per generic support and per
family attribute; each item names where the support lives and the test that proves it. An item
without a green test stays "to do". The Boss owns the ledger; Nature24 is the second party who
checks each item; Main Loop moves an item by landing its build and its test. Read from emitter-click
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
implements the rule, the click and this closed set of primitives; Main Loop (The 3 until record 2186, Coder 3 until record 2209) supports exactly this
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

| Primitive | Key (a family's entry of universe.json unless said) | Allowed values | Its place in the interval's step (9.91 (8)) | Its algebraic expression, written out | ALGEBRA.md | The test (green today, or to do) | From the rule, or beyond the rule (record 2188) |
| --- | --- | --- | --- | --- | --- | --- | --- |
| the pair: the range and the rest rotation of the six-neighbour term | `pair`; a body's or an emitter's `pair` in the world file when the entry says "body" | [num, den], two integers from 1 with den >= num (den = num massless, den > num a range), or the word "body" | the rule's step, (i) for a family with clicks and (iii) for a held family, on every component, from the levels at the interval's start | w a_next + r' = SUM_a R_a (a_{+a} + a_{-a}) + S a_now - w a_before + r - w Sigma_self, 0 <= r' < w, with w = 6 den Gamma^2, R_a = 2 num p_a^2, S = 12 den Gamma^2 - 6 (p_0^2 + Gamma^2)(den - num) - 4 num (p_x^2 + p_y^2 + p_z^2); the inverse the same integers by the ceiling | 9.57 (1), 9.91 (2), (8), 9.85 (3) | green: `tests/test_families_file.py` (the file and the inline list bit for bit; the body's kind where the entry says "body"); `tests/test_engine_acceptance.py` test (f) (three pairs bit for bit against the rule's transcription) | from the rule: its two coefficients |
| the degree: the representation as parts | `parts` | [1], [1, 3] or [1, 3, 6] (degree 0, 1, 2: scalar, vector, tensor) | the rule's step, (i) and (iii): the same line on each component of each part; the hold (iv) with one factor per part | the components 1, 1 + 3, 1 + 3 + 6 in the fixed order t, x, y, z, xx, yy, zz, xy, yz, zx; every component steps by the pair's line; a part that is zero and unheld stays exactly zero (the leak test) | 9.86 (3), 9.88 (7), 9.91 (2) | green: `tests/test_vector_holds.py` (the parts written and inverted; every other part silent at rest); the leak test per part of commit 2 | from the rule: the same line per component |
| the phase: one level or a pair | `phase` | 1 or 2 | the rule's step, (i): the line on each of the two levels, a_{+a} and a_{-a} the arrivals through the Ports after the transport | phase 1: one level a per component, the neighbours' levels the arrivals; phase 2: the pair (re, im) per component, each stepped by the same line, the arrivals the transported pair; with no twist the second level starting zero stays exactly zero | 9.91 (2), (6), 9.81 (2) | green: `tests/test_families_file.py` | from the rule: the line on each level of the pair |
| the signed read with a twist: a coupling into the pace | `reads`, a list of {`family`, `weight`, `twist`, `by`} | `family` a family's name; `weight` today an integer from 1 or the word "Lambda", after the merge any nonzero integer (positive a hollow, negative a hill); `twist` "own", "Lambda_v" or an integer; `by` "plain" (1) or "sign" ("q") | the pace's read, at the head of (i) and (iii), from the read family's levels at the interval's start; the twist on the Port at the transport of (i) | p_0 = Gamma - SUM over reads of weight x by x (the read family's t level at the Node); p_a = p_0 - SUM over reads of weight x by x (the read family's aa level div 2), the remainder on the reading family's record; by = 1 or q; the guard 0 < p <= Gamma; the twist: k_port = sigma x q x w_V x (A_a here + A_a arrived) on the Port along a, the arrival rotated by k_port through the twist table | 9.91 (2), 9.81 (2) (a), 9.108 (8), 9.110 items 2 and 3 | green for the positive weight: the shipped worlds' digests, `tests/test_engine_acceptance.py` test (a) (the same digests under random names); TO DO for the sign: `tests/test_engine_acceptance.py` test (d), a hill on gravity against the algebra's number (xfail strict today) | from the rule: the pace is the rule's own p; the sign a declaration |
| the hold: a body's count and dipole written at its Nodes | `held`, {`count`, `factors`, `dipole`, `dipole_div`} | `count` "content" or "sign"; `factors` one integer per part; `dipole` "spin" or "moment"; `dipole_div` an integer from 1 | (iv), after the held families' step, at every Node of the body's support, both levels, remainder 0; the clicks' changes of M, Q and n of the same interval included | count s = SUM over the families k the body holds of (M_k x P_0) div P_k, one remainder per family on the body's record (9.111 item 3; P_0 = [1, 1000], M_own = 1000 s P_own, a stock's M its count of givings; at a giving M_k falls by one and s by P_0 / P_k, kept in that family's remainder), or Q for the sign; t: f_0 s; a: (f_1 s n_a) div W; ab: (f_2 s n_a n_b) div W^2 (f the factors, W the wall 3 Q M); the dipole on the six neighbours: component i at the Node + sigma e_j += (sigma x (D x e_j)_i) div dipole_div, D the spin or the moment; the divisions' remainders on the body's record | 9.91 (3), 9.78 (2), 9.85 (2), (7), 9.51 (8), 9.111 item 3 | green: `tests/test_vector_holds.py` (a moving body's vector and tensor parts with the remainders carried; the dipoles written and inverted exactly) | the writes from the rule's hold (9.78 (2)); THE WELL THAT HOLDS A BODY'S NODES TOGETHER IS BEYOND THE RULE (record 2188 (3)): kept as the body's declaration, studied by the binding family's runs |
| the source: a record's count added into a family's level | TO DO: `sourced`, {the records' family, the weight, the scale} on the sourced family's entry; the scale E_s (or the table's cap) an integer of universe.json | the weight a nonzero integer; E_s an integer from 1; s_cap an integer from 1 when the table form is declared | (iv), beside the hold, at the record's Nodes, from the record's count at the interval's start; the inverse subtracts the same integers | level_i += weight x s_i, s_i = F_i div E_s (F_i the record's local count at Node i), or, in the table form, s_i = s_cap F_i div (s_cap E_s + F_i); the remainder on the record; the sourced family then steps by its own pair's line | 9.98 (11) (b), 9.108 (8), (10) (a), 9.110 items 2 and 5 | the run files `examples/events/source/` (two worlds, at rest and moving, the plain count and the table as two sourced families in the one universe, the static response beside each; Nature24, record 2217) and `tests/test_source_worlds.py`; the function `src/event_universe/features/source/` with its small test `tests/test_feature_source.py` (the line, the carried remainder, the table, the inverse, the refusals, the hand identity, the run file's counts); TO DO with the loop's call (cut 3): a sourced family's level equals the static response to the record's count, in integers | from the rule: a term added into a level; the saturating table a declaration |
| the clicks: the ladder, the giving, the taking, the recoil | `clicks`, {`gives`, `takes`, `quantum`}; the recoil's store is the click term's `target` (9.110 item 7): the held vector n of a held body, the Port angle accumulators of a sourced body | `gives` and `takes` true or false; `quantum` an integer from 1 | (ii), after the step: the bookings at the detectors' Ports, the ladder, the takings and the givings; the click's writes to M, Q and n enter at the hold (iv) of the same interval, the levels read them from t + 1 | C(t) = C(t - 1) + SUM over the ladder's detectors of the one-way inward flux num (now_i before_j - before_i now_j); theta = (2 u + 1) T div (2 W), u the record's residue; the click at the first t* with C(t*) >= theta, at the Node whose segment of that interval's increment holds theta - C(t* - 1); one quantum: M -= quantum at a giving, += at a taking; sigma_a = sign(the flux booked through the -a face minus through the +a face), the quantum's direction of travel (9.111 item 1); the recoil on a held body: n_a += sigma_a x (W x P_body) div (M x lambda_q); on a sourced body: the Port angle accumulators of its Nodes along a += sigma_a x (k_q div M) in units of theta_unit; the giver with the opposite sign in both; the two the same number (9.111 item 2); the remainders on the body's record | 9.25 (2), (3), 9.91 (4), 9.109 (2), 9.85 (2), 9.111 items 1 and 2 | green: `tests/test_emitter.py` (M excitations give M givings, the quanta conserved), `tests/test_amplitude_click.py` (the offers and the ladder); TO DO for the recoil into the Ports' accumulators: one body keeps its speed across clicks, the ninth question's rerun in the engine (`docs/designs/rule_alone/item9_clicks.py` is the transcription of the bath) | the ladder from the click (9.25); THE STORE OF A CLICK'S RECOIL BELOW ONE INTEGER IS BEYOND THE RULE (record 2188 (3)): the Port accumulator as its declaration, studied by the ninth question's rerun |
| the lifetime: the border a family's records click on at an age | `lifetime` | an integer from 1 through the world's `age_bound`; today admitted on the inline list's family only, not on a universe.json entry (the ray law's form) | (ii), with the bookings: a record whose age reaches L at this interval clicks on the border instead of stepping on | age(record) = L implies a click on the border named `lifetime`, booked as a face's escape with the record's whole count; nothing else changes; a lowered pair [num, den] is the short range itself, the lifetime is a border and not a force | 9.88 (3); the border's rule in docs/ENGINE.md | green: `tests/test_lifetime.py` (the escape booked as a face does; the reach on the flight table; the refusals); TO DO: the key admitted on a universe.json entry, or the entry says the border is retired for the lowered pair | beyond the rule: a declared border, not a force (the short range itself is from the rule, the lowered pair) |
| the internal representation: n pairs with exact rotation tables and the transport | TO DO: `internal`, {n, the generators' tables} | n an integer from 1; every generator an exact triple or quadruple of the twist table | (i), the transport: a neighbour's n pairs rotated on the Port as they arrive, before the step reads them; the inverse per Node from the arrival and the remainders | per pair and per generator on the Port, the plane rotation T d + rho' = c re - s im + rho with (c, s, d) the exact triple (c^2 + s^2 = d^2) and rho the running remainder, the quaternion rotation for a quadruple; the transport composes the generators along the Link; a loop of Links returns every pair to itself | 9.88 (7) (i), (1), 9.81 (2) (c), (d), 9.96 (2), 9.99 (6) | draft green: `tests/test_primitives.py` (the identities and the exact product; the transport composes and inverts per Node; the loader's hook refuses the rest); TO DO: the attribute on the entry and the hook in the loader, then a family of n pairs transported around a loop returns to itself | the transport from the rule's rotation (9.81 (2)); THE TWIST TABLE'S PRECISION IS BEYOND THE RULE (record 2188 (3)): the table a declaration, studied by the loop run |
| the clicks list: several products of one click and the momenta's share | TO DO: `clicks` takes a list of givings, each {`family`, `count`, `sign`}, beside `gives`, `takes`, `quantum` | every product a family's name with an integer count from 1; the conserved integers of the products sum to the taken quantum's or the loader refuses | (ii), at a giving: one click, several given records, each into its family's ladder; the shares booked before the hold (iv) | SUM over products of (count x sign, the charge, the internal numbers) = the taken quantum's, checked at load; the four-momentum shared whole: the shares are the record's residue on its own wheel scaled to W, sorted, each product's share a whole number and the sum exact, the leftover on the giver's record | 9.88 (4), (7) (iii), 9.99 (6) | draft green: `tests/test_primitives.py` (the list balances the conserved integers or refuses; the momenta shared whole with the sum exact); TO DO: the attribute on the entry, then a body giving into two families at its period gives the counts in the declared ratio | the click: the products a declaration, the share by the record's residue |
| the hand: the helicity sign a click takes or gives | TO DO: `hand` on a giving of the clicks list, or on a body's click | -1, 0 (none) or 1 | (ii), at the click's admission on a body, before the ladder books it; a wave has no hand and the check does not run on it | h = sign(S . n), S the body's spin and n its momentum's whole part, an integer in {-1, 0, 1}; a click declaring h admits a body with that sign only, refused by name otherwise | 9.88 (5), (7) (iv) | draft green: `tests/test_primitives.py` (the helicity's sign and its admission); TO DO: the attribute on the entry, then a click with a declared hand refused on a body of the other hand | beyond the rule: a declared admission at the click; a wave has none |
| the self-source as an integer polynomial with a structure table | `self_source` {`unit`} today; TO DO the structure table on the same object, terms [degree, weight, table] | `unit` an integer from 0 (0 off); the table the family's constants, integers, degree two and three | (i) and (iii), off the step's right side of the pair's line, from the levels at the interval's start | Sigma_self = (SUM over the six Links of SUM over the components (a_j - a_i)^2) div P_2, P_2 the unit, 0 when P_2 = 0; with the table the terms of degree two (f_abc x a component x a difference) and three (f f a a a) added under the same div, the remainder on the family's record | 9.78 (3), 9.88 (2), (7) (ii), 9.91 (5) | green for the unit: the shipped worlds' digests; TO DO for the table: waits for the mathematician's line, then two colour sources under a self-coupled family at a large unit and the field's energy between them read against the algebra's number | from the rule: a term off the step's right side; the structure table a declaration |
| the Port's send: what a Node puts on each of its six Ports at the interval's start | TO DO: `step` {`send`} in universe.json (one step for every family) | the components sent by name: the level now (phase 1), the pair (phase 2), the Port angle accumulator | the head of (i) and (iii), before any read: the interval's start values, the previous step's output, never a value written in the same interval | on the Port +a of Node i: send_{+a}(i) = (a_i(t), and for phase 2 its pair, and rho_{+a}(i)); the same on -a; one send per Port per interval | 9.57 (1) (the order of reading), 9.91 (8), 9.96 (2) (e) | TO DO: the trace of every Node's six sends equals its level at the interval's start on every shipped world | from the rule: the neighbours' levels at the interval's start |
| the Port's receive: what a Node takes in through each Port | TO DO: `step` {`receive`} | "plain" (the neighbour's send as it is) or "rotated" (the send turned by the Port's accumulated angle through the twist table) | (i): the arrivals a_{+a} and a_{-a} of the step's line; the transport of 9.91 (6) | arrival_{+a}(i) = T(rho_{+a}(i) + rho_{-a}(i + e_a)) send_{-a}(i + e_a): the neighbour's send rotated by the Link's angle; with no twist the identity, the neighbour's level itself | 9.81 (2), 9.91 (2), (6) | TO DO: the arrivals equal the neighbours' sends of the same interval, one Link per interval, on the shipped worlds; with a twist, the rotation exact by the triple | from the rule: one Link per interval and nothing in zero time (9.57 (1)); the rotation the rule's transport |
| the Port's wait: how many intervals a send waits on the Link before it is received | TO DO: `step` {`wait`} | an integer from 1; 1 is today's engine | between the send and the receive; a wait of w holds w sends on the Link | received at interval t: the send of interval t - wait; wait = 1: the previous step's output, as 9.57 (1) says | 9.57 (1) ("one Link per interval"), 9.91 (8) | TO DO: wait 1 bit for bit with today's shipped worlds; wait 2 halves the speed of the free wave (a diagnostic run, the number beside) | from the rule at wait 1; another wait is a declaration beyond it, studied |
| the operation on a Port: the verb applied to the six arrivals and the Node's own integers | TO DO: `step` {`operation`} with its coefficients as declared integers | the sum with declared weights, the division by the declared wall with the remainder kept, the rotation by a triple, the comparison at the ladder: the verbs on the state vector, no root, no float | (i) and (iii): the step's line at every Node, every component | w a_next + r' = SUM_a R_a (arrival_{+a} + arrival_{-a}) + S a_now - w a_before + r - w Sigma_self, 0 <= r' < w, the coefficients R_a, S, w from the pair and the paces (primitive 1) | 9.57 (1), 9.91 (2) | green for the one operation of today: `tests/test_engine_acceptance.py` test (f) bit for bit against the rule's transcription; TO DO: the operation read from the files | from the rule: the rule is this operation |
| the trace: one line on the side when a primitive acts | TO DO: `trace` in the start file: {primitives by name, Nodes, Ports, intervals}; nothing traced unless the files ask | a list of primitive names from this table; Nodes and intervals as ranges; "ports" true or false | beside every primitive when it acts, after its write; it only reads | one line per act: (interval, Node, Port, primitive, the integers read, the integers written, the remainder kept); a GameBoard reading labelled a diagnostic, never read back by the engine | record 2187; docs/ENGINE.md (the readings by type) | TO DO: a traced run bit for bit the untraced one (the same digests) on every shipped world; the trace's lines equal the step's integers at three declared Nodes | not physics: a reading; it changes no integer of the run |

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

THE PINS, OUTSIDE THE CODE (the model owner's word of 2026-09-26, 12:25Z: "after the engine is
closed and checked and everything plays exactly as we want, think already now how we add the
pins fully generically; the pins will not be in the code, the pins will be outside the code").
Nature24's design, for the Boss's word; nothing of it runs before the Go:

| Piece | What it is | Where it lives |
| --- | --- | --- |
| a pin | one declared expectation on one declared reading: {reading (the name of a `readings` line of the world file), nature's value with its uncertainty and its source, the unit line that turns nature's number into the GameBoard's (Gamma and the Link, from universe.json), the comparison kind (an interval, a ratio within a fraction, a direction, the rule of three), the ALGEBRA.md section of the formula} | a pins file beside the world file, `<world>.pins.json`; never a line of the engine, never a key the loader reads |
| the reader | one generic program that takes a run's output and a pins file and writes the table (expected, read, direction, verdict), knowing reading kinds and comparison kinds and no experiment's name | `tools/`, outside `src/event_universe`; the engine never imports it |
| the rule of kinds | a pin is on a DETECTOR reading alone (a click, a record's moments, an external thing's reading); a pin on a GameBoard reading is refused by the reader with the reason | the reader's one refusal |
| blindness | the run is written first and stamps the world, the universe and the start file; the pins file is read after and stamped in the verdict table; a run cannot depend on it | the reader's stamp |
| the modes | `mode` "check" in the start file: the runner refuses a pins file as today (`tests/test_engine_start.py`); after the Go a second mode names the pins file, and the same reader writes the verdicts | the start file, the reader |
| the old registers | every pin retired by name (records 2172 to 2174) and every expectations register of the ray law's tools become a pins file in this form or stay history; none returns through code | the pins files |

A new pin is a line in a pins file; a new comparison kind is a line of the reader, not of the
engine; the engine is closed the same day with or without pins.

THE PHYSICIST'S RUNS AS RUN FILES (the model owner's word of 2026-09-26, 12:40Z: "all the
experiments you make on the well, a low ceiling, a high ceiling, all those things: make sure you
can do them afterwards from the generic engine simply, and from there ask for attributes; what
you need for your games you do not do in your local code, the engine supports them; after this
you write no code, you run the engine; make sure you have the attributes you need: input,
output, visualizer"). Every knob of the checking code in docs/designs/rule_alone/ mapped to its
declaration; a knob with no home is a to-do item for Main Loop, never a line of the physicist's
code again:

| The knob of my runs | Its declaration in the run's files | State |
| --- | --- | --- |
| a record at rest, moving at v, or two records (`rest`, `moving`, `pair`; `v=`) | bodies of the world file: `position`, `family`, `amount`, `momentum`; two entries for the pair; a record without `fixed` moves by the rule | the keys exist; the free body by the rule is the to-do item of section 2 |
| the record's width (`side=`) and the start's shape | the body's extents and `start` (a Gaussian or the stationary mode) | the extents exist; `start` is the run's declaration above, to do |
| the weights of the hollow and the hill (`km=`, `kr=`) | the `reads` of the matter family, signed (primitive 4) | the sign to do |
| the well's two families, [1000, 1019] and [1000, 1181] | two entries of universe.json with their pairs, parts [1], phase 1 | exists |
| the source's form and scale (`source=level|count|cap|table`, `scap=`, `floor=`, E_s) | the `sourced` primitive with its scale E_s and its table's cap in universe.json (primitive 6) | the run files exist (`examples/events/source/`: the scale and the cap declared, the readings declared); the primitive to do |
| the fields at the pace or plain (`pace=`) | the field families' own `reads` (a field at the pace reads what the matter reads) | exists as a read |
| the board's size and its faces (`n=`, `wrap=`, `sponge=`) | the world's shape; `faces` closed, periodic or absorbing; an absorbing face is the face detector of the engine (`face:+x` .. `face:-z`), so the sponge is not needed there | the shape and the face detectors exist; `faces` as one word to do |
| the stationary start (`passes=`) | `start` "stationary": the record's mode and the fields' levels iterated at the pace (the run's declaration) | to do |
| the pace bounded on both sides, the cut Nodes counted | the engine's rule of the guard and a GameBoard reading of the cut Nodes | to do (section 2) |
| the run's length (`t=`) and the readings' cadence (`EVERY`) | the run's length and the `readings` intervals | to do (the run's declaration) |
| the readings: the centroid, the rms width, the peak and its Node, the count's sum and peak, the content at the peak, the rotation, the bound share, the tail, the record's form, a field's form, the ringing at a Node per window, the coupling and the total | the `readings` declaration, by kind: a body's centre and rms; a level and a count at a Node over intervals; a family's form (GameBoard); a window's amplitude at a Node; the conserved total | to do: these kinds join the `readings` line above |
| the every-Node detector bath and the momentum-keeping click (item9_clicks.py, item9_pair.py, item9_many.py) | detectors as bodies on every Node of a region; the click's recoil (primitive 7); a body of M records as `amount` M | the detectors exist; the recoil to do |
| the emitter, the receivers and the click counts (item8_rate_worlds.py) | the emitter body, receiver bodies, the face detectors, the clicks in the output | exists: these worlds already ran in the engine |
| a free packet's speed against its rms (packet_speed.py) | a body with `momentum` and the centre reading | exists but for the reading |
| the visualizer | a reader of the output's declared readings: a body's centre over intervals, a level at a Node, the clicks by Node and interval | to do, outside the engine |

When every line of this table reads "exists", docs/designs/rule_alone/ is history, every run
of it is a world file under examples/events/ with universe.json and the start file, and the
physicist writes no code: the run files, the small tests and the acceptance tests only (records
2187, 2190).

THE REGISTER (the Boss's records 2211 and 2212, the model owner's decision of 2026-09-26): a
primitive's identity is its unique English name, the key of this table, never a number; the
engine keeps one register of primitives and refuses a name twice at load; every primitive
declares what it reads, what it writes and its place in the step; the loop refuses two writers
of one value at one place unless their order is declared. Main Loop builds the register into
the one interface of a primitive before the cut; until then the finder's rule (skills/workflow.md
point 11) is not in force. The columns the register adds to every primitive:

| Primitive (its name) | Reads | Writes | Who works on it now |
| --- | --- | --- | --- |
| pair | the family's pair and the four paces at the Node | the next level and the remainder of every component (with the operation) | Main Loop (the loop) |
| degree | `parts` | which components exist and step | Main Loop (the loop) |
| phase | `phase` | the one level or the two levels of the pair | Main Loop (the loop) |
| signed read | the read families' t and aa levels at the Node at the interval's start | the four paces and the read's remainder on the reading family's record | Main Loop (the loader's sign; the read itself stands) |
| hold | the body's count, its held vector n, its spin or moment | the held family's levels at the body's Nodes and the dipole's writes at the six neighbours; the divisions' remainders on the body's record | stands; the count per family (9.111 item 3) Main Loop |
| source | the record's local count D_i at the end of its step (9.108 item 13) | the sourced family's level at the record's Nodes; the remainder on the record | Nature24 (record 2217): the run files (`examples/events/source/`) and the function (`features/source/`, `apply` with its inverse) built; the loop's call and the loader's word `sourced` are Main Loop's cut |
| clicks | the inward flux at the detector's Ports, the ladder, u, T, W | the counts M of taker and giver, the click line, the Port accumulators or the held n (the recoil) | Main Loop (the recoil, 9.111 item 2) |
| lifetime | a record's age | the border click, booked as an escape | stands (the ray law's form); its entry key unassigned |
| internal representation | the neighbour's n pairs and the Port's accumulated angle | the arrivals of the step (a value of the interval, kept at no Node) | unassigned |
| clicks list | the taken quantum's conserved integers, the record's residue | the products' records and their shares | unassigned |
| hand | the body's spin and momentum | the admission or the refusal of the click | unassigned |
| self-source | the six neighbours' components | the self term off the step's right side; the remainder on the family's record | Main Loop for the unit (stands); the table waits for the mathematician |
| send | the level, the pair, the accumulator at the interval's start | the six Ports' sends | Main Loop (the loop, record 2186) |
| receive | the neighbours' sends and the Port's accumulator | the six arrivals | Main Loop (the loop) |
| wait | the send of interval t - wait | nothing | Main Loop (the loop) |
| operation | the arrivals, the level now, the level before, the remainder, the coefficients | the next level and the remainder | Main Loop (the loop) |
| trace | whatever the files name | the trace file alone; no value of the run | Main Loop (the interface) |

THE ONE COLLISION KNOWN TODAY: the hold and the source both write a family's level at a Node
in (iv); a family both held and sourced at one Node is refused at load unless the order is
declared, and today no family is both (the hold's families and the sourced families are
distinct entries).

THE TERM FORM behind the table (the mathematician's 9.110 item 7): a family is a shape and a
list of terms [kind, target, of, degree, weight, table], the kind one of four (READ, SOURCE,
HOLD, CLICK); the shape is `parts`, `phase`, `pair` and the internal representation
(primitives 1, 2, 3, 9); every other primitive is a term of one of the four kinds. What stays
code, said honestly: a fifth kind and a new shape; the closing test is that no experiment of
the check-mode table needs either.

THE RULE 9.57 (1) READ AS THE FILES' DECLARATION OF THE STEP, in one line (the model owner's
word of record 2186: "the run file defines what a step is; that is exactly the idea of
locality"): send = every family's level (and pair) at the interval's start on all six Ports;
wait = 1; receive = the neighbour's send rotated by the Port's accumulator (the identity with no
twist); operation = the weighted sum of the six arrivals with R_a = 2 num p_a^2, plus S a_now,
minus w a_before, plus the remainder, divided by w = 6 den Gamma^2 with the remainder kept, and
the self-source's term off the right side. Four declarations and the primitives' coefficients;
no line of code names a family, a force or a number.

THE ROLES (record 2187, the model owner's decision): Main Loop alone writes the engine's code;
the mathematician writes one algebraic line per primitive and gates each build; Nature24 writes
the run's files, the small tests and the acceptance tests, runs the engine and checks each item
on main; the Boss owns the ledger and the records; everyone runs the engine locally and debugs
with the trace, only Main Loop changes it.

BEYOND THE RULE, THE STUDY RUNS (record 2188: "whatever can be built with the rule, let it be
built with the rule; whatever cannot, let it not be forced, and we will see what happens
there"): three pieces today, each kept as its own declaration under its own name and studied:
(1) the well that holds a body's Nodes together: the study is the binding family's runs
(9.108; docs/designs/rule_alone/binding_family.py; the sourced rerun with the four corrections
of 9.108 item 12 running on 2026-09-26): does the rule's own family hold the body, and what
rings; (2) the store of a click's recoil below one integer: the study is the ninth question's
rerun with the momentum-keeping click (9.109 item 3; item9_clicks.py with the label carry as
the store): does one body keep its speed and what walks; (3) the twist table's precision: the
study is a loop run, a phase-2 pair carried around a closed loop of Links under the fine table
(all identities) and under the exact triples, the return error per Link read (to run; the
exact product is tested in tests/test_primitives.py). The mathematician says why the rule does
not give each piece; Nature24 runs what happens there; the ledger marks each in the eighth
column.

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

THE ORDER OF THE DAY (the model owner's word of 2026-09-26, 12:50Z): the hard questions (the
eighth question of record 2140, the well's study runs, the open items of record 2134) are set
aside until a generic engine stands; now the three work on the generic engine alone and help
Main Loop build it; no one but Main Loop writes code. The physicist's part until then: this ledger's
tests and run files, the checks of each item on main, the answers to Main Loop's questions from
the runs already made.

## 4. The closing condition

The engine is closed when section 2 is empty, every item of section 1 has its green test on
main, and every primitive of section 3 reads "green" with no "TO DO" left in it. From then on a force, a coupling or a well is a line in the files, and a run in check
mode is how it is tried.

Every item of this ledger is tried from run files alone: the world file, the universe file and
the start file, run by the one command (`tools/run_inputs.py`), with the engine never rebuilt
for it (the model owner's word of 2026-09-26, 11:45Z). The test of the closing: if trying a
thing needs a line of code, the engine is not closed.
